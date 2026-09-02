---
source: platform
url: https://platform.claude.com/docs/id/models/opus-5/migration-guide
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: eb9de92175fd122fd87eca12f372622c63a800f7b7a8135c096cfc06a4914b00
---

---
title: Migrasi ke Claude Opus 5
url: https://platform.claude.com/docs/id/models/opus-5/migration-guide
description: "Migrasi ke Claude Opus 5 dari model Claude sebelumnya: ID model, perubahan yang merusak kompatibilitas, perubahan yang direkomendasikan, dan daftar periksa migrasi."
---

<Note>
  Panduan ini membahas migrasi kode [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak ada perubahan yang diperlukan selain memperbarui nama model.
</Note>

<Tip>
  **Otomatiskan migrasi Anda dengan skill Claude API.** Di Claude Code, jalankan `/claude-api migrate` untuk memanggil [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model) bawaan. Skill ini berfungsi untuk model Claude terkini mana pun sebagai target:

  ```text wrap
  /claude-api migrate this project to claude-opus-5
  ```

  Skill ini menerapkan penggantian ID model dan, sesuai kebutuhan, perubahan parameter yang bersifat breaking, penggantian prefill, serta kalibrasi effort untuk model target Anda di seluruh basis kode Anda, lalu menghasilkan daftar periksa berisi item yang perlu diverifikasi secara manual. Skill ini meminta Anda mengonfirmasi cakupan migrasi (seluruh direktori kerja, sebuah subdirektori, atau daftar file tertentu) sebelum mengedit file apa pun. Skill ini juga mendeteksi klien Amazon Bedrock dan Claude Platform on AWS serta menyesuaikan format ID model dan perubahan fitur untuk platform tersebut.
</Tip>

Claude Opus 5 adalah peningkatan besar dibandingkan Claude Opus 4.8, unggul dalam penalaran mendalam, tugas agentik dan berjangka panjang, serta penskalaan komputasi saat pengujian (test-time compute scaling). Untuk perbedaan perilaku dan pola prompting khusus model, lihat [Prompting Claude Opus 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5).

Claude Opus 5 adalah peningkatan langsung (drop-in) untuk Claude Opus 4.8 dengan harga yang sama, yaitu $5 USD per juta token input dan $25 USD per juta token output; lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing). Ada dua perubahan yang merusak kompatibilitas untuk kode yang sudah berjalan di Claude Opus 4.8, yang dibahas di bagian [Perubahan yang merusak kompatibilitas](https://platform.claude.com/docs/id/models/opus-5/migration-guide#breaking-changes). Claude Opus 5 mendukung rangkaian fitur yang sama dengan Claude Opus 4.8, termasuk ["context window" (jendela konteks) 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) (default, tanpa header beta), [128k token output maksimum](https://platform.claude.com/docs/id/models/overview), [adaptive thinking (pemikiran adaptif)](https://platform.claude.com/docs/id/build-with-claude/thinking), ["prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching), [pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing), [Files API](https://platform.claude.com/docs/id/build-with-claude/files), [dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support), [vision](https://platform.claude.com/docs/id/build-with-claude/vision), serta [alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien, dengan dua pengecualian: [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) tidak tersedia di Claude Opus 5, dan [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) tidak didukung di Claude Opus 5. Lihat setiap halaman alat untuk ketersediaan model.

## Migrasi ke Claude Opus 5 dari Claude Opus 4.8

<Note>
  Bagian ini hanya mencakup perbedaan dari Claude Opus 4.8. Jika kode Anda menggunakan Claude Opus 4.7 atau yang lebih lama, gunakan bagian berikut sebagai gantinya: [Migrasi ke Claude Opus 5 dari Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-5/migration-guide#migrating-from-claude-opus-47) atau [Migrasi ke Claude Opus 5 dari Claude Opus 4.6 dan model Opus sebelumnya](https://platform.claude.com/docs/id/models/opus-5/migration-guide#migrating-from-claude-opus-46). Bagian-bagian tersebut mencakup perbedaan ini ditambah perubahan yang merusak kompatibilitas dari model sebelumnya (parameter sampling ditolak, "extended thinking" (pemikiran diperpanjang) manual ditolak, prefill dihapus, tokenizer baru).
</Note>

### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-8"  # Before
model = "claude-opus-5"  # After
```

`claude-opus-5` adalah ID model tetap tanpa akhiran tanggal, skema yang sama dengan `claude-opus-4-8` dan `claude-sonnet-5`.

### Perubahan yang merusak kompatibilitas

1. **Thinking aktif secara default:** Di Claude Opus 4.8, permintaan tanpa field `thinking` berjalan tanpa thinking; di Claude Opus 5, permintaan yang sama berjalan dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking). `max_tokens` tetap menjadi batas keras pada total output, yaitu thinking ditambah teks respons, jadi tinjau kembali nilainya untuk beban kerja yang berjalan tanpa thinking di Claude Opus 4.8. Token thinking ditagih sebagai token output bahkan ketika teks thinking tidak dikembalikan kepada Anda, sehingga meskipun harga per token tidak berubah, beban kerja yang berjalan tanpa thinking di Claude Opus 4.8 dapat menghasilkan lebih banyak token output per permintaan di Claude Opus 5; lihat [Kontrol biaya](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#cost-control). Untuk mempertahankan perilaku lama, kirimkan `thinking: {type: "disabled"}`, dengan tunduk pada batas effort di butir berikutnya; perhatikan bahwa dengan thinking dinonaktifkan, model terkadang dapat mengeluarkan panggilan alat sebagai teks biasa atau menyertakan tag XML internal dalam output yang terlihat, jadi utamakan tingkat effort yang lebih rendah dengan thinking diaktifkan jika memungkinkan, dan lihat [Menjalankan dengan thinking dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk mitigasi jika tidak memungkinkan.

   Bentuk respons juga berubah bersamanya. Dengan thinking aktif, respons dapat dimulai dengan satu atau lebih blok `thinking` sebelum blok `text` pertama, dan karena `thinking.display` secara default bernilai `"omitted"` di Claude Opus 5, blok-blok tersebut tiba dengan field `thinking` kosong di samping `signature`-nya. Kode yang membaca balasan berdasarkan posisi, seperti `content[0].text` atau handler stream yang memperlakukan event `content_block_start` pertama sebagai teks, akan rusak pada respons ini. Sebagai gantinya, pilih blok konten berdasarkan field `type`-nya: baca `text` dari blok yang `type`-nya adalah `"text"`, dan lakukan percabangan berdasarkan tipe blok saat menangani event stream. Untuk menerima ringkasan thinking yang dapat dibaca alih-alih field `thinking` kosong, atur `display: "summarized"`; lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).

   Jika Anda menjalankan loop "tool use" (penggunaan alat), kirimkan kembali blok `thinking` dari setiap respons asisten ke API secara lengkap dan tanpa modifikasi saat Anda mengembalikan hasil alat, termasuk blok yang field `thinking`-nya kosong. Kembalikan pesan asisten sebagaimana diterima alih-alih memfilter blok kontennya berdasarkan tipe atau membangunnya ulang: API menolak blok thinking yang diedit, diurutkan ulang, atau dihapus sebagian dengan error 400. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).

2. **Menonaktifkan thinking dibatasi pada effort `high`:** Anda masih dapat menonaktifkan thinking dengan `thinking: {type: "disabled"}`, tetapi hanya pada tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah. Permintaan yang menggabungkan `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400. Claude Opus 4.8 menerima kombinasi ini, jadi audit permintaan yang menonaktifkan thinking sebelum Anda bermigrasi.

   Pemeriksaan ini diberlakukan pada setiap permintaan: konfigurasi effort dan thinking setiap permintaan divalidasi secara independen, sehingga permintaan yang menaikkan effort ke `xhigh` atau `max` saat thinking dinonaktifkan akan ditolak meskipun permintaan sebelumnya dalam percakapan diterima.

   Sebelum (diterima di Claude Opus 4.8, ditolak di Claude Opus 5):

   ```python
   client.messages.create(
       model="claude-opus-4-8",
       max_tokens=16000,
       thinking={"type": "disabled"},
       output_config={"effort": "xhigh"},
       messages=[{"role": "user", "content": "..."}],
   )
   ```

   Sesudah (Claude Opus 5), hapus field `thinking` untuk mengaktifkan kembali thinking:

   ```python
   client.messages.create(
       model="claude-opus-5",
       max_tokens=16000,
       output_config={"effort": "xhigh"},  # thinking is on by default
       messages=[{"role": "user", "content": "..."}],
   )
   ```

   atau biarkan thinking tetap dinonaktifkan dan turunkan effort:

   ```python
   client.messages.create(
       model="claude-opus-5",
       max_tokens=16000,
       thinking={"type": "disabled"},
       output_config={"effort": "high"},  # or "medium", "low"
       messages=[{"role": "user", "content": "..."}],
   )
   ```

### Perubahan yang direkomendasikan

Perubahan ini tidak wajib tetapi akan meningkatkan pengalaman Anda:

1. **Uji effort `max` untuk pekerjaan yang kritis terhadap kapabilitas:** Claude Opus 5 mendukung rangkaian lengkap [tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort) (`low`, `medium`, `high`, `xhigh`, `max`). Jika kapabilitas maksimum lebih penting daripada pengeluaran token, uji effort `max`. Ini dapat memberikan peningkatan pada tugas yang paling menuntut tetapi mungkin menunjukkan hasil yang semakin berkurang dari peningkatan penggunaan token dan dapat cenderung berpikir berlebihan pada tugas yang lebih sederhana. Jika Anda menjalankan pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak; mulai dari 64k token dan sesuaikan dari sana.

2. **Pertimbangkan fallback otomatis:** Claude Opus 5 dirilis dengan pengklasifikasi keamanan siber yang penolakan kategori sibernya dapat melakukan fallback ke Claude Opus 4.8. Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, pertimbangkan parameter `fallbacks` dengan mode `"default"` (`fallbacks: "default"`), yang memilih model fallback yang direkomendasikan berdasarkan kategori penolakan alih-alih daftar model yang dikelola secara manual. Fallback sisi server masih dalam beta; mode `"default"` memerlukan header beta `server-side-fallback-2026-07-01`. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

3. **Cache prompt yang lebih pendek:** Panjang prompt minimum yang dapat di-cache di Claude Opus 5 adalah 512 token, turun dari 1.024 token di Claude Opus 4.8. Prompt yang terlalu pendek untuk di-cache di Claude Opus 4.8 kini dapat membuat entri cache, tanpa perlu perubahan kode. Lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

4. **Ubah alat di tengah percakapan (beta):** Anda dapat menambah atau menghapus alat di antara giliran percakapan tanpa membatalkan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya. Kirim header beta `mid-conversation-tool-changes-2026-07-01`. Ini berguna untuk beban kerja agentik yang mengekspos alat secara bertahap atau menghentikannya seiring kemajuan tugas; tanpanya, daftar alat yang berubah akan membatalkan prefiks yang di-cache.

5. **Sesuaikan ulang prompt panjang dan verbositas:** Respons terlihat default dan hasil tertulis berjalan lebih panjang di Claude Opus 5 daripada di Claude Opus 4.8, dan menurunkan effort mengurangi volume thinking tanpa secara andal memperpendek respons yang terlihat. Sebagai gantinya, berikan prompt secara eksplisit untuk keringkasan atau panjang target. Lihat [Panjang respons dan verbositas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity) dan [Panjang hasil tertulis](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#written-deliverable-length).

6. **Hapus instruksi verifikasi yang terbawa dan batasi cakupan:** Claude Opus 5 memverifikasi pekerjaannya sendiri tanpa perlu diperintahkan, jadi hapus instruksi verifikasi atau pemeriksaan mandiri eksplisit yang terbawa dari prompt yang disetel untuk model sebelumnya; membiarkannya akan menyebabkan verifikasi berlebihan. Untuk tugas yang sempit, batasi cakupan tugas secara eksplisit. Dalam framework multi-agen, berikan panduan eksplisit tentang skenario mana yang memerlukan delegasi atau batasi jumlah subagen, karena Claude Opus 5 lebih mudah mendelegasikan daripada model sebelumnya. Lihat [Cakupan tugas dan verifikasi berlebihan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#task-scope-and-over-verification) dan [Mengontrol pembuatan subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning).

### Daftar periksa migrasi

* Perbarui nama model dari `claude-opus-4-8` ke `claude-opus-5`.
* Tinjau beban kerja yang berjalan tanpa field `thinking`: beban kerja tersebut berjalan dengan thinking di Claude Opus 5. Tinjau kembali `max_tokens`, yang tetap menjadi batas keras pada total output (thinking ditambah teks respons), atau kirimkan `thinking: {type: "disabled"}` pada effort `high` atau lebih rendah untuk mempertahankan perilaku lama. Jika Anda menonaktifkan thinking, tinjau [Menjalankan dengan thinking dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk artefak output yang dapat muncul dan mitigasi prompting-nya.
* Perbarui parsing respons yang membaca konten berdasarkan posisi, seperti `content[0].text` atau handler stream yang mengasumsikan blok konten pertama adalah teks: dengan thinking aktif, blok `thinking` tiba sebelum blok `text`. Sebagai gantinya, pilih blok konten berdasarkan `type`.
* Jika Anda menjalankan loop penggunaan alat, kirimkan kembali blok `thinking` secara lengkap dan tanpa modifikasi saat Anda mengembalikan hasil alat; blok yang dimodifikasi mengembalikan error 400. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).
* Verifikasi bahwa kode apa pun yang mem-parsing field `thinking` memperlakukannya hanya sebagai teks tampilan. `thinking.display` secara default bernilai `"omitted"` di Claude Opus 5, sama seperti di Claude Opus 4.8, sehingga blok thinking tiba dengan field `thinking` kosong; atur `display: "summarized"` untuk menerima ringkasan yang dapat dibaca. Lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).
* Audit permintaan yang menonaktifkan thinking: `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400, diberlakukan pada setiap permintaan. Aktifkan kembali thinking atau turunkan effort ke `high` atau lebih rendah.
* Evaluasi ulang pengaturan `effort` Anda: jalankan sweep [effort](https://platform.claude.com/docs/id/build-with-claude/effort) baru pada eval Anda sendiri alih-alih membawa pengaturan yang disetel untuk model sebelumnya. Effort `low` dan `medium` layak diuji sebagai kontrol biaya dan latensi, dan uji effort `max` jika kapabilitas maksimum lebih penting daripada pengeluaran token. Jika Anda menjalankan pada effort `xhigh` atau `max`, naikkan `max_tokens` ke setidaknya 64k sebagai titik awal.
* Tinjau prompt yang mendekati minimum caching: prompt dengan 512 token atau lebih kini dapat membuat entri cache, turun dari 1.024 token di Claude Opus 4.8.
* Tangani `stop_reason: "refusal"`, dan pertimbangkan `fallbacks: "default"` (beta) untuk menjalankan ulang permintaan yang ditolak pada model fallback yang direkomendasikan secara otomatis.
* Jika organisasi Anda memiliki komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models), rencanakan kapasitas secara terpisah: Priority Tier tidak didukung di Claude Opus 5, sementara Claude Opus 4.8 tetap mendukungnya.
* Untuk beban kerja agentik, pertimbangkan [anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) (beta) dan perubahan alat di tengah percakapan (beta).
* Sesuaikan ulang prompt panjang dan verbositas: respons terlihat default dan hasil tertulis berjalan lebih panjang di Claude Opus 5, dan menurunkan effort mengurangi volume thinking tanpa secara andal memperpendek respons yang terlihat. Berikan prompt secara eksplisit untuk keringkasan atau panjang target. Lihat [Panjang respons dan verbositas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity) dan [Panjang hasil tertulis](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#written-deliverable-length).
* Hapus instruksi verifikasi dan pemeriksaan mandiri yang terbawa dari prompt yang disetel untuk model sebelumnya (instruksi tersebut menyebabkan verifikasi berlebihan di Claude Opus 5), batasi cakupan tugas secara eksplisit untuk tugas yang sempit, dan dalam framework multi-agen arahkan atau batasi delegasi subagen. Lihat [Cakupan tugas dan verifikasi berlebihan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#task-scope-and-over-verification) dan [Mengontrol pembuatan subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning).
* Tetapkan ulang baseline biaya dan latensi pada beban kerja Anda sendiri. Harga per token tidak berubah dari Claude Opus 4.8, tetapi token thinking ditagih sebagai token output, sehingga beban kerja yang berjalan tanpa thinking dapat menghasilkan lebih banyak token output per permintaan.

## Migrasi ke Claude Opus 5 dari Claude Opus 4.7

Claude Opus 5 seharusnya memiliki performa langsung pakai yang kuat pada prompt dan eval Claude Opus 4.7 yang sudah ada, dengan harga yang sama yaitu $5 USD per juta token input dan $25 USD per juta token output. Model ini mendukung rangkaian fitur yang sama dengan Claude Opus 4.7, termasuk [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows), [128k token output maksimum](https://platform.claude.com/docs/id/models/overview), [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking), [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching), [pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing), [Files API](https://platform.claude.com/docs/id/build-with-claude/files), [dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support), [vision](https://platform.claude.com/docs/id/build-with-claude/vision), serta [alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien, dengan dua pengecualian: [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) tidak tersedia di Claude Opus 5, dan [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) tidak didukung di Claude Opus 5. Model ini juga menambahkan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) dan mendokumentasikan secara publik [detail penghentian penolakan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response). Di Claude API dan Google Cloud, Claude Opus 5 juga mendukung [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) sebagai toolset stabil `computer_toolset_20260801` dan [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) untuk tugas di dalam halaman web, yang keduanya tidak didukung oleh Claude Opus 4.7; integrasi yang sudah ada pada versi `computer_20251124` sebelumnya tetap berfungsi tanpa perubahan di kedua model. Untuk meningkatkan integrasi yang sudah ada, lihat [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124).

<Note>
  Jika kode Anda menggunakan Claude Opus 4.6 atau yang lebih lama, gunakan [Migrasi ke Claude Opus 5 dari Claude Opus 4.6 dan model Opus sebelumnya](https://platform.claude.com/docs/id/models/opus-5/migration-guide#migrating-from-claude-opus-46) sebagai gantinya. Bagian tersebut mencakup perubahan yang merusak kompatibilitas (parameter sampling ditolak, pemikiran diperpanjang manual ditolak, tokenizer baru) yang tidak dicakup oleh peningkatan dari Claude Opus 4.7 saja.
</Note>

### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-7"  # Before
model = "claude-opus-5"  # After
```

### Perubahan yang merusak kompatibilitas

1. **Thinking aktif secara default:** Di Claude Opus 4.7, permintaan tanpa field `thinking` berjalan tanpa thinking; di Claude Opus 5, permintaan yang sama berjalan dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking). `max_tokens` tetap menjadi batas keras pada total output, yaitu thinking ditambah teks respons, jadi tinjau kembali nilainya untuk beban kerja yang berjalan tanpa thinking di Claude Opus 4.7. Token thinking ditagih sebagai token output bahkan ketika teks thinking tidak dikembalikan kepada Anda, sehingga meskipun harga per token tidak berubah, beban kerja yang berjalan tanpa thinking di Claude Opus 4.7 dapat menghasilkan lebih banyak token output per permintaan di Claude Opus 5; lihat [Kontrol biaya](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#cost-control). Untuk mempertahankan perilaku lama, kirimkan `thinking: {type: "disabled"}`, dengan tunduk pada batas effort di butir berikutnya; perhatikan bahwa dengan thinking dinonaktifkan, model terkadang dapat mengeluarkan panggilan alat sebagai teks biasa atau menyertakan tag XML internal dalam output yang terlihat, jadi utamakan tingkat effort yang lebih rendah dengan thinking diaktifkan jika memungkinkan, dan lihat [Menjalankan dengan thinking dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk mitigasi jika tidak memungkinkan.

   Bentuk respons juga berubah bersamanya. Dengan thinking aktif, respons dapat dimulai dengan satu atau lebih blok `thinking` sebelum blok `text` pertama, dan karena `thinking.display` secara default bernilai `"omitted"` di Claude Opus 5, blok-blok tersebut tiba dengan field `thinking` kosong di samping `signature`-nya. Kode yang membaca balasan berdasarkan posisi, seperti `content[0].text` atau handler stream yang memperlakukan event `content_block_start` pertama sebagai teks, akan rusak pada respons ini. Sebagai gantinya, pilih blok konten berdasarkan field `type`-nya: baca `text` dari blok yang `type`-nya adalah `"text"`, dan lakukan percabangan berdasarkan tipe blok saat menangani event stream. Untuk menerima ringkasan thinking yang dapat dibaca alih-alih field `thinking` kosong, atur `display: "summarized"`; lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).

   Jika Anda menjalankan loop penggunaan alat, kirimkan kembali blok `thinking` dari setiap respons asisten ke API secara lengkap dan tanpa modifikasi saat Anda mengembalikan hasil alat, termasuk blok yang field `thinking`-nya kosong. Kembalikan pesan asisten sebagaimana diterima alih-alih memfilter blok kontennya berdasarkan tipe atau membangunnya ulang: API menolak blok thinking yang diedit, diurutkan ulang, atau dihapus sebagian dengan error 400. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).

2. **Menonaktifkan thinking dibatasi pada effort `high`:** Anda dapat menonaktifkan thinking dengan `thinking: {type: "disabled"}`, tetapi hanya pada tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah. Permintaan yang menggabungkan `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400. Claude Opus 4.7 menerima kombinasi ini, jadi audit permintaan yang menonaktifkan thinking sebelum Anda bermigrasi.

   Pemeriksaan ini diberlakukan pada setiap permintaan: konfigurasi effort dan thinking setiap permintaan divalidasi secara independen, sehingga permintaan yang menaikkan effort ke `xhigh` atau `max` saat thinking dinonaktifkan akan ditolak meskipun permintaan sebelumnya dalam percakapan diterima.

   Sebelum (diterima di Claude Opus 4.7, ditolak di Claude Opus 5):

   ```python
   client.messages.create(
       model="claude-opus-4-7",
       max_tokens=16000,
       thinking={"type": "disabled"},
       output_config={"effort": "xhigh"},
       messages=[{"role": "user", "content": "..."}],
   )
   ```

   Sesudah (Claude Opus 5), hapus field `thinking` untuk berjalan dengan thinking:

   ```python
   client.messages.create(
       model="claude-opus-5",
       max_tokens=16000,
       output_config={"effort": "xhigh"},  # thinking is on by default
       messages=[{"role": "user", "content": "..."}],
   )
   ```

   atau biarkan thinking tetap dinonaktifkan dan turunkan effort:

   ```python
   client.messages.create(
       model="claude-opus-5",
       max_tokens=16000,
       thinking={"type": "disabled"},
       output_config={"effort": "high"},  # or "medium", "low"
       messages=[{"role": "user", "content": "..."}],
   )
   ```

### Apa yang berubah

Butir-butir berikut bukan perubahan yang merusak kompatibilitas; butir-butir ini menjelaskan perbedaan perilaku yang layak diperiksa setelah Anda mengganti ID model.

1. **Parameter sampling (tidak berubah):** Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default mengembalikan error 400 di Claude Opus 5, sama seperti di Claude Opus 4.7. Sebagian besar SDK masih mendefinisikan field ini untuk kompatibilitas dengan model sebelumnya, sehingga kode yang mengaturnya lolos pemeriksaan tipe meskipun API menolak permintaan tersebut. Python SDK (v1.0 dan yang lebih baru) tidak mendefinisikannya, dan mengirimkannya akan memunculkan `TypeError`. Jika Anda telah menghapus parameter ini saat bermigrasi ke Opus 4.7, tidak diperlukan perubahan lebih lanjut.

2. **Default effort adalah `high`:** Default [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) di Claude Opus 5 adalah `high` di Claude API dan Claude Code. Jika Anda sudah mengatur effort secara eksplisit, pengaturan Anda tidak berubah.

3. **Tingkat effort dikalibrasi ulang:** Alokasi token di balik setiap tingkat effort berubah di Claude Opus 5 dibandingkan dengan Claude Opus 4.7, dan Claude Opus 5 mendukung rangkaian lengkap tingkat effort (`low`, `medium`, `high`, `xhigh`, `max`). Jalankan sweep effort baru pada eval Anda sendiri alih-alih membawa pengaturan yang disetel untuk Claude Opus 4.7. Effort `low` dan `medium` layak diuji sebagai kontrol biaya dan latensi, dan uji effort `max` jika kapabilitas maksimum lebih penting daripada pengeluaran token. Jika Anda menjalankan pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak; mulai dari 64k token dan sesuaikan dari sana. Lihat [Effort](https://platform.claude.com/docs/id/build-with-claude/effort).

4. **Jendela konteks 1 juta adalah default:** Claude Opus 5 menyajikan [jendela konteks](https://platform.claude.com/docs/id/build-with-claude/context-windows) penuh 1 juta token secara default tanpa header beta dan tanpa premi konteks panjang. Jika klien Anda mengirimkan header beta jendela konteks untuk kompatibilitas dengan model lama, Anda dapat menghapusnya di Claude Opus 5.

5. **Pesan sistem di tengah percakapan:** Claude Opus 5 menerima pesan `role: "system"` tepat setelah giliran pengguna dalam array `messages` (tunduk pada [aturan penempatan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)). Gunakan field `system` tingkat atas untuk instruksi yang berlaku sejak awal. Claude Opus 4.7 menolak `role: "system"` dalam `messages` dengan error 400. Jika Anda memelihara jalur kode yang membangun ulang seluruh riwayat pesan untuk memperbarui instruksi, Anda dapat menyederhanakannya dan mempertahankan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya.

6. **Detail penghentian penolakan:** Objek `stop_details` pada respons penolakan (tersedia sejak Claude Opus 4.7) kini didokumentasikan secara publik. Ketika model menolak permintaan, objek ini mengidentifikasi kategori penolakan, selain stop reason `refusal` yang sudah ada. Tidak diperlukan header beta, dan tidak ada opsi untuk menonaktifkannya. Lihat [Menangani stop reason](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons).

7. **Minimum caching prompt lebih rendah:** Panjang prompt minimum yang dapat di-cache di Claude Opus 5 adalah 512 token, lebih rendah daripada di Claude Opus 4.7. Prompt yang terlalu pendek untuk di-cache di Claude Opus 4.7 kini dapat membuat entri cache, tanpa perlu perubahan kode. Lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

8. **Fast mode:** Claude Opus 5 mendukung [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (pratinjau riset); fast mode tidak tersedia di Claude Opus 4.7, di mana permintaan dengan `speed: "fast"` mengembalikan error. Parameter `speed: "fast"` dan header beta `fast-mode-2026-02-01` berfungsi tanpa perubahan di Claude Opus 5.

### Perubahan yang direkomendasikan

Perubahan ini tidak wajib tetapi akan meningkatkan pengalaman Anda:

1. **Pertimbangkan fallback otomatis:** Claude Opus 5 dirilis dengan pengklasifikasi keamanan siber yang penolakan kategori sibernya dapat melakukan fallback ke Claude Opus 4.8. Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, pertimbangkan parameter `fallbacks` dengan mode `"default"` (`fallbacks: "default"`), yang memilih model fallback yang direkomendasikan berdasarkan kategori penolakan alih-alih daftar model yang dikelola secara manual. Fallback sisi server masih dalam beta; mode `"default"` memerlukan header beta `server-side-fallback-2026-07-01`. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

2. **Ubah alat di tengah percakapan (beta):** Anda dapat menambah atau menghapus alat di antara giliran percakapan tanpa membatalkan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya. Kirim header beta `mid-conversation-tool-changes-2026-07-01`. Ini berguna untuk beban kerja agentik yang mengekspos alat secara bertahap atau menghentikannya seiring kemajuan tugas; tanpanya, daftar alat yang berubah akan membatalkan prefiks yang di-cache.

3. **Sesuaikan ulang prompt panjang dan verbositas:** Respons terlihat default dan hasil tertulis berjalan lebih panjang di Claude Opus 5 daripada di model Opus sebelumnya, dan menurunkan effort mengurangi volume thinking tanpa secara andal memperpendek respons yang terlihat. Sebagai gantinya, berikan prompt secara eksplisit untuk keringkasan atau panjang target. Lihat [Panjang respons dan verbositas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity) dan [Panjang hasil tertulis](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#written-deliverable-length).

4. **Hapus instruksi verifikasi yang terbawa dan batasi cakupan:** Claude Opus 5 memverifikasi pekerjaannya sendiri tanpa perlu diperintahkan, jadi hapus instruksi verifikasi atau pemeriksaan mandiri eksplisit yang terbawa dari prompt yang disetel untuk model sebelumnya; membiarkannya akan menyebabkan verifikasi berlebihan. Untuk tugas yang sempit, batasi cakupan tugas secara eksplisit. Dalam framework multi-agen, berikan panduan eksplisit tentang skenario mana yang memerlukan delegasi atau batasi jumlah subagen, karena Claude Opus 5 lebih mudah mendelegasikan daripada model sebelumnya. Lihat [Cakupan tugas dan verifikasi berlebihan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#task-scope-and-over-verification) dan [Mengontrol pembuatan subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning).

### Daftar periksa migrasi

* Perbarui nama model dari `claude-opus-4-7` ke `claude-opus-5` (atau perbarui alias).
* Tinjau beban kerja yang berjalan tanpa field `thinking`: beban kerja tersebut berjalan dengan thinking di Claude Opus 5. Tinjau kembali `max_tokens`, yang tetap menjadi batas keras pada total output (thinking ditambah teks respons), atau kirimkan `thinking: {type: "disabled"}` pada effort `high` atau lebih rendah untuk mempertahankan perilaku lama. Jika Anda menonaktifkan thinking, tinjau [Menjalankan dengan thinking dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk artefak output yang dapat muncul dan mitigasi prompting-nya.
* Perbarui parsing respons yang membaca konten berdasarkan posisi, seperti `content[0].text` atau handler stream yang mengasumsikan blok konten pertama adalah teks: dengan thinking aktif, blok `thinking` tiba sebelum blok `text`. Sebagai gantinya, pilih blok konten berdasarkan `type`.
* Jika Anda menjalankan loop penggunaan alat, kirimkan kembali blok `thinking` secara lengkap dan tanpa modifikasi saat Anda mengembalikan hasil alat; blok yang dimodifikasi mengembalikan error 400. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).
* Verifikasi bahwa kode apa pun yang mem-parsing field `thinking` memperlakukannya hanya sebagai teks tampilan. `thinking.display` secara default bernilai `"omitted"` di Claude Opus 5, sama seperti di Claude Opus 4.7, sehingga blok thinking tiba dengan field `thinking` kosong; atur `display: "summarized"` untuk menerima ringkasan yang dapat dibaca. Lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).
* Audit permintaan yang menonaktifkan thinking: `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400, diberlakukan pada setiap permintaan. Aktifkan kembali thinking atau turunkan effort ke `high` atau lebih rendah.
* Jika Anda telah menghapus parameter sampling selama migrasi Opus 4.7, tidak diperlukan tindakan. Jika Anda menambahkannya kembali dengan jalur retry 400, hapus jalur retry tersebut.
* Evaluasi ulang pengaturan `effort` Anda: jalankan sweep [effort](https://platform.claude.com/docs/id/build-with-claude/effort) baru pada eval Anda sendiri alih-alih membawa pengaturan yang disetel untuk Claude Opus 4.7. Uji effort `low` dan `medium` sebagai kontrol biaya dan latensi, dan effort `max` jika kapabilitas maksimum lebih penting daripada pengeluaran token. Jika Anda menjalankan pada effort `xhigh` atau `max`, naikkan `max_tokens` ke setidaknya 64k sebagai titik awal.
* Hapus header beta jendela konteks apa pun. Jendela konteks 1 juta adalah default di Claude API, Amazon Bedrock, Google Cloud, dan Microsoft Foundry.
* Jika Anda membangun ulang riwayat percakapan untuk memperbarui instruksi, pertimbangkan untuk beralih ke pesan sistem di tengah percakapan untuk mempertahankan hit cache prompt.
* Verifikasi bahwa penanganan stop reason Anda membaca `stop_details` pada penolakan (tersedia sejak Claude Opus 4.7; kini didokumentasikan secara publik), dan pertimbangkan `fallbacks: "default"` (beta) untuk menjalankan ulang permintaan yang ditolak pada model fallback yang direkomendasikan secara otomatis.
* Tinjau prompt yang mendekati minimum caching: prompt dengan 512 token atau lebih kini dapat membuat entri cache.
* Jika Anda menggunakan [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool), rencanakan alternatif: fitur ini tidak tersedia di Claude Opus 5.
* Jika organisasi Anda memiliki komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models), perhatikan bahwa Priority Tier tidak didukung di Claude Opus 5.
* Jika Anda menggunakan fast mode di Claude Opus 4.7, tidak diperlukan perubahan permintaan selain ID model: `speed: "fast"` dan header beta `fast-mode-2026-02-01` berfungsi tanpa perubahan di Claude Opus 5.
* Untuk beban kerja agentik, pertimbangkan [anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) (beta) dan perubahan alat di tengah percakapan (beta).
* Sesuaikan ulang prompt panjang dan verbositas, dan hapus instruksi verifikasi dan pemeriksaan mandiri yang terbawa dari prompt yang disetel untuk model sebelumnya.
* Tetapkan ulang baseline biaya dan latensi pada tingkat effort pilihan Anda. Harga per token tidak berubah dari Claude Opus 4.7, tetapi token thinking ditagih sebagai token output, sehingga beban kerja yang berjalan tanpa thinking dapat menghasilkan lebih banyak token output per permintaan.

## Migrasi ke Claude Opus 5 dari Claude Opus 4.6 dan model Opus sebelumnya

Claude Opus 5 seharusnya memiliki performa langsung pakai yang kuat pada prompt dan eval Claude Opus 4.6 yang sudah ada dengan harga yang sama, tetapi ada beberapa perubahan perilaku dan API yang perlu diketahui saat Anda bermigrasi. Sebagian besar perubahan ini mulai berlaku di Claude Opus 4.7; dua lagi, yaitu thinking aktif secara default dan batas effort untuk menonaktifkan thinking, mulai berlaku di Claude Opus 5. Semuanya dibahas di bagian ini, sehingga bagian ini lengkap untuk kode yang datang langsung dari Claude Opus 4.6. Claude Opus 5 mendukung rangkaian fitur yang sama dengan Claude Opus 4.6, termasuk:

* [Jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) dengan harga API standar tanpa premi konteks panjang
* [128k token output maksimum](https://platform.claude.com/docs/id/models/overview)
* [Adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)
* [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)
* [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing)
* [Files API](https://platform.claude.com/docs/id/build-with-claude/files)
* [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support)
* [Vision](https://platform.claude.com/docs/id/build-with-claude/vision)
* [Alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien ([bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool), [eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool), [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool), [editor teks](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool), [pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool), [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector), [memori](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool))

Dua pengecualian: [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) tidak tersedia di Claude Opus 5, dan [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) tidak didukung di Claude Opus 5. Di Claude API dan Google Cloud, Claude Opus 5 juga mendukung [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) sebagai toolset stabil `computer_toolset_20260801` dan [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) untuk tugas di dalam halaman web, yang keduanya tidak didukung oleh Claude Opus 4.6 atau model Opus sebelumnya; integrasi yang sudah ada pada versi `computer_20251124` sebelumnya tetap berfungsi tanpa perubahan di Claude Opus 5. Untuk meningkatkan integrasi yang sudah ada, lihat [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124).

### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-6"  # Before
model = "claude-opus-5"  # After
```

### Perubahan yang merusak kompatibilitas

1. **Extended thinking dihapus:** `thinking: {type: "enabled", budget_tokens: N}` tidak lagi didukung pada Claude Opus 4.7 atau model yang lebih baru dan mengembalikan error 400. Beralihlah ke [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) (`thinking: {type: "adaptive"}`) dan gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran. Pada Claude Opus 5, pemikiran adaptif **aktif secara default**: `thinking: {type: "adaptive"}` valid dan setara dengan menghilangkan field `thinking` sepenuhnya (lihat butir berikutnya).

   Sebelum (Claude Opus 4.6):

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -H "content-type: application/json" \
       -d '{
         "model": "claude-opus-4-6",
         "max_tokens": 16000,
         "thinking": {
           "type": "enabled",
           "budget_tokens": 10000
         },
         "messages": [
           {
             "role": "user",
             "content": "..."
           }
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-opus-4-6
     max_tokens: 16000
     thinking:
       type: enabled
       budget_tokens: 10000
     messages:
       - role: user
         content: "..."
     YAML
     ```

     ```python Python
     client.messages.create(
         model="claude-opus-4-6",
         max_tokens=16000,
         thinking={"type": "enabled", "budget_tokens": 10000},
         messages=[{"role": "user", "content": "..."}],
     )
     ```

     ```typescript TypeScript
     await client.messages.create({
       model: "claude-opus-4-6",
       max_tokens: 16000,
       thinking: { type: "enabled", budget_tokens: 10000 },
       messages: [{ role: "user", content: "..." }]
     });
     ```

     ```csharp C#
     using Anthropic;
     using Anthropic.Models.Messages;

     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = "claude-opus-4-6",
         MaxTokens = 16000,
         Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
         Messages = [new() { Role = Role.User, Content = "..." }]
     };

     var response = await client.Messages.Create(parameters);
     Console.WriteLine(response);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     "claude-opus-4-6",
     	MaxTokens: 16000,
     	Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
     	},
     })
     if err != nil {
     	log.Fatal(err)
     }
     fmt.Println(response)
     ```

     ```java Java
     AnthropicClient client = AnthropicOkHttpClient.fromEnv();

     MessageCreateParams params = MessageCreateParams.builder()
         .model("claude-opus-4-6")
         .maxTokens(16000L)
         .enabledThinking(10000L)
         .addUserMessage("...")
         .build();

     Message response = client.messages().create(params);
     IO.println(response);
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => '...']],
         model: 'claude-opus-4-6',
         thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: "claude-opus-4-6",
       max_tokens: 16000,
       thinking: {
         type: "enabled",
         budget_tokens: 10000
       },
       messages: [
         { role: "user", content: "..." }
       ]
     )
     ```
   </CodeGroup>

   Sesudah (Claude Opus 5):

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -H "content-type: application/json" \
       -d '{
         "model": "claude-opus-5",
         "max_tokens": 16000,
         "thinking": {
           "type": "adaptive"
         },
         "output_config": {
           "effort": "high"
         },
         "messages": [
           {
             "role": "user",
             "content": "..."
           }
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-opus-5
     max_tokens: 16000
     thinking:
       type: adaptive
     output_config:
       effort: high
     messages:
       - role: user
         content: "..."
     YAML
     ```

     ```python Python
     client.messages.create(
         model="claude-opus-5",
         max_tokens=16000,
         thinking={"type": "adaptive"},
         output_config={"effort": "high"},  # or "max", "xhigh", "medium", "low"
         messages=[{"role": "user", "content": "..."}],
     )
     ```

     ```typescript TypeScript
     await client.messages.create({
       model: "claude-opus-5",
       max_tokens: 16000,
       thinking: { type: "adaptive" },
       output_config: { effort: "high" }, // or "max", "xhigh", "medium", "low"
       messages: [{ role: "user", content: "..." }]
     });
     ```

     ```csharp C#
     using Anthropic;
     using Anthropic.Models.Messages;

     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = "claude-opus-5",
         MaxTokens = 16000,
         Thinking = new ThinkingConfigAdaptive(),
         OutputConfig = new OutputConfig { Effort = Effort.High }, // or Max, Xhigh, Medium, Low
         Messages = [new() { Role = Role.User, Content = "..." }]
     };

     var response = await client.Messages.Create(parameters);
     Console.WriteLine(response);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     "claude-opus-5",
     	MaxTokens: 16000,
     	Thinking: anthropic.ThinkingConfigParamUnion{
     		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
     	},
     	OutputConfig: anthropic.OutputConfigParam{
     		Effort: anthropic.OutputConfigEffortHigh, // or Max, Xhigh, Medium, Low
     	},
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
     	},
     })
     if err != nil {
     	log.Fatal(err)
     }
     fmt.Println(response)
     ```

     ```java Java
     AnthropicClient client = AnthropicOkHttpClient.fromEnv();

     MessageCreateParams params = MessageCreateParams.builder()
         .model("claude-opus-5")
         .maxTokens(16000L)
         .thinking(ThinkingConfigAdaptive.builder().build())
         .outputConfig(OutputConfig.builder()
             .effort(OutputConfig.Effort.HIGH) // or MAX, XHIGH, MEDIUM, LOW
             .build())
         .addUserMessage("...")
         .build();

     Message response = client.messages().create(params);
     IO.println(response);
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => '...']],
         model: 'claude-opus-5',
         thinking: ['type' => 'adaptive'],
         outputConfig: ['effort' => 'high'], // or 'max', 'xhigh', 'medium', 'low'
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: "claude-opus-5",
       max_tokens: 16000,
       thinking: {
         type: "adaptive"
       },
       output_config: {
         effort: "high" # or "max", "xhigh", "medium", "low"
       },
       messages: [
         { role: "user", content: "..." }
       ]
     )
     ```
   </CodeGroup>

   Pemikiran adaptif dapat diarahkan melalui prompting dan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort); lihat [Memilih tingkat effort](https://platform.claude.com/docs/id/models/opus-5/migration-guide#choosing-an-effort-level).

2. **Thinking aktif secara default:** Pada Claude Opus 4.6 dan Claude Opus 4.7, permintaan tanpa field `thinking` berjalan tanpa pemikiran; pada Claude Opus 5, permintaan yang sama berjalan dengan [pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking). `max_tokens` tetap menjadi batas keras pada total output, yaitu pemikiran ditambah teks respons, jadi tinjau kembali nilainya untuk beban kerja yang sebelumnya berjalan tanpa pemikiran. Token pemikiran ditagih sebagai token output bahkan ketika teks pemikiran tidak dikembalikan kepada Anda, sehingga meskipun harga per token tidak berubah, beban kerja yang sebelumnya berjalan tanpa pemikiran dapat menghasilkan lebih banyak token output per permintaan pada Claude Opus 5; lihat [Kontrol biaya](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#cost-control). Untuk mempertahankan perilaku lama, kirimkan `thinking: {type: "disabled"}`, dengan tunduk pada batas effort di butir berikutnya; perhatikan bahwa dengan pemikiran dinonaktifkan, model sesekali dapat mengeluarkan pemanggilan alat sebagai teks biasa atau menyertakan tag XML internal dalam output yang terlihat, jadi utamakan tingkat effort yang lebih rendah dengan pemikiran diaktifkan jika memungkinkan, dan lihat [Menjalankan dengan pemikiran dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk mitigasi jika tidak memungkinkan.

   Bentuk respons juga berubah bersamanya. Dengan pemikiran aktif, sebuah respons dapat dimulai dengan satu atau lebih blok `thinking` sebelum blok `text` pertama, dan karena konten pemikiran dihilangkan secara default pada Claude Opus 5 (butir 5 dalam daftar ini), blok-blok tersebut tiba dengan field `thinking` kosong di samping `signature`-nya. Kode yang membaca balasan berdasarkan posisi, seperti `content[0].text` atau handler stream yang memperlakukan event `content_block_start` pertama sebagai teks, akan rusak pada respons ini. Sebagai gantinya, pilih blok konten berdasarkan field `type`-nya: baca `text` dari blok yang `type`-nya adalah `"text"`, dan lakukan percabangan berdasarkan tipe blok saat menangani event stream.

   Jika Anda menjalankan loop penggunaan alat, kirimkan kembali blok `thinking` dari setiap respons asisten ke API secara lengkap dan tanpa modifikasi saat Anda mengembalikan hasil alat, termasuk blok yang field `thinking`-nya kosong. Kembalikan pesan asisten sebagaimana diterima alih-alih memfilter blok kontennya berdasarkan tipe atau membangunnya ulang: API menolak blok pemikiran yang diedit, diurutkan ulang, atau dihapus sebagian dengan error 400. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).

3. **Menonaktifkan thinking dibatasi pada effort `high`:** Anda dapat mematikan pemikiran dengan `thinking: {type: "disabled"}`, tetapi hanya pada tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah. Permintaan yang menggabungkan `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400 pada Claude Opus 5, yang diberlakukan pada setiap permintaan. Audit permintaan yang menonaktifkan pemikiran sebelum Anda bermigrasi: aktifkan kembali pemikiran atau turunkan effort ke `high` atau lebih rendah.

