# Universal Theta-Induced EDM Response Vanishing Theorem

**Date:** 2026-04-24
**Status:** proposed_retained structural corollary on the proposed_retained strong-CP action
surface
**Script:** `scripts/frontier_universal_theta_induced_edm_vanishing.py`

## Role

This note is the source-scoped extension of
`CKM_NEUTRON_EDM_BOUND_NOTE.md`.

The retained strong-CP theorem gives

```text
theta_eff = 0
```

on the retained Wilson-plus-staggered action surface. The neutron-EDM note
records the first observable consequence:

```text
d_n(theta) = 0,
```

so the surviving neutron EDM is CKM-only up to the stated bounded EFT bridge.

This note packages the corresponding universal response statement: every EDM
component whose source is the QCD vacuum angle has zero theta-induced
contribution on the retained action surface.

## Theorem

For any EDM observable `O` admitting the usual source decomposition

```text
O = O_CKM + O_BSM + theta_eff K_theta[O] + O(theta_eff^2),
```

the retained strong-CP action surface implies

```text
O_theta = theta_eff K_theta[O] = 0.
```

Equivalently, the QCD-theta response functional has zero support on the
retained surface:

```text
dO/dtheta_eff | retained = K_theta[O],
theta_eff | retained = 0,
therefore O_theta | retained = 0.
```

The result is source-scoped. It does not set the CKM component or any
independent BSM component to zero.

## Vanishing Theta-Induced Components

The retained theorem covers the theta-induced pieces of:

| observable family | retained theta-induced statement |
|---|---|
| neutron EDM | `d_n(theta) = 0` |
| proton EDM | `d_p(theta) = 0` |
| light-nuclear EDMs | `d_D(theta) = d_He3(theta) = d_He4(theta) = 0` |
| nuclear Schiff moments | `S_atom(theta) = 0` for theta-sourced Schiff moments |
| atomic and molecular EDMs | `d_atom(theta) = 0` for theta-sourced hadronic/nuclear response |
| charged leptons | QCD-theta-mediated lepton EDM response is zero |

The charged-lepton row is not a new lepton-sector EDM theorem. It only says
that a QCD-vacuum-angle source cannot feed a charged-lepton EDM when the
retained source angle is exactly zero.

## Operator-Level Boundary

The operator statement that is retained exactly is:

```text
theta_eff G Gtilde = 0
```

on the retained action surface.

Theta-sourced matching contributions into hadronic, nuclear, and atomic
CP-odd response channels also vanish. Examples include theta-sourced pion-
nucleon couplings, theta-sourced nucleon EDM counterterms, theta-sourced
Schiff moments, and theta-sourced atomic EDM response.

This is **not** a universal zero theorem for the full CP-odd EFT basis.
Independent quark chromo-EDM, Weinberg three-gluon, and CP-odd four-fermion
operators are separate source directions. They may be absent, CKM-suppressed,
or BSM-generated depending on the model, but their independent coefficients are
not eliminated by `theta_eff = 0` alone.

## Surviving Contributions

The retained package therefore has the following CP/EDM structure:

| source | status |
|---|---|
| QCD theta | exactly zero on the retained action surface |
| CKM weak CP | survives; neutron continuation is bounded near `10^-32 - 10^-33 e cm` |
| independent BSM CP-odd sources | outside this theorem |

For the neutron case, the bounded continuation is recorded in
`CKM_NEUTRON_EDM_BOUND_NOTE.md`. The exact
structural statement here is broader but less numerical: all theta-induced EDM
components vanish.

## Falsification Boundary

A positive EDM measurement by itself would not automatically falsify this
theorem. The falsification condition is source attribution.

The theorem would be falsified by a confirmed EDM signal that requires a
nonzero QCD theta source on the retained action surface. A signal attributed to
CKM weak CP or to an independent BSM CP-odd operator would instead live outside
this theorem.

## What Is Not Claimed

This note does not claim:

- that all EDMs vanish,
- that CKM weak EDMs vanish,
- that independent quark chromo-EDM, Weinberg, or CP-odd four-fermion
  coefficients vanish,
- that BSM CP violation is excluded,
- that the bounded CKM numerical estimates are derived here, or
- that the retained action-surface strong-CP theorem applies to every
  continuum formulation or regulator.

## How It Fits

The strong-CP/EDM chain is:

```text
STRONG_CP_THETA_ZERO
  -> CKM_NEUTRON_EDM_BOUND
  -> UNIVERSAL_THETA_INDUCED_EDM_VANISHING
```

The first note closes the retained action-surface theta source. The second
applies it to the neutron EDM and adds the bounded CKM continuation. This note
packages the general theta-induced response corollary across hadronic, nuclear,
atomic, and theta-mediated charged-lepton EDM channels.

## Command

```bash
python3 scripts/frontier_universal_theta_induced_edm_vanishing.py
```

## Citations

The load-bearing input `theta_eff = 0` is taken from the upstream
strong-CP theta-zero theorem; all theta-induced response statements in
this note inherit retention from that one-hop dependency. The neutron-EDM
specialisation that this note generalises is also explicitly cited.

- [STRONG_CP_THETA_ZERO_NOTE.md](STRONG_CP_THETA_ZERO_NOTE.md) — supplies
  `theta_eff = 0` on the retained Wilson-plus-staggered action surface
  (the load-bearing input of every "theta-induced ... = 0" row in the
  Vanishing Theta-Induced Components table).
- [CKM_NEUTRON_EDM_BOUND_NOTE.md](CKM_NEUTRON_EDM_BOUND_NOTE.md) — the
  prior single-channel statement that this note universalises across
  hadronic, nuclear, atomic, and theta-mediated charged-lepton EDM
  channels.

This citation block resolves the audit-lane condition that the strong-CP
theta-zero authority is registered as a one-hop dependency edge rather
than a prose-level reference.
