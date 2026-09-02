---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/spend-limits-api
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 5ca6fe118600231f83ceded01b42a18ffc1cd4c630f43740fedfebfbc5c808ab
---

---
title: Spend Limits API
url: https://platform.claude.com/docs/id/manage-claude/spend-limits-api
description: Tetapkan batas pengeluaran pada setiap anggota Claude Enterprise, lihat dari mana batas pengeluaran setiap anggota diwarisi, dan tinjau atau tindak lanjuti permintaan anggota untuk batas yang lebih tinggi.
---

Spend Limits API memungkinkan Anda menetapkan "spend limit" (batas pengeluaran) pada setiap anggota Claude Enterprise, melihat dari mana batas pengeluaran setiap anggota diwarisi, dan meninjau atau menindaklanjuti permintaan anggota untuk batas yang lebih tinggi.

Untuk *pelaporan* penggunaan dan biaya per pengguna dan per rentang waktu, lihat [Analytics APIs](https://platform.claude.com/docs/id/manage-claude/analytics-api).

<Check>
  **Diperlukan kunci Admin API dengan cakupan**

  Endpoint ini memerlukan kunci Admin API dengan cakupan `read:spend_limits` (untuk endpoint `GET`) atau cakupan `write:spend_limits` (untuk endpoint `POST` dan `DELETE`). Lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization) untuk mengetahui di mana primary owner Anda membuatnya dan cakupan mana yang harus dipilih. Sertakan kunci tersebut dalam header `x-api-key` pada setiap permintaan.
</Check>

<Note>
  Spend Limits API hanya tersedia untuk organisasi Claude Enterprise. API ini tidak tersedia untuk organisasi Claude Platform (Claude Console).
</Note>

## Ikhtisar

API ini menyediakan delapan endpoint pada dua sumber daya:

| Sumber daya                       | Endpoint                                                                                                                                                                                                                                              | Digunakan untuk                                                                                                                                                      |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Spend limits**                  | `GET /v1/organizations/spend_limits/effective` `GET /v1/organizations/spend_limits/{spend_limit_id}` `POST /v1/organizations/spend_limits` `DELETE /v1/organizations/spend_limits/{spend_limit_id}`                                                   | Membaca batas pengeluaran efektif setiap anggota dan pengeluaran periode berjalan; menetapkan atau menghapus override per pengguna.                                  |
| **Spend limit increase requests** | `GET /v1/organizations/spend_limit_increase_requests` `GET /v1/organizations/spend_limit_increase_requests/{id}` `POST /v1/organizations/spend_limit_increase_requests/{id}/approve` `POST /v1/organizations/spend_limit_increase_requests/{id}/deny` | Mendaftar permintaan anggota untuk batas pengeluaran yang lebih tinggi, beserta konteks yang diperlukan untuk memutuskan; menyetujui atau menolak setiap permintaan. |

Gunakan endpoint **spend limits** untuk menjawab "batas pengeluaran apa yang berlaku untuk setiap anggota, dari mana asalnya, dan seberapa dekat mereka dengan batas tersebut?" serta untuk menetapkan override per pengguna. Gunakan endpoint **spend limit increase requests** untuk memproses antrean permintaan yang diajukan anggota.

## Prasyarat

* Organisasi Anda harus menggunakan paket Claude Enterprise.
* Kredit penggunaan harus diaktifkan untuk organisasi Anda. Primary owner Anda dapat mengaktifkannya di pengaturan penagihan claude.ai.

## Mulai cepat

Daftarkan batas pengeluaran bulanan efektif dan pengeluaran periode berjalan setiap anggota:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limits/effective?limit=20" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Konsep utama

### Hierarki batas pengeluaran

Sebuah **effective spend limit** (batas pengeluaran efektif) berlaku pada pengeluaran setiap anggota, yang ditentukan dari hierarki tingkat cakupan. Ketika seorang anggota tidak memiliki override per pengguna, mereka mewarisi batas pengeluaran yang dikonfigurasi untuk grup mereka (jika organisasi Anda menggunakan batas berbasis grup), seat tier mereka, atau default seluruh organisasi. Batas pengeluaran grup adalah default per anggota: setiap anggota yang mewarisinya dibatasi berdasarkan pengeluaran mereka sendiri, bukan anggaran grup yang digabungkan.

