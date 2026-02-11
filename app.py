import streamlit as st
from sheets import get_sheet
from datetime import datetime

st.set_page_config(page_title="Skylark Drone Ops", layout="wide")
st.title("Drone Operations Coordinator AI Agent")

# =====================================================
# LOAD DATA
# =====================================================

pilot_df, pilot_ws = get_sheet("pilot_roster")
mission_df, mission_ws = get_sheet("missions")
drone_df, drone_ws = get_sheet("drone_fleet")

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def parse_date(date_str):
    return datetime.strptime(str(date_str), "%Y-%m-%d")

def has_overlap(start1, end1, start2, end2):
    return max(start1, start2) <= min(end1, end2)

# =====================================================
# SIDEBAR OPERATIONS
# =====================================================

st.sidebar.header("Operations Panel")

# Pilot Status Update
st.sidebar.subheader("Update Pilot Status")

sel_pilot = st.sidebar.selectbox("Pilot", pilot_df["name"].tolist())
new_pilot_status = st.sidebar.selectbox(
    "Status", ["Available", "On Leave", "Unavailable"]
)

if st.sidebar.button("Update Pilot"):
    row = pilot_df[pilot_df["name"] == sel_pilot].index[0] + 2
    pilot_ws.update(f"F{row}", [[new_pilot_status]])
    st.sidebar.success("Pilot status updated")

# Drone Status Update
st.sidebar.subheader("Update Drone Status")

sel_drone = st.sidebar.selectbox("Drone", drone_df["drone_id"].tolist())
new_drone_status = st.sidebar.selectbox(
    "Status", ["Available", "Deployed", "In Maintenance"]
)

if st.sidebar.button("Update Drone"):
    row = drone_df[drone_df["drone_id"] == sel_drone].index[0] + 2
    drone_ws.update(f"D{row}", [[new_drone_status]])
    st.sidebar.success("Drone status updated")

# Mission Selection
st.sidebar.subheader("Mission Selection")
sel_project = st.sidebar.selectbox(
    "Mission", mission_df["project_id"].tolist()
)

# =====================================================
# DATA DISPLAY
# =====================================================

st.subheader("Pilot Roster")
st.dataframe(pilot_df, use_container_width=True)

st.subheader("Missions")
st.dataframe(mission_df, use_container_width=True)

st.subheader("Drone Inventory")
st.dataframe(drone_df, use_container_width=True)

# =====================================================
# MISSION EVALUATION
# =====================================================

st.divider()
st.subheader("Mission Assignment Evaluation")

mission = mission_df[
    mission_df["project_id"] == sel_project
].iloc[0]

mission_start = parse_date(mission["start_date"])
mission_end = parse_date(mission["end_date"])
is_urgent = mission["priority"].lower() in ["high", "urgent"]

st.markdown(f"""
**Project:** {mission['project_id']}  
**Location:** {mission['location']}  
**Required Skill:** {mission['required_skills']}  
**Required Certification:** {mission['required_certs']}  
**Priority:** {mission['priority']}  
**Dates:** {mission['start_date']} to {mission['end_date']}
""")

if is_urgent:
    st.warning("Urgent mission - reassignment logic active")

# =====================================================
# DRONE EVALUATION
# =====================================================

st.subheader("Drone Evaluation")

selected_drone = st.selectbox(
    "Select Drone for Mission", drone_df["drone_id"].tolist()
)

drone = drone_df[
    drone_df["drone_id"] == selected_drone
].iloc[0]

drone_conflict = False

# Maintenance check
if drone["status"].lower() in ["maintenance", "in maintenance"]:
    st.error("Drone is under maintenance")
    drone_conflict = True

# Double booking check
if drone["current_assignment"]:
    assigned = mission_df[
        mission_df["project_id"] == drone["current_assignment"]
    ]

    if not assigned.empty:
        assigned = assigned.iloc[0]
        a_start = parse_date(assigned["start_date"])
        a_end = parse_date(assigned["end_date"])

        if has_overlap(mission_start, mission_end, a_start, a_end):
            if is_urgent and assigned["priority"].lower() == "low":
                st.warning("Drone can be reassigned from low priority mission")
            else:
                st.error("Drone is double-booked")
                drone_conflict = True

# Capability check
if mission["required_skills"].lower() not in str(drone["capabilities"]).lower():
    st.error("Drone lacks required capability")
    drone_conflict = True

# Location warning
if drone["location"] != mission["location"]:
    st.warning("Drone location mismatch")

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

    if p["status"] == "Available":
        eligible.append(p)
        continue

    if p["current_assignment"]:
        assigned = mission_df[
            mission_df["project_id"] == p["current_assignment"]
        ]

        if not assigned.empty:
            assigned = assigned.iloc[0]
            a_start = parse_date(assigned["start_date"])
            a_end = parse_date(assigned["end_date"])

            if has_overlap(mission_start, mission_end, a_start, a_end):
                if is_urgent and assigned["priority"].lower() == "low":
                    reassign_candidates.append(p)
                else:
                    rejected.append((p["name"], "Overlapping mission"))
            else:
                eligible.append(p)
        else:
            eligible.append(p)

    else:
        rejected.append((p["name"], f"Status: {p['status']}"))

# =====================================================
# FINAL ASSIGNMENT DECISION
# =====================================================

st.divider()
st.subheader("Assignment Recommendation")

if drone_conflict:
    st.error("Resolve drone issues before assigning pilot.")

elif eligible:
    chosen = eligible[0]
    st.success(f"Recommended Pilot: {chosen['name']}")

    if st.button("Confirm Assignment"):
        row = pilot_df[pilot_df["name"] == chosen["name"]].index[0] + 2
        pilot_ws.update(f"F{row}", [["Assigned"]])
        pilot_ws.update(f"G{row}", [[mission["project_id"]]])

        drone_row = drone_df[
            drone_df["drone_id"] == selected_drone
        ].index[0] + 2

        drone_ws.update(f"D{drone_row}", [["Deployed"]])
        drone_ws.update(f"F{drone_row}", [[mission["project_id"]]])

        st.success("Pilot and Drone successfully assigned.")

elif reassign_candidates:
    candidate = reassign_candidates[0]
    st.warning("No free pilots. Urgent reassignment suggested.")
    st.info(
        f"Suggested Reassignment: {candidate['name']} "
        f"(currently on low priority mission)"
    )

else:
    st.error("No suitable pilot available.")

# =====================================================
# REJECTION EXPLANATION
# =====================================================

with st.expander("Why other pilots were rejected"):
    for name, reason in rejected:
        st.write(f"{name} - {reason}")

# =====================================================
# CONVERSATIONAL INTERFACE
# =====================================================

st.divider()
st.subheader("Ask the AI Coordinator")

query = st.chat_input("Ask about pilots, drones, missions...")

if query:
    q = query.lower()

    if "available pilots" in q:
        available = pilot_df[pilot_df["status"] == "Available"]
        st.write(available[["name", "location"]])

    elif "urgent missions" in q:
        urgent = mission_df[
            mission_df["priority"].str.lower().isin(["high", "urgent"])
        ]
        st.write(urgent)

    elif "drones in maintenance" in q:
        maintenance = drone_df[
            drone_df["status"].str.contains("maintenance", case=False)
        ]
        st.write(maintenance)

    else:
        st.write(
            "Try asking: available pilots, urgent missions, or drones in maintenance."
        )
