---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-content-data
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 089810e2f3e66d5ca7f5bea7bf48f90c8435f593960a79f83abc34771bb11171
---

---
title: Mengambil dan menghapus chat, file, dan proyek
url: https://platform.claude.com/docs/id/manage-claude/compliance-content-data
description: Akses konten chat, lampiran file, dan proyek untuk organisasi claude.ai melalui Compliance API.
---

<Note>
  Endpoint di halaman ini hanya tersedia untuk organisasi Claude Enterprise. Endpoint ini mengambil dan menghapus chat, file, dan proyek claude.ai; transkrip sesi di aplikasi seperti Cowork dan Claude Code dibahas di [Mengambil transkrip sesi](https://platform.claude.com/docs/id/manage-claude/compliance-sessions). Lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_user_data` pada Compliance Access Key. Endpoint penghapusan juga memerlukan `delete:compliance_user_data`.

  **Prasyarat:** Tidak ada untuk mendaftar chat di seluruh organisasi. Untuk memfilter daftar chat ke pengguna tertentu, Anda memerlukan ID pengguna dari [Mendaftar pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users). Endpoint lain di halaman ini menerima ID sumber daya secara langsung.
</Check>

Endpoint di halaman ini mengekspos konten chat, unggahan file, proyek, dan lampiran proyek Claude Enterprise kepada peninjau kepatuhan. Endpoint ini mendukung ekspor eDiscovery (electronic discovery atau penemuan elektronik), penegakan "data loss prevention" (pencegahan kehilangan data), atau DLP, dan respons penghapusan akun. Konten chat, file, dan proyek disimpan selama kebijakan retensi organisasi Anda mengizinkan. Ketika pengguna menghapus chat di claude.ai, konten pesannya, file terlampir, file yang dihasilkan alat, dan artifact dihapus bersamanya. Compliance API tetap mendaftar chat tersebut, dengan `deleted_at` terisi dan `name` kosong, serta mengembalikan pesan-pesannya tanpa kontennya. Chat yang telah dihapus permanen (hard-deleted) (melalui Compliance API itu sendiri, atau setelah jendela retensi organisasi berakhir) tidak dapat diambil.

Kedua scope hanya diberikan pada Compliance Access Key (`sk-ant-api01-...`) yang dibuat di claude.ai; lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access) untuk menyediakannya. Scope `read:compliance_user_data` mencakup pengambilan; `delete:compliance_user_data` hanya diperlukan untuk endpoint penghapusan. Endpoint chat, file, proyek, dan lampiran tidak tersedia untuk kunci Admin API (`sk-ant-admin01-...`); panggilan yang diautentikasi dengan kunci Admin API mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden).

Endpoint di halaman ini melakukan paginasi dengan dua cara; lihat [Memaginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results) untuk referensi lengkapnya. Setiap bagian mencatat skema mana yang berlaku.

## Mengambil chat dan pesan

