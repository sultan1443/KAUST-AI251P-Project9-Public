# Phase 2 evidence-to-claim map

This index is reconstructed from the supplied **Project9Team_Phase2_S.pdf (35 pages; revised 17 Nov 2026)**. Paths named below are **references claimed by that report**, not files verified to be present in this GitHub branch. Do not label them as committed, hosted or independently reproduced until verified.

| Area | Recorded evidence / outcome | Missing or limited | Referenced artifact / path |
| --- | --- | --- | --- |
| Grouped data | 1,851 Train, 451 Val, 929 Test, 1,272 excluded; sequence-derived partitions | Cross-group visual-duplicate audit not established | `data_protocol/ef6b35d2ba7f/split_manifest.csv` |
| M4 | Epoch 34 early-stop, best epoch 19; frozen Test box mAP50 = 0.3486949280 and mAP50–95 = 0.2289738041 | Full Test P/R/F1 at service confidence 0.25; size recall; FP taxonomy | M4 `results.csv`, `args.yaml`, `evaluation/FINAL_TEST_ONCE/results.json`, `evaluation/M4/confidence_sweep_corrected.csv` |
| M4 diagnostic | Four deliberately selected Val frames: 5 TP / 9 FP / 13 FN (18 GT), **not Test** | Not representative; do not promote to full-set performance | `evidence/failure_gallery_VAL/` |
| M5 | Early-stopped epoch 36; best epoch 21; Test mask mAP50 = 0.3404084177, mAP50–95 = 0.2107355222 | Full Test IoU/Dice and counting accuracy not measured | M5 `results.csv`, `args.yaml`, `evaluation/FINAL_TEST_ONCE/results.json` |
| M5 paired baseline | 451 Val frames; reconstructed 0-step 4-head mask mAP50–95 = 0.0075264471, tuned = 0.2965478588 | Reconstructed initialization is not original epoch 0; comparison not Test | `saved_evidence/M5_posthoc_VAL/` |
| M5 mask subset | 24 Val frames, mean IoU 0.4011, mean Dice 0.4357 | Not full Test; 50 of 117 GT instances unmatched | `evaluation/M5/mask_iou_dice_VAL_SUBSET24.csv` |
| M5 failure gallery | Four selected Val frames: 6 TP / 8 FP / 12 FN; matching uses same-class mask IoU 0.5 | No full-Test taxonomy or raw binary-mask recheck in source report | `evidence/failure_gallery_VAL/` |
| Original M8 | FastAPI local PyTorch CPU, POST /predict and GET /health, sampled HTTP p50/p95/p99 442.68/1284.87/1669.94 ms (25 serial requests after 2 warmups) | No persistent endpoint; 901.12 MiB post-request RSS not continuous peak | `evaluation/M8/benchmark_requests.csv` and summary |
| M8 stage profile | Separate instrumented 25-request run; client p50/p95 416.672/1100.856 ms | Not controlled optimization or diverse-load test | `evidence/M8_stage_timing_VAL/` |
| ONNX | Opset 17 exports; later M5 sample audit matched 38/38 boxes, binary-mask IoU/Dice 1.0 on eight Val images | Raw tensor and full-split parity unmeasured; ONNX not HTTP backend | `evaluation/release_audit/` |
| Image replay | 30 ordered Val frames in 10s MP4 displayed at chosen 3 fps; processing loop ~1.818 images/s | Not native camera capture / industrial 3fps evidence | `evidence/ZeroWaste_ordered_replay_VAL/` |
| Visual Search | 200 balanced Test GT crops: ResNet top-1 46.5%, histogram 37.5%; Hit@5 87.5% vs 80.0% | Crop-level known-class evaluation, not full-scene or unknown detection | `evidence/Extensions_FINAL_TEST_ONCE/` |
| CLIP | Same Test crops: accuracy 38.0%, histogram 37.5%; macro-F1 0.3585 vs 0.3714 | No CLIP overall superiority; four known classes only | `evidence/Extensions_FINAL_TEST_ONCE/` |
| /assist | Five saved local HTTP Val requests with advice, unchanged M4 predictions | No measured operator outcome or human decision | `evidence/Extensions_operator_VAL/` |
| Phase 2 release | Report identifies older public Phase 1 commit `2203c58303ca6807919c64e237e4e39c7a10024d` | Full Phase 2 source/evidence publication and independently reproducible release not verified | Pending SHA |

## Interpretation rules

- Never substitute Validation metrics for frozen Test metrics.
- The acceptance limits on the four AP values were introduced **during Phase 2 before Test**, not in the Phase 1 report. The HTTP p95 1500 ms limit was retrospective.
- The Test AP confidence floor 0.001 differs from the HTTP operating confidence 0.25.
- The extension Test comprises 200 ground-truth **crops** from 172 frozen Test images; it did not rerun M4/M5 whole-scene Test.
- None of the provided figures validate physical robot grasping, factory speed or sustained industrial sorting.
- Source paths in this index are a **checklist** for collecting evidence from the project owner, not proof the GitHub repository contains them.
