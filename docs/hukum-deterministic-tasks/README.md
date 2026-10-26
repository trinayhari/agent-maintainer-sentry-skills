# Browser-free task proposals

Status: **owner accepted for the bounded test on 23 October 2026**. The user
explicitly approved these three task meanings and the proposed bounded run.
These three tasks cover two
existing Sentry skills at source commit
`94ba0a47b16d5f6f2903ad866f1524cd2be2cfdb`. They exercise drafting decisions from
provided repository facts. They do not create Git branches or commits.

| Task | Skill source | Objective checks | Semantic judgment |
| --- | --- | --- | --- |
| `refactor-link` | `skills/commit/SKILL.md`, Message Rules and Footers | Strict JSON shape; `ref` type; `cache` scope; `Refs #42`; nonbreaking; bounded subject without final period; no tool calls | Useful, accurate, imperative subject for extracting shared cache-key normalization without behavioral change |
| `fix-null-response` | `skills/commit/SKILL.md`, Message Rules and Footers | Strict JSON shape; `fix` type; `api` scope; `Fixes #73`; nonbreaking; bounded subject without final period; no tool calls | Useful, accurate, imperative subject for returning the intended 404 for deleted accounts instead of HTTP 500 |
| `collision-plan` | `skills/create-branch/SKILL.md`, Workflow steps 2–6 | Strict JSON shape; retain current nondefault base; choose the first unoccupied collision suffix across local and remote names; equivalent creation commands accepted; no tool calls | Coherent plan that does not claim actual execution or invent repository facts |

The JSON envelope is a task input/output requirement that makes message
components independently inspectable. It is not a claim that the source skill
normally emits JSON. Exact task scopes, issue IDs, short branch description and
repository state are explicit fixture facts. No exact commit subject is required.

The source skill specifies imperative/capitalized subjects and conventional
types. Deterministic checks own the mechanically verifiable fields and limits;
the retained LLM judge owns usefulness, accuracy and phrasing. A model judgment
cannot override a deterministic failure. The branch task is mostly mechanical;
its semantic review is deliberately narrow. These cases do not establish general
copywriting quality, arbitrary Git correctness or safety of actual mutations.

## Controls and review boundary

[controls.json](controls.json) contains 44 synthetic full-wire responses: known-good,
distinct allowed-alternative, targeted negative controls for every structured
requirement, and interrupted responses. Alternative commit subjects are both
valid. The branch alternative uses `git switch -c` instead of `git checkout -b`
and changes JSON property order/whitespace; both create and switch to the same
branch. Every negative declares the exact requirement
it should violate. These are grader controls, not model evaluations.
Each assertion predicate has its own negative: a wrong type cannot substitute
for exercising a length or punctuation boundary. Subject controls separately
exercise an empty string, 71 characters, a final period, newline and carriage
return. The good subjects stay within the source limit of 70 characters.

[semantic-criteria.json](semantic-criteria.json) supplies the full task facts as
well as the bounded qualitative rubric because the judge receives criteria and
response evidence, not an implicit copy of the task prompt. These criteria and
controls stay outside the runtime skill directories and are never part of the
agent request. Passing structured controls does not calibrate the LLM judge.

[Validation receipts](validation-receipts.json) record all 44 structured controls
passing with complete per-predicate coverage and zero model calls. They are
inner grader receipts; the execution policy separately binds the exact accepted
task, evaluator, runtime and model. They do not themselves authorize execution.

[Semantic review examples](semantic-review-examples.json) give each commit task
an accurate subject and a structurally valid but inaccurate subject. All four
must pass objective constraints; only the latter two should fail qualitative
review. These are review fixtures, not recorded model-judge outcomes. The branch
plan's objective fields nearly exhaust its meaning, so there is no independent
semantic-only failure fixture for that task. Retaining its model review does not
establish additional signal or replace the exact checks.

The task meanings and bounded test are accepted, and structured controls pass.
Before execution, prepare a trusted policy bound to the exact tasks, grader,
deployed runtime and model. Qualitative positive/negative examples are review
fixtures; actual judge calibration is not claimed by the structured receipts.
Keep both skill arms on the same task/model/check/semantic contract. A local
paired invocation on immutable external-repository commits is not evidence of
automatic hosted PR delivery.

The intended run is one pair per task: six Claude agent invocations at at most
2,048 output tokens each and six semantic judgments. Input tokens and AWS
infrastructure charges are additional. The user accepted this bounded test;
do not treat it as an allowance for unattended recurring runs. Existing AXIS
tests are untouched; this bounded Claude drafting
subset does not replace real coding-agent integration tests.
