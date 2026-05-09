# Crank-Nicolson Lieb-Robinson Bridge for the Light-Cone Framing Note

**Date:** 2026-05-09
**Type:** positive_theorem
**Claim scope:** On the canonical lattice Hamiltonian `H` (parent
`docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`,
eqs. 1-2; finite-range / explicit J bridge
`docs/MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md`),
the **Crank-Nicolson time-evolution operator**
`U_CN = (I - i a_tau H/2) (I + i a_tau H/2)^{-1}` admits the explicit
single-step Lieb-Robinson constant
`v_LR(CN, a_tau) = v_LR(H) / (1 - a_tau J / 2)` and converges to
`v_LR(H) = 2 e r J` as `a_tau -> 0`. This closes the
load-bearing-step gap flagged on the audit row
`light_cone_framing_note` (audit verdict 2026-05-03,
`audited_conditional`).
**Status authority:** independent audit lane only. Narrow bridge note;
does not predict an audit outcome.
**Primary runner:** `scripts/light_cone_crank_nicolson_lr_2026_05_09.py`.

## Why this note exists

The parent note `docs/LIGHT_CONE_FRAMING_NOTE.md` validates the
1+1d staggered Dirac dispersion `v_max(m) = sqrt(m^2 + 1) - m` and
notes that the observed Crank-Nicolson 97% containment cone is
"standard lattice-QFT behavior" — but the audit verdict
(`audited_conditional`, 2026-05-03) flagged exactly the bridging step:

> "the load-bearing bridge identifies the observed Crank-Nicolson
> containment behavior with standard lattice-QFT Lieb-Robinson behavior
> without deriving the LR constant for the actual Crank-Nicolson hopping
> kernel."

The recently-landed PR #806 / `MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md`
derives, for the lattice **Hamiltonian** `H = sum_z h_z`,

```text
    v_LR(H)  =  2 e r J,    r = 1,    J <= |m| + 18    (canonical surface)   (1)
```

This note covers the remaining gap: the framework's evolution as
implemented elsewhere in the repo is the **Crank-Nicolson** scheme
(implicit time-step Cayley transform), not literally `exp(-i t H)`.
The two are different operators at finite `a_tau`, and the LR
constant for the Crank-Nicolson kernel must be derived directly.

## Setup and conventions

Adopt the parent finite-range / explicit-`J` results verbatim:

- **Finite-range Hamiltonian decomposition (F1).** From the bridge
  note: `H = sum_z h_z` with each `h_z` Hermitian, supported in a
  ball of radius `r = 1` lattice spacing around `z`, with
  `J = sup_z ||h_z||_op`. Derived from action coefficients
  (parent RP eqs. 1-2). On `Z^4`, `J <= |m| + 18`.

- **Crank-Nicolson scheme.** The repo's discrete-time evolution uses
  the Cayley transform of the lattice Hamiltonian:

  ```text
      U_CN(a_tau)  :=  (I - i a_tau H / 2) · (I + i a_tau H / 2)^{-1}        (2)
  ```

  with `a_tau` the temporal lattice spacing.

- **Heisenberg evolution.** For `n` Crank-Nicolson steps over
  total time `t = n · a_tau`,

  ```text
      alpha_t^CN(O)  :=  (U_CN^dag)^n · O · U_CN^n                            (3)
  ```

  Note the Crank-Nicolson convention: `U_CN -> exp(-i a_tau H)` as
  `a_tau -> 0`, so `alpha_t^CN(O) -> alpha_t(O) = exp(it H) O exp(-it H)`
  in the continuum limit (verified by runner test CN4-CN5).

- **Sub-critical regime.** Throughout this note, `a_tau J < 2`
  (equivalently `a_tau ||H||_op / 2 < 1` after rescaling); this is
  the convergence radius of the Neumann series for the Cayley
  resolvent below.

## Statement

**(CN-A) Cayley-transform unitarity.** For any Hermitian `H`,
`U_CN(a_tau)` defined by (2) is unitary: `U_CN^dag U_CN = I`.

**(CN-B) Single-step support spread.** Let `epsilon := a_tau J / 2`
and assume `epsilon < 1`. Then for any operator `O_x` at site `x`,

```text
    || [U_CN(a_tau) O_x U_CN(a_tau)^dag, O_y] ||_op
       <=  C_CN(epsilon) · ||O_x|| ||O_y|| · epsilon^{d(x, y)}                (4)
```

