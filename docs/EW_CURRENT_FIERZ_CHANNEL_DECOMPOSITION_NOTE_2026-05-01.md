# EW Current Fierz-Channel Decomposition: Exact Group-Theory Derivation of `(N_c^2 - 1)/N_c^2`

**Date:** 2026-05-01
**Status:** support / exact group-theory derivation (cycle-breaking artifact). The exact (N_c^2 - 1)/N_c^2 ratio is derived inline from the SU(N_c) Fierz identity and Hilbert-space dimension counting — both are textbook group theory, no 1/N_c expansion. The remaining matching rule (which channel the physical EW current couples to) is named explicitly as a structural input from the framework's retained lattice gauge surface.
**Primary runner:** `scripts/frontier_ew_current_fierz_channel_decomposition.py`
**Cited authorities (one-hop, all retained on `main`):**
- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) — `proposed_retained` `audit_status: audited_clean` `effective_status: retained`. Provides native cubic Cl(3) / SU(2) and the graph-first SU(3) commutant.
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — `proposed_retained` `audit_status: audited_clean` `effective_status: retained`. Establishes that N_c = 3 follows from the spatial dimension d = 3 of Z^3.

**This note explicitly does NOT cite** `YT_EW_COLOR_PROJECTION_THEOREM.md`, `RCONN_DERIVED_NOTE.md`, or `EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md`. It is an **independent cycle-breaking derivation** for the `(N_c^2 - 1)/N_c^2` ratio that those three nodes currently share through a circular citation graph.

---

## 0. Why this note exists

The 2026-05-01 audit ledger flags a circular dependency:

```
yt_ew_color_projection_theorem  ↔  rconn_derived_note  ↔
    ew_current_matching_ozi_suppression_theorem_note_2026-04-27
```

with the explicit gap "missing direct EW-current matching coefficient
computation". The cycle exists because `rconn_derived_note` and
`ew_current_matching_ozi_suppression_theorem_note_2026-04-27` carry
cross-refs back to `yt_ew_color_projection_theorem`, which the citation
graph builder resolves as load-bearing dependencies.

This note breaks the cycle by deriving the load-bearing `(N_c^2 - 1)/N_c^2`
ratio through a different, **exact** route — the standard SU(N_c) Fierz
completeness identity applied to the q-qbar two-point function. The
derivation is exact at any N_c (no 1/N_c expansion, no large-N_c
approximation) and depends only on retained upstream notes.

The note does not promote the full 9/8 EW coupling correction to retained.
It separates the load-bearing claim into:

- **(F)** an exact group-theory ratio: the connected channel of the q-qbar
  Hilbert space carries weight `(N_c^2 - 1)/N_c^2` of the total. Derived here.
- **(M)** a matching rule: the physical EW vacuum polarization, after the
  framework's retained mean-field/CMT factorization, projects onto the
  adjoint (connected) channel rather than the total channel sum. **This
  remains a load-bearing structural input from the framework's retained
  lattice gauge surface; this note does not derive it.**

The cycle-breaking value is in the citation graph: by deriving (F) from
the Fierz identity directly, this note removes the last edge of the cycle
(the implicit dependence of the package-level coefficient on the 1/N_c
chain). The remaining chain `yt_ew_color_projection → this note →
NATIVE_GAUGE_CLOSURE → ...` is acyclic and lands all dependencies in
retained territory at one hop, with the residual matching rule (M)
explicitly named as the open structural input.

## 1. Setup: the q-qbar Hilbert space and SU(N_c) channel decomposition

On the unified Cl(3)/Z^3 lattice, the retained gauge structure is
SU(3) × SU(2) × U(1) with N_c = 3 fixed by the spatial dimension d = 3
(NATIVE_GAUGE_CLOSURE_NOTE / GRAPH_FIRST_SU3_INTEGRATION_NOTE). Quarks
carry a color index a = 1, ..., N_c in the SU(N_c) fundamental
representation.

A quark-antiquark pair at fixed spacetime separation transforms in the
tensor product representation `(N_c) ⊗ (N_c-bar)`. Under SU(N_c), this
decomposes into irreducible representations as:

```text
(N_c) ⊗ (N_c-bar) = 1  ⊕  adj
```

