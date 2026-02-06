---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: c09ff42ba9b57b1acf052c8133fa7c257c9735753f59bd7ea6e205282c5a7c12
---

# Praktik terbaik prompting

Teknik prompt engineering untuk model Claude terbaru, termasuk Claude Opus 4.6, Claude Sonnet 4.5, dan Claude Haiku 4.5.

---

Panduan ini menyediakan teknik prompt engineering untuk model Claude terbaru, termasuk Claude Opus 4.6, Claude Sonnet 4.5, dan Claude Haiku 4.5. Model-model ini telah dilatih untuk mengikuti instruksi dengan lebih presisi dibandingkan generasi model Claude sebelumnya.
<Tip>
  Untuk gambaran umum tentang kemampuan model, lihat [ringkasan model](/docs/id/about-claude/models/overview). Untuk detail tentang apa yang baru di Claude 4.6, lihat [Apa yang baru di Claude 4.6](/docs/id/about-claude/models/whats-new-claude-4-6). Untuk panduan migrasi, lihat [Panduan migrasi](/docs/id/about-claude/models/migration-guide).
</Tip>

## Prinsip umum

### Jadilah eksplisit dengan instruksi Anda

Claude merespons dengan baik terhadap instruksi yang jelas dan eksplisit. Menjadi spesifik tentang output yang Anda inginkan dapat membantu meningkatkan hasil. Jika Anda menginginkan perilaku "di atas dan seterusnya", minta secara eksplisit daripada mengandalkan model untuk menyimpulkan ini dari prompt yang samar.

<section title="Contoh: Membuat dasbor analitik">

**Kurang efektif:**
```text
Buat dasbor analitik
```

**Lebih efektif:**
```text
Buat dasbor analitik. Sertakan sebanyak mungkin fitur dan interaksi yang relevan. Melampaui dasar-dasar untuk membuat implementasi yang lengkap.
```

</section>

### Tambahkan konteks untuk meningkatkan kinerja

Memberikan konteks atau motivasi di balik instruksi Anda, seperti menjelaskan kepada Claude mengapa perilaku tersebut penting, dapat membantu Claude lebih memahami tujuan Anda dan memberikan respons yang lebih tertarget.

<section title="Contoh: Preferensi pemformatan">

**Kurang efektif:**
```text
JANGAN PERNAH gunakan elipsis
```

**Lebih efektif:**
```text
Respons Anda akan dibaca oleh mesin text-to-speech, jadi jangan pernah gunakan elipsis karena mesin text-to-speech tidak akan tahu cara mengucapkannya.
```

</section>

Claude cukup pintar untuk menggeneralisasi dari penjelasan tersebut.

### Berhati-hatilah dengan contoh & detail

Claude memperhatikan detail dan contoh dengan cermat sebagai bagian dari kemampuan mengikuti instruksi yang presisi. Pastikan bahwa contoh Anda selaras dengan perilaku yang ingin Anda dorong dan meminimalkan perilaku yang ingin Anda hindari.

### Penalaran jangka panjang dan pelacakan status

Model Claude terbaru unggul dalam tugas penalaran jangka panjang dengan kemampuan pelacakan status yang luar biasa. Claude mempertahankan orientasi di seluruh sesi yang diperpanjang dengan fokus pada kemajuan inkremental—membuat kemajuan yang stabil pada beberapa hal sekaligus daripada mencoba melakukan semuanya sekaligus. Kemampuan ini terutama muncul di seluruh beberapa jendela konteks atau iterasi tugas, di mana Claude dapat bekerja pada tugas yang kompleks, menyimpan status, dan melanjutkan dengan jendela konteks yang segar.

#### Kesadaran konteks dan alur kerja multi-jendela

