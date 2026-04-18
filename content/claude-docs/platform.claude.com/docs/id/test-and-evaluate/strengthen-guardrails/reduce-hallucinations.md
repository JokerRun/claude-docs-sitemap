---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: b18fd1e88fcd3193a3e6d7c6b17ef30801df9496d139a38e68ac533593baca5a
---

# Mengurangi halusinasi

Teknik untuk meminimalkan halusinasi dan memastikan output Claude akurat dan dapat dipercaya.

---

Bahkan model bahasa paling canggih sekalipun, seperti Claude, kadang-kadang dapat menghasilkan teks yang faktanya salah atau tidak konsisten dengan konteks yang diberikan. Fenomena ini, yang dikenal sebagai "halusinasi," dapat merusak keandalan solusi berbasis AI Anda.
Panduan ini akan mengeksplorasi teknik untuk meminimalkan halusinasi dan memastikan output Claude akurat dan dapat dipercaya.

## Strategi minimalisasi halusinasi dasar

- **Izinkan Claude untuk mengatakan "Saya tidak tahu":** Secara eksplisit berikan izin kepada Claude untuk mengakui ketidakpastian. Teknik sederhana ini dapat drastis mengurangi informasi palsu.

<section title="Contoh: Menganalisis laporan merger & akuisisi">

| Peran | Konten |
| ---- | ------- |
| Pengguna | Sebagai penasihat M&A kami, analisis laporan ini tentang potensi akuisisi AcmeCo oleh ExampleCorp.<br/><br/>\<report><br/>\{\{REPORT}}<br/>\</report><br/><br/>Fokus pada proyeksi keuangan, risiko integrasi, dan hambatan regulasi. Jika Anda tidak yakin tentang aspek apa pun atau jika laporan kekurangan informasi yang diperlukan, katakan "Saya tidak memiliki informasi yang cukup untuk menilai ini dengan percaya diri." |

</section>

- **Gunakan kutipan langsung untuk penjangkaran faktual:** Untuk tugas yang melibatkan dokumen panjang (>20k token), minta Claude untuk mengekstrak kutipan kata demi kata terlebih dahulu sebelum melakukan tugasnya. Ini mendasarkan responsnya pada teks aktual, mengurangi halusinasi.

<section title="Contoh: Mengaudit kebijakan privasi data">

| Peran | Konten |
| ---- | ------- |
| Pengguna | Sebagai Petugas Perlindungan Data kami, tinjau kebijakan privasi yang diperbarui ini untuk kepatuhan GDPR dan CCPA.<br/>\<br/>\{\{POLICY}}<br/>\</policy><br/><br/>1. Ekstrak kutipan tepat dari kebijakan yang paling relevan dengan kepatuhan GDPR dan CCPA. Jika Anda tidak dapat menemukan kutipan yang relevan, nyatakan "Tidak ada kutipan yang relevan ditemukan."<br/><br/>2. Gunakan kutipan untuk menganalisis kepatuhan bagian kebijakan ini, merujuk kutipan berdasarkan nomor. Hanya dasarkan analisis Anda pada kutipan yang diekstrak. |

</section>

- **Verifikasi dengan kutipan**: Buat respons Claude dapat diaudit dengan memintanya mengutip dan merujuk sumber untuk setiap klaim yang dibuatnya. Anda juga dapat meminta Claude untuk memverifikasi setiap klaim dengan menemukan kutipan pendukung setelah menghasilkan respons. Jika tidak dapat menemukan kutipan, Claude harus menarik kembali klaim tersebut.

<section title="Contoh: Menyusun siaran pers tentang peluncuran produk">

| Peran | Konten |
| ---- | ------- |
| Pengguna | Susun siaran pers untuk produk keamanan siber baru kami, AcmeSecurity Pro, hanya menggunakan informasi dari ringkasan produk dan laporan pasar ini.<br/>\<documents><br/>\{\{DOCUMENTS}}<br/>\</documents><br/><br/>Setelah menyusun, tinjau setiap klaim dalam siaran pers Anda. Untuk setiap klaim, temukan kutipan langsung dari dokumen yang mendukungnya. Jika Anda tidak dapat menemukan kutipan pendukung untuk klaim, hapus klaim tersebut dari siaran pers dan tandai tempat penghapusannya dengan tanda kurung kosong []. |

</section>

***

## Teknik lanjutan

- **Verifikasi rantai pemikiran**: Minta Claude untuk menjelaskan penalarannya langkah demi langkah sebelum memberikan jawaban akhir. Ini dapat mengungkapkan logika atau asumsi yang cacat.

- **Verifikasi terbaik-dari-N**: Jalankan Claude melalui prompt yang sama beberapa kali dan bandingkan hasilnya. Ketidakkonsistenan di seluruh output dapat menunjukkan halusinasi.

- **Penyempurnaan iteratif**: Gunakan output Claude sebagai input untuk prompt tindak lanjut, minta untuk memverifikasi atau memperluas pernyataan sebelumnya. Ini dapat menangkap dan memperbaiki ketidakkonsistenan.

- **Pembatasan pengetahuan eksternal**: Secara eksplisit instruksikan Claude untuk hanya menggunakan informasi dari dokumen yang disediakan dan bukan pengetahuan umum.

<Note>Ingat, meskipun teknik ini secara signifikan mengurangi halusinasi, mereka tidak menghilangkannya sepenuhnya. Selalu validasi informasi kritis, terutama untuk keputusan yang berisiko tinggi.</Note>