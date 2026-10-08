# Scientific figure design sources and actionable rules

## A. Ten Simple Rules for Better Figures
Rougier, N. P., Droettboom, M., & Bourne, P. E. (2014), *PLOS Computational Biology* 10(9): e1003833. DOI: https://doi.org/10.1371/journal.pcbi.1003833 (authoritative full text: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833).

Translated and operationalized (not quotes from the paper):
1. **Know your audience**: For reviewers/astronomers, expose data values, axes, uncertainties, assumptions; for talks simplify and enlarge.
2. **Identify your message**: One central scientific claim per figure; secondary checks in subtables or lower panels.
3. **Adapt to support medium**: Design at final print width; separate larger-font slide version if requested.
4. **Captions are not optional**: Define all symbols, models, uncertainty bands, phase/time conventions, color encoding, panel distinctions.
5. **Do not trust defaults**: Explicitly control fonts, axes, scales, line weights, markers, color, and margins. Preserve comparison fairness.
6. **Use color effectively**: Sequential for ordered magnitudes, diverging for meaningful center/zero, qualitative for categories; combine color with markers/linestyles.
7. **Do not mislead**: Never cherry-pick y limits, remove uncertainty, distort comparisons, or conceal processing. Explain binning/clipping/normalization.
8. **Avoid chartjunk**: Restrict visual elements to those carrying information; no gratuitous 3D/shadow/overgrid.
9. **Message trumps beauty**: Better a correct noisy scatter than a cosmetically smoothed, misleading figure.
10. **Get the right tool**: Use appropriate packages (Astropy WCS/Lightkurve/PHOEBE/Matplotlib/corner) without reimplementing validated science.

For a review, use the rules as **scientific and visual judgment prompts**, not automatic numeric tests.

## B. Scientific Visualization: Python + Matplotlib
Nicolas P. Rougier (2021), open access book and source code: https://github.com/rougier/scientific-visualization-book

Implement its architectural lessons instead of copying plots or book text:
- **Figure anatomy / Artist hierarchy**: use Matplotlib object-oriented API with named `fig`, `ax`; avoid hidden global pyplot state in multi-panel figures.
- **Coordinate systems**: choose `ax.transAxes` for stable panel labels, `ax.transData` for physical markers, `fig.transFigure` for cross-panel placement.
- **Scales & projections**: verify linear/log/symlog scales preserve scientific meaning and mark zero, limits, and units.
- **Typography**: consistent physical units, math italic variables vs upright units and function names, embedded fonts, readable at final width.
- **Color**: perceptual luminance and accessibility, use purpose-specific maps and explicit colorbars with units.
- **Matplotlib styling**: context-managed rcParams and journal profile rather than repeated arbitrary changes across plots.
- **Size/layout**: actual figure inches from mm, GridSpec for unequal residual panel heights, constrained layout with final PDF width audit.
- **Annotations**: legends, arrows, zoom insets, reference lines only for substantive scientific meaning.
- **Optimization**: selective rasterization for dense marks, not for text/model lines; audit embedded DPI and PDF file size.
- **Animation and 3D**: optional specialized medium, not default for publication plots; static publication view remains necessary where required.

## Directly actionable acceptance questions
- Can a reviewer infer *what every observed point, fitted line, and shaded interval means* without guessing?
- Could a color-blind/grayscale reader still distinguish series?
- Could a change in y range, bin size, or ephemeris change the perceived conclusion? If yes, explicitly document and scientifically justify.
- Is the result inspectable in a single-column paper PDF at final size?
- Is the underlying plotting and data-processing pipeline reproducible and archived?
