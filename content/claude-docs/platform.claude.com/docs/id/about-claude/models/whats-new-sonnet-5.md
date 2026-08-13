---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/whats-new-sonnet-5
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 314be80c71e128ec317d372581c58853d0f7cca5f9155ffc6fdf60f529942b59
---

---
title: Apa yang baru di Claude Sonnet 5
url: https://platform.claude.com/docs/id/about-claude/models/whats-new-sonnet-5
description: Ikhtisar fitur baru dan perubahan perilaku di Claude Sonnet 5.
---

Claude Sonnet 5 adalah generasi berikutnya dari keluarga model Sonnet Anthropic. Model ini merupakan peningkatan langsung (drop-in upgrade) untuk Claude Sonnet 4.6 dengan tiga perubahan perilaku: [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) aktif secara default, pemikiran diperpanjang manual sekarang mengembalikan error 400 (fitur ini sudah tidak digunakan lagi pada Claude Sonnet 4.6), dan mengatur parameter sampling (`temperature`, `top_p`, `top_k`) ke nilai non-default akan mengembalikan error 400. Halaman ini merangkum semua hal baru saat peluncuran, termasuk tokenizer baru.

## Model baru

| Model           | ID model API      | Deskripsi                                         |
| --------------- | ----------------- | ------------------------------------------------- |
| Claude Sonnet 5 | `claude-sonnet-5` | Kombinasi terbaik antara kecepatan dan kecerdasan |

