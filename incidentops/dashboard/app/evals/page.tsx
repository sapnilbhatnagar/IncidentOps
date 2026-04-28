import Link from "next/link";
import { getEvalResults, type EvalCheck } from "../../lib/data";

function StatusBadge({ check }: { check: EvalCheck }) {
  if (check.passed) return <span style={{ color: "#22c55e", fontSize: "0.75rem" }}>PASS</span>;
  if (check.hard_gate) return <span style={{ color: "#ef4444", fontSize: "0.75rem" }}>FAIL</span>;
  return <span style={{ color: "#f97316", fontSize: "0.75rem" }}>ADVISORY</span>;
}

function scoreStr(check: EvalCheck): string {
  if (check.n_pass !== undefined && check.n_total !== undefined) {
    return `${check.n_pass}/${check.n_total}`;
  }
  return check.score.toFixed(3);
}

export default function EvalScoreboard() {
  const results = getEvalResults();

  if (!results) {
    return (
      <main style={{ padding: "2rem", color: "#888" }}>
        <Link href="/" style={{ color: "#555", textDecoration: "none", fontSize: "0.875rem" }}>← Queue</Link>
        <p style={{ marginTop: "2rem" }}>No eval-results.json found. Run <code>make evals</code> first.</p>
      </main>
    );
  }

  const gateIcon = results.gate === "pass" ? "✓" : "✗";
  const gateColor = results.gate === "pass" ? "#22c55e" : "#ef4444";

  const byCategory: Record<string, EvalCheck[]> = {};
  for (const check of results.checks) {
    const [cat] = check.check.split("/");
    (byCategory[cat] ??= []).push(check);
  }

  return (
    <main style={{ maxWidth: 780, margin: "0 auto", padding: "2rem 1rem" }}>
      <nav style={{ marginBottom: "1.5rem" }}>
        <Link href="/" style={{ color: "#555", textDecoration: "none", fontSize: "0.875rem" }}>← Queue</Link>
      </nav>

      <header style={{ marginBottom: "2rem" }}>
        <h1 style={{ fontSize: "1.5rem", fontWeight: 600, margin: 0 }}>Eval Scoreboard</h1>
        <div style={{ marginTop: "0.5rem", display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <span style={{ fontSize: "1rem", color: gateColor, fontFamily: "monospace" }}>{gateIcon}</span>
          <span style={{ fontSize: "0.875rem", color: gateColor }}>
            GATE {results.gate.toUpperCase()}
          </span>
          {results.advisory_failures.length > 0 && (
            <span style={{ fontSize: "0.8rem", color: "#555" }}>
              · {results.advisory_failures.length} advisory below target
            </span>
          )}
        </div>
      </header>

      {Object.entries(byCategory).map(([category, checks]) => (
        <section key={category} style={{ marginBottom: "2rem" }}>
          <h2 style={{ fontSize: "0.7rem", textTransform: "uppercase", letterSpacing: "0.15em", color: "#555", margin: "0 0 0.75rem", fontWeight: 500 }}>
            {category}
          </h2>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.875rem" }}>
            <tbody>
              {checks.map((check) => (
                <tr key={check.check} style={{ borderBottom: "1px solid #111" }}>
                  <td style={{ padding: "0.5rem 0.75rem 0.5rem 0", fontFamily: "monospace", fontSize: "0.78rem", color: "#888" }}>
                    {check.check.split("/")[1]}
                  </td>
                  <td style={{ padding: "0.5rem 0.5rem", color: "#aaa", textAlign: "right", fontFamily: "monospace", fontSize: "0.8rem" }}>
                    {scoreStr(check)}
                  </td>
                  <td style={{ padding: "0.5rem 0 0.5rem 0.75rem", textAlign: "right", width: 80 }}>
                    <StatusBadge check={check} />
                  </td>
                  <td style={{ padding: "0.5rem 0 0.5rem 0.75rem", color: "#444", fontSize: "0.75rem" }}>
                    {check.hard_gate ? "hard gate" : "advisory"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      ))}

      <footer style={{ fontSize: "0.75rem", color: "#333", marginTop: "2rem" }}>
        Honest + Harmless hard gates block merge · Helpful is advisory
      </footer>
    </main>
  );
}
