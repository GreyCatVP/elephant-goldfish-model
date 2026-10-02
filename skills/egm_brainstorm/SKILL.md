---
name: egm-brainstorm
disable-model-invocation: true
description: >-
  Interactive multi-lens ideation and brainstorming skill for the Elephant &
  Goldfish Model (EGM). Helps turn half-baked concepts into structured hypotheses
  via clarifying questions, parallel Goldfish shootdown swarms, and iterative
  refinement in concepts_brief.md before egm-discuss or egm-draft.
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

# EGM Brainstorm: Interactive Multi-Lens Ideation & Refinement

## Overview

This skill acts as the upstream conversational ideation and brainstorming engine
for the Elephant & Goldfish Model (EGM). It turns "half-baked" or raw feature
concepts into fully-formed hypotheses by combining **interactive clarifying
questions** with an automated **Goldfish multi-lens shootdown swarm**. The
outcome is an iteratively refined `concepts_brief.md` artifact that leads
seamlessly into `/egm-discuss` or `/egm-draft`.

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
    presenting large proposals, drafts, brainstorm summaries, or briefs directly
    in the chat pane. You **MUST** write/update them directly to a file (e.g.,
    `./concepts_brief.md` in the project root or artifact directory) using your
    environment's file-writing tool and notify the user in
    the chat with a clean link to the file.
2.  **Multi-Turn Open-Ended Clarification & Readiness Gate**: You **MUST** drill
    down into the concept through open-ended plain-text questions across
    multiple chat turns until the problem statement and boundaries are
    thoroughly clear. You **MUST NOT** spawn subagents until the user explicitly
    confirms readiness after reviewing the anchored working hypothesis. You are
    **STRICTLY FORBIDDEN** from using structured question tools or supplying pre-canned multiple-choice candidate answers.
3.  **Parallel Goldfish Swarm**: You **MUST** evaluate the feature
    concept across all 6 specialized Goldfish perspective lenses simultaneously
    via subagents to prevent sequential bias and maximize critique breadth.

--------------------------------------------------------------------------------

## The 6 Goldfish Brainstorming Lenses

| Lens / Persona       | Core Objective           | Key Questions Challenged   |
| :------------------- | :----------------------- | :------------------------- |
| **1. Contrarian /    | Code & complexity        | *Why does this feature     |
: YAGNI**              : minimization             : need to exist? Can an      :
:                      :                          : existing library,          :
:                      :                          : open-source dependency,    :
:                      :                          : API, or service solve 90%  :
:                      :                          : of this problem without    :
:                      :                          : writing new code?*         :
| **2. Cost, Quota &   | Infrastructure & budget  | *What is the peak QPS,     |
: Token Economics**    : scaling                  : memory footprint,          :
:                      :                          : database query load, or    :
:                      :                          : LLM token budget? Will     :
:                      :                          : this hit quota ceilings at :
:                      :                          : scale?*                    :
| **3. UX & Developer  | Usability & cognitive    | *Is the API/CLI intuitive? |
: Ergonomics**         : overhead                 : Does it match ecosystem    :
:                      :                          : conventions? Are error     :
:                      :                          : messages actionable, or    :
:                      :                          : does it add developer      :
:                      :                          : friction?*                 :
| **4. Migration &     | Rollout safety & version | *How do existing           |
: Backward             : skew                     : clients/data migrate? Does :
: Compatibility**      :                          : this break serialized      :
:                      :                          : schemas, protos, or        :
:                      :                          : persistent storage? How is :
:                      :                          : rollback handled           :
:                      :                          : mid-migration?*            :
| **5. Observability & | Telemetry & operational  | *Are key operations        |
: SRE Debuggability**  : visibility               : traceable via distributed  :
:                      :                          : tracing? Are telemetry     :
:                      :                          : metrics actionable? How    :
:                      :                          : will oncall engineers      :
:                      :                          : triage a production        :
:                      :                          : incident at 3 AM?*         :
| **6. Long-Term Tech  | Future maintainability   | *Does this introduce       |
: Debt & Maintenance** :                          : tightly coupled            :
:                      :                          : dependencies or brittle    :
:                      :                          : state machines that will   :
:                      :                          : be painful to maintain in  :
:                      :                          : 2 years?*                  :

--------------------------------------------------------------------------------

## Execution Workflow

### Step 1: Deep Clarification & Problem Statement Drilling

1.  **Check for Concept Foundation**: Verify if the user has provided an initial
    feature idea or concept prompt. If missing, prompt the user to describe what
    they want to brainstorm.
