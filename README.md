# Slack Channel Management

This project provides a set of scripts for managing Slack channels, including archiving channels without members and unarchiving channels archived in the last 10 minutes.

## Features

- List all public and private channels in a Slack workspace.
- Join channels with no members and archive them.
- Confirm with the user before archiving channels.
- Unarchive channels that were archived in the last 10 minutes.

## Requirements

Make sure you have Python 3.x installed. This project requires the following Python packages:

- `requests`
- `slack-bolt`
- `pytest`
- `flake8`
- `black`

You can install the dependencies using the following command:

```bash
pip install -r requirements.txt
````

## Features

1. **Create a Slack App**: Go to the [Slack API](https://api.slack.com/apps) and create a new app. Ensure you enable the necessary scopes:
   - `conversations:read`
   - `conversations:join`
   - `conversations:archive`
   - `admin.conversations.unarchive` (for unarchiving)

2. **Install the App**: Install the app in your Slack workspace and obtain the API token.

3. **Update the Token**: Replace the `SLACK_API_TOKEN` in the scripts with your actual Slack API token.

## Usage

1. **Archive Channels**: Run the script to find channels with no members and archive them. The user will be prompted for confirmation before archiving.

   ```bash
   python archive_channels.py
   ````
2. **Unarchive Recently Archived Channels**: To unarchive channels that were archived in the last 10 minutes, run:

    ````bash
    python unarchive.py
    ````
    
## Logging

The archiving script logs the archived channels into a file named `archived_channels_log.txt`. Each entry includes the following information:
- Channel ID
- Channel Name
- Timestamp of when it was archived

## Contributing

Feel free to submit issues or pull requests if you would like to contribute to this project. We welcome contributions and feedback to improve the functionality and usability of the scripts.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


