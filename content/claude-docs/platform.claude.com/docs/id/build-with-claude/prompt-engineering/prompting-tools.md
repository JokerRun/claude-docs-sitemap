---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-tools
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: dd61e23bba6f1a6338bf8de0fe1b8f5ed8e16f6e886acbb4b3186ca92a6d55cc
---

# Alat prompting Console

---

Claude Console menawarkan serangkaian alat untuk membantu Anda membangun dan menyempurnakan prompt. Halaman ini memandu Anda melalui alat-alat tersebut dalam urutan yang biasanya Anda gunakan: membuat draf pertama, menambahkan template dan variabel, lalu menyempurnakan prompt yang sudah ada.

---

## Generator prompt

<Note>
Generator prompt kompatibel dengan semua model Claude, termasuk yang memiliki kemampuan extended thinking. Untuk tips prompting khusus model extended thinking, lihat [tips prompting extended thinking](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities).
</Note>

Terkadang, bagian tersulit dari menggunakan model AI adalah mencari tahu cara melakukan prompting secara efektif. Generator prompt memandu Claude untuk membuat template prompt berkualitas tinggi yang disesuaikan dengan tugas spesifik Anda, mengikuti banyak praktik terbaik rekayasa prompt kami.

Generator prompt sangat berguna untuk mengatasi "masalah halaman kosong"—ini memberi Anda titik awal untuk pengujian dan iterasi lebih lanjut.

<Tip>Coba generator prompt sekarang langsung di [Console](/dashboard).</Tip>

