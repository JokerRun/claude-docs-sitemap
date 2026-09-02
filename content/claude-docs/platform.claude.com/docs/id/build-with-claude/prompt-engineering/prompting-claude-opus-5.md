---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 527b2cd7e5b5c1251238f4d8d38903c60078dd61fffd125e07e26166b8862a0c
---

---
title: Prompting Claude Opus 5
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5
description: Perbedaan perilaku dan pola prompting untuk Claude Opus 5, mencakup verbositas respons, narasi agentik, pembatasan cakupan tugas, delegasi subagen, koreksi diri, dan artefak output saat thinking dinonaktifkan.
---

Panduan ini membahas pola prompting yang khusus untuk Claude Opus 5. Untuk kemampuan model dan perubahan API, lihat [Yang baru di Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/whats-new-opus-5). Untuk teknik yang berlaku di semua model Claude saat ini, lihat [Praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Claude Opus 5 dibangun untuk pekerjaan agentic coding yang kompleks dan pekerjaan enterprise, dengan kekuatan khusus pada tugas agentik berjangka panjang. Model ini bekerja dengan baik secara langsung pada prompt Claude Opus 4.8 yang sudah ada. Pola-pola berikut mencakup perilaku yang paling sering memerlukan penyesuaian.

<Note>
  Untuk perubahan API saat bermigrasi dari Claude Opus 4.8 (thinking aktif secara default, dan penonaktifan thinking dibatasi pada effort `high`), lihat [panduan migrasi](https://platform.claude.com/docs/id/models/opus-5/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5).
</Note>

## Peningkatan kemampuan

Dibandingkan dengan Claude Opus 4.8, peningkatan yang paling relevan untuk prompting adalah:

* **Agentic coding:** Claude Opus 5 paling kuat pada tugas coding yang sulit: fitur multi-file, refactor yang lebih besar, dan pekerjaan fitur end-to-end. Model ini menyelesaikan tugas secara penuh alih-alih meninggalkan stub atau placeholder, dan bekerja paling baik ketika diberi spesifikasi tugas lengkap di awal lalu dibiarkan berjalan. Model ini juga bekerja dengan baik pada tugas yang lebih mudah seperti edit satu giliran, di mana perbedaannya dari model sebelumnya lebih kecil.
* **Code review dan pencarian bug:** Claude Opus 5 meninjau kode dengan presisi dan recall yang tinggi: model ini menemukan bug nyata dengan tingkat yang tinggi per pass, dan temuan tambahannya sebagian besar adalah masalah nyata, bukan false positive. Akurasi tetap terjaga pada pengaturan effort yang lebih rendah, yang mendukung pass cepat saat review dan pass yang lebih menyeluruh kemudian. Jika prompt review Anda mengatakan "hanya laporkan masalah dengan tingkat keparahan tinggi" atau "bersikaplah konservatif," model mungkin mengikuti instruksi itu secara harfiah dan melaporkan lebih sedikit; sebagai gantinya, minta model untuk melaporkan semuanya dan lakukan penyaringan dalam pass terpisah.
* **Efisiensi pada effort yang lebih rendah:** [Effort](https://platform.claude.com/docs/id/build-with-claude/effort) `low` dan `medium` menghasilkan kualitas yang kuat dengan sebagian kecil token dan latensi dari pengaturan yang lebih tinggi. Mulailah dengan default (`high`) dan sesuaikan berdasarkan eval Anda: gunakan `low` dan `medium` secara leluasa sebagai kontrol utama Anda untuk biaya token dan waktu respons di mana pun kualitas tetap terjaga, dan naikkan ke `xhigh` untuk pekerjaan coding dan agentik yang menuntut. Jika Anda membawa default effort dari model sebelumnya, jalankan ulang effort sweep pada eval Anda sendiri. Lihat [Effort](https://platform.claude.com/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-opus-5) untuk rekomendasi lengkapnya.
* **Vision:** Claude Opus 5 kuat dalam pemahaman bagan, dokumen, dan diagram, serta dalam replikasi visual UI dan frontend. Validasi ulang setiap solusi sementara vision di sisi prompt yang Anda sesuaikan untuk model sebelumnya; solusi tersebut mungkin tidak lagi diperlukan. Kinerja vision paling kuat ketika model memiliki alat untuk menganalisis, memotong, dan memverifikasi pekerjaannya secara visual dan iteratif, dan "tool use" (penggunaan alat) adalah pengungkit yang lebih hemat biaya daripada thinking saja.
* **Pekerjaan konteks panjang:** Claude Opus 5 memiliki ["context window" (jendela konteks) 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) sebagai default sekaligus maksimum, dan kepatuhan instruksi, pemanggilan alat, serta penalarannya tetap konsisten di seluruh jendela tersebut.
* **Tugas Office dan dokumen:** Claude Opus 5 menghasilkan dan bekerja dengan spreadsheet multi-sheet yang kompleks dengan formula yang tidak sederhana, dan menghasilkan slide deck yang terstruktur dengan baik. Berikan prompt dengan gaya atau template spesifik apa pun yang perlu diikutinya.
* **Koordinasi multi-agen:** Claude Opus 5 mengoordinasikan tim subagen dengan baik, dengan pola writer-verifier yang efektif dan sedikit kasus agen yang menimpa pekerjaan satu sama lain. Untuk beban kerja yang sensitif terhadap biaya, batasi delegasi; lihat [Mengontrol pembuatan subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning).

## Panjang respons dan verbositas

Respons default Claude Opus 5 yang ditujukan kepada pengguna lebih panjang daripada model Opus sebelumnya. [Parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) mengontrol seberapa banyak model [berpikir](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost), bukan seberapa banyak yang dikatakannya: menurunkan effort dapat mengurangi volume thinking tanpa secara andal memperpendek respons yang terlihat. Untuk mengontrol panjang respons, berikan prompt secara eksplisit.

Instruksi keringkasan yang singkat sudah efektif. Misalnya, untuk produk multi-giliran yang ditujukan kepada pengguna:

```text wrap
Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
```

Dalam "system prompt" (prompt sistem) yang panjang, pasangkan instruksi tersebut dengan pengingat singkat di dekat akhir prompt:

```text wrap
<tone_preference>
Keep outputs reasonably concise.
</tone_preference>
```

## Pembaruan progres yang ditujukan kepada pengguna

Claude Opus 5 mudah bernarasi selama pekerjaan agentik: model ini cenderung mengumumkan apa yang akan dilakukannya, dan output per pesannya dalam sesi agentik sering kali lebih panjang daripada model sebelumnya. Model ini mendapat manfaat dari panduan eksplisit tentang cara berkomunikasi dengan pengguna selama tugas. Untuk mengurangi narasi, jelaskan irama dan bentuk yang Anda inginkan:

```text wrap
Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it.
```

Untuk meningkatkan narasi, atau mengubah gayanya, pengungkit yang sama berlaku ke arah sebaliknya: jelaskan secara eksplisit seperti apa seharusnya pembaruan tersebut dan berikan contoh. Contoh positif dari gaya komunikasi yang Anda inginkan cenderung lebih efektif daripada instruksi tentang apa yang tidak boleh dilakukan.

## Panjang hasil kerja tertulis

Terpisah dari verbositas percakapan, file yang ditulis Claude Opus 5 ke disk (laporan, dokumen Markdown, ringkasan) sering kali lebih panjang daripada model sebelumnya. Jika produk Anda menyertakan dokumen yang ditulis Claude, tambahkan kalibrasi panjang yang eksplisit:

```text wrap
Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.
```

## Cakupan tugas dan verifikasi berlebihan

Claude Opus 5 memverifikasi pekerjaannya sendiri tanpa diminta. Jika prompt Anda berisi instruksi verifikasi eksplisit ("sertakan langkah verifikasi akhir untuk setiap tugas yang tidak sederhana," "gunakan subagen untuk memverifikasi"), hapuslah: instruksi seperti ini menyebabkan verifikasi berlebihan pada Claude Opus 5, dan menghapusnya mengurangi token yang terbuang tanpa kehilangan kualitas. Hal yang sama berlaku untuk scaffolding harness lama yang menambahkan langkah verifikasi terpisah.

Claude Opus 5 juga dapat memperluas cakupan tugas, menambahkan langkah yang tidak diminta atau menerapkan penilaiannya sendiri tentang apa seharusnya tugas tersebut. Untuk tugas yang sempit, batasi cakupan secara eksplisit:

```text wrap
Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked.
```

## Mengontrol pembuatan subagen

Claude Opus 5 mendelegasikan ke subagen lebih mudah daripada model sebelumnya. Delegasi bermanfaat pada jalur pekerjaan yang benar-benar independen dan cukup besar, tetapi melipatgandakan biaya dan waktu ketika diterapkan pada tugas kecil. Jika harness Anda mendukung subagen, berikan panduan eksplisit tentang skenario mana yang memerlukan delegasi, atau tetapkan batas deterministik pada berapa banyak agen yang dapat diluncurkan. Misalnya:

```text wrap
Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low.
```

Jika harness Anda adalah Claude Code atau Claude Agent SDK, batas deterministiknya adalah variabel lingkungan `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` dan `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` serta opsi `max_budget_usd` pada SDK. Keduanya memerlukan Claude Code 2.1.217 atau lebih baru, jadi perbarui SDK yang di-pin sebelum mengarahkannya ke Claude Opus 5. Claude Code menambahkan instruksi delegasinya sendiri pada Claude Opus 5 hanya ketika Anda menggunakan preset prompt sistem `claude_code`; dengan prompt sistem kustom atau yang dihilangkan, tambahkan sendiri instruksi delegasi seperti contoh di bagian ini. Lihat [Membatasi kedalaman, konkurensi, dan pengeluaran subagen](https://code.claude.com/docs/id/agent-sdk/subagents#cap-subagent-depth-concurrency-and-spend) di dokumentasi Agent SDK.

## Koreksi diri

Claude Opus 5 menangkap dan memperbaiki kesalahannya sendiri dengan baik tanpa prompting. Hindari menginstruksikan pemeriksaan ulang yang sudah dilakukannya ("periksa kembali jawaban Anda," "verifikasi ulang sebelum merespons"); seperti instruksi verifikasi, instruksi ini bertumpuk dengan perilaku model sendiri dan menambah biaya tanpa meningkatkan hasil.

Model ini juga menarasikan koreksi terhadap pernyataan sebelumnya lebih sering daripada model sebelumnya, yang bisa jadi tidak diinginkan dalam produk yang ditujukan kepada pengguna. Untuk membatasi narasi koreksi hanya pada koreksi yang penting:

```text wrap
Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it.
```

## Menjalankan dengan thinking dinonaktifkan

Claude Opus 5 berjalan dengan [thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) aktif secara default, dan thinking hanya dapat dinonaktifkan pada [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah; lihat [panduan migrasi](https://platform.claude.com/docs/id/models/opus-5/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5). Dengan thinking dinonaktifkan, dua artefak terkadang dapat muncul dalam output model yang terlihat. Mitigasi utama untuk keduanya adalah tetap mengaktifkan thinking dan mengontrol biaya token dengan tingkat effort yang lebih rendah alih-alih menonaktifkan thinking: untuk sebagian besar tugas, thinking yang diaktifkan pada effort `low` berkinerja lebih baik daripada thinking yang dinonaktifkan dengan biaya serupa.

**Pemanggilan alat sebagai teks.** Dengan thinking dinonaktifkan, model terkadang menulis pemanggilan alat ke dalam teks yang ditujukan kepada pengguna alih-alih mengeluarkan blok `tool_use` terstruktur. Giliran selesai secara normal dan pemanggilan tersebut tidak pernah berjalan, dan dalam loop agentik teks yang bocor tetap berada dalam riwayat percakapan, sehingga giliran berikutnya juga terpengaruh. Ini paling umum terjadi pada beban kerja yang banyak menggunakan alat seperti pencarian.

**Tag XML internal dalam output.** Dengan thinking dinonaktifkan, model dapat mengeluarkan tag `<thinking>` atau tag XML internal lainnya ke dalam respons yang terlihat. Jika prompt sistem Anda berisi aturan yang menginstruksikan model untuk tidak berpikir atau tidak bernalar, hapuslah; instruksi semacam itu meningkatkan kebocoran tag.

Untuk integrasi yang harus tetap menonaktifkan thinking, satu instruksi gabungan memitigasi kedua artefak: instruksi ini memberi model izin eksplisit untuk berbicara sebelum pemanggilan alat, alternatif selain memaksakan pemanggilan ketika tidak ada alat yang cocok, dan aturan umum yang melarang tag internal:

```text wrap
When you use a tool, you may say a brief sentence first. If no tool can express what the user asked for, say so instead of guessing. Do not include internal or system XML tags in your response.
```

Instruksi yang menyebut tag thinking berdasarkan namanya kurang efektif dibandingkan bentuk umum, jadi hindari menyebutkannya secara spesifik.
