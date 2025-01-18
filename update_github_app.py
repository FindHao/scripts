"""
GitHub App Version Checker and Updater

This script checks and updates specified GitHub applications (currently supports Gitea and Beszel).
It compares the local installed version with the latest release version from GitHub,
and triggers an update if a newer version is available.

Features:
- Supports multiple applications (Gitea, Beszel)
- Automatic version comparison
- Force update option
- Pushover notifications for failed updates
- Executes corresponding update shell script when new version is found

Usage:
    python update_github_app.py --app [gitea|beszel] [--force]
Example crontab entry:
    # Check for updates daily at 3 AM
    0 3 * * * /usr/bin/python3 /path/to/update_github_app.py --app gitea
    0 3 * * * /usr/bin/python3 /path/to/update_github_app.py --app beszel

Environment variables:
    NOTIFICATION_TOKEN: Pushover API token
    NOTIFICATION_USER: Pushover user key
"""

import requests
import subprocess
import re
import os
import argparse

# get current script path
cur_path = os.path.dirname(os.path.realpath(__file__))

# get pushover token and user from environment variables
NOTIFICATION_TOKEN = os.getenv('NOTIFICATION_TOKEN', 'token')
NOTIFICATION_USER = os.getenv('NOTIFICATION_USER', 'user')

# send notification to pushover
# you can replace this with your own notification service
def send_notification(message):
    post_data = {"token": NOTIFICATION_TOKEN,
                 "user": NOTIFICATION_USER,
                 "message": message}
    r = requests.post(
        "https://api.pushover.net/1/messages.json", data=post_data)
    if r.status_code != 200:
        print("notification send error")
    else:
        print("successfully send notification")


def get_latest_github_release(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error on a bad response
    # Normalize version by removing 'v' prefix if present
    return response.json()['tag_name'].lstrip('v')

# Function to get the local Gitea version
def get_local_version(app_path, regex, app_name):
    result = subprocess.run(
        [app_path, '--version'], capture_output=True, text=True)
    version_output = result.stdout
    # Parse the version number from the output
    match = re.search(regex, version_output)
    if match:
        return match.group(1)  # This already has no 'v' prefix
    else:
        raise RuntimeError(f"Could not determine local {app_name} version")

# Main function to check versions and update if necessary


def parse_args():
    parser = argparse.ArgumentParser(description='Gitea version checker and updater')
    parser.add_argument('--app', 
                       default='gitea',
                       choices=['gitea', 'beszel'],
                       help='app name')
    parser.add_argument('--force',
                       action='store_true',
                       help='Force update even if versions match')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.app == 'gitea':
        url = 'https://api.github.com/repos/go-gitea/gitea/releases/latest'
        app_path = '/usr/local/bin/gitea'
        regex = r'Gitea version (\d+\.\d+\.\d+)'
    elif args.app == 'beszel':
        url = 'https://api.github.com/repos/henrygd/beszel/releases/latest'
        app_path = '/opt/beszel/beszel'
        regex = r'beszel version (\d+\.\d+\.\d+)'
    else:
        raise ValueError(f"Unsupported app: {args.app}")
    latest_version = get_latest_github_release(url)
    local_version = get_local_version(app_path, regex, args.app)

    print(f"Latest {args.app} version on GitHub: {latest_version}")
    print(f"Currently installed {args.app} version: {local_version}")

    if latest_version != local_version or args.force:
        print(f"New version found: v{latest_version}. Updating...")
        # Execute the bash script with the latest version as an argument
        update_script_path = os.path.join(cur_path, f'update_{args.app}.sh')
        process_result = subprocess.run(
            [update_script_path, latest_version], capture_output=True, text=True)

        if process_result.returncode == 0:
            print(f"Update {args.app} to v{latest_version} successful.")
        else:
            print(
                f"Update {args.app} to v{latest_version} failed with return code {process_result.returncode}.")
            print(f"Error message: {process_result.stderr}")
            send_notification(
                f"Failed to update {args.app} to v{latest_version}. Error message: {process_result.stderr}")
    else:
        print(f"No new version found. Your {args.app} is up to date.")

