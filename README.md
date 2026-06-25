# Claude Certified Architect — Foundations: Study Kit

An open, self-contained study kit for the **Claude Certified Architect – Foundations** exam: a condensed high-yield study guide, a 60-question practice exam, and a full answer key with explanations.

> **Unofficial.** Not affiliated with, authorized, or endorsed by Anthropic. "Claude" and the certification name belong to Anthropic and are used here only to identify the exam this kit prepares for. These materials are **original work**, synthesized from the *publicly described* structure of Anthropic's official exam guide (domains, task statements, scenarios, and sample-question style). The official exam guide is Anthropic's copyrighted material and is **not redistributed here** — get it from the official source (below). The practice questions are **calibrated approximations, not real exam items**; there is no guarantee they match what you'll see. No exam dumps.

---

## What this exam is

The Claude Certified Architect – Foundations cert validates **tradeoff judgment** for building real-world Claude solutions across **Claude Code, the Claude Agent SDK, the Claude API, and MCP**. It is aimed at solution architects with ~6+ months of hands-on experience across that stack.

| Fact | Detail |
|---|---|
| Format | 100% multiple choice (1 correct answer + 3 distractors) — pick the single best answer |
| Scoring | Scaled 100–1,000; **pass = 720**; pass/fail; **no penalty for guessing** (answer everything) |
| Scenarios | 6 defined; **4 presented at random** per sitting |
| Length | ~60 questions / 120 minutes *(third-party figure — approximate, not from the official guide)* |

**Domain weights** (what to study most):

| Domain | Weight |
|---|---|
| D1 — Agentic Architecture & Orchestration | **27%** |
| D3 — Claude Code Configuration & Workflows | 20% |
| D4 — Prompt Engineering & Structured Output | 20% |
| D2 — Tool Design & MCP Integration | 18% |
| D5 — Context Management & Reliability | 15% |

---

## What's in here

The exam tests judgment, not trivia. The core insight behind this kit: the same ~12 decision patterns generate most of the answers. The materials are layered so you learn the rules first, then drill them.

| File | What it is | Start order |
|---|---|---|
| [`study-guide.md`](study-guide.md) | The high-yield doc. **§2 "The 12 Decision Heuristics" is the crux of the exam** — the recurring tradeoffs every answer turns on. Plus per-domain cheat sheets, factual recall (CLI flags, file paths, config keys), out-of-scope list, and common distractor traps. | **1 — read first** |
| [`practice-exam.md`](practice-exam.md) | 60 scenario-based questions, organized under the 6 official scenarios, each tagged with its domain and weighted to approximate the real exam. No answers inline. | **2 — take timed** |
| [`practice-exam-answers.md`](practice-exam-answers.md) | Answer key: correct letter + concise explanation per question, each citing the heuristic it tests. | **3 — grade & review** |

### How the materials relate

```
Anthropic's official exam guide  (the source — NOT included; link below)
        │  (its task statements + sample questions describe what's tested)
        ▼
study-guide.md     →  distilled rules: the 12 heuristics + cheat sheets + recall
        │
        ▼
practice-exam.md   →  60 fresh questions drilling those same task statements,
practice-exam-answers.md   in the official sample-question style
```

The study guide is **not** a copy of the official guide — its value-add is the compression into 12 reusable decision rules. The practice exam is **not** a copy of the official sample questions — they're newly written to the same style and difficulty. Because everything derives from one public source, these can't surface anything the official guide doesn't already imply; the only true preview is Anthropic's own (gated) practice exam.

---

## How to use this kit

A focused path, ~4–5 hours if you already build with this stack:

1. **Read `study-guide.md` §2** (the 12 heuristics) until you can recall them cold — this is the whole exam in one page. *(~30 min)*
2. **Skim the per-domain cheat sheets (§3) + factual recall (§4).** *(~30 min)*
3. **Take `practice-exam.md` timed** (~2 hours, no notes). *(~2 hrs)*
4. **Grade with `practice-exam-answers.md`.** Re-read the study-guide section for any domain you missed. *(~1 hr)*
5. **Target ≥ 48/60 (80%)** on the practice set before booking. Re-skim the 12 heuristics + the distractor-traps list the morning of.

---

## Official exam guide & registration

The authoritative source — and the official practice exam — come from Anthropic's certification portal. Get the official exam guide, confirm logistics (cost, scheduling, proctoring, retake policy, validity), and register here:

- **Anthropic certification (Skilljar):** https://anthropic.skilljar.com/claude-certified-architect-foundations-access-request *(may require an access request / sign-in)*

Always defer to the official guide where it differs from anything here.

---

## Use & attribution

The original study materials in this repo are free to use and share for studying. Attribution appreciated. If you spot an error or have a better explanation, open an issue or PR.

Built with [Claude Code](https://claude.com/claude-code).