Model Claude Opus 4.6 dan Claude 4.5 menampilkan [kesadaran konteks](/docs/id/build-with-claude/context-windows#context-awareness-in-claude-sonnet-45-and-haiku-45), memungkinkan model untuk melacak jendela konteks yang tersisa (yaitu "anggaran token") di seluruh percakapan. Ini memungkinkan Claude untuk menjalankan tugas dan mengelola konteks lebih efektif dengan memahami berapa banyak ruang yang dimilikinya untuk bekerja.

**Mengelola batas konteks:**

Jika Anda menggunakan Claude dalam harness agen yang memadatkan konteks atau memungkinkan menyimpan konteks ke file eksternal (seperti di Claude Code), kami menyarankan menambahkan informasi ini ke prompt Anda sehingga Claude dapat berperilaku sesuai. Jika tidak, Claude mungkin kadang-kadang secara alami mencoba membungkus pekerjaan saat mendekati batas konteks. Di bawah ini adalah contoh prompt:

```text Contoh prompt
Jendela konteks Anda akan secara otomatis dipadatkan saat mendekati batasnya, memungkinkan Anda untuk terus bekerja tanpa batas dari tempat Anda berhenti. Oleh karena itu, jangan hentikan tugas lebih awal karena kekhawatiran anggaran token. Saat Anda mendekati batas anggaran token, simpan kemajuan dan status saat ini ke memori sebelum jendela konteks disegarkan. Selalu seproaktif dan otonom mungkin dan selesaikan tugas sepenuhnya, bahkan jika akhir anggaran Anda akan segera tiba. Jangan pernah secara artifisial menghentikan tugas apa pun lebih awal terlepas dari konteks yang tersisa.
```

[Alat memori](/docs/id/agents-and-tools/tool-use/memory-tool) berpasangan secara alami dengan kesadaran konteks untuk transisi konteks yang mulus.

#### Alur kerja jendela konteks multi

Untuk tugas yang mencakup beberapa jendela konteks:

1. **Gunakan prompt yang berbeda untuk jendela konteks pertama**: Gunakan jendela konteks pertama untuk menyiapkan kerangka kerja (tulis tes, buat skrip setup), kemudian gunakan jendela konteks di masa depan untuk mengulangi daftar todo.

2. **Buat model menulis tes dalam format terstruktur**: Minta Claude untuk membuat tes sebelum memulai pekerjaan dan lacak dalam format terstruktur (misalnya, `tests.json`). Ini mengarah pada kemampuan jangka panjang yang lebih baik untuk mengulangi. Ingatkan Claude tentang pentingnya tes: "Tidak dapat diterima untuk menghapus atau mengedit tes karena ini dapat menyebabkan fungsionalitas yang hilang atau bermasalah."

3. **Siapkan alat kualitas hidup**: Dorong Claude untuk membuat skrip setup (misalnya, `init.sh`) untuk memulai server dengan baik, menjalankan suite tes, dan linter. Ini mencegah pekerjaan berulang saat melanjutkan dari jendela konteks yang segar.

4. **Memulai dari awal vs pemadatan**: Ketika jendela konteks dihapus, pertimbangkan untuk memulai dengan jendela konteks yang benar-benar baru daripada menggunakan pemadatan. Model Claude terbaru sangat efektif dalam menemukan status dari sistem file lokal. Dalam beberapa kasus, Anda mungkin ingin memanfaatkan ini daripada pemadatan. Jadilah preskriptif tentang cara memulainya:
   - "Panggil pwd; Anda hanya dapat membaca dan menulis file di direktori ini."
   - "Tinjau progress.txt, tests.json, dan git logs."
   - "Jalankan secara manual melalui tes integrasi fundamental sebelum melanjutkan untuk mengimplementasikan fitur baru."

5. **Sediakan alat verifikasi**: Seiring dengan bertambahnya panjang tugas otonom, Claude perlu memverifikasi kebenaran tanpa umpan balik manusia yang berkelanjutan. Alat seperti server Playwright MCP atau kemampuan penggunaan komputer untuk menguji UI sangat membantu.

6. **Dorong penggunaan konteks yang lengkap**: Minta Claude untuk menyelesaikan komponen secara efisien sebelum melanjutkan:

```text Contoh prompt
Ini adalah tugas yang sangat panjang, jadi mungkin bermanfaat untuk merencanakan pekerjaan Anda dengan jelas. Disarankan untuk menghabiskan seluruh konteks output Anda mengerjakan tugas - pastikan saja Anda tidak kehabisan konteks dengan pekerjaan yang belum dikomit yang signifikan. Terus bekerja secara sistematis sampai Anda menyelesaikan tugas ini.
```

#### Praktik terbaik manajemen status

- **Gunakan format terstruktur untuk data status**: Saat melacak informasi terstruktur (seperti hasil tes atau status tugas), gunakan JSON atau format terstruktur lainnya untuk membantu Claude memahami persyaratan skema
- **Gunakan teks tidak terstruktur untuk catatan kemajuan**: Catatan kemajuan bentuk bebas bekerja dengan baik untuk melacak kemajuan umum dan konteks
- **Gunakan git untuk pelacakan status**: Git menyediakan log tentang apa yang telah dilakukan dan checkpoint yang dapat dipulihkan. Model Claude terbaru berkinerja sangat baik dalam menggunakan git untuk melacak status di seluruh beberapa sesi.
- **Tekankan kemajuan inkremental**: Secara eksplisit minta Claude untuk melacak kemajuannya dan fokus pada pekerjaan inkremental

<section title="Contoh: Pelacakan status">

```json
// File status terstruktur (tests.json)
{
  "tests": [
    {"id": 1, "name": "authentication_flow", "status": "passing"},
    {"id": 2, "name": "user_management", "status": "failing"},
    {"id": 3, "name": "api_endpoints", "status": "not_started"}
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
- Memperbaiki validasi token autentikasi
- Memperbarui model pengguna untuk menangani kasus tepi
- Berikutnya: selidiki kegagalan tes user_management (tes #2)
- Catatan: Jangan hapus tes karena ini dapat menyebabkan fungsionalitas yang hilang
```

</section>

### Gaya komunikasi

Model Claude terbaru memiliki gaya komunikasi yang lebih ringkas dan alami dibandingkan dengan model sebelumnya:

- **Lebih langsung dan berdasarkan fakta**: Memberikan laporan kemajuan berbasis fakta daripada pembaruan yang merayakan diri sendiri
- **Lebih percakapan**: Sedikit lebih lancar dan percakapan, kurang seperti mesin
- **Kurang bertele-tele**: Mungkin melewatkan ringkasan terperinci untuk efisiensi kecuali diminta sebaliknya

Gaya komunikasi ini secara akurat mencerminkan apa yang telah dicapai tanpa elaborasi yang tidak perlu.

## Panduan untuk situasi spesifik

### Seimbangkan verbositas

Model Claude terbaru cenderung ke arah efisiensi dan mungkin melewatkan ringkasan verbal setelah panggilan alat, melompat langsung ke tindakan berikutnya. Meskipun ini menciptakan alur kerja yang efisien, Anda mungkin lebih suka visibilitas lebih besar ke dalam proses penalaran.

Jika Anda ingin Claude memberikan pembaruan saat bekerja:

```text Contoh prompt
Setelah menyelesaikan tugas yang melibatkan penggunaan alat, berikan ringkasan cepat tentang pekerjaan yang telah Anda lakukan.
```

### Pola penggunaan alat

Model Claude terbaru dilatih untuk mengikuti instruksi yang presisi dan mendapat manfaat dari arahan eksplisit untuk menggunakan alat tertentu. Jika Anda mengatakan "bisakah Anda menyarankan beberapa perubahan," Claude kadang-kadang akan memberikan saran daripada mengimplementasikannya—bahkan jika membuat perubahan mungkin apa yang Anda maksudkan.

Agar Claude mengambil tindakan, jadilah lebih eksplisit:

<section title="Contoh: Instruksi eksplisit">

**Kurang efektif (Claude hanya akan menyarankan):**
```text
Bisakah Anda menyarankan beberapa perubahan untuk meningkatkan fungsi ini?
```

**Lebih efektif (Claude akan membuat perubahan):**
```text
Ubah fungsi ini untuk meningkatkan kinerjanya.
```

Atau:
```text
Buat pengeditan ini pada alur autentikasi.
```

</section>

Untuk membuat Claude lebih proaktif dalam mengambil tindakan secara default, Anda dapat menambahkan ini ke prompt sistem Anda:

```text Contoh prompt untuk tindakan proaktif
<default_to_action>
Secara default, implementasikan perubahan daripada hanya menyarankannya. Jika niat pengguna tidak jelas, simpulkan tindakan yang paling berguna dan lanjutkan, gunakan alat untuk menemukan detail yang hilang daripada menebak. Coba simpulkan niat pengguna tentang apakah panggilan alat (misalnya pengeditan atau pembacaan file) dimaksudkan atau tidak, dan bertindak sesuai.
</default_to_action>
```

Di sisi lain, jika Anda ingin model lebih ragu-ragu secara default, kurang cenderung melompat langsung ke implementasi, dan hanya mengambil tindakan jika diminta, Anda dapat mengarahkan perilaku ini dengan prompt seperti di bawah:

```text Contoh prompt untuk tindakan konservatif
<do_not_act_before_instructions>
Jangan melompat ke implementasi atau mengubah file kecuali jelas diperintahkan untuk membuat perubahan. Ketika niat pengguna ambigu, default untuk memberikan informasi, melakukan penelitian, dan memberikan rekomendasi daripada mengambil tindakan. Hanya lanjutkan dengan pengeditan, modifikasi, atau implementasi ketika pengguna secara eksplisit memintanya.
</do_not_act_before_instructions>
```

### Penggunaan alat dan pemicu

Claude Opus 4.5 dan Claude Opus 4.6 lebih responsif terhadap prompt sistem daripada model sebelumnya. Jika prompt Anda dirancang untuk mengurangi undertriggering pada alat atau keterampilan, model ini mungkin sekarang overtrigger. Solusinya adalah mengurangi bahasa yang agresif. Di mana Anda mungkin mengatakan "KRITIS: Anda HARUS menggunakan alat ini ketika...", Anda dapat menggunakan prompting yang lebih normal seperti "Gunakan alat ini ketika...".

### Menyeimbangkan otonomi dan keamanan

Tanpa panduan, Claude Opus 4.6 mungkin mengambil tindakan yang sulit untuk dibalikkan atau mempengaruhi sistem bersama, seperti menghapus file, force-push, atau memposting ke layanan eksternal. Jika Anda ingin Claude Opus 4.6 mengonfirmasi sebelum mengambil tindakan yang berpotensi berisiko, tambahkan panduan ke prompt Anda:

```text Contoh prompt
Pertimbangkan reversibilitas dan dampak potensial dari tindakan Anda. Anda didorong untuk mengambil tindakan lokal yang dapat dibalikkan seperti mengedit file atau menjalankan tes, tetapi untuk tindakan yang sulit dibalikkan, mempengaruhi sistem bersama, atau dapat merusak, minta pengguna sebelum melanjutkan.

Contoh tindakan yang memerlukan konfirmasi:
- Operasi destruktif: menghapus file atau cabang, menjatuhkan tabel database, rm -rf
- Operasi yang sulit dibalikkan: git push --force, git reset --hard, mengubah komit yang dipublikasikan
- Operasi yang terlihat oleh orang lain: mendorong kode, berkomentar pada PR/masalah, mengirim pesan, memodifikasi infrastruktur bersama

Ketika menghadapi hambatan, jangan gunakan tindakan destruktif sebagai jalan pintas. Misalnya, jangan lewati pemeriksaan keamanan (misalnya --no-verify) atau buang file yang tidak dikenal yang mungkin merupakan pekerjaan yang sedang berlangsung.
```

### Overthinking dan kesempurnaan yang berlebihan

Claude Opus 4.6 melakukan eksplorasi awal yang jauh lebih signifikan daripada model sebelumnya, terutama pada pengaturan `effort` yang lebih tinggi. Pekerjaan awal ini sering membantu mengoptimalkan hasil akhir, tetapi model mungkin mengumpulkan konteks yang luas atau mengejar beberapa utas penelitian tanpa diminta. Jika prompt Anda sebelumnya mendorong model untuk lebih menyeluruh, Anda harus menyesuaikan panduan itu untuk Claude Opus 4.6:

- **Ganti default blanket dengan instruksi yang lebih tertarget.** Alih-alih "Default untuk menggunakan \[alat\]," tambahkan panduan seperti "Gunakan \[alat\] ketika itu akan meningkatkan pemahaman Anda tentang masalah."
- **Hapus over-prompting.** Alat yang undertriggered di model sebelumnya kemungkinan akan dipicu dengan tepat sekarang. Instruksi seperti "Jika ragu, gunakan \[alat\]" akan menyebabkan overtriggering.
- **Gunakan effort sebagai fallback.** Jika Claude terus menjadi terlalu agresif, gunakan pengaturan yang lebih rendah untuk `effort`.

Dalam beberapa kasus, Claude Opus 4.6 mungkin berpikir secara ekstensif, yang dapat menginflasi token pemikiran dan memperlambat respons. Jika perilaku ini tidak diinginkan, Anda dapat menambahkan instruksi eksplisit untuk membatasi penalarannya, atau Anda dapat menurunkan pengaturan `effort` untuk mengurangi pemikiran dan penggunaan token secara keseluruhan.

```text Contoh prompt
Ketika Anda memutuskan cara mendekati masalah, pilih pendekatan dan berkomitmen padanya. Hindari mengunjungi kembali keputusan kecuali Anda menemukan informasi baru yang secara langsung bertentangan dengan penalaran Anda. Jika Anda menimbang dua pendekatan, pilih satu dan lihat melaluinya. Anda selalu dapat mengubah arah nanti jika pendekatan yang dipilih gagal.
```

### Kontrol format respons

Ada beberapa cara yang kami temukan sangat efektif dalam mengarahkan pemformatan output:

1. **Katakan kepada Claude apa yang harus dilakukan daripada apa yang tidak boleh dilakukan**

   - Alih-alih: "Jangan gunakan markdown dalam respons Anda"
   - Coba: "Respons Anda harus terdiri dari paragraf prosa yang mengalir dengan mulus."

2. **Gunakan indikator format XML**

   - Coba: "Tulis bagian prosa dari respons Anda dalam tag \<smoothly_flowing_prose_paragraphs\>."

3. **Cocokkan gaya prompt Anda dengan output yang diinginkan**

   Gaya pemformatan yang digunakan dalam prompt Anda dapat mempengaruhi gaya respons Claude. Jika Anda masih mengalami masalah steerability dengan pemformatan output, kami merekomendasikan sebaik mungkin mencocokkan gaya prompt Anda dengan gaya output yang diinginkan. Misalnya, menghapus markdown dari prompt Anda dapat mengurangi volume markdown dalam output.

4. **Gunakan prompt terperinci untuk preferensi pemformatan spesifik**

   Untuk kontrol lebih besar atas penggunaan markdown dan pemformatan, berikan panduan eksplisit:

```text Contoh prompt untuk meminimalkan markdown
<avoid_excessive_markdown_and_bullet_points>
Saat menulis laporan, dokumen, penjelasan teknis, analisis, atau konten bentuk panjang apa pun, tulis dalam prosa yang jelas dan mengalir menggunakan paragraf dan kalimat lengkap. Gunakan jeda paragraf standar untuk organisasi dan cadangkan markdown terutama untuk `inline code`, blok kode (```...```), dan heading sederhana (###, dan ###). Hindari menggunakan **bold** dan *italics*.

JANGAN gunakan daftar terurut (1. ...) atau daftar tidak terurut (*) kecuali : a) Anda menyajikan item yang benar-benar diskrit di mana format daftar adalah pilihan terbaik, atau b) pengguna secara eksplisit meminta daftar atau peringkat

Alih-alih membuat daftar item dengan bullet atau angka, gabungkan secara alami ke dalam kalimat. Panduan ini terutama berlaku untuk penulisan teknis. Menggunakan prosa daripada pemformatan yang berlebihan akan meningkatkan kepuasan pengguna. JANGAN PERNAH menampilkan serangkaian poin bullet yang terlalu pendek.

Tujuan Anda adalah teks yang dapat dibaca dan mengalir yang memandu pembaca secara alami melalui ide-ide daripada memfragmentasi informasi menjadi poin-poin terisolasi.
</avoid_excessive_markdown_and_bullet_points>
```

### Penelitian dan pengumpulan informasi

Model Claude terbaru menunjukkan kemampuan pencarian agentic yang luar biasa dan dapat menemukan dan mensintesis informasi dari berbagai sumber secara efektif. Untuk hasil penelitian yang optimal:

1. **Berikan kriteria kesuksesan yang jelas**: Tentukan apa yang merupakan jawaban yang berhasil untuk pertanyaan penelitian Anda

2. **Dorong verifikasi sumber**: Minta Claude untuk memverifikasi informasi di berbagai sumber

3. **Untuk tugas penelitian yang kompleks, gunakan pendekatan terstruktur**:

```text Contoh prompt untuk penelitian kompleks
Cari informasi ini dengan cara yang terstruktur. Saat Anda mengumpulkan data, kembangkan beberapa hipotesis yang bersaing. Lacak tingkat kepercayaan Anda dalam catatan kemajuan untuk meningkatkan kalibrasi. Secara teratur mengkritik diri sendiri pendekatan dan rencana Anda. Perbarui file pohon hipotesis atau catatan penelitian untuk mempertahankan informasi dan memberikan transparansi. Pecahkan tugas penelitian kompleks ini secara sistematis.
```

Pendekatan terstruktur ini memungkinkan Claude untuk menemukan dan mensintesis praktis setiap bagian informasi dan secara iteratif mengkritik temuannya, tidak peduli ukuran corpus.

### Orkestrasi subagen

Model Claude terbaru menunjukkan kemampuan orkestrasi subagen asli yang secara signifikan ditingkatkan. Model-model ini dapat mengenali ketika tugas akan mendapat manfaat dari pendelegasian pekerjaan ke subagen khusus dan melakukannya secara proaktif tanpa memerlukan instruksi eksplisit.

Untuk memanfaatkan perilaku ini:

1. **Pastikan alat subagen yang terdefinisi dengan baik**: Memiliki alat subagen yang tersedia dan dijelaskan dalam definisi alat
2. **Biarkan Claude mengorkestra secara alami**: Claude akan mendelegasikan dengan tepat tanpa instruksi eksplisit
3. **Perhatikan penggunaan berlebihan**: Claude Opus 4.6 memiliki kecenderungan kuat untuk subagen dan mungkin memunculkannya dalam situasi di mana pendekatan yang lebih sederhana dan langsung akan cukup. Misalnya, model mungkin memunculkan subagen untuk eksplorasi kode ketika panggilan grep langsung lebih cepat dan cukup.

Jika Anda melihat penggunaan subagen yang berlebihan, tambahkan panduan eksplisit tentang kapan subagen dan kapan tidak layak:

```text Contoh prompt untuk penggunaan subagen
Gunakan subagen ketika tugas dapat berjalan secara paralel, memerlukan konteks terisolasi, atau melibatkan aliran kerja independen yang tidak perlu berbagi status. Untuk tugas sederhana, operasi sekuensial, pengeditan file tunggal, atau tugas di mana Anda perlu mempertahankan konteks di seluruh langkah, bekerja langsung daripada mendelegasikan.
```

### Pengetahuan diri model

Jika Anda ingin Claude mengidentifikasi dirinya dengan benar dalam aplikasi Anda atau menggunakan string API tertentu:

```text Contoh prompt untuk identitas model
Asisten adalah Claude, dibuat oleh Anthropic. Model saat ini adalah Claude Opus 4.6.
```

Untuk aplikasi bertenaga LLM yang perlu menentukan string model:

```text Contoh prompt untuk string model
Ketika LLM diperlukan, silakan default ke Claude Opus 4.6 kecuali pengguna meminta sebaliknya. String model yang tepat untuk Claude Opus 4.6 adalah claude-opus-4-6.
```

### Sensitivitas pemikiran

Ketika pemikiran yang diperpanjang dinonaktifkan, Claude Opus 4.5 sangat sensitif terhadap kata "think" dan variannya. Kami merekomendasikan mengganti "think" dengan kata-kata alternatif yang menyampaikan makna serupa, seperti "consider," "believe," dan "evaluate."

### Manfaatkan kemampuan pemikiran & pemikiran yang disisipi

Model Claude terbaru menawarkan kemampuan pemikiran yang dapat sangat membantu untuk tugas yang melibatkan refleksi setelah penggunaan alat atau penalaran multi-langkah yang kompleks. Anda dapat memandu pemikiran awal atau disisipi untuk hasil yang lebih baik.

Claude Opus 4.6 menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`), di mana Claude secara dinamis memutuskan kapan dan berapa banyak untuk berpikir. Claude mengkalibrasi pemikirannya berdasarkan dua faktor: parameter `effort` dan kompleksitas kueri. Effort yang lebih tinggi membangkitkan lebih banyak pemikiran, dan kueri yang lebih kompleks juga demikian. Pada kueri yang lebih mudah yang tidak memerlukan pemikiran, model merespons secara langsung. Dalam evaluasi internal, adaptive thinking secara andal mendorong kinerja yang lebih baik daripada extended thinking, dan kami merekomendasikan untuk pindah ke adaptive thinking untuk mendapatkan respons yang paling cerdas. Model yang lebih lama menggunakan mode pemikiran manual dengan `budget_tokens`.

Anda dapat memandu perilaku pemikiran Claude:

```text Contoh prompt
Setelah menerima hasil alat, hati-hati mencerminkan kualitas mereka dan menentukan langkah optimal berikutnya sebelum melanjutkan. Gunakan pemikiran Anda untuk merencanakan dan mengulangi berdasarkan informasi baru ini, kemudian ambil tindakan berikutnya yang terbaik.
```

Perilaku pemicu untuk adaptive thinking dapat diprompt. Jika Anda menemukan model berpikir lebih sering daripada yang Anda inginkan, yang dapat terjadi dengan prompt sistem yang besar atau kompleks, tambahkan panduan untuk mengarahkannya:

```text Contoh prompt
Extended thinking menambah latensi dan hanya boleh digunakan ketika itu akan secara bermakna meningkatkan kualitas jawaban - biasanya untuk masalah yang memerlukan penalaran multi-langkah. Ketika ragu, respons langsung.
```

Jika Anda bermigrasi dari [extended thinking](/docs/id/build-with-claude/extended-thinking) dengan `budget_tokens`, ganti konfigurasi pemikiran Anda dan pindahkan kontrol anggaran ke `effort`:

```python Sebelum (extended thinking, model yang lebih lama)
client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=64000,
    thinking={"type": "enabled", "budget_tokens": 32000},
    messages=[{"role": "user", "content": "..."}],
)
```

```python Sesudah (adaptive thinking)
client.messages.create(
    model="claude-opus-4-6",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},  # atau max, medium, low
    messages=[{"role": "user", "content": "..."}],
)
```

Jika Anda tidak menggunakan extended thinking, tidak ada perubahan yang diperlukan. Pemikiran dimatikan secara default ketika Anda menghilangkan parameter `thinking`.

<Info>
  Untuk informasi lebih lanjut tentang kemampuan pemikiran, lihat [Extended thinking](/docs/id/build-with-claude/extended-thinking) dan [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking).
</Info>

### Pembuatan dokumen

Model Claude terbaru unggul dalam membuat presentasi, animasi, dan dokumen visual dengan kilau kreatif yang mengesankan dan mengikuti instruksi yang kuat. Model menghasilkan output yang dipoles dan dapat digunakan pada percobaan pertama dalam sebagian besar kasus.

Untuk hasil terbaik dengan pembuatan dokumen:

```text Contoh prompt
Buat presentasi profesional tentang [topic]. Sertakan elemen desain yang bijaksana, hierarki visual, dan animasi yang menarik jika sesuai.
```

### Kemampuan visi yang ditingkatkan

Claude Opus 4.5 dan Claude Opus 4.6 memiliki kemampuan visi yang ditingkatkan dibandingkan dengan model Claude sebelumnya. Mereka berkinerja lebih baik pada tugas pemrosesan gambar dan ekstraksi data, terutama ketika ada beberapa gambar yang ada dalam konteks. Peningkatan ini terbawa ke penggunaan komputer, di mana model dapat lebih andal menafsirkan tangkapan layar dan elemen UI. Anda juga dapat menggunakan model ini untuk menganalisis video dengan memecahnya menjadi frame.

Satu teknik yang kami temukan efektif untuk lebih meningkatkan kinerja adalah memberikan Claude alat crop atau [skill](/docs/id/agents-and-tools/agent-skills/overview). Kami telah melihat peningkatan yang konsisten pada evaluasi gambar ketika Claude dapat "zoom" ke wilayah yang relevan dari gambar. Kami telah menyusun cookbook untuk alat crop [di sini](https://platform.claude.com/cookbook/multimodal-crop-tool).

### Optimalkan panggilan alat paralel

Model Claude terbaru unggul dalam eksekusi alat paralel. Model-model ini akan:

- Menjalankan beberapa pencarian spekulatif selama penelitian
- Membaca beberapa file sekaligus untuk membangun konteks lebih cepat
- Menjalankan perintah bash secara paralel (yang bahkan dapat membuat bottleneck kinerja sistem)

Perilaku ini mudah diarahkan. Meskipun model memiliki tingkat keberhasilan yang tinggi dalam panggilan alat paralel tanpa prompting, Anda dapat meningkatkan ini menjadi ~100% atau menyesuaikan tingkat agresivitas:

```text Contoh prompt untuk efisiensi paralel maksimum
<use_parallel_tool_calls>
Jika Anda bermaksud memanggil beberapa alat dan tidak ada ketergantungan antara panggilan alat, buat semua panggilan alat independen secara paralel. Prioritaskan memanggil alat secara bersamaan kapan pun tindakan dapat dilakukan secara paralel daripada secara berurutan. Misalnya, saat membaca 3 file, jalankan 3 panggilan alat secara paralel untuk membaca ketiga file ke dalam konteks pada waktu yang sama. Maksimalkan penggunaan panggilan alat paralel jika memungkinkan untuk meningkatkan kecepatan dan efisiensi. Namun, jika beberapa panggilan alat bergantung pada panggilan sebelumnya untuk menginformasikan nilai dependen seperti parameter, JANGAN panggil alat ini secara paralel dan sebagai gantinya panggil secara berurutan. Jangan pernah gunakan placeholder atau tebak parameter yang hilang dalam panggilan alat.
</use_parallel_tool_calls>
```

```text Contoh prompt untuk mengurangi eksekusi paralel
Jalankan operasi secara berurutan dengan jeda singkat antara setiap langkah untuk memastikan stabilitas.
```

### Kurangi pembuatan file dalam pengkodean agentic

Model Claude terbaru mungkin kadang-kadang membuat file baru untuk tujuan pengujian dan iterasi, terutama saat bekerja dengan kode. Pendekatan ini memungkinkan Claude menggunakan file, terutama skrip python, sebagai 'scratchpad sementara' sebelum menyimpan output akhirnya. Menggunakan file sementara dapat meningkatkan hasil terutama untuk kasus penggunaan pengkodean agentic.

Jika Anda lebih suka meminimalkan pembuatan file baru bersih, Anda dapat menginstruksikan Claude untuk membersihkan setelah dirinya sendiri:

```text Contoh prompt
Jika Anda membuat file baru sementara, skrip, atau file pembantu untuk iterasi, bersihkan file ini dengan menghapusnya di akhir tugas.
```

### Overeagerness

Claude Opus 4.5 dan Claude Opus 4.6 memiliki kecenderungan untuk overengineer dengan membuat file ekstra, menambahkan abstraksi yang tidak perlu, atau membangun fleksibilitas yang tidak diminta. Jika Anda melihat perilaku yang tidak diinginkan ini, tambahkan panduan spesifik untuk menjaga solusi tetap minimal.

Misalnya:

```text Contoh prompt untuk meminimalkan overengineering
Hindari over-engineering. Hanya buat perubahan yang secara langsung diminta atau jelas diperlukan. Jaga solusi tetap sederhana dan terfokus:

- Cakupan: Jangan tambahkan fitur, refactor kode, atau buat "perbaikan" di luar apa yang diminta. Perbaikan bug tidak perlu kode sekitarnya dibersihkan. Fitur sederhana tidak perlu konfigurabilitas ekstra.

- Dokumentasi: Jangan tambahkan docstring, komentar, atau anotasi tipe ke kode yang tidak Anda ubah. Hanya tambahkan komentar di mana logika tidak jelas dengan sendirinya.

- Pengkodean defensif: Jangan tambahkan penanganan kesalahan, fallback, atau validasi untuk skenario yang tidak dapat terjadi. Percayai kode internal dan jaminan framework. Hanya validasi di batas sistem (input pengguna, API eksternal).

- Abstraksi: Jangan buat helper, utilitas, atau abstraksi untuk operasi satu kali. Jangan desain untuk persyaratan masa depan hipotetis. Jumlah kompleksitas yang tepat adalah minimum yang diperlukan untuk tugas saat ini.
```

### Desain frontend

Claude Opus 4.5 dan Claude Opus 4.6 unggul dalam membangun aplikasi web yang kompleks dan dunia nyata dengan desain frontend yang kuat. Namun, tanpa panduan, model dapat default ke pola generik yang menciptakan apa yang pengguna sebut estetika "AI slop". Untuk membuat frontend yang khas dan kreatif yang mengejutkan dan menyenangkan:

<Tip>
Untuk panduan terperinci tentang meningkatkan desain frontend, lihat posting blog kami tentang [meningkatkan desain frontend melalui skills](https://www.claude.com/blog/improving-frontend-design-through-skills).
</Tip>

Berikut adalah cuplikan prompt sistem yang dapat Anda gunakan untuk mendorong desain frontend yang lebih baik:

```text Contoh prompt untuk estetika frontend
<frontend_aesthetics>
Anda cenderung bertemu pada output generik, "on distribution". Dalam desain frontend, ini menciptakan apa yang pengguna sebut estetika "AI slop". Hindari ini: buat frontend yang kreatif dan khas yang mengejutkan dan menyenangkan.

