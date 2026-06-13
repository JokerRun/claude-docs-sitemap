---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/vision
fetched_at: 2026-06-13T03:15:40.418428Z
sha256: a809f9881d13e6936cbcd3bf3abce5ef20c5aba5118480595548d92660cca503
---

# Vision

Kemampuan vision Claude memungkinkannya untuk memahami dan menganalisis gambar, membuka kemungkinan menarik untuk interaksi multimodal.

---

Panduan ini menjelaskan cara bekerja dengan gambar di Claude, termasuk praktik terbaik, contoh kode, dan batasan yang perlu diperhatikan.

---

## Cara menggunakan vision \{#how-to-use-vision}

Gunakan kemampuan vision Claude melalui:

- [claude.ai](https://claude.ai/). Unggah gambar seperti Anda mengunggah file, atau seret dan lepas gambar langsung ke jendela obrolan.
- [Console Workbench](/workbench/). Tombol untuk menambahkan gambar muncul di kanan atas setiap blok pesan User.
- Permintaan API. Lihat contoh dalam panduan ini.

Beberapa gambar dapat disertakan dalam satu permintaan, yang akan dianalisis Claude secara bersamaan saat merumuskan responsnya. Ini dapat berguna untuk membandingkan atau mengontraskan gambar.

---

## Sebelum Anda mengunggah \{#before-you-upload}

### Batasan umum \{#general-limits}

Jumlah maksimal gambar per pesan atau permintaan adalah:
  - 20 per pesan di [claude.ai](https://claude.ai/).
  - 100 per permintaan di API, untuk model dengan jendela konteks 200k token.
  - 600 per permintaan di API, untuk semua model lainnya.

Dimensi maksimal per gambar adalah 8000x8000 px. Jika Anda mengirimkan lebih dari 20 gambar dalam satu permintaan API, batas ini dikurangi menjadi 2000x2000 px.

Ukuran maksimal per gambar adalah:
  - 10&nbsp;MB (dikodekan base64) saat menggunakan Claude API secara langsung.
  - 5&nbsp;MB (dikodekan base64) di Amazon Bedrock dan Vertex AI.
  - 10&nbsp;MB di [claude.ai](https://claude.ai/).

<Note>
Meskipun API mendukung hingga 600 gambar per permintaan, [batas ukuran permintaan](/docs/id/api/overview#request-size-limits) (32&nbsp;MB untuk endpoint standar; lebih rendah pada beberapa platform yang dioperasikan mitra, misalnya Amazon Bedrock dan Vertex AI) dapat tercapai terlebih dahulu. Untuk banyak gambar, pertimbangkan untuk mengunggah dengan [Files API](#files-api-image-example) dan mereferensikan melalui `file_id` agar payload permintaan tetap kecil.

Bahkan saat menggunakan Files API, permintaan dengan banyak gambar besar dapat gagal sebelum mencapai jumlah 600 gambar. Kurangi dimensi gambar atau ukuran file (misalnya, dengan downsampling) sebelum mengunggah (lihat [Mengevaluasi ukuran gambar](#evaluate-image-size)).
</Note>

### Mengevaluasi ukuran gambar \{#evaluate-image-size}

Claude melihat gambar dalam bentuk patch, bukan piksel. Setiap patch adalah blok 28×28 piksel dari gambar, yang disebut sebagai token visual. Oleh karena itu, sebuah gambar menghabiskan `⌈width / 28⌉ × ⌈height / 28⌉` token visual.

Jika Claude menerima gambar yang terlalu besar, Claude akan mengubah ukurannya. Resolusi gambar native maksimal adalah:

- Untuk Claude Fable 5 dan Claude Mythos 5: 4784 token, dan paling banyak 2576 piksel pada sisi terpanjang.
- Untuk Claude Opus 4.8: 4784 token, dan paling banyak 2576 piksel pada sisi terpanjang.
- Untuk Claude Opus 4.7: 4784 token, dan paling banyak 2576 piksel pada sisi terpanjang.
- Untuk model lainnya: 1568 token, dan paling banyak 1568 piksel pada sisi terpanjang.

<Note>
Jika gambar input Anda lebih besar dari resolusi native ini, gambar tersebut terlebih dahulu diubah ukurannya ke ukuran terbesar yang mungkin dengan mempertahankan rasio aspek. Semua gambar, baik yang diubah ukurannya maupun tidak, kemudian diberi padding pada tepi bawah dan kanan hingga kelipatan 28 piksel. Lihat [Cara Claude mengubah ukuran dan memberi padding pada gambar](#how-claude-resizes-and-pads-images) untuk aturan persisnya.

Saat meminta Claude untuk menghasilkan koordinat (titik, bounding box, dan sebagainya), Claude bekerja paling baik dengan koordinat piksel absolut yang dinyatakan terhadap gambar yang telah diubah ukurannya yang dilihatnya. Lihat [Bekerja dengan koordinat dan bounding box](#working-with-coordinates-and-bounding-boxes) untuk cara menanganinya.
</Note>

Untuk meminimalkan latensi dan menyederhanakan alur kerja berbasis koordinat, Anda sebaiknya mengubah ukuran gambar sebelum mengunggahnya.

### Menghitung biaya gambar \{#calculate-image-costs}

Setiap gambar yang Anda sertakan dalam permintaan ke Claude dihitung terhadap penggunaan token Anda. Untuk menghitung perkiraan biaya, kalikan jumlah token visual gambar (lihat [Mengevaluasi ukuran gambar](#evaluate-image-size)) dengan [harga per token dari model](https://claude.com/pricing) yang Anda gunakan.

Berikut adalah contoh tokenisasi dan perkiraan biaya untuk berbagai ukuran gambar dalam batasan ukuran API berdasarkan harga per token Claude Sonnet 4.6 sebesar $3 per juta token input:

| Ukuran gambar                 | \# Token     | Biaya / gambar | Biaya / 1k gambar |
| ----------------------------- | ------------ | -------------- | ----------------- |
| 200x200 px(0,04 megapiksel)   | 64           | \~$0,00019     | \~$0,19           |
| 1000x1000 px(1 megapiksel)    | 1296         | \~$0,0039      | \~$3,89           |
| 1092x1092 px(1,19 megapiksel) | 1521         | \~$0,0046      | \~$4,56           |
| 1920x1080 px(2,07 megapiksel) | 1560         | \~$0,0047      | \~$4,68           |
| 2000x1500 px(3 megapiksel)    | 1564         | \~$0,0047      | \~$4,69           |
| 3840x2160 px(8,29 megapiksel) | 1560         | \~$0,0047      | \~$4,68           |

Perhatikan bahwa tiga gambar terakhir melebihi resolusi native dan diperkecil sebelum diproses (masing-masing menjadi 1456x819 px, 1270x952 px, dan 1456x819 px), yang membatasi biaya tokennya. Gambar 4K tidak lebih mahal daripada gambar 1920x1080 karena keduanya diperkecil ke ukuran yang sama; resolusi tambahan dibuang.

#### Dukungan gambar resolusi tinggi \{#high-resolution-image-support-on-claude-opus-4-7}

Claude Opus 4.7 adalah model Claude pertama dengan dukungan gambar resolusi tinggi; Claude Opus 4.8, Claude Fable 5, Claude Mythos 5, dan model-model selanjutnya juga mendukungnya. Resolusi gambar maksimum adalah 2576 piksel pada sisi terpanjang, naik dari 1568 px pada model sebelumnya. Ini membuka peningkatan performa pada beban kerja yang berat secara visual dan sangat berharga untuk penggunaan komputer, pemahaman tangkapan layar, dan analisis dokumen.

Dukungan resolusi tinggi bersifat otomatis pada Claude Opus 4.7 dan model-model selanjutnya dan tidak memerlukan header beta atau opt-in dari sisi klien.

Gambar resolusi tinggi pada Claude Opus 4.7, Claude Opus 4.8, Claude Fable 5, dan Claude Mythos 5 dapat menggunakan hingga sekitar 3x lebih banyak token gambar dibandingkan model sebelumnya (4784 versus 1568 token per gambar). Jika Anda tidak memerlukan ketelitian tambahan, lakukan downsample pada gambar sebelum mengirim untuk mengontrol biaya token.

Berikut adalah ukuran gambar yang sama yang ditokenisasi untuk Claude Opus 4.7 dan Claude Opus 4.8, berdasarkan harga per token mereka sebesar $5 per juta token input:

| Ukuran gambar                 | \# Token     | Biaya / gambar | Biaya / 1k gambar |
| ----------------------------- | ------------ | -------------- | ----------------- |
| 200x200 px(0,04 megapiksel)   | 64           | \~$0,00032     | \~$0,32           |
| 1000x1000 px(1 megapiksel)    | 1296         | \~$0,0065      | \~$6,48           |
| 1092x1092 px(1,19 megapiksel) | 1521         | \~$0,0076      | \~$7,61           |
| 1920x1080 px(2,07 megapiksel) | 2691         | \~$0,013       | \~$13,46          |
| 2000x1500 px(3 megapiksel)    | 3888         | \~$0,019       | \~$19,44          |
| 3840x2160 px(8,29 megapiksel) | 4784         | \~$0,024       | \~$23,92          |

Hanya gambar terakhir yang melebihi batas yang lebih tinggi: gambar 4K diperkecil menjadi 2576x1449 px sebelum diproses. Dukungan resolusi tinggi menaikkan batas resolusi tetapi tidak menghapusnya; gambar yang lebih besar dari 2576 px pada sisi terpanjang (atau 4784 token visual) tetap diperkecil.

### Memastikan kualitas gambar \{#ensure-image-quality}

Saat memberikan gambar ke Claude, perhatikan hal-hal berikut untuk hasil terbaik:

- **Format gambar**: Gunakan format gambar yang didukung: JPEG, PNG, GIF, atau WebP.\
  Animasi tidak didukung, dan hanya frame pertama yang akan digunakan.
- **Kejernihan gambar**: Pastikan gambar jernih dan tidak terlalu buram atau pecah.
- **Teks**: Jika gambar berisi teks penting, pastikan teks tersebut terbaca dan tidak terlalu kecil. Hindari memotong konteks visual penting hanya untuk memperbesar teks.
- **Pengubahan ukuran**: Perhitungkan bahwa gambar Anda mungkin diubah ukurannya jika terlalu besar (lihat di atas); ini misalnya dapat membuat teks kurang terbaca. Pertimbangkan untuk mengubah ukuran gambar Anda terlebih dahulu, memotongnya, atau keduanya.
- **Kompresi gambar**: Mengompresi gambar sebelum mengirimnya, menggunakan format lossy seperti JPEG atau WebP (mode lossy), dapat mengurangi latensi dengan mengurangi ukuran permintaan. Namun, ini dapat menimbulkan artefak yang merugikan performa model, terutama ketika beberapa tahap kompresi diterapkan. Misalnya, kompresi JPEG yang berat dapat membuat teks sulit dibaca. Pastikan pengaturan kompresi Anda sesuai untuk tugas tersebut dengan memeriksa gambar aktual yang dikirim ke API.

---

## Bekerja dengan koordinat dan bounding box \{#working-with-coordinates-and-bounding-boxes}

Claude dapat menemukan dan memberi label pada region gambar (misalnya, mengembalikan bounding box untuk tabel, kolom formulir, elemen grafik, atau komponen UI).

<Note>
**Claude bekerja paling baik dengan koordinat piksel absolut.** Minta secara eksplisit dalam prompt Anda. Misalnya: *"Return the bounding box of each table as `[x1, y1, x2, y2]` in pixel coordinates."* Claude tidak bekerja dengan baik ketika Anda meminta koordinat yang dinormalisasi, misalnya: *"Return bounding box coordinates between `0` and `1000`."* Selalu minta koordinat piksel dan lakukan normalisasi dalam kode Anda sendiri jika diperlukan.
</Note>

Koordinat mengikuti konvensi gambar standar: titik asal `(0, 0)` adalah sudut kiri atas gambar, dengan x bertambah ke kanan dan y bertambah ke bawah. Koordinat yang dikembalikan Claude adalah posisi piksel dalam gambar yang dilihat Claude: gambar Anda setelah Claude mengubah ukurannya agar sesuai dengan resolusi native model (lihat [Cara Claude mengubah ukuran dan memberi padding pada gambar](#how-claude-resizes-and-pads-images)). Untuk mendapatkan koordinat yang dapat Anda gunakan secara langsung, ubah ukuran gambar Anda terlebih dahulu sehingga koordinat dipetakan satu-ke-satu ke gambar yang Anda miliki (lihat [Ubah ukuran gambar Anda sebelum mengunggah](#resize-your-image-before-uploading)), atau skalakan ulang koordinat yang dikembalikan Claude (lihat [Skalakan ulang koordinat ketika Anda tidak dapat mengubah ukuran terlebih dahulu](#rescale-coordinates-when-you-cannot-pre-resize)).

<Note>
Penalaran spasial Claude memiliki batasan (lihat [Batasan](#limitations)). Akurasi koordinat paling baik ketika Anda menyatakan format koordinat yang diharapkan dalam prompt Anda dan memeriksa hasil secara visual sebelum memproses dalam skala besar. Untuk [unggahan PDF](/docs/id/build-with-claude/pdf-support), halaman dirasterisasi menjadi gambar di sisi server pada dimensi yang tidak Anda kontrol, sehingga koordinat yang dikembalikan tidak dapat dipetakan kembali ke halaman secara andal. Untuk bekerja dengan koordinat pada konten PDF, rasterisasi halaman menjadi gambar sendiri dan gunakan pendekatan pengubahan ukuran terlebih dahulu.
</Note>

### Cara Claude mengubah ukuran dan memberi padding pada gambar \{#how-claude-resizes-and-pads-images}

Claude menemukan ukuran terbesar yang mempertahankan rasio aspek yang memenuhi kedua batas gambar model:

1. **Batas tepi:** tidak ada sisi yang melebihi panjang tepi maksimum (1568 px untuk sebagian besar model, 2576 px untuk Claude Opus 4.7 dan model-model selanjutnya).
2. **Batas token visual:** biaya token gambar `⌈width / 28⌉ × ⌈height / 28⌉` tidak melebihi anggaran token visual model (1568 token untuk sebagian besar model, 4784 untuk Claude Opus 4.7 dan model-model selanjutnya).

Untuk sebagian besar foto dan tangkapan layar, batas tepi adalah yang memicu pengubahan ukuran. Untuk dokumen potret, batas token visual biasanya terpicu terlebih dahulu, dan mengabaikannya adalah penyebab paling umum dari koordinat yang tidak selaras. Misalnya, halaman A4 yang dipindai pada 130 DPI adalah 1075×1520 piksel: kedua sisi di bawah 1568 px, tetapi menghabiskan `39 × 55 = 2145` token visual, sehingga Claude mengubah ukurannya menjadi 924×1307.

Claude kemudian memberi padding pada setiap gambar, baik yang diubah ukurannya maupun tidak, hingga kelipatan 28 piksel berikutnya pada tepi bawah dan kanan (924×1307 menjadi 924×1316 dalam contoh tersebut). Padding tidak berisi konten: Claude melihat gambar yang diberi padding, tetapi konten halaman hanya menempati region yang diubah ukurannya tanpa padding. **Selalu normalisasi atau skalakan ulang berdasarkan dimensi yang diubah ukurannya, bukan dimensi yang diberi padding**; membagi dengan dimensi yang diberi padding akan menskalakan setiap koordinat dengan jumlah kecil.

### Ubah ukuran gambar Anda sebelum mengunggah \{#resize-your-image-before-uploading}

Pendekatan paling andal adalah mengubah ukuran gambar Anda sendiri sebelum mengunggah, sehingga gambar yang Anda miliki persis sama dengan gambar yang dilihat Claude dan koordinat yang dikembalikan Claude tidak memerlukan konversi.

Implementasi referensi berikut menghitung ukuran persis yang digunakan Claude untuk mengubah ukuran gambar:

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

    Defaults are for most models. For Claude Opus 4.7 and later models, use
    max_edge=2576 and max_tokens=4784. Returns (width, height). Images that
    already fit within the limits are returned unchanged.
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
2. Kirim gambar yang telah diubah ukurannya ke API. Jangan memberi padding sendiri; Claude menangani padding, dan padding tidak menggeser titik asal koordinat.
3. Dalam prompt Anda, minta secara eksplisit koordinat piksel. Misalnya: *"Return the bounding box of each table as `[x1, y1, x2, y2]` in pixel coordinates."*
4. Gunakan koordinat yang dikembalikan secara langsung terhadap gambar yang Anda kirim. Jika Anda memerlukan koordinat yang dinormalisasi, bagi dengan dimensi gambar yang Anda kirim, bukan dengan dimensi gambar asli dan bukan dengan dimensi yang diberi padding.

### Skalakan ulang koordinat ketika Anda tidak dapat mengubah ukuran terlebih dahulu \{#rescale-coordinates-when-you-cannot-pre-resize}

Jika Anda tidak dapat mengubah ukuran terlebih dahulu (misalnya, ketika gambar berasal dari sistem upstream yang tidak dapat Anda modifikasi), gunakan `resized_size` dari [Ubah ukuran gambar Anda sebelum mengunggah](#resize-your-image-before-uploading) untuk memulihkan dimensi yang dilihat Claude, lalu petakan koordinat yang dikembalikan Claude ke koordinat yang dinormalisasi atau kembali ke gambar asli Anda. Pendekatan ini memerlukan pengetahuan tentang dimensi piksel gambar yang Anda unggah, sehingga tidak berlaku untuk unggahan PDF.

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

    Pass the dimensions of the image you uploaded. For Claude Opus 4.7 and
    later models, use max_edge=2576 and max_tokens=4784.
    """
    resized_w, resized_h = resized_size(
        original_width, original_height, max_edge, max_tokens
    )
    return (x / resized_w, y / resized_h)


# Untuk menyatakan koordinat dalam ruang piksel gambar asli Anda, kalikan
# koordinat relatif dengan dimensi asli Anda:
# (rel_x * original_width, rel_y * original_height)
```

Padding hanya diterapkan pada tepi bawah dan kanan, sehingga titik asal tidak bergeser dan penskalaan ulang linear per sumbu sudah cukup.

---

## Contoh prompt \{#prompt-examples}

Banyak [teknik prompting](/docs/id/build-with-claude/prompt-engineering/overview) yang bekerja dengan baik untuk interaksi berbasis teks dengan Claude juga dapat diterapkan pada prompt berbasis gambar.

Contoh-contoh ini mendemonstrasikan struktur prompt praktik terbaik yang melibatkan gambar.

<Tip>
  Sama seperti [menempatkan dokumen panjang sebelum kueri Anda](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#long-context-prompting) meningkatkan hasil dalam prompt teks, Claude bekerja paling baik ketika gambar ditempatkan sebelum teks. Gambar yang ditempatkan setelah teks atau disisipkan di antara teks tetap berfungsi dengan baik, tetapi jika kasus penggunaan Anda memungkinkan, lebih baik gunakan struktur gambar-lalu-teks.
</Tip>

### Tentang contoh prompt \{#about-the-prompt-examples}

Contoh-contoh berikut mendemonstrasikan cara menggunakan kemampuan vision Claude menggunakan berbagai bahasa pemrograman dan pendekatan. Anda dapat memberikan gambar ke Claude dengan tiga cara:

1. Sebagai gambar yang dikodekan base64 dalam blok konten `image`
2. Sebagai referensi URL ke gambar yang dihosting secara online
3. Menggunakan Files API (unggah sekali, gunakan berkali-kali)

<Note>
Di Amazon Bedrock dan Vertex AI, saat ini hanya sumber yang dikodekan base64 yang tersedia.
</Note>

Contoh prompt base64 menggunakan variabel-variabel ini:

<CodeGroup>
```bash cURL
    # Untuk gambar berbasis URL, Anda dapat menggunakan URL secara langsung dalam permintaan JSON Anda

    # Untuk gambar yang dienkode base64, Anda perlu mengenkode gambar terlebih dahulu
    # Contoh cara mengenkode gambar ke base64 di bash:
    BASE64_IMAGE_DATA=$(curl -s "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg" | base64)

    # Data yang telah dienkode sekarang dapat digunakan dalam panggilan API Anda
```

```python Python
import base64
import httpx

# Untuk gambar yang dienkode base64
image1_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image1_media_type = "image/jpeg"
image1_data = base64.standard_b64encode(httpx.get(image1_url).content).decode("utf-8")

image2_url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"
image2_media_type = "image/jpeg"
image2_data = base64.standard_b64encode(httpx.get(image2_url).content).decode("utf-8")

# Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan Anda
```

```typescript TypeScript nocheck
import axios from "axios";

// Untuk gambar yang dienkode base64
async function getBase64Image(url: string): Promise<string> {
  const response = await axios.get(url, { responseType: "arraybuffer" });
  return Buffer.from(response.data, "binary").toString("base64");
}

// Penggunaan
async function prepareImages() {
  const imageData = await getBase64Image(
    "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
  );
  // Sekarang Anda dapat menggunakan imageData dalam panggilan API Anda
}

// Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan Anda
```

```csharp C#
using System;
using System.Net.Http;
using System.Threading.Tasks;

// Untuk gambar yang dienkode base64
async Task<string> DownloadAndEncodeImageAsync(string url)
{
    using var client = new HttpClient();
    var bytes = await client.GetByteArrayAsync(url);
    return Convert.ToBase64String(bytes);
}

// Penggunaan:
// var imageData = await DownloadAndEncodeImageAsync("https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg");
// Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan Anda
```

```go Go hidelines={1..9,-8..}
package main

import (
	"encoding/base64"
	"fmt"
	"io"
	"net/http"
)

func downloadAndEncodeImage(url string) (string, error) {
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return "", err
	}
	req.Header.Set("User-Agent", "AnthropicDocsBot/1.0")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	data, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	return base64.StdEncoding.EncodeToString(data), nil
}

func main() {
	imageData, err := downloadAndEncodeImage("https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg")
	if err != nil {
		panic(err)
	}
	fmt.Println(imageData[:50])
}
```

```java Java nocheck hidelines={1..7,-1}
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.Base64;

public class ImageHandlingExample {

  public static void main(String[] args) throws IOException, InterruptedException {
    // Untuk gambar yang dienkode base64
    String image1Url =
      "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";
    String image1MediaType = "image/jpeg";
    String image1Data = downloadAndEncodeImage(image1Url);

    String image2Url =
      "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg";
    String image2MediaType = "image/jpeg";
    String image2Data = downloadAndEncodeImage(image2Url);

    // Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan Anda
  }

  private static String downloadAndEncodeImage(String imageUrl) throws IOException {
    try (InputStream inputStream = new URL(imageUrl).openStream()) {
      return Base64.getEncoder().encodeToString(inputStream.readAllBytes());
    }
  }
}
```

```php PHP nocheck hidelines={1}
<?php
// Untuk gambar yang dienkode base64
function downloadAndEncodeImage($url) {
    $imageData = file_get_contents($url);
    return base64_encode($imageData);
}

$image1Url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";
$image1MediaType = "image/jpeg";
$image1Data = downloadAndEncodeImage($image1Url);

// Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan Anda
```

```ruby Ruby
require "base64"
require "net/http"
require "uri"

# Untuk gambar yang dienkode base64
def download_and_encode_image(url)
  uri = URI.parse(url)
  response = Net::HTTP.get_response(uri)
  Base64.strict_encode64(response.body)
end

image1_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image1_media_type = "image/jpeg"
image1_data = download_and_encode_image(image1_url)

# Untuk gambar berbasis URL, Anda dapat menggunakan URL langsung dalam permintaan Anda
```
</CodeGroup>

Berikut adalah contoh cara menyertakan gambar dalam permintaan Messages API menggunakan gambar yang dikodekan base64 dan referensi URL:

### Contoh gambar yang dikodekan base64 \{#base64-encoded-image-example}

<CodeGroup>
    ```bash cURL hidelines={1..2}
    BASE64_IMAGE_DATA=$(curl -s "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg" | base64 | tr -d '\n')

    curl https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d @- <<EOF
    {
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "image",
              "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": "$BASE64_IMAGE_DATA"
              }
            },
            {
              "type": "text",
              "text": "Describe this image."
            }
          ]
        }
      ]
    }
    EOF
    ```
    ```bash CLI
    curl -sSo ./image.jpg \
      https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg

    ant messages create <<'YAML'
    model: claude-opus-4-8
    max_tokens: 1024
    messages:
      - role: user
        content:
          - type: image
            source:
              type: base64
              media_type: image/jpeg
              data: "@./image.jpg"
          - type: text
            text: Describe this image.
    YAML
    ```
    ```python Python hidelines={1..2}
    import anthropic

    image1_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image1_media_type = "image/png"

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image1_media_type,
                            "data": image1_data,
                        },
                    },
                    {"type": "text", "text": "Describe this image."},
                ],
            }
        ],
    )
    print(message)
    ```
    
    ```typescript TypeScript nocheck hidelines={1..2}
    import Anthropic from "@anthropic-ai/sdk";

    const anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY
    });

    const message = await anthropic.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: {
                type: "base64",
                media_type: "image/jpeg",
                data: imageData // Base64-encoded image data as string
              }
            },
            {
              type: "text",
              text: "Describe this image."
            }
          ]
        }
      ]
    });

    console.log(message);
    ```
    ```csharp C#
    using System.Collections.Generic;
    using Anthropic;
    using Anthropic.Models.Messages;

    AnthropicClient client = new();

    string imageData = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC";

    var message = await client.Messages.Create(new MessageCreateParams
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 1024,
        Messages =
        [
            new()
            {
                Role = Role.User,
                Content = new MessageParamContent(new List<ContentBlockParam>
                {
                    new ContentBlockParam(new ImageBlockParam(
                        new ImageBlockParamSource(new Base64ImageSource()
                        {
                            Data = imageData,
                            MediaType = MediaType.ImagePng,
                        })
                    )),
                    new ContentBlockParam(new TextBlockParam("Describe this image.")),
                }),
            }
        ]
    });

    Console.WriteLine(message);
    ```
    ```go Go hidelines={1..11,-1}
    package main

    import (
    	"context"
    	"fmt"
    	"log"

    	"github.com/anthropics/anthropic-sdk-go"
    )

    func main() {
    	client := anthropic.NewClient()

    	imageData := "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"

    	message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    		Model:     anthropic.ModelClaudeOpus4_8,
    		MaxTokens: 1024,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(
    				anthropic.NewImageBlockBase64("image/png", imageData),
    				anthropic.NewTextBlock("Describe this image."),
    			),
    		},
    	})
    	if err != nil {
    		log.Fatal(err)
    	}

    	fmt.Println(message)
    }
    ```

    
    ```java Java nocheck hidelines={1..8,-2..}
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.*;
    import java.util.List;

    public class VisionExample {

      public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();
        String imageData = ""; // Base64-encoded image data as string

        List<ContentBlockParam> contentBlockParams = List.of(
          ContentBlockParam.ofImage(
            ImageBlockParam.builder()
              .source(
                Base64ImageSource.builder()
                  .mediaType(Base64ImageSource.MediaType.IMAGE_JPEG)
                  .data(imageData)
                  .build()
              )
              .build()
          ),
          ContentBlockParam.ofText(TextBlockParam.builder().text("Describe this image.").build())
        );
        Message message = client
          .messages()
          .create(
            MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024)
              .addUserMessageOfBlockParams(contentBlockParams)
              .build()
          );

        System.out.println(message);
      }
    }
    ```
    ```php PHP hidelines={1..4}
    <?php

    use Anthropic\Client;

    $client = new Client();

    $imageData = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC";

    $message = $client->messages->create(
        maxTokens: 1024,
        messages: [
            [
                'role' => 'user',
                'content' => [
                    [
                        'type' => 'image',
                        'source' => [
                            'type' => 'base64',
                            'media_type' => 'image/png',
                            'data' => $imageData,
                        ],
                    ],
                    ['type' => 'text', 'text' => 'Describe this image.'],
                ],
            ],
        ],
        model: 'claude-opus-4-8',
    );

    echo $message->content[0]->text;
    ```
    ```ruby Ruby hidelines={1..2}
    require "anthropic"

    client = Anthropic::Client.new

    image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"

    message = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: {
                type: "base64",
                media_type: "image/png",
                data: image_data
              }
            },
            { type: "text", text: "Describe this image." }
          ]
        }
      ]
    )

    puts message
    ```
</CodeGroup>

### Contoh gambar berbasis URL \{#url-based-image-example}

<CodeGroup>
    ```bash cURL
    curl https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      -d '{
        "model": "claude-opus-4-8",
        "max_tokens": 1024,
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "image",
                "source": {
                  "type": "url",
                  "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
                }
              },
              {
                "type": "text",
                "text": "Describe this image."
              }
            ]
          }
        ]
      }'
    ```
    ```bash CLI
    ant messages create <<'YAML'
    model: claude-opus-4-8
    max_tokens: 1024
    messages:
      - role: user
        content:
          - type: image
            source:
              type: url
              url: https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg
          - type: text
            text: Describe this image.
    YAML
    ```
    ```python Python hidelines={1..2}
    import anthropic

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                        },
                    },
                    {"type": "text", "text": "Describe this image."},
                ],
            }
        ],
    )
    print(message)
    ```
    ```typescript TypeScript hidelines={1..2}
    import Anthropic from "@anthropic-ai/sdk";

    const anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY
    });

    const message = await anthropic.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: {
                type: "url",
                url: "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
              }
            },
            {
              type: "text",
              text: "Describe this image."
            }
          ]
        }
      ]
    });

    console.log(message);
    ```
    ```csharp C#
    using System.Collections.Generic;
    using Anthropic;
    using Anthropic.Models.Messages;

    AnthropicClient client = new();

    var message = await client.Messages.Create(new MessageCreateParams
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 1024,
        Messages =
        [
            new()
            {
                Role = Role.User,
                Content = new MessageParamContent(new List<ContentBlockParam>
                {
                    new ContentBlockParam(new ImageBlockParam(
                        new ImageBlockParamSource(new UrlImageSource()
                        {
                            Url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                        })
                    )),
                    new ContentBlockParam(new TextBlockParam("Describe this image.")),
                }),
            }
        ]
    });

    Console.WriteLine(message);
    ```
    ```go Go hidelines={1..11,-1}
    package main

    import (
    	"context"
    	"fmt"
    	"log"

    	"github.com/anthropics/anthropic-sdk-go"
    )

    func main() {
    	client := anthropic.NewClient()

    	message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    		Model:     anthropic.ModelClaudeOpus4_8,
    		MaxTokens: 1024,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(
    				anthropic.NewImageBlock(anthropic.URLImageSourceParam{
    					URL: "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
    				}),
    				anthropic.NewTextBlock("Describe this image."),
    			),
    		},
    	})
    	if err != nil {
    		log.Fatal(err)
    	}

    	fmt.Println(message)
    }
    ```
    ```java Java hidelines={1..9,-2..}
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.*;
    import java.io.IOException;
    import java.util.List;

    public class VisionExample {

      public static void main(String[] args) throws IOException, InterruptedException {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        List<ContentBlockParam> contentBlockParams = List.of(
          ContentBlockParam.ofImage(
            ImageBlockParam.builder()
              .source(
                UrlImageSource.builder()
                  .url(
                    "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
                  )
                  .build()
              )
              .build()
          ),
          ContentBlockParam.ofText(TextBlockParam.builder().text("Describe this image.").build())
        );
        Message message = client
          .messages()
          .create(
            MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024)
              .addUserMessageOfBlockParams(contentBlockParams)
              .build()
          );
        System.out.println(message);
      }
    }
    ```
    ```php PHP hidelines={1..4}
    <?php

    use Anthropic\Client;

    $client = new Client();

    $message = $client->messages->create(
        maxTokens: 1024,
        messages: [
            [
                'role' => 'user',
                'content' => [
                    [
                        'type' => 'image',
                        'source' => [
                            'type' => 'url',
                            'url' => 'https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg',
                        ],
                    ],
                    ['type' => 'text', 'text' => 'Describe this image.'],
                ],
            ],
        ],
        model: 'claude-opus-4-8',
    );

    echo $message->content[0]->text;
    ```
    ```ruby Ruby hidelines={1..2}
    require "anthropic"

    client = Anthropic::Client.new

    message = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: {
                type: "url",
                url: "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
              }
            },
            { type: "text", text: "Describe this image." }
          ]
        }
      ]
    )

    puts message
    ```
</CodeGroup>

### Contoh gambar Files API \{#files-api-image-example}

Untuk gambar yang akan Anda gunakan berulang kali atau ketika Anda ingin menghindari overhead encoding, gunakan [Files API](/docs/id/build-with-claude/files). Unggah gambar sekali, lalu referensikan `file_id` yang dikembalikan dalam pesan berikutnya alih-alih mengirim ulang data base64.

<Tip>
  Dalam percakapan multi-giliran dan alur kerja agentic, setiap permintaan
  mengirim ulang seluruh riwayat percakapan. Jika gambar dikodekan base64,
  seluruh byte gambar disertakan dalam payload pada setiap giliran, yang dapat
  secara signifikan meningkatkan ukuran permintaan dan latensi seiring
  bertambahnya percakapan. Mengunggah gambar ke Files API dan mereferensikannya
  melalui `file_id` menjaga payload permintaan tetap kecil terlepas dari berapa
  banyak gambar yang terakumulasi dalam riwayat percakapan.
</Tip>

<CodeGroup>
```bash cURL hidelines={1..2}
cd "$(mktemp -d)"
curl -sSo image.jpg https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg
# Pertama, unggah gambar Anda ke Files API
curl -X POST https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -F "file=@image.jpg"

# Kemudian gunakan file_id yang dikembalikan dalam pesan Anda
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image",
            "source": {
              "type": "file",
              "file_id": "file_abc123"
            }
          },
          {
            "type": "text",
            "text": "Describe this image."
          }
        ]
      }
    ]
  }'
```

```bash CLI nocheck hidelines={1}
cd "$(mktemp -d)"
curl -sSo image.jpg \
  https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg

# Pertama, unggah gambar Anda ke Files API
FILE_ID=$(ant beta:files upload \
  --file ./image.jpg \
  --transform id --raw-output)

# Kemudian gunakan file_id yang dikembalikan dalam pesan Anda
ant beta:messages create \
  --beta files-api-2025-04-14 \
  --transform content --format yaml <<YAML
model: claude-opus-4-8
max_tokens: 1024
messages:
  - role: user
    content:
      - type: image
        source:
          type: file
          file_id: $FILE_ID
      - type: text
        text: Describe this image.
YAML
```

```python Python nocheck hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

# Unggah file gambar
with open("image.jpg", "rb") as f:
    file_upload = client.beta.files.upload(file=("image.jpg", f, "image/jpeg"))

# Gunakan file yang diunggah dalam pesan
message = client.beta.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    betas=["files-api-2025-04-14"],
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "file", "file_id": file_upload.id},
                },
                {"type": "text", "text": "Describe this image."},
            ],
        }
    ],
)

print(message.content)
```

```typescript TypeScript nocheck
import Anthropic, { toFile } from "@anthropic-ai/sdk";
import fs from "fs";

const anthropic = new Anthropic();

// Unggah file gambar
const fileUpload = await anthropic.beta.files.upload({
  file: await toFile(fs.createReadStream("image.jpg"), undefined, { type: "image/jpeg" })
});

// Gunakan file yang diunggah dalam pesan
const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  betas: ["files-api-2025-04-14"],
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: {
            type: "file",
            file_id: fileUpload.id
          }
        },
        {
          type: "text",
          text: "Describe this image."
        }
      ]
    }
  ]
});

console.log(response);
```

```csharp C# nocheck
using Anthropic;

var client = new AnthropicClient();

// Unggah file gambar
var fileUpload = await client.Beta.Files.Upload(
    new FileUploadParams { File = File.OpenRead("image.jpg") });

// Gunakan file yang diunggah dalam pesan
var response = await client.Beta.Messages.Create(
    new MessageCreateParams
    {
        Model = "claude-opus-4-8",
        MaxTokens = 1024,
        Betas = new[] { "files-api-2025-04-14" },
        Messages = new[]
        {
            new BetaMessageParam
            {
                Role = "user",
                Content = new object[]
                {
                    new
                    {
                        type = "image",
                        source = new { type = "file", file_id = fileUpload.Id }
                    },
                    new { type = "text", text = "Describe this image." }
                }
            }
        }
    });

Console.WriteLine(response);
```

```go Go nocheck hidelines={1..12,-1}
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	// Unggah file gambar
	file, err := os.Open("image.jpg")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	fileUpload, err := client.Beta.Files.Upload(context.Background(),
		anthropic.BetaFileUploadParams{
			File: file,
		})
	if err != nil {
		log.Fatal(err)
	}

	// Gunakan file yang diunggah dalam pesan
	message, err := client.Beta.Messages.New(context.Background(),
		anthropic.BetaMessageNewParams{
			Model:     anthropic.ModelClaudeOpus4_8,
			MaxTokens: 1024,
			Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
			Messages: []anthropic.BetaMessageParam{
				anthropic.NewBetaUserMessage(
					anthropic.NewBetaImageBlock(anthropic.BetaFileImageSourceParam{
						FileID: fileUpload.ID,
					}),
					anthropic.NewBetaTextBlock("Describe this image."),
				),
			},
		})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(message.Content)
}
```

```java Java nocheck hidelines={1..2,5..13,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.files.FileMetadata;
import com.anthropic.models.beta.files.FileUploadParams;
import com.anthropic.models.messages.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class ImageFilesExample {

  public static void main(String[] args) throws IOException {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Unggah file gambar
    FileMetadata file = client
      .beta()
      .files()
      .upload(
        FileUploadParams.builder().file(Files.newInputStream(Path.of("image.jpg"))).build()
      );

    // Gunakan file yang diunggah dalam pesan
    ImageBlockParam imageParam = ImageBlockParam.builder().fileSource(file.id()).build();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024)
      .addUserMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofImage(imageParam),
          ContentBlockParam.ofText(
            TextBlockParam.builder().text("Describe this image.").build()
          )
        )
      )
      .build();

    Message message = client.messages().create(params);
    System.out.println(message.content());
  }
}
```

```php PHP nocheck hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

// Unggah file gambar
$fileUpload = $client->beta->files->upload(
    file: fopen('image.jpg', 'r'),
);

// Gunakan file yang diunggah dalam pesan
$message = $client->beta->messages->create(
    maxTokens: 1024,
    messages: [
        [
            'role' => 'user',
            'content' => [
                [
                    'type' => 'image',
                    'source' => ['type' => 'file', 'file_id' => $fileUpload->id],
                ],
                ['type' => 'text', 'text' => 'Describe this image.'],
            ],
        ],
    ],
    model: 'claude-opus-4-8',
    betas: ['files-api-2025-04-14'],
);

echo $message->content[0]->text;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

# Unggah file gambar
file_upload = client.beta.files.upload(
  file: File.open("image.jpg", "rb")
)

# Gunakan file yang diunggah dalam pesan
message = client.beta.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  betas: ["files-api-2025-04-14"],
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: { type: "file", file_id: file_upload.id }
        },
        { type: "text", text: "Describe this image." }
      ]
    }
  ]
)

puts message.content
```
</CodeGroup>

Lihat [contoh Messages API](/docs/id/api/messages/create) untuk lebih banyak contoh kode dan detail parameter.

<section title="Contoh: Satu gambar">

Sebaiknya tempatkan gambar lebih awal dalam prompt daripada pertanyaan tentang gambar tersebut atau instruksi untuk tugas yang menggunakannya.

Minta Claude untuk mendeskripsikan satu gambar.

| Role | Content                        |
| ---- | ------------------------------ |
| User | \[Image\] Describe this image. |

<Tabs>
  <Tab title="Menggunakan Base64">
    ```python Python hidelines={1..2}
    import anthropic

    client = anthropic.Anthropic()
    image1_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image1_media_type = "image/png"

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image1_media_type,
                            "data": image1_data,
                        },
                    },
                    {"type": "text", "text": "Describe this image."},
                ],
            }
        ],
    )
    ```
  </Tab>
  <Tab title="Menggunakan URL">
    ```python Python
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                        },
                    },
                    {"type": "text", "text": "Describe this image."},
                ],
            }
        ],
    )
    ```
  </Tab>
</Tabs>

</section>
<section title="Contoh: Beberapa gambar">

Dalam situasi di mana terdapat beberapa gambar, perkenalkan setiap gambar dengan `Image 1:` dan `Image 2:` dan seterusnya. Anda tidak memerlukan baris baru di antara gambar atau di antara gambar dan prompt.

Minta Claude untuk mendeskripsikan perbedaan antara beberapa gambar.
| Role | Content |
| ---- | ------------------------------------------------------------------------- |
| User | Image 1: \[Image 1\] Image 2: \[Image 2\] How are these images different? |

<Tabs>
  <Tab title="Menggunakan Base64">
    ```python Python hidelines={1..2}
    import anthropic

    client = anthropic.Anthropic()
    image1_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image1_media_type = "image/png"
    image2_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image2_media_type = "image/png"

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Image 1:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image1_media_type,
                            "data": image1_data,
                        },
                    },
                    {"type": "text", "text": "Image 2:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image2_media_type,
                            "data": image2_data,
                        },
                    },
                    {"type": "text", "text": "How are these images different?"},
                ],
            }
        ],
    )
    ```
  </Tab>
  <Tab title="Menggunakan URL">
    ```python Python
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Image 1:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                        },
                    },
                    {"type": "text", "text": "Image 2:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg",
                        },
                    },
                    {"type": "text", "text": "How are these images different?"},
                ],
            }
        ],
    )
    ```
  </Tab>
</Tabs>

</section>
<section title="Contoh: Beberapa gambar dengan prompt sistem">

Minta Claude untuk mendeskripsikan perbedaan antara beberapa gambar, sambil memberikan prompt sistem tentang cara merespons.

| Content |                                                                           |
| ------- | ------------------------------------------------------------------------- |
| System  | Respond only in Spanish.                                                  |
| User    | Image 1: \[Image 1\] Image 2: \[Image 2\] How are these images different? |

<Tabs>
  <Tab title="Menggunakan Base64">
    ```python Python hidelines={1..2}
    import anthropic

    client = anthropic.Anthropic()
    image1_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image1_media_type = "image/png"
    image2_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC"
    image2_media_type = "image/png"

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system="Respond only in Spanish.",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Image 1:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image1_media_type,
                            "data": image1_data,
                        },
                    },
                    {"type": "text", "text": "Image 2:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image2_media_type,
                            "data": image2_data,
                        },
                    },
                    {"type": "text", "text": "How are these images different?"},
                ],
            }
        ],
    )
    ```
  </Tab>
  <Tab title="Menggunakan URL">
    ```python Python
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system="Respond only in Spanish.",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Image 1:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",
                        },
                    },
                    {"type": "text", "text": "Image 2:"},
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg",
                        },
                    },
                    {"type": "text", "text": "How are these images different?"},
                ],
            }
        ],
    )
    ```
  </Tab>
</Tabs>

</section>
<section title="Contoh: Empat gambar dalam dua giliran percakapan">

Kemampuan vision Claude bersinar dalam percakapan multimodal yang menggabungkan gambar dan teks. Anda dapat melakukan pertukaran bolak-balik yang diperpanjang dengan Claude, menambahkan gambar baru atau pertanyaan lanjutan kapan saja. Ini memungkinkan alur kerja yang kuat untuk analisis gambar iteratif, perbandingan, atau menggabungkan visual dengan pengetahuan lain.

Minta Claude untuk mengontraskan dua gambar, lalu ajukan pertanyaan lanjutan yang membandingkan gambar pertama dengan dua gambar baru.
| Role | Content |
| --------- | ------------------------------------------------------------------------------------ |
| User | Image 1: \[Image 1\] Image 2: \[Image 2\] How are these images different? |
| Assistant | \[Claude's response\] |
| User | Image 1: \[Image 3\] Image 2: \[Image 4\] Are these images similar to the first two? |
| Assistant | \[Claude's response\] |

Saat menggunakan API, sisipkan gambar baru ke dalam array Messages dalam role `user` sebagai bagian dari struktur [percakapan multi-giliran](/docs/id/api/messages/create) standar apa pun.

</section>

---

## Batasan \{#limitations}

Meskipun kemampuan pemahaman gambar Claude sangat canggih, ada beberapa batasan yang perlu diperhatikan:

- **Identifikasi orang**: Claude [tidak dapat digunakan](https://www.anthropic.com/legal/aup) untuk menyebutkan nama orang dalam gambar dan menolak untuk melakukannya.
- **Akurasi**: Claude mungkin berhalusinasi atau membuat kesalahan saat menginterpretasikan gambar berkualitas rendah, diputar, atau sangat kecil di bawah 200 piksel.
- **Penalaran spasial**: Output koordinat dan lokalisasi Claude bersifat perkiraan. Ikuti panduan di [Bekerja dengan koordinat dan bounding box](#working-with-coordinates-and-bounding-boxes) dan verifikasi output sebelum mengandalkannya.
- **Menghitung**: Claude dapat memberikan perkiraan jumlah objek dalam gambar tetapi mungkin tidak selalu akurat secara tepat, terutama dengan jumlah besar objek kecil.
- **Gambar yang dihasilkan AI**: Claude tidak mengetahui apakah suatu gambar dihasilkan oleh AI dan mungkin salah jika ditanya. Jangan mengandalkannya untuk mendeteksi gambar palsu atau sintetis.
- **Konten yang tidak pantas**: Claude tidak memproses gambar yang tidak pantas atau eksplisit yang melanggar [Acceptable Use Policy](https://www.anthropic.com/legal/aup).
- **Aplikasi kesehatan**: Meskipun Claude dapat menganalisis gambar medis umum, Claude tidak dirancang untuk menginterpretasikan pemindaian diagnostik kompleks seperti CT atau MRI. Output Claude tidak boleh dianggap sebagai pengganti saran atau diagnosis medis profesional.

Selalu tinjau dan verifikasi interpretasi gambar Claude dengan cermat, terutama untuk kasus penggunaan berisiko tinggi. Jangan gunakan Claude untuk tugas yang memerlukan presisi sempurna atau analisis gambar sensitif tanpa pengawasan manusia.

---

## FAQ \{#faq}

  <section title="Jenis file gambar apa yang didukung Claude?">

    Claude saat ini mendukung format gambar JPEG, PNG, GIF, dan WebP, khususnya:
    - `image/jpeg`
    - `image/png`
    - `image/gif`
    - `image/webp`
  
</section>

{" "}

<section title="Bisakah Claude membaca URL gambar?">

  Ya, Claude dapat memproses gambar dari URL dengan blok sumber gambar URL di API.
  Cukup gunakan tipe sumber "url" alih-alih "base64" dalam permintaan API Anda.
  Contoh:
  ```json
  {
    "type": "image",
    "source": {
      "type": "url",
      "url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
    }
  }
  ```

</section>

  <section title="Apakah ada batas ukuran file gambar yang dapat saya unggah?">

    Ya, ada batasan:
    - Claude API: Maksimum 10&nbsp;MB per gambar
    - Amazon Bedrock dan Vertex AI: Maksimum 5&nbsp;MB per gambar
    - claude.ai: Maksimum 10&nbsp;MB per gambar

    Gambar yang lebih besar dari batas ini ditolak dan mengembalikan error saat menggunakan API.

    Ini adalah batas per gambar. [Batas ukuran permintaan](/docs/id/api/overview#request-size-limits) keseluruhan (32&nbsp;MB pada Claude API; lebih rendah pada Amazon Bedrock dan Vertex AI) juga berlaku, sehingga permintaan dengan banyak gambar besar dapat melebihinya sebelum mencapai batas per gambar. Pada Claude API, unggah dengan [Files API](/docs/id/build-with-claude/files) dan referensikan melalui `file_id` agar payload permintaan tetap kecil. Files API saat ini tidak tersedia di Amazon Bedrock atau Vertex AI, jadi kurangi ukuran gambar pada platform tersebut sebagai gantinya.

  
</section>

  <section title="Berapa banyak gambar yang dapat saya sertakan dalam satu permintaan?">

    Batas gambar adalah:
    - Messages API: Hingga 600 gambar per permintaan (100 untuk model dengan jendela konteks 200k token)
    - claude.ai: Hingga 20 gambar per giliran

    Permintaan yang melebihi batas ini ditolak dan mengembalikan error. Permintaan dengan banyak gambar besar juga dapat gagal sebelum mencapai batas ini; lihat [Batasan umum](#general-limits) untuk detailnya.

  
</section>

{" "}

<section title="Apakah Claude membaca metadata gambar?">

  Tidak, Claude tidak mengurai atau menerima metadata apa pun dari gambar yang diberikan kepadanya.

</section>

{" "}

<section title="Bisakah saya menghapus gambar yang telah saya unggah?">

  Tidak. Unggahan gambar bersifat sementara dan tidak disimpan di luar durasi
  permintaan API. Gambar yang diunggah secara otomatis dihapus setelah
  diproses.

</section>

{" "}

<section title="Di mana saya dapat menemukan detail tentang privasi data untuk unggahan gambar?">

  Lihat halaman kebijakan privasi Anthropic untuk informasi tentang bagaimana
  gambar yang diunggah dan data lainnya ditangani. Anthropic tidak menggunakan
  gambar yang diunggah untuk melatih model.

</section>

  <section title="Bagaimana jika interpretasi gambar Claude tampak salah?">

    Jika interpretasi gambar Claude tampak tidak benar:
    1. Pastikan gambar jernih, berkualitas tinggi, dan berorientasi dengan benar.
    2. Coba teknik prompt engineering untuk meningkatkan hasil.
    3. Jika masalah berlanjut, tandai output di claude.ai (jempol ke atas/bawah) atau hubungi [tim dukungan](https://support.claude.com/).

    Umpan balik Anda membantu meningkatkan Claude!

  
</section>

  <section title="Bisakah Claude menghasilkan atau mengedit gambar?">

    Tidak, Claude hanya merupakan model pemahaman gambar. Claude dapat menginterpretasikan dan menganalisis gambar, tetapi tidak dapat menghasilkan, memproduksi, mengedit, memanipulasi, atau membuat gambar.
  
</section>

---

## Pelajari lebih dalam tentang vision \{#dive-deeper-into-vision}

Siap untuk mulai membangun dengan gambar menggunakan Claude? Berikut beberapa sumber daya yang berguna:

- [Multimodal cookbook](https://platform.claude.com/cookbook/multimodal-getting-started-with-vision): Cookbook ini memiliki tips tentang [memulai dengan gambar](https://platform.claude.com/cookbook/multimodal-getting-started-with-vision) dan [teknik praktik terbaik](https://platform.claude.com/cookbook/multimodal-best-practices-for-vision) untuk memastikan performa kualitas tertinggi dengan gambar. Lihat bagaimana Anda dapat secara efektif memberikan prompt kepada Claude dengan gambar untuk melakukan tugas seperti [menginterpretasikan dan menganalisis grafik](https://platform.claude.com/cookbook/multimodal-reading-charts-graphs-powerpoints) atau [mengekstrak konten dari formulir](https://platform.claude.com/cookbook/multimodal-how-to-transcribe-text).
- [Referensi API](/docs/id/api/messages/create): Dokumentasi untuk Messages API, termasuk contoh [panggilan API yang melibatkan gambar](/docs/id/build-with-claude/working-with-messages#vision).

Jika Anda memiliki pertanyaan lain, hubungi [tim dukungan](https://support.claude.com/). Anda juga dapat bergabung dengan [komunitas developer](https://www.anthropic.com/discord) untuk terhubung dengan kreator lain dan mendapatkan bantuan dari para ahli Anthropic.