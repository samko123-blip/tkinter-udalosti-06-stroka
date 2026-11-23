import tkinter as tk
import random

# -------------------- NASTAVENIA HRY --------------------
SIRKA = 760
VYSKA = 470
VELKOST_STVORCA = 54
TRVANIE_HRY = 30
INTERVAL_PRESUNU = 850

FARBA_POZADIA = "#0b1020"
FARBA_PLOCHY = "#111a2e"
FARBA_TEXTU = "#f4f7ff"
FARBA_VEDLAJSIEHO_TEXTU = "#8fa2c7"
FARBA_AKCENTU = "#6c8cff"
FARBA_ZELENA = "#35d6a0"


class ChytStvorec:
    def __init__(self, okno):
        self.okno = okno
        self.okno.title("CHYŤ ŠTVOREC  |  Reflex Challenge")
        self.okno.geometry("900x880")
        self.okno.resizable(False, False)
        self.okno.configure(bg=FARBA_POZADIA)

        self.skore = 0
        self.zostava = TRVANIE_HRY
        self.bezi = False
        self.stvorec = None
        self.cislo_casovaca = None
        self.cislo_presunu = None
        self.cislo_animacie = None
        self.cas_zaciatku = None

        # Hlavny nadpis a kratky popis.
        hlavicka = tk.Frame(okno, bg=FARBA_POZADIA)
        hlavicka.pack(fill="x", padx=42, pady=(25, 18))

        tk.Label(
            hlavicka,
            text="REFLEX CHALLENGE",
            bg=FARBA_POZADIA,
            fg=FARBA_AKCENTU,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        tk.Label(
            hlavicka,
            text="Chyť štvorec.",
            bg=FARBA_POZADIA,
            fg=FARBA_TEXTU,
            font=("Segoe UI", 28, "bold")
        ).pack(anchor="w", pady=(2, 0))

        tk.Label(
            hlavicka,
            text="Otestuj svoje reflexy. Klikni na cieľ čo najviackrát za 30 sekúnd.",
            bg=FARBA_POZADIA,
            fg=FARBA_VEDLAJSIEHO_TEXTU,
            font=("Segoe UI", 11)
        ).pack(anchor="w", pady=(3, 0))

        # Panel so skore a casom.
        statistiky = tk.Frame(okno, bg=FARBA_POZADIA)
        statistiky.pack(fill="x", padx=42, pady=(0, 15))

        self.skore_karta = self.vytvor_kartu(
            statistiky, "ZÍSKANÉ BODY", "0", FARBA_AKCENTU
        )
        self.skore_karta.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.cas_karta = self.vytvor_kartu(
            statistiky, "ZOSTÁVAJÚCI ČAS", "30 s", FARBA_ZELENA
        )
        self.cas_karta.pack(side="left", fill="x", expand=True, padx=(8, 0))

        # Ukazovatel casu.
        self.progress = tk.Canvas(
            okno, width=816, height=8, bg="#202b43",
            highlightthickness=0, bd=0
        )
        self.progress.pack(padx=42, pady=(0, 16), anchor="w")
        self.progress_bar = self.progress.create_rectangle(
            0, 0, 816, 8, fill=FARBA_ZELENA, outline=""
        )

        # Herny priestor.
        obal = tk.Frame(okno, bg="#263451", padx=1, pady=1)
        obal.pack(padx=42, fill="both")

        self.platno = tk.Canvas(
            obal,
            width=SIRKA,
            height=VYSKA,
            bg=FARBA_PLOCHY,
            highlightthickness=0,
            cursor="crosshair"
        )
        self.platno.pack()

        self.vykresli_pozadie()

        # Spodny ovladaci panel.
        spodok = tk.Frame(okno, bg=FARBA_POZADIA)
        spodok.pack(fill="x", padx=42, pady=18)

        self.tlacidlo = tk.Button(
            spodok,
            text="▶  SPUSTIŤ HRU",
            command=self.start_hry,
            bg=FARBA_AKCENTU,
            fg="white",
            activebackground="#5475ed",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=24,
            pady=13,
            cursor="hand2",
            font=("Segoe UI", 11, "bold")
        )
        self.tlacidlo.pack(side="left")

        self.informacia = tk.Label(
            spodok,
            text="MEDZERNÍK  štart     •     ESC  koniec",
            bg=FARBA_POZADIA,
            fg=FARBA_VEDLAJSIEHO_TEXTU,
            font=("Segoe UI", 9)
        )
        self.informacia.pack(side="right", pady=12)

        # Callback pri kliknuti mysou a pri stlaceni klavesu.
        self.platno.bind("<Button-1>", self.kliknutie)
        self.okno.bind("<KeyPress>", lambda event: self.stlacenie_klavesu(event))
        self.okno.protocol("WM_DELETE_WINDOW", self.zatvorenie)

        self.okno.bind("<Enter>", lambda event: self.okno.focus_set())
        self.okno.focus_set()

    def vytvor_kartu(self, rodic, nazov, hodnota, farba):
        """Vytvori jednu kartu so statistikou."""
        karta = tk.Frame(rodic, bg=FARBA_PLOCHY, padx=20, pady=13)

        tk.Label(
            karta, text=nazov, bg=FARBA_PLOCHY,
            fg=FARBA_VEDLAJSIEHO_TEXTU,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        cislo = tk.Label(
            karta, text=hodnota, bg=FARBA_PLOCHY,
            fg=farba, font=("Segoe UI", 23, "bold")
        )
        cislo.pack(anchor="w", pady=(2, 0))

        karta.hodnota = cislo
        return karta

    def vykresli_pozadie(self):
        """Vykresli jemnu mriezku a dekoracne body na hernom platne."""
        for x in range(0, SIRKA, 40):
            self.platno.create_line(
                x, 0, x, VYSKA, fill="#18243b", width=1, tags="pozadie"
            )
        for y in range(0, VYSKA, 40):
            self.platno.create_line(
                0, y, SIRKA, y, fill="#18243b", width=1, tags="pozadie"
            )

        for _ in range(28):
            x = random.randint(8, SIRKA - 8)
            y = random.randint(8, VYSKA - 8)
            self.platno.create_oval(
                x, y, x + 2, y + 2, fill="#34415d",
                outline="", tags="pozadie"
            )

        self.platno.tag_lower("pozadie")

    def start_hry(self):
        """Spusti novu hru a vynuluje predchadzajuce skore."""
        self.zrus_casovace()
        self.skore = 0
        self.zostava = TRVANIE_HRY
        self.bezi = True

        self.skore_karta.hodnota.config(text="0")
        self.cas_karta.hodnota.config(text="30 s", fg=FARBA_ZELENA)
        self.progress.coords(self.progress_bar, 0, 0, 816, 8)
        self.progress.itemconfig(self.progress_bar, fill=FARBA_ZELENA)

        self.platno.delete("herne")
        self.informacia.config(
            text="DOBRÁ PRÁCA! Klikaj na svietiaci štvorec.",
            fg=FARBA_ZELENA
        )
        self.tlacidlo.config(text="↻  REŠTARTOVAŤ HRU")
        self.presun_stvorca()
        self.odpocet()

    def presun_stvorca(self):
        """Presunie ciel na nahodne miesto v hernom platne."""
        if not self.bezi:
            return

        x = random.randint(12, SIRKA - VELKOST_STVORCA - 12)
        y = random.randint(12, VYSKA - VELKOST_STVORCA - 12)

        self.platno.delete("stvorec")

        # Jemny farebny tien a zaobleny vizualny ciel.
        self.platno.create_rectangle(
            x - 5, y - 5,
            x + VELKOST_STVORCA + 5, y + VELKOST_STVORCA + 5,
            fill="#263f78", outline="", tags=("herne", "stvorec")
        )
        self.platno.create_rectangle(
            x, y,
            x + VELKOST_STVORCA, y + VELKOST_STVORCA,
            fill=FARBA_AKCENTU, outline="#a9baff",
            width=2, tags=("herne", "stvorec")
        )
        self.platno.create_rectangle(
            x + 9, y + 9,
            x + VELKOST_STVORCA - 9, y + VELKOST_STVORCA - 9,
            fill="#91a6ff", outline="", tags=("herne", "stvorec")
        )

        # Automaticky presun ciela po kratkom case.
        if self.cislo_presunu is not None:
            self.okno.after_cancel(self.cislo_presunu)
        self.cislo_presunu = self.okno.after(
            INTERVAL_PRESUNU, self.presun_stvorca
        )

    def kliknutie(self, event):
        """Skontroluje kliknutie; event.x a event.y su suradnice mysi."""
        if not self.bezi:
            return

        objekty = self.platno.find_overlapping(
            event.x, event.y, event.x, event.y
        )

        if any("stvorec" in self.platno.gettags(objekt) for objekt in objekty):
            self.skore += 1
            self.skore_karta.hodnota.config(text=str(self.skore))
            self.presun_stvorca()

    def odpocet(self):
        """Kazdu sekundu aktualizuje zostavajuci cas a ukazovatel."""
        if not self.bezi:
            return

        if self.zostava > 0:
            self.zostava -= 1
            self.cas_karta.hodnota.config(text=f"{self.zostava} s")

            sirka = 816 * self.zostava / TRVANIE_HRY
            self.progress.coords(self.progress_bar, 0, 0, sirka, 8)

            if self.zostava <= 10:
                self.cas_karta.hodnota.config(fg="#ff6b7a")
                self.progress.itemconfig(self.progress_bar, fill="#ff6b7a")

            self.cislo_casovaca = self.okno.after(1000, self.odpocet)
        else:
            self.koniec_hry()

    def koniec_hry(self):
        """Zastavi hru a zobrazi vysledne skore."""
        self.bezi = False
        self.zrus_casovace()
        self.platno.delete("herne")

        self.platno.create_text(
            SIRKA // 2, 175,
            text="ČAS VYPRŠAL!",
            fill=FARBA_TEXTU,
            font=("Segoe UI", 28, "bold"),
            tags="herne"
        )
        self.platno.create_text(
            SIRKA // 2, 230,
            text=f"Získal si {self.skore} bodov",
            fill=FARBA_ZELENA,
            font=("Segoe UI", 20, "bold"),
            tags="herne"
        )
        self.platno.create_text(
            SIRKA // 2, 280,
            text="Klikni na tlačidlo a skús prekonať svoj rekord.",
            fill=FARBA_VEDLAJSIEHO_TEXTU,
            font=("Segoe UI", 11),
            tags="herne"
        )

        self.cas_karta.hodnota.config(text="0 s", fg="#ff6b7a")
        self.informacia.config(
            text=f"HRA UKONČENÁ  •  TVOJE SKÓRE: {self.skore}",
            fg=FARBA_AKCENTU
        )
        self.tlacidlo.config(text="↻  ZAHRAŤ ZNOVA")

    def stlacenie_klavesu(self, event):
        """Medzernik spusti hru a Escape zatvori okno; event.keysym urci klaves."""
        if event.keysym == "space" and not self.bezi:
            self.start_hry()
        elif event.keysym == "Escape":
            self.zatvorenie()

    def zrus_casovace(self):
        """Bezpecne zrusi naplanovane casovace."""
        if self.cislo_casovaca is not None:
            self.okno.after_cancel(self.cislo_casovaca)
            self.cislo_casovaca = None
        if self.cislo_presunu is not None:
            self.okno.after_cancel(self.cislo_presunu)
            self.cislo_presunu = None

    def zatvorenie(self):
        """Zastavi casovace a bezpecne zatvori aplikaciu."""
        self.bezi = False
        self.zrus_casovace()
        self.okno.destroy()


# Vytvorenie okna a spustenie hry.
okno = tk.Tk()
hra = ChytStvorec(okno)
okno.mainloop()
