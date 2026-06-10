---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-content-data
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: a7275ef1183b363c1805e26157109959b6e9a29c8a05da0883e797d95c632607
---

# Mengambil dan menghapus obrolan, file, dan proyek

Akses konten obrolan, lampiran file, dan proyek untuk organisasi claude.ai melalui Compliance API.

---

<Note>
  Compliance API diaktifkan berdasarkan permintaan. Organisasi Claude Enterprise memiliki akses ke API lengkap; organisasi Claude Console hanya memiliki akses ke [Activity Feed](/docs/id/manage-claude/compliance-activity-feed). Lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>
:
    the chat/file/project endpoints read claude.ai content, so unlike the rest of
    the Compliance API they really are Claude Enterprise-only. */}
<Note>
  Endpoint pada halaman ini mengambil dan menghapus konten claude.ai, yang hanya tersedia untuk organisasi dengan paket Claude Enterprise. Compliance API diaktifkan berdasarkan permintaan. Lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_user_data` pada Compliance Access Key. Endpoint penghapusan juga memerlukan `delete:compliance_user_data`.

  **Prasyarat:** Untuk mencantumkan obrolan, setidaknya satu ID pengguna dari [Mencantumkan pengguna organisasi](/docs/id/manage-claude/compliance-org-data#list-organization-users). Endpoint lain pada halaman ini menerima ID sumber daya secara langsung.
</Check>

Endpoint pada halaman ini mengekspos konten obrolan claude.ai, unggahan file, proyek, dan lampiran proyek kepada peninjau kepatuhan. Endpoint ini mendukung ekspor "eDiscovery" (penemuan elektronik), penegakan "data loss prevention" (pencegahan kehilangan data), atau DLP, dan respons penghapusan akun. Konten disimpan selama kebijakan retensi organisasi Anda mengizinkan. Obrolan yang telah di-soft-delete oleh pengguna di claude.ai tetap terlihat melalui Compliance API dengan `deleted_at` terisi; obrolan yang telah di-hard-delete (melalui Compliance API itu sendiri, atau setelah jendela retensi organisasi berakhir) tidak dapat diambil.

Kedua scope hanya diberikan pada Compliance Access Key (`sk-ant-api01-...`) yang dibuat di claude.ai; lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access) untuk menyediakannya. Scope `read:compliance_user_data` mencakup pengambilan; `delete:compliance_user_data` hanya diperlukan untuk endpoint penghapusan. Endpoint obrolan, file, proyek, dan lampiran tidak tersedia untuk Admin API key (`sk-ant-admin01-...`); panggilan yang diautentikasi dengan Admin API key akan mengembalikan [403 Forbidden](/docs/id/manage-claude/compliance-errors#403-forbidden).

Endpoint pada halaman ini melakukan paginasi dengan dua cara; lihat [Melakukan paginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results) untuk referensi lengkapnya. Setiap bagian mencatat skema mana yang berlaku.

## Mengambil obrolan dan pesan \{#retrieve-chats-and-messages}

Gunakan [List chats](/docs/id/api/compliance/apps/chats/list) untuk menelusuri metadata obrolan per halaman, lalu [Get chat messages](/docs/id/api/compliance/apps/chats/messages/list) untuk mengambil konten pesan lengkap dari satu obrolan.

Endpoint daftar obrolan memerlukan setidaknya satu nilai `user_ids[]` (dan menerima hingga 10 dalam satu permintaan), jadi enumerasikan ID pengguna terlebih dahulu dengan [Mencantumkan pengguna organisasi](/docs/id/manage-claude/compliance-org-data#list-organization-users), lalu cantumkan obrolan untuk setiap pengguna atau untuk setiap batch pengguna. Permintaan berikut mencantumkan obrolan yang dimiliki oleh pengguna tertentu sejak tanggal tertentu.

<CodeGroup>
```bash cURL nocheck
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/chats" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "user_ids[]=user_01XyDMpzjS89pFZXqSFUBDr6" \
  --data-urlencode "organization_ids[]=91012d09-e48b-438e-a489-1bebfd8fa6f9" \
  --data-urlencode "created_at.gte=2025-06-01T00:00:00Z" \
  --data-urlencode "limit=100"
