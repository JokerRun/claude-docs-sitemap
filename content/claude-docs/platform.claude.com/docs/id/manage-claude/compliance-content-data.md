---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-content-data
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 82a6cc64aa9b547466ad4feb9c157db3b51969728ae769f46c02006c3a7ad680
---

# Mengambil dan menghapus chat, file, dan proyek

Akses konten chat, lampiran file, dan proyek untuk organisasi claude.ai melalui Compliance API.

---

<Note>
  Endpoint pada halaman ini mengambil dan menghapus konten claude.ai dan hanya tersedia untuk organisasi Claude Enterprise, yang memiliki akses mandiri ke Compliance API. Lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_user_data` pada Compliance Access Key. Endpoint penghapusan juga memerlukan `delete:compliance_user_data`.

  **Prasyarat:** Tidak ada untuk mencantumkan chat di seluruh organisasi. Untuk memfilter daftar chat ke pengguna tertentu, Anda memerlukan ID pengguna dari [List organization users](/docs/id/manage-claude/compliance-org-data#list-organization-users). Endpoint lain pada halaman ini menerima ID sumber daya secara langsung.
</Check>

Endpoint pada halaman ini mengekspos konten chat claude.ai, unggahan file, proyek, dan lampiran proyek kepada peninjau kepatuhan. Endpoint ini mendukung ekspor eDiscovery (electronic discovery), penegakan "data loss prevention" (pencegahan kehilangan data), atau DLP, dan respons penghapusan akun. Konten disimpan selama kebijakan retensi organisasi Anda mengizinkan. Chat yang telah dihapus secara lunak (soft-delete) oleh pengguna di claude.ai tetap terlihat melalui Compliance API dengan `deleted_at` terisi; chat yang telah dihapus secara permanen (hard-delete) (melalui Compliance API itu sendiri, atau setelah jendela retensi organisasi berakhir) tidak dapat diambil.

Kedua scope hanya diberikan pada Compliance Access Key (`sk-ant-api01-...`) yang dibuat di claude.ai; lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access) untuk menyediakannya. Scope `read:compliance_user_data` mencakup pengambilan data; `delete:compliance_user_data` hanya diperlukan untuk endpoint penghapusan. Endpoint chat, file, proyek, dan lampiran tidak tersedia untuk kunci Admin API (`sk-ant-admin01-...`); panggilan yang diautentikasi dengan kunci Admin API mengembalikan [403 Forbidden](/docs/id/manage-claude/compliance-errors#403-forbidden).

Endpoint pada halaman ini melakukan paginasi dengan dua cara; lihat [Paginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results) untuk referensi lengkapnya. Setiap bagian mencatat skema mana yang berlaku.

## Mengambil chat dan pesan

Gunakan [List chats](/docs/id/api/compliance/apps/chats/list) untuk menelusuri metadata chat per halaman, lalu [Get chat messages](/docs/id/api/compliance/apps/chats/messages/list) untuk mengambil konten pesan lengkap dari satu chat.

Endpoint daftar chat secara default mencakup seluruh organisasi: hilangkan `user_ids[]` untuk menyertakan setiap chat di bawah organisasi induk Anda. Tambahkan `order_by=updated_at` untuk mengurutkan berdasarkan waktu pembaruan terakhir. Kombinasi ini adalah cara yang direkomendasikan untuk mengekspor chat dan menjaga ekspor tetap mutakhir, karena satu loop berpaginasi mengambil chat baru maupun yang dimodifikasi untuk setiap pengguna tanpa perlu mengenumerasi pengguna terlebih dahulu. Permintaan berikut mencantumkan chat yang diperbarui sejak tanggal tertentu.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/apps/chats" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    --data-urlencode "order_by=updated_at" \
    --data-urlencode "updated_at.gte=2025-06-01T00:00:00Z" \
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
  "first_id": "eyJrIjogInVwZGF0ZWRfYXQiLCAidCI6ICIyMDI2LTA0LTEwVDA5OjEwOjExKzAwOjAwIiwgImlkIjogImFiY2RlZjAxLS4uLiJ9",
  "last_id": "eyJrIjogInVwZGF0ZWRfYXQiLCAidCI6ICIyMDI2LTA0LTEwVDA5OjEwOjExKzAwOjAwIiwgImlkIjogImFiY2RlZjAxLS4uLiJ9"
}
```

Hasil diurutkan secara menaik berdasarkan field `order_by`, yang terlama lebih dulu, dengan seri dipecahkan oleh `id`. Paginasi menggunakan field kursor standar `first_id`/`last_id`/`has_more` yang dijelaskan di [Paginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results). Untuk bergerak maju menuju chat yang lebih baru, kirimkan kembali `last_id` dari respons sebagai `after_id` pada permintaan berikutnya.

Penelusuran maju tersebut juga merupakan cara Anda menjaga ekspor tetap mutakhir di antara beberapa kali eksekusi: simpan `last_id` dari halaman terakhir dan lanjutkan darinya sebagai `after_id` pada eksekusi berikutnya. Karena daftar diurutkan berdasarkan `updated_at`, chat yang berubah setelah kursor yang Anda simpan akan muncul kembali di depannya, sehingga setiap eksekusi inkremental mengembalikan baik chat yang benar-benar baru maupun chat lama yang telah dimodifikasi. Proses hasil secara idempoten, dengan kunci berupa `id` chat, untuk menangani kemunculan ulang tersebut.

Beberapa batasan berlaku untuk kueri di seluruh organisasi ini. Kursor bersifat opak dan terikat pada kunci pengurutan, sehingga `after_id` yang diterbitkan di bawah satu nilai `order_by` akan ditolak dengan error 400 di bawah nilai yang lain. Batas filter waktu juga harus cocok dengan kunci pengurutan: pasangkan batas `updated_at.*` dengan `order_by=updated_at`, dan batas `created_at.*` dengan `order_by=created_at` default. Paginasi mundur dengan `before_id` tidak didukung, dan filter `project_ids[]` tidak tersedia. Lihat [List chats](/docs/id/api/compliance/apps/chats/list) untuk referensi filter lengkap.