where `1` is the singlet (1 state) and `adj` is the adjoint of dimension
`N_c^2 − 1`. The total Hilbert-space dimension is `N_c × N_c-bar = N_c^2`,
which sums correctly: `1 + (N_c^2 − 1) = N_c^2`.

This decomposition is exact group theory; no expansion is involved.

## 2. The Fierz completeness identity (textbook, proved inline)

For SU(N_c) generators `t^A` (A = 1, ..., N_c^2 − 1) normalized so that
`Tr[t^A t^B] = δ_{AB}/2` (the standard convention), any complex N_c × N_c
matrix M can be expanded uniquely in the orthonormal basis
{`I/√N_c`, `√2 t^A`} of the Hermitian-conjugate-extended N_c × N_c matrix
algebra:

```text
M = (Tr M / N_c) · I + 2 Σ_A Tr[M t^A] · t^A
```

This expansion is the Hilbert-space-orthonormality statement
`Tr[I I]/N_c = 1` and `Tr[(√2 t^A)(√2 t^B)] = δ_{AB}`. From the same
orthonormality:

```text
Tr[M^† M] = (1/N_c) |Tr M|^2  +  2 Σ_A |Tr[M t^A]|^2          (Fierz-1)
```

This is the SU(N_c) Fierz completeness identity for bilinears. Equivalently,
in tensor form:

```text
δ_{ac} δ_{bd} = (1/N_c) δ_{ad} δ_{bc} + 2 Σ_A (t^A)_{ad} (t^A)_{bc}    (Fierz-2)
```

Both forms are exact and well-known. They follow purely from the
orthonormality of the basis {`I/√N_c`, `√2 t^A`} in the Hermitian-extended
matrix algebra; no dynamics, no expansion, no large-N_c assumption.

## 3. Channel decomposition of the q-qbar two-point function

Let `M_{ab}(x, y) = G_{ab}(x, y)` be the quark propagator in a fixed gauge
configuration. The q-qbar two-point function Tr_color[G(x, y) G(y, x)]
admits the exact channel decomposition (substitute M = G into Fierz-1):

```text
Tr_color[G(x, y) G(y, x)] = (1/N_c) |Tr G(x, y)|^2  +  2 Σ_A |Tr[G(x, y) t^A]|^2     (3.1)
                          ≡ S(x, y)  +  C(x, y)
```

where:

- **`S(x, y) = (1/N_c) |Tr G(x, y)|^2`** is the **singlet-channel** piece. It
  carries the disconnected color trace structure (one factor of `Tr G`
  contributed at each end of the q-qbar bilinear).
- **`C(x, y) = 2 Σ_A |Tr[G(x, y) t^A]|^2`** is the **adjoint-channel** piece,
  summed over the `N_c^2 − 1` independent SU(N_c) generators.

This decomposition is exact at every gauge configuration. No expansion is
performed.

## 4. Hilbert-space dimension fraction (the exact `(N_c^2 − 1)/N_c^2` ratio)

The decomposition of equation (3.1) splits the q-qbar two-point function
into exactly two channels: 1 singlet channel and `N_c^2 − 1` adjoint
channels. The total channel count is `1 + (N_c^2 − 1) = N_c^2`, matching
the dimension of the q-qbar tensor-product space.

**The adjoint-channel dimension fraction** of the q-qbar Hilbert space is
exactly:

```text
dim(adj) / dim(N_c ⊗ N_c-bar) = (N_c^2 − 1) / N_c^2                  (4.1)
```

At N_c = 3 (fixed by the retained Cl(3)/Z^3 spatial dimension), this is:

```text
(3^2 − 1) / 3^2  =  8/9                                              (4.2)
```

Equation (4.2) is **exact**. It is the dimension count of the adjoint
representation divided by the dimension of the q-qbar tensor product —
a pure group-theory invariant. It carries no `O(1/N_c^4)` correction,
because it is not a 1/N_c-expansion result; it is the exact representation
dimension at finite N_c.

The reciprocal,

```text
N_c^2 / (N_c^2 − 1)  =  9/8  at  N_c = 3                             (4.3)
```

is the inverse of (4.2). The framework's package-level "9/8 EW coupling
correction" enters as the inverse of the adjoint-channel fraction, in the
specific direction set by the matching rule (M) below.