2.  **Iterative Problem Drilling (Multi-Turn Chat)**: Do **NOT** rush into
    launching subagents after a single response. Continue asking targeted,
    open-ended clarifying questions across multiple turns as needed until the
    problem statement, constraints, and target behavior are thoroughly defined.
    Do **NOT** use structured question tools and do
    **NOT** provide candidate multiple-choice options—ask open-ended questions
    directly in chat:
    *   *What specific problem, bottleneck, or pain point does this solve?*
    *   *Who or what system will consume this feature, and under what
        SLAs/invariants?*
    *   *What are the hard non-negotiable constraints (e.g., zero false
        positives, offline operation, specific platform/dialect)?*
    *   *What are the edge cases or out-of-scope boundaries?*
3.  **Readiness Checkpoint Gate (MANDATORY)**: Once a clear foundation is
    established, summarize the anchored hypothesis in 2-3 sentences and
    explicitly ask the user for confirmation before spawning subagents: *"We
    have anchored the working hypothesis as: [Hypothesis]. Are we ready to
    launch the Goldfish shootdown swarm, or would you like to clarify additional
    details first?"*
4.  **Proceed to Step 2 ONLY** after the user explicitly confirms readiness in
    chat.

--------------------------------------------------------------------------------

### Step 2: Goldfish Swarm Shootdown & Synthesis

1.  **Delegate to Subagent Swarm**:
    Spawn the intermediate
    **`egm-synthesizer`** (or parallel Goldfish subagents across the 6 specialized lenses):
    *   Subagent: `egm-synthesizer` (`personas/synthesizer.md`) (or a general-purpose subagent)
    *   `Prompt`: >- Conduct multi-lens ideation brainstorm for feature concept:
        `[AnchoredFeatureHypothesis]`. Mode: `BRAINSTORM`. Reviewers:
        `[egm-design, egm-codebase-details, egm-zoom-out, egm-comprehension,
        egm-implementation-readiness, egm-structural]`.
2.  **Multi-Lens Risk Matrix & Deduplication**: Collect the raw findings across all
    6 Goldfish lenses, deduplicate overlapping points, and format them into a cohesive
    shootdown analysis.
