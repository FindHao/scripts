#!/usr/bin/env python3
"""
This script updates the desktop files of apps to use pure Wayland.
"""
import os


def update_desktop_file(file_path, update_string):
    """Update the desktop file at the given path with the specified update string."""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return

    with open(file_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()

        updated = False
        for line in lines:
            if line.startswith('Exec=') and update_string not in line:
                line = line.strip() + ' ' + update_string + '\n'
                updated = True
            file.write(line)

        if not updated:
            print(f"No updates needed for {file_path}.")
        else:
            print(f"Updated {file_path}.")


def main():
    # Map of apps and their update modes
    app_map = {
        "code": 3,
        "code-insiders": 3,
        "google-chrome": 1,
        "slack": 2
    }

    # Update strings for each mode
    update_strings = {
        1: '--gtk-version=4',
        2: '--ozone-platform=wayland --enable-features=UseOzonePlatform,WebRTCPipeWireCapturer',
        3: '--enable-features=UseOzonePlatform,WaylandWindowDecorations --ozone-platform=wayland'
    }

    # Directory containing desktop files
    desktop_files_dir = '/usr/share/applications/'
    # desktop_files_dir = '/tmp/tests'

    # Iterate over each app and update its desktop file
    for app, mode in app_map.items():
        file_path = os.path.join(desktop_files_dir, app + '.desktop')
        update_desktop_file(file_path, update_strings[mode])


if __name__ == "__main__":
    main()
