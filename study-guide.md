# Claude Certified Architect — Foundations: High-Yield Study Guide

> The minimum effective dose to pass on the first attempt. Source of truth: Anthropic's official exam guide (v0.1, Feb 2025) — see the README for the link. Everything here is derived from that guide's task statements, sample questions, and appendix.

---

## 1. Exam logistics (know cold)

| Fact | Value |
|---|---|
| Format | 100% multiple choice — 1 correct, 3 distractors. Pick the SINGLE best answer. |
| Scoring | Scaled score **100–1,000**. **Passing = 720.** Pass/fail. |
| Guessing | No penalty. Unanswered = incorrect. **Answer every question.** |
| Scenarios | 6 exist; **4 are presented at random** per sitting. |
| Reported length | ~60 questions / 120 min (per third-party sources — *not* stated in the official guide; treat as approximate). |
| Style | Scenario-based. Distractors are answers a candidate with *incomplete* knowledge would pick. |

**Domain weights** (memorize the ranking — heavier domains = more questions):

| # | Domain | Weight |
|---|---|---|
| 1 | Agentic Architecture & Orchestration | **27%** (biggest) |
| 3 | Claude Code Configuration & Workflows | 20% |
| 4 | Prompt Engineering & Structured Output | 20% |
| 2 | Tool Design & MCP Integration | 18% |
| 5 | Context Management & Reliability | 15% |

**The 6 scenarios** (the exam frames everything inside these):
1. **Customer Support Resolution Agent** — Agent SDK; tools `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`; 80%+ first-contact resolution, knows when to escalate.
2. **Code Generation with Claude Code** — slash commands, CLAUDE.md, plan vs direct.
3. **Multi-Agent Research System** — coordinator delegates to web-search / doc-analysis / synthesis / report subagents.
4. **Developer Productivity** — agent explores codebases; built-in tools (Read/Write/Bash/Grep/Glob) + MCP.
5. **Claude Code for CI/CD** — automated reviews, test gen, PR feedback; actionable, low false positives.
6. **Structured Data Extraction** — extract from unstructured docs, validate against JSON schemas, high accuracy, edge cases.

---

## 2. THE 12 DECISION HEURISTICS (this is how you pass)

Every question is a tradeoff. The same mental models recur. If you internalize these, you can derive most answers. (Each maps to a sample Q in the guide.)

1. **Deterministic guarantee → use code, not prompts.** When a business rule MUST hold (verify identity before refund, block refunds > $X), use **programmatic enforcement** (hooks, prerequisite gates), not system-prompt instructions. Prompts are probabilistic and have a non-zero failure rate. *(Q1)*

2. **Fix the root cause at the lowest-effort, highest-leverage point.** Tool descriptions are the PRIMARY mechanism LLMs use to select tools. If tools are mis-selected and descriptions are minimal → **improve the descriptions** (inputs, examples, edge cases, boundaries) before reaching for few-shot, routing layers, or tool consolidation. *(Q2)*

