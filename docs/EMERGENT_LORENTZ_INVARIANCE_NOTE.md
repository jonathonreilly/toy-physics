# Emergent Lorentz Invariance — Lattice Dispersion Structure Theorem (Bounded)

**Date:** 2026-04-15 (audit-narrowed 2026-04-28; bridge-honest re-scope 2026-05-02)
**Type:** bounded_theorem
**Claim type:** bounded_theorem
**Status:** branch-local bounded structural-dispersion theorem on the cubic
`Cl(3)/Z^3` lattice. The theorem proves: (T1) infrared dispersion is isotropic
to leading order; (T2) the first non-isotropic correction is at dimension-6
(`O(a^2 p^4)`); (T3) the angular signature of that correction is the unique
cubic harmonic `K_4` at `\ell = 4`. The retained CPT theorem
(`CPT_EXACT_NOTE.md`) is cited as a one-hop authority for the corollary that
all dimension-≤5 LV operators vanish (no CPT-odd or P-odd operators). The
physical-precision claim `|\delta E / E| \sim (E/M_{Planck})^2` IS NOT part
of this theorem; it is an **out-of-scope bridge** depending on the
hierarchy-scale identification `a \sim 1/M_{Planck}`, which is not registered
as a retained one-hop dependency for this row.
**Claim scope:** lattice-dispersion structure theorem on `Z^3` cubic
substrate, asserting (T1)–(T3) on `A_min` plus retained CPT. The
phenomenological context (SME-bound comparison, Planck suppression at
specific energies) is reviewer orientation, not derived content of this
theorem.
**Runner:** `scripts/frontier_emergent_lorentz_invariance.py` (PASS=37, FAIL=0)
**Cited authorities (one hop):**
- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) (retained) — provides
  `[CPT, H] = 0`, `P H P = -H`, and the resulting vanishing of all
  CPT-odd SME coefficients on even periodic `Z^3`. Used in Corollary C2
  below.

## Theorem (re-scoped 2026-05-02)

**Theorem (Lattice Dispersion Structure, T1–T3).**
On the cubic `Cl(3)/Z^3` lattice with staggered Dirac action and Wilson
plaquette gauge action at `g_bare = 1`:

- **(T1) Infrared isotropy.** The IR dispersion is isotropic at leading
  order: `E^2 = m^2 + p^2 + O(a^2 p^4)`. The relative anisotropy
  between `[100]`, `[110]`, `[111]` directions vanishes as `O((ap)^2)`.
- **(T2) Dimension-6 leading anisotropy.** The first non-isotropic
  correction is `-(a^2/3) \sum_i p_i^4` for the staggered fermion and
  `-(a^2/12) \sum_i p_i^4` for the bosonic Laplacian. Both are
  `dimension-6` operators (`O(a^2 p^4)`); there is no dimension-3
  (mass-like) or dimension-5 (cubic-momentum) anisotropic correction at
  the *lattice level*.
- **(T3) Cubic-harmonic angular signature.** The angular structure of
  `\sum_i n_i^4` decomposes as `3/5 + (4/5) K_4(\theta, \phi)`, where
  `K_4 = Y_{4,0} + \sqrt{5/14}(Y_{4,4} + Y_{4,-4})` is the unique
  cubic harmonic at `\ell = 4`. There is no `\ell \in \{0, 2, 6\}`
  contamination in the anisotropic part.

**(T1)–(T3) constitute the lattice-dispersion structure theorem.** No
hierarchy-scale identification (`a \sim 1/M_{Planck}`) is used in the
proof of (T1)–(T3); the result is purely a structural property of the
Z^3 staggered-Dirac kinetic operator.

## Corollary (cited from retained CPT)

