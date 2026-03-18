# Command Line Usage

This project wraps two external tools:

- ProLuCID, typically as `ProLuCID1_3.jar`
- DTASelect, usually started through Java with a classpath

## 1. Run ProLuCID Directly

The legacy project constructs this command:

```bash
java -Xmx8G -jar ProLuCID1_3.jar sample.ms2 search.xml 8
```

Meaning:

- `-Xmx8G`: Java heap size
- `-jar ProLuCID1_3.jar`: run the ProLuCID jar
- `sample.ms2`: input spectrum file
- `search.xml`: ProLuCID search parameter file
- `8`: number of threads

In this rewrite:

```bash
python -m prolucid_gui run-prolucid ^
  --java java ^
  --jar C:\tools\ProLuCID1_3.jar ^
  --ms2 C:\data\sample.ms2 ^
  --fasta C:\db\database.fasta ^
  --output-dir C:\results
```

## 2. Run DTASelect Directly

The legacy project constructs a DTASelect command in this form:

```bash
java -cp DTASelect2 DTASelect -p 2 -y 2 --trypstat --pfp 0.05 --modstat --extra --pI --DB --dm -t 0 --brief --quiet
```

Meaning:

- `-cp DTASelect2`: Java classpath for DTASelect
- `DTASelect`: main class
- `-p 2`: minimum peptides per protein
- `-y 2`: minimum tryptic ends
- `--pfp 0.05`: protein-level FDR filter of 5%

The filter flag changes by FDR level:

- protein: `--pfp`
- peptide: `--sfp`
- spectrum: `--fp`

In this rewrite:

```bash
python -m prolucid_gui run-dtaselect ^
  --java java ^
  --dtaselect-classpath C:\tools\DTASelect2 ^
  --sqt-dir C:\results ^
  --output-dir C:\results ^
  --fasta C:\db\database.fasta
```

## 3. Run the Full Workflow

```bash
python -m prolucid_gui run-all ^
  --java java ^
  --jar C:\tools\ProLuCID1_3.jar ^
  --dtaselect-classpath C:\tools\DTASelect2 ^
  --fasta C:\db\database.fasta ^
  --ms2 C:\data\a.ms2 ^
  --ms2 C:\data\b.ms2 ^
  --output-dir C:\results
```

## 4. Generate Only `search.xml`

```bash
python -m prolucid_gui write-search-xml ^
  --fasta C:\db\database.fasta ^
  --output C:\results\search.xml
```

## 5. Legacy Parameter Files

The old GUI stores settings in a JSON file with extension `.prolucid_params`.

This rewrite can still load that format. A sample file is included at:

`examples/default_trypsin.prolucid_params`