3. **Explicit criteria + few-shot beats confidence/sentiment/ML.** To fix calibration (when to escalate, what to flag), add **explicit criteria with few-shot examples** to the prompt. Reject: LLM self-reported confidence scores (poorly calibrated), sentiment analysis (doesn't correlate with complexity), and training a separate classifier (over-engineered). *(Q3, Q4.1)*

4. **Scope decides location.** Shared-with-team → **project scope** (`.claude/commands/`, `.claude/CLAUDE.md`, `.mcp.json` — all version-controlled). Personal/experimental → **user scope** (`~/.claude/commands/`, `~/.claude/CLAUDE.md`, `~/.claude.json`). *(Q4)*

5. **Plan mode for complexity; direct execution for simple scope.** Plan mode = large-scale changes, multiple valid approaches, architectural decisions, multi-file (e.g., monolith→microservices, 45-file migration). Direct execution = simple, well-scoped, clear (single-file bug fix). Complexity already stated in requirements → plan mode *now*, not "switch later if it gets hard." *(Q5)*

6. **Conventions spanning directories → `.claude/rules/` with glob path-scoping.** YAML `paths:` frontmatter (e.g., `["**/*.test.tsx"]`) applies rules by file type regardless of location, and only loads when editing matching files. Beats monolithic CLAUDE.md (inference-based, unreliable) and per-directory CLAUDE.md (directory-bound). *(Q6)*

7. **Coverage gaps trace to the coordinator's decomposition.** In multi-agent systems, if output is incomplete but every subagent succeeded *within its assignment*, the root cause is **too-narrow task decomposition by the coordinator**, not the downstream agents. *(Q7)*

8. **Errors → return structured error context.** On failure, return **failure type + attempted query + partial results + alternative approaches** so the coordinator can recover intelligently. Anti-patterns: generic status ("search unavailable"), silently returning empty-as-success, terminating the whole workflow. *(Q8)*

9. **Least privilege + scoped cross-role tool for the common case.** Give an agent a narrow tool for its frequent need (e.g., synthesis agent gets a scoped `verify_fact`) and route the rare complex case through the coordinator. Don't over-provision (give it all web tools), don't batch (creates blocking deps), don't speculatively cache. *(Q9)*

10. **CI/non-interactive → `claude -p` (`--print`).** Runs Claude Code headless: processes prompt, prints to stdout, exits. Fictional distractors: `CLAUDE_HEADLESS=true`, `--batch`. (`< /dev/null` is a hack, not the right answer.) *(Q10)*

11. **Match the API to latency tolerance.** **Message Batches API** = 50% cheaper, up to 24h window, **no latency SLA**, no multi-turn tool calling → use for overnight/weekly/non-blocking. **Synchronous API** → blocking workflows (pre-merge checks where a human waits). Batch results correlate via `custom_id`. *(Q11, 4.5)*

12. **Big multi-file reviews → multi-pass, not single-pass.** Split into per-file local-analysis passes + a separate cross-file integration pass (avoids attention dilution). Also: an **independent review instance** (no generation context) catches more than self-review. Reject: bigger context window, consensus-of-3-runs (suppresses intermittently-caught real bugs), pushing work to developers. *(Q12, 4.6)*

**Meta-rules that decide ties:**
- Prefer the **proportionate, lowest-effort fix that addresses the actual root cause** over heavier infrastructure.
- **Programmatic/deterministic** beats **prompt/probabilistic** whenever correctness is required.
- Don't blame components that are working correctly within their defined scope.
- "Be conservative" / "only high-confidence" / vague instructions **don't** improve precision — specific categorical criteria do.

---

## 3. Domain cheat sheets

### Domain 1 — Agentic Architecture & Orchestration (27%)

- **Agentic loop:** send request → inspect `stop_reason` → if `"tool_use"`, execute tools, append results to conversation history, loop; if `"end_turn"`, done. Tool results MUST be appended so the model reasons on new info.
  - **Anti-patterns:** parsing natural-language to decide loop termination; using an arbitrary iteration cap as the *primary* stop; checking for assistant text as a completion signal. Terminate on `stop_reason`, not heuristics.
  - **Model-driven** (Claude picks next tool from context) vs **pre-configured decision trees** — know the distinction.
- **Coordinator–subagent (hub-and-spoke):** coordinator manages ALL inter-subagent communication, error handling, routing. **Subagents have ISOLATED context — they do NOT inherit the coordinator's history or share memory.** You must pass context explicitly in the prompt.
  - Coordinator does: task decomposition, delegation, result aggregation, deciding *which* subagents to invoke based on query complexity (dynamic selection > always routing through the full pipeline).
  - Route all subagent comms through coordinator → observability + consistent error handling.
- **Spawning subagents:** the **`Task` tool**; `allowedTools` must include `"Task"` for a coordinator to spawn. **`AgentDefinition`** sets per-subagent descriptions, system prompts, tool restrictions. **Parallel subagents = emit multiple `Task` calls in a SINGLE response** (not across turns). **`fork_session`** = independent branches from a shared baseline.
  - Pass complete prior findings directly in the subagent prompt; use structured formats to separate content from metadata (URLs, doc names, page numbers) for attribution.
  - Coordinator prompts should specify **goals + quality criteria**, not step-by-step procedures (enables subagent adaptability).
- **Enforcement & handoff:** programmatic prerequisites block downstream calls until prereqs complete (block `process_refund` until `get_customer` returns verified ID). Structured handoff summary on escalation = customer ID, root cause, refund amount, recommended action (human lacks the transcript).
- **Hooks:** `PostToolUse` intercepts tool *results* for transformation (normalize Unix/ISO-8601 timestamps, status codes) before the model sees them. Tool-call interception hooks block policy-violating outgoing calls (refund > $500) and redirect to escalation. **Hooks = deterministic guarantee; prompts = probabilistic.**
- **Decomposition:** fixed sequential pipeline (prompt chaining) for predictable multi-aspect work; dynamic/adaptive decomposition for open-ended investigation that generates subtasks from what's discovered.
- **Session state:** `--resume <session-name>` continues a named session; `fork_session` for divergent branches; inform a resumed session about file changes for targeted re-analysis. **Starting fresh with a structured summary > resuming with stale tool results.**

### Domain 2 — Tool Design & MCP Integration (18%)

- **Tool descriptions are the primary selection mechanism.** Include input formats, example queries, edge cases, boundaries, and "when to use vs similar tools." Ambiguous/overlapping descriptions (`analyze_content` vs `analyze_document`) cause misrouting. System-prompt keywords can override good descriptions — review them.
  - Fixes: differentiate descriptions; rename to remove overlap (`analyze_content`→`extract_web_results`); split a generic tool into purpose-specific tools with defined I/O contracts.
- **MCP structured errors:** the **`isError`** flag signals failure. Return `errorCategory` (transient / validation / business / permission), **`isRetryable`** boolean, human-readable description. Distinguish retryable vs non-retryable to avoid wasted retries. Business-rule violations: `retriable: false` + customer-friendly explanation. **Distinguish access failures (needing retry decisions) from valid empty results (successful query, no matches).** Subagents do local recovery for transient errors; propagate only the unrecoverable + partial results + what was attempted.
- **Tool distribution:** too many tools (18 vs 4–5) **degrades** selection reliability (more decision complexity). Agents misuse tools outside their specialization (synthesis agent doing web search). Scope each agent's tools to its role; give limited scoped cross-role tools only for high-frequency needs.
- **`tool_choice`:** `"auto"` (may return text instead of a tool), `"any"` (must call *a* tool, model chooses which), forced `{"type":"tool","name":"..."}` (must call that specific tool). Use `"any"` to guarantee a tool call (not conversational text); use forced to make a specific tool run first (e.g., `extract_metadata` before enrichment).
- **MCP server scoping:** project `.mcp.json` (shared team tooling, version-controlled) vs user `~/.claude.json` (personal/experimental). **Env var expansion** `${GITHUB_TOKEN}` in `.mcp.json` for secrets without committing them. Tools from ALL configured servers are discovered at connection time and available simultaneously. **MCP resources** expose content catalogs (issue summaries, doc hierarchies, DB schemas) to reduce exploratory tool calls. Prefer existing community MCP servers (e.g., Jira) over custom for standard integrations.
- **Built-in tools:** **Grep** = content search (find callers, error strings, imports). **Glob** = file path/name patterns (`**/*.test.tsx`). **Read/Write** = full-file ops; **Edit** = targeted change via unique text match. **When Edit fails on non-unique text → Read + Write fallback.** Build understanding incrementally (Grep entry points → Read to follow imports) rather than reading everything upfront. Enhance MCP tool descriptions so the agent doesn't prefer built-in Grep over more capable MCP tools.

### Domain 3 — Claude Code Configuration & Workflows (20%)

- **CLAUDE.md hierarchy:** user `~/.claude/CLAUDE.md` (personal, NOT shared via VCS) → project `.claude/CLAUDE.md` or root `CLAUDE.md` → directory-level subdir `CLAUDE.md`.
  - New teammate missing instructions = they were put at **user level** instead of project level. Diagnose with **`/memory`** to see which memory files loaded.
  - **`@import`** syntax references external files to keep CLAUDE.md modular. **`.claude/rules/`** = topic-specific rule files (testing.md, deployment.md) as an alternative to a monolithic CLAUDE.md.
- **Path-specific rules:** `.claude/rules/` files with YAML frontmatter **`paths:`** glob patterns (e.g., `paths: ["terraform/**/*"]`). Load only when editing matching files (saves context/tokens). **Glob path-scoping beats subdirectory CLAUDE.md for conventions spread across the codebase by file type.**
- **Slash commands & skills:** project `.claude/commands/` (shared via VCS) vs user `~/.claude/commands/` (personal). Skills in `.claude/skills/` with `SKILL.md` frontmatter: **`context: fork`** (run in isolated sub-agent context so verbose/exploratory output doesn't pollute the main conversation), **`allowed-tools`** (restrict tool access during the skill — e.g., limit to writes to prevent destructive actions), **`argument-hint`** (prompt for required params). Personal skill variants go in `~/.claude/skills/` with different names.
  - **Skills = on-demand task-specific invocation; CLAUDE.md = always-loaded universal standards.**
- **Plan vs direct:** see Heuristic #5. The **Explore subagent** isolates verbose discovery output and returns summaries to preserve main-conversation context. Combine: plan mode to investigate, direct execution to implement.
- **Iterative refinement:** concrete **input/output examples** (2–3) > prose when prose is interpreted inconsistently. **Test-driven iteration**: write tests first, share failures to guide fixes. **Interview pattern**: have Claude ask questions to surface considerations (cache invalidation, failure modes) before implementing in unfamiliar domains. **Interacting problems → one detailed message; independent problems → fix sequentially.**
- **CI/CD:** **`-p`/`--print`** = non-interactive mode. **`--output-format json`** + **`--json-schema`** = machine-parseable structured output for posting inline PR comments. CLAUDE.md supplies project context (testing standards, fixtures, review criteria) to CI-invoked Claude Code. Include prior review findings + instruct "report only new/unaddressed" to avoid duplicate comments. Provide existing test files so test-gen doesn't duplicate coverage. **A session that generated code is less effective reviewing its own changes than an independent instance** (retained reasoning context).

### Domain 4 — Prompt Engineering & Structured Output (20%)

- **Explicit criteria > vague.** "Flag only when claimed behavior contradicts actual code behavior" beats "check that comments are accurate." "Be conservative"/"only high-confidence" do NOT improve precision. High false-positive categories undermine trust in accurate ones → temporarily disable bad categories while fixing.
- **Few-shot is the most effective technique** for consistent format / ambiguous-case handling / reducing hallucination when detailed instructions alone fail. Use 2–4 targeted examples showing reasoning for why one option was chosen over plausible alternatives; demonstrate exact output format (location, issue, severity, fix); distinguish acceptable patterns from genuine issues; cover varied document structures. Few-shot enables **generalization to novel patterns**, not just matching pre-specified cases.
- **Structured output via tool use:** `tool_use` + JSON schema = most reliable for guaranteed schema-compliant output; **eliminates JSON syntax errors but NOT semantic errors** (line items not summing, values in wrong fields). Schema design: required vs optional, **enum + `"other"` + detail string** for extensible categories, **nullable/optional fields so the model returns null instead of fabricating** values absent from the source. `tool_choice: "any"` to guarantee structured output when multiple schemas exist; forced selection to run a specific extraction first. Add enum `"unclear"` for ambiguous cases.
- **Validation/retry:** **retry-with-error-feedback** = append the specific validation error + original doc + failed extraction on retry. **Retries DON'T help when the info is simply absent from the source** (vs format/structural errors, which retries fix). Track `detected_pattern` fields to analyze dismissal/false-positive patterns. Self-correction: extract `calculated_total` alongside `stated_total` to flag discrepancies; add `conflict_detected` booleans. Semantic validation errors ≠ schema syntax errors (the latter eliminated by tool use).
- **Batch processing:** Message Batches API — 50% savings, up to 24h, no SLA, **no multi-turn tool calling in a single request**. Use for non-blocking/latency-tolerant (overnight reports, weekly audits, nightly test gen); NOT for blocking (pre-merge). `custom_id` correlates request/response. Resubmit only failed docs (by `custom_id`) with mods (chunk oversized docs). Refine prompts on a sample before batch-processing large volumes. Calculate submission frequency from SLA (4h windows to guarantee 30h SLA with 24h batch).
- **Multi-instance / multi-pass review:** self-review is weak (retains generation reasoning); use an **independent instance**. Split large reviews into per-file local passes + cross-file integration pass. Verification passes where the model self-reports confidence enable calibrated routing.

### Domain 5 — Context Management & Reliability (15%)

- **Long conversations:** progressive summarization risks condensing numerical values/percentages/dates/expectations into vague text. **"Lost in the middle"** — models reliably use beginning + end of long inputs but may omit middle sections. Tool results accumulate and consume tokens disproportionately (40+ fields when 5 matter). Pass complete conversation history in subsequent requests for coherence.
  - Fixes: extract transactional facts (amounts, dates, order #s, statuses) into a persistent **"case facts" block** included in each prompt, outside summarized history; trim verbose tool outputs to relevant fields before they accumulate; put key-findings summaries at the **start** of aggregated inputs + use section headers to mitigate position effects.
- **Escalation/ambiguity:** escalate on explicit human request, policy exceptions/gaps (not just "complex"), or inability to make progress. Honor explicit human requests **immediately** (don't investigate first). Sentiment/self-reported confidence are unreliable proxies for complexity. Multiple customer matches → **ask for additional identifiers**, don't pick heuristically. Escalate when policy is silent on the request (competitor price-match when policy only covers own-site).
- **Error propagation (multi-agent):** structured error context (failure type, attempted query, partial results, alternatives) enables coordinator recovery. Distinguish access failures (retry decisions) from valid empty results. Generic statuses ("search unavailable") hide context. Silently suppressing errors (empty-as-success) OR terminating the whole workflow on one failure = both anti-patterns. Subagents recover locally for transient failures; propagate only the unrecoverable + what was attempted + partial results. Annotate synthesis with coverage (which findings are well-supported vs which areas have gaps).
- **Large codebase context:** context degrades in long sessions (model references "typical patterns" instead of specific classes found earlier). Use **scratchpad files** to persist key findings across context boundaries; **subagent delegation** isolates verbose exploration while the main agent coordinates; structured **state exports/manifests** for crash recovery (coordinator loads manifest on resume); summarize a phase before spawning next-phase subagents; **`/compact`** reduces context usage in extended sessions.
- **Human review & confidence calibration:** aggregate accuracy (97%) can mask poor performance on specific doc types/fields. Use **stratified random sampling** to measure error rates + detect novel patterns. Field-level confidence scores calibrated with **labeled validation sets** route review attention. Validate accuracy by doc type AND field segment before automating high-confidence extractions. Route low-confidence/ambiguous to humans.
- **Provenance / multi-source synthesis:** attribution is lost when summarization compresses without preserving claim→source mappings. Require structured claim-source mappings (URLs, doc names, excerpts) preserved through synthesis. Conflicting stats from credible sources → **annotate the conflict with attribution**, don't arbitrarily pick one. Require publication/collection **dates** so temporal differences aren't misread as contradictions. Render content types appropriately (financial=tables, news=prose, technical=lists), don't force a uniform format. Structure reports to distinguish well-established from contested findings.

---

## 4. Pure factual recall (easy points — don't fumble these)

**CLI / Claude Code:**
- `claude -p` / `claude --print` — non-interactive/headless (CI). ← *the* CI answer
- `--output-format json`, `--json-schema` — structured CI output
- `--resume <session-name>` — resume named session
- `/memory` — see loaded memory files; `/compact` — reduce context
- Locations: project `.claude/commands/`, `.claude/skills/`, `.claude/rules/`, `.claude/CLAUDE.md` / root `CLAUDE.md`, `.mcp.json` (all VCS-shared) vs user `~/.claude/...` and `~/.claude.json` (personal)
- SKILL.md frontmatter: `context: fork`, `allowed-tools`, `argument-hint`
- `.claude/rules/` frontmatter: `paths: ["glob"]`
- `@import` in CLAUDE.md

**Agent SDK / API:**
- `stop_reason`: `"tool_use"` (loop) vs `"end_turn"` (done)
- `Task` tool spawns subagents; `allowedTools` must include `"Task"`
- `AgentDefinition`: description, system prompt, tool restrictions
- `fork_session`
- Hooks: `PostToolUse` (transform results / intercept calls)
- `tool_choice`: `"auto"` | `"any"` | `{"type":"tool","name":"..."}`

**MCP:**
- `isError` flag; structured error: `errorCategory`, `isRetryable`/`retriable: false`
- `.mcp.json` + `${ENV_VAR}` expansion
- MCP resources = content catalogs

**Message Batches API:** 50% cheaper · up to 24h · no SLA · no multi-turn tool calling · `custom_id` correlation

**Structured output:** `tool_use` + JSON schema (kills syntax errors, not semantic) · enum + `"other"` + detail · nullable fields prevent fabrication

---

## 5. Out-of-scope — DO NOT study (save time)

Fine-tuning/training custom models · API auth/billing/account mgmt · OAuth/key rotation · deep language/framework impl · deploying/hosting MCP servers (infra/networking/containers) · Claude's internal architecture/training/weights · Constitutional AI/RLHF/safety training · embeddings/vector DB impl · computer use / browser automation · vision/image analysis · streaming/SSE impl · rate limits/quotas/pricing math · cloud provider configs (AWS/GCP/Azure) · perf benchmarking/model comparison · prompt-caching impl details (beyond "it exists") · tokenization specifics.

---

## 6. Distractor traps (the wrong answers they love)

- **Prompt instruction** offered as a fix where a **deterministic mechanism** (hook/prereq gate) is required → wrong when correctness must be guaranteed.
- **LLM self-reported confidence** / **sentiment analysis** as a routing signal → wrong (poorly calibrated / doesn't track complexity).
- **Training a separate classifier / ML model** → usually over-engineered vs prompt fixes.
- **Bigger context window / higher-tier model** to fix attention dilution → wrong; restructure into passes instead.
- **Consensus of N runs, flag only if ≥2 agree** → wrong; suppresses real intermittently-caught bugs.
- **Fictional flags/configs:** `CLAUDE_HEADLESS=true`, `--batch`, `.claude/config.json` with a `commands` array → don't exist.
- **Generic error status** / **empty-result-as-success** / **terminate whole workflow** → all anti-patterns.
- **Blaming a downstream subagent** that worked correctly within its scope → look upstream at the coordinator.
- **Adding more tools / a generic mega-tool** → degrades selection; prefer scoped, well-described tools.
- **"Switch to plan mode later if it gets complex"** → wrong when complexity is already known; plan now.
- **Over-engineering a "first step"** (routing layer when descriptions are just thin) → prefer the proportionate root-cause fix.
