import telebot
from telebot.types import Message
from config import BOT_TOKEN
from utils import load_user_data, save_user_data, extract_links, shorten_url

bot = telebot.TeleBot(BOT_TOKEN)

# Load user data
user_data = load_user_data()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    bot.reply_to(message, "Welcome to the URL Shortener Bot!\n"
                          "Use /setapi to set your API key.\n"
                          "Send me any text or message with links, and I'll shorten them!")

@bot.message_handler(commands=['setapi'])
def set_api(message: Message):
    """Command to set the user's API key."""
    user_data[message.chat.id] = {"api_key": None}
    save_user_data(user_data)
    bot.reply_to(message, "Please reply to this message with your API key.")

@bot.message_handler(func=lambda msg: msg.reply_to_message and "API key" in msg.reply_to_message.text)
def save_api_key(message: Message):
    """Save the user's API key."""
    api_key = message.text.strip()
    user_data[message.chat.id] = {"api_key": api_key}
    save_user_data(user_data)
    bot.reply_to(message, "Your API key has been saved!")

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    """Handle incoming messages and shorten URLs."""
    user_id = message.chat.id
    if user_id not in user_data or not user_data[user_id].get("api_key"):
        bot.reply_to(message, "You need to set your API key first using /setapi.")
        return

    api_key = user_data[user_id]["api_key"]
    urls = extract_links(message.text or "")
    if not urls:
        bot.reply_to(message, "No valid links found in the message.")
        return

    shortened_urls = []
    for url in urls:
        if not url.startswith("http"):
            url = f"https://{url}"
        shortened_url = shorten_url(api_key, url)
        shortened_urls.append(shortened_url)

    bot.reply_to(message, "\n".join(shortened_urls))

if __name__ == "__main__":
    bot.polling()
