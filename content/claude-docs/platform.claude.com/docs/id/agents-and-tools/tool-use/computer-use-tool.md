---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool
fetched_at: 2026-06-26T03:16:19.812719Z
sha256: 5b58fef182742bfba1d9d840e95cc55d189a153d25ac0a1e658fa2b944438b62
---

# Alat computer use

---

Claude dapat berinteraksi dengan lingkungan komputer melalui alat "computer use" (penggunaan komputer), yang menyediakan kemampuan tangkapan layar serta kontrol mouse/keyboard untuk interaksi desktop secara otonom. Pada [WebArena](https://webarena.dev/), sebuah benchmark untuk navigasi web otonom di berbagai situs web nyata, Claude mencapai hasil terbaik di kelasnya di antara sistem agen tunggal, menunjukkan kemampuan yang kuat untuk menyelesaikan tugas browser multi-langkah dari awal hingga akhir.

<Note>
Computer use masih dalam tahap beta dan memerlukan [beta header](/docs/id/api/beta-headers):
- `"computer-use-2025-11-24"` untuk Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, dan Claude Opus 4.5
- `"computer-use-2025-01-24"` untuk Claude Sonnet 4.5, Claude Haiku 4.5, Claude Opus 4.1 ([tidak digunakan lagi](/docs/id/about-claude/model-deprecations)), Claude Sonnet 4 ([dihentikan, kecuali di Bedrock dan Vertex AI](/docs/id/about-claude/model-deprecations)), dan Claude Opus 4 ([dihentikan, kecuali di Vertex AI](/docs/id/about-claude/model-deprecations))

Hubungi kami melalui [formulir umpan balik](https://forms.gle/H6UFuXaaLywri9hz6) untuk membagikan masukan Anda tentang fitur ini.
</Note>

<Note>
Fitur ini memenuhi syarat untuk [Zero Data Retention (ZDR)](/docs/id/build-with-claude/api-and-data-retention). Ketika organisasi Anda memiliki pengaturan ZDR, data yang dikirim melalui fitur ini tidak disimpan setelah respons API dikembalikan.
</Note>

## Ikhtisar \{#overview}

Computer use adalah fitur beta yang memungkinkan Claude berinteraksi dengan lingkungan desktop. Alat ini menyediakan:

- **Tangkapan layar:** Melihat apa yang sedang ditampilkan di layar
- **Kontrol mouse:** Mengklik, menyeret, dan menggerakkan kursor
- **Input keyboard:** Mengetik teks dan menggunakan pintasan keyboard
- **Otomatisasi desktop:** Berinteraksi dengan aplikasi atau antarmuka apa pun

Meskipun computer use dapat dilengkapi dengan alat lain seperti bash dan text editor untuk alur kerja otomatisasi yang lebih komprehensif, computer use secara spesifik mengacu pada kemampuan alat computer use untuk melihat dan mengontrol lingkungan desktop.

Untuk dukungan model, lihat [Referensi alat](/docs/id/agents-and-tools/tool-use/tool-reference).

## Pertimbangan keamanan \{#security-considerations}

Computer use adalah fitur beta dengan risiko unik yang berbeda dari fitur API standar. Risiko ini meningkat saat berinteraksi dengan internet.

<Warning>
Untuk meminimalkan risiko, pertimbangkan untuk mengambil tindakan pencegahan seperti:

1. Menggunakan mesin virtual atau container khusus dengan hak akses minimal untuk mencegah serangan sistem langsung atau kecelakaan.
2. Menghindari memberikan model akses ke data sensitif, seperti informasi login akun, untuk mencegah pencurian informasi.
3. Membatasi akses internet ke daftar domain yang diizinkan (allowlist) untuk mengurangi paparan terhadap konten berbahaya.
4. Meminta manusia untuk mengonfirmasi keputusan yang mungkin menghasilkan konsekuensi nyata yang signifikan dan tugas apa pun yang memerlukan persetujuan afirmatif, seperti menerima cookie, menyelesaikan transaksi keuangan, atau menyetujui ketentuan layanan.
</Warning>

Dalam beberapa keadaan, Claude akan mengikuti perintah yang ditemukan dalam konten meskipun bertentangan dengan instruksi pengguna. Misalnya, instruksi untuk Claude di halaman web atau yang terdapat dalam gambar mungkin menggantikan instruksi atau menyebabkan Claude membuat kesalahan. Ambil tindakan pencegahan untuk mengisolasi Claude dari data dan tindakan sensitif guna menghindari risiko terkait prompt injection.

Anthropic telah melatih model untuk menolak prompt injection ini dan telah menambahkan lapisan pertahanan tambahan. Jika Anda menggunakan alat computer use, classifier akan secara otomatis berjalan pada prompt Anda untuk menandai potensi kasus prompt injection. Ketika classifier ini mengidentifikasi potensi prompt injection dalam tangkapan layar, mereka akan secara otomatis mengarahkan model untuk meminta konfirmasi pengguna sebelum melanjutkan ke tindakan berikutnya. Perlindungan tambahan ini tidak akan ideal untuk setiap kasus penggunaan (misalnya, kasus penggunaan tanpa manusia dalam loop), jadi jika Anda ingin menonaktifkannya, [hubungi dukungan](https://support.claude.com/en/).

Tindakan pencegahan ini tetap penting bahkan dengan adanya lapisan pertahanan classifier.

Informasikan pengguna akhir tentang risiko yang relevan dan dapatkan persetujuan mereka sebelum mengaktifkan computer use di produk Anda sendiri.

<Card
  title="Implementasi referensi computer use"
  icon="computer"
  href="https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo"
>

Mulailah dengan implementasi referensi computer use yang mencakup antarmuka web, container Docker, contoh implementasi alat, dan agent loop.

</Card>

## Mulai cepat \{#quick-start}

Berikut cara memulai dengan computer use:

<CodeGroup>
```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: computer-use-2025-11-24" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "tools": [
      {
        "type": "computer_20251124",
        "name": "computer",
        "display_width_px": 1024,
        "display_height_px": 768,
        "display_number": 1
      },
      {
        "type": "text_editor_20250728",
        "name": "str_replace_based_edit_tool"
      },
      {
        "type": "bash_20250124",
        "name": "bash"
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "Save a picture of a cat to my desktop."
      }
    ]
  }'
```

```bash CLI
ant beta:messages create --beta computer-use-2025-11-24 <<'YAML'
model: claude-opus-4-8
max_tokens: 1024
tools:
  - type: computer_20251124
    name: computer
    display_width_px: 1024
    display_height_px: 768
    display_number: 1
  - type: text_editor_20250728
    name: str_replace_based_edit_tool
  - type: bash_20250124
    name: bash
messages:
  - role: user
    content: Save a picture of a cat to my desktop.
YAML
```

```python Python hidelines={1..2}
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-8",  # or another compatible model
    max_tokens=1024,
    tools=[
        {
            "type": "computer_20251124",
            "name": "computer",
            "display_width_px": 1024,
            "display_height_px": 768,
            "display_number": 1,
        },
        {"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"},
        {"type": "bash_20250124", "name": "bash"},
    ],
    messages=[{"role": "user", "content": "Save a picture of a cat to my desktop."}],
    betas=["computer-use-2025-11-24"],
)
print(response)
```

```typescript TypeScript hidelines={1..2}
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const response = await client.beta.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [
    {
      type: "computer_20251124",
      name: "computer",
      display_width_px: 1024,
      display_height_px: 768,
      display_number: 1
    },
    {
      type: "text_editor_20250728",
      name: "str_replace_based_edit_tool"
    },
    {
      type: "bash_20250124",
      name: "bash"
    }
  ],
  messages: [{ role: "user", content: "Save a picture of a cat to my desktop." }],
  betas: ["computer-use-2025-11-24"]
});

console.log(response);
```

```csharp C#
using Anthropic;
using Anthropic.Models.Beta.Messages;
using Messages = Anthropic.Models.Messages;

var client = new AnthropicClient();

var parameters = new MessageCreateParams
{
    Model = Messages::Model.ClaudeOpus4_8,
    MaxTokens = 1024,
    Tools = new BetaToolUnion[]
    {
        new BetaToolComputerUse20251124
        {
            DisplayWidthPx = 1024,
            DisplayHeightPx = 768,
            DisplayNumber = 1
        },
        new BetaToolTextEditor20250728(),
        new BetaToolBash20250124()
    },
    Messages =
    [
        new BetaMessageParam
        {
            Role = Role.User,
            Content = "Save a picture of a cat to my desktop."
        }
    ],
    Betas = ["computer-use-2025-11-24"]
};

var response = await client.Beta.Messages.Create(parameters);
Console.WriteLine(response);
```

```go Go hidelines={1..11,-1}
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
		Model:     anthropic.ModelClaudeOpus4_8,
		MaxTokens: 1024,
		Tools: []anthropic.BetaToolUnionParam{
			{OfComputerUseTool20251124: &anthropic.BetaToolComputerUse20251124Param{
				DisplayWidthPx:  1024,
				DisplayHeightPx: 768,
				DisplayNumber:   anthropic.Int(1),
			}},
			{OfTextEditor20250728: &anthropic.BetaToolTextEditor20250728Param{}},
			{OfBashTool20250124: &anthropic.BetaToolBash20250124Param{}},
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Save a picture of a cat to my desktop.")),
		},
		Betas: []anthropic.AnthropicBeta{
			"computer-use-2025-11-24", // typed constant pending in the Go SDK
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..2}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaToolBash20250124;
import com.anthropic.models.beta.messages.BetaToolComputerUse20251124;
import com.anthropic.models.beta.messages.BetaToolTextEditor20250728;
import com.anthropic.models.beta.messages.MessageCreateParams;

void main() {
    AnthropicClient client = AnthropicOkHttpClient.fromEnv();

    MessageCreateParams params = MessageCreateParams.builder()
        .model("claude-opus-4-8")
        .maxTokens(1024L)
        .addTool(BetaToolComputerUse20251124.builder()
            .displayWidthPx(1024L)
            .displayHeightPx(768L)
            .displayNumber(1L)
            .build())
        .addTool(BetaToolTextEditor20250728.builder().build())
        .addTool(BetaToolBash20250124.builder().build())
        .addUserMessage("Save a picture of a cat to my desktop.")
        .addBeta("computer-use-2025-11-24")
        .build();

    BetaMessage response = client.beta().messages().create(params);
    IO.println(response);
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client();

$response = $client->beta->messages->create(
    maxTokens: 1024,
    messages: [
        ['role' => 'user', 'content' => 'Save a picture of a cat to my desktop.'],
    ],
    model: 'claude-opus-4-8',
    tools: [
        [
            'type' => 'computer_20251124',
            'name' => 'computer',
            'display_width_px' => 1024,
            'display_height_px' => 768,
            'display_number' => 1,
        ],
        [
            'type' => 'text_editor_20250728',
            'name' => 'str_replace_based_edit_tool',
        ],
        [
            'type' => 'bash_20250124',
            'name' => 'bash',
        ],
    ],
    betas: ['computer-use-2025-11-24'],
);

echo $response;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

response = client.beta.messages.create(
  model: "claude-opus-4-8",
  max_tokens: 1024,
  tools: [
    {
      type: "computer_20251124",
      name: "computer",
      display_width_px: 1024,
      display_height_px: 768,
      display_number: 1
    },
    {
      type: "text_editor_20250728",
      name: "str_replace_based_edit_tool"
    },
    {
      type: "bash_20250124",
      name: "bash"
    }
  ],
  messages: [
    { role: "user", content: "Save a picture of a cat to my desktop." }
  ],
  betas: ["computer-use-2025-11-24"]
)

puts response
```
</CodeGroup>

<Note>
Beta header hanya diperlukan untuk alat computer use.

Contoh sebelumnya menunjukkan ketiga alat digunakan bersama, yang memerlukan beta header karena menyertakan alat computer use.
</Note>

---

## Cara kerja computer use \{#how-computer-use-works}

<Steps>
  <Step
    title="Berikan Claude alat computer use dan prompt pengguna"
    icon="tool"
  >
    - Tambahkan alat computer use (dan opsional alat lainnya) ke permintaan API Anda.
    - Sertakan prompt pengguna yang memerlukan interaksi desktop, misalnya, "Simpan gambar kucing ke desktop saya."
  </Step>
  <Step title="Claude memilih alat computer use" icon="wrench">
    - Claude menilai apakah alat computer use dapat membantu dengan kueri pengguna.
    - Jika ya, Claude menyusun permintaan penggunaan alat yang diformat dengan benar.
    - Respons API memiliki `stop_reason` berupa `tool_use`, yang menandakan permintaan penggunaan alat.
  </Step>
  <Step
    title="Ekstrak input alat, evaluasi alat di komputer, dan kembalikan hasilnya"
    icon="computer"
  >
    - Di sisi Anda, ekstrak nama alat dan input dari permintaan Claude.
    - Gunakan alat tersebut pada container atau mesin virtual.
    - Lanjutkan percakapan dengan pesan `user` baru yang berisi blok konten `tool_result`.
  </Step>
  <Step
    title="Claude terus memanggil alat computer use hingga tugas selesai"
    icon="arrows-clockwise"
  >
    - Claude menganalisis hasil alat untuk menentukan apakah diperlukan lebih banyak penggunaan alat atau tugas telah selesai.
    - Jika Claude menentukan alat lain diperlukan, ia merespons dengan `stop_reason` `tool_use` lagi dan Anda harus kembali ke langkah 3.
    - Jika tidak, ia menyusun respons teks untuk pengguna.
  </Step>
</Steps>

Pengulangan langkah 3 dan 4 tanpa input pengguna disebut sebagai "agent loop" (yaitu, Claude merespons dengan permintaan penggunaan alat dan aplikasi Anda merespons Claude dengan hasil evaluasi permintaan tersebut).

### Lingkungan komputasi \{#the-computing-environment}

Computer use memerlukan lingkungan komputasi sandbox tempat Claude dapat berinteraksi dengan aman dengan aplikasi dan web. Lingkungan ini mencakup:

1. **Tampilan virtual:** Server tampilan X11 virtual (menggunakan Xvfb) yang merender antarmuka desktop yang akan dilihat Claude melalui tangkapan layar dan dikontrol dengan tindakan mouse/keyboard.

2. **Lingkungan desktop:** UI ringan dengan window manager (Mutter) dan panel (Tint2) yang berjalan di Linux, yang menyediakan antarmuka grafis yang konsisten untuk Claude berinteraksi.

3. **Aplikasi:** Aplikasi Linux yang sudah terinstal seperti Firefox, LibreOffice, editor teks, dan file manager yang dapat digunakan Claude untuk menyelesaikan tugas.

4. **Implementasi alat:** Kode integrasi yang menerjemahkan permintaan alat abstrak Claude (seperti "gerakkan mouse" atau "ambil tangkapan layar") menjadi operasi aktual di lingkungan virtual.

5. **Agent loop:** Program yang menangani komunikasi antara Claude dan lingkungan, mengirimkan tindakan Claude ke lingkungan dan mengembalikan hasilnya (tangkapan layar, output perintah) kembali ke Claude.

Saat Anda menggunakan computer use, Claude tidak terhubung langsung ke lingkungan ini. Sebaliknya, aplikasi Anda:

1. Menerima permintaan penggunaan alat dari Claude
2. Menerjemahkannya menjadi tindakan di lingkungan komputasi Anda
3. Menangkap hasilnya (seperti tangkapan layar dan output perintah)
4. Mengembalikan hasil ini ke Claude

Untuk keamanan dan isolasi, implementasi referensi menjalankan semua ini di dalam container Docker dengan pemetaan port yang sesuai untuk melihat dan berinteraksi dengan lingkungan.

---

## Cara mengimplementasikan computer use \{#how-to-implement-computer-use}

### Mulai dengan implementasi referensi \{#start-with-the-reference-implementation}

Tersedia [implementasi referensi](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) yang mencakup semua yang Anda butuhkan untuk memulai dengan computer use:

- [Lingkungan dalam container](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/Dockerfile) yang cocok untuk computer use dengan Claude
- Implementasi [alat computer use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo/computer_use_demo/tools)
- [Agent loop](https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo/computer_use_demo/loop.py) yang berinteraksi dengan Claude API dan menjalankan alat computer use
- Antarmuka web untuk berinteraksi dengan container, agent loop, dan alat.

### Memahami agentic loop \{#understanding-the-agentic-loop}

Inti dari computer use adalah "agent loop": siklus di mana Claude meminta tindakan alat, aplikasi Anda menjalankannya, dan mengembalikan hasilnya ke Claude. Berikut contoh yang disederhanakan:

<Tabs>
<Tab title="cURL">
<Info>
Agent loop adalah pola stateful multi-giliran yang tidak dapat diterjemahkan ke perintah shell sekali jalan. Lihat tab SDK untuk implementasinya.
</Info>
</Tab>

<Tab title="CLI">
<Info>
Agent loop adalah pola stateful multi-giliran yang tidak dapat diterjemahkan ke perintah shell sekali jalan. Lihat tab SDK untuk implementasinya.
</Info>
</Tab>

<Tab title="Python">

````python
def sampling_loop(model, messages, max_iterations=10):
    """
    Run the computer-use agent loop until Claude stops requesting tools
    or the iteration limit is reached.
    """
    for _ in range(max_iterations):
        response = client.beta.messages.create(
            model=model,
            max_tokens=4096,
            messages=messages,
            tools=TOOLS,
            betas=["computer-use-2025-11-24"],
        )

        # Tambahkan respons Claude ke riwayat percakapan
        messages.append({"role": "assistant", "content": response.content})

        # Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
        tool_results = process_tool_calls(response)
        if not tool_results:
            return messages  # No more tool use; task complete

        # Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
        messages.append({"role": "user", "content": tool_results})

    return messages
````

</Tab>

<Tab title="TypeScript">

````typescript
async function samplingLoop(
  model: string,
  messages: Anthropic.Beta.BetaMessageParam[],
  maxIterations = 10,
): Promise<Anthropic.Beta.BetaMessageParam[]> {
  // Jalankan loop agen computer-use hingga Claude berhenti meminta alat
  // atau batas iterasi tercapai.
  for (let i = 0; i < maxIterations; i++) {
    const response = await client.beta.messages.create({
      model,
      max_tokens: 4096,
      messages,
      tools,
      betas: ["computer-use-2025-11-24"],
    });

    // Tambahkan respons Claude ke riwayat percakapan
    messages.push({ role: "assistant", content: response.content });

    // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
    const toolResults = processToolCalls(response);
    if (toolResults.length === 0) {
      return messages; // No more tool use; task complete
    }

    // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
    messages.push({ role: "user", content: toolResults });
  }

  return messages;
}
````

</Tab>

<Tab title="C#">

````csharp
async Task<List<BetaMessageParam>> SamplingLoop(
    Model model,
    List<BetaMessageParam> messages,
    int maxIterations = 10
)
{
    // Jalankan loop agen computer-use hingga Claude berhenti meminta alat
    // atau batas iterasi tercapai.
    for (var i = 0; i < maxIterations; i++)
    {
        var response = await client.Beta.Messages.Create(
            new MessageCreateParams
            {
                Model = model,
                MaxTokens = 4096,
                Messages = messages,
                Tools = tools,
                Betas = ["computer-use-2025-11-24"],
            }
        );

        // Tambahkan respons Claude ke riwayat percakapan
        messages.Add(
            new()
            {
                Role = Role.Assistant,
                Content = response
                    .Content.Select(block => new BetaContentBlockParam(block.Json))
                    .ToList(),
            }
        );

        // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
        var toolResults = ProcessToolCalls(response);
        if (toolResults.Count == 0)
        {
            return messages; // No more tool use; task complete
        }

        // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
        messages.Add(new() { Role = Role.User, Content = toolResults });
    }

    return messages;
}
````

</Tab>

<Tab title="Go">

````go
// samplingLoop menjalankan loop agen computer-use hingga Claude berhenti
// meminta alat atau batas iterasi tercapai.
func samplingLoop(ctx context.Context, model anthropic.Model, messages []anthropic.BetaMessageParam, maxIterations int) ([]anthropic.BetaMessageParam, error) {
	for range maxIterations {
		response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
			Model:     model,
			MaxTokens: 4096,
			Messages:  messages,
			Tools:     tools,
			Betas:     []anthropic.AnthropicBeta{"computer-use-2025-11-24"},
		})
		if err != nil {
			return nil, err
		}

		// Tambahkan respons Claude ke riwayat percakapan
		messages = append(messages, response.ToParam())

		// Jalankan alat yang diminta Claude dan kumpulkan hasilnya
		toolResults := processToolCalls(response)
		if len(toolResults) == 0 {
			return messages, nil // No more tool use; task complete
		}

		// Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
		messages = append(messages, anthropic.BetaMessageParam{
			Role:    anthropic.BetaMessageParamRoleUser,
			Content: toolResults,
		})
	}
	return messages, nil
}

````

</Tab>

<Tab title="Java">

````java
/**
 * Run the computer-use agent loop until Claude stops requesting tools
 * or the iteration limit is reached.
 */
List<BetaMessageParam> samplingLoop(Model model, List<BetaMessageParam> messages, int maxIterations) {
    for (int i = 0; i < maxIterations; i++) {
        BetaMessage response = client.beta().messages().create(MessageCreateParams.builder()
                .model(model)
                .maxTokens(4096)
                .messages(messages)
                .addTool(COMPUTER_TOOL)
                .addBeta("computer-use-2025-11-24")
                .build());

        // Tambahkan respons Claude ke riwayat percakapan
        messages.add(BetaMessageParam.builder()
                .role(BetaMessageParam.Role.ASSISTANT)
                .contentOfBetaContentBlockParams(
                        response.content().stream().map(BetaContentBlock::toParam).toList())
                .build());

        // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
        List<BetaContentBlockParam> toolResults = processToolCalls(response);
        if (toolResults.isEmpty()) {
            return messages; // No more tool use; task complete
        }

        // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
        messages.add(BetaMessageParam.builder()
                .role(BetaMessageParam.Role.USER)
                .contentOfBetaContentBlockParams(toolResults)
                .build());
    }
    return messages;
}
````

</Tab>

<Tab title="PHP">

````php
/**
 * Run the computer-use agent loop until Claude stops requesting tools
 * or the iteration limit is reached.
 */
function samplingLoop(string $model, array $messages, int $maxIterations = 10): array
{
    global $client, $tools;

    for ($i = 0; $i < $maxIterations; $i++) {
        $response = $client->beta->messages->create(
            model: $model,
            maxTokens: 4096,
            messages: $messages,
            tools: $tools,
            betas: ['computer-use-2025-11-24'],
        );

        // Tambahkan respons Claude ke riwayat percakapan
        $messages[] = BetaMessageParam::with(role: Role::ASSISTANT, content: $response->content);

        // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
        $toolResults = processToolCalls($response);
        if ($toolResults === []) {
            return $messages; // No more tool use; task complete
        }

        // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
        $messages[] = BetaMessageParam::with(role: Role::USER, content: $toolResults);
    }

    return $messages;
}
````

</Tab>

<Tab title="Ruby">

````ruby
# Jalankan loop agen computer-use hingga Claude berhenti meminta alat
# atau batas iterasi tercapai.
def sampling_loop(model, messages, max_iterations: 10)
  max_iterations.times do
    response = CLIENT.beta.messages.create(
      model: model,
      max_tokens: 4096,
      messages: messages,
      tools: TOOLS,
      betas: ["computer-use-2025-11-24"]
    )

    # Tambahkan respons Claude ke riwayat percakapan
    messages << {role: "assistant", content: response.content}

    # Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
    tool_results = process_tool_calls(response)
    return messages if tool_results.empty? # No more tool use; task complete

    # Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
    messages << {role: "user", content: tool_results}
  end

  messages
end
````

</Tab>
</Tabs>

Loop berlanjut hingga Claude merespons tanpa meminta alat apa pun (tugas selesai) atau batas iterasi maksimum tercapai. Pengaman ini mencegah potensi loop tak terbatas yang dapat mengakibatkan biaya API yang tidak terduga.

Cobalah implementasi referensi sebelum membaca sisa dokumentasi ini.

### Optimalkan performa model dengan prompting \{#optimize-model-performance-with-prompting}

Berikut beberapa tips untuk mendapatkan output berkualitas terbaik:

1. Tentukan tugas yang sederhana dan terdefinisi dengan baik, serta berikan instruksi eksplisit untuk setiap langkah.
2. Claude terkadang mengasumsikan hasil dari tindakannya tanpa secara eksplisit memeriksa hasilnya. Untuk mencegah hal ini, Anda dapat memberikan prompt kepada Claude dengan `After each step, take a screenshot and carefully evaluate if you have achieved the right outcome. Explicitly show your thinking: "I have evaluated step X..." If not correct, try again. Only when you confirm a step was executed correctly should you move on to the next one.`
3. Beberapa elemen UI (seperti dropdown dan scrollbar) mungkin sulit dimanipulasi oleh Claude menggunakan gerakan mouse. Jika Anda mengalami hal ini, coba berikan prompt kepada model untuk menggunakan pintasan keyboard.
4. Untuk tugas atau interaksi UI yang dapat diulang, sertakan contoh tangkapan layar dan pemanggilan alat dari hasil yang berhasil dalam prompt Anda.
5. Jika Anda memerlukan model untuk login, berikan nama pengguna dan kata sandi dalam prompt Anda di dalam tag XML seperti `<robot_credentials>`. Menggunakan computer use dalam aplikasi yang memerlukan login meningkatkan risiko hasil buruk akibat prompt injection. Tinjau [Mitigasi jailbreak dan prompt injection](/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) sebelum memberikan kredensial login kepada model.
6. Saat menyusun array `content` pada giliran pengguna, tempatkan teks instruksi *sebelum* gambar tangkapan layar. Memberikan deskripsi target sebelum gambar diproses meningkatkan akurasi klik.
7. Saat menggunakan `computer_20251124` dengan `enable_zoom: true` diatur, Claude akan memperbesar suatu wilayah ketika ditanya tentang teks kecil atau elemen UI tertentu yang tidak terbaca pada resolusi default tangkapan layar, seperti nama file di sidebar, judul tab, teks status bar, nomor baris, atau label tombol. Jika Claude tidak memperbesar saat Anda mengharapkannya, tanyakan tentang wilayah atau elemen tertentu, bukan layar secara keseluruhan.

<Tip>
  Jika Anda berulang kali menemui serangkaian masalah yang jelas atau mengetahui sebelumnya tugas
  yang perlu diselesaikan Claude, gunakan prompt sistem untuk memberikan Claude
  tips atau instruksi eksplisit tentang cara menyelesaikan tugas dengan sukses.
</Tip>

<Tip>
  Untuk agen yang mencakup beberapa sesi, jalankan verifikasi end-to-end di
  awal setiap sesi, bukan hanya setelah implementasi. Pemeriksaan berbasis browser
  menangkap regresi dari sesi sebelumnya yang terlewat oleh tinjauan tingkat kode saja. Lihat
  [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
  untuk detailnya.
</Tip>

### Prompt sistem \{#system-prompts}

Ketika salah satu alat dengan skema Anthropic diminta melalui Claude API, prompt sistem khusus computer use akan dihasilkan. Ini mirip dengan [prompt sistem penggunaan alat](/docs/id/agents-and-tools/tool-use/define-tools#tool-use-system-prompt) tetapi dimulai dengan:

> You have access to a set of functions you can use to answer the user's question. This includes access to a sandboxed computing environment. You do NOT currently have the ability to inspect files or interact with external resources, except by invoking the below functions.

Seperti halnya penggunaan alat biasa, field `system_prompt` yang disediakan pengguna tetap dihormati dan digunakan dalam penyusunan prompt sistem gabungan.

### Tindakan yang tersedia \{#available-actions}

Alat computer use mendukung tindakan berikut:

**Tindakan dasar (semua versi)**
- **screenshot:** Menangkap tampilan saat ini
- **left_click:** Klik pada koordinat `[x, y]`
- **type:** Mengetik string teks
- **key:** Menekan tombol atau kombinasi tombol (misalnya, "ctrl+s")
- **mouse_move:** Memindahkan kursor ke koordinat

**Tindakan yang ditingkatkan (`computer_20250124`)**
Tersedia di semua model yang mendukung computer use:
- **scroll:** Menggulir ke arah mana pun dengan kontrol jumlah
- **left_click_drag:** Klik dan seret antar koordinat
- **right_click**, **middle_click:** Tombol mouse tambahan
- **double_click**, **triple_click:** Klik ganda dan tiga kali
- **left_mouse_down**, **left_mouse_up:** Kontrol klik yang lebih detail
- **hold_key:** Menahan tombol selama durasi tertentu (dalam detik)
- **wait:** Jeda antar tindakan

**Tindakan yang ditingkatkan (`computer_20251124`)**
Tersedia di Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 4.6, dan Claude Opus 4.5:
- Semua tindakan dari `computer_20250124`
- **zoom:** Melihat wilayah tertentu dari layar pada resolusi penuh. Memerlukan `enable_zoom: true` dalam definisi alat. Menerima parameter `region` dengan koordinat `[x1, y1, x2, y2]` yang mendefinisikan sudut kiri atas dan kanan bawah dari area yang akan diperiksa.

<section title="Contoh tindakan">

Mengambil tangkapan layar:

```json
{
  "action": "screenshot"
}
```

Klik pada posisi:

```json
{
  "action": "left_click",
  "coordinate": [500, 300]
}
```

Mengetik teks:

```json
{
  "action": "type",
  "text": "Hello, world!"
}
```

Menggulir ke bawah:

```json
{
  "action": "scroll",
  "coordinate": [500, 400],
  "scroll_direction": "down",
  "scroll_amount": 3
}
```

Zoom untuk melihat wilayah secara detail (Claude Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 4.6, dan Opus 4.5):

```json
{
  "action": "zoom",
  "region": [100, 200, 400, 350]
}
```

</section>

<section title="Tombol modifier dengan tindakan klik dan scroll">

Untuk menahan tombol modifier (seperti Shift, Ctrl, atau Alt) saat melakukan tindakan klik atau scroll, gunakan parameter `text` pada tindakan tersebut. Ini berbeda dari `hold_key`, yang menahan tombol selama durasi tertentu tanpa melakukan tindakan lain.

Shift+klik (misalnya, untuk memilih rentang item):

```json
{
  "action": "left_click",
  "coordinate": [500, 300],
  "text": "shift"
}
```

Ctrl+klik (misalnya, untuk multi-select di Windows/Linux):

```json
{
  "action": "left_click",
  "coordinate": [500, 300],
  "text": "ctrl"
}
```

Cmd+klik (misalnya, untuk multi-select di macOS):

```json
{
  "action": "left_click",
  "coordinate": [500, 300],
  "text": "super"
}
```

Shift+scroll (misalnya, untuk menggulir secara horizontal):

```json
{
  "action": "scroll",
  "coordinate": [500, 400],
  "scroll_direction": "down",
  "scroll_amount": 3,
  "text": "shift"
}
```

Parameter `text` dalam tindakan klik/scroll menerima tombol modifier seperti `shift`, `ctrl`, `alt`, dan `super` (untuk tombol Command/Windows).

</section>

### Parameter alat \{#tool-parameters}

| Parameter | Wajib | Deskripsi |
|-----------|----------|-------------|
| `type` | Ya | Versi alat (`computer_20251124` atau `computer_20250124`) |
| `name` | Ya | Harus berupa "computer" |
| `display_width_px` | Ya | Lebar tampilan dalam piksel |
| `display_height_px` | Ya | Tinggi tampilan dalam piksel |
| `display_number` | Tidak | Nomor tampilan untuk lingkungan X11 |
| `enable_zoom` | Tidak | Mengaktifkan tindakan zoom (hanya `computer_20251124`). Atur ke `true` untuk mengizinkan Claude memperbesar wilayah layar tertentu. Default: `false` |

<Note>
**Penting:** Aplikasi Anda harus secara eksplisit menjalankan alat computer use; Claude tidak dapat menjalankannya secara langsung. Anda bertanggung jawab untuk mengimplementasikan pengambilan tangkapan layar, gerakan mouse, input keyboard, dan tindakan lainnya berdasarkan permintaan Claude.
</Note>

### Menggabungkan dengan pemikiran diperpanjang \{#combining-with-extended-thinking}

Untuk menggabungkan computer use dengan pemikiran diperpanjang, lihat [Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking).

<Tip>
Khusus untuk computer use, benchmarking internal menyarankan pengaturan `effort` berikut:

- **Claude Opus 4.7:** gunakan `high` sebagai default; gunakan `low` untuk beban kerja dengan throughput tinggi atau yang sensitif terhadap biaya.
- **Claude Sonnet 4.6 dan Claude Opus 4.6:** gunakan `medium` sebagai default (rasio akurasi-terhadap-biaya terbaik). Hindari `max`, yang menambah biaya token tanpa meningkatkan akurasi pada tugas UI. Pada model-model ini, `low` menggunakan *lebih sedikit* token output dibandingkan menonaktifkan thinking sepenuhnya (lebih sedikit kesalahan berarti lebih sedikit percobaan ulang), menjadikannya opsi yang kuat untuk loop yang sensitif terhadap biaya.
</Tip>

### Melengkapi computer use dengan alat lain \{#augmenting-computer-use-with-other-tools}

Untuk menambahkan alat lain bersama computer use, sertakan dalam array `tools` yang sama. Bagian [Mulai cepat](#quick-start) menunjukkan pola ini dengan [alat bash](/docs/id/agents-and-tools/tool-use/bash-tool) dan [alat text editor](/docs/id/agents-and-tools/tool-use/text-editor-tool). Anda dapat menambahkan [definisi alat kustom](/docs/id/agents-and-tools/tool-use/define-tools) Anda sendiri dengan cara yang sama.

### Membangun lingkungan computer use kustom \{#build-a-custom-computer-use-environment}

[Implementasi referensi](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) dimaksudkan untuk membantu Anda memulai dengan computer use. Ini mencakup semua komponen yang diperlukan agar Claude dapat menggunakan komputer. Namun, Anda dapat membangun lingkungan Anda sendiri untuk computer use sesuai kebutuhan Anda. Anda akan memerlukan:

- Lingkungan tervirtualisasi atau dalam container yang cocok untuk computer use dengan Claude
- Implementasi setidaknya satu alat computer use dengan skema Anthropic
- Agent loop yang berinteraksi dengan Claude API dan menjalankan hasil `tool_use` menggunakan implementasi alat Anda
- API atau UI yang memungkinkan input pengguna untuk memulai agent loop

#### Mengimplementasikan alat computer use \{#implement-the-computer-use-tool}

Alat computer use diimplementasikan sebagai alat tanpa skema. Saat menggunakan alat ini, Anda tidak perlu menyediakan skema input seperti pada alat lainnya; skema sudah terintegrasi ke dalam model Claude dan tidak dapat dimodifikasi.

<Steps>
  <Step title="Siapkan lingkungan komputasi Anda">
    Buat tampilan virtual atau hubungkan ke tampilan yang sudah ada yang akan berinteraksi dengan Claude. Ini biasanya melibatkan pengaturan Xvfb (X Virtual Framebuffer) atau teknologi serupa.
  </Step>
  <Step title="Implementasikan action handler">
    Buat fungsi untuk menangani setiap jenis tindakan yang mungkin diminta Claude:
    <Tabs>
    <Tab title="cURL">
    <Info>
    Ini adalah kode helper sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk polanya.
    </Info>
    </Tab>

    <Tab title="CLI">
    <Info>
    Ini adalah kode helper sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk polanya.
    </Info>
    </Tab>

    <Tab title="Python">
    
````python
def capture_screenshot():
    return "<screenshot data>"


def click_at(x, y):
    return f"clicked at ({x}, {y})"


def type_text(text):
    return f"typed: {text}"


def handle_computer_action(action_type, params):
    if action_type == "screenshot":
        return capture_screenshot()
    elif action_type == "left_click":
        x, y = params["coordinate"]
        return click_at(x, y)
    elif action_type == "type":
        return type_text(params["text"])
    # Tangani tindakan lain sesuai kebutuhan
    return f"unhandled action: {action_type}"
````

    </Tab>

    <Tab title="TypeScript">
    
````typescript
function captureScreenshot(): string {
  return "<screenshot data>";
}

function clickAt(x: number, y: number): string {
  return `clicked at (${x}, ${y})`;
}

function typeText(text: string): string {
  return `typed: ${text}`;
}

function handleComputerAction(
  actionType: string,
  params: Record<string, unknown>,
): string {
  if (actionType === "screenshot") {
    return captureScreenshot();
  } else if (actionType === "left_click") {
    const [x, y] = params.coordinate as [number, number];
    return clickAt(x, y);
  } else if (actionType === "type") {
    return typeText(params.text as string);
  }
  // Tangani aksi lainnya sesuai kebutuhan
  return `unhandled action: ${actionType}`;
}
````

    </Tab>

    <Tab title="C#">
    
````csharp
string CaptureScreenshot() => "<screenshot data>";

string ClickAt(int x, int y) => $"clicked at ({x}, {y})";

string TypeText(string text) => $"typed: {text}";

string HandleComputerAction(string actionType, IReadOnlyDictionary<string, JsonElement> input) =>
    actionType switch
    {
        "screenshot" => CaptureScreenshot(),
        "left_click" => ClickAt(
            input["coordinate"][0].GetInt32(),
            input["coordinate"][1].GetInt32()
        ),
        "type" => TypeText(input["text"].GetString()!),
        // Tangani aksi lainnya sesuai kebutuhan
        _ => $"unhandled action: {actionType}",
    };
````

    </Tab>

    <Tab title="Go">
    
````go
func captureScreenshot() string {
	return "<screenshot data>"
}

func clickAt(x, y int) string {
	return fmt.Sprintf("clicked at (%d, %d)", x, y)
}

func typeText(text string) string {
	return fmt.Sprintf("typed: %s", text)
}

func handleComputerAction(actionType string, params map[string]any) string {
	switch actionType {
	case "screenshot":
		return captureScreenshot()
	case "left_click":
		coord := params["coordinate"].([]any)
		return clickAt(int(coord[0].(float64)), int(coord[1].(float64)))
	case "type":
		return typeText(params["text"].(string))
	// Tangani aksi lainnya sesuai kebutuhan
	default:
		return fmt.Sprintf("unhandled action: %s", actionType)
	}
}

````

    </Tab>

    <Tab title="Java">
    
````java
String captureScreenshot() {
    return "<screenshot data>";
}

String clickAt(long x, long y) {
    return "clicked at (" + x + ", " + y + ")";
}

String typeText(String text) {
    return "typed: " + text;
}

String handleComputerAction(String actionType, Map<String, JsonValue> params) {
    return switch (actionType) {
        case "screenshot" -> captureScreenshot();
        case "left_click" -> {
            List<JsonValue> coordinate = (List<JsonValue>) params.get("coordinate").asArray().get();
            long x = ((Number) coordinate.get(0).asNumber().get()).longValue();
            long y = ((Number) coordinate.get(1).asNumber().get()).longValue();
            yield clickAt(x, y);
        }
        case "type" -> typeText(params.get("text").asStringOrThrow());
        // Tangani aksi lain sesuai kebutuhan
        default -> "unhandled action: " + actionType;
    };
}
````

    </Tab>

    <Tab title="PHP">
    
````php
function captureScreenshot(): string
{
    return '<screenshot data>';
}

function clickAt(int $x, int $y): string
{
    return "clicked at ({$x}, {$y})";
}

function typeText(string $text): string
{
    return "typed: {$text}";
}

function handleComputerAction(string $actionType, array $params): string
{
    return match ($actionType) {
        'screenshot' => captureScreenshot(),
        'left_click' => clickAt(...$params['coordinate']),
        'type' => typeText($params['text']),
        // Tangani tindakan lain sesuai kebutuhan
        default => "unhandled action: {$actionType}",
    };
}
````

    </Tab>

    <Tab title="Ruby">
    
````ruby
def capture_screenshot
  "<screenshot data>"
end

def click_at(x, y)
  "clicked at (#{x}, #{y})"
end

def type_text(text)
  "typed: #{text}"
end

def handle_computer_action(action_type, params)
  case action_type
  when "screenshot"
    capture_screenshot
  when "left_click"
    x, y = params[:coordinate]
    click_at(x, y)
  when "type"
    type_text(params[:text])
  # Tangani aksi lainnya sesuai kebutuhan
  else
    "unhandled action: #{action_type}"
  end
end
````

    </Tab>
    </Tabs>
  </Step>
  <Step title="Proses pemanggilan alat dari Claude">
    Ekstrak dan jalankan pemanggilan alat dari respons Claude:
    <Tabs>
    <Tab title="cURL">
    <Info>
    Ini adalah kode helper sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk polanya.
    </Info>
    </Tab>

    <Tab title="CLI">
    <Info>
    Ini adalah kode helper sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk polanya.
    </Info>
    </Tab>

    <Tab title="Python">
    
````python
def process_tool_calls(response):
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            action = block.input["action"]
            result = handle_computer_action(action, block.input)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                }
            )
    return tool_results
````

    </Tab>

    <Tab title="TypeScript">
    
````typescript
function processToolCalls(
  response: Anthropic.Beta.BetaMessage,
): Anthropic.Beta.BetaToolResultBlockParam[] {
  const toolResults: Anthropic.Beta.BetaToolResultBlockParam[] = [];
  for (const block of response.content) {
    if (block.type === "tool_use") {
      const input = block.input as Record<string, unknown>;
      const action = input.action as string;
      const result = handleComputerAction(action, input);
      toolResults.push({
        type: "tool_result",
        tool_use_id: block.id,
        content: result,
      });
    }
  }
  return toolResults;
}
````

    </Tab>

    <Tab title="C#">
    
````csharp
List<BetaContentBlockParam> ProcessToolCalls(BetaMessage response)
{
    List<BetaContentBlockParam> toolResults = [];
    foreach (var block in response.Content)
    {
        if (block.TryPickToolUse(out var toolUse))
        {
            var action = toolUse.Input["action"].GetString()!;
            var result = HandleComputerAction(action, toolUse.Input);
            toolResults.Add(new BetaToolResultBlockParam(toolUse.ID) { Content = result });
        }
    }
    return toolResults;
}
````

    </Tab>

    <Tab title="Go">
    
````go
func processToolCalls(response *anthropic.BetaMessage) []anthropic.BetaContentBlockParamUnion {
	var toolResults []anthropic.BetaContentBlockParamUnion
	for _, block := range response.Content {
		switch variant := block.AsAny().(type) {
		case anthropic.BetaToolUseBlock:
			input := variant.Input.(map[string]any)
			action := input["action"].(string)
			result := handleComputerAction(action, input)
			toolResults = append(toolResults, anthropic.NewBetaToolResultBlock(variant.ID, result, false))
		}
	}
	return toolResults
}

````

    </Tab>

    <Tab title="Java">
    
````java
List<BetaContentBlockParam> processToolCalls(BetaMessage response) {
    List<BetaContentBlockParam> toolResults = new ArrayList<>();
    for (BetaContentBlock block : response.content()) {
        if (block.isToolUse()) {
            BetaToolUseBlock toolUse = block.asToolUse();
            Map<String, JsonValue> input =
                    (Map<String, JsonValue>) toolUse._input().asObject().get();
            String action = input.get("action").asStringOrThrow();
            String result = handleComputerAction(action, input);
            toolResults.add(BetaContentBlockParam.ofToolResult(
                    BetaToolResultBlockParam.builder()
                            .toolUseId(toolUse.id())
                            .content(result)
                            .build()));
        }
    }
    return toolResults;
}
````

    </Tab>

    <Tab title="PHP">
    
````php
function processToolCalls(BetaMessage $response): array
{
    $toolResults = [];
    foreach ($response->content as $block) {
        if ($block instanceof BetaToolUseBlock) {
            $action = $block->input['action'];
            $result = handleComputerAction($action, $block->input);
            $toolResults[] = BetaToolResultBlockParam::with(
                toolUseID: $block->id,
                content: $result,
            );
        }
    }
    return $toolResults;
}
````

    </Tab>

    <Tab title="Ruby">
    
````ruby
def process_tool_calls(response)
  tool_results = []
  response.content.each do |block|
    next unless block.type == :tool_use

    action = block.input[:action]
    result = handle_computer_action(action, block.input)
    tool_results << {
      type: "tool_result",
      tool_use_id: block.id,
      content: result
    }
  end
  tool_results
end
````

    </Tab>
    </Tabs>
  </Step>
  <Step title="Implementasikan agent loop">
    Buat loop yang berlanjut hingga Claude menyelesaikan tugas:
    <Tabs>
    <Tab title="cURL">
    <Info>
    Agent loop adalah pola stateful multi-giliran yang tidak dapat diterjemahkan ke perintah shell sekali jalan. Lihat tab SDK untuk implementasinya.
    </Info>
    </Tab>

    <Tab title="CLI">
    <Info>
    Agent loop adalah pola stateful multi-giliran yang tidak dapat diterjemahkan ke perintah shell sekali jalan. Lihat tab SDK untuk implementasinya.
    </Info>
    </Tab>

    <Tab title="Python">
    
````python
def sampling_loop(model, messages, max_iterations=10):
    """
    Run the computer-use agent loop until Claude stops requesting tools
    or the iteration limit is reached.
    """
    for _ in range(max_iterations):
        response = client.beta.messages.create(
            model=model,
            max_tokens=4096,
            messages=messages,
            tools=TOOLS,
            betas=["computer-use-2025-11-24"],
        )

        # Tambahkan respons Claude ke riwayat percakapan
        messages.append({"role": "assistant", "content": response.content})

        # Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
        tool_results = process_tool_calls(response)
        if not tool_results:
            return messages  # No more tool use; task complete

        # Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
        messages.append({"role": "user", "content": tool_results})

    return messages
````

    </Tab>

    <Tab title="TypeScript">
    
````typescript
async function samplingLoop(
  model: string,
  messages: Anthropic.Beta.BetaMessageParam[],
  maxIterations = 10,
): Promise<Anthropic.Beta.BetaMessageParam[]> {
  // Jalankan loop agen computer-use hingga Claude berhenti meminta alat
  // atau batas iterasi tercapai.
  for (let i = 0; i < maxIterations; i++) {
    const response = await client.beta.messages.create({
      model,
      max_tokens: 4096,
      messages,
      tools,
      betas: ["computer-use-2025-11-24"],
    });

    // Tambahkan respons Claude ke riwayat percakapan
    messages.push({ role: "assistant", content: response.content });

    // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
    const toolResults = processToolCalls(response);
    if (toolResults.length === 0) {
      return messages; // No more tool use; task complete
    }

    // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
    messages.push({ role: "user", content: toolResults });
  }

  return messages;
}
````

    </Tab>

    <Tab title="C#">
    
````csharp
async Task<List<BetaMessageParam>> SamplingLoop(
    Model model,
    List<BetaMessageParam> messages,
    int maxIterations = 10
)
{
    // Jalankan loop agen computer-use hingga Claude berhenti meminta alat
    // atau batas iterasi tercapai.
    for (var i = 0; i < maxIterations; i++)
    {
        var response = await client.Beta.Messages.Create(
            new MessageCreateParams
            {
                Model = model,
                MaxTokens = 4096,
                Messages = messages,
                Tools = tools,
                Betas = ["computer-use-2025-11-24"],
            }
        );

        // Tambahkan respons Claude ke riwayat percakapan
        messages.Add(
            new()
            {
                Role = Role.Assistant,
                Content = response
                    .Content.Select(block => new BetaContentBlockParam(block.Json))
                    .ToList(),
            }
        );

        // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
        var toolResults = ProcessToolCalls(response);
        if (toolResults.Count == 0)
        {
            return messages; // No more tool use; task complete
        }

        // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
        messages.Add(new() { Role = Role.User, Content = toolResults });
    }

    return messages;
}
````

    </Tab>

    <Tab title="Go">
    
````go
// samplingLoop menjalankan loop agen computer-use hingga Claude berhenti
// meminta alat atau batas iterasi tercapai.
func samplingLoop(ctx context.Context, model anthropic.Model, messages []anthropic.BetaMessageParam, maxIterations int) ([]anthropic.BetaMessageParam, error) {
	for range maxIterations {
		response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
			Model:     model,
			MaxTokens: 4096,
			Messages:  messages,
			Tools:     tools,
			Betas:     []anthropic.AnthropicBeta{"computer-use-2025-11-24"},
		})
		if err != nil {
			return nil, err
		}

		// Tambahkan respons Claude ke riwayat percakapan
		messages = append(messages, response.ToParam())

		// Jalankan alat yang diminta Claude dan kumpulkan hasilnya
		toolResults := processToolCalls(response)
		if len(toolResults) == 0 {
			return messages, nil // No more tool use; task complete
		}

		// Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
		messages = append(messages, anthropic.BetaMessageParam{
			Role:    anthropic.BetaMessageParamRoleUser,
			Content: toolResults,
		})
	}
	return messages, nil
}

