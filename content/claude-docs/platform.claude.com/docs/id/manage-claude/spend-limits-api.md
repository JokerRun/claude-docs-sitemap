---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/spend-limits-api
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: cadad0134c489ab1bbe4f187ca29db120e7ac7dff10341fc6cf900aef7a3f4d3
---

# Spend Limits API

Tetapkan batas pengeluaran pada setiap anggota Claude Enterprise, lihat dari mana batas pengeluaran setiap anggota diwarisi, dan tinjau atau tindak lanjuti permintaan anggota untuk batas yang lebih tinggi.

---

Spend Limits API memungkinkan Anda menetapkan batas pengeluaran pada setiap anggota Claude Enterprise, melihat dari mana batas pengeluaran setiap anggota diwarisi, dan meninjau atau menindaklanjuti permintaan anggota untuk batas yang lebih tinggi.

Untuk *pelaporan* penggunaan dan biaya per pengguna dan berdasarkan rentang waktu, lihat [Analytics API](/docs/id/manage-claude/analytics-api).

<Check>
  **Diperlukan kunci Admin API dengan cakupan tertentu**

  Endpoint ini memerlukan kunci Admin API dengan cakupan `read:spend_limits` (untuk endpoint `GET`) atau cakupan `write:spend_limits` (untuk endpoint `POST` dan `DELETE`). Lihat [Membuat kunci Admin API](/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization) untuk mengetahui di mana pemilik utama Anda membuatnya dan cakupan mana yang harus dipilih. Sertakan kunci tersebut dalam header `x-api-key` pada setiap permintaan.
</Check>

<Note>
  Spend Limits API hanya tersedia untuk organisasi Claude Enterprise. API ini tidak tersedia untuk organisasi Claude Platform (Claude Console).
</Note>

## Ikhtisar \{#overview}

API ini menyediakan delapan endpoint di dua resource:

| Resource | Endpoint | Digunakan untuk |
|---|---|---|
| **Spend limits** | `GET /v1/organizations/spend_limits/effective`<br/>`GET /v1/organizations/spend_limits/{spend_limit_id}`<br/>`POST /v1/organizations/spend_limits`<br/>`DELETE /v1/organizations/spend_limits/{spend_limit_id}` | Membaca batas pengeluaran efektif setiap anggota dan pengeluaran periode-hingga-saat-ini; menetapkan atau menghapus override per pengguna. |
| **Spend limit increase requests** | `GET /v1/organizations/spend_limit_increase_requests`<br/>`GET /v1/organizations/spend_limit_increase_requests/{id}`<br/>`POST /v1/organizations/spend_limit_increase_requests/{id}/approve`<br/>`POST /v1/organizations/spend_limit_increase_requests/{id}/deny` | Mencantumkan permintaan anggota untuk batas pengeluaran yang lebih tinggi, dengan konteks yang diperlukan untuk memutuskan; menyetujui atau menolak setiap permintaan. |

Gunakan endpoint **spend limits** untuk menjawab "batas pengeluaran apa yang berlaku untuk setiap anggota, dari mana asalnya, dan seberapa dekat mereka dengan batas tersebut?" dan untuk menetapkan override per pengguna. Gunakan endpoint **spend limit increase requests** untuk memproses antrean permintaan yang diajukan anggota.

## Prasyarat \{#prerequisites}

- Organisasi Anda harus menggunakan paket Claude Enterprise.
- Kredit penggunaan harus diaktifkan untuk organisasi Anda. Pemilik utama Anda dapat mengaktifkannya di pengaturan penagihan claude.ai.

## Mulai cepat \{#quick-start}

Cantumkan batas pengeluaran bulanan efektif setiap anggota dan pengeluaran periode-hingga-saat-ini:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limits/effective?limit=20" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Konsep utama \{#key-concepts}

### Hierarki batas pengeluaran \{#the-spend-limit-hierarchy}

Sebuah **batas pengeluaran efektif** berlaku untuk pengeluaran setiap anggota, yang diresolusi dari hierarki tingkat cakupan. Ketika seorang anggota tidak memiliki override per pengguna, mereka mewarisi batas pengeluaran yang dikonfigurasi untuk grup mereka (jika organisasi Anda menggunakan batas berbasis grup), tingkat kursi mereka, atau default seluruh organisasi. Batas pengeluaran grup adalah default per anggota: setiap anggota yang mewarisinya dibatasi berdasarkan pengeluaran mereka sendiri, bukan anggaran grup yang digabungkan.

