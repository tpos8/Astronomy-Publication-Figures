# Suggested skill calls

## Case 1: improve existing TESS paper figure
`$astronomy-publication-figures 在不改变 QUALITY 过滤、归一化、轨道历表、拟合参数的前提下，统一光变图排版，按 RAA 模板的实际栏宽导出 PDF，并给出前后检查结果。`

## Case 2: phase folded with real data
`$astronomy-publication-figures 把已校正的 Orbital Phase / Normalized Flux / Error / PHOEBE model 四列绘制成上下双面板：观测+模型、O-C；按 MNRAS 标准输出；图注写明实际 P、T0、Pdot、各 Sector offset。没有的数值不要编造。`

## Case 3: audit only
`$astronomy-publication-figures 只审查 figures/*.pdf，输出各图最小文字、线条、嵌入图片 DPI、宽度和论文可访问性问题；未经授权不要覆盖原图或进行科学数据变换。`

## CSV columns

The general plotting CLI consumes pre-existing values and will **not** phase-fold, bin, sigma-clip, or normalize automatically:

- `phase, flux, flux_err, model_flux`
- `time, flux, flux_err` (provide explicit time standard in `--xlabel`)
- `phase, rv, rv_err, model_rv`
- `period, power`
- `wavelength, flux_density, flux_error, model_flux_density`
- `epoch, oc, oc_err`

For advanced use (FITS/WCS images, CornerPlot, PHOEBE-derived posterior), have Codex implement purpose-built scripts using the type protocols rather than forcing all data into the CSV CLI.
