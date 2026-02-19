---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-caching
fetched_at: 2026-02-19T04:23:04.153807Z
sha256: 1b9bf2e4823ff71d409e2b58a1461956e3eb0c6fea67cf1179a7e91bc2967715
---

# Penyimpanan cache prompt

Penyimpanan cache prompt mengoptimalkan penggunaan API Anda dengan memungkinkan melanjutkan dari awalan tertentu dalam prompt Anda.

---

Penyimpanan cache prompt adalah fitur canggih yang mengoptimalkan penggunaan API Anda dengan memungkinkan melanjutkan dari awalan tertentu dalam prompt Anda. Pendekatan ini secara signifikan mengurangi waktu pemrosesan dan biaya untuk tugas berulang atau prompt dengan elemen yang konsisten.

<Note>
Penyimpanan cache prompt menyimpan representasi cache KV dan hash kriptografi konten yang di-cache, tetapi tidak menyimpan teks mentah dari prompt atau respons. Ini mungkin cocok untuk pelanggan yang memerlukan komitmen retensi data [tipe ZDR](/docs/id/build-with-claude/zero-data-retention). Lihat [masa pakai cache](/docs/id/build-with-claude/prompt-caching#what-is-the-cache-lifetime) untuk detail.
</Note>

Berikut adalah contoh cara mengimplementasikan penyimpanan cache prompt dengan Messages API menggunakan blok `cache_control`:

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "system": [
      {
        "type": "text",
        "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
      },
      {
        "type": "text",
        "text": "<the entire contents of Pride and Prejudice>",
        "cache_control": {"type": "ephemeral"}
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "Analyze the major themes in Pride and Prejudice."
      }
    ]
  }'

# Call the model again with the same inputs up to the cache checkpoint
curl https://api.anthropic.com/v1/messages # rest of input
```

```python Python
import anthropic

client = anthropic.Anthropic()

params = {
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "system": [
        {
            "type": "text",
            "text": "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n",
        },
        {
            "type": "text",
            "text": "<the entire contents of 'Pride and Prejudice'>",
            "cache_control": {"type": "ephemeral"},
        },
    ],
    "messages": [
        {
            "role": "user",
            "content": "Analyze the major themes in 'Pride and Prejudice'.",
        }
    ],
}
response = client.messages.create(**params)
print(response.usage.model_dump_json())

# Call the model again with the same inputs up to the cache checkpoint
response = client.messages.create(**params)
print(response.usage.model_dump_json())
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
    },
    {
      type: "text",
      text: "<the entire contents of 'Pride and Prejudice'>",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [
    {
      role: "user",
      content: "Analyze the major themes in 'Pride and Prejudice'."
    }
  ]
});
console.log(response.usage);

// Call the model again with the same inputs up to the cache checkpoint
const new_response = await client.messages.create(/* ... */);
console.log(new_response.usage);
```

```java Java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import java.util.List;

