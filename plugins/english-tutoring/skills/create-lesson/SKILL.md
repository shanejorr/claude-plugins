---
name: create-lesson
description: Generate a full numbered English lesson for the tutoring project at /Users/shaneorr/Documents/English — creates the instructor lesson plan (Lesson_NN_teacher.pdf) in Teacher Materials/, a shared grammar/topic notes reference sheet, and per-kid practice materials for Camilo and Luciana in Student Materials/Lesson_NN/. Use whenever Shane says "create lesson N", "build lesson N", "make lesson N", "generate lesson N", "prep lesson N", or any similar phrasing that references a specific lesson number. Trigger even if he only names the lesson number without enumerating the four artifacts — producing the complete set is the whole point of the skill.
user-invocable: true
disable-model-invocation: true
---

# Create Lesson

End-to-end builder for one full lesson. Given a lesson number, produce exactly four PDFs in the correct local folders:

1. `Lesson_NN_teacher.pdf` — instructor lesson plan (what Shane teaches from) → `Teacher Materials/`
2. `Notes_<TOPIC>_SHARED.pdf` — shared reference sheet on the grammar/topic → `Student Materials/Lesson_NN/`
3. `Materials_Camilo.pdf` — Camilo's personalized reading + practice + homework → `Student Materials/Lesson_NN/`
4. `Materials_Luciana.pdf` — Luciana's personalized reading + practice + homework → `Student Materials/Lesson_NN/`

`CLAUDE.md` at the project root is authoritative for student profiles, tone, CEFR targeting, and constraints. Don't restate that brief here — just follow it.

## Before you draft anything

Read these first. The project evolves; skipping this step is how you re-teach grammar, reuse character names, and drift off-level.

- `CLAUDE.md` — authoritative brief.
- `Progress/Lesson_Schedule.md` — find the entry for lesson N. The topic and description there is the default unless Shane says otherwise.
- `Progress/coverage_tracker.md` — what's been taught and the interest-rotation tally.
- `Progress/vocabulary_log.md` — words already glossed, so you don't re-gloss.
- `Progress/review_queue.md` — pending review items. Drives this lesson's warm-up content per the selection rule below.
- The last two or three existing `Lesson_NN/` folders — so you don't reuse character names or scenarios.

## Confirm scope before drafting

Use `AskUserQuestion` only where there is real ambiguity. Typical questions worth asking:

- If prior lessons shifted and the schedule's topic for N may no longer fit, confirm the topic.
- If the interest-rotation tally in `coverage_tracker.md` is lopsided, confirm which kid's interests lead the shared material.
- If `Lesson_NN/` already exists with files, confirm before overwriting.

If the schedule entry is clean and the rotation is balanced, skip the question. Just say briefly what you're proceeding with (topic, featured interest for shared content) and start drafting.

## Selecting review items for the warm-up

For lesson NN's warm-up, pull review items from `Progress/review_queue.md`. A **pending** row is one where `Scheduled in Lesson` is empty.

Selection rule:

1. Take **all** pending rows where `Source Lesson` = NN-1. These must all be drilled — items flagged in the previous lesson are always reviewed in the next.
2. If step 1 produced at least one row, sample **at least one** additional pending row where `Source Lesson` < NN-1.
3. If step 1 produced **zero** rows, sample **two** pending rows where `Source Lesson` < NN-1.
4. Floor: every warm-up has at least two review items, drawn from the queue, whenever any are pending.

