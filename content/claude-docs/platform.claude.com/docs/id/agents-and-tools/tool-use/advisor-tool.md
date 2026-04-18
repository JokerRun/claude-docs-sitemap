---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 6ed7c3f4def486af8b450ffdc776656b3fea09102b7de8a63155900f8052ad6c
---

# Alat advisor

Pasangkan model executor yang lebih cepat dengan model advisor yang lebih cerdas yang memberikan panduan strategis di tengah generasi.

---

Alat advisor memungkinkan model **executor** yang lebih cepat dan lebih murah untuk berkonsultasi dengan model **advisor** yang lebih cerdas di tengah generasi untuk mendapatkan panduan strategis. Advisor membaca percakapan lengkap, menghasilkan rencana atau koreksi arah (biasanya 400 hingga 700 token teks, 1.400 hingga 1.800 token total termasuk thinking), dan executor melanjutkan dengan tugas.

Pola ini cocok untuk beban kerja agentic dengan horizon panjang (agen coding, penggunaan komputer, pipeline penelitian multi-langkah) di mana sebagian besar giliran bersifat mekanis tetapi memiliki rencana yang sangat baik sangat penting. Anda mendapatkan kualitas yang mendekati advisor-solo sementara sebagian besar generasi token terjadi pada tingkat model executor.

<Note>
  Alat advisor sedang dalam beta. Sertakan header beta `advisor-tool-2026-03-01`
  dalam permintaan Anda. Untuk meminta akses atau berbagi umpan balik, hubungi
  tim akun Anthropic Anda.
</Note>

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

## Kapan menggunakannya

Benchmark awal menunjukkan keuntungan yang berarti untuk konfigurasi ini:

- **Anda saat ini menggunakan Sonnet untuk tugas kompleks:** Tambahkan Opus sebagai advisor untuk peningkatan kualitas dengan biaya yang sama atau lebih rendah.
- **Anda saat ini menggunakan Haiku dan menginginkan peningkatan kecerdasan:** Tambahkan Opus sebagai advisor. Harapkan biaya lebih tinggi dari Haiku saja, tetapi lebih rendah dari beralih executor ke model yang lebih besar.

Hasil tergantung pada tugas. Evaluasi pada beban kerja Anda sendiri.

Advisor adalah kecocokan yang lebih lemah untuk Q&A satu putaran (tidak ada yang direncanakan), pemilih model pass-through murni di mana pengguna Anda sudah memilih tradeoff biaya dan kualitas mereka sendiri, atau beban kerja di mana setiap giliran benar-benar memerlukan kemampuan penuh model advisor.

## Kompatibilitas model

Model executor (bidang `model` tingkat atas) dan model advisor (bidang `model` di dalam definisi alat) harus membentuk pasangan yang valid. Advisor harus setidaknya sama cerdas dengan executor.

| Model Executor                                | Model Advisor                      |
| ---------------------------------------------- | ----------------------------------- |
| Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) | Claude Opus 4.7 (`claude-opus-4-7`) |
| Claude Sonnet 4.6 (`claude-sonnet-4-6`)        | Claude Opus 4.7 (`claude-opus-4-7`) |
| Claude Opus 4.6 (`claude-opus-4-6`)            | Claude Opus 4.7 (`claude-opus-4-7`) |
| Claude Opus 4.7 (`claude-opus-4-7`)            | Claude Opus 4.7 (`claude-opus-4-7`) |

Jika Anda meminta pasangan yang tidak valid, API mengembalikan `400 invalid_request_error` yang menamai kombinasi yang tidak didukung.

## Ketersediaan platform

Alat advisor tersedia dalam beta di Claude API (Anthropic).

## Mulai cepat

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: advisor-tool-2026-03-01" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-sonnet-4-6",
        "max_tokens": 4096,
        "tools": [
            {
                "type": "advisor_20260301",
                "name": "advisor",
                "model": "claude-opus-4-7"
            }
        ],
        "messages": [{
            "role": "user",
            "content": "Build a concurrent worker pool in Go with graceful shutdown."
        }]
    }'
