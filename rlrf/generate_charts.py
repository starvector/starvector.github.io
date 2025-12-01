#!/usr/bin/env python3
"""Generate high-resolution bar charts for RLRF performance comparison."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Set up high-quality figure parameters for SVG output
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 12
plt.rcParams['svg.fonttype'] = 'none'  # Keep text as text in SVG (not paths)

# Data
models = ['GPT-4o', 'LIVE', 'VTracer', 'StarVector-1B', 'Qwen-3B+SFT', 'Qwen-7B+SFT', 'RLRF (7B)']

# Metrics data
mse_data = [16.92, 2.22, 4.25, 4.60, 9.48, 8.60, 1.03]
ssim_data = [66.91, 88.11, 87.94, 87.00, 78.40, 79.40, 95.10]
dino_data = [89.00, 93.45, 95.75, 96.00, 92.60, 93.00, 98.70]
lpips_data = [27.55, 7.23, 11.66, 9.22, 17.44, 16.58, 3.08]
code_eff_data = [1300, -18300, -12900, -800, -2500, -2800, -334]

# Colors
baseline_color = '#2196F3'  # Blue
rlrf_color = '#F68946'  # Orange
baseline_edge = '#1976D2'
rlrf_edge = '#E65100'

def create_bar_colors(n_models):
    colors = [baseline_color] * (n_models - 1) + [rlrf_color]
    edges = [baseline_edge] * (n_models - 1) + [rlrf_edge]
    return colors, edges

def create_chart(ax, data, title, subtitle, y_min=None, y_formatter=None):
    colors, edges = create_bar_colors(len(models))
    
    x = np.arange(len(models))
    bars = ax.bar(x, data, color=colors, edgecolor=edges, linewidth=2)
    
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=45, ha='right', fontsize=10)
    ax.set_title(f'{title}', fontsize=14, fontweight='bold', pad=10)
    ax.text(0.5, 1.02, subtitle, transform=ax.transAxes, ha='center', va='bottom', 
            fontsize=10, color='#666666')
    
    if y_min is not None:
        ax.set_ylim(bottom=y_min)
    
    if y_formatter:
        ax.yaxis.set_major_formatter(plt.FuncFormatter(y_formatter))
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bar, val in zip(bars, data):
        height = bar.get_height()
        label = y_formatter(val, None) if y_formatter else f'{val:.2f}'
        if isinstance(val, int) or (isinstance(val, float) and val == int(val)):
            label = y_formatter(val, None) if y_formatter else f'{int(val)}'
        ax.annotate(label,
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, fontweight='bold')

# Create figure with 5 subplots (2 rows: 3 + 2)
fig = plt.figure(figsize=(20, 12))

# Row 1: MSE, SSIM, DINO
ax1 = fig.add_subplot(2, 3, 1)
create_chart(ax1, mse_data, 'MSE ↓', '(lower is better)')

ax2 = fig.add_subplot(2, 3, 2)
create_chart(ax2, ssim_data, 'SSIM ↑', '(higher is better)', y_min=60)

ax3 = fig.add_subplot(2, 3, 3)
create_chart(ax3, dino_data, 'DINO ↑', '(higher is better)', y_min=85)

# Row 2: LPIPS, Code Efficiency (centered)
ax4 = fig.add_subplot(2, 3, 4)
create_chart(ax4, lpips_data, 'LPIPS ↓', '(lower is better)')

ax5 = fig.add_subplot(2, 3, 5)
def code_eff_formatter(val, pos):
    if val >= 0:
        return f'+{val/1000:.1f}k'
    return f'{val/1000:.1f}k'
create_chart(ax5, code_eff_data, 'Code Efficiency', '(tokens vs ground truth)', y_formatter=code_eff_formatter)

# Hide the 6th subplot
ax6 = fig.add_subplot(2, 3, 6)
ax6.axis('off')

# Add legend
baseline_patch = mpatches.Patch(color=baseline_color, edgecolor=baseline_edge, linewidth=2, label='Baselines')
rlrf_patch = mpatches.Patch(color=rlrf_color, edgecolor=rlrf_edge, linewidth=2, label='RLRF (Ours)')
fig.legend(handles=[baseline_patch, rlrf_patch], loc='lower right', bbox_to_anchor=(0.85, 0.15),
           fontsize=12, frameon=True, fancybox=True, shadow=True)

# Add main title
fig.suptitle('RLRF Performance Comparison', fontsize=20, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0, 0.05, 1, 0.95])

# Save as SVG (vector graphics - infinitely scalable)
plt.savefig('images/rlrf-performance-charts.svg', format='svg', bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Saved: images/rlrf-performance-charts.svg (SVG - vector)")

# Save as PDF (also vector, good for papers)
plt.savefig('images/rlrf-performance-charts.pdf', format='pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Saved: images/rlrf-performance-charts.pdf (PDF - vector)")

# Save high-resolution PNG as fallback
plt.savefig('images/rlrf-performance-charts.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("Saved: images/rlrf-performance-charts.png (300 DPI)")

# Also save an extra high-res version
plt.savefig('images/rlrf-performance-charts-highres.png', dpi=600, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Saved: images/rlrf-performance-charts-highres.png (600 DPI)")

plt.close()
print("\nDone! Charts generated in SVG, PDF, and PNG formats.")

