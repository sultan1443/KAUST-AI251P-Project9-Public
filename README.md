# AI251P Applied Computer Vision — Project 9 (Phase 1)

**Topic:** Waste Recognition and Segmentation on Conveyor Belts  
**Team:** Five students; student names and IDs are recorded in the course-submitted PDF, not in this public source repository.  
**Phase 1 scope:** TrashNet data foundations and material classification (M1–M3). Detection and instance segmentation are later-phase work.

## Contents

- `Training_Notebook.ipynb`: Phase 1 TrashNet preprocessing and three classification model configurations (CNN from scratch, frozen ResNet18, fully fine-tuned ResNet18).
- `config.json`, `requirements.txt`: experiment settings and package versions.
- `class_counts.csv`, `exact_duplicates_removed.csv`: retained class splits and recorded identical-file removals.
- `dataset_card_with_audit_addendum.md`: provenance, splits, audit, and limitations.
- `label_audit_review_completed.csv`: **one team member's** review of 60 sampled image previews; 55 marked correct, 5 flagged for further checking. These flags are not verified ground-truth relabels.
- `WAND_B_RUNS_AND_PROVENANCE.md`: links to logged experiment histories, retrospectively uploaded from original CSV history files.
- `Create_ZeroWaste_Crops_From_COCO.py`, `Evaluate_ZeroWaste_Annotated_Crops.ipynb`: earlier external-domain helper scripts.
- `KAUST_Project9_Advanced_Image_Retrieval.ipynb`, `ADVANCED_RETRIEVAL_RESULTS.md`: executed ImageNet-pretrained ResNet18 retrieval extension; Precision@1 = 80.47% on 507 held-out TrashNet queries (not a conveyor test).
- `KAUST_ZeroWaste_External_Test_Colab.ipynb`, `ZEROWASTE_EXTERNAL_VALIDATION.md`, `zerowaste_predictions.csv`, `zerowaste_evaluation_metrics.json`, `classification_report.json`: **completed limited ZeroWaste-f validation-crop classification test** (75 annotated GT crops; 28.00% top-1, 34.37% macro-F1 for three mapped labels). No raw ZeroWaste images are redistributed.

## Reproduce and limitations

Open `Training_Notebook.ipynb` in Google Colab and follow its data-acquisition instructions. Training data and trained checkpoints are **not included**; dataset redistribution is subject to the source's license. Run settings are in `config.json` and `requirements.txt`; reproducibility requires executing the notebook on the real dataset. The originally saved runs are described in the W&B provenance note. 

**Recorded outcome:** selected fine-tuned ResNet18 achieved 90.14% accuracy on the held-out TrashNet test set (507 images). This TrashNet result is **not** a conveyor-belt ZeroWaste accuracy measurement. A *separate* small ZeroWaste-f annotated object crop test yielded 28.00% top-1 accuracy (21/75; 25 distinct source frames from each of cardboard, metal and plastic). It measures classification from **ground-truth crops**, not detection, segmentation or full industrial throughput. Independently rerunning the full original training and verifying flagged labels on original-resolution images remain outstanding.

## Access for course assessment

The instructor needs access to this code repository, the W&B runs, and the dataset card. W&B project visibility was tested in a signed-out browser (public project overview; three retrospective runs). For privacy, full names, student IDs, private tokens, original image data, and model checkpoints are excluded from this public repository; the full team is identified in the privately submitted course PDF.
