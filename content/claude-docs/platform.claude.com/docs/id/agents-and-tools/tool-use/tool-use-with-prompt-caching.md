---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 12d12ffea95db66f431d05b02be836dfd37e029b6326b07fd3700bcab56d5a30
---

---
title: Penggunaan alat dengan caching prompt
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching
description: Cache definisi alat di seluruh giliran dan pahami apa yang membatalkan cache Anda.
---

Halaman ini membahas "prompt caching" (caching prompt) untuk definisi alat: di mana menempatkan breakpoint `cache_control`, bagaimana `defer_loading` mempertahankan cache Anda, dan apa yang membatalkannya. Untuk caching prompt secara umum, lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching).

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

Entri toolset [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) dan [browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) mengikuti aturan yang sama: tempatkan `cache_control` pada entri toolset itu sendiri, dan breakpoint akan ditempatkan setelah definisi toolset tersebut. `cache_control` tidak diterima di dalam entri `configs` milik anggota, karena anggota toolset dimuat sebagai satu definisi. Di dalam [batch action](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions), penanda `cache_control` pada blok `tool_use` atau `tool_result` anggota mana pun dalam giliran tersebut diterima dan berlaku di akhir batch itu, sehingga beberapa penanda dalam satu batch bertindak sebagai satu breakpoint. Setiap penanda tetap dihitung terhadap batas permintaan sebanyak [empat breakpoint](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#when-to-use-multiple-breakpoints), jadi gunakan satu per giliran.

## defer\_loading dan pelestarian cache

Alat yang ditangguhkan (deferred) tidak disertakan dalam prefiks prompt sistem. Ketika model menemukan alat yang ditangguhkan melalui [tool search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool), definisinya ditambahkan secara inline sebagai blok `tool_reference` dalam riwayat percakapan. Prefiks tidak tersentuh, sehingga caching prompt tetap terjaga.

Ini berarti menambahkan alat secara dinamis melalui tool search tidak merusak cache Anda. Anda dapat memulai percakapan dengan sekumpulan kecil alat yang selalu dimuat (di-cache), membiarkan model menemukan alat tambahan sesuai kebutuhan, dan mempertahankan cache hit yang sama di setiap giliran.

`defer_loading` juga bekerja secara independen dari konstruksi grammar untuk [strict mode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use). Grammar dibangun dari toolset lengkap terlepas dari alat mana yang ditangguhkan, sehingga caching prompt dan caching grammar keduanya tetap terjaga ketika alat dimuat secara dinamis.

## Apa yang membatalkan cache Anda

Cache mengikuti hierarki prefiks (`tools` → `system` → `messages`), sehingga perubahan pada satu tingkat membatalkan tingkat tersebut dan semua yang ada setelahnya:

| Perubahan                                            | Membatalkan                                                                                                                                                                                                             |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Memodifikasi definisi alat                           | Seluruh cache (tools, system, messages)                                                                                                                                                                                 |
| Mengaktifkan/menonaktifkan web search atau citations | Cache system dan messages                                                                                                                                                                                               |
| Mengubah `tool_choice`                               | Cache messages                                                                                                                                                                                                          |
| Mengubah `disable_parallel_tool_use`                 | Cache messages                                                                                                                                                                                                          |
| Mengubah ada/tidaknya gambar                         | Cache messages                                                                                                                                                                                                          |
| Mengubah parameter thinking                          | Cache messages selalu; cache alat dan system juga pada model yang merender konfigurasi thinking sebelum keduanya ([detail](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching)) |
| Mengubah `output_config.effort`                      | Sama seperti parameter thinking; menetapkan nilai default model secara eksplisit setara dengan menghilangkannya                                                                                                         |

<Note>
  Jika Anda perlu memvariasikan `tool_choice` di tengah percakapan, pertimbangkan untuk menempatkan breakpoint cache sebelum titik variasi tersebut.
</Note>

## Hasil server tool di-cache secara otomatis

Ketika permintaan Anda mengaktifkan caching prompt dan Claude menggunakan [server tool](https://platform.claude.com/docs/id/agents-and-tools/tool-use/server-tools) seperti web search, web fetch, atau code execution, API secara otomatis menempatkan breakpoint cache pada hasil server tool sebelum menjalankan iterasi berikutnya dari loop agentik. Ini memungkinkan iterasi selanjutnya dalam permintaan yang sama membaca prefiks yang terus bertambah dari cache alih-alih memprosesnya ulang.

Breakpoint otomatis ini selalu menggunakan TTL default 5 menit, terlepas dari TTL apa pun yang Anda tetapkan pada penanda `cache_control` Anda sendiri. Dalam `usage` respons, penulisan ini muncul di bawah `cache_creation.ephemeral_5m_input_tokens`, sehingga Anda mungkin melihat penulisan cache 5 menit bahkan ketika setiap `cache_control` yang Anda tetapkan menggunakan TTL 1 jam.

Perilaku ini hanya berlaku ketika permintaan Anda sudah memiliki setidaknya satu penanda `cache_control`. Permintaan tanpa caching prompt tidak menerima breakpoint otomatis.

## Tabel interaksi per alat

| Alat                                                                                                | Pertimbangan caching                                                                                                                                                                                                                                                       |
| --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Web search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool)         | Mengaktifkan atau menonaktifkan membatalkan cache system dan messages                                                                                                                                                                                                      |
| [Web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool)           | Mengaktifkan atau menonaktifkan membatalkan cache system dan messages                                                                                                                                                                                                      |
| [Code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool) | Status container independen dari cache prompt                                                                                                                                                                                                                              |
| [Tool search](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool)       | Alat yang ditemukan dimuat sebagai blok `tool_reference`, mempertahankan cache prefiks                                                                                                                                                                                     |
| [Computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool)     | Keberadaan screenshot memengaruhi cache messages; `cache_control` ditempatkan pada entri toolset (lihat [cache\_control pada definisi alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching#cache-control-on-tool-definitions)) |
| [Browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool)       | Keberadaan screenshot memengaruhi cache messages; `cache_control` ditempatkan pada entri toolset (lihat [cache\_control pada definisi alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching#cache-control-on-tool-definitions)) |
| [Text editor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool)       | Alat klien standar, tidak ada interaksi caching khusus                                                                                                                                                                                                                     |
| [Bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool)                     | Alat klien standar, tidak ada interaksi caching khusus                                                                                                                                                                                                                     |
| [Memory](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool)                 | Alat klien standar, tidak ada interaksi caching khusus                                                                                                                                                                                                                     |

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Caching prompt" icon="database" href="https://platform.claude.com/docs/id/build-with-claude/prompt-caching">
    Pelajari model caching prompt secara lengkap, termasuk TTL dan harga.
  </Card>

  <Card title="Tool search" icon="magnifying-glass" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-search-tool">
    Muat alat sesuai permintaan tanpa merusak cache Anda.
  </Card>

  <Card title="Referensi alat" icon="book" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-reference">
    Jelajahi semua alat yang tersedia dan parameternya.
  </Card>
</CardGroup>
