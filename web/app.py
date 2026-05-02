#!/usr/bin/env python3
"""
Streamlit Web Interface for CRISPR Multiplexing Optimizer
"""

import streamlit as st
import pandas as pd
from crispr_mux import CRISPRMultiplexOptimizer


st.set_page_config(page_title="CRISPR Multiplex Optimizer", page_icon="🧬")

st.title("🧬 CRISPR Multiplexing Optimizer")
st.markdown(
    "Optimize simultaneous CRISPR edits with ML predictions + delivery constraints"
)


# Input section
with st.sidebar:
    st.header("Configuration")

    delivery = st.selectbox(
        "Delivery Method",
        ["lnp", "aav", "lipofection", "electroporation"],
        help="Viral vector or lipid nanoparticle delivery",
    )

    cell_type = st.text_input("Cell Type", "HEK293")

    max_sites = st.slider("Max Guides", 4, 50, 20)

    st.divider()

    st.markdown("**Delivery Capacities:**")
    st.caption(
        "• LNP: 50 guides  \n• AAV: 4 guides  \n• Lipofection: 20 guides  \n• Electroporation: 30 guides"
    )


# Main input
targets_text = st.text_area(
    "Target Genes (one per line)",
    placeholder="TP53\nKRAS\nEGFR\nBRCA1\nBRCA2",
    height=150,
)


if st.button("🔬 Generate Designs", type="primary"):
    if not targets_text.strip():
        st.error("Please enter at least one target gene")
    else:
        targets = [t.strip() for t in targets_text.split("\n") if t.strip()]

        with st.spinner("Optimizing..."):
            optimizer = CRISPRMultiplexOptimizer()
            designs = optimizer.optimize(
                targets=targets,
                delivery_method=delivery,
                cell_type=cell_type,
                max_sites=max_sites,
            )

            ranked = optimizer.rank_designs(designs)

            st.success(f"Generated {len(designs)} designs")

            for design, score in ranked:
                with st.expander(
                    f"📦 {design.name} — Score: {score:.2f}", expanded=True
                ):
                    # Metrics
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Guides", len(design.guides))
                    c2.metric("Efficiency", f"{design.efficiency:.1%}")
                    c3.metric("Valid", "✓" if design.is_valid else "✗")

                    # Table
                    data = []
                    for g in design.guides:
                        data.append(
                            {
                                "Gene": g.target_gene,
                                "Sequence": g.sequence,
                                "Doench Score": f"{g.on_target_score:.2f}",
                            }
                        )

                    st.dataframe(pd.DataFrame(data), use_container_width=True)

                    # Download
                    import json
                    import pandas as pd

                    csv = pd.DataFrame(data).to_csv(index=False)
                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        f"{design.name}.csv",
                        "text/csv",
                    )


# Info section
st.divider()
st.markdown("""
**Innovation:** No existing tool handles 50+ site multiplexing with ML predictions + delivery constraints.

**Stack:** Python | PyTorch RL (DQN) | OR-Tools  
**Status:** MVP — needs trained RL model for production
""")
