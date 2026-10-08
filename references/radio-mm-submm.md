# Radio, interferometric, mm and sub-mm astronomy — scientific figure protocol

**Evidence:** CASA image analysis documentation covers image headers, beam, brightness units, spectral axes, Stokes metadata, masks, spectral reframing, moment maps and PV products. See source registry. These are discipline/tool conventions, not MNRAS/AAS layout rules.

## Continuum and interferometric imaging

- Display celestial FITS/CASA world coordinates (RA/Dec or Galactic), with appropriate equinox/reference frame; RA orientation follows WCS, not an arbitrary horizontal flip. State observing band/central frequency if relevant.
- Read `BUNIT`, e.g. `Jy/beam`, `mJy/beam`, `Jy/pixel`, `K`, `K km/s`. **Never equate Jy/beam and integrated Jy**. Convert only if aperture/beam geometry and physics are specified.
- Restoring beam ellipse: use `BMAJ`/`BMIN`/`BPA` when the header defines a meaningful beam. Beam position angle is convention-dependent; use WCS-aware beam drawing; if missing, do not invent an ellipse. Pixel scale is NOT the synthesized beam.
- Background RMS/noise from an approved estimator/region; negative contours may be important to diagnose artifacts. Common contour presentations may use n×RMS but **no global n or RMS is mandated by a journal**; cite exact levels and origin. Avoid auto-clipping to positive-only data.
- Preserve CLEAN/deconvolution/multiscale/restored image provenance, weighting (natural/Briggs/uniform), uv-taper, primary-beam correction and mask. Show dynamic range/sidelobes where they matter, not solely visually appealing stretches.
- When comparing data at different angular resolutions, distinguish unconvolved maps from PSF/beam-matched products; smoothing and common-beam convolution are scientific operations, not styling.
- For multi-frequency spectral index maps record alpha convention (`S_nu ~ nu^alpha`), S/N masks, matched uv response/beam when relevant, and propagated uncertainty.

## Spectral cubes: HI/CO/molecular lines

- State rest frequency and whether x is observed frequency or radial velocity. For velocities, identify Doppler convention (radio/optical/relativistic) and spectral frame (LSRK/barycentric/heliocentric/etc.) plus systemic velocity when plotted. Do not silently interchange velocity conventions.
- Document channel width, spectral smoothing, continuum subtraction, mask, primary-beam correction and synthesized beam (possibly channel-dependent).
- Channel maps: labeled velocity/frequency per channel, shared scaling if comparing spatial brightness, beam and colorbar units, physical pixel/WCS geometry.
- Moment 0 (integrated intensity), moment 1 (intensity-weighted velocity), moment 2 (velocity dispersion) carry DIFFERENT units. Never label all of them `Jy/beam` or imply moment-1 is a raw velocity image without its emission mask.
- Position-velocity diagram: state spatial-cut endpoints, slit width, offset unit, velocity convention, noise threshold and how the cut was extracted; no unapproved interpolation.

## Polarization and interferometry

- Stokes I/Q/U/V are signed quantities with instrument convention. Polarization angle and degree require scientifically documented calculation, uncertainties, debiasing, thresholds, calibration; vector angle is ambiguous modulo 180 degrees.
- Differentiate electric-vector position angle from inferred magnetic-field orientation (the latter may involve a 90-degree interpretation depending on radiation process).
- Faraday rotation RM and Faraday depth are not synonyms without physical assumptions. State lambda-squared coverage, RM-synthesis resolution and instrumental polarization limits if relevant.
- uv-coverage/visibility plot: uv distance and units (lambda, k-lambda, Mlambda), baseline, time, weight, amplitude/phase calibration; do not confuse image-plane flux with complex visibility amplitude.

## Suggested panel forms

- Map + WCS grid + colorbar + optional beam + declared +/- contours.
- Cube: aligned channel mosaic with explicit channel labels (do not collapse by default).
- 3-row moment-0/1/2 map with separate units and color scales.
- PV map with explicitly labeled axes and cut location shown on WCS map.
- Polarization: I intensity and overlaid vectors with legend length; optional Q/U panels and error/mask description.

## Example captions

“Restored continuum image at [frequency] in [BUNIT] with contours at [explicit levels] calculated from a measured rms of [value] in [region]. The beam ([BMAJ] × [BMIN], PA [BPA]) is shown at lower left. The image is [PB-corrected/not] and has [WCS frame].”

“Integrated [line] intensity map using [velocity channels] with [mask]; colorbar is [integrated units]. Velocity reference is [radio/optical/relativistic] in [frame].”