```

```bash CLI
ant beta:messages create --beta advisor-tool-2026-03-01 <<'YAML'
model: claude-sonnet-4-6
max_tokens: 4096
tools:
  - type: advisor_20260301
    name: advisor
    model: claude-opus-4-7
messages:
  - role: user
    content: Build a concurrent worker pool in Go with graceful shutdown.
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    betas=["advisor-tool-2026-03-01"],
    tools=[
        {
            "type": "advisor_20260301",
            "name": "advisor",
            "model": "claude-opus-4-7",
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "Build a concurrent worker pool in Go with graceful shutdown.",
        }
    ],
)

print(response)
```

```typescript TypeScript hidelines={1..5,-3..-1}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

async function main() {
  const response = await client.beta.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 4096,
    betas: ["advisor-tool-2026-03-01"],
    tools: [
      {
        type: "advisor_20260301",
        name: "advisor",
        model: "claude-opus-4-7"
      }
    ],
    messages: [
      {
        role: "user",
        content: "Build a concurrent worker pool in Go with graceful shutdown."
      }
    ]
  });

  console.log(response);
}

main().catch(console.error);
```

```csharp C# nocheck hidelines={1}
using Anthropic;
using Anthropic.Models.Beta.Messages;
using Messages = Anthropic.Models.Messages;

var client = new AnthropicClient();

var parameters = new MessageCreateParams
{
    Model = Messages::Model.ClaudeSonnet4_6,
    MaxTokens = 4096,
    Tools = new BetaToolUnion[]
    {
        new BetaAdvisorTool20260301
        {
            Model = Messages::Model.ClaudeOpus4_7
        }
    },
    Messages =
    [
        new BetaMessageParam
        {
            Role = Role.User,
            Content = "Build a concurrent worker pool in Go with graceful shutdown."
        }
    ],
    Betas = ["advisor-tool-2026-03-01"]
};

var response = await client.Beta.Messages.Create(parameters);
Console.WriteLine(response);
```

```go Go nocheck hidelines={1..11,-1}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     anthropic.ModelClaudeSonnet4_6,
		MaxTokens: 4096,
		Tools: []anthropic.BetaToolUnionParam{
			{OfAdvisorTool20260301: &anthropic.BetaAdvisorTool20260301Param{
				Model: anthropic.ModelClaudeOpus4_7,
			}},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Build a concurrent worker pool in Go with graceful shutdown.")),
		},
		Betas: []anthropic.AnthropicBeta{
			anthropic.AnthropicBetaAdvisorTool2026_03_01,
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->beta->messages->create(
    maxTokens: 4096,
    messages: [
        [
            'role' => 'user',
            'content' => 'Build a concurrent worker pool in Go with graceful shutdown.',
        ],
    ],
    model: 'claude-sonnet-4-6',
    tools: [
        [
            'type' => 'advisor_20260301',
            'name' => 'advisor',
            'model' => 'claude-opus-4-7',
        ],
    ],
    betas: ['advisor-tool-2026-03-01'],
);

echo $response;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.beta.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 4096,
  tools: [
    {
      type: "advisor_20260301",
      name: "advisor",
      model: "claude-opus-4-7"
    }
  ],
  messages: [
    {
      role: "user",
      content: "Build a concurrent worker pool in Go with graceful shutdown."
    }
  ],
  betas: ["advisor-tool-2026-03-01"]
)