````

    </Tab>

    <Tab title="Java">
    
````java
/**
 * Run the computer-use agent loop until Claude stops requesting tools
 * or the iteration limit is reached.
 */
List<BetaMessageParam> samplingLoop(Model model, List<BetaMessageParam> messages, int maxIterations) {
    for (int i = 0; i < maxIterations; i++) {
        BetaMessage response = client.beta().messages().create(MessageCreateParams.builder()
                .model(model)
                .maxTokens(4096)
                .messages(messages)
                .addTool(COMPUTER_TOOL)
                .addBeta("computer-use-2025-11-24")
                .build());

        // Tambahkan respons Claude ke riwayat percakapan
        messages.add(BetaMessageParam.builder()
                .role(BetaMessageParam.Role.ASSISTANT)
                .contentOfBetaContentBlockParams(
                        response.content().stream().map(BetaContentBlock::toParam).toList())
                .build());

        // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
        List<BetaContentBlockParam> toolResults = processToolCalls(response);
        if (toolResults.isEmpty()) {
            return messages; // No more tool use; task complete
        }

        // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
        messages.add(BetaMessageParam.builder()
                .role(BetaMessageParam.Role.USER)
                .contentOfBetaContentBlockParams(toolResults)
                .build());
    }
    return messages;
}
````

    </Tab>

    <Tab title="PHP">
    
