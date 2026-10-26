# Draft: representative Sentry copywriting tasks

Status: **not validated, not accepted, and not enabled for paid evaluation**.

Source: `skills/brand-guidelines/SKILL.md` at repository commit `94ba0a47b16d5f6f2903ad866f1524cd2be2cfdb`. These proposals describe the existing Sentry copywriting skill. They do not change that skill or introduce Anthropic HTML branding criteria.

## Candidate tasks

- **Payment failure:** write a short product message explaining that a payment was declined and the user can update their payment method. This exercises Plain Speech for billing/errors: clear cause, actionable next step, and no joking at the user's expense.
- **Missing page:** write a 404 headline, short explanation, and navigation button. This exercises restrained Sentry Voice where the skill permits it, while preserving understandable recovery.
- **Account settings:** write a label, explanatory sentence, and button for changing a notification preference. This exercises the skill's plain, direct settings language and capitalization conventions.

These prompts still require owner review for task realism, output format, and adequate coverage. The source does not specify a numeric pass threshold or dictate an exact acceptable sentence; this draft does not invent either.

## Validation required before acceptance

For each reviewed prompt, obtain an owner-approved good response and a deliberately failing response. Verify the grader rejects the failing response for the intended reason without requiring one exact phrasing. Include an over-strict counterexample: different wording that still accomplishes the task and follows the source. Keep private scoring criteria and control answers outside the agent's runtime bundle.

Separate objective output checks (required response fields, empty or missing output) from semantic judgments (tone, clarity, appropriate voice). Do not represent keyword presence as proof that copy is useful. Record task provenance, approval, control outcomes, limitations, grader/runtime/model identity, and the accepted task policy before running the hosted comparison.

The hosted acceptance test additionally requires an actual same-repository skill-only PR, automatic paired base/head execution, a current-head GitHub comment, and matching HTML/JSON artifacts. This draft is not evidence of that test.
