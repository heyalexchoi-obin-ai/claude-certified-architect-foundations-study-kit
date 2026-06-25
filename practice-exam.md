# CCA-Foundations — Synthesized Practice Exam (60 questions)

> **Not the official practice exam** (that one is gated behind the access request). These are synthesized to match the official guide's scenario-based format, difficulty, and distractor philosophy — 1 correct answer + 3 plausible distractors that someone with incomplete knowledge would pick.
>
> **How to use:** Answer all 60 (no penalty for guessing on the real exam — answer everything). Time-box to ~120 min for a realistic run. Then grade with `practice-exam-answers.md`. Target ≥ 80% before sitting the real exam (passing is 720/1000 scaled).
>
> **Domain coverage** (≈ matches real weighting): D1 Agentic Architecture (heaviest) · D2 Tool/MCP · D3 Claude Code · D4 Prompt/Structured Output · D5 Context/Reliability. Each question is tagged `[D#]`.

---

## Scenario 1 — Customer Support Resolution Agent
*Agent SDK; tools `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`. Target 80%+ first-contact resolution, escalate appropriately.*

**Q1. [D1]** Your agentic loop occasionally stops mid-task, leaving refunds half-processed. Reviewing the code, the loop terminates as soon as the assistant message contains the phrase "I'll take care of that." What is the correct loop-termination condition?

- A) Continue while `stop_reason` is `"tool_use"`; terminate when `stop_reason` is `"end_turn"`.
- B) Continue until the assistant's text no longer contains action phrases like "I'll" or "let me."
- C) Set a fixed cap of 10 iterations and terminate when it is reached.
- D) Terminate when the most recent tool returns a success status code.

**Q2. [D1]** Production data shows that in 9% of refund cases the agent calls `process_refund` before ever calling `get_customer`, occasionally refunding the wrong account. The business requires that identity is always verified before any refund. What most reliably enforces this?

- A) Add a sentence to the system prompt: "Always verify the customer with `get_customer` before processing refunds."
- B) Add a programmatic prerequisite gate that blocks `process_refund` until `get_customer` has returned a verified customer ID.
- C) Add three few-shot examples showing `get_customer` being called before `process_refund`.
- D) Lower the model temperature so the agent follows instructions more deterministically.

**Q3. [D2]** Logs show the agent frequently calls `get_customer` when users ask about orders (e.g., "where's order #12345?"). Both `get_customer` ("Retrieves customer information") and `lookup_order` ("Retrieves order details") have minimal descriptions. What is the most effective first step?

- A) Add 6–8 few-shot examples to the system prompt showing order queries routing to `lookup_order`.
- B) Expand each tool's description to specify input formats, example queries, edge cases, and when to use it versus the similar tool.
- C) Implement a keyword router that pre-selects the tool before the model sees the request.
- D) Merge both into one `lookup_entity` tool that accepts any identifier and decides internally.

**Q4. [D1]** Compliance requires that no single refund exceed $500 without human approval. The agent is otherwise reliable. What is the most appropriate mechanism?

- A) Instruct the agent in the system prompt to escalate any refund over $500.
- B) A tool-call interception hook that blocks `process_refund` calls above $500 and redirects them to the escalation workflow.
- C) A few-shot example showing the agent escalating a $600 refund.
- D) Set `tool_choice: "any"` so the model is forced to consider escalation.

**Q5. [D1]** A single customer message says: "My order arrived damaged, I was double-charged, and I want to update my email." What is the best way for the agent to handle this?

- A) Escalate immediately to a human because the request has multiple concerns.
- B) Handle only the first concern and ask the customer to open separate tickets for the others.
- C) Decompose the message into distinct items, investigate each (in parallel where possible) using shared context, then synthesize a unified resolution.
- D) Pick the highest-priority concern (the double-charge) and address only that.

**Q6. [D5]** Your support policy covers price adjustments for items discounted on your own site, but is silent on matching a competitor's price. A customer asks for a competitor price match. What should the agent do?

- A) Decline, since the policy does not authorize it.
- B) Approve it, since price matching is generally customer-friendly.
- C) Escalate to a human, because the policy is silent (a policy gap) on this specific request.
- D) Apply the closest matching policy (own-site adjustment) and grant a partial credit.

