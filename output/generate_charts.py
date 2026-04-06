#!/usr/bin/env python3
"""Generate all charts for Week 2 report using matplotlib"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

# Font setup
plt.rcParams['font.family'] = 'NanumSquare'
plt.rcParams['axes.unicode_minus'] = False

outdir = "/home/ubuntu/.cokacdir/workspace/cp7jpheo/insight_lab/output/charts"
os.makedirs(outdir, exist_ok=True)

colors = {
    'red': '#e63946', 'teal': '#2a9d8f', 'orange': '#f4a261',
    'dark': '#264653', 'bg': '#fafafa'
}

# Chart 1: Entropy vs Energy curve
fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor(colors['bg'])
ax.set_facecolor(colors['bg'])

phases = ["건국", "팽창", "전성기", "정체", "과잉팽창", "위기", "붕괴"]
entropy = [10, 20, 35, 55, 75, 90, 98]
energy = [90, 85, 70, 50, 40, 25, 10]
x = range(len(phases))

ax.fill_between(x, entropy, alpha=0.15, color=colors['red'])
ax.plot(x, entropy, '-o', color=colors['red'], linewidth=2.5, markersize=8, label='Entropy (무질서도)')
ax.plot(x, energy, '--s', color=colors['teal'], linewidth=2.5, markersize=8, label='Effective Energy (유효 에너지)')
ax.axvline(4, linestyle=':', color=colors['dark'], alpha=0.6)
ax.annotate('Overstretch\nThreshold', xy=(4.1, 78), fontsize=10, color=colors['dark'], style='italic')
ax.set_xticks(range(len(phases)))
ax.set_xticklabels(phases, fontsize=11, rotation=20)
ax.set_ylabel('Level (%)', fontsize=12)
ax.set_title('Empire Lifecycle: Entropy vs Effective Energy', fontsize=15, fontweight='bold', pad=15)
ax.legend(fontsize=11, loc='center left')
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 105)
plt.tight_layout()
plt.savefig(f"{outdir}/chart1_entropy_curve.png", dpi=150)
plt.close()
print("Chart 1 saved")

# Chart 2: Ibn Khaldun cycle
fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor(colors['bg'])
ax.set_facecolor(colors['bg'])

gens = ["1세대:\n사막의 강인함", "2세대:\n정복과 확립", "3세대:\n사치와 안일", "4세대:\n쇠퇴와 대체"]
asabiyyah = [95, 70, 35, 10]
soc_entropy = [5, 30, 65, 90]
x = np.arange(len(gens))
w = 0.35

bars1 = ax.bar(x - w/2, asabiyyah, w, label='Asabiyyah (아사비야)', color=colors['teal'], alpha=0.8)
bars2 = ax.bar(x + w/2, soc_entropy, w, label='Social Entropy (사회 엔트로피)', color=colors['red'], alpha=0.8)

for bar, val in zip(bars1, asabiyyah):
    ax.text(bar.get_x() + bar.get_width()/2, val + 2, str(val), ha='center', fontsize=10, color=colors['teal'], fontweight='bold')
for bar, val in zip(bars2, soc_entropy):
    ax.text(bar.get_x() + bar.get_width()/2, val + 2, str(val), ha='center', fontsize=10, color=colors['red'], fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(gens, fontsize=10)
ax.set_ylabel('Level (%)', fontsize=12)
ax.set_title("Ibn Khaldun's Dynastic Cycle: Asabiyyah vs Social Entropy", fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f"{outdir}/chart2_khaldun_cycle.png", dpi=150)
plt.close()
print("Chart 2 saved")

# Chart 3: Kennedy Overstretch
fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor(colors['bg'])
ax.set_facecolor(colors['bg'])

t = np.linspace(0, 100, 200)
military = np.clip(10 + 0.8*t + 0.005*t**2, 0, 100)
economic = np.clip(100 - 0.1*t - 0.008*t**2, 5, 100)

cross_idx = np.argmax(military >= economic)
cross_t = t[cross_idx]

ax.plot(t, military, color=colors['red'], linewidth=2.5, label='Military Burden (% GDP)')
ax.plot(t, economic, color=colors['teal'], linewidth=2.5, label='Economic Vitality Index')
ax.axvline(cross_t, linestyle='--', color=colors['orange'], linewidth=1.5)
ax.axvspan(cross_t, 100, alpha=0.06, color=colors['orange'])
ax.annotate('Point of No Return\n(Overstretch Threshold)', xy=(cross_t+2, 62),
            fontsize=10, color=colors['orange'], fontweight='bold')
ax.set_xlabel('Time (Relative)', fontsize=12)
ax.set_ylabel('Index', fontsize=12)
ax.set_title("Kennedy's Overstretch Model", fontsize=15, fontweight='bold', pad=15)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f"{outdir}/chart3_kennedy_overstretch.png", dpi=150)
plt.close()
print("Chart 3 saved")

# Chart 4: Bifurcation diagram
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(colors['bg'])
ax.set_facecolor(colors['bg'])

np.random.seed(42)
x_main = np.linspace(0, 5, 100)
y_main = 50 + 2*x_main

x_chaos = np.linspace(4, 6, 80)
y_chaos = 60 + np.random.normal(0, 8, 80)

x_upper = np.linspace(5, 10, 100)
y_upper = 60 + 5*(x_upper - 5) + np.random.normal(0, 1.2, 100)

x_lower = np.linspace(5, 10, 100)
y_lower = 60 - 8*(x_lower - 5) + np.random.normal(0, 1.2, 100)

ax.plot(x_main, y_main, color=colors['dark'], linewidth=3, label='Old Order')
ax.scatter(x_chaos, y_chaos, color=colors['orange'], alpha=0.3, s=10, label='Chaos Zone')
ax.plot(x_upper, y_upper, color=colors['teal'], linewidth=3, label='New Order (Path B)')
ax.plot(x_lower, y_lower, color=colors['red'], linewidth=3, label='Collapse (Path A)')
ax.axvline(5, linestyle='--', color='#457b9d', alpha=0.7)
ax.annotate('BIFURCATION\nPOINT', xy=(5.2, 92), fontsize=12, fontweight='bold', color='#457b9d')
ax.annotate('New Dissipative\nStructure', xy=(8, 83), fontsize=10, color=colors['teal'], style='italic')
ax.annotate('System Collapse', xy=(8, 15), fontsize=10, color=colors['red'], style='italic')
ax.set_xlabel('Distance from Equilibrium (Crisis Intensity)', fontsize=12)
ax.set_ylabel('System State', fontsize=12)
ax.set_title("Prigogine's Bifurcation: Crisis as Creative Destruction", fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=10, loc='upper left')
ax.set_xlim(0, 10)
ax.set_ylim(0, 100)
plt.tight_layout()
plt.savefig(f"{outdir}/chart4_bifurcation.png", dpi=150)
plt.close()
print("Chart 4 saved")

# Chart 5: US Entropy indicators
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor(colors['bg'])
ax.set_facecolor(colors['bg'])

indicators = ["Military\nOverstretch", "Domestic\nPolarization", "Fiscal\nDeficit",
              "Alliance\nCohesion", "Dollar\nHegemony", "Energy\nDependence"]
levels = [85, 90, 78, 70, 65, 55]
bar_colors = ['#e63946' if v >= 80 else '#f4a261' if v >= 60 else '#2a9d8f' for v in levels]

bars = ax.barh(indicators, levels, color=bar_colors, height=0.6)
for bar, val in zip(bars, levels):
    ax.text(val + 1.5, bar.get_y() + bar.get_height()/2, f'{val}%',
            va='center', fontsize=12, fontweight='bold', color=bar.get_facecolor())

ax.set_xlim(0, 105)
ax.set_title('US Imperial Entropy Indicators (2026)', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Entropy Level (%)', fontsize=12)
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f"{outdir}/chart5_us_entropy.png", dpi=150)
plt.close()
print("Chart 5 saved")

# Chart 6: Two futures
fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor(colors['bg'])
ax.set_facecolor(colors['bg'])

years = np.arange(2020, 2036)
current = [50, 52, 55, 58, 62, 67, 75]
collapse = [None]*6 + [75, 82, 88, 93, 96, 98, 99, 99, 99, 99]
new_order = [None]*6 + [75, 70, 60, 48, 38, 30, 25, 22, 20, 20]

ax.plot(years[:7], current, color=colors['dark'], linewidth=2.5, label='Current Trajectory')
ax.plot(years[6:], [v for v in collapse[6:]], '--', color=colors['red'], linewidth=2.5, label='Path A: Collapse')
ax.plot(years[6:], [v for v in new_order[6:]], '--', color=colors['teal'], linewidth=2.5, label='Path B: New Order')
ax.axvline(2026, linestyle=':', color='gray', alpha=0.5)
ax.annotate('2026\nIran War', xy=(2026.3, 92), fontsize=10, color='gray')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('System Entropy (%)', fontsize=12)
ax.set_title('Two Futures: Entropy Trajectories After 2026', fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 105)
plt.tight_layout()
plt.savefig(f"{outdir}/chart6_two_futures.png", dpi=150)
plt.close()
print("Chart 6 saved")
print("\nAll charts generated!")
