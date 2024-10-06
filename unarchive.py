import requests
from datetime import datetime, timedelta

SLACK_API_TOKEN = 'xoxb-xxxxxxxxxxxxxxxxxx'

url_unarchive_channel = "https://slack.com/api/admin.conversations.unarchive"

headers = {
    'Authorization': f'Bearer {SLACK_API_TOKEN}',
    'Content-Type': 'application/x-www-form-urlencoded',
}

log_file = "archived_channels_log.txt"
minutes_to_check = 10
now = datetime.now()

try:
    with open(log_file, 'r') as log:
        archived_recently = []

        for line in log:
            channel_id, channel_name, timestamp_str = line.strip().split(',')
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")

            # If the channel was archived within the last 10 minutes
            if now - timestamp <= timedelta(minutes=minutes_to_check):
                archived_recently.append((channel_id, channel_name))

    if archived_recently:
        print(f"Channels archived in the last {minutes_to_check} minutes:")
        for channel_id, channel_name in archived_recently:
            print(f"- {channel_name} (ID: {channel_id})")

            # Attempt to unarchive the channel
            response = requests.post(
                url_unarchive_channel,
                headers=headers,
                data={'channel_id': channel_id}
            )

            unarchive_json = response.json()
            if response.ok and unarchive_json.get('ok'):
                print(f"Successfully unarchived channel: {channel_name}")
            else:
                print(f"Failed to unarchive channel {channel_name}: {unarchive_json.get('error')}")
    else:
        print(f"No channels archived in the last {minutes_to_check} minutes.")

except FileNotFoundError:
    print(f"Log file {log_file} not found.")
