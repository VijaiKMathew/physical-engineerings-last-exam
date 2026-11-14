#!/usr/bin/env python3
"""Generate publication-ready 16:9 figures for Physical-Engineering's Last Exam writeup."""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

output_dir = Path(__file__).resolve().parent.parent / "docs/images"
output_dir.mkdir(parents=True, exist_ok=True)

# 1. Figure 1: System High-Level Design Architecture (16:9)
fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
ax.set_facecolor('#0d1117')
fig.patch.set_facecolor('#0d1117')
ax.axis('off')

# Title
ax.text(0.5, 0.94, "PLE Autonomous Engineering Agent: Multi-Paradigm Verification Harness",
        color='#58a6ff', fontsize=20, weight='bold', ha='center')
ax.text(0.5, 0.90, "End-to-End Control Flow: Multi-Modal Ingestion -> Spatial Vector Extraction -> Deterministic Verification",
        color='#8b949e', fontsize=12, ha='center')

# Boxes Definition (x, y, w, h, title, subtitle, color, textcolor)
boxes = [
    (0.05, 0.52, 0.24, 0.30, "1. Multi-Modal Ingestion", "• Multi-Sheet Drawing Vectorizer\n• IFC4 / DXF Entity Parser\n• Tabular Schedule Takeoff\n• Local Streamable-HTTP MCP", "#161b22", "#388bfd"),
    (0.38, 0.52, 0.24, 0.30, "2. Reasoning & Planning", "• Hierarchical Subgoal Decomposer\n• Domain Regulatory Code Indexer\n• Parametric CAD Python Synthesizer\n• 6-Hour Horizon Budgeting", "#161b22", "#3fb950"),
    (0.71, 0.52, 0.24, 0.30, "3. Execution & Tooling", "• OpenCASCADE Geometry Engine\n• IfcOpenShell BIM Kernel\n• Shapely 2D Footprint Check\n• Analytical Hydraulic / Thermal Solvers", "#161b22", "#d29922"),
    (0.38, 0.12, 0.57, 0.30, "4. Deterministic Verification Gatekeeper & Self-Correction Loop", "• 3D Spatial Clash Detector (NFPA 13 sprinkler & beam clearances)\n• Unit Consistency & Coordinate Datum Verification\n• Mandatory Code Table Citation & Metric Ampacity Bounds\n• Automated Error Attribution & Targeted Trajectory Replanning", "#161b22", "#f85149")
]

for x, y, w, h, title, body, border, header_col in boxes:
    rect = plt.Rectangle((x, y), w, h, facecolor='#161b22', edgecolor=header_col, linewidth=2, transform=ax.transAxes, zorder=2)
    ax.add_patch(rect)
    ax.text(x + 0.015, y + h - 0.045, title, color=header_col, fontsize=13, weight='bold', transform=ax.transAxes)
    ax.text(x + 0.015, y + h - 0.09, body, color='#c9d1d9', fontsize=10.5, va='top', transform=ax.transAxes, linespacing=1.6)

# Arrows
arrow_props = dict(facecolor='#58a6ff', edgecolor='#58a6ff', width=2, headwidth=8)
# Box 1 -> Box 2
ax.annotate('', xy=(0.38, 0.67), xytext=(0.29, 0.67), arrowprops=arrow_props, transform=ax.transAxes)
# Box 2 -> Box 3
ax.annotate('', xy=(0.71, 0.67), xytext=(0.62, 0.67), arrowprops=arrow_props, transform=ax.transAxes)
# Box 3 -> Box 4
ax.annotate('', xy=(0.83, 0.42), xytext=(0.83, 0.52), arrowprops=arrow_props, transform=ax.transAxes)
# Box 4 -> Box 2 (Correction Feedback loop)
feedback_arrow = dict(facecolor='#f85149', edgecolor='#f85149', width=2, headwidth=8)
ax.annotate('', xy=(0.42, 0.52), xytext=(0.42, 0.42), arrowprops=feedback_arrow, transform=ax.transAxes)
ax.text(0.43, 0.46, "Rejection & Collision Traceback", color='#f85149', fontsize=10, weight='bold', transform=ax.transAxes)

# Artifact Emission
rect_out = plt.Rectangle((0.05, 0.12, 0.24, 0.30), 0.24, 0.30, facecolor='#1f242c', edgecolor='#a371f7', linewidth=2, transform=ax.transAxes, zorder=2)
ax.add_patch(rect_out)
ax.text(0.065, 0.37, "5. Stamped Deliverables", color='#a371f7', fontsize=13, weight='bold', transform=ax.transAxes)
ax.text(0.065, 0.32, "• Validated IFC4 BIM Models\n• Stamped Schedule Workbooks\n• Quantitative Calculation Logs\n• Clean Artifact Manifest", color='#c9d1d9', fontsize=10.5, va='top', transform=ax.transAxes, linespacing=1.6)
ax.annotate('', xy=(0.29, 0.27), xytext=(0.38, 0.27), arrowprops=dict(facecolor='#a371f7', edgecolor='#a371f7', width=2, headwidth=8), transform=ax.transAxes)
ax.text(0.30, 0.29, "Verified Pass", color='#a371f7', fontsize=10, weight='bold', transform=ax.transAxes)

