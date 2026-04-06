# Slack to Calendar - Project Notes

## What it does
Detects when a new work schedule is posted as an image/PDF in the specified Slack channel,
extracts shifts using table extraction via pdfplumber, and creates accurate Google Calendar events automatically.

---

## Final Tech Stack

| Component         | Decision                                      |
|-------------------|-----------------------------------------------|
| Language          | Python                                        |
| Slack integration | Slack Web API (polling)                       |
| Table extraction  | pdfplumber                                    |
| Calendar          | Google Calendar API                           |
| Scheduling        | cron job, runs once daily                     |
| State tracking    | Simple file storing last processed message ID |
| Logging           | Simple log file                               |
| Hosting           | Local machine                                 |

---

## Refactored out

| Tool                     | Decision                                      |
|--------------------------|-----------------------------------------------|
| Pytesseract (OCR)        | Not suitable for table-based text parsing,    |
|                          | flat image processing lead to inaccurate      |
|                          | parsing of text.                              |
| pdf2image (PDF handling) | Unnecessary without OCR tool usage.           |

---

## Pre-Implementation Research & Decisions

- Slack Web API vs Slack Bolt SDK (DECIDED - see Pre-implementation Log)
    - Is Bolt worth using for a polling-based app or is it overkill?

- Tesseract vs Google Cloud Vision (DECIDED - see Pre-implementation Log)
    - Is the accuracy tradeoff worth it?

- cron vs launchd (macOS scheduler) (DECIDED - see Pre-implementation Log)
    - Which is more approachable?

---

## File Structure

```
slack-to-calendar/
├── main.py              # orchestrates everything
├── slack_client.py      # connects to Slack, finds and downloads schedule file
├── parser.py            # extract shifts from table information via pdfplumber
├── calendar_client.py   # creates Google Calendar events
├── config.py            # API keys, name, channel ID, etc.
├── sync.log             # running log of every sync
└── requirements.txt
```

---

## Metrics to Track (planned)
- Weeks in use
- Total shifts synced
- Parsing errors caught and fixed
- Time saved per week vs doing it manually

---

## Pre-implementation Notes / Decisions Log

1:
    Slack Web API - Allows for access to HTTP methods that can read from/write to Slack channels. Provides
                    basic interactions with Slack channels on an individually called basis.
    Slack Bolt SDK - Provides an application with the capabilities to react to Slack events and channels. 
                    Can use calls from the Slack Web API as well as event routing, connection management, and more
                    support for how to write Slack-based applications.
Decision: Slack Web API, this application will be triggered regularly and therefore won't need to react to events 
        within the Slack channels being observed. In addition, since we will only be reading from one channel for a 
        specific kind of file, keeping the tools lean allows for simpler and more understandable code/structure.

2: (DECISION SUPERSEDED, SEE IMPLEMENTATION LOG)
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

## Implementation Notes / Decisions Log

1:
    Python Tesseract + pdf2image - Allows for text extraction of raw unstructured text, and converts directly into
                                    String data allowing for ease of use. Processing is done as a flat image without 
                                    consideration for any kind of table structure, leading to errors and lost information.
    pdfplumber - Allows for table extraction of structured text from PDFs, providing information such as row/columns that provides
                structure for easy parsing of specific data.
Decision: Since the structure of the pdf schedules sent out is a consistent and readable table, pdfplumber provides a much more
        accurate and usable parsing of data. Pdfplumber also extracts the data locally without sending any information
        to an external service, upholding the privacy of other workers.