# Official domain-specific technical references (2026-10-08 snapshot)

These references support **data representation and instrument/software workflow**, NOT all-publisher graphic typography rules. Check versions and applicability to the actual observatory and reduction software. No single website supplies mandatory plotting standards for every astronomy field.

| Domain | Official or primary technical source | Supported use / caveat |
|---|---|---|
| Journal publishing | AAS https://journals.aas.org/graphics-guide/ ; MNRAS https://academic.oup.com/mnras/pages/General_Instructions ; A&A https://www.aanda.org/for-authors/latex-issues/figures ; RAA https://www.raa-journal.org/sub/author/ | production/figure policy; revisit before submission |
| FITS/WCS | Astropy https://docs.astropy.org/en/stable/visualization/wcsaxes/index.html and https://docs.astropy.org/en/stable/wcs/index.html | image sky axes, WCS overlay and transforms |
| Radio/mm interferometry | CASA https://casadocs.readthedocs.io/en/stable/notebooks/image_analysis.html | beam, BUNIT, spectral frames, Stokes, cube/moments/PV; CASA dataset and telescope-specific caveats |
| High-energy fitting | HEASARC XSPEC https://heasarc.gsfc.nasa.gov/docs/software/xspec/manual/XspecManual.html and https://heasarc.gsfc.nasa.gov/docs/software/xspec/manual/node145.html | count, folded, ratio, residual, unfolded spectra and caveats; version-dependent |
| Gamma-ray analysis | Fermi Science Support Center https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/likelihood_tutorial.html | likelihood-based high-energy analysis, not universal gamma threshold rules |
| Solar | SunPy https://docs.sunpy.org/en/stable/generated/gallery/plotting/grid_plotting.html | solar frames and image coordinate overlay |
| Whole-sky | healpy https://healpy.readthedocs.io/en/stable/generated/healpy.visufunc.mollview.html | HEALPix projection, ordering and coordinate controls |
| Gravitational waves | GWOSC https://gwosc.org/tutorials/ and https://learn.gwosc.org/ | strain and time-frequency workflows; examples are educational, not a universal publication policy |
| General graphical design | Rougier et al. (2014) https://doi.org/10.1371/journal.pcbi.1003833 ; Rougier (2021) https://github.com/rougier/scientific-visualization-book | visualization principles and Matplotlib engineering |

When making a claim about instrument conventions, report the exact source, section (when possible), and verification time. Mark if the official page cannot be accessed in the current environment. Do not borrow rules from one telescope and declare them mandatory for all telescopes.
