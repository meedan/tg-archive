# Telegram Public Groups Archiving Tool

This repository contains a tool designed to archive messages from Telegram public groups. It utilizes the Telegram API for message retrieval.

Original Repo: https://github.com/knadh/tg-archive

## Usage Steps:

1. **Modify `config.json`:** 

    Update the `config.json` file with essential information:

    ```json
    {
        "telegram_api_id": "Your_API_ID",
        "telegram_api_hash": "Your_API_Hash",
        "phone_number": "+1xxxxxxxxxx",
        "fetching_limit": "Max_messages_to_fetch_across_all_batches",
        "fetching_batchsize": "Number_of_messages_to_fetch_in_one_batch (<2000)",
        "number_of_groups": "Specify_0_for_all_groups_in_the_txt_files",
        "start_date_str": "YYYY-MM-DD"
    }
    ```

    Ensure to replace `"Your_API_ID"`, `"Your_API_Hash"`, `"Max_messages_to_fetch_across_all_batches"`, `"Number_of_messages_to_fetch_in_one_batch"`, and other placeholders with your respective API credentials and desired limits for message retrieval.

2. **Run the Tool:**

    Begin by installing the source code on your local device by executing `pip install .`. Subsequently, run `python run.py`. The terminal will prompt you to enter the authentication code from Telegram.

3. **Accessing the Retrieved Data:**

    To review the fetched information, utilize `dbreader.ipynb`. Ensure the successful retrieval of data by checking `data/groupname/media` for all downloaded media files.

