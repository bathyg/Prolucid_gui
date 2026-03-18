# Prolucid GUI

Legacy ProLuCID GUI by Yu (Tom) Gao, with a newer Python 3 rewrite kept in this folder.

This repository contains two related parts:

- The original desktop workflow and example assets used by the legacy project.
- A Python 3 rewrite of the GUI and command-line workflow under `src/prolucid_gui/`.

Both versions follow the same overall process:

1. Choose a FASTA database.
2. Choose one or more `.ms2` files.
3. Generate `search.xml`.
4. Run ProLuCID.
5. Run DTASelect on the resulting `.sqt` files.

## Folder Layout

```text
src/
|-- docs/
|-- examples/
|-- pyproject.toml
|-- README.md
`-- src/
    `-- prolucid_gui/
```

## Python 3 Rewrite

The rewrite keeps the ProLuCID workflow but avoids embedding `ProLuCID1_3.jar` and DTASelect binaries in Python source code. Tool paths are supplied explicitly, which makes the project easier to inspect and maintain.

### Requirements

- Python 3.10+
- Java available on the command line, or a direct path to `java`
- `ProLuCID1_3.jar`
- DTASelect classpath or extracted folder

### Quick Start

Install from this folder:

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

Documentation:

- [`docs/command_line.md`](./docs/command_line.md)
- [`docs/gui_functions.md`](./docs/gui_functions.md)

## Legacy GUI Context

The legacy GUI is a graphical interface for the ProLuCID database search engine for bottom-up proteomics protein identification. It takes MS2 files and a FASTA database as input, produces search outputs, and supports DTASelect-based filtering.

Legacy example assets remain at the repository root, including `example.ms2`, `UniProt_human_with_reversed_sequence.fasta`, and `default_trypsin.prolucid_params`.

## Authors

- Yu (Tom) Gao, Yates Lab
- Python 3 rewrite based on the legacy project in this repository

## License

This tool is free to use for academic research purpose only.

## Citation

Please cite the original ProLuCID paper:

ProLuCID: An improved SEQUEST-like algorithm with enhanced sensitivity and specificity. Journal of Proteomics, 2015.
