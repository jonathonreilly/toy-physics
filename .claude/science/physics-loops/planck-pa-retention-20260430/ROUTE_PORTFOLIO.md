# Route Portfolio

The portfolio is restricted to the single residual theorem: force the active
rank-four `P_A` block, or force first-order boundary incidence, without adding
it as a premise.

| Route | Candidate Derived Asymmetry | Initial Risk | Test |
|---|---|---:|---|
| Oriented cubical boundary incidence | Boundary of a four-cell might prefer normal one-forms over three-form faces | High | Build exact incidence/Hodge test; check whether face orientation is just dual to normal cochain data |
| Variational first derivative | Retained link-local action source variables might select degree one | High | Check whether `A_min` itself supplies one-link source variables, instead of choosing them by hand |
| Reflection positivity / retarded response | Single-clock evolution might select outward normal response | Very high | Search accepted time theorem for causal orientation, then test if it breaks `P_1`/`P_3` Hodge equivalence |
| Intrinsic active-block module induction | Clifford module might be induced directly without choosing `P_A` | Very high | Test whether `Cl_4(C)` action on `H_cell` has a unique rank-four invariant submodule compatible with substrate actions |
| Discrete exterior derivative versus codifferential | `d` might be substrate-native while `delta` is derived | High | Check if accepted substrate contains `d` as an oriented law, or only metric/Hodge-symmetric algebra |

Stretch-cycle rule: because the two preceding audit cycles already produced
clean no-go witnesses, the first executable route in this block must be a
first-principles stretch attempt, not a small wording repair.

## Executed Outcome

The oriented boundary incidence route was executed first. It failed as a
selector:

```text
oriented face incidence = Hodge-dual normal data
P_1 <--> P_3 by Hodge star
```

Fan-out status:

| Route | Outcome |
|---|---|
| Oriented cubical boundary incidence | failed; normal/face Hodge duality |
| Variational first derivative | positive candidate; `A_min` finite Grassmann / staggered-Dirac link-local action supplies one-link source variables |
| Reflection positivity / retarded response | no accepted one-hop law found that breaks `P_1`/`P_3` |
| Intrinsic active-block module induction | blocked by active-block selection and bilinear basis-selector ambiguity |
| Discrete exterior derivative versus codifferential | Hodge-conjugate unless `d` over `delta` is independently primitive |

## New Positive Candidate

The boundary-incidence route failed, but it exposed the needed asymmetry:
boundary orientation alone is Hodge self-dual, while the microscopic action
source domain is not. The accepted `A_min` surface includes the finite
Grassmann / staggered-Dirac partition and lattice operators. Locally those
operators are nearest-neighbor one-link terms. After anomaly-forced time
completion, the source variables are:

```text
u_t, u_x, u_y, u_z.
```

The algebraic differential of the retained link-local action has support:

```text
dS_link(du_a) -> {a},       support = P_1 H_cell = P_A H_cell.
```

The Hodge-dual `P_3` sector is still present, but only as a face/flux dual or
third-composite support. It is not an automorphism of the one-link source
domain.

Artifacts:

```text
docs/PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md
scripts/frontier_planck_link_local_first_variation_p_a_forcing.py
```

Runner result: `PASS=8 / FAIL=0`.

Audit risk: the framework audit must agree that the link-source differential
is already part of `A_min`, not an added observable-response premise.
