---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/thinking
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 529578af488bda9da7b67b1433498b7b4523a66606df864d55bfe3c8f99907d7
---

---
title: Thinking
url: https://platform.claude.com/docs/id/build-with-claude/thinking
description: "Pahami cara kerja thinking Claude: mengaktifkannya, membaca output thinking, mengarahkan kedalaman thinking dengan effort, dan menggunakan thinking dengan alat, caching, dan streaming."
---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

Model yang menjawab dalam satu kali proses harus mendapatkan semuanya dengan benar pada percobaan pertama: tanpa coretan kerja, tanpa pemeriksaan, tanpa mengubah arah di tengah jalan. Untuk sebuah pembuktian, bug yang rumit, atau tugas agentic yang panjang, pendekatan pertama sering kali bukan yang terbaik.

Thinking menghilangkan batasan tersebut. Ketika thinking aktif, Claude mengerjakan masalah dengan kata-katanya sendiri sebelum menjawab: ia menyatakan ulang apa yang ditanyakan, mencoba berbagai pendekatan, memeriksa hasil antara, dan meninggalkan jalur yang tidak berhasil. Penalaran tersebut tiba dalam blok konten `thinking` sebelum respons, dan Claude memanfaatkannya untuk menghasilkan jawaban akhir. Inilah mengapa thinking meningkatkan performa pada tugas kompleks seperti matematika, pemrograman, analisis, dan pekerjaan agentic yang berjalan lama, di mana kualitas jawaban bergantung pada pekerjaan antara yang jika tidak demikian akan dipadatkan ke dalam respons itu sendiri atau dilewati.

Thinking memiliki biaya: token yang dihabiskan Claude untuk bernalar ditagih sebagai token output, bahkan ketika teks thinking tidak dikembalikan kepada Anda, dan token tersebut dihitung terhadap `max_tokens` bersama dengan teks respons. Halaman ini membahas bagaimana thinking berperilaku di seluruh permukaan API: mengaktifkannya, membaca outputnya, dan mengelola interaksinya dengan alat, streaming, caching, dan jendela konteks.

## Cara kerja thinking

