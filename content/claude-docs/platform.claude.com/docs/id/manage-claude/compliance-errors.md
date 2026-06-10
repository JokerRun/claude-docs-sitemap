---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-errors
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: bd3006505c0da88bf85e7053caf69f28d151f204cdf8b0c81e2c5bba26c2f2c6
---

# Menangani error Compliance API

Setiap pesan error Compliance API beserta penyebab dan solusinya, diorganisasi berdasarkan kode status HTTP.

---

<Note>
  Compliance API diaktifkan berdasarkan permintaan. Organisasi Claude Enterprise memiliki akses ke API lengkap; organisasi Claude Console hanya memiliki akses ke [Activity Feed](/docs/id/manage-claude/compliance-activity-feed). Lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

Halaman ini mencantumkan pesan respons yang dikembalikan oleh setiap endpoint Compliance API yang terdokumentasi, penyebabnya, dan solusinya.

Compliance API mengembalikan error dalam format error yang konsisten dengan [format error Anthropic](/docs/id/api/errors) lainnya: kode status non-2xx, header respons `request-id`, dan body JSON dengan objek `error` yang berisi `type` dan `message`. Sertakan nilai header `request-id` saat Anda mengeskalasi ke tim dukungan.

```json
{
  "error": {
    "type": "authentication_error",
    "message": "The API key provided is invalid or has been revoked."
  }
}
```

Lakukan pencocokan pada `error.type`, bukan pada string pesan. Pesan cukup stabil untuk disalin ke dalam runbook tetapi mungkin diubah redaksinya seiring waktu; nilai type adalah bagian dari kontrak API.

Tabel berikut memberi tahu Anda secara sekilas apakah perlu mencoba ulang. Setiap bagian setelahnya menampilkan body error secara verbatim dan solusinya.

