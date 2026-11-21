# Phase 2 — public-source release and privacy checklist

**Updated 21 November 2026** · **This branch is a review candidate. Do not mark it as a completed release or merge the PR before team and source/privacy review.**

## Verified by source inspection / recorded evidence

- [x] Sanitized Phase 2 source exists under [m4_m5_source_review/](m4_m5_source_review/) and [m8_manifest_driven/](m8_manifest_driven/) on this review branch.
- [x] The original full 107-cell notebook was **not uploaded unchanged**; historical copies are sanitized and explicitly archived under [archive/](archive/).
- [x] No raw ZeroWaste image archives or original model checkpoint binaries are included in the reviewed public tree.
- [x] Course-submitted PDF with student names/IDs is kept separate from public code.
- [x] Current README explicitly distinguishes CPU PyTorch HTTP service from separately tested ONNX exports.
- [x] Latest [M8 follow-up](M8_FOLLOWUP_2026-11-21.md) records both successful checks and unmatched ONNX predictions rather than claiming full parity.
- [x] README and [evidence-to-claim map](PHASE2_EVIDENCE_STATUS.md) mark measured versus unmeasured claims distinctly.

## Still required before a public merge / release

- [ ] An authorized team member reviews **all** published notebook cells, metadata, figures and history for credentials, archive passwords, private sharing links, protected dataset content and student identifiers.
- [ ] All five teammates verify descriptions of their actual work and explicitly approve the **private submission** and publication-safe source.
- [ ] Validate current setup instructions in a fresh compatible environment with **authorized** weight/data access; record exact Python/PyTorch dependencies and results. Do not label a source-only syntax check as a full reproduction.
- [ ] Confirm external data, model, library and diagram licensing/attribution and that any visual example uploaded publicly is licensed for redistribution.
- [ ] Verify all paths and links on the eventual release branch, and ensure the privately submitted PDF points to the actual commit containing Phase 2 source.
- [ ] Inspect the final public diff and previous Git history for secrets and personal information, not only the current files.
- [ ] Keep Checkpoint `best_det.pt`, `best_seg.pt`, original images, private evaluation JSON and course ID records out of the public repo.
- [ ] Preserve once-only frozen Test integrity. Do not re-run frozen Test or use it to choose thresholds.
- [ ] Decide with the team whether to merge this PR; merge is **not** required merely to submit a review-branch URL to Blackboard.

## Release boundary

The Phase 2 repository is useful for **code review and audit of reported measurements**, but cannot reproduce every result from the public checkout alone: raw data and weights are absent by design, and the complete source/evidence package is privately submitted through the approved course channel.

**Historical reference:** [reference_service/](reference_service/) is the earlier service and should not be described as the current M8 V2 implementation. [archive/](archive/) notebooks are archival; they are not intended for `Run all`.
