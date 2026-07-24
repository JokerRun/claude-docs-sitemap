---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-4-8
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 97f3a25fed7fba289561ffd1da63c24760a7b23eba85a417ab2b2afd746e7219
---

# Prompting Claude Opus 4.8

Perbedaan perilaku dan pola prompting untuk Claude Opus 4.8, mencakup verbositas, kalibrasi effort, penggunaan alat, subagen, dan default frontend.

---

Panduan ini mencakup pola prompting yang spesifik untuk Claude Opus 4.8. Untuk kemampuan model dan perubahan API, lihat [Apa yang baru di Claude Opus 4.8](/docs/id/about-claude/models/whats-new-claude-4-8). Untuk teknik yang berlaku di semua model Claude saat ini, lihat [Praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Claude Opus 4.8 memiliki kekuatan khusus dalam pekerjaan agentik jangka panjang, pekerjaan pengetahuan, visi, dan tugas memori. Model ini bekerja dengan baik secara langsung pada prompt Claude Opus 4.7 yang sudah ada. Pola-pola berikut mencakup perilaku yang paling sering memerlukan penyetelan.

<Note>
  Untuk perubahan parameter API saat bermigrasi dari Claude Opus 4.7 (parameter sampling, default effort, default jendela konteks 1M, pesan sistem di tengah percakapan, dan detail stop penolakan), lihat [panduan migrasi](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-47).
</Note>

## Panjang respons dan verbositas

Claude Opus 4.8 mengkalibrasi panjang respons berdasarkan seberapa kompleks tugas tersebut menurut penilaiannya, alih-alih menggunakan verbositas tetap secara default. Ini biasanya berarti jawaban yang lebih pendek untuk pencarian sederhana dan jawaban yang jauh lebih panjang untuk analisis terbuka.

Jika produk Anda bergantung pada gaya atau verbositas output tertentu, Anda mungkin perlu menyetel prompt Anda. Sebagai contoh, untuk mengurangi verbositas, Anda dapat menambahkan:

```text wrap
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

Jika Anda melihat contoh spesifik dari jenis verbositas tertentu (seperti penjelasan berlebihan), Anda dapat menambahkan instruksi tambahan dalam prompt Anda untuk mencegahnya. Contoh positif yang menunjukkan bagaimana Claude dapat berkomunikasi dengan tingkat keringkasan yang tepat cenderung lebih efektif daripada contoh negatif atau instruksi yang memberi tahu model apa yang tidak boleh dilakukan.

## Mengkalibrasi effort dan kedalaman pemikiran

[Parameter effort](/docs/id/build-with-claude/effort) memungkinkan Anda menyetel kecerdasan Claude versus penggunaan token, menukar kemampuan untuk kecepatan yang lebih tinggi dan biaya yang lebih rendah. Mulailah dengan level effort `xhigh` untuk kasus penggunaan coding dan agentik, dan gunakan minimal effort `high` untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan. Bereksperimenlah dengan level effort lain untuk lebih menyetel penggunaan token dan kecerdasan:

* **`max`:** Effort max dapat memberikan peningkatan performa dalam beberapa kasus penggunaan, tetapi mungkin menunjukkan hasil yang semakin berkurang dari peningkatan penggunaan token. Pengaturan ini juga terkadang rentan terhadap pemikiran berlebihan. Uji effort max untuk tugas yang menuntut kecerdasan.
* **`xhigh`:** Effort extra high adalah pengaturan terbaik untuk sebagian besar kasus penggunaan coding dan agentik.
* **`high`:** Pengaturan ini menyeimbangkan penggunaan token dan kecerdasan. Untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan, gunakan minimal effort `high`.
* **`medium`:** Baik untuk kasus penggunaan yang sensitif terhadap biaya yang perlu mengurangi penggunaan token dengan menukar kecerdasan.
* **`low`:** Cadangkan untuk tugas pendek yang terbatas dan beban kerja yang sensitif terhadap latensi yang tidak sensitif terhadap kecerdasan.

Claude Opus 4.8 mematuhi level effort secara ketat, terutama pada level rendah. Pada `low` dan `medium`, model membatasi pekerjaannya pada apa yang diminta alih-alih melakukan lebih dari yang diperlukan. Ini baik untuk latensi dan biaya, tetapi pada tugas yang cukup kompleks yang berjalan pada effort `low` ada risiko pemikiran yang kurang mendalam.

Jika Anda mengamati penalaran yang dangkal pada masalah kompleks, naikkan effort ke `high` atau `xhigh` alih-alih mengatasinya dengan prompting. Jika Anda perlu mempertahankan effort pada `low` untuk latensi, tambahkan panduan yang terarah:

```text wrap
This task involves multistep reasoning. Think carefully through the problem before responding.
```

Effort kemungkinan lebih penting untuk model ini dibandingkan Opus sebelumnya, jadi bereksperimenlah secara aktif saat Anda melakukan upgrade.

Pada Claude Opus 4.8, pemikiran dinonaktifkan kecuali Anda secara eksplisit mengatur `thinking: {type: "adaptive"}`. Perilaku pemicu untuk pemikiran adaptif dapat diarahkan. Jika Anda menemukan model berpikir lebih sering dari yang Anda inginkan, yang dapat terjadi dengan prompt sistem yang besar atau kompleks, tambahkan panduan untuk mengarahkannya. Seperti biasa, ukur efek dari setiap perubahan prompting terhadap performa. Contoh:

```text wrap
Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multistep reasoning. When in doubt, respond directly.
```

Sebaliknya, jika Anda menjalankan beban kerja yang berat pada `medium` dan melihat pemikiran yang kurang mendalam, tuas pertama adalah menaikkan effort. Jika Anda memerlukan kontrol yang lebih halus, berikan prompt secara langsung untuk itu.

<Note>
  Jika Anda menjalankan Claude Opus 4.8 pada effort `max` atau `xhigh`, atur anggaran token output maksimum yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan panggilan alatnya. Mulai dari 64k token dan setel dari sana.
</Note>

## Pemicu penggunaan alat

Claude Opus 4.8 memiliki kecenderungan untuk lebih memilih penalaran daripada panggilan alat. Ini menghasilkan hasil yang lebih baik dalam sebagian besar kasus. Namun, meningkatkan pengaturan effort adalah tuas yang berguna untuk meningkatkan tingkat penggunaan alat, terutama dalam pekerjaan pengetahuan. Pengaturan effort `high` atau `xhigh` menunjukkan penggunaan alat yang jauh lebih banyak dalam pencarian agentik dan coding. Untuk skenario di mana Anda menginginkan lebih banyak penggunaan alat, Anda juga dapat menyesuaikan prompt Anda untuk secara eksplisit menginstruksikan model tentang kapan dan bagaimana menggunakan alatnya dengan benar. Misalnya, jika Anda menemukan bahwa model tidak menggunakan alat pencarian web Anda, jelaskan dengan jelas mengapa dan bagaimana seharusnya.

## Pembaruan progres yang ditampilkan ke pengguna

Claude Opus 4.8 memberikan pembaruan yang lebih teratur dan berkualitas lebih tinggi kepada pengguna sepanjang jejak agentik yang panjang. Jika Anda telah menambahkan scaffolding untuk memaksa pesan status sementara ("Setelah setiap 3 panggilan alat, rangkum progres"), coba hapus. Jika Anda menemukan bahwa panjang atau isi pembaruan Claude Opus 4.8 yang ditampilkan ke pengguna tidak terkalibrasi dengan baik untuk kasus penggunaan Anda, jelaskan secara eksplisit seperti apa seharusnya pembaruan ini dalam prompt dan berikan contoh.

## Mengikuti instruksi secara lebih literal

Claude Opus 4.8 menafsirkan prompt secara literal dan eksplisit, terutama pada level effort yang lebih rendah. Model ini tidak secara diam-diam menggeneralisasi instruksi dari satu item ke item lainnya, dan tidak menyimpulkan permintaan yang tidak Anda buat. Keuntungan dari literalisme ini adalah presisi dan lebih sedikit kekacauan, dan umumnya berkinerja lebih baik untuk kasus penggunaan API dengan prompt yang disetel dengan cermat, ekstraksi terstruktur, dan pipeline di mana Anda menginginkan perilaku yang dapat diprediksi. Jika Anda memerlukan Claude untuk menerapkan instruksi secara luas, nyatakan cakupannya secara eksplisit (misalnya, "Terapkan pemformatan ini ke setiap bagian, bukan hanya bagian pertama").

## Nada dan gaya penulisan

Seperti halnya model baru lainnya, gaya prosa pada penulisan bentuk panjang mungkin berubah. Claude Opus 4.8 cenderung ke gaya yang langsung dan berpendirian dengan frasa validasi yang minimal dan penggunaan emoji yang hemat. Jika produk Anda bergantung pada suara tertentu, evaluasi ulang prompt gaya terhadap baseline baru.

Misalnya, jika suara produk Anda lebih hangat atau lebih percakapan, tambahkan:

```text wrap
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

## Mengontrol pembuatan subagen

Claude Opus 4.8 cenderung membuat lebih sedikit subagen secara default. Namun, perilaku ini dapat diarahkan melalui prompting; berikan Claude Opus 4.8 panduan eksplisit tentang kapan subagen diinginkan. Contoh sederhana untuk kasus penggunaan coding:

```text wrap
Do not spawn a subagent for work you can complete directly in a single response (e.g. refactoring a function you can already see).

Spawn multiple subagents in the same turn when fanning out across items or reading multiple files.
```

## Default desain dan frontend

Claude Opus 4.8 memiliki insting desain yang kuat, dengan gaya khas default yang konsisten: latar belakang krem hangat/putih gading (\~`#F4F1EA`), tipe display serif (Georgia, Fraunces, Playfair), aksen kata miring, dan aksen terakota/amber. Ini terlihat bagus untuk brief editorial, perhotelan, dan portofolio, tetapi akan terasa tidak pas untuk dashboard, alat pengembang, fintech, layanan kesehatan, atau aplikasi enterprise. Default ini muncul di slide deck dan UI web.

Default ini persisten. Instruksi generik ("jangan gunakan krem," "buat bersih dan minimal") cenderung menggeser model ke palet tetap yang berbeda alih-alih menghasilkan variasi. Dua pendekatan bekerja dengan andal:

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

**2. Minta model mengusulkan opsi sebelum membangun.** Ini memecah default dan memberi pengguna kontrol. Jika sebelumnya Anda mengandalkan `temperature` untuk variasi desain, gunakan pendekatan ini; pendekatan ini menghasilkan arah yang berbeda secara bermakna di setiap eksekusi. Contoh prompt:

```text wrap
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface — one-line rationale). Ask the user to pick one, then implement only that direction.
```

Selain itu, Claude Opus 4.8 memerlukan lebih sedikit prompting desain frontend dibandingkan model sebelumnya untuk menghindari pola generik yang disebut pengguna sebagai estetika "AI slop". Dengan model sebelumnya, Anthropic merekomendasikan cuplikan prompt yang lebih panjang dalam [skill frontend-design](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md). Namun, Claude Opus 4.8 menghasilkan frontend yang khas dan kreatif dengan panduan prompting yang lebih minimal. Cuplikan prompt ini bekerja dengan baik bersama saran prompting sebelumnya untuk variasi:

```text wrap
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

## Produk coding interaktif

Penggunaan token dan perilaku Claude Opus 4.8 dapat berbeda antara agen coding otonom dan asinkron dengan satu giliran pengguna dan agen coding interaktif dan sinkron dengan beberapa giliran pengguna. Secara khusus, model ini cenderung menggunakan lebih banyak token dalam pengaturan interaktif, terutama karena model bernalar lebih banyak setelah giliran pengguna. Ini dapat meningkatkan koherensi jangka panjang, kepatuhan terhadap instruksi, dan kemampuan coding dalam sesi coding interaktif yang panjang, tetapi juga disertai dengan penggunaan token yang lebih banyak. Untuk memaksimalkan performa dan efisiensi token dalam produk coding, gunakan effort `xhigh` atau `high`, tambahkan fitur otonom seperti mode otomatis, dan kurangi jumlah interaksi manusia yang diperlukan dari pengguna Anda.

Tentu saja, saat membatasi jumlah interaksi pengguna yang diperlukan, penting untuk menentukan tugas, maksud, dan batasan yang relevan di awal pada giliran manusia pertama. Memberikan deskripsi tugas yang terspesifikasi dengan baik, jelas, dan akurat di awal dapat membantu memaksimalkan otonomi dan kecerdasan sambil meminimalkan penggunaan token ekstra setelah giliran pengguna. Karena Claude Opus 4.8 lebih otonom daripada model sebelumnya, pola penggunaan ini membantu memaksimalkan performa. Sebaliknya, prompt yang ambigu atau kurang terspesifikasi yang disampaikan secara bertahap melalui beberapa giliran pengguna cenderung relatif mengurangi efisiensi token dan terkadang performa.

## Harness tinjauan kode

Claude Opus 4.8 secara signifikan lebih baik dalam menemukan bug dibandingkan model sebelumnya, dan memiliki recall dan presisi yang lebih tinggi dalam evaluasi internal. Namun, jika harness tinjauan kode Anda disetel untuk model sebelumnya, Anda mungkin awalnya melihat recall yang lebih rendah. Ini kemungkinan adalah efek harness, bukan regresi kemampuan. Ketika prompt tinjauan mengatakan hal-hal seperti "hanya laporkan masalah dengan tingkat keparahan tinggi," "bersikaplah konservatif," atau "jangan terlalu detail," Claude Opus 4.8 mungkin mengikuti instruksi tersebut dengan lebih setia daripada model sebelumnya: model mungkin menyelidiki kode dengan sama menyeluruhnya, mengidentifikasi bug, dan kemudian tidak melaporkan temuan yang dinilainya berada di bawah standar yang Anda nyatakan. Ini dapat terlihat sebagai model melakukan kedalaman investigasi yang sama tetapi mengonversi lebih sedikit investigasi menjadi temuan yang dilaporkan, terutama pada bug dengan tingkat keparahan lebih rendah. Presisi biasanya meningkat, tetapi recall yang terukur dapat turun meskipun kemampuan dasar model dalam menemukan bug telah meningkat.

Beberapa bahasa prompt yang direkomendasikan:

```text wrap
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

Prompt ini dapat digunakan tanpa memiliki langkah kedua yang sebenarnya, tetapi memindahkan penyaringan kepercayaan keluar dari langkah penemuan sering kali membantu. Jika harness Anda memiliki tahap verifikasi, deduplikasi, atau pemeringkatan terpisah, beri tahu model secara eksplisit bahwa tugasnya pada tahap penemuan adalah cakupan, bukan penyaringan.

Jika Anda memang ingin model menyaring sendiri dalam satu langkah, bersikaplah konkret tentang di mana standarnya alih-alih menggunakan istilah kualitatif seperti "penting": misalnya, "laporkan bug apa pun yang dapat menyebabkan perilaku yang salah, kegagalan pengujian, atau hasil yang menyesatkan; hanya abaikan hal-hal kecil seperti preferensi gaya atau penamaan murni."

Lakukan iterasi pada prompt terhadap subset evaluasi atau kasus uji Anda untuk memvalidasi peningkatan recall atau skor F1.

## Penggunaan komputer

Kemampuan [penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool) bekerja di berbagai resolusi, hingga resolusi maksimum 2576px / 3.75MP. Pengujian penggunaan komputer internal menunjukkan bahwa mengirim gambar pada 1080p memberikan keseimbangan yang baik antara performa dan biaya.

Untuk beban kerja yang sangat sensitif terhadap biaya, 720p atau 1366×768 adalah opsi berbiaya lebih rendah dengan performa yang kuat. Lakukan pengujian Anda sendiri untuk menemukan pengaturan yang ideal untuk kasus penggunaan Anda; bereksperimen dengan pengaturan effort juga dapat membantu menyetel perilaku model.
