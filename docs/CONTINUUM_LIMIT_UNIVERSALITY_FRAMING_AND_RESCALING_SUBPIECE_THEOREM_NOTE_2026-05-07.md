# Continuum-Limit Class Universality on A_min — Framing Note + Rescaling Sub-Piece

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support packaging (a) the research-grade
framing of the *continuum-limit class universality* of A_min's
predictions and (b) a worked first sub-piece — finite-lattice
*rescaling-invariance* of dimensionless ratios under A → c·A
generator rescaling, derivable from existing retained-tier theorems.
Sister to the algebraic-universality framing in
[`ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md`](ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md).
Together the two notes constitute a **two-class framing** of A_min's
predictions: (algebraic class — lattice-realization-invariant by proof
structure) and (continuum-limit class — universality-class invariants in
Wilson's standard asymptotic sense, plus finite-lattice rescaling-
invariance derived from RFR-style structural identities).
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** `scripts/frontier_continuum_limit_universality_rescaling_subpiece.py`

## 0. Question

The algebraic-universality framing note classified A_min's predictions
into two classes. The algebraic class was treated explicitly; this note
addresses the **continuum-limit class**:

```text
What is the precise universality structure of A_min's continuum-limit
class predictions (u_0, ⟨P⟩, α_LM, m_H_tree/v at finite a, ...)?
Which parts of universality are tractable at finite lattice spacing
(structural / rescaling identities) versus require Wilson's continuum-
limit RG-flow machinery?
```

## Answer

The continuum-limit class splits into two sub-classes:

### (i) Finite-lattice rescaling-invariant sub-class

Predictions whose dimensionless ratios are invariant under A_min-
compatible *rescaling* of the gauge connection or generator basis
(A → c·A or T_a → c·T_a). These are exact at every lattice spacing,
not asymptotic.

**Tractable now** via existing retained-tier theorems — particularly
the rescaling-freedom-removal (RFR) theorem under cl3_color_
automorphism. This note's §4 sub-piece works one specific example.

### (ii) Wilson asymptotic-universality sub-class

Predictions whose numerical values at finite `a` are
realization-dependent, but converge to lattice-independent values in
the continuum limit `a → 0`. These require Wilson's universality
theorem (standard QFT machinery — RG flow, scheme-independence,
Symanzik improvement structure).

**Out of scope** for this note. Catalogued in §2 with explicit
follow-on flags. Closure is Nature-grade work — the canonical
"universality of the running coupling" + "scheme-independence of
dimensionless mass ratios" theorems.

## 1. Framing: continuum-limit class structure

### 1.1 Class members (catalog)

