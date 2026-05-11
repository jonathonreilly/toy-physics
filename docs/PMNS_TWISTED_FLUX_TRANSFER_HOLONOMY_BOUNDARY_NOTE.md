# PMNS Twisted Flux Transfer Holonomy Boundary
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).

**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_pmns_twisted_flux_transfer_holonomy_boundary.py`

## Question

Can a twisted transfer, flux insertion, or cycle-holonomy law on the
graph-first oriented-cycle frame select the remaining values of the retained
PMNS cycle channel?

## Answer

Partially.

On the canonical graph-first cycle frame `E12, E23, E31`, the flux-threaded
transfer kernel

```text
T(xbar, ybar, phi) = xbar I + ybar (e^{i phi} C + e^{-i phi} C^2)
```

has an exact holonomy/spectral value law:

```text
tr(T)/3 = xbar
tr(C^2 T)/3 = ybar e^{i phi}
```

so `xbar`, `ybar`, and `phi` are recovered exactly from the twisted transfer
data. This is a genuine axiom-native value law for the fluxed transfer carrier.

But the current exact bank still does not select the full reduced PMNS oriented
cycle family

```text
A_fwd(u, v, w) = (u + i v) E12 + w E23 + (u - i v) E31
```

with one flux holonomy alone. The one-angle holonomy probe has a 2-real kernel
on that reduced carrier, so it does not collapse the full reduced family to a
unique point.

## What This Buys

- The graph-first frame remains canonical.
- The flux-threaded transfer carrier now has an exact nontrivial value law.
- The retained PMNS reduced carrier is still not fully value-selected by a
  single holonomy probe.

## What Remains

Any further positive selection law would have to use genuinely new dynamics or
a further admitted extension beyond the current exact bank.

## Verification

```bash
python3 scripts/frontier_pmns_twisted_flux_transfer_holonomy_boundary.py
```



## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
