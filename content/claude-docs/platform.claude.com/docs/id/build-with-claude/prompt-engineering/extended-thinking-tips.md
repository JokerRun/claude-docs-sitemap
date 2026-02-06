---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/extended-thinking-tips
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: c6fb2e80fc53dbef633d9fcf0156b11e0356d7f347975b45956e452935b722e7
---

# Tips extended thinking

Strategi lanjutan dan teknik untuk memaksimalkan fitur extended thinking Claude

---

Panduan ini menyediakan strategi lanjutan dan teknik untuk memaksimalkan fitur extended thinking Claude. Extended thinking memungkinkan Claude untuk menyelesaikan masalah kompleks secara bertahap, meningkatkan kinerja pada tugas-tugas yang sulit.

Lihat [Extended thinking](/docs/id/build-with-claude/extended-thinking) untuk panduan tentang memutuskan kapan menggunakan extended thinking.

## Sebelum memulai

Panduan ini mengasumsikan bahwa Anda telah memutuskan untuk menggunakan mode extended thinking dan telah meninjau [panduan implementasi extended thinking](/docs/id/build-with-claude/extended-thinking) kami.

### Pertimbangan teknis untuk extended thinking

- Thinking tokens memiliki anggaran minimum 1024 token. Kami merekomendasikan bahwa Anda mulai dengan anggaran thinking minimum dan secara bertahap tingkatkan untuk menyesuaikan berdasarkan kebutuhan dan kompleksitas tugas Anda.
- Untuk beban kerja di mana anggaran thinking optimal berada di atas 32K, kami merekomendasikan bahwa Anda menggunakan [batch processing](/docs/id/build-with-claude/batch-processing) untuk menghindari masalah jaringan. Permintaan yang mendorong model untuk berpikir di atas 32K token menyebabkan permintaan yang berjalan lama yang mungkin menghadapi batas waktu sistem dan batas koneksi terbuka.
- Extended thinking berkinerja terbaik dalam bahasa Inggris, meskipun output akhir dapat dalam [bahasa apa pun yang Claude dukung](/docs/id/build-with-claude/multilingual-support).
- Jika Anda memerlukan thinking di bawah anggaran minimum, kami merekomendasikan menggunakan mode standar, dengan thinking dimatikan, dengan prompting chain-of-thought tradisional dengan tag XML (seperti `<thinking>`). Lihat [chain of thought prompting](/docs/id/build-with-claude/prompt-engineering/chain-of-thought).

## Teknik prompting untuk extended thinking

### Gunakan instruksi umum terlebih dahulu, kemudian troubleshoot dengan instruksi yang lebih step-by-step

Claude sering berkinerja lebih baik dengan instruksi tingkat tinggi untuk hanya berpikir mendalam tentang tugas daripada panduan preskriptif step-by-step. Kreativitas model dalam mendekati masalah mungkin melebihi kemampuan manusia untuk meresepkan proses thinking yang optimal.

Misalnya, alih-alih:

<CodeGroup>
```text User
Pikirkan masalah matematika ini langkah demi langkah:
1. Pertama, identifikasi variabelnya
2. Kemudian, atur persamaannya
3. Selanjutnya, selesaikan untuk x
...
```
</CodeGroup>

Pertimbangkan:

<CodeGroup>
```text User
Silakan pikirkan masalah matematika ini secara menyeluruh dan sangat detail.
Pertimbangkan berbagai pendekatan dan tunjukkan penalaran lengkap Anda.
Coba metode berbeda jika pendekatan pertama Anda tidak berhasil.
```
/>
</CodeGroup>

<TryInConsoleButton
  userPrompt={
    `Silakan pikirkan masalah matematika ini secara menyeluruh dan sangat detail.
Pertimbangkan berbagai pendekatan dan tunjukkan penalaran lengkap Anda.
Coba metode berbeda jika pendekatan pertama Anda tidak berhasil.`
  }
  thinkingBudgetTokens={16000}
