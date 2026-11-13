---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/effort-per-message
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: fe4934e7cb4970e3595322d161b2ee56c0ee31e62ba9c18e15784ff943fbfa51
---

---
title: Effort per pesan
url: https://platform.claude.com/docs/id/build-with-claude/effort-per-message
description: Gunakan pesan sistem untuk mengubah tingkat effort di tengah percakapan dan mempertahankan cache prompt.
featureMetadata:
  status: beta
  betaHeader: mid-conversation-output-config-2026-07-01
  supportedModels:
    - claude-fable-5-2
    - claude-mythos-5-2
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-haiku-5-5
  supportedPlatforms:
    Claude API: beta
    Amazon Bedrock: beta
    Amazon Bedrock (bedrock-runtime):
      availability: beta
      note: Kirim nilai beta dalam array `anthropic_beta` pada body permintaan.
    Claude Platform on AWS: beta
    Claude Models on Google Cloud (Anthropic managed): beta
    Claude Models on Google Cloud (Google managed): beta
    Microsoft Foundry: beta
---

Perubahan effort per pesan menetapkan tingkat effort baru untuk giliran-giliran berikutnya dalam percakapan tanpa mengubah nilai tingkat atas permintaan, sehingga prefiks yang di-cache tetap cocok.

## Mengubah tingkat effort

Untuk mengubah tingkat di tengah percakapan:

