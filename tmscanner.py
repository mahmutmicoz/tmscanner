#!/usr/bin/env python3
# TMScanner - Universal Scanner Application
# Developer: Mahmut MİCOZKADIOĞLU
# License: MIT

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import os
import glob
import threading
from datetime import datetime

__version__ = "2.1.0"
__author__ = "Mahmut MİCOZKADIOĞLU"
__app_name__ = "TMScanner"

# Sürüm notları — sürüm etiketine tıklayınca gösterilir
SURUM_NOTLARI = {
    "Türkçe": (
        "TMScanner v2.1.0 — Sürüm Notları\n"
        "\n"
        "• Düz yüzey (cam) tarama düzeltildi: artık escl arka ucu\n"
        "  kullanılıyor, sonsuz tarama / takılma sorunu giderildi.\n"
        "• Taradıkça ekleme: hem ADF hem düz yüzeyde her tarama\n"
        "  önizlemeye yeni sayfa olarak eklenir, sayfalar birikir.\n"
        "• \"Çoklu PDF Kaydet\": biriken tüm sayfaları tek ve\n"
        "  sıkıştırılmış bir PDF olarak kaydeder.\n"
        "• \"Temizle\": biriken sayfaları sıfırlar.\n"
        "• Artık gereksiz olan FORMAT seçici kaldırıldı (akış her\n"
        "  zaman çok sayfalı PDF üretir).\n"
        "• Uygulamalar menüsünde düzgün görünüm ve simge."
    ),
    "English": (
        "TMScanner v2.1.0 — Release Notes\n"
        "\n"
        "• Flatbed (platen) scanning fixed: now uses the escl\n"
        "  backend, no more endless-scan / freeze issue.\n"
        "• Scan-and-append: every scan (ADF or flatbed) adds a new\n"
        "  page to the preview; pages accumulate.\n"
        "• \"Save Multi-page PDF\": saves all collected pages into a\n"
        "  single compressed PDF.\n"
        "• \"Clear\": resets the collected pages.\n"
        "• Removed the now-redundant FORMAT selector (flow always\n"
        "  produces a multi-page PDF).\n"
        "• Proper application-menu entry and icon."
    ),
}

DEVICE_ADF     = "airscan:e0:Brother MFC-L2715DW series (USB)"
DEVICE_FLATBED = "escl:http://localhost:60000"
KAYIT_KLASORU = os.path.expanduser("~/Documents/TMScanner")

# Ghostscript PDF sıkıştırma kalitesi:
# /screen=küçük, /ebook=dengeli (önerilen), /printer=yüksek kalite
GS_KALITE = "/ebook"


def sikistir_pdf(kaynak: str, hedef: str) -> bool:
    """Ghostscript ile PDF'i sıkıştırır. Başarısız olursa orijinali kopyalar."""
    try:
        subprocess.run([
            "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={GS_KALITE}", "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={hedef}", kaynak
        ], check=True, capture_output=True)
        return True
    except Exception:
        import shutil
        shutil.copy2(kaynak, hedef)
        return False

KOYU  = "#1e1e2e"
PANEL = "#2a2a3e"
VURGU = "#7c6af7"
VURGU2 = "#5a9cf8"
METIN = "#e0e0f0"
METIN2 = "#9090b0"
YESIL = "#50fa7b"
KIRMIZI = "#ff5555"
GIRIS = "#3a3a55"

