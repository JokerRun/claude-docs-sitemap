---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/overview
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: fa4fb5f76ea912937ca9d08b2fd383583281ef066dbd3e8bbdb5248f5700805a
---

# Agent Skills

Agent Skills adalah kemampuan modular yang memperluas fungsionalitas Claude. Setiap Skill mengemas instruksi, metadata, dan sumber daya opsional (skrip, templat) yang digunakan Claude secara otomatis ketika relevan.

---

<Note>
  Fitur ini **tidak** memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Data disimpan sesuai dengan kebijakan retensi standar fitur ini.
</Note>

## Mengapa menggunakan Skills

Skills adalah sumber daya berbasis filesystem yang dapat digunakan kembali dan menyediakan keahlian spesifik domain untuk Claude: alur kerja, konteks, dan praktik terbaik yang mengubah agen serbaguna menjadi spesialis. Tidak seperti prompt (instruksi tingkat percakapan untuk tugas sekali pakai), Skills dimuat sesuai permintaan dan menghilangkan kebutuhan untuk berulang kali memberikan panduan yang sama di berbagai percakapan.

**Manfaat utama**:

* **Menspesialisasikan Claude**: Menyesuaikan kemampuan untuk tugas spesifik domain
* **Mengurangi pengulangan**: Buat sekali, gunakan secara otomatis
* **Menggabungkan kemampuan**: Kombinasikan Skills untuk membangun alur kerja yang kompleks

<Note>
  Untuk pembahasan mendalam tentang arsitektur dan aplikasi dunia nyata dari Agent Skills, lihat postingan blog engineering [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
</Note>

## Menggunakan Skills

Anthropic menyediakan Agent Skills bawaan untuk tugas dokumen umum (PowerPoint, Excel, Word, PDF), dan Anda dapat membuat Skills kustom Anda sendiri. Keduanya bekerja dengan cara yang sama. Claude secara otomatis menggunakannya ketika relevan dengan permintaan Anda.

**Agent Skills bawaan** tersedia di claude.ai, Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry). Di Microsoft Foundry, Agent Skills memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure). Lihat [Skills yang Tersedia](#available-skills) untuk daftar lengkapnya.

**Skills Kustom** memungkinkan Anda mengemas keahlian domain dan pengetahuan organisasi. Skills ini tersedia di seluruh produk Claude: buat di Claude Code, unggah melalui Claude API, atau tambahkan di pengaturan claude.ai. Di [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws) dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry), unggah Skills kustom melalui Skills API.

<Note>
  **Mulai:**

  * Untuk Agent Skills bawaan: Lihat [tutorial quickstart](/docs/id/agents-and-tools/agent-skills/quickstart) untuk mulai menggunakan skills PowerPoint, Excel, Word, dan PDF di API
  * Untuk Skills kustom: Lihat [Agent Skills Cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction) untuk mempelajari cara membuat Skills Anda sendiri
</Note>

## Cara kerja Skills

Skills memanfaatkan lingkungan VM Claude untuk menyediakan kemampuan di luar apa yang mungkin dilakukan dengan prompt saja. Claude beroperasi di mesin virtual dengan akses filesystem, memungkinkan Skills ada sebagai direktori yang berisi instruksi, kode yang dapat dieksekusi, dan materi referensi, yang diorganisir seperti panduan onboarding yang akan Anda buat untuk anggota tim baru.

Arsitektur berbasis filesystem ini memungkinkan **progressive disclosure** (pengungkapan bertahap): Claude memuat informasi secara bertahap sesuai kebutuhan, alih-alih menghabiskan konteks di awal.

### Tiga jenis konten Skill, tiga tingkat pemuatan

Skills dapat berisi tiga jenis konten, masing-masing dimuat pada waktu yang berbeda:

### Tingkat 1: Metadata (selalu dimuat)

**Jenis konten: Instruksi**. Frontmatter YAML dari Skill menyediakan informasi penemuan:

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

Claude memuat metadata ini saat startup dan menyertakannya dalam prompt sistem. Pendekatan ringan ini berarti Anda dapat menginstal banyak Skills tanpa penalti konteks; Claude hanya mengetahui bahwa setiap Skill ada dan kapan harus menggunakannya.

