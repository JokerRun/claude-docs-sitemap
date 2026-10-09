---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence
fetched_at: 2026-10-09T02:29:51.005508Z
sha256: 54e1af2010f5653a6d12ee268e55b25be04c6a78d1d949703406b46192051566
---

---
title: Mengoptimalkan biaya dan kecerdasan
url: https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence
description: Seimbangkan biaya dan kecerdasan di Claude Platform, dengan hasil terukur untuk caching prompt, effort, pilihan model, anggaran, dan strategi multi-model.
---

Ketika sebuah beban kerja berpindah dari prototipe ke produksi, biaya menjadi batasan desain yang utama. Model yang paling mumpuni bisa terlalu mahal dalam skala besar, dan model yang paling murah bisa kurang memadai dari segi kualitas. Mengelola biaya dengan baik berarti memahami bagaimana setiap tuas biaya memengaruhi kualitas output, karena sebagian tuas mengorbankan kualitas dan sebagian lainnya tidak. Claude Platform memberi Anda kendali langsung atas "tradeoff" (kompromi) tersebut. Anda memilih model, tingkat "effort" (upaya), dan arsitektur untuk setiap permintaan, sehingga Anda dapat menempatkan beban kerja hampir di mana saja pada "cost-to-intelligence frontier" (frontier biaya-terhadap-kecerdasan).

Biaya dan kecerdasan biasanya digambarkan sebagai sebuah frontier, tempat yang satu dibeli dengan mengorbankan yang lain. Kelompok tuas pertama di halaman ini menggerakkan beban kerja menuju frontier tersebut dengan memangkas biaya tanpa menyentuh kualitas; hanya kelompok kedua yang bergerak di sepanjang frontier itu:

