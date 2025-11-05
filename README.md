# LLMapper Skill

A Claude Code skill that generates concept maps from Wikipedia articles using a multi-stage LLM pipeline.

## Overview

LLMapper transforms Wikipedia articles into visual knowledge graphs through three stages:
1. **Summarization** - Extract key concepts and relationships
2. **RDF Generation** - Structure as knowledge graph
3. **Graphviz Rendering** - Visualize as concept map

## Origin

This skill is based on the original [LLMapper bash tool](https://github.com/yourusername/llmapper) (link TBD), which uses external tools (llm CLI, Graphviz, ImageMagick). This skill replicates that pipeline using Claude's native capabilities, with no external dependencies required.

## Installation

### Claude Code

Copy the skill to your Claude Code skills directory:

```bash
cp llmapper.claud ~/.config/claude/skills/
```

Or create a symlink to keep it in sync:

```bash
ln -s /path/to/llmapper-skill/llmapper.claud ~/.config/claude/skills/llmapper.claud
```

### Verify Installation

In Claude Code, type `/skills` to see available skills. You should see `llmapper` in the list.

## Usage

### Basic Usage

Simply provide a Wikipedia URL:

```
/llmapper https://en.wikipedia.org/wiki/The_Lord_of_the_Rings
```

Or invoke the skill and then provide the URL:

```
User: Use the llmapper skill
Claude: I'll help you create a concept map. Please provide a Wikipedia URL.
User: https://en.wikipedia.org/wiki/Artificial_Intelligence
```

### What to Expect

1. **Summary Output** - You'll first see extracted concepts and relationships
2. **Concept Map** - A rendered Graphviz diagram showing the knowledge graph
3. **Refinement Options** - Suggestions for regenerating with different focus

### Example Output

The skill produces diagrams like this:

```
[Rendered concept map with nodes and labeled edges]
```

- Nodes: Purple rounded boxes containing concepts
- Edges: Arrows with verb labels showing relationships
- Layout: Automatically optimized by Graphviz

## How It Works

### Multi-Stage Pipeline

```
Wikipedia URL
    ↓
WebFetch (retrieve article)
    ↓
Summarization Prompt (concepts + relationships)
    ↓
RDF Generation Prompt (knowledge graph structure)
    ↓
DOT Generation Prompt (visualization syntax)
    ↓
Rendered Concept Map
```

### Prompt Engineering

The skill uses three carefully crafted prompts located in `prompts/`:

1. **`summarize.md`** - "Panel of experts" approach with three personas
2. **`rdf.md`** - Converts to RDF triples with strict formatting rules
3. **`dot.md`** - Transforms RDF to Graphviz DOT with extensive layout rules

These prompts contain detailed rules developed through iteration to prevent common LLM failure modes (e.g., compound subjects, self-referential nodes, camelCase labels).

### Key Design Principles

- **Focus on "why it matters"** - Maps emphasize significance, not just facts
- **Dynamic focusing questions** - Explores relevance to humanity
- **Non-deterministic** - Each run produces different (valid) results
- **Comprehensive rules** - Extensive constraints ensure valid output

## Customization

### Modifying Prompts

You can adjust the prompts in `prompts/` to change behavior:

- **More/fewer concepts**: Edit the "10 MOST IMPORTANT" line in `summarize.md`
- **Different focus**: Modify the focusing question guidance
- **Visual style**: Edit the DOT template in `dot.md`
- **Relationship density**: Adjust the "no fewer than 20" rule in `summarize.md`

After modifying prompts, restart Claude Code or reload the skill.

### Adding Alternative Output Formats

The current skill outputs Graphviz DOT. To support other formats:

1. Add a new prompt file (e.g., `prompts/mermaid.md` or `prompts/json.md`)
2. Update the skill's stage 3 to support format selection
3. Modify the skill instructions to offer format options

See the [Future Enhancements](#future-enhancements) section below.

## Troubleshooting

### Diagram doesn't render
- Ensure you're using Claude Code (not Claude Desktop)
- Check that the DOT output has no markdown code blocks
- Verify the DOT syntax is valid (no unclosed quotes, proper structure)

### Missing concepts
- Try regenerating - results vary each time
- The skill limits to top 10 concepts by design
- Modify `summarize.md` to extract more concepts

### Cluttered diagram
- Complex articles produce complex graphs
- Try a more focused Wikipedia article
- Reduce relationship count in `summarize.md`

### Wrong concepts extracted
- The skill only uses information in the article
- Wikipedia articles vary in quality and completeness
- Try summarizing a different article about the same topic

## Comparison to Original LLMapper

| Feature | Original (Bash) | Skill (Claude Code) |
|---------|----------------|---------------------|
| Dependencies | llm, strip-tags, ttok, Graphviz, ImageMagick | None (native Claude) |
| Platform | macOS/Linux with tools installed | Any platform with Claude Code |
| Output | PNG file saved to disk | Rendered in Claude interface |
| Iteration | Re-run entire script | Interactive refinement |
| Portability | Requires setup | Works anywhere |
| Speed | Fast (parallel external tools) | Moderate (sequential LLM calls) |
| Cost | API calls to OpenAI/Anthropic | Included in Claude subscription |

## Future Enhancements

Potential improvements for future versions:

### Multi-Format Support
- [ ] Mermaid diagram output (works in Claude Desktop too)
- [ ] React/Cytoscape.js for interactive maps
- [ ] JSON output for custom visualization
- [ ] Export to PNG/SVG

### Input Flexibility
- [ ] Support any URL (not just Wikipedia)
- [ ] Accept pasted text content
- [ ] Process PDF documents
- [ ] Multiple articles → combined map

### Advanced Features
- [ ] Focus controls (emphasize specific aspects)
- [ ] Concept count slider (5-20 concepts)
- [ ] Visual theme options
- [ ] Export/import RDF for editing
- [ ] Compare multiple articles side-by-side

### Quality Improvements
- [ ] Validation step between stages
- [ ] Automatic retry on malformed output
- [ ] Confidence scores for relationships
- [ ] Citation tracking (which facts from which sections)

## Project Structure

```
llmapper-skill/
├── llmapper.claud          # Main skill definition
├── prompts/                # Pipeline stage prompts
│   ├── summarize.md        # Stage 1: Extract concepts
│   ├── rdf.md              # Stage 2: Generate knowledge graph
│   └── dot.md              # Stage 3: Create visualization
└── README.md               # This file
```

## Contributing

This skill is based on an experimental research project. Contributions welcome:

- Prompt improvements (better concept extraction, cleaner output)
- Alternative output formats (Mermaid, D3.js, etc.)
- Support for non-Wikipedia sources
- Better error handling and validation

## License

[Same as original LLMapper project - specify when known]

## Credits

Based on the original LLMapper bash tool by [Your Name].

Prompts developed through extensive iteration and testing with GPT-4 and Claude.

Uses the "panel of experts" prompt engineering pattern for improved concept extraction.

## Related Resources

- [Original LLMapper Repository](#) (link TBD)
- [Graphviz Documentation](https://graphviz.org/)
- [RDF Primer](https://www.w3.org/TR/rdf11-primer/)
- [Concept Mapping Theory](https://en.wikipedia.org/wiki/Concept_map)
- [Claude Code Skills Documentation](https://docs.claude.com/claude-code)

## Questions or Issues?

For issues specific to this skill, please [open an issue](#) (link TBD).

For questions about the original LLMapper project, see the [main repository](#) (link TBD).
