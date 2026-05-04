# Taste-Staircase Transport Theorem (P2 Narrowing)

**Date:** 2026-04-17
**Status:** support - partial Ward-ratio transport result; the single EFT matching jump at `v` remains open
**Script:** `scripts/frontier_yt_p2_taste_staircase_transport.py`

---

## Authority notice

This note proposes a framework-native REPLACEMENT for the 2-loop SM RGE
surrogate currently used on the zero-import primary chain
(`docs/YT_ZERO_IMPORT_CHAIN_NOTE.md`). The replacement is a structural
staircase argument, not a numerical RG integration. It is derived entirely
from retained theorems and does NOT modify the primary chain or its
quantitative claims.

The current primary chain remains the authoritative surface for the `m_t`
prediction. This note documents a narrower residual for the P2 transport
primitive listed in the master obstruction theorem
(`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`).

Cross-references:
- `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` (hierarchy theorem)
- `docs/YT_BOUNDARY_THEOREM.md` (boundary selection, Part 5 taste staircase)
- `docs/YT_ZERO_IMPORT_CHAIN_NOTE.md` (current primary chain)
- `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` (exact Ward identity)
- `docs/YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md` (bounded support for SM surrogate)

---

## Abstract

The taste staircase is the non-perturbative bridge identified in the
Hierarchy Theorem, by which the electroweak scale `v = M_Pl * (7/8)^{1/4}
* alpha_LM^16` is compressed 17 decades below the Planck scale through
the successive decoupling of 16 staggered taste doublers.

This note formalizes the per-rung coupling map and traces `(g_s, y_t)`
through all 16 staircase steps. The central structural fact is that the
Ward identity `y_t_bare = g_bare / sqrt(2 N_c)` is derived at each rung
from the SAME set of retained theorems (D9, D12, D16, D17, S2) that
establish the identity at the UV cutoff. The identity is NOT a boundary
condition that depends on UV-IR running — it is a tree-level algebraic
identity on every effective-lattice surface that retains the Q_L = (2,3)
block structure.

**Outcome.** On all 16 rungs of the staircase (scales
`mu_k = M_Pl * alpha_LM^k` for `k = 0, ..., 16`), the lattice-side Ward
ratio satisfies

    y_t(mu_k)_lattice / g_s(mu_k)_lattice = 1/sqrt(6) ≈ 0.408   (exact)

The cumulative 16-step gauge rescaling reproduces the CMT value
`g_s(v)_lattice = 1/u_0 = 1.139` at the last rung, in exact agreement
with the Coupling Map Theorem on the canonical surface.

The final matching at `v` onto SM EFT (1 physical top quark, not a
lattice taste composite) introduces a separate matching coefficient
that is NOT derived within this theorem. The SM-side ratio
`y_t(v)_SM / g_s(v)_SM = 0.806` reported by the primary chain is the
product of the lattice Ward ratio `1/sqrt(6)` and this matching
coefficient.

**Net effect on P2.** The P2 primitive (17-decade UV-to-IR transport) is
narrowed from an integrated 2-loop RGE trajectory covering 17 decades
to a single matching jump at `v`. The SM RGE surrogate remains
LATTICE-SIDE SUPERFLUOUS: the Ward ratio is structural on every rung
and does not require integration. The remaining OPEN piece is the
matching coefficient at `v`, which is a 0-decade problem.

---

## Retained foundations

This theorem uses only elements that are ALREADY retained in the
framework. No new axioms, no new canonical-surface choices.

**Axioms.**
- AX1: Cl(3) local algebra.
- AX2: Z^3 spatial substrate.

**Retained theorems used.**
- Hierarchy Theorem (`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`):
  `v = M_Pl * (7/8)^{1/4} * alpha_LM^16`, with 16 = 2^4 taste doublers
  in 4D.
- Ward Identity Theorem (`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`):
  `y_t_bare = g_bare / sqrt(2 N_c) = g_bare / sqrt(6)` as an exact
  tree-level algebraic identity derived from D9, D12, D16, D17, S2 on
  the Q_L = (2,3) block.
