## Nedir?
Otomatik açılır kapı yönetim ve loglama sistemidir.

## Detaylı Açıklama
Bir personel takip sistemidir. Bir personel bir kapıdan ne zaman geçti, ne zaman çıkış yaptı (yani içeride ne kadar süre kaldı) gibi verileri loglama amacının yanı sıra ayrıca izin yönetim sistemi ile bir personelin giriş izini olmadığı kapılardan geçememesini de sağlamaktadır. Ayrıca ölçeklenebilir ve gelişime açık bir sistemdir.

## Kullanılan Teknolojiler ve Cihazlar
- NodeMCU ESP8266 mikrodenetleyici geliştirme kartı entegre WiFi modülüne sahip olduğu için tercih edildi ve gerekli şekilde programlandı.
- API ve yönetim paneli için Python dili ve Django kütüphanesi kullanıldı.

## Neler Kullanıldı?
- NodeMCU ESP8266 (Mikrodenetleyici Geliştirme Kartı)
- RFID RC522 (Kart Okuyucu) 
- Röle

## Devre Şeması ve Bağlantılar
| RFID RC522 | NodeMCU DevKit |
| ------ | ------ |
| SDA    | GPIO4  / D2 |
|  SCK   | GPIO14 / D5 |
| MOSI   | GPIO13 / D7 |
| MISO   | GPIO12 / D6 |
| IRQ    |     ---     |
| GND    | GND         |
| RST    | GPIO5 / D1  |
| 3.3V   | 3.3V        |

| Röle | NodeMCU DevKit |
| ------ | ------ |
| GND    | GND  |
| 3.3V   | 3.3V |
| S      | GPIO2 / D4 |

![Devre Şeması](https://raw.githubusercontent.com/prdsmehmetstc/iot-smart-door/master/iot-smart-door_circuit.png)