1. Tambahkan pesan `role: "system"` ke `messages`, dengan `content` kosong dan tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) baru di `output_config.effort`.
2. Kirim [header beta](https://platform.claude.com/docs/id/api/beta-headers) `mid-conversation-output-config-2026-07-01`.
3. Biarkan nilai tingkat atas tidak berubah.

Contoh berikut mempertahankan nilai tingkat atas pada `high` dan beralih ke `low` untuk tindak lanjut rutin:

<CodeGroup>
  ```bash cURL
  # Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: mid-conversation-output-config-2026-07-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 4096,
      "output_config": {"effort": "high"},
      "messages": [
        {"role": "user", "content": "Plan a migration from SQLite to PostgreSQL in three short steps."},
        {"role": "assistant", "content": "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts."},
        {"role": "system", "content": [], "output_config": {"effort": "low"}},
        {"role": "user", "content": "Summarize the plan in one sentence."}
      ]
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta mid-conversation-output-config-2026-07-01 <<'YAML'
  model: claude-opus-5-5
  max_tokens: 4096
  output_config:
    effort: high
  messages:
    - role: user
      content: Plan a migration from SQLite to PostgreSQL in three short steps.
    - role: assistant
      content: "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts."
    # Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
    - role: system
      content: []
      output_config:
        effort: low
    - role: user
      content: Summarize the plan in one sentence.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-5-5",
      max_tokens=4096,
      output_config={"effort": "high"},
      messages=[
          {
              "role": "user",
              "content": "Plan a migration from SQLite to PostgreSQL in three short steps.",
          },
          {
              "role": "assistant",
              "content": "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.",
          },
          # Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
          {"role": "system", "content": [], "output_config": {"effort": "low"}},
          {"role": "user", "content": "Summarize the plan in one sentence."},
      ],
      betas=["mid-conversation-output-config-2026-07-01"],
  )

  for block in response.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 4096,
    output_config: { effort: "high" },
    messages: [
      {
        role: "user",
        content: "Plan a migration from SQLite to PostgreSQL in three short steps."
      },
      {
        role: "assistant",
        content:
          "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts."
      },
      // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
      { role: "system", content: [], output_config: { effort: "low" } },
      { role: "user", content: "Summarize the plan in one sentence." }
    ],
    betas: ["mid-conversation-output-config-2026-07-01"]
  });

  for (const block of response.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  // ...

  AnthropicClient client = new();

  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5_5,
      MaxTokens = 4096,
      OutputConfig = new() { Effort = Effort.High },
      Messages =
      [
          new BetaUserMessageParam { Content = "Plan a migration from SQLite to PostgreSQL in three short steps." },
          new BetaAssistantMessageParam { Content = "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts." },
          // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
          new BetaSystemMessageParam
          {
              Content = new([]),
              OutputConfig = new() { Effort = BetaSystemMessageOutputConfigEffort.Low },
          },
          new BetaUserMessageParam { Content = "Summarize the plan in one sentence." },
      ],
      Betas = [AnthropicBeta.MidConversationOutputConfig2026_07_01],
  });

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var textBlock))
      {
          Console.WriteLine(textBlock.Text);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 4096,
  	OutputConfig: anthropic.BetaOutputConfigParam{
  		Effort: anthropic.BetaOutputConfigEffortHigh,
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Plan a migration from SQLite to PostgreSQL in three short steps.")),
  		{OfAssistant: &anthropic.BetaAssistantMessageParam{
  			Content: []anthropic.BetaContentBlockParamUnion{anthropic.NewBetaTextBlock("1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.")},
  		}},
  		// Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
  		anthropic.NewBetaSystemMessage(anthropic.BetaSystemMessageOutputConfigParam{
  			Effort: anthropic.BetaSystemMessageOutputConfigEffortLow,
  		}),
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Summarize the plan in one sentence.")),
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaMidConversationOutputConfig2026_07_01},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range response.Content {
  	if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.beta.AnthropicBeta;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaOutputConfig;
  import com.anthropic.models.beta.messages.BetaSystemMessageOutputConfig;
  import com.anthropic.models.beta.messages.BetaSystemMessageParam;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(4096L)
          .addBeta(AnthropicBeta.MID_CONVERSATION_OUTPUT_CONFIG_2026_07_01)
          .outputConfig(BetaOutputConfig.builder()
              .effort(BetaOutputConfig.Effort.HIGH)
              .build())
          .addUserMessage("Plan a migration from SQLite to PostgreSQL in three short steps.")
          .addAssistantMessage("1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.")
          // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
          .addMessage(BetaSystemMessageParam.builder()
              .contentOfBlocks(List.of())
              .outputConfig(BetaSystemMessageOutputConfig.builder()
                  .effort(BetaSystemMessageOutputConfig.Effort.LOW)
                  .build())
              .build())
          .addUserMessage("Summarize the plan in one sentence.")
          .build();

      BetaMessage response = client.beta().messages().create(params);
      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  use Anthropic\Beta\AnthropicBeta;
  use Anthropic\Beta\Messages\BetaMessageParam;
  use Anthropic\Beta\Messages\BetaOutputConfig;
  use Anthropic\Beta\Messages\BetaSystemMessageOutputConfig;
  use Anthropic\Beta\Messages\BetaTextBlock;
  // ...

  $client = new Client();

  $response = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 4096,
      outputConfig: BetaOutputConfig::with(effort: 'high'),
      messages: [
          BetaMessageParam::with(role: 'user', content: 'Plan a migration from SQLite to PostgreSQL in three short steps.'),
          BetaMessageParam::with(role: 'assistant', content: '1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts.'),
          // Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
          BetaMessageParam::with(
              role: 'system',
              content: [],
              outputConfig: BetaSystemMessageOutputConfig::with(effort: 'low'),
          ),
          BetaMessageParam::with(role: 'user', content: 'Summarize the plan in one sentence.'),
      ],
      betas: [AnthropicBeta::MID_CONVERSATION_OUTPUT_CONFIG_2026_07_01],
  );

  foreach ($response->content as $block) {
      if ($block instanceof BetaTextBlock) {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 4096,
    output_config: { effort: :high },
    messages: [
      { role: "user", content: "Plan a migration from SQLite to PostgreSQL in three short steps." },
      { role: "assistant", content: "1. Export the SQLite data. 2. Create the PostgreSQL schema. 3. Import the data and verify row counts." },
      # Pesan sistem khusus effort: level baru berlaku mulai giliran pengguna berikutnya.
      { role: "system", content: [], output_config: { effort: :low } },
      { role: "user", content: "Summarize the plan in one sentence." }
    ],
    betas: [Anthropic::AnthropicBeta::MID_CONVERSATION_OUTPUT_CONFIG_2026_07_01]
  )

  response.content.each do |block|
    case block
    when Anthropic::Beta::BetaTextBlock
      puts block.text
    end
  end
  ```
</CodeGroup>

Posisi pesan menentukan kapan tingkat baru mulai berlaku:

* Tepat setelah giliran `user` dengan input baru: balasan Claude untuk giliran tersebut menggunakan tingkat yang baru.
* Di posisi lain mana pun, seperti di antara giliran `assistant` dan giliran `user` berikutnya seperti pada contoh sebelumnya: tingkat yang baru mulai berlaku pada giliran `user` berikutnya dengan input baru.

Giliran `user` yang hanya berisi blok `tool_result` tidak dianggap sebagai input baru.

Tingkat yang baru tetap berlaku sampai pesan selanjutnya mengubahnya.

Letakkan pesan tersebut setelah semua yang telah Anda kirim, dan pertahankan di tempatnya pada permintaan-permintaan berikutnya. Jangan menyisipkannya sebelum giliran yang telah Anda kirim, dan jangan memindahkan atau menghapusnya di kemudian hari. Pada model dengan [pemikiran yang dipertahankan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking), perubahan apa pun tersebut membuat blok thinking di giliran `assistant` setelah pesan tersebut menjadi tidak valid. Untuk mengetahui apa yang terjadi selanjutnya, lihat [Atur `prefix_mismatch_behavior`](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#mismatch-behavior).

Jika pesan ini berada di samping pesan `system` yang memiliki konten, kedua pesan harus mengikuti [aturan penempatan untuk pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations).

Dengan InvokeModel API Amazon Bedrock, kirim nilai beta di array `anthropic_beta` pada body permintaan, bukan di header. Untuk model yang mendukung effort per pesan di sana, lihat [Pesan sistem di tengah percakapan di Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy#mid-conversation-system-messages-on-bedrock).

## Error

* Tanpa header beta, `output_config` per pesan mengembalikan error 400: `messages.N.output_config: Extra inputs are not permitted`, dengan `N` adalah indeks pesan `system` di `messages`.
* Dengan header beta, model yang tidak mendukung effort per pesan, seperti Claude Fable 5, mengembalikan error 400: `output_config.effort requires a model that supports per-turn effort; this model does not`. Di Amazon Bedrock, model-model tersebut dan Claude Opus 5 mengembalikan `Extra inputs are not permitted` sebagai gantinya.
* Pada Claude Sonnet 5.5 dengan `thinking: {"type": "between_tools"}`, dan pada Claude Haiku 5.5 dengan `thinking: {"type": "disabled"}`, Anda tidak dapat mengubah tingkat effort di tengah percakapan. Di sana, `output_config.effort` per pesan dengan tingkat baru mengembalikan error 400. Untuk memvariasikan effort pada setiap giliran, gunakan adaptive thinking.

## Effort per pesan atau tingkat atas

Utamakan effort per pesan daripada [mengubah nilai tingkat atas](https://platform.claude.com/docs/id/build-with-claude/effort#top-level-effort-on-the-next-request) di antara permintaan. Perubahan per pesan membiarkan semua yang ada sebelumnya tidak berubah, sehingga prefiks yang di-cache tetap cocok. Perubahan tingkat atas dapat membuat seluruh atau sebagian cache menjadi tidak valid. Pada Claude Fable 5.1, perubahan tingkat atas juga mengarahkan model dengan kurang andal. Balasan-balasan model sebelumnya ditulis pada tingkat sebelumnya, dan model cenderung tetap konsisten dengan balasan tersebut.

## Ketersediaan

Effort per pesan dalam versi beta di model tertentu.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tersedia

| Status           | Platform cloud                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Model                                                                                                                                                                                                                                                                                                                                      |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Beta             | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) | [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview)                                                                                                                                                                         |
| Beta<sup>1</sup> | [Amazon Bedrock (bedrock-runtime)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | [Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/overview), [Claude Mythos 5.2](https://platform.claude.com/docs/id/models/mythos-5-2/overview), [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview) |
| Beta             | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)                                                                                                   | [Claude Fable 5.2](https://platform.claude.com/docs/id/models/fable-5-2/overview), [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview)     |
| Beta             | Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), [Microsoft Foundry (hosted on Anthropic)](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)                                                                                                                                                                                                                                               | [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview)                                                                                                                                                                                                                                                        |
| Beta             | Claude API, [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed), [Microsoft Foundry (hosted on Anthropic)](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry)                                                                                                                                                                                     | [Claude Mythos 5.2](https://platform.claude.com/docs/id/models/mythos-5-2/overview)                                                                                                                                                                                                                                                        |

1. Kirim nilai beta dalam array `anthropic_beta` pada body permintaan.

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tidak tersedia
* Penggunaan: Sebagai gantinya, atur effort untuk sesi dengan meng-override pengaturan model agen.

### Header beta yang diperlukan

[Ikhtisar header beta](https://platform.claude.com/docs/id/api/beta-headers)

Header beta memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

* `mid-conversation-output-config-2026-07-01`
