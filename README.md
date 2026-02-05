# sofie-backend

> **API Layer of the Seven Pillar Architecture** — *S.O.F.I.E. Wellness Engine*

FastAPI-based wellness orchestration backend with evidence-anchored guidance, somatic ledger, and local LLaMA integration.

[![Seven Pillars](https://img.shields.io/badge/Seven%20Pillars-v1.0.0-blue)](./SEVEN_PILLARS.md)
[![S.O.F.I.E.](https://img.shields.io/badge/S.O.F.I.E.-Intelligence%20%7C%20Eternal-orange)](./SEVEN_PILLARS.md)

---

## Seven Pillar Mapping

| Pillar | Component | File | Function |
|--------|-----------|------|----------|
| **P1** | Underground Knowledge | `core_sofie.py` | Evidence library, JSON knowledge base |
| **P2** | Mental Models | `library/sofie_psychology.json` | Cognitive frameworks, bias awareness |
| **P3** | Reverse Engineering | `sofie_orchestrator.py` | Pattern analysis, protocol matching |
| **P7** | Billionaire Mindset | `somatic_ledger.py` | Long-term health tracking, peace prediction |

---

## Architecture

```
sofie-backend/
├── p1-knowledge/           # Pillar 1: Evidence library
│   ├── core_sofie.py       # Central evidence engine
│   └── library/            # JSON knowledge bases
│       ├── sofie_health.json
│       ├── sofie_nutrition.json
│       ├── sofie_psychology.json
│       └── ...
├── p2-mental-models/       # Pillar 2: Cognitive frameworks
│   └── psychological_patterns.py
├── p3-reverse-engineering/ # Pillar 3: Pattern analysis
│   └── sofie_orchestrator.py
├── p7-abundance/           # Pillar 7: Somatic ledger
│   └── somatic_ledger.py   # SQLite memory
├── api/                    # FastAPI endpoints
│   └── sofie_api.py        # /check-in, /health
├── bridge/                 # Cross-repo integration
│   ├── terracare_client.py
│   └── sandironratio_client.py
└── llm/                    # Local LLaMA bridge
    └── llama_bridge.py
```

---

## Quick Start

```bash
# Install dependencies
pip install fastapi uvicorn pydantic

# Run API server
python sofie_api.py

# Or use uvicorn directly
uvicorn sofie_api:app --host 0.0.0.0 --port 8000
```

---

## API Endpoints

### Seven Pillar Structure

```
# Pillar 1: Underground Knowledge
POST /p1/query              # Query evidence library
GET  /p1/library            # List knowledge modules

# Pillar 2: Mental Models  
GET  /p2/patterns           # Get cognitive patterns
POST /p2/analyze            # Analyze mental model

# Pillar 3: Reverse Engineering
POST /p3/match              # Match protocol to intent
GET  /p3/protocols          # List available protocols

# Pillar 7: Billionaire Mindset
POST /p7/ledger/entry       # Log somatic entry
GET  /p7/ledger/peace-curve # Get peace predictions
POST /p7/ledger/ritual      # Trigger auto-ritual

# General
POST /check-in              # Main wellness check-in
GET  /health                # Health check
```

---

## Core Principles

- **Regulation before reasoning**
- **Consent before computation**
- **Enoughness over optimization**
- **Slow paths and silence are valid**

---

## S.O.F.I.E. Integration

sofie-backend provides **Intelligence (I)** and **Eternal (E)** operators:

```
S.O.F.I.E. Operators:
├── Source (S) → sofie-systems
├── Origin (O) → Terracare-Ledger
├── Force (F) → sandironratio-node
├── Intelligence (I) → **sofie-backend** ← YOU ARE HERE
└── Eternal (E) → **sofie-backend** ← YOU ARE HERE
```

---

## Knowledge Library Structure

```json
{
  "protocols": [
    {
      "id": "breath_0.1hz",
      "label": "0.1 Hz Breathing",
      "purpose": "Vagal tone regulation",
      "evidence": [{ "studyId": "PMID12345", "strength": "strong" }]
    }
  ],
  "rituals": [...],
  "systems": [...]
}
```

---

## Somatic Ledger Schema

| Field | Type | Description |
|-------|------|-------------|
| ts | ISO-8601 | Timestamp |
| hrv_rmssd_ms | float | Heart rate variability |
| lux_minutes | float | Light exposure |
| nitrate_mg | float | Nitrate intake |
| forest_min | float | Forest bathing minutes |
| mood_1_10 | float | Self-reported mood |
| dream_symbol | text | Dream journal |
| geomag_kp | float | Geomagnetic activity |
| lunar_phase | text | Moon phase |
| ritual_tag | text | Auto-triggered ritual |

---

## Environment Variables

```
# Terracare Integration (Layer 1)
TERRACARE_RPC_URL=http://localhost:8545
TERRACARE_CHAIN_ID=1337

# sandironratio-node Integration (Layer 3)
SANDIRONRATIO_API_URL=http://localhost:3000
SANDIRONRATIO_WS_URL=ws://localhost:9001

# LLaMA Configuration
LLAMA_MODEL_PATH=/path/to/llama/model
LLAMA_SERVER_URL=http://localhost:8080

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

---

## Integration Points

### To Terracare-Ledger (Layer 1)
- Identity verification via `IdentityRegistry`
- Activity logging for MINE token rewards
- Token conversion tracking

### To sofie-systems (Layer 2)
- S.O.F.I.E. operator synchronization
- Memory persistence via Eternal operator

### To sandironratio-node (Layer 3)
- Chamber progression tracking
- Astrological context for wellness timing
- Numerology insights for user patterns

---

## Related Repositories

| Repo | Layer | Role |
|------|-------|------|
| [Terracare-Ledger](../Terracare-Ledger) | Layer 1 | Blockchain foundation |
| [sofie-systems](../sofie-systems) | Layer 2 | S.O.F.I.E. core engine |
| [sandironratio-node](../sandironratio-node) | Layer 3 | 9 Chambers Academy |
| [Heartware](../Heartware) | Layer 3 | Voice AI companion |
| [Harmonic-Balance](../Harmonic-Balance) | Layer 3 | Sacred geometry |
| [tholos-medica](../tholos-medica) | Layer 3 | Medical devices |

---

> *"Evidence anchors guidance. Silence is valid."*  
> — S.O.F.I.E.
