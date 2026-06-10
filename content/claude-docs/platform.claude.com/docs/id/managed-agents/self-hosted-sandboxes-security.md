---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: f09197132be4ee43a8544e9239fb565cd8efb9daefdc508f542ec85d3e42fef3
---

# Model keamanan

Model tanggung jawab bersama untuk lingkungan sandbox yang di-host sendiri.

---

Anthropic mengamankan "control plane" (bidang kontrol) di seluruh lingkungan: integritas sesi dan antrean kerja, isolasi multi-tenant, dan minimalisasi konteks agen. Ketika Anda melakukan self-hosting, tanggung jawab berikut menjadi milik Anda.

## Apa yang menjadi tanggung jawab Anda \{#what-you-own}

- **Kualitas image sandbox dan pengerasan runtime.** Anthropic tidak memeriksa atau memverifikasi image sandbox Anda. Ikuti praktik terbaik seperti menghapus kapabilitas Linux yang tidak diperlukan, menjalankan sebagai pengguna non-root, dan menggunakan filesystem root yang bersifat read-only.
- **Kontrol egress jaringan.** Akses jaringan sandbox Anda ditentukan oleh VPC dan aturan firewall Anda. Tanpa pembatasan egress, eksekusi alat yang telah disusupi dapat menjangkau host eksternal mana pun. Batasi lalu lintas keluar hanya ke endpoint yang dibutuhkan oleh alat Anda.
- **Penyimpanan dan rotasi kunci layanan.** Kunci layanan lingkungan (`ANTHROPIC_ENVIRONMENT_KEY`) mengotorisasi polling antrean kerja lingkungan Anda dan pengiriman hasil kembali ke sesi. Simpan kunci ini di secrets manager, bukan di file lingkungan atau image sandbox. Segera lakukan rotasi jika Anda mencurigai adanya kebocoran.
- **Mengisolasi beban kerja yang tidak tepercaya.** Kunci layanan lingkungan dibatasi cakupannya pada antrean kerja satu lingkungan. Jika Anda menjalankan kode yang tidak tepercaya di dalam sandbox Anda, pertimbangkan untuk menyediakan workspace dan lingkungan terpisah untuk setiap batas kepercayaan. Hal ini membatasi setiap kunci hanya pada sesi satu pengguna, bukan pada kumpulan bersama.
- **Radius dampak eksekusi alat.** Alat berjalan di dalam sandbox Anda dengan izin apa pun yang dimiliki proses Anda. Terapkan prinsip hak akses minimal (least privilege) pada pengguna proses dan hanya mount direktori yang dibutuhkan oleh alat Anda.
- **Retensi log dan konten sesi.** Konten percakapan dan output alat melewati worker Anda dan tetap berada di lingkungan Anda. Anda bertanggung jawab untuk menyimpan, meredaksi, atau menghapus data tersebut sesuai dengan kebijakan Anda sendiri. Anthropic tidak memiliki visibilitas terhadap apa yang dilakukan worker Anda dengan konten sesi setelah dikirimkan.

## Apa yang tidak dapat dilakukan Anthropic untuk Anda \{#what-anthropic-cannot-do-for-you}

- **Membatalkan kunci yang bocor secara instan.** Anthropic dapat mendeteksi pola penggunaan yang anomali, tetapi tidak dapat membatalkan kunci secara instan. Perlakukan `ANTHROPIC_ENVIRONMENT_KEY` seperti kata sandi database: segera lakukan rotasi jika disusupi.
- **Memverifikasi build worker Anda.** Anthropic tidak memeriksa image sandbox atau runtime Anda. Penyusupan rantai pasokan (supply-chain) pada image Anda tidak dapat dideteksi dari control plane.
- **Mengisolasi alat di dalam sandbox Anda.** Batas keamanan Anthropic berhenti di sandbox. Bagaimana Anda mengisolasi eksekusi alat individual satu sama lain di dalam batas tersebut sepenuhnya menjadi tanggung jawab Anda.
- **Menegakkan retensi data di lingkungan Anda.** Setelah konten sesi mencapai worker Anda, konten tersebut berada di luar kontrol siklus hidup data Anthropic.