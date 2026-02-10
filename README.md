# Drone-Operations-Coordinator-AI_Agent
 

# Drone Operations Coordinator AI Agent

An AI-powered operations dashboard built for Skylark Drones to streamline pilot coordination, mission assignments, drone inventory management, and conflict detection, fully synchronized with Google Sheets.

---

## Project Overview

Skylark Drones operates multiple drone missions simultaneously across locations and clients.  
This application acts as a Drone Operations Coordinator AI Agent, helping operations teams:

- Track pilot availability and assignments  
- Manage drone inventory and maintenance status  
- Match pilots and drones to missions based on requirements  
- Detect conflicts and edge cases before assignment  
- Handle urgent mission reassignments efficiently  

---

## Core Features

### 1. Pilot Roster Management
- View all pilots with skills, certifications, location, and status  
- Update pilot availability (Available / On Leave / Unavailable)  
- Sync updates back to Google Sheets (2-way sync)  

### 2. Mission Management
- View all missions with required skills, certifications, location, and priority  
- Highlight urgent and high-priority missions  
- Select missions for assignment evaluation  

### 3. Drone Inventory Management
- View drone fleet with capabilities and maintenance status  
- Update drone status (Available / Deployed / In Maintenance)  
- Automatically flag drones under maintenance  

### 4. Intelligent Assignment and Conflict Detection
- Recommend eligible pilots based on:
  - Location match  
  - Skill match  
  - Certification match  
  - Availability  

- Detect and warn about:
  - Pilot already assigned to another mission  
  - Skill or certification mismatch  
  - Pilot–mission location mismatch  
  - Drone–mission location mismatch  
  - Drone under maintenance  

### 5. Urgent Reassignment Support
- High or urgent priority missions trigger warnings  
- Allows reassignment from lower-priority tasks with human confirmation  

---

## User Interface

- Built using Streamlit  
- Sidebar-based operations panel for quick updates  
- Clear visual warnings and success indicators  
- Expandable explanations for rejected pilots  

---

## Tech Stack

- Frontend: Streamlit  
- Backend and Logic: Python  
- Data Source: Google Sheets  

### Libraries Used
- gspread  
- google-auth  
- pandas  

---

## Google Sheets Integration

- Read access:
  - Pilot Roster  
  - Missions  
  - Drone Fleet  

- Write access:
  - Pilot status updates  
  - Pilot assignments  
  - Drone status updates  

Authentication is handled using a Google Service Account configured through Streamlit Secrets.

---

## Repository Structure

Drone-Operations-Coordinator-AI-Agent/
│
├── app.py
│   # Main Streamlit application
│   # Handles UI, mission assignment, conflict detection, and updates
│
├── sheets.py
│   # Google Sheets integration logic
│   # Reads and writes pilot, mission, and drone data
│
├── requirements.txt
│   # Python dependencies required to run the project
│
├── README.md
│   # Project overview, features, tech stack, and usage instructions
│
├── .streamlit/
│   └── secrets.toml
│       # Google Service Account credentials (NOT committed to GitHub)
│
└── .gitignore
    # Excludes secrets, cache files, and virtual environments


