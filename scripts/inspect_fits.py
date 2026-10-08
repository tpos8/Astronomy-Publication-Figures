#!/usr/bin/env python3
"""Read-only report for FITS images, cubes, OGIP-like tables and astronomy metadata."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def inspect_file(path: str | Path) -> dict:
    try:
        from astropy.io import fits
        from astropy.wcs import WCS
    except ImportError as exc:
        raise RuntimeError('Astropy is required for FITS inspection: pip install -r requirements-astro.txt') from exc
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(source)
    report = {'input': str(source), 'hdu': [], 'warnings': [], 'read_only': True}
    with fits.open(source, memmap=True) as hdul:
        for index, hdu in enumerate(hdul):
            h = hdu.header
            rec = {
                'index': index, 'name': hdu.name, 'type': type(hdu).__name__,
                'shape': list(hdu.data.shape) if hdu.data is not None else None,
                'naxis': h.get('NAXIS'),
                'bunit': h.get('BUNIT'), 'btype': h.get('BTYPE'),
                'telescope': h.get('TELESCOP'), 'instrument': h.get('INSTRUME'),
                'date_obs': h.get('DATE-OBS'), 'timesys': h.get('TIMESYS'),
                'radesys': h.get('RADESYS'), 'specsys': h.get('SPECSYS'),
                'restfreq_hz': h.get('RESTFRQ', h.get('RESTFREQ')),
                'beam': {k: h.get(k) for k in ['BMAJ','BMIN','BPA'] if k in h},
                'table_columns': list(hdu.columns.names) if hasattr(hdu, 'columns') and hdu.columns is not None else None,
                'classification': h.get('HDUCLAS1'),
            }
            if hdu.data is not None and isinstance(hdu, (fits.PrimaryHDU, fits.ImageHDU, fits.CompImageHDU)) and h.get('NAXIS',0)>0:
                try:
                    w = WCS(h, relax=True)
                    rec['wcs'] = {
                        'pixel_n_dim': w.pixel_n_dim,
                        'world_axis_physical_types': w.world_axis_physical_types,
                        'ctype': list(w.wcs.ctype),
                        'cunit': [str(x) for x in w.wcs.cunit],
                        'has_celestial': w.has_celestial,
                    }
                except Exception as e:
                    rec['wcs_error'] = str(e)
            if rec['shape'] is not None and len(rec['shape']) > 2:
                report['warnings'].append(f'HDU {index}: multidimensional dataset; do not choose a plane implicitly')
            if rec['bunit'] is None and isinstance(hdu, (fits.PrimaryHDU, fits.ImageHDU, fits.CompImageHDU)) and h.get('NAXIS', 0) >= 2:
                report['warnings'].append(f'HDU {index}: image brightness unit BUNIT missing')
            report['hdu'].append(rec)
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input')
    p.add_argument('--json', action='store_true', help='Print JSON report (default also JSON for machine readability)')
    args = p.parse_args()
    print(json.dumps(inspect_file(args.input), ensure_ascii=False, indent=2, default=str))

if __name__ == '__main__':
    main()
