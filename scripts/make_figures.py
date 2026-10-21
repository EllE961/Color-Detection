"""Plot the HSV ranges in color_detection_app.py and measure how they cover HSV space.

Reads the color_ranges dict straight from the app's source, so the figures follow any edit.

    python scripts/make_figures.py

Writes docs/assets/color_ranges.png, docs/assets/hsv_coverage.png and results/coverage.json.
"""
import ast
import json
import os

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

BG, PANEL = "#0d0c0b", "#131211"
INK, INK2, INK3 = "#ede7de", "#aaa299", "#7a736c"
GRID = "#24221f"
EMBER, TEMPER, PURPLE, GREEN = "#d95926", "#3987e5", "#9085e9", "#199e70"
SERIES = [EMBER, TEMPER, PURPLE, GREEN, "#e8b44c", "#c0509c"]
HEAT = LinearSegmentedColormap.from_list("heat", ["#141110", "#2a1410", "#4b170c", "#7a1f0a", "#ad320c",
                                                  "#d9520f", "#f07a1e", "#f9a63b", "#fccf6b", "#fff0c2"])
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": PANEL, "savefig.facecolor": BG,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "axes.titlecolor": INK, "axes.titleweight": "semibold",
    "axes.titlesize": 12.5, "axes.titlelocation": "left", "axes.titlepad": 12, "axes.labelsize": 10,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID, "grid.linewidth": 0.8, "grid.linestyle": "-",
    "xtick.color": INK3, "ytick.color": INK3, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "xtick.major.size": 0, "ytick.major.size": 0, "xtick.major.pad": 6, "ytick.major.pad": 6,
    "axes.axisbelow": True, "font.family": ["Segoe UI", "DejaVu Sans"], "lines.linewidth": 2,
    "lines.solid_capstyle": "round", "legend.frameon": False, "legend.fontsize": 9.5, "legend.labelcolor": INK2,
    "figure.dpi": 110, "savefig.dpi": 200,
})

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")


def load_ranges():
    tree = ast.parse(open(os.path.join(ROOT, "color_detection_app.py"), encoding="utf-8").read())
    node = next(n for n in ast.walk(tree)
                if isinstance(n, ast.Assign) and ast.unparse(n.targets[0]) == "self.color_ranges")
    return eval(ast.unparse(node.value), {"np": np})  # duplicate keys collapse, as in the app


def hsv_to_rgb(h, s, v):
    return cv2.cvtColor(np.uint8([[[h, s, v]]]), cv2.COLOR_HSV2RGB)[0, 0] / 255.0


def coverage(ranges):
    H, S, V = np.meshgrid(np.arange(180), np.arange(256), np.arange(256), indexing="ij")
    count = np.zeros(H.shape, np.uint8)
    for rs in ranges.values():
        m = np.zeros(H.shape, bool)
        for lo, hi in rs:
            m |= (H >= lo[0]) & (H <= hi[0]) & (S >= lo[1]) & (S <= hi[1]) & (V >= lo[2]) & (V <= hi[2])
        count += m
    return count


def fig_ranges(ranges):
    rows = sorted(ranges.items(), key=lambda kv: (min(lo[0] for lo, _ in kv[1]) if kv[0] != "Red" else -1, kv[0]))
    fig, ax = plt.subplots(figsize=(10, 11))
    for i, (name, rs) in enumerate(rows):
        for lo, hi in rs:
            mid = [(lo[k] + hi[k]) / 2 for k in range(3)]
            ax.barh(i, hi[0] - lo[0] + 1, left=lo[0], height=0.72, color=hsv_to_rgb(*mid), edgecolor="none")
        lo, hi = rs[0]
        ax.text(183, i, f"S {lo[1]}-{hi[1]}   V {lo[2]}-{hi[2]}", va="center", fontsize=8, color=INK3)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([n for n, _ in rows], fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 180)
    ax.set_ylim(len(rows) - 0.4, -0.6)
    ax.grid(axis="x", color=GRID)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("OpenCV hue (0-179)")
    ax.set_title(f"Hue range of each of the {len(rows)} named colors")
    fig.text(0.012, 0.0, "Bar color is the center of the range. Saturation and value limits on the right "
             "(Red also covers hue 170-179).", color=INK3, fontsize=8.5, ha="left", va="top")
    fig.savefig(os.path.join(OUT, "color_ranges.png"), bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def fig_coverage(count):
    vs = [80, 150, 220]
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.2), sharey=True)
    vmax = int(count.max())
    for ax, v in zip(axes, vs):
        im = ax.imshow(count[:, :, v].T, origin="lower", aspect="auto", cmap=HEAT, vmin=0, vmax=vmax,
                       extent=[0, 180, 0, 256], interpolation="nearest")
        ax.grid(False)
        ax.set_title(f"value = {v}", fontsize=11)
        ax.set_xlabel("hue")
    axes[0].set_ylabel("saturation")
    cb = fig.colorbar(im, ax=axes, pad=0.015, fraction=0.025)
    cb.outline.set_visible(False)
    cb.ax.tick_params(colors=INK3, labelsize=8)
    cb.set_label("names that match", color=INK2, fontsize=9)
    fig.suptitle("How many color names match each HSV value", x=0.125, ha="left", color=INK,
                 fontsize=12.5, fontweight="semibold", y=1.02)
    fig.savefig(os.path.join(OUT, "hsv_coverage.png"), bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def main():
    ranges = load_ranges()
    count = coverage(ranges)
    os.makedirs(OUT, exist_ok=True)
    fig_ranges(ranges)
    fig_coverage(count)
    S = np.arange(256)[None, :, None]
    V = np.arange(256)[None, None, :]
    bright = np.broadcast_to((S >= 100) & (V >= 100), count.shape)
    stats = {
        "names": len(ranges),
        "hsv_values": int(count.size),
        "share_by_matches": {str(k): round(float((count == k).mean()), 4) for k in range(int(count.max()) + 1)},
        "share_two_or_more": round(float((count >= 2).mean()), 4),
        "saturated_bright_S100_V100": {
            "none": round(float((count[bright] == 0).mean()), 4),
            "one": round(float((count[bright] == 1).mean()), 4),
            "two_or_more": round(float((count[bright] >= 2).mean()), 4),
        },
        "max_names_at_one_value": int(count.max()),
    }
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "coverage.json"), "w") as f:
        json.dump(stats, f, indent=2)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
