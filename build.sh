#!/bin/bash
# build.sh - Creates distribution ZIP for llmapper skill

# Recreate ZIP with skill files only
zip -r llmapper-skill.zip \
  SKILL.md \
  prompts/ \
  extract-article.py \
  README.md \
  LICENSE \
  -x "*.git*" -x "__pycache__*" -x "*.pyc" -x "build.sh" -x "*.zip" -x "*.png" -x "*.jpg" -x "*.jpeg"

echo "✓ Created llmapper-skill.zip"
