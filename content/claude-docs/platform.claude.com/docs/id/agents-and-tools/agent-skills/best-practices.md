---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/best-practices
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: a10d9bb1f1a6453b7d61b2447d38f4ca9f328d40fb0d8e6e9fc0be9d77549818
---

# Praktik terbaik penulisan Skill

Pelajari cara menulis Skill yang efektif yang dapat ditemukan dan digunakan Claude dengan sukses.

---

Skill yang baik bersifat ringkas, terstruktur dengan baik, dan diuji dengan penggunaan nyata. Panduan ini memberikan keputusan penulisan praktis untuk membantu Anda menulis Skill yang dapat ditemukan dan digunakan Claude secara efektif.

Untuk latar belakang konseptual tentang cara kerja Skill, lihat [ikhtisar Skill](/docs/id/agents-and-tools/agent-skills/overview).

## Prinsip inti

### Ringkas adalah kunci

"Context window" ([jendela konteks](/docs/id/build-with-claude/context-windows)) adalah barang publik. Skill Anda berbagi jendela konteks dengan semua hal lain yang perlu diketahui Claude, termasuk:

* Prompt sistem
* Riwayat percakapan
* Metadata Skill lainnya
* Permintaan Anda yang sebenarnya

Tidak setiap token dalam Skill Anda memiliki biaya langsung. Saat startup, hanya metadata (name dan description) dari semua Skill yang dimuat sebelumnya. Claude membaca SKILL.md hanya ketika Skill menjadi relevan, dan membaca file tambahan hanya sesuai kebutuhan. Namun, menjadi ringkas dalam SKILL.md tetap penting: setelah Claude memuatnya, setiap token bersaing dengan riwayat percakapan dan konteks lainnya.

**Asumsi default:** Claude sudah sangat cerdas

Hanya tambahkan konteks yang belum dimiliki Claude. Tantang setiap bagian informasi:

* "Apakah Claude benar-benar membutuhkan penjelasan ini?"
* "Bisakah saya berasumsi Claude mengetahui ini?"
* "Apakah paragraf ini sepadan dengan biaya tokennya?"

**Contoh baik: Ringkas** (sekitar 50 token):

````markdown
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**Contoh buruk: Terlalu bertele-tele** (sekitar 150 token):

```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but
pdfplumber is recommended because it's easy to use and handles most cases well.
First, you'll need to install it using pip. Then you can use the code below...
```

Versi ringkas mengasumsikan Claude sudah memiliki informasi tentang PDF dan cara kerja library.

### Tetapkan tingkat kebebasan yang sesuai

Sesuaikan tingkat kekhususan dengan kerapuhan dan variabilitas tugas.

**Kebebasan tinggi** (instruksi berbasis teks):

Gunakan ketika:

* Beberapa pendekatan valid
* Keputusan bergantung pada konteks
* Heuristik memandu pendekatan

Contoh:

```markdown
## Code review process

1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability and maintainability
4. Verify adherence to project conventions
```

**Kebebasan sedang** (pseudocode atau skrip dengan parameter):

Gunakan ketika:

* Ada pola yang lebih disukai
* Beberapa variasi dapat diterima
* Konfigurasi memengaruhi perilaku

Contoh:

````markdown
## Generate report

