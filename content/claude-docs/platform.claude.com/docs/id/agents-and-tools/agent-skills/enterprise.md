---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/enterprise
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 5fa784b72b478a819c063c603fdef280c48fd49c5677873b3602c2e5a6e3189b
---

# Skills untuk enterprise

Tata kelola, tinjauan keamanan, evaluasi, dan panduan organisasi untuk menerapkan Agent Skills pada skala enterprise.

---

Panduan ini ditujukan untuk admin dan arsitek enterprise yang perlu mengelola Agent Skills di seluruh organisasi. Panduan ini mencakup cara memeriksa, mengevaluasi, menerapkan, dan mengelola Skills dalam skala besar. Untuk panduan penulisan, lihat [praktik terbaik](/docs/id/agents-and-tools/agent-skills/best-practices). Untuk detail arsitektur, lihat [ikhtisar Skills](/docs/id/agents-and-tools/agent-skills/overview).

## Tinjauan keamanan dan pemeriksaan \{#security-review-and-vetting}

Menerapkan Skills di lingkungan enterprise memerlukan jawaban atas dua pertanyaan yang berbeda:

1. **Apakah Skills aman secara umum?** Lihat bagian [pertimbangan keamanan](/docs/id/agents-and-tools/agent-skills/overview#security-considerations) di ikhtisar untuk detail keamanan tingkat platform.
2. **Bagaimana cara memeriksa Skill tertentu?** Gunakan penilaian risiko dan daftar periksa tinjauan di bawah ini.

### Penilaian tingkat risiko \{#risk-tier-assessment}

Evaluasi setiap Skill terhadap indikator risiko berikut sebelum menyetujui penerapan:

| Indikator risiko | Apa yang perlu dicari | Tingkat kekhawatiran |
|---|---|---|
| Eksekusi kode | Skrip dalam direktori Skill (`*.py`, `*.sh`, `*.js`) | Tinggi: skrip berjalan dengan akses penuh ke lingkungan |
| Manipulasi instruksi | Arahan untuk mengabaikan aturan keamanan, menyembunyikan tindakan dari pengguna, atau mengubah perilaku Claude secara kondisional | Tinggi: dapat melewati kontrol keamanan |
| Referensi server MCP | Instruksi yang mereferensikan alat MCP (`ServerName:tool_name`) | Tinggi: memperluas akses di luar Skill itu sendiri |
| Pola akses jaringan | URL, endpoint API, panggilan `fetch`, `curl`, atau `requests` | Tinggi: potensi vektor eksfiltrasi data |
| Kredensial yang di-hardcode | Kunci API, token, atau kata sandi dalam file atau skrip Skill | Tinggi: rahasia terekspos dalam riwayat Git dan jendela konteks |
| Cakupan akses sistem file | Path di luar direktori Skill, pola glob yang luas, path traversal (`../`) | Sedang: dapat mengakses data yang tidak diinginkan |
| Pemanggilan alat | Instruksi yang mengarahkan Claude untuk menggunakan bash, operasi file, atau alat lainnya | Sedang: tinjau operasi apa yang dilakukan |

### Daftar periksa tinjauan \{#review-checklist}

Sebelum menerapkan Skill apa pun dari pihak ketiga atau kontributor internal, selesaikan langkah-langkah berikut:

1. **Baca semua konten direktori Skill.** Tinjau SKILL.md, semua file markdown yang direferensikan, dan skrip atau sumber daya apa pun yang disertakan.
2. **Verifikasi bahwa perilaku skrip sesuai dengan tujuan yang dinyatakan.** Jalankan skrip di lingkungan sandbox dan konfirmasi bahwa output sesuai dengan deskripsi Skill.
3. **Periksa adanya instruksi yang bersifat adversarial.** Cari arahan yang memberi tahu Claude untuk mengabaikan aturan keamanan, menyembunyikan tindakan dari pengguna, mengeksfiltrasi data melalui respons, atau mengubah perilaku berdasarkan input tertentu.
4. **Periksa adanya pengambilan URL eksternal atau panggilan jaringan.** Cari pola akses jaringan dalam skrip dan instruksi (`http`, `requests.get`, `urllib`, `curl`, `fetch`).
5. **Verifikasi tidak ada kredensial yang di-hardcode.** Periksa adanya kunci API, token, atau kata sandi dalam file Skill. Kredensial harus menggunakan variabel lingkungan atau penyimpanan kredensial yang aman, tidak boleh muncul dalam konten Skill.
6. **Identifikasi alat dan perintah yang diinstruksikan Skill untuk dipanggil oleh Claude.** Buat daftar semua perintah bash, operasi file, dan referensi alat. Pertimbangkan risiko gabungan ketika sebuah Skill menggunakan alat baca-file dan alat jaringan secara bersamaan.
7. **Konfirmasi tujuan pengalihan.** Jika Skill mereferensikan URL eksternal, verifikasi bahwa URL tersebut mengarah ke domain yang diharapkan.
8. **Verifikasi tidak ada pola eksfiltrasi data.** Cari instruksi yang membaca data sensitif lalu menulis, mengirim, atau mengenkodenya untuk transmisi eksternal, termasuk melalui respons percakapan Claude.

<Warning>
Jangan pernah menerapkan Skills dari sumber yang tidak tepercaya tanpa audit penuh. Skill yang berbahaya dapat mengarahkan Claude untuk mengeksekusi kode arbitrer, mengakses file sensitif, atau mentransmisikan data secara eksternal. Perlakukan instalasi Skill dengan ketelitian yang sama seperti menginstal perangkat lunak pada sistem produksi.
</Warning>

## Mengevaluasi Skills sebelum penerapan \{#evaluating-skills-before-deployment}

Skills dapat menurunkan kinerja agen jika terpicu secara tidak tepat, berkonflik dengan Skills lain, atau memberikan instruksi yang buruk. Wajibkan evaluasi sebelum penerapan produksi apa pun.

### Apa yang perlu dievaluasi \{#what-to-evaluate}

Tetapkan gerbang persetujuan untuk dimensi-dimensi berikut sebelum menerapkan Skill apa pun:

| Dimensi | Apa yang diukur | Contoh kegagalan |
|---|---|---|
| Akurasi pemicuan | Apakah Skill aktif untuk kueri yang tepat dan tetap tidak aktif untuk kueri yang tidak terkait? | Skill terpicu pada setiap penyebutan spreadsheet, bahkan ketika pengguna hanya ingin membahas data |
| Perilaku isolasi | Apakah Skill bekerja dengan benar secara mandiri? | Skill mereferensikan file yang tidak ada dalam direktorinya |
| Koeksistensi | Apakah menambahkan Skill ini menurunkan kinerja Skills lain? | Deskripsi Skill baru terlalu luas, mengambil alih pemicu dari Skills yang sudah ada |
| Kepatuhan instruksi | Apakah Claude mengikuti instruksi Skill secara akurat? | Claude melewatkan langkah validasi atau menggunakan library yang salah |
| Kualitas output | Apakah Skill menghasilkan hasil yang benar dan berguna? | Laporan yang dihasilkan memiliki kesalahan format atau data yang hilang |

### Persyaratan evaluasi \{#evaluation-requirements}

Wajibkan penulis Skill untuk menyerahkan rangkaian evaluasi dengan 3-5 kueri representatif per Skill, yang mencakup kasus di mana Skill seharusnya terpicu, seharusnya tidak terpicu, dan kasus tepi yang ambigu. Wajibkan pengujian di seluruh model yang digunakan organisasi Anda (Haiku, Sonnet, Opus), karena efektivitas Skill bervariasi menurut model.

Untuk panduan terperinci tentang membangun evaluasi, lihat [evaluasi dan iterasi](/docs/id/agents-and-tools/agent-skills/best-practices#evaluation-and-iteration) di praktik terbaik. Untuk metodologi evaluasi umum, lihat [mengembangkan kasus uji](/docs/id/test-and-evaluate/develop-tests).

### Menggunakan evaluasi untuk keputusan siklus hidup \{#using-evaluations-for-lifecycle-decisions}

Hasil evaluasi memberi sinyal kapan harus bertindak:

- **Akurasi pemicuan menurun:** Perbarui deskripsi atau instruksi Skill
- **Konflik koeksistensi:** Konsolidasikan Skills yang tumpang tindih atau persempit deskripsi
- **Kualitas output yang konsisten rendah:** Tulis ulang instruksi atau tambahkan langkah validasi
- **Kegagalan yang terus-menerus di seluruh pembaruan:** Hentikan penggunaan Skill tersebut

## Manajemen siklus hidup Skill \{#skill-lifecycle-management}

<Steps>
  <Step title="Rencanakan">
    Identifikasi alur kerja yang repetitif, rentan kesalahan, atau memerlukan pengetahuan khusus. Petakan alur kerja ini ke peran organisasi dan tentukan mana yang menjadi kandidat untuk Skills.
  </Step>
  <Step title="Buat dan tinjau">
    Pastikan penulis Skill mengikuti [praktik terbaik](/docs/id/agents-and-tools/agent-skills/best-practices). Wajibkan tinjauan keamanan menggunakan [daftar periksa tinjauan](#daftar-periksa-tinjauan) di atas. Wajibkan rangkaian evaluasi sebelum persetujuan. Tetapkan pemisahan tugas: penulis Skill tidak boleh menjadi peninjau mereka sendiri.
  </Step>
  <Step title="Uji">
    Wajibkan evaluasi secara terisolasi (Skill sendiri) dan bersama Skills yang sudah ada (pengujian koeksistensi). Verifikasi akurasi pemicuan, kualitas output, dan tidak adanya regresi di seluruh kumpulan Skill aktif Anda sebelum menyetujui untuk produksi.
  </Step>
  <Step title="Terapkan">
    Unggah melalui Skills API untuk akses di seluruh workspace. Lihat [Menggunakan Skills dengan API](/docs/id/build-with-claude/skills-guide) untuk pengunggahan dan manajemen versi. Dokumentasikan Skill dalam registri internal Anda dengan tujuan, pemilik, dan versi.
  </Step>
  <Step title="Pantau">
    Lacak pola penggunaan dan kumpulkan umpan balik dari pengguna. Jalankan kembali evaluasi secara berkala untuk mendeteksi drift atau regresi seiring berkembangnya alur kerja dan model. Analitik penggunaan saat ini tidak tersedia melalui Skills API. Terapkan logging tingkat aplikasi untuk melacak Skills mana yang disertakan dalam permintaan.
  </Step>
  <Step title="Iterasi atau hentikan">
    Wajibkan rangkaian evaluasi lengkap untuk lulus sebelum mempromosikan versi baru. Perbarui Skills ketika alur kerja berubah atau skor evaluasi menurun. Hentikan penggunaan Skills ketika evaluasi secara konsisten gagal atau alur kerja tersebut sudah tidak digunakan.
  </Step>
</Steps>

## Mengorganisasi Skills dalam skala besar \{#organizing-skills-at-scale}

### Batas recall \{#recall-limits}

Sebagai pedoman umum, batasi jumlah Skills yang dimuat secara bersamaan untuk menjaga akurasi "recall" (pemanggilan kembali) yang andal. Metadata setiap Skill (nama dan deskripsi) bersaing untuk mendapatkan perhatian dalam prompt sistem. Dengan terlalu banyak Skills yang aktif, Claude mungkin gagal memilih Skill yang tepat atau melewatkan Skill yang relevan sepenuhnya. Gunakan rangkaian evaluasi Anda untuk mengukur akurasi recall saat Anda menambahkan Skills, dan berhenti menambahkan ketika kinerja menurun.

Perhatikan bahwa permintaan API mendukung maksimum 8 Skills per permintaan (lihat [Menggunakan Skills dengan API](/docs/id/build-with-claude/skills-guide)). Jika suatu peran memerlukan lebih banyak Skills daripada yang didukung oleh satu permintaan, pertimbangkan untuk mengonsolidasikan Skills yang sempit menjadi yang lebih luas atau merutekan permintaan ke kumpulan Skill yang berbeda berdasarkan jenis tugas.

### Mulai spesifik, konsolidasikan kemudian \{#start-specific-consolidate-later}

Dorong tim untuk memulai dengan Skills yang sempit dan spesifik untuk alur kerja daripada yang luas dan multiguna. Seiring munculnya pola di seluruh organisasi Anda, konsolidasikan Skills terkait menjadi bundel berbasis peran.

<Tip>
Gunakan evaluasi untuk memutuskan kapan harus mengonsolidasikan. Gabungkan Skills yang sempit menjadi satu yang lebih luas hanya ketika evaluasi Skill yang dikonsolidasikan mengonfirmasi kinerja yang setara dengan Skills individual yang digantikannya.
</Tip>

**Contoh perkembangan**:
- Mulai: `formatting-sales-reports`, `querying-pipeline-data`, `updating-crm-records`
- Konsolidasi: `sales-operations` (ketika evaluasi mengonfirmasi kinerja yang setara)

### Penamaan dan katalogisasi \{#naming-and-cataloging}

Gunakan konvensi penamaan yang konsisten di seluruh organisasi Anda. Bagian [konvensi penamaan](/docs/id/agents-and-tools/agent-skills/best-practices#naming-conventions) di praktik terbaik menyediakan panduan format.

Pelihara registri internal untuk setiap Skill dengan:
- **Tujuan**: Alur kerja apa yang didukung Skill
- **Pemilik**: Tim atau individu yang bertanggung jawab atas pemeliharaan
- **Versi**: Versi yang saat ini diterapkan
- **Dependensi**: Server MCP, paket, atau layanan eksternal yang diperlukan
- **Status evaluasi**: Tanggal evaluasi terakhir dan hasilnya

### Bundel berbasis peran \{#role-based-bundles}

Kelompokkan Skills berdasarkan peran organisasi untuk menjaga kumpulan Skill aktif setiap pengguna tetap terfokus:

- **Tim penjualan**: Operasi CRM, pelaporan pipeline, pembuatan proposal
- **Engineering**: Tinjauan kode, alur kerja deployment, respons insiden
- **Keuangan**: Pembuatan laporan, validasi data, persiapan audit

Setiap bundel berbasis peran hanya boleh berisi Skills yang relevan dengan alur kerja harian peran tersebut.

## Distribusi dan kontrol versi \{#distribution-and-version-control}

### Kontrol sumber \{#source-control}

Simpan direktori Skill di Git untuk pelacakan riwayat, tinjauan kode melalui pull request, dan kemampuan rollback. Setiap direktori Skill (yang berisi SKILL.md dan file apa pun yang disertakan) secara alami dipetakan ke folder yang dilacak Git.

### Distribusi berbasis API \{#api-based-distribution}

Skills API menyediakan distribusi dengan cakupan workspace. Skills yang diunggah melalui API tersedia untuk semua anggota workspace. Lihat [Menggunakan Skills dengan API](/docs/id/build-with-claude/skills-guide) untuk endpoint pengunggahan, versioning, dan manajemen.

### Strategi versioning \{#versioning-strategy}

- **Produksi**: Sematkan Skills ke versi tertentu. Jalankan rangkaian evaluasi lengkap sebelum mempromosikan versi baru. Perlakukan setiap pembaruan sebagai penerapan baru yang memerlukan tinjauan keamanan penuh.
- **Pengembangan dan pengujian**: Gunakan versi terbaru untuk memvalidasi perubahan sebelum promosi ke produksi.
- **Rencana rollback**: Pertahankan versi sebelumnya sebagai cadangan. Jika versi baru gagal dalam evaluasi di produksi, segera kembalikan ke versi terakhir yang diketahui baik.
- **Verifikasi integritas**: Hitung checksum dari Skills yang telah ditinjau dan verifikasi pada saat penerapan. Gunakan signed commit di repositori Skill Anda untuk memastikan asal-usulnya.

### Pertimbangan lintas surface \{#cross-surface-considerations}

<Warning>
Skills kustom tidak tersinkronisasi antar surface. Skills yang diunggah ke API tidak tersedia di claude.ai atau di Claude Code, dan sebaliknya. Setiap surface memerlukan pengunggahan dan manajemen terpisah.
</Warning>

Pelihara file sumber Skill di Git sebagai satu-satunya sumber kebenaran. Jika organisasi Anda menerapkan Skills di beberapa surface, terapkan proses sinkronisasi Anda sendiri untuk menjaganya tetap konsisten. Untuk detail lengkap, lihat [ketersediaan lintas surface](/docs/id/agents-and-tools/agent-skills/overview#cross-surface-availability).

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card
    title="Ikhtisar Agent Skills"
    icon="book-open"
    href="/docs/id/agents-and-tools/agent-skills/overview"
  >
    Detail arsitektur dan platform
  </Card>
  <Card
    title="Praktik terbaik"
    icon="lightbulb"
    href="/docs/id/agents-and-tools/agent-skills/best-practices"
  >
    Panduan penulisan untuk pembuat Skill
  </Card>
  <Card
    title="Menggunakan Skills dengan API"
    icon="code"
    href="/docs/id/build-with-claude/skills-guide"
  >
    Unggah dan kelola Skills secara terprogram
  </Card>
</CardGroup>