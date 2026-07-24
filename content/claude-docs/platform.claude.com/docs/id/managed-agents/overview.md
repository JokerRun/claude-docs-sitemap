---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/overview
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: 7edd66ecd7dd9f3be6a6bb5043aa1978aca83f6f541a9efc193254396bbd0443
---

# Ikhtisar Claude Managed Agents

Harness agen yang sudah jadi dan dapat dikonfigurasi yang berjalan di infrastruktur terkelola. Terbaik untuk tugas yang berjalan lama dan pekerjaan asinkron.

---

Anthropic menawarkan dua cara untuk membangun dengan Claude, masing-masing cocok untuk kasus penggunaan yang berbeda:

|                           | Messages API                                                                 | Claude Managed Agents                                                                          |
| ------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Apa itu**               | Akses langsung untuk memberikan prompt ke model                              | Kerangka agen yang sudah dibangun dan dapat dikonfigurasi, berjalan di infrastruktur terkelola |
| **Paling cocok untuk**    | Loop agen kustom dan kontrol yang sangat terperinci                          | Tugas yang berjalan lama dan pekerjaan asinkron                                                |
| **Pelajari lebih lanjut** | [Dokumentasi Messages API](/docs/id/build-with-claude/working-with-messages) | [Dokumentasi Claude Managed Agents](/docs/id/managed-agents/overview)                          |

Claude Managed Agents menyediakan harness dan infrastruktur untuk menjalankan Claude sebagai agen otonom. Alih-alih membangun loop agen, eksekusi alat, dan runtime Anda sendiri, Anda mendapatkan lingkungan yang sepenuhnya terkelola di mana Claude dapat membaca file, menjalankan perintah, menjelajahi web, dan menjalankan kode dengan aman. Harness ini mendukung "prompt caching" (caching prompt) bawaan, kompaksi, dan optimisasi kinerja lainnya untuk output agen yang berkualitas tinggi dan efisien.

