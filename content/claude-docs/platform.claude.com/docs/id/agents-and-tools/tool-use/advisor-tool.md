---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool
fetched_at: 2026-06-10T03:15:54.339721Z
sha256: 9462498f6a2bbc61a565e8c0236528d25e124a64fa6e0492ec89c34b6e6223e6
---

# Alat advisor

Pasangkan model eksekutor yang lebih cepat dengan model advisor berkecerdasan lebih tinggi yang memberikan panduan strategis di tengah proses generasi.

---

Alat advisor memungkinkan **model eksekutor** yang lebih cepat dan berbiaya lebih rendah untuk berkonsultasi dengan **model advisor** berkecerdasan lebih tinggi di tengah proses generasi untuk mendapatkan panduan strategis. Advisor membaca seluruh percakapan, menghasilkan rencana atau koreksi arah (biasanya 400 hingga 700 token teks, 1.400 hingga 1.800 token total termasuk thinking), dan eksekutor melanjutkan tugasnya.

Pola ini cocok untuk beban kerja agentik jangka panjang (agen pengkodean, penggunaan komputer, pipeline riset multi-langkah) di mana sebagian besar giliran bersifat mekanis tetapi memiliki rencana yang sangat baik sangatlah krusial. Anda mendapatkan kualitas yang mendekati advisor-solo sementara sebagian besar generasi token terjadi pada tarif model eksekutor.

<Note>
  Alat advisor masih dalam versi beta. Sertakan header beta `advisor-tool-2026-03-01`
  dalam permintaan Anda. Untuk meminta akses atau memberikan masukan, hubungi tim
  akun Anthropic Anda.
</Note>

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

## Kapan menggunakannya \{#when-to-use-it}

Benchmark awal menunjukkan peningkatan yang berarti untuk konfigurasi berikut:

- **Anda saat ini menggunakan Sonnet untuk tugas kompleks:** Tambahkan Opus sebagai advisor untuk peningkatan kualitas dengan total biaya yang serupa atau lebih rendah.
- **Anda saat ini menggunakan Haiku dan menginginkan peningkatan kecerdasan:** Tambahkan Opus sebagai advisor. Perkirakan biaya lebih tinggi daripada Haiku saja, tetapi lebih rendah daripada mengganti eksekutor ke model yang lebih besar.

Hasilnya bergantung pada tugas. Evaluasi pada beban kerja Anda sendiri.

Advisor kurang cocok untuk tanya jawab satu giliran (tidak ada yang perlu direncanakan), pemilih model pass-through murni di mana pengguna Anda sudah memilih sendiri trade-off biaya dan kualitas mereka, atau beban kerja di mana setiap giliran benar-benar membutuhkan kemampuan penuh model advisor.

## Kompatibilitas model \{#model-compatibility}

Model eksekutor (field `model` tingkat atas) dan model advisor (field `model` di dalam definisi alat) harus membentuk pasangan yang valid. Advisor harus setidaknya sama mampunya dengan eksekutor.

| Model eksekutor                                               | Model advisor                                                                                          |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Claude Haiku 4.5 (claude-haiku-4-5-20251001) | Claude Opus 4.8 (claude-opus-4-8), Claude Opus 4.7 (claude-opus-4-7) |
| Claude Sonnet 4.6 (claude-sonnet-4-6)        | Claude Opus 4.8 (claude-opus-4-8), Claude Opus 4.7 (claude-opus-4-7) |
| Claude Opus 4.6 (claude-opus-4-6)            | Claude Opus 4.8 (claude-opus-4-8), Claude Opus 4.7 (claude-opus-4-7) |
| Claude Opus 4.7 (claude-opus-4-7)            | Claude Opus 4.8 (claude-opus-4-8), Claude Opus 4.7 (claude-opus-4-7) |
| Claude Opus 4.8 (claude-opus-4-8)            | Claude Opus 4.8 (claude-opus-4-8)                                                     |
| Claude Fable 5 (`claude-fable-5`)                             | Claude Fable 5 (`claude-fable-5`)                                                                       |
| Claude Mythos 5 (`claude-mythos-5`)                           | Claude Mythos 5 (`claude-mythos-5`)                                                                     |

