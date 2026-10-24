# Additional coding-agent harness support

- **Author:** [@n3wth](https://github.com/n3wth)
- **Status:** Proposal; maintainer scope approval and design review pending
- **Date:** 2026-10-24
- **Tracking:** [Cursor #145](https://github.com/google/elephant-goldfish-model/issues/145), [OpenCode #146](https://github.com/google/elephant-goldfish-model/issues/146), [Copilot CLI #147](https://github.com/google/elephant-goldfish-model/issues/147)

## Problem and goals

EGM needs more than a host that can discover SKILL.md files. Reviewers must
read shared personas and standards, run in fresh contexts, and produce auditable
results. Copying skills alone can leave relative resource paths broken.

Extend the shared EGM workflow to Cursor, OpenCode, and GitHub Copilot CLI.
Use small host-specific adapters and the existing workflow fixtures. Treat each
host as an independent support claim. One host can remain experimental while
another passes verification.

This proposal changes no runtime behavior and establishes no support claim.
It is independent of the packaging and release stack in #135, #136, and #137.
Implementation starts only after maintainer alignment and design approval.

## Scope

Goals:

- Install skills, personas, standards, and required guides as one coherent package.
- Preserve brainstorm, draft, review, human approval gates, and file artifacts.
- Launch fresh reviewers with enforceable read-only access where required.
- Record installation, workflow, and isolation outcomes separately.
- Reuse the shared fixtures tracked in #112 without waiting for a new framework.

Non-goals:

- A generic harness registry, transport, compatibility service, or orchestration framework.
- Forking canonical skill or persona text for each host.
- Claiming support for Copilot in VS Code, Cursor cloud agents, or other surfaces
  based on a successful CLI or local IDE run.
- Paid tests in ordinary CI, provider-policy workarounds, or marketplace publication.
- Implementing Hermes, OpenClaw, or Delta here; #116 and #119 own that work.
- Factory Droid or Pi support in this iteration.

## Existing components and ownership

Canonical behavior remains in skills/, agents/, resources/, and the host guides.
See [harnesses](../harnesses.md) and [testing](../../TESTING.md).

The contributor for each host owns its adapter, installation documentation,
offline checks, and live evidence. A maintainer approves the scope and determines
whether that evidence justifies a support claim. The human user retains approval
of designs and other workflow gates.

Adapters may supply discovery metadata, package-relative resource resolution,
delegation instructions, and tool restrictions. They must read canonical persona
text rather than maintaining a second copy of its review rules.

## Architecture and data flow

1. The host installs a pinned EGM candidate into its native package location.
2. The orchestrator loads the shared skill and resolves resources from that package.
3. Each reviewer starts with a fresh conversation. Its task contains the persona
   location, target artifact, required standards, and necessary source paths.
4. The reviewer reads those resources and returns findings through the host's
   native result mechanism. It does not receive the parent's conversation,
   rationale, memory, or previous reviewer findings.
5. The orchestrator waits for all expected completions, identifies failures,
   writes the reports, and stops at the existing human approval gates.

Use direct dispatch when nested delegation is unavailable. A missing reviewer
must not be represented as a passing review. Retry only the failed reviewer when
the native host can preserve the required isolation; otherwise report the
incomplete stage and ask the user how to proceed.

The reviewer role is read-only. Drafting and report-writing roles retain only
the workspace access needed for their outputs. Do not globally weaken host
permissions to make installation or delegation succeed.

Fresh conversation context is necessary but not sufficient. Host-injected
instructions, memory, MCP access, and shared workspace files must be assessed
separately. Context isolation is not filesystem or process isolation.

## Host adapter plans

| Host and initial surface | Proposed mechanism | Required evidence |
| --- | --- | --- |
| Cursor local Agent | Native plugin package and custom subagents using the host's read-only setting. Reuse shared persona files through thin adapter prompts. | Verify installed resource paths, actual read-only enforcement, native completion records, and what context the child receives. |
| OpenCode CLI | Native skill discovery plus Markdown subagent definitions and restrictive tool permissions. Install the complete EGM tree before exposing entry skills. | Select and pin V1 or V2 before implementation. Verify its delegation API, permission schema, isolated child sessions, and package-relative reads. |
| GitHub Copilot CLI | Native plugin installation and custom agent profiles with an explicit tool allowlist. Leave repository-instruction inclusion disabled for reviewers. | Verify the installed package layout, child context, canonical persona reads, tool denial, and reliable result collection. |

The native plugin manifest and path mapping for each host must be confirmed
against the chosen host version before implementation. Do not claim that
Claude-compatible syntax guarantees equivalent behavior.

For OpenCode, the V1 documentation uses task/permission terminology while V2
documents subagent/permissions. This proposal does not select a version on
popularity alone. Record the chosen stable version and its exact mapping in this
document before that host's implementation review.

Retain the current artifact-directory contract in the host guides. Report where
files were written. Do not introduce a new default output directory here.

## Validation and release gates

Offline checks must cover:

- Manifest parsing and identity/version consistency with the existing package.
- All referenced persona, standard, and guide paths in the installed layout.
- Adapter tool restrictions and the absence of duplicated canonical behavior.
- Recorded evidence with missing starts, missing completions, malformed records,
  and Unicode line separators. Reuse existing parsers and fixtures where possible.

Live checks run only on explicit user invocation. Use a clean host profile and
a pinned candidate. Run brainstorm, draft, and review, including a real human
approval pause. Preserve the raw evidence privately when it contains account data.

For every run record candidate SHA, artifact checksum or installed-file identity,
host version and surface, model identifier, date, and the three outcome categories:
installation, workflow, and isolation. Record reviewer starts and completions
from native evidence rather than relying only on the parent's summary.

Isolation checks must include a random marker available only in the parent
conversation, verification of the child's required reads, and inspection of
host-injected context where available. Failure to repeat a marker alone does not
prove isolation. Probe read-only enforcement using a disposable fixture and
confirm that the reviewer cannot modify it.

If native evidence is inaccessible, retain an explicit unverified isolation
result. A passing install must never upgrade an unknown workflow or isolation
result. Scope all conclusions to the tested host version, model, and surface.

No support claim enters the support table until all three categories pass.
Missing delegation must stop the review with a clear unsupported message.
No inline simulation of independent reviewers is permitted.

## Alternatives considered

| Alternative | Decision and rationale |
| --- | --- |
| Skills-only installation through a universal installer | Insufficient by itself: EGM requires personas and standards outside each skill directory. It may be used only if complete package access is proven. |
| Copy the entire runtime once per host | Reject: duplicated content drifts. Keep canonical content shared and adapters small. |
| Reuse the parent's conversation for reviewers | Reject: it defeats Goldfish isolation. |
| Build a universal adapter framework first | Reject: three concrete integrations do not justify a new framework. Extract common logic only after duplication appears. |
| Add every harness listed by popular repositories | Reject: adoption elsewhere does not prove EGM's installation or isolation requirements. |
| Support only the current hosts | Lowest maintenance cost, but leaves the demand represented by #145–#147 unmet. Maintainers may choose this until validation capacity is available. |

## Risks and mitigations

- Host API drift: pin versions in evidence and update the adapter with regression checks.
- Hidden context injection: inspect native evidence; keep unknowns explicit.
- Missing package resources: validate the installed tree, not just the source checkout.
- Excessive model cost: run small fixtures manually and record usage when available.
- Partial reviewer completion: fail the stage visibly; do not synthesize a pass.
- Maintenance growth: keep each adapter independent and avoid unused capabilities.

## Rollout and rollback

After scope and design approval, implement one host at a time, starting with
Cursor, then OpenCode and Copilot CLI. Each implementation PR references this
design and closes only its own issue after acceptance criteria pass.

Update installation documentation and the support table in the same implementation
PR as the adapter and evidence. Preserve existing host behavior and tests.
A broken integration can be reverted independently; downgrade its support statement
and retain the failure record. Do not remove unrelated user configuration.

The release-critical work proceeds independently. Inclusion of a new adapter in
a release requires regenerated packages and validation of the exact candidate.

## Open decisions and review status

- Maintainers must approve or revise the three inquiries.
- Confirm maintainers can support the validation and ongoing host-version testing.
- Select the supported OpenCode version and finalize all host manifest mappings.
- The full EGM review pipeline and live host tests have not been run for this proposal.
  This document is not implementation-ready until those decisions and review findings
  are resolved.

## Research references

Reviewed 2026-10-24. These are capability references, not EGM test evidence.

- [Cursor subagents](https://cursor.com/docs/subagents)
- [OpenCode agents](https://opencode.ai/docs/agents/)
- [OpenCode V2 agents](https://dev.opencode.ai/v2/docs/agents/)
- [Copilot CLI custom agents](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli)
- [Superpowers integrations](https://github.com/obra/superpowers)
- [Vercel Skills installation ecosystem](https://github.com/vercel-labs/skills)
- [GBrain integrations](https://github.com/garrytan/gbrain)
