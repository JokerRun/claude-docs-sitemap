---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-use-with-prompt-caching
fetched_at: 2026-06-28T03:16:32.677203Z
sha256: 5982f01bf319b1b32796a56dbfa22e710571693dad5fd9576e5a59084aabb59c
---

# Penggunaan alat dengan caching prompt

Cache definisi alat di seluruh giliran dan pahami apa yang membatalkan cache Anda.

---

Halaman ini membahas caching prompt untuk definisi alat: di mana menempatkan breakpoint `cache_control`, bagaimana `defer_loading` mempertahankan cache Anda, dan apa yang membatalkannya. Untuk caching prompt secara umum, lihat [Caching prompt](/docs/id/build-with-claude/prompt-caching).

## cache\_control pada definisi alat

Tempatkan `cache_control: {"type": "ephemeral"}` pada alat terakhir dalam array `tools` Anda. Ini akan meng-cache seluruh prefiks definisi alat, dari alat pertama hingga breakpoint yang ditandai:

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

Untuk `mcp_toolset`, breakpoint `cache_control` ditempatkan pada alat terakhir dalam set tersebut. Anda tidak mengontrol urutan alat dalam toolset MCP, jadi tempatkan breakpoint pada entri `mcp_toolset` itu sendiri dan API akan menerapkannya pada alat terakhir yang diperluas.

## defer\_loading dan pemeliharaan cache

Alat yang ditangguhkan tidak disertakan dalam prefiks prompt sistem. Ketika model menemukan alat yang ditangguhkan melalui [pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool), definisinya ditambahkan secara inline sebagai blok `tool_reference` dalam riwayat percakapan. Prefiks tidak tersentuh, sehingga caching prompt tetap terjaga.

Ini berarti menambahkan alat secara dinamis melalui pencarian alat tidak merusak cache Anda. Anda dapat memulai percakapan dengan sekumpulan kecil alat yang selalu dimuat (di-cache), membiarkan model menemukan alat tambahan sesuai kebutuhan, dan tetap mendapatkan cache hit yang sama di setiap giliran.

`defer_loading` juga bekerja secara independen dari konstruksi grammar untuk [mode ketat](/docs/id/agents-and-tools/tool-use/strict-tool-use). Grammar dibangun dari toolset lengkap terlepas dari alat mana yang ditangguhkan, sehingga caching prompt dan caching grammar keduanya tetap terjaga ketika alat dimuat secara dinamis.

## Apa yang membatalkan cache Anda

Cache mengikuti hierarki prefiks (`tools` → `system` → `messages`), sehingga perubahan pada satu level akan membatalkan level tersebut dan semua yang ada setelahnya:

| Perubahan                                            | Membatalkan                             |
| ---------------------------------------------------- | --------------------------------------- |
| Memodifikasi definisi alat                           | Seluruh cache (tools, system, messages) |
| Mengaktifkan/menonaktifkan pencarian web atau sitasi | Cache system dan messages               |
| Mengubah `tool_choice`                               | Cache messages                          |
| Mengubah `disable_parallel_tool_use`                 | Cache messages                          |
| Mengubah keberadaan gambar (ada/tidak ada)           | Cache messages                          |
| Mengubah parameter thinking                          | Cache messages                          |

<Note>
  Jika Anda perlu memvariasikan `tool_choice` di tengah percakapan, pertimbangkan untuk menempatkan breakpoint cache sebelum titik variasi tersebut.
</Note>

## Hasil alat server di-cache secara otomatis

Ketika permintaan Anda mengaktifkan caching prompt dan Claude menggunakan [alat server](/docs/id/agents-and-tools/tool-use/server-tools) seperti pencarian web, web fetch, atau eksekusi kode, API secara otomatis menempatkan breakpoint cache pada hasil alat server sebelum menjalankan iterasi berikutnya dari loop agentik. Ini memungkinkan iterasi selanjutnya dalam permintaan yang sama membaca prefiks yang terus bertambah dari cache alih-alih memprosesnya ulang.

Breakpoint otomatis ini selalu menggunakan TTL default 5 menit, terlepas dari TTL apa pun yang Anda tetapkan pada penanda `cache_control` Anda sendiri. Dalam `usage` respons, penulisan ini muncul di bawah `cache_creation.ephemeral_5m_input_tokens`, sehingga Anda mungkin melihat penulisan cache 5 menit meskipun setiap `cache_control` yang Anda tetapkan menggunakan TTL 1 jam.

Perilaku ini hanya berlaku ketika permintaan Anda sudah memiliki setidaknya satu penanda `cache_control`. Permintaan tanpa caching prompt tidak menerima breakpoint otomatis.

## Tabel interaksi per alat

| Alat                                                                        | Pertimbangan caching                                                                   |
| --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [Pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool)         | Mengaktifkan atau menonaktifkan akan membatalkan cache system dan messages             |
| [Web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool)              | Mengaktifkan atau menonaktifkan akan membatalkan cache system dan messages             |
| [Eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool)     | Status container independen dari cache prompt                                          |
| [Pencarian alat](/docs/id/agents-and-tools/tool-use/tool-search-tool)       | Alat yang ditemukan dimuat sebagai blok `tool_reference`, mempertahankan cache prefiks |
| [Penggunaan komputer](/docs/id/agents-and-tools/tool-use/computer-use-tool) | Keberadaan screenshot memengaruhi cache messages                                       |
| [Editor teks](/docs/id/agents-and-tools/tool-use/text-editor-tool)          | Alat klien standar, tidak ada interaksi caching khusus                                 |
| [Bash](/docs/id/agents-and-tools/tool-use/bash-tool)                        | Alat klien standar, tidak ada interaksi caching khusus                                 |
| [Memory](/docs/id/agents-and-tools/tool-use/memory-tool)                    | Alat klien standar, tidak ada interaksi caching khusus                                 |

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Caching prompt" icon="database" href="/docs/id/build-with-claude/prompt-caching">
    Pelajari model caching prompt lengkap, termasuk TTL dan harga.
  </Card>

  <Card title="Pencarian alat" icon="magnifying-glass" href="/docs/id/agents-and-tools/tool-use/tool-search-tool">
    Muat alat sesuai permintaan tanpa merusak cache Anda.
  </Card>

  <Card title="Referensi alat" icon="book" href="/docs/id/agents-and-tools/tool-use/tool-reference">
    Jelajahi semua alat yang tersedia dan parameternya.
  </Card>
</CardGroup>
