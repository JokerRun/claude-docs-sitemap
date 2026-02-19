---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/migration-guide
fetched_at: 2026-02-19T04:23:04.153807Z
sha256: 9a82f0541cb7919b5dd9d93ddfc94bd438d4cad92a1d9e0c3756c15cd9fa37c0
---

# Panduan migrasi

Panduan untuk bermigrasi ke model Claude 4.6 dari versi Claude sebelumnya

---

## Bermigrasi ke Claude 4.6

Claude Opus 4.6 adalah pengganti yang hampir drop-in untuk Claude 4.5, dengan beberapa perubahan yang merusak untuk diperhatikan. Untuk daftar lengkap fitur baru, lihat [Yang baru di Claude 4.6](/docs/id/about-claude/models/whats-new-claude-4-6).

### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-5"  # Sebelum
model = "claude-opus-4-6"  # Sesudah
```

### Perubahan yang merusak

1. **Penghapusan prefill:** Prefilling pesan asisten mengembalikan kesalahan 400 pada model Claude 4.6. Gunakan [output terstruktur](/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

2. **Penawaran parameter alat:** Model Claude 4.6 mungkin menghasilkan penghindaran string JSON yang sedikit berbeda dalam argumen panggilan alat (misalnya, penanganan penghindaran Unicode atau penghindaran garis miring yang berbeda). Jika Anda mengurai `input` panggilan alat sebagai string mentah daripada menggunakan parser JSON, verifikasi logika penguraian Anda. Parser JSON standar (seperti `json.loads()` atau `JSON.parse()`) menangani perbedaan ini secara otomatis.

### Perubahan yang direkomendasikan

Ini tidak diperlukan tetapi akan meningkatkan pengalaman Anda:

1. **Bermigrasi ke pemikiran adaptif:** `thinking: {type: "enabled", budget_tokens: N}` tidak direkomendasikan pada model Claude 4.6 dan akan dihapus dalam rilis model di masa depan. Beralih ke `thinking: {type: "adaptive"}` dan gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran. Lihat [Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking).

   <CodeGroup>
   ```python Sebelum
   response = client.beta.messages.create(
       model="claude-opus-4-5",
       max_tokens=16000,
       thinking={"type": "enabled", "budget_tokens": 32000},
       betas=["interleaved-thinking-2025-05-14"],
       messages=[...],
   )
   ```

   ```python Sesudah
   response = client.messages.create(
       model="claude-opus-4-6",
       max_tokens=16000,
       thinking={"type": "adaptive"},
       output_config={"effort": "high"},
       messages=[...],
   )
   ```
   </CodeGroup>

   Perhatikan bahwa migrasi juga bergerak dari `client.beta.messages.create` ke `client.messages.create`. Pemikiran adaptif dan effort adalah fitur GA dan tidak memerlukan namespace SDK beta atau header beta apa pun.

2. **Hapus header beta effort:** Parameter effort sekarang GA. Hapus `betas=["effort-2025-11-24"]` dari permintaan Anda.

3. **Hapus header beta streaming alat yang halus:** Streaming alat yang halus sekarang GA. Hapus `betas=["fine-grained-tool-streaming-2025-05-14"]` dari permintaan Anda.

4. **Hapus header beta pemikiran yang tersisip (Opus 4.6 saja):** Pemikiran adaptif secara otomatis mengaktifkan pemikiran yang tersisip pada Opus 4.6. Hapus `betas=["interleaved-thinking-2025-05-14"]` dari permintaan Opus 4.6 Anda. Catatan: Sonnet 4.6 terus mendukung header beta ini dengan pemikiran yang diperpanjang secara manual.

5. **Bermigrasi ke output_config.format:** Jika menggunakan output terstruktur, perbarui `output_format={...}` ke `output_config={"format": {...}}`. Parameter lama tetap berfungsi tetapi tidak direkomendasikan dan akan dihapus dalam rilis model di masa depan.

### Bermigrasi dari Claude 4.1 atau lebih awal ke Claude 4.6

Jika Anda bermigrasi dari Opus 4.1, Sonnet 4, atau model sebelumnya langsung ke Claude 4.6, terapkan perubahan yang merusak Claude 4.6 di atas ditambah perubahan tambahan di bagian ini.

```python
# Dari Opus 4.1
model = "claude-opus-4-1-20250805"  # Sebelum
model = "claude-opus-4-6"  # Sesudah

