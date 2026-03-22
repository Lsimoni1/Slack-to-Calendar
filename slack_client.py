import config
from slack_sdk import WebClient
import requests

slack_token = config.SLACK_BOT_TOKEN
slack_channel = config.SLACK_CHANNEL_ID

def fetch_new_schedule():
    client = WebClient(token = slack_token)
    messages = client.conversations_history(channel = slack_channel)
    files = []

    try:
        with open("latest_processed_file", "x") as f:
            f.write("0")
    except:
        pass

    with open("latest_processed_file") as f:
        latest_ts = f.read()

    for message in messages["messages"]:
        if "files" in message: 
            if message["ts"] > latest_ts:
                files.append(message)

    if not files:
        return None
    
    with open("latest_processed_file", "w") as f:
        f.write(files[0]["ts"])
    return files

def download_schedules():
    files = fetch_new_schedule() 
    if not files:
        return
    
    url = files[0]["files"][0]["url_private"]
    headers = {
        "Authorization" : "Bearer " + slack_token
    }
    response = requests.get(url, headers = headers)

    with open("latest_schedule", "wb") as f:
        f.write(response.content)

    return "latest_schedule"
    

    
        