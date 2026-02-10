import streamlit as st
from sheets import get_sheet

st.set_page_config(
    page_title="Skylark Drone Ops",
    layout="wide"
)

st.title(" Drone Operations Coordinator AI Agent")

# =====================================================
# LOAD DATA
# =====================================================
pilot_df, pilot_ws = get_sheet("pilot_roster")
mission_df, _ = get_sheet("missions")
drone_df, drone_ws = get_sheet("drone_fleet")

# =====================================================
# SIDEBAR — OPERATOR ACTIONS
# =====================================================
st.sidebar.header("Operations Panel")

# --- Pilot Status Update ---
st.sidebar.subheader("Update Pilot Status")

sel_pilot = st.sidebar.selectbox(
    "Pilot",
    pilot_df["name"].tolist()
)

new_pilot_status = st.sidebar.selectbox(
    "Status",
    ["Available", "On Leave", "Unavailable"]
)

if st.sidebar.button("Update Pilot"):
    row = pilot_df[pilot_df["name"] == sel_pilot].index[0] + 2
    pilot_ws.update(f"F{row}", [[new_pilot_status]])
    st.sidebar.success("Pilot status updated")

# --- Drone Status Update ---
st.sidebar.subheader("Update Drone Status")

sel_drone = st.sidebar.selectbox(
    "Drone",
    drone_df["drone_id"].tolist()
)

new_drone_status = st.sidebar.selectbox(
    "Status",
    ["Available", "Deployed", "In Maintenance"]
)

if st.sidebar.button("Update Drone"):
    row = drone_df[drone_df["drone_id"] == sel_drone].index[0] + 2
    drone_ws.update(f"D{row}", [[new_drone_status]])
    st.sidebar.success("Drone status updated")

# --- Mission Selection ---
st.sidebar.subheader("Mission Selection")

sel_project = st.sidebar.selectbox(
    "Mission",
    mission_df["project_id"].tolist()
)

# =====================================================
# MAIN PAGE — DATA VIEWS
# =====================================================
st.subheader("Pilot Roster")
st.dataframe(pilot_df, use_container_width=True)

st.subheader("Missions")
st.dataframe(mission_df, use_container_width=True)

st.subheader("Drone Inventory")
st.dataframe(drone_df, use_container_width=True)

# Maintenance warning
maintenance = drone_df[
    drone_df["status"].str.contains("Maintenance", case=False, na=False)
]
if not maintenance.empty:
    st.warning("Some drones are currently under maintenance")

# =====================================================
# MISSION ASSIGNMENT & EVALUATION
# =====================================================
st.divider()
st.subheader("Mission Assignment Evaluation")

mission = mission_df[
    mission_df["project_id"] == sel_project
].iloc[0]

st.markdown(
    f"""
    **Project:** {mission['project_id']}  
    **Location:** {mission['location']}  
    **Required Skill:** {mission['required_skills']}  
    **Required Certification:** {mission['required_certs']}  
    **Priority:** {mission['priority']}
    """
)

# Drone selection for mission
selected_drone = st.selectbox(
    "Select Drone for Mission",
    drone_df["drone_id"].tolist()
)

drone_row = drone_df[
    drone_df["drone_id"] == selected_drone
].iloc[0]

if drone_row["location"] != mission["location"]:
    st.warning(
        f"Drone is in {drone_row['location']} "
        f"but mission is in {mission['location']}."
    )

# =====================================================
# PILOT EVALUATION LOGIC
# =====================================================
required_skill = mission["required_skills"].strip().lower()
required_cert = mission["required_certs"].strip().lower()

eligible = []
rejected = []

for _, p in pilot_df.iterrows():
    skills = [s.strip().lower() for s in str(p["skills"]).split(",")]
    certs = [c.strip().lower() for c in str(p["certifications"]).split(",")]

    if p["location"] != mission["location"]:
        rejected.append((p["name"], "Location mismatch"))
        continue
    if p["status"] != "Available":
        rejected.append((p["name"], f"Status: {p['status']}"))
        continue
    if required_skill not in skills:
        rejected.append((p["name"], "Missing required skill"))
        continue
    if required_cert not in certs:
        rejected.append((p["name"], "Missing required certification"))
        continue

    eligible.append(p)

# =====================================================
# FINAL DECISION
# =====================================================
st.divider()
st.subheader("Assignment Result")

if eligible:
    chosen = eligible[0]
    st.success(f"Recommended Pilot: {chosen['name']}")

    if str(chosen["current_assignment"]).strip():
        st.warning(
            f"Pilot already assigned to {chosen['current_assignment']}. "
            "Verify date overlap before confirming."
        )

    if st.button("Assign Pilot to Mission"):
        row = pilot_df[pilot_df["name"] == chosen["name"]].index[0] + 2
        pilot_ws.update(f"F{row}", [["Assigned"]])
        pilot_ws.update(f"G{row}", [[mission["project_id"]]])
        st.success("Pilot assigned successfully")
else:
    st.error("No suitable pilot available")

with st.expander("Why other pilots were not selected"):
    for name, reason in rejected:
        st.write(f"{name}: {reason}")