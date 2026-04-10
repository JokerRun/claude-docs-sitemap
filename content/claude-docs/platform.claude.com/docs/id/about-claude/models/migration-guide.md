---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/migration-guide
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 51eb7decc5e94f27f9ede8e475c1804e11b57b764f69267c76c625e37a8a2710
---

# Panduan migrasi

Panduan untuk migrasi ke model Claude 4.6 dari versi Claude sebelumnya

---

<Note>
Panduan ini mencakup migrasi kode [Messages API](/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](/docs/id/managed-agents/overview), lihat [Migrasi antar versi model](/docs/id/managed-agents/migration#migrating-between-model-versions). Runtime Managed Agents menangani sebagian besar perubahan bentuk permintaan yang dijelaskan di sini.
</Note>

## Migrasi ke Claude 4.6

Claude Opus 4.6 adalah pengganti yang hampir drop-in untuk Claude 4.5, dengan beberapa perubahan yang merusak untuk diperhatikan. Untuk daftar lengkap fitur baru, lihat [Yang baru di Claude 4.6](/docs/id/about-claude/models/whats-new-claude-4-6).

### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-5"  # Sebelum
model = "claude-opus-4-6"  # Sesudah
```

### Perubahan yang merusak

1. **Penghapusan prefill:** Prefilling pesan asisten mengembalikan kesalahan 400 pada model Claude 4.6. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs), instruksi system prompt, atau `output_config.format` sebagai gantinya.

2. **Penawaran parameter tool:** Model Claude 4.6 mungkin menghasilkan escape string JSON yang sedikit berbeda dalam argumen panggilan tool (misalnya, penanganan escape Unicode atau escape forward slash yang berbeda). Jika Anda mengurai `input` panggilan tool sebagai string mentah daripada menggunakan parser JSON, verifikasi logika parsing Anda. Parser JSON standar (seperti `json.loads()` atau `JSON.parse()`) menangani perbedaan ini secara otomatis.

### Perubahan yang direkomendasikan

Ini tidak diperlukan tetapi akan meningkatkan pengalaman Anda:

1. **Migrasi ke adaptive thinking:** `thinking: {type: "enabled", budget_tokens: N}` sudah usang pada model Claude 4.6 dan akan dihapus dalam rilis model di masa depan. Beralih ke `thinking: {type: "adaptive"}` dan gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking. Lihat [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking).

   <CodeGroup>
   
   ```python Before nocheck
   response = client.beta.messages.create(
       model="claude-opus-4-5",
       max_tokens=16000,
       thinking={"type": "enabled", "budget_tokens": 32000},
       betas=["interleaved-thinking-2025-05-14"],
       messages=[...],
   )
   ```

   ```python After
   response = client.messages.create(
       model="claude-opus-4-6",
       max_tokens=16000,
       thinking={"type": "adaptive"},
       output_config={"effort": "high"},
       messages=[{"role": "user", "content": "Your prompt here"}],
   )
   ```

   ```bash CLI
   ant messages create <<'YAML'
   model: claude-opus-4-6
   max_tokens: 16000
   thinking:
     type: adaptive
   output_config:
     effort: high
   messages:
     - role: user
       content: Your prompt here
   YAML
   ```

   ```typescript TypeScript hidelines={1..2}
   import Anthropic from "@anthropic-ai/sdk";

   const client = new Anthropic();

   const response = await client.messages.create({
     model: "claude-opus-4-6",
     max_tokens: 16000,
     thinking: { type: "adaptive" },
     output_config: { effort: "high" },
     messages: [{ role: "user", content: "Your prompt here" }]
   } as unknown as Anthropic.MessageCreateParamsNonStreaming);
   ```

   ```csharp C#
   using Anthropic;
   using Anthropic.Models.Messages;

   public class Program
   {
       public static async Task Main(string[] args)
       {
           AnthropicClient client = new();

           var parameters = new MessageCreateParams
           {
               Model = Model.ClaudeOpus4_6,
               MaxTokens = 16000,
               Thinking = new ThinkingConfigAdaptive(),
               OutputConfig = new OutputConfig { Effort = Effort.High },
               Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
           };

           var response = await client.Messages.Create(parameters);
           Console.WriteLine(response);
       }
   }
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

   	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
   		Model:     anthropic.ModelClaudeOpus4_6,
   		MaxTokens: 16000,
   		Thinking: anthropic.ThinkingConfigParamUnion{
   			OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
   		},
   		OutputConfig: anthropic.OutputConfigParam{
   			Effort: anthropic.OutputConfigEffortHigh,
   		},
   		Messages: []anthropic.MessageParam{
   			anthropic.NewUserMessage(anthropic.NewTextBlock("Your prompt here")),
   		},
   	})
   	if err != nil {
   		log.Fatal(err)
   	}
   	fmt.Println(response)
   }
   ```

   ```java Java hidelines={1..5,8..10,-2..}
   import com.anthropic.client.AnthropicClient;
   import com.anthropic.client.okhttp.AnthropicOkHttpClient;
   import com.anthropic.models.messages.MessageCreateParams;
   import com.anthropic.models.messages.Message;
   import com.anthropic.models.messages.Model;
   import com.anthropic.models.messages.OutputConfig;
   import com.anthropic.models.messages.ThinkingConfigAdaptive;

   public class AdaptiveThinkingExample {
       public static void main(String[] args) {
           AnthropicClient client = AnthropicOkHttpClient.fromEnv();

           MessageCreateParams params = MessageCreateParams.builder()
               .model(Model.CLAUDE_OPUS_4_6)
               .maxTokens(16000L)
               .thinking(ThinkingConfigAdaptive.builder().build())
               .outputConfig(OutputConfig.builder()
                   .effort(OutputConfig.Effort.HIGH)
                   .build())
               .addUserMessage("Your prompt here")
               .build();

           Message response = client.messages().create(params);
           System.out.println(response);
       }
   }
   ```

   ```php PHP hidelines={1..4}
   <?php

   use Anthropic\Client;

   $client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

   $response = $client->messages->create(
       maxTokens: 16000,
       messages: [['role' => 'user', 'content' => 'Your prompt here']],
       model: 'claude-opus-4-6',
       thinking: ['type' => 'adaptive'],
       outputConfig: ['effort' => 'high'],
   );
   ```

   ```ruby Ruby hidelines={1..2}
   require "anthropic"

   client = Anthropic::Client.new

   response = client.messages.create(
     model: "claude-opus-4-6",
     max_tokens: 16000,
     thinking: { type: "adaptive" },
     output_config: { effort: "high" },
     messages: [{ role: "user", content: "Your prompt here" }]
   )
   ```
   </CodeGroup>

   Perhatikan bahwa migrasi juga bergerak dari `client.beta.messages.create` ke `client.messages.create`. Adaptive thinking dan effort adalah fitur GA dan tidak memerlukan namespace SDK beta atau header beta apa pun.

2. **Hapus header beta effort:** Parameter effort sekarang GA. Hapus `betas=["effort-2025-11-24"]` dari permintaan Anda.

3. **Hapus header beta fine-grained tool streaming:** Fine-grained tool streaming sekarang GA. Hapus `betas=["fine-grained-tool-streaming-2025-05-14"]` dari permintaan Anda.

4. **Hapus header beta interleaved thinking:** Adaptive thinking secara otomatis mengaktifkan interleaved thinking pada Opus 4.6 dan Sonnet 4.6. Hapus `betas=["interleaved-thinking-2025-05-14"]` dari permintaan Anda. Header masih berfungsi pada Sonnet 4.6 dengan extended thinking manual, tetapi mode manual sudah usang.

5. **Migrasi ke output_config.format:** Jika menggunakan structured outputs, perbarui `output_format={...}` ke `output_config={"format": {...}}`. Parameter lama tetap berfungsi tetapi sudah usang dan akan dihapus dalam rilis model di masa depan.

### Migrasi dari Claude 4.1 atau lebih awal ke Claude 4.6

Jika Anda bermigrasi dari Opus 4.1, Sonnet 4, atau model sebelumnya langsung ke Claude 4.6, terapkan perubahan yang merusak Claude 4.6 di atas ditambah perubahan tambahan di bagian ini.

```python
# Dari Opus 4.1
model = "claude-opus-4-1-20250805"  # Sebelum
model = "claude-opus-4-6"  # Sesudah

