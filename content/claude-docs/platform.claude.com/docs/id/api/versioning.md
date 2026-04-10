---
source: platform
url: https://platform.claude.com/docs/id/api/versioning
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 4e86dcd0963abd9f31ae7614d6bc3cd4e0ef5fb7cc3946ed2d92624a8ac557fe
---

# Versi

Saat membuat permintaan API, Anda harus mengirimkan header permintaan `anthropic-version`. Misalnya, `anthropic-version: 2023-06-01`. Jika Anda menggunakan [SDK klien](/docs/id/api/client-sdks) kami, ini ditangani secara otomatis untuk Anda.

---

Untuk versi apa pun dengan Messages API, kami akan mempertahankan:

* Parameter input yang ada
* Parameter output yang ada

Namun, kami dapat melakukan hal berikut:

* Menambahkan input opsional tambahan
* Menambahkan nilai tambahan ke output
* Mengubah kondisi untuk jenis kesalahan tertentu
* Menambahkan varian baru ke nilai output seperti enum (misalnya, jenis acara streaming)

Secara umum, jika Anda menggunakan API seperti yang didokumentasikan dalam referensi ini, kami tidak akan merusak penggunaan Anda.

## Riwayat versi

Kami selalu merekomendasikan menggunakan versi API terbaru kapan pun memungkinkan. Versi sebelumnya dianggap usang dan mungkin tidak tersedia untuk pengguna baru.

* `2023-06-01`
   * Format baru untuk acara server-sent (SSE) [streaming](/docs/id/build-with-claude/streaming):
         * Penyelesaian bersifat inkremental. Misalnya, `" Hello"`, `" my"`, `" name"`, `" is"`, `" Claude." ` bukan `" Hello"`, `" Hello my"`, `" Hello my name"`, `" Hello my name is"`, `" Hello my name is Claude."`.
         * Semua acara adalah [acara bernama](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#named%5Fevents), bukan [acara hanya data](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#data-only%5Fmessages).
         * Menghapus acara `data: [DONE]` yang tidak perlu.
   * Menghapus nilai `exception` dan `truncated` warisan dalam respons.
* `2023-01-01`: Rilis awal.