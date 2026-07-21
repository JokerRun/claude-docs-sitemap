---
source: platform
url: https://platform.claude.com/docs/id/api/versioning
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 90090935f46c902d6e3e4a0e004a98ec6eb3e6e0183772a17dea8b16715d4dc0
---

# Versi

Saat membuat permintaan API, Anda harus mengirimkan header permintaan `anthropic-version`. Misalnya, `anthropic-version: 2023-06-01`. Jika Anda menggunakan [SDK klien](/docs/id/cli-sdks-libraries/overview), hal ini ditangani secara otomatis untuk Anda.

---

Untuk setiap versi tertentu dengan Messages API, Anthropic mempertahankan:

* Parameter input yang sudah ada
* Parameter output yang sudah ada

Namun, Anthropic dapat melakukan hal berikut:

* Menambahkan input opsional tambahan
* Menambahkan nilai tambahan ke output
* Mengubah kondisi untuk jenis error tertentu
* Menambahkan varian baru ke nilai output yang menyerupai enum (misalnya, jenis event streaming)

Secara umum, jika Anda menggunakan API sebagaimana didokumentasikan dalam referensi ini, Anthropic tidak akan merusak penggunaan Anda.

## Riwayat versi

Anthropic merekomendasikan penggunaan versi API terbaru bila memungkinkan. Versi sebelumnya dianggap usang (deprecated) dan mungkin tidak tersedia untuk pengguna baru.

* `2023-06-01`

  * Format baru untuk server-sent events (SSE) [streaming](/docs/id/build-with-claude/streaming):

    * Completion bersifat inkremental. Misalnya, `" Hello"`, `" my"`, `" name"`, `" is"`, `" Claude." `alih-alih `" Hello"`, `" Hello my"`, `" Hello my name"`, `" Hello my name is"`, `" Hello my name is Claude."`.
    * Semua event adalah [named events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#named%5Fevents), bukan [data-only events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#data-only%5Fmessages).
    * Menghapus event `data: [DONE]` yang tidak diperlukan.

  * Menghapus nilai `exception` dan `truncated` lama dalam respons.

* `2023-01-01`: Rilis awal.
