# Phase 2 — Project 9: Conveyor Waste Recognition

**KAUST AI251P Applied Computer Vision · Five-person team · M4, M5, M8 and two extensions**

> **Review status:** documented source and measured private evidence, with remaining release/reproducibility checks. The public repository is not a complete weight-and-data bundle. The course-submitted report is private.

## Architecture at a glance

```text
Conveyor / uploaded image
    ├── M4: YOLO11n object detection → material / confidence / box
    ├── M5: YOLO11n-seg → instance polygons
    └── Same-class box matching → candidate pixel centroid / review flag
                                  ↓
              Local FastAPI (PyTorch CPU): /health, /predict
                                  ↓
           Four-class object list, polygons and M4 counts

Optional advisory experiments (separate from the primary API):
  A. ResNet18 image retrieval      B. CLIP material suggestion
```

The four materials are **cardboard, metal, rigid plastic, soft plastic**. Candidate centroids are image-space estimates and **are not certified grasp points**. ONNX exports were run through ONNX Runtime separately, **not** used as the HTTP service backend.

## Reviewer navigation

| Purpose | File/folder | What it provides |
| --- | --- | --- |
| **First-time course review** | [REVIEWER_GUIDE.md](REVIEWER_GUIDE.md) | Quick navigation, precise run prerequisites and demo sequence |
| **M4/M5 source review** | [m4_m5_source_review/](m4_m5_source_review/) | Sanitized preparation source, configs, split manifest and training CSVs |
| **M8 release prototype** | [m8_manifest_driven/](m8_manifest_driven/) | FastAPI source, manifest validation, settings and requirements |
| Historical HTTP code | [reference_service/](reference_service/) | Archival service — not the later reviewed candidate |
| Older notebooks | [archive/](archive/) | Sanitized historical artifacts — **not** Run-all reproduction |
| **Exact evidence scope** | [PHASE2_EVIDENCE_STATUS.md](PHASE2_EVIDENCE_STATUS.md) | Measured results vs missing/limited results |
| **M8 latest follow-up** | [M8_FOLLOWUP_2026-11-21.md](M8_FOLLOWUP_2026-11-21.md) | Team's saved Colab HTTP, ONNX and mask-comparison measurements |
| Privacy before publication | [RELEASE_PRIVACY_CHECKLIST.md](RELEASE_PRIVACY_CHECKLIST.md) | Review gates; do not upload checkpoints or private report |

## W&B training evidence

- [M4 detection run — `epqdtowi`](https://forge.coreweave.com/wandb/sultan--almutairi/AI251P-Waste-Phase2/runs/epqdtowi?nw=nwusersultanalmutairi) — recorded detection run; completion state not independently established by this README.
- [M5 original run — `c6kv4slq`](https://forge.coreweave.com/wandb/sultan--almutairi/AI251P-Waste-Phase2/runs/c6kv4slq?nw=nwusersultanalmutairi) — shown as **Crashed**.
- [M5 resumed run — `pkty4rqs`](https://forge.coreweave.com/wandb/sultan--almutairi/AI251P-Waste-Phase2/runs/pkty4rqs?nw=nwusersultanalmutairi) — shown as **Finished**.

The two M5 runs form an interrupted-and-resumed training history; a run's status is not a substitute for saved model-evaluation results. Links were provided by the team and the resumed status was verified from the displayed run screen.

## Recorded data and evaluation

A sequence-grouped ZeroWaste-f split was recorded: **Train 1,851 / Validation 451 / frozen Test 929** images, with 1,272 further source frames excluded. Dataset access and full original build are private.

| Once-only frozen Test metric | Result |
| --- | ---: |
| M4 box mAP50 | 0.348695 |
| M4 box mAP50–95 | 0.228974 |
| M5 mask mAP50 | 0.340408 |
| M5 mask mAP50–95 | 0.210736 |

These are average-precision metrics (AP confidence floor 0.001, NMS IoU 0.50), **not** service operating-point Precision/Recall/F1. The local service uses confidence **0.25** and NMS IoU **0.50**.

Additional evidence kept distinct from the above Test results:

- M4 Validation: confidence and NMS sweeps, error gallery, normalized confusion matrix and size-stratified recall. The team additionally reviewed four *purposively selected* failure-gallery frames (5 TP / 9 FP / 13 FN on those four only), documenting possible causes without asserting causality.
- M5 Validation: a 451-image baseline comparison, a selected 24-image mask-IoU/Dice audit, class-count MAE and an error gallery. A separate 451-image full-GT audit reported mean mask IoU 0.4078 and Dice 0.4398 under its documented protocol; three batch montages were qualitatively reviewed (not individual-mask manual verification).
- M8: manifest-checked PyTorch service, structured JSON, timed HTTP experiments, ONNX exports and bounded parity audits. See [21 Nov follow-up](M8_FOLLOWUP_2026-11-21.md).
- Two five-member extensions: **ResNet18 image retrieval** and **CLIP four-known-material suggestions**, compared to an RGB-histogram baseline on 200 balanced frozen Test ground-truth crops. These are **crop-level advisory checks**, not end-to-end/unknown-class recognition.
- Separate TACO domain audit: **227 selected images**, M4 box mAP50 **6.99%**; neither a substitute for ZeroWaste Test nor a controlled domain-shift experiment.

## Running the M8 prototype

Read [REVIEWER_GUIDE.md](REVIEWER_GUIDE.md) before installation. The source **requires the exact private authorized checkpoints** and an environment with the right PyTorch CPU builds. It verifies model-file SHA256 on startup. The API binds to localhost for tests; do not publicly expose this unauthenticated prototype.

```bash
cd phase2/m8_manifest_driven
# After restoring the exact private weights and compatible packages:
python -m uvicorn service:app --host 127.0.0.1 --port 8000
# In another terminal:
curl http://127.0.0.1:8000/health
curl -F "file=@/path/to/authorized_validation_image.jpg" http://127.0.0.1:8000/predict
```

**Additional M8 check (22 Nov):** A team member cloned the public source at commit `08f4bc0107cf5f9122508c29e95e607f6a1156d1` in a fresh Colab notebook, restored exact private weights after SHA256 verification and observed `/health` HTTP 200, `/predict` HTTP 200 on one Validation replay image, and HTTP 400 for an invalid image (3 detections, 2 associated masks). Evidence is in the private course bundle. This is a bounded service smoke test, **not** full independent training, a clean-room dependency install, a Test rerun, or a network load benchmark.

**Reproducibility status:** The source is reviewable; a clean-room Train/Val rebuild and full independent training execution are not established by this public branch. Do not rerun the original once-only Test split. Private raw results and the complete course PDF are delivered through the designated academic submission.

## Attribution

ZeroWaste-f: Bashkirova et al., *ZeroWaste Dataset: Towards Deformable Object Segmentation in Cluttered Scenes*, CVPR 2022 ([source](https://ai.bu.edu/zerowaste/), [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)). YOLO11 from Ultralytics; frozen ResNet18 / CLIP are separately attributed in the course report.
