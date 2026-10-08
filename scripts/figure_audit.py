#!/usr/bin/env python3
"""Structural PDF figure audit (NOT a scientific or full journal compliance certificate)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from astroplot_style import load_profile


def audit_pdf(path: str | Path, journal: str = "generic", *, expected_width_mm: float | None = None) -> dict:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF required for PDF inspection: pip install PyMuPDF") from exc
    path = Path(path)
    p = load_profile(journal)
    results = {
        "input": str(path), "journal": journal, "official_source": p["source"],
        "checks": [], "pages": [], "scientific_integrity": "UNKNOWN",
        "visual_review": "UNKNOWN", "overall": "NEEDS_REVIEW",
        "caveat": "PDF preflight detects only some structural properties; verify scientific truth and view actual rendered figure at final size."
    }
    def add(level, code, message):
        results["checks"].append({"status": level, "code": code, "message": message})
    if path.suffix.lower() != ".pdf":
        add("UNKNOWN", "unsupported_format", "Only PDFs inspected; no EPS/PNG audit in this script")
        return results
    if not path.is_file():
        add("FAIL", "not_found", "File not found")
        results["overall"] = "NOT_READY"
        return results
    try:
        doc = fitz.open(path)
    except Exception as exc:
        add("FAIL", "invalid_pdf", f"Cannot open PDF: {exc}")
        results["overall"] = "NOT_READY"
        return results
    if len(doc) != 1:
        add("FAIL", "page_count", f"Expected one figure per PDF file, found {len(doc)} pages")
    else:
        add("PASS", "page_count", "Single-page PDF")
    widths = []
    for index, page in enumerate(doc):
        width_mm = page.rect.width * 25.4 / 72.0
        height_mm = page.rect.height * 25.4 / 72.0
        widths.append(width_mm)
        spans = []
        for block in page.get_text("dict")["blocks"]:
            if "lines" not in block: continue
            for line in block["lines"]:
                for span in line["spans"]:
                    if span.get("text", "").strip():
                        spans.append({"size_pt": round(span["size"], 2), "text": span["text"][:90]})
        drawings = page.get_drawings()
        stroke_widths = sorted(set(round(d["width"], 3) for d in drawings
                                   if d.get("type") in ("s", "fs") and d.get("width") is not None
                                   and d["width"] > 0))
        images = []
        for item in page.get_image_info(xrefs=True):
            rect = fitz.Rect(item["bbox"])
            xdpi = item["width"] * 72.0 / rect.width if rect.width > 0 else None
            ydpi = item["height"] * 72.0 / rect.height if rect.height > 0 else None
            images.append({"pixels": [item["width"], item["height"]],
                           "bbox_pt": [round(v, 2) for v in rect],
                           "effective_dpi": [round(xdpi, 1) if xdpi else None,
                                             round(ydpi, 1) if ydpi else None]})
        results["pages"].append({
            "page": index + 1,
            "size_mm": {"width": round(width_mm, 2), "height": round(height_mm, 2)},
            "font_span_sizes_pt": sorted(set(round(s["size_pt"], 2) for s in spans)),
            "example_text": [s["text"] for s in spans[:12]],
            "stroke_widths_pt": stroke_widths[:40],
            "images": images,
        })
        if not spans:
            add("WARN", "no_text", f"Page {index+1}: no extractable text; fonts may be outlined or image-only")
        if not drawings:
            add("WARN", "no_vector_drawings", f"Page {index+1}: no vector drawings detected")
        # Font and stroke extraction includes hidden/decorative lines and title glyphs.
        # Never issue a definitive hard-compliance result based solely on the minimum.
        font_min = p.get("min_font_pt_official")
        if spans and font_min is not None:
            small = [s for s in spans if s["size_pt"] < font_min - 0.1]
            if small:
                add("WARN", "font_under_threshold", f"Page {index+1}: {len(small)} text spans below {font_min}pt AAS acceptance threshold; inspect which labels matter")
        line_min = p.get("min_line_pt_official")
        if stroke_widths and line_min is not None:
            below = [w for w in stroke_widths if w < line_min - 0.02]
            if below:
                add("WARN", "thin_pdf_strokes", f"Page {index+1}: detected strokes thinner than {line_min}pt; identify whether scientific lines/ticks or harmless ornament")
        for img in images:
            xy = [x for x in img["effective_dpi"] if x is not None]
            min_dpi = min(xy) if xy else None
            dpi_rule = p.get("raster_dpi_official") or {}
            if min_dpi is not None and dpi_rule:
                general = dpi_rule.get("general", dpi_rule.get("generic_bitmap"))
                if general and min_dpi < general:
                    add("WARN", "embedded_image_low_dpi", f"Page {index+1}: embedded image ~{min_dpi:.0f} DPI vs {general} DPI general guidance; check image type-specific exception")
    desired = expected_width_mm if expected_width_mm is not None else p["single_column_mm"]
    if desired is None:
        add("UNKNOWN", "column_width", "Official single-column width unverified; consult target manuscript class")
    elif widths and any(abs(w - desired) > 1.5 for w in widths):
        add("WARN", "column_width", f"PDF width differs from requested/official single-column {desired:g} mm by >1.5 mm; wide panels or intended LaTeX scaling may be valid")
    else:
        add("PASS", "column_width", f"Figure PDF width near target {desired:g} mm")
    if p.get("alt_text_required"):
        add("UNKNOWN", "alt_text", "MNRAS main-article figure Alt Text is required in manuscript; PDF image alone cannot prove presence")
    if journal.upper() == "A&A":
        add("UNKNOWN", "aa_pdf_access", "A&A current official guide PDF fetch was restricted during snapshot collection; recheck before submission")
    if any(c["status"] == "FAIL" for c in results["checks"]):
        results["overall"] = "NOT_READY"
    doc.close()
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    parser.add_argument("--journal", default="generic", choices=["generic", "AAS", "MNRAS", "A&A", "RAA"])
    parser.add_argument("--width-mm", type=float, default=None, help="Optional verified final target page width")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    parser.add_argument("--output", help="Optional audit report destination .json or .txt")
    args = parser.parse_args()
    report = audit_pdf(args.file, args.journal, expected_width_mm=args.width_mm)
    if args.format == "json":
        message = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        lines = [f"FIGURE PREFLIGHT: {report['input']} [{report['journal']}]",
                 f"Structural result: {report['overall']} (scientific/visual review UNKNOWN)"]
        for page in report["pages"]:
            lines.append(f"Page {page['page']}: {page['size_mm']['width']} × {page['size_mm']['height']} mm; fonts={page['font_span_sizes_pt']}; strokes={page['stroke_widths_pt'][:10]}; rasters={len(page['images'])}")
        for check in report["checks"]:
            lines.append(f"[{check['status']}] {check['code']}: {check['message']}")
        lines.append(report["caveat"])
        message = "\n".join(lines)
    if args.output:
        Path(args.output).write_text(message, encoding="utf-8")
    print(message)


if __name__ == "__main__":
    main()
