# AI251P Applied Computer Vision — Project 9

**Waste Recognition and Instance Segmentation on Conveyor Belts**  
KAUST AI251P capstone | Five-member team | Academic research prototype

## Start here

| Phase | Scope | Where to look |
| --- | --- | --- |
| **Phase 2 (M4, M5, M8 + two extensions)** | Object detection, instance segmentation, HTTP pipeline, evaluation and operator-assistance experiments | **[Phase 2 overview](phase2/README.md)** |
| Phase 1 (M1–M3) | TrashNet classification and data foundations | [Phase 1 source](Training_Notebook.ipynb) and [dataset card](dataset_card_with_audit_addendum.md) |

**Reviewing the Phase 2 submission?** Read the [two-minute reviewer guide](phase2/REVIEWER_GUIDE.md), then [source and evidence map](phase2/PHASE2_EVIDENCE_STATUS.md).

### Phase 2 — recorded results

The original **frozen ZeroWaste-f Test split contains 929 images**. The measurements below are from that recorded test, not new GitHub executions:

| Metric | Recorded result |
| --- | ---: |
| M4 box mAP50 | 0.348695 |
| M4 box mAP50–95 | 0.228974 |
| M5 mask mAP50 | 0.340408 |
| M5 mask mAP50–95 | 0.210736 |

The pipeline uses YOLO11n detection + YOLO11n-seg masks, matches same-class boxes and returns labels, bounding boxes, associated mask polygons, candidate pixel centroids and review flags. A local FastAPI service runs **PyTorch on CPU**. Exported ONNX models were tested separately; the HTTP service does **not** serve ONNX.

**[21 November M8 follow-up checks](phase2/M8_FOLLOWUP_2026-11-21.md):** 25/25 HTTP responses succeeded for one repeated Validation image, p95 latency 643.95 ms, sampled process RSS 864.90 MiB; a separate ONNX comparison shows high geometric agreement *only on matched objects*, with unmatched predictions disclosed.

### Scope and integrity

- This public branch contains reviewed/sanitized code and selected metadata. It is **not a self-contained reproduction of every experiment**.
- Original ZeroWaste-f imagery, protected archives, private model checkpoints, student IDs, credentials and the course-submitted PDF are **not published** here.
- Do **not** rerun the original once-only Test evaluation for model selection. Validation and Test evidence are distinguished in the report and evidence map.
- The demo is a local research prototype; **no industrial conveyor-rate, autonomous grasping or production deployment** is claimed.
- The academic report, full private evidence bundle and model weights are submitted/shared only through the approved course channel.

## Phase 1 historical materials

- [Training notebook](Training_Notebook.ipynb) — original three TrashNet classification configurations.
- [Dataset card and audit](dataset_card_with_audit_addendum.md), [Phase 1 run provenance](WAND_B_RUNS_AND_PROVENANCE.md).
- [Earlier retrieval work](KAUST_Project9_Advanced_Image_Retrieval.ipynb), [ZeroWaste crop classification audit](ZEROWASTE_EXTERNAL_VALIDATION.md).

The Phase 1 reported TrashNet fine-tuned ResNet18 result (90.14% accuracy on 507 test images) is **not** a conveyor-image detection score. A distinct ZeroWaste-f ground-truth crop classification check reported 21/75 correct; it is neither a Phase 2 M4 nor M5 result.

### Dataset attribution

ZeroWaste-f: Bashkirova et al., *ZeroWaste Dataset: Towards Deformable Object Segmentation in Cluttered Scenes* (CVPR 2022). [Official dataset](https://ai.bu.edu/zerowaste/) | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Obtain data through authorized original sources; this repository does not redistribute it.
