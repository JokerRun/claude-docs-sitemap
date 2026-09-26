---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-errors
fetched_at: 2026-09-26T02:19:50.539049Z
sha256: 1e2d2c7781469d35ab6152c11ebef359d0980644e80aa5bdb64a4fffaff9bcdb
---

---
title: Menangani error Compliance API
url: https://platform.claude.com/docs/id/manage-claude/compliance-errors
description: Respons error Compliance API berdasarkan kode status HTTP, beserta penyebab dan perbaikan untuk masing-masing.
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

Halaman ini mencantumkan respons error Compliance API yang umum berdasarkan kode status HTTP, beserta penyebab dan perbaikan untuk masing-masing.

Compliance API mengembalikan error dalam [format error Anthropic](https://platform.claude.com/docs/id/api/errors) standar: kode status non-2xx, header respons `request-id`, dan body JSON dengan objek `error` yang berisi `type` dan `message`. Sertakan nilai header `request-id` saat Anda mengeskalasi ke tim dukungan.

```json
{
  "error": {
    "type": "permission_error",
    "message": "Missing required scopes. Got: ['read:compliance_activities'] Needed one of: ['read:compliance_user_data', 'read:org_audit']"
  }
}
```

Di halaman ini, sesi lokal berjalan di mesin pengguna dan sesi jarak jauh berjalan di cloud; lihat [Mengambil transkrip sesi](https://platform.claude.com/docs/id/manage-claude/compliance-sessions).

Cocokkan berdasarkan kode status HTTP dan `error.type`, bukan berdasarkan string pesan. Pesan cukup stabil untuk disalin ke dalam runbook, tetapi mungkin diubah susunan katanya seiring waktu; kode status dan nilai type merupakan bagian dari kontrak API. Beberapa respons yang memiliki kode status dan type yang sama dibedakan berdasarkan pesannya; masing-masing disebutkan di tempat yang relevan.

Tabel berikut memberi tahu Anda secara sekilas apakah perlu mencoba ulang. Setiap bagian berikutnya menampilkan body error apa adanya beserta perbaikannya.

| Status                                                                                                                     | Coba ulang?                      | Kapan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request)                     | Tidak                            | Perbaiki permintaan, atau aktifkan Compliance API jika pesan menyatakan bahwa API tersebut belum diaktifkan, lalu kirim ulang.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [401 Unauthorized](https://platform.claude.com/docs/id/manage-claude/compliance-errors#401-unauthorized)                   | Tidak                            | Kunci tidak dikenali, telah dinonaktifkan, atau telah kedaluwarsa; aktifkan kembali atau ganti kunci tersebut, lalu kirim ulang.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden)                         | Tidak                            | Tambahkan scope yang kurang atau gunakan jenis kunci yang tepat, lalu kirim ulang.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found)                         | Biasanya tidak                   | Pesan yang menyebutkan nama sumber daya berarti sumber daya tersebut telah dihapus atau tidak pernah ada; hapus dari antrean Anda. Pesan polos `Not found` berarti permintaan tidak terautentikasi (atau path tidak ada), bukan berarti sumber daya telah hilang; lihat [Permintaan tidak terautentikasi](https://platform.claude.com/docs/id/manage-claude/compliance-errors#request-not-authenticated). Endpoint sesi menambahkan dua kasus lagi: pada endpoint sesi lokal, pesan `Local sessions are not available.` (dikembalikan pada setiap panggilan, termasuk list) berarti endpoint tersebut saat ini tidak tersedia untuk organisasi induk Anda, bukan berarti sesi telah hilang; simpan ID yang ada di antrean Anda dan lihat [Sesi lokal tidak ditemukan](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-session-not-found). Sesi jarak jauh yang masih berstatus `pending` mengembalikan 404 pada endpoint messages-nya hingga sesi dimulai; lihat [Sesi jarak jauh tidak ditemukan](https://platform.claude.com/docs/id/manage-claude/compliance-errors#remote-session-not-found). |
| [409 Conflict](https://platform.claude.com/docs/id/manage-claude/compliance-errors#409-conflict)                           | Tidak                            | Permintaan bertentangan dengan status sumber daya saat ini; selesaikan konflik tersebut (misalnya dengan melepaskan sumber daya turunan), lalu coba ulang.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| [429 Too Many Requests](https://platform.claude.com/docs/id/manage-claude/compliance-errors#429-too-many-requests)         | Ya, setelah `retry-after`        | Tunggu selama jumlah detik di `retry-after`, lalu coba ulang; jangan majukan kursor Anda.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| [500 Internal Server Error](https://platform.claude.com/docs/id/manage-claude/compliance-errors#500-internal-server-error) | Bergantung pada `x-should-retry` | Periksa header respons `x-should-retry` sebelum mencoba ulang.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [502, 503, 504, 529](https://platform.claude.com/docs/id/manage-claude/compliance-errors#500-internal-server-error)        | Ya, dengan backoff               | Bersifat sementara; coba ulang dengan exponential backoff. Pengecualian: beberapa 503 sesi lokal tidak bersifat sementara. Lihat [Sesi lokal untuk sementara tidak tersedia](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-sessions-temporarily-unavailable).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

## 400 Bad Request

Permintaan valid secara sintaksis, tetapi server menolak sebuah parameter atau Compliance API belum diaktifkan untuk organisasi tersebut. Perbaiki penyebab yang disebutkan dalam pesan dan kirim ulang.

### Compliance API belum diaktifkan

**Type:** `invalid_request_error`

```text wrap
Compliance API is not enabled for this organization
```

**Penyebab:** Kunci valid, tetapi Compliance API belum diaktifkan untuk organisasi atau organisasi induk tempat kunci tersebut berada. Setiap endpoint mengembalikan respons ini hingga API diaktifkan, dan akan mengembalikannya lagi jika administrator menonaktifkan API tersebut.

**Perbaikan:** Aktifkan Compliance API dengan mengikuti [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api), lalu kirim ulang permintaan.

### Parameter query tidak dikenal

**Type:** `invalid_request_error`

```text wrap
Unknown query parameter: 'created_at[gte]'. Did you mean 'created_at.gte'?
```

**Penyebab:** Permintaan menyertakan parameter query yang tidak didefinisikan oleh endpoint; Compliance API menolak parameter yang tidak dikenali alih-alih mengabaikannya. Pesan menyebutkan nama parameter tersebut dan, untuk kesalahan yang nyaris benar seperti notasi kurung siku sebagai pengganti titik atau akhiran `[]` yang hilang, menyarankan nama yang didefinisikan.

**Perbaikan:** Gunakan nama parameter yang ditampilkan di halaman [referensi Compliance API](https://platform.claude.com/docs/id/api/compliance) untuk endpoint tersebut. Filter rentang menggunakan notasi titik (misalnya, `created_at.gte`), filter array menggunakan akhiran `[]` (misalnya, `activity_types[]`), dan parameter paginasi adalah `after_id`, `before_id`, atau `page`, tergantung pada endpoint-nya.

### Nilai parameter tidak valid

**Type:** `invalid_request_error`

```text wrap
limit: Input should be less than or equal to 1000
```

```text wrap
created_at.gte: Input should be a valid datetime or date, invalid character in year
```

```text wrap
activity_types[].0: Input is not one of the permitted values.
```

**Penyebab:** Nilai sebuah parameter query gagal validasi. Pesan diawali dengan nama parameter (diikuti posisi elemen untuk parameter array), lalu menyatakan batasan yang gagal dipenuhi. Tiga kasus umum ditampilkan: `limit` di atas nilai maksimum endpoint (angka dalam pesan adalah nilai maksimum endpoint tersebut), nilai `created_at.*` atau `updated_at.*` yang tidak dapat di-parse sebagai tanggal atau timestamp, dan nilai `activity_types[]` yang bukan merupakan jenis aktivitas yang didukung.

**Perbaikan:** Perbaiki parameter yang disebutkan dalam pesan. Setiap endpoint list memiliki rentang `limit` sendiri; lihat batasan parameter di halaman [referensi Compliance API](https://platform.claude.com/docs/id/api/compliance) yang sesuai. Kirim timestamp dalam format RFC 3339 dengan offset UTC eksplisit, misalnya, `2024-03-01T00:00:00Z` atau `2024-03-01T00:00:00+00:00`; list sesi lokal menolak timestamp tanpa offset (`created_at.gte: Input should have timezone info`). Untuk nilai `activity_types[]` yang didukung, lihat [Mengkueri aktivitas kepatuhan](https://platform.claude.com/docs/id/api/compliance/activities/list).

List sesi lokal (`GET /v1/compliance/apps/sessions/local`) juga mengembalikan 400 `invalid_request_error` ketika kedua batas waktu diberikan dan `created_at.lt` tidak benar-benar lebih lambat dari `created_at.gte`. Body-nya berbunyi:

```text wrap
created_at.lt must be strictly after created_at.gte.
```

Kirim `created_at.lt` yang lebih lambat dari `created_at.gte`, atau hilangkan salah satu batas.

Endpoint transkrip sesi (`GET /v1/compliance/apps/sessions/local/{session_id}/messages` dan `GET /v1/compliance/apps/sessions/remote/{session_id}/messages`) memvalidasi parameter pemotongannya dengan cara yang sama: `tool_use_input_max_bytes` dan `tool_result_max_bytes` masing-masing menerima jumlah byte positif atau `-1` (nilai maksimum server), sehingga nilai seperti `0` mengembalikan 400 `invalid_request_error` yang sama.

### Kursor paginasi tidak valid

**Type:** `invalid_request_error`

```text wrap
Invalid activity_id format: 'activity_invalid123'
```

```text wrap
Invalid pagination cursor for 'after_id'
```

**Penyebab:** Sebuah "pagination cursor" (kursor paginasi) tidak dapat didekode. Pada Activity Feed, nilai `after_id` atau `before_id` yang bukan kursor yang diterbitkan oleh API maupun ID aktivitas yang terbentuk dengan benar akan mengembalikan body pertama, yang menampilkan kembali nilai yang dikirim. Pada endpoint chat dan pesan chat, nilai `after_id` atau `before_id` yang tidak dapat didekode akan mengembalikan body kedua, yang menyebutkan nama parameternya.

**Perbaikan:** Perlakukan kursor paginasi sebagai string buram (opaque). Selalu salin nilai `first_id` atau `last_id` yang dikembalikan oleh halaman sebelumnya; berhenti ketika `has_more` bernilai `false`. Jangan membuat kursor dari ID objek.

Endpoint direktori, proyek, dan sesi (organisasi, pengguna, peran, izin peran, grup, anggota grup, proyek, lampiran proyek, sesi lokal dan jarak jauh, serta pesan sesi) melakukan paginasi dengan token `page` yang buram alih-alih `after_id` dan `before_id`. Saran yang sama berlaku: teruskan nilai `next_page` dari respons sebelumnya tanpa diubah, dan berhenti ketika `has_more` bernilai `false` (atau, pada endpoint sesi, yang tidak mengembalikan `has_more`, ketika `next_page` bernilai `null`). Token `page` yang salah bentuk mengembalikan 400 `invalid_request_error` yang sama seperti `after_id` atau `before_id` yang salah bentuk, dengan pesan yang spesifik untuk endpoint tersebut.

Dua endpoint sesi lokal yang menggunakan paginasi (endpoint list dan endpoint messages) mengembalikan 400 `invalid_request_error` berikut untuk nilai `page` apa pun yang tidak dapat didekode, misalnya, token yang terpotong atau diubah setelah Anda menyimpannya, atau token yang diterbitkan oleh endpoint lain atau di bawah organisasi induk yang berbeda. Pada endpoint messages sesi lokal (`GET /v1/compliance/apps/sessions/local/{session_id}/messages`), setiap kursor `page` juga terikat pada sesi dan `order` tempat kursor tersebut diterbitkan, sehingga kursor yang diterbitkan untuk sesi atau urutan pengurutan yang berbeda mengembalikan body yang sama:

```text wrap
The page parameter is not a valid cursor for this request.
```

Kursor pada endpoint messages juga kedaluwarsa 24 jam setelah penelusuran (satu kali lintasan melalui halaman-halaman) dimulai. Kursor yang kedaluwarsa mengembalikan:

```text wrap
The page cursor has expired. Restart the walk without a page parameter; results will reflect the current retention boundary.
```

Untuk body pertama, kirim ulang nilai `next_page` yang tidak dimodifikasi dari respons sebelumnya ke endpoint dan sesi yang menerbitkannya. Untuk kursor yang kedaluwarsa, mulai ulang tanpa parameter `page`; penelusuran baru mencerminkan batas retensi yang berlaku saat penelusuran dimulai, sehingga pesan yang telah melewati periode retensi dalam rentang waktu tersebut tidak lagi dikembalikan (lihat [Mengambil transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-a-local-session-transcript)).

## 401 Unauthorized

Permintaan membawa Compliance Access Key (`sk-ant-api01-...`) atau kunci Admin API (`sk-ant-admin01-...`) yang tidak berhasil diautentikasi. Permintaan yang tidak membawa kunci, atau membawa kunci jenis lain, akan mengembalikan [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#request-not-authenticated) sebagai gantinya pada setiap endpoint kecuali pengaturan organisasi, dan kunci valid dengan scope yang salah akan mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden).

### Kunci API tidak valid, dinonaktifkan, atau kedaluwarsa

**Type:** `authentication_error`

```text wrap
API key is invalid.
```

```text wrap
API key has been deactivated.
```

```text wrap
API key has expired.
```

**Penyebab:** `API key is invalid.` berarti nilai yang dikirim tidak cocok dengan kunci yang dapat digunakan, misalnya karena terpotong atau diubah saat disimpan. `API key has been deactivated.` berarti kunci telah dinonaktifkan atau dihapus. `API key has expired.` berarti tanggal kedaluwarsa kunci Admin API telah lewat; Compliance Access Key tidak dibuat dengan tanggal kedaluwarsa.

**Perbaikan:** Untuk `API key is invalid.`, bandingkan nilai yang dikirim klien Anda dengan secret yang Anda simpan saat kunci dibuat; secret lengkap hanya ditampilkan sekali, jadi jika salinan yang Anda simpan salah, buat kunci baru. Untuk `API key has been deactivated.`, aktifkan kembali kunci jika kunci tersebut hanya dinonaktifkan, di [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) untuk Compliance Access Key atau [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys) untuk kunci Admin API; kunci yang telah dihapus tidak dapat dipulihkan. Untuk kunci yang dihapus atau kedaluwarsa, buat kunci baru dan perbarui integrasi Anda agar menggunakannya, seperti yang dijelaskan dalam [Mengelola dan merotasi kunci](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#manage-and-rotate-keys).

## 403 Forbidden

Kunci di `x-api-key` valid tetapi tidak membawa scope yang diterima oleh endpoint. Pesan apa adanya mencantumkan scope yang dibawa kunci (`Got:`) dan scope yang diterima endpoint (`Needed one of:` pada endpoint baca, di mana salah satu scope yang tercantum sudah cukup, atau `Needed:` pada endpoint hapus), sehingga Anda dapat memastikan apa yang dibawa kunci tanpa memeriksa ulang Claude Console atau claude.ai. Pada endpoint baca, daftar yang diterima juga mencakup `read:org_audit`, scope audit hanya-baca yang mencakup setiap endpoint baca Compliance API; lihat [Memilih scope untuk kunci Claude Enterprise](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#choose-scopes-for-a-claude-enterprise-key). Scope Compliance Access Key tidak dapat diubah setelah dibuat, sehingga setiap perbaikan untuk scope yang tidak memadai mengarahkan Anda untuk membuat kunci baru alih-alih mengedit kunci yang ada. Organisasi Claude Console mandiri (yang tidak memiliki organisasi induk) tidak dapat membuat Compliance Access Key, sehingga perbaikan yang memerlukannya tidak berlaku untuk organisasi tersebut; organisasi tersebut hanya dapat mengkueri Activity Feed.

### Scope tidak memadai: Activity Feed

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_user_data'] Needed one of: ['read:compliance_activities', 'read:org_audit']
```

**Penyebab:** Kunci tanpa `read:compliance_activities` digunakan untuk memanggil `GET /v1/compliance/activities`. Ada dua jalur umum yang menyebabkan error ini:

* Compliance Access Key (`sk-ant-api01-...`) dibuat tanpa scope `read:compliance_activities`.
* Kunci Admin API Claude Console (`sk-ant-admin01-...`) dibuat saat Compliance API belum diaktifkan untuk organisasi. Kunci yang dibuat saat Compliance API belum diaktifkan tidak membawa scope tersebut; lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api).

**Perbaikan:** Scope Compliance Access Key tidak dapat diubah setelah dibuat. Buat kunci baru yang menyertakan `read:compliance_activities`, atau gunakan kunci Admin API Claude Console. Lihat [Kunci mana yang Anda perlukan?](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#which-key-do-you-need) untuk kondisi di mana kunci Admin API membawa scope ini.

### Scope tidak memadai: data organisasi

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_user_data'] Needed one of: ['read:compliance_org_data', 'read:org_audit']
```

**Penyebab:** Kunci tanpa `read:compliance_org_data` digunakan untuk memanggil endpoint organisasi, peran, grup, atau pengaturan efektif. Ada dua jalur umum yang menyebabkan error ini:

* Compliance Access Key (`sk-ant-api01-...`) dibuat tanpa scope `read:compliance_org_data`.
* Kunci Admin API Claude Console (`sk-ant-admin01-...`) digunakan. Kunci Admin API hanya membawa `read:compliance_activities` dan tidak dapat membaca metadata organisasi.

**Perbaikan:** [Buat Compliance Access Key baru](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) dengan `read:compliance_org_data` dipilih. Kunci Admin API tidak dapat membaca metadata organisasi; Compliance Access Key diperlukan.

### Scope yang dihentikan: pengaturan organisasi

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_org_settings'] Needed one of: ['read:compliance_org_data', 'read:org_audit']
```

**Penyebab:** Scope `read:compliance_org_settings` dihentikan pada 30 Juni 2026. `GET /v1/compliance/organizations/{organization_id}/settings` kini memerlukan `read:compliance_org_data`, scope yang sama dengan endpoint organisasi lainnya, dan scope yang dihentikan tidak lagi memberikan otorisasi apa pun. Compliance Access Key yang hanya membawa `read:compliance_org_settings` mengembalikan error ini pada setiap panggilan ke endpoint pengaturan, meskipun kunci tersebut berfungsi sebelum penghentian. Scope yang dihentikan tidak lagi dapat dipilih atau diberikan saat membuat kunci.

**Perbaikan:** Scope Compliance Access Key tidak dapat diubah setelah dibuat. [Buat Compliance Access Key baru](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) dengan `read:compliance_org_data` dipilih, perbarui integrasi Anda agar menggunakannya, lalu hapus kunci lama. Kunci yang sudah membawa `read:compliance_org_data` tidak terpengaruh oleh penghentian ini.

### Scope tidak memadai: data pengguna

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_activities'] Needed one of: ['read:compliance_user_data', 'read:org_audit']
```

**Penyebab:** Kunci tanpa `read:compliance_user_data` digunakan untuk memanggil endpoint chat, pesan, file, proyek, sesi, pengguna organisasi, atau anggota grup. Ada dua jalur umum yang menyebabkan error ini:

* Compliance Access Key (`sk-ant-api01-...`) dibuat tanpa scope `read:compliance_user_data`.
* Kunci Admin API Claude Console (`sk-ant-admin01-...`) digunakan. Kunci Admin API hanya membawa `read:compliance_activities` dan tidak dapat diberi `read:compliance_user_data`, sehingga tidak dapat memanggil endpoint chat, file, proyek, lampiran proyek, sesi, pengguna, atau anggota grup.

**Perbaikan:** Gunakan [Compliance Access Key](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) yang dibuat di claude.ai dengan `read:compliance_user_data` dipilih. Jika permintaan memang seharusnya hanya untuk Activity Feed, arahkan kunci Admin API ke `GET /v1/compliance/activities` sebagai gantinya.

### Scope tidak memadai: hapus

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_user_data'] Needed: ['delete:compliance_user_data']
```

**Penyebab:** Compliance Access Key tanpa `delete:compliance_user_data` digunakan untuk memanggil endpoint `DELETE` pada chat, file, atau proyek.

**Perbaikan:** [Buat Compliance Access Key baru](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) dengan `delete:compliance_user_data` dipilih. Scope hapus terpisah dari `read:compliance_user_data` agar kunci audit hanya-baca tidak dapat menghapus konten.

## 404 Not Found

404 yang pesannya menyebutkan nama sumber daya atau jenis sumber daya berarti ID di path tidak ada atau telah dihapus. Penghapusan melalui Compliance API bersifat langsung dan permanen, sehingga 404 pada ID yang sebelumnya diketahui biasanya berarti konten telah hilang: dihapus permanen melalui panggilan hapus Compliance API, dihapus oleh kebijakan retensi, atau, untuk file dan artifact, dihapus bersama chat-nya oleh pengguna di claude.ai. 404 dengan pesan polos `Not found` berbeda: permintaan tidak terautentikasi (atau path tidak ada), dan endpoint mana pun dapat mengembalikannya, termasuk endpoint list; lihat [Permintaan tidak terautentikasi](https://platform.claude.com/docs/id/manage-claude/compliance-errors#request-not-authenticated). Endpoint sesi menambahkan dua kasus. Pada endpoint sesi lokal, pesan 404 terpisah, `Local sessions are not available.`, dikembalikan pada setiap panggilan (termasuk list) selama endpoint tersebut tidak tersedia untuk organisasi induk Anda; pesan ini tidak bergantung pada ID sesi dan dapat bersifat sementara. Lihat [Sesi lokal tidak ditemukan](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-session-not-found). Pada endpoint sesi jarak jauh, sesi yang masih dalam proses penyediaan (`status` bernilai `pending`) belum memiliki transkrip, sehingga endpoint messages-nya mengembalikan 404 hingga sesi dimulai. Lihat [Sesi jarak jauh tidak ditemukan](https://platform.claude.com/docs/id/manage-claude/compliance-errors#remote-session-not-found). String jenis aktivitas yang dikutip di setiap Perbaikan (misalnya, `claude_chat_created`) adalah nilai yang dapat Anda teruskan ke filter `activity_types[]` Activity Feed; lihat [Mengkueri aktivitas kepatuhan](https://platform.claude.com/docs/id/api/compliance/activities/list) untuk setiap nilai yang didukung.

### Permintaan tidak terautentikasi

**Type:** `not_found_error`

```text wrap
Not found
```

**Penyebab:** Permintaan tidak membawa kredensial yang diterima oleh Compliance API: tidak ada kunci API yang dikirim, atau kunci tersebut bukan Compliance Access Key (`sk-ant-api01-...`) atau kunci Admin API (`sk-ant-admin01-...`), misalnya, kunci Claude API (`sk-ant-api03-...`). Status, type, dan pesannya sama dengan path yang tidak ada dan tidak bergantung pada endpoint atau ID sumber daya apa pun, sehingga endpoint list seperti `GET /v1/compliance/activities` juga mengembalikan body ini. Satu-satunya pengecualian adalah `GET /v1/compliance/organizations/{organization_id}/settings`, yang menjawab permintaan semacam ini dengan 401 `authentication_error`. Pada setiap endpoint, Compliance Access Key atau kunci Admin API yang tidak berhasil diautentikasi akan mengembalikan [401 Unauthorized](https://platform.claude.com/docs/id/manage-claude/compliance-errors#401-unauthorized) sebagai gantinya.

**Perbaikan:** Kirim kunci di header `x-api-key` dan periksa prefiksnya: Compliance API hanya menerima kunci `sk-ant-api01-...` dan `sk-ant-admin01-...`; lihat [Kunci mana yang Anda perlukan?](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#which-key-do-you-need). Jika header dan kunci sudah benar dan satu path masih mengembalikan `Not found` sementara path lain berhasil, periksa path tersebut terhadap [referensi Compliance API](https://platform.claude.com/docs/id/api/compliance).

### Chat tidak ditemukan

**Type:** `not_found_error`

```text wrap
Chat conversation not found: 'claude_chat_01H5CWunD7RpVJ5bHa8RCkja'
```

**Penyebab:** ID chat di path tidak cocok dengan chat yang dapat dibaca melalui Compliance API. Chat tersebut mungkin telah dihapus permanen melalui panggilan Compliance API sebelumnya atau dihapus oleh kebijakan retensi organisasi Anda, atau mungkin milik organisasi yang tidak dapat dibaca oleh kunci pemanggil. Chat yang dihapus pengguna di claude.ai tidak mengembalikan 404; chat tersebut tetap dapat dibaca, dengan `deleted_at` terisi, tetapi tanpa konten pesannya.

**Perbaikan:** Konfirmasikan ID chat terhadap aktivitas `claude_chat_created` atau `claude_chat_viewed` terbaru. Jika aktivitasnya baru dan pembacaan masih gagal, chat tersebut telah dihapus permanen (melalui API ini atau karena kedaluwarsa kebijakan retensi) atau milik organisasi di luar cakupan kunci Anda.

### File tidak ditemukan

**Type:** `not_found_error`

```text wrap
File not found: 0d3b8f72-6c1e-4a59-b2de-7f4c9a1e5b60
```

**Penyebab:** ID file tidak ada di organisasi yang dapat dibaca oleh kunci Anda, atau file telah dihapus. Menghapus chat di claude.ai juga menghapus file yang dilampirkan padanya, meskipun chat itu sendiri tetap tercantum. Pesan mengidentifikasi file berdasarkan UUID dasarnya, bukan berdasarkan ID `claude_file_...` yang dikirim dalam permintaan. Endpoint metadata, konten, dan hapus mengembalikan body ini; body ini berlaku untuk file yang dilampirkan ke chat (`claude_file_...`) maupun file proyek.

**Perbaikan:** Rekonsiliasikan dengan aktivitas `claude_file_uploaded` atau `claude_file_deleted` terbaru. File yang dihapus bersama chat tidak memiliki aktivitas `claude_file_deleted`, jadi periksa juga aktivitas `claude_chat_deleted` untuk chat tersebut. Jika file telah dihapus, biner-nya sudah hilang; catatan aktivitas tetap ada di feed selama jangka waktu retensi 6 tahun.

### File yang dihasilkan atau artifact tidak ditemukan

**Type:** `not_found_error`

```text wrap
Generated file not found: 'claude_gen_file_01TbR8wAcCeFhJkLnPqStUvX'
```

```text wrap
Generated file content not found: 'claude_gen_file_01TbR8wAcCeFhJkLnPqStUvX'
```

```text wrap
Artifact version not found: 'claude_artifact_version_01KmNpQrSt3UvWxYz5AbCdEfG'
```

**Penyebab:** ID di path tidak cocok dengan file yang dihasilkan alat atau versi artifact yang dapat dibaca melalui Compliance API. Endpoint metadata file yang dihasilkan mengembalikan body pertama, endpoint konten mengembalikan body kedua, dan kedua endpoint artifact mengembalikan body ketiga. File yang dihasilkan dan artifact dihapus bersama chat tempat keduanya dibuat, termasuk ketika pengguna menghapus chat di claude.ai.

**Perbaikan:** Gunakan [Mendapatkan pesan chat](https://platform.claude.com/docs/id/api/compliance/apps/chats/messages/list) untuk mencari chat asal ID tersebut. Jika `deleted_at` chat terisi, atau aktivitas `claude_chat_deleted` menyebutkan chat tersebut, kontennya telah hilang; hapus ID dari antrean Anda. Jika tidak, konfirmasikan ID terhadap array `generated_files` dan `artifacts` pada pesan-pesan chat tersebut.

### Proyek tidak ditemukan

**Type:** `not_found_error`

```text wrap
No project is found with the provided id.
```

```text wrap
No project found with provided id, or it has already been deleted.
```

**Penyebab:** ID proyek tidak ada atau telah dihapus. Endpoint detail proyek, lampiran, dan kolaborator mengembalikan body pertama; `DELETE /v1/compliance/apps/projects/{project_id}` mengembalikan body kedua.

**Perbaikan:** Rekonsiliasikan dengan aktivitas `claude_project_created` atau `claude_project_deleted` terbaru. Activity Feed tetap menampilkan peristiwa siklus hidup proyek bahkan setelah proyek itu sendiri hilang.

### Dokumen proyek tidak ditemukan

**Type:** `not_found_error`

```text wrap
No project document found with the provided id.
```

```text wrap
No project document found with the provided id, or it has already been deleted.
```

**Penyebab:** ID dokumen proyek tidak ada atau telah dihapus. Endpoint konten dan metadata dokumen mengembalikan body pertama; `DELETE /v1/compliance/apps/projects/documents/{document_id}` mengembalikan body kedua. Error ini berlaku untuk dokumen proyek berupa teks (`claude_proj_doc_...`), bukan untuk file proyek.

**Perbaikan:** Gunakan `GET /v1/compliance/apps/projects/{project_id}/attachments` untuk mencantumkan lampiran saat ini. Jika dokumen tidak ada, dokumen tersebut telah dihapus; ambil melalui catatan aktivitas `claude_project_document_uploaded` jika Anda hanya memerlukan metadatanya. Catatan aktivitas menunjukkan siapa yang mengunggah dokumen, kapan, dan ke proyek mana, tetapi tidak menunjukkan namanya.

### Sesi lokal tidak ditemukan

**Type:** `not_found_error`

```text wrap
Local session not found.
```

**Penyebab:** ID sesi yang diteruskan ke `GET /v1/compliance/apps/sessions/local/{session_id}` atau `GET /v1/compliance/apps/sessions/local/{session_id}/messages` tidak cocok dengan sesi lokal yang dapat dibaca melalui Compliance API. Kedua endpoint mengembalikan satu pesan ini, tanpa membedakan penyebabnya, ketika ID bukan sesi di organisasi yang dapat dibaca oleh kunci Anda (termasuk ID milik organisasi induk lain), ketika sesi tidak pernah ada, ketika [zero data retention](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) berlaku untuk sesi tersebut, atau ketika seluruh aktivitas sesi telah melewati periode retensi yang berlaku untuk organisasi yang menjalankannya. Respons `Local session not found.` tidak memiliki bentuk sementara, karena sesi lokal tidak memiliki status penyediaan (`pending`); bandingkan dengan [Sesi jarak jauh tidak ditemukan](https://platform.claude.com/docs/id/manage-claude/compliance-errors#remote-session-not-found), di mana sesi `pending` mengembalikan 404 hingga sesi dimulai. ID sesi yang bukan pengenal `clls_` yang terbentuk dengan benar akan mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request) sebagai gantinya.

Endpoint sesi lokal, termasuk endpoint list, mengembalikan pesan 404 yang berbeda, `Local sessions are not available.`, selama endpoint itu sendiri tidak tersedia untuk organisasi induk Anda. Respons tersebut tidak bergantung pada ID sesi; tidak ada kunci, scope, atau pengaturan di sisi pelanggan yang dapat mengubahnya, dan respons tersebut dapat bersifat sementara. Kedua respons membawa type `not_found_error`; teks pesanlah yang membedakan keduanya.

**Perbaikan:** Konfirmasikan ID sesi terhadap `GET /v1/compliance/apps/sessions/local`; lihat [Sesi di mesin pengguna](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions). Jika sesi tidak lagi muncul di list, kontennya telah melewati masa retensi (atau sesi tersebut karena alasan lain tidak lagi berada di organisasi yang dapat dibaca oleh kunci Anda) dan transkripnya tidak dapat diambil; hapus ID dari antrean Anda. Jika setiap panggilan, termasuk list, mengembalikan `Local sessions are not available.`, simpan ID sesi yang ada di antrean Anda dan coba ulang pada eksekusi terjadwal berikutnya; jika respons tersebut terus muncul, hubungi perwakilan Anthropic Anda dan sertakan header respons `request-id`.

### Sesi jarak jauh tidak ditemukan

**Type:** `not_found_error`

```text wrap
Remote session not found.
```

**Penyebab:** ID sesi yang diteruskan ke `GET /v1/compliance/apps/sessions/remote/{session_id}/messages` tidak cocok dengan transkrip sesi yang dapat dibaca melalui Compliance API. Hal ini terjadi ketika ID sesi (`cse_...`) tidak ada atau sesi telah dihapus, ketika sesi milik organisasi yang tidak dapat dibaca oleh kunci Anda, atau ketika `status` sesi masih `pending`: sesi yang tertunda belum memiliki transkrip, sehingga endpoint messages mengembalikan 404 hingga sesi dimulai. ID sesi yang bukan pengenal `cse_` yang terbentuk dengan benar akan mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request) sebagai gantinya.

**Perbaikan:** Konfirmasikan ID sesi dan `status`-nya terhadap `GET /v1/compliance/apps/sessions/remote`; lihat [Sesi di cloud](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions). Jika sesi berstatus `pending`, coba ulang setelah sesi keluar dari status tersebut. Jika sesi tidak lagi muncul di list, sesi tersebut telah dihapus dan transkripnya tidak dapat diambil.

### Organisasi, peran, atau grup tidak ditemukan

**Type:** `not_found_error`

```text wrap
The "ce86b5f3-7c16-48b3-a9f3-e1d2c4b8a0f1" organization does not exist or the requester is not authorized to access it.
```

Endpoint organisasi, peran, dan grup mengembalikan 404 `not_found_error` dalam format error standar. Pesan organisasi menyebutkan `org_uuid`; pesan peran dan grup bersifat generik (`Role not found.`, `Group not found.`). Hal ini terjadi ketika ID path (`org_uuid`, `role_id`, atau `group_id`) tidak ada atau tidak lagi termasuk dalam hierarki yang dapat dibaca oleh kunci pemanggil.

**Penyebab:** ID di path tidak cocok dengan catatan yang dapat dibaca melalui Compliance API. Peran dan grup dapat dihapus, dan organisasi dapat dilepaskan tautannya dari hierarki induk.

**Perbaikan:** Verifikasi ID terhadap endpoint list yang sesuai, dan rekonsiliasikan dengan aktivitas organisasi, peran, atau grup terbaru di [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed).

### Pengaturan organisasi tidak tersedia

**Type:** `not_found_error`

```text wrap
organization `91012d09-e48b-438e-a489-1bebfd8fa6f9` not found in this organization's hierarchy
```

**Penyebab:** `GET /v1/compliance/organizations/{organization_id}/settings` mengembalikan 404 ini dalam tiga kasus yang sengaja menggunakan body yang sama agar respons tidak mengungkapkan apakah suatu organisasi ada: `organization_id` bukan salah satu organisasi yang tertaut ke induk Anda, nilainya bukan UUID yang valid, atau endpoint pengaturan belum diaktifkan untuk organisasi induk Anda.

**Perbaikan:** Verifikasi ID terhadap [Mencantumkan organisasi](https://platform.claude.com/docs/id/api/compliance/organizations/list). Jika ID organisasi yang diketahui benar masih mengembalikan 404, endpoint pengaturan belum diaktifkan untuk organisasi induk Anda; hubungi perwakilan Anthropic Anda.

## 409 Conflict

Permintaan terbentuk dengan benar dan terotorisasi, tetapi bertentangan dengan status sumber daya saat ini. Body membawa type `invalid_request_error`, yang juga digunakan oleh respons 400, jadi bedakan konflik berdasarkan kode status 409, bukan berdasarkan `error.type`.

### Proyek memiliki chat yang terlampir

**Type:** `invalid_request_error`

```text wrap
The "claude_proj_01KGp4eZNug9ri4kE35RSppq" project cannot be deleted as it has chats attached to it. Delete or detach all chats, and try deleting the project again.
```

**Penyebab:** `DELETE /v1/compliance/apps/projects/{project_id}` dipanggil pada proyek yang masih memiliki chat terlampir.

**Perbaikan:** Cantumkan chat proyek dengan `GET /v1/compliance/apps/chats?user_ids[]={user_id}&project_ids[]={project_id}` (filter `project_ids[]` memerlukan setidaknya satu nilai `user_ids[]`; enumerasikan ID melalui [Mencantumkan pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users)), hapus masing-masing dengan `DELETE /v1/compliance/apps/chats/{claude_chat_id}`, lalu coba ulang penghapusan proyek.

## 429 Too Many Requests

Permintaan ke Compliance API dibatasi hingga **600 permintaan per menit per [organisasi induk](https://platform.claude.com/docs/id/manage-claude/compliance-api#how-the-compliance-api-works)**. Batas ini adalah satu anggaran yang dibagi di antara setiap kunci di bawah induk (Compliance Access Key dan kunci Admin API dari semua organisasi yang tertaut) dan di antara setiap endpoint `/v1/compliance/*`; endpoint sesi jarak jauh membawa anggaran permintaan kedua sebagai tambahan. Untuk organisasi Claude Console mandiri, yang tidak memiliki organisasi induk, anggaran yang sama berlaku untuk organisasi itu sendiri dan dibagi di antara kunci Admin API-nya. Hubungi perwakilan Anthropic Anda jika integrasi Anda memerlukan batas yang lebih tinggi.

Setelah kunci API Anda berhasil diautentikasi, respons Compliance API melaporkan anggaran bersama melalui [header respons "rate limit" (batas laju)](https://platform.claude.com/docs/id/api/rate-limits#response-headers) standar sehingga klien Anda dapat melakukan throttling secara proaktif alih-alih menunggu 429:

* `anthropic-ratelimit-requests-limit` adalah anggaran permintaan per menit.
* `anthropic-ratelimit-requests-remaining` adalah sisa anggaran dalam jendela waktu saat ini.
* `anthropic-ratelimit-requests-reset` adalah timestamp RFC 3339 saat jendela waktu direset dan anggaran penuh dipulihkan.

Respons 429 juga membawa header `retry-after` dengan jumlah detik yang harus ditunggu sebelum mengirim permintaan berikutnya. Nilai ini mungkin menyertakan sedikit margin keamanan di luar `anthropic-ratelimit-requests-reset`; patuhi `retry-after`.

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

**Penyebab:** Organisasi induk Anda (atau organisasi Claude Console mandiri) mengirim lebih dari 600 permintaan ke `/v1/compliance/*` dalam jendela waktu 1 menit, di seluruh kunci yang berbagi anggarannya, atau telah menghabiskan anggaran permintaan kedua milik endpoint sesi jarak jauh (dijelaskan nanti di bagian ini).

**Perbaikan:** Tunggu selama jumlah detik di header `retry-after`, lalu coba ulang. Jika header tidak ada (misalnya, dihapus oleh perantara), gunakan "exponential backoff" (penundaan eksponensial) sebagai cadangan (mulai dari 1 detik, gandakan hingga 60 detik). Jangan majukan kursor paginasi Anda pada 429: permintaan yang gagal tidak mengembalikan data, sehingga kursor dari halaman terakhir yang berhasil masih benar.

Permintaan yang gagal autentikasi (kunci yang hilang atau tidak dikenali, atau kunci Claude API alih-alih Compliance Access Key atau kunci Admin API) ditolak sebelum pembatas laju dan tidak menghabiskan kuota. Kunci valid yang tidak memiliki scope yang diperlukan endpoint menghabiskan satu unit kuota sebelum 403 dikembalikan.

[Endpoint sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) hanya dihitung terhadap batas bersama. [Endpoint sesi jarak jauh](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-remote-sessions) juga membawa anggaran permintaan kedua, yang dikaitkan dengan organisasi induk Anda seperti batas bersama, sebagai tambahan dari batas tersebut. 429 dari anggaran tersebut membawa header `retry-after` yang selalu bernilai `1` (waktu tunggu minimum, bukan waktu reset sebenarnya); header `anthropic-ratelimit-*` apa pun pada respons tersebut menggambarkan batas bersama, bukan anggaran ini, jadi lakukan backoff secara eksponensial jika 429 terus berulang.

Jika Anda melakukan polling [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) secara terjadwal, anggarkan laju permintaan agregat Anda (di seluruh kunci, organisasi yang tertaut, dan worker yang berjalan bersamaan) di bawah batas bersama. Pantau `anthropic-ratelimit-requests-remaining` untuk memperlambat sebelum Anda mencapainya. Lihat [Merancang integrasi kepatuhan Anda](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#choose-a-feed-consumption-pattern) untuk memilih antara polling berbasis jendela waktu dan ingesti berbasis kursor.

## 500 Internal Server Error

500 dari Compliance API membawa header respons `x-should-retry: false` ketika kegagalannya bersifat deterministik. SDK Anthropic mematuhi header ini secara otomatis. Jika Anda menggunakan library retry HTTP generik yang mencoba ulang pada setiap 5xx, nonaktifkan percobaan ulang ketika `x-should-retry` bernilai `false`; mencoba ulang error ini akan gagal dengan cara yang sama pada setiap percobaan.

500 tanpa header `x-should-retry: false` bersifat sementara: coba ulang dengan exponential backoff (mulai dari 1 detik, gandakan hingga 60 detik). Hal yang sama berlaku untuk respons 502, 503, 504, dan 529. Pengecualiannya adalah sekumpulan kecil 503 sesi lokal, yang dijelaskan berikutnya, yang bergantung pada pengaturan organisasi atau kunci enkripsi, bukan pada beban. Lihat [Error](https://platform.claude.com/docs/id/api/errors) untuk semantik percobaan ulang yang berlaku di seluruh platform.

### Sesi lokal untuk sementara tidak tersedia

**Tipe:** `overloaded_error`

```text wrap
The local-sessions index is temporarily unavailable. Try again shortly.
```

```text wrap
Captured content is temporarily unavailable. Try again shortly.
```

```text wrap
The local-sessions index cannot currently evaluate retention overrides for this page. Try again later.
```

**Penyebab:** [Endpoint sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-sessions#retrieve-local-sessions) mengembalikan 503 dengan salah satu body berikut. Ketiganya memiliki tipe `overloaded_error` yang sama. Karena itu, ini adalah salah satu dari sedikit error di halaman ini yang mengharuskan Anda membaca teks pesan, bukan `error.type`, untuk membedakan kondisinya:

* Body `index is temporarily unavailable` berarti daftar sesi tidak tersedia untuk sementara karena beban atau kondisi backend. Kondisi ini bersifat sementara.
* Body `Captured content` berarti konten transkrip sebuah sesi tidak dapat dikembalikan saat ini. Kondisi ini biasanya juga bersifat sementara. Di organisasi yang menggunakan ["customer-managed encryption keys" (kunci enkripsi yang dikelola pelanggan)](https://platform.claude.com/docs/id/manage-claude/cmek), endpoint messages juga mengembalikan body ini untuk setiap halaman yang berisi konten yang tidak dapat didekripsi oleh kunci yang dikelola pelanggan milik Anda. Misalnya, Anda telah menonaktifkan, mencabut, atau menghancurkan kunci tersebut, atau kunci tersebut tidak dapat dijangkau. Dalam kasus ini, error akan terus muncul selama kunci tidak dapat digunakan. Teks pesannya sama dalam kedua kasus, sehingga satu-satunya tanda bahwa kunci adalah penyebabnya adalah error yang terus berulang untuk organisasi tersebut. Kunci yang tidak dapat digunakan tidak pernah dilaporkan sebagai `not_captured`.
* Body `retention overrides` berarti pengaturan "retention" (retensi) atau penanganan data yang berlaku untuk satu atau beberapa sesi dalam rentang yang diminta belum dapat dievaluasi. Pada endpoint retrieve dan messages, body ini berbunyi `for this session`, bukan `for this page`. Kondisi ini bergantung pada data dan pengaturan organisasi yang menjalankan sesi, bukan pada beban, dan dapat berlangsung dalam waktu yang lama.

**Perbaikan:** Tangani setiap body sebagai berikut:

* Untuk kedua body `Try again shortly.`, coba lagi dengan "exponential backoff" (backoff eksponensial) dan jangan majukan kursor `page` Anda, karena permintaan yang gagal tidak mengembalikan data apa pun.

* Jika body `Captured content` terus berulang pada endpoint messages untuk organisasi yang menggunakan kunci yang dikelola pelanggan, anggap kondisi ini persisten. Hentikan penelusuran transkrip organisasi tersebut dan periksa status kunci di "key management service" (layanan manajemen kunci) Anda. Transkrip di organisasi tertaut lainnya, serta metadata sesi di semua organisasi, tidak terpengaruh. Jika Anda mencoba lagi pada proses berikutnya, mulai ulang penelusuran setiap sesi tanpa `page`, karena kursor halaman messages kedaluwarsa 24 jam setelah halaman pertama penelusuran.

* Untuk body `Try again later.`, jangan biarkan penelusuran tetap terbuka sambil menunggu kondisi ini pulih. Pada endpoint list, Anda dapat memilih salah satu cara berikut:

  * Coba lagi nanti dengan memulai ulang tanpa parameter `page`. Token halaman list yang berusia lebih dari 24 jam masih diterima, tetapi dievaluasi ulang terhadap batas retensi saat ini, sehingga penelusuran yang ditunda dapat melewatkan sesi.
  * Persempit jendela `created_at.gte` dan `created_at.lt` hingga permintaan berhasil, lalu ekspor rentang yang terlewat secara terpisah pada proses berikutnya.

  Pada endpoint retrieve dan messages, lewati ID sesi tersebut, lanjutkan sisa ekspor Anda, dan coba lagi sesi tersebut pada proses berikutnya. Kursor halaman messages kedaluwarsa 24 jam setelah halaman pertama penelusuran, jadi mulai ulang penelusuran sesi tersebut tanpa `page` saat Anda kembali ke sesi itu.

Jika salah satu kondisi ini terus berulang di beberapa proses, hubungi perwakilan Anthropic Anda dan sertakan header respons `request-id`. Untuk kasus kunci yang dikelola pelanggan, lakukan ini hanya jika error terus muncul saat kunci tersebut dapat digunakan.

Untuk insiden yang memengaruhi seluruh layanan, periksa [status.anthropic.com](https://status.anthropic.com).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="FAQ Compliance API" href="https://platform.claude.com/docs/id/manage-claude/compliance-faq">
    Pertanyaan umum tentang akses, cakupan, retensi, dan integrasi.
  </Card>

  <Card title="Error" href="https://platform.claude.com/docs/id/api/errors">
    Katalog error untuk seluruh platform dan semantik percobaan ulang.
  </Card>
</CardGroup>
