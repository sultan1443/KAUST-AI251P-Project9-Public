# Additional advanced component: visual image retrieval (Phase 1)

**Project 9, five-member team.** The extension is an additional experimental component, not a replacement for the M1-M3 classification experiments. Instructor acceptance of the five-member technical extension is separate.

## Recorded experiment
The Colab notebook was executed on the original TrashNet data and its saved results are bundled with this folder. An ImageNet-pretrained ResNet18 (fixed backbone, NOT the six-class fine-tuned checkpoint) extracts 512-dimensional L2-normalized embeddings from 160x160 RGB images. Nearest-neighbour gallery search uses cosine similarity, without a score cutoff.

- Reference gallery: 1,509 TRAIN samples. Queries: 507 held-out TEST samples. The original grouped split is reused; validation examples are not in either group.
- Precision@1: **80.47%** (408/507 queries); expected random-gallery baseline **18.59%**.
- Precision@5 **73.73%**; Hit@5 **95.66%**; mean AP@10 **61.95%**; mean RR@10 **87.38%**.
- The saved `retrieval_metrics.json` includes 95% query-bootstrap confidence intervals.
- Per-class Precision@1 is lowest for heterogeneous `trash` class, **53.85%** (14/26 queries).

## Verification and files
The original `split_manifest.csv` (SHA-256 verified byte-for-byte) contains 2,524 cleaned images, split 1,509 train / 508 val / 507 test. The 507 query names match the manifest's held-out test split; no train/test group ID is shared. The query-level CSV means reproduce the numeric summary exactly.

- `KAUST_Project9_Advanced_Image_Retrieval.ipynb`: executable retrieval workflow (upstream data download, hash checks, pretrained embeddings, ranking and output ZIP).
- `retrieval_metrics_core.py`: metric definitions with a simple toy-data smoke test.
- `retrieval_metrics.json`: summary scores, intervals and encoder provenance.
- `retrieval_queries.csv`: per-query score, top-1 label and cosine score, 507 lines of results.
- `retrieval_per_class.csv`: per-class retrieval summaries.
- `split_manifest.csv`: original dataset split and SHA-256 hash manifest.

**Limitations.** These metrics measure same-dataset retrieval on TrashNet, **not** conveyor-domain accuracy and **not** the classification test accuracy of the fine-tuned ResNet18. The retrieved gallery illustration uses raw dataset photos, which are not redistributed in this public repository. A subsequent independent rerun is not documented here.
