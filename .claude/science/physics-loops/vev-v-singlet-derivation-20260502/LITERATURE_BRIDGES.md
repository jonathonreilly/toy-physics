# LITERATURE BRIDGES — VEV V-Singlet Derivation Campaign

**Date:** 2026-05-02
**Literature flag:** allowed (`--literature` passed by user)

## H2 literature needs

H2 is essentially a self-contained reformulation INSIDE the framework. It
needs literature only as:

| Literature element | Role | Authority |
|---|---|---|
| Standard finite-volume thermodynamic / statistical-mechanics fact: `Z = ∑ exp(-S)` is invariant under any symmetry of `S` | non-derivation context (textbook fact, used to justify Lemma H2.1) | any standard stat-mech textbook (e.g., Kardar 2007, Le Bellac 1991) |
| Standard EFT identification: `v²` = curvature of effective potential at origin (or equivalently, inverse propagator at zero momentum) | non-derivation context (used in C1 admission) | Peskin-Schroeder ch. 11 (effective potential), or Coleman-Weinberg 1973 |
| Klein-four / Z₂×Z₂ representation theory | mathematical infrastructure (no novel claim, just standard rep theory) | any group-theory text; framework already uses it |

## H1 literature needs (Route 2 cheap probe)

| Literature element | Role |
|---|---|
| Cl(3) generator counting (8 generators: 1 scalar, 3 vectors, 3 bivectors, 1 pseudoscalar) | standard Clifford algebra |
| Standard SU(N_c) Wilson lattice gauge action: `β = 2N_c/g²` | textbook lattice (Creutz 1983, Montvay-Münster 1994) |

## H1 literature needs (Route 1 deep stretch — if attempted)

| Literature element | Role |
|---|---|
| Class A determinant identity / minimal-block factorization | framework-internal (`A7` from MATSUBARA decomposition) |
| Lattice gauge theory minimal-block / mean-field methods | (Münster 1981, Drouffe-Zuber 1983) — for context only, not load-bearing |

## H1 literature needs (Route 3 bootstrap — OUT OF SCOPE)

Recorded for HANDOFF, not for execution this campaign:
- Anderson-Kruczenski 2017 — modern lattice bootstrap framework
- Kazakov-Zheng 2022 — improved bootstrap precision for SU(N) plaquettes
- Lin et al 2023 — recent SU(3) bootstrap at β=6 (~10⁻³ precision)

## Forbidden literature usage

- Any literature `v_meas`, `M_Pl`, `α_LM`, `⟨P⟩` value as derivation input
- Any phenomenological 7/8 from Stefan-Boltzmann (the framework's (7/8) is
  algebraic A_2/A_4 ratio, not the thermal SB factor — they are NOT the same
  thing despite the numerical coincidence)
- Any beyond-textbook claim from a paper without independent re-derivation
  inside the framework

## Bridges if literature is invoked

When invoking literature, record the exact role in the runner output and the
note's "Out of scope (admitted-context)" section. Do NOT promote
admitted-context literature to load-bearing without independent framework
derivation.
