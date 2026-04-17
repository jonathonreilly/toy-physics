# Ward-Path Uncertainty Budget for y_t(v)

**Date:** 2026-04-17 (v2, addresses review of v1)
**Status:** SUPPORT NOTE for `YT_WARD_SUPERSEDES_BRIDGE_PROPOSAL_2026-04-17.md`
**Scope:** quantify the uncertainty on `y_t(v)` and `m_t(pole)` if they
are derived via the Ward primary path:
> `y_t(M_Pl) = g_s(M_Pl)/√6` exact (Ward, on main) → SM RGE → `y_t(v)` → `m_t`

This note carries no authority status of its own. It is the supporting
quantitative material for **P3** of the supersedes-bridge proposal.

---

## Honest correction from v1

A reviewer correctly flagged that v1 of this note asserted a sub-percent
"standard" Ward-path budget without deriving the lattice-discretization /
matching residual on this surface. v1's "≈0.6%" line was reached by
moving from `α_LM · C_F / π ≈ 3.9%` at the bare interface to
"effective contribution after matching: sub-percent" without showing the
arithmetic.

This v2 corrects that. The honest Ward-path budget on the canonical
surface is **comparable to** the legacy Schur-bridge budget, not
materially smaller. The case for supersession therefore rests on
**methodological character** (replacing framework-native explicit
systematic with standard SM perturbative residuals), not on a
numerical reduction in the quoted error.

---

## Setup

Central inputs (all retained):

```
α_LM(M_Pl)   = α_bare / u_0    = 0.0907         (canonical surface)
g_s(M_Pl)    = √(4π α_LM)      = 1/√u_0 = 1.0674
y_t(M_Pl)    = g_s(M_Pl)/√6    = 0.43577        (Ward identity, exact tree)
v            = 246.22 GeV                       (electroweak VEV input)
m_t(pole)    = standard SM matching at v        (well-known)
```

The Ward identity at M_Pl is **exact at tree level** on the canonical
surface (review-passed and landed on main as
`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`). There is no
framework-native systematic on the UV boundary value itself.

The uncertainty on `y_t(v)` accumulates through the propagation chain
from M_Pl down to v.

---

## Sources of uncertainty on the Ward path (honest accounting)

### A. Input precision on `g_s(M_Pl)` — DERIVED

On the canonical surface `g_s(M_Pl) = 1/√u_0` with `u_0 = ⟨P⟩^{1/4}` from
the plaquette expectation. Standard tadpole-improvement gives
`δ u_0 / u_0 ≲ 10⁻³`. Propagating through the square root:

```
δ g_s(M_Pl) / g_s(M_Pl)  ≈  (1/2) · δ u_0 / u_0  ≲  5 × 10⁻⁴   (~0.05%)
```

Source: `α_LM` measurement on canonical surface (retained,
`ALPHA_S_DERIVED_NOTE.md`). This is genuinely sub-permille.

### B. SM RGE truncation (NNLO vs NNNLO) — STANDARD SM, not derived here

Standard 2-loop vs 3-loop SM RGE running of `y_t` between `M_Pl` and `v`:

- 2-loop central: `m_t(pole) = 172.57 GeV`
- 3-loop central: `m_t(pole) = 173.10 GeV`
- Spread: 0.53 GeV / 173 GeV ≈ 0.31%

The current package quotes both as the truncation indicator. This is a
STANDARD SM running uncertainty published in any precision SM analysis;
nothing framework-specific.

```
δ m_t(pole) from SM RGE truncation  ≈  ±0.5 GeV  (~0.3%)
δ y_t(v)    from SM RGE truncation  ≈  0.3%
```

This is asserted as standard SM result. The reviewer should evaluate
this as the framework citing standard published SM running, not as a
framework-native derivation.

### C. Lattice-to-continuum matching at the M_Pl interface — NOT smaller than the perturbative loop

This is where v1 of this note made the load-bearing error. Honest accounting:

The Ward identity gives `y_t_bare = g_bare/√6` on the canonical bare
lattice. To convert this to `y_t(M_Pl)` in continuum (e.g., MS-bar)
scheme, a lattice → continuum matching is required. On the
tadpole-improved Lepage-Mackenzie surface, this matching at 1-loop has
the standard magnitude

```
δ y_t(M_Pl) / y_t(M_Pl)  ~  α_LM · C_F / (2π)  =  1.92%
```

This is *the same number* as the Ward-derivation NLO bound from Block 9
of `frontier_yt_ward_identity_derivation.py`. The lattice-discretization
residual at the cutoff matching IS the perturbative 1-loop vertex
correction; treating them as separate sources would double-count.

