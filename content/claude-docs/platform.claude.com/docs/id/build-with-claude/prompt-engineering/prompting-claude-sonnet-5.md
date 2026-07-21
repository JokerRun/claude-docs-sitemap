---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: a2d782e3fd2ef8855b29c1fb5d1dcdf10fb8dbb942c0a4c10450c057293ecc77
---

# Prompting Claude Sonnet 5

Perbedaan perilaku dan pola prompting untuk Claude Sonnet 5, mencakup effort, default adaptive thinking, penggunaan alat, dan migrasi dari Claude Sonnet 4.6.

---

Panduan ini mencakup pola prompting yang spesifik untuk Claude Sonnet 5. Untuk kemampuan model dan perubahan API, lihat [Apa yang baru di Claude Sonnet 5](/docs/id/about-claude/models/whats-new-sonnet-5). Untuk teknik yang berlaku di semua model Claude saat ini, lihat [Praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Claude Sonnet 5 memiliki kekuatan khusus dalam coding dan tugas agentik. Model ini bekerja dengan baik secara langsung pada prompt Claude Sonnet 4.6 yang sudah ada. Pola dalam panduan ini mencakup perilaku yang paling sering memerlukan penyetelan.

<Note>
  Untuk perubahan parameter API saat bermigrasi dari Claude Sonnet 4.6 (adaptive thinking aktif secara default, parameter sampling tidak diterima, extended thinking manual dihapus, dan tokenizer baru), lihat [panduan migrasi](/docs/id/about-claude/models/migration-guide#migrating-from-claude-sonnet-4-6-to-claude-sonnet-5).
</Note>

## Panjang respons dan verbositas

Claude Sonnet 5 mengkalibrasi panjang respons sesuai dengan kompleksitas tugas alih-alih menggunakan verbositas tetap secara default. Ini biasanya berarti jawaban yang lebih pendek untuk pencarian sederhana dan jawaban yang lebih panjang untuk analisis terbuka.

Jika produk Anda bergantung pada gaya atau verbositas output tertentu, Anda mungkin perlu menyetel prompt Anda. Sebagai contoh, untuk mengurangi verbositas, Anda dapat menambahkan:

```text wrap
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

Jika Anda melihat jenis verbositas tertentu (seperti penjelasan berlebihan), Anda dapat menambahkan instruksi tambahan dalam prompt Anda untuk mencegahnya. Contoh positif yang menunjukkan bagaimana Claude dapat berkomunikasi dengan tingkat keringkasan yang sesuai cenderung lebih efektif daripada contoh negatif atau instruksi yang memberi tahu model apa yang tidak boleh dilakukan.

## Mengkalibrasi effort dan kedalaman pemikiran

[Parameter effort](/docs/id/build-with-claude/effort) memungkinkan Anda menyetel kecerdasan Claude versus pengeluaran token, menukar kemampuan dengan kecepatan yang lebih tinggi dan biaya yang lebih rendah. Pada Claude Sonnet 5, effort secara default adalah `high`, sama seperti pada Claude Sonnet 4.6. Untuk tugas coding dan agentik yang paling sulit, naikkan effort ke `xhigh`. Bereksperimenlah dengan level effort lainnya untuk lebih menyetel penggunaan token dan kecerdasan:

* **`max`:** Kemampuan maksimum absolut tanpa batasan pada pengeluaran token.
* **`xhigh`:** Effort ekstra tinggi adalah pengaturan yang direkomendasikan untuk kasus penggunaan coding dan agentik yang paling sulit.
* **`high`:** Default. Pengaturan ini menyeimbangkan penggunaan token dan kecerdasan untuk sebagian besar kasus penggunaan.
* **`medium`:** Baik untuk kasus penggunaan yang sensitif terhadap biaya yang perlu mengurangi penggunaan token dengan menukar kecerdasan.
* **`low`:** Cadangkan untuk tugas pendek dengan cakupan terbatas dan beban kerja yang sensitif terhadap latensi yang tidak sensitif terhadap kecerdasan.

Sebagai pemetaan lintas model kasar saat bermigrasi: Claude Sonnet 5 pada medium sebanding dalam kecerdasan dengan Claude Sonnet 4.6 pada high, dan Claude Sonnet 5 pada high sebanding dengan Claude Sonnet 4.6 pada max. Saat melakukan benchmarking, cocokkan berdasarkan panjang pemikiran yang diamati alih-alih nama effort.

Claude Sonnet 5 mematuhi level effort secara ketat, terutama pada level rendah. Pada `low` dan `medium`, model membatasi pekerjaannya pada apa yang diminta alih-alih melakukan lebih dari yang diperlukan. Ini baik untuk latensi dan biaya, tetapi pada tugas yang cukup kompleks yang berjalan pada effort `low` ada risiko pemikiran yang kurang mendalam.

Jika Anda mengamati penalaran yang dangkal pada masalah kompleks, naikkan effort ke `high` atau `xhigh` alih-alih mengatasinya dengan prompting. Jika Anda perlu mempertahankan effort pada `low` untuk latensi, tambahkan panduan yang terarah:

```text wrap
This task involves multi-step reasoning. Think carefully through the problem before responding.
```

Pada Claude Sonnet 5, [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) aktif secara default. Permintaan tanpa field `thinking` berjalan dengan adaptive thinking. Ini adalah perubahan dari Claude Sonnet 4.6, di mana permintaan yang sama berjalan tanpa thinking. Untuk menonaktifkan thinking sepenuhnya, kirimkan `thinking: {type: "disabled"}`. Karena `max_tokens` adalah batas keras pada total output (thinking ditambah teks respons), tinjau kembali nilainya untuk beban kerja yang berjalan tanpa thinking pada Claude Sonnet 4.6. Jika sebelumnya Anda menggunakan thinking nonaktif dengan Claude Sonnet 4.6, coba thinking aktif dengan level effort yang lebih rendah untuk Claude Sonnet 5.

Perilaku pemicu untuk adaptive thinking dapat diarahkan. Jika Anda menemukan model mengeluarkan blok thinking lebih sering dari yang Anda inginkan, yang dapat terjadi dengan prompt sistem yang besar atau kompleks, tambahkan panduan untuk mengarahkannya. Seperti biasa, ukur efek dari setiap perubahan prompting terhadap kinerja. Contoh:

```text wrap
Thinking adds latency and should only be used when it will meaningfully improve answer quality, typically for problems that require multi-step reasoning. When in doubt, respond directly.
```

Sebaliknya, jika Anda menjalankan beban kerja yang sulit pada `medium` dan melihat pemikiran yang kurang mendalam, tuas pertama adalah menaikkan effort. Jika Anda memerlukan kontrol yang lebih halus, berikan prompt secara langsung untuk itu.

Extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung pada Claude Sonnet 5 dan mengembalikan error 400. Fitur ini sudah usang pada Claude Sonnet 4.6 dan sekarang dihapus. Gunakan adaptive thinking dengan parameter effort sebagai gantinya.

<Note>
  Jika Anda menjalankan Claude Sonnet 5 pada effort `high`, `xhigh`, atau `max`, sisakan ruang pada `max_tokens` agar model memiliki ruang untuk thinking dan pemanggilan alat. Pada tugas yang panjang, adaptive thinking dapat menggunakan sebagian besar anggaran; jika anggaran ketat, Anda mungkin melihat respons yang hampir seluruhnya berupa thinking diikuti oleh jawaban yang terpotong dan `stop_reason: "max_tokens"`. Menaikkan `max_tokens` atau menurunkan ke effort `medium` menyelesaikan masalah ini. Karena Claude Sonnet 5 menggunakan [tokenizer baru](/docs/id/about-claude/models/whats-new-sonnet-5#new-tokenizer) yang menghasilkan sekitar 30% lebih banyak token untuk teks yang sama, batas `max_tokens` yang disetel untuk Claude Sonnet 4.6 dapat memotong output yang setara. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja.
</Note>

## Pemicu penggunaan alat

Claude Sonnet 5 lebih agentik daripada Claude Sonnet 4.6 secara default dan akan lebih mudah menggunakan alat dan menjalankan loop verifikasi mandiri. Dengan thinking dinonaktifkan, model cenderung tidak menggunakan alat atau mempertimbangkan pencarian; jika Anda mengandalkan pemanggilan alat dengan thinking nonaktif, tambahkan dorongan eksplisit dalam prompt sistem. Effort juga merupakan tuas untuk penggunaan alat: pengaturan effort `high` atau `xhigh` menunjukkan penggunaan alat yang jauh lebih banyak dalam pencarian agentik dan coding. Untuk skenario di mana Anda menginginkan lebih banyak penggunaan alat, Anda juga dapat menyesuaikan prompt Anda untuk secara eksplisit menginstruksikan model tentang kapan dan bagaimana menggunakan alatnya dengan benar. Misalnya, jika Anda menemukan bahwa model tidak menggunakan alat pencarian web Anda, jelaskan dengan jelas mengapa dan bagaimana seharusnya.

## Pembaruan progres untuk pengguna

Claude Sonnet 5 memberikan pembaruan yang teratur dan berkualitas lebih tinggi kepada pengguna sepanjang jejak agentik yang panjang. Jika Anda telah menambahkan scaffolding untuk memaksa pesan status sementara ("Setelah setiap 3 pemanggilan alat, rangkum progres"), coba hapus. Jika Anda menemukan bahwa panjang atau isi pembaruan untuk pengguna dari Claude Sonnet 5 tidak terkalibrasi dengan baik untuk kasus penggunaan Anda, jelaskan secara eksplisit seperti apa pembaruan ini seharusnya dalam prompt dan berikan contoh.

## Mengikuti instruksi secara lebih literal

Claude Sonnet 5 menafsirkan prompt secara literal dan eksplisit, terutama pada level effort yang lebih rendah. Model ini tidak secara diam-diam menggeneralisasi instruksi dari satu item ke item lainnya, dan tidak menyimpulkan permintaan yang tidak Anda buat. Sisi positif dari literalisme ini adalah presisi, dan umumnya berkinerja lebih baik untuk kasus penggunaan API dengan prompt yang disetel dengan cermat, ekstraksi terstruktur, dan pipeline di mana Anda menginginkan perilaku yang dapat diprediksi. Jika Anda memerlukan Claude untuk menerapkan instruksi secara luas, nyatakan cakupannya secara eksplisit (misalnya, "Terapkan pemformatan ini ke setiap bagian, bukan hanya bagian pertama").

## Nada dan gaya penulisan

Seperti halnya model baru lainnya, gaya prosa pada penulisan bentuk panjang dapat berubah. Jika produk Anda bergantung pada suara tertentu, evaluasi ulang prompt gaya terhadap baseline yang baru.

Misalnya, jika suara produk Anda lebih hangat atau lebih percakapan, tambahkan:

```text wrap
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

Jika sebelumnya Anda mengandalkan `temperature` untuk variasi gaya, perhatikan bahwa mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default mengembalikan error 400 pada Claude Sonnet 5. Batasan ini baru untuk model kelas Sonnet. Hapus parameter ini saat bermigrasi, dan gunakan instruksi prompt sistem untuk memandu nada dan variasi sebagai gantinya.

## Default desain dan frontend

Claude Sonnet 5 mungkin menetap pada gaya visual default yang konsisten pada brief frontend dan desain yang terbuka. Gaya khas default dapat terlihat baik untuk beberapa brief tetapi terasa tidak cocok untuk dashboard, alat pengembang, fintech, layanan kesehatan, atau aplikasi enterprise.

Instruksi generik ("jangan gunakan warna itu," "buat bersih dan minimal") cenderung menggeser model ke palet tetap yang berbeda alih-alih menghasilkan variasi. Dua pendekatan yang bekerja dengan andal:

**1. Tentukan alternatif yang konkret.** Model mengikuti spesifikasi eksplisit dengan tepat:

```text wrap
Design a desktop landing page for a supplement brand called AEFRM.

The visual direction should come from a cold monochrome atmosphere using pale silver-gray tones that gradually deepen into blue-gray and near-black, similar to a misted metallic surface.

The page should feel sharp and controlled, with a strong sense of structure and restraint.

Use this tonal system across the full page instead of introducing bright accent colors.

Use the uploaded image on the hero design in black and white.

The layout should be built with clear horizontal sections and a centered max-width container. Use 4px corner radius consistently across cards, buttons, inputs, and media frames. Margins should feel generous, with enough empty space around each section so the page breathes.

Typography should use a square, angular sans-serif with wider letter spacing than usual, especially in headings and navigation, so the text feels more engineered and less compressed. Headline text can be large and uppercase, while supporting copy remains short and sparse. The sub texts should be written with Alumni Sans SC in 4-6px like tiny little texts on corners bottom centre like that.

For the structure, start with a hero section containing a strong product statement, one short supporting paragraph, and a clean product placeholder or packshot frame. Below that, add a benefit grid with three or four blocks, then a formulation or ingredients section, and finally a cta.

Buttons should be flat and precise, with subtle hover changes using transition: all 160ms ease out where brightness and border contrast shift slightly rather than using dramatic motion.

Color palette should stay within this range:
#E9ECEC, #C9D2D4, #8C9A9E, #44545B, #11171B.
```

**2. Minta model mengusulkan opsi sebelum membangun.** Ini memecah default dan memberi pengguna kontrol. Karena `temperature` tidak diterima pada Claude Sonnet 5, pendekatan ini adalah cara yang direkomendasikan untuk menghasilkan arah desain yang berbeda secara bermakna di berbagai eksekusi. Contoh prompt:

```text wrap
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the user to pick one, then implement only that direction.
```

Untuk menjauh dari pola generik yang disebut pengguna sebagai estetika "AI slop", Anda dapat menyertakan arahan singkat dalam prompt sistem Anda. [Skill frontend-design](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md) memberikan pembahasan yang lebih lengkap, tetapi cuplikan ini bekerja dengan baik bersama pendekatan variasi sebelumnya:

```text wrap
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

## Produk coding interaktif

Penggunaan token dan perilaku dapat berbeda antara agen coding otonom dan asinkron dengan satu giliran pengguna dan agen coding interaktif dan sinkron dengan beberapa giliran pengguna. Untuk memaksimalkan kinerja dan efisiensi token dalam produk coding, gunakan effort `xhigh` atau `high`, tambahkan fitur otonom seperti mode otomatis, dan kurangi jumlah interaksi manusia yang diperlukan dari pengguna Anda.

Saat membatasi jumlah interaksi pengguna yang diperlukan, penting untuk menentukan tugas, maksud, dan batasan yang relevan di awal pada giliran manusia pertama. Memberikan deskripsi tugas yang terspesifikasi dengan baik, jelas, dan akurat di awal dapat membantu memaksimalkan otonomi dan kecerdasan sambil meminimalkan penggunaan token tambahan setelah giliran pengguna. Sebaliknya, prompt yang ambigu atau kurang terspesifikasi yang disampaikan secara bertahap melalui beberapa giliran pengguna cenderung relatif mengurangi efisiensi token dan terkadang kinerja.

## Harness tinjauan kode

Jika harness tinjauan kode Anda disetel untuk model sebelumnya, Anda mungkin awalnya melihat recall yang lebih rendah pada Claude Sonnet 5. Ini kemungkinan besar adalah efek harness, bukan regresi kemampuan. Ketika prompt tinjauan mengatakan hal-hal seperti "hanya laporkan masalah dengan tingkat keparahan tinggi," "bersikaplah konservatif," atau "jangan terlalu detail," Claude Sonnet 5 mungkin mengikuti instruksi tersebut dengan lebih setia daripada model sebelumnya: model mungkin menyelidiki kode dengan sama menyeluruhnya, mengidentifikasi bug, dan kemudian tidak melaporkan temuan yang dinilainya berada di bawah standar yang Anda nyatakan. Ini dapat terlihat sebagai model melakukan kedalaman investigasi yang sama tetapi mengonversi lebih sedikit investigasi menjadi temuan yang dilaporkan, terutama pada bug dengan tingkat keparahan lebih rendah. Presisi biasanya meningkat, tetapi recall yang terukur dapat turun meskipun kemampuan dasar model dalam menemukan bug telah meningkat.

Beberapa bahasa prompt yang direkomendasikan:

```text wrap
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

Prompt ini dapat digunakan tanpa memiliki langkah kedua yang sebenarnya, tetapi memindahkan penyaringan kepercayaan keluar dari langkah penemuan sering kali membantu. Jika harness Anda memiliki tahap verifikasi, deduplikasi, atau pemeringkatan terpisah, beri tahu model secara eksplisit bahwa tugasnya pada tahap penemuan adalah cakupan, bukan penyaringan.

Jika Anda memang ingin model melakukan penyaringan mandiri dalam satu kali proses, jelaskan secara konkret di mana standarnya alih-alih menggunakan istilah kualitatif seperti "penting": misalnya, "laporkan bug apa pun yang dapat menyebabkan perilaku yang salah, kegagalan pengujian, atau hasil yang menyesatkan; hanya abaikan hal-hal kecil seperti preferensi gaya atau penamaan murni."

Lakukan iterasi pada prompt terhadap subset dari eval atau kasus uji Anda untuk memvalidasi peningkatan recall atau skor F1.

## Computer use

Claude Sonnet 5 mendukung versi alat `computer_20251124`. Kemampuan [computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool) bekerja di berbagai resolusi, hingga resolusi maksimum 2576px / 3.75MP. Pengujian internal computer use menunjukkan bahwa mengirim gambar pada 1080p memberikan keseimbangan yang baik antara kinerja dan biaya.

Untuk beban kerja yang sangat sensitif terhadap biaya, 720p atau 1366×768 adalah opsi berbiaya lebih rendah dengan kinerja yang kuat. Lakukan pengujian Anda sendiri untuk menemukan pengaturan ideal untuk kasus penggunaan Anda; bereksperimen dengan pengaturan effort juga dapat membantu menyetel perilaku model.