Use this template and customize as needed:

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```
````

**Kebebasan rendah** (skrip spesifik, sedikit atau tanpa parameter):

Gunakan ketika:

* Operasi rapuh dan rentan kesalahan
* Konsistensi sangat penting
* Urutan tertentu harus diikuti

Contoh:

````markdown
## Database migration

Run exactly this script:

```bash
python scripts/migrate.py --verify --backup
```

Do not modify the command or add additional flags.
````

**Analogi:** Bayangkan Claude sebagai robot yang menjelajahi jalur:

* **Jembatan sempit dengan jurang di kedua sisi:** Hanya ada satu jalan aman ke depan. Berikan pagar pengaman spesifik dan instruksi yang tepat (kebebasan rendah). Contoh: migrasi database yang harus dijalankan dalam urutan yang tepat.
* **Lapangan terbuka tanpa bahaya:** Banyak jalur menuju keberhasilan. Berikan arahan umum dan percayakan Claude untuk menemukan rute terbaik (kebebasan tinggi). Contoh: tinjauan kode di mana konteks menentukan pendekatan terbaik.

### Uji dengan semua model yang Anda rencanakan untuk digunakan

Skill bertindak sebagai tambahan untuk model, sehingga efektivitasnya bergantung pada model yang mendasarinya. Uji Skill Anda dengan semua model yang Anda rencanakan untuk menggunakannya.

**Pertimbangan pengujian berdasarkan model:**

* **Claude Haiku** (cepat, ekonomis): Apakah Skill memberikan panduan yang cukup?
* **Claude Sonnet** (seimbang): Apakah Skill jelas dan efisien?
* **Claude Opus** (penalaran yang kuat): Apakah Skill menghindari penjelasan berlebihan?

Apa yang bekerja sempurna untuk Opus mungkin memerlukan lebih banyak detail untuk Haiku. Jika Anda berencana menggunakan Skill Anda di beberapa model, usahakan instruksi yang bekerja dengan baik untuk semuanya.

## Struktur Skill

<Note>
  **YAML Frontmatter:** Frontmatter SKILL.md memerlukan dua field:

  `name`:

  * Maksimum 64 karakter
  * Hanya boleh berisi huruf kecil, angka, dan tanda hubung
  * Tidak boleh berisi tag XML
  * Tidak boleh berisi kata yang dicadangkan: "anthropic", "claude"

  `description`:

  * Tidak boleh kosong
  * Maksimum 1.024 karakter
  * Tidak boleh berisi tag XML
  * Harus menjelaskan apa yang dilakukan Skill dan kapan menggunakannya

  Untuk detail lengkap struktur Skill, lihat [ikhtisar Skill](/docs/id/agents-and-tools/agent-skills/overview#skill-structure).
</Note>

### Konvensi penamaan

Gunakan pola penamaan yang konsisten untuk membuat Skill lebih mudah dirujuk dan didiskusikan. Pertimbangkan untuk menggunakan **bentuk gerund** (kata kerja + -ing) untuk nama Skill, karena ini dengan jelas menggambarkan aktivitas atau kemampuan yang disediakan Skill.

Ingat bahwa field `name` hanya boleh menggunakan huruf kecil, angka, dan tanda hubung.

**Contoh penamaan yang baik (bentuk gerund):**

* `processing-pdfs`
* `analyzing-spreadsheets`
* `managing-databases`
* `testing-code`
* `writing-documentation`

**Alternatif yang dapat diterima:**

* Frasa nomina: `pdf-processing`, `spreadsheet-analysis`
* Berorientasi tindakan: `process-pdfs`, `analyze-spreadsheets`

**Hindari:**

* Nama yang samar: `helper`, `utils`, `tools`
* Terlalu generik: `documents`, `data`, `files`
* Kata yang dicadangkan: `anthropic-helper`, `claude-tools`
* Pola yang tidak konsisten dalam koleksi skill Anda

Penamaan yang konsisten memudahkan untuk:

* Merujuk Skill dalam dokumentasi dan percakapan
* Memahami apa yang dilakukan Skill secara sekilas
* Mengatur dan mencari di antara beberapa Skill
* Mempertahankan pustaka skill yang profesional dan kohesif

### Menulis deskripsi yang efektif

Field `description` memungkinkan penemuan Skill dan harus mencakup apa yang dilakukan Skill dan kapan menggunakannya.

<Warning>
  **Selalu tulis dalam sudut pandang orang ketiga**. Deskripsi disuntikkan ke dalam prompt sistem, dan sudut pandang yang tidak konsisten dapat menyebabkan masalah penemuan.

  * **Baik:** "Processes Excel files and generates reports"
  * **Hindari:** "I can help you process Excel files"
  * **Hindari:** "You can use this to process Excel files"
</Warning>

**Spesifik dan sertakan istilah kunci**. Sertakan apa yang dilakukan Skill dan pemicu/konteks spesifik kapan menggunakannya.

Setiap Skill memiliki tepat satu field description. Deskripsi sangat penting untuk pemilihan skill: Claude menggunakannya untuk memilih Skill yang tepat dari kemungkinan 100+ Skill yang tersedia. Deskripsi Anda harus memberikan detail yang cukup agar Claude tahu kapan harus memilih Skill ini, sementara sisa SKILL.md menyediakan detail implementasi.

Contoh yang efektif:

**Skill Pemrosesan PDF:**

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Skill Analisis Excel:**

```yaml
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

**Skill Git Commit Helper:**

```yaml
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

Hindari deskripsi yang samar seperti ini:

```yaml
description: Helps with documents
```

```yaml
description: Processes data
```

```yaml
description: Does stuff with files
```

### Pola progressive disclosure

SKILL.md berfungsi sebagai ikhtisar yang mengarahkan Claude ke materi terperinci sesuai kebutuhan, seperti daftar isi dalam panduan onboarding. Untuk penjelasan tentang cara kerja progressive disclosure, lihat [Cara kerja Skill](/docs/id/agents-and-tools/agent-skills/overview#how-skills-work) di ikhtisar.

**Panduan praktis:**

* Jaga isi SKILL.md di bawah 500 baris untuk kinerja optimal
* Pisahkan konten ke file terpisah saat mendekati batas ini
* Gunakan pola berikut untuk mengatur instruksi, kode, dan sumber daya secara efektif

#### Ikhtisar visual: Dari sederhana ke kompleks

Skill dasar dimulai hanya dengan file SKILL.md yang berisi metadata dan instruksi:

![File SKILL.md sederhana yang menunjukkan YAML frontmatter dan isi markdown](/docs/images/agent-skills-simple-file.png)

Seiring Skill Anda berkembang, Anda dapat membundel konten tambahan yang dimuat Claude hanya saat diperlukan:

![Membundel file referensi tambahan seperti reference.md dan forms.md.](/docs/images/agent-skills-bundling-content.png)

Struktur direktori Skill lengkap mungkin terlihat seperti ini:

```text
pdf/
├── SKILL.md              # Main instructions (loaded when triggered)
├── FORMS.md              # Form-filling guide (loaded as needed)
├── reference.md          # API reference (loaded as needed)
├── examples.md           # Usage examples (loaded as needed)
└── scripts/
    ├── analyze_form.py   # Utility script (executed, not loaded)
    ├── fill_form.py      # Form filling script
    └── validate.py       # Validation script