The honest budget therefore folds B and C as a single source (1-loop
matching + RGE truncation) rather than asserting they are independent
sub-percent contributions.

### D. Lattice discretization at IR scales (`O(α_LM · (a · μ)²)`) — genuinely small

For physical observables at scale `μ ≪ M_Pl = 1/a`, the
discretization corrections scale as `(a · μ)² = (μ/M_Pl)²`. At
`μ ~ v = 246 GeV`, this gives `(v/M_Pl)² ~ 10⁻³⁰`, completely
negligible. This is genuinely sub-permille on standard
lattice-QCD power counting.

Note: this is DIFFERENT from C above. C is the matching at the UV
interface (where lattice and continuum descriptions meet); D is the
discretization at IR observables (where the lattice is far below
its cutoff). C is the load-bearing residual; D is genuinely tiny.

---

## Combined Ward-path budget (honest version)

### Standard (1-loop matching + RGE truncation in quadrature)

```
δ y_t(v)     = √(0.05² + 0.3² + 1.92²) %  ≈  1.95%
δ m_t(pole)  ≈  ±3.4 GeV  in quadrature
```

### NNLO matching (if computed)

The 2-loop matching residual is `(α_LM · C_F / π)² = 0.15%` (from
Block 9 of the Ward runner, NNLO perturbative). This would tighten
the matching residual to NNLO, but only with the work to actually
compute the 2-loop matching shift, which is not in the retained
package today.

```
δ y_t(v)  with NNLO matching computed   ≈  ~0.4%   (RGE + NNLO matching)
                                                    + small 1-loop residual
```

This is the budget the supersession case would TARGET if NNLO matching
were retained. It is not retained today.

---

## Comparison to the legacy Schur-bridge budget — apples to apples

| Path | Conservative budget | Tight budget | Methodological character |
|---|---|---|---|
| Schur-bridge (legacy) | 1.21% | 0.755% | framework-native explicit systematic |
| Ward primary (1-loop matching) | ~1.95% | ~1.95% | standard SM PT + lattice 1-loop |
| Ward primary (NNLO matching, future work) | ~0.4% | ~0.4% | standard SM PT + lattice NNLO |

**Honest read of the comparison:** at the current level of computational
work (1-loop on both paths), the Ward-path budget (~1.95%) is
**numerically comparable to or slightly larger than** the legacy
bridge budget (1.21% conservative). The Ward path becomes numerically
tighter only if NNLO lattice matching is computed (which is not
in the current retained package).

The supersession case therefore does NOT rest on a numerical reduction
in the quoted error. It rests on the **methodological character of
the residual**:

- Schur-bridge 1.21% is **framework-native**: it is the bound on the
  gap between SM RGE and an unspecified "true lattice blocking flow"
  in a constructed bridge operator. It exists because the framework
  introduced a methodology that requires it.
- Ward 1.92% is **standard perturbation theory on the tadpole-improved
  Lepage-Mackenzie surface**: it is the standard 1-loop matching
  uncertainty quoted in any lattice-QCD analysis at this `α_LM`. It
  exists in any lattice gauge theory; it is not a framework-specific
  construct.

The proposal asks the reviewer to accept that **a 1.92% standard SM
+ lattice 1-loop budget is methodologically preferable to a 1.21%
framework-native explicit-systematic budget** — even though the
former is numerically larger — because the former's character is
standard published methodology and the latter's character is
framework-native systematic that requires its own retained
justification.

If the reviewer judges that a smaller framework-native budget is
preferable to a larger standard-method budget, the supersession case
fails on numerical grounds and the existing wording stays.

---

## Honest limitations

1. **The 1.92% matching residual is the same as the Ward-NLO loop
   correction.** They are not independent sources to fold separately.
2. **NNLO lattice matching is not in the retained package today.** The
   "~0.4% future" line is a target that requires actual NNLO matching
   work to be done.
3. **Standard SM RGE running is treated as standard published methodology.**
   If the reviewer disputes that for the framework's specific surface,
   the supersession case fails.
4. **Lattice-discretization at IR scales (D)** is genuinely tiny but
   estimated by power counting, not measured on this surface.

---

## Scientific bottom line (revised)

If the proposal is accepted:

```
y_t(v)     = 0.9176 ± 0.018  (Ward path, 1-loop matching + RGE)
m_t(pole)  = 173.10 GeV ± 3.4 GeV (3-loop central; 2-loop = 172.57 GeV)
```

Numerically comparable to the legacy Schur-bridge budget. The change
the proposal asks for is **methodological**: replacing the framework-
native explicit systematic wording with standard-PT-residual wording,
without claiming a tighter quantitative budget.

The route to a tighter Ward-path budget runs through NNLO lattice
matching, which is future work and not in scope for the present
proposal.
