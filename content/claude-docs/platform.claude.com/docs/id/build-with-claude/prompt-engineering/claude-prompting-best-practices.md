---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 45e22d483cee0dad3270634b998ebe2fc3f3d0c024404129e72e867cf9e45c54
---

# Praktik terbaik prompting

Panduan komprehensif teknik prompt engineering untuk model terbaru Claude, mencakup kejelasan, contoh, strukturisasi XML, thinking, dan sistem agentic.

---

Ini adalah referensi tunggal untuk prompt engineering dengan model terbaru Claude, termasuk Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, dan Claude Haiku 4.5. Ini mencakup teknik dasar, kontrol output, penggunaan tool, thinking, dan sistem agentic. Lompat ke bagian yang sesuai dengan situasi Anda.

<Tip>
  Untuk gambaran umum kemampuan model, lihat [ikhtisar model](/docs/id/about-claude/models/overview). Untuk detail tentang apa yang baru di Claude Opus 4.7, lihat [Apa yang baru di Claude Opus 4.7](/docs/id/about-claude/models/whats-new-claude-4-7). Untuk panduan migrasi, lihat [Panduan migrasi](/docs/id/about-claude/models/migration-guide).
</Tip>

## Prompting Claude Opus 4.7

Claude Opus 4.7 adalah model yang paling mampu dan tersedia secara umum, dengan kekuatan khusus dalam pekerjaan agentic jangka panjang, pekerjaan pengetahuan, visi, dan tugas memori. Ini berkinerja baik langsung dari kotak pada prompt Claude Opus 4.6 yang ada. Pola di bawah mencakup perilaku yang paling sering memerlukan penyesuaian.

