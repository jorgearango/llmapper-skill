# LLMapper Skill

A Claude skill that generates concept maps from articles using a multi-stage LLM pipeline. Works with **file uploads** (PDFs, text files), **URLs**, and **pasted text**. Displays Mermaid diagrams inline in Claude and saves them for reuse.

## Overview

LLMapper transforms articles into interactive visual knowledge graphs that answer two key questions:
1. **What is this subject about?**
2. **Why does this subject matter?**

The skill processes content through four stages:
1. **Focusing Questions** - Generate 3 perspectives, user chooses one
2. **Summarization** - Extract key concepts and relationships (with emphasis on distinctions and contrasts)
3. **RDF Generation** - Structure as knowledge graph (canonical source of truth)
4. **Mermaid Rendering** - Visual flowchart diagram that renders inline as Claude artifact

## Installation

**Option 1: Download ZIP (easiest)**
1. Download [llmapper-skill.zip](llmapper-skill.zip)
2. Unzip to `~/.claude/skills/llmapper`

**Option 2: Clone repository**
```bash
git clone http://github.com/jorgearango/llmapper-skill ~/.claude/skills/llmapper
```

**Verify installation:**
```bash
ls -la ~/.claude/skills/llmapper/SKILL.md
```

## Usage

### Invoke the Skill

Use natural language to invoke:
```
Create a concept map from this article
Use the llmapper skill on this URL
Generate a knowledge graph of [topic]
```

Claude will automatically detect when to activate the llmapper skill based on your request.

### Provide Content

**Method 1: File Upload (RECOMMENDED)**
- Drag and drop a PDF, text file, or Word document
- Most reliable - guarantees full content
- No web blocking issues

**Method 2: URL**
- Paste any article URL
- Works best with accessible websites
- Note: Some sites (including Wikipedia) may block WebFetch

**Method 3: Paste Text**
- Copy article text and paste directly
- Fallback when other methods fail

### Workflow

1. **Input** - Provide article via file/URL/text (silently processed)
2. **Choose perspective** - Select from 3 focusing questions
3. **Processing** - Runs silently (no narration or intermediate outputs)
4. **View diagram** - Mermaid diagram appears inline as Claude artifact
5. **Auto-save** - Confirmation: "Saved to /tmp/[subject]-concept-map.mermaid"
6. **Refine** (optional) - Request changes; RDF updates first, visualization regenerates

### Output Modes

**Concise Mode (Default)**
- No narration or explanations
- Only shows: focusing questions → diagram → save confirmation
- Clean, minimal output
- Request "verbose mode" to see intermediate stages (summary, RDF, details)

**Verbose Mode (Opt-in)**
- Shows summary after concept extraction
- Displays RDF knowledge graph
- Explains each processing stage
- Detailed file save information
- Say "verbose mode" or "show me the details" to activate

## How It Works

### Four-Stage Pipeline

```
Article Input (file/URL/text)
    ↓
Stage 0: Focusing Questions (generate 3, user picks 1)
    ↓
Stage 1: Summarization (panel of experts)
    ↓
Stage 2: RDF Knowledge Graph (source of truth)
    ↓
Stage 3: Mermaid Visualization
    ↓
Renders as artifact in Claude + saves to /tmp/[subject]-concept-map.mermaid

Alternative: Cytoscape HTML (interactive)
    ↓
Saved to /tmp/[subject]-concept-map.html → Open in browser
```

### Unified Input Layer

The skill automatically detects input type and routes appropriately:

**Tier 1: File Upload (PRIMARY)**
- PDFs, text files, Word docs
- Most reliable - no web blocking
- Full content guaranteed

**Tier 2: URL (SECONDARY)**
- Fetches via WebFetch
- Validates full text vs. summary
- Offers file upload if blocked

**Tier 3: Pasted Text (FALLBACK)**
- Direct text input
- Always works

### Prompt Engineering

The skill uses carefully engineered prompts in `prompts/`:

1. **`focusing-questions.md`** - Generates 3 dynamic perspectives
2. **`summarize.md`** - "Panel of experts" with distinction/contrast emphasis
3. **`rdf.md`** - Converts to RDF triples with strict rules
4. **`mermaid.md`** - Transforms to Mermaid flowchart (default, renders inline)
5. **`cytoscape.md`** - Transforms to interactive HTML (alternative for Claude Code)

These prompts contain extensive rules developed through iteration to prevent LLM failure modes.

### Technical Features

**Concise Output Mode**
- Silent processing - no narration or "thinking out loud"
- Shows only: focusing questions → diagram → save confirmation
- Optional verbose mode for seeing intermediate stages
- Clean, minimal user experience

**Distinction & Contrast Emphasis**
- Actively identifies opposing concepts (e.g., "Specialized Tools" vs. "General-Purpose Agents")
- Highlights alternatives and before/after states
- Understanding comes from distinctions, not just definitions

**User-Chosen Perspective**
- 3 dynamically generated focusing questions explore different angles
- Each leads to different concept maps from the same content
- Explores *why* the subject matters from various viewpoints
- Non-deterministic by design - encourages exploration