**Q7. [D5]** Over a long multi-turn conversation, the agent starts losing track of the exact refund amount and order number it confirmed earlier, because history is being progressively summarized. What is the best fix?

- A) Increase `max_tokens` so the full history always fits.
- B) Extract transactional facts (amounts, dates, order numbers, statuses) into a persistent "case facts" block included in each prompt, separate from summarized history.
- C) Disable summarization and always send the entire raw transcript.
- D) Ask the customer to re-state the order number each turn.

**Q8. [D2]** `process_refund` can fail for several reasons: the payment processor times out, the refund violates a business rule, or the input is malformed. Currently it returns "Operation failed" for all of them. Why is this a problem, and what should it return?

- A) It's fine; the agent should retry any failure automatically.
- B) Uniform errors prevent appropriate recovery; return structured metadata with `errorCategory` (transient/validation/business/permission), an `isRetryable` boolean, and a human-readable description.
- C) It should always raise an exception so the loop terminates safely.
- D) It should return an empty success so the conversation continues smoothly.

**Q9. [D5]** A customer provides only a common name ("John Smith"), and `get_customer` returns three matching accounts. What should the agent do?

- A) Select the most recently active account and proceed.
- B) Process against all three accounts to be safe.
- C) Ask the customer for an additional identifier (email, order number, or account ID) to disambiguate.
- D) Escalate to a human immediately.

**Q10. [D1]** When the agent escalates to `escalate_to_human`, the human agent has no access to the conversation transcript. What should the handoff include?

- A) Just the customer's last message, so the human can start fresh.
- B) A link to the full raw transcript for the human to read.
- C) A structured summary: customer ID, root cause, refund amount, and recommended action.
- D) Only the customer ID; the human will look up the rest.

---

## Scenario 2 — Code Generation with Claude Code
*Team uses Claude Code for generation, refactoring, debugging, docs; custom slash commands, CLAUDE.md, plan vs direct.*

**Q11. [D3]** You want a `/review` slash command running your team's review checklist, available to every developer automatically when they clone the repo. Where should it live?

- A) `.claude/commands/` in the project repository.
- B) `~/.claude/commands/` in each developer's home directory.
- C) The root `CLAUDE.md` file.
- D) A `.claude/config.json` file with a `commands` array.

**Q12. [D3]** A new team member reports Claude Code isn't following the team's documented conventions, while everyone else's setup works. You suspect a configuration-hierarchy issue. What is the most likely cause?

- A) The conventions were placed in user-level `~/.claude/CLAUDE.md` (not shared via version control) instead of project-level config.
- B) The new member needs to run `/compact` to load the conventions.
- C) The project `CLAUDE.md` is too long and is being truncated.
- D) The conventions must be re-stated in every prompt.

**Q13. [D3]** You're assigned to restructure a monolith into microservices — dozens of files, decisions about service boundaries and dependencies. Which approach fits best?

- A) Enter plan mode to explore the codebase, understand dependencies, and design the approach before changing anything.
- B) Start direct execution and let the implementation reveal natural service boundaries.
- C) Use direct execution with comprehensive upfront instructions specifying each service's structure.
- D) Begin in direct execution and switch to plan mode only if unexpected complexity appears.

**Q14. [D3]** Your codebase has tests spread throughout, alongside the code they test (`Button.test.tsx` next to `Button.tsx`). You want Claude to apply your testing conventions automatically whenever it edits any test file, regardless of directory. What's the most maintainable approach?

- A) A `.claude/rules/` file with YAML frontmatter `paths: ["**/*.test.tsx"]` containing the testing conventions.
- B) Put all conventions in the root `CLAUDE.md` under a "Testing" header and rely on Claude to infer when it applies.
- C) Place a `CLAUDE.md` in every directory that contains test files.
- D) Create a `/test-conventions` slash command developers run before writing tests.

**Q15. [D3]** Your `/analyze-architecture` skill produces a large volume of exploratory output that clutters the main conversation and pushes out relevant context. Which frontmatter option addresses this?

