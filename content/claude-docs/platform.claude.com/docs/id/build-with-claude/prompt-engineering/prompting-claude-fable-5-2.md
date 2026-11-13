---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: e28f708afd2b4b64aba8a87facf6df280276f951c37beaba67cb02907954a47c
---

---
title: Prompting Claude Fable 5.2
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
description: "Pola prompting khusus untuk Claude Fable 5.2 dan Claude Mythos 5.2: effort, berhenti lebih awal, persetujuan, kepemilikan kode, pembaruan progres, subagen, kehati-hatian yang menumpuk, prompt dan harness yang dirancang untuk model sebelumnya, laporan akhir, dan penolakan."
---

Panduan ini membahas pola prompting yang khusus untuk Claude Fable 5.2. Untuk kemampuan model dan perubahan API, lihat [Yang baru di Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2) dan [panduan migrasi Claude Fable 5.2 dan Claude Mythos 5.2](https://platform.claude.com/docs/id/models/fable-5-2/migration-guide). Untuk teknik yang berlaku di semua model Claude saat ini, lihat [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Claude Fable 5.2 berperilaku berbeda dari model sebelumnya dalam beberapa hal. Mulailah dengan bagian yang sesuai dengan apa yang Anda amati:

* Tidak yakin level effort mana yang harus dijalankan, atau permintaan sederhana lambat dimulai: [Kalibrasi effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#calibrate-effort)
* Sebuah giliran berakhir sebelum pekerjaan selesai: [Selesaikan seluruh tugas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#finish-the-whole-task)
* Agen coding menyalin kode yang sudah ada, atau melaporkan masalah dan membiarkannya: [Nyatakan siapa pemilik kode](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#say-who-owns-the-code)
* Giliran agentik yang panjang tampak senyap: [Jaga agar pengguna tetap mendapat informasi selama giliran yang panjang](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#keep-users-informed-during-long-turns)
* Sesi agen memulai lebih banyak subagen daripada yang dibutuhkan tugas: [Tetapkan ekspektasi untuk subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#set-expectations-for-subagents)
* Agen meminta persetujuan yang tidak mereka perlukan, atau menahan pekerjaan rutin: [Cegah kehati-hatian menumpuk](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#keep-caution-from-piling-up)
* Prompt sistem, skill, atau harness Anda ditulis untuk Claude Fable 5.1 atau Claude Opus 5.5: [Tinjau prompt dan harness yang dirancang untuk model sebelumnya](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#review-instructions-written-for-earlier-models)
* Pengguna Anda membaca laporan akhir atau serah terima setelah tugas panjang: [Buat laporan mudah diikuti](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#make-reports-easy-to-follow)
* Permintaan mengembalikan `stop_reason: "refusal"`: [Penolakan safeguard](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#safeguard-refusals)

<Note>
  Untuk urutan penerapan panduan ini saat Anda bermigrasi, lihat [Dari mana memulai](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#where-to-start).

  Beberapa bagian di halaman ini menyarankan teks untuk ditambahkan ke prompt sistem Anda atau perubahan pada deskripsi alat. Beberapa bagian juga menyarankan baris untuk dihapus dari prompt sistem atau dari catatan dan aturan yang dibawa agen Anda. Lakukan perubahan ini hanya pada percakapan baru. Pada Claude Fable 5.2, permintaan yang gagal dalam [pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#prefix-check) mendapatkan [error 400](https://platform.claude.com/docs/id/api/errors#thinking-block-conversation-mismatch). Jika Anda melanjutkan percakapan tersimpan setelah Anda mengubah `system`, `tools`, atau pesan sebelumnya, permintaan tersebut dapat gagal dalam pemeriksaan prefiks. Untuk mengubah instruksi di tengah percakapan, [letakkan instruksi tersebut di giliran terbaru](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#changing-context). Jika [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) tersedia, Anda dapat [menambahkan pesan sistem ke percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#new-instructions) sebagai gantinya.
</Note>

## Kalibrasi effort

Pada Claude Fable 5.2, level [effort](https://platform.claude.com/docs/id/build-with-claude/effort) menentukan seberapa banyak model berpikir, berapa banyak panggilan alat yang dibuatnya, berapa lama sebuah giliran berlangsung, dan berapa banyak token yang digunakannya. Setel level effort bersamaan dengan prompt Anda.

Mulailah dari `high`, nilai default untuk Claude Fable 5.2 di Claude API. Bergantung pada kasus penggunaan, Anda mungkin menaikkan atau menurunkan effort, sambil menguji terhadap eval Anda sendiri. Level effort memiliki urutan yang sama di seluruh model Claude, tetapi jumlah pemikiran pada setiap level dapat berbeda. Jadi, jalankan ulang pengujian effort Anda alih-alih membawa pengaturan yang Anda setel pada Claude Fable 5.1 atau Claude Opus 5.5.

* `low` cocok untuk interaksi bolak-balik yang cepat, tugas yang terdefinisi dengan baik, dan beban kerja bervolume tinggi (misalnya, subagen yang cerdas dan cepat). Pada evaluasi coding, Claude Fable 5.2 berkinerja lebih baik daripada model sebelumnya pada effort `low`. Dalam pengujian Anthropic, skornya mendekati skor Claude Fable 5.1 pada effort yang lebih tinggi.
* `medium` cocok untuk coding interaktif, chat, dan pekerjaan pengetahuan sehari-hari.
* `high` cocok untuk coding yang sulit, riset, pekerjaan agentik, dan eksekusi panjang tanpa pengawasan. Giliran memakan waktu jauh lebih lama untuk selesai dibandingkan pada `medium`.
* `xhigh` ditujukan untuk pekerjaan coding dan agentik jangka panjang Anda yang paling sulit, di mana Anda telah mengukur adanya peningkatan. Level ini sedikit menaikkan skor pada evaluasi coding internal Anthropic dan menggunakan jauh lebih banyak token.
* `max` ditujukan untuk mengukur batas kemampuan model atau untuk tugas langka di mana waktu dan token tidak menjadi masalah. Paling masuk akal menggunakan `max` untuk masalah terbuka seperti penemuan ilmiah dan matematika. Giliran berjalan lambat dan menggunakan jauh lebih banyak token dibandingkan pada `xhigh`.

Anda mendapatkan sebagian besar peningkatan kemampuan saat menggunakan effort `high`. Langkah dari `medium` ke `high` menaikkan skor pada sebagian besar evaluasi coding dan pekerjaan pengetahuan yang dilacak Anthropic. Langkah tersebut juga menggunakan lebih banyak token dan waktu, jadi turunkan ke `medium` di mana pun eval Anda tetap terjaga. Di atas `high`, peningkatannya tidak merata dan bergantung pada tugas.

Untuk pekerjaan agentik pada `low` atau `medium`, tambahkan teks di [Selesaikan seluruh tugas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#finish-the-whole-task). Model lebih mungkin berhenti lebih awal pada level effort yang lebih rendah.

Pada `high` ke atas, model berpikir sebelum hampir setiap balasan, termasuk balasan untuk sapaan. Jika Anda mendapati permintaan dasar memakan waktu cukup lama atau biayanya lebih besar, gunakan effort yang lebih rendah untuk giliran tersebut. Dalam pengujian Anthropic, instruksi untuk menjawab langsung tanpa berpikir panjang tidak menghentikan model dari berpikir pada `medium` ke atas.

Effort hanya berpengaruh kecil terhadap panjang respons giliran asisten. Gunakan prompting untuk mengubah panjang dan nada balasan.

Anda juga dapat mencampur level dalam satu alur kerja. Misalnya, Anda dapat merencanakan dan beriterasi dengan model pada `medium`, lalu menaikkan effort untuk bagian panjang tanpa pengawasan. Untuk mengubah level di dalam percakapan dan mempertahankan cache prompt, gunakan [Effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort-per-message) (beta, header `mid-conversation-output-config-2026-07-01`). Halaman tersebut mencantumkan platform tempat fitur ini tersedia. Sebuah perubahan berlaku hingga perubahan lain menggantikannya. Jika effort per pesan tidak tersedia, tetapkan nilai `effort` tingkat atas yang baru pada permintaan berikutnya, yang dapat membuat pesan yang di-cache menjadi tidak valid.

## Selesaikan seluruh tugas

Pada tugas panjang dengan banyak langkah, Claude Fable 5.2 terkadang mengakhiri giliran sebelum pekerjaan selesai. Model mungkin mengakhiri giliran dengan mencantumkan hal yang masih harus dikerjakan, menawarkan untuk melanjutkan, atau berhenti pada hambatan biasa seperti timeout. Hal ini lebih sering terjadi pada effort `low` dan `medium`.

Jika Anda melihat penghentian seperti ini pada agen Anda, tambahkan teks seperti ini ke prompt sistem Anda:

```text wrap
# Finishing work
Please avoid stopping while you still owe work the user asked for. Be persistent and do not stop unless needed.

While status notes are welcome, as is clarifying with the user on open decisions, carry on with work that does not depend on the user's answer without unnecessary stops.

If you notice yourself inviting the user to redirect you or offering to wait, instead proceed on the next part of the task. You may meet ordinary obstacles like errors, timeouts, locked files, empty results or failing tools. Diagnose them first, and when they are not real blockers, work through them with the access you have (wait and retry, fix the request, use another tool or source) rather than stopping unnecessarily.

If someone clearly decided something is a hard blocker, such as a file marked not to be touched, access that was intentionally withheld, or a safety guardrail, leave it alone, say plainly what you found, and look for another safe way to finish the task. Stopping before the task is complete is very rarely merited, as in when the task can't move forward without user input, or where the blocker is deliberate and should not be worked past. This does not override the need for confirmation on risky or destructive actions.
```

Prompt ini memberi tahu Claude bahwa hambatan biasa, seperti error, timeout, dan alat yang gagal, harus didiagnosis dan diatasi. Penghalang yang disengaja, seperti file yang ditandai agar tidak disentuh, harus dibiarkan dan dilaporkan. Perlakukan ini sebagai titik awal dan sesuaikan prompt lebih lanjut untuk kasus penggunaan Anda.

Dalam pengujian, Anthropic memutar ulang sesi yang direkam dari produk coding agentik pada `medium`. Dengan salah satu versi teks ini, jumlah sesi yang berakhir dengan pekerjaan belum selesai yang sebenarnya masih bisa dilanjutkan berkurang sekitar separuhnya. Teks ini menghilangkan sebagian besar akhir giliran yang meminta izin atau menawarkan untuk melanjutkan, tetapi tidak menghilangkan akhir giliran yang mencantumkan hal yang tersisa lalu berhenti. Token output naik sekitar 30 persen.

Karena model lebih jarang bertanya dengan teks ini, pertahankan langkah konfirmasi Anda sendiri untuk tindakan yang berisiko atau tidak dapat dibatalkan.

### Persetujuan

Saat Anda meminta model untuk terus melanjutkan, nyatakan dengan tepat apa yang Anda inginkan alih-alih hanya mengirim “lanjutkan”. Misalnya, balas “Ya, jalankan migrasi pada database staging” di mana Anda mungkin sebelumnya mengirim “go” atau jempol.

Jika Anda juga menulis aturan persetujuan ke dalam prompt sistem Anda, nyatakan secara spesifik tindakan yang ingin Anda periksa ulang. Dalam pengujian Anthropic pada tugas simulasi tanpa ada orang yang menyetujui, aturan yang mencantumkan “mengirim pesan kepada orang di luar percakapan ini” di antara langkah-langkah yang memerlukan persetujuan membuat model menahan sekitar separuh permintaan rutinnya kepada rekan kerja dan tim lain.

## Nyatakan siapa pemilik kode

Claude Fable 5.2 memperhatikan dengan cermat siapa pemilik kode yang dikerjakannya. Dalam pengujian Anthropic pada tugas coding kecil, model cenderung menambahkan ke struktur yang sudah ada ketika prompt tidak menyebutkan apa pun tentang kepemilikan atau menyajikan basis kode sebagai milik orang lain, bahkan ketika hal itu menduplikasi kode yang sudah ada. Ketika prompt menyatakan bahwa basis kode adalah milik model itu sendiri, model sering menggabungkan kode yang terduplikasi dan terkadang membuat perbaikan terkait tanpa diminta.

Jika Anda ingin model memperbaiki struktur saat bekerja, nyatakan bahwa kode tersebut adalah miliknya sendiri:

```text wrap
You are the owner and long-term maintainer of this codebase, and its design is up to you.
```

Kalimat kepemilikan membuat model jauh lebih mungkin menggabungkan kode yang terduplikasi menjadi satu fungsi bersama. Dalam pengujian Anthropic pada tugas coding kecil, model menggabungkan kode yang terduplikasi pada kurang dari 10 persen eksekusi tanpa kalimat tersebut dan pada sekitar 75 persen eksekusi dengan kalimat tersebut.

Dengan prompt ini, token output naik sekitar 70 hingga 80 persen dan model membuat perubahan yang tidak diminta siapa pun, banyak di antaranya berupa pengujian dan dokumentasi baru. Pada beberapa eksekusi, model juga mengubah perilaku fitur yang sudah ada. Ringkasan PR penutup dari Claude Fable 5.2 sering menghilangkan perubahan kecil, jadi tinjau diff yang dilaporkan dan ringkasannya.

Jangan sertakan kalimat kepemilikan ketika pengguna adalah pemilik kode dan ingin kode tersebut diubah sesedikit mungkin. Aturan yang membatasi cakupan tidak membatalkannya. Dalam pengujian Anthropic, model tetap menggabungkan kode yang terduplikasi pada lebih dari separuh eksekusi ketika “No drive-by refactors, renames or cleanups” muncul di bagian awal prompt yang sama.

## Jaga agar pengguna tetap mendapat informasi selama giliran yang panjang

Terkadang Claude Fable 5.2 menulis sedikit teks yang ditujukan kepada pengguna selama rangkaian panggilan alat yang panjang. Selain itu, model mungkin membuat panggilan alat pertamanya tanpa mengatakan apa yang akan dilakukannya.

Pertama, periksa bahwa klien Anda menerima pembaruan dari model. Pada Claude Fable 5.2, pembaruan yang ditulis model di antara panggilan alat dikembalikan sebagai [blok `thinking` pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates). Pembaruan ini menyatakan apa yang ditemukan model dan apa yang akan dilakukannya selanjutnya. Teksnya kosong pada `thinking.display` default yaitu `"omitted"`. Jadi klien yang hanya merender blok `text` dapat terlihat senyap selama giliran agentik yang panjang. Tetapkan `display: "updates"` (beta, header `thinking-display-updates-2026-08-18`) untuk menerima ringkasan singkat dari setiap pembaruan, atau `"summarized"` untuk menerima pembaruan beserta ringkasan penalaran. Kemudian render blok `thinking` yang tidak kosong di antara panggilan alat.

Pembaruan yang sering paling penting dalam pengaturan interaktif. Jika itu kasus penggunaan Anda, coba langkah-langkah berikut:

### Ubah harness Anda

Cara yang efektif untuk mendorong komunikasi adalah menghitung langkah pemanggilan alat berturut-turut yang tidak memberikan apa pun untuk dibaca pengguna: tidak ada blok `text` dan tidak ada blok `thinking` dengan teks. Hitung dengan `display` disetel ke `"updates"` atau `"summarized"`, karena pada `"omitted"` setiap blok `thinking` kosong. Opsi ini berfungsi jika platform Anda mendukung [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages). Jika beberapa langkah seperti itu terjadi berturut-turut, Anda dapat menambahkan pengingat ini setelah hasil alat terbaru sebagai [pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) (`clear_at: "next_user_message"`, beta, header `mid-conversation-system-clear-at-2026-08-21`):

```text wrap
The user hasn't heard from you in a while: say in a few words what you're doing, then continue.
```

Dalam pengujian Anthropic pada tugas coding multi-giliran, pengingat ini kira-kira memangkas separuh rentang senyap terpanjang, tanpa peningkatan token atau waktu yang terlihat.

Biarkan setiap pengingat tetap ada di `messages` pada permintaan berikutnya. Menghapus atau mengubah kata-kata salah satunya berarti mengedit giliran sebelumnya, yang membuat blok pemikiran setelahnya tidak valid. Lihat [Kirim pengingat untuk satu giliran](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions#per-turn-reminders).

### Sampaikan niat

Untuk menerima kalimat pembuka sebelum panggilan alat pertama, pembaruan singkat, dan rekap penutup, Anda juga dapat menambahkan teks ini ke prompt sistem Anda:

```text wrap
Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own (what you found, what you did, and what's next), so a reader who only sees the last message has the full picture.
```

Dengan teks ini, model menulis pesan sebelum panggilan alat pertamanya di setiap eksekusi tugas coding. Perhatikan bahwa token output per tugas naik sekitar 20 persen sebagai akibatnya.

Gunakan teks ini ketika ada manusia yang terlibat langsung. Untuk meningkatkan pembaruan interaktif, gunakan teks ini bersama dengan pengingat sebelumnya.

### Perbarui instruksi prompt sistem

Jika Anda tidak dapat menambahkan pengingat di harness Anda, atau platform Anda tidak memiliki pesan sistem di tengah percakapan, tambahkan kalimat ini ke prompt sistem Anda sebagai gantinya:

```text wrap
Every few tool calls, give the user a one-line update on where things stand.
```

Dalam pengujian Anthropic, kalimat ini menghilangkan sebagian besar rentang senyap yang panjang pada tugas otomatisasi alur kerja. Tetap perkirakan adanya rangkaian beberapa panggilan alat di antara pembaruan bahkan ketika Anda menggunakan pengingat bersama dengan teks pembuka dan rekap. Claude Fable 5.2 bekerja dengan baik pada tugas asinkron jangka panjang, sehingga Anthropic merekomendasikan model ini untuk pekerjaan yang tidak memerlukan pembaruan yang sering.

## Tetapkan ekspektasi untuk subagen

Seberapa banyak Claude Fable 5.2 mendelegasikan bergantung pada harness dan tugas Anda. Dalam pengujian Anthropic pada tugas singkat dengan alat subagen minimal, model jarang memulai subagen. Dalam produk coding agentik yang prompt-nya mengundang delegasi, model mudah mendelegasikan.

Pada level effort yang lebih tinggi seperti `xhigh` dan `max`, Anthropic melihat Claude Fable 5.2 menggunakan subagen dalam produk coding agentik untuk meninjau pekerjaannya sendiri, hal yang tidak dilakukan Claude Fable 5.1 pada tugas yang sama.

Penguji awal mendapatkan hasil yang baik dengan Claude Fable 5.2 sebagai perencana dan orkestrator untuk model lain. Delegasi dapat mempercepat pekerjaan yang berjalan baik secara paralel. Namun, subagen dapat menyumbang sebagian besar biaya sesi, jadi periksa model mana yang digunakan subagen Anda secara default.

Ubah deskripsi alat subagen Anda hanya jika Claude Fable 5.2 memulai lebih banyak subagen daripada yang dibutuhkan tugas Anda. Deskripsi baru paling berguna dalam harness yang sudah mengundang delegasi dan di mana subagen menyumbang sebagian besar penggunaan token Anda. Jika alat subagen Anda memiliki deskripsi sederhana dan tidak ada hal lain dalam prompt Anda yang meminta delegasi, kemungkinan Anda tidak memerlukannya. Jika prompt sistem, skill, atau file agen Anda memberi tahu model untuk mendelegasikan, tinjau baris-baris tersebut terlebih dahulu.

Dalam deskripsi alat yang baru, nyatakan apa yang ditambahkan subagen ke biaya sesi, katakan kapan delegasi layak dilakukan dan kapan tidak, serta beri tahu model cara memberi arahan kepada subagen yang dimulainya.

Jika model terlalu sering mendelegasikan, sebutkan lebih banyak tentang biaya subagen di harness Anda, dan uji perubahan tersebut. Dalam pengujian Anthropic pada effort `high`, deskripsi yang lebih panjang yang berfokus pada hal ini kira-kira memangkas separuh jumlah subagen dibandingkan dengan versi yang lebih pendek.

Sesuaikan deskripsi Anda dengan kebutuhan Anda dan atur kapan deskripsi tersebut memberi tahu model untuk mendelegasikan.

## Cegah kehati-hatian menumpuk

Instruksi yang bersifat hati-hati dapat menumpuk dari sesi sebelumnya melalui memori, catatan, dan file instruksi. Hal ini dapat menjadi kontraproduktif ketika Claude Fable 5.2 mengikuti instruksi tersebut dengan cermat dan meminta persetujuan yang tidak perlu. Dalam pengujian awal, Anthropic melihat hal ini sebagian besar ketika beberapa agen bekerja bersama.

Jika Anda melihat hal ini, hapus instruksi yang sudah usang dari konteks agen Anda:

* **Hapus catatan yang tidak lagi Anda perlukan.** Memori dapat berisi instruksi lama seperti “jangan pernah mencoba ulang” yang terus diikuti model, jadi hapus instruksi tersebut setelah tidak lagi relevan.
* **Sebutkan langkah-langkah yang tidak memerlukan persetujuan.** Memberi tahu model untuk bertindak lebih bebas terlalu samar, jadi cantumkan langkah-langkah rutin yang dapat diambilnya sendiri.
* **Periksa langkah validasi Anda.** Syarat seperti “berhenti dan tinjau pada error pertama” dapat menghambat pekerjaan otonom, jadi hapus atau persempit syarat penghentian yang tidak Anda perlukan.
* **Nyatakan pengecualian secara eksplisit.** Model memperlakukan instruksi yang mengandung “jangan pernah” sebagai hal mutlak. Misalnya, tulis “minta persetujuan sebelum menghapus file” alih-alih “jangan pernah menghapus file” jika Anda ingin model tetap memegang tanggung jawab atas suatu tindakan. Lihat [Persetujuan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#approvals).

Pertahankan langkah konfirmasi Anda sendiri untuk tindakan yang berisiko atau tidak dapat dibatalkan.

## Tinjau prompt dan harness yang dirancang untuk model sebelumnya

Saat Anda bermigrasi ke Claude Fable 5.2, tinjau prompt dan harness Anda. Dalam pengujian Anthropic, beberapa instruksi dan intervensi yang dirancang untuk model sebelumnya menaikkan biaya, menimbulkan efek samping, atau tidak lagi berpengaruh. Berikut praktik-praktik yang perlu dipertimbangkan kembali:

* **Instruksi tetap untuk mendelegasikan:** Baris yang memberi tahu model untuk mendelegasikan dapat berada di prompt sistem, skill, dan file agen. Baca file-file tersebut sebelum Anda bermigrasi dan hapus baris yang tidak lagi Anda perlukan jika model terlalu sering mendelegasikan dalam pengujian. Lihat [Tetapkan ekspektasi untuk subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#set-expectations-for-subagents).
* **Anggaran token yang ditampilkan kepada model:** Beberapa harness menampilkan kepada model anggaran token untuk tugas dan berapa banyak yang tersisa. Besarnya anggaran tersebut mengubah seberapa banyak yang dihabiskan Claude Fable 5.2. Dalam pengujian Anthropic pada tugas coding pada effort `high` dan `xhigh`, menghapus anggaran yang besar menurunkan biaya, dengan kinerja yang setara. Uji tugas Anda tanpa anggaran tersebut. Temuan ini berkaitan dengan teks dalam prompt, bukan [anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) milik API, sebuah fitur beta yang tidak dicakup oleh pengujian.
* **Kode harness yang mengedit giliran sebelumnya:** Claude Fable 5.2 menggunakan [pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking). Jika harness Anda mengubah prompt sistem, alat, atau pesan sebelumnya di antara permintaan, blok pemikiran yang mengikuti titik yang diubah dalam riwayat menjadi tidak valid. Secara default, Messages API kemudian menolak permintaan, dan Message Batches API tidak menyertakan blok-blok tersebut. Untuk mempersingkat riwayat tanpa error ini, gunakan [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing), atau [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) yang tidak mempertahankan giliran sebelumnya setelah ringkasan. Agar Messages API juga tidak menyertakan blok-blok tersebut, tetapkan `thinking.block_binding.prefix_mismatch_behavior` ke `"drop_block"` (beta, header `thinking-binding-controls-2026-08-01`). Dalam pengujian Anthropic, ketika pemikiran sebelumnya tidak disertakan pada setiap giliran, model berpikir ulang dan menggunakan lebih banyak token output. Itu adalah kasus terburuk, dan peningkatannya bergantung pada seberapa sering harness Anda mengedit giliran sebelumnya. Selain compaction dan context editing, pertahankan riwayat agar bersifat append-only (hanya ditambahkan di akhir). Hal itu menjaga tingkat cache hit tetap tinggi, dan semua pemikiran tetap disertakan. Ukur token output pada tugas Anda sendiri sebelum Anda mengandalkan `"drop_block"`. Lihat [Atur `prefix_mismatch_behavior`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#mismatch-behavior) dan [Ubah alat atau instruksi tanpa gagal dalam pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/change-tools-or-instructions).
* **Baris “anggap jawaban itu selesai”:** [Prompting Claude Opus 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#thinking-instructions-in-chat-system-prompts) menawarkan dua kalimat untuk prompt sistem chat. Kalimat tersebut memberi tahu model untuk menganggap jawaban sebelumnya sudah selesai dan memfokuskan pemikirannya pada pesan baru. Dalam pengujian Anthropic pada effort `high`, instruksi-instruksi ini mengurangi pemikiran Claude Fable 5.2 pada pertanyaan lanjutan. Model juga menjadi jauh lebih kecil kemungkinannya untuk menunjukkan kesalahan dalam jawaban sebelumnya. Jangan sertakan baris-baris ini jika Anda ingin model terus memeriksa ulang jawaban sebelumnya. Di tempat lain, uji apakah model masih menunjukkan kesalahannya sendiri sebelum Anda mengadopsi baris-baris tersebut.
* **Instruksi untuk berpikir lebih sedikit:** Claude Fable 5.1 biasanya mengikuti baris seperti “jawab langsung tanpa berpikir panjang.” Pada Claude Fable 5.2, tambahan ini tidak menghentikan model dari berpikir pada `medium` ke atas. Hapus baris semacam itu dan turunkan level effort, seperti dijelaskan di [Kalibrasi effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#calibrate-effort).
* **Aturan gaya penulisan:** Claude Fable 5.2 mengikuti aturan tersebut dengan cermat, sehingga batas ketat seperti “satu instruksi per kalimat, dalam 20 kata atau kurang” dapat membuat prosanya terputus-putus. Hapus aturan yang tidak lagi Anda perlukan sebelum Anda menambahkan teks di [Buat laporan mudah diikuti](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#make-reports-easy-to-follow).
* **Aturan, catatan, dan memori yang telah menumpuk:** File memori, catatan, dan file instruksi mengumpulkan peringatan kehati-hatian seiring waktu, dan model mungkin telah menulis sebagian di antaranya sendiri. Sebelum Anda bermigrasi, hapus peringatan yang alasannya tidak lagi berlaku, dan tulis ulang aturan absolut beserta cakupan dan alasannya. Jika sebuah sistem sudah macet, pertimbangkan untuk memulai ulang dengan memori dan catatannya dipangkas. Lihat [Cegah kehati-hatian menumpuk](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#keep-caution-from-piling-up).

## Buat laporan mudah diikuti

Penguji awal menilai tulisan Claude Fable 5.2 lebih baik daripada tulisan Claude Fable 5.1 dan setara dalam kejelasan dengan tulisan Claude Opus 5.5. Namun, setelah pekerjaan agentik yang panjang, orang yang membaca laporan akhir Claude Fable 5.2 biasanya belum melihat panggilan alat atau file di baliknya, sehingga laporan harus dapat dipahami dengan sendirinya.

Jika Anda meminta Claude Fable 5.2 untuk menulis laporan akhir atau serah terima, tambahkan teks ini ke prompt sistem Anda, dan sesuaikan dengan pembaca dan produk Anda:

```text wrap
# Communicating clearly
Write for an intelligent but low-context reader. The person reading has not seen your tool calls, your reasoning or the files you opened, and may be switching in from other work. Messages should generally be self-contained: the reader should understand what you mean without having to dig for other context. Put the key points in the first few sentences. Practice progressive disclosure in your sentence order, and do not use undefined references and ideas in line 1 that won't make sense until the reader reaches line 12.

Use plain words, and write in clear, understandable full sentences. Do not use a term or abbreviation that you made up during the work. Say what the thing is in a way any reader would understand. Write mostly in the style of ASD-STE100 Simplified Technical English: short sentences, one idea per sentence, active voice, and consistently using the same word for the same thing. Use a paragraph of flowing prose where ideas connect, and keep bullets for lists of separate items. Leave out unnecessary details unless the reader asks and practice concision, but do ensure that your messages have the key context. Aim to make your user-facing text as human-readable and clear as possible.
```

Dalam pengujian Anthropic pada tugas agentik, teks ini membuat laporan akhir tidak terlalu padat dan mengurangi jumlah titik koma. Teks ini juga memperpendek kalimat pada tugas otomatisasi alur kerja. Bergantung pada kasus penggunaan Anda, Anda mungkin ingin menambahkan instruksi tentang panjang atau meminta model untuk menyertakan detail tertentu.

## Penolakan safeguard

Claude Fable 5.2 menjalankan classifier keamanan yang dapat menolak permintaan. Permintaan yang ditolak mengembalikan `stop_reason: "refusal"`, dan `stop_details.category` menyebutkan [kategori penolakan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response):

* `cyber`: permintaan dapat memungkinkan bahaya siber, seperti pengembangan malware atau exploit.
* `bio`: permintaan dapat memungkinkan bahaya biologis, seperti metode laboratorium yang berbahaya.
* `frontier_llm`: permintaan dapat membantu pengembangan model AI pesaing.
* `reasoning_extraction`: permintaan meminta model mereproduksi penalaran internalnya dalam teks respons.
* `general_harms`: permintaan termasuk dalam area kebijakan penggunaan lainnya.
* `null`: penolakan tidak terpetakan ke kategori bernama mana pun.

Pekerjaan keamanan siber dan ilmu hayati yang tidak berbahaya juga dapat memicu classifier `cyber` dan `bio`. Jika hal tersebut memblokir pekerjaan sah organisasi Anda, lihat [Cyber Verification Program](https://support.claude.com/en/articles/14604842) dan [Life Sciences Verification Program](https://www.anthropic.com/news/life-sciences-verification-program) dari Anthropic. [Claude Mythos 5.2](https://platform.claude.com/docs/id/models/mythos-5-2/overview) menawarkan kemampuan yang sama dengan Claude Fable 5.2 hanya kepada organisasi yang terverifikasi melalui program-program ini.

Jika prompt, skill, atau deskripsi alat Anda meminta model untuk menuliskan penalarannya dalam respons, hapus instruksi tersebut. Untuk melihat bagaimana model bernalar, tetapkan `display: "summarized"` dan baca blok pemikiran. Lihat [Simpan penalaran di blok thinking](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks).

Untuk mencoba ulang permintaan yang ditolak pada model lain, lihat [Penolakan, fallback, dan penagihan](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#refusals-fallback-and-billing).

## Dari mana memulai

1. Tetapkan `effort` ke `high` secara eksplisit, lalu jalankan juga eval Anda pada `medium` dan `xhigh`.
2. Baca prompt sistem, skill, file agen, file memori, catatan, dan teks harness yang Anda bawa, lalu hapus atau uji hal-hal yang dijelaskan di [Tinjau prompt dan harness yang dirancang untuk model sebelumnya](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#review-instructions-written-for-earlier-models).
3. Jalankan tugas agentik Anda yang paling panjang, dan catat di mana model berhenti lebih awal, meminta persetujuan yang tidak diperlukannya, menjadi senyap, mendelegasikan lebih banyak daripada yang dibutuhkan tugas, atau menambahkan ke kode yang sudah ada padahal Anda ingin kode tersebut direstrukturisasi.
4. Tambahkan teks atau ikuti saran untuk setiap perilaku yang Anda amati, satu per satu, dan ukur dampaknya serta biaya tokennya pada tugas Anda sendiri.