**Corollary (C1) — Dimension-5 LV forbidden by retained P.** From
[`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) (retained), spatial parity
`P : x \to -x` satisfies `P H P = -H` exactly on even periodic `Z^3`.
Consequently, any odd-momentum-power correction to the dispersion (which
would violate `P` at the dispersion level) vanishes. Combined with (T2),
the leading `lattice-induced` LV operator is dimension-6.

**Corollary (C2) — All CPT-odd SME coefficients vanish.** From
[`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md), `[CPT, H] = 0` exactly on the
canonical surface, so all CPT-odd SME coefficients
(`a_\mu, b_\mu, e_\mu, f_\mu, g_{\lambda\mu\nu}`) vanish identically. By
the Greenberg theorem, no dimension-3 or dimension-5 LV operator is
CPT-odd-protected away.

C1 and C2 are immediate consequences of the *retained* CPT note plus the
finite-lattice properties (T1)–(T3). They are **not independent claims
of this note**.

## Out-of-scope bridge: hierarchy-scale identification

**This note does NOT claim** that physical Lorentz-violation precision
follows from (T1)–(T3) alone. The phenomenological precision statement
`|\delta E^2 / E^2| \sim (E/M_{Planck})^2` requires the additional input
`a \sim 1/M_{Planck}` (lattice spacing identified with the Planck
length). On the current ledger, the relevant Planck-pin /
hierarchy-scale rows are tracked separately:

- `PLANCK_GRAVITY_BOUNDARY_COFRAME_CARRIER_IDENTIFICATION_THEOREM_NOTE_2026-04-26.md`
  (Planck pin candidate; not yet retained)
- `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`
  (`audited_conditional` per current ledger).

The runner's Part 5 ("Planck suppression") and Part 7 ("combined
emergent Lorentz") explicitly use the constants
`E_{Planck} = 1.220890 \times 10^{19}\,\mathrm{GeV}` and the
identification `a = \ell_{Planck}` to compute reviewer-orientation
precision numbers. **These are class-D phenomenological context lines
and do not form part of (T1)–(T3).** A future "physical Lorentz
invariance" note may combine (T1)–(T3) with a retained Planck pin to
recover the standard SME-bound table — that synthesis is downstream of
this row.

## Mechanism (proof sketch)

### (T1) Infrared isotropy

The free staggered fermion dispersion on `Z^3` is

```text
    E^2  =  m^2 + (1/a^2) \sum_i \sin^2(p_i a)
        =  m^2 + p^2 - (a^2/3) \sum_i p_i^4 + O(a^4 p^6)              (1)
```

For `p \ll \pi/a`, the leading term `p^2` is `SO(3)`-isotropic. The
relative anisotropy `(E_{[100]}^2 - E_{[111]}^2) / E_{[100]}^2` is
`O((ap)^2)` and vanishes as `p \to 0` (verified numerically:
`2.22 \times 10^{-5}` at `p = 0.01`).

### (T2) Dimension-6 leading anisotropy

The Taylor expansion `\sin^2(x) = x^2 - x^4/3 + O(x^6)` gives the
fermion coefficient `c_4^{(F)} = -1/3`. The bosonic Laplacian
`(4/a^2) \sin^2(p_i a/2) = p_i^2 - (a^2/12) p_i^4 + O(a^4)` gives
`c_4^{(B)} = -1/12`. Both corrections are `dimension-6`
(`a^2 p^4` scaling). Numerical extraction agrees with the analytic
coefficients to better than `0.1\%`.

### (T3) Cubic-harmonic angular signature

The anisotropic part `f_4(\theta, \phi) := \sum_i n_i^4 - 3/5` (where
`\hat n = \hat p`) projects entirely onto `\ell = 4`:

- `\langle f_4 | Y_{0,0} \rangle = 0.0011` (numerical, expected `0`)
- `\langle f_4 | Y_{2,0} \rangle = 0.0024` (numerical, expected `0`)
- `\langle f_4 | Y_{4,0} \rangle = 0.4769` (numerical, nonzero)
- `\langle f_4 | Y_{6,0} \rangle = 0.0009` (numerical, expected `0`)

