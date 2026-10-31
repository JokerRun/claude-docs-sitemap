---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/secure-deployment-risks
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 34c68b611b4f0bc29494e5958f3aa7ade94569472629bf88ca016525db0cc55b
---

---
title: Risiko keamanan dan batasan sandbox
url: https://platform.claude.com/docs/id/managed-agents/secure-deployment-risks
description: Mengapa pengaturan agen penting untuk keamanan, dan apa yang dapat dan tidak dapat dilakukan oleh sandbox Managed Agents.
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

Halaman ini menjelaskan mengapa pengaturan dalam [Amankan deployment Managed Agents Anda](https://platform.claude.com/docs/id/managed-agents/secure-deployment) penting, serta apa yang dapat dan tidak dapat dilakukan oleh sandbox.

## Mengapa ini penting

Instruksi tersembunyi dalam konten yang dibaca oleh agen dapat mengarahkan agen tersebut. Hal ini disebut [prompt injection](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) (injeksi prompt). Claude secara inheren tahan terhadapnya, tetapi perilaku model bukanlah kontrol keamanan. Pengaturan dalam [Amankan deployment Managed Agents Anda](https://platform.claude.com/docs/id/managed-agents/secure-deployment) membatasi dampaknya jika suatu upaya berhasil.

Claude juga dapat mengambil langkah yang tidak Anda duga sementara ia terus bekerja untuk menyelesaikan tugas yang Anda berikan. Misalnya, ia mungkin menggunakan alat atau kredensial yang dapat dijangkaunya untuk melewati suatu hambatan. Pengaturan yang sama membatasi apa yang dapat dijangkau oleh langkah semacam itu, dan [peninjau offline](https://platform.claude.com/docs/id/managed-agents/secure-deployment-monitoring#optionally-have-an-offline-reviewer-read-every-transcript) dapat menandainya setelahnya.

| Apa yang bisa salah                                | Contoh                                                                                                                                    | Kontrol                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Input yang tidak tepercaya mengarahkan agen        | Sebuah tiket memerintahkan agen untuk membatalkan setiap pesanan yang terbuka                                                             | [Set alat terkecil](https://platform.claude.com/docs/id/managed-agents/secure-deployment#give-the-agent-the-smallest-tool-set), [input tidak tepercaya dijauhkan dari alat yang kuat](https://platform.claude.com/docs/id/managed-agents/secure-deployment#keep-untrusted-input-away-from-powerful-tools), [persetujuan untuk tindakan berisiko](https://platform.claude.com/docs/id/managed-agents/secure-deployment#approve-risky-actions) |
| Kode di dalam sandbox dapat menggunakan kredensial | Skrip yang dijalankan agen karena tertipu mengirimkan kunci agen ke host luar, atau menggunakannya untuk membaca pesanan setiap pelanggan | [Kredensial di dalam vault](https://platform.claude.com/docs/id/managed-agents/secure-deployment#keep-credentials-in-vaults), [jaringan terbatas](https://platform.claude.com/docs/id/managed-agents/secure-deployment#limit-the-network), [persetujuan untuk tindakan berisiko](https://platform.claude.com/docs/id/managed-agents/secure-deployment#approve-risky-actions)                                                                 |
| Jaringan terbuka memungkinkan data keluar          | Perintah bash mengirimkan file ke host luar                                                                                               | [Jaringan terbatas](https://platform.claude.com/docs/id/managed-agents/secure-deployment#limit-the-network), [daftar domain `web_fetch`](https://platform.claude.com/docs/id/managed-agents/secure-deployment#restrict-web-search-and-web-fetch)                                                                                                                                                                                             |
| Claude mengambil langkah yang tidak Anda duga      | Untuk melewati suatu hambatan, Claude menggunakan alat atau kredensial yang dapat dijangkaunya                                            | Pengaturan dalam [Amankan deployment Managed Agents Anda](https://platform.claude.com/docs/id/managed-agents/secure-deployment). [Peninjau offline](https://platform.claude.com/docs/id/managed-agents/secure-deployment-monitoring#optionally-have-an-offline-reviewer-read-every-transcript) dapat menandai langkah tersebut setelahnya                                                                                                    |

Pengaturan ini menurunkan risiko tetapi tidak menghilangkannya, jadi jangan menaruh data di dalam sandbox yang sama sekali tidak boleh keluar darinya. Agen tetap dapat memasukkan data yang boleh dibacanya ke dalam balasannya sendiri atau output alat. Batasi izin kunci di layanan yang menerbitkannya, karena pengaturan ini tidak membatasinya. Pengaturan ini tidak mengamankan alat kustom Anda, server MCP Anda, atau infrastruktur yang Anda hosting sendiri.

## Apa yang dapat dan tidak dapat dilakukan oleh sandbox

Managed Agents secara desain menyimpan loop agen, riwayat sesi, dan rahasia vault di luar sandbox. Untuk latar belakang desainnya, lihat [Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents).

| Bagian                       | Tempat berjalan                                                                                                                | Apa yang membatasinya                                                                                                                                                                                                                                    |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Loop agen                    | Server Anthropic                                                                                                               | Set alat, kebijakan izin, dan anggaran yang Anda tetapkan                                                                                                                                                                                                |
| `bash` dan alat file         | Sandbox. Di environment cloud, setiap sesi mendapatkan container Linux terisolasinya sendiri                                   | Jaringan environment, set alat, dan kebijakan izin                                                                                                                                                                                                       |
| `web_search` dan `web_fetch` | Server Anthropic                                                                                                               | Daftar domain milik alat itu sendiri, pengaturan web search dan web fetch organisasi Anda di Claude Console, dan, di lingkungan cloud `limited`, host yang diizinkan oleh lingkungan. `web_fetch` juga hanya membuka URL yang sudah muncul di dalam sesi |
| Rahasia vault                | Di luar sandbox. Kredensial MCP tidak pernah masuk ke dalamnya. Untuk kredensial variabel lingkungan, kode melihat placeholder | Untuk kredensial MCP, URL server MCP yang menjadi tujuannya. Untuk kredensial variabel lingkungan, host yang diizinkan oleh kredensial, lokasi injeksinya, dan host yang diizinkan oleh environment                                                      |
| Riwayat sesi                 | Server Anthropic, hingga Anda menghapus sesi                                                                                   | Kunci API untuk workspace, peran Developer dan Admin di Claude Console, dan penghapusan sesi                                                                                                                                                             |
| Alat kustom                  | Aplikasi Anda                                                                                                                  | Kode Anda                                                                                                                                                                                                                                                |

Di environment cloud, sesi tidak berbagi status filesystem. Memory store yang dilampirkan ke lebih dari satu sesi akan dibagikan di antara sesi-sesi tersebut.

Batasan-batasan ini tidak saling menggantikan. Misalnya, membatasi host environment tidak menghentikan agen menggunakan kredensial pada host yang Anda izinkan.