Jika Anda tertarik untuk menganalisis prompt dan arsitektur yang mendasarinya, lihat [notebook Google Colab generator prompt](https://anthropic.com/metaprompt-notebook/) kami. Untuk menjalankan notebook Colab, Anda memerlukan [kunci API](/settings/keys).

---

## Template prompt dan variabel

Saat men-deploy aplikasi berbasis LLM dengan Claude, panggilan API Anda biasanya terdiri dari dua jenis konten:
- **Konten tetap:** Instruksi atau konteks statis yang tetap konstan di berbagai interaksi
- **Konten variabel:** Elemen dinamis yang berubah dengan setiap permintaan atau percakapan, seperti:
    - Input pengguna
    - Konten yang diambil untuk Retrieval-Augmented Generation (RAG)
    - Konteks percakapan seperti riwayat akun pengguna
    - Data yang dihasilkan sistem seperti hasil penggunaan alat yang dimasukkan dari panggilan independen lain ke Claude

**Template prompt** menggabungkan bagian tetap dan variabel ini, menggunakan placeholder untuk konten dinamis. Di [Claude Console](/), placeholder ini dilambangkan dengan **\{\{tanda kurung ganda\}\}**, membuatnya mudah diidentifikasi dan memungkinkan pengujian cepat dengan nilai yang berbeda.

Anda harus menggunakan template prompt dan variabel ketika Anda mengharapkan bagian mana pun dari prompt Anda akan diulang dalam panggilan lain ke Claude (melalui API atau [Claude Console](/). [claude.ai](https://claude.ai/) saat ini tidak mendukung template prompt atau variabel).

Template prompt menawarkan beberapa manfaat:
- **Konsistensi:** Memastikan struktur yang konsisten untuk prompt Anda di berbagai interaksi
- **Efisiensi:** Mudah mengganti konten variabel tanpa menulis ulang seluruh prompt
- **Kemampuan pengujian:** Dengan cepat menguji input dan kasus tepi yang berbeda hanya dengan mengubah bagian variabel
- **Skalabilitas:** Menyederhanakan manajemen prompt seiring pertumbuhan kompleksitas aplikasi Anda
- **Kontrol versi:** Mudah melacak perubahan pada struktur prompt Anda dari waktu ke waktu dengan hanya memantau bagian inti dari prompt Anda, terpisah dari input dinamis

Console menggunakan template prompt dan variabel untuk mendukung alatnya:
- **Generator prompt:** Memutuskan variabel apa yang dibutuhkan prompt Anda dan menyertakannya dalam template yang dihasilkannya
- **Penyempurna prompt:** Mengambil template Anda yang sudah ada, termasuk semua variabel, dan mempertahankannya dalam template yang disempurnakan yang dihasilkannya
- **[Alat evaluasi](/docs/id/test-and-evaluate/eval-tool):** Memungkinkan Anda dengan mudah menguji, menskalakan, dan melacak versi prompt Anda dengan memisahkan bagian variabel dan tetap dari template prompt Anda

### Contoh template prompt

Pertimbangkan aplikasi sederhana yang menerjemahkan teks bahasa Inggris ke bahasa Spanyol. Teks yang diterjemahkan akan menjadi variabel karena berubah antar pengguna atau panggilan ke Claude. Anda mungkin menggunakan template prompt ini:

```text
Translate this text from English to Spanish: {{text}}
```

<Tip>Untuk meningkatkan variabel prompt Anda, bungkus dengan [tag XML](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#structure-prompts-with-xml-tags) untuk struktur yang lebih jelas.</Tip>

---

## Penyempurna prompt

<Note>
Penyempurna prompt kompatibel dengan semua model Claude, termasuk yang memiliki kemampuan extended thinking. Untuk tips prompting khusus model extended thinking, lihat [tips prompting extended thinking](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities).
</Note>

Penyempurna prompt membantu Anda dengan cepat melakukan iterasi dan menyempurnakan prompt Anda melalui analisis dan peningkatan otomatis. Alat ini unggul dalam membuat prompt lebih kuat untuk tugas-tugas kompleks yang memerlukan akurasi tinggi.

<Frame>
  ![Image](/docs/images/prompt_improver.png)
</Frame>

### Sebelum Anda mulai

Anda memerlukan:
- Template prompt (lihat [Template prompt dan variabel](#prompt-templates-and-variables) di atas)
- Umpan balik tentang masalah saat ini dengan output Claude (opsional tetapi disarankan)
- Contoh input dan output ideal (opsional tetapi disarankan)

### Cara kerja penyempurna prompt

Penyempurna prompt meningkatkan prompt Anda dalam 4 langkah:

1. **Identifikasi contoh**: Menemukan dan mengekstrak contoh dari template prompt Anda
2. **Draf awal**: Membuat template terstruktur dengan bagian yang jelas dan tag XML
3. **Penyempurnaan chain of thought**: Menambahkan dan menyempurnakan instruksi penalaran terperinci
4. **Peningkatan contoh**: Memperbarui contoh untuk mendemonstrasikan proses penalaran baru

Anda dapat melihat langkah-langkah ini terjadi secara real-time di modal peningkatan.

### Apa yang Anda dapatkan

Penyempurna prompt menghasilkan template dengan:
- Instruksi chain-of-thought terperinci yang memandu proses penalaran Claude dan biasanya meningkatkan kinerjanya
- Organisasi yang jelas menggunakan tag XML untuk memisahkan komponen yang berbeda
- Pemformatan contoh yang terstandarisasi yang mendemonstrasikan penalaran langkah demi langkah dari input ke output
- Prefill strategis yang memandu respons awal Claude

<Note>
Meskipun contoh muncul secara terpisah di UI Workbench, contoh-contoh tersebut disertakan di awal pesan pengguna pertama dalam panggilan API yang sebenarnya. Lihat format mentah dengan mengklik "**\<\/\> Get Code**" atau masukkan contoh sebagai teks mentah melalui kotak Examples.
</Note>

### Cara menggunakan penyempurna prompt

1. Kirimkan template prompt Anda
2. Tambahkan umpan balik apa pun tentang masalah dengan output Claude saat ini (misalnya, "ringkasan terlalu dasar untuk audiens ahli")
3. Sertakan contoh input dan output ideal
4. Tinjau prompt yang disempurnakan

### Hasilkan contoh pengujian

Belum memiliki contoh? Gunakan [Generator Kasus Uji](/docs/id/test-and-evaluate/eval-tool#creating-test-cases) untuk:
1. Menghasilkan contoh input
2. Mendapatkan respons Claude
3. Mengedit respons agar sesuai dengan output ideal Anda
4. Menambahkan contoh yang telah disempurnakan ke prompt Anda

### Kapan menggunakan penyempurna prompt

Penyempurna prompt paling cocok untuk:
- Tugas kompleks yang memerlukan penalaran terperinci
- Situasi di mana akurasi lebih penting daripada kecepatan
- Masalah di mana output Claude saat ini memerlukan peningkatan signifikan

<Note>
Untuk aplikasi yang sensitif terhadap latensi atau biaya, pertimbangkan untuk menggunakan prompt yang lebih sederhana. Penyempurna prompt membuat template yang menghasilkan respons yang lebih panjang, lebih menyeluruh, tetapi lebih lambat.
</Note>

### Contoh peningkatan

Berikut cara penyempurna prompt meningkatkan prompt klasifikasi dasar:

<section title="Prompt asli">

```text
From the following list of Wikipedia article titles, identify which article this sentence came from.
Respond with just the article title and nothing else.

Article titles:
{{titles}}

Sentence to classify:
{{sentence}}
```

</section>

<section title="Prompt yang disempurnakan">

```text
You are an intelligent text classification system specialized in matching sentences to Wikipedia article titles. Your task is to identify which Wikipedia article a given sentence most likely belongs to, based on a provided list of article titles.

First, review the following list of Wikipedia article titles:
<article_titles>
{{titles}}
</article_titles>

Now, consider this sentence that needs to be classified:
<sentence_to_classify>
{{sentence}}
</sentence_to_classify>

Your goal is to determine which article title from the provided list best matches the given sentence. Follow these steps:

1. List the key concepts from the sentence
2. Compare each key concept with the article titles
3. Rank the top 3 most relevant titles and explain why they are relevant
4. Select the most appropriate article title that best encompasses or relates to the sentence's content

Wrap your analysis in <analysis> tags. Include the following:
- List of key concepts from the sentence
- Comparison of each key concept with the article titles
- Ranking of top 3 most relevant titles with explanations
- Your final choice and reasoning

After your analysis, provide your final answer: the single most appropriate Wikipedia article title from the list.

Output only the chosen article title, without any additional text or explanation.
```

</section>

Perhatikan bagaimana prompt yang disempurnakan:
- Menambahkan instruksi penalaran langkah demi langkah yang jelas
- Menggunakan tag XML untuk mengorganisir konten
- Memberikan persyaratan pemformatan output yang eksplisit
- Memandu Claude melalui proses analisis

### Pemecahan masalah

Masalah umum dan solusinya:

- **Contoh tidak muncul dalam output**: Periksa bahwa contoh diformat dengan benar menggunakan tag XML dan muncul di awal pesan pengguna pertama
- **Chain of thought terlalu bertele-tele**: Tambahkan instruksi spesifik tentang panjang output dan tingkat detail yang diinginkan
- **Langkah penalaran tidak sesuai dengan kebutuhan Anda**: Modifikasi bagian langkah agar sesuai dengan kasus penggunaan spesifik Anda

***

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mulai rekayasa prompt" icon="link" href="/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices">
    Pelajari teknik inti dengan contoh yang dikerjakan.
  </Card>
  <Card title="Uji prompt Anda" icon="link" href="/docs/id/test-and-evaluate/eval-tool">
    Gunakan alat evaluasi untuk menguji prompt yang telah disempurnakan.
  </Card>
  <Card title="Tutorial prompting GitHub" icon="link" href="https://github.com/anthropics/prompt-eng-interactive-tutorial">
    Tutorial yang penuh contoh yang mencakup konsep rekayasa prompt yang ditemukan dalam dokumentasi kami.
  </Card>
</CardGroup>