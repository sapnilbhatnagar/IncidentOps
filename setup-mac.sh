#!/usr/bin/env bash
# setup-mac.sh — one-shot Mac onboarding for IncidentOps.
# Restores the project memory so Claude Code picks up Windows context automatically.
# Idempotent: safe to re-run.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENDORED_MEMORY="${REPO_ROOT}/incidentops/_planning/memory/project_tomoro_work_product.md"

echo "==> IncidentOps Mac setup"
echo "    Repo: ${REPO_ROOT}"

# 1. Sanity checks ------------------------------------------------------------
if [[ ! -f "${VENDORED_MEMORY}" ]]; then
  echo "!! Vendored memory file not found at:"
  echo "   ${VENDORED_MEMORY}"
  echo "   Are you running this from the repo root?"
  exit 1
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "!! Claude Code CLI ('claude') is not on PATH."
  echo "   Install from https://claude.ai/code, then re-run this script."
  exit 1
fi

# 2. Resolve Claude Code's encoded project directory --------------------------
# Claude Code derives the project folder name from the working directory.
# It encodes the path by replacing path separators and ':' with '-', dropping the leading '/'.
# Example: /Users/sapnil/projects/incidentops -> -Users-sapnil-projects-incidentops
ENCODED_CWD="$(echo "${REPO_ROOT}" | sed 's|/|-|g')"
PROJECTS_DIR="${HOME}/.claude/projects/${ENCODED_CWD}"
MEMORY_DIR="${PROJECTS_DIR}/memory"

mkdir -p "${MEMORY_DIR}"
echo "==> Memory dir: ${MEMORY_DIR}"

# 3. Copy the project memory file --------------------------------------------
cp "${VENDORED_MEMORY}" "${MEMORY_DIR}/project_tomoro_work_product.md"
echo "==> Copied project_tomoro_work_product.md"

# 4. Ensure MEMORY.md index has the entry ------------------------------------
INDEX_FILE="${MEMORY_DIR}/MEMORY.md"
INDEX_LINE='- [project_tomoro_work_product.md](project_tomoro_work_product.md) — Active: IncidentOps build for Tomoro.ai application'

if [[ ! -f "${INDEX_FILE}" ]]; then
  cat > "${INDEX_FILE}" <<EOF
# Memory Index

${INDEX_LINE}
EOF
  echo "==> Created MEMORY.md index"
elif ! grep -q "project_tomoro_work_product.md" "${INDEX_FILE}"; then
  printf '\n%s\n' "${INDEX_LINE}" >> "${INDEX_FILE}"
  echo "==> Appended to existing MEMORY.md"
else
  echo "==> MEMORY.md already references project_tomoro_work_product.md (no change)"
fi

# 5. Done ---------------------------------------------------------------------
cat <<'EOF'

==> Done.

Next:
  cd "$(pwd)"
  claude

Then say:
  Resume IncidentOps. Read session-log.md and incidentops/_planning/build-plan.md. Continue Phase 1.
EOF
