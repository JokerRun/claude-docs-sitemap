---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/migration-guide
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 2d02904e35f23a4985877c38115cc0dc1532dfe6e580a8a305e6dd5e7545b821
---

# Panduan migrasi

Panduan untuk bermigrasi ke model Claude 4.6 dari versi Claude sebelumnya

---

## Bermigrasi ke Claude 4.6

Claude Opus 4.6 adalah pengganti yang hampir drop-in untuk Claude 4.5, dengan beberapa perubahan yang merusak yang perlu diperhatikan. Untuk daftar lengkap fitur baru, lihat [Apa yang baru di Claude 4.6](/docs/id/about-claude/models/whats-new-claude-4-6).

### Perbarui nama model Anda

```python
# Migrasi Opus
model="claude-opus-4-5"     # Sebelum
model="claude-opus-4-6"       # Sesudah
```

### Perubahan yang merusak

1. **Penghapusan prefill**: Mengisi pesan asisten sebelumnya mengembalikan kesalahan 400 pada model Claude 4.6. Gunakan [keluaran terstruktur](/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

2. **Penawaran parameter alat**: Model Claude 4.6 mungkin menghasilkan pelarian string JSON yang sedikit berbeda dalam argumen panggilan alat (misalnya, penanganan pelarian Unicode atau pelarian garis miring yang berbeda). Jika Anda mengurai `input` panggilan alat sebagai string mentah daripada menggunakan pengurai JSON, verifikasi logika penguraian Anda. Pengurai JSON standar (seperti `json.loads()` atau `JSON.parse()`) menangani perbedaan ini secara otomatis.

### Perubahan yang direkomendasikan

Ini tidak diperlukan tetapi akan meningkatkan pengalaman Anda:

1. **Bermigrasi ke pemikiran adaptif**: `thinking: {type: "enabled", budget_tokens: N}` sudah usang pada model Claude 4.6 dan akan dihapus dalam rilis model di masa depan. Beralih ke `thinking: {type: "adaptive"}` dan gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran. Lihat [Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking).

   <CodeGroup>
   ```python Sebelum
   response = client.beta.messages.create(
       model="claude-opus-4-5",
       max_tokens=16000,
       thinking={
           "type": "enabled",
           "budget_tokens": 32000
       },
       betas=["interleaved-thinking-2025-05-14"],
       messages=[...]
   )
   ```

   ```python Sesudah
   response = client.messages.create(
       model="claude-opus-4-6",
       max_tokens=16000,
       thinking={
           "type": "adaptive"
       },
       output_config={
           "effort": "high"
       },
       messages=[...]
   )
   ```
   </CodeGroup>

   Perhatikan bahwa migrasi juga bergerak dari `client.beta.messages.create` ke `client.messages.create` — pemikiran adaptif dan effort adalah fitur GA dan tidak memerlukan namespace SDK beta atau header beta apa pun.

2. **Hapus header beta effort**: Parameter effort sekarang GA. Hapus `betas=["effort-2025-11-24"]` dari permintaan Anda.

3. **Hapus header beta streaming alat berbutir halus**: Streaming alat berbutir halus sekarang GA. Hapus `betas=["fine-grained-tool-streaming-2025-05-14"]` dari permintaan Anda.

4. **Hapus header beta pemikiran interleaved**: Pemikiran adaptif secara otomatis mengaktifkan pemikiran interleaved. Hapus `betas=["interleaved-thinking-2025-05-14"]` dari permintaan Anda.

5. **Bermigrasi ke output_config.format**: Jika menggunakan keluaran terstruktur, perbarui `output_format={...}` ke `output_config={"format": {...}}`. Parameter lama tetap berfungsi tetapi sudah usang dan akan dihapus dalam rilis model di masa depan.

### Bermigrasi dari Claude 4.1 atau lebih awal ke Claude 4.6

Jika Anda bermigrasi dari Opus 4.1, Sonnet 4, atau model lebih awal langsung ke Claude 4.6, terapkan perubahan yang merusak Claude 4.6 di atas ditambah perubahan tambahan di bagian ini.

```python
# Dari Opus 4.1
model="claude-opus-4-1-20250805"    # Sebelum
model="claude-opus-4-6"               # Sesudah

# Dari Sonnet 4
model="claude-sonnet-4-20250514"    # Sebelum
model="claude-opus-4-6"              # Sesudah

# Dari Sonnet 3.7
model="claude-3-7-sonnet-20250219"  # Sebelum
model="claude-opus-4-6"              # Sesudah
```

#### Perubahan yang merusak tambahan

1. **Parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya:

   ```python
   # Sebelum - Ini akan error di model Claude 4+
   response = client.messages.create(
       model="claude-3-7-sonnet-20250219",
       temperature=0.7,
       top_p=0.9,  # Tidak dapat menggunakan keduanya
       ...
   )

   # Sesudah
   response = client.messages.create(
       model="claude-opus-4-6",
       temperature=0.7,  # Gunakan temperature ATAU top_p, bukan keduanya
       ...
   )
   ```

2. **Versi alat**

   <Warning>
   Ini adalah perubahan yang merusak dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru. Hapus kode apa pun yang menggunakan perintah `undo_edit`.

   ```python
   # Sebelum
   tools=[{"type": "text_editor_20250124", "name": "str_replace_editor"}]

   # Sesudah
   tools=[{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
   ```

   - **Editor teks**: Gunakan `text_editor_20250728` dan `str_replace_based_edit_tool`. Lihat [Dokumentasi alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool) untuk detail.
   - **Eksekusi kode**: Tingkatkan ke `code_execution_20250825`. Lihat [Dokumentasi alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) untuk instruksi migrasi.

3. **Tangani alasan penghentian `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan penghentian `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals):

   ```python
   response = client.messages.create(...)

   if response.stop_reason == "refusal":
       # Tangani penolakan dengan tepat
       pass
   ```

