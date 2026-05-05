#!/usr/bin/env python3
"""SU(3) Wilson plaquette finite-volume MC: data generator.

Companion runner for `PLAQUETTE_4D_MC_FSS_BOUNDED_THEOREM_NOTE_2026-05-05.md`.

This generator produces deterministic seeded periodic 3+1D SU(3) Wilson
plaquette time-series under the standard Wilson action at `beta = 6`. It is
the data side of a paired chain. The verifier runner consumes the artifacts
this generator writes; neither runner hard-codes a thermodynamic-limit value.

Protocol summary:
- gauge group SU(3), Wilson action at beta=6, periodic BC in all four
  directions on an isotropic L^3 x L lattice;
- Metropolis update with staple precomputation and multi-hit per link;
- step size epsilon auto-tuned during thermalization to a target acceptance,
  then frozen during measurement;
- thermalization length and measurement count grow with L;
- raw plaquette samples persisted as JSON to a repo-local artifact path.

Reproducibility:
- module-level constant `SEED = 42`;
- numpy global seed `np.random.seed(SEED)` re-seeded with a deterministic
  per-volume offset before each volume loop, so each artifact is bitwise
  reproducible from the recorded `(L, SEED)` pair.

Outputs (one JSON file per volume L):
- `outputs/su3_plaquette_fss_2026_05_05/L<L>_seed42_beta6.json`

Modes (`--mode`):
- `quick`  : L in {3, 4}            (~3 min;  CI-friendly default)
- `medium` : L in {3, 4, 5}         (~12 min)
- `full`   : L in {3, 4, 5, 6}      (~30 min)
- `extra`  : L in {3, 4, 5, 6, 8}   (~hours)

Or `--L <int>` to generate a single specific volume.

The generator does not assert any physics. It only writes data. Assertions
about thermodynamic-limit behavior live in the verifier runner.
"""

from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np


SEED = 42
BETA = 6.0
COMPARATOR = 0.5934  # canonical context value only; not a fitted target

ARTIFACT_DIR = os.path.join("outputs", "su3_plaquette_fss_2026_05_05")


GM = np.array(
    [
        [[0, 1, 0], [1, 0, 0], [0, 0, 0]],
        [[0, -1j, 0], [1j, 0, 0], [0, 0, 0]],
        [[1, 0, 0], [0, -1, 0], [0, 0, 0]],
        [[0, 0, 1], [0, 0, 0], [1, 0, 0]],
        [[0, 0, -1j], [0, 0, 0], [1j, 0, 0]],
        [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 0, -1j], [0, 1j, 0]],
        [[1, 0, 0], [0, 1, 0], [0, 0, -2]] / np.sqrt(3),
    ],
    dtype=complex,
)


def random_su3_near_identity(epsilon: float) -> np.ndarray:
    coeffs = np.random.randn(8) * epsilon
    hamiltonian = sum(coeffs[k] * GM[k] for k in range(8)) / 2.0
    eigvals, eigvecs = np.linalg.eigh(hamiltonian)
    return eigvecs @ np.diag(np.exp(1j * eigvals)) @ eigvecs.conj().T


def build_lattice(L: int) -> tuple[int, np.ndarray, np.ndarray]:
    """Build link index and per-link staple structure for an L^4 lattice.

    Returns:
      n_links: number of directed links in the periodic L^4 lattice;
      link_dir: shape (n_links, 4) integer (x,y,z,t) coordinates of the link's
        starting site, with the direction encoded in `link_axis`;
      link_axis: shape (n_links,) direction index in {0,1,2,3} for each link.

    The lattice has 4*L^4 links (one per (site, direction) pair). For a
    periodic Wilson action, the per-link staple in direction mu is

        Sigma_mu(x) = sum_{nu != mu} [
                          U_nu(x+mu) U_mu(x+nu)^dag U_nu(x)^dag
                        + U_nu(x+mu-nu)^dag U_mu(x-nu)^dag U_nu(x-nu) ]

    The action contribution of this link is -(beta/3) Re Tr(U_mu(x) Sigma†).
    """
    n_sites = L ** 4
    coords = np.zeros((n_sites, 4), dtype=np.int32)
    for s in range(n_sites):
        t = s // (L ** 3)
        rem = s - t * L ** 3
        z = rem // (L ** 2)
        rem -= z * L ** 2
        y = rem // L
        x = rem - y * L
        coords[s] = (x, y, z, t)

    n_links = 4 * n_sites
    link_dir = np.zeros((n_links, 4), dtype=np.int32)
    link_axis = np.zeros(n_links, dtype=np.int32)
    for s in range(n_sites):
        for mu in range(4):
            lid = 4 * s + mu
            link_dir[lid] = coords[s]
            link_axis[lid] = mu
    return n_links, link_dir, link_axis


