# Route Portfolio — Cycle 22

Five orthogonal routes were considered for closing the cycle 17 residual
on Carrier Orbit Invariance.

## Route A — Direct exhaustion via representation theory

**Idea:** enumerate ALL operators on the K_R(q) carrier representation
that can distinguish E and T orbits. Show that each such operator is
either (a) the identity, (b) trivial on E ∪ T, or (c) explicitly bounded
by the existing audited_conditional results.

**Score:**
- Closure probability: 2 — exhaustion is hard if "all operators"
  includes infinite-dimensional families.
- Hard-residual pressure: 3 — direct attack.
- Content depth: 3 — full classification.
- Time cost: high — open-ended enumeration.
- Risk: medium — easy to miss exotic operators.

**Status:** partial — implicit in Route B's classification step.

## Route B — Group-theoretic argument (SELECTED)

**Idea:** the carrier K_R(q) carries an explicit Z_2 action via swap
P_ET. Any operator distinguishing E from T orbits must lie in the
antisymmetric isotypic component V^- of the operator space under swap.
The framework's retained structure does NOT include any antisymmetric
operators in the registry; therefore no retained-primitive operator
distinguishes E from T orbits.

**Score:**
- Closure probability: 2 — clean reduction to a finite registry check.
- Hard-residual pressure: 3 — addresses the structural premise head-on.
- Content depth: 3 — explicit Z_2-isotypic decomposition.
- Time cost: medium — Schur reduction + registry enumeration.
- Risk: low — Z_2 rep theory is elementary.

**Status:** SELECTED. Reduces structural exhaustion to a meta-registry
closure premise.

**Why selected over A:** Route A's general enumeration is implicit in
Route B's classification. Route B converts the open-ended exhaustion
into a finite (and currently checkable) registry enumeration plus a
single named meta-premise. This is more honest, more checkable, and
more useful for future cycles.

## Route C — Cohomological argument

**Idea:** cast E/T distinguishing as a cohomology class in
H^1(BZ_2; V^-) where V^- is the antisymmetric carrier representation.
Show that the framework's retained structure makes this class trivial.

**Score:**
- Closure probability: 1 — cohomological machinery is overkill for a
  Z_2 action; the calculation reduces to Schur.
- Hard-residual pressure: 2 — reframes but does not strengthen.
- Content depth: 3 — high-machinery.
- Time cost: high — unfamiliar machinery.
- Risk: high — risk of overstating closure via abstract nonsense.

**Status:** REJECTED — overkill; the cohomological argument reduces
to the same Z_2-isotypic decomposition that Route B uses directly.

## Route D — Sheaf-theoretic argument

**Idea:** treat E and T orbits as sheaves over the carrier base; show
that any morphism between them factors through the trivial sheaf.

**Score:**
- Closure probability: 1 — sheaf theory adds machinery without new
  content for a Z_2-orbit problem.
- Hard-residual pressure: 2 — same as Route C.
- Content depth: 2 — abstract.
- Time cost: high — unfamiliar machinery.
- Risk: high — easy to lose the physical content.

**Status:** REJECTED — overkill for the same reason as Route C. The
Z_2 quotient is finite and the Schur reduction makes sheaves
unnecessary.

## Route E — Computational exhaustion (low-degree polynomials)

**Idea:** enumerate finitely many operator classes on the carrier
(specifically, low-degree polynomial operators in the carrier
coordinates u_E, u_T, delta_A1) and verify each is bounded or
swap-symmetric. Argue that higher-degree operators can't exceed the
bounded-degree case (compactness, etc.).

**Score:**
- Closure probability: 1 — degree-1 and degree-2 classification only;
  higher-degree closure requires a separate compactness argument.
- Hard-residual pressure: 1 — partial enumeration only.
- Content depth: 2 — concrete calculation.
- Time cost: low — direct algebra.
- Risk: medium — easy to miss "exotic" operators.

**Status:** USED AS RUNNER CROSS-CHECK in Part 4. Enumerates degree-1
and degree-2 polynomial operators in carrier coordinates and verifies
each is either swap-symmetric (factors through swap quotient) or
bounded (matches existing Theta_R^(0), Xi_R^(0)).

## Stuck fan-out synthesis

Routes A, B, E are mutually consistent and convergent: they all reduce
the structural exhaustion to a Z_2-isotypic question. Route B is the
cleanest formulation; Route A is the implicit content; Route E is the
runner-level cross-check.

Routes C and D are higher-machinery reformulations that do not change
the actual content of the argument. They are rejected on the
machinery-vs-content tradeoff.

## Selected route output

Route B yields a **partial Carrier Operator Classification Theorem**:

> Let V = R^4 be the carrier representation under the Z_2 swap action.
> Then V decomposes as V = V^+ ⊕ V^- with V^+ = symmetric isotypic
> (dim 2) and V^- = antisymmetric isotypic (dim 2). Any linear operator
> L on V that distinguishes E from T orbits has nontrivial component in
> Hom(V, V^-). The current retained primitive registry contains zero
> operators with nontrivial component in Hom(V, V^-). Therefore no
> retained-primitive operator distinguishes E from T orbits on the
> current audited surface.

The closure ("no future retained primitive can have nontrivial V^-
component") is the residual meta-mathematical premise.