4. **Tangani alasan penghentian `model_context_window_exceeded`**

   Model Claude 4.5+ mengembalikan alasan penghentian `model_context_window_exceeded` ketika generasi berhenti karena mencapai batas jendela konteks, bukan batas `max_tokens` yang diminta. Perbarui aplikasi Anda untuk menangani alasan penghentian baru ini:

   ```python
   response = client.messages.create(...)

   if response.stop_reason == "model_context_window_exceeded":
       # Tangani batas jendela konteks dengan tepat
       pass
   ```

5. **Penanganan parameter alat (trailing newlines)**

   Model Claude 4.5+ mempertahankan trailing newline dalam parameter string panggilan alat yang sebelumnya dihapus. Jika alat Anda mengandalkan pencocokan string yang tepat terhadap parameter panggilan alat, verifikasi logika Anda menangani trailing newline dengan benar.

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4+ memiliki gaya komunikasi yang lebih ringkas dan langsung serta memerlukan arahan eksplisit. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

#### Perubahan yang direkomendasikan tambahan

- **Hapus header beta warisan**: Hapus `token-efficient-tools-2025-02-19` dan `output-128k-2025-02-19` — semua model Claude 4+ memiliki penggunaan alat yang efisien token bawaan dan header ini tidak berpengaruh.

### Daftar periksa migrasi Claude 4.6

- [ ] Perbarui ID model ke `claude-opus-4-6`
- [ ] **MERUSAK**: Hapus prefill pesan asisten (mengembalikan kesalahan 400); gunakan keluaran terstruktur atau `output_config.format` sebagai gantinya
- [ ] **Direkomendasikan**: Bermigrasi dari `thinking: {type: "enabled", budget_tokens: N}` ke `thinking: {type: "adaptive"}` dengan [parameter effort](/docs/id/build-with-claude/effort) (`budget_tokens` sudah usang dan akan dihapus dalam rilis model di masa depan)
- [ ] Verifikasi penguraian JSON panggilan alat menggunakan pengurai JSON standar
- [ ] Hapus header beta `effort-2025-11-24` (effort sekarang GA)
- [ ] Hapus header beta `fine-grained-tool-streaming-2025-05-14`
- [ ] Hapus header beta `interleaved-thinking-2025-05-14`
- [ ] Bermigrasi `output_format` ke `output_config.format` (jika berlaku)
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: perbarui versi alat (`text_editor_20250728`, `code_execution_20250825`)
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: tangani alasan penghentian `refusal`
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: tangani alasan penghentian `model_context_window_exceeded`
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: verifikasi penanganan parameter string alat untuk trailing newline
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: hapus header beta warisan (`token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`)
- [ ] Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Uji di lingkungan pengembangan sebelum penerapan produksi

---

## Bermigrasi ke Claude Sonnet 4.5

Claude Sonnet 4.5 menggabungkan intelijen yang kuat dengan kinerja cepat, menjadikannya ideal untuk tugas pengkodean, analisis, dan konten sehari-hari.

Untuk gambaran lengkap kemampuan, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

<Note>
Harga Sonnet 4.5 adalah $3 per juta token input, $15 per juta token output. Lihat [harga Claude](/docs/id/about-claude/pricing) untuk detail.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Sonnet 4
model="claude-sonnet-4-20250514"        # Sebelum
model="claude-sonnet-4-5-20250929"      # Sesudah

