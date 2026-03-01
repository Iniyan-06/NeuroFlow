from typing import List, Optional
from models import TaskInput, TaskTier, UserEnergy, TaskClassificationResponse, RecommendationRequest
from engine import ClassificationEngine

class ActionRecommender:
    @staticmethod
    def get_tier_weight(tier: TaskTier) -> float:
        weights = {
            TaskTier.SURVIVAL_CRITICAL: 100.0,
            TaskTier.LONG_TERM_MEANINGFUL: 70.0,
            TaskTier.ROUTINE_REPETITIVE: 30.0,
            TaskTier.NOISE: 0.0
        }
        return weights.get(tier, 0.0)

    @staticmethod
    def calculate_energy_match(energy: UserEnergy, effort_hours: float) -> float:
        # High Energy (3) -> High Effort (5+ hours)
        # Low Energy (1) -> Low Effort (<1 hour)
        effort_level = 1
        if effort_hours >= 4: effort_level = 3
        elif effort_hours >= 1: effort_level = 2
        
        energy_map = {UserEnergy.LOW: 1, UserEnergy.MEDIUM: 2, UserEnergy.HIGH: 3}
        user_level = energy_map.get(energy, 2)
        
        diff = abs(user_level - effort_level)
        return max(0, 100 - (diff * 40))

    @staticmethod
    def recommend(request: RecommendationRequest) -> dict:
        # Edge Case 1: No tasks
        if not request.tasks:
            return {
                "selected_task": None,
                "alternative_actions": [],
                "system_note": "No tasks in queue. Take a moment to breathe or plan your day."
            }

        # Edge Case 2: Zero Time Available
        if request.time_available_minutes < 10:
            return {
                "selected_task": None,
                "alternative_actions": [],
                "system_note": "Insufficient time for deep work. Recommended: 5-minute stretching or eye-rest."
            }

        scored_tasks = []
        for task in request.tasks:
            classification = ClassificationEngine.classify(task)
            
            # Recommendation Scoring
            tier_score = ActionRecommender.get_tier_weight(classification["tier"])
            energy_score = ActionRecommender.calculate_energy_match(request.current_energy, task.estimated_effort_hours)
            
            # Time Fit: 1.0 if fits, 0.0 if not. Harsh penalty if it doesn't fit.
            time_fit = 100.0 if (task.estimated_effort_hours * 60) <= request.time_available_minutes else 0.0
            
            # Context Switch Cost (simplified: 10 if category changed, 0 if same)
            # In a real system, we'd compare task tags.
            context_cost = 0.0 # Placeholder
            
            rec_score = (tier_score * 0.4) + (energy_score * 0.3) + (time_fit * 0.3) - context_cost
            
            scored_tasks.append({
                "classification": classification,
                "rec_score": rec_score
            })

        # Sort by recommendation score descending
        scored_tasks.sort(key=lambda x: x["rec_score"], reverse=True)
        
        # Edge Case 3: All tasks are "Noise" and time/energy is low
        top_task = scored_tasks[0]
        if top_task["rec_score"] < 30 and top_task["classification"]["tier"] == TaskTier.NOISE:
            return {
                "selected_task": None,
                "alternative_actions": [t["classification"] for t in scored_tasks[:3]],
                "system_note": "Nothing high-impact fits your current state. Use this time for recovery."
            }

        return {
            "selected_task": top_task["classification"],
            "alternative_actions": [t["classification"] for t in scored_tasks[1:4]],
            "system_note": f"Optimal task selected based on {request.current_energy} energy and {request.time_available_minutes}m free."
        }
