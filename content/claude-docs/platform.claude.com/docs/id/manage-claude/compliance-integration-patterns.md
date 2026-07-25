---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns
fetched_at: 2026-07-25T03:07:29.726338Z
sha256: 9799be7128e6d6e549db564595385305615b08e8b67a0aab0fb99999bc2e7704
---

# Rancang integrasi kepatuhan Anda

Pilih antara konsumsi Activity Feed berbasis polling dan berbasis kursor, korelasikan peristiwa Compliance API dengan SIEM Anda, dan rencanakan retensi.

---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_activities` pada Compliance Access Key atau kunci Admin API.
</Check>

Integrasi Compliance API untuk produksi membuat tiga pilihan desain: bagaimana ia mengonsumsi Activity Feed, bagaimana outputnya berkorelasi dengan sistem "security information and event management" (manajemen informasi dan peristiwa keamanan), atau SIEM, milik Anda, dan di mana salinan jangka panjang dari aktivitas dan konten disimpan. Pilihan-pilihan ini independen dari endpoint itu sendiri; halaman ini membantu Anda mengevaluasi trade-off-nya.

Halaman ini mengasumsikan Anda telah membaca [Kueri Activity Feed](/docs/id/manage-claude/compliance-activity-feed), yang mendefinisikan parameter dan kontrak paginasi yang dirujuk di seluruh halaman ini, dan [Ambil dan hapus chat, file, dan proyek](/docs/id/manage-claude/compliance-content-data), yang mendefinisikan endpoint konten dan semantik `deleted_at` yang dirujuk di [Rencanakan retensi konten](#plan-content-retention).

## Pilih pola konsumsi feed

Activity Feed mendukung dua pola konsumsi: polling jendela periodik yang dibatasi oleh `created_at.gte` dan `created_at.lt`, dan pembacaan inkremental berbasis kursor yang menyimpan kursor dari satu respons dan meneruskannya pada permintaan berikutnya. Keduanya mengembalikan objek `Activity` yang identik; perbedaannya adalah state yang disimpan klien Anda di antara panggilan.

Kedua pola berbagi batasan berikut:

* Aktivitas dapat dikueri dalam 1 menit setelah terjadi dan disimpan selama 6 tahun.
* `limit` maksimum untuk setiap halaman adalah 5.000.
* Nilai kursor adalah string opaque yang tidak boleh Anda parse.
* Permintaan dibatasi hingga 600 per menit per [organisasi induk](/docs/id/manage-claude/compliance-api#how-the-compliance-api-works), dibagi di antara setiap kunci, setiap organisasi yang tertaut, dan setiap endpoint `/v1/compliance/*`; lihat [429 Too Many Requests](/docs/id/manage-claude/compliance-errors#429-too-many-requests) untuk header respons dan kontrak percobaan ulang.

| Pola                                  | Pilih ketika                                                                                                                                                                                                                                                   |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Polling jendela                       | Pipeline Anda berjalan pada jadwal tetap, Anda lebih memilih worker stateless, dan Anda dapat menoleransi pemutaran ulang atau jendela yang tumpang tindih                                                                                                     |
| Pembacaan inkremental berbasis kursor | Anda menginginkan latensi terendah antara terjadinya suatu aktivitas dan pipeline Anda mengingesnya, Anda ingin menghindari membaca ulang halaman yang sudah Anda habiskan, dan Anda memiliki tempat yang tahan lama untuk menyimpan kursor di antara eksekusi |

### Polling jendela

Atur `created_at.lt` setidaknya 1 menit di masa lalu sehingga setiap aktivitas dalam jendela tersebut sudah dapat dikueri. Gunakan `created_at.gte` untuk batas bawah dan `created_at.lt` untuk batas atas sehingga jendela yang berurutan tersusun tanpa celah atau tumpang tindih; gunakan kembali nilai `lt` dari jendela sebelumnya sebagai nilai `gte` jendela berikutnya.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/activities" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "created_at.gte=2026-04-20T07:00:00Z" \
  --data-urlencode "created_at.lt=2026-04-20T08:00:00Z" \
  --data-urlencode "limit=5000"
```

Ketika respons memiliki `has_more: true`, jendela tersebut berisi lebih dari satu halaman aktivitas. Lakukan paginasi di dalam jendela dengan meneruskan `last_id` dari respons sebagai `after_id` pada permintaan berikutnya (berhenti ketika `has_more` bernilai `false`), atau pilih jendela waktu yang lebih kecil. Lihat [Paginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results) untuk kontrak lengkapnya.

Bahkan dengan penyusunan yang rapi, aktivitas yang terindeks setelah jendelanya ditutup tidak akan pernah muncul di jendela berikutnya. Lakukan deduplikasi pada `id` aktivitas dan perlebar setiap jendela baru sehingga tumpang tindih dengan jendela sebelumnya selama beberapa menit, atau jalankan proses rekonsiliasi periodik yang mengueri ulang jendela yang lebih lama.

<Warning>
  Batas `created_at.lt` yang terlalu dekat dengan waktu sekarang akan secara diam-diam dan permanen menghilangkan aktivitas yang terindeks terlambat: begitu `created_at.gte` bergerak melewatinya, tidak ada jendela berikutnya yang dapat memulihkannya. Perlakukan angka keterkuerian 1 menit sebagai jeda pengindeksan yang terdokumentasi, bukan rekomendasi longgar.
</Warning>

### Pembacaan inkremental berbasis kursor

```bash cURL
first_id="activity_01XyDMpzjS89pFZXqSFUBDr6"  # first_id from a previous response

curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/activities" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "limit=5000" \
  --data-urlencode "before_id=$first_id"
```

Lakukan paginasi hingga `has_more` bernilai `false`, lalu simpan `first_id` dari respons terakhir dan teruskan tanpa perubahan sebagai `before_id` pada eksekusi berikutnya untuk mengambil aktivitas yang lebih baru dari kursor yang disimpan. Untuk berjalan ke arah sebaliknya untuk backfill, simpan `last_id` dan teruskan sebagai `after_id` sebagai gantinya. Untuk referensi lengkap kursor-vs-token-halaman dan semantik percobaan ulang, lihat [Paginasi hasil](/docs/id/manage-claude/compliance-activity-feed#paginate-results).

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

Kursor tetap berlaku setelah rotasi kunci; lihat [Kelola dan rotasi kunci](/docs/id/manage-claude/compliance-api-access#manage-and-rotate-keys).

<Warning>
  Setiap halaman berdekatan dengan kursor yang Anda teruskan: loop berjalan maju menuju waktu sekarang, satu halaman pada satu waktu. Jangan menganggap satu respons sebagai sudah terkejar selama `has_more` bernilai `true`. Simpan kursor hanya setelah `has_more` bernilai `false`; halaman yang belum diambil adalah halaman yang lebih baru antara `first_id` dari respons ini dan waktu sekarang, dan halaman tersebut tetap tidak terbaca sampai Anda menyelesaikan loop atau menjalankannya lagi.
</Warning>

## Korelasikan dengan SIEM Anda

Setiap `Activity` membawa field yang dapat Anda gabungkan dengan peristiwa yang sudah ada di SIEM Anda (Splunk, Datadog, Microsoft Sentinel, Cribl, atau sejenisnya):

| Field Compliance API  | Target penggabungan                                                |
| --------------------- | ------------------------------------------------------------------ |
| `actor.user_id`       | Pengidentifikasi pengguna yang stabil dari penyedia identitas Anda |
| `actor.email_address` | Email direktori ketika ID yang stabil tidak tersedia               |
| `actor.ip_address`    | Log jaringan, VPN, dan endpoint                                    |
| `created_at`          | Korelasi jendela waktu di semua sumber                             |

`actor.user_id` dan `actor.email_address` tersedia ketika `actor.type` adalah `user_actor`; periksa diskriminator sebelum membacanya. `user_id` adalah pengidentifikasi yang stabil dan opaque untuk akun pengguna: nilainya konsisten di setiap endpoint Compliance API dan payload aktivitas, dan tidak berubah ketika email atau nama tampilan pengguna berubah. Gunakan `user_id`, bukan `email_address`, sebagai kunci penggabungan utama.

Panggilan ke Compliance API itu sendiri menghasilkan aktivitas `compliance_api_accessed`. Ingest aktivitas ini bersama jenis aktivitas lainnya sehingga SIEM Anda mencatat siapa yang mengueri data kepatuhan, dan kapan. Teruskan `activity_types[]=compliance_api_accessed` untuk membatasi cakupan kueri, lalu di klien Anda, baca `actor.api_key_id` dari setiap aktivitas yang `actor.type`-nya adalah `api_actor` untuk mengatribusikan akses tersebut ke Compliance Access Key atau kunci Admin API tertentu.

## Rencanakan retensi konten

Tiga horizon retensi mengatur apa yang dapat Anda ambil nanti:

| Data                                                | Disimpan selama                                            | Dikendalikan oleh           |
| --------------------------------------------------- | ---------------------------------------------------------- | --------------------------- |
| Catatan Activity Feed                               | 6 tahun                                                    | Anthropic                   |
| Konten chat, file, dan proyek                       | Kebijakan retensi claude.ai organisasi Anda                | Organisasi Anda             |
| Konten yang dihapus permanen melalui Compliance API | Tidak disimpan; penghapusan bersifat langsung dan permanen | Pemanggil endpoint `DELETE` |

Untuk bagaimana bagian lain dari Claude Platform menangani retensi, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

Putuskan antara ekspor-dan-arsip dan pengambilan API sesuai permintaan sebagai berikut:

* Jika horizon legal-hold atau audit Anda melebihi 6 tahun untuk metadata aktivitas, ekspor halaman Activity Feed ke arsip Anda sendiri saat Anda mengingesnya.
* Jika kebijakan retensi konten Anda lebih pendek dari horizon eDiscovery Anda, ekspor konten chat dan file sebelum jendela retensi berakhir; Compliance API tidak dapat mengembalikan konten yang sudah dihapus oleh retensi.
* Jika suatu alur kerja mungkin mengeluarkan hard-delete Compliance API (misalnya, penegakan DLP), ambil dan arsipkan konten target terlebih dahulu. Tidak ada jendela pemulihan setelah hard-delete; soft-delete dari claude.ai tetap dapat diambil dengan `deleted_at` terisi, tetapi penghapusan Compliance API tidak.

Dalam setiap kasus lainnya, andalkan pengambilan API langsung dan hindari memelihara salinan paralel.

### Jaminan pengiriman dan kelengkapan

Perlakukan Activity Feed sebagai **at-least-once**: penelusuran yang dipaginasi dengan benar mengembalikan setiap aktivitas setidaknya sekali, tetapi percobaan ulang setelah kegagalan parsial dapat mengirimkan kembali aktivitas yang sudah Anda simpan. Lakukan deduplikasi pada field `id` aktivitas.

Endpoint list tidak mengembalikan field `total_count` atau checksum. Untuk membuktikan bahwa suatu eksekusi ekspor telah lengkap, catat:

* Kursor awal dan `last_id` terminal.
* Jumlah catatan yang diekspor.
* Timestamp eksekusi dan `request-id` dari halaman terakhir.

Endpoint konten (chat, file, proyek, dan lampiran proyek) hanya melayani data claude.ai; Activity Feed menampilkan peristiwa administratif dan sumber daya di seluruh organisasi. Compliance API tidak mencakup:

* Teks prompt atau respons model dari beban kerja Claude Console atau Claude API.
* Konten yang dihapus oleh kebijakan retensi organisasi Anda.
* Konten yang dihapus permanen melalui Compliance API.

Lihat [FAQ Compliance API](/docs/id/manage-claude/compliance-faq#data-coverage-and-retention) untuk informasi lebih lanjut tentang apa yang dicakup dan tidak dicakup oleh Compliance API.

Untuk chain of custody, simpan catatan yang diekspor dengan metadata provenance: endpoint sumber, parameter kueri, timestamp eksekusi, dan hash konten dari setiap catatan.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Kueri Activity Feed" href="/docs/id/manage-claude/compliance-activity-feed">
    Parameter filter, paginasi, dan skema objek `Activity`.
  </Card>

  <Card title="Ambil dan hapus chat, file, dan proyek" href="/docs/id/manage-claude/compliance-content-data">
    Endpoint konten dan hard-delete.
  </Card>
</CardGroup>
