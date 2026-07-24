---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/context-windows
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 6346a806affb006351c18f6c0d1776ddcea2bc7af23c0dee94b1c12c722b1bae
---

# Jendela konteks

Pahami cara kerja jendela konteks, bagaimana pemikiran diperpanjang dan penggunaan alat dihitung di dalamnya, dan cara mengelola konteks seiring berkembangnya percakapan.

---

Seiring berkembangnya percakapan, Anda pada akhirnya akan mendekati batas jendela konteks. Untuk percakapan yang berjalan lama dan alur kerja agentik, [compaction sisi server](/docs/id/build-with-claude/compaction) adalah strategi utama untuk manajemen konteks.

## Cara kerja jendela konteks

"Context window" (jendela konteks) mengacu pada semua teks yang dapat direferensikan oleh model bahasa saat menghasilkan respons, termasuk respons itu sendiri. Ini berbeda dari corpus data besar tempat model bahasa dilatih, dan sebaliknya mewakili "memori kerja" untuk model. Jendela konteks yang lebih besar memungkinkan model menangani prompt yang lebih kompleks dan panjang, tetapi lebih banyak konteks tidak secara otomatis lebih baik. Seiring bertambahnya jumlah token, akurasi dan recall menurun, sebuah fenomena yang dikenal sebagai *context rot*. Ini membuat kurasi apa yang ada dalam konteks sama pentingnya dengan berapa banyak ruang yang tersedia.