Jika Anda meminta pasangan yang tidak valid, API mengembalikan `400 invalid_request_error` yang menyebutkan kombinasi yang tidak didukung.

## Ketersediaan platform \{#platform-availability}

Alat advisor tersedia dalam versi beta di Claude API dan di [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws). Saat ini belum tersedia di AWS Bedrock, Vertex AI, atau Microsoft Foundry.

## Mulai cepat \{#quick-start}

<CodeGroup>
```bash cURL
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
                "model": "claude-opus-4-8"
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
    model: claude-opus-4-8
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
            "model": "claude-opus-4-8",
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
        model: "claude-opus-4-8"
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
            Model = Messages::Model.ClaudeOpus4_8
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
				Model: anthropic.ModelClaudeOpus4_8,
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

$client = new Client();

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
            'model' => 'claude-opus-4-8',
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
      model: "claude-opus-4-8"
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

## Cara kerjanya \{#how-it-works}

Ketika Anda menambahkan alat advisor ke array `tools` Anda, model eksekutor memutuskan kapan memanggilnya, sama seperti alat lainnya. Ketika eksekutor memanggil advisor:

1. Eksekutor mengeluarkan blok `server_tool_use` dengan `name: "advisor"` dan `input` kosong. Eksekutor memberi sinyal waktu; server menyediakan konteks.
2. Anthropic menjalankan proses inferensi terpisah pada model advisor di sisi server, meneruskan transkrip lengkap eksekutor. Advisor melihat prompt sistem, semua definisi alat, semua giliran sebelumnya, dan semua hasil alat sebelumnya.
3. Respons advisor dikembalikan ke eksekutor sebagai blok `advisor_tool_result`.
4. Eksekutor melanjutkan generasi, dengan mempertimbangkan saran tersebut.

Semua ini terjadi di dalam satu permintaan `/v1/messages`. Tidak ada round trip tambahan di sisi Anda.

Advisor itu sendiri berjalan tanpa alat dan tanpa manajemen konteks. Blok thinking-nya dibuang sebelum hasil dikembalikan; hanya teks saran yang sampai ke eksekutor.

## Parameter alat \{#tool-parameters}

| Parameter               | Tipe           | Default      | Deskripsi                                                                                                                                          |
| ----------------------- | -------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                  | string         | _wajib_      | Harus berupa `"advisor_20260301"`.                                                                                                                 |
| `name`                  | string         | _wajib_      | Harus berupa `"advisor"`.                                                                                                                          |
| `model`                 | string         | _wajib_      | ID model advisor, seperti `"claude-opus-4-8"`. Ditagih dengan tarif model ini untuk sub-inferensi.                                                 |
| `max_uses`              | integer        | tak terbatas | Jumlah maksimum panggilan advisor yang diizinkan dalam satu permintaan. Setelah eksekutor mencapai batas ini, panggilan advisor selanjutnya mengembalikan `advisor_tool_result_error` dengan `error_code: "max_uses_exceeded"` dan eksekutor melanjutkan tanpa saran lebih lanjut. Ini adalah batas per-permintaan, bukan batas per-percakapan; lihat [Kontrol biaya](#kontrol-biaya) untuk batas tingkat percakapan. |
| `max_tokens`            | integer        | batas output model advisor | Membatasi total output advisor (thinking plus teks) per panggilan. Minimum 1024. Lihat [Membatasi output advisor](#membatasi-output-advisor). |
| `caching`               | object \| null | `null` (nonaktif) | Mengaktifkan caching prompt untuk transkrip advisor sendiri di seluruh panggilan dalam satu percakapan. Lihat [Caching prompt advisor](#caching-prompt-advisor). |

Objek `caching` memiliki bentuk `{"type": "ephemeral", "ttl": "5m" | "1h"}`. Tidak seperti `cache_control` pada blok konten, ini bukan penanda breakpoint; ini adalah sakelar on/off. Server yang memutuskan di mana batas cache ditempatkan.

Alat advisor juga menerima properti generik yang tersedia pada definisi alat apa pun: `cache_control`, `allowed_callers`, `defer_loading`, dan `strict` (dibahas dalam [structured outputs](/docs/id/build-with-claude/structured-outputs)). Lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference#tool-definition-properties) untuk semantiknya.

## Struktur respons \{#response-structure}

### Panggilan advisor yang berhasil \{#successful-advisor-call}

Ketika advisor dipanggil, blok `server_tool_use` diikuti oleh blok `advisor_tool_result` dalam konten asisten:

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

`server_tool_use.input` selalu kosong. Server membangun tampilan advisor dari transkrip lengkap secara otomatis; tidak ada yang dimasukkan eksekutor ke dalam `input` yang sampai ke advisor.

### Varian hasil \{#result-variants}

Field `advisor_tool_result.content` adalah discriminated union. Untuk panggilan yang berhasil, variannya bergantung pada model advisor:

| Varian                    | Field                             | Dikembalikan ketika                                                 |
| ------------------------- | --------------------------------- | ------------------------------------------------------------------- |
| `advisor_result`          | `text`, `stop_reason`             | Model advisor mengembalikan plaintext (misalnya, Claude Opus 4.8).  |
| `advisor_redacted_result` | `encrypted_content`, `stop_reason` | Model advisor mengembalikan output terenkripsi.                     |

Field `stop_reason` ada pada kedua varian hasil setiap kali [`max_tokens`](#membatasi-output-advisor) diatur pada definisi alat, membawa stop reason dari sub-panggilan advisor (biasanya `"end_turn"`; `"max_tokens"` ketika batas tercapai), sesuai dengan [`stop_reason`](/docs/id/build-with-claude/handling-stop-reasons) tingkat atas Messages API. Field ini tidak ada ketika `max_tokens` tidak diatur.

Dengan `advisor_result`, field `text` berisi saran yang dapat dibaca manusia. Dengan `advisor_redacted_result`, field `encrypted_content` berisi blob opaque yang tidak dapat Anda baca; pada giliran berikutnya, server mendekripsinya dan merender plaintext ke dalam prompt eksekutor.

Dalam kedua kasus, kirim kembali konten secara verbatim pada giliran berikutnya. Jika Anda mengganti model advisor di tengah percakapan, lakukan percabangan pada `content.type` untuk menangani kedua bentuk tersebut.

### Hasil error \{#error-results}

Jika panggilan advisor gagal, hasilnya membawa error:

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

Eksekutor melihat error tersebut dan melanjutkan tanpa saran lebih lanjut. Permintaan itu sendiri tidak gagal.

| `error_code`              | Arti                                                                                                        |
| ------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `max_uses_exceeded`       | Permintaan mencapai batas `max_uses` yang diatur pada definisi alat. Panggilan advisor selanjutnya dalam permintaan yang sama mengembalikan error ini. |
| `too_many_requests`       | Sub-inferensi advisor terkena batas laju.                                                                   |
| `overloaded`              | Sub-inferensi advisor mencapai batas kapasitas.                                                             |
| `prompt_too_long`         | Transkrip melebihi jendela konteks model advisor.                                                           |
| `execution_time_exceeded` | Sub-inferensi advisor mengalami timeout.                                                                    |
| `unavailable`             | Kegagalan advisor lainnya.                                                                                   |

Batas laju advisor diambil dari bucket per-model yang sama dengan panggilan langsung ke model advisor. Batas laju pada advisor muncul sebagai `too_many_requests` di dalam hasil alat; batas laju pada eksekutor menggagalkan seluruh permintaan dengan HTTP 429.

## Percakapan multi-giliran \{#multi-turn-conversations}

Kirim kembali seluruh konten asisten, termasuk blok `advisor_tool_result`, ke API pada giliran berikutnya:

```python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "type": "advisor_20260301",
        "name": "advisor",
        "model": "claude-opus-4-8",
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

