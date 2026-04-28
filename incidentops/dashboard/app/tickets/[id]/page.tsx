import Link from "next/link";
import { getGoldIncident, getTicket } from "../../../lib/data";

type Props = { params: { id: string } };

export default function TicketWorkspace({ params }: Props) {
  const ticketId = decodeURIComponent(params.id);
  const gold = getGoldIncident(ticketId);
  const ticket = getTicket(ticketId);

  if (!gold || !ticket) {
    return (
      <main style={{ padding: "2rem", color: "#888" }}>
        <Link href="/" style={{ color: "#555", textDecoration: "none", fontSize: "0.875rem" }}>← Queue</Link>
        <p style={{ marginTop: "2rem" }}>Ticket {ticketId} not found.</p>
      </main>
    );
  }

  return (
    <main style={{ maxWidth: 1100, margin: "0 auto", padding: "2rem 1rem" }}>
      <nav style={{ marginBottom: "1.5rem" }}>
        <Link href="/" style={{ color: "#555", textDecoration: "none", fontSize: "0.875rem" }}>← Queue</Link>
        <span style={{ color: "#333", margin: "0 0.5rem" }}>/</span>
        <span style={{ color: "#888", fontFamily: "monospace", fontSize: "0.8rem" }}>{ticketId}</span>
      </nav>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.5rem" }}>

        {/* Left column: ticket + diagnosis */}
        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          <Panel title="Ticket">
            <Field label="ID" value={ticket.ticket_id} mono />
            <Field label="Tenant" value={ticket.tenant_id} mono />
            <Field label="Severity" value={ticket.severity} />
            <Field label="Category" value={ticket.category} />
            <Field label="Title" value={ticket.title} />
            <Field label="Description" value={ticket.description} />
            {ticket.resolution_notes && <Field label="Resolution notes" value={ticket.resolution_notes} />}
          </Panel>

          <Panel title="Diagnosis">
            <div style={{ color: "#555", fontSize: "0.8rem", padding: "0.5rem 0" }}>
              Pipeline runs offline — start with{" "}
              <code style={{ background: "#111", padding: "0.1rem 0.3rem", borderRadius: 3, fontSize: "0.75rem" }}>
                INCIDENTOPS_LIVE=1 make evals
              </code>
            </div>
            <div style={{ marginTop: "0.75rem" }}>
              <div style={{ fontSize: "0.7rem", color: "#555", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "0.25rem" }}>Gold root cause</div>
              <div style={{ color: "#ccc", fontSize: "0.875rem", lineHeight: 1.5 }}>{gold.gold_root_cause}</div>
            </div>
            <div style={{ marginTop: "0.75rem" }}>
              <div style={{ fontSize: "0.7rem", color: "#555", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "0.25rem" }}>Gold remediation</div>
              <div style={{ color: "#ccc", fontSize: "0.875rem", lineHeight: 1.5 }}>{gold.gold_remediation}</div>
            </div>
          </Panel>
        </div>

        {/* Right column: evidence + provenance */}
        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          <Panel title="Evidence">
            <div style={{ display: "flex", gap: "1rem", alignItems: "baseline" }}>
              <span style={{ fontSize: "0.7rem", color: "#555", textTransform: "uppercase", letterSpacing: "0.1em" }}>Gold runbook</span>
              <span style={{ fontFamily: "monospace", fontSize: "0.875rem", color: "#60a5fa" }}>{gold.gold_runbook}</span>
            </div>
            <div style={{ display: "flex", gap: "1rem", alignItems: "baseline", marginTop: "0.5rem" }}>
              <span style={{ fontSize: "0.7rem", color: "#555", textTransform: "uppercase", letterSpacing: "0.1em" }}>Difficulty</span>
              <span style={{ fontSize: "0.875rem", color: "#ccc" }}>{gold.difficulty}</span>
            </div>
            <div style={{ marginTop: "1rem", padding: "0.75rem", background: "#0f0f0f", borderRadius: 6, border: "1px solid #1a1a1a" }}>
              <div style={{ fontSize: "0.7rem", color: "#444", marginBottom: "0.5rem" }}>
                Evidence spans populated when pipeline runs with INCIDENTOPS_LIVE=1
              </div>
              <div style={{ fontSize: "0.75rem", color: "#333" }}>
                Hybrid retrieval: dense (all-MiniLM-L6-v2) + BM25 → RRF → cross-encoder rerank
              </div>
            </div>
          </Panel>

          <Panel title="Pipeline stages">
            {[
              { stage: "Triage", desc: "Route ticket to retrieval query" },
              { stage: "Retrieval", desc: "LanceDB + BM25 → RRF fusion" },
              { stage: "Diagnosis", desc: "Opus 4.7 · forced tool_use" },
              { stage: "Tools", desc: "get_runbook · search_tickets · get_telemetry" },
              { stage: "Remediation", desc: "Opus 4.7 · steps + rollback note" },
              { stage: "Handoff", desc: "HandoffPacket · mode: shadow / assist / guided" },
            ].map(({ stage, desc }, i) => (
              <div key={stage} style={{ display: "flex", gap: "0.75rem", alignItems: "flex-start", padding: "0.4rem 0", borderBottom: i < 5 ? "1px solid #111" : "none" }}>
                <span style={{ fontFamily: "monospace", fontSize: "0.7rem", color: "#444", width: 24, textAlign: "right", paddingTop: 2 }}>{i + 1}</span>
                <div>
                  <span style={{ fontSize: "0.8rem", color: "#888" }}>{stage}</span>
                  <span style={{ fontSize: "0.75rem", color: "#444", marginLeft: "0.5rem" }}>{desc}</span>
                </div>
              </div>
            ))}
          </Panel>
        </div>
      </div>
    </main>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div style={{ border: "1px solid #1a1a1a", borderRadius: 8, padding: "1rem" }}>
      <div style={{ fontSize: "0.7rem", textTransform: "uppercase", letterSpacing: "0.12em", color: "#444", marginBottom: "0.75rem" }}>
        {title}
      </div>
      {children}
    </div>
  );
}

function Field({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div style={{ marginBottom: "0.5rem" }}>
      <div style={{ fontSize: "0.7rem", color: "#444", marginBottom: "0.15rem" }}>{label}</div>
      <div style={{ fontSize: mono ? "0.8rem" : "0.875rem", fontFamily: mono ? "monospace" : undefined, color: "#ccc", lineHeight: 1.5 }}>
        {value}
      </div>
    </div>
  );
}