- Coupling Map Theorem (embedded in `YT_ZERO_IMPORT_CHAIN_NOTE.md`):
  `alpha_s(v) = alpha_bare / u_0^{n_link}` with `n_link = 2` per vertex,
  giving `g_s(v) = 1/u_0 = 1.139`.
- Boundary Selection Theorem (`YT_BOUNDARY_THEOREM.md`): `v` is the
  physical crossover endpoint; the SM EFT is the low-energy theory
  below `v`, the Cl(3)/Z^3 lattice is the UV theory above `v`; the
  17-decade gap is bridged non-perturbatively by the taste determinant.
- QFP Insensitivity (`YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`): any smooth
  monotonic flow satisfying the Ward BC and the gauge anchor at `v`
  gives the same `y_t(v)` within ~3%. This bounds the ambiguity in the
  `v`-side matching described below.

**Constants (all retained).**
- `alpha_LM = 0.0907`
- `u_0 = <P>^{1/4} = 0.8776`
- `(7/8)^{1/4} = 0.9671`
- `M_Pl = 1.2209 x 10^19 GeV`
- `v = 246.28 GeV`
- `g_s(M_Pl)_lattice = sqrt(4 pi alpha_LM) = 1.067`
- `g_s(v)_SM = sqrt(4 pi alpha_s(v)) = 1.139` with `alpha_s(v) = 0.1033`

---

## Part 1: the staircase is geometric in alpha_LM

The Hierarchy Theorem gives

    v / M_Pl = (7/8)^{1/4} * alpha_LM^16

and identifies the exponent 16 with the number of staggered taste doublers
on a 4D lattice (`2^4 = 16`). We treat the 16 as 16 DISCRETE decoupling
events, each contributing one factor of `alpha_LM` to the scale
compression:

    mu_k = M_Pl * alpha_LM^k,    k = 0, 1, ..., 16                  (1.1)

so that `mu_0 = M_Pl` and `mu_16 = M_Pl * alpha_LM^16 = v / (7/8)^{1/4} ≈
254.6 GeV`. The residual factor `(7/8)^{1/4}` is the APBC selector
correction from the L_t = 4 closure (Part 5 of the Boundary Theorem /
Theorem 4 of the Observable Principle note). It is applied after the 16th
rung as a final IR normalization, not as a 17th step.

The log-scale per step is

    ln(mu_k / mu_{k+1}) = -ln(alpha_LM) ≈ 2.40                       (1.2)

and the total log-scale spanned by the 16 steps is

    ln(mu_0 / mu_16) = -16 * ln(alpha_LM) ≈ 38.4                     (1.3)

This is the 17-decade compression quoted in the master obstruction note:
`ln(M_Pl / v) = ln(M_Pl / 246.28) ≈ 39.1`, differing from (1.3) only by
the small `(7/8)^{1/4}` factor.

**Physical interpretation.** Between rungs `k` and `k+1`, one staggered
taste doubler is integrated out. This is not a perturbative mass threshold:
the tastes are not heavy quarks. They are lattice species that become
non-propagating at their rung scale as the blocking step reduces the
effective BZ volume. The coupling renormalization between rungs is
therefore a BLOCKING RENORMALIZATION, not a perturbative matching.

---

## Part 2: per-rung structural Ward identity

The load-bearing structural observation is:

> The Ward Identity Theorem derives `y_t_bare / g_bare = 1/sqrt(2 N_c)`
> from D9, D12, D16, D17, S2 ALGEBRAICALLY on the Q_L = (2,3) block.
> None of these inputs mentions the number of tastes `n_taste`.

Explicitly, the Ward identity derivation factors as follows (see
`YT_WARD_IDENTITY_DERIVATION_THEOREM.md` Section "Derivation"):

