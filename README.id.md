# NIM GAME — Minimax vs Alpha-Beta

Game Nim berbasis grafis yang dibangun dengan **Pygame**, mempertemukan pemain manusia melawan AI. AI menggunakan **Alpha-Beta Pruning** untuk menentukan gerakannya, sementara kedua algoritma **Minimax** dan **Alpha-Beta** dijalankan setiap giliran AI agar performanya bisa dibandingkan secara langsung.

## Apa itu Nim?

Nim adalah permainan strategi dua pemain di mana setiap pemain bergantian mengambil batu dari tumpukan (heap). Pemain yang mengambil **batu terakhir akan kalah** (konvensi misère).

## Fitur

- 5 tingkat kesulitan (Easy → Master) dengan ukuran heap dan kedalaman pencarian yang meningkat
- AI menggunakan Alpha-Beta Pruning untuk bermain secara optimal
- Panel statistik real-time yang membandingkan Minimax vs Alpha-Beta (waktu, node yang dikunjungi, kedalaman maksimum)
- Badge penghematan pruning yang menunjukkan berapa banyak node yang dilewati Alpha-Beta
- Efek partikel saat batu diambil
- Progres level dinamis — menang naik level, kalah turun level

## Tingkat Kesulitan

| Level  | Heap      | Kedalaman Maks |
|--------|-----------|----------------|
| Easy   | [2, 3]    | 4              |
| Normal | [3, 4, 5] | 6              |
| Hard   | [4, 5, 6] | 7              |
| Expert | [3, 5, 7] | 7              |
| Master | [4, 6, 8] | 8              |

## Kebutuhan

- Python 3.x
- Pygame

```bash
pip install pygame
```

## Font

Game ini menggunakan **VCR OSD Mono** untuk tampilan retro-nya. Jika font tidak terpasang, Pygame akan otomatis menggunakan font default sistem.

Untuk memasang font secara manual:
1. Download **VCR OSD Mono** dari [DaFont](https://www.dafont.com/vcr-osd-mono.font)
2. Ekstrak file `.ttf`
3. Install sesuai sistem operasi:
   - **Windows**: Klik kanan file `.ttf` → *Install*
   - **macOS**: Double-click file `.ttf` → *Install Font*
   - **Linux**: Salin file `.ttf` ke `~/.fonts/` lalu jalankan `fc-cache -fv`

## Cara Menjalankan

```bash
python "Nim Game.py"
```

## Cara Bermain

1. Klik sebuah **heap** untuk memilihnya
2. Klik **tombol angka** untuk mengambil sejumlah batu dari heap yang dipilih
3. AI akan merespons secara otomatis setelah giliranmu
4. Pemain yang mengambil **batu terakhir akan kalah**

## Kontrol

| Tombol       | Fungsi                                                    |
|--------------|-----------------------------------------------------------|
| NEW GAME     | Mulai ulang di level saat ini                        	   |
| RUN BOTH NOW | Jalankan kedua algoritma secara manual untuk dibandingkan |
| NEXT LEVEL   | Loncat ke tingkat kesulitan berikutnya                    |
| PREV LEVEL   | Kembali ke tingkat kesulitan sebelumnya                   |

## Struktur Proyek

```
Nim Game.py       # File utama — logika game, AI, dan rendering
```

## Implementasi AI

Kedua algoritma menggunakan **heuristik nilai Nim** (XOR dari semua heap) saat mencapai batas kedalaman:
- `minimax()` — Minimax biasa, dijalankan hanya untuk keperluan statistik
- `alphabeta()` — Alpha-Beta Pruning, digunakan sebagai keputusan gerak AI yang sebenarnya