4. **Parameter sampling dihapus:** Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default apa pun pada Claude Opus 4.7 atau model yang lebih baru, termasuk Claude Opus 5, mengembalikan error 400. Python SDK (v1.0 dan yang lebih baru) tidak mendefinisikannya, dan mengirimkannya akan memunculkan `TypeError`. Jalur migrasi paling aman adalah menghilangkan parameter ini sepenuhnya dari payload permintaan. Prompting adalah cara yang direkomendasikan untuk memandu perilaku model pada Claude Opus 5. Jika Anda sebelumnya menggunakan `temperature = 0` untuk determinisme, perhatikan bahwa hal itu tidak pernah menjamin output yang identik pada model sebelumnya.

5. **Konten thinking dihilangkan secara default:** Blok thinking masih muncul dalam stream respons pada Claude Opus 4.7 dan model yang lebih baru, tetapi field `thinking`-nya kosong kecuali Anda secara eksplisit memilih untuk mengaktifkannya. Ini adalah perubahan diam-diam dari Claude Opus 4.6, di mana defaultnya adalah mengembalikan teks pemikiran yang diringkas. Untuk memulihkan konten pemikiran yang diringkas, atur `thinking.display` ke `"summarized"`:

   <CodeGroup exclude="shell">
     ```python Python
     thinking = {
         "type": "adaptive",
         "display": "summarized",
     }
     ```

     ```typescript TypeScript
     const thinking = {
       type: "adaptive",
       display: "summarized"
     };
     ```

     ```csharp C#
     var thinking = new ThinkingConfigAdaptive { Display = Display.Summarized };
     ```

     ```go Go
     thinking := anthropic.ThinkingConfigParamUnion{
     	OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{
     		Display: anthropic.ThinkingConfigAdaptiveDisplaySummarized,
     	},
     }
     ```

     ```java Java
     ThinkingConfigAdaptive thinking = ThinkingConfigAdaptive.builder()
         .display(ThinkingConfigAdaptive.Display.SUMMARIZED)
         .build();
     ```

     ```php PHP
     $thinking = ['type' => 'adaptive', 'display' => 'summarized'];
     ```

     ```ruby Ruby
     thinking = {
       type: "adaptive",
       display: "summarized"
     }
     ```
   </CodeGroup>

   Defaultnya adalah `"omitted"` pada Claude Opus 4.7 dan model yang lebih baru. Jika produk Anda melakukan streaming penalaran kepada pengguna, default baru ini tampak sebagai jeda panjang sebelum output dimulai; atur `display: "summarized"` untuk memulihkan kemajuan yang terlihat selama pemikiran. Lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display) untuk detailnya.