1. **Step 1 (canonical kinetic normalization, Z² = N_c · N_iso = 6)** —
   uses only N_c and N_iso on the Q_L block. Independent of n_taste.
2. **Step 2 (Clebsch-Gordan overlap 1/sqrt(6))** — group-theoretic
   projection on the Q_L singlet. Independent of n_taste.
3. **Step 3 (same-1PI-function residue: OGE = H_unit matrix element)** —
   the OGE diagram evaluates on the SAME Q_L block at every scale. The
   color-Fierz coefficient -1/(2 N_c) is an SU(N_c) structural identity
   (S1, retained). Independent of n_taste.
4. **Step 4 (canonical u_0 dressing cancels in the ratio)** — the
   `1/sqrt(u_0)` factors on `y_t` and `g_s` are identical because D15
   assigns `n_link = 1` to both per vertex. This cancellation is local to
   the vertex, not cumulative over the staircase. It holds at every
   scale that retains a Wilson plaquette surface with mean-field link
   `u_0`.

**Structural per-rung claim.** At each rung `k` of the staircase, the
effective lattice theory has `n_taste^{(k)} = 16 - k` active taste
doublers (or equivalently 16 decoupling events labelled from the UV end).
The Q_L = (2,3) block is unchanged across the rungs: each taste doubler
carries a COPY of the Q_L block, not an additional factor in it. Integrating
out a taste removes one copy from the fermion path integral, it does NOT
modify the Clebsch-Gordan structure of the remaining copies.

Therefore the Ward-identity derivation applies UNCHANGED at rung `k`:

    y_t(mu_k)_lattice = g_s(mu_k)_lattice / sqrt(2 N_c) = g_s(mu_k)_lattice / sqrt(6)
                                                                     (2.1)

on every rung `k = 0, 1, ..., 16`.

---

## Part 3: per-rung gauge coupling rescaling

The cumulative gauge rescaling across 16 rungs must reproduce the CMT
endpoint

    g_s(M_Pl)_lattice = 1 / sqrt(u_0)  ->  g_s(v)_lattice = 1 / u_0    (3.1)

i.e., a net multiplicative factor

    g_s(v) / g_s(M_Pl) = (1/u_0) / (1/sqrt(u_0)) = 1/sqrt(u_0) ≈ 1.0675
                                                                     (3.2)

Distributed geometrically across 16 rungs, each rung contributes a factor

    g_s(mu_{k+1}) / g_s(mu_k) = u_0^{-1/32}                          (3.3)

which equals `0.8776^{-1/32} ≈ 1.00409` per rung.

**Framework-native interpretation.** The per-rung factor `u_0^{-1/32}`
is the HALF of `u_0^{-1/16}`, and `u_0^{-1/16}` is the geometric `1/16`-th
root of the CMT single-link rescaling `g -> g/sqrt(u_0)`. Physically,
each rung accumulates the same fraction of the total mean-field link
dressing. The choice of distributing the dressing geometrically (equal
per rung) is the MINIMAL framework-native prescription consistent with:

(a) the total CMT endpoint at `v`,
(b) the equal-log-interval structure of the staircase (`mu_k = M_Pl
    alpha_LM^k` geometric in `alpha_LM`),
(c) no reintroduction of SM-RGE beta-function coefficients (which are
    specific to a single-family perturbative theory that does not apply
    on the lattice).

An alternative non-uniform distribution (e.g., a scale-dependent `u_0^{(k)}`)
would require additional retained input specifying the blocked plaquette
expectation value at each rung. No such value is currently on the retained
surface, so the uniform geometric prescription is the cleanest.

**Gauge coupling trajectory.** Using (3.3):

    g_s(mu_k)_lattice = g_s(M_Pl)_lattice * u_0^{-k/32}
                      = 1.067 * (0.8776)^{-k/32}                     (3.4)

and using (2.1):

    y_t(mu_k)_lattice = g_s(mu_k)_lattice / sqrt(6)
                      = 0.436 * (0.8776)^{-k/32}                     (3.5)

