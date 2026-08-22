---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: f3dbfe25108008b1d4bf898779e2f343a3590bf8c3f2bcf38dfc369376e6487b
---

---
title: Mengoptimalkan biaya dan kecerdasan
url: https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence
description: Seimbangkan biaya dan kecerdasan di Claude Platform, dengan hasil terukur untuk caching prompt, effort, pilihan model, anggaran, dan strategi multi-model.
---

Ketika sebuah beban kerja berpindah dari prototipe ke produksi, biaya menjadi batasan desain kelas utama. Model yang paling mumpuni bisa terlalu mahal dalam skala besar, dan model yang paling murah bisa kurang memadai dalam hal kualitas. Mengelola biaya dengan baik berarti memahami bagaimana setiap tuas biaya memengaruhi kualitas output, karena sebagian tuas mengorbankan kualitas dan sebagian tidak. Claude Platform memberi Anda kendali langsung atas tradeoff tersebut. Anda memilih model, tingkat effort, dan arsitektur untuk setiap permintaan, yang memungkinkan Anda menempatkan beban kerja hampir di mana saja pada batas biaya-terhadap-kecerdasan.

Tuas-tuas ini terdiri dari dua jenis:

* **Kemenangan gratis** memangkas pengeluaran tanpa menyentuh kualitas: "prompt caching" (caching prompt), kebersihan token, audit prompt terhadap model yang Anda jalankan, [pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing) dengan diskon 50% untuk pekerjaan yang bisa menunggu hingga 24 jam, dan [batas pengeluaran workspace](https://platform.claude.com/docs/id/api/rate-limits#setting-lower-limits-for-workspaces) sebagai pengaman terakhir.
* **Tradeoff** menukar biaya dengan kecerdasan: pilihan model, effort, batas output dan anggaran tugas, serta arsitektur multi-model.

Setiap tuas disertai hasil terukur dan aturan kapan tuas tersebut menguntungkan. Dalam pengukuran Anthropic, caching prompt adalah tuas terbesar dengan selisih yang jauh: caching memangkas biaya loop agen dengan faktor 2,5 hingga 3,7 pada benchmark panduan ini dan memangkas tagihan agen triase kecil sebesar 83%, atau 88% dengan tambahan pemangkasan input. Tuas multi-model lebih sempit; model kedua menguntungkan dalam dua bentuk, yaitu advisor dan orchestrator.

## Mulai di sini

Cocokkan situasi Anda dengan salah satu baris.

| Situasi Anda                                                 | Lakukan ini                                                                                                                                                                                                                     | Di mana                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Beban kerja apa pun, model apa pun                           | Aktifkan caching prompt dan pangkas token yang tidak diperlukan; keduanya gratis                                                                                                                                                | [Cache konteks berulang](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#cache-repeated-context) · [Pangkas token](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens) |
| Biaya terlalu tinggi; kualitas baik-baik saja                | Turunkan effort secara bertahap pada model Anda saat ini                                                                                                                                                                        | [Sesuaikan effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort)                                                                                                                                                                |
| Anda sedang memilih atau berganti model                      | Bandingkan berdasarkan biaya per tugas selesai, bukan per token                                                                                                                                                                 | [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task)                                                                                                                                            |
| Kualitas belum cukup baik                                    | Jika Anda menurunkan effort, kembalikan; jika tidak, coba tingkat berikutnya di atas dengan effort `low`                                                                                                                        | [Sesuaikan effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort) · [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task)             |
| Percobaan berakhir dengan `stop_reason: max_tokens`          | Naikkan `max_tokens`; 64.000 mencakup setiap giliran yang diukur dan tidak menambah biaya per tugas yang terselesaikan                                                                                                          | [Tetapkan anggaran](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                                                                                                                                               |
| Anda dapat memeriksa output (tes, verifier)                  | Jalankan semuanya dengan effort rendah dan jalankan ulang kegagalan pada default (`high`); pada benchmark coding yang diukur, tingkat kelulusan bertahan dengan sekitar setengah biaya                                          | [Jalankan ulang kegagalan](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#re-run-failures-at-higher-effort)                                                                                                                                   |
| Loop agen dengan beberapa run yang sangat mahal              | Tetapkan anggaran tugas (beta; saat ini tidak tersedia di Claude Sonnet 5), anggaran sesi Claude Managed Agents, dan batas pengeluaran workspace                                                                                | [Tetapkan anggaran](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                                                                                                                                               |
| Model berbiaya lebih rendah hanya macet pada keputusan sulit | Tambahkan advisor frontier. Ini menguntungkan ketika harganya jauh di atas executor dan benar-benar dikonsultasikan, jadi pertama-tama hitung harga model advisor sendirian dengan effort rendah dan ukur tingkat konsultasinya | [Strategi advisor](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#advisor-strategy-escalate-hard-decisions)                                                                                                                                   |
| Pekerjaan melebihi satu jendela konteks                      | Delegasikan partisi ke worker yang lebih murah                                                                                                                                                                                  | [Strategi orchestrator](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#orchestrator-strategy-delegate-bulk-work)                                                                                                                              |

Hasil-hasil ini bersifat internal Anthropic ([Benchmark yang dirujuk](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs)) dan bersifat arahan, bukan jaminan, jadi ukurlah pada beban kerja Anda sendiri dengan [metode empat langkah](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#measure-on-your-own-workload).

## Pangkas pengeluaran tanpa kehilangan kualitas

Caching prompt, kebersihan token, pemrosesan batch, dan audit prompt terhadap model Anda saat ini semuanya menurunkan apa yang Anda bayar tanpa menurunkan kualitas output. Dua catatan berlaku: pemrosesan batch menukar latensi dengan diskonnya, dan context editing, sebuah tuas kebersihan token, berbiaya lebih besar daripada yang dihematnya pada run yang diukur di bagian ini.

### Cache konteks berulang

Aktifkan [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) sebelum tuas lainnya, karena setiap giliran tugas agentik mengirim ulang seluruh percakapan yang terus bertambah: "system prompt" (prompt sistem), definisi alat, dan setiap giliran sebelumnya. Tugas 40 giliran mengirim giliran pertamanya 40 kali, sehingga biaya tugas tumbuh kira-kira sebanding dengan kuadrat jumlah giliran. Caching tidak menghentikan pengiriman ulang, tetapi setiap pengiriman ulang berbiaya sekitar sepersepuluhnya dan diproses lebih cepat: prefiks ditagih dengan [tarif cache-read](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#pricing), sepersepuluh dari harga input, dan setiap giliran membayar tarif cache-write 1,25x hanya untuk bagian yang baru.

Di seluruh run terukur Anthropic, cache read secara rutin merupakan komponen tunggal terbesar dari biaya tugas, menjadikan caching lebih berharga daripada sebagian besar keputusan pilihan model. Anthropic menghitung harga run WideSearch[1](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dan DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dengan dan tanpa caching:

![Grafik dumbbell, biaya per masalah dengan dan tanpa caching prompt: biaya setiap konfigurasi turun dengan faktor 2,5 hingga 3,7](https://platform.claude.com/docs/images/cost-intel-caching.png)

Masa hidup default cache adalah 5 menit dan giliran-giliran loop agen hanya berjarak beberapa detik, sehingga diskon berlaku untuk sebagian besar token pada setiap giliran; run yang digambarkan mencapai hit rate 81% hingga 90%. Penghematannya bervariasi menurut kedalaman episode, karena loop yang lebih pendek membaca ulang lebih sedikit, tetapi caching tetap menjadi tuas tunggal terbesar pada setiap model dan benchmark yang diukur.

Jika loop Anda menunggu manusia di antara giliran, gunakan [durasi cache 1 jam](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration). Biaya penulisannya lebih mahal (2x harga input, bukan 1,25x) tetapi terbayar pada miss pertama yang dicegah, karena sebuah miss mengirim ulang seluruh prefiks dengan harga penuh dan menulisnya lagi.

Penyiapannya hanya memerlukan sedikit pekerjaan. [Caching otomatis](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#automatic-caching) menempatkan breakpoint untuk Anda; jika tidak, [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill) yang disertakan dengan Claude Code dapat menambahkan caching ke integrasi yang sudah ada dari satu prompt. Kutipan berikut menunjukkan skill tersebut menambahkannya ke harness yang menghasilkan pengukuran ini:

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

Tiga pengaturan dapat merusak cache Anda selama sebuah tugas. Mengubah [`effort`](https://platform.claude.com/docs/id/build-with-claude/effort) di antara permintaan membatalkan prefiks yang di-cache, jadi ubahlah hanya di tempat Anda memang akan melakukan cache ulang, seperti pada batas [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction). Mengubah [anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) di tengah jalan melakukan hal yang sama, jadi tetapkan sekali, pada permintaan pertama. Setiap pass [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing#context-editing-and-prompt-caching) membatalkan prefiks dari titik yang dibersihkannya dan permintaan berikutnya membayar untuk melakukan cache ulang semua yang ada setelahnya, jadi bersihkan dalam beberapa batch besar daripada banyak batch kecil. Lakukan ketiga perubahan tersebut pada jeda alami, lalu pastikan cache read tidak turun; jika turun, [diagnostik cache](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics) menunjukkan di mana prefiks menyimpang.

### Pangkas token input dan konteks

Sebagian besar permintaan agen membawa token yang tidak pernah memengaruhi jawaban. Memangkasnya tidak mengorbankan kualitas output sama sekali, meskipun tidak setiap tuas di sini menghemat uang saat diukur. Dua tempat untuk diperiksa:

* **Pemangkasan input.** [Dynamic filtering](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool#dynamic-filtering) pada alat web fetch menjauhkan boilerplate dari halaman yang diambil, [pengubahan ukuran gambar](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size) menyesuaikan ukuran input vision, dan [tool search dengan deferred loading](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool) memuat definisi alat hanya saat diperlukan. [Programmatic tool calling](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) memungkinkan Claude menjalankan beberapa panggilan alat dari kode sehingga hanya hasil yang difilter yang masuk ke konteks; dokumentasinya melaporkan 24% lebih sedikit token input pada benchmark pencarian agentik, dengan skor yang lebih tinggi. [Kelola konteks alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/manage-tool-context) membandingkan tool search, programmatic tool calling, caching prompt, dan context editing.
* **Siklus hidup konteks.** [Context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) membersihkan hasil alat yang sudah usang, dan [compaction otomatis](https://platform.claude.com/docs/id/build-with-claude/compaction) dengan ambang batasnya menghentikan loop panjang agar tidak membawa seluruh riwayatnya ke depan.

Tuas-tuas ini berinteraksi dengan cache dan satu sama lain, jadi nilailah berdasarkan efek bersihnya, dan gunakan [diagnostik cache](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics) untuk memastikan prefiks yang di-cache bertahan dari setiap perubahan. Anthropic mengaktifkan tuas-tuas tersebut satu per satu untuk agen triase isu yang mengerjakan 20 laporan bug nyata dengan tangkapan layar dari repositori publik (dan, untuk panel kedua, varian yang lebih panjang dari pekerjaan yang sama):

![Dua grafik batang biaya run triase: caching memangkas 83%, pemangkasan mencapai 88%; pada run yang lebih panjang, compaction memangkas 38% lagi](https://platform.claude.com/docs/images/cost-intel-hygiene.png)

Caching melakukan hampir semua pekerjaan, dan pemangkasan membawa totalnya ke 88%. Setiap batang adalah satu run, jadi perbedaan $0,10 adalah noise; perbedaan yang ditampilkan di sini bukan. Compaction membutuhkan sesi yang cukup panjang untuk memicunya: run 20 isu tidak pernah mencapai batas bawah 50.000 token setelah inputnya dipangkas, tetapi pada varian yang lebih panjang di panel kedua, compaction terpicu sekali dan memangkas tagihan 38% lagi.

Context editing adalah satu-satunya tuas di sini yang tidak gratis. Setiap pass pembersihan menulis ulang percakapan yang di-cache, yang bekerja melawan caching prompt; pada run ini, context editing berbiaya lebih besar daripada yang dihematnya. Gunakan untuk memberi ruang di jendela konteks, dan [bersihkan dalam beberapa batch besar](https://platform.claude.com/docs/id/build-with-claude/context-editing#context-editing-and-prompt-caching).

### Batch pekerjaan yang bisa menunggu

[Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing) memberi diskon 50% untuk setiap token permintaan, termasuk yang di-cache, dengan imbalan hasil yang tiba kapan saja dalam 24 jam. Arahkan setiap permintaan yang tidak ditunggu siapa pun melalui batch, dan pertahankan jalur interaktif untuk sisanya. Batching adalah tuas gratis terbesar kedua setelah caching untuk pekerjaan agen tanpa pengawasan: run evaluasi, backfill, dan pekerjaan terjadwal seperti run berulang dari agen triase isu pada [pengukuran pemangkasan token](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens). Batching dapat digabungkan dengan semua hal di halaman ini kecuali interaktivitas, tetapi tidak tersedia untuk sesi Claude Managed Agents, yang memang dirancang interaktif (lihat [harga Claude Managed Agents](https://platform.claude.com/docs/id/about-claude/pricing#claude-managed-agents-pricing)).

### Audit prompt terhadap model saat ini

Setiap generasi model merespons prompt secara berbeda, sehingga sebuah prompt mengakumulasi teks yang ditulis untuk model yang tidak lagi Anda gunakan. Kasus yang umum adalah instruksi yang terlalu spesifik yang ditambahkan untuk mengompensasi model lama: "verifikasi dua kali," "bersikaplah seteliti mungkin," prosedur langkah demi langkah yang wajib, atau scratchpad penalaran buatan sendiri. Model yang lebih baru mengikuti semua ini secara harfiah, menghasilkan putaran alat tambahan dan tulisan tambahan, sehingga tagihan naik tanpa peningkatan akurasi. Mengaudit prompt terhadap model yang Anda jalankan sekarang, dan lagi setiap kali Anda berganti model, adalah kemenangan gratis.

Auditnya hanya satu perintah. [Skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill) yang disertakan dengan Claude Code memiliki perintah `prompt-audit` yang membaca prompt dan kode permintaan sebuah proyek dan melaporkan apa yang ditulis untuk model yang berbeda. Kutipan singkat ini menunjukkannya dijalankan terhadap prompt support-desk dan kode permintaan yang berisi pola-pola tersebut:

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

Perintah tersebut kemudian mengusulkan editnya sebagai diff (satu hunk ditampilkan) dan mencantumkan apa yang sengaja dibiarkannya: jangka waktu refund, persyaratan nada, dan standar kualitas. Anda meninjau sebuah patch, bukan penulisan ulang.

Efeknya terukur. Pada evaluasi support-desk[14](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), prompt yang ditulis untuk Claude Opus 4.8 berbiaya 36% lebih mahal per tiket pada Claude Opus 5 tanpa perubahan akurasi. Menjalankan audit pada prompt yang sama membuat Opus 5 lebih murah daripada versi yang tidak diaudit (sebesar 14%) dan lebih akurat (97% tiket, naik dari 92%, peningkatan di luar noise). Pada migrasi Claude Sonnet 4.6 ke Claude Sonnet 5, audit memangkas 14% dengan akurasi yang sama:

![Grafik sebar, evaluasi support-desk: prompt lama berbiaya lebih mahal pada model baru; setelah diaudit, lebih murah dan sama akuratnya](https://platform.claude.com/docs/images/cost-intel-prompt-audit.png)

Kedua jenis teks usang memiliki biaya yang berbeda. Instruksi yang diikuti model baru terlalu harfiah memakan uang: menghapus "verifikasi dua kali" memangkas biaya per tiket Opus 5 sepertiganya, dan menghapus "bersikaplah seteliti mungkin" hampir sebanyak itu. Teks yang tidak lagi cocok dengan model justru memakan akurasi: pengaturan thinking yang sudah dipensiunkan, aturan yang saling bertentangan, dan scratchpad buatan sendiri yang berkonflik dengan thinking model itu sendiri masing-masing memulihkan 7 hingga 11 poin pada Opus 5 ketika dihapus:

![Grafik batang per pola lama: instruksi yang terlalu dipatuhi memakan uang; pengaturan rusak dan aturan yang bertentangan memakan akurasi](https://platform.claude.com/docs/images/cost-intel-prompt-audit-patterns.png)

Pola yang sama muncul dalam deskripsi alat dan skill, dan layak dihapus di sana juga.

## Tukar biaya dengan kecerdasan

Tuas-tuas ini menentukan di mana satu model berada di antara biaya dan kecerdasan: pilihan model, effort, menjalankan ulang kegagalan pada pengaturan yang lebih tinggi, serta anggaran dan batas tempat model bekerja. Mulailah dengan sweep effort pada model Anda saat ini ([Sesuaikan effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort)). Dari biaya dan kemampuan terendah ke tertinggi, model saat ini adalah Claude Haiku 4.5, Claude Sonnet 5, Claude Opus 5, dan Claude Fable 5 (model frontier); [Ikhtisar model](https://platform.claude.com/docs/id/about-claude/models/overview) memuat jajaran lengkap dan harganya.

### Bandingkan model berdasarkan biaya per tugas

Daftar harga ditulis per token, dan per token model frontier terlihat mahal: harga per token Claude Fable 5 beberapa kali lipat harga Claude Sonnet 5. Namun, Anda membayar untuk tugas yang selesai, jadi bandingkan model berdasarkan biaya per tugas selesai. Model yang lebih mumpuni menyelesaikan tugas dengan lebih sedikit pekerjaan: lebih sedikit giliran, lebih sedikit pencarian, lebih sedikit membaca ulang konteksnya sendiri, dan lebih sedikit mundur. Premi per token secara rutin tertutupi oleh melakukan lebih sedikit dari segalanya.

Anthropic mengukur ini secara langsung pada DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), benchmark laporan riset yang cukup sulit untuk membedakan model-model tersebut:

![Grafik sebar, DeepResearch Bench II: Claude Fable 5 dengan effort low berbiaya lebih rendah per tugas dan mendapat skor lebih tinggi daripada Claude Sonnet 5](https://platform.claude.com/docs/images/cost-intel-cost-per-task.png)

Model frontier dengan effort `low` lebih akurat dan sekitar 10% lebih murah per tugas daripada model tingkat menengah, meskipun ada selisih per token. Namun, model frontier tidak selalu menang. Pada subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) halaman ini, yang sebagian besar sudah dijenuhkan oleh kedua model dan yang skornya tidak dapat dibandingkan dengan leaderboard publik, Claude Opus 5 sendirian menyamai Claude Fable 5 sendirian (91,7% dibandingkan 91,3%, di dalam noise antar-run) dengan sekitar 60% biayanya. Pada pekerjaan yang lebih sulit, seperti tugas DeepResearch Bench II, keunggulan Fable muncul kembali.

Untuk sebagian besar beban kerja agen, mulailah dengan Claude Opus 5: per token biayanya setengah dari Fable 5 dan 2,5 kali Sonnet 5, dan pada subset coding tersebut Opus 5 menyamai akurasi Fable. Di ujung lain, Claude Haiku 4.5 menjawab pertanyaan GPQA Diamond[9](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dengan sekitar sepersepuluh biaya per pertanyaan Opus 5, dengan akurasi 63% dibandingkan 92% untuk Opus, dan tertinggal jauh lebih banyak pada tugas coding panjang. Haiku cocok untuk pekerjaan bervolume tinggi dengan output yang dapat diperiksa, bukan loop agentik panjang.

Peringkatnya berbalik menurut beban kerja, dan tidak ada daftar harga yang memberi tahu Anda ke arah mana. Hitung harga setiap kandidat dalam biaya per tugas selesai pada lalu lintas Anda sendiri, termasuk Claude Opus 5 dan model frontier dengan effort yang dikurangi.

Hitung harga ekor beban kerja Anda, bukan mediannya: bandingkan model pada sepersepuluh tugas tersulit Anda, bukan tugas yang tipikal. Pada tugas tipikal setiap model terlihat serupa dan yang termurah terlihat terbaik, tetapi tagihan ditentukan oleh tugas-tugas yang gagal dikerjakan model yang lebih murah, karena tugas yang gagal tetap menagih tokennya, lalu percobaan ulangnya, lalu apa pun biaya kegagalan tersebut di hilir. Ekor juga merupakan tempat uang mengalir bahkan ketika tidak ada yang gagal. Pada run WideSearch[1](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) 20 masalah, dua masalah menanggung 43% pengeluaran:

![Grafik batang 20 masalah WideSearch yang diurutkan berdasarkan biaya: dua teratas menanggung 43% pengeluaran dan separuh termurah 10%](https://platform.claude.com/docs/images/cost-intel-tail.png)

[Strategi multi-model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#combine-models) ada untuk membelanjakan kecerdasan frontier pada ekor tersebut tanpa membayar tarif frontier untuk sisanya.

### Sesuaikan effort

Effort adalah cara paling langsung untuk menyesuaikan model dengan tugas Anda. Parameter `effort` mengatur seberapa banyak thinking, pemanggilan alat, dan verifikasi diri yang dilakukan model, dan default-nya (`high`) cocok untuk tugas yang menuntut. Biaya berskala dengan semua aktivitas itu; akurasi hanya berskala dengan bagian yang dibutuhkan tugas Anda. Di bawah batas atas model, tingkat effort tertinggi membayar kedalaman yang tidak pernah digunakan tugas.

Pada benchmark riset dan pekerjaan pengetahuan (WideSearch[1](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), DeepWideSearch[6](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), BrowseComp[4](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), dan GDPval[2](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), semuanya dengan Claude Fable 5), kurva akurasi terhadap biaya hampir datar: `low` mengorbankan 1 hingga 3 poin untuk potongan sepertiga hingga setengah biaya per tugas, `medium` menyamai akurasi default dengan 70% hingga 85% biayanya, dan default tidak membeli apa pun yang terukur di atas `medium` pada keempatnya. Pada DeepWideSearch, `low` juga menyamai orchestrator dengan worker Claude Sonnet 5 dengan biaya 20% lebih rendah: menurunkan effort mengalahkan perubahan arsitektur.

Pengaturan yang lebih rendah juga lebih cepat, yang penting ketika latensi menjadi batasannya. Pada run ini, `low` memakan 4,5 menit per masalah pada DeepWideSearch, dibandingkan 7,9 menit pada default. Pada [benchmark korpus](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#orchestrator-strategy-delegate-bulk-work), yang inputnya tidak muat dalam satu jendela konteks mana pun, Fable 5 memakan 7,9, 9,1, dan 11,4 jam per episode pada `low`, `medium`, dan default.

Coding jangka panjang adalah bentuk lainnya. Pada SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), Claude Opus 5 mengorbankan sekitar 2 poin pada `medium` untuk setengah biaya dan sekitar 8 poin pada `low` untuk seperempatnya: tradeoff yang nyata, yang diubah kembali menjadi penghematan oleh [menjalankan ulang kegagalan pada effort lebih tinggi](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#re-run-failures-at-higher-effort). Grafik ini memplot akurasi terhadap biaya untuk benchmark riset dan pekerjaan pengetahuan serta untuk SWE-bench Pro:

![Grafik garis akurasi terhadap biaya menurut effort pada lima benchmark: hampir datar pada empat tugas riset, curam pada SWE-bench Pro](https://platform.claude.com/docs/images/cost-intel-effort-sweep.png)

Dua konsekuensi mengikuti. Pertama, gambarlah kurva ini untuk beban kerja Anda sendiri sebelum menambahkan model kedua: dalam pengukuran internal ini, konfigurasi multi-model yang terlihat lebih murah daripada model tunggal default berbiaya lebih mahal daripada model yang sama dengan effort lebih rendah. Kedua, kurva ini adalah baseline model tunggal yang harus dikalahkan oleh strategi multi-model apa pun, sehingga [langkah 2 dari mengukur pada beban kerja Anda sendiri](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#measure-on-your-own-workload) membuat baseline di seluruh tingkat effort.

Effort yang lebih rendah memang mengorbankan akurasi pada beban kerja yang mencapai batas atas model, di mana akurasi benar-benar berskala dengan kedalaman penalaran. Pada DeepResearch Bench II[7](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), di mana setiap laporan menghargai penalaran mendalam per subtopik, setiap langkah effort membeli sekitar 2,4 poin skor rubrik; tidak ada pemangkasan biaya gratis pada kurva itu:

![Grafik garis skor rubrik terhadap biaya per tugas pada DeepResearch Bench II: setiap langkah effort membeli sekitar 2,4 poin](https://platform.claude.com/docs/images/cost-intel-effort-limit.png)

Deskripsi tugas saja tidak mengungkapkan jenis beban kerja mana yang Anda miliki, jadi lakukan sweep dua atau tiga tingkat effort pada sampel lalu lintas Anda sendiri dan baca jawabannya dari kurva. Uji setiap tingkat dalam sesi terpisah: mengubah effort di tengah sesi membatalkan cache (lihat [Cache konteks berulang](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#cache-repeated-context)) dan mendistorsi perbandingan. Untuk detail parameter, lihat [Effort](https://platform.claude.com/docs/id/build-with-claude/effort).

### Jalankan ulang kegagalan pada effort lebih tinggi

Ketika hasil sebuah tugas dapat diperiksa, kebijakan termurah pada kurva effort bukanlah pengaturan tetap: jalankan setiap tugas pada pengaturan rendah dan jalankan ulang hanya kegagalannya pada pengaturan yang lebih tinggi.

Anthropic menghitung kebijakan ini tugas demi tugas dari run effort pada subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) di [Sesuaikan effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort). Dengan Claude Opus 5 pada `low`, 16% tugas gagal; dengan tugas-tugas tersebut dijalankan ulang pada default, sekitar 93% lulus dengan biaya sekitar $0,70 masing-masing, dibandingkan 91,7% dengan $1,39 jika menjalankan semuanya pada default: tingkat kelulusan yang sama dengan setengah biaya, termasuk percobaan murah yang gagal. Memulai dari `medium` justru menyelesaikan sekitar 94% dengan sekitar $0,95. Sebagian besar peningkatan kecil itu berasal dari percobaan kedua (menjalankan ulang kegagalan default sendiri pada default menghasilkan skor yang kira-kira sama, dengan biaya lebih besar), jadi gunakan kebijakan ini untuk penghematannya, bukan peningkatannya:

![Grafik, SWE-bench Pro: menjalankan low atau medium dan menjalankan ulang kegagalan pada default mengalahkan setiap pengaturan effort tetap dalam hal biaya](https://platform.claude.com/docs/images/cost-intel-escalation.png)

Dua syarat berlaku. Pertama, Anda membutuhkan sinyal kegagalan (di sini, tes benchmark itu sendiri); pemeriksa yang meloloskan pekerjaan buruk membiarkan kegagalan tersebut lewat. Kedua, setiap kegagalan pass pertama memakan waktu nyata setara dua run, sehingga penghematannya dibayar dengan latensi pada kegagalan.

### Tetapkan anggaran dan batas output

Sebagian besar run tugas agentik murah, tetapi sebagian kecil menghabiskan berkali-kali lipat biaya median untuk pencarian, verifikasi ulang, dan pengujian berlebihan. [Anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) menargetkan ekor tersebut. Model melihat hitung mundur token langsung untuk seluruh tugas dan mengatur dirinya sendiri, memangkas pencarian bernilai rendah, melewatkan verifikasi yang berlebihan, dan menyelesaikan pekerjaan alih-alih berputar-putar.

Anthropic mengukur tingkat kelulusan dan biaya per tugas pada SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) dengan Claude Fable 5 seiring anggaran diperketat:

![Grafik garis pada SWE-bench Pro: pass@1 turun perlahan seiring anggaran tugas diperketat sementara biaya per tugas turun hampir setengahnya](https://platform.claude.com/docs/images/cost-intel-budget-pareto.png)

Anggaran yang longgar mengorbankan sekitar 2,7 poin tingkat kelulusan untuk penghematan biaya 18%, dan anggaran terketat yang diizinkan mengorbankan 4,4 poin untuk penghematan 47%. Anggaran membeli efisiensi di sini, bukan akurasi.

Tiga kontrol melakukan tiga pekerjaan berbeda. Anggaran tugas menghemat uang, karena model melihatnya. `max_tokens` adalah batas pengaman yang tidak menghemat apa pun. Pada Claude Managed Agents, anggaran sesi adalah penghentian keras dalam dolar di balik keduanya. Tetapkan ketiganya: anggaran tugas, `max_tokens` yang tinggi, dan batas sesi untuk run yang tidak pernah Anda inginkan muncul di tagihan, dengan [batas pengeluaran workspace](https://platform.claude.com/docs/id/api/rate-limits#setting-lower-limits-for-workspaces) sebagai pengaman terakhir.

* **Anggaran tugas** berstatus beta (header beta `task-budgets-2026-03-13`) pada Claude Opus 5, Claude Fable 5, Claude Opus 4.8, dan Claude Opus 4.7, tetapi tidak pada Claude Sonnet 5; periksa [tabel dukungan](https://platform.claude.com/docs/id/build-with-claude/task-budgets#feature-support) terlebih dahulu. Mulailah di dekat penggunaan token persentil ke-90 loop Anda, lalu perketat ([Memilih anggaran](https://platform.claude.com/docs/id/build-with-claude/task-budgets#choosing-a-budget) menunjukkan cara mengumpulkan distribusi tersebut). Anggaran di bawah batas bawah 20.000 token saat ini ditolak, dan anggaran yang sangat ketat dapat menghasilkan perilaku mirip penolakan. Tetapkan anggaran sekali, pada permintaan pertama, karena perubahan di tengah tugas [membatalkan cache](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#cache-repeated-context). Anggaran bersifat anjuran, mengarahkan model alih-alih menghentikannya, jadi verifikasi kepatuhannya pada beban kerja Anda.
* **`max_tokens`** membatasi satu respons, tanpa terlihat oleh model, sehingga menurunkannya tidak membuat model berhemat. Giliran yang membutuhkan ruang tersebut dibuang dan tetap ditagih. Pada benchmark tugas repositori internal[12](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), batas 16.384 token mengakhiri 15% percobaan Claude Opus 5 dan sepertiga percobaan Claude Fable 5, tidak satu pun terselesaikan. Run yang dibatasi menghabiskan lebih sedikit per percobaan tetapi membeli penyelesaian yang secara proporsional lebih sedikit, sehingga biaya per tugas terselesaikan sama dengan pada 64.000. Pada pengaturan itu tidak ada yang terpotong, dan Fable menyelesaikan 54,6% tugas alih-alih 36,6% pada masalah yang dinilai oleh kedua run (pada potongan terpisah dari subset SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), yang dijelaskan dalam referensi 12, 92% alih-alih 90%). Mencoba ulang percobaan yang dibatasi hanya menambah biaya: pada batas yang sama percobaan tersebut tidak pernah berhasil, dan pada batas yang lebih tinggi Anda juga membayar percobaan yang terbuang. Tetapkan `max_tokens` ke 64.000 untuk pekerjaan agentik (128.000, maksimumnya, pada effort `xhigh` atau `max`), [stream respons](https://platform.claude.com/docs/id/build-with-claude/streaming) sebesar itu, perlakukan [`stop_reason: max_tokens`](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons#max-tokens) sebagai kegagalan, dan hemat uang dengan effort dan anggaran tugas, yang dapat dilihat model.
* **Anggaran sesi pada Claude Managed Agents** adalah penghentian keras. [Anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets) adalah batas dolar pada satu sesi dengan tarif daftar untuk token, pencarian, dan waktu sesi. Pada batas tersebut, sesi dijeda dengan `stop_reason: budget_reached`; menaikkan anggaran melanjutkannya. Anggaran ini ditegakkan oleh platform, berfungsi pada model apa pun yang memiliki harga daftar (termasuk Claude Sonnet 5), dan dapat digabungkan dengan anggaran tugas yang bersifat anjuran. Deployment menerapkan field yang sama ke setiap run.

Grafik pertama dari dua grafik `max_tokens` memplot biaya per percobaan dan per tugas terselesaikan pada setiap batas:

![Grafik batang: pada batas 16k kedua model menghabiskan lebih sedikit per percobaan tetapi sama per tugas terselesaikan seperti pada 64k, karena menyelesaikan lebih sedikit tugas](https://platform.claude.com/docs/images/cost-intel-max-tokens-saving.png)

Grafik kedua memplot panjang output per giliran terhadap batas-batas tersebut:

![Dot plot output per giliran untuk Opus 5 dan Fable 5: median beberapa ratus token, giliran terpanjang 33k dan 59k, terhadap batas-batasnya](https://platform.claude.com/docs/images/cost-intel-max-tokens-ladder.png)

## Gabungkan model

Arsitektur multi-model cocok untuk beban kerja yang kompleksitas tugasnya cukup bervariasi sehingga langkah-langkah yang berbeda paling baik dilayani oleh model yang berbeda. Ketika lalu lintas Anda mencampur pekerjaan rutin yang ditangani model lebih kecil dengan andal dengan langkah-langkah lebih sulit yang membutuhkan kemampuan frontier, membagi pekerjaan menjaga kecerdasan frontier di tempat yang penting sementara sebagian besar token ditagih dengan tarif model lebih kecil. Ketika beban kerja tidak memiliki campuran itu, karena kesulitannya seragam atau merupakan satu rantai yang saling bergantung, satu model yang disetel dengan baik biasanya merupakan pilihan yang lebih baik. Setiap bagian strategi memberikan aturan untuk membedakan kedua kasus tersebut.

Dua strategi mencakup sebagian besar beban kerja, dan keduanya berbeda dalam model mana yang memegang loop utama:

| Strategi         | Alur kendali                                                       | Peran model frontier                          | Cocok untuk                                                                                                                     | Biaya frontier berskala dengan                  |
| ---------------- | ------------------------------------------------------------------ | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **Advisor**      | Model lebih kecil menjalankan loop, mengeskalasi sesuai permintaan | Dikonsultasikan untuk rencana dan koreksi     | Pekerjaan serial yang sulit di beberapa titik, seperti banyak giliran agen coding di antara beberapa keputusan nyata            | Seberapa sering executor macet                  |
| **Orchestrator** | Model frontier menjalankan loop, mendelegasikan pekerjaan massal   | Merencanakan, mengirim tugas, dan mensintesis | Pekerjaan yang menyebar ke file, dokumen, atau kasus yang benar-benar independen, terutama yang lebih dari satu jendela konteks | Seberapa sulit bagian-bagiannya dikoordinasikan |

### Strategi advisor: eskalasikan keputusan sulit

Dalam strategi advisor (penasihat), model executor (pelaksana) berbiaya lebih rendah menjalankan loop agen dan melakukan sebagian besar giliran. Ketika model tersebut menemui keputusan yang membutuhkan penilaian lebih mendalam, seperti memilih pendekatan atau memulihkan diri dari kegagalan, ia memanggil model advisor dengan kecerdasan lebih tinggi untuk mendapatkan panduan strategis, lalu melanjutkan. Sebagian besar token ditagih dengan tarif executor, dan hanya konsultasi sesekali yang ditagih dengan tarif advisor.

Untuk menggunakannya, tambahkan [alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool) ke permintaan Anda. Fitur beta ini menjalankan seluruh strategi di sisi server dalam satu permintaan `/v1/messages`: executor mengeluarkan panggilan alat, Anthropic menjalankan inferensi advisor, dan executor melanjutkan dengan saran tersebut; Anda tidak perlu menulis kode orkestrasi apa pun. Di Claude Managed Agents, [berikan sesi sebuah advisor](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor) dengan menambahkan entri `advisor` ke daftar `multiagent` milik agen; thread utama sesi berkonsultasi dengannya dengan cara yang sama. Claude Code juga mendukungnya; lihat [mengeskalasikan keputusan sulit dengan alat advisor](https://code.claude.com/docs/en/advisor).

![Diagram strategi advisor: model executor menjalankan loop utama dan memanggil advisor Claude Fable 5 sesuai kebutuhan](https://platform.claude.com/docs/images/model-routing-advisor-strategy.png)

**Apa yang menentukan hasilnya.** Advisor hanya melihat tugas melalui panggilan executor, sehingga dua hal menentukan seberapa besar bantuannya.

Yang pertama adalah kesenjangan antara kedua model. Advisor hanya dapat menyerahkan kemampuan yang tidak dimiliki executor: pada GPQA Diamond[9](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) executor Claude Haiku 4.5 memperoleh banyak sekali dari advisor Claude Opus 5, executor Claude Sonnet 5 memperoleh beberapa poin, dan executor frontier hampir tidak memperoleh apa-apa.

Yang kedua, dan yang rapuh, adalah apakah executor benar-benar bertanya (tingkat konsultasi atau consult rate). Executor dengan effort rendah dapat berhenti menyadari bahwa ia sedang buntu: pasangan yang berkonsultasi pada sebagian besar tugas dengan effort default dapat turun menjadi hampir tidak berkonsultasi sama sekali ketika effort diturunkan, dan kemudian mendapat skor di bawah executor sendirian. Tingkat ini juga bervariasi menurut tugas: pada DeepSWE[10](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) executor Sonnet 5 dengan effort rendah terus bertanya dan memperoleh 23 poin; pada SWE-bench Pro[3](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) executor yang sama berhenti bertanya. Ketika executor memang bertanya, ia mencapai sebagian besar jalannya. Di seluruh pasangan dalam bagan berikut, advisor menutup 60% hingga 90% kesenjangan terhadap model yang lebih kuat sementara model tersebut hanya dibayar untuk konsultasi, yang memungkinkan kasus-kasus penghematan biaya:

![Bagan batang enam pasangan advisor: kesenjangan yang tersedia versus perolehan yang terealisasi, diberi label dengan tingkat konsultasi, yang diikuti oleh perolehan tersebut](https://platform.claude.com/docs/images/cost-intel-advisor-mechanism.png)

Tingkat konsultasi merespons prompting. Dengan hanya deskripsi bawaan alat, executor terlalu jarang memanggil, terutama pada pekerjaan coding, sehingga [dokumentasi alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#prompting-for-coding-and-agent-tasks) memberikan prompt sistem yang meminta satu panggilan sebelum pekerjaan substantif dan satu sebelum menyelesaikan, sekitar dua hingga tiga panggilan per tugas. Pasangan coding yang diukur berikutnya berjalan dengan irama tersebut, sekitar dua konsultasi pada setiap tugas. Halaman itu juga membahas cara mendorong executor yang terlalu jarang memanggil dan membatasi panggilan di sisi klien untuk membatasi biaya. Jadi perhatikan tingkat konsultasi: minta melalui prompt, ukur, dan pulihkan effort executor jika tingkatnya anjlok.

**Kapan menguntungkan dari sisi biaya.** Advisor menghemat uang ketika beberapa konsultasi singkat, yang ditagih dengan tarif advisor, menggantikan menjalankan model advisor untuk seluruh tugas. Ini bekerja paling baik ketika model advisor dihargai jauh di atas model executor, sehingga konfigurasi yang paling hemat biaya adalah advisor frontier di atas executor tingkat menengah. Sebuah pasangan dapat bertahan bahkan di puncak rentang, karena saran juga menghemat token executor: executor yang diberi tahu pendekatan yang tepat menjelajahi lebih sedikit jalan buntu, yang dapat menutupi biaya konsultasi.

Pada benchmark agentic-coding internal[11](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), yang dijalankan dengan agen API biasa, executor Claude Opus 5 dengan advisor Claude Fable 5 adalah konfigurasi paling akurat yang diukur: 85,7% percobaan terselesaikan dengan biaya $8,40 per percobaan. Konfigurasi ini berada di atas garis yang melalui pengaturan effort masing-masing model sendiri, tetapi hanya satu atau dua poin di atas yang terbaik di antaranya (Opus sendirian pada pengaturan default, 84,4% dengan biaya $8,50, dan Fable sendirian pada `medium`, 83,4% dengan biaya $8,20), yang tidak dapat dipisahkan dari noise oleh satu kali run. Fable sendirian pada effort `medium` mencapai akurasi yang kira-kira sama dengan pasangan tersebut (83,4% dibandingkan dengan 85,7%) dengan biaya yang kira-kira sama ($8,20 dibandingkan dengan $8,40 per percobaan):

![Bagan, benchmark coding: kurva effort kedua model, dengan pasangan Opus 5 plus advisor Fable 5 tepat di atas puncak keduanya](https://platform.claude.com/docs/images/cost-intel-internal-coding-advisor.png)

Pengukuran sebelumnya melalui [mode advisor Claude Code](https://code.claude.com/docs/en/advisor) menghasilkan urutan yang sama. Bacalah hasil ini sebagai bentuk untuk diuji pada beban kerja Anda, bukan sebagai penghematan: di puncak rentang, advisor membeli sedikit akurasi dengan harga frontier, dan kasus penghematan biaya dimiliki oleh pasangan dengan kesenjangan kemampuan yang lebih lebar, seperti kasus pembacaan bagan berikut. Biaya latensinya adalah konsultasi itu sendiri: sekitar dua panggilan model frontier tambahan per tugas pada benchmark ini, masing-masing berada di jalur kritis tugas.

**Kapan menguntungkan dibandingkan menaikkan effort.** Ketika kesenjangan kemampuan lebih lebar dan akurasi beban kerja merespons effort, executor dengan effort rendah yang berkonsultasi dengan advisor dapat menjadi peningkatan yang lebih murah daripada menaikkan effort executor itu sendiri, karena advisor hanya dibayar pada tugas yang membutuhkannya.

Pada Chartography[13](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), benchmark pembacaan bagan publik yang dijalankan di [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) dengan advisor-nya, executor Claude Opus 5 pada effort `low` dengan advisor Claude Fable 5 mendapat skor 67,5 dengan biaya $0,60 per tugas. Itu berada di atas garis yang melalui pengaturan effort masing-masing model sendiri (Opus sendirian naik dari 49 ke 75 antara `low` dan `medium` dengan biaya $0,38 hingga $0,94), meskipun pengaturan `medium` dan default milik executor sendiri masih memegang skor tertinggi, dengan harga 1,6 dan 3,3 kali lipat:

![Bagan garis, Chartography: executor Opus 5 dengan effort rendah bersama advisor Fable 5 berada di atas kurva effort kedua model sendiri](https://platform.claude.com/docs/images/cost-intel-chart-reading-advisor.png)

Executor dengan effort rendah berkonsultasi dengan advisor pada 86% tugas, kondisi yang gagal dipenuhi oleh pasangan SWE-bench Pro. Ukur tingkat konsultasi dalam loop agen Anda sebelum mengandalkan konfigurasi ini.

Apa pun pasangannya, pertama-tama hitung harga model advisor sendirian pada effort rendah; itulah baseline yang harus dikalahkan. Periksa ulang pada setiap rilis model, karena rilis menggeser baik kesenjangan kemampuan maupun rasio harga.

**Kapan cocok.** Strategi advisor cocok untuk beban kerja di mana giliran sebagian besar bersifat mekanis tetapi rencana yang sangat baik itu penting: agen coding, computer use, dan pipeline riset multilangkah. Strategi ini kurang cocok ketika setiap giliran benar-benar membutuhkan kemampuan frontier, ketika tidak ada yang perlu direncanakan (tanya jawab satu giliran), atau ketika executor Anda sudah mendekati kemampuan advisor.

### Strategi orchestrator: delegasikan pekerjaan massal

Dalam strategi orchestrator (orkestrator), model frontier memegang loop. Model ini menguraikan tugas, mengirimkan subtugas ke model worker (pekerja) berbiaya lebih rendah, dan menggabungkan hasilnya. Transkrip orchestrator sendiri tetap pendek karena worker menyerap eksplorasi yang padat token, sehingga sebagian besar token ditagih dengan tarif worker sementara rencana dan sintesis tetap berasal dari model frontier.

Untuk membangunnya, gunakan [orkestrasi multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) di Claude Managed Agents: konfigurasikan agen koordinator (orchestrator) dan daftar agen worker, masing-masing dengan modelnya sendiri. Untuk contoh kerja lengkap dengan koordinator Claude Fable 5 dan worker Claude Sonnet 5, lihat resep Claude Cookbook [Coordinator pattern: big models for planning, small models for execution](https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_plan_big_execute_small.ipynb).

![Diagram strategi orchestrator: orchestrator Claude Fable 5 menyebarkan subtugas ke tiga worker Claude Sonnet 5](https://platform.claude.com/docs/images/model-routing-orchestrator-strategy.png)

Pola ini menghemat waktu nyata (wall-clock) ketika worker dapat berjalan secara paralel: pada benchmark korpus[8](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs), satu episode memakan waktu sedikit di atas 2 jam dengan koordinator menjalankan batas terdokumentasi platform sebanyak 25 worker bersamaan, dibandingkan dengan 11,4 jam secara solo. Pola ini menghemat uang hanya dalam dua situasi yang diukur. Pada pekerjaan yang dapat ditangani satu model sendirian, model yang sama pada effort lebih rendah selalu lebih murah.

**Kasus 1: asuransi terhadap ekor biaya pada pekerjaan rutin.** Model frontier yang berjalan sendirian sesekali berputar-putar pada masalah rutin yang biasanya dapat diselesaikannya. Karena Anda tidak dapat mengetahui sebelumnya mana yang akan demikian, beberapa run seperti itu mendominasi tagihan. Koordinator yang menyerahkan pekerjaan rutin ke worker berbiaya lebih rendah membatasi ekor tersebut, karena setiap putaran berlebih kini terjadi dengan tarif worker.

Anthropic mengukur ini pada potongan BrowseComp[4](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) yang sengaja dibuat mudah (10 masalah yang dapat diselesaikan model solo secara andal; 50 run terdelegasi dan 70 run solo). Koordinator Claude Fable 5 dengan satu worker Claude Sonnet 5 berbiaya sedikit di bawah setengah dari Fable sendirian secara rata-rata dan sekitar sepertiga pada persentil ke-90 ($12 dibandingkan dengan $33), dan satu run termahal model solo, seharga $84, juga salah:

![Dot plot, potongan rutin BrowseComp: run terdelegasi berbiaya sekitar setengah dari Fable sendirian secara rata-rata, sepertiga pada persentil ke-90](https://platform.claude.com/docs/images/cost-intel-tail-insurance.png)

Delegasi menguntungkan pada bagian pekerjaan yang rutin dan biasanya dapat diselesaikan, kebalikan dari intuisi bahwa worker adalah untuk masalah sulit. Pada set BrowseComp lengkap yang lebih sulit, ekonominya berbalik. Jika lalu lintas Anda memiliki ekor biaya panjang pada tugas rutin, inilah kasus orchestrator yang harus diukur pertama kali.

**Kasus 2: pekerjaan yang lebih besar dari satu jendela konteks.** Model solo harus mengerjakan input sebesar itu secara serial, satu "context window" (jendela konteks) pada satu waktu, membayar untuk membaca ulang statusnya sendiri pada setiap lintasan. Worker masing-masing membaca partisinya sendiri, secara paralel dan dengan tarif worker. Pekerjaan padat-baca yang masih muat dalam satu jendela konteks adalah masalah pemilihan model, bukan masalah delegasi: dari sisi biaya pembacaan saja, orchestrator unggul hanya ketika tidak ada satu konteks pun yang dapat menampung pekerjaan tersebut.

Anthropic membangun benchmark untuk kasus ini[8](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs): korpus 21,6 juta token dari 14 paket Python publik dengan 130 cacat yang ditanam, terlalu besar untuk jendela konteks mana pun. Menurunkan effort tidak dapat membantu, karena tagihannya adalah pembacaan korpus itu sendiri: Claude Fable 5 solo berbiaya $720 hingga $764 per episode pada setiap pengaturan effort, dan hanya akurasinya yang bergerak. Konfigurasi koordinator berbiaya lebih dari 60% lebih rendah daripada pengaturan mana pun tersebut dan mendapat skor 2 hingga 6 poin di bawah Fable pada `medium` atau default, sambil mengalahkan baseline Claude Sonnet 5 solo secara telak:

![Bagan, benchmark korpus: koordinator berbiaya lebih dari 60% lebih rendah daripada Fable solo pada setiap pengaturan effort, 2 hingga 6 poin di bawah yang terbaiknya](https://platform.claude.com/docs/images/cost-intel-corpus-pareto.png)

Akuntansi token menunjukkan alasannya. Kedua tagihan sebagian besar adalah pembacaan korpus yang dilayani dari cache: konfigurasi koordinator membaca sekitar 570 juta token cache per episode, hampir tiga kali lipat dari sekitar 200 juta milik model solo, dan tetap berbiaya kurang dari setengahnya, karena pembacaannya ditagih dengan tarif cache-read Claude Sonnet 5 alih-alih Claude Fable 5. Fable 5 pada effort default masih memegang akurasi puncak, dengan biaya 2,8 kali lipat konfigurasi koordinator, sehingga delegasi di sini membeli sebagian besar akurasi, bukan seluruhnya.

**Kapan delegasi tidak menguntungkan.** Orchestrator membeli sesuatu hanya ketika ada pekerjaan massal untuk diserahkan: banyak bagian independen, idealnya terlalu banyak untuk satu jendela konteks. Ketika pekerjaan berupa satu rantai yang saling bergantung, atau muat dalam satu konteks, orchestrator membayar untuk rencana, penyerahan, dan penggabungan yang didapat satu model secara gratis. Dalam setiap kasus seperti itu yang diukur, model koordinator sendirian pada effort lebih rendah unggul.

BrowseComp[4](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs) menunjukkan batasnya di dalam satu benchmark. Delegasi menguntungkan pada potongan rutin dan kalah pada set lengkap yang lebih sulit, di mana model frontier sendirian mencapai akurasi konfigurasi koordinator dengan biaya 22% hingga 30% lebih rendah. Pekerjaan eksternal independen melaporkan pola yang sama[5](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#refs). Jika pekerjaan berupa satu rantai, muat dalam satu konteks tanpa ekor biaya panjang, atau satu model pada effort lebih rendah sudah memenuhi standar Anda, jangan bangun orchestrator.

### Memilih di antara kedua strategi

Sebagian besar kasus bermuara pada satu pertanyaan: apakah pekerjaan terbagi menjadi bagian-bagian independen, atau merupakan satu jawaban yang dicapai melalui rantai langkah yang saling bergantung? [Tabel strategi](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#combine-models) memetakan kedua jawaban tersebut ke kedua strategi.

Jika Anda tidak yakin, jangan bangun apa pun dulu:

1. Sapu effort pada model Anda saat ini terlebih dahulu. Ini adalah eksperimen termurah di halaman ini, dan sebagian besar beban kerja berakhir di sana.
2. Jika sapuan menunjukkan kesenjangan, hitung harga model yang lebih kuat sendirian pada effort rendah. Itulah angka yang harus dikalahkan oleh pasangan advisor, dan pasangan di halaman ini yang mengalahkannya adalah yang executor-nya benar-benar berkonsultasi.

Hasil multi-model di halaman ini dinilai terhadap model yang sama pada effort lebih rendah dan terhadap model satu tingkat di bawahnya yang berjalan sendirian. Itulah perbandingan yang harus dijalankan pada beban kerja Anda sendiri, dan alasan mengapa langkah pertama adalah sapuan effort.

Ketika Anda memang menambahkan advisor, itu berupa definisi alat, bukan perancangan ulang arsitektur.

## Ukur pada beban kerja Anda sendiri

Angka-angka di halaman ini berasal dari Juli dan Agustus 2026, dengan harga daftar pada saat itu, dan akan bergeser seiring perubahan model dan harga. Tingkat eskalasi Anda, seberapa bersih tugas terbagi, dan panjang transkrip juga menggesernya. Metodenya tetap sama:

1. Ambil beberapa tugas dari log produksi, dengan bobot seperti lalu lintas nyata, dan [tulis pemeriksaan hasil](https://platform.claude.com/docs/id/test-and-evaluate/develop-tests) untuk masing-masing: tes lulus, tiket ditutup, jumlah baris benar. Catat biaya per tugas di samping skor: hitung harga keempat jumlah token dalam `usage` setiap respons dengan tarifnya masing-masing, dijumlahkan di seluruh permintaan tugas ([Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api) melaporkan agregatnya).
2. Buat baseline tingkatan model di seluruh level effort, bukan hanya default, dan plot skor terhadap pengeluaran. Konfigurasi multi-model harus mengalahkan seluruh kurva model tunggal.
3. Jika kurva menunjukkan kesenjangan yang tidak dapat ditutup oleh effort, tambahkan strategi multi-model yang cocok dan jalankan ulang suite.
4. Jalankan pemenangnya dalam mode shadow pada sebagian lalu lintas sebelum peralihan, lalu biarkan suite terus berjalan.

Contoh berikut menghitung biaya langkah 1 untuk satu permintaan dengan harga daftar Claude Opus 5:

<CodeGroup>
  ```bash cURL
  # Harga per juta token dari halaman harga; ubah kedua nilai ini untuk model lain.
  INPUT_PER_MTOK=5.00 # Claude Opus 5
  OUTPUT_PER_MTOK=25.00

  response=$(curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }')

  cost=$(jq -r --argjson in_price "$INPUT_PER_MTOK" --argjson out_price "$OUTPUT_PER_MTOK" '
    .usage
    | (.input_tokens * $in_price
       + (.cache_creation_input_tokens // 0) * $in_price * 1.25  # 5-minute cache write
       + (.cache_read_input_tokens // 0) * $in_price * 0.10      # cache read
       + .output_tokens * $out_price) / 1e6
  ' <<<"$response")
  printf 'Request cost: $%.6f\n' "$cost"
  ```

  ```bash CLI
  # Harga per juta token dari halaman harga; ubah dua nilai ini untuk model lain.
  INPUT_PER_MTOK=5.00 # Claude Opus 5
  OUTPUT_PER_MTOK=25.00

  USAGE=$(ant messages create \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}' \
    --transform usage)

  COST=$(jq -r --argjson in_price "$INPUT_PER_MTOK" --argjson out_price "$OUTPUT_PER_MTOK" '
    (.input_tokens * $in_price
      + (.cache_creation_input_tokens // 0) * $in_price * 1.25  # 5-minute cache write
      + (.cache_read_input_tokens // 0) * $in_price * 0.10      # cache read
      + .output_tokens * $out_price) / 1e6
  ' <<<"$USAGE")
  printf 'Request cost: $%.6f\n' "$COST"
  ```

  ```python Python
  # Harga per juta token dari halaman harga; ubah dua nilai ini untuk model lain.
  INPUT_PER_MTOK = 5.00  # Claude Opus 5
  OUTPUT_PER_MTOK = 25.00

  client = anthropic.Anthropic()
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )
  usage = response.usage
  cost = (
      usage.input_tokens * INPUT_PER_MTOK
      # Penulisan cache ditagih 1,25x harga input (cache 5 menit); pembacaan cache 0,1x.
      + (usage.cache_creation_input_tokens or 0) * INPUT_PER_MTOK * 1.25
      + (usage.cache_read_input_tokens or 0) * INPUT_PER_MTOK * 0.10
      + usage.output_tokens * OUTPUT_PER_MTOK
  ) / 1_000_000
  print(f"Request cost: ${cost:.6f}")
  ```

  ```typescript TypeScript
  // Harga per juta token dari halaman harga; ubah dua nilai ini untuk model lain.
  const INPUT_PER_MTOK = 5.0; // Claude Opus 5
  const OUTPUT_PER_MTOK = 25.0;

  const client = new Anthropic();
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  });
  const usage = response.usage;
  const cost =
    (usage.input_tokens * INPUT_PER_MTOK +
      (usage.cache_creation_input_tokens ?? 0) * INPUT_PER_MTOK * 1.25 + // 5-minute cache write
      (usage.cache_read_input_tokens ?? 0) * INPUT_PER_MTOK * 0.1 + // cache read
      usage.output_tokens * OUTPUT_PER_MTOK) /
    1_000_000;
  console.log(`Request cost: $${cost.toFixed(6)}`);
  ```

  ```csharp C#
  // Harga per juta token dari halaman harga; ubah dua nilai ini untuk model lain.
  const double InputPerMtok = 5.00; // Claude Opus 5
  const double OutputPerMtok = 25.00;

  AnthropicClient client = new();
  var response = await client.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5,
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],
      }
  );
  var usage = response.Usage;
  double cost =
      (
          usage.InputTokens * InputPerMtok
          + (usage.CacheCreationInputTokens ?? 0) * InputPerMtok * 1.25 // 5-minute cache write
          + (usage.CacheReadInputTokens ?? 0) * InputPerMtok * 0.10 // cache read
          + usage.OutputTokens * OutputPerMtok
      ) / 1_000_000;
  Console.WriteLine($"Request cost: ${cost:F6}");
  ```

  ```go Go
  // Harga per juta token dari halaman harga; ubah kedua nilai ini untuk model lain.
  const (
  	inputPerMTok  = 5.00 // Claude Opus 5
  	outputPerMTok = 25.00
  )

  // ...
  	client := anthropic.NewClient()

  	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5,
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
  		float64(usage.CacheCreationInputTokens)*inputPerMTok*1.25 + // 5-minute cache write
  		float64(usage.CacheReadInputTokens)*inputPerMTok*0.10 + // cache read
  		float64(usage.OutputTokens)*outputPerMTok) / 1_000_000
  	fmt.Printf("Request cost: $%.6f\n", cost)
  ```

  ```java Java
  // Harga per juta token dari halaman harga; ubah dua nilai ini untuk model lain.
  static final double INPUT_PER_MTOK = 5.00; // Claude Opus 5
  static final double OUTPUT_PER_MTOK = 25.00;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Message response = client.messages().create(MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .build());

      Usage usage = response.usage();
      double cost = (usage.inputTokens() * INPUT_PER_MTOK
          + usage.cacheCreationInputTokens().orElse(0L) * INPUT_PER_MTOK * 1.25 // 5-minute cache write
          + usage.cacheReadInputTokens().orElse(0L) * INPUT_PER_MTOK * 0.10 // cache read
          + usage.outputTokens() * OUTPUT_PER_MTOK) / 1_000_000;
      IO.println("Request cost: $%.6f".formatted(cost));
  }
  ```

  ```php PHP
  // Harga per juta token dari halaman harga; ubah dua nilai ini untuk model lain.
  const INPUT_PER_MTOK = 5.00; // Claude Opus 5
  const OUTPUT_PER_MTOK = 25.00;

  $client = new Client();
  $response = $client->messages->create(
      model: 'claude-opus-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
  );
  $usage = $response->usage;
  $cost = (
      $usage->inputTokens * INPUT_PER_MTOK
      + ($usage->cacheCreationInputTokens ?? 0) * INPUT_PER_MTOK * 1.25 // 5-minute cache write
      + ($usage->cacheReadInputTokens ?? 0) * INPUT_PER_MTOK * 0.10 // cache read
      + $usage->outputTokens * OUTPUT_PER_MTOK
  ) / 1_000_000;
  printf("Request cost: \$%.6f\n", $cost);
  ```

  ```ruby Ruby
  # Harga per juta token dari halaman harga; ubah dua nilai ini untuk model lain.
  INPUT_PER_MTOK = 5.00 # Claude Opus 5
  OUTPUT_PER_MTOK = 25.00

  client = Anthropic::Client.new
  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  )
  usage = response.usage
  cost = (
    usage.input_tokens * INPUT_PER_MTOK +
    usage.cache_creation_input_tokens.to_i * INPUT_PER_MTOK * 1.25 + # 5-minute cache write
    usage.cache_read_input_tokens.to_i * INPUT_PER_MTOK * 0.10 + # cache read
    usage.output_tokens * OUTPUT_PER_MTOK
  ) / 1_000_000
  puts format("Request cost: $%.6f", cost)
  ```
</CodeGroup>

Dalam loop agen, komponen cache-read biasanya yang terbesar dari keempatnya; jika tidak, periksa apakah caching aktif. Ketika [alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#usage-and-billing) atau [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction#understanding-usage) diaktifkan, sebagian token hanya dilaporkan dalam `usage.iterations` dan tidak dalam total tingkat atas, jadi jumlahkan `usage.iterations` sebagai gantinya, dengan menghitung harga entri `advisor_message` pada tarif model advisor.

Tabel berikut mencantumkan tuas-tuas dalam urutan untuk dicoba:

| Tuas                                 | Penghematan dalam run ini                                                                                                                                            | Biaya kualitas                                                             | Latensi                                  | Di mana                                                                                                                                                                            |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Caching prompt                       | Biaya terpangkas dengan faktor 2,5 hingga 3,7 pada loop agen; 83% pada run triase                                                                                    | Tidak ada                                                                  | Lebih cepat                              | [Cache konteks berulang](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#cache-repeated-context)                                      |
| Pemangkasan input                    | Tambahan 5 poin persentase pada run triase                                                                                                                           | Tidak ada                                                                  | Netral                                   | [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens)                      |
| Compaction                           | 38% pada run triase panjang; tidak ada pada loop pendek                                                                                                              | Tidak ada yang terukur                                                     | Netral                                   | [Pangkas token input dan konteks](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#trim-input-and-context-tokens)                      |
| Batch API                            | 50%                                                                                                                                                                  | Tidak ada                                                                  | Hasil dalam 24 jam                       | [Batch pekerjaan yang bisa menunggu](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#batch-work-that-can-wait)                        |
| Audit prompt terhadap model saat ini | 14% pada kedua migrasi yang diukur                                                                                                                                   | Tidak ada; peningkatan pada salah satunya                                  | Lebih cepat (lebih sedikit putaran alat) | [Audit prompt terhadap model saat ini](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#audit-prompts-against-the-current-model)       |
| Effort lebih rendah                  | Pekerjaan pengetahuan: `medium` 15% hingga 30%, `low` sepertiga hingga setengah; coding panjang: `medium` sekitar setengah, `low` sekitar tiga perempat              | 1 hingga 3 poin pada pekerjaan pengetahuan, 2 hingga 8 pada coding panjang | Lebih cepat                              | [Setel effort](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#tune-effort)                                                           |
| Jalankan ulang kegagalan             | Sekitar setengah, pada tingkat kelulusan yang sama                                                                                                                   | Tidak ada                                                                  | Dua run pada tugas yang gagal            | [Jalankan ulang kegagalan pada effort lebih tinggi](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#re-run-failures-at-higher-effort) |
| Anggaran tugas                       | 18% hingga 47%                                                                                                                                                       | 3 hingga 4 poin                                                            | Lebih cepat                              | [Tetapkan anggaran dan batas output](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                     |
| Menaikkan `max_tokens`               | Tidak ada per tugas terselesaikan, tetapi lebih banyak tugas terselesaikan                                                                                           | Peningkatan 2 hingga 18 poin                                               | Netral                                   | [Tetapkan anggaran dan batas output](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#set-budgets-and-output-caps)                     |
| Advisor                              | Bergantung pada kesenjangan kemampuan dan tingkat konsultasi; pasangan pembacaan bagan mendapat skor di atas kurva effort kedua model, pasangan coding hanya sedikit | Peningkatan kecil                                                          | Sekitar dua panggilan tambahan per tugas | [Strategi advisor](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#advisor-strategy-escalate-hard-decisions)                          |
| Orchestrator                         | Lebih dari 60% di bawah model frontier di luar satu jendela konteks; sekitar setengah pada ekor rutin                                                                | 2 hingga 6 poin di bawah model frontier                                    | Jauh lebih cepat pada input besar        | [Strategi orchestrator](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#orchestrator-strategy-delegate-bulk-work)                     |

## Benchmark yang dirujuk

Semua pengukuran adalah run internal Anthropic atas benchmark-benchmark ini. Kecuali disebutkan lain, biaya dalam USD dengan harga daftar Agustus 2026; angka Claude Sonnet 5 menggunakan $2 dan $10 per juta token input dan output. Bagan berlabel "notional USD" menghitung harga jumlah token setiap permintaan pada tarif tersebut alih-alih melaporkan faktur.

1. **WideSearch:** Wong et al., "WideSearch: Benchmarking Agentic Broad Info-Seeking," arXiv:2508.07999, 2025. Tugas riset web luas yang dinilai berdasarkan kelengkapan dan akurasi tabel banyak-baris; 200 masalah, 3 run per konfigurasi. Bagan caching dan effort berasal dari run terpisah, sehingga biaya per masalah sedikit berbeda. Bagan konsentrasi biaya adalah run 20 masalah terpisah, 3 run per masalah, dihitung biayanya dari catatan penagihan per permintaan.
2. **GDPval:** OpenAI, "GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks," 2025. Hasil kerja pengetahuan yang dinilai terhadap rubrik tugas; run 210 tugas dari gold set yang dirilis, satu percobaan per tugas. Model Claude yang menilai, sehingga skor absolut mungkin berbeda dari hasil yang dipublikasikan.
3. **SWE-bench Pro:** Scale AI, "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?", 2025. Subset 482 masalah yang dipilih untuk kompatibilitas dengan harness evaluasi Anthropic; skor tidak dapat dibandingkan dengan leaderboard publik. Claude Opus 5 pada effort default merata-ratakan dua run; pengaturan effort yang dikurangi adalah run tunggal. Angka eskalasi berasal tugas per tugas dari run tersebut: `low` terlebih dahulu, lalu default pada kegagalannya, menyelesaikan 92,5% hingga 93,6% di seluruh pasangan run dengan biaya sekitar $0,70; `medium` terlebih dahulu, 93,8% hingga 94,2% dengan biaya sekitar $0,95; default dijalankan ulang pada kegagalannya sendiri, 94,0% dengan biaya $1,58; semuanya pada default, 90,9% hingga 92,5% dengan biaya $1,39. Pasangan executor Claude Sonnet 5 pada bagan advisor berasal dari seri Agustus 2026 yang sama pada subset ini: pasangan Sonnet-plus-Opus dijalankan dua kali (satu run dan satu replikasi persis) dan pasangan effort rendah satu kali; angka anggaran tugas adalah satu run per anggaran pada subset yang sama. Angka Claude Fable 5 dalam [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task) adalah run tunggal Juli 2026, yang juga merupakan baseline tanpa anggaran pada bagan anggaran tugas; setiap run beranggaran menyelesaikan semua 482 masalah tanpa kesalahan harness.
4. **BrowseComp:** Wei et al., "BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents," OpenAI, 2025. Angka effort menggunakan potongan 500 masalah, satu hingga tiga run per pengaturan. Bagan asuransi biaya menggunakan 10 masalah yang terselesaikan secara andal dari potongan 26 masalah, 50 run terdelegasi dan 70 run solo ($6,45 dibandingkan dengan $11,99 per run secara ekspektasi); angka terdelegasi membawa pita pengukuran sekitar 20%.
5. **Penskalaan arsitektur agen:** Kim et al., "Towards a Science of Scaling Agent Systems," arXiv:2512.08296, 2025. Studi eksternal independen, dikutip hanya untuk arah temuan tentang kapan delegasi tidak menguntungkan, bukan untuk angka apa pun.
6. **DeepWideSearch:** "DeepWideSearch: Benchmarking Depth and Width in Agentic Information Seeking," arXiv:2510.20168, 2025. Ke-220 pertanyaannya mencakup 15 domain, masing-masing menggabungkan pengumpulan banyak-baris dengan pengambilan multi-hop; diukur pada set baris tetap benchmark, 3 run per konfigurasi.
7. **DeepResearch Bench II:** Li et al., "DeepResearch Bench II: Diagnosing Deep Research Agents via Rubrics from Expert Report," arXiv:2601.08536, 2026. Ke-132 tugas risetnya di 22 domain dinilai terhadap rubrik biner turunan pakar; diukur pada subset 50 tugas yang distratifikasi di seluruh tema, satu percobaan per tugas, 3 run, diberi skor pada tugas yang tidak ditolak oleh konfigurasi mana pun. Claude Opus 4.6 menilai di bawah protokol rubrik benchmark; versi aslinya menggunakan penilai berbeda, dan penilai Anthropic mungkin lebih menyukai gaya internal. Run tersebut mendahului Claude Opus 5, sehingga model itu tidak ada dalam bagan [Bandingkan model](https://platform.claude.com/docs/id/about-claude/models/optimizing-for-cost-and-intelligence#compare-models-on-cost-per-task). Biaya Sonnet 5 sedikit berbeda antara bagan caching (biaya inferensi, dengan dan tanpa caching) dan bagan tersebut (biaya keseluruhan, caching aktif); keduanya berasal dari run yang sama.
8. **Sapuan cacat korpus:** Internal Anthropic, untuk pekerjaan yang lebih besar dari satu jendela konteks: korpus 21,6 juta token dari 14 sumber paket Python publik dengan 130 cacat yang ditanam dan penilaian deterministik; protokol ditetapkan sebelum run dan ditinjau secara internal; tiga run per konfigurasi. Setiap konfigurasi berjalan di Claude Managed Agents. Konfigurasi tim yang dibagankan adalah run Agustus 2026 di mana koordinator Claude Fable 5 menjalankan seluruh sapuan di dalam platform pada batas terdokumentasinya sebanyak 25 worker Claude Sonnet 5 bersamaan; ketiga episodenya mendapat skor F1 0,842, 0,805, dan 0,810 dengan biaya $263, $299, dan $261. Konfigurasi solo adalah run Juli 2026 pada build korpus yang sama. F1 absolut bersifat spesifik untuk build korpus ini, tidak dapat dibandingkan antar benchmark; perbandingan konfigurasi bersifat setara.
9. **GPQA Diamond:** Rein et al., "GPQA: A Graduate-Level Google-Proof Q\&A Benchmark," 2023. Subset Diamond 198 pertanyaan, diukur Agustus 2026, dua run per konfigurasi, dinilai model terhadap jawaban referensi, token advisor diukur per permintaan. Pemeriksaan keamanan platform menolak dua pertanyaan biologi pada executor Sonnet dan Opus; mengecualikannya tidak mengubah perbandingan mana pun lebih dari satu poin.
10. **DeepSWE:** Datacurve, "DeepSWE: Measuring Frontier Coding Agents on Original, Long-Horizon Engineering Tasks," arXiv:2607.07946, 2026. Diukur Agustus 2026: 113 tugas orisinal di lima bahasa dengan verifier berbasis program. Pasangan masing-masing dua run dengan token advisor diukur per permintaan, dan menggunakan loop advisor sisi klien alih-alih alat advisor, dengan akuntansi identik. Sapuan effort model tunggal adalah run tunggal yang dihitung harganya dari jumlah token, sebuah pendekatan yang memperhitungkan cache. Biaya per tugas adalah total run dibagi 113.
11. **Benchmark agentic-coding internal:** Internal Anthropic: 370 tugas repositori yang dinilai oleh tes milik repositori itu sendiri. Angka API (Opus 5 sendirian, Fable 5 sendirian, dan pasangannya) diukur Agustus 2026 pada effort default dengan batas output 128.000 token, satu run per konfigurasi: lima percobaan per tugas pada pengaturan default dan untuk pasangan, satu pada `low` dan `medium`; pasangan rata-rata sekitar dua konsultasi advisor per percobaan; biaya adalah per percobaan. Angka Claude Code adalah run Juli 2026 atas tugas yang sama, satu run per konfigurasi, biaya perkiraan.
12. **Benchmark tugas repositori internal (pengukuran batas):** Set internal Anthropic terpisah berisi sekitar 130 tugas repositori, dijalankan Agustus 2026 dengan loop agen API biasa, satu percobaan per tugas. Angka 16.384 token merata-ratakan dua run per model; angka 64.000 token adalah run tunggal (124 tugas diberi skor untuk Opus 5; 108 untuk Claude Fable 5, karena lingkungan melewatkan sisanya sebelum model berjalan). Sekitar setengah percobaan Fable yang diakhiri oleh batas 16.384 terselesaikan pada 64.000; run Fable lebih lanjut pada 128.000 mendapat skor 56,1%, dalam rentang noise dari run 64.000. Angka batas SWE-bench Pro adalah satu run Claude Fable 5 per batas pada effort default pada subset 100 masalah yang distratifikasi dari set 482 masalah referensi 3, tidak dapat dibandingkan dengan skornya. Distribusi per giliran pada bagan berasal dari run Opus pada 64.000 dan run Fable pada 128.000, sehingga tidak ada yang terpotong oleh batasnya sendiri.
13. **Chartography:** Surge AI, "Chartography," 2026. Set lengkap 100 pertanyaan yang dirilis, diukur Agustus 2026 dengan implementasi Anthropic di Claude Managed Agents (sandbox cloud standar; konfigurasi advisor menggunakan advisor Managed Agents). Claude Sonnet 4.6 menilai alih-alih penilai referensi dan benchmark berjalan dengan alat, sehingga skor dapat dibandingkan antar konfigurasi di sini tetapi tidak dengan leaderboard yang dipublikasikan. Dua run per konfigurasi, digabungkan; sebaran antar run adalah 4 hingga 10 poin. Biaya tidak termasuk waktu sandbox, yang menambah kurang dari 1%. Perbandingan tingkat konsultasi berasal dari menjalankan ulang konfigurasi yang sama pada Messages API dengan set alat container.
14. **Evaluasi audit prompt support-desk:** Set buatan Anthropic berisi 44 tiket dukungan dengan penilaian deterministik, dijalankan Agustus 2026 di bawah enam prompt sistem, masing-masing menambahkan ke prompt bersih yang sama satu pola yang umum dalam prompt yang ditulis untuk Claude Opus 4.8 dan Claude Sonnet 4.6. Setiap titik bagan adalah salah satu dari tiga kasus (model lama, model baru pada prompt yang sama, model baru setelah audit) yang dirata-ratakan atas enam prompt dan 44 tiket. Peningkatan akurasi Opus 5 memiliki interval kepercayaan 95% sebesar 3 hingga 8 poin; perbedaan akurasi Sonnet berada dalam rentang noise.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Caching prompt" icon="database" href="https://platform.claude.com/docs/id/build-with-claude/prompt-caching">
    Kemenangan gratis terbesar di halaman ini: penyiapan, masa berlaku, dan diagnostik.
  </Card>

  <Card title="Effort" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Tukar kecerdasan dengan latensi dan biaya dalam satu model.
  </Card>

  <Card title="Memilih model yang tepat" icon="settings" href="https://platform.claude.com/docs/id/about-claude/models/choosing-a-model">
    Evaluasi kemampuan, kecepatan, dan biaya di seluruh keluarga model Claude.
  </Card>

  <Card title="Anggaran tugas" icon="clock" href="https://platform.claude.com/docs/id/build-with-claude/task-budgets">
    Berikan loop agen hitung mundur token yang mereka atur sendiri.
  </Card>

  <Card title="Anggaran sesi" icon="coins" href="https://platform.claude.com/docs/id/managed-agents/budgets">
    Tetapkan batas dolar yang tegas pada sesi Managed Agents.
  </Card>

  <Card title="Harga" icon="dollar-sign" href="https://platform.claude.com/docs/id/about-claude/pricing">
    Lihat harga per token terkini untuk setiap model Claude.
  </Card>

  <Card title="Cookbook: optimasi biaya pada Claude API" icon="book" href="https://platform.claude.com/cookbook/cost-optimization-cost-optimization">
    Terapkan tuas-tuas ini satu per satu pada agen yang berfungsi dalam notebook yang dapat dijalankan, dengan biaya per tugas setelah setiap langkah.
  </Card>

  <Card title="Webinar: Membangun di Claude Platform" icon="play" href="https://www.anthropic.com/webinars/building-on-the-claude-platform-claude-fable-5-and-model-orchestration-patterns">
    Tonton panduan langkah demi langkah tentang Claude Fable 5 serta pola advisor dan orchestrator.
  </Card>
</CardGroup>
