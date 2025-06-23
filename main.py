

main.py(import telebot
import requests
import os
import json

# 🔑 Replace with your real Telegram bot token from @BotFather
BOT_TOKEN = "7579053949:AAG5VKJQ9RMY7TM2RTbOtf-7FhOu7hz42wg"
bot = telebot.TeleBot(BOT_TOKEN)

# JSON file to store last node count
DATA_FILE = "last_node_count.json"

# Get current node count from Bitnodes
def fetch_node_count():
    url = "https://bitnodes.io/api/v1/snapshots/latest/"
    response = requests.get(url).json()
    return response['total_nodes']

# Read previously saved node count
def get_last_count():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f).get("count", None)
    return None

# Save the current count for next use
def save_current_count(count):
    with open(DATA_FILE, 'w') as f:
        json.dump({"count": count}, f)

# Decide LONG/SHORT/NEUTRAL based on node change
def determine_signal(current, previous):
    if previous is None:
        return "NEUTRAL ⚖\n(No previous data to compare)"
    if current > previous:
        return "LONG 📈\nNode count increased since last check."
    elif current < previous:
        return "SHORT 📉\nNode count decreased since last check."
    else:
        return "NEUTRAL ⚖\nNode count unchanged."

@bot.message_handler(commands=['start', 'help'])
def start_msg(message):
    bot.send_message(message.chat.id, "📡 Send /signal to get a trading signal based on Bitcoin node activity.")

@bot.message_handler(commands=['signal'])
def signal_handler(message):
    try:
        current_count = fetch_node_count()
        previous_count = get_last_count()
        signal = determine_signal(current_count, previous_count)

        # Save current count for next time
        save_current_count(current_count)

        response = (
            f"🌐 Current Bitcoin Full Nodes: {current_count}\n"
            f"📊 Signal: {signal}"
        )
        bot.send_message(message.chat.id, response)

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠ Error fetching data: {e}")

# Start polling the bot
bot.polling()
