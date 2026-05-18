# english-tutoring

Personal Cowork plugin for Shane's at-home English tutoring of Camilo (13) and Luciana (16). Encodes the lesson-creation and progress-tracking workflows used in the project at `/Users/shaneorr/Documents/English`. Both children are CEFR A1 entering Cobb County public schools in August 2026.

This plugin is project-specific by design — paths, Drive folder IDs, student profiles, and pedagogical conventions live in the project's `CLAUDE.md` and the bundled skills. It is not intended for general distribution.

## Skills

### create-lesson

Generates a full numbered lesson: the teacher lesson plan PDF, a shared grammar/topic notes sheet, and per-kid practice materials for both children. Reads the project's coverage tracker, vocabulary log, lesson schedule, and review queue first so it doesn't re-teach material or recycle character names. Pitches everything to CEFR A1 by default. Optionally uploads the rendered PDFs to two separate Google Drive folders via the bundled `upload_to_drive.py` script.

The warm-up section of every lesson is built from `Progress/review_queue.md`: all items flagged in the previous lesson get drilled, plus at least one item sampled from an earlier lesson (or two from earlier lessons if the previous lesson flagged nothing). Minimum two review items per warm-up when any are pending.

Trigger phrases: "create lesson N", "build lesson N", "make lesson N", "generate lesson N", "prep lesson N".

### confirm-lesson

Updates `Progress/coverage_tracker.md`, `Progress/vocabulary_log.md`, and `Progress/review_queue.md` after a lesson has actually been taught. Pulls the grammar point and glossed vocabulary out of the lesson PDFs, asks for the date taught and the interest-rotation tag, then asks one Yes/No question per learning objective to populate the review queue. Items flagged "Yes" drive subsequent lessons' warm-ups via `create-lesson`. Single question per item — not split by kid. No free-text per-kid notes or pacing observations are captured. Per project rules these files are never updated until Shane confirms the lesson happened.

Trigger phrases: "confirm lesson N", "we taught lesson N", "mark lesson N as taught", "update tracker for lesson N", "log lesson N".

## Bundled scripts

`skills/create-lesson/scripts/upload_to_drive.py` uploads lesson PDFs to Google Drive using an OAuth 2.0 Desktop-app credential at `~/.config/gdrive-oauth/gdrive_credentials.json`, with the cached refresh token at `~/.config/gdrive-oauth/gdrive_token.pickle`. The OAuth credentials are **shared** with the `reading-pipeline` plugin's `send-to-reader` skill — one consent flow covers both. The full one-time setup is documented in the script's docstring. Destination folder IDs live in `skills/create-lesson/config/folders.json` (gitignored). Dependencies: `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`.

Files uploaded this way are owned by your Google account. Re-uploads update the existing file in place, so Drive share links stay stable.

## Project assumptions

The skills assume the project layout described in `/Users/shaneorr/Documents/English/CLAUDE.md`:

- `Progress/coverage_tracker.md`, `Progress/vocabulary_log.md`, `Progress/review_queue.md`, `Progress/Lesson_Schedule.md`
- `Teacher Materials/Lesson_NN_teacher.pdf` (flat)
- `Student Materials/Lesson_NN/` containing `Notes_<TOPIC>_SHARED.pdf`, `Materials_Camilo.pdf`, `Materials_Luciana.pdf`

If the project layout changes, both SKILL.md files need to be updated to match.
