# CCA-Foundations — Practice Exam Answer Key & Explanations

> Grade against `practice-exam.md`. Each answer cites the underlying principle. If you miss one, re-read the relevant section of `study-guide.md` (the "12 Decision Heuristics" + the matching domain cheat sheet).
>
> **Scoring guide:** 52/65 (80%) is a solid go-signal. Below ~46/65 (70%), review weak domains before sitting the exam. *(These are study proxies — the real exam is scaled 100–1,000 with a 720 pass mark, which does not map to a published raw percentage; see the note at the end.)*

---

## Scenario 1 — Customer Support Resolution Agent

**Q1 → A.** Terminate the agentic loop on `stop_reason`: continue while `"tool_use"`, stop on `"end_turn"`. Parsing natural-language phrases (B), arbitrary iteration caps as the primary stop (C), and checking tool status/assistant text (D) are the named anti-patterns.

**Q2 → B.** A required tool *sequence* with financial consequences needs deterministic enforcement. A programmatic prerequisite gate guarantees it; prompt instructions (A) and few-shot (C) are probabilistic with a non-zero failure rate. A routing classifier (D) controls which tools are *available* for a request, not the *order* they're invoked — so it can't guarantee `get_customer` runs before `process_refund`. *(Heuristic #1)*

**Q3 → B.** Tool descriptions are the primary mechanism the model uses to select tools. With minimal descriptions, the low-effort, root-cause fix is to enrich them (inputs, examples, edge cases, boundaries). Few-shot (A) adds token overhead without fixing the cause; a router (C) is over-engineered; consolidation (D) is a bigger architectural change than a "first step" warrants. *(Heuristic #2)*

**Q4 → B.** A hard compliance limit ($500) requires a deterministic guarantee *before* the action: a tool-call interception hook that blocks and redirects to escalation. Prompt/few-shot (A, C) are probabilistic. A nightly audit (D) only flags violations *after* the refund has already been issued — too late for a hard prevention requirement. *(Heuristic #1)*

**Q5 → C.** Decompose multi-concern requests into distinct items, investigate each (in parallel, shared context), then synthesize one resolution. Escalating (A), deferring (B), or dropping concerns (D) all fail the customer.

**Q6 → C.** Escalate on a **policy gap** — the policy is silent on competitor matching. Don't decline by default (A), unilaterally approve (B), or stretch an unrelated policy (D).

**Q7 → B.** Extract transactional facts into a persistent "case facts" block included each turn, outside summarized history. A recency window (A) still drops those facts once they age past the verbatim cutoff; disabling summarization and sending the raw transcript (C) doesn't scale and reintroduces the cost summarization solved; (D) shifts the burden to the customer.

**Q8 → B.** Uniform "Operation failed" prevents appropriate recovery. Return structured metadata: `errorCategory`, `isRetryable`, human-readable description. Blind retry (A), terminating (C), and empty-success (D) are anti-patterns.

**Q9 → C.** Multiple matches → ask for an additional identifier. Don't pick by recency (A) or infer identity from fuzzy context matches (B) — both risk acting on the wrong person's account — and don't jump straight to a human (D) when one clarifying question resolves it.

**Q10 → C.** The human lacks the transcript, so the handoff must be a structured summary: customer ID, root cause, refund amount, recommended action. A bare last message (A), a raw transcript link (B), or ID-only (D) make the human redo the work.

---

## Scenario 2 — Code Generation with Claude Code

**Q11 → A.** Project-scoped slash commands live in `.claude/commands/` in the repo (version-controlled, auto-available on clone/pull). `~/.claude/commands/` (B) is personal; `CLAUDE.md` (C) is for context, not command definitions; (D) `.claude/config.json` with a `commands` array doesn't exist.

**Q12 → A.** Conventions placed at user level (`~/.claude/CLAUDE.md`) aren't shared via version control, so a new member doesn't get them. `/compact` (B), truncation (C), and re-stating per prompt (D) miss the hierarchy issue. (Diagnose with `/memory`.)

**Q13 → A.** Plan mode fits large-scale, multi-file, multiple-valid-approach, architectural work — exactly monolith→microservices. Incremental discovery (B) and "switch later" (D) risk costly rework; comprehensive upfront instructions (C) assume you already know the structure. *(Heuristic #5)*

**Q14 → A.** `.claude/rules/` with `paths:` glob frontmatter applies conventions by file type regardless of location and loads only when editing matching files. Monolithic CLAUDE.md relies on inference (B); per-directory CLAUDE.md is directory-bound (C); a manual slash command (D) isn't automatic. *(Heuristic #6)*

**Q15 → A.** `context: fork` runs the skill in an isolated sub-agent context so verbose/exploratory output doesn't pollute the main conversation. `allowed-tools` (B) restricts tools; `argument-hint` (C) prompts for params; (D) doesn't address pollution.

**Q16 → A.** Keep CLAUDE.md modular with `@import` to reference external standards files and/or split topics into `.claude/rules/`. Deleting sections (B) loses content; one giant skill (C) changes loading semantics; duplication (D) creates drift.

**Q17 → B.** Use scratchpad files to persist key findings across context boundaries and `/compact` to reduce context when it fills with verbose output. Periodic `/clear` (A) discards the very findings you need; switching to a bigger-context model (C) doesn't address degradation caused by *clutter* rather than capacity; pasting the whole codebase (D) accelerates the problem.

**Q18 → A.** `allowed-tools` restricts the skill to read/validation (prevents destructive actions); `argument-hint` prompts for the missing environment parameter. (B) and (C) miss the restriction or the prompt. (D) is the tempting near-miss: `argument-hint` is right, but `context: fork` only isolates the skill's context — it doesn't stop it from modifying files, which is the actual requirement.

**Q19 → B.** When prior tool results are stale, start fresh with a structured summary rather than resuming with stale results. Resuming (A) or forking (C) trusts stale data; re-running everything (D) is wasteful.

**Q20 → A.** Combine plan mode (investigate/design the 45-file migration) with direct execution (implement the planned approach). Direct-only (B), plan-for-edits (C), and Explore-makes-edits (D) misuse the modes.

---

## Scenario 3 — Multi-Agent Research System

**Q21 → B.** The coordinator's logs reveal it decomposed "creative industries" into only visual-arts subtasks. The subagents executed their assignments correctly — the gap is too-narrow coordinator decomposition. Don't blame downstream agents working within scope (A, C, D). *(Heuristic #7)*

**Q22 → B.** Subagents have isolated context and don't inherit other agents' results; pass the search findings explicitly in the synthesis agent's prompt. Memory isn't shared (A). It isn't an ordering race (C) — search finished and found the data; it simply never entered synthesis's context. Giving synthesis the search tool to re-fetch (D) is wasteful and treats the symptom.

**Q23 → A.** Spawn parallel subagents by emitting multiple `Task` calls in a single coordinator response — the runtime runs them concurrently. Separate turns (B) serialize them; a `max_concurrent` config option (C) doesn't exist; passing prompts as an array to one `Task` call (D) isn't the mechanism.

**Q24 → A.** Return structured error context (failure type, attempted query, partial results, alternatives) so the coordinator can recover. Generic status (B), empty-as-success (C), and terminating the workflow (D) are anti-patterns. *(Heuristic #8)*

**Q25 → A.** Least privilege for the 85% common case: give synthesis a scoped `verify_fact` tool and keep complex cases routing through the coordinator. Over-provisioning (B), end-of-pass batching that creates blocking deps (C), and speculative caching (D) are all worse. *(Heuristic #9)*

**Q26 → B.** Require structured claim-source mappings (claim → URL/doc + excerpt) preserved through synthesis. A disclaimer (A) and re-searching every claim at the end (C) don't help; a per-agent bibliography (D) records *which sources were seen* but not *which claim came from which source*, so provenance is still lost.

**Q27 → B.** Design the coordinator to analyze the query and dynamically select which subagents to invoke based on complexity, rather than always routing through the full pipeline (A) or hard-coding sequences (C). Subagents shouldn't self-select (D).

**Q28 → C.** Annotate conflicting credible stats with source attribution and include publication dates so temporal differences aren't read as contradictions. Taking only the newer figure (A) or only the more authoritative source (B) silently drops context; omitting it (D) loses the data point.

**Q29 → B.** Iterative refinement: the coordinator evaluates synthesis for gaps, re-delegates targeted queries, and re-invokes synthesis until coverage suffices. Accepting the gap (A) or disclaiming it to the reader as a "limitation" (C) leave the report incomplete when it's fixable; a full restart (D) wastes the work already done.

**Q30 → B.** Subagents recover locally for transient failures; if unrecoverable, propagate only that error plus partial results and what was attempted. Terminating the workflow (A) or failing the whole batch (C) discards nine good results; silently dropping the doc (D) hides the gap.

---

## Scenario 4 — Developer Productivity Tools

**Q31 → A.** Grep searches file *contents* (callers of a function). Glob (B) matches paths/names; Read-everything (C) is inefficient; a custom Bash script (D) reinvents Grep.

**Q32 → A.** When Edit fails on non-unique text, Read the full file then Write it back with the change. `replace_all` (B) would change *every* occurrence, not the single intended line; delete/recreate (C) is destructive; Glob (D) finds files, not unique text.

**Q33 → A.** Shared team server → project `.mcp.json` (with `${ENV_VAR}` for the credential); personal/experimental → user `~/.claude.json`. A fictional `personal: true` flag (B), user-only assumption (C), and committing secrets (D) are wrong. *(Heuristic #4)*

**Q34 → A.** Use env var expansion `${GITHUB_TOKEN}` in `.mcp.json` so the secret isn't committed. Gitignoring a committed token (B), CLAUDE.md (C), and comments (D) all leak or misplace the secret.

**Q35 → B.** Build understanding incrementally: Grep entry points, then Read to follow imports and trace flows. Reading everything (A), filename summaries (C), and pasting the codebase (D) waste context.

**Q36 → A.** Expose content catalogs (issue summaries, doc hierarchies, DB schemas) as MCP *resources* to give the agent visibility without exploratory tool calls. More tools (B) hurts selection; caching in CLAUDE.md (C) goes stale; a single dump-everything tool (D) still costs a call and floods context — resources are the right ambient primitive.

**Q37 → A.** Delegate verbose exploration to subagents that return summaries while the main agent coordinates; use scratchpad files for key findings. A larger-context model (B) only delays dilution; disabling tool output (C) or blindly truncating it (D) throws away information the agent needs.

**Q38 → A.** Replace the generic `fetch_url` with a constrained `load_document` that validates document URLs, with a clear boundary description. A prompt warning (B), more tools (C), and removing tools (D) are weaker.

**Q39 → B.** Open-ended tasks call for dynamic decomposition: map structure, identify high-impact areas, build a prioritized plan that adapts as dependencies surface. One giant file (A), alphabetical pipeline (C), and refusing (D) are wrong.

**Q40 → A.** Prefer the well-maintained community MCP server for standard integrations (Jira); reserve custom servers for team-specific workflows. Always-custom (B), Bash REST calls (C), and built-ins-only (D) add cost or capability gaps.

---

## Scenario 5 — Claude Code for Continuous Integration

**Q41 → A.** `claude -p` (`--print`) runs non-interactively: processes the prompt, prints to stdout, exits. `CLAUDE_HEADLESS=true` (B) and `--batch` (D) are fictional; `< /dev/null` (C) is a hack, not the documented mechanism. *(Heuristic #10)*

**Q42 → A.** `--output-format json` with `--json-schema` yields machine-parseable structured output for inline PR comments. The other flags are fictional or unrelated.

**Q43 → B.** Replace the vague instruction with an explicit categorical criterion ("flag a comment only when its claimed behavior contradicts the actual code behavior"). "Be conservative / high-confidence" (A) doesn't sharpen the rule; restricting which comments are checked (C) cuts volume but not the false-positive *rate*; double-checking (D) just re-applies the same vague criterion. *(Heuristic #3)*

**Q44 → A.** Multi-pass: per-file local analysis + a separate cross-file integration pass — fixes attention dilution and contradictory feedback. Pushing work to developers (B), a bigger context window (C), and consensus-of-3 (D, which suppresses intermittently-caught real bugs) are all wrong. *(Heuristic #12)*

**Q45 → B.** A session retains its generation reasoning, so it's predisposed to defend its own decisions; use an independent review instance with no prior context. "Review carefully" (A), extended thinking in the same session (C), and asking the same session to "re-read from scratch" (D) all leave the biasing generation context in place.

**Q46 → A.** Include prior findings in context and instruct "report only new or still-unaddressed issues." Deleting comments first (B) loses the audit trail; reviewing once per PR (C) misses regressions; text-hash dedup (D) fails on reworded findings or shifted line numbers and can't distinguish fixed from open.

**Q47 → A.** Few-shot examples demonstrating the exact output format (location, issue, severity, fix) achieve consistency when instructions alone fail. "Be consistent" (B) is vague; switching models (C) doesn't target format; writing even more detailed prose (D) is exactly what the stem says already failed.

**Q48 → A.** Batch the latency-tolerant overnight report (50% savings, up to 24h, no SLA); keep synchronous calls for the blocking pre-merge check where a developer waits. Batching the blocking workflow (B, D) breaks the wait requirement; keeping both real-time (C) misses savings and misreads `custom_id` correlation. *(Heuristic #11)*

**Q49 → A.** Document testing standards, valuable criteria, and fixtures in CLAUDE.md, and provide existing test files so generation avoids duplicate coverage. Generating more tests (B), allowing longer outputs (C), or enabling extended thinking (D) don't help when the model can't see what's already covered.

**Q50 → A.** Temporarily disable the high-false-positive category while improving its prompt, preserving trust in the accurate categories. Tolerating noise (B), lowering thresholds globally (C, which *increases* false positives), and merging categories (D) erode trust further.

---

## Scenario 6 — Structured Data Extraction

**Q51 → A.** Tool use with a JSON schema is the most reliable path to guaranteed schema-compliant output and eliminates JSON syntax errors. Prompt pleas (B), regex repair (C), and asking for a fenced ```json block (D) all leave validity to chance.

**Q52 → A.** Make fields the source may lack optional/nullable so the model returns null instead of fabricating. A required field with "don't make up values" (B) or a few-shot blank example (D) still structurally pressures fabrication; post-processing defaults (C) hide the gap rather than surfacing it.

**Q53 → A.** Enum of known categories + `"other"` + a free-text detail field handles knowns and extends gracefully. Free-text (B) loses structure; a strict enum with no escape (C) fails on novelty; per-category booleans (D) are clumsy.

**Q54 → A.** Retry-with-error-feedback: include the original document, the failed extraction, and the specific validation error. Identical retries (B) repeat the mistake; chunking (C) targets size limits, not a misplaced-value error; skipping (D) loses the record.

**Q55 → B.** Retries don't help when the information is simply absent from the source (unlike format/structural errors). Make the field nullable, route to another source, or send to a human. Raising temperature (C) or adding few-shot (D) can't conjure missing data.

**Q56 → A.** `"any"` forces a tool call (not prose) while letting the model choose which schema. `"auto"` (B) may return text; a forced specific tool (C) is wrong when you don't know which applies; no setting (D) doesn't guarantee a tool call.

**Q57 → A.** Output field-level confidence scores and calibrate thresholds with a labeled validation set; route low-confidence/ambiguous to humans. Random 10% (B) and everything (C) waste capacity; trusting self-reported confidence (D) is poorly calibrated.

**Q58 → B.** Aggregate accuracy can mask weak performance on specific doc types/fields; analyze accuracy by document type and field (stratified random sampling for ongoing measurement) before reducing review. Dropping review (A), speed-only (C), and re-training (D, out of scope) are wrong.

**Q59 → B.** Strict schemas eliminate syntax errors but not semantic ones (line items not summing). Extract `calculated_total` alongside `stated_total` to flag discrepancies (or add `conflict_detected`). It's not a parsing bug (A); tighter type constraints (C) still only validate structure, not arithmetic; a prompt to "double-check the math" (D) is probabilistic, not a guaranteed catch.

**Q60 → A.** Resubmit only the failed documents (by `custom_id`) with modifications such as chunking the oversized ones. Resubmitting all 100 (B) wastes cost; switching to sync (C) overcorrects; discarding (D) loses coverage.

---

## Bonus — Higher-Difficulty Questions

**Q61 → A.** Add explicit escalation criteria with few-shot examples — this directly addresses the root cause: unclear decision boundaries, and it's the proportionate first move before adding infrastructure. Self-reported confidence (B) is poorly calibrated (the agent is already confidently wrong on hard cases). A trained classifier (C) is over-engineered — labeled data + ML infra before prompt optimization has even been tried. Sentiment analysis (D) solves a different problem; frustration doesn't correlate with case *complexity*. *(Heuristic #3 — explicit criteria + few-shot over confidence/ML/sentiment.)*

**Q62 → A.** Idempotency keys make retries safe deterministically: the server de-duplicates repeats of the same request, so a timeout-triggered retry can't double-refund. A prompt instruction not to retry (B) is probabilistic and the agent can't reliably know whether the first call landed. Swallowing the timeout (C) loses the outcome and may skip a refund that's genuinely needed. Disabling retries (D) overcorrects — now transient timeouts cause *missed* refunds. *(D5 reliability: design for safe retries, don't just suppress them.)*

**Q63 → A.** The dependency is structural, so stage it: discovery search first, then fan out the dependent searches in parallel once their inputs exist, then synthesize. Giving the dependent agents their own search tool (B) duplicates the discovery work and invites inconsistency. Raising the iteration cap (C) re-runs the same searches without ever supplying the missing inputs. One giant merged prompt (D) sacrifices parallelism and focused scope, recreating attention dilution. *(D1 — decomposition must respect data dependencies; parallelize only the independent stages.)*

**Q64 → A.** Consolidating near-duplicate tools into one well-described tool with a `mode` parameter removes the selection ambiguity at its source (too many overlapping tools degrade selection). A look-up meta-tool (B) adds a round trip and still leaves the ambiguity among near-duplicates. More reasoning budget (C) can't disambiguate genuinely overlapping tools. Tool *order* in the schema (D) doesn't reliably drive selection. *(Heuristic #9 — least privilege / fewer, clearer tools.)*

**Q65 → A.** Model the repetition structurally: `line_items` as an array of objects with a fixed sub-schema validates each item and its sub-fields. Numbered fields (B) cap the count and waste schema, breaking on larger invoices. A free-text block (C) reintroduces the parsing problem structured output was meant to remove. A prompt reminder on a flat schema (D) is probabilistic — the array sub-schema enforces capture. *(D4 — match the schema shape to the data's shape.)*

---

## Recurring principles tested (self-check)
If you missed several, the gap is usually one of these:
- **Deterministic (hook/gate/idempotency) > prompt** when correctness must be guaranteed. (Q2, Q4, Q62)
- **Tool descriptions** are the primary selection lever; fix them first. (Q3, Q38)
- **Explicit criteria + few-shot** > confidence/sentiment/ML/vague. (Q43, Q47, Q57, Q61)
- **Scope → location** (project vs user). (Q11, Q12, Q33)
- **Plan mode** for complex/architectural/multi-file. (Q13, Q20)
- **`.claude/rules/` globs** for cross-directory conventions. (Q14)
- **Coordinator decomposition** is the usual root cause of coverage gaps; respect data dependencies; subagents have **isolated context**. (Q21, Q22, Q63)
- **Structured error context** > generic/empty/terminate. (Q8, Q24, Q30)
- **Least privilege / scoped, non-overlapping tools**; too many (or too similar) tools hurts selection. (Q25, Q36, Q64)
- **`-p` for CI**; `--output-format json`/`--json-schema` for structured CI output. (Q41, Q42)
- **Batch API** = non-blocking only; sync for blocking. (Q48, Q60)
- **Multi-pass / independent review** > single-pass / bigger model / consensus. (Q44, Q45)
- **tool_use + schema** kills syntax not semantics; **nullable fields** prevent fabrication; **schema shape matches data shape**; **retries can't fix absent data**. (Q51, Q52, Q55, Q59, Q65)

---

## A note on scoring (why your practice % isn't the same as 720)

The real exam reports a **scaled score from 100–1,000 with a pass mark of 720** — this is *not* a raw percentage, and Anthropic does not publish the raw-correct-to-scaled mapping. Scaled scoring (the same approach AWS, CompTIA, and similar certs use) statistically equates different exam forms so that a given scaled score means the same competency regardless of which mix of questions you got. So **720 ≠ 72% correct**; depending on form difficulty it typically corresponds to *roughly* the low-to-mid 70s in raw terms, but that's an unofficial rule of thumb, not a guarantee.

Practical upshot: treat the percentages here purely as a **study signal**, not a score prediction. The ≥ 80% target is deliberately set *above* the likely pass line to give you margin. If you're consistently clearing 80% across the by-topic drills, you're in good shape.
