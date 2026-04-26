Not approved for `main` as submitted.

Why:

1. The claimed below-`W2` closure is still stronger than the branch actually proves.
   Route 1 uses the retained existence of `SU(2)_L` and `SU(3)_c` plus the
   external mathematical fact `dim_fund(SU(N)) = N`, then identifies those
   dimensions with the Wolfenstein `N_pair` / `N_color` counts. That yields a
   clean consistency equality

       dim_fund(SU(2)) / dim_fund(SU(3)) = 2/3 = A^2

   but it is not an independent retained theorem that the CKM count variables
   are sourced by those gauge-fundamental dimensions. Current `main` already
   carries the narrower honest version of this result under the retained
   lattice-scale EW/CKM bridge note.

2. Route 2 is explicitly only a numerical consistency, not a derivation.
   The note itself says `g_2^2 = 1/N_pair^2` is a retained-numerical
   consistency at the accepted values. That is useful corroboration, but it
   does not derive `N_pair = 2` from the EW lane below W2.

3. The runner replays cleanly, but it does not verify the stronger closure.
   It confirms status labels, then checks the already-assumed arithmetic with
   `A_sq_R6 = A_sq_R7 = A_sq_R8 = 2/3`. So `PASS=24` certifies compatibility
   of the claimed closure with the accepted values, not a new retained theorem
   that closes `A^2` below W2.

Replay status:

- `python3 -m py_compile scripts/frontier_ckm_a_squared_below_w2_y_quantum_closure.py`
- `python3 scripts/frontier_ckm_a_squared_below_w2_y_quantum_closure.py`
- result: `TOTAL: PASS=24, FAIL=0`

Current-main situation:

- The strongest honest retained content from this line is already on current
  `main` as the narrower lattice-scale bridge:

      sin^2(theta_W)|_lattice = A^4 = 4/9

- That existing retained note explicitly leaves

      A2_BELOW_W2_DERIVATION_CLOSED = FALSE

  and treats the gauge-dimension equality only as a retained consistency
  equality, not a below-`W2` derivation.

Landable resubmission path:

- If you want to resubmit, do it only if there is a new theorem identifying the
  Wolfenstein `N_pair` / `N_color` variables with the gauge-fundamental
  dimensions as a retained source theorem.
- Without that, the correct scope is already on `main`: the retained
  EW/CKM lattice-scale bridge plus the gauge-dimension consistency equality.