# Dari Sonnet 4
model = "claude-sonnet-4-20250514"  # Sebelum
model = "claude-opus-4-6"  # Sesudah

# Dari Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Sebelum
model = "claude-opus-4-6"  # Sesudah
```

#### Perubahan yang merusak tambahan

1. **Perbarui parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya:

   
   ```python Python nocheck
   # Sebelum - Ini akan error pada model Claude 4+
   response = client.messages.create(
       model="claude-3-7-sonnet-20250219",
       temperature=0.7,
       top_p=0.9,  # Tidak dapat menggunakan keduanya
       # ...
   )

   # Sesudah
   response = client.messages.create(
       model="claude-opus-4-6",
       temperature=0.7,  # Gunakan temperature ATAU top_p, bukan keduanya
       # ...
   )
   ```

2. **Perbarui versi tool**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi tool terbaru. Hapus kode apa pun yang menggunakan perintah `undo_edit`.

   ```python
   # Sebelum
   tools = [{"type": "text_editor_20250124", "name": "str_replace_editor"}]

   # Sesudah
   tools = [{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
   ```

   - **Text editor:** Gunakan `text_editor_20250728` dan `str_replace_based_edit_tool`. Lihat [dokumentasi tool text editor](/docs/id/agents-and-tools/tool-use/text-editor-tool) untuk detail.
   - **Code execution:** Upgrade ke `code_execution_20250825`. Lihat [dokumentasi tool code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) untuk instruksi migrasi.

3. **Tangani alasan stop `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan stop `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals):

   
   ```python Python nocheck
   response = client.messages.create(...)

   if response.stop_reason == "refusal":
       # Tangani penolakan dengan tepat
       pass
   ```

4. **Tangani alasan stop `model_context_window_exceeded`**

   Model Claude 4.5+ mengembalikan alasan stop `model_context_window_exceeded` ketika generasi berhenti karena mencapai batas jendela konteks, bukan batas `max_tokens` yang diminta. Perbarui aplikasi Anda untuk menangani alasan stop baru ini:

   
   ```python Python nocheck
   response = client.messages.create(...)

   if response.stop_reason == "model_context_window_exceeded":
       # Tangani batas jendela konteks dengan tepat
       pass
   ```

5. **Verifikasi penanganan parameter tool (trailing newlines)**

   Model Claude 4.5+ mempertahankan trailing newlines dalam parameter string panggilan tool yang sebelumnya dihapus. Jika tool Anda mengandalkan pencocokan string yang tepat terhadap parameter panggilan tool, verifikasi logika Anda menangani trailing newlines dengan benar.

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4+ memiliki gaya komunikasi yang lebih ringkas dan langsung serta memerlukan arahan eksplisit. Tinjau [best practices prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

#### Perubahan yang direkomendasikan tambahan

- **Hapus header beta legacy:** Hapus `token-efficient-tools-2025-02-19` dan `output-128k-2025-02-19`. Semua model Claude 4+ memiliki penggunaan tool yang efisien token bawaan dan header ini tidak berpengaruh.

### Daftar periksa migrasi Claude 4.6

- [ ] Perbarui ID model ke `claude-opus-4-6`
- [ ] **BREAKING:** Hapus prefill pesan asisten (mengembalikan kesalahan 400); gunakan structured outputs atau `output_config.format` sebagai gantinya
- [ ] **Recommended:** Migrasi dari `thinking: {type: "enabled", budget_tokens: N}` ke `thinking: {type: "adaptive"}` dengan [parameter effort](/docs/id/build-with-claude/effort) (`budget_tokens` sudah usang dan akan dihapus dalam rilis di masa depan)
- [ ] Verifikasi parsing JSON panggilan tool menggunakan parser JSON standar
- [ ] Hapus header beta `effort-2025-11-24` (effort sekarang GA)
- [ ] Hapus header beta `fine-grained-tool-streaming-2025-05-14`
- [ ] Hapus header beta `interleaved-thinking-2025-05-14` (adaptive thinking mengaktifkan interleaved thinking secara otomatis)
- [ ] Migrasi `output_format` ke `output_config.format` (jika berlaku)
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: perbarui versi tool (`text_editor_20250728`, `code_execution_20250825`)
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: tangani alasan stop `refusal`
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: tangani alasan stop `model_context_window_exceeded`
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: verifikasi penanganan parameter string tool untuk trailing newlines
- [ ] Jika bermigrasi dari Claude 4.1 atau lebih awal: hapus header beta legacy (`token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`)
- [ ] Tinjau dan perbarui prompt mengikuti [best practices prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Uji di lingkungan pengembangan sebelum deployment produksi

---

## Migrasi ke Claude Sonnet 4.6

Claude Sonnet 4.6 menggabungkan intelijen yang kuat dengan kinerja cepat, menampilkan kemampuan pencarian agentic yang ditingkatkan dan eksekusi kode gratis saat digunakan dengan web search atau web fetch. Ini ideal untuk tugas coding, analisis, dan konten sehari-hari.

Untuk gambaran lengkap kemampuan, lihat [overview model](/docs/id/about-claude/models/overview).

<Note>
Harga Sonnet 4.6 adalah $3 per juta token input, $15 per juta token output. Lihat [Claude pricing](/docs/id/about-claude/pricing) untuk detail.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Sonnet 4.5
model = "claude-sonnet-4-5"  # Sebelum
model = "claude-sonnet-4-6"  # Sesudah

# Dari Sonnet 4
model = "claude-sonnet-4-20250514"  # Sebelum
model = "claude-sonnet-4-6"  # Sesudah
```

### Perubahan yang merusak

#### Saat bermigrasi dari Sonnet 4.5

1. **Prefilling pesan asisten tidak lagi didukung**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari Sonnet 4.5 atau lebih awal.
   </Warning>

   Prefilling pesan asisten mengembalikan kesalahan `400` pada Sonnet 4.6. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs), instruksi system prompt, atau `output_config.format` sebagai gantinya.

   **Kasus penggunaan prefill umum dan migrasi:**

   - **Mengontrol format output** (memaksa output JSON/YAML): Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs) atau tools dengan enum fields untuk tugas klasifikasi.

   - **Menghilangkan preamble** (menghapus frasa "Here is..."): Tambahkan instruksi langsung dalam system prompt: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc."

   - **Menghindari penolakan buruk:** Claude sekarang jauh lebih baik dalam penolakan yang tepat. Prompting yang jelas dalam pesan pengguna tanpa prefill harus cukup.

   - **Continuations** (melanjutkan respons yang terputus): Pindahkan continuation ke pesan pengguna: "Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off."

   - **Context hydration / role consistency** (menyegarkan konteks dalam percakapan panjang): Injeksikan apa yang sebelumnya adalah pengingat prefilled-assistant ke dalam user turn sebagai gantinya.

