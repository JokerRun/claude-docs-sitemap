---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/enterprise
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 9ba894ccb938690d0520e32a97b1c840b0c7e1c78dac9ab0c8a2d5384fe51cb5
---

# Skills untuk enterprise

Tata kelola, tinjauan keamanan, evaluasi, dan panduan organisasi untuk menerapkan Agent Skills dalam skala enterprise.

---

Panduan ini ditujukan untuk admin dan arsitek enterprise yang perlu mengatur tata kelola Agent Skills di seluruh organisasi. Panduan ini mencakup cara memeriksa, mengevaluasi, menerapkan, dan mengelola Skills dalam skala besar. Untuk panduan penulisan, lihat [praktik terbaik](/docs/id/agents-and-tools/agent-skills/best-practices). Untuk detail arsitektur, lihat [ikhtisar Skills](/docs/id/agents-and-tools/agent-skills/overview).

## Tinjauan keamanan dan pemeriksaan

Menerapkan Skills di enterprise memerlukan jawaban atas dua pertanyaan yang berbeda:

1. **Apakah Skills aman secara umum?** Lihat bagian [pertimbangan keamanan](/docs/id/agents-and-tools/agent-skills/overview#security-considerations) di ikhtisar untuk detail keamanan tingkat platform.
2. **Bagaimana cara memeriksa Skill tertentu?** Gunakan penilaian risiko dan daftar periksa tinjauan berikut.

### Penilaian tingkat risiko

Evaluasi setiap Skill terhadap indikator risiko berikut sebelum menyetujui penerapan:

| Indikator risiko            | Apa yang harus dicari                                                                                                             | Tingkat kekhawatiran                                            |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Eksekusi kode               | Skrip di direktori Skill (`*.py`, `*.sh`, `*.js`)                                                                                 | Tinggi: skrip berjalan dengan akses penuh ke lingkungan         |
| Manipulasi instruksi        | Arahan untuk mengabaikan aturan keamanan, menyembunyikan tindakan dari pengguna, atau mengubah perilaku Claude secara kondisional | Tinggi: dapat melewati kontrol keamanan                         |
| Referensi server MCP        | Instruksi yang merujuk pada alat MCP (`ServerName:tool_name`)                                                                     | Tinggi: memperluas akses di luar Skill itu sendiri              |
| Pola akses jaringan         | URL, endpoint API, panggilan `fetch`, `curl`, atau `requests`                                                                     | Tinggi: potensi vektor eksfiltrasi data                         |
| Kredensial yang di-hardcode | Kunci API, token, atau kata sandi dalam file atau skrip Skill                                                                     | Tinggi: rahasia terekspos dalam riwayat Git dan jendela konteks |
| Cakupan akses sistem file   | Jalur di luar direktori Skill, pola glob yang luas, path traversal (`../`)                                                        | Sedang: dapat mengakses data yang tidak dimaksudkan             |
| Pemanggilan alat            | Instruksi yang mengarahkan Claude untuk menggunakan bash, operasi file, atau alat lainnya                                         | Sedang: tinjau operasi apa yang dilakukan                       |

### Daftar periksa tinjauan

Sebelum menerapkan Skill apa pun dari pihak ketiga atau kontributor internal, selesaikan langkah-langkah berikut:

1. **Baca semua konten direktori Skill.** Tinjau SKILL.md, semua file markdown yang direferensikan, dan skrip atau sumber daya yang dibundel.
2. **Verifikasi bahwa perilaku skrip sesuai dengan tujuan yang dinyatakan.** Jalankan skrip di lingkungan sandbox dan konfirmasi bahwa output sesuai dengan deskripsi Skill.
3. **Periksa instruksi yang bersifat adversarial.** Cari arahan yang memberi tahu Claude untuk mengabaikan aturan keamanan, menyembunyikan tindakan dari pengguna, mengeksfiltrasi data melalui respons, atau mengubah perilaku berdasarkan input tertentu.
4. **Periksa pengambilan URL eksternal atau panggilan jaringan.** Cari pola akses jaringan dalam skrip dan instruksi (`http`, `requests.get`, `urllib`, `curl`, `fetch`).
5. **Verifikasi tidak ada kredensial yang di-hardcode.** Periksa kunci API, token, atau kata sandi dalam file Skill. Kredensial harus menggunakan variabel lingkungan atau penyimpanan kredensial yang aman, dan tidak boleh muncul dalam konten Skill.
6. **Identifikasi alat dan perintah yang diinstruksikan Skill untuk dipanggil oleh Claude.** Daftarkan semua perintah bash, operasi file, dan referensi alat. Pertimbangkan risiko gabungan ketika sebuah Skill menggunakan alat baca-file dan jaringan secara bersamaan.
7. **Konfirmasi tujuan pengalihan.** Jika Skill merujuk pada URL eksternal, verifikasi bahwa URL tersebut mengarah ke domain yang diharapkan.
8. **Verifikasi tidak ada pola eksfiltrasi data.** Cari instruksi yang membaca data sensitif lalu menulis, mengirim, atau mengenkodenya untuk transmisi eksternal, termasuk melalui respons percakapan Claude.

<Warning>
  Jangan pernah menerapkan Skills dari sumber yang tidak tepercaya tanpa audit penuh. Skill yang berbahaya dapat mengarahkan Claude untuk mengeksekusi kode arbitrer, mengakses file sensitif, atau mengirimkan data ke luar. Perlakukan instalasi Skill dengan ketelitian yang sama seperti menginstal perangkat lunak pada sistem produksi.
</Warning>

## Mengevaluasi Skills sebelum penerapan

Skills dapat menurunkan kinerja agen jika terpicu secara tidak tepat, berkonflik dengan Skills lain, atau memberikan instruksi yang buruk. Wajibkan evaluasi sebelum penerapan produksi apa pun.

### Apa yang harus dievaluasi

Tetapkan gerbang persetujuan untuk dimensi-dimensi berikut sebelum menerapkan Skill apa pun:

| Dimensi             | Apa yang diukur                                                                                 | Contoh kegagalan                                                                                   |
| ------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Akurasi pemicuan    | Apakah Skill aktif untuk kueri yang tepat dan tetap tidak aktif untuk kueri yang tidak terkait? | Skill terpicu pada setiap penyebutan spreadsheet, bahkan ketika pengguna hanya ingin membahas data |
| Perilaku isolasi    | Apakah Skill bekerja dengan benar secara mandiri?                                               | Skill merujuk pada file yang tidak ada di direktorinya                                             |
| Koeksistensi        | Apakah menambahkan Skill ini menurunkan kinerja Skills lain?                                    | Deskripsi Skill baru terlalu luas, mencuri pemicu dari Skills yang sudah ada                       |
| Kepatuhan instruksi | Apakah Claude mengikuti instruksi Skill dengan akurat?                                          | Claude melewatkan langkah validasi atau menggunakan pustaka yang salah                             |
| Kualitas output     | Apakah Skill menghasilkan hasil yang benar dan berguna?                                         | Laporan yang dihasilkan memiliki kesalahan format atau data yang hilang                            |

### Persyaratan evaluasi

Wajibkan penulis Skill untuk menyerahkan rangkaian evaluasi dengan 3–5 kueri representatif per Skill, yang mencakup kasus di mana Skill harus terpicu, tidak boleh terpicu, dan kasus tepi yang ambigu. Wajibkan pengujian di seluruh model yang digunakan organisasi Anda (Haiku, Sonnet, Opus), karena efektivitas Skill bervariasi menurut model.

Untuk panduan terperinci tentang membangun evaluasi, lihat [evaluasi dan iterasi](/docs/id/agents-and-tools/agent-skills/best-practices#evaluation-and-iteration) di praktik terbaik. Untuk metodologi evaluasi umum, lihat [mengembangkan kasus uji](/docs/id/test-and-evaluate/develop-tests).

### Menggunakan evaluasi untuk keputusan siklus hidup

Hasil evaluasi memberi sinyal kapan harus bertindak:

* **Akurasi pemicu menurun:** Perbarui deskripsi atau instruksi Skill
* **Konflik koeksistensi:** Konsolidasikan Skills yang tumpang tindih atau persempit deskripsi
* **Kualitas output yang konsisten rendah:** Tulis ulang instruksi atau tambahkan langkah validasi
* **Kegagalan yang terus-menerus di seluruh pembaruan:** Hentikan penggunaan Skill tersebut

## Manajemen siklus hidup Skill

<Steps>
  <Step title="Rencanakan">
    Identifikasi alur kerja yang repetitif, rawan kesalahan, atau memerlukan pengetahuan khusus. Petakan alur kerja tersebut ke peran organisasi dan tentukan mana yang menjadi kandidat untuk Skills.
  </Step>

  <Step title="Buat dan tinjau">
    Pastikan penulis Skill mengikuti [praktik terbaik](/docs/id/agents-and-tools/agent-skills/best-practices). Wajibkan tinjauan keamanan menggunakan [daftar periksa tinjauan](#review-checklist). Wajibkan rangkaian evaluasi sebelum persetujuan. Tetapkan pemisahan tugas: penulis Skill tidak boleh menjadi peninjau untuk Skill mereka sendiri.
  </Step>

  <Step title="Uji">
    Wajibkan evaluasi secara terisolasi (Skill sendiri) dan bersama Skills yang sudah ada (pengujian koeksistensi). Verifikasi akurasi pemicuan, kualitas output, dan tidak adanya regresi di seluruh kumpulan Skill aktif Anda sebelum menyetujui untuk produksi.
  </Step>

  <Step title="Terapkan">
    Unggah melalui Skills API untuk akses di seluruh workspace. Lihat [Menggunakan Skills dengan API](/docs/id/build-with-claude/skills-guide) untuk pengunggahan dan manajemen versi. Dokumentasikan Skill di registri internal Anda dengan tujuan, pemilik, dan versi.
  </Step>

  <Step title="Pantau">
    Lacak pola penggunaan dan kumpulkan umpan balik dari pengguna. Jalankan ulang evaluasi secara berkala untuk mendeteksi penyimpangan atau regresi seiring berkembangnya alur kerja dan model. Analitik penggunaan saat ini tidak tersedia melalui Skills API. Terapkan pencatatan tingkat aplikasi untuk melacak Skills mana yang disertakan dalam permintaan.
  </Step>

  <Step title="Iterasi atau hentikan">
    Wajibkan rangkaian evaluasi penuh untuk lulus sebelum mempromosikan versi baru. Perbarui Skills ketika alur kerja berubah atau skor evaluasi menurun. Hentikan penggunaan Skills ketika evaluasi secara konsisten gagal atau alur kerja sudah tidak digunakan lagi.
  </Step>
</Steps>

## Mengorganisasi Skills dalam skala besar

### Batas recall

Sebagai pedoman umum, batasi jumlah Skills yang dimuat secara bersamaan untuk mempertahankan akurasi recall yang andal. Metadata setiap Skill (nama dan deskripsi) bersaing untuk mendapatkan perhatian dalam prompt sistem. Dengan terlalu banyak Skills yang aktif, Claude mungkin gagal memilih Skill yang tepat atau melewatkan Skill yang relevan sama sekali. Gunakan rangkaian evaluasi Anda untuk mengukur akurasi recall saat Anda menambahkan Skills, dan berhenti menambahkan ketika kinerja menurun.

Perhatikan bahwa permintaan API mendukung maksimum 8 Skills untuk setiap permintaan (lihat [Menggunakan Skills dengan API](/docs/id/build-with-claude/skills-guide)). Jika suatu peran memerlukan lebih banyak Skills daripada yang didukung oleh satu permintaan, pertimbangkan untuk mengonsolidasikan Skills yang sempit menjadi Skills yang lebih luas atau merutekan permintaan ke kumpulan Skill yang berbeda berdasarkan jenis tugas.

### Mulai dari yang spesifik, konsolidasikan kemudian

Dorong tim untuk memulai dengan Skills yang sempit dan spesifik untuk alur kerja tertentu, bukan yang luas dan serbaguna. Seiring munculnya pola di seluruh organisasi Anda, konsolidasikan Skills yang terkait menjadi bundel berbasis peran.

<Tip>
  Gunakan evaluasi untuk memutuskan kapan harus mengonsolidasikan. Gabungkan Skills yang sempit menjadi satu yang lebih luas hanya ketika evaluasi Skill hasil konsolidasi mengonfirmasi kinerja yang setara dengan Skills individual yang digantikannya.
</Tip>

**Contoh progresi:**

* Mulai: `formatting-sales-reports`, `querying-pipeline-data`, `updating-crm-records`
* Konsolidasi: `sales-operations` (ketika evaluasi mengonfirmasi kinerja yang setara)

### Penamaan dan katalogisasi

Gunakan konvensi penamaan yang konsisten di seluruh organisasi Anda. Bagian [konvensi penamaan](/docs/id/agents-and-tools/agent-skills/best-practices#naming-conventions) di praktik terbaik menyediakan panduan pemformatan.

Pertahankan registri internal untuk setiap Skill dengan:

* **Tujuan:** Alur kerja apa yang didukung oleh Skill
* **Pemilik:** Tim atau individu yang bertanggung jawab atas pemeliharaan
* **Versi:** Versi yang saat ini diterapkan
* **Dependensi:** Server MCP, paket, atau layanan eksternal yang diperlukan
* **Status evaluasi:** Tanggal dan hasil evaluasi terakhir

### Bundel berbasis peran

Kelompokkan Skills berdasarkan peran organisasi agar kumpulan Skill aktif setiap pengguna tetap terfokus:

* **Tim penjualan:** Operasi CRM, pelaporan pipeline, pembuatan proposal
* **Engineering:** Tinjauan kode, alur kerja deployment, respons insiden
* **Keuangan:** Pembuatan laporan, validasi data, persiapan audit

Setiap bundel berbasis peran hanya boleh berisi Skills yang relevan dengan alur kerja harian peran tersebut.

## Distribusi dan kontrol versi

### Kontrol sumber

Simpan direktori Skill di Git untuk pelacakan riwayat, tinjauan kode melalui pull request, dan kemampuan rollback. Setiap direktori Skill (yang berisi SKILL.md dan file yang dibundel) secara alami dipetakan ke folder yang dilacak Git.

### Distribusi berbasis API

Skills API menyediakan distribusi dengan cakupan workspace. Skills yang diunggah melalui API tersedia untuk semua anggota workspace. Lihat [Menggunakan Skills dengan API](/docs/id/build-with-claude/skills-guide) untuk endpoint pengunggahan, pembuatan versi, dan manajemen.

### Strategi pembuatan versi

* **Produksi:** Sematkan Skills ke versi tertentu. Jalankan rangkaian evaluasi penuh sebelum mempromosikan versi baru. Perlakukan setiap pembaruan sebagai penerapan baru yang memerlukan tinjauan keamanan penuh.
* **Pengembangan dan pengujian:** Gunakan versi terbaru untuk memvalidasi perubahan sebelum promosi ke produksi.
* **Rencana rollback:** Pertahankan versi sebelumnya sebagai cadangan. Jika versi baru gagal dalam evaluasi di produksi, segera kembalikan ke versi terakhir yang diketahui baik.
* **Verifikasi integritas:** Hitung checksum dari Skills yang telah ditinjau dan verifikasi pada saat penerapan. Gunakan commit yang ditandatangani di repositori Skill Anda untuk memastikan provenans.

### Pertimbangan lintas permukaan

<Warning>
  Skills kustom tidak tersinkronisasi antar permukaan. Skills yang diunggah ke API tidak tersedia di claude.ai atau di Claude Code, dan sebaliknya. Setiap permukaan memerlukan pengunggahan dan manajemen terpisah.
</Warning>

Pertahankan file sumber Skill di Git sebagai satu-satunya sumber kebenaran. Jika organisasi Anda menerapkan Skills di beberapa permukaan, terapkan proses sinkronisasi Anda sendiri untuk menjaga konsistensinya. Untuk detail lengkap, lihat [ketersediaan lintas permukaan](/docs/id/agents-and-tools/agent-skills/overview#cross-surface-availability).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Ikhtisar Agent Skills" icon="book-open" href="/docs/id/agents-and-tools/agent-skills/overview">
    Detail arsitektur dan platform
  </Card>

  <Card title="Praktik terbaik" icon="lightbulb" href="/docs/id/agents-and-tools/agent-skills/best-practices">
    Panduan penulisan untuk pembuat Skill
  </Card>

  <Card title="Menggunakan Skills dengan API" icon="code" href="/docs/id/build-with-claude/skills-guide">
    Unggah dan kelola Skills secara terprogram
  </Card>
</CardGroup>
