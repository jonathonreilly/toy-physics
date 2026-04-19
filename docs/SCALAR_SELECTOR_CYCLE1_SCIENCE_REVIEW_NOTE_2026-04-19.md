# Scalar-Selector Cycle 1-10 Science Review Note

**Date:** 2026-04-19
**Scope:** Science audit of the cycle-1 to cycle-10 scalar-selector branch.
This note is intentionally **not** a claim-surface audit. The question here is
whether the new logic paths themselves actually close the targeted open gates.

**Later update.** A same-day meta-closure pass tightened the structural read to
`4 -> 2` at the meta-axiom layer via DIM-UNIQ + STRC, but it did **not**
change the per-gate scientific verdict below: the branch still does not clear
the reviewer's object-derivation bar on any of the four gates. See
`docs/SCALAR_SELECTOR_CYCLE13_META_CLOSURE_STATUS_NOTE_2026-04-19.md`.

## Executive decision table

| Path | Target gate | Science result | Does it close the gate? | Review decision |
|---|---|---|---|---|
| MRU | Koide `kappa = 2` | exact equivalence theorem on `Herm_circ(d)` | **No** | support / candidate principle only |
| Berry holonomy | Koide `delta = 2/9` | coherent geometric construction with correct `2/9` output | **No** | geometric support / candidate only |
| DPLE | DM `A-BCC` / F4 lane | useful exact matrix-analysis theorem; reproduces F4 on fixed basin chart | **No** | support theorem on the open DM gate |
| RPSR | quark `a_u` / Min-C lane | strong conditional route with one explicit remaining algebraic gap | **No** | conditional support theorem |

## 1. MRU on `Herm_circ(d)` -- Koide `kappa`

**Primary files**

- `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_koide_moment_ratio_uniformity_theorem.py`

### What scientifically holds

The note proves an exact statement:

- define the isotype moments on the Hermitian circulant algebra
  `Herm_circ(d)` using the Frobenius metric;
- impose Moment-Ratio Uniformity (MRU), meaning those moments are equal across
  `Z_d` isotypes;
- at `d = 3`, MRU is exactly equivalent to `a^2 = 2 |b|^2`, i.e.
  `kappa = 2`.

This is mathematically coherent. The runner verifies the algebraic equivalence,
the per-`d` equation counts, and the `d = 3` singlet-vs-doublet uniqueness
pattern.

### Why it does **not** close the gate

The charged-lepton gate is not merely "find any principle equivalent to
`kappa = 2`." The scientific burden is to show why the physical charged-lepton
carrier should satisfy that principle.

This branch does **not** derive MRU from:

- the retained charged-lepton carrier dynamics,
- a variational law on the physical selected line,
- a previously established operator identity,
- or an independent microscopic mechanism that forces isotype moment equality.

So the branch has not removed the missing scalar selector law. It has
**repackaged** it as MRU.

### Science decision

MRU is scientifically useful as a **support/candidate principle**:

- it gives a clean exact restatement of the remaining scalar condition;
- it shows strong `d = 3` representation-theoretic uniqueness;
- it sharpens what kind of law would be sufficient.

But it does **not** by itself close the Koide `kappa` gate.

## 2. Berry holonomy on `S^2_Koide` -- Koide `delta = 2/9`

**Primary files**

- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`
- `scripts/frontier_koide_berry_phase_theorem.py`

### What scientifically holds

The note constructs a geometric model:

- projectivize the Koide cone to `S^2_Koide`;
- attach a nontrivial line bundle / monopole connection to the doublet sector;
- compute the holonomy over one `C_3` period;
- obtain
  `delta_d = (d - 1) / d^2`, hence `delta_3 = 2/9`.

As a geometric construction, this is coherent and the runner reproduces the
holonomy arithmetic and the `2/9` value.

### Why it does **not** close the gate

The critical scientific step is not the holonomy calculation. It is the
identification of the physical charged-lepton phase with the Berry holonomy of
this particular bundle.

The branch still assumes the load-bearing geometric input:

- a "natural" equivariant line bundle on `S^2_Koide`,
- with the relevant first Chern number `n = d - 1 = 2`,
- and with the physical charged-lepton phase read off from that holonomy.

Those are added geometric choices. They are not independently forced by the
existing charged-lepton package, and the note itself still records an open point
around the Chern-class packaging.

### Verification weakness

The companion runner is weaker than the note:

- several theorem-adjacent items are recorded as `PASS` using hard-coded `True`
  values or narrative placeholders rather than actual checks;
- in particular, equivariance, cross-lane compatibility, minimality
  compatibility, and the uniqueness of `n = 2` are not numerically or
  symbolically certified in the same way as the core holonomy arithmetic.

### Science decision

This is a **geometric support/candidate route** to the Koide phase, not a full
scientific closure of the `delta = 2/9` gate.

## 3. DPLE on the DM pencil -- F4 / `A-BCC`

**Primary files**

- `docs/DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md`
- `docs/DM_CHAMBER_SIGNATURE_STRUCTURE_NOTE_2026-04-19.md`
- `scripts/frontier_dm_dple_theorem.py`

### What scientifically holds

This is the strongest new theorem in the branch.

The note establishes a genuine matrix-analysis statement:

- for a Hermitian pencil `H(t) = H_0 + t H_1`,
- `W(t) = log|det H(t)|` has at most `floor(d/2)` interior Morse-index-0
  critical points;
- at `d = 3`, that gives a clean binary selector structure;
- on the tested DM chart `(H_base, J_*)`, the `d = 3` specialization reproduces
  the previously named F4 condition on the four basins `{1, N, P, X}`.

This is real science. The runner shows:

- the degree-`d` determinant structure,
- the `floor(d/2)` upper bound numerically on sampled Hermitian pairs,
- explicit `d = 4` fragmentation,
- exact agreement with F4 on the four named basins.

### Why it does **not** close the gate

The live DM gate is not only "is F4 mathematically respectable?" The real
question is whether the physical source-side branch / chart is fixed.

DPLE acts **after** the following are already fixed:

- the use of the linear pencil `H_base + t J_*`,
- the specific basin chart `{1, N, P, X}`,
- the retained source-side ingredients that identify `H_base` and `J_*`.

So DPLE does not derive the physical source-side branch by itself. It shows
that **within that fixed chart**, the old F4 selector is the `d = 3`
specialization of a genuine theorem.

That is valuable, but it is not the same as discharging the remaining `A-BCC`
source-side input.

### Science decision

DPLE should be treated as a **support theorem on the open DM gate**:

- stronger than a mere heuristic,
- worth preserving,
- but not a full closure of the DM selector problem.

## 4. RPSR on the projector ray -- quark `a_u`

**Primary files**

- `docs/QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`
- `docs/QUARK_UP_AMPLITUDE_RETAINED_NATIVE_CANDIDATE_NOTE_2026-04-19.md`
- `docs/SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md`
- `scripts/frontier_quark_up_amplitude_rpsr_conditional.py`

### What scientifically holds

This route is scientifically sharp and useful.

The branch isolates:

- a real structural identity for the scalar/tensor ray-magnitude bridge
  `supp = 6/7`;
- a clear NLO correction `rho / 49`;
- an exact target identity for the preferred `a_u`;
- and a clean uniqueness separation among the eight Pareto candidates.

The runner demonstrates that, once the LO identity is assumed,

```text
a_u / sin(delta_std) + a_d = 1 + rho / 49
```

is exact and uniquely singles out the target candidate.

### Why it does **not** close the gate

The note itself is honest here: the LO identity

```text
a_u / sin(delta_std) + a_d = 1
```

at NNI diagonalization remains unproved.

That means the branch has not closed the quark gate; it has reduced it to one
named algebraic gap.

### Science decision

RPSR is a strong **conditional support theorem** and a genuine improvement over
the older Min-C framing. It does not yet constitute full closure.

## 5. Net science conclusion

This branch does contain meaningful science. The new logic paths do **not**
all collapse under scrutiny. But they also do **not** yet close the key open
gates.

The right scientific read is:

1. **MRU**: exact restatement of the remaining Koide scalar law, not a closure.
2. **Berry**: elegant geometric support model for `2/9`, not a closure.
3. **DPLE**: real support theorem that upgrades the old F4 selector story, but
   does not eliminate the remaining DM source-side open input.
4. **RPSR**: strong conditional reduction of the quark gate to one explicit LO
   algebraic identity.

So the branch is **not** a clean "remaining open gates are now closed"
science packet.

It is a **mixed support packet** containing:

- one strong DM support theorem (DPLE),
- one strong conditional quark route (RPSR),
- and two charged-lepton support/candidate routes (MRU, Berry).

## 6. Salvage recommendation

If this branch is mined selectively, the scientifically worth-preserving pieces
are:

- `DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19.md`
  as a support theorem on the open DM gate;
- `QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`
  plus `SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md`
  as a conditional/support quark packet;
- `KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md`
  and `KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md`
  as infrastructure/support notes if their closure language is demoted.

What is **not** justified by this branch:

- claiming the charged-lepton Koide gate is now scientifically closed;
- claiming the DM flagship gate is now closed through DPLE;
- claiming total scalar-selector axiom cost is now zero.