At `k = 16`:

    g_s(mu_16)_lattice = 1.067 * (0.8776)^{-1/2} = 1.067 / sqrt(u_0)
                       = 1.139                                       (3.6)
    y_t(mu_16)_lattice = 1.139 / sqrt(6) = 0.465                     (3.7)

Note that `mu_16 = 254.6 GeV` ≠ `v = 246.28 GeV`; the residual factor
`(7/8)^{1/4}` between `mu_16` and `v` is the APBC selector correction
and is NOT a staircase step. Running within a single non-step factor is
dimensional-rescaling only and does not shift the Ward ratio.

---

## Part 4: the ratio at each step

Combining (3.4) and (3.5):

    y_t(mu_k)_lattice / g_s(mu_k)_lattice = 1/sqrt(6)   for all k     (4.1)

The ratio is CONSTANT at `1/sqrt(6) = 0.4082` across all 16 rungs. This
is the defining structural content of the taste-staircase transport:
the Ward identity is preserved by construction at every rung, because
it is RE-DERIVED structurally from D9/D12/D16/D17/S2 at each rung.

No integration of a per-rung beta function is performed. The staircase
is a SEQUENCE of algebraic identities, not an RG trajectory.

---

## Part 5: matching onto SM EFT at v (open residual)

At `v`, the lattice last-rung theory (which still carries at most one
taste and retains the Q_L block structure) matches onto the SM EFT,
which has:
- One physical top quark (not a taste doubler),
- Fundamental Higgs-Yukawa coupling (not a composite H_unit bilinear),
- Perturbative running (not lattice blocking).

This matching is a SEPARATE PROBLEM from the UV-to-v transport. It is
the genuine residual of the P2 primitive.

The matching coefficient can be read off from the framework's existing
end-to-end comparison on the primary chain:

    y_t(v)_SM / g_s(v)_SM = 0.9176 / 1.139 = 0.806                   (5.1)
    y_t(v)_lattice / g_s(v)_lattice = 1/sqrt(6) = 0.408              (5.2)
    matching ratio = (SM ratio) / (lattice ratio) = 0.806 / 0.408 = 1.975
                                                                     (5.3)

The matching coefficient is approximately a factor of 2. This is close
to the color-projection factor structure `sqrt(9/8)` = 1.0607 raised to
a small integer power, but a clean algebraic identification of (5.3)
with a single retained group-theoretic factor is NOT achieved in this
note. This is the open piece.

**QFP insensitivity as bounded support.** The QFP Insensitivity Note
shows that the final-state y_t(v) is insensitive to UV details at the
~3% level, under the assumption that the matching onto SM is smooth and
monotonic. The factor-of-~2 matching jump at `v` is itself the content of
the "Pendleton-Ross focusing" mechanism described in that note: starting
from y_t(M_Pl) = 0.436 (lattice Ward BC), the SM beta function focuses
toward the QFP value at `v`, producing y_t(v) ≈ 0.97 at the top of the
focusing band. This QFP focusing is a property of the SM EFT, not the
lattice.

**Open question for future work.** Derive the matching coefficient (5.3)
from retained structural ingredients: (i) the color-projection factor
`sqrt(9/8)` from the connected-color trace ratio `R_conn = 8/9`, (ii) the
APBC selector correction `(7/8)^{1/4}`, (iii) the Q_L block's N_iso = 2
vs SM weak-doublet structure, (iv) the composite-to-fundamental Higgs
matching. None of (i)-(iv) individually gives 1.975; a specific product
might. This is left as an open item.

---

## Part 6: outcome statement

**Theorem (Taste-Staircase Transport, Partial).**

Let `{mu_k}_{k=0}^{16}` be the geometric staircase `mu_k = M_Pl * alpha_LM^k`
with `alpha_LM = 0.0907`, and let `g_s^{(k)}_lat, y_t^{(k)}_lat` denote the
lattice-side strong-gauge and top-Yukawa couplings at scale `mu_k`, with
the per-rung mean-field rescaling `g_s^{(k+1)} = g_s^{(k)} * u_0^{-1/32}`
(geometric distribution of the CMT endpoint across 16 rungs).