```
</CodeGroup>

```json Response
{
  "data": [
    {
      "id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja",
      "name": "Product Requirements Discussion",
      "created_at": "2026-04-10T08:09:10Z",
      "updated_at": "2026-04-10T09:10:11Z",
      "deleted_at": null,
      "href": "https://claude.ai/chat/abcdef01-2345-6789-abcd-ef0123456789",
      "model": "claude-opus-4-8",
      "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
      "project_id": "claude_proj_01KGp4eZNug9ri4kE35RSppq",
      "user": {
        "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
        "email_address": "user@example.com"
      }
    }
  ],
  "has_more": true,
  "first_id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja",
  "last_id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja"
}
```

Mencantumkan obrolan hanya mengembalikan metadata. Lihat [List chats](/docs/id/api/compliance/apps/chats/list) untuk daftar filter lengkap; selain `user_ids[]` yang wajib, batas `updated_at.*` berguna untuk peninjauan inkremental terhadap obrolan yang telah berubah sejak ekspor sebelumnya.

Hasil obrolan diurutkan berdasarkan `created_at` secara menaik (terlama lebih dulu), dengan pengurutan tambahan berdasarkan `id` jika ada nilai yang sama. Paginasi menggunakan field kursor `first_id`/`last_id`/`has_more` yang sama seperti [Melakukan paginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results); teruskan `last_id` sebagai `after_id` untuk bergerak maju menuju obrolan yang lebih baru, atau `first_id` sebagai `before_id` untuk bergerak mundur menuju obrolan yang lebih lama.

Untuk menarik konten obrolan yang sebenarnya, file terlampir, dan artifact inline (dokumen terstruktur yang dihasilkan Claude di dalam obrolan), lanjutkan dengan endpoint pesan untuk setiap ID obrolan:

<CodeGroup>
```bash cURL nocheck
chat_id="claude_chat_01H5CWunD7RpVJ5bHa8RCkja"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/chats/$chat_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```
</CodeGroup>

Endpoint pesan mengembalikan metadata obrolan ditambah array `chat_messages` yang diurutkan berdasarkan `created_at`. Ketika `limit` dihilangkan, seluruh kumpulan pesan dikembalikan dalam satu respons; teruskan `limit`, `after_id`, atau `before_id` untuk menelusuri obrolan yang sangat panjang per halaman. Endpoint ini juga menerima batas rentang `created_at.*` dan `updated_at.*` (`gt`, `gte`, `lt`, `lte`) serta parameter `order` (`asc` atau `desc`). Lihat [Get chat messages](/docs/id/api/compliance/apps/chats/messages/list) untuk daftar parameter lengkap. Untuk pesan pengguna, `created_at` adalah waktu pesan dikirim; untuk pesan asisten, ini adalah waktu Claude selesai menghasilkan pesan. Setiap pesan membawa konten teksnya dan, jika ada, file apa pun yang diunggah (biasanya pada pesan pengguna), file apa pun yang dihasilkan alat, dan artifact apa pun yang dihasilkan atau diperbarui oleh asisten (biasanya pada pesan asisten):

```json Response
{
  "id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja",
  "name": "Product Requirements Discussion",
  "created_at": "2026-04-10T08:09:10Z",
  "updated_at": "2026-04-10T09:10:11Z",
  "deleted_at": null,
  "href": "https://claude.ai/chat/abcdef01-2345-6789-abcd-ef0123456789",
  "model": "claude-opus-4-8",
  "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
  "project_id": "claude_proj_01KGp4eZNug9ri4kE35RSppq",
  "user": {
    "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
    "email_address": "user@example.com"
  },
  "chat_messages": [
    {
      "id": "claude_chat_msg_01VnBPkLmtj7YdW5QrXKEA8c",
      "role": "user",
      "created_at": "2026-04-10T08:09:10Z",
      "content": [
        {
          "type": "text",
          "text": "Can you help me draft requirements for our new dashboard feature?"
        }
      ],
      "files": [
        {
          "id": "claude_file_01UaT9wBcDfGhJkLmNpQrSv7",
          "filename": "dashboard_mockup_v1.pdf",
          "mime_type": "application/pdf"
        }
      ]
    },
    {
      "id": "claude_chat_msg_01M8tFcHwbQ2kY6NpEjRZv4D",
      "role": "assistant",
      "created_at": "2026-04-10T08:09:11Z",
      "content": [
        {
          "type": "text",
          "text": "I'd be happy to help you draft requirements for your dashboard feature..."
        }
      ],
      "generated_files": [
        {
          "id": "claude_gen_file_01TbR8wAcCeFhJkLnPqStUvX",
          "filename": "requirements_summary.csv",
          "mime_type": "text/csv"
        }
      ],
      "artifacts": [
        {
          "id": "claude_artifact_01HqRsTuVwXyZa2BcDeFgH4J",
          "version_id": "claude_artifact_version_01KmNpQrSt3UvWxYz5AbCdEfG",
          "title": "Dashboard Requirements Draft",
          "artifact_type": "text/markdown"
        }
      ]
    }
  ],
  "has_more": false,
  "first_id": "eyJtc2dfdXVpZCI6ICIwZjcwYjA2Ni0uLi4ifQ==",
  "last_id": "eyJtc2dfdXVpZCI6ICJhNGUwYjE3Mi0uLi4ifQ=="
}
```

`files`, `generated_files`, dan `artifacts` masing-masing dapat bernilai `null` pada pesan tertentu. `files` adalah unggahan biner (PDF, gambar, spreadsheet) yang dilampirkan pengguna ke pesan. `generated_files` adalah file biner yang dibuat asisten selama percakapan melalui penggunaan alat (misalnya, PDF, spreadsheet, atau slide deck). `artifacts` adalah dokumen berversi (misalnya, kode atau markdown) yang dihasilkan atau diperbarui asisten dalam responsnya; sebuah artifact dapat direvisi di beberapa giliran asisten dalam obrolan yang sama, dan setiap revisi muncul sebagai `version_id` baru di bawah `id` artifact yang sama. Teruskan `id` setiap entri (atau `version_id` untuk artifact) ke endpoint konten yang sesuai di [Mengambil file dan artifact](#retrieve-files-and-artifacts) untuk mengunduhnya.

## Mengambil file dan artifact \{#retrieve-files-and-artifacts}

File dan artifact diunduh berdasarkan ID, bukan dicantumkan secara independen. ID tersebut berasal dari endpoint pesan obrolan di [Mengambil obrolan dan pesan](#retrieve-chats-and-messages) (array `files`, `generated_files`, dan `artifacts` pada setiap pesan) atau, untuk unggahan tingkat proyek, dari [endpoint lampiran proyek](#retrieve-projects-and-attachments).

Pilih endpoint yang sesuai dengan jenis ID Anda dan data yang Anda butuhkan. Endpoint konten file yang sama melayani file obrolan maupun file proyek.

| Anda memiliki | Anda menginginkan | Gunakan endpoint ini |
| --- | --- | --- |
| ID `claude_file_*` | Konten biner file | [Download file content](/docs/id/api/compliance/apps/chats/files/download) |
| ID `claude_file_*` | Hanya metadata file | [Get file metadata](/docs/id/api/compliance/apps/chats/files/retrieve) |
| ID `claude_gen_file_*` | Konten biner file yang dihasilkan alat | [Download a Claude-generated file](/docs/id/api/compliance/apps/chats/generated_files/download) |
| ID `claude_gen_file_*` | Hanya metadata file yang dihasilkan alat | [Get generated-file metadata](/docs/id/api/compliance/apps/chats/generated_files/retrieve) |
| ID `claude_artifact_version_*` | Teks dari satu versi artifact | [Download artifact content](/docs/id/api/compliance/apps/artifacts/download) |
| ID `claude_artifact_version_*` | Hanya metadata versi artifact | [Get artifact metadata](/docs/id/api/compliance/apps/artifacts/retrieve) |
| ID `claude_proj_doc_*` | Konten teks biasa dari dokumen proyek | [Get project document content](/docs/id/api/compliance/apps/projects/documents/retrieve) |
| ID `claude_proj_doc_*` | Hanya metadata dokumen proyek | [Get project document metadata](/docs/id/api/compliance/apps/projects/documents/metadata) |

Endpoint konten file mengalirkan unggahan asli sebagai respons biner chunked dengan header berikut:

- `Content-Disposition: attachment; filename*=utf-8''` membawa nama file unggahan asli dalam bentuk extended RFC 5987. Bentuk extended digunakan untuk setiap nama file, bukan hanya yang non-ASCII.
- `Content-Type` membawa tipe MIME unggahan.
- `Content-MD5` membawa digest MD5 file, dikodekan base64 sebagaimana ditentukan dalam RFC 1864.
- `Transfer-Encoding: chunked` selalu disetel.

<CodeGroup>
```bash cURL nocheck
file_id="claude_file_01UaT9wBcDfGhJkLmNpQrSv7"