def site_idx(x: int, y: int, z: int, t: int, L: int) -> int:
    return x + L * y + L * L * z + L * L * L * t


def link_idx(x: int, y: int, z: int, t: int, mu: int, L: int) -> int:
    return 4 * site_idx(x % L, y % L, z % L, t % L, L) + mu


def compute_staple(
    links: np.ndarray, x: int, y: int, z: int, t: int, mu: int, L: int
) -> np.ndarray:
    """Compute the staple Sigma_mu(x) for the link in direction mu at site x.

    Convention: Sigma is constructed so that each forward plaquette equals
    `U_mu(x) Sigma_fwd` and each backward plaquette equals `U_mu(x) Sigma_bwd`.
    With this convention, the Wilson action contribution of this link is

        S_link = -(beta/3) Re Tr(U_mu(x) Sigma)

    Sums six contributions: three forward-staples (one per nu != mu) and
    three backward-staples.
    """
    Sigma = np.zeros((3, 3), dtype=complex)
    coord = [x, y, z, t]
    for nu in range(4):
        if nu == mu:
            continue
        # forward staple: U_nu(x+mu) U_mu(x+nu)^dag U_nu(x)^dag
        x_plus_mu = coord.copy()
        x_plus_mu[mu] = (x_plus_mu[mu] + 1) % L
        x_plus_nu = coord.copy()
        x_plus_nu[nu] = (x_plus_nu[nu] + 1) % L
        a = links[link_idx(*x_plus_mu, nu, L)]
        b = links[link_idx(*x_plus_nu, mu, L)]
        c = links[link_idx(*coord, nu, L)]
        Sigma += a @ b.conj().T @ c.conj().T

        # backward staple: U_nu(x+mu-nu)^dag U_mu(x-nu)^dag U_nu(x-nu)
        x_minus_nu = coord.copy()
        x_minus_nu[nu] = (x_minus_nu[nu] - 1) % L
        x_plus_mu_minus_nu = x_plus_mu.copy()
        x_plus_mu_minus_nu[nu] = (x_plus_mu_minus_nu[nu] - 1) % L
        d = links[link_idx(*x_plus_mu_minus_nu, nu, L)]
        e = links[link_idx(*x_minus_nu, mu, L)]
        f = links[link_idx(*x_minus_nu, nu, L)]
        Sigma += d.conj().T @ e.conj().T @ f
    return Sigma


def average_plaquette(links: np.ndarray, L: int) -> float:
    """Compute <P> averaged over the whole lattice and the six orientations."""
    total = 0.0
    n_plaquettes = 0
    for s in range(L ** 4):
        t = s // (L ** 3)
        rem = s - t * L ** 3
        z = rem // (L ** 2)
        rem -= z * L ** 2
        y = rem // L
        x = rem - y * L
        for mu in range(4):
            for nu in range(mu + 1, 4):
                a = links[link_idx(x, y, z, t, mu, L)]
                bx = (x + (1 if mu == 0 else 0)) % L
                by = (y + (1 if mu == 1 else 0)) % L
                bz = (z + (1 if mu == 2 else 0)) % L
                bt = (t + (1 if mu == 3 else 0)) % L
                b = links[link_idx(bx, by, bz, bt, nu, L)]
                cx = (x + (1 if nu == 0 else 0)) % L
                cy = (y + (1 if nu == 1 else 0)) % L
                cz = (z + (1 if nu == 2 else 0)) % L
                ct = (t + (1 if nu == 3 else 0)) % L
                c = links[link_idx(cx, cy, cz, ct, mu, L)]
                d = links[link_idx(x, y, z, t, nu, L)]
                M = a @ b @ c.conj().T @ d.conj().T
                total += np.real(np.trace(M)) / 3.0
                n_plaquettes += 1
    return float(total / n_plaquettes)


