# Axiom-Native Derivation — Target List

**Status:** sequential targets for the overnight loop on branch
`claude/axiom-native-overnight-FtUl5`. Work in order. Move to the next
target only when the current one is either (a) derived from the
[starting kit](AXIOM_NATIVE_STARTING_KIT.md) with import count zero, or
(b) documented as unreachable with a specific concrete blocker after
exhausting radically different attack vectors.

Do not skip a target to reach a more tractable later one. The loop's
honesty is more valuable than its progress.

---

## Target 1 — Hierarchy row: derive the exponent 16 and remove the `M_Pl` import

The retained hierarchy row presents `v_EW / M_Pl ~ exp(−16...)` as a
derivation. The two concrete things to do:

- derive the exponent **16** from the kit (what combinatorial / geometric /
  algebraic object on `Cl(3) × Z³` yields exactly 16?);
- either construct `M_Pl` from kit primitives (so the ratio is a pure
  prediction) or prove that `M_Pl` must enter as an independent scale
  (reclassification).

Success = exponent 16 derived from the kit, `M_Pl` either constructed or
proven independent.

## Target 2 — One genuinely stronger prediction / falsification surface

Produce ONE row where the framework is doing more than reproducing known
numbers or pushing to unreachable scales. Options: a uniquely-shaped
observable, a sharp CKM/PMNS/Koide discriminator, a structural
signature that distinguishes the framework from alternatives.

Success = one row with (i) a specific observable, (ii) a specific predicted
shape / value, (iii) a specific condition under which the prediction fails,
all derivable from the kit.

## Target 3 — Koide Q = 2/3 via K = 0 on the normalized reduced carrier

Derive Q = 2/3 axiom-natively. The sharpest concrete endpoint per prior
review:

- derive why the physical selector is source-free (K = 0) on the
  normalized reduced carrier,
- OR prove that "K = 0" is exactly the last remaining primitive beyond
  the kit.

Success = K = 0 derived (closes Q = 2/3), or K = 0 proven to be a
necessary new primitive with exactly-stated form.

## Target 4 — CKM |V_us| tension

The package has `|V_us| = 0.22727` vs PDG `0.22438`. The task is not
cosmetic:

- identify whether `|V_us|` is an exact prediction with a real
  discrepancy (and write the falsification note),
- or an approximation missing a correction (construct the correction
  theorem from the kit),
- or evidence the current tensor/projector surface is not the final
  physical readout (prove the replacement).

Success = a real error budget or correction theorem, both derived from
the kit.

## Target 5 — PMNS: derive `J_χ ≠ 0` OR prove a sharp no-go

Current PMNS status is a negative frontier (selector current law
`a_sel = 0`). The decisive next step:

- derive the missing nonzero `J_χ` from the kit,
- OR prove a sharp no-go identifying exactly what extra kit ingredient
  is required.

Success = either a derived nonzero `J_χ` or a no-go theorem naming the
exact missing primitive.

## Target 6 — Strong CP beyond the action-surface

Strong CP is currently "retained on the action surface only". The next
target:

- derive instanton / measure / topological closure from the kit,
- OR prove that the continuum θ-vacuum issue is absent on the physical
  lattice theory in a non-circular way.

Success = one of the two routes above is closed with import count zero.

---

## Rules for moving between targets

- A target is "complete" only if it passes the hostile audit with import
  count 0 and a novelty audit (new rigorous fact proven).
- A target is "honestly unreachable" only after at least six radically
  different attack vectors have been tried and logged in
  `AXIOM_NATIVE_ATTEMPT_LOG.md`. Write a one-page blocker note and move on.
- Never abandon a target because it is "hard". Abandon it only when the
  attempt log demonstrates that every available attack vector from the
  kit has been exhausted.

## What counts as success at the end of the night

For each of the six targets, exactly one of:

1. Derived axiom-natively (ideal).
2. Honestly unreachable with a concrete blocker (acceptable, science).
3. Not yet touched (loop ran out of time — honest).

What is NOT acceptable:

- "Schema-grade" / "retained-grade" / "algebraic-theorem-grade" claims.
- Narrative PASSes dressed as derivations.
- Language escalation without new rigorous content.
- Any commit whose hostile audit fails.
