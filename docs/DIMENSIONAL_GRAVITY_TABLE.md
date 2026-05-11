# Dimensional Gravity Table

**Status:** bounded finite-entry inventory. This note tabulates point-tested
**Claim type:** bounded_theorem
results on the listed family/parameter rows. It does NOT claim universality
across all dimensions, all h values, or all parameter variations. The bolded
"1.00" entries are point-tested results, not universality theorems. (NARROWED
2026-05-02 in response to audit verdict requesting a finite-scope reframing.)

**Date:** 2026-04-04 (NARROWED 2026-05-02; CERTIFICATE RUNNER ADDED 2026-05-03;
CACHED-ARTIFACT ASSERTIONS ADDED 2026-05-09; STALE BORN ENTRY RECONCILED
2026-05-10)

**Audit-conditional perimeter (2026-05-10):**
The current generated audit ledger records this row `audited_failed` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
bounded_theorem`. The audit chain-closure explanation is exact: "The
note's central table does not match the cache-backed runner output:
the d=3 table reports Born <4e-15, while C6 asserts the registered 3D
cache value Born = 4.20e-15. A bounded finite-entry inventory cannot
be clean while displayed row numerics are stale relative to the
supplied runner evidence." This rigorization edit only updates the
displayed d=3 Born entry to match the registered cache value
(`4.20e-15`) cited verbatim by the certificate-runner C6 assertion;
no other table values are touched, no audit_status is promoted, and
the certificate runner's assertion list is unchanged. The d=4 Born
entry was already in cache-backed form (`4.43e-15` for the W=8 frozen
companion log via C7); this edit just brings the d=3 row into the
same form. The generated audit ledger remains the authority for any verdict; this is the
cache-reconcile repair the verdict prescribed.
**Action:** Valley-linear S = L(1-f)
**Kernel:** 1/L^(d-1) with h^(d-1) measure

**Primary runner:** [`scripts/dimensional_gravity_table_certificate_runner_2026_05_03.py`](../scripts/dimensional_gravity_table_certificate_runner_2026_05_03.py) (structural certificate plus per-row cached-artifact assertions, PASS=7/7)

**Companion runner:** [`scripts/dimensional_gravity_card.py`](../scripts/dimensional_gravity_card.py) — slow lattice card, invoke with `--dim 3` or `--dim 4` to reproduce individual table rows; unsuitable as the audit-lane runner because of runtime.

### Registered cached artifacts (load-bearing for the per-row entries)

The d=3 and d=4 rows below are backed by SHA-pinned runner caches and a
frozen companion log. The certificate runner above parses these and
asserts the table's per-row values (Born, F∝M, distance tail, TOWARD
counts) appear in the registered artifacts:

- d=3 row → [`logs/runner-cache/same_family_3d_closure.txt`](../logs/runner-cache/same_family_3d_closure.txt)
  (cache of [`scripts/same_family_3d_closure.py`](../scripts/same_family_3d_closure.py); freezes Born=4.20e-15, F∝M=1.00, distance tail b^(-0.93), TOWARD gravity, decoherence ≈ 50% on the h=0.25, W=10, L=12 family)
- d=4 row (W=5..7 ladder) → [`logs/runner-cache/four_d_distance_width_probe.txt`](../logs/runner-cache/four_d_distance_width_probe.txt)
  (cache of [`scripts/four_d_distance_width_probe.py`](../scripts/four_d_distance_width_probe.py); records the W=7, h=0.5, L=15 row's TOWARD support 6/6, peak at z=4, far-tail b^(-0.96))
- d=4 W=8 companion → [`logs/2026-04-04-4d-wide-distance-law.txt`](../logs/2026-04-04-4d-wide-distance-law.txt)
  (frozen single-run log: Born=4.43e-15, F∝M=1.00, TOWARD 6/6 over z=2..7, early tail b^(-0.54))

### Cached companion-runner stdout (partial, load-bearing for F∝M point checks)

- [`logs/dimensional_gravity_card_d3_2026-05-08.txt`](../logs/dimensional_gravity_card_d3_2026-05-08.txt) — d=3 run reaching steps 1–5: Born=4.42e-15 [PASS], d_TV=0.8366, k=0=0 [PASS], **F∝M=1.00**, Gravity=+0.000232 (TOWARD).
- [`logs/dimensional_gravity_card_d4_2026-05-08.txt`](../logs/dimensional_gravity_card_d4_2026-05-08.txt) — d=4 run reaching steps 1–5: Born=4.36e-15 [PASS], d_TV=0.7964, k=0=0 [PASS], **F∝M=1.00**, Gravity=+0.000071 (TOWARD).

These cached partial runs back the bolded **F∝M=1.00** entries the auditor
flagged, plus Born and gravity-sign on both d=3 and d=4. The remaining
companion-runner steps (decoherence, distance-law tail fit) were not reached
within this session's wall-time budget and are still backed only by the
structural certificate runner. A future audit-lane compute pass should run
`dimensional_gravity_card.py --dim {3,4}` to completion to attach those
columns explicitly.

## Review-loop runner attachment (2026-05-03; cache assertions added 2026-05-09)

The 2026-05-03 audit flagged that the table's bolded "1.00" entries were
asserted by prose with no executable runner attached at the audit-packet
level. The 2026-05-03 repair added the structural certificate runner
above, which verifies the table's *invariants* (kernel/field/measure
powers, Newtonian targets per d, the linear-mass identity for
valley-linear S=L(1-f), the sqrt-mass identity for spent-delay, and the
4D width-limited honest read) without requiring a long lattice card to
run inside the audit window.

The 2026-05-05 audit verdict (audited_conditional) further requested
that the per-row lattice measurements themselves be inspectable in the
restricted packet, not just structurally argued. The 2026-05-09 repair
adds per-row cached-artifact assertions (C6, C7) to the same runner:
C6 parses the 3D row's SHA-pinned same-family cache and asserts
Born=4.20e-15, F∝M=1.00, distance tail b^(-0.93), TOWARD gravity, and
≈50% decoherence; C7 parses the 4D row's SHA-pinned width-ladder
cache and the frozen W=8 companion log and asserts the W=7 TOWARD
support 6/6, the W=8 Born=4.43e-15, F∝M=1.00, TOWARD 6/6, and the
early-tail b^(-0.54). The slow companion runner remains the source for
arbitrary new (d, kernel, h, lattice family) rows outside the
registered cache set.

## Tested entries

The following table reports point-tested results on the listed (d, kernel,
h, lattice family) rows only. Each "1.00" is a finite measurement at the
listed parameter point with the listed measurement quality, not a
universality claim.

The d=3 and d=4 rows are backed by registered cached artifacts (see
"Registered cached artifacts" above) and asserted by the certificate
runner. The d=2 row is **diagnostic-only / supporting**: no registered
audit-lane cache backs the d=2 numerical entries inside the restricted
packet, so the d=2 row is recorded here for context only and does not
carry a supported per-entry numerical claim.

| d | Kernel | F∝M | Distance tail | Born | Decoh | TOWARD | Status |
|---|--------|-----|---------------|------|-------|--------|--------|
| 2 | 1/L | 1.00 (point) | varies (2D = log) | <6e-16 | →50% | 7/7 at h≤0.5 | diagnostic-only / supporting (no registered cache) |
| 3 | 1/L² | **1.00** (point) | **b^(-0.93)** | 4.20e-15 | →50% | 8/8 at h≤0.5 | cache-backed (`same_family_3d_closure.txt`) |
| 4 | 1/L³ | **0.99-1.00** (point) | bounded, width-limited (`W=7:-0.96`, `W=8:-0.54` companions) | 1.5e-15 .. 4.4e-15 | TBD | `3/3 .. 6/6` at h=0.5 | cache-backed (`four_d_distance_width_probe.txt` + frozen W=8 log) |

The table above covers `d in {2, 3, 4}`, kernel = `1/L^(d-1)`, valley-linear
action `S = L(1-f)`, with `h <= 0.5` for d=2,3 and `h = 0.5` for d=4. No
entries are reported outside that scope. Only the d=3 and d=4 rows have
their numerical entries asserted from registered artifacts in the audit
packet; the d=2 row is supportive context, not a load-bearing audit
claim.

## Newtonian predictions

| d | Newtonian deflection | Model (valley-linear) | Match? |
|---|---------------------|----------------------|--------|
| 2 | ln(b) | varies with h | consistent |
| 3 | 1/b | b^(-0.93) | **yes (~7% off)** |
| 4 | 1/b² | supportive but width-limited | needs wider lattice |

## Key properties on the tested entries

**Linear mass scaling F∝M ≈ 1.00 holds on every cache-backed tested row
above (d=3, d=4 W=7, d=4 W=8 companion).** This is a finite-entry
observation across the listed (d, kernel, h, family) points, not a
universality theorem across all dimensions, all h values, or all
parameter choices. The d=2 entry is supportive context only and not a
cache-backed audit claim. No theorem in this note proves F∝M = 1
outside the tabulated scope. Future work could attempt that
universality theorem; this note does not.

**Decoherence is action-independent on the tested rows.** Valley-linear and
spent-delay give identical d_TV, MI, CL purity at the tested h points.
Decoherence depends on geometry, not the action formula. (Tested entries
only; the cache-backed support is the d=3 row's `same_family_3d_closure.txt`
≈50% decoherence read.)

**Born holds at machine precision on the cache-backed tested rows.** This
is a mathematical property of the linear propagator on the tested
(d, kernel, h, family) points (d=3 Born=4.20e-15 in the registered 3D
cache; d=4 W=8 Born=4.43e-15 in the frozen W=8 companion log).

## Spent-delay comparison

| Property | Spent-delay | Valley-linear |
|----------|------------|---------------|
| F∝M | 0.50 (√M) | **1.00 (linear)** |
| 3D distance | b^(-0.52) | **b^(-0.93)** |
| Decoherence | identical | identical |
| Born | identical | identical |
| Gravity sign | identical | identical |

The ONLY difference is the mass/distance scaling. Everything else
is the same because decoherence and Born don't depend on the action.

## Update: Dimensional field profile (2026-04-04)

The field profile must also scale with dimension:
  f = s / r^(d-2) where d = number of spatial dimensions

| d | f(r) | Newtonian deflection | Measured tail |
|---|------|---------------------|---------------|
| 3 | s/r | 1/b | b^(-0.93) |
| 4 | s/r² | 1/b² | b^(-0.29) (early, W=7) |

The 4D tail is still at an early stage. The current frozen width note keeps
`W = 5..7`, and a heavier raw `W = 8` companion strengthens the support but
does not yet close the asymptotic law.

The complete dimensional prescription:
  Kernel: 1/L^(d-1)
  Field: s/r^(d-2)
  Action: S = L(1-f)
  Measure: h^(d-1)

All four ingredients scale with dimension d.

## 4D distance law frozen result (2026-04-04)

4D W=7, L=15, h=0.5, field f=s/r^2, valley-linear + 1/L^3:

| z | deflection | direction |
|---|-----------|-----------|
| 2 | +0.0000424 | TOWARD |
| 3 | +0.0000708 | TOWARD |
| 4 | +0.0000762 | TOWARD (peak) |
| 5 | +0.0000740 | TOWARD |
| 6 | +0.0000674 | TOWARD |

Tail from peak (z>=4): b^(-0.29), R²=0.884, 3 points
Far tail (z>=5): b^(-0.51), 2 points

This is at the SAME early stage as 3D when it showed -0.35
(which later improved to -1.07 at W=12). The 4D tail needs
W>=10 (~3M nodes in 4D) for a definitive measurement.

The honest read: 4D gravity is TOWARD with the correct field
profile and near-Newtonian mass scaling (F∝M=0.99), but the
distance exponent is unresolved due to lattice width limits.

Heavier same-family raw companion:

- `W = 8`, `L = 15`, `h = 0.5`
- Born: `4.43e-15`
- `F∝M = 1.00`
- `6/6` TOWARD on `z = 2..7`
- early tail from `z >= 4`: `b^(-0.54)`

That row is supportive, but still width-limited.
