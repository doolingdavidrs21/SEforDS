# Software Engineering for Data Scientists

This is the code repository that accompanies the book "Software Engineering for Data Scientists" by Catherine Nelson, published by O'Reilly Media.

## Setup Instructions

This project uses [uv](https://docs.astral.sh/uv/) for fast, reliable Python package management.

### Prerequisites

- Python 3.12 or higher
- uv package manager

### Installing uv

If you don't have uv installed, install it using one of these methods:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Using pip:**
```bash
pip install uv
```

### Setting up the Virtual Environment

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd SEforDS
   ```

2. **Create and activate the virtual environment with all dependencies**:
   ```bash
   uv sync
   ```

   This command will:
   - Create a `.venv` directory in your project root
   - Install Python 3.12 if needed
   - Install all dependencies from `pyproject.toml` and `uv.lock`

3. **Activate the virtual environment**:

   **macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

   **Windows:**
   ```powershell
   .venv\Scripts\activate
   ```

4. **Verify the installation**:
   ```bash
   python --version
   python main.py
   ```

### Alternative: Using uv run

You can also run Python commands directly without explicitly activating the virtual environment:

```bash
uv run python main.py
uv run jupyter notebook
```

### Managing Dependencies

- **Add a new package**: `uv add <package-name>`
- **Remove a package**: `uv remove <package-name>`
- **Update dependencies**: `uv sync`

## Dependencies

This project requires Python 3.12 or higher. All package dependencies are managed in `pyproject.toml` and locked in `uv.lock` for reproducible builds.