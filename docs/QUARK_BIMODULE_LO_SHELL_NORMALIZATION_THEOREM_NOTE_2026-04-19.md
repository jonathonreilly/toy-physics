# Quark Bimodule LO Shell-Normalization Theorem

**Date:** 2026-04-19  
**Lane:** Quark up-amplitude / bimodule LO closure  
**Status:** same-day proposed_retained follow-on theorem. This note gives an
independent support-side corroboration of the physical-point BICAC / STRC-LO
law from exact carrier normalization already on the branch. The earlier
`kappa` obstruction remains valid on the narrower ray/support-only packet;
the exact shell-normalized carrier adds the missing `kappa`-sensitive datum.
**Provenance of `rho = 1/sqrt(42)`:** `rho` is retained on the branch from
the CKM atlas closure (`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`) as the unit-ray
parameter, with `a_d = rho` also retained (see
`QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md`). This note does **not**
derive `rho`; it uses `rho` as retained input and shows that the
shell-normalized coefficient of the exact bimodule carrier agrees with
that retained value only at the BICAC endpoint `kappa = 1`, thereby
selecting `kappa = 1` among the candidate bridge values
`{kappa_support = sqrt(6/7), kappa_target = 48/49, kappa_BICAC = 1}`. T4
explicitly verifies that support and target bridge factors *fail* the same
retained shell coefficient, so T5 is a discriminative consistency check
between two independent retained sources of `rho`, not a tautological
restatement.  
**Primary runner:** `scripts/frontier_quark_bimodule_lo_shell_normalization_theorem.py`

---

## 0. Executive summary

The earlier obstruction theorem proved that the **ray/support-only** quark
packet leaves a positive-width bridge interval

```text
a_u(kappa) = sin_d * (1 - rho * kappa),
kappa in [sqrt(6/7), 1].
```

That result was honest, but it omitted one exact input already present on the
branch: the exact bilinear carrier

```text
K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)
```

has shell and center columns

```text
E-shell  = (1, 0, 0,   0)
E-center = (1, 0, 1/6, 0)
T-shell  = (0, 1, 0,   0)
T-center = (0, 1, 0, 1/6).
```

So the leading bright slot on the shell is already:

- exact,
- unit-normalized,
- and channel-blind.

All unresolved readout freedom lives only in the lower-row `delta_A1`
dressing. In particular, distinct admissible readout maps agree exactly on the
shell and split only on the center `E` lift.

That gives an independent corroborating route to the LO quark closure.

The retained down amplitude is

```text
a_d = rho.
```

On the shell-normalized one-real imaginary channel

```text
I = R * Im(p),
```

the physical LO down action therefore cannot be

```text
D_LO = rho * kappa * Id_I
```

with `kappa != 1`, because that would rescale an already unit-normalized shell
slot away from the retained shell coefficient `rho`.

Hence the physical LO law is forced to be

```text
D_LO(x) = rho x,
U_LO(x) = (1-rho) x.
```

Applying this to `Im(p) = sin_d` gives

```text
a_u + rho * sin_d = sin_d,
```

i.e. **BICAC / STRC-LO**.

So the earlier reviewer-bar quark caveat narrows again:

- full-interval `NORM` naturality remains a useful strengthening theorem,
- but it is no longer load-bearing for deriving the physical LO split,
- because the physical-point LO split is now forced directly by the exact
  shell-normalized carrier.

---

## 1. Exact carrier normalization

The branch already had two exact facts:

1. the bilinear carrier

   ```text
   K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T),
   ```

2. the exact endpoint columns

   ```text
   E-shell  = (1, 0, 0,   0)
   E-center = (1, 0, 1/6, 0)
   T-shell  = (0, 1, 0,   0)
   T-center = (0, 1, 0, 1/6).
   ```

The important structural consequence is:

> on the shell (`delta_A1 = 0`), the bright slot is already exactly
> normalized to `1`.

So any admissible restricted readout

```text
P_R = [[alpha_E, 0, beta_E, 0],
       [0, alpha_T, 0, beta_T]]
```

acts on the shell only through `alpha_E, alpha_T`; the `beta` ambiguity is
invisible there and appears only at the center.

That means the shell slot is the correct LO normalization surface for the
bimodule split.

---

## 2. The theorem

### Formal statement

