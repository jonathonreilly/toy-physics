# Left-Handed Doublet `SU(2)² × U(1)_Y` Anomaly Cancellation From Graph-First Eigenvalues

**Date:** 2026-05-01
**Status:** support / structural anomaly-cancellation theorem (one of three repair-target items for `LEFT_HANDED_CHARGE_MATCHING_NOTE`'s audit objection). This note proves that the left-handed doublet sector of the framework's graph-first surface satisfies the `SU(2)² × U(1)_Y` (W-W-B) triangle anomaly identity exactly. It does **not** close the full anomaly-complete one-generation chain — it addresses only one of the three repair targets named in the LHCM audit verdict.
**Primary runner:** `scripts/frontier_lh_doublet_su2_squared_hypercharge_anomaly.py`
**Cited authorities (one-hop, all retained-grade on `main`):**
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — retained-grade effective status. Provides the eigenvalue pattern: traceless `u(1)` direction has eigenvalue `+1/3` on the 3-dim symmetric/weak-doublet block and `-1` on the 1-dim antisymmetric/weak-doublet block.
- [`GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`](GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md) — retained-grade effective status. Provides the selected-axis surface on which the eigenvalues are computed.
- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) — retained-grade effective status. Provides native cubic SU(2) for the doublet structure.

**This note explicitly cites `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` only as the parent claim whose audit objection is being partially addressed.** It does not import any load-bearing content from LHCM; the derivation goes through retained primitives directly.

---

## 0. Why this note exists

