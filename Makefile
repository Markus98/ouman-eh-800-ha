.PHONY: check lint format typecheck test

check: lint format typecheck test

lint:
	ruff check custom_components/ouman_eh_800/

format:
	ruff format --check custom_components/ouman_eh_800/

typecheck:
	mypy custom_components/ouman_eh_800/

test:
	pytest
