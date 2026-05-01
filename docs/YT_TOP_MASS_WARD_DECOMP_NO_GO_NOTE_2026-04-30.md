# Top-Sector Ward-Decomposition Pass: Exact No-Go for Audit-Clean Yukawa Pin

**Date:** 2026-04-30  
**Status:** no-go / exact-negative-boundary — Ward-decomposition second pass,
  four authorized routes exhausted; exact audit-clean obstruction identified  
**Claim boundary authority:** this note  
**Loop slug:** yt-top-mass-substrate-pin-ward-clean-20260430  
**Import ledger:** `YT_TOP_MASS_WARD_DECOMP_ASSUMPTIONS_AND_IMPORTS_2026-04-30.md`  
**Runner:** `scripts/frontier_yt_top_mass_ward_decomp_no_go.py` (PASS=24 FAIL=0)  
**Delivery surface:** PR #230 (`claude/yt-direct-lattice-correlator-2026-04-30`)  
**Prior no-go artifact:** `YT_TOP_MASS_SUBSTRATE_PIN_NO_GO_NOTE_2026-04-30.md`  
**Prior Ward note (audited_renaming):** `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`

---

## 0. Purpose and Prior-Art Boundary

The first campaign pass executed a five-frame fan-out (spectral, topological,
taste, algebraic, anomaly) and reached a uniform exact-negative-boundary.  The
handoff named one surviving route:

> **Ward-decomposition / same-1PI-function route.**  
> The Ward note derives `y_t_bare = g_bare/sqrt(2 N_c) = 1/sqrt(6)` but was
> classified `audited_renaming` because Rep B (eq. 3.7) **defines** `y_t_bare`
> via the H_unit-to-top matrix element `⟨0|H_unit(0)|t̄t⟩`.

This pass attempts to make the Ward route audit-clean by attacking it through
four field-theoretic routes that the user explicitly authorized:

| Route | Description |
|---|---|
| W-I | Actual Ward-Takahashi identities (gauge, chiral, BRST/ST) |
| W-II | Hubbard-Stratonovich auxiliary-field rewrite of the OGE amplitude |
| W-III | Source-functional / 1PI residue definition of y_t_bare |
| W-IV | Fierz/OGE algebra alone (D12+S2+D16) without any matrix-element step |

**Forbiddance set for this pass (identical to prior campaign):**

- H_unit-to-top matrix element as **definition** of y_t_bare (eq. 3.7)
- Any matrix-element definition `⟨0|op|state⟩` for y_t_bare
- Observed m_t or y_t values
- alpha_LM / plaquette / tadpole normalization
- Fitted selectors

**Success condition:** physical-observable or action-level pin — not a
relabeling of g_bare under a new name.  
**Failure condition:** narrow audit-clean no-go identifying the exact load-
bearing obstruction in each authorized route.

---

## 1. Substrate Inputs Available (Permitted Set)

Same permitted set as the five-frame pass:

| Input | Class |
|---|---|
| `g_bare = 1` (axiom at canonical surface) | axiom |
| `N_c = 3`, `N_iso = 2`, `N_gen = 3` | exact retained counts |
| D9: Cl(3)×Z³ bare action = Wilson plaquette + staggered Dirac, NO independent Yukawa term | exact retained |
| D12: exact SU(N_c) color-singlet Fierz identity | exact structural |
| S2: Lorentz-Clifford scalar projection \|c_S\| = 1 | exact structural |
| D16: tree-level Feynman-rule completeness of bare action (OGE only at O(α_LM)) | exact retained |
| D17: unique unit-normalized scalar-singlet composite on Q_L is H_unit | exact retained (for consistency check only, NOT as Yukawa definition) |
| SM gauge group `SU(3)×SU(2)_L×U(1)_Y` derived from Cl(3)/Z³ | exact retained |
| Standard WTI/PCAC relations of QFT | standard QFT (textbook identities) |

---

## 2. Route W-I — Actual Ward-Takahashi Identities

### 2.1 Scope of QFT Ward Identities

Ward-Takahashi identities (WTI) arise from local symmetry transformations of
the path integral.  For a theory with gauge group G, the WTI relates vertex
functions and propagators.