- A) `context: fork` — run the skill in an isolated sub-agent context so its output doesn't pollute the main conversation.
- B) `allowed-tools: Read` — restrict it to read-only.
- C) `argument-hint` — prompt for parameters.
- D) `model: opus` — give it a bigger context window.

**Q16. [D3]** Your root `CLAUDE.md` has grown to cover testing, API conventions, and deployment for many packages, and it's becoming unwieldy. Each package's maintainer knows which standards apply. What's the cleanest way to keep it modular?

- A) Use `@import` to reference external standards files, and/or split topics into focused files under `.claude/rules/`.
- B) Delete the rarely-used sections to keep it short.
- C) Move everything into a single skill so it's only loaded on demand.
- D) Duplicate the full CLAUDE.md into each subdirectory.

**Q17. [D5]** During a long debugging session, Claude starts giving inconsistent answers and referencing "typical patterns" rather than the specific classes it identified earlier. What helps most?

- A) Restart the session from scratch every 20 minutes regardless of state.
- B) Have Claude maintain a scratchpad file recording key findings and reference it for later questions; use `/compact` when context fills with verbose discovery output.
- C) Increase the temperature so answers are more varied.
- D) Paste the entire codebase into the prompt at the start.

**Q18. [D3]** You're building a `/deploy-check` skill that should only ever read files and run read-only validation — never modify anything — and you want it to prompt the developer for the target environment if they don't supply one. Which frontmatter combination fits?

- A) `allowed-tools` restricted to read/validation tools, plus `argument-hint` for the environment parameter.
- B) `context: fork` plus `model: haiku`.
- C) `paths: ["deploy/**/*"]` plus `@import`.
- D) `tool_choice: "any"` plus `argument-hint`.

**Q19. [D5]** You return to a refactoring task the next day. Several files have changed substantially since your last session, and the prior session's tool results are now stale. What's the most reliable way to continue?

- A) Resume the old session with `--resume`; the cached tool results are good enough.
- B) Start a fresh session with a structured summary of the current state, rather than resuming with stale tool results.
- C) Fork the old session and hope the changes don't matter.
- D) Re-run every tool call from the old session in order.

**Q20. [D3]** You need to plan a library migration affecting ~45 files and then carry it out. What's the best combination of modes?

- A) Use plan mode to investigate and design the migration, then direct execution to implement the planned approach.
- B) Use direct execution throughout; plan mode is only for documentation.
- C) Use plan mode for both the planning and the file edits.
- D) Skip planning and rely on the Explore subagent to make the edits.

---

## Scenario 3 — Multi-Agent Research System
*Coordinator delegates to subagents: web search, document analysis, synthesis, report generation. Produces comprehensive, cited reports.*

**Q21. [D1]** You research "impact of AI on creative industries." Every subagent succeeds — web search finds articles, doc analysis summarizes correctly, synthesis is coherent — but the report covers only visual arts, missing music, writing, and film. The coordinator's logs show it decomposed the topic into "AI in digital art," "AI in graphic design," and "AI in photography." Most likely root cause?

- A) The synthesis agent lacks instructions to identify coverage gaps.
- B) The coordinator's task decomposition is too narrow, producing subagent assignments that don't cover all relevant domains of the topic.
- C) The web search agent's queries aren't comprehensive enough.
- D) The document analysis agent is filtering out non-visual sources.

**Q22. [D1]** Your synthesis subagent produces reports missing details that the web-search subagent clearly found. You assumed the synthesis agent could see the search agent's results. What's the issue?

- A) Subagents share memory by default, so something corrupted it.
- B) Subagents operate with isolated context and do NOT inherit other agents' results; the search findings must be passed explicitly in the synthesis agent's prompt.
- C) The coordinator must increase `max_tokens` on the synthesis agent.
- D) The synthesis agent needs the web search tool to re-fetch everything.

**Q23. [D1]** Your coordinator runs three independent subagents one after another, and total latency is high. The subagents don't depend on each other's output. How do you run them in parallel?

- A) Emit multiple `Task` tool calls in a single coordinator response.
- B) Spawn each subagent in a separate conversation turn, one per turn.
- C) Set `tool_choice: "any"` to parallelize automatically.
- D) Increase the iteration cap so the loop runs faster.

