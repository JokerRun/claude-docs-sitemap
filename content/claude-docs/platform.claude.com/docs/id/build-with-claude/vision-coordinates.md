---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/vision-coordinates
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: 556ae095023743219eaecb0e312910b009312e7762b40723349988b593c10c86
---

# Koordinat dan bounding box

Bagaimana Claude mengubah ukuran gambar, dan cara bekerja dengan koordinat piksel yang dikembalikannya untuk bounding box, titik, dan elemen UI.

---

Claude dapat menemukan dan melabeli wilayah dari sebuah gambar (misalnya, mengembalikan "bounding box" (kotak pembatas) untuk tabel, bidang formulir, elemen grafik, atau komponen UI). Panduan ini membahas bagaimana Claude mengubah ukuran gambar sebelum memprosesnya dan cara bekerja dengan koordinat piksel yang dikembalikannya, sehingga kotak dan titik sejajar dengan gambar asli Anda.

Anda akan membutuhkan ini untuk pipeline OCR, ekstraksi formulir, parsing grafik, penentuan lokasi elemen UI, dan tugas apa pun di mana Anda bertindak pada wilayah tertentu dari sebuah gambar. Untuk pengiriman gambar, format yang didukung, dan batas resolusi per model, lihat [Vision](/docs/id/build-with-claude/vision).

<Note>
  **Claude bekerja paling baik dengan koordinat piksel absolut.** Minta koordinat tersebut secara eksplisit dalam prompt Anda. Misalnya: *"Kembalikan bounding box dari setiap tabel sebagai `[x1, y1, x2, y2]` (sudut kiri-atas dan kanan-bawah) dalam koordinat piksel."* Claude tidak bekerja dengan baik ketika Anda meminta koordinat yang dinormalisasi, misalnya: *"Kembalikan koordinat bounding box antara `0` dan `1000`."* Selalu minta koordinat piksel dan lakukan normalisasi dalam kode Anda sendiri jika diperlukan. Untuk mendapatkan koordinat sebagai JSON yang dapat dibaca mesin alih-alih prosa, definisikan skema dengan [structured outputs](/docs/id/build-with-claude/structured-outputs), misalnya sebuah objek dengan array `[x1, y1, x2, y2]` per elemen yang terdeteksi.
</Note>

