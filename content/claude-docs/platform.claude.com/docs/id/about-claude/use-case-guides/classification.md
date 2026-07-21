---
source: platform
url: https://platform.claude.com/docs/id/about-claude/use-case-guides/classification
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 5579487a487fe9991c7f3c2e0f50539a4f698b3093e1ad306df7db728654aee9
---

# Klasifikasi

Claude unggul dalam memproses, memahami, dan mengenali pola dalam teks, gambar, dan data. Kemampuan ini membuat Claude sangat andal untuk tugas klasifikasi.

---

Panduan ini menjelaskan proses menentukan pendekatan terbaik untuk membangun pengklasifikasi dengan Claude serta hal-hal penting dalam penerapan end-to-end untuk pengklasifikasi Claude, mulai dari eksplorasi kasus penggunaan hingga integrasi back-end. <Tip>
  Kunjungi&#x20;

  [cookbook klasifikasi](https://platform.claude.com/cookbook/capabilities-classification-guide)

  &#x20;untuk melihat contoh implementasi klasifikasi menggunakan Claude.
</Tip>

## Kapan menggunakan Claude untuk klasifikasi

Kapan Anda sebaiknya mempertimbangkan penggunaan LLM alih-alih pendekatan ML tradisional untuk tugas klasifikasi Anda? Berikut beberapa indikator utamanya:

1. **Kelas berbasis aturan**: Gunakan Claude ketika kelas didefinisikan oleh kondisi, bukan oleh contoh, karena Claude dapat memahami aturan yang mendasarinya.
2. **Kelas yang terus berkembang**: Claude beradaptasi dengan baik pada domain baru atau yang berubah dengan kelas yang baru muncul dan batasan yang bergeser.
3. **Input tidak terstruktur**: Claude dapat menangani input teks tidak terstruktur dalam volume besar dengan panjang yang bervariasi.
4. **Contoh berlabel yang terbatas**: Dengan kemampuan "few-shot learning" (pembelajaran dari sedikit contoh), Claude belajar secara akurat dari data pelatihan berlabel yang terbatas.
5. **Kebutuhan penalaran**: Claude unggul dalam tugas klasifikasi yang memerlukan pemahaman semantik, konteks, dan penalaran tingkat tinggi.

***

## Tetapkan kasus penggunaan klasifikasi Anda

Di bawah ini adalah daftar tidak lengkap dari kasus penggunaan klasifikasi umum di mana Claude unggul, berdasarkan industri.

<AccordionGroup>
  <Accordion title="Teknologi & TI">
    * **Moderasi konten**: secara otomatis mengidentifikasi dan menandai konten yang tidak pantas, ofensif, atau berbahaya dalam teks, gambar, atau video buatan pengguna.
    * **Prioritisasi bug**: mengklasifikasikan laporan bug perangkat lunak berdasarkan tingkat keparahan, dampak, atau kompleksitasnya untuk memprioritaskan upaya pengembangan dan mengalokasikan sumber daya secara efektif.
  </Accordion>

  <Accordion title="Layanan Pelanggan">
    * **Analisis intent**: menentukan apa yang ingin dicapai pengguna atau tindakan apa yang mereka inginkan agar dilakukan sistem berdasarkan input teks mereka.
    * **Perutean tiket dukungan**: menganalisis interaksi pelanggan, seperti transkrip pusat panggilan atau tiket dukungan, untuk merutekan masalah ke tim yang tepat, memprioritaskan kasus kritis, dan mengidentifikasi masalah berulang untuk penyelesaian proaktif.
  </Accordion>

  <Accordion title="Layanan Kesehatan">
    * **Triase pasien**: mengklasifikasikan percakapan dan data penerimaan pelanggan berdasarkan urgensi, topik, atau keahlian yang diperlukan untuk triase yang efisien.
    * **Penyaringan uji klinis**: menganalisis data pasien dan rekam medis untuk mengidentifikasi dan mengategorikan peserta yang memenuhi syarat berdasarkan kriteria inklusi dan eksklusi yang ditentukan.
  </Accordion>

  <Accordion title="Keuangan">
    * **Deteksi penipuan**: mengidentifikasi pola mencurigakan atau anomali dalam transaksi keuangan, klaim asuransi, atau perilaku pengguna untuk mencegah dan memitigasi aktivitas penipuan.
    * **Penilaian risiko kredit**: mengklasifikasikan pemohon pinjaman berdasarkan kelayakan kredit mereka ke dalam kategori risiko untuk mengotomatiskan keputusan kredit dan mengoptimalkan proses pemberian pinjaman.
  </Accordion>

  <Accordion title="Hukum">
    * **Kategorisasi dokumen hukum**: mengklasifikasikan dokumen hukum, seperti pleading, mosi, brief, atau memorandum, berdasarkan jenis dokumen, tujuan, atau relevansinya dengan kasus atau klien tertentu.
  </Accordion>
</AccordionGroup>

***

## Mengimplementasikan Claude untuk klasifikasi

Tiga faktor utama dalam keputusan pemilihan model adalah: kecerdasan, "latency" (latensi), dan harga.

Untuk klasifikasi, model yang lebih kecil seperti Claude Haiku 4.5 biasanya ideal karena kecepatan dan efisiensinya. Namun, untuk tugas klasifikasi yang memerlukan pengetahuan khusus atau penalaran kompleks, Sonnet atau Opus mungkin menjadi pilihan yang lebih baik. Pelajari lebih lanjut tentang perbandingan Opus, Sonnet, dan Haiku di [ikhtisar model](/docs/id/about-claude/models).

Gunakan evaluasi untuk mengukur apakah model Claude berkinerja cukup baik untuk diluncurkan ke produksi.

### 1. Bangun prompt input yang kuat

Meskipun Claude menawarkan performa dasar tingkat tinggi secara langsung, prompt input yang kuat membantu mendapatkan hasil terbaik.

Untuk pengklasifikasi generik yang dapat Anda sesuaikan dengan kasus penggunaan spesifik Anda, salin prompt awal di bawah ini:

<Accordion title="Prompt awal">
  ```text wrap
  You will be building a text classifier that can automatically categorize text into a set of predefined categories.
  Here are the categories the classifier will use:

  <categories>
  {{CATEGORIES}}
  </categories>

  To help you understand how to classify text into these categories, here are some example texts that have already been labeled with their correct category:

  <examples>
  {{EXAMPLES}}
  </examples>

  Please carefully study these examples to identify the key features and characteristics that define each category. Write out your analysis of each category inside <category_analysis> tags, explaining the main topics, themes, writing styles, etc. that seem to be associated with each one.

  Once you feel you have a good grasp of the categories, your task is to build a classifier that can take in new, unlabeled texts and output a prediction of which category it most likely belongs to.

  Before giving your final classification, show your step-by-step process and reasoning inside <classification_process> tags. Weigh the evidence for each potential category.

  Then output your final <classification> for which category you think the example text belongs to.

  The goal is to build a classifier that can accurately categorize new texts into the most appropriate category, as defined by the examples.
  ```
</Accordion>

### 2. Kembangkan kasus uji Anda

Untuk menjalankan evaluasi klasifikasi, Anda memerlukan kasus uji untuk menjalankannya. Lihat panduan untuk [mengembangkan kasus uji](/docs/id/test-and-evaluate/develop-tests).

### 3. Jalankan evaluasi Anda

#### Metrik evaluasi

Beberapa metrik keberhasilan yang perlu dipertimbangkan saat mengevaluasi kinerja Claude pada tugas klasifikasi meliputi:

| Kriteria              | Deskripsi                                                                                                                                                                                                 |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Akurasi**           | Output model sama persis dengan jawaban acuan atau mengklasifikasikan input dengan benar sesuai persyaratan tugas. Ini biasanya dihitung sebagai (Jumlah prediksi benar) / (Jumlah keseluruhan prediksi). |
| **F1 Score**          | Output model menyeimbangkan presisi dan recall secara optimal.                                                                                                                                            |
| **Konsistensi**       | Output model konsisten dengan prediksinya untuk input serupa atau mengikuti pola yang logis.                                                                                                              |
| **Struktur**          | Output model mengikuti format atau struktur yang diharapkan, sehingga mudah diurai dan diinterpretasikan. Misalnya, banyak pengklasifikasi diharapkan menghasilkan output dalam format JSON.              |
| **Kecepatan**         | Model memberikan respons dalam batas waktu yang dapat diterima atau ambang batas latensi untuk tugas tersebut.                                                                                            |
| **Bias dan Keadilan** | Jika mengklasifikasikan data tentang orang, penting bahwa model tidak menunjukkan bias apa pun berdasarkan gender, etnis, atau karakteristik lain yang dapat menyebabkan kesalahan klasifikasi.           |

## Terapkan pengklasifikasi Anda

Untuk melihat contoh kode tentang cara menggunakan Claude untuk klasifikasi, lihat [Panduan Klasifikasi](https://platform.claude.com/cookbook/capabilities-classification-guide) di Claude Cookbook.
