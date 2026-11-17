# Phase 2 public-release and privacy gate

**Do not merge or label a release before completing this checklist.**

- [ ] Check all notebook cells, outputs and metadata for API tokens, W&B credentials, private URLs, drive paths revealing personal information, runtime authentication and embedded secrets.
- [ ] Remove executed notebook outputs and obsolete `FINAL TEST NOT RUN`, `M5 interrupted`, or `Due 15 November` statements from any notebook promoted as the *current* execution guide. Historical notebooks may be retained only with a prominent archival warning.
- [ ] Never publish or embed the dataset ZIP password; follow the official dataset access documentation instead. A historical local notebook contains a hard-coded archive extraction password and must not be published unchanged.
- [ ] Keep raw ZeroWaste image archives (about 7.5 GB), whole-source frames, original annotations if redistribution is not authorized, and model `best.pt`/`last.pt` binaries outside the public repository. Document official download routes, license and hashes.
- [ ] Keep student names/IDs, university account details, and correspondence in **private course submission**, not public repository.
- [ ] Check figure and crop redistribution rights; use public figures only with documented permission/license, or replace them with generated diagrams, small permitted examples, or private course evidence.
- [ ] Publish reviewed source code with stable requirements and exact startup commands; distinguish GPU training profile from CPU service profile.
- [ ] Include frozen split manifest hash, checkpoint SHA256, evaluation settings, W&B provenance and a reproducibility test performed by a second team member (record scope honestly).
- [ ] Validate no modified file or helper silently re-runs frozen 929-image M4/M5 Test or uses its metrics for selecting weights/prompts/thresholds.
- [ ] Confirm any original HTTP service uses **PyTorch CPU** despite separate ONNX exports; do not call it deployed ONNX.
- [ ] Verify `README` lists exact files present in repository, not just references to absent Drive artifacts.
- [ ] Obtain explicit review of Phase 2 claims, actual contributions, and submission content from all team members before opening the final course submission.

## Status on creation

- Main branch was inspected and its README identifies **Phase 1**, not a complete Phase 2 release.
- The available `Project9_Phase2_CORRECTED_v3.ipynb` is an **older historical notebook** with executed outputs, a hard-coded archive extraction password, and stale M5/Test status. It is **excluded** from this initial public review branch pending cleansing and updating.
- The 15-page short report and 35-page complete report are **not** uploaded here. The complete report has team IDs and should be submitted privately through Blackboard/Overleaf source as instructed.
- This branch intentionally contains publication notes and evidence mapping only, not trained source/checkpoints or a fully runnable system.