### Tingkat 2: Instruksi (dimuat saat dipicu)

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

Ketika Anda meminta sesuatu yang cocok dengan deskripsi Skill, Claude membaca SKILL.md dari filesystem melalui bash. Baru setelah itu konten ini masuk ke jendela konteks.

### Tingkat 3: Sumber daya dan kode (dimuat sesuai kebutuhan)

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

**Kode**: Skrip yang dapat dieksekusi (fill\_form.py, validate.py) yang dijalankan Claude melalui bash; skrip menyediakan operasi deterministik tanpa menghabiskan konteks

**Sumber daya**: Materi referensi seperti skema database, dokumentasi API, templat, atau contoh

Claude mengakses file-file ini hanya ketika direferensikan. Model filesystem berarti setiap jenis konten memiliki kekuatan yang berbeda: instruksi untuk panduan yang fleksibel, kode untuk keandalan, sumber daya untuk pencarian faktual.

| Tingkat                     | Kapan Dimuat          | Biaya Token                   | Konten                                                                            |
| --------------------------- | --------------------- | ----------------------------- | --------------------------------------------------------------------------------- |
| **Tingkat 1: Metadata**     | Selalu (saat startup) | \~100 token per Skill         | `name` dan `description` dari frontmatter YAML                                    |
| **Tingkat 2: Instruksi**    | Ketika Skill dipicu   | Di bawah 5k token             | Isi SKILL.md dengan instruksi dan panduan                                         |
| **Tingkat 3+: Sumber daya** | Sesuai kebutuhan      | Secara efektif tidak terbatas | File yang disertakan dieksekusi melalui bash tanpa memuat konten ke dalam konteks |

Progressive disclosure memastikan hanya konten yang relevan yang menempati jendela konteks pada waktu tertentu.

### Arsitektur Skills

Skills berjalan di lingkungan eksekusi kode di mana Claude memiliki akses filesystem, perintah bash, dan kemampuan eksekusi kode. Bayangkan seperti ini: Skills ada sebagai direktori di mesin virtual, dan Claude berinteraksi dengannya menggunakan perintah bash yang sama seperti yang Anda gunakan untuk menavigasi file di komputer Anda.

![Arsitektur Agent Skills - menunjukkan bagaimana Skills terintegrasi dengan konfigurasi agen dan mesin virtual](/docs/images/agent-skills-architecture.png)

**Bagaimana Claude mengakses konten Skill:**

Ketika sebuah Skill dipicu, Claude menggunakan bash untuk membaca SKILL.md dari filesystem, membawa instruksinya ke dalam jendela konteks. Jika instruksi tersebut mereferensikan file lain (seperti FORMS.md atau skema database), Claude juga membaca file-file tersebut menggunakan perintah bash tambahan. Ketika instruksi menyebutkan skrip yang dapat dieksekusi, Claude menjalankannya melalui bash dan hanya menerima output-nya (kode skrip itu sendiri tidak pernah masuk ke konteks).

**Apa yang dimungkinkan oleh arsitektur ini:**

**Akses file sesuai permintaan**: Claude hanya membaca file yang diperlukan untuk setiap tugas spesifik. Sebuah Skill dapat menyertakan puluhan file referensi, tetapi jika tugas Anda hanya memerlukan skema penjualan, Claude hanya memuat satu file itu. Sisanya tetap berada di filesystem tanpa menghabiskan token sama sekali.

**Eksekusi skrip yang efisien**: Ketika Claude menjalankan `validate_form.py`, kode skrip tidak pernah dimuat ke dalam jendela konteks. Hanya output skrip (seperti "Validation passed" atau pesan error spesifik) yang menghabiskan token. Ini membuat skrip jauh lebih efisien dibandingkan meminta Claude menghasilkan kode yang setara secara langsung.

**Tidak ada batasan praktis pada konten yang disertakan**: Karena file tidak menghabiskan konteks sampai diakses, Skills dapat menyertakan dokumentasi API yang komprehensif, dataset besar, contoh yang ekstensif, atau materi referensi apa pun yang Anda butuhkan. Tidak ada penalti konteks untuk konten yang disertakan tetapi tidak digunakan.

