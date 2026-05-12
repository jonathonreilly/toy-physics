#!/usr/bin/env python3
"""
PR230 block30 full-approach physics-loop exercise packet.

This runner records four explicit exercises requested for the full PR230
top-Yukawa approach:

  1. Assumption questioning over the whole current approach.
  2. "Elon" first-principles / 10x constraint-reset exercise.  The local
     physics-loop skill has no canonical "Elon exercise" section, so this
     runner records the interpretation and keeps it non-authoritative.
  3. Literature bridge search, with every source classified as context,
     method support, theorem, comparator, or non-derivation analogy.
  4. Math search, including less-common route families that could help only
     after the missing same-surface operator/action/row objects exist.

It also cross-checks other repo bridge work that landed or was proposed around
PR230.  The output is a route-selection and import-firewall certificate, not a
top-Yukawa closure certificate.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block30_full_approach_assumptions_elon_lit_math_bridge_review_2026-05-11.json"
)

PARENT_FILES = {
    "block28_certificate": "outputs/yt_pr230_block28_degree_one_oh_support_intake_checkpoint_2026-05-11.json",
    "block28_note": "docs/YT_PR230_BLOCK28_DEGREE_ONE_OH_SUPPORT_INTAKE_CHECKPOINT_NOTE_2026-05-11.md",
    "block29_wz_pivot_certificate": "outputs/yt_pr230_block29_post_block28_wz_pivot_admission_checkpoint_2026-05-11.json",
    "block29_wz_pivot_note": "docs/YT_PR230_BLOCK29_POST_BLOCK28_WZ_PIVOT_ADMISSION_CHECKPOINT_NOTE_2026-05-11.md",
    "degree_one_oh_theorem": "docs/YT_PR230_DEGREE_ONE_RADIAL_TANGENT_OH_THEOREM_NOTE_2026-05-07.md",
    "fms_candidate_action_packet": "docs/YT_PR230_FMS_OH_CANDIDATE_ACTION_PACKET_NOTE_2026-05-07.md",
    "fms_source_overlap_gate": "docs/YT_PR230_FMS_SOURCE_OVERLAP_READOUT_GATE_NOTE_2026-05-07.md",
    "fms_composite_oh_conditional": "docs/YT_PR230_FMS_COMPOSITE_OH_CONDITIONAL_THEOREM_NOTE_2026-05-06.md",
    "clean_source_higgs_selector": "docs/YT_PR230_CLEAN_SOURCE_HIGGS_MATH_TOOL_ROUTE_SELECTOR_NOTE_2026-05-05.md",
    "gns_flat_extension_attempt": "docs/YT_PR230_GNS_SOURCE_HIGGS_FLAT_EXTENSION_ATTEMPT_NOTE_2026-05-05.md",
    "det_positivity_intake": "docs/YT_PR230_DET_POSITIVITY_BRIDGE_INTAKE_GATE_NOTE_2026-05-05.md",
    "ward_readout_repair": "docs/YT_WARD_PHYSICAL_READOUT_REPAIR_AUDIT_NOTE_2026-05-01.md",
    "beta_lambda_no_go": "docs/YT_BETA_LAMBDA_PLANCK_STATIONARITY_NO_GO_NOTE_2026-05-01.md",
    "assumptions_ledger": ".claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/ASSUMPTIONS_AND_IMPORTS.md",
    "opportunity_queue": ".claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/OPPORTUNITY_QUEUE.md",
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def read_text(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def assumptions_exercise() -> list[dict[str, Any]]:
    return [
        {
            "assumption": "The completed taste-radial row packet can become PR230 closure once chunk063 lands.",
            "stress_result": "False on the current surface.",
            "why_it_matters": "The rows are finite C_ss/C_sx/C_xx staging rows; x is not certified canonical O_H.",
            "falsifier_or_retirement_path": "Supply accepted same-surface O_H plus C_ss/C_sH/C_HH pole rows and rerun Gram/FV/IR gates.",
            "current_disposition": "support-only",
        },
        {
            "assumption": "Degree-one Z3 radial uniqueness identifies the physical Higgs operator.",
            "stress_result": "Only conditional.",
            "why_it_matters": "Block28 proves the axis only under a future action premise that O_H is degree-one radial.",
            "falsifier_or_retirement_path": "Derive the same-surface EW/Higgs action and canonical LSZ normalization.",
            "current_disposition": "exact support, not closure",
        },
        {
            "assumption": "FMS composite O_H can be imported as proof authority.",
            "stress_result": "False for current PR230.",
            "why_it_matters": "FMS gives the right composite-operator shape only after a gauge-Higgs action and Phi field exist on the surface.",
            "falsifier_or_retirement_path": "Derive/adopt a same-surface EW/Higgs action with dynamic Phi, v, h, and source rows.",
            "current_disposition": "conditional-support",
        },
        {
            "assumption": "A source-only scalar response determines source-Higgs overlap.",
            "stress_result": "False.",
            "why_it_matters": "Source-only counterfamilies preserve C_ss while changing C_sH and canonical y_H.",
            "falsifier_or_retirement_path": "Measure C_sH and C_HH or prove a physical rank-one neutral theorem.",
            "current_disposition": "no-go for source-only closure",
        },
        {
            "assumption": "GNS, flat-extension, or moment theory can create the missing O_H label.",
            "stress_result": "False.",
            "why_it_matters": "Moment tools certify full matrices; they do not name the absent second operator.",
            "falsifier_or_retirement_path": "Use them only after C_ss/C_sH/C_HH rows exist.",
            "current_disposition": "method support after rows",
        },
        {
            "assumption": "Determinant positivity is enough for neutral scalar uniqueness.",
            "stress_result": "False.",
            "why_it_matters": "Positivity preservation is compatible with reducible neutral sectors.",
            "falsifier_or_retirement_path": "Prove positivity improvement/irreducibility for the physical neutral transfer kernel.",
            "current_disposition": "support-only positivity",
        },
        {
            "assumption": "W/Z response can bypass O_H without extra rows.",
            "stress_result": "False.",
            "why_it_matters": "The response route still needs accepted action, production W/Z rows, same-source top rows, covariance, strict g2, and delta_perp.",
            "falsifier_or_retirement_path": "Build the strict matched physical-response packet.",
            "current_disposition": "exact-support contract only",
        },
        {
            "assumption": "Observed g2, W/Z masses, m_t, or y_t can select the bridge.",
            "stress_result": "Forbidden.",
            "why_it_matters": "That would repeat the target-selection pattern PR230 was designed to avoid.",
            "falsifier_or_retirement_path": "Use observed values only as comparators after a same-surface derivation or measurement.",
            "current_disposition": "excluded",
        },
        {
            "assumption": "The recent Ward same-1PI repair can be loaded into PR230.",
            "stress_result": "Not as PR230 proof authority.",
            "why_it_matters": "The narrow Ward work still uses H_unit/y_t_bare language and leaves the physical readout/matching issue separate.",
            "falsifier_or_retirement_path": "Let the Ward audit lane decide; keep PR230 on physical correlator/source-Higgs/WZ evidence.",
            "current_disposition": "context only for PR230",
        },
        {
            "assumption": "lambda(M_Pl)=0 implies beta_lambda(M_Pl)=0.",
            "stress_result": "False on the current surface.",
            "why_it_matters": "The beta-lambda no-go shows stationarity is an extra codimension-one selector.",
            "falsifier_or_retirement_path": "Prove a new substrate scale-stationarity theorem or keep double-criticality conditional.",
            "current_disposition": "no-go / conditional route",
        },
        {
            "assumption": "Picard-Fuchs or exact ODE methods can bypass the missing PR230 bridge.",
            "stress_result": "False as a bridge; useful as a computation engine.",
            "why_it_matters": "Exact ODEs compute defined finite-volume integrals; they do not define O_H or C_sH.",
            "falsifier_or_retirement_path": "After Z(beta,s,h) is defined, use PF/WZ/tensor methods to certify rows.",
            "current_disposition": "math-engine support",
        },
        {
            "assumption": "Neutral H3/H4 can be inferred from finite C_sx rows.",
            "stress_result": "False.",
            "why_it_matters": "Finite covariance rows are not a physical transfer/action generator or irreducibility proof.",
            "falsifier_or_retirement_path": "Supply same-surface H3 physical transfer/off-diagonal generator and H4 source-Higgs coupling authority.",
            "current_disposition": "open",
        },
        {
            "assumption": "A scalar LSZ denominator proxy can be repaired by prose contact subtraction.",
            "stress_result": "False.",
            "why_it_matters": "Current diagnostics reject the raw proxy; contact, threshold, FV/IR, and model-class authority must be explicit.",
            "falsifier_or_retirement_path": "Build strict scalar-LSZ/Stieltjes/FV certificate tied to canonical O_H or W/Z response.",
            "current_disposition": "open",
        },
        {
            "assumption": "New literature can serve as hidden derivation authority.",
            "stress_result": "False.",
            "why_it_matters": "The physics-loop protocol classifies literature as method/context unless it supplies a theorem with explicit import status.",
            "falsifier_or_retirement_path": "Enter each item in the import ledger and keep it out of retained proof unless retired.",
            "current_disposition": "firewall",
        },
        {
            "assumption": "An external EW/Higgs action extension would close current-surface PR230.",
            "stress_result": "False unless adopted/derived on the surface.",
            "why_it_matters": "An external extension can produce conditional support, not current retained closure.",
            "falsifier_or_retirement_path": "Derive the action from Cl(3)/Z3 or explicitly register/adopt a new premise with audit status.",
            "current_disposition": "conditional only",
        },
        {
            "assumption": "The direct top-correlator compute path is scientifically unnecessary if a bridge proof appears.",
            "stress_result": "Partly true but not currently actionable.",
            "why_it_matters": "A retained bridge could replace month-scale compute, but every known bridge still lacks O_H/action/rows or stationarity.",
            "falsifier_or_retirement_path": "Continue chunk compute as support while prioritizing action-first O_H or strict W/Z packets.",
            "current_disposition": "parallel support",
        },
    ]


def elon_exercise() -> dict[str, Any]:
    return {
        "canonical_skill_section_found": False,
        "interpretation": (
            "No canonical 'Elon exercise' section was found in the local physics-loop skill. "
            "This packet implements it as a first-principles / 10x constraint-removal exercise."
        ),
        "first_principles_question": (
            "What is the smallest physical artifact that would let PR230 compute y_t without "
            "renaming H_unit, importing observed targets, or waiting for full month-scale MC?"
        ),
        "zeroth_principles_chain": [
            {
                "level": "substrate state space",
                "primitive": "Cl(3)/Z3 finite lattice degrees of freedom with gauge links, staggered fermions, and the declared substrate action.",
                "non_importable_shortcut": "SM field names or continuum Higgs labels before the same-surface operator exists.",
                "required_bridge": "A native action/transfer object that makes the relevant scalar/gauge response an observable on this state space.",
            },
            {
                "level": "observable algebra",
                "primitive": "Gauge-invariant Euclidean correlation functions generated by source derivatives of the partition function.",
                "non_importable_shortcut": "Bare-source labels, H_unit labels, or matrix elements used as definitions.",
                "required_bridge": "A source functional Z(beta, s, h, ...) whose derivatives are physically identified without target fitting.",
            },
            {
                "level": "time evolution",
                "primitive": "Reflection-positive transfer/kernel data and long-distance pole structure.",
                "non_importable_shortcut": "Finite equal-time covariance rows treated as pole residues.",
                "required_bridge": "Strict C_ss/C_sH/C_HH time-kernel rows or a theorem that fixes the hidden neutral coordinate.",
            },
            {
                "level": "canonical scalar coordinate",
                "primitive": "The Higgs readout is the normalized physical scalar direction that couples to masses.",
                "non_importable_shortcut": "Declaring the taste-radial/source axis to be O_H by symmetry label alone.",
                "required_bridge": "Accepted same-surface EW/Higgs action and canonical O_H/LSZ normalization, or a neutral primitive/rank-one proof.",
            },
            {
                "level": "top mass / Yukawa readout",
                "primitive": "y_t is read from m_t = y_t v/sqrt(2) or an equivalent physical response after m_t/v and the scalar coordinate are observable inputs.",
                "non_importable_shortcut": "Defining y_t_bare from a matrix element or choosing observed m_t/y_t as a selector.",
                "required_bridge": "Direct top correlator measurement, strict W/Z matched response, or source-Higgs pole-residue readout with explicit v input status.",
            },
        ],
        "irreducible_missing_object": (
            "The missing object is not a number. It is a same-surface physical map from the PR230 source coordinate "
            "to the canonical scalar/Higgs coordinate, with enough time-kernel or response data to read a pole residue."
        ),
        "non_negotiable_bottleneck": (
            "A same-surface physical bridge from the PR230 source to canonical Higgs response: "
            "either accepted O_H plus C_ss/C_sH/C_HH rows, strict W/Z matched response, or "
            "neutral primitive/rank-one authority."
        ),
        "constraint_deletions": [
            "Stop treating chunk completion as closure; it is row support until x=O_H is certified.",
            "Stop asking source-only data to name the hidden Higgs coordinate.",
            "Stop using exact-math tooling before the physical functional/operator is defined.",
            "Stop mixing Ward repair authority into the direct-observable PR230 route.",
            "Stop letting comparator proximity select a bridge."
        ],
        "ten_x_redesigns": [
            {
                "route": "Action-first O_H packet",
                "idea": "Build or derive the same-surface EW/Higgs action and O_H source directly, then run a small strict C_ss/C_sH/C_HH pilot before full production.",
                "why_10x": "One accepted operator/action packet can replace many proxy-row and alias gates.",
                "risk": "If the action is an external extension rather than derived, status remains conditional.",
            },
            {
                "route": "Strict W/Z response bypass",
                "idea": "Measure same-source top plus W/Z response with covariance and strict non-observed g2.",
                "why_10x": "It may bypass explicit O_H pole-overlap if the physical response packet is complete.",
                "risk": "Engineering-heavy and still blocked by accepted action and delta_perp authority.",
            },
            {
                "route": "Neutral primitive/rank-one theorem",
                "idea": "Prove a physical positivity-improving transfer kernel in the neutral scalar sector.",
                "why_10x": "A theorem could turn source overlap into a uniqueness consequence.",
                "risk": "All current positive-cone facts are support; no physical transfer kernel is present.",
            },
            {
                "route": "Exact-math accelerator after definition",
                "idea": "Use Picard-Fuchs/WZ/tensor/Herglotz methods only after the two-source functional exists.",
                "why_10x": "Can convert a finite row computation into exact or bounded proof once objects are defined.",
                "risk": "No bridge value until O_H/action are supplied.",
            },
        ],
        "decision": (
            "Prioritize action-first O_H authority, with strict W/Z as fallback. Keep chunk rows and "
            "exact math as support engines, not closure substitutes."
        ),
    }


def literature_search() -> list[dict[str, str]]:
    return [
        {
            "source": "Frohlich, Morchio, Strocchi, Higgs phenomenon without symmetry breaking order parameter, IHES P/81/12",
            "url": "https://archives.ihes.fr/document/P_81_12.pdf",
            "exact_item_used": "Gauge-invariant composite-Higgs language behind the FMS route.",
            "import_class": "background context / method bridge",
            "pr230_impact": "Supports O_H = Phi^dagger Phi - <Phi^dagger Phi> only after Phi/action/v/h exist.",
        },
        {
            "source": "Maas, Sondenheimer, Toerek, On the observable spectrum of theories with a BEH effect, arXiv:1709.07477",
            "url": "https://arxiv.org/abs/1709.07477",
            "exact_item_used": "Observable spectrum built from gauge-invariant states; FMS map can fail in generalized sectors.",
            "import_class": "literature bridge / non-derivation context",
            "pr230_impact": "Reinforces using gauge-invariant composite operators, not gauge-dependent labels.",
        },
        {
            "source": "Fradkin and Shenker, Phase diagrams of lattice gauge theories with Higgs fields, Phys. Rev. D 19, 3682",
            "url": "https://journals.aps.org/prd/abstract/10.1103/PhysRevD.19.3682",
            "exact_item_used": "Gauge-Higgs lattice surface context and confinement-Higgs continuity constraints.",
            "import_class": "background context",
            "pr230_impact": "Constrains action-adoption thinking; it is not an O_H/source-overlap selector.",
        },
        {
            "source": "Luscher, Construction of a selfadjoint, strictly positive transfer matrix for Euclidean lattice gauge theories",
            "url": "https://doi.org/10.1007/BF01614090",
            "exact_item_used": "Transfer-matrix setting for Euclidean lattice gauge theory.",
            "import_class": "literature theorem / method support",
            "pr230_impact": "Useful for future time-kernel pole rows; no current O_H closure.",
        },
        {
            "source": "Bulava et al., Higgs-Yukawa model in chirally-invariant lattice field theory, arXiv:1210.1798",
            "url": "https://arxiv.org/abs/1210.1798",
            "exact_item_used": "Nonperturbative lattice Higgs-Yukawa methodology precedent.",
            "import_class": "method context",
            "pr230_impact": "Confirms compute route shape; not a derivation if Yukawa is scanned as input.",
        },
        {
            "source": "Gerhold/Jansen style lattice Higgs-Yukawa program, examples around arXiv:0912.0407 and arXiv:1111.4789",
            "url": "https://arxiv.org/abs/0912.0407",
            "exact_item_used": "Lattice Higgs-Yukawa finite-volume/cutoff methods.",
            "import_class": "method context",
            "pr230_impact": "Helps production design only; does not retire the PR230 bridge.",
        },
    ]


def math_search() -> list[dict[str, str]]:
    return [
        {
            "source": "Curto and Fialkow, Truncated K-moment problems in several variables",
            "url": "https://iro.uiowa.edu/esploro/outputs/journalArticle/Truncated-K-moment-problems-in-several-variables/9984240861702771",
            "exact_item_used": "Flat/rank-preserving extensions imply unique finitely atomic representing measures.",
            "import_class": "literature theorem",
            "pr230_impact": "Powerful after full source-Higgs moment matrix exists; source-only data remain underdetermined.",
        },
        {
            "source": "Gesztesy and Tsekanovskii, On Matrix-Valued Herglotz Functions",
            "url": "https://arxiv.org/abs/funct-an/9712004",
            "exact_item_used": "Matrix-valued spectral measures and Herglotz representations.",
            "import_class": "literature theorem / method support",
            "pr230_impact": "Correct language for C_ss/C_sH/C_HH spectral rows; cannot invent missing entries.",
        },
        {
            "source": "Ho and Kalman, Effective construction of linear state-variable models from input/output functions",
            "url": "https://ntrs.nasa.gov/citations/19670049337",
            "exact_item_used": "Minimal realization from Markov parameters is coordinate/similarity-class data.",
            "import_class": "literature theorem / analogy",
            "pr230_impact": "Explains why source-only response cannot fix canonical hidden coordinate.",
        },
        {
            "source": "Rugh, Cones and gauges in complex spaces, Annals of Mathematics 171 (2010)",
            "url": "https://annals.math.princeton.edu/2010/171-3/p07",
            "exact_item_used": "Complex Perron-Frobenius and cone contraction spectral gaps.",
            "import_class": "literature theorem / possible bridge method",
            "pr230_impact": "Candidate toolkit for neutral primitive theorem after physical transfer kernel exists.",
        },
        {
            "source": "Doplicher and Roberts, Endomorphisms of C*-algebras, cross products, and duality for compact groups",
            "url": "https://annals.math.princeton.edu/1989/130-1/p03",
            "exact_item_used": "Gauge group reconstruction from observable/local algebra structure.",
            "import_class": "literature theorem / long-horizon analogy",
            "pr230_impact": "Conceptual route for reconstructing fields from observables, but far larger data than PR230 has.",
        },
        {
            "source": "Kunis, Peter, Roemer, von der Ohe, multivariate Prony method",
            "url": "https://www.sciencedirect.com/science/article/pii/S0024379515006187",
            "exact_item_used": "Sparse finite moment reconstruction by annihilating/eigenvalue methods.",
            "import_class": "method theorem / conditional support",
            "pr230_impact": "Could help if finite-rank isolated-pole assumptions are certified; current prefixes are not enough.",
        },
        {
            "source": "Plaquette V=1 Picard-Fuchs ODE work in the repo and PR #1131 audit review",
            "url": "https://github.com/jonathonreilly/cl3-lattice-framework/pull/1131",
            "exact_item_used": "Exact ODE/certified finite-integral computation pattern.",
            "import_class": "repo-method analogy",
            "pr230_impact": "Useful pattern after Z(beta,s,h) is defined; not an O_H or y_t selector.",
        },
    ]


def repo_bridge_cross_check() -> list[dict[str, str]]:
    return [
        {
            "artifact": "PR230 block28 degree-one O_H support intake",
            "classification": "exact support",
            "transfer_to_pr230": "Directly useful; proves unique degree-one radial axis under future action premise.",
            "closure_status": "Still missing same-surface EW/Higgs action, canonical O_H, and C_sH/C_HH rows.",
        },
        {
            "artifact": "PR230 FMS composite O_H conditional theorem and action packet",
            "classification": "conditional-support",
            "transfer_to_pr230": "Best current action-first route.",
            "closure_status": "Cannot close without dynamic Phi/v/h/action and source-Higgs pole rows.",
        },
        {
            "artifact": "PR230 GNS/flat-extension and Herglotz/moment attempts",
            "classification": "exact negative boundary for source-only data",
            "transfer_to_pr230": "Useful as future matrix-row validators.",
            "closure_status": "Cannot create missing O_H or C_sH/C_HH entries.",
        },
        {
            "artifact": "PR230 determinant-positivity bridge intake",
            "classification": "bounded support",
            "transfer_to_pr230": "Supports positivity of measure/transfer setting.",
            "closure_status": "Not positivity improvement or neutral rank-one.",
        },
        {
            "artifact": "PR #1080 / PR #1112 YT Ward same-1PI and narrow substitution work",
            "classification": "separate Ward/g_bare lane context",
            "transfer_to_pr230": "May matter to a separate audit of Ward/g_bare; not a PR230 load-bearing physical-observable route.",
            "closure_status": "Uses H_unit/y_t_bare definitions and leaves SM physical readout out of scope.",
        },
        {
            "artifact": "PR #1023 / PR #1077 lambda(M_Pl) and beta-lambda bounded/no-go work",
            "classification": "conditional non-MC route context",
            "transfer_to_pr230": "Numerically interesting but separate from O_H/source-Higgs.",
            "closure_status": "beta_lambda(M_Pl)=0 remains an extra stationarity premise.",
        },
        {
            "artifact": "PR #1131 / PR541 plaquette Picard-Fuchs bridge work",
            "classification": "exact-math method analogy",
            "transfer_to_pr230": "Shows how exact ODE proof can replace MC after the integral is defined.",
            "closure_status": "Does not define PR230 O_H, Z(beta,s,h), or y_t.",
        },
        {
            "artifact": "A3 route1 Higgs/Yukawa C3-breaking obstruction",
            "classification": "negative/obstruction context",
            "transfer_to_pr230": "Warns against relying on C3-equivariant symmetry labels alone.",
            "closure_status": "Does not supply the source-Higgs bridge.",
        },
        {
            "artifact": "Bougerol-Lacroix / staggered-blocking Lyapunov bridge round2",
            "classification": "bounded tautological bridge",
            "transfer_to_pr230": "Mostly cautionary: operator-norm identities can restate inputs.",
            "closure_status": "Not relevant for physical O_H or y_t.",
        },
        {
            "artifact": "W/Z response-ratio and additive-top subtraction contracts",
            "classification": "exact future-row support",
            "transfer_to_pr230": "Strong fallback if a strict physical-response packet is produced.",
            "closure_status": "Needs accepted action, W/Z rows, top rows, covariance, strict g2, and delta_perp.",
        },
    ]


def route_recommendations() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "route": "Action-first canonical O_H plus source-Higgs rows",
            "next_artifact": "Accepted same-surface EW/Higgs action or Cl(3)/Z3 derivation, then C_ss/C_sH/C_HH pole rows.",
            "why_best": "Directly retires the named missing bridge and uses FMS correctly.",
            "blocking_imports": ["same-surface action", "canonical O_H", "strict pole rows", "Gram/FV/IR"],
            "proposal_allowed_now": False,
        },
        {
            "rank": 2,
            "route": "Strict W/Z matched physical-response packet",
            "next_artifact": "Production W/Z rows, same-source top rows, matched covariance, strict non-observed g2, delta_perp.",
            "why_best": "Can bypass explicit source-Higgs overlap if all physical response authority is present.",
            "blocking_imports": ["accepted action", "W/Z rows", "top rows", "covariance", "g2", "delta_perp"],
            "proposal_allowed_now": False,
        },
        {
            "rank": 3,
            "route": "Neutral primitive/rank-one theorem",
            "next_artifact": "Physical positivity-improving transfer kernel or off-diagonal neutral generator plus source-Higgs coupling.",
            "why_best": "Only plausible theorem-only route to source-Higgs uniqueness.",
            "blocking_imports": ["physical transfer", "irreducibility", "canonical coupling"],
            "proposal_allowed_now": False,
        },
        {
            "rank": 4,
            "route": "Exact math after object definition",
            "next_artifact": "Define Z(beta,s,h) or strict response functional first, then use PF/WZ/Herglotz/tensor certificates.",
            "why_best": "Good accelerator, not a bridge by itself.",
            "blocking_imports": ["defined operator/action/functional"],
            "proposal_allowed_now": False,
        },
    ]


def main() -> int:
    print("PR230 block30 full-approach assumptions/Elon/lit/math/bridge review")

    parent_presence = {key: exists(path) for key, path in PARENT_FILES.items()}
    block28 = load_json(PARENT_FILES["block28_certificate"])
    block29 = load_json(PARENT_FILES["block29_wz_pivot_certificate"])
    assumptions = assumptions_exercise()
    elon = elon_exercise()
    lit = literature_search()
    math = math_search()
    bridge = repo_bridge_cross_check()
    routes = route_recommendations()

    skill_text = read_text("/Users/jonBridger/.codex/skills/physics-loop/SKILL.md")
    # Absolute-path read fallback; ROOT-relative helper returns empty for this.
    skill_path = Path("/Users/jonBridger/.codex/skills/physics-loop/SKILL.md")
    if skill_path.exists():
        skill_text = skill_path.read_text(encoding="utf-8", errors="replace")

    report("parent-files-present", all(parent_presence.values()), f"{sum(parent_presence.values())}/{len(parent_presence)} parent files present")
    report("block28-loaded", bool(block28), "block28 certificate loaded")
    report("block29-loaded", bool(block29), "block29 W/Z pivot certificate loaded")
    report("proposal-still-forbidden", not block28.get("proposal_allowed", True), "block28 does not authorize proposal wording")
    report("block29-proposal-still-forbidden", not block29.get("proposal_allowed", True), "block29 W/Z pivot does not authorize proposal wording")
    report("assumptions-count", len(assumptions) >= 16, f"{len(assumptions)} assumptions stress-tested")
    report("assumptions-have-retirement-paths", all(a.get("falsifier_or_retirement_path") for a in assumptions), "every assumption has a retirement/falsifier path")
    report("elon-canonical-absent", "Elon" not in skill_text, "no canonical Elon section found in physics-loop skill")
    report("elon-interpretation-recorded", not elon["canonical_skill_section_found"], "first-principles/10x interpretation recorded")
    report("zeroth-principles-chain-recorded", len(elon.get("zeroth_principles_chain", [])) >= 5 and bool(elon.get("irreducible_missing_object")), "substrate-to-y_t primitive chain recorded")
    report("literature-count", len(lit) >= 6, f"{len(lit)} literature sources classified")
    report("math-count", len(math) >= 6, f"{len(math)} math sources classified")
    report("repo-bridge-count", len(bridge) >= 10, f"{len(bridge)} repo bridge artifacts cross-checked")
    report("each-lit-classified", all(s.get("import_class") for s in lit), "literature imports classified")
    report("each-math-classified", all(s.get("import_class") for s in math), "math imports classified")
    report("ward-not-load-bearing", any("Ward" in b["artifact"] and "not a PR230 load-bearing" in b["transfer_to_pr230"] for b in bridge), "Ward work kept out of PR230 load-bearing route")
    report("beta-lambda-not-closure", any("beta-lambda" in b["artifact"] and "stationarity premise" in b["closure_status"] for b in bridge), "beta-lambda remains conditional")
    report("plaquette-pf-analogy-only", any("Picard-Fuchs" in b["artifact"] and "Does not define PR230" in b["closure_status"] for b in bridge), "PF math marked as method analogy")
    report("top-route-action-first", routes[0]["route"].startswith("Action-first"), routes[0]["route"])
    report("no-route-proposal-now", not any(r["proposal_allowed_now"] for r in routes), "all routes remain non-proposal on current surface")

    output: dict[str, Any] = {
        "artifact": "yt_pr230_block30_full_approach_assumptions_elon_lit_math_bridge_review",
        "date": "2026-05-11",
        "actual_current_surface_status": "bounded-support / full-approach exercise and repo-bridge review; PR230 y_t closure remains open",
        "conditional_surface_status": (
            "Exact support if a future accepted same-surface O_H/action plus strict C_ss/C_sH/C_HH rows exists, "
            "or if a strict W/Z physical-response packet or neutral primitive/rank-one theorem is supplied."
        ),
        "proposal_allowed": False,
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "parent_presence": parent_presence,
        "block28_summary": {
            "proposal_allowed": block28.get("proposal_allowed"),
            "checks": block28.get("checks", {}),
        },
        "block29_wz_pivot_summary": {
            "proposal_allowed": block29.get("proposal_allowed"),
            "route_admission": block29.get("route_admission", {}),
            "checks": block29.get("checks", {}),
        },
        "assumptions_exercise": assumptions,
        "elon_exercise": elon,
        "literature_search": lit,
        "math_search": math,
        "repo_bridge_cross_check": bridge,
        "route_recommendations": routes,
        "forbidden_load_bearing_inputs": [
            "yt_ward_identity as PR230 closure",
            "H_unit-to-top matrix element",
            "y_t_bare definition-as-derivation",
            "observed top mass/y_t/W/Z/g2 target selectors",
            "alpha_LM/u0/plaquette chain as y_t proof input",
            "kappa_s=c2=Z_match=g2=1 conventions",
            "renaming C_sx/C_xx as C_sH/C_HH before O_H is certified",
        ],
        "decision": (
            "The best next PR230 route is still action-first O_H authority plus source-Higgs pole rows. "
            "Strict W/Z response is the main fallback. Neutral primitive/rank-one is the theorem-only fallback. "
            "Other bridge work supplies context, methods, or separate lanes, not current PR230 closure."
        ),
        "passes": PASS_COUNT,
        "fails": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"\nWrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
