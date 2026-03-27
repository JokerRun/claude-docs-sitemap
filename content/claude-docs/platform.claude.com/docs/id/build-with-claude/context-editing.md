---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/context-editing
fetched_at: 2026-03-27T03:10:39.282195Z
sha256: a065f9359969dfa05d6d64344425701b2ee1b8598f1e153aa1c8ca13a9c58862
---

# Pengeditan konteks

Kelola konteks percakapan secara otomatis saat berkembang dengan pengeditan konteks.

---

## Ikhtisar

<Note>
Untuk sebagian besar kasus penggunaan, [kompaksi sisi server](/docs/id/build-with-claude/compaction) adalah strategi utama untuk mengelola konteks dalam percakapan yang berjalan lama. Strategi di halaman ini berguna untuk skenario tertentu di mana Anda memerlukan kontrol yang lebih terperinci atas konten yang dihapus.
</Note>

Pengeditan konteks memungkinkan Anda menghapus konten tertentu secara selektif dari riwayat percakapan saat berkembang. Selain mengoptimalkan biaya dan tetap dalam batas, ini tentang secara aktif mengkurasi apa yang dilihat Claude: konteks adalah sumber daya terbatas dengan hasil yang semakin berkurang, dan konten yang tidak relevan menurunkan fokus model. Pengeditan konteks memberi Anda kontrol runtime yang terperinci atas kurasi tersebut. Untuk prinsip-prinsip yang lebih luas di balik manajemen konteks, lihat [Rekayasa konteks yang efektif](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Halaman ini mencakup:

- **Penghapusan hasil alat** - Terbaik untuk alur kerja agentik dengan penggunaan alat yang berat di mana hasil alat lama tidak lagi diperlukan
- **Penghapusan blok pemikiran** - Untuk mengelola blok pemikiran saat menggunakan pemikiran yang diperluas, dengan opsi untuk mempertahankan pemikiran terbaru untuk kesinambungan konteks
- **Kompaksi sisi klien SDK** - Alternatif berbasis SDK untuk manajemen konteks berbasis ringkasan (kompaksi sisi server umumnya lebih disukai)

| Pendekatan | Tempat berjalan | Strategi | Cara kerjanya |
|----------|---------------|------------|--------------|
| **Sisi server** | API | Penghapusan hasil alat (`clear_tool_uses_20250919`)<br/>Penghapusan blok pemikiran (`clear_thinking_20251015`) | Diterapkan sebelum prompt mencapai Claude. Menghapus konten tertentu dari riwayat percakapan. Setiap strategi dapat dikonfigurasi secara independen. |
| **Sisi klien** | SDK | Kompaksi | Tersedia di [SDK Python dan TypeScript](/docs/id/api/client-sdks) saat menggunakan [`tool_runner`](/docs/id/agents-and-tools/tool-use/implement-tool-use#tool-runner-beta). Menghasilkan ringkasan dan mengganti riwayat percakapan penuh. Lihat [Kompaksi sisi klien](#client-side-compaction-sdk) di bawah. |

## Strategi sisi server

<Note>
Pengeditan konteks saat ini dalam versi beta dengan dukungan untuk penghapusan hasil alat dan penghapusan blok pemikiran. Untuk mengaktifkannya, gunakan header beta `context-management-2025-06-27` dalam permintaan API Anda.

Bagikan umpan balik tentang fitur ini melalui [formulir umpan balik](https://forms.gle/YXC2EKGMhjN1c4L88).
</Note>

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

### Penghapusan hasil alat

Strategi `clear_tool_uses_20250919` menghapus hasil alat ketika konteks percakapan tumbuh melampaui ambang batas yang Anda konfigurasi. Ini sangat berguna untuk alur kerja agentik dengan penggunaan alat yang berat. Hasil alat yang lebih lama (seperti konten file atau hasil pencarian) tidak lagi diperlukan setelah Claude memprosesnya.

Saat diaktifkan, API secara otomatis menghapus hasil alat tertua dalam urutan kronologis. Setiap hasil yang dihapus digantikan dengan teks placeholder sehingga Claude mengetahui bahwa itu telah dihapus. Secara default, hanya hasil alat yang dihapus. Anda dapat secara opsional menghapus hasil alat dan panggilan alat (parameter penggunaan alat) dengan mengatur `clear_tool_inputs` ke true.

### Penghapusan blok pemikiran

Strategi `clear_thinking_20251015` mengelola blok `thinking` dalam percakapan ketika pemikiran yang diperluas diaktifkan. Strategi ini memberi Anda kontrol atas pelestarian pemikiran: Anda dapat memilih untuk menyimpan lebih banyak blok pemikiran untuk mempertahankan kesinambungan penalaran, atau menghapusnya lebih agresif untuk menghemat ruang konteks.

<Tip>
**Perilaku default:** Ketika pemikiran yang diperluas diaktifkan tanpa mengonfigurasi strategi `clear_thinking_20251015`, API secara otomatis hanya menyimpan blok pemikiran dari giliran asisten terakhir (setara dengan `keep: {type: "thinking_turns", value: 1}`).

Untuk memaksimalkan cache hits, pertahankan semua blok pemikiran dengan mengatur `keep: "all"`.
</Tip>

Giliran percakapan asisten dapat mencakup beberapa blok konten (misalnya saat menggunakan alat) dan beberapa blok pemikiran (misalnya dengan [pemikiran yang diselingi](/docs/id/build-with-claude/extended-thinking#interleaved-thinking)).

### Pengeditan konteks terjadi di sisi server

Pengeditan konteks diterapkan di sisi server sebelum prompt mencapai Claude. Aplikasi klien Anda mempertahankan riwayat percakapan penuh yang tidak dimodifikasi. Anda tidak perlu menyinkronkan status klien Anda dengan versi yang telah diedit. Terus kelola riwayat percakapan penuh Anda secara lokal seperti biasa.

### Pengeditan konteks dan caching prompt

Interaksi pengeditan konteks dengan [caching prompt](/docs/id/build-with-claude/prompt-caching) bervariasi berdasarkan strategi:

- **Penghapusan hasil alat**: Membatalkan prefiks prompt yang di-cache ketika konten dihapus. Untuk mengatasinya, hapus cukup token agar pembatalan cache sepadan. Gunakan parameter `clear_at_least` untuk memastikan jumlah minimum token dihapus setiap kali. Anda akan dikenakan biaya penulisan cache setiap kali konten dihapus, tetapi permintaan berikutnya dapat menggunakan kembali prefiks yang baru di-cache.

- **Penghapusan blok pemikiran**: Ketika blok pemikiran **disimpan** dalam konteks (tidak dihapus), cache prompt dipertahankan, memungkinkan cache hits dan mengurangi biaya token input. Ketika blok pemikiran **dihapus**, cache dibatalkan pada titik di mana penghapusan terjadi. Konfigurasikan parameter `keep` berdasarkan apakah Anda ingin memprioritaskan kinerja cache atau ketersediaan jendela konteks.

## Model yang didukung

Pengeditan konteks tersedia di:

- Claude Opus 4.6 (`claude-opus-4-6`)
- Claude Opus 4.5 (`claude-opus-4-5-20251101`)
- Claude Opus 4.1 (`claude-opus-4-1-20250805`)
- Claude Opus 4 (`claude-opus-4-20250514`)
- Claude Sonnet 4.6 (`claude-sonnet-4-6`)
- Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)

## Penggunaan penghapusan hasil alat

Cara paling sederhana untuk mengaktifkan penghapusan hasil alat adalah dengan hanya menentukan jenis strategi. Semua [opsi konfigurasi](#configuration-options-for-tool-result-clearing) lainnya menggunakan nilai defaultnya:

<CodeGroup>

```bash cURL
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": "Search for recent developments in AI"
            }
        ],
        "tools": [
            {
                "type": "web_search_20250305",
                "name": "web_search"
            }
        ],
        "context_management": {
            "edits": [
                {"type": "clear_tool_uses_20250919"}
            ]
        }
    }'
```

```python Python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Search for recent developments in AI"}],
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    betas=["context-management-2025-06-27"],
    context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages: [
    {
      role: "user",
      content: "Search for recent developments in AI"
    }
  ],
  tools: [
    {
      type: "web_search_20250305",
      name: "web_search"
    }
  ],
  context_management: {
    edits: [{ type: "clear_tool_uses_20250919" }]
  },
  betas: ["context-management-2025-06-27"]
});
```

</CodeGroup>

### Konfigurasi lanjutan

Anda dapat menyesuaikan perilaku penghapusan hasil alat dengan parameter tambahan:

<CodeGroup>

```bash cURL
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": "Create a simple command line calculator app using Python"
            }
        ],
        "tools": [
            {
                "type": "text_editor_20250728",
                "name": "str_replace_based_edit_tool",
                "max_characters": 10000
            },
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 3
            }
        ],
        "context_management": {
            "edits": [
                {
                    "type": "clear_tool_uses_20250919",
                    "trigger": {
                        "type": "input_tokens",
                        "value": 30000
                    },
                    "keep": {
                        "type": "tool_uses",
                        "value": 3
                    },
                    "clear_at_least": {
                        "type": "input_tokens",
                        "value": 5000
                    },
                    "exclude_tools": ["web_search"]
                }
            ]
        }
    }'
```

```python Python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Create a simple command line calculator app using Python",
        }
    ],
    tools=[
        {
            "type": "text_editor_20250728",
            "name": "str_replace_based_edit_tool",
            "max_characters": 10000,
        },
        {"type": "web_search_20250305", "name": "web_search", "max_uses": 3},
    ],
    betas=["context-management-2025-06-27"],
    context_management={
        "edits": [
            {
                "type": "clear_tool_uses_20250919",
                # Picu penghapusan ketika ambang batas terlampaui
                "trigger": {"type": "input_tokens", "value": 30000},
                # Jumlah penggunaan alat yang disimpan setelah penghapusan
                "keep": {"type": "tool_uses", "value": 3},
                # Opsional: Hapus setidaknya sebanyak ini token
                "clear_at_least": {"type": "input_tokens", "value": 5000},
                # Kecualikan alat-alat ini dari penghapusan
                "exclude_tools": ["web_search"],
            }
        ]
    },
)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages: [
    {
      role: "user",
      content: "Create a simple command line calculator app using Python"
    }
  ],
  tools: [
    {
      type: "text_editor_20250728",
      name: "str_replace_based_edit_tool",
      max_characters: 10000
    },
    {
      type: "web_search_20250305",
      name: "web_search",
      max_uses: 3
    }
  ],
  betas: ["context-management-2025-06-27"],
  context_management: {
    edits: [
      {
        type: "clear_tool_uses_20250919",
        // Picu penghapusan ketika ambang batas terlampaui
        trigger: {
          type: "input_tokens",
          value: 30000
        },
        // Jumlah penggunaan alat yang disimpan setelah penghapusan
        keep: {
          type: "tool_uses",
          value: 3
        },
        // Opsional: Hapus setidaknya sebanyak ini token
        clear_at_least: {
          type: "input_tokens",
          value: 5000
        },
        // Kecualikan alat-alat ini dari penghapusan
        exclude_tools: ["web_search"]
      }
    ]
  }
});
```

</CodeGroup>

## Penggunaan penghapusan blok pemikiran

Aktifkan penghapusan blok pemikiran untuk mengelola konteks dan caching prompt secara efektif ketika pemikiran yang diperluas diaktifkan:

<CodeGroup>

```bash cURL
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-opus-4-6",
        "max_tokens": 1024,
        "messages": [/* ... */],
        "thinking": {
            "type": "enabled",
            "budget_tokens": 10000
        },
        "context_management": {
            "edits": [
                {
                    "type": "clear_thinking_20251015",
                    "keep": {
                        "type": "thinking_turns",
                        "value": 2
                    }
                }
            ]
        }
    }'
```

```python Python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[...],
    thinking={"type": "enabled", "budget_tokens": 10000},
    betas=["context-management-2025-06-27"],
    context_management={
        "edits": [
            {
                "type": "clear_thinking_20251015",
                "keep": {"type": "thinking_turns", "value": 2},
            }
        ]
    },
)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    // ...
  ],
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  betas: ["context-management-2025-06-27"],
  context_management: {
    edits: [
      {
        type: "clear_thinking_20251015",
        keep: {
          type: "thinking_turns",
          value: 2
        }
      }
    ]
  }
});
```

</CodeGroup>

### Opsi konfigurasi untuk penghapusan blok pemikiran

Strategi `clear_thinking_20251015` mendukung konfigurasi berikut:

| Opsi konfigurasi | Default | Deskripsi |
|---------------------|---------|-------------|
| `keep` | `{type: "thinking_turns", value: 1}` | Mendefinisikan berapa banyak giliran asisten terbaru dengan blok pemikiran yang akan dipertahankan. Gunakan `{type: "thinking_turns", value: N}` di mana N harus > 0 untuk menyimpan N giliran terakhir, atau `"all"` untuk menyimpan semua blok pemikiran. |

**Contoh konfigurasi:**

Simpan blok pemikiran dari 3 giliran asisten terakhir:

```json
{
  "type": "clear_thinking_20251015",
  "keep": {
    "type": "thinking_turns",
    "value": 3
  }
}
```

Simpan semua blok pemikiran (memaksimalkan cache hits):

```json
{
  "type": "clear_thinking_20251015",
  "keep": "all"
}
```

### Menggabungkan strategi

Anda dapat menggunakan penghapusan blok pemikiran dan penghapusan hasil alat secara bersamaan:

<Note>
Saat menggunakan beberapa strategi, strategi `clear_thinking_20251015` harus dicantumkan pertama dalam array `edits`.
</Note>

<CodeGroup>

```python Python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[...],
    thinking={"type": "enabled", "budget_tokens": 10000},
    tools=[...],
    betas=["context-management-2025-06-27"],
    context_management={
        "edits": [
            {
                "type": "clear_thinking_20251015",
                "keep": {"type": "thinking_turns", "value": 2},
            },
            {
                "type": "clear_tool_uses_20250919",
                "trigger": {"type": "input_tokens", "value": 50000},
                "keep": {"type": "tool_uses", "value": 5},
            },
        ]
    },
)
```

```typescript TypeScript
const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    // ...
  ],
  thinking: {
    type: "enabled",
    budget_tokens: 10000
  },
  tools: [
    // ...
  ],
  betas: ["context-management-2025-06-27"],
  context_management: {
    edits: [
      {
        type: "clear_thinking_20251015",
        keep: {
          type: "thinking_turns",
          value: 2
        }
      },
      {
        type: "clear_tool_uses_20250919",
        trigger: {
          type: "input_tokens",
          value: 50000
        },
        keep: {
          type: "tool_uses",
          value: 5
        }
      }
    ]
  }
});
```

</CodeGroup>

## Opsi konfigurasi untuk penghapusan hasil alat

| Opsi konfigurasi | Default | Deskripsi |
|---------------------|---------|-------------|
| `trigger` | 100.000 token input | Mendefinisikan kapan strategi pengeditan konteks diaktifkan. Setelah prompt melampaui ambang batas ini, penghapusan akan dimulai. Anda dapat menentukan nilai ini dalam `input_tokens` atau `tool_uses`. |
| `keep` | 3 penggunaan alat | Mendefinisikan berapa banyak pasangan penggunaan/hasil alat terbaru yang disimpan setelah penghapusan terjadi. API menghapus interaksi alat tertua terlebih dahulu, mempertahankan yang paling baru. |
| `clear_at_least` | Tidak ada | Memastikan jumlah minimum token dihapus setiap kali strategi diaktifkan. Jika API tidak dapat menghapus setidaknya jumlah yang ditentukan, strategi tidak akan diterapkan. Ini membantu menentukan apakah penghapusan konteks sepadan dengan pembatalan cache prompt Anda. |
| `exclude_tools` | Tidak ada | Daftar nama alat yang penggunaan dan hasilnya tidak boleh pernah dihapus. Berguna untuk mempertahankan konteks penting. |
| `clear_tool_inputs` | `false` | Mengontrol apakah parameter panggilan alat dihapus bersama dengan hasil alat. Secara default, hanya hasil alat yang dihapus sementara panggilan alat asli Claude tetap terlihat. |

## Respons pengeditan konteks

Anda dapat melihat pengeditan konteks mana yang diterapkan pada permintaan Anda menggunakan bidang respons `context_management`, bersama dengan statistik berguna tentang konten dan token input yang dihapus.

```json Response
{
  "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message",
  "role": "assistant",
  "content": [
    // ...
  ],
  "usage": {
    // ...
  },
  "context_management": {
    "applied_edits": [
      // Saat menggunakan `clear_thinking_20251015`
      {
        "type": "clear_thinking_20251015",
        "cleared_thinking_turns": 3,
        "cleared_input_tokens": 15000
      },
      // Saat menggunakan `clear_tool_uses_20250919`
      {
        "type": "clear_tool_uses_20250919",
        "cleared_tool_uses": 8,
        "cleared_input_tokens": 50000
      }
    ]
  }
}
```

Untuk respons streaming, pengeditan konteks akan disertakan dalam event `message_delta` terakhir:

```json Streaming Response
{
  "type": "message_delta",
  "delta": {
    "stop_reason": "end_turn",
    "stop_sequence": null
  },
  "usage": {
    "output_tokens": 1024
  },
  "context_management": {
    "applied_edits": [
      // ...
    ]
  }
}
```

## Penghitungan token

Endpoint [penghitungan token](/docs/id/build-with-claude/token-counting) mendukung manajemen konteks, memungkinkan Anda melihat pratinjau berapa banyak token yang akan digunakan prompt Anda setelah pengeditan konteks diterapkan.

<CodeGroup>

```bash cURL
curl https://api.anthropic.com/v1/messages/count_tokens \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "anthropic-beta: context-management-2025-06-27" \
    --data '{
        "model": "claude-opus-4-6",
        "messages": [
            {
                "role": "user",
                "content": "Continue our conversation..."
            }
        ],
        "tools": [...],
        "context_management": {
            "edits": [
                {
                    "type": "clear_tool_uses_20250919",
                    "trigger": {
                        "type": "input_tokens",
                        "value": 30000
                    },
                    "keep": {
                        "type": "tool_uses",
                        "value": 5
                    }
                }
            ]
        }
    }'
```

```python Python
response = client.beta.messages.count_tokens(
    model="claude-opus-4-6",
    messages=[{"role": "user", "content": "Continue our conversation..."}],
    tools=[...],  # Definisi alat Anda
    betas=["context-management-2025-06-27"],
    context_management={
        "edits": [
            {
                "type": "clear_tool_uses_20250919",
                "trigger": {"type": "input_tokens", "value": 30000},
                "keep": {"type": "tool_uses", "value": 5},
            }
        ]
    },
)

print(f"Token asli: {response.context_management['original_input_tokens']}")
print(f"Setelah penghapusan: {response.input_tokens}")
print(
    f"Penghematan: {response.context_management['original_input_tokens'] - response.input_tokens} token"
)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await anthropic.beta.messages.countTokens({
  model: "claude-opus-4-6",
  messages: [
    {
      role: "user",
      content: "Continue our conversation..."
    }
  ],
  tools: [
    // ...
  ], // Definisi alat Anda
  betas: ["context-management-2025-06-27"],
  context_management: {
    edits: [
      {
        type: "clear_tool_uses_20250919",
        trigger: {
          type: "input_tokens",
          value: 30000
        },
        keep: {
          type: "tool_uses",
          value: 5
        }
      }
    ]
  }
});

console.log(`Token asli: ${response.context_management?.original_input_tokens}`);
console.log(`Setelah penghapusan: ${response.input_tokens}`);
console.log(
  `Penghematan: ${(response.context_management?.original_input_tokens || 0) - response.input_tokens} token`
);
```
</CodeGroup>

```json Response
{
  "input_tokens": 25000,
  "context_management": {
    "original_input_tokens": 70000
  }
}
```

Respons menampilkan jumlah token akhir setelah manajemen konteks diterapkan (`input_tokens`) dan jumlah token asli sebelum penghapusan terjadi (`original_input_tokens`).

## Menggunakan dengan Alat Memori

Pengeditan konteks dapat dikombinasikan dengan [alat memori](/docs/id/agents-and-tools/tool-use/memory-tool). Ketika konteks percakapan Anda mendekati ambang batas penghapusan yang dikonfigurasi, Claude menerima peringatan otomatis untuk menyimpan informasi penting. Ini memungkinkan Claude menyimpan hasil alat atau konteks ke file memorinya sebelum dihapus dari riwayat percakapan.

Kombinasi ini memungkinkan Anda untuk:

- **Menyimpan konteks penting**: Claude dapat menulis informasi penting dari hasil alat ke file memori sebelum hasil tersebut dihapus
- **Mempertahankan alur kerja yang berjalan lama**: Mengaktifkan alur kerja agentik yang sebaliknya akan melampaui batas konteks dengan memindahkan informasi ke penyimpanan persisten
- **Mengakses informasi sesuai kebutuhan**: Claude dapat mencari informasi yang sebelumnya dihapus dari file memori saat diperlukan, daripada menyimpan semuanya di jendela konteks aktif

Misalnya, dalam alur kerja pengeditan file di mana Claude melakukan banyak operasi, Claude dapat merangkum perubahan yang telah selesai ke file memori saat konteks berkembang. Ketika hasil alat dihapus, Claude tetap memiliki akses ke informasi tersebut melalui sistem memorinya dan dapat terus bekerja secara efektif.

Untuk menggunakan kedua fitur bersama, aktifkan keduanya dalam permintaan API Anda:

<CodeGroup>

```python Python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    messages=[...],
    tools=[
        {"type": "memory_20250818", "name": "memory"},
        # Alat lainnya
    ],
    betas=["context-management-2025-06-27"],
    context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await anthropic.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  messages: [
    // ...
  ],
  tools: [
    {
      type: "memory_20250818",
      name: "memory"
    }
    // Alat lainnya
  ],
  betas: ["context-management-2025-06-27"],
  context_management: {
    edits: [{ type: "clear_tool_uses_20250919" }]
  }
});
```

</CodeGroup>

## Kompaksi sisi klien (SDK)

<Warning>
**Kompaksi sisi server direkomendasikan daripada kompaksi SDK.** [Kompaksi sisi server](/docs/id/build-with-claude/compaction) menangani manajemen konteks secara otomatis dengan kompleksitas integrasi yang lebih rendah, perhitungan penggunaan token yang lebih baik, dan tanpa batasan sisi klien. Gunakan kompaksi SDK hanya jika Anda secara khusus memerlukan kontrol sisi klien atas proses peringkasan.
</Warning>

<Note>
Kompaksi tersedia di [SDK Python dan TypeScript](/docs/id/api/client-sdks) saat menggunakan [metode `tool_runner`](/docs/id/agents-and-tools/tool-use/implement-tool-use#tool-runner-beta).
</Note>

Kompaksi adalah fitur SDK yang secara otomatis mengelola konteks percakapan dengan menghasilkan ringkasan ketika penggunaan token tumbuh terlalu besar. Tidak seperti strategi pengeditan konteks sisi server yang menghapus konten, kompaksi menginstruksikan Claude untuk meringkas riwayat percakapan, kemudian mengganti riwayat penuh dengan ringkasan tersebut. Ini memungkinkan Claude untuk terus mengerjakan tugas yang berjalan lama yang sebaliknya akan melampaui [jendela konteks](/docs/id/build-with-claude/context-windows).

### Cara kerja kompaksi

Ketika kompaksi diaktifkan, SDK memantau penggunaan token setelah setiap respons model:

1. **Pemeriksaan ambang batas:** SDK menghitung total token sebagai `input_tokens + cache_creation_input_tokens + cache_read_input_tokens + output_tokens`.
2. **Pembuatan ringkasan:** Ketika ambang batas terlampaui, prompt ringkasan disuntikkan sebagai giliran pengguna, dan Claude menghasilkan ringkasan terstruktur yang dibungkus dalam tag `<summary></summary>`.
3. **Penggantian konteks:** SDK mengekstrak ringkasan dan mengganti seluruh riwayat pesan dengannya.
4. **Kelanjutan:** Percakapan dilanjutkan dari ringkasan, dengan Claude melanjutkan dari tempat terakhir berhenti.

### Menggunakan kompaksi

Tambahkan `compaction_control` ke panggilan `tool_runner` Anda:

<CodeGroup>

```python Python
import anthropic

client = anthropic.Anthropic()

runner = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=4096,
    tools=[...],
    messages=[
        {
            "role": "user",
            "content": "Analyze all the files in this directory and write a summary report.",
        }
    ],
    compaction_control={"enabled": True, "context_token_threshold": 100000},
)

for message in runner:
    print(f"Token yang digunakan: {message.usage.input_tokens}")

final = runner.until_done()
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const runner = client.beta.messages.toolRunner({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  tools: [
    // ...
  ],
  messages: [
    {
      role: "user",
      content: "Analyze all the files in this directory and write a summary report."
    }
  ],
  compactionControl: {
    enabled: true,
    contextTokenThreshold: 100000
  }
});

for await (const message of runner) {
  console.log("Token yang digunakan:", message.usage.input_tokens);
}

const finalMessage = await runner.runUntilDone();
```

</CodeGroup>

#### Apa yang terjadi selama kompaksi

Saat percakapan berkembang, riwayat pesan terakumulasi:

**Sebelum kompaksi (mendekati 100k token):**
```json
[
  { "role": "user", "content": "Analyze all files and write a report..." },
  { "role": "assistant", "content": "I'll help. Let me start by reading..." },
  {
    "role": "user",
    "content": [{ "type": "tool_result", "tool_use_id": "...", "content": "..." }]
  },
  { "role": "assistant", "content": "Based on file1.txt, I see..." },
  {
    "role": "user",
    "content": [{ "type": "tool_result", "tool_use_id": "...", "content": "..." }]
  },
  { "role": "assistant", "content": "After analyzing file2.txt..." }
  // ... 50 pertukaran lagi seperti ini ...
]
```

Ketika token melampaui ambang batas, SDK menyuntikkan permintaan ringkasan dan Claude menghasilkan ringkasan. Seluruh riwayat kemudian digantikan:

**Setelah kompaksi (kembali ke ~2-3k token):**
```json
[
  {
    "role": "assistant",
    "content": "# Task Overview\nThe user requested analysis of directory files to produce a summary report...\n\n# Current State\nAnalyzed 52 files across 3 subdirectories. Key findings documented in report.md...\n\n# Important Discoveries\n- Configuration files use YAML format\n- Found 3 deprecated dependencies\n- Test coverage at 67%\n\n# Next Steps\n1. Analyze remaining files in /src/legacy\n2. Complete final report sections...\n\n# Context to Preserve\nUser prefers markdown format with executive summary first..."
  }
]
```

Claude melanjutkan bekerja dari ringkasan ini seolah-olah itu adalah riwayat percakapan asli.

### Opsi konfigurasi

| Parameter | Tipe | Diperlukan | Default | Deskripsi |
|-----------|------|----------|---------|-------------|
| `enabled` | boolean | Ya | - | Apakah akan mengaktifkan kompaksi otomatis |
| `context_token_threshold` | number | Tidak | 100.000 | Jumlah token di mana kompaksi dipicu |
| `model` | string | Tidak | Sama dengan model utama | Model yang digunakan untuk menghasilkan ringkasan |
| `summary_prompt` | string | Tidak | Lihat di bawah | Prompt kustom untuk pembuatan ringkasan |

#### Memilih ambang batas token

Ambang batas menentukan kapan kompaksi terjadi. Ambang batas yang lebih rendah berarti kompaksi lebih sering dengan jendela konteks yang lebih kecil. Ambang batas yang lebih tinggi memungkinkan lebih banyak konteks tetapi berisiko mencapai batas.

<CodeGroup>

```python Python
# Kompaksi lebih sering untuk skenario dengan memori terbatas
compaction_control = {"enabled": True, "context_token_threshold": 50000}

# Kompaksi lebih jarang ketika Anda membutuhkan lebih banyak konteks
compaction_control = {"enabled": True, "context_token_threshold": 150000}
```

```typescript TypeScript hidelines={1,7..9,-1}
const _ = {
  // Kompaksi lebih sering untuk skenario dengan memori terbatas
  compactionControl: {
    enabled: true,
    contextTokenThreshold: 50000
  }
};

const __ = {
  // Kompaksi lebih jarang ketika Anda membutuhkan lebih banyak konteks
  compactionControl: {
    enabled: true,
    contextTokenThreshold: 150000
  }
};
```

</CodeGroup>

#### Menggunakan model berbeda untuk ringkasan

Anda dapat menggunakan model yang lebih cepat atau lebih murah untuk menghasilkan ringkasan:

<CodeGroup>

```python Python
compaction_control = {
    "enabled": True,
    "context_token_threshold": 100000,
    "model": "claude-haiku-4-5",
}
```

```typescript TypeScript hidelines={1,-1}
const _ = {
  compactionControl: {
    enabled: true,
    contextTokenThreshold: 100000,
    model: "claude-haiku-4-5"
  }
};
```

</CodeGroup>

#### Prompt ringkasan kustom

Anda dapat menyediakan prompt kustom untuk kebutuhan domain tertentu. Prompt Anda harus menginstruksikan Claude untuk membungkus ringkasannya dalam tag `<summary></summary>`.

<CodeGroup>

```python Python
compaction_control = {
    "enabled": True,
    "context_token_threshold": 100000,
    "summary_prompt": """Rangkum penelitian yang telah dilakukan sejauh ini, termasuk:
- Sumber yang dikonsultasikan dan temuan utama
- Pertanyaan yang dijawab dan hal yang belum diketahui
- Langkah selanjutnya yang direkomendasikan

Bungkus ringkasan Anda dalam tag <summary></summary>.""",
}
```

```typescript TypeScript hidelines={1,-1}
const _ = {
  compactionControl: {
    enabled: true,
    contextTokenThreshold: 100000,
    summaryPrompt: `Rangkum penelitian yang telah dilakukan sejauh ini, termasuk:
- Sumber yang dikonsultasikan dan temuan utama
- Pertanyaan yang dijawab dan hal yang belum diketahui
- Langkah selanjutnya yang direkomendasikan

Bungkus ringkasan Anda dalam tag <summary></summary>.`
  }
};
```

</CodeGroup>

### Prompt ringkasan default

Prompt ringkasan bawaan menginstruksikan Claude untuk membuat ringkasan kelanjutan terstruktur yang mencakup:

1. **Ikhtisar Tugas:** Permintaan inti pengguna, kriteria keberhasilan, dan batasan.
2. **Status Saat Ini:** Apa yang telah diselesaikan, file yang dimodifikasi, dan artefak yang dihasilkan.
3. **Temuan Penting:** Batasan teknis, keputusan yang dibuat, kesalahan yang diselesaikan, dan pendekatan yang gagal.
4. **Langkah Selanjutnya:** Tindakan spesifik yang diperlukan, pemblokir, dan urutan prioritas.
5. **Konteks yang Perlu Dipertahankan:** Preferensi pengguna, detail spesifik domain, dan komitmen yang dibuat.

Struktur ini memungkinkan Claude untuk melanjutkan pekerjaan secara efisien tanpa kehilangan konteks penting atau mengulangi kesalahan.

<section title="Lihat prompt default lengkap">

```text
You have been working on the task described above but have not yet completed it. Write a continuation summary that will allow you (or another instance of yourself) to resume work efficiently in a future context window where the conversation history will be replaced with this summary. Your summary should be structured, concise, and actionable. Include:

1. Task Overview
The user's core request and success criteria
Any clarifications or constraints they specified

2. Current State
What has been completed so far
Files created, modified, or analyzed (with paths if relevant)
Key outputs or artifacts produced

3. Important Discoveries
Technical constraints or requirements uncovered
Decisions made and their rationale
Errors encountered and how they were resolved
What approaches were tried that didn't work (and why)

4. Next Steps
Specific actions needed to complete the task
Any blockers or open questions to resolve
Priority order if multiple steps remain

5. Context to Preserve
User preferences or style requirements
Domain-specific details that aren't obvious
Any promises made to the user

Be concise but complete—err on the side of including information that would prevent duplicate work or repeated mistakes. Write in a way that enables immediate resumption of the task.

Wrap your summary in <summary></summary> tags.
```

</section>

### Keterbatasan

#### Alat sisi server

<Warning>
Kompaksi memerlukan pertimbangan khusus saat menggunakan alat sisi server seperti [pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool) atau [pengambilan web](/docs/id/agents-and-tools/tool-use/web-fetch-tool).
</Warning>

Saat menggunakan alat sisi server, SDK mungkin salah menghitung penggunaan token, menyebabkan kompaksi dipicu pada waktu yang salah.

Misalnya, setelah operasi pencarian web, respons API mungkin menampilkan:

```json
{
  "usage": {
    "input_tokens": 63000,
    "cache_read_input_tokens": 270000,
    "output_tokens": 1400
  }
}
```

SDK menghitung total penggunaan sebagai 63.000 + 270.000 = 333.000 token. Namun, nilai `cache_read_input_tokens` mencakup pembacaan yang terakumulasi dari beberapa panggilan API internal yang dibuat oleh alat sisi server, bukan konteks percakapan aktual Anda. Panjang konteks nyata Anda mungkin hanya 63.000 `input_tokens`, tetapi SDK melihat 333k dan memicu kompaksi secara prematur.

**Solusi alternatif:**

- Gunakan endpoint [penghitungan token](/docs/id/build-with-claude/token-counting) untuk mendapatkan panjang konteks yang akurat
- Hindari kompaksi saat menggunakan alat sisi server secara ekstensif

#### Kasus tepi penggunaan alat

Ketika kompaksi dipicu sementara respons penggunaan alat sedang tertunda, SDK menghapus blok penggunaan alat dari riwayat pesan sebelum menghasilkan ringkasan. Claude akan mengeluarkan kembali panggilan alat setelah melanjutkan dari ringkasan jika masih diperlukan.

### Memantau kompaksi

Aktifkan logging untuk melacak kapan kompaksi terjadi:

<CodeGroup>

```python Python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("anthropic.lib.tools").setLevel(logging.INFO)

# Log akan menampilkan:
# INFO: Token usage 105000 has exceeded the threshold of 100000. Performing compaction.
# INFO: Compaction complete. New token usage: 2500
```

```typescript TypeScript
// SDK mencatat peristiwa kompaksi ke konsol
// Anda akan melihat pesan seperti:
// Token usage 105000 has exceeded the threshold of 100000. Performing compaction.
// Compaction complete. New token usage: 2500
```

</CodeGroup>

### Kapan menggunakan kompaksi

**Kasus penggunaan yang baik:**

- Tugas agen yang berjalan lama yang memproses banyak file atau sumber data
- Alur kerja penelitian yang mengakumulasi sejumlah besar informasi
- Tugas multi-langkah dengan kemajuan yang jelas dan terukur
- Tugas yang menghasilkan artefak (file, laporan) yang bertahan di luar percakapan

**Kasus penggunaan yang kurang ideal:**

- Tugas yang memerlukan pengingatan tepat dari detail percakapan awal
- Alur kerja yang menggunakan alat sisi server secara ekstensif
- Tugas yang perlu mempertahankan status tepat di banyak variabel