curl --fail-with-body -sS -OJ \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  "https://api.anthropic.com/v1/compliance/apps/chats/files/$file_id/content"
```
</CodeGroup>

Flag `-OJ` memberi tahu curl untuk menyimpan respons dengan nama file dari `Content-Disposition`, yang merupakan nama file asli yang diunggah pengguna.

Endpoint konten artifact mengembalikan isi teks dari satu versi artifact. Teruskan `version_id` dari salah satu entri dalam array `artifacts` pada pesan asisten, bukan `id` stabil artifact tersebut. Setiap versi baru dari sebuah artifact memiliki `version_id` sendiri, dan Compliance API menyajikan byte persis dari versi tersebut.

## Mengambil proyek dan lampiran \{#retrieve-projects-and-attachments}

Proyek menggabungkan obrolan terkait bersama dengan instruksi kustom, konten basis pengetahuan, serta file atau dokumen teks yang dilampirkan. Compliance API mengekspos metadata proyek, detail proyek, dan daftar lampiran yang dimiliki sebuah proyek.

- [List projects](/docs/id/api/compliance/apps/projects/list)
- [Get project details](/docs/id/api/compliance/apps/projects/retrieve)
- [List project attachments](/docs/id/api/compliance/apps/projects/attachments/list)
- [Get project document content](/docs/id/api/compliance/apps/projects/documents/retrieve)

Hasil proyek diurutkan berdasarkan tanggal pembuatan secara menaik. Hasil lampiran diurutkan berdasarkan `created_at` secara menaik, dengan pengurutan tambahan berdasarkan `id` jika ada nilai yang sama. Respons daftar proyek dan daftar lampiran melakukan paginasi dengan token halaman `next_page` yang opaque, bukan kursor `first_id`/`last_id` yang digunakan oleh obrolan dan Activity Feed. Teruskan token tersebut kembali sebagai parameter kueri `page` pada permintaan berikutnya.

### File proyek versus dokumen proyek \{#project-files-versus-project-documents}

Lampiran proyek memiliki salah satu dari dua bentuk berbeda, yang diidentifikasi oleh diskriminator `type` pada setiap entri:

Entri dengan `type` bernilai `project_file` adalah unggahan biner (PDF, gambar, spreadsheet) yang ID-nya dimulai dengan `claude_file_`; unduh dengan [Download file content](/docs/id/api/compliance/apps/chats/files/download). Entri dengan `type` bernilai `project_doc` adalah dokumen teks biasa (selalu `text/plain`) yang ID-nya dimulai dengan `claude_proj_doc_`; ambil dengan [Get project document content](/docs/id/api/compliance/apps/projects/documents/retrieve).

Konsumen yang menelusuri daftar lampiran harus bercabang berdasarkan `type` dan memanggil endpoint konten yang sesuai untuk setiap entri. Permintaan berikut mencantumkan satu halaman lampiran; lakukan paginasi dengan meneruskan `next_page` kembali sebagai parameter `page` hingga `has_more` bernilai `false`.

<CodeGroup>
```bash cURL nocheck
project_id="claude_proj_01KGp4eZNug9ri4kE35RSppq"

curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/projects/$project_id/attachments" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```
</CodeGroup>

```json Response
{
  "data": [
    {
      "id": "claude_file_01UaT9wBcDfGhJkLmNpQrSv7",
      "created_at": "2026-04-10T08:09:10Z",
      "filename": "dashboard_mockup_v1.pdf",
      "mime_type": "application/pdf",
      "type": "project_file"
    },
    {
      "id": "claude_proj_doc_01YnT8sBcWvUtXzQpMkRfDgH",
      "created_at": "2026-04-10T08:09:11Z",
      "filename": "requirements.md",
      "mime_type": "text/plain",
      "type": "project_doc"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

## Menghapus konten \{#delete-content}

<Warning>
  Setiap penghapusan yang berhasil bersifat permanen dan langsung. Tidak ada jendela pemulihan.
</Warning>

Compliance API mengekspos endpoint hard-delete untuk obrolan, file, dokumen proyek, dan seluruh proyek. Obrolan yang telah di-hard-delete tidak dapat dipulihkan, dan tidak lagi muncul dalam respons daftar setelahnya (sedangkan obrolan yang di-soft-delete dari claude.ai masih muncul dengan `deleted_at` terisi).

- [Delete chat](/docs/id/api/compliance/apps/chats/delete): juga menghapus pesan obrolan dan file apa pun yang dilampirkan ke pesan tersebut.
- [Delete file](/docs/id/api/compliance/apps/chats/files/delete): menangani file obrolan maupun file proyek.
- [Delete project document](/docs/id/api/compliance/apps/projects/documents/delete): menghapus satu dokumen proyek berdasarkan ID.
- [Delete project](/docs/id/api/compliance/apps/projects/delete): lihat [Lepaskan obrolan sebelum menghapus proyek](#detach-chats-before-deleting-a-project).

Keempat endpoint tersebut memerlukan scope `delete:compliance_user_data`, yang diberikan secara terpisah dari scope baca saat Compliance Access Key dibuat.

Permintaan berikut menghapus satu obrolan. Pola yang sama berlaku untuk endpoint penghapusan lainnya; hanya URL yang berubah.

<CodeGroup>
```bash cURL nocheck
# PERINGATAN: Operasi ini menghapus obrolan secara PERMANEN, beserta semua pesannya
# dan file apa pun yang terlampir. Penghapusan terjadi seketika dan tidak dapat dibatalkan.
# Operasi ini memerlukan scope `delete:compliance_user_data`, yang diberikan secara terpisah
# dari `read:compliance_user_data` saat Compliance Access Key dibuat.
# Pastikan Anda memiliki otorisasi eksplisit sebelum menjalankan ini.

