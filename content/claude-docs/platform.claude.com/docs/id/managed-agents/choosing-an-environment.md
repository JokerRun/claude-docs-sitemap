---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/choosing-an-environment
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 1fe5dd0be1c71987bd752410af2f1d037d32df9fdb3f2bea8c9e94a01468cda6
---

---
title: Memilih lingkungan agen
url: https://platform.claude.com/docs/id/managed-agents/choosing-an-environment
description: Tentukan apakah alat dan kode Claude Managed Agents berjalan di lingkungan cloud yang dikelola Anthropic atau di sandbox yang di-host sendiri, dan lihat apa yang berubah jika Anda beralih.
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
  zdr:
    eligibility: not-eligible
    note: Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya. Berlaku untuk semua subfitur Managed Agents, termasuk Sandbox yang di-host sendiri.
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
---

Sebuah “environment” (lingkungan) menentukan tempat alat dan kode agen Anda berjalan. Alat dan kode tersebut berjalan di dalam sandbox. Sandbox adalah ruang kerja terisolasi, seperti container, tempat agen menjalankan perintah dan mengerjakan file. Anda memiliki dua opsi:

* **Lingkungan cloud:** Anthropic menjalankan sandbox untuk Anda. Setiap sesi mendapatkan container Linux baru miliknya sendiri di infrastruktur yang dikelola Anthropic, dengan bahasa pemrograman, database, dan utilitas umum yang sudah terinstal. Anda memilih aturan jaringannya dan paket tambahan apa pun yang akan diinstal.
* **Sandbox yang di-host sendiri:** Anda menjalankan sandbox di infrastruktur Anda sendiri. Claude tetap berjalan di sisi Anthropic dan menentukan alat mana yang akan dipanggil berikutnya. Sebuah program yang Anda jalankan, yang disebut “worker” (pekerja), menjalankan panggilan alat bash dan file milik agen di mesin Anda dan mengirimkan setiap hasilnya kembali. Program ini juga dapat menyajikan alat kustom.

