#!/usr/bin/env python3
"""Upload lesson PDFs to Google Drive via the Drive v3 API (OAuth 2.0 auth).

What this does
--------------
Given a lesson number and PDF paths, this script uploads to TWO separate
Google Drive folders:

  1. Student PDFs (Notes_*_SHARED.pdf, Materials_Camilo.pdf,
     Materials_Luciana.pdf) → student parent folder / Lesson_NN subfolder
  2. Teacher PDF (Lesson_NN_teacher.pdf) → teacher folder (flat, no subfolder)

Parent folder IDs are read from a `folders.json` file keyed by role
(`student`, `teacher`) so personal folder IDs do not live in this
script. The script looks for that file in this order:

  1. `--folders-config PATH` (CLI flag)
  2. `$ENGLISH_TUTORING_FOLDERS_CONFIG` environment variable
  3. `~/.config/create-lesson/folders.json`  (preferred — survives plugin upgrades)
  4. `<skill>/config/folders.json`           (legacy in-tree location)

Copy `config/folders.example.json` to one of those paths and fill in
the IDs. The user-config path (#3) is preferred because the in-tree
copy is wiped whenever the plugin is reinstalled or upgraded.

If a file with the same name already exists in the target location, its
contents are updated in place so Drive share links stay stable.

Prints a JSON summary with student_subfolder_url and teacher_file_url.

Auth
----
OAuth 2.0 Desktop app, with the refresh token cached as a pickle. The
OAuth credentials and token are shared with the `reading-pipeline`
plugin's `send-to-reader` skill at:

    ~/.config/gdrive-oauth/gdrive_credentials.json   (you provide)
    ~/.config/gdrive-oauth/gdrive_token.pickle       (auto-created)

First run opens a browser for OAuth consent; subsequent runs are
non-interactive. Files uploaded this way are owned by your Google
account.

First-time setup (one-time, on this Mac)
----------------------------------------
  1. mkdir -p ~/.config/gdrive-oauth && chmod 700 ~/.config/gdrive-oauth
  2. Go to https://console.cloud.google.com and create or pick a project.
  3. Enable the Google Drive API (APIs & Services > Library > "Google
     Drive API" > Enable).
  4. APIs & Services > OAuth consent screen: make sure the scope
     `https://www.googleapis.com/auth/drive` is included.
  5. APIs & Services > Credentials > Create Credentials > OAuth client ID
     > application type "Desktop app". Download the JSON.
  6. Save it as ~/.config/gdrive-oauth/gdrive_credentials.json.
  7. Copy this skill's folders template into your user-config dir and
     fill in your folder IDs:
       mkdir -p ~/.config/create-lesson
       cp config/folders.example.json ~/.config/create-lesson/folders.json
     (The user-config path is preferred over the in-tree config/ path
     because the latter is wiped on plugin upgrade.)
  8. Run the script. A browser window opens for OAuth consent. The
     refresh token is then cached as gdrive_token.pickle.

If reading-pipeline already has a token cached at its old in-tree path
(plugins/reading-pipeline/.../credentials/gdrive_token.pickle) with the
narrower `drive.file` scope, delete it — the new `drive` scope requires
a fresh consent flow.

Dependencies
------------
  pip install --break-system-packages \\
      google-api-python-client google-auth-httplib2 google-auth-oauthlib

Usage
-----
  python3 upload_to_drive.py \\
      --lesson 5 \\
      --student-pdf "/Users/shaneorr/Documents/English/Student Materials/Lesson_05/Notes_POSSESSIVES_SHARED.pdf" \\
      --student-pdf "/Users/shaneorr/Documents/English/Student Materials/Lesson_05/Materials_Camilo.pdf" \\
      --student-pdf "/Users/shaneorr/Documents/English/Student Materials/Lesson_05/Materials_Luciana.pdf" \\
      --teacher-pdf "/Users/shaneorr/Documents/English/Teacher Materials/Lesson_05_teacher.pdf"
"""

from __future__ import annotations

import argparse
import json
import os
import pickle
import sys
from pathlib import Path

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
except ImportError as e:
    missing = getattr(e, "name", "a google-api library")
    sys.exit(
        f"Missing dependency: {missing}\n"
        "Install with:\n"
        "  pip install --break-system-packages google-api-python-client "
        "google-auth-httplib2 google-auth-oauthlib"
    )


SCOPES = ["https://www.googleapis.com/auth/drive"]

DEFAULT_CREDENTIALS_PATH = os.path.expanduser(
    "~/.config/gdrive-oauth/gdrive_credentials.json"
)
DEFAULT_TOKEN_PATH = os.path.expanduser(
    "~/.config/gdrive-oauth/gdrive_token.pickle"
)

