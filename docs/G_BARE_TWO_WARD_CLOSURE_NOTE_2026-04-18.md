# Two-Representation Ward Re-Read on `g_bare`: Path 2 Support Candidate

**Date:** 2026-04-18
**Status:** conditional / support candidate — optional absolute-pair
re-read of the retained tree-level Ward-identity 1PI Green's function
on the Q_L scalar-singlet channel. Offered as a Path 2 support
candidate on the `g_bare = 1` internal-fixation program. Re-uses only
content already established in
[YT_WARD_IDENTITY_DERIVATION_THEOREM.md](YT_WARD_IDENTITY_DERIVATION_THEOREM.md).
No new axioms.
**Primary runner:** `scripts/frontier_g_bare_two_ward_closure.py`

---

## Authority notice

This note does **not** modify:

- the retained tree-level Ward-identity theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`); it inherits Rep A
  and Rep B verbatim and re-reads them without altering their inputs.
- the rigidity theorem
  (`docs/G_BARE_RIGIDITY_THEOREM_NOTE.md`); the present note offers
  a candidate companion route to the same conclusion (`g_bare = 1` is
  not a free parameter) at the 1PI-amplitude level, rather than at
  the operator-algebra level.
- the older bounded normalization note
  (`docs/G_BARE_DERIVATION_NOTE.md`).

What this note adds: a candidate pinning of `g_bare` as a numerical
quantity from a system of two equations already present inside the
retained tree-level Ward theorem, under the support reading that the
theorem's two-representation consistency check may be treated as an
equation to solve rather than only as a verification at the canonical
surface.

---

## Support claim

**Support claim (Two-Representation Ward Re-Read).** On the retained
Cl(3) × Z³ Wilson-staggered canonical surface with the Q_L = (2,3)
block, the tree-level 1PI Green's function
`Γ⁽⁴⁾(q²) := P_{S,(1,1)} · ⟨ψ̄ψ(q) ψ̄ψ(-q)⟩_{1PI,amp}`
on the scalar-singlet channel admits two algebraically distinct
evaluations within the same retained theory:

- **Rep A** (gauge Feynman rules): scales as `g_bare²`.
- **Rep B** (H_unit operator content + canonical fermion
  normalization): is a pure algebraic/kinematic quantity
  independent of `g_bare`.

Under the support reading that these may be treated as two equations,
the joint consistency

```
Rep A = Rep B
```

on the same Green's function supports

```
y_t_bare = 1/√6                       (T2a, from Rep B alone)
g_bare²   = 2 N_c · y_t_bare² / c_S = 1 (T2b, from Rep A = Rep B)
```

so that the retained Ward theorem can be re-read as supporting the
absolute pair `(y_t_bare, g_bare) = (1/√6, 1)`, not merely the ratio.

---

## Equations and inputs

The derivation re-uses the exact content of
[YT_WARD_IDENTITY_DERIVATION_THEOREM.md](YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
Step 3. The two representations are:

### Rep A (OGE gauge Feynman rules)

From the retained bare action (D16, Wilson plaquette + staggered
Dirac, no fundamental scalar, no contact 4-fermion), the unique
tree-order diagram contributing to `Γ⁽⁴⁾` is single gluon exchange.
Applying the SU(N_c) color Fierz (D12) and the Lorentz-scalar Fierz
(S2):

```
Γ⁽⁴⁾(q²)|_A = − c_S · g_bare² / (2 N_c · q²) · O_S     (A1)
```

with `N_c = 3`, `|c_S| = 1` (Itzykson-Zuber), and `g_bare` the
Wilson-plaquette bare coupling. **This expression is stated for
arbitrary `g_bare`; no canonical-surface choice is needed to write
it down.**

Ref: YT_WARD_IDENTITY_DERIVATION_THEOREM.md:213–235, Block 4 + Block
8 of the companion runner.

### Rep B (H_unit operator matrix element)

From D9 (composite-Higgs structural axiom, the framework has no
independent Yukawa parameter) and D17 (scalar-uniqueness of `H_unit`
on the Q_L block with `Z² = N_c · N_iso = 6`, numerically verified
against the (1,8), (3,1), (8,3) alternatives), the unit-normalized
scalar-singlet composite operator is

```
H_unit(x) = (1/√(N_c · N_iso)) · Σ_{α,a} ψ̄_{α,a}(x) ψ_{α,a}(x)
          = (1/√6) · (ψ̄ψ)_{(1,1)}(x)                     (B1)
