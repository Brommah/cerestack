# Makefile for Cere Stack Article Management

.PHONY: all generate watch clean help

# Default target
all: generate

# Generate the full article
generate:
	@echo "📝 Generating full article..."
	@python3 generate_article.py

# Watch for changes and auto-generate
watch:
	@echo "👁️  Starting watch mode..."
	@python3 watch_and_generate.py

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	@rm -f full_article.md full_article_professional.md
	@echo "✅ Clean complete"

# Show help
help:
	@echo "Cere Stack Article Management"
	@echo "============================"
	@echo ""
	@echo "Available commands:"
	@echo "  make generate  - Generate full article from sections"
	@echo "  make watch     - Watch for changes and auto-regenerate"
	@echo "  make clean     - Remove generated article files"
	@echo "  make help      - Show this help message"
	@echo ""
	@echo "Quick usage:"
	@echo "  make          - Same as 'make generate'"
