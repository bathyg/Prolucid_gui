# ProLuCID GUI Python 3 update

This folder contains a clean Python 3 rewrite of the legacy `Prolucid_gui` project. Functions stay the same.

The rewrite keeps the same workflow:

1. Choose a FASTA database.
2. Choose one or more `.ms2` files.
3. Generate `search.xml`.
4. Run ProLuCID.
5. Run DTASelect on the `.sqt` outputs.

This version does not embed `ProLuCID1_3.jar` or DTASelect binaries inside Python source code. You provide the paths explicitly, which makes the project easier to inspect and maintain.

## Project Layout

```text
prolucid_gui_github/
  docs/
  examples/
  src/
    prolucid_gui/
  pyproject.toml
```

## Requirements

- Python 3.10+
- Java available on the command line, or a direct path to `java`
- `ProLuCID1_3.jar`
- DTASelect classpath or extracted folder

## Quick Start

Install in editable mode from this folder:

```bash
pip install -e .
```

Run the GUI:

```bash
python -m prolucid_gui gui
```

Run the CLI help:

```bash
python -m prolucid_gui --help
```

## Documentation

- [Command line usage](./docs/command_line.md)
- [GUI functions](./docs/gui_functions.md)
