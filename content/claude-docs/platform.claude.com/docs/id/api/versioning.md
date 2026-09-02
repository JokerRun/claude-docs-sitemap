---
source: platform
url: https://platform.claude.com/docs/id/api/versioning
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: faefe1ddf1375fc6cc309f5474e55198da5b566dd49e5aba52b33170951383f7
---

---
title: Versi
url: https://platform.claude.com/docs/id/api/versioning
description: "Saat membuat permintaan API, Anda harus mengirimkan header permintaan `anthropic-version`. Misalnya, `anthropic-version: 2023-06-01`. Jika Anda menggunakan [SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview), hal ini ditangani secara otomatis untuk Anda."
---

Untuk versi tertentu dengan Messages API, Anthropic mempertahankan:

* Parameter input yang sudah ada
* Parameter output yang sudah ada

Namun, Anthropic dapat melakukan hal-hal berikut:

* Menambahkan input opsional tambahan
* Menambahkan nilai tambahan pada output
* Mengubah kondisi untuk jenis error tertentu
* Menambahkan varian baru pada nilai output yang menyerupai enum (misalnya, jenis event streaming)

Secara umum, jika Anda menggunakan API sebagaimana didokumentasikan dalam referensi ini, Anthropic tidak akan merusak penggunaan Anda.

## Riwayat versi

Anthropic merekomendasikan penggunaan versi API terbaru bila memungkinkan. Versi sebelumnya dianggap usang (deprecated) dan mungkin tidak tersedia bagi pengguna baru.

* `2023-06-01`

  * Format baru untuk "server-sent events" (event yang dikirim server), atau SSE, pada [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming):

    * Completion bersifat inkremental. Misalnya, `" Hello"`, `" my"`, `" name"`, `" is"`, `" Claude." `alih-alih `" Hello"`, `" Hello my"`, `" Hello my name"`, `" Hello my name is"`, `" Hello my name is Claude."`.
    * Semua event adalah [named events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#named%5Fevents) (event bernama), bukan [data-only events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#data-only%5Fmessages) (event hanya-data).
    * Menghapus event `data: [DONE]` yang tidak diperlukan.

  * Menghapus nilai lama `exception` dan `truncated` dalam respons.

* `2023-01-01`: Rilis awal.