2. **JSON escaping parameter tool mungkin berbeda**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari Sonnet 4.5 atau lebih awal.
   </Warning>

   Escaping string JSON dalam parameter tool mungkin berbeda dari model sebelumnya. Parser JSON standar menangani ini secara otomatis, tetapi parsing berbasis string kustom mungkin perlu update.

#### Saat bermigrasi dari Claude 3.x

3. **Perbarui parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

4. **Perbarui versi tool**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi tool terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

5. **Tangani alasan stop `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan stop `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [best practices prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Perubahan yang direkomendasikan

1. **Hapus header beta `fine-grained-tool-streaming-2025-05-14`:** Fine-grained tool streaming sekarang GA pada Sonnet 4.6 dan tidak lagi memerlukan header beta.
2. **Migrasi `output_format` ke `output_config.format`:** Parameter `output_format` sudah usang. Gunakan `output_config.format` sebagai gantinya.

### Migrasi dari Sonnet 4.5

Pertimbangkan untuk bermigrasi dari Sonnet 4.5 ke Sonnet 4.6, yang memberikan lebih banyak kecerdasan dengan harga yang sama.

<Warning>
Sonnet 4.6 menggunakan tingkat usaha default `high`, berbeda dengan Sonnet 4.5 yang tidak memiliki parameter usaha. Pertimbangkan untuk menyesuaikan parameter usaha saat Anda bermigrasi dari Sonnet 4.5 ke Sonnet 4.6. Jika tidak secara eksplisit diatur, Anda mungkin mengalami latensi yang lebih tinggi dengan tingkat usaha default.
</Warning>

#### Jika Anda tidak menggunakan pemikiran yang diperluas

Jika Anda tidak menggunakan pemikiran yang diperluas pada Sonnet 4.5, Anda dapat melanjutkan tanpanya pada Sonnet 4.6. Anda harus secara eksplisit mengatur usaha ke tingkat yang sesuai untuk kasus penggunaan Anda. Pada usaha `low` dengan pemikiran dinonaktifkan, Anda dapat mengharapkan kinerja yang sama atau lebih baik relatif terhadap Sonnet 4.5 tanpa pemikiran yang diperluas.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 8192,
    "output_config": {
        "effort": "low"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```

```bash CLI
ant messages create <<'YAML'
model: claude-sonnet-4-6
max_tokens: 8192
output_config:
  effort: low
messages:
  - role: user
    content: Your prompt here
YAML
```

```python Python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    output_config={"effort": "low"},
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

```typescript TypeScript
const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 8192,
  output_config: { effort: "low" },
  messages: [{ role: "user", content: "Your prompt here" }]
});
```

```csharp C#
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Messages;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 8192,
            OutputConfig = new OutputConfig
            {
                Effort = Effort.Low
            },
            Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
        };
        var message = await client.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
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

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.Model("claude-sonnet-4-6"),
		MaxTokens: 8192,
		OutputConfig: anthropic.OutputConfigParam{
			Effort: anthropic.OutputConfigEffortLow,
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Your prompt here")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response.Content[0].Text)
}
```

```java Java hidelines={1..4,6..8,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.OutputConfig;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-sonnet-4-6")
            .maxTokens(8192L)
            .outputConfig(OutputConfig.builder()
                .effort(OutputConfig.Effort.LOW)
                .build())
            .addUserMessage("Your prompt here")
            .build();

        Message response = client.messages().create(params);
        response.content().stream()
            .flatMap(block -> block.text().stream())
            .forEach(textBlock -> System.out.println(textBlock.text()));
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 8192,
    messages: [['role' => 'user', 'content' => 'Your prompt here']],
    model: 'claude-sonnet-4-6',
    outputConfig: ['effort' => 'low'],
);
echo $message->content[0]->text;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 8192,
  output_config: {
    effort: "low"
  },
  messages: [
    { role: "user", content: "Your prompt here" }
  ]
)
puts message.content.first.text
```
</CodeGroup>

#### Jika Anda menggunakan pemikiran yang diperluas

Jika Anda menggunakan pemikiran yang diperluas dengan `budget_tokens` pada Sonnet 4.5, masih berfungsi pada Sonnet 4.6 tetapi sudah usang. Bermigrasi ke [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) dengan [parameter usaha](/docs/id/build-with-claude/effort).

##### Bermigrasi ke pemikiran adaptif

[Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) adalah pengganti yang direkomendasikan untuk `budget_tokens` pada Sonnet 4.6. Ini sangat cocok untuk pola beban kerja berikut:

- **Agen multi-langkah otonom:** agen pengkodean yang mengubah persyaratan menjadi perangkat lunak yang berfungsi, pipeline analisis data, dan pencarian bug di mana model berjalan secara independen di banyak langkah. Pemikiran adaptif memungkinkan model untuk mengkalibrasi penalarannya per langkah, tetap berada di jalur selama lintasan yang lebih panjang. Untuk beban kerja ini, mulai dengan usaha `high`. Jika latensi atau penggunaan token menjadi perhatian, kurangi ke `medium`.
- **Agen penggunaan komputer:** Sonnet 4.6 mencapai akurasi terbaik di kelasnya pada evaluasi penggunaan komputer menggunakan mode adaptif.
- **Beban kerja bimodal:** campuran tugas mudah dan sulit di mana adaptif melewatkan pemikiran pada kueri sederhana dan bernalar secara mendalam pada kueri kompleks.

Saat menggunakan pemikiran adaptif, evaluasi usaha `medium` dan `high` pada tugas Anda. Tingkat yang tepat tergantung pada pertukaran beban kerja Anda antara kualitas, latensi, dan penggunaan token.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 64000,
    "thinking": {
        "type": "adaptive"
    },
    "output_config": {
        "effort": "medium"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```

```bash CLI nocheck
ant messages create <<'YAML'
model: claude-sonnet-4-6
max_tokens: 64000
thinking:
  type: adaptive
output_config:
  effort: medium
messages:
  - role: user
    content: Your prompt here
YAML
```

```python Python nocheck
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

```typescript TypeScript nocheck
const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 64000,
  thinking: { type: "adaptive" },
  output_config: { effort: "medium" },
  messages: [{ role: "user", content: "Your prompt here" }]
});
```

```csharp C# nocheck
using Anthropic;
using Anthropic.Models.Messages;
using System;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = Model.ClaudeSonnet4_6,
            MaxTokens = 64000,
            Thinking = new ThinkingConfigAdaptive(),
            OutputConfig = new OutputConfig { Effort = Effort.Medium },
            Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
        };

        var message = await client.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
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

	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     "claude-sonnet-4-6",
		MaxTokens: 64000,
		Thinking: anthropic.ThinkingConfigParamUnion{
			OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
		},
		OutputConfig: anthropic.OutputConfigParam{
			Effort: anthropic.OutputConfigEffortMedium,
		},
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("Your prompt here")),
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java nocheck hidelines={1..4,7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.OutputConfig;
import com.anthropic.models.messages.ThinkingConfigAdaptive;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-sonnet-4-6")
            .maxTokens(64000L)
            .thinking(ThinkingConfigAdaptive.builder().build())
            .outputConfig(OutputConfig.builder()
                .effort(OutputConfig.Effort.MEDIUM)
                .build())
            .addUserMessage("Your prompt here")
            .build();

        Message response = client.messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4} nocheck
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->messages->create(
    maxTokens: 64000,
    messages: [['role' => 'user', 'content' => 'Your prompt here']],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'adaptive'],
    outputConfig: ['effort' => 'medium'],
);

echo $message->content[0]->text;
```

```ruby Ruby nocheck hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 64000,
  thinking: {
    type: "adaptive"
  },
  output_config: {
    effort: "medium"
  },
  messages: [
    { role: "user", content: "Your prompt here" }
  ]
)
puts message
```
</CodeGroup>

<Note>
Jika Anda melihat perilaku yang tidak konsisten atau regresi kualitas dengan pemikiran adaptif, coba kurangi pengaturan [usaha](/docs/id/build-with-claude/effort) atau gunakan `max_tokens` sebagai batas keras terlebih dahulu. Pemikiran yang diperluas dengan `budget_tokens` masih berfungsi pada Sonnet 4.6 tetapi sudah usang dan tidak lagi direkomendasikan.
</Note>

##### Mempertahankan budget_tokens selama migrasi

Jika Anda perlu mempertahankan `budget_tokens` sementara saat bermigrasi, anggaran sekitar 16k token memberikan ruang untuk masalah yang lebih sulit tanpa risiko penggunaan token yang liar. Konfigurasi ini sudah usang dan akan dihapus dalam rilis model di masa depan.

###### Kasus penggunaan pengkodean dan agentic

Untuk pengkodean agentic, desain frontend, alur kerja berat alat, dan alur kerja enterprise yang kompleks, mulai dengan usaha `medium`. Jika Anda menemukan latensi terlalu tinggi, pertimbangkan untuk mengurangi usaha ke `low`. Jika Anda membutuhkan kecerdasan yang lebih tinggi, pertimbangkan untuk meningkatkan usaha ke `high` atau bermigrasi ke Opus 4.6.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "anthropic-beta: interleaved-thinking-2025-05-14" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 16384,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 16384
    },
    "output_config": {
        "effort": "medium"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```

```bash CLI
ant beta:messages create --beta interleaved-thinking-2025-05-14 <<'YAML'
model: claude-sonnet-4-6
max_tokens: 16384
thinking:
  type: enabled
  budget_tokens: 16384
output_config:
  effort: medium
messages:
  - role: user
    content: Your prompt here
YAML
```

```python Python
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16384,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "medium"},
    betas=["interleaved-thinking-2025-05-14"],
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

```typescript TypeScript
const response = await client.beta.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 16384,
  thinking: { type: "enabled", budget_tokens: 16384 },
  output_config: { effort: "medium" },
  betas: ["interleaved-thinking-2025-05-14"],
  messages: [{ role: "user", content: "Your prompt here" }]
});
```

```csharp C#
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta;
using Anthropic.Models.Beta.Messages;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = "claude-sonnet-4-6",
            MaxTokens = 16384,
            Thinking = new BetaThinkingConfigEnabled { BudgetTokens = 16384 },
            OutputConfig = new BetaOutputConfig
            {
                Effort = Effort.Medium
            },
            Betas = [AnthropicBeta.InterleavedThinking2025_05_14],
            Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
        };

        var message = await client.Beta.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
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
		Model:     "claude-sonnet-4-6",
		MaxTokens: 16384,
		Thinking:  anthropic.BetaThinkingConfigParamOfEnabled(16384),
		OutputConfig: anthropic.BetaOutputConfigParam{
			Effort: anthropic.BetaOutputConfigEffortMedium,
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Your prompt here")),
		},
		Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaInterleavedThinking2025_05_14},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..4,7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaThinkingConfigEnabled;
import com.anthropic.models.beta.messages.BetaOutputConfig;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-sonnet-4-6")
            .maxTokens(16384L)
            .thinking(BetaThinkingConfigEnabled.builder()
                .budgetTokens(16384L)
                .build())
            .outputConfig(BetaOutputConfig.builder()
                .effort(BetaOutputConfig.Effort.MEDIUM)
                .build())
            .addBeta("interleaved-thinking-2025-05-14")
            .addUserMessage("Your prompt here")
            .build();

        BetaMessage response = client.beta().messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->beta->messages->create(
    maxTokens: 16384,
    messages: [['role' => 'user', 'content' => 'Your prompt here']],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'enabled', 'budget_tokens' => 16384],
    outputConfig: ['effort' => 'medium'],
    betas: ['interleaved-thinking-2025-05-14'],
);

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.beta.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 16384,
  thinking: {
    type: "enabled",
    budget_tokens: 16384
  },
  output_config: {
    effort: "medium"
  },
  betas: ["interleaved-thinking-2025-05-14"],
  messages: [
    { role: "user", content: "Your prompt here" }
  ]
)
puts message
```
</CodeGroup>

###### Kasus penggunaan chat dan non-pengkodean

Untuk chat, pembuatan konten, pencarian, klasifikasi, dan tugas non-pengkodean lainnya, mulai dengan usaha `low` dengan pemikiran yang diperluas. Jika Anda membutuhkan kedalaman lebih, tingkatkan usaha ke `medium`.

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "anthropic-beta: interleaved-thinking-2025-05-14" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-sonnet-4-6",
    "max_tokens": 8192,
    "thinking": {
        "type": "enabled",
        "budget_tokens": 16384
    },
    "output_config": {
        "effort": "low"
    },
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ]
}'
```

```bash CLI
ant beta:messages create --beta interleaved-thinking-2025-05-14 <<'YAML'
model: claude-sonnet-4-6
max_tokens: 8192
thinking:
  type: enabled
  budget_tokens: 16384
