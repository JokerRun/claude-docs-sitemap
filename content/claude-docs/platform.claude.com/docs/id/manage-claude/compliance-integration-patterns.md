---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: be056da12ddbcd76be11e81db645aa030732a8a67828c4fbd9da250b3213b647
---

---
title: Rancang integrasi kepatuhan Anda
url: https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns
description: Pilih antara polling dan konsumsi Activity Feed berbasis kursor, korelasikan event Compliance API dengan SIEM Anda, dan rencanakan retensi.
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

<Check>
  **Scope yang diperlukan:** `read:compliance_activities` pada Compliance Access Key atau kunci Admin API.
</Check>

Integrasi Compliance API produksi membuat tiga pilihan desain: bagaimana integrasi tersebut mengonsumsi Activity Feed, bagaimana outputnya berkorelasi dengan sistem "security information and event management" (manajemen informasi dan event keamanan), atau SIEM, Anda, dan di mana salinan jangka panjang aktivitas dan konten disimpan. Pilihan-pilihan ini tidak bergantung pada endpoint itu sendiri; halaman ini membantu Anda mengevaluasi pertimbangannya.

Halaman ini mengasumsikan Anda telah membaca halaman-halaman berikut:

* [Kueri Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed), yang mendefinisikan parameter dan kontrak paginasi yang dirujuk di seluruh halaman ini.
* [Ambil dan hapus chat, file, dan proyek](https://platform.claude.com/docs/id/manage-claude/compliance-content-data), yang mendefinisikan endpoint chat, file, dan proyek serta semantik `deleted_at` yang dirujuk dalam [Rencanakan retensi konten](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#plan-content-retention).
* [Ambil transkrip sesi](https://platform.claude.com/docs/id/manage-claude/compliance-sessions), yang mendefinisikan endpoint sesi lokal dan remote.

## Pilih pola konsumsi feed

Activity Feed mendukung dua pola konsumsi: "window polling" (polling jendela) periodik yang dibatasi oleh `created_at.gte` dan `created_at.lt`, serta pembacaan inkremental berbasis kursor yang menyimpan kursor dari satu respons dan meneruskannya pada permintaan berikutnya. Keduanya mengembalikan objek `Activity` yang identik; perbedaannya adalah state yang disimpan klien Anda di antara panggilan.

Kedua pola memiliki batasan berikut:

* Aktivitas dapat dikueri dalam waktu 1 menit setelah terjadi dan disimpan selama 6 tahun. Pencatatan tidak bersifat retroaktif: pencatatan dimulai saat Compliance API pertama kali diaktifkan untuk organisasi Anda, dan aktivitas dari sebelum pengaktifan tidak diisi ulang (backfill).
* `limit` maksimum untuk setiap halaman adalah 5.000.
* Nilai kursor adalah string opaque yang tidak boleh Anda parse.
* Permintaan dibatasi hingga 600 per menit per [organisasi induk](https://platform.claude.com/docs/id/manage-claude/compliance-api#how-the-compliance-api-works), dibagi bersama di seluruh kunci, seluruh organisasi tertaut, dan seluruh endpoint `/v1/compliance/*`; tidak seperti endpoint sesi lokal, endpoint sesi remote memiliki anggaran permintaan kedua di atasnya. Lihat [429 Too Many Requests](https://platform.claude.com/docs/id/manage-claude/compliance-errors#429-too-many-requests) untuk header respons dan kontrak retry.

| Pola                                  | Pilih ketika                                                                                                                                                                                                                                              |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Window polling                        | Pipeline Anda berjalan pada jadwal tetap, Anda lebih memilih worker stateless, dan Anda dapat menoleransi pemutaran ulang atau jendela yang tumpang tindih                                                                                                |
| Pembacaan inkremental berbasis kursor | Anda menginginkan latensi terendah antara terjadinya aktivitas dan saat pipeline Anda menyerapnya, Anda ingin menghindari membaca ulang halaman yang sudah Anda kuras, dan Anda memiliki tempat yang tahan lama untuk menyimpan kursor di antara eksekusi |

### Polling jendela

Tetapkan `created_at.lt` setidaknya 1 menit di masa lalu sehingga setiap aktivitas dalam jendela sudah dapat dikueri. Gunakan `created_at.gte` untuk batas bawah dan `created_at.lt` untuk batas atas sehingga jendela yang berurutan tersusun rapat tanpa celah atau tumpang tindih; gunakan kembali nilai `lt` jendela sebelumnya sebagai `gte` jendela berikutnya.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/activities" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "created_at.gte=2026-04-20T07:00:00Z" \
  --data-urlencode "created_at.lt=2026-04-20T08:00:00Z" \
  --data-urlencode "limit=5000"
```

Ketika respons memiliki `has_more: true`, jendela tersebut berisi lebih dari satu halaman aktivitas. Lakukan paginasi di dalam jendela dengan meneruskan `last_id` dari respons sebagai `after_id` pada permintaan berikutnya (berhenti ketika `has_more` bernilai `false`), atau pilih jendela waktu yang lebih kecil. Lihat [Paginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results) untuk kontrak lengkapnya.

Bahkan dengan penyusunan yang rapi, aktivitas yang terindeks setelah jendelanya ditutup tidak akan pernah muncul di jendela berikutnya. Lakukan deduplikasi berdasarkan `id` aktivitas dan perlebar setiap jendela baru sehingga tumpang tindih dengan jendela sebelumnya selama beberapa menit, atau jalankan proses rekonsiliasi periodik yang mengueri ulang jendela yang lebih lama.

<Warning>
  Batas `created_at.lt` yang terlalu dekat dengan waktu sekarang akan secara diam-diam dan permanen menghilangkan aktivitas yang terindeks terlambat: begitu `created_at.gte` maju melewatinya, tidak ada jendela berikutnya yang dapat memulihkannya. Perlakukan angka keterkuerian 1 menit sebagai lag pengindeksan yang terdokumentasi, bukan rekomendasi lunak.
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

Lakukan paginasi hingga `has_more` bernilai `false`, lalu simpan `first_id` dari respons terakhir dan teruskan tanpa perubahan sebagai `before_id` pada eksekusi berikutnya untuk mengambil aktivitas yang lebih baru dari kursor yang disimpan. Untuk berjalan ke arah sebaliknya untuk backfill, simpan `last_id` dan teruskan sebagai `after_id`. Untuk referensi lengkap kursor-vs-page-token dan semantik retry, lihat [Paginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results).

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

Kursor tetap berlaku setelah rotasi kunci; lihat [Kelola dan rotasi kunci](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#manage-and-rotate-keys).

<Warning>
  Setiap halaman bersebelahan dengan kursor yang Anda teruskan: loop berjalan maju menuju waktu sekarang, satu halaman pada satu waktu. Jangan menganggap satu respons sudah mengejar ketertinggalan selama `has_more` bernilai `true`. Simpan kursor hanya setelah `has_more` bernilai `false`; halaman yang belum diambil adalah halaman yang lebih baru antara `first_id` respons ini dan waktu sekarang, dan halaman tersebut tetap belum terbaca hingga Anda menyelesaikan loop atau menjalankannya lagi.
</Warning>

## Korelasikan dengan SIEM Anda

Setiap `Activity` membawa field yang dapat Anda gabungkan dengan event yang sudah ada di SIEM Anda (Splunk, Datadog, Microsoft Sentinel, Cribl, atau sejenisnya):

| Field Compliance API  | Target join                                                                     |
| --------------------- | ------------------------------------------------------------------------------- |
| `actor.user_id`       | Pengidentifikasi pengguna stabil dari penyedia identitas Anda                   |
| `actor.email_address` | Email direktori ketika ID stabil tidak tersedia                                 |
| `actor.ip_address`    | Log jaringan, VPN, dan endpoint                                                 |
| `actor.user_agent`    | Inventaris endpoint dan perangkat, serta aplikasi klien yang membuat permintaan |
| `created_at`          | Korelasi jendela waktu di seluruh sumber apa pun                                |

`actor.user_id` dan `actor.email_address` ada ketika `actor.type` adalah `user_actor`. `actor.ip_address` dan `actor.user_agent` tidak ada pada beberapa tipe aktor, seperti `anthropic_actor` dan `scim_directory_sync_actor`. Periksa diskriminator sebelum membaca field-field ini. `user_id` adalah pengidentifikasi stabil dan opaque untuk akun pengguna: nilainya konsisten di seluruh endpoint Compliance API dan payload aktivitas, dan tidak berubah ketika email atau nama tampilan pengguna berubah. Gunakan `user_id`, bukan `email_address`, sebagai kunci join utama.

Panggilan ke Compliance API itu sendiri menghasilkan aktivitas `compliance_api_accessed`. Serap aktivitas ini bersama tipe aktivitas lainnya sehingga SIEM Anda mencatat siapa yang mengueri data kepatuhan, dan kapan. Teruskan `activity_types[]=compliance_api_accessed` untuk membatasi kueri, lalu di klien Anda, baca `actor.api_key_id` dari setiap aktivitas yang `actor.type`-nya adalah `api_actor` untuk mengatribusikan akses tersebut ke Compliance Access Key atau kunci Admin API tertentu.

## Rencanakan retensi konten

Lima horizon retensi mengatur apa yang dapat Anda ambil nanti:

| Data                                                              | Disimpan selama                                                                                                   | Dikendalikan oleh                                                          |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Catatan Activity Feed                                             | 6 tahun                                                                                                           | Anthropic                                                                  |
| Konten chat, file, dan proyek                                     | Kebijakan retensi claude.ai organisasi Anda                                                                       | Organisasi Anda                                                            |
| Transkrip sesi lokal (sesi di mesin pengguna)                     | 6 tahun secara default, atau periode retensi percakapan kustom organisasi Anda ketika periode terbatas ditetapkan | Anthropic secara default; organisasi Anda ketika menetapkan periode kustom |
| Transkrip sesi remote (sesi di cloud)                             | 6 tahun                                                                                                           | Anthropic                                                                  |
| Konten yang dihapus permanen (hard-delete) melalui Compliance API | Tidak disimpan; penghapusan bersifat langsung dan permanen                                                        | Pemanggil endpoint `DELETE`                                                |

Untuk cara bagian lain Claude Platform menangani retensi, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).

Putuskan antara ekspor-dan-arsip dan pengambilan API sesuai permintaan sebagai berikut:

* Jika horizon legal-hold atau audit Anda melebihi 6 tahun untuk metadata aktivitas atau transkrip sesi, ekspor halaman Activity Feed dan transkrip sesi ke arsip Anda sendiri saat Anda menyerapnya.
* Jika kebijakan retensi konten Anda lebih pendek dari horizon eDiscovery Anda, ekspor konten chat dan file sebelum jendela retensi berakhir; Compliance API tidak dapat mengembalikan konten yang sudah dihapus oleh retensi. Hal yang sama berlaku untuk transkrip sesi lokal, yang mengikuti periode retensi percakapan kustom organisasi Anda ketika periode terbatas ditetapkan, bahkan ketika periode tersebut lebih pendek dari 6 tahun. Endpoint sesi lokal berhenti mengembalikan pesan yang lebih lama dari periode organisasi Anda saat ini segera setelah pengaturan berubah, dan memperpanjang periode di kemudian hari tidak memulihkan transkrip yang sudah kedaluwarsa, jadi ekspor transkrip apa pun yang harus Anda simpan melampaui periode tersebut.
* Jika suatu alur kerja mungkin mengeluarkan hard-delete Compliance API (misalnya, penegakan DLP), ambil dan arsipkan konten target terlebih dahulu. Tidak ada jendela pemulihan setelah hard-delete; soft-delete dari claude.ai tetap dapat diambil dengan `deleted_at` terisi, tetapi penghapusan Compliance API tidak.

Dalam semua kasus lainnya, andalkan pengambilan API langsung dan hindari memelihara salinan paralel.

### Jaminan pengiriman dan kelengkapan

Perlakukan Activity Feed sebagai **at-least-once** (setidaknya sekali): traversal yang dipaginasi dengan benar mengembalikan setiap aktivitas setidaknya sekali, tetapi retry setelah kegagalan parsial dapat mengirim ulang aktivitas yang sudah Anda simpan. Lakukan deduplikasi berdasarkan field `id` aktivitas.

Endpoint list tidak mengembalikan field `total_count` atau checksum. Untuk membuktikan bahwa suatu eksekusi ekspor sudah lengkap, catat:

* Kursor awal dan `last_id` terminal.
* Jumlah catatan yang diekspor.
* Timestamp eksekusi dan `request-id` dari halaman terakhir.

Volume aktivitas bukanlah pemeriksaan kelengkapan. Tipe aktivitas `claude_*_viewed`, seperti `claude_chat_viewed`, mengikuti pola pemuatan masing-masing aplikasi (lihat [Pahami objek Activity](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#understand-the-activity-object)). Periode dengan pesan chat tetapi tanpa aktivitas `claude_chat_viewed` tidak dengan sendirinya menunjukkan data yang hilang. Sebagai gantinya, andalkan traversal dan proses tumpang tindih atau rekonsiliasi yang dijelaskan dalam [Window polling](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#window-polling).

Endpoint konten (chat, file, proyek, lampiran proyek, serta transkrip sesi lokal dan remote) hanya menyajikan data Claude Enterprise. Activity Feed menampilkan event administratif dan sumber daya di seluruh organisasi. Compliance API tidak mencakup:

* Teks prompt atau respons model dari Claude Console, atau dari beban kerja Claude API yang diautentikasi dengan kunci API.
* Aktivitas di perangkat dalam sesi lokal yang tidak pernah dikirim ke Anthropic, seperti file lokal yang tidak dibaca Claude.
* Penggunaan Claude Code yang diautentikasi dengan kunci API Claude Console, dijalankan melalui platform cloud pihak ketiga (Amazon Bedrock, Google Cloud, atau Microsoft Foundry), atau dijalankan di Claude Code di web.
* Sesi lokal dari organisasi dengan [kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-readiness) diaktifkan, dan sesi lokal yang berlaku [zero data retention](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope).
* Blok thinking, serta gambar atau konten biner lainnya, di dalam transkrip sesi (transkrip hanya membawa prompt pengguna, respons asisten, dan aktivitas alat; transkrip sesi lokal menampilkan blok `text` placeholder di tempat konten biner dihilangkan).
* Prompt sistem dari sesi lokal (pesan penanda menggantikannya).
* Definisi alat dan konfigurasi server MCP dalam transkrip sesi (lokal atau remote), serta metadata sitasi pada blok `text` dalam transkrip sesi lokal.
* Konten transkrip untuk sesi lokal di organisasi yang menggunakan [kunci enkripsi yang dikelola pelanggan](https://platform.claude.com/docs/id/manage-claude/cmek) (metadata sesi tetap dicantumkan).
* Konten yang dihapus oleh kebijakan retensi organisasi Anda.
* Konten yang di-hard-delete melalui Compliance API.

Lihat [FAQ Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-faq#data-coverage-and-retention) untuk informasi lebih lanjut tentang apa yang ditangkap dan tidak ditangkap oleh Compliance API.

Untuk chain of custody (rantai pengawasan), simpan catatan yang diekspor dengan metadata provenans: endpoint sumber, parameter kueri, timestamp eksekusi, dan hash konten dari setiap catatan.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Kueri Activity Feed" href="https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed">
    Parameter filter, paginasi, dan skema objek `Activity`.
  </Card>

  <Card title="Ambil dan hapus chat, file, dan proyek" href="https://platform.claude.com/docs/id/manage-claude/compliance-content-data">
    Endpoint chat, file, dan proyek, termasuk hard delete.
  </Card>

  <Card title="Ambil transkrip sesi" href="https://platform.claude.com/docs/id/manage-claude/compliance-sessions">
    Daftar sesi yang dijalankan pengguna Anda di aplikasi dan agen Claude, seperti Cowork dan Claude Code, dan ambil transkripnya.
  </Card>
</CardGroup>