public class PromptCachingExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
      .maxTokens(1024)
      .systemOfTextBlockParams(
        List.of(
          TextBlockParam.builder()
            .text(
              "You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.\n"
            )
            .build(),
          TextBlockParam.builder()
            .text("<the entire contents of 'Pride and Prejudice'>")
            .cacheControl(CacheControlEphemeral.builder().build())
            .build()
        )
      )
      .addUserMessage("Analyze the major themes in 'Pride and Prejudice'.")
      .build();

    Message message = client.messages().create(params);
    System.out.println(message.usage());
  }
}
```
</CodeGroup>

```json JSON
{"cache_creation_input_tokens":188086,"cache_read_input_tokens":0,"input_tokens":21,"output_tokens":393}
{"cache_creation_input_tokens":0,"cache_read_input_tokens":188086,"input_tokens":21,"output_tokens":393}
```

Dalam contoh ini, seluruh teks "Pride and Prejudice" di-cache menggunakan parameter `cache_control`. Ini memungkinkan penggunaan kembali teks besar ini di berbagai panggilan API tanpa memproses ulang setiap kali. Mengubah hanya pesan pengguna memungkinkan Anda untuk mengajukan berbagai pertanyaan tentang buku sambil memanfaatkan konten yang di-cache, yang menghasilkan respons lebih cepat dan efisiensi yang lebih baik.

---

## Cara kerja penyimpanan cache prompt

Ketika Anda mengirim permintaan dengan penyimpanan cache prompt diaktifkan:

1. Sistem memeriksa apakah awalan prompt, hingga titik henti cache yang ditentukan, sudah di-cache dari kueri baru-baru ini.
2. Jika ditemukan, sistem menggunakan versi yang di-cache, mengurangi waktu pemrosesan dan biaya.
3. Jika tidak, sistem memproses prompt lengkap dan meng-cache awalan setelah respons dimulai.

Ini sangat berguna untuk:
- Prompt dengan banyak contoh
- Jumlah besar konteks atau informasi latar belakang
- Tugas berulang dengan instruksi yang konsisten
- Percakapan multi-putaran yang panjang

Secara default, cache memiliki masa pakai 5 menit. Cache disegarkan tanpa biaya tambahan setiap kali konten yang di-cache digunakan.

<Note>
Jika Anda menemukan bahwa 5 menit terlalu singkat, Anthropic juga menawarkan durasi cache 1 jam [dengan biaya tambahan](#pricing).

Untuk informasi lebih lanjut, lihat [durasi cache 1 jam](#1-hour-cache-duration).
</Note>

<Tip>
  **Penyimpanan cache prompt meng-cache awalan penuh**

Penyimpanan cache prompt mereferensikan seluruh prompt - `tools`, `system`, dan `messages` (dalam urutan itu) hingga dan termasuk blok yang ditunjuk dengan `cache_control`.

</Tip>

---
## Harga

Penyimpanan cache prompt memperkenalkan struktur harga baru. Tabel di bawah menunjukkan harga per juta token untuk setiap model yang didukung:

| Model             | Base Input Tokens | 5m Cache Writes | 1h Cache Writes | Cache Hits & Refreshes | Output Tokens |
|-------------------|-------------------|-----------------|-----------------|----------------------|---------------|
| Claude Opus 4.6     | $5 / MTok         | $6.25 / MTok    | $10 / MTok      | $0.50 / MTok | $25 / MTok    |
| Claude Opus 4.5   | $5 / MTok         | $6.25 / MTok    | $10 / MTok      | $0.50 / MTok | $25 / MTok    |
| Claude Opus 4.1   | $15 / MTok        | $18.75 / MTok   | $30 / MTok      | $1.50 / MTok | $75 / MTok    |
| Claude Opus 4     | $15 / MTok        | $18.75 / MTok   | $30 / MTok      | $1.50 / MTok | $75 / MTok    |
| Claude Sonnet 4.6   | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok | $15 / MTok    |
| Claude Sonnet 4.5   | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok | $15 / MTok    |
| Claude Sonnet 4   | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok | $15 / MTok    |
| Claude Sonnet 3.7 ([deprecated](/docs/en/about-claude/model-deprecations)) | $3 / MTok         | $3.75 / MTok    | $6 / MTok       | $0.30 / MTok | $15 / MTok    |
| Claude Haiku 4.5  | $1 / MTok         | $1.25 / MTok    | $2 / MTok       | $0.10 / MTok | $5 / MTok     |
| Claude Haiku 3.5  | $0.80 / MTok      | $1 / MTok       | $1.6 / MTok     | $0.08 / MTok | $4 / MTok     |
| Claude Opus 3 ([deprecated](/docs/en/about-claude/model-deprecations))    | $15 / MTok        | $18.75 / MTok   | $30 / MTok      | $1.50 / MTok | $75 / MTok    |
| Claude Haiku 3    | $0.25 / MTok      | $0.30 / MTok    | $0.50 / MTok    | $0.03 / MTok | $1.25 / MTok  |

<Note>
Tabel di atas mencerminkan pengganda harga berikut untuk penyimpanan cache prompt:
- Token penulisan cache 5 menit adalah 1,25 kali harga token input dasar
- Token penulisan cache 1 jam adalah 2 kali harga token input dasar
- Token pembacaan cache adalah 0,1 kali harga token input dasar

Pengganda ini ditumpuk dengan pengubah harga lainnya seperti diskon Batch API, harga konteks panjang, dan residensi data. Lihat [harga](/docs/id/about-claude/pricing) untuk detail lengkap.
</Note>

---
## Cara mengimplementasikan penyimpanan cache prompt

### Model yang didukung

Penyimpanan cache prompt saat ini didukung pada:
- Claude Opus 4.6
- Claude Opus 4.5
- Claude Opus 4.1
- Claude Opus 4
- Claude Sonnet 4.6
- Claude Sonnet 4.5
- Claude Sonnet 4
- Claude Sonnet 3.7 ([deprecated](/docs/id/about-claude/model-deprecations))
- Claude Haiku 4.5
- Claude Haiku 3.5 ([deprecated](/docs/id/about-claude/model-deprecations))
- Claude Haiku 3

### Menyusun prompt Anda

Tempatkan konten statis (definisi alat, instruksi sistem, konteks, contoh) di awal prompt Anda. Tandai akhir konten yang dapat digunakan kembali untuk penyimpanan cache menggunakan parameter `cache_control`.

Awalan cache dibuat dalam urutan berikut: `tools`, `system`, kemudian `messages`. Urutan ini membentuk hierarki di mana setiap level dibangun di atas level sebelumnya.

#### Cara kerja pemeriksaan awalan otomatis

Anda dapat menggunakan hanya satu titik henti cache di akhir konten statis Anda, dan sistem akan secara otomatis menemukan urutan blok yang di-cache terpanjang yang cocok. Memahami cara kerjanya membantu Anda mengoptimalkan strategi penyimpanan cache Anda.

**Tiga prinsip inti:**

1. **Kunci cache bersifat kumulatif**: Ketika Anda secara eksplisit meng-cache blok dengan `cache_control`, kunci hash cache dihasilkan dengan melakukan hash semua blok sebelumnya dalam percakapan secara berurutan. Ini berarti cache untuk setiap blok bergantung pada semua konten yang datang sebelumnya.

2. **Pemeriksaan berurutan mundur**: Sistem memeriksa cache hit dengan bekerja mundur dari titik henti eksplisit Anda, memeriksa setiap blok sebelumnya dalam urutan terbalik. Ini memastikan Anda mendapatkan cache hit terpanjang yang mungkin.

3. **Jendela lookback 20 blok**: Sistem hanya memeriksa hingga 20 blok sebelum setiap titik henti `cache_control` eksplisit. Setelah memeriksa 20 blok tanpa kecocokan, sistem berhenti memeriksa dan beralih ke titik henti eksplisit berikutnya (jika ada).

**Contoh: Memahami jendela lookback**

Pertimbangkan percakapan dengan 30 blok konten di mana Anda menetapkan `cache_control` hanya pada blok 30:

- **Jika Anda mengirim blok 31 tanpa perubahan pada blok sebelumnya**: Sistem memeriksa blok 30 (cocok!). Anda mendapatkan cache hit pada blok 30, dan hanya blok 31 yang perlu diproses.

- **Jika Anda memodifikasi blok 25 dan mengirim blok 31**: Sistem memeriksa mundur dari blok 30 → 29 → 28... → 25 (tidak cocok) → 24 (cocok!). Karena blok 24 belum berubah, Anda mendapatkan cache hit pada blok 24, dan hanya blok 25-30 yang perlu diproses ulang.

- **Jika Anda memodifikasi blok 5 dan mengirim blok 31**: Sistem memeriksa mundur dari blok 30 → 29 → 28... → 11 (pemeriksaan #20). Setelah 20 pemeriksaan tanpa menemukan kecocokan, sistem berhenti mencari. Karena blok 5 berada di luar jendela 20 blok, tidak ada cache hit dan semua blok perlu diproses ulang. Namun, jika Anda telah menetapkan titik henti `cache_control` eksplisit pada blok 5, sistem akan terus memeriksa dari titik henti itu: blok 5 (tidak cocok) → blok 4 (cocok!). Ini memungkinkan cache hit pada blok 4, menunjukkan mengapa Anda harus menempatkan titik henti sebelum konten yang dapat diedit.

**Kesimpulan utama**: Selalu tetapkan titik henti cache eksplisit di akhir percakapan Anda untuk memaksimalkan peluang cache hit. Selain itu, tetapkan titik henti tepat sebelum blok konten yang mungkin dapat diedit untuk memastikan bagian tersebut dapat di-cache secara independen.

#### Kapan menggunakan beberapa titik henti

Anda dapat menentukan hingga 4 titik henti cache jika Anda ingin:
- Meng-cache bagian berbeda yang berubah pada frekuensi berbeda (misalnya, alat jarang berubah, tetapi konteks diperbarui setiap hari)
- Memiliki kontrol lebih besar atas apa yang di-cache
- Memastikan penyimpanan cache untuk konten lebih dari 20 blok sebelum titik henti cache Anda
- Menempatkan titik henti sebelum konten yang dapat diedit untuk menjamin cache hit bahkan ketika perubahan terjadi di luar jendela 20 blok

<Note>
**Batasan penting**: Jika prompt Anda memiliki lebih dari 20 blok konten sebelum titik henti cache Anda, dan Anda memodifikasi konten lebih awal dari 20 blok tersebut, Anda tidak akan mendapatkan cache hit kecuali Anda menambahkan titik henti eksplisit tambahan lebih dekat ke konten itu.
</Note>

### Batasan cache
Panjang prompt yang dapat di-cache minimum adalah:
- 4096 token untuk Claude Opus 4.6, Claude Opus 4.5
- 1024 token untuk Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.1, Claude Opus 4, Claude Sonnet 4, dan Claude Sonnet 3.7 ([deprecated](/docs/id/about-claude/model-deprecations))
- 4096 token untuk Claude Haiku 4.5
- 2048 token untuk Claude Haiku 3.5 ([deprecated](/docs/id/about-claude/model-deprecations)) dan Claude Haiku 3

Prompt yang lebih pendek tidak dapat di-cache, bahkan jika ditandai dengan `cache_control`. Permintaan apa pun untuk meng-cache lebih sedikit dari jumlah token ini akan diproses tanpa penyimpanan cache. Untuk melihat apakah prompt di-cache, lihat [field](/docs/id/build-with-claude/prompt-caching#tracking-cache-performance) penggunaan respons.

Untuk permintaan bersamaan, perhatikan bahwa entri cache hanya tersedia setelah respons pertama dimulai. Jika Anda memerlukan cache hit untuk permintaan paralel, tunggu respons pertama sebelum mengirim permintaan berikutnya.

Saat ini, "ephemeral" adalah satu-satunya jenis cache yang didukung, yang secara default memiliki masa pakai 5 menit.

### Memahami biaya titik henti cache

**Titik henti cache itu sendiri tidak menambah biaya apa pun.** Anda hanya dikenakan biaya untuk:
- **Penulisan cache**: Ketika konten baru ditulis ke cache (25% lebih dari token input dasar untuk TTL 5 menit)
- **Pembacaan cache**: Ketika konten yang di-cache digunakan (10% dari harga token input dasar)
- **Token input reguler**: Untuk konten apa pun yang tidak di-cache

Menambahkan lebih banyak titik henti `cache_control` tidak meningkatkan biaya Anda - Anda masih membayar jumlah yang sama berdasarkan konten apa yang sebenarnya di-cache dan dibaca. Titik henti hanya memberi Anda kontrol atas bagian mana yang dapat di-cache secara independen.

### Apa yang dapat di-cache
Sebagian besar blok dalam permintaan dapat ditunjuk untuk penyimpanan cache dengan `cache_control`. Ini termasuk:

- Alat: Definisi alat dalam array `tools`
- Pesan sistem: Blok konten dalam array `system`
- Pesan teks: Blok konten dalam array `messages.content`, untuk putaran pengguna dan asisten
- Gambar & Dokumen: Blok konten dalam array `messages.content`, dalam putaran pengguna
- Penggunaan alat dan hasil alat: Blok konten dalam array `messages.content`, dalam putaran pengguna dan asisten

Setiap elemen ini dapat ditandai dengan `cache_control` untuk mengaktifkan penyimpanan cache untuk bagian permintaan itu.

### Apa yang tidak dapat di-cache
Meskipun sebagian besar blok permintaan dapat di-cache, ada beberapa pengecualian:

- Blok pemikiran tidak dapat di-cache secara langsung dengan `cache_control`. Namun, blok pemikiran DAPAT di-cache bersama konten lain ketika muncul dalam putaran asisten sebelumnya. Ketika di-cache dengan cara ini, mereka MENGHITUNG sebagai token input ketika dibaca dari cache.
- Blok sub-konten (seperti [kutipan](/docs/id/build-with-claude/citations)) itu sendiri tidak dapat di-cache secara langsung. Sebagai gantinya, cache blok tingkat atas.

    Dalam kasus kutipan, blok konten dokumen tingkat atas yang berfungsi sebagai materi sumber untuk kutipan dapat di-cache. Ini memungkinkan Anda menggunakan penyimpanan cache prompt dengan kutipan secara efektif dengan meng-cache dokumen yang akan direferensikan oleh kutipan.
- Blok teks kosong tidak dapat di-cache.

### Apa yang membatalkan cache

Modifikasi pada konten yang di-cache dapat membatalkan sebagian atau seluruh cache.

Seperti dijelaskan dalam [Menyusun prompt Anda](#structuring-your-prompt), cache mengikuti hierarki: `tools` → `system` → `messages`. Perubahan di setiap level membatalkan level itu dan semua level berikutnya.

Tabel berikut menunjukkan bagian mana dari cache yang dibatalkan oleh berbagai jenis perubahan. ✘ menunjukkan bahwa cache dibatalkan, sementara ✓ menunjukkan bahwa cache tetap valid.

| Apa yang berubah | Cache alat | Cache sistem | Cache pesan | Dampak |
|------------|------------------|---------------|----------------|-------------|
| **Definisi alat** | ✘ | ✘ | ✘ | Memodifikasi definisi alat (nama, deskripsi, parameter) membatalkan seluruh cache |
| **Tombol pencarian web** | ✓ | ✘ | ✘ | Mengaktifkan/menonaktifkan pencarian web memodifikasi prompt sistem |
| **Tombol kutipan** | ✓ | ✘ | ✘ | Mengaktifkan/menonaktifkan kutipan memodifikasi prompt sistem |
| **Pengaturan kecepatan** | ✓ | ✘ | ✘ | Beralih antara [`speed: "fast"` dan kecepatan standar](/docs/id/build-with-claude/fast-mode) membatalkan cache sistem dan pesan |
| **Pilihan alat** | ✓ | ✓ | ✘ | Perubahan pada parameter `tool_choice` hanya mempengaruhi blok pesan |
| **Gambar** | ✓ | ✓ | ✘ | Menambahkan/menghapus gambar di mana pun dalam prompt mempengaruhi blok pesan |
| **Parameter pemikiran** | ✓ | ✓ | ✘ | Perubahan pada pengaturan pemikiran yang diperluas (aktifkan/nonaktifkan, anggaran) mempengaruhi blok pesan |
| **Hasil non-alat yang diteruskan ke permintaan pemikiran yang diperluas** | ✓ | ✓ | ✘ | Ketika hasil non-alat diteruskan dalam permintaan saat pemikiran yang diperluas diaktifkan, semua blok pemikiran yang sebelumnya di-cache dihapus dari konteks, dan pesan apa pun dalam konteks yang mengikuti blok pemikiran itu dihapus dari cache. Untuk detail lebih lanjut, lihat [Penyimpanan cache dengan blok pemikiran](#caching-with-thinking-blocks). |

### Melacak kinerja cache

Pantau kinerja cache menggunakan field respons API ini, dalam `usage` dalam respons (atau event `message_start` jika [streaming](/docs/id/build-with-claude/streaming)):

- `cache_creation_input_tokens`: Jumlah token yang ditulis ke cache saat membuat entri baru.
- `cache_read_input_tokens`: Jumlah token yang diambil dari cache untuk permintaan ini.
- `input_tokens`: Jumlah token input yang tidak dibaca dari atau digunakan untuk membuat cache (yaitu, token setelah titik henti cache terakhir).

<Note>
**Memahami rincian token**

Field `input_tokens` mewakili hanya token yang datang **setelah titik henti cache terakhir** dalam permintaan Anda - bukan semua token input yang Anda kirim.

Untuk menghitung total token input:
```text
total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
```

**Penjelasan spasial:**
- `cache_read_input_tokens` = token sebelum titik henti sudah di-cache (pembacaan)
- `cache_creation_input_tokens` = token sebelum titik henti sedang di-cache sekarang (penulisan)
- `input_tokens` = token setelah titik henti terakhir Anda (tidak memenuhi syarat untuk cache)

**Contoh:** Jika Anda memiliki permintaan dengan 100.000 token konten yang di-cache (dibaca dari cache), 0 token konten baru yang di-cache, dan 50 token dalam pesan pengguna Anda (setelah titik henti cache):
- `cache_read_input_tokens`: 100.000
- `cache_creation_input_tokens`: 0
- `input_tokens`: 50
- **Total token input yang diproses**: 100.050 token

Ini penting untuk memahami biaya dan batas laju, karena `input_tokens` biasanya akan jauh lebih kecil dari total input Anda saat menggunakan penyimpanan cache secara efektif.
</Note>

### Praktik terbaik untuk penyimpanan cache yang efektif

Untuk mengoptimalkan kinerja penyimpanan cache prompt:

- Cache konten stabil dan dapat digunakan kembali seperti instruksi sistem, informasi latar belakang, konteks besar, atau definisi alat yang sering digunakan.
- Tempatkan konten yang di-cache di awal prompt untuk kinerja terbaik.
- Gunakan titik henti cache secara strategis untuk memisahkan bagian awalan yang berbeda yang dapat di-cache.
- Tetapkan titik henti cache di akhir percakapan dan tepat sebelum konten yang dapat diedit untuk memaksimalkan tingkat cache hit, terutama saat bekerja dengan prompt yang memiliki lebih dari 20 blok konten.
- Secara teratur analisis tingkat cache hit dan sesuaikan strategi Anda sesuai kebutuhan.

### Mengoptimalkan untuk kasus penggunaan yang berbeda

Sesuaikan strategi penyimpanan cache prompt Anda dengan skenario Anda:

- Agen percakapan: Kurangi biaya dan latensi untuk percakapan yang diperpanjang, terutama yang memiliki instruksi panjang atau dokumen yang diunggah.
- Asisten pengkodean: Tingkatkan pelengkapan otomatis dan Q&A basis kode dengan menyimpan bagian yang relevan atau versi ringkasan basis kode dalam prompt.
- Pemrosesan dokumen besar: Gabungkan materi bentuk panjang lengkap termasuk gambar dalam prompt Anda tanpa meningkatkan latensi respons.
- Set instruksi terperinci: Bagikan daftar instruksi, prosedur, dan contoh yang luas untuk menyempurnakan respons Claude. Pengembang sering menyertakan satu atau dua contoh dalam prompt, tetapi dengan penyimpanan cache prompt Anda dapat mencapai kinerja yang lebih baik dengan menyertakan 20+ contoh beragam jawaban berkualitas tinggi.
- Penggunaan alat agentic: Tingkatkan kinerja untuk skenario yang melibatkan beberapa panggilan alat dan perubahan kode berulang, di mana setiap langkah biasanya memerlukan panggilan API baru.
- Berbicara dengan buku, makalah, dokumentasi, transkrip podcast, dan konten bentuk panjang lainnya: Hidupkan basis pengetahuan apa pun dengan menyematkan seluruh dokumen ke dalam prompt, dan biarkan pengguna mengajukan pertanyaan padanya.

### Pemecahan masalah masalah umum

Jika mengalami perilaku yang tidak terduga:

- Pastikan bagian yang di-cache identik dan ditandai dengan cache_control di lokasi yang sama di seluruh panggilan
- Periksa bahwa panggilan dilakukan dalam masa pakai cache (5 menit secara default)
- Verifikasi bahwa `tool_choice` dan penggunaan gambar tetap konsisten antara panggilan
- Validasi bahwa Anda meng-cache setidaknya jumlah token minimum
- Sistem secara otomatis memeriksa cache hit pada batas blok konten sebelumnya (hingga ~20 blok sebelum titik henti Anda). Untuk prompt dengan lebih dari 20 blok konten, Anda mungkin memerlukan parameter `cache_control` tambahan lebih awal dalam prompt untuk memastikan semua konten dapat di-cache
- Verifikasi bahwa kunci dalam blok konten `tool_use` Anda memiliki urutan yang stabil karena beberapa bahasa (misalnya, Swift, Go) mengacak urutan kunci selama konversi JSON, merusak cache

<Note>
Perubahan pada `tool_choice` atau kehadiran/ketiadaan gambar di mana pun dalam prompt akan membatalkan cache, memerlukan entri cache baru untuk dibuat. Untuk detail lebih lanjut tentang pembatalan cache, lihat [Apa yang membatalkan cache](#what-invalidates-the-cache).
</Note>

### Penyimpanan cache dengan blok pemikiran

Ketika menggunakan [pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking) dengan penyimpanan cache prompt, blok pemikiran memiliki perilaku khusus:

**Penyimpanan cache otomatis bersama konten lain**: Meskipun blok pemikiran tidak dapat secara eksplisit ditandai dengan `cache_control`, mereka mendapat cache sebagai bagian dari konten permintaan ketika Anda membuat panggilan API berikutnya dengan hasil alat. Ini biasanya terjadi selama penggunaan alat ketika Anda meneruskan blok pemikiran kembali untuk melanjutkan percakapan.

**Penghitungan token input**: Ketika blok pemikiran dibaca dari cache, mereka menghitung sebagai token input dalam metrik penggunaan Anda. Ini penting untuk perhitungan biaya dan anggaran token.

**Pola pembatalan cache**:
- Cache tetap valid ketika hanya hasil alat yang disediakan sebagai pesan pengguna
- Cache dibatalkan ketika konten pengguna non-hasil-alat ditambahkan, menyebabkan semua blok pemikiran sebelumnya dihapus
- Perilaku penyimpanan cache ini terjadi bahkan tanpa penanda `cache_control` eksplisit

Untuk detail lebih lanjut tentang pembatalan cache, lihat [Apa yang membatalkan cache](#what-invalidates-the-cache).

**Contoh dengan penggunaan alat**:
```text
Permintaan 1: Pengguna: "Apa cuaca di Paris?"
Respons: [thinking_block_1] + [tool_use block 1]

