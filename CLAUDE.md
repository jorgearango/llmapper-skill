# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LLMapper is a Claude skill that transforms articles into interactive concept maps through a four-stage LLM pipeline: Focusing Questions (user choice) → Summarization → RDF Knowledge Graph → Cytoscape Interactive Visualization. The skill focuses on extracting not just what a subject IS, but WHY IT MATTERS. Accepts multiple input formats (file uploads, URLs, pasted text) and runs in both Claude Code and Claude Desktop. File uploads (PDFs, text files, etc.) are the most reliable input method.

## Architecture

### Pipeline Stages

The skill processes articles through four sequential stages, each with its own prompt file:

1. **Stage 0: Focusing Questions** (`prompts/focusing-questions.md`)
   - Generates 3 distinct "dynamic focusing questions" exploring different perspectives
   - Each question focuses on a different aspect of why the subject matters
   - **User chooses** which perspective to use via AskUserQuestion tool
   - Output: Three focusing questions, user selects one

2. **Stage 1: Summarization** (`prompts/summarize.md`)
   - Uses "panel of experts" approach (Eugene, Mark, Jennie personas)
   - Extracts 10 most important concepts + 20+ relationships
   - Uses the user's chosen focusing question to guide analysis
   - Output: Markdown with sections (TITLE, WHAT THIS IS, WHY IT MATTERS, FOCUSING QUESTION, MAIN CONCEPTS, RELATIONSHIPS)

3. **Stage 2: RDF Generation** (`prompts/rdf.md`)
   - Converts concepts/relationships to Terse RDF Triple Language
   - Creates structured knowledge graph with subjects, predicates, objects
   - Output: Pure RDF code (no markdown, no comments, no backticks)

4. **Stage 3: Cytoscape Visualization** (`prompts/cytoscape.md`)
   - Transforms RDF into interactive HTML visualization using Cytoscape.js
   - Styled as rounded purple boxes with labeled arrows
   - Interactive: drag nodes, zoom, pan
   - Output: Complete HTML file saved to `/tmp/concept-map.html`
   - User opens file in browser for full interactivity
   - Note: `prompts/dot.md` is preserved for historical reference but not actively used

### File Structure

```
llmapper-skill/
├── SKILL.md                # Main skill definition (required by Claude Code)
├── extract-article.py      # Generic HTML text extractor (works with any website)
├── prompts/                # Pipeline stage prompts (DO NOT modify without testing)
│   ├── focusing-questions.md  # Stage 0: Generate 3 perspectives for user choice
│   ├── summarize.md        # Stage 1: Concept extraction with "panel of experts"
│   ├── rdf.md              # Stage 2: Knowledge graph generation (source of truth)
│   ├── cytoscape.md        # Stage 3: Interactive visualization (active)
│   └── dot.md              # Stage 3: Graphviz DOT (preserved for reference)
├── CLAUDE.md               # Developer documentation (this file)
├── README.md               # User-facing documentation
└── LICENSE                 # Project license
```

## Critical Design Principles

### Why the Prompts Are So Detailed

The prompt files contain extensive rules and negative constraints (e.g., "DO NOT use camelCase", "No compound subjects"). These were developed through iteration to prevent common LLM failure modes:

- Compound subjects/objects breaking graph structure
- CamelCase labels reducing readability
- Self-referential nodes creating loops
- Disconnected concepts producing fragmented graphs
- Generic relationships that don't explain "why it matters"

**IMPORTANT**: When applying prompts, use them EXACTLY as written. Do not summarize or simplify them.

### Non-Deterministic by Design

Each run produces different valid results. This is intentional - the "panel of experts" approach explores different perspectives on why a subject matters. Users should be told this is a feature, not a bug.

### RDF as Source of Truth

The RDF knowledge graph (Stage 2) is the **canonical representation** of the concept map:

- **Visualizations are derived from RDF**, not the other way around
- Multiple visualization formats can be generated from the same RDF
- RDF can be exported, imported, queried, and extended
- Future features will allow users to edit and augment the knowledge graph
- The skill preserves RDF between stages for this reason

This architecture enables:
- Switching between visualization formats (Cytoscape, Graphviz, etc.)
- Editing the knowledge graph independently of visualization
- Merging multiple knowledge graphs
- Querying the graph with SPARQL or similar tools

## Development Commands

### Testing the Skill

```bash
# Test in Claude Code by invoking the skill via natural language
# In the Claude Code chat:
"Create a concept map from https://en.wikipedia.org/wiki/Test_Article"

# Or:
"Use the llmapper skill on this article: [paste article text]"
```

### Installing/Updating the Skill

```bash
# Create symlink to keep skill synced during development
ln -s /path/to/llmapper-skill ~/.claude/skills/llmapper

# Or copy directory directly
cp -r /path/to/llmapper-skill ~/.claude/skills/llmapper

# Verify installation
ls -la ~/.claude/skills/llmapper/SKILL.md
```

### Validating Output Formats

```bash
# Validate RDF output (Stage 2)
# Expected: Pure RDF code, no markdown blocks, no comments
# Should start with: @prefix ex: <http://example.org/ns#> .

# Validate HTML output (Stage 3)
# Expected: Complete HTML file saved to /tmp/concept-map.html
# Should start with: <!DOCTYPE html>
# Should include Cytoscape CDN: <script src="https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js"></script>
# Should have valid JavaScript with elements array
# Check the file: open /tmp/concept-map.html
```

