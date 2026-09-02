---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/manage-tool-context
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: d6d52ef861cc816328982e0f26d3d4ae066156e8a419eb68e82bb6c1b6d612df
---

---
title: Mengelola konteks alat
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/manage-tool-context
description: Pilih antara pencarian alat, pemanggilan alat terprogram, caching prompt, dan pengeditan konteks untuk mengelola pembengkakan konteks.
---

Definisi alat dan blok `tool_result` yang terakumulasi menghabiskan "context window" (jendela konteks) Anda. Agen yang berjalan lama dengan banyak alat atau banyak giliran dapat menghabiskan konteks yang tersedia sebelum tugas selesai. Empat pendekatan mengatasi hal ini di titik yang berbeda dalam pipeline.

## Empat pendekatan

Setiap pendekatan menargetkan sumber tekanan konteks yang berbeda. Pilih pendekatan yang sesuai dengan ke mana token Anda mengalir.

| Pendekatan                  | Apa yang dikurangi                           | Kapan cocok digunakan                                                                      | Pelajari lebih lanjut                                                                                                               |
| --------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| Pencarian alat              | Definisi alat yang dimuat di awal            | Kumpulan alat besar (20+ alat) di mana sebagian besar alat tidak diperlukan setiap giliran | [Alat pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool)                               |
| Pemanggilan alat terprogram | Perjalanan bolak-balik `tool_result`         | Rangkaian pemanggilan alat yang dapat dieksekusi sebagai satu skrip                        | [Pemanggilan alat terprogram](https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling)              |
| Caching prompt              | Biaya token dari definisi alat yang berulang | Kumpulan alat yang stabil di banyak permintaan                                             | [Penggunaan alat dengan caching prompt](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching) |
| Pengeditan konteks          | Blok `tool_result` lama dalam riwayat        | Percakapan panjang di mana hasil awal tidak lagi relevan                                   | [Pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing)                                         |

### Pencarian alat

"Tool search" (pencarian alat) menjaga definisi alat tetap di luar jendela konteks sampai Claude memintanya. Alih-alih mengirim 50 skema alat di awal, Anda mengirim satu alat `tool_search` dan membiarkan Claude menemukan sisanya sesuai permintaan. Ini menukar sedikit "latency" (latensi) (satu giliran tambahan untuk mencari alat) dengan pengurangan besar dalam penggunaan konteks dasar.

### Pemanggilan alat terprogram

"Programmatic tool calling" (pemanggilan alat terprogram) meringkas serangkaian pemanggilan alat menjadi satu blok kode yang ditulis Claude dan dijalankan oleh sandbox eksekusi kode Anthropic. Alih-alih lima perjalanan bolak-balik `tool_use` dan `tool_result`, Claude menghasilkan satu skrip yang memanggil kelima fungsi dari dalam sandbox. Hasil perantara tidak pernah masuk ke riwayat percakapan.

### Caching prompt

"Prompt caching" (caching prompt) tidak mengurangi jumlah token dalam konteks, tetapi mengurangi biaya yang Anda bayar untuk token tersebut pada permintaan berikutnya. Jika definisi alat Anda stabil, cache sekali dan gunakan kembali prefiks yang di-cache di ribuan permintaan. Ini adalah pilihan yang tepat ketika kumpulan alat besar tetapi tetap.

### Pengeditan konteks

"Context editing" (pengeditan konteks) menghapus blok `tool_result` lama dari riwayat percakapan setelah blok tersebut memenuhi tujuannya. Loop agen yang panjang mungkin menghasilkan ratusan hasil perantara yang berguna pada saat itu tetapi sekarang menjadi beban mati. Pengeditan konteks memungkinkan Anda memangkasnya tanpa memulai ulang percakapan.

## Menggabungkan pendekatan

Pendekatan-pendekatan ini dapat dikombinasikan. Agen yang berjalan lama mungkin menggunakan pencarian alat untuk menjaga kumpulan alat tetap ramping, caching prompt untuk mengamortisasi biaya definisi yang tersisa, dan pengeditan konteks untuk memangkas hasil yang sudah usang seiring bertambahnya percakapan. Masing-masing menyelesaikan bagian masalah yang berbeda, sehingga tidak ada konflik dalam menggunakannya bersama-sama.

Titik awal yang masuk akal untuk agen bervolume tinggi:

1. Aktifkan caching prompt pada definisi alat Anda sejak hari pertama. Penulisan cache dikenakan markup 25% di atas harga input dasar, yang terbayar kembali pada permintaan kedua yang mengenai cache.
2. Tambahkan pencarian alat setelah kumpulan alat Anda bertambah melebihi sekitar 20 alat atau penggunaan konteks dasar Anda menjadi terasa.
3. Tambahkan pengeditan konteks setelah percakapan individual mulai berjalan cukup lama sehingga hasil awal menjadi tidak relevan.
4. Pertimbangkan pemanggilan alat terprogram jika Anda melihat rangkaian berulang dari pemanggilan alat kecil yang dapat dijalankan sebagai satu batch.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Alat pencarian alat" icon="magnifying-glass" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool">
    Muat definisi alat sesuai permintaan alih-alih di awal.
  </Card>

  <Card title="Pemanggilan alat terprogram" icon="code" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/programmatic-tool-calling">
    Ringkas rangkaian pemanggilan alat menjadi satu skrip yang dapat dieksekusi.
  </Card>

  <Card title="Penggunaan alat dengan caching prompt" icon="database" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching">
    Cache definisi alat di seluruh permintaan untuk memangkas biaya token.
  </Card>

  <Card title="Pengeditan konteks" icon="scissors" href="https://platform.claude.com/docs/id/build-with-claude/context-editing">
    Pangkas hasil alat yang sudah usang dari percakapan yang berjalan lama.
  </Card>
</CardGroup>
