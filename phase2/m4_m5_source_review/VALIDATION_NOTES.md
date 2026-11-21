# Validation performed for this public-source review candidate

- Checked notebook syntax and structure; all code cells start without saved outputs or execution counts.
- Executed every notebook code cell with the default switches OFF, from the unzipped package directory. They ran successfully without images, weights, GPU, network access, training, or test inference.
- Verified the frozen public manifest has 4,503 entries: 1,851 Train, 451 Validation, 929 Test, 1,272 Excluded. Verified that active sequence groups do not overlap.
- Tested detection label conversion against a two-image synthetic COCO fixture: generated correct YOLO labels and YAML without a Test entry, and correctly refused to replace a conflicting build / reused a matching build.
- Verified Python compilation of the separate data-preparation script and all notebook code cells.
- Verified no raw dataset or model weights are packed; the public manifest omits `source_path` and `annotation_path`.
- **Not yet tested:** full actual ZeroWaste-f build, segmentation conversion with the exact Ultralytics runtime, training from the beginning, PyTorch weight parity, M8, or any actual new validation benchmark. No frozen Test was run.
