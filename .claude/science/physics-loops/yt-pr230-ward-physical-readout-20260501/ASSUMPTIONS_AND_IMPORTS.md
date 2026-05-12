# Assumptions And Imports

| Item | Role | Current status | Loop disposition |
|---|---|---|---|
| FH/LSZ target-timeseries chunks001-063 full set | complete L12 same-source target-timeseries support | bounded support only; replacement queue empty | refreshed on 2026-05-12 with full-set checkpoint `PASS=9 FAIL=0`; combiner ready=63/63, target-timeseries complete=63/63, target ESS passed with limiting ESS 895.2344666684801, and all chunks preserve `numba_gauge_seed_v1` seed control.  This remains production-processing support only: no `kappa_s`, canonical `O_H`, `C_sH/C_HH`, W/Z response, strict `g2`, scalar-LSZ/FV/IR, retained, or proposed-retained closure |
| Complete additive-top Jacobian rows at chunks001-063 | bounded support for future W/Z subtraction design | bounded support only; complete coarse row packet | refreshed after chunk063 completion; consumes committed chunks001-063 with `complete_chunk_packet=true`, `row_count=63`, fixed seed metadata, selected mass 0.75, and three-mass scan bracket preserved; still not strict per-configuration additive rows, matched covariance, W/Z response, strict `g2`, accepted action, canonical `O_H`, source-Higgs pole rows, or closure evidence |
| Top mass-scan response harness rows | future per-configuration `dE/dm_bare` rows from existing three-mass top scans | bounded support / infrastructure only | block35 adds `top_mass_scan_response_analysis` to the harness with no extra solves and validates a reduced smoke; existing production chunks predate this field.  These rows are not `dE/dh`, `kappa_s`, W/Z response, matched covariance, strict `g2`, or y_t closure evidence |
| Fresh-artifact intake at PR head e7548e1c6 | committed-head reopen guard for current closure packet | open checkpoint; no closure artifact present | refreshed after chunks059-060 package with chunks001-060; checks current committed head only; active chunk061-062 outputs/logs and pending chunk063 are excluded; no retained/proposed-retained wording unless a same-surface canonical `O_H`/source-Higgs pole-row packet or strict W/Z accepted-action physical-response packet exists |
| Two-source taste-radial chunks001-060 package | finite `C_ss/C_sx/C_xx` row packet | bounded support only | chunks059-060 are packaged; ready=60/63, combined_rows_written=false; active chunks061-062 are run-control only and chunk063 remains pending; finite rows remain non-closure until canonical `O_H`, strict source-Higgs pole rows, scalar-LSZ/FV/IR, W/Z, Schur pole, or neutral primitive authority passes |
| Two-source taste-radial chunks001-058 package | finite `C_ss/C_sx/C_xx` row packet | bounded support only | chunks057-058 are packaged; ready=58/63, combined_rows_written=false; active chunks059-060 are run-control only and chunks061-063 remain pending; finite rows remain non-closure until canonical `O_H`, strict source-Higgs pole rows, scalar-LSZ/FV/IR, W/Z, Schur pole, or neutral primitive authority passes |
| Two-source taste-radial chunks001-056 package | finite `C_ss/C_sx/C_xx` row packet | bounded support only | chunks055-056 are packaged; ready=56/63, combined_rows_written=false; active chunks057-058 are run-control only and chunks059-063 remain pending; finite rows remain non-closure until canonical `O_H`, strict source-Higgs pole rows, scalar-LSZ/FV/IR, W/Z, Schur pole, or neutral primitive authority passes |
| `g_bare = 1` canonical surface | substrate input | existing minimal-axiom surface | allowed as substrate input |
| `N_c = 3`, `N_iso = 2` | structural counts | retained/structural in repo | allowed for arithmetic |
| Old Ward `H_unit` matrix-element readout | forbidden shortcut | `audited_renaming` | may be cited only as the failure mode |
| `yt_ward_identity` as `y_t` authority | forbidden shortcut | same audited-renaming class as the old Ward route | may be cited only as failed/forbidden authority |
| Source / HS / Legendre normalization | physical readout bridge | `audited_renaming` via SSB matching note | open import |
| Chirality projection and right-handed selector | trilinear map | `audited_failed` via Class 5 ledger row | open import |
| Physical scalar carrier uniqueness | maps source scalar to Higgs fluctuation | `audited_failed` on current ledger row | open import |
| Scalar LSZ / `Z_phi` external leg | physical vertex normalization | `audited_conditional` | open import |
| `kappa_s = 1` source-to-Higgs normalization | forbidden shortcut unless derived | not fixed by current retained surface | must be derived by scalar LSZ/canonical normalization |
| Scalar projector/source normalization | needed for ladder pole criterion and residue | not fixed by current retained surface | open import |
| Common tadpole/dressing | needed to compare gauge and scalar readouts | not clean after Ward audit | open import |
| Observed `m_t`, observed `y_t` | comparator only | external observation | forbidden as proof input |
| `alpha_LM` / plaquette normalization | prior quantitative bridge | audited non-clean in this lane | forbidden as load-bearing proof input |
| Production MC data | direct-measurement route evidence | not complete | unavailable for closure |
| Completed L12 chunk compute status | quantified same-source FH/LSZ support | bounded support, not closure | allowed as compute/status support only; single-volume finite-shell rows still need scalar-LSZ denominator authority, `O_H`/source-overlap rows, FV/IR, and matching/running |
| Static heavy-quark additive mass | HQET direct route | not derived on current surface | open import |
| Heavy kinetic-action coefficient `c2` | converts `E(p)-E(0)` into a lattice kinetic mass | not derived on current surface | open import |
| Lattice-HQET-to-SM top mass matching | HQET direct route | not derived on current surface | open import |
| Nonzero-momentum production ensembles | kinetic route evidence | scout and reduced cold pilots only | unavailable for closure |
| Feynman-Hellmann scalar-source response data | alternate observable route | synthetic support only | unavailable for closure |
| Additive-top Jacobian rows at chunks001-052 | chunk-level `dE_top/dm_bare` support for future W/Z subtraction design | bounded support only | refreshed from committed package audit; active chunks053-054 excluded; not matched covariance, not W/Z response, not strict `g2`, not canonical `O_H`, not source-Higgs pole rows, and not closure evidence |
| Same-source scalar pole derivative `D'_ss(pole)` | removes source-coordinate normalization with `dE/ds` | sufficiency theorem support only; production pole data absent | open import until postprocess/model-class/FV/IR/Higgs-identity gates pass |
| Genuine source-pole `O_sp` artifact | same-source source-pole normalization inside the `O_H/C_sH/C_HH` contract | exact support | real source-side artifact only; it does not identify `O_sp` with canonical `O_H` and remains support-only until same-surface `O_H` identity/normalization plus `C_spH/C_HH` pole rows pass |
| Clean source-Higgs outside-math route refresh | route selector after `O_sp`, radial-spurion support, FMS action-adoption minimal cut, current fresh-artifact intake, chunks001-060, and finite Schur diagnostics | exact support only | selects same-surface accepted FMS/EW-Higgs action plus canonical `O_H`, then `O_sp`-Higgs pole rows, as cleanest target; forbids using literature/FMS/math-tool names, partial chunks, radial-spurion algebra, finite Schur rows, or active worker logs as proof selectors |
| Source-Higgs cross-correlator `C_sH` and canonical `C_HH` residue | possible source-pole purity observable | open gate; no hidden current authority | open import; requires a canonical-Higgs source operator and cross-correlator implementation, not assumed |
| FMS/action-first source-Higgs artifact route | possible clean route to `O_H/C_sH/C_HH` rows | bounded support only; no current artifact | allowed only after a same-source EW/Higgs action, gauge-invariant `O_H`, canonical pole normalization, and production `C_ss/C_sH/C_HH` rows exist; FMS literature, gauge-invariant-composite language, and action names are not proof selectors |
| FMS action-adoption minimal cut | strict root cut for adopting the FMS `O_H` packet | exact support only; adoption root open | current support vertices are not action authority; adoption still needs same-surface EW/Higgs action derivation or accepted extension, dynamic `Phi`, canonical `h/v` LSZ metric, canonical `O_H` provenance, no-independent-top-source source derivative, production pole rows, and aggregate gates |
| Post-FMS source-overlap necessity at chunks001-052 | exact boundary after FMS composite support and current two-source row prefix | exact negative boundary | FMS composite support plus source-only LSZ and taste-radial `C_sx/C_xx` rows do not determine `Res C_sH`, source-Higgs Gram purity, or orthogonal-neutral top couplings; reopen requires canonical `O_H` plus production `C_ss/C_sH/C_HH` pole rows with Gram/FV/IR checks, or a strict physical-response bypass |
| Source-Higgs overlap/kappa contract at chunks001-052 | exact formula for the future source-Higgs overlap row object | exact support only | defines `kappa_spH = Res(C_sH)/sqrt(Res(C_ss) Res(C_HH))` once same-pole `O_H/C_sH/C_HH` rows exist; does not set `kappa_s=1` and current FMS/source-only/`C_sx` rows do not supply `Res C_sH` |
| Source-Higgs time-kernel production manifest | future `C_ss/C_sH/C_HH(t)` row command surface | bounded-support infrastructure only | not evidence; launch remains unauthorized until same-surface canonical `O_H` or physical neutral identity exists, and the manifest cannot be used to relabel taste-radial `x` as canonical `O_H` or to infer `kappa_s` |
| Exact tensor/PEPS Schur row production | possible outside-math row engine | exact negative boundary for current PR230 surface | allowed only after a same-surface neutral kernel basis, source/orthogonal projector, `A/B/C` row definitions, contact/FV/IR conventions, and certified contraction are supplied; method name and source-only marginals are not proof inputs |
| Schur A/B/C definition derivation | possible outside-math row-definition route | exact negative boundary for current PR230 surface | allowed only after same-surface Schur A/B/C rows and projectors exist; source-only denominators, Feshbach responses, PSLQ, Picard-Fuchs/D-module, free-probability, and exact-tensor method names are not proof selectors until same-surface Schur A/B/C rows and projectors exist |
| W/Z g2 bare-running bridge | possible non-observed electroweak coupling route | exact negative boundary for current PR230 surface | allowed only after a same-source EW action, scale ratio, thresholds, and finite matching exist; structural bare `g2`, beta-function formulas, PSLQ/value recognition, and convention choices are not proof selectors until same-source EW action, scale ratio, thresholds, and finite matching exist |
| Hardened same-source EW action certificate builder/gate | W/Z route acceptance firewall | exact negative boundary for current PR230 surface | requires the W/Z response-ratio identifiability contract, one no-independent-top-source radial spurion controlling top/W/Z responses, and rejection of the current additive top source as an accepted EW/Higgs action; support-only, not W/Z rows or closure authority |
| W/Z same-source accepted-action minimal certificate cut | executable dependency cut for the W/Z fallback | exact negative boundary; root cut open | conditional action/radial/ratio contracts are not action authority; accepted action still requires canonical O_H, current sector-overlap/adopted radial-spurion authority, and production W/Z mass-fit path roots before W/Z rows, covariance, and strict g2 can matter |
| W/Z route completion with physical-response intake | fallback physical-response route after source-Higgs | exact negative boundary | current route is exhausted, not closed as physics; no accepted action, production W/Z rows, same-source top rows, matched covariance, strict non-observed `g2`, `delta_perp` authority, or final response packet exists |
| Neutral primitive route completion with H3/H4 aperture intake | primitive-cone / irreducibility fallback route | exact negative boundary | route-completion gate now consumes the H3/H4 aperture directly; H1/H2 Z3 support and chunks001-060 `C_sx/C_xx` rows remain bounded support only and do not supply H3 physical neutral transfer, H3 primitive-cone/irreducibility authority, or H4 source/canonical-Higgs coupling |
| Canonical O_H / W/Z common root cut | shared source-Higgs and W/Z action-root checkpoint | exact support plus boundary; root open | common cut, accepted-action stretch, and W/Z response-root checkpoint are support-only gate wiring; they do not supply canonical O_H, accepted EW/Higgs action, C_sH/C_HH rows, W/Z rows, covariance, or strict g2 |
| GNS/source-Higgs flat extension | possible moment-rank purity certificate | exact negative boundary for source-only current surface | allowed only after same-surface `O_H/C_sH/C_HH` pole rows define the full PSD moment matrix; source-only `C_ss` projections and GNS rank labels are not proof selectors until O_H/C_sH/C_HH rows exist |
| Burnside/double-commutant neutral irreducibility | possible outside-math primitive-cone certificate | exact negative boundary for current source-only generator surface | allowed only after a same-surface off-diagonal neutral generator, primitive transfer matrix, or equivalent source/orthogonal row is supplied; theorem names and source-only block-diagonal algebras are not proof selectors until a same-surface off-diagonal neutral generator or primitive transfer exists |
| Carleman/Tauberian scalar-LSZ determinacy | possible outside-math moment/asymptotic certificate | exact negative boundary for finite current scalar rows | allowed only after an infinite same-surface moment/asymptotic certificate exists with contact, threshold, FV/IR, and pole-residue authority; finite moment prefixes, finite shell rows, and theorem names are not proof selectors until an infinite same-surface moment/asymptotic certificate exists |
| Complete-Bernstein inverse-propagator diagnostic | necessary test for a scalar inverse denominator from a positive Stieltjes propagator | exact negative boundary for current polefit8x8 inverse proxy | not proof selectors until a certified scalar denominator object passes the inverse tests; the current positive `Gamma_ss` proxy decreases with `q_hat^2`, so it is not complete-Bernstein denominator authority |
| Schur-complement complete-monotonicity/threshold gate | stricter scalar-LSZ test on the Schur `C_x|s` residual | bounded support plus exact boundary | first-shell `C_x|s` support is not strict scalar-LSZ authority; first-shell C_x|s support is not strict scalar-LSZ authority; complete monotonicity needs higher ordered momentum shells or an analytic moment theorem, plus threshold, pole, FV/IR, and canonical-source bridge authority |
| Neutral primitive H3/H4 aperture at chunks001-060 | neutral primitive/rank-one route freshness guard | bounded support plus exact boundary | dynamic row-prefix guard now consumes ready=60/63; H1/H2 Z3 support and finite `C_sx/C_xx` rows do not supply H3 physical neutral transfer/off-diagonal generator authority or H4 source/canonical-Higgs coupling |
| Degree-one radial-tangent O_H theorem | exact action-first axis selector under a linear same-surface radial-tangent premise | exact support only | action/LSZ premise and pole rows absent; it selects `(S0+S1+S2)/sqrt(3)` only if a future EW/Higgs action derives canonical `O_H` as a degree-one Z3-covariant tangent, and it does not identify the current taste-radial source with canonical `O_H` |
| Taste-radial-to-source-Higgs promotion contract | exact relabeling firewall for finite `C_sx/C_xx` rows | exact support only | current promotion blocked by absent canonical O_H identity/action/LSZ premise; `C_sx/C_xx` may become `C_sH/C_HH` only after same-surface `x=canonical O_H`, canonical LSZ, pole/FV/IR, and Gram-purity authority pass |
| Two-source taste-radial chunks001-054 package | finite `C_ss/C_sx/C_xx` row packet | bounded support only | chunks053-054 are packaged; ready=54/63, combined_rows_written=false; chunks055-056 were active run-control only and chunks057-063 remained pending at that checkpoint; finite rows remain non-closure until canonical `O_H`, strict source-Higgs pole rows, scalar-LSZ/FV/IR, W/Z, Schur pole, or neutral primitive authority passes |
| Two-source taste-radial chunks001-052 package | finite `C_ss/C_sx/C_xx` row packet | bounded support only | chunks051-052 are packaged; ready=52/63, combined_rows_written=false; active chunks053-054 are run-control only and chunks055-063 remain pending; finite rows remain non-closure until canonical `O_H`, strict source-Higgs pole rows, scalar-LSZ/FV/IR, W/Z, Schur pole, or neutral primitive authority passes |
| Two-source taste-radial chunks001-050 package | finite `C_ss/C_sx/C_xx` row packet | bounded support only | chunks047-050 are packaged; ready=50/63, combined_rows_written=false; active chunks051-052 were run-control only at that checkpoint; finite rows remain non-closure until canonical `O_H`, strict source-Higgs pole rows, scalar-LSZ/FV/IR, W/Z, Schur pole, or neutral primitive authority passes |
| Two-source taste-radial chunks001-032 package | finite `C_ss/C_sx/C_xx` row packet | bounded support only | chunks031-032 are packaged; ready=32/63, combined_rows_written=false; active chunks033-034 are run-control only; finite rows remain non-closure until canonical `O_H`, strict source-Higgs pole rows, scalar-LSZ/FV/IR, W/Z, Schur pole, or neutral primitive authority passes |
| Single finite source-shift radius as a zero-source derivative | possible FH shortcut | exact negative boundary for PR230 FH response closure | allowed as diagnostic support only; one finite radius does not exclude odd nonlinear response |
| Reduced mass-bracket `dE/dm_bare` response | lightweight response scout | bounded support | bare-source data; forbidden as physical `y_t` evidence |
| Reduced cold-gauge momentum pilots | implementation support | bounded support | forbidden as strict evidence |
| Scalar-channel contact coupling `G` | HS/RPA pole condition | not in `A_min` | forbidden unless derived from Wilson gauge ladder |
| Scalar-channel Bethe-Salpeter kernel | interacting pole route | not yet retained | open import after ladder scout |
| IR / finite-volume kernel limit | needed for ladder eigenvalue crossing | not yet fixed | open import |
| Reflection positivity / OS reconstruction | possible scalar spectral shortcut | exact negative boundary for PR230 LSZ closure | allowed as positivity support only; does not derive pole saturation, source residue, or canonical-Higgs identity |
| Short-distance/OPE source normalization | possible scalar LSZ shortcut | exact negative boundary for PR230 LSZ closure | allowed as UV/operator support only; finite OPE coefficients do not derive the IR source-pole residue or canonical-Higgs identity |
| Finite effective-mass plateau amplitude | possible scalar LSZ postprocess shortcut | exact negative boundary for PR230 LSZ closure | allowed as diagnostic support only; finite time-window plateaus do not identify the same-source pole residue |
| Effective-potential Hessian / radial curvature | possible canonical-Higgs identity shortcut | exact negative boundary for PR230 source-overlap closure | allowed as canonical-field support only; does not derive the source operator direction |
| BRST/ST/Nielsen gauge identities | possible canonical-Higgs identity shortcut | exact negative boundary for PR230 source-pole identity closure | allowed as gauge-consistency support only; does not derive neutral scalar source direction or source-pole purity |
| Cl(3)/Z3 finite automorphism/orbit data | possible substrate source selector | exact negative boundary for PR230 source-Higgs identity closure | allowed as structural support only; does not derive continuous LSZ overlap, `D'(pole)`, or pole residue |
| Full-staggered PT formula layer | supplies `D_psi`, `D_gluon`, scalar/gauge kinematics | exact support only | formulas reusable; old alpha/plaquette/H_unit surfaces forbidden |
| EW/Higgs canonical doublet notes | structural guardrails | proposed/unaudited or conditional parents | may not be used as PR230 source-normalization closure |
| FMS / gauge-invariant-field literature | source-Higgs bridge context | non-derivation context only; intake runner blocks current use as proof authority | may motivate future `O_FMS` acceptance contract only after same-surface EW/Higgs action, canonical LSZ, and `C_spH/C_HH` pole rows exist; cannot set `kappa_s` or identify `O_sp`/taste-radial `x` with canonical `O_H` |

