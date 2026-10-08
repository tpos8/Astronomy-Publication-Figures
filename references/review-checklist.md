# Figure-review rubric and output contract

## First: scientific integrity (manual and source-dependent)
- `[BLOCKER]` Time scales, units, ephemerides, model-versus-observation, uncertainty, normalization, binning, and selection match source code and method? If cannot inspect source/data: `UNKNOWN`, not PASS.
- `[BLOCKER]` Any clipping of important scientifically meaningful data/points? Any invented observations or unsupported significance? Clear disclosure of transformations?
- `[MAJOR]` Series coding, captions, error definitions, limits, legends, residual convention, panel labels, and grouping scientifically interpretable?

## Second: formal production
- `[MAJOR]` PDF one page per figure; correct column width; no clipping; fonts/lines legible at final size; raster images effective DPI adequate.
- `[MAJOR]` Journal-specific file format, numerical guidelines, and alt text when required. Check current online official instructions against snapshot before submission.
- `[MINOR]` Avoid unneeded heavy grid, inconsistent annotations, oversized outer whitespace.

## Third: visual inspection (human or actual rendered images)
- View a rendered print-width PNG, and preferably grayscale/colorblind simulation. Visually confirm legibility of small text, dashed curves, error bars, contours and residuals.
- Review each multi-panel figure panel separately and its placement within the manuscript template.

## Report schema
```yaml
figure: figure.pdf
journal: MNRAS
journal_source: https://academic.oup.com/mnras/pages/general_instructions
scientific_integrity: UNKNOWN # requires data and method
structural_checks: [PASS, WARN]
visual_review: UNKNOWN # unless visually inspected
blocking_issues: []
major_issues: []
minor_issues: []
caption_draft: "..."
alt_text: "Alt text: ..." # mandatory when MNRAS main article
conclusion: "NEEDS_REVIEW" # READY / NEEDS_REVIEW / NOT_READY
```

Do not issue `READY` if manual scientific and visual checks remain unknown. Present hard minimum vs preference distinctly. Any unresolved blockers = `NOT_READY`.

## Domain-aware review gate (v2 multiwavelength)

- `[BLOCKER]` Radio/mm: BUNIT versus physical interpretation (Jy vs Jy/beam vs K), synthesized beam (if relevant), velocity convention/frame, contour provenance, regridding and primary-beam correction.
- `[BLOCKER]` High energy: counts vs detector count rate vs unfolded/incident energy spectrum, response/background/exposure treatment, valid residual and statistic, real detection vs upper limit confidence.
- `[BLOCKER]` Spectra/polarization: air/vacuum and rest/observed wavelength, F_lambda vs F_nu, Stokes convention, masked gaps, signed quantities and debiasing methodology.
- `[BLOCKER]` Solar/CMB/GW: correct coordinate frame, helioprojective observer metadata, HEALPix `NSIDE`/ordering/mask, `C_ell` vs `D_ell`, strain vs ASD vs PSD.
- `[BLOCKER]` Multiwavelength: verified WCS/astrometry, PSF matching and observation epochs before physical comparison; no pixel-coordinate overlays of unmatched maps.
- `[UNKNOWN]` If scientific metadata cannot be checked from source data, report unknown; a caption cannot substitute for verifying the physical model.
- `[MAJOR]` A fully legible, truthful colorbar and contour levels, including negative data when scientifically relevant; accessible non-detection marker legend.

Use `scripts/science_manifest_audit.py` for a sidecar provenance audit, `scripts/inspect_fits.py` to inspect FITS headers, and retain existing `scripts/figure_audit.py` for PDF production checks. Only manual scientific review can resolve domain-validity uncertainty.