def sweep_metropolis(links: np.ndarray, L: int, epsilon: float, n_hits: int) -> float:
    """One full Metropolis sweep with staple precomputation and multi-hit.

    Returns the per-link acceptance rate.
    """
    n_accept = 0
    n_total = 0
    for s in range(L ** 4):
        t = s // (L ** 3)
        rem = s - t * L ** 3
        z = rem // (L ** 2)
        rem -= z * L ** 2
        y = rem // L
        x = rem - y * L
        for mu in range(4):
            lid = link_idx(x, y, z, t, mu, L)
            Sigma = compute_staple(links, x, y, z, t, mu, L)
            U = links[lid]
            for _ in range(n_hits):
                X = random_su3_near_identity(epsilon)
                U_new = X @ U
                delta_S = -(BETA / 3.0) * np.real(np.trace((U_new - U) @ Sigma))
                n_total += 1
                if delta_S < 0 or np.random.rand() < np.exp(-delta_S):
                    U = U_new
                    n_accept += 1
            links[lid] = U
    return n_accept / max(n_total, 1)


def thermalize(
    links: np.ndarray,
    L: int,
    n_sweeps: int,
    epsilon0: float,
    n_hits: int,
    target_acc: float,
    log_every: int,
) -> tuple[float, list[dict]]:
    epsilon = epsilon0
    history: list[dict] = []
    start = time.time()
    for it in range(n_sweeps):
        acc = sweep_metropolis(links, L, epsilon, n_hits)
        if it % log_every == log_every - 1:
            P = average_plaquette(links, L)
            history.append(
                {"sweep": it + 1, "P": P, "acc": acc, "eps": epsilon, "wall": round(time.time() - start, 1)}
            )
            print(
                f"    therm {it + 1:5d}: P={P:.4f} acc={acc:.2f} eps={epsilon:.3f} t={time.time() - start:.0f}s"
            )
        if acc > target_acc + 0.05:
            epsilon *= 1.05
        elif acc < target_acc - 0.05:
            epsilon *= 0.95
        epsilon = float(np.clip(epsilon, 0.05, 2.5))
    return epsilon, history


def measure(
    links: np.ndarray,
    L: int,
    n_sweeps: int,
    epsilon: float,
    n_hits: int,
    sample_every: int,
    log_every: int,
) -> tuple[list[float], list[float], list[dict]]:
    samples: list[float] = []
    accs: list[float] = []
    history: list[dict] = []
    start = time.time()
    for it in range(n_sweeps):
        acc = sweep_metropolis(links, L, epsilon, n_hits)
        accs.append(acc)
        if (it + 1) % sample_every == 0:
            P = average_plaquette(links, L)
            samples.append(P)
            if (len(samples)) % log_every == 0:
                history.append(
                    {"sample": len(samples), "P": P, "acc_mean": float(np.mean(accs)), "wall": round(time.time() - start, 1)}
                )
                print(
                    f"    measure {it + 1:5d} (n={len(samples)}): P={P:.4f} acc={np.mean(accs):.2f} t={time.time() - start:.0f}s"
                )
    return samples, accs, history