# Dari Sonnet 4
model = "claude-sonnet-4-20250514"  # Sebelum
model = "claude-opus-4-6"  # Sesudah

# Dari Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Sebelum
model = "claude-opus-4-6"  # Sesudah
```

#### Perubahan yang merusak tambahan

1. **Perbarui parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya:

   ```python
   # Sebelum - Ini akan error di model Claude 4+
   response = client.messages.create(
       model="claude-3-7-sonnet-20250219",
       temperature=0.7,
       top_p=0.9,  # Tidak dapat menggunakan keduanya
       # ...
   )

   # Sesudah
   response = client.messages.create(
       model="claude-opus-4-6",
       temperature=0.7,  # Gunakan temperature ATAU top_p, bukan keduanya
       # ...
   )
   ```

2. **Perbarui versi alat**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru. Hapus kode apa pun yang menggunakan perintah `undo_edit`.

   ```python
   # Sebelum
   tools = [{"type": "text_editor_20250124", "name": "str_replace_editor"}]

   # Sesudah
   tools = [{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
   ```

   - **Editor teks:** Gunakan `text_editor_20250728` dan `str_replace_based_edit_tool`. Lihat [Dokumentasi alat editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool) untuk detail.
   - **Eksekusi kode:** Tingkatkan ke `code_execution_20250825`. Lihat [Dokumentasi alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) untuk instruksi migrasi.

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

5. **Verifikasi penanganan parameter alat (trailing newlines)**

   Model Claude 4.5+ mempertahankan trailing newlines dalam parameter string panggilan alat yang sebelumnya dihapus. Jika alat Anda mengandalkan pencocokan string yang tepat terhadap parameter panggilan alat, verifikasi logika Anda menangani trailing newlines dengan benar.

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4+ memiliki gaya komunikasi yang lebih ringkas dan langsung serta memerlukan arahan eksplisit. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

#### Perubahan yang direkomendasikan tambahan

- **Hapus header beta warisan:** Hapus `token-efficient-tools-2025-02-19` dan `output-128k-2025-02-19`. Semua model Claude 4+ memiliki penggunaan alat yang efisien token bawaan dan header ini tidak berpengaruh.

### Daftar periksa migrasi Claude 4.6

- [ ] Perbarui ID model ke `claude-opus-4-6`
- [ ] **MERUSAK:** Hapus prefill pesan asisten (mengembalikan kesalahan 400); gunakan output terstruktur atau `output_config.format` sebagai gantinya
- [ ] **DIREKOMENDASIKAN:** Bermigrasi dari `thinking: {type: "enabled", budget_tokens: N}` ke `thinking: {type: "adaptive"}` dengan [parameter effort](/docs/id/build-with-claude/effort) (`budget_tokens` tidak direkomendasikan dan akan dihapus dalam rilis model di masa depan)
- [ ] Verifikasi parsing JSON panggilan alat menggunakan parser JSON standar
- [ ] Hapus header beta `effort-2025-11-24` (effort sekarang GA)
- [ ] Hapus header beta `fine-grained-tool-streaming-2025-05-14`
- [ ] Hapus header beta `interleaved-thinking-2025-05-14` (Opus 4.6 saja; Sonnet 4.6 masih mendukungnya)
- [ ] Bermigrasi `output_format` ke `output_config.format` (jika berlaku)
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: perbarui versi alat (`text_editor_20250728`, `code_execution_20250825`)
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: tangani alasan penghentian `refusal`
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: tangani alasan penghentian `model_context_window_exceeded`
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: verifikasi penanganan parameter string alat untuk trailing newlines
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: hapus header beta warisan (`token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`)
- [ ] Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Uji di lingkungan pengembangan sebelum penyebaran produksi

---

## Bermigrasi ke Claude Sonnet 4.6

Claude Sonnet 4.6 menggabungkan intelijen yang kuat dengan kinerja cepat, menampilkan kemampuan pencarian agentic yang ditingkatkan dan eksekusi kode gratis saat digunakan dengan pencarian web atau pengambilan web. Ini ideal untuk tugas coding, analisis, dan konten sehari-hari.

Untuk gambaran lengkap kemampuan, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

<Note>
Harga Sonnet 4.6 adalah $3 per juta token input, $15 per juta token output. Lihat [harga Claude](/docs/id/about-claude/pricing) untuk detail.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Sonnet 4.5
model = "claude-sonnet-4-5"  # Sebelum
model = "claude-sonnet-4-6"  # Sesudah

# Dari Sonnet 4
model = "claude-sonnet-4-20250514"  # Sebelum
model = "claude-sonnet-4-6"  # Sesudah
```

### Perubahan yang merusak

#### Saat bermigrasi dari Sonnet 4.5

1. **Prefilling pesan asisten tidak lagi didukung**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari Sonnet 4.5 atau lebih awal.
   </Warning>

   Prefilling pesan asisten mengembalikan kesalahan `400` pada Sonnet 4.6. Gunakan [output terstruktur](/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

   **Kasus penggunaan prefill umum dan migrasi:**

   - **Mengontrol format output** (memaksa output JSON/YAML): Gunakan [output terstruktur](/docs/id/build-with-claude/structured-outputs) atau alat dengan bidang enum untuk tugas klasifikasi.

   - **Menghilangkan preamble** (menghapus frasa "Here is..."): Tambahkan instruksi langsung dalam prompt sistem: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc."

   - **Menghindari penolakan buruk**: Claude jauh lebih baik dalam penolakan yang tepat sekarang. Prompting yang jelas dalam pesan pengguna tanpa prefill harus cukup.

   - **Kelanjutan** (melanjutkan respons yang terputus): Pindahkan kelanjutan ke pesan pengguna: "Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off."

   - **Hidrasi konteks / konsistensi peran** (menyegarkan konteks dalam percakapan panjang): Injeksi apa yang sebelumnya adalah pengingat prefilled-assistant ke giliran pengguna sebagai gantinya.

2. **Penghindaran JSON parameter alat mungkin berbeda**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari Sonnet 4.5 atau lebih awal.
   </Warning>

   Penghindaran string JSON dalam parameter alat mungkin berbeda dari model sebelumnya. Parser JSON standar menangani ini secara otomatis, tetapi parsing berbasis string khusus mungkin memerlukan pembaruan.

#### Saat bermigrasi dari Claude 3.x

3. **Perbarui parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

4. **Perbarui versi alat**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

5. **Tangani alasan penghentian `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan penghentian `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Perubahan yang direkomendasikan

1. **Hapus header beta `fine-grained-tool-streaming-2025-05-14`** — Streaming alat yang halus sekarang GA pada Sonnet 4.6 dan tidak lagi memerlukan header beta.
2. **Bermigrasi `output_format` ke `output_config.format`** — Parameter `output_format` tidak direkomendasikan. Gunakan `output_config.format` sebagai gantinya.

### Bermigrasi dari Sonnet 4.5

Kami sangat mendorong migrasi dari Sonnet 4.5 ke Sonnet 4.6, yang memberikan lebih banyak intelijen dengan harga yang sama.

<Warning>
Sonnet 4.6 default ke tingkat effort `high`, berbeda dengan Sonnet 4.5 yang tidak memiliki parameter effort. Kami merekomendasikan menyesuaikan parameter effort saat Anda bermigrasi dari Sonnet 4.5 ke Sonnet 4.6. Jika tidak secara eksplisit diatur, Anda mungkin mengalami latensi yang lebih tinggi dengan tingkat effort default.
</Warning>

#### Jika Anda tidak menggunakan pemikiran yang diperpanjang

Jika Anda tidak menggunakan pemikiran yang diperpanjang pada Sonnet 4.5, Anda dapat melanjutkan tanpanya pada Sonnet 4.6. Anda harus secara eksplisit menetapkan effort ke tingkat yang sesuai untuk kasus penggunaan Anda. Pada effort `low` dengan pemikiran dinonaktifkan, Anda dapat mengharapkan kinerja yang sama atau lebih baik relatif terhadap Sonnet 4.5 tanpa pemikiran yang diperpanjang.

<CodeGroup>
```python Python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    output_config={"effort": "low"},
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 8192,
  output_config: { effort: "low" },
  messages: [{ role: "user", content: "Your prompt here" }]
});
```

```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 8192,
    "output_config": {
        "effort": "low"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```
</CodeGroup>

#### Jika Anda menggunakan pemikiran yang diperpanjang

Jika Anda menggunakan pemikiran yang diperpanjang pada Sonnet 4.5, itu terus didukung pada Sonnet 4.6 tanpa perubahan yang diperlukan pada konfigurasi pemikiran Anda. Kami merekomendasikan menjaga anggaran pemikiran sekitar 16k token. Dalam praktik, sebagian besar tugas tidak menggunakan sebanyak itu, tetapi itu memberikan ruang kepala untuk masalah yang lebih sulit tanpa risiko penggunaan token yang liar.

##### Kasus penggunaan coding dan agentic

Untuk coding agentic, desain frontend, alur kerja yang berat alat, dan alur kerja enterprise yang kompleks, kami merekomendasikan memulai dengan effort `medium`. Jika Anda menemukan latensi terlalu tinggi, pertimbangkan mengurangi effort ke `low`. Jika Anda memerlukan intelijen yang lebih tinggi, pertimbangkan meningkatkan effort ke `high` atau bermigrasi ke Opus 4.6.

<CodeGroup>
```python Python
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16384,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "medium"},
    betas=["interleaved-thinking-2025-05-14"],
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

```typescript TypeScript
const response = await client.beta.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 16384,
  thinking: { type: "enabled", budget_tokens: 16384 },
  output_config: { effort: "medium" },
  betas: ["interleaved-thinking-2025-05-14"],
  messages: [{ role: "user", content: "Your prompt here" }]
});
```

```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "anthropic-beta: interleaved-thinking-2025-05-14" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 16384,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 16384
    },
    "output_config": {
        "effort": "medium"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```
</CodeGroup>

##### Kasus penggunaan chat dan non-coding

Untuk chat, pembuatan konten, pencarian, klasifikasi, dan tugas non-coding lainnya, kami merekomendasikan memulai dengan effort `low` dengan pemikiran yang diperpanjang. Jika Anda memerlukan lebih banyak kedalaman, tingkatkan effort ke `medium`.

<CodeGroup>
```python Python
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "low"},
    betas=["interleaved-thinking-2025-05-14"],
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

