from fastapi import FastAPI, HTTPException, Query
from models import TaskInput, TaskClassificationResponse, RecommendationRequest, RecommendationResponse
from engine import ClassificationEngine
from recommender import ActionRecommender
from overload_detector import OverloadDetector, OverloadSignals
from db import (
    init_db,
    save_critical_task,
    list_critical_tasks,
    save_focus_event,
    list_focus_events,
)
from monitor import monitor
from mock_google import mock_gmail_tasks, mock_calendar_analysis
from pydantic import BaseModel, Field
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="NeuroFlow OS: Cognitive Engine",
    description="CLR-based task classification, action recommendation, and overload detection.",
    version="0.2.0"
)

init_db()

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; refine for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Pydantic schemas for overload endpoints ─────────────────────────────────

class OverloadSignalInput(BaseModel):
    open_tasks: int = Field(..., ge=0)
    context_switches_per_hour: int = Field(..., ge=0)
    postpone_rate: float = Field(..., ge=0.0, le=1.0)
    stall_minutes: float = Field(..., ge=0.0)

class SessionEventInput(BaseModel):
    event_type: str        # "start" | "switch" | "complete" | "postpone"
    task_id: str
    to_task_id: Optional[str] = None
    open_task_count: Optional[int] = None

class FocusEventInput(BaseModel):
    description: str
    energy: str
    source: str
    tier: str
    score: float

# ─── Existing routes ──────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"message": "NeuroFlow OS v0.2 — /classify, /recommend, /overload/score, /overload/event, /overload/status"}

@app.post("/classify", response_model=TaskClassificationResponse)
async def classify_task(task: TaskInput):
    try:
        result = ClassificationEngine.classify(task)
        if result.get("tier") == "Survival-critical":
            save_critical_task(result, source="classify")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend", response_model=RecommendationResponse)
async def recommend_action(request: RecommendationRequest):
    try:
        result = ActionRecommender.recommend(request)
        selected = result.get("selected_task")
        if selected and selected.get("tier") == "Survival-critical":
            save_critical_task(selected, source="recommend")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/critical-tasks")
async def get_critical_tasks(limit: int = Query(default=50, ge=1, le=200)):
    try:
        return {"items": list_critical_tasks(limit=limit)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/focus-task")
async def record_focus_task(event: FocusEventInput):
    try:
        save_focus_event(
            description=event.description,
            energy=event.energy,
            source=event.source,
            tier=event.tier,
            score=event.score,
        )
        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/focus-events")
async def get_focus_events(limit: int = Query(default=50, ge=1, le=200)):
    try:
        return {"items": list_focus_events(limit=limit)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── Overload detection routes ────────────────────────────────────────────────

@app.post("/overload/score")
async def score_overload(signals: OverloadSignalInput):
    """
    Directly score a fully-formed set of behavioral signals.
    Use this for batch analysis or when you compute signals externally.
    """
    try:
        sig = OverloadSignals(
            open_tasks=signals.open_tasks,
            context_switches_per_hour=signals.context_switches_per_hour,
            postpone_rate=signals.postpone_rate,
            stall_minutes=signals.stall_minutes,
        )
        result = OverloadDetector.score(sig)
        return {
            "raw_score": result.raw_score,
            "level": result.level,
            "component_scores": result.component_scores,
            "intervention": {
                "message": result.intervention.message,
                "actions": result.intervention.actions,
                "ux_mode": result.intervention.ux_mode,
                "suppress_noise": result.intervention.suppress_noise,
                "suggest_break": result.intervention.suggest_break,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/overload/event")
async def record_event(event: SessionEventInput):
    """
    Record a raw behavioral event into the session monitor.
    The monitor auto-derives signals over the sliding 1h window.
    """
    try:
        if event.event_type == "start":
            monitor.record_start(event.task_id)
        elif event.event_type == "switch":
            monitor.record_switch(event.task_id, event.to_task_id or "")
        elif event.event_type == "complete":
            monitor.record_complete(event.task_id)
        elif event.event_type == "postpone":
            monitor.record_postpone(event.task_id)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown event_type: {event.event_type}")

        if event.open_task_count is not None:
            monitor.set_open_tasks(event.open_task_count)

        return {"status": "recorded", "event": event.event_type}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/overload/status")
async def get_overload_status():
    """
    Derive signals from the live session monitor and return current overload level.
    Call this on a polling interval (e.g., every 60s) from the frontend.
    """
    try:
        derived = monitor.derive_signals()
        sig = OverloadSignals(**derived)
        result = OverloadDetector.score(sig)
        return {
            "derived_signals": derived,
            "raw_score": result.raw_score,
            "level": result.level,
            "intervention": {
                "message": result.intervention.message,
                "actions": result.intervention.actions,
                "ux_mode": result.intervention.ux_mode,
                "suppress_noise": result.intervention.suppress_noise,
                "suggest_break": result.intervention.suggest_break,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── Gmail & Calendar routes (mock data, no OAuth) ───────────────────────────


@app.get("/google/gmail/tasks")
async def gmail_tasks(
    max_results: int = Query(default=20, ge=1, le=100),
    since_hours: int = Query(default=24, ge=1, le=168),
):
    """Returns actionable tasks auto-extracted from recent emails."""
    return mock_gmail_tasks()


@app.get("/google/calendar/analysis")
async def calendar_analysis(
    days_ahead: int = Query(default=7, ge=1, le=30),
):
    """Returns meeting overload analysis and free deep-work blocks."""
    return mock_calendar_analysis()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