Claude Sonnet 5 mendukung [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default (1 juta token adalah nilai default sekaligus maksimum; tidak ada varian konteks yang lebih kecil), output maksimum 128 ribu token, [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking), dan kumpulan alat serta fitur platform yang sama dengan Claude Sonnet 4.6, kecuali [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models), yang tidak tersedia pada Claude Sonnet 5.

Untuk harga dan spesifikasi lengkap, lihat [ikhtisar model](https://platform.claude.com/docs/id/about-claude/models/overview).

## Perubahan perilaku

### Adaptive thinking aktif secara default

Pada Claude Sonnet 4.6, permintaan tanpa field `thinking` berjalan tanpa pemikiran. Pada Claude Sonnet 5, permintaan yang sama berjalan dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking). Untuk menonaktifkan pemikiran, kirimkan `thinking: {type: "disabled"}`. Karena `max_tokens` adalah batas keras pada total output (pemikiran ditambah teks respons), tinjau kembali nilainya untuk beban kerja yang sebelumnya berjalan tanpa pemikiran pada Claude Sonnet 4.6.

### Parameter sampling tidak diterima

Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default akan mengembalikan error 400. Hapus parameter ini saat bermigrasi; nilai default (atau menghilangkan parameter) tetap diterima. Gunakan instruksi prompt sistem untuk memandu perilaku model. Ini baru untuk model kelas Sonnet; batasan yang sama sebelumnya diperkenalkan pada Claude Opus 4.7.

### Pemikiran diperpanjang manual dihapus

Pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`) sudah tidak digunakan lagi pada Claude Sonnet 4.6; pada Claude Sonnet 5 fitur ini dihapus dan mengembalikan error 400, sama seperti pada Claude Opus 4.8 dan Claude Opus 4.7. Gunakan adaptive thinking dengan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) sebagai gantinya.

<CodeGroup exclude="shell">
  ```python Python
  # Tidak didukung pada Claude Sonnet 5 (mengembalikan 400)
  thinking = {"type": "enabled", "budget_tokens": 32000}

  # Gunakan ini sebagai gantinya
  thinking = {"type": "adaptive"}
  ```

  ```typescript TypeScript
  // Tidak didukung pada Claude Sonnet 5 (mengembalikan 400)
  const legacyThinking = { type: "enabled", budget_tokens: 32000 };

  // Gunakan ini sebagai gantinya
  const thinking = { type: "adaptive" };
  ```

  ```csharp C#
  // Tidak didukung pada Claude Sonnet 5 (mengembalikan 400)
  var legacyThinking = new ThinkingConfigEnabled(budgetTokens: 32000);

  // Gunakan ini sebagai gantinya
  var thinking = new ThinkingConfigAdaptive();
  ```

  ```go Go
  // Tidak didukung pada Claude Sonnet 5 (mengembalikan 400)
  legacyThinking := anthropic.ThinkingConfigParamUnion{
  	OfEnabled: &anthropic.ThinkingConfigEnabledParam{BudgetTokens: 32000},
  }

  // Gunakan ini sebagai gantinya
  thinking := anthropic.ThinkingConfigParamUnion{
  	OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
  }
  ```

  ```java Java
  // Tidak didukung pada Claude Sonnet 5 (mengembalikan 400)
  var legacyThinking = ThinkingConfigEnabled.builder().budgetTokens(32_000L).build();

  // Gunakan ini sebagai gantinya
  var thinking = ThinkingConfigAdaptive.builder().build();
  ```

  ```php PHP
  // Tidak didukung pada Claude Sonnet 5 (mengembalikan 400)
  $thinking = ['type' => 'enabled', 'budget_tokens' => 32000];

  // Gunakan ini sebagai gantinya
  $thinking = ['type' => 'adaptive'];
  ```

  ```ruby Ruby
  # Tidak didukung pada Claude Sonnet 5 (mengembalikan 400)
  legacy_thinking = {type: "enabled", budget_tokens: 32_000}

  # Gunakan ini sebagai gantinya
  thinking = {type: "adaptive"}
  ```
</CodeGroup>

## Tokenizer baru

Claude Sonnet 5 menggunakan tokenizer baru. Teks input yang sama menghasilkan sekitar 30% lebih banyak token dibandingkan pada Claude Sonnet 4.6. Peningkatan pastinya bergantung pada konten. Ini bukan perubahan API: permintaan, respons, dan event streaming mempertahankan bentuk yang sama, dan tidak diperlukan perubahan kode.

Perubahan ini memengaruhi apa pun yang Anda ukur atau anggarkan dalam token:

* **Jumlah token:** field `usage` dan hasil [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) untuk teks yang sama lebih tinggi dibandingkan pada Claude Sonnet 4.6. Jangan gunakan kembali hitungan yang diukur terhadap model sebelumnya; hitung ulang terhadap Claude Sonnet 5.
* **Kapasitas jendela konteks dalam satuan teks:** jendela konteks adalah 1 juta token, tetapi setiap token rata-rata mencakup lebih sedikit teks, sehingga jendela yang sama menampung lebih sedikit teks dibandingkan pada Claude Sonnet 4.6.
* **Anggaran `max_tokens`:** batas output yang disesuaikan untuk Claude Sonnet 4.6 mungkin memotong output yang setara pada Claude Sonnet 5. Tinjau kembali batas yang ukurannya mendekati panjang output yang Anda harapkan.
* **Biaya per permintaan:** harga per token lebih rendah daripada Claude Sonnet 4.6 (lihat [Harga](https://platform.claude.com/docs/id/about-claude/models/whats-new-sonnet-5#pricing)), tetapi karena teks yang sama menghasilkan lebih banyak token, biaya permintaan yang setara tidak turun secara proporsional langsung.

## Batasan API yang diwarisi dari Claude Sonnet 4.6

<Note>
  Batasan ini tidak berubah dari Claude Sonnet 4.6. Selain tiga [perubahan perilaku](https://platform.claude.com/docs/id/about-claude/models/whats-new-sonnet-5#behavior-changes) (lihat [Panduan migrasi](https://platform.claude.com/docs/id/about-claude/models/whats-new-sonnet-5#migration-guide)), kode yang sudah berjalan pada Claude Sonnet 4.6 tidak memerlukan perubahan lain.
</Note>

### Prefilling pesan asisten tidak didukung

Melakukan prefilling pada pesan asisten akan mengembalikan error `400`, tidak berubah dari Claude Sonnet 4.6. Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) (output terstruktur), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

## Peningkatan kemampuan

Claude Sonnet 5 adalah peningkatan kemampuan dibandingkan Claude Sonnet 4.6 dengan harga yang lebih rendah. Model ini juga merupakan opsi untuk beban kerja yang membutuhkan kemampuan lebih dari yang disediakan Claude Sonnet 4.6 tanpa harus beralih ke model kelas Opus.

Peningkatan terbesar dibandingkan Claude Sonnet 4.6 ada pada tugas coding dan agentic. Untuk hasil benchmark, lihat [Transparency Hub Anthropic](https://www.anthropic.com/transparency).

## Pengamanan keamanan siber

Claude Sonnet 5 adalah model tingkat Sonnet pertama dengan pengamanan keamanan siber real-time. Permintaan yang melibatkan topik keamanan siber yang dilarang atau berisiko tinggi mungkin ditolak. Penolakan dikembalikan sebagai respons HTTP 200 yang berhasil dengan `stop_reason: "refusal"`, bukan sebagai error. Lihat [Safeguards, warnings, and appeals](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals) untuk latar belakangnya.

## Harga

Claude Sonnet 5 dihargai $2 per juta token input dan $10 per juta token output, harga per token yang lebih rendah dibandingkan $3/$15 pada Claude Sonnet 4.6. Karena [tokenizer baru](https://platform.claude.com/docs/id/about-claude/models/whats-new-sonnet-5#new-tokenizer) menghasilkan sekitar 30% lebih banyak token untuk teks yang sama, biaya permintaan yang setara tidak turun secara proporsional langsung terhadap harga per token saat dibandingkan dengan Claude Sonnet 4.6. Perbedaan pastinya bergantung pada konten dan bentuk beban kerja.

Lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) untuk harga lengkap, termasuk tarif batch processing dan caching prompt.

## Ketersediaan

Saat peluncuran, Claude Sonnet 5 tersedia di:

* **Claude API:** tersedia untuk semua pelanggan.
* **AWS:** tersedia melalui [Claude di Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock) dan [Claude Platform di AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Di Amazon Bedrock, Claude Sonnet 5 juga dapat diakses melalui API `InvokeModel`, yang dilayani oleh infrastruktur yang sama dengan Claude di Amazon Bedrock. Integrasi legacy [Claude di Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy) tidak menyertakan Claude Sonnet 5.
* **Google Cloud:** tersedia melalui [Claude di Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai).
* **Microsoft Foundry:** tersedia melalui [Claude di Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry).

Claude Sonnet 5 mendukung [zero data retention](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention) (tanpa retensi data) untuk organisasi dengan perjanjian ZDR.

## Panduan migrasi

Claude Sonnet 5 adalah pengganti langsung (drop-in replacement) untuk Claude Sonnet 4.6. Perbarui ID model Anda:

<CodeGroup exclude="shell">
  ```python Python
  model = "claude-sonnet-4-6"  # Before
  model = "claude-sonnet-5"  # After
  ```

  ```typescript TypeScript
  const legacyModel = "claude-sonnet-4-6"; // Before
  const model = "claude-sonnet-5"; // After
  ```

  ```csharp C#
  var legacyModel = Model.ClaudeSonnet4_6; // Before
  var model = Model.ClaudeSonnet5; // After
  ```

  ```go Go
  // Sebelum
  legacyModel := anthropic.ModelClaudeSonnet4_6
  // Sesudah
  model := anthropic.ModelClaudeSonnet5
  ```

  ```java Java
  var legacyModel = Model.CLAUDE_SONNET_4_6; // Before
  var model = Model.CLAUDE_SONNET_5; // After
  ```

  ```php PHP
  $model = 'claude-sonnet-4-6'; // Before
  $model = 'claude-sonnet-5'; // After
  ```

  ```ruby Ruby
  legacy_model = "claude-sonnet-4-6" # Before
  model = "claude-sonnet-5" # After
  ```
</CodeGroup>

Kemudian tinjau hal-hal berikut:

1. **Anggaran dan jumlah token:** [tokenizer baru](https://platform.claude.com/docs/id/about-claude/models/whats-new-sonnet-5#new-tokenizer) menghasilkan sekitar 30% lebih banyak token untuk teks yang sama. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja. Hitung ulang prompt dengan [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting), dan tinjau kembali batas `max_tokens` yang ukurannya mendekati panjang output yang Anda harapkan.
2. **Pemikiran diperpanjang:** jika Anda masih mengatur `budget_tokens`, migrasikan ke [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking). Pemikiran diperpanjang manual (`thinking: {type: "enabled"}`) tidak didukung dan mengembalikan error 400.
3. **Parameter sampling:** permintaan yang mengatur parameter sampling (`temperature`, `top_p`, `top_k`) ke nilai non-default akan mengembalikan error 400; hapus parameter tersebut saat bermigrasi. Definisi alat dan bentuk respons tidak berubah, dan prefilling pesan asisten memang sudah tidak didukung pada Claude Sonnet 4.6.

Lihat [bagian Claude Sonnet 5 pada panduan migrasi](https://platform.claude.com/docs/id/about-claude/models/migration-guide#migrating-from-claude-sonnet-4-6-to-claude-sonnet-5) untuk detailnya.

## Langkah selanjutnya

<CardGroup>
  <Card title="Ikhtisar model" icon="arrow-right" href="https://platform.claude.com/docs/id/about-claude/models/overview">
    Spesifikasi dan harga lengkap untuk semua model Claude saat ini.
  </Card>

  <Card title="Penghitungan token" icon="database" href="https://platform.claude.com/docs/id/build-with-claude/token-counting">
    Ukur prompt Anda dengan tokenizer baru sebelum bermigrasi.
  </Card>

  <Card title="Adaptive thinking" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Mode pemikiran aktif yang direkomendasikan pada Claude Sonnet 5.
  </Card>

  <Card title="Jendela konteks" icon="sliders" href="https://platform.claude.com/docs/id/build-with-claude/context-windows">
    Cara kerja jendela konteks 1 juta token.
  </Card>

  <Card title="Harga" icon="shield" href="https://platform.claude.com/docs/id/about-claude/pricing">
    Harga lengkap, termasuk tarif batch processing dan caching prompt.
  </Card>
</CardGroup>
