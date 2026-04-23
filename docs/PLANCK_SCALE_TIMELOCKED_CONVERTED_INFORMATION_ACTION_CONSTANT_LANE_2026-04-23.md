# Planck-Scale Time-Locked Converted Information/Action Constant Lane

**Date:** 2026-04-23  
**Status:** science-only theorem-grade sharpening on the converted information
route; not a closure theorem  
**Audit runner:** `scripts/frontier_planck_timelocked_converted_information_action_constant_lane.py`

## Question

After the exact spacetime lock

`a_s = c a_t`,

can the surviving converted information theorem

`q_* = kappa_info I_*`

be finished on the exact time-locked `3+1` carrier?

Equivalently:

- maybe the time-lock picks a unique elementary information quantum;
- maybe that forces the phase-per-information constant `kappa_info`;
- maybe the missing Planck coefficient only closes after spatial and temporal
  units are locked.

## Bottom line

Not fully, but the target is much sharper.

The exact time-lock does **not** derive `kappa_info`. What it does derive is a
canonical democratic information carrier on the minimal `3+1` block:

`p(beta) = (1, 1, 1, beta) / (3 + beta)`

with

`beta = (c a_t / a_s)^2`.

The retained scalar `3+1` bridge forces `beta = 1`, so the time-locked carrier
is exactly

`p_* = (1/4, 1/4, 1/4, 1/4)`.

On the standard finite-information class built from that normalized carrier,
the canonical Shannon/von Neumann information is therefore

`I_* = log 4` nats `= 2` bits.

So the converted information/action route is no longer vague on this carrier.
It reduces to one exact target constant:

`q_* = kappa_info log 4`

and, on the natural minimal cubical defect `eps_* = pi/2`, exact conventional
Planck would require

`kappa_info^(nat) = 1 / (16 log 4) = 1 / (32 log 2)`

or equivalently

`kappa_info^(bit) = 1 / 32`.

That is a real sharpening.

But it is **not** yet a closure theorem, because the exact time-lock does not
derive the conversion law itself. It only fixes the democratic information
content of the carrier on which such a law would have to act.

So the honest verdict is:

- **time-lock fixes the candidate information quantum on the minimal `3+1`
  carrier;**
- **time-lock does not yet derive the phase-per-information constant
  `kappa_info`;**
- **the surviving theorem target is now exact and simple: derive why the
  elementary locked carrier realizes `kappa_info = 1/32` per bit.**

## Inputs

This lane uses:

- [PLANCK_SCALE_INFORMATION_ACTION_UNIT_MAP_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_INFORMATION_ACTION_UNIT_MAP_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md)
- [PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md](./PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md](./PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md)
- [UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md](./UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md)
- [S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md](./S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md)

## The time-locked democratic carrier

The earlier spacetime lane enlarged the exact scalar `3+1` bridge to the
anisotropic family

`K_beta(omega) = 3 + beta sin^2(omega)`,

with

`beta = (c a_t / a_s)^2`.

That family exposes the only hidden relative space/time calibration parameter
on the minimal block.

To extract the associated information carrier, normalize the four
spatial/temporal weights:

`p(beta) = (1, 1, 1, beta) / (3 + beta)`.

This is the exact same minimal `3+1` content as the scalar kernel, but now
written as a normalized finite alternative:

- three equal spatial channels,
- one temporal channel with relative weight `beta`.

The exact retained scalar ratio `A_inf / A_2 = 2 / sqrt(3)` forces `beta = 1`.
Therefore the time-locked carrier is exactly the uniform four-state carrier

`p_* = (1/4, 1/4, 1/4, 1/4)`.

So the derived time direction does produce a real information-theoretic gain:
it turns the anisotropic family into one canonical democratic four-channel
carrier.

## Exact information on the locked carrier

Within the standard finite-information class already under discussion, the
canonical Shannon/von Neumann information of `p(beta)` is

`I(beta) = -sum_i p_i(beta) log p_i(beta)`

`       = log(3 + beta) - beta log(beta) / (3 + beta)`.

Its derivative is exact:

`I'(beta) = -3 log(beta) / (3 + beta)^2`.

Therefore:

- `I'(beta) > 0` for `0 < beta < 1`;
- `I'(beta) = 0` at `beta = 1`;
- `I'(beta) < 0` for `beta > 1`.

So `beta = 1` is the unique stationary point and the unique global maximum on
the positive anisotropic family.

At that exact time-lock point,

`I_* = I(1) = log 4`.

Equivalently:

- `I_* = log 4` in nats;
- `I_* = 2` in bits.

This is the precise sense in which time-lock sharpens the information lane:
the minimal spacetime carrier becomes an exact democratic four-state carrier.

## Converted law on the locked carrier

The earlier information/action lane already ruled out the direct
identifications

- `q_* = I_*`,
- `q_* = log Z_*`,

and reduced the surviving route to a converted theorem

`q_* = kappa_info I_*`.

On the exact time-locked carrier, this becomes

