---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/context-windows
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: 0be557cba73c5bb0a34228e11cf5eff6a331226edc05effea62a8de13c8f2e77
---

# Jendela konteks

---

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

Seiring percakapan berkembang, Anda pada akhirnya akan mendekati batas jendela konteks. Panduan ini menjelaskan cara kerja jendela konteks dan memperkenalkan strategi untuk mengelolanya secara efektif.

Untuk percakapan yang berjalan lama dan alur kerja agentik, [server-side compaction](/docs/id/build-with-claude/compaction) adalah strategi utama untuk manajemen konteks. Untuk kebutuhan yang lebih khusus, [context editing](/docs/id/build-with-claude/context-editing) menawarkan strategi tambahan seperti pembersihan hasil alat dan pembersihan blok pemikiran.

## Memahami jendela konteks \{#understanding-the-context-window}

"Context window" (jendela konteks) mengacu pada semua teks yang dapat direferensikan oleh model bahasa saat menghasilkan respons, termasuk respons itu sendiri. Ini berbeda dari corpus data besar tempat model bahasa dilatih, dan sebaliknya mewakili "memori kerja" untuk model. Jendela konteks yang lebih besar memungkinkan model untuk menangani prompt yang lebih kompleks dan panjang, tetapi lebih banyak konteks tidak secara otomatis lebih baik. Seiring jumlah token bertambah, akurasi dan kemampuan mengingat menurun, sebuah fenomena yang dikenal sebagai *context rot*. Hal ini membuat kurasi apa yang ada dalam konteks sama pentingnya dengan seberapa banyak ruang yang tersedia.