>
  Coba di Konsol
</TryInConsoleButton>

Meskipun demikian, Claude masih dapat secara efektif mengikuti langkah-langkah eksekusi terstruktur yang kompleks ketika diperlukan. Model dapat menangani bahkan daftar yang lebih panjang dengan instruksi yang lebih kompleks daripada versi sebelumnya. Kami merekomendasikan bahwa Anda mulai dengan instruksi yang lebih umum, kemudian baca output thinking Claude dan ulangi untuk memberikan instruksi yang lebih spesifik untuk mengarahkan thinkingnya dari sana.

### Multishot prompting dengan extended thinking

[Multishot prompting](/docs/id/build-with-claude/prompt-engineering/multishot-prompting) bekerja dengan baik dengan extended thinking. Ketika Anda memberikan Claude contoh tentang cara berpikir melalui masalah, Claude akan mengikuti pola penalaran serupa dalam blok extended thinking-nya.

Anda dapat menyertakan contoh few-shot dalam prompt Anda dalam skenario extended thinking dengan menggunakan tag XML seperti `<thinking>` atau `<scratchpad>` untuk menunjukkan pola extended thinking kanonik dalam contoh-contoh tersebut.

Claude akan menggeneralisasi pola ke proses extended thinking formal. Namun, ada kemungkinan Anda akan mendapatkan hasil yang lebih baik dengan memberikan Claude kebebasan untuk berpikir dengan cara yang dianggapnya terbaik.

Contoh:

<CodeGroup>
```text User
Saya akan menunjukkan kepada Anda cara menyelesaikan masalah matematika, kemudian saya ingin Anda menyelesaikan masalah yang serupa.

Masalah 1: Berapa 15% dari 80?

<thinking>
Untuk menemukan 15% dari 80:
1. Konversi 15% ke desimal: 15% = 0,15
2. Kalikan: 0,15 × 80 = 12
</thinking>

Jawabannya adalah 12.

Sekarang selesaikan yang ini:
Masalah 2: Berapa 35% dari 240?
```
/>
</CodeGroup>

<TryInConsoleButton
  userPrompt={
    `Saya akan menunjukkan kepada Anda cara menyelesaikan masalah matematika, kemudian saya ingin Anda menyelesaikan masalah yang serupa.

Masalah 1: Berapa 15% dari 80?

<thinking>
Untuk menemukan 15% dari 80:
1. Konversi 15% ke desimal: 15% = 0,15
2. Kalikan: 0,15 × 80 = 12
</thinking>

Jawabannya adalah 12.

Sekarang selesaikan yang ini:
Masalah 2: Berapa 35% dari 240?`
  }
  thinkingBudgetTokens={16000} 
>
  Coba di Konsol
</TryInConsoleButton>

### Memaksimalkan instruction following dengan extended thinking

Claude menunjukkan instruction following yang secara signifikan lebih baik ketika extended thinking diaktifkan. Model biasanya:
1. Bernalar tentang instruksi di dalam blok extended thinking
2. Melaksanakan instruksi tersebut dalam respons

Untuk memaksimalkan instruction following:
- Jadilah jelas dan spesifik tentang apa yang Anda inginkan
- Untuk instruksi kompleks, pertimbangkan untuk memecahnya menjadi langkah-langkah bernomor yang harus dikerjakan Claude secara metodis
- Berikan Claude anggaran yang cukup untuk memproses instruksi sepenuhnya dalam extended thinking-nya

### Menggunakan extended thinking untuk debug dan mengarahkan perilaku Claude

Anda dapat menggunakan output thinking Claude untuk men-debug logika Claude, meskipun metode ini tidak selalu sempurna dapat diandalkan.

