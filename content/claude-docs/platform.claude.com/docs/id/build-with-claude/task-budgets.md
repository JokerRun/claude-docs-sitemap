---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/task-budgets
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 7d3d40962c9aa67c21cba9bafd6bec1780fc04e01e55fdc845ae0ac0368783d4
---

# Anggaran tugas

Berikan Claude anggaran token penasihat untuk loop agentic penuh untuk membantu model mengatur diri sendiri pada tugas agentic panjang dengan anggaran tugas.

---

<Note>
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Anggaran tugas memungkinkan Anda memberi tahu Claude berapa banyak token yang dimilikinya untuk loop agentic penuh, termasuk pemikiran, panggilan alat, hasil alat, dan output. Model melihat hitungan mundur yang berjalan dan menggunakannya untuk memprioritaskan pekerjaan dan menyelesaikan dengan anggun saat anggaran dikonsumsi.

<Note>
Anggaran tugas berada dalam beta publik di [Claude Opus 4.7](/docs/id/about-claude/models/overview). Atur header beta `task-budgets-2026-03-13` untuk memilih.
</Note>

## Kapan menggunakan anggaran tugas

Anggaran tugas bekerja terbaik untuk alur kerja agentic di mana Claude membuat beberapa panggilan alat dan keputusan sebelum menyelesaikan outputnya untuk menunggu respons manusia berikutnya. Gunakan ketika:

- Anda ingin Claude mengatur diri sendiri pengeluaran token pada tugas horizon panjang.
- Anda memiliki biaya per-tugas yang dapat diprediksi atau batas latensi untuk diterapkan.
- Anda ingin model menyelesaikan dengan anggun (merangkum temuan, melaporkan kemajuan) saat mendekati anggaran daripada memotong di tengah-aksi.

Anggaran tugas melengkapi [parameter effort](/docs/id/build-with-claude/effort): effort mengontrol seberapa menyeluruh Claude bernalar tentang setiap langkah, sementara anggaran tugas membatasi total pekerjaan yang dapat dilakukan Claude di seluruh loop agentic.

## Menetapkan anggaran tugas

Tambahkan `task_budget` ke `output_config` dan sertakan header beta:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: task-budgets-2026-03-13" \
    --header "content-type: application/json" \
    --data '{
        "model": "claude-opus-4-7",
        "max_tokens": 128000,
        "messages": [{
            "role": "user",
            "content": "Review the codebase and propose a refactor plan."
        }],
        "output_config": {
            "effort": "high",
            "task_budget": {"type": "tokens", "total": 64000}
        }
    }'
```

```bash CLI
ant beta:messages create --beta task-budgets-2026-03-13 <<'YAML'
model: claude-opus-4-7
max_tokens: 128000
messages:
  - role: user
    content: Review the codebase and propose a refactor plan.
output_config:
  effort: high
  task_budget:
    type: tokens
    total: 64000
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=128000,
    output_config={
        "effort": "high",
        "task_budget": {"type": "tokens", "total": 64000},
    },
    messages=[
        {"role": "user", "content": "Review the codebase and propose a refactor plan."}
    ],
    betas=["task-budgets-2026-03-13"],
)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.beta.messages.create({
  model: "claude-opus-4-7",
  max_tokens: 128000,
  output_config: {
    effort: "high",
    task_budget: { type: "tokens", total: 64000 }
  },
  messages: [{ role: "user", content: "Review the codebase and propose a refactor plan." }],
  betas: ["task-budgets-2026-03-13"]
});
```

```go Go hidelines={1..10,-2..}
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()

	response, _ := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
		Model:     "claude-opus-4-7",
		MaxTokens: 128000,
		Betas:     []anthropic.AnthropicBeta{"task-budgets-2026-03-13"},
		Messages: []anthropic.BetaMessageParam{{
			Role: anthropic.BetaMessageParamRoleUser,
			Content: []anthropic.BetaContentBlockParamUnion{{
				OfText: &anthropic.BetaTextBlockParam{Text: "Review the codebase and propose a refactor plan."},
			}},
		}},
		OutputConfig: anthropic.BetaOutputConfigParam{
			Effort: anthropic.BetaOutputConfigEffortHigh,
			TaskBudget: anthropic.BetaTokenTaskBudgetParam{
				Total: 64000,
			},
		},
	})
	fmt.Println(response)
}
```

```java Java hidelines={1..7,9..11,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaOutputConfig;
import com.anthropic.models.beta.messages.BetaTokenTaskBudget;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_7)
            .maxTokens(128000L)
            .addUserMessage("Review the codebase and propose a refactor plan.")
            .outputConfig(BetaOutputConfig.builder()
                .effort(BetaOutputConfig.Effort.HIGH)
                .taskBudget(BetaTokenTaskBudget.builder().total(64000L).build())
                .build())
            .addBeta("task-budgets-2026-03-13")
            .build();

        BetaMessage response = client.beta().messages().create(params);
    }
}
```

```csharp C# hidelines={1..3}
using Anthropic;
using Anthropic.Models.Beta.Messages;
using Anthropic.Models.Messages;

