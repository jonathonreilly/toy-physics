# ALT Connectivity Family Complex Failure Note

**Date:** 2026-04-06  
**Status:** diagnosed boundary for complex action on the alternative connectivity family

## Artifact Chain

- [`scripts/ALT_CONNECTIVITY_FAMILY_COMPLEX_SWEEP.py`](/Users/jonreilly/Projects/Physics/scripts/ALT_CONNECTIVITY_FAMILY_COMPLEX_SWEEP.py)
- [`logs/2026-04-06-alt-connectivity-family-complex-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-alt-connectivity-family-complex-sweep.txt)
- [`docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md)

## Question

Does the parity-rotated sector-transition family also carry the complex-action
crossover on the no-restore grown slice?

## Result

No. This is a clean boundary failure.

What the sweep shows:

- gamma = 0 stays on the same side as the field-free reference
- gamma = 0.1, 0.2, 0.5 remain on the same side as gamma = 0
- there is no TOWARD -> AWAY crossover
- weak-field slopes stay near linear where measured

In other words:

- the family keeps the signed-source basin
- but it does **not** carry the complex-action branch

## Safe Read

This is not a control leak:

- the previous signed-source note already established exact zero and neutral
  controls
- the complex sweep fails because the branch never flips sign, not because the
  controls break

The failure is therefore structural:

- the alternative structured connectivity family is selective
- it supports the signed-source package
- it does not support the complex-action crossover on this slice

## Conclusion

This is a useful diagnosed boundary. The new structured connectivity family is
real, but it is not a universal transfer lane for complex action.
