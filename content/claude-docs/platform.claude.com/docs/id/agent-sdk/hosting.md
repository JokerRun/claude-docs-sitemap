---
source: platform
url: https://platform.claude.com/docs/id/agent-sdk/hosting
fetched_at: 2026-02-06T04:18:04.377404Z
sha256: 2efbc1108bd39cd5c4cd7a51ff45464f41b361f1ce35a0fe5f368be52b4cb836
---

# Hosting the Agent SDK

Sebarkan dan hosting Claude Agent SDK di lingkungan produksi

---

Claude Agent SDK berbeda dari API LLM stateless tradisional karena mempertahankan status percakapan dan menjalankan perintah di lingkungan yang persisten. Panduan ini mencakup arsitektur, pertimbangan hosting, dan praktik terbaik untuk menyebarkan agen berbasis SDK dalam produksi.

<Info>
Untuk pengerasan keamanan di luar sandboxing dasar—termasuk kontrol jaringan, manajemen kredensial, dan opsi isolasi—lihat [Secure Deployment](/docs/id/agent-sdk/secure-deployment).
</Info>

## Persyaratan Hosting

### Sandboxing Berbasis Container

Untuk keamanan dan isolasi, SDK harus berjalan di dalam lingkungan container yang tersandbox. Ini menyediakan isolasi proses, batas sumber daya, kontrol jaringan, dan sistem file yang bersifat sementara.

