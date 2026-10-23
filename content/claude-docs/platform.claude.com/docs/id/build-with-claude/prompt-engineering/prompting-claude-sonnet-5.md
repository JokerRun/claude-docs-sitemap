---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
fetched_at: 2026-10-23T02:21:28.653315Z
sha256: 38ee551c0ddd83e643caea0fc86e718273417f11f6b059fa5631e9b2cd984187
---

---
title: Prompting Claude Sonnet 5
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
description: Perbedaan perilaku dan pola prompting untuk Claude Sonnet 5, mencakup effort, default pemikiran adaptif, dan penggunaan alat.
---

Panduan ini membahas pola prompting yang spesifik untuk Claude Sonnet 5. Untuk spesifikasi model, lihat [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview). Untuk teknik yang berlaku di semua model Claude saat ini, lihat [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Claude Sonnet 5 memiliki keunggulan khusus dalam tugas coding dan agentik. Model ini berkinerja baik secara langsung pada prompt Claude Sonnet 4.6 yang sudah ada. Pola dalam panduan ini mencakup perilaku yang paling sering memerlukan penyesuaian.

## Panjang respons dan verbositas

Claude Sonnet 5 mengkalibrasi panjang respons sesuai dengan kompleksitas tugas alih-alih menggunakan verbositas tetap secara default. Ini biasanya berarti jawaban yang lebih pendek untuk pencarian sederhana dan jawaban yang lebih panjang untuk analisis terbuka.

Jika produk Anda bergantung pada gaya atau verbositas output tertentu, Anda mungkin perlu menyesuaikan prompt Anda. Sebagai contoh, untuk mengurangi verbositas, Anda dapat menambahkan:

```text wrap
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

Jika Anda melihat jenis verbositas tertentu (seperti penjelasan yang berlebihan), Anda dapat menambahkan instruksi tambahan dalam prompt Anda untuk mencegahnya. Contoh positif yang menunjukkan bagaimana Claude dapat berkomunikasi dengan tingkat keringkasan yang tepat cenderung lebih efektif daripada contoh negatif atau instruksi yang memberi tahu model apa yang tidak boleh dilakukan.

## Mengkalibrasi effort dan kedalaman pemikiran

[Parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) memungkinkan Anda menyesuaikan kecerdasan Claude terhadap penggunaan token, menukar kemampuan dengan kecepatan yang lebih tinggi dan biaya yang lebih rendah. Pada Claude Sonnet 5, effort secara default bernilai `high`, sama seperti pada Claude Sonnet 4.6. Untuk tugas coding dan agentik yang paling sulit, naikkan effort ke `xhigh`. Bereksperimenlah dengan tingkat effort lainnya untuk menyesuaikan lebih lanjut penggunaan token dan kecerdasan:

* **`max`:** Kemampuan maksimum absolut tanpa batasan pada penggunaan token.
* **`xhigh`:** Effort ekstra tinggi adalah pengaturan yang direkomendasikan untuk kasus penggunaan coding dan agentik yang paling sulit.
* **`high`:** Default. Pengaturan ini menyeimbangkan penggunaan token dan kecerdasan untuk sebagian besar kasus penggunaan.
* **`medium`:** Baik untuk kasus penggunaan yang sensitif terhadap biaya yang perlu mengurangi penggunaan token dengan mengorbankan kecerdasan.
* **`low`:** Gunakan untuk tugas singkat dengan cakupan terbatas dan beban kerja yang sensitif terhadap latensi yang tidak sensitif terhadap kecerdasan.

Sebagai pemetaan kasar lintas model saat migrasi: Claude Sonnet 5 pada medium sebanding kecerdasannya dengan Claude Sonnet 4.6 pada high, dan Claude Sonnet 5 pada high sebanding dengan Claude Sonnet 4.6 pada max. Saat melakukan benchmarking, cocokkan berdasarkan panjang pemikiran yang teramati, bukan nama effort.

Claude Sonnet 5 mematuhi tingkat effort secara ketat, terutama di tingkat rendah. Pada `low` dan `medium`, model membatasi pekerjaannya pada apa yang diminta alih-alih melakukan lebih dari yang diminta. Ini baik untuk latensi dan biaya, tetapi pada tugas yang cukup kompleks yang berjalan pada effort `low` ada risiko pemikiran yang kurang mendalam.

Jika Anda mengamati penalaran yang dangkal pada masalah kompleks, naikkan effort ke `high` atau `xhigh` alih-alih mengakalinya dengan prompt. Jika Anda perlu mempertahankan effort pada `low` demi latensi, tambahkan panduan yang terarah:

```text wrap
This task involves multistep reasoning. Think carefully through the problem before responding.
```

Pada Claude Sonnet 5, ["adaptive thinking" (pemikiran adaptif)](https://platform.claude.com/docs/id/build-with-claude/thinking) aktif secara default. Permintaan tanpa field `thinking` berjalan dengan pemikiran adaptif. Ini merupakan perubahan dari Claude Sonnet 4.6, di mana permintaan yang sama berjalan tanpa pemikiran. Untuk menonaktifkan pemikiran sepenuhnya, berikan `thinking: {type: "disabled"}`. Karena `max_tokens` adalah batas keras pada total output (pemikiran ditambah teks respons), tinjau kembali nilainya untuk beban kerja yang berjalan tanpa pemikiran pada Claude Sonnet 4.6. Jika sebelumnya Anda menggunakan pemikiran nonaktif dengan Claude Sonnet 4.6, cobalah pemikiran aktif dengan tingkat effort yang lebih rendah untuk Claude Sonnet 5.

Perilaku pemicu untuk pemikiran adaptif dapat diarahkan. Jika Anda mendapati model menghasilkan blok pemikiran lebih sering dari yang Anda inginkan, yang dapat terjadi dengan prompt sistem yang besar atau kompleks, tambahkan panduan untuk mengarahkannya. Seperti biasa, ukur efek dari setiap perubahan prompt terhadap kinerja. Contoh:

```text wrap
Thinking adds latency and should only be used when it will meaningfully improve answer quality, typically for problems that require multistep reasoning. When in doubt, respond directly.
```

Sebaliknya, jika Anda menjalankan beban kerja berat pada `medium` dan melihat pemikiran yang kurang mendalam, langkah pertama adalah menaikkan effort. Jika Anda memerlukan kontrol yang lebih halus, berikan prompt secara langsung untuk itu.

"Extended thinking" (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung pada Claude Sonnet 5 dan mengembalikan error 400. Fitur ini sudah deprecated pada Claude Sonnet 4.6 dan kini telah dihapus. Gunakan pemikiran adaptif dengan parameter effort sebagai gantinya.

<Note>
  Jika Anda menjalankan Claude Sonnet 5 pada effort `high`, `xhigh`, atau `max`, sisakan ruang di `max_tokens` agar model memiliki ruang untuk pemikiran dan pemanggilan alat. Pada tugas panjang, pemikiran adaptif dapat menggunakan sebagian besar anggaran; jika anggarannya ketat, Anda mungkin melihat respons yang hampir seluruhnya berupa pemikiran diikuti oleh jawaban yang terpotong dan `stop_reason: "max_tokens"`. Menaikkan `max_tokens` atau menurunkan ke effort `medium` akan mengatasi hal ini. Karena Claude Sonnet 5 menggunakan tokenizer baru yang menghasilkan sekitar 30% lebih banyak token untuk teks yang sama, batas `max_tokens` yang disesuaikan untuk Claude Sonnet 4.6 dapat memotong output yang setara. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja.
</Note>

## Pemicuan penggunaan alat

Claude Sonnet 5 secara default lebih agentik daripada Claude Sonnet 4.6 dan akan lebih mudah menggunakan alat serta menjalankan loop verifikasi mandiri. Dengan pemikiran dinonaktifkan, model cenderung lebih jarang menggunakan alat atau mempertimbangkan pencarian; jika Anda mengandalkan pemanggilan alat dengan pemikiran nonaktif, tambahkan dorongan eksplisit dalam prompt sistem. Effort juga merupakan pengungkit untuk penggunaan alat: pengaturan effort `high` atau `xhigh` menunjukkan penggunaan alat yang jauh lebih banyak dalam pencarian agentik dan coding. Untuk skenario di mana Anda menginginkan lebih banyak penggunaan alat, Anda juga dapat menyesuaikan prompt Anda untuk secara eksplisit menginstruksikan model tentang kapan dan bagaimana menggunakan alatnya dengan benar. Misalnya, jika Anda mendapati model tidak menggunakan alat pencarian web Anda, jelaskan dengan jelas mengapa dan bagaimana model harus menggunakannya.

## Pembaruan progres untuk pengguna

Claude Sonnet 5 memberikan pembaruan yang rutin dan berkualitas lebih tinggi kepada pengguna sepanjang jejak agentik yang panjang. Jika Anda telah menambahkan scaffolding untuk memaksa pesan status sementara ("Setelah setiap 3 pemanggilan alat, rangkum progres"), coba hapus. Jika Anda mendapati panjang atau isi pembaruan Claude Sonnet 5 untuk pengguna tidak terkalibrasi dengan baik untuk kasus penggunaan Anda, jelaskan secara eksplisit seperti apa pembaruan tersebut seharusnya dalam prompt dan berikan contoh.

## Mengikuti instruksi secara lebih harfiah

Claude Sonnet 5 menafsirkan prompt secara harfiah dan eksplisit, terutama pada tingkat effort yang lebih rendah. Model ini tidak secara diam-diam menggeneralisasi instruksi dari satu item ke item lain, dan tidak menyimpulkan permintaan yang tidak Anda buat. Keuntungan dari sifat harfiah ini adalah presisi, dan umumnya berkinerja lebih baik untuk kasus penggunaan API dengan prompt yang disesuaikan dengan cermat, ekstraksi terstruktur, dan pipeline di mana Anda menginginkan perilaku yang dapat diprediksi. Jika Anda memerlukan Claude untuk menerapkan instruksi secara luas, nyatakan cakupannya secara eksplisit (misalnya, "Terapkan format ini ke setiap bagian, bukan hanya bagian pertama").

## Nada dan gaya penulisan

Seperti halnya model baru lainnya, gaya prosa pada tulisan panjang dapat berubah. Jika produk Anda bergantung pada suara tertentu, evaluasi ulang prompt gaya terhadap baseline yang baru.

Misalnya, jika suara produk Anda lebih hangat atau lebih bersifat percakapan, tambahkan:

```text wrap
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

Jika sebelumnya Anda mengandalkan `temperature` untuk variasi gaya, perhatikan bahwa mengatur `temperature`, `top_p`, atau `top_k` mengembalikan error 400 pada Claude Sonnet 5. Batasan ini baru untuk model kelas Sonnet. Hapus parameter ini saat migrasi, dan gunakan instruksi prompt sistem untuk memandu nada dan variasi sebagai gantinya.

## Default desain dan frontend

Claude Sonnet 5 mungkin cenderung menggunakan gaya visual default yang konsisten pada brief frontend dan desain yang terbuka. Gaya bawaan default dapat terlihat baik untuk beberapa brief tetapi terasa kurang cocok untuk dashboard, alat pengembang, fintech, layanan kesehatan, atau aplikasi enterprise.

Instruksi generik ("jangan gunakan warna itu," "buat bersih dan minimalis") cenderung menggeser model ke palet tetap yang berbeda alih-alih menghasilkan variasi. Dua pendekatan bekerja dengan andal:

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

**2. Minta model mengusulkan opsi sebelum membangun.** Ini mematahkan default dan memberi pengguna kendali. Karena `temperature` tidak diterima pada Claude Sonnet 5, pendekatan ini adalah cara yang direkomendasikan untuk menghasilkan arah desain yang benar-benar berbeda di setiap eksekusi. Contoh prompt:

```text wrap
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the user to pick one, then implement only that direction.
```

Untuk menghindari pola generik yang oleh pengguna disebut estetika "AI slop", Anda dapat menyertakan arahan singkat dalam prompt sistem Anda. [Skill frontend-design](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md) memberikan pembahasan yang lebih lengkap, tetapi cuplikan ini bekerja dengan baik bersama pendekatan variasi sebelumnya:

```text wrap
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

## Produk coding interaktif

Penggunaan token dan perilaku dapat berbeda antara agen coding otonom dan asinkron dengan satu giliran pengguna dan agen coding interaktif dan sinkron dengan beberapa giliran pengguna. Untuk memaksimalkan kinerja dan efisiensi token dalam produk coding, gunakan effort `xhigh` atau `high`, tambahkan fitur otonom seperti mode otomatis, dan kurangi jumlah interaksi manusia yang diperlukan dari pengguna Anda.

Saat membatasi jumlah interaksi pengguna yang diperlukan, penting untuk menentukan tugas, maksud, dan batasan yang relevan di awal pada giliran manusia pertama. Memberikan deskripsi tugas yang terspesifikasi dengan baik, jelas, dan akurat di awal dapat membantu memaksimalkan otonomi dan kecerdasan sekaligus meminimalkan penggunaan token tambahan setelah giliran pengguna. Sebaliknya, prompt yang ambigu atau kurang terspesifikasi yang disampaikan secara bertahap selama beberapa giliran pengguna cenderung relatif mengurangi efisiensi token dan terkadang kinerja.

## Harness code review

Jika harness code review Anda disesuaikan untuk model sebelumnya, Anda mungkin awalnya melihat recall yang lebih rendah pada Claude Sonnet 5. Ini kemungkinan merupakan efek harness, bukan regresi kemampuan. Ketika prompt review mengatakan hal-hal seperti "hanya laporkan masalah dengan tingkat keparahan tinggi," "bersikaplah konservatif," atau "jangan terlalu rewel," Claude Sonnet 5 mungkin mengikuti instruksi tersebut lebih setia daripada model sebelumnya: model mungkin menyelidiki kode sama menyeluruhnya, mengidentifikasi bug, lalu tidak melaporkan temuan yang dinilainya berada di bawah standar yang Anda nyatakan. Ini dapat terlihat sebagai model melakukan investigasi dengan kedalaman yang sama tetapi mengubah lebih sedikit investigasi menjadi temuan yang dilaporkan, terutama pada bug dengan tingkat keparahan lebih rendah. Presisi biasanya meningkat, tetapi recall yang terukur dapat turun meskipun kemampuan dasar model dalam menemukan bug telah meningkat.

Beberapa bahasa prompt yang direkomendasikan:

```text wrap
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

Prompt ini dapat digunakan tanpa adanya langkah kedua yang sebenarnya, tetapi memindahkan penyaringan tingkat keyakinan keluar dari langkah penemuan sering kali membantu. Jika harness Anda memiliki tahap verifikasi, deduplikasi, atau pemeringkatan terpisah, beri tahu model secara eksplisit bahwa tugasnya pada tahap penemuan adalah cakupan, bukan penyaringan.

Jika Anda memang ingin model menyaring sendiri dalam satu kali proses, bersikaplah konkret tentang di mana standarnya alih-alih menggunakan istilah kualitatif seperti "penting": misalnya, "laporkan bug apa pun yang dapat menyebabkan perilaku yang salah, kegagalan tes, atau hasil yang menyesatkan; hanya abaikan hal-hal kecil seperti preferensi gaya atau penamaan semata."

Lakukan iterasi pada prompt terhadap subset eval atau kasus uji Anda untuk memvalidasi peningkatan recall atau skor F1.

## Computer use

Claude Sonnet 5 mendukung versi alat sebelumnya `computer_20251124` dan, di Claude API serta Claude Models on Google Cloud (Google managed), toolset `computer_toolset_20260801`. Di kedua platform tersebut, Claude Sonnet 5 juga mendukung [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) (`browser_toolset_20260801`) untuk tugas di dalam halaman web. Kemampuan [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) bekerja di berbagai resolusi, hingga resolusi maksimum 2576px / 3,75MP. Pengujian computer use internal menunjukkan bahwa mengirim gambar pada 1080p memberikan keseimbangan yang baik antara kinerja dan biaya.

Untuk beban kerja yang sangat sensitif terhadap biaya, 720p atau 1366×768 adalah opsi berbiaya lebih rendah dengan kinerja yang kuat. Lakukan pengujian Anda sendiri untuk menemukan pengaturan ideal untuk kasus penggunaan Anda; bereksperimen dengan pengaturan effort juga dapat membantu menyesuaikan perilaku model.
