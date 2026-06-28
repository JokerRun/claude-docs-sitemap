---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 893f8a4fc40c06963a84c23e65eb515f00b04533345ecbe7f9fd909b69a89be7
---

# Menangani panggilan alat

Mengurai blok tool_use, memformat respons tool_result, dan menangani kesalahan dengan is_error.

---

Halaman ini membahas siklus hidup panggilan alat: membaca blok `tool_use` dari respons Claude, memformat blok `tool_result` dalam balasan Anda, dan memberi sinyal kesalahan. Untuk abstraksi SDK yang menangani hal ini secara otomatis, lihat [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner).

<Note>
  **Lebih sederhana dengan Tool Runner**: Penanganan alat secara manual yang dijelaskan di halaman ini dikelola secara otomatis oleh [Tool Runner](/docs/id/agents-and-tools/tool-use/tool-runner). Gunakan halaman ini ketika Anda memerlukan kontrol khusus atas eksekusi alat.
</Note>

Respons Claude berbeda tergantung pada apakah ia menggunakan [alat klien atau server](/docs/id/agents-and-tools/tool-use/overview#how-tool-use-works).

## Menangani hasil dari alat klien

Respons akan memiliki `stop_reason` berupa `tool_use` dan satu atau lebih blok konten `tool_use` yang mencakup:

* `id`: Pengidentifikasi unik untuk blok penggunaan alat tertentu ini. Ini akan digunakan untuk mencocokkan hasil alat nantinya.
* `name`: Nama alat yang sedang digunakan.
* `input`: Objek yang berisi input yang diteruskan ke alat, sesuai dengan `input_schema` alat tersebut.

<Accordion title="Contoh respons API dengan blok konten `tool_use`">
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
</Accordion>

Ketika Anda menerima respons penggunaan alat untuk alat klien, Anda harus:

1. Mengekstrak `name`, `id`, dan `input` dari blok `tool_use`.

2. Menjalankan alat yang sebenarnya di basis kode Anda yang sesuai dengan nama alat tersebut, dengan meneruskan `input` alat.

3. Melanjutkan percakapan dengan mengirim pesan baru dengan `role` berupa `user`, dan blok `content` yang berisi tipe `tool_result` serta informasi berikut:

   * `tool_use_id`: `id` dari permintaan penggunaan alat yang hasilnya ini.
   * `content` (opsional): Hasil dari alat, sebagai string (misalnya, `"content": "15 degrees"`), daftar blok konten bersarang (misalnya, `"content": [{"type": "text", "text": "15 degrees"}]`), atau daftar blok dokumen (misalnya, `"content": [{"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": "15 degrees"}}]`). Blok konten ini dapat menggunakan tipe `text`, `image`, `document`, atau [`search_result`](/docs/id/build-with-claude/search-results).
   * `is_error` (opsional): Atur ke `true` jika eksekusi alat menghasilkan kesalahan.

<Note>
  **Persyaratan pemformatan penting**:

  * Blok hasil alat harus langsung mengikuti blok penggunaan alat yang sesuai dalam riwayat pesan. Anda tidak dapat menyertakan pesan apa pun di antara pesan penggunaan alat dari asisten dan pesan hasil alat dari pengguna.
  * Dalam pesan pengguna yang berisi hasil alat, blok tool\_result harus berada PERTAMA dalam array konten. Teks apa pun harus berada SETELAH semua hasil alat.

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

  Jika Anda menerima kesalahan seperti "tool\_use ids were found without tool\_result blocks immediately after", periksa apakah hasil alat Anda diformat dengan benar.
</Note>

<Warning>
  Hasil alat sering kali membawa konten dari sumber di luar kendali Anda: halaman web, email masuk, unggahan pengguna, API pihak ketiga. Perlakukan konten tersebut sebagai tidak tepercaya: penyerang yang dapat memengaruhinya mungkin menyematkan instruksi yang mencoba mengalihkan Claude (injeksi prompt tidak langsung). Simpan konten yang tidak tepercaya di dalam blok `tool_result` alih-alih prompt `system` atau blok `text` pengguna biasa, dan lihat [Memitigasi jailbreak dan injeksi prompt](/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks#indirect-prompt-injection) untuk pengerasan lebih lanjut.
</Warning>

<AccordionGroup>
  <Accordion title="Contoh hasil alat yang berhasil">
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
  </Accordion>

  <Accordion title="Contoh hasil alat dengan gambar">
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
  </Accordion>

  <Accordion title="Contoh hasil alat kosong">
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
  </Accordion>

  <Accordion title="Contoh hasil alat dengan dokumen">
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
  </Accordion>
</AccordionGroup>

Setelah menerima hasil alat, Claude akan menggunakan informasi tersebut untuk melanjutkan menghasilkan respons terhadap prompt pengguna asli.

## Menangani hasil dari alat server

Claude mengeksekusi alat secara internal dan menggabungkan hasilnya langsung ke dalam responsnya tanpa memerlukan interaksi pengguna tambahan.

<Tip>
  **Perbedaan dari API lain**

  Tidak seperti API yang memisahkan penggunaan alat atau menggunakan peran khusus seperti `tool` atau `function`, API Claude mengintegrasikan alat langsung ke dalam struktur pesan `user` dan `assistant`.

  Pesan berisi array blok `text`, `image`, `tool_use`, dan `tool_result`. Pesan `user` mencakup konten klien dan `tool_result`, sedangkan pesan `assistant` berisi konten yang dihasilkan AI dan `tool_use`.
</Tip>

## Menangani kesalahan dengan is\_error

Ada beberapa jenis kesalahan berbeda yang dapat terjadi saat menggunakan alat dengan Claude:

<AccordionGroup>
  <Accordion title="Kesalahan eksekusi alat">
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
  </Accordion>

  <Accordion title="Nama alat tidak valid">
    Jika upaya Claude menggunakan alat tidak valid (misalnya, parameter yang diperlukan tidak ada), biasanya itu berarti tidak ada cukup informasi bagi Claude untuk menggunakan alat dengan benar. Langkah terbaik Anda selama pengembangan adalah mencoba permintaan lagi dengan nilai `description` yang lebih detail dalam definisi alat Anda.

    Namun, Anda juga dapat melanjutkan percakapan dengan `tool_result` yang menunjukkan kesalahan, dan Claude akan mencoba menggunakan alat lagi dengan informasi yang hilang diisi:

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

    Jika permintaan alat tidak valid atau parameter tidak ada, Claude akan mencoba ulang 2-3 kali dengan koreksi sebelum meminta maaf kepada pengguna.

    <Tip>
      Untuk menghilangkan panggilan alat yang tidak valid sepenuhnya, gunakan [penggunaan alat ketat](/docs/id/agents-and-tools/tool-use/strict-tool-use) dengan `strict: true` pada definisi alat Anda. Ini menjamin bahwa input alat akan selalu cocok dengan skema Anda secara persis, mencegah parameter yang hilang dan ketidakcocokan tipe.
    </Tip>
  </Accordion>

  <Accordion title="Kesalahan alat server">
    Ketika alat server mengalami kesalahan (misalnya, masalah jaringan dengan Web Search), Claude akan menangani kesalahan ini secara transparan dan berupaya memberikan respons atau penjelasan alternatif kepada pengguna. Tidak seperti alat klien, Anda tidak perlu menangani hasil `is_error` untuk alat server.

    Untuk pencarian web secara khusus, kode kesalahan yang mungkin meliputi:

    * `too_many_requests`: Batas laju terlampaui
    * `invalid_input`: Parameter kueri pencarian tidak valid
    * `max_uses_exceeded`: Penggunaan maksimum alat pencarian web terlampaui
    * `query_too_long`: Kueri melebihi panjang maksimum
    * `unavailable`: Terjadi kesalahan internal
  </Accordion>
</AccordionGroup>

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Penggunaan alat paralel" icon="grid" href="/docs/id/agents-and-tools/tool-use/parallel-tool-use">
    Tangani respons di mana Claude memanggil beberapa alat dalam satu giliran.
  </Card>

  <Card title="Tool Runner (SDK)" icon="wrench" href="/docs/id/agents-and-tools/tool-use/tool-runner">
    Biarkan SDK mengelola loop `tool_use`, pemformatan hasil, dan percobaan ulang untuk Anda.
  </Card>

  <Card title="Mendefinisikan alat" icon="hammer" href="/docs/id/agents-and-tools/tool-use/define-tools">
    Tulis skema dan deskripsi yang mengarahkan Claude ke alat yang tepat.
  </Card>
</CardGroup>
