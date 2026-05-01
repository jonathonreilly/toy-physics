# Assumptions And Imports

| Item | Role | Current status | Loop disposition |
|---|---|---|---|
| `g_bare = 1` canonical surface | substrate input | existing minimal-axiom surface | allowed as substrate input |
| `N_c = 3`, `N_iso = 2` | structural counts | retained/structural in repo | allowed for arithmetic |
| Old Ward `H_unit` matrix-element readout | forbidden shortcut | `audited_renaming` | may be cited only as the failure mode |
| Source / HS / Legendre normalization | physical readout bridge | `audited_renaming` via SSB matching note | open import |
| Chirality projection and right-handed selector | trilinear map | `audited_failed` via Class 5 ledger row | open import |
| Physical scalar carrier uniqueness | maps source scalar to Higgs fluctuation | `audited_failed` on current ledger row | open import |
| Scalar LSZ / `Z_phi` external leg | physical vertex normalization | `audited_conditional` | open import |
| Scalar projector/source normalization | needed for ladder pole criterion and residue | not fixed by current retained surface | open import |
| Common tadpole/dressing | needed to compare gauge and scalar readouts | not clean after Ward audit | open import |
| Observed `m_t`, observed `y_t` | comparator only | external observation | forbidden as proof input |
| `alpha_LM` / plaquette normalization | prior quantitative bridge | audited non-clean in this lane | forbidden as load-bearing proof input |
| Production MC data | direct-measurement route evidence | not complete | unavailable for closure |
| Static heavy-quark additive mass | HQET direct route | not derived on current surface | open import |
| Lattice-HQET-to-SM top mass matching | HQET direct route | not derived on current surface | open import |
| Scalar-channel contact coupling `G` | HS/RPA pole condition | not in `A_min` | forbidden unless derived from Wilson gauge ladder |
| Scalar-channel Bethe-Salpeter kernel | interacting pole route | not yet retained | open import after ladder scout |
| IR / finite-volume kernel limit | needed for ladder eigenvalue crossing | not yet fixed | open import |
| Full-staggered PT formula layer | supplies `D_psi`, `D_gluon`, scalar/gauge kinematics | exact support only | formulas reusable; old alpha/plaquette/H_unit surfaces forbidden |

Minimal allowed premise set for the current stretch attempt:

```text
A_min = retained action/substrate + structural counts + standard functional
derivative definitions, but no H_unit matrix-element definition, no observed
top mass/Yukawa, no fitted selector, and no alpha_LM/plaquette bridge as proof.
```

New obstruction from the scalar ladder projector check:

```text
lambda_max[c O] / lambda_max[O] = c^2
lambda_max[F_ps] / lambda_max[F_ps/4] = 16
```

Therefore the ladder pole criterion cannot be made load-bearing until the
scalar projector/source normalization and scalar LSZ residue are derived from
the interacting Wilson-staggered scalar two-point function.

Direct-route HQET import boundary:

```text
C_static(t) / C_static(0) = exp(-E_residual t)
```

The static rephasing removes the absolute heavy rest mass from the normalized
correlator.  A heavy/top-integrated direct route still needs an additive-mass
renormalization and lattice-HQET-to-SM matching theorem before it can determine
`m_t` and `y_t`.

The formal static obstruction is:

```text
C(t; am0, E) = A exp[-(am0 + E)t]
C_sub(t; E) = exp(am0 t) C(t; am0, E) = A exp[-Et]
am0 + delta_m = constant
```

The subtracted correlator is invariant under changes in the absolute rest mass;
the residual-mass decomposition is nonunique until a matching condition fixes
the physical sum.

Legendre normalization boundary:

```text
W_k(J) = W(k J)
phi_k = dW_k/dJ = k phi
Gamma_k(phi_k) = Gamma(phi_k/k)
```

The source Legendre transform is exact, but it is covariant under source/field
rescaling.  It does not select `kappa_H = 1` without an additional physical
pole-residue or canonical kinetic normalization condition.
