# Signed Gravity Retained Boundary Source-Principle No-Go

**Date:** 2026-04-25
**Status:** proposed_retained no-go for the APS/Wald/Gauss source-principle
test of the proposed signed source cross term
**Script:** [`../scripts/signed_gravity_retained_boundary_source_principle_nogo.py`](../scripts/signed_gravity_retained_boundary_source_principle_nogo.py)

This note goes after the last high-value target left by
[`SIGNED_GRAVITY_APS_ACTION_ORIGIN_SUPERSELECTION_STABILITY_NOTE.md`](SIGNED_GRAVITY_APS_ACTION_ORIGIN_SUPERSELECTION_STABILITY_NOTE.md):

> Can a retained boundary source principle derive the `chi_eta rho Phi` cross
> term and protect the APS gap?

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim. It is a
source-principle audit.

## Target

The conditional APS-locked action proposed in
[`SIGNED_GRAVITY_APS_LOCKED_SOURCE_ACTION_PROPOSAL_NOTE.md`](SIGNED_GRAVITY_APS_LOCKED_SOURCE_ACTION_PROPOSAL_NOTE.md)
uses:

```text
S_int = - chi_eta(Y) M_phys <rho, Phi>,
rho = |psi|^2,
chi_eta(Y) = sign eta_delta(D_Y).
```

The retained boundary stack currently contains:

- positive Born/Gauss source scale;
- APS eta as a boundary spectral label;
- positive Wald/area carrier;
- source-unit normalization after an active charge is supplied.

The question is whether those retained pieces force the orientation-odd source
current:

```text
J_+ = +M_phys rho,
J_- = -M_phys rho.
```

## Source-Current Basis

The finite audit represents weak-field source derivatives over the two eta
sectors as two-component vectors:

| term | retained | source vector `(chi=+, chi=-)` | status |
|---|---|---:|---|
| positive Born/Gauss source | yes | `[+1,+1]` | positive unsigned source |
| APS eta spectator | yes | `[0,0]` | topological label, source-neutral |
| positive Wald area | yes | `[0,0]` | source-neutral |
| finite gap penalty | no | `[0,0]` | can discourage crossing but not superselect |
| hard gap constraint | no | `[0,0]` | new admissibility constraint |
| `chi_eta rho Phi` cross term | no | `[+1,-1]` | exact proposed signed source |

The desired source is:

```text
[+1,-1].
```

Command:

```bash
python3 scripts/signed_gravity_retained_boundary_source_principle_nogo.py
```

Output:

```text
[PASS] retained APS/Wald/Gauss source basis cannot span signed source
       residual=1.414e+00, fitted=[-0. -0.]
[PASS] gap penalties/constraints alone do not create a Phi source
       residual=1.414e+00, fitted=[-0. -0.]
[PASS] signed source appears exactly when the cross term is added
       residual=1.110e-16, fitted=[ 1. -1.]
[PASS] retained positive source is orientation-even while desired source is orientation-odd
```

So the current retained source basis cannot derive the signed current. The
missing term is exactly the new orientation-odd cross term:

```text
chi_eta rho Phi.
```

## Gap Protection

The APS eta sign is stable only while the boundary spectrum remains gapped.
The finite audit checks a continuous path between the two eta sectors:

```text
[PASS] continuous path between eta sectors crosses zero
       chi_path=[1, 1, 1, 1, 0, -1, -1, -1, -1]
```

A finite gap penalty is not enough to make this a topological superselection
rule:

```text
[PASS] finite gap penalty is not a topological superselection rule
       V_gap min=6.25e+00, midpoint=1.00e+06, max=1.00e+06
```

It may make crossing costly in a model, but finite cost is not sector
superselection. A hard gap rule works only by adding a new admissibility
constraint:

```text
[PASS] hard gap protection works only as an added admissibility constraint
       allowed_path=[True, True, True, True, False, True, True, True, True]
```

Thus APS gap protection is not derived by eta itself. It requires either a new
hard boundary-sector axiom or a dynamical theorem excluding zero crossings.

## Verdict

The retained source-principle audit returns:

```text
FINAL_TAG: RETAINED_BOUNDARY_SOURCE_PRINCIPLE_NO_GO
```

