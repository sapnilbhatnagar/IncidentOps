UV := uv
PYTHON := $(UV) run python
PNPM := pnpm
DASH_DIR := incidentops/dashboard

.PHONY: install corpus evals agent dash lint test clean

install:
	$(UV) sync --extra dev
	cd $(DASH_DIR) && $(PNPM) install

corpus:
	$(PYTHON) incidentops/data/validate_corpus.py

evals:
	$(UV) run inspect eval incidentops/evals/helpful/task.py incidentops/evals/honest/task.py incidentops/evals/harmless/task.py --log-dir .inspect_logs

agent:
	$(PYTHON) -m incidentops.agent.pipeline

dash:
	cd $(DASH_DIR) && $(PNPM) dev

lint:
	$(UV) run ruff check incidentops/
	$(UV) run ruff format --check incidentops/

test:
	$(UV) run pytest

clean:
	rm -rf .inspect_logs __pycache__ .pytest_cache
