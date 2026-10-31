---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/opentelemetry
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 12b98abe82d3059f4ee332d4c119bc2f83df70b047cf7fb8983fae7cf774f5c1
---

---
title: Tracing OpenTelemetry untuk Claude API
url: https://platform.claude.com/docs/id/manage-claude/opentelemetry
description: Lacak permintaan Messages API, penggunaan alat, dan sesi Managed Agents Anda dengan span OpenTelemetry dari Claude SDK dan Claude API.
featureMetadata:
  topic:
    title: OpenTelemetry
    url: https://platform.claude.com/docs/en/manage-claude/opentelemetry
  status: beta
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
    Claude Models on Google Cloud (Anthropic managed): beta
    Amazon Bedrock: beta
    Amazon Bedrock (InvokeModel): beta
    Claude Models on Google Cloud (Google managed): beta
    Microsoft Foundry: beta
---

<Note>
  Ekspor OpenTelemetry sedang dalam tahap beta. Fitur ini disediakan berdasarkan perjanjian Anda dengan Anthropic, termasuk bagian Layanan Beta dari [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms).
</Note>

<video aria-label="Menelusuri agen dengan OpenTelemetry di Claude Platform">
  <source src="https://media.platform.claude.com/docs/opentelemetry/tracing/overview-1080p.mp4" type="video/mp4" media="(min-width: 1280px)" />
  <source src="https://media.platform.claude.com/docs/opentelemetry/tracing/overview-720p.mp4" type="video/mp4" media="(min-width: 640px)" />
  <source src="https://media.platform.claude.com/docs/opentelemetry/tracing/overview-480p.mp4" type="video/mp4" />
</video>

