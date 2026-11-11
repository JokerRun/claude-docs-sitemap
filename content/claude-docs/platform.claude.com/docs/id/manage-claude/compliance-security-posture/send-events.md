---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/send-events
fetched_at: 2026-11-11T02:12:04.616753Z
sha256: 5d2ab3a845c5b008830c154a3e33fee351cbc256510102baeccde3c6d1f44212
---

---
title: Mengirim peristiwa Security posture ke SIEM Anda
url: https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/send-events
description: Minta aktivitas Security posture dari Activity Feed Compliance API, baca salah satunya field demi field, dan jaga SIEM Anda tetap mutakhir dengan pembacaan terjadwal yang menangkap aktivitas yang terlambat.
---

<Note>
  Untuk mengaktifkan Compliance API, lihat [Menyiapkan Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api-access).
</Note>

Halaman ini memandu Anda mulai dari Compliance Access Key hingga aktivitas Security posture tiba secara terjadwal sebagai peristiwa di sistem security information and event management (SIEM) Anda. Ikhtisar menjelaskan [organisasi mana yang memiliki aktivitas ini](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#availability). Anda memerlukan Compliance Access Key yang mencakup organisasi tersebut, dengan scope `read:compliance_activities` atau `read:org_audit`.

## Meminta aktivitas

Untuk membaca hanya aktivitas ini, filter feed dengan `activity_types[]`. Dalam permintaan ini, `created_at.gte` menetapkan `created_at` paling awal yang dibaca, dan `order=asc` mengembalikan aktivitas terlama terlebih dahulu:

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/activities" \
  -H "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  -H "anthropic-version: 2026-10-21" \
  --data-urlencode "activity_types[]=org_security_control_attestation_updated" \
  --data-urlencode "created_at.gte=2026-10-20T00:00:00Z" \
  --data-urlencode "order=asc" \
  --data-urlencode "limit=5000"
```

[Referensi API](https://platform.claude.com/docs/id/api/compliance/activities/list) menjelaskan setiap parameter.

## Membaca satu aktivitas

Setiap elemen array `data` dalam respons adalah aktivitas seperti ini.

```json
{
  "id": "activity_01Hq7ZtYc4Vb2NmKx8RsPd3W",
  "type": "org_security_control_attestation_updated",
  "created_at": "2026-10-20T15:04:00.220114Z",
  "organization_id": "org_01JuY4bkwkH1x4PodBJaWmh2",
  "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
  "actor": {
    "type": "user_actor",
    "email_address": "jane.doe@example.com",
    "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
    "ip_address": "192.0.2.34",
    "user_agent": "Mozilla/5.0..."
  },
  "control": "directory_sync_enabled",
  "action": "attested",
  "status": "accepted_risk"
}
```

* `control` menyebutkan [kontrol keamanan](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#controls), yaitu satu pengaturan atau praktik yang direkomendasikan.
* `action` menyatakan apa yang terjadi pada [atestasi kontrol tersebut](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#attestations), yaitu pernyataan tercatat seseorang tentang kontrol itu. Di sini `attested` berarti satu atestasi dicatat untuk kontrol yang sebelumnya tidak memilikinya.
* `status` adalah nilai atestasi. Di sini nilainya Risiko diterima (`accepted_risk`): kontrol tersebut tidak diterapkan, dan organisasi menerima risikonya.
* `actor` di sini mengidentifikasi [orang yang memberikan atestasi](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#who-can-see-who-attested), berdasarkan ID pengguna dan alamat email.
* `created_at` di sini adalah waktu mereka memberikan atestasi.

[Referensi peristiwa Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference) mencantumkan lebih banyak field dan nilai.

## Jika respons kosong

Array `data` yang kosong adalah valid. Feed hanya memuat perubahan yang dibuat sejak feed [mulai mencatat aktivitas ini untuk organisasi tersebut](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference#what-the-feed-does-not-record). Feed tetap kosong sampai ada atestasi yang dibuat atau diubah.

Periksa bahwa organisasi tersebut [memiliki aktivitas ini](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/overview#availability). Kemudian minta seseorang memberikan atestasi pada sebuah kontrol. Setelah beberapa saat, ulangi permintaan.

## Menjalankannya secara terjadwal

Salah satu dari aktivitas ini dapat tersedia untuk dikueri lebih lambat daripada [jeda pengindeksan](https://platform.claude.com/docs/id/manage-claude/compliance-integration-patterns#window-polling) Activity Feed yang biasanya 1 menit, dengan `created_at` yang sudah berada di masa lalu. Jadi integrasi yang hanya bergerak maju, dari kursor atau `created_at.gte` yang terus maju, tidak pernah melihat aktivitas seperti itu. Baca ulang rentang waktu mundur tetap selama 4 jam pada setiap eksekusi, dan buang aktivitas yang sudah Anda simpan:

```text
query = activity_types[]=org_security_control_attestation_updated
      & created_at.gte={now - 4 hours}
      & order=asc
      & limit=5000
cursor = null
loop:
  if cursor is null:
    page = GET /v1/compliance/activities?{query}
  else:
    page = GET /v1/compliance/activities?{query}&after_id={cursor}
  for activity in page.data:
    if activity.id is not in stored_ids:
      store(activity)
      add activity.id to stored_ids
  if not page.has_more: break
  cursor = page.last_id
```

* **Jalankan secara rutin:** Jalankan loop sesering yang dibutuhkan peringatan Anda, misalnya setiap 5 menit.
* **Gunakan kueri yang sama untuk seluruh eksekusi:** Hitung `created_at.gte`, dalam UTC dan ter-encode URL, di awal setiap eksekusi. Kirim filter dan `order` yang sama di setiap halaman. Dengan `order=asc`, meneruskan `last_id` sebagai `after_id` mengembalikan halaman berikutnya berisi aktivitas yang lebih baru. [Memaginasi hasil](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#paginate-results) menjelaskan `after_id` dan `last_id`.
* **Lakukan deduplikasi berdasarkan `id`:** Langkah ini wajib, karena eksekusi yang berurutan saling tumpang tindih.
* **Menangani eksekusi yang gagal:** Jika sebuah permintaan gagal setelah percobaan ulang dalam [Menangani error Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-errors), hentikan eksekusi. Eksekusi berikutnya membaca seluruh rentangnya lagi. Jika eksekusi gagal atau berhenti selama lebih dari 4 jam, [pembacaan ulang harian](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/send-events#re-read-15-days-once-a-day) berikutnya membaca aktivitas yang dilewatkan oleh eksekusi tersebut.

## Membaca ulang rentang 15 hari, sekali sehari

Sekali sehari, jalankan loop yang sama dengan rentang waktu mundur 15 hari sebagai pengganti 4 jam. Pembacaan ulang harian ini juga membaca aktivitas yang menjadi bisa dikueri hingga 14 hari setelah `created_at`-nya.

* Catat waktu mulai setiap pembacaan ulang harian yang selesai.
* Hapus `id` yang tersimpan hanya jika Anda menyimpannya lebih dari 16 hari sebelum waktu mulai tercatat yang terakhir.
* Jika belum ada waktu mulai yang tercatat, tetapkan `created_at.gte` sejauh ke belakang yang Anda perlukan; feed menyimpan aktivitas selama 6 tahun.
* Jika sudah lebih dari sehari berlalu sejak waktu mulai tercatat yang terakhir, jalankan pembacaan ulang harian berikutnya dengan `created_at.gte` ditetapkan ke 15 hari sebelum waktu mulai tersebut.

## Jika Anda sudah menyerap seluruh feed

Integrasi yang membaca seluruh Activity Feed, tanpa filter `activity_types[]` yang mengecualikan aktivitas ini, sudah menerimanya. Periksa dua hal:

* **Nilai yang tidak dikenali:** Handler Anda meneruskan apa adanya `type` atau [nilai field](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/events-reference) mana pun yang tidak dikenalinya. Lihat [Memahami objek Activity](https://platform.claude.com/docs/id/manage-claude/compliance-activity-feed#understand-the-activity-object).
* **Aktivitas yang terlambat:** Integrasi yang hanya meminta aktivitas yang lebih baru akan melewatkan aktivitas yang baru dapat dikueri belakangan. Tambahkan [pembacaan ulang 4 jam](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/send-events#run-it-on-a-schedule) dan [pembacaan ulang harian 15 hari](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/send-events#re-read-15-days-once-a-day) ke integrasi tersebut.

## Memeriksa bahwa semuanya berfungsi

Setelah seseorang mengatestasi sebuah kontrol, jalankan loop hingga loop tersebut menyimpan aktivitas baru itu. Lalu jalankan lagi: loop tidak menyimpan aktivitas tersebut untuk kedua kalinya.

## Langkah selanjutnya

Untuk memberikan peringatan berdasarkan waktu Anda menyimpan aktivitas, bukan berdasarkan `created_at`-nya, lihat [Mendeteksi perubahan pada Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/detect-changes#before-you-write-a-rule). Untuk Open Cybersecurity Schema Framework (OCSF), lihat [Memetakan peristiwa Security posture ke OCSF](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/ocsf-mapping). Untuk hasil saat ini, lihat [Referensi hasil Security posture](https://platform.claude.com/docs/id/manage-claude/compliance-security-posture/results-reference).