**Q24. [D5]** The web-search subagent times out on a complex topic. You're designing how that failure flows back to the coordinator to enable intelligent recovery. Best approach?

- A) Return structured error context: failure type, the attempted query, any partial results, and potential alternative approaches.
- B) Retry with backoff inside the subagent and, after exhausting retries, return a generic "search unavailable" status.
- C) Catch the timeout and return an empty result set marked successful.
- D) Propagate the timeout up so a top-level handler terminates the entire research workflow.

**Q25. [D2]** The synthesis agent frequently needs simple fact-checks (dates, names, statistics) while combining findings. Currently it routes every verification back through the coordinator to the web-search agent — adding 2–3 round trips and 40% latency. 85% of these are simple lookups; 15% need deeper investigation. Best fix?

- A) Give the synthesis agent a scoped `verify_fact` tool for simple lookups, while complex verifications continue routing through the coordinator.
- B) Give the synthesis agent access to all web-search tools so it can handle any verification directly.
- C) Have the synthesis agent batch all verification needs and send them to the web-search agent at the end of its pass.
- D) Have the web-search agent speculatively cache extra context around every source during initial research.

**Q26. [D5]** During synthesis, source attribution is being lost — the final report makes claims without traceable sources because intermediate summarization compressed the findings. How do you preserve provenance?

- A) Add a disclaimer that sources may be approximate.
- B) Require subagents to output structured claim-source mappings (URLs, document names, relevant excerpts) that downstream agents preserve through synthesis.
- C) Have the report agent re-search every claim at the end.
- D) Increase the synthesis agent's context window.

**Q27. [D1]** Some research queries are simple and others are broad and multi-faceted. Routing every query through the full four-subagent pipeline wastes time on simple ones. What's the better coordinator design?

- A) Always run the full pipeline for consistency.
- B) Design the coordinator to analyze query requirements and dynamically select which subagents to invoke based on complexity.
- C) Hard-code a fixed sequence and add an iteration cap.
- D) Let each subagent decide whether to run itself.

**Q28. [D5]** Two credible sources report different market-size statistics for the same sector, and one is from 2021 while the other is from 2023. How should the synthesis handle this?

- A) Average the two values.
- B) Pick the value from the more authoritative source and discard the other.
- C) Annotate the conflict with source attribution and include publication/collection dates so the temporal difference isn't misread as a contradiction.
- D) Omit the statistic entirely to avoid confusion.

**Q29. [D1]** The coordinator's first synthesis pass reveals that one subtopic is thinly covered. What's the best pattern to improve coverage?

- A) Accept the gap and note it; re-running is too expensive.
- B) Implement an iterative refinement loop: the coordinator evaluates synthesis output for gaps, re-delegates to search/analysis agents with targeted queries, and re-invokes synthesis until coverage is sufficient.
- C) Tell the synthesis agent to make up plausible content for the thin subtopic.
- D) Restart the whole research run from scratch.

**Q30. [D2]** A document-analysis subagent hits a transient parse error on one of ten documents. How should it behave?

- A) Terminate the entire research workflow.
- B) Attempt local recovery for the transient failure; if unrecoverable, propagate only that error to the coordinator along with partial results and what was attempted.
- C) Return all ten documents as failed to be safe.
- D) Silently drop the document and report success on the other nine.

---

## Scenario 4 — Developer Productivity Tools
*Agent explores unfamiliar codebases, understands legacy systems, generates boilerplate, automates tasks. Built-in tools (Read, Write, Edit, Bash, Grep, Glob) + MCP servers.*

**Q31. [D2]** The agent needs to find every place a function `processPayment` is called across a large codebase. Which built-in tool is the right choice?

- A) Grep — search file contents for the pattern.
- B) Glob — match file path/name patterns.
- C) Read — open every file and scan it.
- D) Bash — write a custom traversal script.

**Q32. [D2]** The agent tries to use Edit to change a line, but the target text appears multiple times in the file, so Edit fails on the non-unique match. What's the reliable fallback?

- A) Read the full file, then Write it back with the modification.
- B) Lower the agent's temperature and retry Edit.
- C) Delete the file and recreate it from memory.
- D) Use Glob to find a unique version of the file.

