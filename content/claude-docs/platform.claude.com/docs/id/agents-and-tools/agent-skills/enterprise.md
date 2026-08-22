---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/enterprise
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: 828c0ce813b3824a2664758e8885dd527138df5993202e9148cec94fc7f59a68
---

---
title: Skills untuk enterprise
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/enterprise
description: Tata kelola, tinjauan keamanan, evaluasi, dan panduan organisasi untuk menerapkan Agent Skills pada skala enterprise.
---

Panduan ini ditujukan bagi admin dan arsitek enterprise yang perlu mengelola Agent Skills di seluruh organisasi. Panduan ini mencakup cara memeriksa, mengevaluasi, menerapkan, dan mengelola Skills dalam skala besar. Untuk panduan penulisan, lihat [praktik terbaik](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/best-practices). Untuk detail arsitektur, lihat [ikhtisar Skills](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview).

## Tinjauan keamanan dan pemeriksaan

Menerapkan Skills di lingkungan enterprise memerlukan jawaban atas dua pertanyaan yang berbeda:

1. **Apakah Skills aman secara umum?** Lihat bagian [pertimbangan keamanan](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview#security-considerations) di ikhtisar untuk detail keamanan tingkat platform.
2. **Bagaimana cara memeriksa Skill tertentu?** Gunakan penilaian risiko dan daftar periksa tinjauan berikut.

### Penilaian tingkat risiko

Evaluasi setiap Skill terhadap indikator risiko berikut sebelum menyetujui penerapan:

| Indikator risiko            | Yang perlu diperhatikan                                                                                                              | Tingkat kekhawatiran                                                               |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| Eksekusi kode               | Skrip di direktori Skill (`*.py`, `*.sh`, `*.js`)                                                                                    | Tinggi: skrip berjalan dengan akses lingkungan penuh                               |
| Manipulasi instruksi        | Arahan untuk mengabaikan aturan keselamatan, menyembunyikan tindakan dari pengguna, atau mengubah perilaku Claude secara kondisional | Tinggi: dapat melewati kontrol keamanan                                            |
| Referensi server MCP        | Instruksi yang mereferensikan alat MCP (`ServerName:tool_name`)                                                                      | Tinggi: memperluas akses di luar Skill itu sendiri                                 |
| Pola akses jaringan         | URL, endpoint API, panggilan `fetch`, `curl`, atau `requests`                                                                        | Tinggi: vektor potensial eksfiltrasi data                                          |
| Kredensial yang di-hardcode | Kunci API, token, atau kata sandi dalam file atau skrip Skill                                                                        | Tinggi: rahasia terekspos dalam riwayat Git dan "context window" (jendela konteks) |
| Cakupan akses sistem file   | Path di luar direktori Skill, pola glob yang luas, path traversal (`../`)                                                            | Sedang: dapat mengakses data yang tidak dimaksudkan                                |
| Pemanggilan alat            | Instruksi yang mengarahkan Claude untuk menggunakan bash, operasi file, atau alat lain                                               | Sedang: tinjau operasi apa yang dilakukan                                          |

### Daftar periksa tinjauan

Sebelum menerapkan Skill apa pun dari pihak ketiga atau kontributor internal, selesaikan langkah-langkah berikut:

1. **Baca seluruh konten direktori Skill.** Tinjau SKILL.md, semua file markdown yang direferensikan, dan skrip atau sumber daya apa pun yang dibundel.
2. **Verifikasi bahwa perilaku skrip sesuai dengan tujuan yang dinyatakan.** Jalankan skrip di lingkungan sandbox dan pastikan output selaras dengan deskripsi Skill.
3. **Periksa adanya instruksi adversarial.** Cari arahan yang memberi tahu Claude untuk mengabaikan aturan keselamatan, menyembunyikan tindakan dari pengguna, mengeksfiltrasi data melalui respons, atau mengubah perilaku berdasarkan input tertentu.
4. **Periksa adanya pengambilan URL eksternal atau panggilan jaringan.** Telusuri skrip dan instruksi untuk pola akses jaringan (`http`, `requests.get`, `urllib`, `curl`, `fetch`).
5. **Verifikasi tidak ada kredensial yang di-hardcode.** Periksa adanya kunci API, token, atau kata sandi dalam file Skill. Kredensial harus menggunakan variabel lingkungan atau penyimpanan kredensial yang aman, dan tidak boleh muncul dalam konten Skill.
6. **Identifikasi alat dan perintah yang diinstruksikan Skill kepada Claude untuk dipanggil.** Daftarkan semua perintah bash, operasi file, dan referensi alat. Pertimbangkan risiko gabungan ketika sebuah Skill menggunakan alat baca-file dan alat jaringan secara bersamaan.
7. **Konfirmasi tujuan pengalihan.** Jika Skill mereferensikan URL eksternal, verifikasi bahwa URL tersebut mengarah ke domain yang diharapkan.
8. **Verifikasi tidak ada pola eksfiltrasi data.** Cari instruksi yang membaca data sensitif lalu menulis, mengirim, atau mengodekannya untuk transmisi eksternal, termasuk melalui respons percakapan Claude.

<Warning>
  Jangan pernah menerapkan Skills dari sumber yang tidak tepercaya tanpa audit penuh. Skill berbahaya dapat mengarahkan Claude untuk mengeksekusi kode arbitrer, mengakses file sensitif, atau mengirimkan data ke luar. Perlakukan instalasi Skill dengan ketelitian yang sama seperti menginstal perangkat lunak pada sistem produksi.
</Warning>

### Pemindaian konten Skill

Organisasi Claude Enterprise dapat mengaktifkan pemindaian keamanan otomatis untuk Skills kustom di claude.ai dan Claude Cowork. Fitur ini dalam tahap beta. Setelah Anda mengaktifkan **Skill and plugin security scanning** di [claude.ai > Organization settings > Skills](https://claude.ai/admin-settings/skills), Skills yang kemudian diunggah atau diedit oleh anggota di claude.ai atau Cowork akan dipindai untuk mencari tanda-tanda perilaku berbahaya, seperti eksekusi kode tersembunyi, pengiriman data Anda ke layanan luar, atau instruksi yang mengganggu pengaman Claude. Skill yang gagal dalam pemindaian, atau yang pemindaiannya belum selesai, diblokir dari penggunaan. Skill yang lolos dengan peringatan tetap dapat digunakan dengan pemberitahuan kehati-hatian. Jika pemindaian tersedia untuk organisasi Anda, aktifkanlah. Fitur ini melengkapi, tetapi tidak menggantikan, [daftar periksa tinjauan](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/enterprise#review-checklist).

Pemindaian tidak mencakup Claude API. Skills yang Anda unggah melalui Skills API (`/v1/skills`), termasuk dari Claude Console, tidak dipindai, sehingga untuk penerapan API, andalkan daftar periksa tinjauan dan [penyematan versi](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/enterprise#versioning-strategy). Pemindaian juga tidak berlaku untuk Skills yang sudah ada di organisasi Anda saat Anda mengaktifkannya, atau untuk organisasi dengan konfigurasi penanganan data tertentu, seperti customer-managed encryption keys (CMEK), zero data retention (ZDR), atau kesiapan HIPAA. Untuk langkah penyiapan, pengecualian, dan jenis hasil, lihat [Get started with skill and plugin scanning](https://support.claude.com/en/articles/15927065-get-started-with-skill-and-plugin-scanning) di Claude Help Center.

## Mengevaluasi Skills sebelum penerapan

Skills dapat menurunkan kinerja agen jika terpicu secara tidak tepat, berkonflik dengan Skills lain, atau memberikan instruksi yang buruk. Wajibkan evaluasi sebelum penerapan produksi apa pun.

### Apa yang perlu dievaluasi

Tetapkan gerbang persetujuan untuk dimensi-dimensi berikut sebelum menerapkan Skill apa pun:

| Dimensi             | Apa yang diukur                                                                                 | Contoh kegagalan                                                                                        |
| ------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Akurasi pemicuan    | Apakah Skill aktif untuk kueri yang tepat dan tetap tidak aktif untuk kueri yang tidak terkait? | Skill terpicu pada setiap penyebutan spreadsheet, bahkan ketika pengguna hanya ingin mendiskusikan data |
| Perilaku isolasi    | Apakah Skill berfungsi dengan benar secara mandiri?                                             | Skill mereferensikan file yang tidak ada di direktorinya                                                |
| Koeksistensi        | Apakah menambahkan Skill ini menurunkan kinerja Skills lain?                                    | Deskripsi Skill baru terlalu luas, merebut pemicu dari Skills yang sudah ada                            |
| Kepatuhan instruksi | Apakah Claude mengikuti instruksi Skill dengan akurat?                                          | Claude melewatkan langkah validasi atau menggunakan library yang salah                                  |
| Kualitas output     | Apakah Skill menghasilkan hasil yang benar dan berguna?                                         | Laporan yang dihasilkan memiliki kesalahan format atau data yang hilang                                 |

### Persyaratan evaluasi

Wajibkan penulis Skill untuk menyerahkan rangkaian evaluasi dengan 3–5 kueri representatif per Skill, yang mencakup kasus di mana Skill seharusnya terpicu, tidak seharusnya terpicu, dan kasus tepi yang ambigu. Wajibkan pengujian di seluruh model yang digunakan organisasi Anda (Haiku, Sonnet, Opus), karena efektivitas Skill bervariasi menurut model.

Untuk panduan terperinci tentang membangun evaluasi, lihat [evaluasi dan iterasi](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/best-practices#evaluation-and-iteration) di praktik terbaik. Untuk metodologi evaluasi umum, lihat [mengembangkan kasus uji](https://platform.claude.com/docs/id/test-and-evaluate/develop-tests).

### Menggunakan evaluasi untuk keputusan siklus hidup

Hasil evaluasi memberi sinyal kapan harus bertindak:

* **Akurasi pemicuan yang menurun:** Perbarui deskripsi atau instruksi Skill
* **Konflik koeksistensi:** Konsolidasikan Skills yang tumpang tindih atau persempit deskripsi
* **Kualitas output yang terus-menerus rendah:** Tulis ulang instruksi atau tambahkan langkah validasi
* **Kegagalan yang berlanjut di berbagai pembaruan:** Hentikan (deprecate) Skill tersebut

## Manajemen siklus hidup Skill

<Steps>
  <Step title="Rencanakan">
    Identifikasi alur kerja yang berulang, rawan kesalahan, atau memerlukan pengetahuan khusus. Petakan alur kerja ini ke peran organisasi dan tentukan mana yang menjadi kandidat untuk Skills.
  </Step>

  <Step title="Buat dan tinjau">
    Pastikan penulis Skill mengikuti [praktik terbaik](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/best-practices). Wajibkan tinjauan keamanan menggunakan [daftar periksa tinjauan](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/enterprise#review-checklist). Wajibkan rangkaian evaluasi sebelum persetujuan. Tetapkan pemisahan tugas: penulis Skill tidak boleh menjadi peninjau bagi dirinya sendiri.
  </Step>

  <Step title="Uji">
    Wajibkan evaluasi secara terisolasi (Skill saja) dan bersama Skills yang sudah ada (pengujian koeksistensi). Verifikasi akurasi pemicuan, kualitas output, dan tidak adanya regresi di seluruh kumpulan Skill aktif Anda sebelum menyetujui untuk produksi.
  </Step>

  <Step title="Terapkan">
    Unggah melalui Skills API untuk akses di seluruh workspace. Lihat [Menggunakan Skills dengan API](https://platform.claude.com/docs/id/build-with-claude/skills-guide) untuk pengunggahan dan manajemen versi. Dokumentasikan Skill di registri internal Anda dengan tujuan, pemilik, dan versi.
  </Step>

  <Step title="Pantau">
    Lacak pola penggunaan dan kumpulkan umpan balik dari pengguna. Jalankan ulang evaluasi secara berkala untuk mendeteksi penyimpangan atau regresi seiring berkembangnya alur kerja dan model. Analitik penggunaan saat ini tidak tersedia melalui Skills API. Implementasikan logging tingkat aplikasi untuk melacak Skills mana yang disertakan dalam permintaan.
  </Step>

  <Step title="Iterasi atau hentikan">
    Wajibkan rangkaian evaluasi lengkap lulus sebelum mempromosikan versi baru. Perbarui Skills ketika alur kerja berubah atau skor evaluasi menurun. Hentikan Skills ketika evaluasi terus-menerus gagal atau alur kerjanya dipensiunkan.
  </Step>
</Steps>

## Mengorganisasi Skills dalam skala besar

### Batas recall

Sebagai pedoman umum, batasi jumlah Skills yang dimuat secara bersamaan untuk menjaga akurasi recall yang andal. Metadata setiap Skill (nama dan deskripsi) bersaing untuk mendapatkan perhatian dalam "system prompt" (prompt sistem). Dengan terlalu banyak Skills yang aktif, Claude mungkin gagal memilih Skill yang tepat atau melewatkan Skill yang relevan sama sekali. Gunakan rangkaian evaluasi Anda untuk mengukur akurasi recall saat Anda menambahkan Skills, dan berhenti menambahkan ketika kinerja menurun.

Perhatikan bahwa permintaan API mendukung maksimum 20 Skills untuk setiap permintaan (lihat [Menggunakan Skills dengan API](https://platform.claude.com/docs/id/build-with-claude/skills-guide)). Jika suatu peran memerlukan lebih banyak Skills daripada yang didukung satu permintaan, pertimbangkan untuk mengonsolidasikan Skills yang sempit menjadi Skills yang lebih luas atau merutekan permintaan ke kumpulan Skill yang berbeda berdasarkan jenis tugas.

### Mulai spesifik, konsolidasikan kemudian

Dorong tim untuk memulai dengan Skills yang sempit dan spesifik untuk alur kerja tertentu daripada Skills yang luas dan serbaguna. Seiring munculnya pola di seluruh organisasi Anda, konsolidasikan Skills terkait ke dalam bundel berbasis peran.

<Tip>
  Gunakan evaluasi untuk memutuskan kapan harus mengonsolidasi. Gabungkan Skills yang sempit menjadi satu Skill yang lebih luas hanya ketika evaluasi Skill hasil konsolidasi mengonfirmasi kinerja yang setara dengan Skills individual yang digantikannya.
</Tip>

**Contoh perkembangan:**

* Mulai: `formatting-sales-reports`, `querying-pipeline-data`, `updating-crm-records`
* Konsolidasi: `sales-operations` (ketika evaluasi mengonfirmasi kinerja yang setara)

### Penamaan dan pengatalogan

Gunakan konvensi penamaan yang konsisten di seluruh organisasi Anda. Bagian [konvensi penamaan](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/best-practices#naming-conventions) di praktik terbaik memberikan panduan format.

Pelihara registri internal untuk setiap Skill dengan:

* **Tujuan:** Alur kerja apa yang didukung Skill
* **Pemilik:** Tim atau individu yang bertanggung jawab atas pemeliharaan
* **Versi:** Versi yang saat ini diterapkan
* **Dependensi:** Server MCP, paket, atau layanan eksternal yang diperlukan
* **Status evaluasi:** Tanggal dan hasil evaluasi terakhir

### Bundel berbasis peran

Kelompokkan Skills berdasarkan peran organisasi agar kumpulan Skill aktif setiap pengguna tetap terfokus:

* **Tim penjualan:** Operasi CRM, pelaporan pipeline, pembuatan proposal
* **Engineering:** Tinjauan kode, alur kerja deployment, respons insiden
* **Keuangan:** Pembuatan laporan, validasi data, persiapan audit

Setiap bundel berbasis peran sebaiknya hanya berisi Skills yang relevan dengan alur kerja harian peran tersebut.

## Distribusi dan kontrol versi

### Kontrol sumber

Simpan direktori Skill di Git untuk pelacakan riwayat, tinjauan kode melalui pull request, dan kemampuan rollback. Setiap direktori Skill (yang berisi SKILL.md dan file apa pun yang dibundel) secara alami dipetakan ke folder yang dilacak Git.

### Distribusi berbasis API

Skills API menyediakan distribusi dengan cakupan workspace. Skills yang diunggah melalui API tersedia bagi semua anggota workspace. Lihat [Menggunakan Skills dengan API](https://platform.claude.com/docs/id/build-with-claude/skills-guide) untuk endpoint pengunggahan, pembuatan versi, dan manajemen.

### Strategi pembuatan versi

* **Produksi:** Sematkan Skills ke versi tertentu. Jika Anda menghilangkan `version`, permintaan akan menggunakan versi terbaru, sehingga versi baru yang diunggah oleh siapa pun di workspace akan langsung mengubah apa yang dijalankan agen produksi. Jalankan rangkaian evaluasi lengkap sebelum mempromosikan versi baru. Perlakukan setiap pembaruan sebagai penerapan baru yang memerlukan tinjauan keamanan penuh.
* **Pengembangan dan pengujian:** Gunakan versi terbaru untuk memvalidasi perubahan sebelum promosi ke produksi.
* **Rencana rollback:** Pertahankan versi sebelumnya sebagai cadangan. Jika versi baru gagal dalam evaluasi di produksi, segera kembalikan ke versi terakhir yang diketahui baik.
* **Verifikasi integritas:** Hitung checksum dari Skills yang telah ditinjau dan verifikasi pada saat penerapan. Gunakan signed commit di repositori Skill Anda untuk memastikan asal-usulnya.

### Pertimbangan lintas permukaan

<Warning>
  Skills kustom tidak disinkronkan di seluruh permukaan. Skills yang diunggah ke API tidak tersedia di claude.ai atau di Claude Code, dan sebaliknya. Setiap permukaan memerlukan pengunggahan dan manajemen terpisah.
</Warning>

Pelihara file sumber Skill di Git sebagai satu-satunya sumber kebenaran. Jika organisasi Anda menerapkan Skills di berbagai permukaan, implementasikan proses sinkronisasi Anda sendiri untuk menjaganya tetap konsisten. Untuk detail lengkap, lihat [ketersediaan lintas permukaan](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview#cross-surface-availability).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Ikhtisar Agent Skills" icon="book-open" href="https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview">
    Detail arsitektur dan platform
  </Card>

  <Card title="Praktik terbaik" icon="lightbulb" href="https://platform.claude.com/docs/id/agents-and-tools/agent-skills/best-practices">
    Panduan penulisan untuk pembuat Skill
  </Card>

  <Card title="Menggunakan Skills dengan API" icon="code" href="https://platform.claude.com/docs/id/build-with-claude/skills-guide">
    Unggah dan kelola Skills secara terprogram
  </Card>
</CardGroup>
