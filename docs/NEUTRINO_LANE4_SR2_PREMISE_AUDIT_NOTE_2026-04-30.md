# Neutrino Lane 4 — SR-2 Premise Audit

**Date:** 2026-04-30
**Status:** support / premise-audit (named obstruction). This note does **not**
close `(C2-X)`, does **not** prove or falsify `(SR-2)`, and does **not** retire
any open Lane 4 primitive. It records a structural gap between the retained
scalar 2-point closure and the admissible-Pfaffian-extension surface that the
2026-04-28 stuck fan-out recommended as a single-cycle attack.
**Script:** `scripts/frontier_neutrino_lane4_sr2_premise_audit.py`
**Lane:** 4 — Neutrino quantitative closure, `(SR-2)` continuum-limit scalar
2-point incompatibility with Pfaffian extensions.

---

## 0. Why this note exists

The 2026-04-28 [`NEUTRINO_AXIOM3_READING_STUCK_FANOUT_NOTE`](./NEUTRINO_AXIOM3_READING_STUCK_FANOUT_NOTE_2026-04-28.md)
§4.2 records:

> Of these, `(SR-2)` is the most promising as a single-cycle attempt: the
> continuum-limit closure is already retained as a theorem-grade result (per
> the framework's emergent-Lorentz cluster), and sharpening it to "constrains
> pairing extensions" is a self-contained structural step.

This note audits that recommendation. It finds that as currently framed,
`(SR-2)` is **not** a single-cycle target: the retained continuum-limit scalar
2-point closure and the admissible-Pfaffian-extension surface live on
separate substrate sectors (free scalar vs. fermion bilinear), and the
connecting primitive — a scalar-fermion loop calculation on the framework
substrate — is itself unretained.

This is a Deep-Work-Rules "named obstruction" finding. It does not close SR-2
negatively; it relocates SR-2 from "single-cycle structural step" to
"multi-block research program with one explicit prerequisite primitive".

## 1. The retained scalar 2-point closure

The 2026-04-25 retained theorems define the scalar 2-point closure as a
property of the **free-scalar Wightman 2-point function** on the framework
Hamiltonian lattice:

- 1+1D: [`LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE`](./LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md)
  proves SO(1,1) boost covariance of `W_lat(Delta t, Delta x; a, m)` in the
  continuum limit `a -> 0`, with `W_lat -> (1/(2pi)) K_0(m sqrt(-s^2))`.
- 3+1D: [`LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE`](./LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md)
  proves SO(3,1) boost covariance of `W_lat(Delta t, Delta vec x; a, m)` in
  the continuum limit, with `W_lat -> m K_1(m sqrt(-s^2)) / (4 pi^2 sqrt(-s^2))`.
  Finite-`a` deviations are `(a^2 p^4)/E^2` cubic-harmonic dim-6 corrections
  inherited from the emergent-Lorentz cluster.

Both theorems are stated for the **free scalar field**. The construction takes
a bosonic Laplacian dispersion `E_lat^2(p) = m^2 + sum_i (4/a^2) sin^2(p_i a/2)`
and integrates against the free-scalar spectral measure. There are no fermion
loops. There is no interaction.

The SO(3,1) invariant `s^2 = Delta t^2 - |Delta vec x|^2` is the **only**
covariant variable in the continuum limit. Any structural input that
introduces a `(Delta t, Delta vec x)` dependence not reducible to `s^2`
breaks boost covariance.

## 2. Admissible Pfaffian extensions

The 2026-04-28 fan-out §4.1 defines admissible Pfaffian extensions as:

> Extensions of the staggered-Dirac partition by `chi^T S chi`-type pairing
> terms `S` that preserve all retained:
> - gauge anomaly cancellations (SM gauge cluster proofs);
> - emergent-Lorentz dimension-6 onset and continuum-limit free-scalar 2-point
>   closure;
> - canonical normalization `g_bare = 1`;
> - Planck-scale conditional completion premises.

Crucially, the Pfaffian term `chi^T S chi` is a **fermion bilinear**. It is
Grassmann-even but has charge `±2` under `U(1)_V` rather than charge `0` like
the standard Dirac mass `bar chi chi`.

The pairing `S` is a Lorentz-tensor structure (in the continuum limit) that
combines two Weyl spinors of the same handedness. In flat-space continuum
QFT, the simplest admissible `S` is `S_alpha beta = epsilon_alpha beta`
(antisymmetric `SL(2, C)` invariant), giving a covariant Majorana mass term.

## 3. The structural gap

§1 establishes the 2-point closure on the **scalar field**. §2 describes
Pfaffian extensions as `chi^T S chi`-type **fermion bilinears**. These are
distinct substrate sectors.

The 2026-04-28 fan-out's recommendation of SR-2 implicitly assumes a
direct constraint:

> Continuum-limit free-scalar 2-point covariance constrains admissible
> Pfaffian pairing structure.

But on the framework substrate as currently retained, this constraint is
**not direct**. A Pfaffian fermion-bilinear extension affects the scalar
2-point function only **indirectly**, through fermion-loop corrections in
an interacting scalar-fermion theory. The retained 2-point closure is for
the **free** scalar; introducing fermion loops requires:

- a retained scalar-fermion coupling on the framework substrate;
- a retained one-loop fermion vacuum-polarization primitive that handles both
  Dirac and Pfaffian propagators;
- a retained renormalization scheme that preserves boost covariance through
  the loop integration (or fails to, in a constrained way).

None of these is currently retained at theorem-grade. The closest analog is
the standard QED running primitive (which the 2026-04-30 atomic Lane 2
firewall identified as itself an open primitive blocking Lane 2).

**Therefore, as currently posed, `(SR-2)` is not a self-contained single-cycle
structural step.** The retained 2-point closure is on the wrong sector;
extending it to the fermion sector requires structural primitives that are
themselves open.

## 4. What `(SR-2)` would actually require

To make SR-2 a single-cycle target, the framework needs at minimum one of:

### 4A. Direct fermionic 2-point closure

Prove an analog of the [`LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM`](./LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md)
on the **staggered-Dirac fermion** substrate, not the free scalar:

> The continuum-limit free-staggered-Dirac fermion 2-point function `<chi(x)
> bar chi(y)>` is SO(3,1) boost covariant, transforming as a Lorentz spinor.

If this holds, then a Pfaffian extension introducing `<chi(x) chi(y)>` would
have to produce a Lorentz-covariant tensor structure. The constraint is then
direct: SO(3,1) covariance constrains the rank-(0, 2) tensor structure of the
anomalous propagator.

This is a structural step, but it is **separate from** the existing scalar
2-point closure. It needs to be retained in its own right.

### 4B. Admitted scalar-fermion coupling

Admit a specific scalar-fermion coupling on the framework substrate (e.g.,
Yukawa) and use the retained scalar 2-point closure as a constraint on the
fermion-loop corrections to it. A Pfaffian-modified fermion propagator in the
loop would produce a different scalar self-energy than a Dirac propagator;
the retained 2-point closure constrains which scalar self-energies are
admissible.

This route requires:

- an admitted Yukawa-type coupling structure;
- a retained one-loop computation on the framework substrate;
- a way to distinguish Pfaffian-induced from Dirac-induced corrections at the
  level of the scalar 2-point.

### 4C. Direct SR-2 as a scalar-fermion identity

A genuine direct constraint between scalar 2-point and fermion bilinear would
have to come from an underlying SUSY-like structure or an identity at the
substrate level. There is no current retained SUSY structure on the framework
substrate.

## 5. Implications for Lane 4 closure

The 2026-04-28 fan-out treated SR-2 as the recommended single-cycle
continuation. This audit shows SR-2 in its current framing is at least a
2-block program:

```text
Block A: Direct fermionic 2-point closure (4A above) OR admitted Yukawa
         + one-loop primitive (4B above)
   |
   v
Block B: SR-2 proper — show admissible Pfaffian extensions either preserve
         covariance (and are trivial via 4A's constraint) or break
         covariance (and are excluded).
```

This does not invalidate SR-2 as a target. It re-times SR-2 from
"single-cycle attempt" to "two-block program with named prerequisite". The
prerequisite is concrete and self-contained.

The other named alternatives in the 2026-04-28 fan-out — `(SR-1)`
Lorentz-onset incompatibility, `(SR-3)` stronger SM anomaly cluster — are
similarly worth re-auditing for hidden prerequisites. This note does not
re-audit them.

## 6. What this note retires

This note retires **one tempting framing**:

> "(SR-2) is a single-cycle structural step combining retained scalar 2-point
> closure and admissible Pfaffian extension."

It is not. The retained closure is on the **free-scalar** sector; the Pfaffian
extension is on the **fermion-bilinear** sector. They share substrate but do
not share derivation grammar without an additional retained primitive.

## 7. What this note does NOT do

- It does not close `(C2-X)`.
- It does not prove or disprove `(SR-2)`.
- It does not retire any Pfaffian-extension companion note.
- It does not falsify the 2026-04-28 fan-out's overall framing — only the
  "single-cycle" timing claim.

## 8. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_neutrino_lane4_sr2_premise_audit.py
```

The runner verifies:

1. The relevant retained 2-point closure notes exist (1+1D and 3+1D).
2. The 2026-04-28 fan-out note exists and contains the SR-2 recommendation
   text being audited.
3. The note does NOT use bare `retained` / `promoted` wording.
4. The structural-gap claim is self-consistent: scalar 2-point notes do not
   reference Pfaffian extensions, and Pfaffian-extension notes do not
   reference the free-scalar 2-point structure as a constraint.
5. The note names at least three concrete prerequisite primitives (4A, 4B,
   4C) that would unblock SR-2.
6. Forbidden-import roles are respected: no PDG observation appears as proof
   input.

## 9. Inputs and import roles

| Input | Role | Import class | Source |
|---|---|---|---|
| 1+1D SO(1,1) boost-covariance theorem | retained 2-point closure (free-scalar sector) | framework retained | [LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md](./LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md) |
| 3+1D SO(3,1) boost-covariance theorem | retained 2-point closure (free-scalar sector) | framework retained | [LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md](./LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md) |
| 2026-04-28 stuck fan-out note | SR-2 recommendation being audited | repo authority surface | [NEUTRINO_AXIOM3_READING_STUCK_FANOUT_NOTE_2026-04-28.md](./NEUTRINO_AXIOM3_READING_STUCK_FANOUT_NOTE_2026-04-28.md) |
| Pfaffian no-forcing theorem | scoping background on Pfaffian extensions | framework retained | [NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md](./NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md) |

No new physical claims, no new numerical comparators, no new admitted observations are introduced. This is structural premise auditing.

## 10. Safe wording

**Can claim:**

- "SR-2 premise audit identifies a structural gap."
- "SR-2 is at least a 2-block program with one named prerequisite primitive."
- "The retained 2-point closure lives on the scalar sector; admissible
  Pfaffian extensions live on the fermion sector."
- "Three candidate prerequisite primitives identified (4A, 4B, 4C)."

**Cannot claim:**

- bare `retained` / `promoted`.
- "(SR-2) closes `(C2-X)`." (it doesn't, in any form yet)
- "(SR-2) is excluded." (it isn't — it is re-timed)
- "(C2-X) is closed by this note." (it isn't)

## 11. Cross-references

- **Block 1 (this campaign):** [ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30](./ATOMIC_LANE2_QED_RUNNING_DEPENDENCY_FIREWALL_NOTE_2026-04-30.md) — analogous QED running primitive audit; sister artifact.
- **Block 2 (this campaign):** `CROSS_LANE_DEPENDENCY_MAP_NOTE_2026-04-30.md` — places this finding in the broader cross-lane structure (Lane 4 component).
- **Lane 4 parent:** [`docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md`](./lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md).
- **Workstream closeout:** [`NEUTRINO_LANE4_WORKSTREAM_CLOSEOUT_NOTE_2026-04-28.md`](./NEUTRINO_LANE4_WORKSTREAM_CLOSEOUT_NOTE_2026-04-28.md) — the close-out that named SR-2 as next-recommended.