```typescript TypeScript
const response = await client.beta.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 8192,
  thinking: { type: "enabled", budget_tokens: 16384 },
  output_config: { effort: "low" },
  betas: ["interleaved-thinking-2025-05-14"],
  messages: [{ role: "user", content: "Your prompt here" }]
});
```

```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "anthropic-beta: interleaved-thinking-2025-05-14" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 8192,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 16384
    },
    "output_config": {
        "effort": "low"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```
</CodeGroup>

##### Kapan mencoba pemikiran adaptif

Jalur migrasi di atas menggunakan pemikiran yang diperpanjang dengan `budget_tokens` untuk penggunaan token yang dapat diprediksi. Jika beban kerja Anda sesuai dengan salah satu pola berikut, pertimbangkan mencoba [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) sebagai gantinya:

- **Agen multi-langkah otonom:** agen coding yang mengubah persyaratan menjadi perangkat lunak yang berfungsi, pipeline analisis data, dan pencarian bug di mana model berjalan secara independen di banyak langkah. Pemikiran adaptif memungkinkan model mengkalibrasi penalaran per langkah, tetap di jalur selama lintasan yang lebih panjang. Untuk beban kerja ini, mulai dengan effort `high`. Jika latensi atau penggunaan token menjadi masalah, skala turun ke `medium`.
- **Agen penggunaan komputer:** Sonnet 4.6 mencapai akurasi terbaik di kelasnya pada evaluasi penggunaan komputer menggunakan mode adaptif.
- **Beban kerja bimodal:** campuran tugas mudah dan sulit di mana adaptif melewati pemikiran pada kueri sederhana dan bernalar dalam pada yang kompleks.

