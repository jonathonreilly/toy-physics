# PR #230 No-Orthogonal-Top-Coupling Selection-Rule No-Go

**Status:** exact negative boundary / no-orthogonal-top-coupling selection rule not derived  
**Runner:** `scripts/frontier_yt_no_orthogonal_top_coupling_selection_rule_no_go.py`  
**Certificate:** `outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json`

## Purpose

The target-time-series Higgs-identity no-go leaves one possible escape: prove
that every scalar orthogonal to the canonical Higgs radial mode has zero top
coupling.  This block tests whether the current PR #230 substrate labels supply
that selection rule.

## Result

They do not.  The runner constructs a charge-table witness with two neutral
scalars:

- `h`, the canonical Higgs radial mode;
- `chi`, an orthogonal neutral scalar.

Both have the same listed current-surface quantum numbers: spin zero, color
singlet, electric charge zero, trivial `Z3` translation character, neutral
Cl(3) scalar carrier, and even CP.  The top bilinear has the same scalar
singlet labels.  Therefore any selection rule based only on those labels that
allows `h tbar t` also allows `chi tbar t`.

This does not prove an orthogonal scalar exists in the retained theory.  It
proves the current authority surface has not derived the rule needed to set
its top coupling to zero.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It
does not assume `y_chi = 0`, does not set `kappa_s = 1`, and does not use
`H_unit`, `yt_ward_identity`, observed top mass, observed `y_t`, `alpha_LM`,
plaquette, or `u0` as proof authority.

## Next Action

Derive a retained charge/representation theorem that distinguishes all
orthogonal neutral scalar modes from the Higgs radial mode, or measure the
orthogonal coupling/source-pole purity directly.