Membaca `GET /v1/organizations/spend_limits/effective` mengembalikan setiap anggota saat ini dengan batas pengeluaran efektif mereka yang telah diresolusi, dari mana batas tersebut diresolusi (`source`), dan pengeluaran periode-hingga-saat-ini mereka. Menetapkan override per pengguna dengan `POST /v1/organizations/spend_limits` mengunci seorang anggota ke batas pengeluaran tertentu terlepas dari apa yang seharusnya mereka warisi. Menghapus override mengembalikan mereka ke batas pengeluaran yang diwarisi (atau membiarkan mereka tanpa batas jika tidak ada yang diwarisi).

Field `source` pada setiap baris anggota memberi tahu Anda dari tingkat mana batas pengeluaran mereka diresolusi: `user` (override per pengguna), `seat_tier`, `rbac_group`, atau `organization`. Perlakukan tipe cakupan sebagai himpunan terbuka; lewati nilai yang tidak dikenal alih-alih gagal.

### Periode \{#period}

`period` adalah jendela berulang di mana batas pengeluaran diberlakukan dan pengeluaran direset. Sebuah batas pengeluaran diidentifikasi oleh pasangan `(scope, period)`-nya. Saat ini `monthly` adalah satu-satunya periode yang didukung; pengeluaran bulanan direset pada pukul 00:00 UTC pada tanggal pertama setiap bulan kalender. Perlakukan `period` sebagai himpunan terbuka.

### Jumlah dan mata uang \{#amounts-and-currency}

Semua nilai moneter adalah string dalam **unit minor dari mata uang penagihan organisasi** (sen, untuk USD). Misalnya, `"50000"` mewakili 500,00 USD. Parse sebagai desimal dan bagi dengan 100 untuk menampilkan dolar; hindari floating-point biner untuk nilai besar.

`amount` bersifat **nullable**. Pada baris efektif seorang anggota, `null` berarti **tanpa batas** (tidak ada batas pengeluaran) dan `"0"` berarti anggota tidak dapat menggunakan Claude di luar penggunaan yang termasuk dalam paket mereka. Pada baris batas pengeluaran yang dikonfigurasi (seperti yang dikembalikan oleh `GET /v1/organizations/spend_limits/{id}`), `null` hanya berarti tidak ada batas pengeluaran numerik yang ditetapkan; baca baris efektif anggota untuk membedakan antara tanpa batas dan hanya-penggunaan-yang-termasuk.

`period_to_date_spend` adalah pengeluaran anggota yang terakumulasi sejak awal `period` saat ini, dalam format unit minor yang sama; nilai ini dapat menyertakan bagian pecahan (misalnya, `"41280.125"`). Nilai ini dapat terbaca sebagai `"0"` jika pembacaan pengeluaran sementara tidak tersedia; perlakukan sebagai informasi, bukan transaksional.

### Siklus hidup permintaan peningkatan \{#increase-request-lifecycle}

Sebuah **permintaan peningkatan batas pengeluaran** dibuat ketika seorang anggota mengklik **Request more usage** di claude.ai. Permintaan tidak dibuat melalui API ini. `status` sebuah permintaan adalah salah satu dari:

| Status | Arti |
|---|---|
| `pending` | Menunggu tindakan admin. Permintaan biasanya membawa `spend_summary` langsung sehingga Anda dapat melihat batas pengeluaran efektif anggota saat ini dan pengeluaran periode-hingga-saat-ini saat memutuskan; `spend_summary` dapat bernilai `null` jika tidak dapat dihitung. |
| `approved` | Permintaan diselesaikan dengan persetujuan: baik admin menyetujuinya secara eksplisit, tindakan admin lain menaikkan batas pengeluaran anggota, atau dukungan Anthropic menaikkan batas pengeluaran atas nama organisasi. `spend_summary` bernilai `null`. |
| `denied` | Admin menolak. `spend_summary` bernilai `null`. claude.ai menyembunyikan tombol permintaan anggota tersebut selama 30 hari sejak `resolved_at`; admin tetap dapat menaikkan batas pengeluaran anggota secara langsung kapan saja. |

Baik `approved` maupun `denied` bersifat terminal. Seorang anggota memiliki paling banyak satu permintaan `pending` pada satu waktu.

Menyetujui dengan `POST /v1/organizations/spend_limit_increase_requests/{id}/approve` menulis baris batas pengeluaran per pengguna yang sama dengan yang ditulis oleh `POST /v1/organizations/spend_limits`. Menetapkan batas pengeluaran secara langsung **tidak** mengubah status permintaan yang tertunda; gunakan endpoint approve untuk menyelesaikan permintaan.

