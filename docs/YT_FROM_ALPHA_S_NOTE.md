# Top Yukawa from alpha_s via Cl(3) Trace Constraint

## Context

The Higgs mass prediction (HIGGS_FROM_LATTICE_NOTE.md) depends on y_t.
The top Yukawa note (TOP_YUKAWA_NOTE.md) showed that y_t is constrained
but not yet derived. This note keeps the lane honest: the Cl(3) trace
structure narrows the allowed coefficient family, but the exact CG factor
is still not uniquely fixed from the retained cubic surface.

## Input

| Quantity | Value | Origin |
|----------|-------|--------|
| alpha_s(M_Pl) | 0.092 | V-scheme plaquette action |
| sin^2(theta_W)(M_Pl) | 3/8 | Cl(3) GUT relation |
| g_s(M_Pl) | 1.075 | sqrt(4*pi*alpha_s) |

## The Constraint

### Step 1: Cl(3) Taste Decomposition

The 8-dimensional taste space of the staggered lattice decomposes
under the Cl(3) grading by Hamming weight:

    8 = 1 (hw=0) + 3 (hw=1) + 3 (hw=2) + 1 (hw=3)

The singlets (hw=0, hw=3) correspond to the scalar and pseudoscalar
channels; the triplet/anti-triplet to the vector/pseudovector channels.

### Step 2: Yukawa Operator Identification

The Higgs field in the Cl(3) framework corresponds to the chiral
projector in taste space:

    P_+ = (1 + G5) / 2

where G5 = i * G1 * G2 * G3 is the pseudoscalar (chirality operator).
P_+ is a rank-4 projector (half the taste space).

### Step 3: Trace Identity

The key algebraic relation:

    Tr(P_+^dag P_+) / dim(taste) = 4/8 = 1/2

Combined with the color factor N_c = 3 for the top quark:

    N_c * y_t^2 = (1/2) * g^2

This gives the benchmark Clebsch-Gordan relation:

    y_t = g / sqrt(2 * N_c) = g / sqrt(6)

### Step 4: Numerical Benchmarks

    y_t(M_Pl) = g_s(M_Pl) / sqrt(6)
              = 1.075 / 2.449
              = 0.439

### Step 5: RG Running to M_Z

Using 1-loop SM RGEs from M_Planck to M_Z:

    y_t(M_Z) = 1.027

    m_t = y_t * v / sqrt(2) = 178.8 GeV

## Results

| Quantity | Benchmark | Observed | Deviation |
|----------|-----------|----------|-----------|
| y_t(M_Pl) | 0.439 | 0.405 (from inversion) | +8.4% |
| y_t(M_Z) | 1.027 | 0.994 | +3.4% |
| m_t | 178.8 GeV | 173.0 GeV | +3.4% |

## Alternative Formulas Explored

| Formula | y_t(M_Pl) | y_t(M_Z) | m_t (GeV) | dev(m_t) |
|---------|----------|----------|-----------|----------|
| g_s/sqrt(6) (trace identity) | 0.439 | 1.027 | 178.8 | +3.4% |
| g_s/sqrt(7) | 0.406 | 0.995 | 173.3 | +0.2% |
| sqrt(C_F * alpha_s) | 0.350 | 0.929 | 161.8 | -6.5% |
| sqrt(alpha_s) | 0.303 | 0.860 | 149.8 | -13.4% |

The N=7 CG factor (y_t = g_s/sqrt(7)) gives a near-exact match
at the per-mille level, but lacks a clean algebraic derivation
from Cl(3). The N=6 trace identity (y_t = g_s/sqrt(6)) overshoots
by 3.4% in m_t -- within the expected precision of 1-loop running.

## Assessment

**What works:**
1. The Cl(3) trace structure confines y_t to an O(g_s) family
   with candidate CG factors of order 1/sqrt(N)
2. The benchmark m_t = 178.8 GeV is 3.4% above observed --
   consistent with a one-loop / threshold-level constraint
3. The trace construction is parameter-light: it uses only alpha_s
   from the plaquette action and the Cl(3) representation data

**What is uncertain:**
1. The exact CG coefficient (1/sqrt(6) vs 1/sqrt(7)) remains
   unresolved at the level of the retained cubic surface
2. The 3.4% overshoot can be absorbed by 2-loop corrections,
   threshold effects, or a refined Yukawa operator identification
3. The "best" formula may involve mixed contributions from all
   gauge groups at the unified scale, not just g_s

**Status: y_t is CONSTRAINED to a narrow O(g_s) family, but the exact
CG coefficient remains open.**

This records the constraint chain:
- alpha_s from the plaquette action (0.092)
- y_t benchmark from the Cl(3) trace identity (g_s/sqrt(6) = 0.439)
- competing coefficients bracket the target, but none are uniquely fixed
- m_t from RG running (178.8 GeV benchmark, 3.4% high)

## Script

`scripts/frontier_yt_from_alpha_s.py` -- self-contained, numpy + scipy only.
