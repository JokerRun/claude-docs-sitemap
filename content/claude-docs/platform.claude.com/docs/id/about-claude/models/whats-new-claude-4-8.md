---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/whats-new-claude-4-8
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 6963598dedccd245518c1749796dc02e82e8dc1c5bc7267de40f8396c58cdf86
---

# Apa yang baru di Claude Opus 4.8

Ikhtisar fitur baru dan perubahan perilaku di Claude Opus 4.8.

---

Claude Opus 4.8 dibangun untuk pengodean agentik yang kompleks dan pekerjaan enterprise. Model ini dibangun di atas Claude Opus 4.7. Halaman ini merangkum semua yang baru pada saat peluncuran, termasuk "fast mode" (mode cepat, pratinjau riset di Claude API) dan panjang prompt minimum yang dapat di-cache yang lebih rendah, yaitu 1.024 token.

## Model baru

| Model           | ID model API    | Deskripsi                                                      |
| --------------- | --------------- | -------------------------------------------------------------- |
| Claude Opus 4.8 | claude-opus-4-8 | Untuk pengodean agentik yang kompleks dan pekerjaan enterprise |

Claude Opus 4.8 mendukung [jendela konteks 1 juta token](/docs/id/build-with-claude/context-windows) secara default di Claude API, Amazon Bedrock, Google Cloud, dan Microsoft Foundry, 128k token output maksimum, [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), dan kumpulan alat serta fitur platform yang sama dengan Claude Opus 4.7.

Untuk harga dan spesifikasi lengkap, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

## Fitur baru

### Pesan sistem di tengah percakapan