puts response
```

</CodeGroup>

## Cara kerjanya

Ketika Anda menambahkan alat advisor ke array `tools` Anda, model executor memutuskan kapan harus memanggilnya, seperti alat lainnya. Ketika executor memanggil advisor:

1. Executor memancarkan blok `server_tool_use` dengan `name: "advisor"` dan `input` kosong. Executor menandakan waktu; server menyediakan konteks.
2. Anthropic menjalankan pass inferensi terpisah pada server model advisor, melewatkan transkrip lengkap executor. Advisor melihat system prompt, semua definisi alat, semua giliran sebelumnya, dan semua hasil alat sebelumnya.
3. Respons advisor kembali ke executor sebagai blok `advisor_tool_result`.
4. Executor terus menghasilkan, diinformasikan oleh saran.

Semua ini terjadi di dalam satu permintaan `/v1/messages`. Tidak ada perjalanan pulang-pergi tambahan di sisi Anda.

Advisor itu sendiri berjalan tanpa alat dan tanpa manajemen konteks. Blok thinking-nya dijatuhkan sebelum hasil kembali; hanya teks saran yang mencapai executor.

## Parameter alat

| Parameter               | Tipe           | Default      | Deskripsi                                                                                                                                        |
| ----------------------- | -------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                  | string         | _required_   | Harus `"advisor_20260301"`.                                                                                                                      |
| `name`                  | string         | _required_   | Harus `"advisor"`.                                                                                                                               |
| `model`                 | string         | _required_   | ID model advisor, seperti `"claude-opus-4-7"`. Ditagih dengan tarif model ini untuk sub-inferensi.                                             |
| `max_uses`              | integer        | unlimited    | Jumlah maksimum panggilan advisor yang diizinkan dalam satu permintaan. Setelah executor mencapai batas ini, panggilan advisor lebih lanjut mengembalikan `advisor_tool_result` dengan `error_code: "max_uses_exceeded"` dan executor melanjutkan tanpa saran lebih lanjut. Ini adalah batas per-permintaan, bukan batas per-percakapan; lihat [Kontrol biaya](#kontrol-biaya) untuk batas tingkat percakapan. |
| `caching`               | object \| null | `null` (off) | Mengaktifkan prompt caching untuk transkrip advisor sendiri di seluruh panggilan dalam percakapan. Lihat [Advisor prompt caching](#advisor-prompt-caching). |

Objek `caching` memiliki bentuk `{"type": "ephemeral", "ttl": "5m" | "1h"}`. Tidak seperti `cache_control` pada blok konten, ini bukan penanda breakpoint; ini adalah saklar on/off. Server memutuskan di mana batas cache berada.

## Struktur respons

### Panggilan advisor yang berhasil

Ketika advisor dipanggil, blok `server_tool_use` diikuti oleh blok `advisor_tool_result` dalam konten assistant:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Let me consult the advisor on this."
    },
    {
      "type": "server_tool_use",
      "id": "srvtoolu_abc123",
      "name": "advisor",
      "input": {}
    },
    {
      "type": "advisor_tool_result",
      "tool_use_id": "srvtoolu_abc123",
      "content": {
        "type": "advisor_result",
        "text": "Use a channel-based coordination pattern. The tricky part is draining in-flight work during shutdown: close the input channel first, then wait on a WaitGroup..."
      }
    },
    {
      "type": "text",
      "text": "Here's the implementation. I'm using a channel-based coordination pattern to avoid writer starvation..."
    }
  ]
}
```

`server_tool_use.input` selalu kosong. Server membangun tampilan advisor dari transkrip lengkap secara otomatis; tidak ada yang executor masukkan dalam `input` yang mencapai advisor.

### Varian hasil

Bidang `advisor_tool_result.content` adalah union yang didiskriminasi. Varian mana yang Anda terima tergantung pada model advisor:

| Varian                   | Bidang              | Dikembalikan ketika                                                       |
| ------------------------- | ------------------- | ------------------------------------------------------------------- |
| `advisor_result`          | `text`              | Model advisor mengembalikan plaintext (misalnya, Claude Opus 4.7). |
| `advisor_redacted_result` | `encrypted_content` | Model advisor mengembalikan output terenkripsi.                         |

Dengan `advisor_result`, bidang `text` berisi saran yang dapat dibaca manusia. Dengan `advisor_redacted_result`, bidang `encrypted_content` berisi blob buram yang tidak dapat Anda baca; pada giliran berikutnya, server mendekripsinya dan merender plaintext ke dalam prompt executor.

