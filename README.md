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

### Claude Desktop (Recommended)

1. Download `llmapper.zip` from this repository
2. Open Claude Desktop
3. Go to **Settings → Capabilities → Skills**
4. Click **"Upload skill"**
5. Select `llmapper.zip`

### Claude Code

Copy the skill to your Claude Code skills directory:

```bash
cp llmapper.claud ~/.claude/skills/
```

Or create a symlink:

```bash
ln -s /path/to/llmapper-skill/llmapper.claud ~/.claude/skills/llmapper.claud
```

## Usage

### Invoke the Skill

**Option 1: Explicit command**
```
/llmapper
```

**Option 2: Natural language** (Claude Desktop will auto-detect)
```
Create a concept map from this article
Generate a knowledge graph of [topic]
Visualize the relationships in this paper
```

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
4. **View map** - Interactive Cytoscape visualization
5. **Refine** - Regenerate with different focus or try again

## Example Output

The skill produces interactive HTML visualizations with:
- **Nodes**: Purple rounded boxes containing concepts
- **Edges**: Labeled arrows showing relationships
- **Interactivity**: Drag nodes, zoom, pan (when opened in browser)

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
Stage 3: Cytoscape Visualization (interactive HTML)
    ↓
Concept Map Output
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

### Claude Desktop Limitation

**Known issue:** Cytoscape HTML does not render as a Claude Desktop artifact (requires external CDN which doesn't load in artifacts).

**Workaround:** Save the HTML file and open in your browser for full interactivity.

**Future solution:** We're exploring pure SVG output that would work inline in Claude Desktop.

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

### Diagram Doesn't Display (Claude Desktop)
- **Expected:** Cytoscape HTML doesn't work as artifact
- **Solution:** Save HTML and open in browser

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
├── llmapper.claud          # Main skill definition
├── extract-article.py      # Optional HTML text extractor
├── prompts/                # Pipeline stage prompts
│   ├── focusing-questions.md  # Stage 0: Generate perspectives
│   ├── summarize.md        # Stage 1: Extract concepts
│   ├── rdf.md              # Stage 2: Knowledge graph
│   ├── cytoscape.md        # Stage 3: Visualization (active)
│   └── dot.md              # Stage 3: Graphviz (reference)
├── CLAUDE.md               # Documentation for Claude Code
└── README.md               # This file
```

## Comparison to Original LLMapper

| Feature | Original (Bash) | Skill (Claude) |
|---------|----------------|----------------|
| Input | Wikipedia URLs | Files, URLs, pasted text |
| Dependencies | llm, Graphviz, ImageMagick | None (native Claude) |
| Platform | macOS/Linux | Claude Desktop + Claude Code |
| Output | PNG file | Interactive HTML |
| Focusing | Predefined | User chooses from 3 options |
| Visualization | Graphviz | Cytoscape.js |
| Distinctions | Implicit | Explicit emphasis |

## Future Enhancements

### High Priority
- [ ] Pure SVG output (works as Claude Desktop artifact)
- [ ] Automatic fallback to file upload when WebFetch blocked
- [ ] Format selection (Cytoscape vs. SVG)

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

1. **Cytoscape doesn't work as Claude Desktop artifact** - requires browser
2. **Wikipedia may block WebFetch** - use file upload instead
3. **Non-deterministic output** - different runs produce different maps (by design)
4. **Limited to ~15k chars** - very long articles may be truncated
5. **No external dependencies** - can't use Graphviz directly

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