<Note>
  Claude Managed Agents juga tersedia di Claude Platform on AWS, dengan beberapa perbedaan dalam ketersediaan fitur dan perilaku sesi. Lihat [Claude Managed Agents](/docs/id/build-with-claude/claude-platform-on-aws#claude-managed-agents) dalam panduan Claude Platform on AWS.
</Note>

<CardGroup cols={3}>
  <Card title="Mulai cepat" icon="play" href="/docs/id/managed-agents/quickstart">
    Buat sesi agen pertama Anda
  </Card>

  <Card title="Mulai sesi" icon="code-brackets" href="/docs/id/managed-agents/sessions">
    Buat sesi dan kirim event pertama Anda
  </Card>

  <Card title="Referensi" icon="book" href="/docs/id/managed-agents/reference">
    Tipe event, batas laju, flag CLI, dan tabel pencarian lainnya
  </Card>
</CardGroup>

## Konsep inti

Claude Managed Agents dibangun di sekitar empat konsep:

| Konsep          | Deskripsi                                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Agent**       | Model, prompt sistem, alat, server MCP, dan skill                                                                                          |
| **Environment** | Konfigurasi untuk tempat sesi dijalankan: sandbox cloud yang dikelola Anthropic, atau sandbox yang di-host sendiri pada infrastruktur Anda |
| **Session**     | Instance agent yang sedang berjalan dalam sebuah environment, menjalankan tugas tertentu dan menghasilkan output                           |
| **Events**      | Pesan yang dipertukarkan antara aplikasi Anda dan agent (giliran pengguna, hasil alat, pembaruan status)                                   |

## Cara kerjanya

<Steps>
  <Step title="Buat agen">
    Tentukan model, prompt sistem, alat, server MCP, dan skill. Buat agen sekali dan referensikan berdasarkan ID di seluruh sesi.
  </Step>

  <Step title="Buat lingkungan">
    Konfigurasikan di mana agen berjalan: sandbox cloud, atau [sandbox yang dihosting sendiri](/docs/id/managed-agents/self-hosted-sandboxes) di infrastruktur Anda sendiri.
  </Step>

  <Step title="Mulai sesi">
    Luncurkan sesi yang mereferensikan konfigurasi agen dan lingkungan Anda.
  </Step>

  <Step title="Kirim event dan streaming respons">
    Kirim pesan pengguna sebagai event. Claude secara otonom menjalankan alat dan melakukan streaming hasil kembali melalui "server-sent events" (event yang dikirim server), atau SSE. Riwayat event disimpan di sisi server dan dapat diambil secara lengkap.
  </Step>

  <Step title="Arahkan atau interupsi">
    Kirim event pengguna tambahan untuk memandu agen di tengah eksekusi, atau interupsi untuk mengubah arah.
  </Step>
</Steps>

## Kapan menggunakan Claude Managed Agents

Claude Managed Agents paling cocok untuk beban kerja yang membutuhkan:

* **Eksekusi yang berjalan lama:** Tugas yang berjalan selama beberapa menit atau jam dengan beberapa panggilan alat
* **Infrastruktur cloud:** Sandbox aman dengan paket yang sudah terpasang dan akses jaringan
* **Eksekusi yang dihosting sendiri:** Sandbox di infrastruktur yang Anda kendalikan untuk kebutuhan kepatuhan atau residensi data
* **Infrastruktur minimal:** Tidak perlu membangun loop agen, sandbox, atau lapisan eksekusi alat Anda sendiri
* **Sesi stateful:** Sistem file persisten dan riwayat percakapan di beberapa interaksi
* **Eksekusi terjadwal:** Menjalankan agen berulang pada jadwal cron melalui [deployment terjadwal](/docs/id/managed-agents/scheduled-deployments)

## Alat yang didukung

Claude Managed Agents memberi Claude akses ke serangkaian alat bawaan:

* **Bash:** Menjalankan perintah shell di sandbox
* **Operasi file:** Membaca, menulis, mengedit, glob, dan grep file di sandbox
* **Pencarian dan pengambilan web:** Mencari di web dan mengambil konten dari URL
* **Server MCP:** Terhubung ke penyedia alat eksternal

Lihat [Alat](/docs/id/managed-agents/tools) untuk daftar lengkap dan opsi konfigurasi.

## Akses beta

<Note>
  Claude Managed Agents dalam tahap beta. Semua endpoint Managed Agents memerlukan header beta `managed-agents-2026-04-01`. SDK mengatur header beta secara otomatis. Perilaku dapat disempurnakan di antara rilis untuk meningkatkan output.
</Note>

Untuk memulai, Anda memerlukan:

1. [Kunci API Claude](/settings/keys)
2. Header beta `managed-agents-2026-04-01` pada semua permintaan
3. Akses ke Claude Managed Agents (diaktifkan secara default untuk semua akun API)

Dalam beta ini, [tunnel MCP](/docs/id/agents-and-tools/mcp-tunnels/overview) dan [dreaming](/docs/id/managed-agents/dreams) berada dalam pratinjau riset yang lebih terbatas. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mengaktifkannya.

Claude Managed Agents bersifat stateful secara desain: sesi berjalan lama, dilanjutkan dengan bersih setelah jeda, dan menyimpan riwayat percakapan, status sandbox, dan output di sisi server. Karena itu, Managed Agents saat ini tidak memenuhi syarat untuk [Zero Data Retention](/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) atau cakupan HIPAA Business Associate Agreement (BAA). Anda tetap memegang kendali atas data ini: Anda dapat [menghapus sesi](/docs/id/managed-agents/session-operations#deleting-a-session), dan secara terpisah menghapus [file](/docs/id/build-with-claude/files#delete-a-file) apa pun yang Anda unggah, kapan saja melalui API. Untuk kelayakan di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention#feature-eligibility).

Lihat [Batas laju](/docs/id/managed-agents/reference#rate-limits) dan [Pedoman branding](/docs/id/managed-agents/reference#branding-guidelines) di referensi.
