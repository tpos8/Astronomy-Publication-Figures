"""Publication figure style helper. Presets are HOUSE_DEFAULT unless noted in JSON."""
from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

PROFILES_PATH = Path(__file__).resolve().parents[1] / "assets" / "journal_profiles.json"


def load_profile(journal: str = "generic") -> dict:
    profiles = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
    key = journal.upper() if journal.upper() in profiles else journal.lower()
    if key not in profiles:
        raise ValueError(f"Unknown journal {journal!r}; choose one of {list(profiles)}")
    return dict(profiles[key])


def figure_width_in(journal: str, width_mm: float | None = None) -> float:
    p = load_profile(journal)
    selected = p["default_width_mm"] if width_mm is None else width_mm
    if selected <= 0:
        raise ValueError("width_mm must be positive")
    return selected / 25.4


def rc_style() -> dict:
    """Conservative house style, NOT officially mandated by any journal."""
    return {
        "font.family": "serif",
        "font.serif": ["DejaVu Serif", "Times New Roman", "Times"],
        "font.size": 8.0,
        "axes.labelsize": 9.0,
        "xtick.labelsize": 8.0,
        "ytick.labelsize": 8.0,
        "legend.fontsize": 8.0,
        "axes.linewidth": 0.8,
        "lines.linewidth": 1.1,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.minor.width": 0.6,
        "ytick.minor.width": 0.6,
        "xtick.top": True,
        "ytick.right": True,
        "xtick.minor.visible": True,
        "ytick.minor.visible": True,
        "axes.unicode_minus": True,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.facecolor": "white",
    }


@contextmanager
def publication_style():
    with mpl.rc_context(rc_style()):
        yield


def make_figure(journal: str = "generic", *, width_mm: float | None = None,
                height_ratio: float = 0.75, residual: bool = False):
    """Return (figure, axes tuple). Axes is always (main, residual_or_None)."""
    if height_ratio <= 0:
        raise ValueError("height_ratio must be positive")
    width = figure_width_in(journal, width_mm)
    if residual:
        fig, (main, bottom) = plt.subplots(
            2, 1, sharex=True,
            figsize=(width, width * height_ratio),
            gridspec_kw={"height_ratios": [3.0, 1.0], "hspace": 0.05},
            layout="constrained",
        )
        return fig, (main, bottom)
    fig, main = plt.subplots(figsize=(width, width * height_ratio), layout="constrained")
    return fig, (main, None)


def export_figure(fig, output: str | Path, *, png_preview: bool = True, dpi: int = 600) -> list[Path]:
    """No 'tight' bounding-box on export: preserves requested physical width."""
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() not in {".pdf", ".png", ".eps", ".svg"}:
        raise ValueError("Output must end with .pdf, .png, .eps or .svg")
    fig.savefig(path, dpi=dpi)
    exported = [path]
    if png_preview and path.suffix.lower() != ".png":
        preview = path.with_suffix(".png")
        fig.savefig(preview, dpi=dpi)
        exported.append(preview)
    return exported