6. **Penghitungan token diperbarui:** Claude Opus 4.7 memperkenalkan tokenizer baru, yang juga digunakan oleh model Opus yang lebih baru, termasuk Claude Opus 5. Tokenizer ini berkontribusi pada peningkatan kinerja di berbagai tugas, dan mungkin menggunakan sekitar 1x hingga 1,35x lebih banyak token saat memproses teks dibandingkan model sebelum Claude Opus 4.7 (hingga \~35% lebih banyak, bervariasi menurut konten).

   [`/v1/messages/count_tokens`](https://platform.claude.com/docs/id/build-with-claude/token-counting) mengembalikan jumlah token yang berbeda untuk Claude Opus 5 dibandingkan untuk Claude Opus 4.6. Efisiensi token dapat bervariasi menurut bentuk beban kerja.

   Intervensi prompting, `task_budget`, dan `effort` dapat membantu mengontrol biaya dan memastikan penggunaan token yang sesuai. Kontrol ini mungkin mengorbankan kecerdasan model. Perbarui parameter `max_tokens` Anda untuk memberikan ruang tambahan, termasuk pemicu compaction. Claude Opus 5 menyediakan jendela konteks 1M dengan harga API standar tanpa premi konteks panjang.

7. **Penghapusan prefill (dibawa dari Opus 4.6):** Melakukan prefill pesan asisten mengembalikan error 400 pada Claude Opus 4.7 dan model yang lebih baru, termasuk Claude Opus 5. Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) (output terstruktur), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

