# Koide A1 — Brannen `δ = arg(b)` Plancherel Identity Support Note

**Date:** 2026-04-25
**Lane:** Koide A1 / radian-bridge — adds an exact algebraic identity to
the existing Brannen support stack. **Does NOT close the physical
Brannen-phase bridge on current `main`.**
**Status:** support-grade algebraic identity inside the Brannen
parameterization. The Round-10 audit residual `P_A1`
(`KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md`)
remains open on the live authority surface.
**Runner:** `scripts/frontier_koide_a1_brannen_plancherel_identity_support.py`

---

## 0. Status correction

A prior version of this note framed its content as "closure of the
radian-bridge / `P_A1` residual on the Brannen observable". On review
(`review.md`, branch `claude/flamboyant-hodgkin-e16786`), that framing
was withdrawn:

- the note proves a clean **algebraic identity inside the assumed
  Brannen parameterization**;
- it does **not** prove that the physical charged-lepton phase bridge
  on current `main` is exactly that parameterization;
- the runner's `chain_uses_RZ_lift = False` was a tautology by
  construction, not a verification of a missing physical step;
- the audit's open Type-B-to-radian residual on the live authority
  surface was therefore bypassed, not removed.

This rewrite preserves the real algebraic content as honest support and
drops the closure framing. §6 records what would actually be needed for
a live closure.

---

## 1. The algebraic identity (real content)

> **Lemma (Brannen `δ = arg(b)` algebraic identity).**
> Let `v = (√m_1, √m_2, √m_3) ∈ ℝ³_{>0}` admit the Brannen
> parameterization
>
> ```text
> √m_k = V_0 (1 + c · cos(δ + 2π(k−1)/3)),     k = 1, 2, 3,
> ```
>
> with `V_0 > 0`, `c > 0`, `δ ∈ ℝ`. Define the real `C_3` Plancherel
> components
>
> ```text
> a_0 := (v_1 + v_2 + v_3)/√3,
> b   := (v_1 + ω̄ v_2 + ω v_3)/√3,        ω = exp(2πi/3).
> ```
>
> Then
>
> ```text
> a_0 = √3 V_0,
> b   = (√3/2) V_0 c · exp(iδ),
> ```
>
> so `arg(b) = δ` (mod 2π).

The proof is direct algebra (verified symbolically by `sympy` in the
runner §1). The cosine sum `Σ_j cos(δ + 2πj/3) = Re(e^{iδ} · Σ_j ω^j) = 0`
gives `a_0 = √3 V_0`; the cube-roots-of-unity computation
`Σ_j ω̄^j · cos(δ + 2πj/3) = (3/2) e^{iδ}` gives `b`.

This is an exact identity inside the Brannen parameterization. It is
useful as a complementary algebraic reading of `δ`, but its scope is
**inside the parameterization**, not the live authority surface.

---

## 2. PDG numerical signature (real content)

The existing Brannen-PDG match
(`KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md` §5,
`frontier_koide_brannen_route3_geometry_support.py` §5)
already verifies that the literal value `δ = 2/9 rad` reproduces PDG
charged-lepton √m to `<0.1%` while `δ = 4π/9 rad` (the canonical
`R/Z → U(1)` lift `χ(2/9) = exp(2πi · 2/9)`) fails outright.

The runner here re-verifies this and adds the Plancherel-side reading:
inverting the PDG `(√m_1, √m_2, √m_3)` through the Plancherel
decomposition produces a doublet `b_PDG` whose argument
(reduced to the first `Z_3` sector) is `≈ 2/9 rad`. This is empirical
support for the algebraic identity §1; it is **not** a derivation that
the live authority surface forces this reading.

---

## 3. Compatibility with the existing selected-line geometry packet

`KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md` §1 records
that on the retained selected-line `H_sel(m)`, the perp-plane rotation
angle `α(m)` of the Koide amplitude satisfies
`α(m_*) − α(m_0) = −2/9` exactly (geometry runner §7.4).

The Plancherel `arg(b)` reading and the perp-plane rotation `α` reading
are two orthonormal-basis choices for the same Euclidean angle in the
2-plane orthogonal to `(1,1,1)/√3`. Their differences agree up to sign
(geometry runner already shows this; this runner re-checks at §4).

This is the "complementary Euclidean-angle reading compatible with the
existing selected-line support packet" that the review identifies as
landable. It is not a new physical-bridge step.

---

## 4. Why this is **not** a closure of `P_A1` on the live surface

The Round-10 audit
(`KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md` §3)
isolates `P_A1` as the Type-B-to-radian observable law on the **live
authority surface**, where:

- the physical Brannen-phase bridge from the actual carrier to the
  ambient `η = 2/9` quantity remains **open**
  (cf. `KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md` §0);
- the actual-route Berry-phase identification of
  `KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` is itself recorded as
  an "actual-route theorem stack" that "current main has not yet
  adopted" (Berry note §5, §9);
- the Brannen mass formula is, at present, a parameterization of the
  observed masses — the framework's authority on `main` does not yet
  derive it as the unique physical mass formula on the retained carrier.

Inside that parameterization, the algebraic identity §1 is exact. But
because the parameterization itself is not promoted to retained-on-main
authority, deriving `δ = arg(b)` inside it does **not** discharge the
audit's open residual on the live surface.

