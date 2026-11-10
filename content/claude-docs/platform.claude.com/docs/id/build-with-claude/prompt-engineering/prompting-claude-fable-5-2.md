---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
fetched_at: 2026-11-10T02:13:26.049428Z
sha256: f3ed886e1e5fc12c532658903d6be5d45af108a4335a586c1a5cd7ffbbc71b2a
---

---
title: Prompting Claude Fable 5.2
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
description: "Pola prompting khusus untuk Claude Fable 5.2 dan Claude Mythos 5.2: effort, berhenti lebih awal, persetujuan, kepemilikan kode, pembaruan progres, subagen, kehati-hatian yang menumpuk, instruksi yang ditulis untuk model sebelumnya, laporan akhir, dan penolakan."
---

Panduan ini membahas pola prompting yang khusus untuk Claude Fable 5.2. Untuk kemampuan model dan perubahan API, lihat [Yang baru di Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2). Untuk teknik yang berlaku di semua model Claude saat ini, lihat [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Claude Fable 5.2 berperilaku berbeda dari model sebelumnya dalam beberapa hal. Mulailah dari bagian yang sesuai dengan apa yang Anda amati:

* Tidak yakin level effort mana yang harus dijalankan, atau permintaan sederhana memakan waktu terlalu lama: [Kalibrasi effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#calibrate-effort)
* Sebuah giliran berakhir sebelum pekerjaan selesai: [Selesaikan seluruh tugas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#finish-the-whole-task)
* Anda menyetujui langkah-langkah saat agen bekerja, atau prompt sistem Anda memiliki aturan persetujuan: [Persetujuan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#approvals)
* Agen coding mengulang kode yang sudah ada alih-alih menggabungkannya, atau melaporkan masalah di sekitarnya tanpa memperbaikinya: [Nyatakan siapa pemilik kode](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#say-who-owns-the-code)
* Giliran agentik yang panjang tampak senyap: [Jaga agar pengguna tetap mendapat informasi selama giliran yang panjang](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#keep-users-informed-during-long-turns)
* Sesi agen memulai lebih banyak subagen daripada yang dibutuhkan tugas: [Tetapkan ekspektasi untuk subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#set-expectations-for-subagents)
* Agen meminta persetujuan yang tidak mereka perlukan, atau menahan pekerjaan rutin: [Cegah kehati-hatian menumpuk](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#keep-caution-from-piling-up)
* Anda membawa prompt sistem, skill, atau harness yang ditulis untuk Claude Fable 5.1 atau Claude Opus 5.5: [Tinjau instruksi yang ditulis untuk model sebelumnya](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#review-instructions-written-for-earlier-models)
* Pengguna Anda membaca laporan akhir atau serah terima setelah tugas panjang: [Buat laporan mudah diikuti](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#make-reports-easy-to-follow)
* Permintaan mengembalikan `stop_reason: "refusal"`: [Penolakan safeguard](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#safeguard-refusals)

<Note>
  Untuk perubahan API saat Anda bermigrasi dari model sebelumnya, lihat [panduan migrasi Claude Fable 5.2 dan Claude Mythos 5.2](https://platform.claude.com/docs/id/models/fable-5-2/migration-guide). Untuk urutan penerapan panduan ini saat Anda bermigrasi, lihat [Dari mana memulai](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#where-to-start).

  Beberapa bagian di halaman ini menyarankan teks untuk ditambahkan ke prompt sistem Anda, baris untuk dihapus darinya atau dari catatan dan aturan yang dibawa agen Anda, atau perubahan pada deskripsi alat. Lakukan perubahan ini hanya pada percakapan baru. Pada Claude Fable 5.2, API menerapkan [pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#prefix-check) untuk setiap akun. Permintaan yang mengirim kembali blok thinking setelah `system`, `tools`, atau pesan sebelumnya berubah dapat mengembalikan error 400, sehingga percakapan tersimpan yang dilanjutkan dengan teks baru dapat gagal. Untuk mengubah instruksi di tengah percakapan, [letakkan instruksi tersebut di giliran terbaru](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#changing-context). Jika [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) tersedia, Anda dapat [menambahkan pesan sistem ke percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#new-instructions) sebagai gantinya.
</Note>

## Kalibrasi effort

Mulailah dari `high`, nilai default di Claude API. Jika kasus penggunaan Anda membutuhkannya, naikkan atau turunkan effort, dan uji setiap perubahan terhadap eval Anda sendiri. Level [effort](https://platform.claude.com/docs/id/build-with-claude/effort) menentukan seberapa banyak Claude Fable 5.2 berpikir, berapa lama sebuah giliran berlangsung, dan berapa banyak token yang digunakannya. Setel effort bersamaan dengan prompt Anda, karena level tersebut juga mengubah cara model berpikir dan berapa banyak panggilan alat yang dibuatnya.

Secara umum, level effort berjalan dalam urutan yang sama di seluruh model Claude, tetapi jumlah pemikiran di balik setiap level dapat berbeda dari satu model ke model lain. Jadi jalankan ulang pengujian effort Anda alih-alih membawa pengaturan yang Anda setel pada Claude Fable 5.1 atau Claude Opus 5.5.

Pilih level berdasarkan jenis pekerjaan:

* `low` cocok untuk interaksi bolak-balik yang cepat, tugas yang terdefinisi dengan baik, dan beban kerja bervolume tinggi, seperti subagen yang cepat dan cerdas. Dalam pengujian Anthropic, skor model pada `low` mendekati skor Claude Fable 5.1 pada level effort yang lebih tinggi.
* `medium` cocok untuk coding interaktif, chat, dan pekerjaan pengetahuan sehari-hari.
* `high` cocok untuk coding yang sulit, riset, pekerjaan agentik, dan eksekusi panjang tanpa pengawasan. Giliran memakan waktu jauh lebih lama untuk selesai dibandingkan pada `medium`.
* `xhigh` ditujukan untuk pekerjaan coding dan agentik jangka panjang Anda yang paling sulit, di mana Anda telah mengukur adanya peningkatan. Pada evaluasi coding internal Anthropic, level ini sedikit menaikkan skor dan menggunakan jauh lebih banyak token.
* `max` ditujukan untuk mengukur batas kemampuan model, atau untuk tugas langka di mana waktu dan token tidak menjadi masalah. Level ini paling cocok untuk masalah terbuka, seperti penemuan ilmiah dan matematika. Giliran berjalan lambat dan menggunakan jauh lebih banyak token dibandingkan pada `xhigh`.

Sebagian besar peningkatan kemampuan sudah ada pada `high`. Langkah dari `medium` ke `high` menaikkan skor pada sebagian besar evaluasi coding dan pekerjaan pengetahuan yang dilacak Anthropic. Langkah tersebut juga menggunakan lebih banyak token dan waktu, jadi turunkan ke `medium` di mana pun eval Anda menunjukkan bahwa kualitasnya tetap terjaga. Di atas `high`, peningkatannya tidak merata dan bergantung pada tugas.

Saat memilih level, perhatikan tiga perilaku berikut:

* Model lebih mungkin berhenti lebih awal pada level effort yang lebih rendah. Untuk pekerjaan agentik pada `low` atau `medium`, tambahkan teks di [Selesaikan seluruh tugas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#finish-the-whole-task).
* Pada `high` ke atas, model berpikir sebelum hampir setiap balasan, termasuk balasan untuk sapaan. Jika permintaan sederhana memakan waktu terlalu lama atau biayanya terlalu besar, gunakan level effort yang lebih rendah untuk giliran tersebut. Dalam pengujian Anthropic, instruksi untuk menjawab langsung tanpa berpikir panjang tidak menghentikan model dari berpikir pada `medium` ke atas.
* Effort hampir tidak mengubah panjang balasan model. Untuk mengubah panjang dan nada balasan, gunakan prompt Anda.

Anda juga dapat mencampur level dalam satu alur kerja. Misalnya, Anda dapat merencanakan dan beriterasi dengan model pada `medium`, lalu menaikkan effort untuk bagian panjang tanpa pengawasan. Untuk mengubah level di dalam percakapan dan mempertahankan cache prompt, gunakan [perubahan effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) (beta, header `mid-conversation-output-config-2026-07-01`); bagian tersebut mencantumkan platform tempat fitur ini tersedia. Sebuah perubahan berlaku hingga perubahan lain menggantikannya. Jika effort per pesan tidak tersedia, tetapkan nilai `effort` tingkat atas yang baru pada permintaan berikutnya, yang akan memulai cache dari awal.

## Selesaikan seluruh tugas

Pada tugas panjang dengan banyak langkah, Claude Fable 5.2 terkadang mengakhiri giliran sebelum pekerjaan selesai. Giliran ditutup dengan daftar hal yang tersisa, tawaran untuk melanjutkan, atau berhenti pada hambatan biasa seperti timeout. Hal ini lebih sering terjadi pada effort `low` dan `medium`.

Jika Anda melihat penghentian seperti ini pada agen Anda, tambahkan teks seperti ini ke prompt sistem Anda:

```text wrap
# Finishing work
Please avoid stopping while you still owe work the user asked for. Be persistent and do not stop unless needed.

While status notes are welcome, as is clarifying with the user on open decisions, carry on with work that does not depend on the user's answer without unnecessary stops.

If you notice yourself inviting the user to redirect you or offering to wait, instead proceed on the next part of the task. You may meet ordinary obstacles like errors, timeouts, locked files, empty results or failing tools. Diagnose them first, and when they are not real blockers, work through them with the access you have (wait and retry, fix the request, use another tool or source) rather than stopping unnecessarily.

If someone clearly decided something is a hard blocker, such as a file marked not to be touched, access that was intentionally withheld, or a safety guardrail, leave it alone, say plainly what you found, and look for another safe way to finish the task. Stopping before the task is complete is very rarely merited, as in when the task can't move forward without user input, or where the blocker is deliberate and should not be worked past. This does not override the need for confirmation on risky or destructive actions.
```

Teks ini membedakan dua jenis hambatan. Teks ini memberi tahu model untuk mendiagnosis dan mengatasi hambatan biasa, seperti error, timeout, dan alat yang gagal. Teks ini juga memberi tahu model untuk membiarkan penghalang yang disengaja, seperti file yang ditandai agar tidak disentuh, dan melaporkannya. Perlakukan teks ini sebagai titik awal, dan pertahankan perbedaan tersebut saat Anda menyesuaikannya dengan aplikasi Anda.

Anthropic memutar ulang sesi yang direkam dari produk coding agentik pada effort `medium`. Dengan salah satu versi teks ini, jumlah sesi yang berakhir dengan pekerjaan yang masih bisa dikerjakan berkurang sekitar separuhnya. Teks ini menghilangkan sebagian besar akhir giliran yang meminta izin atau menawarkan untuk melanjutkan, tetapi tidak menghilangkan akhir giliran yang mencantumkan hal yang tersisa lalu berhenti. Token output naik sekitar 30 persen.

Karena model lebih jarang bertanya dengan teks ini, pertahankan langkah konfirmasi Anda sendiri untuk tindakan yang berisiko atau tidak dapat dibatalkan.

### Persetujuan

Saat Anda memberi tahu model untuk terus melanjutkan, nyatakan dengan jelas apa yang Anda inginkan darinya alih-alih hanya mengirim “lanjutkan”. Misalnya, balas “Ya, jalankan migrasi pada database staging” di mana Anda mungkin sebelumnya mengirim “go” atau jempol.

Jika prompt sistem Anda memiliki aturan persetujuan, sebutkan tindakan persis yang dicakupnya, karena model menerapkannya sesuai yang tertulis. Dalam pengujian Anthropic pada tugas simulasi tanpa ada orang yang menyetujui, satu aturan mencantumkan “mengirim pesan kepada orang di luar percakapan ini” di antara langkah-langkah yang memerlukan persetujuan. Dengan aturan tersebut, model menahan kira-kira separuh permintaan rutinnya kepada rekan kerja dan tim lain.

## Nyatakan siapa pemilik kode

Claude Fable 5.2 merespons dengan cermat apa yang dinyatakan prompt tentang siapa pemilik kode yang dikerjakannya. Dalam pengujian Anthropic pada tugas coding kecil, ketika prompt tidak menyebutkan apa pun tentang kepemilikan atau menyajikan basis kode sebagai milik orang lain, model cenderung menambahkan ke struktur yang sudah ada, bahkan ketika hal itu mengulang kode yang sudah ada. Model juga cenderung melaporkan masalah di sekitarnya alih-alih memperbaikinya. Ketika prompt menyatakan bahwa basis kode adalah milik model itu sendiri, model sering menggabungkan kode yang berulang dan membuat perbaikan terkait tanpa diminta.

Jika Anda ingin model memperbaiki struktur saat bekerja, nyatakan bahwa kode tersebut adalah miliknya sendiri:

```text wrap
This codebase is yours: what it's for and how it's built are your call, and you'll keep building on it.
```

Dalam pengujian Anthropic pada tugas coding kecil, model menggabungkan kode yang berulang pada sekitar separuh percobaan dengan kalimat ini, dan pada kurang dari sepersepuluh percobaan tanpanya. Tingkatnya bervariasi menurut tugas. Hasil ini tetap berlaku ketika kalimat tersebut berada di dalam prompt sistem yang panjang. Fitur yang diminta berfungsi di hampir setiap percobaan dalam kedua kondisi.

Dalam pengujian yang sama, model juga menggunakan sekitar 1,5 kali token output dengan kalimat tersebut dan membuat beberapa perubahan yang tidak diminta siapa pun, banyak di antaranya berupa pengujian dan dokumentasi baru. Selain perbaikan bug, model mengubah perilaku fitur yang sudah ada pada satu dari enam hingga sepuluh percobaan, dan lebih sering pada effort yang lebih tinggi. Ringkasan penutupnya menyebutkan perubahan yang lebih besar tetapi sering menghilangkan perubahan kecil, jadi tinjau diff-nya dan bukan hanya ringkasannya.

Jangan sertakan kalimat kepemilikan ketika pengguna adalah pemilik kode dan ingin kode tersebut diubah sesedikit mungkin. Aturan di bagian lain prompt yang membatasi cakupan tidak membatalkan kalimat kepemilikan. Dalam pengujian Anthropic, dengan “No drive-by refactors, renames or cleanups” di bagian awal prompt yang sama, model tetap menggabungkan kode yang berulang pada sekitar sepertiga percobaan.

## Jaga agar pengguna tetap mendapat informasi selama giliran yang panjang

Claude Fable 5.2 terkadang menulis sedikit teks yang ditujukan kepada pengguna selama rangkaian panggilan alat yang panjang. Model juga mungkin membuat panggilan alat pertamanya tanpa mengatakan apa yang akan dilakukannya.

Pertama, periksa bahwa klien Anda menerima pembaruan dari model. Pada Claude Fable 5.2, pembaruan yang ditulis model di antara panggilan alat dikembalikan sebagai [blok `thinking` pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates). Pembaruan ini menyatakan apa yang ditemukan model dan apa yang akan dilakukannya selanjutnya. Teksnya kosong pada `thinking.display` default yaitu `"omitted"`. Jadi klien yang hanya merender blok `text` dapat terlihat senyap selama giliran agentik yang panjang. Tetapkan `display: "updates"` (beta, header `thinking-display-updates-2026-08-18`) untuk menerima ringkasan singkat dari setiap pembaruan, atau `"summarized"` untuk menerima pembaruan beserta ringkasan penalaran. Kemudian render blok `thinking` yang tidak kosong di antara panggilan alat.

Pembaruan yang sering paling penting ketika pengguna mengamati pekerjaan secara real time, seperti pada coding interaktif. Jika pengguna Anda mengamati pekerjaan dan tetap mendapat terlalu sedikit pembaruan, gunakan satu atau beberapa opsi berikut.

Jika Anda dapat mengubah harness Anda, opsi yang efektif adalah membuatnya menghitung langkah pemanggilan alat berturut-turut yang tidak memberikan apa pun untuk dibaca pengguna: tidak ada blok `text` dan tidak ada blok `thinking` dengan teks. Hitung dengan `display` disetel ke `"updates"` atau `"summarized"`, karena pada `"omitted"` setiap blok `thinking` kosong. Opsi ini berfungsi jika platform Anda mendukung [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages). Setelah beberapa langkah seperti itu berturut-turut, buat harness menambahkan pengingat ini setelah hasil alat terbaru sebagai [pesan sistem berlingkup giliran](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#turn-scoped-system-messages) (`clear_at: "next_user_message"`, beta, header `mid-conversation-system-clear-at-2026-08-21`):

```text wrap
The user hasn't heard from you in a while: say in a few words what you're doing, then continue.
```

Dalam pengujian Anthropic pada tugas coding multi-giliran, pengingat ini kira-kira memangkas separuh rentang senyap terpanjang, tanpa peningkatan token atau waktu yang terlihat.

Biarkan setiap pengingat tetap ada di `messages` pada permintaan berikutnya. Menghapus atau mengubah kata-kata salah satunya berarti mengedit giliran sebelumnya, yang membuat blok thinking setelahnya tidak valid. Lihat [Kirim pengingat per giliran sebagai pesan sistem bercakupan giliran](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#per-turn-reminders).

Untuk juga mendapatkan kalimat pembuka sebelum panggilan alat pertama, pembaruan singkat, dan rekap penutup, tambahkan teks ini ke prompt sistem Anda:

```text wrap
Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own (what you found, what you did, and what's next), so a reader who only sees the last message has the full picture.
```

Dalam pengujian Anthropic pada tugas coding, model selalu berbicara sebelum panggilan alat pertamanya dengan teks ini. Teks ini juga menaikkan token output per tugas sekitar 20 persen. Gunakan teks ini ketika ada manusia yang terlibat langsung. Untuk mendapatkan pembaruan paling banyak, pasangkan dengan pengingat yang ditambahkan oleh harness Anda.

Jika Anda tidak dapat mengubah harness, atau platform Anda tidak memiliki pesan sistem di tengah percakapan, tambahkan kalimat ini ke prompt sistem Anda:

```text wrap
Every few tool calls, give the user a one-line update on where things stand.
```

Dalam pengujian Anthropic pada tugas otomatisasi alur kerja, kalimat ini menghilangkan sebagian besar rentang senyap yang panjang.

Bahkan dengan pengingat serta teks pembuka dan rekap sekaligus, tetap perkirakan adanya rangkaian beberapa panggilan alat di antara pembaruan. Claude Fable 5.2 bekerja dengan baik pada tugas asinkron jangka panjang, di mana pengguna kembali untuk melihat hasilnya alih-alih mengamati setiap langkah. Jeda di antara pembaruan kurang penting dalam situasi tersebut.

## Tetapkan ekspektasi untuk subagen

Seberapa banyak pekerjaan yang didelegasikan Claude Fable 5.2 kepada subagen bergantung pada harness dan tugas Anda. Dalam pengujian Anthropic pada tugas singkat dengan alat minimal untuk memulai subagen, model jarang memulai subagen. Dalam produk coding agentik yang prompt-nya mengundang delegasi, model mudah mendelegasikan.

Jika prompt sistem, skill, atau file agen Anda memberi tahu model untuk mendelegasikan, tinjau baris-baris tersebut terlebih dahulu. Ubah deskripsi alat yang memulai subagen hanya jika Claude Fable 5.2 masih memulai lebih banyak subagen daripada yang dibutuhkan tugas Anda. Jika alat tersebut memiliki deskripsi sederhana dan tidak ada hal lain dalam prompt Anda yang meminta delegasi, kemungkinan Anda tidak memerlukan deskripsi baru.

Dalam deskripsi baru, nyatakan apa yang ditambahkan subagen ke biaya sesi, katakan kapan delegasi layak dilakukan dan kapan tidak, serta beri tahu model cara memberi arahan kepada subagen yang dimulainya. Deskripsi yang diuji Anthropic melakukan ketiga hal ini dan menempatkan biaya di urutan pertama. Deskripsi semacam ini paling berguna ketika harness Anda sudah mengundang delegasi dan subagen menyumbang sebagian besar penggunaan token Anda.

Dalam pengujian Anthropic pada tugas singkat, model mendelegasikan sekitar sepertiga lebih jarang dengan deskripsi yang diuji dibandingkan dengan deskripsi yang sebagian besar mencantumkan alasan untuk mendelegasikan. Tingkat keberhasilan tugas sama.

Dalam deskripsi yang diuji, kalimat pembuka tentang biaya menahan delegasi. Sebutkan lebih sedikit tentang biaya jika model terlalu jarang mendelegasikan. Jika model masih terlalu sering mendelegasikan, sebutkan lebih banyak tentang biaya subagen di harness Anda, dan uji perubahan tersebut.

Anthropic juga mengamati Claude Fable 5.2 menggunakan subagen untuk meninjau pekerjaannya sendiri dalam produk coding agentik pada level effort yang lebih tinggi, seperti `xhigh` dan `max`. Claude Fable 5.1 tidak melakukan hal ini pada tugas yang sama. Penguji awal mendapatkan hasil yang baik dengan Claude Fable 5.2 sebagai perencana dan orkestrator untuk model lain. Delegasi dapat mempercepat pekerjaan yang berjalan baik secara paralel. Namun, subagen dapat menyumbang sebagian besar biaya sesi, jadi periksa model mana yang digunakan harness Anda untuk menjalankan subagen secara default.

## Cegah kehati-hatian menumpuk

Instruksi yang bersifat hati-hati menumpuk di mana pun konteks terbawa: memori, catatan, file instruksi, dan pesan antar agen. Claude Fable 5.2 mengikuti instruksi ini dengan cermat, sehingga model mungkin meminta persetujuan yang tidak diperlukannya atau menahan pekerjaan rutin. Beberapa penguji awal melihat perilaku ini, sebagian besar ketika beberapa agen bekerja bersama. Model sebelumnya juga mengikuti instruksi semacam itu, tetapi dalam salah satu pengaturan yang dijelaskan di sini hanya Claude Fable 5.2 yang menahan diri.

Jika Anda melihat perilaku ini, bersihkan apa yang dibawa agen Anda:

* **Hapus catatan yang tidak lagi Anda perlukan.** Dalam pengujian Anthropic pada tugas simulasi, satu dari selusin catatan dari sesi sebelumnya menyatakan untuk tidak pernah mencoba ulang. Dengan catatan-catatan tersebut dalam konteks, dan tanpa ada apa pun dalam prompt yang mengizinkan percobaan ulang, model mencoba ulang setelah sebuah alat sibuk pada sekitar empat dari sepuluh percobaan, turun dari hampir semuanya tanpa catatan tersebut.
* **Sebutkan langkah-langkah yang tidak memerlukan persetujuan.** Dalam pengujian Anthropic pada tugas simulasi, konteks berisi aturan “jangan pernah”, catatan, dan syarat dari reviewer. Satu baris di akhir aturan yang mencantumkan percobaan ulang di antara langkah-langkah yang tidak memerlukan persetujuan menaikkan percobaan ulang dari hampir tidak ada menjadi sekitar separuh percobaan. Dalam pengaturan yang sama, instruksi umum untuk bertindak lebih bebas tidak mengubah apa pun. Sebutkan percobaan ulang hanya untuk panggilan yang aman untuk diulang.
* **Periksa apa yang dilampirkan agen reviewer.** Dalam pengujian Anthropic pada tugas simulasi, satu pengaturan memiliki baris dalam prompt yang mencantumkan percobaan ulang di antara langkah-langkah yang tidak memerlukan persetujuan, dan “berhenti pada error pertama” dari reviewer dalam konteks. Claude Fable 5.2 tidak mencoba ulang pada sekitar sepertiga percobaan. Claude Fable 5.1 dan Claude Opus 5.5 mencoba ulang.
* **Tuliskan pengecualian ke dalam aturan.** Dalam pengujian Anthropic pada tugas simulasi, orang yang bertanggung jawab telah menyetujui sebuah langkah. Di bawah aturan “jangan pernah”, model mengambil langkah tersebut pada sekitar satu dari sepuluh percobaan. Baris terpisah yang menyatakan bahwa langkah yang disetujui telah mendapat izin tidak banyak mengubah tingkat tersebut. Ketika aturan itu sendiri menyatakan untuk mendapatkan izin terlebih dahulu, model mengambil langkah tersebut pada sekitar sembilan dari sepuluh percobaan. Lihat [Persetujuan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#approvals).

Pertahankan juga langkah konfirmasi Anda sendiri untuk tindakan yang berisiko atau tidak dapat dibatalkan.

## Tinjau instruksi yang ditulis untuk model sebelumnya

Saat Anda bermigrasi ke Claude Fable 5.2, tinjau prompt Anda. Dalam pengujian Anthropic, beberapa instruksi yang ditulis untuk model sebelumnya menaikkan biaya, menimbulkan efek samping, atau tidak lagi berpengaruh. Pertimbangkan kembali instruksi-instruksi berikut:

* **Instruksi tetap untuk mendelegasikan:** Baris yang mendorong pekerjaan ke subagen dapat berada di prompt sistem, skill, dan file agen. Baca file-file tersebut sebelum Anda bermigrasi. Jika, dalam pengujian Anda, model memulai lebih banyak subagen daripada yang dibutuhkan tugas Anda, hapus baris yang tidak lagi Anda perlukan. Lihat [Tetapkan ekspektasi untuk subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#set-expectations-for-subagents).
* **Anggaran token yang ditulis harness Anda ke dalam prompt:** Beberapa harness memberi tahu model dalam prompt berapa banyak token yang boleh digunakan tugas dan berapa yang tersisa. Besarnya anggaran tersebut mengubah seberapa banyak yang dihabiskan Claude Fable 5.2. Dalam pengujian Anthropic pada tugas coding pada effort `high` dan `xhigh`, menghapus anggaran yang besar menurunkan biaya, dengan kinerja yang setara. Uji tugas Anda tanpa anggaran tersebut. Temuan ini berkaitan dengan teks dalam prompt, bukan [anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) milik API, sebuah fitur beta yang tidak dicakup oleh pengujian.
* **Kode harness yang mengedit giliran sebelumnya:** Claude Fable 5.2 menggunakan [preserved thinking](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking). Jika harness Anda mengubah prompt sistem, alat, atau pesan sebelumnya di antara permintaan, blok thinking yang mengikuti titik yang diubah dalam riwayat menjadi tidak valid. Secara default, Messages API kemudian menolak permintaan, dan Message Batches API membuang blok-blok tersebut. Untuk mempersingkat riwayat tanpa error ini, gunakan [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing), atau [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) yang tidak mempertahankan giliran sebelumnya setelah ringkasan. Agar Messages API juga membuang blok-blok tersebut, tetapkan `thinking.block_binding.prefix_mismatch_behavior` ke `"drop_block"` (beta, header `thinking-binding-controls-2026-08-01`). Dalam pengujian Anthropic, ketika thinking sebelumnya dibuang pada setiap giliran, model berpikir ulang dan menggunakan lebih banyak token output. Itu adalah kasus terburuk, dan peningkatannya bergantung pada seberapa sering harness Anda mengedit giliran sebelumnya. Selain compaction dan context editing, pertahankan riwayat agar hanya ditambahkan (append-only). Hal itu menjaga tingkat cache hit tetap tinggi, dan tidak ada thinking yang dibuang. Ukur token output pada tugas Anda sendiri sebelum Anda mengandalkan `"drop_block"`. Lihat [Apa yang dilakukan API terhadap blok yang tidak valid](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#mismatch-behavior) dan [Lakukan perubahan tanpa mengedit prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#replace-prefix-edits).
* **Baris “anggap jawaban itu selesai”:** [Prompting Claude Opus 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#thinking-instructions-in-chat-system-prompts) menawarkan dua kalimat untuk prompt sistem chat. Kalimat tersebut memberi tahu model untuk menganggap jawaban sebelumnya sudah selesai dan memfokuskan pemikirannya pada pesan baru. Dalam pengujian Anthropic pada effort `high`, kalimat-kalimat ini mengurangi pemikiran Claude Fable 5.2 pada pertanyaan lanjutan, tetapi model juga menjadi jauh lebih kecil kemungkinannya untuk menunjukkan kesalahan dalam jawaban sebelumnya. Jangan sertakan baris-baris ini jika Anda ingin model terus memeriksa ulang jawaban sebelumnya. Di tempat lain, uji apakah model masih menunjukkan kesalahannya sendiri sebelum Anda mengadopsi baris-baris tersebut.
* **Instruksi untuk berpikir lebih sedikit:** Claude Fable 5.1 biasanya mengikuti baris seperti “jawab langsung tanpa berpikir panjang.” Dalam pengujian Anthropic, baris semacam itu tidak menghentikan Claude Fable 5.2 dari berpikir pada `medium` ke atas. Hapus baris-baris ini dan turunkan level effort, seperti dijelaskan di [Kalibrasi effort](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#calibrate-effort).
* **Aturan gaya penulisan:** Claude Fable 5.2 mengikuti aturan gaya dengan cermat, sehingga batas ketat seperti “satu instruksi per kalimat, dalam 20 kata atau kurang” dapat membuat prosanya terputus-putus. Hapus aturan yang tidak lagi Anda perlukan sebelum Anda menambahkan teks di [Buat laporan mudah diikuti](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#make-reports-easy-to-follow).
* **Aturan, catatan, dan memori yang telah menumpuk:** File memori, catatan, dan file instruksi mengumpulkan peringatan kehati-hatian seiring waktu, dan model mungkin telah menulis sebagian di antaranya sendiri. Sebelum Anda bermigrasi, hapus peringatan yang alasannya tidak lagi berlaku, dan tulis ulang aturan absolut agar menyatakan cakupan dan alasannya. Jika sebuah sistem sudah macet, pertimbangkan untuk memulai ulang dengan memori dan catatannya dipangkas, dan simpan salinan aslinya. Lihat [Cegah kehati-hatian menumpuk](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#keep-caution-from-piling-up).

## Buat laporan mudah diikuti

Setelah pekerjaan agentik yang panjang, orang yang membaca laporan akhir Claude Fable 5.2 biasanya belum melihat panggilan alat atau file di baliknya. Laporan harus dapat dipahami dengan sendirinya.

Jika Anda meminta Claude Fable 5.2 untuk menulis laporan akhir atau serah terima, tambahkan teks ini ke prompt sistem Anda, dan sesuaikan dengan pembaca dan produk Anda:

```text wrap
# Communicating clearly
Write for an intelligent but low-context reader. The person reading has not seen your tool calls, your reasoning or the files you opened, and may be switching in from other work. Messages should generally be self-contained: the reader should understand what you mean without having to dig for other context. Put the key points in the first few sentences. Practice progressive disclosure in your sentence order, and do not use undefined references and ideas in line 1 that won't make sense until the reader reaches line 12.

Use plain words, and write in clear, understandable full sentences. Do not use a term or abbreviation that you made up during the work. Say what the thing is in a way any reader would understand. Write mostly in the style of ASD-STE100 Simplified Technical English: short sentences, one idea per sentence, active voice, and consistently using the same word for the same thing. Use a paragraph of flowing prose where ideas connect, and keep bullets for lists of separate items. Leave out unnecessary details unless the reader asks and practice concision, but do ensure that your messages have the key context. Aim to make your user-facing text as human-readable and clear as possible.
```

Dalam pengujian Anthropic pada tugas agentik, teks ini membuat laporan akhir tidak terlalu padat, dengan lebih sedikit titik koma. Pada tugas otomatisasi alur kerja, teks ini juga membuat kalimat lebih pendek. Anda juga dapat menambahkan instruksi tentang panjang atau meminta model untuk menyertakan detail tertentu.

## Penolakan safeguard

Claude Fable 5.2 menjalankan classifier keamanan yang dapat menolak permintaan. Permintaan yang ditolak mengembalikan `stop_reason: "refusal"`, dan `stop_details.category` menyebutkan [kategori penolakan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response):

* `cyber`: permintaan dapat memungkinkan bahaya siber, seperti pengembangan malware atau exploit.
* `bio`: permintaan dapat memungkinkan bahaya biologis, seperti metode laboratorium yang berbahaya.
* `frontier_llm`: permintaan dapat membantu pengembangan model AI pesaing.
* `reasoning_extraction`: permintaan meminta model mereproduksi penalaran internalnya dalam teks respons.
* `general_harms`: permintaan termasuk dalam area kebijakan penggunaan lainnya.

Pekerjaan keamanan siber dan ilmu hayati yang tidak berbahaya juga dapat memicu classifier `cyber` dan `bio`. Jika classifier tersebut memblokir pekerjaan sah organisasi Anda, lihat [Cyber Verification Program](https://support.claude.com/en/articles/14604842) dan [Life Sciences Verification Program](https://www.anthropic.com/news/life-sciences-verification-program) dari Anthropic. [Claude Mythos 5.2](https://platform.claude.com/docs/id/models/mythos-5-2/overview) menawarkan kemampuan yang sama dengan Claude Fable 5.2 hanya kepada organisasi yang terverifikasi melalui program-program ini.

Jika prompt, skill, atau deskripsi alat Anda meminta model untuk menulis penalarannya dalam respons, hapus instruksi tersebut. Untuk melihat bagaimana model bernalar, tetapkan `display: "summarized"` dan baca blok thinking. Lihat [Simpan penalaran di blok thinking](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks).

Untuk mencoba ulang permintaan yang ditolak pada model lain, lihat [Penolakan, fallback, dan penagihan](https://platform.claude.com/docs/id/models/fable-5-2/whats-new-fable-5-2#refusals-fallback-and-billing).

## Dari mana memulai

Saat Anda bermigrasi, kerjakan langkah-langkah berikut secara berurutan:

1. Tetapkan `effort` ke `high` secara eksplisit, lalu jalankan juga eval Anda pada `medium` dan `xhigh`.
2. Baca prompt sistem, skill, file agen, file memori, catatan, dan teks harness yang Anda bawa. Hapus atau uji instruksi yang tercantum di [Tinjau instruksi yang ditulis untuk model sebelumnya](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#review-instructions-written-for-earlier-models).
3. Jalankan tugas agentik Anda yang paling panjang. Catat di mana model berhenti lebih awal, meminta persetujuan yang tidak diperlukannya, menjadi senyap, mendelegasikan lebih banyak daripada yang dibutuhkan tugas, atau menambahkan ke kode yang sudah ada padahal Anda ingin kode tersebut direstrukturisasi.
4. Terapkan panduan untuk setiap perilaku yang Anda amati, satu per satu, dan ukur dampaknya serta biaya tokennya pada tugas Anda sendiri.
