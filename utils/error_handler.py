import telebot
import html

def format_error_log(error_msg, log_content=None):
    formatted = f"❌ <b>Deployment Error</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
    formatted += f"<b>Message:</b> <code>{html.escape(str(error_msg))}</code>\n\n"
    
    if log_content:
        formatted += "Your project has multiple errors, please fix:\n"
        formatted += f"```Error Log\n{html.escape(str(log_content))}\n```"
    
    return formatted

def send_error_to_user(bot, chat_id, error_msg, log_content=None):
    text = format_error_log(error_msg, log_content)
    try:
        bot.send_message(chat_id, text, parse_mode='HTML')
    except Exception as e:
        print(f"Failed to send error message: {e}")
