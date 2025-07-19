# Contributing to NgKore Documentation

We welcome and encourage contributions to the NgKore documentation! This guide will help you get started with contributing to our community-driven documentation project.

## Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/docs.git
   cd docs
   ```
3. **Set up the development environment** (see [README.md](README.md))
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Before You Start

**Please discuss your topic** before submitting content to ensure it aligns with our documentation goals:

- **Create a GitHub issue** describing your proposed topic
- **Our team will review** and provide guidance on the content approach
- **This helps avoid** duplicate content and ensures community value

## Development Workflow

### Setting Up Local Environment

Follow the detailed setup instructions in [README.md](README.md#getting-started), including:
- Prerequisites installation
- Virtual environment setup  
- Building and serving documentation locally

### Making Changes

1. **Edit documentation files** (`.md` or `.rst` format)
2. **Use live reload** with `make run` for immediate feedback
3. **Test your changes** locally before submitting

### Adding New Content

1. **Create new `.md` files** in the appropriate directory
2. **Follow existing structure** and naming conventions
3. **Update table of contents** (`toctree`) as needed
4. **Add references** in `index.md` or relevant index files

## Quality Standards

### Before Submitting

Run these quality checks:

```bash
# Check spelling
make spelling

# Validate external links  
make linkcheck

# Check inclusive language
make woke

# Build documentation
make html
```

### Content Guidelines

- **Use clear, concise language**
- **Include relevant examples and code snippets**
- **Ensure all links are valid**
- **Reference images properly**
- **Follow existing file structure and naming conventions**

### Code Style

- **Python code**: Follow PEP 8 standards
- **Markdown**: Use consistent formatting
- **File naming**: Use lowercase with hyphens (`my-new-doc.md`)

## Repository Structure

```
docs/
├── 5g-core/          # 5G core network documentation
├── ebpf/             # eBPF technology guides
├── security/         # Network security topics
├── pqc/              # Post-quantum cryptography
├── oran/             # O-RAN specifications
├── ntn/              # Non-terrestrial networks
├── ai-ml/            # AI/ML integration
├── kernel-bypass/    # Kernel bypass technologies
├── l3af/             # L3AF orchestration
├── .github/          # GitHub workflows and templates
├── _static/          # Static assets (CSS, JS, images)
└── _templates/       # Sphinx templates
```

## Pull Request Process

### 1. Prepare Your Contribution
- Ensure your branch is up to date with `main`
- Run all quality checks
- Test documentation builds successfully

### 2. Submit Pull Request
- **Use a descriptive title**
- **Fill out the PR template** completely
- **Add appropriate labels** 
- **Request review** from relevant code owners

### 3. Review Process
- **Maintainers will review** your contribution
- **Address feedback** promptly and professionally
- **Make requested changes** in additional commits

### 4. Merge Requirements
- All CI/CD checks must pass
- At least one maintainer approval required
- All review comments resolved
- Documentation builds successfully

## Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- **Be respectful** and professional in all interactions
- **Be supportive** of other contributors
- **Be open** to constructive feedback
- **Focus on** what's best for the community

### Communication Channels

- **GitHub Issues**: Technical discussions and bug reports
- **Pull Requests**: Code review and collaboration  
- **Email**: contact@ngkore.org for general inquiries

## Contribution Types

We welcome various types of contributions:

### Documentation
- **New guides** and tutorials
- **Improvements** to existing content
- **Translation** efforts
- **Accessibility** enhancements

### Technical
- **Bug fixes** in documentation tooling
- **New features** for the documentation site
- **Performance improvements**
- **CI/CD enhancements**

### Design
- **UI/UX improvements**
- **Visual design** enhancements
- **Accessibility** improvements
- **Mobile responsiveness**

## Getting Help

Need assistance? We're here to help!

- **Email**: contact@ngkore.org
- **GitHub Issues**: For technical questions
- **Discussions**: For general questions and ideas

## License

By contributing to NgKore documentation, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).

## Recognition

We value all contributions and maintain a record of contributors. Significant contributors may be invited to join the NgKore maintainers team.

---

**Thank you for contributing to NgKore!**

Your contributions help advance 5G Advanced and 6G technologies for the entire community.