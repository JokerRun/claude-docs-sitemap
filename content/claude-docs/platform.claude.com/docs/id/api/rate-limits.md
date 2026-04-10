---
source: platform
url: https://platform.claude.com/docs/id/api/rate-limits
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: ea91862168812ffaa8f5f77d4ba7d1d1ffe79facdb3ad17055167c981c50066a
---

# Batas laju

Untuk mengurangi penyalahgunaan dan mengelola kapasitas pada API, ada batasan tentang seberapa banyak organisasi dapat menggunakan Claude API.

---

Ada dua jenis batasan:

1. **Batas pengeluaran** menetapkan biaya bulanan maksimum yang dapat dikeluarkan organisasi untuk penggunaan API.
2. **Batas laju** menetapkan jumlah maksimum permintaan API yang dapat dilakukan organisasi selama periode waktu yang ditentukan.

API memberlakukan batasan yang dikonfigurasi layanan pada tingkat organisasi, tetapi Anda juga dapat menetapkan batasan yang dapat dikonfigurasi pengguna untuk ruang kerja organisasi Anda.

Batasan ini berlaku untuk penggunaan Tier Standar dan Prioritas. Untuk informasi lebih lanjut tentang Tier Prioritas, yang menawarkan tingkat layanan yang ditingkatkan sebagai imbalan komitmen pengeluaran, lihat [Service Tiers](/docs/id/api/service-tiers).

## Tentang batas laju

* Batasan dirancang untuk mencegah penyalahgunaan API, sambil meminimalkan dampak pada pola penggunaan pelanggan yang umum.
* Batasan ditentukan oleh **tingkat penggunaan**, di mana setiap tingkat dikaitkan dengan set batasan pengeluaran dan laju yang berbeda.
* Organisasi Anda akan meningkat tingkat secara otomatis saat Anda mencapai ambang batas tertentu saat menggunakan API.
  Batasan ditetapkan pada tingkat organisasi. Anda dapat melihat batasan organisasi Anda di halaman [Limits](/settings/limits) di [Claude Console](/).
