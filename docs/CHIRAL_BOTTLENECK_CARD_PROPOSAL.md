# Chiral Expanded Core Card

**Date:** 2026-04-10  
**Scope:** replace the old 10-row closure card as the primary front-door card
with an expanded core card that catches both operating-point health and the
structural bottlenecks that keep surfacing later.

The old 10-row card is still useful, but it is not sufficient. A model can go
`10/10` there and still fail on:

- multi-D dispersion and isotropy
- genuine 3D gauge loops
- fixed-`theta` chromaticity
- fused mass and gravity coupling
- periodic recurrence sensitivity
- observable mismatch
- state-family / preparation sensitivity

So the best current core card is **N = 17** rows:
- **C1-C10:** operating-point card
- **C11-C17:** structural bottleneck card

Optional:
- **C18:** growth / backreaction separation

## Expanded Core Card (N = 17)

| Row | Test | What it measures | Why it belongs in the core card | Current branch read |
|---|---|---|---|---|
| C1 | Born barrier / slit `|I3|/P` | pairwise/Born interference law under blocking | still the cleanest non-negotiable linearity/interference gate | retained in CH-1D / CH-2D / CH-3D operating point |
| C2 | `d_TV` / slit distinguishability | branch separation after blocking | checks whether the slit harness is informative rather than degenerate | retained |
| C3 | null control (`k=0` or `f=0`) | no-field / no-phase baseline | protects against built-in drift being mistaken for gravity | retained |
| C4 | `F∝M` scaling | weak-field linear mass/strength response | keeps the gravity claim honest at first order | retained in chiral operating points |
| C5 | gravity sign at retained operating point | whether the branch has a real TOWARD point | still needed as the minimal gravity gate | retained, but no longer sufficient by itself |
| C6 | decoherence / record proxy | whether branch-separation survives weak environment coupling | still a core observable for the measurement side | retained but bounded |
| C7 | mutual information | branch correlation strength | useful companion to decoherence / purity | retained |
| C8 | purity stability | whether the record proxy is stable across the scanned window | guards against one-off purity positives | retained |
| C9 | gravity grows with propagation | whether the signal is a real trend instead of one lucky layer count | still needed for operating-point sanity | retained |
| C10 | distance law | how the gravity response decays with offset | still needed, but no longer overinterpreted as the whole gravity story | retained with caveats |
| C11 | 3D KG isotropy / coupled-coin dispersion | `E^2` vs `k^2` along axes and diagonals, isotropy ratio | first fast detector of factorized 3D transport | factorized CH-3D fails; generic coupled `6x6` helps but only the `DIR-3D` Hamiltonian lane closes KG cleanly |
| C12 | 3D gauge-loop / AB visibility | Wilson-loop / enclosed-flux response on the same 3D transport | first fast detector of missing cross-axis coupling | factorized CH-3D fails; `DIR-3D` flux-tube restores nonzero AB (`V=0.519`) |
| C13 | fixed-`theta` `k`-achromaticity | deflection CV across carrier `k` at matched travel distance | catches wave-window gravity before it is sold as structural gravity | current CH-1D fails (`CV_k ≈ 2.66`) |
| C14 | split mass vs gravity susceptibility | independent sweep of free mass gap and gravity coupling | tests whether inertial mass and gravity response are fused | current split model helps but does not solve everything |
| C15 | boundary-condition robustness | same `delta = d/n`, `lambda = L/n` point under periodic / reflecting / open boundaries | catches recurrence / wrap artifacts before they become doctrine | current 3+1D periodic sign windows are mostly boundary-sensitive |
| C16 | multi-observable gravity consistency | compare first-arrival, peak, current, centroid, torus-aware centroid | forces us to separate geometric drift from wave readout | concrete on `DIR-3D`; centroid/shell agree best, peak is not a reliable gravity gate |
| C17 | state-family robustness | rerun the same gravity claim across packet-family / polarization / chirality / sublattice preparations | blocks sector-conditioned “perfect cards” from being promoted as universal architecture wins | weak-coin chiral + potential scores on the default `R` packet but flips sign on `L` and symmetric families |

## Optional Row

| Row | Test | What it measures | Why it is optional |
|---|---|---|---|
| C18 | growth / backreaction separation | whether growth fails because it is applied to a coherent state instead of to records/currents | extremely important, but secondary to fixing the transport bottlenecks first |

## Ordering

The card should be run in this order:

1. `C1-C5`: prove the operating point is not nonsense
2. `C11-C17`: prove the architecture is not structurally broken
   If factorized CH-3D fails here, the next move is not “keep tuning the same separable coin”; it is to jump to an irreducible 3+1D transport law such as the Dirac Hamiltonian lane.
3. `C6-C10`: add the measurement and scaling context
4. `C18` if growth or endogenous backreaction is in scope

That ordering is deliberate. The repo’s failure pattern has been:

- a branch looks healthy on an operating point
- a later moonshot reveals a structural bottleneck
- the bottleneck should have been screened much earlier

The expanded card fixes that.

## Immediate Implementation Mapping

- `C1-C10`: existing chiral closure-card harnesses
- `C11-C12`: `scripts/frontier_chiral_3plus1d_coupled_coin_scan.py`, with the stronger current 3+1D closure route in `scripts/frontier_dirac_walk_3plus1d_core_card.py`
- `C13-C14`: `scripts/frontier_chiral_split_mass_gravity.py` plus the literal integrated `DIR-3D` rows now wired in `scripts/frontier_dirac_walk_3plus1d_core_card.py`
- `C15`: `scripts/frontier_chiral_3plus1d_boundary_phase_diagram.py`, with the analogous `DIR-3D` robustness row now wired in `scripts/frontier_dirac_walk_3plus1d_core_card.py`
- `C16`: prototype exists in `scripts/frontier_dirac_walk_3plus1d_observable_panel.py` and is now wired into `scripts/frontier_dirac_walk_3plus1d_core_card.py`
- `C17`: `scripts/frontier_weakcoin_16card.py` is the first clean motivating example; future promotion candidates should include the same packet-family sweep explicitly

The newer `DIR-3D` scans add one more practical lesson:

- source smoothing changes local windows but does not remove the growth/sign failure
- field smoothing can clean up the offset law without fixing `N`-monotonicity
- weaker coupling does not rescue the sign structure

So the remaining 3+1D Dirac problem should now be attacked mainly as a
geometry/recurrence problem, not as a source-shape or coupling-magnitude
problem.

## Bottom Line

The best current core card is not “10 rows plus some moonshots later.”

It is:
- **a 17-row front-door card**
- with the old closure rows kept
- and the seven structural bottleneck rows promoted into the core path

That gives us the right shape of operating environment much earlier.
