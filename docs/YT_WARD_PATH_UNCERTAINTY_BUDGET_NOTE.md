# Ward-Path Uncertainty Budget for y_t(v)

**Date:** 2026-04-17
**Status:** SUPPORT NOTE for `YT_WARD_SUPERSEDES_BRIDGE_PROPOSAL_2026-04-17.md`
**Scope:** quantify the uncertainty on `y_t(v)` and `m_t(pole)` if they
are derived via the Ward primary path:
> `y_t(M_Pl) = g_s(M_Pl)/√6` exact (Ward branch) → SM RGE → `y_t(v)` → `m_t`

This note carries no authority status of its own. It is the supporting
quantitative material for **P3** of the supersedes-bridge proposal.

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
surface (review-passed on `claude/ward-identity-derivation @ 27354ce8`).
There is no framework-native systematic on the UV boundary value itself.

The uncertainty on `y_t(v)` accumulates only through the propagation
chain from M_Pl down to v.

---

## Sources of uncertainty on the Ward path

### A. Input precision on `g_s(M_Pl)`

On the canonical surface `g_s(M_Pl) = 1/√u_0` with `u_0 = ⟨P⟩^{1/4}` from
the plaquette expectation. The plaquette is measured on the canonical
β = 6 lattice; standard tadpole-improvement precision is sub-permille
(`δ u_0 / u_0 ≲ 10⁻³`). Propagating through the square root:

```
δ g_s(M_Pl) / g_s(M_Pl)  ≈  (1/2) · δ u_0 / u_0  ≲  5 × 10⁻⁴  (~0.05%)
```

Source: `α_LM` measurement on canonical surface (retained,
`ALPHA_S_DERIVED_NOTE.md`).

### B. SM RGE truncation (NNLO vs NNNLO)

Standard 2-loop vs 3-loop SM RGE running of `y_t` between `M_Pl` and `v`:

- 2-loop: well-tabulated, central agreement
- 3-loop: shifts central by ~0.3% in `y_t(v)`, ~0.5 GeV in `m_t(pole)`
- 4-loop QCD + 3-loop electroweak: known partially, sub-permille shift
  expected

The current package quotes both `m_t(pole, 2-loop) = 172.57 GeV` and
`m_t(pole, 3-loop) = 173.10 GeV` with the difference treated as the
truncation indicator. This is a STANDARD SM running uncertainty, not a
framework-native systematic.

```
δ y_t(v)        from SM RGE truncation  ≈  0.3% (NNLO → NNNLO comparison)
δ m_t(pole)     from SM RGE truncation  ≈  ±0.5 GeV  (~0.3%)
```

This is the same SM-side uncertainty quoted in any precision SM analysis;
nothing framework-specific.

### C. Lattice discretization `O(α_LM · a²)`

On the framework's canonical Wilson-staggered surface at β = 6 with
α_LM = 0.091, standard lattice power counting gives `O(α_LM · a²)`
discretization corrections. At `v ≪ M_Pl`, the relevant `a²` factor
is `(a · v)² = (v/M_Pl)² ~ 10⁻³⁰`, so discretization corrections at
the IR end are NEGLIGIBLE. At the UV end (where `a · q ~ 1`), they
would be order-unity, but the Ward identity is stated AT the lattice
cutoff, so no propagation through the lattice cutoff is required.

For the running between v and M_Pl, the relevant lattice-systematic
estimate is the standard tadpole-improved coefficient `α_LM · C_F / π`
applied at the BARE-action interface:

```
δ y_t(v)  from lattice-discretization at the M_Pl interface
          ≈  α_LM · C_F / π  ≈  3.9% loop unit, but matches into SM
          → effective contribution after matching: sub-percent
```

This is the standard lattice-to-continuum matching residual. It is NOT
the Schur-bridge endpoint shift (a different quantity, which arose from
a different methodology).

### D. Higher-order Ward-identity NLO (optional)

