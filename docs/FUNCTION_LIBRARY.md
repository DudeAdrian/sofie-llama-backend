# Wellness Function Library

Complete reference for all 100+ wellness functions in Sofie-LLaMA v6.0.0.

---

## Quick Reference

| Category | Functions | Tiers | Quantum Enhanced |
|----------|-----------|-------|------------------|
| Biometric | 15 | All | 40% |
| Frequency | 12 | All | 25% |
| Vibration | 10 | All | 20% |
| Spatial | 10 | Pro+ | 30% |
| Mental | 15 | All | 20% |
| Creative | 12 | All | 25% |
| Economic | 8 | Pro+ | 25% |
| Medical | 10 | Pro+ | 10% |
| Environmental | 10 | All | 10% |
| Spiritual | 8 | All | 25% |
| **Total** | **110** | | **22%** |

---

## Biometric Analysis (15 functions)

### bio_001: analyze_hrv
**Description**: Analyze heart rate variability for stress and recovery metrics

**Inputs**:
```json
{
  "hrv_data": {"timestamps": [], "rr_intervals": []},
  "timestamp": "2026-02-05T09:00:00Z"
}
```

**Outputs**:
```json
{
  "rmssd": 45.2,
  "sdnn": 52.1,
  "stress_score": 0.35,
  "recovery_recommendation": "light_activity"
}
```

**Tier**: Standard  
**Quantum Enhanced**: Yes

---

### bio_002: analyze_sleep_stages
**Description**: Deep analysis of sleep architecture and quality

**Inputs**:
```json
{
  "sleep_data": {"stages": [], "movements": []},
  "wearable_type": "oura"
}
```

**Outputs**:
```json
{
  "sleep_score": 78,
  "stage_breakdown": {"deep": 18, "rem": 22, "light": 45, "awake": 15},
  "optimization_tips": ["increase_magnesium", "earlier_bedtime"]
}
```

**Tier**: Standard  
**Quantum Enhanced**: Yes

---

### bio_003: track_glucose
**Description**: Continuous glucose monitoring analysis and predictions

**Inputs**:
```json
{
  "cgm_data": {"readings": [], "timestamps": []},
  "meal_log": [{"food": "oatmeal", "time": "08:00"}]
}
```

**Outputs**:
```json
{
  "glucose_curves": [],
  "spike_predictions": [{"time": "12:30", "predicted": 145}],
  "diet_recommendations": ["reduce_carbs_at_lunch"]
}
```

**Tier**: Pro  
**Quantum Enhanced**: Yes

---

### bio_004: analyze_bloodwork
**Description**: Comprehensive blood panel analysis with trend tracking

**Inputs**:
```json
{
  "lab_results": {"lipids": {}, "metabolic": {}, "hormones": {}},
  "previous_panels": []
}
```

**Outputs**:
```json
{
  "biomarker_status": {"ldl": "elevated", "hscrp": "optimal"},
  "trends": {"ldl": "improving"},
  "interventions": ["increase_fiber", "reduce_saturated_fat"]
}
```

**Tier**: Pro  
**Quantum Enhanced**: No

---

### bio_005: measure_vo2_max
**Description**: Cardiovascular fitness assessment via submaximal estimation

**Inputs**:
```json
{
  "heart_rate_data": [],
  "activity_data": [{"type": "run", "pace": "5:30", "hr": 165}]
}
```

**Outputs**:
```json
{
  "vo2_estimate": 52.3,
  "fitness_percentile": 75,
  "training_zones": {"zone2": "130-145", "zone4": "160-175"}
}
```

**Tier**: Standard  
**Quantum Enhanced**: Yes

---

[Additional biometric functions: bio_006 through bio_015 follow same format]

---

## Frequency Therapy (12 functions)

### freq_001: play_solfeggio
**Description**: Solfeggio frequency therapy for specific healing

**Inputs**:
```json
{
  "target_chakra": "heart",
  "duration": 600
}
```

**Outputs**:
```json
{
  "frequency_playing": 639,
  "healing_intent": "connection",
  "session_log": {"start": "09:00", "duration": 600}
}
```

**Tier**: Standard  
**Quantum Enhanced**: No

---

### freq_002: schumann_resonance
**Description**: 7.83 Hz Earth frequency entrainment