### Memilih tingkat effort

[Parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) memungkinkan Anda menyetel kecerdasan Claude terhadap pengeluaran token, menukar kemampuan dengan kecepatan yang lebih tinggi dan biaya yang lebih rendah. Claude Opus 5 mendukung seluruh rangkaian tingkat effort dan defaultnya adalah `high`. Jalankan sapuan effort baru pada eval Anda sendiri alih-alih membawa pengaturan yang disetel untuk model sebelumnya:

* **`max`:** Dapat memberikan peningkatan pada tugas yang paling menuntut tetapi mungkin menunjukkan hasil yang semakin berkurang dari peningkatan penggunaan token dan dapat cenderung berpikir berlebihan pada tugas yang lebih sederhana. Uji pada kasus di mana kemampuan maksimum lebih penting daripada pengeluaran token.
* **`xhigh`:** Kemampuan yang diperluas untuk pekerjaan agentic dan coding yang berjalan lama yang membutuhkan kedalaman lebih dari default.
* **`high`:** Default. Menyeimbangkan penggunaan token dan kecerdasan untuk sebagian besar tugas.
* **`medium`:** Penurunan hemat biaya dari default, layak diuji sebagai kontrol biaya dan latensi.
* **`low`:** Paling efisien. Cadangkan untuk tugas singkat dengan cakupan terbatas dan beban kerja yang sensitif terhadap latensi.

