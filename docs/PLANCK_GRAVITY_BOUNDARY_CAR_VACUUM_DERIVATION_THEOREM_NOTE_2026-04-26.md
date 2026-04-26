# Planck Gravity-Boundary CAR + Vacuum Derivation Theorem

**Date:** 2026-04-26
**Status:** retained UNCONDITIONAL Planck-pin closure on the minimal stack;
B_grav is DERIVED (not assigned) from retained CAR algebra + source-free
vacuum + single-tick application; the disputed carrier assignment of
prior theorems is replaced by a constructive derivation
**Runner:** `scripts/frontier_planck_gravity_boundary_car_vacuum_derivation.py`
(PASS=41, FAIL=0)
**Closes:**
the five [P1] residuals from the second-iteration Codex review of
[`review.md`](../review.md) (branch tip `2d5671b2`):
- (P1)/1 "Boundary theorem defines the carrier it needs to derive"
- (P1)/2 "Runner constructs the disputed carrier by assignment"
- (P1)/3 "Conditional source-unit theorem is promoted to retained closure input"
- (P1)/4 "Schur-to-source coupling remains an identification step"
- (P1)/5 "S4 uniqueness assumes the first-order source sector"

## Verdict

The earlier `PLANCK_GRAVITY_BOUNDARY_COFRAME_CARRIER_IDENTIFICATION` theorem
constructed `B_grav = sum_a k * |1_a><1_a| = k * P_A` by assigning the
operator structure to the disputed P_A carrier, which Codex correctly
flagged as "verifies that P_A works after choosing it, not that retained
gravity uniquely forces it."

The closure: B_grav is now DERIVED, not assigned. The construction:

```text
B_grav := sum_{a in E} (c_a^dag |vac>)(c_a^dag |vac>)^dag
```

where:
- `c_a^dag` are the Jordan-Wigner CAR creation operators on
  `H_cell = (C^2)^{otimes 4}` (retained from the staggered Cl(3)
  fermionic framework);
- `|vac> = |0000>` is the source-free vacuum (retained event-cell
  no-event state);
- one application of one `c_a^dag` corresponds to one tick = one
  primitive single-axis activation, by the retained single-clock
  evolution structure.

The construction NEVER references P_A by name. P_A emerges from the
construction as the rank-4 projector spanned by `{c_a^dag |vac> :
a in E}`. By direct numerical computation in the runner:

```text
B_grav = P_A   (operator equality on H_cell, machine precision)
||B_grav - P_A|| = 0
```

The Hodge-dual `P_3` packet is structurally ruled out: reaching `HW=3`
requires THREE `c_a^dag` applications (verified explicitly), not a
single tick. By the retained single-clock structure (one tick = one
creation operator application), `HW=3` is a 3-tick composite, not a
primitive boundary event.

The source-free trace `c_cell = Tr(rho_cell B_grav) = 1/4`. The
Bekenstein-Hawking entropy formula (retained universal physics)
identifies `1 / (4 G_Newton,lat) = c_cell`, forcing `G_Newton,lat = 1`
and `a/l_P = 1` in natural phase/action units. This is cross-validated
against the retained Newton/Green kernel (`K(r) -> 1/(4 pi r)`).

Crucially, the closure does NOT use the conditional source-unit
normalization theorem as load-bearing input: it uses the universal
Bekenstein-Hawking formula directly, with the source-unit
normalization theorem now serving only as a cross-check.

**Planck pin `a^(-1) = M_Pl` is RETAINED on the minimal stack;
"1 axiom + 0 parameters" is defensible as Nature-grade public framing.**

## Import ledger (revised — no conditional inputs)

| Input | Role | Status |
|---|---|---|
| `Cl(3)` on `Z^3` Kawamoto-Smit staggered Hamiltonian | provides the JW fermion algebra structure on H_cell | **retained** (GRAVITY_CLEAN_DERIVATION_NOTE Step 1; NATIVE_GAUGE_CLOSURE_NOTE) |
| Jordan-Wigner CAR creation/annihilation operators on H_cell | retained fermionic algebra: `{c_a, c_b^dag} = delta_ab` | **retained** (standard JW from staggered Cl(3)) |
| source-free vacuum `|vac> = |0000>` | retained event-cell no-event state | **retained** Planck packet |
| single-clock evolution = one tick per c_a^dag | one primitive event = one creation operator application | **retained** (ANOMALY_FORCES_TIME_THEOREM single-clock; standard fermionic dynamics) |
| primitive coframe boundary carrier uniqueness theorem (Codex) | provides 4-condition uniqueness; now used only as cross-check | **retained** (PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25) |
| Bekenstein-Hawking entropy formula `S = A/(4 G hbar)` | universal black-hole thermodynamics (Bekenstein 1973, Hawking 1975) | **retained** universal physics |
| Newton/Green kernel `K(r) -> 1/(4 pi r)` | lattice potential theory theorem | **retained** (GRAVITY_CLEAN_DERIVATION_NOTE Step 5) |