Minimal allowed premise set for the current stretch attempt:

```text
A_min = retained action/substrate + structural counts + standard functional
derivative definitions, but no H_unit matrix-element definition, no observed
top mass/Yukawa, no fitted selector, and no alpha_LM/plaquette bridge as proof.
```

New obstruction from the scalar ladder projector check:

```text
lambda_max[c O] / lambda_max[O] = c^2
lambda_max[F_ps] / lambda_max[F_ps/4] = 16
```

Therefore the ladder pole criterion cannot be made load-bearing until the
scalar projector/source normalization and scalar LSZ residue are derived from
the interacting Wilson-staggered scalar two-point function.

Direct-route HQET import boundary:

```text
C_static(t) / C_static(0) = exp(-E_residual t)
```

The static rephasing removes the absolute heavy rest mass from the normalized
correlator.  A heavy/top-integrated direct route still needs an additive-mass
renormalization and lattice-HQET-to-SM matching theorem before it can determine
`m_t` and `y_t`.

The formal static obstruction is:

```text
C(t; am0, E) = A exp[-(am0 + E)t]
C_sub(t; E) = exp(am0 t) C(t; am0, E) = A exp[-Et]
am0 + delta_m = constant
```

The subtracted correlator is invariant under changes in the absolute rest mass;
the residual-mass decomposition is nonunique until a matching condition fixes
the physical sum.

