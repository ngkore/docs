# NgKore Documentation

NgKore is an open source community led by a group of passionate researchers, engineers, and professionals working to advance the future of 5G Advanced and 6G technologies. Our work spans a wide range of focus areas, including O-RAN, Non-Terrestrial Networks (NTN), AI/ML integration, Post-Quantum Cryptography adoption, blockchain integration, and cloud-native telecom infrastructure.

## Prerequisites

Before running the documentation locally, ensure you have the following installed on your system:

### System Requirements

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **git** (for cloning the repository)
- **make** (build automation tool)

### Install Prerequisites

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git make
```

On CentOS/RHEL/Fedora:

```bash
sudo yum install python3 python3-pip git make
# or for newer versions
sudo dnf install python3 python3-pip git make
```

On macOS:

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install prerequisites
brew install python3 git make
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ngkore/docs.git
cd docs/
```

### 2. Set Up Virtual Environment

The documentation uses a Python virtual environment to manage dependencies.

#### Option A: Using Make (Recommended)

```bash
make install
```

This command will:

- Create a Python virtual environment in `.sphinx/venv`
- Install all required dependencies from `.sphinx/requirements.txt`
- Display available make commands

#### Option B: Manual Virtual Environment Setup

If you prefer to set up the virtual environment manually:

```bash
# Create virtual environment
python3 -m venv .sphinx/venv

# Activate virtual environment
source .sphinx/venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r .sphinx/requirements.txt
```

#### Virtual Environment Management Commands

**Activate virtual environment:**

```bash
source .sphinx/venv/bin/activate
```

**Deactivate virtual environment:**

```bash
deactivate
```

**Remove virtual environment:**

```bash
# Remove virtual environment and build files
make clean

# Or manually remove
rm -rf .sphinx/venv
rm -rf _build
```

### 3. Build and Serve Documentation

#### Option A: Auto-rebuild and Serve (Recommended for Development)

To automatically build and serve the documentation with live reload:

```bash
make run
```

This will:

- Start a development server with auto-rebuild functionality
- Automatically refresh your browser when files change
- Serve the documentation at `http://localhost:8000`

#### Option B: Build Once

To build the documentation without serving:

```bash
make html
```

#### Option C: Serve Pre-built Documentation

If you have already built the documentation and want to serve it:

```bash
make serve
```

This serves the built documentation at `http://localhost:8000`

## Available Commands

The following make commands are available for managing the documentation:

| Command          | Description                                            |
| ---------------- | ------------------------------------------------------ |
| `make install`   | Set up virtual environment and install dependencies    |
| `make run`       | Build, watch, and serve documentation with auto-reload |
| `make html`      | Build documentation to HTML format                     |
| `make epub`      | Build documentation to EPUB format                     |
| `make serve`     | Serve pre-built documentation on localhost:8000        |
| `make clean`     | Remove build files and virtual environment             |
| `make clean-doc` | Remove only build files                                |
| `make spelling`  | Check spelling in documentation                        |
| `make linkcheck` | Validate all external links                            |
| `make woke`      | Check for inclusive language                           |

## Virtual Environment Commands

| Command                                   | Description                                |
| ----------------------------------------- | ------------------------------------------ |
| `source .sphinx/venv/bin/activate`        | Activate the virtual environment           |
| `deactivate`                              | Deactivate the current virtual environment |
| `python3 -m venv .sphinx/venv`            | Create virtual environment manually        |
| `pip install -r .sphinx/requirements.txt` | Install dependencies manually              |
| `rm -rf .sphinx/venv`                     | Remove virtual environment manually        |

## Documentation Framework

This documentation is built using:

- **Sphinx** - Documentation generator
- **MyST Parser** - Markdown support for Sphinx
- **Furo Theme** - Modern, responsive documentation theme
- **Sphinx Extensions** - Additional functionality including:
  - Auto-build with live reload
  - Copy button for code blocks
  - Design elements and tabs
  - Link checking and redirects

## Development Workflow

### Making Changes

1. Edit documentation files (`.md` or `.rst` format)
2. If using `make run`, changes will automatically rebuild and refresh your browser
3. If not using auto-reload, run `make html` to rebuild

### Adding New Pages

1. Create new `.md` files in the appropriate directory
2. Add references to new pages in `index.md` or relevant index files
3. Update the table of contents (`toctree`) as needed

### Quality Checks

Before committing changes, run the following checks:

```bash
# Check spelling
make spelling

# Validate links
make linkcheck

# Check inclusive language
make woke
```

## Troubleshooting

### Common Issues

1. **Python virtual environment issues**

   ```bash
   make clean
   make install
   ```

2. **Build failures**

   ```bash
   make clean-doc
   make html
   ```

3. **Port already in use (8000)**
   - Check if another process is using port `8000`
   - Kill the process or use a different port

### Build Warnings

Build warnings are logged to `.sphinx/warnings.txt` for review.

## Contributing

When contributing to the documentation:

1. Follow the existing file structure and naming conventions
2. Use clear, concise language
3. Include relevant examples and code snippets
4. Run quality checks before submitting
5. Ensure all links are valid and images are properly referenced

## Support

For any queries, feel free to raise an issue.

## Contributing

We welcome contributions from the community! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed information on:

- [Quick Start Guide](CONTRIBUTING.md#quick-start)
- [Before You Start](CONTRIBUTING.md#before-you-start)  
- [Development Workflow](CONTRIBUTING.md#development-workflow)
- [Quality Standards](CONTRIBUTING.md#quality-standards)
- [Pull Request Process](CONTRIBUTING.md#pull-request-process)

## Additional Resources

- **[Contributing Guidelines](CONTRIBUTING.md)** - Comprehensive contribution guide
- **[Code Owners](.github/CODEOWNERS)** - Repository maintainers and subject matter experts
- **[GitHub Issues](https://github.com/ngkore/docs/issues)** - Report bugs or request features
- **[Live Documentation](https://docs.ngkore.org)** - Published documentation site

## Support & Contact

For questions or support:
- **Email**: contact@ngkore.org
- **GitHub Issues**: [Create an issue](https://github.com/ngkore/docs/issues/new)
- **Website**: [ngkore.org](https://ngkore.org)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

Copyright 2024 NgKore Community

## Acknowledgments

This documentation is maintained by the NgKore Community with contributions from researchers, engineers, and professionals advancing 5G Advanced and 6G technologies.
