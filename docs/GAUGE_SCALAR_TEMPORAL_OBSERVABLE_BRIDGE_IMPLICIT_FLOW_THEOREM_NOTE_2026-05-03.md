# Gauge-Scalar Temporal Observable Bridge Implicit-Coordinate Bounded Theorem

**Date:** 2026-05-03
**Claim type:** bounded_theorem
**Status:** bounded response-coordinate theorem proposal. This note proves an
exact implicit coordinate identity for Wilson plaquette expectations; it does
not discharge the parent observable bridge gate, does not evaluate the full
plaquette at `beta = 6`, does not fit `beta_eff`, and does not import
Monte-Carlo, PDG, or perturbative running data.
**Primary runner:** `scripts/frontier_gauge_scalar_temporal_observable_bridge_implicit_flow.py`
**Parent gate:** `docs/GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md`

## 0. Target

The parent stretch note isolated the residual

```text
<P>_full = R_O(beta_eff)                                      (BRIDGE)
```

between the full interacting Wilson plaquette expectation and the local
one-plaquette response at the completed effective coupling.

The bounded lift here is not a numerical evaluation of `<P>_full`. It is the
implicit response-coordinate theorem:

> On each finite Wilson evaluation surface, and on any infinite-volume limit
> where the full plaquette expectation exists, there is one unique
> nonperturbative response coordinate `beta_eff` determined by the Wilson
> partition function itself, and the identity `P = R_O(beta_eff)` holds by
> construction.

This is a bounded theorem proposal because the content is the exact implicit
response-coordinate and susceptibility-flow law. It is not a proof that the
current primitives independently derive an evaluated `beta_eff(6)` or
`<P>(6)`.

## 1. Allowed premises

The proof uses only the fixed `A_min` surface from the stretch note plus
standard compact-measure calculus:

| Premise | Role |
|---|---|
| Finite Wilson gauge action at `beta = 6`, `g_bare = 1` | full interacting expectation surface |
| Accepted Wilson local scalar gauge-source grammar | identifies the local response operator |
| Temporal-completion theorem kernel `K_O(omega) = 3w(3 + sin^2 omega)` | fixes the completed local source class |
| Haar compactness and differentiability under the finite integral | proves analyticity and susceptibility identities |
| Inverse-function theorem | converts strict local response monotonicity into the unique completed coupling |

No external plaquette value, fitted coupling, perturbative beta-function, or
same-surface numerical selector is used as a proof input.

## 2. Definitions

Let

```text
X(U) = (1/3) Re Tr U
```

be the normalized one-plaquette Wilson source observable.

The local response attached to the accepted Wilson gauge-source class is

```text
R_O(gamma) = d/dgamma log Z_1(gamma),

Z_1(gamma) = int_SU(3) dU exp[gamma X(U)].
```

The full finite-volume Wilson plaquette expectation on a symmetric finite
evaluation surface `Lambda` is

```text
P_Lambda(beta)
  = (1 / N_plaq) d/dbeta log Z_Lambda(beta),

Z_Lambda(beta)
  = int DU exp[beta sum_p X(U_p)].
```

The response coordinate is defined structurally, not fitted:

```text
beta_eff,Lambda(beta) := R_O^(-1)(P_Lambda(beta)).
```

This definition uses the exact Wilson partition function and the exact local
response map. It does not consume a measured target value, but it also should
not be read as an independently evaluated coupling.

## 3. Theorem 1: the local response is a bijective response coordinate

`R_O(gamma)` is analytic for real `gamma` because `SU(3)` is compact and the
integrand is entire.

Differentiating gives

```text
R_O'(gamma) = Var_gamma(X).
```

The density `exp[gamma X]` is strictly positive for finite `gamma`, and `X` is
not constant on `SU(3)`:

```text
X(I) = 1,
X(exp(2 pi i / 3) I) = -1/2.
```

Therefore `R_O'(gamma) > 0`. Also `R_O(0) = 0`, `R_O(gamma) < 1` for finite
`gamma`, and `R_O(gamma) -> 1` as `gamma -> infinity`.

Hence `R_O : [0, infinity) -> [0, 1)` is a one-to-one response coordinate.

## 4. Theorem 2: the full finite Wilson plaquette lies in the response range

