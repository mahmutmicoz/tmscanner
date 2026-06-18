# TMScanner

Universal scanner application for Linux (Ubuntu/Debian).

**Developer:** Mahmut MİCOZKADIOĞLU  
**License:** MIT

## Features

- ADF (Auto Document Feeder) and Flatbed scanning
- Color, Grayscale, Black & White modes
- PDF, PNG, JPEG output
- Live preview with multi-page navigation
- Multi-language: 🇹🇷 Turkish · 🇬🇧 English · 🇩🇪 German · 🇫🇷 French · 🇪🇸 Spanish

## Installation

### Option 1 — .deb package
```bash
sudo dpkg -i tmscanner_2.0.0_all.deb
sudo apt-get install -f
```

### Option 2 — install script
```bash
git clone https://github.com/mahmutmicoz/tmscanner.git
cd tmscanner
chmod +x install.sh
./install.sh
```

### Option 3 — run directly
```bash
sudo apt install python3-pil python3-pil.imagetk imagemagick sane-utils
python3 tmscanner.py
```

## Requirements

- Ubuntu 22.04+ / Debian 11+
- Python 3.8+
- SANE-compatible scanner
