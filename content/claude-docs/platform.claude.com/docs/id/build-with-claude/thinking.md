---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/thinking
fetched_at: 2026-07-25T03:07:29.726338Z
sha256: 6afc594fbdfbd00122787429b1930ae7833eebdad5671089973f186fa5fd7258
---

# Pemikiran

Pahami cara kerja pemikiran Claude: mengaktifkannya, membaca output pemikiran, mengarahkan kedalaman pemikiran dengan effort, dan menggunakan pemikiran dengan alat, caching, dan streaming.

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

Model yang menjawab dalam satu langkah harus melakukan semuanya dengan benar pada percobaan pertama: tanpa coretan kerja, tanpa pemeriksaan, tanpa mengubah arah di tengah jalan. Untuk sebuah pembuktian, bug yang rumit, atau tugas agentik yang panjang, pendekatan pertama sering kali bukan yang terbaik.

Pemikiran menghilangkan batasan itu. Ketika pemikiran aktif, Claude mengerjakan masalah dengan kata-katanya sendiri sebelum menjawab: ia menyatakan ulang apa yang ditanyakan, mencoba berbagai pendekatan, memeriksa hasil antara, dan meninggalkan jalur yang tidak berhasil. Penalaran itu tiba dalam blok konten `thinking` sebelum respons, dan Claude memanfaatkannya untuk menghasilkan jawaban akhir. Inilah mengapa pemikiran meningkatkan kinerja pada tugas-tugas kompleks seperti matematika, pemrograman, analisis, dan pekerjaan agentik yang berjalan lama, di mana kualitas jawaban bergantung pada pekerjaan antara yang jika tidak ada akan dipadatkan ke dalam respons itu sendiri atau dilewati.

Pemikiran memiliki biaya: token yang dihabiskan Claude untuk bernalar ditagih sebagai token output, bahkan ketika teks pemikiran tidak dikembalikan kepada Anda, dan token tersebut dihitung terhadap `max_tokens` bersama dengan teks respons. Halaman ini membahas bagaimana pemikiran berperilaku di seluruh permukaan API: mengaktifkannya, membaca outputnya, dan mengelola interaksinya dengan alat, streaming, caching, dan jendela konteks.

## Cara kerja pemikiran

![Diagram cara kerja pemikiran (thinking): Claude mengevaluasi permintaan dan memutuskan apakah akan berpikir; dengan penggunaan alat (tool use), pemikiran dapat berulang di antara panggilan alat; satu respons mengembalikan blok thinking, lalu blok teks](/docs/images/how-thinking-works.svg)

Apakah Claude berpikir pada permintaan tertentu, dan seberapa dalam, bergantung pada konfigurasi pemikiran Anda dan kompleksitas permintaan.

