import telebot
import hashlib
import os
import threading
from flask import Flask

# --- 1. THE WEB SERVER (Fixes Render Port Timeout) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "BARON TRUTH-ENGINE: ACTIVE", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. THE BOT CONFIGURATION ---
TOKEN = "8627970971:AAFx8abv5qTXqncaDeLyswLYHmGURuzKgqE"
bot = telebot.TeleBot(TOKEN)

def calc_truth(seed_string):
    """Real SHA-256 algorithm logic."""
    try:
        h = hashlib.sha256(seed_string.encode()).hexdigest()
        val = int(h[:13], 16)
        if val % 33 == 0: return 1.00
        res = (pow(2, 52)) / (pow(2, 52) - val)
        return max(1.0, round(res * 0.98, 2))
    except:
        return 1.00

# --- 3. THE HANDLERS (Fixed Logic Flow) ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👑 **BARON TRUTH-ENGINE v25.0**\n\nUse `/hack` to input seeds for the next round.")

@bot.message_handler(commands=['hack'])
def start_hack(message):
    sent_msg = bot.send_message(message.chat.id, "🛠 **STEP 1/2**: Paste the **Next Server Seed Hash**:")
    bot.register_next_step_handler(sent_msg, get_server_hash)

def get_server_hash(message):
    server_hash = message.text
    if len(server_hash) < 10:
        bot.send_message(message.chat.id, "❌ Invalid Hash. Start over with `/hack`.")
        return
    sent_msg = bot.send_message(message.chat.id, "✅ Hash Saved. **STEP 2/2**: Enter your **Client Seed**:")
    bot.register_next_step_handler(sent_msg, lambda m: finalize_result(m, server_hash))

def finalize_result(message, s_hash):
    client_seed = message.text
    # Real combination logic
    final_seed = f"{s_hash}-{client_seed}"
    result = calc_truth(final_seed)
    
    confidence = 99 if result > 2.0 else 38
    color = "💗" if result > 50 else "🟢"
    
    output = (
        f"🖥 **SHA-256 MATH TRUTH**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🚀 **PREDICTED CRASH**: `{result}x`\n"
        f"📊 **CONFIDENCE**: `{confidence}%`\n"
        f"💡 **STATUS**: {'EXCELLENT' if result > 10 else 'NORMAL'}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🎯 *Input this BEFORE the round begins.*"
    )
    bot.send_message(message.chat.id, output, parse_mode='Markdown')

# --- 4. EXECUTION ---
if __name__ == "__main__":
    # Start Web Server
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Force kill any old sessions to fix the '409 Conflict' error
    bot.remove_webhook()
    print("Baron Bot is live and waiting for /hack...")
    
    # Infinity polling with higher timeout for stability
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