Dalam kedua kasus, bulatkan konten secara verbatim pada giliran berikutnya. Jika Anda beralih model advisor di tengah percakapan, cabang pada `content.type` untuk menangani kedua bentuk.

### Hasil kesalahan

Jika panggilan advisor gagal, hasil membawa kesalahan:

```json
{
  "type": "advisor_tool_result",
  "tool_use_id": "srvtoolu_abc123",
  "content": {
    "type": "advisor_tool_result_error",
    "error_code": "overloaded"
  }
}
```

Executor melihat kesalahan dan melanjutkan tanpa saran lebih lanjut. Permintaan itu sendiri tidak gagal.

| `error_code`              | Arti                                                                                                     |
| ------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `max_uses_exceeded`       | Permintaan mencapai batas `max_uses` yang ditetapkan pada definisi alat. Panggilan advisor lebih lanjut dalam permintaan yang sama mengembalikan kesalahan ini. |
| `too_many_requests`       | Sub-inferensi advisor dibatasi kecepatan.                                                                 |
| `overloaded`              | Sub-inferensi advisor mencapai batas kapasitas.                                                              |
| `prompt_too_long`         | Transkrip melebihi jendela konteks model advisor.                                                 |
| `execution_time_exceeded` | Sub-inferensi advisor habis waktu.                                                                        |
| `unavailable`             | Kegagalan advisor lainnya.                                                                                  |

Batas kecepatan advisor ditarik dari bucket per-model yang sama dengan panggilan langsung ke model advisor. Batas kecepatan pada advisor muncul sebagai `too_many_requests` di dalam hasil alat; batas kecepatan pada executor gagal seluruh permintaan dengan HTTP 429.

## Percakapan multi-putaran

Lewatkan konten assistant lengkap, termasuk blok `advisor_tool_result`, kembali ke API pada giliran berikutnya:

```python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "type": "advisor_20260301",
        "name": "advisor",
        "model": "claude-opus-4-7",
    }
]

messages = [
    {
        "role": "user",
        "content": "Build a concurrent worker pool in Go with graceful shutdown.",
    }
]

response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    betas=["advisor-tool-2026-03-01"],
    tools=tools,
    messages=messages,
)

# Append the full response content, including any advisor_tool_result blocks
messages.append({"role": "assistant", "content": response.content})

# Continue the conversation
messages.append({"role": "user", "content": "Now add a max-in-flight limit of 10."})

response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    betas=["advisor-tool-2026-03-01"],
    tools=tools,
    messages=messages,
)
```

Jika Anda menghilangkan alat advisor dari `tools` pada giliran lanjutan sementara riwayat pesan masih berisi blok `advisor_tool_result`, API mengembalikan `400 invalid_request_error`.

<Note>
  Alat advisor tidak memiliki batas tingkat percakapan bawaan. Untuk membatasi
  panggilan advisor di seluruh percakapan, hitunglah secara client-side. Ketika
  Anda mencapai batas Anda, hapus alat advisor dari array `tools` **dan** lepas
  semua blok `advisor_tool_result` dari riwayat pesan Anda untuk menghindari
  `400 invalid_request_error`.
</Note>

## Streaming

Sub-inferensi advisor tidak streaming. Stream executor dijeda saat advisor berjalan, kemudian hasil lengkap tiba dalam satu peristiwa.

Blok `server_tool_use` dengan `name: "advisor"` menandakan bahwa panggilan advisor dimulai. Jeda dimulai ketika blok itu ditutup (`content_block_stop`). Selama jeda, stream diam kecuali untuk SSE `ping` keepalive standar yang dipancarkan kira-kira setiap 30 detik; panggilan advisor pendek mungkin tidak menunjukkan ping.

Ketika advisor selesai, `advisor_tool_result` tiba sepenuhnya dalam satu peristiwa `content_block_start` (tidak ada delta). Output executor kemudian melanjutkan streaming.

