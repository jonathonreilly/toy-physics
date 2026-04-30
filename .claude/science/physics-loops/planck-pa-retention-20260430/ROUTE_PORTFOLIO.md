# Route Portfolio

The portfolio is restricted to the single residual theorem: force the active
rank-four `P_A` block, or force first-order boundary incidence, without adding
it as a premise.

| Route | Candidate Derived Asymmetry | Initial Risk | Test |
|---|---|---:|---|
| Oriented cubical boundary incidence | Boundary of a four-cell might prefer normal one-forms over three-form faces | High | Build exact incidence/Hodge test; check whether face orientation is just dual to normal cochain data |
| Variational first derivative | Local action variation with respect to coframe variables might select degree one | High | Check whether choosing variables `u_a` rather than Hodge-dual complements is an extra coordinate choice |
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
| Variational first derivative | failed; choosing `u_a` cochain variables is the first-order premise |
| Reflection positivity / retarded response | no accepted one-hop law found that breaks `P_1`/`P_3` |
| Intrinsic active-block module induction | blocked by active-block selection and bilinear basis-selector ambiguity |
| Discrete exterior derivative versus codifferential | Hodge-conjugate unless `d` over `delta` is independently primitive |

No route supplies a substrate-only asymmetric selector.
