# RB009 — Certificate Rotation and TLS Failures

**ID:** RB009  
**Category:** Security / TLS  
**Applies to:** VC-API-Gateway, VC-Identity, VC-Webhooks  
**Last reviewed:** 2026-02-28

---

## Symptoms

- Customer reports sudden `SSL certificate verify failed` errors
- Webhook deliveries failing with `CERT_EXPIRED` or `HOSTNAME_MISMATCH`
- Auth flows broken immediately after scheduled maintenance window
- Customers on mutual TLS (mTLS) seeing `certificate_required` errors
- Monitoring shows spike in TLS handshake failures across tenants

---

## Triage

1. Check if timing correlates with a scheduled cert rotation or maintenance window
2. Confirm whether failures are on inbound (customer → VC) or outbound (VC → customer webhook)
3. Check expiry of relevant certs: `openssl s_client -connect api.vertexcloud.io:443 | openssl x509 -noout -dates`
4. Confirm whether the customer is pinning certificates on their client

---

## Common Causes

| Cause | Signal |
|---|---|
| Customer certificate pinning after our rotation | All requests fail immediately after our cert rotation |
| Customer webhook endpoint cert expired | Outbound webhook delivery failures; `CERT_EXPIRED` in delivery log |
| Intermediate CA not included in chain | `unable to get local issuer certificate` in customer logs |
| mTLS client cert expired (customer-provided) | `certificate_required` or `certificate_expired` on auth requests |
| New cert not yet propagated to all PoPs | Intermittent failures depending on which PoP the request hits |

---

## Investigation Steps

1. Pull TLS handshake error rate: `service:vc-api-gateway error:tls_handshake`
2. For outbound webhook cert failures — check the customer's endpoint cert:
   `openssl s_client -connect <customer_endpoint>:443 2>/dev/null | openssl x509 -noout -dates`
3. For inbound failures after our rotation — check if customer is pinning:
   ask them to confirm their TLS client config
4. Check cert propagation status across PoPs if intermittent

---

## Remediation

**Customer pinning our cert (now rotated):**
- Certificate pinning is not recommended — share our certificate transparency log and rotation schedule
- Customer must update their pinned cert to the new one
- Provide the new leaf cert fingerprint and chain

**Customer webhook endpoint cert expired:**
- Notify customer to renew their endpoint certificate
- Offer temporary bypass to HTTP for up to 48h on P1 tickets (requires TAM approval)

**Intermediate CA chain incomplete:**
- Confirm our full cert chain is being served: `openssl s_client -connect api.vertexcloud.io:443 -showcerts`
- If chain incomplete on our side → Platform Engineering to fix TLS config

**mTLS client cert expired:**
- Customer must reissue their client certificate and upload new cert to VertexCloud Identity settings
- Provide instructions for certificate upload via `/settings/security/mtls`

---

## Escalation

- TLS failure affecting multiple tenants → Platform Engineering + Security (P1)
- Certificate chain misconfiguration on VertexCloud side → Platform Engineering (P0 if customer-facing)
