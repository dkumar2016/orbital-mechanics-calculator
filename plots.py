"""Plot circular-orbit speed and period against altitude, with the LEO / MEO / GEO
regimes marked. Uses the functions in calculator.py, so the plot always matches
the code that is tested.

Run:    py plots.py
Output: docs/speed_period_vs_altitude.png
"""
import os

import matplotlib.pyplot as plt
import numpy as np

from calculator import (
    circular_speed_km_s,
    orbital_period_min,
    geo_altitude_km,
    leo_max_altitude_km,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PNG = os.path.join(BASE_DIR, "docs", "speed_period_vs_altitude.png")

# Colours: one series per panel, so one hue; text and grid stay neutral
LINE = "#2a78d6"
TEXT = "#0b0b0b"
TEXT_MUTED = "#52514e"
GRID = "#e4e3df"
BAND = "#f1f0ec"
SURFACE = "#fcfcfb"

# Reference satellites to label on the curves (name, altitude in km)
REFERENCES = [("ISS", 408), ("GPS", 20200), ("GEO", geo_altitude_km)]


def main():
    # Log-spaced altitudes from low LEO to beyond GEO
    altitudes = np.geomspace(160, 60000, 400)
    speeds = [circular_speed_km_s(h) for h in altitudes]
    periods_h = [orbital_period_min(h) / 60 for h in altitudes]

    fig, (ax_v, ax_t) = plt.subplots(2, 1, figsize=(9, 7.5), sharex=True,
                                     facecolor=SURFACE)

    def speed_label(h):
        return f"{circular_speed_km_s(h):.2f} km/s"

    def period_label(h):
        minutes = orbital_period_min(h)
        return f"{minutes:.1f} min" if minutes < 120 else f"{minutes / 60:.1f} h"

    # (axis, y-values, y-label, y-function, label text, label offset per reference)
    panels = [
        (ax_v, speeds, "Circular speed (km/s)", lambda h: circular_speed_km_s(h), speed_label,
         {"ISS": (8, -16, "left"), "GPS": (8, 6, "left"), "GEO": (8, 6, "left")}),
        (ax_t, periods_h, "Orbital period (hours)", lambda h: orbital_period_min(h) / 60, period_label,
         {"ISS": (8, 6, "left"), "GPS": (-10, 4, "right"), "GEO": (-10, 4, "right")}),
    ]

    for ax, values, ylabel, func, label, offsets in panels:
        ax.set_facecolor(SURFACE)

        # Regime bands: shade LEO, mark GEO with a line (its band is too thin to see on a log axis)
        ax.axvspan(altitudes[0], leo_max_altitude_km, color=BAND, zorder=0)
        ax.axvline(geo_altitude_km, color=TEXT_MUTED, linewidth=1, linestyle="--", zorder=1)

        ax.plot(altitudes, values, color=LINE, linewidth=2, zorder=3)

        # Reference points with direct labels
        for name, h in REFERENCES:
            y = func(h)
            ax.plot(h, y, "o", markersize=8, color=LINE,
                    markeredgecolor=SURFACE, markeredgewidth=2, zorder=4)
            dx, dy, ha = offsets[name]
            ax.annotate(f"{name}  {label(h)}", (h, y), xytext=(dx, dy), ha=ha,
                        textcoords="offset points", fontsize=9, color=TEXT)

        ax.set_ylabel(ylabel, color=TEXT)
        ax.grid(True, which="major", color=GRID, linewidth=0.8)
        ax.tick_params(colors=TEXT_MUTED)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(GRID)

    # Regime labels just above the upper panel (x in data units, y in axes units)
    for name, x, ha in [("LEO (up to 2,000 km)", 570, "center"),
                        ("MEO", 8500, "center"),
                        ("GEO", geo_altitude_km, "center")]:
        ax_v.text(x, 1.02, name, transform=ax_v.get_xaxis_transform(),
                  color=TEXT_MUTED, fontsize=9, ha=ha, va="bottom")

    ax_t.set_yscale("log")
    ax_t.set_yticks([1.5, 3, 6, 12, 24, 48])
    ax_t.set_yticklabels(["1.5", "3", "6", "12", "24", "48"])
    ax_t.minorticks_off()

    ax_t.set_xscale("log")
    ax_t.set_xticks([200, 500, 1000, 2000, 5000, 10000, 20000, 50000])
    ax_t.set_xticklabels(["200", "500", "1,000", "2,000", "5,000", "10,000", "20,000", "50,000"])
    ax_t.minorticks_off()
    ax_v.minorticks_off()
    ax_t.set_xlabel("Altitude above Earth's surface (km, log scale)", color=TEXT)
    ax_t.set_xlim(altitudes[0], altitudes[-1])

    fig.suptitle("Circular-orbit speed and period vs altitude", color=TEXT,
                 fontsize=13, x=0.08, ha="left")
    fig.text(0.08, 0.935, "Two-body model, spherical Earth. Higher orbits are slower and take longer.",
             color=TEXT_MUTED, fontsize=9.5)
    fig.tight_layout(rect=(0, 0, 1, 0.93))

    os.makedirs(os.path.dirname(OUTPUT_PNG), exist_ok=True)
    fig.savefig(OUTPUT_PNG, dpi=150, facecolor=SURFACE)
    print(f"Saved {OUTPUT_PNG}")


if __name__ == "__main__":
    main()