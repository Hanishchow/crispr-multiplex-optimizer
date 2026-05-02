#!/usr/bin/env python3
"""
CRISPR Multiplexing Optimizer CLI
"""

import click
import json
from pathlib import Path
from crispr_mux import CRISPRMultiplexOptimizer, MultiplexDesign


@click.group()
@click.versionoption(version="0.1.0")
def cli():
    """CRISPR Multiplexing Optimizer — Optimize simultaneous CRISPR edits."""
    pass


@cli.command()
@click.argument("targets", nargs=-1, required=True)
@click.option(
    "--delivery", default="lnp", help="Delivery method (lnp, aav, lipofection)"
)
@click.option("--cell", default="HEK293", help="Cell type")
@click.option("--max", default=20, help="Max sites per design")
def optimize(targets, delivery, cell, max):
    """Optimize CRISPR multiplexing for TARGETS (gene names)."""
    optimizer = CRISPRMultiplexOptimizer()
    designs = optimizer.optimize(targets, delivery, cell, max)

    ranked = optimizer.rank_designs(designs)

    for design, score in ranked:
        click.echo(f"\n{design.name} (score: {score:.2f}):")
        for g in design.guides:
            click.echo(f"  {g.target_gene}: {g.sequence[:20]}")


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", default="designs.json")
def batch(input_file, output):
    """Batch optimize from CSV file."""
    import pandas as pd

    df = pd.read_csv(input_file)
    targets = df["gene"].tolist()

    optimizer = CRISPRMultiplexOptimizer()
    designs = optimizer.optimize(targets)

    from crispr_mux import save_designs

    save_designs(designs, output)
    click.echo(f"Saved {len(designs)} designs to {output}")


@cli.command()
def serve():
    """Launch web interface."""
    click.echo("Web UI coming soon...")
    click.echo("Run: streamlit run web/app.py")


if __name__ == "__main__":
    cli()
