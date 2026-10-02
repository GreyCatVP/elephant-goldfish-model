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

# Elephant & Goldfish Model (EGM)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Website](https://img.shields.io/badge/Website-egm.dev-black.svg)](https://egm.dev)

The **Elephant & Goldfish Model (EGM)** is an open-source framework and methodology for Spec-Driven Development (SDD) with autonomous AI coding agents.

It anchors development in context-rich system descriptions and adversarial multi-agent reviews, making complex codebases easier for both humans and AI to navigate, verify, and evolve.

---

## The Philosophy

EGM uses two animal metaphors to describe how to prompt, constrain, and structure AI agents at different stages of the software development lifecycle:

*   🐘 **The Elephant (Remembers Everything)**:
    Deep-context agents loaded with system history, architecture diagrams, component boundaries, and user journeys. The Elephant conducts structured brainstorming, probes operational limits, and drafts comprehensive specifications.
*   🐠 **The Goldfish (Zero-Context Memory)**:
    Stateless, isolated subagents that read only the draft design specification and live source code without access to conversational bias. The Goldfish swarm subjects designs to adversarial stress-testing across multiple conflicting perspectives (Design Critic, Naive Reader, Tech Lead, Codebase Auditor, Structural Validator, and Style Editor).
*   🧑‍💻 **The Human (Owns the Outcomes)**:
    AI is an exploration partner and automated auditor, but human engineers own architectural decisions, trade-offs, and final outcomes.

For the foundational essay introducing this methodology, see Dave Rensin's article: [Elephants, Goldfish, and the New Golden Age of Software Engineering](https://medium.com/@drensin/elephants-goldfish-and-the-new-golden-age-of-software-engineering-c33641a48874).

---

## Repository Structure

```
├── assets/                       # Branding assets and diagrams
├── docs/                         # Documentation, guides, and FAQ
│   └── designs/                  # Living technical design specifications
├── personas/                     # Stateless reviewer and orchestrator persona prompts
├── resources/
│   └── document_standards/       # Quality evaluation rubrics and standards
├── rules/                        # Continuous behavioral and cognitive rules
├── skills/                       # Modular agent skills (Brainstorm, Draft, Review, etc.)
└── tests/
    └── evals/                    # Automated YAML evaluation benchmarks
```

---

## The Skills Catalog

| Skill | Command | Description |
| :---- | :------ | :---------- |
| **Brainstorm** | `/egm-brainstorm` | Zero-doc ideation tool using a 6-lens Goldfish shootdown swarm to stress-test early concepts. |
| **Draft** | `/egm-draft` | Iterative, section-by-section markdown design specification compiler. |
| **Review** | `/egm-review` | Multi-stage verification pipeline orchestrator (Zoom Out → Comprehension → Critic → Readiness). |
| **Review Loop** | `goldfish_review_loop` | Concurrent review subagent dispatch engine supporting direct and hierarchical dispatch. |
| **Review Resolve** | `/goldfish-review-resolve` | Interactive triage and automated patch application engine for review findings. |
| **Drift Report** | `/egm-drift-report` | Sequential AST scanner detecting divergence between checked-in specs and live code. |
| **Bootstrap** | `/egm-bootstrap` | Recursive bottom-up codebase documentation generator and sentinel-block upserting engine. |

---

## Behavioral Rules (`rules/`)

EGM includes a set of modular behavioral and cognitive rules under `rules/` designed to keep AI coding assistants grounded, critical, and robust:

| Rule File | Objective & Constraint |
| :-------- | :--------------------- |
| [`rules/anti_sycophancy.md`](rules/anti_sycophancy.md) | **Critical Thinking & Anti-Sycophancy**: Eliminates hollow flattery and sycophantic agreement. Mandates stress-testing ideas first, highlighting edge cases, and providing constructive counter-arguments. |

### Installing Rules in Antigravity

EGM behavioral rules are natively supported in Antigravity. Place or symlink the `rules/` directory into your Antigravity workspace or plugin configuration to have them automatically injected into context prompts.

---

## Quickstart & Core Workflow

1.  **Ideate & Stress-Test**:
    Run `/egm-brainstorm` to explore problem boundaries and subject raw concepts to a multi-lens Goldfish shootdown swarm.
2.  **Draft**:
    Run `/egm-draft` to convert the concept brief into a living design document under `docs/designs/<feature>.md`.
3.  **Review**:
    Run `/egm-review docs/designs/<feature>.md` to launch the multi-stage Goldfish reviewer swarm.
4.  **Resolve & Merge**:
    Triage findings using `/goldfish-review-resolve`, submit the design doc via Pull Request, and implement code against the verified specification.

For detailed setup and walkthroughs, see [Getting Started](docs/getting_started.md) and the [Framework Architecture](docs/designs/architecture.md).

---

## Contributing

We welcome community contributions! Please review our [Contribution Guidelines](CONTRIBUTING.md) before submitting pull requests.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
