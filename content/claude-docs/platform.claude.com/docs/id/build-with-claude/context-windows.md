---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/context-windows
fetched_at: 2026-02-19T04:23:04.153807Z
sha256: afe5c015520e2b7fabfe789211e324511821560dbc619d54a69a892349081fbd
---

# Jendela konteks

Pelajari cara mengelola jendela konteks saat percakapan berkembang, termasuk strategi kompaksi dan pengeditan konteks.

---

Seiring percakapan berkembang, Anda pada akhirnya akan mendekati batas jendela konteks. Panduan ini menjelaskan cara kerja jendela konteks dan memperkenalkan strategi untuk mengelolanya secara efektif.

Untuk percakapan jangka panjang dan alur kerja agentic, [kompaksi sisi server](/docs/id/build-with-claude/compaction) adalah strategi utama untuk manajemen konteks. Untuk kebutuhan yang lebih khusus, [pengeditan konteks](/docs/id/build-with-claude/context-editing) menawarkan strategi tambahan seperti pembersihan hasil alat dan pembersihan blok pemikiran.

## Memahami jendela konteks

"Jendela konteks" mengacu pada semua teks yang dapat direferensikan model bahasa saat menghasilkan respons, termasuk respons itu sendiri. Ini berbeda dari corpus data besar tempat model bahasa dilatih, dan sebaliknya mewakili "memori kerja" untuk model. Jendela konteks yang lebih besar memungkinkan model menangani prompt yang lebih kompleks dan panjang. Jendela konteks yang lebih kecil dapat membatasi kemampuan model untuk mempertahankan kohesi selama percakapan yang diperpanjang.

Diagram di bawah mengilustrasikan perilaku jendela konteks standar untuk permintaan API<sup>1</sup>:

![Diagram jendela konteks](/docs/images/context-window.svg)

_<sup>1</sup>Untuk antarmuka obrolan, seperti untuk [claude.ai](https://claude.ai/), jendela konteks juga dapat diatur pada sistem "masuk pertama, keluar pertama" yang bergulir._

* **Akumulasi token progresif:** Seiring percakapan maju melalui giliran, setiap pesan pengguna dan respons asisten terakumulasi dalam jendela konteks. Giliran sebelumnya dipertahankan sepenuhnya.
* **Pola pertumbuhan linier:** Penggunaan konteks tumbuh secara linier dengan setiap giliran, dengan giliran sebelumnya dipertahankan sepenuhnya.
* **Kapasitas token 200K:** Jendela konteks total yang tersedia (200.000 token) mewakili kapasitas maksimum untuk menyimpan riwayat percakapan dan menghasilkan output baru dari Claude.
* **Aliran input-output:** Setiap giliran terdiri dari:
  - **Fase input:** Berisi semua riwayat percakapan sebelumnya ditambah pesan pengguna saat ini
  - **Fase output:** Menghasilkan respons teks yang menjadi bagian dari input masa depan

## Jendela konteks dengan pemikiran yang diperpanjang

Saat menggunakan [pemikiran yang diperpanjang](/docs/id/build-with-claude/extended-thinking), semua token input dan output, termasuk token yang digunakan untuk pemikiran, dihitung menuju batas jendela konteks, dengan beberapa nuansa dalam situasi multi-giliran.

Token anggaran pemikiran adalah subset dari parameter `max_tokens` Anda, ditagih sebagai token output, dan dihitung menuju batas laju. Dengan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking), Claude secara dinamis memutuskan alokasi pemikirannya, jadi penggunaan token pemikiran aktual dapat bervariasi per permintaan.

Namun, blok pemikiran sebelumnya secara otomatis dilepas dari perhitungan jendela konteks oleh API Claude dan bukan bagian dari riwayat percakapan yang "dilihat" model untuk giliran berikutnya, menjaga kapasitas token untuk konten percakapan aktual.

Diagram di bawah menunjukkan manajemen token khusus saat pemikiran yang diperpanjang diaktifkan:

![Diagram jendela konteks dengan pemikiran yang diperpanjang](/docs/images/context-window-thinking.svg)

