---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-errors
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: a74efc4c29acce8a8b84c8828a7ba1339e7945c591599c269eb3d83998ada34b
---

---
title: Menangani kesalahan Compliance API
url: https://platform.claude.com/docs/id/manage-claude/compliance-errors
description: Setiap pesan kesalahan Compliance API beserta penyebab dan perbaikannya, diorganisir berdasarkan kode status HTTP.
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

Halaman ini mencantumkan pesan respons yang dikembalikan oleh setiap endpoint Compliance API yang terdokumentasi, penyebabnya, dan cara memperbaikinya.

Compliance API mengembalikan kesalahan dalam [format kesalahan Anthropic](https://platform.claude.com/docs/id/api/errors) standar: kode status non-2xx, header respons `request-id`, dan body JSON dengan objek `error` yang berisi `type` dan `message`. Sertakan nilai header `request-id` saat Anda mengeskalasi ke dukungan.

```json
{
  "error": {
    "type": "authentication_error",
    "message": "The API key provided is invalid or has been revoked."
  }
}
```

Cocokkan berdasarkan `error.type`, bukan berdasarkan string pesan. Pesan cukup stabil untuk disalin ke dalam runbook tetapi mungkin diubah redaksinya seiring waktu; nilai type adalah bagian dari kontrak API. Endpoint sesi lokal memiliki beberapa pengecualian terdokumentasi di mana respons yang memiliki type yang sama dibedakan berdasarkan pesannya; masing-masing disebutkan di bagian yang relevan.

Tabel berikut memberi tahu Anda secara sekilas apakah perlu mencoba ulang. Setiap bagian berikutnya menampilkan body kesalahan secara verbatim dan perbaikannya.

| Status                                                                                                                     | Coba ulang?                      | Kapan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request)                     | Tidak                            | Perbaiki permintaan dan kirim ulang.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [401 Unauthorized](https://platform.claude.com/docs/id/manage-claude/compliance-errors#401-unauthorized)                   | Tidak                            | Perbaiki atau rotasi kunci, lalu kirim ulang.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden)                         | Tidak                            | Tambahkan scope yang hilang atau gunakan jenis kunci yang tepat, lalu kirim ulang.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found)                         | Biasanya tidak                   | Sumber daya telah dihapus atau tidak pernah ada; hapus dari antrean Anda. Pengecualian: sesi remote yang masih dalam status `pending` mengembalikan 404 pada endpoint messages-nya hingga sesi dimulai; lihat [Sesi remote tidak ditemukan](https://platform.claude.com/docs/id/manage-claude/compliance-errors#remote-session-not-found). Pada endpoint sesi lokal, pesan `Local sessions are not available.` (dikembalikan pada setiap panggilan, termasuk list) berarti endpoint tersebut saat ini tidak tersedia untuk organisasi induk Anda, bukan berarti sesi telah hilang; simpan ID yang diantrekan dan lihat [Sesi lokal tidak ditemukan](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-session-not-found). |
| [409 Conflict](https://platform.claude.com/docs/id/manage-claude/compliance-errors#409-conflict)                           | Tidak                            | Permintaan bertentangan dengan status sumber daya saat ini; selesaikan konflik (seperti melepaskan sumber daya anak), lalu coba ulang.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [429 Too Many Requests](https://platform.claude.com/docs/id/manage-claude/compliance-errors#429-too-many-requests)         | Ya, setelah `retry-after`        | Tunggu sejumlah detik dalam `retry-after`, lalu coba ulang; jangan majukan kursor Anda.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [500 Internal Server Error](https://platform.claude.com/docs/id/manage-claude/compliance-errors#500-internal-server-error) | Tergantung pada `x-should-retry` | Periksa header respons `x-should-retry` sebelum mencoba ulang.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| [502, 503, 504, 529](https://platform.claude.com/docs/id/manage-claude/compliance-errors#500-internal-server-error)        | Ya, dengan backoff               | Sementara; coba ulang dengan exponential backoff. Pengecualian: satu 503 sesi lokal bergantung pada data dan dapat bertahan; lihat [Sesi lokal sementara tidak tersedia](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-sessions-temporarily-unavailable).                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

## 400 Bad Request

Permintaan valid secara sintaksis tetapi berisi parameter yang ditolak server. Perbaiki parameter dan coba ulang.

### Format timestamp tidak valid

**Type:** `invalid_request_error`

```text wrap
The `created_at.gte` parameter contains an invalid timestamp format. Timestamps must be provided in RFC 3339 format e.g., "2024-03-01T00:00:00Z". Got "2024-01-01".
```

**Penyebab:** Nilai `created_at.*` atau `updated_at.*` (`.gte`, `.gt`, `.lte`, `.lt`) tidak dapat diurai sebagai datetime. Pesan menyebutkan parameter yang gagal dan menampilkan kembali nilai yang dikirim.

**Perbaikan:** Kirim timestamp RFC 3339 lengkap termasuk waktu dan zona waktu, misalnya, `2024-03-01T00:00:00Z` atau `2024-03-01T00:00:00+00:00`.

Daftar sesi lokal (`GET /v1/compliance/apps/sessions/local`) juga mengembalikan 400 `invalid_request_error` ketika kedua batas waktu diberikan dan `created_at.lt` tidak secara ketat setelah `created_at.gte`. Body-nya berbunyi:

```text wrap
created_at.lt must be strictly after created_at.gte.
```

Kirim `created_at.lt` yang lebih lambat dari `created_at.gte`, atau hilangkan salah satu batas.

### Limit tidak valid

**Type:** `invalid_request_error`

```text wrap
The limit parameter must be between 1 and 1000, inclusive. Got 1500.
```

**Penyebab:** Parameter query `limit` berada di luar rentang yang diterima. Batas yang disebutkan dalam pesan mencerminkan maksimum untuk endpoint spesifik yang dipanggil.

**Perbaikan:** Kirim `limit` dalam rentang yang diterima endpoint. Setiap endpoint list memiliki rentang `limit` sendiri; lihat batasan parameter pada halaman [referensi Compliance API](https://platform.claude.com/docs/id/api/compliance) yang sesuai.

Endpoint transkrip sesi (`GET /v1/compliance/apps/sessions/remote/{session_id}/messages` dan `GET /v1/compliance/apps/sessions/local/{session_id}/messages`) memvalidasi parameter pemotongannya dengan cara yang sama: `tool_use_input_max_bytes` dan `tool_result_max_bytes` masing-masing menerima jumlah byte positif atau `-1` (maksimum server), sehingga nilai seperti `0` mengembalikan 400 `invalid_request_error` yang sama.

### ID paginasi tidak valid

**Type:** `invalid_request_error`

```text wrap
Invalid `after_id`. No activity found for `after_id` "activity_invalid123"
```

**Penyebab:** Kursor `after_id` atau `before_id` tidak dapat didekode sebagai kursor opaque atau diurai sebagai ID aktivitas.

**Perbaikan:** Perlakukan kursor paginasi sebagai string opaque. Selalu salin nilai `first_id` atau `last_id` yang dikembalikan oleh halaman sebelumnya; berhenti ketika `has_more` bernilai `false`. Jangan membuat kursor dari ID objek.

Endpoint direktori, proyek, dan sesi (organizations, users, roles, role permissions, groups, group members, projects, project attachments, sesi lokal dan remote, serta session messages) melakukan paginasi dengan token `page` opaque alih-alih `after_id` dan `before_id`. Saran yang sama berlaku: teruskan nilai `next_page` dari respons sebelumnya tanpa perubahan, dan berhenti ketika `has_more` bernilai `false` (atau, pada endpoint sesi, yang tidak mengembalikan `has_more`, ketika `next_page` bernilai `null`). Token `page` yang salah format mengembalikan 400 `invalid_request_error` yang sama seperti `after_id` atau `before_id` yang salah format.

Kedua endpoint sesi lokal (list dan endpoint messages) mengembalikan 400 `invalid_request_error` berikut untuk nilai `page` apa pun yang tidak dapat didekode, misalnya token yang terpotong atau diubah setelah Anda menyimpannya, atau token yang diterbitkan oleh endpoint berbeda atau di bawah organisasi induk berbeda. Pada endpoint messages sesi lokal (`GET /v1/compliance/apps/sessions/local/{session_id}/messages`), setiap kursor `page` juga terikat pada sesi dan `order` tempat kursor diterbitkan, sehingga kursor yang diterbitkan untuk sesi atau urutan pengurutan berbeda mengembalikan body yang sama:

```text wrap
The page parameter is not a valid cursor for this request.
```

Kursor pada endpoint messages juga kedaluwarsa 24 jam setelah walk (satu kali penelusuran melalui halaman-halaman) dimulai. Kursor yang kedaluwarsa mengembalikan:

```text wrap
The page cursor has expired. Restart the walk without a page parameter; results will reflect the current retention boundary.
```

Untuk body pertama, kirim ulang nilai `next_page` yang tidak dimodifikasi dari respons sebelumnya ke endpoint dan sesi yang menerbitkannya. Untuk kursor yang kedaluwarsa, mulai ulang tanpa parameter `page`; walk baru mencerminkan batas retensi yang berlaku saat dimulai, sehingga pesan yang telah melewati periode retensi sementara itu tidak lagi dikembalikan (lihat [Mengambil transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-a-local-session-transcript)).

## 401 Unauthorized

Header `x-api-key` tidak ada atau tidak cocok dengan kunci yang dikenal. Kunci yang valid dengan scope yang salah mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden) sebagai gantinya.

### Kunci API tidak valid

**Type:** `authentication_error`

```text wrap
The API key provided is invalid or has been revoked.
```

**Penyebab:** Kunci dalam `x-api-key` tidak ada, telah dihapus, atau telah dinonaktifkan. Header `x-api-key` yang hilang atau kosong mengembalikan body yang sama, jadi periksa baik penyimpanan rahasia Anda maupun status pencabutan kunci.

**Perbaikan:** Konfirmasi nilai kunci, periksa bahwa kunci belum dihapus di claude.ai (Compliance Access Keys) atau Claude Console (Admin API keys), dan konfirmasi bahwa kunci diaktifkan. Lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).

## 403 Forbidden

Kunci dalam `x-api-key` valid tetapi tidak membawa scope yang diperlukan endpoint. Pesan verbatim mencantumkan scope yang dibawa kunci (`Got:`) dan scope yang diperlukan endpoint (`Needed:`), sehingga Anda dapat mengonfirmasi apa yang dibawa kunci tanpa memeriksa ulang Claude Console atau claude.ai. Scope Compliance Access Key tidak dapat diubah setelah pembuatan, sehingga setiap perbaikan scope yang tidak memadai mengarahkan Anda untuk membuat kunci baru alih-alih mengedit yang sudah ada.

### Scope tidak memadai: Activity Feed

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_user_data'] Needed: ['read:compliance_activities']
```

**Penyebab:** Kunci tanpa `read:compliance_activities` digunakan untuk memanggil `GET /v1/compliance/activities`. Ada dua jalur umum menuju kesalahan ini:

* Compliance Access Key (`sk-ant-api01-...`) dibuat tanpa scope `read:compliance_activities`.
* Kunci Admin API Claude Console (`sk-ant-admin01-...`) dibuat saat Compliance API tidak diaktifkan untuk organisasi. Kunci yang dibuat saat Compliance API tidak diaktifkan tidak membawa scope tersebut; lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api).

**Perbaikan:** Scope Compliance Access Key tidak dapat diubah setelah pembuatan. Buat kunci baru yang menyertakan `read:compliance_activities`, atau gunakan kunci Admin API Claude Console. Lihat [Kunci mana yang Anda butuhkan?](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#which-key-do-you-need) untuk kondisi di mana kunci Admin API membawa scope ini.

### Scope tidak memadai: data organisasi

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_user_data'] Needed: ['read:compliance_org_data']
```

**Penyebab:** Kunci tanpa `read:compliance_org_data` digunakan untuk memanggil endpoint organizations, roles, groups, atau effective-settings. Ada dua jalur umum menuju kesalahan ini:

* Compliance Access Key (`sk-ant-api01-...`) dibuat tanpa scope `read:compliance_org_data`.
* Kunci Admin API Claude Console (`sk-ant-admin01-...`) digunakan. Kunci Admin API hanya membawa `read:compliance_activities` dan tidak dapat membaca metadata organisasi.

**Perbaikan:** [Buat Compliance Access Key baru](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) dengan `read:compliance_org_data` dipilih. Kunci Admin API tidak dapat membaca metadata organisasi; Compliance Access Key diperlukan.

### Scope yang dihentikan: pengaturan organisasi

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_org_settings'] Needed: ['read:compliance_org_data']
```

**Penyebab:** Scope `read:compliance_org_settings` dihentikan pada 30 Juni 2026. `GET /v1/compliance/organizations/{organization_id}/settings` sekarang memerlukan `read:compliance_org_data`, scope yang sama dengan endpoint organisasi lainnya, dan scope yang dihentikan tidak lagi mengotorisasi apa pun. Compliance Access Key yang hanya membawa `read:compliance_org_settings` mengembalikan kesalahan ini pada setiap panggilan ke endpoint settings, meskipun kunci tersebut berfungsi sebelum penghentian. Scope yang dihentikan tidak lagi dapat dipilih atau diberikan saat membuat kunci.

**Perbaikan:** Scope Compliance Access Key tidak dapat diubah setelah pembuatan. [Buat Compliance Access Key baru](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) dengan `read:compliance_org_data` dipilih, perbarui integrasi Anda untuk menggunakannya, lalu hapus kunci lama. Kunci yang sudah membawa `read:compliance_org_data` tidak terpengaruh oleh penghentian ini.

### Scope tidak memadai: data pengguna

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_activities'] Needed: ['read:compliance_user_data']
```

**Penyebab:** Kunci tanpa `read:compliance_user_data` digunakan untuk memanggil endpoint chats, messages, files, projects, sessions, organization users, atau group-members. Ada dua jalur umum menuju kesalahan ini:

* Compliance Access Key (`sk-ant-api01-...`) dibuat tanpa scope `read:compliance_user_data`.
* Kunci Admin API Claude Console (`sk-ant-admin01-...`) digunakan. Kunci Admin API hanya membawa `read:compliance_activities` dan tidak dapat diberikan `read:compliance_user_data`, sehingga tidak dapat memanggil endpoint chat, file, project, project attachment, session, user, atau group-member.

**Perbaikan:** Gunakan [Compliance Access Key](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) yang dibuat di claude.ai dengan `read:compliance_user_data` dipilih. Jika permintaan memang seharusnya hanya Activity Feed, arahkan kunci Admin API ke `GET /v1/compliance/activities` sebagai gantinya.

### Scope tidak memadai: delete

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_user_data'] Needed: ['delete:compliance_user_data']
```

**Penyebab:** Compliance Access Key tanpa `delete:compliance_user_data` digunakan untuk memanggil endpoint `DELETE` pada chats, files, atau projects.

**Perbaikan:** [Buat Compliance Access Key baru](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) dengan `delete:compliance_user_data` dipilih. Scope delete terpisah dari `read:compliance_user_data` sehingga kunci audit read-only tidak dapat menghapus konten.

## 404 Not Found

Endpoint berhasil diresolusi tetapi ID sumber daya tidak ada atau telah dihapus. Penghapusan Compliance API bersifat langsung dan permanen, sehingga 404 pada ID yang sebelumnya dikenal biasanya berarti konten telah dihapus secara permanen melalui panggilan delete Compliance API atau dihapus oleh kebijakan retensi. Satu pengecualian adalah sesi remote yang masih dalam status `pending`, yang endpoint messages-nya mengembalikan 404 secara sementara hingga sesi dimulai; lihat [Sesi remote tidak ditemukan](https://platform.claude.com/docs/id/manage-claude/compliance-errors#remote-session-not-found). String activity-type yang dikutip dalam setiap Perbaikan (misalnya, `claude_chat_created`) adalah nilai yang dapat Anda teruskan ke filter `activity_types[]` Activity Feed; lihat [Query compliance activities](https://platform.claude.com/docs/id/api/compliance/activities/list) untuk setiap nilai yang didukung.

Sesi lokal tidak memiliki status `pending`, sehingga 404 `Local session not found.` tidak pernah bersifat sementara; lihat [Sesi lokal tidak ditemukan](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-session-not-found) untuk penyebabnya dan untuk respons `Local sessions are not available.` yang terpisah, yang tidak bergantung pada ID sesi dan dapat bersifat sementara.

### Chat tidak ditemukan

**Type:** `not_found_error`

```text wrap
Chat claude_chat_01H5CWunD7RpVJ5bHa8RCkja not found.
```

**Penyebab:** ID chat dalam path tidak cocok dengan chat yang dapat dibaca melalui Compliance API. Chat mungkin telah dihapus secara permanen melalui panggilan Compliance API sebelumnya atau dihapus oleh kebijakan retensi organisasi Anda, atau mungkin milik organisasi yang tidak dapat dibaca oleh kunci pemanggil. Chat yang dihapus secara soft oleh pengguna di claude.ai tidak mengembalikan 404; chat tersebut tetap dapat dibaca dengan `deleted_at` terisi.

**Perbaikan:** Konfirmasi ID chat terhadap aktivitas `claude_chat_created` atau `claude_chat_viewed` terbaru. Jika aktivitas tersebut baru dan pembacaan masih gagal, chat telah dihapus secara permanen (melalui API ini atau oleh kedaluwarsa kebijakan retensi) atau milik organisasi di luar scope kunci Anda.

### File tidak ditemukan

**Type:** `not_found_error`

```text wrap
No file found with provided id, or it has already been deleted.
```

**Penyebab:** ID file tidak ada atau telah dihapus. Kesalahan ini berlaku untuk file yang dilampirkan ke chat (`claude_file_...`) dan file proyek.

**Perbaikan:** Rekonsiliasi terhadap aktivitas `claude_file_uploaded` atau `claude_file_deleted` terbaru. Jika file telah dihapus, binernya hilang; catatan aktivitas tetap ada di feed selama jendela retensi 6 tahun.

### Proyek tidak ditemukan

**Type:** `not_found_error`

```text wrap
No project is found with the provided id.
```

**Penyebab:** ID proyek tidak ada atau telah dihapus.

**Perbaikan:** Rekonsiliasi terhadap aktivitas `claude_project_created` atau `claude_project_deleted` terbaru. Activity Feed terus mengekspos peristiwa siklus hidup proyek bahkan setelah proyek itu sendiri hilang.

### Dokumen proyek tidak ditemukan

**Type:** `not_found_error`

```text wrap
No project document found with provided id, or it has already been deleted.
```

**Penyebab:** ID dokumen proyek tidak ada atau telah dihapus. Kesalahan ini berlaku untuk dokumen proyek teks (`claude_proj_doc_...`), bukan untuk file proyek.

**Perbaikan:** Gunakan `GET /v1/compliance/apps/projects/{project_id}/attachments` untuk mencantumkan lampiran saat ini. Jika dokumen tidak ada, dokumen telah dihapus; ambil melalui catatan aktivitas `claude_project_document_uploaded` jika Anda hanya memerlukan metadata.

### Sesi remote tidak ditemukan

**Type:** `not_found_error`

```text wrap
Remote session not found.
```

**Penyebab:** ID sesi yang diteruskan ke `GET /v1/compliance/apps/sessions/remote/{session_id}/messages` tidak cocok dengan transkrip sesi yang dapat dibaca melalui Compliance API. Ini terjadi ketika ID sesi (`cse_...`) tidak ada atau sesi telah dihapus, ketika sesi milik organisasi yang tidak dapat dibaca kunci Anda, atau ketika `status` sesi masih `pending`: sesi pending belum memiliki transkrip, sehingga endpoint messages mengembalikan 404 hingga sesi dimulai. ID sesi yang bukan pengidentifikasi `cse_` yang terbentuk dengan baik mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request) sebagai gantinya.

**Perbaikan:** Konfirmasi ID sesi dan `status`-nya terhadap `GET /v1/compliance/apps/sessions/remote`; lihat [Mengambil sesi remote](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-remote-sessions). Jika sesi `pending`, coba ulang setelah sesi meninggalkan status tersebut. Jika sesi tidak lagi muncul dalam daftar, sesi telah dihapus dan transkripnya tidak dapat diambil.

### Sesi lokal tidak ditemukan

**Type:** `not_found_error`

```text wrap
Local session not found.
```

**Penyebab:** ID sesi yang diteruskan ke `GET /v1/compliance/apps/sessions/local/{session_id}` atau `GET /v1/compliance/apps/sessions/local/{session_id}/messages` tidak cocok dengan sesi lokal yang dapat dibaca melalui Compliance API. Kedua endpoint mengembalikan satu pesan ini, tanpa membedakan penyebabnya, ketika ID bukan sesi dalam organisasi yang dapat dibaca kunci Anda (termasuk ID yang milik organisasi induk lain), ketika sesi tidak pernah ada, ketika [zero data retention](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) berlaku untuk sesi tersebut, atau ketika semua aktivitas sesi telah melewati periode retensi yang berlaku untuk organisasi yang menjalankannya. Tidak seperti sesi remote, sesi lokal tidak memiliki status `pending`, sehingga respons `Local session not found.` tidak memiliki bentuk sementara. ID sesi yang bukan pengidentifikasi `clls_` yang terbentuk dengan baik mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request) sebagai gantinya.

Endpoint sesi lokal, termasuk endpoint list, mengembalikan pesan 404 yang berbeda, `Local sessions are not available.`, saat endpoint itu sendiri tidak tersedia untuk organisasi induk Anda. Respons tersebut tidak bergantung pada ID sesi; tidak ada kunci, scope, atau pengaturan di sisi pelanggan yang mengubahnya, dan dapat bersifat sementara. Kedua respons membawa type `not_found_error`; teks pesan adalah yang membedakannya.

**Perbaikan:** Konfirmasi ID sesi terhadap `GET /v1/compliance/apps/sessions/local`; lihat [Mengambil sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-local-sessions). Jika sesi tidak lagi muncul dalam daftar, kontennya telah melewati retensi (atau sesi tidak lagi berada dalam organisasi yang dapat dibaca kunci Anda) dan transkripnya tidak dapat diambil; hapus ID dari antrean Anda. Jika setiap panggilan, termasuk list, mengembalikan `Local sessions are not available.`, simpan ID sesi yang diantrekan dan coba ulang pada jadwal berikutnya; jika respons tetap berlanjut, hubungi perwakilan Anthropic Anda dan sertakan header respons `request-id`.

### Organisasi, role, atau grup tidak ditemukan

**Type:** `not_found_error`

```text wrap
The "ce86b5f3-7c16-48b3-a9f3-e1d2c4b8a0f1" organization does not exist or the requester is not authorized to access it.
```

Endpoint organization, role, dan group mengembalikan 404 `not_found_error` dalam format kesalahan standar. Pesan organization menyebutkan `org_uuid`; pesan role dan group bersifat generik (`Role not found.`, `Group not found.`). Ini terjadi ketika ID path (`org_uuid`, `role_id`, atau `group_id`) tidak ada atau tidak lagi milik pohon yang dapat dibaca kunci pemanggil.

**Penyebab:** ID dalam path tidak cocok dengan catatan yang dapat dibaca melalui Compliance API. Role dan grup dapat dihapus, dan organisasi dapat dilepaskan dari pohon induk.

**Perbaikan:** Verifikasi ID terhadap endpoint list yang sesuai, dan rekonsiliasi terhadap aktivitas organisasi, role, atau grup terbaru di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed).

### Pengaturan organisasi tidak tersedia

**Type:** `not_found_error`

```text wrap
organization `91012d09-e48b-438e-a489-1bebfd8fa6f9` not found in this organization's hierarchy
```

**Penyebab:** `GET /v1/compliance/organizations/{organization_id}/settings` mengembalikan 404 ini dalam tiga kasus yang sengaja berbagi body yang sama sehingga respons tidak mengungkapkan apakah organisasi ada: `organization_id` bukan salah satu organisasi tertaut induk Anda, nilainya bukan UUID yang valid, atau endpoint settings belum diaktifkan untuk organisasi induk Anda.

**Perbaikan:** Verifikasi ID terhadap [List organizations](https://platform.claude.com/docs/id/api/compliance/organizations/list). Jika ID organisasi yang diketahui valid masih mengembalikan 404, endpoint settings belum diaktifkan untuk organisasi induk Anda; hubungi perwakilan Anthropic Anda.

## 409 Conflict

Permintaan terbentuk dengan baik dan terotorisasi tetapi bertentangan dengan status sumber daya saat ini.

### Proyek memiliki chat yang terlampir

**Type:** `conflict_error`

```text wrap
The "claude_proj_01KGp4eZNug9ri4kE35RSppq" project cannot be deleted as it has chats attached to it. Delete or detach all chats, and try deleting the project again.
```

**Penyebab:** `DELETE /v1/compliance/apps/projects/{project_id}` dipanggil pada proyek yang masih memiliki chat terlampir.

**Perbaikan:** Cantumkan chat proyek dengan `GET /v1/compliance/apps/chats?user_ids[]={user_id}&project_ids[]={project_id}` (filter `project_ids[]` memerlukan setidaknya satu nilai `user_ids[]`; enumerasi ID melalui [List organization users](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users)), hapus masing-masing dengan `DELETE /v1/compliance/apps/chats/{claude_chat_id}`, lalu coba ulang penghapusan proyek.

## 429 Too Many Requests

Permintaan ke Compliance API dibatasi hingga **600 permintaan per menit per [organisasi induk](https://platform.claude.com/docs/id/manage-claude/compliance-api#how-the-compliance-api-works)**. Batas ini adalah satu anggaran yang dibagikan di seluruh kunci di bawah induk (Compliance Access Key dan kunci Admin API dari semua organisasi tertaut) dan di seluruh endpoint `/v1/compliance/*`; endpoint sesi remote membawa anggaran permintaan kedua di atasnya. Untuk organisasi Claude Console mandiri, yang tidak memiliki organisasi induk, anggaran yang sama berlaku untuk organisasi itu sendiri dan dibagikan di seluruh kunci Admin API-nya. Hubungi perwakilan Anthropic Anda jika integrasi Anda memerlukan batas yang lebih tinggi.

Setelah kunci API Anda terautentikasi, respons Compliance API melaporkan anggaran bersama melalui [header respons batas laju](https://platform.claude.com/docs/id/api/rate-limits#response-headers) standar sehingga klien Anda dapat melakukan throttle secara proaktif alih-alih menunggu 429:

* `anthropic-ratelimit-requests-limit` adalah anggaran permintaan per menit.
* `anthropic-ratelimit-requests-remaining` adalah anggaran yang tersisa dalam jendela saat ini.
* `anthropic-ratelimit-requests-reset` adalah timestamp RFC 3339 saat jendela direset dan anggaran penuh dipulihkan.

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

**Penyebab:** Organisasi induk Anda (atau organisasi Claude Console mandiri) mengirim lebih dari 600 permintaan ke `/v1/compliance/*` dalam jendela 1 menit, di seluruh kunci yang berbagi anggarannya, atau telah menghabiskan anggaran permintaan kedua endpoint sesi remote (dijelaskan nanti di bagian ini).

**Perbaikan:** Tunggu sejumlah detik dalam header `retry-after`, lalu coba ulang. Jika header tidak ada (misalnya, dihapus oleh perantara), kembali ke exponential backoff (mulai dari 1 detik, gandakan hingga 60 detik). Jangan majukan kursor paginasi Anda pada 429: permintaan yang gagal tidak mengembalikan data, sehingga kursor dari halaman terakhir yang berhasil masih benar.

Permintaan yang gagal autentikasi (kunci yang hilang atau tidak dikenali, atau kunci Claude API alih-alih Compliance Access Key atau kunci Admin API) ditolak sebelum rate limiter dan tidak mengonsumsi kuota. Kunci valid yang tidak memiliki scope yang diperlukan endpoint mengonsumsi satu unit kuota sebelum 403 dikembalikan.

[Endpoint sesi remote](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-remote-sessions) membawa anggaran permintaan kedua, juga dikunci ke organisasi induk Anda, di atas batas bersama. 429 dari anggaran tersebut membawa header `retry-after` yang selalu `1` (waktu tunggu minimum, bukan waktu reset aktual); header `anthropic-ratelimit-*` apa pun pada respons tersebut menggambarkan batas bersama alih-alih anggaran ini, jadi lakukan backoff secara eksponensial jika 429 berulang. [Endpoint sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-local-sessions) tidak memiliki anggaran kedua dan hanya dihitung terhadap batas bersama.

Jika Anda melakukan polling [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) sesuai jadwal, anggarkan laju permintaan agregat Anda (di seluruh kunci, organisasi tertaut, dan worker konkuren) di bawah batas bersama. Pantau `anthropic-ratelimit-requests-remaining` untuk memperlambat sebelum Anda mencapainya. Lihat [Merancang integrasi compliance Anda](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#choose-a-feed-consumption-pattern) untuk memilih antara window-polling dan ingesti berbasis kursor.

## 500 Internal Server Error

500 dari Compliance API membawa header respons `x-should-retry: false` ketika kegagalan bersifat deterministik. SDK Anthropic mematuhi header ini secara otomatis. Jika Anda menggunakan pustaka retry HTTP generik yang mencoba ulang pada setiap 5xx, tekan percobaan ulang ketika `x-should-retry` bernilai `false`; mencoba ulang kesalahan ini gagal secara identik pada setiap percobaan.

500 tanpa header `x-should-retry: false` bersifat sementara: coba ulang dengan exponential backoff (mulai dari 1 detik, gandakan hingga 60 detik). Hal yang sama berlaku untuk respons 502, 503, 504, dan 529. Satu 503 sesi lokal, yang dijelaskan berikutnya, bergantung pada data alih-alih bersifat sementara. Lihat [Kesalahan](https://platform.claude.com/docs/id/api/errors) untuk semantik retry di seluruh platform.

### Sesi lokal sementara tidak tersedia

**Type:** `overloaded_error`

```text wrap
The local-sessions index is temporarily unavailable. Try again shortly.
```

```text wrap
Captured content is temporarily unavailable. Try again shortly.
```

```text wrap
The local-sessions index cannot currently evaluate retention overrides for this page. Try again later.
```

**Penyebab:** [Endpoint sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-local-sessions) mengembalikan 503 dengan salah satu body ini. Dua yang pertama berarti bahwa daftar sesi, atau konten sesi yang ditangkap, tidak tersedia untuk sementara; itu adalah kondisi sementara yang terkait dengan beban atau back end. Body ketiga (yang berbunyi `for this session` alih-alih `for this page` pada endpoint retrieve dan messages) berarti bahwa pengaturan retensi atau penanganan data yang berlaku untuk satu atau lebih sesi dalam rentang yang diminta belum dapat dievaluasi. Itu bergantung pada data dan pengaturan organisasi yang menjalankan sesi alih-alih pada beban, dan dapat bertahan untuk periode yang lama. Ketiga body berbagi type `overloaded_error`, sehingga ini adalah salah satu dari sedikit kasus di halaman ini di mana teks pesan, alih-alih `error.type`, membedakan kondisi yang memerlukan penanganan berbeda.

**Perbaikan:** Untuk dua body `Try again shortly.`, coba ulang dengan exponential backoff dan jangan majukan kursor `page` Anda, karena permintaan yang gagal tidak mengembalikan data. Untuk body `Try again later.`, jangan menahan walk tetap terbuka menunggu kondisi tersebut hilang. Pada endpoint list, coba ulang nanti dengan memulai ulang tanpa parameter `page` (token halaman list yang lebih lama dari 24 jam masih diterima tetapi dievaluasi ulang terhadap batas retensi saat ini, sehingga walk yang diparkir dapat melewatkan sesi), atau persempit jendela `created_at.gte` dan `created_at.lt` hingga permintaan berhasil dan ekspor rentang yang dilewati secara terpisah pada eksekusi berikutnya. Pada endpoint retrieve dan messages, lewati ID sesi tersebut, lanjutkan dengan sisa ekspor Anda, dan coba ulang sesi pada eksekusi berikutnya; kursor halaman messages kedaluwarsa 24 jam setelah halaman pertama walk, jadi mulai ulang walk sesi tersebut tanpa `page` saat Anda kembali ke sana. Jika kondisi berulang di seluruh eksekusi, hubungi perwakilan Anthropic Anda dan sertakan header respons `request-id`.

Untuk insiden di seluruh layanan, periksa [status.anthropic.com](https://status.anthropic.com).

## Langkah berikutnya

<CardGroup cols={2}>
  <Card title="FAQ Compliance API" href="https://platform.claude.com/docs/id/manage-claude/compliance-faq">
    Pertanyaan umum tentang akses, scope, retensi, dan integrasi.
  </Card>

  <Card title="Kesalahan" href="https://platform.claude.com/docs/id/api/errors">
    Katalog kesalahan di seluruh platform dan semantik retry.
  </Card>
</CardGroup>
