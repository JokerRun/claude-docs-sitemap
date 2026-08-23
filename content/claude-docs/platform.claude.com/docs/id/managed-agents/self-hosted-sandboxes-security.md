---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security
fetched_at: 2026-08-23T02:32:19.757524Z
sha256: 096950428fea9b14f3a9e763f144bc2cadcb9592278003c4a2e3d211a189f9a5
---

---
title: Model keamanan
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security
description: Model tanggung jawab bersama untuk lingkungan sandbox yang di-hosting sendiri.
---

Anthropic mengamankan control plane di seluruh lingkungan: integritas sesi dan antrean kerja, isolasi multitenant, dan minimisasi konteks agen. Ketika Anda melakukan self-hosting, tanggung jawab berikut berada di tangan Anda.

## Apa yang menjadi tanggung jawab Anda

* **Kualitas image sandbox dan hardening runtime.** Anthropic tidak memeriksa atau memverifikasi image sandbox Anda. Ikuti praktik terbaik seperti menghapus Linux capabilities yang tidak diperlukan, menjalankan sebagai pengguna non-root, dan menggunakan root filesystem read-only.
* **Kontrol egress jaringan.** Akses jaringan sandbox Anda ditentukan oleh aturan VPC dan firewall Anda. Tanpa pembatasan egress, eksekusi alat yang telah disusupi dapat menjangkau host eksternal mana pun. Batasi lalu lintas keluar hanya ke endpoint yang dibutuhkan alat Anda.
* **Penyimpanan dan rotasi service key.** Environment service key (`ANTHROPIC_ENVIRONMENT_KEY`) mengotorisasi polling antrean kerja lingkungan Anda dan pengiriman hasil kembali ke sesi. Simpan kunci ini di secrets manager, bukan di file environment atau image sandbox. Rotasi segera jika Anda mencurigai adanya kebocoran.
* **Mengisolasi beban kerja yang tidak tepercaya.** Environment service key dibatasi cakupannya pada antrean kerja satu lingkungan. Jika Anda menjalankan kode yang tidak tepercaya di dalam sandbox Anda, pertimbangkan untuk menyediakan workspace dan lingkungan terpisah untuk setiap batas kepercayaan. Ini membatasi setiap kunci pada sesi milik satu pengguna saja, bukan kumpulan bersama.
* **Radius dampak eksekusi alat.** Alat berjalan di dalam sandbox Anda dengan izin apa pun yang dimiliki proses Anda. Terapkan prinsip least privilege pada pengguna proses dan mount hanya direktori yang dibutuhkan alat Anda.
* **Retensi log dan konten sesi.** Konten percakapan dan output alat melewati worker Anda dan tetap berada di lingkungan Anda. Anda bertanggung jawab untuk menyimpan, menyunting (redact), atau menghapus data tersebut sesuai dengan kebijakan Anda sendiri. Anthropic tidak memiliki visibilitas terhadap apa yang dilakukan worker Anda dengan konten sesi setelah dikirimkan.

## Apa yang tidak dapat dilakukan Anthropic untuk Anda

* **Mengetahui bahwa kunci Anda bocor.** Anthropic dapat mendeteksi pola penggunaan yang anomali, tetapi tidak dapat mengetahui bahwa kunci Anda telah disusupi. Jika Anda mencurigai `ANTHROPIC_ENVIRONMENT_KEY` bocor, cabut kunci tersebut dan buat penggantinya segera. Pencabutan divalidasi pada setiap permintaan, sehingga berlaku pada pemanggilan worker berikutnya.
* **Memverifikasi build worker Anda.** Anthropic tidak memeriksa image sandbox atau runtime Anda. Kompromi rantai pasokan (supply-chain) pada image Anda tidak dapat dideteksi dari control plane.
* **Mengisolasi alat di dalam sandbox Anda.** Batas keamanan Anthropic berhenti di sandbox. Cara Anda mengisolasi eksekusi alat individual satu sama lain di dalam batas tersebut sepenuhnya merupakan tanggung jawab Anda.
* **Menegakkan retensi data di lingkungan Anda.** Setelah konten sesi mencapai worker Anda, konten tersebut berada di luar kontrol siklus hidup data Anthropic.