**RDF as Source of Truth**
- Knowledge graph is canonical representation
- All user-requested changes applied to RDF first
- Visualization regenerated from updated RDF
- Enables reliable iterative refinement
- Consistent state management across multiple edits
- Visualizations always derived from RDF (never edited directly)

**White Background Container**
- Mermaid diagrams wrapped in white subgraph
- White edge label backgrounds
- Ensures legibility in both dark and light modes
- Professional appearance across all viewing contexts

## Customization

### Adjust Concept Count

Edit `prompts/summarize.md` line 59:
```markdown
# Current: "Choose the 10 MOST IMPORTANT concepts"
# Change to: "Choose the 15 MOST IMPORTANT concepts"
```

Then update line 78:
```markdown
# Current: "Include no fewer than 20 relationships"
# Change proportionally: "Include no fewer than 30 relationships"
```

### Modify Visual Style

**For Mermaid (default):**
Edit `prompts/mermaid.md` classDef to change:
- Node fill color: `fill:#EDEEFA`
- Border color: `stroke:#9B8FD9`
- Layout direction: `flowchart TD` (top-down) vs `flowchart LR` (left-right)

**For Cytoscape HTML (alternative):**
Edit `prompts/cytoscape.md` to change:
- Node colors: `'background-color': '#EDEEFA'`
- Border colors: `'border-color': '#9B8FD9'`
- Layout algorithm: `name: 'cose'` (try 'dagre', 'circle', etc.)

### Alternative Visualizations

The skill supports multiple visualization formats:
- **Mermaid** (default) - inline rendering
- **Cytoscape** (alternative) - interactive HTML
- **Graphviz DOT** (historical) - `prompts/dot.md` preserved for reference

You could add other formats like D3.js or custom SVG output.

## Troubleshooting

### WebFetch Returns Summary Instead of Full Text
- **Solution:** Use file upload instead
- The skill validates WebFetch output and will notify you

### Can't See the Visualization
- **Mermaid (default):** Should display inline in Claude as artifact automatically
  - Diagram appears in the conversation as a rendered flowchart
  - If not visible, check saved file: `/tmp/[subject]-concept-map.mermaid`
  - List files: `ls /tmp/*-concept-map.mermaid`
  - Open file in Markdown viewer to see it rendered
- **If you requested HTML:** Check `/tmp/[subject]-concept-map.html`
  - List files: `ls /tmp/*-concept-map.html`
  - Open with: `open /tmp/[filename]` (macOS) or drag to browser

### Missing Expected Concepts
- Try regenerating (non-deterministic by design)
- Try a different focusing question
- Request specific additions (e.g., "add a node about X")
- Adjust concept count in `summarize.md`

### Map Doesn't Answer Focusing Question
- The updated prompts emphasize this
- Should include application concepts, limitations, distinctions
- Report as issue if consistently poor

### Making Changes After Initial Generation

**RDF-First Workflow:**
When you request changes, the skill follows this process:
1. Retrieves stored RDF knowledge graph
2. Applies changes to RDF (add/remove/modify nodes or relationships)
3. Stores updated RDF
4. Regenerates visualization from updated RDF
5. Outputs updated diagram with brief confirmation: "Updated."

This ensures consistency and enables multiple iterative refinements.

**Example Change Requests:**
- "Add a node about machine learning ethics"
- "Remove the relationship between X and Y"
- "Add a connection showing how A enables B"
- "Change the label on the 'AI' node to 'Artificial Intelligence'"
- "Show more emphasis on the ethical implications"
- "Remove nodes that aren't central to the focusing question"

**Concise Mode (Default):**
- Changes processed silently
- Updated diagram appears with no preamble
- Brief confirmation: "Updated."

**Verbose Mode:**
- Shows which RDF triples were modified
- Explains what changed in the visualization
- Detailed confirmation of save location

## Known Limitations

1. **Mermaid layout constraints** - Automatic layout may not be optimal for very large graphs (30+ nodes); consider requesting Cytoscape HTML for complex graphs
2. **Inline rendering platform-specific** - Mermaid displays inline in Claude web/desktop as artifacts; saved file can be used in other tools
3. **Wikipedia may block WebFetch** - Use file upload (PDF or text) instead when sites block access
4. **Non-deterministic output** - Different runs produce different maps from same content (by design - encourages exploration)
5. **Article length limits** - Very long articles may be truncated; consider splitting or summarizing first
6. **Fixed output location** - Files save to `/tmp/` directory; future versions may support custom paths
7. **Session file persistence** - Regenerating a map for same subject overwrites previous file (feature for iterative refinement)

## Related Resources

- [Original LLMapper bash tool](http://github.com/jorgearango/llmapper)
- [Mermaid Documentation](https://mermaid.js.org/intro/)
- [Mermaid Flowchart Syntax](https://mermaid.js.org/syntax/flowchart.html)
- [Cytoscape.js Documentation](https://js.cytoscape.org/)
- [RDF Primer](https://www.w3.org/TR/rdf11-primer/)
- [Concept Mapping Theory](https://en.wikipedia.org/wiki/Concept_map)
- [Claude Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)

## License

Apache 2.0

## Questions or Issues?

For issues with the skill, please open an issue in this repository.