Jika Anda menjalankan pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak; mulailah dari 64k token dan setel dari sana. Effort lebih penting untuk model ini dibandingkan Opus sebelumnya mana pun. Bereksperimenlah dengannya secara aktif saat Anda melakukan upgrade.

### Perubahan perilaku

Claude Opus 4.7 memperkenalkan beberapa perbedaan perilaku dari Claude Opus 4.6 yang bukan merupakan perubahan API yang merusak kompatibilitas tetapi mungkin memerlukan pembaruan prompt atau penghapusan scaffolding. Perubahan ini berlanjut ke Claude Opus 5, dengan penyesuaian yang dicatat dalam daftar ini.

1. **Panjang respons bervariasi menurut kasus penggunaan:** Claude Opus 4.7 mengkalibrasi panjang respons sesuai dengan seberapa kompleks tugas tersebut menurut penilaiannya, alih-alih menggunakan tingkat verbositas tetap secara default. Ini biasanya berarti jawaban yang lebih pendek pada pencarian sederhana dan jawaban yang jauh lebih panjang pada analisis terbuka.

   Jika produk Anda bergantung pada gaya atau verbositas output tertentu, Anda mungkin perlu menyetel prompt Anda. Misalnya, untuk mengurangi verbositas, tambahkan: "Provide concise, focused responses. Skip non-essential context, and keep examples minimal." Jika Anda melihat jenis penjelasan berlebihan tertentu, tambahkan instruksi yang ditargetkan dalam prompt Anda untuk mencegahnya.

   Contoh positif yang menunjukkan bagaimana Claude dapat berkomunikasi dengan tingkat keringkasan yang sesuai cenderung lebih efektif daripada contoh negatif atau instruksi yang memberi tahu model apa yang tidak boleh dilakukan. Pada Claude Opus 5, respons terlihat default dan hasil kerja tertulis lebih panjang dibandingkan model Opus sebelumnya, dan menurunkan effort mengurangi volume pemikiran tanpa secara andal memperpendek respons yang terlihat; berikan prompt secara eksplisit untuk keringkasan atau panjang target. Lihat [Panjang respons dan verbositas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity).

2. **Mengikuti instruksi secara lebih harfiah:** Claude Opus 4.7 menafsirkan prompt secara lebih harfiah dan eksplisit daripada Claude Opus 4.6, terutama pada tingkat effort yang lebih rendah. Model ini tidak secara diam-diam menggeneralisasi instruksi dari satu butir ke butir lain, dan tidak menyimpulkan permintaan yang tidak Anda buat. Sisi positif dari keharfiahan ini adalah presisi dan lebih sedikit kerja sia-sia. Model ini umumnya berkinerja lebih baik untuk kasus penggunaan API dengan prompt yang disetel dengan cermat, ekstraksi terstruktur, dan pipeline di mana Anda menginginkan perilaku yang dapat diprediksi. Peninjauan prompt dan harness mungkin sangat membantu untuk migrasi ke Claude Opus 5.

3. **Nada yang lebih langsung:** Seperti halnya model baru mana pun, gaya prosa pada tulisan panjang mungkin bergeser. Claude Opus 4.7 lebih langsung dan beropini, dengan lebih sedikit frasa yang mengutamakan validasi dan lebih sedikit emoji dibandingkan gaya Claude Opus 4.6 yang lebih hangat. Jika produk Anda mengandalkan suara tertentu, evaluasi ulang prompt gaya terhadap baseline baru.

4. **Pembaruan kemajuan bawaan dalam jejak agentic:** Claude Opus 4.7 memberikan pembaruan yang lebih teratur dan berkualitas lebih tinggi kepada pengguna sepanjang jejak agentic yang panjang. Jika Anda telah menambahkan scaffolding untuk memaksa pesan status sementara ("After every 3 tool calls, summarize progress"), cobalah menghapusnya. Jika Anda mendapati bahwa panjang atau isi pembaruan Claude Opus 4.7 yang ditujukan kepada pengguna tidak terkalibrasi dengan baik untuk kasus penggunaan Anda, jelaskan secara eksplisit seperti apa pembaruan ini seharusnya dalam prompt dan berikan contoh.

5. **Pembuatan subagen berubah:** Claude Opus 4.7 cenderung membuat lebih sedikit subagen secara default dibandingkan Claude Opus 4.6, sementara Claude Opus 5 mendelegasikan ke subagen dengan lebih mudah dibandingkan model sebelumnya. Perilaku ini dapat diarahkan melalui prompting ke kedua arah; berikan panduan eksplisit tentang kapan subagen diinginkan, atau batasi jumlah subagen. Lihat [Mengontrol pembuatan subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning).