<Tip>
  Untuk informasi lebih lanjut tentang mengapa konteks panjang menurun dan cara merekayasa solusinya, lihat [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
</Tip>

Diagram berikut mengilustrasikan perilaku standar jendela konteks untuk permintaan API1:

![Diagram giliran yang terakumulasi dalam jendela konteks hingga percakapan mendekati batas token](/docs/images/context-window.svg)

*1Antarmuka chat seperti [claude.ai](https://claude.ai/) juga dapat mengelola jendela konteks secara bergulir dengan basis "first in, first out".*

* **Akumulasi token progresif:** Seiring percakapan berlanjut melalui giliran-giliran, setiap pesan pengguna dan respons asisten terakumulasi dalam jendela konteks, dan giliran sebelumnya dipertahankan sepenuhnya.

* **Kapasitas jendela konteks:** Jendela konteks ([hingga 1M token, tergantung pada model](#context-window-sizes-by-model)) menampung riwayat percakapan ditambah output baru yang dihasilkan Claude.

* **Alur input-output:** Setiap giliran terdiri dari:

  * **Fase input:** Berisi semua riwayat percakapan sebelumnya ditambah pesan pengguna saat ini
  * **Fase output:** Menghasilkan respons teks yang menjadi bagian dari input untuk giliran berikutnya

Semua yang ada dalam permintaan dihitung dalam jendela konteks: prompt sistem, setiap pesan dalam `messages` (termasuk hasil alat, gambar, dan dokumen), dan definisi alat Anda. Output yang dihasilkan Claude untuk giliran tersebut, termasuk pemikiran diperpanjangnya, juga dihitung. Setiap respons melaporkan apa yang dikonsumsi permintaan dalam bidang `usage`-nya. Jika Anda menggunakan [caching prompt](/docs/id/build-with-claude/prompt-caching), jumlah input dibagi menjadi `input_tokens`, `cache_read_input_tokens`, dan `cache_creation_input_tokens`, dan ketiganya dihitung dalam jendela. Untuk memperkirakan permintaan sebelum Anda mengirimnya, gunakan [API penghitungan token](/docs/id/build-with-claude/token-counting).

## Ukuran jendela konteks berdasarkan model

Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6 memiliki jendela konteks 1M token di Claude API, Amazon Bedrock, Google Cloud, dan Microsoft Foundry. [Claude Mythos Preview](https://anthropic.com/glasswing) juga memiliki jendela konteks 1M token.

Claude Fable 5 dan Claude Mythos 5 (claude-fable-5 dan claude-mythos-5) memiliki jendela konteks 1M token, dan satu permintaan ke model-model ini dapat menghasilkan hingga 128k token output (`max_tokens`). Model Claude lainnya, termasuk Claude Sonnet 4.5, memiliki jendela konteks 200k token.

Untuk setiap model dengan jendela konteks 1M token, 1M adalah default: Anda tidak memerlukan header beta, dan permintaan konteks panjang ditagih dengan [harga standar](/docs/id/about-claude/pricing#long-context-pricing).

Satu permintaan dapat mencakup hingga 600 gambar atau halaman PDF (100 untuk model dengan jendela konteks 200k token). Jika Anda mengirim banyak gambar atau dokumen besar, Anda mungkin mencapai [batas ukuran permintaan](/docs/id/api/overview#request-size-limits) sebelum batas token.

Lihat tabel [perbandingan model](/docs/id/about-claude/models/overview#latest-models-comparison) untuk daftar ukuran jendela konteks berdasarkan model.

## Jendela konteks dengan pemikiran diperpanjang

Dengan [pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking), semua token input dan output, termasuk token pemikiran, dihitung dalam batas jendela konteks, dengan beberapa nuansa dalam situasi multi-giliran.

Token anggaran pemikiran adalah bagian dari parameter `max_tokens` Anda, ditagih sebagai token output, dan dihitung dalam batas laju. Dengan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking), Claude menentukan alokasi pemikirannya secara dinamis, sehingga penggunaan token pemikiran bervariasi dari permintaan ke permintaan.

Apakah blok pemikiran dari giliran asisten sebelumnya tetap berada dalam jendela konteks tergantung pada model. Pada Claude Opus 4.5 dan model Opus yang lebih baru, Claude Sonnet 4.6 dan model Sonnet yang lebih baru, Claude Fable 5, Claude Mythos 5, dan Claude Mythos Preview, API mempertahankan blok pemikiran sebelumnya secara default, dan blok tersebut dihitung dalam jendela konteks seperti token input lainnya. Pada model Opus dan Sonnet yang lebih lama serta semua model Haiku, API secara otomatis menghapus blok pemikiran sebelumnya dari riwayat percakapan saat Anda mengirimkannya kembali, yang mempertahankan kapasitas token untuk konten percakapan. Untuk default per model, lihat [preservasi blok pemikiran berdasarkan model](/docs/id/build-with-claude/extended-thinking#thinking-block-preservation-by-model). Untuk mengganti default ke arah mana pun, gunakan [pembersihan blok pemikiran](/docs/id/build-with-claude/context-editing#thinking-block-clearing).

Diagram berikut menunjukkan bagaimana token dikelola ketika pemikiran diperpanjang diaktifkan pada model yang menghapus blok pemikiran sebelumnya:

![Diagram pemikiran diperpanjang (extended thinking) pada model yang menghapus blok pemikiran sebelumnya: blok pemikiran setiap giliran dihasilkan dalam output dan tidak dibawa ke input giliran berikutnya](/docs/images/context-window-thinking.svg)

* **Penghapusan pemikiran diperpanjang:** Pada model yang menghapus blok pemikiran sebelumnya, blok pemikiran diperpanjang (ditampilkan dalam abu-abu gelap) dihasilkan selama fase output setiap giliran tetapi tidak dibawa sebagai token input untuk giliran berikutnya. Anda tidak perlu menghapus blok pemikiran sendiri: jika Anda mengirimkannya kembali, Claude API menghapusnya secara otomatis.
* **Penagihan:** Token pemikiran diperpanjang ditagih sebagai token output satu kali, saat dihasilkan. Pada model yang mempertahankan blok pemikiran sebelumnya, blok yang dipertahankan kemudian menjadi bagian dari input permintaan berikutnya dan ditagih sebagai token input, seperti sisa riwayat percakapan.

<Note>
  Anda dapat membaca lebih lanjut tentang jendela konteks dan pemikiran diperpanjang dalam panduan [Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking).
</Note>

## Jendela konteks dengan pemikiran diperpanjang dan penggunaan alat

Diagram berikut mengilustrasikan bagaimana token dikelola ketika Anda menggabungkan pemikiran diperpanjang dengan penggunaan alat pada model yang menghapus blok pemikiran sebelumnya:

![Diagram pemikiran diperpanjang (extended thinking) dengan penggunaan alat (tool use): pemikiran dipertahankan bersama hasil alatnya, lalu dihapus pada giliran pengguna berikutnya pada model yang menghapus blok pemikiran sebelumnya](/docs/images/context-window-thinking-tools.svg)

<Steps>
  <Step title="Arsitektur giliran pertama">
    * **Komponen input:** Konfigurasi alat dan pesan pengguna
    * **Komponen output:** Pemikiran diperpanjang + respons teks + permintaan penggunaan alat
    * **Perhitungan token:** Semua komponen input dan output dihitung dalam jendela konteks, dan semua komponen output ditagih sebagai token output.
  </Step>

  <Step title="Penanganan hasil alat (giliran 2)">
    * **Komponen input:** Setiap blok dalam giliran pertama dan `tool_result`. Anda harus mengembalikan blok pemikiran diperpanjang dengan hasil alat yang sesuai. Ini adalah satu-satunya kasus di mana Anda harus mengembalikan blok pemikiran.
    * **Komponen output:** Setelah hasil alat dikirimkan kembali ke Claude, Claude merespons hanya dengan teks (tanpa pemikiran diperpanjang tambahan hingga pesan `user` berikutnya, kecuali [pemikiran bersisipan](/docs/id/build-with-claude/extended-thinking#interleaved-thinking) diaktifkan).
    * **Perhitungan token:** Semua komponen input dan output dihitung dalam jendela konteks, dan semua komponen output ditagih sebagai token output.
  </Step>

  <Step title="Giliran pengguna baru (giliran 3)">
    * **Komponen input:** Semua input dan output dari giliran sebelumnya dibawa ke depan. Blok pemikiran dari siklus penggunaan alat yang telah selesai tidak lagi harus tetap berada dalam konteks: pada model yang menghapus blok pemikiran sebelumnya, API menghapusnya secara otomatis saat Anda mengirimkannya kembali, dan pada model yang mempertahankan blok pemikiran sebelumnya, Anda dapat menghapusnya sendiri pada tahap ini. Di sinilah juga Anda menambahkan giliran `user` berikutnya.
    * **Komponen output:** Karena ada giliran `user` baru di luar siklus penggunaan alat, Claude menghasilkan blok pemikiran diperpanjang baru dan melanjutkan dari sana.
    * **Perhitungan token:** Pada model yang menghapus blok pemikiran sebelumnya, token pemikiran sebelumnya tidak lagi dihitung dalam jendela konteks. Semua blok sebelumnya lainnya masih dihitung dalam jendela konteks, begitu juga blok pemikiran dalam giliran `assistant` saat ini.
  </Step>
</Steps>

* **Pertimbangan untuk penggunaan alat dengan pemikiran diperpanjang:**

  * Saat Anda mengirimkan hasil alat, Anda harus menyertakan seluruh blok pemikiran yang tidak dimodifikasi yang menyertai permintaan alat tersebut, termasuk tanda tangannya.
  * API menggunakan tanda tangan kriptografis untuk memverifikasi keaslian blok pemikiran. Jika Anda memodifikasi blok pemikiran, API mengembalikan error.

<Note>
  Sebagian besar model Claude saat ini mendukung [pemikiran bersisipan](/docs/id/build-with-claude/extended-thinking#interleaved-thinking), yang memungkinkan Claude berpikir di antara panggilan alat, termasuk setelah menerima hasil alat. Ini otomatis pada model dengan pemikiran adaptif. Claude Opus 4.5, Claude Sonnet 4.5, dan model Claude 4 yang lebih lama memerlukan header beta `interleaved-thinking-2025-05-14`.

  Untuk informasi lebih lanjut tentang menggunakan alat dengan pemikiran diperpanjang, lihat [Pemikiran diperpanjang dengan penggunaan alat](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-tool-use).
</Note>

Untuk mengurangi konteks yang dikonsumsi oleh definisi alat itu sendiri, lihat [Kelola konteks alat](/docs/id/agents-and-tools/tool-use/manage-tool-context), atau tunda definisi alat dengan [alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool).

## Kesadaran konteks

Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, dan Claude Haiku 4.5 memiliki **kesadaran konteks:** model-model ini melacak sisa jendela konteks mereka ("anggaran token" mereka) sepanjang percakapan. Ini memungkinkan model mengelola tugas yang berjalan lama berdasarkan ruang yang tersisa alih-alih menebak berapa banyak token yang tersisa. Kesadaran konteks bersifat otomatis: tidak ada yang perlu Anda aktifkan, dan Anda tidak pernah mengirim tag yang ditampilkan di bagian ini sendiri. API yang menyuntikkannya.

### Cara kerjanya

Dalam prompt sistem setiap permintaan, API memberi Claude total jendela konteksnya:

```xml
<budget:token_budget>200000</budget:token_budget>
```

Anggaran tersebut sesuai dengan jendela konteks yang tersedia untuk permintaan Anda: 1M token untuk Claude Sonnet 5 dan Claude Sonnet 4.6, dan 200k token untuk Claude Sonnet 4.5 dan Claude Haiku 4.5. Contoh di bagian ini menunjukkan model dengan jendela konteks 200k token.

Setelah setiap panggilan alat, API memberi Claude pembaruan tentang kapasitas yang tersisa:

```xml
<system_warning>Token usage: 35000/200000; 165000 remaining</system_warning>
```

Token gambar termasuk dalam anggaran ini.

Model yang lebih baru tidak menerima tag yang disuntikkan ini. Pada Claude Opus 4.7 dan yang lebih baru, Claude Fable 5, dan Claude Mythos 5, Anda dapat memberi model anggaran eksplisit dengan [anggaran tugas](/docs/id/build-with-claude/task-budgets), yang masih dalam beta.

<Tip>
  Untuk agen yang mencakup beberapa sesi, rancang artefak state Anda sehingga pemulihan konteks cepat saat sesi baru dimulai. [Pola multisesi alat memori](/docs/id/agents-and-tools/tool-use/memory-tool#multisession-software-development-pattern) menjelaskan pendekatan konkret. Lihat juga [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
</Tip>

Untuk panduan prompting tentang menggunakan kesadaran konteks, lihat [Praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#context-awareness-and-multiwindow-workflows).

## Kelola konteks dengan compaction

Jika percakapan Anda secara teratur mendekati batas jendela konteks, gunakan [compaction sisi server](/docs/id/build-with-claude/compaction). Compaction secara otomatis merangkum bagian awal percakapan di server, sehingga percakapan dapat berlanjut melewati batas jendela konteks. Ini tersedia dalam beta untuk Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6.

Untuk kebutuhan yang lebih khusus, [pengeditan konteks](/docs/id/build-with-claude/context-editing) menawarkan strategi tambahan:

* **Pembersihan hasil alat:** Bersihkan hasil alat lama dalam alur kerja agentik
* **Pembersihan blok pemikiran:** Kelola blok pemikiran saat Anda menggunakan pemikiran diperpanjang

Prefiks prompt yang di-cache masih menempati jendela konteks: [caching prompt](/docs/id/build-with-claude/prompt-caching) mengubah apa yang Anda bayar untuk token tersebut, bukan apakah token tersebut dihitung.

## Perilaku overflow jendela konteks

Jika input saja sudah melebihi jendela konteks model, API mengembalikan 400 `invalid_request_error` ("prompt is too long") pada setiap model.

Pada model Claude 4.5 dan yang lebih baru, jika token input ditambah `max_tokens` melebihi ukuran jendela konteks, API menerima permintaan tersebut. Jika generasi kemudian mencapai batas jendela konteks, generasi berhenti dengan `stop_reason: "model_context_window_exceeded"`. Pada model yang lebih lama, API mengembalikan [error validasi](/docs/id/api/errors) sebagai gantinya. Untuk mengaktifkan perilaku `model_context_window_exceeded` pada model-model tersebut, gunakan header beta `model-context-window-exceeded-2025-08-26`. Lihat [Alasan berhenti dan fallback](/docs/id/build-with-claude/handling-stop-reasons) untuk detailnya.

Untuk tetap berada dalam batas jendela konteks, gunakan [API penghitungan token](/docs/id/build-with-claude/token-counting) untuk memperkirakan penggunaan token sebelum mengirim pesan ke Claude.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Compaction" icon="stack" href="/docs/id/build-with-claude/compaction">
    Compaction konteks sisi server untuk mengelola percakapan panjang yang mendekati batas jendela konteks.
  </Card>

  <Card title="Pengeditan konteks" icon="edit" href="/docs/id/build-with-claude/context-editing">
    Kelola konteks percakapan secara otomatis seiring pertumbuhannya dengan pengeditan konteks.
  </Card>

  <Card title="Tabel perbandingan model" icon="scales" href="/docs/id/about-claude/models/overview#latest-models-comparison">
    Lihat tabel perbandingan model untuk daftar ukuran jendela konteks dan harga token input/output berdasarkan model.
  </Card>

  <Card title="Pemikiran diperpanjang" icon="settings" href="/docs/id/build-with-claude/extended-thinking">
    Berikan Claude penalaran yang ditingkatkan untuk tugas kompleks dan kendalikan bagaimana konten pemikiran dikembalikan.
  </Card>
</CardGroup>
