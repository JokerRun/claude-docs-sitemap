---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 1037ad5fc5b08a7cbda9a96e43b16d85ec6c2b3fc4bb678ad7cf84e122edc7d9
---

# Mengkueri Activity Feed

Mengambil, memfilter, dan melakukan paginasi pada Activity Feed Compliance API organisasi Anda.

---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_activities` pada Compliance Access Key atau kunci Admin API.

  Baik Compliance Access Key (`sk-ant-api01-...`) yang membawa scope ini maupun kunci Admin API (`sk-ant-admin01-...`) dapat memanggil Activity Feed. Lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access) untuk mengetahui kondisi di mana setiap jenis kunci membawa scope tersebut.
</Check>

Activity Feed mencatat setiap tindakan autentikasi, chat, file, proyek, administratif, dan platform yang terjadi di organisasi Anda, dalam urutan kronologis terbalik. Aktivitas dapat dikueri dalam waktu 1 menit setelah terjadi dan disimpan selama 6 tahun.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/compliance/activities?limit=1" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

```json Response
{
  "data": [
    {
      "id": "activity_01XyDMpzjS89pFZXqSFUBDr6",
      "created_at": "2026-04-10T08:09:10Z",
      "organization_id": "org_01Wv6QeBcDfGhJkLmNpQrSt8",
      "organization_uuid": "abcdef01-2345-6789-abcd-ef0123456789",
      "actor": {
        "type": "user_actor",
        "email_address": "user@example.com",
        "user_id": "user_01TuVwXyZaBcDeFgH2JkLmN4",
        "ip_address": "192.0.2.34",
        "user_agent": "Mozilla/5.0..."
      },
      "type": "claude_chat_created",
      "claude_chat_id": "claude_chat_01XyDMpzjS89pFZXqSFUBDr6",
      "claude_project_id": "claude_proj_01KGp4eZNug9ri4kE35RSppq"
    }
  ],
  "has_more": true,
  "first_id": "activity_01XyDMpzjS89pFZXqSFUBDr6",
  "last_id": "activity_01XyDMpzjS89pFZXqSFUBDr6"
}
```

## Memfilter aktivitas

Filter berdasarkan organisasi, aktor, jenis aktivitas, atau jendela waktu `created_at` menggunakan sub-parameter bertitik `created_at.gte`, `.gt`, `.lte`, dan `.lt`. Lihat [referensi API](/docs/id/api/compliance/activities/list) untuk tipe dan nilai yang diterima setiap parameter.

Parameter yang dapat diulang menggunakan sintaks kueri array-bracket: berikan `activity_types[]=...`, `actor_ids[]=...`, atau `organization_ids[]=...` satu kali untuk setiap nilai.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/activities" \
    --data-urlencode "activity_types[]=claude_file_uploaded" \
    --data-urlencode "activity_types[]=claude_chat_created" \
    --data-urlencode "created_at.gte=2026-04-01T00:00:00Z" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

Activity Feed menghasilkan ratusan jenis aktivitas yang berbeda. Lihat [Query compliance activities](/docs/id/api/compliance/activities/list) di referensi API untuk daftar lengkap nilai yang diterima oleh `activity_types[]`.

## Melakukan paginasi hasil

Aktivitas dikembalikan dengan urutan terbaru lebih dulu, dengan nilai `created_at` yang sama diurutkan berdasarkan ID aktivitas, dan dibatasi hingga `limit` hasil di setiap respons (default 100, maksimum 5.000). Lihat [referensi API](/docs/id/api/compliance/activities/list) untuk skema respons lengkap.

Compliance API menggunakan dua skema paginasi tergantung pada kelompok endpoint:

| Kelompok endpoint                                                                    | Urutan pengurutan     | Skema      | Parameter                                                            |
| ------------------------------------------------------------------------------------ | --------------------- | ---------- | -------------------------------------------------------------------- |
| Activities                                                                           | Terbaru lebih dulu    | Cursor     | `after_id`, `before_id` (dikembalikan sebagai `first_id`, `last_id`) |
| Chats dan chat messages                                                              | Terlama lebih dulu    | Cursor     | `after_id`, `before_id` (dikembalikan sebagai `first_id`, `last_id`) |
| Projects, project attachments, users, roles, role permissions, groups, group members | Spesifik per endpoint | Page token | `page` (dikembalikan sebagai `next_page`)                            |

Organizations dan files tidak menggunakan paginasi: [List organizations](/docs/id/manage-claude/compliance-org-data#list-organizations) mengembalikan semua hasil dalam satu respons, dan file diambil secara individual berdasarkan ID.

Cursor paginasi dan page token adalah string opaque: kirimkan kembali tanpa perubahan. Format internalnya tidak stabil, dan mem-parsing-nya akan menyebabkan kerusakan tanpa pemberitahuan. Hanya salah satu dari `after_id` atau `before_id` yang boleh diatur dalam setiap permintaan, dan kedua skema mengembalikan `has_more` sehingga Anda tahu kapan harus berhenti.

Untuk melakukan paginasi pada aktivitas:

* Berikan `last_id` dari respons sebagai `after_id` untuk maju ke halaman berikutnya dalam urutan hasil. Dengan aktivitas yang diurutkan terbaru lebih dulu, halaman berikutnya berisi entri yang lebih lama.
* Berikan `first_id` sebagai `before_id` untuk kembali ke halaman sebelumnya.
* Berhenti ketika `has_more` bernilai `false`.

Parameter cursor menentukan arah halaman; urutan pengurutan endpoint menentukan arah waktu. Parameter `after_id` yang sama di sini mencapai aktivitas yang lebih lama. Chats diurutkan terlama lebih dulu; lihat [Mengambil dan menghapus chat, file, dan proyek](/docs/id/manage-claude/compliance-content-data) untuk semantik cursor di sana.

<Note>
  **Cursor aman untuk digunakan kembali saat retry.** Cursor atau page token dari halaman yang berhasil dikembalikan tetap valid; permintaan yang gagal (5xx, timeout, kesalahan jaringan) tidak memajukan posisi Anda. Coba ulang permintaan yang sama dengan cursor yang sama. Hanya pindah ke cursor berikutnya setelah Anda menyimpan halaman yang telah dilewatinya.
</Note>

<CodeGroup>
  ```bash cURL
  # Ambil halaman pertama (aktivitas terbaru lebih dulu) dan simpan kursor akhirnya.
  last_id=$(curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/compliance/activities?limit=2" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" | jq -er '.last_id')

  # Kirim kembali kursor tersebut tanpa perubahan untuk mengambil halaman berikutnya (lebih lama).
  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/activities" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    --data-urlencode "limit=2" \
    --data-urlencode "after_id=${last_id}"
  ```
</CodeGroup>

Loop **backfill** produksi melakukan paginasi melalui aktivitas yang lebih lama dengan menjalankan iterasi berdasarkan `has_more` dan `last_id`:

1. Mulai dari cursor yang Anda simpan (atau hilangkan `after_id` untuk memulai dari awal).
2. Lakukan paginasi dengan `after_id=<last_id>` hingga `has_more` bernilai `false`.
3. Simpan `last_id` terakhir hanya setelah Anda menyimpan setiap halaman yang dicakupnya.

```text
cursor = stored_cursor
loop:
  if cursor is not null:
    page = GET /v1/compliance/activities?after_id={cursor}&limit=100
  else:
    page = GET /v1/compliance/activities?limit=100
  store(page.data)
  if page.last_id is not null:
    cursor = page.last_id
  if not page.has_more: break
