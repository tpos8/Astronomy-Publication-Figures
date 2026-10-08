#!/usr/bin/env python3
"""Conservative, read-only multi-domain provenance check. Never certifies science correctness."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PROFILES = Path(__file__).resolve().parents[1] / 'assets' / 'domain_profiles.json'


def _present(value):
    return value is not None and value != '' and value != [] and value != {}


def _check_numeric_positive(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and 0 < value < float('inf')


def audit_manifest(manifest: dict, profiles: dict | None = None) -> dict:
    """Metadata inventory: PASS_METADATA / NEEDS_REVIEW / NOT_READY, not science validation."""
    if profiles is None:
        profiles = json.loads(PROFILES.read_text(encoding='utf-8'))
    domain = manifest.get('domain')
    domain_def = profiles['profiles'].get(domain)
    checks = []

    def add(field, status, comment):
        checks.append({'field': field, 'status': status, 'message': comment})

    for field in profiles['base_fields']:
        if not _present(manifest.get(field)):
            add(field, 'UNKNOWN', f'Required descriptive metadata {field!r} missing; never infer from style')
    if _present(domain) and domain_def is None:
        add('domain', 'UNKNOWN', f'No specialized protocol for {domain!r}; manual domain review required')
    if domain_def:
        for field in domain_def['review_fields']:
            if not _present(manifest.get(field)):
                add(field, 'UNKNOWN', f'Domain-sensitive field {field!r} not documented; confirm applicability')
    if _present(manifest.get('source_files')) and not isinstance(manifest['source_files'], list):
        add('source_files', 'FAIL', 'source_files must be a nonempty list of input paths')
    if manifest.get('wcs_verified') is True and not _present(manifest.get('coordinate_frame')):
        add('wcs_verified', 'FAIL', 'WCS verified is asserted but coordinate_frame is omitted')
    if 'observing_frequency_hz' in manifest and _present(manifest['observing_frequency_hz']):
        if not _check_numeric_positive(manifest['observing_frequency_hz']):
            add('observing_frequency_hz', 'FAIL', 'Observing frequency must be a positive finite number')
    if 'exposure' in manifest and _present(manifest['exposure']):
        val = manifest['exposure']
        if isinstance(val, (int, float)) and not _check_numeric_positive(val):
            add('exposure', 'FAIL', 'Exposure must be positive; document whether good-time, nominal, or effective exposure')
    if _present(manifest.get('beam')):
        beam = manifest['beam']
        if not isinstance(beam, dict):
            add('beam', 'FAIL', 'Beam must specify meaningful major_deg/minor_deg/pa_deg or be absent')
        else:
            for key in ('major_deg', 'minor_deg'):
                if not _check_numeric_positive(beam.get(key)):
                    add('beam', 'FAIL', f'Beam {key} must be positive and finite')
    if _present(manifest.get('processing')) and not isinstance(manifest['processing'], list):
        add('processing', 'UNKNOWN', 'Processing should be a list of explicitly performed operations')
    if manifest.get('representation') == 'counts_spectrum' and domain in ('xray','gamma'):
        if manifest.get('units') in ('erg cm-2 s-1', 'Jy'):
            add('units', 'FAIL', 'Count spectrum cannot be silently presented in energy flux-density units')
    if domain == 'multiwavelength' and manifest.get('wcs_verified') is False:
        add('wcs_verified', 'FAIL', 'Multiwavelength overlays require verified WCS or explicit registration')

    fail = any(c['status']=='FAIL' for c in checks)
    unknown = any(c['status']=='UNKNOWN' for c in checks)
    result = 'NOT_READY' if fail else ('NEEDS_REVIEW' if unknown else 'PASS_METADATA')
    return {
        'domain': domain, 'overall': result, 'checks': checks,
        'limitations': [
            'Presence of provenance fields does not verify their truth or quality.',
            'Domain-specific review fields may not apply to every product; inspect manually.',
            'Technical PDF auditing and expert scientific interpretation are separate.',
        ]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', help='Figure science metadata as JSON')
    parser.add_argument('--format', choices=('json','text'), default='text')
    args = parser.parse_args()
    obj = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    report = audit_manifest(obj)
    if args.format == 'json':
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"{report['overall']} ({report['domain']}): {len(report['checks'])} findings")
        for check in report['checks']:
            print(f"  {check['status']:<7} {check['field']}: {check['message']}")
        print('Reminder: PASS_METADATA is not an astrophysical integrity certification.')

if __name__ == '__main__':
    main()