Claude mencapai hasil terbaik di kelasnya pada benchmark pengambilan konteks panjang seperti [MRCR](https://arxiv.org/abs/2501.03276) dan [GraphWalks](https://arxiv.org/abs/2412.04360), tetapi peningkatan ini bergantung pada apa yang ada dalam konteks, bukan hanya seberapa banyak yang muat.

<Tip>
Untuk pembahasan mendalam tentang mengapa konteks panjang mengalami penurunan dan cara merekayasa solusinya, lihat [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
</Tip>

Diagram di bawah ini mengilustrasikan perilaku jendela konteks standar untuk permintaan API<sup>1</sup>:

![Diagram jendela konteks](/docs/images/context-window.svg)

_<sup>1</sup>Untuk antarmuka chat, seperti [claude.ai](https://claude.ai/), jendela konteks juga dapat diatur dengan sistem bergulir "first in, first out"._

* **Akumulasi token progresif:** Seiring percakapan berlanjut melalui giliran, setiap pesan pengguna dan respons asisten terakumulasi dalam jendela konteks. Giliran sebelumnya dipertahankan sepenuhnya.
* **Pola pertumbuhan linear:** Penggunaan konteks tumbuh secara linear dengan setiap giliran, dengan giliran sebelumnya dipertahankan sepenuhnya.
* **Kapasitas jendela konteks:** Total jendela konteks yang tersedia (hingga 1 juta token) mewakili kapasitas maksimum untuk menyimpan riwayat percakapan dan menghasilkan output baru dari Claude.
* **Alur input-output:** Setiap giliran terdiri dari:
  - **Fase input:** Berisi semua riwayat percakapan sebelumnya ditambah pesan pengguna saat ini
  - **Fase output:** Menghasilkan respons teks yang menjadi bagian dari input di masa mendatang

## Jendela konteks dengan pemikiran diperpanjang \{#the-context-window-with-extended-thinking}

Saat menggunakan [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking), semua token input dan output, termasuk token yang digunakan untuk berpikir, dihitung terhadap batas jendela konteks, dengan beberapa nuansa dalam situasi multi-giliran.

Token anggaran pemikiran adalah bagian dari parameter `max_tokens` Anda, ditagih sebagai token output, dan dihitung terhadap batas laju. Dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), Claude secara dinamis menentukan alokasi pemikirannya, sehingga penggunaan token pemikiran aktual dapat bervariasi per permintaan.

Namun, blok pemikiran sebelumnya secara otomatis dihapus dari perhitungan jendela konteks oleh API Claude dan bukan bagian dari riwayat percakapan yang "dilihat" model untuk giliran berikutnya, sehingga mempertahankan kapasitas token untuk konten percakapan yang sebenarnya.

Diagram di bawah ini menunjukkan manajemen token khusus saat pemikiran diperpanjang diaktifkan:

![Diagram jendela konteks dengan pemikiran diperpanjang](/docs/images/context-window-thinking.svg)

* **Penghapusan pemikiran diperpanjang:** Blok pemikiran diperpanjang (ditampilkan dalam warna abu-abu gelap) dihasilkan selama fase output setiap giliran, **tetapi tidak dibawa sebagai token input untuk giliran berikutnya**. Anda tidak perlu menghapus blok pemikiran sendiri. API Claude secara otomatis melakukan ini untuk Anda jika Anda mengirimkannya kembali.
* **Detail implementasi teknis:**
  - API secara otomatis mengecualikan blok pemikiran dari giliran sebelumnya saat Anda mengirimkannya kembali sebagai bagian dari riwayat percakapan.
  - Token pemikiran diperpanjang ditagih sebagai token output hanya sekali, selama pembuatannya.
  - Perhitungan jendela konteks efektif menjadi: `context_window = (input_tokens - previous_thinking_tokens) + current_turn_tokens`.
  - Token pemikiran mencakup blok `thinking`.

Arsitektur ini efisien dalam penggunaan token dan memungkinkan penalaran ekstensif tanpa pemborosan token, karena blok pemikiran dapat memiliki panjang yang substansial.

<Note>
Anda dapat membaca lebih lanjut tentang jendela konteks dan pemikiran diperpanjang di [panduan pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking).
</Note>

## Jendela konteks dengan pemikiran diperpanjang dan penggunaan alat \{#the-context-window-with-extended-thinking-and-tool-use}

Diagram di bawah ini mengilustrasikan manajemen token jendela konteks saat menggabungkan pemikiran diperpanjang dengan penggunaan alat:

![Diagram jendela konteks dengan pemikiran diperpanjang dan penggunaan alat](/docs/images/context-window-thinking-tools.svg)

<Steps>
  <Step title="Arsitektur giliran pertama">
    - **Komponen input:** Konfigurasi alat dan pesan pengguna
    - **Komponen output:** Pemikiran diperpanjang + respons teks + permintaan penggunaan alat
    - **Perhitungan token:** Semua komponen input dan output dihitung terhadap jendela konteks, dan semua komponen output ditagih sebagai token output.
  </Step>
  <Step title="Penanganan hasil alat (giliran 2)">
    - **Komponen input:** Setiap blok di giliran pertama dan `tool_result`. Blok pemikiran diperpanjang **harus** dikembalikan bersama dengan hasil alat yang sesuai. Ini adalah satu-satunya kasus di mana Anda **harus** mengembalikan blok pemikiran.
    - **Komponen output:** Setelah hasil alat dikirimkan kembali ke Claude, Claude merespons hanya dengan teks (tidak ada pemikiran diperpanjang tambahan hingga pesan `user` berikutnya, kecuali [interleaved thinking](/docs/id/build-with-claude/extended-thinking#interleaved-thinking) diaktifkan).
    - **Perhitungan token:** Semua komponen input dan output dihitung terhadap jendela konteks, dan semua komponen output ditagih sebagai token output.
  </Step>
  <Step title="Giliran pengguna baru (giliran 3)">
    - **Komponen input:** Semua input dan output dari giliran sebelumnya dibawa ke depan dengan pengecualian blok pemikiran, yang dapat dihapus sekarang karena Claude telah menyelesaikan seluruh siklus penggunaan alat. API akan secara otomatis menghapus blok pemikiran untuk Anda jika Anda mengirimkannya kembali, atau Anda bebas menghapusnya sendiri pada tahap ini. Di sinilah Anda juga akan menambahkan giliran `user` berikutnya.
    - **Komponen output:** Karena ada giliran `user` baru di luar siklus penggunaan alat, Claude menghasilkan blok pemikiran diperpanjang baru dan melanjutkan dari sana.
    - **Perhitungan token:** Token pemikiran sebelumnya secara otomatis dihapus dari perhitungan jendela konteks. Semua blok sebelumnya lainnya masih dihitung sebagai bagian dari jendela token, dan blok pemikiran di giliran `assistant` saat ini dihitung sebagai bagian dari jendela konteks.
  </Step>
</Steps>

* **Pertimbangan untuk penggunaan alat dengan pemikiran diperpanjang:**
  - Saat mengirimkan hasil alat, seluruh blok pemikiran yang tidak dimodifikasi yang menyertai permintaan alat spesifik tersebut (termasuk bagian signature) harus disertakan.
  - Perhitungan jendela konteks efektif untuk pemikiran diperpanjang dengan penggunaan alat menjadi: `context_window = input_tokens + current_turn_tokens`.
  - Sistem menggunakan tanda tangan kriptografis untuk memverifikasi keaslian blok pemikiran. Kegagalan mempertahankan blok pemikiran selama penggunaan alat dapat merusak kontinuitas penalaran Claude. Oleh karena itu, jika Anda memodifikasi blok pemikiran, API akan mengembalikan error.

<Note>
Model Claude 4 mendukung [interleaved thinking](/docs/id/build-with-claude/extended-thinking#interleaved-thinking), yang memungkinkan Claude untuk berpikir di antara panggilan alat dan melakukan penalaran yang lebih canggih setelah menerima hasil alat.

Untuk informasi lebih lanjut tentang menggunakan alat dengan pemikiran diperpanjang, lihat [panduan pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-tool-use).
</Note>

Pemilihan alat Claude dirancang untuk tetap andal dengan dokumen input yang besar, memilih alat yang tepat (atau dengan benar menahan diri) ketika percakapan mencakup 100K+ token konteks non-alat. Untuk mengurangi konteks yang dikonsumsi oleh alat itu sendiri, lihat [Mengelola konteks alat](/docs/id/agents-and-tools/tool-use/manage-tool-context), atau tunda definisi alat dengan [tool search tool](/docs/id/agents-and-tools/tool-use/tool-search-tool).

Claude Opus 4.8, [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6 memiliki jendela konteks 1 juta token pada API Claude, Amazon Bedrock, dan Vertex AI. Pada Microsoft Foundry, Claude Opus 4.8 memiliki jendela konteks 200k token. Model Claude lainnya, termasuk Claude Sonnet 4.5, memiliki jendela konteks 200k token.

Claude Fable 5 dan Claude Mythos 5 (`claude-fable-5` dan `claude-mythos-5`) memiliki jendela konteks 1 juta token pada API Claude. Maksimum 1 juta juga merupakan default, dan satu permintaan dapat menghasilkan hingga 128k token output (`max_tokens`).

Satu permintaan dapat menyertakan hingga 600 gambar atau halaman PDF (100 untuk model dengan jendela konteks 200k token). Saat mengirim banyak gambar atau dokumen besar, Anda mungkin mendekati [batas ukuran permintaan](/docs/id/api/overview#request-size-limits) sebelum mencapai batas token.

## Kesadaran konteks pada Claude Sonnet 4.6, Sonnet 4.5, dan Haiku 4.5 \{#context-awareness-in-claude-sonnet-4-6-sonnet-4-5-and-haiku-4-5}

Claude Sonnet 4.6, Claude Sonnet 4.5, dan Claude Haiku 4.5 memiliki fitur **kesadaran konteks**. Kemampuan ini memungkinkan model-model tersebut melacak sisa jendela konteks mereka (yaitu, "anggaran token") sepanjang percakapan. Hal ini memungkinkan Claude untuk menjalankan tugas dan mengelola konteks secara lebih efektif dengan memahami seberapa banyak ruang yang tersedia untuk bekerja. Claude dilatih untuk menggunakan konteks ini secara presisi, bertahan dalam tugas hingga akhir alih-alih menebak berapa banyak token yang tersisa. Bagi sebuah model, tidak memiliki kesadaran konteks seperti berkompetisi dalam acara memasak tanpa jam. Model yang sadar konteks mengubah hal ini dengan secara eksplisit menerima informasi tentang sisa konteks, sehingga mereka dapat memanfaatkan token yang tersedia secara maksimal.

**Cara kerjanya:**

Di awal percakapan, Claude menerima informasi tentang total jendela konteksnya:

```xml
<budget:token_budget>1000000</budget:token_budget>
```

Anggaran diatur ke 1 juta token (200k untuk model dengan jendela konteks yang lebih kecil).

Setelah setiap panggilan alat, Claude menerima pembaruan tentang kapasitas yang tersisa:

```xml
<system_warning>Token usage: 35000/1000000; 965000 remaining</system_warning>
```

Kesadaran ini membantu Claude menentukan berapa banyak kapasitas yang tersisa untuk bekerja dan memungkinkan eksekusi yang lebih efektif pada tugas yang berjalan lama. Token gambar termasuk dalam anggaran ini.

**Manfaat:**

Kesadaran konteks sangat berharga untuk:
- Sesi agen yang berjalan lama yang memerlukan fokus berkelanjutan
- Alur kerja multi-jendela-konteks di mana transisi state penting
- Tugas kompleks yang memerlukan manajemen token yang cermat

<Tip>
Untuk agen yang mencakup beberapa sesi, rancang artefak state Anda sehingga pemulihan konteks cepat saat sesi baru dimulai. [Pola multi-sesi memory tool](/docs/id/agents-and-tools/tool-use/memory-tool#multi-session-software-development-pattern) menjelaskan pendekatan konkret. Lihat juga [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
</Tip>

Untuk panduan prompting dalam memanfaatkan kesadaran konteks, lihat [panduan praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#context-awareness-and-multi-window-workflows).

## Mengelola konteks dengan compaction \{#managing-context-with-compaction}

Jika percakapan Anda secara rutin mendekati batas jendela konteks, [server-side compaction](/docs/id/build-with-claude/compaction) adalah pendekatan yang direkomendasikan. Compaction menyediakan peringkasan sisi server yang secara otomatis memadatkan bagian awal percakapan, memungkinkan percakapan yang berjalan lama melampaui batas konteks dengan upaya integrasi minimal. Fitur ini tersedia dalam versi beta untuk Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6.

Untuk kebutuhan yang lebih khusus, [context editing](/docs/id/build-with-claude/context-editing) menawarkan strategi tambahan:
- **Pembersihan hasil alat** - Membersihkan hasil alat lama dalam alur kerja agentik
- **Pembersihan blok pemikiran** - Mengelola blok pemikiran dengan pemikiran diperpanjang

## Perilaku overflow jendela konteks \{#context-window-overflow-behavior}

Pada model Claude 4.5 dan yang lebih baru, jika token input ditambah `max_tokens` melebihi ukuran jendela konteks, API menerima permintaan tersebut. Jika pembuatan kemudian mencapai batas jendela konteks, proses berhenti dengan `stop_reason: "model_context_window_exceeded"`. Pada model sebelumnya, API mengembalikan error validasi sebagai gantinya; aktifkan perilaku `model_context_window_exceeded` dengan header beta `model-context-window-exceeded-2025-08-26`. Lihat [Menangani stop reason](/docs/id/build-with-claude/handling-stop-reasons) untuk detailnya.

Untuk tetap berada dalam batas jendela konteks, gunakan [API penghitungan token](/docs/id/build-with-claude/token-counting) untuk memperkirakan penggunaan token sebelum mengirim pesan ke Claude.

Lihat tabel [perbandingan model](/docs/id/about-claude/models/overview#latest-models-comparison) untuk daftar ukuran jendela konteks berdasarkan model.

## Langkah selanjutnya \{#next-steps}
<CardGroup cols={2}>
  <Card title="Compaction" icon="compress" href="/docs/id/build-with-claude/compaction">
    Strategi yang direkomendasikan untuk mengelola konteks dalam percakapan yang berjalan lama.
  </Card>
  <Card title="Context editing" icon="pen" href="/docs/id/build-with-claude/context-editing">
    Strategi yang lebih terperinci seperti pembersihan hasil alat dan pembersihan blok pemikiran.
  </Card>
  <Card title="Tabel perbandingan model" icon="scales" href="/docs/id/about-claude/models/overview#latest-models-comparison">
    Lihat tabel perbandingan model untuk daftar ukuran jendela konteks dan harga token input / output berdasarkan model.
  </Card>
  <Card title="Ikhtisar pemikiran diperpanjang" icon="settings" href="/docs/id/build-with-claude/extended-thinking">
    Pelajari lebih lanjut tentang cara kerja pemikiran diperpanjang dan cara mengimplementasikannya bersama fitur lain seperti penggunaan alat dan caching prompt.
  </Card>
</CardGroup>