The runner's prior `chain_uses_RZ_lift = False` flag was true by
construction (the chain in §1 indeed does not use an `R/Z → U(1)`
lift), but that tautology does not certify that the live physical
observable goes through the §1 chain rather than through the
`χ`-canonical chain the audit identifies.

---

## 5. Honest closeout flags

```text
KOIDE_A1_RADIAN_BRIDGE_AUDIT_CLOSES_DELTA=FALSE
TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE_ON_LIVE_SURFACE=TRUE
P_A1_STATUS=OPEN_ON_CURRENT_MAIN
THIS_NOTE_PROVES=ALGEBRAIC_IDENTITY_INSIDE_BRANNEN_PARAMETERIZATION
THIS_NOTE_DOES_NOT_PROVE=PHYSICAL_OBSERVABLE_IDENTIFICATION_ON_RETAINED_MAIN
SUPPORT_NUMERICAL_WITNESS_ON_RETAINED_SELECTED_LINE=2/9_RAD_AT_1E-12
```

These supersede the prior `=DISCHARGED` flags, which were inconsistent
with the live authority surface.

---

## 6. What an actual closure would require (clean resubmission target)

The review identifies two specific load-bearing steps that this note
does **not** supply and that any future closure attempt must:

1. **Promote the actual-route Berry-phase theorem stack to current-main
   authority.** `KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` already
   identifies the physical selected-line phase observable with the
   tautological Berry holonomy `Hol(m_0 → m) = θ(m) − 2π/3 = δ(m)` on
   the retained `H_sel(m)` carrier. That stack is currently labeled
   "actual-route" support, not retained-main authority. A live closure
   would require auditing why current `main` does not yet adopt it,
   addressing each blocker, and promoting the Berry theorem to
   retained-main. Once promoted, the §1 algebraic identity composes
   with it to show that the Brannen `δ` is the Berry-holonomy reading
   throughout — which by §1 is the cosine argument, hence rad-valued
   without an `R/Z → U(1)` lift.

2. **Derive the value `2/9` from retained dynamics, not match it
   numerically.** The geometry runner verifies
   `α(m_*) − α(m_0) = −2/9` to `10⁻¹²` on the retained `H_sel(m)`, but
   this is a numerical witness on a hard-coded `m_*`. A live closure
   needs an analytic derivation: either (a) the Berry holonomy on
   `H_sel(m)` evaluates to the closed-form `2/9` at the dynamics-selected
   `m_*` (selection theorem on `H_sel`), or (b) a Callan-Harvey-style
   bridge identifies the dynamics value with an ambient retained
   anomaly/Plancherel rational so that the audit's `2/9` source and the
   Berry holonomy are the same observable, not a numerical
   coincidence. The Callan-Harvey candidate
   (`KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md`) is the
   current best-shaped route; it remains "bridge-conditioned support",
   not closure.

These are concrete, named follow-on steps. Neither is supplied here.

---

## 7. Verification

```bash
python3 scripts/frontier_koide_a1_brannen_plancherel_identity_support.py
```

The runner now verifies only what is actually proved:

1. Symbolic identity `a_0 = √3 V_0` (sympy).
2. Symbolic identity `b = (√3/2) V_0 c · exp(iδ)`, hence `arg(b) = δ`
   (sympy).
3. Numerical PDG cross-check: inverting PDG √m through the Plancherel
   decomposition gives `|arg(b)| ≈ 2/9 rad` in the first `Z_3` sector,
   not `4π/9 rad` (the canonical `χ`-lift value).
4. Brannen reconstruction with `δ = 2/9 rad` matches PDG `<0.1%`.
5. Counterfactual: `δ = 4π/9 rad` fails PDG (negative √m eigenvalue).
6. Cross-check against the existing geometry-support runner:
   `α(m_*) − α(m_0) = −2/9` on retained `H_sel(m)` at `10⁻¹²`.
7. Cross-check that the Plancherel `arg(b)`-difference equals the
   perp-plane rotation difference up to sign (basis-change consistency).

The previous tautological closure flags
(`chain_uses_RZ_lift = False`, `RADIAN_BRIDGE_RESIDUAL_DISCHARGED`,
etc.) are removed. The runner now ends with explicit "support-grade"
status, not closure.

---

## 8. Cross-references

- `review.md` (this branch) — review note recording the closure
  overclaim and specifying the resubmission target.
- `docs/KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`
  — parent audit.
- `docs/KOIDE_A1_FRACTIONAL_TOPOLOGY_NO_GO_SYNTHESIS_NOTE_2026-04-24.md`
  — Round-10 no-go batch; sharpens `P_A1` to the period-convention
  formulation that this note does **not** discharge on the live
  authority surface.
- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` — actual-route
  Berry theorem stack (support-grade); the load-bearing physical
  identification a live closure would need to promote.
- `docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md` —
  selected-line geometry support; numerical witness for the value
  `2/9` on the retained carrier.
- `docs/KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md` —
  candidate Callan-Harvey-style bridge route to the value `2/9`;
  currently bridge-conditioned support.
- `docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md` —
  conditional `δ = Q/d` route; preserved on the dimensional-ratio
  reading.
- `docs/KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md` —
  `δ = Q/d` linking; preserved.
- `docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` —
  retained `C_3` Plancherel decomposition.
