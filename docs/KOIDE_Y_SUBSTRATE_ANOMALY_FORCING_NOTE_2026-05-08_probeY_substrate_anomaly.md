# Probe Y-Substrate-Anomaly: Bounded Anomaly-Forcing Boundary

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/cl3_koide_y_substrate_anomaly_2026_05_08_probeY_substrate_anomaly.py`](../scripts/cl3_koide_y_substrate_anomaly_2026_05_08_probeY_substrate_anomaly.py)
**Cache:** [`logs/runner-cache/cl3_koide_y_substrate_anomaly_2026_05_08_probeY_substrate_anomaly.txt`](../logs/runner-cache/cl3_koide_y_substrate_anomaly_2026_05_08_probeY_substrate_anomaly.txt)

## Claim

This note tests a bounded substrate-to-carrier route: whether gauge
anomaly cancellation by itself forces the Standard Model carrier-sector
choices `N_c=3`, `n_gen=3`, the left-handed matter partition, absolute
hypercharge normalization, or the BAE operator-coefficient condition.

**Bounded theorem.** Perturbative `SU(N_c)^2 U(1)`, `SU(2)^2 U(1)`,
gravitational-`U(1)`, and `U(1)^3` anomaly cancellation, together with
the SU(2) Witten parity constraint, does not by itself select the full
Standard Model carrier sector.

More precisely:

1. The usual one-generation anomaly equations have exact rational
   solutions for every odd `N_c >= 3`:

   ```text
   Y(Q_L) = 1/N_c,     Y(L_L) = -1,
   Y(u_R^c) = -(1 + 1/N_c),
   Y(d_R^c) =  (1 - 1/N_c),
   Y(e_R^c) = 2,       Y(nu_R^c) = 0.
   ```

   The perturbative traces vanish for all `N_c >= 2`, while Witten
   parity restricts the chiral `SU(2)` doublet count to even
   `N_c + 1`, hence odd `N_c`. This still does not select `N_c=3`.

2. If one anomaly-free generation is present, any positive generation
   count remains anomaly-free when `N_c` is odd. Anomaly cancellation is
   additive in generations and does not select `n_gen=3`.

3. Vectorlike additions are anomaly-free by construction, so anomaly
   cancellation alone does not uniquely select the left-handed matter
   partition.

4. Hypercharge anomalies are homogeneous in the hypercharge labels.
   Multiplying every hypercharge by a nonzero rational scale preserves
   all zero anomaly traces, so anomaly cancellation fixes at most
   ratios, not the absolute normalization.

5. The BAE condition is an operator-coefficient ratio in a circulant
   flavor operator. Gauge anomaly traces are representation-label
   constraints. No map from the anomaly labels tested here to that
   operator coefficient ratio is supplied.

The result is negative and bounded: it rules out this anomaly-only route
as a derivation of the listed carrier choices. It does not modify or
promote any existing positive anomaly theorem.

## Imports

Bounded mathematical inputs:

- standard perturbative anomaly trace bookkeeping for chiral Weyl
  fermions;
- standard `SU(2)` Witten parity condition that the number of
  left-handed `SU(2)` doublets is even;
- rational arithmetic.

These are standard mathematical/field-theory inputs for this bounded
calculation. They are not new repo-wide axioms and do not alter the
physical Cl(3) local algebra plus Z^3 spatial substrate baseline.

Context only, not load-bearing dependencies:

- `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` is the substrate-side route that
  may select color rank; this note says anomaly cancellation does not.
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` is the substrate-side
  route that may select three generations; this note says anomaly
  cancellation does not.
- Existing hypercharge and anomaly-completion notes remain separate
  positive rows. This note does not strengthen their status.

## Boundaries

This note does not:

- derive Standard Model carrier content;
- claim that anomaly cancellation is useless;
- close the substrate-to-carrier hidden-character bundle;
- assert retained or audited status;
- add any new axiom or physics primitive;
- use PDG values, lattice Monte Carlo values, or fitted constants.

The corrected Witten-parity boundary is important: the anomaly system is
not open to all `N_c >= 2`; it permits the odd-color family and therefore
still does not uniquely force `N_c=3`.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/cl3_koide_y_substrate_anomaly_2026_05_08_probeY_substrate_anomaly.py
```

Expected result:

```text
TOTAL: PASS=39 FAIL=0
```
