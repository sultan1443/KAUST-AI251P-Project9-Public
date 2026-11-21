# Phase 2 — evidence-to-claim map (review branch)

**Updated 21 November 2026** from the team's latest 19-page course report and saved Colab records. These are **reported measurements with private supporting artifacts**, **not** experiments rerun by GitHub. See [reviewer guide](REVIEWER_GUIDE.md) and [M8 follow-up](M8_FOLLOWUP_2026-11-21.md).

| Area | Recorded evidence | Evaluation scope / caveat | Public source |
| --- | --- | --- | --- |
| Grouped ZeroWaste-f split | Train 1,851; Val 451; frozen Test 929; 1,272 excluded | Source-sequence groups separated; near-duplicate freedom not fully proved | [public split manifest](m4_m5_source_review/split_manifest_public.csv), [preparation script](m4_m5_source_review/phase2_data_prep.py) |
| M4 fine-tuning | YOLO11n, selected epoch 19; frozen Test box mAP50 **0.348695**, mAP50–95 **0.228974** | Test AP floor conf 0.001 and NMS 0.50; not service-threshold P/R/F1 | [configs, CSV](m4_m5_source_review/) |
| M4 confidence and NMS | Val macro P/R/F1 for conf 0.25 **0.4988 / 0.5262 / 0.5074**; NMS sweep | Interpolated class curves at IoU 0.50; not pooled Test or direct TP/FP/FN | Private PDF/evidence ZIP |
| M4 errors | Four selected Val frames: 5 TP / 9 FP / 13 FN; full-Val confusion plot also reported | Diagnostic samples and confusion-matrix settings differ; no full Test error taxonomy | Private PDF/evidence ZIP |
| M4 external TACO | 227 selected images; box mAP50 **6.99%**, mAP50–95 **3.96%** | Strict target mapping, incomplete source retrieval; separate external audit | Private PDF/evidence ZIP |
| M5 training and comparison | YOLO11n-seg, selected epoch 21; Val paired baseline mask AP50–95 **0.007526** vs **0.296548** | Baseline was reconstructed zero-step four-class head, not original epoch-zero checkpoint | [training CSV/configs](m4_m5_source_review/) |
| M5 original frozen Test | Mask mAP50 **0.340408**, mAP50–95 **0.210736** | 929 images; not a full-Test mask IoU/Dice | [recorded evidence status](README.md) |
| M5 mask and counting audits | 24 Val images, 117 GT, mean IoU **0.4011**, Dice **0.4357**; separate 451-image Val count MAE | Limited subset and separate Val settings; no physical pick-point success | Private PDF/evidence ZIP |
| M8 HTTP | Local checksum-checked FastAPI on PyTorch CPU | `/health` and `/predict`, not a permanently hosted service | [service](m8_manifest_driven/service.py), [manifest](m8_manifest_driven/release_manifest.json) |
| M8 original and stage benchmark | Original 25-request HTTP p95 **1284.87 ms**; separate stage profiling | Different Colab runtimes; cannot combine as controlled speed gain | Private PDF/evidence ZIP |
| M8 follow-up (21 Nov) | 25/25 HTTP; p50/p95/p99 **405.09/643.95/653.87 ms**, **2.09 images/s**, RSS snapshot **864.90 MiB** | One image repeated, CPU PyTorch, no sustained workload | [complete limitations](M8_FOLLOWUP_2026-11-21.md) |
| M8 ONNX | Exported M4/M5 ONNX files ran; one-image matched M4 boxes **2/3**, M5 **6/7 PT vs 8 ONNX**, mean mask IoU **0.991393** on 6 matched | ONNX not served by HTTP; unmatched predictions remain; conditional agreement, not GT accuracy | [M8 parity report](M8_FOLLOWUP_2026-11-21.md) |
| Ordered Validation replay | 30 sampled frames replayed through local HTTP; recorded loop about **1.82 images/s** | 3-fps MP4 was display rate, not actual capture/inference speed | Private video/evidence |
| Extension A: ResNet18 visual search | 200 balanced Test GT crops: top-1 **46.5%**, RGB histogram **37.5%** | Known-class crop retrieval, not end-to-end sorting | Private report and extension evidence |
| Extension B: CLIP suggestions | Same 200 Test GT crops: accuracy **38.0%**, histogram **37.5%**, macro F1 **0.3585** vs baseline **0.3714** | No overall superiority or unknown-class rejection proved | Private report and extension evidence |
| Team and course submission | Five members jointly contributed, with primary focus areas; report/source ZIP via Blackboard | Names and university IDs retained in private course documents | [reviewer guide](REVIEWER_GUIDE.md) |

## Critical open items — do not overstate completion

1. **M4:** no full frozen-Test Precision/Recall/F1 directly measured at service confidence 0.25; no complete Test recall-by-size or full FP localization/duplicate taxonomy. The old 451-image Validation build is not available in the latest Colab working directory; do not substitute Test.
2. **M5:** manual mask-inspection count and full-Test mean IoU/Dice/counting behavior not established; failure gallery and 24-image Val subset have restricted scope.
3. **M8:** public source alone cannot rerun checkpoints; full numerical ONNX parity does not hold for all predictions; no hosted authenticated service or independently verified industrial belt-rate benchmark.
4. **Extensions:** experiments advise only four known materials, not true unknown-material rejection; GT crops do not establish end-to-end performance.
5. **Release:** public GitHub branch and PR remain review candidates pending explicit privacy review, member approval and final source/release decision.

The original frozen Test remains once-only. Any new analysis must use legitimate Validation or separate clearly labeled evidence, not re-tune against Test.

## Primary evidence not redistributed publicly

- M4: `evaluation/M4/confidence_sweep_corrected.csv`, `evaluation/M4/val_map/`, failure-gallery artifacts.
- M5: `evaluation/M5/mask_iou_dice_VAL_SUBSET24.csv`, `evaluation/M5/M5_count_MAE_VAL.csv`, masks/failure galleries.
- M8: `evaluation/M8/benchmark_requests.csv`, stage-timing and manifest evidence, plus `evaluation/M8_DEMO_EVIDENCE/` (seven JSON records, 21 November).
- Extensions: `evidence/Extensions_FINAL_TEST_ONCE/`, operator-replay evidence and external TACO audit.
- Full 19-page PDF and supporting bundle: official private course submission, not this public repository.
