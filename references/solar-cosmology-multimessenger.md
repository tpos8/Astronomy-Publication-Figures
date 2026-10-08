# Solar physics, cosmology, theoretical astronomy, gravitational waves and other messengers

## Solar/heliophysics (SunPy-oriented)

- Interpret FITS/SunPy observer metadata, Helioprojective Cartesian vs heliographic Stonyhurst/Carrington frames, reference obstime and solar disk geometry. Labels may be arcsec from disk center, heliographic longitude/latitude, etc.; **do not replace with RA/Dec by convention**.
- Wavelength/passband and instrument (SDO/AIA/HMI, Solar Orbiter, etc.), radiance/counts, exposure-normalized intensity, solar image degradation/projection and time alignment must be declared.
- Space-time stackplots require precisely defined slit/path and distance along slit vs elapsed time; differential rotation or coalignment is a scientific transformation needing provenance.
- Magnetograms: signs and units (e.g. Gauss) with diverging color scale around physically meaningful zero; line-of-sight vs vector field must be distinguished.

## Cosmology / CMB / large-scale structure

- For HEALPix maps, specify `NSIDE`, RING/NESTED ordering, frame (Galactic/equatorial/ecliptic), projection/handedness, masks and pixel-weight/beam smoothing; do not treat flattened HEALPix arrays as 2-D Cartesian FITS images.
- Temperature anisotropy map units (K/mK/uK_CMB), CMB monopole/dipole removal and foreground cleaning (if any) are scientific procedures, not display defaults. Label exact maps and masks.
- Angular power spectrum: distinguish `C_ell` from `D_ell = ell(ell+1) C_ell/(2π)`, polarization TT/TE/EE/BB spectra, cosmic variance and instrumental/noise corrections; never convert by relabeling.
- Galaxy maps, clustering and luminosity functions: redshift limits, survey mask/completeness, cosmological parameters, comoving/physical dimensions and h factors (Mpc vs Mpc/h) must be explicit.
- Simulation products: record cosmology, code/snapshot, resolution, scale, projection, transfer function and the fact that figures are simulated.

## Gravitational waves (GWOSC/GWpy-oriented)

- `h(t)` is dimensionless strain, not strain ASD. Label time relative to GPS epoch/UTC with explicit conversion; detector H1/L1/V1/K1 and calibration release as appropriate.
- Spectrograms/Q-transforms: frequency range, sample rate, time-frequency window/transform, normalization, whitening and color units must be stated. A log-frequency scale does not imply log-amplitude.
- Distinguish one-sided PSD (strain²/Hz) and ASD (strain/sqrt(Hz)), characteristic strain and signal-to-noise. Do not fabricate chirp patterns or confidence estimates.
- For Bayesian localization sky maps show posterior density/probability and explicitly computed credible regions (e.g. 50/90%); no guessed area or unverified overlay with electromagnetic transients.

## Neutrino, cosmic rays and multi-messenger

- State angular uncertainty, localization probability treatment, event times/frames, exposure and direction reconstruction conventions; declination-dependent sensitivity and trials effects matter.
- Energy spectra: effective exposure/acceptance, differential vs integral flux, energy calibration and upper-limit CL; `E² Phi` is not the same as differential flux.
- Cross-correlation or lag plots require time conventions and causal/statistical interpretation, not visual alignment of arbitrarily shifted timelines.

## Theory and simulations

- Use natural/physical units consistently (G=c=1, geometrized, SI, solar units). Record plotted dynamical variables, model inputs, timestep, numerical convergence tests, priors and chosen normalization.
- Parameter scans with masked/unphysical regions must preserve and identify masks; don't fill gaps by extrapolation merely to produce smooth contours.
