# Create-branch skill maintenance contract

## Intent and scope

Help developers choose and create Sentry-style branches. Respect an explicit
plan-only request without mutation; actual creation follows the existing workflow.
The caller's repository facts determine the current/default base and collisions.

## Source and evidence

The existing Workflow governs type selection, ASCII kebab-case names, base
selection, local/remote collision handling and creation. The clarification makes
the joint collision check and plan/execution distinction explicit. It does not
change branch-type policy or authorize an unsolicited switch to the default base.

## Validation and maintenance

Review ordinary and collision cases, current nondefault branches, detached heads,
and absent default-branch metadata. Preserve equivalent Git commands that create
the same branch from the same base. Validate actual mutations in an isolated Git
repository; a correct proposed command does not establish successful execution.

Keep runtime instructions in SKILL.md. Store evaluation fixtures and private
grading criteria outside the runtime skill directory. Revisit this contract when
branch naming, base selection, collision or mutation policies change.
