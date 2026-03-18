from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


FDR_LEVEL_MAP = {0: "protein", 1: "peptide", 2: "spectrum"}
FDR_FLAG_MAP = {"protein": "--pfp", "peptide": "--sfp", "spectrum": "--fp"}


@dataclass
class ProlucidConfig:
    java_path: str = "java"
    prolucid_jar_path: str = ""
    dtaselect_classpath: str = ""
    fasta_path: str = ""
    ms2_files: list[str] = field(default_factory=list)
    output_dir: str = ""
    precursor_ppm: str = "50"
    num_isotope: str = "3"
    min_mass: str = "600"
    max_mass: str = "6000"
    protease: str = "trypsin"
    cleave_residue: str = "KR"
    enzyme_spec: int = 2
    max_miss_cleave: str = "2"
    stat_mod: str = "57.02146 C"
    diff_mod: str = ""
    c_term_stat_mod: str = ""
    n_term_stat_mod: str = ""
    dta_min_num_peptide: str = "2"
    dta_min_num_tryptic_end: int = 2
    fdr_level: str = "protein"
    fdr_filter: str = "0.05"
    java_xmx: str = "8G"
    java_thread: str = "8"

    def validate_for_search(self) -> None:
        missing = []
        if not self.fasta_path:
            missing.append("fasta_path")
        if not self.prolucid_jar_path:
            missing.append("prolucid_jar_path")
        if not self.ms2_files:
            missing.append("ms2_files")
        if not self.output_dir:
            missing.append("output_dir")
        if missing:
            raise ValueError(f"Missing required search fields: {', '.join(missing)}")

    def validate_for_dtaselect(self) -> None:
        missing = []
        if not self.fasta_path:
            missing.append("fasta_path")
        if not self.dtaselect_classpath:
            missing.append("dtaselect_classpath")
        if not self.output_dir:
            missing.append("output_dir")
        if missing:
            raise ValueError(f"Missing required DTASelect fields: {', '.join(missing)}")

    def normalize(self) -> "ProlucidConfig":
        self.fdr_level = self.fdr_level.lower().strip()
        if self.fdr_level not in FDR_FLAG_MAP:
            raise ValueError(f"Unsupported fdr_level: {self.fdr_level}")
        self.ms2_files = [str(Path(item)) for item in self.ms2_files if item]
        return self

    @classmethod
    def from_legacy_dict(cls, payload: dict) -> "ProlucidConfig":
        return cls(
            java_path=payload.get("java_path", "java"),
            prolucid_jar_path=payload.get("prolucid_jar_path", ""),
            dtaselect_classpath=payload.get("dtaselect_classpath", ""),
            fasta_path=payload.get("fasta_path", ""),
            precursor_ppm=payload.get("precursor_ppm", "50"),
            num_isotope=payload.get("num_isotope", "3"),
            min_mass=payload.get("min_mass", "600"),
            max_mass=payload.get("max_mass", "6000"),
            protease=payload.get("protease", "trypsin"),
            cleave_residue=payload.get("cleave_residue", "KR"),
            enzyme_spec=int(payload.get("enzyme_spec", 2)),
            max_miss_cleave=payload.get("max_miss_cleave", "2"),
            stat_mod=payload.get("stat_mod", "57.02146 C"),
            diff_mod=payload.get("diff_mod", ""),
            c_term_stat_mod=payload.get("c_term_stat_mod", ""),
            n_term_stat_mod=payload.get("n_term_stat_mod", ""),
            dta_min_num_peptide=payload.get("DTA_min_num_peptide", "2"),
            dta_min_num_tryptic_end=int(payload.get("DTA_min_num_tryptic_end", 2)),
            fdr_level=FDR_LEVEL_MAP.get(int(payload.get("FDR_level", 0)), "protein"),
            fdr_filter=payload.get("FDR_filter", "0.05"),
            java_xmx=payload.get("java_xmx", "8G"),
            java_thread=payload.get("java_thread", "8"),
        ).normalize()

    @classmethod
    def from_legacy_file(cls, path: str | Path) -> "ProlucidConfig":
        return cls.from_legacy_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def to_legacy_dict(self) -> dict:
        reverse_fdr_level = {"protein": 0, "peptide": 1, "spectrum": 2}
        return {
            "java_path": self.java_path,
            "fasta_path": self.fasta_path,
            "precursor_ppm": self.precursor_ppm,
            "num_isotope": self.num_isotope,
            "min_mass": self.min_mass,
            "max_mass": self.max_mass,
            "protease": self.protease,
            "cleave_residue": self.cleave_residue,
            "enzyme_spec": self.enzyme_spec,
            "max_miss_cleave": self.max_miss_cleave,
            "stat_mod": self.stat_mod,
            "diff_mod": self.diff_mod,
            "c_term_stat_mod": self.c_term_stat_mod,
            "n_term_stat_mod": self.n_term_stat_mod,
            "DTA_min_num_peptide": self.dta_min_num_peptide,
            "DTA_min_num_tryptic_end": self.dta_min_num_tryptic_end,
            "FDR_level": reverse_fdr_level[self.fdr_level],
            "FDR_filter": self.fdr_filter,
            "java_xmx": self.java_xmx,
            "java_thread": self.java_thread,
            "prolucid_jar_path": self.prolucid_jar_path,
            "dtaselect_classpath": self.dtaselect_classpath,
        }

    def save_legacy_file(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_legacy_dict(), indent=2), encoding="utf-8")

    def to_dict(self) -> dict:
        return asdict(self)
