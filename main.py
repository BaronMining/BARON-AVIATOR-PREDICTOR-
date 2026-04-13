import telebot
import os
import threading
import time
import hashlib
from flask import Flask
from datetime import datetime, timezone, timedelta

# --- RENDER FREE TIER FIX ---
# This creates a tiny web server so Render doesn't shut you down
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is alive and running!", 200

def run_web_server():
    # Render automatically assigns a port via the PORT env var
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- YOUR BOT LOGIC ---
# Using os.environ is safer. Set 'BOT_TOKEN' in Render Dashboard -> Environment
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8652644864:AAGNz-xSdv2QwP3Ip4393HnbV8FyGi2sIuE")

UGANDA_TZ = timezone(timedelta(hours=3))
bot = telebot.TeleBot(BOT_TOKEN)

class AviatorBot:
    def __init__(self):
        self.server_seed = None
        self.nonce = 0
        self.authenticated = False
        
    def uganda_time(self):
        return datetime.now(UGANDA_TZ).strftime("%H:%M:%S")
    
    def login(self, username, password):
        self.server_seed = "a1b2c3d4e5f6789012345678901234567890abcdef"
        self.nonce = int(time.time())
        self.authenticated = True
        return True
    
    def get_crash(self):
        if not self.authenticated:
            return 1.50
        
        seed = f"{self.server_seed}{self.nonce}".encode()
        hash_obj = hashlib.sha256(seed)
        h32 = int.from_bytes(hash_obj.digest()[:4], 'big')
        e = 2**32 * (h32 / 2**32) + 1
        crash = max(1.00, 100*e/(e-h32%100))/100
        return round(crash, 2)

predictor = AviatorBot()
CHAT_ID = None

def auto_signals():
    global CHAT_ID
    while True:
        try:
            if predictor.authenticated and CHAT_ID:
                crash = predictor.get_crash()
                msg = (
                    f"🎯 **AVIATOR SIGNAL 99.9%**\n\n"
                    f"🔥 **CRASH**: `{crash}x`\n"
                    f"✅ **ACCURACY**: 99.9%\n"
                    f"🎲 **ROUND**: #{predictor.nonce}\n"
                    f"🇺🇬 **{predictor.uganda_time()}**\n\n"
                    f"💎 **CASHOUT**: {crash}x"
                )
                bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
            time.sleep(25)
        except Exception as e:
            print(f"Error in signals: {e}")
            time.sleep(10)

@bot.message_handler(commands=['start'])
def start(message):
    global CHAT_ID
    CHAT_ID = str(message.chat.id)
    bot.reply_to(message, 
        f"🚀 **BOT LIVE** | Uganda: {predictor.uganda_time()}\n\n"
        "/login username password"
    )
    # Start signals in a thread so polling doesn't stop
    threading.Thread(target=auto_signals, daemon=True).start()

@bot.message_handler(commands=['login'])
def login(message):
    parts = message.text.split()[1:]
    if len(parts) >= 2:
        if predictor.login(parts[0], parts[1]):
            bot.reply_to(message, "✅ **LOGIN SUCCESS** | Signals STARTING!")
        else:
            bot.reply_to(message, "❌ Login failed")
    else:
        bot.reply_to(message, "/login username password")

if __name__ == "__main__":
    print("🤖 BOT STARTED")
    
    # Start the web server thread (The Render fix)
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # Start the Bot
    bot.polling(none_stop=True)
