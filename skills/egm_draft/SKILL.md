---
name: egm-draft
disable-model-invocation: true
description: >-
  Drafts a design document section-by-section using the discussion summary from
  egm-discuss. This is the second step in the Elephant & Goldfish (EGM) feature
  flow. Use when you are ready to write a design doc after aligning on
  requirements.
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

# Design Drafting (Specification Authoring)

This skill guides the user through turning a completed design discussion into a
formal design document, drafting it section by section, and gathering feedback
at each stage before saving it to disk.

## Execution Constraints (CRITICAL)

1.  You **MUST** read and apply the
    execution instructions in `resources/execution_instructions.md`.
2.  **Artifact-First Delivery (MANDATORY)**: You are **STRICTLY FORBIDDEN** from
    presenting large proposals, drafts, summaries, or plans directly in the chat
    pane. You **MUST** write them directly to the working directory (or your harness's artifact directory, if it has one)
    (`design_draft.md` or `./design_draft.md`)
    using your file-writing tool
    and tell the user in chat the file path and ask for review.
    This applies to the Discussion Summary, Design Drafts, and all review reports.

--------------------------------------------------------------------------------

## Execution Workflow

Follow these steps sequentially. Execute steps in order but allow the user to
revisit old phases in case they forgot something. Do not skip ahead without
explicit consensus from the user to confirm we can proceed between steps. Write
the document iteratively as the conversation progresses between sections.

--------------------------------------------------------------------------------

### Step 1: Ingest Discussion Summary

1.  **Check for Summary**: Look for `discussion_summary.md` in the current
    working directory (`./discussion_summary.md`) or the conversation artifact directory.
2.  **Fallback**: If the file does not exist in the root, check any local scratch
    directory or active conversation artifacts. If still missing, ask the user to
    provide the path to their summary or notes from their discussion phase
    (`egm-discuss`).
3.  **Verify State**: Parse the summary (Goals, Non-Goals, CUJs, Architecture
    Outline, Risks) by reading it and present a quick confirmation to the user to ensure we
    are starting with the correct context.
4.  **Consensus**: Get explicit approval to start drafting the document.

--------------------------------------------------------------------------------

### Step 2: Draft Overview & Problem Statement

1.  **Review Context**: Use the ingested discussion summary to frame the
    business problem and user pain points.
2.  **Draft Content**: Write "The Problem", "Overview", "Goals", and "Non-Goals"
    in clear, plain English Markdown following the design document template.
3.  **Focus**: Emphasize the *why* (the user need and business value) rather
    than the *how* (technical implementation).
4.  **Write Draft (MANDATORY)**: Save this initial draft to `design_draft.md`
    using your file-writing tool.
5.  **Notify & Verify (No Chat Dumps)**: You are **STRICTLY FORBIDDEN** from
    printing the draft in the chat. Output only a concise message notifying the
    user that the initial draft (Overview & Problem Statement) has been written
    to `design_draft.md` (give its path). Ask the user to review the file and provide feedback
    before proceeding to the technical plan.

--------------------------------------------------------------------------------

### Step 3: Draft Technical Plan

1.  **Synthesize Architecture**: Review the proposed high-level architecture
    from the discussion summary.
2.  **Draft Plan**: Describe the proposed changes in clear prose. Identify new
    components, modified files, and API changes.
3.  **Visual Aids**: Include text-based block diagrams (e.g., Graphviz or simple
    ASCII/Mermaid) to illustrate data flow.
4.  **Update Draft (MANDATORY)**: Update `design_draft.md` to append the
    "Technical Plan" section using your file-writing tool.
5.  **Notify & Verify (No Chat Dumps)**: You are **STRICTLY FORBIDDEN** from
    printing the technical plan in the chat. Notify the user that the Technical
    Plan has been added to `design_draft.md`. Ask the user to review the file
    and approve it before proceeding to alternatives.

--------------------------------------------------------------------------------

### Step 4: Draft Alternatives

1.  **Review Alternatives**: Recall the alternatives debated and rejected during
    the discussion phase.
2.  **Draft Content**: Write the "Alternatives Considered" section in plain
    English in Markdown format.
3.  **Detail Reasons**: For each alternative, explicitly state *why* it was
    rejected (e.g., higher latency, scaling limitations, team unfamiliarity).
4.  **Update Draft (MANDATORY)**: Update `design_draft.md` to append the
    "Alternatives Considered" section using your file-writing tool.
5.  **Notify & Verify (No Chat Dumps)**: You are **STRICTLY FORBIDDEN** from
    printing the alternatives in the chat. Notify the user that the Alternatives
    section has been added to `design_draft.md`. Ask the user to review the file
    and confirm before proceeding.

--------------------------------------------------------------------------------

### Step 5: Draft Implementation

Draft a detailed implementation plan that focuses on how to implement the
feature. This plan must be detailed. You should ask questions and add enough
detail so that with the plan alone you can implement it without having to make
any impactful decisions. Follow these guidelines:

1.  **Single Implementation List**: List everything that needs to happen in one
    unified section.
2.  **Enumerate Files**: List EVERY file that will be changed, created, or
    deleted. Include any documentation, schema, proto, or testing files that
    should be updated. You MUST include a reference to every file touched by the
    plan.
3.  **Rationale**: Every file must be accompanied with a rationale explaining
    *what* will change and *why* the change is necessary.
4.  **Format Links**: Provide full paths to files if known, or clear basenames.
5.  **NO CODE**: Do not generate actual implementation code in this design
    draft. Pseudocode, APIs, or schemas are allowed.
6.  **Update Draft (MANDATORY)**: Update `design_draft.md` to append this
    "Detailed Implementation" section using your file-writing tool.
7.  **Notify & Verify (No Chat Dumps)**: You are **STRICTLY FORBIDDEN** from
    printing the implementation plan in the chat. Notify the user that the
    Detailed Implementation Plan has been added to `design_draft.md`. Ask the
    user to review the file and provide feedback.

--------------------------------------------------------------------------------

### Step 6: Write Design Document Finalization

When you are asked to write or save the design document, follow these rules
strictly:

1.  Verify if the user has specified the target directory. If not, explicitly
    ask for it.
2.  **Update Sitemap**: If `<DESIGN_DIR>/SITEMAP.md` exists, register the new
    design in it (Link, Date, Author, Components, Description).
3.  **Self-Evaluate against Zoom Out Standard**: Before saving the file,
    self-evaluate the compiled design document (contents of `design_draft.md`)
    against the EGM Zoom Out Standard
    (`resources/document_standards/zoom-out-standard.md`).
    Verify that the design remains focused on the root problem, does not
    introduce premature optimizations or speculative logic (YAGNI), and
    maximizes reuse. If any issues are found, present them to the user, explain
    the proposed improvements, and ask for confirmation before refining the
    draft.
4.  **Write doc**: Once finalized, write the contents of `design_draft.md` to
    the designated destination file at `<DESIGN_PATH>` (e.g., `./<FEATURE>.md`) using your file-writing tool.
    Follow the [template](references/design_doc.md) for final structure if any
    adjustments are needed.
5.  **Clean Formatting**: Ensure clean standard Markdown formatting, valid table
    syntax, and proper code block fences.
6.  **Handoff**: Provide a clickable link to the finalized design and recommend
    that the user review the document with:

    ```markdown
    `egm-review` <DESIGN_PATH>
    ```
