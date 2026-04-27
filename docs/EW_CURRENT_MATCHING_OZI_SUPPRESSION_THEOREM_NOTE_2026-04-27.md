# EW Current Matching via OZI / Disconnected-Trace Suppression Theorem

**Date:** 2026-04-27
**Status:** bounded support theorem for EW current matching on the standard 1/N_c expansion surface
**Primary runner:** `scripts/frontier_color_projection_mc.py`
**Depends on:**
[RCONN_DERIVED_NOTE.md](RCONN_DERIVED_NOTE.md),
[YT_EW_COLOR_PROJECTION_THEOREM.md](YT_EW_COLOR_PROJECTION_THEOREM.md)

---

## Statement

**Support theorem (EW disconnected-current suppression at leading order in 1/N_c).**
On the unified `Cl(3) / Z^3` lattice with `N_c = 3` quarks in the
fundamental representation, the physical (continuum-matched) EW vacuum
polarization equals the **connected** color trace plus corrections of
order `1/N_c^2`:

    Pi_EW^{phys} = Pi_EW^{conn} * (1 + O(1/N_c^2))

The disconnected piece — quark-antiquark annihilation through a pure-
gluon (colorless) intermediate state — is **OZI-suppressed by `1/N_c^2`**
relative to the connected piece. This is the same large-`N_c` topology
family that supports the connected-channel ratio
`R_conn = (N_c^2 - 1)/N_c^2 + O(1/N_c^4)`, but it does not by itself
fix the non-perturbative disconnected coefficient.

Equivalently: at leading order in `1/N_c`, the physical EW coupling
extracted from `Pi_EW^{phys}` is bounded toward the connected color
trace rather than the total color trace. The canonical package readout
uses the sibling `R_conn` value:

    alpha_EW^{phys} / alpha_EW^{lattice} = N_c^2 / (N_c^2 - 1) = 9/8 at N_c = 3

as a bounded matching model, not as an exact coefficient derived by this
note alone.

This addresses the matching-rule gap flagged on
[YT_EW_COLOR_PROJECTION_THEOREM.md](YT_EW_COLOR_PROJECTION_THEOREM.md):
the connected-trace route now has an explicit large-`N_c` support
argument. It remains a bounded support input until an independent
derivation fixes the disconnected coefficient required for exact
`9/8` matching.

## Why this is needed

The audit lane traced the 9/8 correction back to a chain of three
distinct claims:

1. `R_conn = (N_c^2 - 1)/N_c^2` is the connected color trace ratio.
2. R_conn equals 8/9 at N_c = 3.
3. **The physical EW coupling reads off the connected (not total) trace.**

