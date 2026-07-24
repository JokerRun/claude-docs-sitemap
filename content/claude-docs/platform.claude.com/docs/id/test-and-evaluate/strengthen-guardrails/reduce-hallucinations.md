---
source: platform
url: https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: b9c2ad65c4e574a78b4314049edfaab3314a6c1fec52c8d1b3acc6f7ea3f6952
---

# Mengurangi halusinasi

Minimalkan halusinasi dalam output Claude dengan mengizinkan ketidakpastian, mendasarkan respons pada kutipan langsung, dan memverifikasi klaim dengan sitasi.

---

Bahkan model bahasa yang paling canggih sekalipun, seperti Claude, terkadang dapat menghasilkan teks yang secara faktual tidak benar atau tidak konsisten dengan konteks yang diberikan. Fenomena ini, yang dikenal sebagai "hallucination" (halusinasi), dapat merusak keandalan solusi berbasis AI Anda. Panduan ini akan mengeksplorasi teknik-teknik untuk meminimalkan halusinasi dan memastikan output Claude akurat dan dapat dipercaya.

## Strategi dasar meminimalkan halusinasi

* **Izinkan Claude untuk mengatakan "Saya tidak tahu":** Secara eksplisit berikan izin kepada Claude untuk mengakui ketidakpastian. Teknik sederhana ini dapat secara drastis mengurangi informasi yang salah.

<Accordion title="Contoh: Menganalisis laporan merger & akuisisi">
  | Peran | Konten                                                                                                                                                                                                                                                                                                                                                                                                 |
  | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  | User  | Sebagai penasihat M\&A kami, analisis laporan ini tentang potensi akuisisi AcmeCo oleh ExampleCorp. \<report> \{\{REPORT}} \</report> Fokus pada proyeksi keuangan, risiko integrasi, dan hambatan regulasi. Jika Anda tidak yakin tentang aspek apa pun atau jika laporan tidak memiliki informasi yang diperlukan, katakan "Saya tidak memiliki cukup informasi untuk menilai hal ini dengan yakin." |
</Accordion>

* **Gunakan kutipan langsung untuk landasan faktual:** Untuk tugas yang melibatkan dokumen panjang (>20k token), minta Claude untuk mengekstrak kutipan kata demi kata terlebih dahulu sebelum melakukan tugasnya. Ini mendasarkan responsnya pada teks yang sebenarnya, sehingga mengurangi halusinasi.

<Accordion title="Contoh: Mengaudit kebijakan privasi data">
  | Peran | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
  | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | User  | Sebagai Data Protection Officer kami, tinjau kebijakan privasi yang diperbarui ini untuk kepatuhan GDPR dan CCPA. \<policy> \{\{POLICY}} \</policy> 1. Ekstrak kutipan persis dari kebijakan yang paling relevan dengan kepatuhan GDPR dan CCPA. Jika Anda tidak dapat menemukan kutipan yang relevan, nyatakan "Tidak ditemukan kutipan yang relevan." 2. Gunakan kutipan tersebut untuk menganalisis kepatuhan bagian-bagian kebijakan ini, dengan merujuk kutipan berdasarkan nomor. Dasarkan analisis Anda hanya pada kutipan yang diekstrak. |
</Accordion>

* **Verifikasi dengan sitasi**: Buat respons Claude dapat diaudit dengan memintanya mengutip kutipan dan sumber untuk setiap klaimnya. Anda juga dapat meminta Claude memverifikasi setiap klaim dengan menemukan kutipan pendukung setelah menghasilkan respons. Jika tidak dapat menemukan kutipan, Claude harus menarik kembali klaim tersebut.

<Accordion title="Contoh: Menyusun siaran pers tentang peluncuran produk">
  | Peran | Konten                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
  | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  | User  | Susun siaran pers untuk produk keamanan siber baru kami, AcmeSecurity Pro, hanya menggunakan informasi dari ringkasan produk dan laporan pasar ini. \<documents> \{\{DOCUMENTS}} \</documents> Setelah menyusun, tinjau setiap klaim dalam siaran pers Anda. Untuk setiap klaim, temukan kutipan langsung dari dokumen yang mendukungnya. Jika Anda tidak dapat menemukan kutipan pendukung untuk suatu klaim, hapus klaim tersebut dari siaran pers dan tandai tempat klaim itu dihapus dengan tanda kurung kosong \[]. |
</Accordion>

***

## Teknik lanjutan

* **Verifikasi chain-of-thought**: Minta Claude untuk menjelaskan penalarannya langkah demi langkah sebelum memberikan jawaban akhir. Ini dapat mengungkap logika atau asumsi yang keliru.

* **Verifikasi best-of-N**: Jalankan Claude melalui prompt yang sama beberapa kali dan bandingkan output-nya. Ketidakkonsistenan di antara output dapat mengindikasikan halusinasi.

* **Penyempurnaan iteratif**: Gunakan output Claude sebagai input untuk prompt lanjutan, dengan memintanya memverifikasi atau memperluas pernyataan sebelumnya. Ini dapat menangkap dan memperbaiki ketidakkonsistenan.

* **Pembatasan pengetahuan eksternal**: Secara eksplisit instruksikan Claude untuk hanya menggunakan informasi dari dokumen yang disediakan dan bukan pengetahuan umumnya.

<Note>
  Ingat, meskipun teknik-teknik ini secara signifikan mengurangi halusinasi, teknik-teknik tersebut tidak menghilangkannya sepenuhnya. Selalu validasi informasi penting, terutama untuk keputusan berisiko tinggi.
</Note>
