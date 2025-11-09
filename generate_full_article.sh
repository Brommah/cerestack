#!/bin/bash

# Script to generate full article by concatenating all sections
# This ensures the full article is always up-to-date with individual section changes

OUTPUT_FILE="full_article.md"

echo "Generating full article..."

# Clear the output file
> "$OUTPUT_FILE"

# Add a header
echo "# Cere Stack: From the Cerebellum to the Cephalum - A Complete System Architecture" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Concatenate all sections in order
# Using tail -n +3 to skip the first two lines (title and blank line) from each section
# except the introduction where we keep everything

# Introduction (keep full content)
cat introduction.md >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Layer 1-7 (skip their individual titles)
tail -n +3 layer1-blockchain.md >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

tail -n +3 layer2-data-infrastructure.md >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

tail -n +3 layer3-data-processing.md >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

tail -n +3 layer4-ai-orchestration.md >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

tail -n +3 layer5-validation-economics.md >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

tail -n +3 layer6-infrastructure.md >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

tail -n +3 layer7-developer-tools.md >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Conclusion (skip title)
tail -n +3 conclusion.md >> "$OUTPUT_FILE"

echo "Full article generated in $OUTPUT_FILE"
echo "Total lines: $(wc -l < "$OUTPUT_FILE")"
