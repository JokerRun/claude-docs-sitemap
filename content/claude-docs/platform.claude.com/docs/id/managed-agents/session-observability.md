---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/session-observability
fetched_at: 2026-10-29T02:15:48.406163Z
sha256: 277bc194729d62c6f484bd1e086bc681a253116e610ccc96c395b7eff517a551
---

---
title: Memeriksa sesi dan melacak penggunaan
url: https://platform.claude.com/docs/id/managed-agents/session-observability
description: Periksa sesi di Claude Console, baca penggunaan token dan biaya daftarnya, serta debug perilaku agen yang tidak terduga.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
  zdr:
    eligibility: not-eligible
    note: Sessions are stateful resources; transcripts persist until you delete them. Applies to all Managed Agents sub-features, including Self-hosted sandboxes.
  supportedModels:
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API: beta
    Claude Platform on AWS: beta
---

Gunakan penampil sesi di Claude Console untuk memeriksa apa yang dilakukan agen dalam sebuah sesi, tanpa menulis kode apa pun. Gunakan total `usage` (csharp, go: `Usage`) sesi untuk melihat apa yang dikonsumsi oleh pekerjaan tersebut. Untuk melihat giliran, permintaan model, dan penggunaan alat sebuah sesi di platform observabilitas Anda, siapkan [tracing OpenTelemetry](https://platform.claude.com/docs/id/manage-claude/opentelemetry).

## Memeriksa sesi di Console

Penampil sesi hanya dapat diakses oleh Developer dan Admin. Untuk membukanya, buka halaman [Sessions](https://platform.claude.com/sessions) (`platform.claude.com/sessions`) di Claude Console. Daftar tersebut menampilkan setiap sesi di workspace beserta status, agen, penggunaan token, biaya, dan waktu pembuatannya. Pilih sebuah sesi untuk membukanya.

Penampil sesi menampilkan:

* **Timeline minimap:** Ikhtisar aktivitas sesi dari waktu ke waktu yang dapat diperbesar, dengan satu jalur untuk setiap thread dalam sesi [multiagen](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration). Pilih sebuah jalur untuk melihat thread tersebut, atau pilih sebuah tanda untuk melompat ke event-nya.
* **Transcript:** Percakapan yang dikelompokkan berdasarkan permintaan model, termasuk pemikiran, panggilan alat beserta input dan hasilnya, serta teks pesan saat di-streaming. Anda dapat memfilter event dan menyalin atau mengunduhnya sebagai JSON.
* **Inspector:** Panel samping yang dapat diubah ukurannya dengan detail tentang sesi, dalam lima tab.

| Tab Inspector | Apa yang ditampilkan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Session**   | Detail dan metadata sesi, biaya kumulatifnya dari waktu ke waktu, dan pengeluaran terhadap [anggaran](https://platform.claude.com/docs/id/managed-agents/budgets) sesi jika ditetapkan.                                                                                                                                                                                                                                                                                                                                       |
| **Events**    | Setiap event mentah pada thread saat ini, dalam urutan yang dikirim oleh server. Pilih sebuah event untuk melihat JSON-nya. Pesan yang di-streaming saat halaman terbuka juga memiliki tampilan **Deltas** dari [event delta](https://platform.claude.com/docs/id/managed-agents/event-deltas)-nya.                                                                                                                                                                                                                           |
| **Tools**     | Alat yang dikonfigurasi untuk agen-agen sesi, beserta jumlah panggilan, kegagalan, dan durasi median. Pilih sebuah alat untuk melihat panggilannya dan melompat ke salah satunya di transkrip.                                                                                                                                                                                                                                                                                                                                |
| **Resources** | [File](https://platform.claude.com/docs/id/managed-agents/files), [repositori](https://platform.claude.com/docs/id/managed-agents/github), dan [memory store](https://platform.claude.com/docs/id/managed-agents/memory) yang di-mount pada path container-nya, termasuk memori di setiap store dan perubahan yang dibuat sesi ini terhadapnya. Juga mencantumkan file yang ditulis agen ke `/mnt/session/outputs` dan [skill](https://platform.claude.com/docs/id/managed-agents/skills) yang dilampirkan ke agen-agen sesi. |
| **Threads**   | Setiap thread beserta status, ukuran konteks, dan biayanya. Pilih sebuah thread untuk melihat detailnya, seperti agen, model, penggunaan konteks, dan biaya.                                                                                                                                                                                                                                                                                                                                                                  |

Tambahkan `?event={event_id}` ke URL sesi untuk membuka sesi pada event tertentu.

Dengan `ant beta:sessions connect`, Anda dapat membuka penampil yang sama dari CLI `ant` atau mengikuti sesi di terminal Anda. Lihat [Terhubung ke sesi Managed Agents dari terminal Anda](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/sessions-connect).

## Melacak penggunaan

Objek sesi menyertakan field `usage` dengan penggunaan kumulatif sesi: jumlah token, penggunaan alat server, waktu aktif, dan biaya daftar yang dilacak. Ambil sesi setelah sesi tersebut menjadi idle untuk membaca total terbaru.

```json
{
  "id": "sesn_01...",
  "status": "idle",
  "usage": {
    "input_tokens": 5000,
    "output_tokens": 3200,
    "cache_read_input_tokens": 20000,
    "cache_creation": {
      "ephemeral_5m_input_tokens": 2000,
      "ephemeral_1h_input_tokens": 0
    },
    "list_cost": {
      "amount": "187",
      "currency": "USD"
    },
    "active_seconds": 342.5,
    "server_tool_use": {
      "web_search_requests": 3,
      "web_fetch_requests": 0
    }
  }
}
```

| Field                     | Deskripsi                                                                                                                                                                                                                                                             |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `input_tokens`            | Token input yang tidak di-cache di seluruh panggilan model dalam sesi.                                                                                                                                                                                                |
| `output_tokens`           | Total token output di seluruh panggilan model dalam sesi.                                                                                                                                                                                                             |
| `cache_read_input_tokens` | Token yang dibaca dari cache prompt.                                                                                                                                                                                                                                  |
| `cache_creation`          | Token pembuatan cache, dirinci berdasarkan masa berlaku cache (`ephemeral_5m_input_tokens` dan `ephemeral_1h_input_tokens`).                                                                                                                                          |
| `list_cost`               | Konsumsi kumulatif sesi yang dihargai dengan tarif daftar publik, sebagai bilangan bulat sen dalam string, dengan kode mata uang.                                                                                                                                     |
| `active_seconds`          | Waktu kumulatif selama sesi memiliki setidaknya satu thread yang berjalan. Aktivitas yang tumpang tindih dari thread yang berjalan bersamaan dihitung sekali. Biaya runtime sesi dihargai berdasarkan durasi ini.                                                     |
| `server_tool_use`         | Jumlah permintaan alat yang dieksekusi server, untuk penetapan harga. Permintaan pencarian web dihargai ke dalam biaya daftar per permintaan. Permintaan web fetch tidak dikenakan biaya per permintaan dan tidak diukur, sehingga `web_fetch_requests` bernilai `0`. |

Entri cache menggunakan TTL 5 menit secara default, sehingga giliran berturut-turut dalam jendela waktu tersebut mendapat manfaat dari pembacaan cache, yang mengurangi biaya per token.

Objek `stats` sesi memiliki `active_seconds` sendiri, yang menjumlahkan waktu aktif masing-masing thread alih-alih menghitung aktivitas yang tumpang tindih sekali.

### Penggunaan per thread

`usage` (csharp, go: `Usage`) milik setiap [thread sesi](https://platform.claude.com/docs/id/managed-agents/session-threads) juga memuat `list_cost` (java, php: `listCost`; csharp, go: `ListCost`) dan `active_seconds` (java, php: `activeSeconds`; csharp, go: `ActiveSeconds`). Angka per thread dibulatkan secara independen dan tidak mencakup biaya waktu berjalan sesi, sehingga jumlahnya tidak persis sama dengan `list_cost` (java, php: `listCost`; csharp, go: `ListCost`) sesi. Angka sesi adalah angka yang otoritatif.

### Membaca penggunaan dari stream

Anda tidak perlu melakukan polling pada sesi untuk mengamati total ini. Event `session.usage` membawa snapshot kumulatif yang sama pada stream sesi dan dalam riwayat event. Snapshot tersebut memuat objek `usage` (csharp, go: `Usage`), ditambah `budget` (csharp, go: `Budget`) sesi jika sesi memilikinya.

Event ini dipancarkan pada transisi idle, bukan berdasarkan timer:

* Sesi memancarkan satu event tepat sebelum menjadi idle, apa pun alasan berhentinya.
* Sesi memancarkan satu event ketika sebuah thread berhenti sementara pada [anggaran sesi](https://platform.claude.com/docs/id/managed-agents/budgets).

### Menerapkan batas pengeluaran

Untuk menerapkan batas pengeluaran, tetapkan anggaran sesi alih-alih melakukan polling penggunaan dan menghentikan sesi sendiri. Platform menghitung harga konsumsi sesi secara terus-menerus, dan menjeda setiap thread sebelum permintaan model berikutnya setelah biaya daftar mencapai batas. Lihat [Ketika sesi mencapai anggarannya](https://platform.claude.com/docs/id/managed-agents/budgets#when-a-session-reaches-its-budget) untuk melihat seperti apa hal tersebut pada stream.

## Tips debugging

* **Periksa event sesi:** Sesi melaporkan kesalahan melalui event [`session.error`](https://platform.claude.com/docs/id/managed-agents/reference#event-types).
* **Tinjau hasil alat:** Kegagalan alat sering kali menjelaskan perilaku agen yang tidak terduga. Tab **Tools** pada Inspector menampilkan kegagalan setiap alat.
* **Gunakan prompt sistem:** Tambahkan instruksi logging ke prompt sistem agar agen merangkum apa yang dilakukannya dan apa yang ditemukannya.
* **Memecahkan masalah pratinjau:** Jika stream yang memilih untuk menerima delta event tidak berperilaku seperti yang Anda harapkan, lihat [Memecahkan masalah pratinjau](https://platform.claude.com/docs/id/managed-agents/event-deltas#troubleshoot-previews).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Aliran event sesi" icon="lightning" href="https://platform.claude.com/docs/id/managed-agents/events-and-streaming">
    Kirim event, streaming respons, dan interupsi atau arahkan ulang sesi Anda saat sedang berjalan.
  </Card>

  <Card title="Anggaran sesi" icon="coins" href="https://platform.claude.com/docs/id/managed-agents/budgets">
    Batasi pengeluaran sesi dengan anggaran dolar yang ketat yang diberlakukan berdasarkan tarif daftar publik.
  </Card>
</CardGroup>

## Availability

Session viewer is in beta on every model.

### API support

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Availability: Always on

| Status | Cloud platforms                                                                                                    |
| ------ | ------------------------------------------------------------------------------------------------------------------ |
| Beta   | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) |

### Required beta headers

[Beta headers overview](https://platform.claude.com/docs/id/api/beta-headers)

Beta headers allow you to access experimental features and new model capabilities before they become part of the standard API.

* `managed-agents-2026-04-01`

### Data handling

[Data handling overview](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item    | Zero data retention                                                                                                                                      | HIPAA                                                                        |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Status  | Not eligible                                                                                                                                             | Not eligible                                                                 |
| Details | Sessions are stateful resources; transcripts persist until you delete them. Applies to all Managed Agents sub-features, including Self-hosted sandboxes. | Applies to all Managed Agents sub-features, including Self-hosted sandboxes. |

Applicable endpoints:

* `/v1/agents`
* `/v1/sessions`
* `/v1/environments`