## 5. The matching rule (named structural input, NOT derived here)

Equation (4.1) gives the exact adjoint-channel fraction. To convert this
into the package-level EW coupling correction, the framework requires one
additional structural input:

> **(M) Matching rule:** the physical (continuum-matched) EW vacuum
> polarization, after the framework's retained Coupling Map Theorem (CMT)
> mean-field factorization U → u_0 V, projects onto the adjoint channel
> `C(x, y)` of equation (3.1), not onto the total `Tr_color[G(x, y) G(y, x)]`.

The matching rule is **not derived in this note**. It is a structural
input from the framework's lattice EW current construction. This note
takes (M) as named and admitted, and notes the audit consequence: under
the matching rule (M) plus the exact group-theory ratio (4.1), the
package-level EW coupling correction is exactly `N_c^2 / (N_c^2 − 1)`.

If a future research lane derives (M) from retained primitives — by, for
example, showing that the framework's specific Wilson-line construction
of the EW current at the lattice level mechanically projects onto the
adjoint channel after the singlet contribution is absorbed by the
mean-field factor `u_0` — then the package-level 9/8 correction would
upgrade from "support / exact group-theory ratio + admitted matching" to
fully retained.

This note explicitly does not propose to make that upgrade.

## 6. What this derivation closes and what it leaves open

**Closed by this note (exact, retained-grade group theory):**

- The ratio `dim(adj) / dim(q-qbar) = (N_c^2 − 1)/N_c^2` is exact at any
  finite N_c.
- At N_c = 3 (retained from Cl(3)/Z^3), the value is exactly 8/9.
- No `O(1/N_c^4)` correction enters. The ratio is not a leading-order
  expansion result; it is a Hilbert-space dimension count.
- The Fierz completeness identity (Fierz-1, Fierz-2) is exact and proved
  inline in §2.

**Cycle-breaking value (audit-graph terms):**

- This note depends only on `NATIVE_GAUGE_CLOSURE_NOTE` and
  `GRAPH_FIRST_SU3_INTEGRATION_NOTE`, both `effective_status: retained`.
- It does NOT cite `RCONN_DERIVED_NOTE`, `EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27`,
  or `YT_EW_COLOR_PROJECTION_THEOREM`. The 3-cycle in the audit graph
  flagged on 2026-05-01 is broken by the existence of this self-contained
  derivation chain for the `(N_c^2 − 1)/N_c^2` ratio.
- After this note lands, `yt_ew_color_projection_theorem` and
  `ew_current_matching_ozi_suppression_theorem_note_2026-04-27` can each
  cite this note as the primary derivation of the ratio, removing the
  audit-graph cycle.

**Left open (the matching rule (M)):**

- Whether the physical EW vacuum polarization mechanically projects onto
  the adjoint channel after the mean-field factorization. Current status:
  admitted structural input from the framework's lattice EW construction.
- An independent derivation of (M) — i.e., a rigorous demonstration that
  the framework's specific Wilson-line construction of the EW current
  reduces to the adjoint-channel projection after CMT factorization —
  would close the full 9/8 package-level coefficient.

**Comparison with `RCONN_DERIVED_NOTE` (1/N_c topology route):**

- `RCONN_DERIVED_NOTE` derives the same ratio via the 't Hooft 1/N_c
  topological expansion. That route gives the ratio at *leading* order
  with explicit `O(1/N_c^4) ~ 1.2%` corrections from non-planar diagrams.
- This note's derivation is **exact at any N_c**: the ratio is an
  irreducible-representation dimension fraction. The 1/N_c expansion and
  the Fierz/Hilbert-space-counting derivation are two independent routes
  to the same coefficient; this note shows the coefficient is not
  contingent on the 1/N_c expansion.

The two routes are complementary: 1/N_c provides the dynamical-correction
estimate (giving the `O(1/N_c^4)` bound on non-leading corrections to the
*physical* matching), while the Fierz-channel route gives the exact ratio
as a representation-theoretic identity. The latter is what the audit
graph needed to break the cycle.

