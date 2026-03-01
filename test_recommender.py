from recommender import ActionRecommender
from models import TaskInput, TaskFrequency, UserEnergy, RecommendationRequest, TaskTier
from datetime import datetime, timedelta, timezone

def test_recommendation():
    recommender = ActionRecommender()
    
    tasks = [
        TaskInput(
            id="1",
            description="Fix Production Bug",
            deadline=datetime.now(timezone.utc) + timedelta(hours=2),
            frequency=TaskFrequency.ONCE,
            estimated_effort_hours=1.5,
            emotional_weight=10
        ),
        TaskInput(
            id="2",
            description="Write Documentation",
            deadline=datetime.now(timezone.utc) + timedelta(days=3),
            frequency=TaskFrequency.ONCE,
            estimated_effort_hours=4.0,
            emotional_weight=5
        ),
        TaskInput(
            id="3",
            description="Check Emails",
            deadline=None,
            frequency=TaskFrequency.DAILY,
            estimated_effort_hours=0.5,
            emotional_weight=2
        )
    ]

    # Scenario 1: High Energy, Lots of Time
    req1 = RecommendationRequest(
        tasks=tasks,
        current_energy=UserEnergy.HIGH,
        time_available_minutes=120
    )
    res1 = recommender.recommend(req1)
    print(f"Scenario 1 (High/120m): Best Task -> {res1['selected_task']['description']} ({res1['selected_task']['tier']})")

    # Scenario 2: Low Energy, Short Time
    req2 = RecommendationRequest(
        tasks=tasks,
        current_energy=UserEnergy.LOW,
        time_available_minutes=30
    )
    res2 = recommender.recommend(req2)
    print(f"Scenario 2 (Low/30m): Best Task -> {res2['selected_task']['description']} ({res2['selected_task']['tier']})")

    # Scenario 3: Very Short Time (Edge Case)
    req3 = RecommendationRequest(
        tasks=tasks,
        current_energy=UserEnergy.MEDIUM,
        time_available_minutes=5
    )
    res3 = recommender.recommend(req3)
    print(f"Scenario 3 (5m): {res3['system_note']}")

if __name__ == "__main__":
    test_recommendation()
