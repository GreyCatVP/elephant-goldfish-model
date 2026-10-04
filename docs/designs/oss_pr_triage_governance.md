<!--
Copyright 2026 Google LLC.
SPDX-License-Identifier: Apache-2.0
-->

# Open-Source Pull Request Triage and Contributor Governance

*   **Author:** [@briansuchy](https://github.com/briansuchy)
*   **Status:** Approved
*   **Date:** 2026-09-29

--------------------------------------------------------------------------------

## Overview

This document specifies the contribution intake and triage architecture for the
Elephant & Goldfish Model (EGM) open-source repository
(`github.com/google/elephant-goldfish-model`).

As AI coding assistants and autonomous agents proliferate, open-source projects
face an asymmetric cost structure: external contributors can generate code,
speculative refactorings, and complex features in seconds with minimal effort,
while human maintainers bear the full cognitive cost of reviewing, verifying,
and maintaining those changes.

This design introduces a system of **good-faith speed bumps**: a non-punitive,
advisory intake funnel that prompts contributors to self-select into the
appropriate contribution track, affirms human accountability, and exercises the
full EGM methodology. Contributors planning large changes (`> 100` non-test
lines or `>= 3` core files in `skills/`, `agents/`, or `rules/`) are advised
to reach out to maintainers first via a GitHub Issue
(`.github/ISSUE_TEMPLATE/feature_proposal.md`). Once maintainers confirm
alignment (`status: approved-for-design`), the contributor submits a Stage-1
**Design Doc PR** (`Refs #<issue>`) adding `docs/designs/<name>.md` (authored
via `/egm-brainstorm`, `/egm-draft`, and `/egm-review`). When maintainers merge
the Design Doc PR, the specification is checked into the codebase and
maintainers manually transition the issue label to `status: approved-for-pr` for
the subsequent Stage-2 **Implementation PR** (`Closes #<issue>`).

--------------------------------------------------------------------------------

## The Problem

Unmoderated open-source contribution funnels experience four primary failure
modes in the presence of ubiquitous LLM tooling:

1.  **Unprompted Architectural Overhauls**: Contributors submit large (200+
    line) pull requests that rewrite core agent behaviors or prompts without
    prior consensus or alignment on requirements.
2.  **Reviewer Fatigue from Unverified Code**: Low-effort submissions that
    appear syntactically plausible but contain unverified logic, subtle
    edge-case regressions, or unvetted dependencies overwhelm the maintainer
    review queue.
3.  **Unaligned Spec and Code Dumps**: Contributors invest in sprawling feature
    implementations or verbose, unstructured prose without first reaching out to
    maintainers to verify project alignment or authoring a concise,
    plain-English EGM design document (`docs/designs/<name>.md`) to keep the
    repository's architectural record current.
4.  **High-Frequency Automated Agent Submissions**: Autonomous agents submit
    unprompted PRs and generate synthetic replies to code review comments
    without human understanding or oversight in the loop.

The core challenge is balancing accessibility for legitimate, targeted bug fixes
while establishing sufficient structure for major features without imposing
punitive auto-close bots that discourage community engagement.

--------------------------------------------------------------------------------

## Goals

*   **Human Accountability**: Codify an explicit policy in
    [`AI_POLICY.md`](../../AI_POLICY.md) and [`AGENTS.md`](../../AGENTS.md)
    requiring human understanding and review of all submitted code while
    encouraging responsible AI usage.
*   **Structured Self-Selection**: Implement a clean intake taxonomy in
    [`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md):
    *   `Bug Fix / Minor Patch` (`<= 100` non-test lines and `< 3` core files in
        `skills/`, `agents/`, `rules/`; no design document required).
    *   `Feature / Architectural Change -- Stage 1: Design Doc PR` (requires an
        aligned issue with `status: approved-for-design`, uses `Refs #<issue>`,
        and adds `docs/designs/<name>.md` + updates `docs/designs/README.md`).
    *   `Feature / Architectural Change -- Stage 2: Implementation PR` (requires
        an aligned issue with `status: approved-for-pr` and implements a merged
        `docs/designs/<name>.md` via `Closes #<issue>`).
*   **EGM Required**: Require features and architectural changes (`> 100`
    non-test lines or `>= 3` core files) to align with maintainers first and
    merge a full, checked-in EGM design document (`docs/designs/<name>.md`
    created via `/egm-brainstorm`, `/egm-draft`, and `/egm-review`) prior to
    implementation review so the repository's `docs/designs/` directory stays up
    to date with the codebase.
*   **Clear Change Summaries**: Require contributors to summarize all key
    changes and their motivation directly in the PR description for immediate
    reviewer context, while capturing scope boundaries (`Goals` and `Non-Goals`)
    in the checked-in EGM design document.
*   **Non-Blocking Advisory Automation**: Deploy a GitHub Action that detects
    large non-test diffs on bug-fix PRs and posts a non-punitive scope advisory
    recommending contributors reach out to maintainers and follow the EGM design
    process without auto-closing the PR.
*   **Runner Infrastructure Safeguards**: Enforce fork execution permissions in
    GitHub Actions to prevent unauthorized runner minute consumption.

--------------------------------------------------------------------------------

## Non-Goals

*   **Total AI Bans**: We do not prohibit or penalize the use of LLMs or AI
    tools in writing code or documentation.
*   **Unconditional Auto-Closing Ingestion Bots**: We will not deploy aggressive
    bots that summarily auto-close all pull requests lacking prior issue links
    on launch day. However, maintainers explicitly reserve the right to close
    spam, low-effort, or non-compliant PRs and to enable stricter automated
    enforcement against bad actors if abuse occurs.
*   **Statistical Text Detectors**: We strictly reject deploying probabilistic
    AI text classifiers due to documented high false-positive rates against
    non-native English speakers.
*   **Premature Hard Rate Limiting**: We will not impose automated per-user
    concurrency caps (e.g., 1 active PR per user) on launch day before empirical
    spam volume is observed, though maintainers may throttle or block abusive
    accounts as needed.

--------------------------------------------------------------------------------

## Key Design Decisions

*   **Diff Threshold Uniformity**: Maintain the uniform 100-line non-test diff
    threshold across all directories; any patch exceeding 100 non-test lines
    (even bug patching) warrants additional explanation and review context.
*   **Two-Stage Feature Progression**: Contributors first reach out to
    maintainers via a GitHub Issue
    (`.github/ISSUE_TEMPLATE/feature_proposal.md`). When maintainers agree the
    problem is worth solving, they apply `status: approved-for-design`,
    authorizing the contributor to open a Stage-1 **Design Doc PR** (`Refs
    #<issue>`, adding `docs/designs/<name>.md` + `docs/designs/README.md`
    authored via `/egm-brainstorm`, `/egm-draft`, and `/egm-review`). Reviewing
    the design specification in a dedicated PR enables line-by-line review
    comments and checks the approved doc into `docs/designs/` upon merge, at
    which point maintainers manually transition the issue label to `status:
    approved-for-pr` for the subsequent Stage-2 **Implementation PR** (`Closes
    #<issue>`).

--------------------------------------------------------------------------------

## Open Questions

*None.* All architectural decisions have been resolved.

--------------------------------------------------------------------------------

## Critical User Journeys (CUJs)

### CUJ 1: Submitting a Targeted Bug Fix

*   **Given**: An external developer discovers a typo or regex bug in a skill
    definition.
*   **When**: The developer opens a pull request, selects `[x] Bug Fix / Minor
    Patch`, modifies 15 lines of code in `skills/egm_brainstorm/SKILL.md`, and
    adds a 30-line test scenario in `skills/egm_brainstorm/test_scenarios.yaml`.
*   **Then**: The Scope Advisory GitHub Action triggers via
    `pull_request_target`, excludes the co-located `test_scenarios.yaml` file,
    verifies that non-test changes are `<= 100` lines and `< 3` core files, and
    remains silent. Code build and test CI workflows execute upon maintainer
    approval. Maintainers review and merge the fix without requiring a design
    document.

### CUJ 2: Proposing a New Skill or Major Capability

*   **Given**: A developer wants to contribute a new subagent, skill, or
    architectural change (`> 100` non-test lines or `>= 3` core files) to EGM.
*   **When**:
    1.  The developer reaches out to maintainers by opening a Feature Inquiry
        Issue (`feature_proposal.md`) outlining the problem statement and
        proposed scope (`Goals` vs. `Non-Goals`).
    2.  Maintainers confirm directional alignment and apply `status:
        approved-for-design`.
    3.  The developer runs the EGM workflow (`/egm-brainstorm` -> `/egm-draft`
        -> `/egm-review`) and opens a Stage-1 **Design Doc PR** (`Refs
        #<issue>`) adding `docs/designs/<name>.md` and registering it in
        `docs/designs/README.md`.
*   **Then**: Maintainers review the specification line-by-line, merge the
    Design Doc PR into `docs/designs/`, and manually transition the issue label
    to `status: approved-for-pr`. The contributor then opens the Stage-2
    **Implementation PR** (`Closes #<issue>`) referencing the merged
    `docs/designs/<name>.md`, summarizes all key changes in the PR body, and
    proceeds to maintainer code review.

### CUJ 3: Accidental Scope Creep on a Bug Fix

*   **Given**: A contributor intends to fix a bug, but refactors 200 lines
    across multiple skill definitions and checks `[x] Bug Fix / Minor Patch`.
*   **When**: The PR is opened.
*   **Then**: The Scope Advisory Action analyzes the diff, recognizes non-test
    changes exceeding 100 lines, applies `advisory: design-doc-suggested`, and
    posts an educational advisory comment recommending that the contributor
    reach out to maintainers (`status: approved-for-design`) and merge an EGM
    design document (`docs/designs/<name>.md`) before submitting large
    implementation changes. The PR remains open in the queue for maintainer
    discretion. If the contributor subsequently reduces the diff to `<= 100`
    lines and `< 3` core files (or switches to the Feature track), the workflow
    automatically removes the advisory label. Artificially splitting a single
    logical change across multiple smaller PRs (e.g., two 60-line PRs) to evade
    the 100-line threshold is explicitly prohibited by repository policy.

--------------------------------------------------------------------------------

## Technical Plan (Architecture)

The contribution architecture comprises four integrated subsystems: Governance
Policies, Ingestion Templates, Automated Advisory Engine, and Platform Perimeter
Hardening.

### 1. Governance Policies (`AI_POLICY.md` & `AGENTS.md`)

The repository's policy layer establishes enforceable boundaries for both human
contributors and AI coding agents:

*   **[`AI_POLICY.md`](../../AI_POLICY.md)**: Establishes human-in-the-loop
    accountability for AI-assisted contributions (prohibiting unreviewed
    autonomous PR creation, requiring interactive defense in review threads,
    and enforcing two-stage EGM alignment for features).
*   **[`AGENTS.md`](../../AGENTS.md)**: Defines hard operational constraints for
    automated coding agents operating in the repository (restricting push/PR
    capabilities, requiring human authorization for external actions, and
    prohibiting artificial PR splitting to circumvent scope limits).

### 2. Ingestion Templates

The ingestion layer introduces cognitive speed bumps at the point of
contribution:

*   **Pull Request Template ([`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md))**:
    Provides structured track selection (Bug Fix vs. Stage-1 Design Doc PR vs.
    Stage-2 Implementation PR), requires a concise summary of all key changes
    made and why, mandates a human accountability affirmation, and specifies
    verification steps.
*   **Feature Inquiry Issue Template ([`.github/ISSUE_TEMPLATE/feature_proposal.md`](../../.github/ISSUE_TEMPLATE/feature_proposal.md))**:
    A low-friction template (`labels: ["feature-inquiry", "needs-triage"]`) for
    contributors to outline problem statements and high-level scope (e.g., from
    `/egm-brainstorm`) so maintainers can confirm directional alignment
    (`status: approved-for-design`) before a design document is drafted.

### 3. Automated Scope Advisory Engine (`pr-scope-advisory.yml`)

The advisory engine operates as a non-blocking GitHub Actions workflow.

*   **Workflow Execution**: Triggered on `pull_request_target` (`opened`,
    `edited`, `synchronize`, annotated with `# zizmor: ignore[dangerous-triggers]`)
    using commit-pinned `actions/github-script@f28e40c7f34bde8b3046d885e986cb6290c5673b` (`v7.1.0`).
*   **Diff Calculation Engine**:
    *   Fetches the paginated list of modified files via GitHub REST API
        (`github.rest.pulls.listFiles`), capped at 3 pages (`300` files).
    *   Applies a path-aware filter to omit non-logic changes:
        *   **Excludes**: General documentation and co-located skill test docs
            (`(^|\/)docs\/|(^|\/)(README|TEST)\.md$`), lockfiles
            (`.*\.lock$|package-lock\.json$`), and test files or scenarios
            (`(^|\/)(tests?|testdata)\/|((^|\/)test_[^/]+|_test|\.test|\.spec)\.[a-zA-Z0-9]+$`).
            Consequently, both dedicated **Design Doc PRs** (modifying only
            `docs/designs/<name>.md` and `docs/designs/README.md`) and co-located
            skill test files (`skills/<skill>/TEST.md` and
            `skills/<skill>/test_scenarios.yaml`) are excluded from non-test
            code and core file counts.
        *   **Exempts**: Core executable Markdown definitions in `skills/**`,
            `agents/**`, and `rules/**` (such as `SKILL.md`) are explicitly
            treated as production logic.
    *   Sums non-test lines added and deleted (`file.changes`).
    *   Counts non-test core architectural definition files touched (`skills/`,
        `agents/`, `rules/`).
*   **Evaluation Heuristics**:
    *   *Bug Fix Track*: Fires if author checked `Bug Fix / Minor Patch` AND
        (`nonTestChanges > 100` OR `coreFilesCount >= 3` OR `files.length >=
        300`).
    *   *Feature Track Passthrough*: PRs with `Feature / Architectural Change`
        checked pass through the bug-fix scope advisory without triggering a
        warning (automated validation of design doc paths on Feature PRs is
        tracked under `## Future Improvements`).
*   **Bidirectional Label Handling & Idempotency**:
    *   Checks existing comments (via paginated `github.rest.issues.listComments`)
        for `<!-- egm-scope-advisory -->`.
    *   If thresholds are breached and comment is absent, posts advisory
        recommending reaching out to maintainers (`status: approved-for-design`)
        and submitting an EGM design document PR (`docs/designs/<name>.md`), and
        adds `advisory: design-doc-suggested`.
    *   If the diff is subsequently trimmed to `<= 100` lines and `< 3` core
        files (or the contributor switches to the Feature track), removes the
        `advisory: design-doc-suggested` label.
    *   **Maintains PR open state (zero auto-closures).**

### 4. Platform Perimeter Hardening

*   **Fork Workflow Isolation**: Configure GitHub Actions to **"Require approval
    for all outside collaborators"**. Workflows on external forks
    (`pull_request`) will not execute until a maintainer reviews the diff for
    malicious scripts or compute abuse.
*   **Bifurcated Execution Model**: The Scope Advisory workflow executes
    immediately upon submission via `pull_request_target` in the base repository
    context without checking out untrusted fork code. Build and test workflows
    execute on `pull_request` and are gated by maintainer approval.
*   **Least-Privilege Token Permissions**: The advisory workflow operates with
    minimal permissions: `pull-requests: read`, `issues: write`, and `contents:
    read`. No repository code write or secret access is granted.

--------------------------------------------------------------------------------

## Alternatives Considered

### Alternative A: Hard Gatekeeper Bot with Immediate Auto-Close

*   **Description**: Automatically close any incoming pull request from an
    external contributor that does not reference an issue with a maintainer
    approval label (e.g., using `robzolkos/require-approved-issue`).
*   **Pros**: Provides complete maintainer insulation; ensures zero review time
    is spent on unapproved diffs.
*   **Cons**: Creates a hostile contributor experience; punishes serendipitous
    novel additions; adds disproportionate friction for small, obvious bug
    fixes.
*   **Reason for Rejection**: Directly contradicts EGM's core philosophy of
    good-faith collaboration and empowering external developers.

### Alternative B: Blanket Ban on Generative AI Contributions

*   **Description**: Adopt a total ban on all content generated by LLMs,
    following the policies of Gentoo Linux, NetBSD, and OpenJDK.
*   **Pros**: Theoretical elimination of synthetic code churn; preserves
    traditional clean-room legal provenance.
*   **Cons**: Completely unenforceable in practice; creates an incentive for
    contributors to conceal AI usage; antithetical to the EGM project, which
    exists specifically to pioneer LLM-native SDLC best practices.
*   **Reason for Rejection**: Unenforceable and fundamentally incompatible with
    the project's mission.

### Alternative C: Statistical AI Text Detectors

*   **Description**: Deploy automated GitHub bots running commercial LLM text
    classifiers (e.g., GPTZero) to detect and flag unreviewed synthetic code in
    issue bodies and PR descriptions.
*   **Pros**: Fully automated scoring without human configuration.
*   **Cons**: Severe false-positive rates (up to 61% on non-native English
    writing per Stanford research); trivial to circumvent by adding prompt
    instructions to sound colloquial.
*   **Reason for Rejection**: Unacceptable false-positive rate that
    systematically discriminates against non-native English contributors.

### Alternative D: Ephemeral Concept Briefs in Issues Instead of Checked-In Design Docs

*   **Description**: Require only a lightweight (`< 500` word) Concept Brief
    pasted into a GitHub Issue rather than a full EGM design document checked
    into `docs/designs/`.
*   **Pros**: Slightly lower initial writing overhead for external contributors.
*   **Cons**: Causes the repository's `docs/designs/` directory to drift out of
    sync with the codebase as new capabilities land without checked-in design
    specs; fails to exercise the full EGM workflow (`/egm-brainstorm` ->
    `/egm-draft` -> `/egm-review`).
*   **Reason for Rejection**: The EGM repository must exercise its own
    methodology and keep `docs/designs/` accurate. Rather than offering a
    half-measure compromise, we encourage contributors to reach out to
    maintainers first (`status: approved-for-design`) to confirm interest before
    authoring a full, concise EGM design document PR (`docs/designs/<name>.md`).

### Alternative E: Day-1 Concurrency Caps (1 PR per User)

*   **Description**: Implement a GitHub Action restricting external contributors
    to a maximum of one concurrent open pull request.
*   **Pros**: Limits burst automated contribution velocity from single accounts.
*   **Cons**: Easily evaded via burner accounts (Sybil attacks); adds code
    complexity to repository CI before actual spam patterns emerge.
*   **Reason for Rejection**: Premature optimization; deferred until empirical
    spam data warrants enforcement.

--------------------------------------------------------------------------------

## Non-Functional Requirements

### Security & Privacy

*   **Token Isolation**: GitHub Actions workflows run with the minimum
    `GITHUB_TOKEN` permissions required (`pull-requests: read`, `issues: write`,
    `contents: read`). Workflows do not have access to repository secrets or
    push rights to protected branches.
*   **Fork Execution Sandbox**: External code from forks is blocked from
    automatic execution by the "Require approval for all outside collaborators"
    setting, preventing crypto-mining and exfiltration attacks.

### Operational Failure Modes & Guardrails

*   **Script Injection Prevention**: To prevent command injection
    vulnerabilities in `pull_request_target`, workflows must never interpolate
    untrusted PR metadata (`github.event.pull_request.title`, `body`) directly
    into shell command strings. All processing must occur within
    `actions/github-script@v7` using in-memory JavaScript objects or isolated
    environment variables.
*   **API Quota Conservation**: The advisory bot paginates changed files up to a
    strict cap of 300 files (3 pages). If a PR reaches 300 files, the engine
    halts pagination and defaults safely to applying `advisory:
    design-doc-suggested` without exhausting the repository's 1,000 req/hr
    `GITHUB_TOKEN` quota.
*   **Automated Swarm Floods**: If an automated agent swarm submits
    high-frequency PR bursts, the advisory bot will post advisories but will not
    auto-close PRs. Maintainers will invoke native GitHub interaction limits
    (temporary 24-hour contributor cooldown) as an operational perimeter
    control.

### Performance & Latency

*   **Sub-10-Second Execution**: The scope advisory workflow runs solely on pull
    request metadata and paginated file lists via the GitHub REST API, avoiding
    deep checkout clones and completing in under 10 seconds.

### Operational Simplicity

*   **No Database Dependencies**: The entire triage pipeline relies on native
    GitHub primitives (labels, templates, REST API, actions), requiring zero
    external hosting, servers, or webhooks.

### Rollout & Rollback

*   **Rollout**: Land contributor policies (`AI_POLICY.md`, `AGENTS.md`,
    `CONTRIBUTING.md`), ingestion templates (`.github/PULL_REQUEST_TEMPLATE.md`,
    `.github/ISSUE_TEMPLATE/feature_proposal.md`), and the non-blocking scope
    advisory workflow (`.github/workflows/pr-scope-advisory.yml`) together,
    alongside creating the repository triage labels and enabling outside
    collaborator workflow approval in GitHub settings.
*   **Rollback**: The advisory workflow can be disabled instantaneously by
    removing `.github/workflows/pr-scope-advisory.yml` or disabling the workflow
    in GitHub repository settings.

--------------------------------------------------------------------------------

## Additional Resources

*   Open Home Foundation AI Policy:
    [Home Assistant AI Policy](https://github.com/home-assistant/core/blob/dev/AI_POLICY.md)
*   Homebrew Responsible AI Usage:
    [Homebrew AI Docs](https://docs.brew.sh/Responsible-AI-Usage)
*   EGM System Architecture:
    [architecture.md](architecture.md)

--------------------------------------------------------------------------------

## Future Improvements

*   **Automated Design Doc & Registry Validation**: Introduce a lightweight CI
    check for `Feature / Architectural Change` pull requests verifying that a
    checked-in design document under `docs/designs/` and an entry in
    `docs/designs/README.md` are present and include the required EGM
    structural sections.
*   **Maintainer-Triggered AI Review & Triage Agent**: Introduce an on-demand
    GitHub Actions workflow (triggered manually by maintainers via
    `workflow_dispatch` or a maintainer `/triage` comment command rather than
    automatically on untrusted `pull_request_target` events, preventing API key
    exhaustion and prompt injection from external forks) that runs an EGM review
    agent over incoming PR diffs to flag multi-PR scope-splitting, undocumented
    behavioral changes, and architectural drift against `docs/designs/`.

--------------------------------------------------------------------------------

## Verification Plan & Test Matrix

### Test Matrix

| Case ID | Track Checked | Non-Test Lines | Core Files | Test Lines | Expected Outcome |
| :------ | :------------ | :------------- | :--------- | :--------- | :--------------- |
| **TC-1** | `[x] Bug Fix` | 40 | 1 | 50 | **Passthrough**: Zero comments, no labels. |
| **TC-2** | `[x] Bug Fix` | 101 | 1 | 0 | **Advisory**: Post comment, apply `advisory: design-doc-suggested`. |
| **TC-3** | `[x] Bug Fix` | 100 | 1 | 20 | **Boundary Passthrough**: Threshold is `> 100`. |
| **TC-4** | `[x] Bug Fix` | 20 | 3 skills | 0 | **Advisory**: Triggers on `coreFilesCount >= 3`. |
| **TC-5** | `[x] Feature` | 500 | 5 | 100 | **Passthrough / Verified**: No bug-fix advisory. |
| **TC-6** | `[x] Bug Fix` | 30 code | 1 (`SKILL.md` + `TEST.md` + `test_scenarios.yaml`) | 250 test | **Passthrough**: Test regex excludes co-located `TEST.md` and `test_scenarios.yaml`. |
| **TC-7** | `[x] Bug Fix` | 150 -> 80 | 1 | 50 | **Bidirectional Cleanup**: Advisory label removed on sync. |