Untuk memanfaatkan metodologi ini dengan sebaik-baiknya, kami merekomendasikan tips berikut:
- Kami tidak merekomendasikan melewatkan extended thinking Claude kembali di blok teks pengguna, karena ini tidak meningkatkan kinerja dan mungkin benar-benar menurunkan hasil.
- Prefilling extended thinking secara eksplisit tidak diizinkan, dan secara manual mengubah teks output model yang mengikuti blok thinkingnya kemungkinan akan menurunkan hasil karena kebingungan model.

Ketika extended thinking dimatikan, prefill teks respons `assistant` standar masih diizinkan.

<Note>
Kadang-kadang Claude mungkin mengulangi extended thinking-nya dalam teks output assistant. Jika Anda menginginkan respons yang bersih, instruksikan Claude untuk tidak mengulangi extended thinking-nya dan hanya mengeluarkan jawabannya.
</Note>

### Memanfaatkan output panjang dan longform thinking dengan sebaik-baiknya

Untuk use case generasi dataset, coba prompt seperti "Silakan buat tabel yang sangat detail dari..." untuk menghasilkan dataset komprehensif.

Untuk use case seperti generasi konten detail di mana Anda mungkin ingin menghasilkan blok extended thinking yang lebih panjang dan respons yang lebih detail, coba tips ini:
- Tingkatkan panjang extended thinking maksimum DAN secara eksplisit minta output yang lebih panjang
- Untuk output yang sangat panjang (20.000+ kata), minta outline detail dengan jumlah kata hingga tingkat paragraf. Kemudian minta Claude untuk mengindeks paragrafnya ke outline dan mempertahankan jumlah kata yang ditentukan

<Warning>
Kami tidak merekomendasikan bahwa Anda mendorong Claude untuk mengeluarkan lebih banyak token demi mengeluarkan token. Sebaliknya, kami mendorong Anda untuk memulai dengan anggaran thinking kecil dan meningkat sesuai kebutuhan untuk menemukan pengaturan optimal untuk use case Anda.
</Warning>

Berikut adalah contoh use case di mana Claude unggul karena extended thinking yang lebih panjang:

  <section title="Masalah STEM kompleks">

    Masalah STEM kompleks memerlukan Claude untuk membangun model mental, menerapkan pengetahuan khusus, dan menyelesaikan langkah-langkah logis berurutan—proses yang mendapat manfaat dari waktu penalaran yang lebih lama.
    
    <Tabs>
      <Tab title="Prompt standar">
        <CodeGroup>
        ```text User
        Tulis skrip python untuk bola kuning yang memantul dalam persegi,
pastikan untuk menangani deteksi tabrakan dengan benar.
Buat persegi berputar perlahan.
        ```
        />
        </CodeGroup>
        
        <TryInConsoleButton
          userPrompt={
            `Tulis skrip python untuk bola kuning yang memantul dalam persegi,
pastikan untuk menangani deteksi tabrakan dengan benar.
Buat persegi berputar perlahan.`
          }
          thinkingBudgetTokens={16000}
        >
          Coba di Konsol
        </TryInConsoleButton>
        <Note>
        Tugas yang lebih sederhana ini biasanya menghasilkan hanya beberapa detik waktu thinking.
        </Note>
      </Tab>
      <Tab title="Prompt yang ditingkatkan">
        <CodeGroup>
        ```text User
        Tulis skrip Python untuk bola kuning yang memantul dalam tesseract,
pastikan untuk menangani deteksi tabrakan dengan benar.
Buat tesseract berputar perlahan.
Pastikan bola tetap berada dalam tesseract.
        ```
        />
        </CodeGroup>
        
        <TryInConsoleButton
          userPrompt={
            `Tulis skrip Python untuk bola kuning yang memantul dalam tesseract,
pastikan untuk menangani deteksi tabrakan dengan benar.
Buat tesseract berputar perlahan.
Pastikan bola tetap berada dalam tesseract.`
          }
          thinkingBudgetTokens={16000}
        >
          Coba di Konsol
        </TryInConsoleButton>
        <Note>
        Tantangan visualisasi 4D yang kompleks ini memanfaatkan waktu extended thinking yang panjang dengan sebaik-baiknya karena Claude menyelesaikan kompleksitas matematika dan pemrograman.
        </Note>
      </Tab>
    </Tabs>
  
