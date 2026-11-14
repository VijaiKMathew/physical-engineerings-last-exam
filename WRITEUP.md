# Aero-Aegis: Multi-Modal Spatial Vector Grounding & Deterministic Verification Loops

- **Repo:** https://github.com/VijaiKMathew/physical-engineerings-last-exam
- **Commit SHA:** `6b507fd8d63577f679e91827379ae77e9f74ff62`
- **Primary model_api:** `google-cloud/gemini-4-argon`
- **Other models tested:** `google-cloud/claude-opus-5-5`, `google-cloud/gemini-3.8-flash`, `google-cloud/llama-4-maverick`, `google-cloud/gemma-4-26b`
- **Dev score (29 tasks):** **0.608** | **$3.80/task** | **42 min/task**

---

## 1. Insights & Failures (25 pts)

Physical engineering is fundamentally different from conversational question-answering or synthetic programming: **physics does not care if your code compiles.** Real-world structural, civil, electrical, and mechanical deliverables require cross-checking up to 50 heterogeneous project files—including multi-sheet CAD vector drawings (`.dxf`), BIM models (`IFC4`), load schedules (`.xlsx`), soil boring logs, and regional regulatory codes—inside an isolated container with a strict 6-hour time limit.

### What Broke in Baseline PLE Runs
- **Spatial Drawing Misreads:** Unassisted models treating CAD drawings as flattened, downscaled raster images misread dense conduit indices and equipment callouts (e.g., reading `Circuit 13B` as `Circuit 138` in crowded panel schedules), causing catastrophic ampacity and short-circuit failures in 34% of baseline runs.
- **Regulatory Code Clause Mismatch:** Generalist frontier models repeatedly applied standard commercial or residential building codes (e.g., general branch lighting rules) rather than industrial mission-critical data center criteria (e.g., NEC Article 645 and ASHRAE TC 9.9 thermal envelopes), causing immediate compliance failure.
- **Unit Conversion & Scale Drift:** Mismatches between imperial drafting callouts (inches, feet, CFM, PSI) and metric analytical equations (kW, L/s, kPa) created subtle 10x calculation errors that propagated into final equipment sizing.
- **Premature Termination Trap:** Faced with 50-file engineering specifications, unassisted agents frequently emitted `done` after completing only the first building pad or single feeder circuit, leaving multi-part rubrics completely unscored.
- **Geometric Clash Blindness:** Baseline agents attempted direct Euclidean point-to-point routing, passing 24-inch chilled-water pipes straight through primary structural steel shear columns and through NFPA 13 sprinkler clearance zones.

### 1.1 Failure Breakdown

![Figure 1: Failures by Discipline and Type](docs/images/figure3_devset_failure_breakdown.png)
*Figure 1: Failure rate and score distribution across all 4 physical engineering disciplines (Structural, Civil, Electrical, and Mechanical) comparing the unassisted baseline against our multi-agent verification harness on the 29 public dev tasks.*

Across the 29 public dev tasks, failure modes distributed into:
1. **Drawing Callout Misreads (34%):** Optical confusion over layered vector lines without coordinate querying.
2. **Regulatory Code Mismatch (26%):** Hallucinating or cross-applying non-applicable regional building codes.
3. **Unit Conversion & Scale Drifts (22%):** Inadvertent imperial/metric formula translation errors.
4. **Premature Completion (18%):** Dropping remaining engineering requirements due to token context exhaustion.

### 1.2 Ablations

| Config | Dev (29) | Str (4) | Civ (9) | Elec (9) | Mech (7) | $/task |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Baseline (Zero-Shot / pi-opus baseline) | 0.142 | 0.125 | 0.148 | 0.182 | 0.104 | $0.45 |
| + Vector & DXF/IFC Extraction Tools | 0.274 | 0.250 | 0.284 | 0.326 | 0.221 | $1.20 |
| + Deterministic Verification Gatekeeper | 0.452 | 0.425 | 0.462 | 0.510 | 0.380 | $2.15 |
| **Submitted (Aero-Aegis Champion + Gemini 4 Argon)** | **0.608** | **0.582** | **0.621** | **0.684** | **0.520** | **$3.80** |

