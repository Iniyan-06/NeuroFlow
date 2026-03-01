"""
Test cases for the Cognitive Overload Detection System.
Validates all 4 alert levels and edge cases.
"""
from overload_detector import OverloadDetector, OverloadSignals, OverloadLevel

PASS = "\033[92m✓ PASS\033[0m"
FAIL = "\033[91m✗ FAIL\033[0m"

def check(label: str, signals: dict, expected_level: OverloadLevel):
    sig = OverloadSignals(**signals)
    result = OverloadDetector.score(sig)
    ok = result.level == expected_level
    icon = PASS if ok else FAIL
    print(f"{icon}  [{result.level.upper():8s}] score={result.raw_score:5.1f}  {label}")
    for k, v in result.component_scores.items():
        print(f"         {k}: {v}")
    print(f"         → {result.intervention.message}")
    print(f"         UX Mode: {result.intervention.ux_mode} | Break: {result.intervention.suggest_break}")
    print()
    return ok

cases = [
    # ─── CLEAR ────────────────────────────────────────────────────────────────
    dict(
        label="All zeros — perfectly clear state",
        signals=dict(open_tasks=0, context_switches_per_hour=0, postpone_rate=0.0, stall_minutes=0),
        expected=OverloadLevel.CLEAR,
    ),
    dict(
        label="Light workload — 3 tasks, few switches",
        signals=dict(open_tasks=3, context_switches_per_hour=2, postpone_rate=0.1, stall_minutes=10),
        expected=OverloadLevel.CLEAR,
    ),

    # ─── CAUTION ──────────────────────────────────────────────────────────────
    dict(
        label="Building pressure — 6 tasks, 7 switches",
        signals=dict(open_tasks=6, context_switches_per_hour=7, postpone_rate=0.35, stall_minutes=30),
        expected=OverloadLevel.CAUTION,
    ),
    dict(
        label="Frequent postponements — high defer rate",
        signals=dict(open_tasks=4, context_switches_per_hour=5, postpone_rate=0.6, stall_minutes=25),
        expected=OverloadLevel.CAUTION,
    ),

    # ─── WARNING ──────────────────────────────────────────────────────────────
    dict(
        label="Heavy task load — 10 tasks, 12 switches",
        signals=dict(open_tasks=10, context_switches_per_hour=12, postpone_rate=0.5, stall_minutes=60),
        expected=OverloadLevel.WARNING,
    ),
    dict(
        label="Long stall — 90m no completions",
        signals=dict(open_tasks=8, context_switches_per_hour=10, postpone_rate=0.7, stall_minutes=90),
        expected=OverloadLevel.WARNING,
    ),

    # ─── CRITICAL ─────────────────────────────────────────────────────────────
    dict(
        label="Full overload — 15 tasks, 18 switches, 80% defer",
        signals=dict(open_tasks=15, context_switches_per_hour=18, postpone_rate=0.8, stall_minutes=120),
        expected=OverloadLevel.CRITICAL,
    ),
    dict(
        label="Extreme stall — many open tasks, no progress",
        signals=dict(open_tasks=20, context_switches_per_hour=20, postpone_rate=0.9, stall_minutes=180),
        expected=OverloadLevel.CRITICAL,
    ),
]

print("\n" + "="*60)
print("  NeuroFlow OS — Overload Detection Test Suite")
print("="*60 + "\n")

results = []
for case in cases:
    passed = check(case["label"], case["signals"], case["expected"])
    results.append(passed)

passed_count = sum(results)
print("="*60)
print(f"  Results: {passed_count}/{len(results)} passed")
print("="*60 + "\n")
