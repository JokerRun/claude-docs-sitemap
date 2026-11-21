---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/overview
fetched_at: 2026-11-21T02:12:50.066053Z
sha256: aca5c25a7dc97f93dc8e0165ad9707bf7b3883a59b6ad2f58380d1bed2b638b1
---

---
title: Claude Platform OAuth
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/overview
description: Izinkan pelanggan Anda membayar penggunaan Claude di produk Anda dari organisasi Claude mereka sendiri.
---

<Warning>
  Claude Platform OAuth adalah Beta Service: perangkat lunak prarilis yang disediakan berdasarkan perjanjian Anda dengan Anthropic, seperti [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms), dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Endpoint, parameter, dan perilaku dapat berubah selama beta. Ini mungkin tidak cocok untuk penggunaan produksi.
</Warning>

Claude Platform OAuth memungkinkan pengguna Anda menagihkan penggunaan di dalam aplikasi Anda ke organisasi Claude mereka.

## Izinkan pelanggan membayar penggunaan Claude mereka sendiri

Ketika produk Anda memanggil Claude, Anda dapat menagihkan penggunaannya ke organisasi Claude milik setiap pelanggan sendiri. Inilah Linked billing. Pengguna Anda mengklik tombol **Link your Claude organization**, masuk ke Claude, dan menyetujui aplikasi Anda. Mereka harus memiliki peran Admin atau Penagihan di organisasi Claude mereka.

Setelah itu:

* Anda memilih pada setiap permintaan Claude API apakah pelanggan yang membayar atau Anda yang membayar.
* Jika permintaan yang Anda tandai untuk pelanggan tidak dapat ditagihkan kepada mereka, Claude API akan menolaknya alih-alih menagih Anda.
* Pelanggan dapat memutuskan tautan aplikasi Anda kapan saja.
* Anda hanya boleh menagih pelanggan untuk permintaan yang mereka arahkan untuk Anda buat, dan sama sekali tidak boleh untuk penggunaan Anda sendiri.

Anda yang memberikan dukungan kepada pelanggan Anda: Anthropic menyediakan halaman persetujuan dan halaman Claude Console tempat mereka menetapkan batas atas pengeluaran atau memutuskan tautan aplikasi Anda, sedangkan semua pertanyaan lain tentang aplikasi Anda diajukan kepada Anda.

Linked billing berfungsi untuk pelanggan yang organisasi Claude-nya membayar Anthropic secara langsung untuk penggunaan API-nya. Fitur ini tidak berfungsi untuk organisasi yang ditagih melalui marketplace cloud. Lihat [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections).

## Cara kerjanya

Linked billing mengikuti perjalanan bolak-balik singkat. Orang tersebut meninggalkan produk Anda menuju halaman persetujuan Claude satu kali, menyetujui aplikasi Anda di sana, lalu kembali:

<Frame>
  !["Sequence diagram" (diagram urutan): orang tersebut menyetujui aplikasi Anda di auth.claude.com, lalu back end Anda menukarkan "one-time code" (kode sekali pakai)](https://platform.claude.com/docs/id/images/oauth-apps-billing-round-trip.svg)
</Frame>

Halaman persetujuan menampilkan nama aplikasi Anda dan apa yang diminta oleh aplikasi Anda, sehingga orang tersebut mengetahui apa yang mereka setujui.

<Note>
  Claude Platform OAuth menggunakan “authorization code flow” (alur kode otorisasi) OAuth 2.0 dengan PKCE. Anthropic adalah “authorization server” (server otorisasi).
</Note>

## Penyiapan aplikasi OAuth satu kali

Linked billing dimulai dengan langkah penyiapan satu kali berikut di Claude Console. Panduan [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#setup-process) memandu Anda melaluinya.

Langkah-langkah ini memerlukan peran Admin di organisasi Claude Anda.

1. **Buat aplikasi.** Di Claude Console, buat aplikasi OAuth dan salin client ID-nya. Aplikasi tersebut menyimpan nama yang dilihat orang di halaman persetujuan serta alamat di produk Anda tempat mereka kembali.
2. **Siapkan autentikasi klien.** Alih-alih “client secret” (rahasia klien), back end Anda menggunakan token berumur pendek untuk membuktikan bahwa suatu permintaan berasal dari aplikasi Anda. Token tersebut berasal dari penyedia identitas Anda sendiri, seperti AWS, Google Cloud, atau Kubernetes. Pada tab **Client authentication** aplikasi, Anda memilih penyedia identitas dan token mana darinya yang diterima.
3. **Siapkan identitas back end Anda.** Buat “service account” (akun layanan) dan aturan federasi kedua dengan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation). Pilih akun layanan tersebut sebagai [akun layanan operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference#terms) aplikasi, yang digunakan back end Anda untuk menagih pelanggan.

## Langkah selanjutnya

Panduan Linked billing memandu Anda melalui penyiapan dan pelanggan tertaut pertama Anda.

<CardGroup cols={2}>
  <Card title="Linked billing" icon="coins" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections">
    Izinkan pelanggan Anda membayar penggunaan Claude di produk Anda dari organisasi Claude mereka sendiri
  </Card>

  <Card title="Referensi OAuth" icon="book" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference">
    Endpoint, parameter, respons token, masa berlaku, dan error
  </Card>
</CardGroup>
