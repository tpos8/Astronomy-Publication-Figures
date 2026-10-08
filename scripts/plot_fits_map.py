#!/usr/bin/env python3
"""Conservative publication plotter for ONE already-calibrated 2D FITS plane.

Never slices cubes, resamples/reprojects, computes moments, estimates RMS,
performs primary beam correction, or makes cross-WCS overlays.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from astroplot_style import publication_style, figure_width_in, export_figure


def parse_levels(values):
    if not values:
        return None
    parts = [float(s.strip()) for s in values.split(',')]
    if not all(np.isfinite(parts)) or len(set(parts)) != len(parts):
        raise ValueError('Contour levels must be finite distinct physical intensity values')
    return sorted(parts)


def plot_map(input_path, output_path, *, hdu=0, journal='generic', levels=None,
             cmap='cividis', vmin=None, vmax=None, width_mm=None,
             allow_pixel_coords=False, no_preview=False, dpi=600, domain='unspecified'):
    try:
        from astropy.io import fits
        from astropy.wcs import WCS
        from astropy.visualization.wcsaxes import add_beam
    except ImportError as exc:
        raise RuntimeError('Install astropy: pip install -r requirements-astro.txt') from exc
    with fits.open(input_path, memmap=True) as hdul:
        record = hdul[hdu]
        if record.data is None:
            raise ValueError(f'HDU {hdu} has no image')
        if record.data.ndim != 2:
            raise ValueError(f'HDU {hdu} has {record.data.ndim} dimensions. Use a vetted science pipeline to select/export an explicitly labeled 2D plane first; no implicit channel/Stokes selection')
        data = np.asarray(record.data, dtype=float)
        header = record.header.copy()
    ctype = [str(header.get(f'CTYPE{i}', '')).upper() for i in (1,2)]
    if any(t.startswith(('HPLN','HPLT','HGLN','HGLT','CRLN','CRLT')) for t in ctype):
        raise ValueError('Solar helioprojective/heliographic WCS detected: use SunPy with observer/time metadata, not the generic celestial map helper')
    mask = np.isfinite(data)
    if not mask.any():
        raise ValueError('No finite data in image; no automatic replacement')
    unit = header.get('BUNIT')
    warnings = ['FITS WCS parsing is not proof of astrometric calibration or cross-band registration']
    if domain == 'unspecified':
        warnings.append('Science domain not specified; domain-specific conventions require manual review')
    if not unit:
        warnings.append('BUNIT missing; figure cannot be labeled with a verified physical brightness unit')
    try:
        projection = WCS(header)
        has_celestial = projection.has_celestial and projection.pixel_n_dim == 2
    except Exception as exc:
        has_celestial = False
        projection = None
        warnings.append(f'WCS parse failed: {exc}')
    if not has_celestial and not allow_pixel_coords:
        raise ValueError('A valid celestial 2D WCS is needed. Pass --allow-pixel-coords only to make an explicitly labeled detector/pixel-coordinate plot')
    if not has_celestial:
        warnings.append('No verified sky WCS; plotted pixel coordinates and no claimed on-sky orientation')
    if vmin is not None and vmax is not None and vmin >= vmax:
        raise ValueError('vmin must be less than vmax')
    contour_values = parse_levels(levels)
    if contour_values and (min(contour_values) > max(data[mask]) or max(contour_values) < min(data[mask])):
        warnings.append('Contour levels fall outside observed pixel value range')
    beam = {k: header.get(k) for k in ('BMAJ','BMIN','BPA')}
    has_beam = has_celestial and all(beam[k] is not None for k in beam)
    if has_beam and not (beam['BMAJ'] > 0 and beam['BMIN'] > 0):
        raise ValueError('Header beam dimensions must be positive; no guessed beam')
    if str(unit or '').lower().find('/beam') >= 0 and not has_beam:
        warnings.append('Image has per-beam units but no complete valid BMAJ/BMIN/BPA header; beam marker omitted')
    with publication_style():
        width = figure_width_in(journal, width_mm)
        fig = plt.figure(figsize=(width, width * 0.95), layout='constrained')
        ax = fig.add_subplot(projection=projection) if has_celestial else fig.add_subplot()
        try:
            im = ax.imshow(np.ma.array(data, mask=~mask), cmap=cmap, origin='lower', vmin=vmin, vmax=vmax, interpolation='nearest')
            cbar = fig.colorbar(im, ax=ax, shrink=0.86, pad=0.03)
            cbar.set_label(str(unit) if unit else 'Intensity [unit unverified]')
            if contour_values:
                ax.contour(data, levels=contour_values, colors='white', linewidths=0.8, origin='lower')
            if has_beam:
                try:
                    add_beam(ax, header=header, corner='bottom left', facecolor='none', edgecolor='white', linewidth=1.0)
                except Exception as exc:
                    warnings.append(f'Could not render beam from FITS header: {exc}')
            if has_celestial:
                pass  # Respect WCSAxes auto labels; never assume RA/Dec.
            else:
                ax.set_xlabel('Pixel X (not sky position)')
                ax.set_ylabel('Pixel Y (not sky position)')
            output = Path(output_path)
            artifacts = export_figure(fig, output, png_preview=not no_preview, dpi=dpi)
        finally:
            plt.close(fig)
    header_science = {
        'domain': domain,
        'figure_kind': 'fits_map_2d', 'journal': journal, 'source_files': [str(input_path)],
        'representation': 'pre-existing FITS image intensity (no scientific transformations)',
        'units': unit, 'coordinate_frame': header.get('RADESYS', 'WCS native coordinates' if has_celestial else None),
        'wcs_verified': None, 'wcs_parse_ok': bool(has_celestial),
        'observing_frequency_hz': header.get('RESTFRQ', header.get('RESTFREQ')),
        'beam': ({'major_deg': float(beam['BMAJ']), 'minor_deg': float(beam['BMIN']), 'pa_deg': float(beam['BPA'])} if has_beam else None),
        'noise': None, 'processing': ['No additional scientific image processing; presentation only'],
        'uncertainties': None, 'contour_levels': contour_values,
        'display': {'colormap': cmap, 'vmin': vmin, 'vmax': vmax, 'masked_invalid_pixels': int((~mask).sum())},
        'warnings': warnings, 'manual_science_review': 'pending',
    }
    manifest = Path(output_path).with_suffix('.science.json')
    manifest.write_text(json.dumps(header_science, indent=2, ensure_ascii=False), encoding='utf-8')
    return artifacts, manifest, warnings


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--hdu', default='0', help='HDU index or extension name; defaults 0 but must be a 2D image')
    p.add_argument('--journal', default='generic', choices=['generic','AAS','MNRAS','A&A','RAA'])
    p.add_argument('--domain', default='unspecified', help='Research domain; do not infer this from FITS BUNIT alone')
    p.add_argument('--levels', help='Explicit intensity contour levels in FITS BUNIT, comma-separated; no derived RMS')
    p.add_argument('--cmap', default='cividis')
    p.add_argument('--vmin', type=float)
    p.add_argument('--vmax', type=float)
    p.add_argument('--width-mm', type=float)
    p.add_argument('--dpi', type=int, default=600)
    p.add_argument('--allow-pixel-coords', action='store_true')
    p.add_argument('--no-preview', action='store_true')
    a = p.parse_args()
    hdu = int(a.hdu) if a.hdu.isdigit() else a.hdu
    output, manifest, warnings = plot_map(
        a.input, a.output, hdu=hdu, journal=a.journal, levels=a.levels,
        cmap=a.cmap, vmin=a.vmin, vmax=a.vmax, width_mm=a.width_mm,
        allow_pixel_coords=a.allow_pixel_coords, no_preview=a.no_preview, dpi=a.dpi, domain=a.domain
    )
    for file in output: print(file)
    print(f'Science manifest: {manifest}')
    for line in warnings: print(f'REVIEW: {line}')

if __name__ == '__main__':
    main()
