#!/usr/bin/env python3
"""
Intervention-style observable for the Wilson mutual-attraction lane.

Motivation: the frozen-source and lagged-source-refresh discriminators were
unable to cleanly separate dynamic backreaction from a static-field explanation.
This script takes a different approach: INTERVENE on the source mid-propagation
and measure whether the test particle's response is:
  (a) causal (change propagates at finite speed from the source location)
  (b) instantaneous (whole field updates at the intervention step)
  (c) absent (frozen-field prediction: no response to intervention)

Three intervention types tested:
  REMOVAL   -- source mass set to 0 at T/2
  DOUBLING  -- source mass doubled at T/2
  DISPLACEMENT -- source moved by +2 lattice sites at T/2

For each intervention, we compare:
  DYNAMIC   -- Poisson field recomputed every step from current source
  FROZEN    -- Poisson field computed once at t=0, never updated
  NO_SOURCE -- source mass=0 from the start (baseline)

Observable: centroid trajectory of a test wavepacket.  If DYNAMIC shows a
trajectory change at or shortly after the intervention step (but not before),
and FROZEN does not, the mutual channel has genuine causal dynamics.

Uses the same OpenWilsonLattice, Poisson solver, and expm_multiply stepper
as frontier_wilson_frozen_source_discriminator.py.

Bounded claims only.  SIDE kept small (14) for speed.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply, spsolve

# ---------- parameters ----------
MASS = 0.30
WILSON_R = 1.0
DT = 0.08
REG = 1e-3
N_STEPS = 30          # longer run to see post-intervention response
T_INTERV = 15         # intervention at step 15 (halfway)
SIGMA = 1.0
G_VAL = 5.0
MU2 = 0.001

SIDE = 14             # small for speed
SOURCE_MASS = 1.0     # source strength (arbitrary units for rho)

INTERVENTION_TYPES = ("removal", "doubling", "displacement")
MODES = ("DYNAMIC", "FROZEN", "NO_SOURCE")

# source and test particle positions
CENTER = SIDE // 2
SOURCE_POS = (CENTER + 3, CENTER, CENTER)
TEST_POS = (CENTER - 3, CENTER, CENTER)
DISPLACEMENT_OFFSET = 2  # sites to move source for displacement intervention


# ---------- lattice ----------
class OpenWilsonLattice:
    def __init__(self, side: int):
        self.side = side
        self.n = side ** 3
        self.pos = np.zeros((self.n, 3), dtype=float)
        self.adj: dict[int, list[int]] = {}
        for x in range(side):
            for y in range(side):
                for z in range(side):
                    i = self.site_index(x, y, z)
                    self.pos[i] = [x, y, z]
                    nbrs: list[int] = []
                    for dx, dy, dz in (
                        (1, 0, 0), (-1, 0, 0),
                        (0, 1, 0), (0, -1, 0),
                        (0, 0, 1), (0, 0, -1),
                    ):
                        nx, ny, nz = x + dx, y + dy, z + dz
                        if 0 <= nx < side and 0 <= ny < side and 0 <= nz < side:
                            nbrs.append(self.site_index(nx, ny, nz))
                    self.adj[i] = nbrs
        self.lap = self._build_laplacian()

    def site_index(self, x: int, y: int, z: int) -> int:
        return x * self.side ** 2 + y * self.side + z

    def coords(self, i: int) -> tuple[int, int, int]:
        x = i // (self.side ** 2)
        y = (i % (self.side ** 2)) // self.side
        z = i % self.side
        return x, y, z

    def _build_laplacian(self):
        rows, cols, vals = [], [], []
        for i in range(self.n):
            rows.append(i)
            cols.append(i)
            vals.append(-len(self.adj[i]))
            for j in self.adj[i]:
                rows.append(i)
                cols.append(j)
                vals.append(1.0)
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def gaussian_wavepacket(self, center, sigma=SIGMA):
        psi = np.zeros(self.n, dtype=complex)
        cx, cy, cz = center
        for i in range(self.n):
            x, y, z = self.pos[i]
            r2 = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
            psi[i] = np.exp(-r2 / (2 * sigma ** 2))
        psi /= np.linalg.norm(psi)
        return psi

    def make_source_rho(self, source_pos, source_mass):
        rho = np.zeros(self.n, dtype=float)
        if source_mass > 0:
            sx, sy, sz = source_pos
            for i in range(self.n):
                x, y, z = self.pos[i]
                r2 = (x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2
                rho[i] = source_mass * np.exp(-r2 / (2 * SIGMA ** 2))
            rho /= max(np.sum(rho), 1e-30)
            rho *= source_mass
        return rho

    def solve_poisson(self, rho):
        A = self.lap - MU2 * sparse.eye(self.n) - REG * sparse.eye(self.n)
        rhs = -4.0 * np.pi * G_VAL * rho
        return spsolve(A.tocsc(), rhs).real

    def build_wilson_hamiltonian(self, phi):
        rows, cols, vals = [], [], []
        for i in range(self.n):
            for j in self.adj[i]:
                if j <= i:
                    continue
                rows.append(i)
                cols.append(j)
                vals.append(-0.5j + 0.5 * WILSON_R)
                rows.append(j)
                cols.append(i)
                vals.append(+0.5j + 0.5 * WILSON_R)
            diag = MASS + phi[i] + 0.5 * WILSON_R * len(self.adj[i])
            rows.append(i)
            cols.append(i)
            vals.append(diag)
        return sparse.csr_matrix((vals, (rows, cols)), shape=(self.n, self.n))

    def center_of_mass_vec(self, psi):
        rho = np.abs(psi) ** 2
        norm = max(np.sum(rho), 1e-30)
        return np.sum(rho[:, None] * self.pos, axis=0) / norm

    def evolve_step(self, psi, H):
        return expm_multiply(-1j * DT * H, psi)


# ---------- source schedule ----------
def source_schedule(intervention: str, step: int):
    """Return (source_pos, source_mass) for a given intervention type and step.

    Before T_INTERV: source ON at SOURCE_POS with SOURCE_MASS.
    At/after T_INTERV: depends on intervention type.
    """
    if step < T_INTERV:
        return SOURCE_POS, SOURCE_MASS

    if intervention == "removal":
        return SOURCE_POS, 0.0
    elif intervention == "doubling":
        return SOURCE_POS, 2.0 * SOURCE_MASS
    elif intervention == "displacement":
        sx, sy, sz = SOURCE_POS
        return (sx + DISPLACEMENT_OFFSET, sy, sz), SOURCE_MASS
    else:
        raise ValueError(f"unknown intervention: {intervention}")


# ---------- single run ----------
def run_single(lat: OpenWilsonLattice, mode: str, intervention: str):
    """Evolve a test wavepacket in a gravitational field from an external source.

    mode:
      DYNAMIC   -- recompute Poisson field from source rho every step
      FROZEN    -- compute Poisson field once at t=0, use forever
      NO_SOURCE -- no gravitational source at all (baseline)

    intervention: only matters for DYNAMIC mode (FROZEN and NO_SOURCE ignore it)

    Returns centroid trajectory of test particle (N_STEPS+1 x 3).
    """
    psi = lat.gaussian_wavepacket(TEST_POS)
    com = np.zeros((N_STEPS + 1, 3), dtype=float)
    com[0] = lat.center_of_mass_vec(psi)

    phi_frozen = None
    if mode == "FROZEN":
        rho_init = lat.make_source_rho(SOURCE_POS, SOURCE_MASS)
        phi_frozen = lat.solve_poisson(rho_init)

    for step in range(N_STEPS):
        if mode == "NO_SOURCE":
            phi = np.zeros(lat.n)
        elif mode == "FROZEN":
            phi = phi_frozen
        elif mode == "DYNAMIC":
            s_pos, s_mass = source_schedule(intervention, step)
            rho = lat.make_source_rho(s_pos, s_mass)
            phi = lat.solve_poisson(rho)
        else:
            raise ValueError(f"unknown mode: {mode}")

        H = lat.build_wilson_hamiltonian(phi)
        psi = lat.evolve_step(psi, H)
        psi /= np.linalg.norm(psi)
        com[step + 1] = lat.center_of_mass_vec(psi)

    return com


# ---------- analysis ----------
def centroid_velocity(com):
    """Finite-difference velocity of centroid x-component at each step."""
    vx = np.zeros(len(com))
    vx[1:] = (com[1:, 0] - com[:-1, 0]) / DT
    vx[0] = vx[1]
    return vx


def analyze_intervention(intervention: str, com_dynamic, com_frozen, com_nosource):
    """Compute intervention diagnostics.

    Key question: does the DYNAMIC trajectory diverge from FROZEN after T_INTERV
    but agree before?
    """
    # x-component centroid (along source-test axis)
    x_dyn = com_dynamic[:, 0]
    x_frz = com_frozen[:, 0]
    x_nos = com_nosource[:, 0]

    # deviation of dynamic from frozen
    dev_dyn_frz = x_dyn - x_frz

    # pre-intervention window: steps 2 to T_INTERV-1
    pre = slice(2, T_INTERV)
    # post-intervention window: steps T_INTERV+2 to end-1 (allow 2 steps for response)
    post_start = min(T_INTERV + 2, N_STEPS)
    post = slice(post_start, N_STEPS + 1)

    pre_dev_mean = float(np.mean(np.abs(dev_dyn_frz[pre])))
    pre_dev_max = float(np.max(np.abs(dev_dyn_frz[pre])))
    post_dev_mean = float(np.mean(np.abs(dev_dyn_frz[post])))
    post_dev_max = float(np.max(np.abs(dev_dyn_frz[post])))

    # velocity change at intervention
    vx_dyn = centroid_velocity(com_dynamic)
    vx_frz = centroid_velocity(com_frozen)

    # delta-v at intervention point
    dv_at_interv = float(vx_dyn[T_INTERV + 1] - vx_dyn[T_INTERV])
    dv_frozen_at_interv = float(vx_frz[T_INTERV + 1] - vx_frz[T_INTERV])

    # displacement of dynamic from no-source (gravitational pull measure)
    pull_pre = float(np.mean(x_dyn[pre] - x_nos[pre]))
    pull_post = float(np.mean(x_dyn[post] - x_nos[post]))

    # divergence ratio: post-intervention deviation should be much larger
    # than pre-intervention if intervention has a causal effect
    # (pre-intervention should be ~0 since the source is static before T_INTERV,
    # so Poisson gives the same field whether recomputed or frozen)
    ratio = post_dev_mean / max(pre_dev_mean, 1e-12)

    # causal test: response should not appear before intervention
    # check if pre-intervention dynamic-frozen deviation is near zero
    pre_near_zero = pre_dev_max < 1e-8

    # response test: post-intervention dynamic-frozen deviation should be nonzero
    post_nonzero = post_dev_mean > 1e-8

    # response onset: which step after T_INTERV does deviation first exceed threshold?
    # This tests finite propagation speed -- if the response appears only at
    # T_INTERV+1 (the very next step), the field update is instantaneous.
    # If it appears later, the propagation has finite speed.
    onset_threshold = 1e-6
    onset_step = None
    for s in range(T_INTERV, N_STEPS + 1):
        if abs(dev_dyn_frz[s]) > onset_threshold:
            onset_step = s
            break
    onset_delay = onset_step - T_INTERV if onset_step is not None else None

    return {
        "intervention": intervention,
        "pre_dev_mean": pre_dev_mean,
        "pre_dev_max": pre_dev_max,
        "post_dev_mean": post_dev_mean,
        "post_dev_max": post_dev_max,
        "divergence_ratio": ratio,
        "dv_dynamic_at_interv": dv_at_interv,
        "dv_frozen_at_interv": dv_frozen_at_interv,
        "pull_pre": pull_pre,
        "pull_post": pull_post,
        "pre_agrees_with_frozen": pre_near_zero,
        "post_diverges_from_frozen": post_nonzero,
        "causal_signature": pre_near_zero and post_nonzero,
        "onset_step": onset_step,
        "onset_delay": onset_delay,
    }


# ---------- plotting ----------
def save_plots(results, com_data):
    """Save diagnostic plots to output/."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available, skipping plots")
        return

    import os
    os.makedirs("output", exist_ok=True)

    steps = np.arange(N_STEPS + 1)
    time_axis = steps * DT

    fig, axes = plt.subplots(len(INTERVENTION_TYPES), 2, figsize=(14, 5 * len(INTERVENTION_TYPES)))
    if len(INTERVENTION_TYPES) == 1:
        axes = axes[np.newaxis, :]

    for row, intervention in enumerate(INTERVENTION_TYPES):
        data = com_data[intervention]

        # left panel: centroid x vs time
        ax = axes[row, 0]
        ax.plot(time_axis, data["DYNAMIC"][:, 0], "b-", label="DYNAMIC", linewidth=1.5)
        ax.plot(time_axis, data["FROZEN"][:, 0], "r--", label="FROZEN", linewidth=1.5)
        ax.plot(time_axis, data["NO_SOURCE"][:, 0], "k:", label="NO_SOURCE", linewidth=1.0)
        ax.axvline(T_INTERV * DT, color="gray", linestyle="-.", alpha=0.7, label="intervention")
        ax.set_xlabel("time (lattice units)")
        ax.set_ylabel("centroid x")
        ax.set_title(f"Intervention: {intervention}")
        ax.legend(fontsize=8)

        # right panel: dynamic-frozen deviation
        ax = axes[row, 1]
        dev = data["DYNAMIC"][:, 0] - data["FROZEN"][:, 0]
        ax.plot(time_axis, dev, "g-", linewidth=1.5)
        ax.axvline(T_INTERV * DT, color="gray", linestyle="-.", alpha=0.7, label="intervention")
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_xlabel("time (lattice units)")
        ax.set_ylabel("x_dynamic - x_frozen")
        ax.set_title(f"Dynamic-Frozen deviation: {intervention}")
        ax.legend(fontsize=8)

    plt.tight_layout()
    path = "output/wilson_intervention.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  plot saved to {path}")


