# IncidentOps

Grounded, action-aware AI agent for enterprise SaaS support and platform operations. 

> **Status (2026-04-27).** Phase 0 complete. Phase 1 (repo scaffold + corpus expansion) is next. See `session-log.md` for the latest decision log.

---

## Start here on Mac

Three commands. Nothing else.

```bash
git clone https://github.com/sapnilbhatnagar/incidentops.git ~/projects/incidentops
cd ~/projects/incidentops
./setup-mac.sh
```

Then start Claude Code:

```bash
claude
```

…and say:

> Resume IncidentOps. Read `session-log.md` and `incidentops/_planning/build-plan.md`. Continue Phase 1.

That's it. `setup-mac.sh` restores the project memory so Claude picks up where Windows left off; if you skip it, just paste the prompt above and Claude will read the in-repo plan and session log itself.

---

## What's in the repo

```
.
├── incidentops-brief.md          # the spec — read sections 4, 5, 7 first
├── session-log.md                # decision audit trail — read the latest Session entry first
├── incidentops/
│   ├── data/                     # synthetic corpus (runbooks, tickets, incidents, telemetry, gold-set spec)
│   └── _planning/
│       ├── build-plan.md         # 8-phase build plan, current state marked
│       └── memory/               # vendored project memory for Claude Code auto-memory
├── setup-mac.sh                  # one-shot memory restore for Mac
└── .gitignore
```

Everything Claude needs to continue the build is in this repo. The memory file in `_planning/memory/` is a convenience for auto-memory; the truth is the brief + session log + build plan.

---

## Build plan at a glance

| Phase | Goal | Status |
|---|---|---|
| 0 | Rename to IncidentOps, git init, contradiction cleanup | ✓ Complete |
| 1 | Repo scaffold (Python + Next.js) + corpus expansion to floor | Next |
| 2 | HHH eval harness (Inspect AI + custom graders) | |
| 3 | Hybrid retrieval pipeline (LanceDB + rerank) | |
| 4 | Diagnosis stage | |
| 5 | Read-only tool layer | |
| 6 | Remediation draft + handoff | |
| 7 | CI integration (GitHub Actions, gated on Honest + Harmless) | |
| 8 | Dashboard (Next.js on Vercel) | |

Application packaging (proposal, Loom, outreach) is **out of scope** for this repo. Focus is the working product.

---

## License

Private repo. Synthetic corpus only — no real customer data, no real SaaS vendor's internal documents.
