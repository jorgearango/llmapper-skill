# LLMapper Skill

A Claude skill that generates concept maps from articles using a multi-stage LLM pipeline. Works with **file uploads** (PDFs, text files), **URLs**, and **pasted text**.

## Overview

LLMapper transforms articles into interactive visual knowledge graphs that answer two key questions:
1. **What is this subject about?**
2. **Why does this subject matter?**

The skill processes content through four stages:
1. **Focusing Questions** - Generate 3 perspectives, user chooses one
2. **Summarization** - Extract key concepts and relationships (with emphasis on distinctions and contrasts)
3. **RDF Generation** - Structure as knowledge graph
4. **Cytoscape Rendering** - Interactive HTML visualization

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
4. **Get visualization** - HTML file saved to `/tmp/concept-map.html`
5. **Open in browser** - View interactive concept map with full interactivity
6. **Refine** - Regenerate with different focus or try again

## Example Output

The skill produces interactive HTML visualizations saved to `/tmp/concept-map.html`:
- **Nodes**: Purple rounded boxes containing concepts
- **Edges**: Labeled arrows showing relationships
- **Interactivity**: Drag nodes, zoom, pan
- **Usage**: Open the file in any web browser for full interactivity

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
Stage 3: Cytoscape Visualization (saved to /tmp/concept-map.html)
    ↓
Open in browser for full interactivity
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

The skill uses four carefully engineered prompts in `prompts/`:

1. **`focusing-questions.md`** - Generates 3 dynamic perspectives
2. **`summarize.md`** - "Panel of experts" with distinction/contrast emphasis
3. **`rdf.md`** - Converts to RDF triples with strict rules
4. **`cytoscape.md`** - Transforms to interactive HTML visualization

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

**File location:** The visualization is saved to `/tmp/concept-map.html`

**How to use:** Open the file in any web browser (Chrome, Firefox, Safari, etc.) for full interactivity.

**Session-persistent:** The file has a fixed name, so it will be overwritten if you generate a new map in the same session. This allows for iterative refinement.

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

Edit `prompts/cytoscape.md` to change:
- Node colors: `'background-color': '#EDEEFA'`
- Border colors: `'border-color': '#9B8FD9'`
- Layout algorithm: `name: 'cose'` (try 'dagre', 'circle', etc.)

### Alternative Visualizations

The skill includes `prompts/dot.md` (Graphviz DOT) preserved for reference. You could add:
- Mermaid diagrams
- D3.js visualizations
- SVG output for Claude Desktop artifacts

## Troubleshooting

### WebFetch Returns Summary Instead of Full Text
- **Solution:** Use file upload instead
- The skill validates WebFetch output and will notify you

### Can't Find the Visualization
- **Location:** Check `/tmp/concept-map.html`
- **How to open:** `open /tmp/concept-map.html` (macOS) or open in any browser

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
│   ├── cytoscape.md        # Stage 3: Visualization (active)
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
| Platform | macOS/Linux | Claude Desktop + Claude Code |
| Output | PNG file | Interactive HTML (saved to `/tmp/concept-map.html`) |
| Focusing | Predefined | User chooses from 3 options |
| Visualization | Graphviz | Cytoscape.js |
| Distinctions | Implicit | Explicit emphasis |

## Future Enhancements

### High Priority
- [ ] Automatic fallback to file upload when WebFetch blocked
- [ ] Multiple output format options (Cytoscape, Graphviz, Mermaid, etc.)
- [ ] Custom output directory option (instead of fixed `/tmp/llmapper.html`)

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

1. **File must be opened in browser** - output saved to `/tmp/concept-map.html`, not rendered inline
2. **Wikipedia may block WebFetch** - use file upload instead
3. **Non-deterministic output** - different runs produce different maps (by design)
4. **Limited to ~15k chars** - very long articles may be truncated
5. **Session file persistence** - `/tmp/concept-map.html` overwritten on each run (feature for iterative refinement)

## Credits

Based on the original LLMapper bash tool by Jorge Arango.

Prompts developed through extensive iteration and testing.

Uses:
- "Panel of experts" prompt engineering pattern
- RDF as canonical knowledge representation
- Cytoscape.js for interactive visualization
- Distinction/contrast emphasis for deeper understanding

## Related Resources

- [Cytoscape.js Documentation](https://js.cytoscape.org/)
- [RDF Primer](https://www.w3.org/TR/rdf11-primer/)
- [Concept Mapping Theory](https://en.wikipedia.org/wiki/Concept_map)
- [Claude Desktop Skills](https://docs.claude.com/en/docs/claude-code/skills)

## License

[To be specified]

## Questions or Issues?

For issues with the skill, please open an issue in this repository.