# Tambahkan seluruh konten respons, termasuk blok advisor_tool_result apa pun
messages.append({"role": "assistant", "content": response.content})

# Lanjutkan percakapan
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
  panggilan advisor di seluruh percakapan, hitung di sisi klien. Ketika Anda
  mencapai batas maksimum Anda, hapus alat advisor dari array `tools` Anda **dan**
  hapus semua blok `advisor_tool_result` dari riwayat pesan Anda untuk menghindari
  `400 invalid_request_error`.
</Note>

## Streaming \{#streaming}

Sub-inferensi advisor tidak melakukan streaming. Stream eksekutor berhenti sementara advisor berjalan, kemudian hasil lengkap tiba dalam satu event.

Blok `server_tool_use` dengan `name: "advisor"` menandakan bahwa panggilan advisor sedang dimulai. Jeda dimulai ketika blok tersebut ditutup (`content_block_stop`). Selama jeda, stream diam kecuali untuk keepalive `ping` SSE standar yang dikeluarkan kira-kira setiap 30 detik; panggilan advisor yang singkat mungkin tidak menampilkan ping.

Ketika advisor selesai, `advisor_tool_result` tiba dalam bentuk lengkap dalam satu event `content_block_start` (tanpa delta). Output eksekutor kemudian melanjutkan streaming.

