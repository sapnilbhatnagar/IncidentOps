# VertexCloud Synthetic Corpus

This directory contains the synthetic knowledge corpus and ticket dataset used by the IncidentOps prototype. All data is fictional. No real customer data, no real SaaS company's internal documents, no PII.

## Conventions

**VertexCloud** is the synthetic enterprise multi-product SaaS archetype, modelled on Salesforce / ServiceNow / Qinecsa Solutions tier players. It runs CRM Cloud, Service Cloud, Analytics Cloud, and Integration Cloud on a multi-tenant platform serving 5,000+ enterprise customers globally.

Where the corpus references real external entities (SOC 2, ISO 27001, GDPR, OAuth 2.0, SAML 2.0), those references are accurate to public information. Where the corpus references internal VertexCloud systems, those are invented but plausible.

**Product-surface scope**: Integration and API support only for the prototype. Issue codes follow common SaaS taxonomies (HTTP status families, OAuth, webhook signatures, multi-tenant ACLs).

**Severity bands**:

- **P1**: cross-tenant impact, breach of an enterprise SLA, or data-integrity risk. VP Customer Support and Head of Platform Reliability notified.
- **P2**: contained tenant impact, or risk of escalation if unresolved within hours.
- **P3**: single-tenant or single-user issue; no SLA exposure.

**Internal VertexCloud systems referenced**:

- `VC-API-Gateway`: edge API layer where all external API calls land (synthetic).
- `VC-Identity`: auth, SSO, SAML, OAuth, MFA service (synthetic).
- `VC-DataPlatform`: shared multi-tenant data store (synthetic).
- `VC-Webhooks`: webhook delivery service (synthetic).
- `VC-Sync`: data sync between products and to customer warehouses (synthetic).
- `VC-Observability`: logs, metrics, traces platform (synthetic; analogue of Datadog).
- `VC-Support`: ticketing system (synthetic; analogue of Zendesk).
- `OAuth 2.0`, `SAML 2.0`, `Okta`, `Azure AD`, `Google Workspace`: real, referenced for IdP context.

## Corpus state: SEED

This corpus is currently at **seed scale**, not full scale. It is sized for prototype credibility, not for the full eval suite.

| Artefact | Seed count | Full target | Status |
|---|---|---|---|
| Runbooks | 5 | 50 | Seed shipped. Templates established. |
| Tickets | 10 | 200 | Seed shipped. JSONL schema established. |
| Incident reports | 2 | 20 | Seed shipped. Structure established. |
| SaaS issue codes | 30 | ~30 | Complete. |
| Telemetry records | 30 | ~500 | Seed shipped. Schema established. |
| Gold eval set | 0 | 200 | Not started. Built after seed corpus is reviewed. |

## How the seed scales to full

Once the seed is reviewed and the patterns are validated, full-scale generation runs in three batches:

1. **Issue-code sweep**: for each of the 30 issue codes, generate 1 to 2 runbooks covering the common operational scenarios that surface that code. Output: 30 to 60 runbooks. Quality-controlled by a senior-engineer-style review prompt + manual spot-check.
2. **Ticket sampling**: generate tickets stratified by severity (10% P1, 30% P2, 60% P3) and by issue category (drawn from the runbook taxonomy). 200 tickets total. Each ticket cites the runbook that resolves it (this is the gold label).
3. **Incident report sweep**: 20 systemic events covering customer-impacting outages, data-integrity events, and near-miss scenarios. Each incident cites the contributing tickets.

The generation is itself prompt-engineered against templates derived from the seed corpus. The prompts and rubrics live in `/data/generation/` (not yet created).

## File formats

- **Runbooks**: Markdown with YAML frontmatter. One runbook per file. Filenames `RB###-slug.md`.
- **Tickets**: JSON Lines. One ticket per line. All in `tickets/tickets.jsonl`.
- **Incident reports**: Markdown with YAML frontmatter. One report per file. Filenames `INC###-slug.md`.
- **Reference**: JSON. One file per reference type.
- **Telemetry**: JSON Lines. One record per line. Separate files per source (logs, request records).

## Provenance and licensing

All synthetic. No copying from any SaaS vendor's real documentation. Issue code definitions follow common public conventions (HTTP, OAuth, SAML). Created 2026-04-26 for the IncidentOps prototype.
