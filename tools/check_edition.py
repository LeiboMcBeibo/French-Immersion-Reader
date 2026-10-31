#!/usr/bin/env python3
"""Check a morning edition before it is saved to the repo.

Usage:  python3 tools/check_edition.py data/edition.json

Exits 0 when the edition is usable, 1 otherwise, and prints what to fix.
It checks:
  - required fields and types (label, date, level, generated_at, phrases,
    vocabularyWords, glossary)
  - every glossary entry has "english"
  - nearly every word in the phrases can be found in the glossary, the
    same way the Reader looks a tapped word up (exact form, then without
    an elided l'/d'/qu'... prefix)
It also reports word count and an estimated listening time.
"""
import json, re, sys, unicodedata

ELISION = re.compile(r"^(l|d|j|m|n|s|t|c|qu|jusqu|lorsqu|puisqu)'")
WORDS_PER_MINUTE = 95   # rough pace of the Reader's "Lent" speed plus pauses
MAX_MISSING_SHARE = 0.03


def norm(s):
    """Mirror of norm() in reader.html."""
    s = s.lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = s.replace("’", "'")
    s = re.sub(r"[^a-z0-9' ]", "", s)
    return s.strip()


def main(path):
    problems = []
    try:
        ed = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        print(f"FAIL: not valid JSON: {e}")
        return 1

    for key, typ in [("label", str), ("date", str), ("level", str), ("generated_at", str),
                     ("phrases", list), ("vocabularyWords", list), ("glossary", dict)]:
        if not isinstance(ed.get(key), typ):
            problems.append(f'missing or wrong type: "{key}" should be {typ.__name__}')
    if problems:
        print("FAIL:\n  " + "\n  ".join(problems))
        return 1

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", ed["date"]):
        problems.append('"date" must look like 2026-11-01')
    if not ed["phrases"] or not all(isinstance(p, str) and p.strip() for p in ed["phrases"]):
        problems.append('"phrases" must be a non-empty list of sentences')

    gloss = {}
    for k, v in ed["glossary"].items():
        if not isinstance(v, dict) or not v.get("english"):
            problems.append(f'glossary entry "{k}" has no "english"')
            continue
        gloss[norm(k)] = v

    tokens, missing = 0, {}
    for p in ed["phrases"]:
        for tok in p.split():
            t = norm(tok)
            if not t or t.isdigit():
                continue
            tokens += 1
            if t in gloss or ELISION.sub("", t) in gloss:
                continue
            missing[t] = missing.get(t, 0) + 1

    share = (sum(missing.values()) / tokens) if tokens else 1
    minutes = tokens / WORDS_PER_MINUTE
    print(f"{len(ed['phrases'])} phrases, {tokens} words (~{minutes:.0f} min), "
          f"{len(gloss)} glossary entries, {len(missing)} distinct words not in glossary ({share:.1%})")
    if missing:
        print("  not in glossary: " + ", ".join(sorted(missing)[:60]))
    if share > MAX_MISSING_SHARE:
        problems.append(f"too many words without a meaning ({share:.1%} > {MAX_MISSING_SHARE:.0%}); add them to the glossary")

    if problems:
        print("FAIL:\n  " + "\n  ".join(problems))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "data/edition.json"))
