format: 
	uvx ruff format src/

check: format
	uvx ruff check src/

lint: check
	uv run pyright src/

run:
	uv run python src/main.py