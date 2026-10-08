"""Tests avoid inventing real astronomy data; all figures generated from deterministic synthetic demo."""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from astroplot_style import load_profile, figure_width_in
from figure_audit import audit_pdf
from make_demo import create_demo
from plot_from_csv import read_numeric_columns


def test_journal_profiles_preserve_source_truth():
    assert load_profile("AAS")["min_line_pt_official"] == 0.5
    assert load_profile("MNRAS")["min_line_pt_official"] == 0.3
    assert load_profile("MNRAS")["alt_text_required"] is True
    assert load_profile("RAA")["min_line_pt_official"] is None
    assert load_profile("A&A")["single_column_mm"] == 88
    assert abs(figure_width_in("MNRAS") * 25.4 - 84) < 1e-8


def test_demo_creates_single_page_pdf_and_report(tmp_path):
    csv_path, pdf_path = create_demo(tmp_path, "MNRAS")
    assert csv_path.is_file() and pdf_path.is_file()
    report = audit_pdf(pdf_path, "MNRAS")
    assert report["overall"] == "NEEDS_REVIEW"
    assert len(report["pages"]) == 1
    assert abs(report["pages"][0]["size_mm"]["width"] - 84) < 1
    assert any(c["code"] == "alt_text" for c in report["checks"])
    assert len(read_numeric_columns(csv_path, ["phase", "flux"])["phase"]) == 200


def test_rejects_nan_in_real_csv(tmp_path):
    bad = tmp_path / "nan.csv"
    bad.write_text("phase,flux\n0.1,1.0\n0.2,nan\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Non-finite"):
        read_numeric_columns(bad, ["phase", "flux"])


def test_requires_pdf_exists(tmp_path):
    result = audit_pdf(tmp_path / "missing.pdf", "AAS")
    assert result["overall"] == "NOT_READY"
