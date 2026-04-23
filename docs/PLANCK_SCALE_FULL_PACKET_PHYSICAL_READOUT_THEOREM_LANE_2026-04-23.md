# Planck-Scale Full-Packet Physical Readout Theorem Lane

**Date:** 2026-04-23  
**Status:** science-only full-packet readout classification theorem plus sharpest remaining physical-law boundary  
**Audit runner:** `scripts/frontier_planck_full_packet_physical_readout_theorem_lane.py`

## Question

The boundary Planck route is now reduced to one exact missing statement:

`p_phys = Tr(rho_cell P_A)`,

where:

- `P_A` is the section-canonical four-axis `hw=1` worldtube packet;
- `P_q` is the Schur-visible rank-2 quotient block;
- `P_E` is the exact hidden rank-2 `E`-doublet complement;
- `P_A = P_q + P_E`;
- under the democratic full-cell state,

  `Tr(rho_cell P_q) = 1/8`,
  `Tr(rho_cell P_E) = 1/8`,
  `Tr(rho_cell P_A) = 1/4`.

The exact remaining question is:

> why should physical boundary pressure count the **full packet**
>
> `P_A`,
>
> rather than only the Schur-visible quotient
>
> `P_q`?

Equivalently:

> is there now a genuine full-packet readout theorem, or is the route still
> waiting on one final physical promotion law?

## Bottom line

The strongest honest result is:

1. the current lane already fixes the **physical coarse packet**

   `P_A`;

2. the missing factor of `2` is already closed:

   `P_A = P_q + P_E`,
   `Tr(rho_cell P_A) = 2 Tr(rho_cell P_q)`;

3. the normalized Schur/Perron route cannot recover quarter from hidden
   weighting; it fixes only the **shape** of the axis-sector state, not the
   total occupation;

4. once one asks for a **packet-local positive additive readout** on the exact
   physical packet `H_A = H_q (+) E` that:

   - agrees with the Schur-visible quotient count on `H_q`,
   - is residual-invariant inside the exact blocks,
   - and uses no extra same-shell weighting datum beyond the already fixed
     packet decomposition,

   every such readout has the form

   `R_alpha(rho) = Tr(rho P_q) + alpha Tr(rho P_E)`,

   with `alpha >= 0`;

5. the quotient-only readout `alpha = 0` is not physically admissible on the
   current lane, because it throws away the exact physical `E` block and
   thereby factors through the forbidden proper quotient `P_q`;

6. the **no-extra-datum full-packet completion principle** fixes

   `alpha = 1`,

   hence the unique full-packet readout is

   `R_full(rho) = Tr(rho P_A)`;

7. on the democratic full-cell state,

   `R_full(rho_cell) = Tr(rho_cell P_A) = 1/4`;

8. therefore the direct readout lane is now sharpened to one final physical
   promotion:

   > physical boundary pressure is the full-packet occupation readout on the
   > section-canonical worldtube packet.

So this note lands a real theorem, but not yet retained Planck closure.

What is now closed:

- full packet `P_A` is forced;
- hidden multiplicity is physical and exact;
- every packet-local additive completion of the quotient count is classified;
- quarter is the unique **no-extra-datum full-packet completion**.

What is still open:

> whether physical boundary pressure is in fact this full-packet readout,
> rather than the current scalar Schur observable.

That is narrower than the old open statement `p_phys = m_axis`, because the
carrier, the lift, and the packet-completion class are now fixed. The only
remaining law is the physical promotion from scalar Schur observable to
full-packet readout.

## Inputs

This lane uses only already-opened branch-local results:

