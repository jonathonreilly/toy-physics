# PMNS Anomaly-Forced 3+1 Retarded Transport / Projection Boundary

**Date:** 2026-04-16  
**Script:** `scripts/frontier_pmns_anomaly_forced_3plus1_retarded_transport_projection_boundary.py`

## Question

Can an anomaly-forced `3+1` retarded lift on the retained `hw=1` lepton
triplet generate a genuinely nontrivial source/transfer pack after projection
back to the retained triplet?

## Answer

No on the current exact bank.

The route is nontrivial upstairs:

- the finite-lag `3+1` retarded history is not the free identity history
- the anomaly-odd source sector produces distinct lifted time slices
- the retarded lift is therefore a real candidate family, not a tautology

But the retained `hw=1` projection kills the anomaly-odd sector exactly:

- the `C3`-even projection of the lifted history is the free triplet `I3`
- the derived active source columns collapse to the basis columns `e1,e2,e3`
- the derived passive source columns collapse to a scalar multiple of the basis
  columns
- the projected active and passive blocks are both exactly `I3`

So the anomaly-forced `3+1` route does not select a nontrivial retained
source/transfer pack.

## Exact Content

Let `A0 = diag(1,-1,0)` and let the lifted history be the finite-lag
retarded accumulation of the orbit-shifted anomaly seed.

The theorem proves:

1. the lifted `3+1` history is genuinely nontrivial for nonzero anomaly
   strength
2. distinct anomaly strengths give distinct lifted histories upstairs
3. all such histories project to the same retained `hw=1` free pack
4. the retained PMNS closure stack rejects that projected pack

So this candidate family is a theorem-grade boundary, not a positive
closure law.

## Consequence

The remaining blocker is not a missing retarded lift or missing projection
machinery. It is a genuinely new dynamical law that survives the retained
projection and selects a nontrivial `hw=1` source/transfer pack.

## Verification

```bash
python3 scripts/frontier_pmns_anomaly_forced_3plus1_retarded_transport_projection_boundary.py
```
