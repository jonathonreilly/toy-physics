# Cycle 9 Claim Status Certificate — Pattern B Audit Companion (EW Fierz general N_c)

**Block:** physics-loop/ew-fierz-audit-companion-block09-20260502
**Companion runner:** scripts/audit_companion_ew_fierz_general_n_c_exact.py (PASS=28/0)
**Target row:** ew_current_fierz_channel_decomposition_note_2026-05-01 (audit_status: unaudited, td=297, claim_type: positive_theorem)

## Block type

**Pattern B — Audit-acceleration companion runner.** Not a new claim row, not a new source note. Provides exact-precision audit-lane evidence that the parent row's load-bearing step (Fierz channel-fraction identity F_adjoint = (N_c² − 1)/N_c²) is a class-(A) algebraic identity holding at general N_c, not a numerical coincidence at N_c = 3.

## Audit-lane positioning

The parent row's primary runner already verifies the Fierz identity at N_c = 3. This companion extends the verification to general N_c ∈ {2, 3, 4, 5, 7, 10, 100} at exact rational precision (sympy `Rational`), demonstrating the algebraic identity holds for any SU(N_c) without numerical fitting.

Audit-lane class for parent row's load-bearing step (per AUDIT_AGENT_PROMPT_TEMPLATE.md rubric):
- **(A)** — algebraic identity / dimension-counting on irreducible SU(N_c) representations.

No new claim_type assertion; this companion supports the parent row's existing claim_type=positive_theorem.

## What this packet does

- Provides exact rational verification of F_singlet + F_adjoint = 1, F_adjoint = (N_c² − 1)/N_c², dim decomposition N_c² = 1 + (N_c²−1) at multiple N_c values.
- Verifies parent row's deps (native_gauge_closure_note retained_bounded, graph_first_su3_integration_note retained_bounded) are still retained-grade via live ledger lookup.

## What this packet does NOT do

- Does not create a new claim row.
- Does not modify the parent source note.
- Does not propose a new claim_type for any row.
