.PHONY: check test clean

# Default target
all: check test

# Quick checks using the quickhead script
check:
	@./src/scripts/quickhead.sh

# Run all tests
test:
	pytest src/tests -v

# Clean up Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".ruff_cache" -exec rm -r {} +

# Show help
help:
	@echo "Available targets:"
	@echo "  make        - Run all checks and tests"
	@echo "  make check  - Run quick checks"
	@echo "  make test   - Run all tests"
	@echo "  make clean  - Clean up cache files"