* Anda mungkin mencapai batas laju selama interval waktu yang lebih pendek. Misalnya, laju 60 permintaan per menit (RPM) dapat diberlakukan sebagai 1 permintaan per detik. Ledakan permintaan singkat dapat melampaui batas dan memicu kesalahan batas laju.
* Batasan yang dijelaskan di bawah adalah batasan tingkat standar. Jika Anda mencari batasan yang lebih tinggi dan khusus atau Tier Prioritas untuk tingkat layanan yang ditingkatkan, hubungi penjualan di halaman [Limits](/settings/limits).
* API menggunakan [algoritma token bucket](https://en.wikipedia.org/wiki/Token_bucket) untuk melakukan pembatasan laju. Ini berarti kapasitas Anda terus-menerus diisi kembali hingga batas maksimum Anda, daripada direset pada interval tetap.
* Semua batasan yang dijelaskan di sini mewakili penggunaan maksimum yang diizinkan, bukan minimum yang dijamin. Batasan ini dimaksudkan untuk mengurangi pengeluaran yang tidak disengaja dan memastikan distribusi sumber daya yang adil di antara pengguna.

## Batas pengeluaran

Setiap tingkat penggunaan memiliki batasan tentang berapa banyak yang dapat Anda keluarkan untuk API setiap bulan kalender. Setelah Anda mencapai batas pengeluaran tingkat Anda, sampai Anda memenuhi syarat untuk tingkat berikutnya, Anda harus menunggu sampai bulan berikutnya untuk dapat menggunakan API lagi.

Untuk memenuhi syarat untuk tingkat berikutnya, Anda harus memenuhi persyaratan setoran. Untuk meminimalkan risiko pendanaan berlebihan akun Anda, Anda tidak dapat menyetor lebih dari batas pengeluaran bulanan Anda.

### Persyaratan untuk meningkatkan tingkat
<table>
  <thead>
    <tr>
      <th>Tingkat Penggunaan</th>
      <th>Pembelian Kredit</th>
      <th>Pembelian Kredit Maksimum</th>
      <th>Batas Pengeluaran Bulanan</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Tier 1</td>
      <td>\$5</td>
      <td>\$100</td>
      <td>\$100</td>
    </tr>
    <tr>
      <td>Tier 2</td>
      <td>\$40</td>
      <td>\$500</td>
      <td>\$500</td>
    </tr>
    <tr>
      <td>Tier 3</td>
      <td>\$200</td>
      <td>\$1,000</td>
      <td>\$1,000</td>
    </tr>
    <tr>
      <td>Tier 4</td>
      <td>\$400</td>
      <td>\$200,000</td>
      <td>\$200,000</td>
    </tr>
    <tr>
      <td>Penagihan Bulanan</td>
      <td>N/A</td>
      <td>N/A</td>
      <td>Tanpa batas</td>
    </tr>
  </tbody>
</table>

<Note>
**Pembelian Kredit** menunjukkan pembelian kredit kumulatif (tidak termasuk pajak) yang diperlukan untuk maju ke tingkat tersebut. Anda maju segera setelah mencapai ambang batas.

**Pembelian Kredit Maksimum** membatasi jumlah maksimum yang dapat Anda tambahkan ke akun Anda dalam satu transaksi untuk mencegah pendanaan berlebihan akun.

**Batas Pengeluaran Bulanan** adalah maksimum yang dapat Anda keluarkan untuk API setiap bulan kalender pada tingkat tersebut.
</Note>

## Meningkatkan batas pengeluaran Anda

Organisasi Anda memiliki dua jenis batas pengeluaran: batas yang ditetapkan pelanggan yang Anda kontrol langsung, dan batas yang diberlakukan tingkat yang ditetapkan oleh tingkat penggunaan Anda. Masing-masing memiliki proses berbeda untuk meningkatkannya.

### Batas pengeluaran yang ditetapkan pelanggan

Anda dapat menetapkan batas pengeluaran lebih rendah dari batas tingkat Anda untuk mengontrol biaya. Untuk menyesuaikannya:

<Steps>
  <Step title="Navigasi ke halaman Limits">
    Buka [Settings > Limits](/settings/limits) di Claude Console.
  </Step>
  <Step title="Buka editor batas pengeluaran">
    Di bagian **Spend limits**, klik **Change Limit** (atau **Set spend limit** jika tidak ada batas yang ditetapkan saat ini).
  </Step>
  <Step title="Sesuaikan batas pengeluaran Anda">
    Masukkan nilai baru. Batas yang ditetapkan pelanggan Anda tidak dapat melebihi batas tingkat saat ini Anda.
  </Step>
</Steps>

### Batas pengeluaran yang diberlakukan tingkat

Ketika Anda membutuhkan batas lebih tinggi dari batas tingkat Anda (batas Tier 4 adalah $200,000 per bulan), klik **Contact Sales** di halaman [Limits](/settings/limits). Ini membuka formulir kontak di tab baru, dan anggota tim penjualan akan menindaklanjuti melalui email ketika organisasi Anda ditingkatkan.

Penagihan Bulanan menghilangkan batas pengeluaran bulanan sepenuhnya dan menggunakan syarat pembayaran Net-30 secara default.

<Note>
Dukungan juga dapat menaikkan batas yang diberlakukan tingkat. Untuk kebutuhan mendesak, hubungi [support](https://support.anthropic.com).
</Note>

## Batas laju

Batas laju untuk Messages API diukur dalam permintaan per menit (RPM), token input per menit (ITPM), dan token output per menit (OTPM) untuk setiap kelas model.
Jika Anda melampaui salah satu batas laju, Anda akan mendapatkan [429 error](/docs/id/api/errors) yang menjelaskan batas laju mana yang terlampaui, bersama dengan header `retry-after` yang menunjukkan berapa lama waktu tunggu.

<Note>
Anda mungkin juga mengalami kesalahan 429 karena batasan akselerasi pada API jika organisasi Anda mengalami peningkatan penggunaan yang tajam. Untuk menghindari mencapai batasan akselerasi, tingkatkan lalu lintas Anda secara bertahap dan pertahankan pola penggunaan yang konsisten.
</Note>

### ITPM yang menyadari cache

Banyak penyedia API menggunakan batas "token per menit" (TPM) gabungan yang mungkin mencakup semua token, baik yang di-cache maupun tidak di-cache, input dan output. **Untuk sebagian besar model Claude, hanya token input yang tidak di-cache yang dihitung menuju batas laju ITPM Anda.** Ini adalah keuntungan utama yang membuat batas laju secara efektif lebih tinggi daripada yang mungkin awalnya terlihat.

Batas laju ITPM diperkirakan di awal setiap permintaan, dan perkiraan disesuaikan selama permintaan untuk mencerminkan jumlah sebenarnya dari token input yang digunakan.

Berikut adalah apa yang dihitung menuju ITPM:
- `input_tokens` (token setelah titik henti cache terakhir) ✓ **Dihitung menuju ITPM**
- `cache_creation_input_tokens` (token yang ditulis ke cache) ✓ **Dihitung menuju ITPM**
- `cache_read_input_tokens` (token yang dibaca dari cache) ✗ **TIDAK dihitung menuju ITPM** untuk sebagian besar model

<Note>
Bidang `input_tokens` hanya mewakili token yang muncul **setelah titik henti cache terakhir Anda**, bukan semua token input dalam permintaan Anda. Untuk menghitung total token input:

```text
total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
```

Ini berarti ketika Anda memiliki konten yang di-cache, `input_tokens` biasanya akan jauh lebih kecil daripada total input Anda. Misalnya, dengan dokumen yang di-cache 200k token dan pertanyaan pengguna 50 token, Anda akan melihat `input_tokens: 50` meskipun total input adalah 200,050 token.

Untuk tujuan batas laju pada sebagian besar model, hanya `input_tokens` + `cache_creation_input_tokens` yang dihitung menuju batas ITPM Anda, membuat [prompt caching](/docs/id/build-with-claude/prompt-caching) cara yang efektif untuk meningkatkan throughput efektif Anda.
</Note>

**Contoh**: Dengan batas ITPM 2.000.000 dan tingkat cache hit 80%, Anda dapat secara efektif memproses 10.000.000 total token input per menit (2M tidak di-cache + 8M di-cache), karena token yang di-cache tidak dihitung menuju batas laju Anda.

<Note>
Beberapa model yang lebih lama (ditandai dengan † dalam tabel batas laju di bawah) juga menghitung `cache_read_input_tokens` menuju batas laju ITPM.

Untuk semua model tanpa penanda †, token input yang di-cache tidak dihitung menuju batas laju dan ditagih dengan tarif yang dikurangi (10% dari harga token input dasar). Ini berarti Anda dapat mencapai throughput efektif yang jauh lebih tinggi dengan menggunakan [prompt caching](/docs/id/build-with-claude/prompt-caching).
</Note>

<Tip>
**Maksimalkan batas laju Anda dengan prompt caching**

Untuk memanfaatkan batas laju Anda sebaik-baiknya, gunakan [prompt caching](/docs/id/build-with-claude/prompt-caching) untuk konten berulang seperti:
- Instruksi sistem dan prompt
- Dokumen konteks besar
- Definisi alat
- Riwayat percakapan

Dengan caching yang efektif, Anda dapat secara dramatis meningkatkan throughput aktual Anda tanpa meningkatkan batas laju Anda. Pantau tingkat cache hit Anda di halaman [Usage](/usage) untuk mengoptimalkan strategi caching Anda.
</Tip>

Batas laju OTPM dievaluasi secara real-time saat token output diproduksi, hanya menghitung token aktual yang dihasilkan. Parameter `max_tokens` tidak mempengaruhi perhitungan batas laju OTPM, jadi tidak ada kerugian batas laju untuk menetapkan nilai `max_tokens` yang lebih tinggi.

Batas laju diterapkan secara terpisah untuk setiap model; oleh karena itu Anda dapat menggunakan model berbeda hingga batas masing-masing secara bersamaan.
Anda dapat memeriksa batas laju saat ini dan perilaku Anda di [Claude Console](/settings/limits).

<Note>
Batas laju saat ini dibagikan di semua nilai `inference_geo`. Permintaan dengan `inference_geo: "us"` dan `inference_geo: "global"` menarik dari kumpulan batas laju yang sama.
</Note>

<Tabs>
<Tab title="Tier 1">
| Model                                                                                        | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
| -------------------------------------------------------------------------------------------- | --------------------------------- | -------------------------------------- | --------------------------------------- |
| Claude Sonnet 4.x<sup>**</sup>                                                               | 50                                | 30,000                                 | 8,000                                   |
| Claude Sonnet 3.7 ([deprecated](/docs/id/about-claude/model-deprecations))                   | 50                                | 20,000                                 | 8,000                                   |
| Claude Haiku 4.5                                                                             | 50                                | 50,000                                 | 10,000                                  |
| Claude Haiku 3.5 ([deprecated](/docs/id/about-claude/model-deprecations))                    | 50                                | 50,000<sup>†</sup>                     | 10,000                                  |
| Claude Haiku 3                                                                               | 50                                | 50,000<sup>†</sup>                     | 10,000                                  |
| Claude Opus 4.x<sup>*</sup>                                                                  | 50                                | 30,000                                 | 8,000                                   |

</Tab>
<Tab title="Tier 2">
| Model                                                                                        | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
| -------------------------------------------------------------------------------------------- | --------------------------------- | -------------------------------------- | --------------------------------------- |
| Claude Sonnet 4.x<sup>**</sup>                                                               | 1,000                             | 450,000                                | 90,000                                  |
| Claude Sonnet 3.7 ([deprecated](/docs/id/about-claude/model-deprecations))                   | 1,000                             | 40,000                                 | 16,000                                  |
| Claude Haiku 4.5                                                                             | 1,000                             | 450,000                                | 90,000                                  |
| Claude Haiku 3.5 ([deprecated](/docs/id/about-claude/model-deprecations))                    | 1,000                             | 100,000<sup>†</sup>                    | 20,000                                  |
| Claude Haiku 3                                                                               | 1,000                             | 100,000<sup>†</sup>                    | 20,000                                  |
| Claude Opus 4.x<sup>*</sup>                                                                  | 1,000                             | 450,000                                | 90,000                                  |

</Tab>
<Tab title="Tier 3">
| Model                                                                                        | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
| -------------------------------------------------------------------------------------------- | --------------------------------- | -------------------------------------- | --------------------------------------- |
| Claude Sonnet 4.x<sup>**</sup>                                                               | 2,000                             | 800,000                                | 160,000                                 |
| Claude Sonnet 3.7 ([deprecated](/docs/id/about-claude/model-deprecations))                   | 2,000                             | 80,000                                 | 32,000                                  |
| Claude Haiku 4.5                                                                             | 2,000                             | 1,000,000                              | 200,000                                 |
| Claude Haiku 3.5 ([deprecated](/docs/id/about-claude/model-deprecations))                    | 2,000                             | 200,000<sup>†</sup>                    | 40,000                                  |
| Claude Haiku 3                                                                               | 2,000                             | 200,000<sup>†</sup>                    | 40,000                                  |
| Claude Opus 4.x<sup>*</sup>                                                                  | 2,000                             | 800,000                                | 160,000                                 |

</Tab>
<Tab title="Tier 4">
| Model                                                                                        | Permintaan maksimum per menit (RPM) | Token input maksimum per menit (ITPM) | Token output maksimum per menit (OTPM) |
| -------------------------------------------------------------------------------------------- | --------------------------------- | -------------------------------------- | --------------------------------------- |
| Claude Sonnet 4.x<sup>**</sup>                                                               | 4,000                             | 2,000,000                              | 400,000                                 |
| Claude Sonnet 3.7 ([deprecated](/docs/id/about-claude/model-deprecations))                   | 4,000                             | 200,000                                | 80,000                                  |
| Claude Haiku 4.5                                                                             | 4,000                             | 4,000,000                              | 800,000                                 |
| Claude Haiku 3.5 ([deprecated](/docs/id/about-claude/model-deprecations))                    | 4,000                             | 400,000<sup>†</sup>                    | 80,000                                  |
| Claude Haiku 3                                                                               | 4,000                             | 400,000<sup>†</sup>                    | 80,000                                  |
| Claude Opus 4.x<sup>*</sup>                                                                  | 4,000                             | 2,000,000                              | 400,000                                 |

</Tab>
<Tab title="Custom">
Jika Anda mencari batasan yang lebih tinggi untuk kasus penggunaan Enterprise, hubungi penjualan melalui [Claude Console](/settings/limits).
</Tab>
</Tabs>

_<sup>* - Batas laju Opus adalah batas total yang berlaku untuk lalu lintas gabungan di Opus 4.6, Opus 4.5, Opus 4.1, dan Opus 4.</sup>_

_<sup>** - Batas laju Sonnet 4.x adalah batas total yang berlaku untuk lalu lintas gabungan di Sonnet 4.6, Sonnet 4.5, dan Sonnet 4.</sup>_

_<sup>† - Batas menghitung `cache_read_input_tokens` menuju penggunaan ITPM.</sup>_

### Message Batches API

Message Batches API memiliki set batas laju sendiri yang dibagikan di semua model. Ini termasuk batas permintaan per menit (RPM) untuk semua endpoint API dan batas jumlah permintaan batch yang dapat berada dalam antrian pemrosesan pada waktu yang sama. "Permintaan batch" di sini mengacu pada bagian dari Message Batch. Anda dapat membuat Message Batch yang berisi ribuan permintaan batch, masing-masing dihitung menuju batas ini. Permintaan batch dianggap bagian dari antrian pemrosesan ketika belum berhasil diproses oleh model.

<Tabs>
<Tab title="Tier 1">
| Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrian pemrosesan | Permintaan batch maksimum per batch |
| --------------------------------- | ------------------------------------------ | -------------------------------- |
| 50                                | 100,000                                    | 100,000                          |
</Tab>
<Tab title="Tier 2">
| Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrian pemrosesan | Permintaan batch maksimum per batch |
| --------------------------------- | ------------------------------------------ | -------------------------------- |
| 1,000                             | 200,000                                    | 100,000                          |
</Tab>
<Tab title="Tier 3">
| Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrian pemrosesan | Permintaan batch maksimum per batch |
| --------------------------------- | ------------------------------------------ | -------------------------------- |
| 2,000                             | 300,000                                    | 100,000                          |
</Tab>
<Tab title="Tier 4">
| Permintaan maksimum per menit (RPM) | Permintaan batch maksimum dalam antrian pemrosesan | Permintaan batch maksimum per batch |
| --------------------------------- | ------------------------------------------ | -------------------------------- |
| 4,000                             | 500,000                                    | 100,000                          |
</Tab>
<Tab title="Custom">
Jika Anda mencari batasan yang lebih tinggi untuk kasus penggunaan Enterprise, hubungi penjualan melalui [Claude Console](/settings/limits).
</Tab>
</Tabs>

### Managed Agents

Endpoint [Claude Managed Agents](/docs/id/managed-agents/overview) dibatasi laju per organisasi. Batasan ini terpisah dari batas laju Messages API di atas.

| Operasi | Batas |
| --- | --- |
| Buat endpoint (agen, sesi, lingkungan, dll.) | 60 permintaan per menit |
| Baca endpoint (ambil, daftar, alirkan, dll.) | 600 permintaan per menit |

### Batas laju mode cepat

Saat menggunakan [fast mode](/docs/id/build-with-claude/fast-mode) (beta: research preview) dengan `speed: "fast"` pada Opus 4.6, batas laju khusus berlaku yang terpisah dari batas laju Opus standar. Ketika batas laju mode cepat terlampaui, API mengembalikan kesalahan `429` dengan header `retry-after`.

Respons mencakup header `anthropic-fast-*` yang menunjukkan status batas laju mode cepat Anda. Lihat [dokumentasi fast mode](/docs/id/build-with-claude/fast-mode#rate-limits) untuk detail tentang header ini.

### Memantau batas laju Anda di Console

Anda dapat memantau penggunaan batas laju Anda di halaman [Usage](/usage) dari [Claude Console](/).

Selain menyediakan bagan token dan permintaan, halaman Usage menyediakan dua bagan batas laju terpisah. Gunakan bagan ini untuk melihat berapa banyak ruang yang Anda miliki untuk tumbuh, kapan Anda mungkin mencapai penggunaan puncak, lebih memahami batas laju apa yang harus diminta, atau bagaimana Anda dapat meningkatkan tingkat caching Anda. Bagan memvisualisasikan sejumlah metrik untuk batas laju tertentu (misalnya per model):

- Bagan **Rate Limit - Input Tokens** mencakup:
  - Maksimum per jam token input yang tidak di-cache per menit
  - Batas laju token input per menit saat ini Anda
  - Tingkat cache untuk token input Anda (yaitu persentase token input yang dibaca dari cache)
- Bagan **Rate Limit - Output Tokens** mencakup:
  - Maksimum per jam token output per menit
  - Batas laju token output per menit saat ini Anda

## Menetapkan batasan yang lebih rendah untuk Workspaces

Untuk informasi lebih lanjut tentang ruang kerja, lihat [Workspaces](/docs/id/build-with-claude/workspaces).

Untuk melindungi Workspaces di Organisasi Anda dari potensi penggunaan berlebihan, Anda dapat menetapkan batasan pengeluaran dan laju khusus per Workspace.

Contoh: Jika batas Organisasi Anda adalah 40.000 token input per menit dan 8.000 token output per menit, Anda mungkin membatasi satu Workspace ke 30.000 total token per menit. Ini melindungi Workspaces lain dari potensi penggunaan berlebihan dan memastikan distribusi sumber daya yang lebih adil di seluruh Organisasi Anda. Token per menit yang tidak digunakan yang tersisa (atau lebih, jika Workspace itu tidak menggunakan batas) kemudian tersedia untuk Workspaces lain gunakan.

Catatan:
- Anda tidak dapat menetapkan batasan pada Workspace default.
- Jika tidak ditetapkan, batasan Workspace cocok dengan batas Organisasi.
- Batasan di seluruh organisasi selalu berlaku, bahkan jika batasan Workspace ditambahkan hingga lebih banyak.
- Dukungan untuk batasan token input dan output akan ditambahkan ke Workspaces di masa depan.

## Header respons

Respons API mencakup header yang menunjukkan batas laju yang diberlakukan, penggunaan saat ini, dan kapan batas akan direset.

Header berikut dikembalikan:

| Header                                        | Deskripsi                                                                                                                                     |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `retry-after`                                 | Jumlah detik untuk menunggu sampai Anda dapat mencoba ulang permintaan. Percobaan ulang lebih awal akan gagal.                                                      |
| `anthropic-ratelimit-requests-limit`          | Jumlah maksimum permintaan yang diizinkan dalam periode batas laju apa pun.                                                                            |
| `anthropic-ratelimit-requests-remaining`      | Jumlah permintaan yang tersisa sebelum dibatasi laju.                                                                                     |
| `anthropic-ratelimit-requests-reset`          | Waktu ketika batas laju permintaan akan sepenuhnya diisi kembali, disediakan dalam format RFC 3339.                                                    |
| `anthropic-ratelimit-tokens-limit`            | Jumlah maksimum token yang diizinkan dalam periode batas laju apa pun.                                                                              |
| `anthropic-ratelimit-tokens-remaining`        | Jumlah token yang tersisa (dibulatkan ke seribu terdekat) sebelum dibatasi laju.                                                     |
| `anthropic-ratelimit-tokens-reset`            | Waktu ketika batas laju token akan sepenuhnya diisi kembali, disediakan dalam format RFC 3339.                                                      |
| `anthropic-ratelimit-input-tokens-limit`      | Jumlah maksimum token input yang diizinkan dalam periode batas laju apa pun.                                                                        |
| `anthropic-ratelimit-input-tokens-remaining`  | Jumlah token input yang tersisa (dibulatkan ke seribu terdekat) sebelum dibatasi laju.                                               |
| `anthropic-ratelimit-input-tokens-reset`      | Waktu ketika batas laju token input akan sepenuhnya diisi kembali, disediakan dalam format RFC 3339.                                                |
| `anthropic-ratelimit-output-tokens-limit`     | Jumlah maksimum token output yang diizinkan dalam periode batas laju apa pun.                                                                       |
| `anthropic-ratelimit-output-tokens-remaining` | Jumlah token output yang tersisa (dibulatkan ke seribu terdekat) sebelum dibatasi laju.                                              |
| `anthropic-ratelimit-output-tokens-reset`     | Waktu ketika batas laju token output akan sepenuhnya diisi kembali, disediakan dalam format RFC 3339.                                               |
| `anthropic-priority-input-tokens-limit`       | Jumlah maksimum token input Priority Tier yang diizinkan dalam periode batas laju apa pun. (Hanya Priority Tier)                                     |
| `anthropic-priority-input-tokens-remaining`   | Jumlah token input Priority Tier yang tersisa (dibulatkan ke seribu terdekat) sebelum dibatasi laju. (Hanya Priority Tier)            |
| `anthropic-priority-input-tokens-reset`       | Waktu ketika batas laju token input Priority Tier akan sepenuhnya diisi kembali, disediakan dalam format RFC 3339. (Hanya Priority Tier)             |
| `anthropic-priority-output-tokens-limit`      | Jumlah maksimum token output Priority Tier yang diizinkan dalam periode batas laju apa pun. (Hanya Priority Tier)                                    |
| `anthropic-priority-output-tokens-remaining`  | Jumlah token output Priority Tier yang tersisa (dibulatkan ke seribu terdekat) sebelum dibatasi laju. (Hanya Priority Tier)           |
| `anthropic-priority-output-tokens-reset`      | Waktu ketika batas laju token output Priority Tier akan sepenuhnya diisi kembali, disediakan dalam format RFC 3339. (Hanya Priority Tier)            |

Header `anthropic-ratelimit-tokens-*` menampilkan nilai untuk batas yang paling ketat saat ini berlaku. Misalnya, jika Anda telah melampaui batas token per menit Workspace, header akan berisi nilai batas laju token per menit Workspace. Jika batasan Workspace tidak berlaku, header akan mengembalikan total token yang tersisa, di mana total adalah jumlah token input dan output. Pendekatan ini memastikan bahwa Anda memiliki visibilitas ke dalam kendala yang paling relevan pada penggunaan API saat ini Anda.