var client = new AnthropicClient();

var response = await client.Beta.Messages.Create(new MessageCreateParams
{
    Model = "claude-opus-4-7",
    MaxTokens = 128000,
    Messages = [new() { Role = Role.User, Content = "Review the codebase and propose a refactor plan." }],
    OutputConfig = new BetaOutputConfig
    {
        Effort = Effort.High,
        TaskBudget = new BetaTokenTaskBudget { Total = 64000 },
    },
    Betas = ["task-budgets-2026-03-13"],
});
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$response = $client->beta->messages->create(
    model: 'claude-opus-4-7',
    maxTokens: 128000,
    messages: [
        ['role' => 'user', 'content' => 'Review the codebase and propose a refactor plan.'],
    ],
    outputConfig: [
        'effort' => 'high',
        'taskBudget' => ['type' => 'tokens', 'total' => 64000],
    ],
    betas: ['task-budgets-2026-03-13'],
);
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.beta.messages.create(
  model: "claude-opus-4-7",
  max_tokens: 128_000,
  messages: [
    { role: "user", content: "Review the codebase and propose a refactor plan." }
  ],
  output_config: {
    effort: :high,
    task_budget: { type: :tokens, total: 64_000 }
  },
  betas: ["task-budgets-2026-03-13"]
)

puts response
```
</CodeGroup>

Objek `task_budget` memiliki tiga bidang:

- `type`: selalu `"tokens"`.
- `total`: jumlah token yang dapat dihabiskan Claude di seluruh loop agentic, termasuk pemikiran, panggilan alat, hasil alat, dan output.
- `remaining` (opsional): sisa anggaran yang dibawa dari permintaan sebelumnya. Defaultnya adalah `total` saat dihilangkan.

## Cara kerja hitungan mundur anggaran

Claude melihat penanda hitungan mundur anggaran yang disuntikkan sisi server di seluruh percakapan. Penanda menunjukkan berapa banyak token yang tersisa dalam loop agentic saat ini dan diperbarui saat model menghasilkan pemikiran, panggilan alat, dan output, serta saat memproses hasil alat. Claude menggunakan sinyal ini untuk mengatur kecepatan dirinya dan menyelesaikan dengan anggun saat anggaran dikonsumsi.

<Warning>
**Hitungan mundur mencerminkan token yang telah diproses Claude dalam loop agentic saat ini, bukan token yang Anda kirim kembali antar giliran.** Jika klien Anda mengirim riwayat percakapan lengkap pada setiap permintaan tindak lanjut, jumlah token sisi klien Anda mungkin berbeda dari anggaran yang dilacak Claude. Jika Anda juga mengurangi `remaining` sambil mengirim kembali riwayat lengkap, model melihat anggaran yang kurang dilaporkan dan hitungan mundur turun lebih cepat dari yang seharusnya, menyebabkan Claude membungkus lebih awal dari yang sebenarnya diizinkan anggaran. Tetapkan anggaran yang murah hati dan biarkan model mengatur diri sendiri terhadap hitungan mundur daripada mencoba mencerminkannya sisi klien.
</Warning>

### Contoh yang dikerjakan: penghitungan anggaran di seluruh giliran

Anggaran tugas menghitung apa yang Claude **lihat** (pemikiran, panggilan alat dan hasil, serta teks), bukan apa yang ada dalam muatan permintaan Anda. Dalam loop agentic, klien Anda mengirim kembali percakapan lengkap pada setiap permintaan, sehingga muatan tumbuh giliran demi giliran, tetapi anggaran hanya berkurang dengan token yang Claude lihat giliran ini.

Pertimbangkan loop dengan `task_budget: {type: "tokens", total: 100000}` dan satu alat `bash`.

**Giliran 1.** Anda mengirim permintaan awal:

```json
{
  "messages": [
    { "role": "user", "content": "Audit this repo for security issues and report findings." }
  ]
}
```

Claude berpikir, kemudian memancarkan panggilan alat dan berhenti dengan `stop_reason: "tool_use"`:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "thinking",
      "thinking": "I'll start by listing dependencies to look for known-vulnerable packages..."
    },
    {
      "type": "tool_use",
      "id": "toolu_01",
      "name": "bash",
      "input": { "command": "cat package.json && npm audit --json" }
    }
  ]
}
```

