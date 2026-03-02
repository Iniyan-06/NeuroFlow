# NeuroFlow OS - Adaptive Focus System

**Cognitive Load Redistribution - Energy-Aware Task Prioritization - Overload Control**  
**Next.js - FastAPI - SQLite - Rule-Based Intelligence**

<div align="center">
  <img src="https://img.shields.io/badge/Frontend-Next.js%2016-black?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge" />
  <img src="https://img.shields.io/badge/State-Zustand-764ABC?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Live%20Demo-success?style=for-the-badge" />
</div>

---

## Live Demo
https://neuro-flow-swart.vercel.app/

---

## Table of Contents
- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Core Features](#core-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Run Locally (Judges)](#run-locally-judges)
- [API Endpoints](#api-endpoints)
- [Database](#database)
- [Demo Flow for Judges](#demo-flow-for-judges)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview
NeuroFlow OS is a focus operating system for people who feel overloaded by long task lists.  
It classifies tasks, recommends the next best action, adapts to current energy (`Low`, `Medium`, `Sharp`), and keeps a lightweight event trail in SQLite.

---

## Problem Statement
Most productivity tools fail during overload because they:
- treat all tasks equally
- ignore energy and time constraints
- encourage context switching
- do not simplify decisions in critical moments

---

## Solution
NeuroFlow OS uses a CLR-style approach:
- classify each task into:
  - `Survival-critical`
  - `Long-term meaningful`
  - `Routine repetitive`
  - `Noise`
- compute recommendation from:
  - tier weight
  - energy match
  - time fit
- allow manual focus selection when the user wants direct control
- persist important activity:
  - critical tasks
  - focus selection events

---

## Core Features
- Energy-aware focus switching (`Low`, `Medium`, `Sharp`)
- One-click "Set as focus"
- Overload support flow ("I feel overwhelmed")
- Critical task auto-capture into DB
- Focus event logging (`manual` and `auto`)
- Mobile + laptop responsive UI

---

## Architecture
1. Frontend collects tasks, energy, and available time.
2. Frontend calls internal Next.js API routes (`/api/recommend`, `/api/focus-task`).
3. Next.js API routes proxy requests to FastAPI backend (`localhost:8000`).
4. Backend classifies/recommends tasks and writes events to SQLite.
5. Frontend renders the final focus task and task breakdown view.

---

## Project Structure
```text
raptors/
|- main.py                      # FastAPI app entry
|- models.py                    # Pydantic schemas
|- engine.py                    # Classification logic
|- recommender.py               # Recommendation engine
|- overload_detector.py         # Overload scoring and interventions
|- monitor.py                   # Session behavior monitor
|- db.py                        # SQLite init + persistence functions
|- neuroflow.db                 # Local SQLite DB
|- frontend/
   |- app/
      |- api/recommend/route.ts # Proxy: frontend -> backend /recommend
      |- api/focus-task/route.ts# Proxy: frontend -> backend /focus-task
      |- page.tsx               # Focus page
      |- tasks/page.tsx         # Task breakdown page
   |- lib/store.ts              # Zustand state + focus logic
```

---

## Tech Stack
- Frontend: Next.js 16, React 19, TypeScript, Tailwind CSS, Zustand
- Backend: Python, FastAPI, Pydantic, Uvicorn
- Database: SQLite

---

## Run Locally (Judges)

### Prerequisites
- Python 3.10+
- Node.js 18+ (20+ recommended)
- npm

### 1. Clone
```bash
git clone <your-repo-url>
cd raptors
```

### 2. Start Backend
```bash
pip install fastapi uvicorn pydantic
python main.py
```
Backend: `http://127.0.0.1:8000`  
API docs: `http://127.0.0.1:8000/docs`

### 3. Start Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```
Frontend: `http://localhost:3000`

### 4. Optional Env
If backend is not running on default host:
`frontend/.env.local`
```env
BACKEND_BASE_URL=http://127.0.0.1:8000
```

---

## API Endpoints
- `POST /classify` - classify a single task
- `POST /recommend` - return recommended next action
- `GET /critical-tasks` - list critical tasks from DB
- `POST /focus-task` - save focus event into DB
- `GET /focus-events` - list focus event history
- `POST /overload/score` - score overload from explicit signals
- `POST /overload/event` - record behavior event
- `GET /overload/status` - current overload status from monitor
- `GET /google/gmail/tasks` - mock Gmail task extraction
- `GET /google/calendar/analysis` - mock Calendar analysis

---

## Database
SQLite file: `neuroflow.db`

Tables:
- `critical_tasks`
- `focus_events`

---

## Demo Flow for Judges
1. Open the live link: https://neuro-flow-swart.vercel.app/
2. Switch energy between `Low`, `Medium`, `Sharp`.
3. Confirm the focus task changes with energy mode.
4. Open **All Tasks** and click **Set as focus**.
5. Return to focus page and verify manual focus is retained.
6. Trigger **I feel overwhelmed** and verify simplification flow.
7. Query backend endpoints (`/critical-tasks`, `/focus-events`) to validate persistence.

---

## Testing
Available backend tests:
- `test_logic.py`
- `test_recommender.py`
- `test_overload.py`

Run:
```bash
python -m pytest
```
If needed:
```bash
pip install pytest
```

---

## Troubleshooting
- `POST /api/recommend 502`: backend is not running on `127.0.0.1:8000`.
- Focus briefly changes then resets: ensure latest `frontend/lib/store.ts` is used (energy-priority stable mode).
- Port conflicts: change frontend or backend port and update `BACKEND_BASE_URL`.

---

## License
MIT (see `LICENSE`)
