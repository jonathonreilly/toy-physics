# Current Review State: `codex/p-derivation-package`

## Verdict

The original fake analytic-closure claim has been removed.

This branch now does contain a real exact finite-`beta` law for the plaquette
on the retained same-surface evaluation surface:

- `docs/CHARACTER_INTERTWINER_FOAM_LAW_NOTE.md`

So the branch is no longer only a support package. It now carries:

- an exact finite-periodic-lattice character/intertwiner foam derivation of
  the plaquette law
- exact low-carrier sector theorems that identify the first explicit pieces of
  that law

What it still does **not** contain is a compact low-carrier closed form or a
small-state recursion that sums that exact law efficiently.

It now also contains the exact no-go that settles the finite-compression
question:

- `docs/FINITE_BX_LOW_CARRIER_NO_GO_NOTE.md`

So the branch no longer has an open “maybe the full exact law collapses to a
small finite `B/X` package” ambiguity. That possibility is now ruled out.

It now also contains the exact constructive replacement:

- `docs/POISSONIZED_OCCUPATION_INTERTWINER_COMPRESSION_NOTE.md`

So the branch no longer stops at a pure no-go. It now has an exact useful
resummed/state-compressed representation of the infinite-carrier law.

It now also contains the exact finite local evaluator state-space theorem:

- `docs/POISSONIZED_LINK_CHANNEL_COMPRESSION_NOTE.md`

So the branch no longer stops at plaquette occupation compression alone. The
truncated evaluator is now an exact finite-state tensor network with explicit
link-channel alphabets.

The exact package now includes:

- exact pure-gauge source identity for the plaquette
- exact `SU(3)` one-plaquette block
- exact strong-coupling slope theorem
- exact no-go against the proposed constant-lift closure
- exact first nonlocal connected correction beyond the one-plaquette block
- corrected exact rooted `3`-chain coefficient engine through five `3`-cells
- exact no-go against boundary-shellable rooted growth
- exact local directed-cell boundary-cluster theorem
- exact root-face odd-parity launch theorem
- exact no-go against directed-cell face-slot factorization at `n = 3`
- bounded rejection of the weakest local face-closure axiom
- exact no-go against one-shell face-state multiset closure
- exact `4`-cube same-boundary hidden-completion theorem
- exact constructive cubical quotient theorem for finite rooted `3`-chains
- exact quotient-distinct same-boundary surface engine through five `3`-cells
- exact quotient-surface gas route at fixed `beta = 6`
- exact finite-lattice character/intertwiner foam law at fixed `beta = 6`
- exact no-go against quotient-surface-only rooted transfer
- exact finite local hidden-shell channel theorem for the first quotient sector

It is a canonical replacement for the claim that the plaquette law was only
implicitly defined. The law is now explicit. What remains non-canonical is any
claim of a compact low-carrier closure or closed-form number.

## What was fixed

The unsupported claim

`P(beta) = P_1plaq(beta * (3/2) * (2/sqrt(3))^(1/4))`

has been removed.

The scalar `3+1` temporal-completion step was deleted from this package because
it never reached the pure-gauge Wilson source sector.

The replacement package now proves the exact gauge-side statement that matters:

`dP_full / d beta |_(0) = dP_1plaq / d beta |_(0) = 1/18`.

So any exact constant-lift identity

`P_full(beta) = P_1plaq(c beta)`

would force

`c = 1`.

That directly rules out the old proposal.

The branch also now records the correct next route in
`docs/PLAQUETTE_OPEN_SURFACE_HIERARCHY_NOTE.md`: the plaquette is an
open-surface hierarchy problem, and the first nonlocal completions already
appear as `4` exact area-`5` cube complements on the `3+1` lattice.

That route now has its first constructive theorem in
`docs/PLAQUETTE_FIRST_NONLOCAL_CONNECTED_CORRECTION_NOTE.md`:

`P_full(beta) = P_1plaq(beta) + beta^5 / 472392 + O_nonlocal(beta^6)`.

It now also has the next exact engine in
`docs/ROOTED_3CHAIN_COEFFICIENT_ENGINE_NOTE.md`:

