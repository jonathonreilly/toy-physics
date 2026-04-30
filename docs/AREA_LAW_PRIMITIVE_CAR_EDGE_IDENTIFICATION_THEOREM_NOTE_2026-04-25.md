# Area-Law Primitive CAR Edge Identification Theorem Note

**Date:** 2026-04-25
**Status:** proposed_retained Target 2 bridge corollary pending audit;
primitive complex-CAR edge semantics supplied by the 2026-04-30
Clifford-Majorana derivation theorem
**Runner:** `scripts/frontier_area_law_primitive_car_edge_identification.py`

## Purpose

The primitive parity-gate carrier theorem proves the exact coefficient once the
two-orbital edge carrier is identified. This note pushes one step deeper: it
states the minimal local-CAR assumptions under which that carrier is forced by
the primitive boundary block itself.

The result is a conditional bridge:

> If the horizon entropy carrier is the minimal local complex CAR edge algebra
> supported on the primitive rank-four boundary packet, then the active block
> is `F(C^2)`, one mode is the normal crossing channel, the other is the
> self-dual transverse-Laplacian channel, and the Widom coefficient is exactly
> `1/4`.

This is stronger than the previous multipocket selector statement: the
half-zone is not an adjustable pocket measure. It is the self-dual half of the
primitive nearest-neighbor transverse Laplacian.

## Primitive-CAR edge axioms

Let

```text
H_cell ~= C^2_t otimes C^2_x otimes C^2_y otimes C^2_z ~= C^16
```

and let `P_A` be the Hamming-weight-one primitive boundary packet with
`rank(P_A)=4`.

For a selected primitive face with normal `e_x`, assume:

1. **Active support.** The entropy carrier is supported exactly on
   `P_A H_cell`, with no hidden active spectator sector.
2. **Minimal complex CAR carrier.** The local edge algebra is a complex CAR
   Fock algebra `F(C^m)`.
3. **Primitive normal channel.** One CAR mode is the selected normal crossing
   channel; as a Widom sector it contributes one occupied `k_x` interval for
   every transverse momentum.
4. **Minimal tangent response.** The remaining nontrivial response uses the
   tangent-symmetric nearest-neighbor transverse Laplacian and the self-dual
   low sheet.
5. **No duplicate normal channel.** Distinct primitive modes are not duplicate
   copies of the same normal channel; the second mode carries the minimal
   transverse response.

These are the explicit physical assumptions. The theorem below is then
algebraic and measure-theoretic, with no fitted coefficient.

## Rank-to-CAR step

For a complex CAR Fock algebra,

```text
dim F(C^m) = 2^m.
```

Since

```text
dim(P_A H_cell) = rank(P_A) = 4,
```

minimal active support forces

```text
2^m = 4,   m = 2.
```

Thus the primitive active boundary block has exactly two complex edge orbitals.
One complex orbital is too small; three are too large. The two-orbital local
Fock space is not chosen to fit `1/4`: it is forced by the rank-four primitive
packet once the carrier class is complex CAR.

## Tangent-Laplacian selector step

Let the selected face have `n_perp` tangent primitive directions. The unique
even nearest-neighbor tangent symbol that is symmetric under tangent-axis
permutations and normalized to range `[0,2]` is

```text
Delta_perp(q)
  = 1 - (1/n_perp) sum_{j=1}^{n_perp} cos(q_j).
```

The all-tangent half-period involution

```text
tau(q) = q + pi(1,...,1)
```

sends

```text
Delta_perp(tau q) = 2 - Delta_perp(q).
```

Therefore the threshold `Delta_perp=1` is the unique self-dual threshold, and
the sheets

```text
Delta_perp < 1,   Delta_perp > 1
```

have equal Haar measure. The tangent set `Delta_perp=1` has measure zero. The
low sheet has normalized measure exactly `1/2`.

This is the missing multipocket selector.

## Edge carrier

The two forced CAR modes are:

