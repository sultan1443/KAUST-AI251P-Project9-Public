# Phase 2 — Project 9

**Project:** Waste Recognition and Segmentation on Conveyor Belts  
**Course:** AI251P Applied Computer Vision  
**Status:** Public source review — final release verification in progress.

## System Overview

The project combines four components:

- **M4 — Object Detection:** YOLO11n detector for cardboard, metal, rigid plastic, and soft plastic.
- **M5 — Instance Segmentation:** YOLO11n-seg for object masks and candidate pixel centroids.
- **M8 — Integration:** Local FastAPI service using PyTorch CPU, with `/health` and `/predict` endpoints.
- **Extensions:** ResNet18 visual search and zero-shot CLIP for operator assistance.

## Recorded Test Results

The original frozen ZeroWaste-f Test evaluation used 929 images.

| Metric | Result |
|---|---:|
| M4 Box mAP50 | 0.348695 |
| M4 Box mAP50–95 | 0.228974 |
| M5 Mask mAP50 | 0.340408 |
| M5 Mask mAP50–95 | 0.210736 |

These are AP evaluation results, not precision and recall at the service operating confidence of 0.25.

A separate external TACO evaluation used 227 selected images with 398 annotated target objects. M4 achieved 6.99% box mAP50 and 3.96% mAP50–95 on that selected external subset.

## Published Source

- [`archive/`](archive/) — Sanitized historical notebook and review-only Phase 2 notebook. These are not complete executable reproduction packages.
- [`reference_service/`](reference_service/) — Historical M8 FastAPI implementation.
- [`m8_manifest_driven/`](m8_manifest_driven/) — Updated M8 V2 FastAPI source, manifest validation, configuration, requirements, and run instructions.
- [`PHASE2_EVIDENCE_STATUS.md`](PHASE2_EVIDENCE_STATUS.md) — Experiment evidence and remaining verification tasks.
- [`RELEASE_PRIVACY_CHECKLIST.md`](RELEASE_PRIVACY_CHECKLIST.md) — Public-release safety checklist.

The newer M8 V2 source has been published in this review branch. Its recorded functional tests covered two selected Validation crops and input-validation cases; they are not a full deployment or throughput benchmark.

## Reproducibility and Limitations

The complete dataset, original model checkpoints, and private course submission files are maintained separately and are not included in this public repository.

The original M8 HTTP benchmark reported p95 latency of 1284.87 ms over 25 serial requests on one Validation image, using an earlier CPU service configuration.

This repository does not establish industrial conveyor throughput, physical grasp reliability, sustained hosting, or complete end-to-end production readiness.

Current M4/M5 execution source, evaluation evidence, dependency compatibility, and independent reproducibility must be reviewed before labeling this branch a complete Phase 2 release.

## Submission

The final report and supporting evidence are submitted through the course's designated private submission channel.

The project team has reviewed and approved its report and contribution statements. The public GitHub release and its final commit reference remain subject to verification.
