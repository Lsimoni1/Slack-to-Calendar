# CLAUDE.md - Project Context

## Learning Philosophy
This project prioritizes the user's learning above all else. The user writes essentially
all code themselves. Claude's role is to explain concepts, guide decisions, review code
for correctness, and answer questions — not to write the implementation. Do not write
code blocks intended to be directly copied unless explicitly asked.

---

## Project Overview
A Python automation tool that detects when a work schedule is posted as an image/PDF
in a Slack channel, extracts shifts using OCR, and creates Google Calendar events
automatically. Runs on a daily cron job.

---

## Tech Stack
| Component         | Decision                                      |
|-------------------|-----------------------------------------------|
| Language          | Python                                        |
| Slack integration | Slack Web API (slack-sdk)                     |
| OCR               | Tesseract via pytesseract                     |
| PDF handling      | pdf2image                                     |
| Calendar          | Google Calendar API                           |
| Scheduling        | cron job, runs once daily                     |
| State tracking    | Simple file storing last processed message ID |
| Logging           | Simple log file (sync.log)                    |
| Hosting           | Local machine                                 |

---

## File Structure
```
slack-to-calendar/
├── main.py              # orchestrates everything
├── slack_client.py      # connects to Slack, finds and downloads schedule file
├── parser.py            # OCR + extract shifts from raw text
├── calendar_client.py   # creates Google Calendar events
├── config.py            # API keys, name, channel ID (gitignored)
├── credentials.json     # Google OAuth credentials (gitignored)
├── token.json           # Google auth token, auto-generated (gitignored)
├── sync.log             # running log of every sync
└── requirements.txt
```

---

## Pipeline
```
Cron triggers main.py
  → slack_client.py checks channel for new schedule file
  → downloads file if new
  → parser.py runs OCR on file, extracts user's shifts
  → calendar_client.py creates Google Calendar events
  → logs result to sync.log
```

---

## Setup Status
- [x] Slack app created, bot token obtained, installed to workspace
- [x] Google Cloud project created, Calendar API enabled
- [x] OAuth credentials downloaded (credentials.json)
- [x] All dependencies installed (slack-sdk, pytesseract, pdf2image, google-api-python-client, google-auth-oauthlib, Pillow)
- [x] Tesseract installed via Homebrew
- [ ] slack_client.py
- [ ] parser.py
- [ ] calendar_client.py
- [ ] main.py
- [ ] cron job setup

---

## Where We Left Off
Ready to start writing code. Begin with slack_client.py.

slack_client.py needs to:
1. Connect to Slack using the bot token from config.py
2. Fetch message history from the schedule channel
3. Identify messages that have a file attached
4. Compare against last processed message ID to avoid duplicates
5. Download the file if it is new

The main Slack SDK method to use is client.conversations_history()