output_config:
  effort: low
messages:
  - role: user
    content: Your prompt here
YAML
```

```python Python
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "low"},
    betas=["interleaved-thinking-2025-05-14"],
    messages=[{"role": "user", "content": "Your prompt here"}],
)
```

```typescript TypeScript
const response = await client.beta.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 8192,
  thinking: { type: "enabled", budget_tokens: 16384 },
  output_config: { effort: "low" },
  betas: ["interleaved-thinking-2025-05-14"],
  messages: [{ role: "user", content: "Your prompt here" }]
});
```

```csharp C#
using System;
using System.Threading.Tasks;
using Anthropic;
using Anthropic.Models.Beta;
using Anthropic.Models.Beta.Messages;

class Program
{
    static async Task Main(string[] args)
    {
        AnthropicClient client = new();

        var parameters = new MessageCreateParams
        {
            Model = "claude-sonnet-4-6",
            MaxTokens = 8192,
            Thinking = new BetaThinkingConfigEnabled { BudgetTokens = 16384 },
            OutputConfig = new BetaOutputConfig
            {
                Effort = Effort.Low
            },
            Betas = [AnthropicBeta.InterleavedThinking2025_05_14],
            Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
        };

        var message = await client.Beta.Messages.Create(parameters);
        Console.WriteLine(message);
    }
}
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
		Model:     "claude-sonnet-4-6",
		MaxTokens: 8192,
		Thinking:  anthropic.BetaThinkingConfigParamOfEnabled(16384),
		OutputConfig: anthropic.BetaOutputConfigParam{
			Effort: anthropic.BetaOutputConfigEffortLow,
		},
		Messages: []anthropic.BetaMessageParam{
			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Your prompt here")),
		},
		Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaInterleavedThinking2025_05_14},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(response)
}
```

```java Java hidelines={1..4,7..9,-2..}
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.BetaMessage;
import com.anthropic.models.beta.messages.BetaThinkingConfigEnabled;
import com.anthropic.models.beta.messages.BetaOutputConfig;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        MessageCreateParams params = MessageCreateParams.builder()
            .model("claude-sonnet-4-6")
            .maxTokens(8192L)
            .thinking(BetaThinkingConfigEnabled.builder()
                .budgetTokens(16384L)
                .build())
            .outputConfig(BetaOutputConfig.builder()
                .effort(BetaOutputConfig.Effort.LOW)
                .build())
            .addBeta("interleaved-thinking-2025-05-14")
            .addUserMessage("Your prompt here")
            .build();

        BetaMessage response = client.beta().messages().create(params);
        System.out.println(response);
    }
}
```

```php PHP hidelines={1..4}
<?php

