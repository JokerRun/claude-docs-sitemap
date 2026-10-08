---
source: platform
url: https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: 50a33bc8e91e523170e48541f5b33436250397d3d8e6e7d6a56e3a9ec87fcf91
---

---
title: Panduan migrasi Claude Sonnet 5.5
url: https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide
description: Beralih ke Claude Sonnet 5.5 dari model Sonnet sebelumnya atau Claude Haiku 4.5 dengan panduan migrasi ini. Panduan untuk mengaktifkan Claude Sonnet 5.5 mencakup pengaturan yang mengembalikan error, perubahan thinking, dan daftar periksa untuk setiap model awal.
---

Panduan ini mencantumkan perubahan kode untuk beralih ke Claude Sonnet 5.5 dari Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Sonnet 4, Claude 3.7 Sonnet, atau Claude Haiku 4.5. Baca dua bagian pertama, lalu lanjutkan membaca hingga bagian untuk model Anda saat ini. [Daftar periksa migrasi](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#migration-checklist) mencantumkan setiap perubahan berdasarkan model awal.

<Note>
  Panduan ini membahas migrasi kode [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak ada perubahan yang diperlukan selain memperbarui nama model.
</Note>

<Tip>
  **Otomatiskan migrasi Anda dengan skill Claude API.** Di Claude Code, jalankan `/claude-api migrate` untuk memanggil [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model) bawaan. Skill ini berfungsi untuk model Claude terkini mana pun sebagai target:

  ```text wrap
  /claude-api migrate this project to claude-sonnet-5-5
  ```

  Skill ini menerapkan penggantian ID model dan, sesuai kebutuhan, perubahan parameter yang bersifat breaking, penggantian prefill, serta kalibrasi effort untuk model target Anda di seluruh basis kode Anda, lalu menghasilkan daftar periksa berisi item yang perlu diverifikasi secara manual. Skill ini meminta Anda mengonfirmasi cakupan migrasi (seluruh direktori kerja, sebuah subdirektori, atau daftar file tertentu) sebelum mengedit file apa pun. Skill ini juga mendeteksi klien Amazon Bedrock dan Claude Platform on AWS serta menyesuaikan format ID model dan perubahan fitur untuk platform tersebut.
</Tip>

Claude Sonnet 5.5 memiliki harga yang sama dengan Claude Sonnet 5, kecuali untuk pembacaan cache prompt, yang berbiaya $0,10 USD per juta token, setengah dari tarif Claude Sonnet 5. Lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing). Untuk "context window" (jendela konteks) dan batas output-nya, lihat [halaman model Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview). Untuk fitur dan prompting, lihat [Yang baru di Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#feature-support) dan [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5).

## Mengirim permintaan ke Claude Sonnet 5.5

Permintaan ini berfungsi di Claude Sonnet 5.5 sebagaimana tertulis. Permintaan ini menetapkan tingkat effort, dan tab SDK membaca balasan berdasarkan jenis blok. Permintaan ini tidak menyertakan lima pengaturan yang mengembalikan error 400: [anggaran pemikiran](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#sonnet-46-breaking-changes), [parameter sampling](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#sonnet-46-breaking-changes), [prefill asisten](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#migrating-from-sonnet-45), [pilihan alat paksa](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#forced-tool-use), dan [`thinking: {"type": "disabled"}`](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#turn-off-up-front-thinking).

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-5-5",
      "max_tokens": 4096,
      "messages": [{
        "role": "user",
        "content": "Analyze the trade-offs between microservices and monolithic architectures"
      }],
      "output_config": {
        "effort": "medium"
      }
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-sonnet-5-5 \
    --max-tokens 4096 \
    --output-config '{effort: medium}' \
    --message '{role: user, content: "Analyze the trade-offs between microservices and monolithic architectures"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-sonnet-5-5",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Analyze the trade-offs between microservices and monolithic architectures",
          }
      ],
      output_config={"effort": "medium"},
  )

  print(f"Stop reason: {response.stop_reason}")
  for block in response.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-sonnet-5-5",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Analyze the trade-offs between microservices and monolithic architectures"
      }
    ],
    output_config: {
      effort: "medium"
    }
  });

  console.log(`Stop reason: ${response.stop_reason}`);
  const textBlock = response.content.find(
    (block): block is Anthropic.TextBlock => block.type === "text"
  );
  console.log(textBlock?.text);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5_5,
      MaxTokens = 4096,
      Messages = [
          new() {
              Role = Role.User,
              Content = "Analyze the trade-offs between microservices and monolithic architectures"
          }
      ],
      OutputConfig = new OutputConfig
      {
          Effort = Effort.Medium
      }
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine($"Stop reason: {message.StopReason?.Raw()}");
  foreach (var block in message.Content)
  {
      if (block.TryPickText(out var textBlock))
      {
          Console.WriteLine(textBlock.Text);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet5_5,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the trade-offs between microservices and monolithic architectures")),
  	},
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortMedium,
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println("Stop reason:", response.StopReason)
  for _, block := range response.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.messages.OutputConfig;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_5_5)
          .maxTokens(4096L)
          .addUserMessage("Analyze the trade-offs between microservices and monolithic architectures")
          .outputConfig(OutputConfig.builder()
              .effort(OutputConfig.Effort.MEDIUM)
              .build())
          .build();

      Message response = client.messages().create(params);
      response.stopReason().ifPresent(reason -> IO.println("Stop reason: " + reason));
      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Analyze the trade-offs between microservices and monolithic architectures']
      ],
      model: 'claude-sonnet-5-5',
      outputConfig: ['effort' => 'medium'],
  );

  echo "Stop reason: {$message->stopReason}", PHP_EOL;
  foreach ($message->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-sonnet-5-5",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Analyze the trade-offs between microservices and monolithic architectures" }
    ],
    output_config: {
      effort: "medium"
    }
  )

  puts "Stop reason: #{message.stop_reason}"
  message.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

## Pemikiran berjalan secara default

