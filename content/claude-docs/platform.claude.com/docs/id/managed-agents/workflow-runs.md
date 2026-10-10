---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/workflow-runs
fetched_at: 2026-10-10T02:28:27.766834Z
sha256: 7db473823ea6b7ca3d4143dbf5002f339625d9fc171a01afb92497ec9d3c9ac6
---

---
title: Eksekusi workflow
url: https://platform.claude.com/docs/id/managed-agents/workflow-runs
description: "Ikuti eksekusi workflow milik agen: status dan event-nya, kapan pekerjaan selesai, apa yang diblokir oleh sebuah eksekusi, anggaran, dan batas."
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

**Workflow** (alur kerja) adalah program yang ditulis oleh agen untuk menjalankan banyak agen dan menggabungkan apa yang mereka kembalikan. **Workflow run** (eksekusi workflow) adalah satu kali jalannya sebuah workflow. **[Dynamic workflows](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#dynamic-workflows)** (alur kerja dinamis) adalah fitur yang memungkinkan agen menulis workflow dan memulai eksekusi. Anda mengaktifkan atau menonaktifkannya dengan pengaturan `workflows` di blok `multiagent` milik agen.

Server menjalankan workflow di latar belakang. Agen-agennya bekerja di [thread sesi](https://platform.claude.com/docs/id/managed-agents/session-threads) yang dibuat server sesuai kebutuhan workflow. Anda mengikuti eksekusi melalui [aliran event](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) sesi. Hanya agen yang memulai eksekusi. Tidak ada event yang Anda kirim yang mengakhiri eksekusi; mengarsipkan sesi dapat mengakhirinya.

## Cara kerja alur kerja dinamis

Agen yang dijalankan sesi menulis setiap workflow untuk pekerjaan yang Anda jelaskan. Workflow adalah sebuah program: ia menjalankan agen lain, mengumpulkan apa yang dikembalikan masing-masing, dan menggabungkan hasilnya. Dengan begitu, agen dapat menangani tugas yang terlalu besar untuk satu percakapan, seperti peninjauan ratusan dokumen. Selama eksekusi, agen dapat terus bekerja atau mengakhiri gilirannya, dan ia dapat memeriksa eksekusi tersebut.

<Frame>
  ![Lapisan dari sebuah workflow run (eksekusi workflow): eksekusi, dua fasenya, dan thread agen di masing-masing fase. Hasil diteruskan dari satu fase ke fase berikutnya.](https://platform.claude.com/docs/images/workflow-anatomy.svg)
</Frame>

Diagram menunjukkan satu contoh. Setiap workflow yang ditulis agen memiliki fase dan agennya sendiri. Sebuah eksekusi memiliki lapisan-lapisan berikut:

* **Eksekusi workflow:** Server menjalankan workflow di latar belakang, sebagai satu eksekusi workflow. Sebuah sesi dapat memiliki beberapa eksekusi yang terbuka pada saat yang sama.
* **Fase:** Workflow dapat membagi pekerjaannya menjadi fase-fase. Fase adalah tahap bernama dari eksekusi, seperti "Read the contracts". Anda mengikuti kemajuan eksekusi melalui event fasenya.
* **Thread agen:** Dalam sebuah fase, program menjalankan agen. Setiap agen bekerja di [thread sesi](https://platform.claude.com/docs/id/managed-agents/session-threads) miliknya sendiri, dengan prompt yang ditulis oleh program. Agen dalam sebuah eksekusi dapat berupa agen inline, yang didefinisikan sendiri oleh program, atau agen predefined, yang Anda cantumkan di [`workflows.predefined_agents`](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#predefined-and-inline-agents). Untuk apa yang ditampilkan setiap thread, lihat [Thread sebuah eksekusi](https://platform.claude.com/docs/id/managed-agents/workflow-runs#a-runs-threads).

Program dapat melakukan hal-hal berikut:

* **Menjalankan agen pada saat yang sama:** Program dapat menjalankan banyak agen pada saat yang sama, yang disebut "fanning out" (penyebaran). Dalam diagram, tiga agen membaca kontrak di fase pertama.
* **Meneruskan hasil dari satu agen ke agen lain:** Setiap agen mengembalikan hasilnya ke program. Program dapat meneruskan hasil tersebut ke agen lain. Dalam diagram, agen di fase kedua bekerja dengan apa yang dikembalikan oleh tiga agen pertama. Agen-agen dalam sebuah eksekusi juga bekerja dengan file yang sama, di sandbox sesi.
* **Mengambil langkah berikutnya sendiri:** Hasil agen masuk ke program, bukan ke agen yang dijalankan sesi. Program menentukan agen mana yang berjalan berikutnya, dan ia menulis prompt mereka.
* **Mengulang dan memilih:** Di dalam sebuah fase, program dapat mengulang pekerjaan dan memilih langkah berikutnya berdasarkan apa yang dikembalikan agen. Misalnya, program dapat meminta sebuah draf direvisi hingga peninjauan lolos atau sejumlah putaran yang ditetapkan habis. Dalam diagram, program dapat mengulang sebuah langkah di dalam fase kedua.
* **Menangani agen yang gagal:** Ketika salah satu agennya gagal, program dapat menangani kegagalan tersebut atau membiarkannya mengakhiri eksekusi.

Ketika eksekusi berakhir, agen yang dijalankan sesi mendapat giliran untuk membaca apa yang dilakukan eksekusi tersebut. Agen kemudian dapat menjawab Anda atau memulai eksekusi lain. [Event eksekusi](https://platform.claude.com/docs/id/managed-agents/workflow-runs#run-events) mencantumkan kasus-kasus di mana giliran itu datang belakangan atau tidak datang.

Anda dapat memandu cara eksekusi melakukan pekerjaan, misalnya cara ia membagi pekerjaan dan apa yang dilakukannya ketika sebuah agen gagal. Lihat [Beri tahu agen kapan menggunakan eksekusi](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#tell-the-agent-when-to-use-a-run).

## Bagaimana eksekusi berpindah antar statusnya

<Frame>
  ![Status workflow run (eksekusi workflow): running, idle, dan ended, serta apa yang memindahkan eksekusi dari satu status ke status lain.](https://platform.claude.com/docs/images/workflow-run-states.svg)
</Frame>

Sebuah eksekusi dimulai dalam status running atau idle. Mencapai anggaran, misalnya, menjeda eksekusi yang sedang berjalan, sehingga menjadi idle; menaikkan atau menghapus anggaran kemudian membuatnya berjalan lagi, kecuali jika interupsi juga menjedanya. Eksekusi yang sedang berjalan berakhir ketika workflow-nya selesai, agen menghentikannya, eksekusi gagal, masa hidupnya habis, atau sesi diarsipkan. Eksekusi yang idle juga dapat berakhir, misalnya ketika agen menghentikannya atau sesi diarsipkan.

Sebuah eksekusi **terbuka** sejak event `workflow_run.created` hingga event `workflow_run.status_ended`, baik saat berjalan maupun idle. Eksekusi berstatus idle selama dijeda, misalnya pada anggaran sesi. Masa hidup eksekusi secara default adalah 24 jam. Agen dapat menetapkan masa hidup yang lebih pendek saat memulai eksekusi. Waktu yang dihabiskan eksekusi untuk menunggu klien Anda dihitung dalam masa hidup tersebut. Jeda tidak menghentikan berjalannya masa hidup eksekusi, sehingga eksekusi yang tetap dijeda dapat berakhir dengan `timeout_error`. Event-event berikut melaporkan awal eksekusi, fase-fasenya, dan akhirnya. Jeda pada anggaran juga mengirim satu event. Jeda setelah interupsi mungkin tidak mengirim event apa pun. Setiap event `workflow_run.*` menyertakan `workflow_run_id`, yang bernilai `null` hanya pada `workflow_run.error` ketika tidak ada eksekusi yang dibuat.

## Event eksekusi

Event eksekusi tiba di aliran event sesi, yaitu aliran thread utama, dan mencantumkan event sesi juga mengembalikannya. Event eksekusi tidak memicu [webhook](https://platform.claude.com/docs/id/managed-agents/webhooks). Event status dari thread eksekusi tiba di aliran yang sama. Masing-masing menyebutkan thread-nya di `session_thread_id`, dan thread sebuah eksekusi adalah thread yang event `session.thread_created`-nya memiliki `workflow_run_id` eksekusi tersebut.

| Event                                                    | Kapan tiba                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Apa yang harus dilakukan                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workflow_run.created`                                   | Agen memulai sebuah eksekusi. Menyertakan `workflow_run_id` (`wrun_…`), `name` dan `description` eksekusi, serta `phases`, yaitu fase-fase yang dideklarasikan workflow, masing-masing dengan `id`, `name`, dan `description`. `description` bernilai `null` ketika workflow tidak memberikannya. `phases` selalu ada dan dapat kosong. `name` dan `description` eksekusi dan fase adalah teks yang ditulis model, sehingga dapat mengulang kata-kata dari permintaan Anda. `name` eksekusi juga dapat berupa nama yang ditetapkan server. | Lacak eksekusi sebagai terbuka. Tampilkan `name`-nya, dan kemajuan terhadap `phases`.                                                                                                                                                                                                                                                                                                                                                                                  |
| `workflow_run.status_running`                            | Ketika eksekusi mulai dijalankan, yang bisa beberapa saat setelah `created`, dan setiap kali eksekusi dilanjutkan setelah jeda pada anggaran. Melanjutkan setelah interupsi mungkin tidak mengirimnya. Eksekusi yang dimulai dalam status idle mungkin mendapat `workflow_run.status_idle` terlebih dahulu.                                                                                                                                                                                                                                | Tampilkan eksekusi sebagai sedang berjalan.                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `workflow_run.status_idle`                               | Eksekusi dijeda, misalnya pada anggaran sesi. Event ini tidak menyebutkan alasannya. Jeda setelah interupsi mungkin tidak mengirimnya.                                                                                                                                                                                                                                                                                                                                                                                                     | Untuk melanjutkan, lihat [Anggaran dan batas](https://platform.claude.com/docs/id/managed-agents/workflow-runs#budgets-and-limits) atau [Menginterupsi sesi dengan eksekusi yang terbuka](https://platform.claude.com/docs/id/managed-agents/workflow-runs#interrupt-a-session-with-runs-open).                                                                                                                                                                        |
| `workflow_run.phase_started`, `workflow_run.phase_ended` | Workflow memasuki atau meninggalkan sebuah fase, atau akhir eksekusi menutup fase yang masih terbuka. Event akhir tidak menyebutkan apakah pekerjaan fase tersebut selesai. Keduanya menyertakan `workflow_run_phase_id`. Event akhir juga memiliki `phase_started_id`, yaitu `id` dari event awal yang ditutupnya. Keduanya tidak memiliki nama fase: cari berdasarkan `workflow_run_phase_id` di `phases` dari `workflow_run.created`.                                                                                                   | Perbarui kemajuan. Fase berjalan satu per satu, dalam urutan `phases`, masing-masing paling banyak sekali, tetapi API tidak menjaminnya. Cocokkan akhir fase dengan awalnya berdasarkan `phase_started_id`. Tangani lebih dari satu fase yang terbuka, fase yang tidak ada di `phases`, dan fase yang tercantum tetapi tidak pernah dimulai, bahkan dalam eksekusi yang selesai. Setiap fase yang dimulai juga berakhir, sebelum `workflow_run.status_ended` eksekusi. |
| `workflow_run.status_ended`                              | Eksekusi berakhir. Selalu menjadi event terakhir dari event `workflow_run.*` eksekusi. Menyertakan `result`.                                                                                                                                                                                                                                                                                                                                                                                                                               | Baca `result` (tabel berikutnya). Agen kemudian mendapat giliran untuk membaca bagaimana eksekusi berakhir. Pada anggaran, atau saat thread utama menunggu klien Anda, giliran itu datang belakangan. Setelah interupsi, giliran itu mungkin tidak datang: kirim `user.message`, atau baca `result` sendiri. Setelah pengarsipan atau penghentian, giliran itu tidak datang.                                                                                           |
| `workflow_run.error`                                     | Server melaporkan error dari sebuah eksekusi, atau permulaan yang ditolaknya. Eksekusi yang berakhir dengan `error` mendapat event ini, dengan error yang sama, sebelum `workflow_run.status_ended`-nya. Menyertakan `error`: sebuah `type` dan `message` yang aman untuk dicatat di log. `workflow_run_id` bernilai `null` ketika tidak ada eksekusi yang dibuat.                                                                                                                                                                         | Catat di log, dan jangan anggap sebagai akhir eksekusi. Jika `workflow_run_id` bernilai `null`, tidak ada eksekusi yang dimulai. Jika tidak, terus lacak eksekusi hingga `workflow_run.status_ended`-nya.                                                                                                                                                                                                                                                              |

| `result`                            | Arti                                                                                                                                                                                                                                                                                                                                                                           |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `{"type": "completed"}`             | Workflow selesai berjalan. Hasil ini tidak menyebutkan apakah pekerjaan tersebut berhasil. Eksekusi dapat berakhir `completed` meskipun pekerjaan di thread-nya gagal, atau sebuah thread tidak dapat dibuat. Untuk menemukan pekerjaan yang gagal, baca event dari setiap [thread eksekusi](https://platform.claude.com/docs/id/managed-agents/workflow-runs#a-runs-threads). |
| `{"type": "stopped"}`               | Agen menghentikan eksekusi, atau sesi diarsipkan. Event ini tidak menyebutkan yang mana, dan rilis mendatang mungkin menambahkan penyebab lain.                                                                                                                                                                                                                                |
| `error` dengan `timeout_error`      | Eksekusi mencapai masa hidupnya: 24 jam secara default, atau yang ditetapkan agen.                                                                                                                                                                                                                                                                                             |
| `error` dengan `program_error`      | Workflow gagal. Kodenya gagal, atau melanggar aturan untuk workflow, selain batas. Atau salah satu thread eksekusi gagal, atau tidak dapat dibuat, dan workflow membiarkan hal itu mengakhiri eksekusi.                                                                                                                                                                        |
| `error` dengan `thread_limit_error` | Eksekusi melampaui [batas jumlah agen yang dimulai oleh workflow](https://platform.claude.com/docs/id/managed-agents/workflow-runs#budgets-and-limits).                                                                                                                                                                                                                        |
| `error` dengan `unknown_error`      | Server tidak dapat melanjutkan eksekusi, atau eksekusi melampaui salah satu batas lain server untuk workflow.                                                                                                                                                                                                                                                                  |

Hasil error terlihat seperti `{"type": "error", "error": {"type": "timeout_error", "message": "..."}}`, di mana `message` aman untuk dicatat di log. Perlakukan `result.type` yang tidak dikenali sebagai eksekusi yang berakhir dengan cara lain, dan `error.type` yang tidak dikenali sebagai error. Ketika sesuatu yang menjadi ketergantungan sesi gagal, seperti model, server MCP, kredensial, atau penagihan, aliran thread yang gagal mendapat `session.error`. Hal itu tidak mengakhiri eksekusi dengan sendirinya. Tetapi jika hal itu membuat salah satu thread eksekusi gagal, dan workflow membiarkan hal itu mengakhiri eksekusi, eksekusi berakhir dengan `program_error`.

Misalnya, Anda bertanya kepada [agen peninjau kontrak](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#turn-on-dynamic-workflows) mana dari 300 kontrak yang memiliki klausul perubahan kendali, dan agen memulai sebuah eksekusi:

1. `workflow_run.created` menamai eksekusi "Find change-of-control clauses" dan mencantumkan fase "Read the contracts" dan "Reconcile the findings" di `phases`. Kemudian `workflow_run.status_running` menyusul.
2. Event fase menandai setiap fase, dan setiap thread yang dibuat eksekusi mengirim `session.thread_created` dengan `workflow_run_id` eksekusi.
3. `workflow_run.status_ended` tiba dengan `result: {"type": "completed"}`.
4. Agen menjawab, "41 dari 300 kontrak memilikinya," dan `session.status_idle` tiba dengan `end_turn`.

Event pertama eksekusi mencantumkan fase-fasenya:

```json
{
  "type": "workflow_run.created",
  "id": "sevt_01abc...",
  "workflow_run_id": "wrun_01J8XkN5uT3vHpLqRfWdY2",
  "name": "Find change-of-control clauses",
  "description": "Reads each contract and lists those that have the clause.",
  "phases": [
    {
      "id": "wrph_01Kd3a1f3",
      "name": "Read the contracts",
      "description": "Reads each contract for the clause."
    },
    { "id": "wrph_01Kd3b7c9", "name": "Reconcile the findings", "description": null }
  ],
  "processed_at": "2026-10-09T14:01:45Z"
}
```

Setiap event fase menyebutkan fasenya berdasarkan `workflow_run_phase_id`. Itu adalah sebuah `id` di `phases`, tetapi API tidak menjaminnya:

```json
{
  "type": "workflow_run.phase_started",
  "id": "sevt_01def...",
  "workflow_run_id": "wrun_01J8XkN5uT3vHpLqRfWdY2",
  "workflow_run_phase_id": "wrph_01Kd3a1f3",
  "processed_at": "2026-10-09T14:01:46Z"
}
```

Event terakhir eksekusi melaporkan bagaimana eksekusi berakhir:

```json
{
  "type": "workflow_run.status_ended",
  "id": "sevt_01ghi...",
  "workflow_run_id": "wrun_01J8XkN5uT3vHpLqRfWdY2",
  "result": { "type": "completed" },
  "processed_at": "2026-10-09T14:09:12Z"
}
```

## Thread sebuah eksekusi

Setiap agen dalam sebuah eksekusi bekerja di [thread sesi](https://platform.claude.com/docs/id/managed-agents/session-threads) miliknya sendiri, yang dibuat server sesuai kebutuhan workflow. Anda dapat mencantumkan, membaca, dan melakukan streaming thread eksekusi seperti thread anak mana pun, dan menjawab panggilan alatnya dari aliran utama. Untuk menghentikannya, minta agen menghentikan eksekusi (lihat [Menginterupsi sesi dengan eksekusi yang terbuka](https://platform.claude.com/docs/id/managed-agents/workflow-runs#interrupt-a-session-with-runs-open)). Anda tidak dapat menghentikan satu thread berdasarkan ID-nya, atau mengarsipkannya selama eksekusinya terbuka.

* **Pengelompokan:** Thread eksekusi membawa `workflow_run_id` eksekusi, begitu pula event `session.thread_created` yang mengumumkannya. Thread lain, dan event `session.thread_created` yang mengumumkannya, memiliki `workflow_run_id` yang diatur ke `null`.
* **Agen:** `agent` menunjukkan agen yang dijalankan thread. Untuk agen yang Anda cantumkan di [`multiagent.workflows.predefined_agents`](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#turn-on-dynamic-workflows), `agent` memiliki `id` dan `version` agen tersebut, seperti pada thread subagen yang Anda cantumkan. Untuk agen yang didefinisikan workflow (agen inline), `agent` memiliki `type` `inline` dan tanpa `id` atau `version`. Agen ini memiliki prompt sistem yang ditulis workflow, bukan milik agen sesi. Agen ini juga memiliki nama dan deskripsi yang diberikan workflow; server menetapkan nama jika workflow tidak memberikannya. Agen ini menggunakan model agen sesi, yaitu agen yang dijalankan sesi. Alat, server MCP, dan skill-nya adalah subset dari milik agen sesi. Agen ini mendapatkan semuanya, tetapi API tidak menjaminnya. Alat-alatnya mempertahankan kebijakan izinnya.
* **Apa yang dibagikan thread:** Thread eksekusi bekerja di sandbox sesi, sehingga setiap thread bekerja dengan file yang sama. Itu termasuk file dari memory store yang di-mount sesi. Agen yang didefinisikan workflow menggunakan server MCP-nya dengan kredensial yang di-resolve sesi untuknya. Setiap thread memiliki riwayat percakapannya sendiri.
* **Event:** Event `session.thread_created`, `session.thread_status_running`, `session.thread_status_idle`, dan `session.thread_status_terminated` dari thread eksekusi juga tiba di aliran utama (lihat [Event eksekusi](https://platform.claude.com/docs/id/managed-agents/workflow-runs#run-events)). Event pesannya tetap di alirannya sendiri. Webhook thread-nya dikirim seperti untuk thread anak mana pun. Untuk apa yang dicatat aliran thread itu sendiri, lihat [Event thread sesi](https://platform.claude.com/docs/id/managed-agents/session-threads#session-thread-events).
* **Fase:** Tidak ada event atau field yang menyebutkan di fase mana sebuah thread bekerja, dan thread dari satu eksekusi dapat memiliki `agent_name` yang sama. Ikuti kemajuan eksekusi melalui event fasenya, dan bedakan thread-nya berdasarkan `session_thread_id`.
* **Batas thread:** Thread eksekusi dikecualikan dari [batas thread anak](https://platform.claude.com/docs/id/managed-agents/session-threads#primary-thread-and-session-threads) sesi.
* **Memulai eksekusi:** Hanya agen di thread utama sesi yang memulai eksekusi. Agen yang bekerja di thread eksekusi tidak dapat memulai eksekusinya sendiri, sehingga eksekusi tidak bersarang.
* **Pengarsipan:** Server mengarsipkan setiap thread paling lambat pada akhir eksekusinya. Server dapat mengarsipkannya lebih awal, setelah thread mengembalikan hasilnya atau eksekusi selesai dengannya. Jika thread masih berjalan atau menunggu klien Anda pada saat itu, server menghentikannya terlebih dahulu. Thread yang diarsipkan tetap ada di daftar thread, dengan status `terminated`. Anda tidak perlu mengarsipkan thread eksekusi sendiri. Selama eksekusi terbuka, permintaan untuk mengarsipkan thread yang belum diarsipkan server mengembalikan 400 dengan `error.details.error_code: "workflow_run_open"`.
* **Visibilitas:** Anda tidak melihat kode workflow, tetapi Anda dapat meminta workflow tersebut kepada agen, seperti yang dijelaskan tip setelah daftar ini. Anda juga tidak melihat panggilan alat yang dilakukan agen untuk memulai dan mengelola eksekusi, atau hasil yang dikembalikan setiap thread ke workflow.

<Tip>
  Anda dapat meminta kepada agen workflow yang ditulisnya untuk permintaan Anda. Tunggu hingga eksekusi berakhir dan sesi berstatus `idle`. Kemudian kirim `user.message` yang meminta agen mencetak workflow yang digunakannya untuk memulai eksekusi, kata demi kata, dan tidak memulai eksekusi lain.

  ```text wrap
  Print the workflow that you started the run with, word for word, in one code block. Do not start another run.
  ```
</Tip>

## Mengetahui kapan pekerjaan selesai

Selama eksekusi berjalan, sesi diharapkan tetap `running`, bahkan ketika tidak ada thread-nya yang bekerja. Sesi menjadi `idle` dengan `requires_action` ketika tidak ada thread yang bekerja dan sebuah thread menunggu klien Anda. Status idle saja tidak berarti pekerjaan selesai. Pekerjaan selesai ketika kedua hal berikut benar:

1. Setiap eksekusi yang Anda lihat dibuat memiliki `workflow_run.status_ended`-nya.
2. Setelah itu, `session.status_idle` tiba dengan `stop_reason` `end_turn`, dan bukan permintaan Anda sendiri, seperti interupsi, yang menyebabkannya. Setelah Anda menginterupsi, hitung hanya idle yang datang setelah `user.message` atau `user.define_outcome` Anda berikutnya.

* **Eksekusi yang dijeda:** Eksekusi yang dijeda tidak membuat sesi tetap `running`, sehingga sesi dapat menjadi idle selagi eksekusi masih terbuka. Pada anggaran, misalnya, sesi menjadi idle dengan `budget_reached`. Pekerjaan belum selesai hingga eksekusi berakhir.
* **Eksekusi lain:** Agen dapat memulai eksekusi baru ketika membaca sebuah hasil, jadi periksa lagi.
* **Outcome:** Jika Anda [mendefinisikan outcome](https://platform.claude.com/docs/id/managed-agents/define-outcomes), tidak ada evaluasi yang dimulai selama eksekusi terbuka, baik sedang berjalan maupun idle. Giliran di mana agen membaca hasil eksekusi dapat memulai evaluasi.
* **`retries_exhausted`:** Giliran agen gagal karena error: percobaan ulang habis, atau error tidak dapat dicoba ulang, seperti kegagalan penagihan. Sebuah eksekusi mungkin masih berjalan ketika idle ini datang. Jika sebuah eksekusi berakhir dan agen belum membaca hasilnya, server memulai giliran baru tanpa input dari Anda. Sesi kembali `running`, jadi tunggu idle berikutnya. Jika sesi tetap idle, baca `session.error` yang datang sebelumnya dan perbaiki penyebabnya. Kemudian kirim `user.message`, atau baca `result` setiap eksekusi sendiri.

## Mengikuti eksekusi

Contoh ini mengikuti sesi dari pesan Anda hingga jawaban agen. Contoh ini membuka aliran dan mengirim pesan. Kemudian contoh ini melakukan hal-hal berikut:

* **Melacak setiap eksekusi** dari `workflow_run.created` hingga `workflow_run.status_ended`-nya, dan mencetak setiap fase saat dimulai.
* **Menjawab panggilan alat kustom** ketika setiap `agent.custom_tool_use` tiba, karena thread eksekusi dapat menunggu klien Anda selagi sesi tetap `running`. Jika alat agen Anda [meminta konfirmasi](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#tool-confirmation), tambahkan cabang yang menjawab setiap `agent.tool_use` atau `agent.mcp_tool_use` yang `evaluated_permission`-nya adalah `ask`. Contoh ini tidak memilikinya, karena cabang yang mengizinkan setiap panggilan akan mengubah `always_ask` menjadi selalu mengizinkan.
* **Berhenti** ketika [pekerjaan selesai](https://platform.claude.com/docs/id/managed-agents/workflow-runs#know-when-the-work-is-done): tidak ada eksekusi yang terbuka, dan sesi menjadi idle dengan `end_turn`. Contoh ini juga berhenti jika sesi dihentikan. Pada idle dengan alasan berhenti lain selain `requires_action`, seperti `budget_reached`, `retries_exhausted`, atau `refusal`, contoh ini mencetak alasannya dan berhenti, jadi tangani hal-hal tersebut dalam kode Anda sendiri. Contoh ini berhenti pada `retries_exhausted` bahkan ketika server akan memulai giliran baru dengan sendirinya. Contoh ini terus menunggu pada `requires_action`, dan pada `end_turn` selama sebuah eksekusi terbuka.

<CodeGroup>
  ```bash cURL
  # Workflow ini tidak cocok diterjemahkan menjadi perintah shell sekali jalan.
  # Gunakan salah satu contoh SDK di grup kode ini sebagai gantinya.
  ```

  ```bash CLI
  # Workflow ini tidak cocok diterjemahkan menjadi perintah shell sekali jalan.
  # Gunakan salah satu contoh SDK di grup kode ini sebagai gantinya.
  ```

  ```python Python
  open_runs: dict[str, str] = {}  # workflow_run_id -> run name
  phase_names: dict[tuple[str, str], str] = {}  # (run ID, phase ID) -> phase name

  # Buka stream terlebih dahulu, lalu kirim pesan pengguna
  with client.beta.sessions.events.stream(session_id) as stream:
      client.beta.sessions.events.send(
          session_id,
          events=[
              {
                  "type": "user.message",
                  "content": [
                      {
                          "type": "text",
                          "text": "Which contracts in /contracts have a change-of-control clause?",
                      },
                  ],
              },
          ],
      )

      for event in stream:
          match event.type:
              case "workflow_run.created":
                  open_runs[event.workflow_run_id] = event.name
                  for phase in event.phases:
                      phase_names[event.workflow_run_id, phase.id] = phase.name
                  print(f"Run started: {event.name}")
              case "workflow_run.phase_started":
                  phase_id = event.workflow_run_phase_id
                  key = (event.workflow_run_id, phase_id)
                  print(f"  Phase: {phase_names.get(key, phase_id)}")
              case "workflow_run.status_ended":
                  name = open_runs.pop(event.workflow_run_id, event.workflow_run_id)
                  print(f"Run ended: {name} ({event.result.type})")
              case "agent.custom_tool_use":
                  # Jawab saat event tiba. Thread sebuah eksekusi dapat menunggu
                  # klien Anda sementara sesi tetap berjalan.
                  result = call_tool(event.name, event.input)
                  try:
                      client.beta.sessions.events.send(
                          session_id,
                          events=[
                              {
                                  "type": "user.custom_tool_result",
                                  "custom_tool_use_id": event.id,
                                  "content": [{"type": "text", "text": result}],
                              },
                          ],
                      )
                  except anthropic.BadRequestError as error:
                      # Server menolak hasil yang datang terlambat, setelah server
                      # mengarsipkan thread panggilan tersebut. Terus ikuti eksekusinya.
                      print(f"  Answer to {event.name} refused: {error.message}")
              case "session.status_idle":
                  # Selesai saat setiap eksekusi telah berakhir dan agen telah menyelesaikan gilirannya
                  if not open_runs and event.stop_reason.type == "end_turn":
                      break
                  # Status idle dengan requires_action menunggu klien Anda, jadi terus baca.
                  # Pada alasan berhenti lainnya, cetak alasannya lalu berhenti.
                  if event.stop_reason.type not in ("end_turn", "requires_action"):
                      print(f"Session idle: {event.stop_reason.type}")
                      break
              case "session.status_terminated":
                  break
  ```

  ```typescript TypeScript
  const openRuns = new Map<string, string>(); // workflow_run_id -> run name
  const phaseNames = new Map<string, string>(); // "run ID:phase ID" -> phase name

  // Buka stream terlebih dahulu, lalu kirim pesan pengguna
  const stream = await client.beta.sessions.events.stream(sessionId);
  await client.beta.sessions.events.send(sessionId, {
    events: [
      {
        type: "user.message",
        content: [{ type: "text", text: "Which contracts in /contracts have a change-of-control clause?" }],
      },
    ],
  });

  events: for await (const event of stream) {
    switch (event.type) {
      case "workflow_run.created":
        openRuns.set(event.workflow_run_id, event.name);
        for (const phase of event.phases) {
          phaseNames.set(`${event.workflow_run_id}:${phase.id}`, phase.name);
        }
        console.log(`Run started: ${event.name}`);
        break;
      case "workflow_run.phase_started": {
        const phaseId = event.workflow_run_phase_id;
        const phaseName = phaseNames.get(`${event.workflow_run_id}:${phaseId}`);
        console.log(`  Phase: ${phaseName ?? phaseId}`);
        break;
      }
      case "workflow_run.status_ended": {
        const name = openRuns.get(event.workflow_run_id) ?? event.workflow_run_id;
        openRuns.delete(event.workflow_run_id);
        console.log(`Run ended: ${name} (${event.result.type})`);
        break;
      }
      case "agent.custom_tool_use": {
        // Jawab saat event tiba. Thread sebuah eksekusi dapat menunggu
        // klien Anda sementara sesi tetap berjalan.
        const result = await callTool(event.name, event.input);
        try {
          await client.beta.sessions.events.send(sessionId, {
            events: [
              {
                type: "user.custom_tool_result",
                custom_tool_use_id: event.id,
                content: [{ type: "text", text: result }],
              },
            ],
          });
        } catch (error) {
          // Server menolak hasil yang datang terlambat, setelah server
          // mengarsipkan thread panggilan tersebut. Terus ikuti eksekusinya.
          if (!(error instanceof Anthropic.BadRequestError)) throw error;
          console.log(`  Answer to ${event.name} refused: ${error.message}`);
        }
        break;
      }
      case "session.status_idle": {
        // Selesai saat setiap eksekusi telah berakhir dan agen telah menyelesaikan gilirannya
        const reason = event.stop_reason.type;
        if (openRuns.size === 0 && reason === "end_turn") {
          break events;
        }
        // Status idle dengan requires_action menunggu klien Anda, jadi terus baca.
        // Pada stop reason lainnya, cetak lalu berhenti.
        if (reason !== "end_turn" && reason !== "requires_action") {
          console.log(`Session idle: ${reason}`);
          break events;
        }
        break;
      }
      case "session.status_terminated":
        break events;
    }
  }
  ```

  ```csharp C#
  var openRuns = new Dictionary<string, string>(); // workflow_run_id -> run name
  var phaseNames = new Dictionary<(string, string), string>(); // (run ID, phase ID) -> phase name

  // Buka stream terlebih dahulu, lalu kirim pesan pengguna. Panggilan raw-response
  // membuka stream sekarang. Panggilan biasa akan menunggu pembacaan pertama.
  using var stream = await client.Beta.Sessions.Events.WithRawResponse.StreamStreaming(sessionId);
  await client.Beta.Sessions.Events.Send(sessionId, new()
  {
      Events =
      [
          new BetaManagedAgentsUserMessageEventParams
          {
              Type = BetaManagedAgentsUserMessageEventParamsType.UserMessage,
              Content =
              [
                  new BetaManagedAgentsTextBlock
                  {
                      Type = BetaManagedAgentsTextBlockType.Text,
                      Text = "Which contracts in /contracts have a change-of-control clause?",
                  },
              ],
          },
      ],
  });

  await foreach (var streamEvent in stream.Enumerate())
  {
      if (streamEvent.Value is BetaManagedAgentsWorkflowRunCreatedEvent created)
      {
          openRuns[created.WorkflowRunID] = created.Name;
          foreach (var listed in created.Phases)
          {
              phaseNames[(created.WorkflowRunID, listed.ID)] = listed.Name;
          }
          Console.WriteLine($"Run started: {created.Name}");
      }
      else if (streamEvent.Value is BetaManagedAgentsWorkflowRunPhaseStartedEvent phase)
      {
          var phaseId = phase.WorkflowRunPhaseID;
          var key = (phase.WorkflowRunID, phaseId);
          Console.WriteLine($"  Phase: {phaseNames.GetValueOrDefault(key, phaseId)}");
      }
      else if (streamEvent.Value is BetaManagedAgentsWorkflowRunStatusEndedEvent ended)
      {
          var name = openRuns.GetValueOrDefault(ended.WorkflowRunID, ended.WorkflowRunID);
          openRuns.Remove(ended.WorkflowRunID);
          var outcome = ended.Result.Value switch
          {
              BetaManagedAgentsWorkflowRunResultCompleted => "completed",
              BetaManagedAgentsWorkflowRunResultStopped => "stopped",
              BetaManagedAgentsWorkflowRunResultError => "error",
              _ => "ended",
          };
          Console.WriteLine($"Run ended: {name} ({outcome})");
      }
      else if (streamEvent.Value is BetaManagedAgentsAgentCustomToolUseEvent toolUse)
      {
          // Jawab saat event tiba. Thread sebuah eksekusi dapat menunggu
          // klien Anda selagi sesi tetap berjalan.
          var result = await CallTool(toolUse.Name, toolUse.Input);
          try
          {
              await client.Beta.Sessions.Events.Send(sessionId, new()
              {
                  Events =
                  [
                      new BetaManagedAgentsUserCustomToolResultEventParams
                      {
                          Type = BetaManagedAgentsUserCustomToolResultEventParamsType.UserCustomToolResult,
                          CustomToolUseID = toolUse.ID,
                          Content =
                          [
                              new BetaManagedAgentsTextBlock
                              {
                                  Type = BetaManagedAgentsTextBlockType.Text,
                                  Text = result,
                              },
                          ],
                      },
                  ],
              });
          }
          catch (AnthropicBadRequestException error)
          {
              // Server menolak hasil yang datang terlambat, setelah server
              // mengarsipkan thread panggilan tersebut. Terus ikuti eksekusinya.
              Console.WriteLine($"  Answer to {toolUse.Name} refused: {error.Message}");
          }
      }
      else if (streamEvent.Value is BetaManagedAgentsSessionStatusIdleEvent idle)
      {
          // Selesai saat setiap eksekusi telah berakhir dan agen telah menyelesaikan gilirannya
          var finished = idle.StopReason?.Value is BetaManagedAgentsSessionEndTurn;
          if (openRuns.Count == 0 && finished)
          {
              break;
          }
          // Status idle dengan requires_action menunggu klien Anda, jadi terus baca.
          // Untuk stop reason lainnya, cetak lalu berhenti.
          if (!finished && idle.StopReason?.Value is not BetaManagedAgentsSessionRequiresAction)
          {
              var reason = idle.StopReason?.Json.GetProperty("type").GetString();
              Console.WriteLine($"Session idle: {reason}");
              break;
          }
      }
      else if (streamEvent.Value is BetaManagedAgentsSessionStatusTerminatedEvent)
      {
          break;
      }
  }
  ```

  ```go Go
  	openRuns := map[string]string{}   // workflow_run_id -> run name
  	phaseNames := map[[2]string]string{} // {run ID, phase ID} -> phase name

  	// Buka stream terlebih dahulu, lalu kirim pesan pengguna
  	stream := client.Beta.Sessions.Events.StreamEvents(ctx, sessionID, anthropic.BetaSessionEventStreamParams{})
  	defer stream.Close()

  	if _, err := client.Beta.Sessions.Events.Send(ctx, sessionID, anthropic.BetaSessionEventSendParams{
  		Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  			OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
  				Type: anthropic.BetaManagedAgentsUserMessageEventParamsTypeUserMessage,
  				Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{
  					OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  						Type: anthropic.BetaManagedAgentsTextBlockTypeText,
  						Text: "Which contracts in /contracts have a change-of-control clause?",
  					},
  				}},
  			},
  		}},
  	}); err != nil {
  		panic(err)
  	}

  events:
  	for stream.Next() {
  		switch event := stream.Current().AsAny().(type) {
  		case anthropic.BetaManagedAgentsWorkflowRunCreatedEvent:
  			openRuns[event.WorkflowRunID] = event.Name
  			for _, phase := range event.Phases {
  				phaseNames[[2]string{event.WorkflowRunID, phase.ID}] = phase.Name
  			}
  			fmt.Printf("Run started: %s\n", event.Name)
  		case anthropic.BetaManagedAgentsWorkflowRunPhaseStartedEvent:
  			phaseName, ok := phaseNames[[2]string{event.WorkflowRunID, event.WorkflowRunPhaseID}]
  			if !ok {
  				phaseName = event.WorkflowRunPhaseID
  			}
  			fmt.Printf("  Phase: %s\n", phaseName)
  		case anthropic.BetaManagedAgentsWorkflowRunStatusEndedEvent:
  			name, ok := openRuns[event.WorkflowRunID]
  			if !ok {
  				name = event.WorkflowRunID
  			}
  			delete(openRuns, event.WorkflowRunID)
  			fmt.Printf("Run ended: %s (%s)\n", name, event.Result.Type)
  		case anthropic.BetaManagedAgentsAgentCustomToolUseEvent:
  			// Jawab saat event tiba. Thread sebuah eksekusi dapat menunggu
  			// klien Anda selagi sesi tetap berjalan.
  			result := callTool(event.Name, event.Input)
  			if _, err := client.Beta.Sessions.Events.Send(ctx, sessionID, anthropic.BetaSessionEventSendParams{
  				Events: []anthropic.BetaManagedAgentsEventParamsUnion{{
  					OfUserCustomToolResult: &anthropic.BetaManagedAgentsUserCustomToolResultEventParams{
  						Type:            anthropic.BetaManagedAgentsUserCustomToolResultEventParamsTypeUserCustomToolResult,
  						CustomToolUseID: event.ID,
  						Content: []anthropic.BetaManagedAgentsUserCustomToolResultEventParamsContentUnion{{
  							OfText: &anthropic.BetaManagedAgentsTextBlockParam{
  								Type: anthropic.BetaManagedAgentsTextBlockTypeText,
  								Text: result,
  							},
  						}},
  					},
  				}},
  			}); err != nil {
  				// Server menolak hasil yang datang terlambat, setelah server
  				// mengarsipkan thread panggilan tersebut. Terus ikuti eksekusinya.
  				var apiErr *anthropic.Error
  				if !errors.As(err, &apiErr) || apiErr.StatusCode != http.StatusBadRequest {
  					panic(err)
  				}
  				fmt.Printf("  Answer to %s refused: %v\n", event.Name, err)
  			}
  		case anthropic.BetaManagedAgentsSessionStatusIdleEvent:
  			// Selesai saat setiap eksekusi telah berakhir dan agen telah menyelesaikan gilirannya
  			switch event.StopReason.AsAny().(type) {
  			case anthropic.BetaManagedAgentsSessionEndTurn:
  				if len(openRuns) == 0 {
  					break events
  				}
  			// Status idle dengan requires_action menunggu klien Anda, jadi terus baca.
  			// Untuk stop reason lainnya, cetak lalu berhenti.
  			case anthropic.BetaManagedAgentsSessionRequiresAction:
  			default:
  				fmt.Printf("Session idle: %s\n", event.StopReason.Type)
  				break events
  			}
  		case anthropic.BetaManagedAgentsSessionStatusTerminatedEvent:
  			break events
  		}
  	}
  	if err := stream.Err(); err != nil {
  		panic(err)
  	}
  ```

  ```java Java
  var openRuns = new HashMap<String, String>(); // workflow_run_id -> run name
  var phaseNames = new HashMap<String, String>(); // "run ID:phase ID" -> phase name

  // Buka stream terlebih dahulu, lalu kirim pesan pengguna
  try (var stream = client.beta().sessions().events().streamStreaming(sessionId)) {
      client.beta().sessions().events().send(
          sessionId,
          EventSendParams.builder()
              .addEvent(BetaManagedAgentsUserMessageEventParams.builder()
                  .type(BetaManagedAgentsUserMessageEventParams.Type.USER_MESSAGE)
                  .addTextContent("Which contracts in /contracts have a change-of-control clause?")
                  .build())
              .build()
      );

      Iterable<BetaManagedAgentsStreamSessionEvents> events = stream.stream()::iterator;
      events:
      for (var event : events) {
          switch (event.type().value()) {
              case WORKFLOW_RUN_CREATED -> {
                  var created = event.asWorkflowRunCreated();
                  openRuns.put(created.workflowRunId(), created.name());
                  created.phases().forEach(phase ->
                      phaseNames.put(created.workflowRunId() + ":" + phase.id(), phase.name()));
                  IO.println("Run started: " + created.name());
              }
              case WORKFLOW_RUN_PHASE_STARTED -> {
                  var started = event.asWorkflowRunPhaseStarted();
                  var phaseId = started.workflowRunPhaseId();
                  var key = started.workflowRunId() + ":" + phaseId;
                  IO.println("  Phase: " + phaseNames.getOrDefault(key, phaseId));
              }
              case WORKFLOW_RUN_STATUS_ENDED -> {
                  var ended = event.asWorkflowRunStatusEnded();
                  var name = openRuns.getOrDefault(ended.workflowRunId(), ended.workflowRunId());
                  openRuns.remove(ended.workflowRunId());
                  var result = ended.result();
                  var outcome = result.isCompleted() ? "completed"
                      : result.isStopped() ? "stopped"
                      : result.isError() ? "error"
                      : "ended";
                  IO.println("Run ended: " + name + " (" + outcome + ")");
              }
              case AGENT_CUSTOM_TOOL_USE -> {
                  // Jawab saat event tiba. Thread sebuah eksekusi dapat menunggu
                  // klien Anda sementara sesi tetap berjalan.
                  var toolUse = event.asAgentCustomToolUse();
                  var result = callTool(toolUse.name(), toolUse.input());
                  try {
                      client.beta().sessions().events().send(
                          sessionId,
                          EventSendParams.builder()
                              .addEvent(BetaManagedAgentsUserCustomToolResultEventParams.builder()
                                  .type(BetaManagedAgentsUserCustomToolResultEventParams.Type.USER_CUSTOM_TOOL_RESULT)
                                  .customToolUseId(toolUse.id())
                                  .addTextContent(result)
                                  .build())
                              .build());
                  } catch (BadRequestException e) {
                      // Server menolak hasil yang datang terlambat, setelah server
                      // mengarsipkan thread panggilan tersebut. Terus ikuti eksekusinya.
                      IO.println("  Answer to " + toolUse.name() + " refused: " + e.getMessage());
                  }
              }
              case SESSION_STATUS_IDLE -> {
                  // Selesai saat setiap eksekusi telah berakhir dan agen telah menyelesaikan gilirannya
                  var stopReason = event.asSessionStatusIdle().stopReason();
                  if (openRuns.isEmpty() && stopReason.isEndTurn()) {
                      break events;
                  }
                  // Status idle dengan requires_action menunggu klien Anda, jadi terus baca.
                  // Pada alasan berhenti lainnya, cetak alasannya lalu berhenti.
                  if (!stopReason.isEndTurn() && !stopReason.isRequiresAction()) {
                      IO.println("Session idle: " + stopReason.type().asString());
                      break events;
                  }
              }
              case SESSION_STATUS_TERMINATED -> {
                  break events;
              }
              default -> {}
          }
      }
  }
  ```

  ```php PHP
  $openRuns = []; // workflow_run_id => run name
  $phaseNames = []; // run ID => [phase ID => phase name]

  // Buka stream terlebih dahulu, lalu kirim pesan pengguna
  $stream = $client->beta->sessions->events->streamStream($sessionId);
  $client->beta->sessions->events->send(
      $sessionId,
      events: [
          [
              'type' => 'user.message',
              'content' => [
                  ['type' => 'text', 'text' => 'Which contracts in /contracts have a change-of-control clause?'],
              ],
          ],
      ],
  );

  foreach ($stream as $event) {
      switch (true) {
          case $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsWorkflowRunCreatedEvent:
              $openRuns[$event->workflowRunID] = $event->name;
              foreach ($event->phases as $phase) {
                  $phaseNames[$event->workflowRunID][$phase->id] = $phase->name;
              }
              echo "Run started: {$event->name}", PHP_EOL;
              break;
          case $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsWorkflowRunPhaseStartedEvent:
              $phaseId = $event->workflowRunPhaseID;
              echo '  Phase: ', $phaseNames[$event->workflowRunID][$phaseId] ?? $phaseId, PHP_EOL;
              break;
          case $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsWorkflowRunStatusEndedEvent:
              $name = $openRuns[$event->workflowRunID] ?? $event->workflowRunID;
              unset($openRuns[$event->workflowRunID]);
              echo "Run ended: {$name} ({$event->result->type})", PHP_EOL;
              break;
          case $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsAgentCustomToolUseEvent:
              // Jawab saat event tiba. Thread sebuah eksekusi dapat menunggu
              // klien Anda sementara sesi tetap berjalan.
              $result = callTool($event->name, $event->input);
              try {
                  $client->beta->sessions->events->send(
                      $sessionId,
                      events: [
                          [
                              'type' => 'user.custom_tool_result',
                              'custom_tool_use_id' => $event->id,
                              'content' => [['type' => 'text', 'text' => $result]],
                          ],
                      ],
                  );
              } catch (\Anthropic\Core\Exceptions\BadRequestException $error) {
                  // Server menolak hasil yang datang terlambat, setelah server
                  // mengarsipkan thread panggilan tersebut. Terus ikuti eksekusinya.
                  echo "  Answer to {$event->name} refused: {$error->getMessage()}", PHP_EOL;
              }
              break;
          case $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsSessionStatusIdleEvent:
              // Selesai saat setiap eksekusi telah berakhir dan agen telah menyelesaikan gilirannya
              $finished = $event->stopReason->type === 'end_turn';
              if (!$openRuns && $finished) {
                  break 2;
              }
              // Status idle dengan requires_action menunggu klien Anda, jadi terus baca.
              // Pada stop reason lainnya, cetak lalu berhenti.
              if (!$finished && $event->stopReason->type !== 'requires_action') {
                  echo "Session idle: {$event->stopReason->type}", PHP_EOL;
                  break 2;
              }
              break;
          case $event instanceof \Anthropic\Beta\Sessions\Events\ManagedAgentsSessionStatusTerminatedEvent:
              break 2;
      }
  }
  $stream->close();
  ```

  ```ruby Ruby
  open_runs = {} # workflow_run_id => run name
  phase_names = {} # [run ID, phase ID] => phase name

  # Buka stream terlebih dahulu, lalu kirim pesan pengguna
  stream = client.beta.sessions.events.stream_events(session_id)

  client.beta.sessions.events.send_(
    session_id,
    events: [{
      type: "user.message",
      content: [{type: "text", text: "Which contracts in /contracts have a change-of-control clause?"}]
    }]
  )

  stream.each do |event|
    case event
    when Anthropic::Beta::Sessions::BetaManagedAgentsWorkflowRunCreatedEvent
      open_runs[event.workflow_run_id] = event.name
      event.phases.each { |phase| phase_names[[event.workflow_run_id, phase.id]] = phase.name }
      puts "Run started: #{event.name}"
    when Anthropic::Beta::Sessions::BetaManagedAgentsWorkflowRunPhaseStartedEvent
      phase_id = event.workflow_run_phase_id
      puts "  Phase: #{phase_names.fetch([event.workflow_run_id, phase_id], phase_id)}"
    when Anthropic::Beta::Sessions::BetaManagedAgentsWorkflowRunStatusEndedEvent
      name = open_runs.delete(event.workflow_run_id) || event.workflow_run_id
      puts "Run ended: #{name} (#{event.result.type})"
    when Anthropic::Beta::Sessions::BetaManagedAgentsAgentCustomToolUseEvent
      # Jawab saat event tiba. Thread sebuah eksekusi dapat menunggu
      # klien Anda sementara sesi tetap berjalan.
      result = call_tool.call(event.name, event.input)
      begin
        client.beta.sessions.events.send_(
          session_id,
          events: [{
            type: "user.custom_tool_result",
            custom_tool_use_id: event.id,
            content: [{type: "text", text: result}]
          }]
        )
      rescue Anthropic::Errors::BadRequestError => error
        # Server menolak hasil yang datang terlambat, setelah server mengarsipkan
        # thread panggilan tersebut. Terus ikuti eksekusinya.
        puts "  Answer to #{event.name} refused: #{error.message}"
      end
    when Anthropic::Beta::Sessions::BetaManagedAgentsSessionStatusIdleEvent
      reason = event.stop_reason.type.to_sym
      # Selesai ketika setiap eksekusi telah berakhir dan agen telah menyelesaikan gilirannya
      break if open_runs.empty? && reason == :end_turn
      # Status idle dengan requires_action menunggu klien Anda, jadi terus baca.
      # Pada alasan berhenti lainnya, cetak alasannya lalu berhenti.
      unless %i[end_turn requires_action].include?(reason)
        puts "Session idle: #{reason}"
        break
      end
    when Anthropic::Beta::Sessions::BetaManagedAgentsSessionStatusTerminatedEvent
      break
    end
  end
  ```
</CodeGroup>

## Menginterupsi sesi dengan eksekusi yang terbuka

Kirim [`user.interrupt`](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#interrupt-the-agent) tanpa `session_thread_id`, atau dengan ID thread utama. Ini menghentikan giliran agen. Ini tidak mengakhiri eksekusi apa pun. Eksekusi sesi mungkin dijeda atau terus berjalan, dan event-nya mungkin tidak menunjukkan yang mana. Masa hidup eksekusi yang dijeda terus berjalan, sehingga eksekusi dapat berakhir dengan `timeout_error` selama dijeda.

* **Panggilan alat yang menunggu:** Setelah interupsi, panggilan alat dari thread eksekusi mungkin masih menunggu klien Anda. Jawab masing-masing. Untuk membatalkan panggilan yang meminta konfirmasi, tolak panggilan tersebut. Untuk membatalkan panggilan alat kustom, kirim hasil dengan `is_error` diatur ke `true` dan teks di `content` yang menjelaskan alasannya. Selama sesi berstatus `idle` dengan `requires_action`, `user.message` mengembalikan 400, jadi jawab panggilan-panggilan tersebut terlebih dahulu.
* **Untuk menghentikan eksekusi:** Kirim `user.message` yang meminta agen menghentikan eksekusinya. Eksekusi yang dihentikan berakhir dengan `result` `{"type": "stopped"}`. Selama sesi berstatus `idle` dengan `budget_reached`, `user.message` mengembalikan 400 hingga Anda menaikkan atau menghapus anggaran. Menaikkan atau menghapusnya juga melanjutkan eksekusi yang dijeda oleh anggaran, kecuali jika interupsi juga menjedanya.
* **Untuk melanjutkan:** Kirim `user.message` yang meminta agen melanjutkan eksekusinya. Setelah interupsi, eksekusi mungkin menunggu pesan ini. Jika sesi berstatus `idle` dengan `budget_reached`, naikkan atau hapus anggaran terlebih dahulu.
* **Hasil eksekusi:** Eksekusi yang berakhir setelah interupsi tetap mengirim `workflow_run.status_ended`.

## Selama eksekusi terbuka

| Permintaan                                                        | Selama eksekusi terbuka                                                                                                                                                                                                                                                                                  | Apa yang harus dilakukan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Mengarsipkan atau menghapus sesi                                  | Mungkin mengembalikan 400 selama eksekusi terbuka, apa pun status sesinya. `error.details.error_code` dari error tersebut dapat berupa `"workflow_run_open"`. Mungkin juga berhasil.                                                                                                                     | Minta agen menghentikan eksekusinya, atau tunggu hingga setiap eksekusi berakhir. Eksekusi yang dijeda berakhir dengan sendirinya hanya ketika masa hidupnya habis. Kemudian kirim permintaan setelah sesi berstatus `idle`. Pengarsipan yang berhasil mengakhiri setiap eksekusi yang terbuka dengan `{"type": "stopped"}`. Setelah pengarsipan, `workflow_run.status_ended` eksekusi, dan `workflow_run.phase_ended` dari fase yang masih terbuka, tidak tiba di aliran. Cantumkan event sesi untuk membacanya. Setelah penghapusan yang berhasil, tidak ada event `workflow_run` yang melaporkan akhir eksekusi sesi.                                                                                                                                              |
| Mengarsipkan salah satu thread eksekusi                           | Mengembalikan 400 dengan `error.details.error_code: "workflow_run_open"` selama eksekusi terbuka, baik berjalan maupun idle, kecuali server telah mengarsipkan thread tersebut.                                                                                                                          | Tidak ada. Server mengarsipkan thread eksekusi.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Memperbarui `agent` sesi                                          | Mengembalikan 400 dengan `error.details.error_code: "workflow_run_open"` selama ada eksekusi yang terbuka, bahkan yang dijeda. Memperbarui agen yang mendasarinya tetap diterima, dan sesi menyimpan salinannya sendiri. Permintaan yang juga mengirim field lain, seperti `budget`, ditolak seluruhnya. | Tunggu hingga setiap eksekusi memiliki `workflow_run.status_ended`-nya, atau minta agen menghentikan eksekusinya.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Menjawab panggilan alat atau konfirmasi alat dari thread eksekusi | Diizinkan. Panggilan tersebut tiba di aliran utama, dan `session_thread_id`-nya menyebutkan thread-nya.                                                                                                                                                                                                  | Jawab segera setelah event tiba, dengan meneruskan `id` event sebagai `tool_use_id` atau `custom_tool_use_id`. Jangan menunggu `session.status_idle`: sesi dapat tetap `running` selagi thread lain dari eksekusi bekerja. Setelah server mengarsipkan thread, hasil alat untuk salah satu panggilannya tidak berpengaruh, dan dapat mengembalikan 400. Ketika hasil alat mengembalikan 400, temukan thread panggilan tersebut di daftar thread. Jika statusnya `terminated`, hasil tersebut datang terlambat, jadi abaikan. Kirim setiap hasil alat dalam permintaannya sendiri, karena server menolak seluruh permintaan ketika menolak salah satu event-nya. Konfirmasi alat yang datang terlambat mengembalikan 200, yang tidak berarti alat tersebut dijalankan. |

### Membangun ulang status eksekusi setelah Anda terhubung kembali

Bangun ulang status setiap eksekusi dari event sesi. Aliran tidak memutar ulang apa yang Anda lewatkan: koneksi baru hanya mengirimkan event yang dipancarkan setelah koneksi dibuka. Jadi cantumkan event dengan filter `types`, satu entri `types[]` untuk setiap jenis event, seperti di [Mendaftar event sebelumnya](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#list-past-events). Teruskan `next_page` setiap respons sebagai `page` hingga `next_page` bernilai `null` atau tidak ada. `workflow_run.created`, `workflow_run.status_running`, `workflow_run.status_idle`, dan `workflow_run.status_ended` memberikan status setiap eksekusi, kecuali bahwa eksekusi yang dijeda setelah interupsi mungkin masih tampil sebagai berjalan. `workflow_run.phase_started` dan `workflow_run.phase_ended` membangun ulang kemajuan. Eksekusi yang belum memiliki event status belum mulai dijalankan. Tidak ada endpoint yang mencantumkan eksekusi.

## Anggaran dan batas

Permintaan model dari sebuah eksekusi dihitung dalam [anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets). Eksekusi tidak memiliki harga tersendiri. Token yang digunakan agen-agennya ditagih seperti token sesi lainnya, sesuai tarif setiap model. Untuk semua biaya sesi, lihat [Harga Claude Managed Agents](https://platform.claude.com/docs/id/about-claude/pricing#claude-managed-agents-pricing).

* **Penggunaan satu eksekusi:** Cantumkan thread sesi dan jumlahkan hitungan token di `usage` dari thread dengan `workflow_run_id` eksekusi tersebut. Daftar ini menyertakan thread yang diarsipkan, yang statusnya `terminated`, sehingga thread dari eksekusi yang sudah selesai ikut dihitung. Teruskan `next_page` setiap respons sebagai `page` hingga `next_page` bernilai `null` atau tidak ada, dan lewati thread yang `usage`-nya bernilai `null`. Jika Anda menjumlahkan `list_cost` thread sebagai gantinya, totalnya tidak mencakup runtime sesi, dan setiap angka dibulatkan secara terpisah.
* **Pada anggaran:** Setiap eksekusi yang terbuka dijeda, dan sesi melaporkan `idle` dengan `budget_reached`, atau `requires_action` jika ada panggilan alat yang juga menunggu. Setiap thread menyelesaikan permintaan model yang sudah dimulainya, sehingga eksekusi dapat melampaui anggaran sebanyak satu permintaan untuk setiap thread yang bekerja. Menaikkan atau menghapus anggaran melanjutkan eksekusi yang dijedanya, kecuali jika interupsi juga menjeda eksekusi tersebut. Jika penggunaan sesi mencakup model tanpa harga daftar, hanya menghapus anggaran yang dapat melakukannya; lihat [Model tanpa harga daftar](https://platform.claude.com/docs/id/managed-agents/budgets#models-without-a-list-price).

| Batas                                                    | Nilai                                                       | Saat batas tercapai                                                                                                                                                                                                                                        |
| -------------------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Thread yang bekerja bersamaan dalam satu eksekusi        | 64                                                          | Eksekusi tidak membuat thread lagi hingga salah satunya selesai. API tidak menjamin angka ini, sehingga dapat berubah.                                                                                                                                     |
| Agen yang dimulai workflow sepanjang masa hidup eksekusi | 1.000                                                       | Ketika workflow meminta lebih banyak, server tidak memulai agen lain, dan eksekusi berakhir dengan `thread_limit_error`. Server dapat menjalankan ulang agen yang gagal di thread baru, sehingga sebuah eksekusi mungkin memiliki lebih dari 1.000 thread. |
| Masa hidup eksekusi                                      | 24 jam secara default, atau masa hidup yang ditetapkan agen | Eksekusi berakhir dengan `timeout_error`. Tidak ada event yang menyebutkan masa hidup yang ditetapkan agen.                                                                                                                                                |
| Eksekusi yang terbuka bersamaan dalam satu sesi          | 10 secara default                                           | Server menolak memulai eksekusi lain. Panggilan alat agen mendapat error, dan Anda mendapat `workflow_run.error` yang `error.type`-nya adalah `max_workflow_runs_error`. Eksekusi yang idle dihitung dalam batas ini.                                      |

Server memendekkan `name` eksekusi atau fase menjadi 64 karakter dan `description`-nya menjadi 256. Server memiliki batas lain untuk workflow, dan aturan untuknya, yang tidak dicantumkan di sini. Apa yang Anda lihat bergantung pada kapan server menemukan masalahnya:

| Apa yang terjadi                                                                                | Apa yang Anda lihat                                                                      |
| ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Workflow melampaui salah satu batas lain ketika agen memulai eksekusi                           | Permulaan ditolak. Anda mendapat `workflow_run.error`, dan tidak ada eksekusi.           |
| Eksekusi melampaui salah satu batas lain di kemudian waktu                                      | Anda mendapat `workflow_run.error`, lalu eksekusi dapat berakhir dengan `unknown_error`. |
| Server menemukan setelah permulaan bahwa workflow melanggar aturan untuk workflow, selain batas | Anda mendapat `workflow_run.error`, lalu eksekusi dapat berakhir dengan `program_error`. |

Sebuah sesi dapat memulai eksekusi dalam jumlah berapa pun sepanjang masa hidupnya.

### Batas laju

Pekerjaan sebuah eksekusi dihitung dalam "rate limit" (batas laju) yang sudah dimiliki organisasi Anda.

| Apa                                                                                     | Dihitung dalam                                                                                                                                                          | Apa yang harus dilakukan                                                                                                                                                     |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Permintaan klien Anda untuk mengambil atau mencantumkan sesi, thread-nya, dan event-nya | Batas baca untuk [endpoint Managed Agents](https://platform.claude.com/docs/id/managed-agents/reference#rate-limits)                                                    | Ikuti eksekusi di aliran event sesi alih-alih melakukan polling.                                                                                                             |
| Permintaan model dari thread eksekusi                                                   | [Batas laju Messages API](https://platform.claude.com/docs/id/api/rate-limits) Anda untuk model yang digunakan setiap thread, bersama dengan lalu lintas Anda yang lain | Sisakan ruang untuk eksekusi dalam batas-batas tersebut, atau [minta batas yang lebih tinggi](https://platform.claude.com/docs/id/api/rate-limits#requesting-higher-limits). |

Ketika permintaan model dari salah satu thread eksekusi terkena batas laju, atau model kelebihan beban, aliran thread itu sendiri dapat menerima `session.error` dengan jenis `model_rate_limited_error` atau `model_overloaded_error`:

* Jika `retry_status.type`-nya adalah `retrying`, server sedang mencoba ulang permintaan, dan thread masih bekerja.
* Jika nilainya `exhausted`, thread telah gagal. Jika workflow membiarkan kegagalan itu mengakhiri eksekusi, eksekusi berakhir dengan `program_error`, yang tidak menyebutkan penyebabnya. Baca event dari thread yang gagal untuk menemukannya.

Server juga membatasi seberapa banyak yang dilakukan semua sesi organisasi Anda setiap menit. Thread yang mencapai batas ini berhenti, dengan `session.error` di alirannya sendiri yang pesannya menyebutkan batas laju. Tunggu satu menit sebelum Anda meminta agen untuk melanjutkan.

Sebuah eksekusi dapat membuat lebih dari satu thread untuk bagian pekerjaan yang sama, jadi pastikan alat yang dipanggil agen Anda aman untuk dipanggil dua kali.