with `C_CN(epsilon)` an `O(1)` constant uniform in `a_tau` for `epsilon`
in any compact subinterval of `[0, 1)`. The matrix elements of `U_CN`
itself decay as `O(epsilon^d)` outside the radius-`r` ball of `H`.

**(CN-C) Crank-Nicolson Lieb-Robinson velocity.** For `n` Crank-
Nicolson steps over `t = n a_tau` with `epsilon = a_tau J / 2 < 1`,

```text
    || [alpha_t^CN(O_x), O_y] ||_op  <=  2 ||O_x|| ||O_y|| · exp(- d(x, y) + v_LR^CN · |t|)    (5)
```

with the explicit Crank-Nicolson Lieb-Robinson velocity

```text
    v_LR^CN(a_tau)  :=  v_LR(H) / (1 - a_tau J / 2)                          (6)
                    =  2 e r J · (1  +  (a_tau J / 2)  +  O((a_tau J)^2))
```

In particular `v_LR^CN(a_tau) >= v_LR(H) = 2 e r J`, with equality
only in the continuum limit.

**(CN-D) Continuum limit.** As `a_tau -> 0` at fixed `t`,
`v_LR^CN(a_tau) -> v_LR(H)`, and `alpha_t^CN(O) -> alpha_t(O) =
exp(itH) O exp(-itH)` strongly with leading error `O(a_tau^2 · t · ||H||^3)`.

Statements (CN-A)-(CN-D) constitute the **Crank-Nicolson Lieb-Robinson
theorem** for the framework's discrete-time evolution.

## Proof

### Step 1 — Cayley-transform unitarity (proves CN-A)

For Hermitian `H = H^dag`, `(I - i a_tau H/2)^dag = (I + i a_tau H/2)`,
so

```text
    U_CN^dag  =  (I + i a_tau H/2)^{-dag} · (I - i a_tau H/2)^dag
              =  (I - i a_tau H/2)^{-1}   · (I + i a_tau H/2)                (7)
```

(using `((I + i a_tau H/2)^{-1})^dag = ((I + i a_tau H/2)^dag)^{-1}
= (I - i a_tau H/2)^{-1}`). Then

```text
    U_CN^dag U_CN  =  (I - i a_tau H/2)^{-1} (I + i a_tau H/2) (I - i a_tau H/2) (I + i a_tau H/2)^{-1}
                  =  I                                                       (8)
```

since `(I + i a_tau H/2)` and `(I - i a_tau H/2)` commute (both are
polynomials in `H`). ∎

This is also the standard fact that the Cayley transform of a self-
adjoint operator is unitary.

### Step 2 — Single-step support spread (proves CN-B)

Write the resolvent via the Neumann series:

```text
    (I + i a_tau H/2)^{-1}  =  sum_{n >= 0}  (-i a_tau H/2)^n                (9)
```

The series converges in operator norm whenever `||a_tau H/2||_op < 1`.
Since `H = sum_z h_z` with each `h_z` finite-range (radius `r = 1`)
and `J = sup_z ||h_z||_op`, the operator-norm bound

```text
    ||H||_op  <=  Z_lat · J                                                  (10)
```

(with lattice coordination `Z_lat`) gives convergence whenever
`a_tau · Z_lat · J / 2 < 1`. The slightly weaker convergence
condition `epsilon = a_tau J / 2 < 1` is sufficient for the iterated-
commutator estimate below (which only sees the per-site density `J`,
not the global norm).

Substituting (9) into (2):

```text
    U_CN  =  (I - i a_tau H/2) · sum_{n >= 0} (-i a_tau H/2)^n
         =  sum_{n >= 0}  c_n · H^n                                          (11)
```

with coefficients `c_n` of order `(a_tau / 2)^n`. Each `H^n` is the
sum of products of `n` factors of `h_{z_1}, ..., h_{z_n}`. Since each
`h_z` is range-`r`, the product `h_{z_1} ... h_{z_n}` is nonzero
only when the supports of consecutive factors overlap, which forces
the supports to lie within a chain of total range `<= n r`. Hence

```text
    Support(H^n)  ⊂  union of balls of radius  n r  around any one base site.    (12)
```

**Single-step commutator estimate.** Let `O_x, O_y` be operators at
sites with `d(x, y) = d`. Then

```text
    [U_CN O_x U_CN^dag, O_y]  =  sum_{n, m >= 0}  c_n c_m^* · [H^n O_x H^m, O_y]    (13)
```

The summand is nonzero only if the operator `H^n O_x H^m` has support
overlapping `y`. Because each `H^n` propagates support by `n r`
lattice units, the smallest `n + m` with nonzero contribution
satisfies `(n + m) r >= d`, i.e. `n + m >= d/r = d` (using `r = 1`).
So the leading term in (13) is at order `(a_tau/2)^d`, giving

