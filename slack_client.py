import config
from slack_sdk import WebClient
import requests

slack_token = config.SLACK_BOT_TOKEN
slack_channel = config.SLACK_CHANNEL_ID
client = WebClient(token = slack_token)


def fetch_new_schedule():
    messages = client.conversations_history(channel = slack_channel)
    files = []

    try:
        with open("latest_processed_file", "x") as f:
            f.write("0")
    except:
        pass

    with open("latest_processed_file") as f:
        latest_ts = f.read()

    if latest_ts == "0":
        for message in messages["messages"]:
            if "files" in message:
                if len(files) < 10:
                    files.append(message)
    else:
        current_ts_set = set()
        for line in latest_ts.split("\n"): 
            if line:
                current_ts_set.add(line.split()[0])
                latest_ts = line.split()[0]
        for message in messages["messages"]:
            if "files" in message: 
                if message["ts"] > latest_ts and message["ts"] not in current_ts_set:
                    files.append(message)

    if not files:
        return None
    
    for file in files:
        with open("latest_processed_file", "a") as f:
            f.write(file["ts"] + " UNPROCESSED\n")
    return files

def download_schedules(ts):
    message = client.conversations_history(channel = slack_channel, oldest = ts, latest = ts, inclusive = True)
    url = message["messages"][0]["files"][0]["url_private"]
    headers = {
        "Authorization" : "Bearer " + slack_token
    }
    response = requests.get(url, headers = headers)

    with open("current_schedule", "wb") as f:
        f.write(response.content)

    return "current_schedule"
    

    
        