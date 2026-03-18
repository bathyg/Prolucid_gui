# GUI Functions

The Python 3 GUI is a simpler replacement for the old `wxPython` window.

## Main Inputs

- `Java path`: path to `java` or just `java` if it is in `PATH`
- `ProLuCID jar`: path to `ProLuCID1_3.jar`
- `DTASelect classpath`: folder or classpath string used with `java -cp`
- `FASTA file`: database FASTA file
- `MS2 files`: one or more `.ms2` files
- `Output folder`: where `.sqt`, `.log`, and DTASelect outputs are written

## Search Parameters

- `Java Xmx`
- `Threads`
- `Precursor ppm`
- `Isotopes`
- `Min/Max mass`
- `Protease`
- `Cleavage residues`
- `Enzyme specificity`
- `Max missed cleavage`
- `Static mod`
- `Diff mod`
- `N-term static mod`
- `C-term static mod`

## DTASelect Parameters

- `Min peptides/protein`
- `Min tryptic ends`
- `FDR level`
- `FDR filter`

## Buttons

- `Load params`: load a legacy `.prolucid_params` JSON file
- `Save params`: save the current settings in the same format
- `Write search.xml`: generate only the ProLuCID XML file
- `Run ProLuCID`: run only the database search
- `Run DTASelect`: run only filtering on existing `.sqt` files
- `Run All`: generate XML, run ProLuCID, then run DTASelect

## Output Files

Typical outputs:

- `search.xml`
- one `.sqt` file per `.ms2` input
- one `.log` file per `.ms2` input
- DTASelect outputs such as `DTASelect-filter.txt` and `DTASelect.html`