3.  **Write/Update Artifact**: Format and write the synthesized brief to
    the working directory (or your harness's artifact directory, if it has one) (`concepts_brief.md`)
    using your file-writing tool.

The `concepts_brief.md` artifact follows this structure:

```markdown
# Concepts Brief / PRD: [Feature Name]

* **Status:** Ideation In-Progress / Ready for Discussion
* **Upstream Lens Review:** 6 Goldfish Lenses Applied

## 1. Executive Summary & Problem Framing
[High-level summary of the feature, target user, and core value proposition.]

## 2. Multi-Lens Analysis & Risk Matrix
* **Contrarian / YAGNI Assessment:** [Findings on code minimization and existing alternatives]
* **Cost, Quota & Token Economics:** [Compute, storage, QPS, and LLM token budgets]
* **UX & Developer Ergonomics:** [API design, CLI usability, and cognitive overhead]
* **Migration & Compatibility Strategy:** [Data migration, rollout phases, rollback safety]
* **Observability & Operational SRE:** [Distributed tracing, telemetry metrics, oncall debuggability]
* **Long-Term Maintainability & Tech Debt:** [Coupling risks and future maintenance surface]

## 3. Scope Boundaries (Goals vs. Non-Goals)
* **In-Scope Goals:** [Explicitly defined scope items]
* **Out-of-Scope Non-Goals:** [Features intentionally excluded]

## 4. Key Architectural Decisions & Staging for Next Stage
[Key decisions resolved during ideation to be carried forward into `/egm-discuss` or `/egm-draft`.]
```

--------------------------------------------------------------------------------

### Step 3: Interactive Iteration & Refinement Loop

1.  **Notify & Highlight (No Chat Dumps)**: Notify the user in chat that
    `concepts_brief.md` has been updated in the working directory (give its path).
    Highlight 2-3 key objections or open risks raised by the Goldfish swarm.
2.  **Iterate**: Ask the user how they wish to address the Goldfish objections
    (e.g., pivoting the approach, narrowing scope, or adding constraints).
3.  **Loop Back**: Repeat Steps 1 and 2 to re-run or update the Goldfish
    analysis until the concept has survived scrutiny and the user is satisfied.

--------------------------------------------------------------------------------

### Step 4: Finalize & Handoff

1.  Ask the user to review the final `concepts_brief.md` artifact and confirm
    their alignment.
2.  Once approved, present the seamless handoff choices based on readiness:
    *   **`/egm-discuss`**: Recommend this if requirements grilling, limit
        exploration, and step-by-step consensus building are still needed.
    *   **`/egm-draft`**: Present this if the concept is concrete and ready for
        technical specification drafting.

---
name: egm-brainstorm
disable-model-invocation: true
description: >-
  Interactive multi-lens ideation and brainstorming skill for the Elephant &
  Goldfish Model (EGM). Helps turn half-baked concepts into structured hypotheses
  via clarifying questions, parallel Goldfish shootdown swarms, and iterative
  refinement in concepts_brief.md before egm-discuss or egm-draft.
---

# EGM Brainstorm: Interactive Multi-Lens Ideation & Refinement

## Overview

This skill acts as the upstream conversational ideation and brainstorming engine
for the Elephant & Goldfish Model (EGM). It turns "half-baked" or raw feature
concepts into fully-formed hypotheses by combining **interactive clarifying
questions** with an automated **Goldfish multi-lens shootdown swarm**. The
outcome is an iteratively refined `concepts_brief.md` artifact that leads
seamlessly into `/egm-discuss` or `/egm-draft`.

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
    presenting large proposals, drafts, brainstorm summaries, or briefs directly
    in the chat pane. You **MUST** write/update them directly to a file (e.g.,
    `./concepts_brief.md` in the project root or artifact directory) using your
    environment's file-writing tool and notify the user in
    the chat with a clean link to the file.
2.  **Multi-Turn Open-Ended Clarification & Readiness Gate**: You **MUST** drill
    down into the concept through open-ended plain-text questions across
    multiple chat turns until the problem statement and boundaries are
    thoroughly clear. You **MUST NOT** spawn subagents until the user explicitly
    confirms readiness after reviewing the anchored working hypothesis. You are
    **STRICTLY FORBIDDEN** from using structured question tools or supplying pre-canned multiple-choice candidate answers.
3.  **Parallel Goldfish Swarm**: You **MUST** evaluate the feature
    concept across all 6 specialized Goldfish perspective lenses simultaneously
    via subagents to prevent sequential bias and maximize critique breadth.

--------------------------------------------------------------------------------

## The 6 Goldfish Brainstorming Lenses

| Lens / Persona       | Core Objective           | Key Questions Challenged   |
| :------------------- | :----------------------- | :------------------------- |
| **1. Contrarian /    | Code & complexity        | *Why does this feature     |
: YAGNI**              : minimization             : need to exist? Can an      :
:                      :                          : existing library,          :
:                      :                          : open-source dependency,    :
:                      :                          : API, or service solve 90%  :
:                      :                          : of this problem without    :
:                      :                          : writing new code?*         :
| **2. Cost, Quota &   | Infrastructure & budget  | *What is the peak QPS,     |
: Token Economics**    : scaling                  : memory footprint,          :
:                      :                          : database query load, or    :
:                      :                          : LLM token budget? Will     :
:                      :                          : this hit quota ceilings at :
:                      :                          : scale?*                    :
| **3. UX & Developer  | Usability & cognitive    | *Is the API/CLI intuitive? |
: Ergonomics**         : overhead                 : Does it match ecosystem    :
:                      :                          : conventions? Are error     :
:                      :                          : messages actionable, or    :
:                      :                          : does it add developer      :
:                      :                          : friction?*                 :
| **4. Migration &     | Rollout safety & version | *How do existing           |
: Backward             : skew                     : clients/data migrate? Does :
: Compatibility**      :                          : this break serialized      :
:                      :                          : schemas, protos, or        :
:                      :                          : persistent storage? How is :
:                      :                          : rollback handled           :
:                      :                          : mid-migration?*            :
| **5. Observability & | Telemetry & operational  | *Are key operations        |
: SRE Debuggability**  : visibility               : traceable via distributed  :
:                      :                          : tracing? Are telemetry     :
:                      :                          : metrics actionable? How    :
:                      :                          : will oncall engineers      :
:                      :                          : triage a production        :
:                      :                          : incident at 3 AM?*         :
| **6. Long-Term Tech  | Future maintainability   | *Does this introduce       |
: Debt & Maintenance** :                          : tightly coupled            :
:                      :                          : dependencies or brittle    :
:                      :                          : state machines that will   :
:                      :                          : be painful to maintain in  :
:                      :                          : 2 years?*                  :

--------------------------------------------------------------------------------

## Execution Workflow

### Step 1: Deep Clarification & Problem Statement Drilling

1.  **Check for Concept Foundation**: Verify if the user has provided an initial
    feature idea or concept prompt. If missing, prompt the user to describe what
    they want to brainstorm.
2.  **Iterative Problem Drilling (Multi-Turn Chat)**: Do **NOT** rush into
    launching subagents after a single response. Continue asking targeted,
    open-ended clarifying questions across multiple turns as needed until the
    problem statement, constraints, and target behavior are thoroughly defined.
    Do **NOT** use structured question tools and do
    **NOT** provide candidate multiple-choice options—ask open-ended questions
    directly in chat:
    *   *What specific problem, bottleneck, or pain point does this solve?*
    *   *Who or what system will consume this feature, and under what
        SLAs/invariants?*
    *   *What are the hard non-negotiable constraints (e.g., zero false
        positives, offline operation, specific platform/dialect)?*
    *   *What are the edge cases or out-of-scope boundaries?*
3.  **Readiness Checkpoint Gate (MANDATORY)**: Once a clear foundation is
    established, summarize the anchored hypothesis in 2-3 sentences and
    explicitly ask the user for confirmation before spawning subagents: *"We
    have anchored the working hypothesis as: [Hypothesis]. Are we ready to
    launch the Goldfish shootdown swarm, or would you like to clarify additional
    details first?"*
4.  **Proceed to Step 2 ONLY** after the user explicitly confirms readiness in
    chat.

--------------------------------------------------------------------------------

### Step 2: Goldfish Swarm Shootdown & Synthesis

1.  **Delegate to Subagent Swarm**:
    Spawn the intermediate
    **`egm-synthesizer`** (or parallel Goldfish subagents across the 6 specialized lenses):
    *   Subagent: `egm-synthesizer` (`personas/synthesizer.md`) (or a general-purpose subagent)
    *   `Prompt`: >- Conduct multi-lens ideation brainstorm for feature concept:
        `[AnchoredFeatureHypothesis]`. Mode: `BRAINSTORM`. Reviewers:
        `[egm-design, egm-codebase-details, egm-zoom-out, egm-comprehension,
        egm-implementation-readiness, egm-structural]`.
2.  **Multi-Lens Risk Matrix & Deduplication**: Collect the raw findings across all
    6 Goldfish lenses, deduplicate overlapping points, and format them into a cohesive
    shootdown analysis.
3.  **Write/Update Artifact**: Format and write the synthesized brief to
    the working directory (or your harness's artifact directory, if it has one) (`concepts_brief.md`)
    using your file-writing tool.

The `concepts_brief.md` artifact follows this structure:

```markdown
# Concepts Brief / PRD: [Feature Name]

* **Status:** Ideation In-Progress / Ready for Discussion
* **Upstream Lens Review:** 6 Goldfish Lenses Applied

## 1. Executive Summary & Problem Framing
[High-level summary of the feature, target user, and core value proposition.]

## 2. Multi-Lens Analysis & Risk Matrix
* **Contrarian / YAGNI Assessment:** [Findings on code minimization and existing alternatives]
* **Cost, Quota & Token Economics:** [Compute, storage, QPS, and LLM token budgets]
* **UX & Developer Ergonomics:** [API design, CLI usability, and cognitive overhead]
* **Migration & Compatibility Strategy:** [Data migration, rollout phases, rollback safety]
* **Observability & Operational SRE:** [Distributed tracing, telemetry metrics, oncall debuggability]
* **Long-Term Maintainability & Tech Debt:** [Coupling risks and future maintenance surface]

## 3. Scope Boundaries (Goals vs. Non-Goals)
* **In-Scope Goals:** [Explicitly defined scope items]
* **Out-of-Scope Non-Goals:** [Features intentionally excluded]

## 4. Key Architectural Decisions & Staging for Next Stage
[Key decisions resolved during ideation to be carried forward into `/egm-discuss` or `/egm-draft`.]
```

--------------------------------------------------------------------------------

### Step 3: Interactive Iteration & Refinement Loop

1.  **Notify & Highlight (No Chat Dumps)**: Notify the user in chat that
    `concepts_brief.md` has been updated in the working directory (give its path).
    Highlight 2-3 key objections or open risks raised by the Goldfish swarm.
2.  **Iterate**: Ask the user how they wish to address the Goldfish objections
    (e.g., pivoting the approach, narrowing scope, or adding constraints).
3.  **Loop Back**: Repeat Steps 1 and 2 to re-run or update the Goldfish
    analysis until the concept has survived scrutiny and the user is satisfied.

--------------------------------------------------------------------------------

### Step 4: Finalize & Handoff

1.  Ask the user to review the final `concepts_brief.md` artifact and confirm
    their alignment.
2.  Once approved, present the seamless handoff choices based on readiness:
    *   **`/egm-discuss`**: Recommend this if requirements grilling, limit
        exploration, and step-by-step consensus building are still needed.
    *   **`/egm-draft`**: Present this if the concept is concrete and ready for
        technical specification drafting.
