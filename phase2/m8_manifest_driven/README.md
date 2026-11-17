# Project 9 — M8 manifest-driven CPU prototype (reviewed source)

**Status: review candidate, not a finished or independently reproduced deployment.**

This package contains the source of the manifest-driven FastAPI service evaluated in `Project9_M8_MANIFEST_VAL_CPU_V2.zip` (17 November 2026). It does **not** include model weights, dataset frames, GT crops, API secrets or private identifiers. The bundle is limited to source and its settings.

## Files

- `service.py`: `GET /health` and `POST /predict` PyTorch CPU service using M4 boxes and same-class M5 polygon matches.
- `manifest_validation.py`: startup validation of supported class order, model paths, settings and input limits.
- `release_manifest.json`: recorded four-class setup, model SHA256 digests, CPU versions and confidence/IoU thresholds.
- `requirements.txt`: packages/versions recorded for the CPU functional-check environment. These are **not** a verified cross-platform installation lockfile. PyTorch `+cpu` builds may require an appropriate official PyTorch wheel index.

## Recorded test evidence (not independently rerun here)

The source bundle's `worker_summary.json` reports a FastAPI **in-process TestClient** check with original private checkpoints. Reference and candidate returned identical JSON for **two selected Validation GT crops** and `/health`. Invalid/empty/32×32 uploads returned 400; upload beyond 12 MiB returned 413. No additional predictor calls were recorded for negative cases. The recorded check used PyTorch FP32 on CPU. This is a narrow interface/functional comparison, **not** a full-image/Test-set accuracy measurement, HTTP network load test, ONNX parity proof, hardware benchmark, or continuously hosted deployment.

The original report's benchmark (p95 = 1284.87 ms, 25 serial requests to one Validation image, earlier runtime) remains **a separate experiment**; do not attribute it to the candidate V2 implementation.

## Private-only local execution prerequisites

1. Obtain the **authorized exact** `best_det.pt` and `best_seg.pt` from the team's private artifact store; do not commit them to public GitHub.
2. Put both weights next to `service.py`. On import, the service checks both files against the SHA256 digests recorded in `release_manifest.json` and refuses to start if they do not match.
3. Establish a compatible Python environment with the recorded dependencies and the correct official PyTorch CPU wheels. The original TestClient run was performed elsewhere; this source-only package has **not** been installed and run in a fresh environment.
4. From this directory, after private model restoration, use `uvicorn service:app --host 127.0.0.1 --port 8000`. Check `/health` and send one image via multipart `POST /predict`.

The API has no authentication or authorization. Do **not** expose it directly to a public network. The reported pixel-space centroids are candidate positions, **not** validated robotic grasp points.

## Source review and remaining release gates

The package retains the candidate's recorded files; the source was syntax-checked and compared with the archived reference. Team approval, dependency/license review, original weight verification and independent reproducibility checks remain required before describing this as a final Phase 2 release. Do not merge the public draft PR solely on the basis of this package.