</section>
  
  <section title="Masalah optimasi kendala">

    Tantangan optimasi kendala menantang Claude untuk memenuhi beberapa persyaratan yang bersaing secara bersamaan, yang paling baik dicapai ketika memungkinkan waktu extended thinking yang panjang sehingga model dapat secara metodis mengatasi setiap kendala.
    
    <Tabs>
      <Tab title="Prompt standar">
        <CodeGroup>
        ```text User
        Rencanakan liburan seminggu ke Jepang.
        ```
        />
        </CodeGroup>
        
        <TryInConsoleButton
          userPrompt="Rencanakan liburan seminggu ke Jepang."
          thinkingBudgetTokens={16000}
        >
          Coba di Konsol
        </TryInConsoleButton>
        <Note>
        Permintaan open-ended ini biasanya menghasilkan hanya beberapa detik waktu thinking.
        </Note>
      </Tab>
      <Tab title="Prompt yang ditingkatkan">
        <CodeGroup>
        ```text User
        Rencanakan perjalanan 7 hari ke Jepang dengan kendala berikut:
- Anggaran $2.500
- Harus mencakup Tokyo dan Kyoto
- Perlu mengakomodasi diet vegetarian
- Preferensi untuk pengalaman budaya daripada belanja
- Harus mencakup satu hari hiking
- Tidak lebih dari 2 jam perjalanan antara lokasi per hari
- Perlu waktu luang setiap sore untuk panggilan kembali ke rumah
- Harus menghindari keramaian jika memungkinkan
        ```
        />
        </CodeGroup>
        
        <TryInConsoleButton
          userPrompt={
            `Rencanakan perjalanan 7 hari ke Jepang dengan kendala berikut:
- Anggaran $2.500
- Harus mencakup Tokyo dan Kyoto
- Perlu mengakomodasi diet vegetarian
- Preferensi untuk pengalaman budaya daripada belanja
- Harus mencakup satu hari hiking
- Tidak lebih dari 2 jam perjalanan antara lokasi per hari
- Perlu waktu luang setiap sore untuk panggilan kembali ke rumah
- Harus menghindari keramaian jika memungkinkan`
          }
          thinkingBudgetTokens={16000}
        >
          Coba di Konsol
        </TryInConsoleButton>
        <Note>
        Dengan beberapa kendala untuk diseimbangkan, Claude akan secara alami berkinerja terbaik ketika diberikan lebih banyak ruang untuk berpikir tentang cara memenuhi semua persyaratan secara optimal.
        </Note>
      </Tab>
    </Tabs>
  
