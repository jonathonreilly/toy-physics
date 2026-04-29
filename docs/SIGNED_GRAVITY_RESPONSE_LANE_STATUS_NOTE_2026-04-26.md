# Signed Gravitational Response Lane Status Note

**Date:** 2026-04-26  
**Status:** open support/no-go lane status; support/open only
**Runner:** `scripts/frontier_signed_gravity_response_lane_status.py`

This note lands the useful science from the signed-gravity review branch
without merging that stale branch wholesale. The safe public name is **signed
gravitational response**, not antigravity.

This is not a manuscript claim or theorem-grade closure.

The lane remains open. The current package does not derive a physical
repulsive gravity sector.

## 1. Current Verdict

The review branch sharpened the signed-response problem into one positive
conditional mechanism and several hard boundary results.

Positive conditional mechanism:

> If a native, conserved branch label `chi_g = +/-1` is supplied and if source
> sign and response sign are locked to that same label, then same-sector pairs
> attract and opposite-sector pairs repel while inertial mass stays positive
> and the two-body action-reaction check passes.

Non-closing verdict:

> The retained finite/local structures reviewed so far do not derive the
> active physical `chi_g` source selector. The best determinant-orientation
> route naturally hosts a `Z_2` orientation line and gives a unique local real
> source character once that APS orientation-line grammar is accepted, but it
> does not canonically select the physical source section or source action from
> the current minimal stack.

So the landed status is:

- **locked-sign consequence algebra:** coherent conditional support;
- **local/taste-cell selector:** strict selector no-go;
- **local signed source primitive:** blocked;
- **determinant-orientation line:** naturally hosted but not canonically
  selected;
- **APS/Wald/Gauss bridge and source action:** conditional, not retained;
- **physical signed gravity:** not closed.

## 2. What Is Worth Keeping

### Locked Source/Response Consequence Algebra

For a toy two-body law

```text
(-Delta + mu^2) Phi = sum_a chi_a m_a |psi_a|^2,
H_a = H_0 + chi_a Phi,
```

with positive inertial masses, the only viable sign option among the three
tested controls is the locked case:

| mode | source sign | response sign | mixed-pair balance | status |
|---|---:|---:|---:|---|
| source-only | `chi` | `+1` | fails | no-go control |
| response-only | `+1` | `chi` | fails | no-go control |
| locked | `chi` | `chi` | passes | conditional mechanism |

The locked table is:

| pair | response to source | readout |
|---|---:|---|
| `++` | positive | attraction |
| `+-` | negative | repulsion |
| `-+` | negative | repulsion |
| `--` | positive | attraction |

This is useful because it isolates the exact algebra a physical signed sector
would need to satisfy. It is not useful as a standalone claim unless the
`chi_g` source label is derived or otherwise accepted as a physical sector.

### Strict Local Selector No-Go

The reviewed finite Kogut-Susskind taste-cell scan asked for a Hermitian
involution `Q_chi` that simultaneously:

1. defines nonempty `+/-` sectors;
2. is conserved by the retained massive parity-correct staggered generators;
3. preserves the parity-correct scalar coupling operator `epsilon`;
4. pins the scalar source sign by branch.

No strict local/taste-cell selector satisfies all four requirements.

The obstruction is structural. The obvious scalar-sign pin is `epsilon`
itself, but `epsilon` anticommutes with the kinetic Clifford generators and
therefore is not a conserved branch label on the full retained surface. The
commuting taste labels that survive as conserved labels do not pin the scalar
source sign; they label neutral degeneracies.

### Local Signed Source Primitive No-Go

The retained local source candidates split cleanly:

| source form | status |
|---|---|
| Born density `|psi|^2` | native and positive, but not signed |
| scalar bilinear `epsilon |psi|^2` | signed and variational, but not branch-fixed/conserved |
| neutral selector expectation `<Q_chi>` | can be signed, but not the retained scalar source |
| inserted `chi_g |psi|^2` | works algebraically only after `chi_g` is inserted |

Therefore the local retained source surface does not provide the active signed
source primitive by itself.

### Determinant-Orientation Support

The strongest positive route is determinant-orientation grammar:

```text
chi_eta(Y) = sign(eta_delta(D_Y)).
```

Within the accepted source-character grammar, `chi_eta` is the unique local
real character compatible with:

- null quarantine;
- orientation reversal;
- unit normalization;
- refinement invariance;
- local sewing.

This is meaningful support. It shows that if the active source is a local
section of the APS determinant-orientation line, the sign character is forced.

But the grammar itself is an additional physical placement premise. The raw
native Hodge boundary complex and the retained-compatible staggered boundary
operators reviewed so far are eta-neutral; they do not contain the unpaired APS
orientation line as a derived active source mode.

### Orientation Line Hosted, Not Selected

The finite Grassmann determinant-line functor naturally hosts a real
orientation line / `Z_2` torsor with multiplicative sewing and stable
refinement pullback. That matters because the signed-response target is not
alien to the framework's determinant-line language.

It still does not choose a canonical signed section. A hosted torsor is not the
same thing as a selected physical source term.

### Tensor And Continuum Boundary

A conditional oriented tensor-source lift can be written as

```text
T_g = chi_eta T_+
```

once the orientation character is supplied. This twists an already-retained
ordinary tensor source bundle. It does not derive the tensor components from a
scalar sign alone.

Likewise, a formal graded Einstein localization can be organized on the chosen
continuum target. That is a useful consistency theorem for the conditional
target, not a global nonlinear physical-sector closure.

## 3. What Is Not Claimed

This lane does **not** claim:

- negative inertial mass;
- gravitational shielding;
- propulsion or reactionless force;
- switchable gravity;
- a physical antigravity technology;
- a retained physical repulsive-gravity sector;
- a canonical source action from the current minimal stack;
- a derived APS/Wald/Gauss bridge;
- a global nonlinear PDE existence theorem for the signed sector.

Any document or runner using stronger language should be treated as legacy
branch wording, not the current `main` posture.

## 4. Remaining Gates

The signed-response lane can move only if one of these gates closes:

1. **Canonical source selector:** derive or accept a native physical section of
   the determinant-orientation line.
2. **Boundary-mode realization:** find a retained boundary operator whose
   eta-character is nonzero without inserting an APS summand.
3. **Source-action bridge:** derive the signed source action, including the
   APS/Wald/Gauss relation, rather than assigning it.
4. **Sector preparation:** specify how compact sources enter a definite
   `chi_g` sector without making the sign a tunable external knob.
5. **Global stability:** prove the signed continuum/nonlinear target remains
   well posed and stable beyond formal/local perturbative control.

Until at least the first three gates are closed, the only retained-safe
statement is:

> The framework has a coherent conditional signed-response consequence
> harness and a sharp determinant-orientation support/no-go boundary. It does
> not yet derive physical signed gravity.

## 5. Harness Tags

The consolidated runner checks the current landed posture with these final
tags:

```text
LOCKED_SIGN_RESPONSE_CONSEQUENCE_PASS
NO_GO_STRICT_SELECTOR
SOURCE_PRIMITIVE_BLOCKED_LOCAL
ETA_SOURCE_CHARACTER_UNIQUENESS_THEOREM_A1_MAXIMAL
CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE
SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED
SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED
SIGNED_GRAVITY_REMAINING_GATES_REDUCED_TO_PRECISE_CONDITIONALS
SIGNED_GRAVITY_PHYSICAL_SECTOR_NOT_RETAINED
```
