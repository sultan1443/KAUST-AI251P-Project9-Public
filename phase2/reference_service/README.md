# Historical PyTorch HTTP reference service (M8)

**This is source extracted from the early `CORRECTED_v3` notebook, NOT the later validated manifest-driven V2 implementation described in the team's 17 Nov 2026 report.**

The extracted source was inspected for syntax (AST parsing), obvious secrets and hard-coded archive passwords. **It was not run with weights on the present GitHub branch.** The newer, paired-TestClient-verified candidate and its pinned environment are separate artifacts and have not yet been made available for publication. Never describe this extraction as that later service.

## Files
- `service.py`: original manifest-loading PyTorch CPU FastAPI reference with `GET /health` and `POST /predict`.
- `release_manifest.example.json`: example settings and SHA256 values **as reported in the team's 17 Nov PDF**, not hashes independently recomputed by this publication step.

## Running only after private checkpoint restoration

1. Obtain the original model files from the team's private approved Drive/release source, not from GitHub. Put `best_det.pt` and `best_seg.pt` next to `service.py`.
2. Copy `release_manifest.example.json` to `release_manifest.json`. Recompute both SHA256 digests locally and compare them with the values recorded here before starting. If the bytes differ, stop and investigate; do not override integrity checks just to run.
3. Install the project-approved, compatible environment including Ultralytics, PyTorch CPU, FastAPI, Uvicorn, python-multipart, NumPy, Pillow and OpenCV. The historical notebook used a runtime-generated requirements file; this public branch **does not yet supply a tested lockfile**.
4. From this folder run `uvicorn service:app --host 127.0.0.1 --port 8000`; send `curl -F file=@image.PNG http://127.0.0.1:8000/predict`, or check `curl http://127.0.0.1:8000/health`.

The response contains material labels, confidence, boxes, optional polygons and pixel-space centroids, counts, and mask-association review flags. Returned centroids are **not** verified robotic grasp points. The service is local only and provides no access control; do not expose it on a public network.

**Scope:** This version lacks the separately recorded November manifest-driven refactor and its full input-validation audit. Its operating confidence 0.25 and NMS IoU 0.50 are not the low-confidence settings used for the saved AP results. No live deployment or industrial-belt throughput claim is made.
