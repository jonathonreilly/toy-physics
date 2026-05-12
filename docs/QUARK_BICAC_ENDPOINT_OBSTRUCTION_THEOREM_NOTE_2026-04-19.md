# Quark BICAC Endpoint Obstruction Theorem

**Date:** 2026-04-19  
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).
**Lane:** Quark up-amplitude.  
**Status:** **proposed_retained obstruction theorem on the ray/support-only packet.**
That narrower packet does **not** derive BICAC. It supports a positive-width
bridge interval of exact candidate amplitudes, and BICAC is only one endpoint
of that interval. Later same-day shell-normalization work adds exact carrier
input that bypasses this obstruction at the physical LO point.

**Primary runner:** `scripts/frontier_quark_bicac_endpoint_obstruction_theorem.py`

---

## 0. Executive summary

The current quark packet already contains three exact bridge points:

1. **Support endpoint**

       kappa_support = sqrt(supp) = sqrt(6/7),
       a_u = sin_d * (1 - rho * sqrt(supp)) = sin_d * 6/7.

2. **Retained full target**

       kappa_target = 1 - supp * delta_A1 = 48/49,
       a_u = sin_d * (1 - 48 rho / 49) = 0.7748865611...

3. **BICAC / STRC-LO endpoint**

       kappa_BICAC = 1,
       a_u = sin_d * (1 - rho),
       a_u + rho * sin_d = sin_d.

All three sit on the exact bridge family

    a_u(kappa) = sin_d * (1 - rho * kappa),
    kappa in [sqrt(6/7), 1].

Every retained ray/support identity currently in hand is `kappa`-independent:
`|p|^2 = 1`, `r = p/sqrt(7)`, `a_d = rho`, `supp = 6/7`,
`delta_A1 = 1/42`, and the collinearity cross-identity
`Re(p) Im(r) = Im(p) Re(r)`.

Therefore the ray/support-only packet does **not** force `kappa = 1`. BICAC
remains an endpoint-selection principle on that narrower data set. The later
shell-normalization theorem changes the branch status by adding exact
`kappa`-sensitive carrier normalization data not used here.

---

## 1. Retained inputs

| Symbol | Value | Role |
|---|---|---|
| `p = cos_d + i sin_d` | `cos_d = 1/sqrt(6)`, `sin_d = sqrt(5/6)` | retained unit projector ray |
| `r = rho + i eta = p/sqrt(7)` | `rho = 1/sqrt(42)`, `eta = sqrt(5/42)` | retained scalar comparison ray |
| `a_d = rho = Re(r)` | `1/sqrt(42)` | retained down amplitude |
| `supp` | `6/7` | retained support bridge |
| `delta_A1` | `1/42` | retained democratic center-excess |
| `supp * delta_A1` | `1/49` | retained NLO contraction |

Two exact identities are the key algebraic links:

    rho * sqrt(supp) = 1/7,
    1 - supp * delta_A1 = 48/49.

The first gives the support endpoint; the second gives the retained full
target bridge factor.

---

## 2. The theorem

> **Theorem (BICAC endpoint obstruction).** Let
>
>     a_u(kappa) = Im(p) * (1 - Re(r) * kappa) = sin_d * (1 - rho * kappa),
>
> with retained atoms `p`, `r`, `a_d = rho`, `supp = 6/7`,
> `delta_A1 = 1/42`. Then:
>
> 1. `kappa_support = sqrt(supp)` gives
>    `a_u = sin_d * supp`.
> 2. `kappa_target = 1 - supp * delta_A1 = 48/49` gives
>    `a_u = sin_d * (1 - 48 rho / 49) = 0.7748865611...`.
> 3. `kappa_BICAC = 1` gives
>    `a_u = sin_d * (1 - rho)` and hence `a_u + rho * sin_d = sin_d`.
> 4. All retained ray/support identities in the present packet are
>    independent of `kappa`.
>
> Since
>
>     sqrt(6/7)  <  48/49  <  1,
>
> the retained packet admits a positive-width bridge interval of exact
> candidate amplitudes and does not force the BICAC endpoint `kappa = 1`.

