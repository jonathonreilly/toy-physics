# Yukawa Color-Singlet Projection Theorem

**Date:** 2026-04-14 (scope tightened 2026-05-02)
**Type:** positive_theorem (proposed; audit-lane to ratify)
**Claim scope:** the SU(N_c) Fierz channel decomposition giving channel
fraction `F_adjoint = (N_c² − 1)/N_c² = 8/9` at `N_c = 3` from
graph-visible primitives. The physical-Higgs-scalar
wave-function renormalization identification `Z_phi^{phys}/Z_phi^{lattice}
= R_conn` (and the resulting `sqrt(8/9)` y_t correction) is **explicitly
out of scope** — that is a separate downstream physical-matching theorem
(part of the lattice → physical matching cluster obstruction; see
prior campaign cycle 13 PR #274).
**Scoped graph dependencies:** the Fierz channel-fraction half is carried by
[`EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md),
[`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md), and
[`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md).
Historical physical-matching context below also references
`RCONN_DERIVED_NOTE.md` and `YT_EW_COLOR_PROJECTION_THEOREM.md`,
but that context is not part of this row's scoped claim.
**Script:** `scripts/frontier_ew_current_fierz_channel_decomposition.py`
**Supporting script:** `scripts/audit_companion_ew_fierz_general_n_c_exact.py`
These test the scoped Fierz channel-counting claim. The legacy
`scripts/frontier_yt_color_projection_correction.py` runner belongs to the
excluded physical-matching context, not to this row's narrowed claim.

## Out of scope: physical-Higgs-Z identification

The claim `Z_phi^{phys} / Z_phi^{lattice} = R_conn` and the resulting
`y_t^{phys} = y_t^{Ward} · sqrt(8/9)` correction are **separate downstream
physical-matching steps**. They identify a physical (continuum) wave-
function renormalization with a lattice color-trace fraction, which is the
class-(F) renaming step identified in prior review. This row's narrowed
load-bearing step is the **algebraic Fierz channel-fraction identity**
(class A on graph-visible primitives via PR #249's
`ew_current_fierz_channel_decomposition_note_2026-05-01`).

For the physical-matching half (the lattice → physical bridge), see the
lattice-physical matching cluster obstruction synthesis (campaign cycle
13, PR #274).

## Independent audit handoff

```yaml
proposed_claim_type: positive_theorem
proposed_claim_scope: |
  SU(N_c) Fierz channel decomposition giving F_adjoint = (N_c²−1)/N_c² at
  N_c=3 = 8/9 from graph-first primitives. NOT the physical
  y_t correction or Higgs-Z identification (out of scope).
proposed_load_bearing_step_class: A
status_authority: independent audit lane only
```

This source note does not set or predict an audit outcome. It submits only
the class-(A) Fierz channel-fraction identity for independent audit. The
physical-Higgs-Z matching material below is preserved as excluded historical
context and must not be read as part of this row's claim boundary.

---

## Scoped Claim and Excluded Physical-Matching Context

The scoped claim submitted by this row is only the SU(N_c) Fierz
channel-counting result

    R_conn = (N_c^2 - 1)/N_c^2 = 8/9   for  N_c = 3.

The excluded downstream physical-matching claim was that the physical
Yukawa coupling y_t receives a multiplicative factor
sqrt(8/9) relative to the Ward-identity value, arising from the
color-singlet wave function renormalization of the composite scalar
(Higgs = taste condensate):

    y_t(phys) = y_t(Ward) * sqrt(R_conn)
              = y_t(Ward) * sqrt(8/9)

    R_conn = (N_c^2 - 1)/N_c^2 = 8/9   for  N_c = 3

The historical EW gauge-coupling comparison used the opposite
connected-trace specialization `sqrt(K_EW(0)) = sqrt(9/8)` from the same
Fierz fraction. The current EW package keeps this as a conditional
`kappa_EW=0` readout rather than an unconditional derived coefficient.
Those physical-coupling statements require a separate matching theorem and
are outside this row's independent-audit submission.

---

## Part 1: The Scalar Propagator Color Trace

### 1.1 Setup: composite scalar on the unified lattice

On the Cl(3)/Z^3 lattice the Higgs field phi is a color-singlet taste
condensate:

    phi(x) = (1/N_c) psi-bar_a(x) psi_a(x)

where a = 1,...,N_c is the color index and the 1/N_c is the singlet
projection normalization. The operator (1/N_c) delta_{ab} projects
onto the color-singlet component of the N_c x N_c-bar bilinear.

The conjugate field:

    phi^dag(y) = (1/N_c) psi-bar_b(y) psi_b(y)

### 1.2 Two-point function: Wick contraction

The scalar propagator is:

    <phi^dag(x) phi(y)> = (1/N_c^2) sum_{a,b} <(psi-bar_a psi_a)(x) (psi-bar_b psi_b)(y)>

Wick contraction of the connected (one-particle-irreducible) part:

    = -(1/N_c^2) sum_{a,b} <G_{ab}(x,y) G_{ba}(y,x)>_gauge

    = -(1/N_c^2) <Tr_color[G(x,y) G(y,x)]>_gauge

where G_{ab}(x,y) is the quark propagator in the SU(3) gauge
background and the angle brackets denote gauge-field averaging.

### 1.3 Fierz decomposition of the color trace

The bilinear color trace Tr_color[G(x,y) G(y,x)] decomposes into
irreducible SU(N_c) channels via the Fierz identity. Define:

    M_{ab} = G_{ab}(x,y)

Then:

    Tr_color[M M^dag] = sum_{a,b} |M_{ab}|^2

This decomposes into:

    Tr[M M^dag] = (1/N_c) |Tr M|^2 + sum_A |Tr[M t^A]|^2

where t^A (A = 1,...,N_c^2-1) are the SU(N_c) generators normalized
to Tr[t^A t^B] = (1/2) delta_{AB}.

**Proof of the Fierz decomposition.** The N_c x N_c matrix M can be
expanded in the complete basis {I/sqrt(N_c), sqrt(2) t^A}:

    M = (Tr M / N_c) I + sum_A 2 Tr[M t^A] t^A

(using Tr[t^A] = 0 and Tr[t^A t^B] = delta_{AB}/2).

The completeness relation for SU(N_c) is:

    delta_{ac} delta_{bd} = (1/N_c) delta_{ad} delta_{bc}
                          + 2 sum_A (t^A)_{ad} (t^A)_{bc}

This is the Fierz identity. Contracting with M_{ab} M^*_{cd}:

    sum_{a,b} |M_{ab}|^2 = (1/N_c) |Tr M|^2 + 2 sum_A |Tr[M t^A]|^2

Therefore:

    Tr[M M^dag] = (1/N_c) |Tr M|^2 + 2 sum_A |Tr[M t^A]|^2

The first term is the **singlet channel**: it depends only on the
color trace of M. The second term is the **adjoint channel**: it
depends on the traceless (adjoint) components of M.

### 1.4 Channel fractions in the interacting theory

In the free theory (U = I, G_{ab} = delta_{ab} G_0):

    Tr M = N_c G_0
    Tr[M t^A] = 0       (diagonal M times traceless t^A)

So:

    Singlet: (1/N_c)|N_c G_0|^2 = N_c |G_0|^2
    Adjoint: 0
    Total: N_c |G_0|^2

All the signal is in the singlet channel. This is expected: without
gluons, quarks propagate independently and the color trace is
diagonal.

In the interacting theory, the gauge field generates off-diagonal
components M_{ab} with a != b (color is exchanged via gluon lines).
These contribute to the adjoint channel. The Fierz decomposition
gives:

    F_singlet = (1/N_c) |Tr M|^2 / Tr[M M^dag]
    F_adjoint = 2 sum_A |Tr[M t^A]|^2 / Tr[M M^dag]
    F_singlet + F_adjoint = 1

The scoped channel-counting statement is that the connected color trace
(the part where color
quantum numbers are exchanged between the two quark lines) saturates
the adjoint channel, giving:

    F_adjoint = (N_c^2 - 1) / N_c^2 = 8/9

    F_singlet = 1 / N_c^2 = 1/9

This is the Fierz channel-counting result: the adjoint representation
has dimension N_c^2 - 1 and the singlet has dimension 1, out of a
total N_c^2-dimensional bilinear space. If the interacting dynamics
populates all channels according to their dimensionality (i.e., the
connected propagator is "ergodic" in color space), then R_conn =
F_adjoint = (N_c^2 - 1)/N_c^2 exactly.

---

## Part 2: Excluded Context: Wave Function Renormalization Z_phi

### 2.1 Definition of Z_phi

The scalar field phi is defined as the color-singlet bilinear. Its
propagator at leading order in the large-N_f expansion or the
strong-coupling expansion is:

    D_phi(p) = <phi^dag(p) phi(-p)>
             = (1/N_c^2) Tr_color[G(p) G(-p)]

The TOTAL bilinear propagator (summing over all color channels) is:

    D_total(p) = (1/N_c^2) sum_{a,b} |G_{ab}(p)|^2 = (1/N_c^2) Tr[M M^dag]

The SINGLET projection extracts only the singlet channel:

    D_singlet(p) = (1/N_c^2) * (1/N_c) |Tr M|^2

The wave function renormalization Z_phi relates the singlet propagator
to the total:

    D_singlet = F_singlet * D_total

But the PHYSICAL scalar propagator is the CONNECTED part. In the
Fierz decomposition, the connected part (where color is exchanged
between the two fermion lines) corresponds to the ADJOINT channel.
The disconnected part (where each fermion line carries its own color
independently) corresponds to the SINGLET channel.

This requires careful treatment of what "connected" and "disconnected"
mean in color space versus in fermion-line topology.

### 2.2 Connected vs disconnected in color space

The two-point correlator of the bilinear is:

    C(x,y) = <(psi-bar_a psi_a)(x) (psi-bar_b psi_b)(y)>

The Wick contraction gives two topologies:

**Disconnected (in fermion lines):**
    C_disc = <psi-bar_a psi_a(x)> <psi-bar_b psi_b(y)>
           = <condensate(x)> * <condensate(y)>

This is the VEV-squared term, which is subtracted when defining the
propagator of the FLUCTUATION phi - <phi>. In any case, it is a
constant (x,y-independent after gauge averaging) and drops out of the
momentum-space propagator at p != 0.

**Connected (in fermion lines):**
    C_conn = -sum_{a,b} <G_{ab}(x,y) G_{ba}(y,x)>_gauge
           = -<Tr_color[G(x,y) G(y,x)]>_gauge

This is the propagator we computed in Section 1.2. Now decompose THIS
connected-fermion-line contribution into color channels:

    Tr_color[G(x,y) G(y,x)] = (1/N_c)|Tr G(x,y)|^2
                               + 2 sum_A |Tr[G(x,y) t^A]|^2

The first term: |Tr G|^2 is the part where the COLOR INDEX is traced
-- both quark lines carry the SAME color trace. This is the
color-singlet part of the quark loop.

The second term: |Tr[G t^A]|^2 involves traceless color structures.
This is the color-adjoint part of the quark loop -- gluon exchange
has generated off-diagonal color components in G_{ab}.

### 2.3 Which channel defines the physical Higgs propagator?

The physical Higgs is a color singlet. Its propagator is obtained by
projecting the bilinear onto the singlet channel:

    phi = (1/N_c) delta_{ab} psi-bar_a psi_b   (singlet projection)

The connected two-point function of phi is:

    <phi^dag(x) phi(y)>_conn = (1/N_c^2) <Tr_color[G(x,y) G(y,x)]>

But crucially, the bilinear Tr_color[G G] contains BOTH the singlet
and adjoint channels of the quark loop (Section 2.2). The physical
scalar propagator includes the FULL connected fermion loop, which is
dominated by the ADJOINT channel (Section 1.4):

    <phi^dag phi>_conn = (1/N_c^2) * [singlet_loop + adjoint_loop]

Now, in the Ward identity that defines y_t on the lattice, the SAME
bilinear Tr_color[G G] appears. The Ward identity constrains the
TOTAL coupling (to all N_c^2 color channels of the bilinear).

The physical Yukawa, however, involves the scalar phi whose
propagator is renormalized by Z_phi. The key question is: what is
Z_phi?

### 2.4 Z_phi from the connected color trace

The scalar self-energy Sigma_phi(p) (the 1PI correction to the scalar
propagator) involves a fermion loop:

    Sigma_phi(p) ~ integral d^4k Tr_color[G(k) Gamma G(k+p) Gamma]

where Gamma is the Yukawa vertex. For the color-singlet scalar, the
external color structure is delta_{ab} at each vertex, giving:

    Sigma_phi = Tr_color[G(k) G(k+p)]

This is the SAME color trace as the scalar two-point function. By the
Fierz decomposition:

    Sigma_phi = Sigma_singlet + Sigma_adjoint

where:
    Sigma_singlet = (1/N_c)|Tr G(k)|^2      (contribution via singlet intermediate state)
    Sigma_adjoint = 2 sum_A |Tr[G(k) t^A]|^2  (contribution via adjoint intermediate state)

The CONNECTED part of the self-energy (where color quantum numbers
flow around the loop) is Sigma_adjoint. The DISCONNECTED part (where
the color trace factorizes) is Sigma_singlet.

The fraction:

    R_conn = Sigma_adjoint / Sigma_total = (N_c^2 - 1)/N_c^2 = 8/9

Now, the physical scalar propagator is dressed by the self-energy:

    D_phi(p)^{-1} = p^2 + m^2 - Sigma_phi(p)

The wave function renormalization is:

    Z_phi = 1 - d Sigma_phi / d p^2 |_{p^2 = 0}

For the LATTICE scalar (full bilinear), the self-energy includes all
N_c^2 color channels. For the PHYSICAL scalar (after matching to the
continuum EFT where SU(3) and EW sectors factorize), only the
CONNECTED color flow contributes to the physical Higgs self-energy.

The reason: in the continuum EFT below the unification scale, the
Higgs field is an elementary color singlet. Its self-energy receives
QCD corrections (gluon exchange in the top loop), which generate
the connected (adjoint) color structure. The disconnected (singlet)
part is absorbed into the VEV renormalization and does not contribute
to the propagator of the physical Higgs fluctuation.

Therefore:

    Z_phi^{phys} / Z_phi^{lattice} = R_conn = (N_c^2 - 1)/N_c^2 = 8/9

### 2.5 Summary: Z_phi = 8/9

The scalar wave function renormalization for the physical Higgs,
relative to the lattice (total bilinear) normalization, is:

    Z_phi = R_conn = (N_c^2 - 1)/N_c^2 = 8/9

This is a multiplicative correction to the scalar propagator.

---

## Part 3: Excluded Context: How Z_phi Enters the Physical Yukawa

### 3.1 LSZ reduction and external leg factors

The physical S-matrix element for the Yukawa vertex psi-bar phi psi
involves the amputated vertex function Gamma_Y times external leg
factors from LSZ reduction:

    M_Y = sqrt(Z_psi) * sqrt(Z_phi) * sqrt(Z_psi) * Gamma_Y

Each external leg contributes sqrt(Z) for its field. The Yukawa vertex
has:
- 2 fermion legs: each contributes sqrt(Z_psi)
- 1 scalar leg: contributes sqrt(Z_phi)

The physical Yukawa coupling:

    y_t^{phys} = Gamma_Y * Z_psi * sqrt(Z_phi)

### 3.2 Gauge vertex for comparison

The SU(3) gauge vertex psi-bar T^A A_mu psi involves:
- 2 fermion legs: each contributes sqrt(Z_psi)
- 1 gluon leg: contributes sqrt(Z_A)

    g_s^{phys} = Gamma_g * Z_psi * sqrt(Z_A)

### 3.3 The Ward ratio

The lattice Ward identity constrains:

    y_t^{bare} / g_s^{bare} = 1/sqrt(6)

In the physical scheme, the ratio becomes:

    y_t^{phys} / g_s^{phys} = (y_t^{bare} / g_s^{bare})
                              * (Gamma_Y / Gamma_g)
                              * (sqrt(Z_phi) / sqrt(Z_A))

The vertex ratio Gamma_Y / Gamma_g = 1 at leading order (the Ward
identity protects both vertices equally in the lattice theory). At
higher orders, this ratio receives perturbative corrections that are
accounted for by the Ward matching correction Delta (see Part 5).

The fermion wave function Z_psi is the SAME for both vertices (it is
a property of the fermion field, not the interaction vertex). So
Z_psi cancels exactly in the ratio.

The gluon wave function Z_A: the gluon is an elementary field in the
continuum EFT. Its wave function renormalization is already accounted
for in the standard RGE running of g_s. In the lattice-to-continuum
matching, the CMT gives g_s^2 = g_bare^2 / u_0^2, which includes
Z_A. There is no additional color projection for the gluon because
gluons ARE colored -- the gluon propagator probes all N_c^2 - 1
adjoint color channels, which is the full gluon Hilbert space.

Therefore:

    y_t^{phys} / g_s^{phys} = (1/sqrt(6)) * sqrt(Z_phi) / 1
                             = (1/sqrt(6)) * sqrt(8/9)

And:

    y_t^{phys} = (g_s^{phys} / sqrt(6)) * sqrt(8/9)

### 3.4 Why sqrt and not the full factor

The Yukawa vertex has ONE scalar leg. The wave function renormalization
enters as sqrt(Z_phi) per external leg (from LSZ reduction). So the
correction is sqrt(8/9), not 8/9.

By contrast, the conditional EW vacuum-polarization readout involves a
bilinear in propagators (a loop with TWO fermion propagators), and the
color projection acts on the FULL loop. If the connected-trace selector
`kappa_EW=0` is chosen, the EW coupling is extracted from Pi_EW with the
inverse correction: 9/8 on alpha_EW, or sqrt(9/8) on g_EW.

The two corrections are structurally different:
- sqrt(8/9) on y_t: scalar external leg normalization (ONE sqrt)
- sqrt(9/8) on g_EW: conditional `kappa_EW=0` vacuum polarization inverse
  (propagator correction)

---

## Part 4: Excluded Context: Why sqrt(8/9) and Not the EW sqrt(9/8) Specialization -- From Color Structure

This section addresses the adversarial question: "How do you know
the Yukawa gets sqrt(8/9) and not sqrt(9/8)?"

### 4.1 The color channel argument

The physical Higgs is a COLOR SINGLET. It couples to the singlet
component of the quark bilinear psi-bar_a psi_a. The singlet
projection of the full bilinear Hilbert space has dimension 1 out
of N_c^2 total.

The physical Higgs propagator involves the color trace of the
quark loop. In the interacting theory, the connected (gluon-dressed)
color trace has:
- Singlet fraction: 1/N_c^2 = 1/9
- Adjoint fraction: (N_c^2-1)/N_c^2 = 8/9

The physical scalar propagator is the FULL connected trace (both
singlet and adjoint parts contribute to the color-singlet bilinear
psi-bar_a psi_a because the EXTERNAL operator traces over color).
The connected trace is (N_c^2-1)/N_c^2 of the TOTAL trace (which
includes the disconnected part).

Therefore Z_phi = (N_c^2-1)/N_c^2 = 8/9 < 1. The physical scalar
propagator is SMALLER than the total lattice propagator. This makes
y_t SMALLER (not larger), giving sqrt(8/9) < 1.

### 4.2 Physical intuition: why the scalar coupling is reduced

The lattice Ward identity constrains the Yukawa coupling through
the TOTAL bilinear (all N_c^2 color channels). But the physical
Higgs couples only to the color-singlet channel. The singlet is a
SUBSET of the total, so the physical coupling is LESS than the
Ward coupling.

Analogy: if you have 9 radio channels all carrying signal, and the
physical detector tunes to only 8 of them (the connected part), the
detected power is 8/9 of the total. The coupling (amplitude) is
sqrt(8/9) of the total amplitude.

### 4.3 Why the conditional EW readout goes the OTHER way

The EW coupling is extracted differently once a physical readout rule is
chosen. Under the connected-trace specialization `kappa_EW=0`, the EW
vacuum polarization Pi_EW receives contributions from the CONNECTED color
channels of the quark loop.

The CMT normalizes the EW coupling using the TOTAL color trace
(N_c channels). The `kappa_EW=0` readout uses the connected trace
(N_c(N_c^2-1)/N_c^2 = 8N_c/9 effective channels). Since the
coupling is alpha ~ 1/(1 + Pi) and Pi_connected < Pi_total, this
fixed-coefficient specialization gives alpha_phys = alpha_CMT * 9/8.

So:
- Scalar Z_phi: physical propagator is 8/9 of total -> coupling
  sqrt(8/9) DOWN
- EW Pi at `kappa_EW=0`: connected Pi is 8/9 of total -> alpha = 1/(1+Pi)
  goes as 9/8 -> coupling sqrt(9/8) UP

The SAME R_conn = 8/9 produces OPPOSITE corrections because it
enters through DIFFERENT quantities (Z_phi vs 1/Pi_EW).

### 4.4 Explicit Feynman diagram verification

Consider the one-loop scalar self-energy diagram:

         phi ----< quark loop >---- phi
                   |       |
                   G_{ab}  G_{ba}
                   |       |
              vertex 1  vertex 2

The color factor at each vertex is delta_{ab} (color-singlet scalar).
The loop color trace is:

    C_loop = sum_{a,b} delta_{ac} G_{cb}(k) delta_{bd} G_{da}(k+p)
           = sum_{a,b} G_{ab}(k) G_{ba}(k+p)
           = Tr_color[G(k) G(k+p)]

In the free theory (G_{ab} = delta_{ab} G_0):

    C_loop^{free} = sum_a G_0(k)^2 = N_c |G_0|^2

In the interacting theory, Fierz decomposition gives:

    C_loop = (1/N_c)|Tr G|^2 + 2 sum_A |Tr[G t^A]|^2

The connected part (where gluon exchange connects the two propagator
lines) is the adjoint term. The ratio:

    C_loop^{connected} / C_loop^{total} = (N_c^2-1)/N_c^2

This is a DOWNWARD correction: the connected part is LESS than the
total (it excludes the 1/N_c^2 singlet fraction).

Now compare with the EW vacuum polarization diagram:

    gamma/Z ----< quark loop >---- gamma/Z
                  |         |
                  G_{ab}    G_{ba}
                  |         |
             vertex 1   vertex 2

The color factor at each vertex is delta_{ab} (color-singlet EW
current -- the photon does not carry color). The loop color trace is
identical: Tr_color[G(k) G(k+p)].

The SAME trace appears in both diagrams. The difference is how the
trace enters the OBSERVABLE:

For the scalar self-energy: Sigma_phi = C_loop (directly).
The physical coupling is y_t ~ sqrt(Z_phi) ~ sqrt(C_loop^conn/C_loop^total)
= sqrt(8/9).

For the EW vacuum polarization under `kappa_EW=0`: Pi_EW = C_loop.
The physical coupling is alpha_EW ~ 1/(1 + Pi_EW). The CMT
normalizes using Pi^total; this fixed readout uses Pi^connected.
So alpha_phys/alpha_CMT = Pi_total/Pi_connected = 9/8.

### 4.5 Summary: the sign is fixed by the color structure

The correction is sqrt(8/9) on y_t (DOWN) because:

1. The Higgs is a color singlet
2. Its propagator involves the connected color trace of the fermion loop
3. The connected trace is (N_c^2-1)/N_c^2 of the total (Fierz identity)
4. The coupling enters as sqrt(Z_phi) (one scalar leg in the vertex)
5. Therefore y_t^{phys} = y_t^{Ward} * sqrt(8/9)

The correction CANNOT be sqrt(9/8) because that would require the
physical scalar propagator to be LARGER than the total lattice
propagator, which is impossible: the singlet projection can only
REDUCE the propagator (it selects a subspace of the full bilinear
Hilbert space).

---

## Part 5: Excluded Context: Independence from the Ward Matching Correction

### 5.1 The Ward matching correction

The perturbative lattice-to-MSbar matching gives (WARD_IDENTITY_CORRECTION_NOTE):

    (y_t/g_s)^{MSbar}_{M_Pl} = (1/sqrt(6)) * (1 + Delta)
    Delta = (d_1 - c_1) * alpha_s/(4 pi) = +0.0205

This arises from 1-loop Brillouin zone integrals over the staggered
fermion action. Properties:
- **Perturbative:** O(alpha_s/(4 pi)) ~ 2%
- **UV:** acts at M_Pl, before RGE running
- **Scheme-dependent:** converts lattice regularization to MSbar

### 5.2 The color projection correction (excluded context)

    y_t(phys) = y_t(Ward) * sqrt(8/9)

Properties:
- **Non-perturbative:** pure group theory, independent of alpha_s
- **IR:** acts at the EFT crossover scale v
- **Scheme-independent:** kinematic channel counting (Fierz identity)

### 5.3 No overlap

The two corrections act at different scales, arise from different
physics, and have different parametric dependences:

| Property        | Ward matching     | Color projection      |
|-----------------|-------------------|-----------------------|
| Scale           | M_Pl (UV)         | v (IR)                |
| Mechanism       | BZ sunset integral| Fierz channel fraction|
| Perturbative?   | Yes (1-loop)      | No (group theory)     |
| alpha_s dep?    | Yes (linear)      | No (independent)      |
| Scheme dep?     | Yes (lat -> MSbar)| No (universal)        |

Both corrections can be applied simultaneously:

    y_t(phys) = [g_s(M_Pl)/sqrt(6)] * (1 + Delta) * [RGE factor] * sqrt(8/9)

The Ward matching modifies the BOUNDARY CONDITION at M_Pl. The color
projection modifies the PHYSICAL COUPLING at v. These are sequential
operations in the prediction chain with no common subdiagram.

---

## Part 6: Excluded Context: Independence from the EW Vacuum Polarization Correction

### 6.1 Two different quantities, one R_conn

The EW correction (YT_EW_COLOR_PROJECTION_THEOREM.md) and the Yukawa
correction (this note) both use R_conn = 8/9. They are NOT the same
correction applied twice. They enter through DIFFERENT quantities:

| Correction    | Quantity modified    | Channel   | Factor      |
|---------------|---------------------|-----------|-------------|
| EW coupling   | Pi_EW (vac. pol.)   | Adjoint   | sqrt(9/8) only at `kappa_EW=0` |
| Yukawa y_t    | Z_phi (scalar w.f.) | Singlet   | sqrt(8/9)   |

The EW vacuum polarization Pi_EW enters the GAUGE BOSON propagator.
The scalar wave function Z_phi enters the SCALAR propagator.

These are different propagators for different particles. The
corrections are applied to different legs of different diagrams:
- g_EW is corrected via the W/Z/gamma propagator
- y_t is corrected via the Higgs propagator

### 6.2 No double counting in the prediction chain

The prediction chain for m_t involves:

    y_t(M_Pl) = g_s(M_Pl)/sqrt(6)            [Ward identity]
                |
    y_t(v) = backward_Ward_RGE(y_t(M_Pl))     [SM 2-loop RGE]
                |
    y_t(phys) = y_t(v) * sqrt(8/9)            [scalar Z_phi, THIS note]
                |
    m_t(MSbar) = y_t(phys) * v / sqrt(2)       [definition]
                |
    m_t(pole) = m_t(MSbar) * [QCD conversion]  [Marquard et al.]

The EW correction `sqrt(K_EW(kappa_EW))` enters SEPARATELY, in the RGE
step; the historical `sqrt(9/8)` value is the `kappa_EW=0`
specialization. It corrects g_1(v) and g_2(v), which are INPUTS to the SM
RGE beta functions. But the y_t beta function is dominated by the QCD term
(-8 g_3^2 y_t), with the EW terms contributing < 7.4% of the total
(QFP insensitivity theorem). So the EW correction affects y_t(v) only
at the sub-percent level through the RGE, and this effect is already
included in the backward Ward scan.

The sqrt(8/9) on y_t is an ADDITIONAL, INDEPENDENT correction that
acts AFTER the RGE running. There is zero double counting.

---

## Part 7: Excluded Context: Numerical Verification

With the correction applied:

| Quantity              | Framework  | Observed   | Deviation |
|-----------------------|------------|------------|-----------|
| y_t(v) [Ward only]   | 0.9732     | --         | --        |
| y_t(v) [with sqrt(8/9)] | 0.9176  | --         | --        |
| m_t(pole, 2-loop)    | 172.57 GeV | 172.69 GeV | -0.07%    |
| m_t(pole, 3-loop)    | 173.10 GeV | 172.69 GeV | +0.24%    |

The 2-loop prediction matches the observed pole mass to 0.07%.

Before the correction: m_t = 182.24 GeV (+5.52% deviation).
After the correction: m_t = 172.57 GeV (-0.07% deviation).

The correction moves m_t from a 5.5% overshoot to a 0.07% match.

---

## Part 8: Legacy Status Assessment for Excluded Physical Matching

### 8.1 Historical physical-matching assertions

1. The correction sqrt(8/9) on y_t follows from the color-singlet
   wave function renormalization Z_phi = R_conn = 8/9 via LSZ
   reduction (one scalar leg gives one factor of sqrt(Z_phi)).

2. The direction (DOWN, not UP) is fixed by the color structure:
   the singlet projection can only reduce the propagator relative
   to the total bilinear.

3. The correction is independent of the EW vacuum polarization
   correction (different quantities, different diagrams).

4. The correction is independent of the Ward matching correction
   (different scales, different mechanisms).

5. m_t(pole) = 172.57 GeV (-0.07%) with the correction.

6. The correction uses the SAME R_conn = 8/9 already needed for
   the EW couplings -- zero new assumptions beyond the EW theorem.

### 8.2 Why this excluded context is not theorem status here

R_conn = 8/9 is now DERIVED from the 1/N_c expansion
(RCONN_DERIVED_NOTE.md): the leading-order result of the 't Hooft
topological classification gives R_conn = (N_c^2-1)/N_c^2 exactly,
with corrections O(1/N_c^4) = O(1/81) ~ 1.2%, bounded by MC to
|c_2| < 0.8. This removes the previous gap (R_conn was BOUNDED,
relying on Fierz counting + MC only).

To promote to THEOREM: prove that higher-genus corrections vanish
identically (an exact non-perturbative result, not currently available).
The current DERIVED status has controlled O(1%) corrections.

### 8.3 Historical status label, not this row's audit status

The correction sqrt(8/9) on y_t is derived from R_conn = 8/9, which
is itself derived from the 1/N_c expansion of SU(3) gauge theory
(RCONN_DERIVED_NOTE.md). The derivation:
- Is analytical (not just numerical)
- Has controlled corrections: O(1/N_c^4) ~ 1.2%
- Is verified by MC (0.2% agreement) and observables (0.07% m_t match)
- Traces to the Cl(3) axiom with zero imports

---

## Legacy Import Table for Excluded Physical-Matching Context

| Element                          | Value      | Status   | Source                            |
|----------------------------------|------------|----------|-----------------------------------|
| g_bare = 1                       | 1.0        | AXIOM    | Cl(3) canonical                   |
| <P> = 0.5934                     | 0.5934     | COMPUTED | SU(3) MC at beta = 6             |
| u_0 = <P>^{1/4}                  | 0.8777     | COMPUTED | mean-field link                   |
| R_conn = (N_c^2-1)/N_c^2         | 8/9        | DERIVED  | 1/N_c expansion (RCONN_DERIVED_NOTE.md) |
| Ward BC: y_t(M_Pl)/g_s = 1/sqrt(6) | --      | DERIVED  | lattice Ward identity             |
| y_t(v) [Ward] = 0.973            | 0.9732     | DERIVED  | backward Ward scan (2-loop RGE)   |
| sqrt(Z_phi) = sqrt(8/9)          | 0.9428     | DERIVED  | scalar wave function (excluded context) |
| y_t(v) [physical] = 0.918        | 0.9176     | DERIVED  | Ward * sqrt(8/9)                  |
| m_t(pole, 2-loop) = 172.57 GeV   | 172.57     | DERIVED  | MSbar-to-pole conversion          |