Event `message_delta` menyusul dengan array `usage.iterations` yang diperbarui yang mencerminkan jumlah token advisor.

## Penggunaan dan penagihan \{#usage-and-billing}

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
        "model": "claude-opus-4-8",
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

Field `usage` tingkat atas hanya mencerminkan token eksekutor. Token advisor tidak digabungkan ke dalam total tingkat atas karena ditagih dengan tarif yang berbeda. Iterasi dengan `type: "advisor_message"` ditagih dengan tarif model advisor; iterasi dengan `type: "message"` ditagih dengan tarif model eksekutor.

Aturan agregasi berbeda per field. `output_tokens` tingkat atas adalah jumlah dari semua iterasi eksekutor. `input_tokens` dan `cache_read_input_tokens` tingkat atas hanya mencerminkan iterasi eksekutor pertama; input iterasi eksekutor berikutnya tidak dijumlahkan ulang karena sudah mencakup token output sebelumnya. Gunakan `usage.iterations` untuk rincian lengkap per-iterasi saat membangun logika pelacakan biaya.

Output advisor biasanya 400 hingga 700 token teks, atau 1.400 hingga 1.800 token total termasuk thinking. Penghematan biaya berasal dari advisor yang tidak menghasilkan output akhir lengkap Anda; eksekutor yang melakukannya dengan tarif yang lebih rendah.