Koordinat mengikuti konvensi gambar standar: titik asal `(0, 0)` adalah sudut kiri-atas gambar, dengan x bertambah ke kanan dan y bertambah ke bawah. Koordinat yang dikembalikan Claude adalah posisi piksel pada gambar yang dilihat Claude: gambar Anda setelah Claude mengubah ukurannya agar sesuai dengan resolusi native model (lihat [Bagaimana Claude mengubah ukuran dan menambahkan padding pada gambar](#how-claude-resizes-and-pads-images)). Untuk mendapatkan koordinat yang dapat Anda gunakan secara langsung, ubah ukuran gambar Anda terlebih dahulu sehingga koordinat terpetakan satu-ke-satu pada gambar yang Anda miliki (lihat [Ubah ukuran gambar Anda sebelum mengunggah](#resize-your-image-before-uploading)), atau skalakan ulang koordinat yang dikembalikan Claude (lihat [Skalakan ulang koordinat ketika Anda tidak dapat mengubah ukuran terlebih dahulu](#rescale-coordinates-when-you-cannot-pre-resize)).

<Note>
  Penalaran spasial Claude memiliki keterbatasan (lihat [Keterbatasan](/docs/id/build-with-claude/vision#limitations)). Akurasi koordinat paling baik ketika Anda menyatakan format koordinat yang diharapkan dalam prompt Anda dan memeriksa hasilnya secara visual sebelum memproses dalam skala besar. Elemen kecil kehilangan presisi ketika gambar diperkecil: untuk target yang halus, potong (crop) wilayah yang diinginkan dan kirim potongan tersebut (geser koordinat yang dikembalikan dengan titik asal potongan), atau gunakan model dengan tingkat resolusi tinggi. Untuk [dukungan PDF](/docs/id/build-with-claude/pdf-support), halaman dirasterisasi menjadi gambar di sisi server dengan dimensi yang tidak Anda kendalikan, sehingga koordinat yang dikembalikan tidak dapat dipetakan kembali ke halaman secara andal. Untuk bekerja dengan koordinat pada konten PDF, rasterisasi halaman menjadi gambar sendiri dan gunakan pendekatan pengubahan ukuran terlebih dahulu.
</Note>

## Bagaimana Claude mengubah ukuran dan menambahkan padding pada gambar

Claude mencari ukuran terbesar yang mempertahankan rasio aspek dan memenuhi kedua batas gambar model:

1. **Batas sisi:** tidak ada sisi yang melebihi panjang sisi maksimum (1568 px pada tingkat standar, 2576 px pada tingkat resolusi tinggi).
2. **Batas token visual:** biaya token gambar `⌈width / 28⌉ × ⌈height / 28⌉` tidak melebihi anggaran token visual model (1568 token pada tingkat standar, 4784 pada tingkat resolusi tinggi).

Lihat [Resolusi dan biaya token](/docs/id/build-with-claude/vision#evaluate-image-size) untuk mengetahui model mana yang berada di tingkat mana.

Untuk hampir semua foto dan tangkapan layar, batas token visual adalah yang menentukan ukuran akhir. Batas sisi hanya berlaku untuk gambar yang memanjang seperti panorama atau tangkapan layar ponsel yang tinggi. Hitung ukurannya dengan [implementasi referensi](#resize-your-image-before-uploading) alih-alih menskalakan ke panjang sisi secara manual: tangkapan layar 1920×1080 diubah ukurannya menjadi 1456×819, bukan 1568×882, dan mengasumsikan batas sisi akan membuat setiap koordinat meleset secara signifikan dari target.

Batas token juga dapat memicu pengubahan ukuran ketika tidak ada sisi yang melebihi batas sisi. Mengabaikan hal ini adalah penyebab paling umum dari koordinat yang tidak sejajar. Misalnya, halaman A4 yang dipindai pada 130 DPI berukuran 1075×1520 piksel: kedua sisinya di bawah 1568 px, tetapi biayanya `39 × 55 = 2145` token visual, sehingga Claude mengubah ukurannya menjadi 924×1307.

<Note>
  Contoh ini mengasumsikan model pada tingkat resolusi standar. Model dengan tingkat resolusi tinggi tidak mengubah ukuran hasil pindaian yang sama: 2145 token berada dalam anggaran 4784 tokennya, sehingga koordinat yang dikembalikannya terpetakan langsung ke gambar asli 1075×1520. Tingkat model tercantum di [Resolusi dan biaya token](/docs/id/build-with-claude/vision#evaluate-image-size).
</Note>

Claude kemudian menambahkan "padding" (pengisi) pada setiap gambar, baik yang diubah ukurannya maupun tidak, hingga kelipatan 28 piksel berikutnya pada tepi bawah dan kanan (924×1307 menjadi 924×1316 dalam contoh tersebut). Padding tidak berisi konten apa pun: Claude melihat gambar yang telah diberi padding, tetapi konten halaman hanya menempati wilayah hasil pengubahan ukuran yang tidak diberi padding. **Selalu normalisasi atau skalakan ulang berdasarkan dimensi hasil pengubahan ukuran, bukan dimensi yang telah diberi padding**; membagi dengan dimensi yang telah diberi padding akan menskalakan setiap koordinat dengan jumlah kecil.

## Ubah ukuran gambar Anda sebelum mengunggah

Pendekatan yang paling andal adalah mengubah ukuran gambar Anda sendiri sebelum mengunggah, sehingga gambar yang Anda miliki persis sama dengan gambar yang dilihat Claude dan koordinat yang dikembalikan Claude tidak memerlukan konversi.

Pertama, periksa tingkat resolusi model Anda (lihat [Resolusi dan biaya token](/docs/id/build-with-claude/vision#evaluate-image-size)) dan berikan batas sisi dan token yang sesuai. Implementasi referensi berikut menghitung ukuran persis yang digunakan Claude untuk mengubah ukuran gambar:

<CodeGroup>
  ```bash cURL
  # Implementasi referensi ini adalah perhitungan matematika lokal yang tidak membuat permintaan API, jadi
  # tidak ada yang bisa ditampilkan untuk cURL. Lihat tab SDK.
  ```

  ```bash CLI
  # Implementasi referensi ini berupa perhitungan matematika lokal yang tidak membuat permintaan API, jadi
  # tidak ada yang perlu ditampilkan untuk CLI. Lihat tab SDK.
  ```

  ```python Python
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

  # Untuk menerapkan pengubahan ukuran, gunakan pustaka gambar Anda, misalnya Pillow:
  # image.resize(resized_size(*image.size))
  ```

  ```typescript TypeScript
  /** Visual tokens consumed by an image: one token per 28x28 pixel patch. */
  function countImageTokens(width: number, height: number): number {
    return Math.ceil(width / 28) * Math.ceil(height / 28);
  }

  /**
   * Round half to even (banker's rounding), matching Python's round(). The
   * live API resolves exact .5 ties toward the even neighbor, so Math.round
   * (which rounds halves up) would compute a different size for some images.
   */
  function roundTiesToEven(value: number): number {
    const floor = Math.floor(value);
    if (value - floor !== 0.5) return Math.round(value);
    return floor % 2 === 0 ? floor : floor + 1;
  }

  /**
   * The size Claude resizes an image to before padding.
   *
   * Defaults are for the standard resolution tier. For high-resolution-tier
   * models, use maxEdge = 2576 and maxTokens = 4784. Returns [width, height].
   * Images that already fit within the limits are returned unchanged.
   */
  function resizedSize(
    width: number,
    height: number,
    maxEdge = 1568,
    maxTokens = 1568
  ): [number, number] {
    const fits = (w: number, h: number): boolean =>
      Math.ceil(w / 28) * 28 <= maxEdge &&
      Math.ceil(h / 28) * 28 <= maxEdge &&
      countImageTokens(w, h) <= maxTokens;

    if (fits(width, height)) return [width, height];
    if (height > width) {
      const [resizedH, resizedW] = resizedSize(height, width, maxEdge, maxTokens);
      return [resizedW, resizedH];
    }

    // Pencarian biner di sepanjang sisi panjang untuk ukuran terbesar yang
    // mempertahankan aspek rasio dan masih muat.
    const aspectRatio = width / height;
    let lo = 1; // lo always fits
    let hi = width; // hi never fits
    while (lo + 1 < hi) {
      const mid = Math.floor((lo + hi) / 2);
      if (fits(mid, Math.max(roundTiesToEven(mid / aspectRatio), 1))) {
        lo = mid;
      } else {
        hi = mid;
      }
    }
    return [lo, Math.max(roundTiesToEven(lo / aspectRatio), 1)];
  }

  // Contoh A4 dari "How Claude resizes and pads images":
  console.log(resizedSize(1075, 1520)); // [ 924, 1307 ]

  // Untuk menerapkan resize, gunakan pustaka gambar Anda, misalnya sharp:
  // await sharp(input).resize(width, height).toBuffer()
  ```

  ```csharp C#
  // Token visual yang dikonsumsi oleh gambar: satu token per patch 28x28 piksel.
  static int CountImageTokens(int width, int height)
  {
      return (width + 27) / 28 * ((height + 27) / 28); // ceil(w/28) * ceil(h/28)
  }

  // Ukuran yang digunakan Claude untuk mengubah ukuran gambar sebelum padding. Default untuk
  // tier resolusi standar; untuk model tier resolusi tinggi, berikan
  // maxEdge: 2576, maxTokens: 4784. Gambar yang sudah muat dalam batas
  // dikembalikan tanpa perubahan.
  static (int Width, int Height) ResizedSize(
      int width, int height, int maxEdge = 1568, int maxTokens = 1568)
  {
      bool Fits(int w, int h) =>
          (w + 27) / 28 * 28 <= maxEdge
          && (h + 27) / 28 * 28 <= maxEdge
          && CountImageTokens(w, h) <= maxTokens;

      if (Fits(width, height))
      {
          return (width, height);
      }
      if (height > width)
      {
          (int resizedH, int resizedW) = ResizedSize(height, width, maxEdge, maxTokens);
          return (resizedW, resizedH);
      }

      // Pencarian biner di sepanjang sisi panjang untuk ukuran terbesar yang mempertahankan
      // rasio aspek dan muat. Sisi pendek membulatkan setengah ke genap, sesuai dengan API
      // langsung pada seri tepat .5 (MidpointRounding.ToEven, default Math.Round).
      double aspectRatio = (double)width / height;
      int lo = 1; // lo always fits
      int hi = width; // hi never fits
      while (lo + 1 < hi)
      {
          int mid = (lo + hi) / 2;
          if (Fits(mid, ShortEdge(mid)))
          {
              lo = mid;
          }
          else
          {
              hi = mid;
          }
      }
      return (lo, ShortEdge(lo));

      int ShortEdge(int longEdge) =>
          Math.Max((int)Math.Round(longEdge / aspectRatio, MidpointRounding.ToEven), 1);
  }

  // Contoh A4 dari "How Claude resizes and pads images":
  Console.WriteLine(ResizedSize(1075, 1520)); // (924, 1307)
  ```

  ```go Go
  // countImageTokens adalah token visual yang dikonsumsi oleh sebuah gambar: satu token per
  // patch 28x28 piksel.
  func countImageTokens(width, height int) int {
  	return ((width + 27) / 28) * ((height + 27) / 28) // ceil(w/28) * ceil(h/28)
  }

  // resizedSize adalah ukuran yang Claude gunakan untuk me-resize gambar sebelum padding, sebagai
  // (width, height). Berikan maxEdge 1568 dan maxTokens 1568 untuk tier resolusi
  // standar, atau 2576 dan 4784 untuk tier resolusi tinggi. Gambar
  // yang sudah muat dalam batas tersebut dikembalikan tanpa perubahan.
  // Contoh A4 dari "How Claude resizes and pads images":
  // resizedSize(1075, 1520, 1568, 1568) mengembalikan (924, 1307).
  func resizedSize(width, height, maxEdge, maxTokens int) (int, int) {
  	fits := func(w, h int) bool {
  		return ((w+27)/28)*28 <= maxEdge &&
  			((h+27)/28)*28 <= maxEdge &&
  			countImageTokens(w, h) <= maxTokens
  	}

  	if fits(width, height) {
  		return width, height
  	}
  	if height > width {
  		resizedH, resizedW := resizedSize(height, width, maxEdge, maxTokens)
  		return resizedW, resizedH
  	}

  	// Binary search di sepanjang sisi panjang untuk ukuran terbesar yang menjaga
  	// rasio aspek dan muat. Sisi pendek dibulatkan half-to-even (math.RoundToEven),
  	// sesuai dengan API langsung pada tie tepat .5; math.Round akan membulatkannya ke atas.
  	aspectRatio := float64(width) / float64(height)
  	lo, hi := 1, width // lo always fits; hi never fits
  	for lo+1 < hi {
  		mid := (lo + hi) / 2
  		short := max(int(math.RoundToEven(float64(mid)/aspectRatio)), 1)
  		if fits(mid, short) {
  			lo = mid
  		} else {
  			hi = mid
  		}
  	}
  	return lo, max(int(math.RoundToEven(float64(lo)/aspectRatio)), 1)
  }

  ```

  ```java Java
  /** A resized image size, as returned by resizedSize. */
  record Size(int width, int height) {}

  /** Visual tokens consumed by an image: one token per 28x28 pixel patch. */
  static int countImageTokens(int width, int height) {
      return Math.ceilDiv(width, 28) * Math.ceilDiv(height, 28);
  }

  /**
   * The size Claude resizes an image to before padding.
   *
   * <p>Pass maxEdge 1568 and maxTokens 1568 for the standard resolution tier,
   * or 2576 and 4784 for the high-resolution tier. Images that already fit
   * within the limits are returned unchanged.
   *
   * <p>The A4 example from "How Claude resizes and pads images":
   * resizedSize(1075, 1520, 1568, 1568) returns new Size(924, 1307).
   */
  static Size resizedSize(int width, int height, int maxEdge, int maxTokens) {
      if (fits(width, height, maxEdge, maxTokens)) {
          return new Size(width, height);
      }
      if (height > width) {
          Size rotated = resizedSize(height, width, maxEdge, maxTokens);
          return new Size(rotated.height(), rotated.width());
      }

      // Binary search di sepanjang sisi panjang untuk ukuran terbesar yang mempertahankan
      // aspek dan muat. Sisi pendek membulatkan setengah ke genap (Math.rint),
      // sesuai API live pada tie tepat .5; Math.round akan membulatkannya ke atas.
      double aspectRatio = (double) width / height;
      int lo = 1; // lo always fits
      int hi = width; // hi never fits
      while (lo + 1 < hi) {
          int mid = (lo + hi) / 2;
          if (fits(mid, shortEdge(mid, aspectRatio), maxEdge, maxTokens)) {
              lo = mid;
          } else {
              hi = mid;
          }
      }
      return new Size(lo, shortEdge(lo, aspectRatio));
  }

  private static boolean fits(int width, int height, int maxEdge, int maxTokens) {
      return Math.ceilDiv(width, 28) * 28 <= maxEdge
              && Math.ceilDiv(height, 28) * 28 <= maxEdge
              && countImageTokens(width, height) <= maxTokens;
  }

  private static int shortEdge(int longEdge, double aspectRatio) {
      return Math.max((int) Math.rint(longEdge / aspectRatio), 1);
  }
  ```

  ```php PHP
  // Token visual yang dikonsumsi oleh gambar: satu token per patch piksel 28x28.
  function countImageTokens(int $width, int $height): int
  {
      return intdiv($width + 27, 28) * intdiv($height + 27, 28);
  }

  /**
   * The size Claude resizes an image to before padding, as [width, height].
   *
   * Defaults are for the standard resolution tier. For high-resolution-tier
   * models, pass maxEdge: 2576, maxTokens: 4784. Images that already fit
   * within the limits are returned unchanged.
   */
  function resizedSize(int $width, int $height, int $maxEdge = 1568, int $maxTokens = 1568): array
  {
      $fits = fn (int $w, int $h): bool =>
          intdiv($w + 27, 28) * 28 <= $maxEdge
          && intdiv($h + 27, 28) * 28 <= $maxEdge
          && countImageTokens($w, $h) <= $maxTokens;

      if ($fits($width, $height)) {
          return [$width, $height];
      }
      if ($height > $width) {
          [$resizedH, $resizedW] = resizedSize($height, $width, $maxEdge, $maxTokens);
          return [$resizedW, $resizedH];
      }

      // Pencarian biner di sepanjang sisi panjang untuk ukuran terbesar yang mempertahankan
      // rasio aspek dan masih muat. Sisi pendek dibulatkan setengah ke genap
      // (PHP_ROUND_HALF_EVEN), sesuai dengan API langsung pada kasus tepat .5.
      $aspectRatio = $width / $height;
      $lo = 1; // lo always fits
      $hi = $width; // hi never fits
      while ($lo + 1 < $hi) {
          $mid = intdiv($lo + $hi, 2);
          $short = max((int) round($mid / $aspectRatio, 0, PHP_ROUND_HALF_EVEN), 1);
          if ($fits($mid, $short)) {
              $lo = $mid;
          } else {
              $hi = $mid;
          }
      }

      return [$lo, max((int) round($lo / $aspectRatio, 0, PHP_ROUND_HALF_EVEN), 1)];
  }

  // Contoh A4 dari "How Claude resizes and pads images":
  [$resizedWidth, $resizedHeight] = resizedSize(1075, 1520);
  echo "({$resizedWidth}, {$resizedHeight})\n"; // (924, 1307)
  ```

  ```ruby Ruby
  # Token visual yang dikonsumsi oleh gambar: satu token per patch piksel 28x28.
  def count_image_tokens(width, height)
    width.ceildiv(28) * height.ceildiv(28)
  end

  # Ukuran yang Claude gunakan untuk mengubah ukuran gambar sebelum padding, sebagai [lebar, tinggi].
  #
  # Nilai default adalah untuk tingkat resolusi standar. Untuk model tingkat resolusi
  # tinggi, berikan max_edge: 2576, max_tokens: 4784. Gambar yang sudah muat
  # dalam batas tersebut dikembalikan tanpa perubahan.
  def resized_size(width, height, max_edge = 1568, max_tokens = 1568)
    fits = lambda do |w, h|
      w.ceildiv(28) * 28 <= max_edge &&
        h.ceildiv(28) * 28 <= max_edge &&
        count_image_tokens(w, h) <= max_tokens
    end

    return [width, height] if fits.call(width, height)

    if height > width
      resized_h, resized_w = resized_size(height, width, max_edge, max_tokens)
      return [resized_w, resized_h]
    end

    # Pencarian biner di sepanjang sisi panjang untuk ukuran terbesar yang mempertahankan
    # rasio aspek dan muat. Sisi pendek dibulatkan setengah ke genap (round(half: :even)),
    # sesuai dengan API langsung pada kasus seri tepat .5.
    aspect_ratio = width.fdiv(height)
    lo = 1      # lo always fits
    hi = width  # hi never fits
    while lo + 1 < hi
      mid = (lo + hi) / 2
      short = [(mid / aspect_ratio).round(half: :even), 1].max
      if fits.call(mid, short)
        lo = mid
      else
        hi = mid
      end
    end

    [lo, [(lo / aspect_ratio).round(half: :even), 1].max]
  end

  # Contoh A4 dari "How Claude resizes and pads images":
  p resized_size(1075, 1520) # => [924, 1307]
  ```
</CodeGroup>

1. Ubah ukuran gambar ke dimensi yang dikembalikan oleh helper pengubah ukuran. Jika gambar sudah sesuai dengan batas model, helper mengembalikan dimensinya tanpa perubahan dan tidak diperlukan pengubahan ukuran.
2. [Kirim gambar yang telah diubah ukurannya](/docs/id/build-with-claude/vision#send-images-to-claude) ke API. Jangan tambahkan padding sendiri. Claude menangani padding, dan padding tidak menggeser titik asal koordinat.
3. Dalam prompt Anda, minta koordinat piksel secara eksplisit. Misalnya: *"Kembalikan titik klik untuk tombol Submit sebagai `[x, y]` dalam koordinat piksel."*
4. Gunakan koordinat yang dikembalikan secara langsung terhadap gambar yang Anda kirim. Jika Anda memerlukan koordinat yang dinormalisasi, bagi dengan dimensi gambar yang Anda kirim, bukan dengan dimensi gambar asli dan bukan dengan dimensi yang telah diberi padding.

<Note>
  Endpoint [Penghitungan token](/docs/id/build-with-claude/token-counting) memperkirakan biaya token sebuah gambar dari dimensinya tanpa memprosesnya secara penuh, sehingga penghitungan yang berhasil tidak berarti gambar tersebut berada dalam [batas permintaan](/docs/id/build-with-claude/vision#request-limits) Messages API. Sebuah gambar dapat berhasil dihitung dan tetap ditolak ketika Anda mengirimkannya.
</Note>

## Skalakan ulang koordinat ketika Anda tidak dapat mengubah ukuran terlebih dahulu

Jika Anda tidak dapat mengubah ukuran terlebih dahulu (misalnya, ketika gambar berasal dari sistem hulu yang tidak dapat Anda modifikasi), gunakan helper pengubah ukuran dari [Ubah ukuran gambar Anda sebelum mengunggah](#resize-your-image-before-uploading) untuk memulihkan dimensi yang dilihat Claude, lalu petakan koordinat yang dikembalikan Claude menjadi koordinat yang dinormalisasi atau kembali ke gambar asli Anda. Claude mengubah ukuran gambar yang terlalu besar alih-alih menolaknya, hingga [batas permintaan](/docs/id/build-with-claude/vision#request-limits) API. Di luar batas tersebut, permintaan akan gagal dengan kesalahan validasi. Berikan batas tingkat yang sesuai dengan model yang Anda panggil: batas tingkat yang salah akan memulihkan dimensi hasil pengubahan ukuran yang salah dan secara diam-diam menggeser setiap koordinat. Pendekatan ini memerlukan pengetahuan tentang dimensi piksel gambar yang Anda unggah, sehingga tidak berlaku untuk unggahan PDF.

<CodeGroup>
  ```bash cURL
  # Konversi koordinat lokal ini tidak membuat permintaan API, jadi tidak ada
  # yang ditampilkan untuk cURL. Lihat tab SDK.
  ```

  ```bash CLI
  # Konversi koordinat lokal ini tidak membuat permintaan API, jadi tidak ada
  # yang perlu ditampilkan untuk CLI. Lihat tab SDK.
  ```

  ```python Python
  # Helper ini memanggil resized_size dari contoh pengubahan ukuran di halaman ini.
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


  # Sudut tabel yang dikembalikan Claude di (462, 653.5) pada halaman A4 yang diubah ukurannya
  # dipetakan kembali ke gambar asli 1075x1520 seperti ini:
  rel_x, rel_y = to_relative_coordinates(462, 653.5, 1075, 1520)
  print((rel_x * 1075, rel_y * 1520))  # (537.5, 760.0)
  ```

  ```typescript TypeScript
  // Helper ini memanggil resizedSize dari contoh resize di halaman ini.
  /**
   * Map a pixel coordinate returned by Claude to relative coordinates in [0, 1].
   *
   * Pass the dimensions of the image you uploaded. For high-resolution-tier
   * models, use maxEdge = 2576 and maxTokens = 4784.
   */
  function toRelativeCoordinates(
    x: number,
    y: number,
    originalWidth: number,
    originalHeight: number,
    maxEdge = 1568,
    maxTokens = 1568
  ): [number, number] {
    const [resizedW, resizedH] = resizedSize(
      originalWidth,
      originalHeight,
      maxEdge,
      maxTokens
    );
    return [x / resizedW, y / resizedH];
  }

  // Sudut tabel yang dikembalikan Claude di (462, 653.5) pada halaman A4 yang di-resize
  // dipetakan kembali ke gambar asli 1075x1520 seperti ini:
  const [relX, relY] = toRelativeCoordinates(462, 653.5, 1075, 1520);
  console.log([relX * 1075, relY * 1520]); // [ 537.5, 760 ]
  ```

  ```csharp C#
  // Helper ini memanggil ResizedSize dari contoh pengubahan ukuran di halaman ini.
  // Memetakan koordinat piksel yang dikembalikan Claude ke koordinat relatif dalam
  // [0, 1]. Berikan dimensi gambar yang Anda unggah, dan batas tier yang sama
  // yang digunakan untuk ResizedSize.
  static (double X, double Y) ToRelativeCoordinates(
      double x, double y, int originalWidth, int originalHeight,
      int maxEdge = 1568, int maxTokens = 1568)
  {
      (int resizedW, int resizedH) =
          ResizedSize(originalWidth, originalHeight, maxEdge, maxTokens);
      return (x / resizedW, y / resizedH);
  }

  // Sudut tabel yang dikembalikan Claude di (462, 653.5) pada halaman A4 yang diubah ukurannya
  // dipetakan kembali ke gambar asli 1075x1520 seperti ini:
  (double relX, double relY) = ToRelativeCoordinates(462, 653.5, 1075, 1520);
  Console.WriteLine((relX * 1075, relY * 1520)); // (537.5, 760)
  ```

  ```go Go
  // Helper ini memanggil resizedSize dari contoh resize di halaman ini.

  // toRelativeCoordinates memetakan koordinat piksel yang dikembalikan Claude ke
  // koordinat relatif dalam [0, 1]. Berikan dimensi gambar yang Anda
  // unggah, dan batas tier yang sama seperti yang digunakan untuk resizedSize.
  func toRelativeCoordinates(
  	x, y float64,
  	originalWidth, originalHeight, maxEdge, maxTokens int,
  ) (float64, float64) {
  	resizedW, resizedH := resizedSize(originalWidth, originalHeight, maxEdge, maxTokens)
  	return x / float64(resizedW), y / float64(resizedH)
  }

  // Untuk memetakan kembali ke ruang piksel gambar asli Anda, kalikan dengan dimensi
  // asli: sudut tabel yang dikembalikan di (462, 653.5) pada halaman A4 yang di-resize
  // adalah (relX*1075, relY*1520) = (537.5, 760) pada gambar asli 1075x1520.
  ```

  ```java Java
  // Helper ini memanggil resizedSize dari contoh resize di halaman ini.
  /** A coordinate scaled into the [0, 1] range on both axes. */
  record RelativeCoordinate(double x, double y) {}

  /**
   * Map a pixel coordinate returned by Claude to relative coordinates in
   * [0, 1]. Pass the dimensions of the image you uploaded, and the same tier
   * limits used for resizedSize.
   */
  static RelativeCoordinate toRelativeCoordinates(
          double x, double y, int originalWidth, int originalHeight, int maxEdge, int maxTokens) {
      Size resized = resizedSize(originalWidth, originalHeight, maxEdge, maxTokens);
      return new RelativeCoordinate(x / resized.width(), y / resized.height());
  }

  // Untuk memetakan kembali ke ruang piksel gambar asli Anda, kalikan dengan dimensi
  // asli: sudut tabel yang dikembalikan di (462, 653.5) pada halaman A4 yang di-resize
  // adalah (relative.x() * 1075, relative.y() * 1520) = (537.5, 760) pada
  // gambar asli 1075x1520.
  ```

  ```php PHP
  // Helper ini memanggil resizedSize() dari contoh pengubahan ukuran di halaman ini.
  /**
   * Map a pixel coordinate returned by Claude to relative coordinates in
   * [0, 1], as [x, y]. Pass the dimensions of the image you uploaded, and the
   * same tier limits used for resizedSize.
   */
  function toRelativeCoordinates(
      float $x,
      float $y,
      int $originalWidth,
      int $originalHeight,
      int $maxEdge = 1568,
      int $maxTokens = 1568,
  ): array {
      [$resizedW, $resizedH] = resizedSize($originalWidth, $originalHeight, $maxEdge, $maxTokens);

      return [$x / $resizedW, $y / $resizedH];
  }

  // Sudut tabel yang dikembalikan Claude di (462, 653.5) pada halaman A4 yang diubah ukurannya
  // dipetakan kembali ke gambar asli 1075x1520 seperti ini:
  [$relX, $relY] = toRelativeCoordinates(462, 653.5, 1075, 1520);
  echo '(' . $relX * 1075 . ', ' . $relY * 1520 . ")\n"; // (537.5, 760)
  ```

  ```ruby Ruby
  # Helper ini memanggil resized_size dari contoh pengubahan ukuran di halaman ini.
  # Memetakan koordinat piksel yang dikembalikan Claude ke koordinat relatif dalam
  # [0, 1], sebagai [x, y]. Berikan dimensi gambar yang Anda unggah, dan
  # batas tingkat yang sama yang digunakan untuk resized_size.
  def to_relative_coordinates(
    x, y, original_width, original_height, max_edge = 1568, max_tokens = 1568
  )
    resized_w, resized_h = resized_size(original_width, original_height, max_edge, max_tokens)
    [x.fdiv(resized_w), y.fdiv(resized_h)]
  end

  # Sudut tabel yang Claude kembalikan di (462, 653.5) pada halaman A4 yang diubah ukurannya
  # dipetakan kembali ke gambar asli 1075x1520 seperti ini:
  rel_x, rel_y = to_relative_coordinates(462, 653.5, 1075, 1520)
  p [rel_x * 1075, rel_y * 1520] # => [537.5, 760.0]
  ```
</CodeGroup>

Padding hanya diterapkan pada tepi bawah dan kanan, sehingga titik asal tidak bergeser dan penskalaan ulang linear per sumbu sudah cukup. Batasi (clamp) koordinat yang dikembalikan ke dimensi hasil pengubahan ukuran sebelum menskalakan ulang, sehingga titik yang sedikit berada di luar gambar tidak dapat terpetakan di luar gambar asli Anda.

Koordinat relatif dikalikan dengan permukaan apa pun yang Anda gunakan: gambar asli, hasil pindaian resolusi penuh, atau layar. Ketika Anda bertindak pada layar dan piksel tangkapan layar berbeda dari koordinat logis (tampilan HiDPI), bagi juga dengan faktor skala tampilan. [Panduan penskalaan alat computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions) membahas pola tersebut.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Agent Skills" icon="stack" href="/docs/id/agents-and-tools/agent-skills/overview">
    Agent Skills adalah kemampuan modular yang memperluas fungsionalitas Claude. Setiap Skill mengemas instruksi, metadata, dan sumber daya opsional (skrip, templat) yang digunakan Claude secara otomatis saat relevan.
  </Card>

  <Card title="Alat computer use" icon="computer" href="/docs/id/agents-and-tools/tool-use/computer-use-tool">
    Berikan Claude kendali tangkapan layar, mouse, dan keyboard atas lingkungan desktop dengan alat computer use.
  </Card>

  <Card title="Dukungan PDF" icon="file" href="/docs/id/build-with-claude/pdf-support">
    Proses PDF dengan Claude. Ekstrak teks, analisis grafik, dan pahami konten visual dari dokumen Anda.
  </Card>

  <Card title="Penghitungan token" icon="calculator" href="/docs/id/build-with-claude/token-counting">
    Hitung token dalam sebuah pesan sebelum Anda mengirimkannya ke Claude. Gunakan jumlah token untuk mengelola batas laju dan biaya, membuat keputusan perutean model, dan menyesuaikan prompt dengan panjang target.
  </Card>
</CardGroup>
