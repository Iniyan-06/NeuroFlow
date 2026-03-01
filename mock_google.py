"""
NeuroFlow OS: Mock Google Data (Demo Mode)
==========================================
Returns realistic mock responses for Gmail and Calendar endpoints
so the full API works without any OAuth credentials or Google account.
Set GOOGLE_DEMO_MODE=1 (or simply don't have client_secret.json) to use this.
"""

from datetime import datetime, timedelta, timezone

_now = datetime.now(timezone.utc)


def mock_gmail_tasks():
    return {
        "source": "gmail",
        "mode": "demo",
        "tasks_found": 3,
        "tasks": [
            {
                "source": "gmail",
                "message_id": "demo_msg_001",
                "thread_id": "demo_thread_001",
                "description": "[Email] Action required: Review and approve the Q2 budget proposal — from Finance Team",
                "score": 78.3,
                "tier": "Long-term meaningful",
                "next_action": "Schedule peak focus time for this.",
                "reasoning": "U:60 I:100 E:20 Em:70",
                "deadline": (_now + timedelta(days=2)).isoformat(),
                "estimated_effort_hours": 1.0,
                "emotional_weight": 7,
                "frequency": "once",
            },
            {
                "source": "gmail",
                "message_id": "demo_msg_002",
                "thread_id": "demo_thread_002",
                "description": "[Email] URGENT: Production deploy blocked — approval needed from DevOps",
                "score": 91.5,
                "tier": "Survival-critical",
                "next_action": "Execute immediately. Limit distractions.",
                "reasoning": "U:100 I:100 E:10 Em:90",
                "deadline": (_now + timedelta(hours=2)).isoformat(),
                "estimated_effort_hours": 0.25,
                "emotional_weight": 9,
                "frequency": "once",
            },
            {
                "source": "gmail",
                "message_id": "demo_msg_003",
                "thread_id": "demo_thread_003",
                "description": "[Email] Can you please review the updated onboarding doc? — from People Team",
                "score": 52.1,
                "tier": "Routine repetitive",
                "next_action": "Batch this with similar tasks later.",
                "reasoning": "U:30 I:40 E:10 Em:50",
                "deadline": None,
                "estimated_effort_hours": 0.5,
                "emotional_weight": 4,
                "frequency": "once",
            },
        ],
    }


def mock_calendar_analysis():
    today = _now.date().isoformat()
    tomorrow = (_now + timedelta(days=1)).date().isoformat()
    day3 = (_now + timedelta(days=2)).date().isoformat()

    return {
        "source": "calendar",
        "mode": "demo",
        "analysis_window_days": 7,
        "total_meetings": 11,
        "total_meeting_hours": 9.5,
        "overload_detected": True,
        "overloaded_days": [
            {
                "date": tomorrow,
                "meeting_count": 5,
                "total_hours": 4.5,
                "meetings": [
                    "Daily Standup",
                    "1:1 with Manager",
                    "Product Review",
                    "Design Sync",
                    "Quarterly Planning",
                ],
            },
            {
                "date": day3,
                "meeting_count": 4,
                "total_hours": 5.0,
                "meetings": [
                    "All Hands",
                    "Tech Roadmap",
                    "Customer Interview",
                    "Sprint Retrospective",
                ],
            },
        ],
        "reduction_suggestions": [
            "Trim \"Quarterly Planning\" — recurring meetings ≥60 min can often be cut to 30.",
            "Reduce \"All Hands\" attendance — 24 attendees. Consider async update instead.",
            "Convert \"Daily Standup\" to async — use a Slack thread update instead of 15m real-time meeting.",
            "Split \"Tech Roadmap\" — 90+ min blocks reduce focus. Break into two 45-min sessions.",
            "Trim \"Sprint Retrospective\" — recurring meetings ≥60 min can often be cut to 30.",
        ],
        "free_deep_work_blocks": [
            {
                "date": today,
                "start": (_now.replace(hour=10, minute=0, second=0)).isoformat(),
                "end": (_now.replace(hour=12, minute=30, second=0)).isoformat(),
                "duration_minutes": 150,
                "label": "Deep work slot",
            },
            {
                "date": tomorrow,
                "start": (_now + timedelta(days=1)).replace(hour=9, minute=0, second=0).isoformat(),
                "end": (_now + timedelta(days=1)).replace(hour=10, minute=0, second=0).isoformat(),
                "duration_minutes": 60,
                "label": "Deep work slot",
            },
        ],
        "auto_classified_tasks": [
            {
                "source": "calendar",
                "event_id": "demo_evt_001",
                "description": "[Calendar] Q2 Product Launch Milestone",
                "score": 82.0,
                "tier": "Survival-critical",
                "next_action": "Execute immediately. Limit distractions.",
                "reasoning": "U:80 I:100 E:50 Em:70",
                "deadline": (_now + timedelta(days=5)).isoformat(),
                "estimated_effort_hours": 2.0,
                "frequency": "once",
            },
        ],
    }