```

#### Pola 1: Panduan tingkat tinggi dengan referensi

````markdown
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

## Quick start

Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features

**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
````

Claude memuat FORMS.md, REFERENCE.md, atau EXAMPLES.md hanya saat diperlukan.

#### Pola 2: Organisasi spesifik domain

Untuk Skill dengan beberapa domain, atur konten berdasarkan domain untuk menghindari pemuatan konteks yang tidak relevan. Ketika pengguna bertanya tentang metrik penjualan, Claude hanya perlu membaca skema terkait penjualan, bukan data keuangan atau pemasaran. Ini menjaga penggunaan token tetap rendah dan konteks tetap fokus.

```text
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

````markdown SKILL.md
# BigQuery Data Analysis

## Available datasets

**Finance**: Revenue, ARR, billing → See [reference/finance.md](reference/finance.md)
**Sales**: Opportunities, pipeline, accounts → See [reference/sales.md](reference/sales.md)
**Product**: API usage, features, adoption → See [reference/product.md](reference/product.md)
**Marketing**: Campaigns, attribution, email → See [reference/marketing.md](reference/marketing.md)

## Quick search

Find specific metrics using grep:

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
```
````

#### Pola 3: Detail bersyarat

Tampilkan konten dasar, tautkan ke konten lanjutan:

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Claude membaca REDLINING.md atau OOXML.md hanya ketika pengguna membutuhkan fitur tersebut.

### Hindari referensi bersarang yang dalam

Claude mungkin membaca file secara parsial ketika file tersebut dirujuk dari file lain yang dirujuk. Saat menemukan referensi bersarang, Claude mungkin menggunakan perintah seperti `head -100` untuk melihat pratinjau konten alih-alih membaca seluruh file, yang menghasilkan informasi yang tidak lengkap.

**Jaga referensi satu tingkat dari SKILL.md**. Semua file referensi harus ditautkan langsung dari SKILL.md untuk memastikan Claude membaca file lengkap saat diperlukan.

**Contoh buruk: Terlalu dalam**:

```markdown
# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...
```

**Contoh baik: Satu tingkat**:

```markdown
# SKILL.md

**Basic usage**: [instructions in SKILL.md]
**Advanced features**: See [advanced.md](advanced.md)
**API reference**: See [reference.md](reference.md)
**Examples**: See [examples.md](examples.md)
```

### Strukturkan file referensi yang lebih panjang dengan daftar isi

Untuk file referensi yang lebih panjang dari 100 baris, sertakan daftar isi di bagian atas. Ini memastikan Claude dapat melihat cakupan penuh informasi yang tersedia bahkan saat melihat pratinjau dengan pembacaan parsial.

**Contoh:**

```markdown
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns
- Code examples

## Authentication and setup
...

## Core methods
...
```

Claude kemudian dapat membaca file lengkap atau melompat ke bagian tertentu sesuai kebutuhan.

Untuk detail tentang bagaimana arsitektur berbasis filesystem ini memungkinkan progressive disclosure, lihat bagian [Lingkungan runtime](#runtime-environment) nanti dalam panduan ini.

## Alur kerja dan loop umpan balik

### Gunakan alur kerja untuk tugas kompleks

Pecah operasi kompleks menjadi langkah-langkah yang jelas dan berurutan. Untuk alur kerja yang sangat kompleks, sediakan checklist yang dapat disalin Claude ke dalam responsnya dan dicentang seiring kemajuannya.

**Contoh 1: Alur kerja sintesis riset** (untuk Skill tanpa kode):

````markdown
## Research synthesis workflow

Copy this checklist and track your progress:

```
Research Progress:
- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create structured summary
- [ ] Step 5: Verify citations
```

**Step 1: Read all source documents**

Review each document in the `sources/` directory. Note the main arguments and supporting evidence.

**Step 2: Identify key themes**

Look for patterns across sources. What themes appear repeatedly? Where do sources agree or disagree?

**Step 3: Cross-reference claims**

For each major claim, verify it appears in the source material. Note which source supports each point.

**Step 4: Create structured summary**

Organize findings by theme. Include:
- Main claim
- Supporting evidence from sources
- Conflicting viewpoints (if any)

**Step 5: Verify citations**

Check that every claim references the correct source document. If citations are incomplete, return to Step 3.
````

Contoh ini menunjukkan bagaimana alur kerja berlaku untuk tugas analisis yang tidak memerlukan kode. Pola checklist bekerja untuk proses kompleks multi-langkah apa pun.

**Contoh 2: Alur kerja pengisian formulir PDF** (untuk Skill dengan kode):

````markdown
## PDF form filling workflow

Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze the form**

Run: `python scripts/analyze_form.py input.pdf`

This extracts form fields and their locations, saving to `fields.json`.

**Step 2: Create field mapping**

Edit `fields.json` to add values for each field.

**Step 3: Validate mapping**

Run: `python scripts/validate_fields.py fields.json`

Fix any validation errors before continuing.

**Step 4: Fill the form**

Run: `python scripts/fill_form.py input.pdf fields.json output.pdf`

**Step 5: Verify output**

Run: `python scripts/verify_output.py output.pdf`

If verification fails, return to Step 2.
````

Langkah-langkah yang jelas mencegah Claude melewatkan validasi penting. Checklist membantu Claude dan Anda melacak kemajuan melalui alur kerja multi-langkah.

### Implementasikan loop umpan balik

**Pola umum:** Jalankan validator → perbaiki kesalahan → ulangi

Pola ini sangat meningkatkan kualitas output.

**Contoh 1: Kepatuhan panduan gaya** (untuk Skill tanpa kode):

```markdown
## Content review process

