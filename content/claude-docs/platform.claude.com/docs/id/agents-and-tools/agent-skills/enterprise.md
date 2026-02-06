---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/enterprise
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 76f762ebb2923c27df99866fc419cda16ae7999934d3c3ed3d8d193229f33cdb
---

# Keterampilan untuk perusahaan

Tata kelola, tinjauan keamanan, evaluasi, dan panduan organisasi untuk menerapkan Agent Skills pada skala perusahaan.

---

Panduan ini ditujukan untuk admin perusahaan dan arsitek yang perlu mengatur Agent Skills di seluruh organisasi. Panduan ini mencakup cara memverifikasi, mengevaluasi, menerapkan, dan mengelola Skills dalam skala besar. Untuk panduan penulisan, lihat [praktik terbaik](/docs/id/agents-and-tools/agent-skills/best-practices). Untuk detail arsitektur, lihat [ringkasan Skills](/docs/id/agents-and-tools/agent-skills/overview).

## Tinjauan keamanan dan verifikasi

Menerapkan Skills di perusahaan memerlukan menjawab dua pertanyaan yang berbeda:

1. **Apakah Skills aman secara umum?** Lihat bagian [pertimbangan keamanan](/docs/id/agents-and-tools/agent-skills/overview#security-considerations) dalam ringkasan untuk detail keamanan tingkat platform.
2. **Bagaimana cara saya memverifikasi Skill tertentu?** Gunakan penilaian risiko dan daftar periksa tinjauan di bawah ini.

### Penilaian tingkat risiko

Evaluasi setiap Skill terhadap indikator risiko ini sebelum menyetujui penerapan:

| Indikator risiko | Apa yang harus dicari | Tingkat kekhawatiran |
|---|---|---|
| Eksekusi kode | Skrip di direktori Skill (`*.py`, `*.sh`, `*.js`) | Tinggi: skrip berjalan dengan akses lingkungan penuh |
| Manipulasi instruksi | Arahan untuk mengabaikan aturan keamanan, menyembunyikan tindakan dari pengguna, atau mengubah perilaku Claude secara kondisional | Tinggi: dapat melewati kontrol keamanan |
| Referensi server MCP | Instruksi yang mereferensikan alat MCP (`ServerName:tool_name`) | Tinggi: memperluas akses di luar Skill itu sendiri |
| Pola akses jaringan | URL, titik akhir API, panggilan `fetch`, `curl`, atau `requests` | Tinggi: vektor potensi eksfiltrasi data |
| Kredensial hardcoded | Kunci API, token, atau kata sandi dalam file Skill atau skrip | Tinggi: rahasia terekspos dalam riwayat Git dan jendela konteks |
| Cakupan akses sistem file | Jalur di luar direktori Skill, pola glob luas, traversal jalur (`../`) | Sedang: dapat mengakses data yang tidak dimaksudkan |
| Invokasi alat | Instruksi yang mengarahkan Claude untuk menggunakan bash, operasi file, atau alat lainnya | Sedang: tinjau operasi apa yang dilakukan |

### Daftar periksa tinjauan

Sebelum menerapkan Skill apa pun dari pihak ketiga atau kontributor internal, selesaikan langkah-langkah berikut:

1. **Baca semua konten direktori Skill.** Tinjau SKILL.md, semua file markdown yang direferensikan, dan skrip atau sumber daya bundel apa pun.
2. **Verifikasi perilaku skrip sesuai dengan tujuan yang dinyatakan.** Jalankan skrip di lingkungan terisolasi dan konfirmasi output selaras dengan deskripsi Skill.
3. **Periksa instruksi yang bersifat adversarial.** Cari arahan yang menyuruh Claude mengabaikan aturan keamanan, menyembunyikan tindakan dari pengguna, mengeksfiltrasi data melalui respons, atau mengubah perilaku berdasarkan input tertentu.
4. **Periksa pengambilan URL eksternal atau panggilan jaringan.** Cari skrip dan instruksi untuk pola akses jaringan (`http`, `requests.get`, `urllib`, `curl`, `fetch`).
5. **Verifikasi tidak ada kredensial hardcoded.** Periksa kunci API, token, atau kata sandi dalam file Skill. Kredensial harus menggunakan variabel lingkungan atau penyimpanan kredensial aman, tidak pernah muncul dalam konten Skill.
6. **Identifikasi alat dan perintah yang diperintahkan Skill kepada Claude untuk dijalankan.** Buat daftar semua perintah bash, operasi file, dan referensi alat. Pertimbangkan risiko gabungan ketika Skill menggunakan alat pembacaan file dan jaringan bersama-sama.
7. **Konfirmasi tujuan pengalihan.** Jika Skill mereferensikan URL eksternal, verifikasi bahwa mereka menunjuk ke domain yang diharapkan.
8. **Verifikasi tidak ada pola eksfiltrasi data.** Cari instruksi yang membaca data sensitif dan kemudian menulis, mengirim, atau mengkodekannya untuk transmisi eksternal, termasuk melalui respons percakapan Claude.

<Warning>
Jangan pernah menerapkan Skills dari sumber yang tidak terpercaya tanpa audit lengkap. Skill yang berbahaya dapat mengarahkan Claude untuk menjalankan kode arbitrer, mengakses file sensitif, atau mengirimkan data secara eksternal. Perlakukan instalasi Skill dengan ketelitian yang sama seperti menginstal perangkat lunak pada sistem produksi.
</Warning>

## Mengevaluasi Skills sebelum penerapan

Skills dapat menurunkan kinerja agen jika mereka dipicu secara tidak benar, bertentangan dengan Skills lain, atau memberikan instruksi yang buruk. Perlukan evaluasi sebelum penerapan produksi apa pun.

### Apa yang harus dievaluasi

Tetapkan gerbang persetujuan untuk dimensi ini sebelum menerapkan Skill apa pun:

| Dimensi | Apa yang diukur | Contoh kegagalan |
|---|---|---|
| Akurasi pemicu | Apakah Skill diaktifkan untuk kueri yang tepat dan tetap tidak aktif untuk kueri yang tidak terkait? | Skill dipicu pada setiap penyebutan spreadsheet, bahkan ketika pengguna hanya ingin membahas data |
| Perilaku isolasi | Apakah Skill berfungsi dengan benar sendiri? | Skill mereferensikan file yang tidak ada di direktorinya |
| Koeksistensi | Apakah menambahkan Skill ini menurunkan Skills lain? | Deskripsi Skill baru terlalu luas, mencuri pemicu dari Skills yang ada |
| Mengikuti instruksi | Apakah Claude mengikuti instruksi Skill dengan akurat? | Claude melewati langkah validasi atau menggunakan perpustakaan yang salah |
| Kualitas output | Apakah Skill menghasilkan hasil yang benar dan berguna? | Laporan yang dihasilkan memiliki kesalahan pemformatan atau data yang hilang |

### Persyaratan evaluasi

Perlukan penulis Skill untuk mengirimkan suite evaluasi dengan 3-5 kueri perwakilan per Skill, mencakup kasus di mana Skill harus dipicu, tidak boleh dipicu, dan kasus tepi yang ambigu. Perlukan pengujian di seluruh model yang digunakan organisasi Anda (Haiku, Sonnet, Opus), karena efektivitas Skill bervariasi menurut model.

Untuk panduan terperinci tentang membangun evaluasi, lihat [evaluasi dan iterasi](/docs/id/agents-and-tools/agent-skills/best-practices#evaluation-and-iteration) dalam praktik terbaik. Untuk metodologi evaluasi umum, lihat [mengembangkan kasus uji](/docs/id/test-and-evaluate/develop-tests).

### Menggunakan evaluasi untuk keputusan siklus hidup

Hasil evaluasi menandakan kapan harus bertindak:

- **Akurasi pemicu menurun:** Perbarui deskripsi atau instruksi Skill
- **Konflik koeksistensi:** Konsolidasikan Skills yang tumpang tindih atau persempit deskripsi
- **Kualitas output konsisten rendah:** Tulis ulang instruksi atau tambahkan langkah validasi
- **Kegagalan persisten di seluruh pembaruan:** Hentikan Skill

## Manajemen siklus hidup Skill

<Steps>
  <Step title="Rencanakan">
    Identifikasi alur kerja yang berulang, rawan kesalahan, atau memerlukan pengetahuan khusus. Petakan ini ke peran organisasi dan tentukan mana yang merupakan kandidat untuk Skills.
  </Step>
  <Step title="Buat dan tinjau">
    Pastikan penulis Skill mengikuti [praktik terbaik](/docs/id/agents-and-tools/agent-skills/best-practices). Perlukan tinjauan keamanan menggunakan [daftar periksa tinjauan](#review-checklist) di atas. Perlukan suite evaluasi sebelum persetujuan. Tetapkan pemisahan tugas: penulis Skill tidak boleh menjadi peninjau mereka sendiri.
  </Step>
  <Step title="Uji">
    Perlukan evaluasi secara terisolasi (Skill sendiri) dan bersama Skills yang ada (pengujian koeksistensi). Verifikasi akurasi pemicu, kualitas output, dan tidak adanya regresi di seluruh set Skill aktif Anda sebelum menyetujui untuk produksi.
  </Step>
  <Step title="Terapkan">
    Unggah melalui Skills API untuk akses di seluruh ruang kerja. Lihat [Menggunakan Skills dengan API](/docs/id/build-with-claude/skills-guide) untuk manajemen unggahan dan versi. Dokumentasikan Skill dalam registri internal Anda dengan tujuan, pemilik, dan versi.
  </Step>
  <Step title="Pantau">
    Lacak pola penggunaan dan kumpulkan umpan balik dari pengguna. Jalankan kembali evaluasi secara berkala untuk mendeteksi pergeseran atau regresi saat alur kerja dan model berkembang. Analitik penggunaan saat ini tidak tersedia melalui Skills API. Implementasikan pencatatan tingkat aplikasi untuk melacak Skills mana yang disertakan dalam permintaan.
  </Step>
  <Step title="Iterasi atau hentikan">
    Perlukan suite evaluasi lengkap untuk lulus sebelum mempromosikan versi baru. Perbarui Skills ketika alur kerja berubah atau skor evaluasi menurun. Hentikan Skills ketika evaluasi secara konsisten gagal atau alur kerja dihentikan.
  </Step>
</Steps>

## Mengorganisir Skills dalam skala besar

### Batas penarikan kembali

Sebagai pedoman umum, batasi jumlah Skills yang dimuat secara bersamaan untuk mempertahankan akurasi penarikan kembali yang andal. Metadata setiap Skill (nama dan deskripsi) bersaing untuk perhatian dalam prompt sistem. Dengan terlalu banyak Skills aktif, Claude mungkin gagal memilih Skill yang tepat atau melewatkan yang relevan sepenuhnya. Gunakan suite evaluasi Anda untuk mengukur akurasi penarikan kembali saat Anda menambahkan Skills, dan berhenti menambahkan ketika kinerja menurun.

Perhatikan bahwa permintaan API mendukung maksimal 8 Skills per permintaan (lihat [Menggunakan Skills dengan API](/docs/id/build-with-claude/skills-guide)). Jika peran memerlukan lebih banyak Skills daripada yang didukung permintaan tunggal, pertimbangkan untuk menggabungkan Skills sempit menjadi yang lebih luas atau merutekan permintaan ke set Skill yang berbeda berdasarkan jenis tugas.

### Mulai spesifik, konsolidasikan nanti

Dorong tim untuk memulai dengan Skills yang sempit dan spesifik alur kerja daripada yang luas dan multi-tujuan. Saat pola muncul di seluruh organisasi Anda, konsolidasikan Skills terkait menjadi bundel berbasis peran.

<Tip>
Gunakan evaluasi untuk memutuskan kapan harus menggabungkan. Gabungkan Skills sempit menjadi yang lebih luas hanya ketika evaluasi Skill yang dikonsolidasikan mengkonfirmasi kinerja setara dengan Skills individual yang digantikannya.
</Tip>

**Contoh perkembangan**:
- Mulai: `formatting-sales-reports`, `querying-pipeline-data`, `updating-crm-records`
- Konsolidasikan: `sales-operations` (ketika evals mengkonfirmasi kinerja setara)

### Penamaan dan katalogisasi

Gunakan konvensi penamaan yang konsisten di seluruh organisasi Anda. Bagian [konvensi penamaan](/docs/id/agents-and-tools/agent-skills/best-practices#naming-conventions) dalam praktik terbaik memberikan panduan pemformatan.

Pertahankan registri internal untuk setiap Skill dengan:
- **Tujuan**: Alur kerja apa yang didukung Skill
- **Pemilik**: Tim atau individu yang bertanggung jawab atas pemeliharaan
- **Versi**: Versi yang saat ini diterapkan
- **Dependensi**: Server MCP, paket, atau layanan eksternal yang diperlukan
- **Status evaluasi**: Tanggal evaluasi terakhir dan hasil

### Bundel berbasis peran

Kelompokkan Skills menurut peran organisasi untuk menjaga set Skill aktif setiap pengguna tetap fokus:

- **Tim penjualan**: Operasi CRM, pelaporan pipeline, pembuatan proposal
- **Teknik**: Tinjauan kode, alur kerja penerapan, respons insiden
- **Keuangan**: Pembuatan laporan, validasi data, persiapan audit

Setiap bundel berbasis peran harus berisi hanya Skills yang relevan dengan alur kerja harian peran tersebut.

## Distribusi dan kontrol versi

### Kontrol sumber

Simpan direktori Skill di Git untuk pelacakan riwayat, tinjauan kode melalui permintaan tarik, dan kemampuan rollback. Setiap direktori Skill (berisi SKILL.md dan file bundel apa pun) memetakan secara alami ke folder yang dilacak Git.

### Distribusi berbasis API

Skills API menyediakan distribusi dengan cakupan ruang kerja. Skills yang diunggah melalui API tersedia untuk semua anggota ruang kerja. Lihat [Menggunakan Skills dengan API](/docs/id/build-with-claude/skills-guide) untuk unggahan, versioning, dan titik akhir manajemen.

### Strategi versioning

- **Produksi**: Sematkan Skills ke versi tertentu. Jalankan suite evaluasi lengkap sebelum mempromosikan versi baru. Perlakukan setiap pembaruan sebagai penerapan baru yang memerlukan tinjauan keamanan lengkap.
- **Pengembangan dan pengujian**: Gunakan versi terbaru untuk memvalidasi perubahan sebelum promosi produksi.
- **Rencana rollback**: Pertahankan versi sebelumnya sebagai fallback. Jika versi baru gagal evaluasi dalam produksi, kembalikan ke versi terakhir yang dikenal baik segera.
- **Verifikasi integritas**: Hitung checksum Skills yang ditinjau dan verifikasi saat waktu penerapan. Gunakan commit yang ditandatangani dalam repositori Skill Anda untuk memastikan provenance.

### Pertimbangan lintas permukaan

<Warning>
Custom Skills tidak disinkronkan di seluruh permukaan. Skills yang diunggah ke API tidak tersedia di claude.ai atau di Claude Code, dan sebaliknya. Setiap permukaan memerlukan unggahan dan manajemen terpisah.
</Warning>

Pertahankan file sumber Skill di Git sebagai sumber kebenaran tunggal. Jika organisasi Anda menerapkan Skills di beberapa permukaan, implementasikan proses sinkronisasi Anda sendiri untuk menjaganya tetap konsisten. Untuk detail lengkap, lihat [ketersediaan lintas permukaan](/docs/id/agents-and-tools/agent-skills/overview#cross-surface-availability).

## Langkah berikutnya

<CardGroup cols={2}>
  <Card
    title="Ringkasan Agent Skills"
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
  <Card
    title="Menerapkan agen AI dengan aman"
    icon="shield"
    href="/docs/id/agent-sdk/secure-deployment"
  >
    Pola keamanan untuk penerapan agen
  </Card>
</CardGroup>