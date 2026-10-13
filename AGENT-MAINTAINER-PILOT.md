# Native skill evaluation pilot

This PR connects the code-review skill to Agent Maintainer's bounded native evaluation. It evaluates the skill bytes at the exact PR head, with and without instructions, on two fictional Python review tasks (query scaling and tenant/cache correctness). Each arm runs three times in fresh macOS sandboxes with actual file inspection and Python execution.

The model is gpt-5.4-mini-2026-03-17. Maximum reservation: 144 model requests. Only SKILL.md is supplied; bundled references and Sentry production services are unavailable. These are screening observations, not independent confirmation or release approval. The integration does not change the skill or claim that it is redundant.

The workflow pins the trusted evaluator in trinayhari/agent-maintainer, checks out this PR only as data, and keeps private grader expectations and GitHub publishing credentials outside agent tool execution. The provider key is restricted to the native-evaluation environment. This pilot runs only for the named same-repository codex/native-skill-ci branch and owner-triggered events. It posts commit-bound results on the PR and uploads public evidence for dashboard import. Changed PR heads invalidate the comment publication step. Nothing is automatically merged or approved.
