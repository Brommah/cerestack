#!/usr/bin/env python3
"""
Generate full article from individual section files.
This script concatenates all sections while maintaining proper formatting.
"""

import os
from pathlib import Path
from datetime import datetime

def read_file_content(filepath, skip_lines=0):
    """Read file content, optionally skipping initial lines."""
    # Try to find the file in multiple locations
    possible_paths = [
        filepath,  # Current directory
        f"../{filepath}",  # Parent directory
        f"../Key Article Content/{filepath}",  # Key Article Content directory
    ]
    
    for path in possible_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return ''.join(lines[skip_lines:])
        except FileNotFoundError:
            continue
    
    print(f"Warning: {filepath} not found in any expected location")
    return ""

def generate_full_article():
    """Generate the complete article by concatenating all sections."""
    
    # Define the sections in order
    sections = [
        ("introduction.md", 0),  # Keep full content including title
        ("layer1-blockchain.md", 2),  # Skip title and blank line
        ("layer2-data-infrastructure.md", 2),
        ("layer3-data-processing.md", 2),
        ("layer4-ai-orchestration.md", 2),
        ("layer5-validation-economics.md", 2),
        ("layer6-infrastructure.md", 2),
        ("layer7-developer-tools.md", 2),
        ("conclusion.md", 2),
        ("cere_dao_governance.md", 0),  # Include the DAO article
    ]
    
    # Start building the article
    article_content = []
    
    # Add main title
    article_content.append("# Cere Stack: From the Cerebellum to the Cephalum - A Complete System Architecture")
    article_content.append("")
    article_content.append(f"*Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}*")
    article_content.append("")
    
    # Process each section
    for i, (filename, skip_lines) in enumerate(sections):
        content = read_file_content(filename, skip_lines)
        if content:
            article_content.append(content.rstrip())
            
            # Add separator between sections (except after the last one)
            if i < len(sections) - 1:
                article_content.append("")
                article_content.append("---")
                article_content.append("")
    
    # Join all content
    full_article = '\n'.join(article_content)
    
    # Write to output file (in parent directory)
    output_file = "../full_article.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_article)
    
    # Also generate a version without emojis for professional use
    professional_article = full_article
    emojis_to_remove = ['🏗️', '🔒', '📊', '🤖', '🔄', '⚙️', '🛠️', '✨', '👉']
    for emoji in emojis_to_remove:
        professional_article = professional_article.replace(emoji + ' ', '')
    
    with open("../full_article_professional.md", 'w', encoding='utf-8') as f:
        f.write(professional_article)
    
    # Print statistics
    word_count = len(full_article.split())
    line_count = len(full_article.splitlines())
    char_count = len(full_article)
    
    print(f"✅ Full article generated successfully!")
    print(f"📄 Output files:")
    print(f"   - full_article.md (with emojis)")
    print(f"   - full_article_professional.md (without emojis)")
    print(f"📊 Statistics:")
    print(f"   - Lines: {line_count:,}")
    print(f"   - Words: {word_count:,}")
    print(f"   - Characters: {char_count:,}")
    print(f"   - Estimated reading time: {word_count // 250} minutes")

if __name__ == "__main__":
    # Change to the script's directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Generate the article
    generate_full_article()