Membaca `GET /v1/organizations/spend_limits/effective` mengembalikan setiap anggota saat ini beserta batas pengeluaran efektif mereka yang telah ditentukan, dari mana batas tersebut ditentukan (`source`), dan pengeluaran periode berjalan mereka. Menetapkan override per pengguna dengan `POST /v1/organizations/spend_limits` mengunci seorang anggota pada batas pengeluaran tertentu terlepas dari apa yang seharusnya mereka warisi. Menghapus override mengembalikan mereka ke batas pengeluaran yang diwarisi (atau membiarkan mereka tanpa batas jika tidak ada).

Field `source` pada baris setiap anggota memberi tahu Anda dari tingkat mana batas pengeluaran mereka ditentukan: `user` (override per pengguna), `seat_tier`, `rbac_group`, atau `organization`. Perlakukan tipe cakupan sebagai himpunan terbuka; lewati nilai yang tidak dikenal alih-alih gagal.

### Periode

`period` adalah jendela berulang di mana batas pengeluaran diberlakukan dan pengeluaran direset. Sebuah batas pengeluaran diidentifikasi oleh pasangan `(scope, period)`-nya. Saat ini `monthly` adalah satu-satunya periode yang didukung; pengeluaran bulanan direset pada 00:00 UTC di tanggal satu setiap bulan kalender. Perlakukan `period` sebagai himpunan terbuka.

### Jumlah dan mata uang

Semua nilai moneter berupa string dalam **satuan minor mata uang penagihan organisasi** (sen, untuk USD). Misalnya, `"50000"` merepresentasikan 500,00 USD. Parse sebagai desimal dan bagi dengan 100 untuk menampilkan dolar; hindari floating-point biner untuk nilai besar.

`amount` bersifat **nullable**. Pada baris efektif seorang anggota, `null` berarti **tanpa batas** (tidak ada batas pengeluaran) dan `"0"` berarti anggota tidak dapat menggunakan Claude melebihi penggunaan yang termasuk dalam paket mereka. Pada baris batas pengeluaran yang dikonfigurasi (seperti yang dikembalikan oleh `GET /v1/organizations/spend_limits/{id}`), `null` hanya berarti tidak ada batas pengeluaran numerik yang ditetapkan; baca baris efektif anggota untuk membedakan tanpa batas dari hanya-penggunaan-termasuk.

`period_to_date_spend` adalah pengeluaran anggota yang terakumulasi sejak awal `period` saat ini, dalam format satuan minor yang sama; nilainya dapat mencakup bagian pecahan (misalnya, `"41280.125"`). Nilainya dapat terbaca sebagai `"0"` jika pembacaan pengeluaran sementara tidak tersedia; perlakukan sebagai informasional, bukan transaksional.

### Siklus hidup permintaan kenaikan

Sebuah **spend limit increase request** (permintaan kenaikan batas pengeluaran) dibuat ketika seorang anggota mengklik **Request more usage** di claude.ai. Permintaan tidak dibuat melalui API ini. `status` sebuah permintaan adalah salah satu dari:

