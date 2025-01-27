# telethon_bot

## Overview
This project is a simple Telegram bot built using the Telethon library. The bot responds with "Hello, World!" when a specific command is triggered.

## Prerequisites
- Python 3.7 or higher
- A Telegram account

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd telethon_bot
   ```

2. **Install dependencies**:
   Make sure you have `pip` installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Obtain API credentials**:
   - Go to [Telegram's API development tools](https://my.telegram.org/apps).
   - Create a new application to get your `API ID` and `API Hash`.

4. **Configure the bot**:
   Open `src/bot.py` and replace the placeholders with your `API ID`, `API Hash`, and bot token.

5. **Run the bot**:
   Execute the following command:
   ```
   python src/bot.py
   ```

## Usage
Once the bot is running, you can interact with it on Telegram by sending the command `/hello`. The bot will respond with "Hello, World!".

## License
This project is licensed under the MIT License.