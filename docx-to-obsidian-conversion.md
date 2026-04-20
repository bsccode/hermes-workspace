# DOCX to Obsidian Markdown Conversion

## Overview
Procedure for converting Word (.docx) files to clean Obsidian-compatible Markdown, preserving formatting while cleaning up Word artifacts.

## Prerequisites
- **pandoc** — the core conversion engine
- **Homebrew** (macOS) or equivalent package manager

## Step 1: Install pandoc
```bash
brew install pandoc
```

## Step 2: Convert with pandoc
```bash
pandoc "input.docx" -f docx -t markdown -o "output.md" --wrap=preserve --standalone
```

| Flag | Purpose |
|------|---------|
| `-f docx` | Input format: Word .docx |
| `-t markdown` | Output format: Markdown |
| `--wrap=preserve` | Preserve existing line wrapping |
| `--standalone` | Include metadata block (useful for frontmatter) |

## Step 3: Clean Word Artifacts
pandoc outputs several Word-specific artifacts that need removal:

### 3.1: Remove TOC Section
Word generates a Table of Contents with anchor links (`#_Toc\d+`). Delete the entire INDEX/TOC block — the heading structure already provides navigation in Obsidian.

### 3.2: Remove Anchor Artifacts
Pattern: `[]{#_Toc\d+ .anchor}` and `{#table-of-contents .TOC-Heading}`

These are Word internal link anchors. They serve no purpose in Markdown.

### 3.3: Unescape Brackets
pandoc escapes all brackets: `\[\[YEAR\]\]` → `[YEAR]`

Case citations like `[1893] 1 QB 256` should be plain brackets. Obsidian doesn't conflict with these since they're not wiki-link syntax.

```python
content = content.replace('\\[', '[').replace('\\]', ']')
```

### 3.4: Remove Dollar Sign Escapes
pandoc escapes `$` as `\$` for money amounts. Clean:

```python
content = content.replace('\\$', '$')
```

### 3.5: Remove Backslash-Newlines
pandoc uses `\n` (backslash + letter n) to represent wrapped content. Replace with space:

```python
content = content.replace('\\n', ' ')
```

### 3.6: Clean Other Escape Sequences
```python
content = content.replace('\\.', '.')
content = content.replace('\\*', '*')
content = content.replace('\\>', '>')
content = content.replace('\\\\', '\\')
```

### 3.7: Remove Orphaned Section Breaks
Word section breaks (`**\`) become orphaned `**` lines. Delete any line that is exactly `**`.

### 3.8: Remove Excessive Blank Lines
Collapse 3+ consecutive blank lines into 2.

## Step 4: Verify
Check the output for:
- **Headings** — should be clean `#`, `##`, `###`
- **Case citations** — should look like `*Case Name* [YEAR]`
- **Lists** — properly indented with `-` or `*`
- **No remaining backslashes** — run `content.count('\\')` should be 0

## What Transfers Well
- Headings (all levels)
- Bold, italic, underline, strikethrough
- Bullet and numbered lists
- Tables (pandoc handles these natively)
- Images
- Links and references
- Code blocks
- Footnotes
- Headers and footers

## What May Be Lost
- SmartArt diagrams
- Custom Word styles
- Text effects (shadows, 3D text)
- Shapes and text boxes
- Complex formatting
- Embedded objects (Excel charts)
- Page breaks (become `---` horizontal rules)

## Example Output Structure
```markdown
**Document Title**

## Section Heading

**Definition**: Some definition text with *italic* and **bold**.

- **Question X.X**: The question text.
  - **Yes** → Proceed to next step.
  - **No** → Stop.

**Key Cases**:

- *Case Name* [YEAR] Page: Brief description.

**IRAC Skeleton**:
- **Issue**: What is the issue?
- **Rule**: The applicable rule.
- **Application**: Apply the rule.
- **Conclusion**: Conclusion.
```

## Tips
- **Test on one file first** before batch converting
- **Obsidian plugins**: The "Pandoc" plugin can also do this from within Obsidian
- **For large documents**: Consider splitting into multiple files by section
- **Wiki-links**: Manually add `[[Case Name]]` for case citations you want to link to note pages