| Status                                                  | Coba ulang?                 | Kapan                                                                 |
| ------------------------------------------------------- | --------------------------- | --------------------------------------------------------------------- |
| [400 Bad Request](#400-bad-request)                     | Tidak                       | Perbaiki permintaan dan kirim ulang.                                  |
| [401 Unauthorized](#401-unauthorized)                   | Tidak                       | Perbaiki atau rotasi kunci, lalu kirim ulang.                         |
| [403 Forbidden](#403-forbidden)                         | Tidak                       | Tambahkan scope yang hilang atau gunakan jenis kunci yang tepat, lalu kirim ulang. |
| [404 Not Found](#404-not-found)                         | Tidak                       | Sumber daya telah dihapus atau tidak pernah ada; hapus dari antrean Anda. |
| [409 Conflict](#409-conflict)                           | Tidak                       | Permintaan bertentangan dengan status sumber daya saat ini; selesaikan konflik (seperti melepaskan sumber daya turunan), lalu coba ulang. |
| [429 Too Many Requests](#429-too-many-requests)         | Ya, setelah `retry-after`   | Tunggu sejumlah detik dalam `retry-after`, lalu coba ulang; jangan majukan kursor Anda. |
| [500 Internal Server Error](#500-internal-server-error) | Tergantung pada `x-should-retry` | Periksa header respons `x-should-retry` sebelum mencoba ulang.   |
| [502, 503, 504, 529](#500-internal-server-error)        | Ya, dengan backoff          | Sementara; coba ulang dengan exponential backoff.                     |

## 400 Bad Request \{#400-bad-request}

Permintaan valid secara sintaksis tetapi berisi parameter yang ditolak server. Perbaiki parameter dan coba ulang.

### Format timestamp tidak valid \{#invalid-timestamp-format}

**Type:** `invalid_request_error`

```text
The `created_at.gte` parameter contains an invalid timestamp format. Timestamps must be provided in RFC 3339 format e.g., "2024-03-01T00:00:00Z". Got "2024-01-01".
```

**Penyebab:** Nilai `created_at.*` atau `updated_at.*` (`.gte`, `.gt`, `.lte`, `.lt`) tidak dapat di-parse sebagai datetime. Pesan menyebutkan parameter yang gagal dan menampilkan kembali nilai yang dikirim.

**Solusi:** Kirim timestamp RFC 3339 lengkap termasuk waktu dan zona waktu, misalnya, `2024-03-01T00:00:00Z` atau `2024-03-01T00:00:00+00:00`.

### Limit tidak valid \{#invalid-limit}

**Type:** `invalid_request_error`

```text
The limit parameter must be between 1 and 1000, inclusive. Got 1500.
```

**Penyebab:** Parameter kueri `limit` berada di luar rentang yang diterima. Batas yang disebutkan dalam pesan mencerminkan maksimum untuk endpoint spesifik yang dipanggil.

**Solusi:** Kirim `limit` dalam rentang yang diterima endpoint. Setiap endpoint list memiliki rentang `limit` sendiri; lihat batasan parameter pada halaman [referensi Compliance API](/docs/id/api/compliance) yang sesuai.

### ID paginasi tidak valid \{#invalid-pagination-id}

**Type:** `invalid_request_error`

```text
Invalid `after_id`. No activity found for `after_id` "activity_invalid123"
```

**Penyebab:** Kursor `after_id` atau `before_id` tidak dapat di-decode sebagai kursor opaque atau di-parse sebagai ID aktivitas.

**Solusi:** Perlakukan kursor paginasi sebagai string opaque. Selalu salin nilai `first_id` atau `last_id` yang dikembalikan oleh halaman sebelumnya; berhenti ketika `has_more` bernilai `false`. Jangan membuat kursor dari ID objek.

Endpoint direktori dan proyek (users, roles, role permissions, groups, group members, projects, dan project attachments) melakukan paginasi dengan token `page` opaque, bukan `after_id` dan `before_id`. Saran yang sama berlaku: teruskan nilai `next_page` dari respons sebelumnya tanpa perubahan, dan berhenti ketika `has_more` bernilai `false`. Token `page` yang salah format mengembalikan 400 `invalid_request_error` yang sama seperti `after_id` atau `before_id` yang salah format.

## 401 Unauthorized \{#401-unauthorized}

Header `x-api-key` tidak ada atau tidak cocok dengan kunci yang dikenal. Kunci yang valid dengan scope yang salah mengembalikan [403 Forbidden](#403-forbidden) sebagai gantinya.

### Kunci API tidak valid \{#invalid-api-key}

**Type:** `authentication_error`

```text
The API key provided is invalid or has been revoked.
```

**Penyebab:** Kunci dalam `x-api-key` tidak ada, telah dihapus, atau telah dinonaktifkan. Header `x-api-key` yang tidak ada atau kosong mengembalikan body yang sama, jadi periksa baik penyimpanan rahasia Anda maupun status pencabutan kunci.

**Solusi:** Konfirmasi nilai kunci, periksa bahwa kunci belum dihapus di claude.ai (Compliance Access Keys) atau Claude Console (Admin API keys), dan konfirmasi bahwa kunci diaktifkan. Lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access).

## 403 Forbidden \{#403-forbidden}

Kunci dalam `x-api-key` valid tetapi tidak membawa scope yang diperlukan endpoint. Pesan verbatim mencantumkan scope yang dibawa kunci (`Got:`) dan scope yang diperlukan endpoint (`Needed:`), sehingga Anda dapat mengonfirmasi apa yang dibawa kunci tanpa memeriksa ulang Claude Console atau claude.ai. Scope Compliance Access Key tidak dapat diubah setelah pembuatan, sehingga setiap solusi untuk scope yang tidak memadai mengarahkan Anda untuk membuat kunci baru alih-alih mengedit yang sudah ada.

### Scope tidak memadai: Activity Feed \{#insufficient-scope-activity-feed}

**Type:** `permission_error`

```text
Missing required scopes. Got: ['read:compliance_user_data'] Needed: ['read:compliance_activities']
```

**Penyebab:** Kunci tanpa `read:compliance_activities` digunakan untuk memanggil `GET /v1/compliance/activities`. Ada dua jalur umum menuju error ini:

- Compliance Access Key (`sk-ant-api01-...`) dibuat tanpa scope `read:compliance_activities`.
- Admin API key Claude Console (`sk-ant-admin01-...`) dibuat sebelum Compliance API diaktifkan untuk organisasi. Kunci yang dibuat sebelum pengaktifan tidak membawa scope tersebut; lihat [Setelah pengaktifan: organisasi Claude Console](/docs/id/manage-claude/compliance-api-access#after-enablement-claude-console-organizations).

**Solusi:** Scope Compliance Access Key tidak dapat diubah setelah pembuatan. Buat kunci baru yang menyertakan `read:compliance_activities`, atau gunakan Admin API key Claude Console. Lihat [Kunci mana yang Anda butuhkan?](/docs/id/manage-claude/compliance-api-access#which-key-do-you-need) untuk kondisi di mana Admin API key membawa scope ini.

### Scope tidak memadai: data organisasi \{#insufficient-scope-organization-data}

**Type:** `permission_error`

```text
Missing required scopes. Got: ['read:compliance_user_data'] Needed: ['read:compliance_org_data']
```

**Penyebab:** Kunci tanpa `read:compliance_org_data` digunakan untuk memanggil endpoint organizations, roles, atau groups. Ada dua jalur umum menuju error ini:

- Compliance Access Key (`sk-ant-api01-...`) dibuat tanpa scope `read:compliance_org_data`.
- Admin API key Claude Console (`sk-ant-admin01-...`) digunakan. Admin API key hanya membawa `read:compliance_activities` dan tidak dapat membaca metadata organisasi.

**Solusi:** [Buat Compliance Access Key baru](/docs/id/manage-claude/compliance-api-access#create-a-compliance-access-key) dengan `read:compliance_org_data` dipilih. Admin API key tidak dapat membaca metadata organisasi; Compliance Access Key diperlukan.

### Scope tidak memadai: data pengguna \{#insufficient-scope-user-data}

**Type:** `permission_error`

```text
Missing required scopes. Got: ['read:compliance_activities'] Needed: ['read:compliance_user_data']
```

**Penyebab:** Kunci tanpa `read:compliance_user_data` digunakan untuk memanggil endpoint chats, messages, files, projects, organization users, atau group-members. Ada dua jalur umum menuju error ini:

- Compliance Access Key (`sk-ant-api01-...`) dibuat tanpa scope `read:compliance_user_data`.
- Admin API key Claude Console (`sk-ant-admin01-...`) digunakan. Admin API key hanya membawa `read:compliance_activities` dan tidak dapat diberikan `read:compliance_user_data`, sehingga tidak dapat memanggil endpoint chat, file, project, project attachment, user, atau group-member.

**Solusi:** Gunakan [Compliance Access Key](/docs/id/manage-claude/compliance-api-access#create-a-compliance-access-key) yang dibuat di claude.ai dengan `read:compliance_user_data` dipilih. Jika permintaan memang seharusnya hanya untuk Activity Feed, arahkan Admin API key ke `GET /v1/compliance/activities` sebagai gantinya.

### Scope tidak memadai: delete \{#insufficient-scope-delete}

**Type:** `permission_error`

```text
Missing required scopes. Got: ['read:compliance_user_data'] Needed: ['delete:compliance_user_data']
```

**Penyebab:** Compliance Access Key tanpa `delete:compliance_user_data` digunakan untuk memanggil endpoint `DELETE` pada chats, files, atau projects.

**Solusi:** [Buat Compliance Access Key baru](/docs/id/manage-claude/compliance-api-access#create-a-compliance-access-key) dengan `delete:compliance_user_data` dipilih. Scope delete terpisah dari `read:compliance_user_data` sehingga kunci audit read-only tidak dapat menghapus konten.

## 404 Not Found \{#404-not-found}

Endpoint berhasil di-resolve tetapi ID sumber daya tidak ada atau telah dihapus. Penghapusan Compliance API bersifat langsung dan permanen, sehingga 404 pada ID yang sebelumnya dikenal biasanya berarti konten telah di-hard-delete melalui panggilan delete Compliance API atau dihapus oleh kebijakan retensi. String activity-type yang dikutip dalam setiap Solusi (misalnya, `claude_chat_created`) adalah nilai yang dapat Anda teruskan ke filter `activity_types[]` Activity Feed; lihat [Kueri aktivitas kepatuhan](/docs/id/api/compliance/activities/list) untuk setiap nilai yang didukung.

### Chat tidak ditemukan \{#chat-not-found}

**Type:** `not_found_error`

```text
Chat claude_chat_01H5CWunD7RpVJ5bHa8RCkja not found.
```

**Penyebab:** ID chat dalam path tidak cocok dengan chat yang dapat dibaca melalui Compliance API. Chat mungkin telah di-hard-delete melalui panggilan Compliance API sebelumnya atau dihapus oleh kebijakan retensi organisasi Anda, atau mungkin milik organisasi yang tidak dapat dibaca oleh kunci pemanggil. Chat yang di-soft-delete oleh pengguna di claude.ai tidak mengembalikan 404; chat tersebut tetap dapat dibaca dengan `deleted_at` terisi.

**Solusi:** Konfirmasi ID chat terhadap aktivitas `claude_chat_created` atau `claude_chat_viewed` terbaru. Jika aktivitas tersebut baru dan pembacaan masih gagal, chat telah di-hard-delete (melalui API ini atau oleh kedaluwarsa kebijakan retensi) atau milik organisasi di luar scope kunci Anda.

### File tidak ditemukan \{#file-not-found}

**Type:** `not_found_error`

```text
No file found with provided id, or it has already been deleted.
```

**Penyebab:** ID file tidak ada atau telah dihapus. Error ini berlaku untuk file yang dilampirkan ke chat (`claude_file_...`) maupun file proyek.

**Solusi:** Rekonsiliasi terhadap aktivitas `claude_file_uploaded` atau `claude_file_deleted` terbaru. Jika file telah dihapus, binary-nya sudah hilang; catatan aktivitas tetap ada di feed selama jendela retensi 6 tahun.

### Proyek tidak ditemukan \{#project-not-found}

**Type:** `not_found_error`

```text
No project is found with the provided id.
```

**Penyebab:** ID proyek tidak ada atau telah dihapus.

**Solusi:** Rekonsiliasi terhadap aktivitas `claude_project_created` atau `claude_project_deleted` terbaru. Activity Feed terus mengekspos peristiwa siklus hidup proyek bahkan setelah proyek itu sendiri hilang.

### Dokumen proyek tidak ditemukan \{#project-document-not-found}

**Type:** `not_found_error`

```text
No project document found with provided id, or it has already been deleted.
```

**Penyebab:** ID dokumen proyek tidak ada atau telah dihapus. Error ini berlaku untuk dokumen proyek teks (`claude_proj_doc_...`), bukan untuk file proyek.

**Solusi:** Gunakan `GET /v1/compliance/apps/projects/{project_id}/attachments` untuk mencantumkan lampiran saat ini. Jika dokumen tidak ada, dokumen tersebut telah dihapus; ambil melalui catatan aktivitas `claude_project_document_uploaded` jika Anda hanya membutuhkan metadata.

### Organisasi, role, atau grup tidak ditemukan \{#organization-role-or-group-not-found}

**Type:** `not_found_error`

```text
The "ce86b5f3-7c16-48b3-a9f3-e1d2c4b8a0f1" organization does not exist or the requester is not authorized to access it.
```

Endpoint organization, role, dan group mengembalikan 404 `not_found_error` dalam format error standar. Pesan organization menyebutkan `org_uuid`; pesan role dan group bersifat generik (`Role not found.`, `Group not found.`). Ini terjadi ketika ID path (`org_uuid`, `role_id`, atau `group_id`) tidak ada atau tidak lagi termasuk dalam pohon yang dapat dibaca oleh kunci pemanggil.

**Penyebab:** ID dalam path tidak cocok dengan catatan yang dapat dibaca melalui Compliance API. Role dan grup dapat dihapus, dan organisasi dapat dilepaskan dari pohon induk.

**Solusi:** Verifikasi ID terhadap endpoint list yang sesuai, dan rekonsiliasi terhadap aktivitas organisasi, role, atau grup terbaru di [Activity Feed](/docs/id/manage-claude/compliance-activity-feed).

## 409 Conflict \{#409-conflict}

Permintaan terbentuk dengan baik dan terotorisasi tetapi bertentangan dengan status sumber daya saat ini.

### Proyek memiliki chat yang terlampir \{#project-has-attached-chats}

**Type:** `conflict_error`

```text
The "claude_proj_01KGp4eZNug9ri4kE35RSppq" project cannot be deleted as it has chats attached to it. Delete or detach all chats, and try deleting the project again.
```

**Penyebab:** `DELETE /v1/compliance/apps/projects/{project_id}` dipanggil pada proyek yang masih memiliki chat terlampir.

**Solusi:** Cantumkan chat proyek dengan `GET /v1/compliance/apps/chats?user_ids[]={user_id}&project_ids[]={project_id}` (endpoint daftar chat memerlukan setidaknya satu nilai `user_ids[]`; enumerasi ID melalui [Mencantumkan pengguna organisasi](/docs/id/manage-claude/compliance-org-data#list-organization-users)), hapus masing-masing dengan `DELETE /v1/compliance/apps/chats/{claude_chat_id}`, lalu coba ulang penghapusan proyek.

## 429 Too Many Requests \{#429-too-many-requests}

Permintaan ke Compliance API dibatasi hingga **600 permintaan per menit per [organisasi induk](/docs/id/manage-claude/compliance-api#how-the-compliance-api-works)**. Batas ini adalah satu anggaran yang dibagi di seluruh kunci di bawah induk (Compliance Access Key dan Admin API key dari semua organisasi yang tertaut) dan di seluruh endpoint `/v1/compliance/*`. Hubungi perwakilan Anthropic Anda jika integrasi Anda membutuhkan batas yang lebih tinggi.

Setelah kunci API Anda terautentikasi, setiap respons Compliance API menyertakan [header respons rate-limit](/docs/id/api/rate-limits#response-headers) standar sehingga klien Anda dapat melakukan throttling secara proaktif alih-alih menunggu 429:

- `anthropic-ratelimit-requests-limit` adalah anggaran permintaan per menit organisasi induk Anda.
- `anthropic-ratelimit-requests-remaining` adalah anggaran yang tersisa dalam jendela saat ini.
- `anthropic-ratelimit-requests-reset` adalah timestamp RFC 3339 saat jendela di-reset dan anggaran penuh dipulihkan.

Respons 429 juga membawa header `retry-after` dengan jumlah detik untuk menunggu sebelum mengirim permintaan berikutnya. Nilai ini mungkin menyertakan margin keamanan kecil di luar `anthropic-ratelimit-requests-reset`; patuhi `retry-after`.

```http
HTTP/1.1 429 Too Many Requests
date: Tue, 21 Apr 2026 14:38:02 GMT
retry-after: 25
anthropic-ratelimit-requests-limit: 600
anthropic-ratelimit-requests-remaining: 0
anthropic-ratelimit-requests-reset: 2026-04-21T14:38:25Z
```

```json
{
  "error": {
    "type": "rate_limit_error",
    "message": "Compliance API rate limit of 600 requests per minute per parent organization has been exceeded. Retry after the time indicated by the retry-after header. Quote the request-id response header when contacting Anthropic support."
  }
}
```

**Penyebab:** Organisasi induk Anda mengirim lebih dari 600 permintaan ke `/v1/compliance/*` dalam jendela 1 menit, di seluruh kunci dan organisasi tertautnya.

**Solusi:** Tunggu sejumlah detik dalam header `retry-after`, lalu coba ulang. Jika header tidak ada (misalnya, dihapus oleh perantara), gunakan exponential backoff sebagai fallback (mulai dari 1 detik, gandakan hingga 60 detik). Jangan majukan kursor paginasi Anda pada 429: permintaan yang gagal tidak mengembalikan data, sehingga kursor dari halaman terakhir yang berhasil masih benar.

Permintaan yang gagal autentikasi (kunci yang tidak ada atau tidak dikenali, atau kunci Claude API alih-alih Compliance Access Key atau Admin API key) ditolak sebelum rate limiter dan tidak mengonsumsi kuota. Kunci valid yang tidak memiliki scope yang diperlukan endpoint mengonsumsi satu unit kuota sebelum 403 dikembalikan.

Jika Anda melakukan polling [Activity Feed](/docs/id/manage-claude/compliance-activity-feed) secara terjadwal, anggarkan laju permintaan agregat Anda (di seluruh kunci, organisasi tertaut, dan worker konkuren) di bawah batas organisasi induk. Pantau `anthropic-ratelimit-requests-remaining` untuk memperlambat sebelum Anda mencapainya. Lihat [Merancang integrasi kepatuhan Anda](/docs/id/manage-claude/compliance-integration-patterns#choose-a-feed-consumption-pattern) untuk memilih antara window-polling dan ingesti berbasis kursor.

## 500 Internal Server Error \{#500-internal-server-error}

500 dari Compliance API membawa header respons `x-should-retry: false` ketika kegagalan bersifat deterministik. SDK Anthropic mematuhi header ini secara otomatis. Jika Anda menggunakan library retry HTTP generik yang mencoba ulang pada setiap 5xx, tekan percobaan ulang ketika `x-should-retry` bernilai `false`; mencoba ulang error ini akan gagal secara identik pada setiap percobaan.

500 tanpa header `x-should-retry: false` bersifat sementara: coba ulang dengan exponential backoff (mulai dari 1 detik, gandakan hingga 60 detik). Hal yang sama berlaku untuk respons 502, 503, 504, dan 529. Lihat [Error](/docs/id/api/errors) untuk semantik retry di seluruh platform.

Untuk insiden di seluruh layanan, periksa [status.anthropic.com](https://status.anthropic.com).

### Ukuran respons maksimum terlampaui \{#maximum-response-size-exceeded}

**Type:** `api_error`

```text
Response exceeds maximum of 1,000 organizations. Contact support for assistance with larger organization lists.
```

**Penyebab:** Endpoint list tanpa paginasi (terutama `GET /v1/compliance/organizations`) akan mengembalikan lebih dari batas kerasnya yaitu 1.000 catatan.

**Solusi:** Endpoint organizations mengembalikan seluruh pohon dalam satu panggilan, hingga 1.000 organisasi tertaut. Jika pohon Anda melebihi 1.000, hubungi dukungan Anthropic untuk bantuan dengan daftar organisasi yang lebih besar. Jika Anda melakukan polling endpoint ini untuk melacak perubahan keanggotaan organisasi, pencantuman ulang secara berkala tetap menjadi pendekatan paling andal setelah batas tersebut diatasi; pendekatan ini menangkap penambahan dan penghapusan terlepas dari sisi mana dari hubungan induk-anak yang memulainya. [Activity Feed](/docs/id/manage-claude/compliance-activity-feed) juga menampilkan peristiwa keanggotaan melalui tipe aktivitas `org_deletion_requested`, `org_deleted_via_bulk`, `org_parent_join_proposal_created`, dan `org_join_proposal_decided`, yang dapat Anda gunakan untuk memicu pencantuman ulang segera alih-alih menunggu interval polling berikutnya.

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card title="FAQ Compliance API" href="/docs/id/manage-claude/compliance-faq">
    Pertanyaan umum tentang akses, scope, retensi, dan integrasi.
  </Card>
  <Card title="Error" href="/docs/id/api/errors">
    Katalog error di seluruh platform dan semantik retry.
  </Card>
</CardGroup>