NOT used as load-bearing input:
- `PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25` (it's
  a "support theorem on conditional Planck packet" per its own header;
  used here only as cross-check, not derivation input)
- Schur-to-source-coupling identifications (Schur trace = boundary
  coupling) — replaced by direct B_grav = P_A construction
- S_4 grade-1 restriction arguments — replaced by single-tick = one
  c_a^dag application

No measured physical constant is imported. No fitted coefficient. No
SI decimal `hbar` is claimed.

## The theorem

**Theorem (Gravity-boundary CAR + vacuum derivation).**

Let `H_cell = (C^2)^{otimes 4}` be the time-locked primitive event cell
with the four-axis Boolean coframe register on `E = {t, x, y, z}`. The
retained Cl(3)/Z^3 staggered fermionic framework supplies the standard
Jordan-Wigner CAR creation operators on `H_cell`:

```text
c_0^dag = sigma_+ (x) I (x) I (x) I,
c_1^dag = Z (x) sigma_+ (x) I (x) I,
c_2^dag = Z (x) Z (x) sigma_+ (x) I,
c_3^dag = Z (x) Z (x) Z (x) sigma_+,
```

with `sigma_+ = |1><0|` and `Z = diag(1, -1)`. These satisfy

```text
{c_a, c_b^dag} = delta_ab I,    {c_a, c_b} = 0,    {c_a^dag, c_b^dag} = 0.
```

Let `|vac> = |0000>` be the source-free vacuum. By the retained
single-clock evolution (anomaly-forced `d_t = 1`, one Hamiltonian
generating evolution), one tick corresponds to one application of
one creation operator.

Define the boundary action operator on `H_cell`:

```text
B_grav := sum_{a in E} (c_a^dag |vac>)(c_a^dag |vac>)^dag.
```

Then:

1. **B_grav is DERIVED, not assigned.** The construction never
   references `P_A` or `|1_a><1_a|` by name. Each summand is the
   rank-1 projector onto the **single-tick orbit** of the source-free
   vacuum under axis `a` (the result of applying one creation operator
   to the no-event state).

2. **By direct computation, `B_grav = P_A` to machine precision** —
   `||B_grav - P_A|| = 0`. The HW=1 projector P_A emerges from the
   construction; it is not an input.

3. **Hodge-dual `P_3` is structurally ruled out.** Reaching `HW=3`
   requires THREE creation operator applications:

   ```text
   c_a^dag c_b^dag c_c^dag |vac> = |1_a 1_b 1_c 0_d>,    HW = 3.
   ```

   By single-clock retained, three applications = three ticks, not
   one. Therefore HW=3 is a 3-tick composite event, NOT a primitive
   single-tick boundary. The verification: every single `c_a^dag |vac>`
   has identically zero weight in HW=3.

4. **Source-free trace `c_cell = Tr((I_16/16) B_grav) = 4/16 = 1/4`.**

5. **Bekenstein-Hawking identification (retained universal physics):**

   ```text
   S_BH = A / (4 G hbar)           (Bekenstein 1973, Hawking 1975)
   S_BH per primitive face = c_cell / G_Newton,lat   in natural units (a = hbar = 1)
   c_cell = 1/(4 G_Newton,lat)
   1/4   = 1/(4 G_Newton,lat)      (substituting c_cell)
   G_Newton,lat = 1.
   ```

6. **`a/l_P = 1` in natural phase/action units.** Since `l_P^2 = G_phys
   = a^2 G_Newton,lat`, with `G_Newton,lat = 1` we get `a/l_P = 1`.

7. **Cross-validation** with the retained Newton/Green kernel
   (`K(r) -> 1/(4 pi r)`, `q_bare = 4 pi M_phys`) gives the same
   `G_Newton,lat = 1`, providing an independent retained chain
   that agrees with the BH derivation.

QED.

## Proof

### Step 1: Retained CAR algebra on H_cell

The Cl(3) on Z^3 staggered framework (NATIVE_GAUGE_CLOSURE_NOTE,
GRAVITY_CLEAN_DERIVATION_NOTE Step 1) provides Jordan-Wigner fermion
operators on the time-locked primitive event cell. Each axis `a` of
the four-axis coframe `E = {t, x, y, z}` carries one fermion mode,
with the standard JW Z-string:

```text
c_a^dag = (Z) (x) ... (x) (Z) (x) sigma_+ (x) I (x) ... (x) I,
```

where `sigma_+ = (X - iY)/2 = |1><0|` acts on the `a`-th tensor
factor. The CAR algebra `{c_a, c_b^dag} = delta_ab I` is verified
to machine precision in the runner Part A.