````php
/**
 * Run the computer-use agent loop until Claude stops requesting tools
 * or the iteration limit is reached.
 */
function samplingLoop(string $model, array $messages, int $maxIterations = 10): array
{
    global $client, $tools;

    for ($i = 0; $i < $maxIterations; $i++) {
        $response = $client->beta->messages->create(
            model: $model,
            maxTokens: 4096,
            messages: $messages,
            tools: $tools,
            betas: ['computer-use-2025-11-24'],
        );

        // Tambahkan respons Claude ke riwayat percakapan
        $messages[] = BetaMessageParam::with(role: Role::ASSISTANT, content: $response->content);

        // Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
        $toolResults = processToolCalls($response);
        if ($toolResults === []) {
            return $messages; // No more tool use; task complete
        }

        // Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
        $messages[] = BetaMessageParam::with(role: Role::USER, content: $toolResults);
    }

    return $messages;
}
````

    </Tab>

    <Tab title="Ruby">
    
````ruby
# Jalankan loop agen computer-use hingga Claude berhenti meminta alat
# atau batas iterasi tercapai.
def sampling_loop(model, messages, max_iterations: 10)
  max_iterations.times do
    response = CLIENT.beta.messages.create(
      model: model,
      max_tokens: 4096,
      messages: messages,
      tools: TOOLS,
      betas: ["computer-use-2025-11-24"]
    )

    # Tambahkan respons Claude ke riwayat percakapan
    messages << {role: "assistant", content: response.content}

    # Jalankan alat apa pun yang diminta Claude dan kumpulkan hasilnya
    tool_results = process_tool_calls(response)
    return messages if tool_results.empty? # No more tool use; task complete

    # Kirim hasil alat kembali ke Claude untuk iterasi berikutnya
    messages << {role: "user", content: tool_results}
  end

  messages