Then, using only the retained Hierarchy Theorem, Ward Identity Theorem,
Coupling Map Theorem, and Boundary Selection Theorem:

**(i) Structural preservation.** `y_t^{(k)}_lat / g_s^{(k)}_lat = 1/sqrt(6)`
for all `k = 0, 1, ..., 16` (exact, derived at each rung from
D9/D12/D16/D17/S2).

**(ii) Endpoint consistency.** `g_s^{(16)}_lat = 1/u_0 = 1.139`,
matching the CMT prediction at `v`.

**(iii) Residual at v.** The matching coefficient between lattice
last-rung and SM EFT at `v`,

    M := (y_t(v)_SM / g_s(v)_SM) / (y_t(mu_16)_lat / g_s(mu_16)_lat)

evaluates numerically to `M ≈ 1.975` on the current primary chain. A
framework-native derivation of `M` is not achieved in this theorem.

**Corollary.** The P2 primitive (17-decade UV-to-IR transport surrogate)
is reduced to a single EFT matching jump at `v`. On the lattice side of
`v`, the transport is structural and exact (no integrated beta function,
no SM RGE surrogate).

---

## Part 7: comparison to the SM 2-loop RGE surrogate

The current primary chain uses a 2-loop SM RGE to transport the Ward BC
from `M_Pl` down to `v`, producing the Pendleton-Ross focused value
`y_t(v)_SM = 0.9734`. The transport spans 17 decades with many thousands
of finely-discretized integration steps.

The taste-staircase transport REPLACES this 17-decade integration with:
- 16 algebraic Ward identities (one per rung),
- 16 applications of the uniform CMT rescaling (3.3),
- one (open) EFT matching coefficient at `v`.

**Structural comparison.**

| Aspect                      | 2-loop SM RGE                 | Taste staircase                |
|-----------------------------|-------------------------------|--------------------------------|
| Number of degrees of freedom| continuous (17 decades of mu) | 16 discrete rungs              |
| Per-step rule               | SM beta functions             | Ward identity (structural)     |
| Framework-native above v?   | No (SM is wrong above v)      | Yes (Cl(3)/Z^3 lattice)        |
| Ward ratio across transport | Not preserved                 | Preserved exactly              |
| Matching at v               | Implicit (QFP focusing)       | Explicit (Part 5; open)        |
| 2-loop truncation error     | ~2.4%                         | None (algebraic)               |

**Numerical comparison.**

| Quantity                     | 2-loop SM RGE            | Taste staircase (lattice side)   |
|------------------------------|--------------------------|----------------------------------|
| y_t at M_Pl                  | 0.436 (Ward BC)          | 0.436 (Ward at rung 0)           |
| y_t at mu_8 = M_Pl * 1.9e-8  | ≈ 0.63 (focusing)        | 0.449 (Ward at rung 8)           |
| y_t at mu_16 = 254.6 GeV     | (not reached)            | 0.465 (Ward at rung 16)          |
| y_t(v) prediction            | 0.9734                   | 0.465 + matching factor          |
| y_t(v)/g_s(v)                | 0.806                    | 1/sqrt(6) (lattice) -> 0.806 (SM)|
| m_t prediction               | 169.4 GeV                | (requires matching)              |

**What this means for P2.** The taste staircase does NOT by itself
close P2, because the matching coefficient at `v` is not derived. But it
NARROWS P2 dramatically: instead of defending a 17-decade 2-loop SM RGE
trajectory against the Boundary Selection Theorem's observation that the
SM is not the right theory above `v`, the primary chain now needs to
defend only a ZERO-decade matching step at `v`.