1. Draft your content following the guidelines in STYLE_GUIDE.md
2. Review against the checklist:
   - Check terminology consistency
   - Verify examples follow the standard format
   - Confirm all required sections are present
3. If issues found:
   - Note each issue with specific section reference
   - Revise the content
   - Review the checklist again
4. Only proceed when all requirements are met
5. Finalize and save the document
```

Ini menunjukkan pola loop validasi menggunakan dokumen referensi alih-alih skrip. "Validator"-nya adalah STYLE\_GUIDE.md, dan Claude melakukan pemeriksaan dengan membaca dan membandingkan.

**Contoh 2: Proses pengeditan dokumen** (untuk Skill dengan kode):

```markdown
## Document editing process

1. Make your edits to `word/document.xml`
2. **Validate immediately**: `python ooxml/scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues in the XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. Test the output document
```

Loop validasi menangkap kesalahan lebih awal.

## Pedoman konten

### Hindari informasi yang sensitif terhadap waktu

Jangan sertakan informasi yang akan menjadi usang:

**Contoh buruk: Sensitif terhadap waktu** (akan menjadi salah):

```markdown
If you're doing this before August 2025, use the old API.
After August 2025, use the new API.
```

**Contoh baik** (gunakan bagian "pola lama"):

```markdown
## Current method

Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>

The v1 API used: `api.example.com/v1/messages`

This endpoint is no longer supported.
</details>
```

Bagian pola lama memberikan konteks historis tanpa mengacaukan konten utama.

### Gunakan terminologi yang konsisten

Pilih satu istilah dan gunakan di seluruh Skill:

**Baik - Konsisten:**

* Selalu "API endpoint"
* Selalu "field"
* Selalu "extract"

**Buruk - Tidak konsisten:**

* Mencampur "API endpoint", "URL", "API route", "path"
* Mencampur "field", "box", "element", "control"
* Mencampur "extract", "pull", "get", "retrieve"

Konsistensi membantu Claude mengurai dan mengikuti instruksi.

## Pola umum

### Pola template

Sediakan template untuk format output. Sesuaikan tingkat ketegasan dengan kebutuhan Anda.

**Untuk persyaratan ketat** (seperti respons API atau format data):

````markdown
## Report structure

ALWAYS use this exact template structure:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```
````

**Untuk panduan fleksibel** (ketika adaptasi berguna):

````markdown
## Report structure

Here is a sensible default format, but use your best judgment based on the analysis:

```markdown
# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]
```

Adjust sections as needed for the specific analysis type.
````

### Pola contoh

Untuk Skill di mana kualitas output bergantung pada melihat contoh, sediakan pasangan input/output seperti dalam prompting biasa:

````markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

**Example 3:**
Input: Updated dependencies and refactored error handling
Output:
```
chore: update dependencies and refactor error handling

- Upgrade lodash to 4.17.21
- Standardize error response format across endpoints
```

Follow this style: type(scope): brief description, then detailed explanation.
````

Contoh menyampaikan gaya dan tingkat detail yang diinginkan kepada Claude lebih jelas daripada deskripsi saja.

### Pola alur kerja bersyarat

Pandu Claude melalui titik keputusan:

```markdown
## Document modification workflow

1. Determine the modification type:

   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   - Use docx-js library
   - Build document from scratch
   - Export to .docx format

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
   - Repack when complete
