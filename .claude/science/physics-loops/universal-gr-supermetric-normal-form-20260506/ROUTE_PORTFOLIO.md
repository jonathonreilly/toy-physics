# Route Portfolio

## Route A: Direct Log-Det Hessian

Differentiate `log det(D+s h+t k)` directly:

`partial_s log det A = Tr(A^-1 h)`,

then

`partial_t partial_s log det A|0 = -Tr(D^-1 k D^-1 h)`.

Status: passed. This is the selected closure route.

## Route B: Pure Block-Localization Import

Import the isotropic Schur-localization note and restate the coefficients.

Status: rejected as insufficient. It repeats the audited problem unless the
Hessian identity is derived independently.

## Route C: New Curvature/Einstein Identification

Try to identify the local Hessian with the full Einstein/Regge dynamics.

Status: out of scope. This is the known remaining GR gap and is not needed for
the local normal-form closure.