Berikut adalah tampilan pemikiran dalam sebuah respons: satu atau lebih blok konten `thinking` tiba sebelum blok `text`. Blok thinking tetap merupakan konten yang dihasilkan, seperti blok `text` yang mengikutinya, tetapi dipisahkan dari respons kanonis. Setiap blok thinking juga membawa bidang `signature`, salinan terenkripsi dari penalaran lengkap yang Anda kirimkan kembali tanpa perubahan dalam percakapan multi-giliran dan penggunaan alat (lihat [Enkripsi pemikiran](#thinking-encryption)):

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

Anda tidak selalu melihat teks ini, dan apa yang Anda lihat tidak pernah merupakan rantai pemikiran mentah: teks dalam blok thinking adalah [ringkasan dari penalaran Claude](#summarized-thinking). Bidang `display` pada konfigurasi pemikiran mengontrol apakah ringkasan itu dikembalikan sama sekali: `"summarized"` mengembalikannya, sementara `"omitted"`, default pada model terbaru, mengembalikan blok thinking dengan bidang `thinking` kosong. Apa pun pilihannya, blok tersebut ditagih dengan cara yang sama dan dikirimkan kembali dengan cara yang sama dalam percakapan multi-giliran; lihat [Mengontrol tampilan pemikiran](#controlling-thinking-display) untuk default per-model dan detailnya.

Jika Claude menggunakan alat, pemikiran juga dapat muncul di antara panggilan alat; lihat [Pemikiran dengan penggunaan alat](#thinking-with-tool-use). Untuk format respons lengkap, lihat [referensi Messages API](/docs/id/api/messages/create).

## Mengonfigurasi pemikiran

Pada model saat ini, pemikiran aktif secara default atau hanya berjarak satu parameter. Konfigurasi mana yang diterima setiap model, dan apa defaultnya, tercantum dalam [tabel konfigurasi per-model](/docs/id/build-with-claude/thinking-troubleshooting#supported-models) di halaman Pemecahan Masalah.

Pada Claude Opus 5, Claude Sonnet 5, Claude Fable 5, Claude Mythos 5, dan Claude Mythos Preview, pemikiran sudah aktif: tidak perlu konfigurasi. Hal pertama yang dibutuhkan sebagian besar pengembang pada model-model ini adalah melihat teks pemikiran, karena `display` default ke `"omitted"` di sana. Aktifkan dengan `thinking: {"type": "adaptive", "display": "summarized"}`, yang persis sama dengan permintaan berikut dengan string model yang diganti.

Pada Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, dan Claude Sonnet 4.6, pemikiran nonaktif sampai Anda menyetel `thinking: {type: "adaptive"}` dalam permintaan Anda. Contoh berikut melakukan hal itu, menyetel `display: "summarized"` agar teks pemikiran terlihat, dan menggunakan `max_tokens` yang lapang:

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

Menjalankan contoh tersebut mencetak pemikiran yang diringkas, lalu jawabannya:

```text Output wrap
Thinking: Use Euclidean algorithm.
1071 = 2*462 + 147
462 = 3*147 + 21
147 = 7*21 + 0
GCD = 21

Response: ## Finding GCD of 1071 and 462

I'll use the **Euclidean algorithm**, repeatedly dividing and taking remainders...
```

Token pemikiran dihitung terhadap `max_tokens`, jadi setel cukup tinggi untuk menyisakan ruang bagi pemikiran dan teks respons. Lihat [Kontrol biaya](/docs/id/build-with-claude/thinking-steering-and-cost#cost-control) di halaman pengarahan dan [Pemikiran dan jendela konteks](#thinking-and-the-context-window).

### Menonaktifkan pemikiran

Pada Claude Sonnet 5, di mana pemikiran aktif secara default, Anda dapat menonaktifkannya:

```python
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=4096,
    thinking={"type": "disabled"},
    messages=[{"role": "user", "content": "Summarize this article in one sentence."}],
)
```

Claude Opus 5 juga memiliki pemikiran yang aktif secara default dan menerima `thinking: {type: "disabled"}` pada [effort](/docs/id/build-with-claude/effort) `high` atau di bawahnya. Pada effort `xhigh` atau `max`, pemikiran tidak dapat dinonaktifkan: permintaan yang menggabungkan `thinking: {type: "disabled"}` dengan level effort tersebut mengembalikan error 400. Pembatasan ini berlaku untuk Claude Opus 5 dan model yang lebih baru dan diberlakukan pada setiap permintaan. Dengan pemikiran dinonaktifkan, Claude Opus 5 terkadang dapat mengeluarkan panggilan alat sebagai teks biasa atau menyertakan tag XML internal dalam output yang terlihat; lihat [Menjalankan dengan pemikiran dinonaktifkan](/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk mitigasi melalui prompting.

Claude Fable 5, Claude Mythos 5, dan Claude Mythos Preview menolak `thinking: {type: "disabled"}`: pemikiran tidak dapat dinonaktifkan pada model-model ini.

Jika model Anda hanya mendukung extended thinking (pemikiran diperpanjang) (lihat [tabel konfigurasi per-model](/docs/id/build-with-claude/thinking-troubleshooting#supported-models)), konfigurasikan dengan `type: "enabled"` dan nilai `budget_tokens` sebagai gantinya; halaman [Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking) membahas konfigurasi tersebut. Dan jika ada konfigurasi pemikiran yang mengembalikan error 400, [Pemecahan masalah pemikiran](/docs/id/build-with-claude/thinking-troubleshooting) mencocokkan setiap pesan error dengan perbaikannya.

## Membaca output pemikiran

### Mengontrol tampilan pemikiran

Bidang `display` pada konfigurasi pemikiran mengontrol bagaimana konten pemikiran dikembalikan dalam respons API. `display` bekerja di kedua mode: setel bersama `type: "adaptive"` atau `type: "enabled"`. Bidang ini menerima dua nilai:

* `"summarized"`: blok thinking berisi teks [pemikiran yang diringkas](#summarized-thinking), ringkasan yang dapat dibaca dari penalaran Claude. Ini adalah default pada Claude Opus 4.6, Claude Sonnet 4.6, dan model yang lebih lama.
* `"omitted"`: blok thinking dikembalikan dengan bidang `thinking` kosong. Bidang `signature` tetap membawa pemikiran lengkap yang terenkripsi untuk kontinuitas multi-giliran (lihat [Enkripsi pemikiran](#thinking-encryption)). Ini adalah default pada Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Sonnet 5, Claude Opus 4.8, Claude Opus 4.7, dan [Claude Mythos Preview](https://anthropic.com/glasswing).

Setel `display: "omitted"` ketika aplikasi Anda tidak menampilkan konten pemikiran kepada pengguna. Manfaat utamanya adalah **waktu-ke-token-teks-pertama yang lebih cepat saat streaming**: server melewati streaming token pemikiran sepenuhnya dan hanya mengirimkan signature, sehingga respons teks akhir mulai di-streaming lebih cepat.

Dengan `display: "omitted"`, respons berisi blok `thinking` dengan bidang `thinking` kosong:

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

Perhatikan hal-hal berikut saat bekerja dengan pemikiran yang dihilangkan:

* Anda tetap dikenakan biaya untuk token pemikiran penuh. Menghilangkan mengurangi latensi, bukan biaya.
* Jika Anda mengirimkan kembali blok thinking dalam percakapan multi-giliran, kirimkan tanpa perubahan. Server mendekripsi `signature` untuk merekonstruksi pemikiran asli untuk konstruksi prompt (lihat [Mempertahankan blok thinking](#preserving-thinking-blocks)). Teks apa pun yang Anda tempatkan di bidang `thinking` dari blok yang dihilangkan yang dikirim bolak-balik akan diabaikan.
* `display` tidak valid dengan `thinking.type: "disabled"` (tidak ada yang perlu ditampilkan).
* Saat menggunakan `thinking.type: "adaptive"` dan model melewati pemikiran untuk permintaan sederhana, tidak ada blok thinking yang dihasilkan terlepas dari `display`.
* Saat streaming dengan `display: "omitted"`, tidak ada event `thinking_delta` yang dikeluarkan; lihat [Streaming pemikiran](#streaming-thinking) untuk urutan event.

<Note>
  Bidang `signature` identik baik `display` bernilai `"summarized"` maupun `"omitted"`. Mengganti nilai `display` di antara giliran dalam sebuah percakapan didukung.
</Note>

Dalam SDK Ruby, setel bidang ini sebagai `display_:` (dengan garis bawah di akhir) untuk menghindari penimpaan `Kernel#display` milik Ruby; bidang pada wire tetap `display`.

### Pemikiran yang diringkas

Ketika `display` bernilai `"summarized"`, teks pemikiran yang Anda terima adalah ringkasan dari proses pemikiran lengkap Claude, bukan rantai pemikiran mentah. Pemikiran yang diringkas memberikan manfaat kecerdasan penuh dari pemikiran sambil mencegah penyalahgunaan. Tidak ada pengaturan `display` yang mengembalikan rantai pemikiran mentah.

Perhatikan hal-hal berikut saat bekerja dengan pemikiran yang diringkas:

* Anda dikenakan biaya untuk token pemikiran penuh yang dihasilkan oleh permintaan asli, bukan token ringkasan. Jumlah token output yang ditagih **tidak cocok** dengan jumlah token yang Anda lihat dalam respons.
* Pada Claude Opus 4.6, Claude Sonnet 4.6, dan model yang lebih lama, beberapa baris pertama output pemikiran lebih rinci, memberikan penalaran terperinci yang sangat membantu untuk keperluan rekayasa prompt. [Claude Mythos Preview](https://anthropic.com/glasswing) meringkas dari token pertama, sehingga blok thinking-nya tidak menampilkan pembukaan yang rinci ini.
* Peringkasan mempertahankan ide-ide kunci dari proses pemikiran Claude dengan latensi tambahan minimal, memungkinkan pengalaman pengguna yang dapat di-streaming.
* Peringkasan diproses oleh model yang berbeda dari yang Anda targetkan dalam permintaan Anda. Model pemikiran tidak melihat output yang diringkas.
* Karena Anthropic berupaya meningkatkan fitur pemikiran, perilaku peringkasan dapat berubah.

<Note>
  Dalam kasus langka di mana Anda memerlukan akses ke output pemikiran lengkap, [hubungi tim penjualan Anthropic](mailto:sales@anthropic.com).
</Note>

### Streaming pemikiran

Pemikiran bekerja dengan [streaming](/docs/id/build-with-claude/streaming). Blok thinking di-streaming sebagai event `thinking_delta` di dalam event `content_block_delta`, diikuti oleh satu event `signature_delta` tepat sebelum `content_block_stop` milik blok tersebut. Blok teks di-streaming setelahnya seperti biasa.

![Diagram urutan event streaming dengan pemikiran (thinking): blok thinking terbuka, delta thinking di-streaming hanya ketika display bernilai summarized, satu delta signature menutup blok, lalu delta teks di-streaming](/docs/images/how-thinking-streams.svg)

Contoh berikut melakukan streaming respons dengan pemikiran adaptif, mencetak delta pemikiran dan teks saat tiba:

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

Ketika `display: "omitted"` disetel, blok thinking terbuka, satu `signature_delta` tiba, dan blok ditutup tanpa event `thinking_delta` apa pun. Streaming teks dimulai segera setelahnya:

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
  Saat menggunakan streaming dengan pemikiran diaktifkan, Anda mungkin memperhatikan bahwa teks terkadang tiba dalam potongan yang lebih besar bergantian dengan pengiriman token-per-token yang lebih kecil. Ini adalah perilaku yang diharapkan, terutama untuk konten pemikiran.

  Sistem streaming perlu memproses konten dalam batch untuk kinerja optimal, yang dapat menghasilkan pola pengiriman "berpotongan" ini, dengan kemungkinan penundaan di antara event streaming.
</Note>

Untuk mekanisme streaming umum, lihat [Streaming Messages](/docs/id/build-with-claude/streaming).

## Pemikiran dan effort

Parameter `thinking` mengontrol apakah Claude berpikir dalam [blok pemikiran](/docs/id/build-with-claude/thinking) sebelum menjawab; parameter `effort` mengontrol seberapa banyak upaya yang Claude curahkan untuk keseluruhan respons, yang dalam mode adaptif mencakup seberapa sering dan seberapa dalam Claude berpikir. Jangan meneruskan `adaptive` sebagai nilai `effort`: `adaptive` adalah mode berpikir, bukan tingkat effort.

Untuk apa yang dilakukan setiap level effort terhadap perilaku pemikiran, lihat [tabel perilaku pemikiran per-level](/docs/id/build-with-claude/thinking-steering-and-cost#effort-levels) di halaman [Mengarahkan pemikiran](/docs/id/build-with-claude/thinking-steering-and-cost); halaman [Effort](/docs/id/build-with-claude/effort) mendokumentasikan parameter itu sendiri, termasuk level mana yang didukung setiap model. Pada Claude Opus 4.5, satu-satunya model khusus extended-thinking yang mendukung effort, effort berkomposisi dengan `budget_tokens`; lihat [Aturan dan penyetelan budget](/docs/id/build-with-claude/extended-thinking#budget-rules-and-tuning).

Dengan kedua kontrol dipisahkan seperti ini, pilih yang sesuai dengan tujuan Anda:

* **Biaya atau latensi lebih rendah pada beban kerja dengan pemikiran aktif:** turunkan `effort` terlebih dahulu. Ini menskalakan seluruh respons ke bawah, termasuk pemikiran.
* **Claude terlalu jarang atau terlalu dangkal berpikir:** naikkan `effort`, atau lihat [Mengarahkan seberapa sering Claude berpikir](/docs/id/build-with-claude/thinking-steering-and-cost#tuning-thinking-behavior) di halaman pengarahan.
* **Anda perlu pemikiran sepenuhnya nonaktif:** gunakan `thinking: {type: "disabled"}` pada model yang mengizinkannya (lihat [tabel konfigurasi per-model](/docs/id/build-with-claude/thinking-troubleshooting#supported-models)).
* **Anda memerlukan batas atas yang ketat pada pengeluaran:** gunakan `max_tokens`. Effort adalah panduan lunak; `max_tokens` adalah batas ketat.

## Pemikiran dengan penggunaan alat

Pemikiran bekerja bersama [penggunaan alat](/docs/id/agents-and-tools/tool-use/overview), memungkinkan Claude bernalar melalui pemilihan alat dan memproses hasil alat. Dua batasan berlaku:

1. **Batasan pilihan alat (mode manual)**: penggunaan alat dengan extended thinking manual (`thinking: {type: "enabled"}`) hanya mendukung `tool_choice: {"type": "auto"}` (default) atau `tool_choice: {"type": "none"}`. Menggunakan `tool_choice: {"type": "any"}` atau `tool_choice: {"type": "tool", "name": "..."}` menghasilkan error karena opsi-opsi ini memaksa penggunaan alat, yang tidak kompatibel dengan extended thinking manual. Pemikiran adaptif, termasuk pada model di mana pemikiran aktif secara default, mendukung penggunaan alat yang dipaksa.
2. **Mempertahankan blok thinking**: ketika Anda mengembalikan hasil alat, Anda harus mengirimkan blok thinking dari pesan assistant kembali ke API, lengkap dan tanpa modifikasi. Lihat [Mempertahankan blok thinking](#preserving-thinking-blocks).

**Satu loop penggunaan alat adalah satu giliran assistant.** Dari perspektif model, giliran assistant tidak selesai sampai Claude menyelesaikan respons lengkapnya, yang mungkin mencakup beberapa panggilan alat dan hasilnya. Seluruh urutan ini adalah satu giliran assistant:

```text wrap
User: "What's the weather in Paris?"
Assistant: [thinking] + [tool_use: get_weather]
User: [tool_result: "20°C, sunny"]
Assistant: [text: "The weather in Paris is 20°C and sunny"]
```

Seluruh giliran berjalan dalam satu mode pemikiran: Anda tidak dapat mengubah pemikiran di tengah giliran, termasuk selama loop penggunaan alat. Dalam mode extended (manual), API juga memberlakukan bahwa giliran assistant terakhir dari permintaan dengan pemikiran aktif dimulai dengan blok thinking. Mode adaptif melonggarkan ini: tidak ada giliran assistant yang perlu dimulai dengan blok thinking.

**Konflik di tengah giliran terdegradasi dengan anggun.** Jika Anda mengubah pemikiran di tengah giliran (misalnya, antara mengirim panggilan alat dan mengembalikan hasilnya), API tidak mengeluarkan error. Sebaliknya, API secara diam-diam menonaktifkan pemikiran untuk permintaan tersebut. Untuk menjaga kualitas model, API dapat menghapus blok thinking yang akan menciptakan struktur giliran yang tidak valid, atau menonaktifkan pemikiran ketika riwayat percakapan tidak kompatibel dengan pemikiran yang diaktifkan. Untuk mengonfirmasi apakah pemikiran aktif, periksa keberadaan blok `thinking` dalam respons.

**Ubah di antara giliran, bukan di dalamnya.** Rencanakan strategi pemikiran Anda di awal setiap giliran. Selesaikan giliran assistant, lalu ubah konfigurasi pemikiran untuk giliran berikutnya:

```text wrap
User: "What's the weather?"
Assistant: [tool_use] (thinking disabled)
User: [tool_result]
Assistant: [text: "It's sunny"]
User: "What about tomorrow?"
Assistant: [thinking] + [text: "..."] (thinking enabled - new turn)
```

Perhatikan bahwa mengubah mode pemikiran juga membatalkan caching prompt; lihat [Pemikiran dan caching prompt](#thinking-and-prompt-caching).

### Mempertahankan blok thinking

Ketika Claude memanggil alat, ia menjeda konstruksi responsnya untuk menunggu informasi eksternal. Ketika Anda mengembalikan hasil alat, Claude melanjutkan membangun respons yang sama, sehingga penalaran sebelumnya harus tetap ada. Kirimkan setiap blok `thinking` kembali ke API lengkap dan tanpa modifikasi, bersama blok `tool_use` yang menyertainya. Ini penting karena dua alasan:

1. **Kontinuitas penalaran**: blok thinking menangkap penalaran langkah demi langkah yang mengarah pada permintaan alat. Menyertakannya memungkinkan Claude melanjutkan penalaran dari tempat ia berhenti.
2. **Pemeliharaan konteks**: hasil alat muncul sebagai pesan user dalam struktur API, tetapi mereka adalah bagian dari satu alur penalaran yang berkelanjutan. Mempertahankan blok thinking menjaga alur tersebut di seluruh panggilan API.

Singkatnya:

* **Wajib:** dalam giliran penggunaan alat, kirimkan blok thinking kembali.
* **Disarankan:** di seluruh giliran, kirimkan semuanya kembali.
* **Diizinkan:** di luar penggunaan alat, hilangkan pemikiran dari giliran sebelumnya.

Anda tidak perlu memangkas pemikiran lama sendiri. Kirimkan semua blok thinking kembali dalam percakapan multi-giliran, dan API secara otomatis memfilternya, menyimpan blok yang diperlukan untuk mempertahankan penalaran model, dan menagih token input hanya untuk blok yang benar-benar ditampilkan kepada Claude. Blok giliran sebelumnya mana yang disimpan bersifat per-model; lihat [Pemertahanan blok thinking per model](#thinking-block-preservation-by-model). Untuk mengganti default, gunakan [strategi context-editing `clear_thinking_20251015`](/docs/id/build-with-claude/context-editing#thinking-block-clearing).

Dalam pesan assistant terbaru, urutan blok `thinking` yang berurutan harus cocok dengan apa yang dihasilkan model dalam permintaan asli: Anda tidak dapat menyusun ulang, mengedit, atau menghapus sebagian. Ini termasuk [blok `redacted_thinking`](#redacted-thinking-blocks).

<Note>
  Blok thinking yang dimodifikasi ditolak dengan error 400; lihat [Error 400 mengatakan blok thinking tidak dapat dimodifikasi](/docs/id/build-with-claude/thinking-troubleshooting#error-thinking-blocks-modified) untuk pesan persisnya, penyebab umum, dan perbaikannya. Satu pengecualian: teks yang ditempatkan di bidang `thinking` kosong dari blok yang [dihilangkan](#controlling-thinking-display) diabaikan alih-alih ditolak.
</Note>

Untuk panduan lengkap dua giliran dengan kode di setiap SDK, lihat [Pemikiran dalam alur kerja alat dan multi-giliran](/docs/id/build-with-claude/thinking-tool-workflows#two-turn-tool-use-round-trip). Panduan tersebut mendefinisikan alat, menerima respons pemikiran-plus-penggunaan-alat, dan mengirimkan kembali giliran assistant dengan hasil alat.

### Pemikiran berselang

Pemikiran berselang (interleaved thinking) memungkinkan Claude berpikir di antara panggilan alat, bernalar tentang setiap hasil alat sebelum bertindak berdasarkan hasil tersebut. Dengan pemikiran berselang, Claude dapat:

* Bernalar tentang hasil panggilan alat sebelum memutuskan apa yang harus dilakukan selanjutnya
* Merangkai beberapa panggilan alat dengan langkah penalaran di antaranya
* Membuat keputusan yang lebih bernuansa berdasarkan hasil antara

<Note>
  Panggilan alat berurutan tidak memerlukan pemikiran berselang. Claude dapat merangkai panggilan alat dengan atau tanpa pemikiran berselang; penyelangan mengubah di mana blok thinking muncul di antara panggilan alat, bukan apakah panggilan alat dapat dirangkai.
</Note>

Dengan pemikiran adaptif, pemikiran berselang otomatis pada setiap model yang mendukung pemikiran adaptif; tidak diperlukan header beta. Pada Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5, Claude Opus 4.8, dan Claude Opus 4.7, penalaran di antara panggilan alat selalu muncul dalam blok thinking. Claude Haiku 4.5 tidak mendukung pemikiran berselang. Pada model yang menggunakan extended thinking manual, penyelangan memerlukan header beta dan mengubah cara budget pemikiran dihitung; [Pemikiran berselang dalam mode manual](/docs/id/build-with-claude/extended-thinking#interleaved-thinking) membahas aturan per-model dan perilaku header khusus platform.

Dengan pemikiran berselang, alokasi pemikiran dapat mencakup seluruh giliran assistant alih-alih satu respons. Pemikiran berselang hanya didukung untuk [alat yang digunakan melalui Messages API](/docs/id/agents-and-tools/tool-use/overview).

Untuk perbandingan terperinci yang menunjukkan apa yang diubah pemikiran berselang dalam alur kerja dua alat, lihat [Bagaimana pemikiran berselang mengubah alur](/docs/id/build-with-claude/thinking-tool-workflows#how-interleaved-thinking-changes-the-flow).

### Pemertahanan blok thinking per model

Apakah blok thinking dari giliran assistant sebelumnya tetap berada dalam konteks secara default bergantung pada model:

* **Simpan semua giliran sebelumnya:** Claude Opus 4.5 dan model Opus yang lebih baru, Claude Sonnet 4.6 dan model Sonnet yang lebih baru, Claude Fable 5, Claude Mythos 5, dan Claude Mythos Preview.
* **Simpan hanya giliran terakhir:** model Opus dan Sonnet yang lebih lama, dan semua model Haiku hingga Claude Haiku 4.5. Ketika Anda mengirimkan kembali blok thinking yang lebih lama, API menghapusnya secara otomatis; Anda tidak perlu menghapusnya sendiri.

Pemertahanan membawa dua manfaat:

* **Optimasi cache**: blok thinking yang dipertahankan memungkinkan cache hit selama penggunaan alat, karena blok tersebut dikirimkan kembali dengan hasil alat dan di-cache secara bertahap di seluruh giliran assistant, menghasilkan penghematan token dalam alur kerja multi-langkah.
* **Tidak ada dampak kecerdasan**: mempertahankan blok thinking tidak memiliki efek negatif pada kinerja model.

Kompromi yang ada adalah penggunaan konteks: percakapan panjang mengonsumsi lebih banyak ruang konteks pada model simpan-semua, karena blok thinking yang dipertahankan dihitung sebagai input seperti riwayat percakapan lainnya (lihat [Pemikiran dan jendela konteks](#thinking-and-the-context-window)). Perilaku ini otomatis di kedua rezim; tidak diperlukan perubahan kode atau header beta, dan Anda harus tetap mengirimkan blok thinking yang lengkap dan tidak dimodifikasi kembali seperti dijelaskan dalam [Mempertahankan blok thinking](#preserving-thinking-blocks). Untuk mengganti default ke arah mana pun, gunakan [penghapusan blok thinking](/docs/id/build-with-claude/context-editing#thinking-block-clearing).

**Mengganti model di tengah percakapan.** Ketika Anda beralih di antara dua model mana pun, misalnya setelah [fallback penolakan classifier](/docs/id/build-with-claude/refusals-and-fallback), hapus blok `thinking` dan `redacted_thinking` dari giliran assistant sebelumnya. Blok thinking terikat pada model yang menghasilkannya. Model lain secara diam-diam mengabaikannya alih-alih menolak permintaan, tetapi blok yang diabaikan tetap menambah token input.

## Pemikiran dan caching prompt

[Prompt caching](/docs/id/build-with-claude/prompt-caching) (caching prompt) berinteraksi dengan pemikiran dalam beberapa cara spesifik. Aturan berikut berlaku di kedua mode pemikiran.

**Perubahan konfigurasi membatalkan caching.** Konfigurasi pemikiran dan level [`effort`](/docs/id/build-with-claude/effort) yang diselesaikan dirender ke dalam prompt itu sendiri, sehingga mengubah salah satunya memulai prefiks cache baru. Beralih antara `adaptive`, `enabled`, dan `disabled`, mengubah `budget_tokens`, dan mengubah nilai effort semuanya membatalkan breakpoint cache: breakpoint level pesan selalu meleset, dan breakpoint alat dan prompt sistem juga dapat meleset, tergantung di mana model merender konfigurasi. Perlakukan setiap perubahan pemikiran atau effort sebagai memulai cache dari awal. Permintaan berurutan yang mempertahankan konfigurasi yang sama mempertahankan cache, dan menyetel parameter secara eksplisit ke nilai defaultnya setara dengan menghilangkannya. Demonstrasi terperinci dengan output penggunaan ada di halaman [Mengarahkan pemikiran](/docs/id/build-with-claude/thinking-steering-and-cost#prompt-caching).

**Blok thinking di-cache dengan hasil alat.** Selama loop penggunaan alat, caching terjadi ketika Anda membuat permintaan lanjutan yang menyertakan hasil alat. Pada saat itu riwayat percakapan sebelumnya, termasuk blok thinking-nya, dapat di-cache, dan blok thinking yang di-cache tersebut dihitung sebagai token input dalam metrik penggunaan Anda ketika dibaca dari cache. Ini terjadi secara otomatis, bahkan tanpa penanda `cache_control` eksplisit, dan berperilaku sama untuk pemikiran reguler dan berselang. Kompromi yang ada: blok thinking yang tidak pernah Anda lihat lagi dalam respons tetap berkontribusi pada penggunaan token input ketika dibaca dari cache.

**Apakah blok sebelumnya ada dalam konteks sama sekali bersifat per-model.** [Default pemertahanan](#thinking-block-preservation-by-model) mengatur ini. Pada model simpan-semua, blok thinking giliran sebelumnya tetap di-cache dan dalam konteks. Pada model hanya-giliran-terakhir, begitu Anda mengirim pesan user yang bukan hasil alat, semua blok thinking sebelumnya dihapus dari konteks. Pada model tersebut, percakapan seperti ini:

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

Pada model simpan-semua, permintaan yang sama mempertahankan `thinking_block_1` dan `thinking_block_2` dalam konteks dan dalam cache.

**Degradasi menghapus pemikiran dari riwayat yang dapat di-cache.** Jika pemikiran menjadi nonaktif di tengah giliran dan Anda mengirimkan konten pemikiran dalam giliran penggunaan alat saat ini, konten pemikiran dihapus dan pemikiran tetap nonaktif untuk permintaan tersebut (lihat [degradasi anggun](#thinking-with-tool-use)). [Pemikiran berselang](#interleaved-thinking) memperkuat efek pembatalan cache, karena blok thinking dapat terjadi di antara beberapa panggilan alat.

<Tip>
  Tugas yang berat pemikiran sering kali membutuhkan waktu lebih lama dari masa hidup cache default 5 menit untuk diselesaikan. Pertimbangkan [durasi cache 1 jam](/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration) untuk mempertahankan cache hit di seluruh sesi pemikiran yang lebih panjang dan alur kerja multi-langkah.
</Tip>

## Pemikiran dan jendela konteks

`max_tokens`, yang mencakup semua pemikiran yang dihasilkan Claude dalam giliran saat ini, diberlakukan sebagai batas ketat. Pada model Claude 4.5 dan yang lebih baru, jika token input ditambah `max_tokens` melebihi ukuran jendela konteks, API menerima permintaan; jika generasi kemudian mencapai batas jendela konteks, generasi berhenti dengan `stop_reason: "model_context_window_exceeded"` alih-alih mengembalikan error. Pada model yang lebih lama, API mengembalikan error validasi sebagai gantinya. Lihat [Menangani stop reason](/docs/id/build-with-claude/handling-stop-reasons).

Bagaimana pemikiran dihitung terhadap jendela bergantung pada kapan pemikiran itu dihasilkan:

* **Pemikiran giliran saat ini** selalu dihitung terhadap `max_tokens`, ditagih sebagai token output, dan menempati ruang jendela konteks untuk giliran yang menghasilkannya.
* **Pemikiran giliran sebelumnya** bergantung pada [default pemertahanan](#thinking-block-preservation-by-model). Pada [model yang menyimpan semua giliran sebelumnya](#thinking-block-preservation-by-model), blok thinking sebelumnya tetap dalam konteks, dihitung terhadap jendela, dan ditagih sebagai token input seperti sisa riwayat percakapan. Pada model yang hanya menyimpan giliran terakhir, API menghapus blok thinking yang lebih lama secara otomatis ketika Anda mengirimkannya kembali, sehingga tidak mengonsumsi ruang jendela atau token input.

Dalam praktiknya:

* Pada model simpan-semua, anggarkan jendela konteks Anda seolah-olah pemikiran adalah riwayat percakapan biasa, karena memang demikian. Sesi agentik yang panjang mengakumulasi pemikiran dalam konteks; gunakan [penghapusan blok thinking](/docs/id/build-with-claude/context-editing#thinking-block-clearing) jika Anda perlu mengambil kembali ruang.
* Pada model hanya-giliran-terakhir, pemikiran hanya merupakan biaya per-giliran: pemikiran setiap giliran dihitung terhadap `max_tokens` giliran tersebut dan kemudian keluar dari jendela.

Diagram berikut mengilustrasikan rezim hanya-giliran-terakhir (penghapusan). Yang pertama menunjukkan percakapan multi-giliran: blok thinking setiap giliran dihasilkan dalam output tetapi tidak dibawa ke input giliran berikutnya.

![Diagram pemikiran (thinking) pada model yang menghapus blok thinking sebelumnya: blok thinking setiap giliran dihasilkan dalam output dan tidak dibawa ke input giliran berikutnya](/docs/images/context-window-thinking.svg)

Yang kedua menunjukkan rezim yang sama dengan penggunaan alat: pemikiran tetap dalam konteks bersama hasil alatnya selama durasi giliran assistant, lalu keluar pada giliran user berikutnya.

![Diagram pemikiran (thinking) dengan penggunaan alat (tool use) pada model yang menghapus blok thinking sebelumnya: pemikiran disimpan dengan hasil alatnya, lalu dihapus pada giliran user berikutnya](/docs/images/context-window-thinking-tools.svg)

Gunakan [API penghitungan token](/docs/id/build-with-claude/token-counting) untuk mendapatkan hitungan yang akurat untuk kasus penggunaan spesifik Anda, terutama untuk percakapan multi-giliran yang menyertakan pemikiran.

## Enkripsi pemikiran

Konten pemikiran lengkap dienkripsi dan dikembalikan dalam bidang `signature` pada setiap blok thinking. API menggunakan signature untuk memverifikasi bahwa blok thinking dihasilkan oleh Claude ketika Anda mengirimkannya kembali.

Perhatikan hal-hal berikut saat bekerja dengan signature:

* Hanya benar-benar diperlukan untuk mengirim kembali blok thinking ketika [menggunakan alat dengan pemikiran](#thinking-with-tool-use). Selain itu Anda dapat menghilangkan blok thinking dari giliran sebelumnya. Jika Anda mengirimkannya kembali, apakah API menyimpan atau menghapusnya bergantung pada model (lihat [Pemertahanan blok thinking per model](#thinking-block-preservation-by-model)); gunakan [context editing](/docs/id/build-with-claude/context-editing) untuk mengonfigurasi ini.
* Saat mengirim kembali blok thinking, kirimkan semuanya kembali persis seperti yang Anda terima, untuk konsistensi dan untuk menghindari potensi masalah.
* Saat [streaming respons](#streaming-thinking), signature tiba sebagai `signature_delta` di dalam event `content_block_delta` tepat sebelum event `content_block_stop`.
* Nilai `signature` secara signifikan lebih panjang pada Claude 4 dan model yang lebih baru dibandingkan model sebelumnya.
* Bidang `signature` bersifat opak: jangan menafsirkan atau mem-parsing-nya.
* Nilai `signature` kompatibel di seluruh platform (Claude API, [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), dan [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai)). Nilai yang dihasilkan di satu platform bekerja di platform lain.

## Blok redacted thinking

Selain blok `thinking` reguler, API dapat mengembalikan blok `redacted_thinking` ketika sebagian penalaran Claude disunting demi keamanan. Blok `redacted_thinking` berisi konten pemikiran terenkripsi dalam bidang `data`, tanpa teks yang dapat dibaca:

```json
{
  "type": "redacted_thinking",
  "data": "..."
}
```

Bidang `data` bersifat opak dan terenkripsi. Seperti bidang `signature` pada blok thinking reguler, kirimkan blok `redacted_thinking` kembali ke API tanpa perubahan saat melanjutkan percakapan multi-giliran dengan [alat](#thinking-with-tool-use).

<Tip>
  Jika kode Anda memfilter blok konten berdasarkan tipe (misalnya, `block.type == "thinking"`) saat mengirim bolak-balik respons dengan penggunaan alat, sertakan juga blok `redacted_thinking`. Memfilter hanya pada `block.type == "thinking"` secara diam-diam menghilangkan blok `redacted_thinking` dan merusak protokol multi-giliran yang dijelaskan dalam [Mempertahankan blok thinking](#preserving-thinking-blocks).
</Tip>

<Note>
  Blok `redacted_thinking` adalah tipe blok konten yang berbeda yang dikembalikan ketika pemikiran disunting demi keamanan. Ini terpisah dari opsi [`display: "omitted"`](#controlling-thinking-display), yang mengembalikan blok `thinking` reguler dengan bidang `thinking` kosong.
</Note>

## Output pemikiran pada Claude Fable 5 dan Claude Mythos 5

Pada Claude Fable 5 dan Claude Mythos 5, rantai pemikiran mentah tidak pernah dikembalikan; blok yang Anda terima adalah blok `thinking` reguler, bukan `redacted_thinking`, dan [pengaturan `display`](#controlling-thinking-display) bekerja sama seperti pada model lain (teks [yang diringkas](#summarized-thinking), atau bidang `thinking` kosong ketika dihilangkan, yang merupakan default di sini). Untuk bentuk respons blok thinking, lihat [referensi Messages API](/docs/id/api/messages/create).

Saat melanjutkan percakapan pada model yang sama, kirimkan setiap blok thinking kembali ke API persis seperti yang diterima, termasuk blok yang bidang `thinking`-nya kosong. Jangan mengedit atau merekonstruksinya. Membaca teks ringkasan untuk ditampilkan tidak masalah: API menolak blok yang konten yang dikembalikannya telah dimodifikasi, bukan blok yang telah Anda baca. Teks yang ditempatkan di bidang `thinking` kosong yang dihilangkan [diabaikan alih-alih ditolak](#controlling-thinking-display).

Untuk apa yang terjadi pada blok thinking ketika Anda mengganti model di tengah percakapan, lihat [Pemertahanan blok thinking per model](#thinking-block-preservation-by-model).

Dua pengecualian, dibahas dalam [Kredit fallback](/docs/id/build-with-claude/fallback-credit):

* Percobaan ulang kredit fallback harus mengirimkan kembali body permintaan yang ditolak tanpa perubahan.
* Blok `fallback` dari fallback di tengah output tetap di tempat mereka muncul.

Untuk mendapatkan visibilitas ke dalam penalaran model, baca blok `thinking` yang dijelaskan di halaman ini alih-alih meminta penalaran dalam teks respons melalui prompt. Pada Claude Fable 5, permintaan yang mencoba memancing penalaran internal model sebagai bagian dari teks respons dapat ditolak dengan `stop_details.category: "reasoning_extraction"`. Lihat [Kategori penolakan](/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk referensi bidang dan panduan penanganan.

## Batasan dan kompatibilitas fitur

**Parameter sampling.** Pada Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, dan Claude Sonnet 5, nilai `temperature`, `top_p`, atau `top_k` yang bukan default akan mengembalikan error 400 pada setiap permintaan, terlepas dari apakah thinking digunakan atau tidak. Pada model yang lebih lama, pembatasan ini hanya berlaku saat thinking aktif: `temperature` dan `top_k` tidak kompatibel dengan thinking, dan `top_p` diizinkan pada nilai antara 0,95 dan 1.

**Prefill respons dan penggunaan alat paksa.** Anda tidak dapat melakukan pre-fill pada respons assistant saat thinking aktif. Penggunaan alat paksa (`tool_choice: {"type": "any"}` atau `{"type": "tool", ...}`) tidak kompatibel dengan extended thinking (pemikiran diperpanjang) manual tetapi berfungsi dengan adaptive thinking; lihat [Pemikiran dengan penggunaan alat](#thinking-with-tool-use).

**Batas output.** Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5, Claude Opus 4.6, dan Claude Sonnet 4.6 mendukung hingga 128k token output per permintaan. Claude Haiku 4.5, Claude Sonnet 4.5, dan Claude Opus 4.5 mendukung hingga 64k. Pada [Message Batches API](/docs/id/build-with-claude/batch-processing#extended-output-beta), [header beta](/docs/id/api/beta-headers) `output-300k-2026-03-24` menaikkan batas menjadi 300k untuk Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5, Claude Opus 4.6, dan Claude Sonnet 4.6. Lihat [ikhtisar model](/docs/id/about-claude/models/overview) untuk batasan pada model legacy.

**Permintaan panjang.** SDK mewajibkan streaming ketika `max_tokens` lebih besar dari 21.333, untuk menghindari timeout HTTP pada permintaan yang berjalan lama. Ini adalah validasi di sisi klien, bukan pembatasan API. Jika Anda tidak perlu memproses event secara inkremental, gunakan `.stream()` dengan `.get_final_message()` (Python) atau `.finalMessage()` (TypeScript) untuk mendapatkan objek `Message` lengkap tanpa menangani event satu per satu; lihat [Streaming Messages](/docs/id/build-with-claude/streaming#get-the-final-message-without-handling-events). Perkirakan waktu respons yang lebih lama saat thinking aktif, karena menghasilkan blok thinking menambah waktu pemrosesan. Untuk beban kerja yang mendorong thinking melebihi sekitar 32k token per permintaan, gunakan [pemrosesan batch](/docs/id/build-with-claude/batch-processing) untuk menghindari masalah jaringan: permintaan semacam itu dapat berjalan cukup lama hingga mencapai timeout sistem dan batas koneksi terbuka.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Mengarahkan thinking" icon="compass" href="/docs/id/build-with-claude/thinking-steering-and-cost">
    Atur kapan dan seberapa dalam Claude berpikir: tingkat effort, pengarahan berbasis prompt, kontrol biaya, dan harga.
  </Card>

  <Card title="Thinking dalam alur kerja alat dan multi-giliran" icon="wrench" href="/docs/id/build-with-claude/thinking-tool-workflows">
    Telusuri perjalanan lengkap penggunaan alat dua giliran dan lihat apa yang diubah oleh interleaved thinking.
  </Card>

  <Card title="Pemecahan masalah thinking" icon="triangle-alert" href="/docs/id/build-with-claude/thinking-troubleshooting">
    Cocokkan error 400 konfigurasi thinking, field thinking kosong, dan cache miss dengan penyebab dan solusinya.
  </Card>

  <Card title="Effort" icon="sliders" href="/docs/id/build-with-claude/effort">
    Kendalikan berapa banyak token yang digunakan Claude untuk teks, pemanggilan alat, dan thinking dengan parameter effort.
  </Card>
</CardGroup>