For the finite interacting Wilson theory,

```text
P_Lambda(beta)
  = (1 / N_plaq) < sum_p X(U_p) >_beta.
```

Each plaquette source satisfies `X(U_p) <= 1`; the set where every plaquette is
exactly identity has measure zero for finite `beta`; and the Wilson density is
strictly positive. Therefore

```text
0 <= P_Lambda(beta) < 1
```

for finite `beta >= 0`. Thus `P_Lambda(beta)` is in the range of the local
response coordinate `R_O`.

## 5. Corollary: exact implicit coordinate identity

Since `R_O` is bijective onto `[0,1)` and `P_Lambda(beta)` lies in `[0,1)`,
the response coordinate

```text
beta_eff,Lambda(beta) = R_O^(-1)(P_Lambda(beta))
```

exists and is unique. Substituting the definition gives the exact coordinate
identity:

```text
P_Lambda(beta) = R_O(beta_eff,Lambda(beta)).
```

At the framework point `beta = 6`, this has the same formal shape as the parent
residual bridge on the finite Wilson surface:

```text
<P>_full,Lambda = R_O(beta_eff,Lambda(6)).
```

If the thermodynamic-limit plaquette

```text
P_full(beta) = lim_Lambda P_Lambda(beta)
```

exists and remains below one, continuity of `R_O^(-1)` gives the corresponding
limit coupling

```text
beta_eff(beta) = lim_Lambda beta_eff,Lambda(beta)
```

and the full-limit coordinate identity

```text
<P>_full = R_O(beta_eff).
```

## 6. Nonperturbative flow form

Differentiating the exact coordinate identity yields the susceptibility
transport law:

```text
beta_eff,Lambda'(beta)
  = chi_Lambda(beta) / chi_1(beta_eff,Lambda(beta)),
```

where

```text
chi_Lambda(beta)
  = d P_Lambda / d beta
  = Var_beta(sum_p X(U_p)) / N_plaq,

chi_1(gamma)
  = d R_O / d gamma
  = Var_gamma(X).
```

Equivalently,

```text
beta_eff,Lambda(beta)
  = R_O^(-1)( int_0^beta chi_Lambda(s) ds ).
```

This is not a perturbative beta-function. It is an exact finite-volume
susceptibility identity derived from the Wilson path integral.

## 7. Relationship to the stretch obstruction routes

| Stretch route | Obstruction in stretch note | What this theorem contributes |
|---|---|---|
| O1 Schwinger-Dyson | hierarchy does not collapse to local response | records an exact inverse-response coordinate once the full expectation is known |
| O2 effective action | full effective action is not computed in closed form | avoids a closed effective action but still depends on the exact Wilson expectation |
| O3 RG | perturbative running cannot derive the bridge | records an exact susceptibility flow, not perturbative RG running |

The cost is explicit and bounded: this theorem gives an implicit coordinate
identity but does not evaluate the nonperturbative susceptibility profile or
the environment Perron data, and it does not close the parent gate by itself.

## 8. What this supports

- exact existence and uniqueness of the completed local response coupling on
  finite Wilson evaluation surfaces;
- exact implicit coordinate identity
  `P_Lambda(beta) = R_O(beta_eff,Lambda(beta))`;
- exact nonperturbative susceptibility-flow law for `beta_eff`;
- proof that no fitted, PDG, Monte-Carlo, perturbative-running, or numeric
  same-surface selector input is load-bearing.

## 9. What remains open

- closed-form evaluation of `beta_eff(6)`;
- closed-form evaluation of `<P>(6)`;
- an independent derivation of `beta_eff(6)` from current primitives rather
  than defining it as `R_O^(-1)(P(6))`;
- explicit `rho_(p,q)(6)` / `Z_6^env(W)` environment Perron data;
- numerical migration of the canonical plaquette package.

This distinction is the bounded status: the implicit coordinate identity is
closed, while the evaluated plaquette, independent completed-coupling
derivation, and environment data are not.

## 10. Commands

```bash
python3 scripts/frontier_gauge_scalar_temporal_observable_bridge_implicit_flow.py
```

Expected summary:

```text
SUMMARY: THEOREM PASS=8 SUPPORT=3 FAIL=0
```
