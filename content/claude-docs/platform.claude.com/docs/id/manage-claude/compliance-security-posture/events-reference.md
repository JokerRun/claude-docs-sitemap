---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 9a667e97b758ecc33f7bae9dda823b67a166fa4407bd67dda854349abd8b5d4f
---

---
title: Referensi peristiwa Security posture
url: https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference
description: "Cari aktivitas Activity Feed yang mencatat perubahan di halaman Security posture: field dan nilainya, contoh untuk masing-masing aktivitas, serta apa yang tidak dicatat oleh feed."
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

[Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) mencatat perubahan pada atestasi di halaman [Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview) sebagai aktivitas yang dijelaskan di halaman ini. Untuk memasukkannya ke sistem security information and event management (SIEM), mulailah dari [Mengirim peristiwa Security posture ke SIEM Anda](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/send-events). Teruskan apa adanya setiap nilai `control`, `action`, atau field lain yang tidak dicantumkan di halaman ini, abaikan field yang tidak terduga, dan perlakukan kunci yang tidak ada dan nilai `null` dengan cara yang sama. [Memahami objek Activity](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#understand-the-activity-object) membahas field standar dan tipe yang tidak dikenal.

Anda memerlukan Compliance Access Key yang mencakup organisasi tersebut, dengan scope `read:compliance_activities` atau `read:org_audit`.

## Aktivitas atestasi

Aktivitas `org_security_control_attestation_updated` mencatat bahwa seseorang mencatat, mengubah, menyimpan ulang, atau mencabut atestasi organisasi untuk suatu kontrol keamanan, atau bahwa atestasi tersebut berhenti berlaku secara otomatis. `created_at`-nya adalah waktu perubahan oleh seseorang atau, untuk perubahan otomatis, waktu saat perubahan dicatat, yang dapat lebih lambat daripada perubahan tersebut. `actor`-nya adalah `user_actor` untuk perubahan oleh seseorang dan `system_actor` untuk perubahan otomatis, seperti `lapsed`.

### Field

Tipe ini menambahkan field berikut, dengan `status` sebagai nilai atestasi dan `review_date` sebagai tanggal berakhirnya.

| Field             | Tipe   | Deskripsi                                                                                                                                                            |
| ----------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `control`         | string | Pengidentifikasi kontrol keamanan yang menjadi sasaran atestasi, misalnya `oauth_conditional_access`; perlakukan sebagai string opaque.                              |
| `action`          | string | Apa yang berubah, sebagai salah satu [nilai `action`](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference#action-values). |
| `status`          | string | Nilai atestasi: Selesai (`completed`), Risiko diterima (`accepted_risk`), atau diatestasi sebagai Gagal (`control_failed`); tidak ada jika atestasi dicabut.         |
| `previous_status` | string | Nilai atestasi sebelum perubahan ini, salah satu dari tiga nilai yang sama; tidak ada jika `action` adalah `attested`.                                               |
| `review_date`     | string | Hari UTC (tanggal ISO 8601) saat atestasi dijadwalkan berhenti berlaku; tidak ada jika atestasi disimpan tanpa tanggal berakhir, atau dicabut.                       |

Pada kontrol khusus informasi, nilai Ditinjau dicatat sebagai `completed`.

### Nilai `action`

| `action`   | Arti                                                                                                                                         |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `attested` | Atestasi dicatat untuk kontrol yang sebelumnya belum memilikinya.                                                                            |
| `changed`  | Atestasi disimpan ulang dengan nilai lain atau, jika `status` sama dengan `previous_status`, dengan nilai yang sama, seperti pada `renewed`. |
| `renewed`  | Atestasi disimpan ulang dengan nilai yang sama.                                                                                              |
| `cleared`  | Seseorang mencabut atestasi.                                                                                                                 |
| `lapsed`   | Atestasi berhenti berlaku secara otomatis, bukan oleh seseorang.                                                                             |

Pada aktivitas `renewed` dan `lapsed`, `status` sama dengan `previous_status`. Penyimpanan dengan nilai yang sama setelah aktivitas `lapsed` dicatat sebagai `renewed`, bukan `attested`.

### Arti aktivitas `lapsed`

Aktivitas `lapsed` berarti hasil pemeriksaan atau nilai saat ini dari kontrol berbeda dari yang menjadi dasar saat atestasi disimpan; nilai saat ini dapat berubah tanpa ada pengaturan yang diubah, misalnya ketika Anthropic mengubah kata-katanya. `status` adalah nilai yang berhenti berlaku: salah satu dari ketiganya. Atestasi untuk kontrol manual tidak pernah mendapatkan aktivitas `lapsed`. Aktivitas ini dapat muncul lebih lambat daripada perubahan yang menyebabkannya.

### Contoh

```json
{
  "id": "activity_01Hq7ZtYc4Vb2NmKx8RsPd3W",
  "type": "org_security_control_attestation_updated",
  "created_at": "2026-10-20T15:04:00.220114Z",
  "organization_id": "org_01JuY4bkwkH1x4PodBJaWmh2",
  "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
  "actor": {
    "type": "user_actor",
    "email_address": "priya@example.com",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
    "ip_address": "192.0.2.34",
    "user_agent": "Mozilla/5.0..."
  },
  "control": "directory_sync_enabled",
  "action": "attested",
  "status": "accepted_risk"
}
```

## Apa yang tidak dicatat oleh feed

Jangan menganggap tidak adanya aktivitas sebagai tanda bahwa tidak ada yang berubah. Untuk hasil saat ini, lihat [Referensi hasil Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference); endpoint-nya dapat menghilangkan kontrol yang disebut oleh suatu aktivitas.

* Perubahan dari sebelum [Activity Feed](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed) mulai mencatat aktivitas ini untuk organisasi, atau selama Compliance API nonaktif. Feed tidak pernah menambahkan aktivitas untuk perubahan tersebut di kemudian hari.
* Jarang terjadi, perubahan jenis apa pun.
* Setiap tanggal berakhir yang tiba: tidak semuanya mendapatkan aktivitas, jadi jangan menunggu aktivitas.
* Setiap kali halaman Security posture dinonaktifkan atau diaktifkan: jangan mengandalkan [aturan deteksi](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/detect-changes) untuk mendeteksinya.
* Komentar yang disimpan bersama atestasi, atau tanda apa pun bahwa komentar tersebut ada. Mengubah komentar memerlukan penyimpanan baru, yang dicatat oleh feed seperti penyimpanan lain dengan nilai yang sama (lihat [nilai `action`](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference#action-values)).
* Jenis kontrol yang menjadi sasaran atestasi: otomatis, manual, atau khusus informasi.
* Setiap perubahan yang dapat membuat atestasi berhenti berlaku: tidak semuanya mendapatkan aktivitas `lapsed`.
