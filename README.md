# Slack-to-Calendar
Simple, python program that allows me to automatically add my work schedule provided to me using Slack as work events on my Google Calendar. This program allows automation of a simple task, saving about 10 minutes of tedious scheduling each week. Run once a day via cronjob in order to ensure no new work events are missed.

# Pipeline
```
Cron triggers main.py:
  → slack_client.py checks channel for new schedule file
  → downloads file if new
  → parser.py runs table extraction on file, extracts user's shifts
  → calendar_client.py creates Google Calendar events
  → logs result to sync.log
```

# Tech Stack
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

* see [notes.md](notes.md) for full decision-making rationale

# Program Setup

1. Clone the repository. Run the following command in your terminal in a new empty folder:
    git clone https://github.com/Lsimoni1/Slack-to-Calendar.git

2. Install project dependencies. Run the following command in a terminal in your newly populated folder:
    pip3 install -r requirements.txt

3. Create a new file in your folder called config.py. In this file paste the following text:
```
SLACK_BOT_TOKEN = "your-slack-bot-token here"
SLACK_CHANNEL_ID = "your-slack-channel-id here"
MY_NAME = "your-name here"
TIMEZONE = "your-timezone here"
```
For MY_NAME, set its value exactly as your name appears on the Bloom Coffee Schedule PDF files. For TIMEZONE, set its value as your current timezone, e.g. "America/Los_Angeles".

4. Create a Slack app and obtain a bot token. Go to api.slack.com/apps and create a new app, enabling channels:history and files:read bot token scopes. Install the app into the Bloom Coffee workspace. Copy the bot User OAuth Token, and add it to config.py as the value for SLACK_BOT_TOKEN. Invite the bot to the #schedules channel in the Bloom Coffee Slack.

5. Create a Google Cloud project. Go to console.cloud.google.com and create a new project, enable the Google Calendar API for that project. Go to APIs & Services -> Credentials, and create an OAuth 2.0 Client ID. Download the credentials, and save it as credentials.json in the project folder.

6. In your terminal, ensure you are still in the project file and run:
    python3 main.py
This initial run will be necessary to grant the program access to your Google Calendar to make new events. This will also save your credentials so that the program can run automatically moving forward.

7. In your terminal, run:
    EDITOR=nano crontab -e 
When in your editor, you can save with Ctrl+O and exit with Ctrl+X. Add the line with the schedule and full absolute paths to Python and main.py as follows: 
```
  0 9 * * * cd /path/to/slack-to-calendar && /usr/bin/python3 main.py 
```
This command will run the program daily on your machine at a specified time. The 0 represents the minutes of the run, and the 9 represents the hour. So in this example, the program will be set to run at 9 am daily. If you wanted it to run at 5:30 pm for example, you would change the line to:
```
  30 17 * * * cd /path/to/slack-to-calendar && /usr/bin/python3 main.py 
```
Also don't forget to ensure you replace the path above with the actual path to the program on your machine. 

# File Structure
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