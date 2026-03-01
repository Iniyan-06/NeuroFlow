# NeuroFlow OS: Task Engine Examples

## Example 1: Survival-critical
**Scenario**: Production server is down.
**Input**:
```json
{
  "description": "Critical Bug: Production server returning 500",
  "deadline": "2026-03-01T00:00:00Z", 
  "frequency": "once",
  "estimated_effort_hours": 2,
  "emotional_weight": 9
}
```
**Output**:
```json
{
  "description": "Critical Bug: Production server returning 500",
  "score": 88.5,
  "tier": "Survival-critical",
  "next_action": "Execute immediately. Limit distractions.",
  "reasoning": "U:100 I:100 E:20 Em:90"
}
```

## Example 2: Long-term meaningful
**Scenario**: Writing the architecture design document.
**Input**:
```json
{
  "description": "Draft NeuroFlow Architecture v2",
  "deadline": "2026-03-05T12:00:00Z",
  "frequency": "once",
  "estimated_effort_hours": 5,
  "emotional_weight": 6
}
```
**Output**:
```json
{
  "description": "Draft NeuroFlow Architecture v2",
  "score": 67.2,
  "tier": "Long-term meaningful",
  "next_action": "Schedule peak focus time for this.",
  "reasoning": "U:45 I:100 E:50 Em:60"
}
```

## Example 3: Routine repetitive
**Scenario**: Weekly sync meeting preparation.
**Input**:
```json
{
  "description": "Prepare weekly status report",
  "deadline": "2026-03-02T09:00:00Z",
  "frequency": "weekly",
  "estimated_effort_hours": 1,
  "emotional_weight": 3
}
```
**Output**:
```json
{
  "description": "Prepare weekly status report",
  "score": 48.5,
  "tier": "Routine repetitive",
  "next_action": "Batch this with similar tasks later.",
  "reasoning": "U:75 I:40 E:10 Em:30"
}
```

## Example 4: Noise
**Scenario**: Checking social media for mentions.
**Input**:
```json
{
  "description": "Check Twitter for product mentions",
  "deadline": null,
  "frequency": "daily",
  "estimated_effort_hours": 0.5,
  "emotional_weight": 2
}
```
**Output**:
```json
{
  "description": "Check Twitter for product mentions",
  "score": 12.0,
  "tier": "Noise",
  "next_action": "Delegate, automate, or ignore for now.",
  "reasoning": "U:0 I:20 E:5 Em:20"
}
```
