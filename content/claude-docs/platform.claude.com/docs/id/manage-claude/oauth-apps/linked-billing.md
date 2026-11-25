---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 7a938976417c754507f3b44c4cf82bac8c758fac24105c7dec44f543894a2754
---

---
title: Linked billing
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing
description: Pelajari siapa yang membayar, pelanggan mana yang memenuhi syarat, dan ketentuan siapa yang berlaku agar Anda dapat memutuskan apakah Linked billing cocok untuk bisnis Anda.
featureMetadata:
  status: beta
  betaHeader: user-profiles-billing-2026-10-01
  supportedModels:
    - claude-fable-5-2
    - claude-mythos-5-2
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
    Claude API:
      availability: beta
      note: Hanya permintaan yang mengirim `billing_policy` yang memerlukan header beta.
---

<Warning>
  Claude Platform OAuth adalah Beta Service: perangkat lunak prarilis yang disediakan berdasarkan perjanjian Anda dengan Anthropic, seperti [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms), dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Endpoint, parameter, dan perilaku dapat berubah selama beta. Ini mungkin tidak cocok untuk penggunaan produksi.
</Warning>

Linked billing memungkinkan pelanggan Anda membayar penggunaan Claude di produk Anda melalui organisasi Claude mereka sendiri. Ini adalah fitur dari [Claude Platform OAuth](https://platform.claude.com/docs/id/manage-claude/oauth-apps/overview), sehingga bekerja melalui [aplikasi OAuth](https://platform.claude.com/docs/id/manage-claude/oauth-apps/overview#your-oauth-app) yang Anda daftarkan untuk produk Anda. Pelanggan menautkan organisasi mereka ke aplikasi Anda satu kali. Setelah itu, Anda memilih pada setiap permintaan Claude API apakah Anda atau pelanggan yang membayar.

## Cara kerjanya

Misalkan Acme menggunakan produk Anda dan sudah membayar Anthropic untuk penggunaan Claude-nya sendiri. Anda membuat [profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) untuk Acme: sebuah catatan di organisasi Anda yang mewakili pelanggan tersebut. Seseorang di Acme mengklik [tombol Link your Claude organization](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-button) di produk Anda. Di halaman persetujuan Claude, mereka menyetujui aplikasi Anda. Persetujuan memerlukan peran Admin atau Billing di organisasi Claude milik Acme. Mereka juga dapat menetapkan [batas atas pengeluaran](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see#spend-caps) bulanan untuk aplikasi tersebut.

Sejak saat itu, back end Anda mengirimkan permintaan Claude API milik Acme sebagai [akun layanan operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#service-account) aplikasi Anda, yaitu akun non-manusia di organisasi Claude Anda. Hanya akun tersebut yang dapat menagih pelanggan yang tertaut. Token akses OAuth milik pelanggan sendiri dihitung sebagai akun tersebut, sehingga permintaan dengan token itu dapat menagih pelanggan tersebut dan bukan pelanggan lain. Back end Anda menandai permintaan yang dibayar oleh Acme, dan Anthropic menagihkannya ke organisasi Acme, bukan ke organisasi Anda, dengan tarif Acme sendiri. [Linked Billing Beta Terms](https://www.anthropic.com/legal/linked-billing-terms) menjelaskan bagaimana pelanggan dikenai biaya.

### Bagaimana koneksi dimulai dan berakhir

Penautan membuat sebuah koneksi, yang mengikat organisasi Claude pelanggan ke profil pengguna mereka. Koneksi tersebut milik organisasi pelanggan, bukan milik orang yang menyetujuinya, sehingga tetap ada jika orang tersebut keluar. Berikut adalah cara umum koneksi berakhir:

* Pelanggan membatalkan tautan aplikasi Anda.
* Admin organisasi Anda membatalkan tautan pelanggan di Claude Console.
* Back end Anda mengakhiri koneksi melalui API.

Ada juga [cara yang kurang umum koneksi berakhir](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see#after-linking). Anthropic tidak memberi tahu Anda ketika pelanggan membatalkan tautan, jadi [periksa apakah pelanggan masih tertaut](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#check-a-links-status).

### Pilih siapa yang membayar pada setiap permintaan

Setiap permintaan yang dikirim akun layanan operator Anda untuk pelanggan yang tertaut menyebutkan profil pengguna mereka di header `anthropic-user-profile-id`. Isi body permintaan menentukan siapa yang membayar:

* **Pelanggan membayar** ketika field [`billing_policy`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#bill-a-request) pada body menetapkan `bill_to` ke `user_profile`.
* **Anda membayar** ketika `bill_to` bernilai `self` atau ketika body tidak memiliki `billing_policy`.

Dengan demikian, Anda dapat menagihkan sebagian penggunaan pelanggan kepada mereka dan membayar sisanya sendiri. Permintaan yang dikirim dengan token akses milik pelanggan sendiri hanya menagih pelanggan tersebut: lihat [Gunakan kredensial terpisah untuk setiap pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer).

### Ketika permintaan ditolak

Jika Anthropic tidak dapat menagih pelanggan untuk suatu permintaan, Claude API menolak permintaan tersebut. API tidak pernah menagih Anda sebagai gantinya. Berikut adalah penyebab umumnya:

* Pelanggan telah mencapai batas atas pengeluaran yang mereka tetapkan untuk aplikasi Anda, atau organisasi mereka telah mencapai batas pengeluaran bulanannya.
* Tidak ada kredit di akun pelanggan yang dapat membayar permintaan tersebut.
* Koneksi telah berakhir.

Anda dapat mengirim ulang permintaan yang ditolak sebagai permintaan yang Anda bayar. Untuk setiap penolakan dan cara memperbaikinya, lihat [Error Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors).

## Kapan menggunakannya

Linked billing cocok untuk produk yang penggunanya sebagian besar adalah pelanggan Claude Platform dengan organisasi Claude mereka sendiri. Untuk menawarkannya, organisasi Anda sendiri harus membayar Anthropic secara langsung, melalui kredit prabayar atau penagihan berbasis faktur.

Beberapa permintaan tidak dapat ditagihkan ke pelanggan. Untuk melayaninya, kirimkan sebagai permintaan yang Anda bayar:

* Permintaan untuk pelanggan yang organisasinya [tidak dapat ditagih dengan cara ini](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#eligible-customers)
* Permintaan ke [endpoint yang tidak dapat menagih pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#which-endpoints-can-bill-a-customer)

### Pelanggan yang memenuhi syarat

Pelanggan dapat ditagih dengan cara ini hanya jika organisasi Claude mereka membayar Anthropic secara langsung untuk penggunaan API-nya, melalui kredit prabayar atau penagihan berbasis faktur. Organisasi berikut tidak dapat ditagih dengan cara ini:

* Organisasi yang ditagih melalui marketplace cloud (AWS, Google Cloud, atau Azure)
* Organisasi yang hanya memiliki langganan Claude tanpa akses Claude API mereka sendiri

Organisasi yang hanya memiliki langganan Claude tidak dapat menautkan aplikasi Anda. Organisasi yang ditagih melalui marketplace cloud akan ditolak baik saat mencoba menautkan maupun pada setiap permintaan yang Anda tagihkan kepadanya. Jadi, tautan yang berhasil diselesaikan tidak menunjukkan bahwa organisasi semacam itu dapat ditagih.

### Kredit mana yang dapat membayar

Tidak semua kredit dapat membayar permintaan yang ditagihkan aplikasi ke pelanggan. Apa yang dapat membayar bergantung pada organisasi yang ditagih:

* **Ketika aplikasi Anda menagih pelanggan:** organisasi pelanggan
* **Ketika aplikasi perusahaan lain menagih Anda:** organisasi Anda sendiri

Kredit yang dibeli di Claude Console untuk organisasi tersebut dapat membayar permintaan ini. Jika organisasi tersebut menggunakan penagihan berbasis faktur, organisasi itu akan menerima faktur untuk permintaan ini.

Beberapa kredit promosi dari Anthropic tidak dapat membayar permintaan ini. Ini termasuk kredit API bulanan yang disertakan dengan paket Claude Max, Ultra, dan Team. Kredit dari program mitra, VC, dan startup Anthropic tidak memenuhi syarat untuk membayar permintaan ini.

Ketika tidak ada apa pun di akun organisasi tersebut yang dapat membayar suatu permintaan, Claude API dapat menolaknya dengan 402. Respons tidak menyebutkan apakah kekurangan kredit atau batas pengeluaran yang menyebabkan penolakan. Lihat [`linked_organization_spend_limit_reached`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#linked-organization-spend-limit-reached).

### Endpoint mana yang dapat menagih pelanggan

| Endpoint | Dapat menagih pelanggan |
| ----- | ----- |
| Messages API (`/v1/messages`) | Ya, kecuali dengan [eksekusi kode yang dapat ditagih](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#if-you-use-code-execution) |
| Kompatibilitas OpenAI SDK (`/v1/chat/completions`) | Ya |
| [Message Batches](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#if-you-use-message-batches) | Tidak |
| Claude Managed Agents | Tidak |

Untuk meminta endpoint lain, hubungi [dukungan Anthropic](https://support.claude.com/en/articles/9015913-how-to-get-support).

## Ketentuan dan batasan siapa yang berlaku

<Warning>
  Jangan tawarkan Linked billing kepada pelanggan yang memerlukan cakupan HIPAA, FERPA, atau kunci enkripsi yang dikelola pelanggan untuk penggunaan ini.
</Warning>

Permintaan yang Anda tagihkan ke pelanggan tetap berjalan di organisasi Anda:

| Pengaturan | Berlaku untuk permintaan ini |
| ----- | ----- |
| Batas laju, tingkat penggunaan, akses model, dan [tingkat layanan](https://platform.claude.com/docs/id/api/service-tiers) milik Anda | Ya |
| [Batas atas pengeluaran bulanan](https://platform.claude.com/docs/id/api/rate-limits#spend-limits) milik tingkat penggunaan Anda | Ya |
| Retensi data dan kunci enkripsi milik Anda | Ya |
| [Zero data retention (ZDR)](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope), business associate agreement (BAA), customer-managed encryption keys (CMEK), dan daftar IP yang diizinkan milik pelanggan | Tidak |
| Batas atas pengeluaran pelanggan untuk aplikasi Anda dan batas pengeluaran bulanan organisasi mereka | Ya |
| Batas pengeluaran yang Anda tetapkan untuk organisasi Anda dan workspace-nya | Tidak |

Setelah organisasi Anda mencapai batas atas pengeluaran bulanan tingkat penggunaan Anda, Claude API menolak semua permintaannya, termasuk permintaan yang menagih pelanggan: lihat [`enforced_spend_limit_reached`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#enforced-spend-limit-reached). Penggunaan yang Anda tagihkan ke pelanggan tidak dihitung terhadap batas atas tersebut.

## Apa yang boleh Anda tagihkan

Tagih pelanggan hanya untuk penggunaan yang mereka arahkan untuk Anda lakukan. Itu adalah penggunaan Claude yang ditimbulkan oleh pelanggan dan pengguna mereka di produk Anda. Jangan tagih mereka untuk penggunaan Anda sendiri, seperti pengujian, evaluasi, atau pekerjaan untuk pelanggan lain. Claude API tidak dapat memeriksa hal ini untuk Anda, jadi ini adalah tanggung jawab Anda. Anda menyetujui [Linked Billing Beta Terms](https://www.anthropic.com/legal/linked-billing-terms) saat Anda membuat aplikasi Anda.

## Siapa yang memberikan dukungan kepada pelanggan

Anda memberikan dukungan kepada pelanggan Anda untuk segala hal tentang aplikasi Anda, termasuk penggunaan Claude yang Anda tagihkan kepada mereka. Anthropic hanya memberi mereka [halaman persetujuan dan halaman Linked platforms](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see) di Claude Console mereka. Semua pertanyaan lain tentang aplikasi Anda akan datang kepada Anda, jadi beri tahu pelanggan Anda cara menghubungi Anda.

## Aturan dan kasus khusus

Beberapa fitur tidak dapat menagih pelanggan, dan beberapa memperlakukan `billing_policy` dengan caranya sendiri.

### Jika Anda menggunakan Message Batches

Kirim permintaan dalam [message batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing) sebagai permintaan yang Anda bayar: dengan `bill_to` diatur ke `self` atau tanpa `billing_policy`. Permintaan tersebut ditagihkan kepada Anda seperti biasa. Permintaan dalam batch yang ditandai untuk pelanggan akan ditolak. Hasilnya adalah `errored` dengan `invalid_request_error`, dan tidak ada yang ditagih untuk permintaan tersebut. Permintaan lain dalam batch berjalan seperti biasa.

### Jika Anda menggunakan eksekusi kode

Permintaan yang menagih pelanggan tidak dapat menggunakan [fitur eksekusi kode yang dapat ditagih](https://platform.claude.com/docs/id/about-claude/pricing#code-execution-tool): API menolaknya dengan 400. Kirim permintaan semacam itu sebagai permintaan yang Anda bayar.

### Jika Anda menghitung token

Endpoint penghitungan token (`/v1/messages/count_tokens`) menerima field `billing_policy` ketika permintaan memiliki beta header `user-profiles-billing-2026-10-01`, dan mengabaikan field tersebut. Anda tidak perlu menghapusnya sebelum menghitung token.

## Ketersediaan

Linked billing dalam versi beta di semua model.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tersedia

| Status | Platform cloud |
| ----- | ----- |
| Beta<sup>1</sup> | Claude API |

1. Hanya permintaan yang mengirim `billing_policy` yang memerlukan header beta.

### Header beta yang diperlukan

[Ikhtisar header beta](https://platform.claude.com/docs/id/api/beta-headers)

Header beta memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

* `user-profiles-billing-2026-10-01`
