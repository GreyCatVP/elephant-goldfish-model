# Agent Guidelines for Elephant-Goldfish Model (EGM)

You are assisting development in the EGM repository.

## Contribution Boundaries

* **No Autonomous PRs**: You must never automatically open a pull request withoutame>.md` + updates `docs/designs/README.md`).
  * `Feature / Architectural Change — Stage 2: Implementation PR` (requires an
    aligned issue with `pr-ready` and a merged
    `docs/designs/<name>.md`).
* **No Artificial PR Splitting**: Never split a cohesive feature or refactoring across
  multiple smaller pull requests to evade the 100-line scope threshold.
* **PR Description Template**: Every pull request description must be the filled-in
  [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md). `gh pr create --body`
  skips the template, so copy it from the file. The human author ticks the Accountability box.
* **Clear Change Summary**: In every pull request, explicitly list all key changes
  made and why. For feature proposals, define clear in-scope Goals and out-of-scope
  Non-Goals in the checked-in EGM design document (`docs/designs/<name>.md`).