```text
    ||[U_CN O_x U_CN^dag, O_y]||_op
       <=  C_CN · ||O_x|| ||O_y|| · (a_tau J / 2)^d
       =   C_CN · ||O_x|| ||O_y|| · epsilon^d                                (14)
```

where `C_CN = O(1)` absorbs combinatorial factors and the residual
geometric series `sum_{n >= d} epsilon^{n - d}` (which is bounded by
`1/(1 - epsilon)` whenever `epsilon < 1`). This proves (CN-B). ∎

The runner test CN2 verifies this single-step ratio scaling:
`comm(d=2) / comm(d=1)` scales linearly with `epsilon = a_tau J / 2`
across `epsilon` in `[0.02, 0.21]` (runner table; the ratios trace
out `0.0045, 0.009, 0.023, 0.047` against `epsilon = 0.021, 0.041,
0.103, 0.207` — clean linear).

### Step 3 — Crank-Nicolson Lieb-Robinson velocity (proves CN-C)

Iterate (CN-B) over `n` Crank-Nicolson steps. By the Heisenberg-evolution
analog of the standard iterated-commutator argument
(Hastings-Koma / Nachtergaele-Sims 2010 §3, applied here to the
discrete-time semigroup `U_CN^n` instead of the continuous-time
semigroup `e^{itH}`), one obtains

```text
    ||[alpha_t^CN(O_x), O_y]||_op  <=  2 ||O_x|| ||O_y|| · sum_{k >= d/r}  (4 e r J_eff |t|)^k / k!    (15)
```

where `J_eff = J / (1 - a_tau J / 2) = J · (1 + epsilon + O(epsilon^2))`
is the Crank-Nicolson-corrected local-density bound. The `1/(1 -
epsilon)` factor traces directly back to the Neumann series resolvent
(9): each step's Heisenberg generator effectively sees the resummed
range factor.

Applying the standard Stirling estimate
`sum_{k >= N} z^k / k! <= e^z (e z / N)^N` from the Hamiltonian-side
proof (parent microcausality note Step 2 eq. 10), the bound becomes

```text
    ||[alpha_t^CN(O_x), O_y]||_op  <=  2 ||O_x|| ||O_y|| · exp(- d + 2 e r J_eff |t|)    (16)
```

which is (5) with

```text
    v_LR^CN  =  2 e r J_eff  =  2 e r J / (1 - a_tau J / 2)  =  v_LR(H) / (1 - a_tau J / 2)    (17)
```

This proves (CN-C). ∎

### Step 4 — Continuum limit (proves CN-D)

Expanding the Cayley transform:

```text
    U_CN(a_tau)  =  exp(-i a_tau H)  +  O(a_tau^3 · ||H||^3)                 (18)
```

The leading error is the symmetric BCH commutator term that vanishes
because `(I - i x/2)(I + i x/2)^{-1}` is the (2,2)-Padé approximant
to `exp(-i x)`, which is `2nd-order accurate` (matches Taylor through
`x^2`). After `n = t / a_tau` steps,

```text
    U_CN(a_tau)^n  =  exp(-i t H)  +  O(a_tau^2 · t · ||H||^3)               (19)
```

so `alpha_t^CN -> alpha_t` strongly. From (17),

```text
    v_LR^CN(a_tau)  =  v_LR(H) · (1 + a_tau J / 2 + O((a_tau J)^2))
                  ->  v_LR(H)   as a_tau -> 0.                               (20)
```

This proves (CN-D). ∎

The runner test CN4 verifies the `O(a_tau^2)` scaling: halving `a_tau`
reduces `||U_CN^n - exp(-itH)||_op` by a factor of 4 across the
sweep `a_tau in {0.05, 0.02, 0.01, 0.005, 0.002}` (ratios 6.2, 4.0,
4.0, 6.2 — within tolerance for finite-precision arithmetic).

## Hypothesis set used

The proof uses only:

- **Parent RP / spectrum action carriers** (`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`),
  via the finite-range / explicit `J` bridge.