**2.1.1 QCD gauge WTI (color current).** Under an infinitesimal SU(3) gauge
transformation `δA^a_μ = D_μ ε^a`, `δψ = ig T^a ε^a ψ`, the Ward identity
for the quark-gluon 3-point function is:

```
q^μ Γ^μ_a(q; p, p') = S^{-1}(p) T^a - T^a S^{-1}(p')         (WTI-1)
```

where `q = p - p'` is the gluon momentum, `S(p)` is the full quark propagator,
and `Γ^μ_a` is the 1PI quark-gluon vertex.  At zero gluon momentum:

```
Γ^μ_a(0; p, p) = -∂S^{-1}(p)/∂p^μ · T^a                      (WTI-2)
```

**Content:** WTI-1/2 constrains the **gauge vertex** (gluon-quark-quark
coupling) in terms of the quark propagator derivative.  It ensures the gauge
coupling `g_bare` is multiplicatively renormalized in the same way as the
propagator residue.  It says nothing about the Yukawa coupling.

**2.1.2 Chiral Ward identity / PCAC.** For a flavor-diagonal axial current
`J^5_μ = ψ̄ γ_μ γ_5 ψ` of the top quark at finite mass:

```
∂^μ J^5_μ = 2 m_t · iψ̄ γ_5 ψ  ≡  2 m_t P                    (WTI-3)
```

The divergence of the axial current equals `2 m_t` times the pseudoscalar
density.  This is the PCAC relation.  **Content:** m_t appears as an INPUT
parameter in the PCAC equation, not as a derived quantity.  The PCAC relation
is satisfied for any value of m_t; it does not select a specific value.

**2.1.3 Slavnov-Taylor identities (BRST/STI).** In a gauge-fixed theory, BRST
symmetry generates Slavnov-Taylor identities relating propagators and vertex
functions.  For QCD:

```
k^μ Γ_{A^a_μ ψ ψ̄}(k; p, q) = f^{abc} [Γ_{c^b ψ ψ̄} S^{-1}_{ψ}(p)
                                          - S^{-1}_{ψ}(q) Γ_{c^a ψ ψ̄}]    (STI-1)
```

These are gauge-sector identities involving the ghost-fermion vertex.  They
constrain the gauge sector (quark-gluon vertex, ghost-fermion coupling) but do
NOT constrain the Yukawa sector.  The Yukawa coupling is a gauge singlet; the
STI does not act on it.

### 2.2 Summary for Route W-I

The standard WTI/PCAC/STI machinery of QFT constrains:
- The **gauge vertex** in terms of the quark propagator (WTI-1/2)
- The **axial-current divergence** as 2m times the pseudoscalar density (PCAC)
- The **gauge-sector vertex relations** via BRST/ghost couplings (STI)

None produces a constraint of the form `y_t_bare = f(g_bare)`.  The reason
is structural: the gauge symmetry acts on the gauge sector, not on Yukawa
couplings.  Yukawa couplings transform as singlets under G; there is no
Ward identity associated with a Yukawa coupling because there is no
corresponding symmetry current.

**WTI obstruction:** No Ward-Takahashi identity of QFT (gauge, chiral, BRST)
constrains the Yukawa coupling of a scalar field to a fermion pair.  The PCAC
identity contains the fermion mass as an INPUT, not as a derived output.  A
WTI that would constrain y_t would require a symmetry that mixes the gauge and
Yukawa sectors — no such symmetry exists in the retained SM gauge group.

---

## 3. Route W-II — Hubbard-Stratonovich Auxiliary-Field Rewrite

### 3.1 Setup

The D12+S2+D16 result gives the OGE-generated 4-fermion amplitude in the
scalar singlet channel at tree level:

```
Γ^(4)_S(q²) = -G_eff O_S / q²
with G_eff = g_bare² / (2 N_c) = 1/6  (at g_bare = 1)         (HS-1)
```

where `O_S = (ψ̄ψ)_{(1,1)} (ψ̄ψ)_{(1,1)}` is the color-singlet, iso-singlet,
Dirac-scalar four-fermion operator.

The Hubbard-Stratonovich (HS) transform introduces an auxiliary bosonic field σ
to linearize the 4-fermion interaction:

```
exp(G_eff ∫d⁴x (ψ̄ψ)²) 
   = ∫Dσ exp(-∫d⁴x [σ²/(4G_eff) - y_σ σ ψ̄ψ])               (HS-2)
```

with the matching condition `y_σ² = G_eff`, giving:

```
y_σ = √G_eff = g_bare / √(2 N_c) = 1/√6                       (HS-3)
```

The coupling `y_σ` of σ to the fermion bilinear is determined by (HS-3).

### 3.2 Is y_σ a substrate-native pin for y_t_bare?

The HS transform gives a numerical value `y_σ = 1/√6`.  The question is
whether `y_σ` constitutes an audit-clean substrate pin for `y_t_bare` that is
independent of the H_unit definition.

**Step 1: What is σ in the composite framework?**

The HS field σ is a formal auxiliary field introduced to linearize the
OGE-induced 4-fermion interaction in the scalar-singlet channel on Q_L.  By
the composite-Higgs structural fact D9, the Cl(3)×Z³ framework has exactly one
composite scalar-singlet degree of freedom on the Q_L block: the composite
taste condensate `phi = (1/N_c) ψ̄_a ψ_a`.

The HS field σ in the scalar singlet channel on Q_L is therefore the
PROPAGATING VERSION of this composite condensate.  It is not an independent
field — it is the composite Higgs H_unit under a formal auxiliary-field
representation.

**Step 2: The identification σ ↔ H_unit is unavoidable.**

The HS partition function (HS-2) integrates out the auxiliary field σ to
recover the original 4-fermion theory.  For the HS transform to describe the
physics of the Cl(3)×Z³ substrate rather than a free-field approximation, σ
must be identified with the physical composite scalar degree of freedom on Q_L.
By D17, that unique composite is H_unit.

Claim: `σ = H_unit` (up to canonical normalization).

Proof: D17 establishes that H_unit = (1/√6)(ψ̄ψ)_{(1,1)} is the UNIQUE
unit-normalized scalar-singlet composite on Q_L with `Z² = N_c · N_iso = 6`.
The HS field σ is introduced to linearize the `(ψ̄ψ)_{(1,1)}²` interaction.
By the LSZ theorem, the physical pole in σ's propagator corresponds to the
lightest scalar-singlet composite state on Q_L.  D17 proves that state is
H_unit.  Therefore σ = H_unit.

**Step 3: The HS definition of y_σ is the H_unit identification in disguise.**

The coupling `y_σ` in the HS Lagrangian `y_σ σ ψ̄ψ` is the coupling of H_unit
to the fermion bilinear (up to the canonical normalization factor Z = √6).
Specifically:

```
y_σ σ ψ̄ψ = y_σ · H_unit · (ψ̄ψ)_{(1,1)} · Z
          = y_t_bare H_unit (ψ̄ψ)_{(1,1)} · Z                  (HS-4)
```

where the factor Z = √6 is the canonical normalization of H_unit from D17.

This is exactly the H_unit-to-top Yukawa vertex that the original Ward note
used in Rep B.  The HS route has reproduced the forbidden identification under
the name "y_σ" instead of "y_t_bare."

### 3.3 Obstruction for Route W-II

**HS exact obstruction:** The HS auxiliary field σ in the Q_L scalar-singlet
channel of the Cl(3)×Z³ framework is algebraically equivalent to H_unit (D17).
Therefore, defining `y_t_bare := y_σ` (the HS coupling) is a renaming of the
H_unit-to-top matrix-element identification.  The audited_renaming classification
of the prior Ward route applies equally to the HS route.

The numerical value `y_σ = 1/√6` is correct and substrate-native, but it
arrives via an identification `σ ≡ H_unit` that is the same step the auditors
flagged.  The HS route does not resolve the audit-clean obstruction.

---

## 4. Route W-III — Source-Functional / 1PI Residue Definition

### 4.1 Definition attempt

Define y_t_bare via the 1PI effective action.  Add a scalar-channel source J
to the bare action:

```
L_J = J(x) · (ψ̄ψ)_{(1,1)}(x)                                 (SF-1)
```

