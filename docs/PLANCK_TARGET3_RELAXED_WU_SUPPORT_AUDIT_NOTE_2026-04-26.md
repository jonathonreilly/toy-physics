# Planck Target 3 Relaxed-Wu Support Audit Note

**Date:** 2026-04-26
**Status:** exact support/control packet for the Planck Target 3 lane; **not**
a minimal-stack retained derivation of `a^(-1)=M_Pl`
**Reviewed branch:** `origin/claude/relaxed-wu-a56584`
**Primary runner:** `scripts/frontier_planck_target3_relaxed_wu_support_audit.py`

---

## 1. Purpose

The `relaxed-wu` branch contains useful object-level Planck-lane algebra, but
its retained-closure framing is too strong. The branch still assumes the
physical source/coupling identification that the current public Planck lane
keeps open.

This note lands the useful parts as support:

1. the CAR/vacuum one-tick construction produces the same rank-four carrier
   `P_1 = P_A` already used in the Planck packet;
2. the signed `S_4` action on abstract `Cl_4` has a unique grade-1 invariant
   generator `H_first`, while grade 2 and grade 3 have no invariant Clifford
   word;
3. the cubic-bivector Schur complement has a clean spectrum
   `+/-4(2 +/- sqrt(2))` and exact trace identity `Tr(|L_K|^-1)=1`;
4. the Hodge-dual `P_3` packet has the same Schur spectrum as `P_1`, so the
   Schur data do not select `P_1` by themselves;
5. matching `c_cell=1/4` to the Wald/Bekenstein-Hawking coefficient gives
   `G_Newton,lat=1` and `a/l_P=1` only after the gravitational boundary/action
   carrier and universal Wald/BH input are accepted.

This is a useful control surface. It is not the Planck kill shot.

---

## 2. What is retained from the branch

### 2.1 CAR/vacuum support for `P_1`

On the time-locked four-axis event cell

```text
H_cell = (C^2)^{otimes 4},
```

let `c_a^dag` be the standard Jordan-Wigner creation operators and let
`|vac> = |0000>`. The one-tick boundary operator

```text
B_1 = sum_a (c_a^dag |vac>)(c_a^dag |vac>)^*
```

is exactly the Hamming-weight-one projector

```text
B_1 = P_1 = P_A.
```

Therefore

```text
Tr((I_16/16) B_1) = rank(P_1)/16 = 4/16 = 1/4.
```

This supports the existing primitive coframe carrier. Its scope is still
conditional on the physical statement that one primitive gravitational
boundary/action event is the one-creation, one-tick sector.

### 2.2 `S_4` grade-1 uniqueness

Under the signed axis-permutation action on abstract `Cl_4`,

```text
dim(Cl_4^{S_4}) = 2,
dim(Cl_4 grade 1)^{S_4} = 1,
dim(Cl_4 grade 2)^{S_4} = 0,
dim(Cl_4 grade 3)^{S_4} = 0.
```

The unique non-scalar grade-1 invariant is

```text
H_first = gamma_0 + gamma_1 + gamma_2 + gamma_3.
```

This is useful because it proves uniqueness inside the first-order Clifford
source class. It does **not** by itself prove that the physical gravitational
boundary/action carrier must be first-order. In the Hamming-weight packet
language, both `P_1` and the Hodge-dual `P_3` are rank-four `S_4`-symmetric
packets.

### 2.3 Cubic-bivector Schur control

For

```text
H_biv = i sum_{a<b} gamma_a gamma_b,
```

the Schur complement on `K=P_1 H_cell` has spectrum

```text
spec(L_K) = {-4(2+sqrt(2)), -4(2-sqrt(2)),
              4(2-sqrt(2)),  4(2+sqrt(2))}.
```

Therefore

```text
Tr(|L_K|^-1)
  = 2/[4(2-sqrt(2))] + 2/[4(2+sqrt(2))]
  = 1.
```

The same spectrum and trace occur on `P_3`. This means the Schur object is a
strong algebraic control, but it is not a `P_1` selector.

### 2.4 Wald/BH coefficient support

If the physical gravitational boundary/action carrier is identified with the
primitive `P_1` carrier and the universal Wald/Bekenstein-Hawking form

```text
S = A/(4 G)
```

is used as physics input, then the framework coefficient

```text
c_cell = 1/4
```

matches the Wald/BH coefficient:

```text
c_cell = 1/(4 G_Newton,lat)  ->  G_Newton,lat = 1.
```

Together with the conventional Planck definition `l_P^2 = G_phys`, this gives
the conditional same-surface result

```text
a/l_P = 1.
```

This is exactly the current Planck package posture: a strong conditional
completion once the carrier/source identification is accepted, not a
minimal-stack derivation of the absolute lattice spacing.

---

## 3. What is not landed

The branch's following headline claims are not retained here:

- `Planck Target 3 unconditionally closed`;
- `a^(-1)=M_Pl` derived from the minimal stack with no package pin;
- `B_grav=P_A` derived as the unique physical gravitational boundary/action
  density without a remaining source principle;
- `Tr(|L_K|^-1)=4 c_cell G_Newton,lat` derived as a physical source-coupling
  law rather than imposed as the coupling interpretation;
- `P_1` selected over `P_3` by Schur spectra alone.

The exact remaining blocker is still:

```text
derive the physical gravitational boundary/action source principle that
identifies the primitive boundary carrier and its Schur/Wald coupling with
Newton's physical source unit.
```

---

## 4. Closeout flags

```text
RELAXED_WU_SUPPORT_LANDED=TRUE
CAR_VACUUM_ONE_TICK_P1_SUPPORT=TRUE
S4_GRADE1_UNIQUENESS_SUPPORT=TRUE
CUBIC_BIVECTOR_SCHUR_TRACE_SUPPORT=TRUE
P1_P3_SCHUR_SPECTRA_IDENTICAL=TRUE
P1_OVER_P3_SELECTOR_CLOSED=FALSE
SCHUR_TRACE_SOURCE_COUPLING_IDENTIFICATION_CLOSED=FALSE
BH_WALD_MATCH_CONDITIONAL_ON_CARRIER_AND_UNIVERSAL_PHYSICS=TRUE
PLANCK_PIN_MINIMAL_STACK_CLOSURE=FALSE
```

---

## 5. Validation

```bash
python3 scripts/frontier_planck_target3_relaxed_wu_support_audit.py
```

The runner checks the retained/support authority boundary from disk and
verifies the CAR/vacuum, `S_4`, Schur-spectrum, Hodge-dual, and conditional
Wald/BH statements at object level.
