# QCD Low-Energy Running Bridge: `alpha_s(v) -> alpha_s(M_Z)` Standard-Infrastructure Note

**Date:** 2026-05-01
**Status:** bounded - bounded-scope same-surface running bridge using standard SM infrastructure (Machacek-Vaughn 2-loop RGE plus quark-mass threshold matching). Not framework-native; scoped explicitly to acknowledge external physics inputs.
**Primary runner:** `scripts/frontier_qcd_low_energy_running_bridge.py`

## Why this note exists

The audit ledger correctly flagged that the downstream
`alpha_s_derived_note` implicitly invokes a running bridge from the
framework scale `v` down to `M_Z` without registering that bridge as a
one-hop authority. The Codex audit verdict on `alpha_s_derived_note`
(2026-04-29) read:

> Issue: the restricted inputs do not include the retained low-energy running
> bridge needed to turn alpha_s(v) into alpha_s(M_Z) ...
> Repair target: cite and audit the running-bridge theorem/threshold map and
> close or explicitly scope the plaquette beta=6 insertion status.

This note registers the bridge explicitly. The bridge itself is not a
framework-native theorem; it is the standard QCD running of the strong
coupling, which the framework reuses as standard infrastructure on the same
footing as PDG quark-mass thresholds and the standard MSbar 2-loop SM RGE
beta functions. The author tier is therefore `bounded`, not
`proposed_retained`.

## Claim

On a same-surface initial condition

```text
alpha_s(v) = alpha_bare / u_0^2 = 0.1033        (framework input)
v          = 246.282818290129 GeV               (framework hierarchy theorem)
```

the standard SM 2-loop renormalization-group running of the
`(g_1, g_2, g_3, y_t, lambda)` system from `mu = v` down to `mu = M_Z = 91.1876 GeV`,
with quark-mass threshold matching at `m_t`, `m_b`, `m_c`, gives

```text
alpha_s(M_Z) = 0.1181 +/- 0.0009              (PDG one-sigma envelope)
```

reproducing the PDG 2025 world-average central value
`alpha_s(M_Z) = 0.1180 +/- 0.0009` within stated uncertainty.

This note treats that bridge as a numerical transfer of a same-surface
running observable, not as a derivation of `alpha_s(M_Z)` from first
principles. It is bounded by:

1. the truncation order of the SM RGE (2-loop here; 4-loop QCD is the PDG
   reference);
2. the chosen quark-mass thresholds (`m_t = 172.69 GeV` pole,
   `m_b = 4.18 GeV` MSbar, `m_c = 1.27 GeV` MSbar);
3. the assumed boundary value `alpha_s(v)` from the plaquette/u_0 chain.

Each of those inputs is documented and held fixed; the bridge is not
adjusted to fit `alpha_s(M_Z)`.

## Bounded-scope statement

This note **does not** claim:

- a framework-native derivation of the QCD beta function;
- a framework-native derivation of the quark-mass thresholds `m_t`, `m_b`,
  `m_c` (these are imported from PDG as standard infrastructure);
- a framework-native derivation of `M_Z` (also PDG-imported);
- audit-clean closure of `alpha_s(M_Z) = 0.1181` independent of the upstream
  plaquette dependency;
- precision better than the 2-loop SM RGE truncation envelope.

This note **does** claim, on the bounded same-surface running scope:

- the existing `frontier_yt_zero_import_chain.py` 2-loop RGE block is the
  standard Machacek-Vaughn (1984) / Arason et al. (1992) two-loop SM RGE
  with explicit threshold matching;
- when fed the framework boundary values
  `(g_1(v), g_2(v), g_3(v), y_t(v), lambda(v))`, the run from `v` to
  `M_Z` reproduces `alpha_s(M_Z) = 0.1181` to within the runner's
  `2%`-of-observed tolerance;
- the bridge is independent of the analytic `beta = 6` insertion status of
  the upstream plaquette (any plaquette evaluation that gives a fixed
  `alpha_s(v)` propagates the same way).

## Standard infrastructure references

The bridge uses only published, peer-reviewed SM RGE infrastructure:

- M. E. Machacek and M. T. Vaughn, "Two-loop renormalization group
  equations in a general quantum field theory," Nucl. Phys. B 222, 83
  (1983); B 236, 221 (1984); B 249, 70 (1985).
- H. Arason, D. J. Castano, B. Kesthelyi, S. Mikaelian, E. J. Piard,
  P. Ramond, B. D. Wright, "Renormalization-group study of the standard
  model and its extensions: The standard model," Phys. Rev. D 46, 3945
  (1992).
- PDG 2025 Review of Particle Physics, "Quantum Chromodynamics" review
  (Section 9.4) — `alpha_s(M_Z) = 0.1180 +/- 0.0009`; restricted average
  `0.1179 +/- 0.0008`.
- C. R. Sturm, Y. Schroder, K. G. Chetyrkin, M. Steinhauser, "MS-bar
  bottom mass from large-N_c expansion of the propagator,"
  Nucl. Phys. B 535, 3 (1998), and follow-up four-loop QCD beta-function
  references.

## Why a `bounded` author tier is the honest choice

The audit ledger separates `proposed_retained` (author claims a
first-principles framework-native derivation) from `bounded` (author
acknowledges the result is conditional on stated external infrastructure).

Three structural facts force the `bounded` tier here:

1. the SM RGE coefficients are derived from continuum SU(3) x SU(2) x U(1)
   group theory plus three SM generations — the framework reproduces the
   gauge-group structure but does not produce the universal beta-function
   coefficients independently;
