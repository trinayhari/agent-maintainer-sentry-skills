# Commit skill maintenance contract

## Intent and scope

Help developers draft Sentry-style commit messages and create coherent commits.
Draft-only requests produce an artifact from supplied facts without repository
mutation. Actual commit requests retain the branch and reviewable-change checks.

## Source and evidence

The existing Message Rules, Footers and Creating the Commit sections are the
behavioral source. The draft-only clarification preserves the distinction between
writing a message and performing a commit; issue linking must not silently become
issue closure. Use anonymized change descriptions when reviewing examples.

## Validation and maintenance

Review accurate message drafts, misleading but well-formatted drafts, and requests
to reference an issue without closing it. Check actual commits in an isolated Git
repository before claiming repository execution works. Output-format checks alone
do not establish subject accuracy or reviewer usefulness. Preserve valid alternate
wording and maintain the existing privacy restrictions.

Keep runtime instructions in SKILL.md. Store evaluation fixtures and private
grading criteria outside the runtime skill directory. Revisit this contract when
drafting, mutation, issue semantics or privacy expectations change.
