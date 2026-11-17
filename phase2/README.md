# Phase 2 — source publication staging (review branch)

**Project 9:** Waste Recognition and Segmentation on Conveyor Belts  
**Course:** AI251P Applied Computer Vision  
**Status:** In review; **not** a complete Phase 2 release or final submission.

This review branch is intentionally separate from the original Phase 1 `main`. It documents the verified scope of Phase 2 and an evidence-aware publication checklist while the executable source and model artifacts are checked for privacy, license compliance, reproducibility and consistency. Do not describe this branch as a complete deployment.

## System and frozen results

- M4: fine-tuned YOLO11n detector, four classes: `cardboard`, `metal`, `rigid_plastic`, `soft_plastic`.
- M5: fine-tuned YOLO11n-seg instance segmenter; training ended by early stopping at epoch 36, selected checkpoint from epoch 21.
- M8: local FastAPI/Uvicorn HTTP service running **PyTorch CPU**, separate ONNX export and sampled parity analysis. ONNX is **not** the served backend.
- Extensions: frozen ResNet18 visual retrieval and zero-shot CLIP as advisory operator-assistance tools; these do **not** claim detection of unknown materials.

Original once-only full-scene Test, **929 ZeroWaste-f images**; nominal input 640, AP confidence floor 0.001, NMS IoU 0.50:

| Metric | Recorded Test result |
| --- | ---: |
| M4 box mAP50 | 0.3486949280 |
| M4 box mAP50–95 | 0.2289738041 |
| M5 mask mAP50 | 0.3404084177 |
| M5 mask mAP50–95 | 0.2107355222 |

Deployment operating confidence is **0.25**, and the AP values must not be mistaken for operating-point precision/recall/F1. Complete Test operating-point error analysis and counting accuracy remain unmeasured in the available records. The four numerical AP acceptance thresholds were set during Phase 2 before Test, **not** before all experiments; the HTTP latency target was retrospective. Industrial belt-speed and grasp reliability were not established.

The separate open-world comparison evaluated **200 balanced Test ground-truth object crops from 172 source images**, not whole-scene or unknown-class performance. On these crops, ResNet retrieval top-1 was 46.5% vs 37.5% RGB-histogram baseline; plain-prompt CLIP accuracy was 38.0% vs 37.5% baseline (its macro-F1 was lower).

## Source present on this review branch (not a final release)

- [Sanitized archival notebook](archive/Project9_Phase2_CORRECTED_v3_SOURCE_ONLY.ipynb): 52-cell source-only historical snapshot with outputs removed, archive password redacted and train/Test guards; it does **not** reflect all subsequent November results.
- [Archive explanation](archive/README.md): explains the exact provenance and why the notebook must not be rerun.
- [Historical FastAPI reference](reference_service/service.py) and [local-run instructions](reference_service/README.md): code extracted from that archived notebook; its manifest example uses reported model SHA256s. **Not** the newer manifest-driven implementation verified on 17 November, and not run against checkpoints during publication.
- [Evidence map](PHASE2_EVIDENCE_STATUS.md) and [release safety gate](RELEASE_PRIVACY_CHECKLIST.md).

No dataset ZIP, raw frames, model weights, API keys, student IDs, or final course report are published here. The current branch is **review-only**; the preserved original team artifacts and latest code/evidence have not all been transferred.

## Evidence and code required before merging

1. Replace or supplement the **sanitized historical M4/M5 source** with an approved, source-checked **current** execution notebook/scripts matching the completed M5 run and final release; the historical archive is not sufficient.
2. Obtain, review and publish the **newer manifest-driven M8 FastAPI source**, its tested pinned CPU requirements, and documented private checkpoint restoration. The historical reference currently published is not that newer version.
3. Verify exact source checksum references, frozen split manifest, training configuration, W&B links and recorded evaluation files. Publish only evidence licensed for redistribution.
4. Include representative failure figures only after reviewing image/data licensing and privacy; original ZeroWaste frames should not be redistributed by default.
5. Document Test-once protocol and post-hoc Validation diagnostics separately; never use frozen Test to retune thresholds.
6. Verify all five members' actual contributions **privately**; public GitHub must not include student IDs or personally identifying records.
7. Update this page with a reviewed **Phase 2 commit SHA** and independently checked reproduction instructions before declaring a release.

See [PHASE2_EVIDENCE_STATUS.md](PHASE2_EVIDENCE_STATUS.md) for the evidence-to-claim map and [RELEASE_PRIVACY_CHECKLIST.md](RELEASE_PRIVACY_CHECKLIST.md) for the publication gate.

## Current limitations

This staging branch includes a syntax-checked historical service and output-free notebook, but **has not** run model inference against the original data/checkpoints. It does not supply trained model files, a hosted service, the later reviewed M8 implementation or the reviewed 35-page report source. The instructor's final evaluation and requested accompanying PDF/Overleaf source ZIP are separate course submission deliverables.
