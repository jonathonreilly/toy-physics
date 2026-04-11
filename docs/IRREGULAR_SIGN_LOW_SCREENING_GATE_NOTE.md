# Irregular Sign Low-Screening Gate Note

## Status: HOLD (gate not passed)

## Summary

Gate test for moving the irregular-sign lane from hold toward bounded
retention. Ran the endogenous sign closure at low screening (mu2=0.001)
on three irregular graph families with three packet families. Gate 1
(shell_packet at low screening) fails. Gate 2 (second packet family)
passes via core_packet. Lane stays on hold.

## Setup

- **Surface**: mu2=0.001 (low screening)
- **Graph families**: random_geometric (side=8), growing (n_target=64),
  layered_cycle (layers=8, width=8)
- **Seeds**: 42-46 (5 seeds), G values: 5.0, 10.0
- **Parameters**: MASS=0.3, DT=0.12, N_STEPS=15, window=[2,11)
- **Packet families**:
  1. shell_packet: exp(-r^2/2s^2) * exp(ikr) -- oscillating shell
  2. core_packet: exp(-r^2/2s^2) -- non-oscillating gaussian
  3. ring_packet: r * exp(-r^2/2s^2) * exp(ikr) -- p-wave with node at center

## Acceptance Gates

### Gate 1: Low-screening shell_packet (threshold >= 80%)

**FAIL**. Min fraction positive across all three margins: 33.3%.

| Metric | Positive | Fraction |
|--------|----------|----------|
| ball1_margin | 20/30 | 66.7% |
| ball2_margin | 13/30 | 43.3% |
| depth_margin | 10/30 | 33.3% |

The shell packet oscillation actively interferes with sign separation
at low screening. The layered_cycle family shows 0% positive on both
ball2 and depth margins. The growing family is also weak (40-60%).

### Gate 2: Second packet family (threshold >= 70%)

**PASS** via core_packet. Min fraction positive: 93.3%.

| Packet | ball1 | ball2 | depth | Min |
|--------|-------|-------|-------|-----|
| core_packet | 93.3% | 100% | 93.3% | 93.3% |
| ring_packet | 83.3% | 36.7% | 80.0% | 36.7% |

Core packet (non-oscillating gaussian) shows strong sign separation
across all graph families even at low screening. The ring packet fails
on ball2_margin (only 36.7% positive).

## Failure Diagnosis

The failure is packet-shape-dependent, not graph-family-dependent:

- **Core packet works everywhere**: 80-100% positive across all graph
  families and metrics. The non-oscillating gaussian sees clean +Phi
  vs -Phi separation at mu2=0.001.
- **Shell packet fails on layered_cycle**: 0% positive on ball2 and
  depth margins. The oscillation (exp(ikr)) creates interference that
  overwhelms the sign signal at low screening.
- **Ring packet fails on ball2**: The p-wave node structure loses
  ball2 capture discrimination, even though ball1 and depth margins
  are decent (80%+).

The oscillation in the shell packet, which is the primary observable
from the original retained result, is specifically what breaks at low
screening. The sign separator is real (core_packet proves this) but
the shell readout is not the right observable for the low-screening
regime.

## Norm Conservation

max_norm_drift = 1.3e-15 (machine precision). The Crank-Nicolson
integrator is unitarity-exact at all parameter points.

## Implications

1. The sign separator (+Phi vs -Phi) is physically real at mu2=0.001.
   Core packet confirms this at 93%+ across all families.
2. The shell packet oscillation is the wrong readout for low screening.
   It creates interference patterns that mask the sign signal.
3. Lane stays on hold because the primary observable (shell packet)
   does not transfer to the low-screening surface.
4. A possible path forward: redefine the primary observable to use the
   core (non-oscillating) packet, which shows robust sign separation.
   But that changes the retained claim, so it needs its own review.

## Script

`scripts/frontier_irregular_sign_low_screening_gate.py`
