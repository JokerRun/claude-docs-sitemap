---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/extended-thinking
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: c46f2d476fc7532bae4a4a9a0e8504c1af4e32ecc4b2c05c93b4bc7282ceb14f
---

# Pemikiran diperpanjang

Berikan Claude penalaran yang ditingkatkan untuk tugas-tugas kompleks dan kendalikan bagaimana konten pemikiran dikembalikan.

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

"Extended thinking" (pemikiran diperpanjang) memberi Claude kemampuan penalaran yang ditingkatkan untuk tugas-tugas kompleks, sambil memberikan berbagai tingkat transparansi ke dalam proses berpikir langkah demi langkahnya sebelum memberikan jawaban akhirnya.

## Model yang didukung

Pemikiran diperpanjang tersedia di semua model Claude saat ini. Cara Anda mengaktifkannya bergantung pada modelnya:

| Model                                                    | Pemikiran diperpanjang manual (`budget_tokens`)                   | Direkomendasikan                                                                                                                                                |
| -------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Fable 5 Claude Mythos 5                           | Tidak didukung (error 400)                                        | [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), selalu aktif; gunakan [effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman |
| [Claude Mythos Preview](https://anthropic.com/glasswing) | Didukung                                                          | [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), aktif secara default                                                                         |
| Claude Opus 4.8                                          | Tidak didukung (error 400)                                        | [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [effort](/docs/id/build-with-claude/effort)                                            |
| Claude Opus 4.7                                          | Tidak didukung (error 400)                                        | [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [effort](/docs/id/build-with-claude/effort)                                            |
| Claude Sonnet 5                                          | Tidak didukung (error 400)                                        | [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [effort](/docs/id/build-with-claude/effort)                                            |
| Claude Opus 4.6                                          | [Usang](/docs/id/build-with-claude/overview#feature-availability) | [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [effort](/docs/id/build-with-claude/effort)                                            |
| Claude Sonnet 4.6                                        | [Usang](/docs/id/build-with-claude/overview#feature-availability) | [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [effort](/docs/id/build-with-claude/effort)                                            |
| Claude Opus 4.5                                          | Didukung                                                          | N/A                                                                                                                                                             |
| Claude Haiku 4.5                                         | Didukung                                                          | N/A                                                                                                                                                             |
| Model Claude 4 sebelumnya                                | Didukung                                                          | N/A                                                                                                                                                             |

Dengan adaptive thinking, model menentukan kapan dan seberapa banyak berpikir pada setiap permintaan. Pada Claude Mythos Preview, Claude Fable 5, dan Claude Mythos 5, `thinking: {type: "disabled"}` tidak didukung. Untuk perbedaan perilaku per model (output pemikiran, pemikiran tersisip, dan pelestarian blok), lihat [Perbedaan pemikiran di berbagai versi model](#differences-in-thinking-across-model-versions).

## Cara kerja pemikiran diperpanjang

Ketika pemikiran diperpanjang diaktifkan, Claude membuat blok konten `thinking` tempat ia mengeluarkan penalaran internalnya. Claude menggabungkan wawasan dari penalaran ini sebelum menyusun respons akhir.

Respons API menyertakan blok konten `thinking`, diikuti oleh blok konten `text`.

Berikut adalah contoh format respons default:

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me analyze this step by step...",
      "signature": "WaUjzkypQ2mUEVM36O2TxuC06KN8xyfbJwyem2dw3URve/op91XWHOEBLLqIOMfFG/UvLEczmEsUjavL...."
    },
    {
      "type": "text",
      "text": "Based on my analysis..."
    }
  ]
}
```

Untuk informasi lebih lanjut tentang format respons pemikiran diperpanjang, lihat [Referensi Messages API](/docs/id/api/messages/create).

## Cara menggunakan pemikiran diperpanjang

Berikut adalah contoh penggunaan pemikiran diperpanjang di Messages API:

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
          "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --transform content --format yaml <<'YAML'
  model: claude-sonnet-4-6
  max_tokens: 16000
  thinking:
    type: enabled
    budget_tokens: 10000
  messages:
    - role: user
      content: Are there an infinite number of prime numbers such that n mod 4 == 3?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=16000,
      thinking={"type": "enabled", "budget_tokens": 10000},
      messages=[
          {
              "role": "user",
              "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?",
          }
      ],
  )

  # Respons berisi blok pemikiran yang diringkas dan blok teks
  for block in response.content:
      match block.type:
          case "thinking":
              print(f"\nThinking summary: {block.thinking}")
          case "text":
              print(f"\nResponse: {block.text}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 16000,
    thinking: {
      type: "enabled",
      budget_tokens: 10000,
    },
    messages: [
      {
        role: "user",
        content: "Are there an infinite number of prime numbers such that n mod 4 == 3?",
      },
    ],
  });

  // Respons berisi blok pemikiran yang diringkas dan blok teks
  for (const block of response.content) {
    if (block.type === "thinking") {
      console.log(`\nThinking summary: ${block.thinking}`);
    } else if (block.type === "text") {
      console.log(`\nResponse: ${block.text}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var response = await client.Messages.Create(new()
  {
      Model = Model.ClaudeSonnet4_6,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = "Are there an infinite number of prime numbers such that n mod 4 == 3?",
          },
      ],
  });

  // Respons berisi blok pemikiran yang diringkas dan blok teks
  foreach (var block in response.Content)
  {
      if (block.TryPickThinking(out var thinking))
      {
          Console.WriteLine($"\nThinking summary: {thinking.Thinking}");
      }
      else if (block.TryPickText(out var text))
      {
          Console.WriteLine($"\nResponse: {text.Text}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet4_6,
  	MaxTokens: 16000,
  	Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Are there an infinite number of prime numbers such that n mod 4 == 3?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Respons berisi blok pemikiran yang diringkas dan blok teks
  for _, block := range response.Content {
  	switch block := block.AsAny().(type) {
  	case anthropic.ThinkingBlock:
  		fmt.Printf("\nThinking summary: %s", block.Thinking)
  	case anthropic.TextBlock:
  		fmt.Printf("\nResponse: %s", block.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      var client = AnthropicOkHttpClient.fromEnv();

      var params = MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_4_6)
          .maxTokens(16_000)
          .enabledThinking(10_000)
          .addUserMessage("Are there an infinite number of prime numbers such that n mod 4 == 3?")
          .build();

      var response = client.messages().create(params);

      // Respons berisi blok pemikiran yang diringkas dan blok teks
      for (var block : response.content()) {
          block.thinking().ifPresent(thinkingBlock ->
              IO.println("\nThinking summary: " + thinkingBlock.thinking())
          );
          block.text().ifPresent(textBlock ->
              IO.println("\nResponse: " + textBlock.text())
          );
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      model: 'claude-sonnet-4-6',
      maxTokens: 16000,
      thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
      messages: [
          [
              'role' => 'user',
              'content' => 'Are there an infinite number of prime numbers such that n mod 4 == 3?',
          ],
      ],
  );

  // Respons berisi blok pemikiran yang diringkas dan blok teks
  foreach ($response->content as $block) {
      echo match ($block->type) {
          'thinking' => "\nThinking summary: {$block->thinking}",
          'text' => "\nResponse: {$block->text}",
          default => '',
      };
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 16_000,
    thinking: {
      type: :enabled,
      budget_tokens: 10_000
    },
    messages: [
      {
        role: :user,
        content: "Are there an infinite number of prime numbers such that n mod 4 == 3?"
      }
    ]
  )

  # Respons berisi blok pemikiran yang diringkas dan blok teks
  response.content.each do |block|
    case block
    in {type: :thinking, thinking:}
      puts "\nThinking summary: #{thinking}"
    in {type: :text, text:}
      puts "\nResponse: #{text}"
    else
    end
  end
  ```
</CodeGroup>

Untuk mengaktifkan pemikiran diperpanjang, tambahkan objek `thinking` dengan `type` diatur ke `enabled` dan nilai `budget_tokens`. Pada model di mana pemikiran diperpanjang manual sudah usang atau tidak didukung (lihat [Model yang didukung](#supported-models)), gunakan `type: "adaptive"` sebagai gantinya seperti yang dijelaskan di [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking).

Parameter `budget_tokens` menetapkan jumlah maksimum token yang dapat digunakan Claude untuk proses penalaran internalnya. Batas ini berlaku untuk token pemikiran penuh, bukan untuk [output yang diringkas](#summarized-thinking). Anggaran yang lebih besar dapat meningkatkan kualitas respons dengan memungkinkan analisis yang lebih menyeluruh untuk masalah kompleks, meskipun Claude mungkin tidak menggunakan seluruh anggaran yang dialokasikan, terutama pada rentang di atas 32k.

<Warning>
  `budget_tokens` sudah [usang](/docs/id/build-with-claude/overview#feature-availability) pada Claude Opus 4.6 dan Claude Sonnet 4.6 dan akan dihapus pada rilis model mendatang. Gunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran sebagai gantinya.
</Warning>

<Note>
  [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5, Claude Opus 4.6, dan Claude Sonnet 4.6 mendukung hingga 128k token output. Claude Haiku 4.5 mendukung hingga 64k. Lihat [ikhtisar model](/docs/id/about-claude/models/overview) untuk batas pada model lama. Pada [Message Batches API](/docs/id/build-with-claude/batch-processing#extended-output-beta), [header beta](/docs/id/api/beta-headers) `output-300k-2026-03-24` menaikkan batas output menjadi 300k untuk Claude Opus 4.8, Opus 4.7, Sonnet 5, Opus 4.6, dan Sonnet 4.6.
</Note>

`budget_tokens` harus diatur ke nilai yang lebih kecil dari `max_tokens`. Namun, saat menggunakan [pemikiran tersisip dengan alat](#interleaved-thinking), Anda dapat melampaui batas ini karena batas token menjadi seluruh jendela konteks Anda. Karena `budget_tokens` harus lebih kecil dari `max_tokens`, pemikiran diperpanjang tidak dapat dikombinasikan dengan `max_tokens: 0` ([pra-pemanasan cache](/docs/id/build-with-claude/prompt-caching#pre-warming-the-cache)).

### Mengontrol tampilan pemikiran

Field `display` pada konfigurasi thinking mengontrol bagaimana konten thinking dikembalikan dalam respons API. Field ini menerima dua nilai:

* `"summarized"`: Blok thinking berisi teks thinking yang diringkas. Lihat [Summarized thinking](#summarized-thinking) untuk detailnya. Ini adalah default pada Claude Opus 4.6, Claude Sonnet 4.6, dan model Claude 4 sebelumnya.
* `"omitted"`: Blok thinking dikembalikan dengan field `thinking` kosong. Field `signature` tetap membawa thinking lengkap yang terenkripsi untuk kontinuitas multi-turn (lihat [Enkripsi thinking](#thinking-encryption)). Ini adalah default pada Claude Fable 5, Claude Mythos 5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, dan [Claude Mythos Preview](https://anthropic.com/glasswing).

Mengatur `display: "omitted"` berguna ketika aplikasi Anda tidak menampilkan konten thinking kepada pengguna. Manfaat utamanya adalah **time-to-first-text-token yang lebih cepat saat streaming:** Server melewati streaming token thinking sepenuhnya dan hanya mengirimkan signature, sehingga respons teks akhir mulai di-stream lebih cepat.

Berikut adalah beberapa pertimbangan penting untuk omitted thinking:

* Anda tetap dikenakan biaya untuk token thinking penuh. Menghilangkan thinking mengurangi latensi, bukan biaya.
* Jika Anda mengirimkan kembali blok thinking dalam percakapan multi-turn, kirimkan tanpa perubahan. Server mendekripsi `signature` untuk merekonstruksi thinking asli untuk konstruksi prompt (lihat [Mempertahankan blok thinking](/docs/id/build-with-claude/extended-thinking#preserving-thinking-blocks)). Teks apa pun yang Anda tempatkan di field `thinking` dari blok omitted yang dikirim bolak-balik akan diabaikan.
* `display` tidak valid dengan `thinking.type: "disabled"` (tidak ada yang perlu ditampilkan).
* Saat menggunakan `thinking.type: "adaptive"` dan model melewati thinking untuk permintaan sederhana, tidak ada blok thinking yang dihasilkan terlepas dari nilai `display`.

<Note>
  Field `signature` identik baik `display` bernilai `"summarized"` maupun `"omitted"`. Mengganti nilai `display` di antara giliran dalam sebuah percakapan didukung.
</Note>

<Note>
  Pada [Claude Mythos Preview](https://anthropic.com/glasswing), `display` secara default adalah `"omitted"`. Contoh-contoh di bagian ini meneruskan `display` secara eksplisit agar berlaku untuk semua model, tetapi pada Mythos Preview Anda dapat membiarkannya tidak diatur dan menerima perilaku yang sama. Untuk menerima pemikiran yang diringkas pada Mythos Preview, atur `display: "summarized"` secara eksplisit.
</Note>

Pipeline otomatis yang tidak pernah menampilkan konten pemikiran kepada pengguna akhir dapat melewati overhead penerimaan token pemikiran melalui jaringan. Aplikasi yang sensitif terhadap latensi mendapatkan kualitas penalaran yang sama tanpa menunggu teks pemikiran di-streaming sebelum respons akhir dimulai.

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
        "budget_tokens": 10000,
        "display": "omitted"
      },
      "messages": [
        {
          "role": "user",
          "content": "What is 27 * 453?"
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-sonnet-4-6 \
    --max-tokens 16000 \
    --transform content \
    --thinking '{type: enabled, budget_tokens: 10000, display: omitted}' \
    --message '{role: user, content: "What is 27 * 453?"}' \
    --format yaml
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=16000,
      thinking={
          "type": "enabled",
          "budget_tokens": 10000,
          "display": "omitted",
      },
      messages=[
          {"role": "user", "content": "What is 27 * 453?"},
      ],
  )

  for block in response.content:
      if block.type == "thinking":
          if block.thinking:
              print(f"Thinking: {block.thinking}")
          else:
              print("Thinking: [omitted]")
      elif block.type == "text":
          print(f"Response: {block.text}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 16000,
    thinking: {
      type: "enabled",
      budget_tokens: 10000,
      display: "omitted"
    },
    messages: [
      {
        role: "user",
        content: "What is 27 * 453?"
      }
    ]
  });

  for (const block of response.content) {
    if (block.type === "thinking") {
      if (block.thinking.length > 0) {
        console.log(`Thinking: ${block.thinking}`);
      } else {
        console.log("Thinking: [omitted]");
      }
    } else if (block.type === "text") {
      console.log(`Response: ${block.text}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var message = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeSonnet4_6,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigEnabled
      {
          BudgetTokens = 10000,
          Display = ThinkingConfigEnabledDisplay.Omitted
      },
      Messages =
      [
          new() { Role = Role.User, Content = "What is 27 * 453?" }
      ]
  });

  foreach (var block in message.Content)
  {
      if (block.TryPickThinking(out ThinkingBlock? thinking))
      {
          Console.WriteLine(string.IsNullOrEmpty(thinking.Thinking)
              ? "Thinking: [omitted]"
              : $"Thinking: {thinking.Thinking}");
      }
      else if (block.TryPickText(out TextBlock? text))
      {
          Console.WriteLine($"Response: {text.Text}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet4_6,
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfEnabled: &anthropic.ThinkingConfigEnabledParam{
  			BudgetTokens: 10000,
  			Display:      anthropic.ThinkingConfigEnabledDisplayOmitted,
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is 27 * 453?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range response.Content {
  	switch v := block.AsAny().(type) {
  	case anthropic.ThinkingBlock:
  		fmt.Println("Thinking:", cmp.Or(v.Thinking, "[omitted]"))
  	case anthropic.TextBlock:
  		fmt.Println("Response:", v.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.messages.ThinkingConfigEnabled;
  // ...
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_4_6)
          .maxTokens(16000L)
          .thinking(ThinkingConfigEnabled.builder()
              .budgetTokens(10000L)
              .display(ThinkingConfigEnabled.Display.OMITTED)
              .build())
          .addUserMessage("What is 27 * 453?")
          .build();

      Message message = client.messages().create(params);

      message.content().forEach(block -> {
          block.thinking().ifPresent(thinkingBlock -> {
              if (thinkingBlock.thinking().isEmpty()) {
                  IO.println("Thinking: [omitted]");
              } else {
                  IO.println("Thinking: " + thinkingBlock.thinking());
              }
          });
          block.text().ifPresent(textBlock ->
              IO.println("Response: " + textBlock.text())
          );
      });
  }
  ```

  ```php PHP
  use Anthropic\Messages\TextBlock;
  use Anthropic\Messages\ThinkingBlock;
  use Anthropic\Messages\ThinkingConfigEnabled;
  use Anthropic\Messages\ThinkingConfigEnabled\Display;
  // ...
  $client = new Client();

  $response = $client->messages->create(
      model: 'claude-sonnet-4-6',
      maxTokens: 16000,
      thinking: ThinkingConfigEnabled::with(
          budgetTokens: 10000,
          display: Display::OMITTED,
      ),
      messages: [
          ['role' => 'user', 'content' => 'What is 27 * 453?'],
      ],
  );

  foreach ($response->content as $block) {
      echo match (true) {
          $block instanceof ThinkingBlock && $block->thinking === '' => "Thinking: [omitted]\n",
          $block instanceof ThinkingBlock => "Thinking: {$block->thinking}\n",
          $block instanceof TextBlock => "Response: {$block->text}\n",
          default => '',
      };
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 16000,
    thinking: {
      type: :enabled,
      budget_tokens: 10000,
      # SDK Ruby menggunakan `display_` (garis bawah di akhir) untuk menghindari
      # penimpaan Kernel#display; field pada wire tetap `display`.
      display_: :omitted
    },
    messages: [{role: "user", content: "What is 27 * 453?"}]
  )

  response.content.each do |block|
    case block.type
    when :thinking
      puts block.thinking.empty? ? "Thinking: [omitted]" : "Thinking: #{block.thinking}"
    when :text
      puts "Response: #{block.text}"
    end
  end
  ```
</CodeGroup>

Ketika `display: "omitted"` diatur, respons berisi blok `thinking` dengan field `thinking` yang kosong:

```json Output
{
  "content": [
    {
      "type": "thinking",
      "thinking": "",
      "signature": "EosnCkYICxIMMb3LzNrMu..."
    },
    {
      "type": "text",
      "text": "The answer is 12,231."
    }
  ]
}
```

Saat streaming dengan `display: "omitted"`, tidak ada event `thinking_delta` yang dikeluarkan; lihat [Streaming pemikiran](#streaming-thinking) untuk urutan event.

### Pemikiran yang diringkas

Dengan "extended thinking" (pemikiran diperpanjang) diaktifkan, Messages API untuk model Claude 4 mengembalikan ringkasan dari proses pemikiran lengkap Claude. Pemikiran yang diringkas memberikan manfaat kecerdasan penuh dari pemikiran diperpanjang, sekaligus mencegah penyalahgunaan. Ini adalah perilaku default pada model Claude 4 ketika field `display` pada konfigurasi thinking tidak disetel atau disetel ke `"summarized"`. Pada Claude Fable 5, Claude Mythos 5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, dan [Claude Mythos Preview](https://anthropic.com/glasswing), `display` secara default disetel ke `"omitted"`, sehingga Anda harus menyetel `display: "summarized"` secara eksplisit untuk menerima pemikiran yang diringkas.

Berikut adalah beberapa pertimbangan penting untuk pemikiran yang diringkas:

* Anda dikenakan biaya untuk token pemikiran penuh yang dihasilkan oleh permintaan asli, bukan token ringkasan.
* Jumlah token output yang ditagih **tidak akan sama** dengan jumlah token yang Anda lihat dalam respons.
* Pada model Claude 4, beberapa baris pertama dari output pemikiran lebih verbose, memberikan penalaran terperinci yang sangat membantu untuk keperluan rekayasa prompt. [Claude Mythos Preview](https://anthropic.com/glasswing) meringkas sejak token pertama, sehingga blok pemikirannya tidak menampilkan pembukaan verbose ini.
* Karena Anthropic terus berupaya meningkatkan fitur pemikiran diperpanjang, perilaku peringkasan dapat berubah sewaktu-waktu.
* Peringkasan mempertahankan ide-ide kunci dari proses pemikiran Claude dengan latensi tambahan yang minimal, memungkinkan pengalaman pengguna yang dapat di-stream.
* Peringkasan diproses oleh model yang berbeda dari model yang Anda targetkan dalam permintaan Anda. Model pemikiran tidak melihat output yang diringkas.

<Note>
  Dalam kasus langka di mana Anda memerlukan akses ke output pemikiran penuh untuk model Claude 4, [hubungi tim penjualan Anthropic](mailto:sales@anthropic.com).
</Note>

### Streaming pemikiran

Anda dapat melakukan streaming respons pemikiran diperpanjang menggunakan [server-sent events (SSE)](https://developer.mozilla.org/en-US/Web/API/Server-sent%5Fevents/Using%5Fserver-sent%5Fevents).

Ketika streaming diaktifkan untuk pemikiran diperpanjang, Anda menerima konten pemikiran melalui event `thinking_delta`.

Ketika `display: "omitted"` diatur, tidak ada event `thinking_delta` yang dikeluarkan. Lihat [Mengontrol tampilan pemikiran](#controlling-thinking-display).

Untuk dokumentasi lebih lanjut tentang streaming melalui Messages API, lihat [Streaming Messages](/docs/id/build-with-claude/streaming).

Berikut cara menangani streaming dengan pemikiran:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-4-6",
      "max_tokens": 16000,
      "stream": true,
      "thinking": {
        "type": "enabled",
        "budget_tokens": 10000
      },
      "messages": [
        {
          "role": "user",
          "content": "What is the greatest common divisor of 1071 and 462?"
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --stream \
    --model claude-sonnet-4-6 \
    --max-tokens 16000 \
    --thinking '{type: enabled, budget_tokens: 10000}' \
    --message '{role: user, content: What is the greatest common divisor of 1071 and 462?}' \
    --format jsonl
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      model="claude-sonnet-4-6",
      max_tokens=16000,
      thinking={"type": "enabled", "budget_tokens": 10000},
      messages=[
          {
              "role": "user",
              "content": "What is the greatest common divisor of 1071 and 462?",
          }
      ],
  ) as stream:
      thinking_started = False
      response_started = False

      for event in stream:
          if event.type == "content_block_start":
              print(f"\nStarting {event.content_block.type} block...")
              # Reset flag untuk setiap blok baru
              thinking_started = False
              response_started = False
          elif event.type == "content_block_delta":
              if event.delta.type == "thinking_delta":
                  if not thinking_started:
                      print("Thinking: ", end="", flush=True)
                      thinking_started = True
                  print(event.delta.thinking, end="", flush=True)
              elif event.delta.type == "text_delta":
                  if not response_started:
                      print("Response: ", end="", flush=True)
                      response_started = True
                  print(event.delta.text, end="", flush=True)
          elif event.type == "content_block_stop":
              print("\nBlock complete.")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = await client.messages.stream({
    model: "claude-sonnet-4-6",
    max_tokens: 16000,
    thinking: {
      type: "enabled",
      budget_tokens: 10000
    },
    messages: [
      {
        role: "user",
        content: "What is the greatest common divisor of 1071 and 462?"
      }
    ]
  });

  let thinkingStarted = false;
  let responseStarted = false;

  for await (const event of stream) {
    if (event.type === "content_block_start") {
      console.log(`\nStarting ${event.content_block.type} block...`);
      // Reset flag untuk setiap blok baru
      thinkingStarted = false;
      responseStarted = false;
    } else if (event.type === "content_block_delta") {
      if (event.delta.type === "thinking_delta") {
        if (!thinkingStarted) {
          process.stdout.write("Thinking: ");
          thinkingStarted = true;
        }
        process.stdout.write(event.delta.thinking);
      } else if (event.delta.type === "text_delta") {
        if (!responseStarted) {
          process.stdout.write("Response: ");
          responseStarted = true;
        }
        process.stdout.write(event.delta.text);
      }
    } else if (event.type === "content_block_stop") {
      console.log("\nBlock complete.");
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeSonnet4_6,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
      Messages = [new() { Role = Role.User, Content = "What is the greatest common divisor of 1071 and 462?" }]
  };

  bool thinkingStarted = false;
  bool responseStarted = false;

  await foreach (var streamEvent in client.Messages.CreateStreaming(parameters))
  {
      if (streamEvent.TryPickContentBlockStart(out var blockStart))
      {
          Console.WriteLine($"\nStarting {blockStart.ContentBlock.Type} block...");
          thinkingStarted = false;
          responseStarted = false;
      }
      else if (streamEvent.TryPickContentBlockDelta(out var blockDelta))
      {
          if (blockDelta.Delta.TryPickThinking(out var thinkingDelta))
          {
              if (!thinkingStarted)
              {
                  Console.Write("Thinking: ");
                  thinkingStarted = true;
              }
              Console.Write(thinkingDelta.Thinking);
          }
          else if (blockDelta.Delta.TryPickText(out var textDelta))
          {
              if (!responseStarted)
              {
                  Console.Write("Response: ");
                  responseStarted = true;
              }
              Console.Write(textDelta.Text);
          }
      }
      else if (streamEvent.TryPickContentBlockStop(out _))
      {
          Console.WriteLine("\nBlock complete.");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet4_6,
  	MaxTokens: 16000,
  	Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the greatest common divisor of 1071 and 462?")),
  	},
  })

  thinkingStarted := false
  responseStarted := false

  for stream.Next() {
  	event := stream.Current()
  	switch eventVariant := event.AsAny().(type) {
  	case anthropic.ContentBlockStartEvent:
  		fmt.Printf("\nStarting %s block...\n", eventVariant.ContentBlock.Type)
  		thinkingStarted = false
  		responseStarted = false
  	case anthropic.ContentBlockDeltaEvent:
  		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
  		case anthropic.ThinkingDelta:
  			if !thinkingStarted {
  				fmt.Print("Thinking: ")
  				thinkingStarted = true
  			}
  			fmt.Print(deltaVariant.Thinking)
  		case anthropic.TextDelta:
  			if !responseStarted {
  				fmt.Print("Response: ")
  				responseStarted = true
  			}
  			fmt.Print(deltaVariant.Text)
  		}
  	case anthropic.ContentBlockStopEvent:
  		fmt.Println("\nBlock complete.")
  	}
  }

  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_SONNET_4_6)
      .maxTokens(16000L)
      .enabledThinking(10000L)
      .addUserMessage("What is the greatest common divisor of 1071 and 462?")
      .build();

  try (var streamResponse = client.messages().createStreaming(params)) {
      streamResponse.stream().forEach(event -> {
          event.contentBlockStart().ifPresent(startEvent ->
              IO.println("\nStarting block...")
          );
          event.contentBlockDelta().ifPresent(deltaEvent -> {
              deltaEvent.delta().thinking().ifPresent(thinkingDelta ->
                  IO.print(thinkingDelta.thinking())
              );
              deltaEvent.delta().text().ifPresent(textDelta ->
                  IO.print(textDelta.text())
              );
          });
          event.contentBlockStop().ifPresent(stopEvent ->
              IO.println("\nBlock complete.")
          );
      });
  }
  ```

  ```php PHP
  $client = new Client();

  $thinkingStarted = false;
  $responseStarted = false;

  $stream = $client->messages->createStream(
      maxTokens: 16000,
      messages: [
          ['role' => 'user', 'content' => 'What is the greatest common divisor of 1071 and 462?']
      ],
      model: 'claude-sonnet-4-6',
      thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
  );

  foreach ($stream as $event) {
      if ($event->type === 'content_block_start') {
          echo "\nStarting {$event->contentBlock->type} block...\n";
          $thinkingStarted = false;
          $responseStarted = false;
      } elseif ($event->type === 'content_block_delta') {
          if ($event->delta->type === 'thinking_delta') {
              if (!$thinkingStarted) {
                  echo "Thinking: ";
                  $thinkingStarted = true;
              }
              echo $event->delta->thinking;
          } elseif ($event->delta->type === 'text_delta') {
              if (!$responseStarted) {
                  echo "Response: ";
                  $responseStarted = true;
              }
              echo $event->delta->text;
          }
      } elseif ($event->type === 'content_block_stop') {
          echo "\nBlock complete.\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  thinking_started = false
  response_started = false

  stream = client.messages.stream(
    model: "claude-sonnet-4-6",
    max_tokens: 16000,
    thinking: {
      type: "enabled",
      budget_tokens: 10000
    },
    messages: [
      { role: "user", content: "What is the greatest common divisor of 1071 and 462?" }
    ]
  )

  stream.each do |event|
    case event.type
    when :content_block_start
      puts "\nStarting #{event.content_block.type} block..."
      thinking_started = false
      response_started = false
    when :content_block_delta
      if event.delta.type == :thinking_delta
        unless thinking_started
          print "Thinking: "
          thinking_started = true
        end
        print event.delta.thinking
      elsif event.delta.type == :text_delta
        unless response_started
          print "Response: "
          response_started = true
        end
        print event.delta.text
      end
    when :content_block_stop
      puts "\nBlock complete."
    end
  end
  ```
</CodeGroup>

Contoh output streaming:

```sse Output
event: message_start
data: {"type": "message_start", "message": {"id": "msg_01...", "type": "message", "role": "assistant", "content": [], "model": "claude-sonnet-4-6", "stop_reason": null, "stop_sequence": null}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": "", "signature": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "I need to find the GCD of 1071 and 462 using the Euclidean algorithm.\n\n1071 = 2 × 462 + 147"}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\n462 = 3 × 147 + 21\n147 = 7 × 21 + 0\n\nSo GCD(1071, 462) = 21"}}

// Additional thinking deltas...

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b3hGgxBdjrkzLoky3dl1pkiMOYds..."}}

event: content_block_stop
data: {"type": "content_block_stop", "index": 0}

event: content_block_start
data: {"type": "content_block_start", "index": 1, "content_block": {"type": "text", "text": ""}}

event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "text_delta", "text": "The greatest common divisor of 1071 and 462 is **21**."}}

// Additional text deltas...

event: content_block_stop
data: {"type": "content_block_stop", "index": 1}

event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", "stop_sequence": null}}

event: message_stop
data: {"type": "message_stop"}
```

Ketika `display: "omitted"` diatur, blok pemikiran terbuka, satu `signature_delta` tiba, dan blok ditutup tanpa event `thinking_delta` apa pun. Streaming teks dimulai segera setelahnya:

```sse Output
event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"thinking","thinking":"","signature":""}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"signature_delta","signature":"EosnCkYICxIMMb3LzNrMu..."}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: content_block_start
data: {"type":"content_block_start","index":1,"content_block":{"type":"text","text":""}}
```

<Note>
  Saat menggunakan streaming dengan pemikiran diaktifkan, Anda mungkin memperhatikan bahwa teks terkadang tiba dalam potongan yang lebih besar bergantian dengan pengiriman token demi token yang lebih kecil. Ini adalah perilaku yang diharapkan, terutama untuk konten pemikiran.

  Sistem streaming perlu memproses konten dalam batch untuk kinerja optimal, yang dapat menghasilkan pola pengiriman "berpotongan" ini, dengan kemungkinan penundaan antara event streaming.
</Note>

## Pemikiran diperpanjang dengan penggunaan alat

Pemikiran diperpanjang dapat digunakan bersama dengan [penggunaan alat](/docs/id/agents-and-tools/tool-use/overview), memungkinkan Claude untuk bernalar melalui pemilihan alat dan pemrosesan hasil.

Saat menggunakan pemikiran diperpanjang dengan penggunaan alat, perhatikan batasan berikut:

1. **Batasan pilihan alat:** Penggunaan alat dengan pemikiran hanya mendukung `tool_choice: {"type": "auto"}` (default) atau `tool_choice: {"type": "none"}`. Menggunakan `tool_choice: {"type": "any"}` atau `tool_choice: {"type": "tool", "name": "..."}` akan menghasilkan error karena opsi-opsi ini memaksa penggunaan alat, yang tidak kompatibel dengan pemikiran diperpanjang.

2. **Melestarikan blok pemikiran:** Selama penggunaan alat, Anda harus meneruskan blok `thinking` kembali ke API untuk pesan asisten terakhir. Sertakan blok lengkap yang tidak dimodifikasi kembali ke API untuk mempertahankan kontinuitas penalaran.

### Mengalihkan mode pemikiran dalam percakapan

Anda tidak dapat mengalihkan pemikiran di tengah giliran asisten, termasuk selama loop penggunaan alat. Seluruh giliran asisten harus beroperasi dalam satu mode pemikiran:

* **Jika pemikiran diaktifkan**, giliran asisten terakhir harus dimulai dengan blok pemikiran.
* **Jika pemikiran dinonaktifkan**, giliran asisten terakhir tidak boleh berisi blok pemikiran apa pun.

Dari perspektif model, **loop penggunaan alat adalah bagian dari giliran asisten**. Giliran asisten tidak selesai sampai Claude menyelesaikan respons penuhnya, yang mungkin mencakup beberapa panggilan alat dan hasil.

Misalnya, urutan ini semuanya merupakan bagian dari **satu giliran asisten**:

```text wrap
User: "What's the weather in Paris?"
Assistant: [thinking] + [tool_use: get_weather]
User: [tool_result: "20°C, sunny"]
Assistant: [text: "The weather in Paris is 20°C and sunny"]
```

Meskipun ada beberapa pesan API, loop penggunaan alat secara konseptual merupakan bagian dari satu respons asisten yang berkelanjutan.

#### Degradasi pemikiran yang anggun

Ketika konflik pemikiran di tengah giliran terjadi (seperti mengaktifkan atau menonaktifkan pemikiran selama loop penggunaan alat), API secara otomatis menonaktifkan pemikiran untuk permintaan tersebut. Untuk menjaga kualitas model dan tetap sesuai distribusi, API dapat:

* Menghapus blok pemikiran dari percakapan ketika blok tersebut akan membuat struktur giliran yang tidak valid
* Menonaktifkan pemikiran untuk permintaan saat ini ketika riwayat percakapan tidak kompatibel dengan pemikiran yang diaktifkan

Ini berarti bahwa mencoba mengalihkan pemikiran di tengah giliran tidak akan menyebabkan error, tetapi pemikiran akan dinonaktifkan secara diam-diam untuk permintaan tersebut. Untuk mengonfirmasi apakah pemikiran aktif, periksa keberadaan blok `thinking` dalam respons.

#### Panduan praktis

**Praktik terbaik:** Rencanakan strategi pemikiran Anda di awal setiap giliran daripada mencoba mengalihkan di tengah giliran.

**Contoh: Mengalihkan pemikiran setelah menyelesaikan giliran**

```text wrap
User: "What's the weather?"
Assistant: [tool_use] (thinking disabled)
User: [tool_result]
Assistant: [text: "It's sunny"]
User: "What about tomorrow?"
Assistant: [thinking] + [text: "..."] (thinking enabled - new turn)
```

Dengan menyelesaikan giliran asisten sebelum mengalihkan pemikiran, Anda memastikan bahwa pemikiran benar-benar diaktifkan untuk permintaan baru.

<Note>
  Mengalihkan mode pemikiran juga membatalkan caching prompt untuk riwayat pesan. Untuk detail lebih lanjut, lihat bagian [Pemikiran diperpanjang dengan caching prompt](#extended-thinking-with-prompt-caching).
</Note>

<AccordionGroup>
  <Accordion title="Contoh: Meneruskan blok pemikiran dengan hasil alat">
    Berikut adalah contoh praktis yang menunjukkan cara melestarikan blok pemikiran saat memberikan hasil alat:

    <CodeGroup>
      ```bash CLI
      ant messages create --transform content <<'YAML'
      model: claude-sonnet-4-6
      max_tokens: 16000
      thinking:
        type: enabled
        budget_tokens: 10000
      tools:
        - name: get_weather
          description: Get current weather for a location
          input_schema:
            type: object
            properties:
              location:
                type: string
                description: City name
            required:
              - location
      messages:
        - role: user
          content: "What's the weather in Paris?"
      YAML
      ```

      ```python Python

      client = anthropic.Anthropic()

      weather_tool = {
          "name": "get_weather",
          "description": "Get current weather for a location",
          "input_schema": {
              "type": "object",
              "properties": {"location": {"type": "string", "description": "City name"}},
              "required": ["location"],
          },
      }

      # Permintaan pertama - Claude merespons dengan pemikiran dan permintaan alat
      response = client.messages.create(
          model="claude-sonnet-4-6",
          max_tokens=16000,
          thinking={"type": "enabled", "budget_tokens": 10000},
          tools=[weather_tool],
          messages=[{"role": "user", "content": "What's the weather in Paris?"}],
      )
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const weatherTool: Anthropic.Tool = {
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      };

      // Permintaan pertama - Claude merespons dengan pemikiran dan permintaan alat
      const response = await client.messages.create({
        model: "claude-sonnet-4-6",
        max_tokens: 16000,
        thinking: {
          type: "enabled",
          budget_tokens: 10000
        },
        tools: [weatherTool],
        messages: [{ role: "user", content: "What's the weather in Paris?" }]
      });
      ```

      ```csharp C#
      AnthropicClient client = new();

      var weatherTool = new ToolUnion(new Tool()
      {
          Name = "get_weather",
          Description = "Get current weather for a location",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "City name" }),
              },
              Required = ["location"],
          },
      });

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeSonnet4_6,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
          Tools = [weatherTool],
          Messages = [new() { Role = Role.User, Content = "What's the weather in Paris?" }]
      };

      var message = await client.Messages.Create(parameters);
      Console.WriteLine(message);
      ```

      ```go Go
      client := anthropic.NewClient()

      weatherTool := anthropic.ToolUnionParam{
      	OfTool: &anthropic.ToolParam{
      		Name:        "get_weather",
      		Description: anthropic.String("Get current weather for a location"),
      		InputSchema: anthropic.ToolInputSchemaParam{
      			Properties: map[string]any{
      				"location": map[string]any{
      					"type":        "string",
      					"description": "City name",
      				},
      			},
      			Required: []string{"location"},
      		},
      	},
      }

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeSonnet4_6,
      	MaxTokens: 16000,
      	Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
      	Tools:     []anthropic.ToolUnionParam{weatherTool},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in Paris?")),
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
          .model(Model.CLAUDE_SONNET_4_6)
          .maxTokens(16000L)
          .enabledThinking(10000L)
          .addTool(Tool.builder()
              .name("get_weather")
              .description("Get current weather for a location")
              .inputSchema(Tool.InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                      "location", Map.of("type", "string", "description", "City name")
                  )))
                  .required(List.of("location"))
                  .build())
              .build())
          .addUserMessage("What's the weather in Paris?")
          .build();

      Message response = client.messages().create(params);
      IO.println(response);
      ```

      ```php PHP
      $client = new Client();

      $weatherTool = [
          'name' => 'get_weather',
          'description' => 'Get current weather for a location',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'location' => ['type' => 'string', 'description' => 'City name']
              ],
              'required' => ['location']
          ]
      ];

      $message = $client->messages->create(
          maxTokens: 16000,
          messages: [
              ['role' => 'user', 'content' => "What's the weather in Paris?"]
          ],
          model: 'claude-sonnet-4-6',
          thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
          tools: [$weatherTool],
      );
      echo $message;
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      weather_tool = {
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      }

      message = client.messages.create(
        model: "claude-sonnet-4-6",
        max_tokens: 16000,
        thinking: {
          type: "enabled",
          budget_tokens: 10000
        },
        tools: [weather_tool],
        messages: [
          { role: "user", content: "What's the weather in Paris?" }
        ]
      )
      puts message
      ```
    </CodeGroup>

    Respons API menyertakan blok thinking, text, dan tool\_use:

    ```json Output
    {
      "content": [
        {
          "type": "thinking",
          "thinking": "The user wants to know the current weather in Paris. I have access to a function `get_weather`...",
          "signature": "BDaL4VrbR2Oj0hO4XpJxT28J5TILnCrrUXoKiiNBZW9P+nr8XSj1zuZzAl4egiCCpQNvfyUuFFJP5CncdYZEQPPmLxYsNrcs...."
        },
        {
          "type": "text",
          "text": "I can help you get the current weather information for Paris. Let me check that for you"
        },
        {
          "type": "tool_use",
          "id": "toolu_01CswdEQBMshySk6Y9DFKrfq",
          "name": "get_weather",
          "input": {
            "location": "Paris"
          }
        }
      ]
    }
    ```

    Sekarang mari kita lanjutkan percakapan dan gunakan alatnya

    <CodeGroup>
      ```bash CLI
      # Giliran pertama: tangkap array konten asisten (thinking + tool_use,
      # dengan signature tetap utuh) sebagai JSON ringkas.
      ASSISTANT_CONTENT=$(ant messages create \
        --transform content <<'YAML'
      model: claude-sonnet-4-6
      max_tokens: 16000
      thinking:
        type: enabled
        budget_tokens: 10000
      tools:
        - name: get_weather
          description: Get current weather for a location
          input_schema:
            type: object
            properties:
              location:
                type: string
                description: City name
            required: [location]
      messages:
        - role: user
          content: What's the weather in Paris?
      YAML
      )

      TOOL_USE_ID=$(printf '%s' "$ASSISTANT_CONTENT" \
        | jq -r '.[] | select(.type == "tool_use") | .id')

      # Giliran kedua: kirimkan kembali blok yang ditangkap sebagai pesan asisten.
      # Blok thinking HARUS menyertai blok tool_use.
      ant messages create <<YAML
      model: claude-sonnet-4-6
      max_tokens: 16000
      thinking:
        type: enabled
        budget_tokens: 10000
      tools:
        - name: get_weather
          description: Get current weather for a location
          input_schema:
            type: object
            properties:
              location:
                type: string
                description: City name
            required: [location]
      messages:
        - role: user
          content: What's the weather in Paris?
        - role: assistant
          content: $ASSISTANT_CONTENT
        - role: user
          content:
            - type: tool_result
              tool_use_id: $TOOL_USE_ID
              content: "Current temperature: 88°F"
      YAML
      ```

      ```python Python

      client = anthropic.Anthropic()
      weather_tool = {
          "name": "get_weather",
          "description": "Get current weather for a location",
          "input_schema": {
              "type": "object",
              "properties": {"location": {"type": "string", "description": "City name"}},
              "required": ["location"],
          },
      }
      response = client.messages.create(
          model="claude-sonnet-4-6",
          max_tokens=16000,
          thinking={"type": "enabled", "budget_tokens": 10000},
          tools=[weather_tool],
          messages=[{"role": "user", "content": "What's the weather in Paris?"}],
      )
      # Ekstrak blok pemikiran dan blok penggunaan alat
      thinking_block = next(
          (block for block in response.content if block.type == "thinking"), None
      )
      tool_use_block = next(
          (block for block in response.content if block.type == "tool_use"), None
      )

      # Panggil API cuaca Anda yang sebenarnya, di sinilah panggilan API Anda yang sebenarnya akan ditempatkan
      # Anggap saja ini yang kita dapatkan kembali
      weather_data = {"temperature": 88}

      # Permintaan kedua - Sertakan blok pemikiran dan hasil alat
      # Tidak ada blok pemikiran baru yang dihasilkan dalam respons
      continuation = client.messages.create(
          model="claude-sonnet-4-6",
          max_tokens=16000,
          thinking={"type": "enabled", "budget_tokens": 10000},
          tools=[weather_tool],
          messages=[
              {"role": "user", "content": "What's the weather in Paris?"},
              # perhatikan bahwa thinking_block diteruskan bersama dengan tool_use_block
              # jika ini tidak diteruskan, error akan muncul
              {"role": "assistant", "content": [thinking_block, tool_use_block]},
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "tool_result",
                          "tool_use_id": tool_use_block.id,
                          "content": f"Current temperature: {weather_data['temperature']}°F",
                      }
                  ],
              },
          ],
      )
      print(continuation)
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const weatherTool: Anthropic.Tool = {
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      };

      const response = await client.messages.create({
        model: "claude-sonnet-4-6",
        max_tokens: 16000,
        thinking: {
          type: "enabled",
          budget_tokens: 10000
        },
        tools: [weatherTool],
        messages: [{ role: "user", content: "What's the weather in Paris?" }]
      });

      // Ekstrak blok pemikiran dan blok penggunaan alat
      const thinkingBlock = response.content.find(
        (block): block is Anthropic.ThinkingBlock => block.type === "thinking"
      );
      const toolUseBlock = response.content.find(
        (block): block is Anthropic.ToolUseBlock => block.type === "tool_use"
      );

      // Panggil API cuaca Anda yang sebenarnya, di sinilah panggilan API Anda yang sebenarnya akan ditempatkan
      // Anggap saja ini yang kita dapatkan kembali
      const weatherData = { temperature: 88 };

      if (thinkingBlock && toolUseBlock) {
        // Permintaan kedua - Sertakan blok pemikiran dan hasil alat
        // Tidak ada blok pemikiran baru yang dihasilkan dalam respons
        const continuation = await client.messages.create({
          model: "claude-sonnet-4-6",
          max_tokens: 16000,
          thinking: {
            type: "enabled",
            budget_tokens: 10000
          },
          tools: [weatherTool],
          messages: [
            { role: "user", content: "What's the weather in Paris?" },
            // perhatikan bahwa thinkingBlock diteruskan bersama dengan toolUseBlock
            // jika ini tidak diteruskan, error akan muncul
            { role: "assistant", content: [thinkingBlock, toolUseBlock] },
            {
              role: "user",
              content: [
                {
                  type: "tool_result" as const,
                  tool_use_id: toolUseBlock.id,
                  content: `Current temperature: ${weatherData.temperature}°F`
                }
              ]
            }
          ]
        });
        console.log(continuation);
      }
      ```

      ```csharp C#
      AnthropicClient client = new();

      var weatherTool = new ToolUnion(new Tool()
      {
          Name = "get_weather",
          Description = "Get current weather for a location",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "City name" }),
              },
              Required = ["location"],
          },
      });

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeSonnet4_6,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
          Tools = [weatherTool],
          Messages = [
              new() { Role = Role.User, Content = "What's the weather in Paris?" }
          ]
      };

      var response = await client.Messages.Create(parameters);

      // Ekstrak blok tool_use untuk mendapatkan ID-nya bagi hasil alat
      ToolUseBlock? toolUseBlock = null;
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var toolUse))
          {
              toolUseBlock = toolUse;
          }
      }

      var weatherData = new { temperature = 88 };

      // Bangun kelanjutan dengan hasil alat
      var continuationParams = new MessageCreateParams
      {
          Model = Model.ClaudeSonnet4_6,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
          Tools = [weatherTool],
          Messages = [
              new() { Role = Role.User, Content = "What's the weather in Paris?" },
              // response.Content menyertakan blok pemikiran; mengirimkannya kembali adalah wajib
              new() { Role = Role.Assistant, Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList() },
              new() { Role = Role.User, Content = new MessageParamContent(new List<ContentBlockParam>
              {
                  new ContentBlockParam(new ToolResultBlockParam()
                  {
                      ToolUseID = toolUseBlock?.ID ?? "",
                      Content = $"Current temperature: {weatherData.temperature}°F"
                  })
              })}
          ]
      };

      var continuation = await client.Messages.Create(continuationParams);
      Console.WriteLine(continuation);
      ```

      ```go Go
      client := anthropic.NewClient()

      weatherTool := anthropic.ToolUnionParam{
      	OfTool: &anthropic.ToolParam{
      		Name:        "get_weather",
      		Description: anthropic.String("Get current weather for a location"),
      		InputSchema: anthropic.ToolInputSchemaParam{
      			Properties: map[string]any{
      				"location": map[string]any{
      					"type":        "string",
      					"description": "City name",
      				},
      			},
      			Required: []string{"location"},
      		},
      	},
      }

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeSonnet4_6,
      	MaxTokens: 16000,
      	Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
      	Tools:     []anthropic.ToolUnionParam{weatherTool},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in Paris?")),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }

      var toolUseBlock anthropic.ToolUseBlock
      for _, block := range response.Content {
      	switch v := block.AsAny().(type) {
      	case anthropic.ToolUseBlock:
      		toolUseBlock = v
      	}
      }

      weatherData := map[string]int{"temperature": 88}

      continuation, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeSonnet4_6,
      	MaxTokens: 16000,
      	Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
      	Tools:     []anthropic.ToolUnionParam{weatherTool},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in Paris?")),
      		response.ToParam(),
      		anthropic.NewUserMessage(
      			anthropic.NewToolResultBlock(toolUseBlock.ID, fmt.Sprintf("Current temperature: %d°F", weatherData["temperature"]), false),
      		),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }

      fmt.Println(continuation)
      ```

      ```java Java
      import com.anthropic.models.messages.ThinkingBlock;
      import com.anthropic.models.messages.ThinkingBlockParam;
      // ...
      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          Tool weatherTool = Tool.builder()
              .name("get_weather")
              .description("Get current weather for a location")
              .inputSchema(Tool.InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                      "location", Map.of("type", "string", "description", "City name")
                  )))
                  .required(List.of("location"))
                  .build())
              .build();

          MessageCreateParams initialParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_4_6)
              .maxTokens(16000L)
              .enabledThinking(10000L)
              .addTool(weatherTool)
              .addUserMessage("What's the weather in Paris?")
              .build();

          Message response = client.messages().create(initialParams);

          ThinkingBlock thinkingBlock = null;
          ToolUseBlock toolUseBlock = null;
          for (var block : response.content()) {
              if (block.thinking().isPresent()) {
                  thinkingBlock = block.thinking().get();
              }
              if (block.toolUse().isPresent()) {
                  toolUseBlock = block.toolUse().get();
              }
          }

          int temperature = 88;

          // Permintaan kedua: kirim kembali blok pemikiran dan hasil alat
          MessageCreateParams continuationParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_4_6)
              .maxTokens(16000L)
              .enabledThinking(10000L)
              .addTool(weatherTool)
              .addUserMessage("What's the weather in Paris?")
              .addAssistantMessageOfBlockParams(List.of(
                  ContentBlockParam.ofThinking(ThinkingBlockParam.builder()
                      .thinking(thinkingBlock.thinking())
                      .signature(thinkingBlock.signature())
                      .build()),
                  ContentBlockParam.ofToolUse(ToolUseBlockParam.builder()
                      .id(toolUseBlock.id())
                      .name(toolUseBlock.name())
                      .input(toolUseBlock._input())
                      .build())
              ))
              .addUserMessageOfBlockParams(List.of(
                  ContentBlockParam.ofToolResult(
                      ToolResultBlockParam.builder()
                          .toolUseId(toolUseBlock.id())
                          .content("Current temperature: " + temperature + "°F")
                          .build()
                  )
              ))
              .build();

          Message continuation = client.messages().create(continuationParams);
          IO.println(continuation);
      }
      ```

      ```php PHP
      $client = new Client();

      $weatherTool = [
          'name' => 'get_weather',
          'description' => 'Get current weather for a location',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'location' => [
                      'type' => 'string',
                      'description' => 'City name'
                  ]
              ],
              'required' => ['location']
          ]
      ];

      $response = $client->messages->create(
          maxTokens: 16000,
          messages: [
              ['role' => 'user', 'content' => "What's the weather in Paris?"]
          ],
          model: 'claude-sonnet-4-6',
          thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
          tools: [$weatherTool],
      );

      $thinkingBlock = null;
      $toolUseBlock = null;
      foreach ($response->content as $block) {
          if ($block->type === 'thinking') {
              $thinkingBlock = $block;
          }
          if ($block->type === 'tool_use') {
              $toolUseBlock = $block;
          }
      }

      $weatherData = ['temperature' => 88];

      $continuation = $client->messages->create(
          maxTokens: 16000,
          messages: [
              ['role' => 'user', 'content' => "What's the weather in Paris?"],
              ['role' => 'assistant', 'content' => [$thinkingBlock, $toolUseBlock]],
              ['role' => 'user', 'content' => [
                  [
                      'type' => 'tool_result',
                      'tool_use_id' => $toolUseBlock->id,
                      'content' => "Current temperature: {$weatherData['temperature']}°F"
                  ]
              ]]
          ],
          model: 'claude-sonnet-4-6',
          thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
          tools: [$weatherTool],
      );

      echo $continuation;
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      weather_tool = {
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      }

      response = client.messages.create(
        model: "claude-sonnet-4-6",
        max_tokens: 16000,
        thinking: {
          type: "enabled",
          budget_tokens: 10000
        },
        tools: [weather_tool],
        messages: [
          { role: "user", content: "What's the weather in Paris?" }
        ]
      )

      thinking_block = response.content.find { |block| block.type == :thinking }
      tool_use_block = response.content.find { |block| block.type == :tool_use }

      raise "No tool_use block found" unless tool_use_block

      weather_data = { temperature: 88 }

      continuation = client.messages.create(
        model: "claude-sonnet-4-6",
        max_tokens: 16000,
        thinking: {
          type: "enabled",
          budget_tokens: 10000
        },
        tools: [weather_tool],
        messages: [
          { role: "user", content: "What's the weather in Paris?" },
          { role: "assistant", content: [thinking_block, tool_use_block] },
          { role: "user", content: [
            {
              type: "tool_result",
              tool_use_id: tool_use_block.id,
              content: "Current temperature: #{weather_data[:temperature]}°F"
            }
          ] }
        ]
      )

      puts continuation
      ```
    </CodeGroup>

    Respons API sekarang **hanya** menyertakan text

    ```json Output
    {
      "content": [
        {
          "type": "text",
          "text": "Currently in Paris, the temperature is 88°F (31°C)"
        }
      ]
    }
    ```
  </Accordion>
</AccordionGroup>

### Melestarikan blok pemikiran

Selama penggunaan alat, Anda harus meneruskan blok `thinking` kembali ke API, dan Anda harus menyertakan blok lengkap yang tidak dimodifikasi kembali ke API. Ini sangat penting untuk mempertahankan alur penalaran model dan integritas percakapan.

<Tip>
  Meskipun Anda dapat menghilangkan blok `thinking` dari giliran peran `assistant` sebelumnya, selalu teruskan kembali semua blok pemikiran ke API untuk percakapan multi-giliran apa pun. API:

  * Secara otomatis memfilter blok pemikiran yang diberikan
  * Menggunakan blok pemikiran relevan yang diperlukan untuk melestarikan penalaran model
  * Hanya menagih token input untuk blok yang ditampilkan kepada Claude

  Blok mana yang disimpan bergantung pada modelnya. Lihat [Pelestarian blok pemikiran berdasarkan model](#thinking-block-preservation-in-claude-opus-45-and-later) untuk default per kelas. Untuk mengganti default, gunakan [strategi context-editing `clear_thinking_20251015`](/docs/id/build-with-claude/context-editing#thinking-block-clearing).
</Tip>

<Note>
  Saat mengalihkan mode pemikiran selama percakapan, ingatlah bahwa seluruh giliran asisten (termasuk loop penggunaan alat) harus beroperasi dalam satu mode pemikiran. Untuk detail lebih lanjut, lihat [Mengalihkan mode pemikiran dalam percakapan](#toggling-thinking-modes-in-conversations).
</Note>

Ketika Claude memanggil alat, ia menjeda konstruksi responsnya untuk menunggu informasi eksternal. Ketika hasil alat dikembalikan, Claude melanjutkan membangun respons yang sudah ada tersebut. Ini mengharuskan pelestarian blok pemikiran selama penggunaan alat, karena beberapa alasan:

1. **Kontinuitas penalaran:** Blok pemikiran menangkap penalaran langkah demi langkah Claude yang mengarah pada permintaan alat. Ketika Anda mengirim hasil alat, menyertakan pemikiran asli memastikan Claude dapat melanjutkan penalarannya dari tempat ia berhenti.

2. **Pemeliharaan konteks:** Meskipun hasil alat muncul sebagai pesan pengguna dalam struktur API, mereka adalah bagian dari alur penalaran yang berkelanjutan. Melestarikan blok pemikiran mempertahankan alur konseptual ini di beberapa panggilan API. Untuk informasi lebih lanjut tentang manajemen konteks, lihat [panduan tentang jendela konteks](/docs/id/build-with-claude/context-windows).

**Penting:** Saat memberikan blok `thinking`, seluruh urutan blok `thinking` yang berurutan harus cocok dengan output yang dihasilkan oleh model selama permintaan asli; Anda tidak dapat mengatur ulang atau memodifikasi urutan blok-blok ini.

<Note>
  Jika blok pemikiran dimodifikasi, API mengembalikan 400 `invalid_request_error` yang pesannya berisi `` `thinking` or `redacted_thinking` blocks in the latest assistant message cannot be modified ``. Penyebab paling umum adalah kode aplikasi yang memfilter blok konten berdasarkan tipe dan membuang blok `redacted_thinking`, atau yang membangun ulang pesan asisten alih-alih menggemakannya. Lihat [Blok pemikiran tidak dapat dimodifikasi](/docs/id/api/errors#thinking-blocks-cannot-be-modified) untuk error lengkap dan langkah perbaikan.
</Note>

### Pemikiran tersisip

Pemikiran diperpanjang dengan penggunaan alat pada model Claude 4 mendukung "interleaved thinking" (pemikiran tersisip), yang memungkinkan Claude berpikir di antara panggilan alat dan membuat penalaran yang lebih canggih setelah menerima hasil alat.

Dengan pemikiran tersisip, Claude dapat:

* Bernalar tentang hasil panggilan alat sebelum memutuskan apa yang harus dilakukan selanjutnya
* Merangkai beberapa panggilan alat dengan langkah-langkah penalaran di antaranya
* Membuat keputusan yang lebih bernuansa berdasarkan hasil antara

Cara Anda mengaktifkan pemikiran tersisip bergantung pada modelnya:

| Model                                                    | Pemikiran tersisip                                                                                                                                                                      |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Fable 5 Claude Mythos 5                           | Otomatis dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking). Penalaran antar-alat berpindah ke blok pemikiran. Tidak perlu header beta.                           |
| [Claude Mythos Preview](https://anthropic.com/glasswing) | Otomatis. Setiap langkah penalaran antar-alat berpindah ke blok pemikiran alih-alih teks biasa. Tidak perlu atau tidak didukung header beta.                                            |
| Claude Opus 4.8                                          | Otomatis dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (satu-satunya mode pemikiran yang didukung). Tidak perlu header beta.                                 |
| Claude Opus 4.7                                          | Otomatis dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (satu-satunya mode pemikiran yang didukung). Tidak perlu header beta.                                 |
| Claude Opus 4.6                                          | Otomatis dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking). Header beta `interleaved-thinking-2025-05-14` sudah usang dan diabaikan dengan aman jika disertakan. |
| Claude Sonnet 5                                          | Otomatis dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking). Header beta `interleaved-thinking-2025-05-14` sudah usang dan diabaikan dengan aman jika disertakan. |
| Claude Sonnet 4.6                                        | Otomatis dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (direkomendasikan). Header beta dengan `type: "enabled"` manual masih berfungsi tetapi sudah usang.   |
| Claude Opus 4.5                                          | Tambahkan [header beta](/docs/id/api/beta-headers) `interleaved-thinking-2025-05-14` ke permintaan API Anda.                                                                            |
| Claude Haiku 4.5                                         | Tidak didukung. Header beta diterima di Claude API tetapi diabaikan.                                                                                                                    |
| Model Claude 4 sebelumnya                                | Tambahkan [header beta](/docs/id/api/beta-headers) `interleaved-thinking-2025-05-14` ke permintaan API Anda.                                                                            |

Model Claude 4 sebelumnya di sini berarti Claude Sonnet 4.5, Claude Opus 4.1 (usang), Claude Opus 4 ([dipensiunkan, kecuali di Google Cloud](/docs/id/about-claude/model-deprecations)), dan Claude Sonnet 4 ([dipensiunkan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations)).

Berikut adalah beberapa pertimbangan penting untuk pemikiran tersisip:

* Dengan pemikiran tersisip, `budget_tokens` dapat melebihi parameter `max_tokens`, karena ini mewakili total anggaran di semua blok pemikiran dalam satu giliran asisten.
* Pemikiran tersisip hanya didukung untuk [alat yang digunakan melalui Messages API](/docs/id/agents-and-tools/tool-use/overview).
* Claude API dan [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws) menerima `interleaved-thinking-2025-05-14` dalam permintaan ke model apa pun tanpa mengembalikan error. Pada model yang tidak mendukung pemikiran tersisip, header diabaikan. Pada Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 5, header ini sudah usang dan diabaikan dengan aman. Pada Claude Mythos Preview, header ini tidak diperlukan dan diabaikan dengan aman.
* Pada platform yang dioperasikan mitra (misalnya, [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock) dan [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai)), jika Anda meneruskan `interleaved-thinking-2025-05-14` ke model apa pun selain Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5, Claude Opus 4.6, Claude Sonnet 4.6, Claude Opus 4.5, Claude Opus 4.1 (usang), Opus 4 ([dipensiunkan, kecuali di Google Cloud](/docs/id/about-claude/model-deprecations)), Sonnet 4.5, atau Sonnet 4 ([dipensiunkan, kecuali di Bedrock dan Google Cloud](/docs/id/about-claude/model-deprecations)), permintaan Anda akan gagal.

<AccordionGroup>
  <Accordion title="Penggunaan alat tanpa pemikiran tersisip">
    Tanpa pemikiran tersisip, Claude berpikir sekali di awal giliran asisten. Respons berikutnya setelah hasil alat berlanjut tanpa blok pemikiran baru.

    ```text
    User: "What's the total revenue if we sold 150 units at $50 each,
           and how does this compare to our average monthly revenue?"

    Turn 1: [thinking] "I need to calculate 150 * $50, then check the database..."
            [tool_use: calculator] { "expression": "150 * 50" }
      ↓ tool result: "7500"

    Turn 2: [tool_use: database_query] { "query": "SELECT AVG(revenue)..." }
            ↑ no thinking block
      ↓ tool result: "5200"

    Turn 3: [text] "The total revenue is $7,500, which is 44% above your
            average monthly revenue of $5,200."
            ↑ no thinking block
    ```
  </Accordion>

  <Accordion title="Penggunaan alat dengan pemikiran tersisip">
    Dengan pemikiran tersisip diaktifkan, Claude dapat berpikir setelah menerima setiap hasil alat, memungkinkannya bernalar tentang hasil antara sebelum melanjutkan.

    ```text
    User: "What's the total revenue if we sold 150 units at $50 each,
           and how does this compare to our average monthly revenue?"

    Turn 1: [thinking] "I need to calculate 150 * $50 first..."
            [tool_use: calculator] { "expression": "150 * 50" }
      ↓ tool result: "7500"

    Turn 2: [thinking] "Got $7,500. Now I should query the database to compare..."
            [tool_use: database_query] { "query": "SELECT AVG(revenue)..." }
            ↑ thinking after receiving calculator result
      ↓ tool result: "5200"

    Turn 3: [thinking] "$7,500 vs $5,200 average - that's a 44% increase..."
            [text] "The total revenue is $7,500, which is 44% above your
            average monthly revenue of $5,200."
            ↑ thinking before final answer
    ```
  </Accordion>
</AccordionGroup>

## Pemikiran diperpanjang dengan caching prompt

[Prompt caching](/docs/id/build-with-claude/prompt-caching) (caching prompt) dengan pemikiran memiliki beberapa pertimbangan penting:

<Tip>
  Tugas pemikiran diperpanjang sering kali membutuhkan waktu lebih dari 5 menit untuk diselesaikan. Pertimbangkan untuk menggunakan [durasi cache 1 jam](/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration) untuk mempertahankan cache hit di sesi pemikiran yang lebih lama dan alur kerja multi-langkah.
</Tip>

**Penghapusan konteks blok pemikiran**

* Pada model Opus/Sonnet sebelumnya dan semua model Haiku, blok pemikiran dari giliran sebelumnya dihapus dari konteks, yang dapat memengaruhi breakpoint cache. Pada Opus 4.5+ dan Sonnet 4.6+, blok tersebut disimpan secara default.
* Saat melanjutkan percakapan dengan penggunaan alat, blok pemikiran di-cache dan dihitung sebagai token input saat dibaca dari cache.
* Ini menciptakan trade-off: meskipun blok pemikiran tidak mengonsumsi ruang jendela konteks secara visual, blok tersebut tetap dihitung dalam penggunaan token input Anda saat di-cache.
* Jika pemikiran dinonaktifkan dan Anda meneruskan konten pemikiran dalam giliran penggunaan alat saat ini, konten pemikiran akan dihapus dan pemikiran akan tetap dinonaktifkan untuk permintaan tersebut.

**Pola pembatalan cache**

* Perubahan pada parameter pemikiran (diaktifkan/dinonaktifkan atau alokasi anggaran) membatalkan breakpoint cache pesan
* [Pemikiran tersisip](#interleaved-thinking) memperbesar pembatalan cache, karena blok pemikiran dapat terjadi di antara beberapa [panggilan alat](#extended-thinking-with-tool-use)
* Prompt sistem dan alat tetap di-cache meskipun ada perubahan parameter pemikiran atau penghapusan blok

<Note>
  Pada model Opus/Sonnet sebelumnya dan semua model Haiku, blok pemikiran dihapus untuk perhitungan caching dan konteks; pada Opus 4.5+ dan Sonnet 4.6+, blok tersebut disimpan secara default. Dalam kedua kasus, blok tersebut harus dilestarikan saat melanjutkan percakapan dengan [penggunaan alat](#extended-thinking-with-tool-use), terutama dengan [pemikiran tersisip](#interleaved-thinking).
</Note>

### Memahami perilaku caching blok pemikiran

Saat menggunakan pemikiran diperpanjang dengan penggunaan alat, blok pemikiran menunjukkan perilaku caching spesifik yang memengaruhi penghitungan token:

**Cara kerjanya:**

1. Caching hanya terjadi ketika Anda membuat permintaan berikutnya yang menyertakan hasil alat
2. Ketika permintaan berikutnya dibuat, riwayat percakapan sebelumnya (termasuk blok pemikiran) dapat di-cache
3. Blok pemikiran yang di-cache ini dihitung sebagai token input dalam metrik penggunaan Anda saat dibaca dari cache
4. Ketika blok pengguna non-hasil-alat disertakan: pada Opus 4.5+ dan Sonnet 4.6+, blok pemikiran sebelumnya disimpan; pada model Opus/Sonnet sebelumnya dan semua model Haiku, semua blok pemikiran sebelumnya diabaikan dan dihapus dari konteks

**Alur contoh terperinci:**

**Permintaan 1:**

```text wrap
User: "What's the weather in Paris?"
```

**Respons 1:**

```text wrap
[thinking_block_1] + [tool_use block 1]
```

**Permintaan 2:**

```text wrap
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True]
```

**Respons 2:**

```text wrap
[thinking_block_2] + [text block 2]
```

Permintaan 2 menulis cache dari konten permintaan (bukan respons). Cache mencakup pesan pengguna asli, blok pemikiran pertama, blok penggunaan alat, dan hasil alat.

**Permintaan 3:**

```text wrap
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [thinking_block_2] + [text block 2],
User: [Text response, cache=True]
```

Untuk Opus 4.5+ dan Sonnet 4.6+, semua blok pemikiran sebelumnya disimpan secara default. Untuk model Opus/Sonnet sebelumnya dan semua model Haiku, karena blok pengguna non-hasil-alat disertakan, semua blok pemikiran sebelumnya diabaikan dan dihapus dari konteks. Permintaan ini akan diproses sama seperti:

```text wrap
User: ["What's the weather in Paris?"],
Assistant: [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [text block 2],
User: [Text response, cache=True]
```

**Poin-poin penting:**

* Perilaku caching ini terjadi secara otomatis, bahkan tanpa penanda `cache_control` eksplisit
* Perilaku ini konsisten baik menggunakan pemikiran biasa maupun pemikiran tersisip

<AccordionGroup>
  <Accordion title="Caching prompt sistem (dipertahankan saat pemikiran berubah)">
    <CodeGroup>
      ```bash CLI
      # Ambil ~10 kB dari Pride and Prejudice untuk blok sistem yang di-cache
      curl -s https://www.gutenberg.org/cache/epub/1342/pg1342.txt \
        | head -c 10000 > pride.txt

      # Hasilkan body permintaan untuk anggaran pemikiran yang diberikan. Setelah CONTENT1
      # terisi (setelah giliran pertama), balasan asisten dan
      # pesan pengguna lanjutan ditambahkan sehingga percakapan bertambah.
      build_body() {
        cat <<YAML
      model: claude-sonnet-4-6
      max_tokens: 20000
      thinking:
        type: enabled
        budget_tokens: $1
      system:
        - type: text
          text: >-
            You are an AI assistant that is tasked with literary analysis.
            Analyze the following text carefully.
        - type: text
          text: "@./pride.txt"
          cache_control:
            type: ephemeral
      messages:
        - role: user
          content: Analyze the tone of this passage.
      YAML
        if [[ -n "${CONTENT1:-}" ]]; then
          printf '  - role: assistant\n    content: %s\n' "$CONTENT1"
          printf '  - role: user\n'
          printf '    content: Analyze the characters in this passage.\n'
        fi
      }

      # Permintaan pertama (anggaran 4000): membuat cache. Tangkap usage
      # dan content sebagai dua baris jsonl agar balasan dapat diteruskan.
      printf 'First request - establishing cache\n'
      {
        read -r USAGE1
        read -r CONTENT1
      } < <(build_body 4000 \
        | ant messages create --transform '[usage,content]' --format jsonl)
      printf 'First response usage: %s\n' "$USAGE1"

      # Permintaan kedua: anggaran sama, cache hit prompt sistem diharapkan.
      printf '\nSecond request - same thinking parameters (cache hit expected)\n'
      USAGE2=$(build_body 4000 \
        | ant messages create --transform usage --format jsonl)
      printf 'Second response usage: %s\n' "$USAGE2"

      # Permintaan ketiga: anggaran diubah menjadi 8000. Prompt sistem yang di-cache
      # masih kena (hit); hanya caching blok pesan yang diinvalidasi.
      printf '\nThird request - different thinking parameters (cache miss for messages)\n'
      USAGE3=$(build_body 8000 \
        | ant messages create --transform usage --format jsonl)
      printf 'Third response usage: %s\n' "$USAGE3"
      ```

      ```python Python
      import requests
      from bs4 import BeautifulSoup

      client = Anthropic()


      def fetch_article_content(url):
          response = requests.get(url)
          soup = BeautifulSoup(response.content, "html.parser")

          # Hapus elemen script dan style
          for script in soup(["script", "style"]):
              script.decompose()

          # Ambil teks
          text = soup.get_text()

          # Pecah menjadi baris-baris dan hapus spasi di awal dan akhir setiap baris
          lines = (line.strip() for line in text.splitlines())
          # Pisahkan frasa yang dipisahkan spasi ganda ke baris masing-masing
          chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
          # Buang baris kosong
          text = "\n".join(chunk for chunk in chunks if chunk)

          return text


      # Ambil konten artikel
      book_url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
      book_content = fetch_article_content(book_url)
      # Gunakan teks secukupnya untuk caching (beberapa bab pertama)
      LARGE_TEXT = book_content[:10000]

      SYSTEM_PROMPT = [
          {
              "type": "text",
              "text": "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully.",
          },
          {"type": "text", "text": LARGE_TEXT, "cache_control": {"type": "ephemeral"}},
      ]

      MESSAGES = [{"role": "user", "content": "Analyze the tone of this passage."}]

      # Permintaan pertama - membuat cache
      print("First request - establishing cache")
      response1 = client.messages.create(
          model="claude-sonnet-4-6",
          max_tokens=20000,
          thinking={"type": "enabled", "budget_tokens": 4000},
          system=SYSTEM_PROMPT,
          messages=MESSAGES,
      )

      print(f"First response usage: {response1.usage}")

      MESSAGES.append({"role": "assistant", "content": response1.content})
      MESSAGES.append({"role": "user", "content": "Analyze the characters in this passage."})
      # Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
      print("\nSecond request - same thinking parameters (cache hit expected)")
      response2 = client.messages.create(
          model="claude-sonnet-4-6",
          max_tokens=20000,
          thinking={"type": "enabled", "budget_tokens": 4000},
          system=SYSTEM_PROMPT,
          messages=MESSAGES,
      )

      print(f"Second response usage: {response2.usage}")

      # Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk messages)
      print("\nThird request - different thinking parameters (cache miss for messages)")
      response3 = client.messages.create(
          model="claude-sonnet-4-6",
          max_tokens=20000,
          thinking={
              "type": "enabled",
              "budget_tokens": 8000,  # Changed thinking budget
          },
          system=SYSTEM_PROMPT,  # System prompt remains cached
          messages=MESSAGES,  # Messages cache is invalidated
      )

      print(f"Third response usage: {response3.usage}")
      ```

      ```typescript TypeScript
      import axios from "axios";
      import * as cheerio from "cheerio";

      const client = new Anthropic();

      async function fetchArticleContent(url: string): Promise<string> {
        const response = await axios.get(url);
        const $ = cheerio.load(response.data);
        $("script, style").remove();
        let text = $.text();
        const lines = text.split("\n").map((line) => line.trim());
        text = lines.filter((line) => line.length > 0).join("\n");
        return text;
      }

      const bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
      const bookContent = await fetchArticleContent(bookUrl);
      const LARGE_TEXT = bookContent.slice(0, 10000);

      const SYSTEM_PROMPT: Anthropic.TextBlockParam[] = [
        {
          type: "text",
          text: "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully."
        },
        {
          type: "text",
          text: LARGE_TEXT,
          cache_control: { type: "ephemeral" }
        }
      ];

      const messages: Anthropic.MessageParam[] = [
        { role: "user", content: "Analyze the tone of this passage." }
      ];

      // Permintaan pertama - membuat cache
      console.log("First request - establishing cache");
      const response1 = await client.messages.create({
        model: "claude-sonnet-4-6",
        max_tokens: 20000,
        thinking: { type: "enabled", budget_tokens: 4000 },
        system: SYSTEM_PROMPT,
        messages
      });

      console.log(`First response usage: ${JSON.stringify(response1.usage)}`);

      messages.push({
        role: "assistant",
        content: response1.content
      });
      messages.push({
        role: "user",
        content: "Analyze the characters in this passage."
      });

      // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
      console.log("\nSecond request - same thinking parameters (cache hit expected)");
      const response2 = await client.messages.create({
        model: "claude-sonnet-4-6",
        max_tokens: 20000,
        thinking: { type: "enabled", budget_tokens: 4000 },
        system: SYSTEM_PROMPT,
        messages
      });

      console.log(`Second response usage: ${JSON.stringify(response2.usage)}`);

      // Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk pesan)
      console.log("\nThird request - different thinking parameters (cache miss for messages)");
      const response3 = await client.messages.create({
        model: "claude-sonnet-4-6",
        max_tokens: 20000,
        thinking: { type: "enabled", budget_tokens: 8000 },
        system: SYSTEM_PROMPT,
        messages
      });

      console.log(`Third response usage: ${JSON.stringify(response3.usage)}`);
      ```

      ```csharp C#
      AnthropicClient client = new();

      // Ambil konten buku
      using var httpClient = new HttpClient();
      var bookContent = await httpClient.GetStringAsync("https://www.gutenberg.org/cache/epub/1342/pg1342.txt");
      var largeText = bookContent.Substring(0, Math.Min(10000, bookContent.Length));

      var systemPrompt = new MessageCreateParamsSystem(new List<TextBlockParam>
      {
          new TextBlockParam()
          {
              Text = "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully."
          },
          new TextBlockParam()
          {
              Text = largeText,
              CacheControl = new CacheControlEphemeral(),
          },
      });

      var messages = new List<MessageParam>
      {
          new() { Role = Role.User, Content = "Analyze the tone of this passage." }
      };

      // Permintaan pertama - membuat cache
      Console.WriteLine("First request - establishing cache");
      var parameters1 = new MessageCreateParams
      {
          Model = Model.ClaudeSonnet4_6,
          MaxTokens = 20000,
          Thinking = new ThinkingConfigEnabled(budgetTokens: 4000),
          System = systemPrompt,
          Messages = messages
      };

      var response1 = await client.Messages.Create(parameters1);
      Console.WriteLine($"First response usage: {response1.Usage}");

      messages.Add(new() { Role = Role.Assistant, Content = response1.Content.Select(block => new ContentBlockParam(block.Json)).ToList() });
      messages.Add(new() { Role = Role.User, Content = "Analyze the characters in this passage." });

      // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
      Console.WriteLine("\nSecond request - same thinking parameters (cache hit expected)");
      var parameters2 = new MessageCreateParams
      {
          Model = Model.ClaudeSonnet4_6,
          MaxTokens = 20000,
          Thinking = new ThinkingConfigEnabled(budgetTokens: 4000),
          System = systemPrompt,
          Messages = messages
      };

      var response2 = await client.Messages.Create(parameters2);
      Console.WriteLine($"Second response usage: {response2.Usage}");

      // Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk pesan)
      Console.WriteLine("\nThird request - different thinking parameters (cache miss for messages)");
      var parameters3 = new MessageCreateParams
      {
          Model = Model.ClaudeSonnet4_6,
          MaxTokens = 20000,
          Thinking = new ThinkingConfigEnabled(budgetTokens: 8000),
          System = systemPrompt,
          Messages = messages
      };

      var response3 = await client.Messages.Create(parameters3);
      Console.WriteLine($"Third response usage: {response3.Usage}");
      ```

      ```go Go
      client := anthropic.NewClient()

      // Ambil konten buku
      resp, err := http.Get("https://www.gutenberg.org/cache/epub/1342/pg1342.txt")
      if err != nil {
      	log.Fatal(err)
      }
      defer resp.Body.Close()

      body, err := io.ReadAll(resp.Body)
      if err != nil {
      	log.Fatal(err)
      }

      largeText := string(body)
      if len(largeText) > 10000 {
      	largeText = largeText[:10000]
      }

      systemPrompt := []anthropic.TextBlockParam{
      	{Text: "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully."},
      	{
      		Text:         largeText,
      		CacheControl: anthropic.NewCacheControlEphemeralParam(),
      	},
      }

      messages := []anthropic.MessageParam{
      	anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the tone of this passage.")),
      }

      // Permintaan pertama - membuat cache
      fmt.Println("First request - establishing cache")
      response1, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeSonnet4_6,
      	MaxTokens: 20000,
      	Thinking:  anthropic.ThinkingConfigParamOfEnabled(4000),
      	System:    systemPrompt,
      	Messages:  messages,
      })
      if err != nil {
      	log.Fatal(err)
      }

      fmt.Printf("First response usage: %s\n", response1.Usage.RawJSON())

      messages = append(messages, response1.ToParam())
      messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the characters in this passage.")))

      // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
      fmt.Println("\nSecond request - same thinking parameters (cache hit expected)")
      response2, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeSonnet4_6,
      	MaxTokens: 20000,
      	Thinking:  anthropic.ThinkingConfigParamOfEnabled(4000),
      	System:    systemPrompt,
      	Messages:  messages,
      })
      if err != nil {
      	log.Fatal(err)
      }

      fmt.Printf("Second response usage: %s\n", response2.Usage.RawJSON())

      // Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk pesan)
      fmt.Println("\nThird request - different thinking parameters (cache miss for messages)")
      response3, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeSonnet4_6,
      	MaxTokens: 20000,
      	Thinking:  anthropic.ThinkingConfigParamOfEnabled(8000),
      	System:    systemPrompt,
      	Messages:  messages,
      })
      if err != nil {
      	log.Fatal(err)
      }

      fmt.Printf("Third response usage: %s\n", response3.Usage.RawJSON())
      ```

      ```java Java
      import com.anthropic.models.messages.CacheControlEphemeral;
      // ...
      void main() throws Exception {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          // Ambil konten buku
          HttpClient httpClient = HttpClient.newHttpClient();
          HttpRequest request = HttpRequest.newBuilder()
              .uri(URI.create("https://www.gutenberg.org/cache/epub/1342/pg1342.txt"))
              .build();
          HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
          String bookContent = response.body();
          String largeText = bookContent.substring(0, Math.min(10000, bookContent.length()));

          List<TextBlockParam> systemPrompt = List.of(
              TextBlockParam.builder()
                  .text("You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully.")
                  .build(),
              TextBlockParam.builder()
                  .text(largeText)
                  .cacheControl(CacheControlEphemeral.builder().build())
                  .build()
          );

          // Permintaan pertama - membuat cache
          IO.println("First request - establishing cache");
          MessageCreateParams params1 = MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_4_6)
              .maxTokens(20000L)
              .enabledThinking(4000L)
              .systemOfTextBlockParams(systemPrompt)
              .addUserMessage("Analyze the tone of this passage.")
              .build();

          Message response1 = client.messages().create(params1);
          IO.println("First response usage: " + response1.usage());

          // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
          IO.println("\nSecond request - same thinking parameters (cache hit expected)");
          MessageCreateParams params2 = MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_4_6)
              .maxTokens(20000L)
              .enabledThinking(4000L)
              .systemOfTextBlockParams(systemPrompt)
              .addUserMessage("Analyze the tone of this passage.")
              .addAssistantMessageOfBlockParams(response1.content().stream()
                  .map(block -> block.toParam())
                  .collect(java.util.stream.Collectors.toList()))
              .addUserMessage("Analyze the characters in this passage.")
              .build();

          Message response2 = client.messages().create(params2);
          IO.println("Second response usage: " + response2.usage());

          // Permintaan ketiga - parameter pemikiran berbeda (cache miss untuk pesan)
          IO.println("\nThird request - different thinking parameters (cache miss for messages)");
          MessageCreateParams params3 = MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_4_6)
              .maxTokens(20000L)
              .enabledThinking(8000L)
              .systemOfTextBlockParams(systemPrompt)
              .addUserMessage("Analyze the tone of this passage.")
              .addAssistantMessageOfBlockParams(response1.content().stream()
                  .map(block -> block.toParam())
                  .collect(java.util.stream.Collectors.toList()))
              .addUserMessage("Analyze the characters in this passage.")
              .build();

          Message response3 = client.messages().create(params3);
          IO.println("Third response usage: " + response3.usage());
      }
      ```

      ```php PHP
      $client = new Client();

      // Ambil konten buku
      $bookContent = file_get_contents("https://www.gutenberg.org/cache/epub/1342/pg1342.txt");
      $largeText = substr($bookContent, 0, 10000);

      $systemPrompt = [
          [
              'type' => 'text',
              'text' => 'You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully.'
          ],
          [
              'type' => 'text',
              'text' => $largeText,
              'cache_control' => ['type' => 'ephemeral']
          ]
      ];

      $messages = [
          ['role' => 'user', 'content' => 'Analyze the tone of this passage.']
      ];

      // Permintaan pertama - membuat cache
      echo "First request - establishing cache\n";
      $response1 = $client->messages->create(
          maxTokens: 20000,
          messages: $messages,
          model: 'claude-sonnet-4-6',
          system: $systemPrompt,
          thinking: ['type' => 'enabled', 'budget_tokens' => 4000],
      );

      echo "First response usage: " . json_encode($response1->usage) . "\n";

      $messages[] = ['role' => 'assistant', 'content' => $response1->content];
      $messages[] = ['role' => 'user', 'content' => 'Analyze the characters in this passage.'];

      // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
      echo "\nSecond request - same thinking parameters (cache hit expected)\n";
      $response2 = $client->messages->create(
          maxTokens: 20000,
          messages: $messages,
          model: 'claude-sonnet-4-6',
          system: $systemPrompt,
          thinking: ['type' => 'enabled', 'budget_tokens' => 4000],
      );

      echo "Second response usage: " . json_encode($response2->usage) . "\n";

      // Permintaan ketiga - parameter pemikiran yang berbeda (cache miss untuk pesan)
      echo "\nThird request - different thinking parameters (cache miss for messages)\n";
      $response3 = $client->messages->create(
          maxTokens: 20000,
          messages: $messages,
          model: 'claude-sonnet-4-6',
          system: $systemPrompt,
          thinking: ['type' => 'enabled', 'budget_tokens' => 8000],
      );

      echo "Third response usage: " . json_encode($response3->usage) . "\n";
      ```

      ```ruby Ruby
      require "net/http"
      require "uri"

      client = Anthropic::Client.new

      # Ambil konten buku
      uri = URI("https://www.gutenberg.org/cache/epub/1342/pg1342.txt")
      response = Net::HTTP.get_response(uri)
      book_content = response.body
      large_text = book_content[0...10000]

      system_prompt = [
        {
          type: "text",
          text: "You are an AI assistant that is tasked with literary analysis. Analyze the following text carefully."
        },
        {
          type: "text",
          text: large_text,
          cache_control: { type: "ephemeral" }
        }
      ]

      messages = [
        { role: "user", content: "Analyze the tone of this passage." }
      ]

      # Permintaan pertama - membuat cache
      puts "First request - establishing cache"
      response1 = client.messages.create(
        model: "claude-sonnet-4-6",
        max_tokens: 20000,
        thinking: {
          type: "enabled",
          budget_tokens: 4000
        },
        system: system_prompt,
        messages: messages
      )

      puts "First response usage: #{response1.usage}"

      messages << { role: "assistant", content: response1.content }
      messages << { role: "user", content: "Analyze the characters in this passage." }

      # Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
      puts "\nSecond request - same thinking parameters (cache hit expected)"
      response2 = client.messages.create(
        model: "claude-sonnet-4-6",
        max_tokens: 20000,
        thinking: {
          type: "enabled",
          budget_tokens: 4000
        },
        system: system_prompt,
        messages: messages
      )

      puts "Second response usage: #{response2.usage}"

      # Permintaan ketiga - parameter pemikiran yang berbeda (cache miss untuk pesan)
      puts "\nThird request - different thinking parameters (cache miss for messages)"
      response3 = client.messages.create(
        model: "claude-sonnet-4-6",
        max_tokens: 20000,
        thinking: {
          type: "enabled",
          budget_tokens: 8000
        },
        system: system_prompt,
        messages: messages
      )

      puts "Third response usage: #{response3.usage}"
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Caching pesan (dibatalkan saat pemikiran berubah)">
    <CodeGroup>
      ```bash CLI
      # Alur kerja ini tidak cocok diterjemahkan menjadi perintah shell sekali jalan.
      # Lihat tab SDK untuk pola multi-giliran; pemanggilan CLI per giliran
      # identik dengan contoh caching prompt sebelumnya.
      ```

      ```python Python
      import requests
      from bs4 import BeautifulSoup

      client = Anthropic()


      def fetch_article_content(url):
          response = requests.get(url)
          soup = BeautifulSoup(response.content, "html.parser")

          # Hapus elemen script dan style
          for script in soup(["script", "style"]):
              script.decompose()

          # Ambil teks
          text = soup.get_text()

          # Pecah menjadi baris-baris dan hapus spasi di awal dan akhir setiap baris
          lines = (line.strip() for line in text.splitlines())
          # Pisahkan frasa yang dipisahkan spasi ganda ke baris masing-masing
          chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
          # Buang baris kosong
          text = "\n".join(chunk for chunk in chunks if chunk)

          return text


      # Ambil konten artikel
      book_url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
      book_content = fetch_article_content(book_url)
      # Gunakan teks secukupnya untuk caching (beberapa bab pertama)
      LARGE_TEXT = book_content[:10000]

      # Tanpa prompt sistem - caching dilakukan di messages
      MESSAGES = [
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": LARGE_TEXT,
                      "cache_control": {"type": "ephemeral"},
                  },
                  {"type": "text", "text": "Analyze the tone of this passage."},
              ],
          }
      ]

      # Permintaan pertama - membuat cache
      print("First request - establishing cache")
      response1 = client.messages.create(
          model="claude-sonnet-4-6",
          max_tokens=20000,
          thinking={"type": "enabled", "budget_tokens": 4000},
          messages=MESSAGES,
      )

      print(f"First response usage: {response1.usage}")

      MESSAGES.append({"role": "assistant", "content": response1.content})
      MESSAGES.append({"role": "user", "content": "Analyze the characters in this passage."})
      # Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
      print("\nSecond request - same thinking parameters (cache hit expected)")
      response2 = client.messages.create(
          model="claude-sonnet-4-6",
          max_tokens=20000,
          thinking={
              "type": "enabled",
              "budget_tokens": 4000,  # Same thinking budget
          },
          messages=MESSAGES,
      )

      print(f"Second response usage: {response2.usage}")

      MESSAGES.append({"role": "assistant", "content": response2.content})
      MESSAGES.append({"role": "user", "content": "Analyze the setting in this passage."})

      # Permintaan ketiga - anggaran pemikiran berbeda (cache miss diharapkan)
      print("\nThird request - different thinking budget (cache miss expected)")
      response3 = client.messages.create(
          model="claude-sonnet-4-6",
          max_tokens=20000,
          thinking={
              "type": "enabled",
              "budget_tokens": 8000,  # Different thinking budget breaks cache
          },
          messages=MESSAGES,
      )

      print(f"Third response usage: {response3.usage}")
      ```

      ```typescript TypeScript
      import axios from "axios";
      import * as cheerio from "cheerio";

      const client = new Anthropic();

      async function fetchArticleContent(url: string): Promise<string> {
        const response = await axios.get(url);
        const $ = cheerio.load(response.data);

        // Hapus elemen script dan style
        $("script, style").remove();

        // Ambil teks
        let text = $.text();

        // Bersihkan teks (pecah menjadi baris, hapus spasi)
        const lines = text.split("\n").map((line) => line.trim());
        const chunks = lines.flatMap((line) => line.split("  ").map((phrase) => phrase.trim()));
        text = chunks.filter((chunk) => chunk).join("\n");

        return text;
      }

      const bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
      const bookContent = await fetchArticleContent(bookUrl);
      const LARGE_TEXT = bookContent.substring(0, 10000);

      // Tanpa prompt sistem - caching di messages sebagai gantinya
      const messages: Anthropic.MessageParam[] = [
        {
          role: "user",
          content: [
            {
              type: "text",
              text: LARGE_TEXT,
              cache_control: { type: "ephemeral" }
            },
            {
              type: "text",
              text: "Analyze the tone of this passage."
            }
          ]
        }
      ];

      // Permintaan pertama - membuat cache
      console.log("First request - establishing cache");
      const response1 = await client.messages.create({
        model: "claude-sonnet-4-6",
        max_tokens: 20000,
        thinking: { type: "enabled", budget_tokens: 4000 },
        messages
      });

      console.log("First response usage: ", response1.usage);

      messages.push(
        { role: "assistant", content: response1.content },
        { role: "user", content: "Analyze the characters in this passage." }
      );

      // Permintaan kedua - parameter thinking sama (cache hit diharapkan)
      console.log("\nSecond request - same thinking parameters (cache hit expected)");
      const response2 = await client.messages.create({
        model: "claude-sonnet-4-6",
        max_tokens: 20000,
        thinking: { type: "enabled", budget_tokens: 4000 },
        messages
      });

      console.log("Second response usage: ", response2.usage);

      messages.push(
        { role: "assistant", content: response2.content },
        { role: "user", content: "Analyze the setting in this passage." }
      );

      // Permintaan ketiga - budget thinking berbeda (cache miss diharapkan)
      console.log("\nThird request - different thinking budget (cache miss expected)");
      const response3 = await client.messages.create({
        model: "claude-sonnet-4-6",
        max_tokens: 20000,
        thinking: { type: "enabled", budget_tokens: 8000 },
        messages
      });

      console.log("Third response usage: ", response3.usage);
      ```

      ```csharp C#
      AnthropicClient client = new();

      string bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
      string bookContent = await FetchArticleContent(bookUrl);
      string largeText = bookContent.Substring(0, Math.Min(10000, bookContent.Length));

      Console.WriteLine("First request - establishing cache");
      var parameters1 = new MessageCreateParams
      {
          Model = Model.ClaudeSonnet4_6,
          MaxTokens = 20000,
          Thinking = new ThinkingConfigEnabled(budgetTokens: 4000),
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = new MessageParamContent(new List<ContentBlockParam>
                  {
                      new ContentBlockParam(new TextBlockParam()
                      {
                          Text = largeText,
                          CacheControl = new CacheControlEphemeral(),
                      }),
                      new ContentBlockParam(new TextBlockParam()
                      {
                          Text = "Analyze the tone of this passage."
                      }),
                  })
              }
          ]
      };

      var response1 = await client.Messages.Create(parameters1);
      Console.WriteLine($"First response usage: {response1.Usage}");

      Console.WriteLine("\nSecond request - same thinking parameters (cache hit expected)");
      var parameters2 = new MessageCreateParams
      {
          Model = Model.ClaudeSonnet4_6,
          MaxTokens = 20000,
          Thinking = new ThinkingConfigEnabled(budgetTokens: 4000),
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = new MessageParamContent(new List<ContentBlockParam>
                  {
                      new ContentBlockParam(new TextBlockParam()
                      {
                          Text = largeText,
                          CacheControl = new CacheControlEphemeral(),
                      }),
                      new ContentBlockParam(new TextBlockParam()
                      {
                          Text = "Analyze the tone of this passage."
                      }),
                  })
              },
              new()
              {
                  Role = Role.Assistant,
                  Content = response1.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              },
              new()
              {
                  Role = Role.User,
                  Content = "Analyze the characters in this passage."
              }
          ]
      };

      var response2 = await client.Messages.Create(parameters2);
      Console.WriteLine($"Second response usage: {response2.Usage}");

      Console.WriteLine("\nThird request - different thinking budget (cache miss expected)");
      var parameters3 = new MessageCreateParams
      {
          Model = Model.ClaudeSonnet4_6,
          MaxTokens = 20000,
          Thinking = new ThinkingConfigEnabled(budgetTokens: 8000),
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = new MessageParamContent(new List<ContentBlockParam>
                  {
                      new ContentBlockParam(new TextBlockParam()
                      {
                          Text = largeText,
                          CacheControl = new CacheControlEphemeral(),
                      }),
                      new ContentBlockParam(new TextBlockParam()
                      {
                          Text = "Analyze the tone of this passage."
                      }),
                  })
              },
              new()
              {
                  Role = Role.Assistant,
                  Content = response1.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              },
              new()
              {
                  Role = Role.User,
                  Content = "Analyze the characters in this passage."
              },
              new()
              {
                  Role = Role.Assistant,
                  Content = response2.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              },
              new()
              {
                  Role = Role.User,
                  Content = "Analyze the setting in this passage."
              }
          ]
      };

      var response3 = await client.Messages.Create(parameters3);
      Console.WriteLine($"Third response usage: {response3.Usage}");

      static async Task<string> FetchArticleContent(string url)
      {
          using HttpClient httpClient = new();
          string content = await httpClient.GetStringAsync(url);
          return content;
      }
      ```

      ```go Go
      client := anthropic.NewClient()

      bookURL := "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
      bookContent, err := fetchArticleContent(bookURL)
      if err != nil {
      	log.Fatal(err)
      }

      largeText := bookContent
      if len(largeText) > 10000 {
      	largeText = largeText[:10000]
      }

      // Tanpa prompt sistem - caching dilakukan di messages sebagai gantinya
      messages := []anthropic.MessageParam{
      	anthropic.NewUserMessage(
      		anthropic.ContentBlockParamUnion{OfText: &anthropic.TextBlockParam{
      			Text:         largeText,
      			CacheControl: anthropic.NewCacheControlEphemeralParam(),
      		}},
      		anthropic.NewTextBlock("Analyze the tone of this passage."),
      	),
      }

      // Permintaan pertama - membuat cache
      fmt.Println("First request - establishing cache")
      response1, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeSonnet4_6,
      	MaxTokens: 20000,
      	Thinking:  anthropic.ThinkingConfigParamOfEnabled(4000),
      	Messages:  messages,
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Printf("First response usage: %s\n", response1.Usage.RawJSON())

      messages = append(messages, response1.ToParam())
      messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the characters in this passage.")))

      // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
      fmt.Println("\nSecond request - same thinking parameters (cache hit expected)")
      response2, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeSonnet4_6,
      	MaxTokens: 20000,
      	Thinking:  anthropic.ThinkingConfigParamOfEnabled(4000),
      	Messages:  messages,
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Printf("Second response usage: %s\n", response2.Usage.RawJSON())

      messages = append(messages, response2.ToParam())
      messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the setting in this passage.")))

      // Permintaan ketiga - anggaran pemikiran berbeda (cache miss diharapkan)
      fmt.Println("\nThird request - different thinking budget (cache miss expected)")
      response3, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeSonnet4_6,
      	MaxTokens: 20000,
      	Thinking:  anthropic.ThinkingConfigParamOfEnabled(8000),
      	Messages:  messages,
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Printf("Third response usage: %s\n", response3.Usage.RawJSON())
      ```

      ```java Java
      import com.anthropic.models.messages.CacheControlEphemeral;
      // ...
      void main() throws Exception {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          String bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
          String bookContent = fetchArticleContent(bookUrl);
          String largeText = bookContent.substring(0, Math.min(10000, bookContent.length()));

          // Permintaan pertama - membuat cache
          IO.println("First request - establishing cache");
          MessageCreateParams params1 = MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_4_6)
              .maxTokens(20000L)
              .enabledThinking(4000L)
              .addUserMessageOfBlockParams(List.of(
                  ContentBlockParam.ofText(TextBlockParam.builder()
                      .text(largeText)
                      .cacheControl(CacheControlEphemeral.builder().build())
                      .build()),
                  ContentBlockParam.ofText(TextBlockParam.builder()
                      .text("Analyze the tone of this passage.")
                      .build())
              ))
              .build();

          Message response1 = client.messages().create(params1);
          IO.println("First response usage: " + response1.usage());

          // Permintaan kedua - parameter pemikiran yang sama (cache hit diharapkan)
          IO.println("\nSecond request - same thinking parameters (cache hit expected)");
          MessageCreateParams params2 = MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_4_6)
              .maxTokens(20000L)
              .enabledThinking(4000L)
              .addUserMessageOfBlockParams(List.of(
                  ContentBlockParam.ofText(TextBlockParam.builder()
                      .text(largeText)
                      .cacheControl(CacheControlEphemeral.builder().build())
                      .build()),
                  ContentBlockParam.ofText(TextBlockParam.builder()
                      .text("Analyze the tone of this passage.")
                      .build())
              ))
              .addAssistantMessageOfBlockParams(response1.content().stream()
                  .map(block -> block.toParam())
                  .collect(java.util.stream.Collectors.toList()))
              .addUserMessage("Analyze the characters in this passage.")
              .build();

          Message response2 = client.messages().create(params2);
          IO.println("Second response usage: " + response2.usage());

          // Permintaan ketiga - anggaran pemikiran berbeda (cache miss diharapkan)
          IO.println("\nThird request - different thinking budget (cache miss expected)");
          MessageCreateParams params3 = MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_4_6)
              .maxTokens(20000L)
              .enabledThinking(8000L)
              .addUserMessageOfBlockParams(List.of(
                  ContentBlockParam.ofText(TextBlockParam.builder()
                      .text(largeText)
                      .cacheControl(CacheControlEphemeral.builder().build())
                      .build()),
                  ContentBlockParam.ofText(TextBlockParam.builder()
                      .text("Analyze the tone of this passage.")
                      .build())
              ))
              .addAssistantMessageOfBlockParams(response1.content().stream()
                  .map(block -> block.toParam())
                  .collect(java.util.stream.Collectors.toList()))
              .addUserMessage("Analyze the characters in this passage.")
              .addAssistantMessageOfBlockParams(response2.content().stream()
                  .map(block -> block.toParam())
                  .collect(java.util.stream.Collectors.toList()))
              .addUserMessage("Analyze the setting in this passage.")
              .build();

          Message response3 = client.messages().create(params3);
          IO.println("Third response usage: " + response3.usage());
      }

      String fetchArticleContent(String url) throws Exception {
          HttpClient client = HttpClient.newHttpClient();
          HttpRequest request = HttpRequest.newBuilder()
              .uri(URI.create(url))
              .build();
          HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
          return response.body();
      }
      ```

      ```php PHP
      function fetchArticleContent($url) {
          $content = file_get_contents($url);
          $lines = explode("\n", $content);
          $cleanedLines = array_filter(array_map('trim', $lines));
          return implode("\n", $cleanedLines);
      }

      $client = new Client();

      $bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
      $bookContent = fetchArticleContent($bookUrl);
      $largeText = substr($bookContent, 0, 10000);

      echo "First request - establishing cache\n";
      $response1 = $client->messages->create(
          maxTokens: 20000,
          messages: [[
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => $largeText,
                      'cache_control' => ['type' => 'ephemeral']
                  ],
                  [
                      'type' => 'text',
                      'text' => 'Analyze the tone of this passage.'
                  ]
              ]
          ]],
          model: 'claude-sonnet-4-6',
          thinking: ['type' => 'enabled', 'budget_tokens' => 4000],
      );

      echo "First response usage: " . json_encode($response1->usage) . "\n";

      echo "\nSecond request - same thinking parameters (cache hit expected)\n";
      $response2 = $client->messages->create(
          maxTokens: 20000,
          messages: [
              [
                  'role' => 'user',
                  'content' => [
                      [
                          'type' => 'text',
                          'text' => $largeText,
                          'cache_control' => ['type' => 'ephemeral']
                      ],
                      [
                          'type' => 'text',
                          'text' => 'Analyze the tone of this passage.'
                      ]
                  ]
              ],
              [
                  'role' => 'assistant',
                  'content' => $response1->content
              ],
              [
                  'role' => 'user',
                  'content' => 'Analyze the characters in this passage.'
              ]
          ],
          model: 'claude-sonnet-4-6',
          thinking: ['type' => 'enabled', 'budget_tokens' => 4000],
      );

      echo "Second response usage: " . json_encode($response2->usage) . "\n";

      echo "\nThird request - different thinking budget (cache miss expected)\n";
      $response3 = $client->messages->create(
          maxTokens: 20000,
          messages: [
              [
                  'role' => 'user',
                  'content' => [
                      [
                          'type' => 'text',
                          'text' => $largeText,
                          'cache_control' => ['type' => 'ephemeral']
                      ],
                      [
                          'type' => 'text',
                          'text' => 'Analyze the tone of this passage.'
                      ]
                  ]
              ],
              [
                  'role' => 'assistant',
                  'content' => $response1->content
              ],
              [
                  'role' => 'user',
                  'content' => 'Analyze the characters in this passage.'
              ],
              [
                  'role' => 'assistant',
                  'content' => $response2->content
              ],
              [
                  'role' => 'user',
                  'content' => 'Analyze the setting in this passage.'
              ]
          ],
          model: 'claude-sonnet-4-6',
          thinking: ['type' => 'enabled', 'budget_tokens' => 8000],
      );

      echo "Third response usage: " . json_encode($response3->usage) . "\n";
      ```

      ```ruby Ruby
      require "net/http"
      require "uri"

      def fetch_article_content(url)
        uri = URI.parse(url)
        response = Net::HTTP.get_response(uri)
        text = response.body

        lines = text.split("\n").map(&:strip)
        lines.reject(&:empty?).join("\n")
      end

      client = Anthropic::Client.new

      book_url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
      book_content = fetch_article_content(book_url)
      large_text = book_content[0...10000]

      puts "First request - establishing cache"
      response1 = client.messages.create(
        model: "claude-sonnet-4-6",
        max_tokens: 20000,
        thinking: {
          type: "enabled",
          budget_tokens: 4000
        },
        messages: [{
          role: "user",
          content: [
            {
              type: "text",
              text: large_text,
              cache_control: { type: "ephemeral" }
            },
            {
              type: "text",
              text: "Analyze the tone of this passage."
            }
          ]
        }]
      )

      puts "First response usage: #{response1.usage}"

      puts "\nSecond request - same thinking parameters (cache hit expected)"
      response2 = client.messages.create(
        model: "claude-sonnet-4-6",
        max_tokens: 20000,
        thinking: {
          type: "enabled",
          budget_tokens: 4000
        },
        messages: [
          {
            role: "user",
            content: [
              {
                type: "text",
                text: large_text,
                cache_control: { type: "ephemeral" }
              },
              {
                type: "text",
                text: "Analyze the tone of this passage."
              }
            ]
          },
          {
            role: "assistant",
            content: response1.content
          },
          {
            role: "user",
            content: "Analyze the characters in this passage."
          }
        ]
      )

      puts "Second response usage: #{response2.usage}"

      puts "\nThird request - different thinking budget (cache miss expected)"
      response3 = client.messages.create(
        model: "claude-sonnet-4-6",
        max_tokens: 20000,
        thinking: {
          type: "enabled",
          budget_tokens: 8000
        },
        messages: [
          {
            role: "user",
            content: [
              {
                type: "text",
                text: large_text,
                cache_control: { type: "ephemeral" }
              },
              {
                type: "text",
                text: "Analyze the tone of this passage."
              }
            ]
          },
          {
            role: "assistant",
            content: response1.content
          },
          {
            role: "user",
            content: "Analyze the characters in this passage."
          },
          {
            role: "assistant",
            content: response2.content
          },
          {
            role: "user",
            content: "Analyze the setting in this passage."
          }
        ]
      )

      puts "Third response usage: #{response3.usage}"
      ```
    </CodeGroup>

    Berikut adalah output dari skrip (Anda mungkin melihat angka yang sedikit berbeda)

    ```text Output wrap
    First request - establishing cache
    First response usage: { cache_creation_input_tokens: 1370, cache_read_input_tokens: 0, input_tokens: 17, output_tokens: 700 }

    Second request - same thinking parameters (cache hit expected)

    Second response usage: { cache_creation_input_tokens: 0, cache_read_input_tokens: 1370, input_tokens: 303, output_tokens: 874 }

    Third request - different thinking budget (cache miss expected)
    Third response usage: { cache_creation_input_tokens: 1370, cache_read_input_tokens: 0, input_tokens: 747, output_tokens: 619 }
    ```

    Contoh ini menunjukkan bahwa ketika caching diatur dalam array pesan, mengubah parameter pemikiran (budget\_tokens ditingkatkan dari 4000 menjadi 8000) **membatalkan cache**. Permintaan ketiga tidak menunjukkan cache hit dengan `cache_creation_input_tokens=1370` dan `cache_read_input_tokens=0`, membuktikan bahwa caching berbasis pesan dibatalkan ketika parameter pemikiran berubah.
  </Accordion>
</AccordionGroup>

## Max tokens dan ukuran jendela konteks dengan pemikiran diperpanjang

`max_tokens` (yang mencakup anggaran pemikiran Anda saat pemikiran diaktifkan) diberlakukan sebagai batas ketat. Pada model Claude 4.5 dan yang lebih baru, jika token input ditambah `max_tokens` melebihi ukuran jendela konteks, API menerima permintaan tersebut. Jika generasi kemudian mencapai batas jendela konteks, generasi berhenti dengan `stop_reason: "model_context_window_exceeded"`. Pada model sebelumnya, API mengembalikan error validasi sebagai gantinya. Lihat [Menangani stop reason](/docs/id/build-with-claude/handling-stop-reasons).

<Note>
  Anda dapat membaca [panduan tentang jendela konteks](/docs/id/build-with-claude/context-windows) untuk analisis yang lebih terperinci.
</Note>

### Jendela konteks dengan pemikiran diperpanjang

Saat menghitung penggunaan jendela konteks dengan pemikiran diaktifkan, ada beberapa pertimbangan yang perlu diperhatikan:

* Pada Opus 4.5+ dan Sonnet 4.6+, blok pemikiran dari giliran sebelumnya disimpan dan dihitung dalam jendela konteks Anda; pada model Opus/Sonnet sebelumnya dan semua model Haiku, blok tersebut dihapus dan tidak dihitung
* Pemikiran giliran saat ini dihitung dalam batas `max_tokens` Anda untuk giliran tersebut

Diagram berikut menunjukkan manajemen token khusus ketika pemikiran diperpanjang diaktifkan:

![Diagram context window (jendela konteks) dengan extended thinking (pemikiran diperpanjang)](/docs/images/context-window-thinking.svg)

Jendela konteks efektif dihitung sebagai:

```text wrap
context window =
  (current input tokens - previous thinking tokens) +
  (thinking tokens + encrypted thinking tokens + text output tokens)
```

Gunakan [API penghitungan token](/docs/id/build-with-claude/token-counting) untuk mendapatkan jumlah token yang akurat untuk kasus penggunaan spesifik Anda, terutama saat bekerja dengan percakapan multi-giliran yang menyertakan pemikiran.

### Jendela konteks dengan pemikiran diperpanjang dan penggunaan alat

Saat menggunakan pemikiran diperpanjang dengan penggunaan alat, blok pemikiran harus secara eksplisit dilestarikan dan dikembalikan dengan hasil alat.

Perhitungan jendela konteks efektif untuk pemikiran diperpanjang dengan penggunaan alat menjadi:

```text wrap
context window =
  (current input tokens + previous thinking tokens + tool use tokens) +
  (thinking tokens + encrypted thinking tokens + text output tokens)
```

Diagram berikut mengilustrasikan manajemen token untuk pemikiran diperpanjang dengan penggunaan alat:

![Diagram context window (jendela konteks) dengan extended thinking (pemikiran diperpanjang) dan tool use (penggunaan alat)](/docs/images/context-window-thinking-tools.svg)

### Mengelola token dengan pemikiran diperpanjang

Mengingat perilaku jendela konteks dan `max_tokens` dengan pemikiran diperpanjang, Anda mungkin perlu:

* Memantau dan mengelola penggunaan token Anda secara lebih aktif
* Menyesuaikan nilai `max_tokens` saat panjang prompt Anda berubah
* Berpotensi menggunakan [endpoint penghitungan token](/docs/id/build-with-claude/token-counting) lebih sering
* Menyadari bahwa blok pemikiran sebelumnya tidak terakumulasi dalam jendela konteks Anda

## Enkripsi pemikiran

Konten pemikiran lengkap dienkripsi dan dikembalikan dalam field `signature`. Field ini memverifikasi bahwa blok pemikiran dihasilkan oleh Claude ketika dikirimkan kembali ke API.

<Note>
  Mengirim kembali blok pemikiran hanya benar-benar diperlukan saat menggunakan [alat dengan pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-tool-use). Selain itu, Anda dapat menghilangkan blok pemikiran dari giliran sebelumnya. Jika Anda mengirimkannya kembali, apakah API menyimpan atau menghapusnya bergantung pada model: Opus 4.5+ dan Sonnet 4.6+ menyimpannya dalam konteks secara default; model Opus/Sonnet sebelumnya dan semua model Haiku menghapusnya. Lihat [pengeditan konteks](/docs/id/build-with-claude/context-editing) untuk mengonfigurasi hal ini.

  Jika mengirim kembali blok pemikiran, kirimkan semuanya kembali persis seperti yang Anda terima demi konsistensi dan untuk menghindari potensi masalah.
</Note>

Berikut adalah beberapa pertimbangan penting tentang enkripsi pemikiran:

* Saat melakukan [streaming respons](/docs/id/build-with-claude/extended-thinking#streaming-thinking), signature ditambahkan melalui `signature_delta` di dalam event `content_block_delta` tepat sebelum event `content_block_stop`.
* Nilai `signature` secara signifikan lebih panjang pada model Claude 4 dibandingkan model sebelumnya.
* Field `signature` adalah field yang bersifat opaque dan tidak boleh diinterpretasikan atau di-parse.
* Nilai `signature` kompatibel di berbagai platform (API Claude, [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), dan [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai)). Nilai yang dihasilkan di satu platform kompatibel dengan platform lainnya.

## Blok pemikiran yang disunting

Selain blok `thinking` biasa, API dapat mengembalikan blok `redacted_thinking`. Blok `redacted_thinking` berisi konten pemikiran terenkripsi dalam field `data`, tanpa ringkasan yang dapat dibaca:

```json
{
  "type": "redacted_thinking",
  "data": "..."
}
```

Field `data` bersifat buram dan terenkripsi. Seperti field `signature` pada blok pemikiran biasa, Anda harus meneruskan blok `redacted_thinking` kembali ke API tanpa perubahan saat melanjutkan percakapan multi-giliran dengan [alat](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-tool-use).

<Tip>
  Jika kode Anda memfilter blok konten berdasarkan tipe (misalnya, `block.type == "thinking"`) saat mengirim bolak-balik respons dengan penggunaan alat, sertakan juga blok `redacted_thinking`. Memfilter hanya pada `block.type == "thinking"` secara diam-diam membuang blok `redacted_thinking` dan merusak protokol multi-giliran yang dijelaskan sebelumnya.
</Tip>

<Note>
  Blok `redacted_thinking` adalah tipe blok konten yang berbeda yang dikembalikan oleh API ketika sebagian pemikiran disunting demi keamanan. Ini terpisah dari opsi [`display: "omitted"`](#controlling-thinking-display), yang mengembalikan blok `thinking` biasa dengan field `thinking` yang kosong.
</Note>

## Perbedaan pemikiran di berbagai versi model

Messages API menangani pemikiran secara berbeda di berbagai versi model Claude. Tabel berikut memberikan perbandingan ringkas:

| Model                                                    | `budget_tokens` | Output pemikiran            | Pemikiran tersisip         | Pelestarian blok                                                        |
| -------------------------------------------------------- | --------------- | --------------------------- | -------------------------- | ----------------------------------------------------------------------- |
| Claude Fable 5 Claude Mythos 5                           | Tidak didukung  | Dihilangkan secara default1 | Otomatis2                  | Lihat [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) |
| [Claude Mythos Preview](https://anthropic.com/glasswing) | Didukung        | Dihilangkan secara default1 | Otomatis2                  | Dilestarikan3                                                           |
| Claude Opus 4.8                                          | Tidak didukung  | Dihilangkan secara default1 | Otomatis2                  | Dilestarikan                                                            |
| Claude Opus 4.7                                          | Tidak didukung  | Dihilangkan secara default1 | Otomatis2                  | Dilestarikan                                                            |
| Claude Sonnet 5                                          | Tidak didukung  | Dihilangkan secara default1 | Otomatis2                  | Dilestarikan                                                            |
| Claude Opus 4.6                                          | Usang           | Diringkas                   | Otomatis2                  | Dilestarikan                                                            |
| Claude Sonnet 4.6                                        | Usang           | Diringkas                   | Otomatis, atau header beta | Dilestarikan                                                            |
| Claude Opus 4.5                                          | Didukung        | Diringkas                   | Header beta                | Dilestarikan                                                            |
| Claude Haiku 4.5                                         | Didukung        | Diringkas                   | Tidak didukung             | Hanya giliran terakhir                                                  |
| Model Claude 4 sebelumnya                                | Didukung        | Diringkas                   | Header beta                | Hanya giliran terakhir                                                  |

*1 Atur `display: "summarized"` untuk menerima pemikiran yang diringkas. Pada Claude Fable 5, Claude Mythos 5, dan Claude Mythos Preview, token pemikiran mentah tidak pernah dikembalikan.*\
*2 Dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking). Header beta `interleaved-thinking-2025-05-14` tidak diperlukan pada model-model ini dan diabaikan dengan aman jika disertakan.*\
*3 Blok dihapus saat melanjutkan percakapan pada model yang tidak mendukung format pemikiran Mythos.*

### Pelestarian blok pemikiran berdasarkan model

Apakah blok pemikiran dari giliran asisten sebelumnya dilestarikan dalam konteks secara default bergantung pada kelas model. **Opus:** Claude Opus 4.5 dan model Opus yang lebih baru menyimpan semua blok pemikiran sebelumnya; Claude Opus 4.1 (usang) dan model Opus sebelumnya hanya menyimpan pemikiran giliran asisten terakhir. **Sonnet:** Claude Sonnet 4.6 dan model Sonnet yang lebih baru menyimpan semuanya; Claude Sonnet 4.5 dan model Sonnet sebelumnya hanya menyimpan giliran terakhir. **Haiku:** semua model Haiku hingga Claude Haiku 4.5 hanya menyimpan giliran terakhir. [Claude Mythos Preview](https://anthropic.com/glasswing) juga menyimpan semua blok pemikiran sebelumnya.

**Manfaat pelestarian blok pemikiran:**

* **Optimasi cache:** Saat menggunakan penggunaan alat, blok pemikiran yang dilestarikan memungkinkan cache hit karena diteruskan kembali dengan hasil alat dan di-cache secara bertahap di seluruh giliran asisten, menghasilkan penghematan token dalam alur kerja multi-langkah
* **Tidak ada dampak pada kecerdasan:** Melestarikan blok pemikiran tidak memiliki efek negatif pada kinerja model

**Pertimbangan penting:**

* **Penggunaan konteks:** Percakapan panjang akan mengonsumsi lebih banyak ruang konteks karena blok pemikiran dipertahankan dalam konteks
* **Perilaku otomatis:** Ini adalah default untuk setiap model seperti yang tercantum di atas. Tidak diperlukan perubahan kode atau header beta
* **Kompatibilitas mundur:** Untuk memanfaatkan fitur ini, terus teruskan blok pemikiran yang lengkap dan tidak dimodifikasi kembali ke API seperti yang Anda lakukan untuk penggunaan alat

<Note>
  Untuk model sebelumnya (seperti Claude Sonnet 4.5 dan Opus 4.1 (usang)), blok pemikiran dari giliran sebelumnya terus dihapus dari konteks. Perilaku yang ada yang dijelaskan di bagian [Pemikiran diperpanjang dengan caching prompt](#extended-thinking-with-prompt-caching) berlaku untuk model-model tersebut.
</Note>

## Harga

Untuk informasi harga lengkap termasuk tarif dasar, penulisan cache, cache hit, dan token output, lihat [halaman harga](/docs/id/about-claude/pricing).

Proses pemikiran dikenakan biaya untuk:

* Token yang digunakan selama pemikiran (token output)
* Blok pemikiran dari giliran asisten sebelumnya yang disimpan dalam konteks: hanya giliran terakhir pada model Opus/Sonnet yang lebih lama dan semua model Haiku; semua giliran secara default pada Opus 4.5+ dan Sonnet 4.6+ (token input)
* Token output teks standar

<Note>
  Ketika pemikiran diperpanjang diaktifkan, prompt sistem khusus secara otomatis disertakan untuk mendukung fitur ini.
</Note>

Saat menggunakan pemikiran yang diringkas:

* **Token input:** Token dalam permintaan asli Anda (tidak termasuk token pemikiran dari giliran sebelumnya)
* **Token output (ditagih):** Token pemikiran asli yang dihasilkan Claude secara internal
* **Token output (terlihat):** Token pemikiran yang diringkas yang Anda lihat dalam respons
* **Tanpa biaya:** Token yang digunakan untuk menghasilkan ringkasan

Saat menggunakan `display: "omitted"`:

* **Token input:** Token dalam permintaan asli Anda (sama seperti yang diringkas)
* **Token output (ditagih):** Token pemikiran asli yang dihasilkan Claude secara internal (sama seperti yang diringkas)
* **Token output (terlihat):** Nol token pemikiran (field `thinking` kosong)

<Warning>
  Jumlah token output yang ditagih **tidak** akan sama dengan jumlah token yang terlihat dalam respons. Anda ditagih untuk seluruh proses pemikiran, bukan konten pemikiran yang terlihat dalam respons.
</Warning>

Untuk melihat berapa banyak token output yang ditagih yang digunakan untuk penalaran internal, baca `usage.output_tokens_details.thinking_tokens` dalam respons. Nilai ini mencerminkan penalaran mentah yang dihasilkan model (bukan teks ringkasan yang dikembalikan dalam body) dan selalu kurang dari atau sama dengan `output_tokens`. Kurangi nilai ini dari `output_tokens` untuk memperkirakan bagian output yang bukan penalaran.

```json
{
  "usage": {
    "input_tokens": 25,
    "output_tokens": 348,
    "output_tokens_details": {
      "thinking_tokens": 312
    }
  }
}
```

`output_tokens` tetap menjadi total inklusif dan otoritatif yang digunakan untuk penagihan. `output_tokens_details` adalah rincian read-only untuk keperluan observabilitas.

## Praktik terbaik dan pertimbangan untuk pemikiran diperpanjang

### Bekerja dengan anggaran pemikiran

* **Optimasi anggaran:** Anggaran minimum adalah 1.024 token. Mulailah dari minimum dan tingkatkan anggaran pemikiran secara bertahap untuk menemukan rentang optimal untuk kasus penggunaan Anda. Jumlah token yang lebih tinggi memungkinkan penalaran yang lebih komprehensif tetapi dengan hasil yang semakin berkurang tergantung pada tugasnya. Meningkatkan anggaran dapat meningkatkan kualitas respons dengan kompromi berupa peningkatan "latency" (latensi). Untuk tugas-tugas kritis, uji pengaturan yang berbeda untuk menemukan keseimbangan optimal. Perhatikan bahwa anggaran pemikiran adalah target, bukan batas yang ketat. Penggunaan token aktual dapat bervariasi berdasarkan tugasnya.
* **Titik awal:** Mulailah dengan anggaran pemikiran yang lebih besar (16k+ token) untuk tugas-tugas kompleks dan sesuaikan berdasarkan kebutuhan Anda.
* **Anggaran besar:** Untuk anggaran pemikiran di atas 32k, gunakan [pemrosesan batch](/docs/id/build-with-claude/batch-processing) untuk menghindari masalah jaringan. Permintaan yang mendorong model untuk berpikir di atas 32k token menyebabkan permintaan yang berjalan lama yang mungkin terbentur dengan batas waktu sistem dan batas koneksi terbuka.
* **Pelacakan penggunaan token:** Pantau penggunaan token pemikiran untuk mengoptimalkan biaya dan kinerja. Field `usage.output_tokens_details.thinking_tokens` dalam respons melaporkan berapa banyak dari token output yang ditagih merupakan penalaran internal. Saat streaming, rincian ini hanya muncul pada event `message_delta` terakhir.

### Pertimbangan kinerja

* **Waktu respons:** Bersiaplah untuk waktu respons yang lebih lama karena pemrosesan tambahan. Menghasilkan blok pemikiran meningkatkan waktu respons secara keseluruhan.
* **Persyaratan streaming:** SDK memerlukan streaming ketika `max_tokens` lebih besar dari 21.333 untuk menghindari batas waktu HTTP pada permintaan yang berjalan lama. Ini adalah validasi sisi klien, bukan pembatasan API. Jika Anda tidak perlu memproses event secara bertahap, gunakan `.stream()` dengan `.get_final_message()` (Python) atau `.finalMessage()` (TypeScript) untuk mendapatkan objek `Message` lengkap tanpa menangani event individual. Lihat [Streaming Messages](/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events) untuk detailnya. Saat streaming, bersiaplah untuk menangani blok konten pemikiran dan teks saat mereka tiba.
* **Menghilangkan pemikiran untuk latensi:** Jika aplikasi Anda tidak menampilkan konten pemikiran, atur `display: "omitted"` pada konfigurasi pemikiran untuk mengurangi waktu-ke-token-teks-pertama. Lihat [Mengontrol tampilan pemikiran](#controlling-thinking-display).

### Kompatibilitas fitur

* Pemikiran tidak kompatibel dengan modifikasi `temperature` atau `top_k` atau dengan [penggunaan alat yang dipaksakan](/docs/id/agents-and-tools/tool-use/define-tools#forcing-tool-use).
* Ketika pemikiran diaktifkan, Anda dapat mengatur `top_p` ke nilai antara 1 dan 0,95.
* Anda tidak dapat mengisi respons terlebih dahulu (pre-fill) ketika pemikiran diaktifkan.
* Perubahan pada anggaran pemikiran membatalkan prefiks prompt yang di-cache yang menyertakan pesan. Namun, prompt sistem dan definisi alat yang di-cache akan tetap berfungsi ketika parameter pemikiran berubah.

### Panduan penggunaan

* **Pemilihan tugas:** Gunakan "extended thinking" (pemikiran diperpanjang) untuk tugas-tugas yang sangat kompleks yang mendapat manfaat dari penalaran langkah demi langkah, seperti matematika, pemrograman, dan analisis.
* **Penanganan konteks:** Anda tidak perlu menghapus blok pemikiran sebelumnya sendiri. Pada Opus 4.5+ dan Sonnet 4.6+, Claude API menyimpan blok pemikiran dari giliran sebelumnya secara default; pada model Opus/Sonnet yang lebih lama dan semua model Haiku, API secara otomatis mengabaikannya dan blok tersebut tidak disertakan saat menghitung penggunaan konteks.
* **Rekayasa prompt:** Tinjau [tips prompting pemikiran diperpanjang](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities) jika Anda ingin memaksimalkan kemampuan berpikir Claude.

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Pemikiran adaptif" icon="brain" href="/docs/id/build-with-claude/adaptive-thinking">
    Biarkan Claude menentukan kapan dan seberapa banyak menggunakan pemikiran diperpanjang.
  </Card>

  <Card title="Coba cookbook pemikiran diperpanjang" icon="book" href="https://platform.claude.com/cookbook/extended-thinking-extended-thinking">
    Jelajahi contoh praktis pemikiran di Cookbook.
  </Card>

  <Card title="Tips prompting pemikiran diperpanjang" icon="code" href="/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities">
    Pelajari praktik terbaik rekayasa prompt untuk pemikiran diperpanjang.
  </Card>
</CardGroup>