Misalkan giliran asisten ini (pemikiran ditambah panggilan alat) berjumlah 5.000 token yang dihasilkan. Hitungan mundur yang Claude lihat selama generasi berakhir dekat `remaining` ≈ 95.000.

**Giliran 2.** Klien Anda menjalankan alat, kemudian mengirim kembali riwayat lengkap dengan hasil alat ditambahkan:

```json
{
  "messages": [
    { "role": "user", "content": "Audit this repo for security issues and report findings." },
    {
      "role": "assistant",
      "content": [
        { "type": "thinking", "thinking": "I'll start by listing dependencies..." },
        {
          "type": "tool_use",
          "id": "toolu_01",
          "name": "bash",
          "input": { "command": "cat package.json && npm audit --json" }
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01",
          "content": "<2,800 tokens of npm audit output>"
        }
      ]
    }
  ]
}
```

Pesan pengguna dan asisten giliran 1 yang dikirim kembali tidak dihitung lagi, tetapi hasil alat 2.800-token adalah konten baru yang Claude lihat giliran ini dan dihitung terhadap anggaran. Claude menghabiskan 4.000 token lagi untuk pemikiran dan panggilan alat kedua (`grep -rn "eval(" src/`). Hitungan mundur berakhir dekat `remaining` ≈ 88.200.

**Giliran 3.** Riwayat lengkap dikirim kembali dengan hasil alat kedua (1.200 token keluaran grep) ditambahkan. Claude menulis laporan temuan akhir 6.000-token dan berhenti dengan `stop_reason: "end_turn"`. `remaining` ≈ 81.000.

Meletakkan tiga giliran berdampingan membuat perbedaan antara ukuran muatan dan pengeluaran anggaran eksplisit:

| Giliran | Muatan permintaan (perkiraan token input yang Anda kirim) | Token dihitung terhadap anggaran giliran ini | Anggaran `remaining` setelah |
|---|---|---|---|
| 1 | ~20 | 5.000 (pemikiran + `tool_use`) | ~95.000 |
| 2 | ~7.800 (riwayat giliran 1 + hasil alat) | 6.800 (2.800 hasil alat + 4.000 pemikiran dan `tool_use`) | ~88.200 |
| 3 | ~13.000 (riwayat lengkap + hasil alat kedua) | 7.200 (1.200 hasil alat + 6.000 `text`) | ~81.000 |
| **Total** | **~20.820 dikirim di seluruh permintaan** | **19.000 dihitung terhadap anggaran** | — |

Klien Anda mengirim pesan pengguna giliran 1 tiga kali dan pesan asisten giliran 1 dua kali, tetapi masing-masing dihitung sekali. Anggaran menghabiskan 19.000 dari 100.000 token, meskipun muatan kumulatif yang dikirim klien Anda lebih besar dan input yang disimpan cache pada giliran 2 dan 3 lebih besar lagi.

### Membawa anggaran di seluruh pemadatan dengan `remaining`

Jika loop agentic Anda memadatkan atau menulis ulang konteks antara permintaan (misalnya, dengan merangkum giliran sebelumnya), server tidak memiliki memori tentang berapa banyak anggaran yang dihabiskan sebelum pemadatan. Lewatkan `remaining` pada permintaan berikutnya sehingga hitungan mundur berlanjut dari tempat Anda tinggalkan daripada mengatur ulang ke `total`:

<CodeGroup>
```python Python
output_config = {
    "effort": "high",
    "task_budget": {
        "type": "tokens",
        "total": 128000,
        "remaining": 128000 - tokens_spent_so_far,
    },
}
```