Fokus pada:
- Tipografi: Pilih font yang indah, unik, dan menarik. Hindari font generik seperti Arial dan Inter; pilih sebagai gantinya pilihan yang khas yang meningkatkan estetika frontend.
- Warna & Tema: Berkomitmen pada estetika yang kohesif. Gunakan variabel CSS untuk konsistensi. Warna dominan dengan aksen tajam mengungguli palet yang takut dan terdistribusi secara merata. Tarik dari tema IDE dan estetika budaya untuk inspirasi.
- Gerakan: Gunakan animasi untuk efek dan micro-interactions. Prioritaskan solusi CSS-only untuk HTML. Gunakan Motion library untuk React ketika tersedia. Fokus pada momen berdampak tinggi: satu pemuatan halaman yang terorkestra dengan baik dengan reveal yang terstagger (animation-delay) menciptakan lebih banyak kegembiraan daripada micro-interactions yang tersebar.
- Latar belakang: Ciptakan suasana dan kedalaman daripada default ke warna solid. Lapisan gradien CSS, gunakan pola geometris, atau tambahkan efek kontekstual yang cocok dengan estetika keseluruhan.

Hindari estetika AI yang dihasilkan secara generik:
- Keluarga font yang terlalu digunakan (Inter, Roboto, Arial, font sistem)
- Skema warna klise (terutama gradien ungu pada latar belakang putih)
- Tata letak dan pola komponen yang dapat diprediksi
- Desain cookie-cutter yang kekurangan karakter khusus konteks

