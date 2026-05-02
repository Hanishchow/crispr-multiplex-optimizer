#!/usr/bin/env python3
"""Generate PDF from project definition."""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import sys
import os

# Output path
OUTPUT_DIR = "C:/Users/yakka/OneDrive/Desktop/lki"
FILENAME = os.path.join(OUTPUT_DIR, "CRISPR_Multiplex_Optimizer_Project.pdf")

# Create directory if needed
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Build PDF
doc = SimpleDocTemplate(
    FILENAME,
    pagesize=letter,
    rightMargin=72,
    leftMargin=72,
    topMargin=72,
    bottomMargin=72,
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    "Title",
    parent=styles["Title"],
    fontSize=24,
    spaceAfter=30,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#1a365d"),
)
heading_style = ParagraphStyle(
    "Heading",
    parent=styles["Heading1"],
    fontSize=16,
    spaceAfter=12,
    textColor=colors.HexColor("#2c5282"),
    borderPadding=5,
)
subheading_style = ParagraphStyle(
    "Subheading",
    parent=styles["Heading2"],
    fontSize=14,
    spaceAfter=10,
    textColor=colors.HexColor("#2b6cb0"),
)
body_style = ParagraphStyle(
    "Body", parent=styles["BodyText"], fontSize=11, spaceAfter=8, alignment=TA_LEFT
)
code_style = ParagraphStyle(
    "Code",
    parent=styles["Code"],
    fontSize=9,
    spaceAfter=6,
    fontName="Courier",
    textColor=colors.darkblue,
)

# Build content
story = []

# Title
story.append(Paragraph("CRISPR Multiplexing Optimizer", title_style))
story.append(Paragraph("Project Definition Document", styles["Heading3"]))
story.append(Spacer(1, 20))
story.append(
    Paragraph(
        "<b>Version:</b> 1.0 | <b>Date:</b> May 2026 | <b>Status:</b> Active Development",
        body_style,
    )
)
story.append(Spacer(1, 30))

# WHAT Section
story.append(Paragraph("WHAT — Project Overview", heading_style))
story.append(Spacer(1, 10))

story.append(Paragraph("<b>Purpose</b>", subheading_style))
story.append(
    Paragraph(
        "The CRISPR Multiplexing Optimizer is a computational tool that optimizes simultaneous "
        "CRISPR gene edits (10-50 sites) using machine learning predictions and delivery constraints. "
        "It addresses a critical gap in genome editing: no existing tool handles large-scale "
        "multiplexed CRISPR designs with ML-powered efficiency predictions.",
        body_style,
    )
)

story.append(Paragraph("<b>Problem Statement</b>", subheading_style))
problems = [
    "Handle only 1-4 guide RNAs per design",
    "Lack ML-powered efficiency predictions",
    "Don't integrate delivery constraints (LNP, AAV, etc.)",
    "Missing off-target risk estimation",
]
for p in problems:
    story.append(Paragraph(f"• {p}", body_style))

story.append(Paragraph("<b>Solution</b>", subheading_style))
solutions = [
    "ML-powered on-target efficiency scoring (Doench algorithm)",
    "Off-target risk estimation",
    "Multiplex delivery capacity constraints",
    "Composite ranking (efficiency × safety)",
    "Web interface + CLI",
]
for s in solutions:
    story.append(Paragraph(f"✓ {s}", body_style))

story.append(Paragraph("<b>Target Users</b>", subheading_style))
users = [
    "Academic researchers — Gene editing scientists",
    "Biotech companies — Therapeutic development teams",
    "iGEM teams — Synthetic biology competitions",
    "Contract research organizations — Drug discovery",
]
for u in users:
    story.append(Paragraph(f"• {u}", body_style))

story.append(Spacer(1, 20))

# HOW Section
story.append(Paragraph("HOW — Technical Implementation", heading_style))
story.append(Spacer(1, 10))

story.append(Paragraph("<b>Architecture</b>", subheading_style))
story.append(
    Paragraph(
        "Three-layer architecture: User Interface → Core Optimizer → ML Models",
        body_style,
    )
)