- [PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_WEIGHTED_C16_STATE_FROM_SCHUR_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_WEIGHTED_C16_STATE_FROM_SCHUR_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_POSITIVE_RESIDUAL_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_POSITIVE_RESIDUAL_THEOREM_LANE_2026-04-23.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

What those lanes already fix exactly:

1. the coarse physical worldtube selector is the full packet

   `P_A`;

2. the Schur-visible quotient is

   `P_q = |t><t| + |s><s|`;

3. the hidden complement is the exact rank-2 `E` block

   `P_E`,

   with

   `P_A = P_q + P_E`,
   `P_q P_E = 0`;

4. the democratic full-cell masses are

   `Tr(rho_cell P_q) = 1/8`,
   `Tr(rho_cell P_E) = 1/8`,
   `Tr(rho_cell P_A) = 1/4`;

5. the normalized Schur/Perron route cannot recover quarter by itself;
6. the current scalar observable principle on the Schur carrier selects

   `p_vac(L_Sigma)`,

   not quarter.

This note attacks the remaining direct readout law.

## Setup

Work on the exact coarse worldtube carrier

`H_A = span{|t>, |x>, |y>, |z>}`.

Let

`|s> = (|x> + |y> + |z>) / sqrt(3)`

and let `E` be the exact spatial doublet block

`E = {a_x |x> + a_y |y> + a_z |z> : a_x + a_y + a_z = 0}`.

Choose any orthonormal basis `|e_1>`, `|e_2>` of `E` and define

`P_q = |t><t| + |s><s|`,

`P_E = |e_1><e_1| + |e_2><e_2|`,

`P_A = P_q + P_E`.

By the multiplicity-lift lane:

- `rank(P_q) = 2`,
- `rank(P_E) = 2`,
- `rank(P_A) = 4`,
- `Tr(rho_cell P_q) = 1/8`,
- `Tr(rho_cell P_E) = 1/8`,
- `Tr(rho_cell P_A) = 1/4`.

So the only remaining question is no longer packet support or multiplicity. It
is the scalar readout law on this already fixed packet.

## Definition: packet-local additive readout extension

Call a scalar `R` on positive block states over `H_A = H_q (+) E` a
**packet-local additive readout extension** of the Schur-visible quotient count
if:

1. **packet-locality**
   `R` depends only on the restriction of the state to `H_A`;
2. **orthogonal additivity**
   for block-diagonal packet states
   `rho = rho_q (+) rho_E`,

   `R(rho) = R_q(rho_q) + R_E(rho_E)`;

3. **positivity**
   `R(rho) >= 0` for every positive packet state;
4. **quotient agreement**
   on the visible quotient block,

   `R_q(rho_q) = Tr(rho_q)`;

5. **residual blindness inside blocks**
   no finer datum inside `H_q` or inside `E` is used beyond the exact block
   decomposition already fixed on the current lane.

This is the smallest class that still deserves to be called a full-packet
completion of the Schur-visible packet count.

## Theorem 1: exact classification of packet-local additive completions

Every packet-local additive readout extension is exactly of the form

`R_alpha(rho) = Tr(rho P_q) + alpha Tr(rho P_E)`,

for one coefficient `alpha >= 0`.

### Proof

By orthogonal additivity on `H_A = H_q (+) E`, the readout splits into one
scalar on `H_q` and one scalar on `E`.

By quotient agreement, the visible piece is already fixed:

`R_q(rho_q) = Tr(rho_q)`.

By residual blindness inside `E`, the invisible piece cannot depend on any
finer projector than the identity on `E`, so it is necessarily proportional to
`Tr(rho_E)`.

Positivity forces the proportionality coefficient to be nonnegative.

So the whole family is exactly

`R_alpha(rho) = Tr(rho P_q) + alpha Tr(rho P_E)`,

with `alpha >= 0`.

This proves that the direct readout problem is now only one-parameter.

## Theorem 2: quotient-only readout is physically inadmissible

The choice `alpha = 0` is not admissible as a physical readout on the current
lane.

### Reason

`alpha = 0` gives

`R_0(rho) = Tr(rho P_q)`,

which discards the exact `E` block completely.

But the current lane already fixes:

- the physical coarse packet is the full section-canonical packet `P_A`,
  not the quotient packet `P_q`;
- the hidden `E` block is exact physical multiplicity, not gauge redundancy;
- no proper exact quotient / reduction preserving retained observable-sector
  semantics is admissible on the accepted physical-lattice surface.

So `alpha = 0` is precisely the forbidden proper-quotient readout.

This closes the old “maybe pressure only sees the visible Schur quotient”
escape hatch.

## Theorem 3: no-extra-datum full-packet completion fixes `alpha = 1`

Assume the physical packet readout introduces **no new same-shell weighting
datum** between the already fixed exact blocks `H_q` and `E`.

Then the unique packet-local additive completion is

`R_full(rho) = Tr(rho P_q) + Tr(rho P_E) = Tr(rho P_A)`.

### Proof

By Theorem 1, every additive packet-local completion is `R_alpha`.

The only remaining freedom is the relative coefficient `alpha` on the exact
same-shell exact-complement block `E`.

Setting `alpha != 1` introduces one new relative weight datum between two
blocks that are already fixed by the exact packet decomposition.

So the no-extra-datum completion principle fixes the unique unweighted
completion:

`alpha = 1`.

Therefore

`R_full(rho) = Tr(rho P_A)`.

This is the exact full-packet readout theorem on the current lane.

## Corollary 1: quarter is the unique no-extra-datum full-packet value

On the democratic full-cell state

`rho_cell = I_16 / 16`,

the classified packet-completion family gives

`R_alpha(rho_cell) = Tr(rho_cell P_q) + alpha Tr(rho_cell P_E) = 1/8 + alpha/8`.

So:

- `alpha = 0` gives `1/8`,
- `alpha = 1` gives `1/4`,
- and `1/4` occurs if and only if `alpha = 1`.

Therefore quarter is the unique no-extra-datum full-packet completion of the
Schur-visible quotient count.

## Corollary 2: action-side closure under full-packet readout

The action lane already gives

`p_*(nu) = nu - lambda_min(L_Sigma)`.

On the canonical witness

`lambda_min(L_Sigma) = 1`.

So if physical boundary pressure is the full-packet readout,

`p_phys = R_full(rho_cell) = Tr(rho_cell P_A) = 1/4`,

then the exact witness vacuum-action density is

`nu = lambda_min(L_Sigma) + 1/4 = 5/4`.

So the whole boundary Planck route closes immediately **if** physical boundary
pressure is identified with the full-packet readout.

## Honest endpoint

This note does **not** prove that the present scalar Schur observable

`p_vac(L_Sigma)`

is equal to the full-packet readout.

It proves something narrower and cleaner:

1. the full packet, not the quotient, is the physical coarse carrier;
2. every additive packet-local completion of the quotient count is classified
   by one coefficient `alpha`;
3. quarter is exactly the unique no-extra-datum completion `alpha = 1`;
4. therefore the only remaining physical promotion law is:

   > physical boundary pressure is the full-packet occupation readout on the
   > section-canonical worldtube packet.

That is sharper than the old open statement `p_phys = m_axis`, because:

- the packet is now fixed;
- the factor of `2` is now fixed;
- the completion family is now fixed;
- the only remaining content is the promotion from scalar Schur observable to
  packet readout.

## Safe wording

**Can claim**

- the direct readout problem is now classified by one coefficient `alpha`
  multiplying the hidden `E` block;
- quotient-only readout `alpha = 0` is physically inadmissible on the current
  lane;
- quarter is the unique no-extra-datum full-packet completion, namely
  `alpha = 1`;
- exact boundary Planck closure on this route is now equivalent to promoting
  physical boundary pressure to the full-packet readout
  `Tr(rho_cell P_A)`.

**Cannot claim**

- that the current scalar Schur observable principle already proves this
  promotion;
- that retained Planck closure is finished without the final physical readout
  promotion.

## Command

```bash
python3 scripts/frontier_planck_full_packet_physical_readout_theorem_lane.py
```
