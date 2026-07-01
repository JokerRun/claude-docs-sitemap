---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/vision-coordinates
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: f8628d06e07c2295ffdf7e62ee24a69071ab948b2affa17b2aac5e1a4c8ab7a3
---

# Koordinat dan bounding box

Bagaimana Claude mengubah ukuran gambar, dan cara bekerja dengan koordinat piksel yang dikembalikannya untuk bounding box, titik, dan elemen UI.

---

Claude dapat menemukan dan melabeli area dalam sebuah gambar (misalnya, mengembalikan "bounding box" (kotak pembatas) untuk tabel, kolom formulir, elemen grafik, atau komponen UI). Panduan ini membahas bagaimana Claude mengubah ukuran gambar sebelum memprosesnya dan cara bekerja dengan koordinat piksel yang dikembalikannya, sehingga kotak dan titik selaras dengan gambar asli Anda.

Anda akan memerlukan ini untuk pipeline OCR, ekstraksi formulir, penguraian grafik, penentuan lokasi elemen UI, dan tugas apa pun yang mengharuskan Anda bertindak pada area tertentu dari sebuah gambar. Untuk pengiriman gambar, format yang didukung, dan batas resolusi per model, lihat [Vision](/docs/id/build-with-claude/vision).

<Note>
  **Claude bekerja paling baik dengan koordinat piksel absolut.** Minta koordinat tersebut secara eksplisit dalam prompt Anda. Misalnya: *"Return the bounding box of each table as `[x1, y1, x2, y2]` in pixel coordinates."* Claude tidak bekerja dengan baik ketika Anda meminta koordinat yang dinormalisasi, misalnya: *"Return bounding box coordinates between `0` and `1000`."* Selalu minta koordinat piksel dan lakukan normalisasi di kode Anda sendiri jika diperlukan.
</Note>

