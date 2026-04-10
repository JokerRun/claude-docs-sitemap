---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/whats-new-claude-4-6
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 28928586514e680de75c74ff8b3c8a6e804b217b4d727aec955e017d519a5d9e
---

# Yang baru di Claude 4.6

Ikhtisar fitur dan kemampuan baru di Claude Opus 4.6 dan Sonnet 4.6.

---

Claude 4.6 mewakili generasi berikutnya dari model Claude, menghadirkan kemampuan baru yang signifikan dan peningkatan API. Halaman ini merangkum semua fitur baru yang tersedia saat peluncuran.

## Model baru

| Model | ID model API | Deskripsi |
|:------|:-------------|:------------|
| Claude Opus 4.6 | `claude-opus-4-6` | Model paling cerdas untuk membangun agen dan coding |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | Kombinasi terbaik antara kecepatan dan kecerdasan |

Claude Opus 4.6 dan Sonnet 4.6 keduanya mendukung [jendela konteks 1M token](/docs/id/build-with-claude/context-windows), extended thinking, dan semua fitur API Claude yang ada. Opus 4.6 menawarkan maksimal 128k token output; Sonnet 4.6 menawarkan maksimal 64k token output.

Untuk harga dan spesifikasi lengkap, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

## Fitur baru

### Mode adaptive thinking

[Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) adalah mode thinking yang direkomendasikan untuk Opus 4.6 dan Sonnet 4.6. Claude secara dinamis memutuskan kapan dan seberapa banyak untuk berpikir. Pada tingkat effort default (`high`), Claude hampir selalu berpikir. Pada tingkat effort yang lebih rendah, ia mungkin melewati thinking untuk masalah yang lebih sederhana.

`thinking: {type: "enabled"}` dan `budget_tokens` **sudah tidak digunakan (deprecated)** pada Opus 4.6 dan Sonnet 4.6. Keduanya masih berfungsi tetapi akan dihapus pada rilis model mendatang. Gunakan adaptive thinking dan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking. Adaptive thinking juga secara otomatis mengaktifkan interleaved thinking.

```python Python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    messages=[{"role": "user", "content": "Solve this complex problem..."}],
)
```

### Parameter effort GA

[Parameter effort](/docs/id/build-with-claude/effort) kini tersedia secara umum (tidak diperlukan beta header). Tingkat effort `max` yang baru memberikan kemampuan tertinggi absolut pada Opus 4.6. Kombinasikan effort dengan adaptive thinking untuk tradeoff biaya-kualitas yang optimal.

Sonnet 4.6 memperkenalkan parameter effort ke keluarga Sonnet. Pertimbangkan untuk menetapkan effort ke `medium` untuk sebagian besar kasus penggunaan Sonnet 4.6 guna menyeimbangkan kecepatan, biaya, dan performa.

### Eksekusi kode kini gratis dengan web tools

[Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) kini gratis ketika digunakan dengan [web search](/docs/id/agents-and-tools/tool-use/web-search-tool) atau [web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool). Ketika salah satu tool disertakan dalam permintaan API Anda, tidak ada biaya tambahan untuk eksekusi kode di luar biaya token input dan output standar. Eksekusi kode memungkinkan pemfilteran dinamis dalam web search dan web fetch tools, meningkatkan akurasi sekaligus mengurangi konsumsi token. Lihat [harga eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#usage-and-pricing) untuk detail penggunaan mandiri.

### Web search dan web fetch yang ditingkatkan dengan pemfilteran dinamis

Tool [web search](/docs/id/agents-and-tools/tool-use/web-search-tool) dan [web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool) kini mendukung pemfilteran dinamis dengan Opus 4.6 dan Sonnet 4.6. Claude dapat menulis dan mengeksekusi kode untuk memfilter hasil sebelum mencapai jendela konteks, hanya menyimpan informasi yang relevan dan meningkatkan akurasi sekaligus mengurangi konsumsi token. Untuk mengaktifkan pemfilteran dinamis, gunakan versi tool `web_search_20260209` atau `web_fetch_20260209`.

### Tool yang lulus ke ketersediaan umum

Tool-tool berikut kini tersedia secara umum:
- [Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) (gratis dengan web tools)
- [Web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool)
- [Pemanggilan tool terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling)
- [Tool pencarian tool](/docs/id/agents-and-tools/tool-use/tool-search-tool)
- [Contoh penggunaan tool](/docs/id/agents-and-tools/tool-use/define-tools#providing-tool-use-examples)
- [Memory tool](/docs/id/agents-and-tools/tool-use/memory-tool)

### Compaction API (beta)

[Compaction](/docs/id/build-with-claude/compaction) menyediakan ringkasan konteks otomatis di sisi server, memungkinkan percakapan yang secara efektif tidak terbatas. Ketika konteks mendekati batas jendela, API secara otomatis merangkum bagian-bagian percakapan sebelumnya.

### Fast mode (beta: research preview)

[Fast mode](/docs/id/build-with-claude/fast-mode) (`speed: "fast"`) menghasilkan generasi token output yang jauh lebih cepat untuk model Opus. Fast mode hingga 2,5x lebih cepat dengan harga premium ($30/$150 per MTok). Ini adalah model yang sama yang berjalan dengan inferensi lebih cepat (tidak ada perubahan pada kecerdasan atau kemampuan).

```python Python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    speed="fast",
    betas=["fast-mode-2026-02-01"],
    messages=[{"role": "user", "content": "Refactor this module..."}],
)
```

### Fine-grained tool streaming (GA)

[Fine-grained tool streaming](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) kini tersedia secara umum di semua model dan platform. Tidak diperlukan beta header.

### Batas token output yang lebih tinggi

Opus 4.6 mendukung hingga 128k token output. Ini memungkinkan anggaran thinking yang lebih panjang dan respons yang lebih komprehensif. SDK memerlukan streaming untuk permintaan dengan nilai `max_tokens` yang besar untuk menghindari timeout HTTP. Jika Anda tidak perlu memproses event secara bertahap, gunakan `.stream()` dengan `.get_final_message()` untuk mendapatkan respons lengkap. Lihat [Streaming Messages](/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events) untuk detailnya.

Pada Message Batches API, Opus 4.6 dan Sonnet 4.6 dapat menghasilkan hingga 300k token output dengan menggunakan beta header `output-300k-2026-03-24`. Lihat [Pemrosesan batch](/docs/id/build-with-claude/batch-processing#extended-output-beta) untuk detailnya.

### Kontrol residensi data

[Kontrol residensi data](/docs/id/build-with-claude/data-residency) memungkinkan Anda menentukan di mana inferensi model berjalan menggunakan parameter `inference_geo`. Anda dapat memilih routing `"global"` (default) atau `"us"` per permintaan. Inferensi khusus AS dihargai 1,1x pada Claude Opus 4.6 dan model yang lebih baru.

## Deprecasi

### `type: "enabled"` dan `budget_tokens`

`thinking: {type: "enabled", budget_tokens: N}` [**sudah tidak digunakan (deprecated)**](/docs/id/build-with-claude/overview#feature-availability) pada Opus 4.6 dan Sonnet 4.6. Masih berfungsi tetapi tidak lagi direkomendasikan dan akan dihapus pada rilis model mendatang. Migrasikan ke `thinking: {type: "adaptive"}` dengan [parameter effort](/docs/id/build-with-claude/effort).

### Beta header `interleaved-thinking-2025-05-14`

Beta header `interleaved-thinking-2025-05-14` **sudah tidak digunakan (deprecated)** pada Opus 4.6. Diabaikan dengan aman jika disertakan, tetapi tidak lagi diperlukan. [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) secara otomatis mengaktifkan [interleaved thinking](/docs/id/build-with-claude/extended-thinking#interleaved-thinking). Hapus `betas=["interleaved-thinking-2025-05-14"]` dari permintaan Anda saat menggunakan Opus 4.6.

Pada **Sonnet 4.6**, beta header `interleaved-thinking-2025-05-14` masih berfungsi untuk digunakan dengan extended thinking manual (`thinking: {type: "enabled"}`), tetapi mode manual sudah deprecated. Adaptive thinking adalah jalur yang direkomendasikan dan secara otomatis mengaktifkan interleaved thinking.

### `output_format`

Parameter `output_format` untuk [structured outputs](/docs/id/build-with-claude/structured-outputs) telah dipindahkan ke `output_config.format`. Parameter lama masih berfungsi tetapi sudah deprecated dan akan dihapus pada rilis model mendatang.

```python Python nocheck
# Sebelum
response = client.messages.create(
    output_format={"type": "json_schema", "schema": {...}},
    # ...
)

# Sesudah
response = client.messages.create(
    output_config={"format": {"type": "json_schema", "schema": {...}}},
    # ...
)
```

## Perubahan yang merusak (breaking changes)

### Penghapusan prefill

Pengisian awal pesan asisten (prefill giliran-asisten-terakhir) **tidak didukung** pada Opus 4.6. Permintaan dengan pesan asisten yang diisi awal mengembalikan error 400.

**Alternatif:**
- [Structured outputs](/docs/id/build-with-claude/structured-outputs) untuk mengontrol format respons
- Instruksi system prompt untuk memandu gaya respons
- [`output_config.format`](/docs/id/build-with-claude/structured-outputs#json-outputs) untuk output JSON

### Pengutipan parameter tool

Opus 4.6 mungkin menghasilkan escaping string JSON yang sedikit berbeda dalam argumen pemanggilan tool (misalnya, penanganan berbeda untuk Unicode escapes atau escaping garis miring ke depan). Parser JSON standar menangani perbedaan ini secara otomatis. Jika Anda mengurai `input` pemanggilan tool sebagai string mentah daripada menggunakan `json.loads()` atau `JSON.parse()`, verifikasi bahwa logika penguraian Anda masih berfungsi.

## Panduan migrasi

Untuk instruksi migrasi langkah demi langkah, lihat [Migrasi ke Claude 4.6](/docs/id/about-claude/models/migration-guide).

## Langkah selanjutnya

<CardGroup>
  <Card title="Adaptive thinking" icon="brain" href="/docs/id/build-with-claude/adaptive-thinking">
    Pelajari cara menggunakan mode adaptive thinking.
  </Card>
  <Card title="Ikhtisar model" icon="list" href="/docs/id/about-claude/models/overview">
    Bandingkan semua model Claude.
  </Card>
  <Card title="Compaction" icon="compress" href="/docs/id/build-with-claude/compaction">
    Jelajahi compaction konteks di sisi server.
  </Card>
  <Card title="Fast mode" icon="bolt" href="/docs/id/build-with-claude/fast-mode">
    Generasi token output yang lebih cepat untuk model Opus.
  </Card>
  <Card title="Panduan migrasi" icon="arrow-right" href="/docs/id/about-claude/models/migration-guide">
    Instruksi migrasi langkah demi langkah.
  </Card>
</CardGroup>