def run_volume(L: int, args: argparse.Namespace) -> dict:
    print()
    print(f"=== L = {L} ===")
    print(f"sites={L ** 4}, links={4 * L ** 4}, plaquettes={6 * L ** 4}")

    np.random.seed(SEED + L)
    links = np.tile(np.eye(3, dtype=complex), (4 * L ** 4, 1, 1))

    n_thermalize = max(args.therm_min, args.therm_factor * (L ** 4))
    n_measure = max(args.meas_min, args.meas_factor * (L ** 4))
    n_thermalize = min(n_thermalize, args.therm_cap)
    n_measure = min(n_measure, args.meas_cap)
    sample_every = args.sample_every
    n_hits = args.hits
    epsilon0 = 0.5

    print(
        f"protocol: therm={n_thermalize}, measure={n_measure}, sample_every={sample_every},"
        f" hits/link={n_hits}, target_acc={args.target_acc}"
    )

    eps_after, therm_history = thermalize(
        links, L, n_thermalize, epsilon0, n_hits, args.target_acc, log_every=max(1, n_thermalize // 5)
    )
    print(f"frozen epsilon={eps_after:.4f}")

    samples, accs, meas_history = measure(
        links, L, n_measure, eps_after, n_hits, sample_every, log_every=max(1, (n_measure // sample_every) // 4)
    )

    mean = float(np.mean(samples))
    naive_se = float(np.std(samples, ddof=1) / np.sqrt(len(samples)))
    print(f"summary L={L}: mean P = {mean:.4f}, naive_se = {naive_se:.4f}, n_samples = {len(samples)}")

    return {
        "L": L,
        "beta": BETA,
        "seed": SEED,
        "lattice": "isotropic 4D periodic",
        "action": "Wilson plaquette",
        "sites": L ** 4,
        "links": 4 * L ** 4,
        "plaquettes": 6 * L ** 4,
        "n_thermalize": n_thermalize,
        "n_measure_sweeps": n_measure,
        "sample_every": sample_every,
        "hits_per_link": n_hits,
        "target_acceptance": args.target_acc,
        "epsilon_frozen": eps_after,
        "acceptance_during_measure": float(np.mean(accs)),
        "samples": samples,
        "naive_mean": mean,
        "naive_se": naive_se,
        "thermalization_log": therm_history,
        "measurement_log": meas_history,
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--mode",
        choices=("quick", "medium", "full", "extra"),
        default="quick",
        help="quick=[3,4], medium=[3,4,5], full=[3,4,5,6], extra=[3,4,5,6,8]",
    )
    p.add_argument(
        "--L",
        type=int,
        default=None,
        help="single-volume override; if set, overrides --mode",
    )
    p.add_argument("--hits", type=int, default=3, help="multi-hit per link in Metropolis")
    p.add_argument("--target-acc", type=float, default=0.50, help="target Metropolis acceptance")
    p.add_argument("--sample-every", type=int, default=2, help="sample interval (in sweeps)")
    p.add_argument("--therm-factor", type=int, default=1, help="thermalization sweeps = factor * L^4")
    p.add_argument("--therm-min", type=int, default=300, help="minimum thermalization sweeps")
    p.add_argument("--therm-cap", type=int, default=1500, help="cap on thermalization sweeps")
    p.add_argument("--meas-factor", type=int, default=2, help="measurement sweeps = factor * L^4")
    p.add_argument("--meas-min", type=int, default=600, help="minimum measurement sweeps")
    p.add_argument("--meas-cap", type=int, default=2000, help="cap on measurement sweeps")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    print("=" * 78)
    print("SU(3) WILSON PLAQUETTE 4D FINITE-VOLUME DATA GENERATOR")
    print("=" * 78)
    print(f"seed={SEED}, beta={BETA}, comparator (context only)={COMPARATOR}")

    if args.L is not None:
        Ls = [args.L]
    else:
        Ls = {
            "quick": [3, 4],
            "medium": [3, 4, 5],
            "full": [3, 4, 5, 6],
            "extra": [3, 4, 5, 6, 8],
        }[args.mode]
    print(f"Ls = {Ls}, mode = {args.mode if args.L is None else 'single'}")

    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    for L in Ls:
        artifact = run_volume(L, args)
        path = os.path.join(ARTIFACT_DIR, f"L{L}_seed{SEED}_beta6.json")
        with open(path, "w") as f:
            json.dump(artifact, f, indent=2)
        print(f"wrote artifact: {path}")

    print()
    print("=" * 78)
    print("DATA GENERATION COMPLETE")
    print("=" * 78)
    print("Run the verifier next:")
    print("  python3 scripts/frontier_su3_4d_plaquette_fss_verify_2026_05_05.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