<Frame>
  ![Skema "cost-to-intelligence frontier" (frontier biaya-terhadap-kecerdasan): satu panah memangkas pengeluaran pada kualitas yang sama, panah lainnya menukar kualitas dengan biaya](https://platform.claude.com/docs/images/cost-intel/frontier.svg)
</Frame>

Tuas-tuas ini terbagi menjadi dua jenis:

* **Keuntungan gratis** memangkas pengeluaran tanpa menyentuh kualitas: "prompt caching" (caching prompt), "token hygiene" (kebersihan token), audit prompt terhadap model yang Anda jalankan, ["batch processing" (pemrosesan batch)](https://platform.claude.com/docs/id/build-with-claude/batch-processing) dengan diskon 50% untuk pekerjaan yang dapat menunggu hingga 24 jam, dan [batas pengeluaran workspace](https://platform.claude.com/docs/id/api/rate-limits#setting-lower-limits-for-workspaces) sebagai pengaman terakhir.
* **Tradeoff** menukar biaya dengan kecerdasan: pilihan model, effort, batas output dan anggaran tugas, jam waktu yang telah berlalu, dan arsitektur multi-model.

Setiap tuas disertai hasil terukur dan aturan kapan tuas tersebut menguntungkan. Dalam pengukuran Anthropic, caching prompt adalah tuas terbesar dengan selisih yang jauh: caching prompt memangkas biaya loop agen dengan faktor 2,7 hingga 5,3 pada benchmark panduan ini dan memangkas tagihan sebuah agen triase kecil sebesar 83%, atau 88% jika ditambah pemangkasan input. Tuas multi-model lebih sempit; model kedua terbukti menguntungkan dalam dua bentuk, yaitu "advisor" (penasihat) dan "orchestrator" (orkestrator).

## Mulai di sini

Cocokkan situasi Anda dengan salah satu baris.

| Situasi Anda                                            | Lakukan ini                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Di mana                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Beban kerja apa pun, model apa pun                      | Aktifkan caching prompt dan pangkas token yang tidak diperlukan; keduanya gratis                                                                                                                                                                                                                                                                                                                                                                                                | [Cache konteks berulang](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#cache-repeated-context) · [Pangkas token](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens) |
| Seseorang menunggu di antara giliran                    | Gunakan durasi cache 1 jam begitu sekitar 1 dari 20 giliran terjadi setelah jeda antara 5 menit dan satu jam dan hanya sedikit jeda yang melebihi satu jam. Di Claude Fable 5.1, jaga cache 5 menit tetap hangat selama jeda berlangsung beberapa menit, dan beli durasi 1 jam ketika jeda mendekati satu jam. Di Claude Opus 5.5, jaga cache 5 menit tetap hangat sebagai gantinya ketika hanya satu atau dua dari 20 giliran terjadi setelah jeda hingga sekitar setengah jam | [Pilih durasi cache](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#pick-the-cache-duration)                                                                                                                                                  |
| Biaya terlalu tinggi; kualitas sudah baik               | Turunkan effort secara bertahap pada model Anda saat ini                                                                                                                                                                                                                                                                                                                                                                                                                        | [Setel effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort)                                                                                                                                                                    |
| Anda tidak menggunakan model terbaru                    | Lakukan upgrade; dalam pengukuran Anthropic, setiap model yang lebih baru menyelesaikan setidaknya sebanyak tugas yang diselesaikan model sebelumnya, biasanya dengan biaya lebih rendah per tugas yang diselesaikan                                                                                                                                                                                                                                                            | [Upgrade model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#upgrade-the-model)                                                                                                                                                             |
| Anda sedang memilih atau berganti model                 | Bandingkan berdasarkan biaya per tugas yang selesai, bukan per token                                                                                                                                                                                                                                                                                                                                                                                                            | [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task)                                                                                                                                            |
| Kualitas belum cukup baik                               | Jika Anda menurunkan effort, kembalikan; jika tidak, coba tingkat berikutnya di atasnya dengan effort `low`                                                                                                                                                                                                                                                                                                                                                                     | [Setel effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort) · [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task)                 |
| Percobaan berakhir dengan `stop_reason: max_tokens`     | Naikkan `max_tokens`; 64.000 mencakup semua kecuali 2 dari 14.000 giliran yang diukur pada effort default, dan 128.000 tidak menambah biaya per tugas yang diselesaikan                                                                                                                                                                                                                                                                                                         | [Tetapkan anggaran](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                                                                                                                                               |
| Anda dapat memeriksa output (tes, verifier)             | Jalankan semuanya dengan effort rendah dan jalankan ulang yang gagal dengan `high`; pada benchmark coding yang diukur, tingkat kelulusan bertahan dengan sekitar setengah biaya                                                                                                                                                                                                                                                                                                 | [Jalankan ulang kegagalan](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#re-run-failures-at-higher-effort)                                                                                                                                   |
| Loop agen dengan beberapa run yang sangat mahal         | Tetapkan anggaran tugas (beta; periksa tabel dukungan untuk model mana saja), anggaran sesi Claude Managed Agents, dan batas pengeluaran workspace                                                                                                                                                                                                                                                                                                                              | [Tetapkan anggaran](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                                                                                                                                               |
| Anda ingin run agen selesai lebih cepat                 | Beri tahu model bahwa waktu itu penting, dan tunjukkan waktu yang telah berlalu; pada tugas riset DRACO dengan Claude Opus 5.5, satu agen membutuhkan waktu 47% lebih sedikit dengan biaya 60% lebih rendah pada tugas tipikal, dengan skor 4,1 poin lebih rendah; pada HLE dan set fisika internal, tugas tipikal membutuhkan waktu paling banyak 14% lebih sedikit, dan skor set fisika 3,0 poin lebih rendah                                                                 | [Tunjukkan waktu yang telah berlalu kepada model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#show-the-model-elapsed-time)                                                                                                                 |
| Model yang lebih murah hanya macet pada keputusan sulit | Tambahkan advisor frontier. Ini menguntungkan ketika harganya jauh di atas executor dan benar-benar dikonsultasikan, jadi pertama-tama hitung harga model advisor saja dengan effort rendah dan ukur tingkat konsultasinya                                                                                                                                                                                                                                                      | [Strategi advisor](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#advisor-strategy-escalate-hard-decisions)                                                                                                                                   |
| Pekerjaan melebihi satu jendela konteks                 | Delegasikan partisi ke worker yang lebih murah                                                                                                                                                                                                                                                                                                                                                                                                                                  | [Strategi orchestrator](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#orchestrator-strategy-delegate-bulk-work)                                                                                                                              |

Hasil ini berasal dari pengukuran internal Anthropic ([Benchmark yang dirujuk](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)) dan bersifat indikatif, bukan jaminan, jadi ukurlah pada beban kerja Anda sendiri dengan [metode empat langkah](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#measure-on-your-own-workload).

## Pangkas pengeluaran tanpa kehilangan kualitas

Caching prompt, kebersihan token, pemrosesan batch, dan audit prompt terhadap model Anda saat ini semuanya menurunkan apa yang Anda bayar tanpa menurunkan kualitas output. Dua catatan berlaku: pemrosesan batch menukar latensi dengan diskonnya, dan context editing, sebuah tuas kebersihan token, berbiaya lebih besar daripada yang dihematnya pada run yang diukur di bagian ini.

### Cache konteks berulang

#### Mengapa caching didahulukan

Aktifkan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) sebelum tuas lain mana pun, karena setiap giliran tugas agentik mengirim ulang seluruh percakapan yang terus bertambah: "system prompt" (prompt sistem), definisi alat, dan setiap giliran sebelumnya. Tugas 40 giliran mengirim giliran pertamanya 40 kali, sehingga biaya tugas tumbuh kira-kira sebanding dengan kuadrat jumlah giliran. Caching tidak menghentikan pengiriman ulang, tetapi setiap pengiriman ulang berbiaya sekitar sepersepuluhnya dan diproses lebih cepat: prefiks ditagih pada [tarif cache-read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#pricing), sepersepuluh harga input, dan setiap giliran membayar tarif cache-write 1,25x hanya untuk apa yang baru.

**Seperti apa kondisi yang baik.** Selama satu hari penuh lalu lintas nyata, loop agen membaca median 84% input mereka dari cache, dan 10% harness teratas, baik coding maupun bukan, membaca 94% atau lebih[17](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs). Jauh di dalam sebuah tugas, loop yang dibangun dengan baik membayar harga penuh untuk kurang dari 1% inputnya. Di bawah sekitar 80%, carilah sesuatu yang merusak cache (lihat [Apa yang merusak cache](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#what-breaks-the-cache)).

Di seluruh run yang diukur Anthropic, cache read secara rutin menjadi komponen tunggal terbesar dari biaya tugas, sehingga caching lebih berharga daripada sebagian besar keputusan pemilihan model. Anthropic menghitung biaya run DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dengan dan tanpa caching:

<Frame>
  ![Grafik dumbbell, DeepResearch Bench II: dengan "caching" (caching prompt), Claude Fable 5.1 turun dari $37,94 USD menjadi $7,12 USD per tugas dan Claude Sonnet 5 dari $3,20 USD menjadi $1,20 USD](https://platform.claude.com/docs/images/cost-intel/caching.svg)
</Frame>

Masa hidup default cache adalah 5 menit dan giliran loop agen berjarak beberapa detik, sehingga diskon berlaku untuk sebagian besar token di setiap giliran. Run pada grafik caching membaca 79% hingga 90% token input mereka dari cache. Penghematannya bervariasi menurut kedalaman episode, karena loop yang lebih pendek membaca ulang lebih sedikit, tetapi caching tetap menjadi tuas tunggal terbesar pada setiap model dan benchmark yang diukur.

#### Pilih durasi cache

Jika loop Anda menunggu seseorang di antara giliran, gunakan [durasi cache 1 jam](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration). Biaya penulisannya lebih tinggi (2x harga input alih-alih 1,25x). Cache miss pada durasi mana pun menagih seluruh prefix dengan harga tulis alih-alih harga baca, sehingga durasi yang lebih panjang menguntungkan begitu beberapa giliran per sesi terjadi setelah jeda antara 5 menit dan satu jam.

Untuk memutuskan, hitung jeda antara permintaan berurutan dalam sebuah percakapan:

* Lebih dari sekitar 1 dari 20 jeda berada antara 5 menit dan satu jam, dan jeda lebih dari satu jam jarang terjadi: gunakan durasi 1 jam. Di Claude Opus 5.5, ketika hanya 1 atau 2 dari 20 jeda berada dalam rentang tersebut dan tidak ada yang berlangsung lebih dari sekitar setengah jam, jaga cache 5 menit tetap hangat sebagai gantinya, dengan permintaan keep-alive yang dijelaskan di bawah.
* Giliran datang dengan jarak beberapa detik: tetap gunakan default 5 menit. Ketika tidak ada jeda, biayanya 15% lebih rendah daripada pengaturan 1 jam di Claude Sonnet 5 dan sekitar 15% hingga 18% lebih rendah di Claude Opus 5.5.
* Jeda lebih dari satu jam sering terjadi: tetap gunakan default. Jeda lebih dari satu jam membuat kedua durasi kedaluwarsa, dan pengaturan 1 jam kemudian menulis ulang prefix dengan harga tulisnya yang lebih tinggi, sehingga rugi pada setiap jeda tersebut. Dari jeda Anda yang lebih lama dari 5 menit, jika sekitar 60% atau lebih juga melewati satu jam, tetap gunakan default; durasi 1 jam hanya menguntungkan ketika setidaknya sekitar 40% jeda panjang berakhir dalam satu jam.

Anthropic mengukur pekerjaan triase dari [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens) dengan jeda yang disisipkan sebelum beberapa giliran untuk menyimulasikan penundaan oleh seseorang[16](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs). Di Claude Sonnet 5 dan Claude Opus 5.5, cache 1 jam menjadi pengaturan yang lebih murah begitu sekitar 1 dari 30 giliran terjadi setelah jeda, sehingga aturan 1-dari-20 menyisakan margin, dan selisihnya melebar dengan cepat setelah titik persilangan karena setiap giliran setelah jeda pada pengaturan 5 menit menulis ulang seluruh prefix. Setiap model saat ini menggunakan pengali cache-write yang sama, dan setiap model kecuali Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, dan Claude Sonnet 5.5 menggunakan harga baca yang sama (Claude Sonnet 5.5 memiliki pengali yang sama dengan Claude Opus 5.5), sehingga titik persilangannya berada dalam rentang yang sama pada model-model lainnya; Fable 5.1 adalah kasus yang dibahas berikutnya. Akurasi tetap berada dalam noise antar-run di setiap sel. Giliran setelah jeda mempertahankan latensi cache hangatnya pada pengaturan 1 jam (diukur di Claude Sonnet 5 dan Claude Opus 5, bukan di Claude Opus 5.5). Grafik berikut memplot biaya per sesi terhadap proporsi giliran setelah jeda di Claude Sonnet 5:

<Frame>
  ![Grafik garis: biaya per sesi triase menurut proporsi giliran setelah jeda; "1-hour cache" (cache 1 jam) lebih murah setelah sekitar 1 dari 30 giliran](https://platform.claude.com/docs/images/cost-intel/cache-ttl.svg)
</Frame>

Anthropic juga mengukur permintaan tambahan yang menjaga cache 5 menit tetap hangat. Di Claude Sonnet 5, biayanya sekitar 8% lebih rendah daripada durasi 1 jam ketika 1 dari 20 giliran terjadi setelah jeda, tetapi kurang lebih sama pada 2 dari 20; di Claude Opus 5, model Opus sebelumnya, permintaan tersebut tidak menghemat apa pun yang terukur. Dengan jeda 6 menit atau lebih sebelum setiap giliran, biayanya lebih tinggi pada kedua model. Karena penghematan Claude Sonnet 5 sudah hilang pada 2 dari 20 giliran, gunakan durasi 1 jam sebagai gantinya di Claude Sonnet 5 dan Claude Opus 5.

Di Claude Fable 5.1, pengaturan termurahnya berbeda. [Cache read](https://platform.claude.com/docs/id/about-claude/pricing#prompt-caching)-nya berharga 0,025x harga input ($0,25 USD per juta token) sementara cache write-nya mempertahankan pengali standar, sehingga permintaan keep-alive yang membaca ulang prefix itu murah dan premi tulis durasi 1 jam menjadi tagihan yang lebih besar. Anthropic mengukur pekerjaan triase di Claude Fable 5.1 dengan tiga pengaturan yang sama[19](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs). Menjaga cache 5 menit tetap hangat memakan biaya 13% hingga 20% lebih rendah per sesi daripada cache 1 jam setiap kali jeda berlangsung beberapa menit; hanya dengan jeda mendekati 45 menit cache 1 jam unggul, sekitar $0,12 USD per sesi. Di Claude Fable 5.1, jaga cache 5 menit tetap hangat selama seseorang pergi beberapa menit, dan beli durasi 1 jam ketika jeda mendekati satu jam:

<Frame>
  ![Grafik biaya: "keep-alive" (menjaga cache tetap hangat) mengalahkan "1-hour cache" (cache 1 jam) di setiap titik pada Fable 5.1; pada Opus 5.5 dan Sonnet 5 hanya jika sedikit giliran yang berjeda](https://platform.claude.com/docs/images/cost-intel/cache-keepalive-opus-5-5.svg)
</Frame>

Di Claude Opus 5.5, yang cache read-nya berharga 0,05x harga input, permintaan keep-alive memakan biaya 8% hingga 13% lebih rendah daripada durasi 1 jam ketika 5% atau 10% giliran terjadi setelah jeda 6 hingga 32 menit (pada effort default, `medium`; 10% hingga 18% lebih rendah pada `high`), tetapi lebih tinggi dengan jeda sebelum setiap giliran: sekitar 4% hingga 6% lebih tinggi pada jeda 6 menit, naik hingga lebih dari 50% lebih tinggi pada jeda 45 menit. Jadi di Claude Opus 5.5, jaga cache 5 menit tetap hangat ketika hanya satu atau dua dari 20 giliran terjadi setelah jeda hingga sekitar setengah jam, dan selain itu ikuti daftar di awal bagian ini. Pengukuran ini mengirim permintaan keep-alive dengan `max_tokens: 1`. Untuk permintaan `max_tokens: 0` yang dijelaskan berikutnya, pengujian API pra-peluncuran Anthropic di Claude Opus 5.5 menunjukkan bahwa permintaan tersebut menulis cache dan permintaan berikutnya membacanya; apakah permintaan tersebut menyegarkan entri yang sudah ada tidak diukur di Opus 5.5.

Untuk menjaga cache tetap hangat, kirim ulang permintaan sebelumnya dengan `max_tokens` diatur ke 0 dalam 4 menit sejak awal permintaan sebelumnya, dan setiap 4 menit setelahnya, dengan menghapus `stream` jika sebelumnya diatur. Hitung dari awal permintaan, bukan dari akhir responsnya: [masa hidup 5 menit cache](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#how-prompt-caching-works) berjalan sejak awal permintaan yang menulis atau menyegarkan entri, sehingga waktu yang dihabiskan respons untuk menghasilkan output ikut terhitung. Itulah [permintaan pre-warming](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#pre-warming-the-cache): permintaan ini menyegarkan masa hidup cache, tidak menghasilkan apa pun, dan hanya menagih cache read. Jangan ubah satu byte pun dari prefix, dan jangan gunakan `max_tokens: 1`, yang mengambil sampel satu token tanpa alasan. Kirim ulang header permintaan serta body-nya: jika permintaan Anda membawa header `anthropic-beta` (misalnya untuk [anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets)), permintaan keep-alive memerlukan header yang sama, atau field yang dibatasi beta dalam body yang diputar ulang akan ditolak. Permintaan `max_tokens: 0` ditolak ketika permintaan mengatur `thinking.type: "enabled"` (adaptive thinking default di Claude Fable 5.1 tidak masalah), structured outputs, atau pilihan alat yang dipaksakan ([batasannya](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#limitations)); pada beban kerja tersebut, beli durasi 1 jam sebagai gantinya. Permintaan `max_tokens: 0` juga ditolak ketika membawa parameter `compaction` tingkat atas, jadi jangan kirim ulang permintaan compaction dari [compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand) sebagai permintaan keep-alive.

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

Penyiapannya butuh sedikit usaha. [Caching otomatis](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching) menempatkan breakpoint untuk Anda; jika tidak, [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill) yang disertakan dengan Claude Code dapat menambahkan caching ke integrasi yang ada dari satu prompt. Kutipan berikut menunjukkan skill tersebut menambahkannya ke harness yang menghasilkan pengukuran ini:

```text wrap
$ claude
> /claude-api add prompt caching to this integration

Done. Prompt caching is now wired into the harness. Two changes:

- build_system() now adds cache_control: {"type": "ephemeral"} to the
  system block. Since the API renders tools -> system -> messages, this
  one breakpoint caches the entire static prefix -- the full tool array
  plus the system prompt.
- apply_moving_cache_breakpoints() strips any stale markers, then marks
  the last content block of the two most recent user turns. The older
  marker is the read point matching the prefix the previous request
  cached; the newer one extends the cache for the next request.

That's 3 breakpoints total, under the limit of 4.
...
```

Penempatan breakpoint tersebut mengikuti pola standar dalam [Breakpoint cache eksplisit](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#explicit-cache-breakpoints).

#### Apa yang merusak cache

Beberapa hal dapat merusak cache Anda selama sebuah tugas. Apa pun yang berubah per permintaan, seperti timestamp atau posisi antrean, yang ditempatkan di depan prefix yang stabil akan mengubah setiap permintaan menjadi cache write penuh: pada run triase di [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens), baris status 25 token di bagian depan prompt sistem memakan biaya $4,24 USD per run alih-alih $0,59 USD, lebih mahal daripada menjalankan tanpa caching. Simpan teks per permintaan di giliran pengguna terbaru.

Cache adalah pencocokan prefix byte-exact atas permintaan secara berurutan (alat, lalu prompt sistem, lalu pesan), sehingga perubahan di mana pun membatalkan semua yang ada setelahnya. Mengubah [`effort`](https://platform.claude.com/docs/id/build-with-claude/effort) atau konfigurasi thinking di antara permintaan membatalkan cache dari titik tersebut dan seterusnya, dan pada beberapa model juga alat dan prompt sistem di depannya; setiap pengeditan prompt sistem membatalkan cache dari titik tersebut dan seterusnya; mengatur atau mengubah format output membatalkan cache untuk seluruh percakapan; menambahkan, menghapus, atau mengurutkan ulang definisi alat membatalkan semuanya. Halaman [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#what-invalidates-the-cache) mencantumkan kasus-kasus ini, kecuali format output, yang dibahas di [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#prompt-modification-and-token-costs). Pada model terbaru, ubah instruksi dengan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages), yaitu pesan `{"role": "system"}` yang ditambahkan ke `messages`, alih-alih mengedit field `system` tingkat atas: prefix yang di-cache tetap utuh. Periksa halaman tersebut untuk mengetahui model mana yang mendukungnya. Pada model yang mendukungnya, [perubahan effort per pesan](https://platform.claude.com/docs/id/build-with-claude/effort#change-effort-mid-conversation-beta) juga membiarkan prefix yang di-cache tetap utuh. Taruhannya paling tinggi di Claude Fable 5.1 dan Claude Mythos 5.1, di mana kerusakan cache menulis ulang prefix dengan 1,25x harga input alih-alih membacanya dengan 0,025x. Pada prefix 100.000 token, satu giliran yang rusak di sana memakan biaya $1,25 USD alih-alih $0,03 USD, 50 kali lipat harga baca; di Claude Opus 5.5 biayanya $0,50 USD alih-alih $0,02 USD, dan di Claude Sonnet 5.5 $0,25 USD alih-alih $0,01 USD, 25 kali lipat, dan di model saat ini lainnya 12,5 kali lipat.

Anthropic mengukur hal ini pada sesi panjang agen triase[18](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs). Perubahan effort dan penambahan alat yang dilakukan di tengah sesi menulis ulang 39.000 dan 60.000 token yang di-cache, dan sesi-sesi tersebut memakan biaya $0,95 USD per sesi. Dua perubahan yang sama pada permintaan pertama setelah compaction memakan biaya $0,75 USD, dan pada permintaan yang memicu compaction $0,92 USD, karena proses peringkasan compaction kemudian memproses ulang konteks 81.000 token dengan harga cache-write: proses peringkasan tersebut memakan biaya $0,21 USD, dibandingkan $0,04 USD ketika perubahan yang sama dilakukan satu permintaan kemudian, dengan akurasi dalam noise antar-run di setiap lengan:

<Frame>
  ![Grafik batang, biaya per sesi triase: $0,81 USD tanpa perubahan, $0,95 USD di tengah sesi, $0,92 USD saat "compaction" (pemadatan), $0,75 USD setelahnya](https://platform.claude.com/docs/images/cost-intel/compaction-timing.svg)
</Frame>

Mengubah [anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) di tengah jalan membatalkan prefix yang di-cache yang berisi nilai anggaran tersebut, jadi tetapkan sekali saja, pada permintaan pertama. Setiap proses [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing#context-editing-and-prompt-caching) membatalkan prefix dari titik yang dibersihkannya dan permintaan berikutnya membayar untuk meng-cache ulang semua yang ada setelahnya, jadi bersihkan dalam beberapa batch besar alih-alih banyak batch kecil. Di Claude Fable 5.1 dan Claude Mythos 5.1, masing-masing hal ini memakan biaya 50 kali harga baca per token, sehingga paling berpengaruh di sana. Lakukan setiap perubahan yang membatalkan cache pada jeda alami, lalu pastikan cache read tidak turun; jika turun, [diagnostik cache](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics) menunjukkan di mana prefix menyimpang.

### Pangkas token input dan konteks

Sebagian besar permintaan agen membawa token yang tidak pernah memengaruhi jawaban. Memangkasnya jarang mengorbankan kualitas output, meskipun tidak semua tuas di sini menghasilkan penghematan saat diukur. Ada dua tempat yang perlu diperiksa:

* **Pemangkasan input.** Ada beberapa tuas di sini:

  * ["Dynamic filtering"](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#dynamic-filtering) (pemfilteran dinamis) pada alat web fetch mencegah boilerplate dari halaman yang diambil masuk ke konteks.
  * [Pengubahan ukuran gambar](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size) menyesuaikan ukuran input vision.
  * ["Tool search" (pencarian alat) dengan deferred loading](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool) hanya memuat definisi alat saat diperlukan (diukur nanti di bagian ini).
  * ["Programmatic tool calling"](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) (pemanggilan alat terprogram) memungkinkan Claude menjalankan beberapa panggilan alat dari kode, sehingga hanya hasil yang sudah difilter yang masuk ke konteks. Dokumentasinya melaporkan 24% lebih sedikit token input pada tolok ukur pencarian agentik, dengan skor yang lebih tinggi.

  [Kelola konteks alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/manage-tool-context) membandingkan pencarian alat, pemanggilan alat terprogram, caching prompt, dan pengeditan konteks.

* **Siklus hidup konteks.** [Context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) membersihkan hasil alat yang sudah usang, dan [compaction otomatis](https://platform.claude.com/docs/id/build-with-claude/compaction-threshold) beserta ambang batasnya mencegah loop panjang membawa seluruh riwayatnya ke depan.

Tuas-tuas ini saling berinteraksi dengan cache dan satu sama lain. Jadi, nilailah berdasarkan efek bersihnya, dan gunakan [diagnostik cache](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics) untuk memastikan prefiks yang di-cache tetap bertahan setelah setiap perubahan. Anthropic mengukurnya pada agen triase isu yang memproses 20 laporan bug nyata beserta tangkapan layar dari repositori publik. Pengukuran juga dilakukan pada varian yang lebih panjang dari pekerjaan yang sama, dengan 2,6 kali jumlah token. Dengan caching aktif, pemangkasan input (pengubahan ukuran gambar dan tool search) memangkas tambahan 26% dari run pendek dan 21% dari run panjang.

#### Tunda definisi alat yang tidak digunakan

Setiap definisi alat yang dilampirkan ke permintaan menjadi input di setiap giliran, dan beberapa server MCP dapat menambahkan hingga ratusan definisi. Anthropic menjalankan agen triase dengan dua alatnya sendiri ditambah katalog definisi alat nyata dari server MCP publik, dengan total hingga 502 alat, memuat semuanya atau menandai alat tambahan dengan `defer_loading` di balik [tool search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool):

<Frame>
  ![Grafik garis: dengan semua alat dimuat, biaya run naik dari $0,55 USD menjadi $1,02 USD pada 502 alat; "tool search" (pencarian alat) menjaganya di $0,56 USD](https://platform.claude.com/docs/images/cost-intel/tool-search.svg)
</Frame>

Dengan setiap definisi dimuat, biaya run hampir berlipat dua seiring bertambahnya katalog, mengikuti token skema pada setiap permintaan. Dengan tool search, biayanya tetap datar di setiap ukuran katalog, 45% lebih rendah pada 502 alat. Akurasinya 15 hingga 18 dari 20 di setiap sel dengan cara mana pun, dan model tidak pernah memanggil alat yang salah, sehingga pada skala ini katalog memakan uang, bukan kebenaran. Hal yang sama berlaku untuk alat yang datang melalui [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector): dengan server MCP GitHub publik terpasang, menunda toolset-nya (`default_config: {defer_loading: true}`) memangkas run sebesar 20% dengan akurasi yang sama.

#### Jauhkan file data dari prompt

Ketika model harus melakukan komputasi atas sebuah tabel, unggah tabel tersebut dengan [Files API](https://platform.claude.com/docs/id/build-with-claude/files) dan biarkan model mengkuerinya dengan [code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) alih-alih menempelkannya. Anthropic mengajukan 25 pertanyaan agregat[15](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) (penjumlahan, hitungan terfilter, group-by, dan filter tanggal) atas CSV publik 1.862 baris, dengan jawaban yang dihitung oleh pandas:

<Frame>
  ![Grafik sebar: file diunggah dengan "code execution" (eksekusi kode), 25 dari 25 benar dengan $0,40 USD; ditempel ke prompt, 6 dari 25 dengan $5,01 USD](https://platform.claude.com/docs/images/cost-intel/data-files.svg)
</Frame>

Jika ditempel ke prompt, tabel tersebut berukuran sekitar 91.000 token input di setiap permintaan, dan Claude Sonnet 5 menjawab 6 dari 25 pertanyaan dengan benar. Jika diunggah, dengan code execution, model menjawab semua 25 pertanyaan, dan biaya run-nya sekitar seperdua belasnya. Claude Opus 5 menunjukkan pola yang sama.

#### Kelola siklus hidup konteks

Tuas konteks hanya menguntungkan pada sesi yang cukup panjang untuk membutuhkannya:

<Frame>
  ![Grafik batang menurut panjang run: "context editing" (pengeditan konteks) menambah 74% pada run pendek; "compaction" (pemadatan) menghemat 32% dan "pruning" (pemangkasan) 39% pada run panjang](https://platform.claude.com/docs/images/cost-intel/hygiene.svg)
</Frame>

Pada run 20 issue, tuas-tuas ini tidak menghemat apa pun, dan context editing memakan biaya 74% lebih tinggi. Pada run panjang, prune menghemat 39% dan compaction 32%, sementara context editing tidak mengubah apa pun. Prune adalah beberapa baris kode yang Anda tulis sendiri: di setiap batas tugas, ganti hasil alat besar yang sudah usang dengan ekstrak satu baris. Prune ter-cache dengan baik karena pengeditannya berada di ekor percakapan, tempat tugas berikutnya toh akan menambahkan konten baru: 89% cache read pada permintaan pertama setelah batas dan 81% pada permintaan di antara batas. Secara keseluruhan run, prune dan context editing ter-cache kurang lebih sama baiknya. Prune lebih murah karena context editing menulis ulang konten di tengah tugas yang dihapus oleh prune (sekitar dua pertiga dari selisihnya) dan karena prune menjaga konteks sekitar setengah ukurannya (sepertiga sisanya). Jika Anda menggunakan context editing, [bersihkan dalam beberapa batch besar](https://platform.claude.com/docs/id/build-with-claude/context-editing#context-editing-and-prompt-caching). Prune, diadaptasi dari harness:

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

[Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing) memotong 50% dari setiap token permintaan, termasuk yang ter-cache, dengan imbalan hasil tiba kapan saja dalam 24 jam. Arahkan setiap permintaan yang tidak ditunggu siapa pun melalui batch, dan pertahankan jalur interaktif untuk sisanya. Batching adalah tuas gratis terbesar kedua setelah caching untuk pekerjaan agen tanpa pengawasan: run evaluasi, backfill, dan pekerjaan terjadwal seperti run berulang agen triase isu dari [pengukuran pemangkasan token](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens). Ia dapat digabungkan dengan semua yang ada di halaman ini kecuali interaktivitas, tetapi tidak tersedia untuk sesi Claude Managed Agents, yang interaktif secara desain (lihat [harga Claude Managed Agents](https://platform.claude.com/docs/id/about-claude/pricing#claude-managed-agents-pricing)).

### Audit prompt terhadap model saat ini

Setiap generasi model merespons prompt secara berbeda, sehingga sebuah prompt mengakumulasi teks yang ditulis untuk model yang tidak lagi Anda gunakan. Kasus yang umum adalah instruksi yang terlalu spesifik yang ditambahkan untuk mengompensasi model lama: "verify twice," "be maximally thorough," prosedur langkah demi langkah yang wajib, atau scratchpad penalaran buatan sendiri. Model yang lebih baru mengikuti instruksi ini secara harfiah, menghasilkan putaran alat tambahan dan tulisan tambahan, sehingga tagihan naik tanpa peningkatan akurasi. Mengaudit prompt terhadap model yang Anda jalankan sekarang, dan lagi setiap kali Anda berganti model, adalah keuntungan gratis.

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

Efeknya terukur. Pada evaluasi support-desk[14](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), prompt yang ditulis untuk Claude Opus 4.8 memakan biaya 36% lebih tinggi per tiket di Claude Opus 5 tanpa perubahan akurasi. Menjalankan audit atas prompt yang sama membuat Opus 5 lebih murah daripada versi yang belum diaudit (sebesar 14%) sekaligus lebih akurat (97% tiket, naik dari 92%, peningkatan di luar noise). Pada migrasi Claude Sonnet 4.6 ke Claude Sonnet 5, audit memangkas 14% dengan akurasi yang sama:

<Frame>
  ![Grafik sebar, evaluasi support-desk: prompt lama lebih mahal pada model baru; setelah "audited" (diaudit), lebih murah dan sama akuratnya](https://platform.claude.com/docs/images/cost-intel/prompt-audit.svg)
</Frame>

Kedua jenis teks usang memiliki biaya yang berbeda. Instruksi yang diikuti model baru secara terlalu harfiah memakan uang: menghapus "verify twice" memangkas biaya per tiket Opus 5 sebesar sepertiga, dan menghapus "be maximally thorough" hampir sebesar itu. Teks yang tidak lagi cocok dengan model justru memakan akurasi: pengaturan thinking yang sudah dihentikan, aturan yang saling bertentangan, dan scratchpad buatan sendiri yang bertentangan dengan thinking model itu sendiri masing-masing memulihkan 7 hingga 11 poin di Opus 5 ketika dihapus:

<Frame>
  ![Grafik batang per pola lama: instruksi yang dipatuhi berlebihan memakan uang; pengaturan yang rusak dan aturan yang bertentangan memakan akurasi](https://platform.claude.com/docs/images/cost-intel/prompt-audit-patterns.svg)
</Frame>

Pola yang sama cenderung muncul dalam deskripsi alat dan skill, yang juga layak diaudit.

## Menukar biaya dengan kecerdasan

Tuas-tuas ini menentukan posisi satu model di antara biaya dan kecerdasan: pilihan model, effort, menjalankan ulang yang gagal dengan pengaturan lebih tinggi, anggaran dan batas yang menjadi ruang kerjanya, dan apakah model dapat melihat berapa banyak waktu yang telah berlalu. Mulailah dengan sapuan effort pada model Anda saat ini ([Setel effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort)). Dari biaya dan kemampuan terendah hingga tertinggi, model-model saat ini adalah Claude Haiku 5.5, Claude Sonnet 5.5, Claude Opus 5.5, dan Claude Fable 5.1 (model frontier); [Ikhtisar model](https://platform.claude.com/docs/id/models/overview) memuat jajaran lengkap dan harganya.

### Bandingkan model berdasarkan biaya per tugas

Daftar harga ditulis per token, dan jika dihitung per token, model frontier terlihat mahal: harga per token Claude Fable 5.1 beberapa kali lipat harga Claude Sonnet 5. Namun, yang Anda bayar adalah tugas yang selesai, jadi bandingkan model berdasarkan "cost per completed task" (biaya per tugas yang selesai). Model yang lebih mampu menyelesaikan tugas dengan lebih sedikit pekerjaan: lebih sedikit giliran, lebih sedikit pencarian, lebih sedikit membaca ulang konteksnya sendiri, dan lebih sedikit mundur untuk mengulang. Premi per token sering kali tertutupi oleh berkurangnya semua pekerjaan tersebut.

Anthropic mengukur hal ini pada subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), dengan harga sesuai tagihan pelanggan:

<Frame>
  ![Diagram sebar, SWE-bench Pro: Claude Opus 5.5 pada pengaturan default-nya menyamai default Claude Fable 5.1 dengan sekitar seperlima biayanya](https://platform.claude.com/docs/images/cost-intel/cost-per-task-opus-5-5.svg)
</Frame>

Claude Fable 5.1 pada effort `low` menyelesaikan 88,6% tugas dengan $0,54 USD per tugas yang terselesaikan, dibandingkan 77,4% dengan $0,84 USD dari Claude Sonnet 5 pada pengaturan default-nya: 11 poin lebih tinggi dengan biaya 35% lebih rendah per tugas yang terselesaikan, meskipun harga per tokennya lima kali lebih tinggi. Namun, model ini tidak selalu unggul. Pada subset yang sama, yang sebagian besar sudah jenuh bagi Claude Opus 5.5 maupun Claude Fable 5.1 dan skornya tidak dapat dibandingkan dengan leaderboard publik, Opus 5.5 pada default-nya, `medium`, menyamai Fable 5.1 pada default-nya (92,8% berbanding 92,3%, masih dalam noise antar-run) dengan sekitar seperlima biaya per tugas yang terselesaikan ($0,22 USD berbanding $1,19 USD). Pada `low`, Opus 5.5 menyelesaikan 87,4% dengan $0,12 USD. Angka-angka ini menggunakan 478 soal yang dijelaskan dalam referensi 3. Dan pada loop riset yang panjang, model frontier justru melakukan lebih banyak pekerjaan, bukan lebih sedikit: pada DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), Fable 5.1 pada `low` mendapat skor 10 poin di atas Sonnet 5 (66% berbanding 56%) dengan biaya per tugas sekitar empat kali lipat ($4,66 USD berbanding $1,20 USD), karena model ini menjalankan loop riset yang lebih panjang atas konteks yang lebih besar. Claude Opus 5 pada default-nya mendapat skor 71% dengan dasar yang sama seharga $6,71 USD per tugas, di atas Fable 5.1 pada default-nya (65% seharga $7,12 USD), sehingga pada riset pun Fable 5.1 hanya sepadan dengan harganya pada `low`.

Untuk sebagian besar beban kerja agen, mulailah dengan Claude Opus 5.5 pada effort default-nya (`medium`), dan gunakan Claude Fable 5.1 untuk penalaran yang menuntut dan pekerjaan agentik jangka panjang, atau ketika eval Anda pada Claude Opus 5.5 dengan effort lebih tinggi masih belum memadai. Pada subset SWE-bench Pro, Opus 5.5 pada default-nya menyamai Fable 5.1 pada default-nya dengan sekitar seperlima biaya per tugas yang terselesaikan, seperti disebutkan sebelumnya. Pada benchmark coding di [Strategi advisor](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#advisor-strategy-escalate-hard-decisions), model ini mendapat skor 86,6% berbanding 84,2% untuk Fable 5.1 pada `medium` (satu kali run Fable 5.1), dengan kurang dari sepertiga biaya per percobaan ($0,84 USD berbanding $2,68 USD). Pada Chartography[13](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), sebuah benchmark membaca grafik, Opus 5.5 pada `low` mendapat skor 68,7 dengan sekitar $0,03 USD per grafik, berbanding 62,5 seharga $0,15 USD dari Fable 5.1 pada `low` dan 49 seharga $0,16 USD dari Claude Opus 5 pada `low`. Di ujung lainnya, Claude Haiku 5.5 menjawab soal GPQA Diamond[9](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dengan sekitar seperdua puluh biaya per soal Claude Opus 5.5, dengan akurasi 85% dibandingkan 91% untuk Opus 5.5 yang dijalankan dengan cara yang sama. Model ini cocok untuk pekerjaan bervolume tinggi dan sensitif terhadap "latency" (latensi) dengan output yang dapat diperiksa.

Peringkatnya berbalik tergantung beban kerja, dan tidak ada daftar harga yang memberi tahu Anda ke arah mana. Hitung harga setiap kandidat dalam biaya per tugas yang selesai pada lalu lintas Anda sendiri, termasuk Claude Opus 5.5 pada effort default-nya dan model frontier pada effort yang diturunkan.

Hitung harga ekor beban kerja Anda, bukan mediannya: bandingkan model pada sepersepuluh tugas tersulit Anda, bukan tugas yang biasa. Pada tugas biasa, setiap model terlihat serupa dan yang termurah terlihat terbaik, tetapi tagihan ditentukan oleh tugas-tugas yang gagal dikerjakan model yang lebih murah, karena tugas yang gagal tetap menagih token-tokennya, lalu percobaan ulangnya, lalu apa pun biaya kegagalan itu di hilir. Ekor juga merupakan tempat uang dihabiskan bahkan ketika tidak ada yang gagal. Pada run WideSearch[1](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dengan 20 soal, dua soal menanggung 43% dari pengeluaran:

<Frame>
  ![Diagram batang 20 soal WideSearch yang diurutkan berdasarkan biaya: dua teratas menanggung 43% pengeluaran dan separuh termurah 10%](https://platform.claude.com/docs/images/cost-intel/tail.svg)
</Frame>

[Strategi multi-model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#combine-models) ada untuk menghabiskan kecerdasan frontier pada ekor tersebut tanpa membayar tarif frontier untuk sisanya.

### Upgrade model

Jika Anda tertinggal satu atau dua model, tuas termurah adalah string model. Anthropic menjalankan model Claude Opus, Claude Sonnet, dan Claude Fable terbaru melalui harness yang sama pada subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), masing-masing dengan pengaturan default bawaannya dan dihargai dengan tarif daftar, lalu menjalankan lini Opus lagi pada Terminal-Bench 3[20](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs):

<Frame>
  ![Dua diagram biaya per tugas yang terselesaikan terhadap tugas yang terselesaikan: pada SWE-bench Pro setiap model menyelesaikan sebagian besar tugas dan langkah peningkatannya kecil; pada Terminal-Bench 3 tangga Opus turun dari $183 USD ke $63 USD ke $28 USD per tugas yang terselesaikan](https://platform.claude.com/docs/images/cost-intel/upgrade-ladder.svg)
</Frame>

Anthropic menetapkan harga per token yang identik untuk Claude Opus 4.7, Opus 4.8, dan Opus 5, sehingga setiap perbedaan di antara mereka berasal dari seberapa banyak pekerjaan yang dilakukan setiap model per tugas: dengan harga sesuai tagihan pelanggan, Claude Opus 4.8 menyelesaikan porsi tugas yang sama dengan Claude Opus 4.7 dengan biaya 14% lebih rendah per tugas yang terselesaikan, lalu Claude Opus 5 menyelesaikan 12 poin tugas lebih banyak dengan biaya 21% lebih tinggi per tugas yang terselesaikan. Claude Opus 5 pada effort `low` mengalahkan default Opus 4.8 pada benchmark ini dengan sekitar 30% dari biaya per tugas yang terselesaikan, sehingga peningkatan termurah adalah model baru pada pengaturan yang lebih rendah. Penghematan Sonnet 5 berasal dari harga per tokennya yang lebih rendah, yang lebih dari mengimbangi token tambahan yang digunakannya per tugas dibandingkan Sonnet 4.6: 15% lebih rendah per tugas yang terselesaikan untuk 5 poin lebih tinggi. Tingkat frontier memperoleh keuntungan dengan cara yang sama: Claude Fable 5.1 menyamai skor Claude Fable 5 dengan biaya 43% lebih rendah per tugas yang terselesaikan, sebagian besar berkat harga cache-read yang lebih rendah. Arah tersebut tidak dijamin: pada DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) peningkatan yang sama berbiaya 41% lebih tinggi per tugas pada `high` (79% lebih tinggi pada `low`) untuk tambahan 2 hingga 3 poin pada tugas-tugas yang bersih di setiap lengan (referensi 7), karena model baru melakukan lebih banyak pekerjaan per tugas di sana. Harga input dan output sama dan cache read 4x lebih murah, jadi ukur peningkatan tersebut pada beban kerja Anda sendiri sebelum berasumsi bahwa itu menghemat.

Pada pekerjaan yang lebih sulit, kesenjangannya melebar. Pada Terminal-Bench 3[20](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), di mana tugas-tugasnya cukup sulit sehingga tingkat kelulusan, bukan token, yang menentukan tagihan, Claude Opus 4.7, Opus 4.8, dan Opus 5 masing-masing menghabiskan $8 USD hingga $15 USD per tugas tetapi menyelesaikan 7%, 15%, dan 41% tugas, sehingga biaya per tugas yang terselesaikan turun dari $183 USD ke $63 USD ke $28 USD seiring naiknya tangga. Premi 21% yang dimiliki Claude Opus 5 dibandingkan Opus 4.8 pada subset coding yang jenuh berubah menjadi penghematan 56% pada Terminal-Bench 3, di mana model lama sebagian besar gagal: semakin beban kerja Anda mengalahkan model lama, semakin banyak peningkatan tersebut menghemat per hasil.

Bandingkan berdasarkan biaya per tugas yang terselesaikan, bukan per token: teks yang sama membutuhkan sekitar 30% lebih banyak token pada Claude Opus 4.7 dan yang lebih baru, sehingga perbandingan per token secara konstruksi membuat model yang lebih baru terlihat lebih mahal.

### Setel effort

Effort adalah cara paling langsung untuk menyetel model sesuai tugas Anda. Parameter `effort` mengatur seberapa banyak pemikiran, pemanggilan alat, dan verifikasi diri yang dilakukan model, dan `high`, default pada sebagian besar model, cocok untuk tugas yang menuntut; Claude Opus 5.5 dan Claude Haiku 5.5 memiliki default `medium`. Biaya meningkat seiring semua aktivitas tersebut; akurasi hanya meningkat seiring bagian yang dibutuhkan tugas Anda. Di bawah batas kemampuan model, tingkat effort tertinggi membayar kedalaman yang tidak pernah digunakan tugas tersebut.

Pada benchmark riset dan pekerjaan pengetahuan (WideSearch[1](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), DeepWideSearch[6](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), BrowseComp[4](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), dan GDPval[2](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), semuanya dengan Claude Fable 5), kurva akurasi terhadap biaya hampir datar: `low` mengorbankan 1 hingga 3 poin untuk pengurangan sepertiga hingga setengah biaya per tugas, `medium` menyamai akurasi default dengan sekitar 70% hingga 87% biayanya, dan default tidak memberikan keuntungan terukur apa pun dibandingkan `medium` pada keempatnya. Pada DeepWideSearch, `low` juga menyamai orchestrator dengan worker Claude Sonnet 5 dengan biaya 29% lebih rendah: menurunkan effort mengalahkan perubahan arsitektur.

Pengaturan effort yang lebih rendah sering kali lebih cepat, yang penting ketika latensi menjadi kendala. Dalam run ini, `low` membutuhkan 4,5 menit per soal pada DeepWideSearch, dibandingkan 7,9 menit pada default. Pada [benchmark korpus](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#orchestrator-strategy-delegate-bulk-work), yang inputnya tidak muat dalam satu "context window" (jendela konteks) mana pun, Fable 5.1 membutuhkan 15,2, 17,5, dan 19,9 jam per episode pada `low`, `medium`, dan `high`.

Coding jangka panjang adalah tempat effort benar-benar meningkatkan akurasi. Pada SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), diukur terhadap `high`, Claude Opus 5.5 mendapat skor sekitar 2,5 poin lebih rendah pada default-nya, `medium`, dengan sekitar 70% biayanya, dan sekitar 8 poin lebih rendah pada `low` dengan sekitar sepertiga biayanya; `xhigh` mendapat skor sekitar 1,4 poin lebih tinggi dengan 2,5 kali biaya `high`: sebuah tradeoff nyata, yang diubah kembali menjadi penghematan oleh [menjalankan ulang kegagalan pada effort lebih tinggi](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#re-run-failures-at-higher-effort). Diagram ini memplot akurasi terhadap biaya untuk benchmark riset dan pekerjaan pengetahuan serta untuk SWE-bench Pro:

<Frame>
  ![Diagram garis akurasi terhadap biaya berdasarkan effort: hampir datar untuk Fable 5 pada pekerjaan riset, curam untuk Opus 5.5 pada SWE-bench Pro](https://platform.claude.com/docs/images/cost-intel/effort-sweep-opus-5-5.svg)
</Frame>

Ada dua konsekuensi. Pertama, gambarlah kurva ini untuk beban kerja Anda sendiri sebelum menambahkan model kedua: dalam pengukuran internal ini, konfigurasi multi-model yang tampak lebih murah daripada model tunggal default ternyata berbiaya lebih tinggi daripada model yang sama pada effort lebih rendah. Kedua, kurva ini adalah baseline model tunggal yang harus dikalahkan oleh strategi multi-model mana pun, sehingga [langkah 2 dari pengukuran pada beban kerja Anda sendiri](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#measure-on-your-own-workload) membuat baseline di berbagai tingkat effort.

Pekerjaan sulit tidak otomatis membutuhkan effort tinggi. Pada DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), Claude Fable 5.1 mendapat skor hampir sama pada `low`, `medium`, dan `high` sementara biaya per tugas naik dari $4,66 USD ke $7,12 USD, sehingga menaikkan effort dalam kasus ini tidak meningkatkan kualitas output secara nyata; pada 21 tugas yang bersih di setiap lengan (referensi 7), Claude Fable 5 juga datar di seluruh tingkat effort, meskipun dasar 33 tugas pada diagram, yang membuang percobaan yang terpotong dari masing-masing model, menunjukkannya naik. Ukur kurva pada model yang Anda rilis, bukan model yang terakhir Anda ukur:

<Frame>
  ![Diagram garis skor rubrik terhadap biaya per tugas pada DeepResearch Bench II: pada Claude Fable 5.1 effort yang lebih tinggi tidak menambah skor, hanya biaya](https://platform.claude.com/docs/images/cost-intel/effort-limit.svg)
</Frame>

Deskripsi tugas saja tidak mengungkapkan jenis beban kerja yang Anda miliki, jadi uji dua atau tiga tingkat effort pada sampel lalu lintas Anda sendiri dan baca jawabannya dari kurva. Uji setiap tingkat dalam sesi terpisah: mengubah effort tingkat atas di tengah sesi membatalkan cache (lihat [Cache konteks berulang](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#cache-repeated-context)) dan mendistorsi perbandingan. Untuk detail parameter, lihat [Effort](https://platform.claude.com/docs/id/build-with-claude/effort).

### Jalankan ulang kegagalan pada effort yang lebih tinggi

Ketika hasil suatu tugas dapat diperiksa, kebijakan termurah pada kurva effort bukanlah pengaturan tetap: jalankan setiap tugas pada pengaturan rendah dan jalankan ulang hanya kegagalannya pada pengaturan yang lebih tinggi.

Anthropic menghitung kebijakan ini tugas demi tugas dari run effort pada subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) di [Setel effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort). Dengan Claude Opus 5.5 pada `low`, 13% tugas gagal; dengan tugas-tugas tersebut dijalankan ulang pada `high`, sekitar 97% lulus dengan sekitar $0,17 USD masing-masing, berbanding 95,3% seharga $0,29 USD jika semuanya dijalankan pada `high`: tingkat kelulusan sedikit lebih tinggi dengan sedikit di atas setengah biayanya, termasuk percobaan murah yang gagal. Memulai pada `medium` justru menyelesaikan sekitar 97% dengan sekitar $0,24 USD. Sebagian besar kenaikan kecil itu berasal dari percobaan kedua (menjalankan ulang kegagalan dari satu run `high` pada `high` menghasilkan skor yang kurang lebih sama, dengan biaya lebih besar), jadi gunakan kebijakan ini untuk penghematannya, bukan kenaikannya:

<Frame>
  ![Diagram, SWE-bench Pro, Opus 5.5: effort low atau medium dengan kegagalan dijalankan ulang pada high menyamai effort tetap mana pun dengan biaya lebih rendah daripada high](https://platform.claude.com/docs/images/cost-intel/escalation-opus-5-5.svg)
</Frame>

Ada dua syarat. Pertama, Anda memerlukan sinyal kegagalan (di sini, tes milik benchmark itu sendiri); pemeriksa yang meloloskan pekerjaan buruk akan membiarkan kegagalan tersebut lolos. Kedua, setiap kegagalan pada percobaan pertama memakan waktu nyata senilai dua run, sehingga penghematan dibayar dengan latensi pada kegagalan.

### Tetapkan anggaran dan batas output

Sebagian besar run tugas agentik murah, tetapi sebagian kecil menghabiskan berkali-kali lipat biaya median untuk pencarian, verifikasi ulang, dan pengujian berlebihan. "Task budget" ([anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets)) menargetkan ekor tersebut. Model melihat hitung mundur token secara langsung untuk seluruh tugas dan mengatur dirinya sendiri, memangkas pencarian bernilai rendah, melewati verifikasi yang berlebihan, dan menyelesaikan pekerjaan alih-alih berputar-putar.

Anthropic mengukur tingkat kelulusan dan biaya per tugas pada SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dengan Claude Fable 5.1 seiring anggaran diperketat:

<Frame>
  ![Diagram garis pada SWE-bench Pro: pass@1 turun beberapa poin seiring anggaran tugas diperketat sementara biaya per tugas turun 44% hingga 58%](https://platform.claude.com/docs/images/cost-intel/budget-pareto.svg)
</Frame>

Anggaran yang longgar memangkas biaya per tugas 44% dengan pengorbanan sekitar 3 poin tingkat kelulusan, di batas noise antar-run, dan anggaran terketat yang diizinkan memangkasnya 58% dengan pengorbanan 6 poin. Anggaran memberikan efisiensi di sini, dengan harga berupa tingkat kelulusan yang bertambah seiring anggaran diperketat.

Tiga kontrol melakukan tiga tugas berbeda. Anggaran tugas menghemat uang, karena model melihatnya. `max_tokens` adalah batas pengaman: menurunkannya memangkas biaya per percobaan tanpa menurunkan biaya per tugas yang terselesaikan. Pada Claude Managed Agents, anggaran sesi adalah penghenti dolar yang tegas di belakang keduanya. Tetapkan ketiganya: anggaran tugas, `max_tokens` yang tinggi, dan batas sesi untuk run yang tidak pernah Anda inginkan muncul di tagihan, dengan [batas pengeluaran workspace](https://platform.claude.com/docs/id/api/rate-limits#setting-lower-limits-for-workspaces) sebagai pengaman terakhir.

* **Anggaran tugas** berstatus beta (header beta `task-budgets-2026-03-13`) pada model-model terbaru; periksa [tabel dukungan](https://platform.claude.com/docs/id/build-with-claude/task-budgets#feature-support) untuk mengetahui model mana. Mulailah di dekat penggunaan token persentil ke-90 dari loop Anda, lalu perketat ([Memilih anggaran](https://platform.claude.com/docs/id/build-with-claude/task-budgets#choosing-a-budget) menunjukkan cara mengumpulkan distribusi tersebut). Anggaran di bawah batas minimum saat ini sebesar 20.000 token akan ditolak, dan anggaran yang sangat ketat dapat menghasilkan perilaku yang menyerupai penolakan. Tetapkan anggaran sekali, pada permintaan pertama, karena perubahan di tengah tugas [membatalkan cache](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#cache-repeated-context). Anggaran bersifat anjuran, mengarahkan model alih-alih menghentikannya, jadi verifikasi kepatuhannya pada beban kerja Anda.
* **`max_tokens`** membatasi satu respons, tanpa terlihat oleh model, sehingga menurunkannya tidak membuat model berhemat. Giliran yang membutuhkan ruang tersebut dibuang dan tetap ditagih. Pada benchmark tugas repositori internal[12](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), batas 16.384 token mengakhiri sekitar seperempat percobaan Claude Opus 5.5 dan 43% percobaan Claude Fable 5.1, masing-masing pada effort default-nya. Hanya 1 dari 66 percobaan Opus 5.5 yang terpotong dan 9 dari 117 percobaan Fable yang terpotong yang tetap lulus. Run yang terpotong menghabiskan lebih sedikit per percobaan tetapi menghasilkan penyelesaian yang secara proporsional lebih sedikit, sehingga biaya per tugas yang terselesaikan kurang lebih sama dengan pada 64.000 (pada Fable 5.1, $21 USD berbanding $22 USD; pada Opus 5.5, dalam selisih 1%). Pada 64.000, 2 dari sekitar 14.000 giliran Claude Fable 5.1 pada effort default-nya masih terpotong (tidak ada giliran Claude Opus 5.5 yang terpotong), dan Fable 5.1 menyelesaikan 58,5% tugas alih-alih 36,3% (pada potongan terpisah dari subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), yang dijelaskan dalam referensi 12, tidak ada perbedaan: 94 dari 100 pada kedua batas). Mencoba ulang percobaan yang terpotong jarang membantu: pada batas yang sama sebagian besar gagal lagi, dan pada batas yang lebih tinggi Anda juga membayar percobaan yang terbuang. Tetapkan `max_tokens` ke 64.000 untuk pekerjaan agentik, atau ke 128.000, nilai maksimum, ketika satu percobaan yang terpotong berbiaya mahal; pada 128.000 Fable 5.1 menyelesaikan 60,0% dengan biaya per tugas yang terselesaikan yang sama. [Lakukan streaming respons](https://platform.claude.com/docs/id/build-with-claude/streaming) sebesar itu, perlakukan [`stop_reason: max_tokens`](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons#max-tokens) sebagai kegagalan, dan hemat uang dengan effort dan anggaran tugas, yang dapat dilihat oleh model.
* **Anggaran sesi pada Claude Managed Agents** adalah penghenti yang tegas. [Anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets) adalah batas dolar pada satu sesi dengan tarif daftar untuk token, pencarian, dan waktu sesi. Saat mencapai batas, sesi dijeda dengan `stop_reason: budget_reached`; menaikkan anggaran akan melanjutkannya. Anggaran ini ditegakkan oleh platform, berfungsi pada model apa pun yang memiliki harga daftar, termasuk model yang belum mendukung anggaran tugas, dan dapat dikombinasikan dengan anggaran tugas yang bersifat anjuran. Deployment menerapkan field yang sama ke setiap run.

Mintalah jawaban yang lebih pendek. Token output berbiaya lima kali token input pada Claude Sonnet 5, dan dalam loop agen setiap token yang ditulis model kembali sebagai input pada setiap giliran berikutnya, sehingga Anda membayar jawaban yang panjang berulang kali. Anthropic menjalankan pekerjaan triase dengan tiga instruksi jawaban akhir, masing-masing tiga run, dengan model dan alat yang sama. Versi asli meminta dua baris:

```text wrap
4. Finish with exactly two lines:
LABEL: <one of: bug-confirmed, needs-more-info, duplicate-candidate, feature-request, upstream-issue, perf, ui-polish>
SUMMARY: <one or two sentences for the engineering team>
```

Varian yang lebih pendek meminta satu baris:

```text wrap
4. Finish with exactly one line in this form:
DECISION | LABEL | REASON
where DECISION is one of: triage-now, needs-info, close-duplicate; LABEL is one of: bug-confirmed, needs-more-info, duplicate-candidate, feature-request, upstream-issue, perf, ui-polish; REASON is one clause under 15 words. Output nothing after that line.
```

Varian yang lebih panjang meminta memo dengan lima bagian berjudul: ringkasan masalah, bukti, pemeriksaan duplikat, label yang direkomendasikan, dan langkah selanjutnya. Untuk satu issue, yaitu prompt dalam antrean yang tidak pernah terkirim setelah pertanyaan dilewati, dua jawaban pertama adalah:

```text wrap
LABEL: bug-confirmed
SUMMARY: When a user submits a new prompt instead of answering an agent's pending question, the question is cancelled/skipped but the new prompt remains stuck in "QUEUED" state indefinitely since it's waiting on a response to the now-cancelled question; the queued prompt should be processed immediately after cancellation.
```

```text wrap
triage-now | bug-confirmed | Clear repro steps show prompt queues indefinitely after cancelled question.
```

<Frame>
  ![Diagram batang: format satu baris $0,49 USD per run, format dua baris asli $0,57 USD, memo $1,40 USD, semuanya 78% hingga 85% benar](https://platform.claude.com/docs/images/cost-intel/output-format.svg)
</Frame>

Jawaban satu baris menggunakan 39% lebih sedikit token output daripada versi asli dua baris dan berbiaya 14% lebih rendah per run. Memo menggunakan enam kali token output dan berbiaya 2,8 kali jawaban satu baris. Ketiganya mendapat skor dalam rentang noise antar-run satu sama lain terhadap label acuan, sehingga format-format tersebut jauh lebih berbeda dalam hal yang Anda bayar daripada dalam hal yang mereka jawab dengan benar. Mintalah jawaban yang akan Anda baca, bukan jawaban yang terlihat menyeluruh.

Pada batas `max_tokens` yang lebih rendah, kedua model menghabiskan lebih sedikit per percobaan tetapi menyelesaikan tugas yang secara proporsional lebih sedikit, sehingga biaya per tugas yang terselesaikan hampir tidak berubah:

<Frame>
  ![Diagram batang, Opus 5.5 dan Fable 5.1: batas max\_tokens 16k berbiaya lebih rendah per percobaan daripada 64k tetapi kurang lebih sama per tugas yang terselesaikan](https://platform.claude.com/docs/images/cost-intel/max-tokens-saving-opus-5-5.svg)
</Frame>

Hampir setiap giliran selesai jauh di bawah kedua batas. Giliran panjang yang langka itulah yang dibeli oleh batas yang lebih tinggi:

<Frame>
  ![Diagram titik output per giliran untuk Opus 5.5 dan Fable 5.1: median beberapa ratus token, terpanjang 61k dan 128k, dibandingkan dengan batasnya](https://platform.claude.com/docs/images/cost-intel/max-tokens-ladder-opus-5-5.svg)
</Frame>

### Tunjukkan waktu yang telah berlalu kepada model

Model dalam loop agen tidak dapat melihat jam. [Anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) menunjukkan berapa banyak token yang tersisa, tetapi secara default tidak ada apa pun dalam permintaan yang menunjukkan berapa lama pekerjaan telah berlangsung. Dua perubahan kecil memberikan sinyal tersebut. Resep Claude Cookbook [Multi-agent teams under latency pressure and budgets](https://github.com/anthropics/claude-cookbooks/blob/main/patterns/agents/latency_multi_agent.ipynb) menggunakan dua perubahan yang sama. Akhiri pesan tugas dengan kalimat yang menyatakan bahwa waktu itu penting, dan sebelum setiap permintaan, tambahkan waktu yang telah berlalu ke akhir pesan `user` terbaru.

Anthropic mengukur kedua perubahan tersebut bersama-sama dengan Claude Opus 5.5 pada effort default-nya, `medium`, pada dua benchmark publik, DRACO[21](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dan HLE[22](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), serta pada set internal berisi 70 soal fisika tingkat riset, yang diadaptasi dari benchmark publik CritPt[23](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs). Halaman ini menyebut set tersebut sebagai set fisika. Masing-masing dari ketiganya dijalankan dengan satu agen, dengan tim di mana agen utama dapat memulai agen pembantu dari model yang sama dalam jumlah berapa pun, dan, sebagai pembanding, dengan satu agen pada effort `low` tanpa perubahan. Kecuali sebuah kalimat menyebut rata-rata, angka waktu dan biaya adalah untuk tugas tipikal: median, atas seluruh tugas, dari rasio setiap tugas antara dua konfigurasi yang dibandingkan. Diagram berikut memplot skor rata-rata terhadap biaya rata-rata per tugas untuk setiap konfigurasi. Baris kedua memberikan waktu tugas tipikal sebagai rasio, dengan kedua perubahan dibandingkan dengan pengaturan yang sama tanpa perubahan tersebut, dan pada effort `low` dibandingkan dengan `medium`. Baris ketiga memberikan perubahan skor rata-rata untuk perbandingan yang sama, dengan interval 95%-nya:

<Frame>
  ![Diagram sebar dan batang, DRACO, HLE, dan set fisika: perubahan tersebut paling banyak menghemat waktu pada DRACO, dengan pengorbanan beberapa poin skor](https://platform.claude.com/docs/images/cost-intel/time-awareness.svg)
</Frame>

**Pada tugas riset yang panjang.** Pada DRACO[21](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), kedua perubahan memangkas waktu satu agen sebesar 47% dan biayanya sebesar 60% pada tugas tipikal. Biaya rata-ratanya turun dari $1,13 USD menjadi $0,44 USD per tugas, dan agen tersebut membuat sekitar setengah jumlah permintaan per percobaan. Skornya 4,1 poin lebih rendah (interval 95% 2,9 hingga 5,2 lebih rendah).

**Pada HLE dan set fisika.** Pada HLE[22](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), perubahan yang sama memangkas waktu satu agen sebesar 14% dan biayanya sebesar 9% pada soal tipikal. Dengan juri Claude Opus 5, skornya tidak menunjukkan perubahan yang jelas (0,9 poin lebih rendah, interval 95% 2,5 lebih rendah hingga 0,7 lebih tinggi). Dengan penilai kedua, skornya 1,9 poin lebih rendah (interval 95% 0,2 hingga 3,7 lebih rendah). Pada set fisika[23](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), perubahan tersebut memangkas waktunya sebesar 7% dan biayanya sebesar 4% pada soal tipikal, dan skornya 3,0 poin lebih rendah (interval 95% 0,4 hingga 5,6 lebih rendah). Waktu rata-rata turun lebih jauh daripada waktu tugas tipikal. Pada HLE, waktu rata-rata turun 43% dan biaya rata-rata 37%, karena perubahan tersebut memotong beberapa soal yang sangat panjang. Pada set fisika, waktu rata-rata turun 14%, seluruhnya pada satu soal.

**Dengan tim.** Dalam run ini, agen utama jarang memulai agen pembantu. Tanpa perubahan, agen utama memulai agen pembantu hanya dalam 5 dari 300 percobaan pada DRACO, 13 dari 1.479 pada HLE, dan tidak satu pun dari 280 pada set fisika. Jadi hasil tim sebagian besar menunjukkan agen utama bekerja sendiri, dengan instruksi dan alat milik tim. Anthropic tidak memiliki pengukuran perubahan tersebut pada tim yang bekerja secara paralel. Tanpa perubahan, tim sudah membutuhkan sekitar setengah waktu agen tunggal pada tugas DRACO tipikal, dan mendapat skor 3,3 poin lebih rendah (interval 95% 2,1 hingga 4,6 lebih rendah). Dengan perubahan, tim membutuhkan waktu 17% lebih sedikit dengan biaya 20% lebih rendah pada tugas DRACO tipikal, dan mendapat skor 1,6 poin lebih rendah (interval 95% 0,3 hingga 2,8 lebih rendah). Pada HLE dan set fisika, waktu tim pada tugas tipikal berubah sebesar 3% atau kurang, dan skornya tidak berubah secara jelas.

**Dibandingkan dengan tingkat effort yang lebih rendah.** Menurunkan effort agen tunggal menghemat lebih banyak waktu dan biaya daripada perubahan tersebut, dan kehilangan lebih banyak skor. Pada effort `low`, agen tunggal mendapat skor 13,3 poin lebih rendah pada DRACO, 3,4 pada HLE, dan 14,0 pada set fisika dibandingkan pada `medium`, dan tugas tipikal membutuhkan waktu 84%, 30%, dan 47% lebih sedikit. Dengan perubahan pada effort `medium`, agen tersebut mendapat skor 9,2, 2,5, dan 11,0 poin lebih tinggi daripada pada `low`, dan tugas tipikal membutuhkan waktu lebih lama daripada pada `low` dengan faktor 1,2 hingga 3,2.

**Kapan menggunakannya.**

* Gunakan kedua perubahan pada tugas riset seperti DRACO ketika waktu agen penting dan pengorbanan beberapa poin skor dapat diterima. Pada HLE dan set fisika, penghematannya jauh lebih kecil.
* Periksa skor pada tugas Anda sendiri sebelum mengadopsinya. Untuk agen tunggal, skornya 4,1 poin lebih rendah pada DRACO, 3,0 poin lebih rendah pada set fisika, dan hingga 1,9 poin lebih rendah pada HLE, tergantung penilainya.
* Jika Anda mempertimbangkan tingkat effort yang lebih rendah untuk menghemat waktu, bandingkan dengan kedua perubahan tersebut. Pada ketiga set, effort `low` lebih cepat daripada perubahan pada `medium`, dan perubahan tersebut mempertahankan lebih banyak skor.

**Cara menambahkannya.** Tambahkan kalimat ini ke akhir tugas dalam pesan `user` pertama agen, setelah baris kosong. Dalam tim, tambahkan juga ke brief setiap agen pembantu:

```text wrap
Time matters here: do not spend time that can be avoided, and the earlier a correct result is obtained, the better.
```

Kemudian, sebelum setiap permintaan, termasuk yang pertama, tambahkan waktu yang telah berlalu dalam detik bulat, seperti `[elapsed 252s]`, ke akhir pesan `user` terbaru. Pada permintaan pertama, waktu tersebut ditempatkan dalam blok teksnya sendiri setelah tugas. Ketika pesan `user` terbaru membawa hasil alat, waktu tersebut ditempatkan di akhir teks hasil alat terakhir, setelah baris kosong. Ketika itu adalah pesan baru milik Anda sendiri, waktu tersebut ditempatkan dalam blok teksnya sendiri di akhir. Hitung dari awal tugas, bukan dari awal agen. Dalam tim, setiap agen membaca jam yang sama, sehingga jam pertama yang dilihat agen pembantu sudah menghitung waktu yang dihabiskan tim sebelum agen pembantu tersebut dimulai. Prompt sistem tidak berubah. Run yang diukur menggunakan kata-kata dan format ini. Jam mereka dimulai pada token pertama dari respons pertama, bukan pada awal tugas. Dalam run tim yang diukur, laporan agen pembantu sampai ke agen utama dalam pesan terpisah setelah jam, bukan di dalam hasil alat terakhir. Untuk menempatkan kalimat "Time matters here" di prompt sistem sebagai gantinya, lihat [Sinyal waktu untuk harness multiagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#time-signals-for-multi-agent-harnesses) di Prompting Claude Opus 5.5.

Biarkan jam-jam sebelumnya di tempatnya. Masing-masing menjadi bagian dari riwayat percakapan, sehingga prefiks yang di-cache tetap cocok pada permintaan berikutnya.

Contoh berikut menjalankan loop alat satu agen dengan kedua perubahan. Contoh ini hanya menangani alat klien, dan `run_tool` mengembalikan hasil setiap alat sebagai string:

```python
import time

import anthropic

client = anthropic.Anthropic()

TIME_MATTERS = (
    "Time matters here: do not spend time that can be avoided, and the earlier a "
    "correct result is obtained, the better."
)


def run_agent(task, system, tools, run_tool, started_at=None):
    """Run one agent's tool loop. In a team, pass the lead's started_at to every helper."""
    if started_at is None:
        # Detik wall-clock, agar helper di proses lain dapat berbagi waktu mulai milik lead.
        started_at = time.time()

    def clock():
        return f"[elapsed {round(time.time() - started_at)}s]"

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"{task}\n\n{TIME_MATTERS}"},
                {"type": "text", "text": clock()},
            ],
        }
    ]
    while True:
        # Gunakan streaming karena batas 128.000 token terlalu besar untuk permintaan non-streaming.
        with client.messages.stream(
            model="claude-opus-5-5",
            max_tokens=128000,
            cache_control={"type": "ephemeral"},
            system=system,
            tools=tools,
            messages=messages,
        ) as stream:
            response = stream.get_final_message()
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            return response
        results = [
            {
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": run_tool(block.name, block.input),
            }
            for block in response.content
            if block.type == "tool_use"
        ]
        # Jam diletakkan di akhir pesan pengguna terbaru: hasil alat terakhir.
        results[-1]["content"] += f"\n\n{clock()}"
        messages.append({"role": "user", "content": results})
```

Pada Claude Managed Agents, Anda dapat menambahkan kalimat tersebut ke tugas dalam event `user.message` yang memulai sesi, dan jam ke setiap event `user.message` dan [`user.custom_tool_result`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#handling-custom-tool-calls) yang Anda kirim. Giliran yang mengikuti alat bawaan platform, seperti pencarian web, melihat jam terakhir yang Anda kirim, bukan waktu saat ini. Dalam [sesi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration), koordinator menulis brief setiap worker, sehingga klien Anda tidak dapat menambahkan kalimat tersebut ke dalamnya. Worker hanya melihat jam dalam hasil alat kustom yang Anda jalankan untuknya. Anthropic tidak mengukur perubahan tersebut pada Claude Managed Agents. Untuk menunjukkan waktu saat ini sebelum setiap permintaan, dan kepada setiap agen dalam tim, jalankan sendiri loop agen pada Messages API.

## Menggabungkan model

Arsitektur multi-model cocok untuk beban kerja yang kompleksitas tugasnya cukup bervariasi sehingga langkah-langkah berbeda paling baik dilayani oleh model berbeda. Ketika lalu lintas Anda mencampur pekerjaan rutin yang ditangani model lebih kecil dengan andal dengan langkah-langkah lebih sulit yang membutuhkan kemampuan frontier, membagi pekerjaan menjaga kecerdasan frontier di tempat yang penting sementara sebagian besar token ditagih dengan tarif model lebih kecil. Ketika beban kerja tidak memiliki campuran itu, karena kesulitannya seragam atau berupa satu rantai yang saling bergantung, satu model yang disetel dengan baik biasanya merupakan pilihan yang lebih baik. Setiap bagian strategi memberikan aturan untuk membedakan kedua kasus tersebut.

Dua strategi mencakup sebagian besar beban kerja, dan keduanya berbeda dalam model mana yang memegang loop utama:

| Strategi         | Alur kontrol                                                      | Peran model frontier                      | Cocok untuk                                                                                                                     | Biaya frontier meningkat seiring                |
| ---------------- | ----------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **Advisor**      | Model lebih kecil menjalankan loop, mengeskalasi sesuai kebutuhan | Dikonsultasikan untuk rencana dan koreksi | Pekerjaan serial yang sulit di beberapa titik, seperti banyak giliran agen coding di antara beberapa keputusan nyata            | Seberapa sering executor macet                  |
| **Orchestrator** | Model frontier menjalankan loop, mendelegasikan pekerjaan massal  | Merencanakan, mengirim, dan mensintesis   | Pekerjaan yang menyebar ke file, dokumen, atau kasus yang benar-benar independen, terutama yang lebih dari satu jendela konteks | Seberapa sulit bagian-bagiannya dikoordinasikan |

### Strategi advisor: eskalasikan keputusan sulit

Dalam strategi advisor, model "executor" (pelaksana) berbiaya lebih rendah menjalankan loop agen dan mengerjakan sebagian besar giliran. Ketika model ini menghadapi keputusan yang membutuhkan penilaian lebih mendalam, seperti memilih pendekatan atau memulihkan diri dari kegagalan, model ini memanggil model "advisor" (penasihat) dengan kecerdasan lebih tinggi untuk mendapatkan panduan strategis, lalu melanjutkan. Sebagian besar token ditagih dengan tarif executor, dan hanya konsultasi sesekali yang ditagih dengan tarif advisor.

Untuk menggunakannya, tambahkan [alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) ke permintaan Anda. Fitur beta ini menjalankan seluruh strategi di sisi server dalam satu permintaan `/v1/messages`: executor mengeluarkan pemanggilan alat, Anthropic menjalankan inferensi advisor, dan executor melanjutkan dengan saran tersebut; Anda tidak menulis kode orkestrasi apa pun. Pada Claude Managed Agents, [berikan advisor kepada sesi](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor) dengan menambahkan entri `advisor` ke roster `multiagent` agen; thread utama sesi berkonsultasi dengannya dengan cara yang sama. Claude Code juga mendukungnya; lihat [mengeskalasikan keputusan sulit dengan alat advisor](https://code.claude.com/docs/en/advisor).

<Frame>
  ![Diagram strategi advisor: model executor menjalankan loop utama dan memanggil advisor Claude Fable 5.1 sesuai kebutuhan](https://platform.claude.com/docs/images/model-routing-advisor-strategy.svg)
</Frame>

**Apa yang menentukan hasilnya.** Advisor melihat tugas hanya melalui panggilan executor, sehingga dua hal menentukan seberapa besar bantuannya.

Yang pertama adalah kesenjangan antara kedua model. Advisor hanya dapat menyerahkan kemampuan yang tidak dimiliki executor: pada GPQA Diamond[9](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), Claude Sonnet 5.5 saja menyamai Claude Opus 5.5 saja di 91% dengan penolakan dihitung sebagai salah, tetapi hanya karena Opus 5.5 menolak enam pertanyaan biologi per run dibandingkan satu pada Sonnet 5.5. Pada pertanyaan yang dijawab masing-masing, Opus 5.5 unggul sekitar 2 poin. Claude Haiku 5.5 saja mendapat skor 6 poin di bawah Opus 5.5 (85%), sehingga advisor Opus 5.5 memiliki lebih banyak hal untuk diserahkan kepadanya.

Yang kedua, dan yang rapuh, adalah apakah executor benar-benar bertanya ("consult rate" atau tingkat konsultasi). Tidak satu pun dari executor tersebut bertanya. Dalam dua run masing-masing, Claude Haiku 5.5 dan Claude Sonnet 5.5 tidak memanggil advisor Opus 5.5 pada satu pun dari 198 pertanyaan, sehingga kedua pasangan mendapat skor dalam batas noise antar-run dari executor saja. Run ini menambahkan alat advisor apa adanya, tanpa prompt sistem yang meminta executor untuk berkonsultasi dengannya, seperti prompt yang [disarankan halaman alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#prompting-for-coding-and-agent-tasks). Definisi alat advisor, sekitar 1.000 token prompt per permintaan, tetap menambah 12% pada biaya per pertanyaan Haiku 5.5 dan 25% pada Sonnet 5.5. Executor dengan effort rendah dapat berhenti mendeteksi bahwa dirinya buntu: pasangan yang berkonsultasi pada sebagian besar tugas dengan effort default dapat turun menjadi hampir tidak berkonsultasi sama sekali ketika effort diturunkan, lalu mendapat skor di bawah executor saja. Tingkat ini juga bervariasi menurut tugas: pada DeepSWE[10](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) executor Sonnet 5 dengan effort rendah terus bertanya dan memperoleh 23 poin; pada SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) executor yang sama berhenti bertanya. Dalam grafik berikut, hanya executor pada pasangan coding yang berkonsultasi pada sebagian besar percobaan, dan hanya peningkatannya yang dapat dikreditkan kepada advisor: 1,7 poin di atas Opus 5.5 saja pada `high`, di batas noise antar-run. Executor yang jarang atau tidak pernah berkonsultasi tidak memperoleh apa pun di luar noise, dan yang berada pada effort `low` kehilangan 7 poin. Ketika executor memang bertanya, Anda membayar model yang lebih kuat hanya untuk konsultasinya, dan itulah yang memungkinkan kasus penghematan biaya:

<Frame>
  ![Grafik batang empat pasangan advisor dari model Claude saat ini: kesenjangan yang tersedia versus peningkatan yang terealisasi, diberi label consult rate (tingkat konsultasi); hanya executor pasangan coding yang sering berkonsultasi, dan hanya peningkatannya yang dapat dikreditkan kepada advisor](https://platform.claude.com/docs/images/cost-intel/advisor-mechanism-v2.svg)
</Frame>

Tingkat konsultasi merespons prompting. Dengan hanya deskripsi bawaan alat, executor kurang sering memanggil, terutama pada pekerjaan coding, sehingga [dokumentasi alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#prompting-for-coding-and-agent-tasks) memberikan prompt sistem yang meminta satu panggilan sebelum pekerjaan substantif dan satu sebelum selesai, sekitar dua hingga tiga panggilan per tugas. Pasangan coding yang diukur berikutnya berjalan dengan ritme tersebut dengan Claude Opus 5 sebagai executor, sekitar dua konsultasi pada setiap tugas; dengan Claude Opus 5.5 sebagai executor, ia meminta saran sekitar 1,4 kali per percobaan, dan 4% percobaannya tidak menerima saran. Halaman tersebut juga membahas cara mendorong executor yang kurang sering memanggil dan membatasi panggilan di sisi klien untuk membatasi biaya. Jadi, pantau tingkat konsultasi: buat prompt untuknya, ukur, dan pulihkan effort executor jika tingkat tersebut anjlok.

**Kapan menguntungkan dari sisi biaya.** Advisor menghemat uang ketika beberapa konsultasi singkat, yang ditagih dengan tarif advisor, menggantikan menjalankan model advisor untuk seluruh tugas. Hal ini paling efektif ketika harga model advisor jauh di atas executor, sehingga konfigurasi paling hemat biaya adalah advisor frontier di atas executor kelas menengah. Pasangan di puncak rentang dapat memulihkan sebagian biaya saran, karena saran juga menghemat token executor: executor yang diberi tahu pendekatan yang tepat menjelajahi lebih sedikit jalan buntu. Pada pasangan coding di bawah dengan executor Claude Opus 5, penghematan tersebut membayar sekitar setengah dari biaya saran: executor menghabiskan $1,26 USD lebih sedikit per percobaan dibandingkan Opus 5 saja pada default-nya, dan konsultasinya berbiaya $2,47 USD. Dengan executor Claude Opus 5.5, saran hampir tidak menghemat biaya executor: $1,36 USD per percobaan dibandingkan $1,38 USD untuk Opus 5.5 saja pada `high`, sementara konsultasinya berbiaya $1,55 USD.

Pada benchmark agentic-coding internal[11](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), yang dijalankan dengan agen API biasa, executor Claude Opus 5.5 pada `high` dengan advisor Claude Fable 5.1 mendapat skor 90,1% dengan biaya $2,92 USD per percobaan. Itu 1,7 poin di atas Opus 5.5 saja pada `high`, pengaturan executor itu sendiri, kesenjangan di batas noise antar-run dengan lima percobaan per tugas, dengan biaya sekitar 2,1 kali lipat; dibandingkan Opus 5.5 pada default-nya, `medium`, selisihnya 3,5 poin dengan biaya sekitar 3,5 kali lipat. Hasil ini kira-kira berada pada kurva effort Opus 5.5 sendiri, sehingga advisor membeli kurang lebih apa yang dibeli oleh effort tambahan: Opus 5.5 saja pada `xhigh` mendapat skor 91,1% dengan biaya $4,11 USD per percobaan (satu percobaan per tugas). Pada bulan Agustus, advisor Claude Fable 5.1 di atas executor Claude Opus 5 adalah konfigurasi paling akurat yang diukur, dengan biaya $6,21 USD per percobaan, sedikit lebih dari dua kali biaya pasangan Opus 5.5. Grafik ini memplot pasangan Opus 5.5 terhadap kurva effort Opus 5.5 sendiri dan kurva Claude Fable 5.1 dari bulan Agustus:

<Frame>
  ![Benchmark coding: Opus 5.5 pada high dengan advisor Fable 5.1 memperoleh 1,7 poin dengan 2,1 kali biaya, dekat dengan kurva effort-nya](https://platform.claude.com/docs/images/cost-intel/internal-coding-advisor-opus-5-5.svg)
</Frame>

Pengukuran sebelumnya melalui [mode advisor Claude Code](https://code.claude.com/docs/en/advisor) juga menempatkan pasangan advisor-nya di atas kedua modelnya masing-masing. Baca hasil Claude Opus 5.5 sebagai pola yang perlu diuji pada beban kerja Anda: advisor membeli beberapa poin dengan biaya sekitar dua kali biaya executor saja. Kesenjangan kemampuan yang lebih lebar tidak menjamin kesepakatan yang lebih baik. Biaya latensinya adalah konsultasi itu sendiri: sekitar satu atau dua panggilan model frontier tambahan per tugas pada benchmark ini, masing-masing berada di jalur kritis tugas.

**Kapan model yang lebih kuat saja merupakan langkah yang lebih baik.** Jika akurasi beban kerja merespons effort, bandingkan pasangan tersebut dengan model advisor saja pada pengaturan yang lebih rendah sebelum membangunnya: advisor hanya dibayar pada tugas yang membutuhkannya, tetapi konsultasi yang terjadi pada sebagian besar tugas lebih mahal daripada menjalankan model yang lebih kuat itu sendiri. Pada Chartography[13](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), executor Claude Opus 5.5 pada `low`, yang diberi advisor Claude Fable 5.1, berkonsultasi dengannya pada 1 dari 300 tugas dan mendapat skor 61,7, 7 poin di bawah Opus 5.5 saja dan di luar noise antar-run, dengan biaya yang kurang lebih sama; pada bulan Agustus, executor Claude Opus 5 berkonsultasi pada hampir setiap tugas, dan pasangan tersebut menyamai Fable 5.1 saja pada `medium` dalam batas noise antar-run (65,0 dibandingkan 67,5) dengan biaya sekitar 1,8 kali per tugas. Ukur tingkat konsultasi Anda sendiri terlebih dahulu: jika executor bertanya pada sebagian besar tugasnya, Anda membayar tarif advisor di seluruh beban kerja, dan menjalankan model advisor itu sendiri adalah cara yang lebih murah untuk mencapai skor yang sama.

Apa pun pasangannya, hitung terlebih dahulu harga model advisor saja pada effort rendah; itulah baseline yang harus dikalahkan. Periksa ulang pada setiap rilis model, karena rilis menggeser baik kesenjangan kemampuan maupun rasio harga.

**Kapan cocok.** Strategi advisor cocok untuk beban kerja di mana giliran sebagian besar bersifat mekanis tetapi rencana yang sangat baik itu penting: agen coding, computer use, dan pipeline riset multilangkah. Strategi ini kurang cocok ketika setiap giliran benar-benar membutuhkan kemampuan frontier, ketika tidak ada yang perlu direncanakan (tanya jawab satu giliran), atau ketika executor Anda sudah mendekati kemampuan advisor.

### Strategi orchestrator: delegasikan pekerjaan massal

Dalam strategi "orchestrator" (pengatur), model frontier memegang loop. Model ini menguraikan tugas, mengirimkan subtugas ke model "worker" (pekerja) berbiaya lebih rendah, dan menggabungkan hasilnya. Transkrip orchestrator sendiri tetap pendek karena worker menyerap eksplorasi yang boros token, sehingga sebagian besar token ditagih dengan tarif worker sementara rencana dan sintesis tetap berasal dari model frontier.

Untuk membangunnya, gunakan [orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) di Claude Managed Agents: konfigurasikan agen "coordinator" (koordinator, yaitu orchestrator) dan daftar agen worker, masing-masing dengan modelnya sendiri. Untuk contoh lengkap yang berfungsi dengan koordinator frontier dan worker Claude Sonnet 5, lihat resep Claude Cookbook [Coordinator pattern: big models for planning, small models for execution](https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_plan_big_execute_small.ipynb).

<Frame>
  ![Diagram strategi orchestrator: orchestrator Claude Fable 5.1 menyebarkan subtugas ke tiga worker Claude Sonnet 5](https://platform.claude.com/docs/images/model-routing-orchestrator-strategy.svg)
</Frame>

Pola ini menghemat waktu nyata ketika worker dapat berjalan secara paralel: pada benchmark korpus[8](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), satu episode memakan waktu sekitar 2,3 jam dengan koordinator menjalankan batas terdokumentasi platform sebanyak 25 worker bersamaan, dibandingkan 15 hingga 20 jam jika dijalankan sendiri. Pola ini menghemat uang hanya dalam dua situasi yang diukur. Pada pekerjaan yang dapat ditangani oleh satu model saja, model yang sama dengan effort lebih rendah selalu lebih murah.

**Kasus 1: asuransi terhadap ekor biaya pada pekerjaan rutin.** Model frontier yang berjalan sendiri sesekali berputar-putar pada masalah rutin yang biasanya dapat diselesaikannya. Karena Anda tidak dapat mengetahui sebelumnya run mana yang akan demikian, beberapa run seperti itu mendominasi tagihan. Koordinator yang menyerahkan pekerjaan rutin kepada worker berbiaya lebih rendah membatasi ekor tersebut, karena setiap perputaran kini terjadi dengan tarif worker.

Anthropic mengukur hal ini pada potongan BrowseComp[4](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) yang sengaja dibuat mudah (10 masalah yang andal diselesaikan oleh model tunggal; 50 run terdelegasi dan 70 run tunggal). Koordinator Claude Fable 5 dengan satu worker Claude Sonnet 5 berbiaya sekitar setengah dari Claude Fable 5 saja secara rata-rata dan sekitar sepertiga pada persentil ke-90 ($12 USD dibandingkan $33 USD), dan run tunggal termahal dari model tunggal, sebesar $84 USD, juga salah:

<Frame>
  ![Dot plot, potongan rutin BrowseComp: run terdelegasi berbiaya sekitar setengah dari Claude Fable 5 saja secara rata-rata, sepertiga pada persentil ke-90](https://platform.claude.com/docs/images/cost-intel/tail-insurance.svg)
</Frame>

Delegasi menguntungkan pada bagian pekerjaan yang rutin dan biasanya dapat diselesaikan, kebalikan dari intuisi bahwa worker ditujukan untuk masalah sulit. Pada set BrowseComp lengkap yang lebih sulit, ekonominya berbalik. Jika lalu lintas Anda memiliki ekor biaya panjang pada tugas rutin, inilah kasus orchestrator yang perlu diukur terlebih dahulu.

**Kasus 2: pekerjaan yang lebih besar dari satu jendela konteks.** Model tunggal harus mengerjakan input sebesar itu secara serial, satu "context window" (jendela konteks) pada satu waktu, dengan membayar untuk membaca ulang state-nya sendiri pada setiap putaran. Worker masing-masing membaca partisinya sendiri, secara paralel dan dengan tarif worker. Pekerjaan yang berat pada pembacaan tetapi masih muat dalam satu jendela konteks adalah masalah pemilihan model, bukan masalah delegasi: dari sisi biaya pembacaan saja, orchestrator hanya unggul ketika tidak ada satu konteks pun yang dapat menampung pekerjaan tersebut.

Anthropic membangun benchmark untuk kasus ini[8](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs): korpus 21,6 juta token dari 14 paket Python publik dengan 130 cacat yang ditanam, terlalu besar untuk jendela konteks mana pun. Menurunkan effort tidak dapat membantu, karena tagihannya adalah pembacaan korpus itu sendiri: Claude Fable 5.1 tunggal berbiaya $468 USD hingga $552 USD per episode di ketiga pengaturan effort, dan hanya akurasinya yang berubah. Konfigurasi koordinator, yaitu Claude Fable 5.1 sebagai pemimpin di atas 25 worker Claude Sonnet 5, berbiaya sekitar setengah dari pengaturan tersebut (47% hingga 55% lebih murah) dan mendapat skor 10 hingga 12 poin di bawahnya, dalam sekitar 2,3 jam per episode dibandingkan 15 hingga 20 jam, sambil mengalahkan baseline Claude Sonnet 5 tunggal secara langsung:

<Frame>
  ![Grafik, benchmark korpus: "coordinator" (koordinator) berbiaya sekitar setengah dari Fable 5.1 tunggal pada effort apa pun, sekitar 12 poin di bawah hasil terbaiknya](https://platform.claude.com/docs/images/cost-intel/corpus-pareto.svg)
</Frame>

Perhitungan token menunjukkan skala pembacaannya: konfigurasi koordinator membaca sekitar 560 juta token cache per episode, sekitar satu setengah kali dari sekitar 365 juta milik model tunggal, hampir semuanya dengan tarif cache-read Claude Sonnet 5, dan tetap berbiaya sekitar setengahnya secara keseluruhan. Fable 5.1 pada effort `high` tetap memegang akurasi puncak, dengan biaya sekitar 2,2 kali biaya konfigurasi koordinator, sehingga delegasi di sini membeli sebagian besar akurasi, bukan seluruhnya.

**Kapan delegasi tidak menguntungkan.** Orchestrator hanya memberikan manfaat ketika ada pekerjaan massal untuk diserahkan: banyak bagian independen, idealnya terlalu banyak untuk satu jendela konteks. Ketika pekerjaan berupa satu rantai yang saling bergantung, atau muat dalam satu konteks, orchestrator membayar untuk rencana, serah terima, dan penggabungan yang didapatkan model tunggal secara gratis. Dalam setiap kasus seperti itu yang diukur, model koordinator saja dengan effort lebih rendah lebih unggul.

Batasnya adalah tingkat kesulitan tugas, bukan benchmark-nya: pada set BrowseComp[4](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) lengkap yang lebih sulit, Claude Fable 5 saja mencapai akurasi konfigurasi koordinator dengan biaya 22% hingga 30% lebih rendah. Penelitian eksternal independen melaporkan pola yang sama[5](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs). Jika pekerjaan berupa satu rantai, muat dalam satu konteks tanpa ekor biaya panjang, atau satu model dengan effort lebih rendah sudah memenuhi standar Anda, jangan membangun orchestrator.

### Memilih di antara strategi

Sebagian besar kasus bermuara pada satu pertanyaan: apakah pekerjaan terbagi menjadi bagian-bagian independen, atau berupa satu jawaban yang dicapai melalui rantai langkah yang saling bergantung? [Tabel strategi](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#combine-models) memetakan kedua jawaban ke kedua strategi.

Jika Anda tidak yakin, jangan membangun apa pun dulu:

1. Sapu effort pada model Anda saat ini terlebih dahulu. Ini adalah eksperimen termurah di halaman ini, dan sebagian besar beban kerja berakhir di sana.
2. Jika sapuan menunjukkan kesenjangan, hitung harga model yang lebih kuat sendirian pada effort rendah. Itulah angka yang harus dikalahkan oleh pasangan advisor, dan pasangan di halaman ini yang mengalahkannya adalah yang executor-nya benar-benar berkonsultasi.

Hasil multi-model di halaman ini dinilai terhadap model yang sama pada effort lebih rendah dan terhadap model satu tingkat di bawahnya yang berjalan sendirian. Itulah perbandingan yang harus dijalankan pada beban kerja Anda sendiri, dan alasan mengapa langkah pertama adalah sapuan effort.

Ketika Anda menambahkan advisor, itu berupa definisi alat, bukan perancangan ulang arsitektur.

## Ukur pada beban kerja Anda sendiri

Angka-angka di halaman ini mencerminkan harga daftar pada saat pengukuran dan akan bergeser seiring perubahan model dan harga. Tingkat eskalasi Anda, seberapa rapi tugas dapat dipecah, dan panjang transkrip juga memengaruhinya. Namun, metodenya tetap sama:

1. Ambil beberapa tugas dari log produksi dengan bobot yang mencerminkan lalu lintas nyata, lalu [tulis pemeriksaan hasil](https://platform.claude.com/docs/id/test-and-evaluate/develop-tests) untuk masing-masing tugas, misalnya tes lulus, tiket ditutup, atau jumlah baris benar. Catat biaya per tugas di samping skornya. Untuk menghitung biaya, kalikan kelima jumlah token berbayar dalam `usage` setiap respons dengan tarifnya masing-masing: input tanpa cache, penulisan cache 5 menit dan 1 jam (masing-masing 1,25x dan 2x harga input), pembacaan cache, dan output. Jumlahkan hasilnya di seluruh permintaan dalam tugas tersebut ([Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api) melaporkan totalnya).
2. Buat baseline untuk setiap tingkatan model di berbagai level effort, bukan hanya pada level default, lalu plot skor terhadap pengeluaran. Konfigurasi multi-model harus mengalahkan seluruh kurva model tunggal.
3. Jika kurva menunjukkan kesenjangan yang tidak dapat ditutup dengan effort, tambahkan strategi multi-model yang sesuai dan jalankan ulang rangkaian pengujian.
4. Jalankan konfigurasi pemenang dalam mode shadow pada sebagian lalu lintas sebelum beralih sepenuhnya, lalu biarkan rangkaian pengujian tetap berjalan.

Contoh berikut menghitung biaya langkah 1 untuk satu permintaan dengan harga daftar Claude Opus 5.5:

<CodeGroup>
  ```bash cURL
  # Harga per juta token dari halaman harga; ubah ketiga nilai ini untuk model lain.
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
  # Harga per juta token dari halaman harga; ubah ketiga nilai ini untuk model lain.
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
  # Harga per sejuta token dari halaman harga; ubah ketiga nilai ini untuk model lain.
  INPUT_PER_MTOK = 4.00  # Claude Opus 5.5
  # 0,05x harga input pada Claude Opus 5.5; pengalinya berbeda per model
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
  // Harga per juta token dari halaman harga; ubah ketiga nilai ini untuk model lain.
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
  // Harga per juta token dari halaman harga; ubah ketiga nilai ini untuk model lain.
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
  // Harga per juta token dari halaman harga; ubah ketiga nilai ini untuk model lain.
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
  // Harga per juta token dari halaman harga; ubah ketiga nilai ini untuk model lain.
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
  // Harga per juta token dari halaman harga; ubah ketiga nilai ini untuk model lain.
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
  # Harga per juta token dari halaman harga; ubah ketiga nilai ini untuk model lain.
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

Dalam loop agen, sebagian besar token input seharusnya berupa pembacaan cache. Jika `cache_read_input_tokens` kecil dibandingkan `input_tokens` ditambah `cache_creation_input_tokens`, pastikan caching aktif dan prefiks tetap sama di antara permintaan. Ketika [alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#usage-and-billing) atau ["compaction" (pemadatan)](https://platform.claude.com/docs/id/build-with-claude/compaction-threshold#understanding-usage) diaktifkan, sebagian token hanya dilaporkan dalam `usage.iterations` dan tidak tercakup dalam total tingkat atas. Dalam kasus ini, jumlahkan token dari `usage.iterations`, dan hitung biaya entri `advisor_message` dengan tarif model advisor.

Tabel berikut mencantumkan tuas-tuas penghematan sesuai urutan yang disarankan untuk dicoba:

| Tuas                                         | Penghematan dalam run ini                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Dampak pada kualitas                                                                  | Latensi                                            | Lokasi                                                                                                                                                                                  |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Caching prompt                               | Biaya turun 2,7 hingga 5,3 kali lipat pada loop agen; 83% pada run triase                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Tidak ada                                                                             | Lebih cepat                                        | [Cache konteks berulang](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#cache-repeated-context)                                           |
| Durasi cache 1 jam                           | Lebih murah daripada default 5 menit jika sekitar 1 dari 20 giliran mengikuti jeda antara 5 menit dan satu jam, dan hanya sedikit jeda yang melebihi satu jam. Pengecualiannya adalah Claude Fable 5.1, yang lebih murah jika cache 5 menit dijaga tetap hangat selama jeda hanya beberapa menit, sedangkan durasi 1 jam lebih unggul jika jeda mendekati satu jam; serta Claude Opus 5.5, yang lebih murah jika cache 5 menit dijaga tetap hangat ketika hanya satu atau dua dari 20 giliran yang mengikuti jeda hingga sekitar setengah jam. Tanpa jeda, default berbiaya 15% lebih rendah pada Claude Sonnet 5 dan sekitar 15% hingga 18% lebih rendah pada Claude Opus 5.5 | Tidak ada                                                                             | Tetap hangat setelah jeda                          | [Pilih durasi cache](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#pick-the-cache-duration)                                              |
| Pemangkasan input                            | Tambahan 5 poin persentase pada run triase                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Tidak ada                                                                             | Netral                                             | [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens)                           |
| Pangkas hasil alat yang usang di batas tugas | 39% pada run triase panjang (compaction 32%); tidak ada pada loop pendek                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Tidak ada yang terukur                                                                | Netral                                             | [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens)                           |
| Tool search                                  | 45% dengan 500 definisi alat terpasang; 20% dengan server MCP GitHub                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Tidak ada                                                                             | Netral                                             | [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens)                           |
| File data melalui eksekusi kode              | 92% pada tugas data berisi 25 pertanyaan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Meningkat, 25 dari 25 alih-alih 6 dari 25                                             | Lebih cepat                                        | [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens)                           |
| Batch API                                    | 50%                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Tidak ada                                                                             | Hasil dalam 24 jam                                 | [Batch pekerjaan yang bisa menunggu](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#batch-work-that-can-wait)                             |
| Audit prompt terhadap model saat ini         | 14% pada kedua migrasi yang diukur                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Tidak ada; meningkat pada salah satunya                                               | Lebih cepat (lebih sedikit putaran alat)           | [Audit prompt terhadap model saat ini](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#audit-prompts-against-the-current-model)            |
| Upgrade model                                | Opus 4.8 ke Opus 5: skor naik 12 poin dengan biaya 21% lebih tinggi per tugas yang terselesaikan (Opus 5 pada `low` mengalahkan Opus 4.8 dengan sekitar 30% biayanya); Sonnet 4.6 ke Sonnet 5: biaya 15% lebih rendah per tugas yang terselesaikan, skor naik 5 poin; Fable 5 ke Fable 5.1: biaya 43% lebih rendah per tugas yang terselesaikan dengan skor yang hampir sama                                                                                                                                                                                                                                                                                                   | Meningkat                                                                             | Netral                                             | [Upgrade model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#upgrade-the-model)                                                         |
| Turunkan effort                              | Pekerjaan pengetahuan: `medium` 13% hingga 31%, `low` sepertiga hingga setengah; coding panjang: `medium` sekitar 30% dan `low` sekitar dua pertiga, keduanya dibandingkan dengan `high`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Turun 1 hingga 3 poin pada pekerjaan pengetahuan, 2 hingga 8 poin pada coding panjang | Lebih cepat                                        | [Setel effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort)                                                                |
| Jalankan ulang tugas yang gagal              | Sekitar 40% dibandingkan menjalankan semuanya pada `high`, dengan tingkat kelulusan yang sama atau sedikit lebih baik                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Tidak ada                                                                             | Dua run pada tugas yang gagal                      | [Jalankan ulang kegagalan pada effort yang lebih tinggi](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#re-run-failures-at-higher-effort) |
| Anggaran tugas                               | 44% hingga 58%                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Turun 3 hingga 6 poin                                                                 | Lebih cepat                                        | [Tetapkan anggaran dan batas output](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                          |
| Minta jawaban yang lebih singkat             | 39% token output, 14% biaya pada run triase                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Tidak ada                                                                             | Lebih cepat                                        | [Tetapkan anggaran dan batas output](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                          |
| Menaikkan `max_tokens`                       | Tidak ada per tugas yang terselesaikan, tetapi lebih banyak tugas yang terselesaikan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Naik hingga 22 poin pada set internal; tidak ada pada pasangan publik                 | Netral                                             | [Tetapkan anggaran dan batas output](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                          |
| Advisor                                      | Bergantung pada kesenjangan kemampuan dan tingkat konsultasi. Pasangan coding mencetak skor 1,7 poin di atas Claude Opus 5.5 yang berjalan sendiri pada `high` dengan biaya sekitar 2,1 kali lipat, kira-kira setara dengan hasil dari menaikkan effort. Dengan Claude Opus 5.5, pasangan pembacaan grafik hampir tidak pernah berkonsultasi dengan advisor dan skornya 7 poin di bawah Opus 5.5 yang berjalan sendiri                                                                                                                                                                                                                                                         | Meningkat pada coding, menurun pada pembacaan grafik                                  | Sekitar satu atau dua panggilan tambahan per tugas | [Strategi advisor](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#advisor-strategy-escalate-hard-decisions)                               |
| Orchestrator                                 | Sekitar setengah dibandingkan model frontier, baik untuk pekerjaan yang melebihi satu jendela konteks maupun pada ekor biaya tugas rutin (yang terakhir diukur pada Claude Fable 5)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 10 hingga 12 poin di bawah model frontier                                             | Jauh lebih cepat pada input besar                  | [Strategi orchestrator](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#orchestrator-strategy-delegate-bulk-work)                          |

## Benchmark yang dirujuk

Kecuali jika suatu referensi menyatakan lain, pengukuran merupakan eksekusi internal Anthropic atas benchmark-benchmark ini. Kecuali dicatat lain, biaya dinyatakan dalam USD pada harga daftar yang berlaku saat setiap benchmark dijalankan; angka Claude Sonnet 5 menggunakan $2 USD dan $10 USD per juta token input dan output. Grafik berlabel "notional USD" menghitung harga jumlah token setiap permintaan pada tarif tersebut alih-alih melaporkan tagihan.

1. **WideSearch:** Wong et al., "WideSearch: Benchmarking Agentic Broad Info-Seeking," arXiv:2508.07999, 2025. Tugas riset web luas yang dinilai berdasarkan kelengkapan dan akurasi tabel dengan banyak baris; 200 soal, 3 eksekusi per konfigurasi, dijalankan 1 hingga 2 Agustus 2026. Grafik konsentrasi biaya adalah eksekusi terpisah atas 20 soal, 3 eksekusi per soal, dijalankan 3 hingga 4 Agustus 2026, dengan biaya dihitung dari catatan penagihan per permintaan.
2. **GDPval:** OpenAI, "GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks," 2025. Hasil kerja pengetahuan yang dinilai terhadap rubrik tugas; eksekusi 210 tugas dari gold set yang dirilis, satu percobaan per tugas, dijalankan 2 Agustus 2026. Model Claude yang menilai, sehingga skor absolut dapat berbeda dari hasil yang dipublikasikan.
3. **SWE-bench Pro:** Scale AI, "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?", 2025. Subset 482 soal yang dipilih karena kompatibel dengan harness evaluasi Anthropic; skornya tidak dapat dibandingkan dengan leaderboard publik. Skor ini juga tidak dapat dibandingkan dengan hasil SWE-bench Pro dalam system card Claude Opus 5.5, yang berasal dari eksekusi pada effort `max` dengan set soal yang berbeda. Angka Claude Opus 5.5 merupakan rata-rata dua eksekusi pada `low`, `medium` (default-nya), dan `high`, serta menggunakan satu eksekusi pada `xhigh`, semuanya dijalankan 19 hingga 20 September 2026, dengan batas 16.384 token per giliran yang sama seperti eksekusi Claude Opus 5 bulan Agustus; batas tersebut memotong 2 percobaan `xhigh` dan tidak ada pada pengaturan lain. Eksekusi Opus 5.5 menggunakan versi benchmark yang container penilaiannya hanya dapat menjangkau mirror paket internal. Versi tersebut menghapus satu soal yang pengujiannya memerlukan situs web aktif, dan pada tiga soal lainnya solusi referensi gagal di sana, sehingga perbandingan Opus 5.5, beserta angka Claude Fable 5.1 yang disandingkan dengannya, menggunakan 478 soal yang tersisa. Angka SWE-bench Pro Claude Opus 5 di [Upgrade model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#upgrade-the-model) dan [grafik pasangan advisor](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#advisor-strategy-escalate-hard-decisions) merupakan rata-rata dua eksekusi pada effort default-nya dan menggunakan satu eksekusi pada `low`, semuanya dijalankan 4 Agustus 2026. Angka eskalasi berasal dari eksekusi Opus 5.5, tugas demi tugas: `low` terlebih dahulu, lalu `high` pada kegagalannya, menyelesaikan 96,4% hingga 97,5% di seluruh pasangan eksekusi dengan biaya sekitar $0,17 USD; `medium` terlebih dahulu, 96,0% hingga 97,1% dengan biaya sekitar $0,24 USD; `high` dijalankan ulang pada kegagalannya sendiri, 96,9% dengan biaya $0,31 USD; semuanya pada `high`, 94,8% hingga 95,8% dengan biaya $0,29 USD. Biaya pada subset ini dihitung sebagaimana organisasi pelanggan diukur: prompt sebelumnya dari setiap permintaan sebagai cache read dan token barunya sebagai cache write 5 menit, dari catatan penggunaan eksekusi itu sendiri, diperiksa terhadap buku besar pelanggan; pengukuran milik organisasi evaluasi sendiri, yang hingga 10 September 2026 menagih cache read dalam blok 8.192 token untuk Claude Opus 5, Claude Fable 5, Claude Opus 4.7, dan Claude Opus 4.8, menghasilkan angka 1,4 hingga 1,8 kali lebih tinggi untuk eksekusi model-model tersebut; untuk Claude Fable 5.1, Claude Sonnet 5, dan Claude Sonnet 4.6 keduanya berbeda paling banyak sekitar 9%, dan untuk angka Claude Opus 5.5 keduanya sesuai dalam rentang 3% pada setiap pengaturan effort. Pasangan executor Claude Sonnet 5 pada grafik advisor berasal dari rangkaian pengukuran yang sama pada subset ini: pasangan Sonnet-plus-Opus 5 dijalankan dua kali (7 Agustus dan 8 Agustus 2026, satu eksekusi dan satu replikasi persis), pasangan effort rendah sekali (8 Agustus 2026), dan Claude Sonnet 5 sendiri dua kali (77,4%, baseline untuk kedua baris Pro). Titik Claude Fable 5 di Upgrade model adalah rata-rata tiga eksekusi pada effort default, dijalankan 26 Agustus 2026, dengan harga dihitung dengan cara yang sama. Angka anggaran tugas Claude Fable 5.1 adalah satu eksekusi per anggaran (dua pada 35.000 token) pada subset yang sama dengan effort default, dijalankan 26 Agustus 2026, dengan eksekusi tanpa anggaran pada hari yang sama (92,1%, $1,10 USD per tugas) sebagai baseline; set sebelumnya pada effort `low`, dijalankan 21 Agustus 2026, mencetak skor 88,6% tanpa anggaran dengan biaya $0,48 USD per tugas. Perbandingan [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task) memasangkan eksekusi tunggal tersebut dengan dua eksekusi Claude Sonnet 5 gabungan dari subset yang sama; pada effort default Fable 5.1, pasangan tersebut menunjukkan arah sebaliknya, 41% lebih mahal per tugas yang terselesaikan dibandingkan Sonnet 5. Tangga peningkatan adalah satu eksekusi per model pada default bawaannya (masing-masing dua untuk Opus 5 dan Sonnet 5, dan titik Fable 5 seperti dijelaskan di atas), dengan eksekusi Opus dan Sonnet pada minggu yang sama dalam satu harness dan organisasi.
4. **BrowseComp:** Wei et al., "BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents," OpenAI, 2025. Angka effort menggunakan potongan 500 soal, satu hingga tiga eksekusi per pengaturan, dijalankan 3 Agustus 2026, dengan titik default menggabungkan dua eksekusi dari 26 hingga 27 Juli 2026. Grafik asuransi biaya menggunakan 10 soal yang terselesaikan secara andal dari irisan 26 soal, 50 eksekusi terdelegasi (1 hingga 2 Agustus 2026) dan 70 eksekusi solo (50 dari 2 hingga 3 Agustus 2026; 20 diarsipkan dari 12 hingga 13 Juli dan 1 Agustus 2026), $6,45 USD dibandingkan dengan $11,99 USD per eksekusi secara ekspektasi; angka terdelegasi memiliki rentang pengukuran sekitar 20%.
5. **Penskalaan arsitektur agen:** Kim et al., "Towards a Science of Scaling Agent Systems," arXiv:2512.08296, 2025. Studi eksternal independen, dikutip hanya untuk arah temuan tentang kapan delegasi tidak menguntungkan, bukan untuk angka apa pun.
6. **DeepWideSearch:** "DeepWideSearch: Benchmarking Depth and Width in Agentic Information Seeking," arXiv:2510.20168, 2025. 220 pertanyaannya mencakup 15 domain, masing-masing menggabungkan pengumpulan banyak baris dengan pengambilan multi-hop; diukur pada set baris tetap milik benchmark, 3 eksekusi per konfigurasi, dijalankan 2 Agustus 2026 (titik tim satu worker dijalankan 26 hingga 27 Juli 2026).
7. **DeepResearch Bench II:** Li et al., "DeepResearch Bench II: Diagnosing Deep Research Agents via Rubrics from Expert Report," arXiv:2601.08536, 2026. 132 tugas risetnya di 22 domain dinilai berdasarkan rubrik biner yang diturunkan dari pakar; diukur pada subset 50 tugas yang distratifikasi di semua tema, satu percobaan per tugas, 3 eksekusi per pengaturan, di [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) dengan alat web search dan fetch milik platform itu sendiri (26 hingga 27 Agustus 2026); dinilai pada 33 tugas yang tidak ditolak oleh konfigurasi mana pun, dengan percobaan yang dihentikan lebih awal oleh classifier keamanan produksi dihapus; biaya adalah yang ditagihkan kepada pelanggan, yaitu permintaan platform ditambah biaya web search. Skor adalah rata-rata setiap model pada basis 33 tugas dengan tugas yang didahului miliknya sendiri dihapus; pada 21 tugas yang bersih di setiap lengan, Claude Fable 5.1 unggul 2 hingga 3 poin atas Claude Fable 5 di setiap tingkat effort dan kedua model datar di seluruh effort. Grafik caching menghitung ulang harga permintaan yang sama dengan setiap token input pada tarif tanpa cache. Claude Opus 4.6 menilai berdasarkan protokol rubrik benchmark; versi aslinya menggunakan penilai yang berbeda, dan penilai Anthropic mungkin lebih menyukai gaya internal. Claude Opus 5 pada effort default-nya dijalankan pada permukaan dan subset yang sama, tiga eksekusi, pada 28 Agustus 2026: 68,8% pada 50 tugas mentah, 70,8% pada basis 33 tugas, dan 71,1% pada set 21 tugas, dengan biaya $6,71 USD per tugas ($23,72 USD tanpa caching); tidak ada percobaannya yang dihentikan lebih awal oleh classifier keamanan, di bawah deployment safeguards yang lebih baru daripada yang digunakan model-model lain.
8. **Penyisiran cacat korpus:** Internal Anthropic, untuk pekerjaan yang lebih besar dari satu jendela konteks: korpus 21,6 juta token dari 14 sumber paket Python publik dengan 130 cacat yang ditanam dan penilaian deterministik; protokol ditetapkan sebelum eksekusi dan ditinjau secara internal; tiga eksekusi per konfigurasi. Setiap konfigurasi dijalankan di Claude Managed Agents. Konfigurasi tim dalam grafik adalah eksekusi di mana koordinator Claude Fable 5.1 menjalankan seluruh penyisiran di dalam platform pada batas terdokumentasinya, yaitu 25 worker Claude Sonnet 5 bersamaan, dijalankan 30 Agustus 2026; tiga episodenya mencetak F1 0,764, 0,825, dan 0,791 setelah audit temuan tambahan (mentah 0,751, 0,821, dan 0,781) dengan biaya $225 USD, $234 USD, dan $283 USD. Konfigurasi solo Claude Sonnet 5 dijalankan 3 hingga 4 Agustus 2026; konfigurasi solo Claude Fable 5.1 dijalankan 24 hingga 25 Agustus 2026, di bawah pengaturan serving peluncuran platform, tiga seed per pengaturan effort, pada build korpus yang sama. Image sandbox membawa salinan terinstal dari sebagian korpus, dan langkah perakitan akhir Claude Fable 5.1 membandingkan dengannya dalam 7 dari 9 episode; penilaian ulang tanpa tambahan tersebut menggeser seed yang terdampak hingga 3 poin. F1 absolut spesifik untuk build korpus ini dan tidak dapat dibandingkan antar benchmark; perbandingan konfigurasi bersifat setara.
9. **GPQA Diamond:** Rein et al., "GPQA: A Graduate-Level Google-Proof Q\&A Benchmark," 2023. Subset Diamond berisi 198 pertanyaan, dua eksekusi per konfigurasi, dijalankan 7 Agustus 2026 (Claude Opus 5.5: 19 September 2026), dinilai oleh model terhadap jawaban referensi, dengan token advisor diukur per permintaan. Pemeriksaan keamanan platform menolak dua pertanyaan biologi pada executor Claude Sonnet 5, dan salah satunya juga pada Claude Opus 5; mengecualikannya tidak mengubah perbandingan apa pun lebih dari satu poin. Angka 92% Claude Opus 5.5 berasal dari dua eksekusi yang menetapkan `fallbacks: "default"` untuk ikut serta dalam [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback), dengan setiap percobaan yang tetap berakhir dengan penolakan dihitung sebagai salah. Dalam setiap eksekusi, pemeriksaan keamanan menandai enam pertanyaan biologi, Claude Opus 5 menjawab lima di antaranya melalui fallback, dan yang keenam tetap berakhir dengan penolakan. Biaya per pertanyaan Opus 5.5 mencakup jawaban fallback tersebut. Tanpa menghitung penolakan sebagai salah, eksekusi ini mencetak skor 93%, karena penilai tetap menetapkan opsi jawaban untuk percobaan yang ditolak, biasanya yang benar. Dengan penolakan dihitung sebagai salah, eksekusi Claude Opus 5 mencetak skor 91% (satu penolakan per eksekusi), begitu pula dua eksekusi Claude Opus 5.5 dengan fallback nonaktif, di mana Opus 5.5 menolak lima atau enam pertanyaan biologi per eksekusi. Claude Haiku 5.5 dan Claude Sonnet 5.5, masing-masing sendiri dan dengan advisor Claude Opus 5.5, menjalankan dua eksekusi per konfigurasi pada 7 Oktober 2026, bersama dua eksekusi Claude Opus 5.5 lainnya, semuanya dengan fallback nonaktif, pada effort default masing-masing model, dan dengan penolakan dihitung sebagai salah. Pemeriksaan keamanan menolak satu pertanyaan biologi per eksekusi pada Claude Haiku 5.5 dan Claude Sonnet 5.5 sendiri, satu dalam dua eksekusi pada Haiku 5.5 dengan advisor, tidak ada pada Sonnet 5.5 dengan advisor, dan enam per eksekusi pada Opus 5.5, yang mencetak skor 91% dengan penolakan tersebut dihitung sebagai salah dan 93,5% pada pertanyaan yang dijawabnya. Konfigurasi advisor menambahkan alat tanpa prompt yang meminta konsultasi, dan tidak ada executor yang memanggil advisor pada pertanyaan mana pun.
10. **DeepSWE:** Datacurve, "DeepSWE: Measuring Frontier Coding Agents on Original, Long-Horizon Engineering Tasks," arXiv:2607.07946, 2026. Set ini memiliki 113 tugas orisinal dalam lima bahasa dengan verifier berbasis program. Pasangan masing-masing dua eksekusi, dijalankan 7 Agustus 2026, dengan token advisor diukur per permintaan, dan menggunakan loop advisor sisi klien alih-alih alat advisor, dengan perhitungan yang identik. Sapuan effort model tunggal adalah eksekusi tunggal yang harganya dihitung dari jumlah token, sebuah aproksimasi yang memperhitungkan cache. Biaya per tugas adalah total eksekusi dibagi 113.
11. **Benchmark agentic-coding internal:** Internal Anthropic: 370 tugas repositori yang dinilai oleh pengujian milik repositori itu sendiri. Angka API diukur dengan batas output 128.000 token, satu eksekusi per konfigurasi: Opus 5 sendiri pada effort default 9 hingga 10 Agustus 2026, dan pada `low` dan `medium` 10 Agustus 2026; Claude Fable 5.1 sendiri pada lima nilai effort yang ditetapkan secara eksplisit 20 Agustus 2026 (grafik menampilkan tiga di antaranya); dan pasangan 24 hingga 25 Agustus 2026. Claude Opus 5.5 sendiri dijalankan pada seluruh 370 tugas, 19 hingga 20 September 2026: pada effort default-nya (`medium`) dan pada `high` dengan lima percobaan per tugas, serta pada `low` dan `xhigh` dengan satu percobaan (369 dari 370 dinilai pada masing-masing, setelah kegagalan pemeriksaan setup). Executor Claude Opus 5.5 pada `high` dengan Claude Fable 5.1 yang telah dirilis sebagai advisor (eksekusi Agustus menggunakan snapshot pra-rilis) menjalankan lima percobaan per tugas pada tanggal yang sama; satu tugas gagal dalam pemeriksaan setup-nya, sehingga 1.845 percobaan dinilai. Grafik advisor membandingkan pasangan tersebut dengan Claude Fable 5.1 yang telah dirilis sendiri pada `high`, default-nya, satu percobaan per tugas pada 7 Oktober 2026: 85,7%, 317 dari 370 tugas. 279 percobaan di mana advisor ditolak karena beban dijalankan ulang, dan percobaan yang konsultasinya mengalami timeout tetap dipertahankan, seperti pada bulan Agustus. Eksekusi Agustus memiliki lima percobaan per tugas untuk pasangan dan kontrol Claude Opus 5 serta satu untuk titik-titik lainnya. Pasangan Agustus rata-rata melakukan sekitar dua konsultasi advisor per percobaan; pasangan Claude Opus 5.5 meminta 1,39 dan menerima 1,35. Biaya dihitung per percobaan. Biaya dihitung sebagaimana organisasi pelanggan diukur: prompt sebelumnya dari setiap permintaan loop agen sebagai cache read dan token barunya sebagai cache write 5 menit, dari catatan penggunaan eksekusi itu sendiri, dan setiap panggilan advisor, yang tidak menggunakan cache, dari token yang tercatat, semuanya pada harga daftar. Angka Claude Code adalah eksekusi tugas yang sama dari 8 hingga 23 Juli 2026, satu eksekusi per konfigurasi, dengan biaya perkiraan.
12. **Benchmark tugas repositori internal (pengukuran batas):** Set internal Anthropic terpisah berisi sekitar 130 tugas repositori, dijalankan 20 Agustus 2026 (Claude Fable 5.1) dan 19 September 2026 (Claude Opus 5.5, pada effort default-nya, `medium`), dengan loop agen API biasa, satu percobaan per tugas. Eksekusi Claude Fable 5.1 adalah 135 tugas per batas dengan effort default yang ditetapkan secara eksplisit: angka 16.384 token merupakan rata-rata dua eksekusi (36,3% pada keduanya); angka 64.000 dan 128.000 adalah eksekusi tunggal (58,5% dan 60,0%). Enam soal memicu penolakan keamanan di setiap eksekusi dan dihitung sebagai kegagalan. Angka 16.384 token Claude Opus 5.5 merupakan rata-rata dua eksekusi (134 dan 135 tugas dinilai), dan angka 64.000 dan 128.000-nya adalah eksekusi tunggal (masing-masing 135 tugas); dua percobaan di setiap eksekusi 16.384 token berakhir dengan penolakan keamanan dan dihitung sebagai kegagalan. Angka batas SWE-bench Pro adalah satu eksekusi Claude Fable 5.1 per batas pada effort default, dijalankan 26 Agustus 2026, pada subset 100 soal yang distratifikasi dari set 482 soal referensi 3, tidak dapat dibandingkan dengan skornya; kedua batas mencetak skor yang sama pada default. Distribusi per giliran dalam grafik berasal dari eksekusi Claude Opus 5.5 dan Claude Fable 5.1 pada 128.000: tidak ada giliran Opus 5.5 yang mencapai batas (yang terpanjang sekitar 61.000 token, dan 0,56% gilirannya melebihi 16.384), dan satu giliran Fable 5.1 mencapai 128.000 (0,46% gilirannya melebihi 16.384).
13. **Chartography:** Surge AI, "Chartography," 2026. Set lengkap 100 pertanyaan yang dirilis, diukur 6 dan 9 Agustus 2026 (Claude Opus 5 sendiri) dan 20 September 2026 (Claude Opus 5.5), dengan implementasi Anthropic di Claude Managed Agents (sandbox cloud standar; konfigurasi advisor menggunakan advisor Managed Agents). Claude Sonnet 4.6 menilai alih-alih juri referensi dan benchmark dijalankan dengan alat, sehingga skor dapat dibandingkan antar konfigurasi di sini tetapi tidak dengan leaderboard yang dipublikasikan. Skor juga tidak dapat dibandingkan dengan hasil Chartography dalam system card Claude Opus 5.5, yang menggunakan penilai berbeda dan dijalankan pada effort `max`. Dua eksekusi per konfigurasi (tiga untuk Claude Opus 5.5), digabungkan; sebaran antar eksekusi mencapai hingga 10 poin. Biaya adalah apa yang ditagihkan kepada pelanggan yang menjalankan agen secara rutin: permintaan pertama setiap grafik membaca prompt sistem bersama dan alat agen dari cache, seperti yang terjadi ketika sesi lain dari agen yang sama berjalan dalam 5 menit sebelumnya. Satu grafik yang dijalankan sendiri biayanya sekitar $0,03 USD lebih mahal dengan Claude Opus 5 atau Claude Opus 5.5 dan sekitar $0,12 USD lebih mahal dengan Claude Fable 5.1. Angka Agustus dihargai ulang dengan cara ini dari catatan penggunaan eksekusi; pengukuran milik organisasi evaluasi sendiri, yang hingga 10 September 2026 menagih cache read Claude Opus 5 dalam blok 8.192 token, melebih-lebihkan biaya Claude Opus 5. Biaya tidak termasuk waktu sandbox, yang menambahkan kurang dari 1% pada eksekusi Agustus. Eksekusi solo Claude Fable 5.1 berasal dari 24 Agustus 2026, di bawah pengaturan serving peluncuran platform, dua eksekusi per pengaturan; enam percobaan mencapai batas sesi 15 menit dan mendapat skor 0, dan dua grafik per eksekusi dijawab oleh Claude Opus 5 setelah penolakan keamanan. Executor effort rendah Claude Opus 5 dengan advisor Claude Fable 5.1 dijalankan dua kali pada 30 Agustus 2026, di bawah pengaturan yang sama (63,0 dan 67,0, rata-rata 65,0, dengan $0,47 USD per grafik; advisor dikonsultasikan pada 88% tugas di setiap eksekusi, dan 4 dari 219 balasannya berasal dari Claude Opus 5, masing-masing setelah filter keamanan produksi menghentikan balasan advisor itu sendiri). Claude Opus 5.5 dijalankan pada `low`, dengan fallback sisi server nonaktif dan classifier keamanan menilai setiap panggilan alat: tiga eksekusi sendiri (70, 68, dan 68) dan tiga dengan advisor Claude Fable 5.1 yang dikonfigurasi (59, 63, dan 63), di mana model tersebut berkonsultasi dengan advisor pada 1 dari 300 tugas. Grafik advisor membandingkan pasangan tersebut dengan Claude Fable 5.1 sendiri pada `high`, default-nya, dijalankan tiga kali pada 7 Oktober 2026, dengan implementasi dan pengaturan platform yang sama seperti eksekusi Claude Opus 5.5: 82, 79, dan 79, rata-rata 80,0. Perbandingan tingkat konsultasi untuk pasangan sebelumnya berasal dari menjalankan ulang konfigurasi yang sama di Messages API dengan set alat container, 10 hingga 11 Agustus 2026.
14. **Evaluasi audit prompt support-desk:** Set 44 tiket dukungan yang disusun Anthropic dengan penilaian deterministik, dijalankan pada awal Agustus 2026 dan dilaporkan pada 8 Agustus 2026, di bawah enam prompt sistem, masing-masing menambahkan ke prompt bersih yang sama satu pola yang umum dalam prompt yang ditulis untuk Claude Opus 4.8 dan Claude Sonnet 4.6. Setiap titik grafik adalah salah satu dari tiga kasus (model lama, model baru pada prompt yang sama, model baru setelah audit) yang dirata-ratakan atas enam prompt dan 44 tiket. Peningkatan akurasi Opus 5 memiliki interval kepercayaan 95% sebesar 3 hingga 8 poin; perbedaan akurasi Sonnet berada dalam batas noise.
15. **Set pertanyaan file data:** Set 25 pertanyaan agregat yang disusun Anthropic atas irisan 1.862 baris dari CSV penjualan minuman keras publik, dengan ground truth yang dihitung oleh pandas dan penilaian exact-match, dijalankan pada Claude Sonnet 5 dan Claude Opus 5 dengan thinking dinonaktifkan (lengan in-context tidak dapat selesai pada default), batas output 4.000 token, dan tanpa caching prompt, tiga eksekusi per konfigurasi, dijalankan 19 Agustus 2026. Lengan file mengunggah CSV melalui Files API dan menggunakan alat `code_execution_20260120`.
16. **Pengukuran durasi cache:** Pekerjaan triase 20 issue dari [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens), dijalankan pada Claude Sonnet 5 pada 23 Agustus 2026, dan pada Claude Opus 5.5 pada 19 dan 20 September 2026, pada effort default-nya (`medium`) dan pada `high`, di Messages API dengan harness yang sama (untuk Claude Opus 5.5, port darinya yang mengirimkan body permintaan yang sama), dengan sel Claude Opus 5.5 menggunakan `max_tokens` yang dinaikkan menjadi 4.096, dengan jeda yang disisipkan sebelum sebagian giliran yang dipilih secara acak (tidak ada, 5%, 10%, dan setiap giliran pada 6 menit pada semua 20 issue di kedua model, ditambah setiap giliran pada 2 menit pada Claude Sonnet 5; jeda 20 menit dan 45 menit pada subset 5 issue di kedua model). Angka keep-alive Claude Opus 5 di bawah berasal dari pekerjaan yang sama pada 23 Agustus 2026, dengan `max_tokens` dinaikkan menjadi 4.096, pada jadwal yang sama kecuali jeda 2 menit dan 45 menit. Tiga eksekusi per sel, biaya dihitung dari field `usage` setiap respons pada harga daftar (untuk Claude Opus 5.5, $4 USD input, $5 USD write 5 menit, $8 USD write 1 jam, $0,20 USD cache read, dan $20 USD output per juta token; Claude Sonnet 5 dijalankan pada organisasi internal Anthropic yang penggunaannya diukur dengan cara yang sama seperti organisasi pelanggan), dengan akurasi terhadap label gold yang sama. Angka Claude Opus 5.5 di halaman ini mencakup kedua tingkat effort. Titik persilangan sekitar 3,3% giliran pada Claude Sonnet 5 dan 3,1% hingga 3,2% pada Claude Opus 5.5: median dari porsi titik impas setiap sesi, dihitung oleh model biaya dari ukuran konteks giliran demi giliran sesi tersebut, atas semua 45 sesi dua puluh issue Claude Sonnet 5 dan 36 sesi dua puluh issue Claude Opus 5.5 pada setiap tingkat effort (setiap jadwal jeda dijalankan pada pekerjaan penuh, di bawah ketiga pengaturan cache, masing-masing tiga eksekusi; sel 5 issue tidak termasuk di dalamnya). Pada sel 5%, pengaturan 5 menit dan 1 jam seri pada Claude Sonnet 5, karena jeda dalam undian tersebut jatuh pada prefix kecil; pada Claude Opus 5.5 keduanya hampir seri. Aturan 1-dari-20 di halaman ini berada di atas titik persilangan yang diukur. Waktu hingga token pertama Claude Opus 5.5 setelah jeda tidak diukur. Anthropic mengukur permintaan keep-alive yang menyegarkan cache 5 menit pada Claude Sonnet 5 dan Claude Opus 5 pada 23 Agustus 2026, dan pada Claude Opus 5.5 dalam eksekusi di atas, selalu dikirim dengan `max_tokens: 1`. Pada Claude Sonnet 5, biayanya 7,7% lebih rendah daripada pengaturan 1 jam dengan 5% giliran dijeda dan kurang lebih sama dengan 10%; pada Claude Opus 5 tidak ada perbedaan yang dapat diukur pada kedua porsi; pada keduanya biayanya lebih tinggi dengan jeda 6 menit atau lebih sebelum setiap giliran. Pada Claude Opus 5.5, biayanya 8% hingga 18% lebih rendah daripada pengaturan 1 jam dengan 5% dan 10% giliran dijeda (sekitar 10% hingga 15% setelah noise antar sesi dihilangkan dengan menagih ulang token milik setiap sesi keep-alive pada harga cache 1 jam), dan lebih tinggi dengan jeda sebelum setiap giliran: 4% hingga 6% lebih tinggi pada 6 menit, 9% hingga 10% pada 20 menit, dan 56% hingga 58% pada 45 menit. Keep-alive menghemat lebih banyak pada Claude Opus 5.5 karena setiap permintaan keep-alive membaca ulang prefix pada harga cache read: 0,05x harga input, dibandingkan 0,1x pada Claude Sonnet 5 dan Claude Opus 5; sesi Claude Opus 5, yang ditagih ulang pada harga Claude Opus 5.5, menunjukkan penghematan yang hampir sama dengan Claude Opus 5.5. Pengujian API pra-peluncuran Anthropic pada Claude Opus 5.5 menunjukkan bahwa permintaan `max_tokens: 0` menulis cache dan permintaan berikutnya membacanya; apakah permintaan semacam itu menyegarkan entri yang sudah ada tidak diukur pada Opus 5.5. Pada Claude Fable 5.1, pada 0,025x, keep-alive lebih murah bahkan dengan jeda sebelum setiap giliran, kecuali pada jeda 45 menit (referensi 19).
17. **Porsi cache read dalam produksi:** Penggunaan Claude API pihak pertama yang diagregasi selama 14 hari yang berakhir 23 Agustus 2026, hanya produk API langsung, organisasi internal Anthropic dikecualikan, tidak ada organisasi yang diidentifikasi. Sebuah organisasi-hari dihitung sebagai loop agen ketika permintaannya membawa definisi alat dan hasil alat, prompt-nya memuat rata-rata 9 atau lebih panggilan alat sebelumnya, caching digunakan, dan organisasi tersebut membuat setidaknya 10 permintaan semacam itu (API tidak memiliki pengidentifikasi percakapan, sehingga ini menjadi pengganti panjang percakapan): 303.003 organisasi-hari di 106.487 organisasi, median porsi cache read 84,2% dari seluruh token input, kuartil atas 91,7%. Label kasus penggunaan (kasus penggunaan yang dideklarasikan organisasi, atau jika tidak, yang diklasifikasikan) mencakup 74% dari organisasi-hari tersebut dan 99% token mereka; organisasi coding menyumbang 87% token input agentik dan membaca median 88,5% (90,9% pada 25 atau lebih panggilan alat sebelumnya), kuartil atas 93,4%, dengan sekitar 72% organisasi-hari coding pada 80% atau lebih; agen dukungan, riset, dan data membaca 84% hingga 85%. Desil teratas organisasi-hari membaca 95,9% atau lebih untuk coding dan 94,2% hingga 94,8% untuk agen dukungan, riset, data, dan lainnya. Pembagian tingkat permintaan pada 25 atau lebih panggilan alat sebelumnya berasal dari sampel enam jam: coding 92% read, 7% write, kurang dari 1% tanpa cache. Organisasi tanpa label, sebagian besar kecil, membaca median 11%. Organisasi-hari tanpa definisi alat membaca median 34,6%. Kueri independen atas jendela waktu yang sama yang merekonstruksi percakapan berisi 10 atau lebih permintaan, alih-alih menilai organisasi-hari, menempatkan median pada 90,2%; perbedaannya terletak pada cakupan, bukan data.
18. **Pengukuran waktu compaction:** Varian panjang agen triase dari [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens), dijalankan 24 Agustus 2026, pada Claude Sonnet 5 dengan cache 5 menit, biaya dari field usage pada harga daftar, lima sesi per lengan: lengan tanpa perubahan pada effort default sepanjang waktu ($0,81 USD per sesi), dan dua lengan yang dimulai pada effort rendah dan membuat dua perubahan pemecah cache yang sama, yaitu peralihan ke effort default dan satu alat tambahan, baik di tengah sesi pada permintaan 12 dan 17 ($0,95 USD) atau bersamaan pada permintaan pertama setelah compaction pertama ($0,75 USD). Lengan keempat berisi enam sesi, dijalankan 25 Agustus 2026, membuat dua perubahan yang sama pada permintaan yang memicu compaction pertama ($0,92 USD per sesi): proses peringkasan permintaan tersebut menulis konteks 81.000 token ke cache alih-alih membacanya, sehingga proses tersebut berbiaya $0,21 USD dibandingkan $0,04 USD untuk proses yang sama di lengan batas. Sesi pertama kali melakukan compaction pada permintaan 21 hingga 25 (16 dari 21 sesi pada permintaan 22), setelah prompt melewati pemicu compaction 80.000 token, dan dua sesi tanpa perubahan melakukan compaction kedua kalinya menjelang akhir. Total lengan batas yang lebih rendah daripada lengan tanpa perubahan mencerminkan permintaan effort rendahnya sebelum perubahan dan compaction kedua tersebut, bukan caching: biaya penulisan ulang kedua lengan berbeda kurang dari $0,01 USD. Lengan tengah sesi membayar $0,23 USD per sesi untuk penulisan ulang cache; perbedaan antara lengan tengah sesi dan lengan batas adalah $0,20 USD dengan interval kepercayaan 95% sebesar $0,11 USD hingga $0,29 USD. Satu sesi tengah sesi berjalan murah ($0,82 USD) setelah modelnya salah memanggil alat pencarian setelah compaction dan mendapatkan hasil kosong; sesi ini disertakan, dan tanpanya lengan tersebut rata-rata $0,98 USD. Akurasi rata-rata 14,2 dari 20 label di setiap lengan 24 Agustus dan 14,7 di lengan 25 Agustus; cache read adalah 91% dari token prompt tanpa perubahan, 85% di tengah sesi, 91% di batas, dan 86% dengan perubahan pada permintaan pemicu.
19. **Pengukuran durasi cache pada Claude Fable 5.1:** Pekerjaan triase 20 issue dan harness yang sama seperti referensi 16, dijalankan 23 Agustus dan 26 Agustus 2026, pada snapshot peluncuran Claude Fable 5.1 dengan harga peluncurannya ($10 USD input, $12,50 USD write 5 menit, $20 USD write 1 jam, $0,25 USD cache read, $50 USD output per juta token), tiga pengaturan per jadwal: cache 5 menit, cache 1 jam, dan cache 5 menit yang dijaga tetap hangat oleh permintaan `max_tokens: 0` pada prefix yang tidak berubah setiap 4 menit, dihitung dari awal permintaan sebelumnya (eksekusi 23 Agustus mengirim permintaan keep-alive dengan `max_tokens: 1`; dalam sel 26 Agustus yang dilaporkan di sini, setiap permintaan keep-alive menyegarkan cache dan tidak menagih output). Jadwal: tanpa jeda, 10% giliran, dan setiap giliran pada 6 menit pada semua 20 issue, serta jeda 45 menit pada subset 5 issue; tiga eksekusi per sel (enam untuk sel keep-alive 26 Agustus dengan jeda 45 menit), biaya dihitung dari field `usage` setiap respons pada harga daftar, akurasi terhadap label gold yang sama (12 hingga 17 label tepat dari 20). Rata-rata per sesi pada 26 Agustus untuk pengaturan 5 menit, 1 jam, dan keep-alive: tanpa jeda $2,42 USD, $3,09 USD, $2,29 USD; 10% dijeda $4,50 USD, $2,96 USD, $2,36 USD; setiap giliran $22,89 USD, $3,01 USD, $2,62 USD; sel 23 Agustus sesuai dalam rentang 6%. Angka 45 menit ($1,68 USD, $0,59 USD, dan $0,71 USD per sesi 5 issue) berasal dari eksekusi ulang yang bersih pada 26 Agustus setelah insiden penagihan cache merusak sel pertama hari itu; eksekusi 23 Agustus memberikan $1,67 USD, $0,58 USD, dan $0,70 USD. Titik persilangan antara pengaturan 5 menit dan 1 jam adalah 3,1% giliran, dengan ukuran yang sama seperti referensi 16.
20. **Terminal-Bench 3:** 74 tugas dari benchmark agen terminal publik, dijalankan di [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) dengan dua alat kustom, yaitu sebuah shell dan editor file yang dijalankan harness evaluasi di container milik setiap tugas, sebagai pengganti alat bawaan platform, dan selebihnya pada pengaturan default platform untuk akun eksternal, dua eksekusi per model pada effort `high`, 27 hingga 28 Agustus 2026. Eksekusi ini menggunakan Terminal-Bench versi 3.0, dan skornya tidak dapat dibandingkan dengan leaderboard Terminal-Bench publik atau dengan hasil Terminal-Bench 4.0 dalam system card Claude Opus 5.5, yang berasal dari eksekusi di Claude Code pada effort `max`. Batas waktu setiap tugas adalah 2,5 kali batas milik benchmark, yang memberi agen antara 75 menit dan 20 jam per tugas (5 jam untuk tugas median), dan setiap tugas mendapat tiga kali memori yang ditentukannya, dari 6 GiB hingga 96 GiB, dengan memori tambahan untuk 12 tugas yang menjalankan layanan pembantu. Agen tidak memiliki akses internet umum: container-nya dapat menjangkau mirror paket internal, daftar pendek situs unduhan termasuk GitHub dan Python Package Index, serta beberapa situs khusus untuk sebagian tugas, dan delapan tugas tidak memiliki akses jaringan sama sekali. Skor adalah tingkat kelulusan mentah atas 148 percobaan per model; eksekusi tunggal berayun 5 hingga 11 poin. Biaya adalah apa yang akan ditagihkan kepada pelanggan pada harga daftar, dihargai ulang permintaan demi permintaan dari catatan penggunaan eksekusi dengan masa hidup cache 5 menit. Claude Opus 4.7 mengakhiri 11 dari 148 percobaannya pada batas output-nya.
21. **DRACO:** Perplexity, "DRACO: a Cross-Domain Benchmark for Deep Research Accuracy, Completeness, and Objectivity," arXiv:2602.11685, 2026. 100 tugas risetnya di 10 domain dinilai terhadap rubrik yang ditulis pakar dengan masing-masing sekitar 40 kriteria berbobot, dan skornya adalah porsi berbobot dari kriteria yang terpenuhi, dari 0 hingga 100. Setiap konfigurasi dijalankan di Claude API dengan Claude Opus 5.5, adaptive thinking default, classifier keamanan produksi aktif, dan `max_tokens` pada 128.000 dengan streaming: agen tunggal pada effort `medium` (default model) dan pada `low`, agen tunggal pada `medium` dengan kalimat dan jam, serta tim pada `medium` dengan dan tanpa keduanya. Tim adalah agen utama yang dapat memulai agen pembantu dari model yang sama melalui sebuah alat, tanpa batas jumlah. Dengan perubahan tersebut, setiap agen memiliki kalimat dan jam dalam bentuk yang dijelaskan di [Tunjukkan waktu yang telah berlalu kepada model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#show-the-model-elapsed-time). Setiap konfigurasi melakukan tiga percobaan pada setiap tugas, dengan batas empat jam per percobaan, dijalankan 24 September 2026, dan semua konfigurasi dari satu set dimulai bersamaan. Agen menggunakan alat search dan fetch yang di-host oleh harness evaluasi atas indeks web Anthropic, serta Python dan shell dalam sandbox tanpa akses jaringan. Alat-alat tersebut menentukan sebagian waktu, dan alat Anda akan berjalan dengan kecepatan berbeda, sehingga halaman ini menyajikan waktu sebagai rasio antar konfigurasi, bukan dalam menit. Waktu adalah waktu wall-clock dari sebuah percobaan, dari permintaan pertamanya hingga akhir permintaan terakhir oleh agen mana pun, termasuk eksekusi alat, dirata-ratakan atas percobaan-percobaan suatu tugas. Angka tugas tipikal adalah median, atas tugas-tugas, dari rasio setiap tugas antara dua konfigurasi. Biaya setiap tugas adalah permintaannya yang dihargai pada harga daftar publik Claude Opus 5.5, dengan caching prompt ditagih sebagaimana untuk pelanggan yang menetapkan cache breakpoint di akhir setiap permintaan dan menggunakan masa hidup cache 5 menit. Setiap permintaan membaca prompt permintaan sebelumnya dari cache dan menulis sisanya. Permintaan pertama sebuah percobaan, dan setiap permintaan yang dimulai lebih dari 5 menit setelah permintaan sebelumnya, menulis seluruh prompt-nya. Biaya hanya mencakup token model; alat harness tidak menambahkan biaya. Semua interval adalah interval bootstrap 95% atas tugas, dan perubahan skor adalah selisih berpasangan atas tugas. Claude Opus 5 menilai jawaban, sehingga Claude Opus 5.5 tidak menilai pekerjaannya sendiri, dan skor setiap jawaban merata-ratakan lima eksekusi penilaian. Classifier keamanan produksi menghentikan tiga percobaan di setiap konfigurasi, semuanya pada satu tugas, dan percobaan tersebut mendapat skor 0; mengecualikan tugas tersebut tidak mengubah temuan apa pun. Eksekusi juga melewatkan "tool use" (penggunaan alat) setiap agen melalui pemeriksaan keamanan internal Anthropic yang tidak dimiliki permintaan pelanggan, yang menambahkan waktu yang tidak terukur pada setiap permintaan di setiap konfigurasi. Pada DRACO, agen tunggal tanpa perubahan membuat sekitar dua kali lebih banyak permintaan, dan tim sekitar sepertiga lebih banyak, sehingga pemeriksaan tersebut kemungkinan membuat penghematan waktu DRACO terlihat sedikit lebih besar.
22. **HLE:** Phan et al., "Humanity's Last Exam," arXiv:2501.14249, 2025. Pertanyaan yang ditulis pakar dengan jawaban pasti, dinilai terhadap jawaban referensi. Diukur pada 500 pertanyaan pertama dari rilis 10 September 2025, termasuk gambar, dengan sumber milik benchmark diblokir dari pencarian, dan penyiapan yang sama seperti referensi 21. Setiap konfigurasi melakukan tiga percobaan pada setiap pertanyaan, dijalankan 24 September 2026. Claude Opus 5 membandingkan setiap jawaban dengan jawaban referensi, menggunakan prompt juri yang dipublikasikan benchmark, dan mayoritas dari tiga penilaian yang dihitung. Skor mencakup 493 pertanyaan di setiap konfigurasi. Untuk lima dari sisanya, permintaan penilaian melebihi batas 1M token juri, dan dua lainnya dikecualikan karena eksekusi agen tunggal tanpa perubahan berhenti sebelum tiga percobaannya pada pertanyaan tersebut selesai. Rasio waktu dan biaya mencakup 492 pertanyaan untuk agen tunggal dan 491 untuk tim, karena satu atau dua pertanyaan tidak memiliki data waktu. Classifier keamanan produksi menghentikan 3% hingga 4% percobaan setiap konfigurasi, dan percobaan tersebut mendapat skor 0; mengecualikannya tidak mengubah temuan apa pun. Dengan penilai kedua, Claude Opus 4.6, skor agen tunggal dengan perubahan 1,9 poin lebih rendah (interval 95% 0,2 hingga 3,7 lebih rendah), sedangkan juri Claude Opus 5 tidak menunjukkan perubahan yang jelas.
23. **Set fisika:** Set internal berisi 70 soal fisika tingkat riset, diadaptasi dari benchmark publik CritPt: Zhu et al., "Probing the Critical Point (CritPt) of AI Reasoning: a Frontier Physics Research Benchmark," arXiv:2509.26574, 2025. Peninjau pakar mengoreksi pernyataan soal. Claude Opus 4.6 menilai setiap jawaban dengan nilai parsial, menggunakan prompt penilaian set tersebut, terhadap solusi referensi pakar yang tidak publik, sehingga skor tidak dapat dibandingkan dengan hasil yang dipublikasikan. Skor adalah nilai rata-rata atas percobaan-percobaan suatu soal, dirata-ratakan atas soal, dalam poin dari 100. Diukur pada semua 70 soal, empat percobaan per soal, dijalankan 24 September 2026. Setiap agen memiliki alat Python, shell, dan editor file dalam container sandbox tanpa akses jaringan, dan tanpa alat search atau fetch. Tidak ada classifier keamanan yang menghentikan percobaan pada set fisika. Selebihnya, penyiapannya sama dengan referensi 21. Seluruh penghematan waktu rata-rata agen tunggal berasal dari satu soal, di mana agen tanpa perubahan menjalankan kode selama sekitar setengah jam per percobaan; tanpa soal tersebut, waktu rata-ratanya kurang lebih sama dengan dan tanpa perubahan.

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

  <Card title="Task budget" icon="clock" href="https://platform.claude.com/docs/id/build-with-claude/task-budgets">
    Berikan loop agen hitung mundur token yang mereka atur sendiri.
  </Card>

  <Card title="Session budget" icon="coins" href="https://platform.claude.com/docs/id/managed-agents/budgets">
    Tetapkan batas dolar yang tegas pada sesi Managed Agents.
  </Card>

  <Card title="Harga" icon="dollar-sign" href="https://platform.claude.com/docs/id/about-claude/pricing">
    Lihat harga per token terkini untuk setiap model Claude.
  </Card>

  <Card title="Cookbook: optimasi biaya pada Claude API" icon="book" href="https://platform.claude.com/cookbook/cost-optimization-cost-optimization">
    Terapkan tuas-tuas ini satu per satu pada agen yang berfungsi dalam notebook yang dapat dijalankan, dengan biaya per tugas setelah setiap langkah.
  </Card>

  <Card title="Webinar: Membangun di Claude Platform" icon="play" href="https://www.anthropic.com/webinars/building-on-the-claude-platform-claude-fable-5-and-model-orchestration-patterns">
    Tonton panduan langkah demi langkah tentang pola advisor dan orchestrator.
  </Card>
</CardGroup>
