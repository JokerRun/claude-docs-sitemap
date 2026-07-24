---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-api
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 9a6383225b50922f7227fc4adfa7d46287dccd41e012698001f5a2a9a07afbfc
---

# Compliance API

Akses terprogram ke aktivitas Claude organisasi Anda, chat, file, proyek, dan pengguna untuk kepatuhan, audit, dan tata kelola.

---

Compliance API memberikan pelanggan Claude Enterprise akses terprogram ke Activity Feed organisasi mereka, direktori pengguna, peran, dan grup di setiap organisasi yang tertaut, pengaturan efektif yang berlaku untuk setiap organisasi, dan, untuk organisasi claude.ai, chat, file, dan proyek yang mendasarinya. Tim keamanan, hukum, dan kepatuhan menggunakannya untuk mengaudit aktivitas, mengambil atau menghapus konten, dan memasukkan peristiwa ke dalam perangkat hilir.

<Note>
  Dua jenis kunci membuka Compliance API. **Compliance Access Key** (dibuat di claude.ai) menjangkau setiap endpoint, dan **Admin API key** (dibuat di Claude Console) hanya menjangkau Activity Feed. Lihat [Kunci mana yang Anda butuhkan?](/docs/id/manage-claude/compliance-api-access#which-key-do-you-need) untuk perbandingan lengkap jenis kunci.
</Note>

Panggilan berikut mengembalikan peristiwa aktivitas terbaru di organisasi Anda. Kunci apa pun dengan cakupan `read:compliance_activities` dapat melakukannya. Untuk membuat kunci dan memberikan cakupan tersebut, lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access).

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/compliance/activities?limit=1" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

Respons yang berhasil mengembalikan objek JSON yang berisi `data` (array dari record `Activity`), `has_more`, `first_id`, dan `last_id`:

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

Setiap endpoint berada di bawah `/v1/compliance/*` pada `https://api.anthropic.com` dan melakukan autentikasi melalui header `x-api-key`. Untuk menyediakan kunci, lihat [Menyiapkan Compliance API](/docs/id/manage-claude/compliance-api-access).

Activity Feed (`GET /v1/compliance/activities`) tersedia untuk kunci apa pun yang membawa cakupan `read:compliance_activities`; lihat [Melakukan kueri Activity Feed](/docs/id/manage-claude/compliance-activity-feed) untuk filter, paginasi, dan objek `Activity` lengkap. Endpoint lainnya memerlukan Compliance Access Key yang membawa cakupan yang relevan.

Tenant Claude Enterprise memiliki satu organisasi induk (kontainer tingkat atas yang memusatkan identitas) dengan organisasi tertaut dari dua jenis: organisasi claude.ai, tempat pengguna melakukan chat dan menyimpan konten, dan organisasi Claude Console, tempat pengguna mengelola beban kerja Claude API. Untuk kunci yang mencakup organisasi induk, endpoint direktori (organisasi, pengguna, peran, dan grup) mengembalikan data dari setiap organisasi tertaut dari kedua jenis tersebut. Endpoint konten (chat, file, proyek, dan lampiran proyek) hanya melayani data claude.ai.

Semua endpoint `/v1/compliance/*` berbagi satu "rate limit" (batas laju) sebesar 600 permintaan per menit per organisasi induk; lihat [429 Too Many Requests](/docs/id/manage-claude/compliance-errors#429-too-many-requests) untuk header respons dan kontrak percobaan ulang.

***

## Compliance API versus fitur terkait

Dua fitur yang berdekatan tumpang tindih dengan Compliance API; berikut cara memilihnya.

### Mengekspor log audit

Ekspor log audit adalah fitur terpisah di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls) yang memungkinkan owner dan primary owner mengunduh CSV berisi peristiwa organisasi. Fitur ini jauh lebih sempit daripada Compliance API: jendela lihat-balik yang dibatasi, hanya unduhan CSV, dan tidak ada akses ke konten chat, file, atau proyek. Standarkan pada Compliance API untuk penggunaan terprogram yang berkelanjutan.

### Analytics API

Anthropic menyediakan dua API analitik: Claude Enterprise Analytics API dan [Claude Code Analytics API](/docs/id/manage-claude/claude-code-analytics-api). Keduanya mengembalikan angka penggunaan dan biaya teragregasi untuk tim IT, FinOps, dan platform, sedangkan Compliance API mengembalikan record per-peristiwa untuk tim keamanan, hukum, dan kepatuhan. Kedua keluarga API ini menjawab pertanyaan yang berbeda, menggunakan kunci yang berbeda, dan disediakan secara terpisah.

***

## Di bagian ini

<CardGroup>
  <Card href="/docs/id/manage-claude/compliance-api-access" title="Menyiapkan Compliance API">
    Aktifkan Compliance API untuk organisasi Anda, lalu buat Compliance Access Key (dengan izin bercakupan) atau Admin API key, dan pelajari mana yang harus digunakan.
  </Card>

  <Card href="/docs/id/manage-claude/compliance-activity-feed" title="Melakukan kueri Activity Feed">
    Ambil, filter, dan lakukan paginasi pada Activity Feed bersama. Didukung oleh kedua jenis kunci.
  </Card>

  <Card href="/docs/id/manage-claude/compliance-content-data" title="Mengambil dan menghapus chat, file, dan proyek">
    Baca konten chat dan lampiran, lalu hapus sesuai permintaan. Memerlukan Compliance Access Key.
  </Card>

  <Card href="/docs/id/manage-claude/compliance-org-data" title="Mendaftar organisasi, pengguna, peran, grup, dan pengaturan">
    Enumerasi organisasi tertaut, anggota, peran, dan grup direktori, serta baca pengaturan efektif setiap organisasi.
  </Card>

  <Card href="/docs/id/manage-claude/compliance-integration-patterns" title="Merancang integrasi kepatuhan Anda">
    Pilih pola konsumsi feed, rencanakan korelasi SIEM, dan tentukan pendekatan retensi Anda.
  </Card>

  <Card href="/docs/id/manage-claude/compliance-errors" title="Menangani kesalahan Compliance API">
    Setiap respons 400, 401, 403, 404, 409, 429, dan 5xx yang dikembalikan Compliance API, beserta perbaikan untuk masing-masing.
  </Card>

  <Card href="/docs/id/api/compliance" title="Referensi API">
    Jalur endpoint, parameter, dan skema respons untuk setiap panggilan Compliance API.
  </Card>

  <Card href="/docs/id/manage-claude/compliance-faq" title="FAQ Compliance API">
    Jawaban atas pertanyaan umum tentang kunci, cakupan, ketersediaan, dan integrasi.
  </Card>
</CardGroup>
