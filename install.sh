#!/bin/bash
# Brother Tarayıcı - Kurulum Betiği
# Geliştirici: Mahmut MİCOZKADIOĞLU

set -e

echo "Brother Tarayıcı kuruluyor..."

# Bağımlılıkları kur
sudo apt-get install -y python3 python3-pil python3-pil.imagetk imagemagick sane-utils

# Program dosyalarını kopyala
sudo mkdir -p /usr/share/brother-tarayici
sudo cp tarayici.py /usr/share/brother-tarayici/tarayici.py
sudo cp icon.png /usr/share/brother-tarayici/icon.png

# Simgeyi sistem ikonlarına da ekle
for size in 16 32 48 64 128 256; do
  if [ -f "icon_${size}.png" ]; then
    sudo mkdir -p /usr/share/icons/hicolor/${size}x${size}/apps
    sudo cp icon_${size}.png /usr/share/icons/hicolor/${size}x${size}/apps/brother-tarayici.png
  fi
done
sudo gtk-update-icon-cache /usr/share/icons/hicolor 2>/dev/null || true

# Başlatıcı oluştur
sudo tee /usr/bin/brother-tarayici > /dev/null << 'EOF'
#!/bin/bash
exec python3 /usr/share/brother-tarayici/tarayici.py "$@"
EOF
sudo chmod +x /usr/bin/brother-tarayici

# Masaüstü kısayolu
sudo cp usr/share/applications/brother-tarayici.desktop /usr/share/applications/
sudo update-desktop-database -q 2>/dev/null || true

echo ""
echo "Kurulum tamamlandı!"
echo "Uygulamayı başlatmak için: brother-tarayici"
echo "veya uygulama menüsünden 'Brother Tarayıcı' arayın."
