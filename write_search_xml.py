import lxml.etree
import lxml.builder


fasta_path=r'E:\Java\prolucid\test_full\namkyung\UniProt_Human_04-01-2015_reversed.fasta'
num_isotope=3
precursor_tolerence_ppm=50
precursor_start=600
precursor_end=6000
n_term_stat_mod=0.0
c_term_stat_mod=0.0

with open('search.xml','wb') as search_xml:
    search_xml.write('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!--Parameters for ProLuCID database search-->\n')
    search = lxml.builder.ElementMaker()
    parameters = search.parameters
    database = search.database
    search_mode = search.search_mode
    database_name = search.database_name
    is_indexed = search.is_indexed
    primary_score_type = search.primary_score_type
    secondary_score_type = search.secondary_score_type
    locus_type = search.locus_type
    charge_disambiguation = search.charge_disambiguation
    atomic_enrichement = search.atomic_enrichement
    min_match = search.min_match
    peak_rank_threshold = search.peak_rank_threshold
    candidate_peptide_threshold = search.candidate_peptide_threshold
    num_output = search.num_output
    is_decharged = search.is_decharged
    fragmentation_method = search.fragmentation_method
    multistage_activation_mode = search.multistage_activation_mode
    preprocess = search.preprocess
    isotopes = search.isotopes
    precursor = search.precursor
    fragment = search.fragment
    num_peaks = search.num_peaks
    tolerance = search.tolerance
    precursor_high = search.precursor_high
    precursor_low = search.precursor_low
    precursor_mass_limits = search.precursor_mass_limits
    minimum = search.minimum
    maximum = search.maximum
    precursor_charge_limits = search.precursor_charge_limits
    peptide_length_limits = search.peptide_length_limits
    num_peak_limits = search.num_peak_limits
    max_num_diffmod = search.max_num_diffmod
    modifications = search.modifications
    display_mod = search.display_mod
    n_term = search.n_term
    static_mod = search.static_mod
    symbol = search.symbol
    mass_shift = search.mass_shift
    diff_mods = search.diff_mods
    diff_mod = search.diff_mod
    c_term = search.c_term


    the_doc = parameters(
        database(
            database_name(fasta_path),
            is_indexed('false'),
                ),
        search_mode(
            primary_score_type('1'),
            secondary_score_type('2'),
            locus_type('1'),
            charge_disambiguation('0'),
            atomic_enrichement('0'),
            min_match('0'),
            peak_rank_threshold('200'),
            candidate_peptide_threshold('500'),
            num_output('5'),
            is_decharged('0'),
            fragmentation_method('CID'),
            multistage_activation_mode('0'),
            preprocess('1'),
        ),
        isotopes(
            precursor('mono'),
            fragment('mono'),
            num_peaks(str(num_isotope)),
        ),
        tolerance(
            precursor_high('3000'),
            precursor_low('3000'),
            precursor(str(precursor_tolerence_ppm)),
            fragment('600'),
        ),
        precursor_mass_limits(
            minimum(str(precursor_start)),
            maximum(str(precursor_end)),
        ),
        precursor_charge_limits(
            minimum('0'),
            maximum('1000'),
        ),
        peptide_length_limits(
            minimum('6'),
        ),
        num_peak_limits(
            minimum('25'),
            maximum('5000'),
        ),
        max_num_diffmod('3'),
        modifications(
            display_mod('0'),
            n_term(
                static_mod(
                    symbol('*'),
                    mass_shift(str(n_term_stat_mod)),
                ),
                diff_mods(
                    diff_mod(
                        symbol('*'),
                        mass_shift(str(n_term_stat_mod)),
                    ),
                ),
            ),
            c_term(
                static_mod(
                    symbol('*'),
                    mass_shift(str(c_term_stat_mod)),
                ),
                diff_mods(
                    diff_mod(
                        symbol('*'),
                        mass_shift(str(n_term_stat_mod)),
                    ),
                ),
            ),
        ),

            )


    newerKid = lxml.etree.Element('cnnn')
    the_doc[9].insert(3, newerKid)

    search_xml.write(lxml.etree.tostring(the_doc, pretty_print=True))