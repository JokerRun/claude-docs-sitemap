---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/overview
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 206764da5e2086ebd549b06d263fc1d6da47f781fce2025bfcc6b85e0fc09496
---

---
title: Claude Platform OAuth
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/overview
description: Tempat memulai dengan Claude Platform OAuth dan Linked billing, serta bagaimana persetujuan pelanggan sampai ke back end Anda.
---

<Warning>
  Claude Platform OAuth adalah Beta Service: perangkat lunak prarilis yang disediakan berdasarkan perjanjian Anda dengan Anthropic, seperti [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms), dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Endpoint, parameter, dan perilaku dapat berubah selama beta. Ini mungkin tidak cocok untuk penggunaan produksi.
</Warning>

Claude Platform OAuth adalah cara pelanggan menyetujui produk Anda untuk menggunakan organisasi Claude mereka. Fitur ini menjadi dasar [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing), yang memungkinkan pelanggan Anda membayar penggunaan Claude di produk Anda melalui organisasi Claude mereka sendiri. Untuk memanggil Claude bagi produk Anda sendiri dengan kredensial organisasi Anda, Anda tidak memerlukan aplikasi OAuth: lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication).

Untuk menawarkan Linked billing, Anda memerlukan aplikasi OAuth dan [penyedia identitas](https://platform.claude.com/docs/id/manage-claude/oauth-apps/overview#no-client-secret) yang menerbitkan token ke back end Anda. Pelanggan Anda memerlukan organisasi Claude yang membayar Anthropic secara langsung: lihat [Pelanggan yang memenuhi syarat](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#eligible-customers).

## Cara kerjanya

Pelanggan menyetujui aplikasi Anda satu kali. Hal itu membuat sebuah koneksi, yang mengikat organisasi Claude mereka ke aplikasi Anda hingga mereka atau Anda mengakhirinya.

Seorang pengguna di perusahaan pelanggan Anda mengklik [tombol Link your Claude organization](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-button) di produk Anda. Back end Anda mengarahkan mereka ke halaman persetujuan Claude di `auth.claude.com`. Jika mereka memiliki peran Admin atau Billing di organisasi pelanggan, mereka menyetujui aplikasi Anda, dan browser kembali dengan kode sekali pakai. Back end Anda menukarkan kode tersebut dengan ID koneksi dan token OAuth. Setelah itu, Anthropic dapat menagih organisasi pelanggan untuk permintaan yang dibuat back end Anda atas nama mereka.

<Frame>
  ![Diagram urutan: orang tersebut menyetujui aplikasi Anda di auth.claude.com, lalu back end Anda menukarkan kode sekali pakai](https://platform.claude.com/docs/id/images/linked-billing-round-trip.svg)
</Frame>

Seseorang yang tidak memiliki salah satu peran tersebut tidak dapat memberikan persetujuan: lihat [Apa yang dilihat pelanggan Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see#approving-the-link). Jika Anda mengenal OAuth, ini adalah “authorization code flow” (alur kode otorisasi) dengan PKCE.

### Aplikasi OAuth Anda

Aplikasi OAuth Anda adalah pendaftaran produk Anda di Anthropic. Seorang Admin organisasi Claude Anda membuatnya di Claude Console, dan aplikasi tersebut memberikan client ID kepada produk Anda. Di halaman persetujuan, pelanggan melihat nama, logo, dan apa yang diminta oleh aplikasi tersebut.

### Penyedia identitas alih-alih client secret

Setiap permintaan yang dikirim back end Anda ke `auth.claude.com` membawa token dari penyedia identitas Anda, melalui [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation). Anthropic tidak menerbitkan “client secret” (rahasia klien) untuk aplikasi OAuth. Penerbit OpenID Connect apa pun dapat digunakan, dan tersedia [panduan untuk penyedia identitas umum](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#identity-providers).

## Pilih jalur Anda

Mulailah dengan tugas yang Anda hadapi sekarang. Untuk membangun integrasi, [siapkan aplikasi Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app), [tautkan dan tagih pelanggan uji](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer), lalu [uji dan publikasikan aplikasi Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish). Sampai aplikasi Anda aktif, hanya pengguna ujinya yang dapat menautkannya, jadi terlebih dahulu [tambahkan pemberi persetujuan pelanggan uji Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#add-test-users).

<CardGroup cols={2}>
  <Card title="Linked billing" icon="coins" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing">
    Tentukan apakah Linked billing sesuai untuk produk dan pelanggan Anda
  </Card>

  <Card title="Siapkan aplikasi Anda untuk Linked billing" icon="settings" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app">
    Daftarkan aplikasi Anda, lalu lanjutkan untuk menautkan dan menagih pelanggan
  </Card>

  <Card title="Kelola pelanggan tertaut" icon="list" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers">
    Dukung pelanggan tertaut, periksa apakah mereka masih tertaut, atau tautkan mereka kembali
  </Card>

  <Card title="Error Linked billing" icon="triangle-alert" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors">
    Perbaiki error yang dikembalikan oleh penautan atau penagihan
  </Card>

  <Card title="Apa yang dilihat pelanggan Anda" icon="browser" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see">
    Untuk tim produk dan dukungan: halaman persetujuan, batas atas pengeluaran, dan email yang dilihat pelanggan Anda
  </Card>

  <Card title="Endpoint dan parameter OAuth" icon="book" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters">
    Cari endpoint, parameter, scope, field token OAuth, atau error yang tepat
  </Card>
</CardGroup>