> **Theorem (LO shell-normalization forces BICAC).** On the retained CKM
> `1 (+) 5` projector ray, let
>
> ```text
> I = R * Im(p)
> ```
>
> be the one-real imaginary channel, with retained down amplitude
>
> ```text
> a_d = rho.
> ```
>
> Suppose the exact bilinear carrier on the aligned bright block has shell
> columns
>
> ```text
> E-shell = (1,0,0,0),
> T-shell = (0,1,0,0),
> ```
>
> and the remaining readout ambiguity enters only through the lower-row
> `delta_A1` dressing.
>
> Then the physical LO down action on `I` is forced to be
>
> ```text
> D_LO(x) = rho x.
> ```
>
> Equivalently, the bridge factor at LO is
>
> ```text
> kappa = 1.
> ```
>
> Therefore
>
> ```text
> U_LO(x) = (1-rho) x
> ```
>
> and applying to `Im(p) = sin_d` gives
>
> ```text
> a_u + rho * sin_d = sin_d,
> ```
>
> i.e. BICAC / STRC-LO.

### Proof

On the shell, the exact bright carrier columns are already the unit basis
vectors. So the leading bright slot is normalized before any center dressing is
considered.

The retained down amplitude on the same common projector ray is

```text
a_d = rho.
```

If one tried to keep a separate bridge factor `kappa`, the LO down action would
be

```text
D_LO(x) = rho * kappa * x.
```

But on the shell-normalized slot this would assign shell coefficient

```text
rho * kappa
```

instead of the retained shell coefficient `rho`.

So the support point

```text
kappa = sqrt(6/7)
```

and the target point

```text
kappa = 48/49
```

are excluded as **physical LO shell laws**:

```text
rho * sqrt(6/7) != rho,
48 rho / 49 != rho.
```

Only

```text
kappa = 1
```

preserves the retained shell coefficient exactly. Hence

```text
D_LO(x) = rho x.
```

Because the shell slot is the common unit LO channel, the complementary up
action is

```text
U_LO(x) = x - D_LO(x) = (1-rho) x.
```

Applying this to `Im(p) = sin_d` gives

```text
U_LO(Im(p)) = sin_d * (1-rho) = a_u,
```

so

```text
a_u + rho * sin_d = sin_d.
```

This is BICAC / STRC-LO. QED.

---

## 3. Why this does not contradict the earlier obstruction theorem

The earlier obstruction theorem was correct on its stated packet:

- unit ray `p`,
- scalar comparison ray `r = p/sqrt(7)`,
- `a_d = rho`,
- `supp = 6/7`,
- `delta_A1 = 1/42`,
- collinearity identities.

All of those are `kappa`-independent.

What this note adds is a **new retained datum not used there**:

> the exact shell-normalized bright carrier.

That datum is explicitly `kappa`-sensitive, because it identifies the physical
LO shell coefficient with `rho` itself. Once that identification is admitted,
the bridge interval collapses at LO.

So the correct synthesis is:

- **ray/support-only packet:** positive-width `kappa` interval;
- **ray/support packet + exact shell-normalized carrier:** `kappa = 1` at LO.

---

## 4. Scientific consequence

This is not the only same-day quark derivation on the branch. The exact
`1(+)5` channel-completeness / ISSR1 route also forces `kappa = 1` at LO.
The present note should be read as the support-side corroborating proof on the
Route-2 carrier.

The branch no longer needs the full-interval `NORM` naturality theorem in
order to derive the physical LO split. That theorem remains valuable because
it shows the stronger statement:

```text
D_a = a Id_I
```

for the whole ownership interval `a in [0,1]`.

But the load-bearing reviewer-bar issue on the quark lane was the physical LO
split itself. This note derives that directly from retained carrier
normalization already on the branch.

The NLO completion remains exactly the old RPSR step:

```text
supp * delta_A1 = 1/49,
a_u = sin_d * (1 - rho + rho/49).
```

So the clean branch-level quark read is now:

1. exact shell-normalized carrier forces `kappa = 1` at LO;
2. therefore BICAC / STRC-LO is derived;
3. the retained `rho/49` dressing supplies the NLO RPSR target.

---

## 5. Runner summary

The companion runner verifies:

1. exact shell columns are unit bright basis vectors;
2. exact center columns keep the same leading slot with only `1/6` lower-row
   dressing;
3. distinct admissible readout maps agree on the shell and split only on the
   center `E` lift;
4. support and target bridge factors fail the retained shell coefficient
   `a_d = rho`;
5. shell normalization therefore forces `kappa = 1` at LO;
6. this yields exact BICAC / STRC-LO;
7. adding `supp * delta_A1 = 1/49` recovers the full RPSR target.

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_bimodule_lo_shell_normalization_theorem.py
```

Expected on this branch:

- `frontier_quark_bimodule_lo_shell_normalization_theorem.py`: `PASS=10 FAIL=0`

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [ckm_atlas_axiom_closure_note](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [quark_projector_parameter_audit_note_2026-04-19](QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md)
