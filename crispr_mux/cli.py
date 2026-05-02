#!/usr/bin/env python3
"""
CRISPR Multiplexing Optimizer CLI v0.2.0
"""

import click
import json
from pathlib import Path
from crispr_mux import CRISPRMultiplexOptimizer, MultiplexDesign, save_designs


@click.group()
@click.version_option(version="0.2.0")
def cli():
    """CRISPR Multiplexing Optimizer — ML-powered CRISPR design."""
    pass


@cli.command()
@click.argument("targets", nargs=-1, required=True)
@click.option("--delivery", default="lnp", help="Delivery method")
@click.option("--cell", default="HEK293", help="Cell type")
@click.option("--max", default=20, help="Max sites per design")
def optimize(targets, delivery, cell, max):
    """Optimize CRISPR multiplexing for TARGETS."""
    optimizer = CRISPRMultiplexOptimizer()
    designs = optimizer.optimize(list(targets), delivery, cell, max)
    ranked = optimizer.rank_designs(designs)

    for i, (design, score) in enumerate(ranked):
        click.echo(f"\n#{i + 1} {design.name} (score: {score:.3f})")
        click.echo(f"   Efficiency: {design.efficiency:.1%}")
        click.echo(f"   Safety: {design.safety_score:.1%}")

        for g in design.guides:
            click.echo(f"   - {g.target_gene}: {g.sequence[:15]}...")
            click.echo(
                f"     Doench: {g.doench_score():.3f} | "
                f"Off-target risk: {g.off_target_risk():.3f}"
            )


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", default="designs.json")
@click.option("--delivery", default="lnp")
def batch(input_file, output, delivery):
    """Batch optimize from CSV."""
    import pandas as pd

    df = pd.read_csv(input_file)
    targets = df["gene"].tolist()

    optimizer = CRISPRMultiplexOptimizer()
    designs = optimizer.optimize(targets, delivery)

    save_designs(designs, output)
    click.echo(f"✓ Saved {len(designs)} designs to {output}")


@cli.command()
@click.argument("targets", nargs=-1, required=True)
def validate(targets):
    """Validate guides against known off-targets."""
    optimizer = CRISPRMultiplexOptimizer()
    guides = []
    for t in targets:
        from crispr_mux import GuideRNA

        guides.append(
            GuideRNA(
                sequence="ACGU" * 5, target_gene=t, genomic_position=f"chr1:{hash(t)}"
            )
        )

    results = optimizer.validate_designs(
        optimizer.optimize(list(targets), "lnp", "HEK293", max_sites=len(targets))
    )

    click.echo("\n🔬 Validation Results:")
    for d in results["designs"]:
        click.echo(f"\n{d['name']}:")
        for g in d["guide_validations"]:
            click.echo(
                f"  {g['gene']}: {g['off_targets']} off-targets "
                f"({g['confidence']} confidence)"
            )


@cli.command()
def serve():
    """Launch web interface."""
    import streamlit
    import sys

    sys.argv = ["streamlit", "run", "web/app.py"]
    streamlit.cli.main()


@cli.command()
def benchmark():
    """Run benchmark on test guides."""
    from crispr_mux import GuideRNA

    test_genes = [
        "TP53",
        "KRAS",
        "EGFR",
        "BRCA1",
        "BRCA2",
        "MYC",
        "PTEN",
        "RB1",
        "APC",
        "CDKN2A",
    ]

    optimizer = CRISPRMultiplexOptimizer()
    guides = []
    for gene in test_genes:
        g = GuideRNA(
            sequence="ACGU" * 5, target_gene=gene, genomic_position=f"chr1:{hash(gene)}"
        )
        guides.append(g)

    designs = optimizer.optimize(test_genes, "lnp", max_sites=10)
    results = optimizer.benchmark(guides)

    click.echo(f"\n📊 Benchmark Results:")
    click.echo(f"  RMSE: {results['rmse']:.3f}")
    click.echo(f"  Correlation: {results['correlation']:.3f}")
    click.echo(f"  Guides tested: {results['n_guides']}")


if __name__ == "__main__":
    cli()
