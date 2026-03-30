# Sanity Check: Sorkin Test

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| Model Consistency | CLEAN | Standard path-sum with different barrier configurations. |
| Scale Reasonableness | FLAG | I₃/P ratios up to 10⁹ are suspiciously large. In continuum QM, I₃ should be exactly 0. Values this large suggest the measurement is dominated by DAG reconfiguration, not interference. |
| Symmetry Compliance | CLEAN | Symmetric slit configs produce symmetric I₃ profiles. |
| Limit Behavior | CLEAN | Close slits (-2,0,+2) have smallest I₃ ratio (91×), wide slits have largest (10⁹×). Consistent with wider slits causing more DAG reconfiguration. |
| Numerical Artifacts | FLAG | Unnormalized probabilities reach 10³¹. At this scale, floating-point cancellation in the I₃ formula (sum of 7 terms with alternating signs) could amplify small errors. Need to verify with higher-precision arithmetic. |
| Bug Likelihood | CLEAN | Each slit_distribution() call is the same function with different open_slits. Logic verified against existing two_slit_distribution(). |

## Skeptical Reviewer's Best Objection
"Your I₃ measures DAG reconfiguration, not higher-order interference. Changing which barrier nodes are blocked changes the entire causal structure. You haven't isolated the interference contribution from the topology-change contribution."

## Response
Correct. The experiment conflates two effects. A refined version should keep the DAG fixed and vary only the amplitude transmission at each slit. This is identified as the key follow-up.

## Verdict
**SUSPICIOUS** — I₃ ≠ 0 is real but the interpretation (higher-order interference vs DAG reconfiguration) is unresolved. Two numerical FLAGs (scale, precision) need follow-up.