Claude Opus 4.8 menerima pesan `role: "system"` segera setelah giliran pengguna dalam array `messages` (tunduk pada [aturan penempatan](/docs/id/build-with-claude/mid-conversation-system-messages#limitations)). Ini memungkinkan Anda menambahkan instruksi yang diperbarui di kemudian hari dalam percakapan yang berjalan lama tanpa menyatakan ulang prompt sistem secara lengkap. Memperbarui instruksi dengan cara ini mempertahankan hit [prompt cache](/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya dan mengurangi biaya input pada loop agentik. Tidak diperlukan header beta. Lihat [Pesan sistem di tengah percakapan](/docs/id/build-with-claude/mid-conversation-system-messages) untuk detail penggunaan.

### Detail stop penolakan

Objek `stop_details` pada respons penolakan (tersedia sejak Claude Opus 4.7) kini didokumentasikan secara publik. Ketika Claude menolak untuk menyelesaikan permintaan, objek ini menjelaskan kategori penolakan, sebagai tambahan dari stop reason `refusal` yang sudah ada. Aplikasi Anda dapat menggunakannya untuk membedakan berbagai kelas permintaan yang ditolak dan mengarahkan pengguna ke langkah berikutnya yang tepat. Tidak diperlukan header beta. Lihat [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk daftar kategori dan [Stop reason dan fallback](/docs/id/build-with-claude/handling-stop-reasons) untuk panduan penanganan.

### Default effort

Default [parameter effort](/docs/id/build-with-claude/effort) pada Claude Opus 4.8 adalah `high` di semua permukaan, termasuk Claude API dan Claude Code. Jika Anda mengatur effort secara eksplisit saat ini, pengaturan Anda tidak berubah. Lihat [Effort](/docs/id/build-with-claude/effort) untuk panduan per level.

### Fast mode

[Fast mode](/docs/id/build-with-claude/fast-mode) kini tersedia untuk Claude Opus 4.8 sebagai pratinjau riset di Claude API. Atur `speed: "fast"` dengan header beta `fast-mode-2026-02-01` untuk mendapatkan hingga 2,5x lebih banyak token output per detik dari model yang sama dengan harga premium. Lihat [Fast mode](/docs/id/build-with-claude/fast-mode) untuk akses, model yang didukung, dan harga.

### Minimum prompt cache yang lebih rendah

Panjang prompt minimum yang dapat di-cache pada Claude Opus 4.8 adalah 1.024 token, turun dari 2.048 token pada Claude Opus 4.7. Prompt yang terlalu pendek untuk di-cache pada Claude Opus 4.7 kini dapat membuat entri cache tanpa perubahan kode. Lihat [Caching prompt](/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

## Batasan API yang diwarisi dari Claude Opus 4.7

<Note>
  Batasan ini tidak berubah dari Claude Opus 4.7, sehingga kode yang sudah berjalan di Claude Opus 4.7 tidak memerlukan perubahan. Batasan ini hanya berlaku untuk Messages API. Claude Managed Agents tidak terpengaruh.
</Note>

### Parameter sampling tidak didukung

Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default akan mengembalikan error 400 pada Claude Opus 4.8, sama seperti pada Claude Opus 4.7. Hilangkan parameter ini dan gunakan prompting untuk memandu perilaku model.

### Adaptive thinking adalah satu-satunya mode thinking

Seperti Claude Opus 4.7, Claude Opus 4.8 tidak mendukung anggaran pemikiran diperpanjang. Mengatur `thinking: {type: "enabled", budget_tokens: N}` akan mengembalikan error 400.

Diff berikut memperbarui permintaan yang ditulis untuk Claude Opus 4.6 atau sebelumnya agar dapat berjalan di Claude Opus 4.8. Baris yang dihapus (`-`) mengatur ID model lama dan anggaran thinking manual yang ditolak oleh Claude Opus 4.8. Baris yang ditambahkan (`+`) mengatur ID model baru, beralih ke [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), dan mengontrol kedalaman thinking dengan [parameter effort](/docs/id/build-with-claude/effort), yang diteruskan dalam field `output_config` tingkat atas. Model menentukan kapan dan seberapa banyak berpikir pada setiap giliran. Jika Anda menghapus field `thinking` sepenuhnya, permintaan berjalan tanpa thinking:

<CodeGroup>
  ```diff cURL
   curl https://api.anthropic.com/v1/messages \
        --header "x-api-key: $ANTHROPIC_API_KEY" \
        --header "anthropic-version: 2023-06-01" \
        --header "content-type: application/json" \
        --data \
   '{
  -    "model": "claude-opus-4-6",
  +    "model": "claude-opus-4-8",
       "max_tokens": 16000,
       "thinking": {
  -        "type": "enabled",
  -        "budget_tokens": 10000
  +        "type": "adaptive"
       },
  +    "output_config": {
  +        "effort": "high"
  +    },
       "messages": [
           {
               "role": "user",
               "content": "Explain why the sum of two even numbers is always even."
           }
       ]
   }'
  ```

  ```diff CLI
   ant messages create <<'YAML'
  -model: claude-opus-4-6
  +model: claude-opus-4-8
   max_tokens: 16000
   thinking:
  -  type: enabled
  -  budget_tokens: 10000
  +  type: adaptive
  +output_config:
  +  effort: high
   messages:
     - role: user
       content: Explain why the sum of two even numbers is always even.
   YAML
  ```

  ```diff Python
   import anthropic

   client = anthropic.Anthropic()

   response = client.messages.create(
  -    model="claude-opus-4-6",
  +    model="claude-opus-4-8",
       max_tokens=16000,
  -    thinking={"type": "enabled", "budget_tokens": 10000},
  +    thinking={"type": "adaptive"},
  +    output_config={"effort": "high"},
       messages=[
           {
               "role": "user",
               "content": "Explain why the sum of two even numbers is always even.",
           }
       ],
   )
  ```

  ```diff TypeScript
   import Anthropic from "@anthropic-ai/sdk";

   const client = new Anthropic();

   const response = await client.messages.create({
  -  model: "claude-opus-4-6",
  +  model: "claude-opus-4-8",
     max_tokens: 16000,
  -  thinking: { type: "enabled", budget_tokens: 10000 },
  +  thinking: { type: "adaptive" },
  +  output_config: { effort: "high" },
     messages: [
       {
         role: "user",
         content: "Explain why the sum of two even numbers is always even."
       }
     ]
   });
  ```

  ```diff C#
   using Anthropic;
   using Anthropic.Models.Messages;

   AnthropicClient client = new();

   var parameters = new MessageCreateParams
   {
  -    Model = "claude-opus-4-6",
  +    Model = Model.ClaudeOpus4_8,
       MaxTokens = 16000,
  -    Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
  +    Thinking = new ThinkingConfigAdaptive(),
  +    OutputConfig = new OutputConfig { Effort = Effort.High },
       Messages = [new() { Role = Role.User, Content = "Explain why the sum of two even numbers is always even." }]
   };

   var response = await client.Messages.Create(parameters);
   Console.WriteLine(response);
  ```

  ```diff Go
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
  -		Model:     "claude-opus-4-6",
  +		Model:     anthropic.ModelClaudeOpus4_8,
   		MaxTokens: 16000,
  -		Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
  +		Thinking: anthropic.ThinkingConfigParamUnion{
  +			OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
  +		},
  +		OutputConfig: anthropic.OutputConfigParam{
  +			Effort: anthropic.OutputConfigEffortHigh,
  +		},
   		Messages: []anthropic.MessageParam{
   			anthropic.NewUserMessage(anthropic.NewTextBlock("Explain why the sum of two even numbers is always even.")),
   		},
   	})
   	if err != nil {
   		log.Fatal(err)
   	}
   	fmt.Println(response)
   }
  ```

  ```diff Java
   import com.anthropic.client.AnthropicClient;
   import com.anthropic.client.okhttp.AnthropicOkHttpClient;
   import com.anthropic.models.messages.Message;
   import com.anthropic.models.messages.MessageCreateParams;
  +import com.anthropic.models.messages.Model;
  +import com.anthropic.models.messages.OutputConfig;
  +import com.anthropic.models.messages.ThinkingConfigAdaptive;

   void main() {
       AnthropicClient client = AnthropicOkHttpClient.fromEnv();

       MessageCreateParams params = MessageCreateParams.builder()
  -        .model("claude-opus-4-6")
  +        .model(Model.CLAUDE_OPUS_4_8)
           .maxTokens(16000L)
  -        .enabledThinking(10000L)
  +        .thinking(ThinkingConfigAdaptive.builder().build())
  +        .outputConfig(OutputConfig.builder()
  +            .effort(OutputConfig.Effort.HIGH)
  +            .build())
           .addUserMessage("Explain why the sum of two even numbers is always even.")
           .build();

       Message response = client.messages().create(params);
       IO.println(response);
   }
  ```

  ```diff PHP
   <?php

   use Anthropic\Client;

   $client = new Client();

   $response = $client->messages->create(
       maxTokens: 16000,
       messages: [['role' => 'user', 'content' => 'Explain why the sum of two even numbers is always even.']],
  -    model: 'claude-opus-4-6',
  -    thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
  +    model: 'claude-opus-4-8',
  +    thinking: ['type' => 'adaptive'],
  +    outputConfig: ['effort' => 'high'],
   );
  ```

  ```diff Ruby
   require "anthropic"

   client = Anthropic::Client.new

   response = client.messages.create(
  -  model: "claude-opus-4-6",
  +  model: "claude-opus-4-8",
     max_tokens: 16000,
  -  thinking: { type: "enabled", budget_tokens: 10000 },
  +  thinking: { type: "adaptive" },
  +  output_config: { effort: "high" },
     messages: [
       { role: "user", content: "Explain why the sum of two even numbers is always even." }
     ]
   )
  ```
</CodeGroup>

## Peningkatan kemampuan

### Area peningkatan

Dibandingkan dengan Claude Opus 4.7, Claude Opus 4.8 menargetkan peningkatan perilaku dalam:

* **Pengodean agentik jangka panjang**, termasuk penanganan konteks panjang yang lebih baik, lebih sedikit pemadatan, dan pemulihan [pemadatan](/docs/id/build-with-claude/compaction) yang lebih baik.
* **Kalibrasi effort penalaran**, dengan perilaku yang lebih andal di setiap level effort di berbagai domain.
* **Pemicuan alat**, dengan lebih sedikit kasus melewatkan pemanggilan alat yang diperlukan oleh tugas.

### Adaptive thinking

Dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) diaktifkan, Claude Opus 4.8 memicu penalaran hanya ketika model menentukan bahwa giliran tersebut membutuhkannya. Pada pencarian sederhana dan langkah agentik singkat, model merespons secara langsung. Pada masalah multi-langkah yang kompleks, model bernalar sebelum menjawab. Ini mengurangi token thinking yang terbuang pada beban kerja bimodal dibandingkan dengan Claude Opus 4.7 pada level effort yang sama. Seperti pada Claude Opus 4.7, thinking dinonaktifkan kecuali Anda secara eksplisit mengatur `thinking: {type: "adaptive"}` dalam permintaan Anda.

## Perubahan perilaku

Ini bukan perubahan yang merusak API tetapi mungkin memerlukan pembaruan prompt. Lihat [Migrasi ke Claude Opus 4.8](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-47) untuk panduan lengkap.

* **Lebih sedikit token thinking yang terbuang** pada level effort yang sama ketika adaptive thinking diaktifkan, karena model menentukan per giliran apakah akan berpikir.
* **Pemicuan alat yang lebih baik.** Model lebih kecil kemungkinannya untuk melewatkan pemanggilan alat yang diperlukan oleh tugas, masalah yang dilaporkan beberapa pengguna pada Claude Opus 4.7.
* **Penanganan pemadatan dan kualitas konteks panjang yang lebih baik.** Jejak agentik yang panjang tetap pada jalurnya dengan lebih sedikit penyimpangan setelah pemadatan.
* **Level effort dikalibrasi ulang.** Alokasi token di balik setiap level effort berubah dibandingkan dengan Claude Opus 4.7: `medium` memungkinkan sedikit lebih banyak thinking, `high` sedikit lebih sedikit, dan `xhigh` jauh lebih banyak. Jika Anda telah menyetel level effort terhadap Claude Opus 4.7, tetapkan ulang baseline biaya dan latensi pada level tersebut sebelum menyesuaikannya.

## Panduan migrasi

Untuk instruksi migrasi langkah demi langkah dan daftar periksa migrasi lengkap, lihat [Migrasi ke Claude Opus 4.8](/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-47). Jika Anda melakukan upgrade dari Claude Opus 4.6 atau sebelumnya, terapkan juga [langkah migrasi Claude Opus 4.7](/docs/id/about-claude/models/migration-guide#migrating-to-claude-opus-4-7). Langkah-langkah tersebut mencakup perubahan yang merusak yang tidak dicakup oleh upgrade Claude Opus 4.8 saja. Jika Anda menggunakan Claude Code atau Agent SDK, [skill Claude API](/docs/id/agents-and-tools/agent-skills/claude-api-skill) dapat menerapkan langkah-langkah migrasi ini ke basis kode Anda secara otomatis.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Panduan migrasi" icon="arrow-right" href="/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-47">
    Panduan untuk migrasi ke model Claude terbaru dari versi Claude sebelumnya.
  </Card>

  <Card title="Effort" icon="gauge" href="/docs/id/build-with-claude/effort">
    Kontrol berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menyeimbangkan antara kelengkapan respons dan efisiensi token.
  </Card>

  <Card title="Adaptive thinking" icon="brain" href="/docs/id/build-with-claude/adaptive-thinking">
    Biarkan Claude secara dinamis menentukan kapan dan seberapa banyak menggunakan pemikiran diperpanjang dengan mode adaptive thinking.
  </Card>

  <Card title="Caching prompt" icon="database" href="/docs/id/build-with-claude/prompt-caching">
    Bagaimana pesan sistem di tengah percakapan mempertahankan cache hit.
  </Card>

  <Card title="Stop reason dan fallback" icon="code" href="/docs/id/build-with-claude/handling-stop-reasons">
    Pelajari apa arti setiap nilai stop\_reason dan cara menangani pemotongan, penggunaan alat, giliran yang dijeda, dan penolakan dalam aplikasi Anda.
  </Card>

  <Card title="Fast mode (pratinjau riset)" icon="bolt" href="/docs/id/build-with-claude/fast-mode">
    Dapatkan hingga 2,5x lebih banyak token output per detik dari model Claude Opus.
  </Card>
</CardGroup>
