# Route Portfolio — Cycle 21 PMNS Branch Selector

Five candidate routes were considered for resolving the Branch A
(0.1888) vs Branch B (1.0) selector ambiguity.

| route | type | (a) closing | (b) obstruction | (c) depth | (d) time | rank |
|-------|------|-------------|------------------|-----------|----------|------|
| A | information-theoretic | 0 | 1 | 2 | low | 4 |
| B | action-theoretic | 0 | 1 | 2 | low | 5 |
| C | transport-extremal | 0 | 1 | 2 | medium | 3 |
| D | symmetry/parity (CP-sheet blindness) | 0 | 3 | 3 | low | **1** |
| E | direct comparison + counterfactual | 0 | 2 | 2 | medium | 2 |

## Route A — information-theoretic (rank 4)

The min-info selector chooses the off-seed source minimizing
`D_KL(x||x_seed) + D_KL(y||y_seed) + (1 - cos δ)`. Output: η/η_obs
= 1 on column 0 with a specific source.

**Score (a) closing**: 0. The minimum-information functional is an
**imported** information-geometric quantity. It is not derivable
from the current Cl(3) staggered Dirac structure or from current
CPT structure on the current bank.

**Score (b) obstruction**: 1. The functional has no first-principles
derivation in the framework. Naming this gap is the obstruction
already named in the source note.

**Verdict**: dominated by Route D, which gives a structural EXCLUSION
of Route A as a unique selector.

## Route B — action-theoretic (rank 5)

The observable-relative-action selector chooses the source minimizing
`S_rel(H_e || H_seed) = Tr(H_seed^{-1} H_e) - log det(H_seed^{-1} H_e) - 3`.

**Score (a) closing**: 0. While the `log det` factor connects to the
current scalar observable principle (cycle 03), the `Tr` and `-3`
terms are not framework-native. The objective is an imported
action-functional, not a Cl(3)-derived stationary principle.

**Score (b) obstruction**: 1. The closing question "does the sole
axiom force stationary minimal relative bosonic action on the fixed
seed surface?" is explicitly named in the source note. Answering it
is a substantial multi-step derivation chain.

**Verdict**: dominated by Route D plus the lower (a) closing score
for any specific action functional.

## Route C — transport-extremal (rank 3)

The transport-extremal selector chooses the source extremizing the
flavored transport functional `max_i η_i / η_obs`.

**Score (a) closing**: 0. This is "use η_obs as the selector" — a
**circular** selector if η_obs is the unknown to be derived. It also
already uses η_obs as a derivation input (forbidden import).

**Score (b) obstruction**: 1. The selector cannot be a closing
derivation of η.

**Verdict**: rejected as a forbidden-import violation when used as a
selector for `η_obs` itself.

## Route D — symmetry/parity (CP-sheet blindness) — rank 1

The cited CP-sheet blindness theorem proves that EVERY
current Branch-B selector objective is even under δ → -δ, while
the baryogenesis source channel `γ = x_1 y_3 sin(δ)` is odd. So
every Branch-B "winner" comes paired with its CP-conjugate "winner"
of equal selector value.

**Score (a) closing**: 0 — this is a negative result, not a positive
selector.

**Score (b) obstruction**: 3 — this is a maximum-strength NAMED
obstruction. It rules out the entire current Branch-B selector
bank as a candidate uniqueness law. Branch B cannot, with current
selectors, choose a unique baryogenesis witness; it can at best
choose a CP-symmetric pair.

**Score (c) content depth**: 3 — gives a structural reason WHY no
Branch-B closure of η can be unique.

**Verdict**: this is the cleanest, most structural result that can
be made on the current bank. It excludes the current Branch-B selector
bank as a unique-selection law: Branch A is not a Branch-B selector,
hence does not have the parity problem; Branch A's prediction (cycle
18's 0.1888 decomposition) is already a unique numerical output that
does not require choosing among CP-conjugate pairs.

## Route E — direct comparison + counterfactual — rank 2

Enumerate the two branches' physical consequences and identify
framework-native selection criteria that don't reduce to PDG fits.

**Score (a) closing**: 0 — does not derive a positive selector.

**Score (b) obstruction**: 2 — gives a comparison map.

**Score (c) content depth**: 2 — useful diagnostic but secondary
to Route D.

**Verdict**: complementary to Route D. The runner will incorporate
Route E's comparison data as a counterfactual section.

## Selected route: D + supporting E

Route D is selected as the primary cycle output because:

1. It is a structural exclusion theorem on the current bank (using
   the cited CP-sheet blindness premise).
2. It sharpens the branch-selector ambiguity by exclusion: no
   current Branch-B selector can choose a unique baryogenesis
   witness, hence Branch B cannot uniquely close η under this bank.
3. By contrast, Branch A produces 0.1888 deterministically (cycle
   18's structural decomposition).
4. The PR delivers (a) named obstruction, (b) structural insight,
   (c) verification runner, and (d) Route-E counterfactual.

Route E provides supporting numerical comparison and counterfactual
analysis (a hypothetical CP-odd selector would break the parity
problem; what would such a functional look like?).