Peristiwa `message_delta` mengikuti dengan array `usage.iterations` yang diperbarui mencerminkan hitungan token advisor.

## Penggunaan dan penagihan

Panggilan advisor berjalan sebagai sub-inferensi terpisah yang ditagih dengan tarif model advisor. Penggunaan dilaporkan dalam array `usage.iterations[]`:

```json
{
  "usage": {
    "input_tokens": 412,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 0,
    "output_tokens": 531,
    "iterations": [
      {
        "type": "message",
        "input_tokens": 412,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0,
        "output_tokens": 89
      },
      {
        "type": "advisor_message",
        "model": "claude-opus-4-7",
        "input_tokens": 823,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0,
        "output_tokens": 1612
      },
      {
        "type": "message",
        "input_tokens": 1348,
        "cache_read_input_tokens": 412,
        "cache_creation_input_tokens": 0,
        "output_tokens": 442
      }
    ]
  }
}
```

Bidang `usage` tingkat atas mencerminkan token executor saja. Token advisor tidak digabungkan ke dalam total tingkat atas karena ditagih dengan tarif yang berbeda. Iterasi dengan `type: "advisor_message"` ditagih dengan tarif model advisor; iterasi dengan `type: "message"` ditagih dengan tarif model executor.

Aturan agregasi berbeda menurut bidang. `output_tokens` tingkat atas adalah jumlah semua iterasi executor. `input_tokens` dan `cache_read_input_tokens` tingkat atas mencerminkan iterasi executor pertama saja; input iterasi executor berikutnya tidak dijumlahkan ulang karena mencakup token output sebelumnya. Gunakan `usage.iterations` untuk rincian per-iterasi lengkap saat membangun logika pelacakan biaya.

Output advisor biasanya 400 hingga 700 token teks, atau 1.400 hingga 1.800 token total termasuk thinking. Penghematan biaya berasal dari advisor tidak menghasilkan output final lengkap Anda; executor melakukan itu dengan tarif yang lebih rendah.

`max_tokens` tingkat atas hanya berlaku untuk output executor. Ini tidak membatasi token sub-inferensi advisor. Token advisor juga tidak ditarik dari anggaran tugas apa pun yang diterapkan pada executor.

## Advisor prompt caching

Ada dua lapisan caching independen.

### Caching sisi executor

Blok `advisor_tool_result` dapat di-cache seperti blok konten lainnya. Breakpoint `cache_control` yang ditempatkan setelahnya pada giliran berikutnya akan mencapai. Prompt executor selalu berisi saran plaintext terlepas dari apakah klien Anda menerima `text` atau `encrypted_content`, jadi perilaku caching identik untuk kedua varian hasil.

### Caching sisi advisor

Atur `caching` pada definisi alat untuk mengaktifkan prompt caching untuk transkrip advisor sendiri di seluruh panggilan dalam percakapan yang sama:

```python
tools = [
    {
        "type": "advisor_20260301",
        "name": "advisor",
        "model": "claude-opus-4-7",
        "caching": {"type": "ephemeral", "ttl": "5m"},
    }
]
```

Prompt advisor pada panggilan ke-N adalah prompt panggilan ke-(N-1) dengan satu segmen lagi ditambahkan, jadi prefiks stabil di seluruh panggilan. Dengan `caching` diaktifkan, setiap panggilan advisor menulis entri cache; panggilan berikutnya membaca hingga titik itu dan hanya membayar delta. Anda akan melihat `cache_read_input_tokens` menjadi nonzero pada iterasi `advisor_message` kedua dan lebih baru.

**Kapan mengaktifkannya:** Penulisan cache biaya lebih dari pembacaan yang disimpan ketika advisor dipanggil dua kali atau lebih sedikit per percakapan. Caching impas pada kira-kira tiga panggilan advisor dan meningkat dari sana. Aktifkan untuk loop agen panjang; biarkan mati untuk tugas pendek.

