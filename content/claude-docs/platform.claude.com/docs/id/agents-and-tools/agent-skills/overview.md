---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 54575688b1e43da340bf21771eb9f1e94b614daa66f9d7f841c68e8296aff71d
---

# Agent Skills

Agent Skills adalah kemampuan modular yang memperluas fungsionalitas Claude. Setiap Skill mengemas instruksi, metadata, dan sumber daya opsional (skrip, templat) yang digunakan Claude secara otomatis saat relevan.

---

<Note>
  Untuk mengetahui bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

## Mengapa menggunakan Skills

Skills adalah sumber daya berbasis filesystem yang dapat digunakan kembali dan memberikan Claude keahlian spesifik domain: alur kerja, konteks, dan praktik terbaik yang mengubah agen serba guna menjadi spesialis. Berbeda dengan prompt (instruksi tingkat percakapan untuk tugas sekali pakai), Skills dimuat sesuai permintaan, sehingga Anda tidak perlu mengulangi panduan yang sama di berbagai percakapan.

**Manfaat utama:**

* **Spesialisasikan Claude:** Sesuaikan kemampuan untuk tugas spesifik domain
* **Kurangi pengulangan:** Buat sekali, gunakan secara otomatis
* **Komposisikan kemampuan:** Gabungkan Skills untuk tugas kompleks dan multilangkah

