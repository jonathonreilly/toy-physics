# Claude Settings, State, and Memory (full bodies)

**Capture date:** 2026-04-25

**Tool / model:** Claude Code CLI, model `claude-opus-4-7`.

**Workspace:** `/Users/jonreilly/Projects/Physics`

**Scope note:** Verbatim full-body dump of Claude settings files (which
configure default model, plugins, MCP servers, status line, permission
mode) and the on-machine memory store (which persists facts across
conversations). These are foundational methodology evidence — the
deterministic state that shapes every session on this machine.

---

## settings.json (user-global)

**Path:** `/Users/jonreilly/.claude/settings.json`

**Bytes:** 1916, **Lines:** 35

```markdown
{
  "permissions": {
    "defaultMode": "acceptEdits"
  },
  "statusLine": {
    "type": "command",
    "command": "input=$(cat); cwd=$(echo \"$input\" | jq -r '.workspace.current_dir'); model=$(echo \"$input\" | jq -r '.model.display_name'); remaining=$(echo \"$input\" | jq -r '.context_window.remaining_percentage // empty'); parts=(); if [ -d \"$cwd/.git\" ]; then branch=$(cd \"$cwd\" && git config --global advice.detachedHead false 2>/dev/null; git branch --show-current 2>/dev/null); if [ -n \"$branch\" ]; then if ! git -C \"$cwd\" diff-index --quiet HEAD -- 2>/dev/null; then parts+=(\"${branch}*\"); else parts+=(\"${branch}\"); fi; fi; fi; if [ -n \"$remaining\" ]; then remaining_int=$(printf \"%.0f\" \"$remaining\"); parts+=(\"ctx: ${remaining_int}%\"); fi; if [ -n \"$model\" ]; then parts+=(\"${model}\"); fi; todo_count=0; if [ -f \"$cwd/TODO\" ]; then todo_count=$(grep -c \"^\\s*[-*]\" \"$cwd/TODO\" 2>/dev/null || echo 0); fi; if [ -f \"$cwd/TODO.md\" ]; then todo_md_count=$(grep -c \"^\\s*[-*]\" \"$cwd/TODO.md\" 2>/dev/null || echo 0); todo_count=$((todo_count + todo_md_count)); fi; if [ $todo_count -gt 0 ]; then parts+=(\"todos: ${todo_count}\"); fi; parts+=(\"$(date '+%H:%M:%S')\"); result=\"\"; for i in \"${!parts[@]}\"; do if [ $i -eq 0 ]; then result=\"${parts[$i]}\"; else result=\"${result} | ${parts[$i]}\"; fi; done; echo \"$result\""
  },
  "enabledPlugins": {
    "sourcekit-lsp": true,
    "code-simplifier@claude-plugins-official": true,
    "ralph-loop@claude-plugins-official": true
  },
  "alwaysThinkingEnabled": true,
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": ""
      }
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```

## settings.local.json (user-local)

**Path:** `/Users/jonreilly/.claude/settings.local.json`

**Bytes:** 1510, **Lines:** 49

```markdown
{
  "permissions": {
    "allow": [
      "Bash(gh auth status:*)",
      "Bash(gh repo list:*)",
      "Bash(gh api:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push)",
      "Bash(git clone:*)",
      "Bash(gh repo clone:*)",
      "Bash(git fetch:*)",
      "Bash(git pull:*)",
      "Bash(git checkout:*)",
      "Bash(git push:*)",
      "Bash(grep:*)",
      "Bash(npm run build:*)",
      "Bash(ls:*)",
      "Bash(npm test:*)",
      "Bash(gh pr list:*)",
      "Bash(gh pr create:*)",
      "Bash(gh pr diff:*)",
      "Bash(gh run view:*)",
      "Bash(gh pr view:*)",
      "Bash(git merge:*)",
      "Bash(for f in web/app/api/admin/health/route.ts web/app/api/admin/courses/route.ts web/app/api/admin/users/route.ts \"web/app/api/admin/users/[id]/route.ts\" web/app/api/admin/stats/route.ts)",
      "Bash(do sed -i '' 's/const limited = rateLimit/const limited = await rateLimit/g' \"$f\")",
      "Bash(done)",
      "Bash(gh pr close:*)",
      "Bash(git rebase:*)",
      "Bash(git reset:*)",
      "Bash(chmod:*)",
      "Bash(npx supabase projects list:*)",
      "Bash(git log:*)",
      "Bash(git show:*)",
      "Bash(git branch:*)",
      "Bash(git stash:*)",
      "Bash(npm install:*)",
      "Bash(tail:*)",
      "Bash(git:*)",
      "Bash(echo === AI Consumer Personas ===:*)",
      "Bash(cd /Users/jonreilly/Projects/bridgerapps/AdPrax/web && npx tsc --noEmit 2>&1)",
      "Bash(npx tsc:*)",
      "Bash(npx tsx:*)",
      "Bash(head:*)"
    ]
  }
}
```

