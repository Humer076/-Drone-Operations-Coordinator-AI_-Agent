from datetime import datetime

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def has_overlap(start1, end1, start2, end2):
    return max(start1, start2) <= min(end1, end2)

# =====================================================
# MISSION ASSIGNMENT & EVALUATION
# =====================================================

st.divider()
st.subheader("Mission Assignment Evaluation")

mission = mission_df[
    mission_df["project_id"] == sel_project
].iloc[0]

mission_start = parse_date(mission["start_date"])
mission_end = parse_date(mission["end_date"])

st.markdown(f"""
**Project:** {mission['project_id']}  
**Location:** {mission['location']}  
**Required Skill:** {mission['required_skills']}  
**Required Certification:** {mission['required_certs']}  
**Priority:** {mission['priority']}  
**Dates:** {mission['start_date']} → {mission['end_date']}
""")

is_urgent = mission["priority"].lower() in ["high", "urgent"]

if is_urgent:
    st.warning("🚨 Urgent Mission — Reassignment Logic Enabled")

# =====================================================
# DRONE VALIDATION
# =====================================================

st.subheader("Drone Evaluation")

selected_drone = st.selectbox(
    "Select Drone for Mission",
    drone_df["drone_id"].tolist()
)

drone = drone_df[
    drone_df["drone_id"] == selected_drone
].iloc[0]

drone_conflict = False

if drone["status"].lower() in ["maintenance", "in maintenance"]:
    st.error("❌ Drone is under maintenance")
    drone_conflict = True

elif drone["status"].lower() == "deployed":
    # Check date overlap
    assigned_mission = drone["current_assignment"]
    if assigned_mission:
        existing = mission_df[
            mission_df["project_id"] == assigned_mission
        ].iloc[0]

        existing_start = parse_date(existing["start_date"])
        existing_end = parse_date(existing["end_date"])

        if has_overlap(mission_start, mission_end, existing_start, existing_end):
            st.error("❌ Drone is double-booked for overlapping mission")
            drone_conflict = True

if drone["location"] != mission["location"]:
    st.warning("⚠ Drone location mismatch")

# =====================================================
# PILOT EVALUATION
# =====================================================

st.subheader("Pilot Evaluation")

required_skill = mission["required_skills"].lower()
required_cert = mission["required_certs"].lower()

eligible = []
reassign_candidates = []
rejected = []

for _, p in pilot_df.iterrows():

    skills = [s.strip().lower() for s in str(p["skills"]).split(",")]
    certs = [c.strip().lower() for c in str(p["certifications"]).split(",")]

    if required_skill not in skills:
        rejected.append((p["name"], "Missing skill"))
        continue

    if required_cert not in certs:
        rejected.append((p["name"], "Missing certification"))
        continue

    if p["location"] != mission["location"]:
        rejected.append((p["name"], "Location mismatch"))
        continue

    # If Available → directly eligible
    if p["status"] == "Available":
        eligible.append(p)
        continue

    # If Assigned → check overlap
    if p["status"] == "Assigned" and p["current_assignment"]:
        existing = mission_df[
            mission_df["project_id"] == p["current_assignment"]
        ].iloc[0]

        existing_start = parse_date(existing["start_date"])
        existing_end = parse_date(existing["end_date"])

        overlap = has_overlap(
            mission_start, mission_end,
            existing_start, existing_end
        )

        if overlap:
            if is_urgent and existing["priority"].lower() == "low":
                reassign_candidates.append(p)
            else:
                rejected.append((p["name"], "Overlapping mission"))
        else:
            eligible.append(p)

    else:
        rejected.append((p["name"], f"Status: {p['status']}"))

# =====================================================
# ASSIGNMENT DECISION
# =====================================================

st.divider()
st.subheader("Assignment Recommendation")

if drone_conflict:
    st.error("Resolve drone conflicts before assignment.")

elif eligible:
    chosen = eligible[0]
    st.success(f"✅ Recommended Pilot: {chosen['name']} (Available)")

    if st.button("Confirm Assignment"):
        row = pilot_df[
            pilot_df["name"] == chosen["name"]
        ].index[0] + 2

        pilot_ws.update(f"F{row}", [["Assigned"]])
        pilot_ws.update(f"G{row}", [[mission["project_id"]]])

        st.success("Pilot assigned successfully.")

elif reassign_candidates:
    st.warning("⚠ No free pilots — Urgent reassignment possible.")

    candidate = reassign_candidates[0]
    st.info(
        f"Suggested Reassignment: {candidate['name']} "
        f"(Currently on low priority mission)"
    )

else:
    st.error("❌ No suitable pilot found.")

# =====================================================
# REJECTION EXPLANATION
# =====================================================

with st.expander("Why other pilots were rejected"):
    for name, reason in rejected:
        st.write(f"{name} → {reason}")
