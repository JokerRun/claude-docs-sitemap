---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: a03fd119127f76af4650116fb4a2d91a72233b6707143e6a31f4869324ddc5cf
---

---
title: Penggunaan alat dengan caching prompt
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching
description: Cache definisi alat di seluruh giliran dan pahami apa yang membatalkan cache Anda.
---

Halaman ini membahas “prompt caching” (caching prompt) untuk definisi alat: di mana menempatkan breakpoint `cache_control`, bagaimana `defer_loading` mempertahankan cache Anda, dan apa yang membatalkannya. Untuk caching prompt secara umum, lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching).

## cache\_control pada definisi alat

Tempatkan `cache_control: {"type": "ephemeral"}` pada alat terakhir dalam array `tools` Anda. Ini meng-cache seluruh prefiks definisi alat, dari alat pertama hingga breakpoint yang ditandai:

```json
{
  "tools": [
    {
      "name": "get_weather",
      "description": "Get the current weather in a given location",
      "input_schema": {
        "type": "object",
        "properties": {
          "location": { "type": "string" }
        },
        "required": ["location"]
      }
    },
    {
      "name": "get_time",
      "description": "Get the current time in a given time zone",
      "input_schema": {
        "type": "object",
        "properties": {
          "timezone": { "type": "string" }
        },
        "required": ["timezone"]
      },
      "cache_control": { "type": "ephemeral" }
    }
  ]
}
```

Untuk `mcp_toolset`, breakpoint `cache_control` ditempatkan pada alat terakhir dalam set tersebut. Anda tidak mengontrol urutan alat di dalam toolset MCP, jadi tempatkan breakpoint pada entri `mcp_toolset` itu sendiri dan API akan menerapkannya pada alat terakhir yang diperluas.

