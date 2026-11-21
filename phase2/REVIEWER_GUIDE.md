# Phase 2 reviewer quickstart

**Project 9 — Waste Recognition and Instance Segmentation on Conveyor Belts**  
**For instructor / teaching-assistant review** · Five-member team · M4 (12), M5 (12), M8 (11), extensions A/B (5+5): total 45 available points. This is **rubric information, not a self-assigned score**.

## Two-minute orientation

1. **Read [Phase 2 overview](README.md)** for the architecture and frozen Test metric table.
2. **M4/M5 source:** [sanitized notebook](m4_m5_source_review/Project9_Phase2_M4_M5_SAFE_SOURCE.ipynb), [preparation script](m4_m5_source_review/phase2_data_prep.py), [recorded configs](m4_m5_source_review/configs/), and [source-review validation notes](m4_m5_source_review/VALIDATION_NOTES.md).
3. **M8 service:** [manifest-driven service](m8_manifest_driven/service.py), [manifest validator](m8_manifest_driven/manifest_validation.py), [release manifest](m8_manifest_driven/release_manifest.json), and [environment](m8_manifest_driven/requirements.txt).
4. **Measured evidence:** [evidence map](PHASE2_EVIDENCE_STATUS.md) and [21 November HTTP/ONNX follow-up](M8_FOLLOWUP_2026-11-21.md).
5. **Report/figures/private raw evidence:** provided through the course's official private submission, **not** redistributed in this public repository.

## How to reproduce a bounded M8 demo

**Prerequisites:** Authorized access to exactly the detector `best_det.pt` and segmenter `best_seg.pt` from the team's *private* Drive/release, a compatible Python/PyTorch environment and an authorized non-Test demonstration image.

The server verifies both checkpoints against the fixed SHA256 digests in [release_manifest.json](m8_manifest_driven/release_manifest.json). Do **not** edit expected hashes to bypass a failure. Do not upload the checkpoints to public GitHub.

Suggested local sequence (from a clone's repository root):

```bash
cd phase2/m8_manifest_driven

# Set up an isolated compatible environment, then install requirements.
# The pinned torch/torchvision +cpu wheels may require the official CPU wheel index:
python -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# After placing the exact private weights next to service.py:
sha256sum best_det.pt best_seg.pt
python -m uvicorn service:app --host 127.0.0.1 --port 8000
```

From a second terminal:

```bash
curl http://127.0.0.1:8000/health
curl -F "file=@/absolute/path/to/authorized_validation_image.jpg" http://127.0.0.1:8000/predict
```

Expected behavior: `/health` returns `status=ok` and `model_verified=true`; `/predict` returns dimensions, detected material/score/box, optional associated polygon/centroid, a review flag and material counts. Outputs depend on the uploaded image; **no fixed count is guaranteed**. The service is **PyTorch CPU**, not ONNX.

**Limitations:** This GitHub source alone lacks authorized image data and weights; a successful clean-room reinstall and full training reproduction are **not verified**. Hardware/package behavior may vary. The unauthenticated service is for localhost only.

## Results and scope: do not confuse these

| Evaluation | Partition / protocol | What the numbers mean |
| --- | --- | --- |
| M4/M5 frozen Test AP | 929 held-out ZeroWaste-f images, once-only evaluation | AP at confidence floor 0.001; **not** service-point P/R/F1 |
| M4 threshold, size recall, confusion | Validation, 451 images, varying recorded settings | Selection/diagnostic evidence, **not** Test performance |
| M5 mean IoU/Dice | 24 deliberately selected Validation images | 117 GT objects; **not** full-Test mask quality |
| Local API smoke | One Validation diagnostic image | Technical function only |
| 21 Nov HTTP benchmark | One repeated Validation image ×25 requests | Bounded latency and throughput, **not** all-input or line-rate proof |
| 21 Nov ONNX parity | One diagnostic image; matched boxes only | Cross-backend agreement, **not** ground-truth accuracy |
| Visual search + CLIP extensions | 200 known-class GT Test crops | Advisory cropped-object comparison; **not** unknown-class detection |

## Reviewer Q&A / limitations

- **Why are model weights and dataset images missing?** They remain private to follow dataset-license, security and course privacy requirements.
- **Why does the repository contain archival notebooks?** To show historical provenance without enabling automatic retraining or repeating the frozen Test. The public review notebook is *not* a complete end-to-end replay.
- **Does an ONNX export mean ONNX is deployed?** No. The HTTP endpoint currently runs PyTorch; ONNX is separately tested.
- **How were responsibilities divided?** All five members cooperated across the project, with a distinct primary coordination focus for each member. Names/IDs and their confirmed descriptions belong in the privately submitted report.
- **Is this industrial-ready?** No. Physical grasp reliability, sustained belt throughput, unknown materials and unattended sorting remain unvalidated.

## Safe review checklist

- [ ] Inspect the source and compare links against the **exact submitted Phase 2 commit**.
- [ ] Read the private PDF and supporting evidence ZIP.
- [ ] If authorized, restore the exact original weights and test `/health` and `/predict` on Validation images.
- [ ] Do not rerun the original frozen Test for additional tuning.
- [ ] Do not publish passwords, private dataset files, raw image crops or personal student IDs.
