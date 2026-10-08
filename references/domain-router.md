# Domain and representation router

**First choose the physically meaningful axes, product and method, then a style.** The same instrument may produce an image, cube, time series, event table, polarization map, power spectrum or likelihood map. Journal instructions govern printed figures; instrument/software documentation governs domain-specific scientific conventions. See `source-registry.md`.

| Trigger | Domain | Common plot type | Required metadata | Fail-safe |
|---|---|---|---|---|
| VLA/VLBI/ALMA, continuum, interferometric sky map | radio, mm/submm | WCS intensity, contours, beam, spectral index | BUNIT, beam, freq, noise, WCS | no inferred beam/contours |
| HI/CO cube, channel map, moment 0/1/2, PV | radio/mm spectral line | 3-D slice, moments, PV diagram | rest frequency, frame, definition, channel width, mask, beam | do not auto-collapse |
| Stokes I/Q/U/V, RM | radio/optical/X-ray polarimetry | Stokes panel, angle vectors, fractional polarization | convention, debiasing, uncertainty, angle frame | no computed vectors from unknown Stokes |
| X-ray OGIP PHA/RMF/ARF | high energy | counts/keV and forward-folded model + residuals | response, background, exposure, grouping, fit statistic | no unfolded-flux claim |
| LAT/TeV likelihood | gamma | SED, TS map, localization, upper limits | bin definition, exposure, energy units, TS/CL | no fabricated threshold |
| UV/optical/NIR spectrum | spectroscopy | F_lambda or F_nu vs lambda, lines, EW | vacuum/air, rest/observed, calibration, resolution | no silent continuum normalize |
| TESS/Gaia/ground photometry | time domain | LC, phase-fold, periodogram | time standard, zero epoch, filters, flags | no inferred phase |
| Solar EUV/XUV/HMI | heliophysics | SunPy map, loops, coordinate grids | observer, solar frame, passband, date | no generic RA/Dec labels |
| CMB HEALPix | cosmology | Mollweide skymap, power C_ell / D_ell | ordering, frame, masked pixels, units | no automatic monopole/dipole removal |
| LIGO/KAGRA/Virgo | GW | strain vs time, spectrogram, ASD/PSD | sampling, whitening, window, units, calibration | don't imply ASD=PSD |
| Neutrino/localization | multi-messenger | probability skymap, credible regions | coordinate frame, normalized posterior, CL, epoch | no invented credible area |
| Spacecraft planetary maps, mission observations | planetary | surface map, mineral spectra, I/F, shape map | body frame, lat/lon convention, epoch, incidence angle | no Earth-like map assumptions |
| Gaia/stellar catalogs/proper motions | astrometry | CMD, proper motions, survey footprint | reference epoch, parallax distance model, covariance, frame | do not invert uncertain parallaxes blindly |
| Simulations / theoretical parameter spaces | theory | profiles, phase spaces, likelihood, corner | dimensionless or physical units, model snapshot, priors | simulation not observation |
| Multi-band overlays | multiwavelength | registered multi-band color/contours; SED | WCS, PSFs, epochs, units, non-detections | no arbitrary pixel overlay |

## Routing procedure

1. Inspect file format and metadata before guessing. A FITS file might be 1-D spectrum, 2-D detector array, 3-D PPV cube, or multi-extension event product.
2. Distinguish *visualization* from *new physical analysis*. If science pipeline parameters are missing, avoid deriving products; continue safe display of approved outputs.
3. Load only relevant specialized references plus `journal-standards.md` and `design-principles.md`; load several specialized documents for cross-domain plots.
4. Record quantities, units, data/statistical treatment, selection, instrument and reference frame in a sidecar manifest for the audit.
5. If uncertainty about the convention can affect a physical conclusion, mark BLOCKER and request the missing source metadata rather than auto-filling common values.
