"""
NeuroFlow OS: Session Monitor
=============================
Tracks in-memory behavioral telemetry for the current user session.
Stores a fixed sliding window of events (context switches, completions,
postponements) and derives the 4 signals needed by OverloadDetector.

In a production system, replace the in-memory store with Redis or Postgres.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from collections import deque
from typing import Deque, List
import threading


@dataclass
class SessionEvent:
    event_type: str         # "switch" | "complete" | "postpone" | "start"
    task_id: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class SessionMonitor:
    """Thread-safe, in-memory behavioral session tracker."""

    def __init__(self, window_hours: int = 1, max_events: int = 500):
        self._lock = threading.Lock()
        self._window = timedelta(hours=window_hours)
        self._events: Deque[SessionEvent] = deque(maxlen=max_events)
        self._session_start: datetime = datetime.now(timezone.utc)
        self._last_completion: datetime = datetime.now(timezone.utc)
        self._open_tasks: int = 0

    # ------------------------------------------------------------------
    # Public event API
    # ------------------------------------------------------------------

    def record_start(self, task_id: str):
        with self._lock:
            self._events.append(SessionEvent("start", task_id))

    def record_switch(self, from_task: str, to_task: str):
        """Call whenever the user navigates to a different task."""
        with self._lock:
            self._events.append(SessionEvent("switch", from_task))

    def record_complete(self, task_id: str):
        with self._lock:
            self._events.append(SessionEvent("complete", task_id))
            self._last_completion = datetime.now(timezone.utc)
            self._open_tasks = max(0, self._open_tasks - 1)

    def record_postpone(self, task_id: str):
        with self._lock:
            self._events.append(SessionEvent("postpone", task_id))

    def set_open_tasks(self, count: int):
        with self._lock:
            self._open_tasks = max(0, count)

    # ------------------------------------------------------------------
    # Signal Derivation
    # ------------------------------------------------------------------

    def _recent_events(self, event_type: str) -> List[SessionEvent]:
        cutoff = datetime.now(timezone.utc) - self._window
        return [e for e in self._events if e.event_type == event_type and e.timestamp >= cutoff]

    def context_switches_per_hour(self) -> int:
        return len(self._recent_events("switch"))

    def postpone_rate(self) -> float:
        recent_completes = len(self._recent_events("complete"))
        recent_postpones = len(self._recent_events("postpone"))
        total = recent_completes + recent_postpones
        if total == 0:
            return 0.0
        return round(recent_postpones / total, 3)

    def stall_minutes(self) -> float:
        """Minutes elapsed since the last task completion."""
        now = datetime.now(timezone.utc)
        delta = (now - self._last_completion).total_seconds() / 60
        return round(delta, 1)

    def derive_signals(self) -> dict:
        with self._lock:
            return {
                "open_tasks": self._open_tasks,
                "context_switches_per_hour": self.context_switches_per_hour(),
                "postpone_rate": self.postpone_rate(),
                "stall_minutes": self.stall_minutes(),
            }


# ---------------------------------------------------------------------------
# Singleton for the FastAPI app to share
# ---------------------------------------------------------------------------
monitor = SessionMonitor()
