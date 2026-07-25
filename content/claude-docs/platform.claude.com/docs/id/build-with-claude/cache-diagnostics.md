---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/cache-diagnostics
fetched_at: 2026-07-25T03:07:29.726338Z
sha256: 5f4060a42a18bc73267874e5f88317ce409eef2db000dd31af268cd064ea44c3
---

# Diagnostik cache

Diagnosis cache miss prompt yang tidak terduga dengan membandingkan permintaan berurutan dan mengidentifikasi dengan tepat di mana prefiks prompt menyimpang.

---

<Note>
  Untuk mengetahui bagaimana "zero data retention" (retensi data nol), atau ZDR, berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

[Prompt caching](/docs/id/build-with-claude/prompt-caching) (caching prompt) memangkas latensi dan biaya secara signifikan, tetapi hanya ketika awal prompt Anda identik byte-demi-byte dengan permintaan terbaru. Alat yang diurutkan ulang, timestamp yang diinterpolasi ke dalam prompt sistem Anda, atau pengeditan pada pesan sebelumnya dapat secara diam-diam membatalkan cache. Tanpa diagnostik cache, satu-satunya sinyal adalah `usage.cache_read_input_tokens` yang turun menjadi nol, tanpa indikasi apa yang berubah.

Diagnostik cache menutup celah tersebut. Berikan `id` dari respons Anda sebelumnya, dan API akan membandingkan kedua permintaan dan memberi tahu Anda di mana keduanya menyimpang (model, prompt sistem, alat, atau riwayat pesan) sehingga Anda dapat memperbaiki akar penyebabnya alih-alih menebak-nebak.

<Note>
  Diagnostik cache sedang dalam tahap beta. Sertakan [header beta](/docs/id/api/beta-headers) `cache-diagnosis-2026-04-07` dalam permintaan API Anda untuk menggunakan fitur ini.

  Diagnostik cache saat ini hanya tersedia di Claude API. Fitur ini tidak didukung di Amazon Bedrock atau Google Cloud.
</Note>

## Cara kerja diagnostik cache

Ketika header beta ada, API menyimpan fingerprint ringan dari setiap permintaan, yang dikunci oleh `id` respons. Pada permintaan Anda berikutnya, sertakan `id` tersebut sebagai `diagnostics.previous_message_id`. API membangun ulang fingerprint untuk permintaan baru, membandingkannya dengan yang tersimpan, dan melampirkan objek `diagnostics` ke respons yang menjelaskan titik divergensi pertama.

