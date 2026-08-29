# Common tasks. Run `make help` for the list.
# Everything runs inside .venv — no need to activate it yourself.

PY := .venv/bin/python
RUN := $(PY) -m orchestrator.run

.DEFAULT_GOAL := help
.PHONY: help setup doctor agents pipelines store clean check tier1 audit watch

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN{FS=":.*?## "}{printf "  \033[1m%-12s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "  Run an agent directly:"
	@echo "    $(RUN) agent ophtha_science --input inputs/brief.md --set asset=TBC-101"

setup: ## First-time local setup (venv, deps, .env, preflight)
	./bootstrap.sh

doctor: ## Check config, agents and which Ollama models are missing
	@$(RUN) doctor

agents: ## List agents and their configured models
	@$(RUN) agents

pipelines: ## List pipelines and their stages
	@$(RUN) pipelines

store: ## List every agent's workspace files
	@$(RUN) store ls

tier1: ## Run the Tier 1 pipeline (INPUT=inputs/your-brief.md)
	@test -n "$(INPUT)" || { echo "usage: make tier1 INPUT=inputs/brief.md"; exit 1; }
	$(RUN) pipeline tier1_assessment --input $(INPUT)

audit: ## Audit a draft against brand + guardrails (FILE=path)
	@test -n "$(FILE)" || { echo "usage: make audit FILE=outputs/drafts/x.md"; exit 1; }
	$(RUN) agent brand_voice --set mode=AUDIT \
		--set ask="Audit this against BRAND.md and GUARDRAILS.md" --input $(FILE)

watch: ## Run the standing literature scan (INPUT=inputs/papers.md)
	@test -n "$(INPUT)" || { echo "usage: make watch INPUT=inputs/papers.md"; exit 1; }
	$(RUN) pipeline lit_watch --input $(INPUT)

check: ## Sanity-check the codebase (imports, config, gitignore)
	@$(PY) -c "import compileall,sys; sys.exit(0 if compileall.compile_dir('orchestrator', quiet=2) else 1)"
	@$(PY) -c "from orchestrator.config import load_yaml; load_yaml('config/models.yaml'); load_yaml('config/orchestration.yaml'); print('  config parses')"
	@$(PY) -c "from orchestrator.agent import available_agents, build_system_prompt as b; \
		[b(a) for a in available_agents()]; print('  all agent prompts assemble')"
	@git check-ignore -q .env && echo "  .env ignored" || { echo "  !! .env NOT ignored"; exit 1; }
	@echo "  ok"

clean: ## Remove drafts, caches and workspace working files (keeps approved/)
	rm -rf outputs/drafts/*.md **/__pycache__ orchestrator/__pycache__ .pytest_cache
	find workspace -type f ! -name '.gitkeep' -delete 2>/dev/null || true
	@echo "cleaned (outputs/approved/ left alone)"