## settings.local.json (project-local)

**Path:** `/Users/jonreilly/Projects/Physics/.claude/settings.local.json`

**Bytes:** 169, **Lines:** 14

```markdown
{
  "permissions": {
    "allow": [
      "WebSearch",
      "Bash(*)",
      "Read(*)",
      "Write(*)",
      "Edit(*)",
      "Glob(*)",
      "Grep(*)"
    ]
  }
}
```

## memory/MEMORY.md (index)

**Path:** `/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics/memory/MEMORY.md`

**Bytes:** 939, **Lines:** 6

```markdown
- [Corrected propagator](project_corrected_propagator.md) — 1/L^p attenuation enables gravitational attraction; gravity is pure phase effect
- [Mirror symmetry breakthrough](project_mirror_symmetry_breakthrough.md) — Z₂ DAGs break CLT ceiling: pur_cl=0.917 at N=100, decoherence grows
- [Axiom chain closure](project_axiom_chain_closure.md) — Full chain from local growth to physics on 4D grown graphs; gravity 2.0 SE + decoherence
- [Brannen CH three-gap closure](project_brannen_ch_three_gap_closure.md) — 2026-04-22: Gap 1 (Berry=CH), Gap 2 (Ω=1 derived), Gap 3 (operator map) all closed; runner 16/16
- [Hostile review must challenge semantics](feedback_hostile_review_semantics.md) — Trace-ratio derivations can be arithmetically perfect while comparing against convention-defined sources rather than physical couplings; hostile-review passes must stress-test the action-level identification of symbols, not just algebra
```

## memory/feedback_hostile_review_semantics.md

**Path:** `/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics/memory/feedback_hostile_review_semantics.md`

**Bytes:** 3382, **Lines:** 20

```markdown
---
name: hostile-review must challenge semantics, not just algebra
description: When hostile-reviewing a physics derivation, stress-test what the symbols are actually coupled to in the action, not just whether the algebra computes — a trace-ratio "derivation" can be arithmetically perfect while comparing against a convention-defined source coefficient rather than the physical coupling
type: feedback
---

When the user asks for a hostile-review pass on a derivation of the form "physical coupling A / physical coupling B = some combinatorial factor", the review must include at least one pass that asks **"what is each symbol actually coupled to in the action?"** — not just "is the algebra correct".

**Why:** On 2026-04-16 I did three hostile-review passes on a derivation of `y_t(M_Pl) = g_s(M_Pl)/sqrt(6)` via a Frobenius trace ratio on the full quark fermion space. All three passes stress-tested: algebraic correctness, circularity, operator-rank choices, color-singlet invariance, direction of the inequality, and cross-validation against a parallel lane. All 22/22 numerical checks passed. I then handed the note to a reviewer who found the derivation was arithmetically clean but **compared the Yukawa coupling to a convention-defined source coefficient**, not to the physical Wilson-plaquette gauge coupling. My own note conceded this directly in Sec 2.2 ("framework convention, not a derivation"), and I didn't flag it as fatal during my hostile passes because I was stress-testing the *trace ratio*, not the *identification of what the trace ratio is between*.

The reviewer's P0 finding was devastating and I should have caught it myself: any derivation that compares a ratio of operator norms needs to prove that the coupling constants being ratio'd are the PHYSICAL couplings appearing in the action, not auxiliary scalar-source coefficients introduced to make the trace comparison work.

A second related trap flagged the same day: the trace ratio `1/6` in the derivation was mechanically `1/dim(Q_L)` the moment any rank-1 projection on the 6-dim quark block was admitted. The derivation did not uniquely identify the physical top-Yukawa vertex — any rank-1 projection gives the same answer. "Dimension bookkeeping disguised as physical content" is a recurring failure mode for derivations that lean on Hilbert-space-norm machinery.

**How to apply:**
- For any derivation of a ratio between physical coupling constants, require at least one hostile-review pass dedicated to "what operator in the action is each coupling the coefficient of?" — before accepting that the derivation closes.
- Treat any phrase like "framework convention", "scalar-source coefficient", "coupling redefinition", or "matching to physical coupling" in the derivation itself as a promotion-blocker until replaced by an explicit on-surface identification.
- For Hilbert-space-norm arguments producing `1/sqrt(N)` or `1/N` answers, always ask "is this just `1/dim(block)` rank counting, or does it uniquely pin down a physical operator?" — if any rank-k projection on the block gives the same answer, the derivation isn't isolating the physical vertex.
- Check that the derivation's load-bearing principle is itself on retained/promoted publication surfaces before leaning new theorems on it. An unpromoted-lane principle cannot carry a replacement authority for another lane.
```