Di Claude Sonnet 5.5, permintaan tanpa field `thinking` berjalan dengan ["adaptive thinking" (pemikiran adaptif)](https://platform.claude.com/docs/id/build-with-claude/thinking), sama seperti `thinking: {"type": "adaptive"}`. Di Claude Sonnet 4.6 dan model sebelumnya serta di Claude Haiku 4.5, permintaan tersebut berjalan tanpa pemikiran. Agar tetap berjalan tanpa pemikiran di awal, lihat [Menonaktifkan pemikiran di awal](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#turn-off-up-front-thinking).

| Model                                  | Pemikiran tanpa field `thinking` | Nilai `thinking.type` yang diterima             | `display` default |
| -------------------------------------- | -------------------------------- | ----------------------------------------------- | ----------------- |
| Claude Sonnet 5.5                      | Aktif                            | `"adaptive"`, `"between_tools"`                 | `"omitted"`       |
| Claude Sonnet 5                        | Aktif                            | `"adaptive"`, `"disabled"`                      | `"omitted"`       |
| Claude Sonnet 4.6                      | Nonaktif                         | `"adaptive"`, `"disabled"`, `"enabled"` (usang) | `"summarized"`    |
| Claude Sonnet 4.5 dan Claude Haiku 4.5 | Nonaktif                         | `"disabled"`, `"enabled"`                       | `"summarized"`    |

### Menangani pemikiran dalam respons

Kode yang sebelumnya berjalan tanpa pemikiran memerlukan ketiga poin berikut. Kode dari Claude Sonnet 5 kemungkinan sudah memiliki dua poin pertama.

* **Baca blok konten berdasarkan `type`.** Respons dapat diawali dengan blok `thinking`, sehingga kode yang membaca `content[0].text` akan rusak.
* **Kirimkan kembali blok `thinking` tanpa perubahan** dalam loop penggunaan alat, termasuk blok yang kosong. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).
* **Tinjau kembali `max_tokens`.** Nilai ini mencakup pemikiran ditambah teks, dan token pemikiran ditagih sebagai token output. Lihat [Kontrol biaya](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#cost-control).

Teks pemikiran dihilangkan secara default. Blok `thinking` tiba dengan field `thinking` yang kosong dan sebuah `signature`. Untuk mendapatkan ringkasan yang dapat dibaca, tetapkan `display: "summarized"`, yang merupakan default di Claude Sonnet 4.6 dan model sebelumnya serta di Claude Haiku 4.5. Lihat [Mengontrol tampilan pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).

### Menonaktifkan pemikiran di awal

Untuk menonaktifkan pemikiran di awal pada Claude Sonnet 5.5, kirim `thinking: {"type": "between_tools"}`. Ini adalah pengaturan thinking terendah. Pembaruan progresnya di antara pemanggilan alat tetap dikembalikan sebagai blok `thinking` beserta teks ringkasannya. Tanpa alat, respons hanya berisi teks. Claude Sonnet 5 menonaktifkan pemikiran dengan `thinking: {"type": "disabled"}`, dan model sebelumnya berjalan tanpa pemikiran secara default. Di Claude Sonnet 5.5, `disabled` mengembalikan `invalid_request_error` 400:

```text wrap
To turn thinking off on this model, send "thinking": {"type": "between_tools"} instead of {"type": "disabled"}. The model does not think before responding. The short updates it writes between tool calls come back as thinking blocks.
```

`between_tools` berfungsi di setiap platform yang menawarkan Claude Sonnet 5.5, tanpa beta header. Pengaturan ini diterima pada effort `low`, `medium`, dan `high`. Pada `xhigh` atau `max`, pengaturan ini mengembalikan error 400. Untuk berjalan pada tingkat tersebut, gunakan pemikiran adaptif: hilangkan field `thinking` atau kirim `thinking: {"type": "adaptive"}`. `between_tools` tidak menerima field lain: `display`, `budget_tokens`, atau `block_binding` yang dikirim bersamanya mengembalikan error 400. Dengan [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback), permintaan `between_tools` yang beralih ke Claude Sonnet 5 berjalan di sana dengan `thinking: {"type": "disabled"}`.

Dengan `between_tools`, effort tidak dapat berubah di tengah percakapan: `output_config.effort` per pesan yang berbeda dari tingkat yang berlaku mengembalikan error 400. Untuk memvariasikan effort per giliran, gunakan pemikiran adaptif. Untuk panduan prompting, lihat [Berjalan tanpa pemikiran di awal](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#running-without-up-front-thinking).

Sebelum (Claude Sonnet 5):

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-5",
      "max_tokens": 16000,
      "thinking": {"type": "disabled"},
      "output_config": {"effort": "xhigh"},
      "messages": [{"role": "user", "content": "..."}]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-sonnet-5 \
    --max-tokens 16000 \
    --thinking '{type: disabled}' \
    --output-config '{effort: xhigh}' \
    --message '{role: user, content: "..."}'
  ```

  ```python Python
  client.messages.create(
      model="claude-sonnet-5",
      max_tokens=16000,
      thinking={"type": "disabled"},
      output_config={"effort": "xhigh"},
      messages=[{"role": "user", "content": "..."}],
  )
  ```

  ```typescript TypeScript
  await client.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 16000,
    thinking: { type: "disabled" },
    output_config: { effort: "xhigh" },
    messages: [{ role: "user", content: "..." }]
  });
  ```

  ```csharp C#
  await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigDisabled(),
      OutputConfig = new() { Effort = Effort.Xhigh },
      Messages = [new() { Role = Role.User, Content = "..." }],
  });
  ```

  ```go Go
  client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet5,
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfDisabled: &anthropic.ThinkingConfigDisabledParam{},
  	},
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortXhigh,
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
  	},
  })
  ```

  ```java Java
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_SONNET_5)
      .maxTokens(16000L)
      .thinking(ThinkingConfigDisabled.builder().build())
      .outputConfig(OutputConfig.builder()
          .effort(OutputConfig.Effort.XHIGH)
          .build())
      .addUserMessage("...")
      .build();

  client.messages().create(params);
  ```

  ```php PHP
  $client->messages->create(
      model: Model::CLAUDE_SONNET_5,
      maxTokens: 16000,
      thinking: ThinkingConfigDisabled::with(),
      outputConfig: OutputConfig::with(effort: Effort::XHIGH),
      messages: [['role' => 'user', 'content' => '...']],
  );
  ```

  ```ruby Ruby
  client.messages.create(
    model: Anthropic::Model::CLAUDE_SONNET_5,
    max_tokens: 16000,
    thinking: Anthropic::ThinkingConfigDisabled.new,
    output_config: { effort: Anthropic::OutputConfig::Effort::XHIGH },
    messages: [{ role: "user", content: "..." }]
  )
  ```
</CodeGroup>

Sesudah (Claude Sonnet 5.5):

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-5-5",
      "max_tokens": 16000,
      "thinking": {"type": "between_tools"},
      "output_config": {"effort": "high"},
      "messages": [{"role": "user", "content": "..."}]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-sonnet-5-5 \
    --max-tokens 16000 \
    --thinking '{type: between_tools}' \
    --output-config '{effort: high}' \
    --message '{role: user, content: "..."}'
  ```

  ```python Python
  client.messages.create(
      model="claude-sonnet-5-5",
      max_tokens=16000,
      thinking={"type": "between_tools"},
      output_config={"effort": "high"},
      messages=[{"role": "user", "content": "..."}],
  )
  ```

  ```typescript TypeScript
  await client.messages.create({
    model: "claude-sonnet-5-5",
    max_tokens: 16000,
    thinking: { type: "between_tools" },
    output_config: { effort: "high" },
    messages: [{ role: "user", content: "..." }]
  });
  ```

  ```csharp C#
  await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5_5,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigBetweenTools(),
      OutputConfig = new() { Effort = Effort.High },
      Messages = [new() { Role = Role.User, Content = "..." }],
  });
  ```

  ```go Go
  client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet5_5,
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfBetweenTools: &anthropic.ThinkingConfigBetweenToolsParam{},
  	},
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortHigh,
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
  	},
  })
  ```

  ```java Java
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_SONNET_5_5)
      .maxTokens(16000L)
      .thinking(ThinkingConfigBetweenTools.builder().build())
      .outputConfig(OutputConfig.builder()
          .effort(OutputConfig.Effort.HIGH)
          .build())
      .addUserMessage("...")
      .build();

  client.messages().create(params);
  ```

  ```php PHP
  $client->messages->create(
      model: Model::CLAUDE_SONNET_5_5,
      maxTokens: 16000,
      thinking: ThinkingConfigBetweenTools::with(),
      outputConfig: OutputConfig::with(effort: Effort::HIGH),
      messages: [['role' => 'user', 'content' => '...']],
  );
  ```

  ```ruby Ruby
  client.messages.create(
    model: Anthropic::Model::CLAUDE_SONNET_5_5,
    max_tokens: 16000,
    thinking: Anthropic::ThinkingConfigBetweenTools.new,
    output_config: { effort: Anthropic::OutputConfig::Effort::HIGH },
    messages: [{ role: "user", content: "..." }]
  )
  ```
