# Public-source privacy review — 21 November 2026

**Scope:** Public repository `sultan1443/KAUST-AI251P-Project9-Public`, Phase 2 review branch, plus selected historical addition commits. **This is a targeted review; it is not a third-party security certification.**

## Checks performed

- Inspected the published tree, notebook files, services, manifests, selected reports/CSV metadata and README/release documentation.
- Applied automated pattern checks for common hard-coded access tokens, API keys, password assignments, student ID values and personal email patterns to reviewed source/text files.
- Inspected notebook execution metadata and outputs: the inspected notebooks were stored without execution outputs; no saved executed output cells were found.
- Specifically inspected the large archived public-review notebook (about 1.1 MB). Its archive-password assignment is a **redaction placeholder**, **not** a valid disclosed password. It contains local Google Drive example paths, not model/data binaries.
- Inspected earlier GitHub commits that originally added the two Phase 2 archived notebooks, sanitized M4/M5 notebook, M8 service source, and Phase 1 starter files for apparent credential additions.
- Inspected the repository's ignore rules: model checkpoint extensions, archive ZIPs, dataset directories, environment/credential files and notebook checkpoints are ignored.

## Findings

**No confirmed exposed live password, API key or private checkpoint was identified in the files and sampled addition commits reviewed.** The repo contains **public file paths** and **model hash digests**, which are not authentication secrets on their own. Public code can include historical local runtime paths; treat them as metadata, not evidence that the private data is in GitHub.

**Important boundary:** An automated scan cannot prove absence of every secret. Historical Git objects, nonstandard tokens, archived links, access policies and third-party redistributability require manual owner review. The larger untrusted codebase and dependency security were not independently pen-tested.

## Team approval status

The team representative confirmed in the project conversation on **21 November 2026** that all **five members agree**. This records the representative's confirmation; separate signed authorizations or each teammate's independent identity were not checked through GitHub.

## Public release boundaries

- Never publish actual dataset archive passwords, API credentials, original ZeroWaste-f images and annotations without appropriate rights, original model binaries, student IDs or the course-submitted private PDF.
- Do not publish saved Validation/Test data or private JSON raw evidence merely to make the repo look more complete.
- Keep the service bound to localhost; it has no authentication. ONNX exports are tested **separately**, not used by the HTTP service.
- The original frozen Test results are once-only and must not be rerun for tuning.
- Team approval and this privacy review do **not** establish full source reproducibility, license approval, live service security, or readiness to merge.

## Release decision

**Public review branch can be shared for academic source review, with its limitations disclosed.** The draft PR should stay unmerged until the team explicitly authorizes a release and reviews the final diff/history/license conditions. The private course PDF and source bundle must point to the *actual final commit SHA*, not a previous commit.
