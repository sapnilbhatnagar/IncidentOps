# INC005 — Certificate Rotation: Mass Customer Outage from Certificate Pinning

**Incident ID:** INC005  
**Date:** 2026-03-18  
**Severity:** P1  
**Duration:** 4 hours (08:55–13:00, staggered by customer)  
**Status:** Resolved. PIR complete.

---

## Summary

VertexCloud's scheduled leaf certificate rotation at 08:50 caused immediate authentication failures for 12 enterprise customers who had implemented certificate pinning. Customers were not identified as certificate-pinners prior to the rotation because no registry of pinning customers existed.

---

## Timeline

| Time | Event |
|---|---|
| 08:50 | Scheduled leaf certificate rotation completed on all VertexCloud endpoints |
| 08:55 | First customer escalation: SSL certificate verify failed |
| 09:05 | 12 customer escalations received in 10 minutes. P1 declared |
| 09:10 | Root cause identified: certificate pinning |
| 09:15 | SRE begins contacting each affected customer with new cert fingerprint |
| 09:30 | First 3 customers update pinned cert and recover |
| 11:00 | 8 of 12 customers recovered |
| 12:00 | 11 of 12 customers recovered |
| 13:00 | Final customer recovered (internal approval process delayed their update) |

---

## Five Whys

1. **Why did 12 customers lose access?** Their clients rejected the new certificate because they had pinned the old leaf certificate.
2. **Why did certificate pinning cause a mass outage?** Certificate pinning ties a client to a specific certificate — rotation always breaks pinned clients.
3. **Why were there 12 customers pinning?** No policy against certificate pinning existed; some customers did it for "extra security."
4. **Why were pinning customers not contacted before rotation?** No registry of certificate-pinning customers existed.
5. **Why did no registry exist?** Certificate pinning is a client-side configuration — VertexCloud has no visibility into it unless customers self-declare.

---

## Impact

- 12 enterprise customers: complete API access loss, staggered duration of 2-4 hours
- Estimated SLA credit exposure: £42,000
- Reputational impact: 4 customers expressed intent to review contract

---

## Actions

| Action | Owner | Due |
|---|---|---|
| Add certificate pinning to onboarding forbidden-practice list | CS Ops | 2026-03-25 ✓ |
| Add certificate-pinning self-declaration to enterprise onboarding form | CS Ops | 2026-03-28 ✓ |
| Add pre-rotation outreach checklist for all cert rotation events | Platform Engineering | 2026-04-01 ✓ |
| Document CA pinning as the supported alternative | Platform Engineering | 2026-03-25 ✓ |
| Pre-announce certificate rotations 30 days in advance via status page | Platform Engineering | 2026-04-05 |
