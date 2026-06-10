---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-api
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: f61db6188e1e2c612aea9fa492bf49ced86be1f5d9c6ec66a994928af77de2f5
---

# Compliance API

Akses terprogram ke aktivitas Claude organisasi Anda, percakapan, file, proyek, dan pengguna untuk kepatuhan, audit, dan tata kelola.

---

<Note>
  Compliance API diaktifkan berdasarkan permintaan. Organisasi Claude Enterprise memiliki akses ke API lengkap; organisasi Claude Console hanya memiliki akses ke [Activity Feed](/docs/id/manage-claude/compliance-activity-feed). Lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access).
</Note>

Compliance API memberi pelanggan Claude Enterprise akses terprogram ke Activity Feed organisasi mereka, direktori pengguna, peran, dan grup di setiap organisasi yang tertaut, serta, untuk organisasi claude.ai, percakapan, file, dan proyek yang mendasarinya. Tim keamanan, hukum, dan kepatuhan menggunakannya untuk mengaudit aktivitas, mengambil atau menghapus konten, dan mengalirkan peristiwa ke perangkat hilir.

<Note>
  Dua jenis kunci membuka akses ke Compliance API. **Compliance Access Key** (dibuat di claude.ai) menjangkau setiap endpoint, dan **kunci Admin API** (dibuat di Claude Console) hanya menjangkau Activity Feed. Lihat [Kunci mana yang Anda butuhkan?](/docs/id/manage-claude/compliance-api-access#which-key-do-you-need) untuk perbandingan lengkap jenis kunci.
</Note>

Panggilan berikut mengembalikan peristiwa aktivitas terbaru di organisasi Anda. Kunci apa pun dengan scope `read:compliance_activities` dapat melakukannya. Untuk membuat kunci dan memberinya scope tersebut, lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access).

<CodeGroup>
```bash cURL nocheck
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/activities?limit=1" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```
</CodeGroup>

Respons yang berhasil mengembalikan objek JSON yang berisi `data` (array berisi record `Activity`), `has_more`, `first_id`, dan `last_id`:

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

---

## Cara kerja Compliance API \{#how-the-compliance-api-works}

Setiap endpoint berada di bawah `/v1/compliance/*` pada `https://api.anthropic.com` dan melakukan autentikasi melalui header `x-api-key`. Untuk menyediakan kunci, lihat [Mendapatkan akses ke Compliance API](/docs/id/manage-claude/compliance-api-access).

Activity Feed (`GET /v1/compliance/activities`) tersedia untuk kunci apa pun yang memiliki scope `read:compliance_activities`; lihat [Mengkueri Activity Feed](/docs/id/manage-claude/compliance-activity-feed) untuk filter, paginasi, dan objek `Activity` lengkap. Endpoint lainnya memerlukan Compliance Access Key yang memiliki scope yang relevan.

Tenant Claude Enterprise memiliki satu organisasi induk (kontainer tingkat atas yang memusatkan identitas) dengan organisasi tertaut dari dua jenis: organisasi claude.ai, tempat pengguna melakukan percakapan dan menyimpan konten, dan organisasi Claude Console, tempat pengguna mengelola beban kerja Claude API. Endpoint direktori (organisasi, pengguna, peran, dan grup) mengembalikan data dari setiap organisasi tertaut dari kedua jenis tersebut. Endpoint konten (percakapan, file, proyek, dan lampiran proyek) hanya menyajikan data claude.ai.

Semua endpoint `/v1/compliance/*` berbagi satu batas laju sebesar 600 permintaan per menit per organisasi induk; lihat [429 Too Many Requests](/docs/id/manage-claude/compliance-errors#429-too-many-requests) untuk header respons dan kontrak percobaan ulang.

---

## Compliance API versus fitur terkait \{#compliance-api-versus-related-features}

Dua fitur yang berdekatan tumpang tindih dengan Compliance API; berikut cara memilihnya.

### Ekspor log audit \{#export-audit-logs}

Ekspor log audit adalah fitur terpisah di [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls) yang memungkinkan owner dan primary owner mengunduh CSV berisi peristiwa organisasi. Fitur ini jauh lebih terbatas dibandingkan Compliance API: jendela lookback yang dibatasi, hanya unduhan CSV, dan tidak ada akses ke konten percakapan, file, atau proyek. Standarkan penggunaan Compliance API untuk penggunaan terprogram yang berkelanjutan.

### Analytics API \{#analytics-api}

Anthropic menyediakan dua API analitik: Claude Enterprise Analytics API dan [Claude Code Analytics API](/docs/id/manage-claude/claude-code-analytics-api). Keduanya mengembalikan angka penggunaan dan biaya agregat untuk tim IT, FinOps, dan platform, sedangkan Compliance API mengembalikan record per peristiwa untuk tim keamanan, hukum, dan kepatuhan. Kedua keluarga API ini menjawab pertanyaan yang berbeda, menggunakan kunci yang berbeda, dan disediakan secara terpisah.

---

## Di bagian ini \{#in-this-section}

<CardGroup>
  <Card href="/docs/id/manage-claude/compliance-api-access" title="Mendapatkan akses ke Compliance API">
    Minta akses Compliance API untuk organisasi Anda, lalu buat Compliance Access Key (dengan izin ber-scope) atau kunci Admin API, dan pelajari mana yang harus digunakan.
  </Card>
  <Card href="/docs/id/manage-claude/compliance-activity-feed" title="Mengkueri Activity Feed">
    Ambil, filter, dan paginasi Activity Feed bersama. Didukung oleh kedua jenis kunci.
  </Card>
  <Card href="/docs/id/manage-claude/compliance-content-data" title="Mengambil dan menghapus percakapan, file, dan proyek">
    Baca konten percakapan dan lampiran, lalu hapus sesuai permintaan. Memerlukan Compliance Access Key.
  </Card>
  <Card href="/docs/id/manage-claude/compliance-org-data" title="Mencantumkan organisasi, pengguna, peran, dan grup">
    Enumerasi organisasi tertaut, anggota, peran, dan grup direktori.
  </Card>
  <Card href="/docs/id/manage-claude/compliance-integration-patterns" title="Merancang integrasi kepatuhan Anda">
    Pilih pola konsumsi feed, rencanakan korelasi SIEM, dan tentukan pendekatan retensi Anda.
  </Card>
  <Card href="/docs/id/manage-claude/compliance-errors" title="Menangani error Compliance API">
    Setiap respons 400, 401, 403, 404, 409, 429, dan 5xx yang dikembalikan Compliance API, beserta perbaikan untuk masing-masing.
  </Card>
  <Card href="/docs/id/api/compliance" title="Referensi API">
    Path endpoint, parameter, dan skema respons untuk setiap panggilan Compliance API.
  </Card>
  <Card href="/docs/id/manage-claude/compliance-faq" title="FAQ Compliance API">
    Jawaban atas pertanyaan umum tentang kunci, scope, ketersediaan, dan integrasi.
  </Card>
</CardGroup>