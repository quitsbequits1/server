import os
import telebot
from flask import Flask, render_template, request

app = Flask(__name__)
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guvenlik-log', methods=['POST'])
def guvenlik_log():
    # Proxy arkasındaysa gerçek IP'yi al (X-Forwarded-For)
    ip_adresi = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_adresi:
        ip_adresi = ip_adresi.split(',')[0] # Eğer birden fazla IP varsa gerçek olanı (ilkini) alır
        
    cihaz_bilgisi = request.headers.get('User-Agent', 'Bilinmeyen Cihaz')

    # Telegram'a gidecek mesajın tasarımı
    mesaj = "🛡️ YENİ GÜVENLİK ONAYI 🛡️\n\n"
    mesaj += f"🌐 IP Adresi: {ip_adresi}\n"
    mesaj += f"📱 Cihaz/Tarayıcı: {cihaz_bilgisi}\n\n"
    mesaj += "Kullanıcı güvenlik sözleşmesini kabul etti."

    try:
        bot.send_message(CHAT_ID, mesaj)
    except Exception as e:
        print("Telegram hatası:", e)
        
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
