# Mac Mini Compute Instructions

Run these scripts on the Mac Mini to close the distance law gap.

## Setup

```bash
git clone https://github.com/jonathonreilly/toy-physics.git Physics-compute
cd Physics-compute
git checkout claude/youthful-neumann
pip3 install numpy scipy
```

## Run 1: Distance Law Definitive (96³)

```bash
python3 scripts/frontier_distance_law_definitive.py 2>&1 | tee ~/Desktop/distance_law_96.txt
```

Expected runtime: ~5 min. Runs 31³ through 96³ Poisson solver + ray deflection.

## Run 2: Distance Law with 128³ extension

Edit line 27 of the script to add 128:
```bash
sed -i '' 's/grid_sizes = \[31, 40, 48, 56, 64, 80, 96\]/grid_sizes = [31, 40, 48, 56, 64, 80, 96, 128]/' scripts/frontier_distance_law_definitive.py
python3 scripts/frontier_distance_law_definitive.py 2>&1 | tee ~/Desktop/distance_law_128.txt
```

Expected runtime: ~8 min. The 128³ Poisson solve is 2.1M unknowns, ~2GB RAM, ~30s.

## Run 3: Frozen-Source Control on 64³

```bash
python3 scripts/frontier_distance_law_64_frozen_control.py 2>&1 | tee ~/Desktop/distance_law_frozen.txt
```

Expected runtime: ~2 min. Compares dynamic Poisson vs hand-crafted 1/r vs analytic sum.

## Run 4: Frozen Stars Rigorous (6-probe)

```bash
python3 scripts/frontier_frozen_stars_rigorous.py 2>&1 | tee ~/Desktop/frozen_stars_rigorous.txt
```

Expected runtime: ~10-20 min. The 3D L=14 eigendecomposition (2744 sites) is the bottleneck.

**What to report:**
- Analytical R_min/R_S formula — does it agree with numerics?
- 1D convergence: does Fermi stabilization hold at N=500, 1000?
- 3D verification: does stabilization persist at L=12, 14?
- Compactness ratio at physical masses
- **GW150914 echo time in milliseconds** — this is the headline number
- Comparison to Abedi et al. (2017) claimed ~100 ms echoes

## Run 5: Sommerfeld Lattice Green's Function (CONVERGENCE FIX)

The script computes S = G_Coulomb(r=0; E) / G_free(r=0; E) directly on a
lattice Hamiltonian. At N=2000 it gets 0/20 within 5% of the analytic formula
due to finite-size effects. Needs N >> 2000.

```bash
python3 scripts/frontier_sommerfeld_lattice_greens.py 2>&1 | tee ~/Desktop/sommerfeld_lattice.txt
```

**The fix needed:** Edit the script to increase lattice sizes:
- 1D: change N from [100, 200, 500, 1000, 2000] to [2000, 5000, 10000, 20000, 50000]
- 3D: change L from [8, 10, 12] to [16, 20, 24, 32] (if memory allows)
- Also try: increase the box size (multiply positions by a scale factor) to reduce
  boundary effects on the Coulomb wavefunction

**What to report:**
- Does S_lattice converge to S_Sommerfeld at larger N?
- At what N does it match to 5%? To 1%?
- The master table: α_s, v_rel, S_analytic, S_lattice(best N), % match
- If 3D L=32 is too large, report the largest L that fits in memory

**Why this matters:** If S_lattice matches S_Sommerfeld at large N, the
Sommerfeld enhancement is a LATTICE OBSERVABLE — codex's last flag on the
DM ratio lane is closed. R = 5.48 becomes fully structural.

Expected runtime: 10-60 min depending on max N. The 1D N=50000 eigendecomposition
is the bottleneck (~50000×50000 matrix).

**Memory note:** For 1D, N=50000 needs ~20GB RAM (dense matrix). If that's too
much, use scipy.sparse.linalg.eigsh with k=500 eigenvectors instead of full
diagonalization, and compute G(0;E) from the partial spectral sum.

## What to report back

From each run, copy the output sections:
- **FINAL VERDICT** — the extrapolated α_inf and PASS/FAIL
- **ANALYTIC CROSS-VALIDATION** — num/analytic agreement table
- **MASS INDEPENDENCE** — α spread across M values

The key number: **α_inf** should be within 1% of -1.000 (deflection convention).
That means the force exponent is within 1% of -2.000 (1/r² law).