```typescript TypeScript
const output_config = {
  effort: "high",
  task_budget: {
    type: "tokens",
    total: 128000,
    remaining: 128000 - tokensSpentSoFar
  }
};
```

```go Go
outputConfig := anthropic.BetaOutputConfigParam{
	Effort: anthropic.BetaOutputConfigEffortHigh,
	TaskBudget: anthropic.BetaTokenTaskBudgetParam{
		Total:     128000,
		Remaining: anthropic.Int(128000 - tokensSpentSoFar),
	},
}
```

```java Java
BetaOutputConfig outputConfig = BetaOutputConfig.builder()
    .effort(BetaOutputConfig.Effort.HIGH)
    .taskBudget(BetaTokenTaskBudget.builder()
        .total(128000L)
        .remaining(128000L - tokensSpentSoFar)
        .build())
    .build();
```

```csharp C#
var outputConfig = new BetaOutputConfig
{
    Effort = Effort.High,
    TaskBudget = new BetaTokenTaskBudget
    {
        Total = 128000,
        Remaining = 128000 - tokensSpentSoFar,
    },
};
```

```php PHP
$outputConfig = [
    'effort' => 'high',
    'taskBudget' => [
        'type' => 'tokens',
        'total' => 128000,
        'remaining' => 128000 - $tokensSpentSoFar,
    ],
];
```

```ruby Ruby
output_config = {
  effort: :high,
  task_budget: {
    type: :tokens,
    total: 128_000,
    remaining: 128_000 - tokens_spent_so_far
  }
}
```
</CodeGroup>

Untuk loop yang mengirim kembali riwayat lengkap yang tidak dipadatkan pada setiap giliran, hilangkan `remaining` dan biarkan server melacak hitungan mundur.

## Anggaran tugas bersifat penasihat, bukan diterapkan

Anggaran tugas adalah **petunjuk lembut, bukan batas keras**. Claude mungkin kadang-kadang melampaui anggaran jika berada di tengah-tengah tindakan yang akan lebih mengganggu untuk dihentikan daripada diselesaikan. Batas yang diterapkan pada total token output masih `max_tokens`, yang memotong respons dengan `stop_reason: "max_tokens"` saat tercapai.

Untuk batas keras pada biaya atau latensi, gabungkan anggaran tugas dengan nilai `max_tokens` yang wajar:

- Gunakan `task_budget` untuk memberikan Claude target untuk mengatur kecepatan.
- Gunakan `max_tokens` sebagai batas absolut yang mencegah generasi liar.

Karena `task_budget` mencakup loop agentic penuh (berpotensi banyak permintaan) sementara `max_tokens` membatasi setiap permintaan individual, kedua nilai tersebut independen; satu tidak diperlukan untuk berada di atau di bawah yang lain.