Saat menggunakan pemikiran adaptif, evaluasi effort `medium` dan `high` pada tugas Anda. Tingkat yang tepat tergantung pada tradeoff beban kerja Anda antara kualitas, latensi, dan penggunaan token.

<CodeGroup>
```python Python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 64000,
  thinking: { type: "adaptive" },
  output_config: { effort: "medium" },
  messages: [{ role: "user", content: "Your prompt here" }]
});
```

```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 64000,
    "thinking": {
        "type": "adaptive"
    },
    "output_config": {
        "effort": "medium"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```
</CodeGroup>

<Note>
Jika Anda melihat perilaku yang tidak konsisten atau regresi kualitas dengan pemikiran adaptif, beralih ke pemikiran yang diperpanjang dengan `budget_tokens`. Ini memberikan hasil yang lebih dapat diprediksi dengan batas pada biaya pemikiran.
</Note>

### Daftar periksa migrasi Sonnet 4.6

- [ ] Perbarui ID model ke `claude-sonnet-4-6`
- [ ] **MERUSAK:** Hapus prefilling pesan asisten; gunakan output terstruktur atau `output_config.format` sebagai gantinya
- [ ] **MERUSAK:** Verifikasi parsing JSON parameter alat menangani perbedaan penghindaran
- [ ] **MERUSAK:** Perbarui versi alat ke terbaru (`text_editor_20250728`, `code_execution_20250825`); versi warisan tidak didukung (jika bermigrasi dari 3.x)
- [ ] **MERUSAK:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
- [ ] **MERUSAK:** Perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`, bukan keduanya (jika bermigrasi dari 3.x)
- [ ] Tangani alasan penghentian `refusal` baru dalam aplikasi Anda
- [ ] Hapus header beta `fine-grained-tool-streaming-2025-05-14` (sekarang GA)
- [ ] Bermigrasi `output_format` ke `output_config.format`
- [ ] Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Pertimbangkan mengaktifkan pemikiran yang diperpanjang atau pemikiran adaptif untuk tugas penalaran kompleks
- [ ] Uji di lingkungan pengembangan sebelum penyebaran produksi

---

## Bermigrasi ke Claude Sonnet 4.5

Claude Sonnet 4.5 menggabungkan intelijen yang kuat dengan kinerja cepat, menjadikannya ideal untuk tugas coding, analisis, dan konten sehari-hari.

Untuk gambaran lengkap kemampuan, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

<Note>
Harga Sonnet 4.5 adalah $3 per juta token input, $15 per juta token output. Lihat [harga Claude](/docs/id/about-claude/pricing) untuk detail.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Sonnet 4
model = "claude-sonnet-4-20250514"  # Sebelum
model = "claude-sonnet-4-5-20250929"  # Sesudah

# Dari Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Sebelum
model = "claude-sonnet-4-5-20250929"  # Sesudah
```