Interpretasikan secara kreatif dan buat pilihan yang tidak terduga yang terasa benar-benar dirancang untuk konteks. Variasikan antara tema terang dan gelap, font yang berbeda, estetika yang berbeda. Anda masih cenderung bertemu pada pilihan umum (Space Grotesk, misalnya) di seluruh generasi. Hindari ini: sangat penting bahwa Anda berpikir di luar kotak!
</frontend_aesthetics>
```

Anda juga dapat merujuk ke skill lengkap [di sini](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md).

### Hindari fokus pada lulus tes dan hard-coding

Claude kadang-kadang dapat fokus terlalu berat pada membuat tes lulus dengan mengorbankan solusi yang lebih umum, atau mungkin menggunakan workaround seperti skrip pembantu untuk refactoring kompleks daripada menggunakan alat standar secara langsung. Untuk mencegah perilaku ini dan memastikan solusi yang kuat dan dapat digeneralisasi:

```text Contoh prompt
Silakan tulis solusi berkualitas tinggi dan tujuan umum menggunakan alat standar yang tersedia. Jangan buat skrip pembantu atau workaround untuk menyelesaikan tugas dengan lebih efisien. Implementasikan solusi yang bekerja dengan benar untuk semua input yang valid, bukan hanya kasus tes. Jangan hard-code nilai atau buat solusi yang hanya bekerja untuk input tes tertentu. Sebagai gantinya, implementasikan logika aktual yang menyelesaikan masalah secara umum.

