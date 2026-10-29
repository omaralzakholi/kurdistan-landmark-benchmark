import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch

GEO = json.load(open('countries.geo.json'))

def country_patches(name):
    for f in GEO['features']:
        if f['properties']['name'] == name:
            g = f['geometry']
            polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
            return polys
    return []

def draw_countries(ax, names, fc='#F2EFE9', ec='#9A9A9A', lw=0.7):
    for n in names:
        for poly in country_patches(n):
            for ring_i, ring in enumerate(poly):
                xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
                if ring_i == 0:
                    ax.fill(xs, ys, color=fc, zorder=1)
                ax.plot(xs, ys, color=ec, lw=lw, zorder=2)

NEI = ['Iraq', 'Turkey', 'Iran', 'Syria', 'Armenia', 'Azerbaijan', 'Georgia',
       'Lebanon', 'Israel', 'Jordan', 'Saudi Arabia', 'Kuwait', 'Cyprus',
       'Greece', 'Bulgaria', 'Italy', 'Egypt', 'Romania', 'Ukraine', 'Russia',
       'Turkmenistan', 'Afghanistan', 'Pakistan', 'Albania', 'Greece',
       'Bosnia and Herzegovina', 'Croatia', 'Serbia', 'Montenegro', 'Macedonia',
       'Hungary', 'Slovenia', 'Austria', 'Switzerland', 'Kosovo', 'Moldova',
       'Libya', 'Tunisia', 'Qatar', 'United Arab Emirates', 'Bahrain', 'Oman',
       'Uzbekistan', 'Kazakhstan', 'Slovakia', 'Czech Republic', 'Poland']

# approximate site coordinates (lon, lat) -- for orientation only
SITES = {
 'Shanidar Cave': (44.22, 36.83), 'Korek Mountain': (44.59, 36.63),
 'Sami Abdulrahman Park': (43.97, 36.19), 'Rawanduz Canyon': (44.52, 36.61),
 'Barzan Area': (44.05, 36.92), 'Soran Area': (44.55, 36.65),
 'Hendrin Mountain': (44.75, 36.75), 'Dukan Lake': (44.95, 35.95),
 'Azmar Mountain': (45.48, 35.58), 'Ahmad Awa Waterfall': (46.05, 35.32),
 'Hawraman Region': (46.12, 35.22), 'Qaradagh Area': (45.26, 35.31),
 'Sirwan River Area': (45.85, 35.10), 'Amedi': (43.49, 37.09),
 'Lalish': (43.30, 36.78), 'Akre': (43.89, 36.74), 'Gali Duhok': (43.00, 36.85),
 'Zakho': (42.68, 37.14), 'Shaqlawa': (44.32, 36.40),
 'Darbandikhan Lake': (45.70, 35.11), 'Darband Lake (Ranya)': (44.88, 36.25),
 'Gali Ali Bag Waterfall': (44.45, 36.63), 'Halgurd Mountain': (44.88, 36.74),
 'Przhe Mountain': (44.95, 36.62), 'Bekhal Waterfall': (44.48, 36.64),
 'Sulav Resort': (43.47, 37.10), 'Zawita Valley': (43.14, 36.90),
 'Gara Mountain': (43.35, 37.00), 'Safeen Mountain': (44.25, 36.35),
 'Piramagrun Mountain': (45.20, 35.72), 'Goizha Mountain': (45.45, 35.57),
 'Penjwen Area': (45.95, 35.62), 'Mergapan Valley': (45.35, 35.45),
 'Dore Canyon': (44.15, 36.95), 'Great Zab River': (43.90, 36.50),
 'Khalifan Area': (44.40, 36.60), 'Chami Rezan Valley': (45.05, 35.75),
 'Sartka Mountain': (45.05, 35.95), 'Smaquli Valley': (44.55, 36.10),
}
LABELS = {'Zakho': (-0.05, 0.13), 'Amedi': (0.05, 0.14), 'Lalish': (-0.55, -0.06),
          'Shanidar Cave': (0.08, 0.12), 'Dukan Lake': (0.10, -0.22),
          'Hawraman Region': (-0.95, -0.30), 'Halgurd Mountain': (0.16, 0.05),
          'Sami Abdulrahman Park': (-1.1, -0.30), }

RED = '#D65F5F'; BLUE = '#4878CF'; GREEN = '#2E8B57'

fig = plt.figure(figsize=(10.4, 4.4))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.25], wspace=0.08)

# ---------- Panel (a): the benchmark sites ----------
ax1 = fig.add_subplot(gs[0])
draw_countries(ax1, ['Iraq', 'Turkey', 'Iran', 'Syria'], lw=0.9)
for name, (x, y) in SITES.items():
    ax1.scatter(x, y, s=26, color=RED, edgecolors='white', linewidths=0.5, zorder=5)
