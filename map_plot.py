import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, RegularPolygon

# csv_path: sökväg till din CSV-fil
csv_path = "map001.csv"

# df: DataFrame som innehåller koordinater och biom
df = pd.read_csv(csv_path)

fig, ax = plt.subplots()

# radius: radien för varje hexagonmarkör
radius = 2/3

# default_color: färg för alla hexagoner
biome_styles = {
    'Water':    {'facecolor': '#00b2ac', 'edgecolor': '#004d47', 'hatch': None,  'linewidth': 0.5},
    'Bog':      {'facecolor': '#5e8b6f', 'edgecolor': '#355646', 'hatch': '///', 'linewidth': 0.5},
    'Plains':   {'facecolor': '#b4d86a', 'edgecolor': '#5a7326', 'hatch': None,  'linewidth': 0.5},
    'Wood':     {'facecolor': '#6ea34f', 'edgecolor': '#2f5422', 'hatch': '///', 'linewidth': 0.5},
    'Hill':     {'facecolor': '#c7b25b', 'edgecolor': '#7a6632', 'hatch': None,  'linewidth': 0.5},
    'Forest':   {'facecolor': '#006031', 'edgecolor': '#002e17', 'hatch': '///', 'linewidth': 0.5},
    'Mountain': {'facecolor': '#9fa9b5', 'edgecolor': '#59626d', 'hatch': None,  'linewidth': 0.5},
}

for _, row in df.iterrows():
    x = row['x']        # kartesisk position: centrum för hexagon
    y = row['y']        # kartesisk position
    col = row['col']    # kolumnindex från datasetet
    r = row['row']      # radindex från datasetet
    biome = row['biome']
    
    style = biome_styles.get(biome, biome_styles['Plains'])  # fallback om okänt biome
    
    hex_patch = RegularPolygon(
        (x, y),             # centrum
        numVertices=6,      # sexhörning
        radius=radius,      # hexagonens radie
        orientation=0,      # 0 radianer = spets uppåt
        facecolor=style['facecolor'],
        edgecolor=style['edgecolor'],
        linewidth=style['linewidth'],
        hatch=style['hatch']
    )
    ax.add_patch(hex_patch)

    ax.text(
        x, y,               # samma punkt som hexagonens centrum
        f"{col},{r}",       # text som ska visas
        ha="center",        # horisontellt centrerad
        va="center",        # vertikalt centrerad
        fontsize=6          # justera vid behov
    )

# proxy_handles: en hexagon per biom som bara används för legend
proxy_handles = []
for biome, style in biome_styles.items():
    proxy = RegularPolygon(
        (0, 0),                # godtyckligt centrum – legenden bryr sig inte
        numVertices=6,
        radius=0.4,            # liten hexagon i legendrutan
        orientation=0,
        facecolor=style['facecolor'],
        edgecolor=style['edgecolor'],
        linewidth=style['linewidth'],
        hatch=style['hatch']
    )
    proxy_handles.append((proxy, biome))

# matplotlib kräver en lista av handles och labels separat
handles = [h for h, _ in proxy_handles]
labels  = [l for _, l in proxy_handles]

legend = ax.legend(handles, labels, title="Biome", loc="upper right", fontsize=8)

# x_min, x_max: min- och maxvärden för x-koordinaten i datasetet
x_min, x_max = df['x'].min(), df['x'].max()

# y_min, y_max: min- och maxvärden för y-koordinaten i datasetet
y_min, y_max = df['y'].min(), df['y'].max()

# margin: extra marginal runt datapunkterna så hexagonerna inte klipps
margin = radius * 2

ax.set_xlim(x_min - margin, x_max + margin)
ax.set_ylim(y_min - margin, y_max + margin)

ax.set_aspect('equal')  # ser till att 1 steg i x = 1 steg i y geometriskt
plt.xlabel("x")
plt.ylabel("y")
plt.title("Hexagonmarkörer för datapunkter")
# --- skapa legend ---
proxy_handles = []
for biome, style in biome_styles.items():
    proxy = RegularPolygon(
        (0, 0),
        numVertices=6,
        radius=0.4,
        orientation=0,
        facecolor=style['facecolor'],
        edgecolor=style['edgecolor'],
        linewidth=style['linewidth'],
        hatch=style['hatch']
    )
    proxy_handles.append((proxy, biome))

handles = [h for h, _ in proxy_handles]
labels  = [l for _, l in proxy_handles]

ax.legend(handles, labels, title="Biome", loc="upper right", fontsize=8)
# ----------------------

plt.show()
