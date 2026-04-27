export default function Home() {
  return (
    <main style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "100vh", gap: "1rem" }}>
      <div style={{ fontSize: "0.75rem", letterSpacing: "0.15em", textTransform: "uppercase", color: "#888" }}>
        IncidentOps
      </div>
      <h1 style={{ fontSize: "2rem", fontWeight: 600, margin: 0 }}>
        Dashboard incoming
      </h1>
      <p style={{ color: "#888", margin: 0, maxWidth: 400, textAlign: "center" }}>
        AI-grounded incident diagnosis for enterprise SaaS support ops.
        Pipeline in build — check back soon.
      </p>
      <div style={{ display: "flex", gap: "0.5rem", marginTop: "1rem" }}>
        {["Triage", "Retrieval", "Diagnosis", "Tools", "Remediation", "Handoff"].map((stage) => (
          <span key={stage} style={{ fontSize: "0.7rem", padding: "0.25rem 0.6rem", border: "1px solid #333", borderRadius: 4, color: "#666" }}>
            {stage}
          </span>
        ))}
      </div>
    </main>
  );
}