</CodeGroup>

## Daftar periksa migrasi berdasarkan model awal

Kerjakan grup-grup berikut secara berurutan dan berhenti setelah grup yang menyebutkan model Anda. Di Claude Haiku 4.5, terapkan setiap grup kecuali "Claude Sonnet 4 atau sebelumnya", dan akhiri dengan "Hanya Claude Haiku 4.5".

### Setiap model awal

* Ubah ID model menjadi `claude-sonnet-5-5`.
* [Baca blok konten berdasarkan `type`](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#thinking-in-responses), dan kirim kembali blok `thinking` tanpa perubahan.
* Agar tetap berjalan tanpa thinking di awal, kirim [pengaturan thinking terendah](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#turn-off-up-front-thinking) pada effort `high` atau lebih rendah.
* Ganti [penggunaan alat paksa](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#forced-tool-use) dengan `auto` dan alat strict, atau dengan `auto` saja di Amazon Bedrock.
* Pertahankan percakapan agar [hanya ditambahkan (append-only)](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#thinking-blocks).
* Di Claude API dan Google Cloud, pindahkan computer use ke [toolset](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#computer-use-toolset), tanpa beta header `fine-grained-tool-streaming-2025-05-14`.
* Pasangkan [alat advisor](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#advisor-tool) dengan advisor yang didukung, dan perkirakan saran yang terenkripsi.
* Baca [teks di antara panggilan alat](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#text-between-tool-calls) dari blok `thinking`.
* [Tangani penolakan](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#safety-classifiers-and-fallback), dan konfigurasikan fallback.
* [Jalankan ulang sweep effort Anda](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#recommended-changes), dan tetapkan ulang baseline biaya.

### Claude Sonnet 4.6 atau sebelumnya

* Perkirakan [pemikiran pada permintaan tanpa field `thinking`](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#thinking-on-by-default), dan tinjau kembali `max_tokens`.
* Ganti [anggaran pemikiran](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#sonnet-46-breaking-changes) dengan tingkat effort.
* Hapus nilai `temperature`, `top_p`, dan `top_k` yang bukan default.
* Jika Anda [menampilkan teks pemikiran](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#thinking-in-responses), tetapkan `display: "summarized"`.
* [Hitung ulang token](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#other-changes-from-claude-sonnet-4-6), dan anggarkan ulang token gambar.

### Claude Sonnet 4.5 atau sebelumnya

* Ganti [prefill asisten](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#migrating-from-sonnet-45).
* Parse input pemanggilan alat dengan parser JSON standar.
* Di Amazon Bedrock, pindahkan computer use dari `computer_20250124` ke [`computer_20251124`](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#computer-use-toolset).
* Tetapkan `output_config.effort` secara eksplisit.
* Hapus beta header jendela konteks apa pun.
* Hapus `interleaved-thinking-2025-05-14`, dan ganti `fine-grained-tool-streaming-2025-05-14` dengan `eager_input_streaming`.
* Pindahkan `output_format` ke `output_config.format`.

### Claude Sonnet 4 atau sebelumnya

* Perbarui [versi alat](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#migrating-from-claude-sonnet-4-or-earlier) ke `text_editor_20250728` dan `code_execution_20260521`.
* Tangani stop reason `refusal` dan `model_context_window_exceeded`.
* Periksa parameter string alat untuk baris baru di akhir.
* Hapus `token-efficient-tools-2025-02-19` dan `output-128k-2025-02-19`.
* Tinjau prompt Anda.

### Hanya Claude Haiku 4.5

* Ganti [`claude-haiku-4-5-20251001`](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#migrating-from-claude-haiku-4-5) atau alias-nya.
* Tetapkan ulang baseline biaya dengan harga per token yang lebih tinggi.
* Tinjau prompt yang terlalu pendek untuk di-cache di Claude Haiku 4.5.

## Migrasi ke Claude Sonnet 5.5 dari Claude Sonnet 5

Setiap model awal memerlukan perubahan di bagian ini. Ganti ID model Anda dengan `claude-sonnet-5-5`, yang tidak memiliki akhiran tanggal. Di platform lain, gunakan ID yang tercantum di bawah [Ketersediaan](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#availability).

### Penggunaan alat paksa tidak didukung

Setiap model sebelumnya di halaman ini menerima `tool_choice` dengan tipe `any` atau `tool`. Claude Sonnet 5.5 menolak keduanya dengan error 400, termasuk di endpoint [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting):

```text wrap
tool_choice: type "tool" and "any" are not supported for this model.
```

Kirim `tool_choice: {"type": "auto"}`, dan tandai alat dengan `strict: true` agar inputnya sesuai dengan skema. Model kemudian dapat menjawab tanpa memanggil alat, jadi sebutkan dalam prompt kapan harus menggunakannya. [Penggunaan alat strict](https://platform.claude.com/docs/id/agents-and-tools/tool-use/strict-tool-use) mendukung subset JSON Schema dan memerlukan `additionalProperties: false` pada setiap objek. Lihat [Batasan JSON Schema](https://platform.claude.com/docs/id/build-with-claude/structured-outputs#json-schema-limitations). Di Amazon Bedrock, ["structured outputs" (output terstruktur)](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), yang mencakup penggunaan alat strict, tidak tersedia untuk Claude Sonnet 5.5. Di sana, kirim `auto` tanpa `strict`, sebutkan dalam prompt kapan harus memanggil alat, dan validasi input alat dalam kode Anda.

Sebelum (Claude Sonnet 5):

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-5",
      "max_tokens": 1024,
      "tools": [{
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"],
          "additionalProperties": false
        }
      }],
      "tool_choice": {"type": "tool", "name": "get_weather"},
      "messages": [{"role": "user", "content": "What'\''s the weather in Paris?"}]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-sonnet-5
  max_tokens: 1024
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city and state, e.g. San Francisco, CA
        required: [location]
        additionalProperties: false
  tool_choice:
    type: tool
    name: get_weather
  messages:
    - role: user
      content: What's the weather in Paris?
  YAML
  ```

  ```python Python
  client.messages.create(
      model="claude-sonnet-5",
      max_tokens=1024,
      tools=tools,
      tool_choice={"type": "tool", "name": "get_weather"},
      messages=[{"role": "user", "content": "What's the weather in Paris?"}],
  )
  ```

  ```typescript TypeScript
  await client.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 1024,
    tools,
    tool_choice: { type: "tool", name: "get_weather" },
    messages: [{ role: "user", content: "What's the weather in Paris?" }]
  });
  ```

  ```csharp C#
  await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 1024,
      Tools = [.. tools],
      ToolChoice = new ToolChoiceTool { Name = "get_weather" },
      Messages = [new() { Role = Role.User, Content = "What's the weather in Paris?" }],
  });
  ```

  ```go Go
  client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:      anthropic.ModelClaudeSonnet5,
  	MaxTokens:  1024,
  	Tools:      tools,
  	ToolChoice: anthropic.ToolChoiceParamOfTool("get_weather"),
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in Paris?")),
  	},
  })
  ```

  ```java Java
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_SONNET_5)
      .maxTokens(1024L)
      .tools(tools)
      .toolChoice(ToolChoiceTool.of("get_weather"))
      .addUserMessage("What's the weather in Paris?")
      .build();

  client.messages().create(params);
  ```

  ```php PHP
  $client->messages->create(
      model: Model::CLAUDE_SONNET_5,
      maxTokens: 1024,
      tools: $tools,
      toolChoice: ToolChoiceTool::with(name: 'get_weather'),
      messages: [['role' => 'user', 'content' => "What's the weather in Paris?"]],
  );
  ```

  ```ruby Ruby
  client.messages.create(
    model: Anthropic::Model::CLAUDE_SONNET_5,
    max_tokens: 1024,
    tools: tools,
    tool_choice: Anthropic::ToolChoiceTool.new(name: "get_weather"),
    messages: [{ role: "user", content: "What's the weather in Paris?" }]
  )
  ```
</CodeGroup>

Sesudah (Claude Sonnet 5.5):

<CodeGroup>
  ```bash cURL
  # penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-5-5",
      "max_tokens": 1024,
      "tools": [{
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"],
          "additionalProperties": false
        },
        "strict": true
      }],
      "tool_choice": {"type": "auto"},
      "messages": [{
        "role": "user",
        "content": "What'\''s the weather in Paris? Use the get_weather tool."
      }]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-sonnet-5-5
  max_tokens: 1024
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city and state, e.g. San Francisco, CA
        required: [location]
        additionalProperties: false
      # penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
      strict: true
  tool_choice:
    type: auto
  messages:
    - role: user
      content: What's the weather in Paris? Use the get_weather tool.
  YAML
  ```

  ```python Python
  client.messages.create(
      model="claude-sonnet-5-5",
      max_tokens=1024,
      # penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
      tools=[{**tool, "strict": True} for tool in tools],
      tool_choice={"type": "auto"},
      messages=[
          {
              "role": "user",
              "content": "What's the weather in Paris? Use the get_weather tool.",
          }
      ],
  )
  ```

  ```typescript TypeScript
  await client.messages.create({
    model: "claude-sonnet-5-5",
    max_tokens: 1024,
    // penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
    tools: tools.map((tool) => ({ ...tool, strict: true })),
    tool_choice: { type: "auto" },
    messages: [
      {
        role: "user",
        content: "What's the weather in Paris? Use the get_weather tool."
      }
    ]
  });
  ```

  ```csharp C#
  await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5_5,
      MaxTokens = 1024,
      // penggunaan alat ketat: setiap panggilan sesuai dengan input_schema milik alat
      Tools = [.. tools.Select(tool => tool with { Strict = true })],
      ToolChoice = new ToolChoiceAuto(),
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = "What's the weather in Paris? Use the get_weather tool.",
          },
      ],
  });
  ```

  ```go Go
  // penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
  var strictTools []anthropic.ToolUnionParam
  for _, tool := range tools {
  	strictTool := *tool.OfTool
  	strictTool.Strict = anthropic.Bool(true)
  	strictTools = append(strictTools, anthropic.ToolUnionParam{OfTool: &strictTool})
  }
  client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:      anthropic.ModelClaudeSonnet5_5,
  	MaxTokens:  1024,
  	Tools:      strictTools,
  	ToolChoice: anthropic.ToolChoiceUnionParam{OfAuto: &anthropic.ToolChoiceAutoParam{}},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewTextBlock("What's the weather in Paris? Use the get_weather tool."),
  		),
  	},
  })
  ```

  ```java Java
  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_SONNET_5_5)
      .maxTokens(1024L)
      // penggunaan alat ketat: setiap panggilan sesuai dengan input_schema milik alat
      .tools(tools.stream()
          .map(tool -> tool.tool()
              .map(customTool -> customTool.toBuilder().strict(true).build())
              .map(ToolUnion::ofTool)
              .orElse(tool))
          .toList())
      .toolChoice(ToolChoiceAuto.builder().build())
      .addUserMessage("What's the weather in Paris? Use the get_weather tool.")
      .build();

  client.messages().create(params);
  ```

  ```php PHP
  $client->messages->create(
      model: Model::CLAUDE_SONNET_5_5,
      maxTokens: 1024,
      // penggunaan alat ketat: setiap panggilan sesuai dengan input_schema milik alat
      tools: array_map(fn (Tool $tool) => $tool->withStrict(true), $tools),
      toolChoice: ToolChoiceAuto::with(),
      messages: [
          [
              'role' => 'user',
              'content' => "What's the weather in Paris? Use the get_weather tool.",
          ],
      ],
  );
  ```

  ```ruby Ruby
  client.messages.create(
    model: Anthropic::Model::CLAUDE_SONNET_5_5,
    max_tokens: 1024,
    # penggunaan alat ketat: setiap panggilan sesuai dengan input_schema alat
    tools: tools.map { |tool| tool.merge(strict: true) },
    tool_choice: Anthropic::ToolChoiceAuto.new,
    messages: [
      { role: "user", content: "What's the weather in Paris? Use the get_weather tool." }
    ]
  )
  ```
</CodeGroup>

Contoh ini menandai setiap alat dalam daftar sebagai strict. Sebuah permintaan dapat memiliki paling banyak 20 alat strict, dan entri toolset MCP, computer use, dan browser use tidak menerima `strict`. Dalam daftar alat yang lebih panjang, tandai hanya alat yang memerlukannya.

### Blok thinking terikat pada model dan percakapan

Claude Sonnet 5.5 membaca blok thinking dari Claude Sonnet 5, Claude Opus 4.8, Claude Haiku 4.5, dan model sebelumnya. Model ini tidak membaca blok dari Claude Opus 5, Claude Opus 5.5, atau model Claude Fable maupun Claude Mythos mana pun. API membuang blok yang tidak dapat dibaca oleh model. Permintaan tetap mengembalikan 200, dan blok yang dibuang tidak ditagih. Lihat [Beralih model di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#switching-models).

Setiap blok thinking Claude Sonnet 5.5 juga ditandatangani atas percakapan sebelumnya. Untuk akun yang dibuat pada atau setelah 31 Agustus 2026, 00:00 UTC, API memberlakukan hal ini secara default, di Claude API, Amazon Bedrock, dan Google Cloud. Pada akun tersebut, permintaan yang memutar ulang blok setelah pengeditan riwayat sebelumnya mengembalikan error 400. Pertahankan percakapan agar hanya ditambahkan, dan ubah instruksi atau alat dengan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages). Blok thinking yang dihasilkan Claude Sonnet 5.5 hanya berfungsi di akun yang menghasilkannya, atau di akun yang terhubung dengannya. Lihat [Pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking#account-bound-thinking).

### Computer use memerlukan toolset di Claude API dan Google Cloud

Di Claude API dan Google Cloud, Claude Sonnet 5.5 mendukung computer use hanya melalui toolset `computer_toolset_20260801`. Di sana, `computer_20251124` mengembalikan error 400. Claude Sonnet 5.5 tidak menerima `computer_20250124` di platform mana pun. Temukan versi yang Anda kirimkan saat ini:

| Versi yang Anda kirimkan saat ini | Model awal yang mengirimkannya                       | Kirimkan di Claude API dan Google Cloud | Kirimkan di Amazon Bedrock |
| --------------------------------- | ---------------------------------------------------- | --------------------------------------- | -------------------------- |
| `computer_20251124`               | Claude Sonnet 5, Claude Sonnet 4.6                   | `computer_toolset_20260801`             | `computer_20251124`        |
| `computer_20250124`               | Claude Sonnet 4.5, Claude Haiku 4.5, Claude Sonnet 4 | `computer_toolset_20260801`             | `computer_20251124`        |

Jika Anda mengirimkan beta header `fine-grained-tool-streaming-2025-05-14`, hapus header tersebut saat Anda berpindah ke toolset. Bersama entri toolset, header ini mengembalikan error 400. Sebagai gantinya, tetapkan `eager_input_streaming: true` pada setiap alat yang memerlukannya.

Kode yang sudah mengirimkan toolset tidak memerlukan perubahan. [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124) mencantumkan perubahan pada permintaan dan loop agen. Untuk platform lain, lihat [Kompatibilitas](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#compatibility).

### Alat advisor menerima lebih sedikit advisor

Dengan [alat advisor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool), executor Claude Sonnet 5.5 memerlukan salah satu advisor berikut: Claude Opus 5, Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5, Claude Fable 5.1, Claude Mythos 5, atau Claude Mythos 5.1. Advisor Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, dan Claude Sonnet 4.6 mengembalikan error 400. Saran dikembalikan dalam bentuk terenkripsi sebagai blok `advisor_redacted_result`, sehingga teksnya tidak dapat dibaca dalam respons. Lihat [Kompatibilitas model](https://platform.claude.com/docs/id/agents-and-tools/tool-use/advisor-tool#model-compatibility).

### Teks di antara pemanggilan alat dikembalikan dalam blok thinking

Di Claude Sonnet 5.5, catatan yang lebih panjang dari satu atau dua kalimat yang ditulis model di antara pemanggilan alat dikembalikan sebagai [blok `thinking` pembaruan progres](https://platform.claude.com/docs/id/build-with-claude/thinking#progress-updates), yang kosong pada `display` default. Komentar yang lebih pendek tetap berupa `text`. Di Claude Sonnet 5 dan model sebelumnya, semua teks di antara pemanggilan alat dikembalikan sebagai blok `text`. Tidak ada permintaan yang gagal, tetapi antarmuka yang menampilkan catatan tersebut menjadi sepi.

Dengan pemikiran adaptif, tetapkan `display` ke `"updates"` (beta, header `thinking-display-updates-2026-08-18`) untuk mendapatkan pembaruan saja, atau ke `"summarized"` untuk mendapatkannya bercampur dengan penalaran. Render setiap blok `thinking` yang tidak kosong sebelum blok `tool_use` yang mengikutinya. Dengan [`between_tools`](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#turn-off-up-front-thinking), teks dikembalikan tanpa `display`. Lihat [Pembaruan progres yang ditampilkan kepada pengguna](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#user-facing-progress-updates).

### Pengklasifikasi keamanan dan fallback

Claude Sonnet 5.5 menolak dalam lebih banyak kategori dibandingkan Claude Sonnet 5. Penolakan mengembalikan `stop_reason: "refusal"`, dan `stop_details`-nya dapat menyebutkan salah satu [kategori](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) berikut:

* **`"cyber"`:** Permintaan dapat memungkinkan bahaya siber, seperti pengembangan malware atau exploit.
* **`"bio"`:** Permintaan dapat memungkinkan bahaya biologis, seperti metode laboratorium yang berbahaya.
* **`"frontier_llm"`:** Permintaan dapat membantu pengembangan model AI pesaing.
* **`"reasoning_extraction"`:** Permintaan meminta model untuk mereproduksi penalaran internalnya dalam teks respons.
* **`"general_harms"`:** Permintaan termasuk dalam area kebijakan penggunaan lainnya. Pekerjaan yang tidak berbahaya juga dapat memicu kategori ini.

[Fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback) (`fallbacks: "default"`, beta, hanya Claude API) mencoba ulang penolakan `"cyber"` dan `"frontier_llm"` di Claude Sonnet 5. Fallback ini tidak mencoba ulang penolakan `"bio"`, `"reasoning_extraction"`, atau `"general_harms"`. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback) dan [Cara penolakan ditagih](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#how-refusals-are-billed).

Perlindungan siber real-time merupakan hal baru bagi kode dari Claude Sonnet 4.6, Claude Sonnet 4.5, dan Claude Haiku 4.5. Untuk pekerjaan keamanan yang sah, ajukan permohonan ke [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet).

### Perubahan lainnya

* **"Prompt caching" (caching prompt):** Prompt minimum yang dapat di-cache adalah 512 token, turun dari 1.024 di Claude Sonnet 5, Claude Sonnet 4.6, dan Claude Sonnet 4.5. Lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations).
* **Fitur baru:** Untuk pesan sistem di tengah percakapan, perubahan alat di tengah percakapan, dan effort per pesan, lihat [Yang baru di Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/whats-new-sonnet-5-5#feature-support). Dengan [`between_tools`](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#turn-off-up-front-thinking), effort tidak dapat berubah di tengah percakapan.

### Perubahan yang direkomendasikan

Jalankan ulang pengujian effort Anda. Claude Sonnet 5.5 memiliki lima tingkat effort: `low`, `medium`, `high`, `xhigh`, dan `max`. Default di Claude API adalah `high`. Tingkat-tingkat ini telah dikalibrasi ulang, sehingga suatu tingkat tidak menghasilkan jumlah pemikiran yang sama seperti di Claude Sonnet 5. Mulailah dari `high` kecuali beban kerja Anda bersifat agentik atau sensitif terhadap "latency" (latensi). Untuk coding agentik dan penggunaan alat multilangkah, mulailah dari `medium` untuk tugas yang terdefinisi dengan baik dan naikkan ke `high` untuk tugas yang lebih sulit atau lebih panjang. Untuk chat dan pekerjaan lain yang sensitif terhadap latensi, mulailah dari `medium` atau `low`. Tetapkan tingkat tersebut di `output_config.effort`. Lihat [Tingkat effort yang direkomendasikan untuk Claude Sonnet 5.5](https://platform.claude.com/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-sonnet-5-5). Kemudian evaluasi ulang instruksi prompt khusus model berdasarkan [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5).

## Migrasi ke Claude Sonnet 5.5 dari Claude Sonnet 4.6 dan model Sonnet sebelumnya

Pertama, terapkan setiap bagian sebelumnya, dengan mengganti `claude-sonnet-4-6`. Kemudian lakukan perubahan berikut. Di Claude Sonnet 4.5 atau sebelumnya, lanjutkan dengan subbagian yang mengikutinya.

### Perubahan yang merusak kompatibilitas

**Pemikiran berjalan pada permintaan yang tidak menyertakannya.** Lihat [Pemikiran berjalan secara default](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#thinking-on-by-default) dan [Menonaktifkan pemikiran di awal](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#turn-off-up-front-thinking).

**Anggaran pemikiran mengembalikan error.** Claude Sonnet 4.6 menerima `thinking: {"type": "enabled", "budget_tokens": N}` sebagai pengaturan yang usang. Claude Sonnet 4.5 dan Claude Haiku 4.5 menggunakannya untuk semua pemikiran. Claude Sonnet 5.5 mengembalikan error 400:

```text wrap
"thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