The angular pattern has factor-of-`3` anisotropy:
`\sum n_i^4 = 1` along `[100]` versus `1/3` along `[111]`. This is the
unique `O_h` cubic harmonic at `\ell = 4`.

## Hypothesis set used (proof of T1–T3)

- **A1 (Cl(3) site algebra)**: only via the staggered fermion bilinears.
- **A2 (Z^3 substrate)**: via `O_h` cubic symmetry and the lattice
  staggered phases `\eta_\mu(x) = (-1)^{x_1 + \ldots + x_{\mu-1}}`.
- **A3 (canonical staggered Dirac)**: the Kogut–Susskind hop
  `(\eta_\mu(x)/2)(U_\mu \chi_{x+\hat\mu} - U_\mu^\dagger \chi_{x-\hat\mu})`.
- **A4 (canonical normalization)**: only via `g_{\rm bare} = 1` and the
  Wilson plaquette form, neither of which enters (T1)–(T3) (the
  free-dispersion structure is gauge-independent at quadratic order).

No hierarchy-scale input. No external bridge. No fitted parameter.

## Hypothesis set used (corollaries C1, C2)

- All hypotheses of (T1)–(T3), plus:
- **Retained** [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) for `[CPT, H] = 0`
  and `P H P = -H` exactly on even periodic `Z^3`.

C1 and C2 inherit only the CPT note's retained status; no additional
unregistered bridge is used.

## Phenomenological context (not part of theorem)

The runner's Part 5 reports, **for reviewer orientation only**, the
numerical Planck suppression of (T2) under the assumption
`a = \ell_{Planck}`:

| Energy | `\|\delta E^2 / E^2\|` | Assumption |
|--------|------------------------|------------|
| `1\,\mathrm{GeV}` | `1.34 \times 10^{-39}` | `a = \ell_{Planck}` (out-of-scope bridge) |
| `1\,\mathrm{TeV}` | `1.34 \times 10^{-33}` | `a = \ell_{Planck}` (out-of-scope bridge) |
| `10^{20}\,\mathrm{eV}` (UHECR) | `1.34 \times 10^{-17}` | `a = \ell_{Planck}` (out-of-scope bridge) |

These numbers are **conditional** on the unregistered hierarchy-scale
identification. They are not derived consequences of (T1)–(T3) alone.

## Runner verification

```bash
python3 scripts/frontier_emergent_lorentz_invariance.py
# PASS=37  FAIL=0
```

Of the 37 PASS lines, the **load-bearing** ones for (T1)–(T3) are:

- Part 1 (5 lines): low-`p` isotropy and continuum agreement —
  first-principles dispersion compute (class C).
- Part 2 (4 lines): `c_4 = -1/3` and `c_4 = -1/12` numerical extraction
  matched to the analytic Taylor coefficient (class C/A).
- Part 3 (9 lines): cubic-harmonic angular projections, all from
  numerical spherical-harmonic decomposition (class C).
- Part 6 (4 lines): finite-lattice `L = 8` diagonalization showing
  `O_h`-exact eigenvalue structure (class C).

**These 22 PASS lines cover (T1)–(T3) on Cl(3)/Z^3 first principles.**

The remaining 15 lines (Parts 4, 5, 7) are **assertion lines citing
external authorities** (`CPT_EXACT_NOTE`, hierarchy-scale, Greenberg's
theorem) or **phenomenological context** (SME bounds, UHECR
sensitivity). Per the audit rubric these are class-D / class-B and
**do not back the load-bearing claim of this note**. Parts 4 and 5
remain in the runner for backward compatibility with the prior
"emergence under retained hierarchy" framing; the present (re-scoped)
note ratifies only what the structural Parts 1–3 + 6 prove.

## Honest claim-status