end
````

    </Tab>
    </Tabs>
  </Step>
</Steps>

#### Menangani error \{#handle-errors}

Saat mengimplementasikan alat computer use, berbagai error mungkin terjadi. Berikut cara menanganinya:

<section title="Kegagalan pengambilan tangkapan layar">

Jika pengambilan tangkapan layar gagal, kembalikan pesan error yang sesuai:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Failed to capture screenshot. Display may be locked or unavailable.",
      "is_error": true
    }
  ]
}
```

</section>

<section title="Koordinat tidak valid">

Jika Claude memberikan koordinat di luar batas tampilan:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Coordinates (1200, 900) are outside display bounds (1024x768).",
      "is_error": true
    }
  ]
}
```

</section>

<section title="Kegagalan eksekusi tindakan">

Jika suatu tindakan gagal dijalankan:

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Failed to perform click action. The application may be unresponsive.",
      "is_error": true
    }
  ]
}
```

</section>

#### Sesuaikan ukuran tangkapan layar agar sesuai batas gambar \{#handle-coordinate-scaling-for-higher-resolutions}

Tangkapan layar yang dikirim ke alat computer harus sudah sesuai dengan batas ukuran gambar Claude (lihat [batas ukuran gambar](/docs/id/build-with-claude/vision#evaluate-image-size)). API tidak mengubah ukuran gambar yang terlalu besar; tangkapan layar yang melebihi batas akan ditolak dengan error validasi HTTP 400.

<Note>
Batas bervariasi menurut model. Claude Opus 4.8 dan Claude Opus 4.7 menerima hingga 2576 piksel pada sisi terpanjang; model sebelumnya menerima hingga 1568 piksel pada sisi terpanjang dan sekitar 1,15 megapiksel total. Contoh berikut menggunakan batas model sebelumnya yaitu 1568 px / 1,15 MP; ganti dengan batas model Anda.
</Note>

Jika layar Anda lebih besar dari batas tersebut, ubah ukuran tangkapan layar sebelum mengirimnya, atur `display_width_px`/`display_height_px` ke dimensi yang telah diubah ukurannya, dan skalakan kembali koordinat yang dikembalikan Claude ke ruang layar asli:

<Tabs>
<Tab title="cURL">
<Info>
Penskalaan koordinat dan pengubahan ukuran tangkapan layar terjadi di kode aplikasi Anda, bukan di permintaan API. Lihat tab SDK untuk pola helper-nya.
</Info>
</Tab>

<Tab title="CLI">
<Info>
Penskalaan koordinat dan pengubahan ukuran tangkapan layar terjadi di kode aplikasi Anda, bukan di permintaan API. Lihat tab SDK untuk pola helper-nya.
</Info>
</Tab>

<Tab title="Python">
```python hidelines={1..7,-2..}
screen_width, screen_height = 1512, 982