Model berbasis filesystem inilah yang membuat progressive disclosure berfungsi. Claude menavigasi Skill Anda seperti Anda mereferensikan bagian spesifik dari panduan onboarding, mengakses persis apa yang dibutuhkan setiap tugas.

### Contoh: Memuat skill pemrosesan PDF

Berikut cara Claude memuat dan menggunakan skill pemrosesan PDF:

1. **Startup**: Prompt sistem menyertakan: `PDF Processing - Extract text and tables from PDF files, fill forms, merge documents`
2. **Permintaan pengguna**: "Ekstrak teks dari PDF ini dan rangkum"
3. **Claude memanggil**: `bash: read pdf-skill/SKILL.md` → Instruksi dimuat ke dalam konteks
4. **Claude menentukan**: Pengisian formulir tidak diperlukan, jadi FORMS.md tidak dibaca
5. **Claude mengeksekusi**: Menggunakan instruksi dari SKILL.md untuk menyelesaikan tugas

![Skills dimuat ke dalam jendela konteks - menunjukkan pemuatan bertahap metadata dan konten skill](/docs/images/agent-skills-context-window.png)

Diagram menunjukkan:

1. Keadaan default dengan prompt sistem dan metadata skill yang telah dimuat sebelumnya
2. Claude memicu skill dengan membaca SKILL.md melalui bash
3. Claude secara opsional membaca file tambahan yang disertakan seperti FORMS.md sesuai kebutuhan
4. Claude melanjutkan dengan tugas

Pemuatan dinamis ini memastikan hanya konten skill yang relevan yang menempati jendela konteks.

## Di mana Skills bekerja

Skills tersedia di seluruh produk agen Claude:

<Note>
  Claude Platform on AWS dan Microsoft Foundry mewarisi perilaku Skills yang sama seperti Claude API di semua bagian berikut.
</Note>

### Claude API

Claude API mendukung Agent Skills bawaan dan Skills kustom. Keduanya bekerja secara identik: tentukan `skill_id` yang relevan dalam parameter `container` bersama dengan alat eksekusi kode.

**Prasyarat**: Menggunakan Skills melalui API memerlukan tiga header beta:

* `code-execution-2025-08-25` - Skills berjalan di container eksekusi kode
* `skills-2025-10-02` - Mengaktifkan fungsionalitas Skills
* `files-api-2025-04-14` - Diperlukan untuk mengunggah/mengunduh file ke/dari container

Gunakan Agent Skills bawaan dengan mereferensikan `skill_id` mereka (misalnya, `pptx`, `xlsx`), atau buat dan unggah milik Anda sendiri melalui Skills API (endpoint `/v1/skills`). Skills kustom dibagikan di seluruh workspace; semua anggota workspace dapat mengaksesnya.

Untuk mempelajari lebih lanjut, lihat [Menggunakan Skills dengan Claude API](/docs/id/build-with-claude/skills-guide).

### Claude Code