Secara default, Anthropic mengirim email kepada anggota ketika permintaan mereka disetujui atau ditolak. Sertakan `suppress_notification: true` pada approve atau deny untuk menekan email tersebut (misalnya, ketika sistem Anda sendiri yang memberi tahu anggota).

## Pembatasan laju \{#rate-limiting}

Kedelapan endpoint berbagi satu batas per organisasi sebesar **60 permintaan per menit**. Permintaan yang melebihi batas mengembalikan **429 Too Many Requests**.

## Paginasi \{#pagination}

`GET /v1/organizations/spend_limits/effective` dan `GET /v1/organizations/spend_limit_increase_requests` dipaginasi dengan **kursor opaque**. Permintaan pertama mengembalikan hingga `limit` baris ditambah kursor `next_page`; teruskan kursor tersebut tanpa perubahan sebagai parameter `page` pada permintaan berikutnya, dan ulangi hingga `next_page` bernilai `null`.

**Jangan mengubah parameter kueri di tengah urutan.** Kursor terikat pada filter yang menghasilkannya. Jika Anda mengubah `user_ids[]`, `period[]`, `status[]`, atau `actor_ids[]` dan meneruskan kursor lama, Anda akan mendapatkan 400 dengan *"cursor does not match current query parameters"*. Mulai urutan baru dari halaman pertama sebagai gantinya.

## Serialisasi parameter daftar \{#serializing-list-parameters}

Parameter daftar menggunakan notasi kurung siku: ulangi nama parameter dengan `[]` untuk setiap nilai.

```text
user_ids[]=user_01AbCdEfGh&user_ids[]=user_01JkLmNoPq
```

## Respons error \{#error-responses}

Respons error mengikuti bentuk standar yang didokumentasikan di [Errors](/docs/id/api/errors). Kutip `request_id` dari body respons saat menghubungi dukungan.

## Spend limits \{#spend-limits}

### Mencantumkan batas pengeluaran efektif setiap anggota \{#list-each-members-effective-spend-limit}

`GET /v1/organizations/spend_limits/effective` mengembalikan satu baris per anggota saat ini, yang mencerminkan batas pengeluaran efektif setiap anggota, `source`-nya dalam hierarki cakupan, dan `period_to_date_spend` mereka. Memerlukan cakupan `read:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [List effective spend limits](/docs/id/api/admin/spend_limits/list_effective) di referensi API.

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

### Mendapatkan satu batas pengeluaran \{#get-a-single-spend-limit}

`GET /v1/organizations/spend_limits/{spend_limit_id}` mengembalikan satu batas pengeluaran yang dikonfigurasi berdasarkan ID. Gunakan untuk memeriksa baris yang dirujuk oleh field `spend_limit_id`. Memerlukan cakupan `read:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Retrieve a spend limit](/docs/id/api/admin/spend_limits/retrieve) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limits/spl_01AbCdEfGhIjKlMnOpQrSt" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

### Menetapkan override per pengguna \{#set-a-per-user-override}

`POST /v1/organizations/spend_limits` menetapkan override batas pengeluaran per pengguna. Ini adalah upsert yang dikunci pada `(scope, period)`: menetapkan batas untuk pengguna dan periode yang sudah memilikinya akan menimpanya di tempat. Endpoint ini hanya menerima `scope.type: "user"`; default tingkat kursi, grup, dan organisasi dikonfigurasi di pengaturan claude.ai. Memerlukan cakupan `write:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Create a spend limit](/docs/id/api/admin/spend_limits/create) di referensi API.

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

### Menghapus override per pengguna \{#remove-a-per-user-override}

`DELETE /v1/organizations/spend_limits/{spend_limit_id}` menghapus override per pengguna, setelah itu anggota kembali ke default tingkat kursi, grup, atau organisasi yang diwarisi. Baris tingkat kursi, grup, dan organisasi tidak dapat dihapus melalui endpoint ini. Memerlukan cakupan `write:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Delete a spend limit](/docs/id/api/admin/spend_limits/delete) di referensi API.

```bash cURL
curl --request DELETE "https://api.anthropic.com/v1/organizations/spend_limits/spl_01RsTuVwXyZaBcDeFgHiJk" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Spend limit increase requests \{#spend-limit-increase-requests}

### Mencantumkan permintaan peningkatan \{#list-increase-requests}

`GET /v1/organizations/spend_limit_increase_requests` mencantumkan permintaan, yang terbaru lebih dulu. Filter berdasarkan `status[]` (`pending`, `approved`, `denied`) dan `actor_ids[]`. Daftar ini mengecualikan permintaan yang pemohonnya bukan lagi anggota organisasi. Memerlukan cakupan `read:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [List spend limit increase requests](/docs/id/api/admin/spend_limits/increase_requests/list) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests?status[]=pending&limit=50" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Setiap permintaan yang tertunda membawa `spend_summary` langsung yang menunjukkan batas pengeluaran efektif pemohon saat ini dan pengeluaran periode-hingga-saat-ini, cukup untuk memutuskan tanpa pencarian terpisah.

