# Atomic Lane 2 — QED Running Dependency Firewall

**Date:** 2026-04-30
**Status:** support / exact reduction theorem (no claim promotion). This note
is a support/firewall artifact for Lane 2; it does **not** derive any
atomic-scale prediction.
**Script:** `scripts/frontier_atomic_lane2_qed_running_dependency_firewall.py`
**Lane:** 2 - Atomic-scale predictions, route depending on `alpha(0)`.

---

## 0. Why this note exists

The 2026-04-27 [`ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE`](./ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md)
records the negative boundary

```text
retained alpha_EM(M_Z) + textbook hydrogen formula  =/=>  retained Rydberg.
```

That note names "QED running bridge from `alpha_EM(M_Z)` to `alpha(0)`" as one
of the three required missing inputs but does not quantify what closing that
bridge would itself require. This note closes that gap. It treats the
`alpha(M_Z) -> alpha(0)` running step as its own reduction theorem and exposes
the load-bearing primitives.

The result is: the running primitive is itself blocked by Lanes 3 + 6 + a
hadronic vacuum-polarization input that depends on Lane 1 substrate work.
It is not a single one-line bridge. Atomic Lane 2 closure is therefore
conditional on at least three other Tier 1 lanes plus a QED substrate
primitive.

This sharpens — does not replace — the 2026-04-27 firewall.

## 1. Standard QED running

Standard reference (textbook QED, Peskin & Schroeder §11.6, MS-bar conventions):
the inverse fine-structure constant runs as

```text
alpha^{-1}(mu) = alpha^{-1}(0) - Delta alpha(mu^2)
```

with the leptonic + heavy-quark + hadronic decomposition

```text
Delta alpha(M_Z^2) = Delta alpha_lep + Delta alpha_top + Delta alpha_had^(5).
```

Each piece is non-trivial:

| piece | sign | physical content | retained primitives required |
|---|---|---|---|
| `Delta alpha_lep` | + | leptonic vacuum polarization summed over `e, mu, tau` | retained `m_e, m_mu, m_tau` (Lane 6) + QED loop primitive |
| `Delta alpha_top` | small + | perturbative top-quark loop | retained `m_t` (already retained) + QED loop primitive |
| `Delta alpha_had^(5)` | + | non-perturbative hadronic vacuum polarization summed over `u, d, s, c, b` | hadronic R-ratio data **or** a retained framework-substrate hadronic vacuum-polarization computation (Lane 1 dependent) |

Each `Delta alpha_lep,f` for a single lepton at the perturbative one-loop
level (`s >> m_f^2`) is

```text
Delta alpha_lep,f(s) ~= (alpha / 3 pi) * [ ln(s / m_f^2) - 5/3 ]
```

(massless-fermion limit; corrected by mass-dependent terms near threshold and
by higher-order O(alpha) and O(alpha alpha_s) effects). The prefactor `alpha`
makes the running self-referential at leading order — it can be evaluated
either with `alpha(0)` or `alpha(M_Z)` at one loop, with the choice
absorbed into higher-order matching. The argument depends on the log of the
lepton mass. Without retained lepton masses on the framework substrate,
this contribution cannot be derived from retained `alpha_EM(M_Z)` alone.

For each heavy-quark threshold the analog one-loop formula is

```text
Delta alpha_q,heavy(s) ~= (3 Q_q^2 alpha / 3 pi) * [ ln(s / m_q^2) - 5/3 ]
```

with the colour factor `N_c = 3` and the electric charge `Q_q = +2/3` or
`-1/3`. Again the result depends on the heavy-quark mass.

For the light-quark contribution (`u, d, s` and the perturbative-tail of
`c, b`) the perturbative formula is unreliable below ~`m_c` because QCD is
strongly coupled. The standard approach is the dispersion-relation /
optical-theorem identity

```text
Delta alpha_had^(5)(s) = - (alpha s / 3 pi) * P int_{4 m_pi^2}^{infty}
    ds'  R(s') / [ s' (s' - s) ]
```

where `R(s) = sigma(e+ e- -> hadrons) / sigma(e+ e- -> mu+ mu-)`. Without
either real `R(s)` data **or** a framework-substrate hadronic-spectrum
computation, this integral cannot be evaluated.

## 2. Numerical decomposition (comparator only, not proof input)

