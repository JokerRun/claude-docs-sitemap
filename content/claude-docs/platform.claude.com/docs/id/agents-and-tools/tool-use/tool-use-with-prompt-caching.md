---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching
fetched_at: 2026-04-25T03:09:48.142425Z
sha256: 65703973049165fdf34e418db33c4b731c3c535bb56da7898da7a4687b7f68b1
---

# Penggunaan alat dengan prompt caching

Cache definisi alat di seluruh turn dan pahami apa yang membatalkan cache Anda.

---

Halaman ini mencakup prompt caching untuk definisi alat: di mana menempatkan breakpoint `cache_control`, bagaimana `defer_loading` menjaga cache Anda, dan apa yang membatalkannya. Untuk prompt caching umum, lihat [Prompt caching](/docs/id/build-with-claude/prompt-caching).

## cache_control pada definisi alat

Tempatkan `cache_control: {"type": "ephemeral"}` pada alat terakhir dalam array `tools` Anda. Ini melakukan cache pada seluruh prefix definisi alat, dari alat pertama melalui breakpoint yang ditandai:

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

Untuk `mcp_toolset`, breakpoint `cache_control` berada pada alat terakhir dalam set. Anda tidak mengontrol urutan alat dalam toolset MCP, jadi tempatkan breakpoint pada entri `mcp_toolset` itu sendiri dan API menerapkannya pada alat yang diperluas terakhir.

## defer_loading dan preservasi cache

Alat yang ditunda tidak disertakan dalam prefix system-prompt. Ketika model menemukan alat yang ditunda melalui [tool search](/docs/id/agents-and-tools/tool-use/tool-search-tool), definisi ditambahkan inline sebagai blok `tool_reference` dalam riwayat percakapan. Prefix tetap tidak tersentuh, sehingga prompt caching dipertahankan.

Ini berarti menambahkan alat secara dinamis melalui tool search tidak merusak cache Anda. Anda dapat memulai percakapan dengan set kecil alat yang selalu dimuat (cached), membiarkan model menemukan alat tambahan sesuai kebutuhan, dan menjaga cache hit yang sama di setiap turn.

`defer_loading` juga bertindak secara independen dari konstruksi grammar untuk [strict mode](/docs/id/agents-and-tools/tool-use/strict-tool-use). Grammar dibangun dari toolset lengkap terlepas dari alat mana yang ditunda, sehingga prompt caching dan grammar caching keduanya dipertahankan ketika alat dimuat secara dinamis.

## Apa yang membatalkan cache Anda

Cache mengikuti hierarki prefix (`tools` → `system` → `messages`), jadi perubahan pada satu level membatalkan level itu dan semuanya setelahnya:

| Perubahan | Membatalkan |
|---|---|
| Memodifikasi definisi alat | Seluruh cache (tools, system, messages) |
| Mengalihkan web search atau citations | Cache system dan messages |
| Mengubah `tool_choice` | Cache messages |
| Mengubah `disable_parallel_tool_use` | Cache messages |
| Mengalihkan kehadiran gambar | Cache messages |
| Mengubah parameter thinking | Cache messages |

<Note>
Jika Anda perlu memvariasikan `tool_choice` di tengah percakapan, pertimbangkan untuk menempatkan breakpoint cache sebelum titik variasi.
</Note>

## Tabel interaksi per-alat

| Alat | Pertimbangan Caching |
|---|---|
| [Web search](/docs/id/agents-and-tools/tool-use/web-search-tool) | Mengaktifkan atau menonaktifkan membatalkan cache system dan messages |
| [Web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool) | Mengaktifkan atau menonaktifkan membatalkan cache system dan messages |
| [Code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool) | Status container independen dari prompt cache |
| [Tool search](/docs/id/agents-and-tools/tool-use/tool-search-tool) | Alat yang ditemukan dimuat sebagai blok `tool_reference`, menjaga cache prefix |
| [Computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool) | Kehadiran screenshot mempengaruhi cache messages |
| [Text editor](/docs/id/agents-and-tools/tool-use/text-editor-tool) | Alat klien standar, tidak ada interaksi caching khusus |
| [Bash](/docs/id/agents-and-tools/tool-use/bash-tool) | Alat klien standar, tidak ada interaksi caching khusus |
| [Memory](/docs/id/agents-and-tools/tool-use/memory-tool) | Alat klien standar, tidak ada interaksi caching khusus |

## Langkah berikutnya

<CardGroup cols={3}>
  <Card title="Prompt caching" icon="database" href="/docs/id/build-with-claude/prompt-caching">
    Pelajari model prompt caching lengkap, termasuk TTL dan pricing.
  </Card>
  <Card title="Tool search" icon="magnifying-glass" href="/docs/id/agents-and-tools/tool-use/tool-search-tool">
    Muat alat sesuai permintaan tanpa merusak cache Anda.
  </Card>
  <Card title="Tool reference" icon="book" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Jelajahi semua alat yang tersedia dan parameternya.
  </Card>
</CardGroup>