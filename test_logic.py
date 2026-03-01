from engine import ClassificationEngine
from models import TaskInput, TaskFrequency
from datetime import datetime, timedelta, timezone

def test_scoring():
    engine = ClassificationEngine()
    
    # 1. Critical
    task1 = TaskInput(
        description="Emergency Fix",
        deadline=datetime.now(timezone.utc) + timedelta(hours=2),
        frequency=TaskFrequency.ONCE,
        estimated_effort_hours=1,
        emotional_weight=10
    )
    res1 = engine.classify(task1)
    print(f"Test 1 (Critical): {res1['tier']} (Score: {res1['score']})")
    
    # 2. Noise
    task2 = TaskInput(
        description="Check discord",
        deadline=None,
        frequency=TaskFrequency.DAILY,
        estimated_effort_hours=0.2,
        emotional_weight=1
    )
    res2 = engine.classify(task2)
    print(f"Test 2 (Noise): {res2['tier']} (Score: {res2['score']})")

if __name__ == "__main__":
    test_scoring()