Permintaan 2:
Pengguna: ["Apa cuaca di Paris?"],
Asisten: [thinking_block_1] + [tool_use block 1],
Pengguna: [tool_result_1, cache=True]
Respons: [thinking_block_2] + [text block 2]
# Permintaan 2 meng-cache konten permintaannya (bukan respons)
# Cache mencakup: pesan pengguna, thinking_block_1, tool_use block 1, dan tool_result_1

Permintaan 3:
Pengguna: ["Apa cuaca di Paris?"],
Asisten: [thinking_block_1] + [tool_use block 1],
Pengguna: [tool_result_1, cache=True],
Asisten: [thinking_block_2] + [text block 2],
Pengguna: [Text response, cache=True]
# Blok pengguna non-hasil-alat menyebabkan semua blok pemikiran diabaikan
# Permintaan ini diproses seolah-olah blok pemikiran tidak pernah ada
```

Ketika blok pengguna non-hasil-alat disertakan, itu menunjuk loop asisten baru dan semua blok pemikiran sebelumnya dihapus dari konteks.

Untuk informasi lebih terperinci, lihat [dokumentasi pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking#understanding-thinking-block-caching-behavior).

---
## Penyimpanan cache dan berbagi

<Warning>
Mulai 5 Februari 2026, penyimpanan cache prompt akan menggunakan isolasi tingkat ruang kerja alih-alih isolasi tingkat organisasi. Cache akan diisolasi per ruang kerja, memastikan pemisahan data antara ruang kerja dalam organisasi yang sama. Perubahan ini berlaku untuk Claude API dan Azure; Amazon Bedrock dan Google Vertex AI akan mempertahankan isolasi cache tingkat organisasi. Jika Anda menggunakan beberapa ruang kerja, tinjau strategi penyimpanan cache Anda untuk memperhitungkan perubahan ini.
</Warning>

- **Isolasi Organisasi**: Cache diisolasi antara organisasi. Organisasi yang berbeda tidak pernah berbagi cache, bahkan jika mereka menggunakan prompt yang identik.

- **Pencocokan Tepat**: Cache hit memerlukan segmen prompt 100% identik, termasuk semua teks dan gambar hingga dan termasuk blok yang ditandai dengan kontrol cache.

- **Pembuatan Token Output**: Penyimpanan cache prompt tidak memiliki efek pada pembuatan token output. Respons yang Anda terima akan identik dengan apa yang Anda dapatkan jika penyimpanan cache prompt tidak digunakan.

---
## Durasi cache 1 jam

Jika Anda menemukan bahwa 5 menit terlalu singkat, Anthropic juga menawarkan durasi cache 1 jam [dengan biaya tambahan](#pricing).

Untuk menggunakan cache yang diperluas, sertakan `ttl` dalam definisi `cache_control` seperti ini:
```json
"cache_control": {
    "type": "ephemeral",
    "ttl": "5m" | "1h"
}
```

Respons akan mencakup informasi cache terperinci seperti berikut:
```json
{
    "usage": {
        "input_tokens": ...,
        "cache_read_input_tokens": ...,
        "cache_creation_input_tokens": ...,
        "output_tokens": ...,

        "cache_creation": {
            "ephemeral_5m_input_tokens": 456,
            "ephemeral_1h_input_tokens": 100,
        }
    }
}
```

Perhatikan bahwa field `cache_creation_input_tokens` saat ini sama dengan jumlah nilai dalam objek `cache_creation`.

### Kapan menggunakan cache 1 jam

Jika Anda memiliki prompt yang digunakan dengan ritme teratur (yaitu, prompt sistem yang digunakan lebih sering daripada setiap 5 menit), terus gunakan cache 5 menit, karena ini akan terus disegarkan tanpa biaya tambahan.

Cache 1 jam paling baik digunakan dalam skenario berikut:
- Ketika Anda memiliki prompt yang kemungkinan digunakan kurang sering daripada 5 menit, tetapi lebih sering daripada setiap jam. Misalnya, ketika agen samping agentic akan memakan waktu lebih dari 5 menit, atau ketika menyimpan percakapan obrolan panjang dengan pengguna dan Anda umumnya mengharapkan pengguna itu mungkin tidak merespons dalam 5 menit berikutnya.
- Ketika latensi penting dan prompt tindak lanjut Anda mungkin dikirim di luar 5 menit.
- Ketika Anda ingin meningkatkan pemanfaatan batas laju Anda, karena cache hit tidak dikurangkan dari batas laju Anda.

<Note>
Cache 5 menit dan 1 jam berperilaku sama sehubungan dengan latensi. Anda umumnya akan melihat waktu-ke-token-pertama yang ditingkatkan untuk dokumen panjang.
</Note>

### Mencampur TTL yang berbeda

Anda dapat menggunakan kontrol cache 1 jam dan 5 menit dalam permintaan yang sama, tetapi dengan batasan penting: Entri cache dengan TTL lebih lama harus muncul sebelum TTL lebih pendek (yaitu, entri cache 1 jam harus muncul sebelum entri cache 5 menit apa pun).

Ketika mencampur TTL, kami menentukan tiga lokasi penagihan dalam prompt Anda:
1. Posisi `A`: Jumlah token pada cache hit tertinggi (atau 0 jika tidak ada hit).
2. Posisi `B`: Jumlah token pada blok `cache_control` 1 jam tertinggi setelah `A` (atau sama dengan `A` jika tidak ada).
3. Posisi `C`: Jumlah token pada blok `cache_control` terakhir.

<Note>
Jika `B` dan/atau `C` lebih besar dari `A`, mereka harus berupa cache miss, karena `A` adalah cache hit tertinggi.
</Note>

Anda akan dikenakan biaya untuk:
1. Token pembacaan cache untuk `A`.
2. Token penulisan cache 1 jam untuk `(B - A)`.
3. Token penulisan cache 5 menit untuk `(C - B)`.

Berikut adalah 3 contoh. Ini menggambarkan token input dari 3 permintaan, masing-masing memiliki cache hit dan cache miss yang berbeda. Masing-masing memiliki penagihan yang berbeda, ditunjukkan dalam kotak berwarna, sebagai hasilnya.
![Diagram Pencampuran TTL](/docs/images/prompt-cache-mixed-ttl.svg)

---

## Contoh prompt caching

Untuk membantu Anda memulai dengan prompt caching, kami telah menyiapkan [prompt caching cookbook](https://platform.claude.com/cookbook/misc-prompt-caching) dengan contoh terperinci dan praktik terbaik.

Di bawah ini, kami telah menyertakan beberapa potongan kode yang menampilkan berbagai pola prompt caching. Contoh-contoh ini menunjukkan cara mengimplementasikan caching dalam skenario berbeda, membantu Anda memahami aplikasi praktis dari fitur ini:

<section title="Contoh caching konteks besar">

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "system": [
        {
            "type": "text",
            "text": "You are an AI assistant tasked with analyzing legal documents."
        },
        {
            "type": "text",
            "text": "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": "What are the key terms and conditions in this agreement?"
        }
    ]
}'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an AI assistant tasked with analyzing legal documents.",
        },
        {
            "type": "text",
            "text": "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
            "cache_control": {"type": "ephemeral"},
        },
    ],
    messages=[
        {
            "role": "user",
            "content": "What are the key terms and conditions in this agreement?",
        }
    ],
)
print(response.model_dump_json())
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  system: [
    {
      type: "text",
      text: "You are an AI assistant tasked with analyzing legal documents."
    },
    {
      type: "text",
      text: "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [
    {
      role: "user",
      content: "What are the key terms and conditions in this agreement?"
    }
  ]
});
console.log(response);
```