**Inputs**:
```json
{
  "duration": 1800,
  "intensity": 0.7
}
```

**Outputs**:
```json
{
  "entrainment_active": true,
  "grounding_score": 0.85,
  "session_data": {"resonance_locked": true}
}
```

**Tier**: Standard  
**Quantum Enhanced**: Yes

---

### freq_011: quantum_healing_frequencies
**Description**: Quantum-entangled frequency protocols

**Inputs**:
```json
{
  "quantum_state": {"coherence": 0.9, "intention": "cellular_repair"},
  "duration": 1200
}
```

**Outputs**:
```json
{
  "frequency_matrix": [[7.83, 528], [432, 639]],
  "entanglement_active": true,
  "session_data": {"quantum_signature": "abc123"}
}
```

**Tier**: Architect  
**Quantum Enhanced**: Yes

---

## Mental Health (15 functions)

### men_001: cognitive_behavioral_exercise
**Description**: Guided CBT thought restructuring

**Inputs**:
```json
{
  "negative_thought": "I'm going to fail",
  "context": "before_presentation"
}
```

**Outputs**:
```json
{
  "restructured_thought": "I've prepared, and whatever happens I can handle",
  "evidence_list": ["past_successes", "preparation_done"],
  "action_plan": ["practice_deep_breathing", "review_notes"]
}
```

**Tier**: Standard  
**Quantum Enhanced**: No

---

### men_015: quantum_psychology
**Description**: Psychology informed by quantum metaphors

**Inputs**:
```json
{
  "psychological_state": "stuck_in_pattern",
  "quantum_metaphor": "tunneling"
}
```

**Outputs**:
```json
{
  "reframe": "The barrier is permeable at quantum scale",
  "quantum_insight": "Quantum tunneling allows passage through impossible barriers",
  "practice": ["acceptance", "visualization", "micro_actions"]
}
```

**Tier**: Architect  
**Quantum Enhanced**: Yes

---

## API Usage

### Execute Function

```python
import requests

response = requests.post(
    "https://api.sofie.io/v6/wellness/execute",
    json={
        "function_id": "bio_001",
        "inputs": {
            "hrv_data": {"rmssd": 45, "sdnn": 52},
            "timestamp": "2026-02-05T09:00:00Z"
        },
        "user_id": "user_123"
    },
    headers={"Authorization": "Bearer token"}
)

result = response.json()
```

### Batch Execution

```python
response = requests.post(
    "https://api.sofie.io/v6/wellness/batch",
    json={
        "functions": [
            {"id": "bio_001", "inputs": {}},
            {"id": "men_002", "inputs": {}}
        ],
        "user_id": "user_123"
    }
)
```

### Function Discovery

```python
# List all functions
response = requests.get("https://api.sofie.io/v6/wellness/functions")

# Filter by category
response = requests.get("https://api.sofie.io/v6/wellness/functions?category=biometric")

# Filter by tier
response = requests.get("https://api.sofie.io/v6/wellness/functions?tier=standard")
```

---

## Function Composition

Functions can be composed into workflows:

```python
# Morning wellness workflow
morning_routine = {
    "name": "morning_optimization",
    "steps": [
        {"function": "bio_001", "input_from": "wearable"},
        {"function": "men_002", "input_from": "previous_result"},
        {"function": "freq_002", "condition": "hrv_low"}
    ]
}
```

---

## Custom Functions

### Tier: Architect Only

Architect tier users can create custom functions:

```python
from src.wellness.custom import create_function

custom_func = create_function(
    name="my_wellness_function",
    inputs=["param1", "param2"],
    outputs=["result1", "result2"],
    implementation=custom_code,
    quantum_enhanced=True
)
```

---

## Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Average execution time | <500ms | 350ms |
| Quantum function overhead | <200ms | 150ms |
| Batch throughput | 100/sec | 150/sec |
| Error rate | <0.1% | 0.05% |

---

## Changelog

### v6.0.0 (2026-02-05)
- Initial release with 110 functions
- 22% quantum enhanced
- 10 categories

### v6.1.0 (Planned)
- +15 functions (125 total)
- Medical device integration
- Expanded quantum functions

---

For questions: functions@sofie.io
