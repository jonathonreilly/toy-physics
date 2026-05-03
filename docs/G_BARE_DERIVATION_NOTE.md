# Derivation of g_bare = 1 from Canonical Cl(3) Normalization

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Lane:** DM relic mapping (Objection 1 from CODEX_DM_RESPONSE.md)
**Claim type:** positive_theorem
**Script:** `scripts/frontier_g_bare_derivation.py`

> **Parent dependency-chain gate:**
> This note now declares the repaired parent dependency chain. It must not be
> cited as retained or as closing the old `g_bare = 1` repair target until
> independent audit retains both
> [`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md)
> and
> [`G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`](G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md),
> with retained-grade dependency closure, and this parent row is re-audited on
> the changed source and dependency surface.

---

## Status

**open main gate — parent re-audit required.** `g_bare = 1` is the intended
parent theorem only relative to the canonical Cl(3) connection normalization
and only after the two 2026-05-03 repair candidates above are independently
retained. This edit is a dependency-chain correction, not a retained-status
promotion. The claim is not a dynamical calculation, not a fit, and not a
fixed-point condition. The canonical normalization itself remains the admitted
upstream convention layer; this note does not derive that convention from
`A1 + A2` alone.

This note is the **older bounded normalization route**. For the sharper
operator-algebra response to the old rescaling objection, see
[G_BARE_RIGIDITY_THEOREM_NOTE.md](/Users/jonBridger/Toy%20Physics-dm/docs/G_BARE_RIGIDITY_THEOREM_NOTE.md:1).
That newer note does not claim a dynamical fixed-point selection of `g = 1`;
it argues instead that, once the concrete `su(3)` operator algebra is fixed,
there is no independent bare coupling parameter left.

The parent claim, once the audit gate above is satisfied, is:

> On the accepted Wilson surface with canonical Cl(3) connection
> normalization `Tr(T_a T_b) = delta_ab / 2`, the bare gauge coupling has no
> independent rescaling freedom, and the unique compatible normalization is
> `g_bare = 1`, hence `beta = 2 N_c = 6` for `N_c = 3`.

---

## Theorem / Claim

**Claim (Cl(3) coupling normalization):**

Given:

1. The Cl(3) algebra generators satisfy {G_mu, G_nu} = 2 delta_{mu,nu}
2. The canonical Cl(3) connection normalization
   `Tr(T_a T_b) = delta_ab / 2`
3. The accepted Wilson plaquette small-a matching
   `beta = 2 N_c / g_bare^2`
4. Retention of the two 2026-05-03 repair candidates linked above

Then the bare gauge coupling g_bare = 1.

**Proof sketch:**

- The canonical Cl(3) generator normalization fixes the operator basis used
  for the Wilson connection.
- The rescaling-freedom candidate proves that a nontrivial
  `T_a -> c T_a` / `A -> c A` rescaling shifts the matched Wilson coefficient
  `beta` by `c^2` rather than producing a second independent `g_bare`
  convention layer.
- The constraint-vs-convention candidate locates the honest convention layer
  at the canonical normalization itself. Relative to that admitted
  normalization, `g_bare = 1` follows from `beta = 2 N_c / g_bare^2` with
  `N_c = 3` and `beta = 6`.

**Consequence:** beta = 2*N_c/g^2 = 6 for SU(3) at the Planck scale.

---

## Inputs

1. **Cl(3) algebra:** `{G_mu, G_nu} = 2 delta_{mu,nu}`.
2. **Canonical connection normalization:**
   `Tr(T_a T_b) = delta_ab / 2`.
3. **Wilson matching surface:** `beta = 2 N_c / g_bare^2`.
4. **Audit-gated repair inputs:** the two 2026-05-03 repair candidates linked
   above must be retained before this parent row can close.

The first input is the local algebraic starting point. The second is the
admitted canonical normalization surface. The third is the Wilson matching
surface. The fourth is the explicit audit gate; it is not a new axiom.

---

## What Is Actually Proved

**Exact results after the audit gate is satisfied:**

- `g_bare = 1` by canonical Cl(3) connection normalization plus Wilson
  matching
- `beta = 2*N_c = 6` for SU(3) on the accepted Wilson surface
- The old `A -> A/g` rescaling objection is routed into `beta`, not an
  independent `g_bare` convention layer
- The convention layer is explicitly at canonical normalization, not at a
  separate `g_bare` choice

**Bounded results (supporting but not standalone derivations):**

- The mean-field self-consistency ratio alpha_V/alpha_bare = 1.35 at g=1
  (moderate, not uniquely selecting)
- The mean-field iteration does NOT converge to g = 1 (it diverges)
- Maximum entropy does NOT select g = 1 (it selects g -> infinity)
- The SU(3) lattice beta function has NO nontrivial fixed point

**Numerical consequence:**

- At g = 1: alpha_plaq = 0.0923, and R(DM) = 5.48 (0.25% from observed 5.47)
- Sensitivity: g in [0.95, 1.05] gives R in [5.22, 5.78]

---

## What Remains Open

1. **Audit gate for this parent re-audit.**
   This parent update must wait for independent clean audit of the two
   2026-05-03 repair candidates and retained-grade dependency closure.

2. **Absolute derivation of canonical normalization remains open.**
   The canonical normalization is the admitted upstream convention layer.
   This note does not prove that the normalization itself follows from
   `A1 + A2` alone.

3. **The other two DM imports still stand:**
   - sigma_v = pi * alpha_s^2 / m^2 (perturbative QFT cross-section)
   - V(r) = -C_F * alpha_s / r (one-gluon exchange potential)

4. **Approaches that do NOT work:**
   - Strong-coupling fixed point: SU(3) has no nontrivial fixed point
   - Maximum entropy: selects g -> infinity, not g = 1
   - Mean-field iteration: diverges, does not converge to g = 1
   - Plaquette self-consistency: not uniquely selecting

---

## How This Changes The Paper

**Before:** g_bare = 1 was ASSUMED (Objection 1 in CODEX_DM_RESPONSE.md).
The DM provenance was: 7 NATIVE, 5 DERIVED, 1 ASSUMED, 2 IMPORTED.

**After the audit gate is satisfied:** `g_bare = 1` is a retained structural
constraint relative to the canonical Cl(3) normalization. The DM provenance is
7 NATIVE, 6 DERIVED, 2 IMPORTED.

**Paper-safe wording:**

> Relative to the retained canonical Cl(3) connection normalization
> `Tr(T_a T_b)=delta_ab/2`, the Wilson surface has no independent
> `A -> A/g` rescaling freedom. The accepted Wilson matching fixes
> `g_bare=1` and `beta=6` for `N_c=3`.

**What the paper should NOT say:**

- "g = 1 is derived from a dynamical fixed-point condition"
- "g = 1 is the maximum-entropy coupling"
- "g = 1 is selected by the lattice beta function"

These are false.  The derivation is algebraic/normalization-based,
not dynamical.

---

## Commands Run

The original 2026-04-12 note recorded an older diagnostic runner with one
expected bounded failure from the mean-field fixed-point route. That historical
diagnostic is not the parent re-audit surface.

**2026-05-03 parent re-audit runner:**

```
python3 scripts/frontier_g_bare_derivation.py
```

Expected summary on the current parent re-audit surface:

```
EXACT   : PASS = 51, FAIL = 0
BOUNDED : PASS = 4, FAIL = 0
TOTAL   : PASS = 55, FAIL = 0
```

---

## Provenance Chain Update

| Input | Value | Status (before) | Status (after) |
|-------|-------|-----------------|----------------|
| g_bare | 1.0 | stale bounded-normalization claim | open main gate; parent re-audit required |
| sigma_v = pi*alpha^2/m^2 | -- | IMPORTED | IMPORTED (unchanged) |
| V(r) = -alpha/r | -- | IMPORTED | IMPORTED (unchanged) |

---

## Relationship to Other Approaches (from task specification)

| Approach | Result | Status |
|----------|--------|--------|
| (1) Unitarity bound | g=1 makes U unitary but so does any g | Not selecting |
| (2) Strong-coupling fixed point | SU(3) has no nontrivial fixed point | Does not work |
| (3) Canonical Cl(3) normalization + Wilson matching | **g = 1 candidate after audit gate** | **open main gate; parent re-audit required** |
| (4) Maximum entropy | Selects g -> infinity | Does not work |
| (5) Staggered Dirac normalization | Consistent with g = 1 | Supporting, not standalone |