# Dari Sonnet 3.7
model="claude-3-7-sonnet-20250219"      # Sebelum
model="claude-sonnet-4-5-20250929"      # Sesudah
```

**Pertimbangkan mengaktifkan pemikiran diperpanjang** untuk peningkatan kinerja yang signifikan pada tugas pengkodean dan penalaran (dinonaktifkan secara default):

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[...]
)
```

### Perubahan yang merusak

Perubahan yang merusak ini berlaku saat bermigrasi dari model Claude 3.x Sonnet.

1. **Parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

2. **Versi alat**

   <Warning>
   Ini adalah perubahan yang merusak dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

3. **Tangani alasan penghentian `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan penghentian `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Daftar periksa migrasi Sonnet 4.5

- [ ] Perbarui ID model ke `claude-sonnet-4-5-20250929`
- [ ] **MERUSAK**: Perbarui versi alat ke terbaru (`text_editor_20250728`, `code_execution_20250825`) — versi warisan tidak didukung (jika bermigrasi dari 3.x)
- [ ] **MERUSAK**: Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
- [ ] **MERUSAK**: Perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`, bukan keduanya (jika bermigrasi dari 3.x)
- [ ] Tangani alasan penghentian `refusal` baru di aplikasi Anda
- [ ] Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Pertimbangkan mengaktifkan pemikiran diperpanjang untuk tugas penalaran kompleks
- [ ] Uji di lingkungan pengembangan sebelum penerapan produksi

---

## Bermigrasi ke Claude Haiku 4.5

Claude Haiku 4.5 adalah model Haiku kami yang tercepat dan paling cerdas dengan kinerja mendekati frontier, memberikan kualitas model premium untuk aplikasi interaktif dan pemrosesan volume tinggi.

Untuk gambaran lengkap kemampuan, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

<Note>
Harga Haiku 4.5 adalah $1 per juta token input, $5 per juta token output. Lihat [harga Claude](/docs/id/about-claude/pricing) untuk detail.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Haiku 3.5
model="claude-3-5-haiku-20241022"      # Sebelum
model="claude-haiku-4-5-20251001"      # Sesudah
```

**Tinjau batas laju baru:** Haiku 4.5 memiliki batas laju terpisah dari Haiku 3.5. Lihat [dokumentasi batas laju](/docs/id/api/rate-limits) untuk detail.

**Pertimbangkan mengaktifkan pemikiran diperpanjang** untuk peningkatan kinerja yang signifikan pada tugas pengkodean dan penalaran (dinonaktifkan secara default):

```python
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 5000},
    messages=[...]
)
```

<Note>
Pemikiran diperpanjang berdampak pada efisiensi [caching prompt](/docs/id/build-with-claude/prompt-caching#caching-with-thinking-blocks).
</Note>

**Jelajahi kemampuan baru:** Lihat [ikhtisar model](/docs/id/about-claude/models/overview) untuk detail tentang kesadaran konteks, kapasitas output yang meningkat (64K token), intelijen yang lebih tinggi, dan kecepatan yang ditingkatkan.

### Perubahan yang merusak

Perubahan yang merusak ini berlaku saat bermigrasi dari model Claude 3.x Haiku.

1. **Parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

2. **Versi alat**

   <Warning>
   Ini adalah perubahan yang merusak dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

3. **Tangani alasan penghentian `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan penghentian `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Daftar periksa migrasi Haiku 4.5

- [ ] Perbarui ID model ke `claude-haiku-4-5-20251001`
- [ ] **MERUSAK**: Perbarui versi alat ke terbaru (`text_editor_20250728`, `code_execution_20250825`) — versi warisan tidak didukung
- [ ] **MERUSAK**: Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
- [ ] **MERUSAK**: Perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`, bukan keduanya
- [ ] Tangani alasan penghentian `refusal` baru di aplikasi Anda
- [ ] Tinjau dan sesuaikan untuk batas laju baru (terpisah dari Haiku 3.5)
- [ ] Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Pertimbangkan mengaktifkan pemikiran diperpanjang untuk tugas penalaran kompleks
- [ ] Uji di lingkungan pengembangan sebelum penerapan produksi

---

## Butuh bantuan?

- Periksa [dokumentasi API](/docs/id/api/overview) kami untuk spesifikasi terperinci
- Tinjau [kemampuan model](/docs/id/about-claude/models/overview) untuk perbandingan kinerja
- Tinjau [catatan rilis API](/docs/id/release-notes/api) untuk pembaruan API
- Hubungi dukungan jika Anda mengalami masalah apa pun selama migrasi