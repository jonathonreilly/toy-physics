# PR Backlog

The block is being added to PR #230 because the user requested the routes be
combined into that draft PR rather than split into separate physics-loop PRs.

Suggested PR body update:

```text
Adds a Ward physical-readout repair block:
- global YT proof inventory: no hidden retained y_t proof found;
- Ward repair audit: old Ward route remains open at source/HS, chirality,
  scalar-carrier, LSZ, and dressing bridges;
- operator-matching candidate: independent tree-level normalizations meet at
  1/sqrt(6), but this is conditional support, not retained closure.

PR #230 remains draft.  Next block attacks the source-to-Higgs Legendre/SSB
bridge.
```

Latest checkpoint text for PR #230:

```text
Adds a scalar-source response harness checkpoint:
- production harness now accepts `--scalar-source-shifts` and emits
  `scalar_source_response_analysis`;
- reduced smoke validator passes `PASS=8 FAIL=0`;
- campaign status now consumes 33 route certificates and reports
  `PASS=29 FAIL=0`;
- this is bounded support for Feynman-Hellmann `dE/ds`, not physical `dE/dh`;
- `kappa_s = 1` remains forbidden unless derived by scalar LSZ/canonical
  normalization.
```

Latest protocol checkpoint text for PR #230:

```text
Adds a Feynman-Hellmann production protocol certificate:
- common-ensemble symmetric source shifts and correlated `dE_top/ds` fits are
  now specified for the strict PR230 volumes;
- validator passes `PASS=9 FAIL=0`; campaign status now consumes 34 route
  certificates and reports `PASS=30 FAIL=0`;
- the protocol identifies the required `kappa_s` fixer: same-source scalar
  two-point LSZ/canonical-normalization measurement;
- still no retained closure and no physical `dE/dh` without derived `kappa_s`.
```

Latest scalar-LSZ measurement checkpoint text for PR #230:

```text
Adds a same-source scalar two-point LSZ measurement primitive:
- computes `C_ss(q)=Tr[S V_q S V_-q]` and `Gamma_ss(q)=1/C_ss(q)` for the
  same additive scalar source used in `dE_top/ds`;
- validator passes `PASS=8 FAIL=0`; campaign status now consumes 35 route
  certificates and reports `PASS=31 FAIL=0`;
- this identifies the measurement object needed to fix `kappa_s`, but the
  reduced cold primitive has no controlled scalar pole/continuum limit and
  does not authorize physical `dE/dh` or retained closure.
```

Latest scalar Bethe-Salpeter residue checkpoint text for PR #230:

```text
Adds a scalar Bethe-Salpeter kernel/residue degeneracy certificate:
- preserves all currently measured same-source `Gamma_ss(q)` finite-mode
  values and a granted scalar pole while moving `dGamma/dp^2` at the pole;
- validator passes `PASS=6 FAIL=0`; campaign status now consumes 36 route
  certificates and reports `PASS=32 FAIL=0`;
- natural `1/N_c^2` denominator remainders at `N_c=3` move the `kappa_s`
  proxy without changing the finite samples;
- still no retained closure: the interacting denominator, finite-volume/IR
  limit, and pole-residue derivative remain open.
```

Latest scalar two-point harness checkpoint text for PR #230:

```text
Adds a scalar two-point production-harness extension:
- `yt_direct_lattice_correlator_production.py` now accepts
  `--scalar-two-point-modes` and `--scalar-two-point-noises`;
- smoke output emits stochastic estimates of same-source `C_ss(q)` and
  `Gamma_ss(q)` plus a finite-difference residue proxy;
- validator passes `PASS=9 FAIL=0`; campaign status now consumes 37 route
  certificates and reports `PASS=33 FAIL=0`;
- this is production-facing support for the `kappa_s` measurement, not
  retained closure; production data, controlled pole/IR limits, and canonical
  Higgs normalization remain open.
```

Latest joint FH/LSZ harness checkpoint text for PR #230:

```text
Adds a joint Feynman-Hellmann / scalar-LSZ harness certificate:
- one reduced smoke run now emits both `dE_top/ds` and same-source
  `C_ss(q)`/`Gamma_ss(q)`;
- validator passes `PASS=10 FAIL=0`; campaign status now consumes 38 route
  certificates and reports `PASS=34 FAIL=0`;
- this defines the exact production observable bundle for the physical-response
  route;
- still no retained closure: production statistics, controlled scalar-pole
  isolation, `dGamma/dp^2`, and canonical-Higgs `kappa_s` remain open.
```