use Anthropic\Client;

$client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

$message = $client->beta->messages->create(
    maxTokens: 8192,
    messages: [['role' => 'user', 'content' => 'Your prompt here']],
    model: 'claude-sonnet-4-6',
    thinking: ['type' => 'enabled', 'budget_tokens' => 16384],
    outputConfig: ['effort' => 'low'],
    betas: ['interleaved-thinking-2025-05-14'],
);

echo $message;
```

```ruby Ruby hidelines={1..2}
require "anthropic"

client = Anthropic::Client.new

message = client.beta.messages.create(
  model: "claude-sonnet-4-6",
  max_tokens: 8192,
  thinking: {
    type: "enabled",
    budget_tokens: 16384
  },
  output_config: {
    effort: "low"
  },
  betas: ["interleaved-thinking-2025-05-14"],
  messages: [
    { role: "user", content: "Your prompt here" }
  ]
)
puts message
```
</CodeGroup>

### Daftar periksa migrasi Sonnet 4.6

- [ ] Perbarui ID model ke `claude-sonnet-4-6`
- [ ] **BREAKING:** Hapus prefilling pesan asisten; gunakan output terstruktur atau `output_config.format` sebagai gantinya
- [ ] **BREAKING:** Verifikasi penanganan parsing JSON parameter alat menangani perbedaan escaping
- [ ] **BREAKING:** Perbarui versi alat ke versi terbaru (`text_editor_20250728`, `code_execution_20250825`); versi legacy tidak didukung (jika bermigrasi dari 3.x)
- [ ] **BREAKING:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
- [ ] **BREAKING:** Perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`, bukan keduanya (jika bermigrasi dari 3.x)
- [ ] Tangani alasan penghentian `refusal` baru di aplikasi Anda
- [ ] Hapus header beta `fine-grained-tool-streaming-2025-05-14` (sekarang GA)
- [ ] Migrasikan `output_format` ke `output_config.format`
- [ ] Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] **Direkomendasikan:** Migrasikan dari `thinking: {type: "enabled", budget_tokens: N}` ke `thinking: {type: "adaptive"}` dengan [parameter usaha](/docs/id/build-with-claude/effort) (`budget_tokens` sudah usang dan akan dihapus dalam rilis model di masa depan)
- [ ] Uji di lingkungan pengembangan sebelum penyebaran produksi

