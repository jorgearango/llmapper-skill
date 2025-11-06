# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LLMapper is a Claude skill that transforms articles into concept maps through a four-stage LLM pipeline: Focusing Questions (user choice) → Summarization → RDF Knowledge Graph → Mermaid Visualization. The skill focuses on extracting not just what a subject IS, but WHY IT MATTERS. Accepts multiple input formats (file uploads, URLs, pasted text) and runs in Claude Code, Claude Desktop, and Claude on the web. File uploads (PDFs, text files, etc.) are the most reliable input method. Mermaid diagrams are saved to `/tmp/[subject]-concept-map.mermaid` and render inline as artifacts.

**Output Mode:** By default, the skill operates in **concise mode** - only showing focusing questions and the final diagram. User can request "verbose mode" to see intermediate outputs (summary, RDF, detailed explanations).

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

4. **Stage 3: Mermaid Visualization (Default)** (`prompts/mermaid.md`)
   - Transforms RDF into Mermaid flowchart diagram
   - Styled as rounded purple boxes with labeled arrows on white background
   - **Dual output**: Displays inline as artifact AND saves to `/tmp/[subject]-concept-map.mermaid`
   - Uses .mermaid extension (required for Claude artifact rendering)
   - Generates descriptive filename from article subject
   - Includes white background theme for legibility
   - Preserves full complexity and richness of knowledge graph
   - Output: Diagram rendered as artifact + .mermaid file with meaningful name for reuse

   **Alternative: Cytoscape Visualization** (`prompts/cytoscape.md`)
   - For Claude Code users or when HTML output is preferred
   - Interactive HTML visualization using Cytoscape.js
   - Features: drag nodes, zoom, pan
   - Generates descriptive filename from article subject
   - Output: Complete HTML file saved to `/tmp/[subject]-concept-map.html`
   - User opens file in browser for full interactivity

   **Historical Reference**: `prompts/dot.md` preserved for Graphviz DOT format

### File Structure

```
llmapper-skill/
├── SKILL.md                # Main skill definition (required by Claude Code)
├── extract-article.py      # Generic HTML text extractor (works with any website)
├── prompts/                # Pipeline stage prompts (DO NOT modify without testing)
│   ├── focusing-questions.md  # Stage 0: Generate 3 perspectives for user choice
│   ├── summarize.md        # Stage 1: Concept extraction with "panel of experts"
│   ├── rdf.md              # Stage 2: Knowledge graph generation (source of truth)
│   ├── mermaid.md          # Stage 3: Mermaid visualization (default, renders inline)
│   ├── cytoscape.md        # Stage 3: Cytoscape HTML (alternative for Claude Code)
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
- The skill preserves RDF throughout the conversation for iterative refinement
- **ALL user-requested changes must be applied to the RDF first, then visualizations regenerated**

This architecture enables:
- Switching between visualization formats (Mermaid, Cytoscape, Graphviz, etc.)
- Editing the knowledge graph independently of visualization
- Merging multiple knowledge graphs
- Querying the graph with SPARQL or similar tools
- Reliable iterative refinement through RDF-first workflow

**CRITICAL WORKFLOW RULE:**
When users request changes after initial generation:
1. Never modify visualization code directly
2. Always retrieve the stored RDF
3. Apply changes to the RDF knowledge graph
4. Store the updated RDF
5. Regenerate visualization from the updated RDF

This ensures consistency and reliability across multiple refinements.

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

# Validate Mermaid output (Stage 3 - Default)
# Expected: TWO outputs
#   1. Diagram displayed inline in chat as artifact (should render with white background)
#   2. Raw Mermaid file saved to /tmp/[subject]-concept-map.mermaid (NO code blocks)
# Filename should be descriptive based on article subject
# Example: "To the Lighthouse" → to-the-lighthouse-concept-map.mermaid
# CRITICAL: File must use .mermaid extension for Claude artifact rendering
# Diagram should:
#   - Start with: %%{init: {'theme':'base', 'themeVariables': {...}}}%%
#   - Include white background configuration
#   - Use: flowchart TD or flowchart LR
#   - Have: classDef conceptNode fill:#EDEEFA,stroke:#9B8FD9...
#   - Include all nodes with :::conceptNode class
#   - Have all edges with -->|label| syntax
# Chat output: wrapped in ```mermaid code block
# File output: raw Mermaid code (NO backticks)
# Check inline rendering as artifact in Claude interface
# Verify file: ls /tmp/*-concept-map.mermaid

# Validate Cytoscape HTML output (Stage 3 - Alternative)
# Expected: Complete HTML file saved to /tmp/[subject]-concept-map.html
# Filename should be descriptive based on article subject
# Should start with: <!DOCTYPE html>
# Should include Cytoscape CDN: <script src="https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js"></script>
# Should have valid JavaScript with elements array
# Check the file: ls /tmp/*-concept-map.html && open /tmp/[filename]
```

## RDF Storage and Management

### Storing RDF During Conversation

The RDF knowledge graph must persist throughout the conversation to enable iterative refinement:

**After generating RDF (Stage 2):**
```
Store the RDF output in conversation context
This can be done by:
- Keeping it in working memory as a variable
- Including it in subsequent prompts as context
- Referencing it explicitly when needed
```

**When user requests changes:**
```
1. Retrieve the RDF from storage
2. Understand the user's change request
3. Modify the RDF accordingly:
   - Adding new triples for new concepts/relationships
   - Removing triples for deletions
   - Modifying subjects/predicates/objects for edits
