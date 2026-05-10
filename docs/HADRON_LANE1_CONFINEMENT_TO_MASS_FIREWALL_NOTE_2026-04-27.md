# Hadron Lane 1 Confinement-To-Mass Firewall

**Date:** 2026-04-27
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** (1) staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`); (2) g_bare = 1 derivation target (canonical parent: [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md)).
**Status:** proposed_retained exact negative boundary for Lane 1 dependency
accounting. This is not a retained derivation of `m_pi`, `m_p`, `m_n`, or the
hadron spectrum.
**Script:** `scripts/frontier_hadron_lane1_confinement_to_mass_firewall.py`
**Lane:** Lane 1 hadron mass program

## Question

Can retained confinement plus the current bounded string-tension readout be
promoted to retained hadron masses?

## Result

No.

The current package has an important structural result:

```text
graph-first SU(3) gauge sector confines at T = 0
```

and a bounded quantitative readout:

```text
sqrt(sigma) ~= 465 MeV
```

But confinement and one bounded scale do not determine the pion, proton,
neutron, or hadron spectrum. They are prerequisites for hadron physics, not
mass-spectrum closure.

## Theorem

**Theorem (Lane 1 confinement-to-mass firewall).** Adopt the current hadron
surface: retained structural confinement, retained `alpha_s(M_Z)`, bounded
`sqrt(sigma)`, and the current Lane 3 quark-mass status.

Then no retained hadron-mass closure follows unless the branch also supplies:

1. retained light-quark masses and chiral inputs for `m_pi` through GMOR;
2. retained hadronic-scale running/matching and standard correlator extraction
   for `m_p` and `m_n`;
3. retained dimensionless spectral coefficients for each hadron family, or an
   ab-initio lattice-QCD-equivalent computation that produces them.

Absent those premises, `sqrt(sigma)` can be used only as a bounded scale
comparator or support input.

## Why One Scale Is Not A Spectrum

If `sqrt(sigma)` is known, every hadron mass still has the form

```text
m_H = c_H * sqrt(sigma)
```

where `c_H` is a dimensionless spectral coefficient depending on quark masses,
chiral dynamics, spin/flavor structure, and the hadron channel. The current
framework does not retain those `c_H`.

Using the current bounded central scale `sqrt(sigma) = 465 MeV`:

```text
c_pi ~= 0.29
c_p  ~= 2.02
```

These coefficients are very different and are not fixed by confinement alone.

## Pion Gate

The clean first target is GMOR:

```text
m_pi^2 f_pi^2 = (m_u + m_d) Sigma
```

The current package does not retain `m_u`, `m_d`, `f_pi`, or the chiral
condensate `Sigma`. Lane 3 currently blocks the light-quark mass side; the
chiral-SB side remains a Lane 1 target.

## Proton / Neutron Gate

Standard lattice QCD can compute `m_p` and `m_n` from a retained action,
retained quark masses, hadronic-scale coupling/matching, and correlator
extraction. The current framework has useful pieces, but not the full retained
calculation. In particular:

- Lane 3 has not retained `m_u` or `m_d`;
- `alpha_s(M_Z)` is retained, but hadronic-scale running/matching is a
  separate bridge;
- no retained nucleon correlator extraction or spectral coefficient has landed.

## What This Retires

This retires three fast-but-wrong upgrades:

```text
confinement => retained hadron masses
```

```text
bounded sqrt(sigma) => retained m_pi or m_p
```

```text
standard lattice-QCD methodology exists => framework has derived m_p
```

## What Remains Open

Lane 1 remains open. The exact next gates are:

- Lane 3 light-quark mass retention;
- chiral condensate and pion decay constant retention for GMOR;
- hadronic-scale `alpha_s` running/matching;
- lattice-QCD-equivalent correlator extraction and dimensionless spectral
  coefficients for nucleons and the wider hadron spectrum;
- tightening `sqrt(sigma)` from bounded to retained if it is to be used as a
  load-bearing scale.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_confinement_to_mass_firewall.py
```

Expected result:

```text
PASS=16 FAIL=0
```

Focused support runner:

```bash
PYTHONPATH=scripts python3 scripts/frontier_confinement_string_tension.py
```

## Inputs And Import Roles

| Input | Role | Import class | Source |
|---|---|---|---|
| confinement at `T=0` | structural prerequisite for bound hadrons | retained structural theorem | `CONFINEMENT_STRING_TENSION_NOTE.md` |
| `sqrt(sigma) ~= 465 MeV` | bounded scale comparator | bounded bridge | `CONFINEMENT_STRING_TENSION_NOTE.md` |
| `alpha_s(M_Z)=0.1181` | retained high-scale coupling | retained quantitative lane | `ALPHA_S_DERIVED_NOTE.md` |
| light quark masses | GMOR and nucleon inputs | open dependency | Lane 3 firewall |
| `m_pi`, `m_p` observed values | numerical sensitivity examples only | comparator | standard hadron values |

No observed hadron mass is used as a derivation input in this note. Observed
values are used only to expose the dimensionless coefficients that remain
unretained.

## Safe Wording

Can claim:

- Lane 1 has an executable firewall between confinement/string-tension support
  and hadron-mass retention;
- current confinement support is necessary but not sufficient;
- `sqrt(sigma)` is a bounded scale readout, not a hadron spectrum;
- `m_pi` and `m_p` remain open until the listed gates land.

Cannot claim:

- pion, proton, neutron, or hadron spectrum masses are retained;
- confinement alone derives hadron masses;
- bounded `sqrt(sigma)` closes GMOR or nucleon spectroscopy;
- standard lattice-QCD methodology by itself counts as a framework derivation.


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on **both** open gates:

1. **Staggered-Dirac realization derivation target** — canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`); in-flight supporting work: `PHYSICAL_LATTICE_NECESSITY_NOTE.md`, `THREE_GENERATION_STRUCTURE_NOTE.md`, `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, `scripts/frontier_generation_rooting_undefined.py`, `GENERATION_AXIOM_BOUNDARY_NOTE.md`.
2. **`g_bare = 1` derivation target** — canonical parent: [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md) (`claim_type: positive_theorem`, `audit_status: audited_conditional`); in-flight supporting work: `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`, `G_BARE_RIGIDITY_THEOREM_NOTE.md`, `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`, `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`, `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`, `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md`, `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`.

The note produces (or directly supports) a quantitative gauge prediction (Wilson plaquette content, `α_s`, `v`, `sin²θ_W`, `m_t`, `m_H`, `g_1`, `g_2`, `β = 6`, CKM/quark/hadron mass hierarchy, action-unit metrology, etc.) by fixing `g_bare = 1` without independently deriving it — therefore both gates must close for the lane to upgrade.

Therefore `claim_type: bounded_theorem` until both gates close. When both gates close, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