---

## 3. Proof

### 3.1 Support endpoint

From `rho = 1/sqrt(42)` and `supp = 6/7`,

    rho * sqrt(supp)
      = (1/sqrt(42)) * sqrt(6/7)
      = sqrt((1/42) * (6/7))
      = sqrt(1/49)
      = 1/7.

Therefore

    a_u(sqrt(supp))
      = sin_d * (1 - rho * sqrt(supp))
      = sin_d * (1 - 1/7)
      = sin_d * 6/7
      = sin_d * supp.

This is the exact support-native endpoint already present in the retained
quark package.

### 3.2 Full target point

The retained NLO contraction gives

    supp * delta_A1 = (6/7) * (1/42) = 1/49,

so

    kappa_target = 1 - supp * delta_A1 = 1 - 1/49 = 48/49.

Substituting into the bridge family:

    a_u(48/49) = sin_d * (1 - 48 rho / 49),

which is the retained full target

    a_u = 0.7748865611...

from the RPSR packet.

### 3.3 BICAC endpoint

Setting `kappa = 1` gives

    a_u(1) = sin_d * (1 - rho).

Hence

    a_u(1) + rho * sin_d = sin_d.

This is precisely STRC-LO / BICAC.

### 3.4 Why this is an obstruction theorem

The currently retained ray/support identities involve only the fixed packet

    p, r, a_d = rho, supp, delta_A1,

and do not contain `kappa`. In particular:

- `|p|^2 = 1`,
- `r = p/sqrt(7)`,
- `|r|^2 = 1/7`,
- `a_d = Re(r) = rho`,
- `Re(p) Im(r) = Im(p) Re(r)`,
- `supp = 6/7`,
- `supp * delta_A1 = 1/49`.

All remain true at `kappa = sqrt(6/7)`, `48/49`, and `1`.

These values are distinct:

    (48/49)^2 - 6/7 = 246/2401 > 0,
    1 - 48/49 = 1/49 > 0.

So

    sqrt(6/7) < 48/49 < 1.

The bridge interval has positive width

    1 - sqrt(6/7) > 0.

Therefore the current packet does not determine a unique `kappa`, and in
particular does not derive the BICAC endpoint. QED.

---

## 4. Consequence for the future bimodule theorem

This sharpens the earlier future-target note. The missing ingredient is not
another quadratic identity or another collinearity identity. The missing
ingredient is an **endpoint-selection theorem**:

> prove, from internal bimodule structure alone, that the bridge factor must
> equal `kappa = 1`.

Equivalently, any successful future derivation must collapse the current
interval

    kappa in [sqrt(6/7), 1]

to the BICAC endpoint.

That is a more precise mathematical target than the earlier generic phrase
"ray-saturation theorem": the theorem must supply a **linear saturation law**
that removes the `kappa` freedom.

---

## 5. What is retained now

Retained after this theorem:

- the exact bridge family `a_u(kappa) = sin_d * (1 - rho * kappa)`,
- the exact support endpoint `kappa = sqrt(6/7)`,
- the exact retained full-target point `kappa = 48/49`,
- the exact BICAC endpoint `kappa = 1`,
- the fact that the current packet leaves `kappa` unfixed.

Not retained:

- any derivation of `kappa = 1` from the current bimodule/ray packet,
- any claim that BICAC has already ceased to be a postulate.

---

## 6. Runner output summary

The companion runner verifies:

- support endpoint identity `rho * sqrt(supp) = 1/7`,
- target bridge factor `1 - supp * delta_A1 = 48/49`,
- full target `a_u = 0.7748865611`,
- BICAC endpoint STRC-LO closure,
- exact ordering `sqrt(6/7) < 48/49 < 1`,
- `kappa`-independence of the retained packet.

Expected runner status:

    PASS=12
    FAIL=0


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [staggered_dirac_realization_gate_note_2026-05-03](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