<Note>
  Untuk informasi lebih lanjut tentang arsitektur dan aplikasi dunia nyata dari Agent Skills, lihat postingan blog engineering [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
</Note>

## Menggunakan Skills

Anthropic menyediakan Agent Skills bawaan untuk tugas dokumen umum (PowerPoint, Excel, Word, PDF), dan Anda dapat membuat Skills kustom Anda sendiri. Keduanya bekerja dengan cara yang sama: setelah sebuah Skill tersedia di lingkungan Anda, Claude menggunakannya secara otomatis saat relevan dengan permintaan Anda.

**Agent Skills bawaan** tersedia di claude.ai, Claude API, [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Di Microsoft Foundry, Agent Skills memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure). Lihat [Skills yang tersedia](#available-skills) untuk daftar lengkapnya.

**Skills kustom** memungkinkan Anda mengemas keahlian domain dan pengetahuan organisasi. Skills ini tersedia di seluruh produk Claude: buat di Claude Code, unggah melalui Claude API, atau tambahkan di pengaturan claude.ai. Di [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws) dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry), unggah Skills kustom melalui Skills API.

<Note>
  **Mulai:**

  * Untuk Agent Skills bawaan: Lihat [tutorial quickstart](/docs/id/agents-and-tools/agent-skills/quickstart) untuk mulai menggunakan Skills PowerPoint, Excel, Word, dan PDF di API
  * Untuk Skills kustom: Lihat [Agent Skills Cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction) untuk mempelajari cara membuat Skills Anda sendiri
</Note>

## Cara kerja Skills

Skills menggunakan lingkungan VM Claude untuk menyediakan kemampuan di luar apa yang mungkin dilakukan dengan prompt saja. Claude beroperasi di mesin virtual dengan akses filesystem, memungkinkan Skills ada sebagai direktori yang berisi instruksi, kode yang dapat dieksekusi, dan materi referensi, yang diorganisir seperti panduan onboarding yang Anda buat untuk anggota tim baru.

Arsitektur berbasis filesystem ini memungkinkan **progressive disclosure** (pengungkapan bertahap): Claude memuat informasi secara bertahap sesuai kebutuhan, alih-alih mengonsumsi konteks di awal.

Skills dapat berisi tiga jenis konten, masing-masing dimuat pada waktu yang berbeda:

### Level 1: Metadata (selalu dimuat)

YAML frontmatter dari Skill menyediakan informasi penemuan:

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

Claude memuat metadata ini saat startup dan menyertakannya dalam prompt sistem. `description` adalah apa yang dicocokkan Claude dengan permintaan Anda saat menentukan apakah akan memicu Skill tersebut, sehingga harus menyatakan baik apa yang dilakukan Skill maupun kapan menggunakannya. Pendekatan ringan ini berarti Anda dapat memasang banyak Skills tanpa penalti konteks: sampai sebuah Skill dipicu, hanya nama dan deskripsinya yang menempati konteks.

### Level 2: Instruksi (dimuat saat dipicu)

Badan utama SKILL.md berisi pengetahuan prosedural: alur kerja, praktik terbaik, dan panduan:

````markdown
# PDF Processing

## Quick start

Use pdfplumber to extract text from PDFs:

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For advanced form filling, see [FORMS.md](FORMS.md).
````

Ketika Anda meminta sesuatu yang cocok dengan deskripsi sebuah Skill, Claude membaca SKILL.md dari filesystem menggunakan bash. Baru pada saat itulah konten ini masuk ke jendela konteks.

### Level 3: Sumber daya dan kode (dimuat sesuai kebutuhan)

Skills dapat membundel materi tambahan:

```text
pdf-processing/
├── SKILL.md (main instructions)
├── FORMS.md (form-filling guide)
├── REFERENCE.md (detailed API reference)
└── scripts/
    └── fill_form.py (utility script)
```

**Instruksi:** File markdown tambahan (FORMS.md, REFERENCE.md) yang berisi panduan dan alur kerja khusus

**Kode:** Skrip yang dapat dieksekusi (fill\_form.py, validate.py) yang dijalankan Claude menggunakan bash, menyediakan operasi deterministik tanpa memuat kodenya ke dalam konteks

**Sumber daya:** Materi referensi seperti skema database, dokumentasi API, templat, atau contoh

Claude mengakses file-file ini hanya saat direferensikan. Model filesystem berarti setiap jenis konten memiliki kekuatan yang berbeda: instruksi untuk panduan yang fleksibel, kode untuk keandalan, sumber daya untuk pencarian faktual.

| Level                     | Kapan dimuat          | Biaya token              | Konten                                                                                                                                            |
| ------------------------- | --------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Level 1: Metadata**     | Selalu (saat startup) | \~100 token per Skill    | `name` dan `description` dari YAML frontmatter                                                                                                    |
| **Level 2: Instruksi**    | Saat Skill dipicu     | Di bawah 5k token        | Badan SKILL.md dengan instruksi dan panduan                                                                                                       |
| **Level 3+: Sumber daya** | Sesuai kebutuhan      | Tidak ada sampai diakses | File yang dibundel. File referensi dimuat ke dalam konteks saat dibaca. Skrip dijalankan melalui bash, dan hanya output-nya yang masuk ke konteks |

Progressive disclosure memastikan hanya konten yang relevan yang menempati jendela konteks pada waktu tertentu.

### Arsitektur Skills

Skills berjalan di lingkungan eksekusi kode di mana Claude memiliki akses filesystem, perintah bash, dan kemampuan eksekusi kode. Skills ada sebagai direktori di mesin virtual, dan Claude berinteraksi dengannya menggunakan perintah bash yang sama yang Anda gunakan untuk menavigasi file di komputer Anda.

![Arsitektur Agent Skills - menunjukkan bagaimana Skills terintegrasi dengan konfigurasi agen dan mesin virtual](/docs/images/agent-skills-architecture.png)

**Bagaimana Claude mengakses konten Skill:**

Ketika sebuah Skill dipicu, Claude menggunakan bash untuk membaca SKILL.md dari filesystem, membawa instruksinya ke dalam jendela konteks. Jika instruksi tersebut mereferensikan file lain (seperti FORMS.md atau skema database), Claude membaca file-file tersebut juga menggunakan perintah bash tambahan. Ketika instruksi menyebutkan skrip yang dapat dieksekusi, Claude menjalankannya melalui bash dan hanya menerima output-nya (kode skrip itu sendiri tidak pernah masuk ke konteks).

**Apa yang dimungkinkan oleh arsitektur ini:**

* **Akses file sesuai permintaan:** Claude hanya membaca file yang dibutuhkan setiap tugas. Sebuah Skill dapat menyertakan puluhan file referensi, tetapi jika tugas Anda hanya membutuhkan skema penjualan, itulah satu-satunya file yang dimuat Claude. Sisanya tetap di filesystem dan tidak memakan token sama sekali.
* **Eksekusi skrip yang efisien:** Ketika Claude menjalankan `validate_form.py`, kode skrip tersebut tidak pernah dimuat ke dalam jendela konteks. Hanya output-nya (seperti "Validation passed" atau pesan kesalahan tertentu) yang mengonsumsi token, yang membuat skrip jauh lebih efisien daripada meminta Claude menghasilkan kode yang setara secara langsung.
* **Tidak ada batas praktis pada konten yang dibundel:** File tidak mengonsumsi konteks sampai diakses, sehingga Skills dapat menyertakan dokumentasi API yang komprehensif, dataset besar, atau contoh yang ekstensif. Tidak ada penalti konteks untuk konten yang dibundel yang tidak digunakan.

### Contoh: Memuat Skill pemrosesan PDF

Berikut adalah bagaimana Claude memuat dan menggunakan Skill kustom `pdf-processing` dari contoh sebelumnya (bukan Skill `pdf` bawaan):

1. **Startup:** Prompt sistem menyertakan: `pdf-processing - Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.`
2. **Permintaan pengguna:** "Ekstrak teks dari PDF ini dan rangkum"
3. **Claude memanggil:** `bash: cat pdf-processing/SKILL.md` → Instruksi dimuat ke dalam konteks
4. **Claude menentukan:** Pengisian formulir tidak diperlukan, sehingga FORMS.md tidak dibaca
5. **Claude mengeksekusi:** Menggunakan instruksi dari SKILL.md untuk menyelesaikan tugas

![Skills dimuat ke dalam context window (jendela konteks) - menunjukkan pemuatan bertahap metadata dan konten skill](/docs/images/agent-skills-context-window.png)

## Di mana Skills bekerja

Skills tersedia di seluruh produk agen Claude:

<Note>
  Claude Platform di AWS dan Microsoft Foundry mewarisi perilaku Skills yang sama dengan Claude API di semua bagian berikut.
</Note>

### Claude API

Claude API mendukung baik Agent Skills bawaan maupun Skills kustom. Keduanya bekerja secara identik: tentukan `skill_id` yang relevan dalam parameter `container` bersama dengan [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool).

**Prasyarat:** Menggunakan Skills melalui API memerlukan [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool), yang container-nya menjadi tempat Skills berjalan, dan satu header beta:

* `skills-2025-10-02` - Mengaktifkan fungsionalitas Skills

Tambahkan header kedua, `files-api-2025-04-14`, ketika Anda menggunakan [Files API](/docs/id/build-with-claude/files) untuk mengunggah file input ke container atau mengunduh file yang dihasilkan sebuah Skill.

Gunakan Agent Skills bawaan dengan mereferensikan `skill_id`-nya (`pptx`, `xlsx`, `docx`, atau `pdf`), atau buat dan unggah milik Anda sendiri melalui Skills API (endpoint `/v1/skills`). Skills kustom dibagikan ke seluruh workspace: semua anggota workspace dapat mengaksesnya.

Skills di API berjalan dalam container sandbox tanpa akses jaringan dan tanpa instalasi paket saat runtime. Lihat [Keterbatasan dan kendala](#limitations-and-constraints) untuk detailnya.

Untuk mempelajari lebih lanjut, lihat [Menggunakan Agent Skills dengan API](/docs/id/build-with-claude/skills-guide).

### Claude Code

[Claude Code](https://code.claude.com/docs/id/overview) mendukung Skills kustom. Skills dokumen bawaan (PowerPoint, Excel, Word, PDF) tidak tersedia di Claude Code, meskipun [Claude API skill](/docs/id/agents-and-tools/agent-skills/claude-api-skill) yang open-source sudah dibundel dengannya. Lihat daftar lengkap [perintah dan Skills bawaan](https://code.claude.com/docs/id/commands) yang disertakan dengan Claude Code.

**Skills kustom:** Buat Skills sebagai direktori dengan file SKILL.md. Claude menemukan dan menggunakannya secara otomatis.

Skills kustom di Claude Code berbasis filesystem dan tidak memerlukan unggahan API: tempatkan di `~/.claude/skills/` (pribadi) atau `.claude/skills/` (proyek).

Untuk mempelajari lebih lanjut, lihat [Menggunakan Skills di Claude Code](https://code.claude.com/docs/id/skills).

### claude.ai

[claude.ai](https://claude.ai) mendukung baik Agent Skills bawaan maupun Skills kustom.

**Agent Skills bawaan:** Skills ini aktif saat Anda membuat dokumen. Claude menggunakannya tanpa perlu pengaturan apa pun.

**Skills kustom:** Unggah Skills Anda sendiri sebagai file zip melalui Settings > Features. Tersedia pada paket Pro, Max, Team, dan Enterprise dengan [eksekusi kode diaktifkan](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude). Skills kustom bersifat individual untuk setiap pengguna. Skills ini tidak dibagikan ke seluruh organisasi dan tidak dapat dikelola secara terpusat oleh admin.

Untuk mempelajari lebih lanjut tentang menggunakan Skills di claude.ai, lihat sumber daya berikut di Claude Help Center:

* [Apa itu Skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
* [Menggunakan Skills di Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
* [Cara membuat Skills kustom](https://support.claude.com/en/articles/12512198-creating-custom-skills)
* [Ajarkan Claude cara kerja Anda menggunakan Skills](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills)

## Struktur Skill

Setiap Skill memerlukan file `SKILL.md` dengan YAML frontmatter:

```markdown
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
[Clear, step-by-step guidance for Claude to follow]

## Examples
[Concrete examples of using this Skill]
```

**Field wajib:** `name` dan `description`

**Persyaratan field:**

`name`:

* Maksimum 64 karakter
* Hanya boleh berisi huruf kecil, angka, dan tanda hubung
* Tidak boleh berisi tag XML
* Tidak boleh berisi kata yang dicadangkan: "anthropic", "claude"

`description`:

* Tidak boleh kosong
* Maksimum 1024 karakter
* Tidak boleh berisi tag XML

`description` harus mencakup baik apa yang dilakukan Skill maupun kapan Claude harus menggunakannya. Untuk panduan penulisan lengkap, lihat [Praktik terbaik penulisan Skill](/docs/id/agents-and-tools/agent-skills/best-practices).

## Pertimbangan keamanan

Gunakan Skills hanya dari sumber tepercaya: yang Anda buat sendiri atau yang diperoleh dari Anthropic. Skills memberikan Claude kemampuan baru melalui instruksi dan kode, yang juga berarti Skill berbahaya dapat mengarahkan Claude untuk memanggil alat atau mengeksekusi kode dengan cara yang tidak sesuai dengan tujuan yang dinyatakan Skill tersebut.

<Warning>
  Jika Anda harus menggunakan Skill dari sumber yang tidak tepercaya atau tidak dikenal, berhati-hatilah secara ekstrem dan audit secara menyeluruh sebelum digunakan. Tergantung pada akses apa yang dimiliki Claude saat mengeksekusi Skill, Skills berbahaya dapat menyebabkan eksfiltrasi data, akses sistem yang tidak sah, atau risiko keamanan lainnya.
</Warning>

**Pertimbangan keamanan utama:**

* **Audit secara menyeluruh:** Tinjau semua file yang dibundel dalam Skill: SKILL.md, skrip, gambar, dan sumber daya lainnya. Cari pola yang tidak biasa seperti panggilan jaringan yang tidak terduga, pola akses file, atau operasi yang tidak sesuai dengan tujuan yang dinyatakan Skill
* **Sumber eksternal berisiko:** Skills yang mengambil data dari URL eksternal menimbulkan risiko khusus, karena konten yang diambil dapat berisi instruksi berbahaya. Bahkan Skills yang dapat dipercaya dapat dikompromikan jika dependensi eksternalnya berubah seiring waktu
* **Penyalahgunaan alat:** Skills berbahaya dapat memanggil alat (operasi file, perintah bash, eksekusi kode) dengan cara yang merugikan
* **Paparan data:** Skills dengan akses ke data sensitif dapat dirancang untuk membocorkan informasi ke sistem eksternal
* **Perlakukan seperti memasang perangkat lunak:** Berhati-hatilah secara khusus saat mengintegrasikan Skills ke dalam sistem produksi dengan akses ke data sensitif atau operasi kritis

Untuk panduan tata kelola, pemeriksaan, dan deployment skala organisasi, lihat [Skills untuk enterprise](/docs/id/agents-and-tools/agent-skills/enterprise).

## Skills yang tersedia

### Agent Skills bawaan

Agent Skills bawaan berikut tersedia untuk langsung digunakan:

* **PowerPoint (pptx):** Membuat presentasi, mengedit slide, menganalisis konten presentasi
* **Excel (xlsx):** Membuat spreadsheet, menganalisis data, menghasilkan laporan dengan grafik
* **Word (docx):** Membuat dokumen, mengedit konten, memformat teks
* **PDF (pdf):** Menghasilkan dokumen dan laporan PDF yang terformat

Skills ini tersedia di Claude API, [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws), [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry), dan claude.ai. Lihat [tutorial quickstart](/docs/id/agents-and-tools/agent-skills/quickstart) untuk mulai menggunakannya di API.

### Skills open-source

Anthropic juga menerbitkan Skills open-source di [repositori skills](https://github.com/anthropics/skills):

* **[Claude API skill](/docs/id/agents-and-tools/agent-skills/claude-api-skill):** Menyediakan Claude dengan materi referensi API terkini, dokumentasi SDK, dan praktik terbaik untuk delapan bahasa pemrograman. Dibundel dengan Claude Code dan juga tersedia untuk instalasi dari repositori skills.

### Contoh Skills kustom

Untuk contoh lengkap Skills kustom, lihat [Skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction).

## Retensi data

Agent Skills tidak tercakup dalam pengaturan ZDR. Definisi Skill dan data eksekusi disimpan sesuai dengan kebijakan retensi data standar Anthropic.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Keterbatasan dan kendala

Claude Platform di AWS dan Microsoft Foundry mengikuti keterbatasan yang sama dengan Claude API di subbagian berikut.

### Ketersediaan lintas permukaan

**Skills kustom tidak tersinkronisasi antar permukaan**. Skills yang diunggah ke satu permukaan tidak secara otomatis tersedia di permukaan lainnya:

* Skills yang diunggah ke claude.ai harus diunggah secara terpisah ke API
* Skills yang diunggah melalui API tidak tersedia di claude.ai
* Skills Claude Code berbasis filesystem dan terpisah dari claude.ai maupun API

Kelola dan unggah Skills secara terpisah untuk setiap permukaan di mana Anda ingin menggunakannya.

### Cakupan berbagi

Skills memiliki model berbagi yang berbeda tergantung di mana Anda menggunakannya:

* **claude.ai:** Hanya pengguna individual. Setiap anggota tim harus mengunggah secara terpisah.
* **Claude API:** Seluruh workspace. Semua anggota workspace dapat mengakses Skills yang diunggah.
* **Claude Code:** Pribadi (`~/.claude/skills/`) atau berbasis proyek (`.claude/skills/`). Juga dapat dibagikan melalui Claude Code Plugins.

claude.ai tidak mendukung manajemen admin terpusat atau distribusi Skills kustom ke seluruh organisasi.

### Kendala lingkungan runtime

Lingkungan runtime yang tepat yang tersedia untuk Skill Anda tergantung pada permukaan produk di mana Anda menggunakannya.

* **claude.ai:**
  * **Akses jaringan bervariasi:** Tergantung pada pengaturan pengguna/admin, Skills mungkin memiliki akses jaringan penuh, sebagian, atau tidak sama sekali. Untuk detail lebih lanjut, lihat artikel dukungan [Create and Edit Files](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude#h_6b7e833898).

* **Claude API:**

  * **Tidak ada akses jaringan:** Skills tidak dapat melakukan panggilan API eksternal atau mengakses internet.
  * **Tidak ada instalasi paket saat runtime:** Hanya paket yang sudah terpasang sebelumnya yang tersedia. Anda tidak dapat memasang paket baru selama eksekusi.
  * **Hanya dependensi yang telah dikonfigurasi sebelumnya:** Periksa dokumentasi [Alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk daftar paket yang tersedia.

* **Claude Code:**

  * **Akses jaringan penuh:** Skills memiliki akses jaringan yang sama seperti program lain di komputer pengguna.
  * **Instalasi paket global tidak disarankan:** Skills sebaiknya hanya memasang paket secara lokal untuk menghindari gangguan pada komputer pengguna.

Rencanakan Skills Anda agar bekerja dalam kendala-kendala ini.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mulai dengan Agent Skills di API" icon="graduation-cap" href="/docs/id/agents-and-tools/agent-skills/quickstart">
    Pelajari cara menggunakan Agent Skills untuk membuat dokumen dengan Claude API dalam waktu kurang dari 10 menit.
  </Card>

  <Card title="Menggunakan Agent Skills dengan API" icon="code" href="/docs/id/build-with-claude/skills-guide">
    Pelajari cara menggunakan Agent Skills untuk memperluas kemampuan Claude melalui API.
  </Card>

  <Card title="Menggunakan Skills di Claude Code" icon="terminal" href="https://code.claude.com/docs/id/skills">
    Buat dan kelola Skills kustom di Claude Code.
  </Card>

  <Card title="Praktik terbaik penulisan Skill" icon="lightbulb" href="/docs/id/agents-and-tools/agent-skills/best-practices">
    Pelajari cara menulis Skills yang efektif yang dapat ditemukan dan digunakan Claude dengan sukses.
  </Card>
</CardGroup>
