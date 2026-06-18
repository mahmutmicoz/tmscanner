#!/bin/bash
# TMScanner - Kurulum Betiği
# Geliştirici: Mahmut MİCOZKADIOĞLU

set -e
echo "TMScanner kuruluyor..."

sudo apt-get install -y python3 python3-pil python3-pil.imagetk imagemagick sane-utils

sudo mkdir -p /usr/share/tmscanner
sudo cp tmscanner.py /usr/share/tmscanner/tmscanner.py
sudo cp icon.png /usr/share/tmscanner/icon.png

for size in 16 32 48 64 128 256; do
  [ -f "icon_${size}.png" ] && sudo mkdir -p /usr/share/icons/hicolor/${size}x${size}/apps && \
    sudo cp icon_${size}.png /usr/share/icons/hicolor/${size}x${size}/apps/tmscanner.png
done
sudo gtk-update-icon-cache /usr/share/icons/hicolor 2>/dev/null || true

sudo tee /usr/bin/tmscanner > /dev/null << 'SCRIPT'
#!/bin/bash
exec python3 /usr/share/tmscanner/tmscanner.py "$@"
SCRIPT
sudo chmod +x /usr/bin/tmscanner

sudo cp usr/share/applications/brother-tarayici.desktop /usr/share/applications/tmscanner.desktop
sudo update-desktop-database -q 2>/dev/null || true

echo ""
echo "Kurulum tamamlandı!"
echo "Başlatmak için: tmscanner"