```java Java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import java.util.List;

public class LegalDocumentAnalysisExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
      .maxTokens(1024)
      .systemOfTextBlockParams(
        List.of(
          TextBlockParam.builder()
            .text("You are an AI assistant tasked with analyzing legal documents.")
            .build(),
          TextBlockParam.builder()
            .text(
              "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]"
            )
            .cacheControl(CacheControlEphemeral.builder().build())
            .build()
        )
      )
      .addUserMessage("What are the key terms and conditions in this agreement?")
      .build();

    Message message = client.messages().create(params);
    System.out.println(message);
  }
}
```
</CodeGroup>
Contoh ini menunjukkan penggunaan prompt caching dasar, caching teks lengkap perjanjian hukum sebagai awalan sambil menjaga instruksi pengguna tidak di-cache.

Untuk permintaan pertama:
- `input_tokens`: Jumlah token dalam pesan pengguna saja
- `cache_creation_input_tokens`: Jumlah token dalam seluruh pesan sistem, termasuk dokumen hukum
- `cache_read_input_tokens`: 0 (tidak ada cache hit pada permintaan pertama)

Untuk permintaan berikutnya dalam masa hidup cache:
- `input_tokens`: Jumlah token dalam pesan pengguna saja
- `cache_creation_input_tokens`: 0 (tidak ada pembuatan cache baru)
- `cache_read_input_tokens`: Jumlah token dalam seluruh pesan sistem yang di-cache