Legendre normalization boundary:

```text
W_k(J) = W(k J)
phi_k = dW_k/dJ = k phi
Gamma_k(phi_k) = Gamma(phi_k/k)
```

The source Legendre transform is exact, but it is covariant under source/field
rescaling.  It does not select `kappa_H = 1` without an additional physical
pole-residue or canonical kinetic normalization condition.

Free scalar two-point boundary:

```text
Pi(p) = sum_k 1 / [(m^2 + D(k))(m^2 + D(k+p))]
Gamma_free^(2)(p) = 1 / Pi(p)
```

On the scanned finite Wilson-staggered source surfaces `Pi(p)` is finite and
`Gamma_free^(2)(p)` has no zero.  The free logdet source curvature therefore
does not supply an isolated Higgs-carrier pole; an interacting denominator or
production measurement is required.

Same-1PI boundary:

```text
Gamma^(4) = y^2 D_phi
y -> kappa y
D_phi -> D_phi / kappa^2
```

A same-four-fermion coefficient can remain fixed while the scalar vertex and
scalar propagator normalization vary.  Same-1PI equality is not enough until
the scalar pole residue/canonical normalization is independently fixed.

Current kinetic-route assumption stress test:

```text
measured Delta E(p) = c2 p_hat^2 / (2 M0)
M_kin(readout) = p_hat^2 / (2 Delta E)       only if c2 = 1
m_t(SM) = Z_match a^{-1} M_kin
```

The nonzero-momentum route removes the static additive rest-mass ambiguity, but
it introduces two explicit imports:

1. `c2`, the heavy kinetic-action coefficient;
2. `Z_match`, the lattice-to-SM mass matching factor.

The current retained surface does not derive either.  Therefore a cold-gauge or
reduced-statistics kinetic-mass proxy cannot be promoted to a physical top mass
or `y_t` theorem.  It is allowed only as implementation support until the
matching theorem or production evidence with independently derived matching is
available.

Feynman-Hellmann source-response route:

```text
dE_top/ds = scalar-source response
h = kappa_s s
dE_top/dh = (dE_top/ds) / kappa_s
```

The response route cancels additive rest-mass shifts in energy slopes, but it
does not fix `kappa_s`.  Therefore it remains blocked by the same scalar
source-to-Higgs normalization / LSZ residue import unless that bridge is
derived or measured on production ensembles.

Finite source-shift derivative boundary:

```text
E(s) = E0 + a s + c s^3
[E(+delta)-E(-delta)]/(2 delta) = a + c delta^2
```

A single finite symmetric source radius fixes the finite-difference slope, not
the zero-source derivative `a = dE/ds|_0`.  Using a single finite source-shift
radius as a zero-source derivative is therefore forbidden as a proof shortcut
until multiple source radii, a finite-source-linearity gate, or a retained
analytic response-bound theorem excludes nonlinear contamination.

Same-source FH/LSZ invariant readout support:

```text
y_proxy = (dE_top/ds) * sqrt(dGamma_ss/dp^2 at pole)
        = (dE_top/ds) / sqrt(Res[C_ss] at pole)
```

