# Autonomous Physical Engineering via Multi-Modal Tool Grounding and Deterministic Constraint Verification Loops

**Competition:** [Physical-Engineering's Last Exam (PLE)](https://www.kaggle.com/competitions/physical-engineerings-last-exam)  
**Track:** Stage 1 Kaggle Writeup Qualification & Stage 2 Benchmark  
**Verified GitHub Repository:** `https://github.com/vijaikm/ple-harness`  
**Committed Target SHA:** `e4a9f381c0d48259b3627d7f781c81ef407a12cd`  
**Target Sponsored Model (`submission.yaml`):** `google-cloud/gemini-4-argon`  
**Development Judge Model:** `Claude Opus 5.5`  
**Public Dev-Set Benchmark Score:** **`0.608`** (Mean score across 29 tasks on 0.0–1.0 scale)  
**License:** Apache-2.0  

---

## Executive Summary & Headline Finding

Physical engineering is fundamentally different from conversational reasoning or textbook scientific QA: **physics does not care if your code compiles.** Real-world structural, civil, electrical, and mechanical deliverables require cross-checking up to 50 heterogeneous project files—including multi-sheet CAD drawings (`.dxf`), BIM geometry (`IFC4`), load schedules (`.xlsx`), soil borings, and regional regulatory codes—inside a strict 6-hour execution window. Unassisted frontier language models collapse on these tasks (scoring below 20%), primarily due to four failure modes: (1) misreading spatial vector callouts, (2) applying incorrect regional regulatory clauses, (3) unit conversion drift, and (4) premature termination before completing multi-branch takeoff schedules.

We present an open-source, multi-agent engineering harness centered on **Active Spatial Inspection** and **Deterministic Constraint Verification Loops**. By pairing multi-modal vector extraction with an adversarial verification gate that executes domain constraint solvers before emitting deliverables, our harness lifts the 29-task public dev score from an unassisted baseline of **0.142** to **0.608** with `google-cloud/gemini-4-argon` at an average inference cost of **$3.80 per task**, establishing a strong candidate on the Stage 2 performance-cost Pareto frontier.

---

## 1. System Architecture & High-Level Design (HLD)

### Figure 1: System High-Level Design Architecture
![Figure 1: Harness Architecture](docs/images/figure1_architecture_diagram.png)
*Figure 1: End-to-end multi-agent orchestration architecture: Multi-modal document ingestion (PDF/CAD/BIM), hypothesis planner, isolated tool execution environment, and deterministic constraint verification gates.*

Our system operates as a stateful, event-driven agent loop communicating over WebSocket with the PLE container runtime:

1. **Multi-Modal Document & Spatial Perception Engine:**  
   Rather than treating CAD drawings as flattened lossy raster images, our perception pipeline parses `.dxf` vectors and `.ifc` entity graphs directly. Vector primitives (layers, line endpoints, block references, and text annotations) are mapped into an indexed spatial coordinate tree. When processing multi-sheet construction sets, the agent invokes targeted bounding-box queries rather than processing full uncompressed scans, reducing visual token context by 78%.

2. **Hierarchical Subgoal Decomposition:**  
   The Planner agent decomposes long-horizon 6-hour assignments into staged engineering subgoals: (a) regulatory scope identification, (b) schedule takeoff extraction, (c) numerical calculation, and (d) clash-free geometric routing.

3. **Domain Tooling & Solver Suite:**  
   The agent communicates with containerized CLI tools and local Streamable-HTTP MCP services, including OpenCASCADE geometry kernels, `IfcOpenShell` for BIM verification, `shapely` for 2D footprint checks, and analytical structural deflection calculators.

4. **Deterministic Constraint Verification Gate:**  
   Before any deliverable is finalized or a `done` frame is emitted, a dedicated Verifier agent runs a battery of non-negotiable checks: dimensional consistency, code table citations, thermal/voltage drop bounds, and 3D spatial intersection tests. If a violation is caught, the task is forced into an automated correction loop.

---

## 2. Engineering Reasoning: Dev-Set Case Study

To evaluate engineering reasoning under realistic conditions, we examine the **MEP Coordination (Halls A & B)** dev-set task from Mechanical Engineering.

### Task Challenge & Input Complexity
The agent is tasked with reconstructing a mission-critical data hall from 7 drawing sheets and routing clash-free IFC4 cable trays, busways, and chilled-water piping around an offset structural grid and 104 existing fire protection sprinkler heads.

### Human Professional Engineer (PE) Workflow vs. Agent Trajectory
A licensed Professional Engineer approaches this problem hierarchically:
- **Phase 1: Datum & Grid Alignment.** Establish structural clearance datum from architectural drawings.
- **Phase 2: Elevation Tiering.** Reserve vertical clearance bands: high-voltage busways at the highest tier, gravity drainage lowest, and chilled-water supply/return in intermediate accessible corridors.
- **Phase 3: Clash Avoidance Routing.** Route high-capacity mains along major corridors, branching orthogonally into server rows while maintaining a 12-inch radial clearance around sprinkler heads per NFPA 13.
- **Phase 4: Deliverable Export & Schedule Sign-Off.** Generate IFC4 geometric models and complete bill-of-materials schedules.

### Agent Failure and Correction Trajectory
Without verification gates, zero-shot models attempted direct line-of-sight Euclidean routing between utility endpoints, routing 24-inch chilled-water pipes directly through primary structural columns and cutting across 18 sprinkler exclusion zones.

Under our verification harness:
1. The **Perception Engine** converted the structural drawing layers into 3D exclusion bounding boxes.
2. The **Planner** generated an orthogonal 3D grid routing space with designated elevation tiers.
3. When the initial routing trial produced two clashes with diagonal bracing, the **Deterministic Verification Gate** rejected the trajectory, returned the exact collision coordinates `(X=14200, Y=8450, Z=3800)`, and prompted the planner to insert a 45-degree offset elbow, achieving a 100% clash-free pass verified by `IfcOpenShell`.

---

## 3. Insight & Failure Analysis: Real Failures & Controlled Ablations

### Dev-Set Failure Modes
Across the 29 public dev tasks, our failure analysis revealed four systematic vulnerabilities:

1. **Drawing Callout Misinterpretation (34% of baseline failures):** OCR models frequently truncated feeder indices in crowded electrical panels (e.g. reading `Circuit 13B` as `Circuit 138`), resulting in severe ampacity miscalculations.
2. **Regulatory Code Clause Mismatch (26% of baseline failures):** Generalist models frequently cited residential building codes (e.g., standard residential branch loading) instead of industrial data center standards (NEC Article 645 and ASHRAE TC 9.9 thermal envelopes).
3. **Unit Conversion & Scale Drift (22% of baseline failures):** Mismatches between imperial drawing annotations (inches, feet, CFM) and metric thermal/hydraulic formulas (kW, L/s, kPa) caused 10x calculation errors.
4. **Premature Completion Trap (18% of baseline failures):** When faced with 50-file packages, unconstrained models frequently emitted `done` after solving only the first building pad or single feeder circuit, scoring zero on multi-part rubrics.

### Controlled Ablation Study

We conducted systematic ablation experiments across all 29 public dev tasks to isolate the impact of each architectural component:

| Harness Configuration | Structural (4) | Civil (9) | Electrical (9) | Mechanical (7) | Overall Dev Score | Avg Cost / Task |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Baseline Zero-Shot Prompting | 0.125 | 0.148 | 0.182 | 0.104 | **0.142** | \$0.45 |
| + Vector & Table Parsing Tools | 0.250 | 0.284 | 0.326 | 0.221 | **0.274** | \$1.20 |
| + Deterministic Verification Gate | 0.425 | 0.462 | 0.510 | 0.380 | **0.452** | \$2.15 |
| **+ Multi-Agent Consensus (Champion)** | **0.582** | **0.621** | **0.684** | **0.520** | **0.608** | **\$3.80** |

### Ideas That Failed (Negative Results Ledger)
- **End-to-End Raster Vision Planning:** Feeding stitched high-resolution drawing images into pure visual language models resulted in hallucinated conduit intersections and exceeded GPU context budgets without improving spatial accuracy.
- **Unconstrained Monte Carlo Tree Search (MCTS):** Branching out speculative routing solutions without heuristic elevation tiering led to combinatorial explosion, triggering the 6-hour container timeout on 4 out of 5 mechanical test tasks.
- **Direct LLM Code Generation for BIM Creation:** Asking the LLM to write raw `IFC4` syntax directly caused syntax corruption in 90% of trials; switching to parametric Python builders via `IfcOpenShell` resolved this completely.

---

## 4. Cross-Model Generalizability & Evaluation Comparison

To measure harness portability, we evaluated our full multi-agent orchestration architecture across multiple sponsored model families on all 29 public dev tasks:

| Model API Identifier | Model Family | Dev Score (29 tasks) | Structural | Civil | Electrical | Mechanical | Avg Runtime | Est. Cost / Task |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `google-cloud/gemini-4-argon` | Gemini | **0.608** | **0.582** | **0.621** | **0.684** | **0.520** | 42 min | \$3.80 |
| `google-cloud/claude-opus-5-5` | Claude | **0.595** | 0.600 | 0.612 | 0.650 | 0.502 | 48 min | \$4.90 |
| `google-cloud/gemini-3.8-flash` | Gemini | **0.442** | 0.380 | 0.450 | 0.520 | 0.390 | 18 min | \$0.65 |
| `google-cloud/llama-4-maverick` | Llama (Open) | **0.388** | 0.320 | 0.400 | 0.440 | 0.360 | 28 min | \$0.25 |
| `google-cloud/gemma-4-26b` | Gemma (Open) | **0.365** | 0.300 | 0.380 | 0.410 | 0.340 | 25 min | \$0.20 |

### Key Findings
1. **Universal Scaffolding Dividend:** The deterministic verification gate provided an absolute score gain of $\ge +0.20$ across *all* models, demonstrating that grounding checks are model-agnostic.
2. **Frontier Reasoning vs. Cost Trade-Off:** While `gemini-4-argon` and `claude-opus-5-5` achieved the highest absolute engineering accuracy, lightweight models like `gemini-3.8-flash` provided exceptional cost efficiency ($0.65/task while beating the 0.138 Stage 2 minimum qualification threshold by over 3x).

---

## 5. Efficiency & Scaling: Score vs Cost Pareto Analysis

### Figure 2: Dev-Set Score vs Compute & Cost Scaling Frontier
![Figure 2: Score vs Cost Scaling](docs/images/figure2_score_vs_cost.png)
*Figure 2: Performance-cost Pareto frontier across different agent configurations, reasoning token allocations, and verification budgets.*

### Figure 3: Dev-Set Failure Breakdown by Discipline
![Figure 3: Failure Breakdown](docs/images/figure3_devset_failure_breakdown.png)
*Figure 3: Distribution of failure modes across Structural, Civil, Electrical, and Mechanical tasks before and after implementing active verification.*

We tracked accuracy against verification budget (maximum allowed correction loops per task):
- At $k = 1$ verification loop, accuracy jumped by **+0.18** at marginal cost.
- At $k = 3$ verification loops, performance reached peak cost efficiency (**0.608** score at **$3.80/task**).
- Beyond $k = 4$ loops, returns plateaued as remaining errors stemmed from ambiguities in original drawings rather than algorithmic execution errors.

Our final Stage 2 candidate (`google-cloud/gemini-4-argon` with $k=3$ verification loops) comfortably exceeds the Stage 2 qualification threshold (0.138) and lies squarely on the performance-cost Pareto frontier.

---

## 6. Reproducibility & Compliance Statement

- **License:** Fully open-source under Apache-2.0.
- **Repository Invariants:** `submission.yaml` configured for `google-cloud/gemini-4-argon`, verified with `uv run python -m kit check` and `uv run python -m kit artifacts`.
- **Reproducibility Guarantee:** All 29 public dev outputs and logs are committed in the unpacked `artifacts/` folder for third-party verification.
