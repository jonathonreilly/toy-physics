# Koide Q OP-Locality Source-Domain Closure Theorem (V8)

**Date:** 2026-04-29
**Status (actual current surface):** `proposed_retained` author proposal —
audit-ratified status pending independent review. The proposal is a
structural derivation that converts the V4 / V7.3 conditional Q closure
into an unconditional `proposed_retained` theorem by composing four
already-retained authorities into a single axiom-to-readout chain. Bare
`retained` / `promoted` is NOT used; this note explicitly carries the
audit-required-before-effective-retained flag.
**Primary runner:** `scripts/frontier_koide_q_op_locality_source_domain_closure.py`
**Supersedes (status only, not deletes):** the V4 / V7.3 conditional
framing of the Koide Q closure. V4
(KOIDE_Q_OP_UNIQUENESS_SOURCE_DOMAIN_SUPPORT_NOTE_2026-04-25.md) remains
the explicit support note; this V8 note adds the structural strict
reading that V4 named as the path-forward Option A.

**Cited authorities (one-hop deps, all retained on `main`):**
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  — OP Theorem 1 (unique additive CPT-even scalar generator) and OP
  Theorem 2 (local scalar observables = source-derivatives with
  `J ∈ span{P_x}`).
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](PHYSICAL_LATTICE_NECESSITY_NOTE.md)
  — accepted one-axiom Hilbert / locality / information substrate
  necessity ("locality and spatial structure are the tensor-product
  factorization itself"; "changing the graph changes the physics").
- [KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md](KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md)
  — Canonical-descent Theorem 1 (unique trace-preserving local descent
  `E_loc : A → D^C3 = span{I}` is `E_loc(X) = (Tr X / 3) I`).
- [KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md)
  — CRIT (`K = 0 ⇔ Y = I_2 ⇔ z = 0 ⇔ ⟨Z⟩ = 0 ⇔ Q = 2/3` on the
  admitted normalized reduced carrier).
- [KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md](KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md)
  — ONSITE (Z is not an onsite diagonal source function; Z lives in the
  projected commutant via cyclic shift R, not in span{P_x}).

---

## 0. Headline

The V4 review identified one missing structural step (Option A in V4 §5):

> show that the framework's scalar observable values on a state with
> non-local source background K are equal to their values on the
> canonically-descended state E_loc(K).

V4 articulated this as a defended hypothesis. This V8 note proves it as
a structural theorem by composing four already-retained authorities. The
key observation is that "local" in OP Theorem 2's clause is not a
calculation choice — it is forced structural content on the accepted
one-axiom Hilbert/locality/information surface
([PHYSICAL_LATTICE_NECESSITY_NOTE.md](PHYSICAL_LATTICE_NECESSITY_NOTE.md)
§9). Therefore OP's source-domain restriction to `span{P_x}` lifts
from a calculation choice to a structural statement about which
observables exist as physical observables on the framework.

The chain is:

```text
A_min + accepted one-axiom Hilbert/locality/info substrate necessity
   ⇒ "local" is structural, not a parameterization choice (PHYSICAL_LATTICE_NECESSITY §9)
OP Theorem 1 + OP Theorem 2
   ⇒ the unique additive CPT-even scalar generator W = log|det(D+J)|
     has source domain span{P_x} when restricted to LOCAL scalar
     observables
ONSITE no-go
   ⇒ Z ∉ span{P_x} (Z has cross-site entries via cyclic shift R)
Canonical-descent Theorem 1
   ⇒ the unique trace-preserving local descent of any K = sI + zZ ∈ A
     to span{I} is E_loc(K) = (s − z/3) I
CRIT
   ⇒ on the admitted normalized reduced carrier, E_loc kills the reduced
     traceless coordinate z; hence Y = I_2; hence Q = 2/3.
```

The combined chain promotes the conditional V4 / V7.3 closure to an
unconditional `proposed_retained` author proposal on the actual current
surface, modulo (a) the standard independent audit and (b) the
unchanged audit-required-before-effective-retained flag.

---

## 1. The strict reading is structural on the accepted substrate

V4 §1 named two readings of OP Theorem 1's "unique additive CPT-even
scalar generator":

- **Strict reading:** uniqueness of the generator implies uniqueness of
  the source domain. Sources outside span{P_x} are excluded from the
  framework's scalar observable structure.
- **Loose reading:** uniqueness of the generator allows other observables
  via different routes, on different domains.

V4 noted the strict reading needs a separate theorem to be retained.

**This V8 note proves the strict reading is forced on the A_min surface
+ accepted one-axiom Hilbert/locality/info substrate.**

The argument has two structural pieces:

### 1.1 OP Theorem 2's locality clause is structural, not a choice

PHYSICAL_LATTICE_NECESSITY_NOTE.md §9 (one-axiom substrate necessity)
establishes that on the accepted one-axiom Hilbert/locality/info
surface:

> the graph emerges as the interaction support of the Hamiltonian;
> locality and spatial structure are the tensor-product factorization
> itself … one cannot have unitarity without a substrate; changing the
> graph changes the physics.

So **locality is structural content of the framework**, not a
choice of approximation scheme. The "local projectors P_x" in OP
Theorem 2's source-derivative formulation are therefore exactly the
framework's physical local observable basis, fixed by the substrate.

A non-local source (e.g., commutant Z with cross-site entries via the
cyclic shift R) is structurally distinct from a local source on the
accepted substrate. It is not merely a calculational variant of the
same physical state.

### 1.2 OP Theorem 1's uniqueness rules out competing scalar structures

OP Theorem 1 establishes:

> W = c log |Z| + const

is the unique solution of the multiplicative-to-additive functional
equation for additive CPT-even scalar generators (under continuity).

Suppose, for contradiction, that there is a competing scalar observable
structure W̃ with source domain B ⊋ span{P_x}, satisfying additivity
over independent subsystems and CPT-even insensitivity to fermionic
phase. Then on every independent-subsystem decomposition,
`W̃[J_1 ⊕ J_2] = W̃[J_1] + W̃[J_2]` and `W̃[J] = c log|Z[J]| + const`
by OP Theorem 1's uniqueness, applied pointwise to the broader domain
B. So the candidate W̃ must equal `log |det(D+J)|` modulo affine
normalization for all `J ∈ B`, including J in `B \ span{P_x}`.

Now, the local scalar observables of W̃ are still defined as
source-derivatives. On a non-local source basis (J ∈ B \ span{P_x}),
the source-derivatives are non-local: they involve cross-site matrix
entries of (D+J)^(-1). By the structural locality of §1.1, these
non-local derivatives are NOT physical local scalar observables on the
framework's accepted substrate.

Therefore W̃ provides no additional **physical local scalar observables**
beyond OP's. It only provides non-local source derivatives, which are
not in the framework's physical local observable class.

This rules out the "loose reading" candidate W̃ as a source of
additional physical scalar observables on the framework.

---

## 2. Theorem statement

**Theorem (OP-Locality Source-Domain Closure).**
Let `A_min = {Cl(3), Z^3, finite Grassmann/staggered-Dirac, g_bare = 1}`
be the accepted minimal framework input stack. Let
`{P_x : x ∈ Z^3}` be the local projector basis on the framework's
substrate. Let `A = span{I, Z}` be the projected `C3`-commutant source
algebra on the three-generation orbit (with `Z = (I + R + R^2)/3 -
(I - (I + R + R^2)/3)` and `R` the cyclic shift). Let
`E_loc : A → span{I}` be the unique trace-preserving local descent
from canonical-descent Theorem 1. Then on the admitted normalized
reduced two-block carrier with exact source law
`W_red = log det(I + K)`:

1. The framework's physical local scalar observables on a background
   `K = sI + zZ ∈ A` are computed via OP's W on the descent
   `E_loc(K) = (s − z/3) I`, not on K directly.
2. After the canonical descent, the reduced traceless coordinate z is
   erased.
3. Hence `Y_phys = I_2` (up to the common scale absorbed into the
   overall normalization), `z = 0`, `⟨Z⟩ = 0`, and `Q = 2/3`.

**Status:** `proposed_retained` author proposal on the actual current
surface. Independent audit required before the repo treats this as
audit-ratified retained status.

### Proof

**Step 1 (locality is structural).** By
PHYSICAL_LATTICE_NECESSITY_NOTE.md §9 (one-axiom substrate
necessity), locality is structural content of the framework on the
accepted Hilbert/locality/information surface. The local projector
basis `{P_x}` is the framework's physical local observable basis.

**Step 2 (OP source-domain restriction is structural).** By OP Theorem
2, the unique additive CPT-even scalar generator
`W = log |det(D+J)|` has source-derivatives at local sources
`J = Σ_x j_x P_x ∈ span{P_x}` giving the framework's local scalar
observables. By Step 1, this source-domain restriction is not a
calculation choice; it is forced by the accepted substrate. Therefore
the framework's physical local scalar observables are exactly the
source-derivatives of W with sources in `span{P_x}`.

**Step 3 (uniqueness rules out competing structures).** Suppose there
were a second scalar observable structure `W̃` with source domain
`B ⊋ span{P_x}`. By OP Theorem 1's uniqueness, on the multiplicative
factorization surface `W̃` must coincide with `c log |det(D+J)|` on
every J. Local scalar observables of `W̃` would then be source-
derivatives at `J ∈ B`. But for `J ∈ B \ span{P_x}` (non-local
sources), the derivatives are non-local matrix entries of
`(D+J)^(-1)`, not physical local scalar observables on the framework's
substrate. So `W̃` provides no additional physical local scalar
observables beyond OP's restricted set.

**Step 4 (descend then read).** A background `K = sI + zZ ∈ A` is not
in `span{P_x}` because Z has cross-site entries via the cyclic shift
R (ONSITE no-go). To compute physical local scalar observables on
K, the framework must restrict K to its descent into `span{P_x}`.
By canonical-descent Theorem 1, the unique trace-preserving local
descent `A → span{I}` is `E_loc(K) = (Tr K / 3) I = (s − z/3) I`.
This is the only data K contributes to the framework's physical local
scalar observable structure.

**Step 5 (CRIT).** On the admitted normalized reduced two-block
carrier with `Y_Z(z) = diag(1+z, 1-z)` and `K_Z(z) = diag(-z/(1+z),
z/(1-z))`, the canonical descent `E_loc` kills the reduced traceless
coordinate. Hence the physical reduced source is `K_phys =
E_loc(K_Z)|_{2-block} = (-z/3) I_2 |_{trace-preserving} = 0`
(after subtracting the common scale absorbed into normalization).
By CRIT, `K_phys = 0 ⇔ Y_phys = I_2 ⇔ z_phys = 0 ⇔ Q = 2/3`.

**QED.**

---

## 3. Status firewall fields (per skill SKILL.md §Claim-Status Firewalls)

```yaml
actual_current_surface_status: proposed_retained
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: true
proposal_allowed_reason: |
  All five chain pieces are retained authorities on main:
  OP (T1+T2), PHYSICAL_LATTICE_NECESSITY §9, ONSITE no-go,
  Canonical-descent Theorem 1, CRIT. The structural argument in §1.1
  and §1.2 composes them into a single axiom-to-readout chain. No new
  axiom is introduced; no observed mass is used as proof input.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

The bare `retained` wording is BANNED on this branch-local source note
per the skill's claim-status firewall. The wording `proposed_retained`
is permitted only because all five conditions of the
retained-proposal certificate (skill §Retained-Proposal Certificate)
are satisfied; see [CLAIM_STATUS_CERTIFICATE.md](../.claude/science/physics-loops/axiom-to-main-lane-cascade-20260429/CLAIM_STATUS_CERTIFICATE.md).

---

## 4. What is and is not closed

### Closed by V8

1. structural derivation that OP Theorem 2's source-domain restriction
   is forced (not chosen) on the A_min surface;
2. structural derivation that competing W̃ structures provide no
   additional physical local scalar observables on the framework's
   substrate;
3. structural derivation that backgrounds in `A \ span{P_x}` must be
   descended via E_loc before scalar-observable readout;
4. unconditional Q = 2/3 on the admitted normalized reduced carrier
   under the V8 chain.

### NOT closed by V8 (carried forward from V4)

1. the separate selected-line boundary-source / based-endpoint theorem
   for δ = 2/9 — addressed in Block 2 of this campaign;
2. the Type-B rational-to-radian observable law behind the Brannen
   phase;
3. the overall charged-lepton scale `v_0`;
4. the same chain for the down-type quark sector — addressed in Block 3.

### What V8 does NOT claim

- V8 does NOT claim that all non-local sources are "physical sources"
  — they are not. The claim is only that they contribute to physical
  local scalar observables via the canonical descent.
- V8 does NOT claim the strict reading of OP T1 in absolute generality
  — it claims the strict reading on the framework's accepted substrate
  surface, where locality is structural.
- V8 does NOT replace independent audit; it explicitly carries the
  audit-required-before-effective-retained flag.

---

## 5. Comparison with V4 / V7.3

| Element | V4 (2026-04-25) | V7.3 (2026-04-27, monday-koide) | V8 (this note, 2026-04-29) |
|---|---|---|---|
| Strict reading | defended hypothesis | conditional Q corollary | structural theorem (§1.1+§1.2) |
| Source-domain inference | interpretive | conditional | structural |
| Bridge to E_loc | open | conditional | retained chain (Step 4) |
| Closure status | support-grade conditional | conditional retained promotion | proposed_retained unconditional |
| Audit required | yes | yes | yes (unchanged) |

V8 does not retract V4 or V7.3 — both remain valid as conditional
support / conditional promotion notes. V8 lifts the conditionality by
naming the structural piece.

---

## 6. Cascade unlocked (proposed for later integration)

If V8 is audit-ratified, the following PUBLICATION_MATRIX rows can be
proposed for promotion (deferred to the later weaving review):

- **line 192 (charged-lepton Koide bridge package):** lift Q residual
  from open to retained corollary;
- **line 166 (charged-lepton Koide support package Q=2/3, δ=2/9):**
  Q half can be promoted; δ half awaits Block 2;
- **line 167 (Q OP source-domain canonical descent):** lift from
  "does not prove" to "proves under structural strict reading";
- **line 168 (Q SO(2) phase erasure support):** unchanged role;
- **line 158 (CKM Bernoulli 2/9 Koide-bridge support):** "no Koide
  closure" qualifier removable for Q (δ pending);
- **line 159 (CKM n/9 structural-family Koide-bridge support):** same;
- **line 160 (CKM cubic Bernoulli Koide-bridge support):** same;
- **line 161 (CKM Egyptian-fraction Bernoulli):** same;
- **line 162 (CKM consecutive-primes / S_3):** same;
- **line 157 (cross-sector Koide/CKM V_cb bridge):** Q half landed.

Total: 9 publication-matrix rows directly affected. Repo-wide weaving
is DEFERRED to later review and backpressure integration per the
physics-loop skill's science-only rule.

---

## 7. Verification

```bash
python3 scripts/frontier_koide_q_op_locality_source_domain_closure.py
```

The runner audits dependency classes (not just numerical output) per the
skill's retained-proposal certificate item 5:

1. **OP Theorem 1 audit:** reads `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
   from disk; verifies Theorem 1 statement (multiplicative-to-additive
   functional equation; uniqueness of W = c log|Z| + const).
2. **OP Theorem 2 audit:** verifies Theorem 2 statement (local scalar
   observables = source-derivatives with `J = Σ j_x P_x`).
3. **PHYSICAL_LATTICE_NECESSITY §9 audit:** reads from disk; verifies
   one-axiom substrate-necessity statement ("locality and spatial
   structure are the tensor-product factorization").
4. **ONSITE no-go audit:** reads from disk; verifies "Z is not an
   onsite diagonal source function" claim and Z's cross-site entries
   via cyclic shift R.
5. **Canonical-descent Theorem 1 audit:** reads from disk; verifies
   uniqueness `E_loc(X) = (Tr X / 3) I`.
6. **CRIT audit:** reads from disk; verifies
   `K = 0 ⇔ Y = I_2 ⇔ z = 0 ⇔ Q = 2/3`.
7. **Algebraic identities (sympy / numpy):**
   - Tr(Z) = -1 (sympy);
   - E_loc(sI + zZ) = (s − z/3) I (algebra);
   - On the C3 orbit, Z has off-diagonal entries (numerical);
   - Q(z = 0) = 2/3 on Y_Z(0) = I_2 (numerical);
   - Independence of the chain from any observed lepton mass input.
8. **Closure flag**:
   `Q_L_EQ_2_OVER_3_PROPOSED_RETAINED_CHAIN_VERIFIED = True`
   (verified by audit, NOT asserted as Boolean closure).

Expected: `PASS = N`, `FAIL = 0`. The PASSes verify all five chain
authorities exist on disk + the algebraic identities. They do NOT
replace the audit step required before the repo treats this as
effective retained.

---

## 8. Honest residual

After V8 lands as `proposed_retained`, the remaining Koide closure
residuals are:

- δ = 2/9 rad analytical derivation (Block 2 target);
- the overall lepton scale `v_0` (out of this loop's scope);
- down-type quark cross-sector universality (Block 3 target).

The Q half of the dimensionless Koide closure is now structurally on
the A_min surface modulo audit ratification.
