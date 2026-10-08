# Journal-specific figure policies — source-traceable snapshot

Checked: 2026-10-08. **Do not pass these as permanent rules**; consult links before manuscript submission. `MANDATORY` is a quoted requirement or definite instruction in the official source; `OFFICIAL_ADVICE` is publisher advice; `HOUSE_DEFAULT` is not journal policy. Measurements refer to **final placed size**, not only the dimensions of source files.

## AAS (ApJ / AJ / ApJS etc.)
Official: https://journals.aas.org/graphics-guide/

- `OFFICIAL_ADVICE` vector EPS/PDF for figure submissions; PNG/JPG/TIFF are also acceptable.
- `MANDATORY` raster files should yield at least 300 DPI in the final PDF; guide also describes a minimum 1000 horizontal pixels for a suitable figure file.
- `MANDATORY` each figure file is one page; split multi-page PDFs/EPS.
- `MANDATORY/ACCEPTED_THRESHOLD` minimum type as small as 6 pt is acceptable; minimum line width 0.5 pt; both must survive reduction. These are limits, **not optimal house font size**.
- `OFFICIAL_ADVICE` match symbol size to typography, line weight to font; distinguish dashed/dotted at small size. Don't rely on color alone; add differing line styles/marker shapes/hatches; support grayscale and color-vision deficiencies.
- `MANDATORY` animated/interactive figures must have static 2D representation; special submission workflow. Read full guide before creating them.
- `HOUSE_DEFAULT` use 8 pt+ where feasible, 0.8 pt axes, 1.1 pt science lines; specific column width comes from paper class, not invented AAS universal.

## MNRAS
Official: https://academic.oup.com/mnras/pages/general_instructions (sections 2.4 and 5.3; Alt Text under section 2.4)

- `MANDATORY` figures numbered and cited in order with suitable captions, axis labels with units as applicable.
- `OFFICIAL_ADVICE` vector for plots, high-quality raster for images; EPS preferred; PDF/TIFF acceptable.
- `MANDATORY` all graphics line weight not less than 0.3 pt **at final size**; don't use complicated triple-dot-dash style.
- `OFFICIAL_ADVICE` plotted labels around **8 pt** at final size; illustrative single column = **84 mm**. **8 pt is guidance, not a hard-coded universal minimum.**
- `OFFICIAL_ADVICE` general bitmap elements at effective 400 dpi or greater; TIFF grayscale/halftone 300 ppi and TIFF mixed line/tone 800 ppi at final size. This is *type-dependent*: do not misreport as single universal 800 dpi mandate.
- `MANDATORY` EPS should have embedded fonts and proper bounding box; author-supplied labels (a)/(b) in image, one figure per file; don't distort aspect ratio using LaTeX.
- `OFFICIAL_ADVICE` avoid red-vs-green as only identifier; support color blindness.
- `MANDATORY` currently all images/figures/illustrations/photos in main article need **Alt Text** directly below figure legend in submitted manuscript, prefixed `Alt text:`. This does not necessarily display in typeset article.
- **Not established as publisher mandate**: top/right ticks or a four-sided box. Fine as a `HOUSE_DEFAULT`, but never label as a current MNRAS rule.

## A&A
Official original host: https://www.aanda.org/doc_journal/instructions/aadoc.pdf
Other official: https://www.aanda.org/for-authors/latex-issues/figures ; https://www.aanda.org/for-authors/latex-issues/typography

- `SOURCE_LIMITATION` the official PDF was indexed by search but web full-text fetch returned 403 at inspection. The following familiar layout numbers appear in the indexed official PDF and historic official guide; recheck the latest actual author PDF before submission. Do not claim fresh page-by-page verification.
- `OFFICIAL_ADVICE` most figures will be reduced to single-column width **88 mm**, up to **180 mm** double-column width, intermediate figures with side captions up to **120 mm** per indexed author guide.
- `OFFICIAL_ADVICE` illustrations should be sharp, numbers clear, avoid extremely thin lines and excessive blank space; verify grayscale reproduction and reduced size. Label referenced panels **within** image area and define symbols in caption.
- `OFFICIAL_ADVICE` vector EPS/PDF and suitable bitmaps (JPG/TIF etc. depending LaTeX engine); avoid conversions harming quality.
- `UNVERIFIED` do **not** assign a universal 0.5 pt or 8 pt *mandatory A&A minimum*. An exact all-purpose raster DPI is also not securely extracted from the linked current guide; do not issue false automatic compliance conclusions.
- Typography guide favors correctly roman-styled units and mathematical nomenclature.

## RAA
Official: https://www.raa-journal.org/sub/

- `MANDATORY/EDITORIAL` figures must be excellent quality, in sharp focus with clear numbers/letters and sharp lines; PostScript format preferred.
- `OFFICIAL_ADVICE` avoid thin lines, especially after reduction; dashed/dot-dashed lines and axis labels must withstand final-size reduction. Oversized labels can also look wrong.
- `MANDATORY` figures/tables mentioned in manuscript and placed appropriately, complete submission PDF; after acceptance individual figures and LaTeX sources required.
- `UNVERIFIED` official public guide does not state a universal point-size, line-width threshold, DPI table, or generic single-column width. Use house defaults **clearly marked as such** and verify the `raa.cls` actual column width.
- `POLICY_NOTE` RAA author page asks transparency about AI use in image generation/scientific analysis, but says basic reference/chart formatting alone does not require disclosure; evaluate user-specific application instead of giving legal/publishing guarantees.

## Implementation policy

- Journal-specific numbers **only** in source-traceable profile fields. Null means *not official specified*, not zero.
- For structural PDF audits, detected font sizes/line widths are not necessarily equal to plotted scientific labels/strokes (ticks and hidden/decorative strokes may be thinner), and embedded image effective DPI depends on print size: report evidence + uncertainty.
- Always visually inspect final size AND grayscale; a PDF preflight script never replaces that.
