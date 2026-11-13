---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 5bc5d74a11e286baceee2e2277441441dfcf261d3af96d8e8e0a985cd031364b
---

---
title: Diagnostik cache
url: https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics
description: Diagnosis cache miss prompt yang tidak terduga dengan membandingkan permintaan berurutan dan mengidentifikasi secara tepat di mana prefiks prompt menyimpang.
featureMetadata:
  status: stable
  zdr:
    eligibility: qualified
    note: Excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements). Prompt Anda dan output Claude tidak disimpan. Fingerprint berupa hash kriptografis dan estimasi jumlah token disimpan sebentar untuk memungkinkan perbandingan dengan permintaan berikutnya.
  supportedModels:
    - claude-fable-5-2
    - claude-mythos-5-2
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API: stable
---

[Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) memangkas latensi dan biaya secara signifikan, tetapi hanya ketika bagian awal prompt Anda identik byte demi byte dengan permintaan terbaru. Alat yang diurutkan ulang, timestamp yang diinterpolasi ke dalam “system prompt” (prompt sistem) Anda, atau pengeditan pada pesan sebelumnya dapat secara diam-diam membatalkan cache. Tanpa diagnostik cache, satu-satunya sinyal adalah `usage.cache_read_input_tokens` yang turun menjadi nol, tanpa indikasi apa pun tentang apa yang berubah.

Diagnostik cache menutup celah tersebut. Teruskan `id` dari respons sebelumnya, dan API akan membandingkan kedua permintaan. API memberi tahu Anda di mana keduanya menyimpang (model, prompt sistem, alat, atau riwayat pesan), sehingga Anda dapat memperbaiki akar masalahnya alih-alih menebak-nebak.

## Cara kerja diagnostik cache

Untuk setiap permintaan yang menyertakan objek `diagnostics`, API menyimpan “fingerprint” (sidik jari) ringan dengan kunci berupa `id` respons. API tidak menyimpan apa pun untuk permintaan yang tidak menyertakan objek tersebut. Pada permintaan berikutnya, sertakan `id` dari respons sebelumnya sebagai `diagnostics.previous_message_id`. API membangun ulang fingerprint untuk permintaan baru, membandingkannya dengan fingerprint yang tersimpan, dan melampirkan objek `diagnostics` ke respons yang menjelaskan titik penyimpangan pertama.

