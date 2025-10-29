# Repository Conventions

This document defines the standard conventions for writing and organizing Markdown content, blog posts, and related assets in this repository.

## File Naming

- File names must be written in **lowercase**.
- Use **dash (-)** to separate words.
- Exclude **common or filler words** such as `a`, `the`, `is`, etc.
- File names should directly reflect the **blog title** (excluding the above common words).
- Example:
  - Blog title: `The Future of Quantum Security`
  - File name: `future-of-quantum-security.md`

## Rules

- Each **main section** (e.g., `ai-ml`) has:
  - Its own `index.md`
  - An `images/` directory for images used in that section
- Each **subsection** (e.g., `devops` under `ai-ml`) has:
  - Its own subdirectory
  - An `images/` folder inside it
- Do not mix images across sections or subsections.
- If a blog belongs to a **series**, place it under a dedicated subdirectory.
- Whenever a new Markdown file is added:
  - Add its filename (without `.md` extension) in the respective `index.md` file.
  - Maintain order by publication or logical grouping.

### Example

**Series:** Devops under AI-ML

```
ai-ml/
├── index.md
├── file-1.md
├── file-2.md
├── images/
│   ├── image-1.png
│   └── image-2.png
├── devops/
│   ├── index.md
│   ├── file-1.md
│   ├── file-2.md
│   └── images/
│       ├── image-1.png
│       └── image-2.png
```

## Formatting and Style

- Use **Prettier** for consistent Markdown formatting.
- Avoid unnecessary emoji or icons.
- Keep language concise and technical.
- Use code blocks (` ``` `) for directory structures, code samples, or examples.
- Headings should be simple and consistent:
  - `#` for main section
  - `##` for subsections
  - `###` for details within subsections
- **Do not use bold styling for headings.** Headings should remain plain text for clean rendering and readability.
