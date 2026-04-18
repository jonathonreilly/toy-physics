# Up-Type Mass Ratio — Phase 2 NNI Scoping Investigation (No-Go)

**Date:** 2026-04-17
**Status:** scoping / no-go  (Phase 2 of the mass-spectrum attack plan)
**Primary runner:** `scripts/frontier_mass_ratio_up_sector_nni_scoping.py`

## Safe statement

On the current live package surface the combination of
1. the promoted atlas CKM package (full `V` from `lambda, A, |V_ub|, delta`),
2. the bounded Phase-1 down-type ratios
   (`m_d/m_s = alpha_s(v)/2`, `m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5)`),
3. an NNI texture on `M_u` (zeros at `(0,0)` and `(0,2)`),

does **not** close the up-type mass-ratio extraction. The structural
obstruction is explicit and falsifiable: the least-squares residual on
the NNI constraints cannot be driven to zero on the
`(x_u, x_c, phi_a)` scan, and every package-native closed-form
candidate for `m_c/m_t` misses the PDG self-scale comparator by
`>= 10%`.

No observed quark masses are used as derivation inputs.

## What the runner establishes

| Part | Check | Outcome |
|---|---|---|
| 1 | atlas V is unitary and reproduces `|V_us|`, `|V_cb|`, `|V_ub|` | PASS |
| 2 | exact SU(3) exponent `C_F - T_F = 5/6`; `A^2 = 2/3` | PASS |
| 3 | Fritzsch-seed `M_d` closed form reconstructs Phase-1 ratios exactly | PASS |
| 4 | NNI-texture inversion scan over `phi_a in [0, 2*pi)` | PASS (scan completes; residual stays `> 1e-9`) |
| 5 | closed-form candidate enumeration for `m_c/m_t` | PASS (none lands within 10%) |
| 6 | chain-rule arithmetic is internally consistent | PASS |
| 7 | `m_t` from `y_t v / sqrt(2)` lands within 5.75% of PDG | PASS |
| 8 | provenance audit: no observed quark mass used as derivation input | PASS |

Total: **30 PASS / 0 FAIL** — all checks are scoping/investigation
milestones, not claimed-closure assertions. The runner is a clean
NO-GO record: it documents that the stated ingredients are
insufficient to close Phase 2 and enumerates what additional
structure would be required.

## Candidate closed-form table

With `|V_cb| = alpha_s(v)/sqrt(6)` and `A = sqrt(2/3)`:

| Candidate | Value | % of PDG m_c/m_t |
|---|---|---|
| `|V_cb|^(6/5)`  (sector-symmetric 5/6 bridge) | 0.02239 | 286.5% |
| `[A |V_cb|]^(6/5)`  (5/6 modulated by atlas A) | 0.01755 | 224.6% |
| `|V_cb|^(3/2)`  (3/2 exponent) | 0.00866 | 110.8% |
| `|V_cb|^2`  (Wolfenstein A^2 lambda^4) | 0.00178 | 22.8% |
| `alpha_s(v)/6`  (linear scaling) | 0.01722 | 220.3% |

PDG self-scale comparator `m_c/m_t ~ 0.00782`. The closest candidate is
`|V_cb|^(3/2)` at +10.8%, which is **not** a retained framework formula:
the exponent `3/2` does not correspond to any promoted Casimir or
anomalous-dimension relation on the current package surface.

## Why Phase 2 does not close here

Two structural causes are exposed:

1. **Over-determination of the NNI constraint system.**
   The atlas V is fully fixed by 4 real atlas inputs. The
   Phase-1 down-type mass ratios fix `M_d` up to one residual phase
   `phi_a` (the NNI texture alone leaves one degree of freedom beyond
   the three eigenvalues). The up-sector NNI texture imposes 3 real
   constraints on `(x_u, x_c, phi_a)`, giving a system of 3 constraints
   on 3 unknowns — formally determined. However the scan finds that
   the residual `|r|^2` has no zero in `[0, 2*pi)` with the
   Fritzsch-seed M_d: the best residual is O(1e-3), two orders of
   magnitude above solver tolerance. The system is thus generically
   over-determined once one accounts for the implicit unitarity
   constraints on U_d.

2. **Up-type hierarchy is dimensionally steeper than down-type.**
   The Phase-1 down-type formulas use the exact SU(3) exponent
   `5/6 = C_F - T_F`. The observed up-type `m_c/m_t ~ |V_cb|^1.53`,
   i.e. exponent near `3/2`, not `6/5`. This asymmetry is already
   known from the flavor literature as the y_t-vs-y_b RG-running
   asymmetry: up-type masses feel the large `y_t^2` anomalous dimension
   while down-type feel only `alpha_s`. The `5/6` bridge therefore
   cannot transplant to the up sector without modification.

## What would close Phase 2

Two routes are open:

**Route A — non-Fritzsch M_d.**
Relax the `(1,1) = 0` Fritzsch constraint on M_d, introducing a second
real residual beyond `phi_a`. The NNI-only M_d has 5 real parameters
fixed by 3 eigenvalues, leaving 2 residuals. Scanning both against the
3 up-sector NNI constraints on `(x_u, x_c)` would be over-determined by
1 — potentially still no-go, but the surface is larger. This has not
been exhaustively explored.

**Route B — y_t-specific RG anomalous dimension.**
If `y_t` promotes to the retained core (pending per gate status
2026-04-14), the up-sector `5/6`-analog exponent becomes
`(C_F - T_F + y_t^2/g_s^2 * gamma_y)` or similar, modifying the
bridge coefficient. This is the more physically motivated route.
It requires y_t promotion as a prerequisite.

## What is not claimed

- a retained or theorem-grade up-type mass-ratio extraction
- a bounded numerical prediction for `m_c/m_t`, `m_u/m_c`, or `m_u/m_t`
  (the best-fit values from the NNI inversion are degenerate, not physical)
- any revision to Phase 1 (which remains a bounded `PASS=23/0` lane)

## Inputs and bridge structure

Same as Phase 1 (see `docs/DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`), plus:

- full atlas V from `build_standard_ckm(lambda, A lambda^2, A lambda^3/sqrt(6), arctan(sqrt(5)))`
- Fritzsch-seed `M_d` via Branco-Lavoura-Silva closed form

## Validation

```bash
python3 scripts/frontier_mass_ratio_up_sector_nni_scoping.py
```

Expected: `TOTAL: PASS=30, FAIL=0`. All checks are scoping milestones;
a future closure runner would replace this one.

## Relation to the 5-phase plan

The plan file (`zesty-nibbling-pretzel.md`) positioned Phase 2 as
"up-type quark mass ratios from CKM inversion" with an expected BOUNDED
extraction similar in spirit to Phase 1. This runner documents that
the stated ingredients (atlas V + Phase 1 down-type + NNI texture) are
**insufficient**. Phases 3, 4, 5 (charged leptons, neutrinos, cosmology)
are downstream of Phase 2 and are not blocked by this no-go per se, but
they cannot use Phase 2 as a "solved" anchor. They must either:
- proceed with their own CKM-analog / PMNS-analog closures, or
- wait on Route B (y_t promotion) to re-open Phase 2.

The cleanest next-step for the broader mass-spectrum program is
therefore to pursue **Phase 3 (charged leptons)** directly — the
PMNS/leptonic CKM-analog is structurally different and may close
without the Phase 2 blocker.
