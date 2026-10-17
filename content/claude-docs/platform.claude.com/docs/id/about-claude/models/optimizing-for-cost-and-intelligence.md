---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence
fetched_at: 2026-10-17T02:19:22.559852Z
sha256: 578a200ffa56a54d801d848b601a8722d90d4c221f1eac95af710a03e7f0df2d
---

---
title: Mengoptimalkan biaya dan kecerdasan
url: https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence
description: Seimbangkan biaya dan kecerdasan di Claude Platform, dengan hasil terukur untuk caching prompt, effort, pilihan model, batas output, dan strategi multi-model.
---

Model yang paling mumpuni bisa terlalu mahal dalam skala besar, dan model yang paling murah bisa kurang memadai dari segi kualitas. Claude Platform memberi Anda kendali langsung atas "tradeoff" (kompromi) tersebut. Anda memilih model, tingkat "effort" (upaya), dan arsitektur untuk setiap permintaan, sehingga Anda dapat menempatkan beban kerja hampir di mana saja pada "cost-to-intelligence frontier" (frontier biaya-terhadap-kecerdasan).

Biaya dan kecerdasan biasanya digambarkan sebagai sebuah frontier, tempat yang satu dibeli dengan mengorbankan yang lain. Kelompok tuas pertama di halaman ini menggerakkan beban kerja menuju frontier tersebut dengan memangkas biaya tanpa menyentuh kualitas; hanya kelompok kedua yang bergerak di sepanjang frontier itu:

