# Astronomy Publication Figures — 全领域天文学科研绘图 Agent Skill

**v2.0 Multiwavelength / Cross-domain Edition**

一款面向 Codex / Agent Skills 的跨领域天文学论文绘图助手，而非仅用于光学光变曲线。它按「期刊出版规范 × 科学领域 × 数据产品类型」选择正确的绘图策略，特别区分 **AAS/MNRAS/A&A/RAA 的出版要求**与 **射电、高能、太阳、宇宙学等领域的物理与仪器约定**。

## 支持领域

- 射电与毫米/亚毫米：VLA、ALMA、VLBI，干涉成像、合成波束、`Jy/beam`、谱线 cube/channel/moment/PV、偏振、可见度、RM 等。
- 红外/光学/紫外：成像、光变、相位折叠、周期、光谱、SED、Polarimetry、时域与双星模型。
- X 射线/伽马射线：观测事件/能谱、响应折叠谱、背景及残差、upper limits、SED、PSF/曝光图与显著性图。
- 太阳与行星地图/探测任务、Gaia 天体测量与星表巡天、宇宙学/CMB、HEALPix、数值模拟、引力波/中微子、多信使联合可视化。

**注意能力边界：**“支持领域”是指 Skill 具有该领域的绘图规范、决策路由和审核守则；并不意味着不提供科学参数就能从原始观测事件自动完成校准、图像反卷积、射电成像、响应拟合或物理建模。内置脚本主要负责经过科学处理的产品可视化和保守审查。

## 安装

解压后将 `astronomy-publication-figures/` 复制到项目 `.agents/skills/` 或用户的 `$HOME/.agents/skills/`。使用 `$astronomy-publication-figures` 调用。目录名和 SKILL.md frontmatter 名称保持一致。

## Codex 提示词示例

- `$astronomy-publication-figures 检查我的 ALMA CO(2-1) FITS 数据立方体，区分频率与 LSRK 速度、确认单位、波束、噪声和 WCS；先提出 channel/moment/PV 作图方案，不要自动计算矩图。`
- `$astronomy-publication-figures 根据已导出的 XSPEC counts/model/residual 数据绘制 MNRAS 能谱拟合图，确认其不是 unfolded spectrum，并输出 PDF 和审查报告。`
- `$astronomy-publication-figures 将射电连续谱等值线叠加到 HST 成像图上，先核验两个 FITS 的 WCS 和 PSF/beam，禁止仅按数组像素覆盖。`
- `$astronomy-publication-figures 按 A&A 版式整理 Fermi 的 E²dN/dE 和 upper limits，不要凭空生成 TS/CL 或把上限画成探测点。`
- `$astronomy-publication-figures 将我的 Planck HEALPix 全天图绘制为 Mollweide 投影，保留坐标系、RING/NESTED 和 mask，不要默认删除 monopole。`
- `$astronomy-publication-figures 审核太阳 AIA/HMI 图，按真实观察时间和 SunPy 世界坐标标记，不要标成通用 RA/Dec。`
- `$astronomy-publication-figures 检查全文 figures 的出版尺寸、字体、颜色以及跨波段单位是否一致，仅审查不要改动原始文件。`

## 架构

- `SKILL.md` — 触发、证据层级、科学防错、领域路由、端到端执行。
- `references/domain-router.md` — 先区分科学领域、物理量和数据产品，再选择作图方式。
- `references/{radio-mm-submm,high-energy,spectroscopy-polarimetry,solar-cosmology-multimessenger,planetary-astrometry-surveys,multiwavelength-crosschecks}.md` — 新增全领域协议。
- `references/source-registry.md` — 官方来源及适用范围；`journal-standards.md` — 出版社规则。
- `scripts/plot_from_csv.py` — 已处理数值数据通用作图，支持常见光变、谱、能谱、极化、时频参数曲线。
- `scripts/inspect_fits.py` — 只读的 FITS HDU、单位、WCS、波束等信息检查（需要 `astropy`）。
- `scripts/plot_fits_map.py` — **仅接受二维** FITS 影像的 WCS 感知绘图、明确等值线与 beam；不会自动计算谱线矩图、自动平滑或自动推断 RMS。
- `scripts/science_manifest_audit.py` — 领域化的元数据完整性检查。
- `scripts/figure_audit.py` — 原有 PDF 制版技术检查。
- `assets/domain_profiles.json`, `evals/cases.json`, `tests/` — 领域风险字段、行为样本与运行测试。

## 安装依赖、运行测试

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-astro.txt  # only for FITS routines
python -m pytest -q tests
python scripts/inspect_fits.py input.fits --json
python scripts/plot_fits_map.py --input image2d.fits --output image.pdf --journal A&A --domain radio --cmap cividis
python scripts/science_manifest_audit.py path/to/figure.science.json --format text
python scripts/figure_audit.py path/to/figure.pdf --journal A&A --format text
```

If 3-D/4-D FITS is provided, `plot_fits_map.py` **fails closed**: select the required slice in a verified scientific pipeline and export an explicitly labeled 2-D FITS first. This avoids silently choosing the wrong velocity/Stokes channel.

## 质量等级与来源

期刊的官方技术规范不等于仪器的科学约定，`HOUSE_DEFAULT` 更不等于强制要求。每张图保留参数、物理处理和图注的可审计性；`PASS_METADATA` 仅表示字段完整，不能替代科学审稿。参考链接详见 `references/source-registry.md`（2026-10-08 检索快照）；投稿前再次核对更新。