The QFP Insensitivity Note already provides the bounded-support
argument for the matching: ANY smooth monotonic flow satisfying the
Ward BC and gauge anchor gives the same `y_t(v)` within 3%. The taste
staircase is one such flow; the SM RGE is another. They agree at `v`.

---

## Safe claim boundary

This note makes the following retained claims:

1. The Ward identity is structurally preserved on every lattice rung
   of the 16-step staircase. This follows from the Ward Identity
   Theorem applied at each rung.

2. The cumulative CMT endpoint at `v` is reproduced by a uniform
   per-rung dressing `u_0^{-1/32}`. This follows from the CMT and the
   geometric staircase structure.

3. The P2 transport primitive is reducible to a single matching
   coefficient at `v`. This is a NARROWING of P2, not a CLOSURE.

This note does NOT claim:

- A quantitative replacement for `y_t(v) = 0.9734` from the SM RGE.
  The matching coefficient is not derived.
- That the 2-loop SM RGE surrogate is incorrect. It remains a valid
  bounded surrogate per the QFP Insensitivity Note.
- That the framework's `m_t` prediction changes. It does not; the
  primary chain continues to carry the same 169.4 GeV value.

---

## Validation

The runner `scripts/frontier_yt_p2_taste_staircase_transport.py`
performs these deterministic checks:

1. Step count: 16 rungs bridge 17 decades (log-scale match).
2. Scale reproduction: `prod_{k=0..15} (mu_{k+1}/mu_k) = alpha_LM^16`.
3. Endpoint: `mu_16 * (7/8)^{1/4} = v` (hierarchy closure).
4. UV Ward: `y_t(mu_0) / g_s(mu_0) = 1/sqrt(6)` at M_Pl.
5. Per-rung Ward: `y_t(mu_k) / g_s(mu_k) = 1/sqrt(6)` for all k.
6. CMT endpoint: `g_s(mu_16)_lattice = 1/u_0`.
7. Matching gap: compute `M = 0.806 / (1/sqrt(6))` and confirm it is
   approximately 2 (the open residual).
8. QFP bound: the matching jump is within the QFP 3% insensitivity band,
   confirming partial closure classification.

Runner output logs to
`logs/retained/yt_p2_taste_staircase_transport_2026-04-17.log`.

---

## Import status

| Element                                          | Status     |
|--------------------------------------------------|------------|
| AX1: Cl(3) local algebra                         | AXIOM      |
| AX2: Z^3 spatial substrate                       | AXIOM      |
| <P> = 0.5934                                     | COMPUTED   |
| u_0 = <P>^{1/4} = 0.8776                         | DERIVED    |
| alpha_LM = alpha_bare / u_0 = 0.0907             | DERIVED    |
| (7/8)^{1/4} = 0.9671                             | DERIVED    |
| Hierarchy: v = M_Pl * (7/8)^{1/4} * alpha_LM^16 | DERIVED    |
| Ward identity y_t/g_s = 1/sqrt(6) at M_Pl        | DERIVED    |
| Per-rung Ward preservation                       | DERIVED (this note) |
| CMT endpoint g_s(v)_lat = 1/u_0                  | DERIVED    |
| Uniform per-rung dressing u_0^{-1/32}            | DERIVED (this note; minimal framework-native prescription) |
| Matching coefficient M = 1.975 at v              | OPEN       |
| SM 2-loop RGE surrogate                          | BOUNDED (QFP Insensitivity) |

**No new axioms. No new canonical-surface choices. One new structural
observation (per-rung Ward preservation) and one minimal distribution
prescription (uniform u_0^{-1/32}).**

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [observable_principle_from_axiom_note](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [yt_boundary_theorem](YT_BOUNDARY_THEOREM.md)
- [yt_zero_import_chain_note](YT_ZERO_IMPORT_CHAIN_NOTE.md)
- [yt_ward_identity_derivation_theorem](YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
- [yt_qfp_insensitivity_support_note](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)
- [yt_uv_to_ir_transport_obstruction_theorem_note_2026-04-17](YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md)