Claude API dan SDK dapat melakukan “tracing” (penelusuran) terhadap permintaan Messages API, penggunaan alat, dan sesi Managed Agents Anda dengan [OpenTelemetry](https://opentelemetry.io/) (OTel). Anda dapat melihat trace ini di platform observabilitas yang sudah Anda miliki. Gunakan trace tersebut untuk men-debug permintaan yang gagal atau lambat, melacak penggunaan token dan “latency” (latensi), serta membangun eval dari lalu lintas nyata. Anda juga dapat melihat setiap permintaan di dalam trace aplikasi Anda sendiri, yang ditautkan ke pengguna atau fitur yang mengirimkannya.

OpenTelemetry adalah standar netral vendor yang didukung oleh sebagian besar platform observabilitas. *Trace* (jejak) adalah catatan lengkap dari satu permintaan yang melewati sistem Anda. *Span* (rentang) adalah satu langkah dalam sebuah trace, seperti permintaan model atau penggunaan alat. API dan SDK menggunakan atribut dari [konvensi semantik GenAI](https://github.com/open-telemetry/semantic-conventions-genai), sehingga platform yang mendukung konvensi tersebut dapat mengenali span tanpa penyiapan tambahan.

## Memulai

Anda dapat menyiapkan tracing SDK, tracing API, atau keduanya. Siapkan keduanya untuk melihat span SDK dan API dari sebuah permintaan dalam satu trace, seperti pada [contoh trace](https://platform.claude.com/docs/id/manage-claude/opentelemetry#example-traces-and-how-to-read-them).

Biarkan Claude Code menyiapkan fitur ini untuk Anda

```text
Siapkan tracing OpenTelemetry dengan Claude API dan Claude SDK
```

<CardGroup cols={3}>
  <Card title="Siapkan tracing SDK" icon="code-brackets" href="https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk" layout="horizontal">
    Instal SDK dan daftarkan tracer provider.
  </Card>

  <Card title="Siapkan tracing API" icon="cloud" href="https://platform.claude.com/docs/id/manage-claude/opentelemetry/api" layout="horizontal">
    Tambahkan tujuan di Claude Console.
  </Card>

  <Card title="Referensi span" icon="book" href="https://platform.claude.com/docs/id/api/opentelemetry/spans" layout="horizontal">
    Cari span dan atributnya.
  </Card>
</CardGroup>

| Yang Anda dapatkan                                                                                                                | Penelusuran SDK                                                             | Penelusuran API                                                                            | Keduanya bersama                                                                           |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| Permintaan [Messages API](https://platform.claude.com/docs/id/api/messages/create)                                                | ✅                                                                           | ✅                                                                                          | ✅                                                                                          |
| Permintaan [Sessions API](https://platform.claude.com/docs/id/managed-agents/sessions)                                            | ✅                                                                           | ✅                                                                                          | ✅                                                                                          |
| Penggunaan token (lihat [Penghitungan token](https://platform.claude.com/docs/id/manage-claude/opentelemetry#count-tokens))       | ✅                                                                           | ✅                                                                                          | ✅                                                                                          |
| Setiap eksekusi model dalam sebuah permintaan                                                                                     | —                                                                           | ✅                                                                                          | ✅                                                                                          |
| Giliran [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)                                             | —                                                                           | ✅                                                                                          | ✅                                                                                          |
| [Alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools), dijalankan oleh API                    | —                                                                           | ✅                                                                                          | ✅                                                                                          |
| Alat klien, dijalankan oleh [tool runner](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-runner)              | ✅                                                                           | —                                                                                          | ✅                                                                                          |
| Alat dalam [sandbox self-hosted](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#trace-a-self-hosted-sandbox) | ✅                                                                           | —                                                                                          | ✅                                                                                          |
| Permintaan API lainnya, seperti mengunggah file                                                                                   | ✅                                                                           | —                                                                                          | ✅                                                                                          |
| Penyiapan                                                                                                                         | [Kode](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk) | [Console](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api)             | Keduanya                                                                                   |
| Izin yang diperlukan                                                                                                              | Tidak ada                                                                   | [Admin](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#what-you-need) | [Admin](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#what-you-need) |
| Cakupan                                                                                                                           | Klien yang menggunakan SDK                                                  | Klien apa pun                                                                              | Klien apa pun                                                                              |
| Dukungan platform cloud                                                                                                           | Apa pun                                                                     | Claude Platform<br />Claude Platform on AWS                                                | Claude Platform<br />Claude Platform on AWS                                                |

Untuk Claude Code, Agent SDK, atau Cowork, lihat [pemantauan Claude Code](https://code.claude.com/docs/en/monitoring-usage), [observability Agent SDK](https://code.claude.com/docs/en/agent-sdk/observability), atau [pemantauan aktivitas Cowork](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry).

## Mengirim trace ke platform mitra

Kirim trace ke platform observabilitas apa pun yang menerima OTLP, termasuk mitra berikut:

<CardGroup cols={3}>
  <Card title="Arize AI" image="https://platform.claude.com/docs/images/partner-logos/arize.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/arize-dark.svg" imageOffsetLeft={2} href="https://arize.com/docs/ax/integrations/platforms/claude-managed-agents/claude-managed-agents-tracing">
    Platform observabilitas dan evaluasi terpadu untuk AI.
  </Card>

  <Card title="Braintrust" image="https://platform.claude.com/docs/images/partner-logos/braintrust.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/braintrust-dark.svg" imageHeight={25} imageOffsetLeft={1} href="https://www.braintrust.dev/docs/integrations/ai-providers/anthropic#export-opentelemetry-traces-from-the-claude-api">
    Platform observabilitas aktif untuk agen.
  </Card>

  <Card title="Databricks" image="https://platform.claude.com/docs/images/partner-logos/databricks.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/databricks-dark.svg" imageHeight={26} imageOffsetLeft={1} href="https://docs.databricks.com/aws/en/ai-gateway/unified-trace-table">
    Control plane AI terpadu untuk observabilitas dan evaluasi.
  </Card>

  <Card title="Datadog" image="https://platform.claude.com/docs/images/partner-logos/datadog.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/datadog-dark.svg" imageHeight={28} imageOffsetLeft={2} href="https://docs.datadoghq.com/llm_observability/instrument/otel_instrumentation/?tab=python#using-claude-managed-agents">
    Observabilitas dan keamanan bertenaga AI.
  </Card>

  <Card title="Dynatrace" image="https://platform.claude.com/docs/images/partner-logos/dynatrace.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/dynatrace-dark.svg" imageHeight={22} href="https://docs.dynatrace.com/docs/observe/dynatrace-for-ai-observability/integrations/claude-platform">
    Observabilitas yang dibangun untuk era AI.
  </Card>

  <Card title="Elastic" image="https://platform.claude.com/docs/images/partner-logos/elastic.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/elastic-dark.svg" imageHeight={32} href="https://www.elastic.co/docs/reference/opentelemetry/motlp">
    Observabilitas berbasis sumber terbuka.
  </Card>

  <Card title="Grafana Cloud" image="https://platform.claude.com/docs/images/partner-logos/grafana.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/grafana-dark.svg" imageHeight={34} imageOffsetLeft={2} href="https://grafana.com/docs/grafana-cloud/observe-and-act/agent-observability/guides/send-claude-platform-traces/">
    Platform observabilitas terbuka yang dikelola sepenuhnya.
  </Card>

  <Card title="Honeycomb" image="https://platform.claude.com/docs/images/partner-logos/honeycomb.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/honeycomb-dark.svg" imageHeight={36} imageOffsetLeft={4} href="https://docs.honeycomb.io/send-data/use-cases/claude-platform">
    Platform observabilitas untuk bentuk baru perangkat lunak.
  </Card>

  <Card title="Langfuse" image="https://platform.claude.com/docs/images/partner-logos/langfuse.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/langfuse-dark.svg" imageHeight={26} imageOffsetLeft={1} href="https://langfuse.com/integrations/model-providers/claude-platform">
    Platform observabilitas dan evaluasi agen sumber terbuka.
  </Card>

  <Card title="LangSmith" image="https://platform.claude.com/docs/images/partner-logos/langchain.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/langchain-dark.svg" imageHeight={29} href="https://docs.langchain.com/langsmith/trace-anthropic">
    Platform rekayasa agen LangSmith.
  </Card>

  <Card title="New Relic" image="https://platform.claude.com/docs/images/partner-logos/new-relic.svg" imageHeight={27} imageOffsetLeft={1} href="https://docs.newrelic.com/docs/ai-monitoring/opentelemetry-ai-monitoring/#anthropic">
    Platform observabilitas cerdas.
  </Card>

  <Card title="PostHog" image="https://platform.claude.com/docs/images/partner-logos/posthog.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/posthog-dark.svg" imageHeight={29} href="https://posthog.com/docs/ai-observability/installation/anthropic?tab=Claude+Platform&utm_source=anthropic&utm_campaign=anthropic-otel">
    Platform lengkap untuk membangun produk yang sukses.
  </Card>

  <Card title="Pydantic Logfire" image="https://platform.claude.com/docs/images/partner-logos/pydantic.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/pydantic-dark.svg" imageHeight={24} href="https://pydantic.dev/docs/logfire/integrations/llms/claude-platform/">
    Observabilitas AI dan umum siap produksi.
  </Card>

  <Card title="Sentry" image="https://platform.claude.com/docs/images/partner-logos/sentry.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/sentry-dark.svg" imageHeight={25} href="https://sentry.io/cookbook/trace-claude-platform-with-opentelemetry/">
    Debug kode Anda yang rusak dan agen yang berperilaku tidak semestinya.
  </Card>

  <Card title="Snowflake" image="https://platform.claude.com/docs/images/partner-logos/snowflake.svg" imageHeight={30} imageOffsetLeft={2} href="https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-ai-gateway/observability#trace-claude-requests">
    Control plane agentik dengan observabilitas dan tata kelola bawaan.
  </Card>

  <Card title="Splunk" image="https://platform.claude.com/docs/images/partner-logos/splunk.svg" imageDark="https://platform.claude.com/docs/images/partner-logos/splunk-dark.svg" imageHeight={27} imageOffsetLeft={1} href="https://agent-observability-docs.splunk.com/sdk-api/third-party-integrations/claude">
    Amati, evaluasi, dan amankan agen.
  </Card>
</CardGroup>

## Mode konten

Setiap tujuan dan setiap klien SDK memiliki mode konten, yang menentukan apakah span menyertakan prompt dan respons model. Atur mode ini saat Anda [menambahkan tujuan](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#add-a-destination) atau [mengonfigurasi SDK](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk#configure-the-sdk).

* **Metadata only** (`metadata_only` di SDK): Default. Span menyertakan pengidentifikasi, waktu, status, jumlah token, dan teks yang Anda pilih, seperti nama dan deskripsi agen dan alat Anda serta nama server MCP Anda.
* **Full content** (`content` di SDK): Visibilitas paling tinggi. Span menyertakan prompt dan respons model, serta semua yang ada di Metadata only.

Dengan Full content, Anda juga dapat melihat mengapa suatu proses gagal atau lambat, membaca percakapan lengkap, dan membangun eval dari trace nyata. Di [referensi span OpenTelemetry](https://platform.claude.com/docs/id/api/opentelemetry/spans), atribut yang menyimpan prompt dan respons ditandai <Badge>Content</Badge>.

<Info>
  Platform observabilitas Anda menyimpan konten ini di bawah pengaturan akses dan retensinya sendiri, jadi periksa bahwa pengaturan tersebut memenuhi persyaratan organisasi Anda.
</Info>

Jika organisasi Anda memiliki pembatasan penanganan data HIPAA, FERPA, atau K-12 dengan Anthropic, tujuan hanya mengekspor metadata apa pun mode kontennya. Span SDK tidak terpengaruh.

Dengan [zero data retention](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention), Anda tetap dapat menggunakan Full content. Untuk permintaan Messages API, API menyimpan konten yang diekspor hanya di memori hingga konten tersebut dikirimkan ke tujuan. [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) tidak memenuhi syarat untuk zero data retention, dan retensi datanya tetap sama saat Anda menggunakan OpenTelemetry.

### Batas konten

Dengan Full content, setiap span secara default menampung konten hingga 0,75 MB. Ukuran itu cukup untuk jendela konteks 200 ribu token berisi teks bahasa Inggris dan tetap di bawah batas permintaan 1 MB pada banyak platform observabilitas dan proxy. Jika Anda memilih platform mitra sebagai **Provider**, Console menetapkan batas yang diterima oleh platform tersebut.

Ketika konten melebihi batas, SDK atau API memendekkan konten tersebut dan mengatur `anthropic.content.truncated` ke `true`. Span permintaan menghapus prompt sistem dan pesan paling awal terlebih dahulu, dan span alat menghapus blok mulai dari akhir hasil. Gambar dan dokumen hanya muncul sebagai jenisnya.

Ubah batas dalam kasus berikut:

* **Platform observabilitas Anda menerima payload yang lebih besar:** Naikkan atau hapus batas agar prompt dan respons yang panjang tetap utuh. Jendela konteks 1M token yang terisi penuh membutuhkan sekitar 4 MB.
* **Platform observabilitas Anda atau proxy di depannya menolak permintaan berukuran besar:** Turunkan batas.

Di SDK, atur `traces.max_content_bytes` (typescript, java, php: `traces.maxContentBytes`; csharp: `Traces.MaxContentBytes`; go: `option.WithOpenTelemetryTracesMaxContentBytes()`). Di Console, atur **Content mode** ke **Full content** saat Anda [menambahkan tujuan](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#add-a-destination), lalu atur **Maximum content size in MB** di bagian **Advanced settings**.

## Contoh trace dan cara membacanya

### Permintaan Messages API

Di bawah span API dari permintaan yang [membuat pesan](https://platform.claude.com/docs/id/api/messages/create), API menambahkan span untuk setiap permintaan model dan span alat untuk setiap penggunaan server tool atau alat konektor MCP yang dijalankan API.

Dalam contoh ini, aplikasi Anda memanggil [tool runner](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-runner), helper SDK yang menjalankan alat Anda dan mengirimkan hasilnya kembali ke Claude. Setiap permintaan yang dikirim tool runner memiliki span klien dari SDK dan span server dari API. Span muncul dalam urutan berikut:

1. Aplikasi Anda memulai span `answer_question` dan memanggil tool runner Messages di dalamnya (ditampilkan sebagai span [`anthropic.messages.tool_runner`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-tool-runner)).
2. Tool runner mengirimkan permintaan pertama (ditampilkan sebagai span klien [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create) pertama dan span di bawahnya). Dalam permintaan ini, API menjalankan alat pencarian web di antara dua permintaan model.
3. Dalam permintaan model kedua, model meminta untuk menggunakan alat kustom `get_weather`, sehingga permintaan pertama berakhir.
4. Tool runner menjalankan `get_weather` (ditampilkan sebagai span `anthropic.custom_tool_use get_weather`).
5. Tool runner mengirimkan permintaan kedua dengan hasil alat (ditampilkan sebagai span klien `anthropic.messages.create` kedua dan span di bawahnya).
6. Dalam permintaan kedua, model memberikan jawaban akhir.

![Contoh trace tool runner Messages: dua permintaan dengan span klien dan server, permintaan model, web\_search, dan get\_weather](https://platform.claude.com/docs/id/images/opentelemetry-sdk-trace-shape.svg)

SDK di aplikasi Anda memancarkan span [`anthropic.messages.tool_runner`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-tool-runner), span [`anthropic.custom_tool_use`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-tool-use-anthropic-mcp-tool-use-and-anthropic-custom-tool-use), dan span klien dari setiap permintaan. Untuk mendapatkan span ini, [siapkan tracing SDK](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk).

Setiap permintaan memiliki penggunaan tokennya di beberapa span-nya. Untuk menghitung setiap token sekali saja, lihat [Penghitungan token](https://platform.claude.com/docs/id/manage-claude/opentelemetry#count-tokens).

Dengan [Full content](https://platform.claude.com/docs/id/manage-claude/opentelemetry#choose-a-content-mode), span server `anthropic.messages.create` berisi prompt dan respons. Prompt sistem ada di `gen_ai.system_instructions`, pesan-pesan dari permintaan di `gen_ai.input.messages`, dan respons di `gen_ai.output.messages`.

Untuk setiap span dan atributnya, lihat [referensi span OpenTelemetry](https://platform.claude.com/docs/id/api/opentelemetry/spans).

### Sesi Managed Agents

Sebuah sesi memiliki span untuk setiap permintaan Sessions API dan span giliran untuk setiap giliran agen. Giliran yang dimulai oleh sebuah permintaan merupakan anak dari span permintaan tersebut. Sebuah giliran berisi span untuk setiap permintaan model dan setiap alat yang dijalankan oleh API, kecuali dalam [kasus yang tercantum dalam referensi span alat](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-tool-use-anthropic-mcp-tool-use-and-anthropic-custom-tool-use). Giliran juga berisi span untuk setiap evaluasi hasil.

Contoh ini mengikuti satu permintaan chat, di mana aplikasi Anda mengirim pesan ke sebuah sesi dan menjalankan alat kustom. Trace tersebut memiliki span dari aplikasi Anda dan dari API, dengan urutan berikut:

1. Aplikasi Anda menerima permintaan `POST /chat` dari pengguna.
2. Aplikasi Anda memulai session tool runner dari SDK, yang mencantumkan dan melakukan streaming event sesi (ditampilkan sebagai span `anthropic.sessions.events.stream` dan `anthropic.sessions.events.list`).
3. Aplikasi Anda mengirim pesan pengguna ke sesi dengan memanggil `sessions.events.send`.
4. Sebuah giliran dimulai dan mencakup permintaan model, penggunaan alat `bash`, dan giliran pada thread lain (ditampilkan sebagai span `anthropic.session.turn` pertama dan span di bawahnya).
5. Model meminta untuk menggunakan [alat kustom](https://platform.claude.com/docs/id/managed-agents/tools) `list_issues`, sehingga giliran berakhir dengan stop reason `requires_action`.
6. Session tool runner menjalankan `list_issues` (ditampilkan sebagai span `anthropic.custom_tool_use list_issues`) dan mengirim hasilnya dengan memanggil `sessions.events.send`.
7. Giliran kedua dimulai dengan hasil alat (ditampilkan sebagai span `anthropic.session.turn` terakhir).

![Contoh trace sesi Managed Agents: POST /chat, empat permintaan event sesi, tiga giliran, satu penggunaan alat bash, dan list\_issues](https://platform.claude.com/docs/id/images/opentelemetry-trace-shape.svg)

SDK di aplikasi Anda memancarkan span [`anthropic.custom_tool_use`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-tool-use-anthropic-mcp-tool-use-and-anthropic-custom-tool-use) dan span klien dari setiap permintaan. Untuk mendapatkan span ini, [siapkan tracing SDK](https://platform.claude.com/docs/id/manage-claude/opentelemetry/sdk).

Span dari sebuah sesi dapat berada di beberapa trace, misalnya ketika Anda mengirim permintaan berikutnya dari root trace baru. Dengan [multiagent](https://platform.claude.com/docs/id/managed-agents/multiagent-orchestration) aktif, sebuah sesi juga dapat memiliki beberapa thread. Untuk menemukan span yang Anda perlukan, kelompokkan berdasarkan ID.

* **Satu thread:** Kelompokkan span berdasarkan `gen_ai.conversation.id`, yang berisi ID thread sesi. Urutkan berdasarkan waktu mulai untuk membaca thread sebagai transkrip.
* **Seluruh sesi, dengan semua thread-nya:** Kelompokkan span berdasarkan `anthropic.session.id`, lintas trace.

Dengan [Full content](https://platform.claude.com/docs/id/manage-claude/opentelemetry#choose-a-content-mode), Anda dapat membaca konten sebuah sesi dari span-nya.

* Untuk membaca konten sebuah giliran, gunakan [span giliran](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-session-turn)-nya. Prompt sistem ada di `gen_ai.system_instructions` pada span giliran pertama sebuah thread, input di `gen_ai.input.messages` (pesan dan hasil alat Anda, event `system.message`, dan pesan dari thread lain), dan output di `gen_ai.output.messages` (pesan agen, penggunaan alat, dan hasil alat).
* Untuk melihat argumen dan hasil dari penggunaan alat, baca [span alat](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-tool-use-anthropic-mcp-tool-use-and-anthropic-custom-tool-use)-nya. Argumen ada di `gen_ai.tool.call.arguments`, dan hasilnya ada di `anthropic.tool_result.content`.

Untuk setiap span dan atributnya, lihat [referensi span OpenTelemetry](https://platform.claude.com/docs/id/api/opentelemetry/spans).

## Penghitungan token

Untuk menghitung setiap token sekali saja, jumlahkan span dari hanya satu sumber untuk setiap permintaan. Ketika permintaan Messages API memiliki span SDK dan span API, jumlahkan span API-nya. Keduanya bernama `anthropic.messages.create`, jadi bedakan berdasarkan jenisnya: span SDK adalah `CLIENT` dan anaknya, span API, adalah `SERVER`.

Untuk setiap sumber, jumlahkan hanya span berikut, karena beberapa atribut penggunaan berulang di lebih dari satu tingkat span API:

* **Span SDK:** Jumlahkan span [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create). Jika sebuah permintaan memiliki [compaction](https://platform.claude.com/docs/id/build-with-claude/compaction), tambahkan juga `anthropic.usage.compaction.input_tokens` dan `anthropic.usage.compaction.output_tokens` dari span tersebut, karena atribut `gen_ai.usage.*` tidak mencakup token compaction. Jika [model fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) melayani sebuah permintaan, span-nya hanya memiliki penggunaan dari model yang melayani respons.
* **Span API dari permintaan Messages API:** Jumlahkan span [`anthropic.messages.create`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-messages-create) atau span [`anthropic.model_request`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-model-request)-nya, bukan keduanya. Jika sebuah permintaan memiliki compaction, tambahkan juga span [`anthropic.compaction`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-compaction)-nya. Jangan tambahkan juga atribut `anthropic.usage.compaction.*` dari span `anthropic.messages.create`, karena atribut tersebut berisi token yang sama.
* **Span API dari sesi Managed Agents:** Jumlahkan span `anthropic.model_request` dan [`anthropic.session.outcome_evaluation`](https://platform.claude.com/docs/id/api/opentelemetry/spans#anthropic-session-outcome-evaluation).

Span dapat tiba lebih dari sekali, misalnya ketika pengiriman dicoba ulang. Jika platform observabilitas Anda tidak menghapus duplikat, hitung setiap span sekali berdasarkan trace ID dan span ID-nya.

`gen_ai.usage.input_tokens` sudah mencakup token yang dibaca dari dan ditulis ke cache prompt, jadi jangan tambahkan atribut cache ke dalamnya. Untuk semua atribut penggunaan, lihat [Penggunaan token](https://platform.claude.com/docs/id/api/opentelemetry/spans#token-usage).

<Note>
  Span yang diekspor tidak dijamin merupakan catatan lengkap penggunaan API Anda. Pengirimannya bersifat [upaya terbaik](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#delivery-and-health), sehingga sebuah span dapat hilang. Pemanggil juga dapat mengecualikan span dari sebuah permintaan dengan menonaktifkan flag sampled di [header `traceparent`](https://platform.claude.com/docs/id/manage-claude/opentelemetry/api#connect-api-spans-to-your-own-traces) permintaan tersebut. Untuk melacak penggunaan setiap kunci API, misalnya untuk mendeteksi kunci yang bocor, gunakan [Usage and Cost Analytics API](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api) dan kelompokkan berdasarkan `api_key_id`. API ini juga menghitung penggunaan permintaan tanpa span. Penggunaan biasanya muncul di sana dalam 4 jam (lihat [Kesegaran data](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api#data-freshness)).
</Note>

## Ketersediaan

OpenTelemetry dalam versi beta di semua model.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tersedia

| Status | Platform cloud               | Model                                                              |
| ------ | ---------------------------- | ------------------------------------------------------------------ |
| Beta   | Semua platform yang didukung | [Semua model](https://platform.claude.com/docs/id/models/overview) |

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tersedia

| Status | Platform cloud               | Model                                                              |
| ------ | ---------------------------- | ------------------------------------------------------------------ |
| Beta   | Semua platform yang didukung | [Semua model](https://platform.claude.com/docs/id/models/overview) |
