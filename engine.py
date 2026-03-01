from datetime import datetime, timezone
from models import TaskInput, TaskTier, TaskFrequency
import math

class ClassificationEngine:
    @staticmethod
    def calculate_urgency(deadline: datetime) -> float:
        if not deadline:
            return 0.0
        
        now = datetime.now(timezone.utc)
        time_diff = (deadline - now).total_seconds()
        
        if time_diff <= 0:
            return 100.0
        
        # Scale: 0 to 100 based on a 7-day window
        # < 1 hour: 100
        # > 7 days: 0
        days_remaining = time_diff / 86400
        if days_remaining < 0.04: # < 1 hour
            return 100.0
        
        score = max(0, 100 * (1 - (math.log(days_remaining + 1) / math.log(8))))
        return min(100.0, score)

    @staticmethod
    def calculate_importance(frequency: TaskFrequency) -> float:
        weights = {
            TaskFrequency.ONCE: 100.0,
            TaskFrequency.MONTHLY: 70.0,
            TaskFrequency.WEEKLY: 40.0,
            TaskFrequency.DAILY: 20.0
        }
        return weights.get(frequency, 50.0)

    @staticmethod
    def classify(task: TaskInput) -> dict:
        # 1. Weights
        W_URGENCY = 0.45
        W_IMPORTANCE = 0.25
        W_EFFORT = 0.20
        W_EMOTION = 0.10

        # 2. Score Components
        urgency_score = ClassificationEngine.calculate_urgency(task.deadline)
        importance_score = ClassificationEngine.calculate_importance(task.frequency)
        effort_score = min(100.0, task.estimated_effort_hours * 10) # 10h = 100
        emotion_score = (task.emotional_weight or 5) * 10 # Default to 5

        # 3. Final Score
        final_score = (
            (urgency_score * W_URGENCY) +
            (importance_score * W_IMPORTANCE) +
            (effort_score * W_EFFORT) +
            (emotion_score * W_EMOTION)
        )

        # 4. Tier Logic
        if final_score >= 80:
            tier = TaskTier.SURVIVAL_CRITICAL
            next_action = "Execute immediately. Limit distractions."
        elif final_score >= 60:
            tier = TaskTier.LONG_TERM_MEANINGFUL
            next_action = "Schedule peak focus time for this."
        elif final_score >= 30:
            tier = TaskTier.ROUTINE_REPETITIVE
            next_action = "Batch this with similar tasks later."
        else:
            tier = TaskTier.NOISE
            next_action = "Delegate, automate, or ignore for now."

        return {
            "description": task.description,
            "score": round(final_score, 2),
            "tier": tier,
            "next_action": next_action,
            "reasoning": f"U:{round(urgency_score)} I:{round(importance_score)} E:{round(effort_score)} Em:{round(emotion_score)}"
        }
