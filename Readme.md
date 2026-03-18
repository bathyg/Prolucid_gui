# Prolucid GUI

Legacy ProLuCID GUI by Yu (Tom) Gao, with a newer Python 3 rewrite kept in [`src/`](./src).

This repository now contains two related parts:

- The original desktop workflow and example assets used by the legacy project.
- A Python 3 rewrite of the GUI and command-line workflow under [`src/`](./src).

Both versions follow the same overall process:

1. Choose a FASTA database.
2. Choose one or more `.ms2` files.
3. Generate `search.xml`.
4. Run ProLuCID.
5. Run DTASelect on the resulting `.sqt` files.

## Repository Layout

```text
.
|-- Prolucid_GUI.py
|-- Prolucid_GUI.exe
|-- example.ms2
|-- UniProt_human_with_reversed_sequence.fasta
|-- default_trypsin.prolucid_params
`-- src/
    |-- docs/
    |-- examples/
    |-- pyproject.toml
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

Install from the rewrite folder:

```bash
cd src
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

Rewrite documentation:

- [`src/docs/command_line.md`](./src/docs/command_line.md)
- [`src/docs/gui_functions.md`](./src/docs/gui_functions.md)

## Legacy GUI Example

The legacy GUI is a graphical interface for the ProLuCID database search engine for bottom-up proteomics protein identification. It takes MS2 files and a FASTA database as input, produces search outputs, and supports DTASelect-based filtering.

### Prerequisites

Check that Java is installed:

```bash
java -version
```

To convert Thermo `.raw` files to `.ms2`, use RawConverter or ProteoWizard before running the search workflow.

### Running the Example

On Windows:

1. Start `Prolucid_GUI.exe`.
2. Select the FASTA database, for example `UniProt_human_with_reversed_sequence.fasta`.
3. Select your `java.exe` path.
4. Select one or more `.ms2` files, for example `example.ms2`.
5. Load parameters such as `default_trypsin.prolucid_params`, or set them manually.
6. Choose an output folder for search results.
7. Run ProLuCID and DTASelect.
8. Re-run DTASelect later if you want to change filtering only.

## Authors

- Yu (Tom) Gao, Yates Lab
- Python 3 rewrite based on the legacy project in this repository

## License

This tool is free to use for academic research purpose only.

## Citation

Please cite the original ProLuCID paper:

ProLuCID: An improved SEQUEST-like algorithm with enhanced sensitivity and specificity. Journal of Proteomics, 2015.