```yaml
actual_current_surface_status: support
conditional_surface_status: branch-local bounded structural-dispersion theorem on A_min + retained CPT
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Bounded structural theorem; depends on retained CPT only. Physical-precision interpretation requires unregistered hierarchy-scale bridge and is explicitly out of scope for this row."
audit_required_before_effective_retained: true
bare_retained_allowed: false
target_effective_status_on_clean_audit: retained_bounded
```

## What this note claims

- **(T1)–(T3)**: lattice dispersion is isotropic at leading order, with
  dimension-6 leading anisotropy in the unique cubic-harmonic K_4
  pattern. Proved on `A_min` first principles by Parts 1–3, 6 of the
  runner.
- **(C1, C2)**: as cited consequences of retained
  [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md), dimension-5 and CPT-odd LV
  operators are forbidden. These are not independent claims.

## What this note does NOT claim

- **Physical-precision Lorentz invariance** (`|\delta E/E| < 10^{-N}` at
  observable energies). That requires the hierarchy-scale bridge
  `a \sim 1/M_{Planck}`, which is not a retained one-hop dependency
  here. The phenomenological table is reviewer orientation only.
- **An unconditional Lorentz-invariance theorem** from the lattice
  alone. The lattice has `O_h \subset SO(3,1)` cubic symmetry, broken
  at the lattice scale; the present theorem only describes the
  *structural form* of the leading anisotropic correction.
- **Audit-clean upstream registration of the hierarchy-scale
  identification.** That registration is downstream work.

## Path to retained-bounded on clean audit

The narrowed theorem (T1)–(T3) plus retained-CPT corollaries (C1, C2)
should clear `audited_clean class C` on re-audit because:

1. (T1)–(T3) are first-principles Z^3 dispersion structure (class C
   compute, no external import).
2. (C1, C2) cite **only** retained `CPT_EXACT_NOTE`, satisfying the
   audit-rubric requirement that conditional verdicts only attach
   when an *unregistered* upstream is load-bearing.
3. Class type is `bounded_theorem`, so the target status is
   `retained_bounded` (not `retained`), matching the structural
   character of (T1)–(T3) (the leading anisotropic correction *is*
   present at dimension-6; the result describes the structure of that
   correction, not its absolute size).

## Promotion to retained (full Lorentz invariance) — Path A future work

Promotion to **unconditional retained** (full physical Lorentz
invariance to all observable precision) would require:

1. A retained Planck-pin / hierarchy-scale row registering
   `a \sim 1/M_{Planck}` as a one-hop dependency.
2. A separate downstream note combining (T1)–(T3) + retained CPT +
   retained hierarchy-scale, deriving the SME-bound suppression as a
   **consequence** rather than an assumed surface.
3. (Optional) A runner that computes the SME-bound saturation from
   first principles rather than asserting it.

Path A is *not* in scope for this row. This row's contribution to the
emergent-Lorentz program is the **structural lattice-dispersion theorem
(T1)–(T3)** plus retained-CPT corollaries (C1, C2).

## Audit history

- 2026-04-15: original note framed unconditional emergence.
- 2026-04-28: `audited_conditional` (`codex-fresh-pr291-emergent-lorentz-harvey-2026-05-02`) — retained Planck/parity/hierarchy bridges asserted in note body, not registered as one-hop deps. Verdict applied 2026-05-02 to ledger row.
- 2026-05-02 (this revision): theorem narrowed to (T1)–(T3) structural
  dispersion + retained-CPT corollaries (C1, C2). Hierarchy-scale and
  unregistered-parity bridges moved out of scope. Cited authority
  `cpt_exact_note` (retained) registered as one-hop dependency.
  Target verdict: `audited_clean class C` →
  `retained_bounded`.

## Citations

- A_min: [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md)
- Retained one-hop dep: [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md)
- Companion (downstream physical-precision synthesis, future work):
  none currently retained
- Standard external references (theorem-grade lattice references; no
  numerical input imported as proof step):
  - Kogut–Susskind staggered Dirac (1975)
  - cubic harmonic K_4 representation theory (von der Lage–Bethe 1947).