</section>
<section title="Caching definisi alat">

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "tools": [
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature, either celsius or fahrenheit"
                    }
                },
                "required": ["location"]
            }
        },
        # many more tools
        {
            "name": "get_time",
            "description": "Get the current time in a given time zone",
            "input_schema": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "The IANA time zone name, e.g. America/Los_Angeles"
                    }
                },
                "required": ["timezone"]
            },
            "cache_control": {"type": "ephemeral"}
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": "What is the weather and time in New York?"
        }
    ]
}'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature, either 'celsius' or 'fahrenheit'",
                    },
                },
                "required": ["location"],
            },
        },
        # many more tools
        {
            "name": "get_time",
            "description": "Get the current time in a given time zone",
            "input_schema": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "The IANA time zone name, e.g. America/Los_Angeles",
                    }
                },
                "required": ["timezone"],
            },
            "cache_control": {"type": "ephemeral"},
        },
    ],
    messages=[{"role": "user", "content": "What's the weather and time in New York?"}],
)
print(response.model_dump_json())
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools = [
    {
      name: "get_weather",
      description: "Get the current weather in a given location",
      input_schema: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "The city and state, e.g. San Francisco, CA"
          },
          unit: {
            type: "string",
            enum: ["celsius", "fahrenheit"],
            description: "The unit of temperature, either 'celsius' or 'fahrenheit'"
          }
        },
        required: ["location"]
      }
    },
    // many more tools
    {
      name: "get_time",
      description: "Get the current time in a given time zone",
      input_schema: {
        type: "object",
        properties: {
          timezone: {
            type: "string",
            description: "The IANA time zone name, e.g. America/Los_Angeles"
          }
        },
        required: ["timezone"]
      },
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [
    {
      role: "user",
      content: "What's the weather and time in New York?"
    }
  ]
});
console.log(response);
```

```java Java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;
import java.util.List;
import java.util.Map;

public class ToolsWithCacheControlExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Weather tool schema
    InputSchema weatherSchema = InputSchema.builder()
      .properties(
        JsonValue.from(
          Map.of(
            "location",
            Map.of(
              "type",
              "string",
              "description",
              "The city and state, e.g. San Francisco, CA"
            ),
            "unit",
            Map.of(
              "type",
              "string",
              "enum",
              List.of("celsius", "fahrenheit"),
              "description",
              "The unit of temperature, either celsius or fahrenheit"
            )
          )
        )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("location")))
      .build();

    // Time tool schema
    InputSchema timeSchema = InputSchema.builder()
      .properties(
        JsonValue.from(
          Map.of(
            "timezone",
            Map.of(
              "type",
              "string",
              "description",
              "The IANA time zone name, e.g. America/Los_Angeles"
            )
          )
        )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("timezone")))
      .build();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
      .maxTokens(1024)
      .addTool(
        Tool.builder()
          .name("get_weather")
          .description("Get the current weather in a given location")
          .inputSchema(weatherSchema)
          .build()
      )
      .addTool(
        Tool.builder()
          .name("get_time")
          .description("Get the current time in a given time zone")
          .inputSchema(timeSchema)
          .cacheControl(CacheControlEphemeral.builder().build())
          .build()
      )
      .addUserMessage("What is the weather and time in New York?")
      .build();

    Message message = client.messages().create(params);
    System.out.println(message);
  }
}
```
</CodeGroup>

Dalam contoh ini, kami menunjukkan caching definisi alat.

Parameter `cache_control` ditempatkan pada alat terakhir (`get_time`) untuk menunjuk semua alat sebagai bagian dari awalan statis.

Ini berarti bahwa semua definisi alat, termasuk `get_weather` dan alat lainnya yang didefinisikan sebelum `get_time`, akan di-cache sebagai satu awalan.

Pendekatan ini berguna ketika Anda memiliki serangkaian alat yang konsisten yang ingin Anda gunakan kembali di berbagai permintaan tanpa memproses ulang setiap kali.

Untuk permintaan pertama:
- `input_tokens`: Jumlah token dalam pesan pengguna
- `cache_creation_input_tokens`: Jumlah token dalam semua definisi alat dan prompt sistem
- `cache_read_input_tokens`: 0 (tidak ada cache hit pada permintaan pertama)

Untuk permintaan berikutnya dalam masa hidup cache:
- `input_tokens`: Jumlah token dalam pesan pengguna
- `cache_creation_input_tokens`: 0 (tidak ada pembuatan cache baru)
- `cache_read_input_tokens`: Jumlah token dalam semua definisi alat dan prompt sistem yang di-cache

</section>

<section title="Melanjutkan percakapan multi-putaran">

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "system": [
        {
            "type": "text",
            "text": "...long system prompt",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hello, can you tell me more about the solar system?",
                }
            ]
        },
        {
            "role": "assistant",
            "content": "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you would like to know more about?"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Good to know."
                },
                {
                    "type": "text",
                    "text": "Tell me more about Mars.",
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        }
    ]
}'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "...long system prompt",
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[
        # ...long conversation so far
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hello, can you tell me more about the solar system?",
                }
            ],
        },
        {
            "role": "assistant",
            "content": "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you'd like to know more about?",
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Good to know."},
                {
                    "type": "text",
                    "text": "Tell me more about Mars.",
                    "cache_control": {"type": "ephemeral"},
                },
            ],
        },
    ],
)
print(response.model_dump_json())
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  system = [
    {
      type: "text",
      text: "...long system prompt",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages = [
    // ...long conversation so far
    {
      role: "user",
      content: [
        {
          type: "text",
          text: "Hello, can you tell me more about the solar system?"
        }
      ]
    },
    {
      role: "assistant",
      content: "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you'd like to know more about?"
    },
    {
      role: "user",
      content: [
        {
          type: "text",
          text: "Good to know."
        },
        {
          type: "text",
          text: "Tell me more about Mars.",
          cache_control: { type: "ephemeral" }
        }
      ]
    }
  ]
});
console.log(response);
```

