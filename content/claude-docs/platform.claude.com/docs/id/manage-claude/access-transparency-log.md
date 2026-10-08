---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/access-transparency-log
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: 3910a6cc1945095416f84b88b09e51818fffd8655edbc0d548d26c3ae005bb8d
---

---
title: Memverifikasi event Access Transparency dengan log transparansi
url: https://platform.claude.com/docs/id/manage-claude/access-transparency-log
description: Gunakan checkpoint bertanda tangan dan bukti Merkle dari Compliance API untuk memverifikasi bahwa tidak ada event Access Transparency yang dihapus atau diubah setelah dicatat ke log.
featureMetadata:
  status: beta
---

Pelajari cara memverifikasi secara kriptografis bahwa tidak ada event [Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency) yang dihapus atau diubah setelah dicatat ke log transparansi organisasi Anda.

<Note>
  Log transparansi sedang dalam tahap beta, dan endpoint serta bentuk responsnya dapat berubah selama beta. Fitur ini merupakan bagian dari Access Transparency, yang tersedia bagi pelanggan yang memenuhi syarat atas permintaan dan tidak bersifat swalayan (lihat [Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency)). Anthropic memelihara satu log untuk organisasi Anda setelah Access Transparency diaktifkan. Anda membacanya melalui Compliance API dengan kunci dan scope yang sama dengan yang Anda gunakan untuk [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed).

  Log Anda dibuat ketika event Access Transparency pertama dicatat untuk organisasi Anda setelah pengaktifan. Sebelum itu, setiap endpoint log transparansi mengembalikan `404`.

  Log transparansi disediakan sebagai informasi bagi Anda. Log ini tidak dirancang atau disertifikasi untuk memenuhi persyaratan keamanan, privasi, atau regulasi apa pun. Anda bertanggung jawab untuk menentukan apakah log ini sesuai dengan kewajiban Anda sendiri.
</Note>

## Cara kerja log transparansi

