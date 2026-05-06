# Assumptions And Imports

## Closed finite-dimensional premises

The theorem uses only these stated mathematical premises:

| premise | role |
|---|---|
| finite-dimensional split `E_- = E_e (+) E_r` | block-domain setup |
| `D_- = [[A, B], [C, F]]` | arbitrary supplied block operator |
| `F` invertible | Schur complement and elimination |
| `L_e = A - B F^(-1) C` invertible | boundary resolvent compression |
| `D_- = D_-^* > 0` | variational principle, positivity, monotonicity only |

## Non-inputs

- No evaluated Wilson-native `D_-` is used.
- No charged support split is derived.
- No observed DM target value or fitted selector is used.
- No literature value, normalization convention, or external comparator is
  load-bearing.

## Open imports

None for the finite-dimensional theorem.

The DM lane still has open downstream work: derive or evaluate the intended
Wilson-native charged block, prove the intended support split from the parent
stack, and close the right-sensitive selector law.
