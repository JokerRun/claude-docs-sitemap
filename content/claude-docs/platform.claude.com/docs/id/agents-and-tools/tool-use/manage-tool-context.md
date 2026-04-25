---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/manage-tool-context
fetched_at: 2026-04-25T03:09:48.142425Z
sha256: fadac903bb26fd0238f2b220c0ab381cf3bc763992bddf68ae521b21e7bedbaa
---

# Kelola konteks alat

Pilih antara pencarian alat, pemanggilan alat terprogram, penyimpanan prompt, dan pengeditan konteks untuk mengelola pembengkakan konteks.

---

Definisi alat dan blok `tool_result` yang terakumulasi mengonsumsi jendela konteks Anda. Agen yang berjalan lama dengan banyak alat atau banyak putaran dapat menghabiskan konteks yang tersedia sebelum tugas selesai. Empat pendekatan mengatasi ini di berbagai titik dalam pipeline.

## Empat pendekatan

Setiap pendekatan menargetkan sumber tekanan konteks yang berbeda. Pilih yang sesuai dengan kemana token Anda pergi.

| Pendekatan | Apa yang dikurangi | Kapan cocok | Pelajari lebih lanjut |
| --- | --- | --- | --- |
| Pencarian alat | Definisi alat dimuat di awal | Set alat besar (20+ alat) di mana sebagian besar alat tidak diperlukan setiap putaran | [Alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool) |
| Pemanggilan alat terprogram | Roundtrip `tool_result` | Rantai pemanggilan alat yang dapat dieksekusi sebagai satu skrip | [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) |
| Penyimpanan prompt | Biaya token dari definisi alat yang diulang | Set alat stabil di seluruh banyak permintaan | [Penggunaan alat dengan penyimpanan prompt](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching) |
| Pengeditan konteks | Blok `tool_result` lama dalam riwayat | Percakapan panjang di mana hasil awal tidak lagi relevan | [Pengeditan konteks](/docs/id/build-with-claude/context-editing) |

### Pencarian alat

Pencarian alat membuat definisi alat tetap keluar dari jendela konteks sampai Claude memintanya. Alih-alih mengirim 50 skema alat di awal, Anda mengirim satu alat `tool_search` dan membiarkan Claude menemukan sisanya sesuai permintaan. Ini menukar sejumlah kecil latensi (satu putaran ekstra untuk mencari alat) dengan pengurangan besar dalam penggunaan konteks dasar.

### Pemanggilan alat terprogram

Pemanggilan alat terprogram meruntuhkan urutan pemanggilan alat menjadi satu blok kode yang Claude tulis dan sandbox eksekusi kode Anthropic jalankan. Alih-alih lima roundtrip `tool_use` dan `tool_result`, Claude mengeluarkan satu skrip yang memanggil semua lima fungsi dari dalam sandbox. Hasil perantara tidak pernah memasuki riwayat percakapan.

### Penyimpanan prompt

Penyimpanan prompt tidak mengurangi jumlah token dalam konteks, tetapi mengurangi apa yang Anda bayar untuk mereka pada permintaan berikutnya. Jika definisi alat Anda stabil, simpan cache sekali dan gunakan kembali awalan cache di seluruh ribuan permintaan. Ini adalah pilihan yang tepat ketika set alat besar tetapi tetap.

### Pengeditan konteks

Pengeditan konteks menghapus blok `tool_result` lama dari riwayat percakapan setelah mereka telah melayani tujuan mereka. Loop agen yang panjang mungkin menghasilkan ratusan hasil perantara yang berguna pada saat itu tetapi sekarang adalah beban mati. Pengeditan konteks memungkinkan Anda memangkasnya tanpa memulai ulang percakapan.

## Menggabungkan pendekatan

Pendekatan-pendekatan ini dapat digabungkan. Agen yang berjalan lama mungkin menggunakan pencarian alat untuk membuat set alat tetap ramping, penyimpanan prompt untuk mengamortisasi biaya definisi yang tersisa, dan pengeditan konteks untuk memangkas hasil yang sudah usang saat percakapan berkembang. Masing-masing menyelesaikan bagian berbeda dari masalah, jadi tidak ada konflik dalam menggunakannya bersama.

Titik awal yang masuk akal untuk agen volume tinggi:

1. Aktifkan penyimpanan prompt pada definisi alat Anda sejak hari pertama. Penulisan cache membawa markup 25% di atas harga input dasar, yang terbayar pada permintaan kedua yang mencapai cache.
2. Tambahkan pencarian alat setelah set alat Anda tumbuh melampaui kira-kira 20 alat atau penggunaan konteks dasar Anda menjadi terlihat.
3. Tambahkan pengeditan konteks setelah percakapan individual mulai berjalan cukup lama sehingga hasil awal menjadi tidak relevan.
4. Pertimbangkan pemanggilan alat terprogram jika Anda melihat rantai berulang dari pemanggilan alat kecil yang dapat dijalankan sebagai satu batch.

## Langkah berikutnya

<CardGroup cols={2}>
  <Card
    title="Alat pencarian alat"
    icon="magnifying-glass"
    href="/docs/id/agents-and-tools/tool-use/tool-search-tool"
  >
    Muat definisi alat sesuai permintaan alih-alih di awal.
  </Card>
  <Card
    title="Pemanggilan alat terprogram"
    icon="code"
    href="/docs/id/agents-and-tools/tool-use/programmatic-tool-calling"
  >
    Runtuhkan rantai pemanggilan alat menjadi satu skrip yang dapat dieksekusi.
  </Card>
  <Card
    title="Penggunaan alat dengan penyimpanan prompt"
    icon="database"
    href="/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching"
  >
    Simpan cache definisi alat di seluruh permintaan untuk mengurangi biaya token.
  </Card>
  <Card
    title="Pengeditan konteks"
    icon="scissors"
    href="/docs/id/build-with-claude/context-editing"
  >
    Pangkas hasil alat yang sudah usang dari percakapan yang berjalan lama.
  </Card>
</CardGroup>