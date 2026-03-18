from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from .config import FDR_FLAG_MAP, ProlucidConfig
from .xml_writer import write_search_xml


def build_prolucid_command(
    java_path: str,
    java_xmx: str,
    prolucid_jar_path: str,
    ms2_file: str | Path,
    search_xml_path: str | Path,
    threads: str,
) -> list[str]:
    return [
        java_path,
        f"-Xmx{java_xmx}",
        "-jar",
        str(prolucid_jar_path),
        str(ms2_file),
        str(search_xml_path),
        str(threads),
    ]


def build_dtaselect_command(config: ProlucidConfig) -> list[str]:
    return [
        config.java_path,
        "-cp",
        config.dtaselect_classpath,
        "DTASelect",
        "-p",
        str(config.dta_min_num_peptide),
        "-y",
        str(config.dta_min_num_tryptic_end),
        "--trypstat",
        FDR_FLAG_MAP[config.fdr_level],
        str(config.fdr_filter),
        "--modstat",
        "--extra",
        "--pI",
        "--DB",
        "--dm",
        "-t",
        "0",
        "--brief",
        "--quiet",
    ]


def write_minimal_sequest_params(fasta_path: str, output_path: str | Path) -> Path:
    text = (
        "# Minimal sequest.params for DTASelect\n"
        "[SEQUEST]\n"
        f"database_name = {fasta_path}\n"
        "peptide_mass_tolerance = 3\n"
        "create_output_files = 1\n"
        "\n"
        "[SEQUEST_ENZYME_INFO]\n"
        "0. No_Enzyme 0 - -\n"
        "1. Trypsin 1 KR P\n"
    )
    path = Path(output_path)
    path.write_text(text, encoding="utf-8")
    return path


def run_prolucid(config: ProlucidConfig) -> list[Path]:
    config.normalize()
    config.validate_for_search()
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    search_xml_path = write_search_xml(config, output_dir / "search.xml")

    produced_sqt_files: list[Path] = []
    for ms2_file in [Path(item) for item in config.ms2_files]:
        cmd = build_prolucid_command(
            java_path=config.java_path,
            java_xmx=config.java_xmx,
            prolucid_jar_path=config.prolucid_jar_path,
            ms2_file=ms2_file,
            search_xml_path=search_xml_path,
            threads=config.java_thread,
        )
        log_path = output_dir / f"{ms2_file.stem}.log"
        with log_path.open("w", encoding="utf-8") as log_handle:
            subprocess.run(
                cmd,
                cwd=ms2_file.parent,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                check=True,
            )
        expected_sqt = ms2_file.with_suffix(".sqt")
        if not expected_sqt.exists():
            raise FileNotFoundError(f"Expected ProLuCID output not found: {expected_sqt}")
        target_sqt = output_dir / expected_sqt.name
        shutil.move(str(expected_sqt), str(target_sqt))
        produced_sqt_files.append(target_sqt)
    return produced_sqt_files


def run_dtaselect(config: ProlucidConfig, sqt_dir: str | Path | None = None) -> Path:
    config.normalize()
    config.validate_for_dtaselect()
    source_dir = Path(sqt_dir or config.output_dir)
    if not source_dir.exists():
        raise FileNotFoundError(f"SQT input directory does not exist: {source_dir}")

    sqt_files = sorted(source_dir.glob("*.sqt"))
    if not sqt_files:
        raise FileNotFoundError(f"No .sqt files found in {source_dir}")

    filtered_dir = Path(config.output_dir) / f"Filtered_result_{config.fdr_level}_{config.fdr_filter}"
    filtered_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="dtaselect_") as temp_dir_raw:
        temp_dir = Path(temp_dir_raw)
        for sqt_file in sqt_files:
            shutil.copy2(sqt_file, temp_dir / sqt_file.name)
        write_minimal_sequest_params(config.fasta_path, temp_dir / "sequest.params")
        subprocess.run(build_dtaselect_command(config), cwd=temp_dir, check=True)
        for pattern in ("*.txt", "*.html", "*.dta", "*.xml"):
            for file_path in temp_dir.glob(pattern):
                shutil.copy2(file_path, filtered_dir / file_path.name)

    return filtered_dir


def run_all(config: ProlucidConfig) -> tuple[list[Path], Path]:
    sqt_files = run_prolucid(config)
    filtered_dir = run_dtaselect(config, sqt_dir=config.output_dir)
    return sqt_files, filtered_dir