<Frame>
  ![Skema "cost-to-intelligence frontier" (frontier biaya-terhadap-kecerdasan): satu panah memangkas pengeluaran pada kualitas yang sama, panah lainnya menukar kualitas dengan biaya](https://platform.claude.com/docs/images/cost-intel/frontier.svg)
</Frame>

Tuas-tuas ini terbagi menjadi dua jenis:

* **Keuntungan gratis** memangkas pengeluaran tanpa menyentuh kualitas: "prompt caching" (caching prompt), "token hygiene" (kebersihan token), audit prompt terhadap model yang Anda jalankan, ["batch processing" (pemrosesan batch)](https://platform.claude.com/docs/id/build-with-claude/batch-processing) dengan diskon 50% untuk pekerjaan yang dapat menunggu hingga 24 jam, dan [batas pengeluaran workspace](https://platform.claude.com/docs/id/api/rate-limits#setting-lower-limits-for-workspaces) sebagai pengaman terakhir.
* **Tradeoff** menukar biaya dengan kecerdasan: pilihan model, effort, batas output dan anggaran sesi, jam waktu yang telah berlalu, dan arsitektur multi-model.

Setiap tuas disertai hasil terukur dan aturan kapan tuas tersebut menguntungkan. Dalam pengukuran Anthropic, caching prompt biasanya merupakan tuas terbesar. Tuas multi-model lebih sempit; model kedua diukur dalam dua bentuk, yaitu "advisor" (penasihat) dan "orchestrator" (orkestrator).

## Mulai di sini

Cocokkan situasi Anda dengan salah satu baris.

| Situasi Anda                                                     | Lakukan ini                                                                                                                                                                                                          | Di mana                                                                                                                                                                                                                                                                                     |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Beban kerja apa pun, model apa pun                               | Aktifkan caching prompt dan pangkas token yang tidak diperlukan; keduanya gratis                                                                                                                                     | [Cache konteks berulang](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#cache-repeated-context) · [Pangkas token](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens) |
| Seseorang menunggu di antara giliran                             | Hitung jeda di antara permintaan Anda, lalu pilih durasi cache dari tabel di bagian tersebut                                                                                                                         | [Pilih durasi cache](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#pick-the-cache-duration)                                                                                                                                                  |
| Biaya terlalu tinggi; kualitas sudah baik                        | Coba effort yang lebih rendah pada model yang Anda gunakan sekarang                                                                                                                                                  | [Setel effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort)                                                                                                                                                                    |
| Anda tidak menggunakan model terbaru                             | Lakukan upgrade; dalam pengukuran Anthropic, setiap model yang lebih baru menyelesaikan setidaknya sebanyak tugas yang diselesaikan model sebelumnya, biasanya dengan biaya lebih rendah per tugas yang diselesaikan | [Upgrade model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#upgrade-the-model)                                                                                                                                                             |
| Anda sedang memilih atau berganti model                          | Bandingkan berdasarkan biaya per tugas yang selesai, bukan per token                                                                                                                                                 | [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task)                                                                                                                                            |
| Pekerjaan bervolume tinggi dengan output yang dapat Anda periksa | Coba Claude Haiku 5.5 terlebih dahulu                                                                                                                                                                                | [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task)                                                                                                                                            |
| Kualitas belum cukup baik                                        | Jika Anda menurunkan effort, kembalikan; jika tidak, coba tingkat berikutnya di atasnya pada effort default-nya                                                                                                      | [Setel effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort) · [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task)                 |
| Percobaan berakhir dengan `stop_reason: max_tokens`              | Naikkan `max_tokens` menjadi 64.000: dalam pengujian Anthropic hanya 2 dari sekitar 14.000 giliran yang lebih panjang, dan biaya per tugas yang diselesaikan tetap kurang lebih sama                                 | [Tetapkan anggaran](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                                                                                                                                               |
| Anda dapat memeriksa output (tes, verifier)                      | Jalankan pada effort `low` dan jalankan ulang kegagalan pada `high`: dalam pengujian Anthropic, biayanya sekitar 40% lebih rendah daripada menjalankan semuanya pada `high`, dengan tingkat kelulusan yang sama      | [Jalankan ulang kegagalan](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#re-run-failures-at-higher-effort)                                                                                                                                   |
| Loop agen dengan beberapa run yang sangat mahal                  | Tetapkan anggaran sesi Claude Managed Agents dan batas pengeluaran workspace                                                                                                                                         | [Tetapkan anggaran](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                                                                                                                                               |
| Anda ingin run agen selesai lebih cepat                          | Beri tahu model bahwa waktu itu penting dan tunjukkan waktu yang telah berlalu: 7% hingga 47% lebih sedikit waktu dalam pengujian Anthropic, dengan pengorbanan beberapa poin skor                                   | [Tunjukkan waktu yang telah berlalu kepada model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#show-the-model-elapsed-time)                                                                                                                 |
| Model yang lebih murah hanya macet pada keputusan sulit          | Coba advisor. Advisor hanya dapat membantu ketika model Anda berkonsultasi dengannya; pertama-tama hitung harga model advisor saja pada effort rendah dan ukur tingkat konsultasinya                                 | [Strategi advisor](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#advisor-strategy-escalate-hard-decisions)                                                                                                                                   |
| Pekerjaan melebihi satu jendela konteks                          | Pecah pekerjaan dan serahkan bagian-bagiannya ke model berbiaya lebih rendah                                                                                                                                         | [Strategi orchestrator](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#orchestrator-strategy-delegate-bulk-work)                                                                                                                              |

Hasil ini berasal dari pengukuran internal Anthropic ([Benchmark yang dirujuk](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)) dan bersifat indikatif, bukan jaminan, jadi ukurlah pada beban kerja Anda sendiri dengan [metode empat langkah](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#measure-on-your-own-workload).

## Pangkas pengeluaran tanpa kehilangan kualitas

Caching prompt, kebersihan token, pemrosesan batch, dan audit prompt terhadap model Anda saat ini semuanya menurunkan apa yang Anda bayar tanpa menurunkan kualitas output. Dua catatan berlaku: pemrosesan batch menukar latensi dengan diskonnya, dan context editing, sebuah tuas kebersihan token, berbiaya lebih besar daripada yang dihematnya pada run yang diukur di bagian ini.

### Cache konteks berulang

#### Mengapa caching didahulukan

Aktifkan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) sebelum tuas lainnya, karena setiap giliran dari tugas agentik mengirim ulang seluruh percakapan yang terus bertambah: "system prompt" (prompt sistem), definisi alat, dan setiap giliran sebelumnya.

* Tugas dengan 40 giliran mengirim giliran pertamanya sebanyak 40 kali, sehingga biaya tugas tumbuh kira-kira sebanding dengan kuadrat jumlah giliran.
* Caching tidak menghentikan pengiriman ulang, tetapi setiap pengiriman ulang hanya berbiaya sekitar sepersepuluh (seperdua puluh pada Claude Opus 5.5 dan Claude Sonnet 5.5, seperempat puluh pada Claude Fable 5.1 dan Claude Mythos 5.1) dan diproses lebih cepat.
* Prefiks ditagih dengan [tarif cache-read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#pricing) alih-alih harga input, dan setiap giliran membayar tarif cache-write 1,25x hanya untuk bagian yang baru.

**Seperti apa kondisi yang baik.**

* Selama satu hari penuh lalu lintas nyata, loop agen membaca median 84% input mereka dari cache, dan 10% teratas di antaranya, baik untuk coding maupun bukan, membaca 94% atau lebih[17](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs).
* Jauh di dalam sebuah tugas, loop yang dibangun dengan baik membayar harga penuh untuk kurang dari 1% inputnya.
* Di bawah sekitar 80%, carilah sesuatu yang merusak cache (lihat [Apa yang merusak cache](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#what-breaks-the-cache)).

Di seluruh run yang diukur Anthropic, cache read secara rutin menjadi komponen tunggal terbesar dari biaya tugas, sehingga caching lebih berharga daripada sebagian besar keputusan pemilihan model. Anthropic menghitung biaya run DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dengan dan tanpa caching:

<Frame>
  ![Grafik, DeepResearch Bench II: caching memangkas Fable 5.1 dari $37,94 USD menjadi $6,89 USD per tugas; Sonnet 5, $3,20 USD menjadi $1,18 USD](https://platform.claude.com/docs/images/cost-intel/caching-repriced.svg)
</Frame>

Masa hidup default cache adalah 5 menit dan giliran loop agen berjarak beberapa detik, sehingga diskon berlaku untuk sebagian besar token di setiap giliran. Run pada grafik caching membaca 84% hingga 90% token input mereka dari cache.

Menghitung harga jumlah token yang tercatat dari run lain dengan cara yang sama, dengan setiap model pada effort default-nya, memberikan rata-rata biaya token per tugas tanpa caching (tidak satu pun dari run ini dijalankan dengan caching dimatikan):

| Benchmark                                                                                                                                                                                                                                                                                                           | Model             | Tanpa caching                 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ----------------------------- |
| SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)                                                                                                                                                                                                 | Claude Opus 5.5   | 3,3 kali biaya dengan caching |
| SWE-bench Pro                                                                                                                                                                                                                                                                                                       | Claude Sonnet 5.5 | 3,1 kali biaya dengan caching |
| Set tugas Claude Managed Agents[25](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), yang sesinya pendek                                                                                                                                                         | Claude Haiku 5.5  | 1,7 kali biaya dengan caching |
| Agen kecil yang melakukan triase laporan bug ([Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens))[16](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) | Claude Sonnet 5.5 | 7,3 kali biaya dengan caching |

Penghematan bervariasi sesuai jumlah giliran yang dibutuhkan sebuah tugas, karena loop yang lebih pendek membaca ulang lebih sedikit.

<Note>
  Pada Claude Haiku 5.5, [lakukan compaction pada sesi panjang](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#manage-the-context-lifecycle) di batas tugas, sebelum permintaannya melewati 100.000 token prompt. Permintaan yang prompt-nya lebih dari 100.000 token membayar 5 kali lipat untuk setiap tokennya, termasuk output. Pembacaan cache dan penulisan cache dihitung dalam 100.000 token tersebut, sehingga permintaan dengan prefiks ter-cache yang besar tetap bisa melewatinya. Lihat [Harga konteks panjang](https://platform.claude.com/docs/id/about-claude/pricing#long-context-pricing).
</Note>

#### Pilih durasi cache

Jika loop Anda menunggu seseorang di antara giliran, gunakan [durasi cache 1 jam](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration) begitu sekitar 1 dari 20 giliran terjadi setelah jeda antara 5 menit dan satu jam dan hanya sedikit jeda yang melebihi satu jam. Pada Claude Fable 5.1, Claude Opus 5.5, dan Claude Sonnet 5.5, menjaga cache 5 menit tetap hangat bisa lebih murah.

Durasi 1 jam lebih mahal untuk ditulis (2x harga input alih-alih 1,25x). Miss pada durasi mana pun menagih seluruh prefiks dengan harga tulis alih-alih harga baca.

Anthropic mengukur agen kecil yang melakukan triase laporan bug ([Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens)) dengan jeda yang disisipkan sebelum beberapa giliran untuk mensimulasikan penundaan dari seseorang[16](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs). Akurasi tetap berada dalam noise antar-run pada setiap pengaturan yang diukur. Anthropic juga mengukur permintaan tambahan yang menjaga cache 5 menit tetap hangat (permintaan keep-alive).

Untuk memutuskan, hitung jeda di antara permintaan berurutan dalam sebuah percakapan, lalu temukan baris Anda pada tabel berikut:

| Jeda di antara permintaan Anda                                                                                                      | Model                                 | Gunakan                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | -------------------------------------------------------------- |
| Giliran datang berjarak beberapa detik                                                                                              | Apa pun                               | Default 5 menit                                                |
| Sekitar 1 dari 20 jeda atau lebih berada antara 5 menit dan satu jam, dan hanya sedikit jeda yang melebihi satu jam                 | Apa pun                               | Durasi 1 jam                                                   |
| Jeda lebih dari satu jam sering terjadi: sekitar 60% atau lebih dari jeda Anda yang lebih dari 5 menit juga melewati satu jam       | Apa pun                               | Default 5 menit                                                |
| Hanya 1 atau 2 dari 20 jeda yang berada antara 5 menit dan satu jam, dan tidak ada yang berlangsung lebih dari sekitar setengah jam | Claude Opus 5.5 dan Claude Sonnet 5.5 | Cache 5 menit yang dijaga tetap hangat, alih-alih durasi 1 jam |
| Ada jeda sebelum setiap giliran                                                                                                     | Claude Opus 5.5 dan Claude Sonnet 5.5 | Durasi 1 jam                                                   |
| Jeda berlangsung beberapa menit                                                                                                     | Claude Fable 5.1                      | Cache 5 menit yang dijaga tetap hangat, alih-alih durasi 1 jam |
| Jeda berlangsung mendekati satu jam                                                                                                 | Claude Fable 5.1                      | Durasi 1 jam                                                   |

Pada Claude Haiku 5.5, gunakan baris "Apa pun". Permintaan keep-alive tidak diukur pada model ini. Berdasarkan harga daftar, bukan pengukuran, setiap permintaan keep-alive berbiaya dua kali lipat relatif terhadap harga input dibandingkan pada Claude Opus 5.5 dan Claude Sonnet 5.5: Claude Haiku 5.5 membaca cache pada tarif standar 0,1x, sedangkan kedua model tersebut pada 0,05x.

**Alasannya, baris demi baris.**

* **Model apa pun.**

  * **Giliran datang berjarak beberapa detik.** Tanpa jeda: default berbiaya sekitar 19% lebih rendah daripada pengaturan 1 jam pada Claude Sonnet 5.5, sekitar 15% hingga 18% lebih rendah pada Claude Opus 5.5.
  * **Sekitar 1 dari 20 jeda atau lebih.** Titik impas, yang dihitung dari jumlah token, adalah sekitar 1 dari 30 giliran pada Claude Sonnet 5.5 dan Claude Opus 5.5.
  * **Jeda lebih dari satu jam sering terjadi.** Pada model apa pun, jeda lebih dari satu jam membuat kedua durasi kedaluwarsa, dan pengaturan 1 jam kemudian menulis ulang prefiks dengan harga tulisnya yang lebih tinggi.

* **Claude Opus 5.5 dan Claude Sonnet 5.5**, yang pembacaan cache-nya berbiaya 0,05x harga input.

  * **Hanya 1 atau 2 dari 20 jeda.** Pada effort default, permintaan keep-alive berbiaya 8% hingga 13% lebih rendah daripada durasi 1 jam pada Claude Opus 5.5, 8% hingga 16% lebih rendah pada Claude Sonnet 5.5.
  * **Ada jeda sebelum setiap giliran.** Pada Claude Opus 5.5 dan Claude Sonnet 5.5, permintaan keep-alive berbiaya beberapa persen lebih tinggi daripada durasi 1 jam pada jeda 6 menit dan lebih dari 50% lebih tinggi pada jeda 45 menit.

* **Claude Fable 5.1**, yang [pembacaan cache](https://platform.claude.com/docs/id/about-claude/pricing#prompt-caching)-nya berbiaya 0,025x harga input.

  * **Jeda berlangsung beberapa menit.** Pada Claude Fable 5.1, permintaan keep-alive[19](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) berbiaya 13% hingga 20% lebih rendah daripada cache 1 jam, dengan 10% giliran dijeda maupun dengan jeda 6 menit sebelum setiap giliran.
  * **Jeda berlangsung mendekati satu jam.** Pada Claude Fable 5.1, hanya dengan jeda 45 menit sebelum setiap giliran cache 1 jam unggul, dengan selisih sekitar $0,12 USD pada sesi berisi 5 laporan bug.

Grafik berikut memplot biaya per sesi terhadap proporsi giliran yang dijeda pada Claude Sonnet 5.5:

<Frame>
  ![Grafik garis: biaya per sesi triase berdasarkan proporsi giliran setelah jeda; cache 1 jam lebih murah setelah sekitar 1 dari 30 giliran](https://platform.claude.com/docs/images/cost-intel/cache-ttl-sonnet-5-5.svg)
</Frame>

Grafik berikut menambahkan cache 5 menit yang dijaga tetap hangat oleh permintaan keep-alive, pada Claude Fable 5.1, Claude Opus 5.5, dan Claude Sonnet 5.5:

<Frame>
  ![Grafik biaya: keep-alive mengalahkan cache 1 jam pada Fable 5.1 di semua titik yang diplot; pada Opus 5.5 dan Sonnet 5.5 hanya jika sedikit giliran yang dijeda](https://platform.claude.com/docs/images/cost-intel/cache-keepalive-sonnet-5-5.svg)
</Frame>

**Yang perlu diketahui.**

* Aturan 1 dari 20 menyisakan margin di atas titik impas sekitar 1 dari 30 giliran. Pada 1 dari 20 giliran, pengaturan 5 menit dan 1 jam berbiaya kurang lebih sama pada Claude Sonnet 5.5, dalam variasi antar-run; pada 1 dari 10 giliran, pengaturan 5 menit berbiaya 54% lebih tinggi (referensi 16).
* Pada model selain Claude Sonnet 5.5 dan Claude Opus 5.5, harga menempatkan titik impas dalam rentang yang sama: setiap model saat ini menggunakan pengali cache-write yang sama, dan setiap model kecuali Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, dan Claude Sonnet 5.5 menggunakan harga baca yang sama.
* Angka keep-alive Claude Opus 5.5 dan Claude Sonnet 5.5 berasal dari permintaan yang dikirim dengan `max_tokens: 1`. Apakah permintaan `max_tokens: 0` menyegarkan entri cache yang sudah ada tidak diukur pada Claude Opus 5.5 (referensi 16).

Untuk menjaga cache tetap hangat:

1. Ambil permintaan sebelumnya, atur `max_tokens` ke 0, dan hapus `stream` jika diatur. Jangan ubah satu byte pun dari prefiks.
2. Kirim ulang header permintaan bersama body-nya. Tanpa header `anthropic-beta` dari permintaan asli, field yang dibatasi beta dalam body yang diputar ulang akan ditolak.
3. Kirim dalam 4 menit sejak awal permintaan sebelumnya, dan setiap 4 menit setelahnya. Hitung dari awal permintaan, karena [masa hidup 5 menit cache](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#how-prompt-caching-works) dimulai dari sana.

Itulah [permintaan pre-warming](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#pre-warming-the-cache): permintaan ini menyegarkan masa hidup cache, tidak mengembalikan output, dan berbiaya sedikit lebih tinggi daripada pembacaan cache. Begitu cache kedaluwarsa, permintaan berikutnya, baik keep-alive maupun bukan, menulis ulang prefiks dengan harga cache write[16](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs).

Permintaan `max_tokens: 0` ditolak dalam kasus berikut:

* Permintaan mengatur `thinking.type: "enabled"` (adaptive thinking default pada Claude Fable 5.1 tidak masalah), structured outputs, atau pilihan alat yang dipaksakan ([batasannya](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#limitations)). Pada beban kerja tersebut, gunakan durasi 1 jam sebagai gantinya.
* Permintaan membawa parameter tingkat atas `compaction`, jadi jangan kirim ulang permintaan compaction dari [compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand) sebagai permintaan keep-alive.

<CodeGroup exclude="shell:CLI, python, typescript, csharp, go, java, php, ruby">
  ```bash cURL
  # Dalam 4 menit sejak awal permintaan terakhir (waktu pembuatan dihitung
  # terhadap masa hidup cache), kirim ulang permintaan itu dengan max_tokens diatur ke
  # 0, tanpa stream (permintaan max_tokens: 0 tidak dapat streaming). Kirim header
  # yang sama dengan permintaan asli, termasuk header anthropic-beta apa pun.
  jq '.max_tokens = 0 | del(.stream)' last_request.json | \
    curl https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "content-type: application/json" \
      --data-binary @-
  ```
</CodeGroup>

#### Aktifkan caching

Penyiapannya hanya membutuhkan sedikit usaha. [Caching otomatis](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching) menempatkan breakpoint untuk Anda; jika tidak, [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill) yang disertakan dengan Claude Code dapat menambahkan caching ke integrasi yang sudah ada dari satu prompt, `/claude-api add prompt caching to this integration`. Pada kode yang menghasilkan pengukuran ini, skill tersebut menempatkan satu breakpoint pada blok system dan satu pada masing-masing dari dua giliran pengguna terbaru; [Breakpoint cache eksplisit](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#explicit-cache-breakpoints) menjelaskan di mana menempatkannya.

#### Apa yang merusak cache

Simpan teks per permintaan di giliran pengguna terbaru, setelah breakpoint cache terakhir, dan lakukan setiap perubahan yang membatalkan cache pada jeda alami, seperti permintaan pertama setelah compaction. Cache adalah pencocokan prefiks byte-exact atas permintaan secara berurutan (tools, lalu prompt sistem, lalu messages), sehingga perubahan di mana pun membatalkan semua yang ada setelahnya.

Taruhannya paling tinggi pada Claude Fable 5.1 dan Claude Mythos 5.1, di mana kerusakan cache menulis ulang prefiks dengan 1,25x harga input alih-alih membacanya dengan 0,025x. Tabel berikut menunjukkan biaya satu giliran yang rusak pada prefiks 100.000 token, dihitung dari harga daftar dengan cache 5 menit, bukan diukur:

| Model                                  | Satu giliran rusak | Pembacaan sebagai gantinya | Dibandingkan dengan pembacaan |
| -------------------------------------- | ------------------ | -------------------------- | ----------------------------- |
| Claude Fable 5.1 dan Claude Mythos 5.1 | $1,25 USD          | $0,025 USD                 | 50 kali                       |
| Claude Opus 5.5                        | $0,50 USD          | $0,02 USD                  | 25 kali                       |
| Claude Sonnet 5.5                      | $0,25 USD          | $0,01 USD                  | 25 kali                       |

Pada model saat ini lainnya, biayanya 12,5 kali lipat pembacaan.

**Yang perlu dilakukan.**

* Jangan letakkan apa pun yang berubah per permintaan, seperti timestamp atau posisi antrean, di depan prefiks yang stabil: hal itu mengubah setiap permintaan menjadi penulisan cache penuh. Dalam pengukuran pada model sebelumnya, baris status 25 token di bagian depan prompt sistem membuat run agen kecil yang melakukan triase laporan bug ([Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens)) berbiaya lebih tinggi daripada menjalankannya dengan caching dimatikan[18](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs).
* Halaman [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#what-invalidates-the-cache) mencantumkan perubahan yang membatalkan cache, seperti perubahan pada [`effort`](https://platform.claude.com/docs/id/build-with-claude/effort), konfigurasi thinking, prompt sistem, atau definisi alat. Mengubah format output membatalkan cache untuk percakapan tersebut (lihat [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#prompt-modification-and-token-costs)).
* Pada model terbaru, ubah instruksi dengan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages), yaitu pesan `{"role": "system"}` yang ditambahkan ke `messages`, alih-alih mengedit field tingkat atas `system`: prefiks yang ter-cache tetap utuh. Periksa halaman tersebut untuk mengetahui model mana yang mendukungnya. Perubahan effort per pesan juga membiarkan prefiks yang ter-cache tetap utuh, tetapi pada lebih sedikit model: [Mengubah effort di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/effort#changing-effort-mid-conversation) mencantumkannya.
* Setelah perubahan yang membatalkan cache, pastikan pembacaan cache tidak turun; jika turun, [diagnostik cache](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics) menunjukkan di mana prefiks menyimpang.

Anthropic mengukur waktu perubahan pada model sebelumnya, pada sesi panjang agen triase[18](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs). Dalam pengukuran tersebut, sesi berbiaya lebih tinggi ketika perubahan effort dan penambahan alat dilakukan di tengah sesi, atau pada permintaan yang memicu compaction, dibandingkan ketika dua perubahan yang sama dilakukan pada permintaan pertama setelah compaction. Akurasi berada dalam noise antar-run di setiap kasus.

Sesi tanpa perubahan berbiaya lebih tinggi daripada sesi yang diubah setelah compaction, tetapi bukan karena caching. Sesi tersebut berjalan pada effort default sepanjang waktu dan dua di antaranya melakukan compaction untuk kedua kalinya, sementara yang lain dimulai pada effort rendah (referensi 18):

<Frame>
  ![Grafik batang, biaya per sesi triase: $0,81 USD tanpa perubahan, $0,95 USD di tengah sesi, $0,92 USD saat "compaction" (pemadatan), $0,75 USD setelahnya](https://platform.claude.com/docs/images/cost-intel/compaction-timing.svg)
</Frame>

### Pangkas token input dan konteks

Sebagian besar permintaan agen membawa token yang tidak pernah memengaruhi jawaban. Memangkasnya jarang mengorbankan kualitas output, meskipun tidak semua tuas di sini menghasilkan penghematan saat diukur. Ada dua tempat yang perlu diperiksa:

* **Pemangkasan input.**

  * ["Dynamic filtering"](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#dynamic-filtering) (pemfilteran dinamis) pada alat web fetch mencegah boilerplate dari halaman yang diambil masuk ke konteks.
  * [Pengubahan ukuran gambar](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size) menyesuaikan ukuran input vision.
  * ["Tool search" (pencarian alat) dengan deferred loading](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool) memuat definisi alat hanya saat dibutuhkan (diukur nanti di bagian ini).
  * ["Programmatic tool calling"](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) (pemanggilan alat terprogram) memungkinkan Claude menjalankan beberapa panggilan alat dari kode sehingga hanya hasil yang telah difilter yang masuk ke konteks; dokumentasinya melaporkan 24% lebih sedikit token input pada benchmark pencarian agentik, dengan skor yang lebih tinggi.
  * [Mengelola konteks alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/manage-tool-context) membandingkan tool search, programmatic tool calling, caching prompt, dan context editing.

* **Siklus hidup konteks.** [Context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) membersihkan hasil alat yang sudah usang, dan [compaction otomatis](https://platform.claude.com/docs/id/build-with-claude/compaction-threshold) beserta ambang batasnya mencegah loop panjang membawa seluruh riwayatnya ke depan.

Tuas-tuas ini berinteraksi dengan cache dan satu sama lain, jadi nilailah berdasarkan efek bersihnya, dan gunakan [diagnostik cache](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics) untuk memastikan prefiks ter-cache Anda bertahan dari setiap perubahan.

Dalam pengukuran pada model sebelumnya[28](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), Anthropic menjalankannya pada agen triase issue yang mengerjakan 20 laporan bug nyata dengan tangkapan layar dari repositori publik, dan pada varian yang lebih panjang dari pekerjaan yang sama dengan 2,6 kali jumlah token. Dengan caching aktif, pemangkasan input (pengubahan ukuran gambar dan tool search) memangkas biaya kedua run lebih jauh lagi.

#### Tunda definisi alat yang tidak digunakan

Setiap definisi alat yang dilampirkan ke permintaan merupakan input di setiap giliran, dan beberapa server MCP dapat menambahkan hingga ratusan definisi.

Dalam pengukuran pada model sebelumnya[27](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), Anthropic menjalankan agen triase dengan dua alatnya sendiri ditambah katalog definisi alat nyata dari server MCP publik, dengan total hingga 502 alat, memuat semuanya atau menandai alat tambahan dengan `defer_loading` di balik [tool search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool):

<Frame>
  ![Grafik garis: dengan semua alat dimuat, biaya run naik dari $0,55 USD menjadi $1,02 USD pada 502 alat; "tool search" (pencarian alat) menjaganya di $0,56 USD](https://platform.claude.com/docs/images/cost-intel/tool-search.svg)
</Frame>

* Dengan setiap definisi dimuat, biaya run naik seiring bertambahnya katalog, mengikuti token skema pada setiap permintaan.
* Dengan tool search, biaya run tetap datar pada setiap ukuran katalog.
* Akurasi berada dalam rentang yang sama di kedua cara, dan model tidak pernah memanggil alat yang salah, sehingga pada skala ini katalog menghabiskan uang, bukan kebenaran.
* Pada model sebelumnya yang sama, dengan server MCP GitHub publik yang dilampirkan melalui [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector), menunda toolset-nya (`default_config: {defer_loading: true}`) memangkas biaya run dengan akurasi yang sama.

#### Jauhkan file data dari prompt

Ketika model harus melakukan komputasi atas sebuah tabel, unggah tabel tersebut dengan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) dan biarkan model mengkuerinya dengan [code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) alih-alih menempelkannya. Anthropic mengajukan 25 pertanyaan agregat[15](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) (penjumlahan, hitungan terfilter, group-by, dan filter tanggal) atas CSV publik 1.862 baris, dengan jawaban yang dihitung oleh pandas:

<Frame>
  ![Grafik sebar: file diunggah dengan code execution, 25 dari 25 benar dengan $0,40 USD; ditempelkan ke prompt, 7 dari 25 dengan $5,01 USD](https://platform.claude.com/docs/images/cost-intel/data-files.svg)
</Frame>

Jika ditempelkan ke prompt, tabel tersebut berukuran sekitar 91.000 token input di setiap permintaan, dan Claude Sonnet 5 menjawab 7 dari 25 pertanyaan dengan benar. Jika diunggah, dengan code execution, model menjawab ke-25 pertanyaan, dan run tersebut berbiaya sekitar seperdua belas. Claude Opus 5 menunjukkan pola yang sama.

#### Kelola siklus hidup konteks

Tuas konteks hanya menguntungkan pada sesi yang cukup panjang untuk membutuhkannya:

<Frame>
  ![Grafik batang berdasarkan panjang run: context editing menambah 73% pada run pendek; compaction menghemat 32% dan pruning 39% pada run panjang](https://platform.claude.com/docs/images/cost-intel/hygiene.svg)
</Frame>

Anthropic mengukur tuas-tuas ini pada model sebelumnya[28](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs):

* Pada run 20 issue, tuas-tuas tersebut menghemat sedikit atau tidak sama sekali, dan context editing membuat run berbiaya lebih tinggi.
* Pada run panjang, prune dan compaction sama-sama memangkas biaya, sementara context editing tidak mengubah apa pun.
* Prune adalah beberapa baris kode yang Anda tulis sendiri: di setiap batas tugas, ganti hasil alat besar yang sudah usang dengan ekstrak satu baris.
* Prune ter-cache dengan baik karena editannya berada di ekor percakapan, tempat tugas berikutnya toh akan menambahkan konten baru.
* Di sepanjang run, prune dan context editing ter-cache kurang lebih sama baiknya. Jika Anda menggunakan context editing, [bersihkan dalam beberapa batch besar](https://platform.claude.com/docs/id/build-with-claude/context-editing#context-editing-and-prompt-caching).

<Note>
  Pada Claude Fable 5.1, Claude Opus 5.5, Claude Sonnet 5.5, dan Claude Haiku 5.5, menulis ulang hasil alat sebelumnya [membatalkan setiap blok thinking setelahnya](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#prefix-check), jadi gunakan compaction sebagai gantinya. Prune diukur pada model sebelumnya tanpa [preserved thinking](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking); pada keempat model ini, [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) dan [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction) berjalan di server dan tidak membatalkan blok thinking.
</Note>

Prune, diadaptasi dari kode agen triase:

```python
import re

PRUNED = "[pruned at issue boundary]"


def prune_task_boundary(messages, tool_name_by_id, threshold=2000):
    """Call once per task boundary. Replaces large, stale search results with a one-line extract."""
    for message in messages:
        if message["role"] != "user" or not isinstance(message["content"], list):
            continue
        for block in message["content"]:
            if not (isinstance(block, dict) and block.get("type") == "tool_result"):
                continue
            if tool_name_by_id.get(block.get("tool_use_id")) != "search_issues":
                continue
            result_text = block.get("content")
            if not isinstance(result_text, str) or len(result_text) <= threshold:
                continue
            if result_text.startswith(PRUNED):
                continue  # already pruned on an earlier boundary
            # batasi hasil satu baris agar ekstraknya tetap pendek
            first_line = result_text.split("\n", 1)[0].strip()[:200]
            refs = re.findall(r"#(\d+)", result_text)[:5]
            extract = f"{PRUNED} {first_line}"
            if refs:
                extract += " kept refs: " + " ".join("#" + r for r in refs)
            block["content"] = extract
```

### Batch pekerjaan yang bisa menunggu

Arahkan setiap permintaan yang tidak ditunggu siapa pun melalui [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing), dan pertahankan jalur interaktif untuk sisanya. Batch API memberikan potongan 50% untuk setiap token dari sebuah permintaan, termasuk yang ter-cache, dengan imbalan hasil yang tiba kapan saja dalam 24 jam.

* Batching adalah tuas gratis terbesar kedua setelah caching untuk pekerjaan agen tanpa pengawasan: run evaluasi, backfill, dan pekerjaan terjadwal seperti run berulang dari agen triase issue dari [pengukuran pemangkasan token](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens).
* Batching dapat dikombinasikan dengan semua hal di halaman ini kecuali interaktivitas, tetapi tidak tersedia untuk sesi Claude Managed Agents, yang memang interaktif secara desain (lihat [harga Claude Managed Agents](https://platform.claude.com/docs/id/about-claude/pricing#claude-managed-agents-pricing)).

### Audit prompt terhadap model saat ini

Audit prompt terhadap model yang Anda jalankan sekarang, dan lakukan lagi setiap kali Anda berganti model: ini adalah keuntungan gratis.

* Setiap generasi model merespons prompt secara berbeda, sehingga sebuah prompt mengakumulasi teks yang ditulis untuk model yang tidak lagi Anda gunakan.
* Kasus yang umum adalah instruksi yang terlalu spesifik yang ditambahkan untuk mengompensasi model lama: "verify twice", "be maximally thorough", prosedur langkah demi langkah yang wajib, atau scratchpad penalaran buatan sendiri.
* Model yang lebih baru mengikuti instruksi semacam itu secara harfiah, menghasilkan putaran alat tambahan dan tulisan tambahan, sehingga tagihan naik tanpa peningkatan akurasi.

Audit ini hanya satu perintah. [Skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill) yang disertakan dengan Claude Code memiliki perintah `prompt-audit` yang membaca prompt dan kode permintaan sebuah proyek dan melaporkan apa yang ditulis untuk model yang berbeda. Kutipan yang dipersingkat ini menunjukkan perintah tersebut dijalankan terhadap prompt support-desk dan kode permintaan yang mengandung pola-pola tersebut:

```text wrap
$ claude
> /claude-api prompt-audit

10 findings. The three that matter most:

1. budget_tokens returns a 400 on Opus 5 (support_agent.py:10). This code
   does not run against its own target model. Everything else here is
   quality; this one is an outage.
2. The prompt contains two live contradictions. Line 15 says confirm before
   every refund, line 17 says process every eligible refund immediately.
   Line 19 asks for a complete recap *and* a three-sentence maximum.
3. The reasoning scaffold and the 6-step script fight the model rather than
   steer it. <scratchpad> + "reason step by step" is now a request
   parameter, not prose; the mandatory 6-step procedure plus "investigate
   fully even when the ticket looks simple" forces four tool calls on a
   "where's my package" ticket.
...
-After any refund or escalation, verify twice before submitting: re-fetch
-the order, re-check every figure in your reply against the fresh lookup,
-and review the reply a second time for errors.
+Before submitting a refund or an escalation, re-fetch the order and confirm
+every figure in your reply matches the fresh lookup.
```

Perintah tersebut kemudian mengusulkan pengeditannya sebagai diff (satu hunk ditampilkan) dan mencantumkan apa yang sengaja dibiarkannya: jendela refund, persyaratan nada, dan standar kualitas. Anda meninjau sebuah patch, bukan penulisan ulang.

Anthropic mengukur efeknya pada evaluasi support-desk[14](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), di dua migrasi antara model-model sebelumnya:

<Frame>
  ![Grafik sebar, evaluasi support-desk: prompt lama lebih mahal pada model baru; setelah "audited" (diaudit), lebih murah dan sama akuratnya](https://platform.claude.com/docs/images/cost-intel/prompt-audit.svg)
</Frame>

* Dari Claude Opus 4.8 ke Claude Opus 5, prompt yang ditulis untuk model lama berbiaya lebih tinggi per tiket pada model yang lebih baru, tanpa perubahan akurasi.
* Menjalankan audit atas prompt yang sama membuat Claude Opus 5 lebih murah daripada versi yang tidak diaudit sekaligus lebih akurat, sebuah peningkatan di luar noise.
* Dari Claude Sonnet 4.6 ke Claude Sonnet 5, audit memangkas biaya per tiket dengan akurasi yang sama.

Kedua jenis teks usang memiliki biaya yang berbeda:

<Frame>
  ![Grafik batang per pola lama: instruksi yang dipatuhi berlebihan memakan uang; pengaturan yang rusak dan aturan yang bertentangan memakan akurasi](https://platform.claude.com/docs/images/cost-intel/prompt-audit-patterns.svg)
</Frame>

* Instruksi yang diikuti model baru terlalu harfiah menghabiskan uang: menghapus "verify twice" memangkas biaya per tiket Claude Opus 5, dan menghapus "be maximally thorough" memangkasnya hampir sebanyak itu.
* Teks yang tidak lagi cocok dengan model justru mengorbankan akurasi: pengaturan thinking yang sudah dihentikan, aturan yang kontradiktif, dan scratchpad buatan sendiri yang bertentangan dengan thinking milik model masing-masing memulihkan akurasi pada Claude Opus 5 ketika dihapus.

Pola yang sama cenderung muncul dalam deskripsi alat dan skill, yang juga layak diaudit.

## Menukar biaya dengan kecerdasan

Tuas-tuas ini menentukan posisi satu model di antara biaya dan kecerdasan: pilihan model, effort, menjalankan ulang yang gagal dengan pengaturan lebih tinggi, anggaran dan batas yang menjadi ruang kerjanya, dan apakah model dapat melihat berapa banyak waktu yang telah berlalu. Mulailah dengan sapuan effort pada model Anda saat ini ([Setel effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort)). Dari biaya dan kemampuan terendah hingga tertinggi, model-model saat ini adalah Claude Haiku 5.5, Claude Sonnet 5.5, Claude Opus 5.5, dan Claude Fable 5.1 (model frontier); [Ikhtisar model](https://platform.claude.com/docs/id/models/overview) memuat jajaran lengkap dan harganya.

### Bandingkan model berdasarkan biaya per tugas

Bandingkan model berdasarkan "cost per completed task" (biaya per tugas yang selesai), bukan per token, karena yang Anda bayar adalah tugas yang selesai. Untuk sebagian besar beban kerja agen, mulailah dengan Claude Opus 5.5 pada effort default-nya (`medium`).

Model yang lebih mampu dapat menyelesaikan tugas dengan pekerjaan yang lebih sedikit, yang dapat mengimbangi sebagian besar selisih harga per token. Anthropic mengukur hal ini pada subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), yang skornya tidak dapat dibandingkan dengan leaderboard publik, dengan harga sesuai tagihan pelanggan:

<Frame>
  ![Diagram sebar, SWE-bench Pro: Claude Opus 5.5 pada effort rendah menyamai default Sonnet 5.5 dengan biaya sekitar 7% lebih tinggi per tugas yang diselesaikan](https://platform.claude.com/docs/images/cost-intel/cost-per-task-sonnet-5-5.svg)
</Frame>

Tabel berikut mencantumkan hasilnya:

| Benchmark                                                                                                                                        | Model             | Effort             | Skor                                                                                           | Biaya                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------- | ------------------ | ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)                       | Claude Sonnet 5.5 | `high` (default)   | 87,6% tugas diselesaikan                                                                       | $0,11 USD per tugas yang diselesaikan                                                                           |
| Subset SWE-bench Pro                                                                                                                             | Claude Opus 5.5   | `low`              | 87,4% tugas diselesaikan                                                                       | $0,12 USD per tugas yang diselesaikan                                                                           |
| Subset SWE-bench Pro                                                                                                                             | Claude Opus 5.5   | `medium` (default) | 92,8% tugas diselesaikan                                                                       | $0,22 USD per tugas yang diselesaikan                                                                           |
| Subset SWE-bench Pro                                                                                                                             | Claude Fable 5.1  | `high` (default)   | 92,3% tugas diselesaikan (satu run)                                                            | $1,19 USD per tugas yang diselesaikan                                                                           |
| Benchmark agentic-coding internal[11](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)         | Claude Opus 5.5   | `medium` (default) | 86,6%                                                                                          | $0,84 USD per percobaan                                                                                         |
| Benchmark agentic-coding internal                                                                                                                | Claude Fable 5.1  | `medium`           | 84,2% (satu run)                                                                               | $2,68 USD per percobaan                                                                                         |
| GPQA Diamond[9](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)                               | Claude Haiku 5.5  | `medium` (default) | Akurasi 85%, dibandingkan dengan 91% untuk masing-masing Claude Opus 5.5 dan Claude Sonnet 5.5 | Sekitar seperdua puluh biaya Claude Opus 5.5 per jawaban benar dan sekitar sepersepuluh biaya Claude Sonnet 5.5 |
| Set tugas Claude Managed Agents[25](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), 79 tugas | Claude Haiku 5.5  | `medium`           | 93% percobaan lulus (satu run)                                                                 | Sekitar $0,011 USD per percobaan yang lulus                                                                     |

**Yang perlu dilakukan.**

* Mulailah dengan Claude Opus 5.5 pada effort default-nya: pada subset SWE-bench Pro, model ini menyamai Claude Fable 5.1 pada default-nya, dalam noise antar-run, dengan sekitar seperlima biaya per tugas yang diselesaikan. Opus 5.5 dan Fable 5.1 sama-sama hampir menjenuhkan subset SWE-bench Pro. Gunakan Claude Fable 5.1 untuk penalaran yang menuntut dan pekerjaan agentik jangka panjang, atau ketika eval Anda pada Claude Opus 5.5 dengan effort yang lebih tinggi masih belum memadai.
* Di ujung lainnya, Claude Haiku 5.5 cocok untuk pekerjaan bervolume tinggi dan sensitif terhadap latensi dengan output yang dapat diperiksa.
* Hitung harga setiap kandidat dalam biaya per tugas yang selesai pada lalu lintas Anda sendiri, termasuk Claude Opus 5.5 pada effort default-nya dan model frontier pada effort yang dikurangi. Setiap harga token Claude Opus 5.5, termasuk pembacaan cache, dua kali lipat harga Claude Sonnet 5.5, tetapi pada subset SWE-bench Pro, Opus 5.5 pada `low` menyelesaikan porsi tugas yang kurang lebih sama dengan Sonnet 5.5 pada default-nya, dalam noise antar-run, dengan biaya sekitar 7% lebih tinggi per tugas yang diselesaikan.
* Peringkatnya berbalik tergantung beban kerja, dan tidak ada daftar harga yang memberi tahu Anda ke arah mana, jadi ukurlah pada beban kerja Anda sendiri. Pada loop riset yang panjang, Claude Fable 5.1 dapat melakukan lebih banyak pekerjaan, bukan lebih sedikit, sehingga biayanya per tugas lebih tinggi (DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)).
* Hitung harga bagian ekor beban kerja Anda, bukan mediannya: bandingkan model pada sepersepuluh tugas tersulit Anda, bukan tugas yang umum.

Tagihan ditentukan oleh tugas-tugas yang gagal diselesaikan oleh model yang lebih murah, karena tugas yang gagal tetap menagih token-nya, lalu percobaan ulangnya, lalu apa pun biaya kegagalan tersebut di tahap selanjutnya. Bagian ekor juga merupakan tempat uang dihabiskan bahkan ketika tidak ada yang gagal. Pada run WideSearch[1](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dengan 20 soal, dua soal menanggung 43% dari pengeluaran:

<Frame>
  ![Diagram batang 20 soal WideSearch yang diurutkan berdasarkan biaya: dua teratas menanggung 43% pengeluaran dan separuh termurah 10%](https://platform.claude.com/docs/images/cost-intel/tail.svg)
</Frame>

[Strategi multi-model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#combine-models) ada untuk menghabiskan kecerdasan frontier pada ekor tersebut tanpa membayar tarif frontier untuk sisanya.

### Upgrade model

Jika Anda tertinggal satu atau dua model, tuas termurah adalah string model. Dalam pengukuran Anthropic, setiap model yang lebih baru menyelesaikan setidaknya sebanyak tugas yang diselesaikan model sebelumnya, biasanya dengan biaya lebih rendah per tugas yang diselesaikan. Diagram ini memetakan model-model Claude terbaru pada subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), tempat setiap model dijalankan melalui penyiapan pengujian yang sama, dan pada Terminal-Bench 3[20](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs); tabel mencantumkan apa yang diubah oleh setiap peningkatan:

<Frame>
  ![Diagram: pada SWE-bench Pro, Opus 5.5 dan Sonnet 5.5 paling banyak memangkas biaya per tugas yang diselesaikan; pada Terminal-Bench 3, Opus turun menjadi $28 USD](https://platform.claude.com/docs/images/cost-intel/upgrade-ladder-sonnet-5-5.svg)
</Frame>

| Benchmark                                                                                                                              | Peningkatan                          | Effort                                           | Skor                                                                             | Biaya                                                                                                                         |
| -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------ | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)             | Claude Sonnet 4.6 ke Claude Sonnet 5 | Default                                          | 5 poin lebih tinggi                                                              | 16% lebih rendah per tugas yang diselesaikan                                                                                  |
| Subset SWE-bench Pro                                                                                                                   | Claude Sonnet 5 ke Claude Sonnet 5.5 | Default                                          | Sekitar 10 poin lebih tinggi                                                     | 87% lebih rendah per tugas yang diselesaikan; 85% lebih rendah dengan harga Claude Sonnet 5                                   |
| Subset SWE-bench Pro                                                                                                                   | Claude Opus 5 ke Claude Opus 5.5     | Default: `high` ke `medium`                      | Kurang lebih sama: 91,9% ke 92,8% tugas diselesaikan                             | 78% lebih rendah per tugas yang diselesaikan; sekitar 69% lebih rendah dengan harga Claude Opus 5                             |
| Subset SWE-bench Pro                                                                                                                   | Claude Fable 5 ke Claude Fable 5.1   | Default                                          | Skor kurang lebih sama                                                           | 43% lebih rendah per tugas yang diselesaikan                                                                                  |
| DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)            | Claude Fable 5 ke Claude Fable 5.1   | `high`                                           | 2 hingga 3 poin lebih tinggi pada 21 tugas yang tidak ada percobaannya terpotong | 46% lebih tinggi per tugas pada seluruh 50 tugas                                                                              |
| DeepResearch Bench II                                                                                                                  | Claude Fable 5 ke Claude Fable 5.1   | `low`                                            | 2 hingga 3 poin lebih tinggi pada 21 tugas yang tidak ada percobaannya terpotong | 94% lebih tinggi per tugas pada seluruh 50 tugas                                                                              |
| Terminal-Bench 3[20](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)                | Claude Opus 4.7 ke Claude Opus 4.8   | `high`                                           | Dari 7% menjadi 15% tugas diselesaikan                                           | Dari $183 USD menjadi $63 USD per tugas yang diselesaikan                                                                     |
| Terminal-Bench 3                                                                                                                       | Claude Opus 4.8 ke Claude Opus 5     | `high`                                           | Dari 15% menjadi 41% tugas diselesaikan                                          | Dari $63 USD menjadi $28 USD per tugas yang diselesaikan, penghematan 56%                                                     |
| Set tugas Claude Managed Agents[25](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) | Claude Haiku 4.5 ke Claude Haiku 5.5 | Sesuai penyajian; `medium` pada Claude Haiku 5.5 | Dari 62% menjadi 93% percobaan lulus, satu run per model                         | Dari $0,041 USD menjadi sekitar $0,010 USD dalam biaya token per percobaan; sekitar 84% lebih rendah per percobaan yang lulus |

**Kapan hal ini menguntungkan.**

* Ketika model lama sudah menyelesaikan sebagian besar tugas, biaya setiap percobaan menentukan penghematannya: pada subset SWE-bench Pro, Claude Opus 5.5 mendapat skor kurang lebih sama dengan Claude Opus 5 dengan biaya 78% lebih rendah per tugas yang diselesaikan.
* Ketika model lama sebagian besar gagal, tingkat kelulusan menentukan penghematannya: pada Terminal-Bench 3[20](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), peningkatan dari Claude Opus 4.8 ke Claude Opus 5 menaikkan tugas yang diselesaikan dari 15% menjadi 41% dan biayanya 56% lebih rendah per tugas yang diselesaikan.
* Ukur peningkatan pada beban kerja Anda sendiri sebelum berasumsi bahwa hal itu menghemat biaya. Penghematan tidak dijamin: pada DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), Claude Fable 5.1 lebih mahal per tugas daripada Claude Fable 5 karena model baru melakukan lebih banyak pekerjaan per tugas di sana, meskipun harga input dan output-nya sama dan pembacaan cache 4x lebih murah.
* Bandingkan berdasarkan biaya per tugas yang diselesaikan, bukan per token: teks yang sama membutuhkan sekitar 30% lebih banyak token pada Claude 4.7 dan model yang lebih baru, sehingga perbandingan per token secara inheren membuat model yang lebih baru tampak lebih mahal.

### Setel effort

Lakukan sapuan effort pada beban kerja Anda sendiri sebelum Anda menambahkan model kedua. Effort yang lebih rendah lebih murah dan sering kali lebih cepat, dan seberapa banyak akurasi yang dikorbankan bergantung pada tugasnya: pada coding jangka panjang, effort membeli akurasi, dan pada tugas riset effort membeli banyak akurasi dalam satu pengukuran dan tidak sama sekali dalam pengukuran lain. Parameter [`effort`](https://platform.claude.com/docs/id/build-with-claude/effort) mengatur seberapa banyak pemikiran, pemanggilan alat, dan verifikasi diri yang dilakukan model; `high` adalah default pada sebagian besar model, dan `medium` pada Claude Opus 5.5 dan Claude Haiku 5.5.

Tabel berikut mencantumkan pengukuran Anthropic pada dua benchmark dengan model-model saat ini; skor dan biaya tidak dapat dibandingkan antara kedua benchmark. Biaya dihitung per tugas, bukan per tugas yang diselesaikan seperti di [Bandingkan model berdasarkan biaya per tugas](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task). Setiap skor menggabungkan dua run pada SWE-bench Pro dan tiga run pada DeepResearch Bench II, kecuali selnya menyatakan lain:

| Benchmark                                                                                                                   | Model            | Effort             | Skor                                | Biaya per tugas |
| --------------------------------------------------------------------------------------------------------------------------- | ---------------- | ------------------ | ----------------------------------- | --------------- |
| Subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)  | Claude Opus 5.5  | `low`              | 87,4% tugas diselesaikan            | $0,11 USD       |
| Subset SWE-bench Pro                                                                                                        | Claude Opus 5.5  | `medium` (default) | 92,8% tugas diselesaikan            | $0,21 USD       |
| Subset SWE-bench Pro                                                                                                        | Claude Opus 5.5  | `high`             | 95,3% tugas diselesaikan            | $0,29 USD       |
| Subset SWE-bench Pro                                                                                                        | Claude Opus 5.5  | `xhigh`            | 96,7% tugas diselesaikan (satu run) | $0,74 USD       |
| DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) | Claude Fable 5.1 | `low`              | Skor rubrik 66%                     | $4,48 USD       |
| DeepResearch Bench II                                                                                                       | Claude Fable 5.1 | `high` (default)   | Skor rubrik 65%                     | $6,89 USD       |

Diagram berikut memetakan akurasi terhadap biaya per tugas untuk Claude Opus 5.5 pada subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs):

<Frame>
  ![Diagram garis akurasi terhadap biaya per tugas berdasarkan effort: curam dari low ke high untuk Claude Opus 5.5 pada SWE-bench Pro](https://platform.claude.com/docs/images/cost-intel/effort-sweep-opus-5-5-swe-bench-pro.svg)
</Frame>

Diagram berikut memetakan skor rubrik terhadap biaya per tugas untuk Claude Fable 5.1 pada DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs):

<Frame>
  ![Diagram garis, DeepResearch Bench II, skor rubrik terhadap biaya per tugas: pada Fable 5.1 effort yang lebih tinggi tidak menambah skor, hanya biaya](https://platform.claude.com/docs/images/cost-intel/effort-limit-repriced.svg)
</Frame>

**Yang perlu dilakukan.**

* Lakukan sapuan pada dua atau tiga tingkat effort pada sampel lalu lintas Anda sendiri, masing-masing dalam sesi terpisah: mengubah effort tingkat atas di tengah sesi [membatalkan cache](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#cache-repeated-context) dan mendistorsi perbandingan. Kurva tersebut adalah baseline yang harus dikalahkan oleh strategi multi-model apa pun ([langkah 2 dari pengukuran pada beban kerja Anda sendiri](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#measure-on-your-own-workload)).
* Pada coding jangka panjang, effort adalah tradeoff yang nyata, yang dapat diubah kembali menjadi penghematan dengan [menjalankan ulang kegagalan pada effort yang lebih tinggi](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#re-run-failures-at-higher-effort). Pada `medium`, Claude Sonnet 5.5 mendapat skor sekitar 7 poin lebih rendah daripada pada default-nya, `high`, pada subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dengan sekitar 59% biaya per tugas (masing-masing 2 run), dan mendapat skor 62,7% dibandingkan dengan 77,8% pada benchmark agentic-coding internal[11](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) (1 percobaan per tugas).
* Pada tugas riset, ukur model yang Anda rilis. Claude Fable 5.1 mendapat skor yang hampir sama dari `low` hingga `high` pada DeepResearch Bench II; Claude Opus 5.5 mendapat skor 13,3 poin lebih rendah pada `low` dibandingkan pada `medium` di DRACO[21](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs). Kedua hasil tersebut berasal dari model yang berbeda pada benchmark yang berbeda, sehingga keduanya menunjukkan bahwa jawabannya bervariasi, bukan alasannya.
* Pada `low`, tugas tipikal Claude Opus 5.5 memakan waktu 84% lebih singkat daripada pada `medium` di DRACO[21](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), 30% lebih singkat di HLE[22](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), dan 47% lebih singkat pada kumpulan soal fisika internal[23](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), dan skornya 13,3; 3,4; dan 14,0 poin lebih rendah (3, 3, dan 4 percobaan per tugas).
* Pada benchmark pencarian cacat internal untuk pekerjaan yang lebih besar dari satu jendela konteks[8](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), Claude Fable 5.1 membutuhkan 15,2; 17,5; dan 19,9 jam per run pada `low`, `medium`, dan `high` (masing-masing 3 run). Untuk menghemat waktu, bandingkan juga effort yang lebih rendah dengan dua perubahan di [Tunjukkan waktu yang telah berlalu kepada model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#show-the-model-elapsed-time): effort `low` menghemat lebih banyak waktu, dan perubahan tersebut mempertahankan lebih banyak skor.

### Jalankan ulang kegagalan pada effort yang lebih tinggi

Ketika hasil suatu tugas dapat diperiksa, kebijakan termurah pada kurva effort bukanlah pengaturan tetap: jalankan setiap tugas pada pengaturan rendah dan jalankan ulang hanya kegagalannya pada pengaturan yang lebih tinggi.

Anthropic menghitung kebijakan ini tugas demi tugas dari run effort Claude Opus 5.5 pada subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) di [Setel effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort):

<Frame>
  ![Diagram, SWE-bench Pro, Opus 5.5: effort low atau medium dengan kegagalan dijalankan ulang pada high menyamai effort tetap mana pun dengan biaya lebih rendah daripada high](https://platform.claude.com/docs/images/cost-intel/escalation-opus-5-5.svg)
</Frame>

Dalam tabel berikut, biaya run ulang turut menghitung percobaan murah yang gagal:

| Kebijakan                                        | Tugas diselesaikan | Biaya per tugas   |
| ------------------------------------------------ | ------------------ | ----------------- |
| `low`, kegagalan dijalankan ulang pada `high`    | Sekitar 97%        | Sekitar $0,17 USD |
| `medium`, kegagalan dijalankan ulang pada `high` | Sekitar 97%        | Sekitar $0,24 USD |
| Semuanya pada `high`                             | 95,3%              | $0,29 USD         |

* Pada `low`, 13% tugas gagal. Dengan tugas-tugas tersebut dijalankan ulang pada `high`, tingkat kelulusannya sedikit lebih tinggi daripada dengan semuanya pada `high`, dengan biaya sedikit di atas setengahnya.
* Gunakan kebijakan ini untuk penghematannya, bukan peningkatannya. Sebagian besar peningkatan kecil tersebut berasal dari percobaan kedua: menjalankan ulang kegagalan dari satu run `high` pada `high` menghasilkan skor yang kurang lebih sama, dengan biaya lebih besar.

Ada dua syarat. Pertama, Anda memerlukan sinyal kegagalan (di sini, tes milik benchmark itu sendiri); pemeriksa yang meloloskan pekerjaan buruk akan membiarkan kegagalan tersebut lolos. Kedua, setiap kegagalan pada percobaan pertama memakan waktu nyata senilai dua run, sehingga penghematan dibayar dengan latensi pada kegagalan.

### Tetapkan anggaran dan batas output

Dua kontrol melakukan dua tugas yang berbeda: anggaran sesi membatasi apa yang dapat dibelanjakan oleh satu sesi Claude Managed Agents, dan `max_tokens` membatasi panjang satu respons. Tetapkan masing-masing di tempat yang berlaku, dengan [batas pengeluaran workspace](https://platform.claude.com/docs/id/api/rate-limits#setting-lower-limits-for-workspaces) sebagai pengaman terakhir.

* **Anggaran sesi pada Claude Managed Agents** adalah penghentian keras atas pengeluaran. [Anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets) adalah batas dalam dolar atas [biaya daftar](https://platform.claude.com/docs/id/managed-agents/budgets#how-list-cost-is-measured) satu sesi, yang diukur oleh platform untuk token, pencarian web, dan waktu berjalan sesi.
* Pada batas tersebut, atau sedikit melewatinya, sesi dijeda dengan `stop_reason: budget_reached`; menaikkan anggaran akan melanjutkannya. Anggaran ini ditegakkan oleh platform dan berfungsi pada model apa pun yang memiliki harga daftar. Deployment menerapkan anggaran yang sama pada setiap sesi yang dimulainya.
* **`max_tokens`** membatasi satu respons, tanpa terlihat oleh model, sehingga menurunkannya tidak membuat model berhemat. Giliran yang membutuhkan ruang tersebut dibuang dan tetap ditagih. Mencoba ulang percobaan yang terpotong jarang membantu: pada batas yang sama sebagian besar gagal lagi, dan pada batas yang lebih tinggi Anda juga membayar percobaan yang terbuang.
* Tetapkan `max_tokens` ke 64.000 untuk pekerjaan agentik, atau ke 128.000, nilai maksimum, ketika satu percobaan yang terpotong berbiaya mahal. Lakukan [streaming respons](https://platform.claude.com/docs/id/build-with-claude/streaming) sebesar itu, perlakukan [`stop_reason: max_tokens`](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons#max-tokens) sebagai kegagalan, dan hemat biaya dengan effort, yang dapat dilihat oleh model.

Tabel berikut menunjukkan apa yang diselesaikan setiap model dan berapa biaya satu tugas yang diselesaikan pada setiap batas di benchmark tugas repositori internal[12](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), satu percobaan per tugas, setiap model pada effort default-nya. Baris pada 16.384 merupakan rata-rata dua run, dan baris lainnya masing-masing satu run:

| Model            | `max_tokens` | Percobaan yang dihentikan oleh batas | Tugas diselesaikan | Biaya per tugas yang diselesaikan |
| ---------------- | ------------ | ------------------------------------ | ------------------ | --------------------------------- |
| Claude Opus 5.5  | 16.384       | 25%                                  | 57,6%              | $5,38 USD dengan harga daftar     |
| Claude Opus 5.5  | 64.000       | 0%                                   | 75,6%              | $5,38 USD dengan harga daftar     |
| Claude Opus 5.5  | 128.000      | 0%                                   | 68,9%              | $5,94 USD dengan harga daftar     |
| Claude Fable 5.1 | 16.384       | 43%                                  | 36,3%              | $21,37 USD sesuai tagihan         |
| Claude Fable 5.1 | 64.000       | 0%                                   | 58,5%              | $21,53 USD sesuai tagihan         |
| Claude Fable 5.1 | 128.000      | 1%                                   | 60,0%              | $21,74 USD sesuai tagihan         |

**Claude Opus 5.5 pada 64.000 dan 128.000:** Tidak ada percobaan yang terpotong pada kedua batas tersebut, sehingga batas tidak menjelaskan mengapa kedua baris ini berbeda dalam tugas yang diselesaikan atau dalam biaya per tugas yang diselesaikan. Setiap baris adalah satu run.

Bandingkan batas-batas di dalam setiap model. Kedua model dijalankan dengan selang waktu satu bulan, dan biayanya dihitung dengan dasar harga yang berbeda.

Mintalah jawaban yang lebih singkat. Token output berharga lima kali token input pada Claude Haiku 5.5, Claude Sonnet 5.5, Claude Opus 5.5, dan Claude Fable 5.1, dan dalam loop agen setiap token yang ditulis model kembali sebagai input pada setiap giliran berikutnya, sehingga Anda membayar jawaban yang panjang berulang kali.

Dalam pengukuran pada model sebelumnya[26](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), Anthropic menjalankan agen kecil yang melakukan triase laporan bug ([Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens)) dengan tiga instruksi jawaban akhir, masing-masing tiga run, dengan model dan alat yang sama:

* Versi asli meminta dua baris.
* Varian yang lebih pendek meminta satu baris.
* Varian yang lebih panjang meminta memo dengan enam bagian berjudul.

Diagram berikut memetakan biaya per run dari setiap format:

<Frame>
  ![Diagram batang: format satu baris $0,49 USD per run, format dua baris asli $0,57 USD, memo $1,40 USD, semuanya 78% hingga 85% benar](https://platform.claude.com/docs/images/cost-intel/output-format.svg)
</Frame>

Ketiganya mendapat skor dalam rentang noise antar-run satu sama lain terhadap label yang benar, sehingga format-format tersebut jauh lebih berbeda dalam hal yang Anda bayar daripada dalam hal ketepatannya. Mintalah jawaban yang akan Anda baca, bukan jawaban yang tampak menyeluruh.

Pada tugas repositori internal[12](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), hampir setiap giliran selesai jauh di bawah batas 16.384 token. Giliran panjang yang jarang terjadi itulah yang dibeli oleh batas yang lebih tinggi:

<Frame>
  ![Diagram titik output per giliran untuk Opus 5.5 dan Fable 5.1: median beberapa ratus token, terpanjang 61k dan 128k, dibandingkan dengan batasnya](https://platform.claude.com/docs/images/cost-intel/max-tokens-ladder-opus-5-5.svg)
</Frame>

### Tunjukkan waktu yang telah berlalu kepada model

Agar agen selesai lebih cepat dan lebih murah, beri tahu agen bahwa waktu itu penting, dan tunjukkan waktu yang telah berlalu pada setiap permintaan. Dalam pengukuran Anthropic, kedua perubahan tersebut memangkas waktu satu agen Claude Opus 5.5 pada effort `medium` sebesar 47% dan biayanya sebesar 60% pada tugas riset DRACO[21](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) yang tipikal (median), dan skor rata-ratanya 4,1 poin lebih rendah.

Pada HLE[22](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dan kumpulan soal fisika internal[23](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), tugas tipikal memakan waktu 14% dan 7% lebih singkat, dan skor fisika 3,0 poin lebih rendah. Menurunkan effort ke `low` menghemat lebih banyak waktu dan biaya daripada perubahan tersebut, dan kehilangan lebih banyak skor (referensi 21). Periksa skor pada tugas Anda sendiri sebelum Anda menerapkan perubahan tersebut.

Untuk kode yang berfungsi, lihat resep Claude Cookbook [Multi-agent teams under latency pressure and budgets](https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/latency_multi_agent.ipynb), yang menerapkan kedua perubahan pada tim agen. Untuk menyatakan bahwa waktu itu penting di prompt sistem sebagai gantinya, lihat [Sinyal waktu untuk harness multiagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#time-signals-for-multi-agent-harnesses).

Diagram berikut juga memetakan sebuah tim, yang agen utamanya jarang memulai agen pembantu, dan satu agen pada effort `low`:

<Frame caption="Dengan kedua perubahan, satu agen memakan waktu 47% lebih singkat pada tugas DRACO yang tipikal, dan skor rata-ratanya 4,1 poin lebih rendah.">
  ![Diagram sebar dan batang, DRACO, HLE, dan set fisika: perubahan tersebut paling banyak menghemat waktu pada DRACO, dengan pengorbanan beberapa poin skor](https://platform.claude.com/docs/images/cost-intel/time-awareness.svg)
</Frame>

## Menggabungkan model

Sesuaikan satu model sebelum Anda menambahkan model kedua: lakukan sapuan effort pada model Anda saat ini terlebih dahulu, karena sebagian besar beban kerja berakhir di sana, dan jika sapuan menunjukkan adanya kesenjangan, hitung harga model yang lebih kuat saja pada effort rendah. Bangun pasangan model hanya jika pasangan tersebut mengalahkan seluruh kurva skor terhadap pengeluaran dari model tunggal. Hasil multi-model di halaman ini dinilai terhadap model yang sama pada effort yang lebih rendah dan terhadap model satu tingkat di bawahnya yang berjalan sendiri, yang merupakan perbandingan yang perlu dijalankan pada beban kerja Anda sendiri.

Tabel berikut membandingkan kedua strategi:

| Strategi         | Alur kontrol                                                      | Peran model frontier                      | Cocok untuk                                                                                                                     | Biaya frontier meningkat seiring                |
| ---------------- | ----------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **Advisor**      | Model lebih kecil menjalankan loop, mengeskalasi sesuai kebutuhan | Dikonsultasikan untuk rencana dan koreksi | Pekerjaan serial yang sulit di beberapa titik, seperti banyak giliran agen coding di antara beberapa keputusan nyata            | Seberapa sering executor macet                  |
| **Orchestrator** | Model frontier menjalankan loop, mendelegasikan pekerjaan massal  | Merencanakan, mengirim, dan mensintesis   | Pekerjaan yang menyebar ke file, dokumen, atau kasus yang benar-benar independen, terutama yang lebih dari satu jendela konteks | Seberapa sulit bagian-bagiannya dikoordinasikan |

### Strategi advisor: eskalasikan keputusan sulit

Advisor hanya dapat membantu ketika executor berkonsultasi dengannya.

Dalam pengukuran Anthropic pada model-model saat ini, satu-satunya pasangan yang executor-nya sering berkonsultasi, pada benchmark coding, mendapat skor 1,7 poin lebih tinggi daripada executor saja pada effort yang sama, di batas noise antar-run, dengan biaya sekitar 2,1 kali lipat. Ketika executor jarang atau tidak pernah berkonsultasi, pasangan tersebut mendapat skor dalam batas noise antar-run dari executor saja, atau lebih rendah.

Untuk mengaktifkannya, tambahkan [alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool), sebuah fitur beta, ke permintaan Anda. Pada Claude Managed Agents, [berikan advisor kepada sesi](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor). Untuk Claude Code, lihat [mengeskalasikan keputusan sulit dengan alat advisor](https://code.claude.com/docs/en/advisor).

<Frame>
  ![Diagram strategi advisor: model executor menjalankan loop utama dan memanggil advisor Claude Fable 5.1 sesuai kebutuhan](https://platform.claude.com/docs/images/model-routing-advisor-strategy.svg)
</Frame>

Tabel berikut membandingkan setiap pasangan dengan executor-nya saja pada effort yang sama:

| Benchmark                                                                                                                                | Skor                                                            | Biaya                                                                                            | Advisor dikonsultasikan                                                                                               |
| ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| Benchmark agentic-coding internal[11](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) | 90,1%, 1,7 poin di atas executor saja, di batas noise antar-run | $2,92 USD per percobaan, sekitar 2,1 kali executor saja                                          | Sekitar 1,4 kali per percobaan; 4% percobaan tidak menerima saran                                                     |
| GPQA Diamond[9](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)                       | Dalam batas noise antar-run dari executor saja                  | 12% lebih tinggi per pertanyaan untuk Claude Haiku 5.5, 25% lebih tinggi untuk Claude Sonnet 5.5 | Tidak pada satu pun dari 198 pertanyaan, dalam masing-masing dua run; tidak ada prompt sistem yang meminta konsultasi |
| Chartography[13](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)                      | 61,7, 7 poin di bawah executor saja dan di luar noise antar-run | Kurang lebih sama dengan executor saja                                                           | Pada 1 dari 300 tugas                                                                                                 |

* **Benchmark agentic-coding internal.** Claude Opus 5.5 pada `high`, dengan advisor Claude Fable 5.1.
* **GPQA Diamond.** Claude Haiku 5.5 atau Claude Sonnet 5.5 pada default masing-masing model (`medium` dan `high`), dengan advisor Claude Opus 5.5.
* **Chartography.** Claude Opus 5.5 pada `low`, dengan advisor Claude Fable 5.1.

Advisor hanya dapat menyerahkan kemampuan yang tidak dimiliki executor: pada GPQA Diamond, Claude Sonnet 5.5 saja menyamai Claude Opus 5.5 saja di 91% dengan penolakan dihitung sebagai salah, tetapi hanya karena Opus 5.5 menolak enam pertanyaan biologi per run dibandingkan dengan satu pertanyaan oleh Sonnet 5.5. Pada pertanyaan yang dijawab masing-masing, Opus 5.5 unggul sekitar 2 poin.

Pada benchmark coding, peningkatan dari pasangan tersebut berada di batas noise antar-run, dan posisinya kurang lebih berada pada kurva effort Claude Opus 5.5 sendiri, sehingga advisor membeli kurang lebih apa yang dihasilkan oleh effort yang lebih tinggi. Diagram berikut memetakan pasangan tersebut terhadap kurva itu dan kurva Claude Fable 5.1 dari bulan Agustus:

<Frame>
  ![Benchmark coding: Opus 5.5 pada high dengan advisor Fable 5.1 memperoleh 1,7 poin dengan 2,1 kali biaya, dekat dengan kurva effort-nya](https://platform.claude.com/docs/images/cost-intel/internal-coding-advisor-opus-5-5.svg)
</Frame>

**Yang perlu dilakukan.**

* Ukur tingkat konsultasi pada tugas Anda sendiri. Definisi alat advisor, sekitar 1.000 token prompt per permintaan, menambah biaya bahkan ketika executor tidak pernah berkonsultasi. Dengan [caching prompt](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#cache-repeated-context), loop agen multi-giliran membayar definisi tersebut dengan harga pembacaan cache setelah permintaan pertama, sehingga overhead ini paling berpengaruh untuk tugas singkat dengan satu permintaan.
* Jika executor jarang berkonsultasi, lihat [Prompting untuk tugas coding dan agen](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#prompting-for-coding-and-agent-tasks) untuk prompt sistem yang meminta konsultasi, dan ukur lagi setelah Anda menambahkannya. Pada 20 soal SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), prompt yang disarankan tidak membuat perbedaan yang jelas untuk Claude Sonnet 5.5.
* Kembalikan effort executor jika tingkat konsultasi anjlok. Dalam pengukuran pada model-model sebelumnya, satu pasangan yang berkonsultasi pada sebagian besar tugas pada effort default hanya berkonsultasi pada sedikit tugas ketika effort diturunkan, lalu mendapat skor di bawah executor saja (SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)).
* Periksa ulang pada setiap rilis model, karena rilis menggeser kesenjangan kemampuan maupun rasio harga.

### Strategi orchestrator: delegasikan pekerjaan massal

Delegasi menghemat biaya hanya dalam dua situasi, dalam pengukuran dengan worker pada Claude Sonnet 5, model sebelumnya:

* Pekerjaan rutin dengan ekor biaya yang panjang (bagian mudah dari BrowseComp[4](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs))
* Pekerjaan yang lebih besar dari satu jendela konteks (benchmark pencarian cacat internal[8](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs))

Ketika pekerjaan berupa satu rantai yang saling bergantung, atau muat dalam satu konteks tanpa ekor biaya yang panjang, model orchestrator saja pada effort yang lebih rendah lebih unggul dalam setiap kasus yang diukur, juga pada model-model sebelumnya (kumpulan BrowseComp yang lebih sulit dan DeepWideSearch[6](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)); penelitian eksternal independen melaporkan pola yang sama[5](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs).

Untuk membangun orchestrator, gunakan [orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) di Claude Managed Agents: konfigurasikan agen orchestrator dan agen worker yang dapat dipanggilnya, masing-masing dengan modelnya sendiri.

<Frame>
  ![Diagram strategi orchestrator: model frontier menyebarkan subtugas ke tiga model worker berbiaya lebih rendah](https://platform.claude.com/docs/images/model-routing-orchestrator-strategy.svg)
</Frame>

[Matriks pemilihan model](https://platform.claude.com/docs/id/about-claude/models/choosing-a-model#model-selection-matrix) mencantumkan Claude Haiku 5.5 untuk tugas sub-agen; sebelum Anda menggunakannya sebagai worker, [ukur pada beban kerja Anda sendiri](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#measure-on-your-own-workload).

Diagram berikut memetakan konfigurasi benchmark pencarian cacat berdasarkan biaya dan skor:

<Frame>
  ![Diagram, benchmark pencarian cacat: orchestrator berbiaya sekitar setengah dari Fable 5.1 saja pada effort apa pun dan skornya 10 hingga 12 poin lebih rendah](https://platform.claude.com/docs/images/cost-intel/corpus-pareto.svg)
</Frame>

**Yang perlu dilakukan.**

* **Pekerjaan rutin dengan ekor biaya yang panjang:** ukur kasus ini terlebih dahulu, untuk akurasi maupun biaya. Pengukuran yang mendasarinya hanya mencakup soal-soal yang dijawab dengan benar oleh konfigurasi yang didelegasikan di setiap run (referensi 4).
* **Pekerjaan yang lebih besar dari satu jendela konteks:** delegasikan partisi kepada worker. Menurunkan effort tidak dapat membantu, karena tagihannya adalah pembacaan itu sendiri: pada benchmark pencarian cacat[8](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), Claude Fable 5.1 saja berbiaya $468 USD hingga $552 USD per run di ketiga pengaturan effort-nya dan memakan waktu 15 hingga 20 jam. Dengan worker dari model sebelumnya, delegasi lebih murah dan selesai lebih cepat, dengan skor yang lebih rendah.

## Ukur pada beban kerja Anda sendiri

Ukur pada beban kerja Anda sendiri: angka-angka di halaman ini mencerminkan harga daftar pada saat pengukuran dan akan bergeser seiring perubahan model dan harga. Tingkat eskalasi Anda, seberapa rapi tugas terbagi, dan panjang transkrip juga ikut menggesernya. Metodenya tetap sama:

1. Ambil beberapa tugas dari log produksi, dengan bobot seperti lalu lintas nyata, dan [tulis pemeriksaan hasil](https://platform.claude.com/docs/id/test-and-evaluate/develop-tests) untuk masing-masing: tes lulus, tiket ditutup, jumlah baris benar. Catat biaya per tugas di samping skornya.
2. Buat baseline tingkatan model di berbagai tingkat effort, bukan hanya default, dan plot skor terhadap pengeluaran. Konfigurasi multi-model harus mengalahkan seluruh kurva model tunggal.
3. Jika kurva menunjukkan kesenjangan yang tidak dapat ditutup oleh effort, tambahkan strategi multi-model yang sesuai dan jalankan ulang rangkaian tes.
4. Jalankan pemenangnya dalam mode bayangan pada sebagian lalu lintas sebelum peralihan, lalu biarkan rangkaian tes tetap berjalan.

**Cara menghitung harga sebuah tugas.** `usage` pada setiap respons memiliki lima jumlah token yang dikenai harga. Hitung masing-masing dengan tarifnya sendiri: input tanpa cache, penulisan cache 5 menit dan 1 jam pada 1,25x dan 2x harga input, pembacaan cache, dan output. Jumlahkan semuanya di seluruh permintaan dalam tugas tersebut ([Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api) melaporkan agregatnya). Pada Claude Haiku 5.5, hitung harga setiap permintaan dengan tarif untuk panjang prompt-nya, termasuk pembacaan dan penulisan cache (lihat [Harga konteks panjang](https://platform.claude.com/docs/id/about-claude/pricing#long-context-pricing)).

Contoh berikut menghitung biaya satu permintaan dengan harga daftar Claude Opus 5.5. Ubah ketiga harga tersebut untuk model lain:

<CodeGroup>
  ```bash cURL
  INPUT_PER_MTOK=4.00 # Claude Opus 5.5
  CACHE_READ_PER_MTOK=0.20 # 0.05x the input price on Claude Opus 5.5; the multiplier differs by model
  OUTPUT_PER_MTOK=20.00

  response=$(curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }')

  cost=$(jq -r --argjson in_price "$INPUT_PER_MTOK" --argjson read_price "$CACHE_READ_PER_MTOK" --argjson out_price "$OUTPUT_PER_MTOK" '
    .usage
    | (.input_tokens * $in_price
       + (.cache_creation.ephemeral_1h_input_tokens // 0) * $in_price * 2.00  # 1-hour cache write
       + (.cache_creation.ephemeral_5m_input_tokens // 0) * $in_price * 1.25  # 5-minute cache write
       + (.cache_read_input_tokens // 0) * $read_price                   # cache read
       + .output_tokens * $out_price) / 1e6
  ' <<<"$response")
  printf 'Request cost: $%.6f\n' "$cost"
  ```

  ```bash CLI
  INPUT_PER_MTOK=4.00 # Claude Opus 5.5
  CACHE_READ_PER_MTOK=0.20 # 0.05x the input price on Claude Opus 5.5; the multiplier differs by model
  OUTPUT_PER_MTOK=20.00

  USAGE=$(ant messages create \
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}' \
    --transform usage)

  COST=$(jq -r --argjson in_price "$INPUT_PER_MTOK" --argjson read_price "$CACHE_READ_PER_MTOK" --argjson out_price "$OUTPUT_PER_MTOK" '
    (.input_tokens * $in_price
      + (.cache_creation.ephemeral_1h_input_tokens // 0) * $in_price * 2.00  # 1-hour cache write
      + (.cache_creation.ephemeral_5m_input_tokens // 0) * $in_price * 1.25  # 5-minute cache write
      + (.cache_read_input_tokens // 0) * $read_price                   # cache read
      + .output_tokens * $out_price) / 1e6
  ' <<<"$USAGE")
  printf 'Request cost: $%.6f\n' "$COST"
  ```

  ```python Python
  INPUT_PER_MTOK = 4.00  # Claude Opus 5.5
  # 0,05x harga input pada Claude Opus 5.5; pengali berbeda per model
  CACHE_READ_PER_MTOK = 0.20
  OUTPUT_PER_MTOK = 20.00

  client = anthropic.Anthropic()
  response = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  usage = response.usage
  cache_writes = usage.cache_creation
  writes_1h = cache_writes.ephemeral_1h_input_tokens if cache_writes else 0
  writes_5m = cache_writes.ephemeral_5m_input_tokens if cache_writes else 0
  cost = (
      usage.input_tokens * INPUT_PER_MTOK
      # Penulisan cache 1 jam ditagih 2x harga input, 5 menit 1,25x; pembacaan dengan harga baca cache.
      + writes_1h * INPUT_PER_MTOK * 2.0
      + writes_5m * INPUT_PER_MTOK * 1.25
      + (usage.cache_read_input_tokens or 0) * CACHE_READ_PER_MTOK
      + usage.output_tokens * OUTPUT_PER_MTOK
  ) / 1_000_000
  print(f"Request cost: ${cost:.6f}")
  ```

  ```typescript TypeScript
  const INPUT_PER_MTOK = 4.0; // Claude Opus 5.5
  const CACHE_READ_PER_MTOK = 0.2; // 0.05x the input price on Claude Opus 5.5; the multiplier differs by model
  const OUTPUT_PER_MTOK = 20.0;

  const client = new Anthropic();
  const response = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  });
  const usage = response.usage;
  const cost =
    (usage.input_tokens * INPUT_PER_MTOK +
      (usage.cache_creation?.ephemeral_1h_input_tokens ?? 0) * INPUT_PER_MTOK * 2 + // 1-hour cache write
      (usage.cache_creation?.ephemeral_5m_input_tokens ?? 0) * INPUT_PER_MTOK * 1.25 + // 5-minute cache write
      (usage.cache_read_input_tokens ?? 0) * CACHE_READ_PER_MTOK + // cache read
      usage.output_tokens * OUTPUT_PER_MTOK) /
    1_000_000;
  console.log(`Request cost: $${cost.toFixed(6)}`);
  ```

  ```csharp C#
  const double InputPerMtok = 4.00; // Claude Opus 5.5
  const double CacheReadPerMtok = 0.20; // 0.05x the input price on Claude Opus 5.5; the multiplier differs by model
  const double OutputPerMtok = 20.00;

  AnthropicClient client = new();
  var response = await client.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],
      }
  );
  var usage = response.Usage;
  double cost =
      (
          usage.InputTokens * InputPerMtok
          + (usage.CacheCreation?.Ephemeral1hInputTokens ?? 0) * InputPerMtok * 2.00 // 1-hour cache write
          + (usage.CacheCreation?.Ephemeral5mInputTokens ?? 0) * InputPerMtok * 1.25 // 5-minute cache write
          + (usage.CacheReadInputTokens ?? 0) * CacheReadPerMtok // cache read
          + usage.OutputTokens * OutputPerMtok
      ) / 1_000_000;
  Console.WriteLine($"Request cost: ${cost:F6}");
  ```

  ```go Go
  const (
  	inputPerMTok     = 4.00 // Claude Opus 5.5
  	cacheReadPerMTok = 0.20 // 0.05x the input price on Claude Opus 5.5; the multiplier differs by model
  	outputPerMTok    = 20.00
  )

  // ...
  	client := anthropic.NewClient()

  	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5_5,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	usage := response.Usage
  	cost := (float64(usage.InputTokens)*inputPerMTok +
  		float64(usage.CacheCreation.Ephemeral1hInputTokens)*inputPerMTok*2.00 + // 1-hour cache write
  		float64(usage.CacheCreation.Ephemeral5mInputTokens)*inputPerMTok*1.25 + // 5-minute cache write
  		float64(usage.CacheReadInputTokens)*cacheReadPerMTok + // cache read
  		float64(usage.OutputTokens)*outputPerMTok) / 1_000_000
  	fmt.Printf("Request cost: $%.6f\n", cost)
  ```

  ```java Java
  static final double INPUT_PER_MTOK = 4.00; // Claude Opus 5.5
  static final double CACHE_READ_PER_MTOK = 0.20; // 0.05x the input price on Claude Opus 5.5; the multiplier differs by model
  static final double OUTPUT_PER_MTOK = 20.00;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .build());

      Usage usage = response.usage();
      long writes1h = usage.cacheCreation().map(CacheCreation::ephemeral1hInputTokens).orElse(0L);
      long writes5m = usage.cacheCreation().map(CacheCreation::ephemeral5mInputTokens).orElse(0L);
      double cost = (usage.inputTokens() * INPUT_PER_MTOK
          + writes1h * INPUT_PER_MTOK * 2.00 // 1-hour cache write
          + writes5m * INPUT_PER_MTOK * 1.25 // 5-minute cache write
          + usage.cacheReadInputTokens().orElse(0L) * CACHE_READ_PER_MTOK // cache read
          + usage.outputTokens() * OUTPUT_PER_MTOK) / 1_000_000;
      IO.println("Request cost: $%.6f".formatted(cost));
  }
  ```

  ```php PHP
  const INPUT_PER_MTOK = 4.00; // Claude Opus 5.5
  const CACHE_READ_PER_MTOK = 0.20; // 0.05x the input price on Claude Opus 5.5; the multiplier differs by model
  const OUTPUT_PER_MTOK = 20.00;

  $client = new Client();
  $response = $client->messages->create(
      model: 'claude-opus-5-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  );
  $usage = $response->usage;
  $cost = (
      $usage->inputTokens * INPUT_PER_MTOK
      + ($usage->cacheCreation?->ephemeral1hInputTokens ?? 0) * INPUT_PER_MTOK * 2.00 // 1-hour cache write
      + ($usage->cacheCreation?->ephemeral5mInputTokens ?? 0) * INPUT_PER_MTOK * 1.25 // 5-minute cache write
      + ($usage->cacheReadInputTokens ?? 0) * CACHE_READ_PER_MTOK // cache read
      + $usage->outputTokens * OUTPUT_PER_MTOK
  ) / 1_000_000;
  printf("Request cost: \$%.6f\n", $cost);
  ```

  ```ruby Ruby
  INPUT_PER_MTOK = 4.00 # Claude Opus 5.5
  CACHE_READ_PER_MTOK = 0.20 # 0.05x the input price on Claude Opus 5.5; the multiplier differs by model
  OUTPUT_PER_MTOK = 20.00

  client = Anthropic::Client.new
  response = client.messages.create(
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  )
  usage = response.usage
  cost = (
    usage.input_tokens * INPUT_PER_MTOK +
    usage.cache_creation&.ephemeral_1h_input_tokens.to_i * INPUT_PER_MTOK * 2.00 + # 1-hour cache write
    usage.cache_creation&.ephemeral_5m_input_tokens.to_i * INPUT_PER_MTOK * 1.25 + # 5-minute cache write
    usage.cache_read_input_tokens.to_i * CACHE_READ_PER_MTOK + # cache read
    usage.output_tokens * OUTPUT_PER_MTOK
  ) / 1_000_000
  puts format("Request cost: $%.6f", cost)
  ```
</CodeGroup>

**Apa yang perlu diperiksa.**

* **Porsi pembacaan cache.** Dalam loop agen, sebagian besar token input seharusnya berupa pembacaan cache. Jika `cache_read_input_tokens` kecil dibandingkan `input_tokens` ditambah `cache_creation_input_tokens`, periksa apakah caching aktif dan apakah prefiks tetap sama di antara permintaan.
* **Alat advisor dan compaction.** Ketika [alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#usage-and-billing) atau ["compaction" (pemadatan)](https://platform.claude.com/docs/id/build-with-claude/compaction-threshold#understanding-usage) diaktifkan, sebagian token hanya dilaporkan di `usage.iterations` dan tidak di total tingkat atas. Jumlahkan dari `usage.iterations` sebagai gantinya, dan hitung harga entri `advisor_message` dengan tarif model advisor.

Tabel berikut mencantumkan tuas-tuas penghematan sesuai urutan untuk dicoba. Angka-angkanya berasal dari pengujian Anthropic sendiri; setiap bagian yang ditautkan beserta referensinya menyebutkan model dan metodenya:

| Tuas                                         | Penghematan dalam pengujian Anthropic                                                                                                                 | Dampak pada kualitas                                                                                                  | Latensi                                                                                                                          | Lokasi                                                                                                                                                                                  |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Caching prompt                               | Biaya turun dengan faktor 2,7 hingga 5,5 pada agen riset, dan sebesar 83% hingga 86% pada agen triase kecil                                           | Tidak ada                                                                                                             | Lebih cepat                                                                                                                      | [Cache konteks berulang](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#cache-repeated-context)                                           |
| Durasi cache 1 jam                           | Dengan 1 dari 10 giliran setelah jeda, default 5 menit berbiaya 54% lebih mahal; dengan 1 dari 20, kurang lebih sama                                  | Tidak ada                                                                                                             | Tetap hangat setelah jeda[16](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) | [Pilih durasi cache](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#pick-the-cache-duration)                                              |
| Pemangkasan input                            | Tambahan 21% hingga 26% dari tagihan agen triase kecil                                                                                                | Tidak ada                                                                                                             | Netral                                                                                                                           | [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens)                           |
| Pangkas hasil alat yang usang di batas tugas | 39% pada tugas agen yang panjang; tidak ada pada tugas pendek. Pada model yang disebutkan di bagian tersebut, gunakan compaction sebagai gantinya     | Tidak ada yang terukur                                                                                                | Netral                                                                                                                           | [Kelola siklus hidup konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#manage-the-context-lifecycle)                                |
| Tool search                                  | 45% dengan 500 definisi alat terlampir; 20% dari menunda toolset server MCP GitHub                                                                    | Tidak ada                                                                                                             | Netral                                                                                                                           | [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens)                           |
| File data melalui eksekusi kode              | 92% pada tugas data berisi 25 pertanyaan                                                                                                              | Peningkatan: 25 dari 25 benar, bukan 7                                                                                | Lebih cepat                                                                                                                      | [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens)                           |
| Batch API                                    | 50%                                                                                                                                                   | Tidak ada                                                                                                             | Hasil dalam 24 jam                                                                                                               | [Batch pekerjaan yang bisa menunggu](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#batch-work-that-can-wait)                             |
| Audit prompt terhadap model saat ini         | 14% pada kedua peningkatan model yang diuji                                                                                                           | Tidak ada; meningkat pada salah satunya                                                                               | Lebih cepat (lebih sedikit putaran alat)                                                                                         | [Audit prompt terhadap model saat ini](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#audit-prompts-against-the-current-model)            |
| Upgrade model                                | Biasanya lebih murah per tugas yang diselesaikan: hingga 87% lebih murah pada benchmark coding                                                        | Tidak ada; peningkatan pada sebagian besar                                                                            | Netral                                                                                                                           | [Upgrade model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#upgrade-the-model)                                                         |
| Turunkan effort                              | Pada tugas coding yang panjang, `medium` berbiaya sekitar 30% hingga 52% lebih murah daripada `high`, dan `low` sekitar dua pertiga lebih murah       | Hingga 15 poin lebih rendah, tergantung tugasnya; tidak ada pada satu agen riset                                      | Lebih cepat                                                                                                                      | [Setel effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort)                                                                |
| Jalankan ulang tugas yang gagal              | Sekitar 40% lebih murah daripada menjalankan semuanya pada `high`, dengan tingkat kelulusan yang sama atau sedikit lebih baik                         | Tidak ada                                                                                                             | Percobaan kedua pada tugas yang gagal                                                                                            | [Jalankan ulang kegagalan pada effort yang lebih tinggi](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#re-run-failures-at-higher-effort) |
| Minta jawaban yang lebih singkat             | Sekitar 13% lebih murah, dari 39% lebih sedikit token output                                                                                          | Tidak ada                                                                                                             | Lebih cepat                                                                                                                      | [Tetapkan anggaran dan batas output](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                          |
| Menaikkan `max_tokens`                       | Tidak ada: biaya per tugas yang diselesaikan tetap kurang lebih sama                                                                                  | Peningkatan: hingga 22 poin lebih banyak tugas diselesaikan pada satu benchmark coding; tidak ada pada benchmark lain | Netral                                                                                                                           | [Tetapkan anggaran dan batas output](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                          |
| Advisor                                      | Tidak ada: sekitar 2,1 kali biaya model saja, pada benchmark coding                                                                                   | Pada coding, peningkatan kecil yang mungkin kebetulan; pada pembacaan grafik, penurunan                               | Sekitar 1,4 panggilan tambahan per percobaan, pada coding                                                                        | [Strategi advisor](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#advisor-strategy-escalate-hard-decisions)                               |
| Orchestrator                                 | Sekitar setengah biaya model orchestrator saja, pada pekerjaan yang lebih besar dari satu jendela konteks; pada pekerjaan rutin, ukur terlebih dahulu | 10 hingga 12 poin lebih rendah pada pekerjaan tersebut                                                                | Jauh lebih cepat pada pekerjaan tersebut                                                                                         | [Strategi orchestrator](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#orchestrator-strategy-delegate-bulk-work)                          |

### Otomatiskan pencarian dengan skill Claude API

Jalankan perintah `cost-optimize` dari [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill) sebelum Anda mencari penghematan. Perintah ini memprofilkan ke mana token Anda digunakan dan menerapkan tuas-tuas secara berurutan, dimulai dari caching. Kemudian jalankan `/claude-api hillclimb` di direktori yang berisi evaluasi Anda.

Anthropic mengukur tuas pertama dari `cost-optimize` dan dua pencarian pada tau2-bench retail[24](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), semuanya pada model-model sebelumnya. Breakpoint cache yang dihasilkan `cost-optimize` memangkas biaya per tugas, dan tingkat kelulusan turun kurang dari sebaran antar-run yang identik.

Sebuah pencarian menemukan konfigurasi yang lebih murah dengan menurunkan effort dan turun satu tingkatan model. Tingkat kelulusannya tetap berada di dalam rentang yang ditetapkan sebelum pencarian dengan selisih sebagian kecil dari satu tugas, dan berakhir di bawah batas bawah yang lebih ketat yang digunakan pencarian untuk putusannya sendiri. Pencarian kedua, yang dimulai dari model berbiaya lebih rendah pada effort default-nya, tidak mempertahankan apa pun. Referensi 24 memuat angka-angkanya dan biaya menjalankan setiap pencarian.

Grafik berikut memplot setiap langkah dari pencarian pertama:

<Frame caption="Satu pencarian pada model-model sebelumnya, langkah demi langkah. Perubahan effort dan model menghasilkan penghematan; suntingan prompt tidak membawa peningkatan yang bertahan lama.">
  ![Grafik sebar, tau2-bench retail: setiap langkah pencarian dari Claude Opus 5; Sonnet 5 pada low 61% lebih murah dengan selisih dalam 2 poin](https://platform.claude.com/docs/images/cost-intel/hillclimb.svg)
</Frame>

Dua pengaturan menentukan apakah Anda dapat memercayai jawaban pencarian:

* **Sisihkan satu split yang tidak pernah dibaca oleh pencarian.** Pencarian menilai adopsi di sana, sehingga konfirmasi menangkap perubahan yang hanya cocok dengan tugas-tugas yang dilihat pencarian, seperti yang terjadi pada suntingan prompt (referensi 24).
* **Ulangi baseline sebelum perubahan pertama.** Run identik dari satu konfigurasi awal berbeda beberapa tugas dalam pengukuran ini (referensi 24). Pengulangan tersebut memberi gerbang adopsi pencarian sebuah batas noise.

## Benchmark yang dirujuk

Kecuali jika suatu referensi menyatakan lain, pengukuran merupakan eksekusi internal Anthropic atas benchmark-benchmark ini. Kecuali dinyatakan lain, biaya dinyatakan dalam USD pada harga daftar yang berlaku saat setiap benchmark dijalankan; angka Claude Sonnet 5 menggunakan $2 USD dan $10 USD per juta token input dan output. Angka Claude Sonnet 5.5 dari eksekusi 24 September 2026 menggunakan harga input dan output yang sama serta harga "cache read" (pembacaan cache) saat ini, yaitu $0,10 USD per juta token, alih-alih harga peluncurannya sebesar $0,20 USD, yang diterapkan pada jumlah token yang tercatat di setiap eksekusi. Eksekusi tersebut menggunakan build pra-rilis Claude Sonnet 5.5, dan tidak ada percobaan di dalamnya yang dijawab oleh model fallback. Grafik berlabel "notional USD" menghitung harga jumlah token setiap permintaan pada tarif tersebut alih-alih melaporkan tagihan.

1. **WideSearch:** Wong et al., "WideSearch: Benchmarking Agentic Broad Info-Seeking," arXiv:2508.07999, 2025. Tugas riset web yang luas yang dinilai berdasarkan kelengkapan dan akurasi sebuah tabel dengan banyak baris; 200 soal, 3 eksekusi per konfigurasi, dijalankan 1 hingga 2 Agustus 2026. Dengan Claude Fable 5 pada benchmark ini, DeepWideSearch (referensi 6), BrowseComp (referensi 4), dan GDPval (referensi 2), effort `low` mengorbankan 1 hingga 3 poin untuk penghematan sepertiga hingga setengah biaya per tugas, `medium` menyamai akurasi default dengan sekitar 70% hingga 87% biayanya, dan default tidak memberikan keuntungan terukur apa pun dibandingkan `medium` pada keempatnya. Grafik konsentrasi biaya adalah eksekusi terpisah dengan 20 soal, 3 eksekusi per soal, dijalankan 3 hingga 4 Agustus 2026, dengan biaya dihitung dari catatan penagihan per permintaan. Grafik ini mencakup 59 dari 60 eksekusi. Eksekusi keenam puluh, yang ditagih $10,91 USD dari total $432,31 USD, tidak memiliki biaya yang tercatat bersama hasilnya dan tidak disertakan.

2. **GDPval:** OpenAI, "GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks," 2025. Hasil kerja pengetahuan yang dinilai terhadap rubrik tugas; eksekusi 210 tugas dari gold set yang dirilis, satu percobaan per tugas, dijalankan 2 Agustus 2026. Penilaian dilakukan oleh model Claude, sehingga skor absolut dapat berbeda dari hasil yang dipublikasikan.

3. **SWE-bench Pro:** Scale AI, "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?", 2025.

   * **Apa yang diukur:** Subset 482 soal yang dipilih karena kompatibel dengan harness evaluasi Anthropic; skornya tidak dapat dibandingkan dengan leaderboard publik. Skor ini juga tidak dapat dibandingkan dengan hasil SWE-bench Pro dalam system card Claude Opus 5.5, yang berasal dari eksekusi pada effort `max` dengan kumpulan soal yang berbeda.
   * **Cara penetapan harga:** Biaya pada subset ini dihargai sebagaimana organisasi pelanggan diukur: prompt sebelumnya dari setiap permintaan sebagai cache read dan token barunya sebagai "cache write" (penulisan cache) 5 menit, dari catatan penggunaan eksekusi itu sendiri, diperiksa terhadap buku besar pelanggan.
   * **Eksekusi Claude Opus 5.5:** Angka Claude Opus 5.5 merata-ratakan dua eksekusi pada `low`, `medium` (default-nya), dan `high`, serta menggunakan satu eksekusi pada `xhigh`, semuanya dijalankan 19 hingga 20 September 2026, dengan batas 16.384 token per giliran yang sama seperti eksekusi Claude Opus 5 bulan Agustus; batas tersebut memotong 2 percobaan `xhigh` dan tidak ada pada pengaturan lain. Diukur terhadap `high`, Claude Opus 5.5 mencetak skor sekitar 2,5 poin lebih rendah pada default-nya, `medium`, dengan sekitar 70% biaya per tugas, dan sekitar 8 poin lebih rendah pada `low` dengan sekitar sepertiga biaya; `xhigh` mencetak skor sekitar 1,4 poin lebih tinggi dengan 2,5 kali biaya `high`. Rasio-rasio tersebut berasal dari biaya yang tidak dibulatkan.
   * **478 soal:** Eksekusi Opus 5.5 menggunakan versi benchmark yang container penilaiannya hanya dapat menjangkau mirror paket internal. Versi tersebut menghapus satu soal yang pengujiannya memerlukan situs web aktif, dan pada tiga soal lainnya solusi referensi gagal di sana, sehingga perbandingan Opus 5.5, dan angka Claude Fable 5.1 yang disandingkan dengannya, menggunakan 478 soal yang tersisa.
   * **Eksekusi Claude Sonnet 5.5:** Claude Sonnet 5.5 menjalankan versi benchmark yang sama: dua eksekusi pada default-nya, `high`, dan dua pada `medium`, semuanya pada 24 September 2026, dengan batas 16.384 token per giliran yang sama, yang tidak memotong satu pun percobaannya. Angkanya menggunakan 478 soal, demikian pula angka Claude Sonnet 5 yang disandingkan dengannya, yang dihitung atas soal-soal tersebut dari eksekusi Agustus mereka.
   * **Eksekusi Claude Opus 5:** Angka SWE-bench Pro Claude Opus 5 di [Upgrade model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#upgrade-the-model) dan dalam referensi ini merata-ratakan dua eksekusi pada effort default-nya dan menggunakan satu eksekusi pada `low`, semuanya dijalankan 4 Agustus 2026.
   * **Advisor, pasangan Claude Sonnet 5:** Pasangan executor Claude Sonnet 5 dengan advisor Claude Opus 5 di balik contoh tingkat konsultasi di [Strategi advisor](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#advisor-strategy-escalate-hard-decisions) berasal dari seri pengukuran yang sama pada subset ini: pasangan pada effort default dijalankan dua kali (7 Agustus dan 8 Agustus 2026, satu eksekusi dan replikasi persisnya), pasangan effort rendah sekali (8 Agustus 2026), dan Claude Sonnet 5 sendiri dua kali (77,4%, baseline untuk kedua pasangan).
   * **Advisor, pemeriksaan konsultasi Claude Sonnet 5.5:** Pemeriksaan konsultasi Claude Sonnet 5.5 yang dikutip di [Strategi advisor](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#advisor-strategy-escalate-hard-decisions) menjalankan satu percobaan pada masing-masing 20 dari 478 soal, pada 24 September 2026, dengan advisor Claude Opus 5.5 melalui alat advisor. Empat konfigurasi dijalankan: `high` dan `xhigh`, masing-masing dengan dan tanpa prompt sistem yang disarankan dokumentasi alat advisor untuk tugas coding. Pada effort default-nya, `high`, Claude Sonnet 5.5 tidak berkonsultasi dengan advisor pada satu pun dari 20 soal, dengan atau tanpa prompt tersebut. Pada `xhigh`, ia berkonsultasi pada 3 dari 20 soal tanpa prompt dan 4 dengan prompt, setiap kali pada percobaannya dengan giliran terbanyak.
   * **Angka eskalasi:** Angka eskalasi berasal tugas demi tugas dari eksekusi Opus 5.5: `low` terlebih dahulu, lalu `high` pada kegagalannya, menyelesaikan 96,4% hingga 97,5% di seluruh pasangan eksekusi dengan sekitar $0,17 USD; `medium` terlebih dahulu, 96,0% hingga 97,1% dengan sekitar $0,24 USD; `high` dijalankan ulang pada kegagalannya sendiri, 96,9% dengan $0,31 USD; semuanya pada `high`, 94,8% hingga 95,8% dengan $0,29 USD.
   * **Bandingkan model:** Angka Claude Fable 5.1 di [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task) berasal dari satu eksekusi pada subset yang sama pada effort default, dijalankan 26 Agustus 2026: dihitung atas 478 soal, ia menyelesaikan 92,3% dengan $1,19 USD per tugas yang diselesaikan. Grafik bagian tersebut serta angka Claude Opus 5.5 dan Claude Sonnet 5.5-nya menggabungkan dua eksekusi pada setiap pengaturan yang diplot, semuanya dihitung atas 478 soal: Claude Opus 5.5 pada `low`, `medium`, dan `high`, serta Claude Sonnet 5.5 pada `medium` dan `high`.
   * **Bandingkan model, pekerjaan per tugas:** Dalam angka-angka tersebut, Claude Opus 5.5 pada `low` melakukan lebih sedikit pekerjaan pada setiap tugas dibandingkan Claude Sonnet 5.5 pada default-nya: sedikit lebih dari setengah token output Sonnet 5.5 dan sedikit lebih dari sepertiga cache read-nya. Pada default masing-masing, Opus 5.5 pada `medium` menyelesaikan sekitar 5 poin persentase lebih banyak daripada Sonnet 5.5 dengan sekitar dua kali biayanya. Pada pengaturan tersebut, ia melakukan sedikit lebih banyak pekerjaan per tugas dibandingkan Sonnet 5.5.
   * **Upgrade model, eksekusi:** Titik Claude Fable 5 di Upgrade model menggabungkan tiga eksekusi pada effort default, dijalankan 26 Agustus 2026, dihargai sebagaimana organisasi pelanggan diukur. Tangga peningkatan menghitung setiap model atas 478 soal, masing-masing pada default bawaannya. Tangga ini menggunakan satu eksekusi per model kecuali Opus 5, Opus 5.5, Sonnet 5, dan Sonnet 5.5 (masing-masing dua eksekusi) serta Fable 5 (tiga eksekusi yang dijelaskan di atas). Eksekusi Opus 4.7, Opus 4.8, Sonnet 4.6, dan Sonnet 5 dijalankan 17 hingga 19 Agustus 2026, dan eksekusi Opus 5 pada 4 Agustus, semuanya dalam satu harness dan organisasi; eksekusi Opus 5.5 dan Sonnet 5.5 adalah yang dijelaskan sebelumnya dalam referensi ini.
   * **Upgrade model, biaya per tugas yang diselesaikan:** Claude Opus 5 berbiaya 21% lebih tinggi per tugas yang diselesaikan dibandingkan Claude Opus 4.8 ketika eksekusi Claude Opus 5 tersebut dibandingkan dengan satu eksekusi Claude Opus 4.8 pada default bawaannya dari seri 17 hingga 19 Agustus, dihitung atas 478 soal yang sama; panel SWE-bench Pro pada grafik tidak menampilkan Claude Opus 4.7 maupun Claude Opus 4.8. Dalam pengukuran yang sama, dihargai sebagaimana pelanggan ditagih, Claude Opus 5 menyelesaikan 12 poin tugas lebih banyak daripada Claude Opus 4.8 dengan biaya 21% lebih tinggi per tugas yang diselesaikan tersebut, Claude Opus 4.8 menyelesaikan porsi tugas yang sama dengan Claude Opus 4.7 dengan biaya 14% lebih rendah per tugas yang diselesaikan, dan Claude Opus 5 pada effort `low` mengungguli default Claude Opus 4.8 pada benchmark ini dengan sekitar 30% biaya per tugas yang diselesaikan.
   * **Upgrade model, harga:** Penghematan Claude Sonnet 5 dibandingkan Claude Sonnet 4.6 di Upgrade model berasal dari harga per token yang lebih rendah, yang lebih dari cukup untuk mengimbangi token tambahan yang digunakannya per tugas. Claude Sonnet 5.5 mengenakan biaya yang sama dengan Claude Sonnet 5 untuk semuanya kecuali cache read, yang biayanya setengahnya. Harga token Claude Opus 5.5 lebih rendah daripada Claude Opus 5, terutama untuk cache read. Seperti Claude Sonnet 5, tingkat frontier memperoleh keuntungan melalui harga: sebagian besar penghematan Claude Fable 5.1 adalah harga cache read yang lebih rendah.
   * **Biaya tanpa caching, dihargai dari jumlah token yang tercatat:** Anthropic juga menghitung ulang harga jumlah token yang tercatat dari eksekusi Claude Opus 5.5 dan Claude Sonnet 5.5 yang dijelaskan sebelumnya dalam referensi ini, atas 478 soal, untuk faktor caching di [Mengapa caching didahulukan](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#why-caching-comes-first); Anthropic tidak melakukan eksekusi dengan caching dinonaktifkan.
   * **Faktor, per model:** Setiap faktor adalah biaya token dengan setiap token input pada harga input, token output tidak berubah, dibagi dengan biaya yang dihargai sebagaimana organisasi pelanggan diukur: untuk Claude Opus 5.5, 3,3 pada `medium`, 2,4 pada `low`, 3,8 pada `high`, dan 5,4 pada `xhigh` (satu eksekusi); untuk Claude Sonnet 5.5, dengan cache read pada $0,10 USD per juta token, 3,1 pada `high` dan 2,4 pada `medium`, atau 2,8 pada `high` dengan harga peluncuran $0,20 USD. Tidak seperti eksekusi pada grafik caching, eksekusi ini tidak dikenai biaya pencarian web, dan permintaan pertama suatu tugas dihargai sebagai cache write.

4. **BrowseComp:** Wei et al., "BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents," OpenAI, 2025. Angka effort menggunakan potongan 500 soal, satu hingga tiga eksekusi per pengaturan, dijalankan 3 Agustus 2026, dengan titik default menggabungkan dua eksekusi dari 26 hingga 27 Juli 2026. Pengukuran pekerjaan rutin dengan ekor biaya panjang di [Strategi orchestrator](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#orchestrator-strategy-delegate-bulk-work) menggunakan 10 soal yang diselesaikan model secara andal sendirian ketika protokol ditetapkan, dari irisan 26 soal, 50 eksekusi terdelegasi (5 per soal; 1 hingga 2 Agustus 2026) dan 70 eksekusi model sendirian (50 dari 2 hingga 3 Agustus 2026; 20 diarsipkan dari 12 hingga 13 Juli dan 1 Agustus 2026), $6,45 USD dibandingkan $11,99 USD per eksekusi secara ekspektasi; angka terdelegasi memiliki rentang pengukuran sekitar 20%. Ke-10 soal tersebut adalah soal-soal di mana konfigurasi terdelegasi, yaitu orchestrator Claude Fable 5 dengan satu worker Claude Sonnet 5, benar di kelima eksekusi dan Claude Fable 5 sendirian benar di kedua eksekusi yang diarsipkan; eksekusi terdelegasi adalah eksekusi yang sama tersebut, dan hanya Claude Fable 5 sendirian yang dijalankan lagi pada kesepuluh soal itu. Dari 70 eksekusinya, yang diarsipkan maupun yang baru, Claude Fable 5 sendirian benar di 68. Pada soal-soal tersebut, konfigurasi terdelegasi berbiaya sekitar setengah dari Claude Fable 5 sendirian secara rata-rata ($6,45 USD dan $11,99 USD yang disebutkan sebelumnya) dan sekitar sepertiga pada persentil ke-90 ($12 USD dibandingkan $33 USD per eksekusi), dan eksekusi termahalnya berbiaya $42 USD dibandingkan $84 USD; eksekusi $84 USD tersebut juga salah. Pada set BrowseComp lengkap yang lebih sulit, Claude Fable 5 sendirian mencapai akurasi konfigurasi orchestrator yang diukur pada set tersebut dengan biaya 22% hingga 30% lebih rendah.

5. **Penskalaan arsitektur agen:** Kim et al., "Towards a Science of Scaling Agent Systems," arXiv:2512.08296, 2025. Studi eksternal independen, dikutip hanya untuk arah temuan tentang kapan delegasi tidak menguntungkan, bukan untuk angka apa pun.

6. **DeepWideSearch:** "DeepWideSearch: Benchmarking Depth and Width in Agentic Information Seeking," arXiv:2510.20168, 2025. Ke-220 pertanyaan mencakup 15 domain, masing-masing menggabungkan pengumpulan banyak baris dengan pengambilan multi-hop; diukur pada set baris tetap benchmark, 3 eksekusi per konfigurasi, dijalankan 2 Agustus 2026 (titik tim dengan satu worker dijalankan 26 hingga 27 Juli 2026). Dengan Claude Fable 5, effort `low` menyamai orchestrator dengan worker Claude Sonnet 5 dengan biaya 29% lebih rendah, dan membutuhkan 4,5 menit per soal, dibandingkan 7,9 menit pada default.

7. **DeepResearch Bench II:** Li et al., "DeepResearch Bench II: Diagnosing Deep Research Agents via Rubrics from Expert Report," arXiv:2601.08536, 2026.

   * **Apa yang diukur:** 132 tugas risetnya di 22 domain dinilai terhadap rubrik biner yang diturunkan dari pakar. Diukur pada subset 50 tugas yang distratifikasi di semua tema, satu percobaan per tugas, 3 eksekusi per pengaturan, di [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) dengan alat pencarian web dan fetch milik platform itu sendiri (26 hingga 27 Agustus 2026).
   * **Cara penilaian:** Dinilai pada 33 tugas yang tidak ditolak oleh konfigurasi mana pun, dengan percobaan yang dihentikan lebih awal oleh classifier keamanan produksi dihapus. Claude Opus 4.6 menilai berdasarkan protokol rubrik benchmark; versi aslinya menggunakan penilai yang berbeda, dan penilai Anthropic mungkin lebih menyukai gaya internal.
   * **Skor:** Skor adalah rata-rata setiap model pada basis 33 tugas dengan tugas-tugasnya sendiri yang didahului dihapus; pada 21 dari 33 tugas di mana tidak ada konfigurasi yang percobaannya dihentikan lebih awal, Claude Fable 5.1 unggul 2 hingga 3 poin atas Claude Fable 5 di setiap tingkat effort dan kedua model datar di seluruh tingkat effort.
   * **Cara penetapan harga:** Biaya dihargai sebagaimana organisasi pelanggan diukur: prompt sebelumnya dari setiap permintaan sebagai cache read dan token barunya sebagai cache write 5 menit, dengan permintaan pertama suatu sesi mempertahankan cache read yang diperolehnya, dari catatan penggunaan eksekusi itu sendiri, ditambah biaya pencarian web platform. Setiap biaya per tugas adalah biaya eksekusi 50 tugas dibagi 50, dengan percobaan yang dihentikan lebih awal disertakan, dirata-ratakan atas tiga eksekusi.
   * **Hasil, Claude Fable 5:** Claude Fable 5 berbiaya $2,30 USD per tugas pada `low` dan $4,71 USD pada `high`, dihargai dengan cara yang sama; persentase di [Upgrade model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#upgrade-the-model) berasal dari biaya yang tidak dibulatkan.
   * **Hasil, Claude Opus 5:** Claude Opus 5 pada effort default-nya dijalankan pada permukaan dan subset yang sama, tiga eksekusi, pada 28 Agustus 2026: 68,8% pada 50 tugas mentah, 70,8% pada basis 33 tugas, dan 71,1% pada set 21 tugas, dengan $6,28 USD per tugas ($23,72 USD tanpa caching); tidak ada percobaannya yang dihentikan lebih awal oleh classifier keamanan, di bawah deployment safeguard yang lebih baru daripada yang digunakan model-model lain.
   * **Bandingkan model:** Perbandingan riset di [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task) bertumpu pada angka-angka ini: Claude Fable 5.1 pada `low` mencetak skor 10 poin di atas Claude Sonnet 5 pada basis 33 tugas (66% berbanding 56%) dengan sekitar empat kali biaya per tugas atas seluruh 50 tugas ($4,48 USD berbanding $1,18 USD); Claude Opus 5 pada default-nya, yang skor dan biayanya disebutkan sebelumnya dalam referensi ini, mencetak skor di atas Claude Fable 5.1 pada default-nya, yang mencetak skor 65% pada basis 33 tugas dan berbiaya $6,89 USD per tugas atas seluruh 50 tugas, sehingga untuk riset, Claude Fable 5.1 sepadan dengan harganya hanya pada `low`.
   * **Grafik caching:** Grafik caching menghitung ulang harga permintaan yang sama dengan setiap token input pada tarif tanpa cache.
   * **Tidak diukur:** Claude Sonnet 5.5 tidak diukur pada benchmark ini.

8. **Penyisiran cacat korpus:** Internal Anthropic, untuk pekerjaan yang lebih besar dari satu jendela konteks: korpus 21,6 juta token dari 14 sumber paket Python publik dengan 130 cacat yang ditanam dan penilaian deterministik; protokol ditetapkan sebelum eksekusi dan ditinjau secara internal; tiga eksekusi per konfigurasi. Setiap konfigurasi dijalankan di Claude Managed Agents. Konfigurasi tim yang ditampilkan di grafik adalah konfigurasi di mana orchestrator Claude Fable 5.1 menjalankan seluruh penyisiran di dalam platform pada batas terdokumentasinya yaitu 25 worker Claude Sonnet 5 secara bersamaan, dijalankan 30 Agustus 2026; tiga eksekusinya mencetak F1 0,764, 0,825, dan 0,791 setelah audit tambahan (mentah 0,751, 0,821, dan 0,781) dengan $225 USD, $234 USD, dan $283 USD. Konfigurasi tim berbiaya sekitar setengah dari Claude Fable 5.1 sendirian pada `low`, `medium`, atau `high` (47% hingga 55% lebih rendah), mencetak skor 10 hingga 12 poin di bawahnya, dan membutuhkan sekitar 2,3 jam per eksekusi, dibandingkan 15 hingga 20 jam. Konfigurasi tim membaca sekitar 560 juta token yang di-cache per eksekusi, hampir semuanya pada tarif cache read Claude Sonnet 5. Itu sekitar satu setengah kali dari sekitar 365 juta yang dibaca Claude Fable 5.1 sendirian. Claude Fable 5.1 sendirian pada effort `high` masih memegang akurasi puncak, dengan sekitar 2,2 kali biaya konfigurasi tim, sehingga delegasi di sini memberikan sebagian besar akurasi, bukan seluruhnya. Konfigurasi dengan Claude Sonnet 5 sendirian dijalankan 3 hingga 4 Agustus 2026; konfigurasi dengan Claude Fable 5.1 sendirian dijalankan 24 hingga 25 Agustus 2026, di bawah pengaturan penyajian peluncuran platform, tiga seed per pengaturan effort, pada build korpus yang sama. Image sandbox membawa salinan terinstal dari sebagian korpus, dan langkah perakitan akhir Claude Fable 5.1 membandingkan dengannya pada 7 dari 9 eksekusi; penilaian ulang tanpa tambahan tersebut menggeser seed yang terdampak hingga 3 poin. F1 absolut spesifik untuk build korpus ini, tidak dapat dibandingkan antar-benchmark; perbandingan konfigurasi bersifat setara.

9. **GPQA Diamond:** Rein et al., "GPQA: A Graduate-Level Google-Proof Q\&A Benchmark," 2023. Subset Diamond dengan 198 pertanyaan, dinilai oleh model terhadap jawaban referensi, token advisor diukur per permintaan. Claude Haiku 5.5 dan Claude Sonnet 5.5, masing-masing sendirian dan dengan advisor Claude Opus 5.5, serta Claude Opus 5.5 sendirian menjalankan dua eksekusi per konfigurasi pada 7 Oktober 2026, semuanya dengan [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback) dinonaktifkan, pada effort default setiap model, dan dengan penolakan dihitung sebagai salah. Pemeriksaan keamanan platform menolak satu pertanyaan biologi per eksekusi pada Claude Haiku 5.5 dan Claude Sonnet 5.5 sendirian, satu dalam dua eksekusi pada Haiku 5.5 dengan advisor, tidak ada pada Sonnet 5.5 dengan advisor, dan enam per eksekusi pada Opus 5.5, yang mencetak skor 91% dengan penolakan tersebut dihitung sebagai salah dan 93,5% pada pertanyaan yang dijawabnya. Claude Haiku 5.5 sendirian mencetak skor 85%, 6 poin di bawah Opus 5.5. Konfigurasi advisor menambahkan alat tersebut tanpa prompt yang meminta konsultasi, dan tidak ada executor yang memanggil advisor pada pertanyaan mana pun. Pasangan-pasangan tersebut mencetak skor 0,5 poin (Claude Haiku 5.5) dan 1,0 poin (Claude Sonnet 5.5) di atas executor sendirian, keduanya dalam batas noise antar-eksekusi.

10. **DeepSWE:** Datacurve, "DeepSWE: Measuring Frontier Coding Agents on Original, Long-Horizon Engineering Tasks," arXiv:2607.07946, 2026. Set ini memiliki 113 tugas orisinal dalam lima bahasa dengan verifier berbasis program. Pasangan masing-masing dua eksekusi, dijalankan 7 Agustus 2026, dengan token advisor diukur per permintaan, dan menggunakan loop advisor sisi klien alih-alih alat advisor, dengan akuntansi yang identik. Sapuan effort model tunggal adalah eksekusi tunggal yang dihargai dari jumlah token, sebuah aproksimasi yang memperhitungkan cache. Biaya per tugas adalah total eksekusi dibagi 113. Pada benchmark ini, executor Claude Sonnet 5 dengan effort rendah yang disertai advisor mencetak skor 23 poin di atas executor yang sama sendirian.

11. **Benchmark agentic-coding internal:**

    * **Apa yang diukur:** Internal Anthropic: 370 tugas repositori yang dinilai oleh pengujian repositori itu sendiri. Angka API diukur dengan agen API sederhana dan batas output 128.000 token, satu eksekusi per konfigurasi: Opus 5 sendirian pada effort default 9 hingga 10 Agustus 2026, dan pada `low` serta `medium` 10 Agustus 2026; Claude Fable 5.1 sendirian pada lima nilai effort yang ditetapkan secara eksplisit 20 Agustus 2026 (grafik menampilkan tiga di antaranya); dan pasangan 24 hingga 25 Agustus 2026.
    * **Eksekusi Agustus:** Eksekusi Agustus memiliki lima percobaan per tugas untuk pasangan dan kontrol Claude Opus 5 serta satu untuk titik-titik lainnya.
    * **Cara penetapan harga:** Biaya dihitung per percobaan. Biaya dihargai sebagaimana organisasi pelanggan diukur: prompt sebelumnya dari setiap permintaan loop agen sebagai cache read dan token barunya sebagai cache write 5 menit, dari catatan penggunaan eksekusi itu sendiri, dan setiap panggilan advisor, yang tidak menggunakan cache, dari token yang tercatat, semuanya pada harga daftar.
    * **Claude Opus 5.5 sendirian:** Claude Opus 5.5 sendirian dijalankan pada seluruh 370 tugas, 19 hingga 20 September 2026: pada effort default-nya (`medium`) dan pada `high` dengan lima percobaan per tugas, serta pada `low` dan `xhigh` dengan satu (369 dari 370 dinilai pada masing-masing, setelah kegagalan pemeriksaan penyiapan). Claude Opus 5.5 sendirian menyelesaikan 74,8% percobaan pada `low` dengan $0,35 USD per percobaan, 86,6% pada `medium` dengan $0,84 USD, 88,4% pada `high` dengan $1,38 USD, dan 91,1% pada `xhigh` dengan $4,11 USD.
    * **Claude Opus 5.5 dengan advisor Claude Fable 5.1, eksekusi:** Executor Claude Opus 5.5 pada `high` dengan Claude Fable 5.1 yang telah dirilis sebagai advisor (eksekusi Agustus menggunakan snapshot pra-rilis) menjalankan lima percobaan per tugas pada tanggal yang sama; satu tugas gagal dalam pemeriksaan penyiapannya, sehingga 1.845 percobaan dinilai. 279 percobaan di mana advisor ditolak karena beban dijalankan ulang, dan percobaan yang konsultasinya mengalami timeout dipertahankan, seperti pada bulan Agustus.
    * **Claude Fable 5.1 sendirian:** Sebagai perbandingan, Claude Fable 5.1 yang telah dirilis sendirian pada `high`, default-nya, mencetak skor 85,7% (317 dari 370 tugas), satu percobaan per tugas pada 7 Oktober 2026.
    * **Konsultasi:** Pasangan Agustus rata-rata melakukan sekitar dua konsultasi advisor per percobaan; pasangan Claude Opus 5.5 meminta 1,39 dan menerima 1,35.
    * **Claude Opus 5.5 dengan advisor Claude Fable 5.1, hasil:** Pasangan Claude Opus 5.5 mencetak skor 90,1% dengan $2,92 USD per percobaan: dibandingkan dengan Claude Opus 5.5 pada default-nya, `medium`, itu berarti 3,5 poin dengan sekitar 3,5 kali biayanya. Biaya latensinya adalah konsultasi itu sendiri: sekitar satu atau dua panggilan model frontier tambahan per tugas, masing-masing berada di jalur kritis tugas. Dengan executor Claude Opus 5.5, saran tersebut hampir tidak menghemat biaya executor: $1,36 USD per percobaan dibandingkan $1,38 USD untuk Claude Opus 5.5 sendirian pada `high`, sementara konsultasinya berbiaya $1,55 USD.
    * **Pasangan Agustus:** Pada bulan Agustus, dengan executor Claude Opus 5 dan advisor Claude Fable 5.1, executor menghabiskan $1,26 USD lebih sedikit per percobaan dibandingkan Claude Opus 5 sendirian pada default-nya, dan konsultasinya berbiaya $2,47 USD, sehingga penghematan tersebut membayar sekitar setengah dari biaya saran. Pasangan Agustus tersebut adalah konfigurasi paling akurat yang diukur pada saat itu, dengan $6,21 USD per percobaan.
    * **Claude Sonnet 5.5 sendirian, eksekusi:** Claude Sonnet 5.5 sendirian dijalankan pada seluruh 370 tugas pada 24 September 2026, pada effort default-nya (`high`) dan pada `medium`, satu percobaan per tugas, dengan batas output 128.000 token yang sama, yang tidak memotong satu pun percobaannya. Seluruh 370 dinilai pada `medium`, dan 369 dari 370 pada `high`, setelah kegagalan pemeriksaan penyiapan. Biayanya dihargai sebagaimana organisasi pelanggan diukur.
    * **Claude Sonnet 5.5 sendirian, hasil:** Tanpa advisor, Claude Sonnet 5.5 mencetak skor 77,8% pada default-nya, `high`, dengan $0,33 USD per percobaan, sekitar 9 poin di bawah Claude Opus 5.5 pada default-nya dengan sekitar dua perlima biayanya; pada `medium`, ia mencetak skor 62,7% dengan $0,16 USD. Pada `medium`, Claude Sonnet 5.5 mencetak skor sekitar 15 poin lebih rendah daripada pada default-nya, `high`, dengan sekitar 48% biaya per percobaan.
    * **Bandingkan model:** Di [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task), Claude Opus 5.5 pada default-nya berbiaya kurang dari sepertiga biaya per percobaan Claude Fable 5.1 pada `medium`, yang merupakan satu eksekusi.

12. **Benchmark tugas repositori internal (pengukuran batas):**

    * **Apa yang diukur:** Set internal Anthropic terpisah berisi sekitar 130 tugas repositori, dijalankan 20 Agustus 2026 (Claude Fable 5.1) dan 19 September 2026 (Claude Opus 5.5, pada effort default-nya, `medium`), dengan loop agen API sederhana, satu percobaan per tugas.
    * **Cara penetapan harga:** Biaya per tugas yang diselesaikan dihargai sebagaimana pelanggan ditagih, dengan cache prompt 5 menit, untuk Claude Fable 5.1, dan pada harga daftar dari jumlah token yang tercatat dalam eksekusinya untuk Claude Opus 5.5.
    * **Eksekusi Claude Fable 5.1:** Eksekusi Claude Fable 5.1 adalah 135 tugas per batas pada effort default yang ditetapkan secara eksplisit: angka 16.384 token merata-ratakan dua eksekusi (36,3% pada keduanya); angka 64.000 dan 128.000 adalah eksekusi tunggal (58,5% dan 60,0%). Lima soal memicu penolakan keamanan di keempat eksekusi dan dihitung sebagai kegagalan.
    * **Eksekusi Claude Opus 5.5:** Angka 16.384 token Claude Opus 5.5 merata-ratakan dua eksekusi (134 dan 135 tugas dinilai), dan angka 64.000 serta 128.000-nya adalah eksekusi tunggal (masing-masing 135 tugas); dua percobaan di setiap eksekusi 16.384 token dan satu di masing-masing eksekusi 64.000 dan 128.000 token berakhir dengan penolakan keamanan dan dihitung sebagai kegagalan. Claude Opus 5.5 menyelesaikan 57,6% pada 16.384 (58,2% dan 57,0%), 75,6% pada 64.000, dan 68,9% pada 128.000. Tidak ada percobaannya yang terpotong pada 64.000 atau 128.000, sehingga batas tersebut tidak menjelaskan perbedaan antara kedua eksekusi itu.
    * **Percobaan yang diakhiri oleh batas:** Hanya 1 dari 66 percobaan Claude Opus 5.5 yang diakhiri oleh batas 16.384 token, dan 9 dari 117 percobaan Claude Fable 5.1, yang tetap lulus.
    * **Biaya per percobaan:** Biaya per percobaan adalah $3 USD pada 16.384 dan $4 USD pada 64.000 untuk Claude Opus 5.5, pada harga daftar, serta $8 USD dan $13 USD untuk Claude Fable 5.1, sebagaimana pelanggan ditagih.
    * **Angka batas SWE-bench Pro:** Angka batas SWE-bench Pro adalah satu eksekusi Claude Fable 5.1 per batas pada effort default, dijalankan 26 Agustus 2026, pada subset 100 soal yang distratifikasi dari set 482 soal referensi 3, tidak dapat dibandingkan dengan skornya; pada effort default, eksekusi pada 16.384 dan pada 64.000 masing-masing menyelesaikan 94 dari 100 soal.
    * **Panjang giliran:** Distribusi per giliran dalam dot plot bagian tersebut berasal dari eksekusi Claude Opus 5.5 dan Claude Fable 5.1 pada 128.000: tidak ada giliran Opus 5.5 yang mencapai batas (yang terpanjang sekitar 61.000 token, dan 0,56% gilirannya melebihi 16.384), dan satu giliran Fable 5.1 mencapai 128.000 (0,46% gilirannya melebihi 16.384). Dengan batas pada 128.000, 2 dari 14.331 giliran Claude Fable 5.1 lebih panjang dari 64.000 token, dan tidak ada giliran Claude Opus 5.5 yang demikian.

13. **Chartography:** Surge AI, "Chartography," 2026.

    * **Apa yang diukur:** Set lengkap 100 pertanyaan yang dirilis, diukur 6 dan 9 Agustus 2026 (Claude Opus 5 sendirian) dan 20 September 2026 (Claude Opus 5.5), dengan implementasi Anthropic di Claude Managed Agents (sandbox cloud standar; konfigurasi advisor menggunakan advisor Managed Agents).
    * **Cara penilaian:** Claude Sonnet 4.6 menilai alih-alih penilai referensi dan benchmark dijalankan dengan alat, sehingga skor dapat dibandingkan antar-konfigurasi di sini tetapi tidak dengan leaderboard yang dipublikasikan. Skor ini juga tidak dapat dibandingkan dengan hasil Chartography dalam system card Claude Opus 5.5, yang menggunakan penilai berbeda dan dijalankan pada effort `max`. Dua eksekusi per konfigurasi (tiga untuk Claude Opus 5.5), digabungkan; sebaran antar-eksekusi mencapai hingga 10 poin.
    * **Cara penetapan harga:** Biaya adalah apa yang ditagihkan kepada pelanggan yang menjalankan agen secara rutin: permintaan pertama setiap grafik membaca prompt sistem dan alat bersama milik agen dari cache, sebagaimana terjadi ketika sesi lain dari agen yang sama berjalan dalam 5 menit sebelumnya. Satu grafik yang dijalankan sendiri berbiaya sekitar $0,03 USD lebih tinggi dengan Claude Opus 5 atau Claude Opus 5.5 dan sekitar $0,12 USD lebih tinggi dengan Claude Fable 5.1. Angka Agustus dihargai ulang dengan cara ini dari catatan penggunaan eksekusi. Biaya tidak termasuk waktu sandbox, yang menambahkan kurang dari 1% pada eksekusi Agustus.
    * **Claude Fable 5.1 sendirian, eksekusi Agustus:** Eksekusi Claude Fable 5.1 sendirian berasal dari 24 Agustus 2026, di bawah pengaturan penyajian peluncuran platform, dua eksekusi per pengaturan; enam percobaan mencapai batas sesi 15 menit dan mendapat skor 0, dan dua grafik per eksekusi dijawab oleh Claude Opus 5 setelah penolakan keamanan.
    * **Claude Opus 5 dengan advisor Claude Fable 5.1:** Executor Claude Opus 5 dengan effort rendah dan advisor Claude Fable 5.1 dijalankan dua kali pada 30 Agustus 2026, di bawah pengaturan yang sama (63,0 dan 67,0, rata-rata 65,0, dengan $0,47 USD per grafik; advisor dikonsultasikan pada 88% tugas di setiap eksekusi, dan 4 dari 219 balasannya berasal dari Claude Opus 5, masing-masing setelah filter keamanan produksi menghentikan balasan advisor itu sendiri). Pasangan tersebut menyamai Claude Fable 5.1 sendirian pada `medium` dalam batas noise antar-eksekusi (65,0 dibandingkan 67,5) dengan sekitar 1,8 kali biaya per tugas: konsultasi yang terpicu pada sebagian besar tugas berbiaya lebih tinggi daripada menjalankan model yang lebih kuat itu sendiri.
    * **Eksekusi Claude Opus 5.5:** Claude Opus 5.5 dijalankan pada `low`, dengan fallback sisi server dinonaktifkan dan classifier keamanan menilai setiap panggilan alat: tiga eksekusi sendirian (70, 68, dan 68) dan tiga dengan advisor Claude Fable 5.1 yang dikonfigurasi (59, 63, dan 63), di mana ia berkonsultasi dengan advisor pada 1 dari 300 tugas.
    * **Hasil pada effort `low`:** Pada benchmark pembacaan grafik ini, Claude Opus 5.5 pada `low` mencetak skor 68,7 dengan sekitar $0,03 USD per grafik, berbanding 62,5 dengan $0,15 USD dari Claude Fable 5.1 pada `low` dan 49 dengan $0,16 USD dari Claude Opus 5 pada `low`.
    * **Claude Fable 5.1 sendirian, eksekusi Oktober:** Sebagai perbandingan dengan pasangan Claude Opus 5.5, Claude Fable 5.1 sendirian pada `high`, default-nya, dijalankan tiga kali pada 7 Oktober 2026, dengan implementasi dan pengaturan platform yang sama seperti eksekusi Claude Opus 5.5: 82, 79, dan 79, rata-rata 80,0.
    * **Tingkat konsultasi:** Perbandingan tingkat konsultasi untuk pasangan-pasangan sebelumnya berasal dari menjalankan ulang konfigurasi yang sama di Messages API dengan set alat container, 10 hingga 11 Agustus 2026.

14. **Evaluasi audit prompt meja dukungan:**

    * **Apa yang diukur:** Set 44 tiket dukungan yang disusun Anthropic dengan penilaian deterministik, dijalankan pada awal Agustus 2026 dan dilaporkan pada 8 Agustus 2026, di bawah enam prompt sistem, masing-masing menambahkan ke prompt bersih yang sama satu pola yang umum dalam prompt yang ditulis untuk Claude Opus 4.8 dan Claude Sonnet 4.6.
    * **Grafik:** Setiap titik grafik adalah salah satu dari tiga kasus (model lama, model baru dengan prompt yang sama, model baru setelah audit) yang dirata-ratakan atas enam prompt dan 44 tiket.
    * **Hasil, Claude Opus 5:** Pada Claude Opus 5, prompt yang ditulis untuk Claude Opus 4.8 berbiaya 36% lebih tinggi per tiket dibandingkan pada Claude Opus 4.8, tanpa perubahan akurasi. Setelah audit, biayanya 14% lebih rendah pada Claude Opus 5 dibandingkan sebelumnya (dari rata-rata yang tidak dibulatkan; biaya yang dibulatkan pada grafik, 3,43 dan 2,93 sen AS per tiket, menghasilkan 14,6%), dan Claude Opus 5 menyelesaikan 97% tiket dengan benar, naik dari 92%. Berdasarkan pola, pada Claude Opus 5: menghapus "verify twice" memangkas biaya per tiket sepertiga, dan menghapus "be maximally thorough" memangkasnya hampir sebanyak itu; menghapus pengaturan thinking yang sudah dihentikan, aturan yang saling bertentangan, dan scratchpad buatan sendiri masing-masing memulihkan 7 hingga 11 poin akurasi.
    * **Hasil, Claude Sonnet 5:** Pada migrasi Claude Sonnet 4.6 ke Claude Sonnet 5, audit memangkas 14% biaya per tiket dengan akurasi yang sama.
    * **Catatan:** Peningkatan akurasi Opus 5 memiliki interval kepercayaan 95% sebesar 3 hingga 8 poin; perbedaan akurasi Sonnet berada dalam batas noise.

15. **Set pertanyaan file data:** Set 25 pertanyaan agregat yang disusun Anthropic atas irisan 1.862 baris dari CSV penjualan minuman keras publik, dengan ground truth yang dihitung oleh pandas dan penilaian exact-match, dijalankan pada Claude Sonnet 5 dan Claude Opus 5 dengan thinking dinonaktifkan (lengan in-context tidak dapat selesai pada default), batas output 4.000 token, dan tanpa caching prompt, tiga eksekusi per konfigurasi, dijalankan 19 Agustus 2026. Lengan file mengunggah CSV melalui Files API dan menggunakan alat `code_execution_20260120`. Tiga eksekusi Claude Sonnet 5 pada lengan in-context menjawab 6, 7, dan 7 dari 25 pertanyaan dengan benar; label grafik dan teks memberikan rata-ratanya, 6,67, dibulatkan ke pertanyaan terdekat, dan titik grafik digambar pada rata-rata, 26,7%.

16. **Pengukuran durasi cache:**

    * **Apa yang diukur:** Pekerjaan triase 20 issue dari [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens), dijalankan pada Claude Sonnet 5 pada 23 Agustus 2026, dan pada Claude Opus 5.5 pada 19 dan 20 September 2026, pada effort default-nya (`medium`) dan pada `high`, di Messages API dengan harness yang sama (untuk Claude Opus 5.5, port dari harness tersebut yang mengirimkan body permintaan yang sama), sel Claude Opus 5.5 dengan `max_tokens` dinaikkan menjadi 4.096, dengan jeda yang disisipkan sebelum porsi giliran yang dipilih secara acak (tidak ada, 5%, 10%, dan setiap giliran pada 6 menit pada seluruh 20 issue di kedua model, ditambah setiap giliran pada 2 menit pada Claude Sonnet 5; jeda 20 menit dan 45 menit pada subset 5 issue di kedua model). Angka Claude Opus 5.5 di halaman ini mencakup kedua tingkat effort.
    * **Model dan tanggal lain:** Angka keep-alive Claude Opus 5 di bawah berasal dari pekerjaan yang sama pada 23 Agustus 2026, dengan `max_tokens` dinaikkan menjadi 4.096, pada jadwal yang sama kecuali jeda 2 menit dan 45 menit. Claude Sonnet 5.5 menjalankan pengukuran yang sama seperti Claude Sonnet 5 (jadwal jeda yang sama dan tiga pengaturan cache, tiga eksekusi per sel), dengan harness port yang digunakan untuk Claude Opus 5.5, pada effort default-nya, `high`, pada 24 September 2026.
    * **Cara penilaian dan penetapan harga:** Tiga eksekusi per sel, biaya dihitung dari field `usage` setiap respons pada harga daftar (untuk Claude Opus 5.5, $4 USD input, $5 USD write 5 menit, $8 USD write 1 jam, $0,20 USD cache read, dan $20 USD output per juta token; Claude Sonnet 5 dijalankan pada organisasi internal Anthropic yang penggunaannya diukur dengan cara yang sama seperti organisasi pelanggan), akurasi terhadap gold label yang sama.
    * **Cara eksekusi dan penetapan harga, Claude Sonnet 5.5:** Claude Sonnet 5.5 menetapkan `max_tokens` ke 4.096 pada permintaan sesi dan ke 1 pada permintaan keep-alive, dijalankan pada organisasi internal Anthropic yang penggunaannya diukur dengan cara yang sama seperti organisasi pelanggan, dan dihargai pada harga daftarnya saat ini ($2 USD input, $2,50 USD write 5 menit, $4 USD write 1 jam, $0,10 USD cache read, dan $10 USD output per juta token). Selain `max_tokens` yang lebih tinggi, yang tidak dicapai oleh giliran mana pun, satu input berbeda dari eksekusi Claude Sonnet 5: satu-satunya GIF animasi dalam pekerjaan tersebut dikirim sebagai PNG dari frame pertamanya, satu-satunya frame yang digunakan API ([Vision](https://platform.claude.com/docs/id/build-with-claude/vision)), dan keduanya dihitung sebagai jumlah token input yang sama.
    * **Titik impas:** Titik impas adalah sekitar 3,3% giliran pada Claude Sonnet 5 dan 3,1% hingga 3,2% pada Claude Opus 5.5: median dari porsi titik impas setiap sesi, yang dihitung oleh model biaya dari ukuran konteks giliran demi giliran sesi tersebut, atas seluruh 45 sesi dua puluh issue Claude Sonnet 5 dan 36 sesi dua puluh issue Claude Opus 5.5 pada setiap tingkat effort (setiap jadwal jeda dijalankan pada pekerjaan lengkap, di bawah ketiga pengaturan cache, masing-masing tiga eksekusi; sel 5 issue tidak termasuk). Titik impas pada Claude Sonnet 5.5 adalah sekitar 3,1% giliran, median atas 45 sesi dua puluh issue-nya. Grafik durasi cache memplot sesi-sesi Claude Sonnet 5.5 ini, tiga per titik.
    * **Pengaturan 5 menit dan 1 jam, Claude Sonnet 5 dan Claude Opus 5.5:** Pada sel 5%, pengaturan 5 menit dan 1 jam seri pada Claude Sonnet 5, karena jeda dalam undian tersebut jatuh pada prefiks kecil; pada Claude Opus 5.5 keduanya hampir seri. Pada Claude Sonnet 5, dengan harga cache read-nya sebesar $0,20 USD per juta token, satu sesi berbiaya $0,60 USD, $0,69 USD, dan $0,99 USD pada pengaturan 5 menit tanpa jeda, dengan 5%, dan 10% giliran dijeda, serta $0,70 USD, $0,70 USD, dan $0,71 USD pada pengaturan 1 jam.
    * **Permintaan keep-alive, Claude Sonnet 5 dan Claude Opus 5:** Anthropic mengukur permintaan keep-alive yang menyegarkan cache 5 menit pada Claude Sonnet 5 dan Claude Opus 5 pada 23 Agustus 2026, dan pada Claude Opus 5.5 dalam eksekusi di atas, selalu dikirim dengan `max_tokens: 1`. Pada Claude Sonnet 5, biayanya 7,7% lebih rendah daripada pengaturan 1 jam dengan 5% giliran dijeda dan kurang lebih sama dengan 10%; pada Claude Opus 5 tidak ada perbedaan yang terukur pada kedua porsi; pada keduanya, biayanya lebih tinggi dengan jeda 6 menit atau lebih sebelum setiap giliran. Jadi pada kedua model tersebut, pengaturan yang sebaiknya digunakan adalah durasi 1 jam, bukan permintaan keep-alive.
    * **Permintaan keep-alive, Claude Opus 5.5:** Pada Claude Opus 5.5, permintaan keep-alive berbiaya 8% hingga 18% lebih rendah daripada pengaturan 1 jam dengan 5% dan 10% giliran dijeda (8% hingga 13% lebih rendah pada effort default-nya, `medium`, dan 10% hingga 18% lebih rendah pada `high`; sekitar 10% hingga 15% setelah noise antar-sesi dihilangkan dengan menagih ulang token setiap sesi keep-alive itu sendiri pada harga cache 1 jam), dan lebih tinggi dengan jeda sebelum setiap giliran: 4% hingga 6% lebih tinggi pada 6 menit, 9% hingga 10% pada 20 menit, dan 56% hingga 58% pada 45 menit.
    * **Permintaan dengan `max_tokens: 0`, Claude Opus 5.5:** Pengujian API pra-peluncuran Anthropic pada Claude Opus 5.5 menunjukkan bahwa permintaan `max_tokens: 0` menulis cache dan permintaan berikutnya membacanya; apakah permintaan semacam itu menyegarkan entri yang sudah ada tidak diukur pada Opus 5.5.
    * **Pengaturan 5 menit dan 1 jam, Claude Sonnet 5.5:** Dengan 5% giliran dijeda, pengaturan 5 menit berbiaya 5% lebih tinggi daripada pengaturan 1 jam secara rata-rata (2% lebih rendah hingga 12% lebih tinggi di ketiga eksekusi), yang masih dalam variasi antar-eksekusi: jeda dalam undian tersebut jatuh pada prefiks kecil, seperti pada Claude Sonnet 5, dan menagih ulang token setiap sesi 5 menit itu sendiri pada harga cache 1 jam menghasilkan sekitar 1% lebih tinggi. Dengan 10% dijeda, biayanya 54% lebih tinggi (36% hingga 73% lebih tinggi). Tanpa jeda, pengaturan 5 menit berbiaya 19% lebih rendah daripada pengaturan 1 jam secara rata-rata (3% hingga 32% lebih rendah di ketiga eksekusi; harga write yang lebih tinggi pada pengaturan 1 jam memprediksi sekitar 20%), dan 21% hingga 24% lebih rendah di setiap eksekusi dengan jeda 2 menit.
    * **Permintaan keep-alive, Claude Sonnet 5.5:** Permintaan keep-alive berbiaya 16% lebih rendah daripada pengaturan 1 jam secara rata-rata dengan 5% giliran dijeda (13% hingga 20% lebih rendah di ketiga eksekusi) dan 8% lebih rendah dengan 10% (3% hingga 10% lebih rendah), dan berbiaya lebih tinggi dengan jeda 6 menit atau lebih sebelum setiap giliran. Dengan 5% dan 10% giliran dijeda, jeda berlangsung 6 hingga 32 menit pada Claude Sonnet 5.5 dan pada Claude Opus 5.5. Menagih ulang token setiap sesi keep-alive itu sendiri pada harga cache 1 jam, seperti untuk Claude Opus 5.5 di atas, menghasilkan 15% hingga 16% lebih rendah pada 5% dijeda dan sekitar 10% lebih rendah pada 10%, dan dengan jeda sebelum setiap giliran 7% lebih tinggi pada 6 menit, 9% hingga 10% lebih tinggi pada 20 menit, dan 66% hingga 73% lebih tinggi pada 45 menit. Angka 6 menit mengecualikan eksekusi 3, di mana 2 dari 39 permintaan keep-alive sesi tersebut mengalami timeout: cache kedaluwarsa sebelum kedua giliran tersebut, sesi menulis 214.000 token ke cache berbanding 80.000 hingga 85.000 pada eksekusi 1 dan 2, dan biayanya 38% lebih tinggi daripada sesi 1 jam eksekusi 3.
    * **Permintaan keep-alive, Claude Sonnet 5.5, per eksekusi:** Jika membandingkan sesi keep-alive setiap eksekusi dengan sesi 1 jam dari eksekusi yang sama, keep-alive berbiaya dari kurang lebih sama hingga 10% lebih tinggi pada 6 menit (eksekusi 1 dan 2; 4% lebih tinggi pada rata-ratanya), dari kurang lebih sama hingga 16% lebih tinggi pada 20 menit, dan 64% hingga 80% lebih tinggi pada 45 menit.
    * **Permintaan keep-alive, Claude Sonnet 5.5, ukuran sampel:** Titik 6 menit pada grafik keep-alive merata-ratakan eksekusi 1 dan 2 untuk ketiga pengaturan. Setiap sel terdiri dari tiga sesi (dua untuk angka 6 menit di atas). Tanpa jeda, keep-alive tidak mengirimkan permintaan tambahan sehingga sama dengan pengaturan 5 menit, namun keduanya berbeda hingga 23% dalam satu eksekusi, sehingga perbedaan beberapa persen dalam rata-rata tiga eksekusi bukanlah efek yang jelas.
    * **Caching nonaktif dan aktif, Claude Sonnet 5:** Pada Claude Sonnet 5, pekerjaan yang sama dijalankan dengan caching nonaktif dan dengan caching aktif, masing-masing tiga eksekusi pada 19 Agustus 2026, dengan `max_tokens` pada 700: $3,36 USD berbanding $0,57 USD per sesi secara rata-rata, penghematan 83%.
    * **Dihargai dari jumlah token yang tercatat, Claude Sonnet 5.5:** Anthropic juga menghitung ulang harga jumlah token yang tercatat dari tiga sesi Claude Sonnet 5.5 dengan cache 5 menit dan tanpa jeda untuk angka caching di [Mengapa caching didahulukan](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#why-caching-comes-first); Anthropic tidak melakukan eksekusi dengan caching nonaktif pada Claude Sonnet 5.5. Masing-masing dari ketiga sesi ini adalah satu percakapan berisi 40 permintaan atas 20 issue pekerjaan tersebut. Pada harga daftar per 12 Oktober 2026, sesi-sesi tersebut berbiaya rata-rata $0,51 USD masing-masing, dari field penggunaan, berbanding $3,70 USD dengan setiap token input pada harga input dan token output tidak berubah: penghematan 86% (86% hingga 87% di ketiga sesi), atau faktor 7,3. Pada harga cache read peluncuran sebesar $0,20 USD, penghematannya 82%, sehingga kenaikan dibandingkan angka Claude Sonnet 5 berasal dari harga cache read yang lebih rendah.
    * **Dihargai dari jumlah token yang tercatat, Claude Opus 5.5:** Dihargai ulang dengan cara yang sama, tiga sesi Claude Opus 5.5 pada effort default-nya, `medium`, dengan cache 5 menit dan tanpa jeda berbiaya rata-rata $1,02 USD masing-masing berbanding $6,93 USD, penghematan 85%, atau faktor 6,8; Anthropic tidak melakukan eksekusi dengan caching nonaktif pada Claude Opus 5.5, dan model menggunakan thinking pada 79% permintaan.
    * **Cara thinking ditetapkan, hanya dua set eksekusi:** Permintaan dari tiga sesi Claude Sonnet 5.5 dengan cache 5 menit dan tanpa jeda tidak menetapkan opsi thinking, sehingga thinking dibiarkan pada default model, dan model menggunakannya pada 38% permintaan. Permintaan dari eksekusi Claude Sonnet 5 dengan caching nonaktif dan dengan caching aktif juga tidak menetapkan opsi thinking, sehingga thinking dibiarkan pada default model, dan model menggunakannya pada 41 dari 121 permintaan dengan caching nonaktif dan 40 dari 120 dengan caching aktif.
    * **Latensi setelah jeda:** Pada Claude Sonnet 5 dan Claude Opus 5, giliran setelah jeda mempertahankan latensi cache hangatnya pada pengaturan 1 jam. Waktu hingga token pertama Claude Opus 5.5 setelah jeda tidak diukur. Waktu hingga token pertama Claude Sonnet 5.5 setelah jeda tidak diukur.

17. **Porsi cache read dalam produksi:** Penggunaan Claude API pihak pertama yang diagregasi selama 14 hari yang berakhir 23 Agustus 2026, hanya produk API langsung, organisasi internal Anthropic dikecualikan, tidak ada organisasi yang diidentifikasi. Satu hari-organisasi dihitung sebagai loop agen ketika permintaannya membawa definisi alat dan hasil alat, prompt-nya memuat rata-rata 9 atau lebih panggilan alat sebelumnya, caching digunakan, dan organisasi tersebut membuat setidaknya 10 permintaan semacam itu (API tidak memiliki pengidentifikasi percakapan, sehingga ini menjadi pengganti panjang percakapan): 303.003 hari-organisasi di 106.487 organisasi, median porsi cache read 84,2% dari seluruh token input, kuartil atas 91,7%. Label kasus penggunaan (kasus penggunaan yang dinyatakan organisasi, atau jika tidak ada, yang diklasifikasikan) mencakup 74% dari hari-organisasi tersebut dan 99% tokennya; sekitar 72% hari-organisasi coding membaca 80% atau lebih. Desil teratas hari-organisasi membaca 95,9% atau lebih untuk coding dan 94,2% hingga 94,8% untuk agen dukungan, riset, data, dan lainnya. Pembagian tingkat permintaan pada 25 atau lebih panggilan alat sebelumnya berasal dari sampel enam jam: coding 92% read, 7% write, kurang dari 1% tanpa cache.

18. **Pengukuran waktu compaction dan status line:**

    * **Apa yang diukur:** Varian panjang agen triase dari [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens), dijalankan 24 Agustus 2026, pada Claude Sonnet 5 dengan cache 5 menit, biaya dari field penggunaan pada harga daftar, lima sesi per lengan: lengan tanpa perubahan pada effort default sepanjang waktu ($0,81 USD per sesi), dan dua lengan yang dimulai pada effort rendah dan membuat dua perubahan yang sama yang merusak cache, yaitu peralihan ke effort default dan satu alat tambahan, baik di tengah sesi pada permintaan 12 dan 17 ($0,95 USD) atau bersamaan pada permintaan pertama setelah compaction pertama ($0,75 USD).
    * **Lengan keempat:** Lengan keempat dengan enam sesi, dijalankan 25 Agustus 2026, membuat dua perubahan yang sama pada permintaan yang memicu compaction pertama ($0,92 USD per sesi): proses peringkasan permintaan tersebut menulis konteks 81.000 token ke cache alih-alih membacanya, sehingga proses tersebut berbiaya $0,21 USD berbanding $0,04 USD untuk proses yang sama di lengan batas.
    * **Compaction:** Sesi pertama kali melakukan compaction pada permintaan 21 hingga 25 (16 dari 21 sesi pada permintaan 22), setelah prompt melewati pemicu compaction 80.000 token, dan dua sesi tanpa perubahan melakukan compaction kedua kalinya menjelang akhir. Total lengan batas yang lebih rendah dibandingkan lengan tanpa perubahan mencerminkan permintaan effort rendahnya sebelum perubahan dan compaction kedua tersebut, bukan caching: biaya penulisan ulang kedua lengan berbeda kurang dari $0,01 USD.
    * **Lengan tengah sesi:** Lengan tengah sesi membayar $0,23 USD per sesi untuk penulisan ulang cache; perbedaan antara lengan tengah sesi dan lengan batas adalah $0,20 USD dengan interval kepercayaan 95% sebesar $0,11 USD hingga $0,29 USD. Di lengan tengah sesi, perubahan effort dan alat tambahan menulis ulang 39.000 dan 60.000 token yang di-cache. Salah satu sesinya berjalan murah ($0,82 USD) setelah modelnya salah memanggil alat pencarian setelah compaction dan mendapatkan hasil kosong; sesi tersebut disertakan, dan tanpanya lengan tersebut rata-rata $0,98 USD.
    * **Akurasi dan cache read:** Akurasi rata-rata 14,2 dari 20 label di setiap lengan 24 Agustus dan 14,7 di lengan 25 Agustus; cache read adalah 91% token prompt tanpa perubahan, 85% di tengah sesi, 91% di batas, dan 86% dengan perubahan pada permintaan pemicu.
    * **Pengukuran terpisah, status line:** Pengukuran terpisah pada pekerjaan triase 20 issue dari [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens), dijalankan 18 Agustus 2026, juga pada Claude Sonnet 5 dengan cache 5 menit, dihargai dengan cara yang sama, tiga eksekusi per lengan: dengan status line 25 token di awal prompt sistem, satu eksekusi berbiaya rata-rata $4,24 USD ($4,12 USD hingga $4,47 USD di ketiga eksekusi) dan tidak membaca apa pun dari cache; dengan baris yang sama di akhir giliran pengguna terbaru, setelah breakpoint cache terakhir, satu eksekusi berbiaya $0,59 USD ($0,55 USD hingga $0,61 USD). Yang pertama lebih mahal daripada biaya pekerjaan yang sama dengan caching nonaktif. Eksekusi ulang kemudian dengan konfigurasi yang sama menghasilkan $4,28 USD dan $0,61 USD.

19. **Pengukuran durasi cache pada Claude Fable 5.1:** Pekerjaan triase 20 issue dan harness yang sama seperti referensi 16, dengan `max_tokens` dinaikkan menjadi 4.096, dijalankan 23 Agustus dan 26 Agustus 2026, pada snapshot peluncuran Claude Fable 5.1 dengan harga peluncurannya ($10 USD input, $12,50 USD write 5 menit, $20 USD write 1 jam, $0,25 USD cache read, $50 USD output per juta token), tiga pengaturan per jadwal: cache 5 menit, cache 1 jam, dan cache 5 menit yang dijaga tetap hangat oleh permintaan `max_tokens: 0` pada prefiks yang tidak berubah setiap 4 menit, dihitung dari awal permintaan sebelumnya (eksekusi 23 Agustus mengirimkan permintaan keep-alive dengan `max_tokens: 1`; pada sel 26 Agustus yang dilaporkan di sini, setiap permintaan keep-alive yang dijawab menyegarkan cache dan responsnya melaporkan tidak ada token output). Jadwal: tanpa jeda, 10% giliran, dan setiap giliran pada 6 menit pada seluruh 20 issue, serta jeda 45 menit pada subset 5 issue; tiga eksekusi per sel (enam untuk sel keep-alive 26 Agustus dengan jeda 45 menit), biaya dihitung dari field `usage` setiap respons pada harga daftar, akurasi terhadap gold label yang sama (12 hingga 18 label tepat dari 20). Rata-rata per sesi pada 26 Agustus untuk pengaturan 5 menit, 1 jam, dan keep-alive: tanpa jeda $2,42 USD, $3,09 USD, $2,29 USD; 10% dijeda $4,50 USD, $2,96 USD, $2,36 USD; setiap giliran $22,89 USD, $3,01 USD, $2,62 USD; sel 23 Agustus sesuai dalam batas 6%. Angka 45 menit ($1,68 USD, $0,59 USD, dan $0,71 USD per sesi 5 issue) berasal dari sesi-sesi selanjutnya pada 26 Agustus: set sesi pertama hari itu terputus ketika mesinnya dimatikan, dan set kedua terdampak oleh gangguan layanan dan dikesampingkan. Set ketiga memberikan angka 5 menit dan 1 jam; tiga sesi keep-alive-nya mengirimkan setiap permintaan keep-alive sekali, kehilangan permintaan karena penolakan batas laju, dan tidak termasuk dalam rata-rata. Angka keep-alive adalah rata-rata dari enam sesi tambahan yang mengirimkan kembali setiap permintaan keep-alive yang ditolak dalam dua detik. Eksekusi 23 Agustus menghasilkan $1,67 USD, $0,58 USD, dan $0,70 USD. Titik impas antara pengaturan 5 menit dan 1 jam adalah 3,1% giliran, ukuran yang sama seperti referensi 16. Cache read Claude Fable 5.1 berbiaya 0,025x harga input sementara cache write-nya mempertahankan pengali standar, sehingga permintaan keep-alive yang membaca ulang prefiks itu murah dan premi write durasi 1 jam menjadi tagihan yang lebih besar, kecuali dengan jeda 45 menit, di mana permintaan keep-alive berbiaya lebih tinggi daripada premi tersebut.

20. **Terminal-Bench 3:** 74 tugas dari benchmark agen terminal publik, dijalankan di [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) dengan dua alat kustom, yaitu shell dan editor file yang dijalankan harness evaluasi di container masing-masing tugas, sebagai pengganti alat bawaan platform, dan selebihnya pada pengaturan default platform untuk akun eksternal, dua eksekusi per model pada effort `high`, 27 hingga 28 Agustus 2026. Eksekusi ini menggunakan Terminal-Bench versi 3.0, dan skornya tidak dapat dibandingkan dengan leaderboard Terminal-Bench publik atau dengan hasil Terminal-Bench 4.0 dalam system card Claude Opus 5.5, yang berasal dari eksekusi di Claude Code pada effort `max`. Batas waktu setiap tugas adalah 2,5 kali batas benchmark itu sendiri, yang memberi agen antara 75 menit dan 20 jam per tugas (5 jam untuk tugas median), dan setiap tugas mendapatkan tiga kali memori yang ditentukannya, dari 6 GiB hingga 96 GiB, dengan memori tambahan untuk 12 tugas yang menjalankan layanan pembantu. Agen tidak memiliki akses internet umum: container-nya dapat menjangkau mirror paket internal, daftar pendek situs unduhan termasuk GitHub dan Python Package Index, serta beberapa situs khusus untuk sebagian tugas, dan delapan tugas tidak memiliki akses jaringan sama sekali. Skor adalah tingkat kelulusan mentah atas 148 percobaan per model; eksekusi tunggal berayun 5 hingga 11 poin. Biaya adalah apa yang akan ditagihkan kepada pelanggan pada harga daftar, dihargai ulang permintaan demi permintaan dari catatan penggunaan eksekusi dengan masa hidup cache 5 menit. Claude Opus 4.7, Claude Opus 4.8, dan Claude Opus 5 masing-masing menghabiskan $8 USD hingga $15 USD per tugas. Claude Opus 4.7 mengakhiri 11 dari 148 percobaannya pada batas output-nya.

21. **DRACO:** Perplexity, "DRACO: a Cross-Domain Benchmark for Deep Research Accuracy, Completeness, and Objectivity," arXiv:2602.11685, 2026.

    * **Apa yang diukur:** 100 tugas risetnya di 10 domain dinilai terhadap rubrik yang ditulis pakar dengan masing-masing sekitar 40 kriteria berbobot, dan skornya adalah porsi berbobot dari kriteria yang terpenuhi, dari 0 hingga 100.
    * **Konfigurasi:** Setiap konfigurasi dijalankan di Claude API dengan Claude Opus 5.5, adaptive thinking default, classifier keamanan produksi aktif, dan `max_tokens` pada 128.000 dengan streaming: agen tunggal pada effort `medium` (default model) dan pada `low`, agen tunggal pada `medium` dengan kalimat dan jam, serta tim pada `medium` dengan dan tanpa keduanya. Tim tersebut adalah agen utama yang dapat memulai agen pembantu dari model yang sama melalui sebuah alat, tanpa batas jumlah.
    * **Kalimat:** Kedua perubahan tersebut adalah sebuah kalimat dan sebuah jam. Kalimat tersebut, "Time matters here: do not spend time that can be avoided, and the earlier a correct result is obtained, the better.", ditempatkan di akhir tugas dalam pesan `user` pertama agen, setelah baris kosong, dan di akhir brief setiap pembantu.
    * **Jam:** Jam adalah waktu yang telah berlalu dalam detik bulat, seperti `[elapsed 252s]`, yang ditambahkan sebelum setiap permintaan, termasuk yang pertama, ke akhir pesan `user` terbaru: dalam blok teksnya sendiri setelah tugas pada permintaan pertama, dan di akhir teks hasil alat terakhir, setelah baris kosong, ketika pesan membawa hasil alat. Jam-jam sebelumnya tetap di tempatnya, sehingga prefiks yang di-cache tetap cocok pada permintaan berikutnya. Setiap agen dalam tim membaca jam yang sama, dan prompt sistem tidak berubah.
    * **Dalam eksekusi yang diukur:** Eksekusi yang diukur menggunakan kata-kata dan format ini. Jamnya dimulai pada token pertama dari respons pertama, bukan pada awal tugas. Dalam eksekusi tim yang diukur, laporan pembantu mencapai agen utama dalam pesan terpisah setelah jam, bukan di dalam hasil alat terakhir.
    * **Kapan:** Setiap konfigurasi melakukan tiga percobaan pada setiap tugas, dengan batas empat jam per percobaan, dijalankan 24 September 2026, dan semua konfigurasi dalam satu set dimulai bersamaan.
    * **Alat:** Agen menggunakan alat pencarian dan fetch yang di-host oleh harness evaluasi atas indeks web Anthropic, serta Python dan shell dalam sandbox tanpa akses jaringan. Alat-alat tersebut menentukan sebagian waktu, dan alat Anda akan berjalan dengan kecepatan berbeda, sehingga halaman ini menyajikan waktu sebagai rasio antar-konfigurasi, bukan dalam menit.
    * **Cara pengukuran waktu:** Waktu adalah waktu wall-clock dari suatu percobaan, dari permintaan pertamanya hingga akhir permintaan terakhir oleh agen mana pun, termasuk eksekusi alat, dirata-ratakan atas percobaan-percobaan suatu tugas. Angka tugas tipikal adalah median, atas tugas-tugas, dari rasio setiap tugas antara dua konfigurasi.
    * **Cara penetapan harga:** Biaya setiap tugas adalah permintaannya yang dihargai pada harga daftar publik Claude Opus 5.5, dengan caching prompt ditagih sebagaimana untuk pelanggan yang menetapkan breakpoint cache di akhir setiap permintaan dan menggunakan masa hidup cache 5 menit. Setiap permintaan membaca prompt permintaan sebelumnya dari cache dan menulis sisanya. Permintaan pertama suatu percobaan, dan setiap permintaan yang dimulai lebih dari 5 menit setelah permintaan sebelumnya, menulis seluruh prompt-nya. Biaya hanya mencakup token model; alat harness tidak menambahkan biaya.
    * **Cara penilaian:** Semua interval adalah interval bootstrap 95% atas tugas-tugas, dan perubahan skor adalah selisih berpasangan atas tugas-tugas. Claude Opus 5 menilai jawaban, sehingga Claude Opus 5.5 tidak menilai pekerjaannya sendiri, dan skor setiap jawaban merata-ratakan lima eksekusi penilaian.
    * **Catatan:** Classifier keamanan produksi menghentikan tiga percobaan di setiap konfigurasi, semuanya pada satu tugas, dan percobaan tersebut mendapat skor 0; mengecualikan tugas tersebut tidak mengubah temuan apa pun. Eksekusi tersebut juga melewatkan penggunaan alat setiap agen melalui pemeriksaan keamanan internal Anthropic yang tidak dimiliki permintaan pelanggan, yang menambahkan waktu yang tidak terukur pada setiap permintaan di setiap konfigurasi. Pada DRACO, agen tunggal tanpa perubahan membuat sekitar dua kali lebih banyak permintaan, dan tim sekitar sepertiga lebih banyak, sehingga pemeriksaan tersebut kemungkinan membuat penghematan waktu DRACO tampak sedikit lebih besar.
    * **Hasil, agen tunggal:** Hasil untuk [Tunjukkan waktu yang telah berlalu kepada model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#show-the-model-elapsed-time): dengan perubahan tersebut, agen tunggal membutuhkan waktu 47% lebih sedikit dengan biaya 60% lebih rendah pada tugas tipikal, biaya rata-ratanya turun dari $1,13 USD menjadi $0,44 USD per tugas, dan skornya 4,1 poin lebih rendah (interval 95% 2,9 hingga 5,2 lebih rendah).
    * **Hasil, effort lebih rendah:** Menurunkan effort agen tunggal menghemat lebih banyak waktu dan biaya daripada perubahan tersebut, dan kehilangan lebih banyak skor. Pada effort `low`, ia mencetak skor 13,3 poin lebih rendah pada DRACO, 3,4 pada HLE, dan 14,0 pada set fisika dibandingkan pada `medium`, dan tugas tipikal membutuhkan waktu 84%, 30%, dan 47% lebih sedikit. Dengan perubahan tersebut pada effort `medium`, ia mencetak skor 9,2, 2,5, dan 11,0 poin lebih tinggi daripada pada `low`, dan tugas tipikal membutuhkan waktu lebih lama daripada pada `low` dengan faktor 1,2 hingga 3,2.
    * **Hasil, tim, pembantu:** Agen utama tim jarang memulai pembantu. Tanpa perubahan tersebut, ia memulai pembantu hanya pada 5 dari 300 percobaan di DRACO, 13 dari 1.479 di HLE, dan tidak ada dari 280 di set fisika.
    * **Hasil, tim:** Jadi hasil tim sebagian besar menunjukkan agen utama bekerja sendirian, dengan instruksi dan alat milik tim itu sendiri, dan Anthropic tidak memiliki pengukuran perubahan tersebut pada tim yang bekerja secara paralel. Tanpa perubahan tersebut, tim sudah membutuhkan sekitar setengah waktu agen tunggal pada tugas DRACO tipikal, dan mencetak skor 3,3 poin lebih rendah (interval 95% 2,1 hingga 4,6 lebih rendah). Dengan perubahan tersebut, tim membutuhkan waktu 17% lebih sedikit dengan biaya 20% lebih rendah pada tugas DRACO tipikal, dan mencetak skor 1,6 poin lebih rendah (interval 95% 0,3 hingga 2,8 lebih rendah).
    * **Tidak diukur:** Anthropic tidak mengukur perubahan tersebut di Claude Managed Agents.

22. **HLE:** Phan et al., "Humanity's Last Exam," arXiv:2501.14249, 2025. Pertanyaan yang ditulis pakar dengan jawaban pasti, dinilai terhadap jawaban referensi. Diukur pada 500 pertanyaan pertama dari rilis 10 September 2025, termasuk gambar, dengan sumber benchmark itu sendiri diblokir dari pencarian, dan pengaturan yang sama seperti referensi 21. Setiap konfigurasi melakukan tiga percobaan pada setiap pertanyaan, dijalankan 24 September 2026. Claude Opus 5 membandingkan setiap jawaban dengan jawaban referensi, menggunakan prompt penilai yang dipublikasikan benchmark, dan mayoritas dari tiga penilaian yang dihitung. Skor mencakup 493 pertanyaan di setiap konfigurasi. Untuk lima pertanyaan lainnya, permintaan penilaian melebihi batas 1M token penilai, dan dua lainnya dikecualikan karena eksekusi agen tunggal tanpa perubahan berhenti sebelum tiga percobaannya pada pertanyaan tersebut selesai. Rasio waktu dan biaya mencakup 492 pertanyaan untuk agen tunggal dan 491 untuk tim, karena satu atau dua pertanyaan tidak memiliki data waktu. Classifier keamanan produksi menghentikan 3% hingga 4% percobaan setiap konfigurasi, dan percobaan tersebut mendapat skor 0; mengecualikannya tidak mengubah temuan apa pun. Hasil untuk [Tunjukkan waktu yang telah berlalu kepada model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#show-the-model-elapsed-time): dengan perubahan tersebut, agen tunggal membutuhkan waktu 14% lebih sedikit dengan biaya 9% lebih rendah pada pertanyaan tipikal. Dengan penilai Claude Opus 5, skornya tidak menunjukkan perubahan yang jelas (0,9 poin lebih rendah, interval 95% 2,5 lebih rendah hingga 0,7 lebih tinggi). Dengan penilai kedua, Claude Opus 4.6, skornya 1,9 poin lebih rendah (interval 95% 0,2 hingga 3,7 lebih rendah). Waktu rata-rata turun lebih jauh daripada pertanyaan tipikal: waktu rata-rata turun 43% dan biaya rata-rata 37%, karena perubahan tersebut memotong beberapa pertanyaan yang sangat panjang. Waktu tim pada pertanyaan tipikal berubah 3% atau kurang, dan skornya tidak berubah secara jelas.

23. **Set fisika:** Set internal berisi 70 soal fisika tingkat riset, diadaptasi dari benchmark CritPt publik: Zhu et al., "Probing the Critical Point (CritPt) of AI Reasoning: a Frontier Physics Research Benchmark," arXiv:2509.26574, 2025. Peninjau pakar mengoreksi pernyataan soal. Claude Opus 4.6 menilai setiap jawaban dengan kredit parsial, menggunakan prompt penilaian set tersebut, terhadap solusi referensi pakar yang tidak dipublikasikan, sehingga skornya tidak dapat dibandingkan dengan hasil yang dipublikasikan. Skornya adalah nilai rata-rata atas percobaan-percobaan suatu soal, dirata-ratakan atas soal-soal, dalam poin dari 100. Diukur pada seluruh 70 soal, empat percobaan per soal, dijalankan 24 September 2026. Setiap agen memiliki alat Python, shell, dan editor file dalam container sandbox tanpa akses jaringan, serta tanpa alat pencarian atau fetch. Tidak ada classifier keamanan yang menghentikan percobaan pada set fisika. Selebihnya, pengaturannya sama dengan referensi 21. Hasil untuk [Tunjukkan waktu yang telah berlalu kepada model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#show-the-model-elapsed-time): dengan perubahan tersebut, agen tunggal membutuhkan waktu 7% lebih sedikit dengan biaya 4% lebih rendah pada soal tipikal, dan skornya 3,0 poin lebih rendah (interval 95% 0,4 hingga 5,6 lebih rendah). Waktu tim pada soal tipikal berubah 3% atau kurang, dan skornya tidak berubah secara jelas. Waktu rata-rata agen tunggal turun 14%. Seluruh penghematan waktu rata-rata agen tunggal berasal dari satu soal, di mana agen tanpa perubahan menjalankan kode selama sekitar setengah jam per percobaan; tanpa soal tersebut, waktu rata-ratanya kurang lebih sama dengan dan tanpa perubahan.

24. **tau2-bench retail:** Barres et al., "τ²-Bench: Evaluating Conversational Agents in a Dual-Control Environment," arXiv:2506.07982, 2025.

    * **Apa yang diukur:** 114 tugas domain retail dijalankan pada harness publik terhadap Claude API, dengan Claude Haiku 4.5 sebagai pengguna simulasi, Claude Sonnet 5 sebagai penilai bahasa alami, dan caching prompt aktif; tugas-tugas dibagi menjadi 57 untuk pencarian dan 57 held-out.
    * **Kapan:** Kedua pencarian dijalankan pada 6 September 2026, digerakkan oleh perintah `hillclimb` dari skill Claude API. Pasangan sebelum-dan-sesudah caching dijalankan pada 8 September 2026.
    * **Cara penilaian:** Dalam pencarian, titik awal dan konfigurasi yang dikonfirmasi adalah rata-rata dari tiga eksekusi held-out, langkah yang dipertahankan dinilai pada dua eksekusi, dan kandidat lain dinilai pada satu atau dua eksekusi. Pasangan caching: masing-masing tiga eksekusi pada seluruh 114 tugas dengan hanya breakpoint cache harness yang diubah, konfigurasi yang dihasilkan perintah `cost-optimize` dalam eksekusi sebelumnya. Angka held-out berasal dari 57 tugas yang tidak pernah dibaca oleh pencarian.
    * **Cara penetapan harga:** Biaya per tugas menghitung harga jumlah token agen dan pengguna simulasi pada harga daftar (Claude Opus 5 $5 USD dan $25 USD, Claude Sonnet 5 $2 USD dan $10 USD per juta token input dan output, cache read dan write pada tarif yang dipublikasikan) dan tidak termasuk penilai; perubahan persentase berasal dari biaya yang tidak dibulatkan; angka bulanan adalah token agen saja, $0,135 USD dan $0,047 USD per tugas, dikalikan 10.000. Pada 10.000 percakapan per bulan, itu sekitar $1.350 USD sebelum pencarian pertama dan $470 USD sesudahnya.
    * **Catatan:** Pengukuran ini dijalankan pada model Claude Opus dan Claude Sonnet sebelumnya: pasangan caching dijalankan pada Claude Sonnet 5, pencarian kedua dimulai dari Claude Sonnet 5, dan pencarian pertama beralih dari Claude Opus 5 ke Claude Sonnet 5. Claude Fable 5.1 tidak diukur pada benchmark ini.
    * **Pasangan caching:** Pasangan tersebut dijalankan pada Claude Sonnet 5 pada effort default. Harness publik, sebagaimana dirilis, mengirimkan seluruh percakapan tanpa cache pada setiap giliran. Konfigurasi dengan cache memiliki satu breakpoint pada prompt sistem dan satu pada pesan terbaru. Kedua pencarian dijalankan dengan caching tersebut aktif. Biaya per tugas turun dari $0,223 USD tanpa cache menjadi $0,062 USD dengan cache, penghematan 72%, dan tingkat kelulusan dari 79,2% menjadi 76,0%. Eksekusi identik dengan cache dari konfigurasi tersebut berkisar dari 85 hingga 93 dari 114 di berbagai hari. Setiap eksekusi dengan cache mencetak skor sama dengan atau di bawah setiap eksekusi tanpa cache, tetapi selisih kurang dari 4 tugas berada di dalam sebaran eksekusi identik dengan cache, sehingga perubahan akurasi terlalu kecil untuk diukur pada ukuran sampel ini.
    * **Cara pencarian berjalan.** Perintah `hillclimb` mengajukan empat pertanyaan, menyajikan rencana, dan menunggu persetujuan sebelum menghabiskan apa pun. Dalam pencarian pertama, rencana tersebut membiarkan simulator pengguna, penilai, caching, temperature, dan tugas tidak berubah. Pertanyaan terakhir dari keempat pertanyaan tersebut dimulai dengan: `One pass over the full set is 114 cases x 1 rep on claude-opus-5, roughly 22 minutes.` Setiap putaran, pencarian mengusulkan satu perubahan dan menjalankan set lengkap. Pencarian mempertahankan perubahan hanya ketika angkanya bergerak dan mekanisme yang diprediksi terlihat dalam data penggunaan. Pencarian berhenti ketika tiga putaran berturut-turut tidak menghasilkan apa pun, lalu mengonfirmasi pemenangnya pada eksekusi baru.
    * **Pencarian pertama, hasil.** Pencarian memangkas biaya per tugas sebesar 61% sambil mempertahankan tingkat kelulusan dalam rentang 2 poin yang ditetapkan sebelum pencarian: dari Claude Opus 5 pada effort default ($0,142 USD per tugas, 76,0% lulus) ke Claude Sonnet 5 pada `low` dengan satu suntingan prompt yang netral biaya ($0,055 USD, 74,3%). Pencarian tersebut berbiaya $179 USD untuk eksekusi evaluasi dan $228 USD untuk tokennya sendiri.
    * **Pencarian pertama, awal: Claude Opus 5, effort default.** 76,0% dengan $0,142 USD. Tiga eksekusi identik berkisar 43 hingga 44 dari 57. Pencarian menetapkan batas bawah 2 poin di bawahnya, pada 74,0%, dan membulatkannya ke atas menjadi 43 dari 57 (75,4%) untuk keputusannya.
    * **Pencarian pertama, langkah 1, effort ke `low`: dipertahankan.** 77,2% pada dua eksekusi yang mempertahankannya, 77,8% pada konfirmasi tiga eksekusi setelah pencarian, dengan $0,119 USD, 17% lebih murah. Status line pencarian itu sendiri berbunyi, sebagian: `two runs held-out 42 and 46, mean 44.0 >= floor 43; cost mean $0.1187 <= gate $0.1208; mechanism confirmed (output tokens -34% with calls flat)`.
    * **Pencarian pertama, langkah 2, Claude Sonnet 5 pada `low`: dipertahankan.** 75,4% dengan $0,055 USD, 61% lebih murah.
    * **Pencarian pertama, langkah 3, suntingan prompt (mencari pesanan pelanggan setelah login alih-alih meminta ID pesanan): dipertahankan saat seleksi, lalu tidak bertahan.** 79,8% pada dua eksekusi; 74,3% pada tiga eksekusi baru. Pencarian membiarkannya sebagai netral biaya: giliran yang dibebaskan menjadi giliran pencarian lainnya.
    * **Pencarian pertama, langkah 4, suntingan prompt (transfer ke manusia hanya ketika diminta): ditolak dan dikembalikan.** 71,9%. Suntingan ini memperbaiki 3 kasus yang ditargetkannya dan merusak 10 kasus lainnya dengan templat generik "sebutkan apa yang dapat dan tidak dapat Anda lakukan".
    * **Pencarian pertama, langkah 5, suntingan prompt: tidak dijalankan.** Prediksi peningkatannya sebesar 0,5 tugas berada di bawah gerbang adopsi 2 tugas milik pencarian.
    * **Pencarian pertama, konfirmasi: Claude Sonnet 5 pada `low` dengan prompt langkah 3, tiga eksekusi baru.** 74,3% dengan $0,055 USD, di dalam rentang 2 poin dengan selisih 0,14 tugas, 1 tugas dari 57 di bawah titik awal, dan di bawah batas bawah 43 dari 57 yang dicatat pencarian. Lima eksekusi konfigurasi ini berkisar 42 hingga 46, lebih lebar daripada 43 hingga 44 pada titik awal.
    * **Pencarian pertama, apa yang ditunjukkannya.** Tuas effort dan model menghasilkan penghematan, dan mekanisme masing-masing mengonfirmasinya. Tuas prompt menghasilkan perubahan perilaku yang nyata tetapi tidak ada peningkatan yang bertahan. Pada beban kerja ini, jumlah giliran dan prefiks yang di-cache yang dibaca ulang setiap giliran menentukan biaya per tugas, bukan kata-katanya.
    * **Pencarian kedua.** Pencarian ini dimulai dari Claude Sonnet 5 pada effort default dengan caching aktif: 79,5% dengan $0,062 USD pada separuh held-out, dengan tiga eksekusi berkisar 42 hingga 47 dari 57, sehingga batas bawahnya adalah 45 dari 57 (78,9%). Eksekusi identik dari konfigurasi awal berbeda hingga 5 tugas dari 57 di sini. Pencarian kedua tidak mempertahankan apa pun. Effort pada `low`, dua suntingan prompt, dan keduanya bersamaan masing-masing mencetak skor 77,2%, di bawah batas bawah, dan menghemat 10% hingga 14%, kurang dari gerbang biaya 15% milik pencarian. Suntingan prompt untuk akurasi mencetak skor 79,8% pada dua eksekusi dan 73,7% pada tiga eksekusi baru, dan dikembalikan. Pencarian tersebut membutuhkan sekitar 19 eksekusi evaluasi dan $120 USD.

25. **Set tugas Claude Managed Agents:**

    * **Apa yang diukur:** Set internal Anthropic berisi 79 tugas agen terskrip dalam delapan area, termasuk pekerjaan memori, multi-agen, dan konteks panjang, dijalankan sebagai sesi [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) di mana pengujian menjawab setiap panggilan alat. Setiap tugas dijalankan lima kali per model.
    * **Eksekusi:** Angka-angka berasal dari satu eksekusi per model pada 7 Oktober 2026, dinilai pada hari itu. Dalam tiga eksekusi tambahan dari tugas yang sama pada 8 dan 9 Oktober 2026, Claude Haiku 5.5 lulus 91% hingga 93% percobaan, dan dalam satu eksekusi tambahan pada 8 Oktober, Claude Haiku 4.5 lulus 63%.
    * **Cara penilaian:** Suatu percobaan lulus hanya jika penilai, Claude Sonnet 4.6, yang menilai sekali, menandai setiap baris checklist tugas sebagai terpenuhi, sehingga tingkat kelulusan bergantung pada penilai. Pada semua tugas kecuali satu, panggilan terpisah, yang diperlihatkan hasil alat secara lengkap, menilai baris yang memeriksa file dan pesan yang ditulis agen melalui alatnya terhadap hasil tersebut.
    * **Cara penetapan harga:** Biaya adalah biaya token pada harga daftar dengan caching prompt 5 menit, dihargai permintaan demi permintaan, dan tidak termasuk runtime sesi.
    * **Hasil, harga token dan biaya:** Claude Haiku 4.5 tidak melakukan cache pada 80% permintaannya: masing-masing memiliki prompt sekitar 4.100 token atau kurang, dan panjang prompt minimum yang dapat di-cache adalah 4.096 token (512 untuk Claude Haiku 5.5). Dari Claude Haiku 4.5 ke Claude Haiku 5.5, harga token turun hingga 90%, dan biaya token dari 79 tugas turun sekitar 75%. Biaya token turun lebih sedikit daripada harga karena sekitar 5% permintaan Claude Haiku 5.5 memiliki prompt lebih dari 100.000 token, yang membayar harga lebih tinggi ([Harga konteks panjang](https://platform.claude.com/docs/id/about-claude/pricing#long-context-pricing)), dan permintaan tersebut menanggung 73% biayanya.
    * **Thinking:** Anthropic menetapkan effort Claude Haiku 5.5 ke `medium` dan tidak mengirimkan pengaturan thinking atau batas output untuk kedua model, sehingga thinking diserahkan pada pengaturan Claude Managed Agents sendiri untuk setiap model. Claude Haiku 5.5 menggunakan thinking pada 59% permintaan, dan Claude Haiku 4.5 pada 22%. Perbandingan ini adalah perbandingan setiap model sebagaimana disajikan, bukan pada pengaturan yang setara.
    * **Biaya tanpa caching, dihargai dari jumlah token yang tercatat:** Anthropic juga menghitung ulang harga jumlah token yang tercatat dari eksekusi 7 Oktober Claude Haiku 5.5 untuk faktor caching di [Mengapa caching didahulukan](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#why-caching-comes-first); Anthropic tidak melakukan eksekusi dengan caching nonaktif, dan Claude Managed Agents menerapkan caching prompt sendiri, sehingga faktor tersebut membandingkan dua harga untuk permintaan yang sama, bukan dua pengaturan.
    * **Faktor:** Faktor tersebut, 1,7, adalah biaya token eksekusi dengan setiap token input pada harga input, token output tidak berubah, dibagi dengan biaya tokennya dengan setiap sesi dihargai secara terpisah: prompt sebelumnya dari setiap permintaan sebagai cache read dan token barunya sebagai cache write 5 menit. Setiap permintaan dihargai sesuai panjang prompt-nya sendiri dalam kedua biaya, sehingga 87 permintaan di atas 100.000 token membayar harga lebih tinggi pada keduanya. Pada jumlah token sebagaimana tercatat, yang digunakan oleh biaya panduan ini untuk eksekusi tersebut, faktornya adalah 1,9, karena lima percobaan suatu tugas berjalan berdampingan dan membaca entri cache satu sama lain.
    * **Mengapa faktornya rendah:** Faktornya rendah karena sesinya pendek, median 4 permintaan: sebagian besar token input tiba sebagai hasil alat pada permintaan kedua atau ketiga dan dibaca dari cache hanya sekali atau dua kali. Delapan tugas konteks panjang menanggung tiga perempat biaya. Eksekusi kedua, pada 8 Oktober, juga menghasilkan 1,7.

26. **Pengukuran format jawaban:**

    * **Apa yang diukur:** Pekerjaan triase 20 issue dari [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens), dijalankan pada Claude Sonnet 5 dengan caching prompt aktif dan tanpa pengaturan thinking dalam permintaan, sehingga thinking dibiarkan pada default model, di bawah tiga instruksi jawaban akhir, tiga eksekusi per instruksi.
    * **Instruksi dua baris:** Versi asli meminta dua baris: `4. Finish with exactly two lines: LABEL: <one of: bug-confirmed, needs-more-info, duplicate-candidate, feature-request, upstream-issue, perf, ui-polish> SUMMARY: <one or two sentences for the engineering team>`
    * **Instruksi satu baris:** Varian yang lebih pendek meminta satu baris: `4. Finish with exactly one line in this form: DECISION | LABEL | REASON where DECISION is one of: triage-now, needs-info, close-duplicate; LABEL is one of: bug-confirmed, needs-more-info, duplicate-candidate, feature-request, upstream-issue, perf, ui-polish; REASON is one clause under 15 words. Output nothing after that line.`
    * **Instruksi memo:** Varian yang lebih panjang meminta memo dengan enam bagian berjudul: ringkasan masalah, bukti, pemeriksaan duplikat, label yang direkomendasikan, langkah selanjutnya, dan tingkat keyakinan.
    * **Juga dalam instruksi sebagaimana dikirim:** Sebagaimana dikirim, instruksi dua baris juga menyatakan "Be concise." dan instruksi memo "Be thorough and explicit."
    * **Kapan:** Instruksi dua baris dan satu baris dijalankan pada 18 Agustus 2026, dengan `max_tokens` pada 700, dan instruksi memo pada 19 Agustus 2026, dengan `max_tokens` pada 3.000. Tidak ada respons yang mencapai batasnya.
    * **Cara penilaian dan penetapan harga:** Angka-angka adalah rata-rata dari tiga eksekusi pada harga daftar Claude Sonnet 5, dan akurasi adalah exact match terhadap gold label.
    * **Hasil:** Jawaban satu baris menggunakan 39% lebih sedikit token output daripada versi asli dua baris dan berbiaya 14% lebih rendah per eksekusi (dari biaya yang dibulatkan pada grafik, $0,49 USD dan $0,57 USD; rata-rata yang tidak dibulatkan menghasilkan 13%). Memo menggunakan enam kali token output versi asli dua baris dan berbiaya 2,8 kali jawaban satu baris.
    * **Thinking:** Sekitar setengah dari respons menyertakan thinking, dan tokennya dihitung dalam token output.

27. **Pengukuran tool search:**

    * **Apa yang diukur:** Pekerjaan triase 20 issue dari [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens), dijalankan pada Claude Sonnet 5 pada 19 Agustus 2026, dengan caching prompt aktif dan tanpa pengaturan thinking dalam permintaan, sehingga thinking dibiarkan pada default model, tiga eksekusi per konfigurasi. Agen memiliki dua alatnya sendiri ditambah definisi alat nyata dari server MCP publik, dengan total 7, 17, 52, 102, 252, atau 502 alat, dengan setiap definisi dimuat atau dengan definisi tambahan ditandai `defer_loading` di balik tool search.
    * **Cara penilaian dan penetapan harga:** Angka-angka adalah rata-rata dari tiga eksekusi pada harga daftar Claude Sonnet 5, dan akurasi adalah exact match terhadap gold label.
    * **Hasil:** Dengan setiap definisi dimuat, biaya eksekusi naik dari $0,55 USD pada 7 alat menjadi $1,02 USD pada 502 alat, hampir dua kali lipat. Dengan tool search, biayanya $0,55 USD hingga $0,56 USD pada setiap ukuran katalog, 45% lebih rendah pada 502 alat (dari biaya yang dibulatkan pada grafik, $0,56 USD dan $1,02 USD; rata-rata yang tidak dibulatkan menghasilkan 45,6%). Setiap eksekusi menjawab 15 hingga 18 dari 20 issue dengan benar, dengan atau tanpa tool search.
    * **Catatan:** Tidak ada eksekusi yang memanggil alat dari katalog atau alat tool search: dua alat milik agen sendiri selalu dimuat, dan setiap panggilan alat ditujukan ke salah satunya. Pengukuran ini menunjukkan biaya membawa definisi yang tidak digunakan, bukan apakah tool search menemukan alat ketika dibutuhkan.
    * **Pengukuran terpisah:** Dalam pengukuran terpisah pada model dan tanggal yang sama, dengan server MCP GitHub publik yang dilampirkan melalui konektor MCP dan tanpa katalog, tiga eksekusi dengan toolset server ditangguhkan berbiaya 20% lebih rendah daripada tiga eksekusi tanpanya ($0,56 USD dan $0,70 USD per eksekusi), dan tiga eksekusi dari setiap lengan menjawab 17, 16, dan 16 issue dengan benar. Permintaan dalam pengukuran terpisah ini tidak menyertakan alat tool search. Dengan toolset dimuat, setiap eksekusi memanggil salah satu alat server, `issue_read`, 3 atau 4 kali; dengan toolset ditangguhkan, tidak ada eksekusi yang memanggil alat server mana pun.

28. **Pengukuran pemangkasan input dan siklus hidup konteks:**

    * **Apa yang diukur:** Pekerjaan triase 20 issue dari [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens) dan varian panjangnya, dijalankan pada Claude Sonnet 5 pada 19 Agustus 2026 (bertanggal dalam UTC), tiga eksekusi per pengaturan, tanpa pengaturan thinking dalam permintaan, sehingga thinking dibiarkan pada default model; sekitar 3 dari 10 respons menyertakan thinking.
    * **Grafik:** Grafik di [Kelola siklus hidup konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#manage-the-context-lifecycle) membandingkan empat pengaturan pada setiap pekerjaan: pekerjaan dengan caching prompt dan pemangkasan input (pengubahan ukuran gambar dan tool search) aktif, dan yang sama dengan satu tuas ditambahkan, yaitu context editing, compaction, atau prune. Grafik menghitung perubahan di bawah 10% sebagai tidak ada perubahan.
    * **Pengaturan tuas:** Pengaturan tuas berbeda antara kedua pekerjaan: context editing membersihkan setidaknya 2.000 token setelah prompt melewati 20.000 pada pekerjaan 20 issue, dan setidaknya 40.000 setelah melewati 50.000 pada pekerjaan panjang, dengan mempertahankan tiga penggunaan alat terbaru, dan compaction terpicu pada 50.000 token input pada pekerjaan 20 issue dan 80.000 pada pekerjaan panjang.
    * **Cara penetapan harga:** Setiap biaya adalah rata-rata dari tiga eksekusi, dari field penggunaan respons pada harga daftar Claude Sonnet 5, dengan cache write pada $2,50 USD dan cache read pada $0,20 USD per juta token.
    * **Hasil, pemangkasan input:** Pengaturan kelima, caching prompt tanpa pemangkasan input, berbiaya $0,57 USD per eksekusi pada pekerjaan 20 issue dan $1,38 USD pada pekerjaan panjang, sehingga pemangkasan input memangkas 26% dari yang pertama dan 21% dari yang kedua. Dibandingkan dengan pekerjaan 20 issue yang sama dengan caching nonaktif, yang berbiaya $3,36 USD per eksekusi (referensi 16), caching prompt dan pemangkasan input bersama-sama menghemat 88% (rata-rata yang tidak dibulatkan menghasilkan 87,5%).
    * **Hasil, eksekusi 20 issue:** Pada eksekusi 20 issue, di mana pekerjaan tanpa tuas berbiaya $0,42 USD per eksekusi, context editing berbiaya 73% lebih tinggi, compaction berjalan sekali menjelang akhir setiap eksekusi dan berbiaya 7% lebih rendah, dan prune tidak menulis ulang apa pun, karena tidak ada hasil pencarian yang melebihi ambang 2.000 karakternya.
    * **Hasil, eksekusi panjang:** Pada eksekusi panjang, di mana pekerjaan tanpa tuas berbiaya $1,09 USD per eksekusi, prune berbiaya 39% lebih rendah, compaction 32% lebih rendah, dan context editing 4% lebih tinggi.
    * **Cache read, eksekusi panjang:** Dalam eksekusi panjang dengan prune, 89% token prompt dibaca dari cache pada permintaan pertama setelah batas tugas dan 81% pada permintaan lainnya. Di seluruh eksekusi panjang, 85% token prompt dibaca dari cache dengan prune dan 85% dengan context editing, berbanding 95% tanpa tuas.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Caching prompt" icon="database" href="https://platform.claude.com/docs/id/build-with-claude/prompt-caching">
    Keuntungan gratis terbesar di halaman ini: penyiapan, masa hidup, dan diagnostik.
  </Card>

  <Card title="Effort" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Tukar kecerdasan dengan latensi dan biaya dalam satu model.
  </Card>

  <Card title="Memilih model yang tepat" icon="settings" href="https://platform.claude.com/docs/id/about-claude/models/choosing-a-model">
    Evaluasi kemampuan, kecepatan, dan biaya di seluruh keluarga model Claude.
  </Card>

  <Card title="Session budget" icon="coins" href="https://platform.claude.com/docs/id/managed-agents/budgets">
    Tetapkan batas dolar yang tegas pada sesi Managed Agents.
  </Card>

  <Card title="Harga" icon="dollar-sign" href="https://platform.claude.com/docs/id/about-claude/pricing">
    Lihat harga per token saat ini untuk setiap model Claude.
  </Card>

  <Card title="Cookbook: optimasi biaya pada Claude API" icon="book" href="https://platform.claude.com/cookbook/cost-optimization-cost-optimization">
    Terapkan tuas-tuas ini satu per satu pada agen yang berfungsi dalam notebook yang dapat dijalankan, dengan biaya per tugas setelah setiap langkah.
  </Card>

  <Card title="Webinar: Membangun di Claude Platform" icon="play" href="https://www.anthropic.com/webinars/building-on-the-claude-platform-claude-fable-5-and-model-orchestration-patterns">
    Tonton panduan langkah demi langkah tentang pola advisor dan orchestrator.
  </Card>
</CardGroup>