**Pertahankan konsistensi:** Atur `caching` sekali dan biarkan untuk seluruh percakapan. Mengalihkannya mati dan menyala di tengah percakapan menyebabkan cache miss.

<Warning>
  [`clear_thinking`](/docs/id/build-with-claude/context-editing) dengan nilai `keep`
  selain `"all"` menggeser transkrip yang dikutip advisor setiap giliran,
  menyebabkan cache miss sisi advisor. Ini adalah degradasi biaya saja; kualitas saran tidak terpengaruh. Ketika extended thinking diaktifkan tanpa konfigurasi `clear_thinking` eksplisit, API default ke
  `keep: {type: "thinking_turns", value: 1}`, yang memicu perilaku ini.
  Atur `keep: "all"` untuk mempertahankan stabilitas cache advisor.
</Warning>

## Menggabungkan dengan alat lain

Alat advisor terdiri dengan alat server-side dan client-side lainnya. Tambahkan semuanya ke array `tools` yang sama:

```python
tools = [
    {
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": 5,
    },
    {
        "type": "advisor_20260301",
        "name": "advisor",
        "model": "claude-opus-4-7",
    },
    {
        "name": "run_bash",
        "description": "Run a bash command",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
        },
    },
]
```

Executor dapat mencari web, memanggil advisor, dan menggunakan alat kustom Anda dalam giliran yang sama. Rencana advisor dapat menginformasikan alat mana yang akan digunakan executor selanjutnya.

