# RB006 — API Versioning and Deprecation Failures

**ID:** RB006  
**Category:** API Management  
**Applies to:** VC-API-Gateway, customer integrations  
**Last reviewed:** 2026-03-01

---

## Symptoms

- Customer reports `HTTP 410 Gone` on previously working endpoints
- Requests to `/v1/` endpoints return deprecation headers or redirect loops
- SDK clients throw `ApiVersionDeprecatedException` or similar
- Increased error rates on tenants running older SDK versions
- Customers report payload shape changes breaking their parsers

---

## Triage

1. Check the request path — which API version is the customer calling?
2. Confirm the deprecation timeline for that version in the API changelog
3. Check `VC-API-Gateway` access logs for `X-API-Deprecated` response headers
4. Identify which SDK version the customer is using (check `User-Agent` header)

---

## Common Causes

| Cause | Signal |
|---|---|
| Customer on deprecated API version past sunset date | `410 Gone` + `Sunset` header in response |
| SDK client not sending `Accept-Version` header | Default routing to oldest stable version |
| Breaking schema change in minor version (our bug) | Payload fields missing or renamed |
| Customer pinned to specific version that was emergency-removed | `404` on version prefix |
| Webhook payloads on new schema, customer parser on old | Deserialization errors on customer side |

---

## Investigation Steps

1. Reproduce the failing request: `curl -H "Authorization: Bearer <token>" -H "Accept-Version: v1" <endpoint>`
2. Compare response headers — look for `Deprecation`, `Sunset`, `Link` (migration guide)
3. Check `VC-API-Gateway` logs for the tenant: `service:vc-api-gateway tenant_id:<id> path:/v1/`
4. Pull the API changelog entry for the version in question
5. Check if the customer's SDK version is in the compatibility matrix

---

## Remediation

**Customer on sunset version:**
- Provide migration guide for target version
- Offer extended deprecation window if on enterprise contract (requires TAM approval)
- Pair on SDK upgrade if customer is on managed onboarding

**Breaking change introduced by VertexCloud (our bug):**
- Raise P1 internally — breaking changes in minor versions violate SemVer contract
- Roll back the breaking change or add a compatibility shim
- Draft customer comms through CX team

**Customer SDK version mismatch:**
- Point to SDK upgrade path in docs
- Confirm their framework compatibility

---

## Escalation

- Breaking change confirmed as VertexCloud regression → Platform Engineering (P1)
- Enterprise customer on expired deprecation window → TAM + VP Customer Success
- Customer data transformation required → Solutions Engineering
