---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/access-transparency-log
fetched_at: 2026-11-06T02:14:07.030986Z
sha256: e2711c50d9a9a33debb040447160ba8235b16e433ee46ee3dfa31525b901bd9e
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

  Jika Anda sudah menjalankan `axt-verify` secara terjadwal, lihat [Tingkatkan untuk versi leaf baru](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#upgrade-for-a-new-leaf-version).

  Log transparansi disediakan sebagai informasi bagi Anda. Log ini tidak dirancang atau disertifikasi untuk memenuhi persyaratan keamanan, privasi, atau regulasi apa pun. Anda bertanggung jawab untuk menentukan apakah log ini sesuai dengan kewajiban Anda sendiri.
</Note>

## Cara kerja log transparansi

“Transparency log” (log transparansi) adalah teknik untuk membuat suatu catatan bersifat tamper-evident (menunjukkan bukti jika dirusak). Entri hanya pernah ditambahkan di akhir. Setiap kali log bertambah, operatornya menandatangani pernyataan singkat, yang disebut checkpoint, yang mengikat setiap entri sejauh ini melalui hash pohon Merkle. Siapa pun yang menyimpan checkpoint nantinya dapat meminta bukti bahwa log saat ini masih berisi semua yang dicakup checkpoint tersebut, tanpa perubahan dan dalam urutan yang sama. Oleh karena itu, penghapusan atau penulisan ulang sebuah entri tidak dapat luput dari perhatian verifier yang menyimpan checkpoint yang mencakup entri tersebut. Certificate Transparency dan database checksum modul Go dibangun di atas teknik yang sama. [C2SP tlog-tiles](https://c2sp.org/tlog-tiles) adalah spesifikasi terbuka untuk menyajikan log semacam itu sebagai checkpoint bertanda tangan ditambah tile statis yang dapat di-cache berisi hash dan entri, sehingga klien dapat mengambil hash dan menghitung setiap bukti sendiri.

Ketika Access Transparency diaktifkan, Anthropic memelihara log transparansi untuk organisasi Anda. Log ini adalah catatan append-only yang ditandatangani secara kriptografis atas event Access Transparency (`anthropic_access` dan `cmek_preserve`). Setiap event semacam itu yang dicatat untuk organisasi Anda setelah log dibuat akan ditambahkan ke dalamnya. Log ini mengikuti format C2SP tlog-tiles, sehingga tooling yang dibangun untuk standar tersebut dapat mengurai checkpoint, tile, dan buktinya.

* **Satu log untuk setiap organisasi.** Log setiap organisasi memiliki string origin tetap: `axt.anthropic.com/<your organization UUID>`. Origin tidak pernah berubah selama organisasi tersebut ada.
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
* Field yang disajikan yang tidak disertakan oleh [versi leaf](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#how-an-event-becomes-a-leaf) mana pun, seperti `workspace_uuid`, tidak dicakup oleh bukti. Field yang ditambahkan ke event di kemudian hari hanya dicakup setelah suatu versi leaf menyertakannya.
* Bukti inklusi berlaku untuk event yang disajikan kepada Anda. Bukti ini sendiri tidak membuktikan bahwa feed mencantumkan setiap leaf yang dimiliki log. [Bundle entri](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-an-entry-bundle) log berisi setiap leaf, sehingga Anda dapat membaca kumpulan lengkap event yang telah dicatat secara langsung saat Anda membutuhkannya.
* Keberadaan `transparency_log_leaf_index` pada sebuah event adalah penunjuk, bukan bukti. Selalu verifikasi inklusi sebelum memperlakukan sebuah event sebagai telah dicatat di log.
* Perlindungan terhadap riwayat yang ditulis ulang berasal dari checkpoint yang Anda simpan. Tanda tangan checkpoint oleh kunci yang tercantum di [Fingerprint kunci yang dipublikasikan](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#published-key-fingerprints) membuktikan bahwa checkpoint tersebut berasal dari log Anthropic. Bukti konsistensi dari checkpoint yang Anda simpan terakhir kali membuktikan bahwa riwayat yang sudah Anda amati hanya bertambah.

## Sebelum Anda memulai

Anda memerlukan:

* Compliance Access Key dengan scope `read:compliance_activities`, kunci dan scope yang sama dengan yang Anda gunakan untuk [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed). Kunci organisasi induk dapat membaca log setiap organisasi anak yang terdaftar dengan menyebutkan organisasi anak tersebut pada setiap permintaan.
* UUID organisasi Anda. Temukan di halaman [Organisasi](https://platform.claude.com/settings/organization) (`platform.claude.com/settings/organization`) di Claude Console. Nilainya sama dengan yang disajikan Activity Feed sebagai `organization_uuid`, tetapi ambillah dari Console. Nilai inilah yang menjadikan sebuah checkpoint milik Anda, sehingga nilai ini tidak boleh berasal dari API yang sedang Anda verifikasi. Anda menurunkan origin log Anda darinya sebagai `axt.anthropic.com/<organization UUID>`. Turunkan string ini sendiri. Jangan membacanya dari respons API.
* Tempat penyimpanan yang tahan lama untuk menyimpan checkpoint terakhir yang Anda verifikasi. Checkpoint tersimpan itulah yang mengubah “log konsisten hari ini” menjadi “log telah konsisten sejak Anda mulai memantau.”

## Waktu

* **Event:** Event Access Transparency muncul di Activity Feed Anda dalam 2 hari kerja sejak akses terjadi. Suatu event masuk ke log hanya setelah memenuhi syarat untuk disajikan, sehingga log tidak pernah mengungkapkan event lebih awal. Karena log ditulis sebelum feed menyajikan event, suatu entri dapat sebentar muncul di log sebelum event-nya muncul di feed Anda. Selisih tersebut bukanlah ketidaksesuaian.
* **Checkpoint:** Checkpoint baru diterbitkan setiap kali log Anda bertambah.
* **Bukti inklusi:** Bukti untuk event yang baru disajikan tersedia setelah checkpoint yang mencakup posisi event tersebut diterbitkan, biasanya sangat segera setelah event muncul. Jika Anda memintanya lebih awal, Anda menerima `404` dan mencoba lagi setelah jeda singkat.
* **Frekuensi verifikasi:** Jalankan verifikasi Anda setidaknya setiap hari. Setiap jam adalah frekuensi yang wajar.
* **Pembatalan pendaftaran:** Jika organisasi Anda berhenti menggunakan Access Transparency, tidak ada yang dihapus. Log Anda tetap dapat dibaca melalui endpoint yang sama. Jika Access Transparency diaktifkan kembali nanti, log yang sama akan berlanjut.

## Retensi dan penghapusan

* **Log transparansi:** Anthropic tidak menghapus entri dari log Anda, dan log tidak memiliki masa kedaluwarsa. Log tetap disimpan jika organisasi Anda berhenti menggunakan Access Transparency dan setelah organisasi Anda dihapus, karena penghapusan entri adalah perubahan yang justru ingin dideteksi oleh log ini. [Bundle entri](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-an-entry-bundle) menyimpan [field leaf](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#how-an-event-becomes-a-leaf) dari setiap event, sehingga field tersebut disimpan selama log disimpan.
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

Checkpoint, tile, dan bundle entri mengikuti format wire C2SP tlog-tiles secara persis. Kedua endpoint bukti hanyalah kemudahan: setiap bukti juga dapat dihitung dari tile, sehingga Anda tidak pernah harus memercayai output endpoint bukti. Anda memverifikasi hash yang dikembalikannya terhadap checkpoint bertanda tangan.

### Autentikasi dan scope

Kirim Compliance Access Key Anda di header `x-api-key` beserta header `anthropic-version`, seperti pada setiap permintaan Compliance API (lihat [Pembuatan versi](https://platform.claude.com/docs/id/manage-claude/compliance-api#versioning)). Compliance API harus diaktifkan untuk organisasi Anda.

Tidak ada izin log transparansi tersendiri. Kunci apa pun yang dapat membaca Activity Feed organisasi Anda, baik untuk organisasi Anda maupun induknya, dapat membaca seluruh log Anda, termasuk field event di dalam bundle entrinya.

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
| `404`  | Tidak ada log yang dapat dibaca oleh kunci ini, atau kasus per-endpoint “tidak tercakup” dan “di luar pohon”                                                                              |
| `429`  | Terkena batas laju. Endpoint ini berbagi [batas laju](https://platform.claude.com/docs/id/manage-claude/compliance-api) per-organisasi-induk milik Compliance API. Patuhi `retry-after`   |
| `503`  | Log untuk sementara tidak tersedia. Coba lagi dengan backoff                                                                                                                              |

### Caching

Respons hanya dapat di-cache oleh klien yang meminta. `Cache-Control` selalu menyertakan `private`, dan respons membawa `Vary: x-api-key`. Jangan menempatkan cache bersama di depan endpoint ini. Tile penuh dan bundle entri penuh tidak pernah berubah dan disajikan dengan `Cache-Control: private, max-age=604800, immutable`. Semua yang lain, termasuk checkpoint, bukti, kunci, tile parsial, dan error, disajikan dengan `Cache-Control: private, no-store`.

### Membaca checkpoint terbaru

`GET /v1/compliance/transparency_log/checkpoint`

```bash
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/transparency_log/checkpoint" \
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  -H "anthropic-version: 2026-10-21"
```

Responsnya berupa `text/plain`: sebuah [signed note](https://c2sp.org/signed-note) C2SP. Baris-baris body adalah origin, ukuran pohon dalam desimal, dan root hash dalam base64. Setelahnya ada baris kosong, lalu baris tanda tangan, yang diawali dengan tanda pisah (U+2014), menyebutkan origin, dan diakhiri dengan nilai base64. Nilai-nilai di sini hanya ilustrasi:

```text wrap
axt.anthropic.com/25f6429a-3293-49bf-afed-cb312911554b
1207
C6C4HzGRqDNlbu54LWCvpDX0NcB5DRTmLcjM4u5vWUI=

— axt.anthropic.com/25f6429a-3293-49bf-afed-cb312911554b q83vATBFAiEAvL8m…(base64)…
```

* 4 byte pertama dari nilai tanda tangan yang telah didekode adalah `key_hash` kunci penandatanganan, yang memberi tahu Anda entri mana dalam [kumpulan kunci verifier](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-the-verifier-keys) yang digunakan untuk verifikasi. Byte sisanya adalah tanda tangan ECDSA P-256 ASN.1 DER atas SHA-256 dari badan note: setiap byte sebelum baris kosong, termasuk newline di akhir badan.
* Checkpoint dapat membawa baris tambahan setelah root hash. Abaikan baris yang tidak Anda pahami. Baris-baris tersebut dicakup oleh tanda tangan.
* Abaikan baris tanda tangan yang namanya bukan origin Anda atau yang hash kuncinya tidak Anda pegang.
* Jangan pernah meng-cache checkpoint. Checkpoint yang usang menyembunyikan ukuran log saat ini, sehingga event yang baru disajikan tampak tidak tercakup.

### Membaca kunci verifier

`GET /v1/compliance/transparency_log/keys`

```bash
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/transparency_log/keys" \
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  -H "anthropic-version: 2026-10-21"
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
| `log_keys[].key_hash`     | string | Delapan digit heksadesimal huruf kecil. Selektor 4 byte yang mencocokkan kunci ini dengan baris tanda tangan checkpoint. Ini adalah 4 byte pertama dari `fingerprint` dan bukan identitas                                                                                                                  |
| `log_keys[].fingerprint`  | string | 64 digit hex huruf kecil: SHA-256 dari DER `SubjectPublicKeyInfo`                                                                                                                                                                                                                                          |
| `log_keys[].algorithm`    | string | Jenis kunci, saat ini `ecdsa_p256_sha256`. Nilai dapat ditambahkan. Lewati kunci yang algoritmanya tidak Anda dukung                                                                                                                                                                                       |
| `log_keys[].public_key`   | string | Kunci publik sebagai base64 DER `SubjectPublicKeyInfo`                                                                                                                                                                                                                                                     |

`key_hash` hanya mencakup byte kunci: nilainya adalah 4 byte pertama dari SHA-256 atas DER `SubjectPublicKeyInfo`, yang merupakan aturan yang digunakan encoding note-verifier ECDSA. Ini bukan ID kunci yang bergantung pada nama yang didefinisikan format signed-note dasar untuk kunci Ed25519, sehingga tidak berubah mengikuti origin. Tanda tangan yang valid oleh kunci yang tercantum di [Fingerprint kunci yang dipublikasikan](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#published-key-fingerprints) membuktikan bahwa checkpoint berasal dari layanan log transparansi Anthropic. Baris origin di dalam checkpoint bertanda tangan itulah yang mengikatnya ke organisasi Anda. Itulah sebabnya Anda membandingkan baris tersebut dengan origin yang Anda turunkan sendiri.

Kunci dapat dirotasi:

* Rotasi adalah peralihan. Mulai dari checkpoint tertentu, checkpoint baru ditandatangani oleh kunci baru.
* Dalam rotasi terencana, kunci baru muncul di `log_keys` sebelum menandatangani apa pun, dan kunci-kunci sebelumnya tetap tercantum. Dengan demikian, checkpoint yang Anda simpan sebelum rotasi tetap dapat diverifikasi.
* Verifier dapat mengambil kumpulan kunci pada setiap eksekusi atau menyimpannya secara lokal. Verifier yang menyimpannya secara lokal membaca ulang endpoint ini ketika menemukan tanda tangan yang `key_hash`-nya tidak dipegangnya.

#### Fingerprint kunci yang dipublikasikan

Anthropic memublikasikan fingerprint setiap kunci yang menandatangani checkpoint di sini, di luar API. Ini memungkinkan Anda memeriksa kunci yang Anda simpan secara lokal terhadap sumber yang tidak dapat diubah oleh jalur penyajian. Kunci yang Anda pegang mungkin berasal dari respons `GET /keys` sebelumnya atau dari tooling yang mem-pin kunci tersebut.

| Hash kunci | Fingerprint SHA-256                                                | Algoritma           | Menandatangani sejak | Status                         |
| ---------- | ------------------------------------------------------------------ | ------------------- | -------------------- | ------------------------------ |
| `1dff5fe4` | `1dff5fe420d49743fe444a04fc17f818eea856699dec2ebbc24df15602c74a58` | `ecdsa_p256_sha256` | 2026-08-17           | Kunci penandatanganan saat ini |

Rotasi terencana diumumkan di halaman ini setidaknya 30 hari sebelum kunci baru menandatangani checkpoint pertamanya. Selama periode pemberitahuan tersebut, kunci baru tercantum di `log_keys` dan di tabel ini beserta tanggal peralihannya. Kunci yang sudah pensiun tetap tercantum beserta tanggal masa layanannya. Kunci yang tidak muncul di tabel ini tidak sah, apa pun yang dikembalikan `GET /keys`. Perlakukan checkpoint yang tidak dapat diverifikasi dengan kunci tercantum mana pun sebagai kegagalan verifikasi, dan laporkan ke perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com).

`axt-verify` membawa kunci saat ini di setiap rilis dan tidak pernah membaca kunci dari API (lihat [Memverifikasi dengan axt-verify](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#verify-with-axt-verify)). Setiap rilis membawa tepat satu kunci. Pada tanggal peralihan, Anthropic mulai menandatangani dengan kunci baru dan menerbitkan rilis `axt-verify` yang membawanya. Pada tanggal yang sama Anthropic menerbitkan ulang checkpoint terbaru setiap organisasi di bawah kunci baru, bahkan untuk log yang tidak bertambah. Lakukan upgrade pada tanggal peralihan. Menjalankan rilis lama setelah peralihan akan gagal dengan status keluar `1`, begitu pula menjalankan rilis baru sebelumnya. Kedua kegagalan tersebut hilang setelah Anda menjalankan rilis yang sesuai. Verifier yang Anda kelola sendiri memerlukan fingerprint baru, beserta tanggal peralihannya, ditambahkan sebelum tanggal tersebut.

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
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  -H "anthropic-version: 2026-10-21"
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

| Field        | Tipe         | Deskripsi                                                                                                                     |
| ------------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `type`       | string       | Selalu `transparency_log_inclusion_proof`                                                                                     |
| `leaf_index` | integer      | Posisi event di log, dikembalikan dari permintaan                                                                             |
| `hashes`     | array string | Hash sibling base64 dari audit path, diurutkan dari leaf ke atas hingga root                                                  |
| `checkpoint` | string       | Checkpoint bertanda tangan terbaru, yaitu checkpoint yang menjadi acuan verifikasi bukti. Checkpoint ini membawa ukuran pohon |

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
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  -H "anthropic-version: 2026-10-21"
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

| Field        | Tipe         | Deskripsi                                                                                                                        |
| ------------ | ------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `type`       | string       | Selalu `transparency_log_consistency_proof`                                                                                      |
| `hashes`     | array string | Hash bukti base64, dalam urutan RFC 9162                                                                                         |
| `checkpoint` | string       | Checkpoint bertanda tangan terbaru, yaitu checkpoint yang menjadi tujuan perpanjangan bukti. Checkpoint ini membawa ukuran pohon |

* Bukti selalu diperpanjang hingga checkpoint terbaru yang diterbitkan. API ini tidak pernah menyajikan checkpoint historis: Anda menyimpan checkpoint yang disajikan kepada Anda.
* `from` yang sama dengan ukuran pohon checkpoint terbaru mengembalikan bukti kosong.
* Checkpoint yang dipegang dengan ukuran pohon 0 tidak memerlukan bukti konsistensi, karena setiap log merupakan perpanjangan dari log kosong. Dalam kasus tersebut, adopsi checkpoint terbaru secara langsung.
* `from` yang kurang dari 1, atau lebih besar dari ukuran pohon checkpoint terbaru, mengembalikan `400`.
* Jika log tidak lagi dapat membuktikan bahwa ia merupakan perpanjangan dari checkpoint yang pernah ditandatanganinya untuk Anda, perlakukan hal itu sebagai kegagalan verifikasi, bukan kesalahan penggunaan.

### Membaca tile hash

`GET /v1/compliance/transparency_log/tile/{level}/{index}`

Mengembalikan `application/octet-stream`: hash SHA-256 32 byte yang digabungkan, sebagaimana ditentukan tlog-tiles. Pengalamatan tile mengikuti tlog-tiles secara persis, termasuk tata bahasa path `{level}` dan `{index}`, bentuk indeks `x001/234` untuk pohon besar, dan sufiks tile parsial `.p/{width}`. Tile hash adalah unit yang digunakan klien tlog-tiles untuk menghitung bukti sendiri.

* Tile penuh bersifat immutable dan disajikan dengan `Cache-Control: private, max-age=604800, immutable`.
* Tile parsial digantikan seiring pohon bertambah dan disajikan dengan `Cache-Control: private, no-store`. Setelah sebuah tile penuh, permintaan untuk bentuk parsial sebelumnya dapat mengembalikan `404` meskipun tile penuhnya ada. Beralih dari tile parsial ke tile penuh adalah tugas klien, sebagaimana ditentukan tlog-tiles, dan klien standar sudah melakukannya.
* `level`, `index`, atau lebar tile parsial yang salah format mengembalikan `400`. Posisi tile di luar ukuran pohon saat ini mengembalikan `404`.

### Membaca entry bundle

`GET /v1/compliance/transparency_log/tile/entries/{index}`

Mengembalikan `application/octet-stream`: entri leaf berurutan, masing-masing diawali dengan panjang `uint16` big-endian, sebagaimana ditentukan tlog-tiles. Bundle entri berisi plaintext event: [byte kanonis](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#how-an-event-becomes-a-leaf) dari setiap event Access Transparency. Itulah sebabnya seluruh permukaan ini memerlukan scope Activity Feed. Pengalamatan, bentuk parsial, caching, dan error identik dengan tile hash.

## Field `transparency_log_leaf_index` pada event Activity Feed

Event `anthropic_access` dan `cmek_preserve` pada `GET /v1/compliance/activities` membawa `transparency_log_leaf_index`, sebuah integer, setiap kali event tersebut memiliki leaf. Jenis aktivitas lain tidak pernah membawanya.

* **Kunci tersebut tidak ada, bukan `null`, ketika event tidak memiliki leaf.** Verifier yang tangguh memperlakukan kunci yang tidak ada dan nilai `null` dengan cara yang sama.
* **Suatu event disajikan tanpa `transparency_log_leaf_index` hanya dalam dua kasus.** Yang pertama adalah saat organisasi Anda tidak terdaftar di Access Transparency, yaitu sebelum pendaftaran atau di antara pembatalan pendaftaran dan pendaftaran ulang. Yang kedua adalah ketika event dicatat sebelum log organisasi Anda dibuat. Untuk organisasi yang terdaftar sebelum log transparansi diperkenalkan, ini mencakup riwayat sebelumnya. Setelah log Anda ada dan selama Anda terdaftar, setiap event ditambahkan ke log sebelum feed menyajikannya. Jika suatu gangguan mencegah feed memperoleh indeks, feed menunda event alih-alih menyajikannya tanpa indeks. Event tersebut tidak hilang: event itu sudah ada di log dan muncul di feed, lengkap dengan indeksnya, setelah gangguan diperbaiki. Event tanpa indeks tidak diharapkan ketika bertanggal setelah log Anda dibuat dan berada dalam periode saat Anda terdaftar.
* **Indeks yang ada adalah penunjuk, bukan bukti.** Verifikasi inklusi sebelum memperlakukan event sebagai telah dicatat di log. Anomali yang layak dieskalasi adalah indeks yang ada tetapi bukti inklusinya masih tidak dapat diambil lama setelah checkpoint yang mencakupnya seharusnya sudah diterbitkan.
* Indeks ditetapkan ketika event ditambahkan ke log dan bukan salah satu field yang membentuk leaf.

## Bagaimana event menjadi leaf

Entri leaf adalah satu byte versi skema diikuti JSON kanonis dari field versi tersebut. JSON mengikuti [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) (JSON Canonicalization Scheme), dan field diambil dari event persis seperti yang disajikan Activity Feed.

Versi leaf adalah kumpulan field yang tetap, dan setiap field bersifat wajib atau opsional.

Versi `0x01` memiliki 11 field wajib dan tidak memiliki field opsional:

* `id`, `type`, `created_at`, `accessed_at`, `organization_id`, `organization_uuid`, `workspace_id`, `accessor_department`, dan `reason_code`
* `actor`, dengan `type` dan `email_address` bersarangnya
* `resource_details`, dengan `type`, `id`, dan `parent` bersarangnya

Versi `0x02` memiliki 11 field wajib yang sama dan satu field opsional:

* `user_profile_id`, ID dari [profil pengguna](https://platform.claude.com/docs/id/api/beta/user_profiles) tempat data yang diakses atau dipertahankan dibuat

Setelah log Anda mulai menulis suatu versi, log tersebut menulis setiap leaf baru di bawah versi itu hingga mulai menulis versi berikutnya, bahkan ketika event tidak memiliki satu pun field opsional versi tersebut. [Tingkatkan untuk versi leaf baru](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#upgrade-for-a-new-leaf-version) menjelaskan kapan log Anda dapat mulai menulis versi baru. Leaf tidak pernah berubah setelah ditulis, sehingga versinya tetap selamanya. Oleh karena itu, satu log dapat menyimpan leaf dari lebih dari satu versi. Tidak ada yang disajikan Activity Feed atau endpoint bukti yang menyebutkan versi suatu leaf (hanya byte leaf itu sendiri dalam [entry bundle](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-an-entry-bundle) yang menyebutkannya), dan Anda tidak perlu mengetahuinya: aturan terakhir di bawah ini menyebutkan entri mana yang harus dibangun ulang untuk suatu event.

Aturannya:

* Field yang disajikan di luar kumpulan suatu versi, seperti `workspace_uuid` dan `transparency_log_leaf_index` itu sendiri, diabaikan.

* Field wajib yang dihilangkan oleh event yang disajikan, atau disajikan sebagai `null`, masuk ke leaf sebagai `null`. String kosong berbeda dari `null`.

* Field opsional masuk ke leaf hanya ketika event yang disajikan memilikinya sebagai string, termasuk string kosong, dan masuk sebagai string tersebut. Ketika event yang disajikan menghilangkannya atau menyajikannya sebagai `null`, leaf sama sekali tidak memiliki kunci tersebut. Field opsional tidak pernah bernilai `null` di dalam leaf. Tolak event yang disajikan yang memiliki nilai JSON lain untuk field opsional.

* `actor` dan `resource_details` adalah objek dengan tepat kunci-kunci yang terdokumentasi ketika event yang disajikan membawanya. `actor.email_address` dan `resource_details.parent` selalu `null`. Ketika event yang disajikan menghilangkan salah satu objek ini atau menyajikannya sebagai `null`, seluruh nilainya adalah `null` di dalam leaf, bukan objek berisi field `null`. Banyak event akses tidak membawa `resource_details`.

* Nilai string, termasuk kedua timestamp dan `reason_code`, diambil byte demi byte seperti yang disajikan. Jika Anda menurunkan ulang timestamp dari representasi lain, reproduksi rendering yang disajikan secara persis:

  * RFC 3339 UTC dengan sufiks `Z`.
  * `created_at` tidak memiliki digit pecahan ketika mikrodetiknya nol, dan tepat enam digit jika tidak.
  * `accessed_at` memiliki nol, tiga, enam, atau sembilan digit pecahan, yang terpendek yang mempertahankan nanodetiknya secara persis.

* JSON kanonis berarti key objek diurutkan, tanpa spasi yang tidak signifikan, dan escaping string minimal. Tidak ada angka yang muncul di mana pun dalam leaf.

* Hash leaf adalah `SHA-256(0x00 || entry)` dari RFC 6962. Node interior di-hash sebagai `SHA-256(0x01 || left || right)`.

* Verifier yang membaca entri leaf, misalnya dari [entry bundle](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-an-entry-bundle), menolak byte versi yang tidak dikenal, dan leaf yang `type`-nya bukan salah satu dari dua jenis Access Transparency. Field baru, jenis event baru, dan perubahan aturan dirilis di bawah byte versi baru. Leaf yang sudah ada tidak pernah di-hash ulang.

* Bangun ulang entri event yang disajikan di bawah setiap versi leaf yang field-nya mencakup setiap field opsional yang dimiliki event yang disajikan sebagai string (setiap versi, jika tidak memiliki satu pun), dan tidak di bawah versi lain. Event tersebut terverifikasi jika bukti inklusinya cocok dengan hash leaf dari salah satunya. Jika field opsional dihapus dari, ditambahkan ke, atau diubah dalam event yang disajikan kepada Anda, event tersebut gagal diverifikasi pada verifier mana pun yang membangun ulang versi leaf dengan field tersebut, leaf mana pun yang disimpan log.

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

menjadi JSON kanonis ini. JSON ini memiliki tepat 11 kunci wajib, terurut, dalam satu baris. `workspace_uuid` dan `transparency_log_leaf_index` dihilangkan, dan `resource_details.parent`, yang tidak ada dalam event yang disajikan, masuk sebagai `null`:

```json
{"accessed_at":"2025-07-08T18:39:58Z","accessor_department":"Trust & Safety","actor":{"email_address":null,"type":"anthropic_actor"},"created_at":"2025-07-08T18:40:00Z","id":"activity_01GPXmAhizavrUuoXNn3tzeA","organization_id":"org_015gtSHLz269eTwgrH8NX5yk","organization_uuid":"25f6429a-3293-49bf-afed-cb312911554b","reason_code":"safety_review","resource_details":{"id":"msg_01HXAMPLE12345678","parent":null,"type":"message"},"type":"anthropic_access","workspace_id":"wrkspc_01PaGUP2rbg1XDh7Z9W1CEpd"}
```

Event ini tidak memiliki field opsional, sehingga entri versi `0x02` dan versi `0x01`-nya berisi JSON yang sama dan hanya berbeda pada byte pertama. Entri versi `0x02` adalah byte `0x02` diikuti byte UTF-8 tersebut. Hash leaf-nya, `SHA-256(0x00 || entry)`, adalah `1iKC1LbEakcNTfp8OwW4LtItQu4+/K/pzaDDLVIA5XE=` dalam base64. Entri versi `0x01` adalah byte `0x01` diikuti byte yang sama, dengan hash leaf `6ro7vTcFq+sYDZiiGvZaFetUIoMSLig3DGDrCKK1HFU=`.

Event yang sama yang disajikan dengan field opsional, di sini `"user_profile_id": "uprof_01H7Z9W1CEpdPaGUP2rbg1XD"`, memiliki 12 kunci dalam JSON versi `0x02`-nya. Kunci opsional diurutkan bersama kunci lainnya, di antara `type` dan `workspace_id`:

```json
{"accessed_at":"2025-07-08T18:39:58Z","accessor_department":"Trust & Safety","actor":{"email_address":null,"type":"anthropic_actor"},"created_at":"2025-07-08T18:40:00Z","id":"activity_01GPXmAhizavrUuoXNn3tzeA","organization_id":"org_015gtSHLz269eTwgrH8NX5yk","organization_uuid":"25f6429a-3293-49bf-afed-cb312911554b","reason_code":"safety_review","resource_details":{"id":"msg_01HXAMPLE12345678","parent":null,"type":"message"},"type":"anthropic_access","user_profile_id":"uprof_01H7Z9W1CEpdPaGUP2rbg1XD","workspace_id":"wrkspc_01PaGUP2rbg1XDh7Z9W1CEpd"}
```

Entri versi `0x02`-nya, satu-satunya yang perlu dibangun ulang, adalah byte `0x02` diikuti byte UTF-8 tersebut, dengan hash leaf `onAlpkDfdXmHPvbffiTpHAgBacf/mJCzTfNDibDrYp4=`. Gunakan ketiga hash ini sebagai test vector untuk kode kanonikalisasi Anda sendiri.

## Memverifikasi log Anda

Verifikasi berjalan di infrastruktur Anda sendiri. Semua yang dikembalikan API tidak tepercaya sampai terverifikasi terhadap dua hal yang Anda pegang sendiri. Yang pertama adalah origin yang Anda turunkan dari UUID organisasi Anda. Yang kedua adalah checkpoint yang Anda simpan pada eksekusi terakhir. Eksekusi verifikasi lengkap melakukan hal-hal berikut, secara berurutan:

1. Ambil [kumpulan kunci verifier](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-the-verifier-keys). Hitung sendiri fingerprint setiap kunci sebagai SHA-256 dari `public_key` yang telah didekode base64. Simpan hanya kunci yang fingerprint-nya muncul di [Fingerprint kunci yang dipublikasikan](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#published-key-fingerprints), beserta status setiap kunci di sana. Verifikasi checkpoint yang baru diambil hanya dengan kunci yang dicantumkan tabel tersebut sebagai kunci saat ini pada tanggal itu. Terima kunci yang sudah pensiun hanya untuk checkpoint yang Anda simpan sebelum tanggal pensiunnya.
2. Tetapkan checkpoint terbaru. Pada eksekusi pertama, ambil dari [endpoint checkpoint](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-the-latest-checkpoint). Pada setiap eksekusi berikutnya, minta [bukti konsistensi](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#fetch-a-consistency-proof) dari ukuran pohon yang Anda simpan. Respons membawa checkpoint terbaru bersama dengan buktinya.
3. Periksa baris origin checkpoint terlebih dahulu. Bandingkan baris pertamanya, byte demi byte, dengan origin yang Anda turunkan. Tolak checkpoint apa pun yang origin-nya berbeda, sebelum melakukan hal lain.
4. Verifikasi tanda tangan checkpoint. Temukan baris tanda tangan yang dinamai sesuai origin Anda yang empat byte pertama hasil dekodenya sama dengan `key_hash` dari kunci valid saat ini yang Anda simpan. Verifikasi byte sisanya sebagai tanda tangan ECDSA P-256 atas SHA-256 dari body note, menggunakan `public_key` kunci tersebut. Jika tidak ada baris tanda tangan yang cocok dengan kunci semacam itu, atau tanda tangan tidak terverifikasi, tolak checkpoint tersebut.
5. Buktikan sifat append-only. Jika ukuran pohon baru lebih kecil dari yang Anda simpan, gagalkan. Jika sama, root hash harus cocok. Jika lebih besar, verifikasi bukti konsistensi RFC 9162 dari ukuran dan root hash yang Anda simpan ke ukuran dan root hash yang baru.
6. Buktikan setiap event disertakan. Baca setiap event Access Transparency yang disajikan Activity Feed. Untuk setiap event baru, bangun ulang setiap [leaf yang perlu dibangun ulang untuknya](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#how-an-event-becomes-a-leaf), hash masing-masing, dan ambil [bukti inklusinya](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#fetch-an-inclusion-proof). Telusuri audit path dari setiap hash leaf pada indeks event naik ke root hash checkpoint. Event terverifikasi jika salah satunya mereproduksi root hash. Jika tidak ada yang berhasil, event yang disajikan kepada Anda bukanlah event yang dicatat log. Respons bukti dapat membawa checkpoint yang berbeda dari yang Anda pegang. Periksa baris origin dan tanda tangannya (langkah 3 dan 4), dan tautkan ke riwayat Anda dengan bukti konsistensi (langkah 5), sebelum Anda memverifikasi apa pun terhadapnya.
7. Periksa ulang apa yang Anda lihat sebelumnya. Setiap kali Anda membaca sebuah event lagi, event itu harus disajikan dengan indeks yang sama dan byte leaf yang sama seperti saat Anda memverifikasinya. Tidak ada event yang boleh kehilangan indeks yang dimilikinya, dan selama Anda terdaftar tidak ada event yang boleh baru muncul tanpa indeks. Event yang disajikan tanpa indeks pada eksekusi pertama Anda adalah riwayat pra-log Anda. Eksekusi yang hanya membaca ulang event terbaru hanya memeriksa ulang event tersebut. Untuk memeriksa ulang event yang lebih lama, verifikasi lagi salinan yang Anda simpan (langkah 8).
8. Simpan checkpoint yang Anda verifikasi dan catatan setiap event yang Anda verifikasi. Keduanya adalah bukti Anda dan titik awal Anda untuk eksekusi berikutnya.

### Tingkatkan untuk versi leaf baru

Setiap rilis `axt-verify` hanya membangun ulang [versi leaf](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#how-an-event-becomes-a-leaf) yang sudah didefinisikan saat rilis tersebut diterbitkan. Asumsikan bahwa log Anda dapat mulai menulis versi baru kapan saja setelah rilis yang membangunnya ulang diterbitkan. Instal rilis tersebut segera setelah diterbitkan.

| Versi leaf | Rilis `axt-verify` yang membangunnya ulang |
| ---------- | ------------------------------------------ |
| `0x01`     | Setiap rilis                               |
| `0x02`     | `v0.2.0` dan yang lebih baru               |

`axt-verify version` mencetak rilis yang Anda jalankan. Instalasi baru mendapatkan rilis terbaru. Jika baris terakhir tabel tidak mencakup rilis Anda, tingkatkan ke rilis di baris tersebut. Jika belum ada yang diterbitkan, tingkatkan segera setelah ada:

1. Instal rilis terbaru dengan cara yang sama seperti Anda menginstal sebelumnya (baris `go install` di [Memverifikasi dengan axt-verify](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#verify-with-axt-verify)).
2. Tetap jalankan seperti sebelumnya: `--org` yang sama, file `--state` yang sama, jadwal yang sama.

Yang dapat diharapkan:

* **Sebelum log Anda mulai menulis versi baru.** Rilis yang lebih baru memverifikasi log Anda seperti sebelumnya, karena rilis tersebut juga membangun ulang versi leaf yang lebih awal.
* **Setelah log Anda mulai menulis versi baru, pada rilis yang tidak membangunnya ulang.** Rilis tersebut melaporkan setiap event yang leaf-nya memiliki versi tersebut sebagai kegagalan verifikasi, dengan status keluar `1`, bahkan ketika event tersebut tidak memiliki satu pun field opsional dari versi tersebut. Leaf dari versi yang dibangun ulang oleh rilis Anda tidak terpengaruh. Leaf tersebut terverifikasi seperti sebelumnya. Kegagalan tersebut hilang setelah Anda menjalankan rilis yang membangun ulang versi tersebut pada file `--state` yang sama, dan pemeriksaan append-only berlanjut dari titik di mana eksekusi terakhir Anda berakhir.
* **Jika Anda kembali ke rilis yang lebih awal.** Jangan berikan kepada rilis yang lebih awal file state yang telah disimpan oleh rilis yang lebih baru. Rilis yang lebih awal akan melaporkan setiap event yang sedang menunggu checkpoint sebagai kegagalan verifikasi. Jika Anda mungkin perlu kembali ke rilis yang lebih awal, salin file state sebelum eksekusi pertama rilis yang lebih baru, dan berikan salinan tersebut kepada rilis yang lebih awal.

Verifier yang Anda kelola sendiri memerlukan field versi baru, serta aturan tentang entri mana yang harus dibangun ulang, dari [Bagaimana event menjadi leaf](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#how-an-event-becomes-a-leaf) sebelum log Anda mulai menulis versi tersebut.

### Memverifikasi dengan axt-verify

Jika Anda sudah menjalankan `axt-verify` secara terjadwal, baca [Tingkatkan untuk versi leaf baru](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#upgrade-for-a-new-leaf-version) terlebih dahulu.

[`axt-verify`](https://github.com/anthropics/axt-verify) adalah verifier open-source milik Anthropic untuk log ini. Ini adalah satu biner Go yang Anda jalankan di infrastruktur Anda sendiri. Setiap rilis memiliki tepat satu kunci penandatanganan log dari [Fingerprint kunci yang dipublikasikan](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#published-key-fingerprints) yang tertanam di dalamnya, sehingga rilis tersebut tidak pernah menanyakan kepada API kunci mana yang harus dipercaya. Ketika Anthropic merotasi kunci, Anda melakukan upgrade ke rilis yang membawa kunci baru pada tanggal peralihan. `axt-verify` menurunkan origin Anda dari UUID organisasi yang Anda berikan dengan `--org`, yaitu UUID yang Anda ambil dari Console di [Sebelum Anda memulai](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#before-you-begin). Alat ini menolak checkpoint apa pun yang baris origin-nya berbeda.

Instal dengan Go 1.26 atau yang lebih baru. Alat ini membaca Compliance Access Key Anda dari variabel lingkungan `ANTHROPIC_COMPLIANCE_ACCESS_KEY`, tidak pernah dari flag atau file. Perintah `run` adalah yang perlu dijadwalkan:

```bash
go install github.com/anthropics/axt-verify/cmd/axt-verify@latest

export ANTHROPIC_COMPLIANCE_ACCESS_KEY="<your Compliance Access Key>"
axt-verify --org 25f6429a-3293-49bf-afed-cb312911554b \
  --state /var/lib/axt-verify/25f6429a-3293-49bf-afed-cb312911554b.state \
  run
```

Setiap `run` mengambil checkpoint terbaru dan memverifikasi tanda tangan serta baris origin-nya. Kemudian alat ini membuktikan bahwa log merupakan perpanjangan append-only dari checkpoint yang disimpan oleh eksekusi sebelumnya. Selanjutnya alat ini menelusuri halaman demi halaman event Access Transparency di Activity Feed Anda. Alat ini mulai 7 hari (berdasarkan `created_at`) sebelum event terbaru yang dibaca oleh eksekusi sebelumnya, sehingga event yang tercantum terlambat atau tidak berurutan tetap terambil. Alat ini membangun ulang setiap [leaf yang harus dibangun ulang untuk event tersebut](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#how-an-event-becomes-a-leaf), memverifikasi bukti inklusi terhadapnya, dan membandingkan setiap event yang pernah diverifikasinya sebelumnya dengan apa yang dicatatnya saat itu. Terakhir, alat ini menyimpan checkpoint baru dan progresnya ke file `--state`, yang menjadi titik awal eksekusi berikutnya. Jalankan setidaknya setiap hari. Setiap jam adalah pilihan yang wajar. Dengan kunci organisasi induk, jalankan satu salinan untuk setiap organisasi anak, masing-masing dengan `--org` dan file `--state` sendiri. UUID setiap organisasi anak juga berasal dari Claude Console, bukan dari respons Compliance API yang sedang Anda verifikasi. Untuk menemukannya, beralihlah ke organisasi anak di menu akun di bagian bawah sidebar Console, lalu buka halaman [Organisasi](https://platform.claude.com/settings/organization) (`platform.claude.com/settings/organization`). Anda juga dapat menemukannya di daftar organisasi milik organisasi induk Anda di Console. `axt-verify checkpoint` hanya menjalankan langkah checkpoint dan append-only. `axt-verify events FILE` memverifikasi event yang sudah Anda miliki, seperti sampel dari auditor atau ekspor Anda sendiri. Perintah ini membuktikan bahwa setiap event dalam file masih tercatat dalam log di bawah checkpoint saat ini. Perintah ini tidak membaca feed atau menyentuh file state.

Satu batasan muncul dari jendela tersebut: `run` hanya membaca ulang event 7 hari terakhir, sehingga ia memeriksa ulang event yang baru-baru ini disajikan (langkah 7), bukan seluruh riwayat Anda. Simpan event yang Anda ekspor (lihat [Menyimpan arsip checkpoint Anda sendiri](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#keep-your-own-checkpoint-archive)). `axt-verify events FILE` membuktikan kapan pun di kemudian hari bahwa salinan tersebut masih tercatat dalam log, tetapi tidak membaca ulang feed. Untuk mendeteksi event lama yang dihapus dari atau ditulis ulang di feed, ekspor ulang rentang tersebut dari Activity Feed dan bandingkan dengan salinan yang Anda simpan. Anda juga dapat memverifikasi hasil ekspor ulang itu sendiri dengan `axt-verify events FILE`. Tumpang tindih 7 hari lebih panjang daripada waktu pengiriman feed selama 2 hari kerja, sehingga event yang datang terlambat tetap jatuh di dalam jendela eksekusi berikutnya. `--overlap` mengubah durasinya jika Anda membutuhkannya.

Jika Anda memerlukan implementasi sendiri, ikuti daftar periksa sebelumnya dengan library tlog-tiles yang mendukung kunci note ECDSA.

### Menafsirkan hasil

`axt-verify` mencetak origin Anda, ukuran pohon dan root hash dari checkpoint yang diverifikasinya, ukuran pohon tempat pemeriksaan append-only dimulai, dan jumlah event berdasarkan hasilnya. Berikan `--json` untuk mendapatkan laporan yang sama sebagai satu objek JSON di setiap baris. Setiap event memiliki salah satu dari empat hasil:

* **Terverifikasi:** leaf yang dibangun ulang dari event yang disajikan tercatat pada indeks event tersebut di log yang ditandatangani.
* **Tertunda:** indeks event berada di luar checkpoint terbaru yang dipublikasikan. Ini normal untuk waktu singkat setelah event muncul. Pada `run`, `axt-verify` mencatat event tersebut, memverifikasinya pada eksekusi berikutnya setelah ada checkpoint yang mencakupnya, dan menggagalkannya jika hal itu memakan waktu lebih dari 24 jam. `events FILE` tidak memiliki eksekusi berikutnya untuk menyelesaikannya, sehingga perintah ini menunggu hingga satu menit agar checkpoint yang mencakupnya dipublikasikan. Jika tidak ada yang datang, perintah ini melaporkan event tersebut sebagai belum tercakup dan berakhir dengan status keluar `3`. Jalankan lagi nanti. Jika `events FILE` melaporkan event yang sama sebagai belum tercakup pada dua eksekusi yang berjarak setidaknya satu hari, perlakukan sebagai kegagalan verifikasi dan eskalasikan seperti untuk status keluar `1`.
* **Tidak dicatat:** event disajikan tanpa indeks. Sebuah event disajikan tanpa `transparency_log_leaf_index` hanya selama organisasi Anda tidak terdaftar di Access Transparency, atau ketika event tersebut dicatat sebelum log organisasi Anda dibuat (lihat [Field `transparency_log_leaf_index` pada event Activity Feed](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#the-transparency-log-leaf-index-field-on-activity-feed-events)). `axt-verify` melaporkan event semacam itu sebagai tidak dicatat dan tidak menggagalkan eksekusi karenanya. Event tanpa indeks tidak diharapkan jika bertanggal setelah log Anda dibuat dan berada dalam periode ketika Anda terdaftar. Tinjau daftar event yang tidak dicatat dalam ringkasan eksekusi atau output `--json` alih-alih hanya mengandalkan status keluar.
* **Gagal:** lihat status keluar `1`.

Status keluar memberi tahu penjadwal Anda apa yang terjadi:

* **`0`:** Tidak ada yang gagal. Event not-logged dilaporkan, bukan digagalkan, begitu pula event pending dalam `run`.

* **`1`:** Kegagalan verifikasi. Jika setiap event baru gagal karena bukti inklusinya tidak mereproduksi root hash yang ditandatangani, pertama-tama pastikan bahwa Anda tidak menjalankan rilis yang tidak membangun ulang versi leaf terbaru log Anda, seperti yang dijelaskan item terkait dalam daftar ini. Jika itu bukan penyebabnya, dan untuk kegagalan lainnya, perlakukan sebagai temuan keamanan, bukan kesalahan sementara. Simpan file state dan output-nya, lalu laporkan kepada perwakilan akun Anthropic Anda atau [dukungan Anthropic](https://support.claude.com). Penyebabnya adalah:

  * Checkpoint dengan origin yang salah, atau tanda tangan yang tidak terverifikasi dengan kunci yang tertanam dalam rilis `axt-verify` Anda. Bandingkan `key_hash` pada baris tanda tangan checkpoint yang gagal dengan [Fingerprint kunci yang dipublikasikan](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#published-key-fingerprints). Kunci yang tercantum di sana dengan tanggal peralihan yang belum Anda tingkatkan berarti Anda memerlukan rilis yang sesuai. Kunci yang tidak tercantum di sana adalah temuan keamanan, apa pun rilis yang Anda jalankan. Pada kegagalan ini `axt-verify` mencetak hash kunci dari setiap tanda tangan pada checkpoint yang disajikan dan hash kunci dari kunci yang dipercayainya, masing-masing sebagai delapan digit heksadesimal. Output tersebut sudah cukup untuk melakukan perbandingan.
  * Checkpoint yang bukan signed note yang terbentuk dengan baik, misalnya checkpoint yang root hash-nya tidak berukuran 32 byte.
  * Log yang menyusut, atau yang tidak dapat membuktikan bahwa ia memperluas checkpoint yang Anda simpan. Output kemudian memuat kedua checkpoint dan buktinya, sehingga bukti tersebut dapat berdiri sendiri.
  * Dua checkpoint yang ditandatangani untuk ukuran pohon yang sama dengan root hash yang berbeda. Output memuat kedua checkpoint tersebut.
  * File checkpoint yang diberikan dengan `--from` yang tanda tangannya tidak terverifikasi dengan kunci yang tertanam dalam rilis `axt-verify` Anda, atau file `--from` atau `--from-trusted` yang origin-nya bukan milik Anda. Untuk arsip yang ditandatangani sebelum rotasi kunci, lihat [Menyimpan arsip checkpoint Anda sendiri](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#keep-your-own-checkpoint-archive).
  * Bukti inklusi yang tidak mereproduksi root hash yang ditandatangani untuk event yang disajikan kepada Anda. Rilis yang tidak membangun ulang suatu versi leaf melaporkan hal ini untuk setiap event yang leaf-nya memiliki versi tersebut. Jika setiap event baru tiba-tiba gagal dengan cara ini sekaligus, periksa terlebih dahulu bahwa Anda menjalankan rilis `axt-verify` terbaru (lihat [Tingkatkan untuk versi leaf baru](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#upgrade-for-a-new-leaf-version)). Jika tidak, salin file state, simpan salinan dan output-nya, lalu jalankan rilis terbaru pada file `--state` asli. Kegagalan tersebut hilang setelah Anda menjalankan rilis yang membangun ulang versi tersebut. Jika Anda sudah menjalankan rilis terbaru, atau kegagalan tetap ada setelah Anda melakukan upgrade, itu adalah temuan keamanan.
  * Event di dalam jendela eksekusi yang disajikan secara berbeda dari cara eksekusi sebelumnya mencatatnya: byte leaf yang berbeda, indeks yang berbeda, atau tanpa indeks padahal sebelumnya memilikinya.
  * Event yang masih pending 24 jam setelah eksekusi pertama kali melihatnya.
  * Bukti inklusi yang ditolak (`400`, `401`, atau `403`) untuk event yang disajikan feed kepada Anda.
  * Bukti inklusi yang dikembalikan untuk `leaf_index` yang berbeda dari yang diminta.
  * Pada `events FILE`, event pada indeks yang sudah dicakup oleh checkpoint terbaru saat pemeriksaan dimulai, yang bukti inklusinya tidak disajikan sebelum waktu tunggu habis.
  * Event yang `organization_uuid`-nya bukan UUID organisasi yang Anda berikan dengan `--org`. Ketika organisasi induk menjalankan `events FILE` pada ekspor yang mencakup beberapa organisasi anak, setiap event organisasi lain akan gagal dengan cara ini, jadi pisahkan ekspor berdasarkan organisasi terlebih dahulu dan verifikasi setiap bagian dengan `--org`-nya sendiri.
  * `id` aktivitas yang sama pada dua indeks berbeda, atau dua kali pada satu indeks dengan konten berbeda, dalam satu eksekusi atau satu input `events FILE`.
  * Event yang leaf-nya tidak dapat dibangun ulang: misalnya, field terdokumentasi yang bukan string, nama field yang muncul dua kali, atau `type` yang hilang atau merupakan varian tidak dikenal dari tipe Access Transparency. `events FILE` melewati baris dengan tipe aktivitas lain dan tidak menggagalkannya.

* **`2`:** Kesalahan penggunaan atau konfigurasi. Penyebabnya adalah:

  * Flag yang hilang atau salah format.
  * Tidak ada `ANTHROPIC_COMPLIANCE_ACCESS_KEY`.
  * Kunci yang ditolak API (`401` atau `403`) sebelum ada checkpoint yang terverifikasi.
  * File state yang tidak dapat dibaca atau milik origin lain.

* **`3`:** Eksekusi tidak dapat diselesaikan. Dalam `run`, apa yang sudah diverifikasi disimpan ke file state. Jalankan lagi. Penyebabnya adalah:

  * Event dalam `events FILE` yang indeksnya tidak dicakup oleh checkpoint yang diterbitkan dalam waktu tunggu. Untuk event semacam itu, hasil **Tertunda** menjelaskan kapan harus berhenti menjalankan ulang dan melakukan eskalasi.
  * Kesalahan jaringan, pembatasan laju, atau kesalahan server yang bertahan melebihi percobaan ulang.
  * Respons yang tidak terduga.
  * File state atau `--save` yang tidak dapat ditulis.

  Status keluar `3` dengan respons `404` adalah hal yang diharapkan sampai Anthropic mencatat event Access Transparency pertama untuk organisasi Anda, karena setiap endpoint log transparansi mengembalikan `404` sampai event tersebut membuat log. Lakukan eskalasi jika endpoint log transparansi masih mengembalikan `404` lebih dari beberapa hari setelah Activity Feed Anda pertama kali menampilkan event Access Transparency, terlepas dari apakah event tersebut membawa `transparency_log_leaf_index`. Kombinasi tersebut tidak diharapkan. Setelah sebuah eksekusi berhasil, eskalasikan status keluar `3` yang terus berlanjut.

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
    Rotasi terencana diumumkan di [Fingerprint kunci yang dipublikasikan](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#published-key-fingerprints) setidaknya 30 hari sebelumnya, beserta tanggal peralihan. Pada tanggal peralihan, Anthropic mulai menandatangani dengan kunci baru dan menerbitkan rilis `axt-verify` yang memuatnya. Pada tanggal yang sama, Anthropic menerbitkan ulang checkpoint terbaru setiap organisasi dengan kunci baru, bahkan untuk log yang tidak bertambah. Setiap rilis `axt-verify` memuat satu kunci, jadi lakukan upgrade pada tanggal peralihan. Menjalankan rilis lama setelah peralihan akan gagal dengan status keluar `1`, begitu pula menjalankan rilis baru sebelum peralihan. Kedua kegagalan tersebut akan hilang setelah Anda menjalankan rilis yang sesuai. Checkpoint yang Anda simpan dengan kunci lama tetap menjadi titik awal yang valid, karena bukti append-only dari checkpoint yang disimpan ke checkpoint baru tidak bergantung pada kunci mana yang menandatangani checkpoint lama. Kunci baru muncul di bagian depan [kumpulan kunci verifier](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#read-the-verifier-keys) dan kunci-kunci sebelumnya tetap tercantum. Oleh karena itu, checkpoint yang sudah Anda verifikasi atau arsipkan tetap dapat diverifikasi terhadap kumpulan tersebut. Verifier milik Anda sendiri yang mem-pin fingerprint yang dipublikasikan perlu menambahkan fingerprint baru, beserta tanggal peralihannya, sebelum tanggal tersebut. Verifier yang menyimpan kumpulan kunci secara lokal akan mengambilnya ulang ketika menemukan tanda tangan yang hash kuncinya tidak dimilikinya. Sebuah checkpoint mengikat seluruh riwayat. Setelah satu checkpoint yang ditandatangani dengan kunci baru terverifikasi, dan bukti konsistensi dari checkpoint yang Anda simpan mengarah kepadanya, setiap entri sebelumnya juga ditetapkan ulang.
  </Accordion>

  <Accordion title="Apa itu versi leaf, dan apakah saya perlu melacak versi mana yang dimiliki sebuah leaf?">
    Versi leaf adalah byte pertama dari entri leaf. Versi ini menyatakan kumpulan field mana yang di-commit oleh leaf (lihat [Bagaimana event menjadi leaf](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#how-an-event-becomes-a-leaf)). Anda tidak perlu melacaknya. Log Anda dapat berisi leaf dari lebih dari satu versi, dan verifier membangun ulang entri yang disebutkan oleh aturan terakhir di bagian tersebut untuk sebuah event, serta menerima event tersebut jika bukti inklusinya cocok dengan salah satunya. Yang Anda perlukan adalah rilis `axt-verify` yang membangun ulang versi terbaru yang ditulis log Anda (lihat [Tingkatkan untuk versi leaf baru](https://platform.claude.com/docs/id/manage-claude/access-transparency-log#upgrade-for-a-new-leaf-version)).
  </Accordion>

  <Accordion title="Bisakah saya menghitung bukti sendiri alih-alih memanggil endpoint bukti?">
    Ya. Hash tile adalah antarmuka utama, dan klien tlog-tiles yang mendukung kunci note ECDSA dapat menghitung bukti inklusi dan bukti konsistensi darinya. Endpoint bukti hanyalah kemudahan. Klien generik memerlukan wrapper tipis untuk mengirim header `x-api-key` dan, untuk kunci organisasi induk, parameter `organization_id`.
  </Accordion>

  <Accordion title="Bagaimana jika organisasi saya berhenti menggunakan Access Transparency?">
    Tidak ada yang dihapus. Log Anda tetap dapat dibaca dan diverifikasi melalui endpoint yang sama, jadi tetap verifikasi seperti sebelumnya. Jika organisasi Anda mengaktifkan Access Transparency lagi di kemudian hari, log yang sama akan berlanjut, dan bukti konsistensi akan menjangkau celah tersebut.
  </Accordion>

  <Accordion title="Bisakah saya memverifikasi semua organisasi anak saya dengan satu kunci?">
    Ya. Kunci organisasi induk membaca log organisasi anak mana pun yang terdaftar dengan memberikan `organization_id`. Setiap organisasi anak memiliki log, origin, dan checkpoint tersimpan sendiri. Jalankan verifikasi terpisah, dengan state-nya sendiri, untuk setiap organisasi anak.
  </Accordion>
</AccordionGroup>

## Sumber daya terkait

* [Access Transparency](https://platform.claude.com/docs/id/manage-claude/access-transparency)
* [Mengkueri Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed)
* [Ikhtisar Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api)
* [Menangani error Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-errors)
* [axt-verify](https://github.com/anthropics/axt-verify), verifier open-source Anthropic untuk log transparansi
* [C2SP tlog-tiles](https://c2sp.org/tlog-tiles) dan [C2SP signed note](https://c2sp.org/signed-note), format wire untuk tile, bundle entri, dan checkpoint
* [RFC 9162](https://www.rfc-editor.org/rfc/rfc9162), algoritma pohon Merkle, bukti inklusi, dan bukti konsistensi
* [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785), JSON Canonicalization Scheme yang digunakan untuk leaf
