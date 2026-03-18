from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .config import ProlucidConfig
from .runner import run_all, run_dtaselect, run_prolucid
from .xml_writer import write_search_xml


FIELD_ORDER = [
    ("java_path", "Java path"),
    ("prolucid_jar_path", "ProLuCID jar"),
    ("dtaselect_classpath", "DTASelect classpath"),
    ("fasta_path", "FASTA file"),
    ("output_dir", "Output folder"),
    ("ms2_files", "MS2 files (; separated)"),
    ("java_xmx", "Java Xmx"),
    ("java_thread", "Threads"),
    ("precursor_ppm", "Precursor ppm"),
    ("num_isotope", "Isotopes"),
    ("min_mass", "Min mass"),
    ("max_mass", "Max mass"),
    ("protease", "Protease"),
    ("cleave_residue", "Cleavage residues"),
    ("enzyme_spec", "Enzyme specificity"),
    ("max_miss_cleave", "Max missed cleavage"),
    ("stat_mod", "Static mod"),
    ("diff_mod", "Diff mod"),
    ("n_term_stat_mod", "N-term static mod"),
    ("c_term_stat_mod", "C-term static mod"),
    ("dta_min_num_peptide", "Min peptides/protein"),
    ("dta_min_num_tryptic_end", "Min tryptic ends"),
    ("fdr_level", "FDR level"),
    ("fdr_filter", "FDR filter"),
]


class ProlucidGuiApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("ProLuCID GUI Python 3")
        self.vars: dict[str, tk.StringVar] = {}
        self._build()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        for idx, (field_name, label) in enumerate(FIELD_ORDER):
            ttk.Label(frame, text=label).grid(row=idx, column=0, sticky="w", padx=(0, 8), pady=3)
            variable = tk.StringVar()
            self.vars[field_name] = variable
            entry = ttk.Entry(frame, textvariable=variable, width=72)
            entry.grid(row=idx, column=1, sticky="ew", pady=3)
            frame.columnconfigure(1, weight=1)

            if field_name in {"fasta_path", "prolucid_jar_path"}:
                ttk.Button(frame, text="...", command=lambda name=field_name: self._pick_file(name)).grid(row=idx, column=2, padx=(6, 0))
            elif field_name == "output_dir":
                ttk.Button(frame, text="...", command=self._pick_dir).grid(row=idx, column=2, padx=(6, 0))
            elif field_name == "ms2_files":
                ttk.Button(frame, text="...", command=self._pick_ms2_files).grid(row=idx, column=2, padx=(6, 0))

        button_row = ttk.Frame(frame)
        button_row.grid(row=len(FIELD_ORDER), column=0, columnspan=3, sticky="ew", pady=(12, 6))
        for idx, (label, callback) in enumerate(
            [
                ("Load params", self.load_params),
                ("Save params", self.save_params),
                ("Write search.xml", self.write_search_xml_only),
                ("Run ProLuCID", self.run_prolucid_only),
                ("Run DTASelect", self.run_dtaselect_only),
                ("Run All", self.run_all_steps),
            ]
        ):
            ttk.Button(button_row, text=label, command=callback).grid(row=0, column=idx, padx=3)

        self.log = tk.Text(frame, height=12, width=100)
        self.log.grid(row=len(FIELD_ORDER) + 1, column=0, columnspan=3, sticky="nsew", pady=(8, 0))

        self._load_config(ProlucidConfig())

    def _pick_file(self, field_name: str) -> None:
        path = filedialog.askopenfilename()
        if path:
            self.vars[field_name].set(path)

    def _pick_dir(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.vars["output_dir"].set(path)

    def _pick_ms2_files(self) -> None:
        paths = filedialog.askopenfilenames(filetypes=[("MS2 files", "*.ms2"), ("All files", "*.*")])
        if paths:
            self.vars["ms2_files"].set(";".join(paths))

    def _load_config(self, config: ProlucidConfig) -> None:
        values = config.to_dict()
        values["ms2_files"] = ";".join(config.ms2_files)
        for field_name in self.vars:
            self.vars[field_name].set(str(values.get(field_name, "")))

    def _collect_config(self) -> ProlucidConfig:
        return ProlucidConfig(
            java_path=self.vars["java_path"].get().strip(),
            prolucid_jar_path=self.vars["prolucid_jar_path"].get().strip(),
            dtaselect_classpath=self.vars["dtaselect_classpath"].get().strip(),
            fasta_path=self.vars["fasta_path"].get().strip(),
            output_dir=self.vars["output_dir"].get().strip(),
            ms2_files=[item.strip() for item in self.vars["ms2_files"].get().split(";") if item.strip()],
            java_xmx=self.vars["java_xmx"].get().strip(),
            java_thread=self.vars["java_thread"].get().strip(),
            precursor_ppm=self.vars["precursor_ppm"].get().strip(),
            num_isotope=self.vars["num_isotope"].get().strip(),
            min_mass=self.vars["min_mass"].get().strip(),
            max_mass=self.vars["max_mass"].get().strip(),
            protease=self.vars["protease"].get().strip(),
            cleave_residue=self.vars["cleave_residue"].get().strip(),
            enzyme_spec=int(self.vars["enzyme_spec"].get().strip() or "2"),
            max_miss_cleave=self.vars["max_miss_cleave"].get().strip(),
            stat_mod=self.vars["stat_mod"].get().strip(),
            diff_mod=self.vars["diff_mod"].get().strip(),
            n_term_stat_mod=self.vars["n_term_stat_mod"].get().strip(),
            c_term_stat_mod=self.vars["c_term_stat_mod"].get().strip(),
            dta_min_num_peptide=self.vars["dta_min_num_peptide"].get().strip(),
            dta_min_num_tryptic_end=int(self.vars["dta_min_num_tryptic_end"].get().strip() or "2"),
            fdr_level=self.vars["fdr_level"].get().strip() or "protein",
            fdr_filter=self.vars["fdr_filter"].get().strip(),
        ).normalize()

    def _append_log(self, message: str) -> None:
        self.log.insert("end", message + "\n")
        self.log.see("end")
        self.root.update_idletasks()

    def _run_action(self, label: str, action) -> None:
        try:
            self._append_log(f"{label} started")
            result = action()
            if result:
                self._append_log(str(result))
            self._append_log(f"{label} finished")
        except Exception as exc:
            self._append_log(f"{label} failed: {exc}")
            messagebox.showerror("Error", str(exc))

    def load_params(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("ProLuCID params", "*.prolucid_params"), ("JSON", "*.json"), ("All files", "*.*")])
        if not path:
            return
        self._load_config(ProlucidConfig.from_legacy_file(path))
        self._append_log(f"Loaded parameters from {path}")

    def save_params(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".prolucid_params", filetypes=[("ProLuCID params", "*.prolucid_params")])
        if not path:
            return
        self._collect_config().save_legacy_file(path)
        self._append_log(f"Saved parameters to {path}")

    def write_search_xml_only(self) -> None:
        def action() -> Path:
            config = self._collect_config()
            output_dir = Path(config.output_dir or ".")
            return write_search_xml(config, output_dir / "search.xml")

        self._run_action("Write search.xml", action)

    def run_prolucid_only(self) -> None:
        self._run_action("Run ProLuCID", lambda: run_prolucid(self._collect_config()))

    def run_dtaselect_only(self) -> None:
        self._run_action("Run DTASelect", lambda: run_dtaselect(self._collect_config()))

    def run_all_steps(self) -> None:
        self._run_action("Run All", lambda: run_all(self._collect_config()))

    def run(self) -> int:
        self.root.mainloop()
        return 0


def launch_gui() -> int:
    return ProlucidGuiApp().run()
