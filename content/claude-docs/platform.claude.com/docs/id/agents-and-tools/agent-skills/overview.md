---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview
fetched_at: 2026-03-27T03:10:39.282195Z
sha256: b34f98899ccbc9b462e38cfb4c834d89381be512b9438292208eb7077fdcfdf8
---

# Agent Skills

Agent Skills adalah kemampuan modular yang memperluas fungsionalitas Claude. Setiap Skill mengemas instruksi, metadata, dan sumber daya opsional (skrip, template) yang digunakan Claude secara otomatis saat relevan.

---

<Note>
This feature is **not** eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). Data is retained according to the feature's standard retention policy.
</Note>

## Mengapa menggunakan Skills

Skills adalah sumber daya berbasis filesystem yang dapat digunakan kembali dan memberikan Claude keahlian domain-spesifik: alur kerja, konteks, dan praktik terbaik yang mengubah agen serba guna menjadi spesialis. Tidak seperti prompt (instruksi tingkat percakapan untuk tugas satu kali), Skills dimuat sesuai permintaan dan menghilangkan kebutuhan untuk berulang kali memberikan panduan yang sama di berbagai percakapan.

**Manfaat utama**:
- **Spesialisasi Claude**: Menyesuaikan kemampuan untuk tugas domain-spesifik
- **Mengurangi pengulangan**: Buat sekali, gunakan secara otomatis
- **Menggabungkan kemampuan**: Kombinasikan Skills untuk membangun alur kerja yang kompleks

<Note>
Untuk pendalaman arsitektur dan aplikasi dunia nyata dari Agent Skills, baca blog teknik kami: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
</Note>

## Menggunakan Skills

Anthropic menyediakan Agent Skills bawaan untuk tugas dokumen umum (PowerPoint, Excel, Word, PDF), dan Anda dapat membuat Skills kustom sendiri. Keduanya bekerja dengan cara yang sama. Claude menggunakannya secara otomatis saat relevan dengan permintaan Anda.