**Q33. [D2]** Your team wants a shared MCP server (with a credential) available to everyone on the project, while you personally want to experiment with another MCP server that teammates shouldn't get. How do you configure these?

- A) Shared server in project `.mcp.json` (with `${ENV_VAR}` expansion for the credential); personal server in user-level `~/.claude.json`.
- B) Both in `.mcp.json`, distinguished by a `personal: true` flag.
- C) Both in `~/.claude.json` since MCP is always user-scoped.
- D) Hard-code the credential in `.mcp.json` and commit it so everyone has access.

**Q34. [D2]** Your shared `.mcp.json` needs a GitHub token to authenticate an MCP server, but you must not commit the secret. What's the correct pattern?

- A) Use environment variable expansion, e.g. `${GITHUB_TOKEN}`, in `.mcp.json`.
- B) Commit the token but add `.mcp.json` to `.gitignore`.
- C) Paste the token into CLAUDE.md instead.
- D) Store the token in a comment in `.mcp.json`.

**Q35. [D1]** Faced with an unfamiliar 200k-line codebase, what's the most context-efficient way for the agent to build understanding?

- A) Read every file upfront to build a complete mental model.
- B) Start with Grep to find entry points, then use Read to follow imports and trace flows incrementally.
- C) Use Glob to list all files, then summarize filenames.
- D) Ask the user to paste the whole codebase into the prompt.

**Q36. [D2]** Your agent repeatedly makes exploratory tool calls just to discover what data exists (which issues, which docs, which DB tables). How can MCP reduce this overhead?

- A) Expose content catalogs (issue summaries, documentation hierarchies, database schemas) as MCP resources so the agent has visibility without exploratory tool calls.
- B) Increase the number of tools available to the agent.
- C) Cache every tool result in CLAUDE.md.
- D) Set `tool_choice: "any"` to force faster discovery.

**Q37. [D5]** During a multi-phase exploration of a large system, the main agent's context fills with verbose discovery output and answers degrade. What's the best mitigation?

- A) Delegate verbose exploration to subagents that return summaries, while the main agent preserves high-level coordination; have agents maintain scratchpad files for key findings.
- B) Increase temperature to keep answers fresh.
- C) Disable all tool output.
- D) Restart from scratch whenever answers degrade.

**Q38. [D2]** The agent misuses a generic `fetch_url` tool by passing it non-document URLs, causing failures. You want it to only operate on valid documents. What's the better tool design?

- A) Replace `fetch_url` with a constrained `load_document` tool that validates document URLs, with a description explaining its boundaries.
- B) Add a system-prompt warning not to pass bad URLs to `fetch_url`.
- C) Give the agent more URL tools so it has options.
- D) Remove all URL tools and have the agent guess content.

**Q39. [D1]** The task is open-ended: "add comprehensive tests to this legacy codebase." How should the agent decompose it?

- A) Generate one giant test file covering everything at once.
- B) First map the structure, identify high-impact areas, then create a prioritized plan that adapts as dependencies are discovered (dynamic decomposition).
- C) Use a fixed sequential pipeline that tests files alphabetically.
- D) Refuse until the user specifies every test case.

**Q40. [D2]** You need a standard Jira integration for your agent. There's a well-maintained community MCP server for Jira. What's the recommended approach?

- A) Use the existing community MCP server for the standard integration; reserve custom servers for team-specific workflows.
- B) Always build a custom MCP server so you control everything.
- C) Avoid MCP and call the Jira REST API via Bash.
- D) Use built-in tools only; MCP isn't needed for Jira.

---

## Scenario 5 — Claude Code for Continuous Integration
*Integrated into CI/CD: automated code reviews, test generation, PR feedback. Actionable feedback, minimal false positives.*

**Q41. [D3]** Your pipeline runs `claude "Analyze this pull request for security issues"` but the job hangs indefinitely, waiting for interactive input. Correct fix?

- A) Add the `-p` (`--print`) flag: `claude -p "Analyze this pull request for security issues"`.
- B) Set `CLAUDE_HEADLESS=true` before running.
- C) Redirect stdin from `/dev/null`.
- D) Add a `--batch` flag.

**Q42. [D3]** Your CI job needs Claude Code's review findings as machine-parseable output so it can post them as inline PR comments. Which flags do you use?

