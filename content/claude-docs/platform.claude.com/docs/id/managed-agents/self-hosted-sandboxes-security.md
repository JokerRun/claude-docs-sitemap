---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 0a42bc7a2ef90cba84b4408a0a545b10b1d0417a3db0418d242a2018d036c543
---

# Model keamanan

Model tanggung jawab bersama untuk lingkungan sandbox yang di-hosting sendiri.

---

Anthropic mengamankan control plane di semua lingkungan: integritas sesi dan antrean kerja, isolasi multitenant, dan minimalisasi konteks agen. Ketika Anda melakukan self-hosting, tanggung jawab berikut menjadi milik Anda.

## Apa yang menjadi tanggung jawab Anda

* **Kualitas image sandbox dan hardening runtime.** Anthropic tidak memeriksa atau memverifikasi image sandbox Anda. Ikuti praktik terbaik seperti menghapus Linux capabilities yang tidak diperlukan, berjalan sebagai pengguna non-root, dan menggunakan root filesystem yang bersifat read-only.
* **Kontrol egress jaringan.** Akses jaringan sandbox Anda ditentukan oleh VPC dan aturan firewall Anda. Tanpa pembatasan egress, eksekusi alat yang telah disusupi dapat menjangkau host eksternal mana pun. Batasi lalu lintas keluar hanya ke endpoint yang dibutuhkan oleh alat Anda.
* **Penyimpanan dan rotasi service key.** Environment service key (`ANTHROPIC_ENVIRONMENT_KEY`) mengotorisasi polling antrean kerja lingkungan Anda dan pengiriman hasil kembali ke sesi. Simpan di secrets manager, bukan di file environment atau image sandbox. Rotasi segera jika Anda mencurigai adanya paparan.
* **Mengisolasi beban kerja yang tidak tepercaya.** Environment service key dibatasi cakupannya pada antrean kerja satu lingkungan. Jika Anda menjalankan kode yang tidak tepercaya di dalam sandbox Anda, pertimbangkan untuk menyediakan workspace dan lingkungan terpisah untuk setiap batas kepercayaan. Ini membatasi setiap key hanya pada sesi satu pengguna alih-alih pool bersama.
* **Blast radius eksekusi alat.** Alat berjalan di dalam sandbox Anda dengan izin apa pun yang dimiliki proses Anda. Terapkan prinsip least privilege pada pengguna proses dan mount hanya direktori yang dibutuhkan oleh alat Anda.
* **Retensi log dan konten sesi.** Konten percakapan dan output alat melewati worker Anda dan tetap berada di lingkungan Anda. Anda bertanggung jawab untuk menyimpan, menyunting, atau menghapus data tersebut sesuai dengan kebijakan Anda sendiri. Anthropic tidak memiliki visibilitas terhadap apa yang dilakukan worker Anda dengan konten sesi setelah dikirimkan.

## Apa yang tidak dapat dilakukan Anthropic untuk Anda

* **Mengetahui bahwa key Anda bocor.** Anthropic dapat mendeteksi pola penggunaan yang anomali, tetapi tidak dapat mengetahui bahwa key Anda telah disusupi. Jika Anda mencurigai `ANTHROPIC_ENVIRONMENT_KEY` bocor, cabut dan buat penggantinya segera. Pencabutan divalidasi pada setiap permintaan, sehingga berlaku pada panggilan worker berikutnya.
* **Memverifikasi build worker Anda.** Anthropic tidak memeriksa image sandbox atau runtime Anda. Penyusupan supply-chain pada image Anda tidak dapat dideteksi dari control plane.
* **Mengisolasi alat di dalam sandbox Anda.** Batas keamanan Anthropic berhenti di sandbox. Bagaimana Anda mengisolasi eksekusi alat individual satu sama lain di dalam batas tersebut sepenuhnya menjadi tanggung jawab Anda.
* **Menegakkan retensi data di lingkungan Anda.** Setelah konten sesi mencapai worker Anda, konten tersebut berada di luar kontrol siklus hidup data Anthropic.
