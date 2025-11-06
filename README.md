# LLMapper Skill

A Claude skill that generates concept maps from articles using a multi-stage LLM pipeline. Works with **file uploads** (PDFs, text files), **URLs**, and **pasted text**. Saves Mermaid diagrams that can be viewed in any markdown renderer or pasted into Claude/GitHub.

## Overview

LLMapper transforms articles into interactive visual knowledge graphs that answer two key questions:
1. **What is this subject about?**
2. **Why does this subject matter?**

The skill processes content through four stages:
1. **Focusing Questions** - Generate 3 perspectives, user chooses one
2. **Summarization** - Extract key concepts and relationships (with emphasis on distinctions and contrasts)
3. **RDF Generation** - Structure as knowledge graph
4. **Mermaid Rendering** - Visual flowchart diagram that renders inline

## Installation

### Claude Desktop

1. Clone or download this repository
2. Open Claude Desktop
3. Go to **Settings → Capabilities → Skills**
4. Click **"Add skill"** and select the `llmapper-skill` directory

Alternatively, manually copy to Claude Desktop's skills directory (location varies by platform).

### Claude Code (Recommended for Development)

Clone or download this repository, then create a symlink to the skill directory:

```bash
# Clone the repository
git clone https://github.com/yourusername/llmapper-skill.git

# Create symlink (development mode - changes sync automatically)
ln -s /path/to/llmapper-skill ~/.claude/skills/llmapper

# Or copy the directory (static installation)
cp -r /path/to/llmapper-skill ~/.claude/skills/llmapper
```

Verify installation:
```bash
ls -la ~/.claude/skills/llmapper/SKILL.md
```

## Usage

### Invoke the Skill

**Claude Desktop:**
Upload your skill ZIP via Settings → Capabilities → Skills, then use natural language:
```
Create a concept map from this article
Generate a knowledge graph of [topic]
Visualize the relationships in this paper
```

**Claude Code:**
Once installed to `~/.claude/skills/`, use natural language to invoke:
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

1. **Input** - Provide article via file/URL/text
2. **Choose perspective** - Select from 3 focusing questions
3. **Review summary** - Verify extracted concepts
4. **Get visualization** - Mermaid diagram saved to `/tmp/concept-map.md`
5. **View the map** - Open in markdown viewer or paste into Claude/GitHub
6. **Refine** - Regenerate with different focus or try again

## Example Output

The skill produces Mermaid flowchart diagrams saved to `/tmp/concept-map.md`:
- **Nodes**: Purple rounded boxes containing concepts
- **Edges**: Labeled arrows showing relationships
- **Portable**: Can be viewed in any markdown renderer
- **Paste-friendly**: Copy and paste into Claude, GitHub, or other platforms to see rendered diagram
- **Rich complexity**: Shows all concepts and relationships from the knowledge graph

**Alternative output**: Interactive HTML visualization saved to `/tmp/concept-map.html` with drag, zoom, and pan features.

**Key features:**
- Emphasizes **why the subject matters**, not just facts
- Highlights **distinctions and contrasts** (e.g., "LLMs" vs. "AGI")
- Uses strong verbs: "threatens", "enables", "transforms", "challenges"
- Non-deterministic - each run explores different valid perspectives

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
Stage 3: Mermaid Visualization (saved to /tmp/concept-map.md)
    ↓
View in markdown viewer or paste into Claude/GitHub

Alternative: Cytoscape HTML (interactive)
    ↓
Saved to /tmp/concept-map.html → Open in browser
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

### Key Features

**Distinction & Contrast Emphasis**
- Actively identifies opposing concepts (e.g., "Specialized Tools" vs. "General-Purpose Agents")
- Highlights alternatives and before/after states
- **Understanding comes from distinctions**

**User-Chosen Perspective**
- 3 focusing questions explore different angles
- Each leads to different concept maps
- Explores *why* the subject matters from various viewpoints

**RDF as Source of Truth**
- Knowledge graph is canonical representation
- Can be exported, imported, queried
- Visualizations derived from RDF

## Important Notes

### Output Format

**Default (Mermaid):** The visualization is saved to `/tmp/concept-map.md`. You can:
- Open it in any markdown viewer (VS Code, Typora, Obsidian, etc.)
- Paste the contents into Claude to see it rendered inline
- Paste into GitHub comments/issues to share
- Use with any tool that renders Mermaid diagrams

**Alternative (Cytoscape HTML):** If you request HTML output for interactive features, the visualization is saved to `/tmp/concept-map.html`. Open this file in any web browser (Chrome, Firefox, Safari, etc.) for full interactivity with drag, zoom, and pan features.

**Session-persistent:** Both output files have fixed names and will be overwritten if you generate a new map in the same session. This allows for iterative refinement.

