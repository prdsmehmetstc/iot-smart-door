# Nedir?
Otomatik açılır kapı yönetim ve loglama sistemidir.

# Detaylı Açıklama
Bir personel takip sistemidir. Bir personel bir kapıdan ne zaman geçti, ne zaman çıkış yaptı (yani içeride ne kadar süre kaldı) gibi verileri loglama amacının yanı sıra ayrıca izin yönetim sistemi ile bir personelin giriş izini olmadığı kapılardan geçememesini de sağlamaktadır. Ayrıca ölçeklenebilir ve gelişime açık bir sistemdir.

# Aşamalar
- Arduino türevi olan NodeMCU ESP8266 geliştirme kartı entegre WiFi modülüne sahip olduğu için tercih edildi ve gerekli şekilde programlandı.
- API ve yönetim paneli için Python dili ve Django kütüphanesi kullanıldı.

# Neler Kullanıldı?
- NodeMCU ESP8266 (Mikrodenetleyici Geliştirme Kartı)
- RFID RC522 (Kart Okuyucu) 
- Röle