---

## Bermigrasi ke Claude Sonnet 4.5

Claude Sonnet 4.5 menggabungkan kecerdasan yang kuat dengan kinerja cepat, menjadikannya ideal untuk tugas pengkodean, analisis, dan konten sehari-hari.

Untuk gambaran lengkap tentang kemampuan, lihat [gambaran umum model](/docs/id/about-claude/models/overview).

<Note>
Harga Sonnet 4.5 adalah $3 per juta token input, $15 per juta token output. Lihat [harga Claude](/docs/id/about-claude/pricing) untuk detail.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Sonnet 4
model = "claude-sonnet-4-20250514"  # Sebelum
model = "claude-sonnet-4-5-20250929"  # Sesudah

# Dari Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Sebelum
model = "claude-sonnet-4-5-20250929"  # Sesudah
```

### Perubahan yang merusak

Perubahan yang merusak ini berlaku saat bermigrasi dari model Claude 3.x Sonnet.

1. **Perbarui parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

2. **Perbarui versi alat**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

3. **Tangani alasan penghentian `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan penghentian `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Daftar periksa migrasi Sonnet 4.5

- [ ] Perbarui ID model ke `claude-sonnet-4-5-20250929`
- [ ] **BREAKING:** Perbarui versi alat ke versi terbaru (`text_editor_20250728`, `code_execution_20250825`); versi legacy tidak didukung (jika bermigrasi dari 3.x)
- [ ] **BREAKING:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
- [ ] **BREAKING:** Perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`, bukan keduanya (jika bermigrasi dari 3.x)
- [ ] Tangani alasan penghentian `refusal` baru di aplikasi Anda
- [ ] Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Pertimbangkan untuk mengaktifkan pemikiran yang diperluas untuk tugas penalaran kompleks
- [ ] Uji di lingkungan pengembangan sebelum penyebaran produksi