"Transparency log" (log transparansi) adalah teknik untuk membuat suatu catatan bersifat tamper-evident (menunjukkan bukti jika dirusak). Entri hanya pernah ditambahkan di akhir. Setiap kali log bertambah, operatornya menandatangani pernyataan singkat, yang disebut checkpoint, yang mengikat setiap entri sejauh ini melalui hash pohon Merkle. Siapa pun yang menyimpan checkpoint nantinya dapat meminta bukti bahwa log saat ini masih berisi semua yang dicakup checkpoint tersebut, tanpa perubahan dan dalam urutan yang sama. Oleh karena itu, penghapusan atau penulisan ulang sebuah entri tidak dapat luput dari perhatian verifier yang menyimpan checkpoint yang mencakup entri tersebut. Certificate Transparency dan Go module checksum database dibangun di atas teknik yang sama. [C2SP tlog-tiles](https://c2sp.org/tlog-tiles) adalah spesifikasi terbuka untuk menyajikan log semacam itu sebagai checkpoint bertanda tangan ditambah tile statis yang dapat di-cache berisi hash dan entri, sehingga klien dapat mengambil hash dan menghitung setiap bukti sendiri.

Ketika Access Transparency diaktifkan, Anthropic memelihara log transparansi untuk organisasi Anda. Log ini adalah catatan append-only yang ditandatangani secara kriptografis atas event Access Transparency (`anthropic_access` dan `cmek_preserve`). Setiap event semacam itu yang dicatat untuk organisasi Anda setelah log dibuat akan ditambahkan ke dalamnya. Log ini mengikuti format C2SP tlog-tiles, sehingga tooling yang dibangun untuk standar tersebut memahami checkpoint, tile, dan buktinya.

* **Satu log per organisasi.** Log setiap organisasi memiliki string origin tetap: `axt.anthropic.com/<your organization UUID>`. Origin tidak pernah berubah selama organisasi tersebut ada.
* **Setiap event baru menjadi leaf.** Ketika sebuah event Access Transparency memenuhi syarat untuk muncul di Activity Feed Anda, event itu terlebih dahulu ditambahkan ke log Anda sebagai leaf, dan baru setelah itu disajikan di feed. Leaf adalah serialisasi deterministik dari field-field terdokumentasi milik event tersebut. Event di feed Anda membawa `transparency_log_leaf_index`, yaitu posisinya (berbasis nol) di log Anda.
* **Checkpoint mengikat seluruh riwayat.** Log ini adalah pohon Merkle. Setiap kali log bertambah, Anthropic menerbitkan checkpoint bertanda tangan: dokumen teks singkat yang menyatakan origin log, ukurannya saat ini, dan root hash yang mengikat setiap leaf. Setiap checkpoint membawa tepat satu tanda tangan dari kunci penandatanganan log.
* **Dua jenis bukti menyusul.** Bukti inklusi menunjukkan bahwa event tertentu ada pada posisinya di bawah sebuah checkpoint. Bukti konsistensi menunjukkan bahwa checkpoint yang lebih baru merupakan perpanjangan append-only dari checkpoint sebelumnya yang Anda simpan, sehingga tidak ada yang dihapus atau diubah di antara keduanya.
* **Kunci verifikasi disajikan in-band.** [Endpoint kunci verifier](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-the-verifier-keys) mengembalikan kunci publik yang menandatangani checkpoint. Dalam rotasi kunci terencana, kunci baru ditambahkan ke daftar tersebut sebelum mulai menandatangani, dan kunci-kunci sebelumnya tetap tercantum. Dengan demikian, checkpoint yang sudah Anda pegang tetap dapat diverifikasi.

### Apa yang dibuktikan oleh log transparansi

* Field leaf dari event yang Anda pegang (tercantum di [Bagaimana event menjadi leaf](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#how-an-event-becomes-a-leaf)) adalah, byte demi byte, apa yang dicatat Anthropic ke log.
* Log untuk organisasi Anda hanya pernah bertambah. Verifikasi terhadap checkpoint yang Anda pegang akan gagal jika event yang telah dicatat ke log kemudian dihapus atau ditulis ulang di sana. Verifikasi juga gagal jika Anda disajikan riwayat yang berbeda dari yang disajikan kepada Anda sebelumnya.
* Entri baru hanya dapat ditambahkan di akhir. Sebuah event tidak dapat disisipkan ke dalam riwayat yang sudah Anda verifikasi.

### Apa yang tidak dibuktikan atau diubahnya

* Log ini tidak membuktikan bahwa setiap akses telah dicatat, atau bahwa event yang dicatat menggambarkan akses tersebut secara akurat. Log ini hanya membuktikan bahwa apa yang dicatat Anthropic ke log tidak berubah sejak saat itu.
* Log ini tidak mengubah [apa yang dicakup Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency#what-access-transparency-covers) atau kapan event tiba.
* Field yang disajikan di luar leaf, seperti `workspace_uuid` dan field apa pun yang ditambahkan kemudian, tidak dicakup oleh bukti.
* Bukti inklusi berlaku untuk event yang disajikan kepada Anda. Bukti ini sendiri tidak membuktikan bahwa feed mencantumkan setiap leaf yang dimiliki log. [Entry bundle](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-an-entry-bundle) log berisi setiap leaf, sehingga Anda dapat membaca kumpulan lengkap event yang telah dicatat secara langsung saat Anda membutuhkannya.
* Keberadaan `transparency_log_leaf_index` pada sebuah event adalah penunjuk, bukan bukti. Selalu verifikasi inklusi sebelum memperlakukan sebuah event sebagai telah dicatat di log.
* Perlindungan terhadap riwayat yang ditulis ulang berasal dari checkpoint yang Anda simpan. Tanda tangan checkpoint oleh kunci yang tercantum di [Fingerprint kunci yang dipublikasikan](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#published-key-fingerprints) membuktikan bahwa checkpoint tersebut berasal dari log Anthropic. Bukti konsistensi dari checkpoint yang Anda simpan terakhir kali membuktikan bahwa riwayat yang sudah Anda amati hanya bertambah.

## Sebelum Anda memulai

Anda memerlukan:

* Compliance Access Key dengan scope `read:compliance_activities`, kunci dan scope yang sama dengan yang Anda gunakan untuk [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed). Kunci organisasi induk dapat membaca log setiap organisasi anak yang terdaftar dengan menyebutkan organisasi anak tersebut pada setiap permintaan.
* UUID organisasi Anda. Temukan di Claude Console di bawah **Settings > Organization**. Nilainya sama dengan yang disajikan Activity Feed sebagai `organization_uuid`, tetapi ambillah dari Console. Nilai inilah yang menjadikan sebuah checkpoint milik Anda, sehingga nilai ini tidak boleh berasal dari API yang sedang Anda verifikasi. Anda menurunkan origin log Anda darinya sebagai `axt.anthropic.com/<organization UUID>`. Turunkan string ini sendiri. Jangan membacanya dari respons API.
* Tempat penyimpanan yang tahan lama untuk menyimpan checkpoint terakhir yang Anda verifikasi. Checkpoint tersimpan itulah yang mengubah "log konsisten hari ini" menjadi "log telah konsisten sejak Anda mulai memantau."

## Waktu

* **Event:** Event Access Transparency muncul di Activity Feed Anda dalam dua hari kerja sejak akses terjadi. Sebuah event masuk ke log hanya setelah memenuhi syarat untuk disajikan, sehingga log tidak pernah mengungkapkan event lebih awal. Karena log ditulis sebelum feed menyajikan event, sebuah entri dapat sebentar muncul di log sebelum event-nya muncul di feed Anda. Selisih tersebut bukan ketidaksesuaian.
* **Checkpoint:** Checkpoint baru diterbitkan setiap kali log Anda bertambah.
* **Bukti inklusi:** Bukti untuk event yang baru disajikan tersedia setelah checkpoint yang mencakup posisi event tersebut diterbitkan, biasanya sangat segera setelah event muncul. Jika Anda memintanya lebih awal, Anda menerima `404` dan mencoba lagi setelah jeda singkat.
* **Frekuensi verifikasi:** Jalankan verifikasi Anda setidaknya setiap hari. Setiap jam adalah frekuensi yang wajar.
* **Pembatalan pendaftaran:** Jika organisasi Anda berhenti menggunakan Access Transparency, tidak ada yang dihapus. Log Anda tetap dapat dibaca melalui endpoint yang sama. Jika Access Transparency diaktifkan kembali nanti, log yang sama akan berlanjut.

## Retensi dan penghapusan

* **Log transparansi:** Anthropic tidak menghapus entri dari log Anda, dan log tidak memiliki masa kedaluwarsa. Log tetap disimpan jika organisasi Anda berhenti menggunakan Access Transparency dan setelah organisasi Anda dihapus, karena penghapusan entri adalah perubahan yang justru ingin dideteksi oleh log ini. [Entry bundle](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-an-entry-bundle) menyimpan [field leaf](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#how-an-event-becomes-a-leaf) dari setiap event, sehingga field tersebut disimpan selama log disimpan.
* **Activity Feed:** Event Access Transparency di Activity Feed mengikuti retensi feed. Aktivitas disimpan selama 6 tahun. Lihat [Mengkueri Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed).
* **Tidak ada penghapusan oleh Anda:** Endpoint log transparansi bersifat read-only. Tidak ada cara untuk menghapus atau mengubah sebuah entri.

## Endpoint log transparansi

Enam endpoint read-only disajikan di bawah `https://api.anthropic.com/v1/compliance/transparency_log/`:

| Endpoint                                                                                                                      | Mengembalikan                                                            |
| ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| [`GET /checkpoint`](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-the-latest-checkpoint)     | Checkpoint bertanda tangan terbaru                                       |
| [`GET /keys`](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-the-verifier-keys)               | Kumpulan kunci verifier                                                  |
| [`GET /inclusion`](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#fetch-an-inclusion-proof)        | Bukti inklusi untuk satu event                                           |
| [`GET /consistency`](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#fetch-a-consistency-proof)     | Bukti konsistensi dari checkpoint yang Anda pegang ke checkpoint terbaru |
| [`GET /tile/{level}/{index}`](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-a-hash-tile)     | Tile hash Merkle                                                         |
| [`GET /tile/entries/{index}`](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-an-entry-bundle) | Entry bundle berisi byte leaf                                            |

Checkpoint, tile, dan entry bundle mengikuti format wire C2SP tlog-tiles secara persis. Kedua endpoint bukti hanyalah kemudahan: setiap bukti juga dapat dihitung dari tile, sehingga Anda tidak pernah harus memercayai output endpoint bukti. Anda memverifikasi hash yang dikembalikannya terhadap checkpoint bertanda tangan.

### Autentikasi dan scope

Kirim Compliance Access Key Anda di header `x-api-key` beserta header `anthropic-version`, seperti pada setiap permintaan Compliance API (lihat [Pembuatan versi](https://platform.claude.com/docs/id/manage-claude/compliance-api#versioning)). Compliance API harus diaktifkan untuk organisasi Anda.

Tidak ada izin log transparansi tersendiri. Kunci apa pun yang dapat membaca Activity Feed organisasi Anda, baik untuk organisasi Anda maupun induknya, dapat membaca seluruh log Anda, termasuk field event di dalam entry bundle-nya.

Setiap permintaan membaca tepat satu log organisasi:

* Kunci tingkat organisasi membaca log organisasinya sendiri. Parameter query `organization_id` bersifat opsional. Jika ada, parameter ini harus menyebutkan organisasi milik kunci itu sendiri.
* Kunci tingkat organisasi induk harus menyertakan `organization_id`, yang menyebutkan satu organisasi anak.
* `organization_id` menerima ID bertag `org_...` atau UUID organisasi.

`404` berarti tidak ada log yang dapat dibaca oleh kunci ini. Organisasi di luar scope kunci, organisasi yang tidak ada, dan organisasi yang lognya belum dibuat sengaja dibuat tidak dapat dibedakan. Log organisasi yang sejak itu berhenti menggunakan Access Transparency tidak termasuk kasus ini: log tersebut tetap disajikan.

### Error

Error menggunakan envelope error JSON standar Compliance API di setiap endpoint, termasuk endpoint teks dan biner. Lihat [Menangani error Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-errors) untuk envelope dan jenis error bersama.

| Status | Arti pada permukaan ini                                                                                                                                                                   |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `400`  | `organization_id` salah format atau dihilangkan saat menggunakan kunci organisasi induk, Compliance API tidak diaktifkan, parameter query tidak dikenal, atau validasi per-endpoint gagal |
| `401`  | Kunci API tidak ada atau tidak valid                                                                                                                                                      |
| `403`  | Kunci tidak memiliki scope yang diperlukan                                                                                                                                                |
| `404`  | Tidak ada log yang dapat dibaca oleh kunci ini, atau kasus per-endpoint "tidak tercakup" dan "di luar pohon"                                                                              |
| `429`  | Terkena batas laju. Endpoint ini berbagi [batas laju](https://platform.claude.com/docs/id/manage-claude/compliance-api) per-organisasi-induk milik Compliance API. Patuhi `retry-after`   |
| `503`  | Log untuk sementara tidak tersedia. Coba lagi dengan backoff                                                                                                                              |

### Caching

Respons hanya dapat di-cache oleh klien yang meminta. `Cache-Control` selalu menyertakan `private`, dan respons membawa `Vary: x-api-key`. Jangan menempatkan cache bersama di depan endpoint ini. Tile penuh dan entry bundle penuh tidak pernah berubah dan disajikan dengan `Cache-Control: private, max-age=604800, immutable`. Semua yang lain, termasuk checkpoint, bukti, kunci, tile parsial, dan error, disajikan dengan `Cache-Control: private, no-store`.

### Membaca checkpoint terbaru

`GET /v1/compliance/transparency_log/checkpoint`

```bash
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/transparency_log/checkpoint" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01"
```

Responsnya berupa `text/plain`: sebuah [signed note](https://c2sp.org/signed-note) C2SP. Baris-baris body adalah origin, ukuran pohon dalam desimal, dan root hash dalam base64. Setelahnya ada baris kosong, lalu baris tanda tangan, yang diawali dengan em dash (U+2014), menyebutkan origin, dan diakhiri dengan nilai base64. Nilai-nilai di sini hanya ilustrasi:

```text wrap
axt.anthropic.com/25f6429a-3293-49bf-afed-cb312911554b
1207
C6C4HzGRqDNlbu54LWCvpDX0NcB5DRTmLcjM4u5vWUI=

— axt.anthropic.com/25f6429a-3293-49bf-afed-cb312911554b q83vATBFAiEAvL8m…(base64)…
```

* Empat byte pertama dari nilai tanda tangan yang telah didekode adalah `key_hash` kunci penandatangan, yang memberi tahu Anda entri mana di [kumpulan kunci verifier](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-the-verifier-keys) yang digunakan untuk verifikasi. Byte sisanya adalah tanda tangan ECDSA P-256 ASN.1 DER atas SHA-256 dari body note: setiap byte sebelum baris kosong, termasuk newline di akhir body.
* Checkpoint dapat membawa baris tambahan setelah root hash. Abaikan baris yang tidak Anda pahami. Baris-baris tersebut dicakup oleh tanda tangan.
* Abaikan baris tanda tangan yang namanya bukan origin Anda atau yang key hash-nya tidak Anda pegang.
* Jangan pernah meng-cache checkpoint. Checkpoint yang usang menyembunyikan ukuran log saat ini, sehingga event yang baru disajikan tampak tidak tercakup.

### Membaca kunci verifier

`GET /v1/compliance/transparency_log/keys`

```bash
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/transparency_log/keys" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01"
```

```json
{
  "type": "transparency_log_keys",
  "origin": "axt.anthropic.com/25f6429a-3293-49bf-afed-cb312911554b",
  "log_keys": [
    {
      "verifier_key": "axt.anthropic.com/25f6429a-3293-49bf-afed-cb312911554b+<key_hash>+<base64 key>",
      "key_hash": "<8 lowercase hex digits>",
      "fingerprint": "<64 lowercase hex digits>",
      "algorithm": "ecdsa_p256_sha256",
      "public_key": "<base64 DER SubjectPublicKeyInfo>"
    }
  ]
}
```

| Field                     | Tipe   | Deskripsi                                                                                                                                                                                                                                                                                                  |
| ------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                    | string | Selalu `transparency_log_keys`                                                                                                                                                                                                                                                                             |
| `origin`                  | string | Baris origin yang dibawa setiap checkpoint log ini. Bersifat informasional: bandingkan checkpoint dengan origin yang Anda turunkan sendiri, bukan dengan field ini                                                                                                                                         |
| `log_keys`                | array  | Kunci yang menandatangani checkpoint baru di urutan pertama, lalu setiap kunci lain yang disajikan log, dari yang terbaru. Tidak pernah kosong                                                                                                                                                             |
| `log_keys[].verifier_key` | string | Kunci sebagai string note-verifier C2SP, `<origin>+<key_hash>+<base64 key>`, yang diterima oleh tooling tlog-tiles yang mendukung kunci note ECDSA (misalnya, modul Go `github.com/transparency-dev/formats`). Bagian base64 didekode menjadi byte algoritma `0x02` diikuti kunci publik yang dienkode DER |
| `log_keys[].key_hash`     | string | Delapan digit hex huruf kecil. Selektor 4-byte yang mencocokkan kunci ini dengan baris tanda tangan checkpoint. Ini adalah empat byte pertama dari `fingerprint` dan bukan identitas                                                                                                                       |
| `log_keys[].fingerprint`  | string | 64 digit hex huruf kecil: SHA-256 dari DER `SubjectPublicKeyInfo`                                                                                                                                                                                                                                          |
| `log_keys[].algorithm`    | string | Jenis kunci, saat ini `ecdsa_p256_sha256`. Nilai dapat ditambahkan. Lewati kunci yang algoritmanya tidak Anda dukung                                                                                                                                                                                       |
| `log_keys[].public_key`   | string | Kunci publik sebagai base64 DER `SubjectPublicKeyInfo`                                                                                                                                                                                                                                                     |

`key_hash` hanya mencakup byte kunci: nilainya adalah empat byte pertama SHA-256 atas DER `SubjectPublicKeyInfo`, yang merupakan aturan yang digunakan encoding note-verifier ECDSA. Ini bukan key ID yang bergantung pada nama yang didefinisikan format signed-note dasar untuk kunci Ed25519, sehingga nilainya tidak berubah mengikuti origin. Tanda tangan yang valid oleh kunci yang tercantum di [Fingerprint kunci yang dipublikasikan](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#published-key-fingerprints) membuktikan bahwa checkpoint berasal dari layanan log transparansi Anthropic. Baris origin di dalam checkpoint bertanda tangan itulah yang mengikatnya ke organisasi Anda. Itulah sebabnya Anda membandingkan baris tersebut dengan origin yang Anda turunkan sendiri.

Kunci dapat dirotasi:

* Rotasi adalah peralihan. Mulai dari checkpoint tertentu, checkpoint baru ditandatangani oleh kunci baru.
* Dalam rotasi terencana, kunci baru muncul di `log_keys` sebelum menandatangani apa pun, dan kunci-kunci sebelumnya tetap tercantum. Dengan demikian, checkpoint yang Anda simpan sebelum rotasi tetap dapat diverifikasi.
* Verifier dapat mengambil kumpulan kunci pada setiap eksekusi atau menyimpannya secara lokal. Verifier yang menyimpannya secara lokal membaca ulang endpoint ini ketika menemukan tanda tangan yang `key_hash`-nya tidak dipegangnya.

#### Fingerprint kunci yang dipublikasikan

Anthropic memublikasikan fingerprint setiap kunci yang menandatangani checkpoint di sini, di luar API. Ini memungkinkan Anda memeriksa kunci yang Anda simpan secara lokal terhadap sumber yang tidak dapat diubah oleh jalur penyajian. Kunci yang Anda pegang dapat berasal dari respons `GET /keys` sebelumnya atau dari tooling yang mem-pin kunci tersebut.

| Key hash   | Fingerprint SHA-256                                                | Algoritma           | Menandatangani sejak | Status                         |
| ---------- | ------------------------------------------------------------------ | ------------------- | -------------------- | ------------------------------ |
| `1dff5fe4` | `1dff5fe420d49743fe444a04fc17f818eea856699dec2ebbc24df15602c74a58` | `ecdsa_p256_sha256` | 2026-08-17           | Kunci penandatanganan saat ini |

Rotasi terencana diumumkan di halaman ini setidaknya 30 hari sebelum kunci baru menandatangani checkpoint pertamanya. Selama periode pemberitahuan tersebut, kunci baru tercantum di `log_keys` dan di tabel ini beserta tanggal peralihannya. Kunci yang sudah pensiun tetap tercantum beserta tanggal masa layanannya. Kunci yang tidak muncul di tabel ini tidak sah, apa pun yang dikembalikan `GET /keys`. Perlakukan checkpoint yang tidak dapat diverifikasi dengan kunci tercantum mana pun sebagai kegagalan verifikasi, dan laporkan ke perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com).

[`axt-verify`](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#verify-with-axt-verify) membawa kunci saat ini di setiap rilis dan tidak pernah membaca kunci dari API. Setiap rilis membawa tepat satu kunci. Pada tanggal peralihan, Anthropic mulai menandatangani dengan kunci baru dan menerbitkan rilis `axt-verify` yang membawanya. Pada tanggal yang sama, Anthropic menerbitkan ulang checkpoint terbaru setiap organisasi dengan kunci baru, bahkan untuk log yang tidak bertambah. Lakukan upgrade pada tanggal peralihan. Menjalankan rilis lama setelah peralihan akan gagal dengan status keluar `1`, begitu pula menjalankan rilis baru sebelum peralihan. Kedua kegagalan tersebut hilang setelah Anda menjalankan rilis yang sesuai. Verifier yang Anda kelola sendiri memerlukan fingerprint baru, beserta tanggal peralihannya, ditambahkan sebelum tanggal tersebut.

### Mengambil bukti inklusi

`GET /v1/compliance/transparency_log/inclusion?leaf_index={index}`

| Parameter         | Tipe             | Deskripsi                                                                                                                           |
| ----------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `leaf_index`      | integer, wajib   | Posisi event di log: `transparency_log_leaf_index` yang disajikan Activity Feed pada event tersebut. Harus nol atau lebih besar     |
| `organization_id` | string, opsional | Lihat [Autentikasi dan scope](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#authentication-and-scoping) |

```bash
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/transparency_log/inclusion" \
  --data-urlencode "leaf_index=41" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01"
```

```json
{
  "type": "transparency_log_inclusion_proof",
  "leaf_index": 41,
  "hashes": [
    "mUdyOWMp0zXIq0CDMvSYDUSBl9yAvnTZzdm51RwWpUM=",
    "yR6tDHkAhKvdQSLqQATVjXOo4GM3FDyiKF2XCKTtMUI=",
    "..."
  ],
  "checkpoint": "axt.anthropic.com/25f6429a-3293-49bf-afed-cb312911554b\n42\nCsRlS31ITFHrX9GR5XjyPw8n0MkfrB8Yh2UDHl3Lr3E=\n\n— axt.anthropic.com/25f6429a-3293-49bf-afed-cb312911554b q83vATBEAiB0…(base64)…\n"
}
```

| Field        | Tipe             | Deskripsi                                                                                                                     |
| ------------ | ---------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `type`       | string           | Selalu `transparency_log_inclusion_proof`                                                                                     |
| `leaf_index` | integer          | Posisi event di log, dikembalikan dari permintaan                                                                             |
| `hashes`     | array of strings | Hash sibling base64 dari audit path, diurutkan dari leaf ke atas hingga root                                                  |
| `checkpoint` | string           | Checkpoint bertanda tangan terbaru, yaitu checkpoint yang menjadi acuan verifikasi bukti. Checkpoint ini membawa ukuran pohon |

Tidak ada pencarian berdasarkan ID aktivitas. Anda selalu memegang indeksnya, karena indeks tersebut datang bersama event, dan Anda memeriksa bukti terhadap byte event yang Anda ambil dari feed.

`404` berarti checkpoint terbaru yang diterbitkan tidak mencakup posisi yang diberikan:

* Untuk indeks yang Anda baca dari event yang disajikan, kondisi ini bersifat sementara. Checkpoint yang mencakupnya akan segera diterbitkan, jadi coba lagi setelah jeda singkat.
* `404` yang sama menjawab posisi lain yang tidak tercakup, seperti indeks yang tidak pernah disajikan feed. Untuk posisi semacam itu, tidak ada jaminan bahwa checkpoint yang mencakupnya akan pernah diterbitkan. Respons tidak menyebutkan kasus mana yang Anda alami.

`leaf_index` yang tidak ada atau bukan integer non-negatif mengembalikan `400`.

### Mengambil bukti konsistensi

`GET /v1/compliance/transparency_log/consistency?from={size}`

| Parameter         | Tipe             | Deskripsi                                                                                                                           |
| ----------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `from`            | integer, wajib   | Ukuran pohon dari checkpoint sebelumnya yang Anda pegang. Harus minimal 1 dan maksimal ukuran pohon checkpoint terbaru              |
| `organization_id` | string, opsional | Lihat [Autentikasi dan scope](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#authentication-and-scoping) |

```bash
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/transparency_log/consistency" \
  --data-urlencode "from=1180" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --header "anthropic-version: 2023-06-01"
```

```json
{
  "type": "transparency_log_consistency_proof",
  "hashes": [
    "dGw0aPzu2N0pdc4C5ZAvNIbkXF7J6F9ZQLkPpV6v8Vg=",
    "9PSWm1T9RUmhjF6z6YQzB9CW6E2m2n3mK0aVgqf5Qm0=",
    "..."
  ],
  "checkpoint": "axt.anthropic.com/25f6429a-3293-49bf-afed-cb312911554b\n1207\nC6C4HzGRqDNlbu54LWCvpDX0NcB5DRTmLcjM4u5vWUI=\n\n— axt.anthropic.com/25f6429a-3293-49bf-afed-cb312911554b q83vATBFAiEAvL8m…(base64)…\n"
}
```

| Field        | Tipe             | Deskripsi                                                                                                                        |
| ------------ | ---------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `type`       | string           | Selalu `transparency_log_consistency_proof`                                                                                      |
| `hashes`     | array of strings | Hash bukti base64, dalam urutan RFC 9162                                                                                         |
| `checkpoint` | string           | Checkpoint bertanda tangan terbaru, yaitu checkpoint yang menjadi tujuan perpanjangan bukti. Checkpoint ini membawa ukuran pohon |

* Bukti selalu diperpanjang hingga checkpoint terbaru yang diterbitkan. API ini tidak pernah menyajikan checkpoint historis: Anda menyimpan checkpoint yang disajikan kepada Anda.
* `from` yang sama dengan ukuran pohon checkpoint terbaru mengembalikan bukti kosong.
* Checkpoint yang dipegang dengan ukuran pohon 0 tidak memerlukan bukti konsistensi, karena setiap log merupakan perpanjangan dari log kosong. Dalam kasus tersebut, adopsi checkpoint terbaru secara langsung.
* `from` yang kurang dari 1, atau lebih besar dari ukuran pohon checkpoint terbaru, mengembalikan `400`.
* Jika log tidak lagi dapat membuktikan bahwa ia merupakan perpanjangan dari checkpoint yang pernah ditandatanganinya untuk Anda, perlakukan hal itu sebagai kegagalan verifikasi, bukan kesalahan penggunaan.

### Membaca hash tile

`GET /v1/compliance/transparency_log/tile/{level}/{index}`

Mengembalikan `application/octet-stream`: hash SHA-256 32-byte yang digabungkan, sesuai tlog-tiles. Pengalamatan tile mengikuti tlog-tiles secara persis, termasuk tata bahasa path `{level}` dan `{index}`, bentuk indeks `x001/234` untuk pohon besar, dan sufiks tile parsial `.p/{width}`. Hash tile adalah unit yang digunakan klien tlog-tiles untuk menghitung bukti sendiri.

* Tile penuh bersifat immutable dan disajikan dengan `Cache-Control: private, max-age=604800, immutable`.
* Tile parsial digantikan seiring pohon bertambah dan disajikan dengan `Cache-Control: private, no-store`. Setelah sebuah tile penuh, permintaan untuk bentuk parsial sebelumnya dapat mengembalikan `404` meskipun tile penuhnya ada. Beralih dari tile parsial ke tile penuh adalah tugas klien, sebagaimana ditentukan tlog-tiles, dan klien standar sudah melakukannya.
* `level`, `index`, atau lebar tile parsial yang salah format mengembalikan `400`. Posisi tile di luar ukuran pohon saat ini mengembalikan `404`.

### Membaca entry bundle

`GET /v1/compliance/transparency_log/tile/entries/{index}`

Mengembalikan `application/octet-stream`: entri leaf berurutan, masing-masing diawali panjangnya dalam `uint16` big-endian, sesuai tlog-tiles. Entry bundle berisi plaintext event: [byte kanonis](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#how-an-event-becomes-a-leaf) dari setiap event Access Transparency. Itulah sebabnya seluruh permukaan ini memerlukan scope Activity Feed. Pengalamatan, bentuk parsial, caching, dan error identik dengan hash tile.

## Field `transparency_log_leaf_index` pada event Activity Feed

Event `anthropic_access` dan `cmek_preserve` pada `GET /v1/compliance/activities` membawa `transparency_log_leaf_index`, sebuah integer, setiap kali event tersebut memiliki leaf. Jenis aktivitas lain tidak pernah membawanya.

* **Key tersebut tidak ada, bukan `null`, ketika event tidak memiliki leaf.** Verifier yang tangguh memperlakukan key yang tidak ada dan nilai `null` dengan cara yang sama.
* **Sebuah event disajikan tanpa `transparency_log_leaf_index` hanya dalam dua kasus.** Yang pertama adalah saat organisasi Anda tidak terdaftar di Access Transparency, yaitu sebelum pendaftaran atau di antara pembatalan pendaftaran dan pendaftaran ulang. Yang kedua adalah ketika event dicatat sebelum log organisasi Anda dibuat. Untuk organisasi yang terdaftar sebelum log transparansi diperkenalkan, hal ini mencakup riwayat sebelumnya. Setelah log Anda ada dan selama Anda terdaftar, setiap event ditambahkan ke log sebelum feed menyajikannya. Jika suatu gangguan mencegah feed mengetahui indeksnya, feed menunda event tersebut alih-alih menyajikannya tanpa indeks. Event tersebut tidak hilang: event itu sudah ada di log dan muncul di feed, lengkap dengan indeksnya, setelah gangguan diperbaiki. Event tanpa indeks tidak diharapkan jika bertanggal setelah log Anda dibuat dan berada dalam periode saat Anda terdaftar.
* **Indeks yang ada adalah penunjuk, bukan bukti.** Verifikasi inklusi sebelum memperlakukan event sebagai telah dicatat di log. Anomali yang layak dieskalasi adalah indeks yang ada tetapi bukti inklusinya masih tidak dapat diambil lama setelah checkpoint yang mencakupnya seharusnya sudah diterbitkan.
* Indeks ditetapkan ketika event ditambahkan ke log dan bukan salah satu field yang membentuk leaf.

## Bagaimana event menjadi leaf

Entri leaf adalah byte versi skema `0x01` diikuti JSON kanonis dari 11 field. JSON tersebut mengikuti [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) (JSON Canonicalization Scheme), dan field-fieldnya diambil dari event persis seperti yang disajikan Activity Feed:

* `id`, `type`, `created_at`, `accessed_at`, `organization_id`, `organization_uuid`, `workspace_id`, `accessor_department`, dan `reason_code`
* `actor`, dengan `type` dan `email_address` bersarangnya
* `resource_details`, dengan `type`, `id`, dan `parent` bersarangnya

Aturannya:

* Field yang disajikan di luar kumpulan tersebut, seperti `workspace_uuid` dan `transparency_log_leaf_index` itu sendiri, diabaikan.

* Field terdokumentasi yang dihilangkan oleh event yang disajikan masuk ke leaf sebagai `null`. String kosong berbeda dari `null`.

* `actor` dan `resource_details` adalah objek dengan tepat key-key terdokumentasinya ketika event yang disajikan membawanya. Pada versi `0x01`, `actor.email_address` dan `resource_details.parent` selalu `null`. Ketika event yang disajikan menghilangkan salah satu objek ini atau menyajikannya sebagai `null`, seluruh nilainya adalah `null` di leaf, bukan objek berisi field `null`. Banyak event akses tidak membawa `resource_details`.

* Nilai string, termasuk kedua timestamp dan `reason_code`, diambil byte demi byte seperti yang disajikan. Jika Anda menurunkan ulang timestamp dari representasi lain, reproduksi rendering yang disajikan secara persis:

  * RFC 3339 UTC dengan sufiks `Z`.
  * `created_at` tidak memiliki digit pecahan ketika mikrodetiknya nol, dan tepat enam digit jika tidak.
  * `accessed_at` memiliki nol, tiga, enam, atau sembilan digit pecahan, yang terpendek yang mempertahankan nanodetiknya secara persis.

* JSON kanonis berarti key objek diurutkan, tanpa whitespace yang tidak signifikan, dan escaping string minimal. Tidak ada angka yang muncul di mana pun dalam leaf.

* Leaf hash adalah `SHA-256(0x00 || entry)` dari RFC 6962. Node interior di-hash sebagai `SHA-256(0x01 || left || right)`.

* Verifier menolak byte versi yang tidak dikenal, dan leaf `0x01` yang `type`-nya bukan salah satu dari dua jenis Access Transparency. Jenis event baru atau perubahan aturan dirilis dengan byte versi baru. Leaf yang sudah ada tidak pernah di-hash ulang.

Sebagai contoh, event akses ini sebagaimana disajikan Activity Feed:

```json
{
  "id": "activity_01GPXmAhizavrUuoXNn3tzeA",
  "type": "anthropic_access",
  "created_at": "2025-07-08T18:40:00Z",
  "accessed_at": "2025-07-08T18:39:58Z",
  "organization_id": "org_015gtSHLz269eTwgrH8NX5yk",
  "organization_uuid": "25f6429a-3293-49bf-afed-cb312911554b",
  "workspace_id": "wrkspc_01PaGUP2rbg1XDh7Z9W1CEpd",
  "workspace_uuid": "b6ce2143-1083-d4a7-247c-17530f55a076",
  "accessor_department": "Trust & Safety",
  "reason_code": "safety_review",
  "actor": { "type": "anthropic_actor", "email_address": null },
  "resource_details": { "type": "message", "id": "msg_01HXAMPLE12345678" },
  "transparency_log_leaf_index": 17
}
```

menjadi JSON kanonis ini. JSON ini memiliki tepat 11 key terdokumentasi, diurutkan, dalam satu baris. `workspace_uuid` dan `transparency_log_leaf_index` dihilangkan, dan `resource_details.parent`, yang tidak ada di event yang disajikan, masuk sebagai `null`:

```text wrap
{"accessed_at":"2025-07-08T18:39:58Z","accessor_department":"Trust & Safety","actor":{"email_address":null,"type":"anthropic_actor"},"created_at":"2025-07-08T18:40:00Z","id":"activity_01GPXmAhizavrUuoXNn3tzeA","organization_id":"org_015gtSHLz269eTwgrH8NX5yk","organization_uuid":"25f6429a-3293-49bf-afed-cb312911554b","reason_code":"safety_review","resource_details":{"id":"msg_01HXAMPLE12345678","parent":null,"type":"message"},"type":"anthropic_access","workspace_id":"wrkspc_01PaGUP2rbg1XDh7Z9W1CEpd"}
```

Entri leaf adalah byte `0x01` diikuti byte UTF-8 tersebut. Leaf hash-nya, `SHA-256(0x00 || entry)`, adalah `6ro7vTcFq+sYDZiiGvZaFetUIoMSLig3DGDrCKK1HFU=` dalam base64. Gunakan contoh ini sebagai test vector untuk kode kanonikalisasi Anda sendiri.

## Memverifikasi log Anda

Verifikasi berjalan di infrastruktur Anda sendiri. Semua yang dikembalikan API tidak tepercaya sampai terverifikasi terhadap dua hal yang Anda pegang sendiri. Yang pertama adalah origin yang Anda turunkan dari UUID organisasi Anda. Yang kedua adalah checkpoint yang Anda simpan pada eksekusi terakhir. Eksekusi verifikasi lengkap melakukan hal-hal berikut, secara berurutan:

1. Ambil [kumpulan kunci verifier](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-the-verifier-keys). Hitung sendiri fingerprint setiap kunci sebagai SHA-256 dari `public_key` yang telah didekode base64. Simpan hanya kunci yang fingerprint-nya muncul di [Fingerprint kunci yang dipublikasikan](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#published-key-fingerprints), beserta status setiap kunci di sana. Verifikasi checkpoint yang baru diambil hanya dengan kunci yang dicantumkan tabel tersebut sebagai kunci saat ini pada tanggal itu. Terima kunci yang sudah pensiun hanya untuk checkpoint yang Anda simpan sebelum tanggal pensiunnya.
2. Tetapkan checkpoint terbaru. Pada eksekusi pertama, ambil dari [endpoint checkpoint](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-the-latest-checkpoint). Pada setiap eksekusi berikutnya, minta [bukti konsistensi](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#fetch-a-consistency-proof) dari ukuran pohon yang Anda simpan. Respons membawa checkpoint terbaru bersama dengan buktinya.
3. Periksa baris origin checkpoint terlebih dahulu. Bandingkan baris pertamanya, byte demi byte, dengan origin yang Anda turunkan. Tolak checkpoint apa pun yang origin-nya berbeda, sebelum melakukan hal lain.
4. Verifikasi tanda tangan checkpoint. Temukan baris tanda tangan yang dinamai sesuai origin Anda yang empat byte pertama hasil dekodenya sama dengan `key_hash` dari kunci valid saat ini yang Anda simpan. Verifikasi byte sisanya sebagai tanda tangan ECDSA P-256 atas SHA-256 dari body note, menggunakan `public_key` kunci tersebut. Jika tidak ada baris tanda tangan yang cocok dengan kunci semacam itu, atau tanda tangan tidak terverifikasi, tolak checkpoint tersebut.
5. Buktikan sifat append-only. Jika ukuran pohon baru lebih kecil dari yang Anda simpan, gagalkan. Jika sama, root hash harus cocok. Jika lebih besar, verifikasi bukti konsistensi RFC 9162 dari ukuran dan root hash yang Anda simpan ke ukuran dan root hash yang baru.
6. Buktikan setiap event disertakan. Baca setiap event Access Transparency yang disajikan Activity Feed. Untuk setiap event baru, bangun ulang [leaf](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#how-an-event-becomes-a-leaf)-nya, hash, dan ambil [bukti inklusi](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#fetch-an-inclusion-proof)-nya. Telusuri audit path dari leaf hash Anda pada indeks event hingga ke root hash checkpoint. Ketidakcocokan berarti event yang disajikan kepada Anda bukan event yang dicatat log. Respons bukti dapat membawa checkpoint yang berbeda dari yang Anda pegang. Hubungkan checkpoint tersebut ke riwayat Anda dengan bukti konsistensi sebelum Anda memverifikasi apa pun terhadapnya.
7. Periksa ulang apa yang Anda lihat sebelumnya. Setiap kali Anda membaca sebuah event lagi, event itu harus disajikan dengan indeks yang sama dan byte leaf yang sama seperti saat Anda memverifikasinya. Tidak ada event yang boleh kehilangan indeks yang dimilikinya, dan selama Anda terdaftar tidak ada event yang boleh baru muncul tanpa indeks. Event yang disajikan tanpa indeks pada eksekusi pertama Anda adalah riwayat pra-log Anda. Eksekusi yang hanya membaca ulang event terbaru hanya memeriksa ulang event tersebut. Untuk memeriksa ulang event yang lebih lama, verifikasi lagi salinan yang Anda simpan (langkah 8).
8. Simpan checkpoint yang Anda verifikasi dan catatan setiap event yang Anda verifikasi. Keduanya adalah bukti Anda dan titik awal Anda untuk eksekusi berikutnya.

### Memverifikasi dengan axt-verify

[`axt-verify`](https://github.com/anthropics/axt-verify) adalah verifier open-source Anthropic untuk log ini. Ini adalah satu binary Go yang Anda jalankan di infrastruktur Anda sendiri. Setiap rilis memiliki tepat satu kunci penandatanganan log dari [Fingerprint kunci yang dipublikasikan](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#published-key-fingerprints) yang tertanam di dalamnya, sehingga tidak pernah menanyakan kepada API kunci mana yang harus dipercaya. Ketika Anthropic merotasi kunci, Anda melakukan upgrade ke rilis yang membawa kunci baru pada tanggal peralihan. `axt-verify` menurunkan origin Anda dari UUID organisasi yang Anda berikan dengan `--org`, yaitu UUID yang Anda ambil dari Console di [Sebelum Anda memulai](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#before-you-begin). Alat ini menolak checkpoint apa pun yang baris origin-nya berbeda.

Instal dengan Go 1.26 atau yang lebih baru. Alat ini membaca Compliance Access Key Anda dari variabel lingkungan `ANTHROPIC_COMPLIANCE_ACCESS_KEY`, tidak pernah dari flag atau file. Perintah `run` adalah yang perlu dijadwalkan:

```bash
go install github.com/anthropics/axt-verify/cmd/axt-verify@latest

export ANTHROPIC_COMPLIANCE_ACCESS_KEY="<your Compliance Access Key>"
axt-verify --org 25f6429a-3293-49bf-afed-cb312911554b \
  --state /var/lib/axt-verify/25f6429a-3293-49bf-afed-cb312911554b.state \
  run
```

Setiap `run` mengambil checkpoint terbaru dan memverifikasi tanda tangan serta baris origin-nya. Kemudian alat ini membuktikan bahwa log merupakan perpanjangan append-only dari checkpoint yang disimpan eksekusi sebelumnya. Selanjutnya alat ini menelusuri halaman demi halaman event Access Transparency di Activity Feed Anda. Penelusuran dimulai tujuh hari (berdasarkan `created_at`) sebelum event terbaru yang dibaca eksekusi sebelumnya, sehingga event yang tercantum terlambat atau tidak berurutan tetap terambil. Alat ini membangun ulang leaf setiap event, memverifikasi bukti inklusi untuknya, dan membandingkan setiap event yang pernah diverifikasinya dengan apa yang dicatatnya saat itu. Terakhir, alat ini menyimpan checkpoint baru dan progresnya ke file `--state`, yang menjadi titik awal eksekusi berikutnya. Jalankan setidaknya setiap hari. Setiap jam adalah frekuensi yang wajar. Dengan kunci organisasi induk, jalankan satu salinan per organisasi anak, masing-masing dengan `--org` dan file `--state` sendiri. UUID setiap organisasi anak juga berasal dari Claude Console, bukan dari respons Compliance API yang sedang Anda verifikasi. Temukan di halaman **Settings > Organization** organisasi anak atau di daftar organisasi milik organisasi induk Anda di Console. `axt-verify checkpoint` hanya melakukan langkah checkpoint dan append-only. `axt-verify events FILE` memverifikasi event yang sudah Anda pegang, seperti sampel auditor atau ekspor Anda sendiri. Perintah ini membuktikan bahwa setiap event dalam file masih tercatat di log di bawah checkpoint saat ini. Perintah ini tidak membaca feed atau menyentuh file state.

Ada satu batasan yang muncul dari jendela tersebut: `run` hanya membaca ulang event tujuh hari terakhir, sehingga hanya memeriksa ulang event yang baru disajikan (langkah 7), bukan seluruh riwayat Anda. Simpan event yang Anda ekspor (lihat [Menyimpan arsip checkpoint Anda sendiri](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#keep-your-own-checkpoint-archive)). `axt-verify events FILE` membuktikan pada tanggal kapan pun di kemudian hari bahwa salinan tersebut masih tercatat di log, tetapi tidak membaca ulang feed. Untuk mendeteksi event lama yang dihapus dari atau ditulis ulang di feed, ekspor ulang rentang tersebut dari Activity Feed dan bandingkan dengan salinan yang Anda simpan. Anda juga dapat memverifikasi hasil ekspor ulang itu sendiri dengan `axt-verify events FILE`. Tumpang tindih tujuh hari lebih panjang dari waktu pengiriman feed selama dua hari kerja, sehingga event yang datang terlambat tetap masuk ke dalam jendela eksekusi berikutnya. `--overlap` mengubah durasinya jika Anda perlu.

Jika Anda memerlukan implementasi sendiri, ikuti daftar periksa sebelumnya dengan library tlog-tiles yang mendukung kunci note ECDSA.

### Menafsirkan hasil

`axt-verify` mencetak origin Anda, ukuran pohon dan root hash dari checkpoint yang diverifikasinya, ukuran pohon tempat pemeriksaan append-only dimulai, serta jumlah event berdasarkan hasilnya. Berikan `--json` untuk mendapatkan laporan yang sama sebagai satu objek JSON per baris. Setiap event memiliki salah satu dari empat hasil:

* **Verified:** leaf yang dibangun ulang dari event yang disajikan telah dicatat pada indeks event tersebut di log yang ditandatangani.
* **Pending:** indeks event berada di luar checkpoint terbaru yang diterbitkan. Hal ini normal untuk waktu singkat setelah sebuah event muncul. Dalam `run`, `axt-verify` mengingat event tersebut, memverifikasinya pada eksekusi berikutnya setelah ada checkpoint yang mencakupnya, dan menggagalkannya jika hal itu memakan waktu lebih dari 24 jam. `events FILE` tidak memiliki eksekusi berikutnya untuk menyelesaikannya, sehingga ia menunggu hingga satu menit agar checkpoint yang mencakupnya diterbitkan. Jika tidak ada yang tiba, ia melaporkan event tersebut sebagai belum tercakup dan berakhir dengan status keluar `3`. Jalankan lagi nanti. Jika `events FILE` melaporkan event yang sama sebagai belum tercakup pada dua eksekusi yang berjarak setidaknya satu hari, perlakukan hal itu sebagai kegagalan verifikasi dan lakukan eskalasi seperti untuk status keluar `1`.
* **Not logged:** event disajikan tanpa indeks. Sebuah event disajikan tanpa `transparency_log_leaf_index` hanya selama organisasi Anda tidak terdaftar di Access Transparency, atau ketika event tersebut dicatat sebelum log organisasi Anda dibuat (lihat [Field `transparency_log_leaf_index` pada event Activity Feed](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#the-transparency-log-leaf-index-field-on-activity-feed-events)). `axt-verify` melaporkan event semacam itu sebagai not logged dan tidak menggagalkan eksekusi karenanya. Event tanpa indeks tidak diharapkan jika bertanggal setelah log Anda dibuat dan berada dalam periode ketika Anda terdaftar. Tinjau daftar not-logged dalam ringkasan eksekusi atau output `--json` alih-alih hanya mengandalkan status keluar.
* **Failed:** lihat status keluar `1`.

Status keluar memberi tahu penjadwal Anda apa yang terjadi:

* **`0`:** Tidak ada yang gagal. Event not-logged dilaporkan, bukan digagalkan, begitu pula event pending dalam `run`.

* **`1`:** Kegagalan verifikasi. Ini adalah temuan keamanan, bukan kesalahan sementara. Simpan file state dan output-nya, lalu laporkan kepada perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com). Penyebabnya adalah:

  * Checkpoint dengan origin yang salah, atau tanda tangan yang tidak terverifikasi dengan kunci yang tertanam dalam rilis `axt-verify` Anda. Bandingkan `key_hash` pada baris tanda tangan checkpoint yang gagal dengan [Fingerprint kunci yang dipublikasikan](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#published-key-fingerprints). Kunci yang tercantum di sana dengan tanggal peralihan yang belum Anda tingkatkan berarti Anda memerlukan rilis yang sesuai. Kunci yang tidak tercantum di sana adalah temuan keamanan, apa pun rilis yang Anda jalankan. Pada kegagalan ini `axt-verify` mencetak key hash dari setiap tanda tangan pada checkpoint yang disajikan dan key hash dari kunci yang dipercayainya, masing-masing sebagai delapan digit heksadesimal. Output tersebut sudah cukup untuk melakukan perbandingan.
  * Checkpoint yang bukan signed note yang terbentuk dengan baik, misalnya checkpoint yang root hash-nya tidak berukuran 32 byte.
  * Log yang menyusut, atau yang tidak dapat membuktikan bahwa ia memperluas checkpoint yang Anda simpan. Output kemudian memuat kedua checkpoint dan buktinya, sehingga bukti tersebut dapat berdiri sendiri.
  * Dua checkpoint yang ditandatangani untuk ukuran pohon yang sama dengan root hash yang berbeda. Output memuat kedua checkpoint tersebut.
  * File checkpoint yang diberikan dengan `--from` yang tanda tangannya tidak terverifikasi dengan kunci yang tertanam dalam rilis `axt-verify` Anda, atau file `--from` atau `--from-trusted` yang origin-nya bukan milik Anda. Untuk arsip yang ditandatangani sebelum rotasi kunci, lihat [Menyimpan arsip checkpoint Anda sendiri](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#keep-your-own-checkpoint-archive).
  * Bukti inklusi yang tidak mereproduksi root hash yang ditandatangani untuk event yang disajikan kepada Anda.
  * Event di dalam jendela eksekusi yang disajikan secara berbeda dari cara eksekusi sebelumnya mencatatnya: byte leaf yang berbeda, indeks yang berbeda, atau tanpa indeks padahal sebelumnya memilikinya.
  * Event yang masih pending 24 jam setelah eksekusi pertama kali melihatnya.
  * Bukti inklusi yang ditolak (`400`, `401`, atau `403`) untuk event yang disajikan feed kepada Anda.
  * Bukti inklusi yang dikembalikan untuk `leaf_index` yang berbeda dari yang diminta.
  * Dalam `events FILE`, event pada indeks yang sudah dicakup oleh checkpoint terbaru ketika pemeriksaan dimulai, yang tidak disajikan bukti inklusinya sebelum waktu tunggu habis.
  * Event yang `organization_uuid`-nya bukan UUID organisasi yang Anda berikan dengan `--org`. Ketika organisasi induk menjalankan `events FILE` pada ekspor yang mencakup beberapa organisasi anak, setiap event organisasi lain akan gagal dengan cara ini, jadi pisahkan ekspor berdasarkan organisasi terlebih dahulu dan verifikasi setiap bagian dengan `--org`-nya sendiri.
  * `id` aktivitas yang sama pada dua indeks berbeda, atau dua kali pada satu indeks dengan konten berbeda, dalam satu eksekusi atau satu input `events FILE`.
  * Event yang leaf-nya tidak dapat dibangun ulang: misalnya, field terdokumentasi yang bukan string, nama field yang muncul dua kali, atau `type` yang hilang atau merupakan varian tidak dikenal dari tipe Access Transparency. `events FILE` melewati baris dengan tipe aktivitas lain dan tidak menggagalkannya.

* **`2`:** Kesalahan penggunaan atau konfigurasi. Penyebabnya adalah:

  * Flag yang hilang atau salah format.
  * Tidak ada `ANTHROPIC_COMPLIANCE_ACCESS_KEY`.
  * Kunci yang ditolak API (`401` atau `403`) sebelum ada checkpoint yang terverifikasi.
  * File state yang tidak dapat dibaca atau milik origin lain.

* **`3`:** Eksekusi tidak dapat diselesaikan. Dalam `run`, apa yang sudah diverifikasi disimpan ke file state. Jalankan lagi. Penyebabnya adalah:

  * Event dalam `events FILE` yang indeksnya tidak dicakup oleh checkpoint yang diterbitkan dalam waktu tunggu. Untuk event semacam itu, hasil **Pending** menjelaskan kapan harus berhenti menjalankan ulang dan melakukan eskalasi.
  * Kesalahan jaringan, pembatasan laju, atau kesalahan server yang bertahan melebihi percobaan ulang.
  * Respons yang tidak terduga.
  * File state atau `--save` yang tidak dapat ditulis.

  Status keluar `3` dengan respons `404` adalah hal yang diharapkan hingga Anthropic mencatat event Access Transparency pertama untuk organisasi Anda, karena setiap endpoint log transparansi mengembalikan `404` hingga event tersebut membuat log. Lakukan eskalasi jika endpoint log transparansi masih mengembalikan `404` lebih dari beberapa hari setelah Activity Feed Anda pertama kali menampilkan event Access Transparency, terlepas dari apakah event tersebut memuat `transparency_log_leaf_index` atau tidak. Kombinasi tersebut tidak diharapkan. Setelah sebuah eksekusi berhasil, lakukan eskalasi untuk status keluar `3` yang terus berlanjut.

### Menyimpan arsip checkpoint Anda sendiri

Bukti terkuat yang dapat Anda miliki adalah catatan Anda sendiri tentang apa yang dinyatakan log pada hari tertentu. `axt-verify --save FILE` menulis checkpoint yang diverifikasi oleh sebuah eksekusi, apa adanya, dan `--from FILE` pada eksekusi berikutnya membuat log membuktikan bahwa ia masih memperluas checkpoint tersebut. Arsipkan checkpoint yang disimpan di penyimpanan yang Anda kendalikan, misalnya setiap hari. Berbulan-bulan kemudian, [bukti konsistensi](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#fetch-a-consistency-proof) dari ukuran pohon checkpoint yang diarsipkan tersebut harus tetap mengarah ke checkpoint apa pun yang disajikan log, atau verifikasi akan gagal. Kunci-kunci sebelumnya tetap tercantum dalam [kumpulan kunci verifier](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-the-verifier-keys) setelah rotasi terencana, sehingga checkpoint yang diarsipkan tetap dapat diverifikasi. Dengan `axt-verify`, jika kunci yang menandatangani checkpoint yang diarsipkan telah dirotasi keluar, berikan arsip tersebut dengan `--from-trusted` alih-alih `--from`. Simpan juga event-nya. Event Access Transparency yang Anda ekspor dari feed merupakan input yang valid untuk `axt-verify events FILE`, yang membuktikan pada tanggal kapan pun di kemudian hari bahwa salinan tersebut masih dicatat dalam log di bawah checkpoint terkininya. Karena `events FILE` tidak membaca ulang feed, ekspor yang Anda simpan juga menjadi acuan untuk membandingkan ekspor ulang rentang yang sama di kemudian hari.

## Pertanyaan yang sering diajukan

<AccordionGroup>
  <Accordion title="Apakah saya harus memverifikasi log transparansi?">
    Tidak. Anthropic memelihara log untuk organisasi Anda terlepas dari apakah ada yang memverifikasinya. Verifikasi adalah cara Anda memeriksa log sendiri. Seorang auditor dapat memverifikasi sampel event yang Anda serahkan dengan langkah-langkah yang sama, asalkan memiliki kunci API dengan cakupan Activity Feed.
  </Accordion>

  <Accordion title="Mengapa bukti inklusi mengembalikan 404 untuk event yang baru saja disajikan kepada saya?">
    Event tersebut disajikan beberapa saat sebelum checkpoint yang mencakup posisinya diterbitkan. Checkpoint yang mencakupnya akan segera menyusul, jadi coba lagi setelah jeda singkat. Event yang bukti inklusinya masih tidak tersedia sehari kemudian adalah anomali yang perlu dieskalasi.
  </Accordion>

  <Accordion title="Apa yang terjadi ketika Anthropic merotasi kunci penandatanganan?">
    Rotasi terencana diumumkan di [Fingerprint kunci yang dipublikasikan](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#published-key-fingerprints) setidaknya 30 hari sebelumnya, beserta tanggal peralihan. Pada tanggal peralihan, Anthropic mulai menandatangani dengan kunci baru dan menerbitkan rilis `axt-verify` yang memuatnya. Pada tanggal yang sama, Anthropic menerbitkan ulang checkpoint terbaru setiap organisasi dengan kunci baru, bahkan untuk log yang tidak bertambah. Setiap rilis `axt-verify` memuat satu kunci, jadi lakukan upgrade pada tanggal peralihan. Menjalankan rilis lama setelah peralihan akan gagal dengan status keluar `1`, begitu pula menjalankan rilis baru sebelum peralihan. Kedua kegagalan tersebut akan hilang setelah Anda menjalankan rilis yang sesuai. Checkpoint yang Anda simpan dengan kunci lama tetap menjadi titik awal yang valid, karena bukti append-only dari checkpoint yang disimpan ke checkpoint baru tidak bergantung pada kunci mana yang menandatangani checkpoint lama. Kunci baru muncul di bagian depan [kumpulan kunci verifier](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-the-verifier-keys) dan kunci-kunci sebelumnya tetap tercantum. Oleh karena itu, checkpoint yang sudah Anda verifikasi atau arsipkan tetap dapat diverifikasi terhadap kumpulan tersebut. Verifier milik Anda sendiri yang mem-pin fingerprint yang dipublikasikan perlu menambahkan fingerprint baru, beserta tanggal peralihannya, sebelum tanggal tersebut. Verifier yang menyimpan kumpulan kunci secara lokal akan mengambilnya ulang ketika menemukan tanda tangan yang key hash-nya tidak dimilikinya. Sebuah checkpoint mengikat seluruh riwayat. Setelah satu checkpoint yang ditandatangani dengan kunci baru terverifikasi, dan bukti konsistensi dari checkpoint yang Anda simpan mengarah kepadanya, setiap entri sebelumnya juga ditetapkan ulang.
  </Accordion>

  <Accordion title="Bisakah saya menghitung bukti sendiri alih-alih memanggil endpoint bukti?">
    Ya. Hash tile adalah antarmuka utama, dan klien tlog-tiles yang mendukung kunci note ECDSA dapat menghitung bukti inklusi dan bukti konsistensi darinya. Endpoint bukti hanyalah kemudahan. Klien generik memerlukan wrapper tipis untuk mengirim header `x-api-key` dan, untuk kunci organisasi induk, parameter `organization_id`.
  </Accordion>

  <Accordion title="Bagaimana jika organisasi saya berhenti menggunakan Access Transparency?">
    Tidak ada yang dihapus. Log Anda tetap dapat dibaca dan diverifikasi melalui endpoint yang sama, jadi tetap verifikasi seperti sebelumnya. Jika organisasi Anda mengaktifkan Access Transparency lagi di kemudian hari, log yang sama akan berlanjut, dan bukti konsistensi akan menjangkau celah tersebut.
  </Accordion>

  <Accordion title="Bisakah saya memverifikasi semua organisasi anak saya dengan satu kunci?">
    Ya. Kunci organisasi induk dapat membaca log organisasi anak mana pun yang terdaftar dengan memberikan `organization_id`. Setiap organisasi anak memiliki log, origin, dan checkpoint tersimpannya sendiri. Jalankan satu verifikasi per organisasi anak, masing-masing dengan state-nya sendiri.
  </Accordion>
</AccordionGroup>

## Sumber daya terkait

* [Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency)
* [Mengkueri Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed)
* [Ikhtisar Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api)
* [Menangani error Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-errors)
* [axt-verify](https://github.com/anthropics/axt-verify), verifier open-source Anthropic untuk log transparansi
* [C2SP tlog-tiles](https://c2sp.org/tlog-tiles) dan [C2SP signed note](https://c2sp.org/signed-note), format wire untuk tile, entry bundle, dan checkpoint
* [RFC 9162](https://www.rfc-editor.org/rfc/rfc9162), algoritma Merkle tree, bukti inklusi, dan bukti konsistensi
* [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785), JSON Canonicalization Scheme yang digunakan untuk leaf
