# Dataset Card — KAUST Project 9 (TrashNet)

- **Source:** https://huggingface.co/datasets/garythung/trashnet, resized archive (`dataset-resized.zip`). Original TrashNet attributed to Thung and Yang.
- **Purpose:** Material classification of single waste items; not an industrial conveyor benchmark.
- **License:** MIT as indicated by the dataset repository; follow source license, no rehosting raw photos.
- **Classes:** cardboard, glass, metal, paper, plastic, trash.
- **Verified after removal:** 2524 images; exact file duplicates removed: 3; damaged: 0.
- **Split:** stratified grouped ~60/20/20 via pHash (threshold <= 2 bit). Seed 42. See split_manifest.csv and class_counts.csv for exact counts.
- **Train/val/test roles:** train optimization; validation for model selection; test once after selection.
- **Image preprocessing:** RGB, training random crop + flip + brightness/contrast jitter, resize to 160, ImageNet normalization for comparability.
- **Audit update (uploaded review record, 29 Oct 2026):** The supplied `label_audit_review_completed.csv` contains choices for all 60 balanced preview images (10 per class): 55 marked correct and 5 marked incorrect (8.33% of this balanced sample). The flagged IDs are 34 (paper -> cardboard), 43 (plastic -> trash), and 51, 53, 57 (trash -> plastic). These are proposed relabels, not corrections validated against original high-resolution images. The CSV form records `Reviewer: (not specified)` for all rows and contains no free-text rationale. One member of the five-member team subsequently confirmed that they personally reviewed all 60 preview images on behalf of the team. The record is one member’s review, not five independent reviews. No dataset image label was changed and original experiment metrics are unchanged. An illustrative one-sided 95% Clopper-Pearson upper bound is 16.73% **only if** independent, random Bernoulli sampling holds; this equal-class sample does not establish that assumption, and the bound must **not** be generalized to all retained images. Full-resolution checks of the five flagged images remain outstanding. No consensus relabelling has been established.

- **Limitations:** white-background single-object images; strong domain gap to cluttered ZeroWaste conveyor; pHash groups reduce but cannot prove absence of scene/source leakage without camera/session metadata; class imbalance. ZeroWaste materials only partially align to six TrashNet classes.
- **Restrictions:** avoid redistribution of public datasets; retain image ownership and licenses; no people/PII expected but inspect external data.

## Class balance by split

| label_name   |   train |   val |   test |
|:-------------|--------:|------:|-------:|
| cardboard    |     240 |    82 |     81 |
| glass        |     302 |   100 |     99 |
| metal        |     243 |    82 |     84 |
| paper        |     355 |   119 |    120 |
| plastic      |     286 |    97 |     97 |
| trash        |      83 |    28 |     26 |
