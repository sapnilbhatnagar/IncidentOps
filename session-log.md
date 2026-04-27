# Session Log: Tomoro.ai Work Product

A continuous audit trail of decisions, scope, and where we left off. Read this first when resuming work.

> **Naming note (2026-04-27).** The product was renamed from "Ops Resilience Copilot" to **IncidentOps** in Session 5. Earlier entries below preserve the original name as historical record. Any reference in Sessions 1-4 to "Ops Resilience Copilot", "ops-resilience-copilot/", or paths under that folder maps to "IncidentOps" / "incidentops/" in current state.
>
> **Domain pivot note (2026-04-26).** The product domain was pivoted from UK retail bank payment ops (NorthStar Bank archetype, FPS scheme) to enterprise SaaS support ops (VertexCloud archetype) in Session 4. Sessions 1-3 entries that mention NorthStar, FPS, VocaLink, or payment-scheme terminology describe the pre-pivot state and the corpus that was deleted as part of the pivot. The current corpus is SaaS-only.

---

## 1. Project at a glance

| Field | Value |
|---|---|
| **Project goal** | Build an unsolicited application work product to pursue AI Delivery Lead and Product Manager roles at Tomoro.ai |
| **Chosen use case** | IncidentOps for enterprise SaaS support and platform operations |
| **Target buyer (illustrative)** | VP Customer Support or VP Customer Operations at an enterprise multi-product SaaS company ("VertexCloud" archetype, modelled on Salesforce / ServiceNow / Qinecsa Solutions tier) |
| **Primary deliverable** | Working prototype + 12-page Tomoro-style proposal + 3-min Loom + outreach note |
| **Status** | Brief complete. Ready to enter planning + build. |
| **Active brief** | `incidentops-brief.md` (this folder) |

---

## 2. Decision log

### 2026-04-27: Session 5, Phase 0 — rename to IncidentOps, git init, contradiction cleanup

**What happened.** Plan mode produced an 8-phase build plan (`C:\Users\Sapnil Bhatnagar\.claude\plans\snazzy-sparking-galaxy.md`). User scoped out application packaging (proposal/Loom/outreach) and renamed the product from "Ops Resilience Copilot" to **IncidentOps**. Phase 0 executed.

**What changed.**
- Brief file renamed: `ops-resilience-copilot-brief.md` → `incidentops-brief.md`. Title and repo-tree references inside the brief updated.
- Corpus folder renamed: `ops-resilience-copilot/` → `incidentops/`. All paths shift accordingly.
- README, INC001, INC002 copy updated to use "IncidentOps".
- Session log: added top-of-file naming + pivot banner so historical entries (Sessions 1-4) remain intact but are clearly flagged as pre-rename / pre-pivot context.
- HHH metric table added to brief section 7 (numbered table of dimension → metric → grader → pass-bar).
- New file: `incidentops/data/gold-set-spec.md` — schema for labelled incidents (the bottleneck for every downstream eval phase).
- Repo placed under git: `git init` at folder root, `.gitignore` added, initial commit `chore: scaffold IncidentOps prototype`.

**What did not change.** Architecture, six-stage pipeline, read-only invariant, two-tier routing, HHH eval philosophy, KPI structure, corpus content (only renames + naming sweep, no rewrites).

**Implications for next session.** Phase 1 begins: repo scaffold (`agent/`, `evals/`, `dashboard/`, `ops/`), tooling pin (Python 3.12 + uv, Next.js 14 + pnpm, Inspect AI, LanceDB), and corpus expansion from seed to floor (5 → 15 runbooks, 10 → 80 tickets, 2 → 8 incidents, gold set seeded with 30 labelled incidents). The gold-set spec is the contract Phase 1 generation must satisfy.

---

### 2026-04-26: Session 4, Domain pivot from banking to SaaS

**What happened.** User decided the brief should target enterprise SaaS companies (Salesforce, ServiceNow, Qinecsa Solutions tier) rather than UK retail banking. Rationale: "all SaaS companies face this problem" and the TAT (turnaround time) improvement story is universal across SaaS support ops. Architecture decisions remain unchanged.

**Decision.** Pivot the entire deliverable from UK retail bank payment ops to enterprise multi-product SaaS support and platform ops.

**What changed.**

