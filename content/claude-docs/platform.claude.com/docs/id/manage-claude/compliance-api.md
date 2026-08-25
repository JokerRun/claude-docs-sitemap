---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-api
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 1405188411957abcef35635b5d2963b6343cb860467a255447fb38a56fe053be
---

---
title: Compliance API
url: https://platform.claude.com/docs/id/manage-claude/compliance-api
description: Akses terprogram ke aktivitas Claude, chat, file, proyek, sesi Claude Cowork dan Claude Code, serta pengguna di organisasi Anda untuk kepatuhan, audit, dan tata kelola.
---

Compliance API memberi pelanggan Claude Enterprise dan Claude Console akses terprogram ke Activity Feed (umpan aktivitas) organisasi mereka. Untuk organisasi Claude Enterprise, API ini juga mencakup direktori pengguna, peran, dan grup di setiap organisasi tertaut; pengaturan efektif yang berlaku untuk setiap organisasi; chat, file, dan proyek yang mendasarinya di organisasi claude.ai; serta sesi Cowork dan Claude Code. Tim keamanan, hukum, dan kepatuhan menggunakannya untuk mengaudit aktivitas, mengambil atau menghapus konten, dan mengalirkan peristiwa ke perangkat hilir.

<Note>
  Dua jenis kunci membuka akses ke Compliance API. **Compliance Access Key** (dibuat di claude.ai) dapat menjangkau setiap endpoint, dan **kunci Admin API** (dibuat di Claude Console) hanya dapat menjangkau Activity Feed. Lihat [Kunci mana yang Anda perlukan?](https://platform.claude.com/docs/id/manage-claude/compliance-api-access#which-key-do-you-need) untuk perbandingan lengkap jenis kunci.
</Note>

Panggilan berikut mengembalikan peristiwa aktivitas terbaru di organisasi Anda. Kunci apa pun dengan cakupan `read:compliance_activities` dapat melakukannya. Untuk membuat kunci dan memberinya cakupan tersebut, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).

