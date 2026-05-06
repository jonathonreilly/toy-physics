# Assumptions And Imports

## Minimal Premises Used

- KS cell/taste factorization on the note's stated finite geometry surface.
- Each encoding is an ordered two-dimensional site-basis support with isometry `V_E : C^2 -> H_E`.
- Canonical logical `Z_E` and axis-adapted `X_E` restrict to standard Pauli `Z` and `X` in the ordered logical basis, as checked by the runner.
- A/R and R/B site maps are the partial isometries `V_R V_A^dag` and `V_B V_R^dag`.
- The Bell resource is the ideal identity logical map `sum_j V_R|j> tensor V_B|j> / sqrt(2)`.
- Alice's Bell projectors and Bob's corrections use the same `(z,x)` convention as the runner.

## Explicit Non-Imports

- No apparatus dynamics.
- No physical Bell-resource preparation channel.
- No durable classical record derivation.
- No Hamiltonian transport theorem.
- No noise or fault-tolerance model.
- No matter, object, mass, charge, energy, or faster-than-light transport claim.

## Import Audit

The derivation imports only standard finite-dimensional Pauli/Bell algebra and the runner-defined encoding isometries. The capped numerical survey is retained as telemetry for enumerator and control behavior, not as the proof of the axis-adapted logical protocol.