Untuk membatasi daftar ke pengguna tertentu (misalnya, legal hold pada kustodian yang disebutkan namanya), kirimkan 1–10 nilai `user_ids[]`. Dapatkan ID-nya dari [List organization users](/docs/id/manage-claude/compliance-org-data#list-organization-users). Kueri yang difilter berdasarkan pengguna selalu diurutkan berdasarkan `created_at` (mengirimkan `order_by=updated_at` mengembalikan error 400) dan mendukung baik `after_id` maupun `before_id`. Pemfilteran berdasarkan `project_ids[]` hanya tersedia dalam bentuk yang difilter berdasarkan pengguna ini.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/apps/chats" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    --data-urlencode "user_ids[]=user_01XyDMpzjS89pFZXqSFUBDr6" \
    --data-urlencode "created_at.gte=2025-06-01T00:00:00Z" \
    --data-urlencode "limit=100"
  ```
</CodeGroup>

Respons daftar hanya membawa metadata chat. Untuk menarik konten chat yang sebenarnya, file terlampir, dan artifact sebaris (dokumen terstruktur yang dihasilkan Claude di dalam chat), lanjutkan dengan endpoint pesan untuk setiap ID chat:

<CodeGroup>
  ```bash cURL
  chat_id="claude_chat_01H5CWunD7RpVJ5bHa8RCkja"

  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/compliance/apps/chats/$chat_id/messages" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

Endpoint pesan mengembalikan metadata chat ditambah array `chat_messages` yang diurutkan berdasarkan `created_at`. Ketika `limit` dihilangkan, seluruh kumpulan pesan dikembalikan dalam satu respons; kirimkan `limit`, `after_id`, atau `before_id` untuk menelusuri chat yang sangat panjang per halaman. Endpoint ini juga menerima batas rentang `created_at.*` dan `updated_at.*` (`gt`, `gte`, `lt`, `lte`) serta parameter `order` (`asc` atau `desc`). Lihat [Get chat messages](/docs/id/api/compliance/apps/chats/messages/list) untuk daftar parameter lengkap. Untuk pesan pengguna, `created_at` adalah waktu pesan dikirim; untuk pesan asisten, itu adalah waktu Claude selesai menghasilkan pesan. Setiap pesan membawa konten teksnya dan, jika ada, file yang diunggah (biasanya pada pesan pengguna), file yang dihasilkan alat, dan artifact apa pun yang dihasilkan atau diperbarui oleh asisten (biasanya pada pesan asisten):

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

`files`, `generated_files`, dan `artifacts` masing-masing dapat bernilai `null` pada pesan tertentu. `files` adalah unggahan biner (PDF, gambar, spreadsheet) yang dilampirkan pengguna ke pesan. `generated_files` adalah file biner yang dibuat asisten selama percakapan melalui penggunaan alat (misalnya, PDF, spreadsheet, atau dek slide). `artifacts` adalah dokumen berversi (misalnya, kode atau markdown) yang dihasilkan atau diperbarui asisten dalam responsnya; sebuah artifact dapat direvisi di beberapa giliran asisten dalam chat yang sama, dan setiap revisi muncul sebagai `version_id` baru di bawah `id` artifact yang sama. Kirimkan `id` setiap entri (atau `version_id` untuk artifact) ke endpoint konten yang sesuai di [Mengambil file dan artifact](#retrieve-files-and-artifacts) untuk mengunduhnya.

## Mengambil file dan artifact

File dan artifact diunduh berdasarkan ID, tidak dicantumkan secara independen. ID berasal dari endpoint pesan chat di [Mengambil chat dan pesan](#retrieve-chats-and-messages) (array `files`, `generated_files`, dan `artifacts` pada setiap pesan) atau, untuk unggahan tingkat proyek, dari [endpoint lampiran proyek](#retrieve-projects-and-attachments).

Pilih endpoint yang cocok dengan tipe ID Anda dan data yang Anda butuhkan. Endpoint konten file yang sama melayani baik file chat maupun file proyek.

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

<CodeGroup>
  ```bash cURL
  file_id="claude_file_01UaT9wBcDfGhJkLmNpQrSv7"

  curl --fail-with-body -sS -OJ \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    "https://api.anthropic.com/v1/compliance/apps/chats/files/$file_id/content"
  ```
</CodeGroup>

Flag `-OJ` memberi tahu curl untuk menyimpan respons dengan nama file dari `Content-Disposition`, yaitu nama file asli yang diunggah pengguna.

Endpoint konten artifact mengembalikan isi teks dari satu versi artifact. Kirimkan `version_id` dari salah satu entri dalam array `artifacts` pesan asisten, bukan `id` stabil milik artifact. Setiap versi baru dari sebuah artifact memiliki `version_id` sendiri, dan Compliance API menyajikan byte persis dari versi tersebut.

## Mengambil proyek dan lampiran

Proyek menggabungkan chat terkait bersama dengan instruksi kustom, konten basis pengetahuan, dan file terlampir atau dokumen teks. Compliance API mengekspos metadata proyek, detail proyek, dan daftar lampiran yang dimiliki sebuah proyek.

* [List projects](/docs/id/api/compliance/apps/projects/list)
* [Get project details](/docs/id/api/compliance/apps/projects/retrieve)
* [List project attachments](/docs/id/api/compliance/apps/projects/attachments/list)
* [Get project document content](/docs/id/api/compliance/apps/projects/documents/retrieve)

Hasil proyek diurutkan berdasarkan tanggal pembuatan secara menaik. Hasil lampiran diurutkan berdasarkan `created_at` secara menaik, dengan seri dipecahkan oleh `id`. Respons daftar proyek dan daftar lampiran melakukan paginasi dengan token halaman `next_page` yang opak, bukan kursor `first_id`/`last_id` yang digunakan oleh chat dan Activity Feed. Kirimkan kembali token tersebut sebagai parameter kueri `page` pada permintaan berikutnya.

### File proyek versus dokumen proyek

Lampiran proyek adalah salah satu dari dua bentuk berbeda, yang diidentifikasi oleh diskriminator `type` pada setiap entri:

Entri dengan `type` bernilai `project_file` adalah unggahan biner (PDF, gambar, spreadsheet) yang ID-nya dimulai dengan `claude_file_`; unduh dengan [Download file content](/docs/id/api/compliance/apps/chats/files/download). Entri dengan `type` bernilai `project_doc` adalah dokumen teks biasa (selalu `text/plain`) yang ID-nya dimulai dengan `claude_proj_doc_`; ambil dengan [Get project document content](/docs/id/api/compliance/apps/projects/documents/retrieve).

Konsumen yang menelusuri daftar lampiran harus melakukan percabangan berdasarkan `type` dan memanggil endpoint konten yang sesuai untuk setiap entri. Permintaan berikut mencantumkan satu halaman lampiran; lakukan paginasi dengan mengirimkan kembali `next_page` sebagai parameter `page` hingga `has_more` bernilai `false`.

<CodeGroup>
  ```bash cURL
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

## Menghapus konten

<Warning>
  Setiap penghapusan yang berhasil bersifat permanen dan langsung. Tidak ada jendela pemulihan.
</Warning>

Compliance API mengekspos endpoint hard-delete untuk chat, file, dokumen proyek, dan seluruh proyek. Chat yang telah di-hard-delete tidak dapat dipulihkan, dan setelahnya berhenti muncul dalam respons daftar (sedangkan chat yang di-soft-delete dari claude.ai masih muncul dengan `deleted_at` terisi).

* [Delete chat](/docs/id/api/compliance/apps/chats/delete): juga menghapus pesan-pesan chat dan file apa pun yang dilampirkan pada pesan-pesan tersebut.
* [Delete file](/docs/id/api/compliance/apps/chats/files/delete): menangani baik file chat maupun file proyek.
* [Delete project document](/docs/id/api/compliance/apps/projects/documents/delete): menghapus satu dokumen proyek berdasarkan ID.
* [Delete project](/docs/id/api/compliance/apps/projects/delete): lihat [Lepaskan chat sebelum menghapus proyek](#detach-chats-before-deleting-a-project).

Keempat endpoint memerlukan scope `delete:compliance_user_data`, yang diberikan secara terpisah dari scope baca saat Compliance Access Key dibuat.

Permintaan berikut menghapus satu chat. Pola yang sama berlaku untuk endpoint penghapusan lainnya; hanya URL-nya yang berubah.

<CodeGroup>
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
</CodeGroup>

```json Response
{
  "id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja",
  "type": "claude_chat_deleted"
}
```

Setiap penghapusan yang berhasil mengembalikan amplop konfirmasi kecil dengan `id` dan diskriminator `type`. Endpoint chat mengembalikan `claude_chat_deleted`; periksa field `type` sebelum menganggap penghapusan terkonfirmasi. Lihat skema respons pada halaman [referensi API](/docs/id/api/compliance/apps) setiap endpoint penghapusan untuk nilai `type` persis yang dikembalikan endpoint lainnya.

### Lepaskan chat sebelum menghapus proyek

Proyek tidak dapat dihapus selama masih ada chat yang terlampir padanya. API mengembalikan 409 dengan body berikut:

```json
{
  "error": {
    "type": "conflict_error",
    "message": "The \"claude_proj_01KGp4eZNug9ri4kE35RSppq\" project cannot be deleted as it has chats attached to it. Delete or detach all chats, and try deleting the project again."
  }
}
```

Untuk mengatasinya, cantumkan chat milik proyek dengan `GET /v1/compliance/apps/chats?user_ids[]={user_id}&project_ids[]={project_id}` (filter `project_ids[]` memerlukan setidaknya satu nilai `user_ids[]`; enumerasi ID melalui [List organization users](/docs/id/manage-claude/compliance-org-data#list-organization-users)), hapus masing-masing dengan `DELETE /v1/compliance/apps/chats/{claude_chat_id}` (atau pindahkan keluar dari proyek melalui claude.ai), lalu coba lagi penghapusan proyek.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi API" href="/docs/id/api/compliance/apps">
    Skema permintaan dan respons lengkap untuk setiap endpoint chat, file, proyek, dan artifact.
  </Card>

  <Card title="Mencantumkan organisasi, pengguna, peran, grup, dan pengaturan" href="/docs/id/manage-claude/compliance-org-data">
    Enumerasi orang dan tim yang terkait dengan chat dan proyek pada halaman ini.
  </Card>
</CardGroup>
