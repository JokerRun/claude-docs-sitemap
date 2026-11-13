---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/message-threads
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: 5d0c2cdb2d9c9ef84828fff30233044dcb5852c199a827199f381b11d7a8bdff
---

---
title: Thread pesan
url: https://platform.claude.com/docs/id/build-with-claude/message-threads
description: Berikan waktu hingga token pertama yang lebih cepat kepada agen yang berjalan lama, terutama dalam percakapan panjang, dengan hanya mengirimkan pesan baru pada setiap permintaan.
featureMetadata:
  status: beta
  betaHeader: message-threads-2026-08-12
  zdr:
    eligibility: not-eligible
    note: Isi thread (percakapan, prompt sistem, dan alat) disimpan di memori, dienkripsi dengan kunci yang dikelola server, tidak pernah ditulis ke penyimpanan permanen, dan dihapus paling lambat 1 jam setelah thread terakhir digunakan. Menggunakan fitur ini tidak memengaruhi penggunaan Anda atas fitur lain yang memiliki kelayakan ZDR.
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
    Claude API: beta
    Claude Platform on AWS: beta
    Claude Models on Google Cloud (Anthropic managed): beta
    Microsoft Foundry: beta
---

Dengan “message thread” (thread pesan), permintaan menjadi lebih kecil, dan “time to first token” (waktu hingga token pertama) tetap lebih rendah dan lebih stabil seiring bertambahnya percakapan. Thread paling membantu dalam loop agen yang panjang. Tanpa thread, setiap giliran mengunggah ulang seluruh percakapan, dan API memvalidasi serta melakukan tokenisasi ulang terhadap semuanya. Dengan thread, sebagian besar pekerjaan tersebut hanya mencakup giliran baru.