Sampling strategy for the "from earlier lessons" steps: prefer older items first (smaller `Source Lesson` numbers — they've waited longest in the queue). Tie-break by `Added on` (oldest date first). This keeps the queue draining instead of letting stale items sit.

**Idempotency.** Before selecting, check `review_queue.md` for any rows already with `Scheduled in Lesson` = NN. If yes, reuse exactly those — you're re-running for the same lesson. If no, run the selection rule and then update `review_queue.md` to write `NN` into `Scheduled in Lesson` for each selected row. Use `Edit` in place — do not rewrite the file. Do not touch other columns.

**Empty-queue edge case.** If no pending rows match the rule (e.g., this is lesson 2 with nothing flagged in lesson 1, or the queue is fresh), the warm-up follows the standard structure with no forced review block. Note this explicitly in the teacher PDF's warm-up section ("No pending review items — warm-up uses topic-appropriate opener").

## What each artifact contains

Pitch everything to CEFR A1 unless the schedule says otherwise. When in doubt, aim at Luciana's level — she is the slower learner on paper and anxious about English. Camilo's IQ-report accommodations (chunking, visual aids, short dictations, varied evaluation formats) are good defaults for both.

Zero-pad `NN` to two digits everywhere it appears in paths and filenames (`Lesson_05`, not `Lesson_5`).

### Lesson_NN_teacher.pdf — instructor lesson plan

One shared document. Shane holds this while teaching. Include:

- Header: lesson number, topic, date blank, estimated total time
- 2–4 measurable learning objectives
- Materials list
- Five sections, each with minute estimate and language-of-instruction label (Spanish / English / mixed): **Warm-up**, **Teaching**, **Guided Practice**, **Independent Practice**, **Wrap-up**
  - **Warm-up** must explicitly drill every review item selected from `review_queue.md` above. Each item gets a short drill block (roughly 2–4 minutes): one Spanish-glossed prompt naming the rule, 3–5 quick prompts in English using the structure, and a one-line reset of the rule. List the items by name in the warm-up section header so Shane sees at a glance which items the warm-up covers. Extend warm-up minute estimate to fit; the rest of the lesson absorbs the difference. If no review items are pending, say so in the warm-up section ("No pending review items") and use a topic-appropriate opener.
- Concrete board-work examples the teacher should write out
- Differentiation notes: where to lean on Camilo's accommodations, where to buffer Luciana's anxiety (low-stakes openers, no cold-call public reading)
- Anticipated A1 Spanish-speaker error patterns for this grammar point, with a one-line fix each
- Homework line that points to the per-kid materials PDFs

Default language routing: Spanish when introducing a new rule, English for drilling and production. Label it explicitly.

### Notes_<TOPIC>_SHARED.pdf — shared reference sheet

One shared document both kids keep. It is the "cheat sheet" for the grammar point:

- Brief Spanish explanation of the rule (a few sentences, not a lecture)
- Form tables — conjugation, subject-pronoun chart, spelling-rule table, whatever fits
- A handful of clear English example sentences with Spanish translation alongside
- Common Spanish → English pitfalls for this structure
- A small glossary only if this topic brings in new high-frequency words

File name uses the grammar/topic in upper snake case: `Notes_TO_BE_SHARED.pdf`, `Notes_PRESENT_SIMPLE_SHARED.pdf`, `Notes_ARTICLES_AND_PLURALS_SHARED.pdf`.

### Materials_Camilo.pdf and Materials_Luciana.pdf

Per-kid independent practice and homework. Tailor to each kid's interests per CLAUDE.md. Each should include:

- A short reading passage (A1: 100–180 words; A2: 180–300) that uses the target grammar naturally and introduces no structure not yet taught
- 4–6 comprehension questions (mix true/false, short answer, multiple choice)
- A vocabulary box with Latin American Spanish translations for any word above A1
- A targeted practice worksheet (fill-in, matching, transform, build-a-sentence) drilling the target grammar
- A short dictation section — especially for Camilo (per his IQ-report recommendation). Luciana benefits from one too.
- A brief homework prompt asking for 3–5 sentences using the target grammar about the kid's own life

Interest cues (from CLAUDE.md): Camilo leans soccer (Real Madrid, Ronaldo), anime, drawing, Bible stories, video games. Luciana leans volleyball, fashion, reggaeton, Catholic faith, friendship, *Lilo & Stitch*, real US-school situations (ordering food, asking a teacher for help, meeting classmates).

Never use adoption, foster, or biological-family history as topic material. Vary character names across lessons — grep the last few lesson folders if unsure.

## Workflow

1. **Read.** `CLAUDE.md`, the schedule entry for N, `coverage_tracker.md`, `vocabulary_log.md`, `review_queue.md`, and the last two or three `Lesson_NN/` folders. These reads are independent — issue them in parallel.
2. **Confirm scope.** Ask only about real ambiguities; otherwise state briefly what you're proceeding with.
3. **Select review items.** Apply the selection rule from "Selecting review items for the warm-up" against `review_queue.md`. If nothing is already scheduled for NN, write `NN` into `Scheduled in Lesson` for the chosen rows now (not later — this happens before drafting so the warm-up has its list).
4. **Draft in markdown first.** Create four `.md` drafts in your outputs directory. Markdown is faster to iterate and the `pdf` skill renders it cleanly. The teacher plan's warm-up section must drill every review item selected in step 3.
5. **Self-check each draft before rendering.** Run through this list; revise the markdown if anything fails.
   - Vocabulary at or below A1 except glossed items
   - Spanish glosses use Latin American Spanish
   - Only grammar already taught (per `coverage_tracker.md`) plus the current target
   - Fresh character names; scenarios not reused from recent lessons
   - Right kid's interests in the right file; shared content reflects the rotation you chose
   - No forbidden topics
   - Length within A1 reading targets
   - Warm-up drills every review item selected from the queue, with minute estimate extended to fit

   Then re-read each reading passage as a true A1 Spanish-speaking beginner would, watching for: subordinate clauses where a simple sentence works, intermediate vocabulary with no gloss, tenses or structures the schedule says haven't been introduced yet, idioms or cultural references that need unpacking.
6. **Render to PDF.** Invoke the `pdf` skill in render mode to convert each markdown draft. Output paths:
   - `/Users/shaneorr/Documents/English/Teacher Materials/Lesson_NN_teacher.pdf`
   - `/Users/shaneorr/Documents/English/Student Materials/Lesson_NN/Notes_<TOPIC>_SHARED.pdf`
   - `/Users/shaneorr/Documents/English/Student Materials/Lesson_NN/Materials_Camilo.pdf`
   - `/Users/shaneorr/Documents/English/Student Materials/Lesson_NN/Materials_Luciana.pdf`
   Create `Student Materials/Lesson_NN/` if it does not exist. `Teacher Materials/` is always flat — no subfolders. If files already exist, confirm before overwriting.
7. **Upload PDFs to Google Drive.** Two separate Drive destinations — run the bundled script via Bash. Before running, substitute the tokens in the template below: `<N>` → lesson number (e.g. `5`), `NN` → zero-padded lesson number (e.g. `05`), `<TOPIC>` → the actual topic in upper snake case (e.g. `PRESENT_SIMPLE`).

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/create-lesson/scripts/upload_to_drive.py" \
     --lesson <N> \
     --student-pdf "/Users/shaneorr/Documents/English/Student Materials/Lesson_NN/Notes_<TOPIC>_SHARED.pdf" \
     --student-pdf "/Users/shaneorr/Documents/English/Student Materials/Lesson_NN/Materials_Camilo.pdf" \
     --student-pdf "/Users/shaneorr/Documents/English/Student Materials/Lesson_NN/Materials_Luciana.pdf" \
     --teacher-pdf "/Users/shaneorr/Documents/English/Teacher Materials/Lesson_NN_teacher.pdf"
   ```

   - **Student PDFs** (`--student-pdf`) → the `student` parent folder from `config/folders.json`, inside a `Lesson_NN` subfolder (created if absent).
   - **Teacher PDF** (`--teacher-pdf`) → the `teacher` folder from `config/folders.json`, uploaded flat (no subfolder).

   The script prints a JSON summary. If a file with the same name already exists, it is updated in place so Drive share links stay stable.

   **Auth.** OAuth 2.0 Desktop app. The script reads OAuth client credentials from `~/.config/gdrive-oauth/gdrive_credentials.json` and caches a refresh token at `~/.config/gdrive-oauth/gdrive_token.pickle`. First run opens a browser for OAuth consent; subsequent runs are non-interactive. Setup is **shared** with the `reading-pipeline` plugin's `send-to-reader` skill — same credentials file, same cached token. If the credentials file is missing, the script exits cleanly and points at the setup walkthrough in its docstring.

   **Dependencies.** The script needs `google-api-python-client`, `google-auth-httplib2`, and `google-auth-oauthlib`. If the script bails on `ImportError`, install them with `pip install --break-system-packages google-api-python-client google-auth-httplib2 google-auth-oauthlib` and retry.

   **Common first-run error.** A `403`/`404` from the Drive API usually means the OAuth account you authorized does not have access to the target Drive folder. Either re-share the folder with that Google account, or update `config/folders.json` with a folder you own.

   Parse the script's JSON output. The two URLs you need downstream are:
   - `student_subfolder_url` — for the student materials link
   - `teacher_file.web_view_link` — for the teacher plan link
8. **Email Jess.** Send the lesson-ready notification. Run the bundled script via Bash; substitute `<N>` (lesson number), `<TEACHER_URL>` (from `teacher_file.web_view_link`), and `<STUDENT_URL>` (from `student_subfolder_url`):

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/create-lesson/scripts/send_completion_email.py" \
     --lesson <N> \
     --teacher-url "<TEACHER_URL>" \
     --student-url "<STUDENT_URL>"
   ```

   **Auth.** Gmail SMTP with an app password. The script reads credentials from `~/.config/create-lesson/smtp.json`. One-time setup: at https://myaccount.google.com/apppasswords, generate a 16-character app password for "Mail," then create `~/.config/create-lesson/smtp.json` with the schema documented in the script's docstring, `chmod 600`.

   **Recipients.** `to_email` in the config is the primary recipient (Jess). The optional `cc_emails` list cc's additional addresses on every send — Shane's address belongs here so he gets a copy of what Jess receives.

   **On failure, do not retry blindly.** The lesson is already uploaded; an email error doesn't undo that. Report the error in your final summary and let Shane decide whether to fix config and rerun the script. Common errors: `SMTPAuthenticationError` (regenerate the app password), missing config file (run first-time setup), or a sandboxed network block.
9. **Share the files.** Return all four local paths (as `computer://` links if available), the Drive student subfolder URL, and the Drive teacher file URL. Note for Shane that the teacher plan goes to a separate Drive folder from the student materials. Also list which review items the warm-up drilled (objective text + source lesson) so Shane sees at a glance what's being recycled. Confirm the email to Jess was sent (or surface the error if it wasn't). Do **not** update `coverage_tracker.md` or `vocabulary_log.md` — per CLAUDE.md those only get updated after Shane confirms the lesson was taught. The only progress file this skill writes to is `review_queue.md` (and only the `Scheduled in Lesson` column on rows it selects).

## What not to do

- Don't write anything the kids will submit as their own work. These materials are for practice, not for them to turn in.
- Don't update `coverage_tracker.md` or `vocabulary_log.md` preemptively — that's the `confirm-lesson` step.
- Don't invent review items. Only items already present in `review_queue.md` get drilled in the warm-up.
- Don't write to `Reviewed in Lesson` or `Reviewed on` in `review_queue.md` — that's `/confirm-lesson`'s job. This skill only writes to `Scheduled in Lesson`.
- Don't delete or reorder rows in `review_queue.md`. The table is append-only and `Edit` should only update the `Scheduled in Lesson` cell on selected rows.
- If you need a one-off helper script, put it in `Progress/scripts/`, not in the lesson folder.