- **Brief** (`ops-resilience-copilot-brief.md`): full domain rewrite. Buyer changed from COO/Director of Payment Ops to VP Customer Support / VP Customer Operations. Synthetic archetype changed from NorthStar Bank to VertexCloud. Scheme scope (FPS) replaced with product-surface scope (Integration and API support). Regulatory framing changed from PS21/3 / DORA / FCA Consumer Duty to SOC 2 / ISO 27001 / GDPR / contractual SLAs. KPIs updated: MTTR replaced by TAT; business KPIs now CSAT, NRR, SLA breach rate, expansion velocity.
- **Corpus** (`ops-resilience-copilot/data/`): full corpus rebuild.
  - `reference/fps-reason-codes.json` deleted, replaced with `reference/saas-issue-codes.json` (30 SaaS issue codes across Auth, RateLimit, Webhook, DataSync, Permission, Integration, Performance, Availability families).
  - 5 runbooks renamed and rewritten: RB001 (auth/SSO/OAuth/SAML/MFA), RB002 (rate limit/quota), RB003 (webhook delivery), RB004 (data sync and consistency), RB005 (multi-tenant permission/ACL).
  - 2 incidents renamed and rewritten: INC001 (webhook cascading failure, 11 Sep 2025, 12,438 events delayed), INC002 (data sync lag near-miss, 4 Feb 2026, 47 tenants affected, $185k credit avoided).
  - 10 tickets in `tickets.jsonl` rewritten with SaaS scenarios: 401 after IdP cert rotation, 429 retry storm, webhook cert expiry, WHK-RETRY-EXHAUSTED on staging endpoint, suspected cross-tenant access, data sync lag, signature mismatch on rotation, dual-region API gateway latency, SDK dedup regression, OAuth scope removed.
  - Telemetry rewritten: `sample-logs.jsonl` updated with VC-* service log lines; `sample-switch-records.jsonl` deleted, replaced with `sample-request-records.jsonl` (API + webhook records).
- **Internal system naming**: NS-PaySwitch → VC-API-Gateway; NS-CoreBank → VC-DataPlatform; NS-ObsHub → VC-Observability; NS-Tickets → VC-Support. Added: VC-Identity, VC-Webhooks, VC-Sync.

**What did not change.**

- Six-stage agent pipeline (triage, retrieval, diagnosis, tool use, remediation, handoff).
- Read-only invariant by architecture.
- Provenance-first.
- Two-tier model routing.
- Three-tier KPI structure (agent / ops / business).
- Eval taxonomy (six categories: retrieval, reasoning, action, safety, UX, business).
- Stack: Claude Agent SDK, Inspect AI + custom Python graders, Next.js on Vercel.
- 12-week build sequence shape.
- Repo visibility, outreach plan, all decisions from Sessions 1-3.

**Files affected (this session).**
- Modified: `ops-resilience-copilot-brief.md`, `session-log.md`, `ops-resilience-copilot/data/README.md`, `ops-resilience-copilot/data/tickets/tickets.jsonl`, `ops-resilience-copilot/data/telemetry/sample-logs.jsonl`.
- Created: `ops-resilience-copilot/data/reference/saas-issue-codes.json`, 5 new runbooks (RB001-RB005 with SaaS slugs), 2 new incidents (INC001 webhook, INC002 data sync), `ops-resilience-copilot/data/telemetry/sample-request-records.jsonl`.
- Deleted: `ops-resilience-copilot/data/reference/fps-reason-codes.json`, 5 FPS runbooks, 2 FPS incidents, `ops-resilience-copilot/data/telemetry/sample-switch-records.jsonl`.

**Implications for next session.** Module-by-module `/plan` flow is unchanged. Eval suite first per build-order decision, then retrieval pipeline. The plan does not need re-derivation; only the corpus retrieval will operate over SaaS knowledge instead of FPS knowledge.

---

### 2026-04-26: Session 1, Discovery and use case selection

**What happened.** Did deep research on Tomoro.ai across four angles in parallel: case studies, company shape, AI Delivery Lead job description, and AI delivery patterns. Synthesised findings into the seven-test "Tomoro-shaped work product" filter. Generated three use case candidates:

- **A.** FNOL Concierge for a UK general insurer (multimodal voice + image agent).
- **B.** Buy-side Analyst Copilot for an asset manager (multi-agent equity research).
- **C.** Ops Resilience Copilot for a UK retail bank's payment ops (grounded action-aware agent).