Perbandingan ini berkaitan dengan struktur permintaan, terlepas dari apakah cache benar-benar hit. Lihat [Membaca diagnostik bersama usage](#reading-diagnostics-alongside-usage) untuk cara menggabungkan hasil `diagnostics` dengan `usage.cache_read_input_tokens`.

Fingerprint hanya berisi hash dan estimasi jumlah token (tidak pernah konten prompt mentah), disimpan untuk waktu terbatas, dibatasi pada organisasi dan workspace Anda, dan tidak digunakan untuk tujuan lain apa pun.

## Penggunaan dasar

Kirim header beta pada setiap giliran. Pada giliran pertama, berikan `"previous_message_id": null` untuk ikut serta tanpa pesan sebelumnya untuk dibandingkan. Pada giliran berikutnya, berikan `id` dari respons sebelumnya.

<CodeGroup>
  ```bash cURL
  # Giliran 1: buat cache dan aktifkan diagnostik
  response=$(curl -sS --fail-with-body https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: cache-diagnosis-2026-04-07" \
    --header "content-type: application/json" \
    --data '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "cache_control": {"type": "ephemeral"},
      "system": "You are an AI assistant analyzing a large document. <document>...</document>",
      "messages": [{"role": "user", "content": "Summarize section 1."}],
      "diagnostics": {"previous_message_id": null}
    }')
  jq '{id, diagnostics}' <<< "$response"
  message_id=$(jq -r '.id' <<< "$response")

  # Giliran 2: rujuk giliran sebelumnya agar API dapat membandingkan prefiks
  curl -sS --fail-with-body https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: cache-diagnosis-2026-04-07" \
    --header "content-type: application/json" \
    --data @- <<EOF | jq '{id, diagnostics}'  # diagnostics: null means no divergence was found
  {
    "model": "claude-opus-5",
    "max_tokens": 1024,
    "cache_control": {"type": "ephemeral"},
    "system": "You are an AI assistant analyzing a large document. <document>...</document>",
    "messages": [
      {"role": "user", "content": "Summarize section 1."},
      {"role": "assistant", "content": "Section 1 covers..."},
      {"role": "user", "content": "Now summarize section 2."}
    ],
    "diagnostics": {"previous_message_id": "$message_id"}
  }
  EOF
  ```

  ```bash CLI
  # Giliran 1
  turn1=$(ant beta:messages create \
    --beta cache-diagnosis-2026-04-07 \
    --transform '{id,usage,diagnostics}' <<'YAML'
  model: claude-opus-5
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
  )
  printf '%s\n' "$turn1"

  # Giliran 2: teruskan id dari giliran 1 sebagai previous_message_id
  message_id=$(jq -r '.id' <<<"$turn1")
  ant beta:messages create \
    --beta cache-diagnosis-2026-04-07 \
    --transform '{id,usage,diagnostics}' <<YAML
  model: claude-opus-5
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
      model="claude-opus-5",
      max_tokens=1024,
      cache_control={"type": "ephemeral"},
      system=SYSTEM,
      messages=[{"role": "user", "content": "Summarize section 1."}],
      diagnostics={"previous_message_id": None},
      betas=["cache-diagnosis-2026-04-07"],
  )

  # Giliran 2: rujuk id respons sebelumnya
  r2 = client.beta.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      cache_control={"type": "ephemeral"},
      system=SYSTEM,
      messages=[
          {"role": "user", "content": "Summarize section 1."},
          {"role": "assistant", "content": r1.content},
          {"role": "user", "content": "Now summarize section 2."},
      ],
      diagnostics={"previous_message_id": r1.id},
      betas=["cache-diagnosis-2026-04-07"],
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
    model: "claude-opus-5",
    max_tokens: 1024,
    cache_control: { type: "ephemeral" },
    system: SYSTEM,
    messages: [{ role: "user", content: "Summarize section 1." }],
    diagnostics: { previous_message_id: null },
    betas: ["cache-diagnosis-2026-04-07"]
  });

  // Giliran 2: rujuk id respons sebelumnya
  const r2 = await client.beta.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    cache_control: { type: "ephemeral" },
    system: SYSTEM,
    messages: [
      { role: "user", content: "Summarize section 1." },
      { role: "assistant", content: r1.content },
      { role: "user", content: "Now summarize section 2." }
    ],
    diagnostics: { previous_message_id: r1.id },
    betas: ["cache-diagnosis-2026-04-07"]
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
  AnthropicClient client = new();

  var system = "You are an AI assistant analyzing a large document. <document>...</document>";

  var r1 = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeOpus5,
          MaxTokens = 1024,
          CacheControl = new(),
          System = system,
          Messages =
          [
              new() { Role = Role.User, Content = "Summarize section 1." },
          ],
          Diagnostics = new() { PreviousMessageID = null },
          Betas = [AnthropicBeta.CacheDiagnosis2026_04_07],
      }
  );

  var r2 = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeOpus5,
          MaxTokens = 1024,
          CacheControl = new(),
          System = system,
          Messages =
          [
              new() { Role = Role.User, Content = "Summarize section 1." },
              new()
              {
                  Role = Role.Assistant,
                  Content = r1.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
              },
              new() { Role = Role.User, Content = "Now summarize section 2." },
          ],
          Diagnostics = new() { PreviousMessageID = r1.ID },
          Betas = [AnthropicBeta.CacheDiagnosis2026_04_07],
      }
  );

  Console.WriteLine(r2.Diagnostics switch
  {
      null => "No divergence detected.",
      { CacheMissReason: null } => "Comparison still pending.",
      { CacheMissReason.Type: var type } => $"cache_miss_reason: {type.GetString()}",
  });
  ```

  ```go Go
  client := anthropic.NewClient()
  ctx := context.Background()

  system := []anthropic.BetaTextBlockParam{
  	{Text: "You are an AI assistant analyzing a large document. <document>...</document>"},
  }

  r1, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:        anthropic.ModelClaudeOpus5,
  	MaxTokens:    1024,
  	CacheControl: anthropic.BetaCacheControlEphemeralParam{},
  	System:       system,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Summarize section 1.")),
  	},
  	Diagnostics: anthropic.BetaDiagnosticsParam{
  		PreviousMessageID: param.Null[string](),
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaCacheDiagnosis2026_04_07},
  })
  if err != nil {
  	panic(err)
  }

  r2, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:        anthropic.ModelClaudeOpus5,
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
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaCacheDiagnosis2026_04_07},
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
  var client = AnthropicOkHttpClient.fromEnv();

  var system = "You are an AI assistant analyzing a large document. <document>...</document>";

  var r1 = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024)
          .cacheControl(BetaCacheControlEphemeral.builder().build())
          .system(system)
          .addUserMessage("Summarize section 1.")
          // Berikan null pada giliran pertama untuk ikut serta tanpa pesan sebelumnya sebagai pembanding.
          .diagnostics(BetaDiagnosticsParam.builder().previousMessageId((String) null).build())
          .addBeta(AnthropicBeta.CACHE_DIAGNOSIS_2026_04_07)
          .build()
  );

  var r2 = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024)
          .cacheControl(BetaCacheControlEphemeral.builder().build())
          .system(system)
          .addUserMessage("Summarize section 1.")
          .addMessage(r1)
          .addUserMessage("Now summarize section 2.")
          .diagnostics(BetaDiagnosticsParam.builder().previousMessageId(r1.id()).build())
          .addBeta(AnthropicBeta.CACHE_DIAGNOSIS_2026_04_07)
          .build()
  );

  if (r2.diagnostics().isEmpty()) {
      IO.println("No divergence detected.");
  } else if (r2.diagnostics().get().cacheMissReason().isEmpty()) {
      IO.println("Comparison still pending.");
  } else {
      var reason = r2.diagnostics().get().cacheMissReason().get();
      // CacheMissReason tidak menyediakan accessor .type() yang bertipe; baca dari JSON mentahnya.
      @SuppressWarnings("unchecked")
      var json = (Map<String, JsonValue>) reason._json().orElseThrow().asObject().orElseThrow();
      IO.println("cache_miss_reason: " + json.get("type").asStringOrThrow());
  }
  ```

  ```php PHP
  $client = new Client();

  $system = 'You are an AI assistant analyzing a large document. <document>...</document>';

  $r1 = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5,
      maxTokens: 1024,
      cacheControl: new BetaCacheControlEphemeral,
      system: $system,
      messages: [
          ['role' => 'user', 'content' => 'Summarize section 1.'],
      ],
      diagnostics: (new BetaDiagnosticsParam)->withPreviousMessageID(null),
      betas: [AnthropicBeta::CACHE_DIAGNOSIS_2026_04_07],
  );

  $r2 = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5,
      maxTokens: 1024,
      cacheControl: new BetaCacheControlEphemeral,
      system: $system,
      messages: [
          ['role' => 'user', 'content' => 'Summarize section 1.'],
          ['role' => 'assistant', 'content' => $r1->content],
          ['role' => 'user', 'content' => 'Now summarize section 2.'],
      ],
      diagnostics: (new BetaDiagnosticsParam)->withPreviousMessageID($r1->id),
      betas: [AnthropicBeta::CACHE_DIAGNOSIS_2026_04_07],
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
    model: :"claude-opus-5",
    max_tokens: 1024,
    cache_control: {type: "ephemeral"},
    system_: SYSTEM,
    messages: [
      {role: "user", content: "Summarize section 1."}
    ],
    diagnostics: {previous_message_id: nil},
    betas: ["cache-diagnosis-2026-04-07"]
  )

  r2 = client.beta.messages.create(
    model: :"claude-opus-5",
    max_tokens: 1024,
    cache_control: {type: "ephemeral"},
    system_: SYSTEM,
    messages: [
      {role: "user", content: "Summarize section 1."},
      {role: "assistant", content: r1.content},
      {role: "user", content: "Now summarize section 2."}
    ],
    diagnostics: {previous_message_id: r1.id},
    betas: ["cache-diagnosis-2026-04-07"]
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
  # Giliran 2: streaming respons. diagnostik tiba pada event message_start;
  # nilai null berarti tidak ditemukan divergensi.
  curl -sS --fail-with-body https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: cache-diagnosis-2026-04-07" \
    --header "content-type: application/json" \
    --data @- <<EOF | jq -R 'select(startswith("data: ")) | ltrimstr("data: ") | fromjson | select(.type == "message_start") | .message.diagnostics'
  {
    "model": "claude-opus-5",
    "max_tokens": 1024,
    "stream": true,
    "cache_control": {"type": "ephemeral"},
    "system": "You are an AI assistant analyzing a large document. <document>...</document>",
    "messages": [
      {"role": "user", "content": "Summarize section 1."},
      {"role": "assistant", "content": "Section 1 covers..."},
      {"role": "user", "content": "Now summarize section 2."}
    ],
    "diagnostics": {"previous_message_id": "$message_id"}
  }
  EOF
  ```

  ```bash CLI
  # Giliran 2: stream. Dengan --stream, CLI mengeluarkan setiap event SSE sebagai satu objek JSON.
  # diagnostics tiba pada event message_start; ambil dengan jq.
  ant beta:messages create \
    --beta cache-diagnosis-2026-04-07 \
    --stream --format jsonl <<YAML |
  model: claude-opus-5
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
    jq -c 'select(.type == "message_start") | .message | {id,usage,diagnostics}'
  ```

  ```python Python
  # Giliran 2: streaming, dengan merujuk id respons sebelumnya
  with client.beta.messages.stream(
      model="claude-opus-5",
      max_tokens=1024,
      cache_control={"type": "ephemeral"},
      system=SYSTEM,
      messages=[
          {"role": "user", "content": "Summarize section 1."},
          {"role": "assistant", "content": r1.content},
          {"role": "user", "content": "Now summarize section 2."},
      ],
      diagnostics={"previous_message_id": r1.id},
      betas=["cache-diagnosis-2026-04-07"],
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
    model: "claude-opus-5",
    max_tokens: 1024,
    cache_control: { type: "ephemeral" },
    system: SYSTEM,
    messages: [
      { role: "user", content: "Summarize section 1." },
      { role: "assistant", content: r1.content },
      { role: "user", content: "Now summarize section 2." }
    ],
    diagnostics: { previous_message_id: r1.id },
    betas: ["cache-diagnosis-2026-04-07"]
  });

  for await (const event of stream) {
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
  process.stdout.write("\n");

  // diagnostics tiba pada message_start dan dibawa hingga pesan akhir
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
  // Giliran 2: streaming, merujuk ke id respons sebelumnya
  BetaDiagnostics? diagnostics = null;

  var stream = client.Beta.Messages.CreateStreaming(
      new()
      {
          Model = Messages::Model.ClaudeOpus5,
          MaxTokens = 1024,
          CacheControl = new(),
          System = system,
          Messages =
          [
              new() { Role = Role.User, Content = "Summarize section 1." },
              new()
              {
                  Role = Role.Assistant,
                  Content = r1.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
              },
              new() { Role = Role.User, Content = "Now summarize section 2." },
          ],
          Diagnostics = new() { PreviousMessageID = r1.ID },
          Betas = [AnthropicBeta.CacheDiagnosis2026_04_07],
      }
  );

  await foreach (var streamEvent in stream)
  {
      if (streamEvent.TryPickStart(out var start))
      {
          // diagnostics tiba pada event message_start
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
      { CacheMissReason.Type: var type } => $"cache_miss_reason: {type.GetString()}",
  });
  ```

  ```go Go
  // Giliran 2: streaming, merujuk ke id respons sebelumnya
  stream := client.Beta.Messages.NewStreaming(ctx, anthropic.BetaMessageNewParams{
  	Model:        anthropic.ModelClaudeOpus5,
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
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaCacheDiagnosis2026_04_07},
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
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(1024)
      .cacheControl(BetaCacheControlEphemeral.builder().build())
      .system(system)
      .addUserMessage("Summarize section 1.")
      .addMessage(r1)
      .addUserMessage("Now summarize section 2.")
      .diagnostics(BetaDiagnosticsParam.builder().previousMessageId(r1.id()).build())
      .addBeta(AnthropicBeta.CACHE_DIAGNOSIS_2026_04_07)
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
      // CacheMissReason tidak menyediakan aksesor .type() bertipe; baca nilainya dari JSON mentah.
      @SuppressWarnings("unchecked")
      var json = (Map<String, JsonValue>) reason._json().orElseThrow().asObject().orElseThrow();
      IO.println("cache_miss_reason: " + json.get("type").asStringOrThrow());
  }
  ```

  ```php PHP
  // Giliran 2: streaming, merujuk ke id respons sebelumnya
  $stream = $client->beta->messages->createStream(
      model: Model::CLAUDE_OPUS_5,
      maxTokens: 1024,
      cacheControl: new BetaCacheControlEphemeral,
      system: $system,
      messages: [
          ['role' => 'user', 'content' => 'Summarize section 1.'],
          ['role' => 'assistant', 'content' => $r1->content],
          ['role' => 'user', 'content' => 'Now summarize section 2.'],
      ],
      diagnostics: (new BetaDiagnosticsParam)->withPreviousMessageID($r1->id),
      betas: [AnthropicBeta::CACHE_DIAGNOSIS_2026_04_07],
  );

  $diagnostics = null;
  foreach ($stream as $event) {
      if ($event instanceof BetaRawMessageStartEvent) {
          // diagnostics tiba pada BetaMessage yang disematkan dalam event message_start
          $diagnostics = $event->message->diagnostics;
      } elseif ($event instanceof BetaRawContentBlockDeltaEvent && $event->delta instanceof BetaTextDelta) {
          echo $event->delta->text;
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
    model: :"claude-opus-5",
    max_tokens: 1024,
    cache_control: {type: "ephemeral"},
    system_: SYSTEM,
    messages: [
      {role: "user", content: "Summarize section 1."},
      {role: "assistant", content: r1.content},
      {role: "user", content: "Now summarize section 2."}
    ],
    diagnostics: {previous_message_id: r1.id},
    betas: ["cache-diagnosis-2026-04-07"]
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

Event `message_start` membawa field `diagnostics` lengkap; lihat [Format respons](#response-format) untuk nilai-nilai yang mungkin.

## Meneruskan diagnostik melalui loop percakapan

Dalam percakapan multi-giliran, teruskan `id` respons terbaru sebagai `previous_message_id` pada setiap giliran. Iterasi pertama memberikan `null` untuk ikut serta; setiap iterasi berikutnya memberikan `id` dari respons sebelumnya.

<Tabs>
  <Tab title="cURL">
    <Info>
      Alur kerja ini tidak cocok diterjemahkan ke perintah shell sekali jalan. Lihat tab SDK untuk pola loop; permintaan HTTP per giliran identik dengan [Penggunaan dasar](#basic-usage).
    </Info>
  </Tab>

  <Tab title="CLI">
    <Info>
      Alur kerja ini tidak cocok diterjemahkan ke perintah shell sekali jalan. Lihat tab SDK untuk pola loop; pemanggilan CLI per giliran identik dengan [Penggunaan dasar](#basic-usage).
    </Info>
  </Tab>

  <Tab title="Python">
    ```python
    client = anthropic.Anthropic()

    SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>"

    messages = []
    prev_id = None

    for i, user_message in enumerate(
        ["Summarize section 1.", "Now section 2.", "Now section 3."]
    ):
        messages.append({"role": "user", "content": user_message})

        r = client.beta.messages.create(
            model="claude-opus-5",
            max_tokens=1024,
            cache_control={"type": "ephemeral"},
            system=SYSTEM,
            messages=messages,
            diagnostics={"previous_message_id": prev_id},
            betas=["cache-diagnosis-2026-04-07"],
        )

        if r.diagnostics is not None and r.diagnostics.cache_miss_reason is not None:
            print(f"Turn {i + 1} cache_miss_reason: {r.diagnostics.cache_miss_reason.type}")

        messages.append({"role": "assistant", "content": r.content})
        prev_id = r.id
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
    const client = new Anthropic();

    const SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>";

    const prompts = ["Summarize section 1.", "Now section 2.", "Now section 3."];

    const messages: BetaMessageParam[] = [];
    let prevId: string | null = null;

    for (const [i, prompt] of prompts.entries()) {
      messages.push({ role: "user", content: prompt });

      const r: BetaMessage = await client.beta.messages.create({
        model: "claude-opus-5",
        max_tokens: 1024,
        cache_control: { type: "ephemeral" },
        system: SYSTEM,
        messages,
        diagnostics: { previous_message_id: prevId },
        betas: ["cache-diagnosis-2026-04-07"]
      });

      if (r.diagnostics?.cache_miss_reason) {
        console.log(`Turn ${i + 1} cache_miss_reason: ${r.diagnostics.cache_miss_reason.type}`);
      }

      messages.push({ role: "assistant", content: r.content });
      prevId = r.id;
    }
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    AnthropicClient client = new();

    var system = "You are an AI assistant analyzing a large document. <document>...</document>";

    List<BetaMessageParam> messages = [];
    string? prevId = null;
    string[] prompts = ["Summarize section 1.", "Now section 2.", "Now section 3."];

    for (int i = 0; i < prompts.Length; i++)
    {
        messages.Add(new() { Role = Role.User, Content = prompts[i] });

        var r = await client.Beta.Messages.Create(
            new()
            {
                Model = Messages::Model.ClaudeOpus5,
                MaxTokens = 1024,
                CacheControl = new(),
                System = system,
                Messages = messages,
                Diagnostics = new() { PreviousMessageID = prevId },
                Betas = [AnthropicBeta.CacheDiagnosis2026_04_07],
            }
        );

        if (r.Diagnostics?.CacheMissReason is { Type: var type })
        {
            Console.WriteLine($"Turn {i + 1} cache_miss_reason: {type.GetString()}");
        }

        messages.Add(
            new()
            {
                Role = Role.Assistant,
                Content = r.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
            }
        );
        prevId = r.ID;
    }
    ```
  </Tab>

  <Tab title="Go">
    ```go
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

    	r, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
    		Model:        anthropic.ModelClaudeOpus5,
    		MaxTokens:    1024,
    		CacheControl: anthropic.BetaCacheControlEphemeralParam{},
    		System:       system,
    		Messages:     messages,
    		Diagnostics: anthropic.BetaDiagnosticsParam{
    			PreviousMessageID: prevID,
    		},
    		Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaCacheDiagnosis2026_04_07},
    	})
    	if err != nil {
    		panic(err)
    	}

    	if r.JSON.Diagnostics.Valid() && r.Diagnostics.JSON.CacheMissReason.Valid() {
    		fmt.Printf("Turn %d cache_miss_reason: %s\n", turn+1, r.Diagnostics.CacheMissReason.Type)
    	}

    	messages = append(messages, r.ToParam())
    	prevID = anthropic.String(r.ID)
    }
    ```
  </Tab>

  <Tab title="Java">
    ```java
    var client = AnthropicOkHttpClient.fromEnv();

    var system = "You are an AI assistant analyzing a large document. <document>...</document>";
    var prompts = List.of("Summarize section 1.", "Now section 2.", "Now section 3.");

    var messages = new ArrayList<BetaMessageParam>();
    String prevId = null;

    for (var turn = 0; turn < prompts.size(); turn++) {
        messages.add(
            BetaMessageParam.builder()
                .role(BetaMessageParam.Role.USER)
                .content(prompts.get(turn))
                .build()
        );

        var r = client.beta().messages().create(
            MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_5)
                .maxTokens(1024)
                .cacheControl(BetaCacheControlEphemeral.builder().build())
                .system(system)
                .messages(messages)
                .diagnostics(BetaDiagnosticsParam.builder().previousMessageId(prevId).build())
                .addBeta(AnthropicBeta.CACHE_DIAGNOSIS_2026_04_07)
                .build()
        );

        if (r.diagnostics().isPresent() && r.diagnostics().get().cacheMissReason().isPresent()) {
            var reason = r.diagnostics().get().cacheMissReason().get();
            // CacheMissReason tidak menyediakan accessor .type() yang bertipe; baca dari JSON mentahnya.
            @SuppressWarnings("unchecked")
            var json = (Map<String, JsonValue>) reason._json().orElseThrow().asObject().orElseThrow();
            IO.println("Turn " + (turn + 1) + " cache_miss_reason: " + json.get("type").asStringOrThrow());
        }

        messages.add(r.toParam());
        prevId = r.id();
    }
    ```
  </Tab>

  <Tab title="PHP">
    ```php
    $client = new Client();

    $system = 'You are an AI assistant analyzing a large document. <document>...</document>';

    $messages = [];
    $prevId = null;

    foreach (['Summarize section 1.', 'Now section 2.', 'Now section 3.'] as $i => $userMsg) {
        $turn = $i + 1;
        $messages[] = ['role' => 'user', 'content' => $userMsg];

        $r = $client->beta->messages->create(
            model: Model::CLAUDE_OPUS_5,
            maxTokens: 1024,
            cacheControl: new BetaCacheControlEphemeral,
            system: $system,
            messages: $messages,
            diagnostics: (new BetaDiagnosticsParam)->withPreviousMessageID($prevId),
            betas: [AnthropicBeta::CACHE_DIAGNOSIS_2026_04_07],
        );

        if ($r->diagnostics?->cacheMissReason !== null) {
            echo "Turn {$turn} cache_miss_reason: {$r->diagnostics->cacheMissReason->type}\n";
        }

        $messages[] = ['role' => 'assistant', 'content' => $r->content];
        $prevId = $r->id;
    }
    ```
  </Tab>

  <Tab title="Ruby">
    ```ruby
    client = Anthropic::Client.new

    SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>"

    messages = []
    prev_id = nil

    ["Summarize section 1.", "Now section 2.", "Now section 3."].each_with_index do |user_msg, i|
      messages << {role: "user", content: user_msg}

      r = client.beta.messages.create(
        model: :"claude-opus-5",
        max_tokens: 1024,
        cache_control: {type: "ephemeral"},
        system_: SYSTEM,
        messages: messages,
        diagnostics: {previous_message_id: prev_id},
        betas: ["cache-diagnosis-2026-04-07"]
      )

      if (reason = r.diagnostics&.cache_miss_reason)
        puts "Turn #{i + 1} cache_miss_reason: #{reason.type}"
      end

      messages << {role: "assistant", content: r.content}
      prev_id = r.id
    end
    ```
  </Tab>
</Tabs>

## Format respons

Field `diagnostics` pada `Message` respons memiliki empat kemungkinan status:

| Nilai                          | Arti                                                                                                                                                                                                                       |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| field tidak ada                | Permintaan tidak menyertakan `diagnostics`, atau header beta tidak ada.                                                                                                                                                    |
| `null`                         | Entah `previous_message_id` bernilai `null` (giliran pertama, tidak ada yang dibandingkan), atau perbandingan telah dijalankan dan tidak menemukan divergensi.                                                             |
| `{"cache_miss_reason": null}`  | Perbandingan masih berjalan ketika respons diserialisasi. Ini dapat terjadi ketika respons dimulai dengan sangat cepat. Perlakukan sebagai tidak konklusif dan periksa giliran berikutnya.                                 |
| `{"cache_miss_reason": {...}}` | Sebuah `cache_miss_reason` dilampirkan. Untuk tipe `*_changed`, ini mengidentifikasi titik divergensi pertama; `previous_message_not_found` dan `unavailable` adalah kasus di mana tidak ada perbandingan yang dihasilkan. |

Ketika `cache_miss_reason` tidak null, tampilannya seperti ini:

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

| Tipe                         | Artinya                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Apa yang harus diubah                                                                                                                                                                                                                                                                                |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model_changed`              | `model` berbeda dari permintaan sebelumnya (misalnya, router, uji A/B, atau fallback memilih model yang berbeda). Cache bersifat per-model.                                                                                                                                                                                                                                                                                                                          | Pertahankan model tetap konstan dalam percakapan yang di-cache.                                                                                                                                                                                                                                      |
| `system_changed`             | Parameter `system` berbeda. Biasanya timestamp, ID permintaan, atau nilai per-permintaan lainnya diinterpolasi ke dalam prompt sistem.                                                                                                                                                                                                                                                                                                                               | Jadikan prompt sistem sebagai konstanta yang stabil secara byte dan pindahkan data dinamis ke pesan `user` pertama setelah breakpoint cache Anda.                                                                                                                                                    |
| `tools_changed`              | Array `tools` berbeda: alat ditambahkan, dihapus, atau diurutkan ulang antar giliran, atau JSON `input_schema` alat diserialisasi secara non-deterministik.                                                                                                                                                                                                                                                                                                          | Kirim daftar alat yang sama pada setiap giliran dalam urutan tetap dengan skema yang diserialisasi secara deterministik (misalnya, urutkan key).                                                                                                                                                     |
| `messages_changed`           | Model, system, dan tools semuanya cocok, tetapi entri sebelumnya dalam `messages` diubah, diurutkan ulang, atau dihapus alih-alih ditambahkan. Biasanya riwayat percakapan dipotong atau diedit, atau giliran assistant dan blok `tool_result` diserialisasi ulang secara berbeda saat dikirim ulang.                                                                                                                                                                | Perlakukan riwayat sebagai append-only; kirim kembali `content` assistant dan hasil alat secara verbatim.                                                                                                                                                                                            |
| `previous_message_not_found` | Tidak ada fingerprint tersimpan untuk `previous_message_id` yang diberikan. Ini bukan bukti bahwa permintaan Anda berubah. Biasanya permintaan sebelumnya tidak membawa header beta, berasal dari workspace yang berbeda, atau terlalu banyak waktu telah berlalu sejak dikirim.                                                                                                                                                                                     | Kirim header beta pada setiap giliran dan jaga agar giliran berurutan berdekatan dalam waktu.                                                                                                                                                                                                        |
| `unavailable`                | Informasi diagnostik tidak tersedia untuk permintaan ini. Ini termasuk kasus di mana `model`, `system`, dan `tools` cocok tetapi parameter permintaan lain yang memengaruhi prompt (`tool_choice`, `thinking`, `context_management`, `output_config`, `output_format`, atau kumpulan header `anthropic-beta` yang aktif) berbeda, dan percakapan yang sangat panjang di mana divergensi berada di luar horizon perbandingan. Permintaan Anda diproses secara normal. | Jaga agar parameter permintaan yang memengaruhi prompt tetap konstan selama masa hidup percakapan yang di-cache. Jika persisten, terapkan pemeriksaan manual di bawah [Pemecahan masalah umum](/docs/id/build-with-claude/prompt-caching#troubleshooting-common-issues) pada halaman caching prompt. |

<Note>
  Keempat tipe `*_changed` juga membawa integer `cache_missed_input_tokens`: estimasi berapa banyak token input yang jatuh setelah titik divergensi, memberi Anda gambaran seberapa banyak prefiks yang dapat di-cache telah hilang. Nilai ini diturunkan dari panjang byte sebelum tokenisasi, jadi perlakukan sebagai indikator besaran alih-alih angka penagihan. Nilai ini dapat berbeda dari (dan terkadang melebihi) `usage.input_tokens`.
</Note>

## Membaca diagnostik bersama usage

`diagnostics` menjawab "apakah permintaan saya berubah?" sementara `usage.cache_read_input_tokens` menjawab "apakah cache hit?". Menggabungkan keduanya memberi tahu Anda di mana harus mencari.

Matriks ini berlaku untuk giliran di mana Anda memberikan `previous_message_id` yang sebenarnya. Pada giliran pertama (`previous_message_id: null`), `diagnostics` selalu `null` dan `cache_read_input_tokens` biasanya nol karena cache sedang ditulis, bukan dibaca; tidak diperlukan pemecahan masalah. Matriks ini juga tidak berlaku ketika `cache_miss_reason` bernilai `null` (perbandingan masih tertunda; periksa giliran berikutnya) atau ketika `type`-nya adalah `previous_message_not_found` atau `unavailable` (tidak ada perbandingan yang dihasilkan).

| Hasil diagnostik                            | Token cache read | Interpretasi                                                                                                                                                                                                            |
| ------------------------------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `null`                                      | tinggi           | Bekerja sesuai harapan. Prefiks Anda stabil dan cache hit.                                                                                                                                                              |
| `null`                                      | rendah atau nol  | Permintaan Anda cocok tetapi entri cache tidak lagi tersedia. Pertimbangkan untuk mempersingkat jeda antar giliran atau menggunakan [TTL cache 1 jam](/docs/id/build-with-claude/prompt-caching#1-hour-cache-duration). |
| `cache_miss_reason` adalah tipe `*_changed` | rendah atau nol  | Bug Anda. Permintaan berubah; perbaiki penyebab yang ditunjukkan oleh `type`.                                                                                                                                           |
| `cache_miss_reason` adalah tipe `*_changed` | tinggi           | Jarang terjadi. Perubahan terjadi di akhir prompt tetapi breakpoint `cache_control` sebelumnya masih hit. Layak diperbaiki, tetapi dampaknya rendah.                                                                    |

## Keterbatasan

* **Beta:** Nama field dan semantik dapat berubah sebelum ketersediaan umum.
* **Hanya Claude API:** Tidak tersedia di Amazon Bedrock atau Google Cloud.
* **Retensi terbatas:** Fingerprint untuk pencarian `previous_message_id` kedaluwarsa setelah periode singkat. Jalankan perbandingan diagnostik antara permintaan yang berjarak dekat.
* **Workspace yang sama:** Permintaan sebelumnya harus dibuat dengan kunci API dari organisasi dan workspace yang sama.
* **Horizon perbandingan:** Untuk percakapan yang sangat panjang di mana satu-satunya perubahan berada jauh di dalam daftar pesan, respons mungkin berupa `unavailable` alih-alih lokasi yang tepat.
* **Best-effort:** Diagnostik tidak pernah memblokir atau menggagalkan permintaan Anda. Jika informasi diagnostik tidak tersedia, respons mengembalikan `unavailable`, atau `cache_miss_reason: null` ketika perbandingan masih berjalan.

## Retensi data

Diagnostik cache memenuhi syarat ZDR (qualified). Anthropic tidak menyimpan teks mentah dari prompt Anda atau output Claude untuk fitur ini.

Fingerprint yang disimpan untuk setiap permintaan hanya terdiri dari hash kriptografis dan estimasi jumlah token, dikunci oleh `id` respons dan dibatasi pada organisasi dan workspace Anda. Fingerprint kedaluwarsa setelah periode singkat dan tidak digunakan untuk tujuan lain apa pun.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).

## Lihat juga

* [Prompt caching](/docs/id/build-with-claude/prompt-caching)
* [Penghitungan token](/docs/id/build-with-claude/token-counting)
* [Header beta](/docs/id/api/beta-headers)
