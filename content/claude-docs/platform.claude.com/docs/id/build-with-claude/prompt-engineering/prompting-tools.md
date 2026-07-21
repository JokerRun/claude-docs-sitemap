---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-tools
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: d92fc8887ea695176f5f822f05fb0a896a576c745089cc2c83960a2560453fab
---

# Alat prompting di Console

---

Claude Console menawarkan serangkaian alat untuk membantu Anda membangun dan menyempurnakan prompt. Halaman ini memandu Anda melalui alat-alat tersebut sesuai urutan yang biasanya Anda gunakan: menghasilkan draf pertama, menambahkan template dan variabel, lalu meningkatkan prompt yang sudah ada.

***

## Prompt generator

<Note>
  Prompt generator kompatibel dengan semua model Claude, termasuk model dengan kemampuan "extended thinking" (pemikiran diperpanjang). Untuk tips prompting khusus model pemikiran diperpanjang, lihat [tips prompting pemikiran diperpanjang](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities).
</Note>

Terkadang, bagian tersulit dalam menggunakan model AI adalah mencari tahu cara membuat prompt yang efektif. Prompt generator memandu Claude untuk membuat template prompt berkualitas tinggi yang disesuaikan dengan tugas spesifik Anda, dengan mengikuti banyak praktik terbaik rekayasa prompt kami.

Prompt generator sangat berguna untuk mengatasi "masalah halaman kosong"—alat ini memberi Anda titik awal untuk pengujian dan iterasi lebih lanjut.

<Tip>
  Coba prompt generator sekarang langsung di 

  [Console](/dashboard)

  .
</Tip>

