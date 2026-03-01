"""
NeuroFlow OS: Cognitive Overload Detection System
================================================
Detects cognitive overload in real-time using 4 behavioral signals:
  - open_tasks:        Number of currently active tasks
  - context_switches:  Task switches in the last hour
  - postpone_rate:     Proportion of tasks deferred vs. completed
  - stall_minutes:     Minutes actively working without any completion

Overwhelm Score Formula (0-100):
  OS = (T * 0.30) + (C * 0.30) + (P * 0.25) + (S * 0.15)
where each component is normalized to 0-100 before weighting.

Thresholds:
  < 40   → CLEAR   (normal state)
  40-69  → CAUTION (early fatigue signs)
  70-84  → WARNING (overload approaching)
  ≥ 85   → CRITICAL (intervention required)
"""

from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Optional
import math


class OverloadLevel(str, Enum):
    CLEAR = "clear"
    CAUTION = "caution"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class OverloadSignals:
    open_tasks: int                 # absolute count
    context_switches_per_hour: int  # raw count
    postpone_rate: float            # 0.0 – 1.0  (proportion)
    stall_minutes: float            # minutes without completion


@dataclass
class OverloadResult:
    raw_score: float
    level: OverloadLevel
    component_scores: dict          # breakdown for transparency
    intervention: "Intervention"


@dataclass
class Intervention:
    message: str
    actions: List[str]
    ux_mode: str                    # "normal" | "calm" | "minimal" | "lockdown"
    suppress_noise: bool
    suggest_break: bool


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------

def _normalize_tasks(n: int) -> float:
    """0→0, 5→50, 10→80, 20→100  (logarithmic)"""
    if n <= 0:
        return 0.0
    return min(100.0, 100 * math.log(n + 1) / math.log(21))


def _normalize_switches(sw: int) -> float:
    """0→0, 6→50, 12→75, 20+→100  (logarithmic, 20 = ceiling)"""
    if sw <= 0:
        return 0.0
    return min(100.0, 100 * math.log(sw + 1) / math.log(21))


def _normalize_postpone(rate: float) -> float:
    """Direct 0-1 → 0-100 with gentle curve"""
    rate = max(0.0, min(1.0, rate))
    return round(rate ** 0.8 * 100, 2)


def _normalize_stall(minutes: float) -> float:
    """0→0, 30→50, 60→75, 120+→100"""
    if minutes <= 0:
        return 0.0
    return min(100.0, 100 * math.log(minutes + 1) / math.log(121))


# ---------------------------------------------------------------------------
# Thresholding
# ---------------------------------------------------------------------------

def _level(score: float) -> OverloadLevel:
    if score >= 85:
        return OverloadLevel.CRITICAL
    if score >= 70:
        return OverloadLevel.WARNING
    if score >= 40:
        return OverloadLevel.CAUTION
    return OverloadLevel.CLEAR


# ---------------------------------------------------------------------------
# Intervention Catalogue
# ---------------------------------------------------------------------------

INTERVENTIONS: dict[OverloadLevel, Intervention] = {
    OverloadLevel.CLEAR: Intervention(
        message="You're in the zone. Keep it up.",
        actions=[
            "Continue with your current task.",
            "Review your task list in 30 minutes.",
        ],
        ux_mode="normal",
        suppress_noise=False,
        suggest_break=False,
    ),
    OverloadLevel.CAUTION: Intervention(
        message="Early fatigue signals detected. Let's simplify.",
        actions=[
            "Hide all Routine and Noise tasks from the dashboard.",
            "Set a 5-minute micro-break reminder.",
            "Disable non-critical notifications for 1 hour.",
        ],
        ux_mode="calm",
        suppress_noise=True,
        suggest_break=False,
    ),
    OverloadLevel.WARNING: Intervention(
        message="You're approaching overload. Time to reduce load.",
        actions=[
            "Switch the dashboard to Minimal mode (1-task view only).",
            "Automatically defer all Routine tasks by 24h.",
            "Prompt the user with the 'Overwhelmed' flow.",
            "Suggest a 10-minute walk or breathing exercise.",
        ],
        ux_mode="minimal",
        suppress_noise=True,
        suggest_break=True,
    ),
    OverloadLevel.CRITICAL: Intervention(
        message="Cognitive overload detected. Intervention required now.",
        actions=[
            "Lock the UI to show ONLY the single most critical task.",
            "Send a push notification: 'NeuroFlow recommends a 20m break.'",
            "Auto-defer all non-Critical tasks to tomorrow.",
            "Offer a guided 4-7-8 breathing exercise on-screen.",
            "Log this event for the weekly cognitive pattern report.",
        ],
        ux_mode="lockdown",
        suppress_noise=True,
        suggest_break=True,
    ),
}


# ---------------------------------------------------------------------------
# Main Engine
# ---------------------------------------------------------------------------

class OverloadDetector:

    # Weights — must sum to 1.0
    W_TASKS = 0.30
    W_SWITCHES = 0.30
    W_POSTPONE = 0.25
    W_STALL = 0.15

    @classmethod
    def score(cls, signals: OverloadSignals) -> OverloadResult:
        t_score = _normalize_tasks(signals.open_tasks)
        c_score = _normalize_switches(signals.context_switches_per_hour)
        p_score = _normalize_postpone(signals.postpone_rate)
        s_score = _normalize_stall(signals.stall_minutes)

        raw = (
            t_score * cls.W_TASKS
            + c_score * cls.W_SWITCHES
            + p_score * cls.W_POSTPONE
            + s_score * cls.W_STALL
        )

        level = _level(raw)

        return OverloadResult(
            raw_score=round(raw, 2),
            level=level,
            component_scores={
                "tasks_score": round(t_score, 1),
                "context_switch_score": round(c_score, 1),
                "postpone_score": round(p_score, 1),
                "stall_score": round(s_score, 1),
            },
            intervention=INTERVENTIONS[level],
        )