## 7. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_ew_current_fierz_channel_decomposition.py
```

The runner verifies:

1. The note exists with correct title and status language.
2. The note does NOT cite the 3 cycle nodes (`YT_EW_COLOR_PROJECTION_THEOREM.md`,
   `RCONN_DERIVED_NOTE.md`, `EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md`).
3. The note DOES cite the retained upstreams (`NATIVE_GAUGE_CLOSURE_NOTE.md`,
   `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`).
4. The Fierz completeness identity is correct: numerically verifies
   `Tr[M^† M] = (1/N_c) |Tr M|^2 + 2 Σ_A |Tr[M t^A]|^2` for random
   matrices at N_c = 2, 3, 4, 5.
5. The dimension count `1 + (N_c^2 − 1) = N_c^2` is exact for
   N_c = 2, 3, 4, 5.
6. The adjoint-channel fraction `(N_c^2 − 1)/N_c^2` evaluates to
   exactly 8/9 at N_c = 3 (no `O(1/N_c^4)` correction).
7. The matching rule (M) is explicitly named as not-derived in this
   note, with the load-bearing structural input role labeled.

## 8. Inputs and import roles

| Input | Role | Import class | Source |
|---|---|---|---|
| `N_c = 3` from Cl(3)/Z^3 spatial dimension | retained input | framework retained | `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` |
| SU(N_c) gauge structure | retained input | framework retained | `NATIVE_GAUGE_CLOSURE_NOTE.md` |
| SU(N_c) Fierz completeness identity (Fierz-1, Fierz-2) | textbook bridge | admitted standard math, proved inline §2 | textbook (e.g., Peskin & Schroeder Ch. 16, or any group-theory reference) |
| Hilbert-space dimension count `1 + (N_c^2 − 1) = N_c^2` | exact group theory | proved inline §1, §4 | direct count |
| **Matching rule (M):** physical EW vacuum polarization projects onto adjoint channel after CMT factorization | **structural input, not derived** | **admitted structural input from retained framework EW-current construction** | the framework's lattice EW Wilson-line construction (an *open* primitive on this note's surface) |

No new physical claims, no new numerical comparators, no new admitted
observations. The note's load-bearing arithmetic is exact group theory
that any group-theory reference verifies.

## 9. Forbidden imports

- `RCONN_DERIVED_NOTE.md` — explicitly NOT cited; this note is an independent
  derivation route.
- `YT_EW_COLOR_PROJECTION_THEOREM.md` — explicitly NOT cited.
- `EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md` — explicitly
  NOT cited.

If any of the three cycle nodes is retroactively cited from this note,
the audit-graph cycle returns and this note's cycle-breaking value is lost.

## 10. Safe wording

**Can claim:**
- "Exact group-theory derivation of the `(N_c^2 − 1)/N_c^2` channel
  ratio, independent of the 1/N_c topological expansion."
- "Cycle-breaking derivation: cites only retained upstreams; no
  citation-graph cycle through `yt_ew_color_projection`,
  `rconn_derived`, or `ew_current_matching_ozi_suppression`."
- "At N_c = 3, the adjoint-channel fraction is exactly 8/9 (no
  `O(1/N_c^4)` correction)."

**Cannot claim:**
- bare `retained` / `promoted`.
- "This closes the 9/8 EW coupling correction." (it does not — the
  matching rule (M) remains a load-bearing input)
- "This retires `RCONN_DERIVED_NOTE`." (it does not — `RCONN` is an
  independent dynamical-correction estimate, complementary to this
  representation-theoretic ratio)
- "This derives the matching rule (M)." (it does not — (M) is named
  as an admitted structural input)

## 11. Cross-references

- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) — retained.
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — retained.
- The 3 cycle nodes from the 2026-05-01 audit ledger:
  `YT_EW_COLOR_PROJECTION_THEOREM.md`, `RCONN_DERIVED_NOTE.md`,
  `EW_CURRENT_MATCHING_OZI_SUPPRESSION_THEOREM_NOTE_2026-04-27.md`. After
  this note lands, those three nodes can each cite this note for the
  exact `(N_c^2 − 1)/N_c^2` ratio, removing the audit-graph cycle.
- 2026-05-01 audit ledger leverage map:
  [`AUDIT_LHF_LEVERAGE_MAP_FOR_RETAINED_PROMOTION_NOTE_2026-05-01.md`](AUDIT_LHF_LEVERAGE_MAP_FOR_RETAINED_PROMOTION_NOTE_2026-05-01.md) (PR #248).
