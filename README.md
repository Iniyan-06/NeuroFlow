# NeuroFlow OS

NeuroFlow OS is a cognitive load management app that classifies tasks, recommends what to do next, adapts to your current energy (`Low`, `Medium`, `High/Sharp`), and records critical/focus events in a local database.

This project includes:
- A **FastAPI backend** (`localhost:8000`) with task intelligence APIs
- A **Next.js frontend** (`localhost:3000`) with responsive UI for mobile + laptop
- A **SQLite database** (`neuroflow.db`) for critical tasks and focus activity

## Live Demo
https://neuro-flow-swart.vercel.app/

## Problem
People keep long task lists but still lose time due to:
- Poor prioritization
- Mismatch between task difficulty and current energy
- Frequent context switching and overload

## Solution
NeuroFlow OS applies a CLR-style approach:
- Scores and classifies tasks into tiers:
  - `Survival-critical`
  - `Long-term meaningful`
  - `Routine repetitive`
  - `Noise`
- Recommends one best task based on:
  - Task tier
  - User energy
  - Available time
- Supports manual focus selection and logs focus events
- Detects overload and suggests interventions
- Persists critical tasks and focus actions in SQLite

## Tech Stack
- Backend: Python, FastAPI, Pydantic, Uvicorn
- Frontend: Next.js 16, React 19, TypeScript, Tailwind CSS, Zustand
- Database: SQLite (`neuroflow.db`)

## Project Structure
```text
raptors/
  main.py                    # FastAPI entry point
  models.py                  # Request/response schemas
  engine.py                  # Task classification engine
  recommender.py             # Recommendation scoring
  overload_detector.py       # Overload scoring + interventions
  monitor.py                 # Session event monitor
  db.py                      # SQLite init and persistence helpers
  neuroflow.db               # Local SQLite database
  frontend/                  # Next.js app
    app/
      api/recommend/route.ts # Frontend proxy -> backend /recommend
      api/focus-task/route.ts# Frontend proxy -> backend /focus-task
      page.tsx               # Focus page
      tasks/page.tsx         # Task list page
```

## Local Setup (Judges)

### 1) Prerequisites
- Python `3.10+`
- Node.js `18+` (Node `20+` recommended)
- npm

### 2) Clone and open project
```bash
git clone <your-repo-url>
cd raptors
```

### 3) Backend setup and run
Install backend packages:
```bash
pip install fastapi uvicorn pydantic
```

Start backend:
```bash
python main.py
```

Backend will run on:
- `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`

### 4) Frontend setup and run
Open another terminal:
```bash
cd frontend
npm install
npm run dev
```

Frontend will run on:
- `http://localhost:3000`

## Configuration
Frontend API routes forward to backend using:
- `BACKEND_BASE_URL` (optional)

Default (if not set):
- `http://127.0.0.1:8000`

If your backend runs elsewhere, create `frontend/.env.local`:
```env
BACKEND_BASE_URL=http://127.0.0.1:8000
```

## How to Use (Demo Flow for Judges)
1. Open `http://localhost:3000`
2. Select energy (`Low`, `Medium`, `Sharp`)
3. Observe focus task update based on energy
4. Go to **All tasks**
5. Click **Set as focus** on any task
6. Return to focus screen and verify manual focus is applied
7. (Optional) Click **I feel overwhelmed** to see overload simplification UI

## Key API Endpoints
- `POST /classify` - classify one task
- `POST /recommend` - recommend best next task
- `GET /critical-tasks` - list stored critical tasks
- `POST /focus-task` - store focus event
- `GET /focus-events` - list focus events
- `POST /overload/score` - overload score from signals
- `POST /overload/event` - record session event
- `GET /overload/status` - current overload status
- `GET /google/gmail/tasks` - mock Gmail task extraction
- `GET /google/calendar/analysis` - mock Calendar analysis

## Database Details
SQLite DB file:
- `neuroflow.db`

Tables:
- `critical_tasks`
  - Populated when `Survival-critical` tasks are classified/recommended
- `focus_events`
  - Populated when user focus is set (manual/auto source)

## Testing
Backend test files available:
- `test_logic.py`
- `test_recommender.py`
- `test_overload.py`

Run with:
```bash
python -m pytest
```
If `pytest` is missing:
```bash
pip install pytest
```

## Notes
- Backend and frontend must both be running.
- If frontend shows `502` on `/api/recommend`, backend is likely not running.
- The UI is responsive for both mobile and laptop screens.

## License
MIT (see `LICENSE`)