This formula is invariant under source/operator rescaling when the response and
two-point function use the same source coordinate.  It does not set
`kappa_s = 1`; it identifies `kappa_s` with the same-source pole overlap.  The
load-bearing open import is now the actual scalar pole, pole derivative, and
canonical-Higgs match.

Scalar pole determinant gate:

```text
C_ss(x) = Pi(x) / D(x)
D(x) = 1 - K(x) Pi(x)
D(x_pole) = 0
D'(x_pole) = -K'(x_pole) Pi(x_pole) - K(x_pole) Pi'(x_pole)
```

The pole location fixes only `K(x_pole)`, not the LSZ residue.  The interacting
kernel derivative `K'(x_pole)` or a direct production pole-derivative
measurement remains load-bearing.

Matrix ladder eigen-derivative gate:

```text
lambda_max(pole) = 1
LSZ residue needs d lambda_max / d p^2 at the crossing
```

A finite eigenvalue crossing is not enough unless the total-momentum
dependence of the scalar Bethe-Salpeter kernel is derived or measured.

Scalar ladder total-momentum derivative scout:

```text
d lambda_max / d p^2 = finite-difference derivative of the
total-momentum-shifted Wilson-exchange ladder eigenvalue
```

The derivative is computable in a finite scout, but the scout leaves the
projector, gauge-zero-mode, IR-regulator, finite-volume, and canonical Higgs
normalization choices open.  The finite negative sign observed in the scan is
not a proof selector; the load-bearing missing input remains the retained
limiting prescription or production pole-derivative measurement.

Scalar ladder derivative limiting-order obstruction:

```text
zero mode included: d lambda_max/dp^2 grows as mu_IR^2 is lowered
zero mode removed:  d lambda_max/dp^2 is comparatively stable on the same scan
```

The zero-mode/IR limiting order is therefore a load-bearing proof input.  A
route that uses the finite derivative as `kappa_s`/LSZ normalization without
deriving that order is importing a hidden prescription.

Scalar ladder residue-envelope obstruction:

```text
g = 1 / lambda_max(0)
residue_proxy = |lambda_max(0) / lambda'_max(0)|
```

Tuning each finite ladder surface to its own pole removes the pole-location
ambiguity, but does not fix scalar LSZ normalization.  The pole-tuned residue
proxy still changes under zero-mode, source-projector, and finite-volume
choices.  Therefore a finite ladder residue envelope cannot be used as
`kappa_s` or a canonical-Higgs LSZ input unless the limiting prescription and
source/projector normalization are derived, or the pole derivative is measured
on production ensembles.

Scalar-kernel Ward-identity obstruction:

```text
D(x_pole) = 0 fixes K(x_pole)
D'(x_pole) still depends on K'(x_pole)
```

Existing Ward/gauge/Feshbach response identities do not derive
`K'(x_pole)` or common scalar/gauge dressing.  A route that uses
`yt_ward_identity`, `H_unit`, or exact Feshbach response preservation as
authority for the scalar LSZ derivative is importing the missing scalar
denominator theorem.

Cl(3)/Z3 source-unit normalization boundary:

```text
D + m + s fixes the source coordinate s and dS/ds
h = kappa_s s still requires a scalar pole/kinetic normalization theorem
```

Unit lattice spacing, unit Clifford generator norms, and `g_bare=1` do not fix
the canonical Higgs field metric.  Setting `kappa_s=1` from the substrate source
unit remains forbidden.

Joint FH/LSZ production manifest boundary:

```text
exact launch commands != production evidence
```

The manifest is allowed as planning support only.  The load-bearing inputs
remain production certificates, correlated response fits, scalar pole
derivative, and finite-volume/IR/zero-mode control.

Retained-closure route refresh:

```text
proposal_allowed = false
```

The refreshed gate includes the current source-unit and production-manifest
blocks.  It remains forbidden to promote PR #230 until that certificate is
changed by production evidence or a new theorem.

Reflection positivity boundary:

```text
M_ij = C(t_i + t_j) >= 0
```

For a positive spectral measure, OS reflection matrices are positive
semidefinite.  This is not enough for the PR #230 scalar LSZ bridge: positive
reflection-positive pole-plus-continuum families can keep the finite
same-source shell values fixed while changing the pole residue.  A route that
uses OS positivity as `kappa_s`, pole saturation, or canonical-Higgs identity
is importing the missing scalar-denominator theorem.

Effective-potential Hessian boundary:

```text
O_s(theta) = cos(theta) h + sin(theta) chi
```

The canonical VEV, W/Z mass algebra, and scalar Hessian eigenvalues can remain
fixed while the source operator direction rotates.  A route that identifies the
PR #230 source with the canonical radial Higgs mode from Hessian curvature
alone is importing the missing source-overlap/source-pole identity.

Scalar zero-mode limit-order boundary:

```text
Delta M_zero-mode = (4/3) w_i / (V mu_IR^2)
```

Retaining the gauge zero mode adds an exact positive diagonal term to the
finite scalar ladder.  Taking `mu_IR -> 0` first, taking volume first, or
box-scaling the regulator selects different scalar denominators.  The
zero-mode/IR/finite-volume prescription is therefore a load-bearing premise,
not a numerical detail.

Zero-mode prescription import audit:

```text
hidden current-surface authorities fixing the prescription = []
```

Perturbative BZ notes use regulator conventions, the continuum-identification
note warns about alternative gauge fixings, and the production manifest
requires finite-volume/IR/zero-mode control.  None can be used as the missing
PR #230 scalar denominator prescription.

Flat toron sector boundary:

```text
constant commuting Cartan links: plaquette action = 0
scalar bubble / inverse denominator proxy changes with Polyakov phase
```

The compact action does not select the trivial toron sector.  A route that
uses the trivial zero mode, removes the zero mode, or averages torons must
derive that prescription before using the scalar denominator as LSZ input.

Flat toron thermodynamic washout support:

```text
fixed physical holonomy phi => link angle theta = phi/N
N^-4 sum_k f(k + phi/N) and N^-4 sum_k f(k) have the same thermodynamic limit
```

For the local massive scalar bubble, the flat-toron finite-volume dependence
washes out because the integrand is smooth and periodic for `m > 0`.  This is
support only.  It does not derive the massless gauge-zero-mode/IR prescription,
interacting pole denominator, or LSZ derivative.

Color-singlet gauge-zero-mode cancellation:

```text
(T_q^a + T_qbar^a)|S> = 0
C_F + C_F - 2 C_F = 0
```

The exact `q=0` gauge mode cancels in a color-neutral scalar `q qbar` singlet
when self and exchange pieces are included together.  This permits a
zero-mode-removed color-singlet scalar kernel as exact support, but does not
derive the finite-`q` IR behavior or the pole derivative.

Color-singlet finite-`q` IR regularity:

```text
d^4q / q^2 ~ q dq near q=0
```

After the exact `q=0` cancellation, the remaining massless gauge kernel is
locally integrable in four dimensions.  This removes the finite-`q` IR
divergence concern but still does not derive the interacting scalar pole or
inverse-propagator derivative.

Zero-mode-removed finite ladder pole-search boundary:

```text
q=0 removed, mu_IR^2 = 0
finite lambda_max >= 1 witnesses exist at small mass
crossings depend on volume parity, taste corners, source projector, and derivative proxy
```

These finite witnesses are not production evidence and not a continuum scalar
pole theorem.  They cannot be used as `kappa_s`, a canonical-Higgs LSZ
normalization, or retained top-Yukawa closure unless the continuum/taste/
projector limit and inverse-propagator derivative are derived or measured.

Taste-corner carrier import:

```text
non-origin sin(p)=0 corners dominate finite ladder crossings
physical-origin-only filtering removes every crossing
```

Any route that treats those non-origin corners as part of the physical scalar
carrier must derive that taste/corner projection from the retained action.  It
cannot be assumed as a proof input.

Current taste-carrier authority audit:

```text
retained authorities admitting non-origin corners as scalar carrier = []
```

Existing taste and staggered-PT surfaces are support/conditional or
renaming-bounded.  They do not derive the PR #230 scalar color/taste/spin
projector or physical scalar carrier.

Taste-singlet normalization boundary:

```text
normalized taste-singlet over 16 BZ corners => lambda_max -> lambda_max / 16
```

Under the normalized singlet source convention, every finite ladder crossing
witness drops below `lambda_max = 1`.  Therefore any scalar-pole route must
derive which taste/projector normalization is physical; it cannot use the
unnormalized 16-corner multiplicity as a hidden proof input.

Scalar taste/projector normalization attempt:

```text
O_singlet = (1/sqrt(16)) sum_t O_t
s O_local = (sqrt(16) s) O_singlet
```

The unit projector algebra is allowed support, but it does not fix the
canonical scalar source coordinate, physical taste carrier, or pole derivative.
Those remain imports unless derived from the source functional plus interacting
LSZ pole, or measured in same-source production data.

Unit-projector pole-threshold boundary:

```text
max lambda_unit = 0.442298920672
min extra kernel multiplier for crossing = 2.26091440260
```

Any route that forces a unit-projector finite pole must derive this additional
scalar-channel enhancement from retained dynamics.  It cannot be fitted or
declared as a hidden normalization.

Scalar-kernel enhancement import audit:

```text
closing_candidates = []
```

HS/RPA, reusable ladder formulae, same-1PI, and Ward/Feshbach response surfaces
do not derive the multiplier required by the unit-projector finite ladder or
the derivative `K'(x_pole)`.

Source-reparametrization gauge boundary:

```text
source-only products are covariant under h = kappa_s s
y^2 D_phi and response identities do not determine kappa_s
```

Any route that sets `kappa_s = 1` without deriving canonical scalar
normalization is importing a hidden normalization.  This includes source
curvature, same-1PI, and Feynman-Hellmann response routes.

Explicit closure attempt result:

```text
allowed current-surface premises fixing kappa_s = []
```

The missing theorem must derive the isolated scalar pole, residue derivative,
and match to canonical Higgs kinetic normalization.

Refreshed `A_min` for the positive-closure rerun:

```text
A_min =
  retained Cl(3)/Z^3 substrate
  + g_bare = 1 as substrate input
  + Wilson-staggered Dirac/gauge action already in PR230 harness
  + standard functional derivative / correlator extraction definitions
  + structural counts N_c=3, N_iso=2

Forbidden in A_min =
  H_unit-to-top matrix-element definition; H_unit matrix-element readout
  yt_ward_identity as y_t authority
  observed top mass / observed y_t as proof selectors
  alpha_LM / plaquette / u0 as load-bearing normalization; alpha_LM / plaquette / u0 as load-bearing proof input
  reduced cold pilots as production evidence, including reduced cold-gauge pilot values
  c2 = 1 unless derived from the action in the same route
  Z_match = 1 unless derived as a matching theorem
  kappa_s = 1 unless derived by scalar LSZ/canonical normalization
```

The FH/LSZ postprocess gate enforces the same firewall for future production
outputs: a manifest, reduced smoke file, partial production output, or finite
residue proxy is not physical `y_t` evidence unless the same-source scalar pole
derivative and FV/IR/zero-mode limit are derived or measured without importing
the forbidden normalizations above.

The fitted-kernel selector check extends the firewall to finite ladder pole
forcing.  A constant `g_eff` chosen only to satisfy
`g_eff * lambda_unit = 1` is a fitted scalar-channel normalization, not a
derived premise.  It is therefore forbidden as a retained proof input unless
the same route derives the momentum-dependent scalar kernel and its pole
derivative.

The production checkpoint-granularity check extends the reduced-pilot firewall:
an interrupted or partial foreground production launch is not production
evidence.  Current `--resume` support loads only completed per-volume artifacts,
so the FH/LSZ route needs chunk-level checkpointing or an external scheduler
that can finish the smallest shard before any production certificate can be
considered.

The chunked-production manifest preserves that boundary.  A foreground-sized
L12 chunk is still only a production-targeted launch command until it completes
and is combined with enough independent chunks by a postprocess certificate.
It cannot be used as a reduced-pilot substitute for production evidence.

The chunk-combiner gate adds a provenance requirement to the same firewall.
Future L12 chunks must record `metadata.run_control` with seed and command
settings, and must pass production-phase same-source FH/LSZ checks before
combination.  Missing, partial, or L12-only chunk sets are forbidden as proof
selectors for physical `y_t`.
The chunk manifest now also requires chunk-local artifact directories, so
reusing or overwriting per-volume artifacts is not an allowed provenance path.
The negative source-shift CLI fix is syntactic only; it does not upgrade a
manifest, partial chunk, or L12-only output into physical `y_t` evidence.
The pole-fit kinematics gate extends that boundary: a finite secant from the
current one nonzero momentum shell is not a scalar pole derivative unless the
route supplies richer kinematics, analytic continuation control, or a retained
theorem.
The eight-mode/eight-noise budget is also not an assumption license.  Lowering
the noise count is a launch-planning trade that requires a variance gate before
it can be used as production-facing pole-fit evidence.
The variance gate keeps that trade closed on the current surface: the reduced
smoke and the running four-mode/x16 chunk cannot be imported as an x8
same-source production variance calibration, and `sqrt(2)` stochastic-error
inflation cannot be waived without a measured calibration or theorem.
The new `noise_subsample_stability` fields are diagnostics only.  They may
support a future paired production calibration, but reduced smoke diagnostics
are still forbidden as proof input for physical `y_t`.
The paired x8/x16 calibration manifest is also not an assumption license: only
completed production-phase calibration outputs with matching run-control
metadata can test the lower-noise route.
The canonical electroweak VEV and gauge-boson masses are not an assumption
license for `kappa_s=1`.  They normalize canonical `h` after it is identified;
they do not identify the Cl(3)/Z3 source coordinate `s` with that field.
The canonical Higgs kinetic renormalization condition is likewise not an
assumption license for `kappa_s=1`.  `Z_h=1` fixes the h-field residue, not the
source operator overlap `<0|O_s|h>`; that overlap must come from same-source
pole residue data or a retained source-overlap theorem.
Source contact counterterms are not an assumption license either.  A
contact-renormalized convention for `C_ss(0)` or `C_ss'(0)` may be useful for a
scheme definition, but it is forbidden as a proof selector for `kappa_s` unless
the isolated same-source pole residue is also derived or measured.

The same-source gauge-normalized response ratio adds one more explicit
forbidden shortcut.  A common source label and common source-coordinate
rescaling do not imply equal sector overlaps:

```text
dE_top/ds = k_top y_t / sqrt(2)
dM_W/ds   = k_gauge g2 / 2
y_readout = y_t (k_top / k_gauge)
```

Setting `k_top/k_gauge = 1` is forbidden unless the same route derives the
canonical-Higgs source identity or measures an equivalent same-source W/Z
physical-response certificate.  Static `v`, observed W/Z masses, and the EW
gauge-mass theorem after canonical `H` is supplied are not proof selectors for
that equality.

A completed same-source pole residue is not by itself an assumption license
for the canonical Higgs identity.  If

```text
|source pole> = cos(theta) |h_canonical> + sin(theta) |chi_orthogonal>
```

then the FH/LSZ source-pole readout is a coupling to the source pole.  It is
physical `y_t` only after `cos(theta)=1` is derived or directly measured, or an
equivalent theorem excludes orthogonal scalar admixture.

Positive-closure candidates left after the assumption exercise:

1. production/statistics with momentum modes plus a derived heavy matching
   bridge;
2. scalar-channel pole/LSZ theorem deriving projector, zero-mode/IR limit,
   eigenvalue crossing, and residue;
3. an independent retained parent repair for the chirality/scalar carrier
   bridge.

2026-05-02 no-orthogonal-top-coupling import audit:

The current Class #3 SUSY/2HDM authority may be used only as support for no
retained fundamental second scalar, no retained 2HDM species split, and D17
one-dimensional `Q_L` scalar-singlet structure.  It must not be promoted into
the stronger LSZ/source-pole premise needed by PR #230.

Still forbidden unless derived or measured on the current surface:

- source pole equals canonical Higgs radial mode;
- no orthogonal response component in the source pole;
- zero top coupling for every orthogonal scalar response component;
- `kappa_s = 1`, `Z_match = 1`, or `c2 = 1`.