## memory/project_axiom_chain_closure.md

**Path:** `/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics/memory/project_axiom_chain_closure.md`

**Bytes:** 2326, **Lines:** 51

```markdown
---
name: axiom_chain_closure
description: Full axiom chain from local growth to physics closes on 4D grown graphs — gravity 2.0 SE + decoherence 0.8% with emergent mass
type: project
---

The axiom chain closes on locally-grown 4D geometric DAGs (2026-04-03):

Axiom 1 (network) → geometric growth rule (parent + offset in d dims)
Axiom 3 (space) → positions inferred from parent + random offset
Axiom 6 (continuation) → radius-based edges = geometric locality
Axiom 2 (patterns) → amplitude concentration = emergent mass
Axiom 8 (gravity) → phase valley in mass-sourced 1/r field
Axiom 9 (records) → barrier at N/3 (still imposed, not emergent)

Key result: d_growth=3 (4D), N=30, 20 seeds:
  Gravity: +0.432 (2.0 SE), Decoherence: pur_min=0.992 (0.8%)
  On the SAME grown graph with emergent mass. Nothing imposed.

Dimensional scaling confirmed on grown graphs:
  d_growth=2 (3D): alpha=-0.63 (matches imposed -0.7)
  d_growth=3 (4D): alpha=-0.18 (matches imposed -0.178 exactly)
  d_growth=4 (5D): alpha=+0.61 (positive, flat)

Random (non-geometric) growth rules fail catastrophically (alpha=-3.16).
The key requirement: edges must respect GEOMETRIC locality.

All axioms now close including Axiom 9 (emergent barrier from
amplitude-density damping). Self-consistent mass-field loop converges
in ~7 iterations and improves both metrics.

DIMENSIONAL SELECTION PRINCIPLE (2026-04-03):
d=3 transverse (3+1 spacetime) is the UNIQUE dimension where both
gravity and decoherence coexist on grown graphs:
  d<3: decoherence too weak
  d=3: BOTH WORK (3.5% decoherence + gravity +0.52)
  d>3: gravity wrong sign (amplitude too diluted)

This is derivable from the axioms: the dimension of space is selected
by the requirement that both phenomena emerge from the same structure.

**How to apply:** The program is at a natural completion point.
The axiom chain is closed, the dimensional selection is established.
Remaining work is refinement (stronger signals, continuum limit).

**Mirror branch update (2026-04-03):** Structured mirror growth with
LINEAR propagator gives Born=8e-17 + gravity +3.05 (21 SE) + 14-19%
decoherence at npl=30, N=30. The geometry does the work, not
normalization. MI on grown geometry: 0.23-0.29 bits (lower than
imposed S4 mirror 0.48-0.77). Gravity sign is slit-selection-sensitive.
```

## memory/project_brannen_ch_three_gap_closure.md

**Path:** `/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics/memory/project_brannen_ch_three_gap_closure.md`

**Bytes:** 2082, **Lines:** 16

```markdown
---
name: Brannen phase CH-descent three-gap closure
description: On 2026-04-22, closed the three identified gaps in the Callan-Harvey bridge for Koide Brannen phase δ = 2/9; runner 16/16 PASS
type: project
originSessionId: 3024a28f-f874-4bff-b0ee-3b66239f6e6d
---
Closed on 2026-04-22 the three gaps a reviewer called out in the charged-lepton Brannen-phase / Callan-Harvey bridge:

- **Gap 1 (identification)**: theorem that selected-line Berry phase = CH descent phase, proved as two evaluations of the same defect zero-mode wavefunction's Pancharatnam-Berry holonomy on the CP¹ carrier. Not an equality of raw 1-forms but of integrated phases; the former can differ by gauge.
- **Gap 2 (descent factor Ω = 1)**: derived by explicit Fubini integration of `∫F_Y∧F_Y/(8π²)` over the minimum-winding 4-tube on the retained physical Z³ × R lattice. Ω = 2·n_⊥·n_∥·(2π)²/(8π²) = n_⊥·n_∥ = 1 when both transverse and tangent Dirac-quantized windings = 1. Minimum-nonzero choice supported by two retained consistency observations (anomaly-active sector, generation-distinguishing Z_3).
- **Gap 3 (operator map)**: explicit chain bulk J^μ_Y → Q_Σ (transverse integration of CS_3) → CP¹ tautological Berry connection (Pancharatnam-Berry dualization of conjugate-pair ray). Verified numerically: projective winding rate d(arg ζ)/dθ = -n_eff = -2 on the selected-line Koide amplitude.

**Why:** the existing `KOIDE_BRANNEN_PHYSICAL_BRIDGE_DERIVATION_NOTE_2026-04-22.md` stated the chain schematically; a reviewer correctly flagged that Gaps 1-3 were asserted rather than derived.

**How to apply:** when questions come up about "is the Brannen 2/9 actually derived?" or "what is the selected-line CP¹ tied to the bulk anomaly?", point to `docs/KOIDE_BRANNEN_CH_THREE_GAP_CLOSURE_NOTE_2026-04-22.md` and the runner `scripts/frontier_koide_brannen_ch_three_gap_closure.py` (16/16 PASS). For the residual Q = 2/3 lane and m_* axiom-native characterization, those remain separate open lanes tracked in frontier map + SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS.
```