### Perubahan yang merusak

Perubahan yang merusak ini berlaku saat bermigrasi dari model Claude 3.x Sonnet.

1. **Perbarui parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

2. **Perbarui versi alat**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

3. **Tangani alasan penghentian `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan penghentian `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Daftar periksa migrasi Sonnet 4.5

- [ ] Perbarui ID model ke `claude-sonnet-4-5-20250929`
- [ ] **MERUSAK:** Perbarui versi alat ke terbaru (`text_editor_20250728`, `code_execution_20250825`); versi warisan tidak didukung (jika bermigrasi dari 3.x)
- [ ] **MERUSAK:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
- [ ] **MERUSAK:** Perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`, bukan keduanya (jika bermigrasi dari 3.x)
- [ ] Tangani alasan penghentian `refusal` baru dalam aplikasi Anda
- [ ] Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Pertimbangkan mengaktifkan pemikiran yang diperpanjang untuk tugas penalaran kompleks
- [ ] Uji di lingkungan pengembangan sebelum penyebaran produksi

---

## Bermigrasi ke Claude Haiku 4.5

Claude Haiku 4.5 adalah model Haiku tercepat dan paling cerdas dengan kinerja mendekati frontier, memberikan kualitas model premium untuk aplikasi interaktif dan pemrosesan volume tinggi.

Untuk gambaran lengkap kemampuan, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

<Note>
Harga Haiku 4.5 adalah $1 per juta token input, $5 per juta token output. Lihat [harga Claude](/docs/id/about-claude/pricing) untuk detail.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Haiku 3.5
model = "claude-3-5-haiku-20241022"  # Sebelum
model = "claude-haiku-4-5-20251001"  # Sesudah
```

