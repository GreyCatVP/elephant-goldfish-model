---
name: egm-discuss
disable-model-invocation: true
description: >-
  An interactive design discussion to align on the problem, requirements, and
  high-level architecture before drafting a design document. This is the first
  step in the Elephant & Goldfish (EGM) feature flow. Use to discuss a feature
  request in detail.
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

# Design Discussion (Problem Alignment)

This skill guides the user through the initial phases of the design process:
loading context, clarifying the feature, and grilling the requirements to align
on the problem and high-level architecture.

## Execution Constraints (CRITICAL)

1.  You **MUST** read and apply the
    [execution instructions](references/instructions.md).
2.  **Artifact-First Delivery (MANDATORY)**: You are **STRICTLY FORBIDDEN** from
    presenting large proposals, drafts, summaries, or plans directly in the chat
    pane. You **MUST** write them directly to the conversation artifact
    directory (`<appDataDir>/brain/<conversation-id>/discussion_summary.md` or `./discussion_summary.md`)
    using `write_to_file` with `ArtifactMetadata` (`UserFacing: true`, `RequestFeedback: true`)
    and notify the user that the artifact is ready for review in their side panel.
    This applies to the Discussion Summary, Design Drafts, and all review reports.

--------------------------------------------------------------------------------

## Execution Workflow

Follow these steps sequentially, but allow the user to revisit phases in case
they forgot something. Only move on to subsequent sections with explicit
consensus from the user. Confirm with the user before proceeding between steps.

--------------------------------------------------------------------------------

### Step 1: Load Context

1.  **Check for Context**: Verify if the user has provided documentation, code
    paths, or references to understand the system. If none are provided,
    explicitly ask the user for them.
2.  **Analyze Context**: Read and synthesize the provided materials using `view_file`,
    focusing on the system's purpose, main components, and architectural boundaries.
3.  **Summarize & Verify**: Provide a concise, high-level summary of the system
    to the user. Explicitly ask the user to confirm or correct your
    understanding before proceeding to feature discussion. Tell the user to be
    nitpicky to prevent gaps in your understanding.

--------------------------------------------------------------------------------

### Step 2: Start Feature Discussion

1.  **Initiate discussion**: Ask the user to provide the feature they want to
    build if they haven't already done so.
2.  **Act as a Partner**: Ask clarifying questions to understand the
    requirements and intended behavior. Use `ask_question` to present structured
    options when clarifying user preferences or choosing between alternatives.
    If there is a preferred or recommended alternative based on best practices,
    prefix it with `(Recommended)` and list it first.
3.  **Challenge Assumptions**: Identify potential edge cases, single points of
    failure, or missing details. Think critically. Do not simply agree with the
    user.
4.  **Reach consensus**: Wait for the user's response before offering
    architectural proposals.

--------------------------------------------------------------------------------

### Step 3: Requirements Grilling & High-Level Architecture

1.  **Adopt a Skeptical Persona**: Assume the current design proposal has hidden
    flaws, scaling limits, or operational complexities.
2.  **Ask Questions**: Proactively infer, confirm, or query these questions to
    establish a solid baseline:
    1.  *Objective*: What are you trying to do? (No jargon!)
    2.  *Limits*: How is it done today, and what are the limits?
    3.  *New Approach*: What is new in your approach and why will it succeed?
    4.  *Impact*: Who cares? What difference will it make?
    5.  *Risks*: What are the risks?
    6.  *Cost*: How much will it cost (dev time, compute, storage, LLM tokens,
        etc.)?
    7.  *Verification*: What are the verification plans? What tests do we need
        to run? How will we measure success?
    8.  *Infer & Confirm & Ask One-by-One*: Proactively infer answers from
        context, present them, and ask the user to refine. For any unanswered
        questions, you MUST ask them one-by-one using `ask_question`, providing
        your inferred answers as selectable options. Prefix your best inferred answer
        option with `(Recommended)` and list it first. You are strictly forbidden
        from asking multiple grilling questions in a single turn. Wait for the user's
        response to each question before moving to the next.
3.  **Challenge**: Do not simply agree with the user's statements. Explicitly
    point out potential issues or alternatives for every proposal made.
    Challenge the user throughout the process.
4.  **Identify Weaknesses**: Analyze the design for single points of failure
    (SPOFs), high latency paths, or excessive operational burden.

--------------------------------------------------------------------------------

### Step 4: Align on Discussion Summary

1.  **Synthesize Discussion**: Review the requirements, goals, limits, risks,
    and high-level architecture aligned in Step 3. Make sure you have the
    answers you need to these areas:

    -   [ ] The *Objective*
    -   [ ] The *Limits*
    -   [ ] The *New Approach*
    -   [ ] The *Impact*
    -   [ ] The *Risks*
    -   [ ] The *Cost*
    -   [ ] The *Verification*

2.  **Save Draft Summary**: Create a structured Markdown summary of
    the discussion (Goals, Non-Goals, CUJs, Architecture Outline, Risks, Cost,
    Success Exams).

    *   **Self-Evaluate against Zoom Out Standard**: Before saving, perform a
        self-evaluation of the proposed architecture against the standard in
        `references/zoom-out-standard.md`.
        Ensure the design focuses on the root problem, avoids premature
        optimization and speculative features (YAGNI), and leverages existing
        codebase utilities. If you detect any potential violations, note them as
        warnings or open design risks in your summary.
    *   **Write Document (MANDATORY)**: You **MUST** immediately write this
        draft summary to `discussion_summary.md` (e.g., `<appDataDir>/brain/<conversation-id>/discussion_summary.md`
        or `./discussion_summary.md`) using `write_to_file` with `ArtifactMetadata`
        (`UserFacing: true`, `RequestFeedback: true`).
    *   **Notify User (No Chat Dumps)**: You are **STRICTLY FORBIDDEN** from
        printing the full summary in the chat. Output only a concise message
        notifying the user that the draft discussion summary is ready for their
        review in the side panel.

3.  **Review Gate (CRITICAL)**: Ask the user to review `discussion_summary.md`
    for clarity and confirm its accuracy. Encourage them to provide comments,
    request changes, or approve it.

4.  **Achieve Consensus**: Wait for the user's explicit approval of the summary
    before proceeding. If they request modifications, update the file and ask them
    to review again. Do NOT proceed to the handoff until the user explicitly approves.

--------------------------------------------------------------------------------

### Step 5: Finalize & Handoff

1.  **Handoff**: Once the user explicitly approves the summary, output the final
    handoff message: "The discussion summary has been finalized in
    `discussion_summary.md`. I recommend we draft a design document. We
    can continue to iterate on the plan or start the drafting process
    with the `egm-draft` skill."
