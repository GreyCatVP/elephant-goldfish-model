---
name: egm-review
disable-model-invocation: true
description: >-
  Orchestrates the EGM Goldfish Review Protocol. Used as part of the EGM
  process to perform design document reviews. Executes five review phases:
  Initial Zoom Out Review, Comprehension Review, Design Critique, Intermediate
  Zoom Out Review, and Implementation Readiness.
---

<!--
Copyright 2026 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# EGM Review: Goldfish Review Orchestrator

## Overview

This skill acts as the main entry point for EGM Design Doc Reviews. It helps the
user target the correct sections of their document and runs the Initial Zoom Out
Review (Step 5), Comprehension Test (Step 6), Critic Review (Step 7),
Intermediate Zoom Out Review (Step 8), and Implementation Readiness Test
(Step 9) either individually or as a sequential Full Flow.

## Delegation

A Goldfish runs in a fresh context with no conversation history. Spawn each
subagent with your harness's subagent tool (Claude Code: Task tool; Codex:
`spawn_agent`; Cursor and Gemini CLI: subagents; Antigravity:
`invoke_subagent`). Each subagent is defined in `personas/<file>.md`, and its
frontmatter `name` (for example `egm-zoom-out`) is the subagent type to request
where your harness registers named subagents. Otherwise spawn a general-purpose
subagent and tell it to read that persona file first. Pass the prompt verbatim
and wait for the report. If your harness cannot nest subagents,
use direct dispatch instead of the synthesizer. See `docs/harnesses.md`.
If your harness has no subagent tool, stop and tell the user: a review in the same context is not a Goldfish review.

## Execution Constraints (CRITICAL)

1.  **Artifact-First Delivery (MANDATORY)**: You are **STRICTLY FORBIDDEN** from
    presenting large proposals, drafts, summaries, or plans directly in the chat
    pane. You **MUST** write them to the working directory (or your harness's artifact directory, if it has one) using
    your file-writing tool and then tell the user in chat
    the file path and ask for review. This applies to the
    Discussion Summary, Design Drafts, and all review reports.

## Inputs

*   **`TargetFile`**: Absolute path to the design document.
*   **`GoldfishContext`** (Optional): Reading list to establish the system
    baseline. If omitted, the system defaults to no additional context (but
    always automatically reads files linked or referenced in the design doc).
*   **`Step` (Optional)**: Specific step to run (`5`, `6`, `7`, `8`, or `9`). If
    omitted, the user is prompted.

## Workflow

### Step 1: Intake & Setup

1.  Verify if `TargetFile` is provided. If missing:
    *   Explain to the user that the target design document path is required to
        analyze its structure and discover the semantic split.
    *   Ask the user to provide the absolute path.
    *   **CRITICAL**: Do NOT use structured question tools. Ask the question as a
        regular text message and end your turn.
2.  Once `TargetFile` is provided, verify if `GoldfishContext` is provided. If
    missing:
    *   Explain to the user that the goldfish context (reading list of files) is
        optional, but can be provided to establish a baseline of knowledge for
        the reviewers (e.g., related design specs).
    *   Clarify that the goldfish reviewers will **always automatically read**
        any files explicitly mentioned or linked in the target design document
        itself, so there is no need to manually list them.
    *   Ask if the user wants to provide any *additional* context files, or if
        they prefer to proceed with no additional context.
    *   **CRITICAL**: Do NOT use structured question tools. Ask the question as a
        regular text message and end your turn.

### Step 2: Semantic Split Discovery

1.  Read the `TargetFile` to identify the boundary between the high-level
    Feature Design and the Detailed Design:
    *   Scan the document for standard headers like `## Detailed Implementation
        Plan` (from the EGM template) or other common headers like "Detailed
        Design", "Detailed Implementation".
2.  If a boundary header is found:
    *   Define `FeatureRange` as lines 1 to (Split Line - 1).
    *   Define `DetailedRange` as lines Split Line to End of File.
    *   **Heuristic for skipping confirmation**: If the header is exactly `##
        Detailed Implementation Plan` (case-insensitive) and appears to be the
        primary split point, you may **skip confirmation** and proceed directly
        to Step 3.
    *   **Otherwise (if header is non-standard or ambiguity exists)**:
        *   Output a visible chat message to ask the user to confirm the split.
            **CRITICAL**: You **MUST** immediately yield active execution by
            calling **zero tools** in this turn payload to wait for their
            response.
        *   **CRITICAL**: In the chat message, you **MUST** include a snippet
            showing 2-3 lines before and after the identified split line so the
            user has context.
        *   Present these options in text:
            *   **(Recommended) Confirm split** (proceeds with these ranges).
            *   **Reject split and specify boundary manually** (allows custom
                write-in to specify header or line number).
3.  If no boundary header was found, or if the user rejected the found boundary:
    *   Scan the document to extract all Level 2 (`##`) and Level 3 (`###`)
        headers.
    *   Output a visible chat message to ask the user to select the boundary
        header from the extracted list. **CRITICAL**: You **MUST** immediately
        yield active execution by calling **zero tools** in this turn payload.
    *   Present these options in text:
        *   [List of extracted headers as individual options]
        *   **Specify boundary manually** (allows custom write-in to specify
            custom header or line number).
        *   **Cancel review**.
    *   Recalculate the ranges based on the user's selection (or abort if
        cancelled).

### Step 3: Flow Selection & Execution

1.  If `Step` is specified, invoke the corresponding subflow:
    *   If `5`: Run **Subflow: Zoom Out Review**.
    *   If `6`: Run **Subflow: Comprehension Test** passing `FeatureRange` and
        `DetailedRange`.
    *   If `7`: Run **Subflow: Critic Review** passing `FeatureRange`.
    *   If `8`: Run **Subflow: Zoom Out Review** (Intermediate Post-Critic Pruning).
    *   If `9`: Run **Subflow: Implementation Readiness Test** passing
        `DetailedRange`.