Using PDG comparator values (textbook m_l, m_q, and a textbook hadronic
R-ratio sum) only to expose the magnitude of each contribution at leading
order:

| piece | LO comparator value | LO percent of leading-order sum |
|---|---:|---:|
| `Delta alpha_lep` (e, mu, tau) | `+0.031477` | ~53% |
| `Delta alpha_top` (perturbative t loop, vanishingly small at M_Z) | `~ -7e-5` | ~0% |
| `Delta alpha_had^(5)` (u, d, s, c, b non-perturbative) | `+0.02766` | ~47% |
| Sum of leading-order pieces | `+0.05908` | 100% |

The total all-orders `Delta alpha(M_Z^2) ~= 0.0663` (extracted from PDG-2024
`alpha^{-1}(M_Z^2) = 127.951` via `Delta alpha = 1 - alpha(0)/alpha(M_Z)`)
is larger by `~12%` because of `O(alpha^2)` and `O(alpha alpha_s)`
higher-order corrections. The structural dependency argument here uses only
the LO sum; higher-order corrections introduce additional QED-loop primitive
imports but do not change the named load-bearing pieces R-Lep, R-Q-Heavy,
R-Had-NP.

These comparator values come from the PDG-2024 review and are admitted only
to scale the dependency, not to certify the framework. The framework itself
must reproduce the leptonic and hadronic contributions from retained
primitives before the running step is closed.

## 3. Theorem

**Theorem (Lane 2 QED running dependency firewall).** Assume the current
`origin/main` state on 2026-04-30:

- retained `alpha_EM(M_Z) = 1 / 127.67`;
- retained top-quark mass `m_t = 172.57 GeV`;
- open Lane 6 charged-lepton masses `m_e, m_mu, m_tau`;
- open Lane 3 quark masses `m_u, m_d, m_s, m_c, m_b`;
- open Lane 1 framework-substrate hadronic spectrum.

Then the QED running step `alpha_EM(M_Z) -> alpha(0)` cannot be closed as a
retained primitive on this surface. It splits into three sub-residuals, each
of which is itself open:

1. (R-Lep) leptonic vacuum-polarization contribution `Delta alpha_lep` is
   blocked by Lane 6.
2. (R-Q-Heavy) heavy-quark vacuum-polarization contribution
   `Delta alpha_q,heavy` for `c, b` is blocked by Lane 3.
3. (R-Had-NP) hadronic vacuum-polarization contribution
   `Delta alpha_had^(5)` for the non-perturbative `u, d, s` sector is
   blocked unless either:
   (a) the framework imports literature `R(s)` dispersion data (a hidden
   observational input), **or**
   (b) Lane 1 supplies a retained framework-substrate hadronic-spectrum
   computation that lets `R(s)` be derived internally.

In particular, no Lane 6 closure alone is sufficient for Lane 2 closure. Even
with `m_e` retained, both Lane 3 (via R-Q-Heavy) and Lane 1 (via R-Had-NP)
remain on the dependency chain.

## 4. What this retires

This retires one tempting follow-on shortcut not blocked by the 2026-04-27
firewall:

```text
retained alpha_EM(M_Z) + retained m_e (post-Koide / Lane 6)
  =/=>  retained alpha(0)
  =/=>  retained Rydberg.
```

The shortcut is false because the `alpha(M_Z) -> alpha(0)` running primitive
itself depends on Lane 3 + Lane 1, not only Lane 6.

It also names the smallest viable Lane 2 closure path:

> Lane 2 closure requires Lane 6 closure, Lane 3 closure (for `c, b`
> perturbative thresholds), and either (a) literature `R(s)` admitted as an
> observational input or (b) Lane 1 substrate `R(s)` retention.

If the closure path goes through (a), Lane 2 explicitly admits a hadronic
R-ratio observational import and the Rydberg claim becomes
"retained-with-budget on the admitted-R(s) surface" rather than fully
retained from internal primitives.

If the closure path goes through (b), Lane 2 closure is downstream of Lane 1
hadron spectroscopy retention.

## 5. Forbidden imports for this firewall

This note must not consume:

- the observed Rydberg value `13.6057 eV` as a proof input (only as a
  comparator);
- the observed PDG `alpha^{-1}(0) = 137.036` as a proof input (only as a
  comparator);
