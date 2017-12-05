# Prolucid GUI 
by Yu (Tom) Gao @ Yates laboratory

This is a graphical user interface for the Prolucid database search engine [https://doi.org/10.1016/j.jprot.2015.07.001] for bottom-up proteomics protein identification. This tool takes MS2 files and .fasta database as input, to generate sqt file for protein and peptide identification. It also contains an internal DTASelect2 for the FDR estimation and result filtering. I hope this tool can make proteomics research easier for all researchers.

## Example with Thermo .raw files

Here is an example of how to use this tool to search Thermo .raw files.

### Prerequisites

This tool needs java to be installed on your computer, to check, run the following command using cmd.exe:

```
java -version
```

### Convert your Thermo raw files to ms2 

Please use rawconveter [http://fields.scripps.edu/rawconv/] or proteowizard [http://proteowizard.sourceforge.net/] to convert .raw files to .ms2 files. We also have an experimental version of this tool which converts raw files internally (works on Ubuntu, OSX and Windows), please send me a request if you'd like to test it.

For demo purpose, I have included an example.ms2 file for you to practice. I have also added an exmple fasta file (Uniprot Human protein database with reviewed sequence only, reversed sequence for FDR estimation added at the end).

### Running the example

On windows:

1. Double click Prolucid_GUI.exe
2. Click "..." on the right side of "FASTA file:" to specify your database file, here we use "UniProt_human_with_reversed_sequence.fasta"  
3. Click "..." on the right side of "Java path:" to specify your java.exe location, it is typically at "C:\Program Files\Java\jre1.X.X\bin\java.exe"
4. Click "..." on the right side of "MS2 file path:" to select all MS2 files that you want to search. Here we select "example.ms2". You can select multiple MS2 files for search, each MS2 file will be separated by ';' and you can edit it manually.
5. Set all the parameters, see the "Parameters" section for details. Or you can simply click "Load parameters ..." to load previously saved parameters, here we can load "default_trypsin.prolucid_params" file to set default parameters.
6. Click "..." on the right side of "Result file output folder:" to specify a folder to store search results.
7. Click Run ProLuCID and DTASelect to run database search. It may take 5-60 minutes depends on the size of your MS2 file, the size of the database and your specific parameters.
8. After search, you can re-do the DTASelect filtering with different parameters using the button "Re-run DTASelect only", this will only take a minute or less.
9. You can now check your results at the folder you specified in Step 6

### Parameters
* Precursor tolerance in ppm: 50 (default) 
The maximum allowed mass shift in ppm for precursor ions.
For high resolution instrument, such as Orbitrap, we recommend no more than 50. Well calibrated instrument, you can set to 25

* Number of isotopes: 3 (default)
The number of isotopic peaks allowed to search. If your data has been corrected for monoisotopic peak, i.e. you assume all assigned precursor mass within MS2 file is the monoisotopic mass, then you can set this to "1" and it will accelerate your database search.
For normal data, we recommend 3. For heavy isotope depleted sample, use 1.

* Precursor starts and Precursor ends (Da): 600 - 6000 (default)
The range of allowed precursor mass in Dalton.  

* Protease name: trypsin (default) The name of your enzyme.

* Cleavage residues: KR (default for trypsin) The cleavage sites for your enzyme.

* Enzyme specificity: 2 specific at both ends (default) The specificity of your enzyme. "0" assumes no specificity, therefore, no matter what you set for protease and cleavage residues, all cleavages are allowed, i.e. peptide can break at any amino acid. "1" assumes at least one end of each peptide is specific. In trypsin, that means at least one end is "R" or "K". "2" assumes your enzyme to be highly specific. For trypsin, both ends of each peptides needs to be either "K" or "R".

* Maximum missed cleavage: 2 (default) In the case of trypsin, how many "K" and "R" are allows in the middle of a peptide. For example, "SVSAGGERGLGSAGR" has 1 missed cleavage.

* Static modification: 57.02146 (default) Static modification of the peptide. The carbamidomethyl (+57.02146) modification on Cysteine, which is typical in bottom-up proteomics to alkylate cys to prevent cys-cys formation after reduction. Do not change if you don't know what it is. Other examples such as "225.1558 K" for TMT 2-plex on K, "229.1629 K" for both TMT 6-plex and 10-plex on K, "144.1021 K" for iTRAQ on K, "28.0313 K" for Dimethyl labeling.

* Differential modification: none (default) The variable modification on peptide such as post-translational modification or incomplete reaction. You can put multiple ones in here by separating them with ";". For example "79.966331 STY;0.984016 NQ" will search for both Deamidation and Phosphorylation.

* C-term and N-term static mod: none (default) The static modification on the C-termini or N-termini of the peptides. For example, N-term "28.0313" for dimethyl labeling.

* Min # of peptide/protein: 2 (default) The minimum number of peptides per protein. When set to 2, DTASelect will only report proteins with at least two identified peptides as evidence. When searching small data set, this can be set to "1" to include proteins evidenced by only one peptide.

* Min # of tryptic end: 2 (default) Similar as Enzyme specificity, but performed by DTASelect at filter level.

* Protein/Peptide/Spectrum level FDR : Protein (default) FDR estimation level. False discovery rate (FDR) can be estimated at either protein, peptide or spectrum level.

* FDR threshold: 0.05 (default) The FDR threshold of the filter, 0.05 Protein level FDR means DTASelect will allow at most 5% false protein identification in the results. For good quality data with many proteins (lysate sample), this can be set as low as 1% Protein level. Protein level filter is typically more stringent. (Protein >> Peptide > Spectrum)

* Other advanced parameters cannot be set by this interface, but can be loaded with "Load parameters...", please contact me for advanced search.  

## Authors

* **Yu (Tom) Gao** - *@Yates Lab* - [My website](http://www.pepchem.org)

Email me if you have any question [email me](mailto:bathygao@gmail.com).

## License

This tool is free to use for academic research purpose only. 

## Citation

Please cite the original ProLuCID paper: [https://doi.org/10.1016/j.jprot.2015.07.001]

"ProLuCID: An improved SEQUEST-like algorithm with enhanced sensitivity and specificity"
Journal of Proteomics, 2015
