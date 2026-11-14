# Stage 1 Kaggle Writeup Rubric & Audit Checklist

**Competition:** Physical-Engineering's Last Exam (PLE)  
**Total Points:** 100  
**Qualification Gate:** Top 100 submissions advance to Stage 2 hidden test set evaluation  
**Maximum Length:** 2,000 words  

---

## 📋 The 100-Point Evaluation Rubric

| Criterion | Points | Focus Areas & Scoring Triggers |
| :--- | :---: | :--- |
| **1. Insight & Failure Analysis** | **25** | • Non-obvious domain insights into physical engineering agents.<br>• Real dev-set failures documented (drawing callouts, code clauses, unit errors, early exits).<br>• Controlled ablations ("Adding mechanism X improved score from A to B").<br>• Negative results ledger (ideas that sounded good but failed). |
| **2. Engineering Reasoning** | **25** | • Concrete end-to-end case study of a real dev-set task.<br>• Side-by-side comparison of agent trajectory vs. licensed Professional Engineer (PE) workflow.<br>• Analysis of reasoning shortcuts, hallucinations, and corrections.<br>• Key domain skills identified (reading CAD/BIM, verifying code tables, numerical solvers). |
| **3. Cross-Model Generalizability** | **15** | • Benchmark across all 29 public dev tasks with $\ge 2$ models / model families.<br>• Model comparison table with task-level and discipline-level breakdown.<br>• Identification of universal improvements vs model-specific interventions.<br>• Target sponsored `model_api` in `submission.yaml` clearly justified. |
| **4. Efficiency & Scaling** | **20** | • Dev score vs compute budget / cost curve ($/task, token usage, verification attempts).<br>• Identification of score plateaus and saturation thresholds.<br>• Analysis of performance-cost Pareto efficiency for Stage 2 qualification (mean score $\ge 0.138$). |
| **5. Clarity & Visuals** | **15** | • High-signal executive presentation tailored for ML researchers without PE background.<br>• Clear headline finding placed near the top.<br>• Inclusion of the 3 required figures in clean 16:9 format.<br>• Strict compliance with the < 2,000-word limit. |

---

## 🔍 Pre-Submission Audit Checklist

### 1. Mandatory Submission Metadata
- [ ] Writeup submitted under the official Kaggle Writeups tab before January 5, 2027.
- [ ] GitHub repository URL linked under `Project Links`.
- [ ] Exact 40-character commit SHA (`git rev-parse HEAD`) stated at the top of the writeup.
- [ ] Cover image uploaded to Kaggle Writeup Media Gallery.
- [ ] Total word count is strictly **under 2,000 words** (verify via `wc -w`).

### 2. Required Figures (16:9 PNG, No Raw Mermaid)
- [ ] **Figure 1:** System Architecture Diagram (`docs/images/figure1_architecture_diagram.png`)
- [ ] **Figure 2:** Score vs Cost Scaling Curve (`docs/images/figure2_score_vs_cost.png`)
- [ ] **Figure 3:** Dev-Set Domain Failure Breakdown (`docs/images/figure3_devset_failure_breakdown.png`)

### 3. Repository Root Compliance
- [ ] `submission.yaml` present with one of the 8 approved `google-cloud/*` models.
- [ ] `serve.py` present (binds to `0.0.0.0:$PORT` within 120s over WebSocket).
- [ ] `harness.py` present.
- [ ] `LICENSE` present (`Apache-2.0` or `MIT`).
- [ ] `artifacts/` committed as an unpacked directory ($\le 512$ MiB, $\le 10,000$ files, no Git LFS, no symlinks).
- [ ] Passes `uv run python -m kit check` and `uv run python -m kit artifacts`.

### 4. Security & Privacy Checks
- [ ] Zero API keys, secrets, or credential tokens in tracked files (`tools/checks/check_secrets.py`).
- [ ] No local home directories or absolute user paths in writeup (`/Users/...` or `/home/...`).