<Note>
Untuk perubahan parameter API saat bermigrasi dari Claude Opus 4.6 (tingkat upaya, anggaran tugas, konfigurasi thinking, penghapusan parameter sampling, dan tokenisasi), lihat [panduan migrasi](/docs/id/about-claude/models/migration-guide#migrating-to-claude-opus-4-7).
</Note>

### Panjang respons dan verbositas

Claude Opus 4.7 mengkalibrasi panjang respons berdasarkan seberapa kompleks tugas yang dianggapnya, bukan dengan default ke verbositas tetap. Ini biasanya berarti jawaban yang lebih pendek pada pencarian sederhana dan jawaban yang jauh lebih panjang pada analisis terbuka.

Jika produk Anda bergantung pada gaya atau verbositas output tertentu, Anda mungkin perlu menyesuaikan prompt Anda. Sebagai contoh, untuk mengurangi verbositas, Anda dapat menambahkan:

```text
Berikan respons yang ringkas dan terfokus. Lewati konteks yang tidak penting, dan jaga contoh tetap minimal.
```

Jika Anda melihat contoh spesifik jenis verbositas (yaitu penjelasan berlebihan), Anda dapat menambahkan instruksi tambahan dalam prompt Anda untuk mencegahnya. Contoh positif yang menunjukkan bagaimana Claude dapat berkomunikasi dengan tingkat keringkasan yang tepat cenderung lebih efektif daripada contoh negatif atau instruksi yang memberi tahu model apa yang tidak boleh dilakukan.

### Mengkalibrasi upaya dan kedalaman thinking

[Parameter upaya](/docs/id/build-with-claude/effort) memungkinkan Anda menyesuaikan kecerdasan Claude versus pengeluaran token, menukar kemampuan untuk kecepatan lebih cepat dan biaya lebih rendah. Mulai dengan tingkat upaya `xhigh` baru untuk kasus penggunaan coding dan agentic, dan gunakan minimum upaya `high` untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan. Bereksperimen dengan tingkat upaya lain untuk lebih menyesuaikan penggunaan token dan kecerdasan:

- **`max`:** Upaya maksimal dapat memberikan peningkatan kinerja dalam beberapa kasus penggunaan, tetapi mungkin menunjukkan hasil yang semakin berkurang dari peningkatan penggunaan token. Pengaturan ini juga kadang-kadang dapat rentan terhadap overthinking. Kami merekomendasikan pengujian upaya maksimal untuk tugas yang menuntut kecerdasan.
- **`xhigh` (baru):** Upaya ekstra tinggi adalah pengaturan terbaik untuk sebagian besar kasus penggunaan coding dan agentic.
- **`high`:** Pengaturan ini menyeimbangkan penggunaan token dan kecerdasan. Untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan, kami merekomendasikan minimum upaya `high`.
- **`medium`:** Baik untuk kasus penggunaan yang sensitif terhadap biaya yang perlu mengurangi penggunaan token sambil menukar kecerdasan.
- **`low`:** Cadangkan untuk tugas pendek dan terbatas serta beban kerja yang sensitif terhadap latensi yang tidak sensitif terhadap kecerdasan.

Berubah secara bermakna dari Claude Opus 4.6, Claude Opus 4.7 menghormati tingkat upaya dengan ketat, terutama di ujung bawah. Pada `low` dan `medium`, model membatasi pekerjaannya pada apa yang diminta daripada melampaui. Ini bagus untuk latensi dan biaya, tetapi pada tugas yang cukup kompleks yang berjalan pada upaya `low` ada beberapa risiko under-thinking.

Jika Anda mengamati penalaran dangkal pada masalah kompleks, naikkan upaya ke `high` atau `xhigh` daripada meminta di sekitarnya. Jika Anda perlu menjaga upaya pada `low` untuk latensi, tambahkan panduan yang ditargetkan:

```text
Tugas ini melibatkan penalaran multi-langkah. Pikirkan dengan hati-hati melalui masalah sebelum merespons.
```

Kami mengharapkan upaya menjadi lebih penting untuk model ini daripada untuk Opus sebelumnya, dan merekomendasikan bereksperimen dengannya secara aktif saat Anda upgrade.

Perilaku pemicu untuk adaptive thinking dapat diarahkan. Jika Anda menemukan model berpikir lebih sering daripada yang Anda inginkan — yang dapat terjadi dengan prompt sistem yang besar atau kompleks — tambahkan panduan untuk mengarahkannya. Seperti biasa, ukur efek dari perubahan prompting apa pun pada kinerja. Contoh:

```text
Thinking menambah latensi dan hanya boleh digunakan ketika akan secara bermakna meningkatkan kualitas jawaban — biasanya untuk masalah yang memerlukan penalaran multi-langkah. Jika ragu, respons langsung.
```

Sebaliknya, jika Anda menjalankan beban kerja keras pada `medium` dan melihat under-thinking, lever pertama adalah menaikkan upaya. Jika Anda memerlukan kontrol yang lebih halus, minta secara langsung.

<Note>
Jika Anda menjalankan Claude Opus 4.7 pada upaya `max` atau `xhigh`, atur anggaran token output maksimal yang besar sehingga model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan panggilan tool-nya. Kami merekomendasikan memulai dengan 64k token dan menyesuaikan dari sana.
</Note>

### Pemicu penggunaan tool

Claude Opus 4.7 memiliki kecenderungan untuk menggunakan tool lebih jarang daripada Claude Opus 4.6 dan menggunakan penalaran lebih banyak. Ini menghasilkan hasil yang lebih baik dalam sebagian besar kasus. Namun, meningkatkan pengaturan upaya adalah lever yang berguna untuk meningkatkan tingkat penggunaan tool, terutama dalam pekerjaan pengetahuan. Pengaturan upaya `high` atau `xhigh` menunjukkan penggunaan tool yang jauh lebih banyak dalam pencarian agentic dan coding. Untuk skenario di mana Anda menginginkan lebih banyak penggunaan tool, Anda juga dapat menyesuaikan prompt Anda untuk secara eksplisit menginstruksikan model tentang kapan dan bagaimana menggunakan tool-nya dengan benar. Misalnya, jika Anda menemukan bahwa model tidak menggunakan tool pencarian web Anda, jelaskan dengan jelas mengapa dan bagaimana seharusnya.

### Pembaruan kemajuan yang menghadap pengguna

Claude Opus 4.7 memberikan pembaruan yang lebih teratur dan berkualitas lebih tinggi kepada pengguna di seluruh jejak agentic yang panjang. Jika Anda telah menambahkan scaffolding untuk memaksa pesan status interim ("Setelah setiap 3 panggilan tool, ringkas kemajuan"), coba hapus. Jika Anda menemukan bahwa panjang atau konten pembaruan yang menghadap pengguna Claude Opus 4.7 tidak dikalibrasi dengan baik untuk kasus penggunaan Anda, jelaskan secara eksplisit seperti apa pembaruan ini dalam prompt dan berikan contoh.

### Penurutan instruksi yang lebih literal

Claude Opus 4.7 menafsirkan prompt lebih literal dan eksplisit daripada Claude Opus 4.6, terutama pada tingkat upaya yang lebih rendah. Ini tidak akan diam-diam menggeneralisasi instruksi dari satu item ke item lain, dan tidak akan menyimpulkan permintaan yang tidak Anda buat. Sisi positif dari literalisme ini adalah presisi dan lebih sedikit thrash, dan umumnya berkinerja lebih baik untuk kasus penggunaan API dengan prompt yang dikalibrasi dengan hati-hati, ekstraksi terstruktur, dan pipeline di mana Anda menginginkan perilaku yang dapat diprediksi. Jika Anda memerlukan Claude untuk menerapkan instruksi secara luas, nyatakan cakupannya secara eksplisit (misalnya, "Terapkan pemformatan ini ke setiap bagian, bukan hanya yang pertama").

### Nada dan gaya penulisan

Seperti halnya model baru apa pun, gaya prosa pada penulisan bentuk panjang mungkin bergeser. Claude Opus 4.7 lebih langsung dan berpendapat, dengan frasa yang lebih sedikit yang berpusat pada validasi dan emoji lebih sedikit daripada gaya yang lebih hangat dari Claude Opus 4.6. Jika produk Anda mengandalkan suara tertentu, evaluasi kembali prompt gaya terhadap baseline baru.

Misalnya, jika suara produk Anda lebih hangat atau lebih percakapan, tambahkan:

```text
Gunakan nada yang hangat dan kolaboratif. Akui framing pengguna sebelum menjawab.
```

### Mengontrol spawning subagen

Claude Opus 4.7 cenderung untuk spawn lebih sedikit subagen secara default. Namun, perilaku ini dapat diarahkan melalui prompting; berikan Claude Opus 4.7 panduan eksplisit tentang kapan subagen diinginkan. Contoh mainan untuk kasus penggunaan coding:

```text
Jangan spawn subagen untuk pekerjaan yang dapat Anda selesaikan langsung dalam satu respons (misalnya refactoring fungsi yang sudah dapat Anda lihat).

Spawn beberapa subagen dalam giliran yang sama saat fanning out di seluruh item atau membaca beberapa file.
```

### Desain dan default frontend

Claude Opus 4.7 memiliki insting desain yang lebih kuat daripada Claude Opus 4.6, dengan gaya rumah default yang konsisten: latar belakang krem hangat/off-white (~`#F4F1EA`), tipe tampilan serif (Georgia, Fraunces, Playfair), aksen kata miring, dan aksen terracotta/amber. Ini terbaca dengan baik untuk editorial, perhotelan, dan brief portofolio, tetapi akan terasa tidak tepat untuk dashboard, dev tools, fintech, healthcare, atau aplikasi enterprise — dan muncul di slide deck serta UI web.

Default ini persisten. Instruksi generik ("jangan gunakan krem," "buat bersih dan minimal") cenderung menggeser model ke palet tetap yang berbeda daripada menghasilkan variasi. Dua pendekatan bekerja dengan andal:

**1. Tentukan alternatif konkret.** Model mengikuti spesifikasi eksplisit dengan tepat:

```text
Desain halaman landing desktop untuk merek suplemen yang disebut AEFRM.

Arah visual harus berasal dari suasana monokrom dingin menggunakan nada perak-abu-abu pucat yang secara bertahap menjadi lebih dalam menjadi biru-abu-abu dan hampir hitam, mirip dengan permukaan logam berkabut.

Halaman harus terasa tajam dan terkontrol, dengan rasa struktur dan penahan yang kuat.

Gunakan sistem nada ini di seluruh halaman daripada memperkenalkan warna aksen cerah.

Gunakan gambar yang diunggah pada desain pahlawan dalam hitam dan putih.

Tata letak harus dibangun dengan bagian horizontal yang jelas dan wadah lebar maksimal yang berpusat. Gunakan radius sudut 4px secara konsisten di seluruh kartu, tombol, input, dan bingkai media. Margin harus terasa murah hati, dengan cukup ruang kosong di sekitar setiap bagian sehingga halaman bernapas.

Tipografi harus menggunakan sans-serif persegi dan sudut dengan spasi huruf yang lebih lebar dari biasanya, terutama dalam judul dan navigasi, sehingga teks terasa lebih dirancang dan kurang dikompresi. Teks judul dapat besar dan huruf besar, sementara salinan pendukung tetap pendek dan jarang. Teks sub harus ditulis dengan Alumni Sans SC dalam 4-6px seperti teks kecil di sudut bawah tengah seperti itu.

Untuk struktur, mulai dengan bagian pahlawan yang berisi pernyataan produk yang kuat, satu paragraf pendukung pendek, dan bingkai placeholder produk yang bersih atau packshot. Di bawah itu, tambahkan grid manfaat dengan tiga atau empat blok, kemudian bagian formulasi atau bahan, dan akhirnya cta.

Tombol harus datar dan presisi, dengan perubahan hover halus menggunakan transition: all 160ms ease out di mana kecerahan dan kontras perbatasan bergeser sedikit daripada menggunakan gerakan dramatis.

Palet warna harus tetap dalam kisaran ini:
#E9ECEC, #C9D2D4, #8C9A9E, #44545B, #11171B.
```

**2. Biarkan model mengusulkan opsi sebelum membangun.** Ini memecah default dan memberi pengguna kontrol. Jika Anda sebelumnya mengandalkan `temperature` untuk variasi desain, gunakan pendekatan ini — ini menghasilkan arah yang bermakna berbeda di seluruh run. Contoh prompt:

```text
Sebelum membangun, usulkan 4 arah visual yang berbeda yang disesuaikan dengan brief ini (masing-masing sebagai: bg hex / accent hex / typeface — alasan satu baris). Minta pengguna untuk memilih satu, kemudian implementasikan hanya arah itu.
```

Selain itu, Claude Opus 4.7 memerlukan prompting desain frontend yang lebih sedikit daripada model sebelumnya untuk menghindari pola generik yang pengguna sebut estetika "AI slop". Dengan model sebelumnya, kami merekomendasikan cuplikan prompt yang lebih panjang dalam [skill desain frontend](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md) kami. Namun, Claude Opus 4.7 menghasilkan frontend yang khas dan kreatif dengan panduan prompting yang lebih minimal. Cuplikan prompt ini bekerja dengan baik dengan saran prompting di atas untuk variasi:

```text
<frontend_aesthetics>
JANGAN pernah gunakan estetika AI yang dihasilkan secara generik seperti keluarga font yang terlalu banyak digunakan (Inter, Roboto, Arial, font sistem), skema warna klise (terutama gradien ungu pada latar belakang putih atau gelap), tata letak yang dapat diprediksi dan pola komponen, dan desain cookie-cutter yang kurang karakter khusus konteks. Gunakan font unik, warna dan tema yang kohesif, dan animasi untuk efek dan micro-interactions.
</frontend_aesthetics>
```

### Produk coding interaktif

Penggunaan token Claude Opus 4.7 dan perilaku dapat berbeda antara agen coding otonom dan asinkron dengan satu giliran pengguna dan agen coding interaktif dan sinkron dengan beberapa giliran pengguna. Secara khusus, ini cenderung menggunakan lebih banyak token dalam pengaturan interaktif, terutama karena itu bernalar lebih banyak setelah giliran pengguna. Ini dapat meningkatkan kohesi jangka panjang, penurutan instruksi, dan kemampuan coding dalam sesi coding interaktif yang panjang, tetapi juga datang dengan penggunaan token yang lebih banyak. Untuk memaksimalkan kinerja dan efisiensi token dalam produk coding, kami merekomendasikan menggunakan upaya `xhigh` atau `high`, menambahkan fitur otonom seperti mode otomatis, dan mengurangi jumlah interaksi manusia yang diperlukan dari pengguna Anda.

Tentu saja, saat membatasi jumlah interaksi yang diperlukan, penting untuk menentukan tugas, niat, dan batasan yang relevan di muka dalam giliran manusia pertama. Memberikan deskripsi tugas yang ditentukan dengan baik, jelas, dan akurat di muka dapat membantu memaksimalkan otonomi dan kecerdasan sambil meminimalkan penggunaan token ekstra setelah giliran pengguna. Kami menemukan bahwa karena Claude Opus 4.7 lebih otonom daripada model sebelumnya, pola penggunaan ini membantu memaksimalkan kinerja. Sebaliknya, prompt yang ambigu atau kurang ditentukan yang disampaikan secara progresif selama beberapa giliran pengguna cenderung secara relatif mengurangi efisiensi token dan kadang-kadang kinerja.

### Harness review kode

Claude Opus 4.7 secara bermakna lebih baik dalam menemukan bug daripada model sebelumnya, dan memiliki recall dan presisi yang lebih tinggi dalam eval kami — 11pp recall yang lebih baik dalam salah satu eval penemuan bug tersulit kami berdasarkan PR Anthropic nyata. Namun, jika harness review kode Anda disesuaikan untuk model sebelumnya, Anda mungkin awalnya melihat recall yang lebih rendah. Ini mungkin efek harness, bukan regresi kemampuan. Ketika prompt review mengatakan hal-hal seperti "hanya laporkan masalah tingkat tinggi," "bersikap konservatif," atau "jangan nitpick," Claude Opus 4.7 dapat mengikuti instruksi itu lebih setia daripada model sebelumnya — itu mungkin menyelidiki kode dengan sama menyeluruhnya, mengidentifikasi bug, dan kemudian tidak melaporkan temuan yang dianggapnya di bawah bar yang dinyatakan. Ini dapat muncul sebagai model melakukan kedalaman investigasi yang sama tetapi mengonversi lebih sedikit investigasi menjadi temuan yang dilaporkan, terutama pada bug tingkat rendah. Presisi biasanya naik, tetapi recall yang diukur dapat turun meskipun kemampuan penemuan bug model yang mendasar telah meningkat.

Beberapa bahasa prompt yang direkomendasikan:

```text
Laporkan setiap masalah yang Anda temukan, termasuk yang Anda tidak yakin atau anggap tingkat rendah. Jangan filter untuk kepentingan atau kepercayaan pada tahap ini - langkah verifikasi terpisah akan melakukan itu. Tujuan Anda di sini adalah cakupan: lebih baik untuk permukaan temuan yang kemudian disaring daripada diam-diam menjatuhkan bug nyata. Untuk setiap temuan, sertakan tingkat kepercayaan Anda dan perkiraan keparahan sehingga filter hilir dapat mengurutkannya.
```

Prompt ini dapat digunakan tanpa memiliki langkah kedua yang sebenarnya, tetapi memindahkan penyaringan kepercayaan keluar dari langkah penemuan sering membantu. Jika harness Anda memiliki verifikasi terpisah, deduplikasi, atau tahap peringkat, beri tahu model secara eksplisit bahwa pekerjaannya pada tahap penemuan adalah cakupan daripada penyaringan.

Jika Anda ingin model untuk self-filter dalam satu pass, bersikap konkret tentang di mana bar daripada menggunakan istilah kualitatif seperti "penting" — misalnya, "laporkan bug apa pun yang dapat menyebabkan perilaku tidak benar, kegagalan tes, atau hasil yang menyesatkan; hanya lewati nits seperti preferensi gaya murni atau penamaan."

Kami merekomendasikan iterasi pada prompt terhadap subset eval atau kasus uji Anda untuk memvalidasi recall atau keuntungan skor F1.

### Penggunaan komputer

Kemampuan [penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool) bekerja di seluruh resolusi, hingga resolusi maksimal baru 2576px / 3.75MP. Dalam pengujian penggunaan komputer kami, kami menemukan bahwa mengirim gambar pada 1080p memberikan keseimbangan yang baik antara kinerja dan biaya.

Untuk beban kerja yang sangat sensitif terhadap biaya, kami merekomendasikan 720p atau 1366×768 sebagai opsi biaya lebih rendah dengan kinerja yang kuat. Kami merekomendasikan bahwa Anda melakukan pengujian Anda sendiri untuk menemukan pengaturan ideal untuk kasus penggunaan Anda; bereksperimen dengan pengaturan upaya juga dapat membantu menyesuaikan perilaku model.

## Prinsip umum

### Jadilah jelas dan langsung

Claude merespons dengan baik terhadap instruksi yang jelas dan eksplisit. Menjadi spesifik tentang output yang diinginkan dapat membantu meningkatkan hasil. Jika Anda menginginkan perilaku "di atas dan di luar," minta secara eksplisit daripada mengandalkan model untuk menyimpulkan ini dari prompt yang samar.

Pikirkan Claude sebagai karyawan cemerlang tetapi baru yang kurang konteks tentang norma dan alur kerja Anda. Semakin tepat Anda menjelaskan apa yang Anda inginkan, semakin baik hasilnya.

**Aturan emas:** Tunjukkan prompt Anda kepada rekan kerja dengan konteks minimal tentang tugas dan minta mereka mengikutinya. Jika mereka akan bingung, Claude juga akan.

- Jadilah spesifik tentang format output yang diinginkan dan batasan.
- Berikan instruksi sebagai langkah berurutan menggunakan daftar bernomor atau poin peluru ketika urutan atau kelengkapan langkah penting.

<section title="Contoh: Membuat dashboard analitik">

**Kurang efektif:**
```text
Buat dashboard analitik
```

**Lebih efektif:**
```text
Buat dashboard analitik. Sertakan sebanyak mungkin fitur dan interaksi yang relevan. Lakukan lebih dari dasar untuk membuat implementasi yang lengkap.
```

</section>

### Tambahkan konteks untuk meningkatkan kinerja

Memberikan konteks atau motivasi di balik instruksi Anda, seperti menjelaskan kepada Claude mengapa perilaku seperti itu penting, dapat membantu Claude lebih memahami tujuan Anda dan memberikan respons yang lebih ditargetkan.

<section title="Contoh: Preferensi pemformatan">

**Kurang efektif:**
```text
JANGAN pernah gunakan elipsis
```

**Lebih efektif:**
```text
Respons Anda akan dibaca oleh mesin text-to-speech, jadi jangan pernah gunakan elipsis karena mesin text-to-speech tidak akan tahu cara mengucapkannya.
```

</section>

Claude cukup pintar untuk menggeneralisasi dari penjelasan.

### Gunakan contoh secara efektif

Contoh adalah salah satu cara paling andal untuk mengarahkan format output, nada, dan struktur Claude. Beberapa contoh yang dirancang dengan baik (dikenal sebagai prompting few-shot atau multishot) dapat secara dramatis meningkatkan akurasi dan konsistensi.

Saat menambahkan contoh, buatlah:
- **Relevan:** Cerminkan kasus penggunaan aktual Anda dengan dekat.
- **Beragam:** Cakup kasus tepi dan bervariasi cukup sehingga Claude tidak mengambil pola yang tidak disengaja.
- **Terstruktur:** Bungkus contoh dalam tag `<example>` (beberapa contoh dalam tag `<examples>`) sehingga Claude dapat membedakannya dari instruksi.

<Tip>Sertakan 3–5 contoh untuk hasil terbaik. Anda juga dapat meminta Claude untuk mengevaluasi contoh Anda untuk relevansi dan keragaman, atau untuk menghasilkan contoh tambahan berdasarkan set awal Anda.</Tip>

### Struktur prompt dengan tag XML

Tag XML membantu Claude mengurai prompt kompleks secara tidak ambigu, terutama ketika prompt Anda mencampur instruksi, konteks, contoh, dan input variabel. Membungkus setiap jenis konten dalam tag-nya sendiri (misalnya `<instructions>`, `<context>`, `<input>`) mengurangi salah tafsir.

Praktik terbaik:
- Gunakan nama tag yang konsisten dan deskriptif di seluruh prompt Anda.
- Bersarangkan tag ketika konten memiliki hierarki alami (dokumen di dalam `<documents>`, masing-masing di dalam `<document index="n">`).

### Berikan Claude peran

Menetapkan peran dalam prompt sistem memfokuskan perilaku dan nada Claude untuk kasus penggunaan Anda. Bahkan satu kalimat membuat perbedaan:

```python Python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    system="Anda adalah asisten coding yang membantu dan mengkhususkan diri dalam Python.",
    messages=[
        {"role": "user", "content": "Bagaimana cara mengurutkan daftar kamus berdasarkan kunci?"}
    ],
)
print(message.content)
```

### Prompting konteks panjang

Saat bekerja dengan dokumen besar atau input kaya data (20k+ token), struktur prompt Anda dengan hati-hati untuk mendapatkan hasil terbaik:

- **Letakkan data bentuk panjang di atas**: Tempatkan dokumen panjang dan input Anda di dekat bagian atas prompt Anda, di atas kueri, instruksi, dan contoh Anda. Ini dapat secara signifikan meningkatkan kinerja di semua model.

    <Note>Kueri di akhir dapat meningkatkan kualitas respons hingga 30% dalam tes, terutama dengan input multi-dokumen yang kompleks.</Note>

- **Struktur konten dokumen dan metadata dengan tag XML**: Saat menggunakan beberapa dokumen, bungkus setiap dokumen dalam tag `<document>` dengan subtag `<document_content>` dan `<source>` (dan metadata lainnya) untuk kejelasan.

    <section title="Contoh struktur multi-dokumen">

    ```xml
    <documents>
      <document index="1">
        <source>annual_report_2023.pdf</source>
        <document_content>
          {{ANNUAL_REPORT}}
        </document_content>
      </document>
      <document index="2">
        <source>competitor_analysis_q2.xlsx</source>
        <document_content>
          {{COMPETITOR_ANALYSIS}}
        </document_content>
      </document>
    </documents>

    Analisis laporan tahunan dan analisis pesaing. Identifikasi keunggulan strategis dan rekomendasikan area fokus Q3.
    ```
    
</section>

- **Tandaskan respons dalam kutipan**: Untuk tugas dokumen panjang, minta Claude untuk mengutip bagian dokumen yang relevan terlebih dahulu sebelum melaksanakan tugasnya. Ini membantu Claude memotong kebisingan dari sisa konten dokumen.

    <section title="Contoh ekstraksi kutipan">

    ```xml
    Anda adalah asisten dokter AI. Tugas Anda adalah membantu dokter mendiagnosis kemungkinan penyakit pasien.

    <documents>
      <document index="1">
        <source>patient_symptoms.txt</source>
        <document_content>
          {{PATIENT_SYMPTOMS}}
        </document_content>
      </document>
      <document index="2">
        <source>patient_records.txt</source>
        <document_content>
          {{PATIENT_RECORDS}}
        </document_content>
      </document>
      <document index="3">
        <source>patient01_appt_history.txt</source>
        <document_content>
          {{PATIENT01_APPOINTMENT_HISTORY}}
        </document_content>
      </document>
    </documents>

    Temukan kutipan dari catatan pasien dan riwayat janji temu yang relevan dengan mendiagnosis gejala yang dilaporkan pasien. Tempatkan ini dalam tag <quotes>. Kemudian, berdasarkan kutipan ini, daftarkan semua informasi yang akan membantu dokter mendiagnosis gejala pasien. Tempatkan informasi diagnostik Anda dalam tag <info>.
    ```
    
</section>

### Pengetahuan diri model

Jika Anda ingin Claude mengidentifikasi dirinya dengan benar dalam aplikasi Anda atau menggunakan string API tertentu:

```text Contoh prompt untuk identitas model
Asisten adalah Claude, dibuat oleh Anthropic. Model saat ini adalah Claude Opus 4.7.
```

Untuk aplikasi bertenaga LLM yang perlu menentukan string model:

```text Contoh prompt untuk string model
Ketika LLM diperlukan, silakan default ke Claude Opus 4.7 kecuali pengguna meminta sebaliknya. String model yang tepat untuk Claude Opus 4.7 adalah claude-opus-4-7.
```

## Output dan pemformatan

### Gaya komunikasi dan verbositas

Model terbaru Claude memiliki gaya komunikasi yang lebih ringkas dan alami dibandingkan dengan model sebelumnya:

- **Lebih langsung dan berbasis fakta:** Memberikan laporan kemajuan berbasis fakta daripada pembaruan yang merayakan diri sendiri
- **Lebih percakapan:** Sedikit lebih lancar dan percakapan, kurang seperti mesin
- **Kurang verbose:** Mungkin melewati ringkasan terperinci untuk efisiensi kecuali diminta sebaliknya

Ini berarti Claude mungkin melewati ringkasan verbal setelah panggilan tool, melompat langsung ke tindakan berikutnya. Jika Anda lebih suka lebih banyak visibilitas ke dalam penalarannya:

```text Contoh prompt
Setelah menyelesaikan tugas yang melibatkan penggunaan tool, berikan ringkasan cepat tentang pekerjaan yang telah Anda lakukan.
```

### Kontrol format respons

Ada beberapa cara yang sangat efektif untuk mengarahkan pemformatan output:

1. **Beri tahu Claude apa yang harus dilakukan daripada apa yang tidak boleh dilakukan**

   - Daripada: "Jangan gunakan markdown dalam respons Anda"
   - Coba: "Respons Anda harus terdiri dari paragraf prosa yang mengalir dengan mulus."

2. **Gunakan indikator format XML**

   - Coba: "Tulis bagian prosa respons Anda dalam tag \<smoothly_flowing_prose_paragraphs\>."

3. **Cocokkan gaya prompt Anda dengan output yang diinginkan**

   Gaya pemformatan yang digunakan dalam prompt Anda dapat mempengaruhi gaya respons Claude. Jika Anda masih mengalami masalah steerability dengan pemformatan output, coba cocokkan gaya prompt Anda sedekat mungkin dengan gaya output yang diinginkan. Misalnya, menghapus markdown dari prompt Anda dapat mengurangi volume markdown dalam output.

4. **Gunakan prompt terperinci untuk preferensi pemformatan spesifik**

   Untuk kontrol lebih besar atas penggunaan markdown dan pemformatan, berikan panduan eksplisit:

```text Contoh prompt untuk meminimalkan markdown
<avoid_excessive_markdown_and_bullet_points>
Saat menulis laporan, dokumen, penjelasan teknis, analisis, atau konten bentuk panjang apa pun, tulis dalam prosa yang jelas dan mengalir menggunakan paragraf dan kalimat lengkap. Gunakan pemisah paragraf standar untuk organisasi dan cadangkan markdown terutama untuk `inline code`, blok kode (```...```), dan judul sederhana (###, dan ###). Hindari menggunakan **bold** dan *italics*.

JANGAN gunakan daftar terurut (1. ...) atau daftar tidak terurut (*) kecuali : a) Anda menyajikan item yang benar-benar diskrit di mana format daftar adalah opsi terbaik, atau b) pengguna secara eksplisit meminta daftar atau peringkat

Alih-alih membuat daftar item dengan peluru atau angka, gabungkan secara alami ke dalam kalimat. Panduan ini berlaku terutama untuk penulisan teknis. Menggunakan prosa daripada pemformatan berlebihan akan meningkatkan kepuasan pengguna. JANGAN pernah keluarkan serangkaian poin peluru yang terlalu pendek.

Tujuan Anda adalah teks yang dapat dibaca dan mengalir yang memandu pembaca secara alami melalui ide daripada memfragmentasi informasi menjadi poin terisolasi.
</avoid_excessive_markdown_and_bullet_points>
```

### Output LaTeX

Claude Opus 4.6 default ke LaTeX untuk ekspresi matematika, persamaan, dan penjelasan teknis. Jika Anda lebih suka teks biasa, tambahkan instruksi berikut ke prompt Anda:

```text Contoh prompt
Format respons Anda dalam teks biasa saja. Jangan gunakan LaTeX, MathJax, atau notasi markup apa pun seperti \( \), $, atau \frac{}{}. Tulis semua ekspresi matematika menggunakan karakter teks standar (misalnya, "/" untuk pembagian, "*" untuk perkalian, dan "^" untuk eksponen).
```

### Pembuatan dokumen

Model terbaru Claude unggul dalam membuat presentasi, animasi, dan dokumen visual dengan kilau kreatif yang mengesankan dan penurutan instruksi yang kuat. Model menghasilkan output yang dipoles dan dapat digunakan pada percobaan pertama dalam sebagian besar kasus.

Untuk hasil terbaik dengan pembuatan dokumen:

```text Contoh prompt
Buat presentasi profesional tentang [topik]. Sertakan elemen desain yang bijaksana, hierarki visual, dan animasi yang menarik jika sesuai.
```

### Bermigrasi dari respons yang sudah diisi sebelumnya

Mulai dengan model Claude 4.6 dan [Claude Mythos Preview](https://anthropic.com/glasswing), respons yang sudah diisi sebelumnya pada giliran asisten terakhir tidak lagi didukung. Pada Mythos Preview, permintaan dengan pesan asisten yang sudah diisi sebelumnya mengembalikan kesalahan 400. Kecerdasan model dan penurutan instruksi telah maju sedemikian rupa sehingga sebagian besar kasus penggunaan prefill tidak lagi memerlukan itu. Model yang ada akan terus mendukung prefill, dan menambahkan pesan asisten di tempat lain dalam percakapan tidak terpengaruh.

Berikut adalah skenario prefill umum dan cara bermigrasi darinya:

<section title="Mengontrol pemformatan output">

Prefill telah digunakan untuk memaksa format output spesifik seperti JSON/YAML, klasifikasi, dan pola serupa di mana prefill membatasi Claude ke struktur tertentu.

**Migrasi:** Fitur [Structured Outputs](/docs/id/build-with-claude/structured-outputs) dirancang khusus untuk membatasi respons Claude agar sesuai dengan skema tertentu. Coba cukup minta model untuk menyesuaikan dengan struktur output Anda terlebih dahulu, karena model yang lebih baru dapat secara andal mencocokkan skema kompleks ketika diberitahu, terutama jika diimplementasikan dengan percobaan ulang. Untuk tugas klasifikasi, gunakan tool dengan bidang enum yang berisi label valid Anda atau output terstruktur.

</section>

<section title="Menghilangkan preambul">

Prefill seperti `Here is the requested summary:\n` digunakan untuk melewati teks pengantar.

**Migrasi:** Gunakan instruksi langsung dalam prompt sistem: "Respons langsung tanpa preambul. Jangan mulai dengan frasa seperti 'Berikut adalah...', 'Berdasarkan...', dll." Alternatifnya, arahkan model untuk output dalam tag XML, gunakan output terstruktur, atau gunakan pemanggilan tool. Jika preambul sesekali terselip, lepaskan dalam post-processing.

</section>

<section title="Menghindari penolakan yang buruk">

Prefill digunakan untuk mengarahkan penolakan yang tidak perlu.

**Migrasi:** Claude sekarang jauh lebih baik dalam penolakan yang tepat. Prompting yang jelas dalam pesan `user` tanpa prefill harus cukup.

</section>

<section title="Kelanjutan">

Prefill digunakan untuk melanjutkan penyelesaian parsial, melanjutkan respons yang terputus, atau melanjutkan dari mana generasi sebelumnya berhenti.

**Migrasi:** Pindahkan kelanjutan ke pesan pengguna, dan sertakan teks terakhir dari respons yang terputus: "Respons sebelumnya Anda terputus dan berakhir dengan \`[previous_response]\`. Lanjutkan dari mana Anda berhenti." Jika ini adalah bagian dari penanganan kesalahan atau penanganan respons yang tidak lengkap dan tidak ada penalti UX, coba lagi permintaan.

</section>

<section title="Hidrasi konteks dan konsistensi peran">

Prefill digunakan untuk secara berkala memastikan konteks yang disegarkan atau disuntikkan.

**Migrasi:** Untuk percakapan yang sangat panjang, suntikkan apa yang sebelumnya adalah pengingat asisten yang sudah diisi sebelumnya ke dalam giliran pengguna. Jika hidrasi konteks adalah bagian dari sistem agentic yang lebih kompleks, pertimbangkan hidrasi melalui tool (paparkan atau dorong penggunaan tool yang berisi konteks berdasarkan heuristik seperti jumlah giliran) atau selama pemadatan konteks.

</section>

## Penggunaan tool

### Penggunaan tool

Model terbaru Claude dilatih untuk penurutan instruksi yang tepat dan mendapat manfaat dari arahan eksplisit untuk menggunakan tool tertentu. Jika Anda mengatakan "dapatkah Anda menyarankan beberapa perubahan," Claude kadang-kadang akan memberikan saran daripada menerapkannya, bahkan jika membuat perubahan mungkin apa yang Anda maksudkan.

Untuk Claude mengambil tindakan, jadilah lebih eksplisit:

<section title="Contoh: Instruksi eksplisit">

**Kurang efektif (Claude hanya akan menyarankan):**
```text
Dapatkah Anda menyarankan beberapa perubahan untuk meningkatkan fungsi ini?
```

**Lebih efektif (Claude akan membuat perubahan):**
```text
Ubah fungsi ini untuk meningkatkan kinerjanya.
```

Atau:
```text
Buat edit ini pada alur autentikasi.
```

</section>

Untuk membuat Claude lebih proaktif tentang mengambil tindakan secara default, Anda dapat menambahkan ini ke prompt sistem Anda:

```text Contoh prompt untuk tindakan proaktif
<default_to_action>
Secara default, implementasikan perubahan daripada hanya menyarankannya. Jika niat pengguna tidak jelas, simpulkan tindakan yang paling mungkin berguna dan lanjutkan, menggunakan tool untuk menemukan detail yang hilang daripada menebak. Coba simpulkan niat pengguna tentang apakah panggilan tool (misalnya edit file atau baca) dimaksudkan atau tidak, dan bertindak sesuai.
</default_to_action>
```

Di sisi lain, jika Anda ingin model lebih ragu secara default, kurang rentan untuk langsung melompat ke implementasi, dan hanya mengambil tindakan jika diminta, Anda dapat mengarahkan perilaku ini dengan prompt seperti di bawah:

```text Contoh prompt untuk tindakan konservatif
<do_not_act_before_instructions>
Jangan melompat ke implementasi atau ubah file kecuali jelas diperintahkan untuk membuat perubahan. Ketika niat pengguna ambigu, default untuk memberikan informasi, melakukan penelitian, dan memberikan rekomendasi daripada mengambil tindakan. Hanya lanjutkan dengan edit, modifikasi, atau implementasi ketika pengguna secara eksplisit memintanya.
</do_not_act_before_instructions>
```

Claude Opus 4.5 dan Claude Opus 4.6 juga lebih responsif terhadap prompt sistem daripada model sebelumnya. Jika prompt Anda dirancang untuk mengurangi undertriggering pada tool atau skill, model ini mungkin sekarang overtrigger. Perbaikannya adalah mengurangi bahasa yang agresif. Di mana Anda mungkin telah mengatakan "KRITIS: Anda HARUS menggunakan tool ini ketika...", Anda dapat menggunakan prompting yang lebih normal seperti "Gunakan tool ini ketika...".

### Optimalkan pemanggilan alat paralel

Model terbaru Claude unggul dalam eksekusi alat paralel. Model-model ini akan:

- Menjalankan beberapa pencarian spekulatif selama penelitian
- Membaca beberapa file sekaligus untuk membangun konteks lebih cepat
- Menjalankan perintah bash secara paralel (yang bahkan dapat membuat kemacetan kinerja sistem)

Perilaku ini mudah diarahkan. Meskipun model memiliki tingkat keberhasilan tinggi dalam pemanggilan alat paralel tanpa prompting, Anda dapat meningkatkan ini hingga ~100% atau menyesuaikan tingkat agresivitas:

```text Contoh prompt untuk efisiensi paralel maksimal
<use_parallel_tool_calls>
Jika Anda bermaksud memanggil beberapa alat dan tidak ada ketergantungan antara panggilan alat, buat semua panggilan alat independen secara paralel. Prioritaskan pemanggilan alat secara bersamaan kapan pun tindakan dapat dilakukan secara paralel daripada berurutan. Misalnya, saat membaca 3 file, jalankan 3 panggilan alat secara paralel untuk membaca ketiga file ke dalam konteks pada waktu yang sama. Maksimalkan penggunaan panggilan alat paralel jika memungkinkan untuk meningkatkan kecepatan dan efisiensi. Namun, jika beberapa panggilan alat bergantung pada panggilan sebelumnya untuk menginformasikan nilai dependen seperti parameter, JANGAN panggil alat-alat ini secara paralel dan sebaliknya panggil secara berurutan. Jangan pernah gunakan placeholder atau tebak parameter yang hilang dalam panggilan alat.
</use_parallel_tool_calls>
```

```text Contoh prompt untuk mengurangi eksekusi paralel
Jalankan operasi secara berurutan dengan jeda singkat antara setiap langkah untuk memastikan stabilitas.
```

## Pemikiran dan penalaran

### Pemikiran berlebihan dan kesempurnaan yang berlebihan

Claude Opus 4.6 melakukan eksplorasi awal yang jauh lebih signifikan dibandingkan model sebelumnya, terutama pada pengaturan `effort` yang lebih tinggi. Pekerjaan awal ini sering membantu mengoptimalkan hasil akhir, tetapi model dapat mengumpulkan konteks ekstensif atau mengejar beberapa thread penelitian tanpa diminta. Jika prompt Anda sebelumnya mendorong model untuk lebih menyeluruh, Anda harus menyesuaikan panduan tersebut untuk Claude Opus 4.6:

- **Ganti default blanket dengan instruksi yang lebih tertarget.** Alih-alih "Default menggunakan \[tool\]," tambahkan panduan seperti "Gunakan \[tool\] ketika itu akan meningkatkan pemahaman Anda tentang masalah."
- **Hapus over-prompting.** Alat yang kurang terpicu di model sebelumnya kemungkinan akan terpicu dengan tepat sekarang. Instruksi seperti "Jika ragu, gunakan \[tool\]" akan menyebabkan overtriggering.
- **Gunakan effort sebagai fallback.** Jika Claude terus menjadi terlalu agresif, gunakan pengaturan yang lebih rendah untuk `effort`.

Dalam beberapa kasus, Claude Opus 4.6 mungkin berpikir secara ekstensif, yang dapat meningkatkan thinking tokens dan memperlambat respons. Jika perilaku ini tidak diinginkan, Anda dapat menambahkan instruksi eksplisit untuk membatasi penalarannya, atau Anda dapat menurunkan pengaturan `effort` untuk mengurangi pemikiran dan penggunaan token secara keseluruhan.

```text Contoh prompt
Ketika Anda memutuskan cara mendekati masalah, pilih pendekatan dan berkomitmen padanya. Hindari meninjau kembali keputusan kecuali Anda menemukan informasi baru yang secara langsung bertentangan dengan penalaran Anda. Jika Anda mempertimbangkan dua pendekatan, pilih satu dan lihat sampai selesai. Anda selalu dapat mengubah arah nanti jika pendekatan yang dipilih gagal.
```

Jika Anda memerlukan batas keras pada biaya pemikiran, extended thinking dengan batas `budget_tokens` masih berfungsi pada Opus 4.6 dan Sonnet 4.6 tetapi sudah usang. Lebih suka menurunkan pengaturan [effort](/docs/id/build-with-claude/effort) atau menggunakan `max_tokens` sebagai batas keras dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking).

### Manfaatkan kemampuan thinking & interleaved thinking

Model terbaru Claude menawarkan kemampuan thinking yang dapat sangat membantu untuk tugas-tugas yang melibatkan refleksi setelah penggunaan alat atau penalaran multi-langkah yang kompleks. Anda dapat memandu pemikiran awal atau interleaved-nya untuk hasil yang lebih baik.

Claude Opus 4.6 dan Claude Sonnet 4.6 menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`), di mana Claude secara dinamis memutuskan kapan dan berapa banyak untuk berpikir. Claude mengkalibrasi pemikirannya berdasarkan dua faktor: parameter `effort` dan kompleksitas query. Effort yang lebih tinggi menghasilkan lebih banyak pemikiran, dan query yang lebih kompleks juga demikian. Pada query yang lebih mudah yang tidak memerlukan pemikiran, model merespons secara langsung. Dalam evaluasi internal, adaptive thinking secara andal mendorong kinerja yang lebih baik daripada extended thinking. Pertimbangkan untuk pindah ke adaptive thinking untuk mendapatkan respons yang paling cerdas.

Gunakan adaptive thinking untuk beban kerja yang memerlukan perilaku agentic seperti penggunaan alat multi-langkah, tugas coding kompleks, dan loop agent jangka panjang. Model yang lebih lama menggunakan mode pemikiran manual dengan `budget_tokens`.

Anda dapat memandu perilaku pemikiran Claude:

```text Contoh prompt
Setelah menerima hasil alat, hati-hati refleksikan kualitas mereka dan tentukan langkah selanjutnya yang optimal sebelum melanjutkan. Gunakan pemikiran Anda untuk merencanakan dan mengulangi berdasarkan informasi baru ini, kemudian ambil tindakan terbaik berikutnya.
```

Perilaku pemicu untuk adaptive thinking dapat diprompt. Jika Anda menemukan model berpikir lebih sering daripada yang Anda inginkan, yang dapat terjadi dengan prompt sistem yang besar atau kompleks, tambahkan panduan untuk mengarahkannya:

```text Contoh prompt
Extended thinking menambah latensi dan hanya boleh digunakan ketika itu akan secara bermakna meningkatkan kualitas jawaban - biasanya untuk masalah yang memerlukan penalaran multi-langkah. Jika ragu, respons secara langsung.
```

Jika Anda bermigrasi dari [extended thinking](/docs/id/build-with-claude/extended-thinking) dengan `budget_tokens`, ganti konfigurasi pemikiran Anda dan pindahkan kontrol budget ke `effort`:

**Sebelumnya (extended thinking, model yang lebih lama):**

```python Python nocheck
client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=64000,
    thinking={"type": "enabled", "budget_tokens": 32000},
    messages=[{"role": "user", "content": "..."}],
)
```

**Sesudahnya (adaptive thinking):**

```python Python nocheck
client.messages.create(
    model="claude-opus-4-7",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},  # or "max", "xhigh", "medium", "low"
    messages=[{"role": "user", "content": "..."}],
)
```

Jika Anda tidak menggunakan extended thinking, tidak ada perubahan yang diperlukan. Thinking dimatikan secara default ketika Anda menghilangkan parameter `thinking`.

- **Lebih suka instruksi umum daripada langkah-langkah preskriptif.** Prompt seperti "berpikir secara menyeluruh" sering menghasilkan penalaran yang lebih baik daripada rencana langkah demi langkah yang ditulis tangan. Penalaran Claude sering kali melebihi apa yang akan ditentukan manusia.
- **Contoh multishot bekerja dengan thinking.** Gunakan tag `<thinking>` di dalam contoh few-shot Anda untuk menunjukkan kepada Claude pola penalaran. Itu akan menggeneralisasi gaya itu ke blok extended thinking-nya sendiri.
- **Manual CoT sebagai fallback.** Ketika thinking dimatikan, Anda masih dapat mendorong penalaran langkah demi langkah dengan meminta Claude untuk berpikir melalui masalah. Gunakan tag terstruktur seperti `<thinking>` dan `<answer>` untuk memisahkan penalaran dari output akhir dengan bersih.
- **Minta Claude untuk self-check.** Tambahkan sesuatu seperti "Sebelum Anda selesai, verifikasi jawaban Anda terhadap [test criteria]." Ini menangkap kesalahan dengan andal, terutama untuk coding dan matematika.

<Note>Ketika extended thinking dinonaktifkan, Claude Opus 4.5 sangat sensitif terhadap kata "think" dan variannya. Pertimbangkan menggunakan alternatif seperti "consider," "evaluate," atau "reason through" dalam kasus-kasus tersebut.</Note>

<Info>
  Untuk informasi lebih lanjut tentang kemampuan thinking, lihat [Extended thinking](/docs/id/build-with-claude/extended-thinking) dan [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking).
</Info>

## Sistem agentic

### Penalaran jangka panjang dan pelacakan status

Model terbaru Claude unggul dalam tugas penalaran jangka panjang dengan kemampuan pelacakan status yang luar biasa. Claude mempertahankan orientasi di seluruh sesi yang diperpanjang dengan fokus pada kemajuan inkremental, membuat kemajuan yang stabil pada beberapa hal sekaligus daripada mencoba semuanya sekaligus. Kemampuan ini terutama muncul di seluruh beberapa jendela konteks atau iterasi tugas, di mana Claude dapat bekerja pada tugas kompleks, menyimpan status, dan melanjutkan dengan jendela konteks yang segar.

#### Kesadaran konteks dan alur kerja multi-jendela

Model Claude 4.6 dan Claude 4.5 menampilkan [context awareness](/docs/id/build-with-claude/context-windows#context-awareness-in-claude-sonnet-4-6-sonnet-4-5-and-haiku-4-5), memungkinkan model untuk melacak jendela konteks yang tersisa (yaitu "token budget") di seluruh percakapan. Ini memungkinkan Claude untuk menjalankan tugas dan mengelola konteks lebih efektif dengan memahami berapa banyak ruang yang dimilikinya untuk bekerja.

**Mengelola batas konteks:**

Jika Anda menggunakan Claude dalam harness agent yang memadatkan konteks atau memungkinkan menyimpan konteks ke file eksternal (seperti di Claude Code), pertimbangkan menambahkan informasi ini ke prompt Anda sehingga Claude dapat berperilaku sesuai. Jika tidak, Claude mungkin kadang-kadang secara alami mencoba membungkus pekerjaan saat mendekati batas konteks. Di bawah ini adalah contoh prompt:

```text Contoh prompt
Jendela konteks Anda akan secara otomatis dipadatkan saat mendekati batasnya, memungkinkan Anda untuk terus bekerja tanpa batas dari tempat Anda berhenti. Oleh karena itu, jangan hentikan tugas lebih awal karena kekhawatiran anggaran token. Saat Anda mendekati batas anggaran token, simpan kemajuan dan status saat ini ke memori sebelum jendela konteks menyegarkan. Selalu sebersifat persisten dan otonom mungkin dan selesaikan tugas sepenuhnya, bahkan jika akhir anggaran Anda mendekati. Jangan pernah secara artifisial hentikan tugas apa pun lebih awal terlepas dari konteks yang tersisa.
```

[Memory tool](/docs/id/agents-and-tools/tool-use/memory-tool) berpasangan secara alami dengan context awareness untuk transisi konteks yang mulus.

#### Alur kerja multi-jendela konteks

Untuk tugas yang mencakup beberapa jendela konteks:

1. **Gunakan prompt yang berbeda untuk jendela konteks pertama yang sangat pertama**: Gunakan jendela konteks pertama untuk menyiapkan kerangka kerja (tulis tes, buat skrip setup), kemudian gunakan jendela konteks masa depan untuk mengulangi daftar todo.

2. **Buat model menulis tes dalam format terstruktur**: Minta Claude untuk membuat tes sebelum memulai pekerjaan dan lacak mereka dalam format terstruktur (misalnya, `tests.json`). Ini mengarah pada kemampuan jangka panjang yang lebih baik untuk mengulangi. Ingatkan Claude tentang pentingnya tes: "Tidak dapat diterima untuk menghapus atau mengedit tes karena ini dapat menyebabkan fungsionalitas yang hilang atau buggy."

3. **Siapkan alat kualitas hidup**: Dorong Claude untuk membuat skrip setup (misalnya, `init.sh`) untuk memulai server dengan baik, menjalankan suite tes, dan linters. Ini mencegah pekerjaan berulang saat melanjutkan dari jendela konteks yang segar.

4. **Memulai dari awal vs pemadatan**: Ketika jendela konteks dihapus, pertimbangkan memulai dengan jendela konteks yang benar-benar baru daripada menggunakan pemadatan. Model terbaru Claude sangat efektif dalam menemukan status dari filesystem lokal. Dalam beberapa kasus, Anda mungkin ingin memanfaatkan ini daripada pemadatan. Jadilah preskriptif tentang bagaimana itu harus dimulai:
   - "Panggil pwd; Anda hanya dapat membaca dan menulis file di direktori ini."
   - "Tinjau progress.txt, tests.json, dan git logs."
   - "Jalankan secara manual melalui tes integrasi fundamental sebelum melanjutkan untuk mengimplementasikan fitur baru."

5. **Sediakan alat verifikasi**: Seiring dengan bertambahnya panjang tugas otonom, Claude perlu memverifikasi kebenaran tanpa umpan balik manusia yang berkelanjutan. Alat seperti server Playwright MCP atau kemampuan penggunaan komputer untuk menguji UI sangat membantu.

6. **Dorong penggunaan konteks yang lengkap**: Prompt Claude untuk menyelesaikan komponen secara efisien sebelum melanjutkan:

```text Contoh prompt
Ini adalah tugas yang sangat panjang, jadi mungkin bermanfaat untuk merencanakan pekerjaan Anda dengan jelas. Disarankan untuk menghabiskan seluruh konteks output Anda bekerja pada tugas - hanya pastikan Anda tidak kehabisan konteks dengan pekerjaan yang belum dikomit yang signifikan. Terus bekerja secara sistematis sampai Anda menyelesaikan tugas ini.
```

#### Praktik terbaik manajemen status

- **Gunakan format terstruktur untuk data status**: Saat melacak informasi terstruktur (seperti hasil tes atau status tugas), gunakan JSON atau format terstruktur lainnya untuk membantu Claude memahami persyaratan skema
- **Gunakan teks tidak terstruktur untuk catatan kemajuan**: Catatan kemajuan freeform bekerja dengan baik untuk melacak kemajuan umum dan konteks
- **Gunakan git untuk pelacakan status**: Git menyediakan log apa yang telah dilakukan dan checkpoint yang dapat dipulihkan. Model terbaru Claude berkinerja sangat baik dalam menggunakan git untuk melacak status di seluruh beberapa sesi.
- **Tekankan kemajuan inkremental**: Secara eksplisit minta Claude untuk melacak kemajuannya dan fokus pada pekerjaan inkremental

<section title="Contoh: Pelacakan status">

```json
// File status terstruktur (tests.json)
{
  "tests": [
    { "id": 1, "name": "authentication_flow", "status": "passing" },
    { "id": 2, "name": "user_management", "status": "failing" },
    { "id": 3, "name": "api_endpoints", "status": "not_started" }
  ],
  "total": 200,
  "passing": 150,
  "failing": 25,
  "not_started": 25
}
```

```text
// Catatan kemajuan (progress.txt)
Kemajuan Sesi 3:
- Perbaiki validasi token autentikasi
- Perbarui model pengguna untuk menangani kasus tepi
- Berikutnya: investigasi kegagalan tes user_management (tes #2)
- Catatan: Jangan hapus tes karena ini dapat menyebabkan fungsionalitas yang hilang
```

</section>

### Menyeimbangkan otonomi dan keamanan

Tanpa panduan, Claude Opus 4.6 dapat mengambil tindakan yang sulit untuk dibalikkan atau mempengaruhi sistem bersama, seperti menghapus file, force-pushing, atau posting ke layanan eksternal. Jika Anda ingin Claude Opus 4.6 mengkonfirmasi sebelum mengambil tindakan yang berpotensi berisiko, tambahkan panduan ke prompt Anda:

```text Contoh prompt
Pertimbangkan reversibilitas dan dampak potensial dari tindakan Anda. Anda didorong untuk mengambil tindakan lokal yang dapat dibalikkan seperti mengedit file atau menjalankan tes, tetapi untuk tindakan yang sulit dibalikkan, mempengaruhi sistem bersama, atau dapat merusak, minta pengguna sebelum melanjutkan.

Contoh tindakan yang memerlukan konfirmasi:
- Operasi destruktif: menghapus file atau cabang, menjatuhkan tabel database, rm -rf
- Operasi sulit dibalikkan: git push --force, git reset --hard, mengamandemen komit yang dipublikasikan
- Operasi terlihat oleh orang lain: mendorong kode, berkomentar pada PR/issues, mengirim pesan, memodifikasi infrastruktur bersama

Ketika menghadapi hambatan, jangan gunakan tindakan destruktif sebagai jalan pintas. Misalnya, jangan lewati pemeriksaan keamanan (misalnya --no-verify) atau buang file yang tidak dikenal yang mungkin merupakan pekerjaan yang sedang berlangsung.
```

### Penelitian dan pengumpulan informasi

Model terbaru Claude menunjukkan kemampuan pencarian agentic yang luar biasa dan dapat menemukan serta mensintesis informasi dari beberapa sumber secara efektif. Untuk hasil penelitian yang optimal:

1. **Sediakan kriteria kesuksesan yang jelas**: Tentukan apa yang merupakan jawaban yang berhasil untuk pertanyaan penelitian Anda

2. **Dorong verifikasi sumber**: Minta Claude untuk memverifikasi informasi di seluruh beberapa sumber

3. **Untuk tugas penelitian kompleks, gunakan pendekatan terstruktur**:

```text Contoh prompt untuk penelitian kompleks
Cari informasi ini dengan cara yang terstruktur. Saat Anda mengumpulkan data, kembangkan beberapa hipotesis yang bersaing. Lacak tingkat kepercayaan Anda dalam catatan kemajuan untuk meningkatkan kalibrasi. Secara teratur self-kritik pendekatan dan rencana Anda. Perbarui file pohon hipotesis atau catatan penelitian untuk mempertahankan informasi dan memberikan transparansi. Pecahkan tugas penelitian kompleks ini secara sistematis.
```

Pendekatan terstruktur ini memungkinkan Claude untuk menemukan dan mensintesis hampir semua informasi dan secara iteratif mengkritik temuannya, tidak peduli ukuran corpus.

### Orkestrasi subagent

Model terbaru Claude menunjukkan kemampuan orkestrasi subagent asli yang jauh lebih baik. Model-model ini dapat mengenali kapan tugas akan mendapat manfaat dari pendelegasian pekerjaan ke subagent khusus dan melakukannya secara proaktif tanpa memerlukan instruksi eksplisit.

Untuk memanfaatkan perilaku ini:

1. **Pastikan alat subagent yang terdefinisi dengan baik**: Memiliki alat subagent yang tersedia dan dijelaskan dalam definisi alat
2. **Biarkan Claude mengorkestrasi secara alami**: Claude akan mendelegasikan dengan tepat tanpa instruksi eksplisit
3. **Perhatikan penggunaan berlebihan**: Claude Opus 4.6 memiliki predileksi yang kuat untuk subagent dan dapat memunculkannya dalam situasi di mana pendekatan yang lebih sederhana dan langsung akan cukup. Misalnya, model dapat memunculkan subagent untuk eksplorasi kode ketika panggilan grep langsung lebih cepat dan cukup.

Jika Anda melihat penggunaan subagent yang berlebihan, tambahkan panduan eksplisit tentang kapan subagent dan tidak layak:

```text Contoh prompt untuk penggunaan subagent
Gunakan subagent ketika tugas dapat berjalan secara paralel, memerlukan konteks terisolasi, atau melibatkan alur kerja independen yang tidak perlu berbagi status. Untuk tugas sederhana, operasi berurutan, pengeditan file tunggal, atau tugas di mana Anda perlu mempertahankan konteks di seluruh langkah, bekerja langsung daripada mendelegasikan.
```

### Rantai prompt kompleks

Dengan adaptive thinking dan orkestrasi subagent, Claude menangani sebagian besar penalaran multi-langkah secara internal. Prompt chaining eksplisit (memecah tugas menjadi panggilan API berurutan) masih berguna ketika Anda perlu memeriksa output perantara atau memberlakukan struktur pipeline tertentu.

Pola chaining paling umum adalah **self-correction**: hasilkan draft → buat Claude meninjau terhadap kriteria → buat Claude menyempurnakan berdasarkan tinjauan. Setiap langkah adalah panggilan API terpisah sehingga Anda dapat mencatat, mengevaluasi, atau bercabang di titik mana pun.

### Kurangi pembuatan file dalam coding agentic

Model terbaru Claude mungkin kadang-kadang membuat file baru untuk tujuan pengujian dan iterasi, terutama saat bekerja dengan kode. Pendekatan ini memungkinkan Claude menggunakan file, terutama skrip python, sebagai 'scratchpad sementara' sebelum menyimpan output akhirnya. Menggunakan file sementara dapat meningkatkan hasil terutama untuk kasus penggunaan coding agentic.

Jika Anda lebih suka meminimalkan pembuatan file baru bersih, Anda dapat menginstruksikan Claude untuk membersihkan setelah dirinya sendiri:

```text Contoh prompt
Jika Anda membuat file baru sementara, skrip, atau file pembantu untuk iterasi, bersihkan file-file ini dengan menghapusnya di akhir tugas.
```

### Overeagerness

Claude Opus 4.5 dan Claude Opus 4.6 memiliki kecenderungan untuk overengineer dengan membuat file ekstra, menambahkan abstraksi yang tidak perlu, atau membangun fleksibilitas yang tidak diminta. Jika Anda melihat perilaku yang tidak diinginkan ini, tambahkan panduan spesifik untuk menjaga solusi tetap minimal.

Misalnya:

```text Contoh prompt untuk meminimalkan overengineering
Hindari over-engineering. Hanya buat perubahan yang secara langsung diminta atau jelas diperlukan. Jaga solusi tetap sederhana dan terfokus:

- Cakupan: Jangan tambahkan fitur, refactor kode, atau buat "perbaikan" di luar apa yang diminta. Perbaikan bug tidak perlu kode sekitarnya dibersihkan. Fitur sederhana tidak perlu konfigurabilitas ekstra.

- Dokumentasi: Jangan tambahkan docstring, komentar, atau anotasi tipe ke kode yang tidak Anda ubah. Hanya tambahkan komentar di mana logika tidak jelas dengan sendirinya.

- Defensive coding: Jangan tambahkan penanganan kesalahan, fallback, atau validasi untuk skenario yang tidak dapat terjadi. Percayai kode internal dan jaminan framework. Hanya validasi di batas sistem (input pengguna, API eksternal).

- Abstraksi: Jangan buat helper, utilitas, atau abstraksi untuk operasi satu kali. Jangan desain untuk persyaratan masa depan hipotetis. Jumlah kompleksitas yang tepat adalah minimum yang diperlukan untuk tugas saat ini.
```

### Hindari fokus pada lulus tes dan hard-coding

Claude kadang-kadang dapat fokus terlalu berat pada membuat tes lulus dengan mengorbankan solusi yang lebih umum, atau dapat menggunakan workaround seperti skrip pembantu untuk refactoring kompleks alih-alih menggunakan alat standar secara langsung. Untuk mencegah perilaku ini dan memastikan solusi yang kuat dan dapat digeneralisasi:

```text Contoh prompt
Silakan tulis solusi berkualitas tinggi dan tujuan umum menggunakan alat standar yang tersedia. Jangan buat skrip pembantu atau workaround untuk menyelesaikan tugas dengan lebih efisien. Implementasikan solusi yang bekerja dengan benar untuk semua input yang valid, bukan hanya kasus tes. Jangan hard-code nilai atau buat solusi yang hanya bekerja untuk input tes tertentu. Sebaliknya, implementasikan logika aktual yang menyelesaikan masalah secara umum.

Fokus pada pemahaman persyaratan masalah dan implementasi algoritma yang benar. Tes ada untuk memverifikasi kebenaran, bukan untuk mendefinisikan solusi. Sediakan implementasi yang berprinsi yang mengikuti praktik terbaik dan prinsip desain perangkat lunak.

Jika tugas tidak masuk akal atau tidak layak, atau jika ada tes yang salah, silakan beri tahu saya daripada bekerja di sekitarnya. Solusi harus kuat, dapat dipertahankan, dan dapat diperluas.
```

### Meminimalkan halusinasi dalam coding agentic

Model terbaru Claude kurang rentan terhadap halusinasi dan memberikan jawaban yang lebih akurat, berdasarkan, dan cerdas berdasarkan kode. Untuk mendorong perilaku ini bahkan lebih dan meminimalkan halusinasi:

```text Contoh prompt
<investigate_before_answering>
Jangan pernah berspekulasi tentang kode yang belum Anda buka. Jika pengguna mereferensikan file tertentu, Anda HARUS membaca file sebelum menjawab. Pastikan untuk menyelidiki dan membaca file yang relevan SEBELUM menjawab pertanyaan tentang codebase. Jangan pernah membuat klaim apa pun tentang kode sebelum menyelidiki kecuali Anda yakin dengan jawaban yang benar - berikan jawaban yang berdasar dan bebas halusinasi.
</investigate_before_answering>
```

## Tips khusus kemampuan

### Kemampuan visi yang ditingkatkan

Claude Opus 4.5 dan Claude Opus 4.6 memiliki kemampuan visi yang ditingkatkan dibandingkan dengan model Claude sebelumnya. Mereka berkinerja lebih baik pada tugas pemrosesan gambar dan ekstraksi data, terutama ketika ada beberapa gambar yang ada dalam konteks. Peningkatan ini terbawa ke penggunaan komputer, di mana model dapat lebih andal menginterpretasi screenshot dan elemen UI. Anda juga dapat menggunakan model ini untuk menganalisis video dengan memecahnya menjadi frame.

Satu teknik yang telah terbukti efektif untuk lebih meningkatkan kinerja adalah memberikan Claude alat crop atau [skill](/docs/id/agents-and-tools/agent-skills/overview). Pengujian telah menunjukkan peningkatan yang konsisten pada evaluasi gambar ketika Claude dapat "zoom" ke wilayah yang relevan dari gambar. Anthropic telah membuat [cookbook untuk alat crop](https://platform.claude.com/cookbook/multimodal-crop-tool).

### Desain frontend

Claude Opus 4.5 dan Claude Opus 4.6 unggul dalam membangun aplikasi web kompleks dan dunia nyata dengan desain frontend yang kuat. Namun, tanpa panduan, model dapat default ke pola generik yang menciptakan apa yang pengguna sebut estetika "AI slop". Untuk membuat frontend yang khas dan kreatif yang mengejutkan dan menyenangkan:

<Tip>
Untuk panduan terperinci tentang meningkatkan desain frontend, lihat posting blog tentang [meningkatkan desain frontend melalui skills](https://www.claude.com/blog/improving-frontend-design-through-skills).
</Tip>

Berikut adalah cuplikan prompt sistem yang dapat Anda gunakan untuk mendorong desain frontend yang lebih baik:

```text Contoh prompt untuk estetika frontend
<frontend_aesthetics>
Anda cenderung bertemu pada output generik, "on distribution". Dalam desain frontend, ini menciptakan apa yang pengguna sebut estetika "AI slop". Hindari ini: buat frontend yang kreatif dan khas yang mengejutkan dan menyenangkan.

Fokus pada:
- Tipografi: Pilih font yang indah, unik, dan menarik. Hindari font generik seperti Arial dan Inter; pilih sebaliknya pilihan yang khas yang meningkatkan estetika frontend.
- Warna & Tema: Berkomitmen pada estetika yang kohesif. Gunakan variabel CSS untuk konsistensi. Warna dominan dengan aksen tajam mengungguli palet yang takut dan merata. Ambil inspirasi dari tema IDE dan estetika budaya.
- Gerakan: Gunakan animasi untuk efek dan micro-interactions. Prioritaskan solusi CSS-only untuk HTML. Gunakan Motion library untuk React ketika tersedia. Fokus pada momen berdampak tinggi: satu pemuatan halaman yang terkoordinasi dengan baik dengan reveal yang terstagger (animation-delay) menciptakan lebih banyak kesenangan daripada micro-interactions yang tersebar.
- Latar Belakang: Ciptakan suasana dan kedalaman daripada default ke warna solid. Lapisan gradien CSS, gunakan pola geometris, atau tambahkan efek kontekstual yang cocok dengan estetika keseluruhan.

Hindari estetika AI yang dihasilkan secara generik:
- Keluarga font yang terlalu sering digunakan (Inter, Roboto, Arial, font sistem)
- Skema warna klise (terutama gradien ungu pada latar belakang putih)
- Tata letak dan pola komponen yang dapat diprediksi
- Desain cookie-cutter yang kurang karakter khusus konteks

Interpretasikan secara kreatif dan buat pilihan yang tidak terduga yang terasa benar-benar dirancang untuk konteks. Variasikan antara tema terang dan gelap, font yang berbeda, estetika yang berbeda. Anda masih cenderung bertemu pada pilihan umum (Space Grotesk, misalnya) di seluruh generasi. Hindari ini: sangat penting bahwa Anda berpikir di luar kotak!
</frontend_aesthetics>
```

Anda juga dapat merujuk ke [definisi skill lengkap](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md).

## Pertimbangan migrasi

Saat bermigrasi ke model Claude 4.6 dari generasi sebelumnya:

1. **Jadilah spesifik tentang perilaku yang diinginkan**: Pertimbangkan menggambarkan dengan tepat apa yang ingin Anda lihat dalam output.

2. **Bingkai instruksi Anda dengan modifier**: Menambahkan modifier yang mendorong Claude untuk meningkatkan kualitas dan detail output dapat membantu membentuk kinerja Claude dengan lebih baik. Misalnya, alih-alih "Buat dashboard analitik", gunakan "Buat dashboard analitik. Sertakan sebanyak mungkin fitur dan interaksi yang relevan. Melampaui dasar untuk membuat implementasi yang lengkap."

3. **Minta fitur spesifik secara eksplisit**: Animasi dan elemen interaktif harus diminta secara eksplisit ketika diinginkan.

4. **Perbarui konfigurasi thinking**: Model Claude 4.6 menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) alih-alih pemikiran manual dengan `budget_tokens`. Gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran.

5. **Migrasi dari respons yang sudah diisi sebelumnya**: Respons yang sudah diisi sebelumnya pada giliran asisten terakhir sudah usang mulai dengan model Claude 4.6. Lihat [Migrating away from prefilled responses](#migrating-away-from-prefilled-responses) untuk panduan terperinci tentang alternatif.

6. **Sesuaikan anti-laziness prompting**: Jika prompt Anda sebelumnya mendorong model untuk lebih menyeluruh atau menggunakan alat lebih agresif, kurangi panduan itu. Model Claude 4.6 jauh lebih proaktif dan dapat overtrigger pada instruksi yang diperlukan untuk model sebelumnya.

Untuk langkah migrasi terperinci, lihat [Migration guide](/docs/id/about-claude/models/migration-guide).

### Bermigrasi dari Claude Sonnet 4.5 ke Claude Sonnet 4.6

Claude Sonnet 4.6 default ke tingkat effort `high`, berbeda dengan Claude Sonnet 4.5 yang tidak memiliki parameter effort. Pertimbangkan menyesuaikan parameter effort saat Anda bermigrasi dari Claude Sonnet 4.5 ke Claude Sonnet 4.6. Jika tidak secara eksplisit diatur, Anda mungkin mengalami latensi yang lebih tinggi dengan tingkat effort default.

**Pengaturan effort yang direkomendasikan:**
- **Medium** untuk sebagian besar aplikasi
- **Low** untuk beban kerja sensitif volume tinggi atau latensi
- Atur anggaran token output maksimal yang besar (64k token direkomendasikan) pada effort medium atau high untuk memberi model ruang untuk berpikir dan bertindak

**Kapan menggunakan Opus 4.7 sebagai gantinya:** Untuk masalah tersulit dan jangka panjang (migrasi kode skala besar, penelitian mendalam, pekerjaan otonom yang diperpanjang), Opus 4.7 tetap menjadi pilihan yang tepat. Sonnet 4.6 dioptimalkan untuk beban kerja di mana turnaround cepat dan efisiensi biaya paling penting.

#### Jika Anda tidak menggunakan extended thinking

Jika Anda tidak menggunakan extended thinking pada Claude Sonnet 4.5, Anda dapat melanjutkan tanpanya pada Claude Sonnet 4.6. Anda harus secara eksplisit mengatur effort ke tingkat yang sesuai untuk kasus penggunaan Anda. Pada effort `low` dengan thinking dinonaktifkan, Anda dapat mengharapkan kinerja yang sama atau lebih baik relatif terhadap Claude Sonnet 4.5 tanpa extended thinking.

```python Python
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    thinking={"type": "disabled"},
    output_config={"effort": "low"},
    messages=[{"role": "user", "content": "..."}],
)
```

#### Jika Anda menggunakan extended thinking

Jika Anda menggunakan extended thinking dengan `budget_tokens` pada Claude Sonnet 4.5, itu masih berfungsi pada Claude Sonnet 4.6 tetapi sudah usang. Migrasi ke [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [parameter effort](/docs/id/build-with-claude/effort).

##### Bermigrasi ke adaptive thinking

Adaptive thinking sangat cocok untuk pola beban kerja berikut:

- **Agen multi-langkah otonom:** agen coding yang mengubah persyaratan menjadi perangkat lunak yang bekerja, pipeline analisis data, dan pencarian bug di mana model berjalan secara independen di seluruh banyak langkah. Adaptive thinking memungkinkan model mengkalibrasi penalarannya per langkah, tetap di jalur di atas lintasan yang lebih panjang. Untuk beban kerja ini, mulai dengan effort `high`. Jika latensi atau penggunaan token menjadi perhatian, skala turun ke `medium`.
- **Agen penggunaan komputer:** Claude Sonnet 4.6 mencapai akurasi terbaik di kelasnya pada evaluasi penggunaan komputer menggunakan mode adaptive.
- **Beban kerja bimodal:** campuran tugas mudah dan sulit di mana adaptive melewati pemikiran pada query sederhana dan bernalar secara mendalam pada query kompleks.

Saat menggunakan adaptive thinking, evaluasi effort `medium` dan `high` pada tugas Anda. Tingkat yang tepat tergantung pada tradeoff beban kerja Anda antara kualitas, latensi, dan penggunaan token.

```python Python nocheck
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[{"role": "user", "content": "..."}],
)
```

##### Menjaga budget_tokens selama migrasi

Jika Anda perlu menjaga `budget_tokens` sementara saat bermigrasi, anggaran sekitar 16k token memberikan ruang untuk masalah yang lebih sulit tanpa risiko penggunaan token yang liar. Konfigurasi ini sudah usang dan akan dihapus dalam rilis model masa depan.

**Untuk kasus penggunaan coding** (coding agentic, alur kerja tool-heavy, code generation), mulai dengan effort `medium`:

```python Python nocheck
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16384,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "..."}],
)
```

**Untuk kasus penggunaan chat dan non-coding** (chat, content generation, search, classification), mulai dengan effort `low`:

```python Python nocheck
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "low"},
    messages=[{"role": "user", "content": "..."}],
)
```