Jika Anda tertarik untuk menganalisis prompt dan arsitektur yang mendasarinya, lihat [notebook Google Colab prompt generator](https://anthropic.com/metaprompt-notebook/) kami. Untuk menjalankan notebook Colab tersebut, Anda memerlukan [kunci API](/settings/keys).

***

## Template dan variabel prompt

Saat men-deploy aplikasi berbasis LLM dengan Claude, panggilan API Anda biasanya akan terdiri dari dua jenis konten:

* **Konten tetap:** Instruksi atau konteks statis yang tetap konstan di berbagai interaksi

* **Konten variabel:** Elemen dinamis yang berubah pada setiap permintaan atau percakapan, seperti:

  * Input pengguna
  * Konten yang diambil untuk "Retrieval-Augmented Generation" (generasi yang diperkaya pengambilan), atau RAG
  * Konteks percakapan seperti riwayat akun pengguna
  * Data yang dihasilkan sistem seperti hasil penggunaan alat yang dimasukkan dari panggilan independen lain ke Claude

Sebuah **template prompt** menggabungkan bagian tetap dan variabel ini, menggunakan placeholder untuk konten dinamis. Di [Claude Console](/), placeholder ini ditandai dengan **\{\{kurung kurawal ganda}}**, sehingga mudah diidentifikasi dan memungkinkan pengujian cepat terhadap nilai yang berbeda.

Anda sebaiknya menggunakan template dan variabel prompt ketika Anda memperkirakan bagian mana pun dari prompt Anda akan diulang dalam panggilan lain ke Claude (melalui API atau [Claude Console](/). [claude.ai](https://claude.ai/) saat ini tidak mendukung template atau variabel prompt).

Template prompt menawarkan beberapa manfaat:

* **Konsistensi:** Memastikan struktur yang konsisten untuk prompt Anda di berbagai interaksi
* **Efisiensi:** Dengan mudah menukar konten variabel tanpa menulis ulang seluruh prompt
* **Kemudahan pengujian:** Dengan cepat menguji berbagai input dan kasus tepi dengan hanya mengubah bagian variabel
* **Skalabilitas:** Menyederhanakan pengelolaan prompt seiring bertambahnya kompleksitas aplikasi Anda
* **Kontrol versi:** Dengan mudah melacak perubahan pada struktur prompt Anda dari waktu ke waktu dengan hanya memantau bagian inti prompt Anda, terpisah dari input dinamis

Console menggunakan template dan variabel prompt untuk mendukung alat-alatnya:

* **Prompt generator:** Menentukan variabel apa yang dibutuhkan prompt Anda dan menyertakannya dalam template yang dihasilkannya
* **Prompt improver:** Mengambil template Anda yang sudah ada, termasuk semua variabel, dan mempertahankannya dalam template yang telah ditingkatkan yang dihasilkannya
* **[Alat evaluasi](/docs/id/test-and-evaluate/eval-tool):** Memungkinkan Anda dengan mudah menguji, menskalakan, dan melacak versi prompt Anda dengan memisahkan bagian variabel dan tetap dari template prompt Anda

### Contoh template prompt

Pertimbangkan aplikasi sederhana yang menerjemahkan teks bahasa Inggris ke bahasa Spanyol. Teks yang diterjemahkan akan menjadi variabel karena berubah antar pengguna atau panggilan ke Claude. Anda mungkin menggunakan template prompt ini:

```text wrap
Translate this text from English to Spanish: {{text}}
```

<Tip>
  Untuk meningkatkan variabel prompt Anda, bungkus variabel tersebut dalam 

  [tag XML](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#structure-prompts-with-xml-tags)

   untuk struktur yang lebih jelas.
</Tip>

***

## Prompt improver

<Note>
  Prompt improver kompatibel dengan semua model Claude, termasuk model dengan kemampuan pemikiran diperpanjang. Untuk tips prompting khusus model pemikiran diperpanjang, lihat [tips prompting pemikiran diperpanjang](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities).
</Note>

Prompt improver membantu Anda dengan cepat melakukan iterasi dan meningkatkan prompt Anda melalui analisis dan penyempurnaan otomatis. Alat ini unggul dalam membuat prompt lebih tangguh untuk tugas kompleks yang memerlukan akurasi tinggi.

<Frame>
  ![](/docs/images/prompt_improver.png)
</Frame>

### Sebelum Anda mulai

Anda memerlukan:

* Template prompt (lihat [Template dan variabel prompt](#prompt-templates-and-variables) di atas)
* Umpan balik tentang masalah saat ini dengan output Claude (opsional tetapi direkomendasikan)
* Contoh input dan output ideal (opsional tetapi direkomendasikan)

### Cara kerja prompt improver

Prompt improver menyempurnakan prompt Anda dalam 4 langkah:

1. **Identifikasi contoh**: Menemukan dan mengekstrak contoh dari template prompt Anda
2. **Draf awal**: Membuat template terstruktur dengan bagian yang jelas dan tag XML
3. **Penyempurnaan chain of thought**: Menambahkan dan menyempurnakan instruksi penalaran yang terperinci
4. **Penyempurnaan contoh**: Memperbarui contoh untuk mendemonstrasikan proses penalaran yang baru

Anda dapat menyaksikan langkah-langkah ini terjadi secara real-time di modal penyempurnaan.

### Apa yang Anda dapatkan

Prompt improver menghasilkan template dengan:

* Instruksi "chain-of-thought" (rantai pemikiran) terperinci yang memandu proses penalaran Claude dan biasanya meningkatkan kinerjanya
* Pengorganisasian yang jelas menggunakan tag XML untuk memisahkan komponen yang berbeda
* Format contoh yang terstandarisasi yang mendemonstrasikan penalaran langkah demi langkah dari input ke output
* Prefill strategis yang memandu respons awal Claude

<Note>
  Meskipun contoh muncul secara terpisah di UI Workbench, contoh tersebut disertakan di awal pesan pengguna pertama dalam panggilan API yang sebenarnya. Lihat format mentahnya dengan mengklik "**\</> Get Code**" atau masukkan contoh sebagai teks mentah melalui kotak Examples.
</Note>

### Cara menggunakan prompt improver

1. Kirimkan template prompt Anda
2. Tambahkan umpan balik apa pun tentang masalah dengan output Claude saat ini (misalnya, "ringkasan terlalu dasar untuk audiens ahli")
3. Sertakan contoh input dan output ideal
4. Tinjau prompt yang telah ditingkatkan

### Menghasilkan contoh pengujian

Belum memiliki contoh? Gunakan [Test Case Generator](/docs/id/test-and-evaluate/eval-tool#creating-test-cases) untuk:

1. Menghasilkan input sampel
2. Mendapatkan respons Claude
3. Mengedit respons agar sesuai dengan output ideal Anda
4. Menambahkan contoh yang telah disempurnakan ke prompt Anda

### Kapan menggunakan prompt improver

Prompt improver bekerja paling baik untuk:

* Tugas kompleks yang memerlukan penalaran terperinci
* Situasi di mana akurasi lebih penting daripada kecepatan
* Masalah di mana output Claude saat ini memerlukan peningkatan yang signifikan

<Note>
  Untuk aplikasi yang sensitif terhadap "latency" (latensi) atau biaya, pertimbangkan untuk menggunakan prompt yang lebih sederhana. Prompt improver membuat template yang menghasilkan respons yang lebih panjang, lebih menyeluruh, tetapi lebih lambat.
</Note>

### Contoh peningkatan

Berikut adalah cara prompt improver menyempurnakan prompt klasifikasi dasar:

<Accordion title="Prompt asli">
  ```text wrap
  From the following list of Wikipedia article titles, identify which article this sentence came from.
  Respond with just the article title and nothing else.

  Article titles:
  {{titles}}

  Sentence to classify:
  {{sentence}}
  ```
</Accordion>

<Accordion title="Prompt yang ditingkatkan">
  ```text wrap
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
</Accordion>

Perhatikan bagaimana prompt yang ditingkatkan:

* Menambahkan instruksi penalaran langkah demi langkah yang jelas
* Menggunakan tag XML untuk mengorganisasi konten
* Menyediakan persyaratan format output yang eksplisit
* Memandu Claude melalui proses analisis

### Pemecahan masalah

Masalah umum dan solusinya:

* **Contoh tidak muncul di output**: Periksa apakah contoh diformat dengan benar menggunakan tag XML dan muncul di awal pesan pengguna pertama
* **Chain of thought terlalu panjang**: Tambahkan instruksi spesifik tentang panjang output dan tingkat detail yang diinginkan
* **Langkah penalaran tidak sesuai dengan kebutuhan Anda**: Modifikasi bagian langkah agar sesuai dengan kasus penggunaan spesifik Anda

***

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mulai rekayasa prompt" icon="link" href="/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices">
    Pelajari teknik inti dengan contoh yang dikerjakan.
  </Card>

  <Card title="Uji prompt Anda" icon="link" href="/docs/id/test-and-evaluate/eval-tool">
    Gunakan alat evaluasi untuk menguji prompt Anda yang telah ditingkatkan.
  </Card>

  <Card title="Tutorial prompting GitHub" icon="link" href="https://github.com/anthropics/prompt-eng-interactive-tutorial">
    Tutorial yang penuh dengan contoh yang mencakup konsep rekayasa prompt yang terdapat dalam dokumentasi kami.
  </Card>
</CardGroup>
