---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/overview
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 930510677379b48408aeab2a6b12241365ca52d95d37aa88ada37671d133ca91
---

---
title: Ikhtisar Claude Managed Agents
url: https://platform.claude.com/docs/id/managed-agents/overview
description: Harness agen siap pakai dan dapat dikonfigurasi yang berjalan di infrastruktur terkelola. Paling cocok untuk tugas yang berjalan lama dan pekerjaan asinkron.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
  zdr:
    eligibility: not-eligible
    note: Tidak memiliki kelayakan ZDR, kecuali untuk Managed Agents yang di-host sendiri. Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya.
  supportedModels:
    - claude-fable-5-2
    - claude-mythos-5-2
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
---

Anthropic menawarkan dua cara untuk membangun dengan Claude, masing-masing cocok untuk kasus penggunaan yang berbeda:

|                        | Messages API                                    | Claude Managed Agents                                                                    |
| ---------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Apa itu**            | Akses langsung untuk memberikan prompt ke model | Harness agen siap pakai yang dapat dikonfigurasi dan berjalan di infrastruktur terkelola |
| **Paling cocok untuk** | Loop agen kustom dan kontrol yang terperinci    | Tugas yang berjalan lama dan pekerjaan asinkron                                          |

Claude Managed Agents menyediakan harness dan infrastruktur untuk menjalankan Claude sebagai agen otonom. Alih-alih membangun loop agen, eksekusi alat, dan runtime Anda sendiri, Anda mendapatkan lingkungan yang sepenuhnya terkelola tempat Claude dapat membaca file, menjalankan perintah, menjelajahi web, dan menjalankan kode dengan aman. Harness ini mendukung “prompt caching” (caching prompt) bawaan, compaction (pemadatan), dan optimasi performa lainnya untuk output agen yang berkualitas tinggi dan efisien. Untuk membangun loop agen Anda sendiri dengan akses model langsung, lihat [Menggunakan Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages).

