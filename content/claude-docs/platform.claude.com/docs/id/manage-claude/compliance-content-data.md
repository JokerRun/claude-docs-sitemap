---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-content-data
fetched_at: 2026-09-24T02:21:35.920672Z
sha256: db78f42e2d644c14375b40467600d2d37b9fae0028dd4fb656fb2e8be0108dd7
---

---
title: Mengambil dan menghapus chat, file, dan proyek
url: https://platform.claude.com/docs/id/manage-claude/compliance-content-data
description: Akses konten chat, lampiran file, dan proyek untuk organisasi claude.ai melalui Compliance API.
---

<Note>
  Endpoint di halaman ini hanya tersedia untuk organisasi Claude Enterprise. Endpoint ini mengambil dan menghapus chat, file, dan proyek claude.ai. Transkrip sesi di aplikasi seperti Cowork dan Claude Code dibahas di [Mengambil transkrip sesi](https://platform.claude.com/docs/id/manage-claude/compliance-sessions). Lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_user_data` pada Compliance Access Key. Endpoint penghapusan juga memerlukan `delete:compliance_user_data`.

  **Prasyarat:** Tidak ada untuk mencantumkan chat di seluruh organisasi. Untuk memfilter daftar chat ke pengguna tertentu, Anda memerlukan ID pengguna dari [Mencantumkan pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users). Endpoint lain di halaman ini menerima ID sumber daya secara langsung.
</Check>

Endpoint di halaman ini menyediakan konten chat Claude Enterprise, unggahan file, proyek, dan lampiran proyek bagi peninjau kepatuhan. Endpoint ini mendukung ekspor eDiscovery (electronic discovery), penegakan "data loss prevention" (pencegahan kehilangan data), atau DLP, serta penanganan permintaan penghapusan akun. Konten chat, file, dan proyek disimpan selama diizinkan oleh kebijakan retensi organisasi Anda. Ketika pengguna menghapus chat di claude.ai, konten pesannya, file terlampir, file yang dihasilkan alat, dan artifact ikut terhapus. Compliance API tetap mencantumkan chat tersebut, dengan `deleted_at` terisi dan `name` kosong, serta mengembalikan pesan-pesannya tanpa konten. Chat yang telah dihapus secara permanen ("hard-delete") tidak dapat diambil, baik penghapusan itu dilakukan melalui Compliance API sendiri maupun setelah jendela retensi organisasi berakhir.

Kedua scope hanya diberikan pada Compliance Access Key (`sk-ant-api01-...`) yang dibuat di claude.ai. Lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access) untuk membuatnya. Scope `read:compliance_user_data` mencakup pengambilan data, sedangkan `delete:compliance_user_data` hanya diperlukan untuk endpoint penghapusan. Endpoint chat, file, proyek, dan lampiran tidak tersedia untuk kunci Admin API (`sk-ant-admin01-...`). Panggilan yang diautentikasi dengan kunci Admin API akan mengembalikan [403 Forbidden](https://platform.claude.com/docs/id/manage-claude/compliance-errors#403-forbidden).

Endpoint di halaman ini menggunakan dua cara "pagination" (paginasi). Lihat [Paginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results) untuk referensi lengkapnya. Setiap bagian menyebutkan skema mana yang berlaku.

## Mengambil chat dan pesan

Gunakan [Mencantumkan chat](https://platform.claude.com/docs/id/api/compliance/apps/chats/list) untuk menelusuri metadata chat halaman demi halaman, lalu [Mendapatkan pesan chat](https://platform.claude.com/docs/id/api/compliance/apps/chats/messages/list) untuk mengambil konten pesan lengkap dari satu chat.

Endpoint daftar chat secara default menggunakan cakupan seluruh organisasi: hilangkan `user_ids[]` untuk menyertakan setiap chat di bawah organisasi induk Anda. Tambahkan `order_by=updated_at` untuk mengurutkan berdasarkan waktu pembaruan terakhir. Kombinasi ini adalah cara yang direkomendasikan untuk mengekspor chat dan menjaga ekspor tetap mutakhir, karena satu loop berpaginasi akan menangkap chat baru, chat dengan pesan baru, dan chat yang dihapus di claude.ai untuk setiap pengguna tanpa perlu mengenumerasi pengguna terlebih dahulu. Permintaan berikut mencantumkan chat yang diperbarui sejak tanggal tertentu.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/chats" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01" \
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
      "model": "claude-opus-5-5",
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

Hasil diurutkan secara menaik berdasarkan field `order_by`, dari yang terlama, dengan nilai yang sama diurutkan berdasarkan `id`. Paginasi menggunakan field kursor standar `first_id`/`last_id`/`has_more` yang dijelaskan di [Memaginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results). Untuk bergerak maju ke chat yang lebih baru, kirimkan kembali `last_id` dari respons sebagai `after_id` pada permintaan berikutnya.

Penelusuran maju tersebut juga merupakan cara Anda menjaga ekspor tetap mutakhir di setiap eksekusi: simpan `last_id` dari halaman terakhir dan lanjutkan darinya sebagai `after_id` pada eksekusi berikutnya. Karena daftar diurutkan berdasarkan `updated_at`, sebuah chat akan muncul kembali setelah kursor yang Anda simpan ketika chat tersebut menerima pesan baru, dipindahkan ke dalam atau keluar dari proyek, atau dihapus di claude.ai. Oleh karena itu, setiap eksekusi inkremental mengembalikan chat yang benar-benar baru sekaligus chat lama yang telah berubah dengan salah satu cara tersebut. Perubahan lain, seperti penggantian nama, tidak dijamin membuat chat muncul kembali. Proses hasil secara idempoten, dengan kunci berupa `id` chat, untuk menangani kemunculan ulang tersebut. Chat yang muncul kembali dengan `deleted_at` terisi tidak lagi memiliki konten untuk diambil, jadi perlakukan sebagai terhapus, bukan diperbarui.

Beberapa batasan berlaku untuk kueri seluruh organisasi ini. Kursor bersifat opaque dan terikat pada kunci pengurutan, sehingga `after_id` yang diterbitkan dengan satu nilai `order_by` akan ditolak dengan error 400 pada nilai lainnya. Batas filter waktu juga harus sesuai dengan kunci pengurutan: pasangkan batas `updated_at.*` dengan `order_by=updated_at`, dan batas `created_at.*` dengan `order_by=created_at` default. Paginasi mundur dengan `before_id` tidak didukung, dan filter `project_ids[]` tidak tersedia. Lihat [Mencantumkan chat](https://platform.claude.com/docs/id/api/compliance/apps/chats/list) untuk referensi filter lengkap.

Untuk membatasi daftar ke pengguna tertentu (misalnya, "legal hold" (penahanan hukum) pada kustodian yang disebutkan namanya), kirimkan 1–10 nilai `user_ids[]`. Dapatkan ID tersebut dari [Mencantumkan pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users). Kueri yang difilter berdasarkan pengguna selalu diurutkan berdasarkan `created_at` (mengirimkan `order_by=updated_at` akan mengembalikan error 400) dan mendukung `after_id` maupun `before_id`. Pemfilteran berdasarkan `project_ids[]` hanya tersedia dalam bentuk yang difilter berdasarkan pengguna ini. Menggabungkan `user_ids[]` dengan batas `updated_at.*` apa pun sudah tidak digunakan lagi (deprecated) dan akan ditolak dengan error 400 setelah 2026-09-22; untuk menjaga kumpulan kustodian tetap mutakhir berdasarkan waktu pembaruan, jalankan penelusuran `order_by=updated_at` seluruh organisasi tanpa `user_ids[]` dan pilih chat milik kustodian dari hasilnya, serta gunakan daftar yang difilter berdasarkan pengguna untuk ekspor yang diurutkan berdasarkan `created_at`.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/chats" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --data-urlencode "user_ids[]=user_01XyDMpzjS89pFZXqSFUBDr6" \
  --data-urlencode "created_at.gte=2025-06-01T00:00:00Z" \
  --data-urlencode "limit=100"
```

Respons daftar hanya berisi metadata chat. Untuk mengambil konten chat yang sebenarnya, file yang dilampirkan, dan artifact inline (dokumen terstruktur yang dihasilkan Claude di dalam chat), lanjutkan dengan endpoint pesan untuk setiap ID chat:

```bash cURL
chat_id="claude_chat_01H5CWunD7RpVJ5bHa8RCkja"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/chats/$chat_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01"
```

Endpoint pesan mengembalikan metadata chat beserta array `chat_messages` yang diurutkan berdasarkan `created_at`. Jika `limit` dihilangkan, seluruh kumpulan pesan dikembalikan dalam satu respons; kirimkan `limit`, `after_id`, atau `before_id` untuk menelusuri chat yang sangat panjang halaman demi halaman. Endpoint ini juga menerima batas rentang `created_at.*` dan `updated_at.*` (`gt`, `gte`, `lt`, `lte`) serta parameter `order` (`asc` atau `desc`). Lihat [Mendapatkan pesan chat](https://platform.claude.com/docs/id/api/compliance/apps/chats/messages/list) untuk daftar parameter lengkap. Untuk pesan pengguna, `created_at` adalah waktu pesan dikirim; untuk pesan asisten, ini adalah waktu Claude selesai menghasilkan pesan. Setiap pesan berisi konten teksnya dan, jika ada, file yang diunggah (biasanya pada pesan pengguna), file yang dihasilkan alat, dan artifact yang dihasilkan atau diperbarui oleh asisten (biasanya pada pesan asisten):

```json Response
{
  "id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja",
  "name": "Product Requirements Discussion",
  "created_at": "2026-04-10T08:09:10Z",
  "updated_at": "2026-04-10T09:10:11Z",
  "deleted_at": null,
  "href": "https://claude.ai/chat/abcdef01-2345-6789-abcd-ef0123456789",
  "model": "claude-opus-5-5",
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

`files`, `generated_files`, dan `artifacts` masing-masing dapat bernilai `null` pada pesan tertentu. `files` adalah file dan lampiran teks (misalnya, PDF, gambar, spreadsheet, dokumen, dan teks yang ditempel) yang dilampirkan pengguna ke pesan, sebagaimana disimpan oleh claude.ai. `generated_files` adalah file biner yang dibuat asisten selama percakapan melalui "tool use" (penggunaan alat), misalnya PDF, spreadsheet, atau slide presentasi. `artifacts` adalah dokumen berversi (misalnya, kode atau markdown) yang dihasilkan atau diperbarui asisten dalam responsnya; sebuah artifact dapat direvisi di beberapa giliran asisten dalam chat yang sama, dan setiap revisi muncul sebagai `version_id` baru di bawah `id` artifact yang sama. Kirimkan `id` setiap entri (atau `version_id` untuk artifact) ke endpoint konten yang sesuai di [Mengambil file dan artifact](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-files-and-artifacts) untuk mengunduhnya.

## Mengambil file dan artifact

File dan artifact diunduh berdasarkan ID dan tidak dicantumkan secara terpisah. ID tersebut berasal dari endpoint pesan chat di [Mengambil chat dan pesan](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-chats-and-messages), yaitu array `files`, `generated_files`, dan `artifacts` pada setiap pesan. Untuk unggahan tingkat proyek, ID berasal dari [endpoint lampiran proyek](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#retrieve-projects-and-attachments).

Pilih endpoint yang sesuai dengan jenis ID Anda dan data yang Anda butuhkan. Endpoint konten file yang sama melayani file chat maupun file proyek.

| Yang Anda miliki               | Yang Anda inginkan                       | Gunakan endpoint ini                                                                                                                |
| ------------------------------ | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| ID `claude_file_*`             | Konten file                              | [Mengunduh konten file](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/download)                               |
| ID `claude_file_*`             | Hanya metadata file                      | [Mendapatkan metadata file](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/retrieve)                           |
| ID `claude_gen_file_*`         | Konten biner file yang dihasilkan alat   | [Mengunduh file yang dihasilkan Claude](https://platform.claude.com/docs/id/api/compliance/apps/chats/generated_files/download)     |
| ID `claude_gen_file_*`         | Hanya metadata file yang dihasilkan alat | [Mendapatkan metadata file yang dihasilkan](https://platform.claude.com/docs/id/api/compliance/apps/chats/generated_files/retrieve) |
| ID `claude_artifact_version_*` | Teks dari satu versi artifact            | [Mengunduh konten artifact](https://platform.claude.com/docs/id/api/compliance/apps/artifacts/download)                             |
| ID `claude_artifact_version_*` | Hanya metadata versi artifact            | [Mendapatkan metadata artifact](https://platform.claude.com/docs/id/api/compliance/apps/artifacts/retrieve)                         |
| ID `claude_proj_doc_*`         | Konten teks biasa dokumen proyek         | [Mendapatkan konten dokumen proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/retrieve)            |
| ID `claude_proj_doc_*`         | Hanya metadata dokumen proyek            | [Mendapatkan metadata dokumen proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/metadata)          |

Endpoint konten file melakukan streaming konten yang disimpan claude.ai untuk file tersebut sebagai respons biner chunked. Konten itu tidak selalu identik dengan file yang diunggah pengguna:

* Gambar dapat disajikan sebagai salinan yang telah diproses, bukan byte asli yang diunggah.
* Beberapa dokumen yang dilampirkan ke chat (misalnya, file Word, file PowerPoint, dan sebagian PDF) disimpan sebagai teks yang diekstrak claude.ai darinya. Untuk dokumen seperti ini, endpoint mengembalikan teks hasil ekstraksi dengan nama file asli, dan dokumen aslinya tidak tersedia melalui Compliance API.

Field `size_bytes` dan `md5` menggambarkan konten yang disimpan, bukan file yang diunggah. Nama file dan `mime_type` mungkin tetap menunjukkan format dokumen yang diunggah. Karena itu, tentukan format file dari byte yang dikembalikan, bukan dari nama atau tipe yang dideklarasikan.

Respons menyertakan header berikut:

* `Content-Disposition: attachment; filename*=utf-8''<percent-encoded filename>` berisi nama file unggahan asli dalam bentuk extended RFC 5987. Bentuk extended ini digunakan untuk setiap nama file, tidak hanya yang mengandung karakter non-ASCII.
* `Content-Type` berisi tipe MIME yang tercatat untuk konten yang disimpan. Untuk dokumen yang disimpan sebagai teks hasil ekstraksi, nilainya mungkin tetap menunjukkan format dokumen asli.
* `Content-MD5` berisi digest MD5 dari byte yang disajikan, dienkode base64 sesuai RFC 1864.
* `Transfer-Encoding: chunked` selalu disetel.

```bash cURL
file_id="claude_file_01UaT9wBcDfGhJkLmNpQrSv7"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/chats/files/$file_id/content" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --output "dashboard_mockup_v1.pdf"
```

Di curl, opsi `--remote-header-name` (`-J`) biasanya menyimpan unduhan dengan nama file dari `Content-Disposition`, tetapi opsi ini tidak membaca bentuk `filename*`. Karena itu, tentukan sendiri nama file yang disimpan dengan `--output`. Dalam skrip, ambil nama dari field `filename` file tersebut di respons pesan chat atau [Mendapatkan metadata file](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/retrieve), atau dekode `filename*`.

Apa pun caranya, nama tersebut adalah nama yang diberikan pengguna saat mengunggah, jadi anggap tidak tepercaya sebelum menggunakannya sebagai path output:

* Ambil hanya nama dasarnya.
* Izinkan hanya karakter yang aman untuk sistem file Anda.
* Tolak nama yang diawali dengan `-` atau `.`.

Berbeda dengan endpoint konten file, endpoint konten artifact mengembalikan objek JSON. Kirimkan `version_id` dari salah satu entri dalam array `artifacts` pada pesan asisten, bukan `id` artifact yang stabil. Setiap versi baru artifact memiliki `version_id` sendiri. Field `content` pada respons berisi teks dari versi tersebut secara persis, sedangkan field `title` dan `artifact_type` menggambarkan artifact-nya. [Mendapatkan metadata artifact](https://platform.claude.com/docs/id/api/compliance/apps/artifacts/retrieve) menghitung `size_bytes` dan `md5` dari encoding UTF-8 teks tersebut. Jadi, bandingkan keduanya dengan nilai `content`, bukan dengan seluruh body respons.

## Mengambil proyek dan lampiran

Proyek mengelompokkan chat yang saling terkait beserta instruksi kustom, konten basis pengetahuan, dan file atau dokumen teks terlampir. Compliance API menyediakan metadata proyek, detail proyek, dan daftar lampiran milik sebuah proyek.

* [Mencantumkan proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/list)
* [Mendapatkan detail proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/retrieve)
* [Mencantumkan lampiran proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/attachments/list)
* [Mendapatkan konten dokumen proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/retrieve)

Hasil proyek diurutkan secara menaik berdasarkan tanggal pembuatan. Hasil lampiran diurutkan secara menaik berdasarkan `created_at`, dan jika nilainya sama, urutan ditentukan oleh `id`. Respons daftar proyek dan daftar lampiran menggunakan token halaman `next_page` yang bersifat opaque untuk paginasi, bukan kursor `first_id`/`last_id` seperti pada chat dan Activity Feed. Kirimkan token tersebut sebagai parameter kueri `page` pada permintaan berikutnya.

### File proyek versus dokumen proyek

Lampiran proyek memiliki salah satu dari dua bentuk berbeda, yang dibedakan oleh diskriminator `type` pada setiap entri:

* Entri dengan `type` bernilai `project_file` adalah unggahan file (PDF, gambar, spreadsheet) dengan ID yang diawali `claude_file_`. Unduh dengan [Mengunduh konten file](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/download).
* Entri dengan `type` bernilai `project_doc` adalah dokumen teks biasa (selalu `text/plain`) dengan ID yang diawali `claude_proj_doc_`. Ini termasuk dokumen seperti file Word yang dikonversi claude.ai menjadi teks saat ditambahkan ke proyek. Ambil dengan [Mendapatkan konten dokumen proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/retrieve).

Kode yang menelusuri daftar lampiran harus bercabang berdasarkan `type` dan memanggil endpoint konten yang sesuai untuk setiap entri. Permintaan berikut mencantumkan satu halaman lampiran. Untuk paginasi, kirimkan `next_page` sebagai parameter `page` hingga `has_more` bernilai `false`.

```bash cURL
project_id="claude_proj_01KGp4eZNug9ri4kE35RSppq"

curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/projects/$project_id/attachments" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01"
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
  Setiap penghapusan yang berhasil bersifat permanen dan langsung berlaku. Tidak ada periode pemulihan.
</Warning>

Compliance API menyediakan endpoint penghapusan permanen untuk chat, file, dokumen proyek, dan seluruh proyek. Chat yang dihapus secara permanen tidak dapat dipulihkan dan tidak lagi muncul di respons daftar.

* [Menghapus chat](https://platform.claude.com/docs/id/api/compliance/apps/chats/delete): juga menghapus pesan-pesan chat dan semua file yang dilampirkan ke pesan tersebut.
* [Menghapus file](https://platform.claude.com/docs/id/api/compliance/apps/chats/files/delete): menangani file chat maupun file proyek.
* [Menghapus dokumen proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/documents/delete): menghapus satu dokumen proyek berdasarkan ID.
* [Menghapus proyek](https://platform.claude.com/docs/id/api/compliance/apps/projects/delete): lihat [Melepaskan chat sebelum menghapus proyek](https://platform.claude.com/docs/id/manage-claude/compliance-content-data#detach-chats-before-deleting-a-project).

Keempat endpoint memerlukan scope `delete:compliance_user_data`. Scope ini diberikan terpisah dari scope baca saat Compliance Access Key dibuat.

Permintaan berikut menghapus satu chat. Pola yang sama berlaku untuk endpoint penghapusan lainnya; hanya URL-nya yang berbeda.

```bash cURL
# PERINGATAN: Operasi ini menghapus chat secara PERMANEN, beserta semua pesannya,
# dan semua file terlampir. Penghapusan berlaku seketika dan tidak dapat dibatalkan. Operasi ini
# memerlukan scope `delete:compliance_user_data`, yang diberikan terpisah
# dari `read:compliance_user_data` saat Compliance Access Key dibuat.
# Pastikan Anda memiliki otorisasi eksplisit sebelum menjalankan ini.

chat_id="claude_chat_01H5CWunD7RpVJ5bHa8RCkja"

curl --fail-with-body -sS -X DELETE \
  "https://api.anthropic.com/v1/compliance/apps/chats/$chat_id" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01"
```

```json Response
{
  "id": "claude_chat_01H5CWunD7RpVJ5bHa8RCkja",
  "type": "claude_chat_deleted"
}
```

Setiap penghapusan yang berhasil mengembalikan envelope konfirmasi kecil berisi `id` dan diskriminator `type`. Endpoint chat mengembalikan `claude_chat_deleted`. Periksa field `type` sebelum menganggap penghapusan telah terkonfirmasi. Untuk nilai `type` persis yang dikembalikan endpoint lainnya, lihat skema respons di halaman [referensi API](https://platform.claude.com/docs/id/api/compliance/apps) masing-masing endpoint penghapusan.

### Melepaskan chat sebelum menghapus proyek

Proyek tidak dapat dihapus selama masih ada chat yang terlampir padanya. API mengembalikan 409 dengan body berikut:

```json
{
  "error": {
    "type": "invalid_request_error",
    "message": "The \"claude_proj_01KGp4eZNug9ri4kE35RSppq\" project cannot be deleted as it has chats attached to it. Delete or detach all chats, and try deleting the project again."
  }
}
```

Untuk mengatasinya:

1. Cantumkan chat milik proyek dengan `GET /v1/compliance/apps/chats?user_ids[]={user_id}&project_ids[]={project_id}`. Filter `project_ids[]` memerlukan setidaknya satu nilai `user_ids[]`; dapatkan ID tersebut melalui [Mencantumkan pengguna organisasi](https://platform.claude.com/docs/id/manage-claude/compliance-org-data#list-organization-users).
2. Hapus setiap chat dengan `DELETE /v1/compliance/apps/chats/{claude_chat_id}`, atau pindahkan chat keluar dari proyek melalui claude.ai.
3. Coba lagi penghapusan proyek.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Referensi API" href="https://platform.claude.com/docs/id/api/compliance/apps">
    Skema permintaan dan respons lengkap untuk setiap endpoint chat, file, proyek, dan artifact.
  </Card>

  <Card title="Mengambil transkrip sesi" href="https://platform.claude.com/docs/id/manage-claude/compliance-sessions">
    Cantumkan sesi yang dijalankan pengguna Anda di aplikasi dan agen Claude, seperti Cowork dan Claude Code, lalu ambil transkripnya.
  </Card>

  <Card title="Mencantumkan organisasi, pengguna, peran, grup, dan pengaturan" href="https://platform.claude.com/docs/id/manage-claude/compliance-org-data">
    Data orang dan tim yang terkait dengan chat dan proyek di halaman ini.
  </Card>
</CardGroup>
