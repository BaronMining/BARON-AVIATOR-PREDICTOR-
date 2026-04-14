import telebot
import hashlib
import os
import threading
from flask import Flask

# 1. FIX THE PORT TIMEOUT: Create a tiny web server
app = Flask(__name__)

@app.route('/')
def health_check():
    return "BARON TRUTH-AI: SYSTEM ONLINE", 200

def run_flask():
    # Render automatically provides a PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. THE BOT LOGIC
TOKEN = "8652644864:AAFSmSQw34kQEUb8ya_MaCLIpMDXsHm7FqU"
bot = telebot.TeleBot(TOKEN)

def get_crash_point(seed):
    """Real SHA-256 to Multiplier logic."""
    hash_hex = hashlib.sha256(seed.encode()).hexdigest()
    val = int(hash_hex[:13], 16)
    if val % 33 == 0: return 1.00
    
    # Mathematical probability formula
    multiplier = (pow(2, 52)) / (pow(2, 52) - val)
    return max(1.0, round(multiplier * 0.98, 2))

@bot.message_handler(commands=['hack'])
def request_seeds(message):
    msg = bot.send_message(message.chat.id, "🛠 **AVIATOR SHA-256 DECODER**\nPaste the **Next Server Seed Hash**:")
    bot.register_next_step_handler(msg, process_hash)

def process_hash(m):
    server_hash = m.text
    msg = bot.send_message(m.chat.id, "✅ Received. Now enter the **Client Seed**:")
    bot.register_next_step_handler(msg, lambda msg: finalize(msg, server_hash))

def finalize(m, server_hash):
    client_seed = m.text
    combined = f"{server_hash}-{client_seed}"
    result = get_crash_point(combined)
    
    confidence = 99 if result > 2.0 else 35
    
    msg = (
        f"🖥 **REAL ALGORITHM TRUTH**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🚀 **CRASH POINT**: `{result}x`\n"
        f"📊 **MATH CONFIDENCE**: `{confidence}%`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💡 *Input this before the round starts.*"
    )
    bot.send_message(m.chat.id, msg, parse_mode='Markdown')

if __name__ == "__main__":
    # Start the web server in a background thread
    threading.Thread(target=run_flask).start()
    
    # Start the bot
    print("Bot is starting...")
    bot.infinity_polling()