2026-05-02 D17 source-pole identity closure attempt:

D17 may be used as carrier/irrep uniqueness support only.  It must not be used
as a source-pole LSZ normalization theorem.  The source operator overlap
`<0|O_s|h>`, source two-point pole residue, inverse-propagator derivative
`D'(pole)`, and canonical-Higgs identity remain open unless separately derived
or measured.  It also must not be treated as a rank-one theorem for the full
neutral scalar response space.

2026-05-02 spectral sum-rule audit:

Finite positive spectral or moment sum rules for `C_ss` may be used as support
or diagnostics only.  They must not be used to infer pole saturation, the
source-pole residue, or the source overlap without a separate microscopic
denominator/threshold theorem or production pole-residue measurement.

2026-05-02 latest Higgs-pole identity blocker:

The consolidated blocker certificate makes these additional shortcut bans
explicit.  Do not set `cos(theta)=1`, do not set the orthogonal scalar top
coupling to zero, and do not equate top-sector and gauge-sector source
overlaps unless the current route derives or measures that identity.  A fixed
same-source pole readout is not physical `y_t` until source-pole purity,
source residue, and `D'(pole)` are independently certified.

2026-05-02 confinement-gap threshold import audit:

Qualitative confinement/mass-gap language is support for broad sector
structure only.  It must not be used as a uniform same-source scalar continuum
threshold, pole-saturation certificate, or pole-residue bound unless a
current-surface scalar denominator theorem supplies that exact bridge.

2026-05-02 same-source W/Z response manifest:

The formula using `(dE_top/ds)/(dM_W/ds)` may be used only as a future
measurement design.  It must not be treated as evidence without a real W/Z
mass-response harness, correlated production slopes, retained electroweak
coupling normalization, and same-source sector-overlap / Higgs-pole identity
certificates.  Observed W/Z masses remain forbidden proof selectors.

2026-05-02 same-source W/Z response certificate gate:

Static EW W/Z algebra is not a source-response certificate.  `dM_W/dh = g2/2`
is allowed only after canonical `H` has been supplied; it must not be imported
as `dM_W/ds` for the Cl(3)/Z3 source.  Slope-only W/Z outputs are also
forbidden as proof input unless they come from production W/Z correlator mass
fits under the same source and are paired with sector-overlap and
canonical-Higgs identity certificates.

2026-05-02 canonical-Higgs operator realization gate:

EW gauge-mass diagonalization, scalar Hessian algebra, or any note that begins
after canonical `H` is supplied is not a same-surface PR #230 operator
realization.  The route needs an explicit `O_H` or radial `H` observable on the
Cl(3)/Z3 source surface, with `C_sH` and `C_HH` pole residues or an equivalent
identity theorem.  Do not treat source-only `C_ss`, static EW algebra, D17
carrier support, or `H_unit` matrix-element readout as that missing operator.

2026-05-02 H_unit canonical-Higgs operator candidate gate:

`H_unit` may be discussed as a substrate/D17 bilinear candidate only.  It must
not be used as the canonical `O_H` for PR #230 unless the route supplies the
same pole-purity, `C_sH` / `C_HH`, source-overlap, inverse-propagator
derivative, and canonical-normalization certificates required of any
same-surface canonical-Higgs operator candidate.

2026-05-02 source-Higgs cross-correlator manifest:

A manifest for `O_H` / `C_sH` / `C_HH` production rows is planning support
only.  It must not be used as evidence until production rows, pole residues,
covariance, model-class/FV/IR controls, and the retained-route claim gate all
pass.

2026-05-02 neutral scalar commutant rank no-go:

Neutral scalar symmetry labels, D17 carrier support, and commutant rank
bookkeeping may be used only as support.  They must not be promoted to a
rank-one dynamical theorem, source-pole purity certificate, or
canonical-Higgs overlap identity.  A future positive route must derive the
rank-one response dynamically or measure `C_sH` / `C_HH` pole data on the same
surface.

2026-05-02 neutral scalar dynamical rank-one closure attempt:

A finite orthogonal neutral pole must not be assumed away.  Current dynamics
do not derive rank-one purity merely because the source-created pole mass and
residue can be measured.  Rank-one closure requires a new microscopic theorem,
same-surface `C_sH` / `C_HH` Gram-purity data, or an accepted source-Higgs
identity certificate.

2026-05-02 orthogonal neutral decoupling no-go:

Finite or heavy orthogonal neutral mass gaps may not be used as decoupling
closure unless a current-surface theorem derives the required scaling of
source-Higgs overlap or orthogonal top coupling.  Generic gap language is
support only and does not certify `cos(theta)=1`, `kappa_s`, or source-pole
purity.

2026-05-03 source-Higgs harness default-off guard:

The production certificate's `source_higgs_cross_correlator` guard is claim
hygiene only.  The harness may contain default-off finite-row instrumentation,
but it is enabled only behind a same-surface canonical-Higgs operator
certificate and explicit source-Higgs cross/noise settings.  Guard metadata,
default-off instrumentation, and unratified finite rows must not be used as
source-Higgs evidence, Gram purity, canonical-Higgs normalization, or
retained/proposed-retained support.

2026-05-02 W/Z response harness absence guard:

The production certificate's `wz_mass_response` guard is claim hygiene only.
It marks W/Z response rows absent unless actually implemented.  It must not be
used as W/Z response evidence, gauge-normalized closure, sector-overlap
identity, canonical-Higgs identity, or retained/proposed-retained support.

2026-05-02 complete source-spectrum identity no-go:

Complete same-source `C_ss(p)` data and same-source `dE_top/ds` are still
source-only observables.  They must not be used as a canonical-Higgs identity,
`O_H`, `C_sH`, `C_HH`, W/Z response, or no-orthogonal-top-coupling theorem.
Any route using complete source-spectrum data still needs non-source-only
identity input before retained/proposed-retained wording is allowed.

2026-05-02 neutral scalar top-coupling tomography gate:

A rank-one source-only response matrix is not a top-coupling tomography
certificate.  It must not be used as a rank-one neutral-scalar theorem, a
no-orthogonal-top-coupling theorem, a same-surface `O_H/C_sH/C_HH` row, or a
W/Z response row.  Retained/proposed-retained wording still requires a full
rank/identity certificate on the current surface.

2026-05-05 neutral off-diagonal generator derivation:

Neutral off-diagonal generator derivation is an allowed outside-math route
only if it derives a mixed source/orthogonal neutral generator on the same
PR230 Cl(3)/Z3 surface.  Burnside, Perron-Frobenius, Schur commutants, GNS
flat extension, exact tensor methods, and PSLQ/value recognition are not proof
selectors until the mixed generator is derived on the same PR230 surface.  A
synthetic primitive matrix or source-only block-diagonal witness must not be
used as a neutral irreducibility, primitive-cone, source-Higgs, W/Z, Schur, or
retained/proposed-retained top-Yukawa certificate.

2026-05-02 FH/LSZ chunk011 target-timeseries checkpoint:

Target time-series presence in one chunk is not production evidence and not a
canonical-Higgs identity.  It must not be used as target ESS for chunks that do
not carry target time series, as response stability, as pole/FV/IR/model-class
control, or as retained/proposed-retained `y_t` support.

2026-05-05 fresh artifact literature route review:

The selected clean artifact contract is `O_H/C_sH/C_HH`, but no such artifact
exists on the current surface.  FMS/gauge-invariant Higgs literature may guide
an action-first construction only after a same-source EW/Higgs action is
defined on the PR230 surface.  It must not be used to identify the current
Cl(3)/Z3 scalar source with the canonical Higgs, to set `kappa_s = 1`, or to
treat source-only FH/LSZ rows as source-Higgs Gram purity.  Feynman-Hellmann,
Lellouch-Luscher, RI/MOM, PSLQ, Picard-Fuchs/D-module, exact tensor/PEPS,
free-probability, and motivic tools remain certificate engines only; method
names are not proof selectors.

2026-05-05 action-first `O_H/C_sH/C_HH` artifact attempt:

