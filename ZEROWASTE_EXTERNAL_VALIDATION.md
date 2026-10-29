# ZeroWaste-f external-domain crop validation (Phase 1 supplementary evidence)

**Status:** Actual Colab-generated results supplied by the team on 29 October 2026; saved JSON and CSV reviewed for internal consistency. This is not independently rerun by this reviewer.

- Model: TrashNet fine-tuned ResNet18 checkpoint, **no retraining**.
- Dataset: ZeroWaste-f official annotated **validation** frames; cropped ground-truth COCO boxes, not detected boxes.
- Classes mapped: cardboard, metal, plastic (ZeroWaste soft and rigid plastics mapped to plastic).
- Sample: 75 **distinct source frames**, 25 annotated object crops per mapped class; random seed 42, no unreadable crops recorded.
- Input: 160 x 160 RGB; predicted class = argmax, **no threshold**.
- **Top-1 crop classification accuracy: 21/75 = 28.00%.** Reported 95% exact CI (18.24%, 39.56%); conditional on the sampled crops.
- **Macro F1 over the three mapped labels: 34.37%.** Class recall: cardboard 15/25 (60%), metal 0/25 (0%), plastic 6/25 (24%).
- This performance is lower than the model's separate held-out TrashNet test score of **90.14%**; the test sets differ and must not be conflated.
- **Not a detection/segmentation evaluation:** no mAP, mask IoU, throughput, or all-frame accuracy is claimed.

Raw numeric evidence:
- `zerowaste_predictions.csv`: query/annotation identifiers, true mapped labels, model predictions and confidence.
- `zerowaste_evaluation_metrics.json`: sample and aggregate scores.
- `classification_report.json`: three mapped-class precision/recall/F1.
- `KAUST_ZeroWaste_External_Test_Colab.ipynb`: reproducible scripted evaluation and source archive instructions.

**Important limits:** The 75 crops are not representative of all conveyor footage. Distinct source frames were selected within the small sample, but scene/session independence is not documented. Metal recognition failed for all 25 evaluated crops. The public repository must not include any ZeroWaste-f source images or privately held training checkpoint; source licensing applies.