```

The bare Yukawa coupling is defined as the matrix element

```
y_t_bare := ⟨0 | H_unit(0) | t̄_{top,up} t_{top,up} ⟩    (B2)
```

and computed directly from (B1):

```
y_t_bare = (1/√6) · ⟨0 | ψ̄_{top,up} ψ_{top,up}(0) | t̄ t ⟩
         = (1/√6) · 1 = 1/√6                             (B3)
```

where the second factor is the unit-amplitude Wick contraction in
canonical fermion normalization — a kinematic identity, fixed by
canonical anticommutation relations on the free Grassmann fields,
independent of any gauge dynamics. **This evaluation does not use
g_bare anywhere; the Clebsch-Gordan weight 1/√(N_c · N_iso), the
canonical fermion-state norm, and the canonical scalar-composite
norm Z² = N_c · N_iso are all properties of the operator content of
the composite field, not of the gauge coupling.**

The tree-level H_unit-mediated contribution to the same 1PI Green's
function is then

```
Γ⁽⁴⁾(q²)|_B = − y_t_bare² / q² · O_S = − (1/6 q²) · O_S  (B4)
```

for `q² ≫ m_{H_unit}²` (physical IR-scale separation; the EW scale
is 17 orders of magnitude below M_Pl, so this is a physical fact
about the spectrum, not a convention).

Ref: YT_WARD_IDENTITY_DERIVATION_THEOREM.md:241–302, Block 2 + Block
5 + Block 6 of the companion runner.

### g_bare-independence audit of Rep B

Rep B uses exactly three ingredients:

1. The operator content of `H_unit` (line B1). This is fixed by D17
   + Steps 1-2 of the Ward theorem: `Z² = N_c · N_iso = 6` is the
   unique unit-residue normalization of the free 2-point function
   `<φφ>_free = −(N_c·N_iso / Z²) · G_0²`. The free propagator `G_0`
   does not depend on `g_bare`. `Z² = 6` is a statement about the
   free-theory kinetic term, not about gauge dynamics.
2. The canonical fermion-state normalization `⟨0|ψ̄ψ|tt̄⟩ = 1`. This
   comes from canonical anticommutation on free fermion fields
   `{ψ, ψ†} = δ`. No gauge coupling enters.
3. The Clebsch-Gordan weight `1/√(N_c · N_iso)` on the Q_L = (2,3)
   singlet. This is a purely group-theoretic overlap of the
   unit-normalized singlet with a basis component (Block 6 of the
   Ward runner: six basis overlaps, each exactly `1/√6`).

None of these three ingredients depends on the value of `g_bare`.
Therefore `y_t_bare = 1/√6` is an exact statement of the retained
framework at all `g_bare`, not only at `g_bare = 1`.

### Joint consistency

The same 1PI Green's function `Γ⁽⁴⁾(q²)` admits the two evaluations
(A1) and (B4). In a consistent quantum theory, these must agree on
their overlap of validity (tree level, momentum far above the IR
composite mass):

```
− c_S · g_bare² / (2 N_c · q²) · O_S = − (1/6 q²) · O_S  (C1)
```

Projecting onto the single channel `O_S` and canceling `q²`:

```
c_S · g_bare² / (2 N_c) = 1/6
g_bare² = 2 N_c · (1/6) / c_S = 6 · (1/6) / 1 = 1        (C2)
```

with `|c_S| = 1` from S2 (Lorentz-Clifford identity, Block 8).

**Under this re-read, the two-representation consistency supports
`g_bare² = 1` as an absolute number, given only:**

- the retained bare action (Wilson plaquette + staggered Dirac, no
  scalars, no contact 4-fermion);
- D9, D12, D16, D17 (retained structural);
- S2 (standard Lorentz Clifford identity);
- canonical fermion-state normalization (canonical anticommutation,
  not a gauge choice);
- physical IR-scale separation (physical fact, not a convention).

No axiom `g_bare = 1` is invoked inside either Rep A (which is
written for arbitrary g_bare) or Rep B (which does not reference
g_bare at all).

---

## Relationship to the rigidity theorem

The rigidity theorem
([G_BARE_RIGIDITY_THEOREM_NOTE.md](G_BARE_RIGIDITY_THEOREM_NOTE.md))
argues at the **operator-algebra level** that, once the `su(3)`
gauge algebra is realized as a concrete compact subalgebra of
`End(V)` with the fixed Hilbert-Schmidt trace form on `V`, there is
no independent scalar dilation freedom left in the canonical
generator basis. In the canonical basis, the standard notation
corresponds to `g_bare = 1`.

The present note gives a **candidate companion route** at the
1PI-amplitude level. Under the support reading above, the
two-representation consistency of `Γ⁽⁴⁾` supports `g_bare² = 1` from
the OGE-vs-H_unit matching on the Q_L scalar-singlet channel, without
reference to the operator-algebra trace form.

The rigidity theorem and the two-Ward re-read are therefore
potentially mutually supporting rather than competing. They address
the old "you can always rescale `A → A/g`" objection from different
angles, but only the rigidity route is part of the accepted-input
stack today:

- Rigidity: the canonical generator basis has no scalar dilation
  freedom.
- Two-Ward re-read: even if one tries to treat `g_bare` as free,
  the two representations of the retained 1PI Green's function can
  be read as supporting `g_bare = 1`, subject to the interpretive
  caveat below.

---

## Relationship to Path 2 of the `g_bare` program

Path 2 asks: does a SECOND independent bare-scale identity, on the
framework's current retained surface, together with
`y_t(M_Pl)/g_s(M_Pl) = 1/√6`, pin both `y_t_bare` and `g_bare`
absolutely?

The present note offers a support-level YES, under the reading that
Rep A and Rep B of the retained Ward theorem are two **independent**
evaluations of the same 1PI Green's function. The pair (A1) and (B3)
are:

- Equation 1 (from Rep B alone): `y_t_bare = 1/√6`.
- Equation 2 (from Rep A = Rep B): `g_bare² = 1`.

Treating the theorem's "verify (3.10) = (3.11) at g_bare = 1" step
as an **equation to solve** rather than a consistency check at a
fixed point gives the candidate absolute pinning.

This is a Path 2 support candidate **modulo the interpretive move** that
treats the consistency of the two representations as an equation
on `g_bare`. The bare theorem as written in
YT_WARD_IDENTITY_DERIVATION_THEOREM.md evaluates the consistency
at the pre-chosen canonical surface `g_bare = 1`; the present note
reads the same two representations as a system.

### Honest caveat

The two representations of `Γ⁽⁴⁾` are not physically independent in
the same sense as, say, two different observables. They are two
algebraically equivalent representations of the same quantity in
the same retained theory. A rigorous Path 2 closure would therefore
have to rest on the claim that Rep B's evaluation `y_t_bare = 1/√6` is a
statement that the framework can make without pre-selecting
`g_bare = 1`. The audit above supports that claim, but a reviewer
could object that the canonical scalar-composite norm `Z² = 6` is
part of a package of canonical choices that includes `g_bare = 1`
(MINIMAL_AXIOMS:18-20 bundles "g_bare = 1" with "the accepted
plaquette/u_0 surface").

Under the strongest reading that the MINIMAL_AXIOMS package treats
`g_bare = 1` and `Z² = 6` as jointly stipulated canonical choices
rather than as independently derivable facts, the two-Ward candidate
reduces to the rigidity statement: `g_bare` is not free, by
canonical convention. Under the weaker reading (each of the three
Rep B ingredients is derivable independently of `g_bare`), the
pinning is genuine.

The framework's current practice leans toward the weaker reading:
`Z² = 6` is derived by Step 1 of the Ward theorem from the
free-theory 2-point function, which is computable in any gauge
theory on the same Q_L block independent of `g_bare`; and the
canonical fermion-state norm is a property of free Grassmann
quantization. The CG weight `1/√(N_c · N_iso)` is a pure
group-theory overlap. None of these three facts demonstrably
depends on `g_bare = 1` in the retained derivation chain.

---

## Runner expectations

The companion runner
`scripts/frontier_g_bare_two_ward_closure.py`
verifies:

1. Re-derivation of `y_t_bare² = g_bare²/(2 N_c)` at tree level
   (symbolic in `g_bare`).
2. Rep B evaluation `y_t_bare = 1/√6` from:
   - `Z² = N_c · N_iso = 6` from free-propagator 2-point function
     (sum over N_c·N_iso contractions, no gauge coupling).
   - Unit Wick contraction `⟨0|ψ̄ψ|tt̄⟩ = 1` (canonical fermion
     normalization).
   - CG weight `1/√(N_c · N_iso)` from unit-normalized singlet.
3. `|c_S| = 1` from explicit Dirac-gamma Clifford expansion
   (inherited from Block 8 of the Ward runner).
4. The two-representation consistency
   `c_S · g_bare² / (2 N_c) = y_t_bare²` solved for g_bare².
5. Unique real positive solution `g_bare = 1`.
6. Absolute pair `(y_t_bare, g_bare) = (1/√6, 1)` verified to
   machine precision.
7. Sensitivity: if Rep B gave a different numerical value `y_*²`,
   the same consistency would yield `g_bare² = 2 N_c y_*² / c_S`.
   The pinning is algebraic, not circular.
8. Cross-check: the inherited ratio identity
   `y_t_bare / g_bare = 1/√6` is recovered from the absolute pair.

All checks are structural/algebraic; no Monte Carlo or running
required.

---

## Import status table

| Element | Value | Status | Source |
|--|--|--|--|
| Rep A: `Γ_A = −c_S g_bare²/(2 N_c q²) · O_S` | symbolic | RETAINED | YT_WARD_IDENTITY_DERIVATION_THEOREM:213-235 |
| Rep B: `Γ_B = −y_t_bare²/q² · O_S` | symbolic | RETAINED | YT_WARD_IDENTITY_DERIVATION_THEOREM:294-302 |
| `y_t_bare = 1/√6` (from Rep B alone) | 0.40825 | DERIVED support | Rep B evaluation; no g_bare input |
| `g_bare² = 1` (from Rep A = Rep B) | 1.0 | conditional / support candidate | Two-representation consistency re-read |
| `|c_S| = 1` | 1.0 | RETAINED | S2 Clifford; Block 8 of Ward runner |
| `N_c = N_iso · 3/2` (Q_L dim = 6) | 6 | RETAINED | NATIVE_GAUGE_CLOSURE + CKM_ATLAS |

No IMPORTED rows. No BOUNDED rows. The proposed pinning is a
conditional / support re-read of retained Ward-theorem content and is
not part of the accepted input stack.

---

## Honest boundary

This note does **not** claim:

- A new axiom or a new framework primitive.
- A different derivation of `y_t_bare = 1/√6` from the retained
  Ward theorem (that evaluation is unchanged).
- Any modification to the perturbative-matching residual budget
  (`~1.95%` from the UV-to-IR transport obstruction theorem) which
  is orthogonal to the tree-level pinning.
- Any modification to the publication matrix or the retained IR
  observable central values.

This note does claim:

- That the retained Ward theorem already contains, without
  extension, TWO independent algebraic statements: Rep B gives
  `y_t_bare = 1/√6` without invoking `g_bare`; under the support
  re-read, Rep A = Rep B then supports `g_bare² = 1`.
- That reading these as a system supports a candidate absolute pair
  `(y_t_bare, g_bare)`, not merely the ratio `y_t/g_s`.
- That this constitutes a Path 2-compatible support candidate for the
  `g_bare = 1` internal-fixation program, modulo the interpretive
  caveat recorded above (`Z² = 6` vs `g_bare = 1` as independent
  retained facts).

---

## References

- [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
  — retained tree-level Ward identity, source of Rep A and Rep B.
- [G_BARE_RIGIDITY_THEOREM_NOTE.md](G_BARE_RIGIDITY_THEOREM_NOTE.md)
  — operator-algebra route to the same conclusion `g_bare = 1`.
- [G_BARE_DERIVATION_NOTE.md](G_BARE_DERIVATION_NOTE.md)
  — older bounded normalization route, superseded for this purpose.
- [MINIMAL_AXIOMS_2026-04-11.md](MINIMAL_AXIOMS_2026-04-11.md)
  — current minimal-input stack.
- [YUKAWA_COLOR_PROJECTION_THEOREM.md](YUKAWA_COLOR_PROJECTION_THEOREM.md)
  — composite-Higgs D9 + free 2-point structure for Z² = 6.
