#!/bin/bash
# Brother Tarayıcı - Kurulum Betiği
# Geliştirici: Mahmut MİCOZKADIOĞLU

set -e

echo "Brother Tarayıcı kuruluyor..."

# Bağımlılıkları kur
sudo apt-get install -y python3 python3-pil python3-pil.imagetk imagemagick sane-utils

# Program dosyasını kopyala
sudo mkdir -p /usr/share/brother-tarayici
sudo cp tarayici.py /usr/share/brother-tarayici/tarayici.py

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
