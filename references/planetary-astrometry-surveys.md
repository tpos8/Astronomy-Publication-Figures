# Planetary science, astrometry, catalog surveys and stellar dynamics

## Planetary and Solar System surfaces

- Planet-centered coordinates are **not automatically Earth-like**. State body, IAU frame, positive-east/positive-west longitude convention, latitude type (planetocentric vs planetographic), reference ellipsoid, map projection, prime meridian and epoch; verify mission camera/image geometry and spacecraft geometry against the source pipeline.
- Map image scales may be km/pixel, angular resolution, radiance (I/F), reflectance, temperature or spectral index; do not label a physically calibrated map as ordinary RGB color when it is a false-color multispectral composite.
- Annotate phase angle, incidence/emission angles, subsolar/subobserver geometry when relevant; map projection can distort area or distance, so use correct geodesic/angular scales.
- Spectral cubes, mineral abundance maps, thermal maps and crater densities need processing/photometric calibration provenance; do not apply unrecorded photometric corrections or project lat-long coordinates as an image with equal pixel areas.
- Spacecraft/planet ephemerides require explicit time and reference frames (ICRF/IAU body-fixed etc.). Surface features can appear mirrored if east/west is assumed incorrectly.

## Astrometry and survey visualizations

- Proper motion: mas/yr, epoch, RA* = mu_alpha cos(delta) distinction, covariance and reference frame. Gaia sources may have correlated astrometric errors; don't apply scalar error bars to transformed coordinates without uncertainty propagation.
- Parallax vs inferred distance must remain distinct, including negative parallax measurements where valid. Do not simply invert low-SNR parallax without a model.
- Color-magnitude diagrams: magnitudes vs colors, extinction and zero point and magnitude-axis orientation documented; distance modulus, membership selection and completeness cuts matter.
- Survey footprints/selection functions: masks, limits, field boundaries, HEALPix resolution where used, selection bias and spatial coordinates.
- Position/velocity diagrams and orbital kinematics: Galactocentric/heliocentric/LSR conventions, line-of-sight versus 3D velocities, coordinate transforms and Solar motion assumptions.

## Theory and computational dynamics

- Clearly identify simulation vs observation; energy/angular momentum error diagnostics, time stepping, particle sampling, softening length, convergence and normalization.
- Histograms vs density estimators, uncertainty bands and priors depend on sample weights and effective selection function; avoid visual features created by smoothing bandwidth.