```

<Tip>
  Jika alur kerja menjadi besar atau rumit dengan banyak langkah, pertimbangkan untuk memindahkannya ke file terpisah dan beri tahu Claude untuk membaca file yang sesuai berdasarkan tugas yang sedang dikerjakan.
</Tip>

## Evaluasi dan iterasi

### Bangun evaluasi terlebih dahulu

**Buat evaluasi SEBELUM menulis dokumentasi yang ekstensif.** Ini memastikan Skill Anda menyelesaikan masalah nyata alih-alih mendokumentasikan masalah yang dibayangkan.

**Pengembangan berbasis evaluasi:**

1. **Identifikasi kesenjangan:** Jalankan Claude pada tugas representatif tanpa Skill. Dokumentasikan kegagalan spesifik atau konteks yang hilang
2. **Buat evaluasi:** Bangun tiga skenario yang menguji kesenjangan ini
3. **Tetapkan baseline:** Ukur kinerja Claude tanpa Skill
4. **Tulis instruksi minimal:** Buat konten secukupnya untuk mengatasi kesenjangan dan lulus evaluasi
5. **Iterasi:** Jalankan evaluasi, bandingkan dengan baseline, dan perbaiki

Pendekatan ini memastikan Anda menyelesaikan masalah aktual alih-alih mengantisipasi persyaratan yang mungkin tidak pernah terwujud.

**Struktur evaluasi:**

```json
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using an appropriate PDF processing library or command-line tool",
    "Extracts text content from all pages in the document without missing any pages",
    "Saves the extracted text to a file named output.txt in a clear, readable format"
  ]
}
```

<Note>
  Contoh ini mendemonstrasikan evaluasi berbasis data dengan rubrik pengujian sederhana. Saat ini belum ada cara bawaan untuk menjalankan evaluasi ini. Pengguna dapat membuat sistem evaluasi mereka sendiri. Evaluasi adalah sumber kebenaran Anda untuk mengukur efektivitas Skill.
</Note>

### Kembangkan Skill secara iteratif dengan Claude

Proses pengembangan Skill yang paling efektif melibatkan Claude itu sendiri. Bekerjalah dengan satu instans Claude ("Claude A") untuk membuat Skill yang digunakan oleh instans lain ("Claude B"). Claude A membantu Anda merancang dan menyempurnakan instruksi, sementara Claude B mengujinya dalam tugas nyata. Ini berhasil karena model Claude memahami cara menulis instruksi agen yang efektif dan informasi apa yang dibutuhkan agen.

**Membuat Skill baru:**

1. **Selesaikan tugas tanpa Skill:** Kerjakan masalah dengan Claude A menggunakan prompting biasa. Saat Anda bekerja, Anda secara alami akan memberikan konteks, menjelaskan preferensi, dan berbagi pengetahuan prosedural. Perhatikan informasi apa yang berulang kali Anda berikan.

2. **Identifikasi pola yang dapat digunakan kembali:** Setelah menyelesaikan tugas, identifikasi konteks apa yang Anda berikan yang akan berguna untuk tugas serupa di masa depan.

   **Contoh:** Jika Anda mengerjakan analisis BigQuery, Anda mungkin telah memberikan nama tabel, definisi field, aturan pemfilteran (seperti "selalu kecualikan akun uji"), dan pola kueri umum.

3. **Minta Claude A untuk membuat Skill:** "Buat Skill yang menangkap pola analisis BigQuery yang baru saja kita gunakan. Sertakan skema tabel, konvensi penamaan, dan aturan tentang pemfilteran akun uji."

   <Tip>
     Model Claude memahami format dan struktur Skill secara native. Anda tidak memerlukan prompt sistem khusus atau skill "menulis skill" agar Claude membantu membuat Skill. Cukup minta Claude untuk membuat Skill dan ia akan menghasilkan konten SKILL.md yang terstruktur dengan benar dengan frontmatter dan isi konten yang sesuai.
   </Tip>

4. **Tinjau untuk keringkasan:** Periksa bahwa Claude A tidak menambahkan penjelasan yang tidak perlu. Tanyakan: "Hapus penjelasan tentang apa arti win rate - Claude sudah tahu itu."

5. **Tingkatkan arsitektur informasi:** Minta Claude A untuk mengatur konten dengan lebih efektif. Misalnya: "Atur ini agar skema tabel berada di file referensi terpisah. Kita mungkin menambahkan lebih banyak tabel nanti."

6. **Uji pada tugas serupa:** Gunakan Skill dengan Claude B (instans baru dengan Skill yang dimuat) pada kasus penggunaan terkait. Amati apakah Claude B menemukan informasi yang tepat, menerapkan aturan dengan benar, dan menangani tugas dengan sukses.

7. **Iterasi berdasarkan pengamatan:** Jika Claude B kesulitan atau melewatkan sesuatu, kembali ke Claude A dengan detail spesifik: "Ketika Claude menggunakan Skill ini, ia lupa memfilter berdasarkan tanggal untuk Q4. Haruskah kita menambahkan bagian tentang pola pemfilteran tanggal?"

**Iterasi pada Skill yang sudah ada:**

Pola hierarkis yang sama berlanjut saat meningkatkan Skill. Anda bergantian antara:

* **Bekerja dengan Claude A** (ahli yang membantu menyempurnakan Skill)
* **Menguji dengan Claude B** (agen yang menggunakan Skill untuk melakukan pekerjaan nyata)
* **Mengamati perilaku Claude B** dan membawa wawasan kembali ke Claude A

1. **Gunakan Skill dalam alur kerja nyata:** Berikan Claude B (dengan Skill yang dimuat) tugas aktual, bukan skenario uji

2. **Amati perilaku Claude B:** Catat di mana ia kesulitan, berhasil, atau membuat pilihan yang tidak terduga

   **Contoh pengamatan:** "Ketika saya meminta Claude B untuk laporan penjualan regional, ia menulis kueri tetapi lupa memfilter akun uji, meskipun Skill menyebutkan aturan ini."

3. **Kembali ke Claude A untuk perbaikan:** Bagikan SKILL.md saat ini dan jelaskan apa yang Anda amati. Tanyakan: "Saya perhatikan Claude B lupa memfilter akun uji ketika saya meminta laporan regional. Skill menyebutkan pemfilteran, tetapi mungkin tidak cukup menonjol?"

4. **Tinjau saran Claude A:** Claude A mungkin menyarankan pengaturan ulang untuk membuat aturan lebih menonjol, menggunakan bahasa yang lebih kuat seperti "MUST filter" alih-alih "always filter," atau merestrukturisasi bagian alur kerja.

5. **Terapkan dan uji perubahan:** Perbarui Skill dengan penyempurnaan Claude A, lalu uji lagi dengan Claude B pada permintaan serupa

6. **Ulangi berdasarkan penggunaan:** Lanjutkan siklus amati-perbaiki-uji ini saat Anda menemukan skenario baru. Setiap iterasi meningkatkan Skill berdasarkan perilaku agen nyata, bukan asumsi.

**Mengumpulkan umpan balik tim:**

1. Bagikan Skill dengan rekan tim dan amati penggunaan mereka
2. Tanyakan: Apakah Skill aktif saat diharapkan? Apakah instruksinya jelas? Apa yang kurang?
3. Masukkan umpan balik untuk mengatasi kesenjangan dalam pola penggunaan Anda sendiri

**Mengapa pendekatan ini berhasil:** Claude A memahami kebutuhan agen, Anda memberikan keahlian domain, Claude B mengungkapkan kesenjangan melalui penggunaan nyata, dan penyempurnaan iteratif meningkatkan Skill berdasarkan perilaku yang diamati alih-alih asumsi.

### Amati bagaimana Claude menavigasi Skill

Saat Anda mengiterasi Skill, perhatikan bagaimana Claude benar-benar menggunakannya dalam praktik. Perhatikan:

* **Jalur eksplorasi yang tidak terduga:** Apakah Claude membaca file dalam urutan yang tidak Anda antisipasi? Ini mungkin menunjukkan struktur Anda tidak seintuitif yang Anda kira
* **Koneksi yang terlewat:** Apakah Claude gagal mengikuti referensi ke file penting? Tautan Anda mungkin perlu lebih eksplisit atau menonjol
* **Ketergantungan berlebihan pada bagian tertentu:** Jika Claude berulang kali membaca file yang sama, pertimbangkan apakah konten tersebut seharusnya berada di SKILL.md utama
* **Konten yang diabaikan:** Jika Claude tidak pernah mengakses file yang dibundel, file tersebut mungkin tidak diperlukan atau kurang ditandai dengan baik dalam instruksi utama

Iterasi berdasarkan pengamatan ini alih-alih asumsi. 'name' dan 'description' dalam metadata Skill Anda sangat penting. Claude menggunakannya saat menentukan apakah akan memicu Skill sebagai respons terhadap tugas saat ini. Pastikan keduanya dengan jelas menjelaskan apa yang dilakukan Skill dan kapan harus digunakan.

## Anti-pola yang harus dihindari

### Hindari jalur gaya Windows

Selalu gunakan garis miring ke depan dalam jalur file, bahkan di Windows:

* ✓ **Baik:** `scripts/helper.py`, `reference/guide.md`
* ✗ **Hindari:** `scripts\helper.py`, `reference\guide.md`

Jalur gaya Unix bekerja di semua platform, sementara jalur gaya Windows menyebabkan kesalahan pada sistem Unix.

### Hindari menawarkan terlalu banyak opsi

Jangan sajikan beberapa pendekatan kecuali diperlukan:

````markdown
**Bad example: Too many choices** (confusing):
"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."

**Good example: Provide a default** (with escape hatch):
"Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."
````

## Lanjutan: Skill dengan kode yang dapat dieksekusi

Bagian berikut berfokus pada Skill yang menyertakan skrip yang dapat dieksekusi. Jika Skill Anda hanya menggunakan instruksi markdown, lewati ke [Checklist untuk Skill yang efektif](#checklist-for-effective-skills).

### Selesaikan, jangan tunda

Saat menulis skrip untuk Skill, tangani kondisi kesalahan alih-alih menyerahkannya kepada Claude.

**Contoh baik: Tangani kesalahan secara eksplisit:**

```python
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # Buat file dengan konten default alih-alih gagal
        print(f"File {path} not found, creating default")
        with open(path, "w") as f:
            f.write("")
        return ""
    except PermissionError:
        # Berikan alternatif alih-alih gagal
        print(f"Cannot access {path}, using default")
        return ""
