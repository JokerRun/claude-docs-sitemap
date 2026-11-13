---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 8f34d374979f9f995f1ca20f3de30e8d46f531806408080d2af6aa3cc26d7929
---

---
title: Referensi hasil Security posture
url: https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference
description: "Cari endpoint Compliance API yang mengembalikan hasil Security posture terkini suatu organisasi: permintaan, field respons, arti setiap status, dan error-nya."
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

Endpoint ini mengembalikan satu entri untuk masing-masing dari sebagian besar kontrol keamanan milik suatu organisasi, yang dievaluasi pada saat permintaan. Field `attestation` pada setiap entri berisi [atestasi Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#attestations) milik kontrol tersebut atau `null`. Nilai `null` tidak membuktikan bahwa tidak ada yang mengatestasi: [Bagaimana atestasi ditampilkan dalam respons](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference#how-an-attestation-shows-in-the-response) mencantumkan atestasi mana yang ditampilkan respons. Anda memerlukan Compliance Access Key yang mencakup organisasi tersebut, dengan scope `read:compliance_org_data` atau `read:org_audit`. [Ketersediaan Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#availability) menjelaskan organisasi mana yang dapat dibaca.

## Permintaan

Kirim permintaan `GET` ke `/v1/compliance/organizations/{organization_id}/security_posture`. Setiap panggilan membaca satu organisasi, dan respons tidak dipaginasi.

```bash cURL
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/organizations/91012d09-e48b-438e-a489-1bebfd8fa6f9/security_posture" \
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  -H "anthropic-version: 2026-10-21"
```

| Item                | Aturan                                                                                                                                                                                                                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `organization_id`   | `uuid` dari [organisasi tertaut](https://platform.claude.com/docs/id/manage-claude/compliance-api#how-the-compliance-api-works) dari [Daftar organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organizations); nilai lain mana pun mengembalikan 404. |
| Kunci               | [Kunci untuk organisasi induk](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) dapat menyebut organisasi tertaut mana pun, dan kunci untuk satu organisasi hanya dapat menyebut organisasi tersebut.                                    |
| `anthropic-version` | Wajib; permintaan tanpanya mengembalikan 400.                                                                                                                                                                                                                                              |
| Parameter kueri     | Tidak ada; permintaan dengan parameter kueri mana pun mengembalikan 400.                                                                                                                                                                                                                   |

## Respons

Contoh ringkas berikut menampilkan empat dari kontrol yang dapat dimuat dalam respons. Ini adalah respons untuk kunci yang memiliki `read:compliance_org_data` dan `read:compliance_user_data`.

```json Response
{
  "type": "security_posture",
  "organization_id": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
  "evaluated_at": "2027-02-09T09:00:02.417305Z",
  "comments_status": "not_enabled",
  "controls": [
    {
      "id": "sso_enabled",
      "display_name": "Single sign-on (SSO)",
      "section": "identity_access",
      "setting_name": "sso_enabled",
      "status": "passed",
      "rating": "passed",
      "current_value": "On",
      "desired_state": "On",
      "attestation": null
    },
    {
      "id": "directory_sync_enabled",
      "display_name": "Directory sync (SCIM)",
      "section": "identity_access",
      "setting_name": "directory_sync_enabled",
      "status": "failed_check_accepted_risk",
      "rating": "passed",
      "current_value": "Off",
      "desired_state": "On",
      "attestation": {
        "state": "in_force",
        "attested_at": "2026-10-20T15:04:00.220114Z",
        "comment": null,
        "attested_by": {
          "type": "user_actor",
          "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu"
        }
      }
    },
    {
      "id": "allowed_invite_domains",
      "display_name": "Allowed email domains",
      "section": "identity_access",
      "setting_name": "allowed_invite_domains",
      "status": "descriptive",
      "rating": "descriptive",
      "current_value": "example.com",
      "desired_state": null,
      "attestation": null
    },
    {
      "id": "oauth_conditional_access",
      "display_name": "OAuth conditional access on connected SaaS",
      "section": "connectors_integrations",
      "setting_name": null,
      "status": "not_attested",
      "rating": "not_attested",
      "current_value": null,
      "desired_state": "Completed",
      "attestation": {
        "state": "review_due",
        "attested_at": "2026-11-02T09:30:00.008771Z",
        "comment": null,
        "attested_by": {
          "type": "user_actor",
          "user_id": "user_01AbCdEfGhJkLmNpQrStUvWx"
        }
      }
    }
  ]
}
```

Setiap field selalu ada, dan field tanpa nilai bernilai `null`; field tersebut tidak pernah dihilangkan. Nilai waktu memiliki nol atau enam digit pecahan, jadi bandingkan waktu sebagai waktu, bukan sebagai string.

### Field tingkat atas

| Field             | Tipe                   | Deskripsi                                                                                                                                                                                                  |
| ----------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`            | string                 | Selalu `security_posture`.                                                                                                                                                                                 |
| `organization_id` | string                 | UUID organisasi.                                                                                                                                                                                           |
| `evaluated_at`    | string (RFC 3339, UTC) | Waktu saat setiap kontrol dievaluasi.                                                                                                                                                                      |
| `comments_status` | string                 | Apakah komentar atestasi dibaca; lihat [Siapa yang mengatestasi, dan komentar](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference#who-attested-and-comments). |
| `controls`        | array objek            | Kontrol-kontrol organisasi; array ini tidak pernah kosong.                                                                                                                                                 |

### Field `controls[]`

| Field           | Tipe             | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                     |
| --------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`            | string           | Pengidentifikasi kontrol, yang sama untuk setiap organisasi dan tidak pernah berubah.                                                                                                                                                                                                                                                                                                         |
| `display_name`  | string           | Nama tampilan kontrol, berupa teks tampilan dalam bahasa Inggris yang kata-katanya dapat berubah.                                                                                                                                                                                                                                                                                             |
| `section`       | string           | Bagian tempat kontrol ini berada, salah satu dari 10 bagian yang dicantumkan setelah tabel ini; nilai lain dapat ditambahkan, jadi perlakukan nilai yang tidak dikenal sebagai bagian tersendiri.                                                                                                                                                                                             |
| `setting_name`  | string atau null | `name` dari entri dalam pengaturan efektif organisasi yang dibaca kontrol ini; `null` jika kontrol tidak membaca entri semacam itu.                                                                                                                                                                                                                                                           |
| `status`        | string           | Alasan hasil kontrol; lihat [Nilai status](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference#status-values).                                                                                                                                                                                                                                    |
| `rating`        | string           | Hasil kontrol, yang mengikuti dari `status`; lihat [Nilai status](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference#status-values).                                                                                                                                                                                                             |
| `current_value` | string atau null | Nilai saat ini, berupa teks tampilan dalam bahasa Inggris yang kata-katanya dapat berubah; `null` pada kontrol manual atau jika tidak ada nilai yang dibaca.                                                                                                                                                                                                                                  |
| `desired_state` | string atau null | Nilai yang direkomendasikan, berupa teks tampilan dalam bahasa Inggris yang kata-katanya dapat berubah; `null` jika tidak ada untuk organisasi ini.                                                                                                                                                                                                                                           |
| `attestation`   | objek atau null  | Atestasi yang respons tampilkan, juga selama atestasi tersebut tidak berlaku; `null` selama `status` bernilai `descriptive`, `not_applicable`, atau `not_evaluated`, dan dalam kasus-kasus di bawah [Bagaimana atestasi ditampilkan dalam respons](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference#how-an-attestation-shows-in-the-response). |

`section` adalah salah satu dari `identity_access`, `data_privacy`, `capabilities`, `connectors_integrations`, `chats_desktop_mdm`, `cowork_admin_console`, `cowork_desktop_mdm`, `claude_code_admin_console`, `claude_code_managed_settings`, dan `healthy_adoption`.

Untuk membandingkan nilai dalam kode, cari `setting_name` di [pengaturan efektif](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#get-effective-organization-settings) organisasi yang sama. Pencarian ini bisa tidak menemukan apa pun, dan dua kontrol dapat berbagi satu `setting_name`.

### Field `attestation`

| Field         | Tipe                   | Deskripsi                                                                                                                                                                                                                                                         |
| ------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `state`       | string                 | Apakah atestasi berlaku; lihat [Keadaan atestasi](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference#attestation-states).                                                                                            |
| `attested_at` | string (RFC 3339, UTC) | Waktu atestasi dibuat.                                                                                                                                                                                                                                            |
| `comment`     | string atau null       | Komentar yang disimpan bersama atestasi, paling banyak 2.000 karakter; `null` jika tidak ada, atau jika `comments_status` bukan `available`.                                                                                                                      |
| `attested_by` | objek atau null        | Orang yang mengatestasi; `null` jika kunci tidak memiliki `read:compliance_user_data` maupun `read:org_audit`, jika akun orang tersebut telah dihapus atau sedang dihapus, atau jika, untuk organisasi ini, endpoint tidak mengembalikan siapa yang mengatestasi. |

### Field `attested_by`

| Field     | Tipe   | Deskripsi                                 |
| --------- | ------ | ----------------------------------------- |
| `type`    | string | Selalu `user_actor`.                      |
| `user_id` | string | ID pengguna, yang diawali dengan `user_`. |

## Nilai status

`status` memberikan alasan hasil suatu kontrol, dan setiap status memiliki satu `rating`.

| `status`                     | Jenis kontrol        | Arti                                                                                                                         | `rating`       | Di halaman                                             |
| ---------------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------------------------ |
| `passed`                     | otomatis             | Nilai saat ini memenuhi nilai yang direkomendasikan.                                                                         | `passed`       | Lulus                                                  |
| `matches_profile`            | otomatis             | Nilai saat ini sama dengan nilai yang direkomendasikan.                                                                      | `passed`       | Lulus                                                  |
| `exceeds_baseline`           | otomatis             | Nilai saat ini lebih ketat daripada nilai yang direkomendasikan.                                                             | `passed`       | Lulus                                                  |
| `failed_check_accepted_risk` | otomatis             | Pemeriksaan otomatis tidak berhasil, dan risiko diterima berlaku.                                                            | `passed`       | Lulus                                                  |
| `failed`                     | otomatis atau manual | Nilai saat ini tidak memenuhi nilai yang direkomendasikan, atau atestasi yang dihilangkan dari respons memberikan hasil ini. | `failed`       | Gagal, atau Lulus dengan atestasi Selesai yang berlaku |
| `review`                     | otomatis             | Nilai saat ini lebih longgar daripada nilai yang direkomendasikan.                                                           | `failed`       | Gagal                                                  |
| `attested_completed`         | manual               | Atestasi dengan nilai Selesai (`completed`) berlaku.                                                                         | `passed`       | Lulus                                                  |
| `attested_accepted_risk`     | manual               | Atestasi dengan nilai Risiko diterima (`accepted_risk`) berlaku.                                                             | `passed`       | Lulus                                                  |
| `not_attested`               | manual               | Tidak ada atestasi yang berlaku.                                                                                             | `not_attested` | Belum diatestasi                                       |
| `attestation_not_enabled`    | manual               | Tidak ada yang dapat mengatestasi kontrol ini.                                                                               | `not_attested` | Deskriptif                                             |
| `descriptive`                | khusus informasi     | Kontrol ini dilaporkan, tidak diberi hasil.                                                                                  | `descriptive`  | Deskriptif                                             |
| `not_applicable`             | mana pun             | Kontrol ini tidak berlaku bagi organisasi.                                                                                   | `descriptive`  | Deskriptif                                             |
| `not_evaluated`              | mana pun             | Pengaturan, atau pengaturan lain yang menentukan apakah kontrol berlaku, tidak dapat dibaca.                                 | `descriptive`  | Deskriptif                                             |

Tidak ada field yang menyebutkan jenis kontrol; untuk `failed`, `current_value` yang bernilai `null` menandakan kontrol manual. Nilai lain dapat ditambahkan, jadi hitung kontrol dengan `status` yang tidak dikenal berdasarkan `rating`-nya, dan anggap `rating` yang tidak dikenal sebagai tidak Lulus. Status `review` dan keadaan atestasi `review_due` tidak berkaitan.

## Keadaan atestasi

`state` menyatakan apakah atestasi yang respons tampilkan berlaku.

| `state`           | Arti                                                                                                                                      |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `in_force`        | Atestasi berlaku.                                                                                                                         |
| `review_due`      | Tanggal berakhir telah tiba.                                                                                                              |
| `setting_changed` | Pemeriksaan tidak berhasil pada nilai selain nilai yang risikonya diterima, atau risiko diterima sudah tercatat sebagai berhenti berlaku. |
| `check_passing`   | Pemeriksaan berhasil, jadi tidak ada risiko yang perlu diterima.                                                                          |

Jika lebih dari satu alasan berlaku, respons memberikan yang pertama dari `check_passing`, `setting_changed`, dan `review_due`. Sejak pukul 00.00 UTC pada tanggal berakhirnya, atestasi tidak berlaku. Respons tidak memuat tanggal berakhir, jadi `state` yang menentukan; tanggal berakhir yang tersimpan adalah [`review_date`](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference#attestation-activity) milik aktivitas atestasi. Anggap `state` yang tidak dikenal sebagai tidak berlaku.

## Bagaimana atestasi ditampilkan dalam respons

Respons menampilkan sebagian atestasi dan menghilangkan yang lain, jadi `attestation` yang bernilai `null` tidak membuktikan bahwa tidak ada yang mengatestasi.

| Jenis kontrol                           | Diatestasi sebagai                              | `status`                                                                              | `rating`                    | `attestation`                                               |
| --------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------- | --------------------------- | ----------------------------------------------------------- |
| Manual                                  | Tanpa atestasi                                  | `not_attested`, atau `attestation_not_enabled` jika tidak ada yang dapat mengatestasi | `not_attested`              | `null`                                                      |
| Manual                                  | Selesai                                         | `attested_completed`                                                                  | `passed`                    | Ditampilkan                                                 |
| Manual                                  | Risiko diterima                                 | `attested_accepted_risk`                                                              | `passed`                    | Ditampilkan                                                 |
| Manual                                  | Gagal (`control_failed`)                        | `failed`                                                                              | `failed`                    | `null`: tidak pernah ditampilkan                            |
| Otomatis, pemeriksaan tidak berhasil    | Tanpa atestasi                                  | `failed` atau `review`                                                                | `failed`                    | `null`                                                      |
| Otomatis, pemeriksaan tidak berhasil    | Risiko diterima                                 | `failed_check_accepted_risk`                                                          | `passed`                    | Ditampilkan                                                 |
| Otomatis, pemeriksaan tidak berhasil    | Selesai                                         | `failed`, bahkan jika pemeriksaan otomatis memberikan `review`                        | `failed`                    | `null`: tidak pernah ditampilkan                            |
| Otomatis, pemeriksaan tidak berhasil    | Gagal                                           | `status` yang diberikan pemeriksaan otomatis                                          | `failed`                    | `null`: tidak pernah ditampilkan                            |
| Otomatis, pemeriksaan berhasil          | Tanpa atestasi                                  | `passed`, `matches_profile`, atau `exceeds_baseline`                                  | `passed`                    | `null`                                                      |
| Otomatis, pemeriksaan berhasil          | Selesai                                         | `status` yang diberikan pemeriksaan otomatis                                          | `passed`                    | `null`: tidak pernah ditampilkan                            |
| Otomatis, pemeriksaan berhasil          | Risiko diterima                                 | `status` yang diberikan pemeriksaan otomatis                                          | `passed`                    | `null` selama pemeriksaan berhasil pada nilai yang diterima |
| Otomatis, pemeriksaan berhasil          | Gagal                                           | `failed`                                                                              | `failed`                    | `null`: tidak pernah ditampilkan                            |
| Khusus informasi                        | Nilai apa pun                                   | `descriptive`                                                                         | `descriptive`               | `null`: tidak pernah ditampilkan                            |
| Mana pun, selama atestasi tidak berlaku | Nilai yang ditampilkan menurut baris sebelumnya | Sama seperti tanpa atestasi                                                           | Sama seperti tanpa atestasi | Ditampilkan, dengan `state` selain `in_force`               |
| Mana pun, selama atestasi tidak berlaku | Nilai yang dihilangkan oleh baris sebelumnya    | Sama seperti tanpa atestasi                                                           | Sama seperti tanpa atestasi | `null`                                                      |

Setiap baris kecuali dua baris terakhir berlaku selama atestasi masih berlaku. Pada kontrol otomatis, atestasi tidak berlaku selama nilai yang dibaca pemeriksaan berbeda dari nilai saat atestasi tersebut disimpan. Setiap atestasi yang respons tampilkan pada kontrol otomatis adalah risiko diterima. [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) juga mencatat atestasi dari jenis-jenis yang dihilangkan dari respons.

## Menghitung hasil

Periksa empat hal saat Anda menghitung kontrol berdasarkan `rating`.

| Jika Anda menghitung       | Periksa juga                                                                                                                                                                                                         |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lulus (`passed`)           | Ini mencakup setiap kontrol dengan risiko diterima yang berlaku, jadi cari `failed_check_accepted_risk` dan `attested_accepted_risk`.                                                                                |
| Gagal (`failed`)           | Ini mencakup kontrol yang diatestasi sebagai Gagal (`control_failed`), serta pemeriksaan otomatis yang tidak berhasil dengan atestasi Selesai yang berlaku, yang ditampilkan halaman Security posture sebagai Lulus. |
| Deskriptif (`descriptive`) | Ini dapat menyembunyikan kontrol yang tidak dapat dibaca, jadi cari `not_evaluated`.                                                                                                                                 |
| Setiap kontrol             | Kontrol yang tidak ada dalam respons tidak dianggap Lulus dan tidak disebutkan, jadi bandingkan nilai `id` dengan nilai yang pernah Anda lihat untuk organisasi tersebut.                                            |

## Siapa yang mengatestasi, dan komentar

`attested_by` hanya diisi untuk kunci yang memiliki `read:compliance_user_data` bersama `read:compliance_org_data`, atau yang memiliki `read:org_audit`. Kunci yang hanya memiliki `read:compliance_user_data` mendapat 403. `user_id` di `attested_by` sama dengan `user_id` milik `actor` pada aktivitas atestasi. `attested_by` hanya berisi ID pengguna: [Daftar pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users) memberikan nama dan alamat email setiap anggota saat ini. Sebelum Anda menambahkan scope ini, lihat [Siapa yang dapat melihat siapa yang melakukan atestasi](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#who-can-see-who-attested).

Endpoint ini tidak mengembalikan komentar, bahkan ketika halaman Security posture menampilkannya: setiap `comment` bernilai `null`, dan `comments_status` bernilai `not_enabled` atau `not_permitted`. Jadi, `not_enabled` dan komentar yang bernilai `null` tidak berarti atestasi tersebut tidak memiliki komentar. `comments_status` menjelaskan cara membaca komentar yang bernilai `null`, dan skema mendefinisikan nilai berikut.

| `comments_status`           | Arti                                                                                                                                                             |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `not_permitted`             | Kunci API tidak memiliki `read:compliance_user_data` maupun `read:org_audit`, jadi setiap `comment` dan setiap `attested_by` bernilai `null`.                    |
| `requires_organization_key` | Kunci API tidak dibuat di organisasi tersebut, seperti halnya kunci untuk organisasi induk, jadi setiap `comment` bernilai `null`. Mencoba lagi tidak membantu.  |
| `available`                 | Komentar telah dibaca, jadi komentar yang bernilai `null` berarti tidak ada komentar, atau komentar tersebut baru disimpan beberapa saat lalu.                   |
| `not_enabled`               | Endpoint ini tidak mengembalikan komentar untuk organisasi ini, jadi setiap `comment` bernilai `null`.                                                           |
| `unavailable`               | Komentar tidak dapat dibaca untuk respons ini; permintaan berikutnya mungkin berhasil, tetapi beberapa penyebab berlangsung hingga pelanggan mengambil tindakan. |

Nilai lain dapat ditambahkan; anggap nilai yang tidak dikenal sebagai `unavailable`.

## Error

Error menggunakan body yang sama seperti bagian lain dari Compliance API. [Menangani error Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-errors) menjelaskan body tersebut. Tabel ini mencantumkan error yang dikembalikan endpoint ini dengan caranya sendiri.

| Status dan `error.type`                                                                        | Kapan                                                                                                                                  | Yang harus dilakukan                                                                                                                                   |
| ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 400 `invalid_request_error`                                                                    | `anthropic-version` tidak ada atau tidak valid, Compliance API tidak diaktifkan untuk organisasi induk, atau terdapat parameter kueri. | Perbaiki hal yang disebutkan `error.message`.                                                                                                          |
| 401 `authentication_error`                                                                     | Kunci tidak ada, tidak dikenali, atau bukan Compliance Access Key maupun kunci Admin API.                                              | Kirim Compliance Access Key yang valid di `x-api-key`.                                                                                                 |
| 403 `permission_error`                                                                         | Kunci tidak boleh memanggil endpoint ini, biasanya karena tidak memiliki `read:compliance_org_data` maupun `read:org_audit`.           | Gunakan kunci dengan salah satu scope tersebut.                                                                                                        |
| 404 `not_found_error`                                                                          | Lihat penyebab yang tercantum setelah tabel ini.                                                                                       | Jangan langsung mencoba ulang. 404 tidak berarti organisasi tersebut tidak memiliki kontrol yang gagal.                                                |
| 429 `rate_limit_error`                                                                         | Batas laju bersama Compliance API, atau batas endpoint ini yang lebih rendah, telah habis; `error.message` menyebutkan yang mana.      | Tunggu sesuai `retry-after`; lihat [429 Too Many Requests](https://platform.claude.com/docs/id/manage-claude/compliance-errors#429-too-many-requests). |
| 503 `overloaded_error`, dengan `error.details.error_code` bernilai `posture_evaluation_failed` | Hasil tidak dapat dihasilkan.                                                                                                          | Tunggu sesuai `retry-after`, lalu coba lagi; jika berulang untuk satu organisasi pada eksekusi berikutnya, hubungi dukungan Anthropic satu kali.       |
| 503 tanpa `error_code`, atau 504 `timeout_error`                                               | Kegagalan sementara.                                                                                                                   | Coba lagi dengan exponential backoff.                                                                                                                  |

Penyebab 404:

* `organization_id` bukan UUID, tidak merujuk ke organisasi mana pun, atau merujuk ke organisasi yang telah dihapus.
* `organization_id` merujuk ke organisasi induk, organisasi di bawah induk lain, atau organisasi yang tidak dicakup oleh kunci organisasi tunggal.
* Organisasi tidak menggunakan Claude Enterprise, atau Security posture tidak tersedia untuknya, seperti pada organisasi Claude Console.
* Halaman Security posture telah dinonaktifkan untuk organisasi (lihat [Ketersediaan Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#availability)).
* Security posture tersedia untuk organisasi, tetapi endpoint tidak melayaninya.
* Ketersediaan tidak dapat diperiksa; permintaan berikutnya dapat berhasil.

Setiap 404 memiliki body yang sama, begitu pula path yang tidak ada.

## Kesegaran data dan efek samping

Endpoint ini mengevaluasi setiap kontrol saat Anda memanggilnya, dan `evaluated_at` adalah waktu tersebut.

* Perubahan dari beberapa menit terakhir mungkin belum terlihat.
* Hasil dapat berubah tanpa ada pengaturan yang berubah, misalnya ketika tanggal berakhir tiba atau Anthropic mengubah nilai yang direkomendasikan.
* Jika Anthropic mengubah kata-kata suatu nilai saat ini, risiko diterima pada nilai tersebut tidak berlaku.
* Panggilan tidak menyimpan hasil apa pun dan tidak membuat atestasi apa pun berhenti berlaku.
* Permintaan dengan kunci untuk organisasi induk maupun kunci untuk satu organisasi di Claude Enterprise mencatat satu aktivitas `compliance_api_accessed`. Aktivitas ini dicatat ketika permintaan lolos pemeriksaan kunci, scope, dan versi tanpa parameter kueri, baik berhasil maupun gagal. `url` milik aktivitas tersebut menyebutkan organisasi yang dibaca, dan `organization_uuid` bernilai `null` untuk kunci untuk organisasi induk.