```bash cURL
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/activities?limit=1" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

Respons yang berhasil mengembalikan objek JSON yang berisi `data` (array berisi catatan `Activity`), `has_more`, `first_id`, dan `last_id`:

```json Response
{
  "data": [
    {
      "id": "activity_01XyDMpzjS89pFZXqSFUBDr6",
      "created_at": "2026-04-10T08:09:10Z",
      "organization_id": "org_01Wv6QeBcDfGhJkLmNpQrSt8",
      "organization_uuid": "abcdef01-2345-6789-abcd-ef0123456789",
      "actor": {
        "type": "user_actor",
        "email_address": "user@example.com",
        "user_id": "user_01TuVwXyZaBcDeFgH2JkLmN4",
        "ip_address": "192.0.2.34",
        "user_agent": "Mozilla/5.0..."
      },
      "type": "claude_chat_created",
      "claude_chat_id": "claude_chat_01XyDMpzjS89pFZXqSFUBDr6",
      "claude_project_id": "claude_proj_01KGp4eZNug9ri4kE35RSppq"
    }
  ],
  "has_more": true,
  "first_id": "activity_01XyDMpzjS89pFZXqSFUBDr6",
  "last_id": "activity_01XyDMpzjS89pFZXqSFUBDr6"
}
```

***

## Cara kerja Compliance API

Setiap endpoint berada di bawah `/v1/compliance/*` pada `https://api.anthropic.com` dan diautentikasi melalui header `x-api-key`. Untuk menyediakan kunci, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).

Activity Feed (`GET /v1/compliance/activities`) tersedia untuk kunci apa pun yang memiliki cakupan `read:compliance_activities`; lihat [Mengkueri Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) untuk filter, paginasi, dan objek `Activity` lengkap. Endpoint lainnya memerlukan Compliance Access Key yang memiliki cakupan yang relevan.

Tenant Claude Enterprise memiliki satu organisasi induk (wadah tingkat atas yang memusatkan identitas) dengan organisasi tertaut dari dua jenis: organisasi claude.ai, tempat pengguna melakukan chat dan menyimpan konten, dan organisasi Claude Console, tempat pengguna mengelola beban kerja Claude API. Untuk kunci yang mencakup organisasi induk, endpoint direktori (organisasi, pengguna, peran, dan grup) mengembalikan data dari setiap organisasi tertaut dari kedua jenis tersebut. Endpoint konten (chat, file, proyek, lampiran proyek, dan sesi) hanya melayani data Claude Enterprise. Endpoint chat, file, dan proyek mengembalikan chat, file, dan proyek claude.ai. Endpoint sesi mengembalikan transkrip sesi Cowork dan Claude Code di mesin pengguna (sesi lokal), yang direkam saat pengguna masuk dengan akun Claude Enterprise mereka. Endpoint ini juga mengembalikan transkrip sesi Cowork yang dimulai di claude.ai web atau seluler, yang berjalan di cloud dalam lingkungan yang dikelola Anthropic (sesi jarak jauh). Organisasi Claude Console mandiri (yang tidak memiliki organisasi induk) bukan bagian dari tenant Claude Enterprise; organisasi ini menggunakan kunci Admin API dan hanya dapat mengkueri Activity Feed.

Semua endpoint `/v1/compliance/*` berbagi "rate limit" (batas laju) sebesar 600 permintaan per menit per organisasi induk (untuk organisasi Claude Console mandiri, per organisasi). Endpoint sesi lokal hanya dihitung terhadap batas bersama tersebut, dan endpoint sesi jarak jauh memiliki anggaran permintaan kedua di atasnya. Lihat [429 Too Many Requests](https://platform.claude.com/docs/id/manage-claude/compliance-errors#429-too-many-requests) untuk header respons dan kontrak percobaan ulang.

***

## Compliance API versus fitur terkait

Beberapa fitur yang berdekatan tumpang tindih dengan Compliance API; berikut cara memilihnya.

### Ekspor log audit

Ekspor log audit adalah fitur terpisah di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls) yang memungkinkan pemilik dan pemilik utama mengunduh CSV berisi peristiwa organisasi. Fitur ini jauh lebih sempit daripada Compliance API: jendela lihat-balik yang dibatasi, hanya unduhan CSV, dan tanpa akses ke konten chat, file, atau proyek. Standarkan pada Compliance API untuk penggunaan terprogram yang berkelanjutan.

### Analytics API

Anthropic menyediakan dua API analitik: Claude Enterprise Analytics API dan [Claude Code Analytics API](https://platform.claude.com/docs/id/manage-claude/claude-code-analytics-api). Keduanya mengembalikan angka penggunaan dan biaya teragregasi untuk tim IT, FinOps, dan platform, sedangkan Compliance API mengembalikan catatan per peristiwa untuk tim keamanan, hukum, dan kepatuhan. Kedua keluarga API ini menjawab pertanyaan yang berbeda, menggunakan kunci yang berbeda, dan disediakan secara terpisah.

### Logging OpenTelemetry

[Logging OpenTelemetry Cowork](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) dan [pemantauan Claude Code](https://code.claude.com/docs/en/monitoring-usage) melakukan streaming telemetri per peristiwa, termasuk metadata token, biaya, dan host, ke kolektor yang Anda jalankan saat aktivitas terjadi, sedangkan Compliance API mengembalikan transkrip per sesi yang disimpan dari Anthropic berdasarkan permintaan dan berfungsi dengan Compliance Access Key Anda yang sudah ada. Logging OpenTelemetry juga dapat merekam prompt dan respons, tetapi Anthropic merekomendasikan Compliance API untuk mengambil konten sesi Cowork dan Claude Code. Untuk tabel yang membandingkan sesi lokal, sesi jarak jauh, dan logging OpenTelemetry, lihat pengantar [Mengambil transkrip sesi](https://platform.claude.com/docs/id/manage-claude/compliance-sessions).

### Inference hooks

[Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks) (beta) bekerja secara inline: server keamanan AI organisasi Anda menerima setiap prompt yang diatur sebelum inferensi dan dapat menolaknya secara real time, sedangkan Compliance API mengambil catatan setelah kejadian dan mengembalikan data yang lebih kaya, seperti pengaturan organisasi dan file non-teks lengkap.

***

## Di bagian ini

<CardGroup>
  <Card href="https://platform.claude.com/docs/id/manage-claude/compliance-api-access" title="Menyiapkan Compliance API">
    Aktifkan Compliance API untuk organisasi Anda, lalu buat Compliance Access Key (dengan izin tercakup) atau kunci Admin API, dan pelajari mana yang harus digunakan.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed" title="Mengkueri Activity Feed">
    Ambil, filter, dan paginasi Activity Feed bersama. Didukung oleh kedua jenis kunci.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/compliance-content-data" title="Mengambil dan menghapus chat, file, dan proyek">
    Baca konten chat, file, dan lampiran proyek; hapus chat, file, dan proyek sesuai permintaan. Memerlukan Compliance Access Key.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/compliance-sessions" title="Mengambil transkrip sesi">
    Daftarkan sesi yang dijalankan pengguna Anda di aplikasi dan agen Claude, seperti Cowork dan Claude Code, dan ambil transkripnya. Memerlukan Compliance Access Key.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/compliance-org-data" title="Mendaftar organisasi, pengguna, peran, grup, dan pengaturan">
    Enumerasi organisasi tertaut, anggota, peran, dan grup direktori, serta baca pengaturan efektif setiap organisasi.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns" title="Merancang integrasi kepatuhan Anda">
    Pilih pola konsumsi feed, rencanakan korelasi SIEM, dan tentukan pendekatan retensi Anda.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/compliance-errors" title="Menangani error Compliance API">
    Setiap respons 400, 401, 403, 404, 409, 429, dan 5xx yang dikembalikan Compliance API, beserta perbaikan untuk masing-masing.
  </Card>

  <Card href="https://platform.claude.com/docs/id/api/compliance" title="Referensi API">
    Jalur endpoint, parameter, dan skema respons untuk setiap panggilan Compliance API.
  </Card>

  <Card href="https://platform.claude.com/docs/id/manage-claude/compliance-faq" title="FAQ Compliance API">
    Jawaban atas pertanyaan umum tentang kunci, cakupan, ketersediaan, dan integrasi.
  </Card>
</CardGroup>