4. Validate the updated RDF (check syntax, no self-references, etc.)
5. Store the updated RDF (replacing the old version)
6. Pass the updated RDF to the visualization prompt
```

**Example change workflow:**
```
User: "Add a relationship between AI and job displacement"

Step 1: Retrieve current RDF
Step 2: Analyze what exists (AI node? job displacement node?)
Step 3: Add necessary triples:
   - If nodes don't exist, create them
   - Add relationship triple connecting them
Step 4: Store updated RDF
Step 5: Regenerate Mermaid/Cytoscape from updated RDF
```

### Why This Matters

- **Consistency**: Visualization always matches the knowledge graph
- **Traceability**: Changes are applied systematically
- **Extensibility**: Can add features like RDF export, diff, merge
- **Reliability**: Less likely to introduce visualization syntax errors
- **Future-proof**: Enables advanced features (SPARQL queries, graph algorithms)

## Common Gotchas

### Output Format Violations

**For Mermaid (Default):**
If the visualization doesn't render inline, check that:
- Stage 2 RDF has NO markdown code blocks (```), backticks, or comments
- Stage 3 Mermaid uses DUAL output:
  - First outputs diagram directly in chat (for inline rendering)
  - Then saves to `/tmp/concept-map.md` (for persistence)
- Diagram syntax is valid Mermaid (no syntax errors)
- Starts with ```mermaid and ends with ```
- All nodes have the :::conceptNode class applied
- Node IDs are alphanumeric (no spaces, only underscores allowed)
- Edge labels use proper |label| syntax
- classDef is defined at the top with correct colors
- User was informed diagram is displayed above AND saved to file

**For Cytoscape HTML (Alternative):**
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

**For Mermaid (Default):**
Edit `prompts/mermaid.md` classDef section to modify:
- Node fill color: `fill:#EDEEFA` → `fill:#yourcolor`
- Border color: `stroke:#9B8FD9` → `stroke:#yourcolor`
- Border width: `stroke-width:2px` → `stroke-width:3px`
- Font: `font-family:Arial` → `font-family:Helvetica`
- Layout direction: `flowchart TD` → `flowchart LR` (top-down vs left-right)

**For Cytoscape HTML (Alternative):**
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

**CONCISE MODE (default):**
```
User provides input (file upload, URL, or pasted text)
    ↓
STEP 0: Input Detection and Acquisition
    - Detect input type silently (file path, URL, or plain text)
    - FILE: Use Read tool to extract text
    - URL: Use WebFetch, validate full text vs. summary
           If summary detected → offer file upload alternative
    - TEXT: Accept as-is
    ↓
Apply prompts/focusing-questions.md → Generate 3 focusing questions
    ↓
AskUserQuestion → User selects preferred perspective
    ↓
Apply prompts/summarize.md with chosen question (silently - no output shown)
    ↓
Apply prompts/rdf.md → Generate RDF (source of truth, stored internally)
    ↓
Apply prompts/mermaid.md → Output diagram inline + save to /tmp/[subject]-concept-map.mermaid
    ↓
Brief confirmation: "Saved to /tmp/[filename]"
    ↓
User can request changes or ask for verbose mode
    ↓
IF USER REQUESTS CHANGES:
    ↓
    Retrieve stored RDF silently
    ↓
    Apply changes to RDF (add/remove/modify nodes or relationships)
    ↓
    Store updated RDF (replace previous)
    ↓
    Regenerate visualization from updated RDF
    ↓
    Output updated diagram inline + save to /tmp/[same-filename]
    ↓
    Brief confirmation: "Updated and saved."
```

**VERBOSE MODE (when user requests):**
```
Same flow as above, but:
    - Show summary output after Stage 1
    - Show RDF output after Stage 2
    - Provide detailed explanations at each step
    - Detailed file save information
    - Offer refinement options explicitly
```

**ALTERNATIVE FLOW (for interactive HTML preference):**
```
    Apply prompts/cytoscape.md → Save HTML to /tmp/[subject]-concept-map.html
    ↓
    Inform user where to find the file and how to open it
```

## Related Documentation

- Main skill definition: `SKILL.md`
- User documentation: `README.md`
- Developer documentation: `CLAUDE.md` (this file)
- Original LLMapper bash tool: https://github.com/yourusername/llmapper (TBD)
- Mermaid Documentation: https://mermaid.js.org/intro/
- Mermaid Flowchart Syntax: https://mermaid.js.org/syntax/flowchart.html
- Graphviz DOT language: https://graphviz.org/doc/info/lang.html
- RDF Primer: https://www.w3.org/TR/rdf11-primer/
- Claude Code Skills: https://docs.claude.com/en/docs/claude-code/skills
