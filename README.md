
# Scam Detection Telegram Bot

This project creates a **Telegram bot** that detects scam messages in Telegram groups or channels. The bot utilizes **Elasticsearch** for storing and searching scam messages and uses **GPT-4** via the OpenAI API to analyze whether a message is a scam. The bot automatically notifies the admin in case of a scam message and can remove users involved in scam activities.

## Features
- **Message Detection**: Detects scam messages in Telegram groups or channels.
- **Elasticsearch Integration**: Uses Elasticsearch to store and search messages based on language-specific indexes.
- **GPT-4 Analysis**: Uses GPT-4 (OpenAI API) for advanced scam detection when no match is found in Elasticsearch.
- **Admin Notifications**: Notifies the admin when a scam message is detected.
- **User Removal**: Removes the user who sent a scam message (if possible).
- **Multi-language Support**: Supports scam detection in various languages using language-specific Elasticsearch indexes.

## Project Structure
1. **`telegram_bot.py`**: The main file that runs the Telegram bot and handles incoming messages.
2. **`elasticsearch_handler.py`**: Handles all operations related to Elasticsearch, including searching for scam messages, analyzing messages with GPT-4, and storing detected scam messages.
3. **`config.py`**: Contains configuration details, such as the Telegram bot token and Elasticsearch credentials.
4. **`requirements.txt`**: Lists the required Python dependencies for the project.

## Requirements

Before running the bot, ensure that you have the following:

- **Python 3.7+**
- **Elasticsearch instance** (locally or on a remote server)
- **OpenAI API Key** for GPT-4 integration
- **Telegram Bot Token** from [BotFather](https://core.telegram.org/bots#botfather)

You can install the required Python dependencies using:

```bash
pip install -r requirements.txt
```

## Setting Up

### Step 1: Configure Elasticsearch

1. Ensure that your Elasticsearch instance is running and accessible.
2. Set up Elasticsearch indexes for different languages (e.g., `scam-texts-uz`, `scam-texts-tr`).

### Step 2: Set Up OpenAI API

1. Sign up for an OpenAI account and get your API key from the [OpenAI dashboard](https://platform.openai.com/account/api-keys).
2. Set your OpenAI API key in the `config.py` file.

```python
# config.py
TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token'
ELASTICSEARCH_URL = 'https://localhost:9200'
ELASTICSEARCH_USERNAME = 'elastic'
ELASTICSEARCH_PASSWORD = 'your-elasticsearch-password'
OPENAI_API_KEY = 'your-openai-api-key'
```

### Step 3: Set Up Telegram Bot

1. Create a new bot on Telegram via [BotFather](https://core.telegram.org/bots#botfather).
2. Get your bot token and place it in `config.py` under the `TELEGRAM_BOT_TOKEN` field.

### Step 4: Run the Bot

Run the Telegram bot with:

```bash
python telegram_bot.py
```

The bot will start listening to incoming messages in groups or channels. If a scam message is detected, it will notify the admin and remove the user if possible.

## How It Works

1. **Language Detection**: When a message is received, the bot first detects the language of the message using the `langdetect` library.
2. **Search Elasticsearch**: The bot checks if the message is already stored in the corresponding language index in Elasticsearch. If found, it marks the message as a scam.
3. **GPT-4 Analysis**: If the message is not found in Elasticsearch, the bot uses GPT-4 (via the OpenAI API) to analyze the message and determine whether it's a scam.
4. **Store in Elasticsearch**: If the message is identified as a scam, the bot stores it in the appropriate language-specific Elasticsearch index.
5. **Notify Admin**: If a scam is detected, the bot notifies the admin (or first user) in the group and removes the user if applicable.

## Troubleshooting

- **Error: "Forbidden: bots can't send messages to bots"**: This error occurs if the bot attempts to send a message to another bot. Ensure that your admin is a real user, not a bot.
- **Elasticsearch Not Found**: Make sure Elasticsearch is running, and the correct indexes are created for the respective languages.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---