- A) `--output-format json` together with `--json-schema`.
- B) `--format pretty` and parse the text.
- C) `--comments` to post automatically.
- D) `--resume` with a session name.

**Q43. [D4]** Developers complain the automated reviewer flags too many false positives on comment-accuracy, eroding trust. The current instruction says "check that comments are accurate." How do you improve precision?

- A) Add "be conservative and only report high-confidence findings."
- B) Replace the vague instruction with explicit criteria: "flag a comment only when its claimed behavior contradicts the actual code behavior."
- C) Lower the temperature.
- D) Ask the model to double-check each finding twice.

**Q44. [D4]** A PR modifies 14 files. Your single-pass review (all files at once) gives detailed feedback on some files, superficial comments on others, misses obvious bugs, and even gives contradictory feedback. How should you restructure?

- A) Split into focused passes: analyze each file individually for local issues, then run a separate integration-focused pass examining cross-file data flow.
- B) Require developers to split large PRs into 3–4 file submissions.
- C) Switch to a higher-tier model with a larger context window for one big pass.
- D) Run three independent passes on the full PR and flag only issues appearing in ≥2 runs.

**Q45. [D4]** The same Claude session that generated a chunk of code is now reviewing it and missing subtle issues. Why, and what's better?

- A) The session is fine; just add "review carefully" to the prompt.
- B) A session retains its generation reasoning context, making it less likely to question its own decisions; use an independent review instance with no prior reasoning context.
- C) Enable extended thinking and re-review in the same session.
- D) Increase `max_tokens` so it can review more thoroughly.

**Q46. [D3]** After new commits, your reviewer re-runs and posts duplicate comments on issues it already flagged. How do you prevent this?

- A) Include prior review findings in context and instruct Claude to report only new or still-unaddressed issues.
- B) Delete all prior comments before each run.
- C) Run the review only once per PR, never on updates.
- D) Lower the temperature so it produces identical comments (which can be deduped).

**Q47. [D4]** Your reviewer's output format is inconsistent — sometimes it gives severity, sometimes not, sometimes suggests fixes, sometimes doesn't — making it hard to post structured comments. Detailed instructions haven't fixed it. What's most effective?

- A) Provide few-shot examples demonstrating the exact desired output format (location, issue, severity, suggested fix).
- B) Add "always be consistent" to the prompt.
- C) Switch models.
- D) Set `tool_choice: "auto"`.

**Q48. [D4]** Two CI workflows use real-time Claude calls: (1) a blocking pre-merge check where developers wait, and (2) an overnight technical-debt report. Your manager proposes moving BOTH to the Message Batches API for 50% savings. How do you evaluate this?

- A) Use batch processing for the overnight technical-debt report only; keep real-time (synchronous) calls for the blocking pre-merge check.
- B) Move both to batch with status polling.
- C) Keep both real-time to avoid batch result-ordering issues.
- D) Move both to batch with a timeout fallback to real-time.

**Q49. [D3]** Your CI-invoked test generation keeps producing low-value tests that duplicate existing coverage and ignore your team's fixtures and standards. How do you improve it?

- A) Document testing standards, valuable test criteria, and available fixtures in CLAUDE.md, and provide the existing test files in context so generation avoids duplicating coverage.
- B) Generate more tests so something useful slips through.
- C) Run test generation in batch mode.
- D) Use `tool_choice: "any"`.

**Q50. [D4]** One review category (style nitpicks) has a very high false-positive rate that's undermining developer trust in the accurate categories (bugs, security). What's a reasonable interim action?

- A) Temporarily disable the high-false-positive category while you improve its prompt, preserving trust in the accurate categories.
- B) Keep all categories on; developers should learn to ignore noise.
- C) Lower the confidence threshold across all categories.
- D) Merge all categories into one "issues" bucket.

---

## Scenario 6 — Structured Data Extraction
*Extracts info from unstructured documents, validates against JSON schemas, high accuracy, graceful edge-case handling, downstream integration.*

**Q51. [D4]** You need guaranteed schema-compliant JSON output and keep getting malformed JSON (trailing commas, unescaped quotes) when you ask the model to "respond in JSON." What's the most reliable approach?