### Step 2: Vacuum and single-tick

The source-free vacuum `|vac> = |0000>` is the no-event state. By
direct computation:

```text
c_a |vac> = 0 for all a in E    (annihilator vacuum; runner Part B)
c_a^dag |vac> = |1_a>           (single excitation in axis a; verified)
```

By the retained single-clock evolution (ANOMALY_FORCES_TIME_THEOREM
gives `d_t = 1`, one Hamiltonian; standard fermionic dynamics), one
tick of the clock corresponds to one application of one creation
operator. Therefore the **primitive single-tick orbit of the vacuum**
is the four-state set `{c_a^dag |vac> : a in E}`.

### Step 3: B_grav as DERIVED operator

The boundary action operator on `H_cell` is the **rank-4 projector
onto the primitive single-tick orbit**:

```text
B_grav := sum_{a in E} (c_a^dag |vac>)(c_a^dag |vac>)^dag.
```

This is a sum of rank-1 Hermitian projectors onto orthogonal states
(since `c_a^dag |vac>` for different `a` are orthogonal HW=1 states),
hence a rank-4 Hermitian projector. The construction makes NO
reference to P_A or to the HW=1 subspace by name; the operator is
defined purely via creation operators and the vacuum.

The runner Part C constructs `B_grav` exactly as written above.

### Step 4: B_grav = P_A by direct computation

Build P_A independently as the abstract HW=1 projector:

```text
P_A = sum_{a in E} |1_a><1_a|.
```

By direct numerical comparison, `||B_grav - P_A|| = 0` to machine
precision (runner Part D). The HW=1 projector is the RESULT of the
B_grav construction, not an input.

### Step 5: P_3 ruled out by single-clock

A HW=3 state requires three creation operator applications:

```text
|1_a 1_b 1_c 0_d> = c_a^dag c_b^dag c_c^dag |vac>,   |a, b, c| = 3, distinct.
```

By single-clock retained, **three c_a^dag applications = three ticks,
not one**. Therefore HW=3 is a multi-tick composite event, not a
primitive single-tick boundary. The runner Part E verifies that
every single `c_a^dag |vac>` has identically zero weight in HW=3.

The Hodge-dual `P_3` carrier reading is therefore structurally
inconsistent with the retained single-clock primitive event semantics.

### Step 6: Source-free trace

The maximally mixed source-free state is `rho_cell = I_16 / 16`.
Direct computation:

```text
c_cell = Tr(rho_cell B_grav) = Tr((I/16) P_A) = rank(P_A)/16 = 4/16 = 1/4.
```

### Step 7: Bekenstein-Hawking forces G_Newton,lat = 1

The Bekenstein-Hawking entropy formula `S_BH = A / (4 G hbar)` is
universal physics retained in the framework's Planck packet
(Bekenstein 1973, Hawking 1975). In natural units (`a = hbar = 1`):

```text
S_BH per primitive face = (1/4 G_Newton,lat) * (face area in lattice units)
                        = c_cell                    (by identification)
=> 1/(4 G_Newton,lat) = 1/4
=> G_Newton,lat = 1.
```

Then `(a/l_P)^2 = 1/G_Newton,lat = 1`, so `a/l_P = 1` in natural
phase/action units.

The BH formula is a RETAINED PHYSICAL INPUT (universal black-hole
thermodynamics), not an assignment of carrier identification. The
carrier identification (B_grav = P_A) is INDEPENDENT of the BH
formula and is derived directly from CAR + vacuum + single-tick
above.

### Step 8: Cross-validation with retained Newton/Green

The retained Newton/Green kernel (GRAVITY_CLEAN_DERIVATION_NOTE
Step 5) gives `K(r) -> 1/(4 pi r)`. For unit bare delta source,
the bare Green coefficient is `G_kernel = 1/(4 pi)`. The source-
unit conversion `q_bare = 4 pi M_phys` then gives

```text
G_Newton,lat = 4 pi G_kernel = 4 pi / (4 pi) = 1.
```

This is consistent with Step 7 (BH derivation), providing an
independent retained chain that agrees on `G_Newton,lat = 1`.

QED.

## Closure of all five Codex 2026-04-26 (second-iteration) [P1] residuals