SKILL_DIR = Path(__file__).resolve().parent.parent
USER_CONFIG_FOLDERS = os.path.expanduser("~/.config/create-lesson/folders.json")
INTREE_FOLDERS_CONFIG = str(SKILL_DIR / "config" / "folders.json")
EXAMPLE_FOLDERS_CONFIG = str(SKILL_DIR / "config" / "folders.example.json")

FOLDER_MIME = "application/vnd.google-apps.folder"


def resolve_folders_config(cli_value: str | None) -> str:
    """Pick the folders.json path: CLI > env var > user-config > in-tree.

    Returns the first path that exists, or the highest-priority default
    so error messages point the user at the preferred location.
    """
    if cli_value:
        return cli_value
    env_value = os.environ.get("ENGLISH_TUTORING_FOLDERS_CONFIG")
    if env_value:
        return env_value
    if os.path.exists(USER_CONFIG_FOLDERS):
        return USER_CONFIG_FOLDERS
    if os.path.exists(INTREE_FOLDERS_CONFIG):
        return INTREE_FOLDERS_CONFIG
    return USER_CONFIG_FOLDERS


def load_folders(folders_config_path: str) -> tuple[str, str]:
    """Return (student_parent_id, teacher_folder_id) from folders.json."""
    if not os.path.exists(folders_config_path):
        sys.exit(
            f"Folders config not found at {folders_config_path}.\n"
            f"Copy the template and fill in your folder IDs:\n"
            f"  mkdir -p {os.path.dirname(USER_CONFIG_FOLDERS)}\n"
            f"  cp {EXAMPLE_FOLDERS_CONFIG} {USER_CONFIG_FOLDERS}\n"
            f"Open each Drive folder in a browser and copy the folder ID "
            f"(the last segment of the URL) into the JSON.\n"
            f"The user-config path above is preferred — the in-tree "
            f"plugin config is wiped on every plugin upgrade."
        )

    with open(folders_config_path, "r") as f:
        folders = json.load(f)

    missing = [k for k in ("student", "teacher") if k not in folders]
    if missing:
        sys.exit(
            f"Missing keys {missing} in {folders_config_path}. "
            f"Both 'student' and 'teacher' are required."
        )

    unset = [
        k for k in ("student", "teacher")
        if not folders[k] or str(folders[k]).startswith("REPLACE_")
    ]
    if unset:
        sys.exit(
            f"Folder ID(s) for {unset} are unset in {folders_config_path}. "
            f"Open each Drive folder in a browser and copy the folder ID "
            f"(the last segment of the URL) into the JSON file."
        )

    return folders["student"], folders["teacher"]


def get_credentials(credentials_path: str, token_path: str) -> Credentials:
    creds = None
    if os.path.exists(token_path):
        with open(token_path, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                sys.exit(
                    f"OAuth credentials file not found at {credentials_path}.\n"
                    "See the setup instructions in this script's docstring."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)

        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, "wb") as f:
            pickle.dump(creds, f)

    return creds


def escape_drive_query(value: str) -> str:
    """Escape single quotes and backslashes for a Drive `q` parameter string."""
    return value.replace("\\", "\\\\").replace("'", "\\'")


def find_or_create_subfolder(service, parent_id: str, name: str) -> tuple[str, str]:
    """Return (folder_id, action) where action is 'found' or 'created'."""
    q_name = escape_drive_query(name)
    q_parent = escape_drive_query(parent_id)
    query = (
        f"'{q_parent}' in parents "
        f"and name = '{q_name}' "
        f"and mimeType = '{FOLDER_MIME}' "
        f"and trashed = false"
    )
    resp = (
        service.files()
        .list(
            q=query,
            fields="files(id, name)",
            pageSize=10,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        )
        .execute()
    )
    existing = resp.get("files", [])
    if existing:
        return existing[0]["id"], "found"
    meta = {
        "name": name,
        "mimeType": FOLDER_MIME,
        "parents": [parent_id],
    }
    folder = (
        service.files()
        .create(body=meta, fields="id", supportsAllDrives=True)
        .execute()
    )
    return folder["id"], "created"


def upload_pdf(service, folder_id: str, pdf_path: Path) -> dict:
    """Upload or update a PDF in the given Drive folder."""
    q_folder = escape_drive_query(folder_id)
    q_name = escape_drive_query(pdf_path.name)
    query = (
        f"'{q_folder}' in parents "
        f"and name = '{q_name}' "
        f"and trashed = false"
    )
    resp = (
        service.files()
        .list(
            q=query,
            fields="files(id, name)",
            pageSize=5,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        )
        .execute()
    )
    existing = resp.get("files", [])
    media = MediaFileUpload(str(pdf_path), mimetype="application/pdf", resumable=False)
    if existing:
        file_id = existing[0]["id"]
        updated = (
            service.files()
            .update(
                fileId=file_id,
                media_body=media,
                fields="id, webViewLink",
                supportsAllDrives=True,
            )
            .execute()
        )
        return {
            "id": updated["id"],
            "name": pdf_path.name,
            "web_view_link": updated.get("webViewLink"),
            "action": "updated",
        }
    meta = {"name": pdf_path.name, "parents": [folder_id]}
    created = (
        service.files()
        .create(
            body=meta,
            media_body=media,
            fields="id, webViewLink",
            supportsAllDrives=True,
        )
        .execute()
    )
    return {
        "id": created["id"],
        "name": pdf_path.name,
        "web_view_link": created.get("webViewLink"),
        "action": "created",
    }