**Tinjau batas laju baru:** Haiku 4.5 memiliki batas laju terpisah dari Haiku 3.5. Lihat [dokumentasi batas laju](/docs/id/api/rate-limits) untuk detail.

<Tip>
Untuk peningkatan kinerja yang signifikan pada tugas coding dan penalaran, pertimbangkan mengaktifkan pemikiran yang diperpanjang dengan `thinking: {type: "enabled", budget_tokens: N}`.
</Tip>

<Note>
Pemikiran yang diperpanjang berdampak pada efisiensi [prompt caching](/docs/id/build-with-claude/prompt-caching#caching-with-thinking-blocks).

Pemikiran yang diperpanjang tidak direkomendasikan di model Claude 4.6 atau lebih baru. Jika menggunakan model yang lebih baru, gunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) sebagai gantinya.
</Note>

**Jelajahi kemampuan baru:** Lihat [ikhtisar model](/docs/id/about-claude/models/overview) untuk detail tentang kesadaran konteks, kapasitas output yang ditingkatkan (64K token), intelijen yang lebih tinggi, dan kecepatan yang ditingkatkan.

### Perubahan yang merusak

Perubahan yang merusak ini berlaku saat bermigrasi dari model Claude 3.x Haiku.

1. **Perbarui parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

2. **Perbarui versi alat**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

3. **Tangani alasan penghentian `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan penghentian `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Daftar periksa migrasi Haiku 4.5

- [ ] Perbarui ID model ke `claude-haiku-4-5-20251001`
- [ ] **MERUSAK:** Perbarui versi alat ke terbaru (`text_editor_20250728`, `code_execution_20250825`); versi warisan tidak didukung
- [ ] **MERUSAK:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
- [ ] **MERUSAK:** Perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`, bukan keduanya
- [ ] Tangani alasan penghentian `refusal` baru dalam aplikasi Anda
- [ ] Tinjau dan sesuaikan untuk batas laju baru (terpisah dari Haiku 3.5)
- [ ] Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Pertimbangkan mengaktifkan pemikiran yang diperpanjang untuk tugas penalaran kompleks
- [ ] Uji di lingkungan pengembangan sebelum penyebaran produksi

---

## Butuh bantuan?

- Periksa [dokumentasi API](/docs/id/api/overview) untuk spesifikasi terperinci
- Tinjau [kemampuan model](/docs/id/about-claude/models/overview) untuk perbandingan kinerja
- Tinjau [catatan rilis API](/docs/id/release-notes/api) untuk pembaruan API
- Hubungi dukungan jika Anda mengalami masalah apa pun selama migrasi