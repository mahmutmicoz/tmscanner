#!/usr/bin/env python3
# Brother MFC-L2716DW Tarayıcı Uygulaması
# Geliştirici: Mahmut MİCOZKADIOĞLU

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import os
import glob
import threading
from datetime import datetime

__version__ = "1.0.0"
__author__ = "Mahmut MİCOZKADIOĞLU"

DEVICE = "airscan:e0:Brother MFC-L2715DW series (USB)"
KAYIT_KLASORU = os.path.expanduser("~/Belgeler/Taramalar")

KOYU = "#1e1e2e"
PANEL = "#2a2a3e"
VURGU = "#7c6af7"
VURGU2 = "#5a9cf8"
METIN = "#e0e0f0"
METIN2 = "#9090b0"
YESIL = "#50fa7b"
KIRMIZI = "#ff5555"
GIRIS = "#3a3a55"

os.makedirs(KAYIT_KLASORU, exist_ok=True)


class TarayiciApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brother Tarayıcı")
        self.root.geometry("900x580")
        self.root.minsize(750, 480)
        self.root.configure(bg=KOYU)

        self.kaynak = tk.StringVar(value="ADF")
        self.renk = tk.StringVar(value="Renkli")
        self.cozunurluk = tk.StringVar(value="300")
        self.format = tk.StringVar(value="pdf")
        self.sayfa_sayisi = tk.StringVar(value="10")
        self.durum = tk.StringVar(value="Hazır")
        self.kayit_yolu = tk.StringVar(value=KAYIT_KLASORU)

        self.son_dosyayi = None
        self.onizleme_sayfalar = []
        self.aktif_sayfa = 0
        self._tk_img = None

        self._stil_ayarla()
        self._arayuz_olustur()

    def _stil_ayarla(self):
        stil = ttk.Style()
        stil.theme_use("clam")

        stil.configure(".", background=KOYU, foreground=METIN, font=("Segoe UI", 10))
        stil.configure("TFrame", background=KOYU)
        stil.configure("Panel.TFrame", background=PANEL)

        stil.configure("TLabel", background=KOYU, foreground=METIN, font=("Segoe UI", 10))
        stil.configure("Title.TLabel", background=KOYU, foreground=METIN, font=("Segoe UI", 13, "bold"))
        stil.configure("Sub.TLabel", background=KOYU, foreground=METIN2, font=("Segoe UI", 8))
        stil.configure("Panel.TLabel", background=PANEL, foreground=METIN, font=("Segoe UI", 10))
        stil.configure("Baslik.TLabel", background=PANEL, foreground=METIN, font=("Segoe UI", 11, "bold"))

        stil.configure("TRadiobutton", background=KOYU, foreground=METIN,
                       indicatorcolor=VURGU, font=("Segoe UI", 10))
        stil.map("TRadiobutton", background=[("active", KOYU)], foreground=[("active", VURGU)])

        stil.configure("TSpinbox", fieldbackground=GIRIS, foreground=METIN,
                       background=GIRIS, arrowcolor=VURGU)

        stil.configure("TEntry", fieldbackground=GIRIS, foreground=METIN, insertcolor=METIN)

        stil.configure("Tara.TButton", background=VURGU, foreground="#ffffff",
                       font=("Segoe UI", 11, "bold"), padding=(20, 10), relief="flat")
        stil.map("Tara.TButton",
                 background=[("active", "#6a5ae0"), ("disabled", "#444466")],
                 foreground=[("disabled", METIN2)])

        stil.configure("Kucuk.TButton", background=GIRIS, foreground=METIN,
                       font=("Segoe UI", 9), padding=(8, 4), relief="flat")
        stil.map("Kucuk.TButton",
                 background=[("active", VURGU), ("disabled", GIRIS)],
                 foreground=[("disabled", METIN2)])

        stil.configure("TProgressbar", troughcolor=GIRIS, background=VURGU,
                       lightcolor=VURGU, darkcolor=VURGU)

        stil.configure("TSeparator", background="#444466")

    def _arayuz_olustur(self):
        # Pencere simgesi
        try:
            icon_yolu = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
            if not os.path.exists(icon_yolu):
                icon_yolu = "/usr/share/brother-tarayici/icon.png"
            if os.path.exists(icon_yolu):
                img = tk.PhotoImage(file=icon_yolu)
                self.root.iconphoto(True, img)
        except Exception:
            pass

        # Ana çerçeve
        ana = tk.Frame(self.root, bg=KOYU)
        ana.pack(fill=tk.BOTH, expand=True)

        # Sol panel (sabit genişlik)
        sol = tk.Frame(ana, bg=PANEL, width=310)
        sol.pack(side=tk.LEFT, fill=tk.Y)
        sol.pack_propagate(False)

        # Başlık alanı
        baslik_frame = tk.Frame(sol, bg=VURGU, pady=14)
        baslik_frame.pack(fill=tk.X)
        tk.Label(baslik_frame, text="Brother MFC-L2716DW",
                 bg=VURGU, fg="#ffffff", font=("Segoe UI", 13, "bold")).pack()
        tk.Label(baslik_frame, text="Tarayıcı Uygulaması",
                 bg=VURGU, fg="#d0c8ff", font=("Segoe UI", 9)).pack()

        # Kaydırılabilir ayarlar alanı
        ayar_canvas = tk.Canvas(sol, bg=PANEL, highlightthickness=0)
        ayar_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(sol, orient=tk.VERTICAL, command=ayar_canvas.yview)
        # Scrollbar sadece gerekince görünsün — mousewheel ile kaydır
        ayar_canvas.configure(yscrollcommand=scrollbar.set)

        ic = tk.Frame(ayar_canvas, bg=PANEL, padx=20)
        ic_win = ayar_canvas.create_window((0, 0), window=ic, anchor=tk.NW)

        def _ic_boyut(e):
            ayar_canvas.configure(scrollregion=ayar_canvas.bbox("all"))
            ayar_canvas.itemconfig(ic_win, width=ayar_canvas.winfo_width())
        ic.bind("<Configure>", _ic_boyut)
        ayar_canvas.bind("<Configure>", lambda e: ayar_canvas.itemconfig(ic_win, width=e.width))
        ayar_canvas.bind_all("<MouseWheel>", lambda e: ayar_canvas.yview_scroll(-1*(e.delta//120), "units"))
        ayar_canvas.bind_all("<Button-4>", lambda e: ayar_canvas.yview_scroll(-1, "units"))
        ayar_canvas.bind_all("<Button-5>", lambda e: ayar_canvas.yview_scroll(1, "units"))

        def bolum_baslik(parent, metin):
            tk.Label(parent, text=metin, bg=PANEL, fg=METIN2,
                     font=("Segoe UI", 8, "bold")).pack(anchor=tk.W, pady=(12, 2))

        def radio_satir(parent, secenekler, degisken):
            f = tk.Frame(parent, bg=PANEL)
            f.pack(anchor=tk.W)
            for metin, deger in secenekler:
                rb = tk.Radiobutton(f, text=metin, variable=degisken, value=deger,
                                    bg=PANEL, fg=METIN, selectcolor=VURGU,
                                    activebackground=PANEL, activeforeground=METIN,
                                    font=("Segoe UI", 10), cursor="hand2")
                rb.pack(side=tk.LEFT, padx=(0, 8))

        bolum_baslik(ic, "KAYNAK")
        radio_satir(ic, [("ADF (Otomatik)", "ADF"), ("Düz Yüzey", "Flatbed")], self.kaynak)

        bolum_baslik(ic, "ÇÖZÜNÜRLÜK")
        radio_satir(ic, [("150 DPI", "150"), ("300 DPI", "300"), ("600 DPI", "600")], self.cozunurluk)

        bolum_baslik(ic, "RENK MODU")
        radio_satir(ic, [("Renkli", "Renkli"), ("Gri", "Gri"), ("Siyah-Beyaz", "Siyah-Beyaz")], self.renk)

        bolum_baslik(ic, "FORMAT")
        radio_satir(ic, [("PDF", "pdf"), ("PNG", "png"), ("JPEG", "jpeg")], self.format)

        bolum_baslik(ic, "MAKS SAYFA (ADF)")
        sayfa_f = tk.Frame(ic, bg=PANEL)
        sayfa_f.pack(anchor=tk.W)
        tk.Spinbox(sayfa_f, from_=1, to=50, textvariable=self.sayfa_sayisi,
                   width=6, bg=GIRIS, fg=METIN, buttonbackground=GIRIS,
                   relief="flat", insertbackground=METIN,
                   font=("Segoe UI", 10)).pack(side=tk.LEFT)

        bolum_baslik(ic, "KAYIT KLASÖRÜ")
        klas_f = tk.Frame(ic, bg=PANEL)
        klas_f.pack(fill=tk.X)
        tk.Entry(klas_f, textvariable=self.kayit_yolu, bg=GIRIS, fg=METIN,
                 insertbackground=METIN, relief="flat", font=("Segoe UI", 9),
                 width=22).pack(side=tk.LEFT, ipady=4)
        tk.Button(klas_f, text="Seç", command=self._klasor_sec,
                  bg=GIRIS, fg=METIN, relief="flat", cursor="hand2",
                  font=("Segoe UI", 9), padx=6).pack(side=tk.LEFT, padx=(4, 0), ipady=4)

        # ── Alt sabit alan: durum + TARA butonu ──
        alt_panel = tk.Frame(sol, bg=PANEL)
        alt_panel.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Frame(alt_panel, bg="#444466", height=1).pack(fill=tk.X)

        self.durum_label = tk.Label(alt_panel, textvariable=self.durum, bg=PANEL,
                                    fg=METIN2, font=("Segoe UI", 9), wraplength=260)
        self.durum_label.pack(pady=(8, 2))

        self.ilerleme = ttk.Progressbar(alt_panel, mode="indeterminate", length=260,
                                        style="TProgressbar")
        self.ilerleme.pack(pady=4, padx=20)

        self.tara_btn = tk.Button(alt_panel, text="  TARA  ", command=self._tara_baslat,
                                  bg=VURGU, fg="#ffffff", relief="flat",
                                  font=("Segoe UI", 13, "bold"), cursor="hand2",
                                  padx=30, pady=12,
                                  activebackground="#6a5ae0", activeforeground="#ffffff")
        self.tara_btn.pack(pady=6, fill=tk.X, padx=20)

        self.son_dosya_btn = tk.Button(alt_panel, text="Dosyayı Aç", command=self._son_dosyayi_ac,
                                       bg=GIRIS, fg=METIN2, relief="flat",
                                       font=("Segoe UI", 9), cursor="hand2",
                                       padx=10, pady=4, state=tk.DISABLED)
        self.son_dosya_btn.pack(pady=(0, 4))

        tk.Label(alt_panel, text=f"v{__version__}  ·  {__author__}",
                 bg=PANEL, fg=METIN2, font=("Segoe UI", 7)).pack(pady=(0, 6))

        # Sağ panel: önizleme
        sag = tk.Frame(ana, bg=KOYU)
        sag.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0)

        oniz_baslik = tk.Frame(sag, bg=KOYU, pady=10)
        oniz_baslik.pack(fill=tk.X, padx=20)
        tk.Label(oniz_baslik, text="Önizleme", bg=KOYU, fg=METIN,
                 font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT)

        canvas_cerceve = tk.Frame(sag, bg="#444466", padx=1, pady=1)
        canvas_cerceve.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        self.canvas = tk.Canvas(canvas_cerceve, bg="#12121e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_text(
            300, 250, text="Tarama sonrası\nburada görünecek",
            fill=METIN2, font=("Segoe UI", 12), justify=tk.CENTER, tags="placeholder"
        )

        # Sayfa gezinme
        nav = tk.Frame(sag, bg=KOYU)
        nav.pack(pady=(0, 12))
        self.onceki_btn = tk.Button(nav, text="◀", command=self._onceki_sayfa,
                                    bg=GIRIS, fg=METIN, relief="flat", width=3,
                                    cursor="hand2", state=tk.DISABLED)
        self.onceki_btn.pack(side=tk.LEFT)
        self.sayfa_label = tk.Label(nav, text="", bg=KOYU, fg=METIN2,
                                    font=("Segoe UI", 9), width=14)
        self.sayfa_label.pack(side=tk.LEFT, padx=8)
        self.sonraki_btn = tk.Button(nav, text="▶", command=self._sonraki_sayfa,
                                     bg=GIRIS, fg=METIN, relief="flat", width=3,
                                     cursor="hand2", state=tk.DISABLED)
        self.sonraki_btn.pack(side=tk.LEFT)

    def _klasor_sec(self):
        secilen = filedialog.askdirectory(initialdir=self.kayit_yolu.get())
        if secilen:
            self.kayit_yolu.set(secilen)

    def _tara_baslat(self):
        self.tara_btn.config(state=tk.DISABLED)
        self.ilerleme.start(10)
        self.durum.set("Taranıyor...")
        self.durum_label.config(fg=VURGU2)
        threading.Thread(target=self._tara, daemon=True).start()

    def _tara(self):
        try:
            zaman = datetime.now().strftime("%Y%m%d_%H%M%S")
            klasor = self.kayit_yolu.get()
            os.makedirs(klasor, exist_ok=True)
            fmt = self.format.get()
            kaynak = self.kaynak.get()
            coz = self.cozunurluk.get()
            renk_mod = self.renk.get()

            # Tarayıcı yalnızca Color ve Gray destekliyor;
            # Siyah-Beyaz için gri taranıp sonra eşikleme uygulanıyor
            renk_map = {"Renkli": "Color", "Gri": "Gray", "Siyah-Beyaz": "Gray"}
            renk_deger = renk_map.get(renk_mod, "Color")

            gecici = os.path.join(klasor, f"_gecici_{zaman}")
            os.makedirs(gecici, exist_ok=True)

            cmd = [
                "scanimage",
                f"--device={DEVICE}",
                f"--source={kaynak}",
                f"--mode={renk_deger}",
                f"--resolution={coz}",
                "--format=png",
                f"--batch={gecici}/sayfa%03d.png",
            ]
            if kaynak == "ADF":
                cmd.append(f"--batch-count={self.sayfa_sayisi.get()}")

            subprocess.run(cmd, capture_output=True)

            sayfalar = sorted(glob.glob(f"{gecici}/sayfa*.png"))
            if not sayfalar:
                raise Exception("Hiç sayfa taranamadı. Kağıt beslendi mi?")

            # Siyah-Beyaz modu: gri görüntüyü eşikleyerek ikili (1-bit) yap
            if renk_mod == "Siyah-Beyaz":
                for s in sayfalar:
                    img = Image.open(s).convert("L")
                    img = img.point(lambda p: 255 if p > 128 else 0, "1")
                    img.save(s)

            if fmt == "pdf":
                cikti = os.path.join(klasor, f"tarama_{zaman}.pdf")
                subprocess.run(["convert"] + sayfalar + [cikti], check=True)
                onizleme_sayfalar = sayfalar[:]  # PNG'ler henüz silinmedi, önizleme için sakla
            elif fmt == "png":
                if len(sayfalar) == 1:
                    cikti = os.path.join(klasor, f"tarama_{zaman}.png")
                    os.rename(sayfalar[0], cikti)
                    sayfalar = [cikti]
                else:
                    new = []
                    for i, s in enumerate(sayfalar):
                        dst = os.path.join(klasor, f"tarama_{zaman}_{i+1:03d}.png")
                        os.rename(s, dst)
                        new.append(dst)
                    sayfalar = new
                    cikti = sayfalar[0]
                onizleme_sayfalar = sayfalar[:]
            elif fmt == "jpeg":
                new = []
                for i, s in enumerate(sayfalar):
                    dst = os.path.join(klasor, f"tarama_{zaman}_{i+1:03d}.jpg")
                    Image.open(s).convert("RGB").save(dst, "JPEG", quality=90)
                    os.remove(s)
                    new.append(dst)
                sayfalar = new
                cikti = sayfalar[0]
                onizleme_sayfalar = sayfalar[:]

            self.son_dosyayi = cikti

            # Geçici klasör temizliği (PDF için PNG'ler önizleme yüklendikten sonra silinecek)
            temizle = gecici if fmt == "pdf" else None
            self.root.after(0, self._tara_bitti, onizleme_sayfalar,
                            f"Kaydedildi: {os.path.basename(cikti)}", temizle)

        except Exception as e:
            self.root.after(0, self._tara_hata, str(e))

    def _tara_bitti(self, sayfalar, mesaj, temizle=None):
        self.ilerleme.stop()
        self.durum.set(mesaj)
        self.durum_label.config(fg=YESIL)
        self.tara_btn.config(state=tk.NORMAL)
        self.son_dosya_btn.config(state=tk.NORMAL)
        self._onizleme_yukle(sayfalar)
        if temizle:
            for f in glob.glob(f"{temizle}/*"):
                try:
                    os.remove(f)
                except Exception:
                    pass
            try:
                os.rmdir(temizle)
            except Exception:
                pass

    def _tara_hata(self, mesaj):
        self.ilerleme.stop()
        self.durum.set(f"Hata: {mesaj}")
        self.durum_label.config(fg=KIRMIZI)
        self.tara_btn.config(state=tk.NORMAL)
        messagebox.showerror("Tarama Hatası", mesaj)

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
        toplam = len(self.onizleme_sayfalar)
        self.sayfa_label.config(text=f"Sayfa {self.aktif_sayfa + 1} / {toplam}")
        self.onceki_btn.config(state=tk.NORMAL if self.aktif_sayfa > 0 else tk.DISABLED)
        self.sonraki_btn.config(state=tk.NORMAL if self.aktif_sayfa < toplam - 1 else tk.DISABLED)

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
    app = TarayiciApp(root)
    root.mainloop()
