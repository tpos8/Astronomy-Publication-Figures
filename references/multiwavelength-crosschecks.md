# Multiwavelength and cross-observatory scientific integrity

Cross-band figures are often most scientifically dangerous because each field uses different units, coordinates and response assumptions.

## Seven checks before combination

1. **Position/frame:** WCS and equinox/epoch, source astrometry, proper motions, different observer frames; reproject maps only with specified algorithm. Pixel-to-pixel overlays without WCS verification are a BLOCKER.
2. **Angular resolution:** beam vs PSF, convolution and pixel scales; record if morphology is matched at a common resolution. Do not compare peak brightness of maps with different beams as if directly equivalent.
3. **Time:** observational epochs, barycentric/geocentric/mission corrections, time precision; simultaneity must be reported rather than implied.
4. **Spectral quantity:** F_lambda vs F_nu vs photon flux vs energy flux vs brightness temperature vs counts; explicit integration band, bandwidth and calibration.
5. **Sensitivity/selection:** detection, upper limits, confidence levels, flux completeness, heterogeneous noise and sky coverage; never turn limits into points with symmetric error bars.
6. **Instrument response:** bandpasses, zero points, extinction/absorption, RMF/ARF, primary beam or throughput; transformations need physically justified models.
7. **Statistics:** independent errors vs correlated calibration systematics, covariance, model uncertainty, censored likelihoods and multiple-testing correction.

## Visualization patterns

- Matched-resolution multi-band cutouts: shared sky geometry, per-band scale bars, colorbars with true units, filters/frequencies/energies as panel labels.
- Cross-band SED: observational points, limits, and model curves clearly separated; indicate measurement units and spectral convention (nu F_nu, lambda F_lambda, E² dN/dE) and valid conversion method.
- Multi-messenger timeline: explicitly marked mission detector epochs and uncertainties; do not infer delay causality from plotted shifts.
- Image + contours: contours reprojected using WCS transformation; include contour levels, map units, noise sources, PSF/beam information and registration limitations.

## Labeling template

“[Band/data product] observed by [instrument] on [date] in [physical units]. Astrometry/beam has [been / not been] matched using [specified procedure]. Upper limits are [confidence]. Color scale and contours show [distinct quantities], not common physical units unless calibrated.”