Gunakan [Mendaftar chat](https://platform.claude.com/docs/id/api/compliance/apps/chats/list) untuk menelusuri halaman metadata chat, lalu [Mendapatkan pesan chat](https://platform.claude.com/docs/id/api/compliance/apps/chats/messages/list) untuk mengambil konten pesan lengkap dari satu chat.

Endpoint daftar chat secara default menggunakan cakupan seluruh organisasi: hilangkan `user_ids[]` untuk menyertakan setiap chat di bawah organisasi induk Anda. Tambahkan `order_by=updated_at` untuk mengurutkan berdasarkan waktu pembaruan terakhir. Kombinasi ini adalah cara yang direkomendasikan untuk mengekspor chat dan menjaga ekspor tetap mutakhir, karena satu loop berpaginasi menangkap chat baru, chat yang dimodifikasi, dan chat yang dihapus di claude.ai untuk setiap pengguna tanpa perlu mengenumerasi pengguna terlebih dahulu. Permintaan berikut mendaftar chat yang diperbarui sejak tanggal tertentu.

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

Hasil diurutkan menaik berdasarkan field `order_by`, yang terlama lebih dulu, dengan nilai yang sama dipisahkan berdasarkan `id`. Paginasi menggunakan field kursor standar `first_id`/`last_id`/`has_more` yang dijelaskan di [Memaginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results). Untuk bergerak maju menuju chat yang lebih baru, teruskan `last_id` dari respons sebagai `after_id` pada permintaan berikutnya.

Penelusuran maju itu juga merupakan cara Anda menjaga ekspor tetap mutakhir di antara beberapa kali eksekusi: simpan `last_id` dari halaman terakhir dan lanjutkan darinya sebagai `after_id` pada eksekusi berikutnya. Karena daftar diurutkan berdasarkan `updated_at`, chat yang berubah setelah kursor tersimpan Anda akan muncul kembali di depannya, sehingga setiap eksekusi inkremental mengembalikan chat yang benar-benar baru maupun chat lama yang sejak itu telah dimodifikasi atau dihapus di claude.ai. Proses hasil secara idempoten, dengan kunci berupa `id` chat, untuk menangani kemunculan ulang tersebut. Chat yang kembali dengan `deleted_at` terisi tidak memiliki konten tersisa untuk diambil, jadi perlakukan sebagai dihapus, bukan diperbarui.

Beberapa batasan berlaku untuk kueri seluruh organisasi ini. Kursor bersifat opaque dan terikat pada kunci pengurutan, sehingga `after_id` yang diterbitkan di bawah satu nilai `order_by` ditolak dengan error 400 di bawah nilai lainnya. Batas filter waktu juga harus cocok dengan kunci pengurutan: pasangkan batas `updated_at.*` dengan `order_by=updated_at`, dan batas `created_at.*` dengan `order_by=created_at` default. Paginasi mundur dengan `before_id` tidak didukung, dan filter `project_ids[]` tidak tersedia. Lihat [Mendaftar chat](https://platform.claude.com/docs/id/api/compliance/apps/chats/list) untuk referensi filter lengkap.

Untuk membatasi daftar ke pengguna tertentu (misalnya, legal hold pada kustodian yang disebutkan namanya), teruskan 1–10 nilai `user_ids[]`. Dapatkan ID tersebut dari [Mendaftar pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users). Kueri yang difilter berdasarkan pengguna selalu diurutkan berdasarkan `created_at` (meneruskan `order_by=updated_at` mengembalikan error 400) dan mendukung `after_id` maupun `before_id`. Pemfilteran berdasarkan `project_ids[]` hanya tersedia dalam bentuk yang difilter berdasarkan pengguna ini. Menggabungkan `user_ids[]` dengan batas `updated_at.*` apa pun sudah deprecated dan akan ditolak dengan error 400 setelah 2026-09-22; untuk menjaga kumpulan kustodian tetap mutakhir berdasarkan waktu pembaruan, jalankan penelusuran seluruh organisasi `order_by=updated_at` tanpa `user_ids[]` dan pilih chat milik kustodian dari hasilnya, serta pertahankan daftar yang difilter berdasarkan pengguna untuk ekspor yang diurutkan berdasarkan `created_at`.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/chats" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "user_ids[]=user_01XyDMpzjS89pFZXqSFUBDr6" \
  --data-urlencode "created_at.gte=2025-06-01T00:00:00Z" \
  --data-urlencode "limit=100"
```

Respons daftar hanya membawa metadata chat. Untuk mengambil konten chat sebenarnya, file terlampir, dan artifact inline (dokumen terstruktur yang dihasilkan Claude di dalam chat), lanjutkan dengan endpoint pesan untuk setiap ID chat:

```bash cURL
chat_id="claude_chat_01H5CWunD7RpVJ5bHa8RCkja"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/chats/$chat_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

Endpoint pesan mengembalikan metadata chat ditambah array `chat_messages` yang diurutkan berdasarkan `created_at`. Ketika `limit` dihilangkan, seluruh kumpulan pesan dikembalikan dalam satu respons; teruskan `limit`, `after_id`, atau `before_id` untuk menelusuri halaman chat yang sangat panjang. Endpoint ini juga menerima batas rentang `created_at.*` dan `updated_at.*` (`gt`, `gte`, `lt`, `lte`) serta parameter `order` (`asc` atau `desc`). Lihat [Mendapatkan pesan chat](https://platform.claude.com/docs/id/api/compliance/apps/chats/messages/list) untuk daftar parameter lengkap. Untuk pesan pengguna, `created_at` adalah waktu pesan dikirim; untuk pesan asisten, itu adalah waktu Claude selesai menghasilkan pesan. Setiap pesan membawa konten teksnya dan, jika ada, file yang diunggah (biasanya pada pesan pengguna), file yang dihasilkan alat, dan artifact yang dihasilkan atau diperbarui asisten (biasanya pada pesan asisten):

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
          "mime_type": "application/pdf",
          "size_bytes": 482133,
          "md5": "56367e4d2705cc9c025ad07424e944f0",
          "created_at": "2026-04-10T08:09:10Z"
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
          "mime_type": "text/csv",
          "size_bytes": 2048,
          "md5": "89968669461d95416549937168269d6b"
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

`files`, `generated_files`, dan `artifacts` masing-masing dapat bernilai `null` pada pesan tertentu. `files` adalah file dan lampiran teks (misalnya, PDF, gambar, spreadsheet, dokumen, dan teks yang ditempel) yang dilampirkan pengguna ke pesan, sebagaimana claude.ai menyimpannya. `generated_files` adalah file biner yang dibuat asisten selama percakapan melalui "tool use" (penggunaan alat) (misalnya, PDF, spreadsheet, atau slide deck). `artifacts` adalah dokumen berversi (misalnya, kode atau markdown) yang dihasilkan atau diperbarui asisten dalam responsnya; sebuah artifact dapat direvisi di beberapa giliran asisten dalam chat yang sama, dan setiap revisi muncul sebagai `version_id` baru di bawah `id` artifact yang sama. Teruskan `id` setiap entri (atau `version_id` untuk artifact) ke endpoint konten yang sesuai di [Mengambil file dan artifact](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-files-and-artifacts) untuk mengunduhnya.

## Mengambil file dan artifact

File dan artifact diunduh berdasarkan ID, bukan didaftar secara independen. ID tersebut berasal dari endpoint pesan chat di [Mengambil chat dan pesan](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-chats-and-messages) (array `files`, `generated_files`, dan `artifacts` pada setiap pesan) atau, untuk unggahan tingkat proyek, dari [endpoint lampiran proyek](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-projects-and-attachments).

Pilih endpoint yang cocok dengan jenis ID Anda dan data yang Anda butuhkan. Endpoint konten file yang sama melayani file chat maupun file proyek.

| Anda memiliki                  | Anda menginginkan                        | Gunakan endpoint ini                                                                                                                |
| ------------------------------ | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| ID `claude_file_*`             | Konten file                              | [Mengunduh konten file](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/download)                               |
| ID `claude_file_*`             | Hanya metadata file                      | [Mendapatkan metadata file](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/retrieve)                           |
| ID `claude_gen_file_*`         | Konten biner file yang dihasilkan alat   | [Mengunduh file yang dihasilkan Claude](https://platform.claude.com/docs/id/api/compliance/apps/chats/generated_files/download)     |
| ID `claude_gen_file_*`         | Hanya metadata file yang dihasilkan alat | [Mendapatkan metadata file yang dihasilkan](https://platform.claude.com/docs/id/api/compliance/apps/chats/generated_files/retrieve) |
| ID `claude_artifact_version_*` | Teks satu versi artifact                 | [Mengunduh konten artifact](https://platform.claude.com/docs/id/api/compliance/apps/artifacts/download)                             |
| ID `claude_artifact_version_*` | Hanya metadata versi artifact            | [Mendapatkan metadata artifact](https://platform.claude.com/docs/id/api/compliance/apps/artifacts/retrieve)                         |
| ID `claude_proj_doc_*`         | Konten teks biasa dokumen proyek         | [Mendapatkan konten dokumen proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/retrieve)            |
| ID `claude_proj_doc_*`         | Hanya metadata dokumen proyek            | [Mendapatkan metadata dokumen proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/metadata)          |

Endpoint konten file melakukan streaming konten yang disimpan claude.ai untuk file tersebut sebagai respons biner chunked. Konten itu tidak selalu identik dengan file yang diunggah pengguna. Gambar dapat disajikan sebagai salinan yang telah diproses, bukan byte yang diunggah. Beberapa dokumen yang dilampirkan ke chat (misalnya, file Word, file PowerPoint, dan beberapa PDF) disimpan sebagai teks yang diekstrak claude.ai darinya. Untuk dokumen-dokumen ini, endpoint mengembalikan teks yang diekstrak dengan nama file asli, dan dokumen asli tidak tersedia melalui Compliance API. Field `size_bytes` dan `md5` mendeskripsikan konten yang disimpan, bukan file yang diunggah. Nama file dan `mime_type` masih dapat menyebutkan format dokumen yang diunggah. Identifikasi format file dari byte yang dikembalikan, bukan dari nama atau tipe yang dideklarasikan.

Respons membawa header berikut:

* `Content-Disposition: attachment; filename*=utf-8''<percent-encoded filename>` membawa nama file unggahan asli dalam bentuk extended RFC 5987. Bentuk extended digunakan untuk setiap nama file, bukan hanya yang non-ASCII.
* `Content-Type` membawa tipe MIME yang dicatat untuk konten yang disimpan, yang untuk dokumen yang disimpan sebagai teks terekstrak masih dapat menyebutkan format dokumen asli.
* `Content-MD5` membawa digest MD5 dari byte yang disajikan, dienkode base64 sebagaimana ditentukan dalam RFC 1864.
* `Transfer-Encoding: chunked` selalu disetel.

```bash cURL
file_id="claude_file_01UaT9wBcDfGhJkLmNpQrSv7"

curl --fail-with-body -sS -OJ \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  "https://api.anthropic.com/v1/compliance/apps/chats/files/$file_id/content"
```

Flag `-OJ` memberi tahu curl untuk menyimpan respons dengan nama file dari `Content-Disposition`, yaitu nama file asli yang diunggah pengguna.

Endpoint konten artifact mengembalikan isi teks dari satu versi artifact. Teruskan `version_id` dari salah satu entri dalam array `artifacts` pesan asisten, bukan `id` stabil artifact. Setiap versi baru artifact memiliki `version_id` sendiri, dan Compliance API menyajikan byte persis dari versi tersebut.

## Mengambil proyek dan lampiran

Proyek menggabungkan chat terkait bersama dengan instruksi kustom, konten basis pengetahuan, dan file atau dokumen teks terlampir. Compliance API mengekspos metadata proyek, detail proyek, dan daftar lampiran yang dimiliki suatu proyek.

* [Mendaftar proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/list)
* [Mendapatkan detail proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/retrieve)
* [Mendaftar lampiran proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/attachments/list)
* [Mendapatkan konten dokumen proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/retrieve)

Hasil proyek diurutkan berdasarkan tanggal pembuatan secara menaik. Hasil lampiran diurutkan berdasarkan `created_at` secara menaik, dengan nilai yang sama dipisahkan berdasarkan `id`. Respons daftar proyek dan daftar lampiran melakukan paginasi dengan token halaman `next_page` yang opaque, bukan kursor `first_id`/`last_id` yang digunakan oleh chat dan Activity Feed. Teruskan token tersebut kembali sebagai parameter kueri `page` pada permintaan berikutnya.

### File proyek versus dokumen proyek

Lampiran proyek memiliki salah satu dari dua bentuk berbeda, yang diidentifikasi oleh diskriminator `type` pada setiap entri:

Entri dengan `type` bernilai `project_file` adalah unggahan file (PDF, gambar, spreadsheet) yang ID-nya dimulai dengan `claude_file_`; unduh dengan [Mengunduh konten file](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/download). Entri dengan `type` bernilai `project_doc` adalah dokumen teks biasa (selalu `text/plain`) yang ID-nya dimulai dengan `claude_proj_doc_`, termasuk dokumen seperti file Word yang dikonversi claude.ai menjadi teks ketika ditambahkan ke proyek; ambil dengan [Mendapatkan konten dokumen proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/retrieve).

Konsumen yang menelusuri daftar lampiran harus bercabang berdasarkan `type` dan memanggil endpoint konten yang sesuai untuk setiap entri. Permintaan berikut mendaftar satu halaman lampiran; lakukan paginasi dengan meneruskan `next_page` kembali sebagai parameter `page` hingga `has_more` bernilai `false`.

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
      "size_bytes": 482133,
      "md5": "56367e4d2705cc9c025ad07424e944f0",
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
  Setiap penghapusan yang berhasil bersifat permanen dan langsung berlaku. Tidak ada jendela pemulihan.
</Warning>

Compliance API mengekspos endpoint hard-delete untuk chat, file, dokumen proyek, dan seluruh proyek. Chat yang dihapus permanen tidak dapat dipulihkan, dan setelahnya berhenti muncul dalam respons daftar.

* [Menghapus chat](https://platform.claude.com/docs/id/api/compliance/apps/chats/delete): juga menghapus pesan-pesan chat dan file apa pun yang dilampirkan ke pesan tersebut.
* [Menghapus file](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/delete): menangani file chat maupun file proyek.
* [Menghapus dokumen proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/delete): menghapus satu dokumen proyek berdasarkan ID.
* [Menghapus proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/delete): lihat [Melepaskan chat sebelum menghapus proyek](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#detach-chats-before-deleting-a-project).

Keempat endpoint memerlukan scope `delete:compliance_user_data`, yang diberikan secara terpisah dari scope baca ketika Compliance Access Key dibuat.

Permintaan berikut menghapus satu chat. Pola yang sama berlaku untuk endpoint penghapusan lainnya; hanya URL-nya yang berubah.

```bash cURL
# PERINGATAN: Operasi ini menghapus chat secara PERMANEN, beserta semua pesannya,
# dan semua file terlampir. Penghapusan berlangsung seketika dan tidak dapat dibatalkan. Operasi ini
# memerlukan scope `delete:compliance_user_data`, yang diberikan secara terpisah
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

Setiap penghapusan yang berhasil mengembalikan amplop konfirmasi kecil dengan `id` dan diskriminator `type`. Endpoint chat mengembalikan `claude_chat_deleted`; periksa field `type` sebelum menganggap penghapusan telah terkonfirmasi. Lihat skema respons di halaman [referensi API](https://platform.claude.com/docs/id/api/compliance/apps) setiap endpoint penghapusan untuk nilai `type` persis yang dikembalikan endpoint lainnya.

### Melepaskan chat sebelum menghapus proyek

Proyek tidak dapat dihapus selama masih ada chat yang terlampir padanya. API mengembalikan 409 dengan isi berikut:

```json
{
  "error": {
    "type": "conflict_error",
    "message": "The \"claude_proj_01KGp4eZNug9ri4kE35RSppq\" project cannot be deleted as it has chats attached to it. Delete or detach all chats, and try deleting the project again."
  }
}
```

Untuk menyelesaikannya, daftar chat proyek dengan `GET /v1/compliance/apps/chats?user_ids[]={user_id}&project_ids[]={project_id}` (filter `project_ids[]` memerlukan setidaknya satu nilai `user_ids[]`; enumerasi ID melalui [Mendaftar pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users)), hapus masing-masing dengan `DELETE /v1/compliance/apps/chats/{claude_chat_id}` (atau pindahkan keluar dari proyek melalui claude.ai), lalu coba lagi penghapusan proyek.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi API" href="https://platform.claude.com/docs/id/api/compliance/apps">
    Skema permintaan dan respons lengkap untuk setiap endpoint chat, file, proyek, dan artifact.
  </Card>

  <Card title="Mengambil transkrip sesi" href="https://platform.claude.com/docs/id/manage-claude/compliance-sessions">
    Daftar sesi yang dijalankan pengguna Anda di aplikasi dan agen Claude, seperti Cowork dan Claude Code, dan ambil transkripnya.
  </Card>

  <Card title="Mendaftar organisasi, pengguna, peran, grup, dan pengaturan" href="https://platform.claude.com/docs/id/manage-claude/compliance-org-data">
    Enumerasi orang dan tim yang terkait dengan chat dan proyek di halaman ini.
  </Card>
</CardGroup>