| Status     | Arti                                                                                                                                                                                                                                                                    |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pending`  | Menunggu tindakan admin. Permintaan biasanya membawa `spend_summary` langsung sehingga Anda dapat melihat batas pengeluaran efektif anggota saat ini dan pengeluaran periode berjalan saat memutuskan; `spend_summary` dapat bernilai `null` jika tidak dapat dihitung. |
| `approved` | Permintaan diselesaikan dengan persetujuan: baik admin menyetujuinya secara eksplisit, tindakan admin lain menaikkan batas pengeluaran anggota, atau dukungan Anthropic menaikkan batas pengeluaran atas nama organisasi. `spend_summary` bernilai `null`.              |
| `denied`   | Admin menolak. `spend_summary` bernilai `null`. claude.ai menyembunyikan tombol permintaan anggota tersebut selama 30 hari sejak `resolved_at`; admin tetap dapat menaikkan batas pengeluaran anggota secara langsung kapan saja.                                       |

Baik `approved` maupun `denied` bersifat terminal. Seorang anggota memiliki paling banyak satu permintaan `pending` pada satu waktu.

Menyetujui dengan `POST /v1/organizations/spend_limit_increase_requests/{id}/approve` menulis baris batas pengeluaran per pengguna yang sama dengan yang ditulis oleh `POST /v1/organizations/spend_limits`. Menetapkan batas pengeluaran secara langsung **tidak** mentransisikan permintaan yang pending; gunakan endpoint approve untuk menyelesaikan permintaan.

Secara default, Anthropic mengirim email kepada anggota ketika permintaan mereka disetujui atau ditolak. Sertakan `suppress_notification: true` pada approve atau deny untuk menekan email tersebut (misalnya, ketika sistem Anda sendiri yang memberi tahu anggota).

## Pembatasan laju

Kedelapan endpoint berbagi satu "rate limit" (batas laju) per organisasi sebesar **60 permintaan per menit**. Permintaan yang melebihi batas mengembalikan **429 Too Many Requests**.

## Paginasi

`GET /v1/organizations/spend_limits/effective` dan `GET /v1/organizations/spend_limit_increase_requests` dipaginasi dengan **cursor opaque**. Permintaan pertama mengembalikan hingga `limit` baris ditambah cursor `next_page`; teruskan cursor tersebut tanpa perubahan sebagai parameter `page` pada permintaan berikutnya, dan ulangi hingga `next_page` bernilai `null`.

**Jangan mengubah parameter query di tengah urutan.** Cursor terikat pada filter yang menerbitkannya. Jika Anda mengubah `user_ids[]`, `period[]`, `status[]`, atau `actor_ids[]` dan meneruskan cursor lama, Anda akan mendapatkan 400 dengan *"cursor does not match current query parameters"*. Mulailah urutan baru dari halaman pertama.

## Serialisasi parameter list

Parameter list menggunakan notasi kurung siku: ulangi nama parameter dengan `[]` untuk setiap nilai.

```text wrap
user_ids[]=user_01AbCdEfGh&user_ids[]=user_01JkLmNoPq
```

## Respons error

Respons error mengikuti bentuk standar yang didokumentasikan di [Errors](https://platform.claude.com/docs/id/api/errors). Kutip `request_id` dari body respons saat menghubungi dukungan.

## Spend limits

### Mendaftar batas pengeluaran efektif setiap anggota

`GET /v1/organizations/spend_limits/effective` mengembalikan satu baris per anggota saat ini, yang mencerminkan batas pengeluaran efektif setiap anggota, `source`-nya dalam hierarki cakupan, dan `period_to_date_spend` mereka. Memerlukan cakupan `read:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [List effective spend limits](https://platform.claude.com/docs/id/api/admin/spend_limits/list_effective) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limits/effective?limit=20" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "data": [
    {
      "scope": { "type": "user", "user_id": "user_01AbCdEfGh" },
      "actor": {
        "type": "user_actor",
        "user_id": "user_01AbCdEfGh",
        "name": "Jane Smith",
        "email_address": "jane@example.com",
        "deleted": false
      },
      "amount": "50000",
      "currency": "USD",
      "period": "monthly",
      "source": { "type": "seat_tier", "seat_tier": "enterprise_standard" },
      "spend_limit_id": "spl_01XyZaBcDeFgHiJkLmNoPq",
      "period_to_date_spend": "31402.5"
    }
  ],
  "next_page": "page_..."
}
```

### Mendapatkan satu batas pengeluaran

`GET /v1/organizations/spend_limits/{spend_limit_id}` mengembalikan satu batas pengeluaran yang dikonfigurasi berdasarkan ID. Gunakan untuk memeriksa baris yang dirujuk oleh field `spend_limit_id`. Memerlukan cakupan `read:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Retrieve a spend limit](https://platform.claude.com/docs/id/api/admin/spend_limits/retrieve) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limits/spl_01AbCdEfGhIjKlMnOpQrSt" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

### Menetapkan override per pengguna

`POST /v1/organizations/spend_limits` menetapkan override batas pengeluaran per pengguna. Ini adalah upsert dengan kunci `(scope, period)`: menetapkan batas untuk pengguna dan periode yang sudah memilikinya akan menimpanya di tempat. Endpoint ini hanya menerima `scope.type: "user"`; default tingkat seat-tier, grup, dan organisasi dikonfigurasi di pengaturan claude.ai. Memerlukan cakupan `write:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Create a spend limit](https://platform.claude.com/docs/id/api/admin/spend_limits/create) di referensi API.

```bash cURL
curl --request POST "https://api.anthropic.com/v1/organizations/spend_limits" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"scope": {"type": "user", "user_id": "user_01AbCdEfGh"}, "amount": "75000"}'
```

```json
{
  "type": "spend_limit",
  "id": "spl_01RsTuVwXyZaBcDeFgHiJk",
  "created_at": "2026-05-11T10:02:44Z",
  "updated_at": "2026-05-11T10:02:44Z",
  "scope": { "type": "user", "user_id": "user_01AbCdEfGh" },
  "amount": "75000",
  "currency": "USD",
  "period": "monthly"
}
```

### Menghapus override per pengguna

`DELETE /v1/organizations/spend_limits/{spend_limit_id}` menghapus override per pengguna, setelah itu anggota kembali ke default seat-tier, grup, atau organisasi yang diwarisi. Baris tingkat seat-tier, grup, dan organisasi tidak dapat dihapus melalui endpoint ini. Memerlukan cakupan `write:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Delete a spend limit](https://platform.claude.com/docs/id/api/admin/spend_limits/delete) di referensi API.

```bash cURL
curl --request DELETE "https://api.anthropic.com/v1/organizations/spend_limits/spl_01RsTuVwXyZaBcDeFgHiJk" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Spend limit increase requests

### Mendaftar permintaan kenaikan

`GET /v1/organizations/spend_limit_increase_requests` mendaftar permintaan, yang terbaru lebih dulu. Filter berdasarkan `status[]` (`pending`, `approved`, `denied`) dan `actor_ids[]`. Daftar ini mengecualikan permintaan yang pemohonnya bukan lagi anggota organisasi. Memerlukan cakupan `read:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [List spend limit increase requests](https://platform.claude.com/docs/id/api/admin/spend_limits/increase_requests/list) di referensi API.

```bash cURL
curl --globoff "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests?status[]=pending&limit=50" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Setiap permintaan pending membawa `spend_summary` langsung yang menunjukkan batas pengeluaran efektif pemohon saat ini dan pengeluaran periode berjalan, cukup untuk memutuskan tanpa pencarian terpisah.

### Mendapatkan satu permintaan kenaikan

`GET /v1/organizations/spend_limit_increase_requests/{id}` mengembalikan satu permintaan berdasarkan ID. Memerlukan cakupan `read:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Retrieve a spend limit increase request](https://platform.claude.com/docs/id/api/admin/spend_limits/increase_requests/retrieve) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

### Menyetujui permintaan kenaikan

`POST /v1/organizations/spend_limit_increase_requests/{id}/approve` menyetujui permintaan pending: endpoint ini menulis batas pengeluaran per pengguna pada `amount` yang diberikan admin untuk pemohon dan mentransisikan permintaan ke `approved`. Permintaan tidak membawa jumlah yang diminta; Anda memberikan batas pengeluaran baru saat persetujuan. Memerlukan cakupan `write:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Approve a spend limit increase request](https://platform.claude.com/docs/id/api/admin/spend_limits/increase_requests/approve) di referensi API.

```bash cURL
curl --request POST "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt/approve" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"amount": "75000", "suppress_notification": true}'
```

### Menolak permintaan kenaikan

`POST /v1/organizations/spend_limit_increase_requests/{id}/deny` menolak permintaan pending. Idempoten pada `denied`: menolak permintaan yang sudah ditolak mengembalikan 200 dengan sumber daya yang ada. Endpoint ini menolak upaya untuk menolak permintaan yang sudah disetujui sehingga otomatisasi dapat membedakan percobaan ulang dari keputusan yang bertentangan. Memerlukan cakupan `write:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Deny a spend limit increase request](https://platform.claude.com/docs/id/api/admin/spend_limits/increase_requests/deny) di referensi API.

```bash cURL
curl --request POST "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt/deny" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"suppress_notification": true}'
```

## Contoh alur kerja

Beberapa alur kerja ini menggabungkan Spend Limits API dengan endpoint biaya [Analytics APIs](https://platform.claude.com/docs/id/manage-claude/analytics-api). Endpoint biaya Analytics dirancang untuk pelaporan pengeluaran seluruh organisasi dalam rentang tanggal. `GET /spend_limits/effective` mengembalikan batas yang saat ini berlaku untuk setiap anggota. Mulailah penyisiran dengan Analytics untuk menemukan anggota mana yang perlu dilihat, lalu baca batas mereka saat ini dengan `/effective`.

Endpoint Spend Limits memerlukan cakupan `spend_limits` dan endpoint biaya Analytics memerlukan `read:analytics`; lihat [Analytics APIs](https://platform.claude.com/docs/id/manage-claude/analytics-api) untuk cara menyediakan akses. Semua nilai moneter pada keduanya berupa string desimal dalam satuan minor (sen). Kedua API dipaginasi dengan cursor opaque. Tetapkan `limit` eksplisit dan telusuri halaman melalui `next_page` hingga bernilai `null` untuk mencakup seluruh organisasi.

### Mengotomatiskan alur peninjauan permintaan kenaikan

Jalankan job terjadwal yang mengambil permintaan pending, menerapkan kebijakan persetujuan organisasi Anda, dan menyelesaikan masing-masing.

1. Daftarkan permintaan pending:

   ```bash cURL
   curl --globoff "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests?status[]=pending&limit=100" \
     --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
   ```

   Setiap permintaan membawa `actor.user_id` pemohon dan `spend_summary` langsung dengan `amount` efektif mereka saat ini dan `period_to_date_spend`, cukup untuk memutuskan tanpa pencarian terpisah.

2. Terapkan kebijakan Anda. Misalnya, setujui otomatis ketika `amount` anggota saat ini di bawah ambang, dan arahkan batas yang lebih besar untuk peninjauan manual.

3. Selesaikan setiap permintaan. Untuk menyetujui, berikan batas baru:

   ```bash cURL
   curl --request POST "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/{id}/approve" \
     --header "content-type: application/json" \
     --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
     --data '{"amount": "75000", "suppress_notification": true}'
   ```

   Untuk menolak, lakukan `POST` ke `.../{id}/deny`. Sertakan `suppress_notification: true` ketika sistem Anda sendiri yang memberi tahu pemohon.

### Mengidentifikasi anggota yang mendekati batas pengeluaran mereka

Temukan anggota yang mendekati batas mereka sehingga Anda dapat menaikkannya sebelum mereka terblokir.

1. Ambil pengeluaran bulan berjalan setiap anggota dari Analytics API (satu baris per anggota, pengeluaran tertinggi lebih dulu secara default):

   ```bash cURL
   curl "https://api.anthropic.com/v1/organizations/analytics/user_cost_report?starting_at=2026-06-01T00:00:00Z&limit=1000" \
     --header "x-api-key: $ANALYTICS_API_KEY"
   ```

   Setiap baris membawa `actor.user_id`, `actor.email`, dan `amount` (pengeluaran anggota dalam sen). Telusuri halaman melalui `next_page` untuk mencakup seluruh organisasi.

2. Untuk pembelanja teratas (atau semua orang di atas ambang dolar), ambil batas efektif dalam batch:

   ```bash cURL
   curl --globoff "https://api.anthropic.com/v1/organizations/spend_limits/effective?user_ids[]=user_01Ab...&user_ids[]=user_01Cd...&limit=100" \
     --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
   ```

   Setiap baris mengembalikan batas sebagai `amount` (`null` = tanpa batas, `"0"` = hanya penggunaan termasuk) bersama `period_to_date_spend`.

3. Untuk setiap anggota dengan batas positif, hitung `period_to_date_spend / amount` dan tandai mereka yang berada pada atau di atas ambang Anda (misalnya, 80 persen). Perlakukan batas `"0"` sebagai sudah mencapai batas. Tidak ada filter sisi server untuk rasio ini.

4. Tindak lanjuti anggota yang ditandai: naikkan batas dengan `POST /v1/organizations/spend_limits`, setujui permintaan kenaikan pending jika ada, atau hubungi anggota tersebut.

### Menemukan anggota dengan penggunaan yang berubah cepat

Munculkan anggota yang pengeluarannya melonjak dari minggu ke minggu.

1. Ambil biaya harian per anggota untuk dua minggu terakhir dari Analytics API:

   ```bash cURL
   curl "https://api.anthropic.com/v1/organizations/analytics/user_cost_report?starting_at=2026-06-09T00:00:00Z&ending_at=2026-06-23T00:00:00Z&bucket_width=1d&limit=1000" \
     --header "x-api-key: $ANALYTICS_API_KEY"
   ```

   Dengan `bucket_width` ditetapkan, setiap anggota mencakup satu baris per hari dengan penggunaan; telusuri halaman melalui `next_page` untuk mengumpulkan seri lengkap setiap anggota.

2. Kelompokkan baris berdasarkan `actor.user_id`. Untuk setiap anggota, jumlahkan tujuh hari terakhir dan tujuh hari sebelumnya. Tandai anggota yang minggu terakhirnya melebihi minggu sebelumnya dengan kelipatan pilihan Anda (misalnya, tiga). Biaya hari-hari terakhir bersifat sementara dan dapat direvisi naik; untuk perbandingan yang dapat diulang, tetapkan `ending_at` pada atau sebelum `data_refreshed_at` yang dikembalikan sebelumnya (lihat [Ketersediaan dan kesegaran data](https://platform.claude.com/docs/id/manage-claude/analytics-api#data-availability-and-freshness)).

3. Tindak lanjuti anggota yang ditandai: sesuaikan batas dengan `POST /v1/organizations/spend_limits`, atau hubungi mereka.

### Menaikkan sementara batas pengeluaran anggota selama insiden

Beri ruang bagi penanggap insiden untuk bekerja selama insiden terbuka: naikkan batas pengeluaran mereka ketika insiden dimulai, dan kembalikan setelah insiden ditutup. Kendalikan kenaikan tersebut berdasarkan sistem manajemen insiden Anda, misalnya dengan mewajibkan ID insiden aktif dengan anggota yang ditugaskan padanya.

1. Baca batas anggota saat ini, dan catat untuk rollback:

   ```bash cURL
   curl --globoff "https://api.anthropic.com/v1/organizations/spend_limits/effective?user_ids[]=user_01AbCdEfGh&period[]=monthly" \
     --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
   ```

2. Naikkan batas:

   ```bash cURL
   curl --request POST "https://api.anthropic.com/v1/organizations/spend_limits" \
     --header "content-type: application/json" \
     --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
     --data '{"scope": {"type": "user", "user_id": "user_01AbCdEfGh"}, "amount": "500000", "period": "monthly"}'
   ```

3. Jika penanggap memerlukan akses yang lebih luas selama insiden, sediakan terlebih dahulu grup incident-responders yang [peran kustomnya](https://platform.claude.com/docs/id/manage-claude/user-management#custom-roles) memberikan akses tersebut, dan tambahkan anggota selama durasi insiden:

   ```bash cURL
   curl --request POST "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members" \
     --header "content-type: application/json" \
     --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
     --data '{"user_id": "user_01AbCdEfGh"}'
   ```

   Lihat [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management#groups) untuk endpoint grup.

4. Ketika sistem insiden Anda menandai insiden ditutup, kembalikan kedua perubahan: pulihkan batas pengeluaran yang Anda catat di langkah 1 (atau hapus override dengan `DELETE /v1/organizations/spend_limits/{spend_limit_id}` jika anggota sebelumnya tidak memilikinya), dan hapus anggota dari grup dengan `DELETE /v1/organizations/rbac_groups/{group_id}/members/{user_id}`.

## Pertanyaan yang sering diajukan

### Apakah menetapkan batas pengeluaran secara langsung menyelesaikan permintaan kenaikan pending seorang anggota?

Tidak. `POST /v1/organizations/spend_limits` menulis override tetapi membiarkan permintaan pending tidak tersentuh. Gunakan `POST /v1/organizations/spend_limit_increase_requests/{id}/approve` untuk menyelesaikan permintaan dan menulis override dalam satu panggilan.

### Apa yang terjadi ketika saya menghapus override per pengguna?

Anggota kembali ke apa pun yang akan mereka warisi dari hierarki: default grup, seat-tier, atau organisasi mereka. Jika tidak ada default di tingkat mana pun, anggota tersebut tanpa batas.

### Dapatkah saya menetapkan default seat-tier atau seluruh organisasi melalui API ini?

Tidak. Hanya override per pengguna yang dapat ditulis melalui API ini. Default tingkat seat-tier, grup, dan organisasi dikonfigurasi di pengaturan Organisasi claude.ai.

### Mengapa `period_to_date_spend` terkadang terbaca sebagai `"0"` untuk anggota aktif?

Pembacaan pengeluaran dapat sementara tidak tersedia, dalam hal ini field terbaca `"0"` alih-alih menghasilkan error. Perlakukan sebagai informasional.

## Lihat juga

<CardGroup cols={2}>
  <Card title="Referensi Spend Limits API" href="https://platform.claude.com/docs/id/api/admin/spend_limits">
    Skema permintaan dan respons yang dihasilkan untuk setiap endpoint Spend Limits API.
  </Card>

  <Card title="Referensi Spend Limit Increase Requests API" href="https://platform.claude.com/docs/id/api/admin/spend_limits/increase_requests">
    Skema permintaan dan respons yang dihasilkan untuk endpoint permintaan kenaikan.
  </Card>

  <Card title="Analytics APIs" href="https://platform.claude.com/docs/id/manage-claude/analytics-api">
    Pelaporan penggunaan dan biaya per pengguna dan per rentang waktu untuk Claude Enterprise.
  </Card>
</CardGroup>