DILLER = {
    "Türkçe": {
        "baslik": "Tarayıcı Uygulaması",
        "kaynak": "KAYNAK",
        "adf": "ADF (Otomatik)",
        "duz": "Düz Yüzey",
        "cozunurluk": "ÇÖZÜNÜRLÜK",
        "renk_modu": "RENK MODU",
        "renkli": "Renkli",
        "gri": "Gri",
        "sb": "Siyah-Beyaz",
        "format": "FORMAT",
        "maks_sayfa": "MAKS SAYFA (ADF)",
        "klasor": "KAYIT KLASÖRÜ",
        "sec": "Seç",
        "hazir": "Hazır",
        "tara": "TARA",
        "dosya_ac": "Dosyayı Aç",
        "onizleme": "Önizleme",
        "onizleme_bos": "Tarama sonrası\nburada görünecek",
        "sayfa": "Sayfa",
        "taranıyor": "Taranıyor...",
        "kaydedildi": "Kaydedildi",
        "hata": "Hata",
        "hata_baslik": "Tarama Hatası",
        "kagit_yok": "Hiç sayfa taranamadı. Kağıt beslendi mi?",
        "dil": "DİL",
        "coklu": "Çoklu sayfa (tek PDF)",
        "sayfa_ekle": "➕ Sayfa Ekle",
        "bitir_kaydet": "📄 Çoklu PDF Kaydet",
        "biriken_temizle": "✗ Temizle",
        "biriken": "{n} sayfa biriktirildi",
        "tara_ilk": "İLK SAYFAYI TARA",
    },
    "English": {
        "baslik": "Scanner Application",
        "kaynak": "SOURCE",
        "adf": "ADF (Auto)",
        "duz": "Flatbed",
        "cozunurluk": "RESOLUTION",
        "renk_modu": "COLOR MODE",
        "renkli": "Color",
        "gri": "Grayscale",
        "sb": "Black & White",
        "format": "FORMAT",
        "maks_sayfa": "MAX PAGES (ADF)",
        "klasor": "SAVE FOLDER",
        "sec": "Browse",
        "hazir": "Ready",
        "tara": "SCAN",
        "dosya_ac": "Open File",
        "onizleme": "Preview",
        "onizleme_bos": "Preview will\nappear here",
        "sayfa": "Page",
        "taranıyor": "Scanning...",
        "kaydedildi": "Saved",
        "hata": "Error",
        "hata_baslik": "Scan Error",
        "kagit_yok": "No pages scanned. Is paper loaded?",
        "dil": "LANGUAGE",
        "coklu": "Multi-page (single PDF)",
        "sayfa_ekle": "➕ Add Page",
        "bitir_kaydet": "📄 Save Multi-page PDF",
        "biriken_temizle": "✗ Clear",
        "biriken": "{n} pages collected",
        "tara_ilk": "SCAN FIRST PAGE",
    },
    "Deutsch": {
        "baslik": "Scanner-Anwendung",
        "kaynak": "QUELLE",
        "adf": "ADF (Automatisch)",
        "duz": "Flachbett",
        "cozunurluk": "AUFLÖSUNG",
        "renk_modu": "FARBMODUS",
        "renkli": "Farbe",
        "gri": "Graustufen",
        "sb": "Schwarzweiß",
        "format": "FORMAT",
        "maks_sayfa": "MAX SEITEN (ADF)",
        "klasor": "SPEICHERORDNER",
        "sec": "Wählen",
        "hazir": "Bereit",
        "tara": "SCANNEN",
        "dosya_ac": "Datei öffnen",
        "onizleme": "Vorschau",
        "onizleme_bos": "Vorschau erscheint\nnach dem Scannen",
        "sayfa": "Seite",
        "taranıyor": "Wird gescannt...",
        "kaydedildi": "Gespeichert",
        "hata": "Fehler",
        "hata_baslik": "Scan-Fehler",
        "kagit_yok": "Keine Seiten gescannt. Ist Papier eingelegt?",
        "dil": "SPRACHE",
        "coklu": "Mehrseitig (eine PDF)",
        "sayfa_ekle": "➕ Seite hinzufügen",
        "bitir_kaydet": "📄 Mehrseitige PDF speichern",
        "biriken_temizle": "✗ Löschen",
        "biriken": "{n} Seiten gesammelt",
        "tara_ilk": "ERSTE SEITE SCANNEN",
    },
    "Français": {
        "baslik": "Application Scanner",
        "kaynak": "SOURCE",
        "adf": "ADF (Auto)",
        "duz": "Plateau",
        "cozunurluk": "RÉSOLUTION",
        "renk_modu": "MODE COULEUR",
        "renkli": "Couleur",
        "gri": "Niveaux de gris",
        "sb": "Noir et blanc",
        "format": "FORMAT",
        "maks_sayfa": "MAX PAGES (ADF)",
        "klasor": "DOSSIER",
        "sec": "Parcourir",
        "hazir": "Prêt",
        "tara": "NUMÉRISER",
        "dosya_ac": "Ouvrir le fichier",
        "onizleme": "Aperçu",
        "onizleme_bos": "L'aperçu apparaîtra\naprès la numérisation",
        "sayfa": "Page",
        "taranıyor": "Numérisation...",
        "kaydedildi": "Enregistré",
        "hata": "Erreur",
        "hata_baslik": "Erreur de numérisation",
        "kagit_yok": "Aucune page numérisée. Le papier est-il chargé?",
        "dil": "LANGUE",
        "coklu": "Multipage (un seul PDF)",
        "sayfa_ekle": "➕ Ajouter une page",
        "bitir_kaydet": "📄 Enregistrer PDF multipage",
        "biriken_temizle": "✗ Effacer",
        "biriken": "{n} pages collectées",
        "tara_ilk": "NUMÉRISER 1RE PAGE",
    },
    "Español": {
        "baslik": "Aplicación de Escáner",
        "kaynak": "FUENTE",
        "adf": "ADF (Auto)",
        "duz": "Plano",
        "cozunurluk": "RESOLUCIÓN",
        "renk_modu": "MODO DE COLOR",
        "renkli": "Color",
        "gri": "Escala de grises",
        "sb": "Blanco y negro",
        "format": "FORMATO",
        "maks_sayfa": "MÁX PÁGINAS (ADF)",
        "klasor": "CARPETA",
        "sec": "Elegir",
        "hazir": "Listo",
        "tara": "ESCANEAR",
        "dosya_ac": "Abrir archivo",
        "onizleme": "Vista previa",
        "onizleme_bos": "La vista previa\naparecerá aquí",
        "sayfa": "Página",
        "taranıyor": "Escaneando...",
        "kaydedildi": "Guardado",
        "hata": "Error",
        "hata_baslik": "Error de escaneo",
        "kagit_yok": "No se escaneó ninguna página. ¿Hay papel cargado?",
        "dil": "IDIOMA",
        "coklu": "Multipágina (un solo PDF)",
        "sayfa_ekle": "➕ Añadir página",
        "bitir_kaydet": "📄 Guardar PDF multipágina",
        "biriken_temizle": "✗ Borrar",
        "biriken": "{n} páginas recogidas",
        "tara_ilk": "ESCANEAR 1A PÁGINA",
    },
}

