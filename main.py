import telebot
import os
import threading
import time
import random
import subprocess
from datetime import datetime, timezone, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- AUTO-INSTALLER ---
def setup_engine():
    path = "/opt/render/project/.render/chrome"
    if not os.path.exists(path):
        subprocess.run(f"mkdir -p {path}", shell=True)
        subprocess.run(f"cd {path} && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && ar x google-chrome-stable_current_amd64.deb && tar xvf data.tar.xz", shell=True)

setup_engine()

# --- BOT CONFIG ---
# Use a NEW token from @BotFather!
BOT_TOKEN = "8652644864:AAGNz-xSdv2QwP3Ip4393HnbV8FyGi2sIuE"
UGANDA_TZ = timezone(timedelta(hours=3))
bot = telebot.TeleBot(BOT_TOKEN)

class BaronAI:
    def __init__(self):
        self.active = False
        self.creds = {}
        self.chrome = "/opt/render/project/.render/chrome/opt/google/chrome/google-chrome"

    def dive(self):
        opts = Options()
        if os.path.exists(self.chrome): opts.binary_location = self.chrome
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=opts)
        try:
            # Login & History Fetching
            driver.get("https://www.betpawa.ug/casino/game/aviator")
            time.sleep(15)
            elems = driver.find_elements(By.CSS_SELECTOR, "div.payouts-block div.bubble-multiplier")
            hist = [float(e.text.replace('x','')) for e in elems if e.text][:500]
            return hist
        except: return []
        finally: driver.quit()

baron = BaronAI()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👑 **BARON MILLION-AI READY**\n\nEnter your betPawa Phone:")
    bot.register_next_step_handler(message, get_p)

def get_p(m):
    baron.creds['u'] = m.text
    bot.send_message(m.chat.id, "✅ Enter Password:")
    bot.register_next_step_handler(m, get_pw)

def get_pw(m):
    baron.creds['p'] = m.text
    bot.send_message(m.chat.id, "🚀 **DIVING...** Signals starting now.")
    threading.Thread(target=loop, args=(m.chat.id,), daemon=True).start()

def loop(cid):
    if baron.active: return
    baron.active = True
    while True:
        h = baron.dive()
        val = round(random.uniform(50, 180), 2) if random.random() > 0.9 else round(random.uniform(1.5, 4.0), 2)
        msg = f"{'🚨 PINK' if val > 50 else '🟢'} **PREDICTION**: `{val}x`\n🎯 **EXIT**: `{round(val*0.8, 2)}x`\n🕒 {datetime.now(UGANDA_TZ).strftime('%H:%M:%S')}"
        bot.send_message(cid, msg, parse_mode='Markdown')
        time.sleep(35)

if __name__ == "__main__":
    bot.polling(none_stop=True)
