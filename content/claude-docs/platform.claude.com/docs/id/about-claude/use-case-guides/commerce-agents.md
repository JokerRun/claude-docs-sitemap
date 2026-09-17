---
source: platform
url: https://platform.claude.com/docs/id/about-claude/use-case-guides/commerce-agents
fetched_at: 2026-09-17T02:21:00.513769Z
sha256: 1b32a06d11a95203786eff10f88c0c09ca461eff03d71d7c3bfe2f0afac539d6
---

---
title: Agen perdagangan
url: https://platform.claude.com/docs/id/about-claude/use-case-guides/commerce-agents
description: Bangun agen belanja dan agen merchant di Claude menggunakan Claude for commerce, sebuah blueprint open-source dengan implementasi yang berfungsi pada Messages API, Claude Agent SDK, dan Claude Managed Agents.
---

Panduan ini menunjukkan cara membangun agen perdagangan di Claude: "shopping agent" (agen belanja) yang digunakan pelanggan di dalam aplikasi Anda, dan "merchant agent" (agen merchant) untuk orang-orang yang menjalankan toko, baik staf operasional bisnis itu sendiri maupun para penjual di platformnya. Panduan ini melakukannya melalui Claude for commerce, sebuah "blueprint" (cetak biru) open-source yang berisi implementasi yang berfungsi dari setiap agen pada [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages), [Claude Agent SDK](https://code.claude.com/docs/id/agent-sdk/overview), dan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), contoh yang dapat dijalankan untuk ritel, perjalanan, telekomunikasi, dan hiburan, serta plugin Claude Code yang membuat kerangka desain yang sama untuk sistem Anda sendiri.

Kode, instruksi penyiapan, dan dokumentasi keamanan tersedia di [repositori Claude for commerce di GitHub](https://github.com/anthropics/commerce-agents). Untuk mengetahui cara agen dibangun beserta alasannya, termasuk desain agen tunggal dengan skill, komponen UI sebagai alat, keamanan yang ditegakkan oleh harness, "prompt caching" (caching prompt), memori, dan eval, baca postingan engineering [Panduan anatomi agen perdagangan yang efektif](https://claude.com/blog/the-anatomy-of-effective-commerce-agents).

<Note>
  Blueprint ini adalah implementasi referensi untuk di-fork dan diadaptasi, bukan produk yang didukung atau layanan yang di-hosting.
</Note>

## Agen belanja

Agen belanja berada di dalam aplikasi Anda dan menjangkau sistem Anda melalui satu antarmuka backend yang Anda implementasikan di atas layanan katalog, keranjang, preferensi, pesanan, kebijakan, dan pemenuhan pesanan Anda. Tidak ada metode pada antarmuka tersebut yang membuat pesanan atau memindahkan uang. Dalam percakapan, agen dapat:

* Mencari di katalog, membandingkan kandidat akhir, dan mengubah kebutuhan yang dijelaskan menjadi daftar pilihan dan rekomendasi.
* Merencanakan serangkaian item yang terkoordinasi untuk suatu tujuan seperti perjalanan, acara, atau ruangan, dan menyesuaikannya dengan anggaran.
* Menampilkan produk, perbandingan, rencana, status pesanan, dan keranjang sebagai komponen UI yang dirender dalam percakapan.
* Mengisi keranjang dan menyerahkannya ke checkout Anda.
* Menjawab pertanyaan tentang pesanan, pengiriman, pengembalian, dan kebijakan dari sistem pesanan dan kebijakan Anda sendiri.
* Mengingat apa yang diminta pelanggan untuk diingat dan menerapkannya di sesi berikutnya.

Lima skill dimuat sesuai kebutuhan untuk mencakup pencarian dan penemuan, riset pembelian, perencanaan menuju suatu tujuan, layanan pelanggan, serta memori dan personalisasi. Aturan yang dibutuhkan agen di sebagian besar giliran, seperti grounding, semantik keranjang dan checkout, serta presentasi, ditempatkan di "system prompt" (prompt sistem) sebagai gantinya.

Agen menyebutkan produk, harga, ketersediaan, dan ketentuan toko hanya berdasarkan hasil alat dalam percakapan, dan penulisan ke keranjang hanya menerima ID produk yang dikembalikan oleh alat katalog atau pesanan dalam sesi tersebut. Checkout menyiapkan ringkasan yang dikonfirmasi pelanggan di aplikasi Anda. Jika Anda menggunakan checkout yang di-hosting, back end Anda mengembalikan URL-nya dan host merendernya tanpa meneruskannya melalui model.

## Agen merchant

Agen merchant mendukung orang-orang yang menjalankan toko. Agen ini menjangkau sistem analitik, katalog, inventaris, harga, dan kampanye Anda melalui antarmuka backend-nya sendiri, dan dapat:

* Menjelaskan kinerja bisnis: mengapa suatu metrik berubah, segmen mana yang mendorongnya, dan laju dibandingkan dengan periode yang sebanding. Delegasi analisis opsional menjalankan kueri hanya-baca dengan batas waktu dan ukuran.
* Menyajikan ringkasan harian tentang hal-hal yang perlu diperhatikan, termasuk stok rendah, produk yang lambat terjual, dan pengecualian pesanan.
* Meningkatkan konten listing dan memperbaiki data katalog dari materi yang diberikan operator.
* Merekomendasikan perubahan harga dan promosi dalam batas "guardrails" (pagar pengaman) toko, dengan pratinjau margin.
* Menyusun draf kampanye pemasaran lengkap dengan audiens, penempatan, dan anggaran.

Lima skill-nya mencakup wawasan kinerja, inventaris dan operasional, katalog dan listing, harga dan promosi, serta kampanye pemasaran.

Setiap penulisan yang diusulkan agen merchant, baik pembaruan listing, perubahan harga, tindakan inventaris, promosi, maupun kampanye, merupakan "staged change" (perubahan yang disiapkan) dengan ID yang dibuat server, yang dilihat operator sebagai kartu pratinjau. Pagar pengaman seperti perubahan harga maksimum, kedalaman promosi, ukuran restock, anggaran kampanye, dan kolom yang dilindungi diperiksa saat perubahan disiapkan dan sekali lagi saat diterapkan. Perubahan hanya diterapkan setelah seseorang menyetujuinya di luar percakapan: tombol di portal merchant pada jalur Messages API, prompt konfirmasi di konsol Agent SDK, atau [kebijakan izin always-ask](https://platform.claude.com/docs/id/managed-agents/permission-policies) pada alat apply di Claude Managed Agents. Persetujuan yang diketik di chat tidak menyetujui apa pun.

## Contoh vertikal

Setiap contoh mencakup etalase pelanggan dan portal merchant dengan data fiktif.

| Vertikal       | Etalase                                                                                       | Portal merchant                                                                                                        |
| -------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Ritel          | Pencarian, perbandingan, rencana, keranjang, checkout, dan memori menggunakan komponen bawaan | Ringkasan harian, restock dan perbaikan listing yang disiapkan, serta delegasi analisis di atas view SQL               |
| Perjalanan     | Inventaris yang terikat tanggal dan komponen itinerary                                        | Kalender okupansi dan perubahan tarif berdasarkan rentang tanggal                                                      |
| Telekomunikasi | Konteks akun, matriks paket, dan pengungkapan biaya yang ditulis server                       | Komposisi paket, perubahan harga yang menyebutkan jalur yang terdampak, dan biaya teregulasi yang dilindungi           |
| Hiburan        | Penahanan berwaktu, daftar tunggu, transfer, peta venue, dan pengungkapan biaya all-in        | Laju penjualan acara, pelepasan penahanan yang menambah kapasitas nyata, dan perubahan harga yang mempertahankan biaya |

## Tempat menjalankannya

Runtime Messages API dan Agent SDK berjalan pada Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Cloud's Agent Platform](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), atau [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), atau melalui gateway Anda sendiri. Jalur Claude Managed Agents berjalan pada Claude API. Panduan deployment di repositori menunjukkan di mana setiap jalur memilih platformnya dan format ID model yang diharapkan oleh masing-masing jalur.

## Bangun milik Anda sendiri dengan plugin Claude Code

Blueprint ini dilengkapi dengan plugin [Claude Code](https://code.claude.com/docs/id/overview) yang membaca repositori hasil clone sebagai referensinya dan membangun agen untuk sistem Anda sendiri. Empat perintahnya mencakup jalur dari nol hingga agen yang telah diuji:

| Perintah                   | Fungsinya                                                                                                                                                    |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/scaffold-commerce-agent` | Mewawancarai Anda tentang stack Anda, memaparkan kembali rencananya, dan membuat kerangka agen belanja, agen merchant, atau keduanya di atas paket referensi |
| `/add-commerce-flow`       | Menambahkan satu alur ke agen yang sudah ada dengan menyalin skill-nya, menghubungkan alat yang dipanggilnya, dan menulis kasus eval pertamanya              |
| `/author-commerce-evals`   | Membangun rangkaian eval dengan runner, kasus pertama terhadap katalog Anda sendiri, dan gerbang replay untuk CI                                             |
| `/review-commerce-agent`   | Memetakan agen yang sudah Anda jalankan, membandingkannya dengan referensi, dan mengonversi bagian yang Anda pilih                                           |

Plugin ini juga membawa enam skill tentang arsitektur, caching prompt, UI sebagai alat, kepercayaan dan keamanan, eval, serta operasional merchant, yang dimuat setiap kali percakapan Claude Code cocok dengannya. Instruksi instalasi tersedia di README repositori.

Untuk mengadaptasi referensi secara manual, implementasikan antarmuka backend belanja atau merchant di atas layanan Anda, nonaktifkan sistem yang tidak Anda miliki dengan flag konfigurasi agar alat dan baris prompt terkait dihapus, lalu atur nama merek, nama asisten, dan gaya bahasa Anda. Panduan backend di repositori menjelaskan identitas dan kredensial, alur berurutan, penyerahan ke checkout, serta produk dengan opsi. Sebuah pilot dapat mengimplementasikan pencarian dan detail produk, lalu membuat stub untuk sisanya.

## Memulai

<CardGroup cols={2}>
  <Card title="Claude for commerce di GitHub" icon="github-logo" href="https://github.com/anthropics/commerce-agents">
    Clone blueprint dan jalankan kedua agen secara lokal.
  </Card>

  <Card title="Panduan anatomi agen perdagangan yang efektif" icon="book" href="https://claude.com/blog/the-anatomy-of-effective-commerce-agents">
    Baca cara agen dibangun beserta alasannya.
  </Card>
</CardGroup>
