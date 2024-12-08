import telebot
from elasticsearch_handler import process_message
from config import TELEGRAM_BOT_TOKEN  # Only the bot token is needed now

# Initialize the bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_admins(chat_id):
    """
    Retrieve the list of admins in the group, excluding bots.
    Returns the admin user ID(s).
    """
    try:
        admins = bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins if not admin.user.is_bot]  # Exclude bots
        return admin_ids
    except Exception as e:
        print(f"Error fetching admins: {e}")
        return []

# Handle messages in group chat
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """
    Handles incoming messages from Telegram (both group and private).
    """
    user_message = message.text
    if not user_message:
        return  # Ignore non-text messages

    print(f"Received message: {user_message}")
    
    # Process the message with the handler
    result = process_message(user_message)
    
    # Reply to the user with the result
    response = f"Message Status: {result}"
    
    if result == "scam":
        # If scam detected, notify the admin and remove the user from the group
        admins = get_admins(message.chat.id)
        if admins:
            notify_admin(admins[0], message, user_message)  # Notify the first admin in the list
        ban_user(message)

    bot.reply_to(message, response)

def notify_admin(admin_id, message, user_message):
    """
    Notify the admin about a scam message detected in the group.
    """
    admin_message = f"Scam message detected!\nUser: {message.from_user.username}\nMessage: {user_message}"
    
    # Send a message to the admin's chat
    bot.send_message(admin_id, admin_message)

def ban_user(message):
    """
    Ban a user from the group who sent the scam message.
    """
    try:
        bot.kick_chat_member(message.chat.id, message.from_user.id)
        bot.unban_chat_member(message.chat.id, message.from_user.id)  # Unban the user immediately after kicking
        print(f"Banned user {message.from_user.username} from the group.")
    except Exception as e:
        print(f"Error banning user: {e}")

# Start polling
if __name__ == "__main__":
    print("Telegram bot is running...")
    bot.infinity_polling()
