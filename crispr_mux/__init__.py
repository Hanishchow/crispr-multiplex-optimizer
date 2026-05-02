#!/usr/bin/env python3
"""
CRISPR Multiplexing Optimizer
Optimize simultaneous CRISPR edits (10-50 sites) with ML predictions + delivery constraints.
"""

__version__ = "0.1.0"
__author__ = "AI Engineer"

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import json


@dataclass
class GuideRNA:
    """Single gRNA target."""
    sequence: str
    target_gene: str
    genomic位置: str
    pam: str = "NGG"
    
    def __post_init__(self):
        self.sequence = self.sequence.upper().replace("T", "U")
        
    @property
    def gc_content(self) -> float:
        """Calculate GC content."""
        gc = self.sequence.count('G') + self.sequence.count('C')
        return gc / len(self.sequence)
    
    @property
    def on_target_score(self) -> float:
        """Doench score approximation."""
        # Simplified Doench score (0-1)
        gc = self.gc_content
        position_weight = np.sin(np.pi * (20 - min(20, max(0, 14))) / 2  # Position 14-17 preferred
        return 0.5 + 0.3 * gc + 0.2 * position_weight


@dataclass  
class MultiplexDesign:
    """A complete multiplex design."""
    name: str
    guides: List[GuideRNA]
    delivery_method: str  # lnp, aav, lipofection
    cell_type: str
    
    def __post_init__(self):
        self.capacity = self._get_capacity()
        
    def _get_capacity(self) -> int:
        """Get max guides for delivery method."""
        capacities = {
            "lnp": 50,      # Lipid nanoparticles
            "aav": 4,        # AAV packaging limit
            "lipofection": 20,
            "electroporation": 30,
        }
        return capacities.get(self.delivery_method, 10)
    
    @property
    def is_valid(self) -> bool:
        """Check if design fits delivery."""
        return len(self.guides) <= self.capacity
    
    @property
    def efficiency(self) -> float:
        """Predicted multiplex efficiency."""
        if not self.guides:
            return 0.0
        scores = [g.on_target_score for g in self.guides]
        # Interaction penalty for more guides
        penalty = 0.05 * (len(self.guides) / self.capacity)
        return np.mean(scores) - penalty


class CRISPRMultiplexOptimizer:
    """Optimize CRISPR multiplexing with RL + combinatorial constraints."""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.device = "cpu"  # cuda check
        self.trained = False
        
    def predict_efficiency(self, guides: List[GuideRNA]) -> np.ndarray:
        """Predict editing efficiency for all guides."""
        if not guides:
            return np.array([])
            
        features = self._extract_features(guides)
        
        if self.model and self.trained:
            return self.model.predict(features)
        
        # Fallback: use rule-based scoring
        return np.array([g.on_target_score for g in guides])
    
    def _extract_features(self, guides: List[GuideRNA]) -> np.ndarray:
        """Extract ML features from guides."""
        features = []
        for g in guides:
            feat = [
                g.gc_content,
                len(g.sequence),
                1 if "GG" in g.sequence else 0,  # GG in seed
                sum(ord(c) for c in g.sequence) / (len(g.sequence) * 3),
            ]
            features.append(feat)
        return np.array(features)
    
    def optimize(
        self,
        targets: List[str],
        delivery_method: str = "lnp",
        cell_type: str = "HEK293",
        max_sites: int = 20,
    ) -> List[MultiplexDesign]:
        """Generate optimized multiplex designs."""
        
        # Generate guides from targets
        guides = []
        for target in targets:
            g = GuideRNA(
                sequence=self._generate_mock_guide(target),
                target_gene=target,
                genomic位置=f"chr1:{1000000+len(guides)*1000}",
            )
            guides.append(g)
        
        # Sort by efficiency
        guides.sort(key=lambda g: g.on_target_score, reverse=True)
        
        # Split into batches within capacity
        designs = []
        for i in range(0, len(guides), max_sites):
            batch = guides[i:i+max_sites]
            design = MultiplexDesign(
                name=f"batch_{i//max_sites + 1}",
                guides=batch,
                delivery_method=delivery_method,
                cell_type=cell_type,
            )
            if design.is_valid:
                designs.append(design)
        
        return designs
    
    def _generate_mock_guide(self, target: str) -> str:
        """Generate mock gRNA sequence (placeholder)."""
        np.random.seed(hash(target) % 2**32)
        bases = "ACUG"
        return "".join(np.random.choice(list(bases), size=20))
    
    def rank_designs(
        self, designs: List[MultiplexDesign]
    ) -> List[Tuple[MultiplexDesign, float]]:
        """Rank designs by composite score."""
        results = []
        for design in designs:
            # Composite: efficiency + safety - off_target_risk
            eff = design.efficiency
            safety = 0.9  # Placeholder for actual safety score
            score = eff * 0.6 + safety * 0.4
            results.append((design, score))
        
        return sorted(results, key=lambda x: x[1], reverse=True)
    
    def cross_interaction_score(
        self, guide1: GuideRNA, guide2: GuideRNA
    ) -> float:
        """Estimate gRNA-gRNA interaction (crosstalk/competition)."""
        # Homology penalty
        homology = sum(
            a == b for a, b in zip(guide1.sequence, guide2.sequence)
        ) / len(guide1.sequence)
        
        # Position proximity penalty (same locus = competition)
        same_locus = guide1.genomic位置 == guide2.genomic位置
        pos_penalty = 0.3 if same_locus else 0.0
        
        return max(0, 1.0 - homology - pos_penalty)


def load_guides_from_csv(path: str) -> List[GuideRNA]:
    """Load guides from CSV."""
    df = pd.read_csv(path)
    return [
        GuideRNA(
            sequence=row['sequence'],
            target_gene=row['gene'],
            genomic位置=row['position'],
        )
        for _, row in df.iterrows()
    ]


def save_designs(designs: List[MultiplexDesign], path: str):
    """Save designs to JSON."""
    data = []
    for d in designs:
        data.append({
            "name": d.name,
            "guides": [
                {
                    "sequence": g.sequence,
                    "gene": g.target_gene,
                    "position": g.genomic位置,
                    "score": g.on_target_score,
                }
                for g in d.guides
            ],
            "delivery": d.delivery_method,
            "cell_type": d.cell_type,
            "efficiency": d.efficiency,
            "valid": d.is_valid,
        })
    
    with open(path, "w') as f:
        json.dump(data, f, indent=2)


def demo():
    """Demo run."""
    # Example targets (gene names)
    targets = [
        "TP53", "KRAS", "EGFR", "BRCA1", "BRCA2",
        "MYC", "PTEN", "RB1", "APC", "CDKN2A",
    ]
    
    optimizer = CRISPRMultiplexOptimizer()
    
    print("🧬 CRISPR Multiplexing Optimizer")
    print("=" * 40)
    
    # Generate designs
    designs = optimizer.optimize(
        targets=targets,
        delivery_method="lnp",
        cell_type="HEK293",
        max_sites=10,
    )
    
    print(f"\n📊 Generated {len(designs)} designs")
    
    # Rank and display
    ranked = optimizer.rank_designs(designs)
    for design, score in ranked:
        print(f"\n🔬 {design.name}")
        print(f"   Guides: {len(design.guides)}")
        print(f"   Efficiency: {design.efficiency:.2%}")  
        print(f"   Composite Score: {score:.2f}")
        
        for g in design.guides[:3]:
            print(f"   - {g.target_gene}: {g.sequence[:8]}...")
    
    return designs


if __name__ == "__main__":
    demo()