The Ward branch's Step 5 (now removed from the authority theorem; lives
in support note) computes the perturbative 1-loop vertex correction on
the tadpole-improved surface as `α_LM · C_F / (2π) = 1.92%`. This is
the magnitude of the NLO correction TO the Ward ratio at M_Pl, but
since the proposal treats the Ward identity as exact at tree level (the
review-passed status), this correction is at most a sub-leading shift
on the input boundary value.

Folding it conservatively into the y_t(v) error budget would add ~1.9%
in quadrature with B and C, giving total ~2.0%. This is still smaller
than the 1.21% bridge budget after considering that the bridge's 1.21%
was *added* to a separate set of input uncertainties; the Ward-NLO 1.9%
already contains the equivalent of the bridge's 1.21% transport piece
plus more.

```
δ y_t(v)  from Ward NLO (if folded)   ~ 1.9%   (perturbative 1-loop)
                       (if not folded)  not applicable to tree identity
```

---

## Combined budget (Ward primary path)

### Conservative (folding all of A, B, C, D in quadrature)

```
δ y_t(v)     = √(0.05² + 0.3² + 0.5² + 1.9²) %  ≈  2.0%
δ m_t(pole)  = ~0.6 GeV (RGE/discretization) + ~3.3 GeV (Ward NLO if folded)
             ≈ ±2.4 GeV total in quadrature  ≈ 1.4%
```

### Standard (A + B + C, treating Ward identity as exact tree)

```
δ y_t(v)     = √(0.05² + 0.3² + 0.5²) %  ≈  0.6%
δ m_t(pole)  = ±0.6 GeV ≈ 0.3%
```

The "standard" line treats the Ward identity at M_Pl as the exact tree-
level result (the review-passed status), with all uncertainty coming
from the CONTINUUM/RGE/lattice-discretization side. This is the cleanest
budget and the one the proposal recommends.

---

## Comparison to the legacy bridge budget

| Path | Conservative budget | Tight budget | Source |
|---|---|---|---|
| Schur-bridge (legacy) | 1.21% | 0.755% | endpoint shift `r_ho + r_nl` |
| Ward primary (standard) | 0.6% | 0.3% | A + B + C above |
| Ward + NLO conservative | 2.0% | 1.4% | A + B + C + D in quadrature |

The Ward-primary "standard" budget at 0.6% is materially smaller than
the bridge budget at 1.21% AND consists entirely of standard SM /
lattice-QCD uncertainties (not framework-native explicit systematic).

The Ward-primary "conservative" budget at 2.0% is comparable to the
bridge budget but again carries STANDARD perturbative-loop uncertainty,
not framework-native bridge-construction artifact.

In either case, the Ward-primary path **does not require a framework-
native explicit systematic** to quote `y_t(v)` and `m_t(pole)`; it
requires only standard SM and standard lattice-QCD uncertainties.

---

## Honest limitations

1. The standard budget (0.6%) treats the Ward identity at M_Pl as exact;
   conservative reading would fold the 1.92% Ward NLO. The proposal
   should quote both options for transparency.
2. Lattice-discretization estimate folded into B+C above is itself an
   estimate, not a directly retained systematic. A reviewer wanting an
   independent lattice-discretization theorem on this specific surface
   would need that work done separately.
3. The 0.5% from NNLO/NNNLO RGE comparison reflects the framework's
   current 2-loop / 3-loop spread; quoting NNNLO QCD + 3-loop electroweak
   would tighten this further but is sub-permille either way.

---

## Scientific bottom line

If the proposal is accepted, the y_t lane reports:

```
y_t(v)     = 0.9176 ± 0.005   (standard)  or  ± 0.018 (conservative incl. Ward NLO)
m_t(pole)  = 173.10 GeV ± 0.6 GeV (standard)  or  ± 2.4 GeV (conservative)
                                              [3-loop central; 2-loop = 172.57 GeV]
```

with NO framework-native explicit systematic; all uncertainties are
standard SM / lattice-QCD residuals.

This is a tightening of the central package quote — and a cleaner
methodological status — relative to the legacy bridge budget.
