---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/manage-tool-context
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: e4f543cac88e6eb5ad615101fa8f4333b2700dd1ac5be514e80c1abd934c9eac
---

# Mengelola konteks alat

Pilih antara pencarian alat, pemanggilan alat terprogram, caching prompt, dan pengeditan konteks untuk mengelola pembengkakan konteks.

---

Definisi alat dan blok `tool_result` yang terakumulasi menghabiskan "context window" (jendela konteks) Anda. Agen yang berjalan lama dengan banyak alat atau banyak giliran dapat menghabiskan konteks yang tersedia sebelum tugas selesai. Empat pendekatan berikut mengatasi hal ini di titik-titik berbeda dalam pipeline.

## Empat pendekatan \{#the-four-approaches}

Setiap pendekatan menargetkan sumber tekanan konteks yang berbeda. Pilih pendekatan yang sesuai dengan ke mana token Anda terpakai.

| Pendekatan | Apa yang dikurangi | Kapan cocok digunakan | Pelajari lebih lanjut |
| --- | --- | --- | --- |
| Pencarian alat | Definisi alat yang dimuat di awal | Kumpulan alat besar (20+ alat) di mana sebagian besar alat tidak diperlukan di setiap giliran | [Alat pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool) |
| Pemanggilan alat terprogram | Bolak-balik `tool_result` | Rangkaian pemanggilan alat yang dapat dieksekusi sebagai satu skrip | [Pemanggilan alat terprogram](/docs/id/agents-and-tools/tool-use/programmatic-tool-calling) |
| Caching prompt | Biaya token dari definisi alat yang berulang | Kumpulan alat yang stabil di banyak permintaan | [Penggunaan alat dengan caching prompt](/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching) |
| Pengeditan konteks | Blok `tool_result` lama dalam riwayat | Percakapan panjang di mana hasil awal tidak lagi relevan | [Pengeditan konteks](/docs/id/build-with-claude/context-editing) |

### Pencarian alat \{#tool-search}

Pencarian alat menjaga definisi alat tetap di luar jendela konteks sampai Claude memintanya. Alih-alih mengirim 50 skema alat di awal, Anda mengirim satu alat `tool_search` dan membiarkan Claude menemukan sisanya sesuai kebutuhan. Ini menukar sedikit "latency" (latensi) tambahan (satu giliran ekstra untuk mencari alat) dengan pengurangan besar dalam penggunaan konteks dasar.

### Pemanggilan alat terprogram \{#programmatic-tool-calling}

Pemanggilan alat terprogram meringkas serangkaian pemanggilan alat menjadi satu blok kode yang ditulis oleh Claude dan dijalankan oleh sandbox eksekusi kode Anthropic. Alih-alih lima kali bolak-balik `tool_use` dan `tool_result`, Claude menghasilkan satu skrip yang memanggil kelima fungsi tersebut dari dalam sandbox. Hasil antara tidak pernah masuk ke riwayat percakapan.

### Caching prompt \{#prompt-caching}

"Prompt caching" (caching prompt) tidak mengurangi jumlah token dalam konteks, tetapi mengurangi biaya yang Anda bayar untuk token tersebut pada permintaan berikutnya. Jika definisi alat Anda stabil, cache sekali dan gunakan kembali prefiks yang di-cache di ribuan permintaan. Ini adalah pilihan yang tepat ketika kumpulan alat besar tetapi tetap.

### Pengeditan konteks \{#context-editing}

Pengeditan konteks menghapus blok `tool_result` lama dari riwayat percakapan setelah blok tersebut tidak lagi diperlukan. Loop agen yang panjang mungkin menghasilkan ratusan hasil antara yang berguna pada saat itu tetapi sekarang hanya menjadi beban. Pengeditan konteks memungkinkan Anda memangkasnya tanpa memulai ulang percakapan.

## Menggabungkan pendekatan \{#combining-approaches}

Pendekatan-pendekatan ini dapat dikombinasikan. Agen yang berjalan lama mungkin menggunakan pencarian alat untuk menjaga kumpulan alat tetap ramping, caching prompt untuk mengamortisasi biaya definisi yang tersisa, dan pengeditan konteks untuk memangkas hasil usang seiring bertambahnya percakapan. Masing-masing menyelesaikan bagian masalah yang berbeda, sehingga tidak ada konflik dalam menggunakannya bersama-sama.

Titik awal yang masuk akal untuk agen bervolume tinggi:

1. Aktifkan caching prompt pada definisi alat Anda sejak hari pertama. Penulisan cache dikenakan markup 25% di atas harga input dasar, yang akan terbayar kembali pada permintaan kedua yang mengenai cache.
2. Tambahkan pencarian alat setelah kumpulan alat Anda tumbuh melewati sekitar 20 alat atau penggunaan konteks dasar Anda mulai terasa signifikan.
3. Tambahkan pengeditan konteks setelah percakapan individual mulai berjalan cukup lama sehingga hasil awal menjadi tidak relevan.
4. Pertimbangkan pemanggilan alat terprogram jika Anda melihat rangkaian berulang dari pemanggilan alat kecil yang dapat dijalankan sebagai satu batch.

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card
    title="Alat pencarian alat"
    icon="magnifying-glass"
    href="/docs/id/agents-and-tools/tool-use/tool-search-tool"
  >
    Muat definisi alat sesuai kebutuhan, bukan di awal.
  </Card>
  <Card
    title="Pemanggilan alat terprogram"
    icon="code"
    href="/docs/id/agents-and-tools/tool-use/programmatic-tool-calling"
  >
    Ringkas rangkaian pemanggilan alat menjadi satu skrip yang dapat dieksekusi.
  </Card>
  <Card
    title="Penggunaan alat dengan caching prompt"
    icon="database"
    href="/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching"
  >
    Cache definisi alat di seluruh permintaan untuk memangkas biaya token.
  </Card>
  <Card
    title="Pengeditan konteks"
    icon="scissors"
    href="/docs/id/build-with-claude/context-editing"
  >
    Pangkas hasil alat yang usang dari percakapan yang berjalan lama.
  </Card>
</CardGroup>