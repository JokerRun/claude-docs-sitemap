---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/budgets
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 0d83494f093d4d33fc707385cde9198ca99b2f3746796302d0ed80ec73983387
---

---
title: Anggaran sesi
url: https://platform.claude.com/docs/id/managed-agents/budgets
description: Batasi pengeluaran sesi dengan anggaran dolar tetap yang diberlakukan berdasarkan tarif daftar publik.
---

Anggaran sesi adalah batas pengeluaran tetap opsional yang Anda tetapkan saat [membuat sesi](https://platform.claude.com/docs/id/managed-agents/sessions). Platform secara terus-menerus menghitung harga semua yang dikonsumsi sesi berdasarkan tarif daftar publik (disebut **list cost** atau biaya daftar sesi) dan berhenti mengeluarkan permintaan model baru setelah biaya tersebut mencapai anggaran. Permintaan yang sedang berjalan saat batas terlampaui tetap diselesaikan, sehingga biaya daftar akhir dapat berada [sedikit di atas anggaran](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget). Sesi yang mencapai anggarannya akan dijeda dan menjadi [idle](https://platform.claude.com/docs/id/managed-agents/session-operations#session-statuses) alih-alih dihentikan; mengubah atau menghapus anggaran akan melanjutkan pekerjaannya secara otomatis. Deployment menerima anggaran yang sama dan menerapkannya ke setiap sesi yang dimulainya; lihat [Anggaran pada deployment](https://platform.claude.com/docs/id/managed-agents/budgets#budgets-on-deployments).

<Note>
  Permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`, kecuali endpoint memory store, yang menggunakan `agent-memory-2026-07-22` sebagai gantinya. SDK mengatur header beta yang benar secara otomatis. Lihat [Header beta](https://platform.claude.com/docs/id/api/beta-headers#endpoint-specific-headers).
</Note>

## Menetapkan anggaran saat pembuatan sesi

Sertakan field opsional `budget` saat Anda membuat sesi:

<CodeGroup>
  ```bash cURL
  session=$(curl -fsSL https://api.anthropic.com/v1/sessions \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<EOF
  {
    "agent": "$AGENT_ID",
    "environment_id": "$ENVIRONMENT_ID",
    "budget": {
      "type": "limit",
      "max_list_cost": {"amount": "2500", "currency": "USD"}
    }
  }
  EOF
  )
  SESSION_ID=$(jq -r '.id' <<< "$session")
  ```
</CodeGroup>

Objek `budget` memiliki dua field:

* `type` selalu bernilai `"limit"`.
* `max_list_cost` adalah batas itu sendiri: `amount` adalah bilangan bulat dalam sen AS yang ditulis sebagai string tanpa angka nol di depan (`"2500"` adalah $25,00 dan `"50"` adalah 50 sen) dan harus lebih besar dari nol. Bentuk desimal seperti `"25.00"` akan ditolak. Jumlah ini berupa string, bukan angka, agar tidak ada pembulatan float yang diterapkan padanya. `currency` adalah kode mata uang ISO-4217 dalam huruf kapital; `USD` adalah satu-satunya mata uang yang didukung.

Anggaran hanya dapat dilampirkan saat sesi dibuat. Menambahkan anggaran ke sesi yang sudah ada dan tidak memilikinya akan ditolak dengan error 400. Batas pada sesi yang memiliki anggaran dapat [diubah](https://platform.claude.com/docs/id/managed-agents/budgets#change-the-budget) atau [dihapus](https://platform.claude.com/docs/id/managed-agents/budgets#remove-the-budget) kapan saja.

## Cara biaya daftar diukur

Platform menghitung harga apa yang dikonsumsi sesi, secara terus-menerus, berdasarkan tarif daftar publik:

* **Token model**, berdasarkan harga daftar setiap model yang digunakan
* **Pencarian web**, sebesar $10 per 1.000 pencarian
* **Waktu berjalan sesi**, sebesar $0,08 per jam

Total dolar berjalan ini adalah **list cost** (biaya daftar) sesi, dan inilah yang dibandingkan dengan anggaran. Biaya daftar bukanlah harga kontrak Anda: jika organisasi Anda telah menegosiasikan diskon, sesi mencapai batasnya ketika total harga daftar mencapainya, dan pengeluaran yang ditagihkan kepada Anda mungkin lebih rendah dari batas tersebut.

Penegakan menggunakan biaya daftar yang tepat dan tidak dibulatkan. Angka `list_cost` yang dilaporkan pada sesi dan event-nya adalah sen bulat, dibulatkan ke sen terdekat, sehingga angka yang dilaporkan dapat berbeda hingga setengah sen di kedua sisi dari jumlah tepat yang digunakan dalam penegakan.

## Ketika sesi mencapai anggarannya

Batas diberlakukan di antara permintaan model, bukan di tengah permintaan. Sebelum setiap permintaan model, platform memeriksa biaya daftar yang telah dikonsumsi sesi, dan setelah total tersebut mencapai batas, setiap thread dijeda sebelum permintaan berikutnya. Permintaan yang membawa total melewati batas diterima saat sesi masih di bawah batas dan berjalan hingga selesai, sehingga `list_cost` yang tercatat pada sesi yang dijeda terbaca pada atau sedikit di atas `max_list_cost`: sesi dengan batas `"50"` (50 sen) dapat dijeda dengan `list_cost` sebesar `"53"`. Ini adalah hal yang diharapkan, bukan kesalahan penagihan, dan kelebihan tersebut dibatasi oleh satu permintaan model per thread. Perlakukan anggaran sebagai batas untuk pekerjaan baru, bukan titik berhenti yang tepat, dan tentukan ukuran batas dengan mempertimbangkan margin satu permintaan tersebut.

Sesi yang mencapai anggarannya menjadi idle dengan `stop_reason` bernilai `budget_reached`; sesi tidak dihentikan, dan riwayat serta sandbox-nya dipertahankan seperti sesi idle lainnya. Pada [event stream](https://platform.claude.com/docs/id/managed-agents/events-and-streaming), Anda akan melihat, secara berurutan:

1. Event `session.thread_status_idle` dengan `stop_reason` bernilai `budget_reached` saat setiap thread dijeda.
2. Event [`session.usage`](https://platform.claude.com/docs/id/managed-agents/budgets#monitor-spend) dengan penggunaan kumulatif dan biaya daftar sesi.
3. Event `session.status_idle` dengan `stop_reason` bernilai `budget_reached`. Event usage selalu langsung mendahului event idle ini.

Thread yang permintaan terakhirnya melewati batas sekaligus menyelesaikan gilirannya akan melaporkan `end_turn` pada event `session.thread_status_idle` miliknya sendiri, sementara sesi tetap melaporkan `budget_reached`; perlakukan `stop_reason` tingkat sesi sebagai sinyal bahwa sesi dijeda pada anggarannya.

### Event yang diterima saat mencapai batas

Saat sesi berada pada atau di atas anggarannya, sesi hanya menerima event yang menyelesaikan pekerjaan yang sudah berjalan:

* `user.tool_confirmation`
* `user.tool_result`
* `user.custom_tool_result`
* `user.interrupt`

Event apa pun yang akan memulai pekerjaan baru, seperti `user.message`, ditolak dengan error 400 yang menyebutkan daftar ini. Hasil yang diselesaikan dicatat tanpa memicu permintaan model baru; sesi tetap dijeda pada anggarannya.

`user.interrupt` yang dikirim saat sesi dijeda pada anggarannya (semua thread dijeda pada batas) diterima dan diabaikan: event tersebut tidak muncul dalam daftar event dan tidak mengubah apa pun. Ubah atau hapus anggaran untuk melanjutkan.

## Melanjutkan sesi yang mencapai anggarannya

Ubah atau hapus anggaran dengan pembaruan sesi. Pembaruan yang diterima akan melanjutkan pekerjaan sesi yang dijeda secara otomatis; tidak diperlukan tindakan klien lebih lanjut.

### Mengubah anggaran

Perbarui sesi dengan `max_list_cost` baru. Nilai baru dapat lebih tinggi atau lebih rendah dari batas saat ini, tetapi harus benar-benar lebih besar dari biaya daftar yang telah dikonsumsi sesi; jika tidak, pembaruan ditolak dengan error 400: `budget.max_list_cost must be greater than the session's consumed list cost`. Karena biaya yang dikonsumsi biasanya berada [sedikit di atas batas lama](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget) saat sesi dijeda, dasarkan nilai baru pada `usage.list_cost` yang dilaporkan sesi, bukan pada `max_list_cost` lama. Tetapkan satu sen atau lebih di atas angka tersebut: nilai yang dilaporkan dibulatkan dan dapat berada sedikit di bawah biaya konsumsi tepat yang digunakan dalam pemeriksaan.

<CodeGroup>
  ```bash cURL
  curl -sS --fail-with-body "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d @- <<'EOF'
  {
    "budget": {
      "type": "limit",
      "max_list_cost": {"amount": "4000", "currency": "USD"}
    }
  }
  EOF
  ```
</CodeGroup>

### Menghapus anggaran

Tetapkan `budget` ke `null` untuk menghapus batas sepenuhnya. Pekerjaan sesi yang dijeda akan dilanjutkan, dan event `session.updated` yang dihasilkan membawa `budget` yang ditetapkan ke `null`.

<CodeGroup>
  ```bash cURL
  curl -sS --fail-with-body "https://api.anthropic.com/v1/sessions/$SESSION_ID" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: managed-agents-2026-04-01" \
    -H "content-type: application/json" \
    -d '{"budget": null}'
  ```
</CodeGroup>

<Warning>
  Menghapus anggaran sesi bersifat satu arah: sesi yang anggarannya telah dihapus tidak dapat diberi anggaran baru. Untuk tetap mempertahankan batas pada sesi, ubah anggaran sebagai gantinya.
</Warning>

## Memantau pengeluaran

Objek sesi membawa `budget` miliknya dan objek `usage` dengan pengeluaran yang dilacak: `usage.list_cost` adalah biaya daftar yang dikonsumsi sesi, dan `usage.active_seconds` adalah waktu berjalan yang menjadi dasar penghitungan biaya runtime-nya. Pada sesi yang dijeda dengan `budget_reached`, harapkan `usage.list_cost` terbaca pada atau sedikit di atas `max_list_cost`: [permintaan yang melewati batas](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget) selesai sebelum jeda. `active_seconds` tingkat sesi menghitung aktivitas yang tumpang tindih dari thread yang berjalan bersamaan hanya satu kali. Respons pengambilan thread membawa dua field yang sama pada `usage` milik thread itu sendiri, dihitung per thread. Angka per thread dibulatkan secara independen dan tidak termasuk biaya waktu berjalan sesi, sehingga jumlahnya tidak persis sama dengan `list_cost` sesi; angka sesi adalah yang digunakan untuk menegakkan anggaran.

Event `session.usage` adalah snapshot dari penggunaan kumulatif sesi dan biaya daftar yang dilacak. Event ini membawa total token sesi, `list_cost`, `active_seconds`, jumlah permintaan `server_tool_use` (`web_search_requests`, yang dihitung ke dalam biaya daftar per permintaan, dan `web_fetch_requests`, yang terbaca `0` karena permintaan web fetch tidak membawa biaya per permintaan dan tidak diukur), serta salinan `budget` sesi, atau `null` jika sesi tidak memilikinya. Event ini muncul dalam daftar event dan stream sesi. Sesi mengeluarkan satu event ini tepat sebelum menjadi idle, apa pun stop reason-nya, sehingga sesi yang mencapai anggarannya selalu mengeluarkan satu event ini tepat sebelum event idle budget-reached.

Untuk membaca penggunaan dari stream dan objek sesi, lihat [Melacak penggunaan](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#tracking-usage).

## Anggaran dalam sesi multiagent

Sesi [multiagent](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) memiliki satu anggaran yang dibagikan di seluruh thread-nya; tidak ada batas per thread. Konsumsi setiap thread dihitung berdasarkan model yang digunakannya masing-masing, dan thread dijeda secara independen saat batas bersama tercapai. Konsultasi [advisor](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration#give-the-session-an-advisor) dihitung terhadap anggaran yang sama, dihargai berdasarkan tarif model advisor. Satu thread dapat dijeda pada `budget_reached` sementara thread lain menyelesaikan permintaannya yang sedang berjalan.

Permintaan yang tertunda lebih diutamakan daripada batas: sesi dengan satu thread yang menunggu pada `requires_action` dan thread lain yang dijeda pada `budget_reached` melaporkan `requires_action` di tingkat sesi. Permintaan yang tertunda tetap memerlukan jawaban, dan menjawabnya adalah [event penyelesaian](https://platform.claude.com/docs/id/managed-agents/budgets#events-accepted-at-the-cap) yang tidak diblokir oleh anggaran.

## Anggaran pada deployment

[Deployment](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments) menerima objek `budget` yang sama saat Anda membuat atau memperbaruinya:

```json
{
  "budget": {
    "type": "limit",
    "max_list_cost": { "amount": "2000", "currency": "USD" }
  }
}
```

Batas disalin ke setiap sesi yang dimulai oleh deployment, sehingga membatasi setiap eksekusi secara terpisah, bukan pengeluaran kumulatif deployment. Mengubah anggaran deployment berlaku untuk sesi yang dimulai deployment setelahnya, bukan untuk sesi yang sudah berjalan. Tidak seperti sesi, anggaran deployment dapat dihapus dengan `null` dan ditetapkan lagi nanti. Lihat [Menetapkan anggaran pada setiap eksekusi](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments#set-a-budget-on-each-run).

## Model tanpa harga daftar

Anggaran hanya dapat melacak konsumsi yang dapat dihargai oleh platform. Membuat sesi beranggaran yang agent-nya, atau agent atau advisor mana pun pada [daftar multiagent](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration)-nya, menggunakan model tanpa harga daftar publik akan ditolak dengan error 400 yang menyatakan bahwa tidak ada harga daftar yang tersedia untuk model tersebut.

Jika penggunaan sesi beranggaran kemudian mencakup model tanpa harga daftar, anggaran tidak dapat lagi mengukur pengeluaran sesi: sesi dapat dijeda dengan `stop_reason` bernilai `budget_reached`, dan mengubah anggaran akan ditolak. Hapus anggaran untuk melanjutkan sesi.

## Referensi error

Permintaan terkait anggaran ditolak dalam kasus-kasus berikut:

| Kondisi                                                                                                                                                                                                                                                     | Status |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| Event yang memulai pekerjaan (misalnya, `user.message`) dikirim saat sesi berada pada atau di atas anggarannya; error menyebutkan [event penyelesaian yang diterima](https://platform.claude.com/docs/id/managed-agents/budgets#events-accepted-at-the-cap) | 400    |
| Anggaran ditetapkan ke nilai yang sama dengan atau di bawah biaya daftar yang dikonsumsi sesi                                                                                                                                                               | 400    |
| Anggaran ditambahkan ke sesi yang dibuat tanpa anggaran, atau ditambahkan kembali setelah dihapus                                                                                                                                                           | 400    |
| `amount` bukan bilangan bulat dalam sen (misalnya, `"25.00"`), bernilai nol atau negatif, atau `currency` bukan `USD`                                                                                                                                       | 400    |
| Pembuatan beranggaran mereferensikan model [tanpa harga daftar publik](https://platform.claude.com/docs/id/managed-agents/budgets#models-without-a-list-price)                                                                                              | 400    |

<Note>
  Anggaran sesi adalah batas tetap dalam dolar AS (ditulis dalam sen) pada satu sesi, yang diberlakukan oleh platform. Ini berbeda dari [task budget](https://platform.claude.com/docs/id/build-with-claude/task-budgets) pada Messages API, yang merupakan anggaran bersifat saran dalam denominasi token yang digunakan model untuk mengatur dirinya sendiri dalam satu loop agentik.
</Note>