persist(cursor)
```

## Memahami objek Activity

Setiap entri dalam `data` adalah sebuah Activity dengan bentuk tingkat atas berikut:

| Field               | Tipe             | Deskripsi                                                                                                                                                                                                                                |
| ------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                | string           | Pengidentifikasi unik untuk aktivitas.                                                                                                                                                                                                   |
| `created_at`        | string RFC 3339  | Kapan aktivitas terjadi.                                                                                                                                                                                                                 |
| `organization_id`   | string atau null | Organisasi tempat aktivitas terjadi, atau `null` untuk peristiwa yang tidak terkait dengan organisasi (sign-in, sign-out, panggilan Compliance API).                                                                                     |
| `organization_uuid` | string atau null | Cakupan yang sama dengan `organization_id`, dinyatakan sebagai UUID.                                                                                                                                                                     |
| `actor`             | Actor union      | Siapa atau apa yang melakukan aktivitas. Lihat tabel aktor berikut.                                                                                                                                                                      |
| `type`              | string           | Jenis aktivitas, misalnya `claude_chat_created`.                                                                                                                                                                                         |
| *field tambahan*    | bervariasi       | Field spesifik per jenis, misalnya `claude_chat_id` pada peristiwa chat atau `filename` pada peristiwa file. Lihat [Query compliance activities](/docs/id/api/compliance/activities/list) di referensi API untuk daftar field per jenis. |

Field `actor` adalah discriminated union. Diskriminator `type` memberi tahu Anda field lain mana yang ada:

| `actor.type`                 | Kapan muncul                                                                                                                                                                                                           | Field utama                                                                                                                                                |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `user_actor`                 | Pengguna claude.ai atau Claude Console yang sudah masuk melakukan tindakan tersebut.                                                                                                                                   | `email_address`, `user_id`, `ip_address`, `user_agent`                                                                                                     |
| `api_actor`                  | Sebuah permintaan memanggil Claude API atau Compliance API dengan kunci API yang diterbitkan pelanggan. Panggilan Compliance API menghasilkan jenis aktor ini baik untuk Compliance Access Key maupun kunci Admin API. | `api_key_id`, `ip_address`, `user_agent`                                                                                                                   |
| `admin_api_key_actor`        | Admin organisasi menggunakan kunci Admin API untuk mengelola pengguna, undangan, workspace, atau kunci API.                                                                                                            | `admin_api_key_id`                                                                                                                                         |
| `unauthenticated_user_actor` | Sebuah tindakan terjadi sebelum proses masuk selesai, misalnya `sso_login_initiated`.                                                                                                                                  | `unauthenticated_email_address`, `ip_address`, `user_agent`                                                                                                |
| `anthropic_actor`            | Anthropic bertindak pada organisasi, misalnya melalui tooling internal.                                                                                                                                                | `email_address` (selalu `null`; ada untuk konsistensi bentuk dengan `user_actor`, karena operator Anthropic tidak direpresentasikan oleh email individual) |
| `scim_directory_sync_actor`  | Penyedia identitas (seperti Okta, Microsoft Entra ID, atau JumpCloud) mendorong perubahan melalui sinkronisasi direktori SCIM.                                                                                         | `workos_event_id`, `directory_id`, `idp_connection_type` (nullable; misalnya `OktaSCIMV2`, `AzureSCIMV2`)                                                  |

<Note>
  **Bangun handler yang kompatibel ke depan.** Teruskan nilai `type` dan `actor.type` yang tidak dikenali, dan abaikan field yang tidak diharapkan oleh handler Anda, sehingga integrasi Anda tetap berfungsi ketika jenis aktivitas baru dirilis.
</Note>

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi API" href="/docs/id/api/compliance/activities/list">
    Skema permintaan dan respons lengkap untuk `GET /v1/compliance/activities`, termasuk setiap nilai `activity_types[]` yang didukung.
  </Card>

  <Card title="Mengambil dan menghapus chat, file, dan proyek" href="/docs/id/manage-claude/compliance-content-data">
    Kueri dan hapus konten yang mendasari aktivitas yang Anda temukan di feed (memerlukan Compliance Access Key).
  </Card>

  <Card title="Merancang integrasi compliance Anda" href="/docs/id/manage-claude/compliance-integration-patterns">
    Pilih pola konsumsi polling atau batch dan rencanakan korelasi SIEM.
  </Card>

  <Card title="Menangani error Compliance API" href="/docs/id/manage-claude/compliance-errors">
    Katalog error lengkap.
  </Card>
</CardGroup>