Perbandingan ini berkaitan dengan struktur permintaan, terlepas dari apakah cache benar-benar hit atau tidak. Lihat [Membaca diagnostik bersama usage](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics#reading-diagnostics-alongside-usage) untuk cara menggabungkan hasil `diagnostics` dengan `usage.cache_read_input_tokens`.

Fingerprint hanya berisi hash dan estimasi jumlah token (tidak pernah berisi konten prompt mentah), disimpan untuk waktu yang terbatas, dibatasi pada organisasi dan workspace Anda, dan tidak digunakan untuk tujuan lain apa pun.

## Penggunaan dasar

Sertakan objek `diagnostics` pada setiap giliran. Objek inilah yang menjadi tanda keikutsertaan (opt-in): API hanya menyimpan fingerprint untuk permintaan yang menyertakannya. Pada giliran pertama, berikan `"previous_message_id": null` untuk ikut serta tanpa pesan sebelumnya sebagai pembanding. Pada giliran-giliran berikutnya, berikan `id` dari respons sebelumnya.

<CodeGroup>
  ```bash cURL
  # Giliran 1: buat cache dan aktifkan diagnostik
  curl -sS --fail-with-body https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "cache_control": {"type": "ephemeral"},
      "system": "You are an AI assistant analyzing a large document. <document>...</document>",
      "messages": [{"role": "user", "content": "Summarize section 1."}],
      "diagnostics": {"previous_message_id": null}
    }'

  # Giliran 2: teruskan id dari respons giliran 1 sebagai previous_message_id agar API dapat membandingkan prefiks.
  # Dalam respons, diagnostics: null berarti tidak ditemukan divergensi.
  curl -sS --fail-with-body https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "cache_control": {"type": "ephemeral"},
      "system": "You are an AI assistant analyzing a large document. <document>...</document>",
      "messages": [
        {"role": "user", "content": "Summarize section 1."},
        {"role": "assistant", "content": "Section 1 covers..."},
        {"role": "user", "content": "Now summarize section 2."}
      ],
      "diagnostics": {"previous_message_id": "'"$message_id"'"}
    }'
  ```

  ```bash CLI
  # Giliran 1: buat cache dan aktifkan diagnostik
  ant beta:messages create <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  cache_control:
    type: ephemeral
  system: "You are an AI assistant analyzing a large document. <document>...</document>"
  messages:
    - role: user
      content: Summarize section 1.
  diagnostics:
    previous_message_id: null
  YAML

  # Giliran 2: teruskan id dari respons giliran 1 sebagai previous_message_id
  ant beta:messages create <<YAML
  model: claude-opus-5-5
  max_tokens: 1024
  cache_control:
    type: ephemeral
  system: "You are an AI assistant analyzing a large document. <document>...</document>"
  messages:
    - role: user
      content: Summarize section 1.
    - role: assistant
      content: Section 1 covers...
    - role: user
      content: Now summarize section 2.
  diagnostics:
    previous_message_id: $message_id
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>"

  # Giliran 1: ikut serta dengan previous_message_id=None
  r1 = client.beta.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      cache_control={"type": "ephemeral"},
      system=SYSTEM,
      messages=[{"role": "user", "content": "Summarize section 1."}],
      diagnostics={"previous_message_id": None},
  )

  # Giliran 2: rujuk id respons sebelumnya
  r2 = client.beta.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      cache_control={"type": "ephemeral"},
      system=SYSTEM,
      messages=[
          {"role": "user", "content": "Summarize section 1."},
          {"role": "assistant", "content": r1.content},
          {"role": "user", "content": "Now summarize section 2."},
      ],
      diagnostics={"previous_message_id": r1.id},
  )

  diagnostics = r2.diagnostics
  if diagnostics is None:
      print("No divergence detected.")
  elif diagnostics.cache_miss_reason is None:
      print("Comparison still pending.")
  else:
      print(f"cache_miss_reason: {diagnostics.cache_miss_reason.type}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>";

  // Giliran 1: ikut serta dengan previous_message_id: null
  const r1 = await client.beta.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    cache_control: { type: "ephemeral" },
    system: SYSTEM,
    messages: [{ role: "user", content: "Summarize section 1." }],
    diagnostics: { previous_message_id: null }
  });

  // Giliran 2: rujuk id respons sebelumnya
  const r2 = await client.beta.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    cache_control: { type: "ephemeral" },
    system: SYSTEM,
    messages: [
      { role: "user", content: "Summarize section 1." },
      { role: "assistant", content: r1.content },
      { role: "user", content: "Now summarize section 2." }
    ],
    diagnostics: { previous_message_id: r1.id }
  });

  if (r2.diagnostics === null) {
    console.log("No divergence detected.");
  } else if (r2.diagnostics.cache_miss_reason === null) {
    console.log("Comparison still pending.");
  } else {
    console.log(`cache_miss_reason: ${r2.diagnostics.cache_miss_reason.type}`);
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var system = "You are an AI assistant analyzing a large document. <document>...</document>";

  var r1 = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          CacheControl = new(),
          System = system,
          Messages = [new BetaUserMessageParam { Content = "Summarize section 1." }],
          Diagnostics = new() { PreviousMessageID = null },
      }
  );

  var r2 = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          CacheControl = new(),
          System = system,
          Messages =
          [
              new BetaUserMessageParam { Content = "Summarize section 1." },
              new BetaAssistantMessageParam
              {
                  Content = r1.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
              },
              new BetaUserMessageParam { Content = "Now summarize section 2." },
          ],
          Diagnostics = new() { PreviousMessageID = r1.ID },
      }
  );

  Console.WriteLine(r2.Diagnostics switch
  {
      null => "No divergence detected.",
      { CacheMissReason: null } => "Comparison still pending.",
      { CacheMissReason.Type: var type } => $"cache_miss_reason: {type.Raw()}",
  });
  ```

  ```go Go
  client := anthropic.NewClient()
  ctx := context.Background()

  system := []anthropic.BetaTextBlockParam{
  	{Text: "You are an AI assistant analyzing a large document. <document>...</document>"},
  }

  r1, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:        anthropic.ModelClaudeOpus5_5,
  	MaxTokens:    1024,
  	CacheControl: anthropic.BetaCacheControlEphemeralParam{},
  	System:       system,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Summarize section 1.")),
  	},
  	Diagnostics: anthropic.BetaDiagnosticsParam{
  		PreviousMessageID: param.Null[string](),
  	},
  })
  if err != nil {
  	panic(err)
  }

  r2, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:        anthropic.ModelClaudeOpus5_5,
  	MaxTokens:    1024,
  	CacheControl: anthropic.BetaCacheControlEphemeralParam{},
  	System:       system,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Summarize section 1.")),
  		r1.ToParam(),
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Now summarize section 2.")),
  	},
  	Diagnostics: anthropic.BetaDiagnosticsParam{
  		PreviousMessageID: anthropic.String(r1.ID),
  	},
  })
  if err != nil {
  	panic(err)
  }

  switch {
  case !r2.JSON.Diagnostics.Valid():
  	fmt.Println("No divergence detected.")
  case !r2.Diagnostics.JSON.CacheMissReason.Valid():
  	fmt.Println("Comparison still pending.")
  default:
  	fmt.Printf("cache_miss_reason: %s\n", r2.Diagnostics.CacheMissReason.Type)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaCacheControlEphemeral;
  import com.anthropic.models.beta.messages.BetaDiagnosticsParam;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      var client = AnthropicOkHttpClient.fromEnv();

      var system = "You are an AI assistant analyzing a large document. <document>...</document>";

      var r1 = client.beta().messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(1024)
              .cacheControl(BetaCacheControlEphemeral.builder().build())
              .system(system)
              .addUserMessage("Summarize section 1.")
              // Berikan null pada giliran pertama untuk ikut serta tanpa pesan sebelumnya sebagai pembanding.
              .diagnostics(BetaDiagnosticsParam.builder().previousMessageId((String) null).build())
              .build()
      );

      var r2 = client.beta().messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5_5)
              .maxTokens(1024)
              .cacheControl(BetaCacheControlEphemeral.builder().build())
              .system(system)
              .addUserMessage("Summarize section 1.")
              .addMessage(r1)
              .addUserMessage("Now summarize section 2.")
              .diagnostics(BetaDiagnosticsParam.builder().previousMessageId(r1.id()).build())
              .build()
      );

      if (r2.diagnostics().isEmpty()) {
          IO.println("No divergence detected.");
      } else if (r2.diagnostics().get().cacheMissReason().isEmpty()) {
          IO.println("Comparison still pending.");
      } else {
          var reason = r2.diagnostics().get().cacheMissReason().get();
          IO.println("cache_miss_reason: " + reason.type().asString());
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Messages\BetaCacheControlEphemeral;
  use Anthropic\Beta\Messages\BetaDiagnosticsParam;
  use Anthropic\Messages\Model;

  $client = new Client();

  $system = 'You are an AI assistant analyzing a large document. <document>...</document>';

  $r1 = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 1024,
      cacheControl: new BetaCacheControlEphemeral,
      system: $system,
      messages: [
          ['role' => 'user', 'content' => 'Summarize section 1.'],
      ],
      diagnostics: (new BetaDiagnosticsParam)->withPreviousMessageID(null),
  );

  $r2 = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 1024,
      cacheControl: new BetaCacheControlEphemeral,
      system: $system,
      messages: [
          ['role' => 'user', 'content' => 'Summarize section 1.'],
          ['role' => 'assistant', 'content' => $r1->content],
          ['role' => 'user', 'content' => 'Now summarize section 2.'],
      ],
      diagnostics: (new BetaDiagnosticsParam)->withPreviousMessageID($r1->id),
  );

  echo match (true) {
      $r2->diagnostics === null => "No divergence detected.\n",
      $r2->diagnostics->cacheMissReason === null => "Comparison still pending.\n",
      default => "cache_miss_reason: {$r2->diagnostics->cacheMissReason->type}\n",
  };
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>"

  r1 = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    cache_control: {type: "ephemeral"},
    system_: SYSTEM,
    messages: [
      {role: "user", content: "Summarize section 1."}
    ],
    diagnostics: {previous_message_id: nil}
  )

  r2 = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    cache_control: {type: "ephemeral"},
    system_: SYSTEM,
    messages: [
      {role: "user", content: "Summarize section 1."},
      {role: "assistant", content: r1.content},
      {role: "user", content: "Now summarize section 2."}
    ],
    diagnostics: {previous_message_id: r1.id}
  )

  case r2.diagnostics
  in nil
    puts "No divergence detected."
  in {cache_miss_reason: nil}
    puts "Comparison still pending."
  in {cache_miss_reason: {type:}}
    puts "cache_miss_reason: #{type}"
  end
  ```
</CodeGroup>

## Streaming

Dalam respons streaming, `diagnostics` muncul pada event `message_start`.

<CodeGroup>
  ```bash cURL
  # Giliran 2: lakukan streaming respons. diagnostics tiba pada event message_start;
  # nilai null berarti tidak ditemukan divergensi.
  curl -sS --fail-with-body https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "stream": true,
      "cache_control": {"type": "ephemeral"},
      "system": "You are an AI assistant analyzing a large document. <document>...</document>",
      "messages": [
        {"role": "user", "content": "Summarize section 1."},
        {"role": "assistant", "content": "Section 1 covers..."},
        {"role": "user", "content": "Now summarize section 2."}
      ],
      "diagnostics": {"previous_message_id": "'"$message_id"'"}
    }'
  ```

  ```bash CLI
  # Giliran 2: streaming. Dengan --stream, CLI mengeluarkan setiap event SSE sebagai satu objek JSON.
  # diagnostics tiba pada event message_start.
  ant beta:messages create --stream <<YAML
  model: claude-opus-5-5
  max_tokens: 1024
  cache_control:
    type: ephemeral
  system: "You are an AI assistant analyzing a large document. <document>...</document>"
  messages:
    - role: user
      content: Summarize section 1.
    - role: assistant
      content: Section 1 covers...
    - role: user
      content: Now summarize section 2.
  diagnostics:
    previous_message_id: $message_id
  YAML
  ```

  ```python Python
  # Giliran 2: streaming, merujuk ke id respons sebelumnya
  with client.beta.messages.stream(
      model="claude-opus-5-5",
      max_tokens=1024,
      cache_control={"type": "ephemeral"},
      system=SYSTEM,
      messages=[
          {"role": "user", "content": "Summarize section 1."},
          {"role": "assistant", "content": r1.content},
          {"role": "user", "content": "Now summarize section 2."},
      ],
      diagnostics={"previous_message_id": r1.id},
  ) as stream:
      for text in stream.text_stream:
          print(text, end="", flush=True)
      print()
      r2 = stream.get_final_message()

  diagnostics = r2.diagnostics
  if diagnostics is None:
      print("No divergence detected.")
  elif diagnostics.cache_miss_reason is None:
      print("Comparison still pending.")
  else:
      print(f"cache_miss_reason: {diagnostics.cache_miss_reason.type}")
  ```

  ```typescript TypeScript
  const stream = client.beta.messages.stream({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    cache_control: { type: "ephemeral" },
    system: SYSTEM,
    messages: [
      { role: "user", content: "Summarize section 1." },
      { role: "assistant", content: r1.content },
      { role: "user", content: "Now summarize section 2." }
    ],
    diagnostics: { previous_message_id: r1.id }
  });

  for await (const event of stream) {
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
  process.stdout.write("\n");

  // diagnostics tiba pada message_start dan diteruskan hingga pesan akhir
  const r2 = await stream.finalMessage();

  if (r2.diagnostics === null) {
    console.log("No divergence detected.");
  } else if (r2.diagnostics.cache_miss_reason === null) {
    console.log("Comparison still pending.");
  } else {
    console.log(`cache_miss_reason: ${r2.diagnostics.cache_miss_reason.type}`);
  }
  ```

  ```csharp C#
  // Giliran 2: streaming, dengan merujuk id respons sebelumnya
  BetaDiagnostics? diagnostics = null;

  var stream = client.Beta.Messages.CreateStreaming(
      new()
      {
          Model = Messages::Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          CacheControl = new(),
          System = system,
          Messages =
          [
              new BetaUserMessageParam { Content = "Summarize section 1." },
              new BetaAssistantMessageParam
              {
                  Content = r1.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
              },
              new BetaUserMessageParam { Content = "Now summarize section 2." },
          ],
          Diagnostics = new() { PreviousMessageID = r1.ID },
      }
  );

  await foreach (var streamEvent in stream)
  {
      if (streamEvent.TryPickStart(out var start))
      {
          // diagnostics diterima pada event message_start
          diagnostics = start.Message.Diagnostics;
      }
      else if (streamEvent.TryPickContentBlockDelta(out var delta) && delta.Delta.TryPickText(out var textDelta))
      {
          Console.Write(textDelta.Text);
      }
  }
  Console.WriteLine();

  Console.WriteLine(diagnostics switch
  {
      null => "No divergence detected.",
      { CacheMissReason: null } => "Comparison still pending.",
      { CacheMissReason.Type: var type } => $"cache_miss_reason: {type.Raw()}",
  });
  ```

  ```go Go
  // Giliran 2: streaming, merujuk ke id respons sebelumnya
  stream := client.Beta.Messages.NewStreaming(ctx, anthropic.BetaMessageNewParams{
  	Model:        anthropic.ModelClaudeOpus5_5,
  	MaxTokens:    1024,
  	CacheControl: anthropic.BetaCacheControlEphemeralParam{},
  	System:       system,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Summarize section 1.")),
  		r1.ToParam(),
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Now summarize section 2.")),
  	},
  	Diagnostics: anthropic.BetaDiagnosticsParam{
  		PreviousMessageID: anthropic.String(r1.ID),
  	},
  })
  defer stream.Close()

  // diagnostics tiba pada message_start; Accumulate membawanya ke r2
  var r2 anthropic.BetaMessage
  for stream.Next() {
  	if err := r2.Accumulate(stream.Current()); err != nil {
  		panic(err)
  	}
  }
  if err := stream.Err(); err != nil {
  	panic(err)
  }

  switch {
  case !r2.JSON.Diagnostics.Valid():
  	fmt.Println("No divergence detected.")
  case !r2.Diagnostics.JSON.CacheMissReason.Valid():
  	fmt.Println("Comparison still pending.")
  default:
  	fmt.Printf("cache_miss_reason: %s\n", r2.Diagnostics.CacheMissReason.Type)
  }
  ```

  ```java Java
  // Giliran 2: streaming, merujuk ke id respons sebelumnya
  var params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024)
      .cacheControl(BetaCacheControlEphemeral.builder().build())
      .system(system)
      .addUserMessage("Summarize section 1.")
      .addMessage(r1)
      .addUserMessage("Now summarize section 2.")
      .diagnostics(BetaDiagnosticsParam.builder().previousMessageId(r1.id()).build())
      .build();

  var accumulator = BetaMessageAccumulator.create();
  try (var streamResponse = client.beta().messages().createStreaming(params)) {
      streamResponse.stream()
          .peek(accumulator::accumulate)
          .flatMap(event -> event.contentBlockDelta().stream())
          .flatMap(deltaEvent -> deltaEvent.delta().text().stream())
          .forEach(textDelta -> IO.print(textDelta.text()));
      IO.println("");
  }

  // diagnostics tiba pada message_start dan diteruskan ke pesan yang terakumulasi
  var diagnostics = accumulator.message().diagnostics();
  if (diagnostics.isEmpty()) {
      IO.println("No divergence detected.");
  } else if (diagnostics.get().cacheMissReason().isEmpty()) {
      IO.println("Comparison still pending.");
  } else {
      var reason = diagnostics.get().cacheMissReason().get();
      IO.println("cache_miss_reason: " + reason.type().asString());
  }
  ```

  ```php PHP
  // Giliran 2: streaming, merujuk ke id respons sebelumnya
  $stream = $client->beta->messages->createStream(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 1024,
      cacheControl: new BetaCacheControlEphemeral,
      system: $system,
      messages: [
          ['role' => 'user', 'content' => 'Summarize section 1.'],
          ['role' => 'assistant', 'content' => $r1->content],
          ['role' => 'user', 'content' => 'Now summarize section 2.'],
      ],
      diagnostics: (new BetaDiagnosticsParam)->withPreviousMessageID($r1->id),
  );

  $diagnostics = null;
  foreach ($stream as $event) {
      switch (true) {
          case $event instanceof \Anthropic\Beta\Messages\BetaRawMessageStartEvent:
              // diagnostics tiba pada BetaMessage yang tertanam di event message_start
              $diagnostics = $event->message->diagnostics;
              break;
          case $event instanceof \Anthropic\Beta\Messages\BetaRawContentBlockDeltaEvent:
              if ($event->delta instanceof \Anthropic\Beta\Messages\BetaTextDelta) {
                  echo $event->delta->text;
              }
              break;
      }
  }
  echo PHP_EOL;

  echo match (true) {
      $diagnostics === null => "No divergence detected.\n",
      $diagnostics->cacheMissReason === null => "Comparison still pending.\n",
      default => "cache_miss_reason: {$diagnostics->cacheMissReason->type}\n",
  };
  ```

  ```ruby Ruby
  # Giliran 2: streaming, merujuk ke id respons sebelumnya
  stream = client.beta.messages.stream(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    cache_control: {type: "ephemeral"},
    system_: SYSTEM,
    messages: [
      {role: "user", content: "Summarize section 1."},
      {role: "assistant", content: r1.content},
      {role: "user", content: "Now summarize section 2."}
    ],
    diagnostics: {previous_message_id: r1.id}
  )

  stream.each do |event|
    print(event.text) if event.is_a?(Anthropic::Streaming::TextEvent)
  end
  puts

  # diagnostics tiba pada message_start dan dipertahankan pada pesan yang terakumulasi
  r2 = stream.accumulated_message

  case r2.diagnostics
  in nil
    puts "No divergence detected."
  in {cache_miss_reason: nil}
    puts "Comparison still pending."
  in {cache_miss_reason: {type:}}
    puts "cache_miss_reason: #{type}"
  end
  ```
</CodeGroup>

Event `message_start` membawa field `diagnostics` lengkap; lihat [Format respons](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics#response-format) untuk nilai-nilai yang mungkin.

## Meneruskan diagnostik melalui loop percakapan

Dalam percakapan multi-giliran, bawa `id` respons terbaru ke depan sebagai `previous_message_id` pada setiap giliran. Iterasi pertama meneruskan `null` untuk ikut serta; setiap iterasi berikutnya meneruskan `id` dari respons sebelumnya.

<CodeGroup exclude="shell:cURL, shell:CLI">
  <CodeGroupItem language="cURL">
    Alur kerja ini memerlukan logika yang lebih banyak daripada satu perintah shell. Gunakan Anthropic SDK untuk menjalankan loop. Setiap giliran mengirimkan permintaan HTTP yang sama seperti di [Penggunaan dasar](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics#basic-usage).
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Alur kerja ini memerlukan logika yang lebih banyak daripada satu perintah shell. Gunakan Anthropic SDK untuk menjalankan loop. Setiap giliran mengirimkan permintaan yang sama seperti di [Penggunaan dasar](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics#basic-usage).
  </CodeGroupItem>

  ```python Python
  client = anthropic.Anthropic()

  SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>"

  messages = []
  prev_id = None

  for turn, user_message in enumerate(
      ["Summarize section 1.", "Now section 2.", "Now section 3."]
  ):
      messages.append({"role": "user", "content": user_message})

      response = client.beta.messages.create(
          model="claude-opus-5-5",
          max_tokens=1024,
          cache_control={"type": "ephemeral"},
          system=SYSTEM,
          messages=messages,
          diagnostics={"previous_message_id": prev_id},
      )

      if (
          response.diagnostics is not None
          and response.diagnostics.cache_miss_reason is not None
      ):
          print(
              f"Turn {turn + 1} cache_miss_reason: {response.diagnostics.cache_miss_reason.type}"
          )

      messages.append({"role": "assistant", "content": response.content})
      prev_id = response.id
  ```

  ```typescript TypeScript
  import type { BetaMessage, BetaMessageParam } from "@anthropic-ai/sdk/resources/beta";

  const client = new Anthropic();

  const SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>";

  const prompts = ["Summarize section 1.", "Now section 2.", "Now section 3."];

  const messages: BetaMessageParam[] = [];
  let prevId: string | null = null;

  for (const [turn, prompt] of prompts.entries()) {
    messages.push({ role: "user", content: prompt });

    const response: BetaMessage = await client.beta.messages.create({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      cache_control: { type: "ephemeral" },
      system: SYSTEM,
      messages,
      diagnostics: { previous_message_id: prevId }
    });

    if (response.diagnostics?.cache_miss_reason) {
      console.log(
        `Turn ${turn + 1} cache_miss_reason: ${response.diagnostics.cache_miss_reason.type}`
      );
    }

    messages.push({ role: "assistant", content: response.content });
    prevId = response.id;
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

  AnthropicClient client = new();

  var system = "You are an AI assistant analyzing a large document. <document>...</document>";

  List<BetaMessageParam> messages = [];
  string? prevId = null;
  string[] prompts = ["Summarize section 1.", "Now section 2.", "Now section 3."];

  for (int turn = 0; turn < prompts.Length; turn++)
  {
      messages.Add(new BetaUserMessageParam { Content = prompts[turn] });

      var response = await client.Beta.Messages.Create(
          new()
          {
              Model = Messages::Model.ClaudeOpus5_5,
              MaxTokens = 1024,
              CacheControl = new(),
              System = system,
              Messages = messages,
              Diagnostics = new() { PreviousMessageID = prevId },
          }
      );

      if (response.Diagnostics?.CacheMissReason is { Type: var type })
      {
          Console.WriteLine($"Turn {turn + 1} cache_miss_reason: {type.Raw()}");
      }

      messages.Add(
          new BetaAssistantMessageParam
          {
              Content = response.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
          }
      );
      prevId = response.ID;
  }
  ```

  ```go Go
  client := anthropic.NewClient()
  ctx := context.Background()

  system := []anthropic.BetaTextBlockParam{
  	{Text: "You are an AI assistant analyzing a large document. <document>...</document>"},
  }

  prompts := []string{"Summarize section 1.", "Now section 2.", "Now section 3."}

  var messages []anthropic.BetaMessageParam
  prevID := param.Null[string]()

  for turn, prompt := range prompts {
  	messages = append(messages, anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(prompt)))

  	response, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  		Model:        anthropic.ModelClaudeOpus5_5,
  		MaxTokens:    1024,
  		CacheControl: anthropic.BetaCacheControlEphemeralParam{},
  		System:       system,
  		Messages:     messages,
  		Diagnostics: anthropic.BetaDiagnosticsParam{
  			PreviousMessageID: prevID,
  		},
  	})
  	if err != nil {
  		panic(err)
  	}

  	if response.JSON.Diagnostics.Valid() && response.Diagnostics.JSON.CacheMissReason.Valid() {
  		fmt.Printf("Turn %d cache_miss_reason: %s\n", turn+1, response.Diagnostics.CacheMissReason.Type)
  	}

  	messages = append(messages, response.ToParam())
  	prevID = anthropic.String(response.ID)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaCacheControlEphemeral;
  import com.anthropic.models.beta.messages.BetaDiagnosticsParam;
  import com.anthropic.models.beta.messages.BetaMessageParam;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      var client = AnthropicOkHttpClient.fromEnv();

      var system = "You are an AI assistant analyzing a large document. <document>...</document>";
      var prompts = List.of("Summarize section 1.", "Now section 2.", "Now section 3.");

      var messages = new ArrayList<BetaMessageParam>();
      String prevId = null;

      for (var turn = 0; turn < prompts.size(); turn++) {
          messages.add(BetaMessageParam.ofUser(prompts.get(turn)));

          var response = client.beta().messages().create(
              MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5_5)
                  .maxTokens(1024)
                  .cacheControl(BetaCacheControlEphemeral.builder().build())
                  .system(system)
                  .messages(messages)
                  .diagnostics(BetaDiagnosticsParam.builder().previousMessageId(prevId).build())
                  .build()
          );

          if (response.diagnostics().isPresent() && response.diagnostics().get().cacheMissReason().isPresent()) {
              var reason = response.diagnostics().get().cacheMissReason().get();
              IO.println("Turn " + (turn + 1) + " cache_miss_reason: " + reason.type().asString());
          }

          messages.add(response.toParam());
          prevId = response.id();
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Messages\BetaCacheControlEphemeral;
  use Anthropic\Beta\Messages\BetaDiagnosticsParam;
  use Anthropic\Messages\Model;

  $client = new Client();

  $system = 'You are an AI assistant analyzing a large document. <document>...</document>';

  $messages = [];
  $prevId = null;

  foreach (['Summarize section 1.', 'Now section 2.', 'Now section 3.'] as $index => $userMsg) {
      $turn = $index + 1;
      $messages[] = ['role' => 'user', 'content' => $userMsg];

      $response = $client->beta->messages->create(
          model: Model::CLAUDE_OPUS_5_5,
          maxTokens: 1024,
          cacheControl: new BetaCacheControlEphemeral,
          system: $system,
          messages: $messages,
          diagnostics: (new BetaDiagnosticsParam)->withPreviousMessageID($prevId),
      );

      if ($response->diagnostics?->cacheMissReason !== null) {
          echo "Turn {$turn} cache_miss_reason: {$response->diagnostics->cacheMissReason->type}\n";
      }

      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      $prevId = $response->id;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>"

  messages = []
  prev_id = nil

  ["Summarize section 1.", "Now section 2.", "Now section 3."].each_with_index do |user_msg, turn|
    messages << {role: "user", content: user_msg}

    response = client.beta.messages.create(
      model: Anthropic::Model::CLAUDE_OPUS_5_5,
      max_tokens: 1024,
      cache_control: {type: "ephemeral"},
      system_: SYSTEM,
      messages: messages,
      diagnostics: {previous_message_id: prev_id}
    )

    if (reason = response.diagnostics&.cache_miss_reason)
      puts "Turn #{turn + 1} cache_miss_reason: #{reason.type}"
    end

    messages << {role: "assistant", content: response.content}
    prev_id = response.id
  end
  ```
</CodeGroup>

## Format respons

Field `diagnostics` pada `Message` respons memiliki tiga kemungkinan nilai:

| Nilai                          | Arti                                                                                                                                                                                                                         |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `null`                         | Permintaan tidak menyertakan objek `diagnostics`, `previous_message_id` bernilai `null` (giliran pertama, tidak ada yang dibandingkan), atau tidak ada yang menyimpang sebelum breakpoint terakhir.                          |
| `{"cache_miss_reason": null}`  | Perbandingan masih berjalan ketika respons diserialisasi. Hal ini dapat terjadi ketika respons dimulai dengan sangat cepat. Anggap hasilnya tidak meyakinkan dan periksa giliran berikutnya.                                 |
| `{"cache_miss_reason": {...}}` | Sebuah `cache_miss_reason` dilampirkan. Untuk tipe `*_changed`, ini mengidentifikasi titik penyimpangan pertama; `previous_message_not_found` dan `unavailable` adalah kasus di mana tidak ada perbandingan yang dihasilkan. |

Ketika `cache_miss_reason` tidak null, bentuknya seperti ini:

```json
{
  "id": "msg_01Xyz...",
  "type": "message",
  "role": "assistant",
  "content": [{ "type": "text", "text": "..." }],
  "usage": {
    "input_tokens": 42,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 41850,
    "output_tokens": 210
  },
  "diagnostics": {
    "cache_miss_reason": {
      "type": "system_changed",
      "cache_missed_input_tokens": 41850
    }
  }
}
```

## Tipe alasan cache miss

`cache_miss_reason` adalah discriminated union pada `type`. Respons hanya melaporkan divergensi paling awal, jadi perbaiki itu terlebih dahulu; divergensi berikutnya mungkin tersembunyi di baliknya.

| Tipe                         | Artinya                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Yang perlu diubah                                                                                                                                                                                                                                                                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model_changed`              | `model` berbeda dari permintaan sebelumnya (misalnya, router, pengujian A/B, atau fallback memilih model yang berbeda). Cache bersifat per-model.                                                                                                                                                                                                                                                                                                                        | Pertahankan model tetap konstan dalam percakapan yang di-cache.                                                                                                                                                                                                                                                                         |
| `system_changed`             | Parameter `system` berbeda. Biasanya timestamp, ID permintaan, atau nilai per-permintaan lainnya diinterpolasi ke dalam prompt sistem.                                                                                                                                                                                                                                                                                                                                   | Jadikan prompt sistem sebagai konstanta yang stabil secara byte dan letakkan nilai yang berubah di pesan `user` yang akan Anda kirim.                                                                                                                                                                                                   |
| `tools_changed`              | Array `tools` berbeda: alat ditambahkan, dihapus, atau diurutkan ulang antar giliran, atau JSON `input_schema` alat diserialisasi secara non-deterministik.                                                                                                                                                                                                                                                                                                              | Kirim daftar alat yang sama pada setiap giliran dalam urutan tetap dengan skema yang diserialisasi secara deterministik (misalnya, urutkan kunci).                                                                                                                                                                                      |
| `messages_changed`           | Model, prompt sistem, dan alat semuanya cocok, tetapi entri sebelumnya dalam `messages` diubah, diurutkan ulang, atau dihapus alih-alih ditambahkan di akhir. Biasanya riwayat percakapan dipotong atau diedit, atau giliran asisten dan blok `tool_result` diserialisasi ulang secara berbeda saat dikirim kembali.                                                                                                                                                     | Perlakukan riwayat sebagai append-only; kembalikan `content` asisten dan hasil alat secara verbatim.                                                                                                                                                                                                                                    |
| `previous_message_not_found` | Tidak ada fingerprint tersimpan untuk `previous_message_id` yang diberikan. Ini bukan bukti bahwa permintaan Anda berubah. Biasanya permintaan sebelumnya tidak menyertakan objek `diagnostics`, berasal dari workspace yang berbeda, atau sudah terlalu lama sejak dikirim.                                                                                                                                                                                             | Sertakan objek `diagnostics` pada setiap giliran dan jaga agar giliran-giliran berturut-turut berdekatan waktunya.                                                                                                                                                                                                                      |
| `unavailable`                | Informasi diagnostik tidak tersedia untuk permintaan ini. Ini mencakup kasus di mana `model`, `system`, dan `tools` cocok tetapi parameter permintaan lain yang memengaruhi prompt (`tool_choice`, `thinking`, `context_management`, `output_config`, `output_format`, atau kumpulan header `anthropic-beta` yang aktif) berbeda, serta percakapan yang sangat panjang di mana penyimpangan berada di luar horizon perbandingan. Permintaan Anda diproses secara normal. | Pertahankan parameter permintaan yang memengaruhi prompt tetap konstan selama masa hidup percakapan yang di-cache. Jika terus terjadi, terapkan pemeriksaan manual di bagian [Memecahkan masalah umum](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#troubleshooting-common-issues) pada halaman caching prompt. |

<Note>
  Keempat tipe `*_changed` juga membawa integer `cache_missed_input_tokens`: estimasi berapa banyak token input yang berada setelah titik penyimpangan, memberi Anda gambaran tentang seberapa banyak prefiks yang dapat di-cache yang hilang. Nilai ini diturunkan dari panjang byte sebelum tokenisasi, jadi perlakukan sebagai indikator besaran, bukan angka penagihan. Nilainya dapat berbeda dari (dan terkadang melebihi) `usage.input_tokens`.
</Note>

## Membaca diagnostik bersama usage

`diagnostics` memberi tahu Anda apakah permintaan Anda berubah, dan `usage.cache_read_input_tokens` memberi tahu Anda apakah cache hit. Menggabungkan keduanya memberi tahu Anda di mana harus mencari.

Matriks ini berlaku untuk giliran di mana Anda meneruskan `previous_message_id` yang nyata. Pada giliran pertama (`previous_message_id: null`), `diagnostics` selalu `null` dan `cache_read_input_tokens` biasanya nol karena cache sedang ditulis, bukan dibaca; tidak diperlukan pemecahan masalah. Matriks ini juga tidak berlaku ketika `cache_miss_reason` bernilai `null` (perbandingan masih tertunda; periksa giliran berikutnya) atau ketika `type`-nya adalah `previous_message_not_found` atau `unavailable` (tidak ada perbandingan yang dihasilkan).

| Hasil diagnostik                            | Token pembacaan cache | Interpretasi                                                                                                                                                                                                                                                     |
| ------------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `null`                                      | tinggi                | Cache hit.                                                                                                                                                                                                                                                       |
| `null`                                      | rendah atau nol       | Permintaan Anda cocok, tetapi tidak ada entri cache untuk dibaca: entri tersebut telah kedaluwarsa, atau prompt lebih pendek dari [panjang minimum yang dapat di-cache](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations). |
| `cache_miss_reason` adalah tipe `*_changed` | rendah atau nol       | Permintaan berubah; perbaiki penyebab yang ditunjukkan oleh `type`.                                                                                                                                                                                              |
| `cache_miss_reason` adalah tipe `*_changed` | tinggi                | Jarang. Perubahan terjadi di bagian akhir prompt tetapi breakpoint `cache_control` sebelumnya masih hit. Layak diperbaiki, tetapi dampaknya rendah.                                                                                                              |

## Keterbatasan

* **Hanya Claude API:** Diagnostik cache tersedia di Claude API.
* **Retensi terbatas:** Fingerprint untuk pencarian `previous_message_id` kedaluwarsa setelah periode singkat. Jalankan perbandingan diagnostik antara permintaan yang berdekatan waktunya.
* **Workspace yang sama:** Permintaan sebelumnya harus dijalankan dalam organisasi dan workspace yang sama. Untuk memeriksanya, bandingkan [header respons](https://platform.claude.com/docs/id/api/overview#response-headers) `anthropic-workspace-id` pada kedua respons.
* **Cakupan perbandingan:** Untuk percakapan yang sangat panjang ketika satu-satunya perubahan berada jauh di dalam daftar pesan, respons mungkin berupa `unavailable` alih-alih lokasi yang tepat.
* **Upaya terbaik:** Diagnostik tidak pernah memblokir atau menggagalkan permintaan Anda. Jika informasi diagnostik tidak tersedia, respons mengembalikan `unavailable`, atau `cache_miss_reason: null` ketika perbandingan masih berjalan.

## Retensi data

Diagnostik cache memenuhi syarat ZDR (dengan kualifikasi). Anthropic tidak menyimpan teks mentah prompt Anda atau output Claude untuk fitur ini.

API hanya menyimpan fingerprint untuk permintaan yang menyertakan objek `diagnostics`. Fingerprint hanya terdiri dari hash kriptografis dan estimasi jumlah token, dengan kunci berupa `id` respons dan dibatasi cakupannya pada organisasi dan workspace Anda. Fingerprint kedaluwarsa setelah periode singkat dan tidak digunakan untuk tujuan lain apa pun.

## Lihat juga

* [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)
* [Penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting)

## Ketersediaan

Diagnostik cache tersedia di semua model.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tersedia

| Status   | Platform cloud |
| -------- | -------------- |
| Tersedia | Claude API     |

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tidak tersedia

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                                                                                                                                                             | HIPAA       |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------- |
| Status | Layak (bersyarat; tidak termasuk [Model yang dicakup](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements))                                                                                                                                  | Tidak layak |
| Detail | Prompt Anda dan output Claude tidak disimpan. Fingerprint berupa hash kriptografis dan estimasi jumlah token disimpan sebentar untuk memungkinkan perbandingan dengan permintaan berikutnya. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics#data-retention) | —           |

Endpoint yang berlaku:

* `/v1/messages` dengan `diagnostics`