`q_* = kappa_info^(nat) log 4`

or equivalently

`q_* = kappa_info^(bit) * 2`,

with the two conventions related by base compensation:

`kappa_info^(bit) = kappa_info^(nat) log 2`.

So the time-lock removes one ambiguity but not the last one:

- it fixes the carrier information content,
- it does not yet fix the conversion constant that turns information into
  action phase.

## Exact Planck target on the locked carrier

The elementary action-phase reduction theorem gives

`a^2 / l_P^2 = 8 pi q_* / eps_*`.

On the natural minimal cubical defect,

`eps_* = pi/2`,

so

`a^2 / l_P^2 = 16 q_*`.

Substituting the time-locked converted law yields

`a^2 / l_P^2 = 16 kappa_info^(nat) log 4`

or

`a^2 / l_P^2 = 32 kappa_info^(bit)`.

Therefore exact conventional `a = l_P` on this specific locked carrier would
require

`kappa_info^(nat) = 1 / (16 log 4) = 1 / (32 log 2)`

or equivalently

`kappa_info^(bit) = 1 / 32`.

This is the cleanest surviving target on the information lane:

> one bit of the exact locked elementary carrier would have to contribute
> exactly `1/32` of the dimensionless action phase.

## Why this still does not close the lane

Three real gaps remain.

### 1. Time-lock fixes `I_*`, not `kappa_info`

The exact scalar `3+1` bridge collapses `beta` to `1`, so it fixes the
democratic information content of the carrier. But nothing in the current
retained stack turns that information content into a physical phase law.

So the time-lock kills anisotropy in the information carrier, not the final
phase-per-information ambiguity.

### 2. Base compensation still leaves a free physical constant

The earlier log-base objection still applies. The physical law can only be

`q_* = kappa_info I_*`

with inverse base compensation between `kappa_info` and the information unit.

The time-lock does not eliminate that; it only makes the carrier content
simple enough that the exact target constant can be written cleanly.

### 3. The common spacetime scale ray is still homogeneous

Even after `a_s = c a_t`, the common spacetime rescaling

`a -> lambda a`

leaves the locked carrier probabilities and their entropy unchanged. So the
time-lock does not secretly anchor the absolute unit through the information
side either.

## The theorem-level statement

**Theorem (Time-locked converted information constant sharpens but does not
close).**
Assume:

1. the anisotropic minimal `3+1` family
   `p(beta) = (1, 1, 1, beta) / (3 + beta)`;
2. the exact derived-time lock `beta = 1`;
3. the surviving converted information/action law
   `q_* = kappa_info I_*`;
4. the elementary action-phase reduction
   `a^2 / l_P^2 = 8 pi q_* / eps_*`.

Then:

1. the locked carrier is exactly the democratic four-state carrier
   `p_* = (1/4, 1/4, 1/4, 1/4)`;
2. its canonical Shannon/von Neumann information is exactly
   `I_* = log 4` nats `= 2` bits;
3. on the minimal cubical defect `eps_* = pi/2`, the converted Planck relation
   becomes
   `a^2 / l_P^2 = 16 kappa_info^(nat) log 4 = 32 kappa_info^(bit)`;
4. therefore exact conventional `a = l_P` on this carrier would require
   `kappa_info^(nat) = 1 / (32 log 2)` or equivalently
   `kappa_info^(bit) = 1 / 32`;
5. but the current retained stack does not derive that constant, so the lane
   is sharpened to one exact target constant rather than closed.

## What this closes

This closes two imprecisions in the surviving information route.

1. The converted theorem target is no longer an arbitrary pair
   `(I_*, kappa_info)` on an unspecified carrier.
   On the exact time-locked minimal `3+1` carrier, the canonical democratic
   information content is fixed to `log 4` nats or `2` bits.
2. The exact Planck target constant is now explicit:
   `kappa_info^(bit) = 1/32`.

So the information lane now has a concrete same-surface question:

> why should one bit on the exact locked elementary spacetime carrier produce
> `1/32` of the dimensionless action phase?

## What this does not close

This note does **not** prove:

- that Shannon/von Neumann information is already the physical action phase;
- that the converted law `q_* = kappa_info I_*` has been derived;
- that `kappa_info = 1/32` per bit is a retained theorem;
- that the common spacetime scale ray is broken.

It proves only the sharper statement:

- **time-lock fixes the democratic elementary information content,**
- **not yet the action-per-information conversion constant.**

## Safe wording

Use:

> On the exact time-locked minimal `3+1` carrier, the surviving converted
> information/action route sharpens to a single exact target constant. The
> carrier’s canonical democratic information content is `log 4` nats (`2`
> bits), so exact conventional Planck on the minimal cubical defect would
> require `kappa_info = 1/(32 log 2)` in natural units, equivalently `1/32`
> per bit. This is a theorem-grade narrowing, not yet a closure theorem.

Avoid:

> The time-locked information lane derives Planck.

That would overstate what is actually proved here.
