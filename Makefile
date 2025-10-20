format: 
	uvx ruff format src/

check: format
	uvx ruff check src/

lint: check
# 	uv run pyright src/