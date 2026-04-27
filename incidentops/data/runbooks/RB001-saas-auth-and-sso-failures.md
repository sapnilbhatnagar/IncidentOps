---
id: RB001
title: Auth and SSO Failures (401, 403, OAuth, SAML, MFA)
last_updated: 2026-02-14
owner: identity-platform
severity_levels: [P3, P2, P1]
related_runbooks: [RB005]
related_codes: [AUTH-401-EXPIRED, AUTH-401-INVALID, AUTH-403-PERMISSION, AUTH-OAUTH-DRIFT, AUTH-SSO-CONFIG, AUTH-MFA-FAIL]
---

## When to use

Use this runbook when one or more of the following is observed:

- Customer reports inability to sign in or call APIs.
- VC-Identity emits AUTH-* events at elevated rate for a tenant.
- VC-API-Gateway returns 401 or 403 to a tenant for more than 1% of requests over a 5-minute window.

## Symptoms

- Customer support ticket: "users cannot sign in", "API returns 401", "SSO redirect loop".
- VC-Observability alert: `AUTH-FAIL-RATE` for tenant.
- VC-Identity alert: `SAML-METADATA-DRIFT` or `OAUTH-CLIENT-DRIFT`.

## Severity

- **P1**: tenant-wide sign-in failure on enterprise customer.
- **P2**: subset of users affected, or single integration broken.
- **P3**: individual user, expected MFA challenge, expired token in customer client.

## Initial triage (5 minutes)

1. Identify scope: one user, one role, one integration, or whole tenant?
2. Pull last 50 AUTH-* events for the tenant from VC-Observability.
3. Check VC-Identity status board for any platform-side incident on auth flow.
4. Confirm whether the customer recently changed IdP configuration, rotated certificates, or upgraded their client SDK.

## Investigation by code

### AUTH-401-EXPIRED

Bearer token past expiry. Expected behaviour. Customer's client should refresh.

- Confirm client is calling `/oauth/token` refresh endpoint.
- If refresh also fails, escalate to AUTH-OAUTH-DRIFT path.

### AUTH-401-INVALID

Token cannot be validated.

- Check whether VC-Identity rotated signing keys in last 24h. If yes, customer client may have stale JWKS cache.
- Verify customer is hitting the published JWKS endpoint and respecting cache headers.

### AUTH-403-PERMISSION

Authenticated, but lacks scope.

- Diff requested resource scope against principal's role.
- Most common cause: customer admin removed a scope from the OAuth client without informing the integration owner.

### AUTH-OAUTH-DRIFT

OAuth client config no longer matches what's registered.

- Pull registered client config from VC-Identity admin API.
- Diff against the customer's deployed client config.
- Common drift: redirect URI added in dev, not pushed to prod registration.

### AUTH-SSO-CONFIG

SAML metadata or attribute mismatch.

- Re-import the customer's IdP metadata.
- Verify NameID format matches what VC-Identity expects (typically email).
- Check attribute claims for `groups`, `email`, `displayName`.

### AUTH-MFA-FAIL

MFA challenge or response broken.

- Confirm customer's MFA enforcement policy (per-user, per-role, per-tenant).
- Check whether customer recently changed MFA provider (Okta to Azure AD, etc.).

## Common causes (ranked by frequency)

1. Customer-side IdP certificate rotation without VertexCloud-side metadata refresh.
2. Customer admin removed an OAuth scope.
3. Customer's client SDK out of date and caching stale JWKS.
4. VertexCloud-side signing key rotation, customer client not handling rotation gracefully.
5. Customer's MFA provider migration mid-quarter.

## Remediation

- For customer-side configuration drift: provide diff and remediation steps to customer admin.
- For VertexCloud-side issue (signing key rotation, gateway misconfig): engage Identity Platform on-call.
- Never reset a customer's MFA, never bypass auth, never share token contents with the customer.

## Escalation

- P1 (tenant-wide sign-in failure): page Identity Platform on-call, open incident bridge, prepare status page update.
- P2: assign to Identity Platform queue, target 4h response.
- P3: standard support response.

## Post-resolution checklist

- Customer confirms sign-in working.
- Root cause documented in ticket.
- If pattern repeats across tenants in 30 days, escalate to engineering for product fix.
