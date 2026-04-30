# Alpha_s Direct Wilson-Loop Phase 2 Production Blocker Report

**Date:** 2026-04-30
**Branch:** `claude/alpha-s-direct-wilson-loop-2026-04-30`
**PR:** #227
**Status:** production evidence not complete; strict certificate not issued

## Summary

The requested Phase 2 production measurement was not completed. The existing
repository infrastructure is a pure-Python small-volume Metropolis SU(3)
Wilson-code path, not a production Cabibbo-Marinari heat-bath / overrelaxation
engine. It is adequate for scout-mode and qualitative plaquette/Wilson-loop
checks, but it is not adequate for the requested 12^3 x 24, 16^3 x 32, and
24^3 x 48 production campaign inside this session.

No production alpha_s(M_Z) certificate was generated.
No alpha_s(M_Z)=0.1181 measurement is claimed.
The strict runner should remain blocked until a real production certificate
exists.

## Infrastructure Found

Reusable code paths:

- `scripts/frontier_alpha_s_direct_wilson_loop.py`: strict certificate gate
  plus tiny scout-mode Metropolis Wilson-loop smoke test.
- `scripts/frontier_plaquette_self_consistency.py`: small-volume pure-gauge
  SU(3) Metropolis plaquette evaluator.
- `scripts/frontier_g_bare_critical_feature_scan.py`: array-backed
  rectangular-lattice SU(3) Metropolis implementation.
- `scripts/frontier_confinement_string_tension.py`: small `4^4`
  qualitative Wilson-loop / area-law check.

The existing code does not include a production SU(3) heat-bath implementation,
APE/HYP smearing infrastructure, autocorrelation analysis, or a production
static-potential analysis pipeline.

## Benchmark

Command executed:

```bash
python3 - <<'PY'
import time
import numpy as np
from scripts.frontier_g_bare_critical_feature_scan import init_cold_links, metropolis_sweep
L,Lt=12,24
shape=(L,L,L,Lt)
U=init_cold_links(L,Lt)
rng=np.random.default_rng(20260430)
t0=time.time()
acc=metropolis_sweep(U,6.0,rng,shape)
dt=time.time()-t0
links=L*L*L*Lt*4
print(f"{L}^3x{Lt}: {dt:.3f}s/sweep, links={links}, {dt/links*1e6:.2f} us/link, acc={acc:.3f}")
for L,Lt in [(12,24),(16,32),(24,48)]:
    links=L*L*L*Lt*4
    est=dt/(12*12*12*24*4)*links
    sweeps=1000+1000*20
    print(f"estimate {L}^3x{Lt}: {est:.1f}s/sweep; {sweeps} sweeps={est*sweeps/86400:.1f} days")
PY
```

Output:

```text
12^3x24: 14.181s/sweep, links=165888, 85.49 us/link, acc=0.152
estimate 12^3x24: 14.2s/sweep; 21000 sweeps=3.4 days
estimate 16^3x32: 44.8s/sweep; 21000 sweeps=10.9 days
estimate 24^3x48: 226.9s/sweep; 21000 sweeps=55.1 days
```

The requested 21000 sweeps per volume are:

```text
1000 thermalization sweeps + 1000 measurements * 20 separated sweeps.
```

Estimated sweep-only wall time:

```text
12^3 x 24:  3.4 days
16^3 x 32: 10.9 days
24^3 x 48: 55.1 days
Total:      69.4 days
```

This estimate excludes measurement overhead. Measuring all rectangular loops
`R,T in {1,...,8}` over all origins and spatial orientations every saved
configuration would add substantial runtime.

## Audit Consequence

The direct Wilson-loop alpha_s derivation remains a proposed-retained
measurement route with missing production evidence. The correct current strict
runner result is still:

```text
STRICT GATE BLOCKED
missing production Wilson-loop/static-potential certificate
```

## Honest Completion Requirements

To complete Phase 2 without fabrication, the project needs one of:

1. a production SU(3) heat-bath / overrelaxation implementation, preferably
   vectorized or compiled, plus APE/HYP smearing and jackknife/bootstrap
   analysis;
2. access to an external lattice-QCD production code path with the same
   Cl(3)/Z^3 Wilson-surface inputs and auditable output schema;
3. a reduced-scope audit-approved production protocol that explicitly weakens
   the volume/statistics requirements.

Until then, no strict certificate should be committed.
