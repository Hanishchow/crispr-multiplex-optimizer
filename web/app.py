#!/usr/bin/env python3
"""
CRISPR Multiplexing Optimizer v0.2.0
Optimize simultaneous CRISPR edits with ML predictions + Doench scoring.
"""

import streamlit as st
import pandas as pd
from crispr_mux import CRISPRMultiplexOptimizer, GuideRNA, save_designs


st.set_page_config(
    page_title="CRISPR Multiplex Optimizer v0.2", page_icon="🧬", layout="wide"
)

st.title("🧬 CRISPR Multiplexing Optimizer")
st.markdown("**v0.2.0** — ML-powered with Doench + off-target risk scoring")


# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    delivery = st.selectbox(
        "Delivery Method",
        ["lnp", "aav", "lipofection", "electroporation", "lentivirus"],
        help="Viral vector or lipid nanoparticle delivery",
    )

    cell_type = st.text_input("Cell Type", "HEK293")
    max_sites = st.slider("Max Guides", 4, 50, 20)

    st.divider()

    st.markdown("**Delivery Capacities:**")
    st.caption(
        "• LNP: 50 guides  \n"
        "• Lentivirus: 10 guides  \n"
        "• AAV: 4 guides  \n"
        "• Lipofection: 20 guides  \n"
        "• Electroporation: 30 guides"
    )

    st.divider()

    st.markdown("**Scoring Features:**")
    st.caption(
        "• Doench score (on-target efficiency)  \n"
        "• Off-target risk  \n"
        "• GC content + seed analysis  \n"
        "• PAMproximal bonuses"
    )


# Main input
targets_text = st.text_area(
    "🎯 Target Genes (one per line)",
    placeholder="TP53\nKRAS\nEGFR\nBRCA1\nBRCA2\nMYC",
    height=180,
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

            st.success(f"✓ Generated {len(designs)} designs")

            # Display ranked designs
            for i, (design, score) in enumerate(ranked):
                with st.expander(
                    f"📦 #{i + 1} {design.name} — Score: {score:.2f}", expanded=i == 0
                ):
                    # Metrics
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Guides", len(design.guides))
                    c2.metric("Efficiency", f"{design.efficiency:.0%}")
                    c3.metric("Safety", f"{design.safety_score:.0%}")
                    c4.metric("Valid", "✓" if design.is_valid else "✗")

                    # Detailed table
                    data = []
                    for g in design.guides:
                        data.append(
                            {
                                "Gene": g.target_gene,
                                "Sequence": g.sequence[:20],
                                "Doench": f"{g.doench_score():.2f}",
                                "GC%": f"{g.gc_content:.0%}",
                                "Off-Target Risk": f"{g.off_target_risk():.2f}",
                            }
                        )

                    st.dataframe(pd.DataFrame(data), use_container_width=True)

                    # Download
                    csv = pd.DataFrame(data).to_csv(index=False)
                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        f"{design.name}.csv",
                        "text/csv",
                    )

            # Validation section
            st.divider()
            st.subheader("🔬 Validation")

            validation = optimizer.validate_designs(designs)
            for d in validation["designs"][:2]:
                with st.expander(f"Validate {d['name']}"):
                    for g in d["guide_validations"]:
                        st.caption(
                            f"**{g['gene']}**: {g['off_targets']} off-targets "
                            f"({g['confidence']} confidence)"
                        )


# Info
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Innovation:**
    First tool to combine:
    - Doench scoring (on-target)
    - Off-target risk estimation
    - Multiplex delivery constraints
    - Composite ranking
    """)

with col2:
    st.markdown("""
    **Next Steps:**
    1. Train RL model on published data
    2. Add GUIDE-seq validation
    3. Integrate with Benchling API
    """)

st.markdown("---")
st.caption("Built with gstack workflow | v0.2.0")
