---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/whats-new-claude-4-6
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 7c01c27f3bfe66af40987bb1f8567f4f73bf4d7996063e9b8f217a296685c14a
---

# Apa yang baru di Claude 4.6

Gambaran umum fitur dan kemampuan baru di Claude Opus 4.6.

---

Claude 4.6 mewakili generasi berikutnya dari model Claude, membawa kemampuan baru yang signifikan dan peningkatan API. Halaman ini merangkum semua fitur baru yang tersedia saat peluncuran.

## Model baru

| Model | API model ID | Deskripsi |
|:------|:-------------|:------------|
| Claude Opus 4.6 | `claude-opus-4-6` | Model paling cerdas kami untuk membangun agen dan coding |

Claude Opus 4.6 mendukung jendela konteks 200K (dengan [jendela konteks token 1M](/docs/id/build-with-claude/context-windows#1m-token-context-window) tersedia dalam beta), token output maksimal 128K, pemikiran yang diperluas, dan semua fitur Claude API yang ada.

Untuk harga lengkap dan spesifikasi, lihat [gambaran umum model](/docs/id/about-claude/models/overview).

## Fitur baru

### Mode pemikiran adaptif

[Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) adalah mode pemikiran yang direkomendasikan untuk Opus 4.6. Claude secara dinamis memutuskan kapan dan berapa banyak untuk berpikir. Pada tingkat upaya default (`high`), Claude hampir selalu akan berpikir. Pada tingkat upaya yang lebih rendah, mungkin melewati pemikiran untuk masalah yang lebih sederhana.

`thinking: {type: "enabled"}` dan `budget_tokens` adalah **deprecated** pada Opus 4.6. Mereka tetap berfungsi tetapi akan dihapus dalam rilis model di masa depan. Gunakan pemikiran adaptif dan [parameter upaya](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran sebagai gantinya. Pemikiran adaptif juga secara otomatis mengaktifkan pemikiran yang tersisip.

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    messages=[{"role": "user", "content": "Solve this complex problem..."}]
)
```

### Parameter upaya GA

[Parameter upaya](/docs/id/build-with-claude/effort) sekarang tersedia secara umum (tidak diperlukan header beta). Tingkat upaya `max` baru memberikan kemampuan tertinggi mutlak pada Opus 4.6. Gabungkan upaya dengan pemikiran adaptif untuk pertukaran biaya-kualitas yang optimal.

### Compaction API (beta)

[Compaction](/docs/id/build-with-claude/compaction) menyediakan ringkasan konteks otomatis di sisi server, memungkinkan percakapan yang efektif tak terbatas. Ketika konteks mendekati batas jendela, API secara otomatis merangkum bagian-bagian sebelumnya dari percakapan.

### Fine-grained tool streaming (GA)

[Fine-grained tool streaming](/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming) sekarang tersedia secara umum di semua model dan platform. Tidak diperlukan header beta.

### Token output 128K

Opus 4.6 mendukung hingga 128K token output, menggandakan batas sebelumnya 64K. Ini memungkinkan anggaran pemikiran yang lebih panjang dan respons yang lebih komprehensif. SDK memerlukan streaming untuk permintaan dengan nilai `max_tokens` besar untuk menghindari timeout HTTP. Jika Anda tidak perlu memproses acara secara bertahap, gunakan `.stream()` dengan `.get_final_message()` untuk mendapatkan respons lengkap — lihat [Streaming Messages](/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events) untuk detail.

### Kontrol residensi data

[Kontrol residensi data](/docs/id/build-with-claude/data-residency) memungkinkan Anda menentukan di mana inferensi model berjalan menggunakan parameter `inference_geo`. Anda dapat memilih routing `"global"` (default) atau `"us"` per permintaan. Inferensi hanya AS dikenakan harga 1,1x pada Claude Opus 4.6 dan model yang lebih baru.

## Deprecations

### `type: "enabled"` dan `budget_tokens`

`thinking: {type: "enabled", budget_tokens: N}` adalah **deprecated** pada Opus 4.6. Ini tetap berfungsi tetapi akan dihapus dalam rilis model di masa depan. Migrasi ke `thinking: {type: "adaptive"}` dengan [parameter upaya](/docs/id/build-with-claude/effort).

### Header beta `interleaved-thinking-2025-05-14`

Header beta `interleaved-thinking-2025-05-14` adalah **deprecated** pada Opus 4.6. Ini dengan aman diabaikan jika disertakan, tetapi tidak lagi diperlukan. [Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) secara otomatis mengaktifkan [pemikiran yang tersisip](/docs/id/build-with-claude/extended-thinking#interleaved-thinking). Hapus `betas=["interleaved-thinking-2025-05-14"]` dari permintaan Anda saat menggunakan Opus 4.6.

### `output_format`

Parameter `output_format` untuk [structured outputs](/docs/id/build-with-claude/structured-outputs) telah dipindahkan ke `output_config.format`. Parameter lama tetap berfungsi tetapi deprecated dan akan dihapus dalam rilis model di masa depan.

```python
# Before
response = client.messages.create(
    output_format={"type": "json_schema", "schema": {...}},
    ...
)

# After
response = client.messages.create(
    output_config={"format": {"type": "json_schema", "schema": {...}}},
    ...
)
```

## Perubahan yang merusak

### Penghapusan prefill

Prefilling pesan asisten (prefill giliran asisten terakhir) **tidak didukung** pada Opus 4.6. Permintaan dengan pesan asisten yang sudah diisi sebelumnya mengembalikan kesalahan 400.

**Alternatif:**
- [Structured outputs](/docs/id/build-with-claude/structured-outputs) untuk mengontrol format respons
- Instruksi prompt sistem untuk memandu gaya respons
- [`output_config.format`](/docs/id/build-with-claude/structured-outputs#json-outputs) untuk output JSON

### Quoting parameter tool

Opus 4.6 mungkin menghasilkan escaping string JSON yang sedikit berbeda dalam argumen panggilan tool (misalnya, penanganan Unicode escapes atau forward slash escaping yang berbeda). Parser JSON standar menangani perbedaan ini secara otomatis. Jika Anda mengurai `input` panggilan tool sebagai string mentah daripada menggunakan `json.loads()` atau `JSON.parse()`, verifikasi logika parsing Anda masih berfungsi.

## Panduan migrasi

Untuk instruksi migrasi langkah demi langkah, lihat [Migrasi ke Claude 4.6](/docs/id/about-claude/models/migration-guide).

## Langkah berikutnya

<CardGroup>
  <Card title="Pemikiran adaptif" icon="brain" href="/docs/id/build-with-claude/adaptive-thinking">
    Pelajari cara menggunakan mode pemikiran adaptif.
  </Card>
  <Card title="Gambaran umum model" icon="list" href="/docs/id/about-claude/models/overview">
    Bandingkan semua model Claude.
  </Card>
  <Card title="Compaction" icon="compress" href="/docs/id/build-with-claude/compaction">
    Jelajahi compaction konteks di sisi server.
  </Card>
  <Card title="Panduan migrasi" icon="arrow-right" href="/docs/id/about-claude/models/migration-guide">
    Instruksi migrasi langkah demi langkah.
  </Card>
</CardGroup>