Entri toolset [penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) dan [penggunaan browser](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) mengikuti aturan yang sama: tempatkan `cache_control` pada entri toolset itu sendiri, dan breakpoint akan jatuh setelah definisi toolset tersebut. `cache_control` tidak diterima di dalam entri `configs` milik anggota, karena anggota toolset dimuat sebagai satu definisi. Di dalam sebuah [tindakan batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions), penanda `cache_control` pada blok `tool_use` atau `tool_result` anggota mana pun dalam giliran tersebut diterima dan berlaku di akhir batch itu, sehingga beberapa penanda dalam satu batch bertindak sebagai satu breakpoint. Setiap penanda tetap dihitung terhadap batas permintaan sebanyak [empat breakpoint](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#when-to-use-multiple-breakpoints), jadi gunakan paling banyak satu di setiap giliran.

## defer\_loading dan pelestarian cache

Alat yang ditangguhkan (deferred) tidak disertakan dalam prefiks prompt sistem. Ketika model menemukan alat yang ditangguhkan melalui [pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool), definisinya ditambahkan secara inline sebagai blok `tool_reference` dalam riwayat percakapan. Prefiks tidak tersentuh, sehingga caching prompt tetap terjaga.

Anda dapat memulai percakapan dengan sekumpulan kecil alat yang selalu dimuat (di-cache), membiarkan model menemukan alat tambahan sesuai kebutuhan, dan mempertahankan cache hit yang sama di setiap giliran.

`defer_loading` juga bekerja secara independen dari konstruksi grammar untuk [mode strict](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use). Grammar dibangun dari daftar lengkap alat terlepas dari alat mana yang ditangguhkan, sehingga caching prompt dan caching grammar keduanya tetap terjaga ketika alat dimuat secara dinamis.

## Apa yang membatalkan cache Anda

Cache mengikuti hierarki prefiks (`tools` → `system` → `messages`), sehingga perubahan pada satu tingkat membatalkan tingkat tersebut dan semua yang ada setelahnya:

| Perubahan                                             | Membatalkan                                                                                                                                                                                                                                                                                        |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Memodifikasi definisi alat                            | Seluruh cache (alat, sistem, pesan)                                                                                                                                                                                                                                                                |
| Mengaktifkan/menonaktifkan pencarian web atau kutipan | Cache system dan messages                                                                                                                                                                                                                                                                          |
| Mengubah `tool_choice`                                | Cache messages                                                                                                                                                                                                                                                                                     |
| Mengubah `disable_parallel_tool_use`                  | Cache messages                                                                                                                                                                                                                                                                                     |
| Mengubah ada/tidaknya gambar                          | Cache messages                                                                                                                                                                                                                                                                                     |
| Mengubah parameter thinking                           | Cache messages selalu; cache alat dan system juga pada model yang merender konfigurasi thinking sebelum keduanya (lihat [Pemikiran dan caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching))                                                |
| Mengubah `output_config.effort`                       | Dapat membatalkan cache messages, dan pada beberapa model juga cache alat dan system (lihat [Pemikiran dan caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching)); mengirimkan nilai default secara eksplisit setara dengan menghilangkannya |

<Note>
  Jika Anda perlu memvariasikan `tool_choice` di tengah percakapan, pertimbangkan untuk menempatkan breakpoint cache sebelum titik variasi tersebut.
</Note>

## Hasil alat server di-cache secara otomatis

Ketika permintaan Anda mengaktifkan caching prompt dan Claude menggunakan [alat server](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools) seperti pencarian web, web fetch, atau eksekusi kode, API secara otomatis menempatkan breakpoint cache pada hasil alat server sebelum menjalankan iterasi berikutnya dari loop agentik. Ini memungkinkan iterasi selanjutnya dalam permintaan yang sama membaca prefiks yang terus bertambah dari cache alih-alih memprosesnya ulang.

Breakpoint otomatis ini selalu menggunakan TTL default 5 menit, terlepas dari TTL apa pun yang Anda tetapkan pada penanda `cache_control` Anda sendiri. Dalam `usage` respons, penulisan ini muncul di bawah `cache_creation.ephemeral_5m_input_tokens`, sehingga Anda mungkin melihat penulisan cache 5 menit bahkan ketika setiap `cache_control` yang Anda tetapkan menggunakan TTL 1 jam.

Perilaku ini hanya berlaku ketika permintaan Anda sudah memiliki setidaknya satu penanda `cache_control`. Permintaan tanpa caching prompt tidak menerima breakpoint otomatis.

## Tabel interaksi per alat

| Alat                                                                                                   | Pertimbangan caching                                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool)         | Mengaktifkan atau menonaktifkan membatalkan cache system dan messages                                                                                                                                                                                                      |
| [Web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool)              | Mengaktifkan atau menonaktifkan membatalkan cache system dan messages                                                                                                                                                                                                      |
| [Eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool)     | Status container independen dari cache prompt                                                                                                                                                                                                                              |
| [Pencarian alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool)       | Alat yang ditemukan dimuat sebagai blok `tool_reference`, mempertahankan cache prefiks                                                                                                                                                                                     |
| [Penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) | Keberadaan screenshot memengaruhi cache messages; `cache_control` ditempatkan pada entri toolset (lihat [cache\_control pada definisi alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching#cache-control-on-tool-definitions)) |
| [Penggunaan browser](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool)   | Keberadaan screenshot memengaruhi cache messages; `cache_control` ditempatkan pada entri toolset (lihat [cache\_control pada definisi alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching#cache-control-on-tool-definitions)) |
| [Editor teks](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool)          | Alat klien standar, tidak ada interaksi caching khusus                                                                                                                                                                                                                     |
| [Bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool)                        | Alat klien standar, tidak ada interaksi caching khusus                                                                                                                                                                                                                     |
| [Memori](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool)                    | Alat klien standar, tidak ada interaksi caching khusus                                                                                                                                                                                                                     |

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Caching prompt" icon="database" href="https://platform.claude.com/docs/id/build-with-claude/prompt-caching">
    Pelajari model caching prompt secara lengkap, termasuk TTL dan harga.
  </Card>

  <Card title="Alat pencarian alat" icon="magnifying-glass" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool">
    Muat alat sesuai permintaan tanpa merusak cache Anda.
  </Card>

  <Card title="Referensi alat" icon="book" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference">
    Jelajahi semua alat yang tersedia dan parameternya.
  </Card>
</CardGroup>
