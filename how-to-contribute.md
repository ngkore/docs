# How to Contribute

We welcome and encourage contributions to the NgKore documentation! This guide will help you get started with contributing to our community-driven documentation project.

## Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/docs.git
   cd docs
   ```
3. **Set up the development environment** (see below)
4. **Create a topic branch**:
   ```bash
   git checkout -b topic/your-topic-name
   ```

## Development Setup

### Prerequisites

Before running the documentation locally, ensure you have the following installed:

#### System Requirements

- Python 3.8 or higher
- pip
- git
- make

#### Install Prerequisites

**On Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git make
```

**On CentOS/RHEL/Fedora:**

```bash
sudo yum install python3 python3-pip git make
# or for newer versions
sudo dnf install python3 python3-pip git make
```

**On macOS:**

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install prerequisites
brew install python3 git make
```

### Virtual Environment Setup

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

### Virtual Environment Management

| Command                                   | Description                                |
| ----------------------------------------- | ------------------------------------------ |
| `source .sphinx/venv/bin/activate`        | Activate the virtual environment           |
| `deactivate`                              | Deactivate the current virtual environment |
| `python3 -m venv .sphinx/venv`            | Create virtual environment manually        |
| `pip install -r .sphinx/requirements.txt` | Install dependencies manually              |
| `make clean`                              | Remove build files and virtual environment |
| `rm -rf .sphinx/venv _build`              | Remove virtual environment manually        |

## Building and Serving Documentation

### Option A: Auto-rebuild and Serve (Recommended)

To automatically build and serve the documentation with live reload:

```bash
make run
```

This will:

- Start a development server with auto-rebuild functionality
- Automatically refresh your browser when files change
- Serve the documentation at `http://localhost:8000`

### Option B: Build & Serve

To build the documentation and serve it:

```bash
# Build the documentation to HTML format
make html

# Serve the built documentation
make serve
```

This build the documentation and serve it at `http://localhost:8000`

### Available Commands

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

## Development Workflow

### Making Changes

1. Edit documentation files (`.md` format)
2. If using `make run`, changes will automatically rebuild and refresh your browser
3. If not using auto-reload, run `make html` to rebuild

### Adding New Pages

1. Create new `.md` files in the appropriate directory
2. Add references to new pages in `index.md` or relevant index files
3. Update the table of contents (`toctree`) as needed

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
   - Check if another process is using port `8000` (`lsof -i :8000`)
   - Kill the process (`kill -9 <PID>`) or use a different port

### Build Warnings

Build warnings are logged to `.sphinx/warnings.txt` for review.

## License

By contributing to NgKore documentation, you agree that your contributions will be licensed under the [Apache License 2.0](https://github.com/ngkore/docs/blob/main/LICENSE).

## Recognition

We value all contributions and maintain a record of contributors. Significant contributors may be invited to join the NgKore maintainers team.

---

**Thank you for contributing to NgKore!**