## Common Gotchas

### Output Format Violations

If the visualization doesn't render, check that:
- Stage 2 RDF has NO markdown code blocks (```), backticks, or comments
- Stage 3 HTML was saved to `/tmp/concept-map.html` (not output to chat)
- HTML is complete and valid (check for syntax errors in JavaScript)
- Cytoscape CDN loads properly (check browser console for errors)
- User was informed where to find the file

### Prompt Application Issues

- Do NOT simplify or paraphrase the prompt files when applying them
- Do NOT skip the negative rules (DO NOT...) - they prevent critical failures
- Each stage must use its FULL prompt file contents

### Label Formatting Rules

These rules apply to ALL three stages and prevent visualization failures:

- ❌ camelCase, snake_case, kebab-case, PascalCase
- ✅ Plain English phrases in quotes: "Star Wars", "Galactic Empire"
- ❌ Compound subjects/objects: "Peter and Mary visited cinema"
- ✅ Separate statements: "Peter visited cinema" + "Mary visited cinema"
- ❌ Self-referential: `"2011" -> "2011"[label="is a"];`
- ✅ Must point to different nodes

## Customization Guidance

### Adjusting Concept Count

Edit `prompts/summarize.md` line 41:
```markdown
# Current: "Choose the 10 MOST IMPORTANT concepts"
# Change to: "Choose the 15 MOST IMPORTANT concepts"
```

Then update line 53:
```markdown
# Current: "Include no fewer than 20 relationships"
# Change proportionally: "Include no fewer than 30 relationships"
```

### Changing Visual Style

Edit `prompts/cytoscape.md` HTML template to modify:
- Node colors: `'background-color': '#EDEEFA'` → `'background-color': '#yourcolor'`
- Border colors: `'border-color': '#9B8FD9'` → `'border-color': '#yourcolor'`
- Node shape: `'shape': 'roundrectangle'` → `'shape': 'ellipse'`
- Font: `'font-family': 'Arial'` → `'font-family': 'Helvetica'`
- Layout algorithm: `name: 'cose'` → `name: 'dagre'` or other Cytoscape layouts

### Unified Input Layer

The skill accepts content through a three-tier input abstraction layer. All input types normalize to "article text" before entering the pipeline.

**TIER 1: FILE UPLOAD (PRIMARY - Most Reliable)**
- PDFs, text files, Word documents, and other text-based formats
- User uploads directly to Claude (drag-and-drop in Claude Desktop)
- Uses Read tool to extract text (natively supports PDF extraction)
- **Most reliable method** - guarantees full content without summarization
- **Recommended for Claude Desktop users**
- No character limits or content filtering

**TIER 2: URL (SECONDARY - With Validation)**
- Any article URL (Wikipedia, news sites, blogs, etc.)
- Uses WebFetch to retrieve content
- **CRITICAL:** WebFetch may return summaries instead of full text
- Skill validates output using heuristics:
  - Length check (< 1000 chars suggests summary)
  - Content markers ("Summary:", "Overview:", "Key Points:")
  - Structural indicators (missing paragraph breaks)
- If summary detected, offers file upload alternative to user
- Fallback available using bash + Python (`extract-article.py`) in Claude Code

**TIER 3: PASTED TEXT (FALLBACK - Always Works)**
- User can paste article text directly into chat
- No validation needed - trust user input
- Guaranteed to work when other methods fail
- Last resort option

**Detection Logic:**
The skill automatically detects input type:
- File path or upload → Use Read tool (Tier 1)
- URL (http:// or https://) → Use WebFetch with validation (Tier 2)
- Plain text → Treat as pasted article (Tier 3)

**Primary target:** Claude Desktop with file uploads as the most reliable input method

## Skill Invocation Flow

```
User provides input (file upload, URL, or pasted text)
    ↓
STEP 0: Input Detection and Acquisition
    - Detect input type (file path, URL, or plain text)
    - FILE: Use Read tool to extract text
    - URL: Use WebFetch, validate full text vs. summary
           If summary detected → offer file upload alternative
    - TEXT: Accept as-is
    ↓
Apply prompts/focusing-questions.md → Generate 3 focusing questions
    ↓
AskUserQuestion → User selects preferred perspective
    ↓
Apply prompts/summarize.md with chosen question → Show summary to user
    ↓
Apply prompts/rdf.md → Generate RDF (source of truth, stored)
    ↓
Apply prompts/cytoscape.md → Save HTML to /tmp/concept-map.html
    ↓
Inform user where to find the file and how to open it
    ↓
Offer refinement options (including choosing different focusing question)
```

## Related Documentation

- Main skill definition: `SKILL.md`
- User documentation: `README.md`
- Developer documentation: `CLAUDE.md` (this file)
- Original LLMapper bash tool: https://github.com/yourusername/llmapper (TBD)
- Graphviz DOT language: https://graphviz.org/doc/info/lang.html
- RDF Primer: https://www.w3.org/TR/rdf11-primer/
- Claude Code Skills: https://docs.claude.com/en/docs/claude-code/skills
