---
name: confirm-lesson
description: Confirm that a numbered lesson was actually taught and update the project's progress files for the English tutoring project at /Users/shaneorr/Documents/English. Updates Progress/coverage_tracker.md (grammar covered, interest rotation), Progress/vocabulary_log.md (master list + by-lesson block), and Progress/review_queue.md (per-objective review flags) for the named lesson. Trigger when Shane says "confirm lesson N", "confirm-lesson N", "we taught lesson N", "mark lesson N as taught", "update tracker for lesson N", "log lesson N", or any similar phrasing that signals a specific lesson is now done. The lesson number is required.
user-invocable: true
disable-model-invocation: true
---

# Confirm Lesson

Per-CLAUDE.md, `Progress/coverage_tracker.md`, `Progress/vocabulary_log.md`, and `Progress/review_queue.md` are updated **only after Shane confirms a lesson was taught**. This skill is that update step. It takes one parameter — the lesson number — and writes back to all three progress files.

`CLAUDE.md` at the project root is authoritative. Don't restate it; just follow it.

## Parameter

- **Lesson number** (required, e.g., `5`, `12`). Zero-pad internally to two digits when constructing folder/file paths (`Lesson_05`, `Lesson_12`).

If the user invokes the skill without a number, ask once via `AskUserQuestion`.

## Inputs to read first

Before writing anything, gather context from the lesson and the existing trackers:

- `CLAUDE.md` — authoritative brief (tracker columns, vocab-log conventions, never-update-preemptively rule).
- `Progress/coverage_tracker.md` — current state, including the running interest-rotation tally and any prior entries for this lesson number (in case of a re-confirmation).
- `Progress/vocabulary_log.md` — current master list and the `### Lesson NN` block (it may already say `_(not yet taught)_`).
- `Progress/review_queue.md` — current state. You'll need the rows with `Scheduled in Lesson` = NN (to mark them reviewed) and the full list of objectives this lesson covered (to ask the per-objective review question).
- `Progress/Lesson_Schedule.md` — the planned topic for lesson N. Useful as the default `Grammar / skill` label if the lesson plan is unambiguous.
- `Teacher Materials/Lesson_NN_teacher.pdf` — the teacher plan. Pull the lesson topic, learning objectives, and any vocabulary the plan called out.
- `Student Materials/Lesson_NN/Notes_<TOPIC>_SHARED.pdf` — the shared reference sheet (grammar point name, glossary if any).
- `Student Materials/Lesson_NN/Materials_Camilo.pdf` and `Materials_Luciana.pdf` — vocabulary boxes are the authoritative list of glossed words for the lesson, plus the `Source` for each.

If the lesson folder or teacher PDF is missing, stop and tell Shane — don't fabricate a topic.

To extract text from the PDFs, invoke the `pdf` skill (read mode). Vocabulary boxes inside the per-kid PDFs typically render as a small table; pull the EN word, the ES-LatAm translation, and the part of speech if present.

## Information to gather from Shane

After reading the lesson materials, ask Shane for the following in a **single** `AskUserQuestion` call. Keep it short — he runs the lesson, so this is the only thing he needs to type:

1. **Date taught** (default to today). Convert any relative wording ("yesterday", "Friday") to an absolute date.
2. **Interest-rotation tag** for the shared materials in this lesson — one of `L` / `C` / `S` / `B` (Luciana-leaning / Camilo-leaning / genuinely shared / blended). Default: read it off the lesson contents and propose a tag, let Shane override.

If the user invocation already supplied any of these (e.g., "confirm lesson 5, taught today"), don't re-ask — fill them in and only ask for what's missing.

**Do not ask Shane about how the lesson went, what stuck, what didn't, per-kid status, or pacing changes in free text.** The only structured outcome signal this skill captures is the per-objective review check below — a yes/no per learning objective, not split by kid, no free-text reasoning.

## Per-objective review check

After the date and rotation question, run a second `AskUserQuestion` call covering the lesson's **learning objectives**. Extract the objectives from `Teacher Materials/Lesson_NN_teacher.pdf` (the teacher plan lists 2–4 measurable learning objectives in its header section). Ask one question per objective — one `AskUserQuestion` call with multiple `questions` entries.

- Question phrasing: `Does "<objective>" need review?`
- Options: exactly `Yes` and `No`. Use these literal labels so parsing is deterministic.
- Do **not** split by kid. One question per objective covers both Camilo and Luciana.
- Do not add a free-text option, "Other", or "Partial". Yes/No only.

