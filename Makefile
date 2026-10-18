.PHONY: install run debug clean lint lint-strict test fclean

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs

install:
	uv sync

run:
	uv run python -m src $(ARGS)

debug:
	uv run python -m pdb -m src $(ARGS)

clean:
	find . -type d \( -name __pycache__ -o -name .mypy_cache -o -name .pytest_cache \) \
		-not -path "./.venv/*" -prune -exec rm -rf {} +

fclean: clean
	rm -rf .venv

lint:
	uv run flake8 app/ pac-man.py
	uv run mypy app/ pac-man.py $(MYPY_FLAGS)

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

test:
	uv run pytest