chat_id="claude_chat_01H5CWunD7RpVJ5bHa8RCkja"

curl --fail-with-body -sS -X DELETE \
  "https://api.anthropic.com/v1/compliance/apps/chats/$chat_id" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```
</CodeGroup>

```json Response
{
  "id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja",
  "type": "claude_chat_deleted"
}
```

Setiap penghapusan yang berhasil mengembalikan envelope konfirmasi kecil dengan `id` dan diskriminator `type`. Endpoint obrolan mengembalikan `claude_chat_deleted`; periksa field `type` sebelum memperlakukan penghapusan sebagai terkonfirmasi. Lihat skema respons pada halaman [referensi API](/docs/id/api/compliance/apps) masing-masing endpoint penghapusan untuk nilai `type` persis yang dikembalikan oleh endpoint lainnya.

### Lepaskan obrolan sebelum menghapus proyek \{#detach-chats-before-deleting-a-project}

Sebuah proyek tidak dapat dihapus selama masih ada obrolan yang terlampir padanya. API mengembalikan 409 dengan body berikut:

```json
{
  "error": {
    "type": "conflict_error",
    "message": "The \"claude_proj_01KGp4eZNug9ri4kE35RSppq\" project cannot be deleted as it has chats attached to it. Delete or detach all chats, and try deleting the project again."
  }
}
```

Untuk mengatasinya, cantumkan obrolan proyek dengan `GET /v1/compliance/apps/chats?user_ids[]={user_id}&project_ids[]={project_id}` (endpoint daftar obrolan memerlukan setidaknya satu nilai `user_ids[]`; enumerasikan ID melalui [Mencantumkan pengguna organisasi](/docs/id/manage-claude/compliance-org-data#list-organization-users)), hapus masing-masing dengan `DELETE /v1/compliance/apps/chats/{claude_chat_id}` (atau pindahkan keluar dari proyek melalui claude.ai), lalu coba lagi penghapusan proyek.

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card title="Referensi API" href="/docs/id/api/compliance/apps">
    Skema permintaan dan respons lengkap untuk setiap endpoint obrolan, file, proyek, dan artifact.
  </Card>
  <Card title="Mencantumkan organisasi, pengguna, peran, dan grup" href="/docs/id/manage-claude/compliance-org-data">
    Enumerasikan orang dan tim yang terkait dengan obrolan dan proyek pada halaman ini.
  </Card>
</CardGroup>