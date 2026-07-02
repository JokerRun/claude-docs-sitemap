---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/overview
fetched_at: 2026-07-02T03:13:49.360020Z
sha256: 70e77d387a7a1db48a9d0b92f3a4de7d6ccc90110c257a6367e7e6c24b0b7c5e
---

# Ikhtisar Claude Managed Agents

Harness agen yang telah dibangun sebelumnya dan dapat dikonfigurasi yang berjalan di infrastruktur terkelola. Paling cocok untuk tugas yang berjalan lama dan pekerjaan asinkron.

---

Anthropic menawarkan dua cara untuk membangun dengan Claude, masing-masing cocok untuk kasus penggunaan yang berbeda:

|                           | Messages API                                                                 | Claude Managed Agents                                                                          |
| ------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Apa itu**               | Akses langsung untuk memberikan prompt ke model                              | Kerangka agen yang sudah dibangun dan dapat dikonfigurasi, berjalan di infrastruktur terkelola |
| **Paling cocok untuk**    | Loop agen kustom dan kontrol yang sangat terperinci                          | Tugas yang berjalan lama dan pekerjaan asinkron                                                |
| **Pelajari lebih lanjut** | [Dokumentasi Messages API](/docs/id/build-with-claude/working-with-messages) | [Dokumentasi Claude Managed Agents](/docs/id/managed-agents/overview)                          |

Claude Managed Agents menyediakan harness dan infrastruktur untuk menjalankan Claude sebagai agen otonom. Alih-alih membangun loop agen, eksekusi alat, dan runtime Anda sendiri, Anda mendapatkan lingkungan yang sepenuhnya terkelola di mana Claude dapat membaca file, menjalankan perintah, menjelajahi web, dan mengeksekusi kode dengan aman. Harness ini mendukung caching prompt bawaan, pemadatan, dan optimasi performa lainnya untuk menghasilkan output agen yang berkualitas tinggi dan efisien.

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
    Tipe event, batas laju, flag CLI, dan tabel referensi lainnya
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
    Tentukan model, prompt sistem, alat, server MCP, dan skill. Buat agen satu kali dan referensikan berdasarkan ID di seluruh sesi.
  </Step>

  <Step title="Buat environment">
    Konfigurasikan tempat agen berjalan: sandbox cloud, atau [sandbox self-hosted](/docs/id/managed-agents/self-hosted-sandboxes) di infrastruktur Anda sendiri.
  </Step>

  <Step title="Mulai sesi">
    Luncurkan sesi yang mereferensikan konfigurasi agen dan environment Anda.
  </Step>

  <Step title="Kirim event dan stream respons">
    Kirim pesan pengguna sebagai event. Claude secara otonom mengeksekusi alat dan mengalirkan kembali hasilnya melalui "server-sent events" (peristiwa yang dikirim server), atau SSE. Riwayat event disimpan di sisi server dan dapat diambil secara lengkap.
  </Step>

  <Step title="Arahkan atau interupsi">
    Kirim event pengguna tambahan untuk memandu agen di tengah eksekusi, atau interupsi untuk mengubah arah.
  </Step>
</Steps>

## Kapan menggunakan Claude Managed Agents

Claude Managed Agents paling cocok untuk beban kerja yang membutuhkan:

* **Eksekusi jangka panjang:** Tugas yang berjalan selama beberapa menit atau jam dengan banyak pemanggilan alat
* **Infrastruktur cloud:** Sandbox aman dengan paket yang sudah terinstal dan akses jaringan
* **Eksekusi self-hosted:** Sandbox di infrastruktur yang Anda kendalikan untuk kebutuhan kepatuhan atau residensi data
* **Infrastruktur minimal:** Tidak perlu membangun loop agen, sandbox, atau lapisan eksekusi alat Anda sendiri
* **Sesi stateful:** Filesystem persisten dan riwayat percakapan di seluruh interaksi
* **Eksekusi terjadwal:** Agen yang berjalan berulang sesuai jadwal cron melalui [scheduled deployments](/docs/id/managed-agents/scheduled-deployments)

## Alat yang didukung

Claude Managed Agents memberi Claude akses ke serangkaian alat bawaan:

* **Bash:** Menjalankan perintah shell di dalam sandbox
* **Operasi file:** Membaca, menulis, mengedit, glob, dan grep file di dalam sandbox
* **Pencarian dan pengambilan web:** Mencari di web dan mengambil konten dari URL
* **Server MCP:** Terhubung ke penyedia alat eksternal

Lihat [Alat](/docs/id/managed-agents/tools) untuk daftar lengkap dan opsi konfigurasi.

## Akses beta

<Note>
  Claude Managed Agents saat ini dalam tahap beta. Semua endpoint Managed Agents memerlukan header beta `managed-agents-2026-04-01`. SDK menetapkan header beta secara otomatis. Perilaku dapat disempurnakan di antara rilis untuk meningkatkan output.
</Note>

Untuk memulai, Anda memerlukan:

1. [Kunci API Claude](/settings/keys)
2. Header beta `managed-agents-2026-04-01` pada semua permintaan
3. Akses ke Claude Managed Agents (diaktifkan secara default untuk semua akun API)

Dalam beta ini, [MCP tunnels](/docs/id/agents-and-tools/mcp-tunnels/overview) dan [dreaming](/docs/id/managed-agents/dreams) berada dalam pratinjau riset yang lebih terbatas. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mengaktifkannya.

Claude Managed Agents bersifat stateful secara desain: sesi berjalan lama, dapat dilanjutkan dengan mulus setelah jeda, dan menyimpan riwayat percakapan, status sandbox, serta output di sisi server. Karena itu, Managed Agents saat ini tidak memenuhi syarat untuk [Zero Data Retention](/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) atau cakupan HIPAA Business Associate Agreement (BAA). Anda tetap memegang kendali atas data ini: Anda dapat [menghapus sesi](/docs/id/managed-agents/session-operations#deleting-a-session), dan secara terpisah menghapus [file](/docs/id/build-with-claude/files#delete-a-file) apa pun yang Anda unggah, kapan saja melalui API. Untuk kelayakan di seluruh fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention#feature-eligibility).

Lihat [Batas laju](/docs/id/managed-agents/reference#rate-limits) dan [Pedoman branding](/docs/id/managed-agents/reference#branding-guidelines) di referensi.