## memory/project_corrected_propagator.md

**Path:** `/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics/memory/project_corrected_propagator.md`

**Bytes:** 1646, **Lines:** 39

```markdown
---
name: Corrected propagator — complete characterization
description: 1/L^p propagator, phase valley gravity, two-register decoherence, saturation theory
type: project
---

## Corrected Propagator
`attenuation_mode="geometry"` in `RulePostulates`.

## Results (2026-03-31, 67 experiments)

### What works (qualitatively correct)
- Gravity: 90% attract (2D), 88% (3D), pure phase (k=0→zero)
- Interference: 100%, Born rule I₃=4.28e-15, R_c exact at f=0
- Growth emergence: 6-8 layers
- Endogenous decoherence: universal on irregular DAGs (purity<0.99 for 20/20)
- Phase valley: ΔS ≈ -L√(2f), shift ∝ k² in perturbative regime

### What doesn't work (quantitatively wrong)
- Distance scaling: shift increases with b (not 1/b), saturates at k>0.5
- Mass scaling: shift is mass-independent (threshold)
- Decoherence scaling: purity increases with graph size (0.57→0.89)
- All three failures same root cause: path averaging on dense graphs

### Three regimes of gravitational coupling
- k < 0.15: perturbative, shift ∝ k² (shift/k²≈35)
- k ≈ 0.2-0.5: nonlinear transition
- k > 0.5: SATURATED, shift = ±height (beam width limit)
- Previous tests at k=2-5 were all in saturated regime
- Even perturbative regime doesn't give 1/b

### Decoherence architectures tested (5, all wrong-scaling)
1. Node-label, 2. Cumulative action, 3. Evolving phase, 4. Scaled bins, 5. Graph growth
All show purity increasing with graph size (linear env vs exponential paths)

### Graph requirement
Regular lattice: gravity + interference but no decoherence (symmetry)
Irregular DAG: all three phenomena (broken symmetry enables env selectivity)
```

## memory/project_mirror_symmetry_breakthrough.md

**Path:** `/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics/memory/project_mirror_symmetry_breakthrough.md`

**Bytes:** 1491, **Lines:** 24

```markdown
---
name: Mirror symmetry breakthrough
description: Z₂ mirror-symmetric DAGs break the CLT decoherence ceiling — pur_cl=0.917 at N=100 with growing decoherence
type: project
---

Z₂ mirror-symmetric DAGs are the strongest decoherence result in the project.

**Result:** Mirror DAGs maintain pur_cl ~ 0.90-0.92 from N=25 to N=100, with decoherence appearing to GROW with N (opposite of the 1/N ceiling on random graphs).

**Why:** The transfer matrix commutes with the y → -y reflection operator, forcing the product T_N...T_1 to maintain rank-2 (one singular value per symmetry sector). Slit A and slit B map to different sectors and cannot converge by symmetry.

**How to apply:** When working on decoherence, use `generate_mirror_dag()` from `scripts/mirror_symmetric_dag.py`. Key parameters: NPL_HALF=25 (50 total per layer), p_cross=0.0 for exact symmetry.

**Open items:** Born check needs chokepoint barrier variant (standard layer-2 connectivity fails Born equally for random and mirror — barrier structure issue, not symmetry issue). Gravity is noisy on mirror graphs.

**Branch:** claude/distracted-napier, merged to main.

**Continuum limit (2026-04-03):** NN lattice (3 edges/node) converges
through h=0.25 with Born at machine precision. RG coupling ~ 1/h² keeps
gravity finite. Distance law b^(-1.01) at R²=0.998 in ultra-weak regime.
Light cone: strict (max_speed=1.0). Massless dispersion (no mass gap).
MI → 1.0 bit, decoherence → 50% in the continuum limit.
```