```

**Contoh buruk: Menyerahkan kepada Claude:**

```python
def process_file(path):
    # Cukup gagalkan dan biarkan Claude yang menanganinya
    return open(path).read()
```

Parameter konfigurasi juga harus dijustifikasi dan didokumentasikan untuk menghindari "voodoo constants" (hukum Ousterhout). Jika Anda tidak tahu nilai yang tepat, bagaimana Claude akan menentukannya?

**Contoh baik: Mendokumentasikan diri sendiri:**

```python
# Permintaan HTTP biasanya selesai dalam 30 detik
# Timeout yang lebih lama memperhitungkan koneksi yang lambat
REQUEST_TIMEOUT = 30

# Tiga kali percobaan ulang menyeimbangkan keandalan dan kecepatan
# Sebagian besar kegagalan intermiten teratasi pada percobaan ulang kedua
MAX_RETRIES = 3
```

**Contoh buruk: Angka ajaib:**

```python
TIMEOUT = 47  # Why 47?
RETRIES = 5  # Why 5?
```

### Sediakan skrip utilitas

Bahkan jika Claude dapat menulis skrip, skrip yang sudah jadi menawarkan keuntungan:

**Manfaat skrip utilitas:**

* Lebih andal daripada kode yang dihasilkan
* Menghemat token (tidak perlu menyertakan kode dalam konteks)
* Menghemat waktu (tidak perlu pembuatan kode)
* Memastikan konsistensi di seluruh penggunaan

![Membundel skrip yang dapat dieksekusi bersama file instruksi](/docs/images/agent-skills-executable-scripts.png)

Diagram sebelumnya menunjukkan bagaimana skrip yang dapat dieksekusi bekerja bersama file instruksi. File instruksi (forms.md) merujuk skrip, dan Claude dapat mengeksekusinya tanpa memuat isinya ke dalam konteks.

**Perbedaan penting:** Perjelas dalam instruksi Anda apakah Claude harus:

* **Mengeksekusi skrip** (paling umum): "Run `analyze_form.py` to extract fields"
* **Membacanya sebagai referensi** (untuk logika kompleks): "See `analyze_form.py` for the field extraction algorithm"

Untuk sebagian besar skrip utilitas, eksekusi lebih disukai karena lebih andal dan efisien. Lihat bagian [Lingkungan runtime](#runtime-environment) berikut untuk detail tentang cara kerja eksekusi skrip.

**Contoh:**

````markdown
## Utility scripts

**analyze_form.py**: Extract all form fields from PDF

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

Output format:
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

**validate_boxes.py**: Check for overlapping bounding boxes

```bash
python scripts/validate_boxes.py fields.json
# Returns: "OK" or lists conflicts
```

**fill_form.py**: Apply field values to PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
````

### Gunakan analisis visual

Ketika input dapat dirender sebagai gambar, minta Claude menganalisisnya:

````markdown
## Form layout analysis

1. Convert PDF to images:
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. Analyze each page image to identify form fields
3. Claude can see field locations and types visually
````

<Note>
  Dalam contoh ini, Anda perlu menulis skrip `pdf_to_images.py`.
</Note>

Kemampuan visi Claude membantu menganalisis tata letak dan struktur.

### Buat output perantara yang dapat diverifikasi

Ketika Claude melakukan tugas kompleks dan terbuka, ia dapat membuat kesalahan. Pola "rencanakan-validasi-eksekusi" menangkap kesalahan lebih awal dengan meminta Claude terlebih dahulu membuat rencana dalam format terstruktur, lalu memvalidasi rencana tersebut dengan skrip sebelum mengeksekusinya.

**Contoh:** Bayangkan meminta Claude untuk memperbarui 50 field formulir dalam PDF berdasarkan spreadsheet. Tanpa validasi, Claude mungkin merujuk field yang tidak ada, membuat nilai yang bertentangan, melewatkan field yang wajib, atau menerapkan pembaruan secara tidak benar.

**Solusi:** Gunakan pola alur kerja yang ditunjukkan sebelumnya (pengisian formulir PDF), tetapi tambahkan file `changes.json` perantara yang divalidasi sebelum menerapkan perubahan. Alur kerjanya menjadi: analisis → **buat file rencana** → **validasi rencana** → eksekusi → verifikasi.

**Mengapa pola ini berhasil:**

* **Menangkap kesalahan lebih awal:** Validasi menemukan masalah sebelum perubahan diterapkan
* **Dapat diverifikasi mesin:** Skrip memberikan verifikasi objektif
* **Perencanaan yang dapat dibalik:** Claude dapat mengiterasi rencana tanpa menyentuh yang asli
* **Debugging yang jelas:** Pesan kesalahan menunjuk ke masalah spesifik

**Kapan menggunakan:** Operasi batch, perubahan destruktif, aturan validasi kompleks, operasi berisiko tinggi.

**Tip implementasi:** Buat skrip validasi verbose dengan pesan kesalahan spesifik seperti "Field 'signature\_date' not found. Available fields: customer\_name, order\_total, signature\_date\_signed" untuk membantu Claude memperbaiki masalah.

### Dependensi paket

Skill berjalan di lingkungan eksekusi kode dengan batasan spesifik platform:

* **claude.ai:** Dapat menginstal paket dari npm dan PyPI serta menarik dari repositori GitHub
* **Claude API:** Tidak memiliki akses jaringan dan tidak ada instalasi paket saat runtime

Daftarkan paket yang diperlukan dalam SKILL.md Anda dan verifikasi ketersediaannya dalam dokumentasi [Alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool).

### Lingkungan runtime

Skill berjalan di lingkungan eksekusi kode dengan akses filesystem, perintah bash, dan kemampuan eksekusi kode. Untuk penjelasan konseptual arsitektur ini, lihat [Arsitektur Skill](/docs/id/agents-and-tools/agent-skills/overview#the-skills-architecture) di ikhtisar.

**Bagaimana ini memengaruhi penulisan Anda:**

**Bagaimana Claude mengakses Skill:**

1. **Metadata dimuat sebelumnya:** Saat startup, name dan description dari YAML frontmatter semua Skill dimuat ke dalam prompt sistem
2. **File dibaca sesuai permintaan:** Claude menggunakan alat Read bash untuk mengakses SKILL.md dan file lain dari filesystem saat diperlukan
3. **Skrip dieksekusi secara efisien:** Skrip utilitas dapat dieksekusi melalui bash tanpa memuat seluruh isinya ke dalam konteks. Hanya output skrip yang mengonsumsi token
4. **Tidak ada penalti konteks untuk file besar:** File referensi, data, atau dokumentasi tidak mengonsumsi token konteks sampai benar-benar dibaca

* **Jalur file penting:** Claude menavigasi direktori skill Anda seperti filesystem. Gunakan garis miring ke depan (`reference/guide.md`), bukan garis miring terbalik

* **Beri nama file secara deskriptif:** Gunakan nama yang menunjukkan konten: `form_validation_rules.md`, bukan `doc2.md`

* **Atur untuk penemuan:** Strukturkan direktori berdasarkan domain atau fitur

  * Baik: `reference/finance.md`, `reference/sales.md`
  * Buruk: `docs/file1.md`, `docs/file2.md`

* **Bundel sumber daya yang komprehensif:** Sertakan dokumentasi API lengkap, contoh ekstensif, dataset besar; tidak ada penalti konteks sampai diakses

* **Lebih suka skrip untuk operasi deterministik:** Tulis `validate_form.py` alih-alih meminta Claude menghasilkan kode validasi

* **Perjelas maksud eksekusi:**

  * "Run `analyze_form.py` to extract fields" (eksekusi)
  * "See `analyze_form.py` for the extraction algorithm" (baca sebagai referensi)

* **Uji pola akses file:** Verifikasi Claude dapat menavigasi struktur direktori Anda dengan menguji menggunakan permintaan nyata

**Contoh:**

```text
bigquery-skill/
├── SKILL.md (overview, points to reference files)
└── reference/
    ├── finance.md (revenue metrics)
    ├── sales.md (pipeline data)
    └── product.md (usage analytics)
