# Historical CKM Mass-Basis NNI Note: V_ub from Schur Complement + Mass-Ratio Suppression

**Status (effective 2026-05-16):** historical bounded CKM route note. Re-audited
2026-05-05 as `audited_numerical_match` (class G); see
[AUDIT_LEDGER](../../audit/AUDIT_LEDGER.md) entry
`work_history.ckm.ckm_mass_basis_nni_note`. This file is NOT a live
authority. It is retained as a route-history / diagnostic note.

**Script:** `scripts/frontier_ckm_mass_basis_nni.py`

**Cites (for context, not load-bearing):** `CKM_SCHUR_COMPLEMENT_THEOREM`,
`CABIBBO_BOUND_NOTE.md`, `JARLSKOG_PHASE_BOUND_NOTE.md`.

**Publication disposition:** bounded flavor companion only. Not on the
retained flagship claim surface (see
[DERIVATION_ATLAS](../../publication/ci3_z3/DERIVATION_ATLAS.md), row "CKM
mass-basis route").

---

## What this note actually certifies (the scoped bounded statement)

The companion runner certifies four pure-algebra source theorems that hold
identically for ANY positive masses and ANY positive geometric-mean
coefficients. These are the only theorem-grade content of the note.

Let `m_1 < m_2 < m_3` be any positive reals and let `(c_12, c_23)` be any
positive geometric-mean NNI off-diagonal coefficients in the Hermitian NNI
mass matrix `M_ij = c_ij * sqrt(m_i * m_j)`. Define the mass-eigenvalue
NNI normalization (Branco-Lavoura-Silva, "CP Violation," Ch. 6):

    c_ij^phys = c_ij^geom * sqrt(m_i / m_j)    for i < j.

Then:

- **(T1) Chain rule.** `sqrt(m_1/m_3) = sqrt(m_1/m_2) * sqrt(m_2/m_3)`.
- **(T2) Geometric Schur normalization.**
  `M_13^geom / (M_12^geom * M_23^geom) = 1/m_2`.
- **(T3) `geom -> phys` is closed under (T1).**
  `c_13^phys = c_12^phys * c_23^phys`.
- **(T4) Gap-closure ratio is exactly `sqrt(m_1/m_3)`.**
  `c_13^phys / c_13^geom = sqrt(m_1/m_3)`, independent of `(c_12, c_23)`.

The runner verifies (T1)-(T4) at machine precision over 200 random
ordered mass triples in Part 0. No PDG input, no quark mass, no fitted
coefficient is touched in that block.

---

## What this note imports (and therefore does NOT derive)

The runner also evaluates (T1)-(T4) on PDG inputs and reports a
numerical correspondence with PDG CKM values. The illustration uses:

- **PDG 2024 quark masses** (`M_UP`, `M_CHARM`, ..., `M_BOTTOM`).
- **Fitted O(1) geometric-mean NNI coefficients**
  (`C12_U_FIT = 1.48`, `C23_U_FIT = 0.65`, `C12_D_FIT = 0.91`,
  `C23_D_FIT = 0.65`), themselves fitted to observed CKM mixing angles
  in `scripts/frontier_ckm_schur_complement.py` and imported here.
- **PDG 2024 CKM comparators** (`V_US_PDG`, `V_CB_PDG`, `V_UB_PDG`,
  `J_PDG`, `LAMBDA_PDG`, `A_PDG`, `RHO_BAR_PDG`, `ETA_BAR_PDG`).

The 2026-05-05 audit verdict (`audited_numerical_match`, class G) is
correct on this point: the headline "`|V_ub|_pred = 1.14x PDG`" in the
calibrated illustration is a numerical match under imported inputs, not
a first-principles closure from any retained axiom. The 2026-05-16
patch keeps the calibrated block for diagnostic continuity but
brackets it as imports-dependent and separates it from the structural
source theorems above.

---

## Safe claim boundary

### Safe to say

- The four structural identities (T1)-(T4) hold identically for any
  positive masses and any positive geometric-mean coefficients in the
  Hermitian NNI mass matrix.
- In particular, applying the mass-eigenvalue normalization
  `c_ij^phys = c_ij^geom * sqrt(m_i/m_j)` to a Schur-complement-induced
  `c_13^geom = c_12 * c_23` rescales the (1,3) off-diagonal exactly by
  the factor `sqrt(m_1/m_3)`, independent of (c_12, c_23).
- Evaluated on imported PDG 2024 quark masses and imported fitted O(1)
  geometric-mean NNI coefficients, the resulting `|V_ub|_pred` lies
  within about 14% of the PDG 2024 central value. This is a numerical
  consistency check, useful as a diagnostic.

### NOT safe to say

- That this note derives the CKM matrix from framework axioms.
- That this note derives the quark mass hierarchy. (The runner imports
  PDG masses; the prior claim that "all mass ratios are framework-derived"
  via an EWSB cascade was not backed by any runner-level instantiation
  of such a cascade and has been removed from this revision.)
- That the bounded `1.14x` numerical match upgrades the lane status; it
  does not, and the audit ledger row remains `audited_numerical_match`
  (class G) under this patch.
- That the calibrated block exhibits a first-principles closure of
  Wolfenstein parameters. The Wolfenstein correspondence in Part 6 is
  a numerical match under imports, conditional on the same fitted O(1)
  coefficients.

---

## Source-theorem table (machine-precision algebraic checks)

| ID | Statement | Class | Where verified |
|----|-----------|-------|----------------|
| T1 | `sqrt(m_1/m_3) = sqrt(m_1/m_2) * sqrt(m_2/m_3)` for any `m_i > 0` | algebraic identity | runner Part 0 (200 random triples) |
| T2 | `M_13^geom / (M_12^geom * M_23^geom) = 1/m_2` in the NNI parametrization | algebraic identity | runner Part 0 (200 random triples) |
| T3 | `c_13^phys = c_12^phys * c_23^phys` under the geom->phys map | algebraic identity (corollary of T1) | runner Part 0 + Parts 1, 2 |
| T4 | `c_13^phys / c_13^geom = sqrt(m_1/m_3)` independent of `(c_12, c_23)` | algebraic identity | runner Part 0 (200 random triples) |

All four pass at worst relative deviation `< 1e-12` on the random sample.

---

## Calibrated illustration (imports-dependent; NOT load-bearing)

The remaining sections of the runner evaluate (T1)-(T4) at PDG and
fitted-coefficient inputs and tabulate the resulting CKM-like numbers.
These are kept for continuity with the older note but should not be
read as a derivation:

- **Mass-ratio suppression factors** at PDG inputs: `sqrt(m_d/m_b) ~ 0.033`,
  `sqrt(m_u/m_t) ~ 0.0035` (both pure consequences of PDG imports + T1).
- **Mass-basis coefficients** at PDG and fitted-coefficient inputs:
  `c_13^phys(down) ~ 0.020`, `c_13^phys(up) ~ 3.4e-3`.
- **CKM comparison table** at imports:

  | Element | Mass-basis NNI (at imports) | PDG | Ratio | Status |
  |---------|-----------------------------|-----|-------|--------|
  | `|V_us|` | 0.2251 | 0.2243 | 1.004 | numerical match (imports) |
  | `|V_cb|` | 0.0420 | 0.0422 | 0.994 | numerical match (imports) |
  | `|V_ub|` | 0.00435 | 0.00382 | 1.14  | numerical match (imports) |
  | `J`      | 4.5e-6 | 3.1e-5 | 0.15  | bounded (imports) |

  Read every entry as `(operation T1-T4) applied to (PDG mass imports +
  fitted geometric-mean coefficient imports)`. No row is a first-principles
  derivation from retained axioms.

- **Gap-closure scan** (Part 5): a numerical scan of `c_13` from the
  geometric-mean value down to the mass-basis value, showing that the
  geometric-mean overshoot factor (`5.3x` PDG) collapses to `1.14x` PDG
  exactly when `c_13` is multiplied by `sqrt(m_1/m_3)`. This is (T4)
  evaluated at imports.

---

## Open issues (NOT addressed by this patch)

1. **Jarlskog invariant.** `J` is suppressed by ~7x relative to PDG in
   the calibrated block. See
   [JARLSKOG_PHASE_BOUND_NOTE](JARLSKOG_PHASE_BOUND_NOTE.md) for the
   currently-active bounded Jarlskog statement on the publication surface.

2. **`rho_bar` and `eta_bar`.** These Wolfenstein parameters are off in
   the calibrated block (`rho_bar` too large, `eta_bar` too small),
   related to the `J` suppression.

3. **No framework derivation of the geometric-mean coefficients
   `(c_12, c_23)`.** Until such a derivation is in hand, every entry of
   the calibrated illustration block remains imports-conditional.

4. **No framework derivation of the quark mass hierarchies.** The earlier
   prose claim that "the EWSB cascade gives the mass hierarchy from
   loop suppressions" is not instantiated by this runner and was
   removed in the 2026-05-16 patch.

Closing any of (3) or (4) at retained-axiom grade would be required to
upgrade the lane status; this patch does not attempt either.

---

## 2026-05-16 patch (audit response)

Audit row: `work_history.ckm.ckm_mass_basis_nni_note`
(`audited_numerical_match`, class G, auditor
`codex-cli-gpt-5.5-20260505-040942-beec6e04`, independence `cross_family`).

Auditor-quoted load-bearing step:
"The conversion `c_ij^phys = c_ij^geom * sqrt(m_i/m_j)` for `i < j`
applies the quark mass-ratio suppression that brings `|V_ub|` near PDG."

Auditor rationale (excerpt): "The runner performs real matrix and ratio
computations, but those computations are over hard-coded external quark
masses, PDG comparator values, and fitted geometric coefficients. The
quoted 1.14x `|V_ub|` agreement is therefore a numerical match after
importing calibrated inputs, not a first-principles closure from the
axiom. The runner source does not instantiate the claimed framework
operators or derive the mass hierarchy internally, despite the note
saying the mass ratios are framework-derived."

This patch addresses the audit at the note + runner level by:

  (P1) **Scope reduction to source theorems (T1)-(T4).** The runner now
       begins with a Part 0 block that verifies the four structural
       identities at machine precision over 200 random ordered mass
       triples and random positive O(1) coefficients. These are
       axiom-free algebraic identities; no PDG input is read.

  (P2) **Explicit source-citation of every import.** The runner header
       and the constants block now mark every numerical constant as an
       external import: PDG 2024 quark masses, PDG 2024 CKM comparators,
       and the fitted O(1) coefficients lifted from
       `scripts/frontier_ckm_schur_complement.py`. The note's "What this
       note imports" section repeats the same enumeration.

  (P3) **Removal of the false "framework-derived" prose.** The earlier
       sentences asserting that the mass hierarchy is supplied by an
       EWSB cascade have been removed both from the note and from the
       runner's Part 1 commentary. The EWSB-cascade `ALPHA_S_PL`,
       `ALPHA_2_PL`, `M_PL`, `V_EW`, `SIN2_TW`, `C_F`, `N_C`
       parameters were unused in the actual computation and have been
       removed from the runner.

  (P4) **Honest framing of Parts 1-7 as an imports-dependent
       illustration.** Each subsequent block now declares its inputs and
       reframes its checks as evaluations of (T1)-(T4) at imports.
       The Wolfenstein block (Part 6) is relabeled "Wolfenstein
       correspondence" rather than "Wolfenstein identification" and no
       longer asserts that the parametrization is derived.

  (P5) **Safe-to-say / NOT-safe-to-say block.** Added above, mirroring
       the format used in
       [JARLSKOG_PHASE_BOUND_NOTE](JARLSKOG_PHASE_BOUND_NOTE.md).

The class-G `audited_numerical_match` status is unchanged by this
patch; the patch removes the runner-level and prose-level discretion
the audit objected to, but does not attempt the structural derivation
(of either the geometric-mean coefficients or the mass hierarchy) that
would be required to upgrade the lane.

---

## Pointers

- Live bounded Cabibbo authority: [CABIBBO_BOUND_NOTE](CABIBBO_BOUND_NOTE.md).
- Live bounded Jarlskog statement: [JARLSKOG_PHASE_BOUND_NOTE](JARLSKOG_PHASE_BOUND_NOTE.md).
- Retained Schur-complement source theorem:
  [CKM_SCHUR_COMPLEMENT_THEOREM](../../CKM_SCHUR_COMPLEMENT_THEOREM.md).
- Runner: [scripts/frontier_ckm_mass_basis_nni.py](../../../scripts/frontier_ckm_mass_basis_nni.py).
- Cached runner output:
  [logs/runner-cache/frontier_ckm_mass_basis_nni.txt](../../../logs/runner-cache/frontier_ckm_mass_basis_nni.txt).
