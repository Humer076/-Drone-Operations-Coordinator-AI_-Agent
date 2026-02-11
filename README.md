# Skylark Drones – Drone Operations Coordinator AI Agent

## Overview

This project implements an AI-powered Drone Operations Coordinator for Skylark Drones.  
The system assists in managing pilot assignments, drone inventory, mission coordination, and conflict detection across multiple projects.

The application is built using Streamlit and integrates directly with Google Sheets for real-time two-way data synchronization.

---

## Problem Addressed

Skylark Drones currently manages:

- Pilot roster and availability
- Drone fleet tracking
- Project assignment coordination
- Conflict detection and resolution

These processes require high coordination and context switching.

This AI Agent reduces manual effort by:
- Automating pilot-mission matching
- Detecting scheduling conflicts
- Flagging equipment mismatches
- Supporting urgent reassignment decisions

---

## Key Features

### 1. Pilot Roster Management
- View all pilots and their current assignments
- Update pilot status (Available / On Leave / Unavailable)
- Sync updates directly to Google Sheets
- Query available pilots via conversational interface

---

### 2. Drone Fleet Management
- Track drone availability and deployment status
- Identify drones under maintenance
- Validate drone capabilities against mission requirements
- Sync drone status updates to Google Sheets

---

### 3. Mission Assignment Coordination
- Match pilots based on:
  - Skill compatibility
  - Required certifications
  - Location alignment
  - Availability
- Match drones based on:
  - Capability compatibility
  - Maintenance status
  - Deployment conflicts
- Prevent invalid assignments

---

### 4. Conflict Detection

The system automatically detects:

- Pilot double-booking across overlapping mission dates
- Drone double-booking across overlapping mission dates
- Skill mismatch
- Certification mismatch
- Drone capability mismatch
- Location mismatch
- Assignment during maintenance

Assignments are blocked when conflicts are detected.

---

### 5. Urgent Reassignment Logic

For High or Urgent priority missions:

- The system evaluates pilots currently assigned to Low priority missions.
- Suggests reassignment when appropriate.
- Prevents reassignment if it impacts equal or higher priority missions.

This ensures intelligent resource prioritization.

---

### 6. Conversational Interface

The AI Coordinator supports basic operational queries via chat input.

Supported examples:

- `available pilots`
- `urgent missions`
- `drones in maintenance`

This satisfies the conversational interface requirement.

---

## System Architecture

Frontend:
- Streamlit

Backend Logic:
- Rule-based decision engine
- Conflict validation functions
- Date overlap detection

Data Layer:
- Google Sheets (via gspread API)
- Two-way synchronization

---

## Date Conflict Detection

The system uses date overlap logic:


This ensures:
- No overlapping pilot assignments
- No overlapping drone deployments

---

## Technology Stack

- Python
- Streamlit
- Pandas
- gspread
- Google OAuth Service Account

---

## Google Sheets Integration

The system reads from:
- pilot_roster sheet
- drone_fleet sheet
- missions sheet

The system writes updates to:
- Pilot status
- Pilot assignment
- Drone status
- Drone assignment

All updates sync in real-time.

---

## Assumptions

- One pilot per mission
- One drone per mission
- Dates are formatted as YYYY-MM-DD
- Capabilities must explicitly match mission required skill
- Priority levels: Low, Medium, High, Urgent

---

## Edge Cases Handled

- Overlapping mission dates
- Drone under maintenance
- Pilot unavailable or on leave
- Location mismatch
- Skill mismatch
- Certification mismatch
- Drone capability mismatch
- Urgent reassignment from lower priority missions

---

## What Could Be Improved (Future Work)

- Optimization-based assignment (instead of first eligible pilot)
- Semantic capability mapping (e.g., LiDAR → Mapping)
- Historical assignment tracking
- Full LLM-based conversational reasoning
- Slack / email integration for notifications
- Multi-pilot missions

---

## Deployment

The application is deployed using Streamlit Cloud and connected to GitHub for automatic CI/CD deployment.

---

## Conclusion

This AI Agent reduces manual coordination overhead by:

- Automating mission assignments
- Preventing scheduling conflicts
- Ensuring compliance with skill and certification requirements
- Supporting urgent mission prioritization
- Providing real-time operational visibility

The system is scalable and can be extended with optimization models or advanced AI reasoning in future iterations.