def capture_and_resize(w, h): ...
def perform_click(x, y): ...


import math


def get_scale_factor(width, height):
    """Calculate scale factor to meet API constraints."""
    long_edge = max(width, height)
    total_pixels = width * height

    long_edge_scale = 1568 / long_edge
    total_pixels_scale = math.sqrt(1_150_000 / total_pixels)

    return min(1.0, long_edge_scale, total_pixels_scale)


# Saat mengambil tangkapan layar
scale = get_scale_factor(screen_width, screen_height)
scaled_width = int(screen_width * scale)
scaled_height = int(screen_height * scale)

# Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
screenshot = capture_and_resize(scaled_width, scaled_height)


# Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
def execute_click(x, y):
    screen_x = x / scale
    screen_y = y / scale
    perform_click(screen_x, screen_y)


print(f"scale={scale:.6f} scaled={scaled_width}x{scaled_height}")
```
</Tab>

<Tab title="TypeScript">
```typescript hidelines={1..6,-2..}
const screenWidth = 1512;
const screenHeight = 982;
function captureAndResize(w: number, h: number): string {
  return "";
}
function performClick(x: number, y: number): void {}
const MAX_LONG_EDGE = 1568;
const MAX_PIXELS = 1_150_000;

function getScaleFactor(width: number, height: number): number {
  const longEdge = Math.max(width, height);
  const totalPixels = width * height;

  const longEdgeScale = MAX_LONG_EDGE / longEdge;
  const totalPixelsScale = Math.sqrt(MAX_PIXELS / totalPixels);

  return Math.min(1.0, longEdgeScale, totalPixelsScale);
}

