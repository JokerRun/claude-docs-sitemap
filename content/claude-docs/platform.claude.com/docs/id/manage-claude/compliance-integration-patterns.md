---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns
fetched_at: 2026-07-10T03:11:05.177659Z
sha256: f50b548542cd1252473deb4fa53ba823d4303870056fefcccb33fe1c9a8f2c10
---

# Rancang integrasi kepatuhan Anda

Pilih antara polling dan konsumsi Activity Feed berbasis kursor, korelasikan peristiwa Compliance API dengan SIEM Anda, dan rencanakan retensi.

---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Cakupan yang diperlukan:** `read:compliance_activities` pada Compliance Access Key atau kunci Admin API.
</Check>

Integrasi Compliance API untuk produksi membuat tiga pilihan desain: bagaimana integrasi tersebut mengonsumsi Activity Feed, bagaimana output-nya berkorelasi dengan sistem "security information and event management" (manajemen informasi dan peristiwa keamanan), atau SIEM, Anda, dan di mana salinan jangka panjang dari aktivitas dan konten disimpan. Pilihan-pilihan ini tidak bergantung pada endpoint itu sendiri; halaman ini membantu Anda mengevaluasi pertukarannya.

Halaman ini mengasumsikan Anda telah membaca [Mengkueri Activity Feed](/docs/id/manage-claude/compliance-activity-feed), yang mendefinisikan parameter dan kontrak paginasi yang dirujuk di seluruh halaman ini, dan [Mengambil dan menghapus obrolan, file, dan proyek](/docs/id/manage-claude/compliance-content-data), yang mendefinisikan endpoint konten dan semantik `deleted_at` yang dirujuk di [Rencanakan retensi konten](#plan-content-retention).

## Pilih pola konsumsi feed

Activity Feed mendukung dua pola konsumsi: polling jendela periodik yang dibatasi oleh `created_at.gte` dan `created_at.lt`, serta pembacaan inkremental berbasis kursor yang menyimpan kursor dari satu respons dan meneruskannya pada permintaan berikutnya. Keduanya mengembalikan objek `Activity` yang identik; perbedaannya adalah state yang disimpan klien Anda di antara panggilan.

Kedua pola berbagi batasan berikut:

* Aktivitas dapat dikueri dalam 1 menit setelah terjadi dan disimpan selama 6 tahun.
* `limit` maksimum untuk setiap halaman adalah 5.000.
* Nilai kursor adalah string opaque yang tidak boleh Anda parse.
* Permintaan dibatasi hingga 600 per menit per [organisasi induk](/docs/id/manage-claude/compliance-api#how-the-compliance-api-works), dibagi di seluruh kunci, setiap organisasi yang tertaut, dan setiap endpoint `/v1/compliance/*`; lihat [429 Too Many Requests](/docs/id/manage-claude/compliance-errors#429-too-many-requests) untuk header respons dan kontrak percobaan ulang.

| Pola                                  | Pilih ketika                                                                                                                                                                                                                                              |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Polling jendela                       | Pipeline Anda berjalan pada jadwal tetap, Anda lebih memilih worker stateless, dan Anda dapat menoleransi pemutaran ulang atau jendela yang tumpang tindih                                                                                                |
| Pembacaan inkremental berbasis kursor | Anda menginginkan latensi terendah antara terjadinya aktivitas dan pipeline Anda menyerapnya, Anda ingin menghindari pembacaan ulang halaman yang sudah Anda habiskan, dan Anda memiliki tempat yang tahan lama untuk menyimpan kursor di antara eksekusi |

### Polling jendela

Atur `created_at.lt` setidaknya 1 menit di masa lalu sehingga setiap aktivitas dalam jendela sudah dapat dikueri. Gunakan `created_at.gte` untuk batas bawah dan `created_at.lt` untuk batas atas sehingga jendela yang berurutan tersusun tanpa celah atau tumpang tindih; gunakan kembali nilai `lt` dari jendela sebelumnya sebagai `gte` jendela berikutnya.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/activities" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    --data-urlencode "created_at.gte=2026-04-20T07:00:00Z" \
    --data-urlencode "created_at.lt=2026-04-20T08:00:00Z" \
    --data-urlencode "limit=5000"
  ```
</CodeGroup>

Ketika respons memiliki `has_more: true`, jendela tersebut berisi lebih dari satu halaman aktivitas. Lakukan paginasi di dalam jendela dengan meneruskan `last_id` dari respons sebagai `after_id` pada permintaan berikutnya (berhenti ketika `has_more` bernilai `false`), atau pilih jendela waktu yang lebih kecil. Lihat [Paginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results) untuk kontrak lengkapnya.

Bahkan dengan penyusunan yang bersih, aktivitas yang terindeks setelah jendelanya ditutup tidak akan pernah muncul di jendela berikutnya. Lakukan deduplikasi pada `id` aktivitas dan perlebar setiap jendela baru sehingga tumpang tindih dengan jendela sebelumnya selama beberapa menit, atau jalankan proses rekonsiliasi periodik yang mengkueri ulang jendela yang lebih lama.

<Warning>
  Batas `created_at.lt` yang terlalu dekat dengan waktu sekarang akan secara diam-diam dan permanen menghilangkan aktivitas yang terindeks terlambat: setelah `created_at.gte` bergerak melewatinya, tidak ada jendela berikutnya yang dapat memulihkannya. Perlakukan angka 1 menit untuk dapat dikueri sebagai jeda pengindeksan yang terdokumentasi, bukan rekomendasi lunak.
</Warning>

### Pembacaan inkremental berbasis kursor

<CodeGroup>
  ```bash cURL
  first_id="activity_01XyDMpzjS89pFZXqSFUBDr6"  # first_id from a previous response

  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/activities" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    --data-urlencode "limit=5000" \
    --data-urlencode "before_id=$first_id"
  ```
</CodeGroup>

Lakukan paginasi hingga `has_more` bernilai `false`, lalu simpan `first_id` dari respons terakhir dan teruskan tanpa perubahan sebagai `before_id` pada eksekusi berikutnya untuk mengambil aktivitas yang lebih baru dari kursor yang disimpan. Untuk berjalan ke arah sebaliknya untuk backfill, simpan `last_id` dan teruskan sebagai `after_id`. Untuk referensi lengkap kursor-vs-token-halaman dan semantik percobaan ulang, lihat [Paginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results).

Loop **catch-up** produksi mengambil aktivitas yang tercatat sejak polling terakhir Anda dengan menggerakkan iterasi berdasarkan `has_more` dan `first_id`:

```text
cursor = stored_cursor
loop:
  page = GET /v1/compliance/activities?before_id={cursor}&limit=5000
  store(page.data)
  if page.first_id is not null:
    cursor = page.first_id
  if not page.has_more: break
persist(cursor)
```

Kursor tetap bertahan melewati rotasi kunci; lihat [Mengelola dan merotasi kunci](/docs/id/manage-claude/compliance-api-access#manage-and-rotate-keys).

<Warning>
  Setiap halaman berdekatan dengan kursor yang Anda teruskan: loop berjalan maju menuju waktu sekarang, satu halaman pada satu waktu. Jangan memperlakukan satu respons sebagai sudah mengejar ketertinggalan selama `has_more` bernilai `true`. Simpan kursor hanya setelah `has_more` bernilai `false`; halaman yang belum diambil adalah halaman yang lebih baru antara `first_id` respons ini dan waktu sekarang, dan halaman tersebut tetap belum terbaca sampai Anda menyelesaikan loop atau menjalankannya lagi.
</Warning>

## Korelasikan dengan SIEM Anda

Setiap `Activity` membawa field yang dapat Anda gabungkan (join) dengan peristiwa yang sudah ada di SIEM Anda (Splunk, Datadog, Microsoft Sentinel, Cribl, atau sejenisnya):

| Field Compliance API  | Target join                                                   |
| --------------------- | ------------------------------------------------------------- |
| `actor.user_id`       | Pengidentifikasi pengguna stabil dari penyedia identitas Anda |
| `actor.email_address` | Email direktori ketika ID stabil tidak tersedia               |
| `actor.ip_address`    | Log jaringan, VPN, dan endpoint                               |
| `created_at`          | Korelasi jendela waktu di seluruh sumber mana pun             |

`actor.user_id` dan `actor.email_address` tersedia ketika `actor.type` adalah `user_actor`; periksa diskriminator sebelum membacanya. `user_id` adalah pengidentifikasi stabil dan opaque untuk akun pengguna: nilainya konsisten di seluruh endpoint Compliance API dan payload aktivitas, dan tidak berubah ketika email atau nama tampilan pengguna berubah. Gunakan `user_id`, bukan `email_address`, sebagai kunci join utama.

Panggilan ke Compliance API itu sendiri menghasilkan aktivitas `compliance_api_accessed`. Serap aktivitas ini bersama dengan tipe aktivitas lainnya sehingga SIEM Anda mencatat siapa yang mengkueri data kepatuhan, dan kapan. Teruskan `activity_types[]=compliance_api_accessed` untuk membatasi cakupan kueri, lalu di klien Anda, baca `actor.api_key_id` dari setiap aktivitas yang `actor.type`-nya adalah `api_actor` untuk mengatribusikan akses ke Compliance Access Key atau kunci Admin API tertentu.

## Rencanakan retensi konten

Tiga horizon retensi mengatur apa yang dapat Anda ambil nanti:

| Data                                              | Disimpan selama                                            | Dikendalikan oleh           |
| ------------------------------------------------- | ---------------------------------------------------------- | --------------------------- |
| Catatan Activity Feed                             | 6 tahun                                                    | Anthropic                   |
| Konten obrolan, file, dan proyek                  | Kebijakan retensi claude.ai organisasi Anda                | Organisasi Anda             |
| Konten yang di-hard-delete melalui Compliance API | Tidak disimpan; penghapusan bersifat langsung dan permanen | Pemanggil endpoint `DELETE` |

Untuk bagaimana bagian lain dari Claude Platform menangani retensi, lihat [Retensi API dan data](/docs/id/manage-claude/api-and-data-retention).

Putuskan antara ekspor-dan-arsip dan pengambilan API sesuai permintaan sebagai berikut:

* Jika horizon legal-hold atau audit Anda melebihi 6 tahun untuk metadata aktivitas, ekspor halaman Activity Feed ke arsip Anda sendiri saat Anda menyerapnya.
* Jika kebijakan retensi konten Anda lebih pendek dari horizon eDiscovery Anda, ekspor konten obrolan dan file sebelum jendela retensi berakhir; Compliance API tidak dapat mengembalikan konten yang sudah dihapus oleh retensi.
* Jika suatu alur kerja mungkin mengeluarkan hard-delete Compliance API (misalnya, penegakan DLP), ambil dan arsipkan konten target terlebih dahulu. Tidak ada jendela pemulihan setelah hard-delete; soft-delete dari claude.ai tetap dapat diambil dengan `deleted_at` terisi, tetapi penghapusan Compliance API tidak.

Dalam setiap kasus lainnya, andalkan pengambilan API langsung dan hindari memelihara salinan paralel.

### Jaminan pengiriman dan kelengkapan

Perlakukan Activity Feed sebagai **at-least-once**: traversal yang dipaginasi dengan benar mengembalikan setiap aktivitas setidaknya satu kali, tetapi percobaan ulang setelah kegagalan parsial dapat mengirimkan kembali aktivitas yang sudah Anda simpan. Lakukan deduplikasi pada field `id` aktivitas.

Endpoint list tidak mengembalikan field `total_count` atau checksum. Untuk membuktikan bahwa eksekusi ekspor telah lengkap, catat:

* Kursor awal dan `last_id` terminal.
* Jumlah record yang diekspor.
* Timestamp eksekusi dan `request-id` dari halaman terakhir.

Endpoint konten (obrolan, file, proyek, dan lampiran proyek) hanya menyajikan data claude.ai; Activity Feed menampilkan peristiwa administratif dan sumber daya di seluruh organisasi. Compliance API tidak mencakup:

* Teks prompt atau respons model dari beban kerja Claude Console atau Claude API.
* Konten yang dihapus oleh kebijakan retensi organisasi Anda.
* Konten yang di-hard-delete melalui Compliance API.

Lihat [FAQ Compliance API](/docs/id/manage-claude/compliance-faq#data-coverage-and-retention) untuk informasi lebih lanjut tentang apa yang dicakup dan tidak dicakup oleh Compliance API.

Untuk chain of custody (rantai penjagaan), simpan record yang diekspor dengan metadata asal-usul: endpoint sumber, parameter kueri, timestamp eksekusi, dan hash konten dari setiap record.

## Langkah berikutnya

<CardGroup cols={2}>
  <Card title="Mengkueri Activity Feed" href="/docs/id/manage-claude/compliance-activity-feed">
    Parameter filter, paginasi, dan skema objek `Activity`.
  </Card>

  <Card title="Mengambil dan menghapus obrolan, file, dan proyek" href="/docs/id/manage-claude/compliance-content-data">
    Endpoint konten dan hard-delete.
  </Card>
</CardGroup>