for name, (dx, dy) in LABELS.items():
    x, y = SITES[name]
    short = {'Shanidar Cave': 'Shanidar', 'Dukan Lake': 'Dukan',
             'Hawraman Region': 'Hawraman', 'Halgurd Mountain': 'Halgurd',
             'Sami Abdulrahman Park': 'Erbil (park)',
             'Gali Ali Bag Waterfall': 'Gali Ali Bag'}.get(name, name)
    ax1.annotate(short, (x, y), (x + dx, y + dy), fontsize=7.5, zorder=6,
                 color='0.15')
ax1.annotate('Gali Ali Bag', SITES['Gali Ali Bag Waterfall'], (43.05, 36.18),
             fontsize=7.5, color='0.15', zorder=6,
             arrowprops=dict(arrowstyle='-', lw=0.6, color='0.45'))
ax1.text(42.4, 37.65, 'TURKEY', fontsize=9, color='0.45', style='italic')
ax1.text(46.25, 36.45, 'IRAN', fontsize=9, color='0.45', style='italic', rotation=90)
ax1.text(42.15, 36.25, 'SYRIA', fontsize=9, color='0.45', style='italic')
ax1.text(43.3, 35.0, 'IRAQ', fontsize=10, color='0.35', style='italic')
ax1.set_xlim(41.9, 46.75); ax1.set_ylim(34.6, 37.95)
ax1.set_aspect(1 / np.cos(np.deg2rad(36)))
ax1.set_xticks([]); ax1.set_yticks([])
for s in ax1.spines.values(): s.set_color('0.6')
ax1.set_title('(a) The 39 benchmark sites\n(locations approximate)', fontsize=9, loc='left')

# ---------- Panel (b): where the photographs were sent ----------
ax2 = fig.add_subplot(gs[1])
draw_countries(ax2, NEI, lw=0.5)
cx, cy = 44.4, 36.2  # region centroid
# shares of 312 Kurdish photographs (Qwen2.5-VL-3B country answers)
flows = [
 ('Turkey',  (35.0, 39.3), 27.9),
 ('Iran',    (53.5, 32.8), 10.3),
 ('Lebanon', (35.9, 34.1), 5.4),
 ('Italy',   (13.6, 42.6), 4.5),
 ('Armenia', (44.9, 40.3), 2.9),
]
for name, (tx, ty), share in flows:
    ax2.add_patch(FancyArrowPatch((cx, cy), (tx, ty), arrowstyle='-|>',
                  mutation_scale=11, lw=0.8 + share * 0.10, color=BLUE,
                  alpha=0.85, zorder=6,
                  connectionstyle='arc3,rad=-0.12'))
labpos = {'Turkey': (33.0, 40.1), 'Iran': (53.0, 31.6), 'Lebanon': (30.6, 32.6),
          'Italy': (11.2, 44.0), 'Armenia': (45.6, 41.0)}
for name, (tx, ty), share in flows:
    lx, ly = labpos[name]
    ax2.text(lx, ly, f'{name} {share:.1f}%', fontsize=8, color='#1F3F7A',
             weight='bold', zorder=7)
# off-map China arrow
ax2.add_patch(FancyArrowPatch((cx, cy), (59.0, 37.6), arrowstyle='-|>',
              mutation_scale=11, lw=0.8 + 4.5 * 0.10, color=BLUE, alpha=0.85,
              zorder=6, connectionstyle='arc3,rad=-0.08'))
ax2.text(51.3, 38.6, 'China 4.5% →', fontsize=8, color='#1F3F7A', weight='bold', zorder=7)
# correct marker at home
ax2.scatter([cx], [cy], s=90, marker='s', color=RED, edgecolors='white', zorder=8)
ax2.annotate('Kurdistan Region sites\ncorrect country: 8.0%', xy=(cx, cy - 0.4),
             xytext=(44.4, 29.6), fontsize=8, color=GREEN, weight='bold',
             ha='center', zorder=8,
             arrowprops=dict(arrowstyle='-', lw=0.7, color=GREEN))
ax2.text(10.6, 26.9, 'Other countries or no answer: 36.5%\n(remaining shares below 3% each)',
         fontsize=7.5, color='0.35', zorder=8)
ax2.set_xlim(9.5, 60.5); ax2.set_ylim(25.5, 46.5)
ax2.set_aspect(1 / np.cos(np.deg2rad(37)))
ax2.set_xticks([]); ax2.set_yticks([])
for s in ax2.spines.values(): s.set_color('0.6')
ax2.set_title('(b) Countries assigned to the 312 Kurdish photographs\n(Qwen2.5-VL-3B, country-identification task)', fontsize=9, loc='left')

ax1.set_anchor('N'); ax2.set_anchor('N')
plt.tight_layout()
plt.savefig('../figures/map_reassignment.png', dpi=300, bbox_inches='tight', facecolor='white')
print('map saved')
