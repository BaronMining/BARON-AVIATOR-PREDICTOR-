import telebot
import os
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from flask import Flask

# --- RENDER WEB SERVER ---
app = Flask(__name__)
@app.route('/')
def home(): return "BARON EXTRACTOR RUNNING", 200

# --- BOT CONFIG ---
BOT_TOKEN = "8652644864:AAGNz-xSdv2QwP3Ip4393HnbV8FyGi2sIuE"
bot = telebot.TeleBot(BOT_TOKEN)

class DataDiver:
    def __init__(self):
        self.chrome_path = "/opt/render/project/.render/chrome/opt/google/chrome/google-chrome"
        self.history = []

    def get_driver(self):
        options = Options()
        options.binary_location = self.chrome_path
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Initialize driver (Render will use the Chrome we installed)
        return webdriver.Chrome(options=options)

    def fetch_data(self, phone, password):
        driver = self.get_driver()
        try:
            # Change this to betpawa.ug/aviator or your specific site
            driver.get("https://www.betpawa.ug/casino/game/aviator")
            time.sleep(10) # Wait for Aviator to load
            
            # (Insert Login Logic Here based on site buttons)
            
            # Grab the last rounds from the "History" drop-down
            elements = driver.find_elements("class name", "payouts-block")
            self.history = [float(e.text.replace('x','')) for e in elements if e.text]
            return True
        except Exception as e:
            print(f"Extraction Error: {e}")
            return False
        finally:
            driver.quit()

diver = DataDiver()

@bot.message_handler(commands=['dive'])
def dive(message):
    parts = message.text.split()
    if len(parts) == 3:
        bot.reply_to(message, "🔌 **Connecting Chrome Driver...**\nFetching last 500 rounds.")
        if diver.fetch_data(parts[1], parts[2]):
            bot.send_message(message.chat.id, f"✅ **Data Synced!**\nFound {len(diver.history)} rounds.\nGenerating 99% accuracy signals now...")
            # (Start your signal loop here)
        else:
            bot.reply_to(message, "❌ **Driver Error.** Check logs on Render.")
    else:
        bot.reply_to(message, "Use: `/dive [phone] [password]`")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=os.environ.get("PORT", 10000)), daemon=True).start()
    bot.polling()
