# Planck-Scale Hbar Status and Remaining Objections Audit

**Date:** 2026-04-23
**Status:** hostile-review scope audit for the hbar / unit-convention bar
**Verifier:** `scripts/frontier_planck_hbar_status_and_remaining_objections_audit.py`

## Verdict

The current branch does **not** derive `hbar`.

It derives a native dimensionless primitive boundary coefficient

`c_cell = 1/4`

on the retained primitive one-step boundary/worldtube object class. With the
standard gravitational area/action normalization

`S_grav / k_B = A c_light^3 / (4 G hbar) = A / (4 l_P^2)`,

that coefficient gives

`a^2 / l_P^2 = 1`.

That is a serious conditional Planck-length result. It is not yet a structural
derivation of the quantum of action.

## Axis Placement

| Claim axis | Current status | Reason |
| --- | --- | --- |
| Structural derivation of `hbar` from graph/combinatorics | **Not achieved** | `hbar` enters through unitary action phases and the standard gravitational area/action law. |
| Numerical prediction of `hbar` in SI units | **Not a physical target** | Since the 2019 SI revision, the Planck constant `h` has an exact fixed SI value; predicting that number would predict a unit convention. |
| Dimensionless prediction involving `hbar` | **Not yet achieved** | The branch derives `a^2/l_P^2 = 1` only after importing the standard gravitational normalization containing `hbar`, `G`, and `c_light`. |
| Native dimensionless microscopic coefficient | **Achieved on the retained object class** | The packet derives `rank(P_A)/dim(H_cell) = 4/16 = 1/4`. |
| Planck length as physical lattice spacing | **Conditional closure** | Closed if the primitive boundary count is accepted as the microscopic gravitational boundary/action carrier. |

Official SI guardrail:

- BIPM lists `h = 6.626 070 15 x 10^-34 J s` as an exact defining constant of
  the SI: <https://www.bipm.org/measurement-units/si-defining-constants>.
- NIST states the same revised-SI exact value:
  <https://www.nist.gov/si-redefinition/meet-constants>.

Therefore an honest "derive hbar" claim must be a claim about a dimensionless
physical relation, not the decimal SI value of `hbar`.

## Remaining Objections

### O1. Hbar is still an input to the final unit map

The area/action normalization theorem explicitly imports:

`S_grav / k_B = A c_light^3 / (4 G hbar)`

and

`l_P^2 := hbar G / c_light^3`.

So the current packet derives the coefficient multiplying the Planck area. It
does not derive the action quantum appearing in that Planck area.

### O2. The result is a conditional dimensionless Planck statement

The nontrivial dimensionless statement is

`a^2 c_light^3 / (hbar G) = 1`.

The branch derives this only after accepting that the primitive boundary count
is the microscopic carrier of the standard gravitational boundary/action
density. A reviewer can reject that carrier identification without disputing the
internal count `1/4`.

### O3. The primitive boundary-action object class remains the top live denial

The parent-source theorem closes the Schur/event common-source bridge only
inside the retained primitive one-step boundary/worldtube object class.

The remaining physical denial is:

> the gravitational boundary-action source does not belong to that primitive
> object class.

If this denial is accepted, the packet falls back to a native counting theorem,
not a Planck-length theorem.

### O4. Source-free state semantics are authorized, not derived from the older minimal ledger

The branch now makes the one-axiom information / Hilbert / locality surface an
explicit Planck-packet input. That is cleaner than hiding it, but it means the
older minimal ledger alone still does not prove

`rho_cell = I_16 / 16`.

A hostile reviewer can reject the extension, or accept it only as a conservative
state-semantics postulate.

### O5. Parent-source equivalence can still be challenged physically

The parent-source theorem says the event source is the faithful representation
of the full axis source `P_A`, and the Schur source is quotient shape plus
retained doublet multiplicity:

`P_A = P_q + P_E`.

The mathematical bridge is now explicit. The remaining challenge is whether that
is the physical gravitational boundary source rather than a selected readout
class.

### O6. The scalar Schur/free-energy lane remains a rival object class

The branch deliberately does not claim that ordinary Schur scalar free-energy
readouts alone give the Planck coefficient. Earlier scalar lanes produce
different weights or no exact `a = l_P`.

This is not a contradiction if the object classes are separated. It is a review
risk if the paper blurs them.

### O7. The information/action route is still open, not closed

The current information/action audit rules out the obvious direct versions:

- direct count/Shannon/von Neumann information is log-base dependent;
- raw `log Z` is chart-density dependent;
- exact Planck would require a new phase-per-information theorem
  `q_* = kappa_info I_*`.

No such `kappa_info` theorem is currently derived.

### O8. The elementary action-phase route is reduced, not solved

The first-principles action-phase reduction gives

`a^2 / l_P^2 = 8 pi q_* / eps_*`.

Exact conventional `a = l_P` requires

`q_* / eps_* = 1 / (8 pi)`.

The current branch does not derive that ratio. The boundary-density route is the
current closure route instead.

### O9. No independent dimensionless phenomenological prediction is yet attached

A skeptical reviewer can ask:

> What can this predict besides identifying `a` with the conventional Planck
> length after the gravitational normalization is accepted?

At present the answer is the exact microscopic coefficient `1/4`, not a new
measured dimensionless constant such as `alpha` or a mass ratio.

### O10. Historical notes can confuse the scope

Older branch notes record failed or conditional lanes. They are useful as audit
history, but a reviewer packet must lead with the canonical submission packet
and this hbar-status audit. Otherwise a hostile reader can cite superseded
"not yet closed" language as if it were the current claim.

## What Would Count As A Structural Hbar Derivation

A real structural `hbar` theorem would need to derive an action quantum from the
discrete structure itself, for example:

1. a graph-native projective phase theorem showing why one primitive closed
   process contributes exactly one fixed action phase;
2. a combinatorial commutator/symplectic theorem deriving the unit in
   `[q,p] = i hbar`;
3. an information/action theorem deriving a base-independent
   `q_* = kappa_info I_*`;
4. a microscopic boundary-term theorem deriving the gravitational action
   normalization without importing `hbar`;
5. a dimensionless prediction such as a fixed value of `alpha` or another
   measured ratio involving the same action unit.

None of those is currently in hand.

## Safe Claim

Use:

> The branch derives a native dimensionless boundary-cell coefficient `c_cell =
> 1/4` on the retained primitive boundary-action object class. With the standard
> gravitational area/action normalization, this gives `a^2/l_P^2 = 1`. This is a
> conditional structural Planck-length result, not a derivation of `hbar`.

Do not use:

> The branch derives the Planck constant.

Do not use:

> The branch predicts the numerical SI value of `hbar`.

Do not use:

> Bare `Cl(3)` / `Z^3` alone, without the explicit state-semantics and
> gravitational carrier assumptions, forces `hbar`.