Fokus pada pemahaman persyaratan masalah dan mengimplementasikan algoritma yang benar. Tes ada di sana untuk memverifikasi kebenaran, bukan untuk mendefinisikan solusi. Berikan implementasi yang berprinsipi yang mengikuti praktik terbaik dan prinsip desain perangkat lunak.

Jika tugas tidak masuk akal atau tidak dapat dilakukan, atau jika ada tes yang salah, silakan beri tahu saya daripada bekerja di sekitarnya. Solusi harus kuat, dapat dipertahankan, dan dapat diperluas.
```

### Meminimalkan halusinasi dalam pengkodean agentic

Model Claude terbaru kurang rentan terhadap halusinasi dan memberikan jawaban yang lebih akurat, berdasarkan fakta, dan cerdas berdasarkan kode. Untuk mendorong perilaku ini bahkan lebih dan meminimalkan halusinasi:

```text Contoh prompt
<investigate_before_answering>
Jangan pernah berspekulasi tentang kode yang belum Anda buka. Jika pengguna mereferensikan file tertentu, Anda HARUS membaca file sebelum menjawab. Pastikan untuk menyelidiki dan membaca file yang relevan SEBELUM menjawab pertanyaan tentang codebase. Jangan pernah membuat klaim tentang kode sebelum menyelidiki kecuali Anda yakin dengan jawaban yang benar - berikan jawaban yang berdasarkan fakta dan bebas halusinasi.
</investigate_before_answering>
```

### Migrasi dari respons yang sudah diisi sebelumnya

Mulai dari Claude Opus 4.6, respons yang sudah diisi sebelumnya pada giliran asisten terakhir tidak lagi didukung. Kecerdasan model dan kemampuan mengikuti instruksi telah berkembang sedemikian rupa sehingga sebagian besar kasus penggunaan prefill tidak lagi memerlukan fitur ini. Model yang ada akan terus mendukung prefill, dan menambahkan pesan asisten di tempat lain dalam percakapan tidak terpengaruh.

Berikut adalah skenario prefill umum dan cara bermigrasi darinya:

<section title="Mengontrol format output">

Prefill telah digunakan untuk memaksa format output tertentu seperti JSON/YAML, klasifikasi, dan pola serupa di mana prefill membatasi Claude pada struktur tertentu.

**Migrasi:** Fitur [Structured Outputs](/docs/id/build-with-claude/structured-outputs) dirancang khusus untuk membatasi respons Claude agar mengikuti skema yang diberikan. Coba minta model untuk menyesuaikan dengan struktur output Anda terlebih dahulu, karena model yang lebih baru dapat secara andal mencocokkan skema kompleks ketika diberitahu, terutama jika diimplementasikan dengan percobaan ulang. Untuk tugas klasifikasi, gunakan alat dengan bidang enum yang berisi label valid Anda atau output terstruktur.

</section>

<section title="Menghilangkan pembukaan">

Prefill seperti `Here is the requested summary:\n` digunakan untuk melewati teks pengantar.

**Migrasi:** Gunakan instruksi langsung dalam system prompt: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc." Atau, arahkan model untuk output dalam tag XML, gunakan output terstruktur, atau gunakan tool calling. Jika pembukaan sesekali terlewat, hapus dalam post-processing.

</section>

<section title="Menghindari penolakan yang buruk">

Prefill digunakan untuk mengarahkan di sekitar penolakan yang tidak perlu.

**Migrasi:** Claude sekarang jauh lebih baik dalam penolakan yang tepat. Prompting yang jelas dalam pesan `user` tanpa prefill harus cukup.

</section>

<section title="Kelanjutan">

Prefill digunakan untuk melanjutkan penyelesaian parsial, melanjutkan respons yang terputus, atau melanjutkan dari mana generasi sebelumnya berhenti.

**Migrasi:** Pindahkan kelanjutan ke pesan pengguna, dan sertakan teks terakhir dari respons yang terputus: "Your previous response was interrupted and ended with \`[previous_response]\`. Continue from where you left off." Jika ini adalah bagian dari penanganan kesalahan atau penanganan respons yang tidak lengkap dan tidak ada penalti UX, coba ulang permintaan.

</section>

<section title="Hidrasi konteks dan konsistensi peran">

Prefill digunakan untuk secara berkala memastikan konteks yang disegarkan atau disuntikkan.

**Migrasi:** Untuk percakapan yang sangat panjang, suntikkan apa yang sebelumnya merupakan pengingat asisten yang sudah diisi sebelumnya ke dalam giliran pengguna. Jika hidrasi konteks adalah bagian dari sistem agentic yang lebih kompleks, pertimbangkan untuk menghidrasi melalui alat (paparkan atau dorong penggunaan alat yang berisi konteks berdasarkan heuristik seperti jumlah giliran) atau selama pemadatan konteks.

</section>

### Output LaTeX

Claude Opus 4.6 secara default menggunakan LaTeX untuk ekspresi matematika, persamaan, dan penjelasan teknis. Jika Anda lebih suka teks biasa, tambahkan instruksi berikut ke prompt Anda:

```text Sample prompt
Format your response in plain text only. Do not use LaTeX, MathJax, or any markup notation such as \( \), $, or \frac{}{}. Write all math expressions using standard text characters (e.g., "/" for division, "*" for multiplication, and "^" for exponents).
```

## Pertimbangan migrasi

Saat bermigrasi ke model Claude 4.6 dari generasi sebelumnya:

1. **Jadilah spesifik tentang perilaku yang diinginkan**: Pertimbangkan untuk menjelaskan dengan tepat apa yang ingin Anda lihat dalam output.

2. **Bingkai instruksi Anda dengan pengubah**: Menambahkan pengubah yang mendorong Claude untuk meningkatkan kualitas dan detail outputnya dapat membantu membentuk kinerja Claude dengan lebih baik. Misalnya, alih-alih "Create an analytics dashboard", gunakan "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation."

3. **Minta fitur spesifik secara eksplisit**: Animasi dan elemen interaktif harus diminta secara eksplisit ketika diinginkan.

4. **Perbarui konfigurasi thinking**: Claude Opus 4.6 menggunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) alih-alih thinking manual dengan `budget_tokens`. Gunakan [effort parameter](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking.

5. **Migrasi dari respons yang sudah diisi sebelumnya**: Respons yang sudah diisi sebelumnya pada giliran asisten terakhir tidak direkomendasikan mulai dari Claude Opus 4.6. Lihat [Migrasi dari respons yang sudah diisi sebelumnya](#migrasi-dari-respons-yang-sudah-diisi-sebelumnya) untuk panduan terperinci tentang alternatif.

6. **Sesuaikan prompting anti-laziness**: Jika prompt Anda sebelumnya mendorong model untuk lebih menyeluruh atau menggunakan alat lebih agresif, kurangi panduan tersebut. Claude Opus 4.6 jauh lebih proaktif dan mungkin overtrigger pada instruksi yang diperlukan untuk model sebelumnya.

Untuk langkah migrasi terperinci, lihat [Migration guide](/docs/id/about-claude/models/migration-guide).