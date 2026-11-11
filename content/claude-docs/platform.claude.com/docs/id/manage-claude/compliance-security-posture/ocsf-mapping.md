---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/ocsf-mapping
fetched_at: 2026-11-11T02:12:04.616753Z
sha256: 7e38db714dfff8a0d06d027f54a148db4055b7e2a36d019f7f1c546a337a37f5
---

---
title: Memetakan peristiwa Security posture ke OCSF
url: https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/ocsf-mapping
description: Petakan setiap aktivitas Security posture di Compliance API ke kelas dan atribut Open Cybersecurity Schema Framework (OCSF)-nya sebelum Anda menyimpannya.
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

[Open Cybersecurity Schema Framework](https://schema.ocsf.io/) (OCSF) adalah skema terbuka untuk peristiwa keamanan. Terapkan pemetaan ini pada aktivitas [Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview) di pipeline Anda sendiri, setelah Anda membacanya dan sebelum Anda menyimpannya. Untuk memasukkannya ke sistem security information and event management (SIEM) Anda, mulailah dari [Mengirim peristiwa Security posture ke SIEM Anda](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/send-events).

## Versi OCSF

Pemetaan ini menggunakan OCSF 1.6.0. Jika Anda melakukan validasi terhadap versi lain, periksa atribut di halaman ini terhadap versi tersebut. Misalnya, di OCSF 1.7.0, `metadata.uid` adalah pengidentifikasi dari peristiwa OCSF itu sendiri, dan `metadata.original_event_uid` menyimpan pengidentifikasi dari sumber. OCSF 1.9.0 menghentikan penggunaan `actor.app_name` dan menggantinya dengan `actor.application`.

## Atribut untuk setiap aktivitas Security posture

Petakan field berikut pada setiap peristiwa.

| Field aktivitas     | Atribut OCSF                   | Catatan                                                                                                                                                                                                                              |
| ------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`                | `metadata.uid`                 | Salin tanpa perubahan.                                                                                                                                                                                                               |
| `type`              | `metadata.event_code`          | Salin tanpa perubahan.                                                                                                                                                                                                               |
| `created_at`        | `time`                         | Konversikan string RFC 3339 menjadi milidetik sejak epoch Unix, lalu potong menjadi bilangan bulat.                                                                                                                                  |
| `created_at`        | `metadata.original_time`       | Salin string tanpa perubahan.                                                                                                                                                                                                        |
| Tidak ada           | `metadata.logged_time`         | Waktu saat Anda menyimpan aktivitas (`stored_at` di [Mendeteksi perubahan](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/detect-changes#before-you-write-a-rule)), dalam milidetik sejak epoch Unix. |
| `organization_uuid` | `metadata.tenant_uid`          | Salin tanpa perubahan.                                                                                                                                                                                                               |
| `organization_id`   | `unmapped.organization_id`     | Salin tanpa perubahan.                                                                                                                                                                                                               |
| Tidak ada           | `metadata.version`             | Konstan: `1.6.0`.                                                                                                                                                                                                                    |
| Tidak ada           | `metadata.product.vendor_name` | Konstan: `Anthropic`.                                                                                                                                                                                                                |
| Tidak ada           | `metadata.product.name`        | Konstan: `Compliance API`.                                                                                                                                                                                                           |
| Tidak ada           | `type_uid`                     | `class_uid * 100 + activity_id`.                                                                                                                                                                                                     |
| Tidak ada           | `severity_id`                  | Setel ke `1` (Informational) pada setiap peristiwa, dan tetapkan prioritas peringatan di [aturan deteksi](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/detect-changes) yang memunculkannya.         |

Masukkan setiap field yang tidak memiliki atribut OCSF ke dalam objek `unmapped` dengan nama yang digunakan di Activity Feed, termasuk field yang tidak dikenali oleh handler Anda. Jika sebuah field tidak ada atau bernilai `null`, hilangkan atribut OCSF-nya.

Petakan objek `actor`:

| Field aktivitas       | Atribut OCSF              | Catatan                                                                                |
| --------------------- | ------------------------- | -------------------------------------------------------------------------------------- |
| Tidak ada             | `metadata.profiles`       | Tambahkan `host`, yaitu profil OCSF (sekumpulan atribut opsional) yang memuat `actor`. |
| `actor.type`          | `unmapped.actor.type`     | Salin tanpa perubahan.                                                                 |
| `actor.user_id`       | `actor.user.uid`          | Hanya `user_actor`.                                                                    |
| `actor.email_address` | `actor.user.email_addr`   | Hanya `user_actor`.                                                                    |
| `actor.ip_address`    | `src_endpoint.ip`         | Hanya `user_actor`.                                                                    |
| `actor.user_agent`    | `http_request.user_agent` | Hanya `user_actor`.                                                                    |
| `actor.service`       | `actor.app_name`          | Hanya `system_actor`.                                                                  |

## Aktivitas atestasi: Entity Management

Petakan aktivitas [`org_security_control_attestation_updated`](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference#attestation-activity) ke kelas OCSF Entity Management (3004). Peristiwa Entity Management melaporkan operasi pada entitas yang dikelola, dalam hal ini atestasi organisasi untuk sebuah kontrol keamanan.

| Field aktivitas   | Atribut OCSF               | Catatan                                                                      |
| ----------------- | -------------------------- | ---------------------------------------------------------------------------- |
| Tidak ada         | `class_uid`                | Konstan: `3004` (Entity Management).                                         |
| Tidak ada         | `category_uid`             | Konstan: `3` (Identity & Access Management).                                 |
| `action`          | `activity_id`              | Dari tabel nilai `action` berikut.                                           |
| `action`          | `unmapped.action`          | Salin tanpa perubahan, karena dua nilai `action` berbagi satu `activity_id`. |
| Tidak ada         | `entity.type_id`           | Konstan: `99` (Other).                                                       |
| Tidak ada         | `entity.type`              | Konstan: `Security control attestation`.                                     |
| `control`         | `entity.uid`               | Salin tanpa perubahan.                                                       |
| `status`          | `entity.data.status`       | Salin tanpa perubahan: nilai atestasi.                                       |
| `review_date`     | `entity.data.review_date`  | Salin tanpa perubahan: tanggal berakhir atestasi.                            |
| `previous_status` | `unmapped.previous_status` | Salin tanpa perubahan: nilai atestasi sebelum perubahan.                     |

Jangan petakan `status` ke `status_id` atau ke nilai lulus atau gagal mana pun: atestasi adalah pernyataan seseorang tentang sebuah kontrol, bukan hasil dari sebuah pemeriksaan.

| `action`            | `activity_id`     | `type_uid` |
| ------------------- | ----------------- | ---------- |
| `attested`          | `1` (Create)      | `300401`   |
| `changed`           | `3` (Update)      | `300403`   |
| `renewed`           | `3` (Update)      | `300403`   |
| `cleared`           | `4` (Delete)      | `300404`   |
| `lapsed`            | `11` (Deactivate) | `300411`   |
| Nilai lain mana pun | `99` (Other)      | `300499`   |

Untuk `99` (Other), setel `activity_name` ke nilai `action`.

Aktivitas `attested` dipetakan ke peristiwa seperti berikut, dengan nilai contoh:

```json
{
  "class_uid": 3004,
  "category_uid": 3,
  "activity_id": 1,
  "type_uid": 300401,
  "severity_id": 1,
  "time": 1794495872517,
  "metadata": {
    "version": "1.6.0",
    "profiles": ["host"],
    "uid": "activity_01Kp5RvNd8Wc3TgMy6BxQf4Z",
    "event_code": "org_security_control_attestation_updated",
    "original_time": "2026-11-12T15:04:32.517208Z",
    "logged_time": 1794495910000,
    "tenant_uid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
    "product": { "vendor_name": "Anthropic", "name": "Compliance API" }
  },
  "actor": {
    "user": {
      "uid": "user_01TuVwXyZaBcDeFgH2JkLmN4",
      "email_addr": "admin@example.com"
    }
  },
  "src_endpoint": { "ip": "192.0.2.34" },
  "http_request": { "user_agent": "ExampleBrowser/1.0" },
  "entity": {
    "type_id": 99,
    "type": "Security control attestation",
    "uid": "mdm_chat_required_organization",
    "data": { "status": "completed" }
  },
  "unmapped": {
    "action": "attested",
    "actor": { "type": "user_actor" },
    "organization_id": "org_01JuY4bkwkH1x4PodBJaWmh2"
  }
}
```