Interpretation:

1. The retained positive Born/Gauss source and positive Wald carrier are
   orientation-even.
2. APS eta is a clean boundary label, but source-neutral on a gapped sector.
3. Gap penalties or hard constraints can address sector crossing only by adding
   new structure; they do not create the signed `Phi` source.
4. The proposed APS-locked action works only because it adds the exact missing
   `chi_eta rho Phi` cross term.

This closes the current retained-boundary route. To continue the signed
response lane as more than a control packet, a new axiom or theorem would have
to derive both:

```text
S_int = - chi_eta M_phys <rho, Phi>
gap_0(D_Y(t)) >= g > 0 on admissible boundary dynamics.
```

Without that new principle, the lane remains a documented consequence/control
and no-go-boundary packet.

## Axiomatic Continuation

The new-principle route is now made explicit in
`SIGNED_GRAVITY_APS_LOCKED_AXIOM_EXTENSION_NOTE.md`
(downstream consumer in same lane; cross-reference only — not a one-hop dep of this note)
with runner
[`../scripts/signed_gravity_aps_locked_axiom_extension_audit.py`](../scripts/signed_gravity_aps_locked_axiom_extension_audit.py).

That continuation does not soften this no-go. It accepts the missing
`chi_eta rho Phi` cross term as a new eta-polarized source-line axiom and
accepts hard gapped-sector admissibility as new structure:

```text
FINAL_TAG: APS_LOCKED_AXIOM_EXTENSION_CONTROLLED_CANDIDATE
```

The retained status remains no-go; the extension status is axiomatic and
controlled.

The later source-line origin pass in
`SIGNED_GRAVITY_SOURCE_LINE_ORIGIN_TENSOR_LIFT_NOTE.md` (downstream
follow-up artifact; cross-reference only — that note cites the
axiom-extension note as its predecessor, not this no-go)
does not change this retained no-go. It adds a new determinant-orientation
source-line principle and then proves that `chi_eta` is forced inside that
principle:

```text
FINAL_TAG: ETA_SOURCE_LINE_ORIGIN_CONDITIONAL_A1_TENSOR_LIFT
```

So the retained APS/Wald/Gauss route is still blocked; the source-line route
is a conditional extension target.

The strongest follow-up is the source-character uniqueness theorem:

```text
FINAL_TAG: ETA_SOURCE_CHARACTER_UNIQUENESS_THEOREM_A1_MAXIMAL
```

It proves uniqueness only after admitting the determinant-orientation
source-character grammar, so it does not reopen the retained APS/Wald/Gauss
route.

The finite original-stack derivation now improves the source-character side:

```text
FINAL_TAG: CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE
```

This derives the determinant-orientation source-character grammar from the
accepted finite `Cl(3)`/`Z^3` Grassmann/staggered-Dirac determinant-line
surface. It still does not derive the term from the old separable
APS/Wald/Gauss source basis, so this retained no-go remains intact.

The native boundary-complex containment audit now sharpens the actual APS
realization side:

```text
FINAL_TAG: SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED
```

The raw retained cochain/Hodge boundary complex has parity-paired spectrum and
`eta=0`; the orientation-line APS mode used by the signed source-character
harness is therefore an added extension unless a later retained boundary
theorem derives that line from the actual graph/refinement complex.

The staggered-Dirac boundary realization audit now returns:

```text
FINAL_TAG: SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_NOT_CONTAINED
```

Retained-compatible staggered boundary operators do not repair this no-go:
they are gapped but eta-neutral. Odd open-face eta and Pfaffian signs are
quarantined as imbalance/metadata controls, not source-locking selectors.

The naturally-hosted orientation-line audit then gives the precise middle
status:

```text
FINAL_TAG: SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED
```

The determinant-line functor naturally hosts an orientation line as a `Z2`
torsor/flat local system, so the source-character grammar is not arbitrary
decoration. But the torsor does not choose a canonical section and does not
force the `chi_eta rho Phi` term. This preserves the retained
APS/Wald/Gauss no-go: the missing ingredient is a section/source theorem, not
the mere existence of an orientation-line host.
