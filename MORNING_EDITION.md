# Morning edition — instructions for the scheduled run

Each morning a scheduled Claude run writes Mark's French news edition, saves it to
this repo, and emails him the Reader link. Mark is the only reader. He uses the
Reader on his iPad; words he taps go to his Flashcards with the glossary meaning.

## 1. Read the settings

`data/settings.json`:
- `level` — CEFR level to write at (A1–C2). See the level guide below.
- `target_minutes` — listening length at the Reader's slow speed (~95 words/minute).
- `story_mix` — what kind of stories to choose.
- `special_request` — a one-off wish for the next edition (e.g. "a story about
  Africa"). If it is not empty, honor it, then set it back to `""` in the same commit.
- `email_to`, `reader_url` — where to send the morning email and what to link.

## 2. Find the stories

Search the web for today's news (use today's date in America/New_York). Follow
`story_mix`: mostly US stories Mark has likely already seen in English (that
familiarity is how he guesses meaning), plus one or two Paris/France stories he
would not see in US media. Prefer concrete, non-partisan stories; report facts
plainly and evenly. Avoid repeating the stories in the current `data/edition.json`
unless there is real news on them.

## 3. Write the edition at the level

| Level | How to write |
|---|---|
| A1 | Present tense almost only; very short sentences; ~500 most common words; heavy repetition; no idioms; bare facts. |
| A2 | Adds passé composé and futur proche; connectors (parce que, mais, donc); still concrete. |
| B1 | Imparfait vs passé composé; some subjunctive; relative clauses; some abstraction. |
| B2 | Full tense range incl. conditional and subjunctive; complex sentences; some idiom; near-journalistic. |
| C1 | Authentic journalistic register; nuance, idiom, varied syntax. |
| C2 | Native-level press French, as in Le Monde; dense and idiomatic. |

- One sentence per phrase (each phrase is read aloud and highlighted word by word).
- Open with a short greeting line and announce each story ("Maintenant, une nouvelle de Paris.").
- End with a short sign-off ("C'est la fin de ce résumé. À demain !").
- Length: about `target_minutes × 95` words in total.
- Use plain punctuation; write numbers people would say aloud in words when short.

## 4. Build the glossary (this is what makes tapped words useful)

`glossary` maps **every word form that appears in the phrases** (lowercase, as
written, including elided forms like `l'économie` — the Reader also tries the form
without `l'`, `d'`, `qu'`…) to:

```json
"montent": {"french": "monter", "english": "to rise; to go up", "level": "A1", "tag": "economy"}
```

- `french` = the dictionary form the flashcard should show (infinitive for verbs;
  noun with its article, e.g. `le prix`; adjective in the masculine singular).
- `english` = short, accurate meaning **as used in this sentence**.
- `level` = CEFR level of the word; `tag` = a one- or two-word topic.
- Cover every word, including small ones (le, de, est, et…), so any tap works.
  Proper names can map to themselves with english like "(name) Karoline Leavitt".

`vocabularyWords` = 8–12 words worth learning at this level; the Reader shows them
in red. Write each one exactly as it appears in a phrase (e.g. `citrouilles`,
`choisissent`), single words only, so the Reader can match it.

## 5. Save and check

Write `data/edition.json`:

```json
{
  "label": "Actualité américaine et parisienne • 1 novembre 2026 • Niveau A1",
  "date": "2026-11-01",
  "level": "A1",
  "generated_at": "2026-11-01T05:40:00-04:00",
  "vocabularyWords": ["..."],
  "phrases": ["...", "..."],
  "glossary": {"...": {"french": "...", "english": "...", "level": "...", "tag": "..."}}
}
```

Run `python3 tools/check_edition.py data/edition.json`. If it prints FAIL, fix the
edition (usually: add missing words to the glossary) and run it again until it prints OK.

Commit to `main` with the message `Morning edition YYYY-MM-DD (LEVEL)` and push.

## 6. Email Mark

Send **exactly one** email to `email_to` from Mark's Gmail. Before sending, search
Gmail for `subject:"Ton français du jour" newer_than:1d` and look at the subjects:
only an email whose subject has **today's** French date counts as already sent
(yesterday's will usually show up too). If today's is there, do not send another.
Call the send tool once; if its result is unclear, check with that same search
instead of sending again.
- Subject: `Ton français du jour — <date in French> (<level>)`
- Send it as HTML (`htmlBody`) with a plain-text `body` fallback. Mark reads it on
  his iPad, so the link must be obvious:
  1. A large tappable button at the top: `<a href="READER_URL">` styled as a blue
     button (padding 14px 24px, white bold text, rounded corners) reading
     "▶ Ouvrir le Reader — édition du jour".
  2. One line under it: "Le Reader s'ouvre directement sur les nouvelles d'aujourd'hui."
  3. A short list of the story titles in French.
  4. At the bottom, the full `reader_url` as a plain link, in case the button does
     not show.
  The plain-text `body` has the same content, with the URL on its own line.
  Nothing else.

If saving or pushing failed, send instead a short email saying the edition could
not be prepared today and why, so Mark knows to ask in the Claude app.