* **Melepas pemikiran yang diperpanjang:** Blok pemikiran yang diperpanjang (ditampilkan dalam abu-abu gelap) dihasilkan selama fase output setiap giliran, **tetapi tidak dibawa maju sebagai token input untuk giliran berikutnya**. Anda tidak perlu melepas blok pemikiran sendiri. API Claude secara otomatis melakukan ini untuk Anda jika Anda meneruskannya kembali.
* **Detail implementasi teknis:**
  - API secara otomatis mengecualikan blok pemikiran dari giliran sebelumnya saat Anda meneruskannya kembali sebagai bagian dari riwayat percakapan.
  - Token pemikiran yang diperpanjang ditagih sebagai token output hanya sekali, selama pembuatannya.
  - Perhitungan jendela konteks yang efektif menjadi: `context_window = (input_tokens - previous_thinking_tokens) + current_turn_tokens`.
  - Token pemikiran mencakup blok `thinking` dan blok `redacted_thinking`.

Arsitektur ini efisien token dan memungkinkan penalaran ekstensif tanpa pemborosan token, karena blok pemikiran dapat memiliki panjang yang substansial.

<Note>
Anda dapat membaca lebih lanjut tentang jendela konteks dan pemikiran yang diperpanjang dalam [panduan pemikiran yang diperpanjang](/docs/id/build-with-claude/extended-thinking).
</Note>

## Jendela konteks dengan pemikiran yang diperpanjang dan penggunaan alat

Diagram di bawah mengilustrasikan manajemen token jendela konteks saat menggabungkan pemikiran yang diperpanjang dengan penggunaan alat:

![Diagram jendela konteks dengan pemikiran yang diperpanjang dan penggunaan alat](/docs/images/context-window-thinking-tools.svg)

<Steps>
  <Step title="Arsitektur giliran pertama">
    - **Komponen input:** Konfigurasi alat dan pesan pengguna
    - **Komponen output:** Pemikiran yang diperpanjang + respons teks + permintaan penggunaan alat
    - **Perhitungan token:** Semua komponen input dan output dihitung menuju jendela konteks, dan semua komponen output ditagih sebagai token output.
  </Step>
  <Step title="Penanganan hasil alat (giliran 2)">
    - **Komponen input:** Setiap blok di giliran pertama serta `tool_result`. Blok pemikiran yang diperpanjang **harus** dikembalikan dengan hasil alat yang sesuai. Ini adalah satu-satunya kasus di mana Anda **harus** mengembalikan blok pemikiran.
    - **Komponen output:** Setelah hasil alat telah diteruskan kembali ke Claude, Claude akan merespons hanya dengan teks (tidak ada pemikiran yang diperpanjang tambahan sampai pesan `user` berikutnya).
    - **Perhitungan token:** Semua komponen input dan output dihitung menuju jendela konteks, dan semua komponen output ditagih sebagai token output.
  </Step>
  <Step title="Langkah Ketiga">
    - **Komponen input:** Semua input dan output dari giliran sebelumnya dibawa maju dengan pengecualian blok pemikiran, yang dapat dijatuhkan sekarang bahwa Claude telah menyelesaikan seluruh siklus penggunaan alat. API akan secara otomatis melepas blok pemikiran untuk Anda jika Anda meneruskannya kembali, atau Anda dapat merasa bebas untuk melepasnya sendiri pada tahap ini. Ini juga di mana Anda akan menambahkan giliran `User` berikutnya.
    - **Komponen output:** Karena ada giliran `User` baru di luar siklus penggunaan alat, Claude akan menghasilkan blok pemikiran yang diperpanjang baru dan melanjutkan dari sana.
    - **Perhitungan token:** Token pemikiran sebelumnya secara otomatis dilepas dari perhitungan jendela konteks. Semua blok sebelumnya lainnya masih dihitung sebagai bagian dari jendela token, dan blok pemikiran dalam giliran `Assistant` saat ini dihitung sebagai bagian dari jendela konteks.
  </Step>
</Steps>

* **Pertimbangan untuk penggunaan alat dengan pemikiran yang diperpanjang:**
  - Saat memposting hasil alat, seluruh blok pemikiran yang tidak dimodifikasi yang menyertai permintaan alat spesifik itu (termasuk bagian tanda tangan/redaksi) harus disertakan.
  - Perhitungan jendela konteks yang efektif untuk pemikiran yang diperpanjang dengan penggunaan alat menjadi: `context_window = input_tokens + current_turn_tokens`.
  - Sistem menggunakan tanda tangan kriptografi untuk memverifikasi keaslian blok pemikiran. Gagal mempertahankan blok pemikiran selama penggunaan alat dapat memecah kontinuitas penalaran Claude. Jadi, jika Anda memodifikasi blok pemikiran, API akan mengembalikan kesalahan.

