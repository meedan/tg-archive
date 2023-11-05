import os
from telethon.sync import TelegramClient
from telethon.errors import PhoneMigrateError

# Initialize session and phone number variables
session_name = "session"
phone_number = None

# Function to authenticate the user and store the session
def authenticate():
    global phone_number
    api_id = os.environ.get("telegram_api_id")
    api_hash = os.environ.get("telegram_api_hash")

    if not phone_number:
        phone_number = input("Please enter your phone (or bot token): ")

    try:
        client = TelegramClient(session_name, api_id, api_hash)
        client.start(phone_number)
        return client
    except PhoneMigrateError as e:
        # Handle phone number migration to a new data center
        client.disconnect()
        phone_number = None
        return authenticate()

# Authenticate and store the session
client = authenticate()


import subprocess
import re
import shutil
import os

# List of group_names
group_names = ["osama1984osama", "moigovps", "newpress1"]


# Loop through the list of group_names
for group_name in group_names:
    # Delete the directory if it exists
    if os.path.exists(group_name):
        shutil.rmtree(group_name)

    # Create a new site and edit config.yaml
    subprocess.run(["tg-archive", "--new", f"--path={group_name}"])

    # Copy the session file to the group_name directory
    session_file = f"{session_name}.session"
    shutil.copy(session_file, os.path.join(group_name, session_file))

    # Change the working directory to the created directory
    os.chdir(group_name)

    # Substitute the group field in config.yaml
    config_path = "config.yaml"
    with open(config_path, 'r') as config_file:
        config_content = config_file.read()
        # Use regular expressions to find and replace the group field
        config_content = re.sub(r'group: .*', f'group: "{group_name}"', config_content)

        # Update fetch_batch_size and fetch_limit
        config_content = re.sub(r'fetch_batch_size: 2000', 'fetch_batch_size: 10', config_content)
        config_content = re.sub(r'fetch_limit: 0', 'fetch_limit: 20', config_content)
    
    with open(config_path, 'w') as config_file:
        config_file.write(config_content)

    # Sync data into data.sqlite
    subprocess.run(["tg-archive", "--sync"])

    # Change the working directory back to the previous directory
    os.chdir("..")
    
    print("completed!!\n")

    # Build the static site
    # subprocess.run(["tg-archive", "--build"])
