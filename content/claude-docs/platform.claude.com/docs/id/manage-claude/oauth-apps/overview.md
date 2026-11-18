---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/overview
fetched_at: 2026-11-18T02:14:00.973041Z
sha256: ed1bcb01a262699da26465d10afcc8e1993f6a8183704800c258ef9f7bc5fcf6
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

## Apa yang dapat Anda bangun

### Izinkan pelanggan membayar penggunaan Claude mereka sendiri

Ketika produk Anda memanggil Claude, penggunaannya dapat ditagihkan ke organisasi Claude milik pelanggan Anda sendiri. Pengguna Anda mengklik tombol **Link your Claude organization**, masuk ke Claude, dan menyetujui aplikasi Anda. Untuk Linked billing, pengguna harus memiliki peran Admin atau Penagihan di organisasi Claude mereka.

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
  Jika Anda pernah bekerja dengan OAuth sebelumnya: Claude Platform OAuth menggunakan “authorization code flow” (alur kode otorisasi) OAuth 2.0 dengan PKCE, dengan Anthropic sebagai “authorization server” (server otorisasi).
</Note>

## Penyiapan aplikasi OAuth satu kali

Linked billing dimulai dengan langkah penyiapan satu kali berikut di Claude Console. Panduan [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections#setup-process) memandu Anda melaluinya.

1. **Buat aplikasi.** Anggota organisasi Claude Anda dengan peran Admin membuat aplikasi OAuth di Claude Console dan menyalin client ID-nya. Aplikasi tersebut menyimpan nama yang dilihat orang di halaman persetujuan, serta alamat di produk Anda tempat mereka kembali.
2. **Siapkan autentikasi klien.** Alih-alih “client secret” (rahasia klien), back end Anda membuktikan bahwa suatu permintaan berasal dari aplikasi Anda dengan token berumur pendek dari penyedia identitas Anda sendiri, seperti AWS, Google Cloud, Microsoft Entra ID, atau Kubernetes. Anda memilih penyedia identitas, dan token mana darinya yang diterima, pada tab **Client authentication** aplikasi.
3. **Siapkan identitas back end Anda.** Buat “service account” (akun layanan) dan aturan federasi kedua dengan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation), lalu pilih akun layanan tersebut sebagai akun layanan operator aplikasi.

## Langkah selanjutnya

Panduan Linked billing memandu Anda melalui penyiapan dan pelanggan tertaut pertama Anda.

<CardGroup cols={3}>
  <Card title="Linked billing" icon="coins" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/organization-billing-connections">
    Izinkan pelanggan Anda membayar penggunaan Claude di produk Anda dari organisasi Claude mereka sendiri
  </Card>

  <Card title="Referensi OAuth" icon="book" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/oauth-reference">
    Endpoint, parameter, respons token, masa berlaku, dan error
  </Card>
</CardGroup>
