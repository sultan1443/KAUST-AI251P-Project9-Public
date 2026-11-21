# Historical M8 reference service — archival only

**Important:** This is an early PyTorch HTTP service extracted from the original `CORRECTED_v3` notebook. It is **not** the later [manifest-driven M8 V2 implementation](../m8_manifest_driven/), which is separately available on this branch.

The extraction was syntax-reviewed and sanitized, but this *archival file* was not independently executed with the original private weights as part of the GitHub publication step. Historical code is retained for provenance rather than promoted as the recommended demo.

## Contents

- [service.py](service.py) — old FastAPI `GET /health` and `POST /predict` implementation.
- [release_manifest.example.json](release_manifest.example.json) — illustrative historical settings/hash inventory.

## Recommended reviewer path

Use the later [manifest-driven service](../m8_manifest_driven/service.py), [reviewer guide](../REVIEWER_GUIDE.md) and [21 November 2026 M8 measurements](../M8_FOLLOWUP_2026-11-21.md). The recorded 21-Nov Colab HTTP session used the team's private service and weights; this source-only archive has **not** been independently rerun in that session.

If specifically inspecting the old implementation, you must restore exact authorized private weights, verify its manifest/checksums and use compatible dependencies. Do not bypass integrity checks. No original weights, raw dataset images, credentials or student IDs are in this public folder.

**Limitations:** Local PyTorch CPU prototype only; `/predict` results are not verified production sorting commands, image centroids are not validated physical grasps, and there is no authenticated public hosting or industrial throughput claim. Frozen Test metrics were measured separately with their own confidence and NMS settings.
