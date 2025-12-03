import matplotlib.pyplot as plt
import mplhep as hep

# Apply CMS style globally
hep.style.use("CMS")

import matplotlib.pyplot as plt
import json

data = [
    {"Element": "AlCa", "Time": 56.2, "Fraction": 1.7},
    {"Element": "DQM", "Time": 26.7, "Fraction": 0.8},
    {"Element": "E/Gamma", "Time": 41.6, "Fraction": 1.3},
    {"Element": "ECAL", "Time": 48.1, "Fraction": 1.5},
    {"Element": "event setup", "Time": 10.6, "Fraction": 0.3},
    {"Element": "Framework", "Time": 0.0, "Fraction": 0.0},
    {"Element": "HCAL", "Time": 86.5, "Fraction": 2.7},
    {"Element": "HLT", "Time": 0.1, "Fraction": 0.0},
    {"Element": "I/O", "Time": 6.2, "Fraction": 0.2},
    {"Element": "idle", "Time": 1.0, "Fraction": 0.0},
    {"Element": "Jets/MET", "Time": 57.2, "Fraction": 1.8},
    {"Element": "L1T", "Time": 0.2, "Fraction": 0.0},
    {"Element": "Muons", "Time": 623.6, "Fraction": 19.2},
    {"Element": "Particle Flow", "Time": 348.9, "Fraction": 10.7},
    {"Element": "Pixels", "Time": 443.9, "Fraction": 13.6},
    {"Element": "Tracking", "Time": 1305.8, "Fraction": 40.1},
    {"Element": "Unassigned", "Time": 0.0, "Fraction": 0.0},
    {"Element": "Vertices", "Time": 141.9, "Fraction": 4.4},
    {"Element": "other", "Time": 55.8, "Fraction": 1.7},
]

# JSON color mapping
color_json = """
{
  "AlCa": "#ff9999",
  "B tagging": "#663300",
  "DQM": "#a00000",
  "E/Gamma": "#ffee00",
  "ECAL": "#4ddbff",
  "Framework": "#404040",
  "HCAL": "#b5a642",
  "HGCal": "#daa520",
  "HLT": "#808080",
  "I/O": "#222222",
  "Jets/MET": "#ee3300",
  "L1T": "#cccccc",
  "Muons": "#0040ff",
  "Particle Flow": "#ff66cc",
  "Pixels": "#33ff33",
  "Pixel track and vertex": "#33ff33",
  "Taus": "#800055",
  "Tracking": "#009900",
  "Full track and vertex": "#009900",
  "Vertices": "#006600",
  "Pixels on GPU": "#33ff33",
  "ECAL on GPU": "#4ddbff",
  "HCAL on GPU": "#b5a642",
  "others": "#cccccc",
  "non-event processing": "#808080",
  "event setup": "#404040",
  "idle": "#e8e8e8",
  "other": "#ffffff"
}
"""
colors_map = json.loads(color_json)

# Filter out elements <1% for display
labels = [d["Element"] if d["Fraction"] >= 1 else '' for d in data if d["Time"] > 0]
sizes = [d["Time"] for d in data if d["Time"] > 0]
colors = [colors_map.get(d["Element"], "#cccccc") for d in data if d["Time"] > 0]

# Function to show percentage only if >=1%
def autopct_filter(pct):
    return f'{pct:.1f}%' if pct >= 1 else ''

# Create figure
fig, ax = plt.subplots(figsize=(12, 12))

# Draw pie chart on the CMS-style axis
wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    colors=colors,
    autopct=autopct_filter,
    startangle=140,
    textprops={'fontsize': 14, 'fontweight': 'bold'}
)

# Make the autopct text bold
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_fontweight('bold')

# Add white circle for donut
centre_circle = plt.Circle((0, 0), 0.40, color='white')
ax.add_artist(centre_circle)

# Add total time in center
total_time = sum(sizes)
ax.text(0, 0, f'{total_time:.1f} ms', horizontalalignment='center', 
        verticalalignment='center', fontsize=20, fontweight='bold')

# Add CMS Preliminary label
fontsize = 20
hep.cms.text("Preliminary", ax=ax, fontsize=fontsize)       # top-left by default
hep.cms.lumitext("2025 (13.6 TeV)", ax=ax, fontsize=fontsize)  # top-right by default

# Ensure the pie chart is circular
ax.axis('equal')

#plt.show()

# Save as PNG
plt.savefig("cms_pie_chart_twoIters.png", dpi=300, bbox_inches='tight')

# Save as PDF
plt.savefig("cms_pie_chart_twoIters.pdf", bbox_inches='tight')
