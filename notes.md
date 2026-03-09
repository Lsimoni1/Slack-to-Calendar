# Slack to Calendar - Project Notes

## What it does
Detects when a new work schedule is posted as an image/PDF in Slack,
extracts shifts using OCR, and creates Google Calendar events automatically.

---

## Tech Stack (decided)

| Component         | Decision                                      |
|-------------------|-----------------------------------------------|
| Language          | Python                                        |
| Slack integration | Slack Web API (polling)                       |
| OCR               | Tesseract via pytesseract                     |
| PDF handling      | pdf2image                                     |
| Calendar          | Google Calendar API                           |
| Scheduling        | cron job, runs once daily                     |
| State tracking    | Simple file storing last processed message ID |
| Logging           | Simple log file                               |
| Hosting           | Local machine                                 |

---

## Still Researching

- Slack Web API vs Slack Bolt SDK (DECIDED - info below)
    - Is Bolt worth using for a polling-based app or is it overkill?

- Tesseract vs Google Cloud Vision (DECIDED - info below)
    - Is the accuracy tradeoff worth it?

- cron vs launchd (macOS scheduler) (DECIDED - info below)
    - Which is more approachable?

---

## File Structure (planned)

```
slack-to-calendar/
├── main.py              # orchestrates everything
├── slack_client.py      # connects to Slack, finds and downloads schedule file
├── parser.py            # OCR + extract shifts from raw text
├── calendar_client.py   # creates Google Calendar events
├── config.py            # API keys, name, channel ID, etc.
├── sync.log             # running log of every sync
└── requirements.txt
```

---

## Metrics to Track (for resume)
- Weeks in use
- Total shifts synced
- Parsing errors caught and fixed
- Time saved per week vs doing it manually

---

## Notes / Decisions Log

1:
    Slack Web API - Allows for accesss to HTTP methods that can read from/write to Slack channels. Provides
                    basic interactions with Slack channels on an individually called basis.
    Slack Bolt SDK - Provides an application with the capabilities to react to Slack events and channels. 
                    Can use calls from the Slack Web API as well as event routing, connection management, and more
                    support for how to write Slack-based applications.
Decision: Slack Web API, this application will be triggered regularly and therefore won't need to react to events 
        within the Slack channels being observed. In addition, since we will only be reading from one channel for a 
        specific kind of file, keeping the tools lean allows for simpler and more understandable code/structure.

2:
    Python Tesseract - Simple text recognition from images, processed data can be translated directly into String 
                        data. No need for any type of web/server communication so very lightweight. Accuracy can vary 
                        according to picture quality.
    Google Cloud Vision - More precise and accurate image processing, with access to cloud storage and more complex 
                        capabilities. Set up requires authentication with Google Cloud and use of a client library.
Decision: Since the format of our images being processed is a consistent pdf, accuracy in the case of poor images will
        be an irrelevant factor. In addition, because of privacy of other workers, using a service like Google Cloud could
        be a concern. Because of the simple needs for our use case, Python Tesseract will be better here.

3:
    Cron - Long-time industry standard for automated services/jobs. Very simple implementation with a variety of applications.
            The biggest downside of cron is that if a machine is not on at the scheduled time of a service, that service will 
            be missed/not run.
    Launchd - Allows automated services/jobs on MacOS systems by allowing daemons/agents to control what programs run on 
            system startup. Gives control to daemons/agents before kernel, allowing for lots of control over O/S.
Decision: Cron will fit the uses of this application better. We can get around the issue of missed runs by scheduling generously
        (daily). In addition, if I want to install the application on my Windows desktop as well, I will be less likely to miss
        scheduled program runs (will require WSL on setup).

---