![Diagram cara kerja thinking: Claude mengevaluasi permintaan dan memutuskan apakah akan berpikir; dengan penggunaan alat, thinking dapat berulang di antara pemanggilan alat; satu respons mengembalikan blok thinking, lalu blok teks](https://platform.claude.com/docs/images/how-thinking-works.svg)

Apakah Claude berpikir pada permintaan tertentu, dan seberapa dalam, bergantung pada konfigurasi thinking Anda dan kompleksitas permintaan.

Berikut adalah tampilan thinking dalam sebuah respons: satu atau lebih blok konten `thinking` tiba sebelum blok `text`. Blok thinking tetap merupakan konten yang dihasilkan, seperti blok `text` yang mengikutinya, tetapi dipisahkan dari respons kanonis. Setiap blok thinking juga membawa field `signature`, salinan terenkripsi dari penalaran lengkap yang Anda kirim kembali tanpa perubahan dalam percakapan multi-turn dan penggunaan alat (lihat [Enkripsi thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-encryption)):

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "Let me break this down. The question has two parts, so I'll start with the simpler one and use its result to constrain the second...",
      "signature": "WaUjzkypQ2mUEVM36O2Txu...."
    },
    {
      "type": "text",
      "text": "Based on my analysis..."
    }
  ]
}
```

Anda tidak selalu melihat teks ini, dan apa yang Anda lihat tidak pernah merupakan rantai pemikiran mentah: teks dalam blok thinking adalah [ringkasan dari penalaran Claude](https://platform.claude.com/docs/id/build-with-claude/thinking#summarized-thinking). Field `display` pada konfigurasi thinking mengontrol apakah ringkasan tersebut dikembalikan sama sekali: `"summarized"` mengembalikannya, sementara `"omitted"`, default pada model terbaru, mengembalikan blok thinking dengan field `thinking` kosong. Bagaimanapun, blok tersebut ditagih sama dan dikirim kembali dengan cara yang sama dalam percakapan multi-turn. Lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display) untuk default per-model dan detailnya.

Jika Claude menggunakan alat, thinking juga dapat muncul di antara pemanggilan alat. Lihat [Thinking dengan penggunaan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-with-tool-use). Untuk format respons lengkap, lihat [referensi Messages API](https://platform.claude.com/docs/id/api/messages/create).

## Mengonfigurasi thinking

Pada model saat ini, thinking aktif secara default atau hanya perlu satu parameter. Konfigurasi mana yang diterima setiap model, dan apa defaultnya, tercantum dalam [tabel konfigurasi per-model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#supported-models) di halaman Troubleshooting.

Pada Claude Opus 5, Claude Sonnet 5, Claude Fable 5, Claude Mythos 5, dan Claude Mythos Preview, thinking sudah aktif: tidak perlu konfigurasi. Hal pertama yang dibutuhkan sebagian besar developer pada model ini adalah melihat teks thinking, karena `display` secara default adalah `"omitted"` di sana. Aktifkan dengan `thinking: {"type": "adaptive", "display": "summarized"}`, yang persis merupakan permintaan berikut dengan [string model](https://platform.claude.com/docs/id/about-claude/models/overview) yang ditukar.

Pada Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6, thinking nonaktif sampai Anda mengatur `thinking: {type: "adaptive"}`, yang memungkinkan Claude memutuskan kapan dan seberapa dalam untuk berpikir berdasarkan permintaan. Contoh berikut melakukan hal tersebut, mengatur `display: "summarized"` agar teks thinking terlihat, dan menggunakan `max_tokens` yang lapang:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 16000,
      "thinking": {
        "type": "adaptive",
        "display": "summarized"
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
    --model claude-opus-4-8 \
    --max-tokens 16000 \
    --thinking '{type: adaptive, display: summarized}' \
    --message '{role: user, content: "What is the greatest common divisor of 1071 and 462?"}' \
    --transform content \
    --format yaml
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=16000,
      thinking={"type": "adaptive", "display": "summarized"},
      messages=[
          {
              "role": "user",
              "content": "What is the greatest common divisor of 1071 and 462?",
          }
      ],
  )

  for block in response.content:
      if block.type == "thinking":
          print(f"\nThinking: {block.thinking}")
      elif block.type == "text":
          print(f"\nResponse: {block.text}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    thinking: {
      type: "adaptive",
      display: "summarized"
    },
    messages: [
      {
        role: "user",
        content: "What is the greatest common divisor of 1071 and 462?"
      }
    ]
  });

  for (const block of response.content) {
    if (block.type === "thinking") {
      console.log(`\nThinking: ${block.thinking}`);
    } else if (block.type === "text") {
      console.log(`\nResponse: ${block.text}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigAdaptive { Display = Display.Summarized },
      Messages = [
          new() {
              Role = Role.User,
              Content = "What is the greatest common divisor of 1071 and 462?"
          }
      ]
  };

  var message = await client.Messages.Create(parameters);

  foreach (var block in message.Content)
  {
      if (block.TryPickThinking(out ThinkingBlock? thinking))
      {
          Console.WriteLine($"\nThinking: {thinking.Thinking}");
      }
      else if (block.TryPickText(out TextBlock? text))
      {
          Console.WriteLine($"\nResponse: {text.Text}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{
  			Display: anthropic.ThinkingConfigAdaptiveDisplaySummarized,
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the greatest common divisor of 1071 and 462?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range response.Content {
  	switch v := block.AsAny().(type) {
  	case anthropic.ThinkingBlock:
  		fmt.Printf("\nThinking: %s", v.Thinking)
  	case anthropic.TextBlock:
  		fmt.Printf("\nResponse: %s", v.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.messages.ThinkingConfigAdaptive;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(16000L)
          .thinking(ThinkingConfigAdaptive.builder()
              .display(ThinkingConfigAdaptive.Display.SUMMARIZED)
              .build())
          .addUserMessage("What is the greatest common divisor of 1071 and 462?")
          .build();

      Message response = client.messages().create(params);

      response.content().forEach(block -> {
          block.thinking().ifPresent(thinkingBlock ->
              IO.println("\nThinking: " + thinkingBlock.thinking())
          );
          block.text().ifPresent(textBlock ->
              IO.println("\nResponse: " + textBlock.text())
          );
      });
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 16000,
      messages: [
          [
              'role' => 'user',
              'content' => 'What is the greatest common divisor of 1071 and 462?'
          ]
      ],
      model: 'claude-opus-4-8',
      thinking: ['type' => 'adaptive', 'display' => 'summarized'],
  );

  foreach ($message->content as $block) {
      if ($block->type === 'thinking') {
          echo "\nThinking: " . $block->thinking;
      } elseif ($block->type === 'text') {
          echo "\nResponse: " . $block->text;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 16000,
    thinking: {
      type: "adaptive",
      display: "summarized"
    },
    messages: [
      {
        role: "user",
        content: "What is the greatest common divisor of 1071 and 462?"
      }
    ]
  )

  message.content.each do |block|
    case block.type
    when :thinking
      puts "\nThinking: #{block.thinking}"
    when :text
      puts "\nResponse: #{block.text}"
    end
  end
  ```
</CodeGroup>

Menjalankan contoh tersebut akan mencetak thinking yang diringkas, lalu jawabannya:

```text Output wrap
Thinking: Use Euclidean algorithm.
1071 = 2*462 + 147
462 = 3*147 + 21
147 = 7*21 + 0
GCD = 21

Response: ## Finding GCD of 1071 and 462

I'll use the **Euclidean algorithm**, repeatedly dividing and taking remainders...
```

Token thinking dihitung terhadap `max_tokens`, jadi atur nilainya cukup tinggi untuk menyisakan ruang bagi thinking dan teks respons. Lihat [Kontrol biaya](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#cost-control) di halaman steering dan [Thinking dan jendela konteks](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-the-context-window).

### Menonaktifkan thinking

Pada Claude Sonnet 5, di mana thinking aktif secara default, Anda dapat menonaktifkannya:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-sonnet-5",
      "max_tokens": 4096,
      "thinking": {"type": "disabled"},
      "messages": [
        {
          "role": "user",
          "content": "Summarize this article in one sentence."
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-sonnet-5 \
    --max-tokens 4096 \
    --thinking '{type: disabled}' \
    --message '{role: user, content: "Summarize this article in one sentence."}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-sonnet-5",
      max_tokens=4096,
      thinking={"type": "disabled"},
      messages=[{"role": "user", "content": "Summarize this article in one sentence."}],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 4096,
    thinking: { type: "disabled" },
    messages: [{ role: "user", content: "Summarize this article in one sentence." }]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 4096,
      Thinking = new ThinkingConfigDisabled(),
      Messages = [
          new() {
              Role = Role.User,
              Content = "Summarize this article in one sentence."
          }
      ]
  };

  var message = await client.Messages.Create(parameters);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet5,
  	MaxTokens: 4096,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfDisabled: &anthropic.ThinkingConfigDisabledParam{},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Summarize this article in one sentence.")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.messages.ThinkingConfigDisabled;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_SONNET_5)
          .maxTokens(4096L)
          .thinking(ThinkingConfigDisabled.builder().build())
          .addUserMessage("Summarize this article in one sentence.")
          .build();

      Message response = client.messages().create(params);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 4096,
      messages: [
          [
              'role' => 'user',
              'content' => 'Summarize this article in one sentence.'
          ]
      ],
      model: 'claude-sonnet-5',
      thinking: ['type' => 'disabled'],
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-sonnet-5",
    max_tokens: 4096,
    thinking: { type: "disabled" },
    messages: [
      {
        role: "user",
        content: "Summarize this article in one sentence."
      }
    ]
  )
  ```
</CodeGroup>

Claude Opus 5 juga memiliki thinking yang aktif secara default dan menerima `thinking: {type: "disabled"}` pada [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau di bawahnya. Pada effort `xhigh` atau `max`, thinking tidak dapat dinonaktifkan: permintaan yang menggabungkan `thinking: {type: "disabled"}` dengan level effort tersebut mengembalikan error 400. Pembatasan ini berlaku untuk Claude Opus 5 dan model yang lebih baru dan diberlakukan pada setiap permintaan. Dengan thinking dinonaktifkan, Claude Opus 5 terkadang dapat mengeluarkan pemanggilan alat sebagai teks biasa atau menyertakan tag XML internal dalam output yang terlihat. Lihat [Menjalankan dengan thinking dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk mitigasi prompting.

Claude Fable 5, Claude Mythos 5, dan Claude Mythos Preview menolak `thinking: {type: "disabled"}`: thinking tidak dapat dinonaktifkan pada model-model ini.

Jika model Anda hanya mendukung extended thinking (lihat [tabel konfigurasi per-model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#supported-models)), konfigurasikan dengan `type: "enabled"` dan nilai `budget_tokens` sebagai gantinya. Halaman [Extended thinking](https://platform.claude.com/docs/id/build-with-claude/extended-thinking) membahas konfigurasi tersebut. Dan jika konfigurasi thinking apa pun kembali dengan error 400, [Troubleshooting thinking](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting) mencocokkan setiap pesan error dengan perbaikannya.

## Membaca output thinking

### Mengontrol tampilan thinking

Field `display` pada konfigurasi thinking mengontrol bagaimana konten thinking dikembalikan dalam respons API. `display` berfungsi di kedua mode: atur bersama dengan `type: "adaptive"` atau `type: "enabled"`. Field ini menerima dua nilai:

* `"summarized"`: blok thinking berisi teks [thinking yang diringkas](https://platform.claude.com/docs/id/build-with-claude/thinking#summarized-thinking), ringkasan yang dapat dibaca dari penalaran Claude. Ini adalah default pada Claude Opus 4.6, Claude Sonnet 4.6, dan model sebelumnya.
* `"omitted"`: blok thinking dikembalikan dengan field `thinking` kosong. Field `signature` tetap membawa thinking lengkap yang terenkripsi untuk kontinuitas multi-turn (lihat [Enkripsi thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-encryption)). Ini adalah default pada Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, dan [Claude Mythos Preview](https://anthropic.com/glasswing).

Atur `display: "omitted"` ketika aplikasi Anda tidak menampilkan konten thinking kepada pengguna. Manfaat utamanya adalah time-to-first-text-token yang lebih cepat saat streaming: server melewati streaming token thinking sepenuhnya dan hanya mengirimkan signature, sehingga respons teks akhir mulai di-stream lebih cepat.

Dengan `display: "omitted"`, respons berisi blok `thinking` dengan field `thinking` kosong:

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

Perhatikan hal-hal berikut saat bekerja dengan thinking yang dihilangkan:

* Anda tetap dikenakan biaya untuk token thinking penuh. Menghilangkan mengurangi latensi, bukan biaya.
* Jika Anda mengirim kembali blok thinking dalam percakapan multi-turn, kirim tanpa perubahan. Server mendekripsi `signature` untuk merekonstruksi thinking asli untuk konstruksi prompt (lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks)). Teks apa pun yang Anda tempatkan di field `thinking` dari blok omitted yang di-round-trip akan diabaikan.
* `display` tidak valid dengan `thinking.type: "disabled"` (tidak ada yang perlu ditampilkan).
* Saat menggunakan `thinking.type: "adaptive"` dan model melewati thinking untuk permintaan sederhana, tidak ada blok thinking yang dihasilkan terlepas dari `display`.
* Saat streaming dengan `display: "omitted"`, tidak ada event `thinking_delta` yang dikeluarkan. Lihat [Streaming thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#streaming-thinking) untuk urutan event.

<Note>
  Field `signature` identik baik `display` adalah `"summarized"` maupun `"omitted"`. Mengganti nilai `display` antar turn dalam percakapan didukung.
</Note>

Dalam Ruby SDK, hash biasa menerima `display:` seperti yang ditunjukkan contoh. Kelas bertipe `ThinkingConfigAdaptive` menamai parameter tersebut `display_` (dengan garis bawah di akhir, untuk menghindari pembayangan `Kernel#display` Ruby). Bagaimanapun, field pada wire tetap `display`.

### Thinking yang diringkas

Ketika `display` adalah `"summarized"`, teks thinking yang Anda terima adalah ringkasan dari proses thinking lengkap Claude, bukan rantai pemikiran mentah. Thinking yang diringkas memberikan manfaat kecerdasan penuh dari thinking sambil mencegah penyalahgunaan. Tidak ada pengaturan `display` yang mengembalikan rantai pemikiran mentah.

Perhatikan hal-hal berikut saat bekerja dengan thinking yang diringkas:

* Anda dikenakan biaya untuk token thinking penuh yang dihasilkan oleh permintaan asli, bukan token ringkasan. Jumlah token output yang ditagih tidak cocok dengan jumlah token yang Anda lihat dalam respons.
* Pada Claude Opus 4.6, Claude Sonnet 4.6, dan model sebelumnya, beberapa baris pertama dari output thinking lebih verbose, memberikan penalaran terperinci yang sangat membantu untuk tujuan prompt engineering. [Claude Mythos Preview](https://anthropic.com/glasswing) meringkas dari token pertama, sehingga blok thinking-nya tidak menunjukkan pembukaan verbose ini.
* Peringkasan mempertahankan ide-ide kunci dari proses thinking Claude dengan latensi tambahan minimal, sehingga ringkasan dapat di-stream saat tiba.
* Peringkasan diproses oleh model yang berbeda dari yang Anda targetkan dalam permintaan Anda. Model thinking tidak melihat output yang diringkas.
* Karena Anthropic berupaya meningkatkan fitur thinking, perilaku peringkasan dapat berubah.

<Note>
  Dalam kasus langka di mana Anda memerlukan akses ke output thinking penuh, [hubungi tim penjualan Anthropic](mailto:sales@anthropic.com).
</Note>

### Streaming thinking

Thinking berfungsi dengan [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming). Blok thinking di-stream sebagai event `thinking_delta` di dalam event `content_block_delta`, diikuti oleh satu event `signature_delta` tepat sebelum `content_block_stop` blok tersebut. Blok teks di-stream setelahnya seperti biasa.

![Diagram urutan event streaming dengan thinking: blok thinking terbuka, thinking delta di-stream hanya ketika display adalah summarized, satu signature delta menutup blok, lalu text delta di-stream](https://platform.claude.com/docs/images/how-thinking-streams.svg)

Contoh berikut melakukan streaming respons dengan adaptive thinking, mencetak thinking dan text delta saat tiba:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 16000,
      "stream": true,
      "thinking": {
        "type": "adaptive",
        "display": "summarized"
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
    --model claude-opus-4-8 \
    --max-tokens 16000 \
    --thinking '{type: adaptive, display: summarized}' \
    --message '{role: user, content: "What is the greatest common divisor of 1071 and 462?"}' \
    --stream \
    --format jsonl
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      model="claude-opus-4-8",
      max_tokens=16000,
      thinking={"type": "adaptive", "display": "summarized"},
      messages=[
          {
              "role": "user",
              "content": "What is the greatest common divisor of 1071 and 462?",
          }
      ],
  ) as stream:
      for event in stream:
          if event.type == "content_block_start":
              print(f"\nStarting {event.content_block.type} block...")
          elif event.type == "content_block_delta":
              if event.delta.type == "thinking_delta":
                  print(event.delta.thinking, end="", flush=True)
              elif event.delta.type == "text_delta":
                  print(event.delta.text, end="", flush=True)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.messages.stream({
    model: "claude-opus-4-8",
    max_tokens: 16000,
    thinking: { type: "adaptive", display: "summarized" },
    messages: [{ role: "user", content: "What is the greatest common divisor of 1071 and 462?" }]
  });

  for await (const event of stream) {
    if (event.type === "content_block_start") {
      console.log(`\nStarting ${event.content_block.type} block...`);
    } else if (event.type === "content_block_delta") {
      if (event.delta.type === "thinking_delta") {
        process.stdout.write(event.delta.thinking);
      } else if (event.delta.type === "text_delta") {
        process.stdout.write(event.delta.text);
      }
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 16000,
      Thinking = new ThinkingConfigAdaptive { Display = Display.Summarized },
      Messages = [new() { Role = Role.User, Content = "What is the greatest common divisor of 1071 and 462?" }]
  };

  await foreach (var rawEvent in client.Messages.CreateStreaming(parameters))
  {
      if (rawEvent.TryPickContentBlockStart(out var start))
      {
          Console.WriteLine($"\nStarting {start.ContentBlock.Type} block...");
      }
      else if (rawEvent.TryPickContentBlockDelta(out var delta))
      {
          if (delta.Delta.TryPickThinking(out var thinkingDelta))
          {
              Console.Write(thinkingDelta.Thinking);
          }
          else if (delta.Delta.TryPickText(out var textDelta))
          {
              Console.Write(textDelta.Text);
          }
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 16000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{
  			Display: anthropic.ThinkingConfigAdaptiveDisplaySummarized,
  		},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the greatest common divisor of 1071 and 462?")),
  	},
  })

  for stream.Next() {
  	event := stream.Current()
  	switch eventVariant := event.AsAny().(type) {
  	case anthropic.ContentBlockStartEvent:
  		fmt.Printf("\nStarting %s block...\n", eventVariant.ContentBlock.Type)
  	case anthropic.ContentBlockDeltaEvent:
  		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
  		case anthropic.ThinkingDelta:
  			fmt.Print(deltaVariant.Thinking)
  		case anthropic.TextDelta:
  			fmt.Print(deltaVariant.Text)
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.messages.ThinkingConfigAdaptive;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(16000L)
          .thinking(ThinkingConfigAdaptive.builder()
              .display(ThinkingConfigAdaptive.Display.SUMMARIZED)
              .build())
          .addUserMessage("What is the greatest common divisor of 1071 and 462?")
          .build();

      try (var streamResponse = client.messages().createStreaming(params)) {
          streamResponse.stream().forEach(event -> {
              if (event.contentBlockStart().isPresent()) {
                  var startEvent = event.contentBlockStart().get();
                  var block = startEvent.contentBlock();
                  if (block.isThinking()) {
                      IO.println("\nStarting thinking block...");
                  } else if (block.isText()) {
                      IO.println("\nStarting text block...");
                  }
              } else if (event.contentBlockDelta().isPresent()) {
                  var deltaEvent = event.contentBlockDelta().get();
                  deltaEvent.delta().thinking().ifPresent(td ->
                      IO.print(td.thinking())
                  );
                  deltaEvent.delta().text().ifPresent(td ->
                      IO.print(td.text())
                  );
              }
          });
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $stream = $client->messages->createStream(
      maxTokens: 16000,
      messages: [
          ['role' => 'user', 'content' => 'What is the greatest common divisor of 1071 and 462?']
      ],
      model: 'claude-opus-4-8',
      thinking: ['type' => 'adaptive', 'display' => 'summarized'],
  );

  foreach ($stream as $event) {
      if ($event->type === 'content_block_start') {
          echo "\nStarting {$event->contentBlock->type} block...\n";
      } elseif ($event->type === 'content_block_delta') {
          if ($event->delta->type === 'thinking_delta') {
              echo $event->delta->thinking;
          } elseif ($event->delta->type === 'text_delta') {
              echo $event->delta->text;
          }
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  stream = client.messages.stream(
    model: "claude-opus-4-8",
    max_tokens: 16000,
    thinking: { type: "adaptive", display: "summarized" },
    messages: [
      { role: "user", content: "What is the greatest common divisor of 1071 and 462?" }
    ]
  )

  stream.each do |event|
    case event
    when Anthropic::Streaming::ThinkingEvent
      print event.thinking
    when Anthropic::Streaming::TextEvent
      print event.text
    end
  end
  ```
</CodeGroup>

Untuk menyusun kembali blok thinking lengkap dengan signature-nya setelah streaming, gunakan helper akumulasi pesan SDK Anda jika tersedia (misalnya, `stream.get_final_message()` di Python atau `stream.finalMessage()` di TypeScript) alih-alih menggabungkan delta sendiri.

<Accordion title="Jejak event streaming lengkap">
  ```sse Output
  event: message_start
  data: {"type": "message_start", "message": {"id": "msg_01...", "type": "message", "role": "assistant", "content": [], "model": "claude-opus-4-8", "stop_reason": null, "stop_sequence": null}}

  event: content_block_start
  data: {"type": "content_block_start", "index": 0, "content_block": {"type": "thinking", "thinking": "", "signature": ""}}

  event: content_block_delta
  data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "I need to find the GCD of 1071 and 462 using the Euclidean algorithm.\n\n1071 = 2 × 462 + 147"}}

  event: content_block_delta
  data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "\n462 = 3 × 147 + 21\n147 = 7 × 21 + 0\n\nSo GCD(1071, 462) = 21"}}

  // Additional thinking deltas...

  event: content_block_delta
  data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM1gbcDa9GJwZA2b..."}}

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
</Accordion>

Ketika `display: "omitted"` diatur, blok thinking terbuka, satu `signature_delta` tiba, dan blok ditutup tanpa event `thinking_delta` apa pun. Streaming teks dimulai segera setelahnya:

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
  Saat menggunakan streaming dengan thinking diaktifkan, Anda mungkin memperhatikan bahwa teks terkadang tiba dalam potongan yang lebih besar bergantian dengan pengiriman token-per-token yang lebih kecil. Ini adalah perilaku yang diharapkan, terutama untuk konten thinking.

  Sistem streaming memproses konten dalam batch, yang dapat menunda dan mengelompokkan event streaming ke dalam pola pengiriman "berpotongan" ini.
</Note>

Untuk mekanisme streaming umum, lihat [Streaming Messages](https://platform.claude.com/docs/id/build-with-claude/streaming).

## Thinking dan effort

Parameter `thinking` mengontrol apakah Claude berpikir dalam [blok pemikiran](https://platform.claude.com/docs/id/build-with-claude/thinking) sebelum menjawab; parameter `effort` mengontrol seberapa banyak upaya yang Claude curahkan untuk keseluruhan respons, yang dalam mode adaptif mencakup seberapa sering dan seberapa dalam Claude berpikir. Jangan meneruskan `adaptive` sebagai nilai `effort`: `adaptive` adalah mode berpikir, bukan tingkat effort.

Untuk apa yang dilakukan setiap level effort terhadap perilaku thinking, lihat [tabel perilaku thinking per-level](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#effort-levels) di halaman [Mengarahkan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost). Halaman [Effort](https://platform.claude.com/docs/id/build-with-claude/effort) mendokumentasikan parameter itu sendiri, termasuk level mana yang didukung setiap model. Pada Claude Opus 4.5, satu-satunya model khusus extended-thinking yang mendukung effort, effort berkomposisi dengan `budget_tokens`. Lihat [Aturan dan penyetelan budget](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#budget-rules-and-tuning).

Dengan dua kontrol yang dipisahkan seperti ini, pilih yang sesuai dengan tujuan Anda:

* **Menurunkan biaya atau latensi pada beban kerja dengan thinking diaktifkan:** turunkan `effort` terlebih dahulu. Ini menskalakan seluruh respons ke bawah, termasuk thinking.
* **Claude berpikir terlalu jarang atau terlalu dangkal:** naikkan `effort`, atau lihat [Mengarahkan seberapa sering Claude berpikir](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#tuning-thinking-behavior) di halaman steering.
* **Anda perlu thinking sepenuhnya nonaktif:** gunakan `thinking: {type: "disabled"}` pada model yang mengizinkannya (lihat [tabel konfigurasi per-model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#supported-models)).
* **Anda perlu batas atas keras pada pengeluaran:** gunakan `max_tokens`. Effort adalah panduan lunak. `max_tokens` adalah batas ketat.

## Thinking dengan penggunaan alat

Thinking bekerja bersama [penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview), memungkinkan Claude bernalar melalui pemilihan alat dan memproses hasil alat. Dua batasan berlaku:

1. **Batasan tool choice (mode manual):** penggunaan alat dengan extended thinking manual (`thinking: {type: "enabled"}`) hanya mendukung `tool_choice: {"type": "auto"}` (default) atau `tool_choice: {"type": "none"}`. Menggunakan `tool_choice: {"type": "any"}` atau `tool_choice: {"type": "tool", "name": "..."}` menghasilkan error karena opsi ini memaksa penggunaan alat, yang tidak kompatibel dengan extended thinking manual. Adaptive thinking, termasuk pada model di mana thinking aktif secara default, mendukung penggunaan alat yang dipaksa.
2. **Mempertahankan blok thinking:** ketika Anda mengembalikan hasil alat, Anda harus mengirim kembali blok thinking dari pesan asisten ke API, lengkap dan tidak dimodifikasi. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).

**Loop penggunaan alat adalah satu turn asisten.** Dari perspektif model, turn asisten tidak selesai sampai Claude menyelesaikan respons penuhnya, yang mungkin mencakup beberapa pemanggilan alat dan hasil. Seluruh urutan ini adalah satu turn asisten:

```text wrap
User: "What's the weather in Paris?"
Assistant: [thinking] + [tool_use: get_weather]
User: [tool_result: "20°C, sunny"]
Assistant: [text: "The weather in Paris is 20°C and sunny"]
```

Seluruh turn berjalan dalam satu mode thinking: Anda tidak dapat mengalihkan thinking di tengah turn, termasuk selama loop penggunaan alat. Dalam mode extended (manual), API juga memberlakukan bahwa turn asisten terakhir dari permintaan dengan thinking diaktifkan dimulai dengan blok thinking. Mode adaptive melonggarkan ini: tidak ada turn asisten yang perlu dimulai dengan blok thinking.

**Konflik di tengah turn terdegradasi dengan baik.** Jika Anda mengalihkan thinking di tengah turn (misalnya, antara mengirim pemanggilan alat dan mengembalikan hasilnya), API tidak mengembalikan error. Sebaliknya, API secara diam-diam menonaktifkan thinking untuk permintaan tersebut. Untuk mempertahankan kualitas model, API dapat menghapus blok thinking yang akan menciptakan struktur turn yang tidak valid, atau menonaktifkan thinking ketika riwayat percakapan tidak kompatibel dengan thinking yang diaktifkan. Untuk mengonfirmasi apakah thinking aktif, periksa keberadaan blok `thinking` dalam respons.

**Alihkan antar turn, bukan di dalamnya.** Rencanakan strategi thinking Anda di awal setiap turn. Selesaikan turn asisten, lalu ubah konfigurasi thinking untuk turn berikutnya:

```text wrap
User: "What's the weather?"
Assistant: [tool_use] (thinking disabled)
User: [tool_result]
Assistant: [text: "It's sunny"]
User: "What about tomorrow?"
Assistant: [thinking] + [text: "..."] (thinking enabled - new turn)
```

Mengalihkan mode thinking juga membatalkan caching prompt. Lihat [Thinking dan caching prompt](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-prompt-caching).

### Mempertahankan blok thinking

Ketika Claude memanggil alat, ia menjeda konstruksi responsnya untuk menunggu informasi eksternal. Ketika Anda mengembalikan hasil alat, Claude melanjutkan membangun respons yang sama, sehingga penalaran sebelumnya harus tetap ada. Kirim kembali setiap blok `thinking` ke API secara lengkap dan tidak dimodifikasi, bersama dengan blok `tool_use` yang menyertainya. Ini penting karena dua alasan:

1. **Kontinuitas penalaran:** blok thinking menangkap penalaran langkah demi langkah yang mengarah ke permintaan alat. Menyertakannya memungkinkan Claude melanjutkan penalaran dari tempat ia berhenti.
2. **Pemeliharaan konteks:** hasil alat muncul sebagai pesan pengguna dalam struktur API, tetapi mereka adalah bagian dari satu alur penalaran yang berkelanjutan. Mempertahankan blok thinking menjaga alur tersebut di seluruh panggilan API.

Singkatnya:

* **Wajib:** dalam turn penggunaan alat, kirim kembali blok thinking.
* **Direkomendasikan:** antar turn, kirim kembali semuanya.
* **Diizinkan:** di luar penggunaan alat, hilangkan thinking dari turn sebelumnya.

Anda tidak perlu memangkas thinking lama sendiri. Kirim kembali semua blok thinking dalam percakapan multi-turn, dan API secara otomatis memfilternya, menyimpan blok yang diperlukan untuk mempertahankan penalaran model, dan menagih token input hanya untuk blok yang benar-benar ditampilkan ke Claude. Blok turn sebelumnya mana yang disimpan bersifat per-model. Lihat [Preservasi blok thinking berdasarkan model](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-block-preservation-by-model). Untuk mengganti default, gunakan [strategi context-editing `clear_thinking_20251015`](https://platform.claude.com/docs/id/build-with-claude/context-editing#thinking-block-clearing).

Dalam pesan asisten terbaru, urutan blok `thinking` berturut-turut harus cocok dengan apa yang dihasilkan model dalam permintaan asli: Anda tidak dapat menyusun ulang, mengedit, atau menghapus sebagian. Ini termasuk [blok `redacted_thinking`](https://platform.claude.com/docs/id/build-with-claude/thinking#redacted-thinking-blocks).

<Note>
  Blok thinking yang dimodifikasi ditolak dengan error 400. Lihat [Error 400 mengatakan blok thinking tidak dapat dimodifikasi](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-blocks-modified) untuk pesan persisnya, penyebab umum, dan perbaikannya. Satu pengecualian: teks yang ditempatkan di field `thinking` kosong dari blok [omitted](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display) diabaikan alih-alih ditolak.
</Note>

Untuk panduan lengkap dua turn dengan kode di setiap SDK, lihat [Thinking dalam alur kerja alat dan multi-turn](https://platform.claude.com/docs/id/build-with-claude/thinking-tool-workflows#two-turn-tool-use-round-trip). Panduan tersebut mendefinisikan alat, menerima respons thinking-plus-tool-use, dan mengirim kembali turn asisten dengan hasil alat.

### Interleaved thinking

Interleaved thinking memungkinkan Claude berpikir di antara pemanggilan alat, bernalar tentang setiap hasil alat sebelum bertindak berdasarkan hasil tersebut. Dengan interleaved thinking, Claude dapat:

* Bernalar tentang hasil pemanggilan alat sebelum memutuskan apa yang harus dilakukan selanjutnya
* Merangkai beberapa pemanggilan alat dengan langkah penalaran di antaranya
* Membuat keputusan yang lebih bernuansa berdasarkan hasil antara

<Note>
  Pemanggilan alat berturut-turut tidak memerlukan interleaved thinking. Claude dapat merangkai pemanggilan alat dengan atau tanpa interleaved thinking. Interleaving mengubah di mana blok thinking muncul di antara pemanggilan alat, bukan apakah pemanggilan alat dapat dirangkai.
</Note>

Dengan adaptive thinking, interleaved thinking otomatis pada setiap model yang mendukung adaptive thinking. Tidak diperlukan header beta. Pada Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5, Claude Opus 4.8, dan Claude Opus 4.7, penalaran di antara pemanggilan alat selalu muncul dalam blok thinking. Claude Haiku 4.5 tidak mendukung interleaved thinking. Pada model yang menggunakan extended thinking manual, interleaving memerlukan header beta dan mengubah cara budget thinking dihitung. [Interleaved thinking dalam mode manual](https://platform.claude.com/docs/id/build-with-claude/extended-thinking#interleaved-thinking) membahas aturan per-model dan perilaku header spesifik platform.

Dengan interleaved thinking, alokasi thinking dapat mencakup seluruh turn asisten alih-alih satu respons. Interleaved thinking hanya didukung untuk [alat yang digunakan melalui Messages API](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview).

Untuk perbandingan yang dikerjakan yang menunjukkan apa yang diubah interleaved thinking dalam alur kerja dua alat, lihat [Bagaimana interleaved thinking mengubah alur](https://platform.claude.com/docs/id/build-with-claude/thinking-tool-workflows#how-interleaved-thinking-changes-the-flow).

### Preservasi blok thinking berdasarkan model

Apakah blok thinking dari turn asisten sebelumnya tetap dalam konteks secara default bergantung pada model:

* **Menyimpan semua turn sebelumnya:** Claude Opus 4.5 dan model Opus yang lebih baru, Claude Sonnet 4.6 dan model Sonnet yang lebih baru, Claude Fable 5, Claude Mythos 5, dan Claude Mythos Preview.
* **Menyimpan turn terakhir saja:** model Opus dan Sonnet sebelumnya, dan semua model Haiku hingga Claude Haiku 4.5. Ketika Anda mengirim kembali blok thinking yang lebih lama, API menghapusnya secara otomatis. Anda tidak perlu menghapusnya sendiri.

Preservasi membawa dua manfaat:

* **Optimasi cache:** blok thinking yang dipertahankan memungkinkan cache hit selama penggunaan alat, karena mereka dikirim kembali dengan hasil alat dan di-cache secara inkremental di seluruh turn asisten, menghasilkan penghematan token dalam alur kerja multistep.
* **Tidak ada dampak kecerdasan:** mempertahankan blok thinking tidak memiliki efek negatif pada performa model.

Trade-off-nya adalah penggunaan konteks: percakapan panjang mengonsumsi lebih banyak ruang konteks pada model keep-all, karena blok thinking yang dipertahankan dihitung sebagai input seperti riwayat percakapan lainnya (lihat [Thinking dan jendela konteks](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-and-the-context-window)). Perilaku ini otomatis di kedua rezim. Tidak diperlukan perubahan kode atau header beta, dan Anda harus tetap mengirim kembali blok thinking yang lengkap dan tidak dimodifikasi seperti yang dijelaskan dalam [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks). Untuk mengganti default di kedua arah, gunakan [penghapusan blok thinking](https://platform.claude.com/docs/id/build-with-claude/context-editing#thinking-block-clearing).

**Mengganti model di tengah percakapan.** Ketika Anda beralih antara dua model mana pun, misalnya setelah [fallback penolakan classifier](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback), hapus blok `thinking` dan `redacted_thinking` dari turn asisten sebelumnya. Blok thinking terikat pada model yang menghasilkannya. Model lain secara diam-diam mengabaikannya alih-alih menolak permintaan, tetapi blok yang diabaikan tetap menambah token input.

## Thinking dan caching prompt

[Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) berinteraksi dengan thinking dalam beberapa cara spesifik. Aturan berikut berlaku di kedua mode thinking.

**Perubahan konfigurasi membatalkan caching.** Konfigurasi thinking dan level [`effort`](https://platform.claude.com/docs/id/build-with-claude/effort) yang di-resolve dirender ke dalam prompt itu sendiri, sehingga mengubah salah satunya memulai prefix cache baru. Beralih antara `adaptive`, `enabled`, dan `disabled`, mengubah `budget_tokens`, dan mengubah nilai effort semuanya membatalkan breakpoint cache: breakpoint level pesan selalu miss, dan breakpoint alat serta prompt sistem juga dapat miss, tergantung di mana model merender konfigurasi. Perlakukan setiap perubahan thinking atau effort sebagai memulai cache dari awal. Permintaan berturut-turut yang mempertahankan konfigurasi yang sama mempertahankan cache, dan mengatur parameter secara eksplisit ke nilai defaultnya setara dengan menghilangkannya. Demonstrasi yang dikerjakan dengan output usage ada di halaman [Mengarahkan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#prompt-caching).

**Blok thinking di-cache dengan hasil alat.** Selama loop penggunaan alat, caching terjadi ketika Anda membuat permintaan lanjutan yang menyertakan hasil alat. Pada titik itu riwayat percakapan sebelumnya, termasuk blok thinking-nya, dapat di-cache, dan blok thinking yang di-cache tersebut dihitung sebagai token input dalam metrik usage Anda ketika dibaca dari cache. Ini terjadi secara otomatis, bahkan tanpa penanda `cache_control` eksplisit, dan berperilaku sama untuk thinking reguler dan interleaved. Trade-off-nya: blok thinking yang tidak pernah Anda lihat lagi dalam respons tetap berkontribusi pada penggunaan token input ketika dibaca dari cache.

**Apakah blok sebelumnya ada dalam konteks sama sekali bersifat per-model.** [Default preservasi](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-block-preservation-by-model) mengatur hal ini. Pada model keep-all, blok thinking dari turn sebelumnya tetap di-cache dan dalam konteks. Pada model last-turn-only, begitu Anda mengirim pesan pengguna yang bukan hasil alat, semua blok thinking sebelumnya dihapus dari konteks. Pada model tersebut, percakapan seperti ini:

```text wrap
User: ["What's the weather in Paris?"],
Assistant: [thinking_block_1] + [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [thinking_block_2] + [text block 2],
User: [Text response, cache=True]
```

diproses seolah-olah blok thinking tidak pernah ada:

```text wrap
User: ["What's the weather in Paris?"],
Assistant: [tool_use block 1],
User: [tool_result_1, cache=True],
Assistant: [text block 2],
User: [Text response, cache=True]
```

Pada model keep-all, permintaan yang sama menyimpan `thinking_block_1` dan `thinking_block_2` dalam konteks dan dalam cache.

**Degradasi menghapus thinking dari riwayat yang dapat di-cache.** Jika thinking menjadi nonaktif di tengah turn dan Anda mengirim konten thinking dalam turn penggunaan alat saat ini, konten thinking dihapus dan thinking tetap nonaktif untuk permintaan tersebut (lihat [degradasi yang baik](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-with-tool-use)). [Interleaved thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#interleaved-thinking) memperkuat efek pembatalan cache, karena blok thinking dapat terjadi di antara beberapa pemanggilan alat.

<Tip>
  Tugas yang berat thinking sering memakan waktu lebih lama dari masa hidup cache default 5 menit untuk diselesaikan. Pertimbangkan [durasi cache 1 jam](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration) untuk mempertahankan cache hit di seluruh sesi thinking yang lebih lama dan alur kerja multistep.
</Tip>

## Thinking dan jendela konteks

`max_tokens`, yang mencakup semua thinking yang dihasilkan Claude dalam turn saat ini, diberlakukan sebagai batas ketat. Pada model Claude 4.5 dan yang lebih baru, jika token input ditambah `max_tokens` melebihi ukuran jendela konteks, API menerima permintaan tersebut. Jika generasi kemudian mencapai batas jendela konteks, generasi berhenti dengan `stop_reason: "model_context_window_exceeded"` alih-alih mengembalikan error. Pada model sebelumnya, API mengembalikan error validasi sebagai gantinya. Lihat [Menangani stop reason](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons).

Bagaimana thinking dihitung terhadap jendela bergantung pada kapan thinking dihasilkan:

* **Thinking turn saat ini** selalu dihitung terhadap `max_tokens`, ditagih sebagai token output, dan menempati ruang jendela konteks untuk turn yang menghasilkannya.
* **Thinking turn sebelumnya** bergantung pada [default preservasi](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-block-preservation-by-model). Pada [model yang menyimpan semua turn sebelumnya](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-block-preservation-by-model), blok thinking sebelumnya tetap dalam konteks, dihitung terhadap jendela, dan ditagih sebagai token input seperti sisa riwayat percakapan. Pada model yang hanya menyimpan turn terakhir, API menghapus blok thinking yang lebih lama secara otomatis ketika Anda mengirimnya kembali, sehingga tidak mengonsumsi ruang jendela atau token input.

Dalam praktiknya:

* Pada model keep-all, anggarkan jendela konteks Anda seolah-olah thinking adalah riwayat percakapan biasa, karena memang demikian. Sesi agentic yang panjang mengakumulasi thinking dalam konteks. Gunakan [penghapusan blok thinking](https://platform.claude.com/docs/id/build-with-claude/context-editing#thinking-block-clearing) jika Anda perlu merebut kembali ruang.
* Pada model last-turn-only, thinking hanya merupakan biaya per-turn: thinking setiap turn dihitung terhadap `max_tokens` turn tersebut dan kemudian keluar dari jendela.

Diagram berikut mengilustrasikan rezim last-turn-only (penghapusan). Yang pertama menunjukkan percakapan multi-turn: blok thinking setiap turn dihasilkan dalam output tetapi tidak dibawa ke input turn berikutnya.

![Diagram thinking pada model yang menghapus blok thinking sebelumnya: blok thinking setiap turn dihasilkan dalam output dan tidak dibawa ke input turn berikutnya](https://platform.claude.com/docs/images/context-window-thinking.svg)

Yang kedua menunjukkan rezim yang sama dengan penggunaan alat: thinking tetap dalam konteks bersama hasil alatnya selama durasi turn asisten, lalu keluar pada turn pengguna berikutnya.

![Diagram thinking dengan penggunaan alat pada model yang menghapus blok thinking sebelumnya: thinking disimpan dengan hasil alatnya, lalu dihapus pada turn pengguna berikutnya](https://platform.claude.com/docs/images/context-window-thinking-tools.svg)

Gunakan [API penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) untuk mendapatkan hitungan akurat untuk kasus penggunaan spesifik Anda, terutama untuk percakapan multi-turn yang menyertakan thinking.

## Enkripsi thinking

Konten thinking penuh dienkripsi dan dikembalikan dalam field `signature` pada setiap blok thinking. API menggunakan signature untuk memverifikasi bahwa blok thinking dihasilkan oleh Claude ketika Anda mengirimnya kembali.

Perhatikan hal-hal berikut saat bekerja dengan signature:

* Hanya benar-benar diperlukan untuk mengirim kembali blok thinking ketika [menggunakan alat dengan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-with-tool-use). Jika tidak, Anda dapat menghilangkan blok thinking dari turn sebelumnya. Jika Anda mengirimnya kembali, apakah API menyimpan atau menghapusnya bergantung pada model (lihat [Preservasi blok thinking berdasarkan model](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-block-preservation-by-model)). Gunakan [context editing](https://platform.claude.com/docs/id/build-with-claude/context-editing) untuk mengonfigurasi ini.
* Saat mengirim kembali blok thinking, kirim semuanya persis seperti yang Anda terima, untuk konsistensi dan untuk menghindari potensi masalah.
* Saat [streaming respons](https://platform.claude.com/docs/id/build-with-claude/thinking#streaming-thinking), signature tiba sebagai `signature_delta` di dalam event `content_block_delta` tepat sebelum event `content_block_stop`.
* Nilai `signature` secara signifikan lebih panjang pada model Claude 4 dan yang lebih baru dibandingkan model sebelumnya.
* Field `signature` bersifat opaque: jangan menginterpretasikan atau mem-parse-nya.
* Nilai `signature` kompatibel lintas platform (Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), dan [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)). Nilai yang dihasilkan pada satu platform berfungsi pada platform lain.

## Blok redacted thinking

Selain blok `thinking` reguler, API dapat mengembalikan blok `redacted_thinking` ketika bagian dari penalaran Claude diredaksi karena alasan keamanan. Blok `redacted_thinking` berisi konten thinking terenkripsi dalam field `data`, tanpa teks yang dapat dibaca:

```json
{
  "type": "redacted_thinking",
  "data": "..."
}
```

Field `data` bersifat opaque dan terenkripsi. Seperti field `signature` pada blok thinking reguler, kirim kembali blok `redacted_thinking` ke API tanpa perubahan ketika melanjutkan percakapan multi-turn dengan [alat](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-with-tool-use).

<Tip>
  Jika kode Anda memfilter blok konten berdasarkan tipe (misalnya, `block.type == "thinking"`) saat melakukan round-trip respons dengan penggunaan alat, sertakan juga blok `redacted_thinking`. Memfilter hanya pada `block.type == "thinking"` secara diam-diam menghapus blok `redacted_thinking` dan merusak protokol multi-turn yang dijelaskan dalam [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).
</Tip>

<Note>
  Blok `redacted_thinking` adalah tipe blok konten yang berbeda yang dikembalikan ketika thinking diredaksi karena alasan keamanan. Ini terpisah dari opsi [`display: "omitted"`](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display), yang mengembalikan blok `thinking` reguler dengan field `thinking` kosong.
</Note>

## Output thinking pada Claude Fable 5 dan Claude Mythos 5

Pada Claude Fable 5 dan Claude Mythos 5, rantai pemikiran mentah tidak pernah dikembalikan. Blok yang Anda terima adalah blok `thinking` reguler, bukan `redacted_thinking`, dan [pengaturan `display`](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display) bekerja sama seperti pada model lain (teks [yang diringkas](https://platform.claude.com/docs/id/build-with-claude/thinking#summarized-thinking), atau field `thinking` kosong ketika omitted, yang merupakan default di sini). Untuk bentuk respons blok thinking, lihat [referensi Messages API](https://platform.claude.com/docs/id/api/messages/create).

Saat melanjutkan percakapan pada model yang sama, kirim kembali setiap blok thinking ke API persis seperti yang diterima, termasuk blok yang field `thinking`-nya kosong. Jangan mengedit atau merekonstruksinya. Membaca teks ringkasan untuk ditampilkan tidak masalah: API menolak blok yang konten yang dikembalikannya telah dimodifikasi, bukan blok yang telah Anda baca. Teks yang ditempatkan di field `thinking` omitted yang kosong [diabaikan alih-alih ditolak](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).

Untuk bagaimana blok thinking ditangani ketika Anda mengganti model di tengah percakapan, lihat [Preservasi blok thinking berdasarkan model](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-block-preservation-by-model).

Dua pengecualian, dibahas dalam [Fallback credit](https://platform.claude.com/docs/id/build-with-claude/fallback-credit):

* Retry fallback-credit harus mengirim kembali body permintaan yang ditolak tanpa perubahan.
* Blok `fallback` dari fallback mid-output tetap di tempat mereka muncul.

Untuk mendapatkan visibilitas ke dalam penalaran model, baca blok `thinking` yang dijelaskan di halaman ini alih-alih meminta penalaran dalam teks respons. Pada Claude Fable 5, permintaan yang mencoba memunculkan penalaran internal model sebagai bagian dari teks respons dapat ditolak dengan `stop_details.category: "reasoning_extraction"`. Lihat [Kategori penolakan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk referensi field dan panduan penanganan.

## Batasan dan kompatibilitas fitur

**Parameter sampling.** Pada Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, dan Claude Sonnet 5, nilai `temperature`, `top_p`, atau `top_k` yang bukan default akan mengembalikan error 400 pada setiap permintaan, terlepas dari apakah thinking digunakan atau tidak. Pada model yang lebih lama, pembatasan ini hanya berlaku saat thinking aktif: `temperature` dan `top_k` tidak kompatibel dengan thinking, dan `top_p` diizinkan pada nilai antara 0,95 dan 1.

**Prefill respons dan penggunaan alat yang dipaksa.** Anda tidak dapat melakukan pre-fill pada respons asisten saat thinking aktif. Penggunaan alat yang dipaksa (`tool_choice: {"type": "any"}` atau `{"type": "tool", ...}`) tidak kompatibel dengan pemikiran diperpanjang manual tetapi berfungsi dengan adaptive thinking. Lihat [Thinking dengan penggunaan alat](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-with-tool-use).

**Batas output.** Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5, Claude Opus 4.6, dan Claude Sonnet 4.6 mendukung hingga 128k token output per permintaan. Claude Haiku 4.5, Claude Sonnet 4.5, dan Claude Opus 4.5 mendukung hingga 64k. Pada [Message Batches API](https://platform.claude.com/docs/id/build-with-claude/batch-processing#extended-output-beta), [beta header](https://platform.claude.com/docs/id/api/beta-headers) `output-300k-2026-03-24` menaikkan batas menjadi 300k untuk Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5, Claude Opus 4.6, dan Claude Sonnet 4.6. Lihat [ikhtisar model](https://platform.claude.com/docs/id/about-claude/models/overview) untuk batasan pada model lama.

**Permintaan panjang.** SDK mewajibkan streaming ketika `max_tokens` lebih besar dari 21.333, untuk menghindari timeout HTTP pada permintaan yang berjalan lama. Ini adalah validasi sisi klien, bukan pembatasan API. Jika Anda tidak perlu memproses event secara inkremental, gunakan `.stream()` dengan `.get_final_message()` (Python) atau `.finalMessage()` (TypeScript) untuk mendapatkan objek `Message` lengkap tanpa menangani event satu per satu. Lihat [Streaming Messages](https://platform.claude.com/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events). Perkirakan waktu respons yang lebih lama saat thinking aktif, karena menghasilkan blok thinking menambah waktu pemrosesan. Untuk beban kerja yang mendorong thinking melebihi sekitar 32k token per permintaan, gunakan [batch processing](https://platform.claude.com/docs/id/build-with-claude/batch-processing) untuk menghindari masalah jaringan: permintaan semacam itu dapat berjalan cukup lama hingga mencapai timeout sistem dan batas koneksi terbuka.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mengarahkan thinking" icon="compass" href="https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost">
    Arahkan seberapa sering dan seberapa dalam Claude berpikir dengan tingkat effort, panduan prompt sistem, dan pengarahan per pesan, serta pahami biaya dan harga thinking.
  </Card>

  <Card title="Thinking dalam alur kerja alat dan multi-turn" icon="wrench" href="https://platform.claude.com/docs/id/build-with-claude/thinking-tool-workflows">
    Pelajari siklus lengkap penggunaan alat dua turn yang mempertahankan blok thinking dengan benar, dan lihat bagaimana interleaved thinking mengubah alurnya.
  </Card>

  <Card title="Pemecahan masalah thinking" icon="hammer" href="https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting">
    Diagnosis dan perbaiki kegagalan thinking yang paling umum: error 400 konfigurasi, blok thinking yang kosong atau hilang, penghentian max\_tokens, dan cache miss.
  </Card>

  <Card title="Effort" icon="sliders" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kontrol berapa banyak token yang digunakan Claude saat merespons dengan parameter effort, menyeimbangkan antara kelengkapan respons dan efisiensi token.
  </Card>
</CardGroup>
