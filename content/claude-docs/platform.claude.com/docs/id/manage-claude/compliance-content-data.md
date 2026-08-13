---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-content-data
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: f973d07275c666784794bc4469883a21fbb88c72c6fd2ef31b6235d62ae617b9
---

---
title: Mengambil dan menghapus obrolan, file, proyek, dan sesi
url: https://platform.claude.com/docs/id/manage-claude/compliance-content-data
description: Akses konten obrolan, lampiran file, proyek, dan transkrip sesi untuk organisasi claude.ai melalui Compliance API.
---

<Note>
  Endpoint pada halaman ini hanya tersedia untuk organisasi Claude Enterprise. Endpoint ini mengambil obrolan, file, proyek claude.ai, serta transkrip sesi Cowork dan Claude Code; endpoint ini juga menghapus obrolan, file, dan proyek. Lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_user_data` pada Compliance Access Key. Endpoint penghapusan juga memerlukan `delete:compliance_user_data`.

  **Prasyarat:** Tidak ada untuk mencantumkan obrolan atau sesi di seluruh organisasi. Untuk memfilter daftar obrolan atau sesi remote ke pengguna tertentu, Anda memerlukan ID pengguna dari [Mencantumkan pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users); daftar sesi lokal tidak memiliki filter pengguna. Endpoint lain pada halaman ini menerima ID sumber daya secara langsung.
</Check>

Endpoint pada halaman ini mengekspos konten obrolan Claude Enterprise, unggahan file, proyek, lampiran proyek, dan transkrip sesi kepada peninjau kepatuhan. Endpoint ini mendukung ekspor "eDiscovery" (penemuan elektronik), penegakan "data loss prevention" (pencegahan kehilangan data), atau DLP, dan respons penghapusan akun. Konten obrolan, file, dan proyek disimpan selama kebijakan retensi organisasi Anda mengizinkan; transkrip sesi remote disimpan selama 6 tahun, dan transkrip sesi lokal (sesi Cowork dan Claude Code pada mesin pengguna Anda) selama 6 tahun secara default (atau periode retensi percakapan kustom organisasi Anda, jika periode terbatas telah ditetapkan). Obrolan yang telah di-soft-delete oleh pengguna di claude.ai tetap terlihat melalui Compliance API dengan `deleted_at` terisi; obrolan yang telah di-hard-delete (melalui Compliance API itu sendiri, atau setelah jendela retensi organisasi berakhir) tidak dapat diambil.

Kedua scope hanya diberikan pada Compliance Access Key (`sk-ant-api01-...`) yang dibuat di claude.ai; lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access) untuk menyediakannya. Scope `read:compliance_user_data` mencakup pengambilan; `delete:compliance_user_data` hanya diperlukan untuk endpoint penghapusan. Endpoint obrolan, file, proyek, lampiran, dan sesi tidak tersedia untuk Admin API key (`sk-ant-admin01-...`); panggilan yang diautentikasi dengan Admin API key mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden).

Endpoint pada halaman ini melakukan paginasi dengan dua cara; lihat [Melakukan paginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results) untuk referensi lengkap. Setiap bagian mencatat skema mana yang berlaku.

## Mengambil obrolan dan pesan

Gunakan [List chats](https://platform.claude.com/docs/id/api/compliance/apps/chats/list) untuk menelusuri metadata obrolan per halaman, lalu [Get chat messages](https://platform.claude.com/docs/id/api/compliance/apps/chats/messages/list) untuk mengambil konten pesan lengkap dari satu obrolan.

Endpoint daftar obrolan secara default mencakup seluruh organisasi: hilangkan `user_ids[]` untuk menyertakan setiap obrolan di bawah organisasi induk Anda. Tambahkan `order_by=updated_at` untuk mengurutkan berdasarkan waktu pembaruan terakhir. Kombinasi ini adalah cara yang direkomendasikan untuk mengekspor obrolan dan menjaga ekspor tetap terkini, karena satu loop paginasi menangkap obrolan baru maupun yang dimodifikasi untuk setiap pengguna tanpa perlu mengenumerasi pengguna terlebih dahulu. Permintaan berikut mencantumkan obrolan yang diperbarui sejak tanggal tertentu.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/chats" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "order_by=updated_at" \
  --data-urlencode "updated_at.gte=2025-06-01T00:00:00Z" \
  --data-urlencode "limit=100"
```

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
      "model": "claude-opus-5",
      "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
      "project_id": "claude_proj_01KGp4eZNug9ri4kE35RSppq",
      "user": {
        "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
        "email_address": "user@example.com"
      }
    }
  ],
  "has_more": true,
  "first_id": "eyJrIjogInVwZGF0ZWRfYXQiLCAidCI6ICIyMDI2LTA0LTEwVDA5OjEwOjExKzAwOjAwIiwgImlkIjogImFiY2RlZjAxLS4uLiJ9",
  "last_id": "eyJrIjogInVwZGF0ZWRfYXQiLCAidCI6ICIyMDI2LTA0LTEwVDA5OjEwOjExKzAwOjAwIiwgImlkIjogImFiY2RlZjAxLS4uLiJ9"
}
```

Hasil diurutkan secara menaik berdasarkan field `order_by`, yang terlama lebih dulu, dengan nilai yang sama dipecah berdasarkan `id`. Paginasi menggunakan field kursor standar `first_id`/`last_id`/`has_more` yang dijelaskan di [Melakukan paginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results). Untuk berjalan maju menuju obrolan yang lebih baru, kirimkan kembali `last_id` dari respons sebagai `after_id` pada permintaan berikutnya.

Penelusuran maju tersebut juga merupakan cara Anda menjaga ekspor tetap terkini di antara proses yang berjalan: simpan `last_id` dari halaman terakhir dan lanjutkan darinya sebagai `after_id` pada proses berikutnya. Karena daftar diurutkan berdasarkan `updated_at`, obrolan yang berubah setelah kursor tersimpan Anda akan muncul kembali di depannya, sehingga setiap proses inkremental mengembalikan obrolan yang benar-benar baru maupun obrolan lama yang telah dimodifikasi sejak saat itu. Proses hasil secara idempoten, dengan kunci `id` obrolan, untuk menangani kemunculan kembali tersebut.

Beberapa batasan berlaku untuk kueri seluruh organisasi ini. Kursor bersifat opaque dan terikat pada kunci pengurutan, sehingga `after_id` yang diterbitkan di bawah satu nilai `order_by` akan ditolak dengan error 400 di bawah nilai lainnya. Batas filter waktu juga harus cocok dengan kunci pengurutan: pasangkan batas `updated_at.*` dengan `order_by=updated_at`, dan batas `created_at.*` dengan `order_by=created_at` default. Paginasi mundur dengan `before_id` tidak didukung, dan filter `project_ids[]` tidak tersedia. Lihat [List chats](https://platform.claude.com/docs/id/api/compliance/apps/chats/list) untuk referensi filter lengkap.

Untuk membatasi daftar ke pengguna tertentu saja (misalnya, legal hold pada kustodian yang disebutkan namanya), kirimkan 1–10 nilai `user_ids[]`. Dapatkan ID tersebut dari [Mencantumkan pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users). Kueri yang difilter pengguna selalu diurutkan berdasarkan `created_at` (mengirimkan `order_by=updated_at` mengembalikan error 400) dan mendukung `after_id` maupun `before_id`. Pemfilteran berdasarkan `project_ids[]` hanya tersedia dalam bentuk yang difilter pengguna ini.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/chats" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "user_ids[]=user_01XyDMpzjS89pFZXqSFUBDr6" \
  --data-urlencode "created_at.gte=2025-06-01T00:00:00Z" \
  --data-urlencode "limit=100"
```

Respons daftar hanya membawa metadata obrolan. Untuk menarik konten obrolan yang sebenarnya, file terlampir, dan artifact inline (dokumen terstruktur yang dihasilkan Claude di dalam obrolan), lanjutkan dengan endpoint pesan untuk setiap ID obrolan:

```bash cURL
chat_id="claude_chat_01H5CWunD7RpVJ5bHa8RCkja"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/chats/$chat_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

Endpoint pesan mengembalikan metadata obrolan ditambah array `chat_messages` yang diurutkan berdasarkan `created_at`. Ketika `limit` dihilangkan, seluruh kumpulan pesan dikembalikan dalam satu respons; kirimkan `limit`, `after_id`, atau `before_id` untuk menelusuri obrolan yang sangat panjang per halaman. Endpoint ini juga menerima batas rentang `created_at.*` dan `updated_at.*` (`gt`, `gte`, `lt`, `lte`) serta parameter `order` (`asc` atau `desc`). Lihat [Get chat messages](https://platform.claude.com/docs/id/api/compliance/apps/chats/messages/list) untuk daftar parameter lengkap. Untuk pesan pengguna, `created_at` adalah waktu pesan dikirim; untuk pesan asisten, ini adalah waktu Claude selesai menghasilkan pesan. Setiap pesan membawa konten teksnya dan, jika ada, file yang diunggah (biasanya pada pesan pengguna), file yang dihasilkan alat, dan artifact yang dihasilkan atau diperbarui asisten (biasanya pada pesan asisten):

```json Response
{
  "id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja",
  "name": "Product Requirements Discussion",
  "created_at": "2026-04-10T08:09:10Z",
  "updated_at": "2026-04-10T09:10:11Z",
  "deleted_at": null,
  "href": "https://claude.ai/chat/abcdef01-2345-6789-abcd-ef0123456789",
  "model": "claude-opus-5",
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

`files`, `generated_files`, dan `artifacts` masing-masing dapat bernilai `null` pada pesan tertentu. `files` adalah unggahan biner (PDF, gambar, spreadsheet) yang dilampirkan pengguna ke pesan. `generated_files` adalah file biner yang dibuat asisten selama percakapan melalui penggunaan alat (misalnya, PDF, spreadsheet, atau slide deck). `artifacts` adalah dokumen berversi (misalnya, kode atau markdown) yang dihasilkan atau diperbarui asisten dalam responsnya; sebuah artifact dapat direvisi di beberapa giliran asisten dalam obrolan yang sama, dan setiap revisi muncul sebagai `version_id` baru di bawah `id` artifact yang sama. Kirimkan `id` setiap entri (atau `version_id` untuk artifact) ke endpoint konten yang sesuai di [Mengambil file dan artifact](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-files-and-artifacts) untuk mengunduhnya.

## Mengambil file dan artifact

File dan artifact diunduh berdasarkan ID, bukan dicantumkan secara independen. ID tersebut berasal dari endpoint pesan obrolan di [Mengambil obrolan dan pesan](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-chats-and-messages) (array `files`, `generated_files`, dan `artifacts` pada setiap pesan) atau, untuk unggahan tingkat proyek, dari [endpoint lampiran proyek](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-projects-and-attachments).

Pilih endpoint yang sesuai dengan tipe ID Anda dan data yang Anda butuhkan. Endpoint konten file yang sama melayani file obrolan maupun file proyek.

| Anda memiliki                  | Anda menginginkan                       | Gunakan endpoint ini                                                                                                       |
| ------------------------------ | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| ID `claude_file_*`             | Konten biner file                       | [Download file content](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/download)                      |
| ID `claude_file_*`             | Metadata file saja                      | [Get file metadata](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/retrieve)                          |
| ID `claude_gen_file_*`         | Konten biner file yang dihasilkan alat  | [Download a Claude-generated file](https://platform.claude.com/docs/id/api/compliance/apps/chats/generated_files/download) |
| ID `claude_gen_file_*`         | Metadata file yang dihasilkan alat saja | [Get generated-file metadata](https://platform.claude.com/docs/id/api/compliance/apps/chats/generated_files/retrieve)      |
| ID `claude_artifact_version_*` | Teks satu versi artifact                | [Download artifact content](https://platform.claude.com/docs/id/api/compliance/apps/artifacts/download)                    |
| ID `claude_artifact_version_*` | Metadata versi artifact saja            | [Get artifact metadata](https://platform.claude.com/docs/id/api/compliance/apps/artifacts/retrieve)                        |
| ID `claude_proj_doc_*`         | Konten teks biasa dokumen proyek        | [Get project document content](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/retrieve)        |
| ID `claude_proj_doc_*`         | Metadata dokumen proyek saja            | [Get project document metadata](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/metadata)       |

Endpoint konten file melakukan streaming unggahan asli sebagai respons biner chunked dengan header berikut:

* `Content-Disposition: attachment; filename*=utf-8''<percent-encoded filename>` membawa nama file unggahan asli dalam bentuk extended RFC 5987. Bentuk extended digunakan untuk setiap nama file, bukan hanya yang non-ASCII.
* `Content-Type` membawa tipe MIME unggahan.
* `Content-MD5` membawa digest MD5 file, dikodekan base64 sebagaimana ditentukan dalam RFC 1864.
* `Transfer-Encoding: chunked` selalu ditetapkan.

```bash cURL
file_id="claude_file_01UaT9wBcDfGhJkLmNpQrSv7"

curl --fail-with-body -sS -OJ \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  "https://api.anthropic.com/v1/compliance/apps/chats/files/$file_id/content"
```

Flag `-OJ` memberi tahu curl untuk menyimpan respons dengan nama file dari `Content-Disposition`, yang merupakan nama file asli yang diunggah pengguna.

Endpoint konten artifact mengembalikan isi teks dari satu versi artifact. Kirimkan `version_id` dari salah satu entri dalam array `artifacts` pesan asisten, bukan `id` stabil artifact. Setiap versi baru dari sebuah artifact memiliki `version_id` sendiri, dan Compliance API menyajikan byte persis dari versi tersebut.

## Mengambil proyek dan lampiran

Proyek mengelompokkan obrolan terkait bersama dengan instruksi kustom, konten basis pengetahuan, dan file atau dokumen teks terlampir. Compliance API mengekspos metadata proyek, detail proyek, dan daftar lampiran yang dimiliki sebuah proyek.

* [List projects](https://platform.claude.com/docs/id/api/compliance/apps/projects/list)
* [Get project details](https://platform.claude.com/docs/id/api/compliance/apps/projects/retrieve)
* [List project attachments](https://platform.claude.com/docs/id/api/compliance/apps/projects/attachments/list)
* [Get project document content](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/retrieve)

Hasil proyek diurutkan berdasarkan tanggal pembuatan secara menaik. Hasil lampiran diurutkan berdasarkan `created_at` secara menaik, dengan nilai yang sama dipecah berdasarkan `id`. Respons daftar proyek dan daftar lampiran melakukan paginasi dengan token halaman `next_page` yang opaque, bukan kursor `first_id`/`last_id` yang digunakan oleh obrolan dan Activity Feed. Kirimkan kembali token tersebut sebagai parameter kueri `page` pada permintaan berikutnya.

### File proyek versus dokumen proyek

Lampiran proyek adalah salah satu dari dua bentuk yang berbeda, diidentifikasi oleh diskriminator `type` pada setiap entri:

Entri dengan `type` bernilai `project_file` adalah unggahan biner (PDF, gambar, spreadsheet) yang ID-nya dimulai dengan `claude_file_`; unduh dengan [Download file content](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/download). Entri dengan `type` bernilai `project_doc` adalah dokumen teks biasa (selalu `text/plain`) yang ID-nya dimulai dengan `claude_proj_doc_`; ambil dengan [Get project document content](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/retrieve).

Konsumen yang menelusuri daftar lampiran harus bercabang berdasarkan `type` dan memanggil endpoint konten yang sesuai untuk setiap entri. Permintaan berikut mencantumkan satu halaman lampiran; lakukan paginasi dengan mengirimkan kembali `next_page` sebagai parameter `page` hingga `has_more` bernilai `false`.

```bash cURL
project_id="claude_proj_01KGp4eZNug9ri4kE35RSppq"

curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/projects/$project_id/attachments" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

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

## Mengambil sesi lokal

Sesi lokal adalah sesi Cowork dan Claude Code yang berjalan pada mesin pengguna sendiri saat pengguna masuk dengan akun Claude Enterprise mereka: Cowork di Claude Desktop, dan Claude Code di terminal, di Claude Desktop, atau di ekstensi IDE. Anthropic merekam setiap percakapan di sisi server saat permintaannya mencapai Claude API; tidak ada yang diinstal pada perangkat, dan tidak ada yang dikumpulkan di luar permintaan yang sudah dikirim klien ke Claude API.

Compliance API mengekspos sesi lokal melalui tiga endpoint: `GET /v1/compliance/apps/sessions/local` mencantumkan metadata sesi, `GET /v1/compliance/apps/sessions/local/{session_id}` mengambil metadata satu sesi, dan `GET /v1/compliance/apps/sessions/local/{session_id}/messages` mengembalikan transkrip satu sesi. Ketiganya memerlukan scope `read:compliance_user_data` dan hanya dihitung terhadap batas laju Compliance API bersama; ketiganya tidak tunduk pada batas tambahan khusus endpoint yang berlaku untuk endpoint sesi remote. Lihat [429 Too Many Requests](https://platform.claude.com/docs/id/manage-claude/compliance-errors#429-too-many-requests). Jika sesi lokal tidak tersedia untuk organisasi induk Anda, ketiga endpoint mengembalikan 404 dengan pesan `Local sessions are not available.` (lihat [Sesi lokal tidak ditemukan](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-session-not-found)); saat daftar sesi atau konten yang ditangkap tidak tersedia untuk sementara, endpoint mengembalikan 503 (lihat [Sesi lokal tidak tersedia untuk sementara](https://platform.claude.com/docs/id/manage-claude/compliance-errors#local-sessions-temporarily-unavailable)).

<Note>
  Endpoint sesi lokal masih dalam tahap beta. Endpoint ini bekerja dengan Compliance Access Key dan scope `read:compliance_user_data` yang sama seperti endpoint konten lainnya; tidak diperlukan kunci, scope, pengaturan, atau pembaruan klien baru.
</Note>

Tabel berikut merangkum perbedaan sesi lokal dengan [sesi remote](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-remote-sessions) yang dibahas kemudian di halaman ini.

|                                     | Sesi lokal                                                                                                             | Sesi remote                                                               |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Endpoint                            | Endpoint list, retrieve, dan messages di bawah `/v1/compliance/apps/sessions/local`                                    | Endpoint list dan messages di bawah `/v1/compliance/apps/sessions/remote` |
| Tempat sesi berjalan                | Mesin pengguna sendiri                                                                                                 | Lingkungan cloud yang dikelola Anthropic                                  |
| Nilai `product_surface`             | `cowork`, `claude_code`                                                                                                | `cowork_remote`                                                           |
| Prefiks ID                          | `clls_`                                                                                                                | `cse_`                                                                    |
| Filter daftar                       | Hanya rentang `created_at`                                                                                             | Organisasi, pengguna, dan rentang `created_at`                            |
| Field siklus hidup                  | Tidak ada: tidak ada `status` atau `updated_at`                                                                        | `status`, `updated_at`                                                    |
| Retensi                             | 6 tahun secara default, atau periode retensi percakapan kustom organisasi Anda, jika periode terbatas telah ditetapkan | 6 tahun                                                                   |
| Batas laju tambahan khusus endpoint | Tidak                                                                                                                  | Ya                                                                        |
| Penghapusan melalui API             | Tidak                                                                                                                  | Tidak                                                                     |

Transkrip sesi lokal menunjukkan apa yang diminta untuk dilakukan Claude dan apa yang dikembalikannya, bukan apa yang terjadi pada perangkat. Aktivitas file dan jaringan hanya terlihat melalui panggilan alat dan hasil alat dalam transkrip, sehingga aktivitas yang tidak pernah mencapai API (misalnya, file lokal yang tidak pernah dikirim sesi) tidak ditangkap.

Penangkapan terikat pada diaktifkannya Compliance API untuk organisasi Anda dan berlaku saat pengguna masuk dengan akun Claude Enterprise mereka. Sesi tidak ditangkap ketika Claude Code mengautentikasi dengan kunci API Claude Console atau berjalan melalui platform cloud pihak ketiga seperti Amazon Bedrock, Google Cloud, atau Microsoft Foundry, dan sesi Claude Code di web tidak ditangkap. Claude Code di web berjalan di lingkungan cloud yang dikelola Anthropic tetapi juga bukan sesi remote; endpoint sesi remote hanya mengembalikan sesi Cowork. Untuk organisasi dengan [kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-readiness) yang diaktifkan, tidak ada data sesi lokal yang ditangkap, sehingga endpoint ini tidak mengembalikan sesi lokal untuk organisasi tersebut. Untuk organisasi yang menggunakan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek), sesi lokal dicantumkan dan dapat diambil seperti biasa, tetapi konten transkrip saat ini tidak dikembalikan: setiap pesan pada endpoint pesan membawa `provenance.type` bernilai `content_unavailable` dengan `reason` bernilai `not_captured` dan array `content` kosong (lihat [Mengambil transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-a-local-session-transcript)).

Endpoint daftar mengembalikan metadata sesi, tanpa konten transkrip, untuk setiap organisasi tertaut yang dapat dibaca kunci Anda. Tidak seperti daftar sesi remote, endpoint ini tidak memiliki filter organisasi atau pengguna: batasi hasil dalam waktu dengan parameter `created_at.gte` dan `created_at.lt`. Keduanya menerima timestamp RFC 3339 dengan offset UTC yang wajib, dan ketika keduanya disediakan, `created_at.lt` harus benar-benar setelah `created_at.gte` atau permintaan mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request). Sesi yang berlaku [zero data retention (ZDR)](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) dikecualikan. Sesi dan pesan baru muncul dalam hasil setelah penundaan pemrosesan singkat, biasanya dalam hitungan menit; sesi yang tidak ada segera setelah dimulai belum tentu tidak tertangkap. Permintaan berikut mencantumkan sesi yang dibuat sejak tanggal tertentu.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/sessions/local" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "created_at.gte=2026-07-01T00:00:00Z" \
  --data-urlencode "limit=100"
```

```json Response
{
  "data": [
    {
      "type": "compliance_local_session",
      "id": "clls_01HxKpLmNoPqRsTuVwXyZaBc",
      "organization_uuid": "9a1e0000-0000-0000-0000-000000000000",
      "workspace_id": "wrkspc_01SvYKoWVRVHoEbwESNvzYdR",
      "user": {
        "id": "user_01GpKpLmNoPqRsTuVwXyZaBc",
        "email_address": "engineer@example.com"
      },
      "product_surface": "cowork",
      "created_at": "2026-07-09T14:02:11Z"
    },
    {
      "type": "compliance_local_session",
      "id": "clls_01HyLqMnOpQrStUvWxYzAbCd",
      "organization_uuid": "9a1e0000-0000-0000-0000-000000000000",
      "workspace_id": null,
      "user": {
        "id": "user_01HqRsTuVwXyZaBcDeFgHiJk",
        "email_address": null
      },
      "product_surface": "claude_code",
      "created_at": "2026-07-08T09:15:43Z"
    }
  ],
  "next_page": "page_AAEfQx7mPdLkq9Rt2VwHbZk"
}
```

Hasil diurutkan dalam urutan kronologis terbalik (terbaru lebih dulu) berdasarkan `created_at`, dengan nilai yang sama dipecah berdasarkan `id`, dan dibatasi pada `limit` hasil per respons (default 100, maks 500). Endpoint ini hanya melakukan paginasi maju, dengan skema token halaman yang sama seperti proyek dan lampiran (lihat [Melakukan paginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results)): kirimkan kembali nilai `next_page` dari respons sebagai parameter kueri `page` pada permintaan berikutnya, dan berhenti ketika `next_page` bernilai `null`. Respons tidak memiliki field `has_more`. Selesaikan penelusuran daftar dalam 24 jam sejak memulainya; kursor daftar yang lebih lama masih diterima tetapi dievaluasi ulang terhadap batas retensi saat ini, sehingga sesi yang aktivitas tertua yang disimpannya akan segera melewati periode retensi dapat terlewati.

Dalam setiap objek sesi, `user.id` selalu ditetapkan dan bertahan setelah penghapusan akun; `user.email_address` bernilai `null` ketika akun pengguna telah dihapus atau pengguna tidak lagi menjadi anggota organisasi yang dapat dibaca kunci Anda. `workspace_id` bernilai `null` ketika sesi tidak dikaitkan dengan workspace. Sesi lokal berkorespondensi dengan satu ID sesi klien: memulai percakapan baru di klien, atau menghapus konteksnya, memulai catatan sesi baru. Perlakukan nilai `id` sebagai string opaque; formatnya dapat berubah tanpa pemberitahuan.

Sesi lokal tidak membawa `status` dan tidak membawa `updated_at`: sesi lokal tidak memiliki siklus hidup sisi server, dan visibilitasnya diatur oleh retensi. Sesi lokal ditangkap sebagai rangkaian panggilan Claude API (panggilan inferensi) yang dibuat klien selama sesi, dan retensi berlaku untuk setiap panggilan yang ditangkap secara individual. `created_at` adalah timestamp dari panggilan tertua yang disimpan dalam sesi (UTC). Saat panggilan yang lebih lama melewati periode retensi, `created_at` maju sesuai dengan itu, dan setelah setiap panggilan dalam sesi telah melewati batas, sesi tidak lagi dikembalikan. Karena `created_at` dapat bergeser di antara proses yang berjalan, lakukan deduplikasi pada `id` ketika Anda menelusuri ulang daftar dari waktu ke waktu. `created_at` sesi tidak bergerak lebih lambat saat sesi berlanjut, dan tidak ada `updated_at`, sehingga sesi yang mendapat pesan setelah Anda pertama kali mengekspornya tidak muncul kembali di jendela `created_at` berikutnya. Untuk menjaga transkrip tetap terkini, cantumkan ulang jendela trailing setidaknya sepanjang sesi terlama Anda pada setiap proses dan ambil ulang transkrip sesi yang dikembalikannya, dengan melakukan deduplikasi pesan pada `id`.

Daftar dibangun dari metadata aktivitas sesi, sehingga dapat menyertakan sesi yang konten transkripnya tidak ditangkap, misalnya sesi yang berjalan sebelum penangkapan dimulai untuk organisasi Anda (sejauh periode retensi Anda mengizinkan); setiap pesan dalam transkrip sesi tersebut membawa `provenance.type` bernilai `content_unavailable` dengan `reason` bernilai `not_captured` (lihat [Mengambil transkrip sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-a-local-session-transcript)).

Konten sesi lokal yang ditangkap disimpan selama 6 tahun sejak penangkapan secara default. Jika organisasi yang menjalankan sesi telah menetapkan periode retensi percakapan kustom yang terbatas di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), periode tersebut yang berlaku, baik lebih pendek maupun lebih panjang dari default; ketika organisasi memiliki lebih dari satu periode retensi kustom yang dikonfigurasi, yang terpendek yang berlaku. Perubahan pada pengaturan tersebut berlaku dengan dua cara berbeda: endpoint berhenti mengembalikan aktivitas yang lebih lama dari periode organisasi saat ini segera setelah pengaturan berubah, sedangkan setiap pesan yang ditangkap disimpan selama periode yang berlaku saat pesan ditangkap, sehingga memperpanjang periode di kemudian hari tidak memulihkan konten yang sudah kedaluwarsa.

Untuk mengambil metadata satu sesi secara langsung, kirimkan ID-nya ke `GET /v1/compliance/apps/sessions/local/{session_id}`. Responsnya adalah objek sesi yang sama dengan yang dikembalikan endpoint daftar, tanpa envelope dan tanpa konten transkrip. ID sesi yang salah format mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request). Satu [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found) mencakup empat kasus yang tidak dibedakan oleh respons: sesi tidak berada dalam organisasi yang dapat dibaca kunci Anda (termasuk sesi di bawah organisasi induk lain), sesi tidak ada, zero data retention berlaku untuknya, atau setiap panggilan di dalamnya telah melewati retensi.

`product_surface` (string atau `null`) mengidentifikasi produk yang membuat sesi: `cowork` untuk sesi Cowork di Claude Desktop, dan `claude_code` untuk sesi Claude Code. Nilai baru muncul seiring cakupan diperluas.

<Note>
  **Bangun handler yang kompatibel ke depan.** Teruskan nilai `product_surface` yang tidak dikenali, dan abaikan field yang tidak diharapkan handler Anda, sehingga integrasi Anda tetap berfungsi saat product surface baru dirilis.
</Note>

### Mengambil transkrip sesi lokal

Endpoint pesan mengembalikan transkrip sesi, direkonstruksi dari panggilan Claude API yang ditangkap: prompt pengguna, teks asisten, panggilan alat, dan bagian teks dari hasil alat, semuanya dikembalikan sebagaimana dikirim selain pemotongan ukuran. Tidak ada yang menyamarkan URL, kredensial, atau data pribadi dalam konten tersebut, jadi perlakukan transkrip sebagai data sensitif. Transkrip menghilangkan atau mengganti hal berikut:

* Blok thinking tidak pernah disertakan.
* Prompt sistem permintaan tidak pernah dikembalikan. Pesan penanda bertuliskan `[system prompt content not shown]` menggantikannya (biasanya sekali per sesi; sesi tanpa konten yang ditangkap tidak membawa penanda).
* Definisi alat dan konfigurasi server MCP bukan bagian dari transkrip.
* Gambar, PDF, dan blok biner atau terstruktur lainnya tidak dikembalikan. Masing-masing muncul sebagai blok `text` bertuliskan `[<block type> content not shown]` (misalnya, `[image content not shown]`) dengan `truncated` ditetapkan ke `true`. Item non-teks di dalam hasil alat digantikan oleh satu entri `[N non-text item(s) not shown]`, dan `truncated` pada blok hasil alat bernilai `true`.
* Metadata sitasi pada blok `text` dihilangkan, dan blok yang terpengaruh membawa `truncated` yang ditetapkan ke `true`.

File instruksi proyek seperti `CLAUDE.md` muncul sebagai konten peran pengguna biasa. Konten skill muncul ketika klien mengirimkannya sebagai konten pesan dan tidak dibedakan dari teks pengguna lainnya. Untuk ringkasan cakupan dan perbandingan dengan logging OpenTelemetry untuk Cowork dan Claude Code, lihat [FAQ Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-faq#data-coverage-and-retention).

```bash cURL
session_id="clls_01HxKpLmNoPqRsTuVwXyZaBc"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/sessions/local/$session_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

```json Response
{
  "session": {
    "type": "compliance_local_session",
    "id": "clls_01HxKpLmNoPqRsTuVwXyZaBc",
    "organization_uuid": "9a1e0000-0000-0000-0000-000000000000",
    "workspace_id": "wrkspc_01SvYKoWVRVHoEbwESNvzYdR",
    "user": {
      "id": "user_01GpKpLmNoPqRsTuVwXyZaBc",
      "email_address": null
    },
    "product_surface": "cowork",
    "created_at": "2026-07-09T14:02:11Z"
  },
  "data": [
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBa",
      "role": "user",
      "created_at": "2026-07-09T14:02:11Z",
      "provenance": {
        "type": "synthetic_marker"
      },
      "content": [
        {
          "type": "text",
          "text": "[system prompt content not shown]",
          "truncated": true
        }
      ]
    },
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBc",
      "role": "user",
      "created_at": "2026-07-09T14:02:11Z",
      "provenance": null,
      "content": [
        {
          "type": "text",
          "text": "Fix the failing test in tests/auth_test.py",
          "truncated": false
        }
      ]
    },
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBd",
      "role": "assistant",
      "created_at": "2026-07-09T14:02:11Z",
      "provenance": null,
      "content": [
        {
          "type": "text",
          "text": "I'll read the test file first.",
          "truncated": false
        },
        {
          "type": "tool_use",
          "id": "toolu_01AbCdEfGhIjKlMnOpQrSt",
          "name": "Read",
          "input": "{\"file_path\":\"tests/auth_test.py\"}",
          "truncated": false
        }
      ]
    },
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBe",
      "role": "user",
      "created_at": "2026-07-09T14:02:38Z",
      "provenance": null,
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01AbCdEfGhIjKlMnOpQrSt",
          "name": "Read",
          "is_error": false,
          "content": [
            {
              "type": "text",
              "text": "def test_login_expiry():\n    ..."
            }
          ],
          "truncated": false
        }
      ]
    },
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBf",
      "role": "assistant",
      "created_at": "2026-07-09T14:02:38Z",
      "provenance": null,
      "content": [
        {
          "type": "text",
          "text": "The test was asserting on a stale expiry timestamp. I've updated it.",
          "truncated": false
        }
      ]
    }
  ],
  "next_page": null
}
```

Respons menyematkan envelope `session` di samping array `data` yang dipaginasi. Record pertama dalam contoh ini adalah penanda yang menggantikan prompt sistem permintaan; `provenance`-nya dijelaskan kemudian di bagian ini. Pada endpoint ini `user.email_address` selalu `null`: endpoint pesan tidak me-resolve alamat email, sehingga `null` di sini tidak berarti akun pengguna telah dihapus. Untuk mengatribusikan sesi ke alamat email, gabungkan `user.id` dengan [endpoint daftar](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-local-sessions) atau endpoint retrieve (`GET /v1/compliance/apps/sessions/local/{session_id}`).

Pesan dikembalikan dari yang terlama lebih dulu secara default; kirimkan `order=desc` untuk membalik. Paginasi menggunakan skema `page`/`next_page` yang sama seperti endpoint daftar, dengan `limit` default 100 dan maks 1.000. Sebuah halaman dapat berakhir lebih awal ketika respons mencapai batas ukurannya, sehingga halaman dengan pesan lebih sedikit dari `limit` tidak berarti Anda telah mencapai akhir; terus lakukan paginasi hingga `next_page` bernilai `null`. Kursor halaman terikat pada sesi dan urutan pengurutan tempat kursor diterbitkan, dan kursor penelusuran kedaluwarsa 24 jam setelah halaman pertamanya: kursor yang kedaluwarsa mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request) yang memberi tahu Anda untuk memulai ulang tanpa parameter `page`, dan penelusuran yang dimulai ulang mencerminkan batas retensi saat ini. Kursor yang diterbitkan untuk sesi atau `order` yang berbeda juga mengembalikan 400, sebagai kursor yang tidak valid.

Setiap pesan membawa `role` (`user` atau `assistant`) dan array `content` berisi blok `text`, `tool_use`, dan `tool_result`. Blok `text` membawa `text` dan `truncated`. Blok `tool_use` membawa `id`, `name`, `input`, dan `truncated`, di mana `input` adalah string yang dikodekan JSON, bukan objek. Blok `tool_result` membawa `tool_use_id`, `name`, `is_error`, array `content` berisi entri `text`, dan `truncated`. Panggilan dan hasil alat MCP, serta sebagian besar panggilan dan hasil alat server, dinormalisasi ke dalam bentuk `tool_use` dan `tool_result` yang sama ini; tipe blok lainnya muncul sebagai placeholder `[<block type> content not shown]`. `id` pesan bersifat stabil selama giliran tersebut disimpan. Setiap pesan yang direkonstruksi dari panggilan inferensi yang sama membawa timestamp panggilan tersebut, sehingga pesan berurutan sering berbagi nilai `created_at`; pertahankan urutan yang dikembalikan daripada mengurutkan ulang berdasarkan timestamp.

Setiap pesan juga membawa field `provenance` yang menjelaskan bagaimana kontennya ditangkap. `provenance` bernilai `null` untuk konten terverifikasi yang ditangkap oleh Claude API, yang merupakan kasus umum. Jika tidak, ini adalah objek yang `type`-nya menandai pengecualian:

* `content_unavailable` berarti konten tidak dapat dikembalikan. Array `content` kosong, dan `provenance.reason` menyatakan alasannya. `not_captured` berarti tidak ada konten yang tersedia untuk giliran tersebut; ini tidak membuktikan bahwa tidak ada record yang disimpan, karena konten yang ditahan oleh kebijakan akses sisi penyimpanan dilaporkan dengan alasan yang sama (misalnya, di organisasi yang menggunakan kunci enkripsi yang dikelola pelanggan, sebagaimana dijelaskan di [Mengambil sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-local-sessions)), dan giliran individual dalam sesi yang selain itu tertangkap dapat tidak tersedia karena alasan penanganan data lainnya dan membawa alasan yang sama. `cmek_key_revoked` dicadangkan untuk konten yang dienkripsi di bawah kunci yang dikelola pelanggan organisasi Anda ketika kunci tersebut tidak tersedia (misalnya, dicabut); saat ini tidak dikembalikan, jadi tangani untuk kompatibilitas ke depan. `retention_elapsed` berarti konten telah melewati retensi. `oversize` berarti satu pesan melebihi batas ukuran per pesan; pesan tetap dikembalikan, dengan array `content` kosong.
* `client_asserted` menandai pesan asisten yang disediakan klien sebagai riwayat percakapan dan yang tidak dapat dicocokkan dengan respons yang ditangkap; kepengarangannya tidak diverifikasi.
* `synthetic_marker` menandai record yang dihasilkan oleh endpoint itu sendiri, seperti penanda yang menggantikan prompt sistem. Ketika klien menulis ulang atau memadatkan riwayat percakapannya di tengah sesi (misalnya, setelah pemadatan konteks), transkrip menyisipkan pesan penanda pada titik tersebut dan melanjutkan dengan konten baru yang dikirim klien; ketika organisasi Anda memiliki periode retensi terbatas, riwayat yang ditulis ulang itu sendiri ditahan (penanda kedua mencatat hal ini) dan hanya giliran pengguna terbaru dan yang mengikutinya yang ditampilkan.

Pesan penanda dan client-asserted dimulai dengan blok `text` penjelasan dalam kurung siku yang ditandai `truncated: true`, misalnya `[system prompt content not shown]`. Perlakukan record ini sebagai ada tetapi tidak tersedia atau tidak terverifikasi, bukan hilang, dan toleransi tipe dan alasan `provenance` yang tidak dikenali.

Dua parameter membatasi berapa banyak byte dari setiap blok alat yang dikembalikan: `tool_use_input_max_bytes` dan `tool_result_max_bytes`, keduanya default 10.000 byte. Kirimkan `-1` untuk maksimum server (sekitar 1 MiB per string); `0` mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request), dan nilai di atas maksimum dibatasi ke maksimum tersebut. String yang terpotong oleh salah satu batas dipotong pada batas karakter dan memiliki sufiks in-band yang ditambahkan (misalnya, `…[truncated; pass tool_result_max_bytes=-1 for the server max]`), dan bloknya membawa `"truncated": true`. Oleh karena itu, `input` `tool_use` yang terpotong tidak lagi merupakan JSON yang valid, jadi parse input alat hanya dari blok yang tidak terpotong (atau naikkan batas dan ambil ulang). Blok bertipe `text` selalu dibatasi pada maksimum server yang sama sekitar 1 MiB; tidak ada parameter yang menaikkannya, dan blok `text` pada batas tersebut juga membawa `"truncated": true`.

Konten transkrip mematuhi periode retensi yang dijelaskan di [Mengambil sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-local-sessions). Ketika awal sesi telah melewatinya, transkrip dimulai dengan satu placeholder `content_unavailable` dengan `reason` bernilai `retention_elapsed`, dan pesan yang disimpan mengikutinya. Ketika setiap panggilan dalam sesi telah melewati batas, endpoint pesan mengembalikan [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found), sebagaimana halnya untuk sesi di organisasi yang tidak dapat dibaca kunci Anda, sesi yang tidak ada, dan sesi yang berlaku zero data retention. ID sesi yang salah format mengembalikan [400 Bad Request](https://platform.claude.com/docs/id/manage-claude/compliance-errors#400-bad-request).

## Mengambil sesi jarak jauh

Sesi Cowork yang dimulai di claude.ai web atau seluler berjalan di lingkungan cloud yang dikelola Anthropic. Compliance API mengekspos sesi jarak jauh ini melalui dua endpoint: `GET /v1/compliance/apps/sessions/remote` mencantumkan metadata sesi, dan `GET /v1/compliance/apps/sessions/remote/{session_id}/messages` mengembalikan transkrip satu sesi. Keduanya memerlukan scope `read:compliance_user_data`, dan keduanya dihitung terhadap batas laju Compliance API bersama ditambah anggaran kedua yang khusus untuk endpoint ini; lihat [429 Too Many Requests](https://platform.claude.com/docs/id/manage-claude/compliance-errors#429-too-many-requests).

<Note>
  Endpoint sesi jarak jauh masih dalam versi beta. Tidak diperlukan pengaturan tambahan: endpoint ini bekerja dengan Compliance Access Key dan scope `read:compliance_user_data` yang sama seperti endpoint konten lainnya.
</Note>

Endpoint daftar secara default menggunakan cakupan seluruh organisasi: hilangkan `organization_ids[]` untuk menyertakan setiap organisasi claude.ai yang dapat dibaca oleh kunci Anda, atau berikan hingga 500 nilai untuk mempersempit cakupan. Untuk membatasi daftar ke pengguna tertentu, berikan 1–10 nilai `user_ids[]` (dapatkan ID dari [Mencantumkan pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users)); filter ini mencocokkan pengguna pemilik sesi, sehingga sesi yang dimiliki agen dikecualikan setiap kali `user_ids[]` diatur. Batasi hasil berdasarkan waktu dengan parameter rentang `created_at` (`gte`, `gt`, `lt`, `lte`, dalam format RFC 3339). Tidak ada filter `updated_at`. Permintaan berikut mencantumkan sesi yang dibuat sejak tanggal tertentu.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/sessions/remote" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "created_at.gte=2026-06-01T00:00:00Z" \
  --data-urlencode "limit=100"
```

```json Response
{
  "data": [
    {
      "id": "cse_01WpQrStUvXyZaBcDeFgHjK6",
      "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
      "user": {
        "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
        "email_address": "user@example.com"
      },
      "agent_id": null,
      "started_by_user": null,
      "status": "active",
      "created_at": "2026-07-01T17:04:05Z",
      "updated_at": "2026-07-01T18:00:41Z",
      "product_surface": "cowork_remote"
    },
    {
      "id": "cse_01TkNpRsUvWxYzAbCdEfGhJ4",
      "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
      "user": null,
      "agent_id": "cagt_01MnPqRsTuVwXyZaBcDeFgH8",
      "started_by_user": {
        "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
        "email_address": "user@example.com"
      },
      "status": "archived",
      "created_at": "2026-06-28T09:15:22Z",
      "updated_at": "2026-06-28T09:47:10Z",
      "product_surface": "cowork_remote"
    }
  ],
  "next_page": "page_AAEfMk93cXpYdGxrZXk"
}
```

Hasil diurutkan dalam urutan kronologis terbalik (terbaru lebih dulu) berdasarkan `created_at` dan dibatasi pada `limit` hasil per respons (default 100, maksimum 500). Endpoint ini melakukan paginasi dengan skema page-token yang sama seperti proyek dan lampiran (lihat [Melakukan paginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results)): berikan kembali nilai `next_page` dari respons sebagai parameter kueri `page` pada permintaan berikutnya, dan berhenti ketika `next_page` bernilai `null`.

Sebuah sesi dimiliki oleh pengguna atau agen, tidak pernah keduanya. Untuk sesi yang dimiliki pengguna, `user` berisi ID dan alamat email pemilik (`email_address` bernilai `null` ketika pengguna tidak lagi menjadi anggota organisasi yang dapat dibaca oleh kunci Anda) dan `agent_id` bernilai `null`. Untuk sesi yang dimiliki agen (misalnya, tugas terjadwal), `user` bernilai `null`, `agent_id` berisi ID agen (prefiks `cagt_`), dan `started_by_user` mengidentifikasi manusia yang memulai eksekusi, misalnya dengan memulai tugas terjadwal; pada sesi yang dimiliki pengguna, `started_by_user` bernilai `null`.

`status` adalah salah satu dari `pending`, `active`, `paused`, `archived`, atau `failed`. Sebuah sesi berstatus `pending` saat sedang disediakan; sesi `pending` belum memiliki transkrip, dan endpoint pesan mengembalikan 404 untuk sesi tersebut hingga penyediaan selesai. Sesi yang telah dihapus tidak pernah dikembalikan.

`product_surface` (string atau `null`) mengidentifikasi produk yang membuat sesi. Endpoint saat ini hanya mengembalikan sesi dengan `product_surface` bernilai `cowork_remote`: sesi Cowork yang dimulai di claude.ai web atau seluler.

<Note>
  **Bangun handler yang kompatibel ke depan.** Teruskan nilai `status` dan `product_surface` yang tidak dikenali, dan abaikan field yang tidak diharapkan oleh handler Anda, sehingga integrasi Anda tetap berfungsi saat status dan product surface baru dirilis.
</Note>

### Mengambil transkrip sesi jarak jauh

Endpoint pesan mengembalikan transkrip sesi: prompt pengguna, respons asisten, serta pemanggilan dan hasil alat. Blok thinking dan gambar tidak disertakan. Untuk ringkasan cakupan dan perbandingan dengan logging OpenTelemetry Cowork, lihat [FAQ Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-faq#data-coverage-and-retention).

```bash cURL
session_id="cse_01WpQrStUvXyZaBcDeFgHjK6"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/sessions/remote/$session_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

```json Response
{
  "session": {
    "id": "cse_01WpQrStUvXyZaBcDeFgHjK6",
    "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
    "user": {
      "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
      "email_address": null
    },
    "agent_id": null,
    "started_by_user": null,
    "status": "active",
    "created_at": "2026-07-01T17:04:05Z",
    "updated_at": "2026-07-01T18:00:41Z",
    "product_surface": "cowork_remote"
  },
  "data": [
    {
      "id": "csev_01HjKmNpQrStUvWxYzAbCdE2",
      "role": "user",
      "created_at": "2026-07-01T17:04:05Z",
      "content": [
        {
          "type": "text",
          "text": "Summarize the customer feedback in the attached spreadsheet."
        }
      ],
      "sent_by_user_id": null,
      "content_unavailable": false
    },
    {
      "id": "csev_01BcDeFgHjKmNpQrStUvWxY4",
      "role": "assistant",
      "created_at": "2026-07-01T17:04:06Z",
      "content": [
        {
          "type": "text",
          "text": "I'll start by reading the spreadsheet..."
        }
      ],
      "sent_by_user_id": null,
      "content_unavailable": false
    }
  ],
  "next_page": null
}
```

Respons menyematkan envelope `session` di samping array `data` yang dipaginasi. Pada endpoint ini, envelope selalu memiliki `user.email_address` dan `started_by_user` yang diatur ke `null`; dapatkan nilai-nilai tersebut dari endpoint daftar sebagai gantinya.

Pesan dikembalikan dari yang terlama lebih dulu secara default; berikan `order=desc` untuk membalik urutan. Paginasi menggunakan skema `page`/`next_page` yang sama seperti endpoint daftar, dengan `limit` default 100 dan maksimum 1.000. Sebuah halaman dapat berakhir lebih awal ketika respons mencapai anggaran ukurannya, sehingga halaman dengan pesan lebih sedikit dari `limit` tidak berarti Anda telah mencapai akhir; terus lakukan paginasi hingga `next_page` bernilai `null`.

Setiap pesan memiliki `role` (`user` atau `assistant`) dan array `content` yang terdiri dari blok `text`, `tool_use`, dan `tool_result`. Nilai `created_at` pesan adalah timestamp commit: pesan berurutan dapat memiliki timestamp yang sama atau sedikit terbalik, jadi pertahankan urutan yang dikembalikan alih-alih mengurutkan ulang berdasarkan `created_at`. Pada sesi yang dimiliki agen, `sent_by_user_id` mencatat pengguna yang mengirim pesan pengguna tertentu ketika dapat diatribusikan; nilainya `null` dalam kasus lain, termasuk pada semua pesan asisten. Ketika konten pesan tidak dapat dikembalikan sama sekali (misalnya, melebihi batas ukuran), pesan tersebut memiliki `content_unavailable` yang diatur ke `true`.

Dua parameter membatasi berapa banyak byte dari setiap blok alat yang dikembalikan: `tool_use_input_max_bytes` dan `tool_result_max_bytes`, keduanya default ke 10.000 byte. Berikan `-1` untuk maksimum server (sekitar 1 MiB); `0` tidak valid. Blok yang terpotong oleh salah satu batas tersebut memiliki `"truncated": true`, dan input `tool_use` yang terpotong tidak lagi merupakan JSON yang valid, jadi parse input alat hanya dari blok yang tidak terpotong (atau naikkan batas dan ambil ulang).

Endpoint pesan mengembalikan [404 Not Found](https://platform.claude.com/docs/id/manage-claude/compliance-errors#404-not-found) untuk sesi `pending`, sesi yang dihapus, dan sesi dalam organisasi yang tidak dapat dibaca oleh kunci Anda.

## Menghapus konten

<Warning>
  Setiap penghapusan yang berhasil bersifat permanen dan langsung. Tidak ada jendela pemulihan.
</Warning>

Compliance API mengekspos endpoint hard-delete untuk obrolan, file, dokumen proyek, dan seluruh proyek. Obrolan yang di-hard-delete tidak dapat dipulihkan, dan berhenti muncul dalam respons daftar setelahnya (sedangkan obrolan yang di-soft-delete dari claude.ai masih muncul dengan `deleted_at` terisi).

* [Menghapus obrolan](https://platform.claude.com/docs/id/api/compliance/apps/chats/delete): juga menghapus pesan obrolan dan file apa pun yang dilampirkan ke pesan tersebut.
* [Menghapus file](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/delete): menangani file obrolan dan file proyek.
* [Menghapus dokumen proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/delete): menghapus satu dokumen proyek berdasarkan ID.
* [Menghapus proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/delete): lihat [Lepaskan obrolan sebelum menghapus proyek](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#detach-chats-before-deleting-a-project).

Keempat endpoint memerlukan scope `delete:compliance_user_data`, yang diberikan secara terpisah dari scope baca saat Compliance Access Key dibuat.

Endpoint sesi bersifat hanya-baca; sesi lokal dan jarak jauh tidak dapat dihapus melalui Compliance API. Transkrip sesi jarak jauh disimpan selama 6 tahun, dan transkrip sesi lokal selama 6 tahun secara default, atau periode retensi percakapan kustom organisasi Anda, ketika periode terbatas diatur; lihat [Mengambil sesi lokal](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-local-sessions) dan [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).

Permintaan berikut menghapus satu obrolan. Pola yang sama berlaku untuk endpoint penghapusan lainnya; hanya URL yang berubah.

```bash cURL
# PERINGATAN: Operasi ini menghapus obrolan secara PERMANEN, termasuk semua pesannya
# dan file yang dilampirkan. Penghapusan terjadi seketika dan tidak dapat dibatalkan.
# Operasi ini memerlukan scope `delete:compliance_user_data`, yang diberikan terpisah
# dari `read:compliance_user_data` saat Compliance Access Key dibuat.
# Pastikan Anda memiliki otorisasi eksplisit sebelum menjalankan ini.

chat_id="claude_chat_01H5CWunD7RpVJ5bHa8RCkja"

curl --fail-with-body -sS -X DELETE \
  "https://api.anthropic.com/v1/compliance/apps/chats/$chat_id" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

```json Response
{
  "id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja",
  "type": "claude_chat_deleted"
}
```

Setiap penghapusan yang berhasil mengembalikan envelope konfirmasi kecil dengan `id` dan diskriminator `type`. Endpoint obrolan mengembalikan `claude_chat_deleted`; periksa field `type` sebelum memperlakukan penghapusan sebagai terkonfirmasi. Lihat skema respons pada halaman [referensi API](https://platform.claude.com/docs/id/api/compliance/apps) masing-masing endpoint penghapusan untuk nilai `type` persis yang dikembalikan oleh endpoint lainnya.

### Lepaskan obrolan sebelum menghapus proyek

Sebuah proyek tidak dapat dihapus selama masih ada obrolan yang terlampir padanya. API mengembalikan 409 dengan body ini:

```json
{
  "error": {
    "type": "conflict_error",
    "message": "The \"claude_proj_01KGp4eZNug9ri4kE35RSppq\" project cannot be deleted as it has chats attached to it. Delete or detach all chats, and try deleting the project again."
  }
}
```

Untuk mengatasinya, cantumkan obrolan proyek dengan `GET /v1/compliance/apps/chats?user_ids[]={user_id}&project_ids[]={project_id}` (filter `project_ids[]` memerlukan setidaknya satu nilai `user_ids[]`; enumerasi ID melalui [Mencantumkan pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users)), hapus masing-masing dengan `DELETE /v1/compliance/apps/chats/{claude_chat_id}` (atau pindahkan keluar dari proyek melalui claude.ai), lalu coba lagi penghapusan proyek.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi API" href="https://platform.claude.com/docs/id/api/compliance/apps">
    Skema permintaan dan respons lengkap untuk setiap endpoint obrolan, file, proyek, dan artifact.
  </Card>

  <Card title="Mencantumkan organisasi, pengguna, peran, grup, dan pengaturan" href="https://platform.claude.com/docs/id/manage-claude/compliance-org-data">
    Enumerasi orang dan tim yang terkait dengan obrolan, proyek, dan sesi di halaman ini.
  </Card>
</CardGroup>