6. **Kalibrasi effort yang lebih ketat:** Berubah secara signifikan dari Claude Opus 4.6, Claude Opus 4.7 mematuhi [tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort) secara ketat, terutama di tingkat rendah. Pada `low` dan `medium`, model membatasi cakupan pekerjaannya pada apa yang diminta alih-alih melakukan lebih dari yang diminta.

   Ini baik untuk latensi dan biaya, tetapi pada tugas yang cukup kompleks yang berjalan pada effort `low` ada risiko kurang berpikir. Jika Anda mengamati penalaran yang dangkal pada masalah kompleks, naikkan effort ke `high` atau `xhigh` alih-alih mengatasinya dengan prompting.

   Jika Anda perlu mempertahankan effort pada `low` demi latensi, tambahkan panduan yang ditargetkan: "This task involves multistep reasoning. Think carefully through the problem before responding." Lihat [Tingkat effort yang direkomendasikan untuk Claude Opus 4.7](https://platform.claude.com/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-opus-4-7).

7. **Lebih sedikit pemanggilan alat secara default:** Claude Opus 4.7 memiliki kecenderungan untuk menggunakan alat lebih jarang dibandingkan Claude Opus 4.6 dan lebih banyak menggunakan penalaran. Ini menghasilkan hasil yang lebih baik dalam sebagian besar kasus.

   Untuk meningkatkan penggunaan alat, naikkan pengaturan effort. Pengaturan effort `high` atau `xhigh` menunjukkan penggunaan alat yang jauh lebih banyak dalam pencarian agentic dan coding. Anda juga dapat menyesuaikan prompt Anda untuk secara eksplisit menginstruksikan model tentang kapan dan bagaimana menggunakan alatnya dengan benar.

8. **Pengamanan keamanan siber real-time:** Baru ditambahkan di Claude Opus 4.7, permintaan yang melibatkan topik terlarang atau berisiko tinggi dapat menyebabkan penolakan. Untuk pekerjaan keamanan yang sah seperti pengujian penetrasi, penelitian kerentanan, atau red-teaming, ajukan permohonan ke [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet) untuk meminta pengurangan pembatasan. Jalur permohonan bergantung pada cara Anda mengakses Claude.

9. **Dukungan gambar resolusi tinggi:** Claude Opus 4.7 adalah model Claude pertama dengan dukungan gambar resolusi tinggi. Resolusi gambar maksimum adalah 2.576 piksel pada sisi panjang, naik dari 1.568 piksel pada model sebelumnya. Ini membuka peningkatan pada beban kerja yang banyak menggunakan visi dan sangat berharga untuk computer use, pemahaman tangkapan layar, dan analisis dokumen.

   Dukungan resolusi tinggi bersifat otomatis dan tidak memerlukan header beta atau opt-in di sisi klien. Dua hal yang perlu direncanakan:

   * Gambar resolusi penuh dapat menggunakan hingga sekitar 3x lebih banyak token gambar dibandingkan model sebelumnya (hingga 4.784 token per gambar, dibandingkan batas sebelumnya sekitar 1.600 token per gambar). Anggarkan ulang `max_tokens` dan ekspektasi biaya untuk beban kerja yang banyak menggunakan gambar, atau lakukan downsample sebelum mengirim jika Anda tidak memerlukan fidelitas tambahan.
   * Koordinat penunjukan dan bounding-box yang dikembalikan oleh model bersifat 1:1 dengan piksel gambar sebenarnya pada Claude Opus 4.7, sehingga tidak diperlukan konversi faktor skala.

   Lihat [Dukungan gambar resolusi tinggi pada Claude Opus 4.7](https://platform.claude.com/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) untuk detailnya.

### Perubahan yang direkomendasikan

Perubahan ini tidak wajib tetapi akan meningkatkan pengalaman Anda:

1. **Evaluasi ulang `max_tokens`:** Karena teks yang sama menghasilkan jumlah token yang lebih tinggi pada Claude Opus 4.7 dan model yang lebih baru, perbarui parameter `max_tokens` Anda untuk memberikan ruang tambahan, termasuk pemicu compaction. Intervensi prompting, [`task_budget`](https://platform.claude.com/docs/id/build-with-claude/task-budgets), dan [`effort`](https://platform.claude.com/docs/id/build-with-claude/effort) dapat membantu mengontrol biaya dan memastikan penggunaan token yang sesuai.

2. **Audit ekspektasi jumlah token:** Setiap jalur kode yang memperkirakan token di sisi klien atau mengasumsikan rasio token-ke-karakter yang tetap harus diuji ulang terhadap Claude Opus 5. Gunakan [endpoint penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) untuk memverifikasi.

3. **Adopsi [task budgets](https://platform.claude.com/docs/id/build-with-claude/task-budgets) (anggaran tugas) (beta):** Claude Opus 4.7 memperkenalkan task budgets. Anggaran ini memungkinkan Anda memberi tahu Claude berapa banyak token yang dimilikinya untuk satu loop agentic penuh, termasuk pemikiran, pemanggilan alat, hasil alat, dan output akhir. Model melihat hitungan mundur yang berjalan dan menggunakannya untuk memprioritaskan pekerjaan dan menyelesaikan tugas dengan baik saat anggaran habis. Untuk menggunakannya, atur header beta `task-budgets-2026-03-13` dan tambahkan yang berikut ke output config Anda:

   <CodeGroup exclude="shell">
     ```python Python
     output_config = {
         "effort": "high",
         "task_budget": {"type": "tokens", "total": 128000},
     }
     ```

     ```typescript TypeScript
     const output_config = {
       effort: "high",
       task_budget: { type: "tokens", total: 128000 }
     };
     ```

     ```csharp C#
     var outputConfig = new BetaOutputConfig
     {
         Effort = Effort.High,
         TaskBudget = new BetaTokenTaskBudget
         {
             Total = 128000,
         },
     };
     ```

     ```go Go
     outputConfig := anthropic.BetaOutputConfigParam{
     	Effort: anthropic.BetaOutputConfigEffortHigh,
     	TaskBudget: anthropic.BetaTokenTaskBudgetParam{
     		Total: 128000,
     	},
     }
     ```

     ```java Java
     BetaOutputConfig outputConfig = BetaOutputConfig.builder()
         .effort(BetaOutputConfig.Effort.HIGH)
         .taskBudget(BetaTokenTaskBudget.builder()
             .total(128000L)
             .build())
         .build();
     ```

     ```php PHP
     $outputConfig = [
         'effort' => 'high',
         'taskBudget' => [
             'type' => 'tokens',
             'total' => 128000,
         ],
     ];
     ```

     ```ruby Ruby
     output_config = {
       effort: :high,
       task_budget: {
         type: :tokens,
         total: 128_000
       }
     }
     ```
   </CodeGroup>

   Anda mungkin perlu bereksperimen dengan task budget yang berbeda untuk kasus penggunaan Anda. Jika model diberi task budget yang terlalu ketat, model mungkin menyelesaikan tugas dengan kurang menyeluruh, dengan merujuk anggarannya sebagai kendala.

   Untuk tugas agentic terbuka di mana kualitas lebih penting daripada kecepatan, jangan atur task budget. Cadangkan task budget untuk beban kerja di mana Anda memerlukan model untuk membatasi cakupan pekerjaannya pada jatah token. Nilai minimum untuk task budget adalah 20k token.

   Task budget bukanlah batas keras; ini adalah saran yang disadari oleh model. Ini berbeda dari `max_tokens`:

   * **`task_budget`:** batas bersifat anjuran di seluruh loop agentic penuh. Model melihatnya dan menggunakannya untuk mengatur kecepatannya sendiri.
   * **`max_tokens`:** batas atas keras per permintaan pada token yang dihasilkan. Nilai ini tidak diteruskan ke model, sehingga model tidak menyadarinya.

   Gunakan `task_budget` ketika Anda ingin model memoderasi dirinya sendiri, dan `max_tokens` sebagai batas atas keras untuk membatasi penggunaan.

4. **Atur `max_tokens` yang besar pada effort `max` atau `xhigh`:** Jika Anda menjalankan Claude Opus 4.7 atau model yang lebih baru pada effort `max` atau `xhigh`, atur anggaran token output maksimum yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alatnya. Mulailah dari 64k token dan setel dari sana.

5. **Lakukan downsample gambar jika resolusi tinggi tidak diperlukan:** Claude Opus 4.7 dan model yang lebih baru mendukung gambar hingga 2576px / 3,75MP. Gambar resolusi tinggi menggunakan lebih banyak token. Jika fidelitas gambar tambahan tidak diperlukan, lakukan downsample gambar sebelum mengirim ke Claude untuk menghindari peningkatan penggunaan token. Lihat [Gambar dan visi](https://platform.claude.com/docs/id/build-with-claude/vision).

6. **Pertimbangkan fallback otomatis:** Claude Opus 5 dirilis dengan classifier keamanan siber yang penolakan kategori sibernya dapat melakukan fallback ke Claude Opus 4.8. Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, pertimbangkan parameter `fallbacks` dengan mode `"default"` (`fallbacks: "default"`), yang memilih model fallback yang direkomendasikan berdasarkan kategori penolakan alih-alih daftar model yang dikelola secara manual. Fallback sisi server masih dalam beta; mode `"default"` memerlukan header beta `server-side-fallback-2026-07-01`. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

7. **Cache prompt yang lebih pendek:** Panjang prompt minimum yang dapat di-cache pada Claude Opus 5 adalah 512 token, lebih rendah dibandingkan model Opus sebelumnya. Prompt yang sebelumnya terlalu pendek untuk di-cache kini dapat membuat entri cache, tanpa perlu perubahan kode. Lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

8. **Ubah alat di tengah percakapan (beta):** Anda dapat menambah atau menghapus alat di antara giliran percakapan tanpa membatalkan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya. Kirim header beta `mid-conversation-tool-changes-2026-07-01`. Ini berguna untuk beban kerja agentic yang mengekspos alat secara bertahap atau menghentikannya seiring kemajuan tugas; tanpanya, daftar alat yang berubah akan membatalkan prefiks yang di-cache.

9. **Hapus instruksi verifikasi yang terbawa dan batasi cakupan:** Claude Opus 5 memverifikasi pekerjaannya sendiri tanpa perlu diberi tahu, jadi hapus instruksi verifikasi atau pemeriksaan mandiri eksplisit yang terbawa dari prompt yang disetel untuk model sebelumnya; membiarkannya akan menyebabkan verifikasi berlebihan. Untuk tugas yang sempit, batasi cakupan tugas secara eksplisit. Lihat [Cakupan tugas dan verifikasi berlebihan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#task-scope-and-over-verification).

### Daftar periksa migrasi

* Perbarui nama model dari `claude-opus-4-6` ke `claude-opus-5` (atau perbarui alias).
* Hapus `temperature`, `top_p`, dan `top_k` dari payload permintaan.
* Ganti `thinking: {type: "enabled", budget_tokens: N}` dengan `thinking: {type: "adaptive"}` ditambah [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort), atau hapus field `thinking` sepenuhnya; pemikiran adaptif aktif secara default pada Claude Opus 5.
* Tinjau beban kerja yang berjalan tanpa field `thinking`: beban kerja tersebut berjalan dengan pemikiran pada Claude Opus 5. Tinjau kembali `max_tokens`, yang tetap menjadi batas keras pada total output (pemikiran ditambah teks respons), atau kirimkan `thinking: {type: "disabled"}` pada effort `high` atau lebih rendah untuk mempertahankan perilaku lama.
* Perbarui parsing respons yang membaca konten berdasarkan posisi, seperti `content[0].text` atau handler stream yang mengasumsikan blok konten pertama adalah teks: dengan pemikiran aktif, blok `thinking` tiba sebelum blok `text`. Pilih blok konten berdasarkan `type` sebagai gantinya.
* Jika Anda menjalankan loop penggunaan alat, kirimkan kembali blok `thinking` secara lengkap dan tanpa modifikasi saat Anda mengembalikan hasil alat; blok yang dimodifikasi mengembalikan error 400. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).
* Audit permintaan yang menonaktifkan pemikiran: `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400, yang diberlakukan pada setiap permintaan. Aktifkan kembali pemikiran atau turunkan effort ke `high` atau lebih rendah.
* Hapus semua prefill pesan asisten.
* Jika UI Anda menampilkan konten pemikiran, secara eksplisit pilih untuk mengaktifkan peringkasan pemikiran.
* Lakukan benchmark ulang biaya dan latensi end-to-end di bawah tokenisasi yang diperbarui; token pemikiran ditagih sebagai token output, sehingga beban kerja yang sebelumnya berjalan tanpa pemikiran juga dapat menghasilkan lebih banyak token output per permintaan.
* Setel ulang `max_tokens` untuk memperhitungkan tokenisasi yang diperbarui.
* Uji ulang semua estimasi jumlah token di sisi klien.
* Jika aplikasi Anda mengirim gambar, anggarkan ulang untuk [dukungan gambar resolusi tinggi](https://platform.claude.com/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) (hingga sekitar 3x lebih banyak token gambar per gambar resolusi penuh). Lakukan downsample sebelum mengirim jika Anda tidak memerlukan fidelitas tambahan.
* Jika Anda menggunakan koordinat penunjukan atau bounding-box dari model, hapus semua konversi faktor skala; koordinat bersifat 1:1 dengan piksel gambar sebenarnya pada Claude Opus 4.7 dan model yang lebih baru.
* Tinjau prompt untuk perubahan perilaku (panjang respons, keharfiahan, nada, pembaruan kemajuan, subagen, kalibrasi effort, pemicuan alat, pengamanan siber, penanganan gambar resolusi tinggi).
* Tetapkan ulang baseline panjang respons dengan prompt kontrol panjang yang ada dihapus, lalu setel secara eksplisit.
* Jika menggunakan effort `xhigh` atau `max`, naikkan `max_tokens` ke setidaknya 64k sebagai titik awal.
* Pertimbangkan untuk mengadopsi task budgets (beta) dan perubahan alat di tengah percakapan (beta) untuk alur kerja agentic.
* Tangani `stop_reason: "refusal"`, dan pertimbangkan `fallbacks: "default"` (beta) untuk menjalankan ulang permintaan yang ditolak pada model fallback yang direkomendasikan secara otomatis.
* Tinjau prompt yang mendekati minimum caching: prompt dengan 512 token atau lebih kini dapat membuat entri cache pada Claude Opus 5.
* Jika Anda menggunakan [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool), rencanakan alternatif: fitur ini tidak tersedia pada Claude Opus 5.
* Jika organisasi Anda memiliki komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models), perhatikan bahwa Priority Tier tidak didukung pada Claude Opus 5.
* Hapus instruksi verifikasi dan pemeriksaan mandiri yang terbawa dari prompt yang disetel untuk model sebelumnya; instruksi tersebut menyebabkan verifikasi berlebihan pada Claude Opus 5.
* Jika produk Anda melakukan pekerjaan keamanan yang sah, ajukan permohonan ke [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet) untuk akses ke pembatasan yang lebih rendah pada konten siber.

### Bermigrasi dari Claude Opus 4.5 atau yang lebih lama

Jika Anda bermigrasi dari Claude Opus 4.5, Opus 4.1, atau model yang lebih lama langsung ke Claude Opus 5, terapkan **semua perubahan sebelumnya di bagian ini** ditambah perubahan kumulatif berikut, yang mulai berlaku antara Opus 4.5 dan Opus 4.7. Jika Anda bermigrasi dari Opus 4.6, perubahan sebelumnya di bagian ini adalah semua yang Anda perlukan.

#### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-5"  # Before
model = "claude-opus-5"  # After
```

#### Perubahan yang merusak kompatibilitas

1. **Penghapusan prefill** dibahas dalam [perubahan yang merusak kompatibilitas untuk bermigrasi dari Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-5/migration-guide#opus-46-breaking-changes).

2. **Pengutipan parameter alat:** Claude Opus 4.6 dan model yang lebih baru mungkin menghasilkan escaping string JSON yang sedikit berbeda dalam argumen pemanggilan alat (misalnya, penanganan escape Unicode atau escaping garis miring yang berbeda). Jika Anda mem-parsing `input` pemanggilan alat sebagai string mentah alih-alih menggunakan parser JSON, verifikasi logika parsing Anda. Parser JSON standar (seperti `json.loads()` atau `JSON.parse()`) menangani perbedaan ini secara otomatis.

#### Perubahan yang direkomendasikan

Perubahan ini meningkatkan pengalaman Anda pada Claude Opus 4.7 dan model yang lebih baru. Butir yang ditandai **(wajib pada Opus 4.7)** merupakan rekomendasi opsional saat Opus 4.6 diluncurkan tetapi kini bersifat wajib; sisanya tetap direkomendasikan.

1. **Bermigrasi ke pemikiran adaptif (wajib pada Opus 4.7):** `thinking: {type: "enabled", budget_tokens: N}` mengembalikan error 400 pada Claude Opus 4.7 dan model yang lebih baru. Beralihlah ke `thinking: {type: "adaptive"}` dan gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran; pada Claude Opus 5, `thinking: {type: "adaptive"}` setara dengan menghilangkan field `thinking`, yang berjalan dengan pemikiran adaptif secara default. Lihat [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking).

   <CodeGroup>
     ```bash cURL
     curl -sS https://api.anthropic.com/v1/messages \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d '{
         "model": "claude-opus-5",
         "max_tokens": 16000,
         "thinking": {"type": "adaptive"},
         "output_config": {"effort": "high"},
         "messages": [{"role": "user", "content": "Your prompt here"}]
       }'
     ```

     ```python Before
     response = client.beta.messages.create(
         model="claude-opus-4-5",
         max_tokens=16000,
         thinking={"type": "enabled", "budget_tokens": 32000},
         betas=["interleaved-thinking-2025-05-14"],
         messages=[{"role": "user", "content": "Your prompt here"}],
     )
     ```

     ```python After
     response = client.messages.create(
         model="claude-opus-5",
         max_tokens=16000,
         thinking={"type": "adaptive"},
         output_config={"effort": "high"},
         messages=[{"role": "user", "content": "Your prompt here"}],
     )
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-opus-5
     max_tokens: 16000
     thinking:
       type: adaptive
     output_config:
       effort: high
     messages:
       - role: user
         content: Your prompt here
     YAML
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const response = await client.messages.create({
       model: "claude-opus-5",
       max_tokens: 16000,
       thinking: { type: "adaptive" },
       output_config: { effort: "high" },
       messages: [{ role: "user", content: "Your prompt here" }]
     });
     ```

     ```csharp C#
     using Anthropic;
     using Anthropic.Models.Messages;

     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = Model.ClaudeOpus5,
         MaxTokens = 16000,
         Thinking = new ThinkingConfigAdaptive(),
         OutputConfig = new OutputConfig { Effort = Effort.High },
         Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
     };

     var response = await client.Messages.Create(parameters);
     Console.WriteLine(response);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     anthropic.ModelClaudeOpus5,
     	MaxTokens: 16000,
     	Thinking: anthropic.ThinkingConfigParamUnion{
     		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
     	},
     	OutputConfig: anthropic.OutputConfigParam{
     		Effort: anthropic.OutputConfigEffortHigh,
     	},
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("Your prompt here")),
     	},
     })
     if err != nil {
     	log.Fatal(err)
     }
     fmt.Println(response)
     ```

     ```java Java
     import com.anthropic.models.messages.OutputConfig;
     import com.anthropic.models.messages.ThinkingConfigAdaptive;
     // ...
     public class AdaptiveThinkingExample {
         public static void main(String[] args) {
             AnthropicClient client = AnthropicOkHttpClient.fromEnv();

             MessageCreateParams params = MessageCreateParams.builder()
                 .model(Model.CLAUDE_OPUS_5)
                 .maxTokens(16000L)
                 .thinking(ThinkingConfigAdaptive.builder().build())
                 .outputConfig(OutputConfig.builder()
                     .effort(OutputConfig.Effort.HIGH)
                     .build())
                 .addUserMessage("Your prompt here")
                 .build();

             Message response = client.messages().create(params);
             System.out.println(response);
         }
     }
     ```

     ```php PHP
     $client = new Client();

     $response = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => 'Your prompt here']],
         model: 'claude-opus-5',
         thinking: ['type' => 'adaptive'],
         outputConfig: ['effort' => 'high'],
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     response = client.messages.create(
       model: "claude-opus-5",
       max_tokens: 16000,
       thinking: { type: "adaptive" },
       output_config: { effort: "high" },
       messages: [{ role: "user", content: "Your prompt here" }]
     )
     ```
   </CodeGroup>

   Perhatikan bahwa migrasi ini juga berpindah dari `client.beta.messages.create` ke `client.messages.create`. Pemikiran adaptif dan effort tidak memerlukan namespace SDK beta atau header beta apa pun.

2. **Hapus header beta effort:** Parameter effort tidak memerlukan header beta. Hapus `betas=["effort-2025-11-24"]` dari permintaan Anda.

3. **Hapus header beta fine-grained tool streaming:** Fine-grained tool streaming tidak memerlukan header beta. Hapus `betas=["fine-grained-tool-streaming-2025-05-14"]` dari permintaan Anda.

4. **Hapus header beta interleaved thinking:** Pemikiran adaptif secara otomatis mengaktifkan interleaved thinking pada Claude Opus 4.7, Opus 4.6, dan Sonnet 4.6. Hapus `betas=["interleaved-thinking-2025-05-14"]` dari permintaan Anda. Header ini masih berfungsi pada Sonnet 4.6 dengan pemikiran diperpanjang manual, tetapi mode manual sudah deprecated.

5. **Bermigrasi ke output\_config.format:** Jika menggunakan structured outputs, perbarui `output_format={...}` menjadi `output_config={"format": {...}}`. API masih menerima parameter `output_format` yang deprecated, tetapi parameter ini akan dihapus dalam rilis model mendatang. Python SDK (v1.0 dan yang lebih baru) tidak menerima `output_format={...}` pada `client.beta.messages.create()` atau `count_tokens()`. Argumen `output_format=Model` dari helper `parse()` dan `stream()` tidak berubah.

### Bermigrasi dari Claude 4.1 atau yang lebih lama

Jika Anda bermigrasi dari Opus 4.1 atau model yang lebih lama langsung ke Claude Opus 5, terapkan semua perubahan sebelumnya di bagian ini, ditambah perubahan tambahan di sub-bagian ini.

```python
# Dari Opus 4.1
model = "claude-opus-4-1-20250805"  # Before
model = "claude-opus-5"  # After

# Dari Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Before
model = "claude-opus-5"  # After
```

#### Perubahan tambahan yang merusak kompatibilitas

1. **Hapus parameter sampling**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
   </Warning>

   Mulai dari Claude Opus 4.7, mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default apa pun mengembalikan error 400. Python SDK (v1.0 dan yang lebih baru) tidak mendefinisikannya, dan mengirimkannya akan memunculkan `TypeError`. Jalur migrasi paling aman adalah menghilangkan parameter ini sepenuhnya dari permintaan, dan menggunakan prompting untuk memandu perilaku model. Jika Anda sebelumnya menggunakan `temperature = 0` untuk determinisme, perhatikan bahwa hal itu tidak pernah menjamin output yang identik.

   <CodeGroup exclude="shell">
     ```python Python
     # Sebelum - Ini akan menghasilkan error pada model Claude 4+
     response = client.messages.create(
         model="claude-3-7-sonnet-20250219",
         temperature=0.7,
         top_p=0.9,  # Non-default sampling params return 400 on Opus 4.7
         # ...
     )

     # Sesudah
     response = client.messages.create(
         model="claude-opus-5",
         # ...
     )
     ```

     ```typescript TypeScript
     // Sebelum - Ini akan menghasilkan error pada model Claude 4+
     await client.messages.create({
       model: "claude-3-7-sonnet-20250219",
       temperature: 0.7,
       top_p: 0.9 // Non-default sampling params return 400 on Opus 4.7
       // ...
     });

     // Sesudah
     await client.messages.create({
       model: "claude-opus-5"
       // ...
     });
     ```

     ```csharp C#
     // Sebelum - Ini akan menghasilkan error pada model Claude 4+
     await client.Messages.Create(new MessageCreateParams
     {
         Model = "claude-3-7-sonnet-20250219",
         Temperature = 0.7,
         TopP = 0.9, // Non-default sampling params return 400 on Opus 4.7
         // ...
     });

     // Sesudah
     await client.Messages.Create(new MessageCreateParams
     {
         Model = "claude-opus-5",
         // ...
     });
     ```

     ```go Go
     // Sebelum - Ini akan menghasilkan error pada model Claude 4+
     client.Messages.New(ctx, anthropic.MessageNewParams{
     	Model:       "claude-3-7-sonnet-20250219",
     	Temperature: anthropic.Float(0.7),
     	TopP:        anthropic.Float(0.9), // Non-default sampling params return 400 on Opus 4.7
     	// ...
     })

     // Sesudah
     client.Messages.New(ctx, anthropic.MessageNewParams{
     	Model: "claude-opus-5",
     	// ...
     })
     ```

     ```java Java
     // Sebelum - Ini akan menghasilkan error pada model Claude 4+
     client.messages().create(MessageCreateParams.builder()
         .model("claude-3-7-sonnet-20250219")
         .temperature(0.7)
         .topP(0.9) // Non-default sampling params return 400 on Opus 4.7
         // ...
         .build());

     // Sesudah
     client.messages().create(MessageCreateParams.builder()
         .model("claude-opus-5")
         // ...
         .build());
     ```

     ```php PHP
     // Sebelum - Ini akan menghasilkan error pada model Claude 4+
     $client->messages->create(
         model: 'claude-3-7-sonnet-20250219',
         temperature: 0.7,
         topP: 0.9, // Non-default sampling params return 400 on Opus 4.7
         // ...
     );

     // Sesudah
     $client->messages->create(
         model: 'claude-opus-5',
         // ...
     );
     ```

     ```ruby Ruby
     # Sebelum - Ini akan menghasilkan error pada model Claude 4+
     client.messages.create(
       model: "claude-3-7-sonnet-20250219",
       temperature: 0.7,
       top_p: 0.9, # Non-default sampling params return 400 on Opus 4.7
       # ...
     )

     # Sesudah
     client.messages.create(
       model: "claude-opus-5",
       # ...
     )
     ```
   </CodeGroup>

2. **Perbarui versi alat**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru. Hapus semua kode yang menggunakan perintah `undo_edit`.

   <CodeGroup exclude="shell">
     ```python Python
     # Sebelum
     tools = [{"type": "text_editor_20250124", "name": "str_replace_editor"}]

     # Sesudah
     tools = [{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
     ```

     ```typescript TypeScript
     // Sebelum
     const legacyTools = [{ type: "text_editor_20250124", name: "str_replace_editor" }];

     // Sesudah
     const tools = [{ type: "text_editor_20250728", name: "str_replace_based_edit_tool" }];
     ```

     ```csharp C#
     var parameters = new MessageCreateParams
     {
         // Sebelum: {"type": "text_editor_20250124", "name": "str_replace_editor"}
         // Sesudah:
         Tools = [new ToolTextEditor20250728()],
         // ...
     };
     ```

     ```go Go
     params := anthropic.MessageNewParams{
     	// Sebelum: {"type": "text_editor_20250124", "name": "str_replace_editor"}
     	// Sesudah:
     	Tools: []anthropic.ToolUnionParam{
     		{OfTextEditor20250728: &anthropic.ToolTextEditor20250728Param{}},
     	},
     	// ...
     }
     ```

     ```java Java
     MessageCreateParams params = MessageCreateParams.builder()
         // Sebelum: {"type": "text_editor_20250124", "name": "str_replace_editor"}
         // Sesudah:
         .addTool(ToolTextEditor20250728.builder().build())
         // ...
         .build();
     ```

     ```php PHP
     $message = $client->messages->create(
         // Sebelum: ['type' => 'text_editor_20250124', 'name' => 'str_replace_editor']
         // Sesudah:
         tools: [new ToolTextEditor20250728()],
         // ...
     );
     ```

     ```ruby Ruby
     # Sebelum
     legacy_tools = [{type: "text_editor_20250124", name: "str_replace_editor"}]

     # Sesudah
     tools = [{type: "text_editor_20250728", name: "str_replace_based_edit_tool"}]
     ```
   </CodeGroup>

   * **Text editor:** Gunakan `text_editor_20250728` dan `str_replace_based_edit_tool`. Lihat dokumentasi [alat text editor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool) untuk detailnya.
   * **Code execution:** Upgrade ke `code_execution_20260521`. Lihat dokumentasi [alat code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) untuk instruksi migrasi.

3. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals):

   <CodeGroup exclude="shell">
     ```python Python
     response = client.messages.create(...)

     if response.stop_reason == "refusal":
         # Tangani penolakan dengan tepat
         pass
     ```

     ```typescript TypeScript
     const response = await client.messages.create(/* ... */);

     if (response.stop_reason === "refusal") {
       // Tangani penolakan dengan tepat
     }
     ```

     ```csharp C#
     var response = await client.Messages.Create(...);

     if (response.StopReason?.Value() == StopReason.Refusal)
     {
         // Tangani penolakan dengan tepat
     }
     ```

     ```go Go
     response, _ := client.Messages.New(ctx, params) // your existing request

     if response.StopReason == anthropic.StopReasonRefusal {
     	// Tangani penolakan dengan tepat
     }
     ```

     ```java Java
     Message response = client.messages().create(...);

     StopReason reason = response.stopReason().orElse(StopReason.END_TURN);
     if (reason.equals(StopReason.REFUSAL)) {
         // Tangani penolakan dengan tepat
     }
     ```

     ```php PHP
     $response = $client->messages->create(...);

     if ($response->stopReason === 'refusal') {
         // Tangani penolakan dengan tepat
     }
     ```

     ```ruby Ruby
     response = client.messages.create(...)

     if response.stop_reason == :refusal
       # Tangani penolakan dengan tepat
     end
     ```
   </CodeGroup>

4. **Tangani stop reason `model_context_window_exceeded`**

   Model Claude 4.5+ mengembalikan stop reason `model_context_window_exceeded` ketika pembuatan berhenti karena mencapai batas jendela konteks, bukan batas `max_tokens` yang diminta. Perbarui aplikasi Anda untuk menangani stop reason baru ini:

   <CodeGroup exclude="shell">
     ```python Python
     response = client.messages.create(...)

     if response.stop_reason == "model_context_window_exceeded":
         # Tangani batas jendela konteks dengan tepat
         pass
     ```

     ```typescript TypeScript
     const response = await client.messages.create(/* ... */);

     if (response.stop_reason === "model_context_window_exceeded") {
       // Tangani batas jendela konteks dengan tepat
     }
     ```

     ```csharp C#
     var response = await client.Messages.Create(...);

     if (response.StopReason?.Raw() == "model_context_window_exceeded")
     {
         // Tangani batas jendela konteks dengan tepat
     }
     ```

     ```go Go
     response, _ := client.Messages.New(ctx, params) // your existing request

     if response.StopReason == "model_context_window_exceeded" {
     	// Tangani batas jendela konteks dengan tepat
     }
     ```

     ```java Java
     Message response = client.messages().create(...);

     StopReason reason = response.stopReason().orElse(StopReason.END_TURN);
     if (reason.equals(StopReason.of("model_context_window_exceeded"))) {
         // Tangani batas jendela konteks dengan tepat
     }
     ```

     ```php PHP
     $response = $client->messages->create(...);

     if ($response->stopReason === 'model_context_window_exceeded') {
         // Tangani batas jendela konteks dengan tepat
     }
     ```

     ```ruby Ruby
     response = client.messages.create(...)

     if response.stop_reason == :model_context_window_exceeded
       # Tangani batas jendela konteks dengan tepat
     end
     ```
   </CodeGroup>

5. **Verifikasi penanganan parameter alat (newline di akhir)**

   Model Claude 4.5+ mempertahankan newline di akhir dalam parameter string pemanggilan alat yang sebelumnya dihapus. Jika alat Anda mengandalkan pencocokan string yang persis terhadap parameter pemanggilan alat, verifikasi bahwa logika Anda menangani newline di akhir dengan benar.

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4+ memiliki gaya komunikasi yang lebih ringkas dan langsung serta memerlukan arahan eksplisit. Tinjau [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

#### Perubahan tambahan yang direkomendasikan

* **Hapus header beta lama:** Hapus `token-efficient-tools-2025-02-19` dan `output-128k-2025-02-19`. Semua model Claude 4+ memiliki penggunaan alat hemat token bawaan dan header ini tidak berpengaruh.

### Daftar periksa migrasi (dari Claude Opus 4.5 atau lebih lama)

* Perbarui ID model ke `claude-opus-5`
* Terapkan semua [perubahan yang merusak untuk migrasi dari Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-5/migration-guide#opus-46-breaking-changes) (pemikiran diperpanjang dihapus, pemikiran aktif secara default, batas effort saat menonaktifkan pemikiran, parameter sampling dihapus, tampilan pemikiran dihilangkan secara default, tokenisasi diperbarui)
* **MERUSAK:** Hapus prefill pesan asisten (mengembalikan error 400); gunakan output terstruktur atau `output_config.format` sebagai gantinya
* **MERUSAK pada Opus 4.7:** Ganti `thinking: {type: "enabled", budget_tokens: N}` dengan `thinking: {type: "adaptive"}` ditambah [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) (mengembalikan 400 pada Opus 4.7)
* Verifikasi bahwa parsing JSON panggilan alat menggunakan parser JSON standar
* Hapus header beta `effort-2025-11-24` (parameter effort tidak memerlukannya)
* Hapus header beta `fine-grained-tool-streaming-2025-05-14`
* Hapus header beta `interleaved-thinking-2025-05-14` (pemikiran adaptif mengaktifkan pemikiran berselang-seling secara otomatis)
* Migrasikan `output_format` ke `output_config.format` (jika berlaku)
* Jika bermigrasi dari Claude 4.1 atau lebih lama: hapus `temperature`, `top_p`, dan `top_k` (nilai non-default mengembalikan 400 pada Opus 4.7)
* Jika bermigrasi dari Claude 4.1 atau lebih lama: perbarui versi alat (`text_editor_20250728`, `code_execution_20260521`)
* Jika bermigrasi dari Claude 4.1 atau lebih lama: tangani stop reason `refusal`
* Jika bermigrasi dari Claude 4.1 atau lebih lama: tangani stop reason `model_context_window_exceeded`
* Jika bermigrasi dari Claude 4.1 atau lebih lama: verifikasi penanganan parameter string alat untuk baris baru di akhir
* Jika bermigrasi dari Claude 4.1 atau lebih lama: hapus header beta lama (`token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`)
* Tinjau dan perbarui prompt dengan mengikuti [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
* Uji di lingkungan pengembangan sebelum deployment produksi

## Migrasi ke Claude Opus 5 dari Claude Sonnet 5

Claude Opus 5 dan Claude Sonnet 5 berbagi permukaan API yang sama: keduanya berjalan dengan [pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking) aktif secara default, keduanya menetapkan default [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) ke `high` pada Claude API dan Claude Code, keduanya menyediakan ["context window" (jendela konteks) 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default dengan [128k token output maksimum](https://platform.claude.com/docs/id/models/overview), dan keduanya tidak mendukung [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models). Pemikiran diperpanjang manual dan parameter sampling non-default mengembalikan error 400 pada kedua model, begitu pula prefill asisten.

### Perbarui nama model Anda

```python
model = "claude-sonnet-5"  # Before
model = "claude-opus-5"  # After
```

### Apa yang berubah

1. **Harga:** Claude Opus 5 dihargai $5 USD per juta token input dan $25 USD per juta token output. Claude Sonnet 5 dihargai $2/$10 USD per juta token input/output. Lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing) untuk harga lengkap.

2. **Menonaktifkan pemikiran dibatasi pada effort `high`:** Pada Claude Sonnet 5, `thinking: {type: "disabled"}` diterima pada level effort apa pun. Pada Claude Opus 5, ini hanya diterima pada level [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah; permintaan yang menggabungkan `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400, yang diberlakukan pada setiap permintaan. Audit permintaan yang menonaktifkan pemikiran sebelum Anda bermigrasi.

3. **Pesan sistem di tengah percakapan:** Claude Opus 5 menerima pesan `role: "system"` tepat setelah giliran pengguna dalam array `messages` (tunduk pada [aturan penempatan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)). Fitur ini tidak tersedia pada Claude Sonnet 5. Jika Anda memelihara jalur kode yang membangun ulang seluruh riwayat pesan untuk memperbarui instruksi, Anda dapat menyederhanakannya dan mempertahankan hit ["prompt cache" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya.

4. **Web fetch tidak tersedia:** Alat [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) tersedia pada Claude Sonnet 5 tetapi tidak pada Claude Opus 5.

### Daftar periksa migrasi

* Perbarui nama model dari `claude-sonnet-5` ke `claude-opus-5`.
* Audit permintaan yang menonaktifkan pemikiran: `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400 pada Claude Opus 5. Aktifkan kembali pemikiran atau turunkan effort ke `high` atau lebih rendah.
* Jika Anda menggunakan [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool), rencanakan alternatif: alat ini tidak tersedia pada Claude Opus 5.
* Jalankan ulang [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) terhadap Claude Opus 5 alih-alih menggunakan kembali hitungan yang diukur terhadap Claude Sonnet 5, dan tetapkan ulang baseline biaya dan latensi pada beban kerja Anda sendiri; harga per token berbeda.
