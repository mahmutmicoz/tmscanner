# Brother MFC-L2716DW Tarayıcı

Ubuntu için Brother MFC-L2716DW tarayıcı uygulaması.

**Geliştirici:** Mahmut MİCOZKADIOĞLU

## Özellikler

- ADF (Otomatik Kağıt Besleyici) ve Düz Yüzey tarama
- PDF, PNG, JPEG formatlarında kayıt
- Anlık önizleme paneli
- Çok sayfalı belge desteği (◀ ▶ gezinme)
- 150 / 300 / 600 DPI çözünürlük seçimi

## Kurulum

### Kolay kurulum (betik ile)

```bash
git clone https://github.com/mahmutmicoz/brother-tarayici.git
cd brother-tarayici
chmod +x install.sh
./install.sh
```

### .deb paketi ile kurulum

```bash
sudo dpkg -i brother-tarayici_1.0.0_all.deb
sudo apt-get install -f
```

### Manuel çalıştırma

```bash
# Bağımlılıklar
sudo apt install python3-pil python3-pil.imagetk imagemagick sane-utils

# Çalıştır
python3 tarayici.py
```

## Gereksinimler

- Ubuntu 22.04 veya üzeri
- Brother MFC-L2716DW (USB bağlantı)
- Python 3.8+

## Lisans

MIT License