### Ideas That Failed or Surprised Us
- **End-to-End Vision-Only Raster Ingestion (Failed):** Stitching multi-sheet high-res drawings into vision models exhausted context windows within 3 turns and failed to discern minute conductor gauge callouts. Switching to direct `.dxf` vector parsing and `IfcOpenShell` entity trees improved accuracy by +0.132.
- **Unconstrained Monte Carlo Tree Search (Failed):** Exploring open-ended routing possibilities without elevation tiering caused combinatorial explosion, exceeding the 6-hour container timeout on 4 out of 5 mechanical test tasks.
- **Surprise: Deterministic Verification is Model-Agnostic:** Enforcing non-negotiable physical constraint checkers before `done` boosted every tested model family by at least +0.20 points, demonstrating that grounding safeguards outweigh raw model scale.

---

## 2. Architecture & Reasoning (25 pts)

![Figure 2: System Architecture Diagram](docs/images/figure1_architecture_diagram.png)
*Figure 2: System Architecture: Multi-Modal Ingestion, Context Compactor, Hierarchical Planner, Tool Execution (OpenCASCADE / IfcOpenShell / MCP), and the Deterministic Collision-Traceback Verification Loop.*

### Control Loop & Core Mechanisms
1. **Perception & Spatial Parsing:** Directly parses `.dxf` vector geometry and `.ifc` BIM entities. Bounding-box spatial queries allow the agent to inspect specific equipment bays without loading whole sheets into token context.
2. **Context Compaction over 6-Hour Runs:** To prevent context degradation over 6-hour trajectories, we implement a **Sliding Key-Fact State Ledger**. Intermediate tool outputs (e.g. 5,000-line IFC geometric dumps) are digested into strict JSON coordinate tables and purged from conversational history, preserving under 32k active tokens.
3. **Timeout & Cancel Recovery:** Our `serve.py` WebSocket runner monitors container heartbeats. If a task exceeds 5.5 hours, the agent enters an **Emergency Deliverable Finalizer** mode, packaging all verified sub-modules and flushing stamped artifacts before the 6-hour container cutoff.
4. **Tooling & Streamable MCP:** Leverages OpenCASCADE geometry kernels, `IfcOpenShell`, `shapely` 2D boundary polygons, and analytical hydraulic/thermal solvers.

### Dev-Set Task Deep Dive: MEP Coordination (Hall B) vs. Practicing Engineer Workflow
In the **MEP Coordination (Halls A & B)** dev task, the agent must route clash-free IFC4 cable trays, busways, and chilled-water piping across 7 drawing sheets around an offset grid and 104 existing sprinkler heads.

- **Practicing Engineer Workflow:**
  1. *Grid & Elevation Tiering:* Establishes architectural datums and assigns vertical clearance bands (high-voltage electrical busways top, chilled water intermediate, gravity drainage bottom).
  2. *Constraint Mapping:* Identifies NFPA 13 sprinkler exclusion zones (12-inch radial clearance).
  3. *Orthogonal Routing & Clash Detection:* Runs iterative collision checks against structural steel beams.
  4. *Final Takeoff & Stamping:* Generates an IFC4 coordinate deliverable and schedules.
- **Agent Trajectory & Auto-Correction:**
  - *Initial Attempt:* The agent planned a direct Euclidean path for 24-inch chilled-water supply piping, resulting in 2 structural steel penetrations and 4 sprinkler clashes.
  - *Verification Gate Interception:* The deterministic verification gate parsed the geometry via `IfcOpenShell`, caught the collisions, and returned exact collision coordinates: `CLASH: (X=14200, Y=8450, Z=3800) with BEAM_W24x68`.
  - *Self-Correction:* The agent rerouted through an orthogonal 45-degree offset corridor, verifying zero clashes and outputting a compliant IFC model scoring **1.00** on automated spatial checks.

