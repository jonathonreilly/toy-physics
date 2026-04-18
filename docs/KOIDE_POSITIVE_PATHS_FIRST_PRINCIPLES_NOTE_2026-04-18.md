# Koide Positive Paths — First-Principles Attack Map

**Date:** 2026-04-18
**Status:** ranked constructive search map for closing the charged-lepton Koide
lane positively, with axiom-only routes prioritized over transplant routes

## Question

After reducing the charged-lepton Koide lane to:

- a cyclic `3`-response Wilson descendant law on
  `B0 = I`, `B1 = C + C^2`, `B2 = i(C - C^2)`,
- and one scalar selector equation
  `2 r0^2 = r1^2 + r2^2`,

what are the simplest **positive** closure routes worth attacking next?

The right search order is not “reuse later machinery first.” The right order
is:

1. fresh axiom-only / first-principles routes,
2. then retained-interface routes,
3. then transplant / extension routes.

That is exactly how the Koide lane itself first surfaced.

Since the first draft of this map, four exact reductions have also been closed:

1. the full charged Hermitian law `dW_e^H` compresses canonically to the same
   three cyclic channels
   `[KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md](./KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md)`;
2. the physical full taste cube descends, after exact `C_3[111]` averaging and
   Schur-compatible charged reduction, to the same three channels
   `[KOIDE_TASTE_CUBE_CYCLIC_SOURCE_DESCENT_NOTE_2026-04-18.md](./KOIDE_TASTE_CUBE_CYCLIC_SOURCE_DESCENT_NOTE_2026-04-18.md)`;
3. the retained `Gamma_1` second-order return already gives an exact three-slot
   orbit object whose species Fourier transport lands on the same Koide basis
   `[KOIDE_GAMMA_ORBIT_CYCLIC_RETURN_CANDIDATE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_CYCLIC_RETURN_CANDIDATE_NOTE_2026-04-18.md)`;
4. the cleanest selector candidate is now the exact scalar-versus-traceless
   cyclic block-power law
   `[KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md](./KOIDE_CYCLIC_PROJECTOR_BLOCK_DEMOCRACY_NOTE_2026-04-18.md)`;
5. that selector now pulls back exactly to one symmetric quadratic cone on the
   physical `Gamma`-orbit slots `(u, v, w)`
   `[KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md).
6. the old cross-axis `Gamma_i` basis candidate is now closed exactly by the
   full-cube axis-covariant orbit law
   `[KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md](./KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md).

So the positive-path question is sharper than it was at the start of the day:
the route space is not diverging. It is converging to one microscopic
three-channel law.

Since that draft, one more exact reduction has closed:

7. if the microscopic full-cube route is required to come from repeated
   identical positive local clock steps on the reachable `T_2` block, the
   value law is forced into the exact exponential semigroup class
   `X_beta = exp(beta G)` for one Hermitian generator `G`
   [KOIDE_GAMMA_ORBIT_POSITIVE_ONE_CLOCK_SEMIGROUP_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_POSITIVE_ONE_CLOCK_SEMIGROUP_NOTE_2026-04-18.md).
8. if the exact parity-compatible observable selector is then imposed on the
   live affine Hermitian chart, the generator search collapses further to the
   one-real line `G_m = H(m, sqrt(6)/3, sqrt(6)/3)`
   [KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md).
9. if the preserved reachable-slot ratio of the earlier `H_*` witness is then
   matched on that selected line and the branch is fixed by threshold
   continuity, the current positive candidate route becomes coordinate-closed
   [KOIDE_GAMMA_ORBIT_SELECTED_LINE_CLOSURE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_SELECTED_LINE_CLOSURE_NOTE_2026-04-18.md).
10. the remaining charged-lepton promotion target on that route is only one
    scalar cyclic-response bridge law
    `kappa = sqrt(3) r2 / (2 r0 - r1) = (v-w)/(v+w)`
    [KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md](./KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md).
11. that bridge target now sharpens one step further: on the exact selected
    slice `delta = q_+ = sqrt(6)/3`, the remaining microscopic datum is only
    the scalar `m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3`, and `kappa(m)` is monotone
    on the physical first branch
    [KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md](./KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md).
