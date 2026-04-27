# RB007 — SDK Client and Integration Errors

**ID:** RB007  
**Category:** SDK / Client Integration  
**Applies to:** VC-SDK (all languages), VC-API-Gateway  
**Last reviewed:** 2026-02-15

---

## Symptoms

- Customer reports `NullPointerException` or `AttributeError` on SDK method calls
- SDK returns unexpected `None` / `null` where an object is expected
- Authentication works but API calls fail immediately after
- Customer reports SDK methods that "disappeared" after upgrading
- Intermittent `ConnectionResetError` or `SSL: WRONG_VERSION_NUMBER`

---

## Triage

1. Confirm SDK language and version from the bug report
2. Ask for a minimal reproduction — SDK version, method called, full stack trace
3. Check if the issue appeared after a specific SDK upgrade
4. Check `VC-API-Gateway` for corresponding inbound requests (are they arriving?)

---

## Common Causes

| Cause | Signal |
|---|---|
| Customer on SDK version with known bug | SDK version matches a bug in release notes |
| Method signature changed in new SDK version | `TypeError` on known method call |
| SDK initialised before environment variables set | `NoneType` on client object attributes |
| TLS version mismatch between SDK and gateway | `SSL: WRONG_VERSION_NUMBER` |
| Customer dependency conflict with SDK's own dependencies | `ImportError` or version conflict in logs |
| SDK caching stale auth tokens | 401s after credential rotation |

---

## Investigation Steps

1. Ask for SDK version: `pip show vertexcloud-sdk` / `npm list @vertexcloud/sdk`
2. Check SDK changelog between customer's version and latest stable
3. Check if the bug is in the known-issues registry (`lookup_issue_code(SDK-*)`)
4. Ask customer to set `VC_SDK_DEBUG=1` and share debug logs
5. Check `VC-API-Gateway` for inbound requests — if none arrive, issue is client-side

---

## Remediation

**Known SDK bug:**
- Direct to patched version
- Provide workaround if upgrade is not immediately possible
- Log affected tenant in bug tracking

**Environment initialisation issue:**
- Review customer's SDK bootstrap order
- Confirm env vars are set before client instantiation

**TLS version mismatch:**
- Confirm minimum TLS version for customer's runtime
- VertexCloud gateway requires TLS 1.2+; TLS 1.0/1.1 connections are rejected

**Stale auth token cache:**
- Call `client.auth.refresh()` explicitly or set `auto_refresh=True` on client init

---

## Escalation

- Bug confirmed in current SDK version → SDK team (fix + patch release)
- Customer on LTS SDK version with incompatible change → SDK team + TAM