os.makedirs(KAYIT_KLASORU, exist_ok=True)


class TMScanner:
    def __init__(self, root):
        self.root = root
        self.root.geometry("920x600")
        self.root.minsize(750, 500)
        self.root.configure(bg=KOYU)

        self.aktif_dil = tk.StringVar(value="Türkçe")
        self.kaynak    = tk.StringVar(value="ADF")
        self.renk      = tk.StringVar(value="renkli")
        self.cozunurluk = tk.StringVar(value="300")
        self.sayfa_sayisi = tk.StringVar(value="10")
        self.durum     = tk.StringVar(value="")
        self.kayit_yolu = tk.StringVar(value=KAYIT_KLASORU)

        # Çoklu sayfa (düz yüzey) biriktirme durumu
        self.biriken = []          # biriktirilen PNG sayfa yolları
        self.biriken_klasor = None  # kalıcı geçici klasör

        self.son_dosyayi = None
        self.onizleme_sayfalar = []
        self.aktif_sayfa = 0
        self._tk_img = None
        self._widgets = {}  # dil değişiminde güncellenecek widget'lar

        self._stil_ayarla()
        self._arayuz_olustur()
        self._dil_guncelle()

    def _(self, key):
        return DILLER.get(self.aktif_dil.get(), DILLER["Türkçe"]).get(key, key)

    def _stil_ayarla(self):
        stil = ttk.Style()
        stil.theme_use("clam")
        stil.configure("TProgressbar", troughcolor=GIRIS, background=VURGU,
                       lightcolor=VURGU, darkcolor=VURGU)
        stil.configure("TSeparator", background="#444466")

    def _arayuz_olustur(self):
        # Pencere simgesi
        try:
            for yol in [
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png"),
                "/usr/share/tmscanner/icon.png",
            ]:
                if os.path.exists(yol):
                    img = tk.PhotoImage(file=yol)
                    self.root.iconphoto(True, img)
                    break
        except Exception:
            pass

        ana = tk.Frame(self.root, bg=KOYU)
        ana.pack(fill=tk.BOTH, expand=True)

        # ── Sol panel ──
        sol = tk.Frame(ana, bg=PANEL, width=320)
        sol.pack(side=tk.LEFT, fill=tk.Y)
        sol.pack_propagate(False)

        # Başlık
        self._baslik_frame = tk.Frame(sol, bg=VURGU, pady=14)
        self._baslik_frame.pack(fill=tk.X)
        tk.Label(self._baslik_frame, text=__app_name__,
                 bg=VURGU, fg="#ffffff", font=("Segoe UI", 16, "bold")).pack()
        self._w("alt_baslik", tk.Label(self._baslik_frame, text="",
                 bg=VURGU, fg="#d0c8ff", font=("Segoe UI", 9)))
        self._widgets["alt_baslik"].pack()

        # Kaydırılabilir ayarlar
        ayar_canvas = tk.Canvas(sol, bg=PANEL, highlightthickness=0)
        ayar_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        ic = tk.Frame(ayar_canvas, bg=PANEL, padx=20)
        ic_win = ayar_canvas.create_window((0, 0), window=ic, anchor=tk.NW)

        def _boyut(e):
            ayar_canvas.configure(scrollregion=ayar_canvas.bbox("all"))
            ayar_canvas.itemconfig(ic_win, width=ayar_canvas.winfo_width())
        ic.bind("<Configure>", _boyut)
        ayar_canvas.bind("<Configure>", lambda e: ayar_canvas.itemconfig(ic_win, width=e.width))
        for ev, d in [("<MouseWheel>", lambda e: ayar_canvas.yview_scroll(-1*(e.delta//120), "units")),
                      ("<Button-4>", lambda e: ayar_canvas.yview_scroll(-1, "units")),
                      ("<Button-5>", lambda e: ayar_canvas.yview_scroll(1, "units"))]:
            ayar_canvas.bind_all(ev, d)

        def baslik(key, parent=ic):
            lbl = tk.Label(parent, text="", bg=PANEL, fg=METIN2, font=("Segoe UI", 8, "bold"))
            lbl.pack(anchor=tk.W, pady=(12, 2))
            self._widgets[key] = lbl

        def radio_grup(frame_key, secenekler_keys, degerler, degisken, parent=ic):
            f = tk.Frame(parent, bg=PANEL)
            f.pack(anchor=tk.W)
            self._widgets[frame_key] = {}
            for sk, deger in zip(secenekler_keys, degerler):
                rb = tk.Radiobutton(f, text="", variable=degisken, value=deger,
                                    bg=PANEL, fg=METIN, selectcolor=VURGU,
                                    activebackground=PANEL, activeforeground=METIN,
                                    font=("Segoe UI", 10), cursor="hand2")
                rb.pack(side=tk.LEFT, padx=(0, 8))
                self._widgets[frame_key][sk] = rb

        # Dil seçimi
        baslik("lbl_dil")
        dil_f = tk.Frame(ic, bg=PANEL)
        dil_f.pack(anchor=tk.W)
        dil_menu = tk.OptionMenu(dil_f, self.aktif_dil, *DILLER.keys(),
                                 command=lambda _: self._dil_guncelle())
        dil_menu.config(bg=GIRIS, fg=METIN, activebackground=VURGU,
                        activeforeground="#fff", relief="flat",
                        font=("Segoe UI", 10), highlightthickness=0)
        dil_menu["menu"].config(bg=GIRIS, fg=METIN, activebackground=VURGU,
                                activeforeground="#fff")
        dil_menu.pack(side=tk.LEFT)

        baslik("lbl_kaynak")
        radio_grup("rg_kaynak", ["adf", "duz"], ["ADF", "Flatbed"], self.kaynak)

        baslik("lbl_cozunurluk")
        radio_grup("rg_coz", ["150", "300", "600"],
                   ["150", "300", "600"], self.cozunurluk)

        baslik("lbl_renk")
        radio_grup("rg_renk", ["renkli", "gri", "sb"],
                   ["renkli", "gri", "sb"], self.renk)

        baslik("lbl_maks")
        sayfa_f = tk.Frame(ic, bg=PANEL)
        sayfa_f.pack(anchor=tk.W)
        tk.Spinbox(sayfa_f, from_=1, to=50, textvariable=self.sayfa_sayisi,
                   width=6, bg=GIRIS, fg=METIN, buttonbackground=GIRIS,
                   relief="flat", insertbackground=METIN,
                   font=("Segoe UI", 10)).pack(side=tk.LEFT)

        baslik("lbl_klasor")
        klas_f = tk.Frame(ic, bg=PANEL)
        klas_f.pack(fill=tk.X)
        tk.Entry(klas_f, textvariable=self.kayit_yolu, bg=GIRIS, fg=METIN,
                 insertbackground=METIN, relief="flat", font=("Segoe UI", 9),
                 width=22).pack(side=tk.LEFT, ipady=4)
        self._w("btn_sec", tk.Button(klas_f, text="", command=self._klasor_sec,
                bg=GIRIS, fg=METIN, relief="flat", cursor="hand2",
                font=("Segoe UI", 9), padx=6))
        self._widgets["btn_sec"].pack(side=tk.LEFT, padx=(4, 0), ipady=4)

        # Alt sabit panel
        alt = tk.Frame(sol, bg=PANEL)
        alt.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Frame(alt, bg="#444466", height=1).pack(fill=tk.X)

        self._w("lbl_durum", tk.Label(alt, textvariable=self.durum, bg=PANEL,
                fg=METIN2, font=("Segoe UI", 9), wraplength=280))
        self._widgets["lbl_durum"].pack(pady=(8, 2))

        self.ilerleme = ttk.Progressbar(alt, mode="indeterminate", length=270)
        self.ilerleme.pack(pady=4, padx=20)

        self._w("btn_tara", tk.Button(alt, text="", command=self._tara_baslat,
                bg=VURGU, fg="#ffffff", relief="flat",
                font=("Segoe UI", 13, "bold"), cursor="hand2",
                padx=30, pady=12,
                activebackground="#6a5ae0", activeforeground="#ffffff"))
        self._widgets["btn_tara"].pack(pady=6, fill=tk.X, padx=20)

        # Çoklu sayfa: Bitir/Temizle butonları (başta gizli)
        coklu_btn_f = tk.Frame(alt, bg=PANEL)
        self._widgets["coklu_btn_f"] = coklu_btn_f
        self._w("btn_bitir", tk.Button(coklu_btn_f, text="",
                command=self._coklu_bitir, bg=YESIL, fg="#ffffff",
                relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2",
                padx=8, pady=6, activebackground="#1e8e4e",
                activeforeground="#ffffff"))
        self._widgets["btn_bitir"].pack(side=tk.LEFT, expand=True, fill=tk.X,
                                        padx=(20, 4))
        self._w("btn_biriken_temizle", tk.Button(coklu_btn_f, text="",
                command=self._coklu_temizle, bg=GIRIS, fg=METIN2,
                relief="flat", font=("Segoe UI", 10), cursor="hand2",
                padx=8, pady=6))
        self._widgets["btn_biriken_temizle"].pack(side=tk.LEFT, padx=(0, 20))

        self._w("btn_dosya", tk.Button(alt, text="", command=self._son_dosyayi_ac,
                bg=GIRIS, fg=METIN2, relief="flat",
                font=("Segoe UI", 9), cursor="hand2",
                padx=10, pady=4, state=tk.DISABLED))
        self._widgets["btn_dosya"].pack(pady=(0, 4))

        surum_lbl = tk.Label(alt, text=f"v{__version__}  ·  {__author__}",
                             bg=PANEL, fg=METIN2, font=("Segoe UI", 7),
                             cursor="hand2")
        surum_lbl.pack(pady=(0, 6))
        surum_lbl.bind("<Button-1>", lambda _: self._surum_notlari_goster())

        # ── Sağ panel: önizleme ──
        sag = tk.Frame(ana, bg=KOYU)
        sag.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        oniz_ust = tk.Frame(sag, bg=KOYU, pady=10)
        oniz_ust.pack(fill=tk.X, padx=20)
        self._w("lbl_onizleme", tk.Label(oniz_ust, text="", bg=KOYU, fg=METIN,
                font=("Segoe UI", 11, "bold")))
        self._widgets["lbl_onizleme"].pack(side=tk.LEFT)

        cerceve = tk.Frame(sag, bg="#444466", padx=1, pady=1)
        cerceve.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        self.canvas = tk.Canvas(cerceve, bg="#12121e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self._canvas_boyut_degisti)
        self._w("canvas_text", None)

        nav = tk.Frame(sag, bg=KOYU)
        nav.pack(pady=(0, 12))
        self.onceki_btn = tk.Button(nav, text="◀", command=self._onceki_sayfa,
                                    bg=GIRIS, fg=METIN, relief="flat", width=3,
                                    cursor="hand2", state=tk.DISABLED)
        self.onceki_btn.pack(side=tk.LEFT)
        self.sayfa_label = tk.Label(nav, text="", bg=KOYU, fg=METIN2,
                                    font=("Segoe UI", 9), width=16)
        self.sayfa_label.pack(side=tk.LEFT, padx=8)
        self.sonraki_btn = tk.Button(nav, text="▶", command=self._sonraki_sayfa,
                                     bg=GIRIS, fg=METIN, relief="flat", width=3,
                                     cursor="hand2", state=tk.DISABLED)
        self.sonraki_btn.pack(side=tk.LEFT)

    def _w(self, key, widget):
        self._widgets[key] = widget
        return widget

    def _dil_guncelle(self):
        d = self.aktif_dil.get()
        t = DILLER.get(d, DILLER["Türkçe"])
        self.root.title(__app_name__)

        self._widgets["alt_baslik"].config(text=t["baslik"])
        self._widgets["lbl_dil"].config(text=t["dil"])
        self._widgets["lbl_kaynak"].config(text=t["kaynak"])
        self._widgets["lbl_cozunurluk"].config(text=t["cozunurluk"])
        self._widgets["lbl_renk"].config(text=t["renk_modu"])
        self._widgets["lbl_maks"].config(text=t["maks_sayfa"])
        self._widgets["lbl_klasor"].config(text=t["klasor"])
        self._widgets["btn_sec"].config(text=t["sec"])
        self._widgets["btn_tara"].config(text=t["tara"])
        self._widgets["btn_dosya"].config(text=t["dosya_ac"])
        self._widgets["lbl_onizleme"].config(text=t["onizleme"])
        self._widgets["btn_bitir"].config(text=t["bitir_kaydet"])
        self._widgets["btn_biriken_temizle"].config(text=t["biriken_temizle"])

        rg_k = self._widgets["rg_kaynak"]
        rg_k["adf"].config(text=t["adf"])
        rg_k["duz"].config(text=t["duz"])

        rg_c = self._widgets["rg_coz"]
        for dpi in ["150", "300", "600"]:
            rg_c[dpi].config(text=f"{dpi} DPI")

        rg_r = self._widgets["rg_renk"]
        rg_r["renkli"].config(text=t["renkli"])
        rg_r["gri"].config(text=t["gri"])
        rg_r["sb"].config(text=t["sb"])

        if not self.durum.get() or self.durum.get() in [
            v["hazir"] for v in DILLER.values()
        ]:
            self.durum.set(t["hazir"])

        # Canvas placeholder
        if not self.onizleme_sayfalar:
            self.canvas.delete("all")
            w = self.canvas.winfo_width() or 500
            h = self.canvas.winfo_height() or 480
            self.canvas.create_text(w//2, h//2, text=t["onizleme_bos"],
                                    fill=METIN2, font=("Segoe UI", 12),
                                    justify=tk.CENTER, tags="placeholder")

        # Sayfa etiketi
        if self.onizleme_sayfalar:
            toplam = len(self.onizleme_sayfalar)
            self.sayfa_label.config(
                text=f"{t['sayfa']} {self.aktif_sayfa + 1} / {toplam}")

    def _klasor_sec(self):
        secilen = filedialog.askdirectory(initialdir=self.kayit_yolu.get())
        if secilen:
            self.kayit_yolu.set(secilen)

    def _tara_baslat(self):
        self._widgets["btn_tara"].config(state=tk.DISABLED)
        self.ilerleme.start(10)
        t = DILLER.get(self.aktif_dil.get(), DILLER["Türkçe"])
        self.durum.set(t["taranıyor"])
        self._widgets["lbl_durum"].config(fg=VURGU2)
        threading.Thread(target=self._tara, daemon=True).start()

    def _tara(self):
        """Her tarama, sonucu önizlemeye/biriktirmeye ekler (ADF veya Düz Yüzey)."""
        try:
            zaman = datetime.now().strftime("%Y%m%d_%H%M%S")
            klasor = self.kayit_yolu.get()
            os.makedirs(klasor, exist_ok=True)
            kaynak = self.kaynak.get()
            coz = self.cozunurluk.get()
            renk_mod = self.renk.get()
            t = DILLER.get(self.aktif_dil.get(), DILLER["Türkçe"])

            renk_map = {"renkli": "Color", "gri": "Gray", "sb": "Gray"}
            renk_deger = renk_map.get(renk_mod, "Color")

            # Biriktirme klasörü (ilk taramada oluşturulur)
            if not self.biriken_klasor:
                self.biriken_klasor = os.path.join(klasor, f"_biriken_{zaman}")
                os.makedirs(self.biriken_klasor, exist_ok=True)

            gecici = os.path.join(self.biriken_klasor, f"_g_{zaman}")
            os.makedirs(gecici, exist_ok=True)

            if kaynak == "ADF":
                cmd = [
                    "scanimage",
                    f"--device={DEVICE_ADF}",
                    "--source=ADF",
                    f"--mode={renk_deger}",
                    f"--resolution={coz}",
                    "--format=png",
                    f"--batch={gecici}/page%03d.png",
                    f"--batch-count={self.sayfa_sayisi.get()}",
                ]
            else:
                cmd = [
                    "scanimage",
                    f"--device={DEVICE_FLATBED}",
                    "--source=Flatbed",
                    f"--mode={renk_deger}",
                    f"--resolution={coz}",
                    "--format=png",
                    f"--output-file={gecici}/page001.png",
                ]

            subprocess.run(cmd, capture_output=True)

            yeni = sorted(glob.glob(f"{gecici}/page*.png"))
            if not yeni:
                raise Exception(t["kagit_yok"])

            # Siyah-Beyaz: yazılım eşikleme
            if renk_mod == "sb":
                for s in yeni:
                    img = Image.open(s).convert("L")
                    img = img.point(lambda p: 255 if p > 128 else 0, "1")
                    img.save(s)

            # Taranan sayfaları biriktirme listesine, sıralı isimle taşı
            for s in yeni:
                idx = len(self.biriken) + 1
                dst = os.path.join(self.biriken_klasor, f"sayfa{idx:03d}.png")
                os.rename(s, dst)
                self.biriken.append(dst)
            try:
                os.rmdir(gecici)
            except Exception:
                pass

            self.root.after(0, self._biriken_eklendi)

        except Exception as e:
            self.root.after(0, self._tara_hata, str(e))

    def _biriken_eklendi(self):
        """Tarama bitti; biriken sayfaları önizlemede göster, butonları aç."""
        self.ilerleme.stop()
        self._widgets["btn_tara"].config(state=tk.NORMAL)
        t = DILLER.get(self.aktif_dil.get(), DILLER["Türkçe"])
        self.durum.set(t["biriken"].format(n=len(self.biriken)))
        self._widgets["lbl_durum"].config(fg=YESIL)
        self._biriken_butonlari(True)
        self._onizleme_yukle(self.biriken)
        # En son taranan sayfaya atla
        if self.onizleme_sayfalar:
            self.aktif_sayfa = len(self.onizleme_sayfalar) - 1
            self._sayfa_goster()

    def _biriken_butonlari(self, goster):
        f = self._widgets["coklu_btn_f"]
        if goster:
            f.pack(fill=tk.X, pady=(0, 4), before=self._widgets["btn_dosya"])
        else:
            f.pack_forget()

    def _coklu_bitir(self):
        """Biriken tüm sayfaları tek PDF olarak kaydeder."""
        if not self.biriken:
            return
        self._widgets["btn_tara"].config(state=tk.DISABLED)
        self._widgets["btn_bitir"].config(state=tk.DISABLED)
        self.ilerleme.start(10)
        threading.Thread(target=self._coklu_kaydet, daemon=True).start()

    def _coklu_kaydet(self):
        try:
            t = DILLER.get(self.aktif_dil.get(), DILLER["Türkçe"])
            zaman = datetime.now().strftime("%Y%m%d_%H%M%S")
            klasor = self.kayit_yolu.get()
            ham_pdf = os.path.join(klasor, f"_ham_{zaman}.pdf")
            cikti = os.path.join(klasor, f"scan_{zaman}.pdf")
            subprocess.run(["convert"] + self.biriken + [ham_pdf], check=True)
            sikistir_pdf(ham_pdf, cikti)
            try:
                os.remove(ham_pdf)
            except Exception:
                pass
            self.son_dosyayi = cikti
            mesaj = f"{t['kaydedildi']}: {os.path.basename(cikti)}"
            self.root.after(0, self._coklu_kaydedildi, mesaj)
        except Exception as e:
            self.root.after(0, self._tara_hata, str(e))

    def _coklu_kaydedildi(self, mesaj):
        self.ilerleme.stop()
        self.durum.set(mesaj)
        self._widgets["lbl_durum"].config(fg=YESIL)
        self._widgets["btn_tara"].config(state=tk.NORMAL)
        self._widgets["btn_bitir"].config(state=tk.NORMAL)
        self._widgets["btn_dosya"].config(state=tk.NORMAL)
        self._coklu_temizle()  # kaydedildi; biriktirmeyi sıfırla

    def _coklu_temizle(self):
        """Biriken sayfaları ve önizlemeyi temizler."""
        for f in list(self.biriken):
            try:
                os.remove(f)
            except Exception:
                pass
        self.biriken = []
        if self.biriken_klasor:
            try:
                for f in glob.glob(f"{self.biriken_klasor}/*"):
                    try:
                        os.remove(f)
                    except Exception:
                        pass
                os.rmdir(self.biriken_klasor)
            except Exception:
                pass
            self.biriken_klasor = None
        self._biriken_butonlari(False)
        self.onizleme_sayfalar = []
        self.aktif_sayfa = 0
        self.sayfa_label.config(text="")
        self.onceki_btn.config(state=tk.DISABLED)
        self.sonraki_btn.config(state=tk.DISABLED)
        t = DILLER.get(self.aktif_dil.get(), DILLER["Türkçe"])
        w = self.canvas.winfo_width() or 500
        h = self.canvas.winfo_height() or 480
        self.canvas.delete("all")
        self.canvas.create_text(w // 2, h // 2, text=t["onizleme_bos"],
                                fill=METIN2, font=("Segoe UI", 12),
                                justify=tk.CENTER, tags="placeholder")

    def _surum_notlari_goster(self):
        d = self.aktif_dil.get()
        metin = SURUM_NOTLARI.get(d, SURUM_NOTLARI["English"])
        messagebox.showinfo(f"{__app_name__} v{__version__}", metin)

    def _tara_hata(self, mesaj):
        self.ilerleme.stop()
        t = DILLER.get(self.aktif_dil.get(), DILLER["Türkçe"])
        self.durum.set(f"{t['hata']}: {mesaj}")
        self._widgets["lbl_durum"].config(fg=KIRMIZI)
        self._widgets["btn_tara"].config(state=tk.NORMAL)
        messagebox.showerror(t["hata_baslik"], mesaj)

    def _onizleme_yukle(self, sayfalar):
        self.onizleme_sayfalar = []
        for yol in sayfalar:
            try:
                img = Image.open(yol)
                self.onizleme_sayfalar.append(img.copy())
            except Exception:
                pass
        if self.onizleme_sayfalar:
            self.aktif_sayfa = 0
            self._sayfa_goster()

    def _sayfa_goster(self):
        if not self.onizleme_sayfalar:
            return
        img = self.onizleme_sayfalar[self.aktif_sayfa].copy()
        w = self.canvas.winfo_width() or 500
        h = self.canvas.winfo_height() or 480
        img.thumbnail((w - 20, h - 20), Image.LANCZOS)
        self._tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(w // 2, h // 2, anchor=tk.CENTER, image=self._tk_img)
        t = DILLER.get(self.aktif_dil.get(), DILLER["Türkçe"])
        toplam = len(self.onizleme_sayfalar)
        self.sayfa_label.config(text=f"{t['sayfa']} {self.aktif_sayfa + 1} / {toplam}")
        self.onceki_btn.config(state=tk.NORMAL if self.aktif_sayfa > 0 else tk.DISABLED)
        self.sonraki_btn.config(state=tk.NORMAL if self.aktif_sayfa < toplam - 1 else tk.DISABLED)

    def _canvas_boyut_degisti(self, event):
        if self.onizleme_sayfalar:
            self._sayfa_goster()
        else:
            # Placeholder metnini ortala
            t = DILLER.get(self.aktif_dil.get(), DILLER["Türkçe"])
            self.canvas.delete("all")
            self.canvas.create_text(event.width // 2, event.height // 2,
                                    text=t["onizleme_bos"], fill=METIN2,
                                    font=("Segoe UI", 12), justify=tk.CENTER,
                                    tags="placeholder")

    def _onceki_sayfa(self):
        if self.aktif_sayfa > 0:
            self.aktif_sayfa -= 1
            self._sayfa_goster()

    def _sonraki_sayfa(self):
        if self.aktif_sayfa < len(self.onizleme_sayfalar) - 1:
            self.aktif_sayfa += 1
            self._sayfa_goster()

    def _son_dosyayi_ac(self):
        if self.son_dosyayi and os.path.exists(self.son_dosyayi):
            subprocess.Popen(["xdg-open", self.son_dosyayi])


if __name__ == "__main__":
    root = tk.Tk()
    app = TMScanner(root)
    root.mainloop()