```

Ketika pengguna bertanya tentang pendapatan, Claude membaca SKILL.md, melihat referensi ke `reference/finance.md`, dan memanggil bash untuk membaca hanya file itu. File sales.md dan product.md tetap berada di filesystem, mengonsumsi nol token konteks sampai diperlukan. Model berbasis filesystem inilah yang memungkinkan progressive disclosure. Claude dapat menavigasi dan memuat secara selektif persis apa yang dibutuhkan setiap tugas.

Untuk detail lengkap tentang arsitektur teknis, lihat [Cara kerja Skill](/docs/id/agents-and-tools/agent-skills/overview#how-skills-work) di ikhtisar Skill.

### Referensi alat MCP

Jika Skill Anda menggunakan alat MCP (Model Context Protocol), selalu gunakan nama alat yang sepenuhnya memenuhi syarat untuk menghindari kesalahan "tool not found".

**Format:** `ServerName:tool_name`

**Contoh:**

```markdown
Use the BigQuery:bigquery_schema tool to retrieve table schemas.
Use the GitHub:create_issue tool to create issues.
```

Di mana:

* `BigQuery` dan `GitHub` adalah nama server MCP
* `bigquery_schema` dan `create_issue` adalah nama alat dalam server tersebut

Tanpa prefiks server, Claude mungkin gagal menemukan alat tersebut, terutama ketika beberapa server MCP tersedia.

### Hindari mengasumsikan alat sudah terinstal

Jangan berasumsi paket tersedia:

````markdown
**Bad example: Assumes installation**:
"Use the pdf library to process the file."

**Good example: Explicit about dependencies**:
"Install required package: `pip install pypdf`

Then use it:
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```"
````