- corrected exact rooted same-boundary counts through `|V| = 5`
- exact proof that boundary-shellable rooted growth was undercounting
- corrected local-resummed partial dressing
- exact proof that directed-cell face-slot factorization is already false at
  `n = 3`

The branch now also has the exact local closure surface:

- `docs/DIRECTED_CELL_BOUNDARY_CLUSTER_THEOREM_NOTE.md`
- `docs/ROOT_FACE_LAUNCH_THEOREM_NOTE.md`
- `docs/DIRECTED_CELL_BOUNDARY_STATE_TRANSFER_NOTE.md`

and one explicit rejected closure attempt:

- `docs/LOCAL_FACE_CLOSURE_REJECTION_NOTE.md`

The branch now also has the next stronger exact closure no-go:

- `docs/ONE_SHELL_FACE_STATE_TRANSFER_NO_GO_NOTE.md`

and the next exact hidden rooted-volume sector:

- `docs/SAME_BOUNDARY_HYPERCUBE_COMPLEMENT_NOTE.md`

That hidden sector is now integrated into the real physical counting object by:

- `docs/CUBICAL_QUOTIENT_THEOREM_NOTE.md`
- `docs/QUOTIENT_SURFACE_ENGINE_NOTE.md`

The current canonical closure route is therefore no longer a raw rooted-filling
transfer. It is the quotient-distinct anchored surface gas summarized in:

- `docs/ANCHORED_SURFACE_GAS_ROUTE_NOTE.md`

The exact next obstruction on that route is now:

- `docs/QUOTIENT_SURFACE_TRANSFER_NO_GO_NOTE.md`

The exact first constructive enriched-state replacement is now:

- `docs/HIDDEN_SHELL_CHANNEL_THEOREM_NOTE.md`
- `docs/HIDDEN_TWO_SHELL_PROPAGATION_THEOREM_NOTE.md`
- `docs/HIDDEN_TWO_SHELL_CHANNEL_THEOREM_NOTE.md`
- `docs/FUNDAMENTAL_DISK_ACTIVITY_THEOREM_NOTE.md`
- `docs/FIRST_NONDISK_Z3_LIFT_THEOREM_NOTE.md`
- `docs/FIRST_NONDISK_CHARACTER_FOAM_THEOREM_NOTE.md`
- `docs/CHARACTER_INTERTWINER_FOAM_LAW_NOTE.md`
- `docs/FINITE_BX_LOW_CARRIER_NO_GO_NOTE.md`
- `docs/POISSONIZED_OCCUPATION_INTERTWINER_COMPRESSION_NOTE.md`
- `docs/POISSONIZED_LINK_CHANNEL_COMPRESSION_NOTE.md`

## What remains valid

- the one-plaquette Toeplitz/Bessel determinant
- the derivative formula for `P_1plaq(beta)`
- the independent Weyl-angle cross-check
- the numerical fact that the rejected lifted value lands very near the
  canonical same-surface plaquette at `beta = 6`

The near-hit is retained as a bounded curiosity, not as a theorem.

## Safe branch statement

The branch now supports exactly this paper-safe claim:

> The local `SU(3)` plaquette block is exact, the proposed constant-lift
> analytic closure is not, and the correct exact finite-`beta` law on the
> retained finite periodic `3+1` evaluation surface is an absolutely convergent
> `SU(3)` character/intertwiner foam ratio. Any smaller analytic closure must
> therefore be a compression of that exact foam law, not a lifted one-plaquette
> ansatz, a boundary-shellable transfer, a factorized directed-cell closure, a
> one-shell face-state multiset closure, or any raw rooted-filling closure that
> ignores exact `4`-cube boundary quotienting.

It also now supports the sharper claim that quotienting alone is not enough to
make the rooted transfer local on surface keys: the quotient surface key is the
right counting object, but not an exact rooted Markov state.

The branch now also supports the first constructive hidden-sector claim:

> at the first nontrivial quotient layer (`n = 5`), the missing rooted state is
> not arbitrary. It collapses to a finite local cube-shell alphabet (`6`
> unordered channels / `12` ordered channels under unit `4`-cube symmetry), and
> those `12` ordered states already carry a finite exact one-step quotient
> transfer kernel.

The next propagated theorem sharpens that immediately:

> the `12`-state one-shell alphabet is not a closed final rooted Markov state,
> but its one-step image remains local and exact: every propagated duplicate
> class is again a single unit `4`-cube defect, now with `2` shared exterior
> `3`-cells instead of `1`.

The next theorem sharpens it again:

> that exact propagated two-shell sector also collapses to a finite local
> alphabet under unit `4`-cube symmetry, but not a tiny one: `226` ordered
> local two-shell states, `121` unordered pair-orbits, and `184` distinct exact
> one-step quotient transfer histograms.

The direct quotient-surface route now also has its first exact finite-`beta`
activity theorem:

> the local anchor `p = P_1plaq(6)` is the exact normalized fundamental
> character coefficient of the Wilson plaquette weight, and the isolated
> simply-sheeted disk sector through `n <= 5` has exact activity `p^A`, giving
> an exact isolated disk-sector value `0.549664307405897` and an exact isolated
> unique-surface sector value `0.552217312490512`.

It now also has the first exact non-disk lift theorem:

> the first genuine non-disk window at `p^14` already rules out a scalar
> `p`-only quotient-surface gas. Exactly `20/72` surfaces admit a pure
> fundamental `Z_3` face-orientation lift and `52/72` do not, so the direct
> exact closure object must be character-labeled or sheet-enriched.

It now also has the first exact character-foam split:

> even the minimal plaquette-character face alphabet `{3, 3bar, 8}` still
> carries only the `20` genus/crossing surfaces and misses the `52` singular
> surfaces. The exact first non-disk defect signatures are `B^0X^0`, `B^0X^4`,
> `B^1X^3`, and `B^4X^0`, so the direct exact carrier is a quotient foam with
> local baryon-junction `B` and crossing `X` defect slots.

And it now has the exact finite-`beta` law that subsumes all of those local
theorems:

> on the retained finite periodic lattice, the Wilson plaquette expectation is
> exactly a ratio of absolutely convergent `SU(3)` character/intertwiner foam
> sums. The earlier `p`, `p_8`, `B`, and `X` objects are the first explicit
> low-carrier pieces of that exact law.

And it now has the exact finite-compression no-go that sharpens the endpoint:

> the one-plaquette Wilson weight already carries infinitely many strictly
> positive symmetric-representation coefficients, so the exact law cannot
> compress to any finite face alphabet, and therefore not to any exact small
> finite `B/X` low-carrier closure either.

And it now has the exact constructive compression that survives that no-go:

> the full infinite-carrier law reorganizes exactly as a Poissonized plaquette
> occupation/intertwiner law. Each plaquette carries a countable local state
> `(m,n) in N^2`, truncating to `m+n <= K` gives the finite local alphabet
> `|Omega_K| = (K+1)(K+2)/2`, and the normalized finite-lattice law has explicit
> truncation tail `epsilon_K(P) = 1 - (1 - q_K)^P` with `q_K = P(Poisson(beta) > K)`.

And it now has the exact local-channel theorem that sharpens the evaluator:

> after plaquette truncation to `Omega_K`, each link lives on the finite
> invariant-channel alphabet
> `Lambda_K = {(r,s,alpha): r+s <= 4K, 1 <= alpha <= dim Inv(3^(⊗r) ⊗ 3bar^(⊗s))}`.
> The earlier regular, `X`, and `B` tensors are exactly the first special
> channels `dim Inv(1,1)=1`, `dim Inv(2,2)=2`, and `dim Inv(3,0)=dim Inv(0,3)=1`.

## What should not be changed from this branch alone

Do not rewire:

- canonical `<P>`
- canonical `u_0`
- canonical `alpha_s(v)`
- manuscript language that calls the plaquette low-carrier-closed or
  closed-form analytic

unless a genuine low-carrier compression theorem is added later.

Right now the remaining missing theorem is no longer “find the exact law.”
That is done.

It is also no longer “prove the law collapses to a small finite `B/X`
carrier.” That is now ruled out.

The remaining missing theorem is narrower:

> find a faster evaluator or recursion for the already exact finite-state
> Poissonized occupation/intertwiner tensor network. The hidden-shell hierarchy
> is now known to be finite for its first two layers but already large at layer
> two, the one-plaquette law itself forces infinitely many nonzero face
> characters, and the truncated local link-channel basis also grows rapidly.