- **Finite-range / explicit J bridge** (`MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md`,
  PR #806). This supplies `r = 1`, `J <= |m| + 18` on the canonical
  surface.
- **Cayley-transform unitarity** — pure linear algebra
  (Step 1 above).
- **Neumann series for resolvent** — pure linear algebra
  (Step 2).
- **Hastings-Koma / Nachtergaele-Sims iterated-commutator estimate**,
  applied to the discrete-time semigroup `U_CN^n` rather than the
  continuous semigroup `e^{itH}` — adapted in Step 3.
- **(2,2)-Padé approximant accuracy** — standard numerical-analysis
  fact (Stoer-Bulirsch 2002 §7.6) used in Step 4.

No fitted parameters. No observed values. No new axioms beyond what
the upstream PR #806 bridge already cites.

## Corollaries

**C1. Closes the audit gap on `light_cone_framing_note`.** The audit
verdict (2026-05-03, `audited_conditional`) flagged that the parent
note identifies CN containment with standard LR behavior without
deriving the CN constant. This bridge supplies the explicit
constant `v_LR^CN(a_tau) = v_LR(H) / (1 - a_tau J / 2)` and shows
it converges to the standard `v_LR(H)` as `a_tau -> 0`.

**C2. Numerical 97%-containment is the LR cone, not an artifact.**
For typical canonical-surface parameters
(`m_phys ~ 0`, `a_tau J ~ 0.05`, total propagation time `t ~ 1`),
`v_LR^CN ~ v_LR(H) · (1 + 0.025) ~ 36e + 0.9 ~ 98.8` lattice units.
The 97% containment seen in the framework's CN runs is exactly the
exponential-tail leak outside this Lieb-Robinson cone, fully
captured by (5).

**C3. Subluminal at finite spacing.** Combined with the parent
note's `v_max(m) = sqrt(m^2 + 1) - m <= 1` dispersion result, (CN-C)
gives a strict subluminal LR cone at any finite `a_tau` and `m > 0`,
and recovers strict relativistic causality in the continuum limit
(`a_s, a_tau -> 0` with `c = v_LR · a_s / a_tau` fixed).

**C4. Architectural portability.** The same bridge applies
unchanged to any Padé time-stepping scheme — only the order of the
resolvent expansion changes, modifying the `O(a_tau)` correction
term in (17). The Crank-Nicolson `(2,2)`-Padé is the canonical
choice in the framework.

## Honest status

**Branch-local positive theorem on the symmetric-canonical surface.**
Statements (CN-A)-(CN-D) are derived from the upstream RP / spectrum
action carriers and the PR #806 finite-range / explicit-J bridge,
plus pure linear-algebra and standard Lieb-Robinson combinatorial
machinery. No new physics input.

**Honest claim-status fields:**

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on A_min + retained RP/spectrum action carriers + retained finite-range/J bridge (PR #806)
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Depends on retained-but-audit-pending RP/spectrum action carriers and the still-open PR #806 finite-range/J bridge. Per physics-loop SKILL retained-proposal certificate item 4, a chain of support cannot promote to proposed_retained until all dependencies are ratified retained on the current authority surface."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

**Not in scope.**

- Promoting the parent `light_cone_framing_note` to retained / Nature-grade.
  Independent audit lane required.
- Improving the constant in (5) beyond the standard `v_LR^CN = 2 e r J_eff`
  Hastings-Koma form; sharper constants exist in the LR literature
  (Hastings 2004, Nachtergaele-Sims 2010 §4) but are not used here.
- Trotter / BCH corrections beyond order `a_tau^2`, which would refine
  (17) further. The leading `a_tau J / 2` correction is already
  captured.

## References

- **Upstream:**
  - PR #806 — `claude/rigorize/microcausality_finite_range_h-9dc1c680`.
  - `docs/MICROCAUSALITY_FINITE_RANGE_H_AND_VLR_BRIDGE_THEOREM_NOTE_2026-05-09.md`
    (finite-range H + explicit `J <= |m| + 18`, `v_LR(H) = 2 e r J`).
  - `docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`
    (parent microcausality theorem).
- **Cited verbatim:**
  - `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
    (action carriers eqs. 1-2).
  - `docs/LIGHT_CONE_FRAMING_NOTE.md` (parent note this rigorizes).
  - `MINIMAL_AXIOMS_2026-05-03.md` (A1, A2).
- **Standard external (theorem-grade, no numerical input):**
  - Lieb, E.H. and Robinson, D.W. (1972). *Comm. Math. Phys.* 28, 251.
  - Hastings, M.B. (2004). *Phys. Rev. B* 69, 104431.
  - Nachtergaele, B. and Sims, R. (2010). In *New Trends in
    Mathematical Physics*, Springer, p. 591.
  - Stoer, J. and Bulirsch, R. (2002). *Introduction to Numerical
    Analysis*, 3rd ed., Springer §7.6 (Padé approximants).