def drive_hint(status) -> str:
    if status in (403, 404):
        return (
            "\nHint: a 403/404 here usually means the OAuth account you "
            "authorized does not have access to the target Drive folder. "
            "Either re-share the folder with that account, or update "
            "your folders.json (see --folders-config) with a folder you own."
        )
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Upload lesson PDFs to two Google Drive folders using OAuth.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--lesson",
        type=int,
        required=True,
        help="Lesson number (e.g. 5). Student subfolder named Lesson_NN (zero-padded).",
    )
    parser.add_argument(
        "--student-pdf",
        action="append",
        dest="student_pdfs",
        metavar="PATH",
        help=(
            "Local path to a student-facing PDF (Notes or Materials). "
            "Repeat for multiple files. Uploaded to student_parent/Lesson_NN/."
        ),
    )
    parser.add_argument(
        "--teacher-pdf",
        dest="teacher_pdf",
        metavar="PATH",
        help=(
            "Local path to the teacher lesson plan PDF. "
            "Uploaded flat into the teacher folder (no subfolder)."
        ),
    )
    parser.add_argument(
        "--folders-config",
        default=None,
        help=(
            "Path to folders.json. If omitted, the script searches: "
            "$ENGLISH_TUTORING_FOLDERS_CONFIG → "
            f"{USER_CONFIG_FOLDERS} → {INTREE_FOLDERS_CONFIG}"
        ),
    )
    parser.add_argument(
        "--credentials",
        default=os.environ.get("GDRIVE_CREDENTIALS", DEFAULT_CREDENTIALS_PATH),
        help="Path to OAuth credentials JSON",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GDRIVE_TOKEN", DEFAULT_TOKEN_PATH),
        help="Path to saved auth token",
    )
    args = parser.parse_args()

    if not 1 <= args.lesson <= 99:
        sys.exit("Lesson number must be between 1 and 99.")
    if not args.student_pdfs and not args.teacher_pdf:
        sys.exit("Provide at least one --student-pdf or --teacher-pdf.")

    student_paths = [Path(p).expanduser().resolve() for p in (args.student_pdfs or [])]
    teacher_path = Path(args.teacher_pdf).expanduser().resolve() if args.teacher_pdf else None

    missing = [p for p in student_paths if not p.is_file()]
    if teacher_path and not teacher_path.is_file():
        missing.append(teacher_path)
    if missing:
        sys.exit("Missing file(s):\n  " + "\n  ".join(str(p) for p in missing))

    folders_config_path = resolve_folders_config(args.folders_config)
    student_parent_id, teacher_folder_id = load_folders(folders_config_path)

    creds = get_credentials(args.credentials, args.token)
    service = build("drive", "v3", credentials=creds, cache_discovery=False)

    subfolder_name = f"Lesson_{args.lesson:02d}"
    result: dict = {"lesson": subfolder_name, "uploaded_by": "oauth"}

    # --- Student PDFs → student_parent_id / Lesson_NN subfolder ---
    if student_paths:
        try:
            subfolder_id, folder_action = find_or_create_subfolder(
                service, student_parent_id, subfolder_name
            )
            student_files = [upload_pdf(service, subfolder_id, p) for p in student_paths]
        except HttpError as e:
            status = getattr(getattr(e, "resp", None), "status", None)
            sys.exit(f"Google Drive API error (student folder): {e}{drive_hint(status)}")

        result["student_subfolder_name"] = subfolder_name
        result["student_subfolder_id"] = subfolder_id
        result["student_subfolder_url"] = f"https://drive.google.com/drive/folders/{subfolder_id}"
        result["student_subfolder_action"] = folder_action
        result["student_files"] = student_files

    # --- Teacher PDF → teacher_folder_id (flat) ---
    if teacher_path:
        try:
            teacher_file = upload_pdf(service, teacher_folder_id, teacher_path)
        except HttpError as e:
            status = getattr(getattr(e, "resp", None), "status", None)
            sys.exit(f"Google Drive API error (teacher folder): {e}{drive_hint(status)}")

        result["teacher_folder_id"] = teacher_folder_id
        result["teacher_folder_url"] = f"https://drive.google.com/drive/folders/{teacher_folder_id}"
        result["teacher_file"] = teacher_file

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