[Claude Code](https://code.claude.com/docs/en/overview) hanya mendukung Skills Kustom.

**Skills Kustom**: Buat Skills sebagai direktori dengan file SKILL.md. Claude menemukan dan menggunakannya secara otomatis.

Skills Kustom di Claude Code berbasis filesystem dan tidak memerlukan unggahan API.

Untuk mempelajari lebih lanjut, lihat [Menggunakan Skills di Claude Code](https://code.claude.com/docs/en/skills).

### claude.ai

[claude.ai](https://claude.ai) mendukung Agent Skills bawaan dan Skills kustom.

**Agent Skills bawaan**: Skills ini sudah bekerja di balik layar ketika Anda membuat dokumen. Claude menggunakannya tanpa memerlukan pengaturan apa pun.

**Skills Kustom**: Unggah Skills Anda sendiri sebagai file zip melalui Settings > Features. Tersedia pada paket Pro, Max, Team, dan Enterprise dengan eksekusi kode diaktifkan. Skills Kustom bersifat individual untuk setiap pengguna; tidak dibagikan di seluruh organisasi dan tidak dapat dikelola secara terpusat oleh admin.

Untuk mempelajari lebih lanjut tentang menggunakan Skills di claude.ai, lihat sumber daya berikut di Claude Help Center:

* [Apa itu Skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
* [Menggunakan Skills di Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
* [Cara membuat Skills kustom](https://support.claude.com/en/articles/12512198-creating-custom-skills)
* [Ajarkan Claude cara kerja Anda menggunakan Skills](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills)

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

* Maksimum 64 karakter
* Hanya boleh berisi huruf kecil, angka, dan tanda hubung
* Tidak boleh berisi tag XML
* Tidak boleh berisi kata yang dicadangkan: "anthropic", "claude"

`description`:

* Tidak boleh kosong
* Maksimum 1024 karakter
* Tidak boleh berisi tag XML

`description` harus mencakup apa yang dilakukan Skill dan kapan Claude harus menggunakannya. Untuk panduan penulisan lengkap, lihat [panduan praktik terbaik](/docs/id/agents-and-tools/agent-skills/best-practices).

## Pertimbangan keamanan

Gunakan Skills hanya dari sumber tepercaya: yang Anda buat sendiri atau diperoleh dari Anthropic. Skills memberikan Claude kemampuan baru melalui instruksi dan kode, dan meskipun ini membuatnya kuat, ini juga berarti Skill berbahaya dapat mengarahkan Claude untuk memanggil alat atau mengeksekusi kode dengan cara yang tidak sesuai dengan tujuan yang dinyatakan Skill tersebut.

<Warning>
  Jika Anda harus menggunakan Skill dari sumber yang tidak tepercaya atau tidak dikenal, berhati-hatilah dan audit secara menyeluruh sebelum digunakan. Tergantung pada akses yang dimiliki Claude saat mengeksekusi Skill, Skills berbahaya dapat menyebabkan eksfiltrasi data, akses sistem yang tidak sah, atau risiko keamanan lainnya.
</Warning>

**Pertimbangan keamanan utama**:

* **Audit secara menyeluruh**: Tinjau semua file yang disertakan dalam Skill: SKILL.md, skrip, gambar, dan sumber daya lainnya. Cari pola yang tidak biasa seperti panggilan jaringan yang tidak terduga, pola akses file, atau operasi yang tidak sesuai dengan tujuan yang dinyatakan Skill
* **Sumber eksternal berisiko**: Skills yang mengambil data dari URL eksternal menimbulkan risiko khusus, karena konten yang diambil mungkin berisi instruksi berbahaya. Bahkan Skills yang tepercaya dapat dikompromikan jika dependensi eksternalnya berubah seiring waktu
* **Penyalahgunaan alat**: Skills berbahaya dapat memanggil alat (operasi file, perintah bash, eksekusi kode) dengan cara yang merugikan
* **Paparan data**: Skills dengan akses ke data sensitif dapat dirancang untuk membocorkan informasi ke sistem eksternal
* **Perlakukan seperti menginstal perangkat lunak**: Hanya gunakan Skills dari sumber tepercaya. Berhati-hatilah terutama saat mengintegrasikan Skills ke dalam sistem produksi dengan akses ke data sensitif atau operasi kritis

## Skills yang tersedia

### Agent Skills bawaan

Agent Skills bawaan berikut tersedia untuk digunakan langsung:

* **PowerPoint (pptx)**: Membuat presentasi, mengedit slide, menganalisis konten presentasi
* **Excel (xlsx)**: Membuat spreadsheet, menganalisis data, menghasilkan laporan dengan grafik
* **Word (docx)**: Membuat dokumen, mengedit konten, memformat teks
* **PDF (pdf)**: Menghasilkan dokumen dan laporan PDF yang terformat

Skills ini tersedia di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry), dan claude.ai. Di Microsoft Foundry, Agent Skills memerlukan [deployment Hosted on Anthropic](/docs/id/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure). Lihat [tutorial quickstart](/docs/id/agents-and-tools/agent-skills/quickstart) untuk mulai menggunakannya di API.

### Skills open-source

Anthropic juga menerbitkan Skills open-source di [repositori skills](https://github.com/anthropics/skills):

* **[Claude API](/docs/id/agents-and-tools/agent-skills/claude-api-skill)**: Menyediakan Claude dengan materi referensi API terkini, dokumentasi SDK, dan praktik terbaik untuk 8 bahasa pemrograman. Disertakan dengan Claude Code dan juga tersedia untuk instalasi dari repositori skills.

### Contoh Skills kustom

Untuk contoh lengkap Skills kustom, lihat [Skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction).

## Retensi data

Agent Skills tidak tercakup oleh pengaturan ZDR. Definisi Skill dan data eksekusi disimpan sesuai dengan kebijakan retensi data standar Anthropic.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Batasan dan kendala

Memahami batasan ini membantu Anda merencanakan deployment Skills Anda secara efektif. Claude Platform on AWS dan Microsoft Foundry mengikuti batasan yang sama seperti Claude API di subbagian berikut.

### Ketersediaan lintas surface

**Skills Kustom tidak tersinkronisasi antar surface**. Skills yang diunggah ke satu surface tidak secara otomatis tersedia di surface lainnya:

* Skills yang diunggah ke claude.ai harus diunggah secara terpisah ke API
* Skills yang diunggah melalui API tidak tersedia di claude.ai
* Skills Claude Code berbasis filesystem dan terpisah dari claude.ai maupun API

Anda perlu mengelola dan mengunggah Skills secara terpisah untuk setiap surface tempat Anda ingin menggunakannya.

### Cakupan berbagi

Skills memiliki model berbagi yang berbeda tergantung di mana Anda menggunakannya:

* **claude.ai**: Hanya pengguna individual; setiap anggota tim harus mengunggah secara terpisah
* **Claude API**: Seluruh workspace; semua anggota workspace dapat mengakses Skills yang diunggah
* **Claude Code**: Personal (`~/.claude/skills/`) atau berbasis proyek (`.claude/skills/`); juga dapat dibagikan melalui Claude Code Plugins

claude.ai tidak mendukung manajemen admin terpusat atau distribusi Skills kustom di seluruh organisasi.

### Kendala lingkungan runtime

Lingkungan runtime yang tersedia untuk skill Anda bergantung pada surface produk tempat Anda menggunakannya.

* **claude.ai**:
  * **Akses jaringan bervariasi**: Tergantung pada pengaturan pengguna/admin, Skills mungkin memiliki akses jaringan penuh, sebagian, atau tidak sama sekali. Untuk detail lebih lanjut, lihat artikel dukungan [Create and Edit Files](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude#h_6b7e833898).

* **Claude API**:

  * **Tidak ada akses jaringan**: Skills tidak dapat melakukan panggilan API eksternal atau mengakses internet
  * **Tidak ada instalasi paket runtime**: Hanya paket yang sudah terinstal yang tersedia. Anda tidak dapat menginstal paket baru selama eksekusi.
  * **Hanya dependensi yang telah dikonfigurasi sebelumnya**: Periksa [dokumentasi alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool) untuk daftar paket yang tersedia

* **Claude Code**:

  * **Akses jaringan penuh**: Skills memiliki akses jaringan yang sama seperti program lain di komputer pengguna
  * **Instalasi paket global tidak disarankan**: Skills sebaiknya hanya menginstal paket secara lokal untuk menghindari gangguan pada komputer pengguna

Rencanakan Skills Anda agar bekerja dalam batasan ini.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mulai dengan Agent Skills" icon="graduation-cap" href="/docs/id/agents-and-tools/agent-skills/quickstart">
    Buat Skill pertama Anda
  </Card>

  <Card title="Panduan API" icon="code" href="/docs/id/build-with-claude/skills-guide">
    Gunakan Skills dengan Claude API
  </Card>

  <Card title="Gunakan Skills di Claude Code" icon="terminal" href="https://code.claude.com/docs/en/skills">
    Buat dan kelola Skills kustom di Claude Code
  </Card>

  <Card title="Praktik terbaik penulisan" icon="lightbulb" href="/docs/id/agents-and-tools/agent-skills/best-practices">
    Tulis Skills yang dapat digunakan Claude secara efektif
  </Card>
</CardGroup>