SDK juga mendukung [konfigurasi sandbox terprogram](/docs/id/agent-sdk/typescript#sandbox-settings) untuk eksekusi perintah.

### Persyaratan Sistem

Setiap instans SDK memerlukan:

- **Dependensi runtime**
  - Python 3.10+ (untuk Python SDK) atau Node.js 18+ (untuk TypeScript SDK)
  - Node.js (diperlukan oleh Claude Code CLI)
  - Claude Code CLI: `npm install -g @anthropic-ai/claude-code`

- **Alokasi sumber daya**
  - Direkomendasikan: 1GiB RAM, 5GiB disk, dan 1 CPU (sesuaikan ini berdasarkan tugas Anda sesuai kebutuhan)

- **Akses jaringan**
  - HTTPS keluar ke `api.anthropic.com`
  - Opsional: Akses ke server MCP atau alat eksternal

## Memahami Arsitektur SDK

Tidak seperti panggilan API stateless, Claude Agent SDK beroperasi sebagai **proses yang berjalan lama** yang:
- **Menjalankan perintah** di lingkungan shell yang persisten
- **Mengelola operasi file** dalam direktori kerja
- **Menangani eksekusi alat** dengan konteks dari interaksi sebelumnya

## Opsi Penyedia Sandbox

Beberapa penyedia mengkhususkan diri dalam lingkungan container aman untuk eksekusi kode AI:

- **[Modal Sandbox](https://modal.com/docs/guide/sandbox)** - [implementasi demo](https://modal.com/docs/examples/claude-slack-gif-creator)
- **[Cloudflare Sandboxes](https://github.com/cloudflare/sandbox-sdk)**
- **[Daytona](https://www.daytona.io/)**
- **[E2B](https://e2b.dev/)**
- **[Fly Machines](https://fly.io/docs/machines/)**
- **[Vercel Sandbox](https://vercel.com/docs/functions/sandbox)**

Untuk opsi self-hosted (Docker, gVisor, Firecracker) dan konfigurasi isolasi terperinci, lihat [Isolation Technologies](/docs/id/agent-sdk/secure-deployment#isolation-technologies).

## Pola Penyebaran Produksi

### Pola 1: Sesi Ephemeral

Buat container baru untuk setiap tugas pengguna, kemudian hancurkan saat selesai.

Terbaik untuk tugas sekali jalan, pengguna mungkin masih berinteraksi dengan AI saat tugas sedang diselesaikan, tetapi setelah selesai container dihancurkan.

**Contoh:**
- Investigasi & Perbaikan Bug: Debug dan selesaikan masalah spesifik dengan konteks yang relevan
- Pemrosesan Invoice: Ekstrak dan strukturkan data dari kwitansi/invoice untuk sistem akuntansi
- Tugas Terjemahan: Terjemahkan dokumen atau batch konten antar bahasa
- Pemrosesan Gambar/Video: Terapkan transformasi, optimasi, atau ekstrak metadata dari file media

### Pola 2: Sesi Berjalan Lama

Pertahankan instans container persisten untuk tugas yang berjalan lama. Sering kali menjalankan **beberapa** proses Claude Agent di dalam container berdasarkan permintaan.

Terbaik untuk agen proaktif yang mengambil tindakan tanpa masukan pengguna, agen yang melayani konten atau agen yang memproses jumlah pesan yang tinggi.

**Contoh:**
- Email Agent: Memantau email masuk dan secara otomatis melakukan triase, merespons, atau mengambil tindakan berdasarkan konten
- Site Builder: Menghost situs web khusus per pengguna dengan kemampuan pengeditan langsung yang disajikan melalui port container
- Chat Bot Frekuensi Tinggi: Menangani aliran pesan berkelanjutan dari platform seperti Slack di mana waktu respons cepat sangat penting

### Pola 3: Sesi Hybrid

Container ephemeral yang dihidrasi dengan riwayat dan status, mungkin dari database atau dari fitur resumption sesi SDK.

Terbaik untuk container dengan interaksi intermiten dari pengguna yang memulai pekerjaan dan berhenti saat pekerjaan selesai tetapi dapat dilanjutkan.

**Contoh:**
- Personal Project Manager: Membantu mengelola proyek berkelanjutan dengan check-in intermiten, mempertahankan konteks tugas, keputusan, dan kemajuan
- Deep Research: Melakukan tugas penelitian multi-jam, menyimpan temuan dan melanjutkan investigasi saat pengguna kembali
- Customer Support Agent: Menangani tiket dukungan yang mencakup beberapa interaksi, memuat riwayat tiket dan konteks pelanggan

### Pola 4: Container Tunggal

Jalankan beberapa proses Claude Agent SDK dalam satu container global.

Terbaik untuk agen yang harus berkolaborasi erat satu sama lain. Ini mungkin pola yang paling tidak populer karena Anda harus mencegah agen saling menimpa.

**Contoh:**
- **Simulasi**: Agen yang berinteraksi satu sama lain dalam simulasi seperti video game.

# FAQ

### Bagaimana cara saya berkomunikasi dengan sandbox saya?
Saat hosting di container, ekspos port untuk berkomunikasi dengan instans SDK Anda. Aplikasi Anda dapat mengekspos endpoint HTTP/WebSocket untuk klien eksternal sementara SDK berjalan secara internal dalam container.

### Berapa biaya hosting container?
Kami telah menemukan bahwa biaya dominan untuk melayani agen adalah token, container bervariasi berdasarkan apa yang Anda sediakan tetapi biaya minimum kira-kira 5 sen per jam berjalan.

### Kapan saya harus mematikan container idle vs. menjaganya tetap hangat?
Ini mungkin tergantung penyedia, penyedia sandbox yang berbeda akan membiarkan Anda menetapkan kriteria berbeda untuk idle timeout setelah itu sandbox mungkin berhenti.
Anda akan ingin menyetel timeout ini berdasarkan seberapa sering Anda pikir respons pengguna mungkin terjadi.

### Seberapa sering saya harus memperbarui Claude Code CLI?
Claude Code CLI diversi dengan semver, jadi perubahan breaking apa pun akan diversi.

### Bagaimana cara saya memantau kesehatan container dan kinerja agen?
Karena container hanyalah server, infrastruktur logging yang sama yang Anda gunakan untuk backend akan bekerja untuk container.

### Berapa lama sesi agen dapat berjalan sebelum timeout?
Sesi agen tidak akan timeout, tetapi kami merekomendasikan menetapkan properti 'maxTurns' untuk mencegah Claude terjebak dalam loop.

## Langkah Selanjutnya

- [Secure Deployment](/docs/id/agent-sdk/secure-deployment) - Kontrol jaringan, manajemen kredensial, dan pengerasan isolasi
- [TypeScript SDK - Sandbox Settings](/docs/id/agent-sdk/typescript#sandbox-settings) - Konfigurasi sandbox secara terprogram
- [Sessions Guide](/docs/id/agent-sdk/sessions) - Pelajari tentang manajemen sesi
- [Permissions](/docs/id/agent-sdk/permissions) - Konfigurasi izin alat
- [Cost Tracking](/docs/id/agent-sdk/cost-tracking) - Pantau penggunaan API
- [MCP Integration](/docs/id/agent-sdk/mcp) - Perluas dengan alat khusus