2.  If `Step` is omitted, output a visible chat message asking the user which
    step they want to run. **CRITICAL**: You **MUST** immediately yield active
    execution by calling **zero tools** in this turn payload to wait for their
    response. Present these options in text:
    *   (Recommended) Full EGM Flow (Runs all review stages sequentially from
        Step 5 through Step 9, including Step 8 Intermediate Zoom Out Review)
    *   Step 5: Initial Zoom Out Review ("Does the design focus on the root
        problem and avoid YAGNI?")
    *   Step 6: Comprehension Test ("Is the doc self-contained?")
    *   Step 7: Critic Review ("Find edge cases and assumptions")
    *   Step 8: Intermediate Zoom Out Review ("Does the revised design avoid
        speculative complexity and YAGNI?")
    *   Step 9: Implementation Readiness Test ("Is it ready to implement?")
3.  Execute the chosen option:
    *   For individual step selections (Step 5, 6, 7, 8, or 9), invoke the
        respective subflow and exit.
    *   For the Full Flow selection:
        *   Run **Subflow: Zoom Out Review** (Step 5: Initial Zoom Out Review).
        *   Wait for completion. If the user passes the manual checkpoint,
            proceed.
        *   Run **Subflow: Comprehension Test** passing `FeatureRange` and
            `DetailedRange` (Step 6: Comprehension Test).
        *   Wait for completion. If the user passes the manual checkpoint,
            proceed.
        *   Run **Subflow: Critic Review** passing `FeatureRange` (Step 7: Critic
            Review).
        *   Wait for the loop to complete and findings to be resolved.
        *   Run **Subflow: Zoom Out Review** as Step 8 (Intermediate Zoom Out
            Review) to double check that the design remains focused and removes
            any YAGNI items before implementation planning. Focus specifically
            on additions or mitigations introduced during Comprehension and Critic
            Review.
        *   Wait for completion. If the user passes the manual checkpoint,
            proceed.
        *   Run **Subflow: Implementation Readiness Test** passing `DetailedRange`
            (Step 9: Implementation Readiness Test).
        *   Wait for the loop to complete.

--------------------------------------------------------------------------------

## Subflows

### Subflow: Zoom Out Review

1.  **Spawn Zoom Out Subagent**: Spawn the specialized `egm-zoom-out` auditor:
    *   Subagent: `egm-zoom-out` (`personas/zoom_out.md`)
    *   `Prompt`: >- Audit the file `[TargetFile]` at line range `full file`.
        Apply standard `resources/document_standards/zoom-out-standard.md`.
        Context documents: `[GoldfishContext]`.
2.  **Write Report Artifact**: Save findings to `zoom_out_report.md` (or
    `intermediate_zoom_out_report.md` for Step 8) in the working directory
    using your file-writing tool.
3.  **Notify User (No Chat Dumps)**: Notify the user in chat that the Zoom Out
    findings have been written to the report file (give its path),
    highlight 2-3 key risks, and prompt for review.
4.  **Manual Checkpoint Gate**: Ask the user in chat whether to proceed to the next
    stage or pause to address Zoom Out findings.

### Subflow: Comprehension Test

1.  **Spawn Comprehension Subagent**: Spawn the `egm-comprehension` reviewer:
    *   Subagent: `egm-comprehension` (`personas/comprehension.md`)
    *   `Prompt`: >- Audit the file `[TargetFile]` at line range `[FeatureRange]`
        and `[DetailedRange]`. Apply standard
        `resources/document_standards/re-implementation-standard.md`.
        Context documents: `[GoldfishContext]`.
2.  **Write Report Artifact**: Save findings to `comprehension_report.md` in
    the working directory using your file-writing tool.
3.  **Notify User (No Chat Dumps)**: Notify the user in chat that the Comprehension
    findings have been written to `comprehension_report.md` (give its path).
4.  **Manual Checkpoint Gate**: Prompt the user in chat:
    *   *Yes, I will update the doc/context* (pause to let user edit, then offer re-run).
    *   *No, these gaps are not significant* (proceed to next step).

### Subflow: Critic Review

1.  **Invoke Antagonistic Review Loop**: Execute the local **`goldfish-review-loop`**
    workflow directly in this conversation.
2.  Pass parameters:
    *   `TargetFile`: Same.
    *   `SemanticTarget`: `FeatureRange` (passed as lines).
    *   `Reviewers`: `[egm-design, egm-structural, egm-style]`
    *   `Standards`: `{"egm-design": "feature-spec-standard", "egm-structural": "feature-spec-standard"}`
    *   `GoldfishContext`: Same.
3.  Allow `goldfish-review-loop` to manage the iterative audit, findings resolution
    via `goldfish-review-resolve`, and repair application.

### Subflow: Implementation Readiness Test

1.  **Invoke Antagonistic Review Loop**: Execute the local **`goldfish-review-loop`**
    workflow directly in this conversation.
2.  Pass parameters:
    *   `TargetFile`: Same.
    *   `SemanticTarget`: `DetailedRange` (passed as lines).
    *   `Reviewers`: `[egm-implementation-readiness, egm-codebase-details, egm-style]`
    *   `Standards`: `{"egm-implementation-readiness": "implementation-readiness-standard", "egm-codebase-details": "implementation-readiness-standard"}`
    *   `GoldfishContext`: Same.
3.  Allow `goldfish-review-loop` to manage the iterative audit, findings resolution
    via `goldfish-review-resolve`, and repair application.
