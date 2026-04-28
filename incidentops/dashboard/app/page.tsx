import Link from "next/link";
import { getGoldIncidents, getTickets } from "../lib/data";

const SEVERITY_COLOR: Record<string, string> = {
  P1: "#ef4444",
  P2: "#f97316",
  P3: "#eab308",
  P4: "#6b7280",
};

const DIFFICULTY_COLOR: Record<string, string> = {
  easy: "#22c55e",
  medium: "#f97316",
  hard: "#ef4444",
};

export default function TicketQueue() {
  const gold = getGoldIncidents();
  const tickets = getTickets();
  const ticketMap = Object.fromEntries(tickets.map((t) => [t.ticket_id, t]));

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: "2rem 1rem" }}>
      <header style={{ marginBottom: "2rem" }}>
        <p style={{ fontSize: "0.7rem", letterSpacing: "0.15em", textTransform: "uppercase", color: "#555", margin: "0 0 0.5rem" }}>
          IncidentOps
        </p>
        <div style={{ display: "flex", alignItems: "baseline", gap: "1.5rem" }}>
          <h1 style={{ fontSize: "1.5rem", fontWeight: 600, margin: 0 }}>Ticket Queue</h1>
          <nav style={{ display: "flex", gap: "1rem" }}>
            <Link href="/evals" style={{ fontSize: "0.8rem", color: "#555", textDecoration: "none" }}>
              Eval Scoreboard →
            </Link>
          </nav>
        </div>
        <p style={{ color: "#555", margin: "0.5rem 0 0", fontSize: "0.875rem" }}>
          {gold.length} gold-labelled incidents · stub agent (INCIDENTOPS_LIVE=1 for real pipeline)
        </p>
      </header>

      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.875rem" }}>
        <thead>
          <tr style={{ borderBottom: "1px solid #222" }}>
            {["Ticket", "Title", "Severity", "Category", "Runbook", "Difficulty"].map((h) => (
              <th key={h} style={{ textAlign: "left", padding: "0.5rem 0.75rem", color: "#555", fontWeight: 500, fontSize: "0.75rem" }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {gold.map((g) => {
            const t = ticketMap[g.ticket_id];
            return (
              <tr key={g.ticket_id} style={{ borderBottom: "1px solid #111" }}>
                <td style={{ padding: "0.6rem 0.75rem" }}>
                  <Link href={`/tickets/${g.ticket_id}`} style={{ color: "#60a5fa", textDecoration: "none", fontFamily: "monospace", fontSize: "0.8rem" }}>
                    {g.ticket_id}
                  </Link>
                </td>
                <td style={{ padding: "0.6rem 0.75rem", color: "#ccc", maxWidth: 260, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                  {t?.title ?? "—"}
                </td>
                <td style={{ padding: "0.6rem 0.75rem" }}>
                  <span style={{ color: SEVERITY_COLOR[t?.severity ?? ""] ?? "#888", fontFamily: "monospace", fontSize: "0.75rem" }}>
                    {t?.severity ?? "—"}
                  </span>
                </td>
                <td style={{ padding: "0.6rem 0.75rem", color: "#888", fontSize: "0.8rem" }}>{t?.category ?? "—"}</td>
                <td style={{ padding: "0.6rem 0.75rem", fontFamily: "monospace", fontSize: "0.75rem", color: "#888" }}>{g.gold_runbook}</td>
                <td style={{ padding: "0.6rem 0.75rem" }}>
                  <span style={{ color: DIFFICULTY_COLOR[g.difficulty] ?? "#888", fontSize: "0.75rem" }}>{g.difficulty}</span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </main>
  );
}