**Decision.** User selected **Use Case C (Ops Resilience Copilot)**.

**Reasoning recorded.** Best fit for AI Delivery Lead role specifically. Highest score on the seven-test filter (33 / 35). Strongest governance and prototype-to-production story. Clean adjacency to OakNorth (existing Tomoro client, but in credit underwriting, not payment ops, so no overlap with shipped work).

**Files created.** `tomoro-ai-work-product-brief.md` (the three-option brief). Subsequently superseded by the deep brief on Use Case C and **deleted to keep the repo clean** per user instruction.

---

### 2026-04-26: Session 3, Stack swap and seed dataset

**Stack updated** (brief §9.2 and §9.3): Claude Agent SDK in place of OpenAI Agents SDK; Next.js on Vercel in place of Streamlit; Inspect AI as the eval runner with custom Python deterministic graders alongside.

**Seed corpus built** at `ops-resilience-copilot/data/`. Coverage:

- `README.md`: corpus design, scaling spec, conventions for the synthetic NorthStar Bank archetype.
- `reference/fps-reason-codes.json`: 30 ISO 20022 FPS reason codes, paraphrased; complete for prototype scope.
- `runbooks/`: 5 high-quality exemplars (RB001 account-class rejects; RB002 settlement failure; RB003 cut-off window breach surge; RB004 duplicate payment; RB005 Vocalink gateway degradation). Templates established for the remaining 45.
- `incidents/`: 2 post-incident reports (INC001 Vocalink edge degradation 11 Sep 2025 with 5-whys; INC002 settlement near-miss 4 Feb 2026). Templates established for the remaining 18.
- `tickets/tickets.jsonl`: 10 well-structured tickets, each with gold-runbook label, gold-root-cause label, and gold-remediation label. JSONL schema established for the remaining 190.
- `telemetry/`: 15 log lines and 6 switch records consistent with the ticket scenarios.
- `gold/`: empty. Built after the seed corpus is reviewed.

**Quality bar.** Every artefact written to be plausible to a real UK FPS ops engineer. Real schemes (FPS), real operators (Pay.UK, Vocalink, BoE RTGS), real ISO 20022 reason code conventions. All NorthStar internal systems invented but plausible (`NS-PaySwitch`, `NS-CoreBank`, `NS-ObsHub`, `NS-Tickets`).

**Next session entry point.** Move into module-by-module feature planning using the /plan flow. The dataset is the foundation; agent pipeline modules can now be scoped against real retrieval material.

---

### 2026-04-26: Session 2, Deep dive on Use Case C

**What happened.** Expanded the Ops Resilience Copilot brief into a full product, delivery and AI brief. Designed the evaluation strategy as the centre of gravity of the document, since Tomoro's stated POV is that trace-based evals are the new substrate for enterprise AI.

**Specific design decisions taken.**

1. **Agent architecture is a six-stage pipeline**, not a monolithic prompt. Stages: triage, retrieval, diagnosis, tool use, remediation, handoff.
2. **Read-only invariant by architecture**, not by policy. Mutating tools physically not in the registry.
3. **Two-tier model routing**: small model for triage and tool shaping, frontier model for diagnosis and remediation. Inherits the Supercell pattern.
4. **Knowledge sources**: Confluence runbooks, ServiceNow tickets, post-incident reports, scheme reference data. Hybrid retrieval (vector + BM25) with reranker.
5. **Memory**: per-turn and per-incident only. No implicit cross-incident learning. Deliberate choice to support model risk management.
6. **Adoption phasing**: Shadow, then Assist, then Guided. Full autonomy is not the destination.
7. **Eval taxonomy**: 6 categories (retrieval, reasoning, action, safety, UX, business). Each has a set of metrics and gates.
8. **Eval execution loops**: pre-merge CI, nightly replay, champion / challenger, live shadow, quarterly red team.
9. **Promotion gates**: tech, risk, operational. None bypassable.
10. **Prototype scope locked**: FPS-only, "NorthStar Bank" archetype, 50 runbooks, 200 tickets, 20 incidents, 200-incident gold set.

**Files created.**
- `ops-resilience-copilot-brief.md` (active brief).
- `session-log.md` (this file).

**Files deleted.**
- `tomoro-ai-work-product-brief.md` (superseded; user requested clean repo).

---

## 3. Open decisions to resolve in the next session

Each one is a concrete pick-up point. None blocks starting build.

