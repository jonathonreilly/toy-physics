# Cycle 9 Claim Status Certificate — Pattern B Audit Companion (EW Fierz general N_c)

**Block:** physics-loop/ew-fierz-audit-companion-block09-20260502
**Companion runner:** scripts/audit_companion_ew_fierz_general_n_c_exact.py (PASS=42/0)
**Target row:** ew_current_fierz_channel_decomposition_note_2026-05-01

## Block type

**Pattern B — Audit-acceleration companion runner.** Not a new claim row, not a new source note, and not an audit verdict. Provides exact-precision companion evidence that the parent row's load-bearing step (Fierz channel-fraction identity F_adjoint = (N_c² − 1)/N_c²) is a class-(A) algebraic identity, not a numerical coincidence at N_c = 3.

## Audit-lane positioning

The parent row's primary runner already verifies the Fierz identity at N_c = 3. This companion adds a symbolic identity check, exact rational samples at N_c ∈ {2, 3, 4, 5, 7, 10, 100}, and explicit normalized-generator Fierz-completeness checks for SU(2), SU(3), and SU(4). That supports the algebraic boundary without numerical fitting.

Audit-lane class for parent row's load-bearing step (per AUDIT_AGENT_PROMPT_TEMPLATE.md rubric):
- **(A)** — algebraic identity / dimension-counting on irreducible SU(N_c) representations.

No new claim_type assertion; this companion supports the parent row's existing audit-ledger row without changing its status.

## What this packet does

- Provides symbolic and exact rational verification of F_singlet + F_adjoint = 1, F_adjoint = (N_c² − 1)/N_c², and dim decomposition N_c² = 1 + (N_c²−1).
- Verifies parent row's load-bearing deps are still graph-visible and satisfy review-loop dependency-closure policy via live ledger lookup.

## What this packet does NOT do

- Does not create a new claim row.
- Does not modify the parent source note.
- Does not propose a new claim_type for any row.
