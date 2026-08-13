---
source: platform
url: https://platform.claude.com/docs/id/api/versioning
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: c0b5d00f83aeadd3fd4a895e148539202bc00a1fceb03151b6aca6083113f158
---

---
title: Versi
url: https://platform.claude.com/docs/id/api/versioning
description: "Saat membuat permintaan API, Anda harus mengirimkan header permintaan `anthropic-version`. Misalnya, `anthropic-version: 2023-06-01`. Jika Anda menggunakan [SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview), hal ini ditangani secara otomatis untuk Anda."
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

  * Format baru untuk server-sent events (SSE) [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming):

    * Completion bersifat inkremental. Misalnya, `" Hello"`, `" my"`, `" name"`, `" is"`, `" Claude." `alih-alih `" Hello"`, `" Hello my"`, `" Hello my name"`, `" Hello my name is"`, `" Hello my name is Claude."`.
    * Semua event adalah [named events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#named%5Fevents), bukan [data-only events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#data-only%5Fmessages).
    * Menghapus event `data: [DONE]` yang tidak diperlukan.

  * Menghapus nilai `exception` dan `truncated` lama dalam respons.

* `2023-01-01`: Rilis awal.
