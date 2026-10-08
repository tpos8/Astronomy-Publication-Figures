# Astronomy figure protocols — scientific safeguards

Apply common publication style, but do not let aesthetics alter scientific quantities. For each figure, identify the **science question, axes + units, source data, treatment, uncertainty, model convention and caption text**.

## `light_curve` — temporal flux/magnitude
Input `time, flux` plus optional `flux_err`, sector IDs, quality flags, calibrated/normalized series. Record TESS PDCSAP vs SAP and QUALITY filtering *only if actually performed*. Require BJD_TDB/BTJD/MJD or another explicit timescale and offsets (e.g. BTJD=BJD−2457000). Show gaps honestly; do not connect across detector/sector gaps with smooth lines unless model independently predicts them. Magnitudes may have reversed y-axis only if scientifically appropriate and labeled. For multiple sectors use legend/panel/offset description; explicitly show `flux+offset` if offset applied.

## `phase_folded` — orbital phase
Input approved phase column preferred, OR compute with user's specified ephemeris formula and parameters; don't assume `phase = frac((t-T0)/P)` when Pdot or eccentric timing applies. State phase range `[0,1)` or `[-0.5,0.5)` and period interpretation (`P_orb` versus `P_phot=P_orb/2`). If plotting phase twice, say why. Raw and binned traces have distinct marks; error bar means STD vs SEM vs propagated errors. Confirm time system and phase-zero event (conjunction, eclipse, ascending node). Multi-sector offset must be explicit.

## `periodogram` — GLS/Lomb–Scargle
Require x-axis period or frequency (units) and sampling/grid range. Identify normalization and model/weights, explain false-alarm threshold calculation (bootstrap/analytic) if shown; never draw invented confidence lines. Note aliases/window function and limits. Plot apparent `P/2` carefully; don't label it the orbital period without independent evidence.

## `rv` — radial velocities
x usually time or orbital phase with stated zero point. y = RV (km s^-1) with per-observation errors. Distinguish instruments using shapes; model in line; optionally mark systemic velocity gamma. Residual panel should use stated `O−C` convention and velocity units. Eccentric solution should not silently be treated as sine wave. Don't extrapolate beyond data unless requested and marked.

## `sed` — spectral energy distribution
Require wavelength/frequency system and flux density units (e.g. Jy vs erg s^-1 cm^-2 Å^-1). Separate band-integrated photometry, upper limits, synthetic photometry and continuous model spectra. Align extinction/reddening assumptions and zero points; meaningful log axes where appropriate. Error bars must represent actual measurement/model uncertainties; upper limits are directional symbols, not detections.

## `phoebe` — forward light-curve model
Keep observed points, predicted light curve and signed residuals separate. Declare physical assumptions: shared inclination vs sector-specific spots/offsets/noise; any fitted phase shift, normalization, third light, limb darkening. If a model or data is offset for display, the offset is not part of physics unless explicitly modeled. Show unmatched morphology rather than cosmetically fixing it. Record likelihood/noise and fitted interval where relevant.

## `corner` — posterior distributions
Label parameters and units; show stated quantiles/HPD and priors if shown. Distinguish posterior samples from optimization errors; don't claim 68% credible contours unless actually calculated. MCMC convergence / autocorrelation / effective sample diagnostics belong in analysis; failing diagnostics should be disclosed rather than hidden by plot styling.

## `oc` — timing residuals
State reference linear/quadratic ephemeris, standard units (s or d), and whether O−C values share same time scale. Error bars and correlated timing uncertainties if relevant. Trend model must be labeled as model, not raw measurements.

## `fits_wcs` — images / images with contours
Plot with Astropy WCS if sky coordinates; include RA/Dec, scale, orientation, beam/PSF when applicable. State stretch (linear/log/asinh), colormap, exposure, processing, colorbar units and limits. Use perceptually sensible colormaps and visible source masks. Don't add missing sources, recolor in a way that implies different data, or omit saturation description.

## Caption template (adapt—not literal mandatory wording)
"[Panel assignments]. [Data source, units, and measurement treatment]. [Meaning of points, lines, shades, and uncertainties]. [Period/T0/timescale or fit parameters if relevant]. [Residual sign, offset, and binning policy]."

## Alt-text template for MNRAS
"Alt text: [Number of panels, axes and ranges]. [Main rising/falling pattern]. [Data-vs-model visual comparison]. [Large deviations or outliers relevant to reading the figure]." Keep concise and informative; do not just repeat the caption or invent trends.

## Cross-disciplinary extension (v2)

The preceding photometric, RV, SED and FITS recipes are **one subset** of astronomy, NOT the complete Skill scope. Route high-energy count spectra, radio interferometry, spectral cubes, Stokes/RM maps, solar projections, HEALPix maps and GW spectrograms via `domain-router.md` and the corresponding specialist references. Do not use the optical SED defaults for photon-count spectra, or a generic 2D WCS image helper to slice a radio cube without specified axes. For physical representation distinctions, consult `multiwavelength-crosschecks.md`.
