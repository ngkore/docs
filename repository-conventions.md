# Repository Conventions

This document defines the standard conventions for writing and organizing Markdown content in this repository.

## File Naming

- File names must be written in **lowercase**.
- Use **dash (-)** to separate words.
- Exclude common or filler words such as `a`, `the`, `is`, etc.
- File names should directly reflect the content title.
- Examples:
  - Title: `The Future of Quantum Security` → `future-of-quantum-security.md`
  - Title: `OAI RAN Deployment` → `oai-ran.md`

## Directory Structure

- Each main section (e.g., `ai-ml`, `pqc`, `ebpf`, `tutorials`) has:
  - Its own `index.md` with a `toctree` directive
  - An `images/` directory for images used in that section
- Each subsection has:
  - Its own subdirectory
  - Its own `index.md`
  - Images in the parent `images/` directory under a subdirectory
- Do not mix images across sections or subsections.
- If content belongs to a series or category, place it under a dedicated subdirectory.

### Example Structure

```
section-name/
├── index.md
├── file-1.md
├── file-2.md
├── images/
│   ├── image-1.png
│   └── image-2.png
└── subsection/
    ├── index.md
    ├── file-1.md
    └── images/
        └── image-1.png
```

## Metadata Format

Every Markdown file should include standardized metadata at the top:

```markdown
# Document Title

**Author:** [Author Name](https://linkedin.com/in/username/)

**Published:** Month Day, Year

Brief introduction or description of the content.
```

For multiple authors:

```markdown
**Author:** [Name 1](link), [Name 2](link) & [Name 3](link)
```

## Repository Links

When referencing code repositories, implementation guides, or related projects, include them in a note block at the beginning of the document:

```markdown
> **Note:**
> Follow this repository ([github/username/repo-name](https://github.com/username/repo-name)) for implementation details.
```

## Formatting and Style

### General Guidelines

- Use Prettier for consistent Markdown formatting.
- Avoid unnecessary emoji or icons.
- Keep language concise and technical.
- Use code blocks for directory structures, code samples, or examples.
- Do not use bold styling for headings.
- Do not use em dash (`—`).

### Header Hierarchy

Headers must follow consecutive levels - no jumps allowed:

**Correct:**

```markdown
# Main Title (H1)

## Section (H2)

### Subsection (H3)

#### Detail (H4)
```

**Incorrect:**

```markdown
# Main Title (H1)

### Subsection (H3) ← Skipped H2, will cause Sphinx warning
```

**Rules:**

- `#` (H1) for document title - use once at the top
- `##` (H2) for main sections
- `###` (H3) for subsections
- `####` (H4) for detailed points
- Never jump levels (H2 to H4 or H1 to H3)

### Code Blocks

Use appropriate language identifiers for syntax highlighting:

````text
```python
# Python code
```

```javascript
// JavaScript code
```

```yaml
# YAML configuration
```

```json
# JSON data
```

```groovy
// Gradle build files
```

```bash
# Shell commands/scripts
```

```console
# Terminal output with commands
```

```diff
# Patch/diff files
```

```c
# C code
```

```cpp
// C++ code
```
````

**Important distinctions:**

- Use `console` for terminal output that includes commands and their output
- Use `bash` for shell scripts or commands only
- Use `groovy` for Gradle build files (not `gradle`)
- Use `diff` for patch files (not `patch`)

**Examples:**

Terminal output:

```console
ubuntu@server:~$ kubectl get pods
NAME                      READY   STATUS    RESTARTS   AGE
nginx-6d4cf56db6-xyz      1/1     Running   0          2d
```

Shell script:

```bash
#!/bin/bash
make clean
make all
```

Configuration file:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
```

### Horizontal Lines

Do not use horizontal lines (`---`) in Markdown files. They can cause rendering issues in Sphinx documentation.

<br>

**Incorrect:**

```markdown
## Section 1

---

## Section 2
```

**Correct:**

```markdown
## Section 1

Content here.

## Section 2
```

## Git Commits and Sign-off

All commits must include a Developer Certificate of Origin (DCO) sign-off to certify that you have the right to submit the code under the project's license.

### Adding Sign-off

Add the `-s` or `--signoff` flag when creating commits:

```bash
git commit -s -m "Add new feature"
```

This automatically adds a `Signed-off-by` line with your name and email:

```text
Signed-off-by: Your Name <your.email@example.com>
```

### Commit Message Format

- Use clear, descriptive commit messages
- Start with a verb in imperative mood (add, fix, update, remove)
- Keep the subject line under 72 characters
- Add details in the commit body if needed

**Example:**

```text
Add PQC implementation guide

This commit adds a comprehensive guide for implementing
post-quantum cryptography in 5G core networks.

Signed-off-by: Your Name <your.email@example.com>
```

## Index Files and Navigation

When adding new Markdown files:

1. Add to the respective `index.md` file:

   ````markdown
   ```{toctree}
   :maxdepth: 2

   new-file-name
   ```
   ````

2. Maintain logical order by publication date, category, or logical flow

3. Use appropriate maxdepth:
   - `:maxdepth: 1` for flat lists
   - `:maxdepth: 2` for hierarchical navigation

## Image Organization

### Naming Conventions

- Use lowercase with dashes: `image-name.png`
- Be descriptive: `oai-ran-deployment-flow.png` not `diagram1.png`
- Include category/section prefix: `section-topic-description.png`

### Supported Formats

- Diagrams/Screenshots: `.png` (preferred), `.jpg`
- Architecture diagrams: `.png`, `.svg`
- Web images: `.webp` (for optimization)

### Image References

Always use relative paths from the document location:

```markdown
![description](../images/category/image-name.png)
```
