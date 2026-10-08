#!/usr/bin/env python3
"""Synthetic demo/test data only, not observational astronomy."""
from __future__ import annotations
import argparse
import csv
from pathlib import Path

import numpy as np

from astroplot_style import export_figure, make_figure, publication_style
import matplotlib.pyplot as plt


def create_demo(output_dir: Path, journal: str = "RAA") -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(20261008)
    phase = np.linspace(0.005, 0.995, 200)
    model = 1.0 - 0.065 * np.cos(4 * np.pi * phase) + 0.012 * np.sin(2 * np.pi * phase)
    sigma = np.full(len(phase), 0.008)
    flux = model + rng.normal(0, sigma)
    csv_file = output_dir / "synthetic_lightcurve.csv"
    with csv_file.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["phase", "flux", "flux_err", "model_flux"])
        w.writerows(zip(phase, flux, sigma, model))
    pdf_file = output_dir / "SYNTHETIC_DEMO_NOT_REAL.pdf"
    with publication_style():
        fig, (ax, res) = make_figure(journal, height_ratio=0.95, residual=True)
        try:
            ax.errorbar(phase, flux, yerr=sigma, fmt="o", ms=2, color="#315B72", alpha=0.65,
                        ecolor="#7F91A2", elinewidth=0.5, label="Synthetic observations")
            ax.plot(phase, model, lw=1.2, color="#C06827", label="Synthetic model")
            ax.set_ylabel("Normalized Flux")
            ax.legend(loc="best", frameon=False)
            res.scatter(phase, flux-model, s=6, color="#315B72", alpha=0.65)
            res.axhline(0, color="black", ls="--", lw=0.8)
            res.set_ylabel("O$-$C")
            res.set_xlabel("Orbital Phase")
            fig.text(0.5, 0.992, "SYNTHETIC DEMO — NOT RESEARCH DATA", fontsize=6,
                     ha="center", va="top", color="#8A3636")
            export_figure(fig, pdf_file, dpi=600)
        finally:
            plt.close(fig)
    return csv_file, pdf_file


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", default="examples/generated")
    p.add_argument("--journal", default="RAA", choices=["generic", "AAS", "MNRAS", "A&A", "RAA"])
    args = p.parse_args()
    for file in create_demo(Path(args.output_dir), args.journal): print(file)


if __name__ == "__main__":
    main()