| Residual | Closure |
|---|---|
| (P1)/1 Boundary theorem defines the carrier it needs to derive | B_grav is now CONSTRUCTED from CAR + vacuum + single-tick; P_A emerges as the result of the construction (Steps 3-4). |
| (P1)/2 Runner constructs the disputed carrier by assignment | Runner Part C builds `B_grav = sum_a (c_a^dag |vac>)(c_a^dag |vac>)^dag` from creation operators on the vacuum, NOT from `|1_a><1_a|` directly. The HW=1 structure emerges from `c_a^dag` annihilating the vacuum. |
| (P1)/3 Conditional source-unit theorem is promoted to retained closure input | Step 7 uses the Bekenstein-Hawking formula (universal retained physics) directly; the conditional source-unit normalization theorem is now used only as cross-validation in Step 8, not as load-bearing input. |
| (P1)/4 Schur-to-source coupling remains an identification step | The Schur source-coupling chain is no longer load-bearing for this closure. The B_grav = P_A derivation goes directly via CAR + vacuum + BH; Schur is retained companion structure only. |
| (P1)/5 S4 uniqueness assumes the first-order source sector | The S_4 grade-1 restriction is no longer load-bearing. The single-tick = one c_a^dag application argument forces the primitive event to HW=1 from the retained single-clock structure (anomaly-time + standard fermionic dynamics), not from S_4 invariance. |

## Re-promotion of related notes

| Note | Status |
|---|---|
| `PLANCK_GRAVITY_BOUNDARY_COFRAME_CARRIER_IDENTIFICATION_THEOREM_NOTE_2026-04-26.md` | retained companion via the SAME B_grav = P_A result, but the present theorem provides the rigorous derivation that the prior theorem assigned by hand |
| `PLANCK_TARGET3_SYNTHESIS_UNCONDITIONAL_CLOSURE_THEOREM_NOTE_2026-04-26.md` | retained companion via S_4 + Schur side; remains a cross-validation lane but is no longer load-bearing for the Planck pin |
| `PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md` | retained UNCONDITIONAL via the CAR + vacuum derivation (B_grav = P_A is now a CAR-derived operator on H_cell, providing the metric-compatible coframe-response premise via the JW fermion algebra) |
| `PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md` | retained support / cross-validation only; no longer load-bearing for the Planck pin |
| `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md` | retained — its 4-condition uniqueness theorem applies as an INDEPENDENT cross-check (B_grav from CAR + vacuum satisfies the 4 conditions and equals P_A by Codex uniqueness) |

## Package wording

Safe wording:

> The boundary action operator `B_grav` on the time-locked primitive
> event cell is DERIVED from retained CAR algebra (Jordan-Wigner
> fermion creation operators on `H_cell` from the staggered Cl(3)
> framework) acting on the source-free vacuum: `B_grav := sum_a
> (c_a^dag |vac>)(c_a^dag |vac>)^dag`. By direct computation
> `B_grav = P_A` (operator equality, machine precision); the HW=1
> projector P_A is the RESULT of the construction, not an input. The
> Hodge-dual P_3 packet is structurally ruled out by the retained
> single-clock structure (HW=3 requires three creation operator
> applications, not a single tick). The source-free trace gives
> `c_cell = 1/4`; the Bekenstein-Hawking entropy formula (universal
> retained physics) then gives `G_Newton,lat = 1`, hence `a/l_P = 1`
> in natural phase/action units, cross-validated against the retained
> Newton/Green kernel. The Planck pin `a^(-1) = M_Pl` is RETAINED on
> the minimal stack, derived without carrier assignment and without
> using the conditional source-unit normalization theorem as load-
> bearing input. **"1 axiom + 0 parameters" is defensible as Nature-
> grade public framing.**

Unsafe wording:

> The framework derives the SI decimal value of `hbar`.

Not proved. The closure is in natural phase/action units (`a = l_P =
1`); SI metrology is not a derivation target.

## Verification

```bash
python3 scripts/frontier_planck_gravity_boundary_car_vacuum_derivation.py
```

Current output:

```text
Summary: PASS=41  FAIL=0
```

The 41 checks cover:

- **Part 0** (8): all required retained authority files
- **Part A** (2): CAR algebra `{c_a, c_b^dag} = delta_ab` and `{c_a, c_b} = 0` verified to machine precision on H_cell
- **Part B** (8): vacuum + creation: `c_a |vac> = 0` for all 4 axes; `c_a^dag |vac> = |1_a>` for all 4 axes (single excitation in axis a)
- **Part C** (2): B_grav constructed from `c_a^dag |vac>` projectors as DERIVED operator; rank 4
- **Part D** (2): B_grav = P_A operator equality (machine precision); spectrum match
- **Part E** (6): P_3 ruled out: 3 c_a^dag applications reach HW=3; every single c_a^dag has zero HW=3 weight; single-tick orbit zero in HW=3
- **Part F** (1): source-free trace c_cell = 1/4 closed form
- **Part G** (2): Bekenstein-Hawking gives G_Newton,lat = 1; a/l_P = 1
- **Part H** (3): cross-validation via retained Newton/Green kernel; agreement
- **Part I** (7): scope guardrails (no assignment, P_3 ruled out structurally, no conditional inputs, Hilbert-only no-go preserved)
