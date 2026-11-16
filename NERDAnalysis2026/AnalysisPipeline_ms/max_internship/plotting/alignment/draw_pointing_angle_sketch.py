#!/usr/bin/env python3
"""Sketch of the dimuon pointing angle cos(phi_3D), as used by ScoutingDiMuonVertexMonitor.

Geometry only: PV -> dimuon vertex displacement, dimuon momentum and the angle phi_3D between them.
Square canvas, to sit next to the bullet list on the slide.

Usage : draw_pointing_angle_sketch.py [-o plots/sketches/pointing_angle]
"""
import argparse
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Arc, FancyArrowPatch  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
C_VTX, C_MU, C_P, C_TXT = "#d62728", "#1f5fbf", "#2e7d32", "#222222"


def arrow(ax, a, b, color, lw=2.5, ls="-", head=18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=head, color=color, lw=lw, ls=ls,
                                 shrinkA=0, shrinkB=0, zorder=3))


def definition(ax):
    pv, sv = np.array([0.0, 0.0]), np.array([4.2, 2.1])
    dhat = (sv - pv) / np.linalg.norm(sv - pv)
    # muon momenta, summing to p_mumu
    pp, pm = np.array([-0.25, 1.75]), np.array([2.0, 0.25])
    p = pp + pm
    phat = p / np.linalg.norm(p)

    arrow(ax, pv, sv, C_VTX, lw=3)
    arrow(ax, sv, sv + pp, C_MU)
    arrow(ax, sv, sv + pm, C_MU)
    arrow(ax, sv, sv + p, C_P, lw=3)
    # parallelogram: p_mumu = p(mu+) + p(mu-)
    for a, b in ((sv + pp, sv + p), (sv + pm, sv + p)):
        ax.plot(*zip(a, b), color=C_MU, lw=1, ls=":", zorder=2)
    # extension of the displacement direction
    ax.plot(*zip(sv, sv + 2.4 * dhat), color=C_VTX, lw=1.5, ls="--", zorder=2)

    # angle phi_3D
    a0, a1 = np.degrees(np.arctan2(dhat[1], dhat[0])), np.degrees(np.arctan2(phat[1], phat[0]))
    ax.add_patch(Arc(sv, 2.6, 2.6, theta1=a0, theta2=a1, color=C_TXT, lw=1.5, zorder=4))
    mid = np.radians(0.5 * (a0 + a1))
    ax.text(*(sv + 1.75 * np.array([np.cos(mid), np.sin(mid)])), r"$\phi_{3D}$", fontsize=20, ha="left",
            va="center", color=C_TXT)

    ax.plot(*pv, "o", color=C_TXT, ms=13, zorder=5)
    ax.plot(*sv, "o", color=C_VTX, ms=13, zorder=5)
    ax.text(pv[0], pv[1] - 0.45, "PV", fontsize=20, weight="bold", ha="center", va="top", color=C_TXT)
    ax.text(pv[0] - 1.1, pv[1] - 1.05, "reconstructed primary vertex\nclosest to the dimuon vertex", fontsize=15,
            ha="left", va="top", color=C_TXT)
    ax.text(sv[0] + 0.35, sv[1] - 0.45, "dimuon vertex", fontsize=19, weight="bold", ha="left", va="top",
            color=C_VTX)
    ax.text(sv[0] + 0.35, sv[1] - 1.05, "fitted at HLT\n" r"from the $\mu^{+}\mu^{-}$ pair", fontsize=15, ha="left",
            va="top", color=C_VTX)
    ax.text(*(0.5 * (pv + sv) + np.array([0.1, -0.55])), r"$\vec{\Delta}_{3D}$", fontsize=22, color=C_VTX,
            ha="center")
    ax.text(*(sv + pp + np.array([-0.15, 0.2])), r"$\vec{p}(\mu^{+})$", fontsize=18, color=C_MU, ha="center")
    ax.text(*(sv + pm + np.array([0.15, -0.1])), r"$\vec{p}(\mu^{-})$", fontsize=18, color=C_MU, ha="left",
            va="center")
    ax.text(*(sv + p + np.array([0.15, 0.15])), r"$\vec{p}_{\mu\mu}$", fontsize=22, color=C_P, ha="left")

    ax.text(3.9, 5.7, r"$\cos\phi_{3D} = \dfrac{\vec{\Delta}_{3D}\cdot\vec{p}_{\mu\mu}}"
            r"{|\vec{\Delta}_{3D}|\,|\vec{p}_{\mu\mu}|}$", fontsize=22, color=C_TXT, ha="center", va="center")
    ax.text(-1.1, -3.6, r"Not to scale: only $|\vec{\Delta}_{xy}| < 50\ \mu$m is used", fontsize=14,
            style="italic", color="#666666")

    # axes triad
    o = np.array([7.9, -2.2])
    for d, lab in ((np.array([0.9, 0.15]), "y"), (np.array([0.0, 0.9]), "z"), (np.array([-0.55, -0.45]), "x")):
        arrow(ax, o, o + d, C_TXT, lw=1.2, head=10)
        ax.text(*(o + 1.2 * d), lab, fontsize=13, ha="center", va="center", color=C_TXT)

    ax.set_xlim(-1.4, 9.4)
    ax.set_ylim(-4.0, 6.8)
    ax.set_aspect("equal")
    ax.axis("off")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--output", default=os.path.join(HERE, "plots", "sketches", "pointing_angle"))
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.output), exist_ok=True)

    fig = plt.figure(figsize=(8, 8))
    definition(fig.add_axes([0.0, 0.0, 1.0, 1.0]))
    for ext in ("png", "pdf"):
        fig.savefig(f"{a.output}.{ext}", dpi=200)
    print(f"-> {a.output}.{{png,pdf}}")


if __name__ == "__main__":
    main()
