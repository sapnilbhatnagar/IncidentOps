# IncidentOps — Project Conventions

## Writing style for documentation and READMEs

**Documentation describes the system as it is.** Not how it was built, not how to extend it, not what's coming next. A reader landing on a README should learn what the thing does and how to read its output. Nothing else.

**Cut these patterns from any doc unless explicitly asked:**
- "What a stub agent looks like" / explanations of temporary scaffolding
- "How to add a new X" tutorials — that's a contributor guide, not a feature doc
- Meta-commentary on development process, phases, or what's coming
- Apologies, hedges, or "this is a placeholder for…" prose
- AI-style filler: "we run a stub", "this proves", "expected results", framing-of-framing

**Prefer:**
- Tables over prose for any list of checks, fields, or pass bars
- Direct statements: "X is checked" not "we check X"
- One-line section intros, then the table or code
- Concrete examples of actual output, not hypothetical flow

If a section can be deleted without the reader losing information about the system, delete it.

## Code style

- Pydantic for all schema. No dict-shaped contracts between modules.
- Deterministic graders return `(passed: bool, score: float, detail: str)`.
- No comments explaining what the code does — names should carry that. Comments only for non-obvious WHY.
- Module docstrings are one line. No "this module provides…" boilerplate.

## Feature IDs

Every module references its feature ID in the commit and the build-plan checkbox. Do not invent new prefixes — use the existing scheme: INFRA, CORPUS, EVAL, AGENT, TOOL, DASH, CI.

## Memory

The Claude memory system at `~/.claude/projects/.../memory/` is the source of truth across sessions. Update it when phase status, architecture, or stack decisions change. Do not duplicate that content in repo files.
