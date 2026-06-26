#!/usr/bin/env python3
"""
Build the standalone practice-exam web app (index.html) from the Markdown
source of truth.

It parses:
  - practice-exam.md          (questions, options, domain tags, scenarios)
  - practice-exam-answers.md  (correct letter + explanation per question)

and injects the joined data into tools/exam.template.html, writing index.html
at the repo root. The end user just opens index.html — no build step needed
for them. Run this only when the questions/answers/UI change:

    python3 tools/build_exam.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAM_MD = ROOT / "practice-exam.md"
ANS_MD = ROOT / "practice-exam-answers.md"
TEMPLATE = ROOT / "tools" / "exam.template.html"
OUT = ROOT / "index.html"

DASH = r"[—–-]"  # em-dash / en-dash / hyphen
SCEN_RE = re.compile(r"^##\s*Scenario\s*(\d+)\s*" + DASH + r"\s*(.+?)\s*$")
Q_RE = re.compile(r"^\*\*Q(\d+)\.\s*\[(D\d)\]\*\*\s*(.+?)\s*$")
OPT_RE = re.compile(r"^-\s*([A-D])\)\s*(.+?)\s*$")
ANS_RE = re.compile(r"^\*\*Q(\d+)\s*" + DASH + r"\s*→?\s*([A-D])\.\*\*\s*(.+?)\s*$")
# the arrow in the answer key is "→" (U+2192); allow it explicitly:
ANS_RE = re.compile(r"^\*\*Q(\d+)\s*→\s*([A-D])\.\*\*\s*(.+?)\s*$")


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_questions(text):
    questions = {}
    cur = None
    scen_num = scen_title = None
    for line in text.splitlines():
        m = SCEN_RE.match(line)
        if m:
            scen_num, scen_title = int(m.group(1)), m.group(2).strip()
            continue
        m = Q_RE.match(line)
        if m:
            qid = int(m.group(1))
            if scen_num is None:
                fail(f"Q{qid} appears before any scenario header")
            questions[qid] = {
                "id": qid,
                "domain": m.group(2),
                "scenario": scen_num,
                "scenarioTitle": scen_title,
                "q": m.group(3).strip(),
                "options": {},
            }
            cur = qid
            continue
        m = OPT_RE.match(line)
        if m and cur is not None:
            questions[cur]["options"][m.group(1)] = m.group(2).strip()
    return questions


def parse_answers(text):
    answers = {}
    for line in text.splitlines():
        m = ANS_RE.match(line)
        if m:
            answers[int(m.group(1))] = (m.group(2), m.group(3).strip())
    return answers


def main():
    for p in (EXAM_MD, ANS_MD, TEMPLATE):
        if not p.exists():
            fail(f"missing {p}")

    questions = parse_questions(EXAM_MD.read_text(encoding="utf-8"))
    answers = parse_answers(ANS_MD.read_text(encoding="utf-8"))

    if not questions:
        fail("no questions parsed — check practice-exam.md format")

    # join + validate
    errs = []
    for qid, q in sorted(questions.items()):
        opts = q["options"]
        if sorted(opts) != ["A", "B", "C", "D"]:
            errs.append(f"Q{qid}: options {sorted(opts)} (expected A–D)")
        if qid not in answers:
            errs.append(f"Q{qid}: no answer found in answer key")
            continue
        letter, expl = answers[qid]
        if letter not in opts:
            errs.append(f"Q{qid}: answer {letter} not among options")
        if not expl:
            errs.append(f"Q{qid}: empty explanation")
        q["answer"] = letter
        q["explanation"] = expl

    orphan = sorted(set(answers) - set(questions))
    if orphan:
        errs.append(f"answer key has Qs with no question: {orphan}")

    if errs:
        fail("validation failed:\n  - " + "\n  - ".join(errs))

    data = [questions[qid] for qid in sorted(questions)]

    # report domain distribution
    dist = {}
    for q in data:
        dist[q["domain"]] = dist.get(q["domain"], 0) + 1
    print(f"Parsed {len(data)} questions.")
    for d in sorted(dist):
        print(f"  {d}: {dist[d]}")

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    template = TEMPLATE.read_text(encoding="utf-8")
    if "__QUESTIONS_JSON__" not in template:
        fail("template is missing the __QUESTIONS_JSON__ placeholder")
    html = template.replace("__QUESTIONS_JSON__", payload)
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT} ({len(html):,} bytes).")


if __name__ == "__main__":
    main()
