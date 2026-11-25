---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 9e8a22a48bb546c6fa06665c35826357b36c6cdaf818175532fbde95791a30f9
---

---
title: API Safety Cases
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api
description: Cantumkan, baca, dan tanggapi Safety Cases melalui HTTP dengan Compliance API.
---

API Safety Cases menyajikan Safety Cases melalui HTTP. API ini sedang dalam beta. Anda dapat memilih [bucket kasus](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/faq#glossary) untuk setiap workspace di bawah **Safety Case and Transcript storage**. Tanpa bucket, Anda tidak mendapatkan Safety Cases untuk pesan dengan profil pengguna. API ini merupakan bagian dari [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api), dan hanya tersedia di Claude Platform. Untuk mempelajari cara tim Anda meninjau dan menanggapi Safety Case, lihat [Tinjau Safety Cases](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases).

<Warning>
  Enterprise Frontier Safeguards saat ini dalam tahap beta. Fitur ini tersedia berdasarkan perjanjian Anda dengan Anthropic, seperti ketentuan khusus penggunaan internal, [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Pengaturan dan perilaku dapat berubah selama beta.
</Warning>

## Dapatkan akses

Untuk mendapatkan akses ke API Safety Cases:

1. **Aktifkan Compliance API.** Compliance API harus aktif untuk organisasi Anda. Jika nonaktif, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#set-up-the-compliance-api) untuk mengaktifkannya.
2. **Buat kunci Admin API.** Sebagai admin organisasi, buat [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-console-organization) di Claude Console. Tidak ada scope yang perlu dipilih. Kunci Admin API mendapatkan akses ke API Safety Cases hanya jika Anda membuatnya saat API tersebut tersedia untuk organisasi Anda. Kunci Admin API yang Anda buat sebelumnya tidak akan pernah mendapatkan akses ini. Jika Anda menonaktifkan Compliance API, API Safety Cases menolak permintaan kunci Anda dengan error 400.

Untuk menguji kunci tersebut, [tampilkan daftar Safety Cases Anda](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#poll) dengan kunci tersebut:

| Respons | Artinya dan yang perlu dilakukan |
| ----- | ----- |
| 200, bahkan dengan daftar kosong | Kunci Anda dapat menampilkan daftar Safety Cases. Anda hanya mendapatkan Safety Cases untuk workspace tanpa Anthropic Human Review. |
| 401, 403, atau 404 | Kunci Anda tidak dapat menampilkan daftar Safety Cases. Periksa bahwa Anda mengirimkan kunci tersebut secara utuh, lalu buat kunci Admin API lain dan coba lagi. |
| 403 atau 404 dengan kunci baru | API tidak tersedia untuk organisasi Anda. |

Hapus kunci Admin API yang tidak Anda perlukan.

Kunci tersebut hanya menjangkau Safety Cases dan pesan milik organisasinya sendiri, bahkan di bawah organisasi induk. Kunci ini adalah kunci Admin API penuh. Selama API tersedia untuk organisasi Anda, setiap kunci Admin API yang Anda buat mendapatkan akses ini. Karena itu, batasi siapa yang dapat membuat dan memegang kunci-kunci ini. Kunci milik organisasi uji tidak mendapatkan akses ini.

Kunci tersebut mendapatkan ketiga scope berikut:

| Scope | Yang diizinkan |
| ----- | ----- |
| `read:compliance_review_cases` | Mencantumkan dan membaca Safety Cases serta Safety Notices, yang tidak pernah memuat prompt atau respons suatu pesan. |
| `read:compliance_review_items` | Membaca prompt, respons, dan pengirim pesan yang ditandai. |
| `write:compliance_review_cases` | Menanggapi Safety Case. |

Kunci lain juga dapat membaca data ini:

* **Safety Cases dan Safety Notices:** Di tempat API tersedia, kunci dengan [`read:org_audit`](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#choose-scopes-for-a-claude-enterprise-key) hanya dapat membaca Safety Cases dan Safety Notices milik organisasinya sendiri. Kunci tersebut hanya dapat melakukannya jika organisasi tersebut memiliki organisasi induk.
* **Pesan yang ditandai:** Di beberapa organisasi, kunci dengan `read:org_audit` juga dapat membaca pesan yang ditandai, begitu pula kunci dengan `read:compliance_user_data`. Beberapa kunci ini menjangkau pesan yang ditandai dari setiap organisasi di bawah organisasi induknya.

Kirimkan header [`anthropic-version`](https://platform.claude.com/docs/id/api/versioning) pada setiap permintaan. Permintaan tanpa header tersebut dapat mengembalikan error 400. Setelah error 429 atau 503, coba lagi permintaan tersebut nanti.

## Polling untuk Safety Cases

Periksa API Safety Cases secara berkala untuk Safety Cases baru, agar Anda dapat menanggapinya dengan segera.

Pada eksekusi pertama Anda, jangan sertakan `updated_at[gte]`. Kemudian, simpan `updated_at` terbesar yang telah Anda baca, dan kirimkan sebagai `updated_at[gte]` pada eksekusi berikutnya:

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/review/cases" \
  --data-urlencode "updated_at[gte]=2026-11-23T18:15:34Z" \
  -d "order_by=updated_at" \
  -d "order=asc" \
  -d "limit=100" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2026-10-21"
```

```json Response
{
  "data": [
    {
      "type": "compliance_review_case",
      "id": "rvc_01Hq3Zt8KpWv5NcR2yLbXs7D",
      "organization_id": "abcdef01-2345-6789-abcd-ef0123456789",
      "status": { "type": "open" },
      "created_at": "2026-11-23T18:42:07.106255Z",
      "updated_at": "2026-11-23T18:42:07.106255Z",
      "workspace_id": "wrkspc_01AbCdEfGhJkLmNpQrStUvWx",
      "policy_categories": ["cyber"],
      "enforcement_action": null,
      "transcripts": [
        {
          "item_id": "msg_01XFDUDYJgAACzvnptvVoYEL",
          "user_profile_id": null
        }
      ]
    }
  ],
  "next_page": null
}
```

Permintaan ini mengembalikan Safety Cases yang dibuka, ditutup, atau mendapatkan Safety Notice sejak waktu tersebut. Untuk membaca satu Safety Case, kirimkan `GET /v1/compliance/review/cases/{case_id}`.

Ikuti rekomendasi berikut saat Anda membangun tugas polling:

* **Baca setiap halaman.** Untuk membaca halaman berikutnya, kirimkan `next_page` sebagai `page` hingga permintaan mengembalikan `next_page` sebagai `null`. Halaman dapat berisi sedikit item atau kosong meskipun `next_page` diatur.
* **Jangan simpan `next_page` di antara eksekusi.** Nilai ini hanya berfungsi dalam satu hasil daftar, dan API menolaknya dengan error 400 jika filter atau urutannya berbeda.
* **Perbarui salinan setiap Safety Case Anda berdasarkan `id`.** API juga mengembalikan Safety Cases yang sedikit lebih lama dari waktu yang Anda kirimkan, dan mengembalikannya lagi ketika Safety Case ditutup atau mendapatkan Safety Notice.
* **Filter berdasarkan `updated_at`, bukan `created_at`.** Filter berdasarkan `created_at` akan melewatkan Safety Case yang ditutup atau mendapatkan Safety Notice setelah Anda pertama kali membacanya, dan dapat melewatkan Safety Case baru.

Safety Case yang ditutup memiliki `status.type` yang diatur ke `closed`, dan `status.reason.type` menyebutkan alasannya:

| `status.reason.type` | Artinya |
| ----- | ----- |
| `responded` | Anthropic telah menerima tanggapan Anda. |
| `window_ended` | Anthropic tidak menerima tanggapan yang valid dalam 7 hari kalender sejak `created_at`. |
| `ended_by_anthropic` | Anthropic mengakhiri Safety Case sebelum itu. |

Anthropic dapat menambahkan field, nilai `policy_categories`, tipe `enforcement_action`, dan alasan penutupan, jadi terimalah nilai yang tidak Anda kenali.

### Polling untuk Safety Notices

Safety Notice adalah pesan dari Anthropic tentang satu atau beberapa Safety Cases Anda, atau tentang organisasi Anda secara keseluruhan. Safety Notice dapat meminta jawaban sebelum waktu tertentu. `kind.type`-nya menyebutkan jenis Safety Notice tersebut:

| `kind.type` | Artinya |
| ----- | ----- |
| `response_requested` | Permintaan untuk menanggapi. Untuk menjawab, [tanggapi Safety Case](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#respond). |
| `warning` | Peringatan. |
| `question` | Pertanyaan. Untuk menjawab, hubungi tim akun Anthropic Anda. |

Anthropic dapat menambahkan jenis lain, jadi terimalah jenis yang tidak Anda kenali. Jangan mengandalkan Safety Notice untuk mengingatkan Anda tentang Safety Case yang masih terbuka: Safety Case yang tidak memiliki file di bucket kasus Anda tidak mendapatkan pengingat otomatis.

Untuk membaca Safety Notices, lakukan polling ke `GET /v1/compliance/review/notices`:

* **Kirimkan `created_at[gte]` dan `order=asc`,** lalu simpan `created_at` terbesar yang telah Anda baca. Safety Notices tidak memiliki `updated_at` atau `order_by`, dan tidak pernah berubah.
* **Baca setiap halaman,** seperti yang Anda lakukan untuk Safety Cases.
* **Cocokkan Safety Notices berdasarkan `id`,** karena hasil dapat berulang.

Daftar Safety Notices terlihat seperti ini:

```json Response
{
  "data": [
    {
      "type": "compliance_review_notice",
      "id": "rvn_01Jt5Yw2MnQx8VbK4zRcHd6F",
      "organization_id": "abcdef01-2345-6789-abcd-ef0123456789",
      "case_ids": ["rvc_01Hq3Zt8KpWv5NcR2yLbXs7D"],
      "kind": { "type": "response_requested" },
      "created_at": "2026-11-27T18:00:00Z",
      "message": "Anthropic has found no valid response to the Case in case_ids. Review the Case and write your response file before the time in respond_by. If you wrote a valid response file in the last hour, ignore this notice.",
      "respond_by": "2026-11-30T18:42:07Z"
    }
  ],
  "next_page": null
}
```

`respond_by` bernilai `null` jika Safety Notice tidak memiliki tenggat waktu. [File Safety Notice](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#notice) memiliki field yang sama, tanpa `type` dan `organization_id`, dan dengan `schema_version`.

### Perbedaan field dengan file

Anthropic juga dapat menulis Safety Cases ke bucket di akun cloud Anda sendiri, sebagai [file Safety Case](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files). File tersebut merupakan cara lain untuk membaca dan menanggapi Safety Cases. File menggunakan nama field API, dengan perbedaan berikut:

| Di API | Di [file Safety Case](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#safety-case-file) |
| ----- | ----- |
| `type`, `organization_id` | Tidak ada di file |
| `transcripts[].user_profile_id` bernilai `null` jika tidak ada, atau jika pesan berusia lebih dari 28 hari | Kunci tersebut tidak disertakan jika tidak ada |
| Tidak ada di API | `schema_version`, `transcripts[].object_key`, `derived_data_object_keys` |
| Safety Case yang ditutup selalu memiliki `status.reason` | `status.reason` dapat bernilai `null` |
| `updated_at` juga berubah ketika Safety Notice menyebutkan Safety Case tersebut | `updated_at` hanya berubah ketika Anthropic menulis file |
| Waktu dengan pecahan detik | Waktu dalam detik bulat. `created_at` dapat sedikit lebih awal. |

## Membaca pesan

Ambil setiap `item_id` di `transcripts`. Apakah Anda dapat membaca pesan yang Anda kirim dengan profil pengguna bergantung pada kuncinya:

* **Kunci Admin API dari Claude Console** tidak dapat membaca pesan seperti itu. Permintaan tersebut mengembalikan error 404. Anthropic menulis [transkrip](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-case-files#transcript) pesan tersebut ke bucket kasus workspace, jika workspace tersebut memilikinya.
* **Kunci lain** dapat membaca pesan seperti itu di beberapa organisasi (lihat [Dapatkan akses](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/safety-cases-api#get-access)). Dengan kunci tersebut, kirimkan ID profil pengguna di header `anthropic-user-profile-id`. Untuk pesan lainnya, jangan sertakan header tersebut. ID yang salah atau tidak ada akan mengembalikan error 404, begitu pula ID pada pesan yang Anda kirim tanpa profil pengguna.

```bash cURL
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/safeguards/items/msg_01XFDUDYJgAACzvnptvVoYEL" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2026-10-21"
```

Respons memuat pesan tersebut serta pengirim yang dicatat oleh Anthropic:

```json Response
{
  "type": "compliance_safeguards_review_item",
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "organization_uuid": "abcdef01-2345-6789-abcd-ef0123456789",
  "sampled_at": "2026-11-23T17:58:12.482913Z",
  "content_expires_at": "2026-12-21T17:58:12.482913Z",
  "product_surface": "api",
  "model": "claude-opus-5-5",
  "workspace_id": "wrkspc_01AbCdEfGhJkLmNpQrStUvWx",
  "api_key_id": null,
  "user": { "id": "user_01JkWm4Rt7YpXc2NvBq9sZdH", "email_address": "user@example.com" },
  "user_profile_id": null,
  "refs": {
    "batch_id": null,
    "local_session_id": null,
    "claude_chat_id": null,
    "claude_chat_message_id": null,
    "remote_session_id": null,
    "remote_session_event_id": null,
    "agent_session_id": null
  },
  "content": {
    "request": {
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [{ "role": "user", "content": "Hello, Claude" }]
    },
    "response": {
      "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
      "type": "message",
      "role": "assistant",
      "content": [{ "type": "text", "text": "Hello! How can I help you today?" }]
    }
  },
  "content_unavailable_reason": null
}
```

`content` memuat permintaan dan respons yang disimpan. Ini bukan salinan persis: Anthropic memotong beberapa URL menjadi host-nya, menyamarkan token server MCP, menghapus blok thinking, dan dapat mengganti gambar atau dokumen dengan gambar yang diubah ukurannya atau placeholder.

Anthropic mencatat satu pengirim untuk setiap pesan:

| Pengirim | `user` | `api_key_id` |
| ----- | ----- | ----- |
| [Kunci pribadi](https://platform.claude.com/docs/id/manage-claude/authentication#key-types) atau proses masuk pengguna | ID dan alamat email akun tersebut | `null` |
| Kunci workspace | `null` | ID kunci tersebut |
| Akun layanan, atau tidak ada pengirim yang dicatat | `null` | `null` |

`user` mengidentifikasi akun tersebut, bukan orang yang menulis prompt. Untuk menemukan orang tersebut, gunakan log Anda sendiri (lihat [Catat ID pesan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#log-message-ids)). `email_address` selalu bernilai `null` di organisasi tanpa organisasi induk, dan dapat bernilai `null` di organisasi lainnya.

Safety Case dapat mencantumkan pesan yang tidak dapat Anda baca. Tabel ini menunjukkan apa yang dapat dikembalikan oleh permintaan:

| Hasil | Artinya | Yang perlu dilakukan |
| ----- | ----- | ----- |
| Error 404 | Misalnya, pesan telah kedaluwarsa atau tidak lagi ditandai. | Error 404 dapat bersifat sementara, jadi coba lagi nanti sebelum Anda menganggap pesan tidak dapat dibaca. |
| Error 404 untuk setiap pesan | Hal ini terjadi jika Anthropic belum mengaktifkan pembacaan pesan untuk organisasi Anda, atau jika organisasi Anda tidak lagi memiliki persetujuan Anthropic untuk menonaktifkan Anthropic Human Review. | Lihat [Menghubungi untuk mendapatkan bantuan](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#get-help). Error 404 dapat bersifat sementara, jadi coba lagi nanti sebelum Anda menganggap pesan tidak dapat dibaca. |
| Error 503 | Error ini dapat bersifat sementara. | Coba lagi nanti sebelum Anda menganggap pesan tidak dapat dibaca. |
| Pesan, dengan `content` yang diatur ke `null` | Anthropic tidak memiliki salinan teksnya. `content_unavailable_reason` bernilai `not_captured` atau `use_ref`, dan Anthropic dapat menambahkan nilai lain. | Dengan `use_ref`, `refs` dapat memuat ID yang menyebutkan percakapan tersebut. Baca percakapan tersebut melalui endpoint Compliance API untuk ID itu, dengan kunci yang memiliki akses ke percakapan tersebut. |

Baca dan simpan setiap pesan segera setelah Safety Case tiba, dan tidak lebih lambat dari `content_expires_at`. Waktu tersebut paling lama 28 hari setelah `sampled_at`, dan Safety Case yang masih terbuka tidak memperpanjangnya. Pesan dapat berhenti dapat dibaca sebelum waktu tersebut.

## Menanggapi Safety Case

Setelah Anda menyelidiki Safety Case, kirimkan tanggapan untuk memberi tahu Anthropic apa yang Anda temukan. [Menanggapi Safety Case](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#respond-to-a-case) menjelaskan apa yang dikonfirmasi oleh sebuah tanggapan, dan [Jika Anda tidak menanggapi](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/flagged-cases#if-you-dont-respond) menjelaskan apa yang terjadi tanpa tanggapan.

<Warning>
  Tanggapan akan menutup Safety Case, sehingga Anda tidak dapat mengubah tanggapan Anda nanti.
</Warning>

Kirimkan satu permintaan dalam 7 hari kalender sejak `created_at` Safety Case:

```bash cURL
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/review/cases/rvc_01Hq3Zt8KpWv5NcR2yLbXs7D/respond" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2026-10-21" \
  -H "content-type: application/json" \
  -d '{
    "determination": "violation",
    "policy_categories": ["cyber"]
  }'
```

`determination` wajib diisi, `policy_categories` wajib diisi bersama `violation`, dan `verdicts` bersifat opsional:

| Field | Yang perlu dikirim |
| ----- | ----- |
| `determination` | `violation` atau `no_violation`, untuk Safety Case secara keseluruhan |
| `policy_categories` | Dengan `violation`, satu hingga empat kategori yang Anda konfirmasi, seperti `cyber`, atau `other` jika tidak ada yang sesuai. `benign` dan `undetermined` mengembalikan error 400. Dengan `no_violation`, jangan sertakan field ini atau kirimkan daftar kosong. |
| `verdicts` | Untuk menilai pesan secara terpisah, daftar yang berisi `item_id`, `determination`, dan `policy_category` (sebuah kategori atau `null`, dan selalu `null` dengan `no_violation`) untuk masing-masing pesan. |

Respons 200 mengembalikan Safety Case yang telah ditutup, dengan `status.reason.type` yang diatur ke `responded`. Hal ini mengonfirmasi bahwa Anthropic telah menerima tanggapan Anda.

Anthropic menghitung tanggapan pertama, baik yang masuk melalui API maupun sebagai file:

| Yang Anda kirim berikutnya | Yang dikembalikan API |
| ----- | ----- |
| Tanggapan yang sama lagi | Respons 200. Tidak ada yang berubah, sehingga aman untuk mencoba ulang. |
| Tanggapan valid lainnya untuk Safety Case yang telah ditutup | Error 400 dengan `error.details.error_code` yang diatur ke `case_closed`. |
