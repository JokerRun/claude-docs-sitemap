---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/detect-changes
fetched_at: 2026-11-11T02:12:04.616753Z
sha256: fbebf70dd0991f0d2615ee434a9a57f6985d17b8323e2bba31f3237051fd3dff
---

---
title: Mendeteksi perubahan pada Security posture
url: https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/detect-changes
description: "Mulailah dari contoh aturan deteksi untuk aktivitas Security posture di SIEM Anda: risiko diterima, kontrol yang diatestasi sebagai Gagal, pengedit yang tidak terduga, lonjakan perubahan, dan atestasi yang berhenti berlaku secara otomatis."
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

Contoh aturan ini memberi peringatan saat terjadi perubahan pada [Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview) organisasi Anda, menggunakan aktivitas yang dicatat oleh Activity Feed Compliance API. Aturan ini mengasumsikan bahwa sistem security information and event management (SIEM) Anda menyimpan aktivitas tersebut, seperti yang dijelaskan di [Mengirim peristiwa ke SIEM Anda](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/send-events).

## Sebelum Anda menulis aturan

Setiap aturan berupa deskripsi sederhana dan kueri yang tidak terikat pada bahasa kueri tertentu.

* Kueri menggunakan nama field Activity Feed, ditambah `stored_at`, yaitu nama yang digunakan halaman ini untuk waktu Anda menyimpan suatu aktivitas. Nama lain mana pun adalah daftar atau alias milik Anda sendiri.
* Sebelum aturan menghitung aktivitas, lakukan deduplikasi aktivitas tersebut berdasarkan `id`.
* Kecuali suatu aturan menyatakan lain, jalankan aturan tersebut pada rentang waktu sejak eksekusi terakhirnya yang selesai, berdasarkan `stored_at`, bukan `created_at`, karena suatu aktivitas dapat tiba terlambat; kueri tidak menyertakan rentang tersebut.
* Tulis aturan yang terpicu oleh aktivitas yang telah Anda simpan, jangan pernah oleh aktivitas yang belum Anda simpan: aktivitas itu mungkin terlambat, atau merupakan perubahan yang [tidak dicatat oleh feed](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference#what-the-feed-does-not-record). Untuk membandingkan aktivitas yang tersimpan dengan hasil saat ini, lihat [Mencocokkan peristiwa dengan hasil](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/check-events-against-results).

## Aturan atestasi

Kelima aturan ini membaca aktivitas [`org_security_control_attestation_updated`](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference#attestation-activity).

### Risiko diterima

Beri peringatan saat seseorang menerima risiko (`accepted_risk`) karena tidak memenuhi suatu kontrol keamanan, agar orang kedua dapat meninjau keputusan tersebut.

```sql
type == "org_security_control_attestation_updated"
AND status == "accepted_risk"
AND actor.type != "system_actor"
```

Aturan ini mengecualikan `system_actor`, karena perubahan otomatis, seperti atestasi yang berhenti berlaku (`lapsed`), mempertahankan `status` tetapi bukan merupakan penerimaan risiko.

### Kontrol diatestasi sebagai Gagal

Beri peringatan saat seseorang mengatestasi suatu kontrol sebagai Gagal (`control_failed`), agar seseorang menindaklanjuti kontrol tersebut.

```sql
type == "org_security_control_attestation_updated"
AND status == "control_failed"
AND actor.type != "system_actor"
```

Aturan ini mengecualikan `system_actor` dengan alasan yang sama seperti pada [Risiko diterima](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/detect-changes#a-risk-was-accepted).

### Seseorang di luar allowlist mengubah atestasi

Beri peringatan saat suatu atestasi dicatat, diubah, disimpan ulang, atau dicabut oleh seseorang yang tidak ada dalam daftar orang yang mengelola atestasi milik Anda. Simpan nilai `user_id` mereka (`allowed_user_ids`) di SIEM Anda.

```sql
type == "org_security_control_attestation_updated"
AND actor.type != "system_actor"
AND NOT (actor.type == "user_actor" AND actor.user_id IN allowed_user_ids)
```

* Aktor mana pun selain `user_actor` yang terdaftar atau `system_actor` akan memicu aturan ini.
* Pastikan daftar diidentifikasi berdasarkan `actor.user_id`: `actor.email_address` adalah alamat yang dimiliki orang tersebut saat aktivitas dicatat ([Korelasikan dengan SIEM Anda](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#correlate-with-your-siem)).

### Satu orang membuat banyak perubahan atestasi

Beri peringatan saat satu orang membuat lebih banyak perubahan atestasi dalam waktu singkat daripada yang biasa terjadi di organisasi Anda. Ambang batas 10 dan rentang 1 jam hanyalah contoh; tentukan keduanya berdasarkan aktivitas Anda sendiri.

```sql
type == "org_security_control_attestation_updated"
AND actor.type == "user_actor"
| group by organization_uuid, actor.user_id over a sliding 1 hour of created_at
| where count(distinct id) >= 10
```

* Kirim peringatan hanya untuk grup yang memuat aktivitas yang disimpan sejak eksekusi terakhir aturan, dan hitung atas setiap aktivitas yang telah Anda simpan, agar aktivitas yang terlambat tergabung ke dalam lonjakan yang aktivitas lainnya telah Anda simpan sebelumnya.
* Menghitung berdasarkan `created_at` mengukur laju orang tersebut, bukan laju ingesti Anda.

### Atestasi berhenti berlaku secara otomatis

Perlakukan aktivitas `lapsed` sebagai dorongan untuk meninjau kontrol yang disebutkannya.

```sql
type == "org_security_control_attestation_updated"
AND action == "lapsed"
```

[Aktivitas `lapsed`](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference#what-a-lapsed-activity-means) berarti bahwa hasil pemeriksaan kontrol atau nilai saat ini berbeda dari yang berlaku saat atestasi disimpan, bukan berarti tanggal berakhir (`review_date`) telah lewat. Aktivitas ini dapat datang terlambat.

## Menjaga aturan tetap berfungsi saat nilai berubah

Nilai baru dapat muncul di salah satu field ini.

* Identifikasi perubahan otomatis berdasarkan `actor.type`, bukan berdasarkan nilai `actor.service`.
* Jangan membuang aktivitas yang nilai `control`, `action`, atau `status`-nya tidak tercantum dalam aturan; nilai `action` yang baru dapat mencatat penerimaan risiko. Lihat [Referensi peristiwa](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference).

## Menguji aturan

Untuk melihat [aturan allowlist](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/detect-changes#someone-outside-an-allowlist-changed-an-attestation) terpicu, pilih seseorang yang dapat melakukan atestasi dan yang tidak ada dalam daftar Anda. Mintalah orang tersebut mengatestasi suatu kontrol yang belum memiliki atestasi dan hasilnya tidak diandalkan oleh siapa pun, lalu mencabut atestasi tersebut. Sampai atestasi dicabut, atestasi tersebut dapat mengubah hasil kontrol itu. Kedua aktivitas mungkin memerlukan waktu beberapa saat untuk mencapai Activity Feed.

Jika Anda menyimpan aktivitas ini sebagai peristiwa Open Cybersecurity Schema Framework (OCSF), [Memetakan peristiwa Security posture ke OCSF](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/ocsf-mapping) memetakan field-fieldnya.