The partition function Z[J] = ∫DψDψ̄DA exp(-(S + ∫J(ψ̄ψ)_{(1,1)})) generates
connected correlators W[J] = log Z[J].  The scalar field expectation value is:

```
φ(x) = δW/δJ(x) = ⟨(ψ̄ψ)_{(1,1)}(x)⟩_J                      (SF-2)
```

The 1PI effective action Γ[φ] = -W[J] + ∫J φ has vertices:

```
Γ^{(n)}(x_1,...,x_n) = δⁿΓ/δφ(x_1)...δφ(x_n)                (SF-3)
```

The physical scalar mass is defined by the pole of Γ^{(2)}.  The Yukawa
coupling can be defined as:

```
y_t_bare_eff := Γ^{(1,1,1)}(0; p, -p) = δ³Γ/δφ δt̄ δt |_{φ=⟨φ⟩}  (SF-4)
```

where the derivative is with respect to the source J (scalar channel) and the
external top-quark legs.

### 4.2 Evaluation at tree level

At tree level in the OGE approximation, the connected 3-point function
`W^{(1,1,1)}` for one scalar-source insertion and two external fermion legs is:

```
W^{(1,1,1)}(q; p, p') = G_F(p) · [coupling vertex] · G_F(p')
                       = S(p) · y_eff · S(p')                  (SF-5)
```

where `y_eff` is the effective coupling.  Amputating and projecting onto 1PI:

```
Γ^{(1,1,1)}(0; p, -p) = y_eff = √G_eff = 1/√6                (SF-6)
```

The source-functional definition gives the same numerical value.

### 4.3 Is this definition independent of H_unit?

The source J couples to the operator `(ψ̄ψ)_{(1,1)}` — the unnormalized
scalar-singlet fermion bilinear on Q_L.  The normalized version of this
operator is exactly H_unit (D17, with Z = √6).  Therefore:

```
J · (ψ̄ψ)_{(1,1)} = J · √6 · H_unit                           (SF-7)
```

The source-functional definition uses `(ψ̄ψ)_{(1,1)}` as the source.  But
`(ψ̄ψ)_{(1,1)}` normalized is H_unit.  The 1PI residue y_t_bare_eff is the
coupling of the normalized composite to the top quark — which is precisely the
H_unit matrix element `⟨0|H_unit|t̄t⟩ = 1/√6`.

**The canonical normalization Z = √6 (which determines whether y_eff = 1/√6
comes from the source-functional route) is itself derived from D17 (uniqueness
of the scalar singlet on Q_L with Z² = N_c · N_iso = 6).**  Removing D17
from the calculation leaves y_eff with an undetermined normalization factor Z:

```
y_eff = √G_eff / Z  (with Z undetermined without D17)           (SF-8)
```

So the source-functional definition gives a canonical result only IF the
normalization Z is pinned by D17 — and D17 is the same ingredient that defines
H_unit as the unique composite operator.

### 4.4 Obstruction for Route W-III

**Source-functional exact obstruction:** The 1PI residue `Γ^{(1,1,1)}` defines
y_t_bare as the coupling of the normalized scalar-singlet composite operator
to the top quark.  The normalization of this operator is Z = √6, which is
determined by D17 (the uniqueness theorem for H_unit on Q_L).  Therefore:

1. Without D17, the source-functional definition gives y_eff = √G_eff / Z with
   Z undetermined — no pin.
2. With D17, the canonical normalization gives y_eff = 1/√6, but this is
   algebraically equivalent to using the H_unit matrix element `⟨0|H_unit|t̄t⟩`.

The source-functional route cannot produce an audit-clean pin because it either
lacks a canonical normalization (no pin) or uses D17 as the normalization
source (equivalent to H_unit).

---

## 5. Route W-IV — Fierz/OGE Algebra Alone (D12+S2+D16), No Matrix-Element Step

### 5.1 What the OGE algebra gives

D12 + S2 + D16 together give the exact tree-level result:

```
Γ^(4)_S(q²) = -g_bare² / (2 N_c q²) O_S                       (OGE-1)
```

This is a **four-fermion amplitude** — the 1PI 4-point function in the scalar-
singlet channel, projected onto `O_S = (ψ̄ψ)_{(1,1)}²`.

