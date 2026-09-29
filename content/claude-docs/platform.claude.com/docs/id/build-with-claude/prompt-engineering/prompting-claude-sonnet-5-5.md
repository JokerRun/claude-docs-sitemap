---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5
fetched_at: 2026-09-29T02:22:52.185218Z
sha256: df112a5992b3dedb2c04a524afc535e75a6f521f2e53aef1ff1b20303c377c81
---

---
title: Prompting untuk Claude Sonnet 5.5
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5
description: "Pola prompting khusus untuk Claude Sonnet 5.5: effort, inisiatif dan cakupan, berjalan tanpa pemikiran di awal, output JSON, pembaruan progres, penggunaan alat, pesan di tengah giliran, verifikasi coding, pemanggilan alat, input visual, dan penolakan."
---

Panduan ini membahas pola prompting yang khusus untuk Claude Sonnet 5.5. Untuk perubahan API pada model ini, lihat [Yang baru di Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5). Untuk teknik yang berlaku di semua model Claude saat ini, lihat [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Prompt Claude Sonnet 5 yang sudah ada seharusnya tetap berkinerja baik tanpa perubahan, dan pola dalam [Prompting untuk Claude Sonnet 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5) tetap menjadi titik awal yang wajar. Untuk pekerjaan jangka panjang yang paling sulit, model Opus adalah pilihan yang lebih baik. Mulailah dari bagian yang sesuai dengan apa yang Anda amati:

* Tidak yakin level effort mana yang harus digunakan, atau giliran berjalan lebih lama atau lebih singkat dibandingkan di Claude Sonnet 5: [Kalibrasi effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#calibrate-effort)
* Model berhenti untuk meminta konfirmasi sebelum tugas coding selesai, atau melakukan lebih dari yang Anda minta: [Arahkan inisiatif dan cakupan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#steer-initiative-and-scope)
* Integrasi Anda saat ini berjalan dengan pemikiran dinonaktifkan: [Berjalan tanpa pemikiran di awal](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#running-without-up-front-thinking)
* Jawaban JSON untuk tugas yang memerlukan beberapa langkah penyelesaian salah atau tidak dapat di-parse: [Tugas penalaran dengan output JSON](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#reasoning-tasks-with-json-output)
* Giliran agentik yang panjang tampak diam: [Pembaruan progres untuk pengguna](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#user-facing-progress-updates)
* Model menjawab dari pengetahuan pelatihannya padahal pencarian akan menangkap detail yang telah berubah: [Penggunaan alat dalam chat dan pekerjaan pengetahuan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#tool-use-in-chat-and-knowledge-work)
* Pesan yang dikirim pengguna di tengah tugas diabaikan atau diperlakukan sebagai teks yang disisipkan: [Pesan pengguna di tengah giliran](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#mid-turn-user-messages-and-task-budgets)
* Perubahan kode dilaporkan selesai tanpa menjalankan tes atau build: [Verifikasi pada tugas coding](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#verification-on-coding-tasks)
* Model memanggil alat dengan huruf besar/kecil yang salah atau meneruskan parameter dengan nama yang sedikit berbeda: [Penanganan pemanggilan alat yang toleran](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#tolerant-tool-call-handling)
* Jawaban tentang grafik padat atau gambar teknis melewatkan detail: [Alat untuk input visual yang kompleks](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#tools-for-complex-visual-inputs)
* Permintaan mengembalikan `stop_reason: "refusal"`: [Penolakan safeguard](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#safeguard-refusals)

<Note>
  Untuk lima perubahan API yang bersifat breaking saat bermigrasi dari Claude Sonnet 5, lihat [panduan migrasi](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#migrating-from-claude-sonnet-5).
</Note>

## Kalibrasi effort

[Effort](https://platform.claude.com/docs/id/build-with-claude/effort) adalah kontrol utama untuk seberapa banyak Claude Sonnet 5.5 berpikir, dan bersamanya kualitas, "latency" (latensi), dan biaya. Level-levelnya telah dikalibrasi ulang: suatu level tidak menghasilkan jumlah pemikiran yang sama dengan level yang sama di Claude Sonnet 5. Jalankan pengujian ulang terhadap eval Anda sendiri alih-alih membawa pengaturan yang Anda gunakan di Claude Sonnet 5. Mulailah dari `high`, default di Claude API, kecuali beban kerja Anda bersifat agentik atau sensitif terhadap latensi. Untuk coding agentik dan penggunaan alat multilangkah, mulailah dari `medium` untuk tugas yang terdefinisi dengan baik dan naikkan ke `high` untuk tugas yang lebih sulit atau lebih panjang. Untuk chat dan pekerjaan lain yang sensitif terhadap latensi, mulailah dari `medium` atau `low`, karena effort yang lebih tinggi berarti waktu tunggu yang lebih lama sebelum balasan dimulai. Naikkan effort jika kualitas membutuhkannya.

Effort yang lebih rendah juga mengubah cara model menyelesaikan pekerjaan agentik. Pada `low`, model menjaga pemikirannya tetap singkat dan dapat melewatkan verifikasi perubahan. Lihat [Verifikasi pada tugas coding](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#verification-on-coding-tasks). Pada `low` dan `medium`, dalam tugas agentik yang panjang, model lebih mungkin berhenti dan meminta konfirmasi kepada pengguna sebelum selesai. Lihat [Arahkan inisiatif dan cakupan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#steer-initiative-and-scope).

Tiga penyesuaian dapat membantu:

* Atur `max_tokens` dengan ruang untuk pemikiran dan balasan yang Anda harapkan. Pemikiran dihitung dalam `max_tokens` bahkan ketika konten pemikiran tidak dikembalikan kepada Anda. Batas yang diukur untuk permintaan tanpa pemikiran dapat memotong balasan. Untuk coding agentik, atur `max_tokens` ke 128.000, nilai maksimum model, dan lakukan [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming) pada respons.
* Simpan `xhigh` dan `max` untuk pekerjaan di mana Anda telah mengukur peningkatan kualitas, karena pemikiran dan balasan menjadi jauh lebih panjang di level tersebut. Pada level tersebut, `between_tools` tidak diterima, sehingga pemikiran di awal tidak dapat dinonaktifkan.
* Untuk mendapatkan pemikiran yang lebih sedikit, turunkan level effort. Mulai dari `medium` ke atas, model berpikir sebentar sebelum hampir setiap balasan, bahkan untuk sapaan, yang menambah waktu sebelum token pertama yang terlihat. Meminta model dalam prompt sistem untuk berpikir lebih sedikit tidak secara andal mengurangi pemikirannya. Pada `low`, model melewatkan pemikiran pada sebagian besar permintaan sederhana.

Mengubah nilai `effort` tingkat atas di antara permintaan akan membatalkan cache prompt. Untuk menjalankan giliran tertentu pada level yang berbeda, gunakan [perubahan effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) (beta) sebagai gantinya, yang mempertahankan cache. Misalnya, jalankan sesi interaktif pada `low` dan naikkan effort ke `high` ketika pengguna mengajukan masalah yang sulit. Perubahan effort per pesan memerlukan pemikiran adaptif. Dengan `between_tools`, perubahan tersebut mengembalikan error 400, seperti yang dijelaskan dalam [Berjalan tanpa pemikiran di awal](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#running-without-up-front-thinking).

## Arahkan inisiatif dan cakupan

Seberapa jauh Claude Sonnet 5.5 bertindak sendiri bergantung pada level effort dan permintaannya. Pada effort yang lebih rendah, model terkadang meminta konfirmasi sebelum tugas coding selesai. Pada effort yang lebih tinggi, atau pada permintaan yang terbuka, model dapat melakukan lebih dari yang Anda minta. Arahkan model dengan level effort dan dengan instruksi dalam prompt sistem Anda.

**Menuntaskan pekerjaan.** Pada tugas coding agentik dengan effort `low` dan `medium`, model terkadang meminta konfirmasi sebelum pekerjaan selesai. Model mungkin berhenti untuk mengonfirmasi rencana, mengajukan pertanyaan yang sebenarnya dapat dijawabnya sendiri, atau berhenti setelah satu bagian dari tugas multibagian untuk menanyakan apakah harus melanjutkan. Coba level effort yang lebih tinggi terlebih dahulu. Agar model tetap bekerja tanpa mengubah effort, tambahkan ini ke prompt sistem Anda:

```text wrap
Keep working until everything the user asked for is done, and only stop to ask when you can't go on without the user or before a risky step.

When the work the user asked for is done and checked, stop and report. Don't add features, tests, files, docs or refactors that weren't asked for. If you think one would help, mention it at the end instead of doing it.
```

Dengan prompt ini, model menuntaskan lebih banyak pekerjaan pada effort `low` dan `medium`, sehingga sesi pada level tersebut berjalan lebih lama dan lebih mahal. Prompt ini tidak menggantikan aturan Anda sendiri tentang tindakan yang berisiko atau tidak dapat dibatalkan. Tetap simpan aturan tersebut dalam prompt sistem Anda.

**Tambahan yang tidak diminta saat coding.** Model cenderung menambahkan tes, dokumentasi, dan file pendukung kecil yang sesuai dengan konvensi repositori Anda, bahkan ketika Anda tidak memintanya. Model melakukan ini di setiap level effort, dan lebih banyak pada effort yang lebih tinggi. Perubahan yang diminta itu sendiri tetap dekat dengan apa yang diminta. Sebagian besar tim akan menyambut baik hal ini. Jika Anda lebih suka perubahan dibatasi pada apa yang diminta secara eksplisit, tambahkan hanya paragraf kedua dari prompt tersebut, yang dimulai dengan "When the work the user asked for is done". Pada effort `xhigh` dan `max`, paragraf tersebut mengurangi tambahan ini dan membuat perubahan secara keseluruhan lebih kecil.

**Ketelitian pada effort `xhigh` dan `max`.** Pada level ini, model sangat teliti. Setelah menyelesaikan tugas, model dapat memulai putaran tinjauan dan verifikasinya sendiri, terkadang dengan "subagents" (subagen) jika "harness" (kerangka kerja agen) Anda menyediakannya. Model juga dapat melakukan perbaikan terkait yang diperhatikannya di sepanjang jalan. Ini membutuhkan lebih banyak waktu dan token, jadi jalankan pekerjaan rutin pada `high` atau di bawahnya, di mana hal ini jarang terjadi. Jika Anda memang menginginkan ketelitian ekstra dari level effort ini, tetapi ingin mengarahkannya pada tugas itu sendiri, tambahkan ini ke prompt sistem Anda:

```text wrap
When the work the user asked for is done and its checks pass, stop and report. Don't start extra rounds of review or hardening on your own, and don't launch reviewer sub-agents unless the user asked for a review. If you think a deeper review is worth doing, say so at the end.
```

Dalam pengujian pada tugas coding dengan effort `max`, ini menghentikan model meluncurkan subagen peninjau dan memangkas biaya sesi sekitar sepertiga, tanpa perubahan kualitas. Ini membuat putaran tinjauan yang dimulai sendiri oleh agen utama lebih jarang tetapi tidak menghilangkannya sepenuhnya.

**Permintaan terbuka.** Ketika permintaan bersifat terbuka, misalnya "tunjukkan apa yang bisa Anda lakukan dengan ini", model dapat mulai membuat presentasi, laporan, atau video padahal Anda hanya menginginkan ide. Jika Anda menginginkan ide atau rencana terlebih dahulu, nyatakan hal itu dalam permintaan, atau tambahkan ini ke prompt sistem Anda:

```text wrap
When the user asks for ideas, options or a plan, give them that and stop. Don't start building or changing anything until they say to go ahead.
```

## Berjalan tanpa pemikiran di awal

Untuk menjalankan Claude Sonnet 5.5 tanpa pemikiran di awal, kirim `thinking: {"type": "between_tools"}`. Ini adalah pengaturan pemikiran terendah pada model ini, dan diterima pada effort `high` atau di bawahnya. Jika integrasi Anda saat ini berjalan dengan pemikiran dinonaktifkan, alihkan ke `between_tools` dan periksa poin-poin berikut:

* **Kirim `between_tools` pada effort `high` atau di bawahnya.** Pada effort `xhigh` atau `max`, permintaan dengan `between_tools` mengembalikan error 400. Dengan `between_tools`, effort juga tidak dapat diubah di tengah percakapan: `output_config.effort` per pesan yang berbeda dari level yang berlaku mengembalikan error 400. Untuk memvariasikan effort per giliran, gunakan pemikiran adaptif. Dengan `between_tools`, hapus instruksi apa pun yang memberi tahu model untuk tidak berpikir. Instruksi semacam itu membuat model lebih mungkin menulis tag XML internal dalam output yang terlihat.
* **Baca respons berdasarkan tipe blok.** Dengan pemikiran adaptif, respons dapat dimulai dengan blok `thinking`, yang field `thinking`-nya kosong di bawah default `display: "omitted"`. Dengan `between_tools`, respons dapat dimulai dengan blok `thinking` pembaruan progres. Jangan berasumsi bahwa blok konten pertama adalah teks.
* **Kembalikan blok `thinking` tanpa perubahan.** Dengan `between_tools`, catatan yang ditulis model di antara pemanggilan alat tetap dikembalikan sebagai blok `thinking` ketika panjangnya lebih dari satu atau dua kalimat. Setiap blok membawa ringkasan dari catatan tersebut. Kembalikan blok-blok tersebut tanpa perubahan bersama sisa giliran asisten. Blok yang Anda kirim kembali memberi model catatan lengkap yang ditulisnya, bukan ringkasannya.
* **Gunakan pemikiran adaptif untuk tugas penalaran tanpa alat.** Dalam permintaan tanpa alat, `between_tools` berarti model menjawab tanpa berpikir terlebih dahulu. Untuk tugas yang memerlukan beberapa langkah penyelesaian, gunakan pemikiran adaptif sebagai gantinya. Lihat [Tugas penalaran dengan output JSON](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#reasoning-tasks-with-json-output).

## Tugas penalaran dengan output JSON

Bagian ini berlaku ketika Anda meminta Claude Sonnet 5.5 memberikan jawaban JSON untuk tugas yang memerlukan beberapa langkah penyelesaian. Contohnya termasuk menjumlahkan angka dari dokumen, menerapkan aturan, atau mengurutkan item. Pada tugas seperti ini, model sering menjawab tanpa berpikir terlebih dahulu, terutama pada effort `low` dan `medium`. Apa yang membantu bergantung pada cara Anda meminta JSON. Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-outputs) (output terstruktur) jika tersedia. Teks respons kemudian berupa JSON yang sesuai dengan skema Anda, sehingga tidak ada yang perlu di-parse.

Dengan output terstruktur, teks respons hanya berisi JSON, sehingga model hanya dapat menyelesaikan masalah dalam pemikirannya. Ketika model melewatkan pemikiran, akurasinya pada tugas ini dapat menurun. Perubahan berikut membantu menjaga akurasi tetap tinggi.

**Minta model untuk berpikir terlebih dahulu.** Dengan pemikiran adaptif, tambahkan baris ini di akhir prompt sistem Anda:

```text wrap
Think the problem through before you answer.
```

Dengan baris ini, model lebih sering berpikir sebelum menjawab. Pada effort `high`, baris ini membawa akurasi mendekati apa yang dicapai model pada `xhigh`, dengan peningkatan token output yang moderat. Pada effort `low` dan `medium`, baris ini meningkatkan akurasi, meskipun tidak sampai ke tingkat yang dicapai model pada `high`, dan peningkatan token output-nya lebih besar.

**Atau gunakan effort `xhigh`.** Dengan pemikiran adaptif, `xhigh` memberikan akurasi tertinggi pada tugas ini bahkan tanpa baris tersebut. Level ini menggunakan lebih banyak token output dibandingkan `high`.

**Gunakan pemikiran adaptif alih-alih `between_tools`.** Dalam permintaan tanpa alat, model tidak berpikir sebelum menjawab di bawah `between_tools`. Baris tersebut tidak berpengaruh di sana, dan akurasi pada tugas ini lebih rendah. Gunakan pemikiran adaptif untuk permintaan ini, dengan langkah-langkah di bagian ini. Dalam pengujian, memecah permintaan menjadi dua, satu permintaan untuk jawaban dan satu untuk JSON, menghasilkan akurasi jawaban dan kepatuhan JSON yang tinggi, tetapi dengan biaya dan latensi yang sangat tinggi.

Dengan output terstruktur pada effort `low` dan `medium`, model sesekali terus berpikir hingga mencapai `max_tokens`. Pada effort `high` ke atas, hal ini hampir tidak pernah terjadi. Perlakukan setiap respons yang `stop_reason`-nya adalah `"max_tokens"` sebagai gagal, meskipun teksnya berisi JSON yang valid, dan coba lagi. Atur `max_tokens` cukup tinggi untuk pemikiran dan JSON, seperti yang dijelaskan dalam [Kalibrasi effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#calibrate-effort), tetapi tidak lebih tinggi dari yang bersedia Anda keluarkan untuk satu percobaan.

Jika Anda tidak dapat menggunakan output terstruktur, minta JSON dalam prompt sebagai gantinya. Model kemudian sering menyelesaikan masalah dalam teks respons dan menulis JSON di akhir. JSON biasanya berisi jawaban yang benar, tetapi parser yang mengharapkan seluruh respons berupa JSON akan gagal. Dua hal dapat membantu:

* **Parse nilai JSON terakhir dalam respons.** Baca hanya blok `text`, dan perlakukan respons yang `stop_reason`-nya adalah `"max_tokens"` sebagai gagal. Mulai dari setiap `{` atau `[`, coba parse nilai JSON. Ketika satu nilai berhasil di-parse, lanjutkan dari akhir nilai tersebut, sehingga nilai yang bersarang di dalamnya tidak dihitung secara terpisah. Simpan nilai terakhir yang ditemukan. Jangan mengambil semuanya dari `{` pertama hingga `}` terakhir. Model sesekali menulis draf sebelum JSON finalnya, dan rentang tersebut akan mencakup keduanya. Jika jawaban Anda berupa beberapa nilai JSON berturut-turut, seperti satu record per baris, simpan rangkaian nilai terakhir yang hanya dipisahkan oleh spasi, koma, atau baris baru. Periksa bahwa hasilnya memiliki field yang Anda harapkan, dan coba lagi sekali jika tidak. Dalam pengujian, ini membuat hampir setiap respons dapat digunakan tanpa mengubah akurasinya.
* **Pertimbangkan juga effort `xhigh` dengan pemikiran adaptif.** Model kemudian menyelesaikan masalah dalam pemikirannya dan hampir selalu mengembalikan JSON saja. Total token output tetap kurang lebih sama dengan pada `high`, karena proses penyelesaian berpindah dari teks respons ke dalam pemikiran.

## Pembaruan progres untuk pengguna

Di antara pemanggilan alat, Claude Sonnet 5.5 menulis catatan untuk pengguna tentang apa yang baru saja ditemukannya dan apa yang akan dilakukannya selanjutnya. Catatan yang lebih panjang dari satu atau dua kalimat dikembalikan sebagai [blok `thinking` pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates). Komentar yang lebih pendek tetap berupa `text`. Pada `thinking.display` default, teks blok pembaruan progres kosong, sehingga klien yang hanya merender blok `text` dapat tampak diam selama giliran agentik yang panjang. Hal ini paling penting dalam antarmuka chat dan produk lain di mana pengguna mengikuti pekerjaan model secara real-time.

Untuk menampilkan catatan ini, atur `display: "updates"` (beta, header `thinking-display-updates-2026-08-18`). Dengan `between_tools`, catatan dikembalikan beserta teks ringkasannya, sehingga field `display` tidak diperlukan. `between_tools` tidak menerima field lain: `display`, `budget_tokens`, atau `block_binding` yang dikirim bersamanya mengembalikan error 400. [Panduan migrasi](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#text-between-tool-calls) menunjukkan cara merender catatan tersebut. Terkadang model perlu menampilkan teks persis kepada pengguna di tengah giliran yang panjang, seperti cuplikan kode atau pertanyaan yang perlu dijawab. Untuk kasus tersebut, berikan model alat sederhana untuk mengirim pesan kepada pengguna. Beri tahu model untuk menggunakan alat tersebut hanya untuk konten semacam itu. Deklarasikan alat tersebut dalam permintaan pertama sesi, sehingga daftar `tools` tidak berubah di kemudian hari.

Selanjutnya, hapus instruksi lama seperti "simpan semua temuan untuk respons akhir". Jika Anda kemudian menginginkan pembaruan pada titik-titik yang dapat diprediksi, misalnya satu baris tentang apa yang akan dilakukan model sebelum pemanggilan alat pertamanya dan rekap singkat di akhir, nyatakan hal itu dalam prompt sistem. Model mengikuti instruksi seperti ini. Pembaruan pada titik-titik yang ditetapkan paling membantu dalam pekerjaan "human-in-the-loop" (dengan keterlibatan manusia).

Jika giliran pemanggilan alat yang panjang masih diam lebih lama dari yang Anda inginkan, harness Anda dapat memicu pembaruan. Minta harness menghitung langkah pemanggilan alat berturut-turut yang tidak mengirimkan teks atau pembaruan progres kepada pengguna. Setelah beberapa langkah berturut-turut, misalnya lima, tambahkan pengingat satu giliran setelah hasil alat terbaru. Kirim sebagai [pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) (beta), dengan teks seperti ini:

```text wrap
The user hasn't heard from you in a while — say in a few words what you're doing, then continue.
```

Jika giliran tetap diam, berhentilah mengirim pengingat setelah yang kedua atau ketiga. Teks harness yang sering muncul setelah hasil alat dapat membuat model mencurigai adanya "prompt injection" (injeksi prompt), seperti yang dijelaskan dalam [Pesan pengguna di tengah giliran](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#mid-turn-user-messages-and-task-budgets). Biarkan setiap pengingat tetap ada di `messages` pada permintaan berikutnya. Karena pengingat ditambahkan di akhir alih-alih disisipkan lalu dihapus kemudian, cache prompt dan [pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking) tetap utuh. Pada effort `high`, dengan tersedianya alat untuk mengirim pesan kepada pengguna, pengingat tersebut membuat model lebih sering memberi pembaruan kepada pengguna dan memperpendek rentang diam terpanjangnya, tanpa perubahan kualitas tugas yang terukur.

## Penggunaan alat dalam chat dan pekerjaan pengetahuan

Pada tugas chat dan pekerjaan pengetahuan, Claude Sonnet 5.5 terkadang menjawab dari pengetahuan pelatihannya padahal pencarian web akan menangkap detail yang telah berubah. Contohnya termasuk apa yang diizinkan, diwajibkan, atau dikenakan biaya.

Pertama, periksa prompt Anda untuk bahasa yang menghambat penggunaan alat, seperti "hanya gunakan alat jika benar-benar diperlukan" atau "minimalkan pemanggilan alat", dan hapus. Kemudian, jika produk Anda memberi model alat pencarian, tambahkan ini ke prompt sistem Anda:

```text wrap
Use the search tool to check specifics that may have changed since your training, such as what is allowed, required or charged, even when you feel confident. For researched work such as a report or a comparison, gather current sources rather than writing from your training knowledge.
```

Hal ini paling penting untuk produk riset dan dukungan, di mana jawaban bergantung pada detail terkini.

## Pesan pengguna di tengah giliran

Claude Sonnet 5.5 dilatih untuk menahan injeksi prompt tidak langsung, yaitu instruksi berbahaya yang datang melalui hasil alat dan konten lain yang dibacanya selama tugas. Terkadang model memperlakukan pesan pengguna yang asli sebagai kemungkinan injeksi. Misalkan pesan yang diketik pengguna di tengah tugas sampai ke model sebagai [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) yang ditempatkan langsung setelah hasil alat, atau di dalam blok `tool_result`. Model kemudian dapat memberi tahu pengguna bahwa hasil alat berisi teks yang menyamar sebagai pesan dari mereka, lalu mengabaikan pesan tersebut atau meminta pengguna untuk mengonfirmasinya.

Hitungan mundur token yang ditambahkan harness Anda setelah setiap hasil alat dapat menyebabkan hal ini. Begitu pula dengan mengizinkan pengguna mengirim pesan saat model sedang berada di tengah giliran multilangkah, atau membuat harness Anda menambahkan instruksi atau konteks setelah hasil alat di setiap langkah. Dalam setiap kasus, teks datang tepat setelah hasil alat. Dengan hitungan mundur atau instruksi per langkah, hal itu dapat terjadi pada setiap pemanggilan alat. Pengingat satu giliran yang sesekali, seperti yang ada di [Pembaruan progres untuk pengguna](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#user-facing-progress-updates), datang jauh lebih jarang. Jika Anda melihat reaksi ini terhadap pengingat Anda sendiri, kirim pengingat lebih jarang. Untuk menghindari salah tafsir:

* Jangan pernah menempatkan teks pengguna di dalam blok `tool_result`. Model paling sering salah menafsirkan penempatan tersebut.
* Sampaikan input pengguna di tengah giliran sebagai giliran pengguna. Tambahkan kata-kata pengguna sebagai blok teks dalam pesan pengguna yang membawa blok `tool_result`, setelah `tool_result` terakhir.
* Simpan pemberitahuan harness, seperti pengingat, dalam pesan sistem di tengah percakapan yang terpisah setelah kata-kata pengguna. Jangan pernah menempatkan pemberitahuan dan kata-kata pengguna dalam blok yang sama.
* Dalam sesi interaktif di mana pengguna dapat mengetik di tengah giliran, jangan tambahkan hitungan mundur token atau anggaran Anda sendiri setelah hasil alat. [Task budgets](https://platform.claude.com/docs/id/build-with-claude/task-budgets) (anggaran tugas) (beta) menambahkan hitungan mundur serupa, tetapi belum terlihat menyebabkan salah tafsir ini. Jika Anda melihat salah tafsir saat anggaran tugas diatur, coba sesi tanpa anggaran tugas.

## Verifikasi pada tugas coding

Pada tugas coding agentik, Claude Sonnet 5.5 umumnya memeriksa pekerjaannya sebelum melaporkan perubahan sebagai selesai. Namun, pada effort `low`, model terkadang melaporkan perubahan sebagai selesai tanpa menjalankan pemeriksaan yang menguji perubahan tersebut. Misalnya, model mungkin melewatkan tes proyek karena dependensi proyek belum terinstal.

Jika Anda melihat perubahan dilaporkan selesai tanpa output tes atau build dalam transkrip, tambahkan paragraf ini, atau yang serupa, ke prompt sistem. Pada effort `low`, paragraf ini membuat pemeriksaan yang dilewati atau dangkal menjadi jarang, tanpa perubahan kualitas tugas yang terukur dan hanya dengan biaya per tugas yang sedikit lebih tinggi:

```text wrap
When you change code that can be run, built, or type-checked, run a real check that exercises the change before reporting it done: the project's tests, type-checker, or build, or the changed command itself. A syntax-only check, or a check command that failed to start, does not count; if all that is missing is the project's declared dependencies, install them with its own package manager and lockfile (e.g. npm install, pip install -r requirements.txt), never via sudo or the system package manager, unless told not to. Only if no real check can run here, say which one you did not run and why instead of reporting the change as done.
```

## Penanganan pemanggilan alat yang toleran

Claude Sonnet 5.5 sesekali memanggil alat yang dideklarasikan dengan nama yang hanya berbeda dalam huruf besar/kecil, seperti `bash` untuk `Bash`. Model juga dapat meneruskan parameter yang dikenal dengan nama yang sedikit berbeda. Alih-alih memperlakukan pemanggilan seperti itu sebagai error fatal, minta harness Anda menanganinya dengan salah satu dari dua cara:

* Terima pemanggilan ketika kecocokannya tidak ambigu, meskipun huruf besar/kecilnya salah.
* Kembalikan `tool_result` dengan `is_error: true` yang menyebutkan nama persis yang diharapkan. Model biasanya memperbaiki pemanggilan pada giliran berikutnya. Lihat [Menangani error dengan `is_error`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/handle-tool-calls#handling-errors-with-is-error).

## Alat untuk input visual yang kompleks

Untuk grafik padat dan gambar teknis, berikan Claude Sonnet 5.5 cara untuk memotong, memperbesar, atau menjalankan kode pada gambar. Dengan alat seperti itu, model membaca input ini dengan jauh lebih akurat. Pada grafik, alat membantu di setiap level effort. Pada gambar teknis, alat hanya membantu mulai dari effort `high` ke atas, dan paling banyak pada `xhigh` dan `max`. Untuk grafik, menambahkan alat lebih membantu daripada menaikkan effort: dalam pengujian, dengan alat pada effort `high`, model membaca grafik lebih akurat dibandingkan tanpa alat pada effort `max`, dengan biaya yang jauh lebih kecil. [Resep alat crop](https://platform.claude.com/cookbook/multimodal-crop-tool) memiliki definisi alat yang berfungsi.

## Penolakan safeguard

Claude Sonnet 5.5 menjalankan pengklasifikasi keamanan yang dapat menolak permintaan. Penolakan datang sebagai respons normal dengan `stop_reason: "refusal"`, dan `stop_details.category` menyebutkan [kategori penolakan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response):

* `cyber`: permintaan dapat memungkinkan bahaya siber, seperti pengembangan malware atau exploit. Menemukan kerentanan dalam kode sumber diizinkan. Pekerjaan keamanan siber berisiko tinggi yang bersifat penggunaan ganda tidak diizinkan.
* `bio`: permintaan dapat memungkinkan bahaya biologis, seperti metode laboratorium yang berbahaya. Pertanyaan kesehatan sehari-hari dan pertanyaan edukatif tidak terpengaruh.
* `frontier_llm`: permintaan dapat membantu pengembangan model AI pesaing.
* `reasoning_extraction`: permintaan meminta model untuk mereproduksi penalaran internalnya dalam teks respons.
* `general_harms`: permintaan termasuk dalam area kebijakan penggunaan lainnya. Pekerjaan yang tidak berbahaya juga dapat memicu kategori ini.

Jika pengklasifikasi `bio` memblokir pekerjaan ilmu hayati organisasi Anda, Anda dapat mendaftar ke [Life Sciences Verification Program](https://www.anthropic.com/news/life-sciences-verification-program).

Jika Anda mengaktifkan [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback) (beta), fitur ini mencoba ulang penolakan `cyber` dan `frontier_llm` pada Claude Sonnet 5. Fitur ini tidak mencoba ulang penolakan `bio`, `reasoning_extraction`, atau `general_harms`. Lihat [Penolakan, fallback, dan penagihan](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#refusals-fallback-and-billing).

Jika prompt Anda meminta model untuk menyertakan penalarannya dalam respons, hapus instruksi tersebut, karena instruksi itu memicu penolakan `reasoning_extraction`. Dengan pemikiran adaptif, baca penalaran dari blok [pemikiran yang diringkas](https://platform.claude.com/docs/id/build-with-claude/thinking#summarized-thinking) sebagai gantinya (`display: "summarized"`).