1. a baseline normal channel

   ```text
   epsilon_0(k) = cos(k_x),
   ```

   which contributes two Fermi crossings on every transverse fiber;

2. a self-dual tangent-response channel

   ```text
   epsilon_1(k) = cos(k_x) + Delta_perp(q),
   ```

   which contributes two Fermi crossings exactly on the half-zone
   `Delta_perp(q)<1`.

The average crossing count is therefore

```text
<N_x> = 2 + 2*(1/2) = 3.
```

By the Widom-Gioev-Klich formula for a flat primitive cut,

```text
c_Widom = <N_x> / 12 = 3/12 = 1/4.
```

This matches the primitive Planck trace:

```text
c_cell = Tr((I_16/16)P_A) = 4/16 = 1/4.
```

## Uniqueness inside the primitive-CAR class

With two CAR modes and one required normal channel, the second mode has only
three minimal possibilities at the Widom-counting level:

```text
empty/spectator     -> c = 2/12 = 1/6,
duplicate normal    -> c = 4/12 = 1/3,
self-dual tangent   -> c = 3/12 = 1/4.
```

The primitive-CAR axioms exclude the first by active support and exclude the
second by no duplicate normal channel. The remaining minimal local tangent
response is the self-dual Laplacian-gated channel, giving the Bekenstein-
Hawking coefficient.

## What this closes, and audit fallback

This note closes the carrier-identification step relative to the
primitive-CAR edge axioms. It upgrades the earlier parity-gate theorem from
"a candidate multipocket selector" to "the unique minimal local-CAR edge
carrier."

The remaining question was exactly whether the primitive-CAR edge axioms are
accepted as native `Cl(3)/Z^3` horizon semantics. The Target 3 Clifford phase
bridge supplies a sufficient metric-compatible coframe response, and the
2026-04-30 primitive Clifford-Majorana edge derivation now proposes to derive
that response from retained spatial `Cl(3)` bivectors plus the anomaly-forced
time axis. If the new derivation is audit-ratified, this result becomes a
corollary rather than a conditional theorem. If it is rejected or stripped
away, this result remains a sharp conditional theorem and the retained no-go
packet still describes the selector-free surface.

[AREA_LAW_NATIVE_CAR_SEMANTICS_TIGHTENING_NOTE_2026-04-25.md](./AREA_LAW_NATIVE_CAR_SEMANTICS_TIGHTENING_NOTE_2026-04-25.md)
tightens this question further: primitive-CAR semantics are equivalent to
accepting irreducible Clifford-Majorana edge statistics on the rank-four
active block. Rank four alone does not force that statistics choice.

[PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md](./PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md)
states the sufficient coframe-response bridge: metric-compatible primitive
coframe response forces the complex `Cl_4` relations on `P_A H_cell`, and the
rank-four irreducible module is equivalent to the two-mode CAR carrier. On a
stripped Hilbert-only surface the conditional wording still applies.

[PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md](./PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md)
is the proposed retained construction of that coframe response from retained
substrate content.

## Relation to retained no-gos

- The half-filled nearest-neighbor no-go is untouched; it is a different
  single-orbital carrier.
- The simple-fiber Widom no-go is bypassed because the primitive-CAR carrier
  has two sectors and average crossing count `3`.
- The multipocket selector no-go is answered by adding the self-dual
  Laplacian selector and showing it is forced inside the primitive-CAR axioms.
- The algebraic finite-spectrum no-go is untouched because this is a gapless
  Widom leading-log carrier, not a finite gapped Schmidt-spectrum entropy.

## Verification

Run:

```bash
python3 scripts/frontier_area_law_primitive_car_edge_identification.py
```

The runner checks the rank-to-CAR identification, uniqueness of `m=2`, the
normal-plus-tangent mode classification, uniqueness of the tangent-symmetric
nearest-neighbor Laplacian selector, exact half-zone measure in `2D` and `3D`,
and the final equality `c_Widom=c_cell=1/4`.

Current output:

```text
SUMMARY: PASS=36  FAIL=0
```