---

## 3. Cross-Model Generalizability (15 pts)

We evaluated our harness across 5 Google-sponsored foundation models from distinct architectural families on all 29 public dev tasks:

| model_api | Baseline | Yours | Delta | Tokens in / out / cached | $/task |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `google-cloud/gemini-4-argon` | 0.165 | **0.608** | **+0.443** | 185k / 24k / 142k | $3.80 |
| `google-cloud/claude-opus-5-5` | 0.170 | **0.595** | **+0.425** | 210k / 28k / 165k | $4.90 |
| `google-cloud/gemini-3.8-flash` | 0.118 | **0.442** | **+0.324** | 145k / 18k / 110k | $0.65 |
| `google-cloud/llama-4-maverick` | 0.095 | **0.388** | **+0.293** | 190k / 22k / 130k | $0.25 |
| `google-cloud/gemma-4-26b` | 0.082 | **0.365** | **+0.283** | 160k / 19k / 115k | $0.20 |

### Universal Gains vs. Model-Specific Sensitivities
- **Universal Gains:** The Deterministic Verification Gatekeeper and direct DXF/IFC vector extraction produced consistent gains ($\ge +0.28$) across all model families, preventing basic syntax corruption and physical collisions.
- **Model-Specific Differences:** Frontier models (`gemini-4-argon` and `claude-opus-5-5`) excelled at synthesizing multi-step parametric Python scripts on the first iteration, while smaller open-weight models (`gemma-4-26b`, `llama-4-maverick`) required 1–2 extra verification loops to correct sign and unit conventions.
- **Cost Efficiency:** `gemini-3.8-flash` achieved a score of **0.442** at just **$0.65/task**, beating the Stage 2 qualification threshold (0.138) by more than 3x on an ultra-low compute budget.

---

## 4. Efficiency & Scaling (20 pts)

![Figure 3: Score vs. Cost Pareto Frontier](docs/images/figure2_score_vs_cost.png)
*Figure 3: Score vs. Cost Pareto frontier across model families, verification budgets ($k=1$ to $k=5$), and reasoning token allocations.*

### Scaling Dynamics & Plateau Analysis
- **Verification Loop Budget ($k$):** At $k=1$ verification attempt, accuracy jumps from 0.274 to 0.452. At $k=3$, the system achieves optimal Pareto efficiency (**0.608** at **$3.80/task**).
- **Diminishing Returns:** Beyond $k=4$ loops, performance plateaus (0.612) while cost increases by 45%. Errors beyond $k=3$ stem from contradictory baseline project documents (e.g. conflicting elevation numbers across architectural vs. structural sheets) rather than agent routing failures.
- **Managing the 6-Hour Container Limit:** By utilizing local vector caching and keeping context compressed under 32k tokens, mean task latency is capped at **42 minutes**, leaving a 5-hour margin to prevent task timeouts.

---

## 5. Reproducibility & Audit Notes (15 pts)

- **Verification Confirmation:** Both official kit verification commands run cleanly on our submitted commit (`bbc04496f52b76fb8534a2d9c1f1eeb146e3a175`):
  ```bash
  # Check submission format and environment readiness
  uv run python -m kit check .

  # Verify 29 public dev task outputs and manifest
  uv run python -m kit artifacts .
  ```
- **License:** Fully licensed under `Apache-2.0`.
- **Reviewer Audit Notes:**
  - `submission.yaml` is pinned to `google-cloud/gemini-4-argon` with zero external egress.
  - All 28 non-empty task output bundles, final messages, and execution trajectories reside in the unpacked `artifacts/` folder ($\approx 26$ MiB, zero Git LFS, zero symlinks).
  - Reproducible figure generation script is available at `scratch/generate_writeup_figures.py`.
