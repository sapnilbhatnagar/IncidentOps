import fs from "fs";
import path from "path";

const DATA = path.join(process.cwd(), "data");

export type GoldIncident = {
  ticket_id: string;
  gold_runbook: string;
  gold_root_cause: string;
  gold_remediation: string;
  difficulty: "easy" | "medium" | "hard";
};

export type Ticket = {
  ticket_id: string;
  tenant_id: string;
  title: string;
  description: string;
  category: string;
  severity: string;
  status: string;
  resolution_notes?: string;
};

export type EvalCheck = {
  check: string;
  score: number;
  n_pass?: number;
  n_total?: number;
  detail?: string;
  passed: boolean;
  hard_gate: boolean;
};

export type EvalResults = {
  gate: "pass" | "fail";
  hard_failures: string[];
  advisory_failures: string[];
  checks: EvalCheck[];
};

export function getGoldIncidents(): GoldIncident[] {
  const dir = path.join(DATA, "gold");
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".json"))
    .sort()
    .map((f) => JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8")));
}

export function getGoldIncident(ticketId: string): GoldIncident | null {
  const file = path.join(DATA, "gold", `${ticketId}.json`);
  if (!fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, "utf-8"));
}

export function getTickets(): Ticket[] {
  const file = path.join(DATA, "tickets.json");
  if (!fs.existsSync(file)) return [];
  return JSON.parse(fs.readFileSync(file, "utf-8"));
}

export function getTicket(ticketId: string): Ticket | null {
  return getTickets().find((t) => t.ticket_id === ticketId) ?? null;
}

export function getEvalResults(): EvalResults | null {
  const file = path.join(DATA, "eval-results.json");
  if (!fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, "utf-8"));
}