// Saat mengambil screenshot
const scale = getScaleFactor(screenWidth, screenHeight);
const scaledWidth = Math.floor(screenWidth * scale);
const scaledHeight = Math.floor(screenHeight * scale);

// Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
const screenshot = captureAndResize(scaledWidth, scaledHeight);

// Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
function executeClick(x: number, y: number): void {
  const screenX = x / scale;
  const screenY = y / scale;
  performClick(screenX, screenY);
}

console.log(`scale=${scale.toFixed(6)} scaled=${scaledWidth}x${scaledHeight}`);
```
</Tab>

<Tab title="C#">
```csharp hidelines={1..5,-2..}
int screenWidth = 1512, screenHeight = 982;

object? CaptureAndResize(int w, int h) => null;
void PerformClick(double x, double y) { }

double GetScaleFactor(int width, int height)
{
    // Hitung faktor skala untuk memenuhi batasan API.
    int longEdge = Math.Max(width, height);
    int totalPixels = width * height;

    double longEdgeScale = 1568.0 / longEdge;
    double totalPixelsScale = Math.Sqrt(1_150_000.0 / totalPixels);

    return Math.Min(1.0, Math.Min(longEdgeScale, totalPixelsScale));
}

// Saat mengambil tangkapan layar
double scale = GetScaleFactor(screenWidth, screenHeight);
int scaledWidth = (int)(screenWidth * scale);
int scaledHeight = (int)(screenHeight * scale);

// Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
var screenshot = CaptureAndResize(scaledWidth, scaledHeight);

// Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
void ExecuteClick(int x, int y)
{
    double screenX = x / scale;
    double screenY = y / scale;
    PerformClick(screenX, screenY);
}

Console.WriteLine($"scale={scale:F6} scaled={scaledWidth}x{scaledHeight}");
```
</Tab>

<Tab title="Go">
```go hidelines={1..10,17..19,-4..}
package main

import (
	"fmt"
	"math"
)

func captureAndResize(w, h int) any { return nil }
func performClick(x, y float64)     {}

func getScaleFactor(width, height int) float64 {
	longest := float64(max(width, height))
	area := float64(width * height)
	return min(1.0, 1568/longest, math.Sqrt(1_150_000/area))
}

func main() {
	screenWidth, screenHeight := 1512, 982

	// Saat mengambil screenshot
	scale := getScaleFactor(screenWidth, screenHeight)
	scaledWidth := int(float64(screenWidth) * scale)
	scaledHeight := int(float64(screenHeight) * scale)

	// Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
	screenshot := captureAndResize(scaledWidth, scaledHeight)

	// Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
	executeClick := func(x, y int) {
		performClick(float64(x)/scale, float64(y)/scale)
	}

	_, _ = screenshot, executeClick
	fmt.Printf("scale=%.6f scaled=%dx%d\n", scale, scaledWidth, scaledHeight)
}
```
</Tab>

<Tab title="Java">
```java hidelines={1..5,17..18,30..31}
import java.util.function.BiConsumer;

static Object captureAndResize(int w, int h) { return null; }
static void performClick(double x, double y) {}

static double getScaleFactor(int width, int height) {
    return Math.min(
        1.0,
        Math.min(
            1568.0 / Math.max(width, height),
            Math.sqrt(1_150_000.0 / (width * height))
        )
    );
}

void main() {
    int screenWidth = 1512, screenHeight = 982;

    // Saat mengambil screenshot
    double scale = getScaleFactor(screenWidth, screenHeight);
    int scaledWidth = (int)(screenWidth * scale);
    int scaledHeight = (int)(screenHeight * scale);

    // Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
    var screenshot = captureAndResize(scaledWidth, scaledHeight);

    // Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
    BiConsumer<Integer, Integer> executeClick =
        (x, y) -> performClick(x / scale, y / scale);

    IO.println("scale=%.6f scaled=%dx%d".formatted(scale, scaledWidth, scaledHeight));
}
```
</Tab>

<Tab title="PHP">
```php hidelines={1..5,14..17,-2..}
<?php

function captureAndResize(int $w, int $h): mixed { return null; }
function performClick(float $x, float $y): void {}

function getScaleFactor(int $width, int $height): float
{
    return min(
        1.0,
        1568 / max($width, $height),
        sqrt(1_150_000 / ($width * $height)),
    );
}

$screenWidth = 1512;
$screenHeight = 982;

// Saat mengambil tangkapan layar
$scale = getScaleFactor($screenWidth, $screenHeight);
$scaledWidth = (int)($screenWidth * $scale);
$scaledHeight = (int)($screenHeight * $scale);

// Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
$screenshot = captureAndResize($scaledWidth, $scaledHeight);

// Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
$executeClick = fn(int $x, int $y) => performClick($x / $scale, $y / $scale);

printf("scale=%.6f scaled=%dx%d\n", $scale, $scaledWidth, $scaledHeight);
```
</Tab>

<Tab title="Ruby">
```ruby hidelines={1..3,7..9,-2..}
def capture_and_resize(w, h) = nil
def perform_click(x, y) = nil

def get_scale_factor(width, height)
  [1.0, 1568.0 / [width, height].max, Math.sqrt(1_150_000.0 / (width * height))].min
end

screen_width, screen_height = 1512, 982

# Saat mengambil tangkapan layar
scale = get_scale_factor(screen_width, screen_height)
scaled_width = (screen_width * scale).to_i
scaled_height = (screen_height * scale).to_i

# Ubah ukuran gambar ke dimensi yang diskalakan sebelum mengirim ke Claude
screenshot = capture_and_resize(scaled_width, scaled_height)

# Saat menangani koordinat dari Claude, skalakan kembali ke ukuran asli
execute_click = ->(x, y) { perform_click(x / scale, y / scale) }