---

## Bermigrasi ke Claude Haiku 4.5

Claude Haiku 4.5 adalah model Haiku tercepat dan paling cerdas dengan kinerja mendekati frontier, memberikan kualitas model premium untuk aplikasi interaktif dan pemrosesan volume tinggi.

Untuk gambaran lengkap tentang kemampuan, lihat [gambaran umum model](/docs/id/about-claude/models/overview).

<Note>
Harga Haiku 4.5 adalah $1 per juta token input, $5 per juta token output. Lihat [harga Claude](/docs/id/about-claude/pricing) untuk detail.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Haiku 3.5
model = "claude-3-5-haiku-20241022"  # Sebelum
model = "claude-haiku-4-5-20251001"  # Sesudah

# Dari Haiku 3
model = "claude-3-haiku-20240307"  # Sebelum
model = "claude-haiku-4-5-20251001"  # Sesudah
```

**Tinjau batas laju baru:** Haiku 4.5 memiliki batas laju terpisah dari Haiku 3.5 dan Haiku 3. Lihat [dokumentasi Batas laju](/docs/id/api/rate-limits) untuk detail.

<Tip>
Untuk peningkatan kinerja yang signifikan pada tugas pengkodean dan penalaran, pertimbangkan untuk mengaktifkan pemikiran yang diperluas dengan `thinking: {type: "enabled", budget_tokens: N}`.
</Tip>

<Note>
Pemikiran yang diperluas mempengaruhi efisiensi [prompt caching](/docs/id/build-with-claude/prompt-caching#caching-with-thinking-blocks).

Pemikiran yang diperluas sudah usang dalam model Claude 4.6 atau lebih baru. Jika menggunakan model lebih baru, gunakan [pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking) sebagai gantinya.
</Note>

**Jelajahi kemampuan baru:** Lihat [gambaran umum model](/docs/id/about-claude/models/overview) untuk detail tentang kesadaran konteks, kapasitas output yang ditingkatkan (64k token), kecerdasan yang lebih tinggi, dan kecepatan yang ditingkatkan.

### Perubahan yang merusak

Perubahan yang merusak ini berlaku saat bermigrasi dari model Claude 3.x Haiku.

1. **Perbarui parameter sampling**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

2. **Perbarui versi alat**

   <Warning>
   Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

3. **Tangani alasan penghentian `refusal`**

   Perbarui aplikasi Anda untuk [menangani alasan penghentian `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Daftar periksa migrasi Haiku 4.5

- [ ] Perbarui ID model ke `claude-haiku-4-5-20251001`
- [ ] **BREAKING:** Perbarui versi alat ke versi terbaru (`text_editor_20250728`, `code_execution_20250825`); versi legacy tidak didukung
- [ ] **BREAKING:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
- [ ] **BREAKING:** Perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`, bukan keduanya
- [ ] Tangani alasan penghentian `refusal` baru di aplikasi Anda
- [ ] Tinjau dan sesuaikan untuk batas laju baru (terpisah dari Haiku 3.5)
- [ ] Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [ ] Pertimbangkan untuk mengaktifkan pemikiran yang diperluas untuk tugas penalaran kompleks
- [ ] Uji di lingkungan pengembangan sebelum penyebaran produksi

---

## Dapatkan bantuan

- Periksa [dokumentasi API](/docs/id/api/overview) untuk spesifikasi terperinci
- Tinjau [kemampuan model](/docs/id/about-claude/models/overview) untuk perbandingan kinerja
- Tinjau [catatan rilis API](/docs/id/release-notes/api) untuk pembaruan API
- Hubungi dukungan jika Anda mengalami masalah apa pun selama migrasi