The question: can (OGE-1) itself be called "the Yukawa coupling = 1/√6"
without any matrix-element or auxiliary-field step?

### 5.2 What a Yukawa coupling IS

A Yukawa coupling is defined as the coefficient in a three-point interaction:

```
L_Y = y φ ψ̄ ψ  (Yukawa Lagrangian term)                        (YK-1)
```

where φ is a scalar field, ψ is a Dirac fermion.  The Yukawa coupling y is a
dimensionless parameter that multiplies a **three-field interaction vertex**.
It is the coefficient of the 1PI 3-point function with one scalar and two
fermion external legs:

```
y = Γ^{(1,2)}_{φ ψ̄ ψ}(q=0; p, -p)                            (YK-2)
```

The OGE amplitude (OGE-1) is a **four-fermion** 1PI function
`Γ^{(4)}_{ψ̄ψ ψ̄ψ}`.  It has a different field content from a Yukawa coupling:
four external fermionic legs vs. two fermionic + one scalar.

### 5.3 The factorization step requires a scalar field

To extract y_t_bare from the OGE amplitude (OGE-1), one must factorize the
4-fermion amplitude into a product of two Yukawa vertices:

```
Γ^(4)_S(q²) = -y_t_bare² / q² O_S                             (OGE-2)
```

This factorization is valid ONLY if the amplitude (OGE-1) arises from the
exchange of a single propagating scalar with mass ≈ 0 (at scales q² >> m²_scalar)
and Yukawa coupling y_t_bare on each side.

For the factorization (OGE-2) to hold:
1. There must exist a scalar field φ with propagator 1/q² (at high q²).
2. φ must couple to `(ψ̄ψ)_{(1,1)}` with coupling y_t_bare.
3. The propagator and coupling must account for the FULL amplitude (OGE-1).

Condition (1) requires identifying the scalar field φ.  In the composite
framework, the only scalar-singlet field on Q_L is H_unit (D17).  Conditions
(2)-(3) are then the H_unit matrix-element step.

### 5.4 The dimensional mismatch argument

An alternative way to see the obstruction:

- `Γ^(4)` has dimension [mass]^{4-d·4} = [mass]^{-4} in d=4 with canonical scaling.
  At tree level it is `g² / q²` → dimensionless at high q² for the coefficient.
- A Yukawa coupling y is dimensionless.
- The ratio `y² = G_eff = g² / (2 N_c)` is derived by equating the 4-fermion
  coefficient to y²; this equating step implicitly introduces the scalar
  propagator `1/q²` and asserts that the scalar is the carrier.

The carrier identification — declaring that a `1/q²` pole in the 4-fermion
amplitude arises from a scalar exchange — requires naming the scalar.  On the
Q_L block, the scalar is H_unit (D17).  Without D17 or equivalent, the 4-fermion
amplitude has no canonical factorization into a scalar-exchange diagram.

### 5.5 Obstruction for Route W-IV

**OGE-algebra exact obstruction:** The OGE amplitude (OGE-1) from D12+S2+D16 is
a four-fermion 1PI function.  Calling its coefficient `g²/(2N_c)` a "Yukawa
coupling squared" requires factorizing the 4-fermion function into
`-y² / q² · O_S`.  This factorization:

1. Requires introducing a scalar propagator `1/q²` in the scalar channel.
2. Requires identifying the scalar field that carries this propagator.
3. In the Cl(3)/Z³ framework, the only scalar singlet on Q_L is H_unit (D17).

Without step (3), the coefficient `g²/(2N_c)` is a dimensionless 4-fermion
coupling constant — not a Yukawa coupling.  With step (3), the factorization
is the H_unit identification, which is forbidden.

---

## 6. Synthesis: The Exact Audit-Clean Obstruction

### 6.1 Agreement across four routes

All four authorized routes reach the same structural obstruction:

| Route | Attempt | Obstruction |
|---|---|---|
| W-I: actual WTI | WTI constrains gauge vertex, not Yukawa | No WTI acts on Yukawa sector; PCAC uses m_t as input |
| W-II: HS rewrite | HS field σ gives y_σ = 1/√6 | σ ≡ H_unit by D17; HS is H_unit identification in disguise |
| W-III: source-functional | Γ^{(1,2)} residue = 1/√6 | Canonical normalization Z = √6 requires D17 ↔ H_unit |
| W-IV: Fierz/OGE alone | Coefficient g²/(2N_c) from D12+S2+D16 | 4-fermion amplitude ≠ Yukawa coupling without scalar-field identification |

### 6.2 The narrow Ward-clean no-go statement

**The prior Ward route (YT_WARD_IDENTITY_DERIVATION_THEOREM.md) cannot be
made audit-clean without H_unit or an equivalent definition because:**

1. **The bare Cl(3)×Z³ action has NO Yukawa term** (D9).  There is no bare
   parameter `y_t_bare` in the Lagrangian; it is an emergent observable.

2. **Γ^(4)_S from D12+S2+D16 is a four-fermion amplitude, not a Yukawa
   coupling.**  A Yukawa coupling is a 3-point function coefficient
   (φψ̄ψ vertex), not a 4-point function coefficient (ψ̄ψψ̄ψ amplitude).

3. **Any conversion of Γ^(4) to a Yukawa coupling requires identifying a
   scalar field.**  That identification requires either:
   - H_unit (D17) — explicitly forbidden
   - HS auxiliary σ ≡ H_unit — equivalent to forbidden
   - Source-functional scalar normalized by D17 — equivalent to forbidden

4. **The actual Ward-Takahashi identities of QFT (W-I) do not constrain
   Yukawa couplings.**  They constrain gauge vertices.  No Ward identity
   enforces `y_t = f(g)` from a symmetry principle.

5. **The "Ward route" in the framework is not a Ward-Takahashi identity.**
   It is a same-1PI-function consistency check: two representations of
   `Γ^(4)_S` (Rep A via OGE, Rep B via H_unit) agree numerically.  This
   consistency checks D17's scalar-uniqueness but does not derive a Yukawa
   coupling independently of H_unit.

### 6.3 What the Ward note actually proves (audit-clean reading)

Reading the Ward note under the forbiddance set gives the following:

- **Rep A** (OGE via D12+S2+D16): proves exactly that `Γ^(4)_S = -g²/(2N_c q²)`.
  This is a fact about the SU(N_c) gauge dynamics on the Q_L block.
  **Status:** exact retained, no H_unit required.

- **Rep B** (H_unit matrix element): DEFINES y_t_bare as `⟨0|H_unit(0)|t̄t⟩ = 1/√6`.
  Then computes `Γ^(4)_B = -y_t_bare²/q² = -1/(6q²)`.
  **Status:** forbidden as a definition under the current forbiddance set.

- **Consistency check** (Rep A = Rep B): confirms that IF y_t_bare is defined
  by H_unit (Rep B), its value is numerically consistent with the OGE amplitude
  (Rep A).  This is a non-trivial structural consistency but is NOT a derivation
  of y_t_bare that is independent of H_unit.

The audit-clean consequence of the Ward note is:

> **Rep A alone:** `g_bare² / (2 N_c) = 1/6` is the coefficient of `O_S` in
> `Γ^(4)`.  This is a retained fact.

> **Without Rep B:** The coefficient `1/6` is a four-fermion coupling constant.
> It is NOT y_t_bare until a scalar field is named and D17 provides the
> normalization.  Calling it y_t_bare² is a naming step, not a derivation.

### 6.4 Diagram of the exact obstruction

```
D9  →  No bare Yukawa parameter in action
D12 + S2 + D16  →  Γ^(4)_S = -g²/(2N_c q²) O_S   [four-fermion amplitude]
                       ↓
       To extract y_t_bare, need: Γ^(4) = -y²/q² O_S
                       ↓
       Factorization requires: scalar propagator 1/q² + scalar-fermion coupling y
                       ↓
       Scalar identification requires: naming the scalar φ on Q_L
                       ↓
       D17: unique scalar singlet on Q_L is H_unit
                       ↓
       H_unit identification = audited_renaming obstruction
```

This diagram has no bypass.  Every authorized alternative route (W-I, W-II,
W-III, W-IV) reaches the same node: **"naming the scalar φ on Q_L = H_unit."**

