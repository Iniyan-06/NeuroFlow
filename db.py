import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent / "neuroflow.db"


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS critical_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                score REAL NOT NULL,
                next_action TEXT NOT NULL,
                reasoning TEXT NOT NULL,
                source TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS focus_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                energy TEXT NOT NULL,
                source TEXT NOT NULL,
                tier TEXT NOT NULL,
                score REAL NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_critical_task(task: dict[str, Any], source: str) -> None:
    with _get_conn() as conn:
        conn.execute(
            """
            INSERT INTO critical_tasks (description, score, next_action, reasoning, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                task.get("description", ""),
                float(task.get("score", 0.0)),
                task.get("next_action", ""),
                task.get("reasoning", ""),
                source,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()


def list_critical_tasks(limit: int = 50) -> list[dict[str, Any]]:
    safe_limit = max(1, min(limit, 200))
    with _get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, description, score, next_action, reasoning, source, created_at
            FROM critical_tasks
            ORDER BY id DESC
            LIMIT ?
            """,
            (safe_limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def save_focus_event(
    description: str,
    energy: str,
    source: str,
    tier: str,
    score: float,
) -> None:
    with _get_conn() as conn:
        conn.execute(
            """
            INSERT INTO focus_events (description, energy, source, tier, score, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                description,
                energy,
                source,
                tier,
                float(score),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()


def list_focus_events(limit: int = 50) -> list[dict[str, Any]]:
    safe_limit = max(1, min(limit, 200))
    with _get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, description, energy, source, tier, score, created_at
            FROM focus_events
            ORDER BY id DESC
            LIMIT ?
            """,
            (safe_limit,),
        ).fetchall()
    return [dict(row) for row in rows]
