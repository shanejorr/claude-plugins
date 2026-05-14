#!/usr/bin/env python3
"""Send the "lesson ready" email to Jess after a /create-lesson run.

What this does
--------------
Sends a plain-text email announcing that a lesson is uploaded to Google
Drive, with the two share URLs (teacher PDF, student folder). The body is
fixed by Shane's template — no signature, no banner, no HTML alternative.

Auth
----
Gmail SMTP with an app password. The script reads credentials from
~/.config/create-lesson/smtp.json — same directory as the Drive
service-account key used by upload_to_drive.py, by design.

Config file schema (mode 0600):
  {
    "smtp_user": "shane.j.orr@gmail.com",
    "smtp_password": "<16-char Gmail app password, no spaces>",
    "from_email": "shane.j.orr@gmail.com",
    "to_email":   "jessorr11@gmail.com"
  }

First-time setup
----------------
  1. Enable 2-Step Verification on the sending Gmail account if not yet on.
  2. Generate an app password at https://myaccount.google.com/apppasswords
     (app: "Mail", device: name it whatever — "create-lesson script").
     Google shows a 16-character token; strip spaces.
  3. Create the config file:
       mkdir -p ~/.config/create-lesson
       # write smtp.json with the schema above
       chmod 600 ~/.config/create-lesson/smtp.json

Usage
-----
  python3 send_completion_email.py \\
      --lesson 5 \\
      --teacher-url "https://drive.google.com/file/d/<id>/view?usp=drivesdk" \\
      --student-url "https://drive.google.com/drive/folders/<id>"

Exit codes
----------
  0 — sent
  1 — usage / config / validation error
  2 — SMTP authentication failed (regenerate app password)
  3 — other SMTP / network error
"""

from __future__ import annotations

import argparse
import json
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "create-lesson"
SMTP_CONFIG_PATH = CONFIG_DIR / "smtp.json"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

REQUIRED_KEYS = ("smtp_user", "smtp_password", "from_email", "to_email")


def load_config() -> dict:
    if not SMTP_CONFIG_PATH.exists():
        sys.exit(
            f"Missing SMTP config at {SMTP_CONFIG_PATH}.\n"
            "Create a Gmail app password at https://myaccount.google.com/apppasswords "
            "(app: Mail), then write the file with this schema:\n"
            '  {\n'
            '    "smtp_user": "shane.j.orr@gmail.com",\n'
            '    "smtp_password": "<16-char app password, no spaces>",\n'
            '    "from_email": "shane.j.orr@gmail.com",\n'
            '    "to_email":   "jessorr11@gmail.com"\n'
            '  }\n'
            f"Then: chmod 600 {SMTP_CONFIG_PATH}"
        )
    try:
        config = json.loads(SMTP_CONFIG_PATH.read_text())
    except json.JSONDecodeError as e:
        sys.exit(f"SMTP config at {SMTP_CONFIG_PATH} is not valid JSON: {e}")
    missing = [k for k in REQUIRED_KEYS if not config.get(k)]
    if missing:
        sys.exit(
            f"SMTP config at {SMTP_CONFIG_PATH} is missing required keys: "
            f"{', '.join(missing)}"
        )
    return config


def build_message(lesson: int, teacher_url: str, student_url: str, from_email: str, to_email: str) -> EmailMessage:
    subject = f"Lesson {lesson:02d} ready"
    body = (
        f"Hey h,\n\n"
        f"Lesson {lesson:02d} is uploaded to google drive.\n\n"
        f"- Teacher Material {teacher_url}\n"
        f"- Student materials {student_url}\n"
    )
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)
    return msg


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Send the lesson-ready notification email to Jess.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--lesson", type=int, required=True, help="Lesson number (1-99).")
    parser.add_argument("--teacher-url", required=True, help="Drive URL for the teacher PDF.")
    parser.add_argument("--student-url", required=True, help="Drive URL for the student lesson folder.")
    args = parser.parse_args()

    if not 1 <= args.lesson <= 99:
        sys.exit("Lesson number must be between 1 and 99.")
    if not args.teacher_url.strip():
        sys.exit("--teacher-url must be a non-empty URL.")
    if not args.student_url.strip():
        sys.exit("--student-url must be a non-empty URL.")

    config = load_config()
    msg = build_message(
        lesson=args.lesson,
        teacher_url=args.teacher_url.strip(),
        student_url=args.student_url.strip(),
        from_email=config["from_email"],
        to_email=config["to_email"],
    )

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
            smtp.starttls()
            smtp.login(config["smtp_user"], config["smtp_password"])
            smtp.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        sys.stderr.write(
            f"Gmail SMTP authentication failed: {e}\n"
            "The app password is likely wrong or revoked. Regenerate one at "
            "https://myaccount.google.com/apppasswords and update "
            f"{SMTP_CONFIG_PATH}.\n"
        )
        return 2
    except (smtplib.SMTPException, OSError) as e:
        sys.stderr.write(f"Email send failed: {e}\n")
        return 3

    print(json.dumps({
        "status": "sent",
        "to": config["to_email"],
        "subject": msg["Subject"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
