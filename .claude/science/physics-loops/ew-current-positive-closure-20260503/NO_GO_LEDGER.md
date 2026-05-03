# No-Go Ledger

## Existing Gate No-Go

`EW_CURRENT_MATCHING_RULE_OPEN_GATE_NOTE_2026-05-03.md`:

- Fierz fixes `F_adj=8/9`.
- CMT scales singlet and adjoint uniformly.
- OZI supplies bounded suppression only.
- `kappa_EW=0` and `kappa_EW=1` share the retained primitive signature but give
  different EW factors.

## Prior Stretch No-Go

`YT_EW_M_RESIDUAL_STRETCH_ATTEMPT_NOTE_2026-05-02.md`:

- The naive claim that CMT absorbs `S` and leaves `C` is false.
- Channel bookkeeping shows `S` and `C` both inherit `u_0^2`.

## New Block No-Go

`EW_CURRENT_TRACELESS_GENERATOR_SELECTOR_NO_GO_NOTE_2026-05-03.md`:

- `Tr_internal(Q_EW)=0` kills the Wick-disconnected product
  `<J_EW(x)><J_EW(y)>`.
- The gate's missing coefficient multiplies color Fierz singlet `S` inside the
  same-line connected two-current contraction.
- That term is weighted by `Tr_internal(Q_EW^2)`, which is nonzero.
- Exact counterexample: `Q_EW=T3`, `M=I_color`, `N_c=3` gives nonzero singlet
  contribution `3/2` and zero adjoint contribution.