## Catatan teknis

### Persyaratan YAML frontmatter

Frontmatter SKILL.md memerlukan field `name` dan `description` dengan aturan validasi spesifik:

* `name`: Maksimum 64 karakter, hanya huruf kecil/angka/tanda hubung, tanpa tag XML, tanpa kata yang dicadangkan
* `description`: Maksimum 1.024 karakter, tidak kosong, tanpa tag XML

Lihat [ikhtisar Skill](/docs/id/agents-and-tools/agent-skills/overview#skill-structure) untuk detail struktur lengkap.

### Anggaran token

Jaga isi SKILL.md di bawah 500 baris untuk kinerja optimal. Jika konten Anda melebihi ini, pisahkan ke file terpisah menggunakan pola progressive disclosure yang dijelaskan sebelumnya. Untuk detail arsitektur, lihat [ikhtisar Skill](/docs/id/agents-and-tools/agent-skills/overview#how-skills-work).

## Checklist untuk Skill yang efektif

Sebelum membagikan Skill, verifikasi:

### Kualitas inti

* [ ] Deskripsi spesifik dan menyertakan istilah kunci
* [ ] Deskripsi mencakup apa yang dilakukan Skill dan kapan menggunakannya
* [ ] Isi SKILL.md di bawah 500 baris
* [ ] Detail tambahan berada di file terpisah (jika diperlukan)
* [ ] Tidak ada informasi yang sensitif terhadap waktu (atau berada di bagian "pola lama")
* [ ] Terminologi konsisten di seluruh dokumen
* [ ] Contoh bersifat konkret, bukan abstrak
* [ ] Referensi file satu tingkat
* [ ] Progressive disclosure digunakan dengan tepat
* [ ] Alur kerja memiliki langkah yang jelas

### Kode dan skrip

* [ ] Skrip menyelesaikan masalah alih-alih menyerahkannya kepada Claude
* [ ] Penanganan kesalahan eksplisit dan membantu
* [ ] Tidak ada "voodoo constants" (semua nilai dijustifikasi)
* [ ] Paket yang diperlukan tercantum dalam instruksi dan diverifikasi ketersediaannya
* [ ] Skrip memiliki dokumentasi yang jelas
* [ ] Tidak ada jalur gaya Windows (semua garis miring ke depan)
* [ ] Langkah validasi/verifikasi untuk operasi penting
* [ ] Loop umpan balik disertakan untuk tugas yang kritis terhadap kualitas

### Pengujian

* [ ] Setidaknya tiga evaluasi dibuat
* [ ] Diuji dengan Haiku, Sonnet, dan Opus
* [ ] Diuji dengan skenario penggunaan nyata
* [ ] Umpan balik tim dimasukkan (jika berlaku)

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mulai dengan Agent Skills" icon="rocket" href="/docs/id/agents-and-tools/agent-skills/quickstart">
    Buat Skill pertama Anda
  </Card>

  <Card title="Gunakan Skill di Claude Code" icon="terminal" href="https://code.claude.com/docs/id/skills">
    Buat dan kelola Skill di Claude Code
  </Card>

  <Card title="Gunakan Skill dengan API" icon="code" href="/docs/id/build-with-claude/skills-guide">
    Unggah dan gunakan Skill secara terprogram
  </Card>
</CardGroup>