</section>
  
  <section title="Kerangka kerja thinking">

    Kerangka kerja thinking terstruktur memberikan Claude metodologi eksplisit untuk diikuti, yang mungkin bekerja terbaik ketika Claude diberikan ruang extended thinking yang panjang untuk mengikuti setiap langkah.
    
    <Tabs>
      <Tab title="Prompt standar">
        <CodeGroup>
        ```text User
        Kembangkan strategi komprehensif untuk Microsoft
memasuki pasar personalized medicine pada tahun 2027.
        ```
        />
        </CodeGroup>
        
        <TryInConsoleButton
          userPrompt={
            `Kembangkan strategi komprehensif untuk Microsoft
memasuki pasar personalized medicine pada tahun 2027.`
          }
          thinkingBudgetTokens={16000}
        >
          Coba di Konsol
        </TryInConsoleButton>
        <Note>
        Pertanyaan strategis yang luas ini biasanya menghasilkan hanya beberapa detik waktu thinking.
        </Note>
      </Tab>
      <Tab title="Prompt yang ditingkatkan">
        <CodeGroup>
        ```text User
        Kembangkan strategi komprehensif untuk Microsoft memasuki
pasar personalized medicine pada tahun 2027.

Mulai dengan:
1. Kanvas Blue Ocean Strategy
2. Terapkan Porter's Five Forces untuk mengidentifikasi tekanan kompetitif

Selanjutnya, lakukan latihan scenario planning dengan empat
masa depan yang berbeda berdasarkan variabel regulasi dan teknologi.

Untuk setiap skenario:
- Kembangkan respons strategis menggunakan Ansoff Matrix

Terakhir, terapkan kerangka kerja Three Horizons untuk:
- Memetakan jalur transisi
- Mengidentifikasi inovasi disruptif potensial di setiap tahap
        ```
        />
        </CodeGroup>
        
        <TryInConsoleButton
          userPrompt={
            `Kembangkan strategi komprehensif untuk Microsoft memasuki
pasar personalized medicine pada tahun 2027.

Mulai dengan:
1. Kanvas Blue Ocean Strategy
2. Terapkan Porter's Five Forces untuk mengidentifikasi tekanan kompetitif

Selanjutnya, lakukan latihan scenario planning dengan empat
masa depan yang berbeda berdasarkan variabel regulasi dan teknologi.

Untuk setiap skenario:
- Kembangkan respons strategis menggunakan Ansoff Matrix

Terakhir, terapkan kerangka kerja Three Horizons untuk:
- Memetakan jalur transisi
- Mengidentifikasi inovasi disruptif potensial di setiap tahap`
          }
          thinkingBudgetTokens={16000}
        >
          Coba di Konsol
        </TryInConsoleButton>
        <Note>
        Dengan menentukan beberapa kerangka kerja analitik yang harus diterapkan secara berurutan, waktu thinking secara alami meningkat karena Claude menyelesaikan setiap kerangka kerja secara metodis.
        </Note>
      </Tab>
    </Tabs>
  
</section>

### Biarkan Claude merenungkan dan memeriksa pekerjaannya untuk konsistensi dan penanganan kesalahan yang lebih baik

Anda dapat menggunakan prompting bahasa alami sederhana untuk meningkatkan konsistensi dan mengurangi kesalahan:
1. Minta Claude untuk memverifikasi pekerjaannya dengan tes sederhana sebelum mendeklarasikan tugas selesai
2. Instruksikan model untuk menganalisis apakah langkah sebelumnya mencapai hasil yang diharapkan
3. Untuk tugas coding, minta Claude untuk menjalankan test case dalam extended thinking-nya

Contoh:

<CodeGroup>
```text User
Tulis fungsi untuk menghitung faktorial dari angka.
Sebelum Anda selesai, silakan verifikasi solusi Anda dengan test case untuk:
- n=0
- n=1
- n=5
- n=10
Dan perbaiki masalah apa pun yang Anda temukan.
```
/>
</CodeGroup>

<TryInConsoleButton
  userPrompt={
    `Tulis fungsi untuk menghitung faktorial dari angka.
Sebelum Anda selesai, silakan verifikasi solusi Anda dengan test case untuk:
- n=0
- n=1
- n=5
- n=10
Dan perbaiki masalah apa pun yang Anda temukan.`
  }
  thinkingBudgetTokens={16000}
>
  Coba di Konsol
</TryInConsoleButton>

## Langkah berikutnya

<CardGroup>
  <Card title="Extended thinking cookbook" icon="book" href="https://platform.claude.com/cookbook/extended-thinking-extended-thinking">
    Jelajahi contoh praktis extended thinking dalam cookbook kami.
  </Card>
  <Card title="Panduan extended thinking" icon="code" href="/docs/id/build-with-claude/extended-thinking">
    Lihat dokumentasi teknis lengkap untuk mengimplementasikan extended thinking.
  </Card>
</CardGroup>