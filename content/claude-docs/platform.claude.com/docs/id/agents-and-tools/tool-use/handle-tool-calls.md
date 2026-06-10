---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 4336686bb2bf27719b975ae735483fde7f520326949f87d041c92fbe45083974
---

# Menangani panggilan alat

Mengurai blok tool_use, memformat respons tool_result, dan menangani kesalahan dengan is_error.

---

Halaman ini membahas siklus hidup panggilan alat: membaca blok `tool_use` dari respons Claude, memformat blok `tool_result` dalam balasan Anda, dan memberi sinyal kesalahan. Untuk abstraksi SDK yang menangani hal ini secara otomatis, lihat [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner).

<Note>
**Lebih sederhana dengan Tool Runner**: Penanganan alat secara manual yang dijelaskan di halaman ini dikelola secara otomatis oleh [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner). Gunakan halaman ini ketika Anda membutuhkan kontrol khusus atas eksekusi alat.
</Note>

Respons Claude berbeda tergantung pada apakah ia menggunakan [alat klien atau server](/docs/id/agents-and-tools/tool-use/overview#how-tool-use-works).

## Menangani hasil dari alat klien \{#handling-results-from-client-tools}

Respons akan memiliki `stop_reason` berupa `tool_use` dan satu atau lebih blok konten `tool_use` yang mencakup:

- `id`: Pengidentifikasi unik untuk blok penggunaan alat tertentu ini. Ini akan digunakan untuk mencocokkan hasil alat nantinya.
- `name`: Nama alat yang sedang digunakan.
- `input`: Objek yang berisi input yang diteruskan ke alat, sesuai dengan `input_schema` alat tersebut.

<section title="Contoh respons API dengan blok konten `tool_use`">

```json JSON
{
  "id": "msg_01Aq9w938a90dw8q",
  "model": "claude-opus-4-8",
  "stop_reason": "tool_use",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "I'll check the current weather in San Francisco for you."
    },
    {
      "type": "tool_use",
      "id": "toolu_01A09q90qw90lq917835lq9",
      "name": "get_weather",
      "input": { "location": "San Francisco, CA", "unit": "celsius" }
    }
  ]
}
```

</section>

Ketika Anda menerima respons penggunaan alat untuk alat klien, Anda harus:

1. Mengekstrak `name`, `id`, dan `input` dari blok `tool_use`.
2. Menjalankan alat yang sebenarnya dalam basis kode Anda yang sesuai dengan nama alat tersebut, dengan meneruskan `input` alat.
3. Melanjutkan percakapan dengan mengirim pesan baru dengan `role` berupa `user`, dan blok `content` yang berisi tipe `tool_result` serta informasi berikut:
   - `tool_use_id`: `id` dari permintaan penggunaan alat yang hasilnya ini.
   - `content` (opsional): Hasil dari alat, sebagai string (misalnya, `"content": "15 degrees"`), daftar blok konten bersarang (misalnya, `"content": [{"type": "text", "text": "15 degrees"}]`), atau daftar blok dokumen (misalnya, `"content": [{"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": "15 degrees"}}]`). Blok konten ini dapat menggunakan tipe `text`, `image`, atau `document`.
   - `is_error` (opsional): Atur ke `true` jika eksekusi alat menghasilkan kesalahan.

<Note>
**Persyaratan pemformatan penting**:
- Blok hasil alat harus langsung mengikuti blok penggunaan alat yang sesuai dalam riwayat pesan. Anda tidak dapat menyertakan pesan apa pun di antara pesan penggunaan alat dari asisten dan pesan hasil alat dari pengguna.
- Dalam pesan pengguna yang berisi hasil alat, blok tool_result harus berada PERTAMA dalam array konten. Teks apa pun harus berada SETELAH semua hasil alat.

Misalnya, ini akan menyebabkan kesalahan 400:
```json
{
  "role": "user",
  "content": [
    { "type": "text", "text": "Here are the results:" }, // ❌ Text before tool_result
    { "type": "tool_result", "tool_use_id": "toolu_01" /* ... */ }
  ]
}
```

Ini benar:
```json
{
  "role": "user",
  "content": [
    { "type": "tool_result", "tool_use_id": "toolu_01" /* ... */ },
    { "type": "text", "text": "What should I do next?" } // ✅ Text after tool_result
  ]
}
```

Jika Anda menerima kesalahan seperti "tool_use ids were found without tool_result blocks immediately after", periksa apakah hasil alat Anda diformat dengan benar.
</Note>

<Warning>
Hasil alat sering kali membawa konten dari sumber di luar kendali Anda: halaman web, email masuk, unggahan pengguna, API pihak ketiga. Perlakukan konten tersebut sebagai tidak tepercaya: penyerang yang dapat memengaruhinya mungkin menyematkan instruksi yang mencoba mengalihkan Claude (injeksi prompt tidak langsung). Simpan konten yang tidak tepercaya di dalam blok `tool_result` alih-alih prompt `system` atau blok `text` pengguna biasa, dan lihat [Mitigasi jailbreak dan injeksi prompt](/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks#indirect-prompt-injection) untuk penguatan lebih lanjut.
</Warning>

<section title="Contoh hasil alat yang berhasil">

```json JSON
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "15 degrees"
    }
  ]
}
```

</section>

<section title="Contoh hasil alat dengan gambar">

```json JSON
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": [
        { "type": "text", "text": "15 degrees" },
        {
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": "/9j/4AAQSkZJRg..."
          }
        }
      ]
    }
  ]
}
```

</section>
<section title="Contoh hasil alat kosong">

```json JSON
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9"
    }
  ]
}
```

</section>

<section title="Contoh hasil alat dengan dokumen">

```json JSON
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": [
        { "type": "text", "text": "The weather is" },
        {
          "type": "document",
          "source": {
            "type": "text",
            "media_type": "text/plain",
            "data": "15 degrees"
          }
        }
      ]
    }
  ]
}
```

</section>

Setelah menerima hasil alat, Claude akan menggunakan informasi tersebut untuk melanjutkan menghasilkan respons terhadap prompt pengguna asli.

## Menangani hasil dari alat server \{#handling-results-from-server-tools}

Claude mengeksekusi alat secara internal dan menggabungkan hasilnya langsung ke dalam responsnya tanpa memerlukan interaksi pengguna tambahan.

<Tip>
  **Perbedaan dari API lain**

Tidak seperti API yang memisahkan penggunaan alat atau menggunakan peran khusus seperti `tool` atau `function`, API Claude mengintegrasikan alat langsung ke dalam struktur pesan `user` dan `assistant`.

Pesan berisi array blok `text`, `image`, `tool_use`, dan `tool_result`. Pesan `user` mencakup konten klien dan `tool_result`, sedangkan pesan `assistant` berisi konten yang dihasilkan AI dan `tool_use`.

</Tip>

## Menangani kesalahan dengan is_error \{#handling-errors-with-is-error}

Ada beberapa jenis kesalahan berbeda yang dapat terjadi saat menggunakan alat dengan Claude:

<section title="Kesalahan eksekusi alat">

Jika alat itu sendiri melemparkan kesalahan selama eksekusi (misalnya, kesalahan jaringan saat mengambil data cuaca), Anda dapat mengembalikan pesan kesalahan dalam `content` bersama dengan `"is_error": true`:

```json JSON
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "ConnectionError: the weather service API is not available (HTTP 500)",
      "is_error": true
    }
  ]
}
```

Claude kemudian akan menggabungkan kesalahan ini ke dalam responsnya kepada pengguna. Misalnya: "Maaf, saya tidak dapat mengambil cuaca saat ini karena API layanan cuaca tidak tersedia. Silakan coba lagi nanti."

<Tip>
Tulis pesan kesalahan yang instruktif. Alih-alih kesalahan generik seperti `"failed"`, sertakan apa yang salah dan apa yang harus dicoba Claude selanjutnya, misalnya, `"Rate limit exceeded. Retry after 60 seconds."` Ini memberi Claude konteks yang dibutuhkan untuk pulih atau beradaptasi tanpa menebak-nebak.
</Tip>

</section>
<section title="Nama alat tidak valid">

Jika upaya Claude untuk menggunakan alat tidak valid (misalnya, parameter yang diperlukan tidak ada), biasanya ini berarti tidak ada cukup informasi bagi Claude untuk menggunakan alat dengan benar. Langkah terbaik Anda selama pengembangan adalah mencoba permintaan lagi dengan nilai `description` yang lebih detail dalam definisi alat Anda.

Namun, Anda juga dapat melanjutkan percakapan dengan `tool_result` yang menunjukkan kesalahan tersebut, dan Claude akan mencoba menggunakan alat lagi dengan informasi yang hilang diisi:

```json JSON
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Missing required 'location' parameter",
      "is_error": true
    }
  ]
}
```

Jika permintaan alat tidak valid atau parameternya tidak lengkap, Claude akan mencoba ulang 2-3 kali dengan koreksi sebelum meminta maaf kepada pengguna.

<Tip>
Untuk menghilangkan panggilan alat yang tidak valid sepenuhnya, gunakan [penggunaan alat ketat](/docs/id/agents-and-tools/tool-use/strict-tool-use) dengan `strict: true` pada definisi alat Anda. Ini menjamin bahwa input alat akan selalu cocok dengan skema Anda secara persis, mencegah parameter yang hilang dan ketidakcocokan tipe.
</Tip>

</section>
<section title="Kesalahan alat server">

Ketika alat server mengalami kesalahan (misalnya, masalah jaringan dengan Web Search), Claude akan menangani kesalahan ini secara transparan dan berupaya memberikan respons atau penjelasan alternatif kepada pengguna. Tidak seperti alat klien, Anda tidak perlu menangani hasil `is_error` untuk alat server.

Untuk pencarian web secara khusus, kode kesalahan yang mungkin meliputi:
- `too_many_requests`: Batas laju terlampaui
- `invalid_input`: Parameter kueri pencarian tidak valid
- `max_uses_exceeded`: Penggunaan maksimum alat pencarian web terlampaui
- `query_too_long`: Kueri melebihi panjang maksimum
- `unavailable`: Terjadi kesalahan internal

</section>

## Langkah selanjutnya \{#next-steps}

- Untuk menjalankan beberapa alat dalam satu giliran, lihat [Penggunaan alat paralel](/docs/id/agents-and-tools/tool-use/parallel-tool-use).
- Untuk abstraksi SDK yang mengotomatiskan loop ini, lihat [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner).
- Untuk alur kerja penggunaan alat lengkap, lihat [Mendefinisikan alat](/docs/id/agents-and-tools/tool-use/define-tools).