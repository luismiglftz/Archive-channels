import requests
import json
import time
from datetime import datetime

#Need admin permissions...

SLACK_API_TOKEN = 'xoxb-XXXXXXXXXXXXXXXXXXXXXX'

url_list_channels = 'https://slack.com/api/conversations.list'
url_join_channel = 'https://slack.com/api/conversations.join'
url_archive_channel = 'https://slack.com/api/conversations.archive'

headers = {
    'Authorization': f'Bearer {SLACK_API_TOKEN}',
    'Content-Type': 'application/x-www-form-urlencoded',
}

archived_channels_count = 0
channels_to_archive = []

log_file = "archived_channels_log.txt"

try:
    response = requests.get(
        url_list_channels,
        headers=headers,
        params={'types': 'public_channel,private_channel', 'limit': 1000},
    )

    if not response.ok:
        print(f'Error with API request: Status code {response.status_code}')
    else:
        response_json = response.json()
        if not response_json.get('ok'):
            print(f'Error in response: {response_json.get("error")}')
        else:
            channels = response_json.get('channels', [])
            print(f'{len(channels)} Channels found.')

            for channel in channels:
                if channel.get('is_archived', False):
                    archived_channels_count += 1
                elif channel['num_members'] == 0:
                    channels_to_archive.append(channel)

            print(f'Number of already archived channels: {archived_channels_count}')
            print(f'{len(channels_to_archive)} channels have no members and are not archived.')

            if channels_to_archive:
                user_input = input(f'Do you want to archive {len(channels_to_archive)} channels with 0 members? (yes/no): ').strip().lower()

                if user_input == 'yes':
                    #Archive channels without members
                    with open(log_file, 'a') as log:
                        for channel in channels_to_archive:
                            channel_id = channel['id']
                            channel_name = channel['name']
                            timestamp = datetime.now()

                            print(f'Trying to join the channel: {channel_name} ({channel_id})')

                            join_response = requests.post(
                                url_join_channel, headers=headers, data={'channel': channel_id}
                            )

                            join_json = join_response.json()
                            if join_response.ok and join_json.get('ok'):
                                print(f'Joined channel \'{channel_name}\'. Archiving...')

                                archive_response = requests.post(
                                    url_archive_channel,
                                    headers=headers,
                                    data={'channel': channel_id},
                                )
                                archive_json = archive_response.json()
                                if archive_response.ok and archive_json.get('ok'):
                                    print(f'Channel \'{channel_name}\' archived successfully.')

                                    # Log the archive action
                                    log.write(f"{channel_id},{channel_name},{timestamp}\n")
                                else:
                                    print(
                                        f'Error archiving the channel \'{channel_name}\': {archive_json.get("error")}'
                                    )
                            else:
                                print(
                                    f'Error joining the channel \'{channel_name}\': {join_json.get("error")}'
                                )
                else:
                    print('No channels were archived.')

except requests.exceptions.RequestException as e:
    print(f'An error occurred while making the API request: {e}')
except json.JSONDecodeError as e:
    print(f'Error parsing the JSON response: {e}')