Hapus anggaran tersebut dan tetapkan tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort). Tidak ada pemetaan tetap dari anggaran ke tingkat effort, jadi jalankan evaluasi Anda pada dua atau tiga tingkat.

Sebelum (Claude Sonnet 4.6):

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-6",
      "max_tokens": 16000,
      "thinking": {
        "type": "enabled",
        "budget_tokens": 10000
      },
      "messages": [
        {
          "role": "user",
          "content": "..."
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-sonnet-4-6
  max_tokens: 16000
  thinking:
    type: enabled
    budget_tokens: 10000
  messages:
    - role: user
      content: "..."
  YAML
  ```

  ```python Python
  client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=16000,
      thinking={"type": "enabled", "budget_tokens": 10000},
      messages=[{"role": "user", "content": "..."}],
  )
  ```

  ```typescript TypeScript
  await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 16000,
    thinking: { type: "enabled", budget_tokens: 10000 },
    messages: [{ role: "user", content: "..." }]
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = "claude-sonnet-4-6",
      MaxTokens = 16000,
      Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
      Messages = [new() { Role = Role.User, Content = "..." }]
  };

  var response = await client.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-sonnet-4-6",
  	MaxTokens: 16000,
  	Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model("claude-sonnet-4-6")
      .maxTokens(16000L)
      .enabledThinking(10000L)
      .addUserMessage("...")
      .build();

  Message response = client.messages().create(params);
  IO.println(response);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 16000,
      messages: [['role' => 'user', 'content' => '...']],
      model: 'claude-sonnet-4-6',
      thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 16000,
    thinking: {
      type: "enabled",
      budget_tokens: 10000
    },
    messages: [
      { role: "user", content: "..." }
    ]
  )
  ```
</CodeGroup>

Sesudah (Claude Sonnet 5.5):

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-5-5",
      "max_tokens": 16000,
      "thinking": {
        "type": "adaptive"
      },
      "output_config": {
        "effort": "high"
      },
      "messages": [
        {
          "role": "user",
          "content": "..."
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-sonnet-5-5
  max_tokens: 16000
  thinking:
    type: adaptive
  output_config:
    effort: high
  messages:
    - role: user
      content: "..."
  YAML
  ```

  ```python Python
  client.messages.create(
      model="claude-sonnet-5-5",
      max_tokens=16000,
      thinking={"type": "adaptive"},
      output_config={"effort": "high"},  # or "max", "xhigh", "medium", "low"
      messages=[{"role": "user", "content": "..."}],
  )
  ```

  ```typescript TypeScript
  await client.messages.create({
    model: "claude-sonnet-5-5",
    max_tokens: 16000,
    thinking: { type: "adaptive" },
    output_config: { effort: "high" }, // or "max", "xhigh", "medium", "low"
    messages: [{ role: "user", content: "..." }]
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = "claude-sonnet-5-5",
      MaxTokens = 16000,
      Thinking = new ThinkingConfigAdaptive(),
      OutputConfig = new OutputConfig { Effort = Effort.High }, // or Max, Xhigh, Medium, Low
      Messages = [new() { Role = Role.User, Content = "..." }]
  };

  var response = await client.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-sonnet-5-5",
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
  	},
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortHigh, // or Max, Xhigh, Medium, Low
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model("claude-sonnet-5-5")
      .maxTokens(16000L)
      .thinking(ThinkingConfigAdaptive.builder().build())
      .outputConfig(OutputConfig.builder()
          .effort(OutputConfig.Effort.HIGH) // or MAX, XHIGH, MEDIUM, LOW
          .build())
      .addUserMessage("...")
      .build();

  Message response = client.messages().create(params);
  IO.println(response);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 16000,
      messages: [['role' => 'user', 'content' => '...']],
      model: 'claude-sonnet-5-5',
      thinking: ['type' => 'adaptive'],
      outputConfig: ['effort' => 'high'], // or 'max', 'xhigh', 'medium', 'low'
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-sonnet-5-5",
    max_tokens: 16000,
    thinking: {
      type: "adaptive"
    },
    output_config: {
      effort: "high" # or "max", "xhigh", "medium", "low"
    },
    messages: [
      { role: "user", content: "..." }
    ]
  )
  ```