Koordinat mengikuti konvensi gambar standar: titik asal `(0, 0)` berada di sudut kiri atas gambar, dengan x bertambah ke kanan dan y bertambah ke bawah. Koordinat yang dikembalikan Claude adalah posisi piksel pada gambar yang dilihat Claude: yaitu gambar Anda setelah Claude mengubah ukurannya agar sesuai dengan resolusi native model (lihat [Bagaimana Claude mengubah ukuran dan menambahkan padding pada gambar](#how-claude-resizes-and-pads-images)). Untuk mendapatkan koordinat yang dapat Anda gunakan secara langsung, lakukan pra-pengubahan ukuran pada gambar Anda sehingga koordinat dipetakan satu-ke-satu ke gambar yang Anda miliki (lihat [Ubah ukuran gambar Anda sebelum mengunggah](#resize-your-image-before-uploading)), atau skalakan ulang koordinat yang dikembalikan Claude (lihat [Skalakan ulang koordinat ketika Anda tidak dapat melakukan pra-pengubahan ukuran](#rescale-coordinates-when-you-cannot-pre-resize)).

<Note>
  Penalaran spasial Claude memiliki keterbatasan (lihat [Keterbatasan](/docs/id/build-with-claude/vision#limitations)). Akurasi koordinat paling baik ketika Anda menyatakan format koordinat yang diharapkan dalam prompt Anda dan memeriksa hasilnya secara visual sebelum memproses dalam skala besar. Untuk [dukungan PDF](/docs/id/build-with-claude/pdf-support), halaman di-rasterisasi menjadi gambar di sisi server dengan dimensi yang tidak Anda kendalikan, sehingga koordinat yang dikembalikan tidak dapat dipetakan kembali ke halaman secara andal. Untuk bekerja dengan koordinat pada konten PDF, rasterisasi halaman menjadi gambar sendiri dan gunakan pendekatan pra-pengubahan ukuran.
</Note>

## Bagaimana Claude mengubah ukuran dan menambahkan padding pada gambar

Claude mencari ukuran terbesar yang mempertahankan rasio aspek dan memenuhi kedua batas gambar model:

1. **Batas sisi:** tidak ada sisi yang melebihi panjang sisi maksimum (1568 px pada tier standar, 2576 px pada tier resolusi tinggi).
2. **Batas token visual:** biaya token gambar `⌈width / 28⌉ × ⌈height / 28⌉` tidak melebihi anggaran token visual model (1568 token pada tier standar, 4784 pada tier resolusi tinggi).

Lihat [Resolusi dan biaya token](/docs/id/build-with-claude/vision#evaluate-image-size) untuk mengetahui model mana yang berada di tier mana.

Untuk sebagian besar foto dan tangkapan layar, batas sisi adalah yang memicu pengubahan ukuran. Untuk dokumen potret, batas token visual biasanya terpicu lebih dulu, dan mengabaikannya adalah penyebab paling umum dari koordinat yang tidak selaras. Misalnya, halaman A4 yang dipindai pada 130 DPI berukuran 1075×1520 piksel: kedua sisinya di bawah 1568 px, tetapi biayanya `39 × 55 = 2145` token visual, sehingga Claude mengubah ukurannya menjadi 924×1307.

Claude kemudian menambahkan padding pada setiap gambar, baik yang diubah ukurannya maupun tidak, hingga kelipatan 28 piksel berikutnya pada sisi bawah dan kanan (924×1307 menjadi 924×1316 dalam contoh ini). Padding tidak berisi konten apa pun: Claude melihat gambar yang telah diberi padding, tetapi konten halaman hanya menempati area hasil pengubahan ukuran tanpa padding. **Selalu lakukan normalisasi atau penskalaan ulang berdasarkan dimensi hasil pengubahan ukuran, bukan dimensi setelah padding**; membagi dengan dimensi setelah padding akan menggeser setiap koordinat dengan jumlah kecil.

## Ubah ukuran gambar Anda sebelum mengunggah

Pendekatan yang paling andal adalah mengubah ukuran gambar Anda sendiri sebelum mengunggah, sehingga gambar yang Anda miliki persis sama dengan gambar yang dilihat Claude dan koordinat yang dikembalikan Claude tidak memerlukan konversi.

Implementasi referensi berikut menghitung ukuran persis yang digunakan Claude saat mengubah ukuran gambar:

```python
import math


def count_image_tokens(width: int, height: int) -> int:
    """Visual tokens consumed by an image: one token per 28x28 pixel patch."""
    return math.ceil(width / 28) * math.ceil(height / 28)


def resized_size(
    width: int,
    height: int,
    max_edge: int = 1568,
    max_tokens: int = 1568,
) -> tuple[int, int]:
    """The size Claude resizes an image to before padding.

    Defaults are for the standard resolution tier. For high-resolution-tier
    models, use max_edge=2576 and max_tokens=4784. Returns (width, height).
    Images that already fit within the limits are returned unchanged.
    """

    def fits(w: int, h: int) -> bool:
        return (
            math.ceil(w / 28) * 28 <= max_edge
            and math.ceil(h / 28) * 28 <= max_edge
            and count_image_tokens(w, h) <= max_tokens
        )

    if fits(width, height):
        return (width, height)
    if height > width:
        resized_h, resized_w = resized_size(height, width, max_edge, max_tokens)
        return (resized_w, resized_h)

    # Pencarian biner di sepanjang sisi panjang untuk ukuran terbesar yang mempertahankan
    # rasio aspek dan masih muat.
    aspect_ratio = width / height
    lo, hi = 1, width  # lo always fits; hi never fits
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if fits(mid, max(round(mid / aspect_ratio), 1)):
            lo = mid
        else:
            hi = mid
    return (lo, max(round(lo / aspect_ratio), 1))


# Contoh A4 dari "How Claude resizes and pads images":
print(resized_size(1075, 1520))  # (924, 1307)
```

1. Ubah ukuran gambar ke dimensi yang dikembalikan oleh `resized_size`. Jika gambar sudah sesuai dengan batas model, `resized_size` mengembalikan dimensinya tanpa perubahan dan tidak diperlukan pengubahan ukuran.
2. Kirim gambar yang telah diubah ukurannya ke API. Jangan tambahkan padding sendiri; Claude menangani padding, dan padding tidak menggeser titik asal koordinat.
3. Dalam prompt Anda, minta koordinat piksel secara eksplisit. Misalnya: *"Return the bounding box of each table as `[x1, y1, x2, y2]` in pixel coordinates."*
4. Gunakan koordinat yang dikembalikan secara langsung pada gambar yang Anda kirim. Jika Anda memerlukan koordinat yang dinormalisasi, bagi dengan dimensi gambar yang Anda kirim, bukan dengan dimensi gambar asli dan bukan dengan dimensi setelah padding.

## Skalakan ulang koordinat ketika Anda tidak dapat melakukan pra-pengubahan ukuran

Jika Anda tidak dapat melakukan pra-pengubahan ukuran (misalnya, ketika gambar berasal dari sistem upstream yang tidak dapat Anda modifikasi), gunakan `resized_size` dari [Ubah ukuran gambar Anda sebelum mengunggah](#resize-your-image-before-uploading) untuk mendapatkan kembali dimensi yang dilihat Claude, lalu petakan koordinat yang dikembalikan Claude ke koordinat yang dinormalisasi atau kembali ke gambar asli Anda. Pendekatan ini mengharuskan Anda mengetahui dimensi piksel dari gambar yang Anda unggah, sehingga tidak berlaku untuk unggahan PDF.

```python
def to_relative_coordinates(
    x: float,
    y: float,
    original_width: int,
    original_height: int,
    max_edge: int = 1568,
    max_tokens: int = 1568,
) -> tuple[float, float]:
    """Map a pixel coordinate returned by Claude to relative coordinates in [0, 1].

    Pass the dimensions of the image you uploaded. For high-resolution-tier
    models, use max_edge=2576 and max_tokens=4784.
    """
    resized_w, resized_h = resized_size(
        original_width, original_height, max_edge, max_tokens
    )
    return (x / resized_w, y / resized_h)


# Untuk menyatakan koordinat dalam ruang piksel gambar asli Anda, kalikan
# koordinat relatif dengan dimensi asli Anda:
# (rel_x * original_width, rel_y * original_height)
```

Padding hanya diterapkan pada sisi bawah dan kanan, sehingga titik asal tidak bergeser dan penskalaan ulang linear per sumbu sudah cukup.

## Terkait

* [Computer use tool](/docs/id/agents-and-tools/tool-use/computer-use-tool) mengharuskan tangkapan layar sudah sesuai dengan batas ukuran gambar (tangkapan layar yang terlalu besar akan ditolak, bukan diubah ukurannya); lihat panduan penskalaannya untuk pola pengubahan ukuran dan penskalaan koordinat di sisi klien.
* [Dukungan PDF](/docs/id/build-with-claude/pdf-support): halaman di-rasterisasi di sisi server dengan dimensi yang tidak Anda kendalikan, jadi rasterisasi halaman sendiri dan gunakan pendekatan pra-pengubahan ukuran ketika Anda memerlukan koordinat pada konten PDF.