- A) Define an extraction tool with a JSON schema and use tool use (`tool_use`) to get the structured output from the tool call.
- B) Add "make sure the JSON is valid" to the prompt.
- C) Post-process the text output with a regex JSON repair step.
- D) Lower temperature to 0.

**Q52. [D4]** Some source documents lack a "tax_id" field. With a required `tax_id` field, the model sometimes fabricates a plausible-looking value. How do you design the schema to prevent this?

- A) Make `tax_id` an optional/nullable field so the model returns null when the source doesn't contain it.
- B) Keep it required and add "don't make up values" to the prompt.
- C) Default `tax_id` to an empty string in post-processing.
- D) Set `tool_choice: "auto"`.

**Q53. [D4]** Your "document_type" field must handle a known set of categories but also gracefully accommodate new, unforeseen types. What's the best schema design?

- A) An enum of known categories plus an `"other"` value paired with a free-text detail field for extensible categorization.
- B) A single free-text string field.
- C) A required enum with no escape value (fail if unknown).
- D) A boolean per category.

**Q54. [D4]** Schema validation fails on an extraction because a value landed in the wrong field. What's the most effective retry strategy?

- A) Send a follow-up request that includes the original document, the failed extraction, and the specific validation error to guide correction.
- B) Retry the identical request unchanged a few times.
- C) Lower the temperature and retry the same prompt.
- D) Skip the document and log it as unprocessable.

**Q55. [D5]** Extraction of "contract_end_date" keeps failing validation. On inspection, the date simply isn't present in the source documents. Will retry-with-feedback help?

- A) Yes — more retries eventually surface the value.
- B) No — retries don't help when the required information is absent from the source (vs format/structural errors, which retries can fix); route to a different source or human, or make the field nullable.
- C) Yes — if you raise the temperature on each retry.
- D) Yes — if you add more few-shot examples.

**Q56. [D4]** You have several extraction schemas and, for a given document, you're not sure which applies, but you want to guarantee the model calls one of them (not return prose). What `tool_choice` setting?

- A) `"any"` — the model must call a tool but can choose which.
- B) `"auto"` — the model may return text instead.
- C) A forced specific tool `{"type":"tool","name":"..."}` — always the same one.
- D) No `tool_choice` setting is needed.

**Q57. [D5]** You want to route only genuinely uncertain extractions to human reviewers, who have limited capacity. How do you calibrate this?

- A) Have the model output field-level confidence scores and calibrate review thresholds using a labeled validation set; route low-confidence/ambiguous cases to humans.
- B) Send a fixed 10% of all extractions to humans at random.
- C) Send everything to humans to be safe.
- D) Trust the model's self-reported "I'm confident" statements directly.

**Q58. [D5]** Your extraction system reports 97% aggregate accuracy, and you're tempted to drop human review. What's the risk and the right check?

- A) No risk — 97% is high enough; drop review.
- B) Aggregate accuracy can mask poor performance on specific document types or fields; analyze accuracy by document type and field segment (and use stratified random sampling for ongoing error measurement) before reducing review.
- C) The only risk is latency; just speed it up.
- D) Re-train the model on the 3% errors.

**Q59. [D4]** Tool use with a strict JSON schema eliminated your JSON syntax errors, but you still get invoices where the line items don't sum to the stated total. What does this tell you, and how do you catch it?

- A) Strict schemas guarantee correctness; this must be a parsing bug.
- B) Schemas eliminate syntax errors but NOT semantic errors; extract `calculated_total` alongside `stated_total` and flag discrepancies (or add a `conflict_detected` boolean).
- C) Increase `max_tokens`.
- D) Switch `tool_choice` to `"auto"`.

**Q60. [D4]** You batch-process 100 documents via the Message Batches API. Eight fail because they exceeded the context limit. How do you handle the failures efficiently?

- A) Resubmit only the failed documents (identified by `custom_id`) with modifications such as chunking the oversized ones.
- B) Resubmit the entire batch of 100.
- C) Switch the whole pipeline to synchronous calls.
- D) Discard the 8 failures and accept 92% coverage.

---

*End of 60 questions. Grade with `practice-exam-answers.md`.*