```java Java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import java.util.List;

public class ConversationWithCacheControlExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Create ephemeral system prompt
    TextBlockParam systemPrompt = TextBlockParam.builder()
      .text("...long system prompt")
      .cacheControl(CacheControlEphemeral.builder().build())
      .build();

    // Create message params
    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
      .maxTokens(1024)
      .systemOfTextBlockParams(List.of(systemPrompt))
      // First user message (without cache control)
      .addUserMessage("Hello, can you tell me more about the solar system?")
      // Assistant response
      .addAssistantMessage(
        "Certainly! The solar system is the collection of celestial bodies that orbit our Sun. It consists of eight planets, numerous moons, asteroids, comets, and other objects. The planets, in order from closest to farthest from the Sun, are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Each planet has its own unique characteristics and features. Is there a specific aspect of the solar system you would like to know more about?"
      )
      // Second user message (with cache control)
      .addUserMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofText(TextBlockParam.builder().text("Good to know.").build()),
          ContentBlockParam.ofText(
            TextBlockParam.builder()
              .text("Tell me more about Mars.")
              .cacheControl(CacheControlEphemeral.builder().build())
              .build()
          )
        )
      )
      .build();

    Message message = client.messages().create(params);
    System.out.println(message);
  }
}
```
</CodeGroup>

Dalam contoh ini, kami menunjukkan cara menggunakan prompt caching dalam percakapan multi-putaran.

Selama setiap putaran, kami menandai blok terakhir dari pesan terakhir dengan `cache_control` sehingga percakapan dapat di-cache secara bertahap. Sistem akan secara otomatis mencari dan menggunakan urutan blok yang di-cache paling lama untuk pesan lanjutan. Artinya, blok yang sebelumnya ditandai dengan blok `cache_control` kemudian tidak ditandai dengan ini, tetapi mereka masih akan dianggap sebagai cache hit (dan juga penyegaran cache!) jika mereka terkena dalam 5 menit.

Selain itu, perhatikan bahwa parameter `cache_control` ditempatkan pada pesan sistem. Ini untuk memastikan bahwa jika ini dikeluarkan dari cache (setelah tidak digunakan selama lebih dari 5 menit), itu akan ditambahkan kembali ke cache pada permintaan berikutnya.

Pendekatan ini berguna untuk mempertahankan konteks dalam percakapan berkelanjutan tanpa berulang kali memproses informasi yang sama.

Ketika ini diatur dengan benar, Anda harus melihat yang berikut dalam respons penggunaan setiap permintaan:
- `input_tokens`: Jumlah token dalam pesan pengguna baru (akan minimal)
- `cache_creation_input_tokens`: Jumlah token dalam putaran asisten dan pengguna baru
- `cache_read_input_tokens`: Jumlah token dalam percakapan hingga putaran sebelumnya

</section>

<section title="Menyatukannya semua: Titik henti cache ganda">

<CodeGroup>

```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "tools": [
        {
            "name": "search_documents",
            "description": "Search through the knowledge base",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "get_document",
            "description": "Retrieve a specific document by ID",
            "input_schema": {
                "type": "object",
                "properties": {
                    "doc_id": {
                        "type": "string",
                        "description": "Document ID"
                    }
                },
                "required": ["doc_id"]
            },
            "cache_control": {"type": "ephemeral"}
        }
    ],
    "system": [
        {
            "type": "text",
            "text": "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": "Can you search for information about Mars rovers?"
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": "tool_1",
                    "name": "search_documents",
                    "input": {"query": "Mars rovers"}
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "tool_1",
                    "content": "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)"
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Yes, please tell me about the Perseverance rover specifically.",
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        }
    ]
}'
```

```python Python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[
        {
            "name": "search_documents",
            "description": "Search through the knowledge base",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"],
            },
        },
        {
            "name": "get_document",
            "description": "Retrieve a specific document by ID",
            "input_schema": {
                "type": "object",
                "properties": {
                    "doc_id": {"type": "string", "description": "Document ID"}
                },
                "required": ["doc_id"],
            },
            "cache_control": {"type": "ephemeral"},
        },
    ],
    system=[
        {
            "type": "text",
            "text": "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
            "cache_control": {"type": "ephemeral"},
        },
        {
            "type": "text",
            "text": "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
            "cache_control": {"type": "ephemeral"},
        },
    ],
    messages=[
        {
            "role": "user",
            "content": "Can you search for information about Mars rovers?",
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": "tool_1",
                    "name": "search_documents",
                    "input": {"query": "Mars rovers"},
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "tool_1",
                    "content": "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)",
                }
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document.",
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Yes, please tell me about the Perseverance rover specifically.",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
        },
    ],
)
print(response.model_dump_json())
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  tools: [
    {
      name: "search_documents",
      description: "Search through the knowledge base",
      input_schema: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description: "Search query"
          }
        },
        required: ["query"]
      }
    },
    {
      name: "get_document",
      description: "Retrieve a specific document by ID",
      input_schema: {
        type: "object",
        properties: {
          doc_id: {
            type: "string",
            description: "Document ID"
          }
        },
        required: ["doc_id"]
      },
      cache_control: { type: "ephemeral" }
    }
  ],
  system: [
    {
      type: "text",
      text: "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base",
      cache_control: { type: "ephemeral" }
    },
    {
      type: "text",
      text: "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]",
      cache_control: { type: "ephemeral" }
    }
  ],
  messages: [
    {
      role: "user",
      content: "Can you search for information about Mars rovers?"
    },
    {
      role: "assistant",
      content: [
        {
          type: "tool_use",
          id: "tool_1",
          name: "search_documents",
          input: { query: "Mars rovers" }
        }
      ]
    },
    {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: "tool_1",
          content: "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)"
        }
      ]
    },
    {
      role: "assistant",
      content: [
        {
          type: "text",
          text: "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document."
        }
      ]
    },
    {
      role: "user",
      content: [
        {
          type: "text",
          text: "Yes, please tell me about the Perseverance rover specifically.",
          cache_control: { type: "ephemeral" }
        }
      ]
    }
  ]
});
console.log(response);
```