**Agent Skills bawaan** tersedia untuk semua pengguna di claude.ai dan melalui Claude API. Lihat bagian [Skills yang Tersedia](#available-skills) di bawah untuk daftar lengkapnya.

**Custom Skills** memungkinkan Anda mengemas keahlian domain dan pengetahuan organisasi. Tersedia di seluruh produk Claude: buat di Claude Code, unggah melalui API, atau tambahkan di pengaturan claude.ai.

<Note>
**Mulai:**
- Untuk Agent Skills bawaan: Lihat [tutorial quickstart](/docs/id/agents-and-tools/agent-skills/quickstart) untuk mulai menggunakan skill PowerPoint, Excel, Word, dan PDF di API
- Untuk custom Skills: Lihat [Agent Skills Cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction) untuk mempelajari cara membuat Skills Anda sendiri
</Note>

## Cara kerja Skills

Skills memanfaatkan lingkungan VM Claude untuk menyediakan kemampuan di luar apa yang mungkin dilakukan dengan prompt saja. Claude beroperasi dalam mesin virtual dengan akses filesystem, memungkinkan Skills ada sebagai direktori yang berisi instruksi, kode yang dapat dieksekusi, dan materi referensi, diorganisir seperti panduan orientasi yang akan Anda buat untuk anggota tim baru.

Arsitektur berbasis filesystem ini memungkinkan **pengungkapan progresif**: Claude memuat informasi secara bertahap sesuai kebutuhan, daripada mengonsumsi konteks di awal.

### Tiga jenis konten Skill, tiga tingkat pemuatan

Skills dapat berisi tiga jenis konten, masing-masing dimuat pada waktu yang berbeda:

### Level 1: Metadata (selalu dimuat)

**Jenis konten: Instruksi**. Frontmatter YAML Skill menyediakan informasi penemuan:

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

Claude memuat metadata ini saat startup dan menyertakannya dalam system prompt. Pendekatan ringan ini berarti Anda dapat menginstal banyak Skills tanpa penalti konteks; Claude hanya mengetahui setiap Skill ada dan kapan menggunakannya.

### Level 2: Instruksi (dimuat saat dipicu)

**Jenis konten: Instruksi**. Isi utama SKILL.md berisi pengetahuan prosedural: alur kerja, praktik terbaik, dan panduan:

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

Ketika Anda meminta sesuatu yang cocok dengan deskripsi Skill, Claude membaca SKILL.md dari filesystem melalui bash. Baru kemudian konten ini masuk ke jendela konteks.

### Level 3: Sumber daya dan kode (dimuat sesuai kebutuhan)

**Jenis konten: Instruksi, kode, dan sumber daya**. Skills dapat menyertakan materi tambahan:

```text
pdf-skill/
├── SKILL.md (main instructions)
├── FORMS.md (form-filling guide)
├── REFERENCE.md (detailed API reference)
└── scripts/
    └── fill_form.py (utility script)
```

**Instruksi**: File markdown tambahan (FORMS.md, REFERENCE.md) yang berisi panduan dan alur kerja khusus

**Kode**: Skrip yang dapat dieksekusi (fill_form.py, validate.py) yang dijalankan Claude melalui bash; skrip menyediakan operasi deterministik tanpa mengonsumsi konteks

**Sumber daya**: Materi referensi seperti skema database, dokumentasi API, template, atau contoh

Claude mengakses file-file ini hanya saat direferensikan. Model filesystem berarti setiap jenis konten memiliki kekuatan yang berbeda: instruksi untuk panduan fleksibel, kode untuk keandalan, sumber daya untuk pencarian faktual.

| Level | Kapan Dimuat | Biaya Token | Konten |
|-------|------------|------------|---------|
| **Level 1: Metadata** | Selalu (saat startup) | ~100 token per Skill | `name` dan `description` dari frontmatter YAML |
| **Level 2: Instruksi** | Saat Skill dipicu | Di bawah 5k token | Isi SKILL.md dengan instruksi dan panduan |
| **Level 3+: Sumber daya** | Sesuai kebutuhan | Efektif tidak terbatas | File yang dibundel dieksekusi melalui bash tanpa memuat konten ke dalam konteks |

Pengungkapan progresif memastikan hanya konten skill yang relevan yang menempati jendela konteks pada waktu tertentu.

### Arsitektur Skills

Skills berjalan di lingkungan eksekusi kode di mana Claude memiliki akses filesystem, perintah bash, dan kemampuan eksekusi kode. Bayangkan seperti ini: Skills ada sebagai direktori di mesin virtual, dan Claude berinteraksi dengannya menggunakan perintah bash yang sama yang Anda gunakan untuk menavigasi file di komputer Anda.

![Arsitektur Agent Skills - menunjukkan bagaimana Skills terintegrasi dengan konfigurasi agen dan mesin virtual](/docs/images/agent-skills-architecture.png)

**Cara Claude mengakses konten Skill:**

Ketika sebuah Skill dipicu, Claude menggunakan bash untuk membaca SKILL.md dari filesystem, membawa instruksinya ke dalam jendela konteks. Jika instruksi tersebut mereferensikan file lain (seperti FORMS.md atau skema database), Claude membaca file-file tersebut juga menggunakan perintah bash tambahan. Ketika instruksi menyebutkan skrip yang dapat dieksekusi, Claude menjalankannya melalui bash dan hanya menerima outputnya (kode skrip itu sendiri tidak pernah masuk ke konteks).

**Apa yang diaktifkan oleh arsitektur ini:**

**Akses file sesuai permintaan**: Claude hanya membaca file yang diperlukan untuk setiap tugas tertentu. Sebuah Skill dapat menyertakan lusinan file referensi, tetapi jika tugas Anda hanya membutuhkan skema penjualan, Claude hanya memuat file tersebut. Sisanya tetap di filesystem mengonsumsi nol token.

**Eksekusi skrip yang efisien**: Ketika Claude menjalankan `validate_form.py`, kode skrip tidak pernah dimuat ke dalam jendela konteks. Hanya output skrip (seperti "Validation passed" atau pesan kesalahan tertentu) yang mengonsumsi token. Ini membuat skrip jauh lebih efisien daripada meminta Claude menghasilkan kode yang setara secara langsung.

**Tidak ada batas praktis pada konten yang dibundel**: Karena file tidak mengonsumsi konteks sampai diakses, Skills dapat menyertakan dokumentasi API yang komprehensif, dataset besar, contoh yang luas, atau materi referensi apa pun yang Anda butuhkan. Tidak ada penalti konteks untuk konten yang dibundel yang tidak digunakan.

Model berbasis filesystem inilah yang membuat pengungkapan progresif bekerja. Claude menavigasi Skill Anda seperti Anda mereferensikan bagian tertentu dari panduan orientasi, mengakses tepat apa yang dibutuhkan setiap tugas.

### Contoh: Memuat skill pemrosesan PDF

Berikut cara Claude memuat dan menggunakan skill pemrosesan PDF:

1. **Startup**: System prompt menyertakan: `PDF Processing - Extract text and tables from PDF files, fill forms, merge documents`
2. **Permintaan pengguna**: "Ekstrak teks dari PDF ini dan rangkum"
3. **Claude memanggil**: `bash: read pdf-skill/SKILL.md` → Instruksi dimuat ke dalam konteks
4. **Claude menentukan**: Pengisian formulir tidak diperlukan, sehingga FORMS.md tidak dibaca
5. **Claude mengeksekusi**: Menggunakan instruksi dari SKILL.md untuk menyelesaikan tugas

![Skills dimuat ke dalam jendela konteks - menunjukkan pemuatan progresif metadata dan konten skill](/docs/images/agent-skills-context-window.png)

Diagram menunjukkan:
1. Status default dengan system prompt dan metadata skill yang sudah dimuat sebelumnya
2. Claude memicu skill dengan membaca SKILL.md melalui bash
3. Claude secara opsional membaca file tambahan yang dibundel seperti FORMS.md sesuai kebutuhan
4. Claude melanjutkan dengan tugas

Pemuatan dinamis ini memastikan hanya konten skill yang relevan yang menempati jendela konteks.

## Di mana Skills bekerja

Skills tersedia di seluruh produk agen Claude:

### Claude API

Claude API mendukung Agent Skills bawaan dan custom Skills. Keduanya bekerja secara identik: tentukan `skill_id` yang relevan dalam parameter `container` bersama dengan tool eksekusi kode.

**Prasyarat**: Menggunakan Skills melalui API memerlukan tiga header beta:
- `code-execution-2025-08-25` - Skills berjalan di container eksekusi kode
- `skills-2025-10-02` - Mengaktifkan fungsionalitas Skills
- `files-api-2025-04-14` - Diperlukan untuk mengunggah/mengunduh file ke/dari container

Gunakan Agent Skills bawaan dengan mereferensikan `skill_id`-nya (misalnya, `pptx`, `xlsx`), atau buat dan unggah milik Anda sendiri melalui Skills API (endpoint `/v1/skills`). Custom Skills dibagikan di seluruh organisasi.

Untuk mempelajari lebih lanjut, lihat [Gunakan Skills dengan Claude API](/docs/id/build-with-claude/skills-guide).

### Claude Code

[Claude Code](https://code.claude.com/docs/en/overview) hanya mendukung Custom Skills.

**Custom Skills**: Buat Skills sebagai direktori dengan file SKILL.md. Claude menemukan dan menggunakannya secara otomatis.

Custom Skills di Claude Code berbasis filesystem dan tidak memerlukan unggahan API.

Untuk mempelajari lebih lanjut, lihat [Gunakan Skills di Claude Code](https://code.claude.com/docs/en/skills).

### Claude Agent SDK

[Claude Agent SDK](/docs/id/agent-sdk/overview) mendukung custom Skills melalui konfigurasi berbasis filesystem.

**Custom Skills**: Buat Skills sebagai direktori dengan file SKILL.md di `.claude/skills/`. Aktifkan Skills dengan menyertakan `"Skill"` dalam konfigurasi `allowed_tools` Anda.

Skills di Agent SDK kemudian ditemukan secara otomatis saat SDK berjalan.

Untuk mempelajari lebih lanjut, lihat [Agent Skills di SDK](/docs/id/agent-sdk/skills).

### Claude.ai

[Claude.ai](https://claude.ai) mendukung Agent Skills bawaan dan custom Skills.

**Agent Skills bawaan**: Skills ini sudah bekerja di balik layar saat Anda membuat dokumen. Claude menggunakannya tanpa memerlukan pengaturan apa pun.

**Custom Skills**: Unggah Skills Anda sendiri sebagai file zip melalui Pengaturan > Fitur. Tersedia pada paket Pro, Max, Team, dan Enterprise dengan eksekusi kode yang diaktifkan. Custom Skills bersifat individual untuk setiap pengguna; tidak dibagikan di seluruh organisasi dan tidak dapat dikelola secara terpusat oleh admin.

Untuk mempelajari lebih lanjut tentang menggunakan Skills di Claude.ai, lihat sumber daya berikut di Pusat Bantuan Claude:
- [Apa itu Skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Menggunakan Skills di Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Cara membuat custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Ajarkan Claude cara kerja Anda menggunakan Skills](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills)

## Struktur Skill

Setiap Skill memerlukan file `SKILL.md` dengan frontmatter YAML:

```yaml
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

**Field yang diperlukan**: `name` dan `description`

**Persyaratan field**:

`name`:
- Maksimum 64 karakter
- Hanya boleh mengandung huruf kecil, angka, dan tanda hubung
- Tidak boleh mengandung tag XML
- Tidak boleh mengandung kata-kata yang dicadangkan: "anthropic", "claude"

`description`:
- Harus tidak kosong
- Maksimum 1024 karakter
- Tidak boleh mengandung tag XML

`description` harus mencakup apa yang dilakukan Skill dan kapan Claude harus menggunakannya. Untuk panduan penulisan lengkap, lihat [panduan praktik terbaik](/docs/id/agents-and-tools/agent-skills/best-practices).

## Pertimbangan keamanan

Kami sangat menyarankan untuk menggunakan Skills hanya dari sumber tepercaya: yang Anda buat sendiri atau diperoleh dari Anthropic. Skills memberikan Claude kemampuan baru melalui instruksi dan kode, dan meskipun ini membuatnya kuat, ini juga berarti Skill yang berbahaya dapat mengarahkan Claude untuk memanggil tool atau mengeksekusi kode dengan cara yang tidak sesuai dengan tujuan yang dinyatakan Skill.

<Warning>
Jika Anda harus menggunakan Skill dari sumber yang tidak tepercaya atau tidak dikenal, berhati-hatilah dan audit secara menyeluruh sebelum digunakan. Bergantung pada akses apa yang dimiliki Claude saat mengeksekusi Skill, Skills yang berbahaya dapat menyebabkan eksfiltrasi data, akses sistem yang tidak sah, atau risiko keamanan lainnya.
</Warning>

**Pertimbangan keamanan utama**:
- **Audit secara menyeluruh**: Tinjau semua file yang dibundel dalam Skill: SKILL.md, skrip, gambar, dan sumber daya lainnya. Cari pola yang tidak biasa seperti panggilan jaringan yang tidak terduga, pola akses file, atau operasi yang tidak sesuai dengan tujuan yang dinyatakan Skill
- **Sumber eksternal berisiko**: Skills yang mengambil data dari URL eksternal menimbulkan risiko tertentu, karena konten yang diambil mungkin mengandung instruksi berbahaya. Bahkan Skills yang dapat dipercaya dapat dikompromikan jika dependensi eksternalnya berubah seiring waktu
- **Penyalahgunaan tool**: Skills yang berbahaya dapat memanggil tool (operasi file, perintah bash, eksekusi kode) dengan cara yang merugikan
- **Paparan data**: Skills dengan akses ke data sensitif dapat dirancang untuk membocorkan informasi ke sistem eksternal
- **Perlakukan seperti menginstal perangkat lunak**: Hanya gunakan Skills dari sumber tepercaya. Berhati-hatilah terutama saat mengintegrasikan Skills ke dalam sistem produksi dengan akses ke data sensitif atau operasi kritis

## Skills yang Tersedia

### Agent Skills Bawaan

Agent Skills bawaan berikut tersedia untuk digunakan segera:

- **PowerPoint (pptx)**: Membuat presentasi, mengedit slide, menganalisis konten presentasi
- **Excel (xlsx)**: Membuat spreadsheet, menganalisis data, menghasilkan laporan dengan grafik
- **Word (docx)**: Membuat dokumen, mengedit konten, memformat teks
- **PDF (pdf)**: Menghasilkan dokumen PDF yang diformat dan laporan

Skills ini tersedia di Claude API dan claude.ai. Lihat [tutorial quickstart](/docs/id/agents-and-tools/agent-skills/quickstart) untuk mulai menggunakannya di API.

### Contoh Custom Skills

Untuk contoh lengkap custom Skills, lihat [Skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction).

## Retensi data

Agent Skills tidak dicakup oleh pengaturan ZDR. Definisi Skill dan data eksekusi disimpan sesuai dengan kebijakan retensi data standar Anthropic.

Untuk kelayakan ZDR di semua fitur, lihat [API dan Retensi Data](/docs/id/build-with-claude/api-and-data-retention).

## Batasan dan kendala

Memahami batasan ini membantu Anda merencanakan penerapan Skills secara efektif.

### Ketersediaan lintas permukaan

**Custom Skills tidak disinkronkan di seluruh permukaan**. Skills yang diunggah ke satu permukaan tidak secara otomatis tersedia di permukaan lain:

- Skills yang diunggah ke Claude.ai harus diunggah secara terpisah ke API
- Skills yang diunggah melalui API tidak tersedia di Claude.ai
- Skills Claude Code berbasis filesystem dan terpisah dari Claude.ai dan API

Anda perlu mengelola dan mengunggah Skills secara terpisah untuk setiap permukaan tempat Anda ingin menggunakannya.

### Cakupan berbagi

Skills memiliki model berbagi yang berbeda tergantung di mana Anda menggunakannya:
- **Claude.ai**: Hanya pengguna individual; setiap anggota tim harus mengunggah secara terpisah
- **Claude API**: Seluruh workspace; semua anggota workspace dapat mengakses Skills yang diunggah
- **Claude Code**: Personal (`~/.claude/skills/`) atau berbasis proyek (`.claude/skills/`); juga dapat dibagikan melalui Claude Code Plugins

Claude.ai saat ini tidak mendukung manajemen admin terpusat atau distribusi custom Skills di seluruh organisasi.

### Kendala lingkungan runtime

Lingkungan runtime yang tersedia untuk skill Anda bergantung pada permukaan produk tempat Anda menggunakannya.

 - **Claude.ai**:
    - **Akses jaringan bervariasi**: Bergantung pada pengaturan pengguna/admin, Skills mungkin memiliki akses jaringan penuh, sebagian, atau tidak sama sekali. Untuk detail lebih lanjut, lihat artikel dukungan [Create and Edit Files](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude#h_6b7e833898).
- **Claude API**:
    - **Tidak ada akses jaringan**: Skills tidak dapat melakukan panggilan API eksternal atau mengakses internet
    - **Tidak ada instalasi paket runtime**: Hanya paket yang sudah terinstal yang tersedia. Anda tidak dapat menginstal paket baru selama eksekusi.
    - **Hanya dependensi yang sudah dikonfigurasi**: Periksa [dokumentasi tool eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk daftar paket yang tersedia
- **Claude Code**:
    - **Akses jaringan penuh**: Skills memiliki akses jaringan yang sama seperti program lain di komputer pengguna
    - **Instalasi paket global tidak disarankan**: Skills hanya boleh menginstal paket secara lokal untuk menghindari gangguan pada komputer pengguna

Rencanakan Skills Anda untuk bekerja dalam batasan-batasan ini.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card
    title="Mulai dengan Agent Skills"
    icon="graduation-cap"
    href="/docs/id/agents-and-tools/agent-skills/quickstart"
  >
    Buat Skill pertama Anda
  </Card>
  <Card
    title="Panduan API"
    icon="code"
    href="/docs/id/build-with-claude/skills-guide"
  >
    Gunakan Skills dengan Claude API
  </Card>
  <Card
    title="Gunakan Skills di Claude Code"
    icon="terminal"
    href="https://code.claude.com/docs/en/skills"
  >
    Buat dan kelola custom Skills di Claude Code
  </Card>
  <Card
    title="Gunakan Skills di Agent SDK"
    icon="cube"
    href="/docs/id/agent-sdk/skills"
  >
    Gunakan Skills secara programatik di TypeScript dan Python
  </Card>
  <Card
    title="Praktik terbaik penulisan"
    icon="lightbulb"
    href="/docs/id/agents-and-tools/agent-skills/best-practices"
  >
    Tulis Skills yang dapat digunakan Claude secara efektif
  </Card>
</CardGroup>