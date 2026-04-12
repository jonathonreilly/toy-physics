# Mac Mini Instructions: UV-IR Cosmological Constant Investigation

## Overview

The script `scripts/frontier_uv_ir_cosmological.py` runs 7 tests investigating
whether the UV-IR connection a/R_Hubble = 1.44 is physics or numerology.

On a MacBook, it runs in ~6 minutes with lattice sizes up to N=24.
On the Mac Mini, we can push to N=48+ for more reliable scaling.

## Requirements

```bash
pip3 install numpy scipy
```

## Quick Run (Laptop-scale, ~6 min)

```bash
python3 scripts/frontier_uv_ir_cosmological.py
```

## Mac Mini Modifications for Larger Lattices

The script has hardcoded lattice sizes. To push further on the Mac Mini,
edit the following constants directly in the script:

### Test 1 (Hierarchical): Line ~200

Change `N_fine = 12` to `N_fine = 20` or `24`.
This increases memory usage as O(N^6) for full eigendecomposition.
At N_fine=20, the matrix is 8000x8000 -- about 500 MB for eigvalsh.

### Test 3 (Lambda_min): Line ~340

Add larger sizes to `sizes_periodic`:
```python
sizes_periodic = [4, 6, 8, 10, 12, 14, 16, 20, 24, 32, 40, 48]
```
At N=48, the sparse eigensolver handles n=110,592 nodes comfortably.
The sparse eigsh (which='SM') call takes ~30s at N=48.

### Test 4 (Growing graph): Line ~390

Change `N_FINAL = 200` to `N_FINAL = 1000` or more.
This tests Lambda scaling over a wider range but grows linearly in time.
At N=1000, each lambda_min computation (sparse eigsh, k=6) takes ~2s.
Total: ~15 min for 1000 nodes with 20 measurement points.

### Test 6 (Spectral gap): Line ~470

Add larger sizes: `sizes_p = [4, 6, 8, 10, 12, 14, 16, 20, 24, 32]`.
The full eigendecomposition (needed for gap/BW ratio) works up to N=16
(n=4096). For larger N, only the sparse eigsh results are available.

### Test 7 (Holographic mode counting): Line ~520

Add N=16, 18, 20 to `sizes`:
```python
sizes = [6, 8, 10, 12, 14, 16, 18, 20]
```
At N=20, full eigendecomposition of the 8000x8000 Laplacian takes ~10s.
At N=24, n=13,824 -- this needs ~16 GB RAM and ~60s.

## Memory Estimates

| N (lattice side) | n = N^3 | Dense matrix (float64) | eigvalsh time |
|------------------|---------|------------------------|---------------|
| 16               | 4,096   | 128 MB                 | ~2s           |
| 20               | 8,000   | 488 MB                 | ~10s          |
| 24               | 13,824  | 1.4 GB                 | ~60s          |
| 32               | 32,768  | 8.0 GB                 | ~10 min       |
| 40               | 64,000  | 31 GB                  | sparse only   |
| 48               | 110,592 | 93 GB                  | sparse only   |

For N > 24, use ONLY sparse eigensolver (eigsh with k << n).
This gets the lowest few eigenvalues in O(n) memory and O(n*k) time.

## Key Quantities to Watch

1. **lambda_min scaling exponent** (Test 3): Should approach -2.0 with larger N.
   Currently -1.90 (periodic) and -2.19 (Dirichlet).

2. **Holographic rho_holo exponent** (Test 7): Currently -0.43 vs expected -1/3.
   Larger N should clarify whether this converges to -1/3 or stays steeper.

3. **Growing graph exponent** (Test 4): Spatial growth gives -0.87 at N=20-200.
   Need N up to 2000+ to see if it converges to -2/3.

4. **Self-consistent UV/IR ratio** (Test 2): Currently ~ N^(-22). Need larger N
   to see if this is a real power law or an exponential decay.

## Recommended Mac Mini Run

Create a modified script for the Mac Mini:

```bash
# Copy and modify
cp scripts/frontier_uv_ir_cosmological.py scripts/frontier_uv_ir_cosmological_large.py
# Edit sizes as described above
# Run with nohup for long jobs
nohup python3 scripts/frontier_uv_ir_cosmological_large.py > uv_ir_large_output.txt 2>&1 &
```

Expected runtime on Mac Mini (M2/M4, 16+ GB RAM):
- With N up to 32: ~30 min
- With N up to 48 (sparse only): ~2 hours
- With growing graph to N=2000: ~1 hour

## What Success Looks Like

The UV-IR connection is promoted from "suggestive" to "robust" if:

1. lambda_min exponent converges to exactly -2.0 at large N (Test 3)
2. Holographic rho_holo exponent converges to -1/3 (Test 7)
3. Spatial growing graph gives exponent -2/3 at large N (Test 4)
4. All three mechanisms agree on Lambda ~ 1/L^2
