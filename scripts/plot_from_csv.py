#!/usr/bin/env python3
"""Produce visualizations from already-processed CSV columns. Never performs science transformations."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from astroplot_style import export_figure, make_figure, publication_style, load_profile

KIND_AXES = {
    "light_curve": ("Time [specify timescale]", "Flux [specify units]"),
    "phase_folded": ("Orbital Phase", "Normalized Flux"),
    "rv": ("Orbital Phase", r"Radial Velocity (km s$^{-1}$)"),
    "periodogram": ("Period [specify units]", "Periodogram Power"),
    "sed": (r"Wavelength ($\AA$)", "Flux density [specify units]"),
    "oc": ("Epoch", "O-C [specify units]"),
    "spectrum": ("Wavelength / Frequency [specify convention and units]", "Flux density [specify units]"),
    "radio_spectrum": ("Frequency / Velocity [specify frame and units]", "Brightness [specify units]"),
    "visibility": ("uv distance [specify lambda units]", "Visibility amplitude [specify units]"),
    "xray_spectrum": ("Energy / Channel [specify units]", "Counts / Rate [specify observable and units]"),
    "gamma_sed": ("Energy [specify units]", "Spectral energy quantity [specify units]"),
    "polarization": ("Wavelength / Frequency [specify units]", "Stokes / polarization quantity [specify units]"),
    "solar_profile": ("Distance / Time [specify units]", "Solar intensity / field [specify units]"),
    "gw_asd": ("Frequency (Hz)", "Strain ASD [specify units]"),
    "cmb_power": ("Multipole ell", "C_ell or D_ell [specify and include units]"),
    "theory": ("X [specify units]", "Y [specify units]"),
}


def read_numeric_columns(path: Path, column_names: list[str]) -> dict[str, np.ndarray]:
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [c for c in column_names if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Missing CSV columns: {missing}; available columns: {reader.fieldnames}")
        cols = {key: [] for key in column_names}
        for i, row in enumerate(reader, start=2):
            for key in column_names:
                try:
                    v = float(row[key])
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"Non-numeric CSV value in row {i}, column {key!r}; decide on treatment explicitly") from exc
                if not np.isfinite(v):
                    raise ValueError(f"Non-finite value in row {i}, column {key!r}; no rows discarded automatically")
                cols[key].append(v)
    if not cols or not next(iter(cols.values())):
        raise ValueError("Input CSV has no rows")
    return {key: np.asarray(value, dtype=float) for key, value in cols.items()}


def draw_series(ax, x, y, *, yerr=None, model=None, residual_ax=None, kind="light_curve", upper_mask=None, limit_label=None) -> None:
    if yerr is not None and np.any(yerr < 0):
        raise ValueError("Negative measurement uncertainties are invalid")
    if upper_mask is None:
        upper_mask = np.zeros(len(x), dtype=bool)
    if len(upper_mask) != len(x):
        raise ValueError("Upper limit flag length does not match data")
    if np.any(upper_mask) and not limit_label:
        raise ValueError("Upper-limit values require --limit-label with a scientifically verified confidence level")
    if kind == "periodogram":
        if model is not None or residual_ax is not None or yerr is not None or np.any(upper_mask):
            raise ValueError("Periodogram models, FAP thresholds and uncertainties require a science-specific implementation")
        order = np.argsort(x, kind="stable")
        ax.plot(x[order], y[order], color="#315B72", lw=1.0, label="Supplied periodogram")
        ax.legend(frameon=False, loc="best")
        return
    detected = ~upper_mask
    if yerr is not None and np.any(detected):
        ax.errorbar(x[detected], y[detected], yerr=yerr[detected], fmt="o", ms=2.0, color="#315B72",
                    ecolor="#7F91A2", elinewidth=0.6, capsize=0,
                    alpha=0.72, label="Measurements", zorder=2)
    elif np.any(detected):
        ax.scatter(x[detected], y[detected], s=5.0, marker="o", color="#315B72", alpha=0.72,
                   rasterized=np.sum(detected) > 6000, label="Measurements", zorder=2)
    if np.any(upper_mask):
        # The y-value is the stated limit. Shape distinguishes nondetections; no fake error length.
        ax.scatter(x[upper_mask], y[upper_mask], s=22, marker="v", facecolors="none",
                   edgecolors="#B45439", linewidths=1.0, label=f"Upper limit ({limit_label})", zorder=3)
    if model is not None:
        # Sorting only sets drawing order of an *already supplied* model; it changes no values.
        order = np.argsort(x, kind="stable")
        ax.plot(x[order], model[order], color="#C06827", lw=1.2, ls="-",
                label="Supplied model", zorder=4)
        if residual_ax is not None:
            residual = y[detected] - model[detected]  # Only detections: limits are censored values.
            if yerr is not None:
                residual_ax.errorbar(x[detected], residual, yerr=yerr[detected], fmt="o", ms=1.8,
                    color="#315B72", ecolor="#7F91A2", elinewidth=0.5,
                    alpha=0.7, capsize=0)
            else:
                residual_ax.scatter(x[detected], residual, s=4, color="#315B72", alpha=0.7,
                                    rasterized=np.sum(detected) > 6000)
            residual_ax.axhline(0, lw=0.8, color="#333333", ls="--", zorder=1)
            residual_ax.set_ylabel(r"O$-$C (km s$^{-1}$)" if kind == "rv" else "O$-$C")
            residual_ax.tick_params(which="both", direction="in", top=True, right=True)
    ax.legend(frameon=False, loc="best")


def build(args) -> list[Path]:
    load_profile(args.journal)
    fields = [args.x, args.y]
    fields += [x for x in (args.yerr, args.model, args.upper_limit_flag) if x is not None]
    data = read_numeric_columns(Path(args.input), list(dict.fromkeys(fields)))
    if args.residual and not args.model:
        raise ValueError("--residual requires --model")
    if args.kind not in KIND_AXES:
        raise ValueError(f"Unknown figure kind: {args.kind}")
    if args.kind in {"radio_spectrum", "visibility", "xray_spectrum", "gamma_sed", "polarization", "solar_profile", "gw_asd", "cmb_power", "theory", "spectrum"} and (not args.xlabel or not args.ylabel):
        raise ValueError(f"{args.kind} requires explicit --xlabel and --ylabel to prevent assumed science units")
    upper = None
    if args.upper_limit_flag:
        flags = data[args.upper_limit_flag]
        if not np.isin(flags, [0,1]).all():
            raise ValueError("Upper limit flag column must contain exactly 0 for detection or 1 for upper limit")
        upper = flags.astype(bool)
        if upper.any() and not args.limit_label:
            raise ValueError("Upper limits require --limit-label, e.g. '95% CL', from analysis")
    explicit_domain = getattr(args, 'domain', None)
    default_domains = {"xray_spectrum":"xray", "gamma_sed":"gamma", "radio_spectrum":"radio", "visibility":"radio", "gw_asd":"gravitational_wave", "solar_profile":"solar", "cmb_power":"cosmology", "phase_folded":"optical", "rv":"optical", "oc":"optical"}
    figure_domain = explicit_domain or default_domains.get(args.kind, "unspecified")
    def_x, def_y = KIND_AXES[args.kind]
    with publication_style():
        fig, (ax, res) = make_figure(args.journal, width_mm=args.width_mm,
                                    height_ratio=(0.95 if args.residual else 0.75), residual=args.residual)
        try:
            draw_series(ax, data[args.x], data[args.y],
                        yerr=data.get(args.yerr), model=data.get(args.model),
                        residual_ax=res, kind=args.kind, upper_mask=upper, limit_label=args.limit_label)
            ax.set_ylabel(args.ylabel or def_y)
            (res if res is not None else ax).set_xlabel(args.xlabel or def_x)
            if args.loglog:
                if np.any(data[args.x] <= 0) or np.any(data[args.y] <= 0):
                    raise ValueError("Log scales require positive x and y; do not discard non-positive rows")
                ax.set_xscale("log")
                ax.set_yscale("log")
                if res is not None: res.set_xscale("log")
            output = Path(args.output)
            produced = export_figure(fig, output, png_preview=not args.no_preview, dpi=args.dpi)
            metadata = {
                "kind": args.kind, "figure_kind": args.kind, "journal": args.journal, "input": str(args.input),
                "domain": figure_domain,
                "source_files": [str(args.input)], "representation": "preprocessed supplied numeric data",
                "units": args.ylabel, "processing": ["No scientific processing; optional O-C only for detected supplied points"],
                "upper_limits": {"flag_column": args.upper_limit_flag, "confidence_label": args.limit_label} if args.upper_limit_flag else None,
                "input_columns": {"x": args.x, "y": args.y, "yerr": args.yerr, "model": args.model, "upper_limit_flag": args.upper_limit_flag},
                "n_points": len(data[args.x]), "transformations": ["none; retained raw CSV numeric values"],
                "derived_display_values": (["O-C = observed - supplied model"] if args.residual else []),
                "notes": ["Printed column width is audited separately.",
                          "Flux/error/phase/time provenance must be verified from source data."],
                "outputs": [str(p) for p in produced],
            }
            output.with_suffix(".plot-manifest.json").write_text(
                json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        finally:
            plt.close(fig)
    return produced


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True)
    p.add_argument("--kind", choices=sorted(KIND_AXES), required=True)
    p.add_argument("--domain", help="Research domain for provenance; never inferred from generic spectra or SED")
    p.add_argument("--journal", default="generic", choices=["generic", "AAS", "MNRAS", "A&A", "RAA"])
    p.add_argument("--x", required=True, help="Name of already-derived x column")
    p.add_argument("--y", required=True, help="Name of already-derived y column")
    p.add_argument("--yerr", help="Name of uncertainty column (optional)")
    p.add_argument("--model", help="Name of already-computed model column (optional)")
    p.add_argument("--upper-limit-flag", help="Column with 1=upper limit (not a detection), 0=detection")
    p.add_argument("--limit-label", help="Verified confidence definition for limits, e.g. '95% CL'")
    p.add_argument("--residual", action="store_true", help="Show O-C panel, needs model")
    p.add_argument("--xlabel", help="Use explicit physics label with time standard and units")
    p.add_argument("--ylabel", help="Use explicit physics label with units")
    p.add_argument("--loglog", action="store_true", help="Require positive x/y; presentation only, does not discard data")
    p.add_argument("--width-mm", type=float, help="Manual override after verifying journal column width")
    p.add_argument("--dpi", type=int, default=600)
    p.add_argument("--output", required=True, help=".pdf, .eps, .svg or .png")
    p.add_argument("--no-preview", action="store_true")
    args = p.parse_args()

    files = build(args)
    for file in files: print(file)


if __name__ == "__main__":
    main()
