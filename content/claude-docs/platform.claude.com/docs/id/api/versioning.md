---
source: platform
url: https://platform.claude.com/docs/id/api/versioning
fetched_at: 2026-10-22T02:21:21.745661Z
sha256: 1df0082e0331eedad966cc7b6523c6ca79145d358ac93b9c1e00163ce5cc576a
---

---
title: Versi
url: https://platform.claude.com/docs/id/api/versioning
description: "Saat membuat permintaan API, Anda harus mengirimkan header permintaan `anthropic-version`. Misalnya, `anthropic-version: 2026-10-21`. Jika Anda menggunakan [SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview), hal ini ditangani secara otomatis untuk Anda."
---

Untuk versi API tertentu, Anthropic mempertahankan:

* Parameter input yang sudah ada
* Parameter output yang sudah ada

Namun, Anthropic dapat melakukan hal-hal berikut:

* Menambahkan input opsional tambahan
* Menambahkan nilai tambahan pada output
* Mengubah kondisi untuk jenis error tertentu
* Menambahkan varian baru pada nilai output yang menyerupai enum (misalnya, jenis event streaming)

Secara umum, jika Anda menggunakan API sebagaimana didokumentasikan dalam referensi ini, Anthropic tidak akan merusak penggunaan Anda.

## Riwayat versi

Anthropic merekomendasikan penggunaan versi API terbaru bila memungkinkan.

* `2026-10-21`

  * [Migrasi ke versi API 2026-10-21](https://platform.claude.com/docs/id/api/migration-2026-10-21) menunjukkan cara melakukan upgrade.

  * Tersedia di Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), dan [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai). Di [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), versi ini tersedia untuk model Claude 4.7 dan yang lebih baru. Untuk model lain di Bedrock, lihat [panduan migrasi](https://platform.claude.com/docs/id/api/migration-2026-10-21#upgrade).

  * Messages API:

    * Permintaan yang menempatkan blok `document` secara langsung dalam pesan `assistant` akan mengembalikan error 400.
    * Mengirimkan blok `text` dengan array `citations` yang tidak kosong dalam pesan `user`, baik secara langsung maupun di dalam blok `search_result`, akan mengembalikan error 400.
    * Parameter permintaan `temperature`, `top_p`, dan `top_k` dihapus. Permintaan yang mengirimkan salah satu dari parameter tersebut akan mengembalikan error 400 pada setiap model.

  * Admin API:

    * [Grup RBAC](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/list) tidak lagi mengembalikan `roles`. Gunakan `role_ids` sebagai gantinya.
    * [Anggota grup RBAC](https://platform.claude.com/docs/id/api/beta/organization/rbac_groups/members/list), serta respons saat menghapus salah satunya, tidak lagi mengembalikan `group_id`. Gunakan `rbac_group_id` sebagai gantinya.
    * [Peran RBAC](https://platform.claude.com/docs/id/api/beta/organization/rbac_roles/list) tidak lagi mengembalikan `name`. Gunakan `display_name` sebagai gantinya.
    * Entri "rate limit" (batas laju) [organisasi](https://platform.claude.com/docs/id/api/organization/rate_limits/list) dan [workspace](https://platform.claude.com/docs/id/api/organization/workspaces/rate_limits/list) tidak lagi mengembalikan `group_type`. Gunakan `group.type` sebagai gantinya.
    * [Kunci API](https://platform.claude.com/docs/id/api/organization/api_keys/list) tidak lagi mengembalikan `workspace_id`. Gunakan `scope.workspace_id` sebagai gantinya, yang memberikan ID sebenarnya dari workspace bahkan untuk Default Workspace (kunci untuk semua workspace tidak memiliki `workspace_id` dalam `scope`).

  * Claude Enterprise Analytics API:

    * Laporan [penggunaan](https://platform.claude.com/docs/id/api/beta/organization/analytics/user_usage_report/list) dan [biaya](https://platform.claude.com/docs/id/api/beta/organization/analytics/user_cost_report/list) per pengguna tidak lagi memiliki `actor.email`. Gunakan `actor.email_address` sebagai gantinya.
    * Respons [ringkasan aktivitas](https://platform.claude.com/docs/id/api/beta/organization/analytics/summaries/list) tidak lagi memiliki `summaries`. Gunakan `data` sebagai gantinya.

- `2023-06-01`

  * Format baru untuk "server-sent events" (event yang dikirim server), atau SSE, pada [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming):

    * Completion bersifat inkremental. Misalnya, `" Hello"`, `" my"`, `" name"`, `" is"`, `" Claude." `alih-alih `" Hello"`, `" Hello my"`, `" Hello my name"`, `" Hello my name is"`, `" Hello my name is Claude."`.
    * Semua event adalah [named events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#named%5Fevents) (event bernama), bukan [data-only events](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents#data-only%5Fmessages) (event hanya-data).
    * Menghapus event `data: [DONE]` yang tidak diperlukan.

  * Menghapus nilai lama `exception` dan `truncated` dalam respons.

- `2023-01-01`: Rilis awal.