```java Java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.JsonValue;
import com.anthropic.models.messages.CacheControlEphemeral;
import com.anthropic.models.messages.ContentBlockParam;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.TextBlockParam;
import com.anthropic.models.messages.Tool;
import com.anthropic.models.messages.Tool.InputSchema;
import com.anthropic.models.messages.ToolResultBlockParam;
import com.anthropic.models.messages.ToolUseBlockParam;
import java.util.List;
import java.util.Map;

public class MultipleCacheBreakpointsExample {

  public static void main(String[] args) {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    // Search tool schema
    InputSchema searchSchema = InputSchema.builder()
      .properties(
        JsonValue.from(
          Map.of("query", Map.of("type", "string", "description", "Search query"))
        )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("query")))
      .build();

    // Get document tool schema
    InputSchema getDocSchema = InputSchema.builder()
      .properties(
        JsonValue.from(
          Map.of("doc_id", Map.of("type", "string", "description", "Document ID"))
        )
      )
      .putAdditionalProperty("required", JsonValue.from(List.of("doc_id")))
      .build();

    MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_6)
      .maxTokens(1024)
      // Tools with cache control on the last one
      .addTool(
        Tool.builder()
          .name("search_documents")
          .description("Search through the knowledge base")
          .inputSchema(searchSchema)
          .build()
      )
      .addTool(
        Tool.builder()
          .name("get_document")
          .description("Retrieve a specific document by ID")
          .inputSchema(getDocSchema)
          .cacheControl(CacheControlEphemeral.builder().build())
          .build()
      )
      // System prompts with cache control on instructions and context separately
      .systemOfTextBlockParams(
        List.of(
          TextBlockParam.builder()
            .text(
              "You are a helpful research assistant with access to a document knowledge base.\n\n# Instructions\n- Always search for relevant documents before answering\n- Provide citations for your sources\n- Be objective and accurate in your responses\n- If multiple documents contain relevant information, synthesize them\n- Acknowledge when information is not available in the knowledge base"
            )
            .cacheControl(CacheControlEphemeral.builder().build())
            .build(),
          TextBlockParam.builder()
            .text(
              "# Knowledge Base Context\n\nHere are the relevant documents for this conversation:\n\n## Document 1: Solar System Overview\nThe solar system consists of the Sun and all objects that orbit it...\n\n## Document 2: Planetary Characteristics\nEach planet has unique features. Mercury is the smallest planet...\n\n## Document 3: Mars Exploration\nMars has been a target of exploration for decades...\n\n[Additional documents...]"
            )
            .cacheControl(CacheControlEphemeral.builder().build())
            .build()
        )
      )
      // Conversation history
      .addUserMessage("Can you search for information about Mars rovers?")
      .addAssistantMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofToolUse(
            ToolUseBlockParam.builder()
              .id("tool_1")
              .name("search_documents")
              .input(JsonValue.from(Map.of("query", "Mars rovers")))
              .build()
          )
        )
      )
      .addUserMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofToolResult(
            ToolResultBlockParam.builder()
              .toolUseId("tool_1")
              .content(
                "Found 3 relevant documents: Document 3 (Mars Exploration), Document 7 (Rover Technology), Document 9 (Mission History)"
              )
              .build()
          )
        )
      )
      .addAssistantMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofText(
            TextBlockParam.builder()
              .text(
                "I found 3 relevant documents about Mars rovers. Let me get more details from the Mars Exploration document."
              )
              .build()
          )
        )
      )
      .addUserMessageOfBlockParams(
        List.of(
          ContentBlockParam.ofText(
            TextBlockParam.builder()
              .text("Yes, please tell me about the Perseverance rover specifically.")
              .cacheControl(CacheControlEphemeral.builder().build())
              .build()
          )
        )
      )
      .build();

    Message message = client.messages().create(params);
    System.out.println(message);
  }
}
```
</CodeGroup>

Contoh komprehensif ini menunjukkan cara menggunakan semua 4 titik henti cache yang tersedia untuk mengoptimalkan bagian berbeda dari prompt Anda:

1. **Cache alat** (titik henti cache 1): Parameter `cache_control` pada definisi alat terakhir melakukan cache semua definisi alat.

2. **Cache instruksi yang dapat digunakan kembali** (titik henti cache 2): Instruksi statis dalam prompt sistem di-cache secara terpisah. Instruksi ini jarang berubah antar permintaan.

3. **Cache konteks RAG** (titik henti cache 3): Dokumen basis pengetahuan di-cache secara independen, memungkinkan Anda memperbarui dokumen RAG tanpa membatalkan cache alat atau instruksi.

4. **Cache riwayat percakapan** (titik henti cache 4): Respons asisten ditandai dengan `cache_control` untuk mengaktifkan caching bertahap percakapan saat berkembang.

Pendekatan ini memberikan fleksibilitas maksimal:
- Jika Anda hanya memperbarui pesan pengguna terakhir, keempat segmen cache digunakan kembali
- Jika Anda memperbarui dokumen RAG tetapi menjaga alat dan instruksi yang sama, dua segmen cache pertama digunakan kembali
- Jika Anda mengubah percakapan tetapi menjaga alat, instruksi, dan dokumen yang sama, tiga segmen pertama digunakan kembali
- Setiap titik henti cache dapat dibatalkan secara independen berdasarkan apa yang berubah dalam aplikasi Anda

Untuk permintaan pertama:
- `input_tokens`: Token dalam pesan pengguna terakhir
- `cache_creation_input_tokens`: Token dalam semua segmen yang di-cache (alat + instruksi + dokumen RAG + riwayat percakapan)
- `cache_read_input_tokens`: 0 (tidak ada cache hit)

Untuk permintaan berikutnya dengan hanya pesan pengguna baru:
- `input_tokens`: Token dalam pesan pengguna baru saja
- `cache_creation_input_tokens`: Token baru apa pun yang ditambahkan ke riwayat percakapan
- `cache_read_input_tokens`: Semua token yang di-cache sebelumnya (alat + instruksi + dokumen RAG + percakapan sebelumnya)

Pola ini sangat kuat untuk:
- Aplikasi RAG dengan konteks dokumen besar
- Sistem agen yang menggunakan beberapa alat
- Percakapan jangka panjang yang perlu mempertahankan konteks
- Aplikasi yang perlu mengoptimalkan bagian berbeda dari prompt secara independen

</section>

---
## FAQ

  <section title="Apakah saya memerlukan beberapa titik henti cache atau satu di akhir sudah cukup?">

    **Dalam kebanyakan kasus, satu titik henti cache di akhir konten statis Anda sudah cukup.** Sistem secara otomatis memeriksa cache hit di semua batas blok konten sebelumnya (hingga 20 blok sebelum titik henti Anda) dan menggunakan urutan blok yang di-cache paling lama.

    Anda hanya memerlukan beberapa titik henti jika:
    - Anda memiliki lebih dari 20 blok konten sebelum titik cache yang diinginkan
    - Anda ingin melakukan cache bagian yang diperbarui pada frekuensi berbeda secara independen
    - Anda memerlukan kontrol eksplisit atas apa yang di-cache untuk optimasi biaya

    Contoh: Jika Anda memiliki instruksi sistem (jarang berubah) dan konteks RAG (berubah setiap hari), Anda mungkin menggunakan dua titik henti untuk melakukan cache mereka secara terpisah.
  
</section>

  <section title="Apakah titik henti cache menambah biaya ekstra?">

    Tidak, titik henti cache itu sendiri gratis. Anda hanya membayar untuk:
    - Menulis konten ke cache (25% lebih dari token input dasar untuk TTL 5 menit)
    - Membaca dari cache (10% dari harga token input dasar)
    - Token input reguler untuk konten yang tidak di-cache

    Jumlah titik henti tidak mempengaruhi harga - hanya jumlah konten yang di-cache dan dibaca yang penting.
  
