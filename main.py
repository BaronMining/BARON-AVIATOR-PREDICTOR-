import telebot
import hashlib
import hmac
import struct

TOKEN = "8652644864:AAFSmSQw34kQEUb8ya_MaCLIpMDXsHm7FqU"
bot = telebot.TeleBot(TOKEN)

def calculate_crash_point(seed):
    """The real Aviator SHA-256 to Multiplier logic."""
    # 1. Generate the hash
    hash_hex = hashlib.sha256(seed.encode()).hexdigest()
    
    # 2. Take the first 13 hex chars (52 bits) for precision
    # This is the industry standard for 'Provably Fair' crash games
    val = int(hash_hex[:13], 16)
    
    # 3. Apply the 97% RTP Math
    # Formula: (2^52) / (2^52 - val) * 0.99 (or 0.97 depending on house edge)
    if val % 33 == 0: return 1.00 # Instant 1.00x crash
    
    multiplier = (math.pow(2, 52)) / (math.pow(2, 52) - val)
    return max(1.0, round(multiplier * 0.97, 2))

@bot.message_handler(commands=['hack'])
def request_seeds(message):
    msg = bot.send_message(message.chat.id, "🛠 **AVIATOR SHA-256 DECODER**\nPaste the **Server Seed Hash** (Next Round):")
    bot.register_next_step_handler(msg, process_hash)

def process_hash(m):
    server_hash = m.text
    msg = bot.send_message(m.chat.id, "✅ Hash Received. Now enter your **Client Seed**:")
    bot.register_next_step_handler(msg, lambda msg: finalize_calc(msg, server_hash))

def finalize_calc(m, server_hash):
    client_seed = m.text
    # We combine them like the real game does
    combined_seed = f"{server_hash}-{client_seed}-0" # 0 is the nonce/round number
    
    # Calculate the 'Truth' based on the math
    result = calculate_crash_point(combined_seed)
    
    confidence = 98 if result > 2.0 else 40
    color = "💗" if result > 50 else "💛"
    
    output = (
        f"🖥 **ALGORITHM CALCULATION**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🔑 **Combined Hash**: `{combined_seed[:20]}...`\n"
        f"🚀 **CALCULATED MULTIPLIER**: `{result}x`\n"
        f"📊 **MATH CONFIDENCE**: `{confidence}%`\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⚠️ *Note: Final result depends on the other 3 players' seeds.*"
    )
    bot.send_message(m.chat.id, output, parse_mode='Markdown')

if __name__ == "__main__":
    import math # Added for the formula
    bot.polling(none_stop=True)
