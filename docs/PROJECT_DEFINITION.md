# CRISPR Multiplexing Optimizer
## Project Definition Document

**Version:** 1.0  
**Date:** May 2026  
**Status:** Active Development  

---

# WHAT — Project Overview

## Purpose

The CRISPR Multiplexing Optimizer is a computational tool that optimizes simultaneous CRISPR gene edits (10-50 sites) using machine learning predictions and delivery constraints. It addresses a critical gap in genome editing: no existing tool handles large-scale multiplexed CRISPR designs with ML-powered efficiency predictions and safety scoring.

## Problem Statement

Current CRISPR design tools:
- Handle only 1-4 guide RNAs per design
- Lack ML-powered efficiency predictions
- Don't integrate delivery constraints (LNP, AAV, etc.)
- Missing off-target risk estimation

## Solution

Our tool provides:
- ML-powered on-target efficiency scoring (Doench algorithm)
- Off-target risk estimation
- Multiplex delivery capacity constraints
- Composite ranking (efficiency × safety)
- Web interface + CLI

## Target Users

1. **Academic researchers** — Gene editing scientists
2. **Biotech companies** — Therapeutic development teams
3. **iGEM teams** — Synthetic biology competitions
4. **Contract research organizations** — Drug discovery

---

# HOW — Technical Implementation

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                       │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Streamlit │  │     CLI     │  │   Library API │  │
│  │  Web UI     │  │  Click     │  │   Python      │  │
│  └──────┬──────┘  └──────┬─────┘  └───────┬───────┘  │
└─────────┼─────────────────┼─────────────────┼──────────┘
          │                 │                 │
          ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────┐
│                   CORE OPTIMIZER                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │           CRISPRMultiplexOptimizer                │   │
│  │  - optimize()  - rank_designs()  - validate()   │   │
│  └───────────────────────┬─────────────────────────┘   │
│                          │                             │
│         ┌───────────────┼───────────────┐             │
│         ▼               ▼               ▼              │
│  ┌────────────┐  ┌──────────┐  ┌───────────┐       │
│  │   Guide    │  │ Multiplex │  │Validation │       │
│  │   RNA      │  │  Design   │  │   Data    │       │
│  │  Scoring  │  │  Batching │  │  (GUIDE)  │       │
│  └───────────┘  └──────────┘  └───────────┘       │
└─────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│                    ML MODELS                            │
│  ┌────────────────────┐  ┌───────────────────────┐   │
│  │   Doench Scoring   │  │   Off-Target Risk      │   │
│  │  (Rule-based)      │  │   (CHOPCHOP-style)     │   │
│  └────────────────────┘  └───────────────────────┘   │
│                                                          │
│  ┌────────────────────┐  ┌───────────────────────┐   │
│  │   RL Optimizer     │  │   Future: Deep        │   │
│  │   (Placeholder)    │  │   Learning Model      │   │
│  └────────────────────┘  └───────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Key Components

### 1. GuideRNA Class
```python
@dataclass
class GuideRNA:
    sequence: str          # 20nt gRNA sequence
    target_gene: str      # Target gene name
    genomic_position: str # Chromosome:position
    
    # Properties
    gc_content: float      # GC percentage
    doench_score: float   # On-target efficiency (0-1)
    off_target_risk: float # Off-target risk (0-1)
```

### 2. MultiplexDesign Class
```python
@dataclass
class MultiplexDesign:
    name: str                    # Design identifier
    guides: List[GuideRNA]       # List of gRNAs
    delivery_method: str        # lnp, aav, lipofection
    cell_type: str              # HEK293, K562, etc.
    
    # Scoring
    efficiency: float             # Average Doench score
    safety_score: float        # 1 - off_target_risk
    composite_score: float      # efficiency × safety
```

### 3. Scoring Algorithms

**Doench Score (On-Target):**
- GC content (optimal ~50%)
- Position-weighted bases
- PAMproximal bonuses
- Negative features (poly-T, GC clusters)

**CHOPCHOP Score (Off-Target):**
- GC content
- Seed region analysis
- Homology to genome

## Delivery Capacities

| Method | Max Guides |
|--------|-----------|
| LNP | 50 |
| Lentivirus | 10 |
| AAV | 4 |
| Lipofection | 20 |
| Electroporation | 30 |

---

# WHERE — Roadmap

## Current State

✅ **v0.2.0 (Published)**
- Doench scoring
- Off-target risk
- Validation data
- Streamlit web UI
- CLI interface

## Phase 1: Core ML (Weeks 1-2)

| Milestone | Status | Owner |
|-----------|--------|-------|
| Training data pipeline | 🔲 Pending | - |
| Feature extraction | 🔲 Pending | - |
| ML model training | 🔲 Pending | - |

**Deliverable:** PyTorch DQN model for efficiency prediction

## Phase 2: Validation (Weeks 3-4)

| Milestone | Status | Owner |
|-----------|--------|-------|
| Cross-validation | 🔲 Pending | - |
| Benchmark publication | 🔲 Pending | - |
| Accuracy target: RMSE < 0.15 | 🔲 Pending | - |

**Deliverable:** Peer-reviewed preprint on bioRxiv

## Phase 3: Production (Weeks 5-6)

| Milestone | Status | Owner |
|-----------|--------|-------|
| API deployment | 🔲 Pending | - |
| Benchling integration | 🔲 Pending | - |
| User authentication | 🔲 Pending | - |

**Deliverable:** Production web tool at crispr-mux.example.com

## Phase 4: Monetization (Weeks 7+)

| Revenue Stream | Model |
|---------------|-------|
| Academic (free) | Free tier |
| Biotech (paid) | $99/month |
| Enterprise (custom) | Contact sales |

---

# SUCCESS METRICS

| Metric | Target | Current |
|--------|--------|---------|
| GitHub Stars | 100+ | 🆕 |
| Citations | 10+ | 0 |
| Accuracy (RMSE) | < 0.15 | N/A |
| Active Users | 100+ | 🆕 |
| Revenue | $10K ARR | $0 |

---

# COMPETITION

| Tool | Multiplexing | ML Scoring | Web UI | Open Source |
|------|---------------|-----------|--------|-------------|
| CHOPCHOP | ❌ | ❌ | ✅ | ✅ |
| CRISPOR | ❌ | ❌ | ✅ | ✅ |
| **Our Tool** | ✅ (50+) | ✅ | ✅ | ✅ |

---

# TEAM

| Role | Name | Status |
|------|------|--------|
| Lead Developer | AI Engineer | Active |
| Biology Advisor | TBD | Needed |
| Business Lead | TBD | Needed |

---

# RESOURCES

**Repository:** https://github.com/Hanishchow/crispr-multiplex-optimizer

**Tech Stack:**
- Python 3.10+
- NumPy, Pandas
- PyTorch (future)
- Streamlit
- Click

---

*Document generated by gstack workflow*
*Last updated: May 2026*