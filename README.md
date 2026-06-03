# French Immersion Reader Scaffold

This is the permanent project scaffold.

## Permanent files

Do not redesign these during daily production:

- `index.html`
- `reader.html`
- `flashcards.html`

## Daily-changing file

Replace only this file when creating a new daily lesson:

- `data/today_news.js`

That file contains:

- metadata for the day
- the French sentence list
- optional vocabulary highlight words

## Vocabulary model

Vocabulary is now user-selected, not AI-selected.

In the Reader:

1. Press Pause.
2. Select/highlight a French word or short phrase.
3. Tap `Ajouter aux cartes`.

In Flashcards:

- User-added words appear automatically.
- `Edit meaning` lets you add or correct the English meaning.
- `Retire` hides a learned word from normal review.
- `Retired words` mode lets you restore retired words.

The user vocabulary is stored in the browser using `localStorage`. On iPad and iPhone, each browser/device may have its own saved vocabulary until cloud sync/export is added.

## GitHub Pages setup

Upload all files in this folder to a GitHub repository. Then enable GitHub Pages for the repository.

Typical repository structure:

```text
french-immersion-reader/
  index.html
  reader.html
  flashcards.html
  data/
    today_news.js
    base_vocabulary.js
  archive/
  masters/
```

## Daily production rule

Never regenerate the app.
Never change button labels, layout, swipe behavior, speech behavior, or visual design during daily news generation.
Only replace `data/today_news.js`.

## Acceptance checklist

Reader:

- Play starts speech.
- Pause stops speech.
- Repeat repeats current phrase.
- Previous/Next work.
- Previous/current/next phrase layout is preserved.
- Moving word highlight works when browser supports speech boundary events.
- Selecting text shows `Ajouter aux cartes`.

Flashcards:

- Card speaks French automatically when shown.
- `fr-FR` or another French voice is used.
- Tap flips card.
- Swipe left/right works.
- Important/Difficult work.
- Retire/Restore works.
- User-added words appear.

## Codex role

Codex should work on this folder as a software project. Its rule is:

> Preserve the scaffold. Modify only the daily content file unless explicitly asked to improve the app version.

