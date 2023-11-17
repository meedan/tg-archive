import os
import json
import asyncio
import subprocess
import re
import shutil
from telethon.sync import TelegramClient
from telethon.errors import PhoneMigrateError
from util import read_group_names_txt
import nest_asyncio

nest_asyncio.apply()


# Load config file
with open('config.json', 'r') as json_file:
    config = json.load(json_file)


# Initialize session and phone number variables
session_name = "session"
phone_number = config["phone_number"]



# Function to authenticate the user and store the session
def authenticate():
    global phone_number
    api_id = config["telegram_api_id"]
    api_hash = config["telegram_api_hash"]

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


# List of group_names
num_groups = config["number_of_groups"]
if num_groups != 0:
    group_names = read_group_names_txt('chatnames.txt')[:num_groups]
else: group_names = read_group_names_txt('chatnames.txt')

# Create a 'data' directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Loop through the list of group_names+1
for group_name in group_names:
    # Create a directory under the 'data' directory for each group_name
    group_directory = os.path.join('data', group_name)

    # Delete the directory if it exists
    if os.path.exists(group_directory):
        shutil.rmtree(group_directory)

    # Create a new site and edit config.yaml
    subprocess.run(["tg-archive", "--new", f"--path={group_directory}"])

    # Copy the session file to the group_name directory
    session_file = f"{session_name}.session"
    shutil.copy(session_file, os.path.join(group_directory, session_file))

    # Change the working directory to the created directory
    os.chdir(group_directory)

    # Substitute the group field in config.yaml
    config_path = "config.yaml"
    with open(config_path, 'r') as config_file:
        config_content = config_file.read()
        # Use regular expressions to find and replace the group field
        config_content = re.sub(r'group: .*', f'group: "{group_name}"', config_content)

        # Update fetch_batch_size and fetch_limit
        config_content = re.sub(r'fetch_batch_size: 2000', f'fetch_batch_size: {config["fetching_batchsize"]}', config_content)
        config_content = re.sub(r'fetch_limit: 0', f'fetch_limit: {config["fetching_limit"]}', config_content)
    
    with open(config_path, 'w') as config_file:
        config_file.write(config_content)
        
    # Get the message id to start fetching by date
    date_str = config["date_str"]

    # Sync data into data.sqlite
    subprocess.run(["tg-archive", "-from-date", f"{date_str}", "--sync"])

    # Change the working directory back to the 'data' directory
    os.chdir('../..')
    
    print(f"Completed fetching group: {group_name}\n")

    # Build the static site
    # subprocess.run(["tg-archive", "--build"])
