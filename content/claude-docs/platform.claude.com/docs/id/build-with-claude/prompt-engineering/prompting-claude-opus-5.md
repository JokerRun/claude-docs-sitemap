---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5
fetched_at: 2026-07-25T03:07:29.726338Z
sha256: 2e530ecb0d84704f4792992620d29797edff5d1f84e06b415d51956b4c4fd7c4
---

# Prompting Claude Opus 5

Perbedaan perilaku dan pola prompting untuk Claude Opus 5, mencakup verbositas respons, narasi agentik, pembatasan cakupan tugas, delegasi subagen, koreksi diri, dan artefak output saat thinking dinonaktifkan.

---

Panduan ini mencakup pola prompting yang spesifik untuk Claude Opus 5. Untuk kemampuan model dan perubahan API, lihat [Apa yang baru di Claude Opus 5](/docs/id/about-claude/models/whats-new-opus-5). Untuk teknik yang berlaku di semua model Claude saat ini, lihat [Praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Claude Opus 5 dibangun untuk pekerjaan coding agentik yang kompleks dan pekerjaan enterprise, dengan kekuatan khusus pada tugas agentik jangka panjang. Model ini bekerja dengan baik secara langsung pada prompt Claude Opus 4.8 yang sudah ada. Pola-pola berikut mencakup perilaku yang paling sering memerlukan penyetelan.

<Note>
  Untuk perubahan API saat bermigrasi dari Claude Opus 4.8 (thinking aktif secara default, dan menonaktifkan thinking dibatasi pada effort `high`), lihat [panduan migrasi](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5).
</Note>

## Peningkatan kemampuan

Dibandingkan dengan Claude Opus 4.8, peningkatan yang paling relevan untuk prompting adalah:

* **Coding agentik:** Claude Opus 5 paling kuat pada tugas coding yang sulit: fitur multi-file, refactor yang lebih besar, dan pekerjaan fitur end-to-end. Model ini menyelesaikan tugas secara penuh alih-alih meninggalkan stub atau placeholder, dan bekerja paling baik ketika diberikan spesifikasi tugas lengkap di awal dan dibiarkan berjalan. Model ini juga bekerja dengan baik pada tugas yang lebih mudah seperti pengeditan satu giliran, di mana perbedaan dari model sebelumnya lebih kecil.
* **Tinjauan kode dan pencarian bug:** Claude Opus 5 meninjau kode dengan presisi dan recall yang tinggi: model ini menemukan bug nyata dengan tingkat yang tinggi per lintasan, dan temuan tambahannya sebagian besar adalah masalah nyata alih-alih false positive. Akurasi tetap terjaga pada pengaturan effort yang lebih rendah, yang mendukung lintasan cepat saat waktu tinjauan dan lintasan yang lebih menyeluruh kemudian. Jika prompt tinjauan Anda mengatakan "hanya laporkan masalah dengan tingkat keparahan tinggi" atau "bersikaplah konservatif," model mungkin mengikuti instruksi tersebut secara harfiah dan melaporkan lebih sedikit; mintalah model untuk melaporkan semuanya dan lakukan penyaringan dalam lintasan terpisah sebagai gantinya.
* **Efisiensi pada effort yang lebih rendah:** [Effort](/docs/id/build-with-claude/effort) `low` dan `medium` menghasilkan kualitas yang kuat dengan sebagian kecil dari token dan latensi dibandingkan pengaturan yang lebih tinggi. Mulailah dengan default (`high`) dan sesuaikan berdasarkan eval Anda: gunakan `low` dan `medium` secara leluasa sebagai kontrol utama Anda untuk biaya token dan waktu respons di mana pun kualitas tetap terjaga, dan naikkan ke `xhigh` untuk pekerjaan coding dan agentik yang menuntut. Jika Anda membawa default effort dari model sebelumnya, jalankan kembali sapuan effort pada eval Anda sendiri. Lihat [Effort](/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-opus-5) untuk rekomendasi lengkap.
* **Vision:** Claude Opus 5 kuat dalam pemahaman bagan, dokumen, dan diagram, serta dalam replikasi visual UI dan frontend. Validasi ulang setiap solusi vision di sisi prompt yang Anda setel untuk model sebelumnya; solusi tersebut mungkin tidak lagi diperlukan. Kinerja vision paling kuat ketika model memiliki alat untuk menganalisis, memotong, dan memverifikasi pekerjaannya secara visual dan iteratif, dan penggunaan alat adalah tuas yang lebih hemat biaya daripada thinking saja.
* **Pekerjaan konteks panjang:** Claude Opus 5 memiliki [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) sebagai default sekaligus maksimum, dan kemampuan mengikuti instruksi, pemanggilan alat, dan penalarannya tetap konsisten di sepanjang jendela tersebut.
* **Tugas perkantoran dan dokumen:** Claude Opus 5 menghasilkan dan bekerja dengan spreadsheet multi-sheet yang kompleks dengan formula yang tidak sepele, dan menghasilkan slide deck yang terstruktur dengan baik. Berikan prompt dengan gaya atau templat spesifik apa pun yang perlu diikutinya.
* **Koordinasi multi-agen:** Claude Opus 5 mengoordinasikan tim subagen dengan baik, dengan pola writer-verifier yang efektif dan sedikit kasus agen yang saling menimpa pekerjaan satu sama lain. Untuk beban kerja yang sensitif terhadap biaya, batasi delegasi; lihat [Mengontrol pemunculan subagen](#controlling-subagent-spawning).

## Panjang respons dan verbositas

Respons default yang ditampilkan kepada pengguna dari Claude Opus 5 lebih panjang daripada model Opus sebelumnya. [Parameter effort](/docs/id/build-with-claude/effort) mengontrol seberapa banyak model [berpikir](/docs/id/build-with-claude/thinking-steering-and-cost) alih-alih seberapa banyak yang dikatakannya: menurunkan effort dapat mengurangi volume thinking tanpa secara andal memperpendek respons yang terlihat. Untuk mengontrol panjang respons, berikan prompt secara eksplisit.

Instruksi keringkasan yang singkat sudah efektif. Misalnya, untuk produk multi-giliran yang ditampilkan kepada pengguna:

```text wrap
Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
```

Dalam prompt sistem yang panjang, pasangkan instruksi tersebut dengan pengingat singkat di dekat akhir prompt:

```text wrap
<tone_preference>
Keep outputs reasonably concise.
</tone_preference>
```

## Pembaruan progres yang ditampilkan kepada pengguna

Claude Opus 5 mudah bernarasi selama pekerjaan agentik: model ini cenderung mengumumkan apa yang akan dilakukannya, dan output per pesannya dalam sesi agentik sering kali lebih panjang daripada model sebelumnya. Model ini mendapat manfaat dari panduan eksplisit tentang cara berkomunikasi dengan pengguna selama tugas. Untuk mengurangi narasi, jelaskan irama dan bentuk yang Anda inginkan:

```text wrap
Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it.
```

Untuk meningkatkan narasi, atau mengubah gayanya, tuas yang sama berlaku ke arah sebaliknya: jelaskan secara eksplisit seperti apa pembaruan seharusnya dan berikan contoh. Contoh positif dari gaya komunikasi yang Anda inginkan cenderung lebih efektif daripada instruksi tentang apa yang tidak boleh dilakukan.

## Panjang hasil kerja tertulis

Terpisah dari verbositas percakapan, file yang ditulis Claude Opus 5 ke disk (laporan, dokumen Markdown, ringkasan) sering kali lebih panjang daripada model sebelumnya. Jika produk Anda menyertakan dokumen yang ditulis oleh Claude, tambahkan kalibrasi panjang yang eksplisit:

```text wrap
Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.
```

## Cakupan tugas dan verifikasi berlebihan

Claude Opus 5 memverifikasi pekerjaannya sendiri tanpa diminta. Jika prompt Anda berisi instruksi verifikasi eksplisit ("sertakan langkah verifikasi akhir untuk tugas yang tidak sepele," "gunakan subagen untuk memverifikasi"), hapus instruksi tersebut: instruksi seperti ini menyebabkan verifikasi berlebihan pada Claude Opus 5, dan menghapusnya mengurangi token yang terbuang tanpa kehilangan kualitas. Hal yang sama berlaku untuk scaffolding harness lama yang menambahkan langkah verifikasi terpisah.

Claude Opus 5 juga dapat memperluas cakupan tugas, menambahkan langkah yang tidak diminta atau menerapkan penilaiannya sendiri tentang apa yang seharusnya menjadi tugas tersebut. Untuk tugas yang sempit, batasi cakupan secara eksplisit:

```text wrap
Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked.
```

## Mengontrol pemunculan subagen

Claude Opus 5 mendelegasikan ke subagen lebih mudah daripada model sebelumnya. Delegasi memberikan hasil pada jalur pekerjaan yang benar-benar independen dan berukuran besar, tetapi melipatgandakan biaya dan waktu ketika diterapkan pada tugas kecil. Jika harness Anda mendukung subagen, berikan panduan eksplisit tentang skenario mana yang layak untuk delegasi, atau tetapkan batas deterministik pada berapa banyak agen yang dapat diluncurkan. Misalnya:

```text wrap
Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low.
```

## Koreksi diri

Claude Opus 5 menangkap dan memperbaiki kesalahannya sendiri dengan baik tanpa prompting. Hindari menginstruksikan pemeriksaan ulang yang sudah dilakukannya ("periksa kembali jawaban Anda," "verifikasi ulang sebelum merespons"); seperti instruksi verifikasi, instruksi ini bertumpuk dengan perilaku model itu sendiri dan menambah biaya tanpa meningkatkan hasil.

Model ini juga menarasikan koreksi terhadap pernyataan sebelumnya lebih banyak daripada model sebelumnya, yang bisa tidak diinginkan dalam produk yang ditampilkan kepada pengguna. Untuk membatasi narasi koreksi hanya pada koreksi yang penting:

```text wrap
Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it.
```

## Berjalan dengan thinking dinonaktifkan

Claude Opus 5 berjalan dengan [thinking](/docs/id/build-with-claude/thinking) aktif secara default, dan thinking hanya dapat dinonaktifkan pada [effort](/docs/id/build-with-claude/effort) `high` atau di bawahnya; lihat [panduan migrasi](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5). Dengan thinking dinonaktifkan, dua artefak kadang-kadang dapat muncul dalam output model yang terlihat. Mitigasi utama untuk keduanya adalah tetap mengaktifkan thinking dan mengontrol biaya token dengan tingkat effort yang lebih rendah alih-alih menonaktifkan thinking: untuk sebagian besar tugas, thinking yang diaktifkan pada effort `low` berkinerja lebih baik daripada thinking yang dinonaktifkan dengan biaya serupa.

**Panggilan alat sebagai teks.** Dengan thinking dinonaktifkan, model kadang-kadang menulis panggilan alat ke dalam teks yang ditampilkan kepada pengguna alih-alih mengeluarkan blok `tool_use` yang terstruktur. Giliran selesai secara normal dan panggilan tidak pernah berjalan, dan dalam loop agentik teks yang bocor tetap berada dalam riwayat percakapan, sehingga giliran berikutnya juga terpengaruh. Ini paling umum terjadi pada beban kerja yang banyak menggunakan alat seperti pencarian.

**Tag XML internal dalam output.** Dengan thinking dinonaktifkan, model dapat mengeluarkan tag `<thinking>` atau tag XML internal lainnya ke dalam respons yang terlihat. Jika prompt sistem Anda berisi aturan yang menginstruksikan model untuk tidak berpikir atau tidak bernalar, hapus aturan tersebut; instruksi semacam itu meningkatkan kebocoran tag.

Untuk integrasi yang harus tetap menonaktifkan thinking, satu instruksi gabungan memitigasi kedua artefak: instruksi ini memberikan izin eksplisit kepada model untuk berbicara sebelum panggilan alat, alternatif untuk memaksa panggilan ketika tidak ada alat yang cocok, dan aturan umum terhadap tag internal:

```text wrap
When you use a tool, you may say a brief sentence first. If no tool can express what the user asked for, say so instead of guessing. Do not include internal or system XML tags in your response.
```

Instruksi yang menyebutkan tag thinking secara spesifik kurang efektif dibandingkan bentuk umum, jadi hindari menyebutkannya secara spesifik.