- the observed PDG `Delta alpha_had^(5)(M_Z^2)` numerical value as a proof
  input (only as a comparator).

The numerical decomposition in §2 uses these only to scale the magnitude of
each dependency.

## 6. What remains open after this firewall

- (R-Lep) needs Lane 6 + a retained QED leptonic-loop primitive on the
  framework substrate.
- (R-Q-Heavy) needs Lane 3 + a retained QED heavy-quark-loop primitive on the
  framework substrate.
- (R-Had-NP) needs Lane 1 substrate `R(s)` retention or admitted-R(s) status.
- The QED loop primitive itself (vacuum polarization at one loop with proper
  threshold matching) is currently a textbook input. Its retention on the
  framework substrate is a separate open primitive (it is implicit in
  `alpha_EM(M_Z)` retention, but the running formula uses the loop integrand
  shape, not just the value at one scale).

## 7. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_atomic_lane2_qed_running_dependency_firewall.py
```

Expected: `PASS=N FAIL=0` (see runner for current N).

The runner checks:

1. The firewall note exists and references the 2026-04-27 predecessor.
2. The theorem language is `support / exact reduction theorem`, not bare
   `retained`.
3. The numerical decomposition reproduces the textbook running on textbook
   inputs, demonstrating the running is well-defined when the load-bearing
   masses + hadronic data are supplied.
4. The substitution-failure magnitude (~7% in inverse-alpha, ~14% in `alpha^2`)
   matches the 2026-04-27 firewall's ~15% Rydberg-energy shift.
5. Each sub-residual (R-Lep, R-Q-Heavy, R-Had-NP) is independently named.
6. Forbidden-import roles are respected: comparator values do not appear as
   proof inputs.

## 8. Inputs and import roles

| Input | Role | Import class | Source |
|---|---|---|---|
| `alpha_EM(M_Z) = 1/127.67` | retained EW value | framework-derived | `docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX.md` |
| `m_t = 172.57 GeV` | retained top mass | framework-derived | retained matter-mass program |
| textbook `m_e, m_mu, m_tau` | scaling comparator for R-Lep | observational comparator (NOT proof input) | PDG 2024 |
| textbook `m_c, m_b` | scaling comparator for R-Q-Heavy | observational comparator (NOT proof input) | PDG 2024 |
| textbook `Delta alpha_had^(5)(M_Z^2) = 0.02766` | scaling comparator for R-Had-NP | observational comparator (NOT proof input) | Jegerlehner 2019 (PDG-cited) |
| `Delta alpha(mu^2)` formula | admitted standard QED running formula | admitted bridge | Peskin & Schroeder §11.6 |

No atomic observable is used to tune a framework parameter in this note.

## 9. Safe wording

**Can claim:**

- "Atomic Lane 2 closure depends on Lane 6 + Lane 3 + Lane 1 closures plus a
  retained QED loop primitive."
- "The `alpha_EM(M_Z) -> alpha(0)` running step is itself an open primitive
  requiring three sub-residuals."
- "Substituting `alpha_EM(M_Z)` for `alpha(0)` directly fails by ~7% in
  inverse-alpha and ~14% in the Rydberg energy."

**Cannot claim:**

- "This closes Lane 2." (it doesn't)
- "This retires the QED running step." (it doesn't — it sharpens the firewall)
- "Lane 2 closure is downstream only of Lane 6." (it isn't)
- bare `retained` or `promoted` on this artifact.

## 10. Cross-references

- [ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md](./ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md) — predecessor firewall this note sharpens.
- [docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md](./lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md) — Lane 2 parent.
- [docs/lanes/open_science/03_QUARK_MASS_RETENTION_OPEN_LANE_2026-04-26.md](./lanes/open_science/03_QUARK_MASS_RETENTION_OPEN_LANE_2026-04-26.md) — Lane 3 parent (R-Q-Heavy dependency).
- [docs/lanes/open_science/06_CHARGED_LEPTON_MASS_RETENTION_OPEN_LANE_2026-04-26.md](./lanes/open_science/06_CHARGED_LEPTON_MASS_RETENTION_OPEN_LANE_2026-04-26.md) — Lane 6 parent (R-Lep dependency).
- [docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md](./lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md) — Lane 1 parent (R-Had-NP dependency).