</section>

  <section title="Bagaimana cara menghitung total token input dari bidang penggunaan?">

    Respons penggunaan mencakup tiga bidang token input terpisah yang bersama-sama mewakili total input Anda:

    ```text
    total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
    ```

    - `cache_read_input_tokens`: Token yang diambil dari cache (semuanya sebelum titik henti cache yang di-cache)
    - `cache_creation_input_tokens`: Token baru yang ditulis ke cache (di titik henti cache)
    - `input_tokens`: Token **setelah titik henti cache terakhir** yang tidak di-cache

    **Penting:** `input_tokens` TIDAK mewakili semua token input - hanya bagian setelah titik henti cache terakhir Anda. Jika Anda memiliki konten yang di-cache, `input_tokens` biasanya akan jauh lebih kecil dari total input Anda.

    **Contoh:** Dengan dokumen 200K token yang di-cache dan pertanyaan pengguna 50 token:
    - `cache_read_input_tokens`: 200.000
    - `cache_creation_input_tokens`: 0
    - `input_tokens`: 50
    - **Total**: 200.050 token

    Rincian ini sangat penting untuk memahami biaya dan penggunaan batas laju Anda. Lihat [Melacak kinerja cache](#tracking-cache-performance) untuk detail lebih lanjut.
  
</section>

  <section title="Berapa lama masa hidup cache?">

    Masa hidup minimum cache (TTL) default adalah 5 menit. Masa hidup ini disegarkan setiap kali konten yang di-cache digunakan.

    Jika Anda menemukan bahwa 5 menit terlalu singkat, Anthropic juga menawarkan [cache TTL 1 jam](#1-hour-cache-duration).
  
</section>

  <section title="Berapa banyak titik henti cache yang dapat saya gunakan?">

    Anda dapat menentukan hingga 4 titik henti cache (menggunakan parameter `cache_control`) dalam prompt Anda.
  
</section>

  <section title="Apakah prompt caching tersedia untuk semua model?">

    Tidak, prompt caching saat ini hanya tersedia untuk Claude Opus 4.6, Claude Opus 4.5, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.1, Claude Opus 4, Claude Sonnet 4, Claude Sonnet 3.7 ([deprecated](/docs/id/about-claude/model-deprecations)), Claude Haiku 4.5, Claude Haiku 3.5 ([deprecated](/docs/id/about-claude/model-deprecations)), dan Claude Haiku 3.
  
</section>

  <section title="Bagaimana cara kerja prompt caching dengan pemikiran yang diperluas?">

    Prompt sistem yang di-cache dan alat akan digunakan kembali ketika parameter pemikiran berubah. Namun, perubahan pemikiran (mengaktifkan/menonaktifkan atau perubahan anggaran) akan membatalkan awalan prompt yang sebelumnya di-cache dengan konten pesan.

    Untuk detail lebih lanjut tentang pembatalan cache, lihat [Apa yang membatalkan cache](#what-invalidates-the-cache).

    Untuk lebih lanjut tentang pemikiran yang diperluas, termasuk interaksinya dengan penggunaan alat dan prompt caching, lihat [dokumentasi pemikiran yang diperluas](/docs/id/build-with-claude/extended-thinking#extended-thinking-and-prompt-caching).
  
</section>

  <section title="Bagaimana cara mengaktifkan prompt caching?">

    Untuk mengaktifkan prompt caching, sertakan setidaknya satu titik henti `cache_control` dalam permintaan API Anda.
  
</section>

  <section title="Bisakah saya menggunakan prompt caching dengan fitur API lainnya?">

    Ya, prompt caching dapat digunakan bersama fitur API lainnya seperti penggunaan alat dan kemampuan visi. Namun, mengubah apakah ada gambar dalam prompt atau memodifikasi pengaturan penggunaan alat akan memecahkan cache.

    Untuk detail lebih lanjut tentang pembatalan cache, lihat [Apa yang membatalkan cache](#what-invalidates-the-cache).
  
</section>

  <section title="Bagaimana prompt caching mempengaruhi harga?">

    Prompt caching memperkenalkan struktur harga baru di mana penulisan cache biaya 25% lebih dari token input dasar, sementara cache hit biaya hanya 10% dari harga token input dasar.
  
</section>

  <section title="Bisakah saya menghapus cache secara manual?">

    Saat ini, tidak ada cara untuk menghapus cache secara manual. Awalan yang di-cache secara otomatis kedaluwarsa setelah minimal 5 menit tidak aktif.
  
</section>

  <section title="Bagaimana cara melacak efektivitas strategi caching saya?">

    Anda dapat memantau kinerja cache menggunakan bidang `cache_creation_input_tokens` dan `cache_read_input_tokens` dalam respons API.
  
</section>

  <section title="Apa yang dapat memecahkan cache?">

    Lihat [Apa yang membatalkan cache](#what-invalidates-the-cache) untuk detail lebih lanjut tentang pembatalan cache, termasuk daftar perubahan yang memerlukan pembuatan entri cache baru.
  
</section>

  <section title="Bagaimana prompt caching menangani privasi dan pemisahan data?">

Prompt caching dirancang dengan langkah-langkah privasi dan pemisahan data yang kuat:

1. Kunci cache dihasilkan menggunakan hash kriptografi dari prompt hingga titik kontrol cache. Ini berarti hanya permintaan dengan prompt identik yang dapat mengakses cache tertentu.

2. Cache adalah spesifik organisasi. Pengguna dalam organisasi yang sama dapat mengakses cache yang sama jika mereka menggunakan prompt identik, tetapi cache tidak dibagikan di seluruh organisasi yang berbeda, bahkan untuk prompt identik.

3. Mekanisme caching dirancang untuk mempertahankan integritas dan privasi setiap percakapan atau konteks unik.

4. Aman untuk menggunakan `cache_control` di mana saja dalam prompt Anda. Untuk efisiensi biaya, lebih baik mengecualikan bagian yang sangat variabel (misalnya, input arbitrer pengguna) dari caching.

Langkah-langkah ini memastikan bahwa prompt caching mempertahankan privasi dan keamanan data sambil menawarkan manfaat kinerja.

Catatan: Mulai 5 Februari 2026, cache akan diisolasi per ruang kerja alih-alih per organisasi. Perubahan ini berlaku untuk Claude API dan Azure. Lihat [Penyimpanan dan berbagi cache](#cache-storage-and-sharing) untuk detail.

  
</section>
  <section title="Bisakah saya menggunakan prompt caching dengan Batches API?">

    Ya, dimungkinkan untuk menggunakan prompt caching dengan permintaan [Batches API](/docs/id/build-with-claude/batch-processing) Anda. Namun, karena permintaan batch asinkron dapat diproses secara bersamaan dan dalam urutan apa pun, cache hit disediakan atas dasar upaya terbaik.

    [Cache 1 jam](#1-hour-cache-duration) dapat membantu meningkatkan cache hit Anda. Cara paling hemat biaya untuk menggunakannya adalah sebagai berikut:
    - Kumpulkan serangkaian permintaan pesan yang memiliki awalan bersama.
    - Kirim permintaan batch dengan hanya satu permintaan yang memiliki awalan bersama ini dan blok cache 1 jam. Ini akan ditulis ke cache 1 jam.
    - Segera setelah selesai, kirimkan sisa permintaan. Anda harus memantau pekerjaan untuk mengetahui kapan selesai.

    Ini biasanya lebih baik daripada menggunakan cache 5 menit hanya karena umum untuk permintaan batch memakan waktu antara 5 menit dan 1 jam untuk diselesaikan. Kami mempertimbangkan cara untuk meningkatkan tingkat cache hit ini dan membuat proses ini lebih mudah.
  
</section>
  <section title="Mengapa saya melihat kesalahan `AttributeError: 'Beta' object has no attribute 'prompt_caching'` di Python?">

  Kesalahan ini biasanya muncul ketika Anda telah meningkatkan SDK atau menggunakan contoh kode yang sudah ketinggalan zaman. Prompt caching sekarang tersedia secara umum, jadi Anda tidak lagi memerlukan awalan beta. Alih-alih:
    <CodeGroup>
      ```python
      client.beta.prompt_caching.messages.create(**params)
      ```
    </CodeGroup>
    Cukup gunakan:
    <CodeGroup>
      ```python
      client.messages.create(**params)
      ```
    </CodeGroup>
  
</section>
  <section title="Mengapa saya melihat 'TypeError: Cannot read properties of undefined (reading 'messages')'?">

  Kesalahan ini biasanya muncul ketika Anda telah meningkatkan SDK atau menggunakan contoh kode yang sudah ketinggalan zaman. Prompt caching sekarang tersedia secara umum, jadi Anda tidak lagi memerlukan awalan beta. Alih-alih:

      ```typescript TypeScript
      client.beta.promptCaching.messages.create(/* ... */);
      ```

      Cukup gunakan:

      ```typescript
      client.messages.create(/* ... */);
      ```
  
</section>