# ---------- main ----------
def main():
    t0 = time.time()

    print("=" * 100)
    print("WILSON MUTUAL-ATTRACTION: INTERVENTION-STYLE OBSERVABLE")
    print("=" * 100)
    print(f"MASS={MASS}, WILSON_R={WILSON_R}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"G={G_VAL}, mu2={MU2}, REG={REG}, SIGMA={SIGMA}")
    print(f"SIDE={SIDE}, T_INTERV={T_INTERV}")
    print(f"SOURCE_POS={SOURCE_POS}, TEST_POS={TEST_POS}")
    print(f"SOURCE_MASS={SOURCE_MASS}, DISPLACEMENT_OFFSET={DISPLACEMENT_OFFSET}")
    print(f"intervention types: {INTERVENTION_TYPES}")
    print()

    lat = OpenWilsonLattice(SIDE)
    print(f"lattice: {SIDE}^3 = {lat.n} sites  (built in {time.time() - t0:.1f}s)")
    print()

    # ---------- run baselines (shared across interventions) ----------
    print("running FROZEN baseline ...")
    t1 = time.time()
    # FROZEN is the same for all interventions (field set once at t=0, never updated)
    com_frozen = run_single(lat, "FROZEN", "removal")
    print(f"  FROZEN done ({time.time() - t1:.1f}s)")

    print("running NO_SOURCE baseline ...")
    t1 = time.time()
    com_nosource = run_single(lat, "NO_SOURCE", "removal")
    print(f"  NO_SOURCE done ({time.time() - t1:.1f}s)")

    # ---------- run each intervention ----------
    results = []
    com_data = {}
    for intervention in INTERVENTION_TYPES:
        print(f"\nrunning DYNAMIC with intervention={intervention} ...")
        t1 = time.time()
        com_dynamic = run_single(lat, "DYNAMIC", intervention)
        elapsed = time.time() - t1
        print(f"  DYNAMIC/{intervention} done ({elapsed:.1f}s)")

        result = analyze_intervention(intervention, com_dynamic, com_frozen, com_nosource)
        results.append(result)
        com_data[intervention] = {
            "DYNAMIC": com_dynamic,
            "FROZEN": com_frozen,
            "NO_SOURCE": com_nosource,
        }

    # ---------- per-intervention results ----------
    print()
    print("=" * 100)
    print("PER-INTERVENTION RESULTS")
    print("=" * 100)
    hdr = (
        f"{'intervention':>14s} | "
        f"{'pre_dev':>10s} {'post_dev':>10s} {'ratio':>10s} | "
        f"{'dv_dyn':>10s} {'dv_frz':>10s} | "
        f"{'pull_pre':>10s} {'pull_post':>10s} | "
        f"{'pre~frz':>7s} {'post!=frz':>9s} {'causal':>6s} {'onset':>6s}"
    )
    print(hdr)
    print("-" * len(hdr))
    for r in results:
        print(
            f"{r['intervention']:>14s} | "
            f"{r['pre_dev_mean']:10.2e} {r['post_dev_mean']:10.2e} {r['divergence_ratio']:10.1e} | "
            f"{r['dv_dynamic_at_interv']:+10.2e} {r['dv_frozen_at_interv']:+10.2e} | "
            f"{r['pull_pre']:+10.6f} {r['pull_post']:+10.6f} | "
            f"{'Y' if r['pre_agrees_with_frozen'] else 'N':>7s} "
            f"{'Y' if r['post_diverges_from_frozen'] else 'N':>9s} "
            f"{'Y' if r['causal_signature'] else 'N':>6s} "
            f"{'+' + str(r['onset_delay']) if r['onset_delay'] is not None else 'none':>6s}"
        )

    # ---------- summary and verdict ----------
    print()
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)

    n_causal = sum(1 for r in results if r["causal_signature"])
    n_pre_ok = sum(1 for r in results if r["pre_agrees_with_frozen"])
    n_post_ok = sum(1 for r in results if r["post_diverges_from_frozen"])
    n = len(results)

    print(f"interventions tested: {n}")
    print(f"pre-intervention dynamic agrees with frozen: {n_pre_ok}/{n}")
    print(f"post-intervention dynamic diverges from frozen: {n_post_ok}/{n}")
    print(f"full causal signature (both): {n_causal}/{n}")
    print()

    for r in results:
        tag = r["intervention"].upper()
        if r["causal_signature"]:
            onset_msg = ""
            if r["onset_delay"] is not None:
                if r["onset_delay"] <= 1:
                    onset_msg = (
                        f" Response onset at T_INTERV+{r['onset_delay']} "
                        f"(instantaneous within solver resolution)."
                    )
                else:
                    onset_msg = (
                        f" Response onset at T_INTERV+{r['onset_delay']} "
                        f"(delayed by {r['onset_delay']} steps = {r['onset_delay'] * DT:.3f} time units)."
                    )
            print(
                f"  {tag}: CAUSAL -- dynamic trajectory matches frozen before "
                f"intervention, then diverges after. Divergence ratio = {r['divergence_ratio']:.1e}x."
                f"{onset_msg}"
            )
        elif r["post_diverges_from_frozen"] and not r["pre_agrees_with_frozen"]:
            print(
                f"  {tag}: INCONCLUSIVE -- dynamic diverges from frozen both before "
                f"and after intervention. Pre-intervention deviation = {r['pre_dev_mean']:.2e}. "
                f"Cannot isolate intervention effect from ongoing dynamic differences."
            )
        elif r["pre_agrees_with_frozen"] and not r["post_diverges_from_frozen"]:
            print(
                f"  {tag}: ADIABATIC/STATIC -- dynamic agrees with frozen both before "
                f"and after intervention. The field update has no measurable effect "
                f"on the test particle trajectory at this resolution."
            )
        else:
            print(
                f"  {tag}: NO SIGNAL -- neither pre nor post criteria met. "
                f"Pre dev = {r['pre_dev_mean']:.2e}, post dev = {r['post_dev_mean']:.2e}."
            )

    print()
    print("=" * 100)
    print("VERDICT")
    print("=" * 100)

    if n_causal == n:
        print(
            f"ALL {n} interventions show causal signature: dynamic trajectory "
            f"agrees with frozen before intervention, then diverges after."
        )
        print(
            "This is consistent with genuine self-consistent dynamics rather than "
            "a static or adiabatic field approximation."
        )
        print(
            "Bounded claim: the Poisson-sourced gravitational field on this lattice "
            "responds to source changes with a detectable, temporally-located effect "
            "on the test particle centroid."
        )
        # check if onset is instantaneous (expected for elliptic Poisson solver)
        onsets = [r["onset_delay"] for r in results if r["onset_delay"] is not None]
        if onsets and all(d <= 1 for d in onsets):
            print()
            print(
                "NOTE: Response onset is at T_INTERV+1 for all interventions. "
                "This is expected because the Poisson solver is elliptic -- it "
                "instantaneously updates the field everywhere when the source "
                "changes. This confirms the field IS dynamically recomputed "
                "(not frozen), but does NOT demonstrate finite propagation speed. "
                "A causal (retarded/wave-equation) propagator would be needed to "
                "test for light-cone structure."
            )
    elif n_causal > 0:
        causal_types = [r["intervention"] for r in results if r["causal_signature"]]
        print(
            f"{n_causal}/{n} interventions show causal signature: {causal_types}."
        )
        print(
            "Partial evidence for dynamic backreaction. The interventions that "
            "do not show a clean causal signature may require larger lattice, "
            "longer propagation, or stronger coupling."
        )
    elif n_post_ok > 0:
        print(
            f"0/{n} interventions show clean causal signature. "
            f"{n_post_ok}/{n} show post-intervention divergence but pre-intervention "
            f"deviation is already nonzero."
        )
        print(
            "The dynamic field update has a measurable effect, but it is not cleanly "
            "localized to the intervention point. The pre-existing dynamic-frozen "
            "difference obscures the causal timing."
        )
    else:
        print(
            f"0/{n} interventions show causal signature. Dynamic and frozen "
            f"trajectories are indistinguishable at this resolution."
        )
        print(
            "The Poisson field update does not produce a detectable trajectory "
            "change when the source is intervened on. At this lattice size and "
            "coupling, the mutual channel is consistent with a static-field "
            "explanation."
        )

    print()

    # ---------- save plots ----------
    save_plots(results, com_data)

    print(f"total elapsed: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