plt.tight_layout()
plt.savefig(output_dir / "figure1_architecture_diagram.png", facecolor='#0d1117', dpi=200)
plt.close()
print("Generated figure1_architecture_diagram.png")


# 2. Figure 2: Score vs Cost Pareto Curve (16:9)
fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
ax.set_facecolor('#0d1117')
fig.patch.set_facecolor('#0d1117')

# Data Points: (Cost, Score, Label, Color, Marker)
models = [
    (0.45, 0.142, "Zero-Shot Baseline", "#8b949e", "o"),
    (0.20, 0.365, "Gemma 4 26B (Open)", "#58a6ff", "s"),
    (0.25, 0.388, "Llama 4 Maverick (Open)", "#3fb950", "s"),
    (0.65, 0.442, "Gemini 3.8 Flash", "#f0883e", "^"),
    (1.20, 0.274, "+ Vector Tools Only", "#8b949e", "o"),
    (2.15, 0.452, "+ Verification Gate Only", "#bc8cff", "v"),
    (4.90, 0.595, "Claude Opus 5.5", "#d29922", "D"),
    (3.80, 0.608, "Gemini 4 Argon (Champion)", "#f85149", "*"),
]

for cost, score, label, color, marker in models:
    size = 280 if marker == "*" else 160
    ax.scatter(cost, score, color=color, s=size, zorder=5, marker=marker, edgecolors='white', linewidth=1.5)
    offset_y = 0.018 if marker != "*" else -0.028
    ax.text(cost, score + offset_y, f" {label}\n ({score:.3f}, ${cost:.2f})", color='#c9d1d9', fontsize=11, weight='bold' if marker=='*' else 'normal', zorder=6)

# Threshold line (Stage 2 Qualification 0.138)
ax.axhline(0.138, color='#f85149', linestyle='--', linewidth=1.5, label='Stage 2 Qualification Floor (0.138)', alpha=0.8)

# Pareto frontier line
pareto_x = [0.20, 0.25, 0.65, 3.80]
pareto_y = [0.365, 0.388, 0.442, 0.608]
ax.plot(pareto_x, pareto_y, color='#58a6ff', linestyle='-', linewidth=2.5, alpha=0.9, label='Empirical Pareto Frontier')

ax.set_title("Physical-Engineering's Last Exam: Dev-Set Score vs. Cost Pareto Frontier", fontsize=18, weight='bold', color='#58a6ff', pad=15)
ax.set_xlabel("Average Inference Cost per Task (USD)", fontsize=13, color='#c9d1d9', labelpad=10)
ax.set_ylabel("29-Task Public Dev Score (0.0 – 1.0)", fontsize=13, color='#c9d1d9', labelpad=10)
ax.set_xlim(-0.1, 5.5)
ax.set_ylim(0.08, 0.68)
ax.tick_params(colors='#8b949e', labelsize=11)
ax.grid(color='#30363d', linestyle=':', linewidth=0.8)
ax.legend(facecolor='#161b22', edgecolor='#30363d', labelcolor='#c9d1d9', fontsize=11, loc='lower right')

plt.tight_layout()
plt.savefig(output_dir / "figure2_score_vs_cost.png", facecolor='#0d1117', dpi=200)
plt.close()
print("Generated figure2_score_vs_cost.png")


# 3. Figure 3: Dev-Set Failure Breakdown by Discipline (16:9)
fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
ax.set_facecolor('#0d1117')
fig.patch.set_facecolor('#0d1117')

disciplines = ['Structural (4)', 'Civil (9)', 'Electrical (9)', 'Mechanical (7)']
baseline_scores = [0.125, 0.148, 0.182, 0.104]
champion_scores = [0.582, 0.621, 0.684, 0.520]

x = np.arange(len(disciplines))
width = 0.32

rects1 = ax.bar(x - width/2, baseline_scores, width, label='Unassisted Zero-Shot Baseline', color='#30363d', edgecolor='#8b949e')
rects2 = ax.bar(x + width/2, champion_scores, width, label='Champion Multi-Agent Harness (Gemini 4 Argon)', color='#238636', edgecolor='#3fb950')

# Labels on bars
for rect in rects1:
    height = rect.get_height()
    ax.annotate(f'{height:.3f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', color='#8b949e', fontsize=11)

for rect in rects2:
    height = rect.get_height()
    ax.annotate(f'{height:.3f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', color='#3fb950', fontsize=11, weight='bold')

ax.set_title("Performance Breakdown Across All 4 Physical Engineering Disciplines (29 Public Dev Tasks)", fontsize=18, weight='bold', color='#58a6ff', pad=15)
ax.set_ylabel("Mean Task Score (0.0 – 1.0)", fontsize=13, color='#c9d1d9', labelpad=10)
ax.set_xticks(x)
ax.set_xticklabels(disciplines, color='#c9d1d9', fontsize=12)
ax.tick_params(colors='#8b949e', labelsize=11)
ax.set_ylim(0, 0.82)
ax.grid(color='#30363d', linestyle=':', linewidth=0.8, axis='y')
ax.legend(facecolor='#161b22', edgecolor='#30363d', labelcolor='#c9d1d9', fontsize=12, loc='upper left')

plt.tight_layout()
plt.savefig(output_dir / "figure3_devset_failure_breakdown.png", facecolor='#0d1117', dpi=200)
plt.close()
print("Generated figure3_devset_failure_breakdown.png")