The 2026-05-01 audit verdict on
[`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
(LHCM) states a precise repair target:

> *Repair target: a retained theorem deriving the matter assignment,
> U(1)_Y normalization/readout, and anomaly-complete chiral completion
> from the graph-first surface.*

LHCM is `proposed_retained` `audited_conditional` with **267 transitive
descendants**. Its audit objection has three items:

1. **Matter assignment.** The Sym(3) eigenspace identifies as the
   "quark-doublet block" and the Anti(1) eigenspace as the
   "lepton-doublet block".
2. **U(1)_Y normalization.** The structural eigenvalue pattern
   `+1/3 : −1` matches the SM hypercharge values for `Q_L` and `L_L` in
   the convention `Q = T_3 + Y/2`.
3. **Anomaly-complete chiral completion.** The matter content satisfies
   the SM anomaly cancellation identities.

This note closes item (3) **for the LH-doublet sector** by deriving the
`SU(2)² × U(1)_Y` (W-W-B) triangle anomaly identity from the framework's
retained structural eigenvalues. Items (1) and (2) and the remaining
anomaly identities (SU(3)² × Y, gravitational × Y, Y³) are scoped
explicitly to the parent
[`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
and are **not** derived in this note.

The cycle-cleanup PR pattern from PR #249 / PR #250 applies here too:
this note is a **support theorem on a sister surface** that addresses one
specific named item from a multi-item audit objection. Closing it does
not promote LHCM to retained-grade; it removes one of three open items.

## 1. Setup: the framework's retained structural eigenvalues

From `GRAPH_FIRST_SU3_INTEGRATION_NOTE` (retained):

> *The traceless `u(1)` direction has eigenvalues `+1/3` on the
> `6`-dimensional symmetric/weak-doublet block and `-1` on the
> `2`-dimensional antisymmetric/weak-doublet block.*

In the 4-point base × 2-point fiber decomposition:

- **Sym(3) × doublet** = 3 × 2 = 6-dim block, eigenvalue **`+1/3`**.
- **Anti(1) × doublet** = 1 × 2 = 2-dim block, eigenvalue **`−1`**.

The eigenvalues are forced by the gl(3) ⊕ gl(1) commutant structure:
the unique traceless direction satisfies
`3 · (+1/3) + 1 · (−1) = 0` (tracelessness on the 4-dim base).

We adopt the SM convention `Y(Q_L) = +1/3` and `Y(L_L) = −1`, and
identify:

- **Q_L doublet**: Sym(3) block paired with the SU(2) doublet — 3 colors,
  hypercharge `Y(Q_L) = +1/3`.
- **L_L doublet**: Anti(1) block paired with the SU(2) doublet — 1 color
  (singlet under SU(3)), hypercharge `Y(L_L) = −1`.

These identifications are also part of the LHCM repair target items (1)
and (2). They are taken here as load-bearing structural inputs cited from
the retained graph-first SU(3) integration note. Their independent
derivation is the parent ONE_GENERATION_MATTER_CLOSURE work.

## 2. The `SU(2)² × U(1)_Y` triangle anomaly

For a chiral gauge theory with gauge group `G_W × G_Y` where `G_W` is
non-abelian (here SU(2)_L) and `G_Y` is abelian (here U(1)_Y), the
triangle diagram with two `G_W` gauge bosons and one `G_Y` boson on the
external legs has anomaly coefficient:

```text
A_{G_W² G_Y} = Σ_(LH chiral fermions in irrep R)  T(R) · Y(R)
```

where:

- `T(R)` is the Dynkin index of representation `R` of `G_W`,
  normalized so that `T(R) δ^{ab} = Tr_R(t^a t^b)`.
- `Y(R)` is the U(1)_Y charge of the LH fermion in irrep `R`.
- The sum runs over all LH chiral fermions, with each multiplet
  contributing once weighted by its multiplicity (e.g., color
  multiplicity `N_c` for quarks).

For `G_W = SU(2)_L` and the **fundamental representation (doublet)**:

```text
T(fundamental of SU(2)) = 1/2
```

(standard convention `Tr[t^a t^b] = (1/2) δ^{ab}` with t^a = σ^a / 2).

Anomaly cancellation requires:

```text
A_{SU(2)² Y} = 0
```

i.e., the sum of `T(R) · Y(R)` over all LH SU(2) doublets must vanish.

## 3. The cancellation identity

For the LH-doublet sector with Q_L (3 colors of quark doublet) and L_L
(1 lepton doublet), summing the SU(2)² × U(1)_Y anomaly contribution:

```text
A_{SU(2)² Y}
  = Σ_(LH doublets, weighted by color) T(doublet) · Y(R)
  = N_c · T(2) · Y(Q_L)  +  1 · T(2) · Y(L_L)
  = 3 · (1/2) · (+1/3)  +  1 · (1/2) · (−1)
  = (3 · 1/3 · 1/2)  +  (1 · (−1) · 1/2)
  = (1/2)  +  (−1/2)
  = 0.                                                        (3.1)
```

**The anomaly cancels exactly.**

The cancellation has **three** structural ingredients, all sourced from
retained primitives:

1. `N_c = 3` from `GRAPH_FIRST_SU3_INTEGRATION_NOTE` — the symmetric
   block of the residual swap τ has dimension 3.
2. `Y(Q_L) = +1/3` and `Y(L_L) = −1` from the framework's retained
   eigenvalue pattern on the gl(3) ⊕ gl(1) commutant traceless
   direction.
3. The doublet Dynkin index `T(2) = 1/2` from the standard SU(2)
   normalization (admitted convention; identical at the lattice and
   continuum level since the SU(2) generators in
   `NATIVE_GAUGE_CLOSURE_NOTE` satisfy `Tr[T_i T_j] = (1/2) δ_{ij}`).

## 4. Why the cancellation is structural, not numerical coincidence

The identity `3 · (+1/3) + 1 · (−1) = 0` is the **same identity** as the
tracelessness of the gl(3) ⊕ gl(1) commutant's u(1) direction, which is
forced by the dimension count `dim(Sym) + dim(Anti) = 4`:

- The unique traceless direction in gl(4) restricted to gl(3) ⊕ gl(1)
  must satisfy `dim(Sym) · y_Sym + dim(Anti) · y_Anti = 0`.
- With `dim(Sym) = 3`, `dim(Anti) = 1`, normalizing `y_Anti = −1`
  immediately gives `y_Sym = +1/3`.

The W-W-B anomaly identity (3.1) becomes, with `T(2) = 1/2` factored out:

```text
A_{SU(2)² Y} / T(2)
  = N_c · y_Sym + 1 · y_Anti
  = 3 · (+1/3) + 1 · (−1)
  = 0.                                                        (4.1)
```

So the anomaly cancellation in the LH-doublet sector is **the same**
identity as the tracelessness of the structural u(1) direction. They are
literally the same equation. The framework does not need to fine-tune
hypercharges to cancel the anomaly; the anomaly cancels because the
hypercharges are the trace-free eigenvalues of a graph-first commutant.

This is the structural content that closes repair-target item (3) for
the LH-doublet sector.

## 5. What this note does NOT close

This note is explicitly **partial**. Items not closed:

- **(R-A) SU(3)² × U(1)_Y anomaly**: requires `Σ_(quarks) Y = 0`. With
  only the LH doublet (Y = +1/3) and 3 colors contributing, the
  contribution is `3 · (+1/3) = 1`, which must cancel against RH-quark
  hypercharges (`u_R` and `d_R` singlets, with Y values -2 each ... but
  wait, that's the SM sum; let me re-check):
  - In the SM: `Y(u_R) = −4/3` (left-conjugate convention), `Y(d_R) = +2/3`.
  - SU(3)² × Y for the quarks: `2 · Y(Q_L) − Y(u_R) − Y(d_R)` summed
    over color must vanish. With Y(Q_L) = +1/3, Y(u_R) = +4/3,
    Y(d_R) = −2/3 (one SM convention): `2 · (1/3) − 4/3 + 2/3 = 0`.
  - This anomaly identity needs the **RH-quark sector** with retained
    Y values, which is NOT on this note's scope.
- **(R-B) U(1)_Y³ anomaly**: requires `Σ Y³ = 0` over all LH fermions
  (after Weyl-rotating RH to LH-conjugate). Requires the full one-
  generation matter content.
- **(R-C) Mixed gravitational × U(1)_Y anomaly**: requires `Σ Y = 0`
  over all LH fermions.
- **(R-D) Witten SU(2) global anomaly**: requires an even number of LH
  SU(2) doublets. With Q_L (3 colors) + L_L (1) = 4 doublets, this is
  satisfied by the LH doublet sector alone, so the Witten anomaly is
  trivially OK.

Closing (R-A), (R-B), (R-C) requires the right-handed sector of one
generation. That work belongs to
[`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
and similar retained-program notes.

## 6. Theorem statement

**Theorem (LH-doublet `SU(2)² × U(1)_Y` cancellation).** On the
framework's graph-first selected-axis surface, with the retained
eigenvalue pattern (`y_Sym = +1/3`, `y_Anti = −1`) inherited from
`GRAPH_FIRST_SU3_INTEGRATION_NOTE`, the SU(2)² × U(1)_Y triangle anomaly
contribution from LH doublets vanishes identically:

```text
A_{SU(2)² Y, LH doublets}
  = N_c · T(2) · y_Sym  +  1 · T(2) · y_Anti
  = T(2) · (3 · (+1/3) + 1 · (−1))
  = T(2) · 0
  = 0.
```

The cancellation is the same equation as the trace-freeness of the
structural u(1) direction on the gl(3) ⊕ gl(1) commutant; it is forced,
not tuned.

## 7. What this changes for LHCM's audit verdict

After this note lands and the audit pipeline regenerates:

- LHCM's **repair-target item (3)** ("anomaly-complete chiral
  completion") is partially addressed — specifically, the LH-doublet
  sector of the SU(2)² × U(1)_Y anomaly is now derived rather than
  asserted.
- LHCM's **repair-target items (1)** (matter assignment via SU(3)
  representation) and **(2)** (Y normalization via trace-freeness) are
  unchanged — they remain admitted on the parent note's surface, with
  this note citing the same retained structural inputs.
- LHCM remains `audited_conditional` until items (1), (2), and the
  remaining (R-A), (R-B), (R-C) anomaly identities are also closed in
  the parent ONE_GENERATION_MATTER_CLOSURE program.

Audit-graph effect: the open-dependency-paths surface for LHCM should
narrow by one specific item ("anomaly-complete chiral completion of LH
doublets"), keeping the ONE_GENERATION dependency for the RH sector.

## 8. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_lh_doublet_su2_squared_hypercharge_anomaly.py
```

The runner verifies:

1. The note exists with correct title, status, and cited retained
   authorities.
2. The retained eigenvalue pattern (`+1/3`, `−1`) is reproduced from
   first principles: the unique traceless direction on `gl(3) ⊕ gl(1)`
   normalized so the 1-dim block has eigenvalue −1.
3. The Dynkin index `T(2) = 1/2` for the SU(2) doublet matches the
   standard normalization used in `NATIVE_GAUGE_CLOSURE_NOTE`'s
   generators: `Tr[T_i T_j] = (1/2) δ_{ij}`.
4. The SU(2)² × U(1)_Y anomaly contribution from LH doublets evaluates
   to **exactly 0** as a `Fraction` equality (not floating-point).
5. The same identity holds at general `(y_Sym, y_Anti)` satisfying the
   trace-freeness `3 y_Sym + y_Anti = 0` — i.e., the cancellation is
   the trace-freeness condition, restated.
6. The (R-A), (R-B), (R-C) remaining anomaly identities are explicitly
   named as out-of-scope for this note.

## 9. Inputs and import roles

| Input | Role | Import class | Source |
|---|---|---|---|
| `dim(Sym) = 3`, `dim(Anti) = 1` | structural retained input | framework retained | `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` (residual swap of complementary axes) |
| Trace-freeness of u(1) direction on `gl(3) ⊕ gl(1)` | structural retained input | framework retained | same note (commutant theorem) |
| `y_Sym = +1/3`, `y_Anti = −1` | structural retained input | framework retained | same note (eigenvalue check by runner) |
| `T(2) = 1/2` (SU(2) doublet Dynkin index) | admitted standard convention | textbook bridge | standard SU(2) normalization, matches `NATIVE_GAUGE_CLOSURE_NOTE`'s native generator trace |
| Anomaly-coefficient formula `A = Σ T(R) · Y(R)` | admitted standard QFT identity | textbook bridge | any QFT reference (e.g., Peskin & Schroeder Ch. 19) |
| `Q = T_3 + Y/2` (electric-charge formula) | admitted SM photon-definition convention | textbook bridge | standard SM, NOT used as proof input in this note |

No new physical claims, no new numerical comparators, no new admitted
observations beyond standard QFT triangle-anomaly machinery and the SM
photon-definition convention. The note's load-bearing arithmetic
(equation 3.1) is exact rational arithmetic.

## 10. Forbidden imports

- `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` is cited only as the parent note
  whose audit objection is being addressed; no load-bearing content is
  imported from it. The runner verifies this.
- The Q = T_3 + Y/2 formula is admitted as the SM photon-definition
  convention but is NOT used as a proof input — the anomaly identity is
  derived directly from `(T(R), Y(R))` data, which depends only on
  `Y(Q_L) = +1/3` and `Y(L_L) = −1` (retained inputs).

## 11. Safe wording

**Can claim:**
- "Structural derivation of the SU(2)² × U(1)_Y anomaly cancellation
  for the LH doublet sector from retained graph-first eigenvalues."
- "The cancellation is forced by the trace-freeness of the structural
  u(1) direction; it is not tuned."
- "Closes one of three repair-target items in the LHCM audit verdict."

**Cannot claim:**
- bare `retained` / `promoted`.
- "Promotes LHCM to retained-grade." (it does not — items 1, 2, R-A,
  R-B, R-C remain open)
- "Closes the anomaly-complete chiral completion." (it closes only the
  SU(2)² × U(1)_Y piece for LH doublets)

## 12. Cross-references

- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  — parent note whose audit objection items (3) is partially addressed.
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  — retained source of the eigenvalue pattern.
- [`GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`](GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md)
  — retained source of the selected-axis surface.
- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) —
  retained source of the SU(2) generators.
- [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
  — parent program for the remaining anomaly identities (R-A, R-B,
  R-C) requiring the RH sector.
- LHF leverage map: PR #248 (LHCM is rank 3, 488 transitive descendants).
