# Figure science-manifest format

A **manifest** is a sidecar provenance record, not proof that metadata is true. `scripts/science_manifest_audit.py` reads JSON and reports missing fields according to domain. Sample shape:

```json
{
  "domain": "radio",
  "figure_kind": "radio_continuum",
  "journal": "MNRAS",
  "source_files": ["my_image.fits"],
  "representation": "restored_continuum_image",
  "units": "Jy/beam",
  "coordinate_frame": "ICRS",
  "wcs_verified": true,
  "observing_frequency_hz": 1400000000.0,
  "beam": {"major_deg": 0.001, "minor_deg": 0.0008, "pa_deg": 32.0},
  "noise": {"rms": 0.0001, "unit": "Jy/beam", "method": "measured in named off-source region"},
  "processing": ["restored image from validated pipeline"],
  "uncertainties": "off-source rms",
  "caption": "...",
  "manual_science_review": "pending"
}
```

No template numbers here should be assumed for real files; these are structural examples. If unknown, omit keys or set `null`. Domain-specific required-field policy is conservative and aimed at detecting missing *provenance*, not validating scientific method.

Supported domain audit profiles include `radio`, `mm_submm`, `xray`, `gamma`, `solar`, `cosmology`, `gravitational_wave`, `multiwavelength`, `optical`, `infrared`, `ultraviolet`, `theoretical`. Generic checks require nonempty figure_kind, source_files, units, and representation. A missing primary key yields UNKNOWN, explicit impossible metadata yields FAIL. `PASS_METADATA` means fields are present and structurally consistent; it does not certify their truth or the science pipeline.
