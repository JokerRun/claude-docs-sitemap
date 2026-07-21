---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-4-8
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: e28ec5f69ef127758bd16644e28c72a2d1f6850b44c3acf5bdb69a0f1e50e11b
---

# Prompting Claude Opus 4.8

Perbedaan perilaku dan pola prompting untuk Claude Opus 4.8, mencakup verbositas, kalibrasi effort, penggunaan alat, subagent, dan default frontend.

---

Panduan ini membahas pola prompting yang spesifik untuk Claude Opus 4.8. Untuk kemampuan model dan perubahan API, lihat [Apa yang baru di Claude Opus 4.8](/docs/id/about-claude/models/whats-new-claude-4-8). Untuk teknik yang berlaku di semua model Claude saat ini, lihat [Praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Claude Opus 4.8 memiliki kekuatan khusus dalam pekerjaan agentik jangka panjang, pekerjaan pengetahuan, visi, dan tugas memori. Model ini bekerja dengan baik secara langsung pada prompt Claude Opus 4.7 yang sudah ada. Pola-pola berikut mencakup perilaku yang paling sering memerlukan penyesuaian.

<Note>
  Untuk perubahan parameter API saat bermigrasi dari Claude Opus 4.7 (parameter sampling, default effort, default jendela konteks 1M, pesan sistem di tengah percakapan, dan detail refusal stop), lihat [panduan migrasi](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-47).
</Note>

## Panjang respons dan verbositas

Claude Opus 4.8 mengkalibrasi panjang respons berdasarkan seberapa kompleks model menilai tugas tersebut, alih-alih menggunakan verbositas tetap secara default. Ini biasanya berarti jawaban yang lebih pendek untuk pencarian sederhana dan jawaban yang jauh lebih panjang untuk analisis terbuka.

Jika produk Anda bergantung pada gaya atau verbositas output tertentu, Anda mungkin perlu menyesuaikan prompt Anda. Sebagai contoh, untuk mengurangi verbositas, Anda dapat menambahkan:

```text wrap
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

Jika Anda melihat contoh spesifik dari jenis verbositas tertentu (seperti penjelasan berlebihan), Anda dapat menambahkan instruksi tambahan dalam prompt Anda untuk mencegahnya. Contoh positif yang menunjukkan bagaimana Claude dapat berkomunikasi dengan tingkat keringkasan yang sesuai cenderung lebih efektif daripada contoh negatif atau instruksi yang memberi tahu model apa yang tidak boleh dilakukan.

## Mengkalibrasi effort dan kedalaman pemikiran

Parameter [effort](/docs/id/build-with-claude/effort) memungkinkan Anda menyesuaikan kecerdasan Claude versus penggunaan token, menukar kemampuan dengan kecepatan yang lebih tinggi dan biaya yang lebih rendah. Mulailah dengan tingkat effort `xhigh` untuk kasus penggunaan coding dan agentik, dan gunakan minimal effort `high` untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan. Bereksperimenlah dengan tingkat effort lain untuk menyesuaikan lebih lanjut penggunaan token dan kecerdasan:

* **`max`:** Effort maksimum dapat memberikan peningkatan performa dalam beberapa kasus penggunaan, tetapi mungkin menunjukkan hasil yang semakin berkurang dari peningkatan penggunaan token. Pengaturan ini juga terkadang rentan terhadap pemikiran berlebihan. Uji effort maksimum untuk tugas yang menuntut kecerdasan tinggi.
* **`xhigh`:** Effort ekstra tinggi adalah pengaturan terbaik untuk sebagian besar kasus penggunaan coding dan agentik.
* **`high`:** Pengaturan ini menyeimbangkan penggunaan token dan kecerdasan. Untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan, gunakan minimal effort `high`.
* **`medium`:** Baik untuk kasus penggunaan yang sensitif terhadap biaya yang perlu mengurangi penggunaan token sambil menukar kecerdasan.
* **`low`:** Simpan untuk tugas pendek dengan cakupan terbatas dan beban kerja yang sensitif terhadap latensi yang tidak sensitif terhadap kecerdasan.

Claude Opus 4.8 mematuhi tingkat effort secara ketat, terutama pada tingkat rendah. Pada `low` dan `medium`, model membatasi pekerjaannya pada apa yang diminta alih-alih melampaui ekspektasi. Ini baik untuk latensi dan biaya, tetapi pada tugas yang cukup kompleks yang berjalan pada effort `low`, ada risiko pemikiran yang kurang mendalam.

Jika Anda mengamati penalaran yang dangkal pada masalah kompleks, naikkan effort ke `high` atau `xhigh` alih-alih mengatasinya melalui prompting. Jika Anda perlu mempertahankan effort pada `low` untuk latensi, tambahkan panduan yang ditargetkan:

```text wrap
This task involves multi-step reasoning. Think carefully through the problem before responding.
```

Effort kemungkinan akan lebih penting untuk model ini dibandingkan Opus sebelumnya, jadi bereksperimenlah secara aktif dengannya saat Anda melakukan upgrade.

Pada Claude Opus 4.8, thinking dinonaktifkan kecuali Anda secara eksplisit mengatur `thinking: {type: "adaptive"}`. Perilaku pemicu untuk adaptive thinking dapat diarahkan. Jika Anda menemukan model berpikir lebih sering dari yang Anda inginkan, yang dapat terjadi dengan prompt sistem yang besar atau kompleks, tambahkan panduan untuk mengarahkannya. Seperti biasa, ukur efek dari setiap perubahan prompting terhadap performa. Contoh:

```text wrap
Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multi-step reasoning. When in doubt, respond directly.
```

Sebaliknya, jika Anda menjalankan beban kerja yang sulit pada `medium` dan melihat pemikiran yang kurang mendalam, langkah pertama adalah menaikkan effort. Jika Anda memerlukan kontrol yang lebih halus, berikan prompt untuk itu secara langsung.

<Note>
  Jika Anda menjalankan Claude Opus 4.8 pada effort `max` atau `xhigh`, atur anggaran token output maksimum yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagent dan pemanggilan alatnya. Mulai dari 64k token dan sesuaikan dari sana.
</Note>

## Pemicu penggunaan alat

Claude Opus 4.8 memiliki kecenderungan untuk lebih memilih penalaran daripada pemanggilan alat. Ini menghasilkan hasil yang lebih baik dalam sebagian besar kasus. Namun, meningkatkan pengaturan effort adalah tuas yang berguna untuk meningkatkan tingkat penggunaan alat, terutama dalam pekerjaan pengetahuan. Pengaturan effort `high` atau `xhigh` menunjukkan penggunaan alat yang jauh lebih banyak dalam pencarian agentik dan coding. Untuk skenario di mana Anda menginginkan lebih banyak penggunaan alat, Anda juga dapat menyesuaikan prompt Anda untuk secara eksplisit menginstruksikan model tentang kapan dan bagaimana menggunakan alatnya dengan benar. Misalnya, jika Anda menemukan bahwa model tidak menggunakan alat pencarian web Anda, jelaskan dengan jelas mengapa dan bagaimana model harus menggunakannya.

## Pembaruan progres yang ditampilkan kepada pengguna

Claude Opus 4.8 memberikan pembaruan yang lebih teratur dan berkualitas lebih tinggi kepada pengguna sepanjang jejak agentik yang panjang. Jika Anda telah menambahkan scaffolding untuk memaksa pesan status sementara ("Setelah setiap 3 pemanggilan alat, rangkum progres"), coba hapus itu. Jika Anda menemukan bahwa panjang atau konten pembaruan yang ditampilkan kepada pengguna dari Claude Opus 4.8 tidak terkalibrasi dengan baik untuk kasus penggunaan Anda, jelaskan secara eksplisit seperti apa pembaruan ini seharusnya dalam prompt dan berikan contoh.

## Mengikuti instruksi secara lebih harfiah

Claude Opus 4.8 menafsirkan prompt secara harfiah dan eksplisit, terutama pada tingkat effort yang lebih rendah. Model tidak secara diam-diam menggeneralisasi instruksi dari satu item ke item lain, dan tidak menyimpulkan permintaan yang tidak Anda buat. Keuntungan dari literalisme ini adalah presisi dan lebih sedikit kekacauan, dan secara umum berkinerja lebih baik untuk kasus penggunaan API dengan prompt yang disesuaikan dengan cermat, ekstraksi terstruktur, dan pipeline di mana Anda menginginkan perilaku yang dapat diprediksi. Jika Anda memerlukan Claude untuk menerapkan instruksi secara luas, nyatakan cakupannya secara eksplisit (misalnya, "Terapkan pemformatan ini ke setiap bagian, bukan hanya yang pertama").

## Nada dan gaya penulisan

Seperti halnya model baru lainnya, gaya prosa pada penulisan panjang mungkin berubah. Claude Opus 4.8 cenderung ke arah gaya yang langsung dan beropini dengan frasa yang mengutamakan validasi yang minimal dan penggunaan emoji yang hemat. Jika produk Anda bergantung pada suara tertentu, evaluasi ulang prompt gaya terhadap baseline baru.

Misalnya, jika suara produk Anda lebih hangat atau lebih percakapan, tambahkan:

```text wrap
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

## Mengontrol pembuatan subagent

Claude Opus 4.8 cenderung membuat lebih sedikit subagent secara default. Namun, perilaku ini dapat diarahkan melalui prompting; berikan Claude Opus 4.8 panduan eksplisit tentang kapan subagent diinginkan. Contoh sederhana untuk kasus penggunaan coding:

```text wrap
Do not spawn a subagent for work you can complete directly in a single response (e.g. refactoring a function you can already see).

Spawn multiple subagents in the same turn when fanning out across items or reading multiple files.
```

## Default desain dan frontend

Claude Opus 4.8 memiliki naluri desain yang kuat, dengan gaya khas default yang konsisten: latar belakang krem hangat/putih gading (\~`#F4F1EA`), tipografi display serif (Georgia, Fraunces, Playfair), aksen kata miring, dan aksen terakota/amber. Ini terlihat baik untuk brief editorial, perhotelan, dan portofolio, tetapi akan terasa tidak cocok untuk dashboard, dev tools, fintech, layanan kesehatan, atau aplikasi enterprise. Default ini muncul di slide deck dan UI web.

Default ini bersifat persisten. Instruksi generik ("jangan gunakan krem," "buat bersih dan minimal") cenderung menggeser model ke palet tetap yang berbeda alih-alih menghasilkan variasi. Dua pendekatan berikut bekerja dengan andal:

**1. Tentukan alternatif konkret.** Model mengikuti spesifikasi eksplisit dengan tepat:

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

**2. Minta model mengusulkan opsi sebelum membangun.** Ini mematahkan default dan memberikan kontrol kepada pengguna. Jika sebelumnya Anda mengandalkan `temperature` untuk variasi desain, gunakan pendekatan ini; pendekatan ini menghasilkan arah yang berbeda secara bermakna di seluruh eksekusi. Contoh prompt:

```text wrap
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface — one-line rationale). Ask the user to pick one, then implement only that direction.
```

Selain itu, Claude Opus 4.8 memerlukan lebih sedikit prompting desain frontend dibandingkan model sebelumnya untuk menghindari pola generik yang disebut pengguna sebagai estetika "AI slop". Dengan model sebelumnya, Anthropic merekomendasikan cuplikan prompt yang lebih panjang dalam [frontend-design skill](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md). Namun, Claude Opus 4.8 menghasilkan frontend yang khas dan kreatif dengan panduan prompting yang lebih minimal. Cuplikan prompt ini bekerja dengan baik bersama saran prompting sebelumnya untuk variasi:

```text wrap
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

## Produk coding interaktif

Penggunaan token dan perilaku Claude Opus 4.8 dapat berbeda antara agen coding otonom dan asinkron dengan satu giliran pengguna, dan agen coding interaktif dan sinkron dengan beberapa giliran pengguna. Secara spesifik, model cenderung menggunakan lebih banyak token dalam pengaturan interaktif, terutama karena model bernalar lebih banyak setelah giliran pengguna. Ini dapat meningkatkan koherensi jangka panjang, kepatuhan instruksi, dan kemampuan coding dalam sesi coding interaktif yang panjang, tetapi juga disertai dengan penggunaan token yang lebih banyak. Untuk memaksimalkan performa dan efisiensi token dalam produk coding, gunakan effort `xhigh` atau `high`, tambahkan fitur otonom seperti mode auto, dan kurangi jumlah interaksi manusia yang diperlukan dari pengguna Anda.

Tentu saja, saat membatasi jumlah interaksi pengguna yang diperlukan, penting untuk menentukan tugas, maksud, dan batasan yang relevan di awal pada giliran manusia pertama. Memberikan deskripsi tugas yang terspesifikasi dengan baik, jelas, dan akurat di awal dapat membantu memaksimalkan otonomi dan kecerdasan sambil meminimalkan penggunaan token tambahan setelah giliran pengguna. Karena Claude Opus 4.8 lebih otonom daripada model sebelumnya, pola penggunaan ini membantu memaksimalkan performa. Sebaliknya, prompt yang ambigu atau kurang terspesifikasi yang disampaikan secara progresif melalui beberapa giliran pengguna cenderung relatif mengurangi efisiensi token dan terkadang performa.

## Harness code review

Claude Opus 4.8 secara signifikan lebih baik dalam menemukan bug dibandingkan model sebelumnya, dan memiliki recall dan presisi yang lebih tinggi dalam evaluasi internal. Namun, jika harness code-review Anda disesuaikan untuk model sebelumnya, Anda mungkin awalnya melihat recall yang lebih rendah. Ini kemungkinan adalah efek harness, bukan regresi kemampuan. Ketika prompt review mengatakan hal-hal seperti "hanya laporkan masalah dengan tingkat keparahan tinggi," "bersikap konservatif," atau "jangan mencari-cari kesalahan kecil," Claude Opus 4.8 mungkin mengikuti instruksi tersebut dengan lebih setia daripada model sebelumnya: model mungkin menyelidiki kode sama menyeluruhnya, mengidentifikasi bug, dan kemudian tidak melaporkan temuan yang dinilainya berada di bawah ambang batas yang Anda nyatakan. Ini dapat muncul sebagai model yang melakukan kedalaman investigasi yang sama tetapi mengonversi lebih sedikit investigasi menjadi temuan yang dilaporkan, terutama pada bug dengan tingkat keparahan lebih rendah. Presisi biasanya meningkat, tetapi recall yang terukur dapat turun meskipun kemampuan dasar model dalam menemukan bug telah meningkat.

Beberapa bahasa prompt yang direkomendasikan:

```text wrap
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

Prompt ini dapat digunakan tanpa benar-benar memiliki langkah kedua, tetapi memindahkan pemfilteran kepercayaan keluar dari langkah penemuan sering kali membantu. Jika harness Anda memiliki tahap verifikasi, deduplikasi, atau pemeringkatan terpisah, beri tahu model secara eksplisit bahwa tugasnya pada tahap penemuan adalah cakupan, bukan pemfilteran.

Jika Anda memang ingin model melakukan pemfilteran sendiri dalam satu langkah, bersikaplah konkret tentang di mana ambang batasnya alih-alih menggunakan istilah kualitatif seperti "penting": misalnya, "laporkan bug apa pun yang dapat menyebabkan perilaku yang salah, kegagalan tes, atau hasil yang menyesatkan; hanya abaikan hal-hal kecil seperti preferensi gaya atau penamaan murni."

Iterasi pada prompt terhadap subset evaluasi atau kasus uji Anda untuk memvalidasi peningkatan recall atau skor F1.

## Computer use

Kemampuan [computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool) bekerja di berbagai resolusi, hingga resolusi maksimum 2576px / 3,75MP. Pengujian computer use internal menunjukkan bahwa mengirim gambar pada 1080p memberikan keseimbangan yang baik antara performa dan biaya.

Untuk beban kerja yang sangat sensitif terhadap biaya, 720p atau 1366×768 adalah opsi dengan biaya lebih rendah dengan performa yang kuat. Lakukan pengujian Anda sendiri untuk menemukan pengaturan ideal untuk kasus penggunaan Anda; bereksperimen dengan pengaturan effort juga dapat membantu menyesuaikan perilaku model.