Definisi agen tetap sama apa pun pilihan Anda. Anda mengatur model, prompt, dan alat pada [agen](https://platform.claude.com/docs/id/managed-agents/agent-setup), bukan pada lingkungan.

## Mulai dengan lingkungan cloud

Jika Anda tidak yakin mana yang harus dipilih, atau Anda baru mengenal Claude Managed Agents, mulailah dengan [lingkungan cloud](https://platform.claude.com/docs/id/managed-agents/environments), seperti yang dilakukan dalam [panduan memulai cepat](https://platform.claude.com/docs/id/managed-agents/quickstart). Anthropic menjalankan container terisolasi untuk setiap sesi, dengan bahasa pemrograman dan alat umum yang sudah terinstal, sehingga tidak ada yang perlu Anda host. Pilih sandbox yang di-host sendiri hanya jika alat harus berjalan di infrastruktur yang Anda kendalikan.

## Bandingkan opsi-opsinya

Tabel berikut membandingkan kedua opsi tersebut.

|                                       | [Lingkungan cloud](https://platform.claude.com/docs/id/managed-agents/environments) (default)                                                                                                                                                            | [Sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes)                    |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Tempat alat dan kode berjalan         | Sandbox yang dikelola Anthropic                                                                                                                                                                                                                          | Worker Anda, di infrastruktur Anda                                                                                          |
| Apa yang sampai ke Anthropic          | [Riwayat percakapan](https://platform.claude.com/docs/id/managed-agents/events-and-streaming#list-past-events), [hasil alat](https://platform.claude.com/docs/id/managed-agents/tools#available-tools), file dan status sandbox, skill, dan memory store | Riwayat percakapan, hasil alat, skill, dan memory store. File dan proses sandbox tetap berada di worker Anda.               |
| Apa yang Anda operasikan              | Tidak ada                                                                                                                                                                                                                                                | Host worker, pengerasan keamanannya, batasan jaringannya, dan kunci lingkungan yang digunakan worker Anda untuk autentikasi |
| Jangkauan jaringan                    | Aturan jaringan yang Anda atur pada lingkungan                                                                                                                                                                                                           | Kebijakan jaringan Anda sendiri                                                                                             |
| Pemasangan file dan repositori GitHub | Dikelola oleh Anthropic                                                                                                                                                                                                                                  | Dikelola oleh Anda                                                                                                          |
| Memory store                          | Dipasang oleh Anthropic di `/mnt/memory/`                                                                                                                                                                                                                | Diunduh ke `/mnt/memory/` dan disinkronkan oleh worker                                                                      |
| Siklus hidup sandbox                  | Dikelola oleh Anthropic                                                                                                                                                                                                                                  | Dikelola oleh Anda                                                                                                          |
| Pilih ketika                          | Default. Alat tidak perlu berjalan di infrastruktur Anda sendiri.                                                                                                                                                                                        | Alat harus berjalan di infrastruktur yang Anda kendalikan.                                                                  |

## Kapan memilih sandbox yang di-host sendiri

Sandbox yang di-host sendiri cocok ketika agen perlu melakukan salah satu hal berikut:

* **Mengerjakan data yang tidak boleh keluar dari jaringan Anda:** File dan proses agen tetap berada di worker Anda. Apa yang dikembalikan alat ke model tetap sampai ke layanan Managed Agents.
* **Menjangkau layanan internal yang tidak dapat dirutekan secara publik:** Alat bash dan file milik agen, serta alat kustom apa pun yang disajikan worker Anda, berjalan di dalam jaringan Anda. Anthropic, bukan worker Anda, yang terhubung ke server MCP milik agen. Server MCP privat mungkin berada di depan sistem tiket internal atau wiki perusahaan Anda. Untuk menjangkaunya, Anda dapat menggunakan [tunnel MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-tunnels/overview) dengan opsi mana pun. Tunnel MCP berada dalam tahap pratinjau riset dan memerlukan permintaan akses. Lihat [Sandbox yang di-host sendiri dan tunnel MCP](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#self-hosted-sandboxes-and-mcp-tunnels).
* **Berjalan di bawah kontrol kepatuhan dan audit milik organisasi Anda sendiri:** Alat berjalan di host yang Anda konfigurasikan, catat log-nya, dan audit.

## Apa yang tidak diubah oleh sandbox yang di-host sendiri

Dengan opsi mana pun, riwayat percakapan dan hasil alat dikirim ke layanan Managed Agents, yang dioperasikan oleh Anthropic. Begitulah cara model menerima hasil dari setiap panggilan alat. Alat web search dan web fetch juga berjalan di sisi Anthropic, bukan di sandbox. Lihat [Membatasi domain web search dan web fetch](https://platform.claude.com/docs/id/managed-agents/tools-web-restrictions). Tidak ada opsi yang mengubah cakupan kepatuhan Managed Agents atau berapa lama layanan tersebut menyimpan riwayat percakapan. Lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility).

## Apa yang Anda tanggung dan lepaskan dengan sandbox yang di-host sendiri

Sandbox yang di-host sendiri menjadikan Anda operator host worker. Anda memperkuat keamanan image sandbox, mengendalikan lalu lintas jaringan keluar, menyimpan dan merotasi kunci lingkungan, serta mengisolasi sesi satu sama lain. Halaman [Model keamanan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security) berisi detailnya.

Anda juga melepaskan fitur-fitur lingkungan cloud berikut:

* [Sumber daya sesi `file` dan `github_repository`](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#session-resources). Anda [menyiapkan file input sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#stage-files-for-a-session), dan Anda juga bertanggung jawab untuk memasang repositori GitHub Anda sendiri.
* [Penemuan skill dari repositori](https://platform.claude.com/docs/id/managed-agents/skills#load-skills-from-a-github-repository).
* [Kredensial variabel lingkungan](https://platform.claude.com/docs/id/managed-agents/vaults#add-a-credential) di vault.
* [Runtime dan paket pra-instal](https://platform.claude.com/docs/id/managed-agents/cloud-sandboxes-reference) pada sandbox cloud. Sandbox yang di-host sendiri memiliki apa pun yang disediakan worker Anda.

## Perbedaan pada Claude Platform on AWS

Jika Anda menggunakan Claude Managed Agents melalui Claude Platform on AWS, Anthropic tetap mengoperasikan layanannya. Di sana, sandbox yang di-host sendiri tidak dapat menggunakan memory store, worker tidak menggunakan kunci lingkungan, dan tunnel MCP tidak tersedia. Lihat [Claude Managed Agents di Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#claude-managed-agents) dan [Fitur yang tidak didukung](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#features-not-supported).

## Perbedaan pada Claude Models on Google Cloud (Anthropic managed)

Jika Anda menggunakan Claude Managed Agents melalui Claude Models on Google Cloud (Anthropic managed), Anthropic tetap mengoperasikan layanannya. Di sana, memory store tidak didukung di sandbox yang di-host sendiri, dan tunnel MCP tidak tersedia. Worker melakukan autentikasi dengan kredensial Google Cloud, bukan kunci lingkungan, dan Anda menulis worker Anda sendiri, karena worker bawaan di CLI `ant` serta SDK Python, TypeScript, dan Go tidak berfungsi di sana. Lihat [Dukungan fitur](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#feature-support) dalam panduan Claude Models on Google Cloud (Anthropic managed).

## Beralih dari lingkungan cloud ke sandbox yang di-host sendiri

Untuk beralih ke sandbox yang di-host sendiri, Anda mempertahankan agen, membuat lingkungan `self_hosted`, dan mereferensikan ID-nya di sesi dan deployment baru.

* **Apa yang tetap terbawa:** Definisi agen, kunci API, kredensial Google Cloud, atau kredensial AWS yang digunakan aplikasi Anda, skill Anda, server MCP Anda, dan [memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory) Anda.
* **Apa yang baru:** Lingkungan `self_hosted`, kunci lingkungan yang Anda buat di Claude Console, dan worker yang Anda jalankan. [Panduan memulai cepat sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#quickstart) mencakup ketiganya.
* **Apa yang berhenti berfungsi:** Fitur-fitur yang tercantum di [Apa yang Anda tanggung dan lepaskan dengan sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/choosing-an-environment#what-you-take-on-and-give-up-with-a-self-hosted-sandbox).

Di Claude Platform on AWS, memory store tidak terbawa ke sandbox yang di-host sendiri, dan worker tidak menggunakan kunci lingkungan. Lihat [Perbedaan pada Claude Platform on AWS](https://platform.claude.com/docs/id/managed-agents/choosing-an-environment#differences-on-claude-platform-on-aws).

Di Claude Models on Google Cloud (Anthropic managed), memory store tidak didukung di sandbox yang di-host sendiri, dan Anda menulis worker Anda sendiri, yang tidak menggunakan kunci lingkungan. Lihat [Perbedaan pada Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/managed-agents/choosing-an-environment#differences-on-claude-models-on-google-cloud-anthropic-managed).