For each `Yes` answer, append a row to `Progress/review_queue.md` with:

- **Source Lesson** = NN
- **Objective** = the objective text, lightly trimmed (drop trailing periods, keep wording verbatim otherwise)
- **Added on** = today's date (`YYYY-MM-DD`)
- **Scheduled in Lesson** / **Reviewed in Lesson** / **Reviewed on** = empty

`No` answers create no row.

If the teacher PDF has no clearly enumerated objectives (older lessons may not), tell Shane and ask him to list them — don't fabricate.

## Close out items scheduled for this lesson

Before adding new rows for this lesson's flags, find every row in `Progress/review_queue.md` where **Scheduled in Lesson** = NN. For each:

- Set **Reviewed in Lesson** = NN
- Set **Reviewed on** = today's date (`YYYY-MM-DD`)

These rows were drilled in this lesson's warm-up by `/create-lesson NN`. Use `Edit` in place — do not rewrite the file. Do not touch rows that already have a value in `Reviewed in Lesson` — those are historical record.

If no rows are scheduled for NN (e.g., this is lesson 1, or the queue was empty when `/create-lesson NN` ran, or `/create-lesson` wasn't used to build this lesson), skip this step silently.

## Updates to `Progress/coverage_tracker.md`

Edit the file in place. Don't rewrite it from scratch. Specific edits:

### 1. Grammar & skills covered table

Append one row to the table:

```
| YYYY-MM-DD | NN | <grammar / skill from lesson plan> |
```

If the existing table still has the placeholder row `_(none yet — school starts 2026-08-03)_`, replace that placeholder row with the new entry rather than appending below it.

### 2. Interest rotation in shared materials

Append a row for each shared material that has a clear featured interest. Typically that's the shared notes sheet plus any shared in-lesson content; per-kid materials don't go in this table. If the lesson only produced one shared artifact, one row is fine.

```
| NN | <material name, e.g., Notes_PRESENT_SIMPLE_SHARED> | <featured interest, e.g., faith / school / soccer / volleyball> | <L|C|S|B> |
```

Then **update the running balance line** at the bottom of that section. Increment whichever tag(s) you just added. Keep the format exact:

```
**Running balance:** L: <n> · C: <n> · S: <n> · B: <n>
```

## Updates to `Progress/vocabulary_log.md`

Edit in place.

### 1. Master list

For each glossed word that appears in the lesson's per-kid PDFs or the shared notes glossary:

- **If the word is not yet in the master list:** append a row.
  ```
  | <word EN> | <translation ES-LatAm> | <part of speech> | NN | <shared|Luciana|Camilo> | | <optional note> |
  ```
  `Source` is `shared` if the word first appeared in `Notes_..._SHARED.pdf` or in both kids' materials; otherwise `Luciana` or `Camilo`.
- **If the word is already in the master list from a previous lesson:** do **not** add a new row. Instead, append `Lesson NN` to the `Seen again` column, comma-separated.

Sort: keep the master list alphabetical by `Word (EN)` if it's already alphabetical; otherwise just append. Don't re-sort an unsorted table — that creates noisy diffs.

If the table still contains the placeholder row `_(none yet — school starts 2026-08-03)_`, replace it with the first real entry.

### 2. By-lesson block

Replace the `### Lesson NN` block's `_(not yet taught)_` placeholder (or append a new block if missing) with a tidy bulleted list of the words newly glossed in this lesson:

```
### Lesson NN
- <word EN> — <translation ES-LatAm> (<source>)
- ...
```

Words that were *re-glossed* (already in the master list) should be listed here too, but tag them `(review)` so the by-lesson block reflects what showed up in the lesson, not just what was new.

### 3. Quick-reference list

Don't touch the `Quick-reference: words both kids should know cold` section automatically. Per CLAUDE.md, words move there only after being recycled in at least two lessons *and* used correctly in writing or speaking. That's a judgment call Shane makes; if he says "promote X and Y to the quick-reference list," do that. Otherwise leave it alone.

## Updates to `Progress/review_queue.md`

Two distinct edits, both in place. Use `Edit`, not `Write`.

### 1. Close out scheduled rows

For every row where `Scheduled in Lesson` = NN, fill in `Reviewed in Lesson` = NN and `Reviewed on` = today's date. (See "Close out items scheduled for this lesson" above.)

### 2. Append new pending rows

For each `Yes` answer from the per-objective review check, append one row to the **Items** table:

```
| NN | <objective text> | YYYY-MM-DD | | | |
```

The last three columns (`Scheduled in Lesson`, `Reviewed in Lesson`, `Reviewed on`) are intentionally blank — `/create-lesson` will fill in `Scheduled in Lesson` when it builds the next lesson's warm-up.

If the table still contains the placeholder row `_(none yet)_`, replace it with the first real entry rather than appending below it.

## Workflow

1. **Resolve the lesson number.** Zero-pad. Confirm the corresponding folder and teacher PDF exist; bail with a clear message if not.
2. **Read inputs.** `CLAUDE.md`, all three progress files (`coverage_tracker.md`, `vocabulary_log.md`, `review_queue.md`), the schedule entry, and the three lesson PDFs (teacher plan, shared notes, per-kid materials). Use the `pdf` skill for the PDFs.
3. **Extract** the grammar/skill label, the lesson topic, the full glossed-vocabulary list (EN, ES-LatAm, part of speech, source), and the **learning objectives** from the teacher PDF.
4. **Ask Shane** for the items in *Information to gather* via a single `AskUserQuestion` call. Skip anything already supplied in the invoking message.
5. **Ask the per-objective review question** as a second `AskUserQuestion` call — one question per learning objective, Yes/No only. (See "Per-objective review check.")
6. **Compute the diffs** for all three files in your head before writing — placeholder replacements, new rows, balance increments, close-outs of `Scheduled in Lesson` = NN rows, and new pending review rows for each `Yes`.
7. **Summarize the planned edits in one block, then apply them.** List the grammar row, vocabulary additions/updates, rotation increment, review-queue close-outs, and review-queue new rows, then proceed to step 8 in the same turn. Pause only if a planned edit conflicts with an existing row — for example, a re-confirmation that would duplicate a `Lesson NN` entry already in the grammar table.
8. **Apply edits** with `Edit`. Do **not** use `Write` — these files are living docs and rewriting them from scratch loses formatting. Use `Edit` with enough surrounding context to make each `old_string` unique.
9. **Confirm** what was written: list the rows added/changed in each file, report the new running-balance line, and call out which review items were closed out and which new items entered the queue.

## Edge cases

- **Re-confirmation of a lesson already in the tracker.** If a row for `Lesson NN` already exists in the grammar table, don't duplicate. Update the existing row (date change) rather than appending. Tell Shane you're updating, not appending.
- **Lesson taught out of order.** Insert the row chronologically by date if the table is date-sorted; otherwise just append. The Lesson column is the source of truth, not row position.
- **No new vocabulary.** Some lessons drill structure with already-known words. That's fine — add nothing to the master list, and the by-lesson block can read `- (no new words; reviewed: <list>)`.
- **Shared materials with no clear featured interest.** Tag `S` (genuinely shared). Don't force `L` or `C`.
- **Lesson folder exists but PDFs are still markdown drafts.** This means the lesson was authored but not rendered/printed. Ask Shane whether to proceed using the markdown drafts or to wait — don't silently use drafts.
- **Teacher PDF has no clearly enumerated learning objectives.** Skip the per-objective review question and ask Shane to dictate the objectives (or accept that this lesson contributes nothing to the review queue). Don't invent objectives just to ask the question.
- **Re-confirmation of a lesson already in the tracker.** For the review queue specifically: any rows you previously appended with `Source Lesson` = NN remain (they're append-only). Don't delete or rewrite them. Close-outs of `Scheduled in Lesson` = NN rows are idempotent (re-writing today's date is fine).

## What not to do

- Don't update any tracker file before Shane confirms the lesson was taught — this skill *is* the confirmation step, but if invoked without a clear "we taught this," ask first.
- Don't ask Shane for free-text lesson-outcome notes (what stuck, what didn't, per-kid status, pacing changes). The only structured outcome signal is the per-objective Yes/No question — nothing else.
- Don't ask the review question separately for Camilo and Luciana. One question per objective covers both.
- Don't free-text Shane's reasoning. Yes/No only.
- Don't touch `Reviewed in Lesson` rows in `review_queue.md` that already have a value. They're historical record.
- Don't delete review-queue rows. The table is append-only.
- Don't promote words into the `Quick-reference` section unprompted.
- Don't rewrite any tracker file from scratch with `Write`. Edit in place.
- Don't fabricate a topic, grammar point, vocabulary, or learning objectives if the lesson PDFs are missing or unclear. Stop and tell Shane.
- Don't touch `Progress/Lesson_Schedule.md` from this skill. Schedule edits are a separate, deliberate action.
