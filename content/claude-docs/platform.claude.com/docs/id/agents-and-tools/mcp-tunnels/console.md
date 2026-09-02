---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 984c2e3a68140a736ecb10430c9546336b81ee6609e7e8abf3aa74719fcaa1b8
---

---
title: Mengelola tunnel di Console
url: https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console
description: Buat tunnel, daftarkan sertifikat CA, ambil token tunnel, dan lampirkan server MCP yang di-tunnel ke agen dari Claude Console.
---

<Note>
  Tunnel MCP sedang dalam pratinjau riset. [Minta akses](https://claude.com/form/claude-managed-agents) untuk mencobanya.
</Note>

Halaman ini membahas sisi Console dari deployment MCP tunnels: membuat tunnel, mendaftarkan sertifikat CA Anda, mengambil token tunnel, dan melampirkan [server MCP upstream](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) ke agen. [Deploy MCP tunnels dengan Helm](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-helm) dan [Deploy MCP tunnels dengan Docker Compose](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose) membahas cara menjalankan [tunnel stack](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) di dalam jaringan Anda.

## Prasyarat

* **Satu atau lebih server MCP** yang berjalan di jaringan privat Anda. Tunnel merutekan lalu lintas ke server tersebut; tunnel tidak meng-host-nya. Lihat [Server MCP jarak jauh](https://platform.claude.com/docs/id/agents-and-tools/remote-mcp-servers) untuk contoh yang dapat Anda deploy.

* **Peran Console dengan izin Manage tunnels**, sehingga Anda dapat membuat dan mengarsipkan tunnel, merotasi token, dan mengelola sertifikat. Admin dan pemilik organisasi memilikinya secara default; peran kustom dan pemberian izin per akun juga dapat menyertakannya. Peran tanpa izin ini memiliki akses hanya-baca ke halaman **MCP tunnels** dan detail tunnel.

* **Cara bagi stack Anda untuk melakukan autentikasi ke Tunnels API.** Pilih salah satu:

  * **[Akses programatik](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#credential-provisioning) (direkomendasikan).** Siapkan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) selama pembuatan tunnel sehingga stack Anda mencetak token API berumur pendek dari penyedia identitas Anda, mengambil token tunnel, serta membuat dan mendaftarkan sertifikat CA secara otomatis. Memerlukan izin untuk mengelola aturan federasi, issuer OIDC yang terdaftar, dan aturan federasi dengan scope `workspace:manage_tunnels`.
  * **[Manual](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#credential-provisioning).** Lewati akses programatik. Setelah membuat tunnel, [dapatkan token tunnel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#get-the-connection-details), buat dan [daftarkan sertifikat CA](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate) sendiri, lalu berikan token dan sertifikat server Anda ke tunnel stack sebagai secret.

## Membuat tunnel

<Steps>
  <Step title="Buka halaman MCP tunnels">
    Di sidebar Console, buka **Manage > MCP tunnels**. Tunnel memiliki cakupan workspace; tunnel baru menjadi milik workspace yang saat ini dipilih di Console, jadi ganti workspace terlebih dahulu jika Anda ingin menempatkannya di tempat lain.
  </Step>

  <Step title="Beri nama tunnel">
    Klik **New tunnel** dan masukkan nama di dialog **Create tunnel**. Nama wajib diisi dan mengidentifikasi tunnel di daftar, di halaman detail, dan di pemilih server MCP agen. Domain dengan bentuk `abcd1234.tunnel.anthropic.com` ditetapkan secara otomatis.
  </Step>

  <Step title="Opsional: siapkan akses programatik">
    Jika peran Anda dapat mengelola aturan federasi, toggle **Set up programmatic access** akan muncul (nonaktif secara default). Jika tidak, Console menampilkan pemberitahuan sebagai gantinya dan tunnel stack Anda menggunakan alur manual. Sisa alur pembuatan sama untuk kedua kasus.

    Akses programatik bergantung pada [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation); baca halaman tersebut terlebih dahulu jika issuer federasi, aturan, dan service account belum familier bagi Anda. Untuk mengaktifkan toggle, Anda memerlukan:

    1. **Issuer OIDC yang terdaftar** untuk penyedia identitas tempat stack Anda menyajikan token (seperti cluster Kubernetes, AWS IAM, Google Cloud, atau GitHub Actions). Daftarkan satu di bawah **Settings > Workload identity > Issuers** jika organisasi Anda belum memilikinya.
    2. **Aturan federasi dengan scope `workspace:manage_tunnels`.** Mengaktifkan toggle akan menampilkan pemilih **Federation rule**. Pilih aturan yang sudah ada dengan scope tersebut, atau klik **Create federation rule** untuk membuatnya secara inline.
    3. **Service account milik aturan tersebut ditambahkan ke workspace ini.** Tunnels API melakukan otorisasi berdasarkan keanggotaan workspace dari service account. Jika Anda membuat tunnel di workspace selain workspace default organisasi, tambahkan service account di bawah **Settings > Workspaces** dan berikan ID workspace saat deploy (`api.wif.workspaceId` untuk Helm, `ANTHROPIC_WORKSPACE_ID` untuk Compose).

    Melewati langkah ini didukung sepenuhnya; kedua panduan deploy memiliki tab **Without programmatic access**.
  </Step>

  <Step title="Buat tunnel">
    Klik **Create tunnel**. Console menyediakan tunnel dan membuka halaman detail.
  </Step>

  <Step title="Catat pengidentifikasi deployment">
    Kedua jalur deploy memerlukan:

    * **ID tunnel** (`tnl_...`), ditampilkan di halaman detail tunnel.
    * **Domain tunnel** (`abcd1234.tunnel.anthropic.com`), ditampilkan di halaman detail tunnel. Digunakan sebagai `tunnel_domain` proxy dan di SAN sertifikat server.

    Hal lain yang Anda perlukan bergantung pada [mode penyediaan kredensial](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#credential-provisioning):

    | Dengan akses programatik                                                                                                                                                                         | Tanpa akses programatik                                                                                                                                                                                                                                      |
    | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | **ID aturan federasi** (`fdrl_...`) dari aturan yang Anda pilih. Aturan ini berada di tingkat organisasi, tidak disimpan pada tunnel; temukan di bawah **Settings > Workload identity > Rules**. | **Token tunnel**, ditampilkan dengan ikon mata di sebelah **Token** pada halaman detail. Perlakukan sebagai secret. Lihat [Mendapatkan detail koneksi](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#get-the-connection-details). |
    | **ID organisasi** (sebuah UUID), ditampilkan di bawah **Settings > Organization**.                                                                                                               | **Sertifikat CA** yang Anda buat dan [daftarkan pada tunnel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate).                                                                                                 |

    Dengan akses programatik, stack Anda mengambil token tunnel melalui Tunnels API, membuat CA dan sertifikat server secara lokal (private key tidak pernah meninggalkan lingkungan Anda), dan hanya mendaftarkan sertifikat publik CA ke Anthropic. Anda tetap bertanggung jawab untuk mengamankan private key dan memperbarui sertifikat server sebelum kedaluwarsa.
  </Step>
</Steps>

Organisasi Anda dapat memiliki hingga 10 tunnel aktif. Membuat tunnel tidak membangun konektivitas apa pun; hal itu terjadi setelah stack Anda terhubung menggunakan token tunnel dan sertifikat CA telah didaftarkan.

## Mendapatkan detail koneksi

Buka tunnel. Halaman detail menampilkan bagian **Connection** dengan domain dan token serta bagian **Certificates**.

| Field      | Deskripsi                                                                                                                                                                                                                           |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Domain** | Salin nilai `abcd1234.tunnel.anthropic.com` yang ditetapkan. Rute proxy Anda adalah subdomain dari domain ini.                                                                                                                      |
| **Token**  | Klik ikon mata (**Show token**) untuk mengambil token tunnel, lalu gunakan ikon salin untuk menyalinnya ke penyimpanan secret tunnel stack Anda. Klik **Rotate token** untuk membatalkan token saat ini dan menerbitkan token baru. |

<Note>
  Setiap penampilan dan rotasi token dicatat dalam log aktivitas [Compliance API](https://platform.claude.com/docs/id/manage-claude/compliance-api) organisasi Anda. Rotasi tidak memutus koneksi cloudflared yang sudah terbentuk, sehingga Anda dapat merotasi, melakukan deploy ulang dengan nilai baru, dan membiarkan koneksi lama terkuras.
</Note>

## Menambahkan sertifikat CA

Anthropic memverifikasi [inner TLS](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) ke [proxy](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/concepts#components) Anda terhadap sertifikat CA yang Anda daftarkan pada tunnel. Tunnel tanpa sertifikat aktif tidak dapat menerima koneksi, dan tidak muncul di pemilih server MCP agen hingga satu sertifikat didaftarkan.

<Steps>
  <Step title="Temukan bagian Certificates">
    Di halaman detail tunnel, gulir ke bagian **Certificates** dan klik **Add certificate**.
  </Step>

  <Step title="Berikan sertifikat">
    Klik **Choose file** untuk memilih file `.pem`, `.crt`, atau `.cer`, seret file ke area teks, atau tempel blok PEM secara langsung. Modal menolak materi private key dan konten yang bukan blok `-----BEGIN CERTIFICATE-----`. File harus berukuran 8 kB atau lebih kecil.
  </Step>

  <Step title="Tambahkan sertifikat">
    Klik **Add certificate**. Fingerprint dan masa berlaku muncul di daftar sertifikat, dan jumlah slot pada header bagian bertambah.
  </Step>
</Steps>

Sebuah tunnel menampung hingga dua sertifikat aktif sehingga Anda dapat merotasi tanpa downtime: daftarkan sertifikat baru berdampingan dengan yang lama, deploy ulang proxy Anda dengan pasangan kunci baru, pastikan lalu lintas mengalir, lalu klik **Revoke** pada baris sertifikat lama. Sertifikat yang dicabut tetap terlihat di daftar dengan badge **Revoked**.

## Deploy tunnel stack

Tunnel sudah ada di Console, tetapi tidak ada lalu lintas yang mengalir hingga tunnel stack berjalan di dalam jaringan Anda dan terhubung menggunakan token tunnel. Ikuti salah satu panduan deploy:

<CardGroup cols={2}>
  <Card title="Deploy dengan Docker Compose" icon="cube" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-compose">
    Jalankan tunnel stack pada satu host. Mencakup alur akses programatik dan manual.
  </Card>

  <Card title="Deploy dengan Helm" icon="stack" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-helm">
    Jalankan tunnel stack pada cluster Kubernetes. Mencakup alur akses programatik dan manual.
  </Card>
</CardGroup>

## Menggunakan tunnel dalam agen

Setelah stack Anda berjalan dan memiliki satu atau lebih server MCP yang dikonfigurasi, lampirkan server MCP upstream ke sesi Managed Agent. Untuk memanggil server yang sama dari Messages API, lihat [Menggunakan server MCP yang di-tunnel](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview#use-the-tunneled-mcp-servers).

<Note>
  Pemilih hanya menampilkan tunnel dengan setidaknya satu sertifikat aktif. Tunnel yang masih menampilkan **Needs certificate** di daftar **MCP tunnels** tidak muncul di dropdown; daftarkan sertifikat CA terlebih dahulu. Pemilih juga memiliki cakupan workspace: pemilih mencantumkan tunnel di workspace yang sama dengan sesi, bukan workspace lain.
</Note>

<Steps>
  <Step title="Buka modal New session">
    Buka **Managed Agents > Sessions** dan klik **New session**.
  </Step>

  <Step title="Definisikan agen inline">
    Di pemilih agen, pilih **Create new agent** sehingga Anda dapat mengedit daftar server MCP secara langsung.
  </Step>

  <Step title="Tambahkan server MCP">
    Klik **+ MCP Server** dan buka dropdown. Tunnel yang dibuat di workspace saat ini muncul di bagian atas daftar, di atas katalog konektor publik. Pilih tunnel yang berada di depan server yang ingin Anda jangkau.
  </Step>

  <Step title="Berikan perutean">
    Kartu menampilkan dua field opsional: **Subdomain** (ditambahkan di depan domain tunnel) dan **Path** (ditambahkan setelahnya). Isi salah satu atau keduanya, bergantung pada cara rute proxy Anda dikonfigurasi. Baris **Resolves to** menampilkan URL server MCP lengkap yang dihubungi agen.
  </Step>
</Steps>

<Note>
  Tunnel membawa lalu lintas; tunnel tidak melakukan autentikasi ke server MCP upstream. Konfigurasikan OAuth atau autentikasi bearer pada server MCP dengan cara yang sama seperti server MCP lainnya.
</Note>

## Mengarsipkan tunnel

Pengarsipan segera menghentikan tunnel dari menerima koneksi dan bersifat permanen.

Di daftar **MCP tunnels**, buka menu baris untuk tunnel tersebut dan pilih **Archive**. Tunnel yang diarsipkan tetap terlihat saat Anda memfilter daftar berdasarkan **Archived** atau **All**.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Deploy dengan Helm" icon="stack" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/deploy-helm">
    Instal pada cluster Kubernetes menggunakan Helm chart Anthropic.
  </Card>

  <Card title="Keamanan" icon="lock" href="https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/security">
    Panduan hardening, rotasi kredensial, dan respons terhadap pelanggaran.
  </Card>
</CardGroup>