<Warning>
**Anggaran yang terlalu kecil untuk tugas dapat menyebabkan perilaku seperti penolakan.** Ketika Claude melihat anggaran yang jelas tidak cukup untuk pekerjaan yang diminta (misalnya, anggaran 20.000-token untuk tugas pengkodean agentic multi-jam), mungkin menolak untuk mencoba tugas sama sekali, membatasi ruang lingkup secara agresif, atau berhenti lebih awal dengan hasil parsial daripada memulai pekerjaan yang tidak dapat diselesaikan. Jika Anda mengamati penolakan yang tidak terduga atau pemberhentian prematur setelah menetapkan anggaran, naikkan anggaran sebelum men-debug parameter lain. Ukuran anggaran terhadap distribusi panjang tugas aktual Anda daripada default tetap; lihat [Memilih anggaran](#choosing-a-budget).
</Warning>

## Memilih anggaran

Anggaran yang tepat tergantung pada berapa banyak pekerjaan yang dilakukan loop agentic Anda saat ini. Daripada menebak, ukur penggunaan token yang ada terlebih dahulu dan kemudian sesuaikan dari sana.

### Ukur penggunaan saat ini Anda

Jalankan sampel tugas yang representatif **tanpa** `task_budget` yang ditetapkan dan catat total token yang dihabiskan Claude per tugas. Untuk loop agentic, jumlahkan `usage.output_tokens` ditambah pemikiran dan token hasil alat di seluruh setiap permintaan dalam loop:

<CodeGroup>
```python Python
def run_task_and_count_tokens(messages: list) -> int:
    """Runs an agentic loop to completion and returns total tokens spent."""
    total_spend = 0
    while True:
        response = client.beta.messages.create(
            model="claude-opus-4-7",
            max_tokens=128000,
            messages=messages,
            tools=tools,
            betas=["task-budgets-2026-03-13"],
        )
        # Count what Claude generated this turn (output covers text + thinking + tool calls).
        # Tool-result tokens also count against the budget; add the token count of the
        # tool_result blocks you append below if you want client-side tracking to match
        # the server-side countdown.
        total_spend += response.usage.output_tokens
        if response.stop_reason == "end_turn":
            return total_spend
        # Append the assistant turn and your tool results, then continue the loop.
        messages += [
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": run_tools(response.content)},
        ]
```

```typescript TypeScript
async function runTaskAndCountTokens(
  messages: Anthropic.Beta.BetaMessageParam[]
): Promise<number> {
  let totalSpend = 0;
  while (true) {
    const response = await client.beta.messages.create({
      model: "claude-opus-4-7",
      max_tokens: 128000,
      messages,
      tools,
      betas: ["task-budgets-2026-03-13"]
    });
    // Count what Claude generated this turn (output covers text + tool calls;
    // add cache creation and thinking via the same usage object if you opt in).
    totalSpend += response.usage.output_tokens;
    if (response.stop_reason === "end_turn") {
      return totalSpend;
    }
    // Append the assistant turn and your tool results, then continue the loop.
    messages = [
      ...messages,
      { role: "assistant", content: response.content },
      { role: "user", content: runTools(response.content) }
    ];
  }
}
```
</CodeGroup>

Jalankan ini di seluruh set tugas yang representatif dan catat distribusinya. Mulai dengan p99 pengeluaran token per-tugas Anda untuk memahami bagaimana memberikan model dengan anggaran tugas dapat mengubah perilaku model, kemudian uji naik atau turun sesuai kebutuhan.

Minimum yang diterima `task_budget.total` adalah **20.000 token**; nilai di bawah minimum mengembalikan kesalahan 400.

## Interaksi dengan parameter lain

- **`max_tokens`:** Ortogonal terhadap anggaran tugas. `max_tokens` adalah batas keras per-permintaan pada token yang dihasilkan, sementara `task_budget` adalah batas penasihat di seluruh loop agentic penuh (berpotensi mencakup banyak permintaan). Pada effort `xhigh` atau `max`, atur `max_tokens` ke setidaknya 64k untuk memberi Claude ruang untuk berpikir dan bertindak pada setiap permintaan.
- **[Effort](/docs/id/build-with-claude/effort):** Effort mengontrol seberapa dalam Claude bernalar per langkah. Anggaran tugas mengontrol berapa banyak total pekerjaan yang dilakukan Claude di seluruh loop agentic. Keduanya saling melengkapi: effort menyesuaikan kedalaman, anggaran tugas menyesuaikan luas.
- **[Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking):** Anggaran tugas termasuk token pemikiran dalam hitungan, sehingga pemikiran adaptif secara alami berkurang saat anggaran habis.
- **[Prompt caching](/docs/id/build-with-claude/prompt-caching):** Penanda hitungan mundur anggaran disuntikkan sisi server per giliran, sehingga tidak cocok di seluruh permintaan. Jika klien Anda mengurangi `task_budget.remaining` pada setiap permintaan tindak lanjut, nilai yang berubah membatalkan awalan cache apa pun yang memuatnya. Untuk mempertahankan caching, atur anggaran sekali pada permintaan awal dan biarkan model mengatur diri sendiri terhadap hitungan mundur sisi server daripada memutasi anggaran sisi klien.

## Dukungan fitur

| Model | Dukungan |
|-------|---------|
| Claude Opus 4.7 | Beta publik (atur header `task-budgets-2026-03-13`) |
| Claude Opus 4.6 | Tidak didukung |
| Claude Sonnet 4.6 | Tidak didukung |
| Claude Haiku 4.5 | Tidak didukung |

Anggaran tugas tidak didukung di permukaan [Claude Code](https://docs.claude.com/en/docs/claude-code) atau Cowork saat peluncuran. Gunakan anggaran tugas langsung melalui Messages API di Claude Opus 4.7.