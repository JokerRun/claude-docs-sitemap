---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/overview
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 1cc82ed073c46266644bf25de9d13d6a9729f00799167faff6403bdcfade57ab
---

---
title: Ikhtisar Claude Managed Agents
url: https://platform.claude.com/docs/id/managed-agents/overview
description: Harness agen siap pakai dan dapat dikonfigurasi yang berjalan di infrastruktur terkelola. Paling cocok untuk tugas yang berjalan lama dan pekerjaan asinkron.
---

Anthropic menawarkan dua cara untuk membangun dengan Claude, masing-masing cocok untuk kasus penggunaan yang berbeda:

|                        | Messages API                                 | Claude Managed Agents                                                                    |
| ---------------------- | -------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Apa itu**            | Akses prompting model secara langsung        | Harness agen siap pakai yang dapat dikonfigurasi dan berjalan di infrastruktur terkelola |
| **Paling cocok untuk** | Loop agen kustom dan kontrol yang terperinci | Tugas yang berjalan lama dan pekerjaan asinkron                                          |

Claude Managed Agents menyediakan harness dan infrastruktur untuk menjalankan Claude sebagai agen otonom. Alih-alih membangun agent loop (loop agen), eksekusi alat, dan runtime Anda sendiri, Anda mendapatkan lingkungan yang sepenuhnya terkelola tempat Claude dapat membaca file, menjalankan perintah, menjelajahi web, dan menjalankan kode dengan aman. Harness ini mendukung "prompt caching" (caching prompt) bawaan, compaction (pemadatan), dan optimasi performa lainnya untuk output agen yang berkualitas tinggi dan efisien. Untuk membangun loop agen Anda sendiri dengan akses model langsung, lihat [Menggunakan Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages).

<Note>
  Claude Managed Agents juga tersedia di Claude Platform on AWS, dengan beberapa perbedaan dalam ketersediaan fitur dan perilaku sesi. Lihat [Claude Managed Agents](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#claude-managed-agents) dalam panduan Claude Platform on AWS.
</Note>

<CardGroup cols={3}>
  <Card title="Quickstart" icon="play" href="https://platform.claude.com/docs/id/managed-agents/quickstart">
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

| Konsep          | Deskripsi                                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Agent**       | Model, prompt sistem, alat, server MCP, dan skill                                                                                          |
| **Environment** | Konfigurasi untuk tempat sesi dijalankan: sandbox cloud yang dikelola Anthropic, atau sandbox yang di-host sendiri pada infrastruktur Anda |
| **Session**     | Instance agent yang sedang berjalan dalam sebuah environment, menjalankan tugas tertentu dan menghasilkan output                           |
| **Events**      | Pesan yang dipertukarkan antara aplikasi Anda dan agent (giliran pengguna, hasil alat, pembaruan status)                                   |

## Cara kerjanya

<Steps>
  <Step title="Buat agen">
    Tentukan model, prompt sistem, alat, server MCP, dan skill. Buat agen satu kali dan rujuk berdasarkan ID di berbagai sesi.
  </Step>

  <Step title="Buat lingkungan">
    Konfigurasikan tempat agen berjalan: sandbox cloud, atau [sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) di infrastruktur Anda sendiri.
  </Step>

  <Step title="Mulai sesi">
    Luncurkan sesi yang merujuk pada konfigurasi agen dan lingkungan Anda.
  </Step>

  <Step title="Kirim event dan stream respons">
    Kirim pesan pengguna sebagai event. Claude secara otonom menjalankan alat dan melakukan streaming hasilnya kembali melalui "server-sent events" (event yang dikirim server), atau SSE. Riwayat event disimpan di sisi server dan dapat diambil secara lengkap.
  </Step>

  <Step title="Arahkan atau interupsi">
    Kirim event pengguna tambahan untuk memandu agen di tengah eksekusi, atau interupsi agen untuk mengubah arah.
  </Step>
</Steps>

## Kapan menggunakan Claude Managed Agents

Claude Managed Agents paling cocok untuk beban kerja yang membutuhkan:

* **Eksekusi yang berjalan lama:** Tugas yang berjalan selama beberapa menit atau jam dengan banyak pemanggilan alat
* **Infrastruktur cloud:** Sandbox aman dengan paket yang sudah terinstal dan akses jaringan
* **Eksekusi self-hosted:** Sandbox di infrastruktur yang Anda kendalikan untuk kebutuhan kepatuhan atau residensi data
* **Infrastruktur minimal:** Tidak perlu membangun loop agen, sandbox, atau lapisan eksekusi alat Anda sendiri
* **Sesi stateful:** Filesystem dan riwayat percakapan yang persisten di berbagai interaksi
* **Eksekusi terjadwal:** Menjalankan agen secara berulang dengan jadwal cron melalui [deployment terjadwal](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments)

## Alat yang didukung

Claude Managed Agents memberi Claude akses ke sekumpulan alat bawaan:

* **Bash:** Menjalankan perintah shell di sandbox
* **Operasi file:** Membaca, menulis, mengedit, glob, dan grep file di sandbox
* **Pencarian dan pengambilan web:** Mencari di web dan mengambil konten dari URL, secara opsional dibatasi pada allowlist atau blocklist domain
* **Server MCP:** Terhubung ke penyedia alat eksternal

Lihat [Alat](https://platform.claude.com/docs/id/managed-agents/tools) untuk daftar lengkap dan opsi konfigurasi.

## Akses beta

<Note>
  Claude Managed Agents sedang dalam tahap beta. Semua endpoint Managed Agents memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis. Perilaku dapat disempurnakan antar rilis untuk meningkatkan output.
</Note>

Untuk memulai, Anda memerlukan:

1. Sebuah [kunci API Claude](https://platform.claude.com/settings/keys)
2. Header beta `managed-agents-2026-04-01` pada semua permintaan
3. Akses ke Claude Managed Agents (diaktifkan secara default untuk semua akun API)

Dalam beta ini, [MCP tunnels](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview) dan [dreaming](https://platform.claude.com/docs/id/managed-agents/dreams) berada dalam pratinjau riset yang lebih terbatas. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mengaktifkannya.

Claude Managed Agents dirancang bersifat stateful: sesi berjalan lama, dapat dilanjutkan dengan mulus setelah jeda, dan menyimpan riwayat percakapan, status sandbox, serta output di sisi server. Karena itu, Managed Agents saat ini tidak memenuhi syarat untuk [Zero Data Retention](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) atau cakupan HIPAA Business Associate Agreement (BAA). Anda tetap memegang kendali atas data ini: Anda dapat [menghapus sesi](https://platform.claude.com/docs/id/managed-agents/session-operations#deleting-a-session), dan secara terpisah menghapus [file](https://platform.claude.com/docs/id/build-with-claude/files#delete-a-file) apa pun yang Anda unggah, kapan saja melalui API. Untuk kelayakan di seluruh fitur, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).

Lihat [Batas laju](https://platform.claude.com/docs/id/managed-agents/reference#rate-limits) dan [Pedoman branding](https://platform.claude.com/docs/id/managed-agents/reference#branding-guidelines) di referensi.
