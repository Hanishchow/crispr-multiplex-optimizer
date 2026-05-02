# CRISPR Multiplexing Optimizer

Optimize simultaneous CRISPR edits (10-50 sites) with ML predictions + delivery constraints.

## Install

```bash
pip install crispr-multiplex-optimizer
```

## CLI Usage

```bash
# Single batch
crispr-mux optimize TP53 KRAS EGFR BRCA1 BRCA2 --delivery lnp --max 20

# Batch from CSV
crispr-mux batch targets.csv -o designs.json
```

## Web Interface

```bash
streamlit run web/app.py
```

## Library Usage

```python
from crispr_mux import CRISPRMultiplexOptimizer, GuideRNA

optimizer = CRISPRMultiplexOptimizer()

designs = optimizer.optimize(
    targets=["TP53", "KRAS", "EGFR"],
    delivery_method="lnp",
    cell_type="HEK293",
    max_sites=10,
)

ranked = optimizer.rank_designs(designs)
for design, score in ranked:
    print(f"{design.name}: {score:.2f}")
```

## Features

- [ ] ML efficiency prediction (needs training data)
- [ ] gRNA interaction scoring
- [ ] Delivery capacity constraints
- [ ] Batch optimization with OR-Tools
- [ ] Web UI with Streamlit

## License

MIT