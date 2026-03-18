from __future__ import annotations

import argparse

from .config import ProlucidConfig
from .gui import launch_gui
from .runner import run_all, run_dtaselect, run_prolucid
from .xml_writer import write_search_xml


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--java", dest="java_path", default=None)
    parser.add_argument("--jar", dest="prolucid_jar_path", default=None)
    parser.add_argument("--dtaselect-classpath", default=None)
    parser.add_argument("--fasta", dest="fasta_path", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--ms2", action="append", default=None)
    parser.add_argument("--java-xmx", default=None)
    parser.add_argument("--threads", dest="java_thread", default=None)
    parser.add_argument("--precursor-ppm", default=None)
    parser.add_argument("--num-isotope", default=None)
    parser.add_argument("--min-mass", default=None)
    parser.add_argument("--max-mass", default=None)
    parser.add_argument("--protease", default=None)
    parser.add_argument("--cleave-residue", default=None)
    parser.add_argument("--enzyme-spec", type=int, default=None)
    parser.add_argument("--max-miss-cleave", default=None)
    parser.add_argument("--stat-mod", default=None)
    parser.add_argument("--diff-mod", default=None)
    parser.add_argument("--c-term-stat-mod", default=None)
    parser.add_argument("--n-term-stat-mod", default=None)
    parser.add_argument("--dta-min-num-peptide", default=None)
    parser.add_argument("--dta-min-num-tryptic-end", type=int, default=None)
    parser.add_argument("--fdr-level", choices=["protein", "peptide", "spectrum"], default=None)
    parser.add_argument("--fdr-filter", default=None)
    parser.add_argument("--params-file", default=None)


def _config_from_args(args: argparse.Namespace) -> ProlucidConfig:
    config = ProlucidConfig.from_legacy_file(args.params_file) if args.params_file else ProlucidConfig()
    for field_name in (
        "java_path",
        "prolucid_jar_path",
        "dtaselect_classpath",
        "fasta_path",
        "output_dir",
        "java_xmx",
        "java_thread",
        "precursor_ppm",
        "num_isotope",
        "min_mass",
        "max_mass",
        "protease",
        "cleave_residue",
        "enzyme_spec",
        "max_miss_cleave",
        "stat_mod",
        "diff_mod",
        "c_term_stat_mod",
        "n_term_stat_mod",
        "dta_min_num_peptide",
        "dta_min_num_tryptic_end",
        "fdr_level",
        "fdr_filter",
    ):
        value = getattr(args, field_name, None)
        if value is not None:
            setattr(config, field_name, value)
    if args.ms2 is not None:
        config.ms2_files = args.ms2
    return config.normalize()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prolucid_gui")
    subparsers = parser.add_subparsers(dest="command", required=False)

    gui_parser = subparsers.add_parser("gui", help="Launch the Tk GUI")

    xml_parser = subparsers.add_parser("write-search-xml", help="Write search.xml only")
    _add_common_args(xml_parser)
    xml_parser.add_argument("--output", required=True)

    search_parser = subparsers.add_parser("run-prolucid", help="Run ProLuCID only")
    _add_common_args(search_parser)

    dta_parser = subparsers.add_parser("run-dtaselect", help="Run DTASelect only")
    _add_common_args(dta_parser)
    dta_parser.add_argument("--sqt-dir", default="")

    all_parser = subparsers.add_parser("run-all", help="Run ProLuCID and DTASelect")
    _add_common_args(all_parser)

    save_parser = subparsers.add_parser("save-params", help="Save a legacy .prolucid_params file")
    _add_common_args(save_parser)
    save_parser.add_argument("--output", required=True)

    gui_parser.set_defaults(handler=lambda _args: launch_gui())
    xml_parser.set_defaults(handler=handle_write_search_xml)
    search_parser.set_defaults(handler=handle_run_prolucid)
    dta_parser.set_defaults(handler=handle_run_dtaselect)
    all_parser.set_defaults(handler=handle_run_all)
    save_parser.set_defaults(handler=handle_save_params)
    return parser


def handle_write_search_xml(args: argparse.Namespace) -> int:
    path = write_search_xml(_config_from_args(args), args.output)
    print(f"Wrote {path}")
    return 0


def handle_run_prolucid(args: argparse.Namespace) -> int:
    outputs = run_prolucid(_config_from_args(args))
    for output in outputs:
        print(output)
    return 0


def handle_run_dtaselect(args: argparse.Namespace) -> int:
    filtered_dir = run_dtaselect(_config_from_args(args), sqt_dir=args.sqt_dir or None)
    print(filtered_dir)
    return 0


def handle_run_all(args: argparse.Namespace) -> int:
    sqt_files, filtered_dir = run_all(_config_from_args(args))
    for path in sqt_files:
        print(path)
    print(filtered_dir)
    return 0


def handle_save_params(args: argparse.Namespace) -> int:
    _config_from_args(args).save_legacy_file(args.output)
    print(args.output)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        return launch_gui()
    return args.handler(args)