---

## 7. Claim Status

```yaml
actual_current_surface_status: no-go / exact-negative-boundary
conditional_surface_status: null
hypothetical_axiom_status: >
  conditional on: permitting D17 as definition source (not only as consistency
  check), the Ward route gives exact y_t_bare = 1/sqrt(6). This is not permitted
  under the current forbiddance set.
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: >
  No positive substrate pin found. This is a no-go artifact.
audit_required_before_effective_retained: false
bare_retained_allowed: false
```

---

## 8. Implications for PR #230

The Ward-decomposition pass resolves the surviving route from the prior handoff.
All authorized field-theoretic routes (W-I through W-IV) have been exhausted.
The narrow audit-clean no-go is:

> **The prior Ward route cannot be made audit-clean without H_unit or an
> equivalent definition.  The Cl(3)/Z³ bare action has no Yukawa term (D9);
> D12+S2+D16 give a four-fermion amplitude, not a Yukawa coupling; converting
> the four-fermion amplitude to a Yukawa coupling requires identifying the
> scalar field, which is H_unit by D17.**

This completes the two-pass structured search for a non-MC top-sector substrate
pin.  The honest status of PR #230 is confirmed:

1. **Calibrated physical-observable readout**: The direct staggered-correlator
   lane measures `m_t → y_t` from the ensemble.  Derivational status requires
   either (a) the Ward route with H_unit permitted as a proof input, or (b) a
   new dynamical substrate premise outside the current framework.

2. **The Ward/H_unit route is separately auditable**: If the campaign decision
   is made to permit the Ward route (i.e., to accept D17's H_unit as a
   definition source rather than only a consistency check), then `y_t_bare =
   1/√6` is a substrate-native exact result.  The `audited_renaming` failure
   arose from the *presentation* (defining y_t_bare by matrix element, then
   checking consistency), not from any error in the algebra.  A re-audit
   focusing on whether D17 constitutes a definition source or a consistency
   check would resolve this.

---

## 9. Runner Check Map

The paired runner `scripts/frontier_yt_top_mass_ward_decomp_no_go.py` verifies:

1. **W-I route:** QCD WTI (WTI-1) constrains gauge vertex, not Yukawa vertex —
   verified by checking that WTI acts on the wrong field channel (PASS ×6)
2. **W-II route:** HS coupling y_σ = √G_eff = 1/√6 confirmed numerically —
   confirmed that σ ≡ H_unit via D17 (canonical normalization Z = √6 required)
   (PASS ×5)
3. **W-III route:** Source-functional 1PI residue = 1/√6 confirmed — confirmed
   that normalization requires D17 (without D17, result is undetermined) (PASS ×5)
4. **W-IV route:** OGE amplitude coefficient = 1/6 confirmed — confirmed that
   factorization to y² requires scalar-field identification (PASS ×4)
5. **Obstruction synthesis:** Diagram of the single load-bearing node
   (D17 = scalar identification required) verified across all four routes
   (PASS ×4)

Expected: `PASS = 24, FAIL = 0`

---

## 10. Cross-References

- Prior five-frame no-go: `YT_TOP_MASS_SUBSTRATE_PIN_NO_GO_NOTE_2026-04-30.md`
- Prior Ward note (audited_renaming): `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
- Scalar-uniqueness theorem (D17): `YT_WARD_IDENTITY_DERIVATION_THEOREM.md` §3.2
- Same-1PI pinning theorem: `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`
- Rep B independence theorem: `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`
- Lepton-sector failure (for context): `CHARGED_LEPTON_Y_TAU_WARD_IDENTITY_SU2_ANCHOR_STRETCH_ATTEMPT_NOTE_2026-04-28.md`
- Assumptions and imports: `YT_TOP_MASS_WARD_DECOMP_ASSUMPTIONS_AND_IMPORTS_2026-04-30.md`
- Claim status certificate: `.claude/science/physics-loops/yt-top-mass-substrate-pin-ward-clean-20260430/CLAIM_STATUS_CERTIFICATE.md`
- Handoff note: `YT_TOP_MASS_WARD_DECOMP_HANDOFF_2026-04-30.md`