### Wikipedia Access

Wikipedia and some other sites may block WebFetch. **Solution:** Upload Wikipedia articles as PDFs or paste the text.

**Workflow:**
1. Go to Wikipedia article in browser
2. File → Print → Save as PDF
3. Upload PDF to Claude Desktop
4. Run `/llmapper`

### Optional: Text Extraction (Claude Code only)

The `extract-article.py` script provides faster HTML text extraction but is optional. The skill works without it using WebFetch.

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
- **Mermaid (default):** Check `/tmp/concept-map.md`
- **How to view:** Open in markdown viewer or paste contents into Claude/GitHub
- **If you requested HTML:** Check `/tmp/concept-map.html`
- **How to open HTML:** `open /tmp/concept-map.html` (macOS) or open in any browser

### Missing Expected Concepts
- Try regenerating (non-deterministic by design)
- Try a different focusing question
- Adjust concept count in `summarize.md`

### Map Doesn't Answer Focusing Question
- The updated prompts emphasize this
- Should include application concepts, limitations, distinctions
- Report as issue if consistently poor

## Project Structure

```
llmapper-skill/
├── SKILL.md                # Main skill definition (required by Claude Code)
├── extract-article.py      # Optional HTML text extractor
├── prompts/                # Pipeline stage prompts
│   ├── focusing-questions.md  # Stage 0: Generate perspectives
│   ├── summarize.md        # Stage 1: Extract concepts
│   ├── rdf.md              # Stage 2: Knowledge graph
│   ├── mermaid.md          # Stage 3: Mermaid visualization (default)
│   ├── cytoscape.md        # Stage 3: Cytoscape HTML (alternative)
│   └── dot.md              # Stage 3: Graphviz (reference)
├── CLAUDE.md               # Developer documentation
├── README.md               # This file
└── LICENSE                 # Project license
```

## Comparison to Original LLMapper

| Feature | Original (Bash) | Skill (Claude) |
|---------|----------------|----------------|
| Input | Wikipedia URLs | Files, URLs, pasted text |
| Dependencies | llm, Graphviz, ImageMagick | None (native Claude) |
| Platform | macOS/Linux | Claude Desktop + Claude Code + Web |
| Output | PNG file | Markdown with Mermaid or HTML |
| Focusing | Predefined | User chooses from 3 options |
| Visualization | Graphviz | Mermaid (default), Cytoscape.js (alternative) |
| Distinctions | Implicit | Explicit emphasis |
| Rendering | External file | Saved file (can paste for inline) |

## Future Enhancements

### High Priority
- [x] Mermaid visualization format (completed)
- [ ] Automatic fallback to file upload when WebFetch blocked
- [ ] User preference for output format (Mermaid, Cytoscape, Graphviz)
- [ ] Custom output directory option for files (instead of fixed `/tmp/` directory)

### Input Expansion
- [ ] Multiple articles → merged map
- [ ] YouTube transcript support
- [ ] Academic paper parsing (citations)

### Advanced Features
- [ ] Edit RDF and regenerate visualization
- [ ] Export to various formats (JSON, GraphML)
- [ ] Merge/compare multiple maps
- [ ] Confidence scores for relationships
- [ ] Temporal maps (show evolution over time)

## Known Limitations

1. **Mermaid layout constraints** - Mermaid automatic layout may not be optimal for very large graphs (20+ nodes)
2. **File must be viewed separately** - Output saved to `/tmp/concept-map.md`, requires separate viewer or paste action
3. **Wikipedia may block WebFetch** - use file upload instead
4. **Non-deterministic output** - different runs produce different maps (by design)
5. **Limited to ~15k chars** - very long articles may be truncated
6. **Session file persistence** - Output files overwritten on each run (feature for iterative refinement)

## Credits

Based on the original LLMapper bash tool by Jorge Arango.

Prompts developed through extensive iteration and testing.

Uses:
- "Panel of experts" prompt engineering pattern
- RDF as canonical knowledge representation
- Mermaid for inline visualization (default)
- Cytoscape.js for interactive HTML visualization (alternative)
- Distinction/contrast emphasis for deeper understanding

## Related Resources

- [Mermaid Documentation](https://mermaid.js.org/intro/)
- [Mermaid Flowchart Syntax](https://mermaid.js.org/syntax/flowchart.html)
- [Cytoscape.js Documentation](https://js.cytoscape.org/)
- [RDF Primer](https://www.w3.org/TR/rdf11-primer/)
- [Concept Mapping Theory](https://en.wikipedia.org/wiki/Concept_map)
- [Claude Desktop Skills](https://docs.claude.com/en/docs/claude-code/skills)

## License

[To be specified]

## Questions or Issues?

For issues with the skill, please open an issue in this repository.