### Mendapatkan satu permintaan peningkatan \{#get-a-single-increase-request}

`GET /v1/organizations/spend_limit_increase_requests/{id}` mengembalikan satu permintaan berdasarkan ID. Memerlukan cakupan `read:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Retrieve a spend limit increase request](/docs/id/api/admin/spend_limits/increase_requests/retrieve) di referensi API.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

### Menyetujui permintaan peningkatan \{#approve-an-increase-request}

`POST /v1/organizations/spend_limit_increase_requests/{id}/approve` menyetujui permintaan yang tertunda: endpoint ini menulis batas pengeluaran per pengguna pada `amount` yang disediakan admin untuk pemohon dan mengubah status permintaan menjadi `approved`. Permintaan tidak membawa jumlah yang diminta; Anda menyediakan batas pengeluaran baru saat persetujuan. Memerlukan cakupan `write:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Approve a spend limit increase request](/docs/id/api/admin/spend_limits/increase_requests/approve) di referensi API.

```bash cURL
curl --request POST "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt/approve" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"amount": "75000", "suppress_notification": true}'
```

### Menolak permintaan peningkatan \{#deny-an-increase-request}

`POST /v1/organizations/spend_limit_increase_requests/{id}/deny` menolak permintaan yang tertunda. Idempoten pada `denied`: menolak permintaan yang sudah ditolak mengembalikan 200 dengan resource yang ada. Endpoint menolak upaya untuk menolak permintaan yang sudah disetujui sehingga otomatisasi dapat membedakan antara percobaan ulang dan keputusan yang bertentangan. Memerlukan cakupan `write:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Deny a spend limit increase request](/docs/id/api/admin/spend_limits/increase_requests/deny) di referensi API.

```bash cURL
curl --request POST "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt/deny" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"suppress_notification": true}'
```

## Pertanyaan yang sering diajukan \{#frequently-asked-questions}

### Apakah menetapkan batas pengeluaran secara langsung menyelesaikan permintaan peningkatan anggota yang tertunda? \{#does-setting-a-spend-limit-directly-resolve-a-members-pending-increase-request}

Tidak. `POST /v1/organizations/spend_limits` menulis override tetapi membiarkan permintaan yang tertunda tidak tersentuh. Gunakan `POST /v1/organizations/spend_limit_increase_requests/{id}/approve` untuk menyelesaikan permintaan dan menulis override dalam satu panggilan.

### Apa yang terjadi ketika saya menghapus override per pengguna? \{#what-happens-when-i-delete-a-per-user-override}

Anggota kembali ke apa pun yang akan mereka warisi dari hierarki: default grup, tingkat kursi, atau organisasi mereka. Jika tidak ada default di tingkat mana pun, anggota tersebut tanpa batas.

### Dapatkah saya menetapkan default tingkat kursi atau seluruh organisasi melalui API ini? \{#can-i-set-a-seat-tier-or-organization-wide-default-through-this-api}

Tidak. Hanya override per pengguna yang dapat ditulis melalui API ini. Default tingkat kursi, grup, dan organisasi dikonfigurasi di pengaturan Organisasi claude.ai.

### Mengapa `period_to_date_spend` terkadang terbaca sebagai `"0"` untuk anggota yang aktif? \{#why-does-period-to-date-spend-sometimes-read-as-0-for-an-active-member}

Pembacaan pengeluaran dapat sementara tidak tersedia, dalam hal ini field tersebut terbaca `"0"` alih-alih menghasilkan error. Perlakukan sebagai informasi.

## Lihat juga \{#see-also}

<CardGroup cols={2}>
  <Card title="Referensi Spend Limits API" href="/docs/id/api/admin/spend_limits">
    Skema permintaan dan respons yang dihasilkan untuk setiap endpoint Spend Limits API.
  </Card>
  <Card title="Referensi Spend Limit Increase Requests API" href="/docs/id/api/admin/spend_limits/increase_requests">
    Skema permintaan dan respons yang dihasilkan untuk endpoint permintaan peningkatan.
  </Card>
  <Card title="Analytics API" href="/docs/id/manage-claude/analytics-api">
    Pelaporan penggunaan dan biaya per pengguna dan berdasarkan rentang waktu untuk Claude Enterprise.
  </Card>
</CardGroup>