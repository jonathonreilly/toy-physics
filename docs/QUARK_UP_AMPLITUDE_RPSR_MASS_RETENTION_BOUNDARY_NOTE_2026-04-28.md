# Quark Up-Amplitude RPSR Mass-Retention Boundary Note

**Date:** 2026-04-28

**Status:** exact support/boundary theorem for Lane 3 target 3B. This
block-10 artifact audits the existing STRC/RPSR up-amplitude theorem as a
constructive retained support surface, and separates it from retained
non-top quark mass closure. It does not claim retained `m_u`, `m_c`, or any
other non-top quark mass.

**Primary runner:**
`scripts/frontier_quark_up_amplitude_rpsr_mass_retention_boundary.py`

## 1. Question

Lane 3 priority includes a hard route:

```text
3B up-type amplitude scalar law derivation.
```

The repo already contains a strong same-day up-amplitude package:

- `STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md` derives the LO balance
  on the exact `1(+)5` carrier;
- `QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md` assembles
  the LO+NLO RPSR amplitude;
- `QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md` carries the retained
  projector parameters.

This block asks:

```text
What exactly does this existing 3B package retain, and what is still missing
before it can count as retained m_u/m_c/m_t or m_u/m_c, m_c/m_t closure?
```

## 2. Minimal Premise Set

Allowed premises:

1. retained unit projector ray
   `p = cos_d + i sin_d`, with `cos_d = 1/sqrt(6)` and
   `sin_d = sqrt(5/6)`;
2. retained scalar comparison ray `r = p/sqrt(7)`;
3. retained down-sector reduced amplitude `a_d = rho = 1/sqrt(42)`;
4. retained support bridge `supp = 6/7`;
5. retained democratic center-excess `delta_A1 = 1/42`;
6. STRC/RPSR theorem surfaces already in the repo.

Forbidden proof inputs:

1. observed quark masses;
2. fitted Yukawa entries;
3. CKM mixing data treated as mass eigenvalues;
4. treating the reduced amplitude `a_u` as a mass ratio without a retained
   amplitude-to-Yukawa readout theorem;
5. using top-Ward normalization as species-uniform non-top closure.

## 3. Exact Up-Amplitude Support

The LO theorem gives:

```text
a_u_LO + rho * sin_d = sin_d
a_u_LO = sin_d * (1 - rho).
```

The RPSR NLO assembly gives:

```text
a_u / sin_d + rho = 1 + rho / 49
a_u = sin_d * (1 - 48 rho / 49)
    = sqrt(5/6) * (1 - 48/(49 sqrt(42))).
```

This is an exact retained algebraic amplitude on the reduced projector ray.
It is valuable 3B support.

## 4. Boundary To Mass Retention

The theorem variable `a_u` is a reduced amplitude on the `1(+)5` projector
carrier. It is not, by itself:

```text
m_u/m_c,
m_c/m_t,
y_u/y_c,
y_c/y_t,
or an absolute non-top Yukawa.
```

To become mass retention, the package still needs a typed readout theorem:

```text
RPSR reduced amplitude a_u
=> physical up-sector Yukawa eigenvalue ratios.
```

It also needs species/scale anchoring compatible with the top Ward theorem
without reusing top normalization species-uniformly.

## 5. Theorem

**Theorem (up-amplitude RPSR mass-retention boundary).** The existing
STRC/RPSR package supplies exact retained support for a 3B up-sector reduced
amplitude scalar law on the physical `1(+)5` projector carrier:

```text
a_u = sqrt(5/6) * (1 - 48/(49 sqrt(42))).
```

However, the current Lane 3 support bank does not contain a typed readout edge
from this reduced amplitude to physical up-type Yukawa eigenvalue ratios or
absolute non-top masses. Therefore RPSR is retained amplitude support, not
retained `m_u` or `m_c` mass closure.

## 6. What This Retires

This retires the direct promotion:

```text
RPSR reduced amplitude a_u
=> retained m_u/m_c or m_c/m_t.
```

The amplitude theorem is real support. The amplitude-to-Yukawa readout remains
load-bearing.

## 7. What Remains Open

Lane 3 remains open. A future 3B route can reopen mass retention by supplying:

1. a retained readout theorem from the `1(+)5` reduced amplitude to up-type
   Yukawa eigenvalue ratios;
2. a retained sector/scale bridge tying that readout to the top Ward anchor;
3. a proof that the same readout is compatible with the existing CKM and 3C
   generation-source boundaries;
4. an exact no-go showing the RPSR amplitude cannot be a mass-ratio source
   under admissible Lane 3 readouts.

## 8. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_up_amplitude_rpsr_mass_retention_boundary.py
```

Expected result:

```text
TOTAL: PASS=50, FAIL=0
VERDICT: RPSR is exact up-amplitude support, not retained up-quark mass
closure without a new readout theorem.
```