2. the quark-mass thresholds `m_t`, `m_b`, `m_c` are PDG numerical inputs;
   the framework has no closed lane producing them as same-surface
   structural quantities;
3. the truncation order (2-loop vs. 4-loop) is a pragmatic choice and the
   residual is empirical rather than structural.

A `proposed_retained` claim would assert that this bridge is derivable
from `Cl(3)` on `Z^3` axioms alone. That claim is not in scope here. The
honest claim is the narrower one: given standard QCD running infrastructure
plus the framework's `alpha_s(v)`, the v -> M_Z transfer is consistent with
the PDG world average within the 2-loop truncation envelope.

## Verification surface

The runner `scripts/frontier_qcd_low_energy_running_bridge.py` checks:

1. **Beta-function structural sanity.** The 1-loop gauge beta-function
   coefficient
   `b_3 = -(11 - 2 n_f / 3)` matches the expected QCD UV asymptotic-freedom
   coefficient at `n_f = 5`: `b_3 = -23/3`.
2. **Threshold matching identity.** For each threshold transition
   (`m_t: 6 -> 5 quarks`, `m_b: 5 -> 4`, `m_c: 4 -> 3`), the matched
   coupling is continuous (no jump) at leading order, with the threshold
   discontinuity entering only at NLO.
3. **One-decade transfer reproduction.** Starting from the same-surface
   boundary
   `alpha_s(v) = 0.1033` at `v = 246.28 GeV`, the 2-loop SM RGE running
   downward to `M_Z = 91.1876 GeV` with the threshold map above gives
   `alpha_s(M_Z) ≈ 0.1181`, within 2% of the PDG world average.
4. **Bridge independence from plaquette analytic insertion.** A varied
   `alpha_s(v)` (representing different evaluations of the upstream
   plaquette) propagates monotonically through the bridge without
   changing the bridge's structural form. This isolates the bridge from
   the plaquette-side insertion gap.
5. **Truncation envelope.** A 1-loop-only re-run gives a different
   `alpha_s(M_Z)` value, and the 1-loop -> 2-loop shift bounds the
   higher-loop residual envelope, which is then conservatively quoted.
6. **Cross-check against PDG one-sigma band.** The final
   `alpha_s(M_Z)` is checked against PDG `0.1180 +/- 0.0009` and against
   the restricted-average `0.1179 +/- 0.0008`.

## Cited authorities (one hop)

- [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
  — provides the boundary `<P> = 0.5934`, hence `alpha_s(v) = 0.1033`.
  This dependency is read as a value transfer (class `B` in the audit
  rubric); the running bridge does not require the analytic `beta = 6`
  insertion to be closed.

The runner reuses the same 2-loop SM RGE block that appears in
`scripts/frontier_yt_zero_import_chain.py`; that runner is referenced by
file path (not by markdown link to a sibling note) to avoid creating a
citation back-edge into a downstream consumer.

The framework boundary inputs (`g_bare^2 = 1`, `Cl(3)` graph-first gauge
surface) are referenced by name only, since the inventory note that
catalogs them (`MINIMAL_AXIOMS_2026-04-11.md`) currently sits at terminal
`audited_conditional` due to a renaming-class load-bearing step in that
inventory; making it a one-hop dep would propagate that conditional
verdict downstream without adding any new bridge content.

## Explicit non-claims

- This is not an axiomatic derivation of the QCD beta function.
- This is not a same-surface derivation of `M_Z` or the quark-mass
  thresholds.
- This is not a substitute for the direct Wilson-loop alpha_s lane;
  that downstream lane (described in
  `ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md`,
  cited by file path rather than as a one-hop authority) is the
  audit-clean replacement target.

## Reuse rule

Downstream lanes may cite this note as the registered one-hop authority
for the v -> M_Z transfer of `alpha_s` provided they explicitly read the
result as `bounded` (PDG-truncation-envelope), not as a first-principles
derivation. In particular, `ALPHA_S_DERIVED_NOTE.md` is the primary
downstream consumer; that note cites this one as its registered
v -> M_Z bridge so that its quoted `alpha_s(M_Z) = 0.1181` has a
documented one-hop running-bridge dependency.

## Bridge-support progress 2026-05-09 (upstream plaquette boundary)

The 2026-05-05 audit pass on this row recorded the explicit repair
target:

> dependency_not_retained: retain or replace
> docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md with a retained-grade
> boundary authority for alpha_s(v), and separately register the
> imported SM RGE/threshold infrastructure as an explicit bounded
> retained dependency.

A first concrete piece of the upstream plaquette boundary repair
target landed audited_clean on 2026-05-09 in
[`GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md`](GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md).
That delivery is a bounded finite-box computation of the normalized
single-link SU(3) Wilson boundary character coefficients
`rho_(p,q)(6)` for `0 <= p,q <= 4` by two independent methods.

That audited_clean coefficient table does not by itself close either
the upstream analytic `beta = 6` insertion or the SM RGE / threshold
infrastructure imports of this bridge note. The honest read remains:

- this row is correctly carried as `bounded`;
- the load-bearing step is class `(G)` (numerical match at an
  imported `alpha_s(v)`); that classification is not affected by the
  rho_(p,q)(6) audited_clean delivery, which is upstream of the
  plaquette evaluation rather than at the bridge step;
- the SM RGE / quark-mass threshold imports remain explicit
  standard-infrastructure references that this note does not derive;
- effective-status propagation continues to cap this row at
  `audited_conditional` until both the upstream plaquette analytic
  insertion gap is closed and the SM RGE / threshold infrastructure
  is registered with retained-grade audit cover.

This subsection is informational reuse-discipline only; it does not
promote the audit verdict and does not amend the load-bearing step.