| Fitur                                                          | Interaksi                                                                                                                                                                                                                                                                        |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Batch processing](/docs/id/build-with-claude/batch-processing)         | Didukung. `usage.iterations` dilaporkan per item.                                                                                                                                                                                                                                |
| [Token counting](/docs/id/build-with-claude/token-counting)      | Mengembalikan token input iterasi pertama executor saja. Untuk perkiraan advisor kasar, panggil `count_tokens` dengan `model` diatur ke model advisor dan pesan yang sama.                                                                                                           |
| [Context editing](/docs/id/build-with-claude/context-editing) | `clear_tool_uses` belum sepenuhnya kompatibel dengan blok alat advisor; dukungan penuh direncanakan untuk rilis lanjutan. Dengan `clear_thinking`, lihat peringatan caching di atas.                                                                                                    |
| `pause_turn`                                                     | Panggilan advisor yang menggantung mengakhiri respons dengan `stop_reason: "pause_turn"` dan blok `server_tool_use` sebagai blok konten terakhir. Advisor mengeksekusi pada resume. Lihat [Server tools](/docs/id/agents-and-tools/tool-use/server-tools#the-server-side-loop-and-pause-turn). |

## Praktik terbaik

### Prompting untuk tugas coding dan agent

Alat advisor dilengkapi dengan deskripsi bawaan yang mendorong executor untuk memanggilnya di dekat awal tugas kompleks dan ketika mengalami kesulitan. Untuk tugas penelitian, biasanya tidak diperlukan prompting tambahan.

Pada tugas coding dan agent, advisor menghasilkan kecerdasan yang lebih tinggi dengan biaya yang sama ketika mengurangi total panggilan alat dan panjang percakapan. Dua waktu mendorong peningkatan ini:

1. Panggilan advisor pertama awal, setelah beberapa pembacaan eksplorasi ada dalam transkrip.
2. Untuk tugas yang sulit, panggilan advisor akhir setelah penulisan file dan output tes ada dalam transkrip.

Jika agen Anda mengekspos alat seperti planner lainnya (misalnya, alat daftar todo), minta model untuk memanggil advisor sebelum alat tersebut sehingga rencana advisor mengalir ke dalamnya. Prompt sistem yang disarankan di bawah memperkuat pola panggilan awal; tambahkan kalimat corong Anda sendiri yang menunjuk ke alat planner mana pun yang diekspos agen Anda.

#### Prompt sistem yang disarankan untuk tugas coding

Untuk tugas coding di mana Anda menginginkan waktu advisor yang konsisten dan sekitar dua hingga tiga panggilan per tugas, tambahkan blok berikut ke prompt sistem executor Anda sebelum kalimat lain yang menyebutkan advisor. Pada evaluasi coding internal pola ini menghasilkan kecerdasan tertinggi dengan biaya mendekati Sonnet.

Panduan waktu:

```text
You have access to an `advisor` tool backed by a stronger reviewer model. It takes NO parameters — when you call advisor(), your entire conversation history is automatically forwarded. They see the task, every tool call you've made, every result you've seen.

Call advisor BEFORE substantive work — before writing, before committing to an interpretation, before building on an assumption. If the task requires orientation first (finding files, fetching a source, seeing what's there), do that, then call advisor. Orientation is not substantive work. Writing, editing, and declaring an answer are.

Also call advisor:
- When you believe the task is complete. BEFORE this call, make your deliverable durable: write the file, save the result, commit the change. The advisor call takes time; if the session ends during it, a durable result persists and an unwritten one doesn't.
- When stuck — errors recurring, approach not converging, results that don't fit.
- When considering a change of approach.

On tasks longer than a few steps, call advisor at least once before committing to an approach and once before declaring done. On short reactive tasks where the next action is dictated by tool output you just read, you don't need to keep calling — the advisor adds most of its value on the first call, before the approach crystallizes.
```

Bagaimana executor harus memperlakukan saran (tempatkan langsung setelah blok waktu):

```text
Give the advice serious weight. If you follow a step and it fails empirically, or you have primary-source evidence that contradicts a specific claim (the file says X, the paper states Y), adapt. A passing self-test is not evidence the advice is wrong — it's evidence your test doesn't check what the advice is checking.

If you've already retrieved data pointing one way and the advisor points another: don't silently switch. Surface the conflict in one more advisor call — "I found X, you suggest Y, which constraint breaks the tie?" The advisor saw your evidence but may have underweighted it; a reconcile call is cheaper than committing to the wrong branch.
```

#### Memangkas panjang output advisor

Output advisor adalah pendorong biaya terbesar advisor. Untuk mengurangi biaya itu, tambahkan instruksi conciseness tunggal ke prompt sistem sebelum kalimat lain yang menyebutkan advisor. Dalam pengujian internal, baris berikut mengurangi total token output advisor kira-kira 35 hingga 45 persen tanpa mengubah frekuensi panggilan:

```text
The advisor should respond in under 100 words and use enumerated steps, not explanations.
```

Pasangkan ini dengan blok waktu di atas untuk tradeoff biaya-versus-kualitas terkuat.

### Memasangkan dengan pengaturan effort

Untuk tugas coding, memasangkan executor Sonnet pada [effort](/docs/id/build-with-claude/effort) medium dengan advisor Opus mencapai kecerdasan yang sebanding dengan Sonnet pada effort default, dengan biaya lebih rendah. Untuk kecerdasan maksimum, pertahankan executor pada effort default.

### Kontrol biaya

- Untuk anggaran tingkat percakapan, hitung panggilan advisor client-side. Ketika Anda mencapai batas Anda, hapus alat advisor dari `tools` **dan** lepas semua blok `advisor_tool_result` dari riwayat pesan Anda untuk menghindari `400 invalid_request_error`.
- Aktifkan `caching` hanya untuk percakapan di mana Anda mengharapkan tiga atau lebih panggilan advisor.

## Keterbatasan

- **Output advisor tidak streaming.** Harapkan jeda dalam stream saat sub-inferensi berjalan.
- **Tidak ada batas tingkat percakapan bawaan pada panggilan advisor.** Lacak dan batasi secara client-side.
- **`max_tokens` hanya berlaku untuk output executor.** Ini tidak membatasi token advisor.
- **Anthropic Priority Tier** dihormati per model. Priority Tier pada model executor tidak meluas ke advisor; Anda memerlukan Priority Tier pada model advisor secara khusus.