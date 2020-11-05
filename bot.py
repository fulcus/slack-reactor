import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']
emoji = 'thumbsup'

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    #user_id = event.get('user')
    timestamp = event.get('ts')

    if event.get("subtype") == 'bot_message':
        client.reactions_add(channel=channel_id,
                             name=emoji, timestamp=timestamp)
        print("Bot message, reacted with " + emoji)
    else:
        print("User message, didn't react")


if __name__ == "__main__":
    app.run(debug=True)  # port 5000 by default