</CodeGroup>

**Parameter sampling mengembalikan error.** Claude Sonnet 4.6 dan model sebelumnya serta Claude Haiku 4.5 menerima `temperature`, `top_p`, dan `top_k`. Di Claude Sonnet 5.5, nilai yang bukan default mengembalikan error 400. Hapus parameter tersebut.

**Teks pemikiran dihilangkan secara default.** Lihat [Menangani pemikiran dalam respons](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#thinking-in-responses).

### Perubahan lainnya

* **Sekitar 30% lebih banyak token:** Claude Sonnet 5.5 menggunakan tokenizer Claude Sonnet 5. Dibandingkan dengan Claude Sonnet 4.6, Claude Sonnet 4.5, dan Claude Haiku 4.5, teks yang sama menghasilkan sekitar 30% lebih banyak token, tergantung pada kontennya. Hitung ulang dengan [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting), dan tinjau kembali `max_tokens` serta biaya.
* **Effort:** `xhigh` adalah tingkat baru, dan tingkat-tingkat lainnya telah dikalibrasi ulang. Lihat [Perubahan yang direkomendasikan](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#recommended-changes).
* **Gambar:** Claude Sonnet 5.5 menggunakan tingkat gambar resolusi tinggi, hingga 2576 piksel pada sisi terpanjang dan 4.784 token visual per gambar. Claude Sonnet 4.6, Claude Sonnet 4.5, dan Claude Haiku 4.5 berhenti pada 1568 piksel dan 1.568 token. Gambar berukuran 2000×1500 memerlukan sekitar 2,5 kali lebih banyak token di Claude Sonnet 5.5. Lihat [Resolusi dan biaya token](https://platform.claude.com/docs/id/build-with-claude/vision#evaluate-image-size).

### Migrasi dari Claude Sonnet 4.5 atau sebelumnya

Di Claude Sonnet 4.5, Claude Sonnet 4, atau Claude 3.7 Sonnet, pertama terapkan setiap bagian sebelumnya, lalu perubahan berikut.

**Prefill mengembalikan error.** Claude Sonnet 5.5 menolak giliran asisten terakhir yang di-prefill dengan error 400, sama seperti Claude Sonnet 4.6 dan Claude Sonnet 5. Claude Sonnet 4.5, Claude Haiku 4.5, dan model yang lebih lama menerimanya. Error-nya berbunyi:

```text wrap
This model does not support assistant message prefill. The conversation must end with a user message.
```

Ganti setiap prefill sesuai dengan tujuannya:

* **Format output:** gunakan [output terstruktur](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), atau alat dengan field enum untuk klasifikasi. Di Amazon Bedrock, output terstruktur tidak tersedia untuk Claude Sonnet 5.5. Di sana, jelaskan format dalam prompt atau gunakan alat tanpa `strict`, dan validasi output dalam kode Anda.
* **Pembukaan:** minta jawaban langsung dalam prompt sistem.
* **Penolakan yang tidak diinginkan:** instruksi yang jelas dalam pesan pengguna biasanya sudah cukup.
* **Kelanjutan:** pindahkan ke pesan pengguna, misalnya "Respons Anda sebelumnya terputus dan berakhir dengan `[previous_response]`. Lanjutkan dari bagian terakhir."
* **Pengingat konteks:** letakkan di giliran pengguna.

**Escaping input alat.** Escaping dalam argumen pemanggilan alat dapat berbeda. Parse `input` dengan parser JSON standar.

**Computer use.** Claude Sonnet 5.5 tidak menerima `computer_20250124`. Lihat [tabel computer use](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#computer-use-toolset).

**Effort.** Claude Sonnet 4.5 tidak memiliki parameter effort. Tetapkan tingkat effort secara eksplisit, seperti yang dijelaskan dalam [Perubahan yang direkomendasikan](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#recommended-changes).

**Konteks dan output.** Claude Sonnet 5.5 memiliki jendela konteks yang lebih besar, tanpa beta header, dan batas output yang lebih tinggi. Lihat [halaman model](https://platform.claude.com/docs/id/models/sonnet-5-5/overview). Hapus beta header jendela konteks apa pun.

**Beta header.** Hapus `interleaved-thinking-2025-05-14`, karena pemikiran adaptif menyisipkan pemikiran secara otomatis. Ganti `fine-grained-tool-streaming-2025-05-14` dengan `eager_input_streaming: true` pada setiap alat yang memerlukannya. Header tersebut mengembalikan error 400 bila digunakan bersama entri toolset computer use atau browser use. Lihat [Streaming alat fine-grained](https://platform.claude.com/docs/id/agents-and-tools/tool-use/fine-grained-tool-streaming).

**Output terstruktur.** Parameter `output_format` sudah usang dan akan dihapus di masa mendatang. Untuk tetap menggunakannya, tambahkan beta header `structured-outputs-2025-11-13`. Tanpa header tersebut, API mengembalikan error 400. Gunakan `output_config.format` sebagai gantinya.

### Migrasi dari Claude Sonnet 4 atau sebelumnya

Claude Sonnet 4 telah dihentikan di Claude API dan masih tersedia di Amazon Bedrock dan Google Cloud. Claude 3.7 Sonnet telah dihentikan. Dari salah satu model tersebut, pertama terapkan setiap bagian sebelumnya, lalu perubahan berikut:

* **Versi alat:** Gunakan `text_editor_20250728`, dengan nama alat `str_replace_based_edit_tool` dan tanpa perintah `undo_edit`. Gunakan `code_execution_20260521`. Lihat [alat text editor](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool) dan [alat code execution](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version).
* **Stop reason:** Tangani `refusal`. Claude 4.5 dan model yang lebih baru juga berhenti dengan `model_context_window_exceeded` pada batas jendela konteks. Lihat [Menangani stop reason](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons).
* **Baris baru di akhir:** Claude 4.5 dan model yang lebih baru mempertahankannya dalam parameter string pemanggilan alat.
* **Beta header lama:** Hapus `token-efficient-tools-2025-02-19` dan `output-128k-2025-02-19`.
* **Prompt:** Tinjau prompt Anda berdasarkan [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices).

## Migrasi ke Claude Sonnet 5.5 dari Claude Haiku 4.5

Pertama, terapkan setiap bagian hingga dan termasuk [Migrasi dari Claude Sonnet 4.5 atau sebelumnya](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#migrating-from-sonnet-45), dengan melewati subbagian Claude Sonnet 4. Kemudian lakukan perubahan berikut:

* **ID model:** Ganti `claude-haiku-4-5-20251001`, atau alias `claude-haiku-4-5`, dengan `claude-sonnet-5-5`.
* **Biaya:** Harga per token lebih tinggi, dan teks yang sama menghasilkan lebih banyak token. Hitung ulang token dan tetapkan ulang baseline biaya. Lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).
* **Caching prompt:** Prompt minimum yang dapat di-cache turun dari 4.096 token ke [minimum Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/migration-guide#other-changes-from-claude-sonnet-5).
* **Pemikiran yang disisipkan:** Pemikiran adaptif berjalan di antara pemanggilan alat secara otomatis, tanpa beta header.
* **Routing:** Claude Sonnet 5.5 membaca blok thinking Claude Haiku 4.5. Percakapan yang berpindah ke model yang lebih tinggi mempertahankan penalarannya. Percakapan yang kembali turun ke Claude Haiku 4.5 membuang blok milik Claude Sonnet 5.5.