The action-first `O_H/C_sH/C_HH` route is allowed only as a genuine artifact
attempt.  It must first derive or certify a same-source EW/Higgs action on the
PR230 Cl(3)/Z3 surface, then derive a gauge-invariant canonical `O_H`, and
only then write or consume same-surface `C_ss/C_sH/C_HH` pole rows.  Standard
EW action formulas, FMS names, gauge-invariant-composite language, and the
existence of structural EW/Higgs notes are not proof selectors for current
PR230 closure.

2026-05-05 PR541-style holonomic source-response route:

The PR541-style holonomic source-response route is a compute/proof discipline,
not an operator-definition shortcut.  Picard-Fuchs, D-module, creative
telescoping, exact tensor/PEPS, and source-generating functional methods are
not proof selectors until a same-current-surface O_H/h-source artifact exists.
They may compute `Z(beta,s,h)` derivatives only after the PR230 action/measure,
source operator, canonical `O_H`, and source coordinates are defined on the
same current surface.  Source-only `Z(s,0)` does not determine `C_sH`, `C_HH`,
or source-Higgs Gram purity.

2026-05-05 Reflection plus determinant positivity primitive-upgrade:

Reflection plus determinant positivity primitive-upgrade is now an exact
negative boundary on the current PR230 surface.  OS/reflection positivity and
the staggered-Wilson determinant-positivity bridge are not proof selectors
until a same-surface neutral primitive-cone certificate exists.  They supply
positivity preservation only; a reducible block-diagonal neutral transfer can
preserve positive spectral/fermion-measure support while leaving an
orthogonal neutral top-coupled scalar invisible to source-only rows.

2026-05-05 derived rank-one bridge:

The source-only rank-one route may use Perron-Frobenius/Krein-Rutman or
primitive-cone mathematics only after PR230 supplies a same-surface neutral
scalar transfer certificate.  The load-bearing premises are a defined neutral
basis, a nonnegative transfer matrix on a certified cone, strong connectivity,
a positive primitive power, isolated pole authority, positive source overlap,
and canonical-Higgs/source-overlap authority.  Positivity preservation from
reflection positivity, determinant positivity, positive Euclidean measure, or
synthetic finite matrices is not enough and must not be used as positivity
improvement.  Conditional rank-one support is not a source-to-Higgs
normalization and cannot set `kappa_s = 1` or authorize
retained/proposed-retained closure.

2026-05-07 same-surface neutral multiplicity-one gate:

The gate is intake support only.  It requires a future same-surface
`Cl(3)/Z3` neutral representation/action, top-coupled neutral sector,
multiplicity-one or primitive-generator proof, canonical metric/LSZ
normalization, and an `O_sp = O_H` identity or measured `C_spH/C_HH`
pole-overlap rows.  The current two-singlet neutral surface is rejected and
cannot be used as canonical `O_H`, source-Higgs overlap, scalar-LSZ
normalization, `kappa_s=1`, retained, or proposed-retained authority.

2026-05-07 same-surface neutral multiplicity-one candidate attempt:

The target candidate file is not a proof selector.  The current candidate is
rejected until the PR230 surface supplies a physical primitive/off-diagonal
transfer, a selection rule excluding the orthogonal neutral top coupling,
canonical scalar LSZ/FV/IR metric authority, or measured `C_spH/C_HH`
pole-overlap rows.  Candidate file presence alone cannot certify canonical
`O_H`, source-Higgs overlap, scalar-LSZ normalization, `kappa_s=1`, retained,
or proposed-retained authority.

2026-05-05 O_H/source-Higgs authority rescan:

O_H/source-Higgs authority rescan is an exact current-surface inventory gate,
not a proof selector.  Existing FMS, action-first, invariant-ring, GNS,
holonomic, Perron, positivity, and determinant/reflection-positivity artifacts
are not proof selectors until canonical O_H or C_sH/C_HH pole rows exist on the
same PR230 surface.  A source-only row family with fixed `C_ss` and variable
`C_sH/C_HH` remains positive, so source-only rows plus positivity cannot select
the canonical-Higgs overlap, set `kappa_s = 1`, or authorize
retained/proposed-retained closure.

2026-05-07 two-source taste-radial chunks029-030 package:

Chunks001-030 now supply finite same-surface `C_ss/C_sx/C_xx` row support
through the taste-radial chart.  This is not permission to read `x` as
canonical `H`, not permission to alias `C_sx/C_xx` as canonical
`C_sH/C_HH`, and not permission to treat first-shell Schur/Stieltjes
diagnostics as scalar-LSZ authority.  The same forbidden imports remain
forbidden: `H_unit`, `yt_ward_identity`, observed top or `y_t`, `alpha_LM`,
plaquette/`u0`, reduced pilots as production evidence, and fiat
`c2 = 1`, `Z_match = 1`, or `kappa_s = 1`.  Successor chunks031-032 are
active run-control/log state only until completed, checkpointed, and packaged.

2026-05-07 two-source taste-radial chunks027-028 package:

Chunks001-028 now supply finite same-surface `C_ss/C_sx/C_xx` row support
through the taste-radial chart.  This is not permission to read `x` as
canonical `H`, not permission to alias `C_sx/C_xx` as canonical
`C_sH/C_HH`, and not permission to treat first-shell Schur/Stieltjes
diagnostics as scalar-LSZ authority.  The same forbidden imports remain
forbidden: `H_unit`, `yt_ward_identity`, observed top or `y_t`, `alpha_LM`,
plaquette/`u0`, reduced pilots as production evidence, and fiat
`c2 = 1`, `Z_match = 1`, or `kappa_s = 1`.  Successor chunks029-030 are
run-control/log/empty-directory state only until completed, checkpointed, and
packaged.

2026-05-07 two-source taste-radial chunks025-026 package:

Chunks001-026 now supply finite same-surface `C_ss/C_sx/C_xx` row support
through the taste-radial chart.  This is not permission to read `x` as
canonical `H`, not permission to alias `C_sx/C_xx` as canonical
`C_sH/C_HH`, and not permission to treat first-shell Schur/Stieltjes
diagnostics as scalar-LSZ authority.  The same forbidden imports remain
forbidden: `H_unit`, `yt_ward_identity`, observed top or `y_t`, `alpha_LM`,
plaquette/`u0`, reduced pilots as production evidence, and fiat
`c2 = 1`, `Z_match = 1`, or `kappa_s = 1`.  Chunks027-028 are active
run-control only until completed, checkpointed, and packaged.

2026-05-07 two-source taste-radial chunks023-024 package:

Chunks001-024 now supply finite same-surface `C_ss/C_sx/C_xx` row support
through the taste-radial chart.  This is not permission to read `x` as
canonical `H`, not permission to alias `C_sx/C_xx` as canonical
`C_sH/C_HH`, and not permission to treat first-shell Schur/Stieltjes
diagnostics as scalar-LSZ authority.  The same forbidden imports remain
forbidden: `H_unit`, `yt_ward_identity`, observed top or `y_t`, `alpha_LM`,
plaquette/`u0`, reduced pilots as production evidence, and fiat
`c2 = 1`, `Z_match = 1`, or `kappa_s = 1`.

2026-05-07 OS transfer-kernel artifact gate:

The OS/transfer/GEVP route is an artifact contract, not a shortcut.  The
current finite scalar `C_ss/C_sx/C_xx` rows are equal-time covariance
diagnostics with configuration timeseries.  They must not be treated as
same-surface Euclidean-time scalar correlation matrices `C_ij(t)`, transfer
matrices, action generators, pole-residue rows, or source-Higgs overlap
authority.  Top-correlator `tau` rows do not supply scalar source/Higgs
matrix rows.

Forbidden load-bearing assumptions for this route:

- `configuration_timeseries = Euclidean-time kernel`
- `static C(0) covariance = transfer/action generator`
- `finite C_sx/C_xx = canonical C_sH/C_HH`
- `taste-radial x = canonical O_H`
- `OS/transfer/GEVP/D-module/tensor/PSLQ method name = proof authority`
- `kappa_s = 1`, `c2 = 1`, or `Z_match = 1` by convention