12. the selected slice itself is now decomposed exactly as a frozen slot/CP
    bank plus one real direction
    `K_Z3^sel(m) = K_frozen + m T_m^(K)`
    [KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md](./KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md).

## Top-line attack order

The recommended attack order is:

1. **Retained microscopic scalar selector law on the selected `Z_3` doublet block**
2. **Full-lattice / taste-cube cyclic source law**
3. **Axiom-only observable-principle cyclic-source law**
4. **Independent retained replacement for the `H_*` witness bridge**

Those four are the cleanest positive routes currently visible in the tree.

## The 10 approaches

### 1. Observable-principle cyclic-source law on the exact retained operators

**Type:** axiom-only / first-principles  
**Core idea:** start directly from the exact observable generator
`W[J] = log|det(D+J)| - log|det D|`, but restrict `J` to the exact cyclic
Hermitian bundle generated by retained operators on `H_hw=1`.

Use:

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- [KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md](./KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)

The three responses would be:
```
r_i = dW(B_i)
```
for the exact retained cyclic basis `B0,B1,B2`.

**Why it is strong:** no new carrier, no two-Higgs import, no later-atlas
machinery. This is the cleanest direct axiom-only route.

**Current gap:** derive the actual local source law `dW(B_i)` on this cyclic
bundle from the microscopic `D`.

### 2. Exact matrix-unit source law, then cyclic projection

**Type:** axiom-only / first-principles  
**Core idea:** use the exact retained matrix units
`E_ij = P_i C^k P_j` from the generation algebra, derive their microscopic
source responses, then project that `9`-real law down to the cyclic `3`-real
bundle.

Use:

- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- [KOIDE_CIRCULANT_WILSON_TARGET_NOTE_2026-04-18.md](./KOIDE_CIRCULANT_WILSON_TARGET_NOTE_2026-04-18.md)
- [KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md](./KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)
- [KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md](./KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md)

**Why it is strong:** completely exact retained operator basis; the cyclic law
then becomes a canonical projection rather than an ansatz. The April 18
compression theorem now proves exactly which three cyclic sums Koide keeps.

**Why it ranks below #1:** it solves a larger problem first (`9` real channels)
than the Koide lane actually asks for.

### 3. Full taste-cube / physical-lattice cyclic averaging law

**Type:** axiom-only / first-principles  
**Core idea:** work on the full `C^8` / BZ-corner carrier, derive the source
bundle there, then descend by exact `C_3[111]` averaging to the Koide cyclic
triplet.

Use:

- [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- [KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md](./KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md)

**Why it is strong:** fully respects the physical-lattice caution; does not
pretend the bare `hw=1` sector is the whole story.

**Current gap:** derive the microscopic full-carrier source law before
descending.

### 4. `hw=1` source/transfer cyclic projection law

**Type:** retained-interface / nearly first-principles  
**Core idea:** the PMNS lane already isolates an exact source/transfer pack on
`hw=1`. Project that pack to the cyclic `C_3` bundle instead of the full PMNS
carrier.

Use:

- [PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](./PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)
- [KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md](./KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)

**Why it is strong:** positive route already exists at the interface level; it
only needs to be specialized to the cyclic bundle.

**Why it ranks below #1–#3:** the note itself says the exact bank still does not
derive that pack from the sole axiom alone.

### 5. Native transfer-kernel extension from the even slice to the full cyclic law

**Type:** retained-interface positive route  
**Core idea:** start from the already-positive dominant-mode transfer kernel
`x I + y(C + C^2)`, then derive the missing odd slot that upgrades it from an
even `2`-real law to the full cyclic `3`-response law.

Use:

- [PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md](./PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md)
- [KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md](./KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)

**Why it is attractive:** it already has the right spectral language and the
right `C_3`-structured kernel.

**Current gap:** derive the odd cyclic response `r2` natively rather than by
import.

### 6. Projected-commutant Fourier law

**Type:** retained-interface positive route  
**Core idea:** use the projected commutant eigenoperator route, where the
`C_3`-even mode and `C_3`-odd mode already separate different pieces of the
microscopic data, and reinterpret those as cyclic source channels.

Use:

- [PMNS_COMMUTANT_EIGENOPERATOR_SELECTOR_NOTE.md](./PMNS_COMMUTANT_EIGENOPERATOR_SELECTOR_NOTE.md)

**Why it is attractive:** it already speaks directly in `C_3` Fourier modes.

**Why it ranks lower:** current theorem content is selector-side, not full value
law; it would need one more constructive lift.

### 7. DM odd-circulant tool transplant

**Type:** constructive transplant  
**Core idea:** transplant the exact minimal `Z_3`-covariant circulant family
from the DM neutrino lane:
```
mu I + nu(C + C^2) + i eta(C - C^2)
```
and reinterpret `(mu,nu,eta)` as the charged-lepton cyclic response carrier.

Use:

- [DM_NEUTRINO_Z3_CIRCULANT_CP_TOOL_NOTE_2026-04-15.md](./DM_NEUTRINO_Z3_CIRCULANT_CP_TOOL_NOTE_2026-04-15.md)
- [KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md](./KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)

**Why it is attractive:** the basis matches almost perfectly; the odd
generator is already exact and explicit.

**Why it ranks below #1–#6:** it is a transplant from a different physical
lane, not a fresh derivation on the charged-lepton surface.

### 8. Canonical two-Higgs right-Gram bridge transplant

**Type:** constructive transplant / extension  
**Core idea:** use the exact canonical gauge
`K_can(d,r,delta)` from the two-Higgs right-Gram bridge and map it to the
charged-lepton cyclic response law.

Use:

- [DM_NEUTRINO_TWO_HIGGS_RIGHT_GRAM_BRIDGE_NOTE_2026-04-15.md](./DM_NEUTRINO_TWO_HIGGS_RIGHT_GRAM_BRIDGE_NOTE_2026-04-15.md)

**Why it is attractive:** it is already a positive exact bridge theorem on a
circulant target family.

**Why it ranks lower:** it imports a specific extension class and a subcone
criterion before the charged-lepton source law itself is native.

### 9. Positive-parent principal-square-root source law

**Type:** constructive extension  
**Core idea:** derive a positive cyclic parent `M`, then read the cyclic
responses from its principal square root `M^(1/2)`.

Use:

- [KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md](./KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md)
- [KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md](./KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)

**Why it is attractive:** it aims directly at the eventual `√m` interpretation.

**Why it ranks lower:** it is not the simplest way to get the source law; it
mixes the source-law and readout problems too early.

### 10. Real-irrep block-democracy selector closure

**Type:** selector-only positive principle  
**Core idea:** once the three cyclic responses exist, use the unweighted
real-irrep block democracy / block-log-volume maximum to enforce the Koide
circle law.

Use:

- [HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md](./HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
- [KOIDE_CIRCULANT_CHARACTER_BRIDGE_NOTE_2026-04-18.md](./KOIDE_CIRCULANT_CHARACTER_BRIDGE_NOTE_2026-04-18.md)

**Why it is attractive:** it is already the sharpest named positive selector
candidate for `A1`.

**Why it ranks last in the source-law search:** it closes the selector only
after a source law exists; it does not provide the microscopic responses by
itself.

## Recommended immediate attack

The cleanest next attack is still **Approach 1**:

> derive the local observable-principle source law directly on the exact cyclic
> bundle `B0,B1,B2`.

Why this is the best next move:

- it is the most axiom-only route available;
- it stays on the exact retained operator surface;
- it works directly on the actual Koide carrier size (`3` responses), not a
  larger intermediate problem;
- it naturally composes with the already-identified selector candidate in
  Approach 10 if the source law lands successfully.

If that stalls, the next fallback should be **Approach 3** rather than a
high-layer transplant: go outward to the full physical lattice / taste-cube
carrier, then descend back.

## Bottom line

The positive search is now organized cleanly:

- **primary:** axiom-only cyclic source law routes,
- **secondary:** retained-interface cyclic projection routes,
- **tertiary:** transplant / extension routes.

The simplest constructive target is not generic anymore. It is:

1. derive the microscopic physical-lattice **value law** for the exact
   three-slot orbit object `(u,v,w)`,
2. then derive the selector law
   `u^2 + v^2 + w^2 = 4(uv + uw + vw)`,
3. equivalently recover the cyclic response law
   `2 r0^2 = r1^2 + r2^2`.