<Note>
Model Claude 4 mendukung [pemikiran yang disisipi](/docs/id/build-with-claude/extended-thinking#interleaved-thinking), yang memungkinkan Claude untuk berpikir di antara panggilan alat dan melakukan penalaran yang lebih canggih setelah menerima hasil alat.

Claude Sonnet 3.7 tidak mendukung pemikiran yang disisipi, jadi tidak ada penyisipan pemikiran yang diperpanjang dan panggilan alat tanpa giliran pengguna non-`tool_result` di antaranya.

Untuk informasi lebih lanjut tentang menggunakan alat dengan pemikiran yang diperpanjang, lihat [panduan pemikiran yang diperpanjang](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-tool-use).
</Note>

## Jendela konteks token 1M

Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5, dan Sonnet 4 mendukung jendela konteks token 1 juta. Jendela konteks yang diperpanjang ini memungkinkan Anda memproses dokumen yang jauh lebih besar, mempertahankan percakapan yang lebih lama, dan bekerja dengan basis kode yang lebih ekstensif.

<Note>
Jendela konteks token 1M saat ini dalam beta untuk organisasi dalam [tingkat penggunaan](/docs/id/api/rate-limits) 4 dan organisasi dengan batas laju kustom. Jendela konteks token 1M hanya tersedia untuk Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5, dan Sonnet 4.
</Note>

Untuk menggunakan jendela konteks token 1M, sertakan [header beta](/docs/id/api/beta-headers) `context-1m-2025-08-07` dalam permintaan API Anda:

<CodeGroup>

```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: context-1m-2025-08-07" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Process this large document..."}
    ]
  }'
```

```python Python
from anthropic import Anthropic

client = Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Process this large document..."}],
    betas=["context-1m-2025-08-07"],
)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic();

const msg = await anthropic.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "Process this large document..." }
  ],
  betas: ["context-1m-2025-08-07"]
});
```

</CodeGroup>

**Pertimbangan penting:**
- **Status beta:** Ini adalah fitur beta yang dapat berubah. Fitur dan harga dapat dimodifikasi atau dihapus dalam rilis mendatang.
- **Persyaratan tingkat penggunaan:** Jendela konteks token 1M tersedia untuk organisasi dalam [tingkat penggunaan](/docs/id/api/rate-limits) 4 dan organisasi dengan batas laju kustom. Organisasi tingkat lebih rendah harus maju ke tingkat penggunaan 4 untuk mengakses fitur ini.
- **Ketersediaan:** Jendela konteks token 1M saat ini tersedia di Claude API, [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry), [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock), dan [Google Cloud's Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai).
- **Harga:** Permintaan yang melebihi 200K token secara otomatis ditagih dengan tarif premium (2x input, 1,5x output pricing). Lihat [dokumentasi harga](/docs/id/about-claude/pricing#long-context-pricing) untuk detail.
- **Batas laju:** Permintaan konteks panjang memiliki batas laju khusus. Lihat [dokumentasi batas laju](/docs/id/api/rate-limits#long-context-rate-limits) untuk detail.
- **Pertimbangan multimodal:** Saat memproses sejumlah besar gambar atau pdf, perhatikan bahwa file dapat bervariasi dalam penggunaan token. Saat memasangkan prompt besar dengan sejumlah besar gambar, Anda mungkin mencapai [batas ukuran permintaan](/docs/id/api/overview#request-size-limits).

## Kesadaran konteks di Claude Sonnet 4.6, Sonnet 4.5, dan Haiku 4.5

Claude Sonnet 4.6, Claude Sonnet 4.5, dan Claude Haiku 4.5 menampilkan **kesadaran konteks**. Kemampuan ini memungkinkan model-model ini melacak jendela konteks sisa mereka (yaitu "anggaran token") sepanjang percakapan. Ini memungkinkan Claude untuk menjalankan tugas dan mengelola konteks lebih efektif dengan memahami berapa banyak ruang yang dimilikinya untuk bekerja. Claude dilatih untuk menggunakan konteks ini dengan tepat, bertahan dalam tugas sampai akhir daripada menebak berapa banyak token yang tersisa. Bagi model, kurangnya kesadaran konteks seperti berkompetisi dalam acara memasak tanpa jam. Model Claude 4.5+ mengubah ini dengan secara eksplisit menginformasikan model tentang konteks sisanya, sehingga dapat memanfaatkan token yang tersedia secara maksimal.

**Cara kerjanya:**

Di awal percakapan, Claude menerima informasi tentang jendela konteks totalnya:

```xml
<budget:token_budget>200000</budget:token_budget>
```

Anggaran ditetapkan ke 200K token (standar), 500K token (claude.ai Enterprise), atau 1M token (beta, untuk organisasi yang memenuhi syarat).

Setelah setiap panggilan alat, Claude menerima pembaruan tentang kapasitas sisa:

```xml
<system_warning>Token usage: 35000/200000; 165000 remaining</system_warning>
```

Kesadaran ini membantu Claude menentukan berapa banyak kapasitas yang tersisa untuk pekerjaan dan memungkinkan eksekusi yang lebih efektif pada tugas jangka panjang. Token gambar disertakan dalam anggaran ini.

**Manfaat:**

Kesadaran konteks sangat berharga untuk:
- Sesi agen jangka panjang yang memerlukan fokus berkelanjutan
- Alur kerja multi-jendela-konteks di mana transisi status penting
- Tugas kompleks yang memerlukan manajemen token yang cermat

Untuk panduan prompting tentang memanfaatkan kesadaran konteks, lihat [panduan praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#context-awareness-and-multi-window-workflows).

## Mengelola konteks dengan kompaksi

Jika percakapan Anda secara teratur mendekati batas jendela konteks, [kompaksi sisi server](/docs/id/build-with-claude/compaction) adalah pendekatan yang direkomendasikan. Kompaksi menyediakan ringkasan sisi server yang secara otomatis mengondensasi bagian awal percakapan, memungkinkan percakapan jangka panjang melampaui batas konteks dengan pekerjaan integrasi minimal. Saat ini tersedia dalam beta untuk Claude Opus 4.6.

Untuk kebutuhan yang lebih khusus, [pengeditan konteks](/docs/id/build-with-claude/context-editing) menawarkan strategi tambahan:
- **Pembersihan hasil alat** - Hapus hasil alat lama dalam alur kerja agentic
- **Pembersihan blok pemikiran** - Kelola blok pemikiran dengan pemikiran yang diperpanjang

## Manajemen jendela konteks dengan model Claude yang lebih baru

Model Claude yang lebih baru (dimulai dengan Claude Sonnet 3.7) mengembalikan kesalahan validasi saat token prompt dan output melebihi jendela konteks, daripada secara diam-diam memotong. Perubahan ini memberikan perilaku yang lebih dapat diprediksi tetapi memerlukan manajemen token yang lebih hati-hati.

Gunakan [API penghitungan token](/docs/id/build-with-claude/token-counting) untuk memperkirakan penggunaan token sebelum mengirim pesan ke Claude. Ini membantu Anda merencanakan dan tetap berada dalam batas jendela konteks.

Lihat tabel [perbandingan model](/docs/id/about-claude/models/overview#latest-models-comparison) untuk daftar ukuran jendela konteks menurut model.

## Langkah berikutnya
<CardGroup cols={2}>
  <Card title="Kompaksi" icon="compress" href="/docs/id/build-with-claude/compaction">
    Strategi yang direkomendasikan untuk mengelola konteks dalam percakapan jangka panjang.
  </Card>
  <Card title="Pengeditan konteks" icon="pen" href="/docs/id/build-with-claude/context-editing">
    Strategi butir halus seperti pembersihan hasil alat dan pembersihan blok pemikiran.
  </Card>
  <Card title="Tabel perbandingan model" icon="scales" href="/docs/id/about-claude/models/overview#latest-models-comparison">
    Lihat tabel perbandingan model untuk daftar ukuran jendela konteks dan harga token input / output menurut model.
  </Card>
  <Card title="Gambaran umum pemikiran yang diperpanjang" icon="settings" href="/docs/id/build-with-claude/extended-thinking">
    Pelajari lebih lanjut tentang cara kerja pemikiran yang diperpanjang dan cara mengimplementasikannya bersama fitur lain seperti penggunaan alat dan caching prompt.
  </Card>
</CardGroup>