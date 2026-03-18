from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from .config import ProlucidConfig


VALID_RESIDUES = set("ARNDCQEGHILKMFPSTWYV")


def _parse_modifications(raw: str) -> list[tuple[str, str]]:
    parsed: list[tuple[str, str]] = []
    for item in raw.split(";"):
        item = item.strip()
        if not item or " " not in item:
            continue
        mass, residues = item.split(None, 1)
        parsed.append((mass.strip(), residues.strip().upper()))
    return parsed


def _append_text(parent: ET.Element, name: str, value: str) -> ET.Element:
    child = ET.SubElement(parent, name)
    child.text = value
    return child


def build_search_tree(config: ProlucidConfig) -> ET.ElementTree:
    config.normalize()
    root = ET.Element("parameters")

    database = ET.SubElement(root, "database")
    _append_text(database, "database_name", config.fasta_path)
    _append_text(database, "is_indexed", "false")

    search_mode = ET.SubElement(root, "search_mode")
    for key, value in (
        ("primary_score_type", "1"),
        ("secondary_score_type", "2"),
        ("locus_type", "1"),
        ("charge_disambiguation", "0"),
        ("atomic_enrichement", "0"),
        ("min_match", "0"),
        ("peak_rank_threshold", "200"),
        ("candidate_peptide_threshold", "500"),
        ("num_output", "5"),
        ("is_decharged", "0"),
        ("fragmentation_method", "CID"),
        ("multistage_activation_mode", "0"),
        ("preprocess", "1"),
    ):
        _append_text(search_mode, key, value)

    isotopes = ET.SubElement(root, "isotopes")
    _append_text(isotopes, "precursor", "mono")
    _append_text(isotopes, "fragment", "mono")
    _append_text(isotopes, "num_peaks", config.num_isotope)

    tolerance = ET.SubElement(root, "tolerance")
    _append_text(tolerance, "precursor_high", "3000")
    _append_text(tolerance, "precursor_low", "3000")
    _append_text(tolerance, "precursor", config.precursor_ppm)
    _append_text(tolerance, "fragment", "600")

    precursor_mass_limits = ET.SubElement(root, "precursor_mass_limits")
    _append_text(precursor_mass_limits, "minimum", config.min_mass)
    _append_text(precursor_mass_limits, "maximum", config.max_mass)

    precursor_charge_limits = ET.SubElement(root, "precursor_charge_limits")
    _append_text(precursor_charge_limits, "minimum", "0")
    _append_text(precursor_charge_limits, "maximum", "1000")

    peptide_length_limits = ET.SubElement(root, "peptide_length_limits")
    _append_text(peptide_length_limits, "minimum", "6")

    num_peak_limits = ET.SubElement(root, "num_peak_limits")
    _append_text(num_peak_limits, "minimum", "25")
    _append_text(num_peak_limits, "maximum", "5000")

    _append_text(root, "max_num_diffmod", "5")

    modifications = ET.SubElement(root, "modifications")
    _append_text(modifications, "display_mod", "0")

    for terminus_name, mass_shift in (
        ("n_term", config.n_term_stat_mod or "0.0"),
        ("c_term", config.c_term_stat_mod or "0.0"),
    ):
        terminus = ET.SubElement(modifications, terminus_name)
        static_mod = ET.SubElement(terminus, "static_mod")
        _append_text(static_mod, "symbol", "*")
        _append_text(static_mod, "mass_shift", mass_shift)
        diff_mods = ET.SubElement(terminus, "diff_mods")
        diff_mod = ET.SubElement(diff_mods, "diff_mod")
        _append_text(diff_mod, "symbol", "*")
        _append_text(diff_mod, "mass_shift", mass_shift)

    static_mods = ET.SubElement(modifications, "static_mods")
    for mass, residues in _parse_modifications(config.stat_mod):
        for residue in residues:
            if residue not in VALID_RESIDUES:
                continue
            static_mod = ET.SubElement(static_mods, "static_mod")
            _append_text(static_mod, "symbol", "*")
            _append_text(static_mod, "mass_shift", mass)
            _append_text(static_mod, "residue", residue)

    diff_mods = ET.SubElement(modifications, "diff_mods")
    for mass, residues in _parse_modifications(config.diff_mod):
        diff_mod = ET.SubElement(diff_mods, "diff_mod")
        _append_text(diff_mod, "symbol", "*")
        _append_text(diff_mod, "mass_shift", mass)
        residues_node = ET.SubElement(diff_mod, "residues")
        for residue in residues:
            if residue in VALID_RESIDUES:
                _append_text(residues_node, "residue", residue)

    enzyme = ET.SubElement(root, "enzyme_info")
    _append_text(enzyme, "name", config.protease)
    _append_text(enzyme, "specificity", str(config.enzyme_spec))
    _append_text(enzyme, "max_num_internal_mis_cleavage", config.max_miss_cleave)
    _append_text(enzyme, "type", "true")
    residues = ET.SubElement(enzyme, "residues")
    for residue in config.cleave_residue.upper():
        if residue in VALID_RESIDUES:
            _append_text(residues, "residue", residue)

    advanced = ET.SubElement(root, "advanced_params")
    _append_text(advanced, "scan_number", "0")

    return ET.ElementTree(root)


def write_search_xml(config: ProlucidConfig, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    tree = build_search_tree(config)
    output.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<!--Parameters for ProLuCID database search-->\n',
        encoding="utf-8",
    )
    with output.open("a", encoding="utf-8") as handle:
        ET.indent(tree, space="  ")
        tree.write(handle, encoding="unicode")
    return output
