---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 09616e660268a1aa625fce59c7a4bcd9584be6ee70d13292a4a5aad772081a21
---

# Prompting Claude Fable 5

Perbedaan perilaku dan pola prompting untuk Claude Fable 5 dan Claude Mythos 5, mencakup effort, kepatuhan instruksi, run panjang, memori, dan perubahan scaffolding.

---

Panduan ini mencakup pola prompting dan scaffolding yang spesifik untuk Claude Fable 5 dan Claude Mythos 5. Untuk kemampuan model, perubahan API, harga, dan ketersediaan, lihat [Memperkenalkan Claude Fable 5 dan Claude Mythos 5](/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5). Untuk teknik yang berlaku di semua model Claude saat ini, lihat [Praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Claude Fable 5 menangani masalah yang sebelumnya terlalu kompleks, terlalu lama berjalan, atau terlalu ambigu untuk model-model sebelumnya, dan sangat efektif pada pekerjaan end-to-end yang membutuhkan waktu berjam-jam, berhari-hari, atau berminggu-minggu bagi seseorang untuk menyelesaikannya. Tim yang melihat hasil terbaik menerapkan Claude Fable 5 pada masalah tersulit mereka yang belum terpecahkan; mengujinya hanya pada beban kerja yang lebih sederhana cenderung meremehkan rentang kemampuannya. Model ini juga bekerja dengan andal pada tugas-tugas yang lebih sederhana.

Claude Fable 5 memiliki beberapa perbedaan perilaku dari Claude Opus 4.8 yang mungkin memerlukan pembaruan prompt atau scaffolding. Peningkatan kemampuan pada level ini juga merupakan momen yang baik untuk mengevaluasi ulang instruksi, alat, dan guardrail mana yang masih diperlukan. Pola-pola di bawah ini mencakup perilaku yang paling sering memerlukan penyesuaian.

<Note>
  Untuk perubahan parameter API yang spesifik untuk Claude Fable 5 dan Claude Mythos 5 (hanya adaptive thinking, output thinking yang hanya diringkas, tanpa budget pemikiran diperpanjang, stop reason `refusal` dan penanganan fallback), lihat [Memperkenalkan Claude Fable 5 dan Claude Mythos 5](/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5).

  Claude Fable 5 menjalankan classifier keamanan yang menargetkan teknik keamanan siber ofensif (seperti membangun exploit, malware, atau perkakas serangan), konten biologi dan ilmu hayati (seperti metode laboratorium atau mekanisme molekuler), dan ekstraksi thinking model yang telah diringkas. Pekerjaan keamanan siber yang tidak berbahaya dan tugas ilmu hayati yang bermanfaat juga dapat memicu pengaman ini. Untuk mengalihkan permintaan yang ditolak secara otomatis, konfigurasikan [fallback sisi server atau sisi klien](/docs/id/build-with-claude/refusals-and-fallback) ke Claude Opus 4.8.
</Note>

## Peningkatan kemampuan

Dibandingkan dengan Claude Opus 4.8, Claude Fable 5 menunjukkan peningkatan dalam:

* **Otonomi jangka panjang.** Claude Fable 5 mempertahankan output yang produktif selama periode yang panjang, menyelesaikan run berorientasi tujuan selama beberapa hari dengan retensi instruksi yang kuat di sepanjang tugas yang panjang dan kompleks.
* **Kebenaran pada percobaan pertama untuk masalah kompleks yang terspesifikasi dengan baik.** Penguji awal melaporkan implementasi sekali jalan untuk sistem yang sebelumnya membutuhkan iterasi berhari-hari.
* **Visi.** Claude Fable 5 menginterpretasikan gambar teknis yang padat, aplikasi web, dan tangkapan layar yang detail dengan akurasi yang jauh lebih tinggi, sering kali sambil menggunakan lebih sedikit token output, dan dilatih untuk menggunakan alat bash dan crop untuk menangani gambar yang terbalik, buram, atau bernoise.
* **Alur kerja enterprise.** Claude Fable 5 mengikuti instruksi, tetap dalam cakupan, dan menghasilkan output berkualitas profesional pada analisis keuangan, spreadsheet, slide, dan dokumen.
* **Code review dan debugging.** Recall penemuan bug (di luar domain keamanan siber yang dicakup oleh classifier keamanan) terasa lebih tinggi daripada Claude Opus 4.8, termasuk pencarian di seluruh codebase dan riwayat repositori.
* **Menavigasi ambiguitas.** Claude Fable 5 bekerja dengan baik ketika diberi permintaan yang kompleks dan bercabang banyak serta diminta untuk menentukan langkah selanjutnya.
* **Delegasi dan kolaborasi.** Claude Fable 5 secara signifikan lebih dapat diandalkan dalam mengirim dan mempertahankan subagen paralel, dan secara andal mengelola komunikasi berkelanjutan dengan subagen yang berjalan lama dan agen sejawat.

Di luar peningkatan spesifik ini, Claude Fable 5 secara umum lebih mampu daripada model-model sebelumnya pada hampir semua tugas. Claude Fable 5 tidak ditujukan untuk pekerjaan keamanan siber ofensif atau biologi dan ilmu hayati; permintaan di domain tersebut dapat mengembalikan [`stop_reason: "refusal"`](/docs/id/build-with-claude/refusals-and-fallback).

## Giliran yang lebih panjang secara default

Permintaan individual pada tugas yang sulit dapat berjalan selama beberapa menit pada pengaturan [effort](/docs/id/build-with-claude/effort) yang lebih tinggi, terutama ketika tugas tersebut memerlukan pengumpulan konteks, pembangunan, dan verifikasi mandiri, dan run otonom dapat berlangsung selama berjam-jam. Ini adalah salah satu perubahan terbesar yang dihadapi tim saat menyesuaikan diri dengan Claude Fable 5. Sesuaikan timeout klien, streaming, dan indikator progres yang dilihat pengguna sebelum migrasi, dan pertimbangkan untuk merestrukturisasi harness agar memeriksa run secara asinkron, misalnya melalui job terjadwal, alih-alih memblokir. Untuk mencegah Claude Fable 5 melakukan perencanaan berlebihan ketika tugas bersifat ambigu:

```text wrap
When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks.
```

## Pertimbangkan semua level effort

[Effort](/docs/id/build-with-claude/effort) adalah kontrol utama untuk trade-off antara kecerdasan, latensi, dan biaya pada Claude Fable 5. Gunakan `high` sebagai default untuk sebagian besar tugas, dengan `xhigh` untuk beban kerja yang paling sensitif terhadap kemampuan dan `medium` atau `low` untuk pekerjaan rutin. Pengaturan effort yang lebih rendah pada Claude Fable 5 tetap bekerja dengan baik dan sering kali melampaui performa `xhigh` pada model-model sebelumnya. Kurangi effort jika sebuah tugas selesai tetapi memakan waktu lebih lama dari yang diperlukan, atau jika Anda menginginkan gaya kerja yang lebih cepat dan lebih interaktif.

Pada pekerjaan rutin dengan effort yang lebih tinggi, Claude Fable 5 dapat mengumpulkan konteks dan berdeliberasi melebihi apa yang dibutuhkan tugas. Pada saat yang sama, effort yang lebih tinggi sering menghasilkan perilaku verifikasi yang sangat baik, penalaran yang canggih, dan output yang paling teliti. Untuk mencegah perapian atau refactoring yang tidak diminta pada effort yang lebih tinggi:

```text wrap
Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need surrounding cleanup and a one-shot operation usually doesn't need a helper. Don't design for hypothetical future requirements: do the simplest thing that works well. Avoid premature abstraction and half-finished implementations. Don't add error handling, fallbacks, or validation for scenarios that cannot happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs). Don't use feature flags or backwards-compatibility shims when you can just change the code.
```

## Kepatuhan instruksi yang kuat

Kepatuhan terhadap instruksi telah cukup meningkat sehingga Anda dapat mengarahkan sebagian besar perilaku dengan instruksi singkat alih-alih menyebutkan setiap perilaku satu per satu. Sebagai contoh, ketika tidak diarahkan, Claude Fable 5 dapat mengelaborasi melebihi apa yang dibutuhkan tugas, terutama pada pengaturan effort yang lebih tinggi: menyurvei opsi yang tidak akan dikerjakannya, menjelaskan akar masalah secara panjang lebar, menghasilkan deskripsi PR yang sangat terstruktur, atau menulis komentar yang menarasikan apa yang dilakukan baris berikutnya. Instruksi singkat tentang keringkasan sama efektifnya dengan mendaftar setiap pola:

```text wrap
Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail and reasoning come after. Being readable and being concise are different things, and readability matters more.

The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon.
```

Hal yang sama berlaku untuk perilaku checkpoint dalam alur kerja yang berjalan lama. Agar Claude Fable 5 berhenti hanya di tempat yang benar-benar membutuhkan Anda, tidak perlu menyebutkan setiap kasus:

```text wrap
Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise.
```

## Dasarkan klaim progres pada bukti selama run panjang

Pada run otonom yang panjang, instruksikan Claude Fable 5 untuk mengaudit progres terhadap hasil alat yang sebenarnya. Dalam pengujian Anthropic, ini hampir menghilangkan laporan status yang dibuat-buat bahkan pada tugas yang dirancang untuk memancingnya:

```text wrap
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.
```

## Nyatakan batasannya

Claude Fable 5 terkadang dapat mengambil tindakan yang tidak diminta (menyusun draf email padahal tidak diminta, membuat backup git-branch defensif). Definisikan batasan eksplisit tentang apa yang boleh dan tidak boleh dilakukan Claude Fable 5:

```text wrap
When the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one. Before running a command that changes system state (restarts, deletes, config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

## Subagen paralel

Claude Fable 5 mengirim subagen paralel lebih mudah daripada model-model sebelumnya. Gunakan subagen secara sering, berikan panduan eksplisit tentang kapan delegasi tepat dilakukan, dan utamakan komunikasi asinkron antara orkestrator dan subagen daripada memblokir hingga setiap subagen kembali. Subagen berumur panjang yang mempertahankan konteksnya di sepanjang subtugas menghemat waktu dan biaya melalui pembacaan cache dan menghindari bottleneck pada subagen yang paling lambat.

```text wrap
Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context.
```

## Bangun sistem memori

Claude Fable 5 bekerja sangat baik ketika dapat mencatat pelajaran dari run sebelumnya dan merujuknya. Sediakan tempat untuk menulis catatan, sesederhana file Markdown:

```text wrap
Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong.
```

Untuk memulai sistem memori dari riwayat yang sudah ada, minta Claude Fable 5 meninjau sesi-sesi sebelumnya:

```text wrap
Reflect on the previous sessions we've had together. Use subagents to identify core themes and lessons, and store them in [X]. Make sure you know to reference [X] for future use.
```

## Kasus langka berhenti lebih awal

Jauh di dalam sesi yang panjang, Claude Fable 5 terkadang dapat mengakhiri giliran dengan pernyataan niat berupa teks saja ("Saya sekarang akan menjalankan X") tanpa mengeluarkan panggilan alat yang sesuai, atau berhenti untuk meminta izin padahal sudah memiliki cukup informasi untuk melanjutkan. Sebuah "lanjutkan" atau "silakan kerjakan sampai selesai" sudah cukup. Untuk mendefinisikan kapan berhenti sejenak itu tepat, padukan ini dengan instruksi checkpoint di [Kepatuhan instruksi yang kuat](#strong-instruction-following). Untuk pipeline otonom, tambahkan pengingat sistem:

```text wrap
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking "Want me to…?" or "Shall I…?" will block the work. For reversible actions that follow from the original request, proceed without asking. Offering follow-ups after the task is done is fine; asking permission after already discussing with the user before doing the work is not. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ("I'll…", "let me know when…"), do that work now with tool calls. End your turn only when the task is complete or you are blocked on input only the user can provide.
```

## Kasus langka kekhawatiran budget konteks

Dalam sesi yang sangat panjang, Claude Fable 5 terkadang dapat menyarankan sesi baru, menawarkan untuk merangkum dan menyerahkan, atau memangkas pekerjaannya sendiri. Ini paling sering dipicu ketika harness menampilkan hitungan mundur token tersisa kepada model. Hindari menampilkan hitungan budget konteks secara eksplisit jika memungkinkan. Jika harness harus menampilkannya, sebuah penenangan akan membantu:

```text wrap
You have ample context remaining. Do not stop, summarize, or suggest a new session on account of context limits. Continue the work.
```

## Berikan alasannya, bukan hanya permintaannya

Claude Fable 5 cenderung bekerja lebih baik ketika memahami maksud di balik sebuah permintaan: konteks memungkinkannya menghubungkan tugas dengan informasi yang relevan alih-alih menyimpulkan maksud sendiri. Berikan konteks tentang mengapa Anda meminta, terutama untuk agen yang berjalan lama yang mengambil dari beberapa alur kerja:

```text wrap
I'm working on [the larger task] for [who it's for]. They need [what the output enables]. With that in mind: [request].
```

## Keterbacaan saat berkomunikasi dengan pengguna

Dalam percakapan yang panjang atau agentik (banyak panggilan alat, konteks kerja yang besar), Claude Fable 5 dapat menghasilkan teks yang sulit diikuti: singkatan rantai panah yang padat, detail implementasi yang dalam, referensi ke thinking yang tidak pernah dilihat pengguna, atau frasa yang terlalu teknis. Tambahan gaya komunikasi dapat memitigasi ini:

```text wrap
Terse shorthand is fine between tool calls (that's you thinking out loud, and brevity there is good). Your final summary is different: it's for a reader who didn't see any of that.

If you've been working for a while without the user watching (overnight, across many tool calls, since they last spoke), your final message is their first look at any of it. Write it as a re-grounding, not a continuation of your working thread: the outcome first, then the one or two things you need from them, each explained as if new. The vocabulary you built up while working is yours, not theirs; leave it behind unless you re-introduce it.

When you write the summary at the end, drop the working shorthand. Write complete sentences. Spell out terms. Don't use arrow chains, hyphen-stacked compounds, or labels you made up earlier. When you mention files, commits, flags, or other identifiers, give each one its own plain-language clause. Open with the outcome: one sentence on what happened or what you found. Then the supporting detail. If you have to choose between short and clear, choose clear.
```

## Buat alat send-to-user

Saat menjalankan agen asinkron yang panjang, berikan agen cara untuk menampilkan pesan yang harus dilihat pengguna persis seperti yang ditulis, tanpa mengakhiri gilirannya: sebuah deliverable (cuplikan kode yang dihasilkan atau draf pesan), pembaruan progres dengan angka spesifik, atau balasan langsung untuk pertanyaan yang diajukan pengguna di tengah loop. Input alat ini adalah pesan yang akan ditampilkan; ketika Claude memanggilnya, render input tersebut langsung di UI Anda dan kembalikan pengakuan sederhana sebagai hasil alat. Input alat tidak pernah diringkas, sehingga konten tiba secara utuh.

```json
{
  "name": "send_to_user",
  "description": "Display a message directly to the user. Use this for progress updates, partial results, or content the user must see exactly as written before the task finishes.",
  "input_schema": {
    "type": "object",
    "properties": {
      "message": {
        "type": "string",
        "description": "The content to display to the user."
      }
    },
    "required": ["message"]
  }
}
```

Tambahkan alat ini kapan pun UX Anda bergantung pada penyampaian konten atau interaksi pengguna langsung secara verbatim di tengah tugas. Untuk agen yang hanya menarasikan progres rutin, ringkasan dari model itu sendiri biasanya sudah memadai. Mendefinisikan alat saja tidak cukup; tanpa instruksi di prompt sistem, Claude Fable 5 jarang memanggilnya. Padukan alat ini dengan bahasa elisitasi seperti:

```text wrap
Between tool calls, when you have content the user must read verbatim (a partial deliverable, a direct answer to their question), call the send_to_user tool with that content. Use send_to_user only for user-facing content, not for narration or reasoning.
```

Jangan mengarahkan narasi atau penalaran internal melalui `send_to_user`; memanggilnya secara berlebihan untuk konten yang tidak ditujukan kepada pengguna menggagalkan tujuannya.

## Perubahan scaffolding yang direkomendasikan

* **Mulai dari puncak rentang kesulitan Anda.** Pilih tugas yang lebih sulit daripada yang akan Anda berikan ke model-model sebelumnya, dan minta Claude Fable 5 menentukan cakupannya, mengajukan pertanyaan klarifikasi, dan mengeksekusinya.
* **Buat verifikasi mandiri eksplisit dalam prompt run panjang.** Subagen verifikator terpisah dengan konteks baru cenderung mengungguli kritik diri. Untuk tugas yang berjalan lama, instruksikan: `Establish a method for checking your own work at an interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the specification.`
* **Refactor prompt dan skill yang sudah ada.** Skill yang dikembangkan untuk model-model sebelumnya sering kali terlalu preskriptif untuk Claude Fable 5 dan dapat menurunkan kualitas output. Tinjau dan pertimbangkan untuk menghapus instruksi lama jika performa default lebih baik. Claude Fable 5 juga melakukan pekerjaan yang baik dalam memperbarui skill secara langsung berdasarkan apa yang dipelajarinya dari tugas yang sedang dikerjakan.
* **Jangan instruksikan Claude untuk mereproduksi penalarannya dalam respons.** Prompt, skill, atau instruksi harness yang memberi tahu model untuk menggemakan, menyalin, atau menjelaskan penalaran internalnya sebagai teks respons dapat memicu [kategori penolakan `reasoning_extraction`](/docs/id/build-with-claude/refusals-and-fallback#refusal-response) pada Claude Fable 5, menyebabkan peningkatan fallback ke Claude Opus 4.8. Audit skill dan prompt sistem yang ada untuk instruksi refleksi atau tunjukkan-pemikiran-Anda saat migrasi. Jika aplikasi Anda memerlukan visibilitas penalaran, baca blok `thinking` terstruktur dari [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) sebagai gantinya, dan gunakan [alat send-to-user](#create-a-send-to-user-tool) untuk menampilkan progres selama run panjang.
* **Buat alat send-to-user.** Untuk agen asinkron yang panjang, alat sisi klien menyampaikan pesan ke pengguna secara verbatim tanpa mengakhiri giliran. Lihat [Buat alat send-to-user](#create-a-send-to-user-tool).