`max_tokens` tingkat atas hanya berlaku untuk output eksekutor. Ini tidak membatasi token sub-inferensi advisor. Untuk membatasi output advisor secara langsung, atur [`max_tokens` pada definisi alat](#membatasi-output-advisor). Token advisor juga tidak diambil dari anggaran tugas apa pun yang diterapkan pada eksekutor.

## Caching prompt advisor \{#advisor-prompt-caching}

Ada dua lapisan caching yang independen.

### Caching sisi eksekutor \{#executor-side-caching}

Blok `advisor_tool_result` dapat di-cache seperti blok konten lainnya. Breakpoint `cache_control` yang ditempatkan setelahnya pada giliran berikutnya akan mengenai cache. Prompt eksekutor selalu berisi saran plaintext terlepas dari apakah klien Anda menerima `text` atau `encrypted_content`, sehingga perilaku caching identik untuk kedua varian hasil.

### Caching sisi advisor \{#advisor-side-caching}

Atur `caching` pada definisi alat untuk mengaktifkan caching prompt untuk transkrip advisor sendiri di seluruh panggilan dalam percakapan yang sama:

```python
tools = [
    {
        "type": "advisor_20260301",
        "name": "advisor",
        "model": "claude-opus-4-8",
        "caching": {"type": "ephemeral", "ttl": "5m"},
    }
]
```

Prompt advisor pada panggilan ke-N adalah prompt panggilan ke-(N-1) dengan satu segmen lagi yang ditambahkan, sehingga prefiksnya stabil di seluruh panggilan. Dengan `caching` diaktifkan, setiap panggilan advisor menulis entri cache; panggilan berikutnya membaca hingga titik tersebut dan hanya membayar untuk delta-nya. Anda akan melihat `cache_read_input_tokens` menjadi bukan nol pada iterasi `advisor_message` kedua dan seterusnya.

**Kapan mengaktifkannya:** Penulisan cache lebih mahal daripada penghematan dari pembacaan ketika advisor dipanggil dua kali atau kurang per percakapan. Caching mencapai titik impas pada kira-kira tiga panggilan advisor dan semakin menguntungkan setelahnya. Aktifkan untuk loop agen yang panjang; biarkan nonaktif untuk tugas singkat.

**Jaga konsistensinya:** Atur `caching` sekali dan biarkan untuk seluruh percakapan. Mengaktifkan dan menonaktifkannya di tengah percakapan menyebabkan cache miss.

<Warning>
  [`clear_thinking`](/docs/id/build-with-claude/context-editing) dengan nilai `keep`
  selain `"all"` menggeser transkrip yang dikutip advisor setiap giliran,
  menyebabkan cache miss di sisi advisor. Ini hanya degradasi biaya; kualitas
  saran tidak terpengaruh. Ketika pemikiran diperpanjang diaktifkan tanpa
  konfigurasi `clear_thinking` eksplisit, API secara default menggunakan
  `keep: {type: "thinking_turns", value: 1}`, yang memicu perilaku ini
  (default pada model Opus/Sonnet sebelumnya dan semua model Haiku; pada Opus
  4.5+ dan Sonnet 4.6+ default-nya adalah mempertahankan semua giliran). Atur
  `keep: "all"` untuk menjaga stabilitas cache advisor.
</Warning>

## Menggabungkan dengan alat lain \{#combining-with-other-tools}

Alat advisor dapat dikombinasikan dengan alat sisi server dan sisi klien lainnya. Tambahkan semuanya ke array `tools` yang sama:

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
        "model": "claude-opus-4-8",
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

Eksekutor dapat mencari web, memanggil advisor, dan menggunakan alat kustom Anda dalam giliran yang sama. Rencana advisor dapat menginformasikan alat mana yang akan digunakan eksekutor selanjutnya.

| Fitur                                                            | Interaksi                                                                                                                                                                                                                                                                          |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Pemrosesan batch](/docs/id/build-with-claude/batch-processing)  | Didukung. `usage.iterations` dilaporkan per item.                                                                                                                                                                                                                                 |
| [Penghitungan token](/docs/id/build-with-claude/token-counting)  | Mengembalikan token input iterasi pertama eksekutor saja. Untuk estimasi kasar advisor, panggil `count_tokens` dengan `model` diatur ke model advisor dan pesan yang sama.                                                                                                       |
| [Pengeditan konteks](/docs/id/build-with-claude/context-editing) | `clear_tool_uses` tidak sepenuhnya kompatibel dengan blok alat advisor. Dengan `clear_thinking`, lihat peringatan caching sebelumnya.                                                                                                                                             |
| `pause_turn`                                                     | Panggilan advisor yang menggantung mengakhiri respons dengan `stop_reason: "pause_turn"` dan blok `server_tool_use` sebagai blok konten terakhir. Advisor dieksekusi saat dilanjutkan. Lihat [Alat server](/docs/id/agents-and-tools/tool-use/server-tools#the-server-side-loop-and-pause-turn). |

## Praktik terbaik \{#best-practices}

### Prompting untuk tugas pengkodean dan agen \{#prompting-for-coding-and-agent-tasks}

Alat advisor dilengkapi dengan deskripsi bawaan yang mendorong eksekutor untuk memanggilnya di awal tugas kompleks dan ketika menemui kesulitan. Untuk tugas riset, biasanya tidak diperlukan prompting tambahan.

Pada tugas pengkodean dan agen, advisor menghasilkan kecerdasan yang lebih tinggi dengan biaya serupa ketika mengurangi total panggilan alat dan panjang percakapan. Dua waktu pemanggilan mendorong peningkatan ini:

1. Panggilan advisor pertama yang lebih awal, setelah beberapa pembacaan eksploratif ada dalam transkrip.
2. Untuk tugas yang sulit, panggilan advisor terakhir setelah penulisan file dan output pengujian ada dalam transkrip.

Jika agen Anda mengekspos alat mirip perencana lainnya (misalnya, alat daftar todo), arahkan model untuk memanggil advisor sebelum alat-alat tersebut sehingga rencana advisor mengalir ke dalamnya. Prompt sistem yang disarankan di bawah ini memperkuat pola panggilan awal; tambahkan kalimat pengarah Anda sendiri yang menunjuk ke alat perencana apa pun yang diekspos agen Anda.

#### Prompt sistem yang disarankan untuk tugas pengkodean \{#suggested-system-prompt-for-coding-tasks}

Tanpa pengarahan prompt sistem, eksekutor cenderung kurang memanggil advisor di beberapa domain — khususnya tugas pengkodean. Untuk tugas pengkodean di mana Anda menginginkan waktu pemanggilan advisor yang konsisten dan sekitar dua hingga tiga panggilan per tugas, tambahkan blok berikut di awal prompt sistem eksekutor Anda sebelum kalimat lain yang menyebutkan advisor.

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

Bagaimana eksekutor harus memperlakukan saran (tempatkan langsung setelah blok waktu):

```text
Give the advice serious weight. If you follow a step and it fails empirically, or you have primary-source evidence that contradicts a specific claim (the file says X, the paper states Y), adapt. A passing self-test is not evidence the advice is wrong — it's evidence your test doesn't check what the advice is checking.

If you've already retrieved data pointing one way and the advisor points another: don't silently switch. Surface the conflict in one more advisor call — "I found X, you suggest Y, which constraint breaks the tie?" The advisor saw your evidence but may have underweighted it; a reconcile call is cheaper than committing to the wrong branch.
```

#### Memangkas panjang output advisor \{#trimming-advisor-output-length}

Output advisor adalah pendorong biaya terbesar advisor, dan `max_tokens` tingkat atas tidak membatasinya. Advisor melihat prompt sistem Anda dan pesan pengguna Anda sebagai konteks yang dikutip tentang tugas eksekutor, sehingga instruksi yang ditujukan langsung kepada advisor diikuti jauh lebih andal daripada deskripsi orang ketiga. Penempatan paling efektif yang diuji Anthropic adalah satu baris dalam pesan pengguna:

```text
(Advisor: please keep your guidance under 80 words — I need a focused starting point, not a comprehensive plan.)
```

Baris ini dapat ditambahkan sebagai prefiks secara terprogram oleh framework agen Anda sebelum mengirim permintaan. Batas ini adalah batasan lunak; advisor kadang-kadang akan melebihinya, jadi minta kira-kira 80 persen dari batas maksimum Anda yang sebenarnya.

<Note>
  Dalam pengujian Anthropic, baris ini juga meningkatkan seberapa sering eksekutor
  berkonsultasi dengan advisor, tetapi efek bersihnya tetap total biaya yang lebih rendah
  (lebih banyak konsultasi, masing-masing lebih singkat).
</Note>

Pasangkan pendekatan ini dengan panduan waktu di [Prompt sistem yang disarankan untuk tugas pengkodean](#prompt-sistem-yang-disarankan-untuk-tugas-pengkodean) untuk trade-off biaya-versus-kualitas terkuat. Untuk batas keras alih-alih permintaan lunak, lihat [Membatasi output advisor](#membatasi-output-advisor).

### Membatasi output advisor \{#capping-advisor-output}

Atur `max_tokens` pada definisi alat untuk membatasi total output advisor (thinking plus teks) per panggilan:

```python
tools = [
    {
        "type": "advisor_20260301",
        "name": "advisor",
        "model": "claude-opus-4-8",
        "max_tokens": 2048,
    }
]
```

Nilai minimum adalah 1024. Mengatur `max_tokens` di atas batas output model advisor sendiri mengembalikan error 400. Batas ini berlaku untuk setiap panggilan advisor secara independen dan tidak dibagi di seluruh panggilan dalam permintaan yang sama.

Ini bukan sekadar pemotongan keras. Server juga meneruskan anggaran token yang tersisa kepada advisor, sehingga advisor membentuk responsnya agar sesuai.

**Titik awal yang direkomendasikan:** `max_tokens: 2048`. Dalam pengujian Anthropic pada benchmark penalaran sulit (n=40 per konfigurasi), ini mengurangi rata-rata output advisor sekitar 7x dibandingkan dengan membiarkan batas tidak diatur, dengan pemotongan mendekati nol dan tanpa degradasi kualitas yang terdeteksi. Nilai minimum 1024 mengurangi output sekitar 10x tetapi memotong sekitar 10 persen panggilan. Perbedaan akurasi di semua konfigurasi berada dalam rentang noise pada ukuran sampel ini; validasi pada beban kerja Anda sendiri.

| `max_tokens` | Rata-rata token output advisor | Panggilan terpotong |
| ------------ | ------------------------------ | ------------------- |
| tidak diatur | ~4.200 hingga 5.900            | n/a                 |
| 2048         | ~630 hingga 840                | ~0%                 |
| 1024         | ~370 hingga 480                | ~10%                |

Tugas penalaran sulit memunculkan output advisor yang jauh lebih panjang daripada [1.400 hingga 1.800 token tipikal](#penggunaan-dan-penagihan) yang dikutip sebelumnya untuk beban kerja yang lebih ringan. Gunakan tabel ini untuk mengukur rasio penghematan, bukan sebagai baseline universal untuk output advisor.

Ketika advisor mencapai batas, blok hasil membawa `stop_reason: "max_tokens"`. Gunakan ini untuk mendeteksi saran yang terpotong dan memutuskan apakah akan menaikkan batas atau membiarkan eksekutor melanjutkan dengan panduan parsial. Field ini tidak ada ketika `max_tokens` tidak diatur.

```json
{
  "type": "advisor_tool_result",
  "tool_use_id": "srvtoolu_abc123",
  "content": {
    "type": "advisor_result",
    "text": "Use a channel-based coordination pattern. The tricky part is",
    "stop_reason": "max_tokens"
  }
}
```

Periksa `output_tokens` pada entri `advisor_message` yang sesuai di `usage.iterations` untuk melihat seberapa dekat setiap panggilan dengan batasnya.

Dibandingkan dengan [pendekatan berbasis prompt](#memangkas-panjang-output-advisor), `max_tokens` adalah batas keras alih-alih permintaan lunak. Gunakan `max_tokens` ketika Anda membutuhkan batas yang dijamin untuk biaya atau latensi; gunakan pendekatan berbasis prompt (atau keduanya bersama-sama) ketika Anda ingin mengarahkan ke keringkasan tanpa risiko terpotong di tengah pemikiran.

### Memasangkan dengan pengaturan effort \{#pairing-with-effort-settings}

Untuk tugas pengkodean, memasangkan eksekutor Sonnet pada [effort](/docs/id/build-with-claude/effort) medium dengan advisor Opus mencapai kecerdasan yang sebanding dengan Sonnet pada effort default, dengan biaya lebih rendah. Untuk kecerdasan maksimum, pertahankan eksekutor pada effort default.

### Kontrol biaya \{#cost-control}

- Untuk anggaran tingkat percakapan, hitung panggilan advisor di sisi klien. Ketika Anda mencapai batas Anda, hapus alat advisor dari `tools` **dan** hapus semua blok `advisor_tool_result` dari riwayat pesan Anda untuk menghindari `400 invalid_request_error`.
- Aktifkan `caching` hanya untuk percakapan di mana Anda mengharapkan tiga atau lebih panggilan advisor.

## Keterbatasan \{#limitations}

- **Output advisor tidak melakukan streaming.** Perkirakan jeda dalam stream saat sub-inferensi berjalan.
- **Tidak ada batas tingkat percakapan bawaan pada panggilan advisor.** Lacak dan batasi di sisi klien.
- **`max_tokens` tingkat atas hanya berlaku untuk output eksekutor.** Ini tidak membatasi token advisor. Untuk membatasi output advisor, atur [`max_tokens` pada definisi alat](#membatasi-output-advisor).
- **[Priority Tier](/docs/id/api/service-tiers)** dihormati untuk setiap model. Priority Tier pada model eksekutor tidak meluas ke advisor; Anda memerlukan Priority Tier pada model advisor secara spesifik.