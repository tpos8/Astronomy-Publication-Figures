# Matplotlib engineering notes

## Script design
- Use Matplotlib OO API, keep science analysis separate from presentation and write small deterministic functions.
- Prefer numeric arrays, original IDs, metadata; no mutations or rejection of rows without explicit logged user-approved policy.
- Use `with plt.rc_context(...)`, `fig, ax = plt.subplots(...)`, `GridSpec`, `ax.transAxes`, and stable rcParams.
- Use consistent `zorder`: axes/reference guide (low), dense raw points, uncertainty bars, models, annotations (high). Don't hide real scatter behind opaque model markers.
- Use marker+linestyle+color simultaneously when showing categorical datasets. Do not use single hue to carry all scientific meaning.
- PDF: Matplotlib `pdf.fonttype=42`, `ps.fonttype=42`, PDF for line art; font availability depends on platform, check fallback.
- Plotting data from CSV should operate on existing derived phase/time/flux rather than silently recompute it.

## Actual width and DPI
- 1 inch = 25.4 mm. For width `w_mm`, use `w_in = w_mm / 25.4`.
- Pixel dimensions = final physical size in inches × DPI. Effective DPI in vector PDFs concerns **embedded raster only**, not PDF canvas dpi.
- `savefig(..., bbox_inches='tight')` may change actual output width. Prefer explicit margins when exact column width is essential; audit with PyMuPDF afterwards.
- For thousands of vector points, rasterize dense data artists only: `ax.scatter(..., rasterized=True)`; save with `dpi=600` for embedded data and verify effective resolution at final placed width.

## Installation
```bash
python -m pip install -r requirements.txt
```

## Example CLI
```bash
python scripts/plot_from_csv.py --input results.csv --kind phase_folded --journal MNRAS --x phase --y flux --yerr flux_err --model model_flux --xlabel 'Orbital Phase' --ylabel 'Normalized Flux' --output figures/phase.pdf
python scripts/figure_audit.py figures/phase.pdf --journal MNRAS --format json
```

These scripts are *illustrative presentation infrastructure*. They cannot estimate P, T0, model parameters, uncertainties, GLS FAP, or astrophysical physical truth.