puts format("scale=%.6f scaled=%dx%d", scale, scaled_width, scaled_height)
```
</Tab>
</Tabs>

<Note>
**Layar Retina macOS** menangkap tangkapan layar pada rasio piksel perangkat 2, sehingga gambar memiliki resolusi dua kali lipat dari koordinat layar logis. Perkecil tangkapan layar sebesar 2x sebelum mengirim, atau bagi dua koordinat yang dikembalikan Claude sebelum melakukan klik.
</Note>

#### Mendiagnosis masalah klik \{#diagnose-click-issues}

Jika klik meleset dari targetnya, penyebabnya biasanya salah satu dari berikut:

| Gejala | Kemungkinan penyebab | Coba |
|---------|--------------|-----|
| Klik secara konsisten bergeser ke satu arah | `display_width_px`/`display_height_px` tidak cocok dengan dimensi gambar yang sebenarnya dikirim | Pastikan dimensi tampilan persis cocok dengan tangkapan layar yang Anda kirim |
| Klik mendarat di area yang benar tetapi meleset dari target | Target sangat kecil, detail hilang saat memperkecil sumber 4K+, atau rasio aspek terdistorsi | Atur `enable_zoom: true`; tangkap pada DPI lebih rendah atau potong ke wilayah yang relevan; pertahankan rasio aspek saat mengubah ukuran |
| Claude mengklik elemen yang sepenuhnya salah | Instruksi ambigu, atau ada elemen yang secara visual mirip di dekatnya | Gunakan prompt posisional ("tombol Submit biru di kanan bawah"); pecah interaksi menjadi langkah-langkah yang lebih kecil |
| Akurasi secara konsisten buruk | Resolusi terlalu rendah | Coba 1280x720 sebagai baseline |

<Tip>
**Pilihan model memengaruhi presisi klik.** Claude Sonnet 4.6 secara mekanis lebih presisi dalam mengklik dibandingkan Claude Opus 4.6 dan lebih tangguh ketika tangkapan layar memerlukan pengecilan yang signifikan. Claude Opus 4.7 mempersempit kesenjangan tersebut: presisi kliknya kurang lebih sebanding dengan Sonnet 4.6, dan batas resolusinya yang lebih tinggi berarti lebih sedikit pengecilan yang diperlukan.
</Tip>

#### Ikuti praktik terbaik implementasi \{#follow-implementation-best-practices}

<section title="Gunakan resolusi tampilan yang sesuai">

Atur dimensi tampilan yang sesuai dengan kasus penggunaan Anda sambil tetap dalam batas yang direkomendasikan:
- Untuk tugas desktop umum: 1024x768 atau 1280x720
- Untuk aplikasi web: 1280x800 atau 1366x768
- Hindari resolusi di atas 1920x1080 untuk mencegah masalah performa

</section>

<section title="Implementasikan penanganan tangkapan layar yang tepat">

Saat mengembalikan tangkapan layar ke Claude:
- Encode tangkapan layar sebagai PNG atau JPEG base64
- Pertimbangkan untuk mengompresi tangkapan layar besar untuk meningkatkan performa
- Sertakan metadata yang relevan seperti timestamp atau status tampilan
- Jika menggunakan resolusi lebih tinggi, pastikan koordinat diskalakan secara akurat

</section>

<section title="Kelola riwayat tangkapan layar untuk caching prompt">

Agent loop yang panjang mengakumulasi tangkapan layar dengan cepat (sekitar 1.000–1.800 token input masing-masing). Agar [Caching prompt](/docs/id/build-with-claude/prompt-caching) tetap efektif sambil membatasi konteks:
- Tempatkan satu breakpoint `cache_control` setelah prompt sistem dan definisi alat, dan hingga tiga lagi pada blok `tool_result` terbaru, memajukannya setiap giliran.
- Pangkas tangkapan layar lama dalam *batch*, bukan satu per giliran. Menghapus satu tangkapan layar setiap giliran mengubah prefix setiap giliran dan membatalkan cache. Default yang wajar adalah menyimpan tiga tangkapan layar terakhir dan memangkas setiap 25 giliran, sehingga prefix tetap identik byte demi byte di antara peristiwa pemangkasan.

</section>

<section title="Tambahkan jeda tindakan">

Beberapa aplikasi memerlukan waktu untuk merespons tindakan:
<Tabs>
<Tab title="cURL">
<Info>
Ini adalah kode helper sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk polanya.
</Info>
</Tab>

<Tab title="CLI">
<Info>
Ini adalah kode helper sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk polanya.
</Info>
</Tab>

<Tab title="Python">
```python hidelines={1..4,-3..}
import time


def click_at(x, y): ...
def click_and_wait(x, y, wait_time=0.5):
    click_at(x, y)
    time.sleep(wait_time)  # Allow UI to update


print("ok")
```
</Tab>

<Tab title="TypeScript">
```typescript hidelines={1..4,-3..}
import { setTimeout } from "node:timers/promises";

function clickAt(x: number, y: number): void {}

async function clickAndWait(x: number, y: number, waitMs = 500): Promise<void> {
  clickAt(x, y);
  await setTimeout(waitMs); // Allow UI to update
}

await clickAndWait(100, 200);
console.log("ok");
```
</Tab>

<Tab title="C#">
```csharp hidelines={1..5}
ClickAndWait(100, 200);
Console.WriteLine("ok");

static void ClickAt(int x, int y) { }

static void ClickAndWait(int x, int y, double waitSeconds = 0.5)
{
    ClickAt(x, y);
    Thread.Sleep(TimeSpan.FromSeconds(waitSeconds));  // Allow UI to update
}
```
</Tab>

<Tab title="Go">
```go hidelines={1..9,-4..}
package main

import (
	"fmt"
	"time"
)

func clickAt(x, y int) {}

func clickAndWaitFor(x, y int, wait time.Duration) {
	clickAt(x, y)
	time.Sleep(wait) // Allow UI to update
}

func clickAndWait(x, y int) {
	clickAndWaitFor(x, y, 500*time.Millisecond)
}

func main() {
	fmt.Println("ok")
}
```
</Tab>

<Tab title="Java">
```java hidelines={1..2,-4..}
void clickAt(int x, int y) {}

void clickAndWait(int x, int y) throws InterruptedException {
    clickAndWait(x, y, 500);
}

void clickAndWait(int x, int y, long waitTimeMillis) throws InterruptedException {
    clickAt(x, y);
    Thread.sleep(waitTimeMillis);  // Allow UI to update
}

void main() {
    IO.println("ok");
}
```
</Tab>

<Tab title="PHP">
```php hidelines={1..4,-2..}
<?php

function clickAt(int $x, int $y): void {}

function clickAndWait(int $x, int $y, float $waitSeconds = 0.5): void
{
    clickAt($x, $y);
    usleep((int) ($waitSeconds * 1_000_000));  // Allow UI to update
}

echo "ok\n";
```
</Tab>

<Tab title="Ruby">
```ruby hidelines={1..2,-2..}
def click_at(x, y) = nil

def click_and_wait(x, y, wait_time: 0.5)
  click_at(x, y)
  sleep(wait_time) # Allow UI to update
end

puts "ok"
```
</Tab>
</Tabs>

</section>

<section title="Validasi tindakan sebelum menjalankannya">

Periksa bahwa tindakan yang diminta aman dan valid:
<Tabs>
<Tab title="cURL">
<Info>
Ini adalah kode helper sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk polanya.
</Info>
</Tab>

<Tab title="CLI">
<Info>
Ini adalah kode helper sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk polanya.
</Info>
</Tab>

<Tab title="Python">
```python hidelines={1,-3..}
display_width, display_height = 1024, 768


def validate_action(action_type, params):
    if action_type == "left_click":
        x, y = params.get("coordinate", (0, 0))
        if not (0 <= x < display_width and 0 <= y < display_height):
            return False, "Coordinates out of bounds"
    return True, None


print(validate_action("left_click", {"coordinate": (2000, 100)}))
```
</Tab>

<Tab title="TypeScript">
```typescript hidelines={1..3,-2..}
const displayWidth = 1024;
const displayHeight = 768;

interface ActionParams {
  coordinate?: [number, number];
}

function validateAction(actionType: string, params: ActionParams): [boolean, string | null] {
  if (actionType === "left_click") {
    const [x, y] = params.coordinate ?? [0, 0];
    if (!(x >= 0 && x < displayWidth && y >= 0 && y < displayHeight)) {
      return [false, "Coordinates out of bounds"];
    }
  }
  return [true, null];
}

console.log(validateAction("left_click", { coordinate: [2000, 100] }));
```
</Tab>

<Tab title="C#">
```csharp hidelines={1..2,5..7}
using System.Text.Json;

const int DisplayWidth = 1024;
const int DisplayHeight = 768;

Console.WriteLine(ValidateAction("left_click", new Dictionary<string, JsonElement> { ["coordinate"] = JsonSerializer.SerializeToElement(new[] { 2000, 100 }) }));

static (bool IsValid, string? Error) ValidateAction(string actionType, IReadOnlyDictionary<string, JsonElement> parameters)
{
    if (actionType == "left_click")
    {
        int x = parameters["coordinate"][0].GetInt32();
        int y = parameters["coordinate"][1].GetInt32();
        if (x is < 0 or >= DisplayWidth || y is < 0 or >= DisplayHeight)
        {
            return (false, "Coordinates out of bounds");
        }
    }
    return (true, null);
}
```
</Tab>

<Tab title="Go">
```go hidelines={1..4,-5..}
package main

import "fmt"

const (
	displayWidth  = 1024
	displayHeight = 768
)

func validateAction(actionType string, params map[string]any) (bool, string) {
	if actionType == "left_click" {
		coord, ok := params["coordinate"].([]any)
		if !ok || len(coord) != 2 {
			return false, "Invalid coordinate"
		}
		x, y := int(coord[0].(float64)), int(coord[1].(float64))
		if !(0 <= x && x < displayWidth && 0 <= y && y < displayHeight) {
			return false, "Coordinates out of bounds"
		}
	}
	return true, ""
}

func main() {
	ok, msg := validateAction("left_click", map[string]any{"coordinate": []any{2000.0, 100.0}})
	fmt.Println(ok, msg)
}
```
</Tab>

<Tab title="Java">
```java hidelines={1..2,-4..}
import com.anthropic.core.JsonValue;

static final int DISPLAY_WIDTH = 1024;
static final int DISPLAY_HEIGHT = 768;

record Validation(boolean valid, String error) {}

Validation validateAction(String actionType, Map<String, JsonValue> params) {
    if (actionType.equals("left_click")) {
        List<JsonValue> coord = (List<JsonValue>) params.get("coordinate").asArray().get();
        long x = ((Number) coord.get(0).asNumber().get()).longValue();
        long y = ((Number) coord.get(1).asNumber().get()).longValue();
        if (!(0 <= x && x < DISPLAY_WIDTH && 0 <= y && y < DISPLAY_HEIGHT)) {
            return new Validation(false, "Coordinates out of bounds");
        }
    }
    return new Validation(true, null);
}

