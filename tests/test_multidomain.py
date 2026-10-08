"""Safety regression tests for cross-domain plotting. Synthetic values are only test fixtures."""
from __future__ import annotations
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from science_manifest_audit import audit_manifest
from plot_from_csv import build, KIND_AXES
from plot_fits_map import parse_levels


def test_domains_are_present_and_bookended():
    profiles = json.loads((ROOT/'assets'/'domain_profiles.json').read_text())
    for domain in ('radio','mm_submm','xray','gamma','infrared','optical','ultraviolet','solar','cosmology','gravitational_wave','neutrino','multiwavelength','theoretical','planetary','astrometry'):
        assert domain in profiles['profiles']
    for kind in ('radio_spectrum','visibility','xray_spectrum','gamma_sed','polarization','solar_profile','gw_asd','cmb_power','spectrum'):
        assert kind in KIND_AXES


def test_manifest_missing_radio_provenance_is_unknown():
    example = {'domain':'radio','figure_kind':'radio_continuum','source_files':['image.fits'], 'representation':'restored', 'units':'Jy/beam'}
    r = audit_manifest(example)
    assert r['overall']=='NEEDS_REVIEW'
    assert any(x['field']=='beam' and x['status']=='UNKNOWN' for x in r['checks'])


def test_manifest_multiwavelength_false_wcs_blocker():
    example = {'domain':'multiwavelength','figure_kind':'overlay','source_files':['a.fits','b.fits'],'representation':'registered maps','units':'mixed', 'wcs_verified':False}
    assert audit_manifest(example)['overall']=='NOT_READY'


def test_manifest_complete_metadata_is_not_science_certification():
    data = {'domain':'radio','figure_kind':'map','representation':'restored','source_files':['a.fits'], 'units':'Jy/beam',
            'coordinate_frame':'ICRS','wcs_verified':True,'observing_frequency_hz':1.4e9,
            'beam':{'major_deg':0.001, 'minor_deg':0.0009,'pa_deg':4.},
            'noise':{'rms':0.01,'unit':'Jy/beam'},'processing':['pipeline'], 'uncertainties':'rms'}
    r = audit_manifest(data)
    assert r['overall']=='PASS_METADATA'
    assert 'does not verify' in r['limitations'][0]
    data['observing_frequency_hz']=-1
    assert audit_manifest(data)['overall']=='NOT_READY'


def test_contour_levels_are_physical_input():
    assert parse_levels('4,2,-2') == [-2.0,2.0,4.0]
    with pytest.raises(ValueError): parse_levels('3,nan')
    with pytest.raises(ValueError): parse_levels('4,4')


def args_for(tmp_path, kind='gamma_sed', *, label=None, xlabel='Energy (GeV)', ylabel='E2dN/dE'):
    f=tmp_path/'obs.csv'
    f.write_text('energy,flux,error,limit,model\n1,2,0.2,0,1.9\n2,1,0.1,1,0.9\n3,1.4,0.3,0,1.2\n')
    return SimpleNamespace(journal='generic', x='energy', y='flux', yerr='error',model='model',
          upper_limit_flag='limit',limit_label=label, input=str(f),residual=True,kind=kind,
          xlabel=xlabel, ylabel=ylabel,loglog=False,width_mm=None,output=str(tmp_path/'out.pdf'),no_preview=True,dpi=120)


def test_upper_limit_needs_confidence(tmp_path):
    with pytest.raises(ValueError, match='limit-label'):
        build(args_for(tmp_path, label=None))


def test_upper_limits_preserved_no_science_residual(tmp_path):
    a=args_for(tmp_path,label='95% CL')
    output=build(a)
    assert output[0].is_file()
    man=json.loads((tmp_path/'out.plot-manifest.json').read_text())
    assert man['n_points']==3
    assert man['upper_limits']['confidence_label']=='95% CL'


def test_energy_spectrum_requires_explicit_science_units(tmp_path):
    a=args_for(tmp_path, kind='xray_spectrum',xlabel=None,label='95% CL')
    with pytest.raises(ValueError, match='explicit'):
        build(a)


@pytest.mark.skipif(importlib.util.find_spec('astropy') is None, reason='Astropy optional FITS dependency not installed')
def test_fits_3d_cube_rejected(tmp_path):
    from astropy.io import fits
    from plot_fits_map import plot_map
    cube=tmp_path/'cube.fits'
    fits.writeto(cube, np.ones((3,6,8)), overwrite=True)
    with pytest.raises(ValueError, match='dimensions'):
        plot_map(cube,tmp_path/'wrong.pdf',allow_pixel_coords=True)


@pytest.mark.skipif(importlib.util.find_spec('astropy') is None, reason='Astropy optional FITS dependency not installed')
def test_fits_inspector_reports_axes(tmp_path):
    from astropy.io import fits
    from inspect_fits import inspect_file
    f=tmp_path/'arr.fits'
    fits.writeto(f,np.ones((3,5,5)), overwrite=True)
    r=inspect_file(f)
    assert r['hdu'][0]['shape']==[3,5,5]
    assert any('multidimensional' in w for w in r['warnings'])
