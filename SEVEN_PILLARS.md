# Seven Pillar Architecture — sofie-backend

> API Layer Implementation — S.O.F.I.E. Wellness Engine

## Overview

sofie-backend implements the wellness intelligence layer of the Seven Pillar Architecture, providing evidence-based guidance and long-term health tracking through S.O.F.I.E.'s Intelligence and Eternal operators.

## Pillar Implementation

### Pillar 1: Underground Knowledge
**Location**: `p1-knowledge/`
- Evidence library with JSON knowledge bases
- Protocol matching based on user intent
- PubMed-linked research anchoring

**Key Files**:
- `core_sofie.py` — Central evidence engine
- `library/*.json` — Knowledge modules

### Pillar 2: Mental Models
**Location**: `p2-mental-models/`
- Cognitive bias awareness
- Psychological pattern recognition
- Wellness framework integration

**Key Files**:
- `library/sofie_psychology.json`
- `library/sofie_philosophy.json`

### Pillar 3: Reverse Engineering
**Location**: `p3-reverse-engineering/`
- Protocol decomposition
- Intent-to-evidence matching
- Success factor analysis

**Key Files**:
- `sofie_orchestrator.py` — Main orchestration logic

### Pillar 7: Billionaire Mindset
**Location**: `p7-abundance/`
- Long-term health tracking (somatic ledger)
- Peace-curve prediction
- Ritual auto-triggering

**Key Files**:
- `somatic_ledger.py` — SQLite schema + operations

## Integration Points

### To Layer 1 (Terracare-Ledger)
```python
# Activity logging for token rewards
terracare_client.log_activity(
    user_id=user_id,
    activity_type="wellness_checkin",
    value_points=10
)
```

### To Layer 2 (sofie-systems)
```python
# Operator synchronization
from sofie_systems import Intelligence, Eternal

Intelligence.recognize_pattern(input)
Eternal.remember(memory)
```

### To Layer 3 (All)
- Heartware: Voice interface
- Harmonic-Balance: Dwelling wellness
- tholos-medica: Patient outcomes

## API Conventions

### Endpoint Structure
```
/p{pillar}/{resource}/{action}

Examples:
POST /p1/query              # Query evidence
POST /p7/ledger/entry       # Log somatic data
GET  /p7/ledger/peace-curve # Get predictions
```

## Version

**Implementation**: API Layer v1.0.0
**Last Updated**: 2026-02-05