Latest joint FH/LSZ resource checkpoint text for PR #230:

```text
Adds a joint Feynman-Hellmann / scalar-LSZ resource projection:
- modest scalar-LSZ plan: 4 momentum modes and 16 noise vectors/configuration;
- projected solve budget is `15.8889x` the existing three-mass direct
  projection;
- validator passes `PASS=7 FAIL=0`; campaign status now consumes 39 route
  certificates and reports `PASS=35 FAIL=0`;
- projected mass-scaled foreground cost is about `3630` single-worker hours,
  so this is exact next-action planning, not retained closure.
```

Latest FH/LSZ invariant-readout checkpoint text for PR #230:

```text
Adds a Feynman-Hellmann / scalar-LSZ invariant readout theorem:
- proves the same-source formula
  `y_proxy=(dE_top/ds)*sqrt(dGamma_ss/dp^2 at pole)=dE_top/ds/sqrt(Res[C_ss])`;
- validator passes `PASS=7 FAIL=0`; campaign status now consumes 40 route
  certificates and reports `PASS=36 FAIL=0`;
- this removes the need for any `kappa_s = 1` shortcut: `kappa_s` is measured
  by the same-source pole overlap;
- still no retained closure because production response, isolated pole,
  pole derivative, and canonical-Higgs matching remain open.
```

Latest scalar pole determinant-gate checkpoint text for PR #230:

```text
Adds a scalar pole determinant gate:
- isolates the denominator condition `D(x)=1-K(x)Pi(x)` and pole condition
  `D(x_pole)=0`;
- shows pole location fixes `K(x_pole)` but not `K'(x_pole)`, which controls
  the LSZ residue through `D'(x_pole)`;
- validator passes `PASS=7 FAIL=0`; campaign status now consumes 41 route
  certificates and reports `PASS=37 FAIL=0`;
- still no retained closure: interacting `K(x)`, finite-volume/IR control, or
  production pole-derivative data remain open.
```

Latest scalar ladder eigen-derivative checkpoint text for PR #230:

```text
Adds a scalar ladder eigen-derivative gate:
- matrix Bethe-Salpeter pole condition `lambda_max=1` is only a crossing
  witness;
- holding the crossing fixed while varying `dK/dp^2` moves
  `d lambda_max/dp^2`, the LSZ residue proxy, and the FH/LSZ readout factor;
- validator passes `PASS=7 FAIL=0`; campaign status now consumes 42 route
  certificates and reports `PASS=38 FAIL=0`;
- still no retained closure: total-momentum kernel derivative or production
  pole-derivative data remain open.
```

Latest scalar ladder total-momentum derivative checkpoint text for PR #230:

```text
Adds a scalar ladder total-momentum derivative scout:
- computes finite-difference `d lambda_max/dp^2` in a Wilson-exchange scalar
  ladder by shifting the fermion bubble with total momentum;
- validator passes `PASS=9 FAIL=0`; campaign status now consumes 43 route
  certificates and reports `PASS=39 FAIL=0`;
- derivative is finite and negative on the 108-point scan, but its magnitude
  varies by about `3903.98x` across projector, zero-mode, IR, mass, and volume
  choices;
- still no retained closure: the limiting prescription, scalar pole
  derivative, canonical-Higgs normalization, or production pole data remain
  open.
```

Latest scalar ladder derivative limiting-order checkpoint text for PR #230:

```text
Adds a scalar ladder derivative limiting-order obstruction:
- tests the total-momentum derivative as `mu_IR^2` is lowered with the gauge
  zero mode included versus removed;
- validator passes `PASS=8 FAIL=0`; campaign status now consumes 44 route
  certificates and reports `PASS=40 FAIL=0`;
- included zero mode makes the derivative grow by `13.882x` to `24.0129x`,
  while zero-mode-removed stays within about `1.11x`;
- pole crossing occurs only in the zero-mode-included prescription;
- still no retained closure: the zero-mode/IR limiting theorem or production
  pole derivative remains load-bearing.
```
