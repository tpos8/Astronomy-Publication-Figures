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

---

## Agent 自助安装与验证提示词（Codex / Agent Skills）

以下指令可直接交给具有本地文件和终端操作能力的 Codex 或其他编程 Agent。请同时向 Agent 提供本 Skill 的 ZIP 压缩包（或已解压的文件夹）。本节是**安装指令**，不是要求 Skill 在绘图任务中反复执行安装。

```text
你是一名资深 AI Agent 工程师，负责将我提供的 Astronomy Publication Figures v2.0 Multiwavelength Skill 安装到当前可用的 Agent 环境，并完成可核验的安装测试。请直接执行，不要仅提供安装建议或命令清单。

目标：安全安装 astronomy-publication-figures，使其可以在后续会话中通过 $astronomy-publication-figures 使用；保留四大期刊的绘图规范、跨领域科学守则和全部现有脚本。

A. 环境与安装包检查
1. 识别 Agent 平台、操作系统、用户主目录、当前项目目录、Python 与包管理工具。
2. 在我提供的附件或当前工作目录中查找 astronomy-publication-figures-multiwavelength-v2.zip 或 astronomy-publication-figures/ 文件夹；不要猜测不存在的路径。
3. 安全检查 ZIP 的目录结构和压缩文件路径，防止路径穿越；确保压缩包中存在 astronomy-publication-figures/SKILL.md。
4. 检查 SKILL.md 的 YAML frontmatter，包括 name 与 description。确认 name = astronomy-publication-figures，名称与目标目录一致。
5. 阅读 README.md、requirements.txt、requirements-astro.txt 和测试说明，再制定最小化安装方案。

B. 自动安装
1. 对 Codex 默认选择用户级目录 $HOME/.agents/skills/astronomy-publication-figures/；如果当前项目明确要求项目级隔离，则使用 <project>/.agents/skills/astronomy-publication-figures/。对于其他 Agent，先检查其实际支持的 Skills 发现路径，不要直接套用 Codex 目录。
2. 将 Skill 解压或复制到目标路径，保持 SKILL.md、references/、scripts/、assets/、agents/、tests/ 等目录结构完整，避免重复嵌套。
3. 如果目标目录已有旧版本，先比较并备份；未经确认，不得删除旧版自定义配置或覆盖冲突文件。
4. 不编辑无关项目文件，不修改全局 Agent 配置，除非该平台确实需要且改动是安全、必要的。

C. Python 依赖
1. 优先利用已有的兼容环境；如需安装 Python 包，创建或使用隔离虚拟环境，避免更改系统 Python。
2. 按 requirements.txt 安装基础依赖；仅在需要 FITS 相关能力时，按 requirements-astro.txt 安装额外依赖。
3. CASA、XSPEC、SunPy、healpy 等领域专用软件只进行能力探测和记录；未经我的明确要求，不批量安装大型专业软件。
4. 如出现离线或权限限制，保留 Skill 文件安装结果，并如实报告哪些功能尚未验证。

D. 自动验证
1. 核验安装位置和 SKILL.md frontmatter；检查 references/source-registry.md、references/domain-router.md、assets/domain_profiles.json 等关键文件。
2. 在可用环境中运行 python -m pytest -q tests，并记录每项测试的 PASS、FAIL、SKIP。
3. 执行不改动科研数据的烟雾测试，例如绘制合成数据并导出 PDF、审查生成的 PDF，或在安装的脚本参数允许时检查 --help。
4. 检查 radio/mm/submm、optical/IR/UV、high-energy、solar/planetary、cosmology、multimessenger 等领域的路由资料均可读取。
5. 如果具备 astropy，可使用临时生成的二维测试 FITS 验证 inspect_fits.py 与 plot_fits_map.py；对三维/四维 FITS 必须验证其拒绝自动切片的安全行为。若缺依赖，则标记 SKIP。
6. 尽可能通过 Agent 平台的 Skill 发现机制确认 Skill 已被识别；如平台无法在当前会话热加载，说明是否需要开启新会话，不得宣称已经完成真实调用验证。

E. 科学与安全边界
1. 禁止为测试改动真实观测数据、物理参数、拟合后验、频谱轴定义、WCS、PSF、合成波束、误差和 upper limits。
2. 禁止未经授权自动进行去噪、binning、FITS cube 切片、矩图制作、图像配准、背景扣除或响应拟合。
3. 明确区分期刊官方硬性标准、官方建议、领域规范和 HOUSE_DEFAULT；不可将检查项自动通过等同于科学结论正确。
4. 不运行未知来源的安装脚本，不通过 sudo 进行全局安装，不上传我的数据或密钥。

F. 交付结果
安装结束后给出简洁的验收报告，包括：Agent 平台、Skill 版本、实际安装路径、依赖安装状态、PASS/FAIL/SKIP 测试数量、真实 Skill 发现状态、未解决的问题和下一步操作。最后给出一句可直接使用的调用示例：
$astronomy-publication-figures 按 A&A 期刊规范审核此项目的全部天文图，仅审查，不修改科学数据。

现在开始执行。凡属非破坏性、权限范围内的操作可自主完成；遇到需要覆盖用户已有修改、提升系统权限或进行其他破坏性操作时先征求确认。
```

**安装完成后的调用示例：**

```text
$astronomy-publication-figures 审查我的全部天文学科研图，自动识别科学领域和目标期刊，逐张检查科学表达、单位、坐标系、图像尺寸、字体、分辨率和可复现性；只报告问题，不修改输入数据。
```