“Message thread” (thread pesan) menyimpan percakapan di server untuk waktu yang singkat. Anda mengirimkan percakapan lengkap satu kali, beserta prompt sistem dan alat Anda. Pada setiap giliran berikutnya, Anda hanya mengirimkan pesan-pesan baru dan `id` dari respons sebelumnya. API membangun ulang percakapan sebelum memanggil model. Anda menambahkan satu parameter, `thread`, ke permintaan [Messages API](https://platform.claude.com/docs/id/api/messages). Responsnya adalah pesan seperti biasa.

<Note>
  Thread pesan berbeda dari [thread sesi](https://platform.claude.com/docs/id/managed-agents/session-threads) di Claude Managed Agents.
</Note>

## Cara kerja thread pesan

* **Buat.** Kirim permintaan pertama Anda seperti yang Anda lakukan saat ini, dengan percakapan lengkap, `system`, dan `tools`, lalu tambahkan `"thread": {"type": "create"}`. API menyimpan percakapan, termasuk balasan Claude, di bawah `id` respons.
* **Lanjutkan.** Kirim hanya pesan-pesan sejak respons sebelumnya, lalu tambahkan `"thread": {"type": "continue", "previous_message_id": "<previous id>"}`. Jangan sertakan `system` dan `tools` dalam permintaan. Thread mempertahankan nilai-nilai dari permintaan create. Gunakan setiap `id` respons baru untuk giliran berikutnya.
* **Putar ulang.** Thread bersifat best-effort. Thread kedaluwarsa 5 menit setelah permintaan terakhirnya, dan API menghapusnya paling lambat 1 jam setelah penggunaan terakhirnya. Setiap respons yang disimpan API memulai ulang waktu 5 menit tersebut. Jika API tidak lagi dapat melanjutkan thread, permintaan continue akan mengembalikan error 404. Kirim kembali percakapan lengkap dalam permintaan create baru, dan lanjutkan dari `id` respons tersebut. Helper thread SDK melakukan pemutaran ulang ini untuk Anda (lihat [Cara kerja helper SDK](https://platform.claude.com/docs/id/build-with-claude/message-threads#sdk-helper-handles)). Setelah respons dari model fallback, lihat [Menggunakan fallback dengan thread](https://platform.claude.com/docs/id/build-with-claude/message-threads#fallbacks).

Aplikasi Anda tetap menjadi sumber kebenaran untuk percakapan. Simpan salinan Anda sendiri dari setiap pesan, dan bangun [jalur pemutaran ulang](https://platform.claude.com/docs/id/build-with-claude/message-threads#recover) sejak awal. Tidak ada respons, baik untuk permintaan create maupun continue, yang menyatakan apakah API menyimpan giliran tersebut. Anda baru mengetahuinya pada permintaan continue berikutnya. Helper thread SDK menyimpan salinan ini di memori selama objek helper tersebut ada, dan tidak menyimpannya di tempat lain. Jika percakapan harus bertahan lebih lama dari proses Anda, simpan salinan Anda sendiri.

## Menggunakan thread dengan SDK

SDK memiliki helper thread yang membangun permintaan thread untuk Anda. Buat helper tersebut dengan field yang sama seperti permintaan Messages, lalu kirimkan satu giliran pada satu waktu. Helper menyimpan percakapan lengkap di memori.

Contoh ini memiliki dua giliran. Helper membuat thread pada giliran pertama dan melanjutkannya pada giliran kedua, serta menambahkan header beta untuk Anda. `cache_control` tingkat atas bersifat opsional. Field ini meminta caching prompt pada setiap giliran (lihat [Caching prompt pada thread](https://platform.claude.com/docs/id/build-with-claude/message-threads#prompt-caching)). Tanpanya, setiap giliran berikutnya tetap hanya mengirimkan pesan-pesan baru, tetapi tidak ada yang di-cache kecuali Anda menambahkan breakpoint cache sendiri.

<CodeGroup exclude="shell">
  ```python Python
  client = anthropic.Anthropic()

  # Buat helper. Panggilan ini tidak mengirim permintaan apa pun.
  thread = client.beta.messages.thread(
      model="claude-opus-5-5",
      max_tokens=1024,
      cache_control={"type": "ephemeral"},
      system="You are a support agent for Acme. Keep replies short.",
  )

  # Giliran 1: helper membuat thread dan mengirim seluruh percakapan
  thread.send({"role": "user", "content": "Hi! I have a question about an order."})

  # Giliran 2: helper melanjutkan thread dan hanya mengirim pesan baru
  second = thread.send(
      {"role": "user", "content": "How long does standard shipping usually take?"}
  )

  for block in second.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Buat helper. Panggilan ini tidak mengirim permintaan.
  const thread = client.beta.messages.thread({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    cache_control: { type: "ephemeral" },
    system: "You are a support agent for Acme. Keep replies short."
  });

  // Giliran 1: helper membuat thread dan mengirim seluruh percakapan
  await thread.send({ role: "user", content: "Hi! I have a question about an order." });

  // Giliran 2: helper melanjutkan thread dan hanya mengirim pesan baru
  const second = await thread.send({
    role: "user",
    content: "How long does standard shipping usually take?"
  });

  for (const block of second.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  using Anthropic.Helpers.Beta;

  AnthropicClient client = new();

  // Buat helper. Panggilan ini tidak mengirim permintaan apa pun.
  var thread = client.Beta.Messages.Thread(
      new ThreadCreateParams
      {
          Model = Messages::Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [],
          CacheControl = new(),
          System = "You are a support agent for Acme. Keep replies short.",
      }
  );

  // Giliran 1: helper membuat thread dan mengirim seluruh percakapan
  await thread.Send(
      new BetaUserMessageParam { Content = "Hi! I have a question about an order." }
  );

  // Giliran 2: helper melanjutkan thread dan hanya mengirim pesan baru
  var second = await thread.Send(
      new BetaUserMessageParam { Content = "How long does standard shipping usually take?" }
  );

  foreach (var block in second.Content)
  {
      if (block.TryPickText(out var textBlock))
      {
          Console.WriteLine(textBlock.Text);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()
  ctx := context.Background()

  // Buat helper. Panggilan ini tidak mengirim permintaan.
  thread := client.Beta.Messages.NewThread(anthropic.BetaMessageThreadCreateParams{
  	Model:        anthropic.ModelClaudeOpus5_5,
  	MaxTokens:    1024,
  	CacheControl: anthropic.NewBetaCacheControlEphemeralParam(),
  	System: []anthropic.BetaTextBlockParam{
  		{Text: "You are a support agent for Acme. Keep replies short."},
  	},
  })

  // Giliran 1: helper membuat thread dan mengirim seluruh percakapan
  _, err := thread.Send(ctx, anthropic.BetaMessageThreadSendParams{
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hi! I have a question about an order.")),
  	},
  })
  if err != nil {
  	panic(err)
  }

  // Giliran 2: helper melanjutkan thread dan hanya mengirim pesan baru
  second, err := thread.Send(ctx, anthropic.BetaMessageThreadSendParams{
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("How long does standard shipping usually take?")),
  	},
  })
  if err != nil {
  	panic(err)
  }

  for _, block := range second.Content {
  	if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  var client = AnthropicOkHttpClient.fromEnv();

  // Buat helper. Panggilan ini tidak mengirim permintaan apa pun.
  var thread = client.beta().messages().thread(
      ThreadCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          .cacheControl(BetaCacheControlEphemeral.builder().build())
          .system("You are a support agent for Acme. Keep replies short.")
          .build()
  );

  // Giliran 1: helper membuat thread dan mengirim seluruh percakapan
  thread.send("Hi! I have a question about an order.");

  // Giliran 2: helper melanjutkan thread dan hanya mengirim pesan baru
  var second = thread.send("How long does standard shipping usually take?");

  second.content().stream()
      .flatMap(block -> block.text().stream())
      .forEach(textBlock -> IO.println(textBlock.text()));
  ```

  ```php PHP
  $client = new Client();

  // Buat helper. Panggilan ini tidak mengirim permintaan apa pun.
  $thread = $client->beta->messages->thread(
      maxTokens: 1024,
      model: Model::CLAUDE_OPUS_5_5,
      cacheControl: new BetaCacheControlEphemeral,
      system: 'You are a support agent for Acme. Keep replies short.',
  );

  // Giliran 1: helper membuat thread dan mengirim seluruh percakapan
  $thread->send(['role' => 'user', 'content' => 'Hi! I have a question about an order.']);

  // Giliran 2: helper melanjutkan thread dan hanya mengirim pesan baru
  $second = $thread->send(['role' => 'user', 'content' => 'How long does standard shipping usually take?']);

  foreach ($second->content as $block) {
      if ($block instanceof \Anthropic\Beta\Messages\BetaTextBlock) {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Buat helper. Panggilan ini tidak mengirim permintaan apa pun.
  thread = client.beta.messages.thread(
    model: :"claude-opus-5-5",
    max_tokens: 1024,
    cache_control: {type: "ephemeral"},
    system_: "You are a support agent for Acme. Keep replies short."
  )

  # Giliran 1: helper membuat thread dan mengirim seluruh percakapan
  thread.send_message({role: "user", content: "Hi! I have a question about an order."})

  # Giliran 2: helper melanjutkan thread dan hanya mengirim pesan baru
  second = thread.send_message({role: "user", content: "How long does standard shipping usually take?"})

  second.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

## Mengirim field `thread` sendiri

Untuk membangun permintaan thread sendiri, misalnya dengan cURL, CLI, atau metode `create` biasa dari SDK, tambahkan field `thread` ke setiap permintaan.

Kirim header beta `message-threads-2026-08-12` pada setiap permintaan dalam sebuah thread.

Contoh ini membuat thread pada giliran pertama dan melanjutkannya pada giliran kedua. `cache_control` tingkat atas meminta caching prompt pada setiap giliran. Field ini berlaku setelah percakapan lebih panjang dari [panjang minimum yang dapat di-cache](https://platform.claude.com/docs/id/build-with-claude/prompt-caching).

<CodeGroup>
  ```bash cURL
  # Giliran 1: kirim seluruh percakapan dan buat thread
  curl -sS --fail-with-body https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: message-threads-2026-08-12" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "cache_control": {"type": "ephemeral"},
      "system": "You are a support agent for Acme. Keep replies short.",
      "messages": [{"role": "user", "content": "Hi! I have a question about an order."}],
      "thread": {"type": "create"}
    }'

  # Giliran 2: kirim hanya pesan baru. Atur message_id ke id respons giliran 1.
  # Jangan sertakan system dan tools: thread sudah menyimpannya.
  curl -sS --fail-with-body https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: message-threads-2026-08-12" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "cache_control": {"type": "ephemeral"},
      "messages": [{"role": "user", "content": "How long does standard shipping usually take?"}],
      "thread": {"type": "continue", "previous_message_id": "'"$message_id"'"}
    }'
  ```

  ```bash CLI
  # Giliran 1: kirim seluruh percakapan dan buat thread
  ant beta:messages create --beta message-threads-2026-08-12 <<'YAML'
  model: claude-opus-5-5
  max_tokens: 1024
  cache_control:
    type: ephemeral
  system: "You are a support agent for Acme. Keep replies short."
  messages:
    - role: user
      content: "Hi! I have a question about an order."
  thread:
    type: create
  YAML

  # Giliran 2: kirim hanya pesan baru. Atur message_id ke id respons giliran 1.
  # Jangan sertakan system dan tools: thread sudah menyimpannya.
  ant beta:messages create --beta message-threads-2026-08-12 <<YAML
  model: claude-opus-5-5
  max_tokens: 1024
  cache_control:
    type: ephemeral
  messages:
    - role: user
      content: "How long does standard shipping usually take?"
  thread:
    type: continue
    previous_message_id: $message_id
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  # Giliran 1: kirim seluruh percakapan dan buat thread
  first = client.beta.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      cache_control={"type": "ephemeral"},
      system="You are a support agent for Acme. Keep replies short.",
      messages=[{"role": "user", "content": "Hi! I have a question about an order."}],
      thread={"type": "create"},
      betas=["message-threads-2026-08-12"],
  )

  # Giliran 2: kirim hanya pesan baru dan id respons giliran 1.
  # Jangan sertakan system dan tools: thread sudah menyimpannya.
  second = client.beta.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      cache_control={"type": "ephemeral"},
      messages=[
          {"role": "user", "content": "How long does standard shipping usually take?"}
      ],
      thread={"type": "continue", "previous_message_id": first.id},
      betas=["message-threads-2026-08-12"],
  )

  for block in second.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Giliran 1: kirim seluruh percakapan dan buat thread
  const first = await client.beta.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    cache_control: { type: "ephemeral" },
    system: "You are a support agent for Acme. Keep replies short.",
    messages: [{ role: "user", content: "Hi! I have a question about an order." }],
    thread: { type: "create" },
    betas: ["message-threads-2026-08-12"]
  });

  // Giliran 2: kirim hanya pesan baru dan id respons giliran 1.
  // Jangan sertakan system dan tools: thread sudah menyimpannya.
  const second = await client.beta.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    cache_control: { type: "ephemeral" },
    messages: [{ role: "user", content: "How long does standard shipping usually take?" }],
    thread: { type: "continue", previous_message_id: first.id },
    betas: ["message-threads-2026-08-12"]
  });

  for (const block of second.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Giliran 1: kirim seluruh percakapan dan buat thread
  var first = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          CacheControl = new(),
          System = "You are a support agent for Acme. Keep replies short.",
          Messages =
          [
              new BetaUserMessageParam { Content = "Hi! I have a question about an order." },
          ],
          Thread = new BetaThreadCreateParams(),
          Betas = [AnthropicBeta.MessageThreads2026_08_12],
      }
  );

  // Giliran 2: kirim hanya pesan baru dan id respons giliran 1.
  // Jangan sertakan System dan Tools: thread sudah menyimpannya.
  var second = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          CacheControl = new(),
          Messages =
          [
              new BetaUserMessageParam { Content = "How long does standard shipping usually take?" },
          ],
          Thread = new BetaThreadContinueParams(first.ID),
          Betas = [AnthropicBeta.MessageThreads2026_08_12],
      }
  );

  foreach (var block in second.Content)
  {
      if (block.TryPickText(out var textBlock))
      {
          Console.WriteLine(textBlock.Text);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()
  ctx := context.Background()

  // Giliran 1: kirim seluruh percakapan dan buat thread
  threadCreate := anthropic.NewBetaThreadCreateParams()
  first, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:        anthropic.ModelClaudeOpus5_5,
  	MaxTokens:    1024,
  	CacheControl: anthropic.NewBetaCacheControlEphemeralParam(),
  	System: []anthropic.BetaTextBlockParam{
  		{Text: "You are a support agent for Acme. Keep replies short."},
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hi! I have a question about an order.")),
  	},
  	Thread: anthropic.BetaMessageThreadParamUnion{OfCreate: &threadCreate},
  	Betas:  []anthropic.AnthropicBeta{anthropic.AnthropicBetaMessageThreads2026_08_12},
  })
  if err != nil {
  	panic(err)
  }

  // Giliran 2: kirim hanya pesan baru dan id respons giliran 1.
  // Jangan sertakan System dan Tools: thread sudah menyimpannya.
  second, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:        anthropic.ModelClaudeOpus5_5,
  	MaxTokens:    1024,
  	CacheControl: anthropic.NewBetaCacheControlEphemeralParam(),
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("How long does standard shipping usually take?")),
  	},
  	Thread: anthropic.BetaMessageThreadParamOfContinue(first.ID),
  	Betas:  []anthropic.AnthropicBeta{anthropic.AnthropicBetaMessageThreads2026_08_12},
  })
  if err != nil {
  	panic(err)
  }

  for _, block := range second.Content {
  	if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  var client = AnthropicOkHttpClient.fromEnv();

  // Giliran 1: kirim seluruh percakapan dan buat thread
  var first = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          .cacheControl(BetaCacheControlEphemeral.builder().build())
          .system("You are a support agent for Acme. Keep replies short.")
          .addUserMessage("Hi! I have a question about an order.")
          .thread(BetaThreadCreateParams.builder().build())
          .addBeta(AnthropicBeta.MESSAGE_THREADS_2026_08_12)
          .build()
  );

  // Giliran 2: kirim hanya pesan baru dan id respons giliran 1.
  // Jangan sertakan system dan tools: thread sudah menyimpannya.
  var second = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          .cacheControl(BetaCacheControlEphemeral.builder().build())
          .addUserMessage("How long does standard shipping usually take?")
          .continueThread(first.id())
          .addBeta(AnthropicBeta.MESSAGE_THREADS_2026_08_12)
          .build()
  );

  second.content().stream()
      .flatMap(block -> block.text().stream())
      .forEach(textBlock -> IO.println(textBlock.text()));
  ```

  ```php PHP
  $client = new Client();

  // Giliran 1: kirim seluruh percakapan dan buat thread
  $first = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 1024,
      cacheControl: new BetaCacheControlEphemeral,
      system: 'You are a support agent for Acme. Keep replies short.',
      messages: [
          ['role' => 'user', 'content' => 'Hi! I have a question about an order.'],
      ],
      thread: BetaThreadCreateParams::with(),
      betas: ['message-threads-2026-08-12'],
  );

  // Giliran 2: kirim hanya pesan baru dan id respons giliran 1.
  // Jangan sertakan system dan tools: thread sudah menyimpannya.
  $second = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_5_5,
      maxTokens: 1024,
      cacheControl: new BetaCacheControlEphemeral,
      messages: [
          ['role' => 'user', 'content' => 'How long does standard shipping usually take?'],
      ],
      thread: BetaThreadContinueParams::with(previousMessageID: $first->id),
      betas: ['message-threads-2026-08-12'],
  );

  foreach ($second->content as $block) {
      if ($block instanceof \Anthropic\Beta\Messages\BetaTextBlock) {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Giliran 1: kirim seluruh percakapan dan buat thread
  first = client.beta.messages.create(
    model: :"claude-opus-5-5",
    max_tokens: 1024,
    cache_control: {type: "ephemeral"},
    system_: "You are a support agent for Acme. Keep replies short.",
    messages: [{role: "user", content: "Hi! I have a question about an order."}],
    thread: {type: "create"},
    betas: ["message-threads-2026-08-12"]
  )

  # Giliran 2: kirim hanya pesan baru dan id respons giliran 1.
  # Jangan sertakan system_ dan tools: thread sudah menyimpannya.
  second = client.beta.messages.create(
    model: :"claude-opus-5-5",
    max_tokens: 1024,
    cache_control: {type: "ephemeral"},
    messages: [{role: "user", content: "How long does standard shipping usually take?"}],
    thread: {type: "continue", previous_message_id: first.id},
    betas: ["message-threads-2026-08-12"]
  )

  second.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

## Apa yang dikirim pada setiap permintaan

| Grup          | Field                                                                                                                                                                                                                             | Aturan                                                                                                                                                                                                                                  |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Khusus create | `system`, `tools`                                                                                                                                                                                                                 | Kirim hanya pada permintaan create, beserta breakpoint `cache_control` apa pun pada field tersebut. Mengirim salah satunya pada permintaan continue, bahkan sebagai `null`, mengembalikan error 400.                                    |
| Tetap         | `model`, `tool_choice`, `thinking`, `mcp_servers` (selain token otorisasi setiap server), `context_management`, `output_config`, `skills` di dalam `container`, `cache_control` tingkat atas, dan kumpulan nilai `anthropic-beta` | Kirim pada setiap permintaan dalam thread, dengan nilai yang sama seperti pada permintaan create. Nilai yang berbeda mengembalikan error 400 dengan kode `thread_fingerprint_mismatch`, dan pesan error menyebutkan field yang berbeda. |
| Bebas         | `max_tokens`, `stop_sequences`, `stream`, `metadata`, `service_tier`, dan field lain yang tidak disebutkan di halaman ini                                                                                                         | Field ini dapat berubah dari giliran ke giliran.                                                                                                                                                                                        |

API tidak menyimpan URL server MCP, token otorisasi MCP, atau `id` container. Kirim `mcp_servers` dan `container` pada setiap permintaan yang menggunakannya. Token otorisasi MCP dapat berubah antar permintaan.

Helper thread SDK tidak menyertakan `system` dan `tools` dalam permintaan continue untuk Anda dan mengirim ulang field-field tetap pada setiap giliran.

Jika Anda menggunakan [fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback), kirim field `fallbacks` pada setiap permintaan dalam thread atau tidak sama sekali. Lihat [Menggunakan fallback dengan thread](https://platform.claude.com/docs/id/build-with-claude/message-threads#fallbacks).

Untuk mengubah field khusus create atau field tetap, mulai thread baru: kirim percakapan lengkap dalam permintaan create dengan nilai-nilai baru.

**Jika Anda mengubah `system` atau `tools`:** Pada model-model berikut, keluarkan semua blok `thinking` dan `redacted_thinking` dari percakapan yang Anda kirim dalam permintaan create baru: Claude Fable 5.2, Claude Mythos 5.2, Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Sonnet 5.5, dan Claude Haiku 5.5. Model kemudian menjawab tanpa penalaran sebelumnya tersebut.

* **Alasannya:** Mengubah `system` atau `tools` membuat blok `thinking` dan `redacted_thinking` yang sudah ada dalam percakapan menjadi tidak valid. Lihat [Apa yang dihitung sebagai perubahan](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#what-counts-as-an-edit).
* **Jika Anda tetap mengirim blok tersebut:** Permintaan create dapat menerima error 400 (lihat [Blok pemikiran yang terikat ke percakapan lain](https://platform.claude.com/docs/id/api/errors#thinking-block-conversation-mismatch)). Lihat [Model mana yang menjalankan pemeriksaan prefiks](https://platform.claude.com/docs/id/build-with-claude/preserved-thinking/prefix-checks#enforcement).

Kirim hanya pesan-pesan baru pada permintaan continue. API tidak memeriksanya terhadap pesan-pesan yang sudah dimilikinya. Pesan yang Anda kirim ulang dapat muncul dua kali dalam percakapan, atau permintaan dapat mengembalikan error. Misalnya, permintaan continue yang dimulai dengan respons sebelumnya akan mengembalikan error.

Pesan-pesan baru biasanya dimulai dengan pesan `user`: giliran pengguna Anda berikutnya, atau blok `tool_result` yang menjawab `tool_use` dalam respons sebelumnya. Jika respons berhenti dengan [`stop_reason: "pause_turn"`](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons#pause-turn), lanjutkan dengan permintaan continue dari `id` respons tersebut dan daftar `messages` kosong (`"messages": []`). Jika permintaan tersebut mengembalikan error 404, putar ulang percakapan lengkap, termasuk respons yang dijeda, dalam permintaan create baru. Jangan mengirim pesan `user` baru saat giliran sedang dijeda: API akan menolaknya. Dengan helper thread SDK, panggil `send()` (go, csharp: `Send()`; ruby: `send_message()`) tanpa pesan: helper mengirim permintaan ini dan melakukan pemutaran ulang jika terjadi error 404.

Thread bersifat “append-only” (hanya dapat ditambahkan), dan setiap `id` respons hanya dapat dilanjutkan satu kali. Selalu lanjutkan dari `id` respons terbaru dalam thread. Untuk mengedit atau membuat cabang dari pesan sebelumnya, mulai thread baru dengan permintaan create. Untuk mengganti giliran-giliran sebelumnya dengan ringkasan, lihat [Memadatkan percakapan](https://platform.claude.com/docs/id/build-with-claude/message-threads#compaction).

## Caching prompt pada thread

Thread tidak melakukan cache prompt Anda untuk Anda. [“Prompt caching” (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) bekerja sama seperti tanpa thread: Anda memilih di mana cache breakpoint ditempatkan.

Untuk melakukan cache setiap giliran, kirim `cache_control` tingkat atas pada setiap permintaan dalam thread, seperti pada contoh sebelumnya. API menerapkannya ke blok terakhir dari `messages` setiap permintaan yang dapat di-cache. Setiap giliran kemudian membaca percakapan sebelumnya dari cache dan menulis giliran baru ke dalamnya. `cache_control` tingkat atas adalah field tetap: kirim nilai yang sama pada setiap permintaan.

Anda juga dapat menempatkan breakpoint `cache_control` pada blok sendiri:

* Breakpoint yang Anda kirim pada permintaan create tetap berfungsi pada setiap giliran berikutnya jika berada di `tools`, di `system`, atau di blok pesan sebelum blok terakhir. Breakpoint pada blok terakhir dari `messages` sebuah permintaan menulis cache pada permintaan tersebut. Untuk melakukan cache pada setiap giliran baru, kirim breakpoint pada setiap permintaan. Permintaan tanpa breakpoint mungkin masih membaca sebagian percakapan dari cache.
* Anda tidak dapat memindahkan atau menghapus breakpoint setelah Anda mengirimnya, karena permintaan continue tidak dapat mengirim ulang pesan sebelumnya.
* Permintaan dengan `thread` dapat membawa paling banyak 4 breakpoint `cache_control`. `cache_control` tingkat atas dihitung sebagai satu. Breakpoint pada `system` dan `tools` dari permintaan create dihitung lagi pada setiap permintaan continue. Breakpoint pada pesan tersimpan sebelumnya tidak dihitung. Kelebihan satu breakpoint saja akan mengembalikan error 400 dengan kode `thread_unsupported_request`.
* Jika Anda menempatkan breakpoint pada blok pesan sendiri, hapus breakpoint tersebut dari pesan-pesan sebelumnya saat Anda memutar ulang percakapan dalam permintaan create baru, dan pertahankan satu pada blok terakhir, sehingga permintaan tetap berada dalam batas 4.

## Streaming

Thread berfungsi dengan [streaming](https://platform.claude.com/docs/id/build-with-claude/streaming). `id` respons tiba dalam event `message_start`, tetapi lanjutkan darinya hanya setelah Anda menerima event `message_stop`. Permintaan continue yang dikirim lebih awal dapat mengembalikan error 404.

Jika stream dari permintaan continue terputus sebelum `message_stop`, kirim ulang permintaan continue yang sama. Jika permintaan tersebut mengembalikan error `thread_already_continued` atau `thread_continue_in_flight`, putar ulang percakapan lengkap dalam permintaan create baru.

Koneksi Anda mungkin terputus saat server masih menghasilkan respons, atau setelah server menyimpannya. Itulah sebabnya API dapat menolak percobaan ulang. Memutar ulang salinan persis Anda aman.

Helper thread SDK tidak mencoba ulang permintaan continue setelah stream terputus. Lihat [Cara kerja helper SDK](https://platform.claude.com/docs/id/build-with-claude/message-threads#sdk-helper-handles).

## Memulihkan ketika thread tidak dapat dilanjutkan

Permintaan continue mengembalikan error 404 dengan `error.details.error_code` diatur ke `thread_not_found` ketika API tidak dapat melanjutkan thread. Respons tidak menyebutkan alasannya. Penyebabnya meliputi hal-hal berikut:

* Thread telah kedaluwarsa.
* API melayani giliran sebelumnya tetapi tidak menyimpannya. Misalnya, API tidak menyimpan respons yang berakhir dengan pemanggilan alat yang terpotong oleh `max_tokens`.
* Respons sebelumnya ditulis oleh model fallback. Lihat [Menggunakan fallback dengan thread](https://platform.claude.com/docs/id/build-with-claude/message-threads#fallbacks).
* Respons sebelumnya masih dalam proses pembuatan.
* Permintaan berasal dari organisasi atau workspace yang berbeda.
* Permintaan berasal dari pengguna atau akun layanan yang berbeda dari yang membuat thread. Thread yang dibuat dengan [kunci workspace (lama)](https://platform.claude.com/docs/id/manage-claude/authentication#key-types) tetap terikat pada kunci tersebut, jadi gunakan kunci yang sama untuk seluruh thread.
* Pesan-pesan baru menambahkan sesuatu yang tidak dapat diterima oleh percakapan yang tersimpan. Misalnya, gambar pertama dalam percakapan yang sebelumnya tidak memiliki gambar dapat mengembalikan error ini.

Untuk memulihkan, kirim seluruh percakapan dari salinan Anda sendiri dalam permintaan create baru, dengan `system` dan `tools`. Helper thread SDK mengirimkan permintaan create ini satu kali dengan sendirinya, dan tidak menyertakan breakpoint `cache_control` dari giliran sebelumnya saat melakukannya. Jika pesan-pesan sebelumnya dalam salinan Anda membawa breakpoint `cache_control`, hapus terlebih dahulu (lihat [Caching prompt pada thread](https://platform.claude.com/docs/id/build-with-claude/message-threads#prompt-caching)). Kemudian lanjutkan dari `id` respons yang baru. Jika model fallback yang menulis respons sebelumnya, lihat [Menggunakan fallback dengan thread](https://platform.claude.com/docs/id/build-with-claude/message-threads#fallbacks). Untuk menyingkirkan penyebab terkait kepemilikan, gunakan kunci API dan workspace yang sama untuk setiap permintaan dalam sebuah thread. Di Claude Platform on AWS, tandatangani setiap permintaan dalam sebuah thread dengan kredensial untuk peran IAM atau pengguna IAM yang membuatnya.

Permintaan untuk model yang tidak ada juga mengembalikan error 404, jadi periksa `error.details.error_code` sebelum Anda memutar ulang.

Jika permintaan continue masih mengembalikan error 404 tepat setelah Anda memutar ulang, API mungkin tidak dapat menyimpan percakapan tersebut, misalnya percakapan yang sangat besar. Kirim tanpa `thread`. Helper thread SDK melakukan ini ketika Anda membuatnya dengan `unsupported_request_behavior` (typescript, java, php: `unsupportedRequestBehavior`; go, csharp: `UnsupportedRequestBehavior`) diatur ke `continue_unthreaded` (ruby: `:continue_unthreaded`; java: `CONTINUE_UNTHREADED`; csharp: `ContinueUnthreaded`; go: `BetaMessageThreadUnsupportedRequestBehaviorContinueUnthreaded`). Jika tidak, helper memutar ulang pada setiap giliran.

### Setelah penolakan

Ketika respons memiliki `stop_reason: "refusal"`, jangan lanjutkan thread. API mungkin sudah menyimpan giliran yang ditolak, dan permintaan continue tidak dapat menghapusnya. Mulai thread baru dengan permintaan create yang tidak menyertakan atau merumuskan ulang giliran yang menyebabkan penolakan. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback). Helper thread SDK melakukan ini untuk Anda: helper tidak menyimpan giliran yang ditolak, dan giliran berikutnya memulai thread baru.

### Menggunakan fallback dengan thread

[Fallback sisi server](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback) tersedia dengan thread di Claude API. Tentukan saat Anda membuat thread: kirim `fallbacks` pada setiap permintaan dalam thread, atau tidak sama sekali. Nilai `fallbacks` dapat berubah antar permintaan. Permintaan continue yang menambahkan `fallbacks` atau tidak lagi menyertakannya mengembalikan error 400 dengan kode `thread_fingerprint_mismatch`.

Thread mempertahankan satu model, sehingga API tidak menyimpan giliran yang ditulis oleh model fallback. Anda menerima respons seperti biasa, tetapi Anda tidak dapat melanjutkan dari `id`-nya. Setelah setiap respons, ikuti langkah-langkah berikut:

1. Jika `stop_reason` adalah `"refusal"`, ikuti [Setelah penolakan](https://platform.claude.com/docs/id/build-with-claude/message-threads#after-a-refusal).

2. Jika tidak, cari entri `fallback_message` di `usage.iterations`. Pada stream, baca entri tersebut dari event `message_delta` terakhir. Jika tidak ada, lanjutkan thread seperti biasa.

3. Jika ada, model fallback yang menulis respons tersebut. Kirim seluruh percakapan, termasuk respons tersebut dan pesan Anda berikutnya, dalam permintaan create baru. Pertahankan header beta `server-side-fallback-2026-07-01` pada permintaan tersebut. Pilih salah satu dari dua permintaan berikut:

   * **Permintaan yang sama lagi.** Pertahankan `model`, `fallbacks`, dan parameter Anda lainnya seperti semula. Jika model yang Anda minta menjawab, API menyimpan thread baru tersebut. Jika model fallback menjawab, respons kembali memiliki entri `fallback_message` dan API tidak menyimpannya, jadi ulangi langkah ini pada giliran berikutnya. [Perutean persisten](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#sticky-routing) mungkin mengirim permintaan ini langsung ke model fallback, sehingga setiap giliran mungkin mengirim seluruh percakapan. Helper thread SDK bekerja dengan cara ini.
   * **Thread baru pada model fallback.** Atur `model` ke `model` dalam entri `fallback_message` tersebut, jangan sertakan `fallbacks`, dan gunakan parameter yang diterima oleh model ini. API langsung menyimpan thread ini, dan thread tetap berada pada model fallback. Percobaan fallback mungkin berjalan dengan pengaturan yang berbeda dari yang Anda kirimkan, sehingga API mungkin menolak nilai yang disalin dari permintaan pertama Anda.

4. Kembali ke langkah 1 dengan respons dari permintaan tersebut. Ketika respons tidak memiliki entri `fallback_message`, lanjutkan thread baru dari `id`-nya.

[Perutean persisten](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#sticky-routing) dimulai setelah sebuah permintaan beralih ke fallback (permintaan create, atau permintaan tanpa `thread`). Selama sekitar satu jam, fitur ini mungkin mengirim permintaan create berikutnya untuk percakapan yang sama yang menyertakan `fallbacks` langsung ke model fallback, tanpa mencoba model yang Anda minta. API tidak menyimpan satu pun dari giliran tersebut, dan setiap giliran yang dijawab memulai ulang hitungan satu jam tersebut. Permintaan continue tidak pernah memulai perutean ini dan tidak pernah menggunakannya. Perutean persisten tidak berlaku jika organisasi atau workspace Anda menggunakan zero data retention atau kunci enkripsi yang dikelola pelanggan.

## Memadatkan percakapan

Thread bersifat append-only (hanya dapat ditambahkan), sehingga Anda tidak dapat mengganti giliran-giliran sebelumnya dengan ringkasan. Untuk memadatkan percakapan, mulai thread baru dari ringkasan tersebut. Tulis ringkasan dalam kode Anda, lalu kirimkan sebagai pesan biasa dalam permintaan create baru, dengan `system` dan `tools`. [Compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand) tidak tersedia dengan thread (lihat [Fitur yang tidak didukung oleh thread](https://platform.claude.com/docs/id/build-with-claude/message-threads#unsupported)).

## Cara kerja helper SDK

Yang dilakukan helper untuk Anda:

* Menambahkan header beta `message-threads-2026-08-12` ke setiap permintaan yang menggunakan thread.
* Membuat thread pada giliran pertama dan melanjutkannya setelah itu, dengan hanya mengirim pesan baru dan tidak menyertakan `system` dan `tools`.
* Memutar ulang seluruh percakapan satu kali dalam permintaan create baru ketika permintaan continue mengembalikan `thread_not_found`, `thread_already_continued`, atau `thread_continue_in_flight`.
* Melanjutkan respons `pause_turn` ketika Anda memanggil `send()` (go, csharp: `Send()`; ruby: `send_message()`) tanpa pesan.
* Memulai thread baru setelah penolakan. Anda mendapatkan respons `stop_reason: "refusal"` seperti biasa, tetapi helper tidak menyimpan giliran tersebut: helper menarik kembali pesan yang Anda berikan pada panggilan itu. Pesan yang Anda tambahkan dengan `thread.append(...)` (csharp, go: `thread.Append(...)`; php: `$thread->append(...)`), atau yang Anda berikan saat membuat helper, tetap berada dalam antrean. Giliran Anda berikutnya mengirimkannya bersama percakapan dari sebelum giliran yang ditolak, dalam permintaan create baru. Kirim pesan yang dirumuskan ulang, atau, jika pesan dalam antrean yang menyebabkan penolakan, mulai thread baru dari params tanpa pesan tersebut.
* Mengirim permintaan create baru setelah respons dari model fallback. Ketika respons memiliki entri `fallback_message` di `usage.iterations`, helper menyimpan respons tersebut dan mengirimkan seluruh percakapan dalam permintaan create baru pada giliran berikutnya. Helper tidak menunggu error 404. Permintaan tersebut mempertahankan `model` dan `fallbacks` yang Anda tetapkan.
* Tidak menyertakan breakpoint `cache_control` dari giliran sebelumnya setiap kali helper mengirimkannya lagi, misalnya dalam pemutaran ulang atau pada giliran pertama dari sebuah fork. Pesan terbaru Anda, `system`, `tools`, dan `cache_control` tingkat atas dikirim sebagaimana Anda memberikannya.

Yang Anda tangani sendiri:

* **Fallback.** Selama API terus menjawab dari model fallback, helper mengirimkan seluruh percakapan dalam permintaan create baru pada setiap giliran, karena API tidak menyimpan satu pun dari giliran tersebut. Helper kembali ke permintaan continue setelah respons dari model yang Anda minta. Untuk memindahkan percakapan ke model fallback, mulai thread baru dari params dengan `model` tersebut dan tanpa `fallbacks`, seperti dalam [Menggunakan fallback dengan thread](https://platform.claude.com/docs/id/build-with-claude/message-threads#fallbacks).
* **Stream yang terputus.** Jika stream berakhir di tengah respons, helper menyimpan blok yang sudah selesai dan teks apa pun yang sudah diterima, dan giliran berikutnya mengirim seluruh percakapan dalam permintaan create baru. Helper tidak mencoba ulang dengan sendirinya: untuk mengirim ulang giliran yang terputus, panggil `send()` (go, csharp: `Send()`; ruby: `send_message()`) tanpa pesan. Jika bagian yang disimpan berakhir dengan pemanggilan alat, jawab pemanggilan tersebut dalam pesan Anda berikutnya. Jika Anda berhenti membaca stream setelah stream menampilkan `stop_reason: "refusal"`, helper memperlakukan giliran tersebut sebagai penolakan.
* **Error lainnya.** Error `thread_fingerprint_mismatch` dan `thread_unsupported_request` diteruskan ke kode Anda. Untuk melanjutkan tanpa `thread` setelah error `thread_unsupported_request`, buat helper dengan `unsupported_request_behavior` (typescript, java, php: `unsupportedRequestBehavior`; go, csharp: `UnsupportedRequestBehavior`) diatur ke `continue_unthreaded` (ruby: `:continue_unthreaded`; java: `CONTINUE_UNTHREADED`; csharp: `ContinueUnthreaded`; go: `BetaMessageThreadUnsupportedRequestBehaviorContinueUnthreaded`). Dengan pengaturan tersebut, helper juga berhenti menggunakan `thread` ketika permintaan continue pertama setelah pemutaran ulang kembali mengembalikan `thread_not_found`. API mungkin tidak dapat menyimpan percakapan tersebut. Tanpa pengaturan tersebut, helper memutar ulang pada setiap giliran. Tool runner yang membuat thread-nya sendiri menggunakan pengaturan tersebut secara default.

Tool runner beta pada SDK juga menggunakan thread secara default, yang dapat Anda nonaktifkan saat membuat runner.

### Metode helper lainnya

| Untuk melakukan ini                                         | Gunakan                                                                                                                                                                                                                                                                                                                              |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Melakukan streaming satu giliran                            | `thread.stream(...)` (csharp: `thread.SendStreaming(...)`; go: `thread.SendStreaming(ctx, params)`; java: `thread.sendStreaming(...)`; php: `$thread->sendStream(...)`)                                                                                                                                                              |
| Respons akhir dari giliran yang di-streaming                | `stream.get_final_message()` (typescript: `stream.finalMessage()`; csharp: `thread.LastMessage`; go: `thread.LastMessage()`; java: `thread.lastMessage()`; php: `$thread->lastMessage()`; ruby: `stream.accumulated_message`)                                                                                                        |
| Percakapan lengkap                                          | `thread.messages` (csharp: `thread.Messages`; go: `thread.Messages()`; java: `thread.messages()`; php: `$thread->messages()`)                                                                                                                                                                                                        |
| `id` respons yang menjadi titik lanjutan giliran berikutnya | `thread.previous_message_id` (typescript: `thread.previousMessageId`; csharp: `thread.PreviousMessageID`; go: `thread.PreviousMessageID()`; java: `thread.previousMessageId()`; php: `$thread->previousMessageId()`)                                                                                                                 |
| Menambahkan pesan tanpa mengirim                            | `thread.append(...)` (csharp, go: `thread.Append(...)`; php: `$thread->append(...)`)                                                                                                                                                                                                                                                 |
| Mengubah field untuk giliran berikutnya                     | `thread.update(...)` (csharp: `thread.Update(p => p with { ... })`; go: `thread.Params.MaxTokens = ...`; java: `thread.update(b -> ...)`; php: `$thread->update([...])`)                                                                                                                                                             |
| Menyalin thread                                             | `thread.fork()` (csharp, go: `thread.Fork()`; php: `$thread->fork()`; ruby: `thread.fork`)                                                                                                                                                                                                                                           |
| Field dan percakapan, untuk memulai thread baru             | `thread.params` (csharp, go: `thread.Params`; java: `thread.params()`; php: `$thread->params()`)                                                                                                                                                                                                                                     |
| Tool runner pada thread ini                                 | `thread.tool_runner()` (typescript, java: `thread.toolRunner()`; csharp: `thread.ToolRunner(tools)`; go: `thread.NewToolRunner(tools)`; php: `$thread->toolRunner()`; ruby: `thread.tool_runner`)                                                                                                                                    |
| Tool runner tanpa thread                                    | `tool_runner(..., thread=False)` (typescript: `toolRunner({ ..., thread: false })`; csharp: `ToolRunner(parameters, tools, thread: false)`; go: `BetaToolRunnerParams{DisableThread: true}`; java: `ToolRunnerCreateParams.builder().thread(false)`; php: `toolRunner(..., thread: false)`; ruby: `tool_runner(..., thread: false)`) |

**Streaming.** Helper mencatat respons ketika stream mencapai `message_stop`, jadi baca stream hingga akhir. Jika Anda berhenti membaca lebih awal, akhiri stream agar thread bebas untuk giliran berikutnya:

* Python: keluar dari blok `with`.
* TypeScript: keluar dari loop atau panggil `abort()`.
* Go: panggil `Close`.
* Java dan Ruby: panggil `close()`.
* C#: lakukan dispose pada enumerator. Keluar dari `await foreach` melakukan hal ini.
* PHP: panggil `close()`.

Di C#, permintaan dikirim ketika Anda mulai membaca stream.

Di C#, Go, Java, dan PHP, setelah penolakan `thread.LastMessage` (go: `thread.LastMessage()`; java: `thread.lastMessage()`; php: `$thread->lastMessage()`) tetap mengembalikan respons giliran sebelumnya, atau tidak mengembalikan apa pun pada giliran pertama. Baca penolakan dari event stream.

**Mengubah field.** Pembaruan tidak mengirimkan apa pun dan berlaku untuk setiap giliran berikutnya. Setelah thread memiliki respons, helper menolak giliran yang mengubah `system` atau `tools`, dan API menolak perubahan pada field tetap lainnya (lihat [Apa yang dikirim pada setiap permintaan](https://platform.claude.com/docs/id/build-with-claude/message-threads#what-to-send)). Untuk mengubah salah satu field ini, mulai thread baru dari params, atau lakukan fork pada thread dan perbarui fork tersebut sebelum giliran pertamanya.

**Melakukan fork.** Fork menyalin percakapan, field, dan opsi permintaan, serta tidak mengirimkan apa pun. Giliran pertamanya mengirimkan percakapan lengkap dalam permintaan create baru, dan kedua thread tersebut independen setelahnya. Fork selalu dimulai dari seluruh percakapan, bukan dari respons sebelumnya.

**Params.** Params menyimpan field milik helper dan seluruh percakapan. Teruskan params tersebut ke metode yang membuat helper untuk memulai thread baru, misalnya dengan `system` yang berbeda (lihat [Apa yang dikirim pada setiap permintaan](https://platform.claude.com/docs/id/build-with-claude/message-threads#what-to-send)), atau dengan `messages` yang dipangkas agar tidak menyertakan giliran-giliran berikutnya. Thread yang Anda mulai dari params mengirim setiap pesan persis seperti yang Anda berikan, termasuk breakpoint `cache_control`, jadi tetaplah dalam batas 4 (lihat [Caching prompt pada thread](https://platform.claude.com/docs/id/build-with-claude/message-threads#prompt-caching)). Kecuali di Ruby, params tidak menyertakan opsi permintaan, jadi teruskan opsi tersebut lagi.

**Output terstruktur.** Berikan format output saat Anda membuat helper. Giliran berikutnya tidak dapat mengubahnya. Cara Anda mendapatkan hasil yang telah di-parse bergantung pada SDK:

* Python dan TypeScript: panggil `thread.parse(...)`.
* C#: buat helper dengan `client.Beta.Messages.Thread<T>(...)`.
* Go: `Send` melakukan unmarshal ke struct yang ditunjuk oleh `Params.OutputConfig.Format.Schema`.
* Java: buat helper dengan `thread(...)` dan `outputConfig(MyClass.class)`.
* PHP: `send()` mengatur `parsed` pada blok teks ketika `outputConfig` menyebutkan kelas model.
* Ruby: teruskan `output_config: {format: MyModel}` ke `thread(...)`, lalu baca `reply.parsed_output`.

## Error

API mengembalikan error dalam tabel ini sebelum model berjalan. Permintaan tidak menggunakan token, dan thread serta waktu kedaluwarsanya tidak berubah. `error.type` adalah `invalid_request_error` untuk error 400 dan `not_found_error` untuk error 404.

| Status | `error_code`                  | Arti                                                                                                                                          | Yang harus dilakukan                                                                                                   |
| ------ | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 404    | `thread_not_found`            | API tidak dapat melanjutkan thread.                                                                                                           | Kirim percakapan lengkap dalam permintaan create baru.                                                                 |
| 400    | `thread_fingerprint_mismatch` | Field tetap berbeda dari nilai yang disimpan bersama thread. Pesan error menyebutkan field-field tersebut.                                    | Pertahankan field tetap tetap sama, atau mulai thread baru untuk mengubahnya.                                          |
| 400    | `thread_already_continued`    | Setiap `id` respons hanya dapat dilanjutkan satu kali.                                                                                        | Lanjutkan dari `id` respons terbaru dalam thread. Jika klien Anda tidak pernah menerima respons tersebut, putar ulang. |
| 400    | `thread_continue_in_flight`   | Permintaan continue lain dari `id` respons ini masih berjalan. Biasanya ini adalah percobaan Anda sendiri sebelumnya.                         | Biarkan selesai dan lanjutkan dari `id` responsnya, atau putar ulang.                                                  |
| 400    | `thread_unsupported_request`  | Permintaan menggunakan fitur atau pengaturan organisasi yang tidak didukung oleh thread. `error.details.unsupported` menyebutkannya jika ada. | Hapus fitur tersebut dari permintaan, atau kirim percakapan lengkap tanpa `thread`.                                    |

Beberapa error 400 untuk permintaan thread tidak membawa `error_code`, misalnya permintaan continue tanpa `previous_message_id`, atau permintaan yang menyertakan `system` atau `tools`.

Contoh berikut menunjukkan body error:

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "thread: a maximum of 4 blocks with cache_control may be provided when `thread` is set. Found 5.",
    "details": {
      "error_code": "thread_unsupported_request",
      "unsupported": ["cache_control"]
    }
  },
  "request_id": "req_011CSHoEeqs5C35K2UUqR7Fy"
}
```

## Fitur yang tidak didukung oleh thread

Thread tidak mendukung fitur-fitur berikut:

* [Message Batches](https://platform.claude.com/docs/id/build-with-claude/batch-processing). Item permintaan yang menyertakan `thread` berakhir dengan `invalid_request_error` dalam hasil batch.
* [Penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting). Permintaan penghitungan token yang menyertakan `thread` mengembalikan error 400. Sebagai gantinya, hitung percakapan lengkap, dengan `system` dan `tools`.
* [Compaction](https://platform.claude.com/docs/id/build-with-claude/compaction). [Compaction sesuai permintaan](https://platform.claude.com/docs/id/build-with-claude/compaction-on-demand) tidak tersedia dengan thread. Permintaan yang menyertakan `thread` mengembalikan error 400 jika permintaan tersebut mengatur parameter `compaction`, atau jika mengirimkan blok `compaction` dengan header beta `compact-2026-09-04`. Lihat [Memadatkan percakapan](https://platform.claude.com/docs/id/build-with-claude/message-threads#compaction).
* [Pengeditan konteks](https://platform.claude.com/docs/id/build-with-claude/context-editing), kecuali `clear_thinking_20251015` dengan `keep: "all"`.
* Organisasi yang mengaktifkan [kesiapan HIPAA](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#hipaa-readiness).
* Organisasi yang mengaktifkan [Inference hooks](https://platform.claude.com/docs/id/manage-claude/inference-hooks).

API menolak sebagian besar permintaan yang tidak didukung oleh thread dengan error 400 dan kode `thread_unsupported_request`. Jika `error.details.unsupported` ada, field tersebut berisi salah satu nilai berikut:

| Nilai                | Arti                                                                                                                                                                                   |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `context_management` | Permintaan menggunakan manajemen konteks atau compaction yang tidak didukung oleh thread.                                                                                              |
| `cache_control`      | Permintaan memiliki lebih dari 4 breakpoint `cache_control`. Lihat [Caching prompt pada thread](https://platform.claude.com/docs/id/build-with-claude/message-threads#prompt-caching). |
| `fallbacks`          | Permintaan mengatur `fallbacks`, dan organisasi Anda tidak dapat menggunakan `fallbacks` dengan thread.                                                                                |
| `hipaa`              | Organisasi Anda mengaktifkan kesiapan HIPAA.                                                                                                                                           |
| `inference_hooks`    | Organisasi Anda mengaktifkan Inference hooks.                                                                                                                                          |

API dapat menambahkan nilai ke daftar ini. Jika Anda mendapatkan nilai yang tidak Anda kenali, kirim percakapan lengkap tanpa `thread`. Permintaan yang memenuhi beberapa kondisi ini mendapatkan error yang hanya menyebutkan salah satunya.

## Keterbatasan

* Tidak ada API untuk mencantumkan, membaca, atau menghapus thread.
* Thread tersedia di Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), Claude Models on Google Cloud (Anthropic managed), dan [Claude di Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry).

## Harga dan batas laju

Thread tidak mengubah harga atau [“rate limits” (batas laju)](https://platform.claude.com/docs/id/api/rate-limits).

## Retensi data

Thread pesan tidak memenuhi syarat ZDR. Menggunakan fitur ini tidak memengaruhi penggunaan Anda atas fitur lain yang memenuhi syarat ZDR. API menampung thread di memori, dienkripsi dengan kunci yang dikelola server, tidak pernah menuliskannya ke penyimpanan permanen, dan menghapusnya paling lambat 1 jam setelah penggunaan terakhirnya.

Thread menampung percakapan yang dikirim API ke model, `system` dan `tools` dari permintaan create, serta fingerprint dari field tetap, yang digunakan untuk memeriksa permintaan berikutnya. Thread menampung file berdasarkan referensi, jadi pastikan setiap file yang digunakan percakapan tetap tersedia selama Anda menggunakan thread.

Untuk kelayakan ZDR di semua fitur, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).

## Lihat juga

* [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)
* [Streaming pesan](https://platform.claude.com/docs/id/build-with-claude/streaming)
* [Error Claude API](https://platform.claude.com/docs/id/api/errors)

## Ketersediaan

Thread pesan dalam versi beta di semua model.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tersedia

| Status | Platform cloud                                                                                                                                                                                                                                                                                                                                                                         |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Beta   | Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed), [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) |

### Header beta yang diperlukan

[Ikhtisar header beta](https://platform.claude.com/docs/id/api/beta-headers)

Header beta memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

* `message-threads-2026-08-12`

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                                                                                                                                                                                                                                                                                                       | HIPAA       |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------- |
| Status | Tidak layak                                                                                                                                                                                                                                                                                                                                                                                                                                            | Tidak layak |
| Detail | Isi thread (percakapan, prompt sistem, dan alat) disimpan di memori, dienkripsi dengan kunci yang dikelola server, tidak pernah ditulis ke penyimpanan permanen, dan dihapus paling lambat 1 jam setelah thread terakhir digunakan. Menggunakan fitur ini tidak memengaruhi penggunaan Anda atas fitur lain yang memiliki kelayakan ZDR. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/build-with-claude/message-threads#data-retention) | —           |

Endpoint yang berlaku:

* `/v1/messages` dengan `thread`