void main() {
    IO.println(validateAction("left_click", Map.of("coordinate", JsonValue.from(List.of(2000, 100)))));
}
```
</Tab>

<Tab title="PHP">
```php hidelines={1..2,-3..}
<?php

const DISPLAY_WIDTH = 1024;
const DISPLAY_HEIGHT = 768;

/** @return array{bool, ?string} */
function validateAction(string $actionType, array $params): array
{
    if ($actionType === 'left_click') {
        [$x, $y] = $params['coordinate'] ?? [0, 0];
        if (!(0 <= $x && $x < DISPLAY_WIDTH && 0 <= $y && $y < DISPLAY_HEIGHT)) {
            return [false, 'Coordinates out of bounds'];
        }
    }
    return [true, null];
}

[$valid, $error] = validateAction('left_click', ['coordinate' => [2000, 100]]);
echo ($valid ? 'true' : 'false') . ' ' . $error . "\n";
```
</Tab>

<Tab title="Ruby">
```ruby hidelines={-2..}
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768

def validate_action(action_type, params)
  if action_type == "left_click"
    x, y = params.fetch(:coordinate, [0, 0])
    unless (0...DISPLAY_WIDTH).cover?(x) && (0...DISPLAY_HEIGHT).cover?(y)
      return [false, "Coordinates out of bounds"]
    end
  end
  [true, nil]
end

p validate_action("left_click", {coordinate: [2000, 100]})
```
</Tab>
</Tabs>

</section>

<section title="Catat tindakan untuk debugging">

Simpan log semua tindakan untuk pemecahan masalah:
<Tabs>
<Tab title="cURL">
<Info>
Ini adalah kode helper sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk polanya.
</Info>
</Tab>

<Tab title="CLI">
<Info>
Ini adalah kode helper sisi aplikasi tanpa permintaan API. Lihat tab SDK untuk polanya.
</Info>
</Tab>

<Tab title="Python">
```python hidelines={-3..}
import logging


def log_action(action_type, params, result):
    logging.info(f"Action: {action_type}, Params: {params}, Result: {result}")


print("ok")
```
</Tab>

<Tab title="TypeScript">
```typescript hidelines={-2..}
function logAction(actionType: string, params: unknown, result: unknown): void {
  console.error(
    `Action: ${actionType}, Params: ${JSON.stringify(params)}, Result: ${JSON.stringify(
      result
    )}`
  );
}

console.log("ok");
```
</Tab>

<Tab title="C#">
```csharp hidelines={1..3}
LogAction("screenshot", null, "<image data>");
Console.WriteLine("ok");

static void LogAction(string actionType, object? parameters, object? result)
{
    Console.Error.WriteLine($"Action: {actionType}, Params: {parameters}, Result: {result}");
}
```
</Tab>

<Tab title="Go">
```go hidelines={1..7,-4..}
package main

import (
	"fmt"
	"log"
)

func logAction(actionType string, params map[string]any, result any) {
	log.Printf("Action: %s, Params: %v, Result: %v", actionType, params, result)
}

func main() {
	fmt.Println("ok")
}
```
</Tab>

<Tab title="Java">
```java hidelines={-4..}
import static java.lang.System.Logger.Level.INFO;

static final System.Logger LOGGER = System.getLogger("computer-use");

void logAction(String actionType, Object params, Object result) {
    LOGGER.log(INFO, "Action: {0}, Params: {1}, Result: {2}", actionType, params, result);
}

void main() {
    IO.println("ok");
}
```
</Tab>

<Tab title="PHP">
```php hidelines={1..2,-2..}
<?php

function logAction(string $actionType, array $params, mixed $result): void
{
    error_log(sprintf(
        'Action: %s, Params: %s, Result: %s',
        $actionType,
        json_encode($params),
        json_encode($result),
    ));
}

echo "ok\n";
```
</Tab>

<Tab title="Ruby">
```ruby hidelines={-2..}
require "logger"

LOGGER = Logger.new($stderr)

def log_action(action_type, params, result)
  LOGGER.info("Action: #{action_type}, Params: #{params}, Result: #{result}")
end

puts "ok"
```
</Tab>
</Tabs>

</section>

---

## Memahami keterbatasan computer use \{#understand-computer-use-limitations}

Fungsionalitas "computer use" (penggunaan komputer) masih dalam tahap beta. Meskipun kemampuan Claude sudah sangat canggih, pengembang harus menyadari keterbatasannya:

1. **Latency:** "Latency" (latensi) computer use saat ini untuk interaksi manusia-AI mungkin terlalu lambat dibandingkan dengan tindakan komputer biasa yang diarahkan manusia. Fokuslah pada kasus penggunaan di mana kecepatan tidak kritis (misalnya, pengumpulan informasi di latar belakang, pengujian perangkat lunak otomatis) dalam lingkungan tepercaya.
2. **Akurasi dan keandalan computer vision:** Claude mungkin membuat kesalahan atau berhalusinasi saat menghasilkan koordinat spesifik ketika membuat tindakan. Pemikiran diperpanjang dapat membantu Anda memahami penalaran model dan mengidentifikasi potensi masalah.
3. **Akurasi dan keandalan pemilihan alat:** Claude mungkin membuat kesalahan atau berhalusinasi saat memilih alat ketika menghasilkan tindakan, atau mengambil tindakan yang tidak terduga untuk menyelesaikan masalah. Selain itu, keandalan mungkin lebih rendah saat berinteraksi dengan aplikasi khusus atau beberapa aplikasi sekaligus. Berikan prompt kepada model dengan hati-hati saat meminta tugas yang kompleks.
4. **Keandalan scrolling:** Tindakan scroll mendukung kontrol arah (atas, bawah, kiri, kanan) dan jumlah yang ditentukan. Dalam aplikasi di mana scrolling tidak berfungsi, alternatif keyboard seperti Page Down dapat membantu.
5. **Interaksi spreadsheet:** Gunakan tindakan kontrol mouse yang lebih presisi (`left_mouse_down`, `left_mouse_up`) dan kombinasi tombol modifier untuk memilih sel individual. Operasi spreadsheet yang kompleks mungkin masih memerlukan beberapa kali percobaan.
6. **Pembuatan akun dan pembuatan konten di platform sosial dan komunikasi:** Meskipun Claude akan mengunjungi situs web, kemampuan Claude untuk membuat akun atau menghasilkan dan membagikan konten atau terlibat dalam peniruan identitas manusia di seluruh situs web dan platform media sosial dibatasi. Kemampuan ini mungkin diperbarui di masa mendatang.
7. **Kerentanan:** Kerentanan seperti jailbreaking atau prompt injection mungkin tetap ada di seluruh sistem AI terdepan, termasuk API computer use beta. Dalam beberapa keadaan, Claude akan mengikuti perintah yang ditemukan dalam konten, terkadang bahkan bertentangan dengan instruksi pengguna. Misalnya, instruksi untuk Claude di halaman web atau yang terdapat dalam gambar mungkin menimpa instruksi atau menyebabkan Claude membuat kesalahan. Pertimbangkan hal-hal berikut:
   a. Membatasi computer use pada lingkungan tepercaya seperti mesin virtual atau container dengan hak akses minimal
   b. Menghindari memberikan akses computer use ke akun atau data sensitif tanpa pengawasan ketat
   c. Menginformasikan pengguna akhir tentang risiko yang relevan dan mendapatkan persetujuan mereka sebelum mengaktifkan atau meminta izin yang diperlukan untuk fitur computer use dalam aplikasi Anda
8. **Tindakan yang tidak pantas atau ilegal:** Berdasarkan Ketentuan Layanan Anthropic, Anda tidak boleh menggunakan computer use untuk melanggar hukum apa pun atau Kebijakan Penggunaan yang Dapat Diterima.

Selalu tinjau dan verifikasi dengan cermat tindakan dan log computer use Claude. Jangan gunakan Claude untuk tugas yang memerlukan presisi sempurna atau informasi pengguna yang sensitif tanpa pengawasan manusia.

## Retensi data \{#data-retention}

Computer use adalah alat sisi klien. Semua tangkapan layar, tindakan mouse, input keyboard, dan file apa pun yang terlibat dalam sesi ditangkap dan disimpan di lingkungan Anda, bukan oleh Anthropic. Anthropic memproses gambar tangkapan layar dan permintaan tindakan secara real time sebagai bagian dari panggilan API tetapi tidak menyimpannya setelah respons dikembalikan.

Karena aplikasi Anda mengontrol di mana dan bagaimana data computer use disimpan, computer use memenuhi syarat ZDR. Untuk kelayakan ZDR di seluruh fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Harga \{#pricing}

Computer use mengikuti [harga penggunaan alat](/docs/id/agents-and-tools/tool-use/overview#pricing) standar. Saat menggunakan alat computer use:

**Overhead prompt sistem**: Beta computer use menambahkan 466-499 token ke prompt sistem

**Penggunaan token alat computer use**:
| Model | Token input per definisi alat |
| ----- | -------------------------------- |
| Model Claude 4.x | 735 token |

**Konsumsi token tambahan**:
- Gambar tangkapan layar (lihat [Harga Vision](/docs/id/build-with-claude/vision))
- Hasil eksekusi alat yang dikembalikan ke Claude

<Note>
Jika Anda juga menggunakan alat bash atau text editor bersamaan dengan computer use, alat-alat tersebut memiliki biaya token tersendiri sebagaimana didokumentasikan di halaman masing-masing.
</Note>

## Langkah selanjutnya \{#next-steps}

<CardGroup cols={2}>
  <Card
    title="Alat editor teks"
    icon="file"
    href="/docs/id/agents-and-tools/tool-use/text-editor-tool"
  >
    Lanjutkan ke alat berikutnya: lihat, buat, dan edit file dengan Claude
  </Card>
  <Card
    title="Implementasi referensi"
    icon="github-logo"
    href="https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo"
  >
    Mulai dengan implementasi lengkap berbasis Docker
  </Card>
  <Card
    title="Dokumentasi alat"
    icon="tool"
    href="/docs/id/agents-and-tools/tool-use/overview"
  >
    Pelajari lebih lanjut tentang penggunaan alat dan pembuatan alat kustom
  </Card>
  <Card
    title="Praktik terbaik secara detail"
    icon="book-open"
    href="https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude"
  >
    Rekomendasi yang telah diuji untuk resolusi, upaya pemikiran, dan manajemen konteks
  </Card>
</CardGroup>