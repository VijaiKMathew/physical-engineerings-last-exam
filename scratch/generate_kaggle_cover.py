#!/usr/bin/env python3
"""Generate a dedicated Kaggle Writeup Card & Thumbnail cover image."""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

output_dir = Path(__file__).resolve().parent.parent / "docs/images"
media_dir = Path(__file__).resolve().parent.parent / "media"
output_dir.mkdir(parents=True, exist_ok=True)
media_dir.mkdir(parents=True, exist_ok=True)

# Create 16:9 Card with Safe Center Zone (for both Card and Square Thumbnail)
fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
ax.set_facecolor('#0b0f19')
fig.patch.set_facecolor('#0b0f19')
ax.axis('off')

# Gradient-like background glow in the center
center_glow = patches.Rectangle((0.15, 0.12), 0.70, 0.76, 
                                facecolor='#161d2f', edgecolor='#388bfd', 
                                linewidth=2.5, linestyle='-', zorder=1,
                                transform=ax.transAxes, alpha=0.95)
ax.add_patch(center_glow)

# Header Badges (Inside safe center)
ax.text(0.5, 0.79, "GOOGLE CLOUD AI RESEARCH  •  PLE BENCHMARK", 
        color='#58a6ff', fontsize=13, weight='bold', ha='center', transform=ax.transAxes)

# Main Title (Center Safe Area)
ax.text(0.5, 0.70, "AERO-AEGIS", 
        color='#ffffff', fontsize=40, weight='heavy', ha='center', transform=ax.transAxes)

# Subtitle / Paradigm
ax.text(0.5, 0.63, "Autonomous Physical Engineering Agent", 
        color='#7ee787', fontsize=18, weight='bold', ha='center', transform=ax.transAxes)

# Key Metrics Pill Banner (Center Safe Area)
metrics_bg = patches.Rectangle((0.22, 0.49), 0.56, 0.09, 
                               facecolor='#0d1117', edgecolor='#30363d', 
                               linewidth=1.5, zorder=2, transform=ax.transAxes)
ax.add_patch(metrics_bg)

ax.text(0.31, 0.545, "0.608 SOTA", color='#f85149', fontsize=16, weight='bold', ha='center', transform=ax.transAxes)
ax.text(0.31, 0.51, "29 Public Dev Tasks", color='#8b949e', fontsize=10, ha='center', transform=ax.transAxes)

ax.text(0.50, 0.545, "GEMINI 4 ARGON", color='#58a6ff', fontsize=16, weight='bold', ha='center', transform=ax.transAxes)
ax.text(0.50, 0.51, "Sponsored Foundation Model", color='#8b949e', fontsize=10, ha='center', transform=ax.transAxes)

ax.text(0.69, 0.545, "$3.80 / TASK", color='#d29922', fontsize=16, weight='bold', ha='center', transform=ax.transAxes)
ax.text(0.69, 0.51, "Stage 2 Pareto Frontier", color='#8b949e', fontsize=10, ha='center', transform=ax.transAxes)

# Discipline Icons / Pills (Center Safe Area)
disciplines = [
    ("STRUCTURAL", "10 Tasks\nRoof & Shears", "#388bfd"),
    ("CIVIL", "18 Tasks\nSite IFC & Soils", "#3fb950"),
    ("ELECTRICAL", "27 Tasks\nLV Cables & Specs", "#d29922"),
    ("MECHANICAL", "30 Tasks\nClash-Free MEP", "#f85149")
]

x_start = 0.20
col_w = 0.145
for i, (disc, desc, col) in enumerate(disciplines):
    bx = x_start + i * 0.155
    card = patches.Rectangle((bx, 0.22), col_w, 0.22, 
                             facecolor='#0d1117', edgecolor=col, 
                             linewidth=2, zorder=2, transform=ax.transAxes)
    ax.add_patch(card)
    ax.text(bx + col_w/2, 0.38, disc, color=col, fontsize=12, weight='bold', ha='center', transform=ax.transAxes)
    ax.text(bx + col_w/2, 0.28, desc, color='#c9d1d9', fontsize=10, ha='center', va='center', linespacing=1.4, transform=ax.transAxes)

# Bottom Feature Callout
ax.text(0.5, 0.16, "Multi-Modal Vector Perception  •  OpenCASCADE / IfcOpenShell  •  Deterministic Verification Loops", 
        color='#8b949e', fontsize=11, ha='center', transform=ax.transAxes)

# Save Cover
cover_path = output_dir / "figure0_kaggle_cover_card.png"
media_cover = media_dir / "cover_image.png"

plt.tight_layout()
plt.savefig(cover_path, facecolor='#0b0f19', dpi=200)
plt.savefig(media_cover, facecolor='#0b0f19', dpi=200)
plt.close()

print(f"Generated {cover_path}")
print(f"Generated {media_cover}")