<Note>
  Claude Managed Agents juga tersedia di Claude Models on Google Cloud (Anthropic managed) dan Claude Platform on AWS, dengan beberapa perbedaan dalam ketersediaan fitur dan perilaku sesi. Lihat panduan [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#claude-managed-agents) atau [Claude Managed Agents](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#claude-managed-agents) dalam panduan Claude Platform on AWS.
</Note>

<CardGroup cols={3}>
  <Card title="Mulai cepat" icon="play" href="https://platform.claude.com/docs/id/managed-agents/quickstart">
    Buat sesi agen pertama Anda
  </Card>

  <Card title="Memulai sesi" icon="code-brackets" href="https://platform.claude.com/docs/id/managed-agents/sessions">
    Buat sesi dan kirim event pertama Anda
  </Card>

  <Card title="Referensi" icon="book" href="https://platform.claude.com/docs/id/managed-agents/reference">
    Jenis event, batas laju, flag CLI, dan tabel rujukan lainnya
  </Card>
</CardGroup>

## Konsep inti

Claude Managed Agents dibangun di atas empat konsep:

| Konsep         | Deskripsi                                                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Agen**       | Model, prompt sistem, alat, server MCP, dan skill                                                                                                 |
| **Lingkungan** | Konfigurasi untuk tempat sesi berjalan: sandbox cloud yang dikelola Anthropic, atau sandbox yang di-hosting sendiri di infrastruktur Anda sendiri |
| **Sesi**       | Instans agen yang sedang berjalan di dalam sebuah environment, melakukan tugas tertentu dan menghasilkan output                                   |
| **Event**      | Pesan yang dipertukarkan antara aplikasi Anda dan agen (giliran pengguna, hasil alat, pembaruan status)                                           |

## Cara kerjanya

<Steps>
  <Step title="Buat agen">
    Tentukan model, prompt sistem, alat, server MCP, dan skill. Buat agen sekali dan rujuk berdasarkan ID di berbagai sesi.
  </Step>

  <Step title="Buat environment">
    [Konfigurasikan tempat agen berjalan](https://platform.claude.com/docs/id/managed-agents/choosing-an-environment): sandbox cloud, atau [sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) di infrastruktur Anda sendiri.
  </Step>

  <Step title="Mulai sesi">
    Luncurkan sesi yang merujuk pada konfigurasi agen dan environment Anda.
  </Step>

  <Step title="Kirim event dan stream respons">
    Kirim pesan pengguna sebagai event. Claude secara otonom menjalankan alat dan melakukan streaming hasilnya kembali melalui “server-sent events” (event yang dikirim server), atau SSE. Layanan Managed Agents menyimpan riwayat event, dan Anda dapat mengambilnya secara lengkap.
  </Step>

  <Step title="Arahkan atau interupsi">
    Kirim event pengguna tambahan untuk memandu agen saat sedang berjalan, atau interupsi agen untuk mengubah arah.
  </Step>
</Steps>

## Kapan menggunakan Claude Managed Agents

Claude Managed Agents paling cocok untuk beban kerja yang membutuhkan:

* **Eksekusi yang berjalan lama:** Tugas yang berjalan selama beberapa menit atau jam dengan banyak pemanggilan alat
* **Infrastruktur cloud:** Sandbox aman dengan paket yang sudah terinstal dan akses jaringan
* **Eksekusi self-hosted:** Sandbox di infrastruktur yang Anda kendalikan untuk kebutuhan kepatuhan atau residensi data
* **Layanan self-hosted:** Seluruh layanan Managed Agents di infrastruktur Anda sendiri, dengan [Claude Managed Agents self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted)
* **Infrastruktur minimal:** Tidak perlu membangun loop agen, sandbox, atau lapisan eksekusi alat Anda sendiri
* **Sesi stateful:** Filesystem dan riwayat percakapan yang persisten di berbagai interaksi
* **Eksekusi terjadwal:** Menjalankan agen secara berulang dengan jadwal cron melalui [deployment terjadwal](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments)

## Alat yang didukung

Claude Managed Agents memberi Claude akses ke serangkaian alat bawaan:

* **Bash:** Menjalankan perintah shell di sandbox
* **Operasi file:** Membaca, menulis, mengedit, glob, dan grep file di sandbox
* **Pencarian dan pengambilan web:** Mencari di web dan mengambil konten dari URL, secara opsional dibatasi pada allowlist atau blocklist domain
* **Server MCP:** Terhubung ke penyedia alat eksternal

Lihat [Alat](https://platform.claude.com/docs/id/managed-agents/tools) untuk daftar lengkap dan opsi konfigurasi.

## Akses beta

<Note>
  Claude Managed Agents sedang dalam tahap beta. Semua endpoint Managed Agents memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis. Anthropic dapat menyempurnakan perilaku antar rilis untuk meningkatkan output.
</Note>

Untuk memulai, Anda memerlukan:

1. Sebuah [kunci API Claude](https://platform.claude.com/settings/keys) dari Claude Console.
2. Header beta `managed-agents-2026-04-01` pada semua permintaan.
3. Akses ke Claude Managed Agents (diaktifkan secara default untuk semua akun API).

Dalam beta ini, [Tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview) dan [dreaming](https://platform.claude.com/docs/id/managed-agents/dreams) berada dalam pratinjau riset yang lebih terbatas. Untuk mengaktifkannya, [minta akses ke pratinjau riset](https://claude.com/form/claude-managed-agents).

Claude Managed Agents dirancang bersifat stateful: sesi berjalan lama, dapat dilanjutkan dengan mulus setelah jeda, dan menyimpan riwayat percakapan, status sandbox, serta output di sisi server. Karena itu, Managed Agents saat ini tidak memenuhi syarat untuk [Zero Data Retention](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) atau cakupan HIPAA Business Associate Agreement (BAA). Pengecualian untuk Zero Data Retention adalah Claude Managed Agents self-hosted, tempat Anda menyimpan data tersebut sendiri, seperti yang dijelaskan dalam [Berapa lama data disimpan](https://platform.claude.com/docs/id/managed-agents/self-hosted-data-and-access#how-long-data-is-kept). Anda tetap memegang kendali atas data ini: Anda dapat [menghapus sesi](https://platform.claude.com/docs/id/managed-agents/session-operations#deleting-a-session), dan secara terpisah menghapus [file](https://platform.claude.com/docs/id/build-with-claude/files#delete-a-file) apa pun yang Anda unggah, kapan saja melalui API. Untuk kelayakan di seluruh fitur, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).

Lihat [Batas laju](https://platform.claude.com/docs/id/managed-agents/reference#rate-limits) dan [Pedoman branding](https://platform.claude.com/docs/id/managed-agents/reference#branding-guidelines) di referensi.

## Ketersediaan

Managed Agents dalam versi beta di semua model.

### Dukungan API

| Status | Platform cloud                                                                                                                                                                                                                                                                 | Model                                                              |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| Beta   | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed) | [Semua model](https://platform.claude.com/docs/id/models/overview) |

### Header beta yang diperlukan

[Ikhtisar header beta](https://platform.claude.com/docs/id/api/beta-headers)

Header beta memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

* `managed-agents-2026-04-01`

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                                                                                                                                                     | HIPAA                                                                        |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Status | Tidak layak                                                                                                                                                                                                                                                                                          | Tidak layak                                                                  |
| Detail | Tidak memiliki kelayakan ZDR, kecuali untuk Managed Agents yang di-host sendiri. Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/managed-agents/self-hosted-data-and-access#how-long-data-is-kept) | Tidak memiliki kelayakan HIPAA. Berlaku untuk semua subfitur Managed Agents. |

Endpoint yang berlaku:

* `/v1/agents`
* `/v1/sessions`
* `/v1/environments`
