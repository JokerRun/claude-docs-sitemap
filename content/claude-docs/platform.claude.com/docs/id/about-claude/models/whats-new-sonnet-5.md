---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/whats-new-sonnet-5
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 64d8276368e77dd13be6a3a51cdfca8c994c934b996f830289731aad55fbdb4e
---

# Apa yang baru di Claude Sonnet 5

Ikhtisar fitur baru dan perubahan perilaku di Claude Sonnet 5.

---

Claude Sonnet 5 adalah generasi berikutnya dari keluarga model Sonnet Anthropic. Model ini merupakan peningkatan drop-in untuk Claude Sonnet 4.6 dengan tiga perubahan perilaku: [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) aktif secara default, extended thinking (pemikiran diperpanjang) manual sekarang mengembalikan error 400 (fitur ini telah usang pada Claude Sonnet 4.6), dan mengatur parameter sampling (`temperature`, `top_p`, `top_k`) ke nilai non-default mengembalikan error 400. Halaman ini merangkum semua hal baru saat peluncuran, termasuk tokenizer baru.

## Model baru

| Model           | ID model API      | Deskripsi                                         |
| --------------- | ----------------- | ------------------------------------------------- |
| Claude Sonnet 5 | `claude-sonnet-5` | Kombinasi terbaik antara kecepatan dan kecerdasan |

Claude Sonnet 5 mendukung [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) secara default (1M token adalah nilai default sekaligus maksimum; tidak ada varian konteks yang lebih kecil), maksimum 128k token output, [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), dan rangkaian alat serta fitur platform yang sama dengan Claude Sonnet 4.6, kecuali [Priority Tier](/docs/id/api/service-tiers#supported-models), yang tidak tersedia di Claude Sonnet 5.

Untuk harga dan spesifikasi lengkap, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

## Perubahan perilaku

### Adaptive thinking aktif secara default

Pada Claude Sonnet 4.6, permintaan tanpa field `thinking` berjalan tanpa thinking. Pada Claude Sonnet 5, permintaan yang sama berjalan dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking). Untuk menonaktifkan thinking, kirimkan `thinking: {type: "disabled"}`. Karena `max_tokens` adalah batas keras untuk total output (thinking ditambah teks respons), tinjau kembali nilainya untuk beban kerja yang sebelumnya berjalan tanpa thinking di Claude Sonnet 4.6.

### Parameter sampling tidak diterima

Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default mengembalikan error 400. Hapus parameter ini saat melakukan migrasi; nilai default (atau menghilangkan parameter tersebut) akan diterima. Gunakan instruksi prompt sistem untuk mengarahkan perilaku model. Ini adalah hal baru untuk model kelas Sonnet; batasan yang sama sebelumnya diperkenalkan pada Claude Opus 4.7.

### Extended thinking manual dihapus

Extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) telah usang pada Claude Sonnet 4.6; pada Claude Sonnet 5 fitur ini dihapus dan mengembalikan error 400, sama seperti pada Claude Opus 4.8 dan Claude Opus 4.7. Gunakan adaptive thinking dengan [parameter effort](/docs/id/build-with-claude/effort) sebagai gantinya.

```python Python
# Tidak didukung pada Claude Sonnet 5 (mengembalikan 400)
thinking = {"type": "enabled", "budget_tokens": 32000}

# Gunakan ini sebagai gantinya
thinking = {"type": "adaptive"}
```

## Tokenizer baru

Claude Sonnet 5 menggunakan tokenizer baru. Teks input yang sama menghasilkan sekitar 30% lebih banyak token dibandingkan pada Claude Sonnet 4.6. Peningkatan pastinya bergantung pada konten. Ini bukan perubahan API: permintaan, respons, dan event streaming tetap memiliki bentuk yang sama, dan tidak diperlukan perubahan kode.

Perubahan ini memengaruhi semua hal yang Anda ukur atau anggarkan dalam token:

* **Jumlah token:** field `usage` dan hasil [penghitungan token](/docs/id/build-with-claude/token-counting) untuk teks yang sama lebih tinggi dibandingkan pada Claude Sonnet 4.6. Jangan gunakan kembali jumlah yang diukur terhadap model sebelumnya; hitung ulang terhadap Claude Sonnet 5.
* **Kapasitas jendela konteks dalam ukuran teks:** jendela konteks adalah 1M token, tetapi setiap token rata-rata mencakup lebih sedikit teks, sehingga jendela yang sama menampung lebih sedikit teks dibandingkan pada Claude Sonnet 4.6.
* **Anggaran `max_tokens`:** batas output yang disetel untuk Claude Sonnet 4.6 dapat memotong output yang setara pada Claude Sonnet 5. Tinjau kembali batas yang ukurannya mendekati panjang output yang Anda harapkan.
* **Biaya per permintaan:** harga per token tidak berubah (lihat [Harga](#pricing)), tetapi karena teks yang sama menghasilkan lebih banyak token, biaya permintaan yang setara dapat berbeda dari Claude Sonnet 4.6.

## Batasan API yang diwarisi dari Claude Sonnet 4.6

<Note>
  Batasan ini tidak berubah dari Claude Sonnet 4.6. Selain tiga [perubahan perilaku](#behavior-changes) (lihat [Panduan migrasi](#migration-guide)), kode yang sudah berjalan di Claude Sonnet 4.6 tidak memerlukan perubahan lain.
</Note>

### Prefilling pesan assistant tidak didukung

Melakukan prefilling pada pesan assistant mengembalikan error `400`, tidak berubah dari Claude Sonnet 4.6. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

## Peningkatan kemampuan

Claude Sonnet 5 adalah peningkatan kemampuan dibandingkan Claude Sonnet 4.6 dengan harga yang sama. Model ini juga merupakan pilihan untuk beban kerja yang membutuhkan kemampuan lebih dari yang disediakan Claude Sonnet 4.6 tanpa harus beralih ke model kelas Opus.

Peningkatan terbesar dibandingkan Claude Sonnet 4.6 ada pada tugas coding dan agentik. Untuk hasil benchmark, lihat [Transparency Hub Anthropic](https://www.anthropic.com/transparency).

## Pengamanan keamanan siber

Claude Sonnet 5 adalah model tingkat Sonnet pertama dengan pengamanan keamanan siber real-time. Permintaan yang melibatkan topik keamanan siber yang dilarang atau berisiko tinggi dapat ditolak. Penolakan dikembalikan sebagai respons HTTP 200 yang berhasil dengan `stop_reason: "refusal"`, bukan sebagai error. Lihat [Safeguards, warnings, and appeals](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals) untuk latar belakangnya.

## Harga

Claude Sonnet 5 dihargai $3 per juta token input dan $15 per juta token output, tidak berubah dari Claude Sonnet 4.6. Karena [tokenizer baru](#new-tokenizer) menghasilkan sekitar 30% lebih banyak token untuk teks yang sama, biaya permintaan yang setara dapat berbeda dari Claude Sonnet 4.6 meskipun harga per token tidak berubah. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja.

Harga perkenalan sebesar $2/$10 per juta token input/output berlaku hingga 31 Agustus 2026, setelah itu harga standar sebesar $3/$15 per juta token input/output akan berlaku.

Lihat [Harga](/docs/id/about-claude/pricing) untuk harga lengkap, termasuk tarif pemrosesan batch dan caching prompt.

## Ketersediaan

Saat peluncuran, Claude Sonnet 5 tersedia di:

* **Claude API:** tersedia untuk semua pelanggan.
* **AWS:** tersedia melalui [Claude in Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock) dan [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws). Di Amazon Bedrock, Claude Sonnet 5 juga dapat diakses melalui API `InvokeModel`, yang dilayani oleh infrastruktur yang sama dengan Claude in Amazon Bedrock. Integrasi lama [Claude on Amazon Bedrock (Opus 4.6 dan sebelumnya)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) tidak mencakup Claude Sonnet 5.
* **Google Cloud:** tersedia melalui [Claude on Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai).
* **Microsoft Foundry:** tersedia melalui [Claude in Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry).

Claude Sonnet 5 mendukung [zero data retention](/docs/id/manage-claude/api-and-data-retention) untuk organisasi dengan perjanjian ZDR.

## Panduan migrasi

Claude Sonnet 5 adalah pengganti drop-in untuk Claude Sonnet 4.6. Perbarui ID model Anda:

```python
model = "claude-sonnet-4-6"  # Before
model = "claude-sonnet-5"  # After
```

Kemudian tinjau hal-hal berikut:

1. **Anggaran dan jumlah token:** [tokenizer baru](#new-tokenizer) menghasilkan sekitar 30% lebih banyak token untuk teks yang sama. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja. Hitung ulang prompt dengan [penghitungan token](/docs/id/build-with-claude/token-counting), dan tinjau kembali batas `max_tokens` yang ukurannya mendekati panjang output yang Anda harapkan.
2. **Extended thinking:** jika Anda masih mengatur `budget_tokens`, migrasikan ke [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking). Extended thinking manual (`thinking: {type: "enabled"}`) tidak didukung dan mengembalikan error 400.
3. **Parameter sampling:** permintaan yang mengatur parameter sampling (`temperature`, `top_p`, `top_k`) ke nilai non-default mengembalikan error 400; hapus parameter tersebut saat melakukan migrasi. Definisi alat dan bentuk respons tidak berubah, dan prefilling pesan assistant memang sudah tidak didukung di Claude Sonnet 4.6.

Lihat [bagian Claude Sonnet 5 pada panduan migrasi](/docs/id/about-claude/models/migration-guide#migrating-from-claude-sonnet-4-6-to-claude-sonnet-5) untuk detailnya.

## Langkah selanjutnya

<CardGroup>
  <Card title="Ikhtisar model" icon="arrow-right" href="/docs/id/about-claude/models/overview">
    Spesifikasi dan harga lengkap untuk semua model Claude saat ini.
  </Card>

  <Card title="Penghitungan token" icon="database" href="/docs/id/build-with-claude/token-counting">
    Ukur prompt Anda dengan tokenizer baru sebelum Anda bermigrasi.
  </Card>

  <Card title="Adaptive thinking" icon="brain" href="/docs/id/build-with-claude/adaptive-thinking">
    Mode thinking aktif yang direkomendasikan pada Claude Sonnet 5.
  </Card>

  <Card title="Jendela konteks" icon="sliders" href="/docs/id/build-with-claude/context-windows">
    Cara kerja jendela konteks 1M token.
  </Card>

  <Card title="Harga" icon="shield" href="/docs/id/about-claude/pricing">
    Harga lengkap, termasuk tarif pemrosesan batch dan caching prompt.
  </Card>
</CardGroup>
