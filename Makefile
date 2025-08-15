# BentoML Service Management with Conda + UV

CONDA_ENV=githubscreening
PYTHON_VERSION=3.13

.PHONY: help setup-env activate up serve build clean freeze-deps save-model

help:  ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

setup-env:  ## Create conda environment and install uv
	conda create -n $(CONDA_ENV) python=$(PYTHON_VERSION) -y || true
	eval "$$(conda shell.bash hook)" && conda activate $(CONDA_ENV) && pip install uv

activate:  ## Activate conda environment (use: eval $$(make activate))
	@echo "eval \"\$$(conda shell.bash hook)\" && conda activate $(CONDA_ENV)"

freeze-deps:  ## Freeze dependencies for reproducibility
	eval "$$(conda shell.bash hook)" && conda activate $(CONDA_ENV) && uv pip freeze > requirements.txt
	conda env export > environment.yml

up:  ## Update bentofile.yaml with pipreqs
	uv run python scripts/update_bentofile.py

serve: up  ## Serve BentoML service
	cd src/serving && uv run bentoml serve service.py:service --reload

load:  ## Load trained model to BentoML
	cd src/serving && uv run python load_model.py

build: up  ## Build BentoML service
	cd src/serving && uv run bentoml build

clean:  ## Clean generated files
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +