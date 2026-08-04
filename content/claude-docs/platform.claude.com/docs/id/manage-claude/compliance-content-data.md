---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-content-data
fetched_at: 2026-08-04T03:08:17.915636Z
sha256: 74819030488a0d4bc48685ebb874555f86738aeee9ca1544c33caa2f9589b657
---

# Mengambil dan menghapus chat, file, dan proyek

Akses konten chat, lampiran file, dan proyek untuk organisasi claude.ai melalui Compliance API.

---

<Note>
  Endpoint pada halaman ini mengambil dan menghapus konten claude.ai dan hanya tersedia untuk organisasi Claude Enterprise, yang memiliki akses layanan mandiri ke Compliance API. Lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_user_data` pada Compliance Access Key. Endpoint penghapusan juga memerlukan `delete:compliance_user_data`.

  **Prasyarat:** Tidak ada untuk mencantumkan chat atau sesi jarak jauh di seluruh organisasi. Untuk memfilter daftar chat atau sesi ke pengguna tertentu, Anda memerlukan ID pengguna dari [List organization users](/docs/id/manage-claude/compliance-org-data#list-organization-users). Endpoint lain pada halaman ini menerima ID sumber daya secara langsung.
</Check>

Endpoint pada halaman ini mengekspos konten chat claude.ai, unggahan file, proyek, lampiran proyek, dan transkrip sesi jarak jauh kepada peninjau kepatuhan. Endpoint ini mendukung ekspor eDiscovery (electronic discovery), penegakan "data loss prevention" (pencegahan kehilangan data), atau DLP, dan respons penghapusan akun. Konten chat, file, dan proyek dipertahankan selama kebijakan retensi organisasi Anda mengizinkan; transkrip sesi jarak jauh dipertahankan selama 6 tahun. Chat yang telah di-soft-delete oleh pengguna di claude.ai tetap terlihat melalui Compliance API dengan `deleted_at` terisi; chat yang telah di-hard-delete (melalui Compliance API itu sendiri, atau setelah jendela retensi organisasi berakhir) tidak dapat diambil.

Kedua scope hanya diberikan pada Compliance Access Key (`sk-ant-api01-...`) yang dibuat di claude.ai; lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access) untuk menyediakannya. Scope `read:compliance_user_data` mencakup pengambilan; `delete:compliance_user_data` hanya diperlukan untuk endpoint penghapusan. Endpoint chat, file, proyek, lampiran, dan sesi tidak tersedia untuk kunci Admin API (`sk-ant-admin01-...`); panggilan yang diautentikasi dengan kunci Admin API mengembalikan [403 Forbidden](/docs/id/manage-claude/compliance-errors#403-forbidden).

Endpoint pada halaman ini melakukan paginasi dengan dua cara; lihat [Paginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results) untuk referensi lengkapnya. Setiap bagian mencatat skema mana yang berlaku.

## Mengambil chat dan pesan

Gunakan [List chats](/docs/id/api/compliance/apps/chats/list) untuk menelusuri halaman metadata chat, lalu [Get chat messages](/docs/id/api/compliance/apps/chats/messages/list) untuk mengambil konten pesan lengkap dari satu chat.

Endpoint daftar chat secara default menggunakan cakupan seluruh organisasi: hilangkan `user_ids[]` untuk menyertakan setiap chat di bawah organisasi induk Anda. Tambahkan `order_by=updated_at` untuk mengurutkan berdasarkan waktu pembaruan terakhir. Kombinasi ini adalah cara yang direkomendasikan untuk mengekspor chat dan menjaga ekspor tetap mutakhir, karena satu loop berpaginasi mengambil chat baru maupun yang dimodifikasi untuk setiap pengguna tanpa perlu mengenumerasi pengguna terlebih dahulu. Permintaan berikut mencantumkan chat yang diperbarui sejak tanggal tertentu.

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

Hasil diurutkan menaik berdasarkan bidang `order_by`, yang tertua lebih dulu, dengan seri dipecahkan oleh `id`. Paginasi menggunakan bidang kursor standar `first_id`/`last_id`/`has_more` yang dijelaskan di [Paginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results). Untuk berjalan maju menuju chat yang lebih baru, kirimkan kembali `last_id` dari respons sebagai `after_id` pada permintaan berikutnya.

Penelusuran maju itu juga merupakan cara Anda menjaga ekspor tetap mutakhir di antara beberapa eksekusi: simpan `last_id` dari halaman terakhir dan lanjutkan darinya sebagai `after_id` pada eksekusi berikutnya. Karena daftar diurutkan berdasarkan `updated_at`, chat yang berubah setelah kursor yang Anda simpan akan muncul kembali di depannya, sehingga setiap eksekusi inkremental mengembalikan chat yang benar-benar baru maupun chat lama yang telah dimodifikasi sejak itu. Proses hasil secara idempoten, dengan kunci `id` chat, untuk menangani kemunculan ulang tersebut.

Beberapa batasan berlaku untuk kueri seluruh organisasi ini. Kursor bersifat opak dan terikat pada kunci pengurutan, sehingga `after_id` yang diterbitkan di bawah satu nilai `order_by` akan ditolak dengan error 400 di bawah nilai yang lain. Batas filter waktu juga harus cocok dengan kunci pengurutan: pasangkan batas `updated_at.*` dengan `order_by=updated_at`, dan batas `created_at.*` dengan `order_by=created_at` default. Paginasi mundur dengan `before_id` tidak didukung, dan filter `project_ids[]` tidak tersedia. Lihat [List chats](/docs/id/api/compliance/apps/chats/list) untuk referensi filter lengkap.

Untuk membatasi daftar ke pengguna tertentu (misalnya, legal hold pada kustodian yang disebutkan namanya), kirimkan 1–10 nilai `user_ids[]`. Dapatkan ID dari [List organization users](/docs/id/manage-claude/compliance-org-data#list-organization-users). Kueri yang difilter berdasarkan pengguna selalu diurutkan berdasarkan `created_at` (mengirimkan `order_by=updated_at` mengembalikan error 400) dan mendukung `after_id` maupun `before_id`. Pemfilteran berdasarkan `project_ids[]` hanya tersedia dalam bentuk yang difilter berdasarkan pengguna ini.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/chats" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "user_ids[]=user_01XyDMpzjS89pFZXqSFUBDr6" \
  --data-urlencode "created_at.gte=2025-06-01T00:00:00Z" \
  --data-urlencode "limit=100"
```

Respons daftar hanya membawa metadata chat. Untuk menarik konten chat yang sebenarnya, file terlampir, dan artifact sebaris (dokumen terstruktur yang dihasilkan Claude di dalam chat), lanjutkan dengan endpoint pesan untuk setiap ID chat:

```bash cURL
chat_id="claude_chat_01H5CWunD7RpVJ5bHa8RCkja"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/chats/$chat_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

Endpoint pesan mengembalikan metadata chat ditambah array `chat_messages` yang diurutkan berdasarkan `created_at`. Ketika `limit` dihilangkan, seluruh kumpulan pesan dikembalikan dalam satu respons; kirimkan `limit`, `after_id`, atau `before_id` untuk menelusuri halaman chat yang sangat panjang. Endpoint ini juga menerima batas rentang `created_at.*` dan `updated_at.*` (`gt`, `gte`, `lt`, `lte`) dan parameter `order` (`asc` atau `desc`). Lihat [Get chat messages](/docs/id/api/compliance/apps/chats/messages/list) untuk daftar parameter lengkap. Untuk pesan pengguna, `created_at` adalah saat pesan dikirim; untuk pesan asisten, itu adalah saat Claude selesai menghasilkan pesan. Setiap pesan membawa konten teksnya dan, jika ada, file yang diunggah (biasanya pada pesan pengguna), file yang dihasilkan alat, dan artifact apa pun yang dihasilkan atau diperbarui oleh asisten (biasanya pada pesan asisten):

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

`files`, `generated_files`, dan `artifacts` masing-masing dapat bernilai `null` pada pesan tertentu. `files` adalah unggahan biner (PDF, gambar, spreadsheet) yang dilampirkan pengguna ke pesan. `generated_files` adalah file biner yang dibuat asisten selama percakapan melalui penggunaan alat (misalnya, PDF, spreadsheet, atau slide deck). `artifacts` adalah dokumen berversi (misalnya, kode atau markdown) yang dihasilkan atau diperbarui asisten dalam responsnya; sebuah artifact dapat direvisi di beberapa giliran asisten dalam chat yang sama, dan setiap revisi muncul sebagai `version_id` baru di bawah `id` artifact yang sama. Kirimkan `id` setiap entri (atau `version_id` untuk artifact) ke endpoint konten yang sesuai di [Mengambil file dan artifact](#retrieve-files-and-artifacts) untuk mengunduhnya.

## Mengambil file dan artifact

File dan artifact diunduh berdasarkan ID, tidak dicantumkan secara independen. ID berasal dari endpoint pesan chat di [Mengambil chat dan pesan](#retrieve-chats-and-messages) (array `files`, `generated_files`, dan `artifacts` pada setiap pesan) atau, untuk unggahan tingkat proyek, dari [endpoint lampiran proyek](#retrieve-projects-and-attachments).

Pilih endpoint yang cocok dengan tipe ID Anda dan data yang Anda butuhkan. Endpoint konten file yang sama melayani file chat maupun file proyek.

| Anda memiliki                  | Anda menginginkan                        | Gunakan endpoint ini                                                                            |
| ------------------------------ | ---------------------------------------- | ----------------------------------------------------------------------------------------------- |
| ID `claude_file_*`             | Konten biner file                        | [Download file content](/docs/id/api/compliance/apps/chats/files/download)                      |
| ID `claude_file_*`             | Hanya metadata file                      | [Get file metadata](/docs/id/api/compliance/apps/chats/files/retrieve)                          |
| ID `claude_gen_file_*`         | Konten biner file yang dihasilkan alat   | [Download a Claude-generated file](/docs/id/api/compliance/apps/chats/generated_files/download) |
| ID `claude_gen_file_*`         | Hanya metadata file yang dihasilkan alat | [Get generated-file metadata](/docs/id/api/compliance/apps/chats/generated_files/retrieve)      |
| ID `claude_artifact_version_*` | Teks dari satu versi artifact            | [Download artifact content](/docs/id/api/compliance/apps/artifacts/download)                    |
| ID `claude_artifact_version_*` | Hanya metadata versi artifact            | [Get artifact metadata](/docs/id/api/compliance/apps/artifacts/retrieve)                        |
| ID `claude_proj_doc_*`         | Konten teks biasa dari dokumen proyek    | [Get project document content](/docs/id/api/compliance/apps/projects/documents/retrieve)        |
| ID `claude_proj_doc_*`         | Hanya metadata dokumen proyek            | [Get project document metadata](/docs/id/api/compliance/apps/projects/documents/metadata)       |

Endpoint konten file melakukan streaming unggahan asli sebagai respons biner terpotong (chunked) dengan header berikut:

* `Content-Disposition: attachment; filename*=utf-8''<percent-encoded filename>` membawa nama file unggahan asli dalam bentuk diperluas RFC 5987. Bentuk diperluas digunakan untuk setiap nama file, bukan hanya yang non-ASCII.
* `Content-Type` membawa tipe MIME unggahan.
* `Content-MD5` membawa digest MD5 file, dikodekan base64 sebagaimana ditentukan dalam RFC 1864.
* `Transfer-Encoding: chunked` selalu disetel.

```bash cURL
file_id="claude_file_01UaT9wBcDfGhJkLmNpQrSv7"

curl --fail-with-body -sS -OJ \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  "https://api.anthropic.com/v1/compliance/apps/chats/files/$file_id/content"
```

Flag `-OJ` memberi tahu curl untuk menyimpan respons dengan nama file dari `Content-Disposition`, yaitu nama file asli yang diunggah pengguna.

Endpoint konten artifact mengembalikan isi teks dari satu versi artifact. Kirimkan `version_id` dari salah satu entri dalam array `artifacts` pesan asisten, bukan `id` stabil artifact. Setiap versi baru dari sebuah artifact memiliki `version_id` sendiri, dan Compliance API menyajikan byte persis dari versi tersebut.

## Mengambil proyek dan lampiran

Proyek menggabungkan chat terkait bersama dengan instruksi kustom, konten basis pengetahuan, dan file terlampir atau dokumen teks. Compliance API mengekspos metadata proyek, detail proyek, dan daftar lampiran yang dimiliki sebuah proyek.

* [List projects](/docs/id/api/compliance/apps/projects/list)
* [Get project details](/docs/id/api/compliance/apps/projects/retrieve)
* [List project attachments](/docs/id/api/compliance/apps/projects/attachments/list)
* [Get project document content](/docs/id/api/compliance/apps/projects/documents/retrieve)

Hasil proyek diurutkan berdasarkan tanggal pembuatan secara menaik. Hasil lampiran diurutkan berdasarkan `created_at` secara menaik, dengan seri dipecahkan oleh `id`. Respons daftar proyek dan daftar lampiran melakukan paginasi dengan token halaman `next_page` yang opak alih-alih kursor `first_id`/`last_id` yang digunakan oleh chat dan Activity Feed. Kirimkan kembali token tersebut sebagai parameter kueri `page` pada permintaan berikutnya.

### File proyek versus dokumen proyek

Lampiran proyek adalah salah satu dari dua bentuk yang berbeda, diidentifikasi oleh diskriminator `type` pada setiap entri:

Entri dengan `type` bernilai `project_file` adalah unggahan biner (PDF, gambar, spreadsheet) yang ID-nya dimulai dengan `claude_file_`; unduh dengan [Download file content](/docs/id/api/compliance/apps/chats/files/download). Entri dengan `type` bernilai `project_doc` adalah dokumen teks biasa (selalu `text/plain`) yang ID-nya dimulai dengan `claude_proj_doc_`; ambil dengan [Get project document content](/docs/id/api/compliance/apps/projects/documents/retrieve).

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

## Mengambil sesi jarak jauh

Sesi Cowork yang dimulai di web atau seluler claude.ai berjalan di lingkungan cloud yang dikelola Anthropic. Compliance API mengekspos sesi jarak jauh ini melalui dua endpoint: `GET /v1/compliance/apps/sessions/remote` mencantumkan metadata sesi, dan `GET /v1/compliance/apps/sessions/remote/{session_id}/messages` mengembalikan transkrip satu sesi. Keduanya memerlukan scope `read:compliance_user_data`, dan keduanya dihitung terhadap batas laju Compliance API bersama ditambah anggaran kedua yang khusus untuk endpoint ini; lihat [429 Too Many Requests](/docs/id/manage-claude/compliance-errors#429-too-many-requests).

<Note>
  Endpoint sesi jarak jauh berada dalam tahap beta. Tidak diperlukan penyiapan tambahan: endpoint ini bekerja dengan Compliance Access Key dan scope `read:compliance_user_data` yang sama seperti endpoint konten lainnya.
</Note>

Endpoint daftar secara default menggunakan cakupan seluruh organisasi: hilangkan `organization_ids[]` untuk menyertakan setiap organisasi claude.ai yang dapat dibaca kunci Anda, atau kirimkan hingga 500 nilai untuk mempersempit cakupan. Untuk membatasi daftar ke pengguna tertentu, kirimkan 1–10 nilai `user_ids[]` (dapatkan ID dari [List organization users](/docs/id/manage-claude/compliance-org-data#list-organization-users)); filter ini mencocokkan pengguna pemilik sesi, sehingga sesi yang dimiliki agen dikecualikan setiap kali `user_ids[]` disetel. Batasi hasil berdasarkan waktu dengan parameter rentang `created_at` (`gte`, `gt`, `lt`, `lte`, dalam format RFC 3339). Tidak ada filter `updated_at`. Permintaan berikut mencantumkan sesi yang dibuat sejak tanggal tertentu.

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

Hasil diurutkan dalam urutan kronologis terbalik (terbaru lebih dulu) berdasarkan `created_at` dan dibatasi hingga `limit` hasil per respons (default 100, maksimum 500). Endpoint ini melakukan paginasi dengan skema token halaman yang sama seperti proyek dan lampiran (lihat [Paginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results)): kirimkan kembali nilai `next_page` dari respons sebagai parameter kueri `page` pada permintaan berikutnya, dan berhenti ketika `next_page` bernilai `null`.

Sebuah sesi dimiliki oleh pengguna atau agen, tidak pernah keduanya. Untuk sesi yang dimiliki pengguna, `user` membawa ID dan alamat email pemilik (`email_address` bernilai `null` ketika pengguna tidak lagi menjadi anggota organisasi yang dapat dibaca kunci Anda) dan `agent_id` bernilai `null`. Untuk sesi yang dimiliki agen (misalnya, tugas terjadwal), `user` bernilai `null`, `agent_id` membawa ID agen (awalan `cagt_`), dan `started_by_user` mengidentifikasi manusia yang memulai eksekusi, misalnya dengan memulai tugas terjadwal; pada sesi yang dimiliki pengguna, `started_by_user` bernilai `null`.

`status` adalah salah satu dari `pending`, `active`, `paused`, `archived`, atau `failed`. Sebuah sesi berstatus `pending` saat sedang disediakan; sesi `pending` belum memiliki transkrip, dan endpoint pesan mengembalikan 404 untuknya hingga penyediaan selesai. Sesi yang telah dihapus tidak pernah dikembalikan.

`product_surface` (string atau `null`) mengidentifikasi produk yang membuat sesi. Endpoint ini saat ini hanya mengembalikan sesi dengan `product_surface` bernilai `cowork_remote`: sesi Cowork yang dimulai di web atau seluler claude.ai.

<Note>
  **Bangun handler yang kompatibel ke depan.** Teruskan nilai `status` dan `product_surface` yang tidak dikenali, dan abaikan bidang yang tidak diharapkan handler Anda, sehingga integrasi Anda tetap bekerja saat status dan permukaan produk baru dirilis.
</Note>

### Mengambil transkrip sesi

Endpoint pesan mengembalikan transkrip sesi: prompt pengguna, respons asisten, serta panggilan alat dan hasilnya. Blok pemikiran dan gambar tidak disertakan. Untuk ringkasan cakupan dan perbandingan dengan pencatatan OpenTelemetry Cowork, lihat [FAQ Compliance API](/docs/id/manage-claude/compliance-faq#data-coverage-and-retention).

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

Respons menyematkan amplop `session` di samping array `data` yang berpaginasi. Pada endpoint ini, amplop selalu memiliki `user.email_address` dan `started_by_user` yang disetel ke `null`; dapatkan nilai-nilai tersebut dari endpoint daftar sebagai gantinya.

Pesan dikembalikan dari yang tertua lebih dulu secara default; kirimkan `order=desc` untuk membalik urutan. Paginasi menggunakan skema `page`/`next_page` yang sama seperti endpoint daftar, dengan `limit` default 100 dan maksimum 1.000. Sebuah halaman dapat berakhir lebih awal ketika respons mencapai anggaran ukurannya, sehingga halaman dengan pesan lebih sedikit dari `limit` tidak berarti Anda telah mencapai akhir; terus lakukan paginasi hingga `next_page` bernilai `null`.

Setiap pesan membawa `role` (`user` atau `assistant`) dan array `content` berisi blok `text`, `tool_use`, dan `tool_result`. Nilai `created_at` pesan adalah stempel waktu commit: pesan yang berurutan dapat berbagi stempel waktu atau sedikit terbalik, jadi pertahankan urutan yang dikembalikan alih-alih mengurutkan ulang berdasarkan `created_at`. Pada sesi yang dimiliki agen, `sent_by_user_id` mencatat pengguna yang mengirim pesan pengguna tertentu ketika dapat diatribusikan; bernilai `null` jika tidak, termasuk pada semua pesan asisten. Ketika konten sebuah pesan sama sekali tidak dapat dikembalikan (misalnya, melebihi batas ukuran), pesan tersebut membawa `content_unavailable` yang disetel ke `true`.

Dua parameter membatasi berapa banyak byte dari setiap blok alat yang dikembalikan: `tool_use_input_max_bytes` dan `tool_result_max_bytes`, keduanya default 10.000 byte. Kirimkan `-1` untuk maksimum server (sekitar 1 MiB); `0` tidak valid. Blok yang terpotong oleh salah satu batas membawa `"truncated": true`, dan input `tool_use` yang terpotong tidak lagi merupakan JSON yang valid, jadi parse input alat hanya dari blok yang tidak terpotong (atau naikkan batasnya dan ambil ulang).

Endpoint pesan mengembalikan [404 Not Found](/docs/id/manage-claude/compliance-errors#404-not-found) untuk sesi `pending`, sesi yang dihapus, dan sesi di organisasi yang tidak dapat dibaca kunci Anda.

## Menghapus konten

<Warning>
  Setiap penghapusan yang berhasil bersifat permanen dan langsung. Tidak ada jendela pemulihan.
</Warning>

Compliance API mengekspos endpoint hard-delete untuk chat, file, dokumen proyek, dan seluruh proyek. Chat yang di-hard-delete tidak dapat dipulihkan, dan berhenti muncul dalam respons daftar setelahnya (sedangkan chat yang di-soft-delete dari claude.ai masih muncul dengan `deleted_at` terisi).

* [Delete chat](/docs/id/api/compliance/apps/chats/delete): juga menghapus pesan chat dan file apa pun yang dilampirkan ke pesan tersebut.
* [Delete file](/docs/id/api/compliance/apps/chats/files/delete): menangani file chat maupun file proyek.
* [Delete project document](/docs/id/api/compliance/apps/projects/documents/delete): menghapus satu dokumen proyek berdasarkan ID.
* [Delete project](/docs/id/api/compliance/apps/projects/delete): lihat [Lepaskan chat sebelum menghapus proyek](#detach-chats-before-deleting-a-project).

Keempat endpoint memerlukan scope `delete:compliance_user_data`, yang diberikan secara terpisah dari scope baca saat Compliance Access Key dibuat.

Endpoint sesi jarak jauh bersifat hanya-baca; sesi jarak jauh tidak dapat dihapus melalui Compliance API. Transkrip sesi dipertahankan selama 6 tahun; lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

Permintaan berikut menghapus satu chat. Pola yang sama berlaku untuk endpoint penghapusan lainnya; hanya URL yang berubah.

```bash cURL
# PERINGATAN: Operasi ini menghapus chat secara PERMANEN, semua pesannya,
# dan semua file yang dilampirkan. Penghapusan bersifat langsung dan tidak dapat dibatalkan.
# Operasi ini memerlukan scope `delete:compliance_user_data`, yang diberikan secara terpisah
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

Setiap penghapusan yang berhasil mengembalikan amplop konfirmasi kecil dengan `id` dan diskriminator `type`. Endpoint chat mengembalikan `claude_chat_deleted`; periksa bidang `type` sebelum menganggap penghapusan terkonfirmasi. Lihat skema respons pada halaman [referensi API](/docs/id/api/compliance/apps) setiap endpoint penghapusan untuk nilai `type` persis yang dikembalikan endpoint lainnya.

### Lepaskan chat sebelum menghapus proyek

Sebuah proyek tidak dapat dihapus selama masih ada chat yang terlampir padanya. API mengembalikan 409 dengan isi berikut:

```json
{
  "error": {
    "type": "conflict_error",
    "message": "The \"claude_proj_01KGp4eZNug9ri4kE35RSppq\" project cannot be deleted as it has chats attached to it. Delete or detach all chats, and try deleting the project again."
  }
}
```

Untuk mengatasinya, cantumkan chat proyek dengan `GET /v1/compliance/apps/chats?user_ids[]={user_id}&project_ids[]={project_id}` (filter `project_ids[]` memerlukan setidaknya satu nilai `user_ids[]`; enumerasi ID melalui [List organization users](/docs/id/manage-claude/compliance-org-data#list-organization-users)), hapus masing-masing dengan `DELETE /v1/compliance/apps/chats/{claude_chat_id}` (atau pindahkan keluar dari proyek melalui claude.ai), lalu coba lagi penghapusan proyek.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi API" href="/docs/id/api/compliance/apps">
    Skema permintaan dan respons lengkap untuk setiap endpoint chat, file, proyek, dan artifact.
  </Card>

  <Card title="Mencantumkan organisasi, pengguna, peran, grup, dan pengaturan" href="/docs/id/manage-claude/compliance-org-data">
    Enumerasi orang dan tim yang terkait dengan chat, proyek, dan sesi pada halaman ini.
  </Card>
</CardGroup>
