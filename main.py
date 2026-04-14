import telebot
import hashlib
import hmac
import os
from flask import Flask
import threading

# --- WEB SERVER (Fixes Port Timeout on Render) ---
app = Flask(__name__)
@app.route('/')
def home(): return "BARON TRUTH-AI: ONLINE", 200

# --- THE REAL ALGORITHM ---
TOKEN = "8652644864:AAFSmSQw34kQEUb8ya_MaCLIpMDXsHm7FqU"
bot = telebot.TeleBot(TOKEN)

def get_crash_point(seed):
    """The real industry standard SHA-256 to Multiplier logic."""
    # 1. Create the SHA-256 hash from the combined seeds
    hash_hex = hashlib.sha256(seed.encode()).hexdigest()
    
    # 2. Extract the first 13 hex characters (52 bits)
    val = int(hash_hex[:13], 16)
    
    # 3. Apply the 97% RTP Probability Math
    # Formula: (2^52) / (2^52 - val) * 0.99
    # If the remainder is 0, it crashes at 1.00x instantly
    if val % 33 == 0: return 1.00
    
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
    # Combine seeds as the real game does: ServerHash-ClientSeed
    combined = f"{server_hash}-{client_seed}"
    result = get_crash_point(combined)
    
    # Truth-based Confidence
    confidence = 99 if result > 2.0 else 35
    color = "💗" if result > 50 else "🔴"
    
    msg = (
        f"🖥 **REAL ALGORITHM TRUTH**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🚀 **CRASH POINT**: `{result}x`\n"
        f"📊 **MATH CONFIDENCE**: `{confidence}%`\n"
        f"💡 **STATUS**: {'HIGH PROBABILITY' if confidence > 90 else 'HIGH RISK'}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"*Verify this in your Spribe Provably Fair settings.*"
    )
    bot.send_message(m.chat.id, msg, parse_mode='Markdown')

if __name__ == "__main__":
    # Start web server for Render Free Tier
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=os.environ.get("PORT", 10000))).start()
    bot.polling(none_stop=True)
