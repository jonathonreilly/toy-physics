# yt_ew Matching Rule M Stretch Attempt: Named Obstruction

**Date:** 2026-05-02
**Status:** stretch-attempt note + named obstruction packet on the EW current
matching rule M residual of `yt_ew_color_projection_theorem`. NOT
proposed_retained — see CLAIM_STATUS_CERTIFICATE.md. This note documents a
worked attempt to derive R_conn = 8/9 exactly for the physical EW current
from minimal premises (A_min) and isolates the named obstruction at the
non-perturbative singlet/disconnected coefficient.
**Primary runner:** `scripts/frontier_yt_ew_matching_rule_m_stretch.py`
**Authority role:** stretch-attempt deliverable per skill workflow #6
route type "no-go/obstruction"; deep block on a named hard residual.

## 0. The matching rule M residual

The audit verdict for `yt_ew_color_projection_theorem` flagged that the
**physical EW current → adjoint channel matching factor** is not derived
from minimal premises. The theorem promotes a universal package-level 9/8
EW coupling correction from R_conn, but the matching dependency only
supplies bounded large-N_c/OZI support and explicitly does not prove the
exact coefficient equality.

The matching rule M is the physical claim:

> Only the **connected/adjoint** color flow (= (N_c² − 1)/N_c² = 8/9 of the
> full color trace at N_c = 3) supplies the physical Higgs Yukawa
> renormalization; the **disconnected/singlet** piece (= 1/N_c² = 1/9) is
> absorbed into the Higgs VEV normalization.

This identifies R_conn (the physical/continuum quantity) with the
group-theoretic ratio (N_c² − 1)/N_c² **exactly**, beyond the bounded
large-N_c support already established in
`EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27`.

## 1. A_min — minimal allowed premise set

Per skill workflow #9, the stretch attempt declares a minimal premise set:

| Premise | Class | Source |
|---------|-------|--------|
| graph-first SU(N_c) integration with N_c = 3 | retained | `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` |
| 't Hooft 1/N_c topological expansion | standard QFT machinery | 't Hooft 1974, Coleman 1985 |
| Fierz identity for SU(N_c): N_c × N̄_c = 1 ⊕ (N_c²−1) | exact group theory (retained derived in PR #249) | `YUKAWA_COLOR_PROJECTION_THEOREM.md` + PR #249 |
| OZI rule: disconnected vector-current contributions suppressed by 1/N_c² | standard QFT machinery | Witten 1979, Coleman 1985 |
| Adler-Bell-Jackiw triangle anomaly machinery | standard QFT machinery | ABJ 1969 |

## 2. Forbidden imports

Per skill workflow #9, explicit forbidden inputs to this stretch attempt:

- **PDG observed y_t** (top Yukawa coupling)
- **PDG observed Higgs VEV** v ≈ 246 GeV
- **PDG observed m_H** Higgs mass
- **Fitted lattice empirical R_conn** (the runner-measured 0.888337 ± 0.001896)
- **Same-surface family arguments** (no use of α² conventions or sister-trace identities as proof inputs)
- **Literature numerical comparators** for R_conn beyond the leading-order
  group-theory ratio (N_c² − 1)/N_c² = 8/9 derived in PR #249

## 3. Worked attempt

### 3.1 The Higgs Yukawa color decomposition

The Higgs Yukawa term in SM is `−y_t H̄ Q̄_L t_R + h.c.`. The Higgs
self-energy from the t-quark loop involves a color trace over the t-quark
color indices.

Decompose the t-quark bilinear `t̄_a t^a` into singlet and adjoint channels
under SU(3)_c. Per Fierz:

```text
N_c × N̄_c  =  1  ⊕  (N_c² − 1)
3 × 3̄    =  1  ⊕  8     (at N_c = 3)
```

The singlet projector `P_s = (1/N_c) δ_a^a` and the adjoint projector
`P_adj = δ_a^b − (1/N_c) δ_a^a δ^b_a` satisfy:

```text
P_s + P_adj  =  I              (completeness)
Tr P_s       =  1              (singlet has 1 state)
Tr P_adj     =  N_c² − 1       (adjoint has N_c²−1 states)
```

The full color trace decomposes as:

```text
Tr_color [...]  =  Tr [P_s ⋅ ...]  +  Tr [P_adj ⋅ ...]
```

The fraction of the full trace in the adjoint channel is:

```text
R_adj  =  Tr P_adj / Tr I  =  (N_c² − 1) / N_c²  =  8/9   at N_c = 3.
```

This is the exact group-theory ratio. It is the result PR #249 derived for
the Fierz F-half.

### 3.2 The matching M claim restated

The matching rule M asserts:

```text
y_t^{phys}^2  =  R_adj × Σ_t^{full}  +  0 × Σ_v^{disc}
              =  (N_c²−1)/N_c² × Σ_t^{full}                       (M)
```

where Σ_t^{full} is the full t-loop self-energy and Σ_v^{disc} is the
disconnected (singlet) piece, claimed to renormalize v rather than y_t.

If (M) holds exactly, then `y_t^{phys}^2 / y_t^{lattice}^2 = (N_c²−1)/N_c²
= 8/9`, equivalently the EW coupling correction is `9/8`.

### 3.3 1/N_c topology of disconnected piece

Per `RCONN_DERIVED_NOTE.md` and `EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM`:

```text
Σ_t^{disc} / Σ_t^{full}  =  1/N_c²  +  O(1/N_c⁴)        (large-N_c bound)
```

This gives R_conn = 8/9 + O(1/81) as a **bounded** result at N_c = 3. The
O(1/81) ~ 1.2% correction is the next-order genus-2 contribution.

### 3.4 The named obstruction

For the matching rule M to hold **exactly** (with no O(1/N_c⁴) correction
at N_c = 3), one of the following must be true:

**(O1) The disconnected piece vanishes identically at all genus orders.**
This is **false**. Glueball intermediate states exist at any N_c ≥ 2; they
contribute at genus ≥ 1 with non-zero amplitude. The disconnected piece is
suppressed but not zero.

**(O2) The disconnected piece contributes only to v, not to y_t.**
This is the claimed matching rule itself, but it requires a non-perturbative
input. The decomposition `Σ_t^{full} = Σ_t^{conn} + Σ_t^{disc}` is
algebraic; the assignment of `Σ_t^{disc}` exclusively to v (rather than y_t)
is a **renormalization scheme choice**, not a derivation.

**(O3) An exact OZI-vanishing theorem at all genus orders.**
The standard OZI rule (Okubo 1963, Zweig 1964, Iizuka 1966) is a
**phenomenological** statement that disconnected diagrams in QCD are
suppressed beyond the 1/N_c² leading order. It is not an exact theorem —
even at N_c = ∞, the OZI rule has corrections.

### 3.5 Where the obstruction lives

The **exact** matching coefficient `(N_c² − 1)/N_c²` for the physical EW
current renormalization requires fixing the disconnected coefficient at
non-perturbative level. This is equivalent to:

1. Computing the full glueball spectrum and matrix elements `<0|J_EW|G>`
   for SU(N_c) gauge theory at the relevant scales — a hard non-perturbative
   problem.

2. Or providing an exact OZI-vanishing theorem at all genus orders — not
   available in standard QFT.

3. Or constructing a renormalization scheme in which the disconnected piece
   is by definition absorbed into v — but this is a scheme choice, not a
   derivation of the physical matching coefficient.

### 3.6 Sharper named obstruction

The matching rule M is **NOT exact at any finite N_c**. The sharpest honest
statement is:

```text
R_conn^{phys}  =  (N_c² − 1) / N_c²  +  O(1/N_c⁴)  at N_c ≥ 2
              =  8/9  +  bounded O(1/81)  ≈  8/9  ±  1.2%   at N_c = 3
```

This is **bounded support**, not exact retention. The package-level 9/8 EW
coupling correction is therefore a **bounded approximation** valid to ~1%
precision, not an exact derivation.

## 4. Status

```yaml
actual_current_surface_status: stretch_attempt + named_obstruction
conditional_surface_status: bounded support theorem at large-N_c (already documented in EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27)
hypothetical_axiom_status: |
  An exact matching M would require either:
    (a) an exact OZI-vanishing theorem at all genus orders, OR
    (b) a non-perturbative computation of the singlet/disconnected coefficient,
    OR
    (c) a renormalization scheme choice in which the disconnected piece is
        absorbed into v by definition.
  None of these is currently available as a derivation from minimal premises.
proposal_allowed: false
proposal_allowed_reason: |
  The matching rule M is not exact at finite N_c. The current best is bounded
  support at O(1/N_c⁴) precision. Retention as exact would require closing
  one of the obstructions above.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 5. What this stretch attempt closes

- **A clear named obstruction** for the matching rule M residual:
  - The disconnected (singlet) coefficient cannot be fixed exactly within
    standard QFT machinery (1/N_c expansion + OZI rule + ABJ machinery)
    without additional non-perturbative input.
  - The bounded-support tier (O(1/N_c⁴) ~ 1.2% at N_c = 3) is the narrowest
    honest tier currently available.
- **A_min and forbidden imports** are explicitly recorded for future stretch
  attempts.
- **Three concrete obstruction routes (O1, O2, O3)** are identified with
  their failure modes documented.

## 6. What this stretch attempt does NOT close

- An exact derivation of R_conn = 8/9 for the physical EW current matching.
  The bounded-support tier remains the honest current statement.
- The retention status of `yt_ew_color_projection_theorem` (still
  `audited_conditional`).
- The retention status of `rconn_derived_note` (still
  `audited_conditional`).

## 7. Validation

- primary runner:
  [`scripts/frontier_yt_ew_matching_rule_m_stretch.py`](../scripts/frontier_yt_ew_matching_rule_m_stretch.py)
  — verifies (a) the Fierz channel decomposition, (b) the bounded
  large-N_c result R_conn = (N_c²−1)/N_c² + O(1/N_c⁴) at exact rational
  precision for the leading term, (c) the three identified obstruction
  routes (O1, O2, O3) are each non-derivable from minimal premises within
  standard QFT machinery, and (d) explicit non-closure of the exact matching
  coefficient.

## 8. Cross-references

- [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md) — parent (M residual flagged in audit verdict)
- [`YUKAWA_COLOR_PROJECTION_THEOREM.md`](YUKAWA_COLOR_PROJECTION_THEOREM.md) — parent of audit verdict
- [`RCONN_DERIVED_NOTE.md`](RCONN_DERIVED_NOTE.md) — leading-order 1/N_c R_conn derivation (sister)
- [`EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md`](EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md) — bounded-support theorem (already documents the same bounded statement)
- PR #249 (merged) — Fierz-channel exact group-theory derivation
- PR #250 — cycle-cleanup integration
- 't Hooft 1974, Witten 1979, Coleman 1985, Manohar 1998 — standard 1/N_c references