story.append(Paragraph("<b>Key Components</b>", subheading_style))

story.append(Paragraph("1. GuideRNA Class", body_style))
code1 = """@dataclass
class GuideRNA:
    sequence: str          # 20nt gRNA sequence
    target_gene: str      # Target gene name
    genomic_position: str # Chromosome:position
    
    # Properties
    gc_content: float      # GC percentage
    doench_score: float   # On-target efficiency (0-1)
    off_target_risk: float # Off-target risk (0-1)"""
story.append(Paragraph(code1.replace("<", "&lt;").replace(">", "&gt;"), code_style))

story.append(Paragraph("<b>Delivery Capacities</b>", subheading_style))
table_data = [
    ["Method", "Max Guides"],
    ["LNP", "50"],
    ["Lentivirus", "10"],
    ["AAV", "4"],
    ["Lipofection", "20"],
    ["Electroporation", "30"],
]
t = Table(table_data, colWidths=[2 * inch, 1.5 * inch])
t.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )
)
story.append(t)

story.append(Spacer(1, 20))

# WHERE Section
story.append(Paragraph("WHERE — Roadmap", heading_style))
story.append(Spacer(1, 10))

story.append(Paragraph("<b>Current State: v0.2.0 (Published)</b>", subheading_style))
story.append(
    Paragraph(
        "✓ Doench scoring • ✓ Off-target risk • ✓ Validation data • ✓ Web UI • ✓ CLI",
        body_style,
    )
)

story.append(Paragraph("<b>Phase 1: Core ML (Weeks 1-2)</b>", subheading_style))
p1 = [
    "• Training data pipeline (GUIDE-seq/CIRCLE-seq from GEO)",
    "• Feature extraction (sequence + chromatin)",
    "• ML model training (PyTorch DQN)",
]
for item in p1:
    story.append(Paragraph(item, body_style))

story.append(Paragraph("<b>Phase 2: Validation (Weeks 3-4)</b>", subheading_style))
p2 = [
    "• Cross-validation (RMSE target: < 0.15)",
    "• Benchmark publication (bioRxiv)",
    "• Peer review",
]
for item in p2:
    story.append(Paragraph(item, body_style))

story.append(Paragraph("<b>Phase 3: Production (Weeks 5-6)</b>", subheading_style))
p3 = [
    "• API deployment",
    "• Benchling integration",
    "• User authentication",
]
for item in p3:
    story.append(Paragraph(item, body_style))

story.append(Paragraph("<b>Phase 4: Monetization (Weeks 7+)</b>", subheading_style))
mone = [
    "• Academic (free) — Free tier",
    "• Biotech (paid) — Fixed rate $99/month",
    "• Enterprise (custom) — Contact sales",
]
for item in mone:
    story.append(Paragraph(item, body_style))

story.append(Spacer(1, 20))

# SUCCESS METRICS
story.append(Paragraph("SUCCESS METRICS", heading_style))
metrics_data = [
    ["Metric", "Target", "Current"],
    ["GitHub Stars", "100+", "New"],
    ["Citations", "10+", "0"],
    ["Accuracy (RMSE)", "< 0.15", "N/A"],
    ["Active Users", "100+", "New"],
    ["Revenue", "$10K ARR", "$0"],
]
m = Table(metrics_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch])
m.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5282")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )
)
story.append(m)

story.append(Spacer(1, 20))

# RESOURCES
story.append(Paragraph("RESOURCES", heading_style))
story.append(
    Paragraph(
        "<b>Repository:</b> <link href='https://github.com/Hanishchow/crispr-multiplex-optimizer'>GitHub</link>",
        body_style,
    )
)
story.append(
    Paragraph(
        "<b>Tech Stack:</b> Python 3.10+, NumPy, Pandas, PyTorch, Streamlit, Click",
        body_style,
    )
)

story.append(Spacer(1, 30))
story.append(Paragraph("<i>Document generated by gstack workflow</i>", body_style))
story.append(Paragraph("<i>Last updated: May 2026</i>", body_style))

# Build PDF
doc.build(story)
print(f"PDF saved to: {FILENAME}")
