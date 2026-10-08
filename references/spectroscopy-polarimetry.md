# IR/optical/UV spectroscopy, imaging and polarization

## Spectroscopy

- State the wavelength unit, **vacuum vs air** convention, rest-frame vs observed-frame spectrum, barycentric or other velocity correction, redshift, resolution (R or FWHM) and spectral extraction aperture/slit when relevant.
- Preserve `F_lambda` vs `F_nu` vs normalized flux. `F_lambda` and `F_nu` cannot be interchanged by relabeling; conversions require wavelength/frequency and valid units. Distinguish absolute flux-calibrated from continuum-normalized spectra.
- Spectral line panels: mark transitions from verified wavelengths, account for air/vacuum and redshift, show line profiles/continuum model/residuals; line equivalent width, velocity dispersion and uncertainties should come from fitted/derived products, not graphics heuristics.
- Telluric absorption, sky-line masks, chip gaps, saturation, blaze correction, resampling and variance spectrum treatment must be documented. Never silently interpolate across masked wavelengths.
- Log wavelength / flux axes are acceptable only where representation remains meaningful; spectra with negative flux from background subtraction need explicit handling rather than disappearing on log plots.

## IR / optical / UV imaging and photometry

- Show WCS celestial axes, passband, exposure and photometric flux/brightness units; declare stretch and clipping. False-color RGB images are **composites**, not literal physical-color observations; state channel-to-filter mapping and nonlinear stretch.
- When multi-filter morphology is compared, register astrometry, PSFs, sky background and epoch differences. Distinguish a PSF FWHM from a radio synthesized restoring beam.
- Difference images and significance maps must be identified as such, including difference sign, reference epoch, masking, detection metric and artifacts. Magnitude axes may run brighter-up (inverted) only when explicitly labeled.
- Extinction-corrected vs observed photometry and AB/Vega/ST photometric systems cannot be silently mixed.

## Spectropolarimetry

- Stokes I,Q,U,V, linear polarization fraction and angle, uncertainties/covariance, polarization bias correction and sign conventions must be verified.
- Polarization degree and position angle versus wavelength: angle wrapping and 180-degree ambiguity, instrumental polarization, S/N cuts and wavelength calibration can materially affect conclusions.
- Always distinguish detected polarization from confidence-based upper limits.

## Useful layouts

Spectrum + error trace + line markers + fitted continuum/line model + residual panel; per-band image grid at matched angular resolution; Stokes/polarization multi-panel plot; spectroscopic time series with actual cadence, not interpolated bands.