Claims (1) and (2) are derived in
[RCONN_DERIVED_NOTE.md](RCONN_DERIVED_NOTE.md) via the 't Hooft 1/N_c
expansion. Claim (3) — the **matching rule** — was previously asserted
in YT_EW_COLOR_PROJECTION_THEOREM.md Section 2.6 ("The physical claim:
the 9/8 correction arises if the physical EW current uses the connected
color trace") without an independent derivation.

This note fills part of that third step. The connected-trace preference
follows from the same 1/N_c topological mechanism that gives R_conn,
applied to the EW vacuum polarization directly rather than to the
q-qbar propagator. The exact coefficient identification with `1/R_conn`
remains an additional package assumption.

## Derivation

### 1. The two contributions to Pi_EW

Let `J_EW^μ` be the EW current built from quark bilinears
`J_EW^μ ~ q-bar_a γ^μ T_EW q^a` summed over colors `a`. The vacuum
polarization is the two-point function:

    Pi_EW^{μν}(q) = i ∫ d^4 x e^{iqx} <0| T J_EW^μ(x) J_EW^ν(0) |0>

Wick-contracting the four quark fields gives two topologies:

**Connected piece (`Pi_EW^{conn}`).** The two `J_EW` insertions are
joined by a single quark loop. Color flows continuously from one
insertion to the other through the quark line plus any gluon dressing.

**Disconnected piece (`Pi_EW^{disc}`).** The two `J_EW` insertions
each have their own closed quark loop. The two loops are joined only
through gluons. The intermediate state between the two insertions is
a pure-glue (color-singlet) configuration — i.e., a glueball.

The full vacuum polarization is the sum:

    Pi_EW^{full} = Pi_EW^{conn} + Pi_EW^{disc}

### 2. The disconnected piece factors through a colorless intermediate

By construction, `Pi_EW^{disc}` factorizes as:

    Pi_EW^{disc} ~ <0| J_EW^μ |G> <G| J_EW^ν |0>  summed over glueball states |G>

where each matrix element `<0| J_EW^μ |G>` couples a colored quark
bilinear to a color-singlet hadronic state. By Wigner-Eckart on
`SU(3)_c`, this matrix element is a singlet-channel projection of
the q-qbar bilinear:

    <0| J_EW^μ |G> = (1/N_c) trace_c[G_glueball^μ]

where the `1/N_c` arises from normalizing the singlet projector
`P_{singlet} = (1/N_c) δ_a^a` against the fundamental color sum.

Therefore each insertion picks up a factor of `1/N_c`, and the
disconnected piece is suppressed by `1/N_c^2`:

    Pi_EW^{disc} / Pi_EW^{conn} ~ 1/N_c^2 * h(λ)

where `h(λ)` is a non-perturbative function of the 't Hooft coupling
encoding glueball dynamics. This is the standard OZI suppression rule
for vector currents in large-N_c QCD (Witten 1979, Coleman 1985).

### 3. Matching the lattice readout

The lattice EW coupling is extracted from `Pi_EW^{full}` via the CMT,
which is color-blind:

    g_EW^{lattice}^2 = N_c * <Pi_EW^{full}>_{lattice} / (vertex normalization)

At leading order in `1/N_c`, the disconnected piece is suppressed:

    Pi_EW^{full} = Pi_EW^{conn} + O(1/N_c^2) * Pi_EW^{conn}

so the lattice readout includes both pieces but is dominated by the
connected piece up to `O(1/N_c^2)` corrections.

The continuum EW coupling, by contrast, is matched to a perturbative
QCD-corrected quark loop that has no glueball intermediate state at
leading order in `α_s`. The continuum readout therefore picks up only
the connected piece. The matching factor between lattice and continuum
is:

    g_EW^{phys}^2 / g_EW^{lattice}^2 = Pi_EW^{conn} / Pi_EW^{full}
                                     = 1 / (1 + O(1/N_c^2))
                                     = 1 - O(1/N_c^2)

The package-level `9/8` correction is obtained if the disconnected
coefficient is identified with the sibling `R_conn` complement. The
large-`N_c` argument here supports that route parametrically; it does
not prove the coefficient equality. Therefore this note is a bounded
support input for the EW matching lane, not a stand-alone closure of
the physical matching factor.

### 4. Consistency check against MC

The runner [`scripts/frontier_color_projection_mc.py`](../scripts/frontier_color_projection_mc.py)
measures `R_conn = 0.887 ± 0.008` on a 4^4 lattice at β = 6, in
agreement with `8/9 = 0.8889` to 0.2%. That validates the sibling
`R_conn` channel. This note uses the same large-`N_c` suppression
logic for the EW disconnected topology, but a dedicated physical
matching theorem or runner would still be required to turn the
parametric suppression argument into an exact `1/R_conn` coefficient
claim.

## Claim boundary

This theorem proves a **bounded support route** for connected-trace EW
matching at leading order in `1/N_c`. It does **not** prove:

- An exact (genus-2-vanishing) matching identity. Exact matching would
  require showing the disconnected piece vanishes identically, which
  is false (glueball intermediate states exist), or deriving its
  coefficient from an independent physical matching condition.
- A first-principles derivation independent of the `1/N_c` expansion.
  The matching uses the same topological mechanism as R_conn; an
  independent derivation route would strengthen the result but is
  not present here.
- Specific values of the disconnected coefficient. The MC bound on
  `R_conn` is relevant corroboration for the sibling color channel,
  not a direct measurement of the EW disconnected topology.

## What this lane does NOT change

- `g_1`, `g_2`, `sin²θ_W`, `1/α_EM(M_Z)` numerical agreements with PDG
  remain as-is. This theorem supplies bounded support for the
  matching route; the comparator values are unchanged.
- `R_conn = 8/9` itself remains a separate theorem in
  [RCONN_DERIVED_NOTE.md](RCONN_DERIVED_NOTE.md), with its own audit
  row and its own MC verification.
- The 't Hooft expansion and the OZI rule are both standard textbook
  results (Witten 1979; Coleman 1985, Ch. 8; Manohar 1998
  hep-ph/9802419). This note applies them; it does not invent them.

## References

- 't Hooft, *Nucl. Phys.* B72, 461 (1974) — original 1/N_c paper.
- Witten, *Nucl. Phys.* B160, 57 (1979) — OZI suppression of
  disconnected vector-current contributions.
- Coleman, *Aspects of Symmetry* (1985), Ch. 8 — pedagogical large-N_c.
- Manohar, *Large N QCD* (1998), hep-ph/9802419 — modern review.
- Lucini, Teper, Wenger, *JHEP* 0401, 061 (2004) — lattice MC
  verification of `1/N_c^2` suppression of non-planar observables at
  strong coupling.

## Cross-references

- Parent claim:
  [YT_EW_COLOR_PROJECTION_THEOREM.md](YT_EW_COLOR_PROJECTION_THEOREM.md)
  — the EW color projection lane that this theorem unblocks.
- Sibling derivation:
  [RCONN_DERIVED_NOTE.md](RCONN_DERIVED_NOTE.md) — the q-qbar channel
  R_conn derivation, using the same `1/N_c` topological mechanism.
- Audit lane handoff:
  [docs/audit/worker_lanes/01_rconn_derivation.md](audit/worker_lanes/01_rconn_derivation.md).
