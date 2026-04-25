---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls
fetched_at: 2026-04-25T03:09:48.142425Z
sha256: e52b7f75d5fe1b09a0abb7698bcab86ef9719635233097d1b9aa8672bcc81fbb
---

# Menangani pemanggilan alat

Mengurai blok tool_use, memformat respons tool_result, dan menangani kesalahan dengan is_error.

---

Halaman ini mencakup siklus hidup pemanggilan alat: membaca blok `tool_use` dari respons Claude, memformat blok `tool_result` dalam balasan Anda, dan menandakan kesalahan. Untuk abstraksi SDK yang menangani ini secara otomatis, lihat [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner).

<Note>
**Lebih Sederhana dengan Tool Runner**: Penanganan alat manual yang dijelaskan di halaman ini dikelola secara otomatis oleh [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner). Gunakan halaman ini ketika Anda memerlukan kontrol khusus atas eksekusi alat.
</Note>

Respons Claude berbeda tergantung pada apakah menggunakan alat klien atau server.

## Menangani hasil dari alat klien

Respons akan memiliki `stop_reason` dari `tool_use` dan satu atau lebih blok konten `tool_use` yang mencakup:

- `id`: Pengenal unik untuk blok penggunaan alat tertentu ini. Ini akan digunakan untuk mencocokkan hasil alat nanti.
- `name`: Nama alat yang digunakan.
- `input`: Objek yang berisi input yang diteruskan ke alat, sesuai dengan `input_schema` alat.

<section title="Contoh respons API dengan blok konten `tool_use`">

```json JSON
{
  "id": "msg_01Aq9w938a90dw8q",
  "model": "claude-opus-4-7",
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

1. Ekstrak `name`, `id`, dan `input` dari blok `tool_use`.
2. Jalankan alat sebenarnya di basis kode Anda yang sesuai dengan nama alat tersebut, meneruskan `input` alat.
3. Lanjutkan percakapan dengan mengirim pesan baru dengan `role` dari `user`, dan blok `content` yang berisi tipe `tool_result` dan informasi berikut:
   - `tool_use_id`: `id` dari permintaan penggunaan alat ini adalah hasil untuk.
   - `content`: Hasil alat, sebagai string (misalnya, `"content": "15 degrees"`), daftar blok konten bersarang (misalnya, `"content": [{"type": "text", "text": "15 degrees"}]`), atau daftar blok dokumen (misalnya, `"content": [{"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": "15 degrees"}}]`). Blok konten ini dapat menggunakan tipe `text`, `image`, atau `document`.
   - `is_error` (opsional): Atur ke `true` jika eksekusi alat menghasilkan kesalahan.

<Note>
**Persyaratan pemformatan penting**:
- Blok hasil alat harus segera mengikuti blok penggunaan alat yang sesuai dalam riwayat pesan. Anda tidak dapat menyertakan pesan apa pun antara pesan penggunaan alat asisten dan pesan hasil alat pengguna.
- Dalam pesan pengguna yang berisi hasil alat, blok tool_result harus datang PERTAMA dalam array konten. Teks apa pun harus datang SETELAH semua hasil alat.

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

Jika Anda menerima kesalahan seperti "tool_use ids were found without tool_result blocks immediately after", periksa bahwa hasil alat Anda diformat dengan benar.
</Note>

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

Setelah menerima hasil alat, Claude akan menggunakan informasi tersebut untuk terus menghasilkan respons terhadap prompt pengguna asli.

## Menangani hasil dari alat server

Claude menjalankan alat secara internal dan menggabungkan hasilnya langsung ke dalam responsnya tanpa memerlukan interaksi pengguna tambahan.

<Tip>
  **Perbedaan dari API lain**

Tidak seperti API yang memisahkan penggunaan alat atau menggunakan peran khusus seperti `tool` atau `function`, API Claude mengintegrasikan alat langsung ke dalam struktur pesan `user` dan `assistant`.

Pesan berisi array blok `text`, `image`, `tool_use`, dan `tool_result`. Pesan `user` mencakup konten klien dan `tool_result`, sementara pesan `assistant` berisi konten yang dihasilkan AI dan `tool_use`.

</Tip>

## Menangani kesalahan dengan is_error

Ada beberapa jenis kesalahan berbeda yang dapat terjadi saat menggunakan alat dengan Claude:

<section title="Kesalahan eksekusi alat">

Jika alat itu sendiri melempar kesalahan selama eksekusi (misalnya, kesalahan jaringan saat mengambil data cuaca), Anda dapat mengembalikan pesan kesalahan dalam `content` bersama dengan `"is_error": true`:

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

Claude kemudian akan menggabungkan kesalahan ini ke dalam responsnya kepada pengguna. Misalnya: "I'm sorry, I was unable to retrieve the current weather because the weather service API is not available. Please try again later."

<Tip>
Tulis pesan kesalahan yang instruktif. Alih-alih kesalahan generik seperti `"failed"`, sertakan apa yang salah dan apa yang harus dicoba Claude selanjutnya, misalnya, `"Rate limit exceeded. Retry after 60 seconds."` Ini memberi Claude konteks yang diperlukan untuk pulih atau beradaptasi tanpa menebak.
</Tip>

</section>
<section title="Nama alat tidak valid">

Jika upaya Claude menggunakan alat tidak valid (misalnya, parameter yang diperlukan hilang), biasanya berarti tidak ada cukup informasi bagi Claude untuk menggunakan alat dengan benar. Pilihan terbaik Anda selama pengembangan adalah mencoba permintaan lagi dengan nilai `description` yang lebih terperinci dalam definisi alat Anda.

Namun, Anda juga dapat melanjutkan percakapan ke depan dengan `tool_result` yang menunjukkan kesalahan, dan Claude akan mencoba menggunakan alat lagi dengan informasi yang hilang diisi:

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

Jika permintaan alat tidak valid atau parameter hilang, Claude akan mencoba ulang 2-3 kali dengan koreksi sebelum meminta maaf kepada pengguna.

<Tip>
Untuk menghilangkan pemanggilan alat yang tidak valid sepenuhnya, gunakan [strict tool use](/docs/id/agents-and-tools/tool-use/strict-tool-use) dengan `strict: true` pada definisi alat Anda. Ini menjamin bahwa input alat akan selalu cocok dengan skema Anda dengan tepat, mencegah parameter yang hilang dan ketidaksesuaian tipe.
</Tip>

</section>
<section title="Kesalahan alat server">

Ketika alat server mengalami kesalahan (misalnya, masalah jaringan dengan Web Search), Claude akan menangani kesalahan ini secara transparan dan mencoba memberikan respons alternatif atau penjelasan kepada pengguna. Tidak seperti alat klien, Anda tidak perlu menangani hasil `is_error` untuk alat server.

Untuk pencarian web khususnya, kode kesalahan yang mungkin termasuk:
- `too_many_requests`: Batas laju terlampaui
- `invalid_input`: Parameter kueri pencarian tidak valid
- `max_uses_exceeded`: Penggunaan alat pencarian web maksimum terlampaui
- `query_too_long`: Kueri melebihi panjang maksimum
- `unavailable`: Kesalahan internal terjadi

</section>

## Langkah berikutnya

- Untuk menjalankan beberapa alat dalam satu putaran, lihat [Parallel tool use](/docs/id/agents-and-tools/tool-use/parallel-tool-use).
- Untuk abstraksi SDK yang mengotomatisasi loop ini, lihat [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner).
- Untuk alur kerja tool-use lengkap, lihat [Define tools](/docs/id/agents-and-tools/tool-use/define-tools).