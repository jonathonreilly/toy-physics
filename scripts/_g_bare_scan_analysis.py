#!/usr/bin/env python3
"""Cross-lattice summary analysis for the g_bare scan.

Reads two JSON outputs (L=4 and L=6) and produces:
  - side-by-side plots
  - a summary table of where each observable's slope and curvature peak
  - a "distance to beta=6" metric per observable
"""
from __future__ import annotations
import json, os, sys
import numpy as np
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

OUT_DIR = "outputs/figures/g_bare_critical_feature_scan"
os.makedirs(OUT_DIR, exist_ok=True)

data = {}
for lbl, path in [("L4", "outputs/g_bare_critical_feature_scan_L4.json"),
                  ("L6", "outputs/g_bare_critical_feature_scan_L6.json")]:
    if os.path.exists(path):
        with open(path) as f:
            data[lbl] = json.load(f)
    else:
        print(f"missing {path}")

if "L4" not in data or "L6" not in data:
    print("need both L4 and L6 JSON files; run scan twice and rename outputs first")
    sys.exit(1)

def d2(x, y):
    out = np.zeros_like(y)
    for i in range(1, len(x) - 1):
        h1 = x[i] - x[i - 1]; h2 = x[i + 1] - x[i]
        out[i] = 2.0 * ((y[i + 1] - y[i]) / h2 - (y[i] - y[i - 1]) / h1) / (h1 + h2)
    return out

def locate(bg, y):
    dy = np.gradient(y, bg)
    d2y = d2(bg, y)
    # ignore boundary two points when hunting for extrema
    j = int(np.argmax(np.abs(dy[1:-1])) + 1)
    k = int(np.argmax(np.abs(d2y[1:-1])) + 1)
    return bg[j], bg[k], d2y

print(f"{'observable':>16s} | {'beta*(L4 slope)':>16s} {'beta*(L4 curv)':>16s} | "
      f"{'beta*(L6 slope)':>16s} {'beta*(L6 curv)':>16s} | convergent?")
print("-" * 110)

CRIT = {}
for obs, label in [
    ("plaquette", "<P>"),
    ("polyakov_abs", "|<L>|"),
    ("logdet_density", "ln|det|/V"),
    ("lambda_min", "lam_min"),
    ("spectral_gap", "gap"),
    ("rho_near_zero", "rho(0)"),
]:
    b4 = np.array(data["L4"]["betas"]); y4 = np.array(data["L4"][obs])
    b6 = np.array(data["L6"]["betas"]); y6 = np.array(data["L6"][obs])
    s4, c4, _ = locate(b4, y4)
    s6, c6, _ = locate(b6, y6)
    conv = "yes" if (abs(c4 - c6) < 1.0) else "shifts"
    near_6 = all(abs(b - 6.0) < 1.0 for b in (s4, s6, c4, c6))
    tag = " <- AT beta=6" if near_6 else ""
    print(f"{label:>16s} | {s4:>16.2f} {c4:>16.2f} | {s6:>16.2f} {c6:>16.2f} | {conv}{tag}")
    CRIT[obs] = {"slope_L4": float(s4), "curv_L4": float(c4),
                 "slope_L6": float(s6), "curv_L6": float(c6),
                 "near_6": near_6}

with open("outputs/g_bare_critical_location_summary.json", "w") as f:
    json.dump(CRIT, f, indent=2)

if HAVE_MPL:
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True)
    plots = [
        ("plaquette", "<P>"),
        ("polyakov_abs", "|<L>|"),
        ("logdet_density", "ln|det D|/dim"),
        ("lambda_min", "|lambda_min|"),
        ("spectral_gap", "spectral gap"),
        ("rho_near_zero", "rho(0)"),
    ]
    for ax, (obs, label) in zip(axes.flat, plots):
        b4 = np.array(data["L4"]["betas"]); y4 = np.array(data["L4"][obs])
        b6 = np.array(data["L6"]["betas"]); y6 = np.array(data["L6"][obs])
        ax.plot(b4, y4, "o-", label="L=4", color="#1f77b4", alpha=0.8)
        ax.plot(b6, y6, "s-", label="L=6", color="#d62728", alpha=0.8)
        ax.axvline(6.0, color="black", ls="--", lw=1.0, alpha=0.6, label=r"$\beta=6$")
        ax.set_title(label)
        ax.set_xlabel(r"Wilson $\beta = 2N_c/g_{\rm bare}^2$")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle("Lattice-size convergence of g_bare scan observables on $\\mathbb{Z}^3\\times L_t$", fontsize=13)
    fig.tight_layout()
    out = os.path.join(OUT_DIR, "g_bare_scan_convergence_panel.png")
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"\nwrote {out}")

    # curvature panel
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True)
    for ax, (obs, label) in zip(axes.flat, plots):
        b4 = np.array(data["L4"]["betas"]); y4 = np.array(data["L4"][obs])
        b6 = np.array(data["L6"]["betas"]); y6 = np.array(data["L6"][obs])
        ax.plot(b4, d2(b4, y4), "o-", label="L=4 d²/dβ²", color="#1f77b4", alpha=0.7)
        ax.plot(b6, d2(b6, y6), "s-", label="L=6 d²/dβ²", color="#d62728", alpha=0.7)
        ax.axvline(6.0, color="black", ls="--", lw=1.2, alpha=0.7, label=r"$\beta=6$")
        ax.axhline(0.0, color="gray", lw=0.6, alpha=0.5)
        ax.set_title(f"d²/dβ² of {label}")
        ax.set_xlabel(r"$\beta$")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle("Second-derivative panels — locate critical-feature candidates", fontsize=13)
    fig.tight_layout()
    out = os.path.join(OUT_DIR, "g_bare_scan_curvature_panel.png")
    fig.savefig(out, dpi=120)
    plt.close(fig)
    print(f"wrote {out}")

print("\nDone.")