The only admissible reopen is a same-surface scalar time-lag row packet
`C_ss(t)`, `C_sH(t)`, `C_HH(t)` for certified canonical `O_H`, or
`C_ss(t)`, `C_sx(t)`, `C_xx(t)` plus a theorem identifying `x` with canonical
`O_H` or a physical neutral transfer, with pole/FV/IR/threshold authority,
overlap normalization, covariance, seed metadata, and all claim firewalls.

2026-05-07 source-Higgs time-kernel harness extension:

The harness can now emit default-off same-surface scalar time-lag rows, but
that is an implementation artifact, not a physics premise.  The current smoke
uses the taste-radial second-source certificate and therefore does not derive
canonical `O_H`, source-Higgs overlap, scalar LSZ normalization, or `kappa_s`.

Additional forbidden load-bearing assumptions:

- `source_higgs_time_kernel_v1 smoke = production evidence`
- `C_sx/C_xs/C_xx(t) taste-radial aliases = canonical C_sH/C_Hs/C_HH(t)`
- `same-surface time-kernel schema = pole extraction`
- `normal-cache reuse = physics authority`
- `selected-mass-only support row = physical y_t readout`

Allowed use: run future production rows once a canonical `O_H` or physical
neutral/W/Z identity exists, then apply OS/GEVP pole/FV/IR/threshold and
overlap-normalization gates before any retained proposal.

2026-05-07 source-Higgs time-kernel GEVP contract:

The GEVP postprocessor can be a valid extraction method only after the physical
row and identity premises exist.  On the current smoke surface, a formal GEVP
diagnostic is just algebra on reduced rows.

Additional forbidden load-bearing assumptions:

- `formal GEVP diagnostic = physical scalar pole`
- `negative or small smoke GEVP eigenvalue = physical energy`
- `two time lags = pole plateau`
- `one configuration = production covariance`
- `GEVP method name = canonical O_H/source-overlap authority`

Allowed use: keep the GEVP contract as the future acceptance target for
production same-surface `C_ij(t)` rows after the canonical `O_H` or physical
neutral/W/Z identity premise is independently certified.

2026-05-07 two-source taste-radial chunks033-034 package:

Chunks001-034 now supply finite same-surface `C_ss/C_sx/C_xx` row support
through the taste-radial chart.  This is not permission to read `x` as
canonical `H`, not permission to alias `C_sx/C_xx` as canonical
`C_sH/C_HH`, and not permission to treat first-shell Schur/Stieltjes
diagnostics as scalar-LSZ authority.  The same forbidden imports remain
forbidden: `H_unit`, `yt_ward_identity`, observed top or `y_t`, `alpha_LM`,
plaquette/`u0`, reduced pilots as production evidence, and fiat
`c2 = 1`, `Z_match = 1`, or `kappa_s = 1`.  Chunk035 is active run-control
only until completed, checkpointed, and packaged.

2026-05-07 higher-shell Schur/scalar-LSZ production contract:

The higher-shell command contract is infrastructure support only.  It is not
proof selectors until the separate higher-shell rows are actually run,
complete, pole-tested, FV/IR-tested, and bridged to canonical O_H or physical
response.  It must not be treated as row evidence, complete monotonicity,
scalar-pole authority, FV/IR authority, canonical `O_H`/source-overlap,
physical `W/Z` response, `kappa_s`, retained, or proposed-retained closure.

Additional forbidden load-bearing assumptions:

- `higher-shell command preview = measurement rows`
- `five q_hat^2 levels = complete monotonicity`
- `higher-shell manifest = pole/threshold/FV/IR authority`
- `future Schur rows = canonical O_H/source-overlap authority`
- `launch_allowed_now=false` can be ignored while active chunks own the packet

2026-05-07 two-source taste-radial chunks035-036 package:

Chunks035-036 are bounded support only.  The package raises the partial row
packet to `ready=36/63`, but finite `C_ss/C_sx/C_xx` rows, first-shell
Stieltjes/Schur diagnostics, and chunk logs are not proof selectors for
canonical `O_H`, scalar-LSZ/FV, W/Z response, Schur pole authority, neutral
primitive transfer, retained, or proposed-retained closure.

2026-05-07 Schur `C_x|s` one-pole finite-residue scout:

The Schur C_x|s one-pole finite-residue scout is bounded support only.  The
two endpoint means determine a one-pole interpolation, but that interpolation
is model-class support only: one-pole interpolation is model-class support only.
Positive two-pole endpoint counterfamilies match the same current endpoints
while changing the low-pole residue.  Therefore the one-pole fit is not
scalar-LSZ pole authority, not a physical scalar pole certificate, not a
`K'(pole)` or pole-residue certificate, and not canonical
`O_H`/source-overlap/W/Z response authority.

Additional forbidden load-bearing assumptions:

- `C_x|s` one-pole interpolation = physical scalar pole
- one-pole residue = scalar-LSZ pole residue
- one-pole finite-residue scout is not scalar-LSZ pole authority
- two endpoint values = complete Stieltjes/threshold/FV authority
- `C_x|s` residual = canonical `O_H`
- one-pole finite-residue scout = retained or proposed-retained closure

2026-05-07 two-source taste-radial chunks037-038 package:

Chunks037-038 are bounded support only.  The package raises the partial row
packet to `ready=38/63`, but finite `C_ss/C_sx/C_xx` rows, first-shell
Stieltjes/Schur diagnostics, the refreshed one-pole interpolation, chunk logs,
live status, and active workers are not proof selectors for canonical `O_H`,
scalar-LSZ/FV, W/Z response, Schur pole authority, neutral primitive transfer,
retained, or proposed-retained closure.

Additional forbidden load-bearing assumptions:

- `ready=38/63` = complete production row packet
- active chunks039-040 = evidence
- refreshed one-pole interpolation = pole/model-class authority
- finite `C_sx/C_xx` rows = canonical `C_sH/C_HH`
- finite first-shell Schur support = scalar-LSZ/FV authority

2026-05-07 two-source taste-radial chunks061-062 package:

Chunks061-062 are bounded support only.  The package raises the partial row
packet to `ready=62/63`, but finite `C_ss/C_sx/C_xx` rows, first-shell
Stieltjes/Schur diagnostics, the one-pole interpolation, chunk logs, live
status, and active workers are not proof selectors for canonical `O_H`,
scalar-LSZ/FV, W/Z response, Schur pole authority, neutral primitive transfer,
retained, or proposed-retained closure.

Additional forbidden load-bearing assumptions:

- `ready=62/63` = complete production row packet
- active chunk063 = evidence
- refreshed one-pole interpolation = pole/model-class authority
- finite `C_sx/C_xx` rows = canonical `C_sH/C_HH`
- finite first-shell Schur support = scalar-LSZ/FV authority
- H1/H2 Z3 support plus 62 finite rows = H3/H4 primitive transfer authority

2026-05-12 higher-shell Schur/scalar-LSZ launch preflight:

The refreshed higher-shell contract is launch-admissible infrastructure only.
The completed four-mode packet and absent active workers clear the run-control
preflight for a separate higher-shell campaign, but no higher-shell rows have
been launched or written.

Additional forbidden load-bearing assumptions:

- `launch_allowed_now=true` = measurement evidence
- higher-shell command preview = complete monotonicity
- five planned `q_hat^2` levels = scalar-pole/threshold/FV authority
- future higher-shell roots = existing Schur `A/B/C` pole rows
- launch preflight = canonical `O_H`, source-overlap, W/Z response, retained,
  or proposed-retained closure

2026-05-12 higher-shell Schur/scalar-LSZ chunks001-002 active wave:

The launched higher-shell chunks are run-control state only.  Active process
rows, logs, pid files, empty directories, partial directories, and
uncheckpointed higher-shell row outputs are not load-bearing proof inputs.

Additional forbidden load-bearing assumptions:

- active higher-shell chunks001-002 = row evidence
- chunk pid/log existence = completed measurement
- partial higher-shell output directories = scalar-LSZ authority
- uncheckpointed higher-shell JSON = complete monotonicity or pole authority
- two active chunks = complete higher-shell packet
- higher-shell run-control = canonical `O_H`, source-overlap, W/Z response,
  retained, or proposed-retained closure
