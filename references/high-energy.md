# X-ray, gamma-ray and high-energy astrophysics — scientific figure protocol

**Evidence:** HEASARC XSPEC documentation distinguishes count, data, ratio, residual, model, unfolded and statistic plots, with energy/channel axes and plot-only rebin options. Fermi Science Support Center documents likelihood products and test statistics. Those analysis details are NOT publisher layout mandates.

## High-energy event lists, imaging and timing

- Name instrument, energy band, exposure and GTI filtering, dead time, event grade/quality selections, event extraction regions and background selection (when relevant). An event list is not an exposure-corrected flux map.
- Image intensity can represent raw counts, counts/s, surface brightness, exposure-corrected intensity, model intensity or significance; never change labels casually. Explain smoothing kernel/adaptive binning and PSF. A raw counts map divided by exposure is **new analysis** needing valid exposure products.
- Light curves: specify energy selection, bin width, exposure/GTI treatment, background, detector dead time and unit. In low-count regimes use suitable counting-statistics errors and state the method; avoid unconstrained Gaussian errors.
- Pulsar folding: barycentric corrections and ephemeris should be verified, including phase zero reference and timing time system. Do not assume phase bin counts are background-subtracted flux.

## X-ray/soft-gamma spectra (PHA/OGIP + RMF + ARF)

- **Never confuse:** PHA channels, detector energy estimates (keV), observed counts/bin, net count rate, folded expected source counts, incident model photon spectrum, unfolded spectrum, absorbed/unabsorbed energy flux and luminosity.
- If plotting fit: data/model in *count space* with correct instrument redistribution response; residuals may be (data-model), data/model, standardized delchi, or fit-statistic contributions. Label exact definition, use the **same grouping/response** as fitted output where appropriate.
- State detector/instrument(s), fitted energy range, background treatment, grouping/binning, exposure, effective area/response (RMF/ARF), fit statistic (e.g. C-stat/W-stat/chi^2) and whether plotted rebin differs from fitting bins.
- `XSPEC plot ufspec` and related variants can be model-dependent: do **not** call an unfolded spectrum an independent set of measured flux points. The current XSPEC documentation also provides response-inversion plot options with their own correlated errors/limitations; record exactly which estimator was used.
- Bins with 0 or negative background-subtracted counts must not silently vanish on a logarithmic axis. Use count-space panels or mathematically justified alternatives, with explicit visible handling.

## Gamma rays and VHE

- Distinguish spectral differential photon flux (photons cm^-2 s^-1 energy^-1), `E^2 dN/dE` energy SED, integrated photon flux and energy flux. Conversions require consistent energy units; do not automatically apply `E²` to unknown CSV columns.
- Each energy bin may be a detection or a one-sided upper limit; preserve confidence level and source-specific threshold logic (likelihood TS, not automatically sigma). Do not attach invented detection limits or TS contours.
- For sky maps include energy band, exposure, PSF, ROI, diffuse/background model, coordinate/WCS reference, and any smoothing or significance mapping convention.
- Periodic high-energy data: trial factors, exposure variation, photon weights, pulsar timing ephemerides and phase assignment require vetted analysis methods.

## Panel and caption templates

- `counts/model/residuals`: top counts or count rate vs energy/channel with forward-folded model; bottom observed−model, ratio or standardized residuals and reference line.
- `gamma_sed`: points/upper-limit arrows with declared confidence levels and energies, a model curve and uncertainty band only if actually computed.
- `xray_image`: WCS sky image, surface brightness units, colorbar, energy range, PSF/exposure processing, region apertures where relevant.
- `energy_time`: energy-time event selection/dynamic spectrum, shared GTIs and explicitly defined color quantity.

“[Instrument] spectrum in [energy band]. Points represent [counts/other observable] grouped by [method] and the line is the response-folded model. Lower panel shows [exact residual definition]. Background and response treatment are [methods]; fit statistic [name].”