1. ~~**Agent framework**~~: **RESOLVED 2026-04-26.** Initially picked OpenAI Agents SDK; reverted same session to **Claude Agent SDK** at user request, driven by cost (user already pays for Claude, does not want to subscribe to OpenAI separately). Narrative reframe locked in: the choice is positioned in the proposal as a deliberate demonstration of multi-provider portability, consistent with Tomoro's published "avoid vendor lock-in" POV. Architecture remains provider-neutral: a thin model wrapper, swappable. Teaching of Claude Agent SDK to be done at build time, not as prep. **Implication for §9 of the brief**: the tech stack section must be updated to swap "OpenAI Agents SDK" for "Claude Agent SDK" and the proposal narrative must add the multi-provider framing.
2. ~~**Eval framework**~~: **RESOLVED 2026-04-26.** **Inspect AI** as the runner, plus custom Python for deterministic graders (retrieval recall, citation existence, read-only invariant). Reasons: UK AISI provenance is a credibility transfer to a UK Tomoro panel; provider-agnostic so it stays consistent with the Claude-first multi-provider architecture; trace-based by design, which is the exact phrase from Tomoro's POV essay. Half-day ramp accepted as worth the signal.
3. ~~**Dashboard form**~~: **RESOLVED 2026-04-26.** **Next.js on Vercel**, kept deliberately lean for the prototype (engineering-focused, not marketing-polished). User explicit: this is to demonstrate capability, not to dazzle; polish layer comes later. Public URL ships in the proposal so the Tomoro reader can click into a live dashboard.
4. ~~**Bank archetype framing**~~: **RESOLVED 2026-04-26.** **NorthStar Bank (synthetic), explicitly modelled on a Tier 1 UK retail bank.** Proposal narrative names NorthStar; prototype data is 100% synthetic. Avoids any IP / insider-knowledge claim while preserving specificity.
5. ~~**Real reference anchor**~~: **RESOLVED 2026-04-26.** **Include public-domain references at cohort level, not individual-bank level.** Cite FCA Operational Resilience published reviews + the public 2024-2025 UK bank IT-incident cohort generically. No naming-and-shaming of any specific institution. Anchors cost claims with real evidence.
6. ~~**Repo visibility**~~: **RESOLVED 2026-04-26.** **Private GitHub until the proposal is sent**, then flip to public. Allows messy iteration without audience; public on send so Tomoro can browse the code.
7. ~~**Outreach plan**~~: **RESOLVED 2026-04-26.** **Two-track**: (a) formal application via Tomoro's careers portal for AI Delivery Lead, (b) same-day direct LinkedIn outreach to 3-5 named humans (one co-founder, one Head of Delivery / VP Engineering, one or two current AI Delivery Leads). Names to be researched at the start of the next session. Cover-note template drafted at build time. Message structure: 4 lines, what + why for them + link + 20-minute ask.

---

## 4. Out of scope (for this engagement)

These are deliberately not in the brief and should not be re-litigated unless the user reopens them.

- Pitching this to a real bank (this is an application piece for Tomoro, not a sales artefact).
- Going beyond payment ops into other ops domains (incident management generally, IT ops, etc.).
- Training a custom model. We use frontier model APIs.
- Multilingual scope.
- Any write actions in the agent's tool registry.

---

## 5. Definitions and conventions

- **NorthStar Bank**: the synthetic Tier 1 UK retail bank archetype used throughout the brief and the prototype.
- **Tier 1 UK retail bank**: shorthand for the cohort of HSBC UK, Barclays UK, NatWest, Lloyds Banking Group, Santander UK. Used as the buyer-economics reference cohort.
- **The seven-test filter**: the criteria from section 3 of the original three-option brief, used to score the three candidate use cases. Preserved in the active brief implicitly via the design choices that satisfy each test.

---

## 6. How to resume

When you re-enter this project:

1. Read this file in full. It is the orientation layer.
2. Read `ops-resilience-copilot-brief.md` next, focused on sections 4 (agent), 5 (evaluation) and 9 (prototype scope), since those will drive the next planning step.
3. Resolve the seven open decisions in section 3 above.
4. Move into planning: lay out the 2 to 3 weekend build plan, decide on order of construction (eval suite first, agent stages second, dashboard third).
5. Begin generating the synthetic dataset. The dataset is the bottleneck for everything downstream.