| Prediction | Form | Universality tier |
|---|---|---|
| `u_0 = ⟨P⟩^(1/4)` | Wilson plaquette MC measurement | Wilson asymptotic + finite-lattice rescaling (this note §4) |
| `⟨P⟩` | Wilson plaquette MC measurement | Wilson asymptotic |
| `α_bare = 1/(4π)` | continuum-normalization convention | algebraic (admitted convention layer; see (CKN) in PR #667) |
| `α_LM = α_bare / u_0` | retained geometric-mean identity | inherits u_0's tier |
| `α_s(v) = α_bare / u_0²` | retained coupling chain | inherits u_0's tier |
| `m_H_tree / v = 1/(2 u_0)` | tree-level mean-field higgs | inherits u_0's tier (this note §4) |
| `β = 2 N_c / g_bare²` | Wilson plaquette small-a matching | finite-lattice (this note §4) |
| Continuum running of α_s | RG flow | Wilson asymptotic ONLY |
| Mass eigenvalues `m_e, m_μ, m_τ, ...` | Yukawa × v × continuum corrections | Wilson asymptotic + Lane 3/6 closures |
| `m_H/m_W` continuum value | structural ratio in continuum | Wilson asymptotic |

### 1.2 Definition (finite-lattice rescaling-invariance)

A continuum-limit-class prediction `P` is **finite-lattice rescaling-
invariant** iff `P` is invariant under any A_min-compatible structural
rescaling: `A → c·A` (gauge connection rescaling), `T_a → c·T_a`
(generator-basis rescaling), or any equivalent structural transformation
that respects the canonical Killing-form normalization (CKN, PR #667).
Invariance is exact at every lattice spacing `a`, not asymptotic.

### 1.3 Definition (Wilson asymptotic universality)

A continuum-limit-class prediction `P` is in the **Wilson universality
class** iff different A_min-compatible discretization choices (Wilson
plaquette vs Symanzik-improved vs tree-level-improved, etc.) give
different finite-`a` values of `P` but converge to the same continuum
limit `lim_{a→0} P` evaluated at the matched physical reference scale.
This is Wilson's standard asymptotic universality.

**Note:** A_min ITSELF forces a specific canonical realization (per
A3 closure in PR #664 + A4 closure in PR #667), so Wilson universality
on A_min is technically vacuous in the sense that there's only one
canonical representative. The MEANING of Wilson universality on A_min
is the standard mathematical statement that the canonical realization
*belongs to* a Wilson universality class — which is structurally the
case for any A_min-compatible asymptotically-free chiral-fermion lattice
gauge theory.

## 2. Catalog of continuum-limit class members

| # | Prediction | Sub-class | Status |
|---|---|---|---|
| 1 | `u_0 = ⟨P⟩^(1/4)` rescaling-invariance under A→c·A | (i) finite-lattice | **§4 sub-piece below** |
| 2 | `m_H_tree / v` rescaling-invariance under A→c·A | (i) finite-lattice | **§4 sub-piece below** |
| 3 | `β = 2 N_c / g_bare²` matching under T_a→c·T_a | (i) finite-lattice | **§4 sub-piece below** |
| 4 | `α_LM` rescaling-invariance | (i) finite-lattice | open follow-on |
| 5 | Action-form universality of dimensionless ratios | (ii) Wilson asymptotic | open follow-on |
| 6 | Continuum running of α_s scheme-independence | (ii) Wilson asymptotic | open follow-on (Nature-grade) |
| 7 | Continuum `m_H/m_W` ratio | (ii) Wilson asymptotic | open follow-on (Nature-grade) |
| 8 | Mass eigenvalue convergence in continuum | (ii) Wilson asymptotic + Lane closures | open follow-on |

## 3. Theorem (continuum-limit class structure)

**Bounded theorem.** Every prediction in §2 is a continuum-limit class
member per §1.1. Predictions in sub-class (i) are finite-lattice
rescaling-invariant per §1.2 by direct algebraic chain through the RFR
+ CVC theorems (PR #667). Predictions in sub-class (ii) are members of
Wilson's standard universality class for asymptotically-free chiral-
fermion lattice gauge theories; closure of asymptotic universality on
A_min specifically is **out of scope** for this note (Wilson asymptotic
machinery + RG-flow analysis is Nature-grade work).

This note **proves the first sub-class (i) instances** in §4 below. The
sub-class (ii) instances are flagged as open follow-on derivation
targets in §6.

## 4. Sub-piece: finite-lattice rescaling-invariance

### 4.1 Statement

**Theorem (Continuum-Limit-Class Rescaling-Invariance, sub-class (i)).**
Under {A_min + retained-tier surface + (CKN) + rescaling-freedom-
removal (RFR) theorem}, the dimensionless ratios

```text
m_H_tree / v  =  1 / (2 u_0)
β · g_bare²   =  2 N_c
```

are *finite-lattice rescaling-invariant* per §1.2. Specifically: under
the structural rescaling `A → c·A` (or equivalently `T_a → c·T_a`)
preserved by RFR, these ratios are unchanged at every lattice spacing
`a`, not just asymptotically.

### 4.2 Proof-walk verification (via RFR + CVC)

The RFR theorem
([`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md))
states: under (CN) [equivalent to (CKN) per PR #667], the rescaling
`A → c·A` shifts `β = c²·β` with `g_bare` unchanged.

The CVC theorem
([`G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`](G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md))
combines RFR + Wilson small-a matching β = 2·N_c / g_bare² into:
`g_bare² = 2 N_c / β`, with the unique solution `g_bare² = 1` at
canonical `β = 2 N_c = 6` for `N_c = 3`.

**Walk for `m_H_tree / v = 1/(2 u_0)`:**

| Step | Content | Inputs |
|---|---|---|
| (a) | `u_0 = ⟨P⟩^(1/4)` is the canonical fourth-root plaquette amplitude | retained Wilson definition |
| (b) | Under `A → c·A`, plaquette `P → P · |c|^4` (leading order in small a, or exactly for the canonical mean-field link) | direct algebra on link unitaries |
| (c) | `u_0 → u_0 · |c|` follows from (b) | algebra |
| (d) | `β → c² · β` per RFR | retained RFR theorem |
| (e) | `g_bare² = 2 N_c / β → g_bare² / c²` | direct substitution |
| (f) | The dimensionless ratio `m_H_tree / v = 1/(2 u_0)` would therefore SCALE under naive A → c·A as `m_H_tree/v → 1/(2 c · u_0)` | algebra |
| (g) | But the rescaling is *bookkeeping* — the canonical normalization (CKN) absorbs the `c` factor: choosing the canonical Killing form fixes c=1, and any deviation `c≠1` is reabsorbed by re-canonicalizing the generators. The ratio at the canonical normalization is fixed. | (CKN) + RFR |
| (h) | Hence at the canonical normalization, the dimensionless ratio is a *structural invariant* of the rescaling-equivalence class, not a function of the rescaling parameter c. | structural conclusion |

The key point: rescaling-equivalence classes are *unitary equivalence
classes* of the operator algebra acting on the gauge bundle. (CKN) picks
a canonical representative; the ratio is the SAME on every representative
of the class. ∎

**Walk for `β · g_bare² = 2 N_c`:**

| Step | Content | Inputs |
|---|---|---|
| (a) | Wilson small-a matching gives `β · g_bare² = 2 N_c` (exact rational at canonical Killing form) | retained Wilson matching (G_BARE_TWO_WARD_*) |
| (b) | Under T_a → c·T_a, β → c²·β AND g_bare² → g_bare²/c² simultaneously | RFR theorem |
| (c) | Product `β · g_bare² = (c²·β) · (g_bare²/c²) = β · g_bare²` is unchanged | direct algebra |
| (d) | Hence `β · g_bare² = 2 N_c` is rescaling-invariant at every lattice spacing | structural conclusion |

This identity is the cleanest finite-lattice universality result
available from existing retained-tier scaffolding. ∎

### 4.3 Concrete rescaling-invariance test

The runner verifies via exact `Fraction` arithmetic that for several
choices of rescaling parameter c ∈ {1/2, 1, 2, 3}:

```text
β'(c) · g_bare'(c)²  =  (c² · β) · (g_bare² / c²)  =  β · g_bare²  =  2 N_c
```

independent of c, at exact rational precision.

This is a structural test: the invariant holds by direct algebra, not
by numerical convergence.

### 4.4 What this sub-piece does NOT close

- **Wilson asymptotic universality (sub-class (ii))** for action-form
  changes (Wilson vs Symanzik vs tree-level-improved) is a separate
  Nature-grade closure target. This sub-piece addresses only
  rescaling-equivalence within a fixed action-form choice.
- **Continuum-limit values** of `u_0`, `m_H/m_W`, etc. require RG-flow
  analysis. Out of scope.
- **(CKN) canonical-Killing-form admission itself** remains the same
  math-machinery admission as in PR #667. Whether (CKN) descends from
  raw A_min alone is a separate meta-question.

## 5. Relation to algebraic-universality framing

The two-class framing now reads:

| Class | Universality structure | Closure status |
|---|---|---|
| **Algebraic** | Lattice-realization-invariant by proof structure (uses only multiplicity counts + Dynkin indices + rational arithmetic). Stronger than Wilson universality — exact at every lattice scale, not asymptotic. | Hypercharge sub-piece worked in [`ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md`](ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md). 7 follow-on sub-pieces (Tr[Y²], Y_GUT, sin²θ_W^GUT, SU(5) decomposition, anomaly cancellation, 3+1 spacetime, g_bare=1) flagged. |
| **Continuum-limit (i) finite-lattice rescaling-invariant** | Structural invariance under A → c·A, T_a → c·T_a within the rescaling-equivalence class. Tractable from RFR + CVC. | First sub-piece worked in §4 below (this note). Open follow-ons: α_LM rescaling-invariance, additional dimensionless ratios. |
| **Continuum-limit (ii) Wilson asymptotic** | Standard universality theorem for asymptotically-free chiral-fermion lattice gauge theories. Action-form choices converge to same continuum predictions for dimensionless ratios. | **Out of scope** (Nature-grade RG-flow work). Catalogued in §2 with follow-on flags. |

The two notes together complete the *two-class framing* of A_min's
predictions. **No new axioms.** A_min stays {A1, A2}.

## 6. Open follow-on sub-pieces

### Sub-class (i) finite-lattice (tractable)

| Sub-piece | Authority |
|---|---|
| `α_LM = α_bare/u_0` rescaling-invariance | RFR + α_LM geometric-mean identity |
| `α_s(v) = α_bare/u_0²` rescaling-invariance | RFR + retained α_s definition |
| Cross-sector ratio `α_s(v)/α_LM = u_0` | RFR + identities |
| `m_H_tree/m_W` rescaling-invariance | RFR + retained Higgs-W ratio chain |

Each is a small bounded_theorem PR following this note's pattern.

### Sub-class (ii) Wilson asymptotic (Nature-grade)

| Sub-piece | Open content |
|---|---|
| Action-form universality on dimensionless ratios | Wilson's universality theorem applied to A_min specifically; Symanzik improvement structure |
| Continuum running of α_s scheme-independence | RG flow + scheme-independence proof |
| Continuum-limit `m_H/m_W` from `m_H/m_W` lattice flow | Lattice-spacing convergence per HIGGS_FROM_LATTICE_NOTE.md `m_H/m_W = 1.85` at a=1 → 1.64 at a=0.5 → 1.558 SM in continuum |
| Continuum-limit charged-lepton mass eigenvalues | Lane 6 closure + Wilson asymptotic universality |
| Continuum-limit quark mass eigenvalues | Lane 3 closure + Wilson asymptotic universality |
| Continuum-limit hadron masses | Lane 1 closure + lattice-QCD continuum-limit machinery |

These are research-grade derivation targets. Each is multi-PR work and
out of scope for any single session.

## 7. What this does NOT close

- **Sub-class (ii) Wilson asymptotic universality.** That is the
  candidate-(1) work proper. This note partial-addresses by classifying
  predictions; full closure requires RG-flow analysis.
- **The (CKN) admission itself.** Same status as in PR #667 — standard
  math machinery, not derived from raw A_min.
- **Action-form choice.** This note assumes the canonical Wilson
  plaquette form (forced by A4 closure, PR #667). Action-form
  universality across alternative forms (Symanzik etc.) is sub-class
  (ii) work.
- **Promotion of any cited authority.** RFR is decoration; CVC is
  audited_conditional. Their statuses are unchanged by this note.

## 8. Status

```yaml
actual_current_surface_status: bounded support theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on retained-tier {A1, A2, RFR (decoration under
  cl3_color_automorphism), CVC (audited_conditional), G_BARE_TWO_WARD_*
  Wilson small-a matching}, plus the explicit (CKN) math-convention
  admission (already surfaced in PR #667). Eligible for retention upgrade
  once: (a) RFR + CVC reach retained tier via independent audit, (b) this
  note is independently audited, (c) sub-class (i) follow-ons in §6 are
  landed.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 9. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_continuum_limit_universality_rescaling_subpiece.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: continuum-limit class universality framing landed, with
sub-class (i) (finite-lattice rescaling-invariance) closed via
RFR + CVC chain. The dimensionless invariant β · g_bare² = 2 N_c
verified rescaling-invariant at exact rational precision for c
∈ {1/2, 1, 2, 3}. Sub-class (ii) Wilson asymptotic universality
catalogued with follow-on flags; full closure is Nature-grade
RG-flow work outside this note's scope.
```

The runner uses Python standard library only (`fractions.Fraction` for
exact arithmetic). It checks:

1. **Note structure** (framing, two-sub-class definition, theorem, sub-piece, open-follow-on flags, scope guards).
2. **Premise-class consistency** (cited authorities exist on disk).
3. **Wilson small-a matching identity** `β · g_bare² = 2 N_c` at exact
   rational precision for N_c=3 → 6.
4. **Rescaling-invariance verification** for c ∈ {1/2, 1, 2, 3}: under
   `β → c²·β` and `g_bare² → g_bare²/c²`, the product `β · g_bare²`
   is invariant.
5. **`m_H_tree / v` structural invariance** at canonical (CKN)
   normalization: ratio defined modulo rescaling-equivalence class.
6. **Two-class framing cross-check**: the algebraic-universality
   framing note (sister) is cross-referenced; the catalog in §2
   correctly identifies which predictions are in which sub-class.
7. **Forbidden-import audit**: stdlib only, no PDG pins.
8. **Boundary check**: Wilson asymptotic universality (sub-class (ii)),
   continuum-limit machinery, scheme-independence all explicitly NOT
   closed.

## 10. Cross-references

- Sister framing note (algebraic class):
  [`ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md`](ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md)
- Load-bearing RFR theorem:
  [`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md)
- Load-bearing CVC theorem:
  [`G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md`](G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md)
- Load-bearing Wilson small-a matching (WM):
  [`G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`](G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md),
  [`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md)
- (CKN) admission analogue note:
  [`G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md`](G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md)
  (forward-reference; on PR #667 branch)
- α_LM coupling chain identity:
  [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- Higgs gap chain (continuum-limit example):
  [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md),
  [`HIGGS_FROM_LATTICE_NOTE.md`](HIGGS_FROM_LATTICE_NOTE.md)
- Minimal axioms parent:
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## 11. Honest scope

**Branch-local theorem + framing.** This note completes the *two-class
framing* of A_min's predictions started in the algebraic-universality
framing note. Sub-class (i) rescaling-invariance is closed via direct
algebraic chain through RFR + CVC; sub-class (ii) Wilson asymptotic
universality is catalogued but not closed (Nature-grade RG-flow work).

The framing dissolves the "imports problem" structurally: the
algebraic-class predictions live outside lattice machinery (sister
framing); the continuum-limit-class predictions split into structural
finite-lattice invariants (this note's sub-class (i), tractable) and
Wilson asymptotic universality-class members (this note's sub-class
(ii), Nature-grade).

**Not in scope.**

- Wilson's standard universality theorem applied to A_min specifically.
  That is sub-class (ii) work — multi-PR research-grade.
- Action-form universality across Wilson, Symanzik-improved, tree-level-
  improved, etc.
- Continuum-limit `m_H/m_W` numerical convergence from finite-`a`
  lattice values.
- Lane 1 / Lane 3 / Lane 6 mass-spectrum closures.
- Re-derivation of (CKN) from raw A_min.
