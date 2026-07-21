---
source: platform
url: https://platform.claude.com/docs/id/about-claude/use-case-guides/legal-summarization
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 72383352470397e57259a4c9aa0d3ef4bda8ef8ccfb1f4e79a0e52fcfeeebd1e
---

# Peringkasan dokumen hukum

Panduan ini menjelaskan cara memanfaatkan kemampuan pemrosesan bahasa alami canggih dari Claude untuk meringkas dokumen hukum secara efisien, mengekstrak informasi penting, dan mempercepat riset hukum. Dengan Claude, Anda dapat menyederhanakan peninjauan kontrak, persiapan litigasi, dan pekerjaan regulasi, sehingga menghemat waktu dan memastikan akurasi dalam proses hukum Anda.

---

> Kunjungi [cookbook peringkasan](https://platform.claude.com/cookbook/capabilities-summarization-guide) untuk melihat contoh implementasi peringkasan dokumen hukum menggunakan Claude.

## Sebelum membangun dengan Claude

### Tentukan apakah akan menggunakan Claude untuk peringkasan dokumen hukum

Berikut adalah beberapa indikator utama bahwa Anda sebaiknya menggunakan LLM seperti Claude untuk meringkas dokumen hukum:

<AccordionGroup>
  <Accordion title="Anda ingin meninjau dokumen dalam volume besar secara efisien dan terjangkau">
    Peninjauan dokumen berskala besar dapat memakan waktu dan biaya yang mahal jika dilakukan secara manual. Claude dapat memproses dan meringkas dokumen hukum dalam jumlah besar dengan cepat, sehingga secara signifikan mengurangi waktu dan biaya yang terkait dengan peninjauan dokumen. Kemampuan ini sangat berharga untuk tugas-tugas seperti uji tuntas (due diligence), analisis kontrak, atau penemuan litigasi (litigation discovery), di mana efisiensi sangat penting.
  </Accordion>

  <Accordion title="Anda memerlukan ekstraksi metadata penting secara otomatis">
    Claude dapat secara efisien mengekstrak dan mengategorikan metadata penting dari dokumen hukum, seperti pihak-pihak yang terlibat, tanggal, ketentuan kontrak, atau klausul tertentu. Ekstraksi otomatis ini dapat membantu mengorganisasi informasi, sehingga lebih mudah untuk mencari, menganalisis, dan mengelola kumpulan dokumen yang besar. Ini sangat berguna untuk manajemen kontrak, pemeriksaan kepatuhan, atau pembuatan basis data informasi hukum yang dapat dicari. 
  </Accordion>

  <Accordion title="Anda ingin menghasilkan ringkasan yang jelas, ringkas, dan terstandardisasi">
    Claude dapat menghasilkan ringkasan terstruktur yang mengikuti format yang telah ditentukan sebelumnya, sehingga memudahkan para profesional hukum untuk dengan cepat memahami poin-poin utama dari berbagai dokumen. Ringkasan terstandardisasi ini dapat meningkatkan keterbacaan, memfasilitasi perbandingan antar dokumen, dan meningkatkan pemahaman secara keseluruhan, terutama ketika berhadapan dengan bahasa hukum yang kompleks atau jargon teknis.
  </Accordion>

  <Accordion title="Anda memerlukan sitasi yang tepat untuk ringkasan Anda">
    Saat membuat ringkasan hukum, atribusi dan sitasi yang tepat sangat penting untuk memastikan kredibilitas dan kepatuhan terhadap standar hukum. Claude dapat diberi prompt untuk menyertakan sitasi yang akurat untuk semua poin hukum yang dirujuk, sehingga memudahkan para profesional hukum untuk meninjau dan memverifikasi informasi yang diringkas.
  </Accordion>

  <Accordion title="Anda ingin menyederhanakan dan mempercepat proses riset hukum Anda">
    Claude dapat membantu dalam riset hukum dengan menganalisis secara cepat volume besar yurisprudensi, undang-undang, dan komentar hukum. Claude dapat mengidentifikasi preseden yang relevan, mengekstrak prinsip-prinsip hukum utama, dan meringkas argumen hukum yang kompleks. Kemampuan ini dapat secara signifikan mempercepat proses riset, memungkinkan para profesional hukum untuk fokus pada analisis tingkat tinggi dan pengembangan strategi.
  </Accordion>
</AccordionGroup>

### Tentukan detail yang ingin Anda ekstrak dalam peringkasan

Tidak ada satu ringkasan yang benar untuk dokumen tertentu. Tanpa arahan yang jelas, Claude mungkin kesulitan menentukan detail mana yang harus disertakan. Untuk mencapai hasil yang optimal, identifikasi informasi spesifik yang ingin Anda sertakan dalam ringkasan.

Misalnya, saat meringkas perjanjian sewa-menyewa kembali (sublease agreement), Anda mungkin ingin mengekstrak poin-poin utama berikut:

```python
details_to_extract = [
    "Parties involved (sublessor, sublessee, and original lessor)",
    "Property details (address, description, and permitted use)",
    "Term and rent (start date, end date, monthly rent, and security deposit)",
    "Responsibilities (utilities, maintenance, and repairs)",
    "Consent and notices (landlord's consent, and notice requirements)",
    "Special provisions (furniture, parking, and subletting restrictions)",
]
```

### Tetapkan kriteria keberhasilan

Mengevaluasi kualitas ringkasan adalah tugas yang terkenal menantang. Tidak seperti banyak tugas pemrosesan bahasa alami lainnya, evaluasi ringkasan sering kali tidak memiliki metrik yang jelas dan objektif. Prosesnya bisa sangat subjektif, dengan pembaca yang berbeda menghargai aspek ringkasan yang berbeda pula. Berikut adalah kriteria yang mungkin ingin Anda pertimbangkan saat menilai seberapa baik Claude melakukan peringkasan dokumen hukum.

<AccordionGroup>
  <Accordion title="Kebenaran faktual">
    Ringkasan harus secara akurat merepresentasikan fakta, konsep hukum, dan poin-poin utama dalam dokumen.
  </Accordion>

  <Accordion title="Presisi hukum">
    Terminologi dan referensi ke undang-undang, yurisprudensi, atau regulasi harus benar dan selaras dengan standar hukum.
  </Accordion>

  <Accordion title="Keringkasan">
     Ringkasan harus memadatkan dokumen hukum ke poin-poin esensialnya tanpa kehilangan detail penting.
  </Accordion>

  <Accordion title="Konsistensi">
    Jika meringkas beberapa dokumen, LLM harus mempertahankan struktur dan pendekatan yang konsisten untuk setiap ringkasan.
  </Accordion>

  <Accordion title="Keterbacaan">
    Teks harus jelas dan mudah dipahami. Jika audiensnya bukan ahli hukum, peringkasan tidak boleh menyertakan jargon hukum yang dapat membingungkan audiens.
  </Accordion>

  <Accordion title="Bias dan keadilan">
    Ringkasan harus menyajikan gambaran yang tidak bias dan adil tentang argumen dan posisi hukum.
  </Accordion>
</AccordionGroup>

Lihat panduan tentang [menetapkan kriteria keberhasilan](/docs/id/test-and-evaluate/develop-tests) untuk informasi lebih lanjut.

***

## Cara meringkas dokumen hukum menggunakan Claude

### Pilih model Claude yang tepat

Akurasi model sangat penting saat meringkas dokumen hukum. Claude Opus 4.8 adalah pilihan yang sangat baik untuk kasus penggunaan seperti ini di mana akurasi tinggi diperlukan. Jika ukuran dan jumlah dokumen Anda besar sehingga biaya mulai menjadi perhatian, Anda juga dapat mencoba menggunakan model yang lebih kecil seperti Claude Haiku 4.5.

Untuk membantu memperkirakan biaya ini, berikut adalah perbandingan biaya untuk meringkas 1.000 perjanjian sewa-menyewa kembali menggunakan Opus dan Haiku:

* **Ukuran konten**

  * Jumlah perjanjian: 1.000
  * Karakter per perjanjian: 300.000
  * Total karakter: 300 juta

* **Estimasi token**

  * Token input: 86 juta (dengan asumsi 1 token per 3,5 karakter)
  * Token output per ringkasan: 350
  * Total token output: 350.000

* **Estimasi biaya Claude Opus 4.8**

  * Biaya token input: 86 MTok \* $5,00/MTok = $430,00 USD
  * Biaya token output: 0,35 MTok \* $25,00/MTok = $8,75 USD
  * Total biaya: $430,00 + $8,75 = $438,75 USD

* **Estimasi biaya Claude Haiku 4.5**

  * Biaya token input: 86 MTok \* $1,00/MTok = $86,00 USD
  * Biaya token output: 0,35 MTok \* $5,00/MTok = $1,75 USD
  * Total biaya: $86,00 + $1,75 = $87,75 USD

<Tip>
  Biaya aktual mungkin berbeda dari estimasi ini. Estimasi ini didasarkan pada contoh yang disorot di bagian tentang 

  [prompting](#build-a-strong-prompt)

  .
</Tip>

### Ubah dokumen menjadi format yang dapat diproses Claude

Sebelum Anda mulai meringkas dokumen, Anda perlu menyiapkan data Anda. Ini melibatkan ekstraksi teks dari PDF, pembersihan teks, dan memastikan teks siap diproses oleh Claude.

Berikut adalah demonstrasi proses ini pada contoh pdf:

```python
from io import BytesIO
import re

import pypdf
import requests


def get_llm_text(pdf_file):
    reader = pypdf.PdfReader(pdf_file)
    text = "\n".join([page.extract_text() for page in reader.pages])

    # Hapus nomor halaman
    text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

    # Hapus spasi berlebih
    text = re.sub(r"\s+", " ", text)

    return text


# Buat URL lengkap dari repositori GitHub
url = "https://raw.githubusercontent.com/anthropics/anthropic-cookbook/main/skills/summarization/data/Sample Sublease Agreement.pdf"
url = url.replace(" ", "%20")

# Unduh file PDF ke dalam memori
response = requests.get(url)

# Muat PDF dari memori
pdf_file = BytesIO(response.content)

document_text = get_llm_text(pdf_file)
print(document_text[:50000])
```

Dalam contoh ini, Anda terlebih dahulu mengunduh pdf dari contoh perjanjian sewa-menyewa kembali yang digunakan dalam [cookbook peringkasan](https://platform.claude.com/cookbook/capabilities-summarization-guide). Perjanjian ini bersumber dari perjanjian sewa-menyewa kembali yang tersedia untuk umum dari [situs web sec.gov](https://www.sec.gov/Archives/edgar/data/1045425/000119312507044370/dex1032.htm).

Contoh ini menggunakan pustaka pypdf untuk mengekstrak konten pdf dan mengonversinya menjadi teks. Data teks kemudian dibersihkan dengan menghapus nomor halaman dan spasi berlebih.

### Bangun prompt yang kuat

Claude dapat beradaptasi dengan berbagai gaya peringkasan. Anda dapat mengubah detail prompt untuk mengarahkan Claude agar lebih atau kurang bertele-tele, menyertakan lebih banyak atau lebih sedikit terminologi teknis, atau memberikan ringkasan tingkat tinggi atau rendah dari konteks yang ada.

Berikut adalah contoh cara membuat prompt yang memastikan ringkasan yang dihasilkan mengikuti struktur yang konsisten saat menganalisis perjanjian sewa-menyewa kembali:

```python Python
# Inisialisasi klien Anthropic
client = anthropic.Anthropic()


def summarize_document(
    text, details_to_extract, model="claude-opus-4-8", max_tokens=1000
):
    # Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
    details_to_extract_str = "\n".join(details_to_extract)

    # Minta model untuk meringkas perjanjian sub-sewa
    prompt = f"""Summarize the following sublease agreement. Focus on these key aspects:

    {details_to_extract_str}

    Provide the summary in bullet points nested within the XML header for each section. For example:

    <parties involved>
    - Sublessor: [Name]
    // Add more details as needed
    </parties involved>

    If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.

    Sublease agreement text:
    {text}
    """

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system="You are a legal analyst specializing in real estate law, known for highly accurate and detailed summaries of sublease agreements.",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response.content[0].text


sublease_summary = summarize_document(document_text, details_to_extract)
print(sublease_summary)
```

Kode ini mengimplementasikan fungsi `summarize_document` yang menggunakan Claude untuk meringkas konten perjanjian sewa-menyewa kembali. Fungsi ini menerima string teks dan daftar detail yang akan diekstrak sebagai input. Dalam contoh ini, kode memanggil fungsi dengan variabel `document_text` dan `details_to_extract` yang didefinisikan dalam cuplikan kode sebelumnya.

Di dalam fungsi, sebuah prompt dibuat untuk Claude, termasuk dokumen yang akan diringkas, detail yang akan diekstrak, dan instruksi spesifik untuk meringkas dokumen. Prompt tersebut menginstruksikan Claude untuk merespons dengan ringkasan dari setiap detail yang akan diekstrak, yang disarangkan di dalam header XML.

Karena kode menghasilkan setiap bagian ringkasan di dalam tag, setiap bagian dapat dengan mudah diurai sebagai langkah pasca-pemrosesan. Pendekatan ini memungkinkan ringkasan terstruktur yang dapat disesuaikan untuk kasus penggunaan Anda, sehingga setiap ringkasan mengikuti pola yang sama.

### Evaluasi prompt Anda

Prompting sering kali memerlukan pengujian dan optimasi agar siap untuk produksi. Untuk menentukan kesiapan solusi Anda, evaluasi kualitas ringkasan Anda menggunakan proses sistematis yang menggabungkan metode kuantitatif dan kualitatif. Membuat [evaluasi empiris yang kuat](/docs/id/test-and-evaluate/develop-tests#building-evals-and-test-cases) berdasarkan kriteria keberhasilan yang telah Anda tetapkan memungkinkan Anda mengoptimalkan prompt Anda. Berikut adalah beberapa metrik yang mungkin ingin Anda sertakan dalam evaluasi empiris Anda:

<AccordionGroup>
  <Accordion title="Skor ROUGE">
    Ini mengukur tumpang tindih antara ringkasan yang dihasilkan dan ringkasan referensi yang dibuat oleh ahli. Metrik ini terutama berfokus pada recall dan berguna untuk mengevaluasi cakupan konten.
  </Accordion>

  <Accordion title="Skor BLEU">
    Meskipun awalnya dikembangkan untuk terjemahan mesin, metrik ini dapat diadaptasi untuk tugas peringkasan. Skor BLEU mengukur presisi kecocokan n-gram antara ringkasan yang dihasilkan dan ringkasan referensi. Skor yang lebih tinggi menunjukkan bahwa ringkasan yang dihasilkan mengandung frasa dan terminologi yang serupa dengan ringkasan referensi. 
  </Accordion>

  <Accordion title="Kemiripan embedding kontekstual">
    Metrik ini melibatkan pembuatan representasi vektor (embedding) dari ringkasan yang dihasilkan dan ringkasan referensi. Kemiripan antara embedding ini kemudian dihitung, sering kali menggunakan cosine similarity. Skor kemiripan yang lebih tinggi menunjukkan bahwa ringkasan yang dihasilkan menangkap makna semantik dan konteks dari ringkasan referensi, meskipun kata-kata persisnya berbeda.
  </Accordion>

  <Accordion title="Penilaian berbasis LLM">
    Metode ini melibatkan penggunaan LLM seperti Claude untuk mengevaluasi kualitas ringkasan yang dihasilkan berdasarkan rubrik penilaian. Rubrik dapat disesuaikan dengan kebutuhan spesifik Anda, menilai faktor-faktor utama seperti akurasi, kelengkapan, dan koherensi. Untuk panduan tentang penerapan penilaian berbasis LLM, lihat 

    [tips ini](/docs/id/test-and-evaluate/develop-tests#tips-for-llm-based-grading)

    .
  </Accordion>

  <Accordion title="Evaluasi manusia">
    Selain membuat ringkasan referensi, ahli hukum juga dapat mengevaluasi kualitas ringkasan yang dihasilkan. Meskipun ini mahal dan memakan waktu dalam skala besar, ini sering dilakukan pada beberapa ringkasan sebagai pemeriksaan kewajaran sebelum diterapkan ke produksi.
  </Accordion>
</AccordionGroup>

### Terapkan prompt Anda

Berikut adalah beberapa pertimbangan tambahan yang perlu diingat saat Anda menerapkan solusi Anda ke produksi.

1. **Pastikan tidak ada tanggung jawab hukum:** Pahami implikasi hukum dari kesalahan dalam ringkasan, yang dapat menyebabkan tanggung jawab hukum bagi organisasi atau klien Anda. Berikan disclaimer atau pemberitahuan hukum yang menjelaskan bahwa ringkasan dihasilkan oleh AI dan harus ditinjau oleh profesional hukum.

2. **Tangani beragam jenis dokumen:** Panduan ini membahas cara mengekstrak teks dari PDF. Di dunia nyata, dokumen mungkin datang dalam berbagai format (PDF, dokumen Word, file teks, dll.). Pastikan pipeline ekstraksi data Anda dapat mengonversi semua format file yang Anda harapkan akan diterima.

3. **Paralelkan panggilan API ke Claude:** Dokumen panjang dengan jumlah token yang besar mungkin memerlukan waktu hingga satu menit bagi Claude untuk menghasilkan ringkasan. Untuk koleksi dokumen yang besar, Anda mungkin ingin mengirim panggilan API ke Claude secara paralel sehingga ringkasan dapat diselesaikan dalam jangka waktu yang wajar. Lihat [batas laju](/docs/id/api/rate-limits#rate-limits) Anthropic untuk menentukan jumlah maksimum panggilan API yang dapat dilakukan secara paralel.

***

## Tingkatkan performa

Dalam skenario yang kompleks, mungkin bermanfaat untuk mempertimbangkan strategi tambahan guna meningkatkan performa di luar [teknik rekayasa prompt](/docs/id/build-with-claude/prompt-engineering/overview) standar. Berikut adalah beberapa strategi lanjutan:

### Lakukan meta-summarization untuk meringkas dokumen panjang

Peringkasan dokumen hukum sering kali melibatkan penanganan dokumen panjang atau banyak dokumen terkait sekaligus, sehingga Anda melampaui jendela konteks Claude. Anda dapat menggunakan metode chunking yang dikenal sebagai "meta-summarization" (meta-peringkasan) untuk menangani kasus penggunaan ini. Teknik ini melibatkan pemecahan dokumen menjadi potongan-potongan yang lebih kecil dan dapat dikelola, lalu memproses setiap potongan secara terpisah. Anda kemudian dapat menggabungkan ringkasan dari setiap potongan untuk membuat meta-ringkasan dari seluruh dokumen.

Berikut adalah contoh cara melakukan meta-summarization:

```python Python
# Inisialisasi klien Anthropic
client = anthropic.Anthropic()


def chunk_text(text, chunk_size=20000):
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def summarize_long_document(
    text, details_to_extract, model="claude-opus-4-8", max_tokens=1000
):
    # Format detail yang akan diekstrak untuk ditempatkan dalam konteks prompt
    details_to_extract_str = "\n".join(details_to_extract)

    # Iterasi setiap potongan dan rangkum masing-masing
    chunk_summaries = [
        summarize_document(
            chunk, details_to_extract, model=model, max_tokens=max_tokens
        )
        for chunk in chunk_text(text)
    ]

    final_summary_prompt = f"""

    You are looking at the chunked summaries of multiple documents that are all related.
    Combine the following summaries of the document from different truthful sources into a coherent overall summary:

    <chunked_summaries>
    {"".join(chunk_summaries)}
    </chunked_summaries>

    Focus on these key aspects:
    {details_to_extract_str}

    Provide the summary in bullet points nested within the XML header for each section. For example:

    <parties involved>
    - Sublessor: [Name]
    // Add more details as needed
    </parties involved>

    If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.
    """

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system="You are a legal expert that summarizes notes on one document.",
        messages=[
            {"role": "user", "content": final_summary_prompt},
        ],
    )

    return response.content[0].text


long_summary = summarize_long_document(document_text, details_to_extract)
print(long_summary)
```

Fungsi `summarize_long_document` dibangun di atas fungsi `summarize_document` sebelumnya dengan membagi dokumen menjadi potongan-potongan yang lebih kecil dan meringkas setiap potongan secara individual.

Kode mencapai ini dengan menerapkan fungsi `summarize_document` ke setiap potongan berisi 20.000 karakter dalam dokumen asli. Ringkasan individual kemudian digabungkan, dan ringkasan akhir dibuat dari ringkasan-ringkasan potongan ini.

Perhatikan bahwa fungsi `summarize_long_document` tidak sepenuhnya diperlukan untuk contoh pdf ini, karena seluruh dokumen muat dalam jendela konteks Claude. Namun, fungsi ini menjadi penting untuk dokumen yang melebihi jendela konteks Claude atau saat meringkas beberapa dokumen terkait secara bersamaan. Terlepas dari itu, teknik meta-summarization ini sering kali menangkap detail penting tambahan dalam ringkasan akhir yang terlewatkan dalam pendekatan ringkasan tunggal sebelumnya.

### Gunakan dokumen terindeks ringkasan untuk menjelajahi koleksi dokumen yang besar

Mencari koleksi dokumen dengan LLM biasanya melibatkan "retrieval-augmented generation" (generasi yang diperkaya pengambilan), atau RAG. Namun, dalam skenario yang melibatkan dokumen besar atau ketika pengambilan informasi yang presisi sangat penting, pendekatan RAG dasar mungkin tidak memadai. Dokumen terindeks ringkasan (summary indexed documents) adalah pendekatan RAG lanjutan yang menyediakan cara yang lebih efisien untuk memeringkat dokumen untuk pengambilan, menggunakan lebih sedikit konteks dibandingkan metode RAG tradisional. Dalam pendekatan ini, Anda terlebih dahulu menggunakan Claude untuk menghasilkan ringkasan singkat untuk setiap dokumen dalam korpus Anda, lalu menggunakan Claude untuk memeringkat relevansi setiap ringkasan terhadap kueri yang diajukan. Untuk detail lebih lanjut tentang pendekatan ini, termasuk contoh berbasis kode, lihat bagian dokumen terindeks ringkasan di [cookbook peringkasan](https://platform.claude.com/cookbook/capabilities-summarization-guide).

### Lakukan fine-tuning pada Claude untuk belajar dari dataset Anda

Teknik lanjutan lainnya untuk meningkatkan kemampuan Claude dalam menghasilkan ringkasan adalah "fine-tuning" (penyetelan halus). Fine-tuning melibatkan pelatihan Claude pada dataset khusus yang secara spesifik selaras dengan kebutuhan peringkasan dokumen hukum Anda, memastikan bahwa Claude beradaptasi dengan kasus penggunaan Anda. Berikut adalah gambaran umum tentang cara melakukan fine-tuning:

1. **Identifikasi kesalahan:** Mulailah dengan mengumpulkan contoh-contoh di mana ringkasan Claude kurang memadai — ini bisa termasuk melewatkan detail hukum yang penting, salah memahami konteks, atau menggunakan terminologi hukum yang tidak tepat.

2. **Kurasi dataset:** Setelah Anda mengidentifikasi masalah-masalah ini, kumpulkan dataset dari contoh-contoh bermasalah tersebut. Dataset ini harus mencakup dokumen hukum asli beserta ringkasan yang telah Anda koreksi, memastikan bahwa Claude mempelajari perilaku yang diinginkan.

3. **Lakukan fine-tuning:** Fine-tuning melibatkan pelatihan ulang model pada dataset yang telah Anda kurasi untuk menyesuaikan bobot dan parameternya. Pelatihan ulang ini membantu Claude lebih memahami persyaratan spesifik dari domain hukum Anda, meningkatkan kemampuannya untuk meringkas dokumen sesuai dengan standar Anda.

4. **Peningkatan iteratif:** Fine-tuning bukanlah proses satu kali. Saat Claude terus menghasilkan ringkasan, Anda dapat secara iteratif menambahkan contoh-contoh baru di mana performanya kurang baik, sehingga semakin menyempurnakan kemampuannya. Seiring waktu, siklus umpan balik berkelanjutan ini akan menghasilkan model yang sangat terspesialisasi untuk tugas peringkasan dokumen hukum Anda.

<Tip>
  Fine-tuning saat ini hanya tersedia melalui Amazon Bedrock. Detail tambahan tersedia di 

  [blog peluncuran AWS](https://aws.amazon.com/blogs/machine-learning/fine-tune-anthropics-claude-3-haiku-in-amazon-bedrock-to-boost-model-accuracy-and-quality/)

  .
</Tip>

<CardGroup cols={2}>
  <Card title="Cookbook peringkasan" icon="link" href="https://platform.claude.com/cookbook/capabilities-summarization-guide">
    Lihat contoh berbasis kode yang diimplementasikan sepenuhnya tentang cara menggunakan Claude untuk meringkas kontrak.
  </Card>

  <Card title="Cookbook sitasi" icon="link" href="https://platform.claude.com/cookbook/misc-using-citations">
    Jelajahi resep cookbook Sitasi untuk panduan tentang cara memastikan akurasi dan keterjelasan informasi.
  </Card>
</CardGroup>
