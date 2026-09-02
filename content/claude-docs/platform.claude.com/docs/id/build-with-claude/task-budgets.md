---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/task-budgets
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 1346265b67074dcd6eff6f135dc18c490ed42b98a9fdc1bd1e8443bcaf92ae56
---

---
title: Anggaran tugas
url: https://platform.claude.com/docs/id/build-with-claude/task-budgets
description: Berikan Claude anggaran token yang bersifat saran untuk seluruh loop agentik guna membantu model mengatur dirinya sendiri pada tugas agentik yang panjang.
---

## Compatibility
- Status: Beta
- [Beta header](https://platform.claude.com/docs/en/api/beta-headers): `task-budgets-2026-03-13`
- Supported models: `claude-fable-5-1`, `claude-mythos-5-1`, `claude-fable-5`, `claude-mythos-5`, `claude-opus-5`, `claude-opus-4-8`, `claude-opus-4-7`

"Task budgets" (anggaran tugas) memungkinkan Anda memberi tahu Claude berapa banyak token yang dimilikinya untuk seluruh loop agentik, termasuk pemikiran, pemanggilan alat, hasil alat, dan output. Model melihat hitung mundur yang terus berjalan dan menggunakannya untuk memprioritaskan pekerjaan serta menyelesaikannya dengan baik seiring anggaran terpakai.

## Kapan menggunakan anggaran tugas

Anggaran tugas paling cocok untuk alur kerja agentik di mana Claude melakukan beberapa pemanggilan alat dan pengambilan keputusan sebelum memfinalisasi outputnya untuk menunggu respons manusia berikutnya. Gunakan ketika:

* Anda ingin Claude mengatur sendiri pengeluaran token pada tugas berjangka panjang.
* Anda memiliki batas atas biaya atau latensi per tugas yang dapat diprediksi dan perlu ditegakkan.
* Anda ingin model menyelesaikan dengan baik (merangkum temuan, melaporkan kemajuan) saat mendekati anggaran, alih-alih terputus di tengah tindakan.

Anggaran tugas melengkapi [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort): effort mengontrol seberapa teliti Claude bernalar tentang setiap langkah, sedangkan anggaran tugas membatasi total pekerjaan yang dapat dilakukan Claude di seluruh loop agentik.

## Menetapkan anggaran tugas

Tambahkan `task_budget` ke `output_config` dan sertakan header beta:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -N \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: task-budgets-2026-03-13" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 128000,
      "stream": true,
      "messages": [{
        "role": "user",
        "content": "Review the codebase and propose a refactor plan."
      }],
      "output_config": {
        "effort": "high",
        "task_budget": {"type": "tokens", "total": 64000}
      }
    }'
  ```

  ```bash CLI
  ant beta:messages create --beta task-budgets-2026-03-13 \
    --stream --format jsonl <<'YAML' | jq 'select(.type == "message_delta").usage'
  model: claude-opus-5
  max_tokens: 128000
  messages:
    - role: user
      content: Review the codebase and propose a refactor plan.
  output_config:
    effort: high
    task_budget:
      type: tokens
      total: 64000
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.beta.messages.stream(
      model="claude-opus-5",
      max_tokens=128000,
      output_config={
          "effort": "high",
          "task_budget": {"type": "tokens", "total": 64000},
      },
      messages=[
          {"role": "user", "content": "Review the codebase and propose a refactor plan."}
      ],
      betas=["task-budgets-2026-03-13"],
  ) as stream:
      response = stream.get_final_message()

  print(response.usage)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.beta.messages.stream({
    model: "claude-opus-5",
    max_tokens: 128000,
    output_config: {
      effort: "high",
      task_budget: { type: "tokens", total: 64000 }
    },
    messages: [{ role: "user", content: "Review the codebase and propose a refactor plan." }],
    betas: ["task-budgets-2026-03-13"]
  });

  const response = await stream.finalMessage();
  console.log(response.usage);
  ```

  ```csharp C#

  var client = new AnthropicClient();

  var responseUpdates = client.Beta.Messages.CreateStreaming(new MessageCreateParams
  {
      Model = Messages::Model.ClaudeOpus5,
      MaxTokens = 128000,
      Messages = [new() { Role = Role.User, Content = "Review the codebase and propose a refactor plan." }],
      OutputConfig = new BetaOutputConfig
      {
          Effort = Effort.High,
          TaskBudget = new BetaTokenTaskBudget { Total = 64000 },
      },
      Betas = ["task-budgets-2026-03-13"],
  });

  var response = await responseUpdates.Aggregate();
  Console.WriteLine(response.Usage);
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Beta.Messages.NewStreaming(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 128000,
  	Betas:     []anthropic.AnthropicBeta{"task-budgets-2026-03-13"},
  	Messages: []anthropic.BetaMessageParam{{
  		Role: anthropic.BetaMessageParamRoleUser,
  		Content: []anthropic.BetaContentBlockParamUnion{{
  			OfText: &anthropic.BetaTextBlockParam{Text: "Review the codebase and propose a refactor plan."},
  		}},
  	}},
  	OutputConfig: anthropic.BetaOutputConfigParam{
  		Effort: anthropic.BetaOutputConfigEffortHigh,
  		TaskBudget: anthropic.BetaTokenTaskBudgetParam{
  			Total: 64000,
  		},
  	},
  })

  message := anthropic.BetaMessage{}
  for stream.Next() {
  	event := stream.Current()
  	if err := message.Accumulate(event); err != nil {
  		panic(err)
  	}
  }
  if stream.Err() != nil {
  	panic(stream.Err())
  }

  fmt.Printf("Usage: input_tokens=%d, output_tokens=%d\n", message.Usage.InputTokens, message.Usage.OutputTokens)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(128000L)
      .addUserMessage("Review the codebase and propose a refactor plan.")
      .outputConfig(BetaOutputConfig.builder()
          .effort(BetaOutputConfig.Effort.HIGH)
          .taskBudget(BetaTokenTaskBudget.builder().total(64000L).build())
          .build())
      .addBeta("task-budgets-2026-03-13")
      .build();

  BetaMessageAccumulator accumulator = BetaMessageAccumulator.create();
  try (StreamResponse<BetaRawMessageStreamEvent> stream =
          client.beta().messages().createStreaming(params)) {
      stream.stream().forEach(accumulator::accumulate);
  }

  BetaMessage response = accumulator.message();
  IO.println(response.usage());
  ```

  ```php PHP
  use Anthropic\Beta\Messages\BetaRawMessageDeltaEvent;

  $client = new Client();

  $stream = $client->beta->messages->createStream(
      model: 'claude-opus-5',
      maxTokens: 128000,
      messages: [
          ['role' => 'user', 'content' => 'Review the codebase and propose a refactor plan.'],
      ],
      outputConfig: [
          'effort' => 'high',
          'taskBudget' => ['type' => 'tokens', 'total' => 64000],
      ],
      betas: ['task-budgets-2026-03-13'],
  );

  // Event message_delta terakhir membawa penggunaan token kumulatif untuk permintaan tersebut.
  $usage = null;
  foreach ($stream as $event) {
      if ($event instanceof BetaRawMessageDeltaEvent) {
          $usage = $event->usage;
      }
  }

  echo $usage;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  stream = client.beta.messages.stream(
    model: "claude-opus-5",
    max_tokens: 128_000,
    messages: [
      { role: "user", content: "Review the codebase and propose a refactor plan." }
    ],
    output_config: {
      effort: :high,
      task_budget: { type: :tokens, total: 64_000 }
    },
    betas: ["task-budgets-2026-03-13"]
  )

  response = stream.accumulated_message

  puts response.usage
  ```
</CodeGroup>

Objek `task_budget` memiliki tiga field:

* `type`: selalu `"tokens"`.
* `total`: jumlah token yang dapat digunakan Claude di seluruh loop agentik, termasuk pemikiran, pemanggilan alat, hasil alat, dan output.
* `remaining` (opsional): sisa anggaran yang dibawa dari permintaan sebelumnya. Secara default bernilai `total` jika dihilangkan.

## Cara kerja hitung mundur anggaran

Claude melihat penanda hitung mundur anggaran yang disisipkan di sisi server sepanjang percakapan. Penanda ini menunjukkan berapa banyak token yang tersisa dalam loop agentik saat ini dan diperbarui seiring model menghasilkan pemikiran, pemanggilan alat, dan output, serta saat model memproses hasil alat. Claude menggunakan sinyal ini untuk mengatur kecepatannya dan menyelesaikan dengan baik seiring anggaran terpakai.

<Note>
  **Hitung mundur hanya terlihat oleh model.** Respons API tidak menyertakan field sisa anggaran: tidak ada informasi `task_budget` dalam objek `usage` pada respons, dan SDK tidak memiliki accessor untuknya. Untuk melacak pengeluaran di sisi klien, jumlahkan penggunaan token di seluruh permintaan dalam loop Anda seperti ditunjukkan di [Ukur penggunaan Anda saat ini](https://platform.claude.com/docs/id/build-with-claude/task-budgets#measure-your-current-usage), atau teruskan angka Anda sendiri dengan `remaining` saat [membawa anggaran melewati compaction](https://platform.claude.com/docs/id/build-with-claude/task-budgets#carrying-a-budget-across-compaction-with-remaining).
</Note>

<Warning>
  **Hitung mundur mencerminkan token yang telah diproses Claude dalam loop agentik saat ini, bukan token yang Anda kirim ulang antar giliran.** Jika klien Anda mengirim seluruh riwayat percakapan pada setiap permintaan lanjutan, hitungan token di sisi klien Anda mungkin berbeda dari anggaran yang dilacak Claude. Jika Anda juga mengurangi `remaining` sambil mengirim ulang seluruh riwayat, model akan melihat anggaran yang dilaporkan lebih kecil dari seharusnya dan hitung mundur turun lebih cepat dari yang semestinya, sehingga Claude menyelesaikan lebih awal daripada yang sebenarnya diizinkan anggaran. Tetapkan anggaran yang longgar dan biarkan model mengatur dirinya sendiri terhadap hitung mundur, alih-alih mencoba mencerminkannya di sisi klien.
</Warning>

### Contoh terperinci: penghitungan anggaran antar giliran

Anggaran tugas menghitung apa yang **dilihat** Claude (pemikiran, pemanggilan dan hasil alat, serta teks), bukan apa yang ada dalam payload permintaan Anda. Dalam loop agentik, klien Anda mengirim ulang seluruh percakapan pada setiap permintaan, sehingga payload bertambah dari giliran ke giliran, tetapi anggaran hanya berkurang sebesar token yang dilihat Claude pada giliran ini.

Pertimbangkan sebuah loop dengan `task_budget: {type: "tokens", total: 100000}` dan satu alat `bash`.

**Giliran 1.** Anda mengirim permintaan awal:

```json
{
  "messages": [
    { "role": "user", "content": "Audit this repo for security issues and report findings." }
  ]
}
```

Claude berpikir, lalu mengeluarkan pemanggilan alat dan berhenti dengan `stop_reason: "tool_use"`:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "thinking",
      "thinking": "I'll start by listing dependencies to look for known-vulnerable packages..."
    },
    {
      "type": "tool_use",
      "id": "toolu_01",
      "name": "bash",
      "input": { "command": "cat package.json && npm audit --json" }
    }
  ]
}
```

Misalkan giliran asisten ini (pemikiran ditambah pemanggilan alat) berjumlah total 5.000 token yang dihasilkan. Hitung mundur yang dilihat Claude selama pembuatan berakhir di sekitar `remaining` ≈ 95.000.

**Giliran 2.** Klien Anda menjalankan alat, lalu mengirim ulang seluruh riwayat dengan hasil alat ditambahkan:

```json
{
  "messages": [
    { "role": "user", "content": "Audit this repo for security issues and report findings." },
    {
      "role": "assistant",
      "content": [
        { "type": "thinking", "thinking": "I'll start by listing dependencies..." },
        {
          "type": "tool_use",
          "id": "toolu_01",
          "name": "bash",
          "input": { "command": "cat package.json && npm audit --json" }
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01",
          "content": "<2,800 tokens of npm audit output>"
        }
      ]
    }
  ]
}
```

Pesan pengguna dan asisten giliran 1 yang dikirim ulang tidak dihitung lagi, tetapi hasil alat sebesar 2.800 token adalah konten baru yang dilihat Claude pada giliran ini dan dihitung terhadap anggaran. Claude menghabiskan 4.000 token lagi untuk pemikiran dan pemanggilan alat kedua (`grep -rn "eval(" src/`). Hitung mundur berakhir di sekitar `remaining` ≈ 88.200.

**Giliran 3.** Seluruh riwayat dikirim ulang lagi dengan hasil alat kedua (1.200 token output grep) ditambahkan. Claude menulis laporan temuan akhir sebesar 6.000 token dan berhenti dengan `stop_reason: "end_turn"`. `remaining` ≈ 81.000.

Menempatkan ketiga giliran berdampingan memperjelas perbedaan antara ukuran payload dan pengeluaran anggaran:

| Giliran   | Payload permintaan (perkiraan token input yang Anda kirim) | Token yang dihitung terhadap anggaran pada giliran ini    | `remaining` anggaran setelahnya |
| --------- | ---------------------------------------------------------- | --------------------------------------------------------- | ------------------------------- |
| 1         | \~20                                                       | 5.000 (pemikiran + `tool_use`)                            | \~95.000                        |
| 2         | \~7.800 (riwayat giliran 1 + hasil alat)                   | 6.800 (2.800 hasil alat + 4.000 pemikiran dan `tool_use`) | \~88.200                        |
| 3         | \~13.000 (seluruh riwayat + hasil alat kedua)              | 7.200 (1.200 hasil alat + 6.000 `text`)                   | \~81.000                        |
| **Total** | **\~20.820 dikirim di seluruh permintaan**                 | **19.000 dihitung terhadap anggaran**                     | N/A                             |

Klien Anda mengirim pesan pengguna giliran 1 tiga kali dan pesan asisten giliran 1 dua kali, tetapi masing-masing hanya dihitung sekali. Anggaran terpakai 19.000 dari 100.000 token, meskipun payload kumulatif yang dikirimkan klien Anda lebih besar dan input yang di-cache melalui caching prompt pada giliran 2 dan 3 lebih besar lagi.

### Membawa anggaran melewati compaction dengan `remaining`

Jika loop agentik Anda melakukan compaction atau menulis ulang konteks di antara permintaan (misalnya, dengan merangkum giliran sebelumnya), server tidak memiliki ingatan tentang berapa banyak anggaran yang telah terpakai sebelum compaction. Teruskan `remaining` pada permintaan berikutnya agar hitung mundur berlanjut dari titik terakhir Anda, alih-alih direset ke `total`:

<CodeGroup exclude="shell">
  ```python Python
  # Token yang digunakan sebelum pemadatan, dilacak di sisi klien
  tokens_spent_so_far = 45000

  output_config = {
      "effort": "high",
      "task_budget": {
          "type": "tokens",
          "total": 128000,
          "remaining": 128000 - tokens_spent_so_far,
      },
  }
  ```

  ```typescript TypeScript
  // Token yang digunakan sebelum pemadatan, dilacak di sisi klien
  const tokensSpentSoFar = 45000;

  const outputConfig = {
    effort: "high",
    task_budget: {
      type: "tokens",
      total: 128000,
      remaining: 128000 - tokensSpentSoFar
    }
  };
  ```

  ```csharp C#
  // Token yang digunakan sebelum pemadatan, dilacak di sisi klien
  var tokensSpentSoFar = 45000;

  var outputConfig = new BetaOutputConfig
  {
      Effort = Effort.High,
      TaskBudget = new BetaTokenTaskBudget
      {
          Total = 128000,
          Remaining = 128000 - tokensSpentSoFar,
      },
  };
  ```

  ```go Go
  // Token yang digunakan sebelum pemadatan, dilacak di sisi klien
  tokensSpentSoFar := int64(45000)

  outputConfig := anthropic.BetaOutputConfigParam{
  	Effort: anthropic.BetaOutputConfigEffortHigh,
  	TaskBudget: anthropic.BetaTokenTaskBudgetParam{
  		Total:     128000,
  		Remaining: anthropic.Int(128000 - tokensSpentSoFar),
  	},
  }
  ```

  ```java Java
  // Token yang digunakan sebelum pemadatan, dilacak di sisi klien
  long tokensSpentSoFar = 45000;

  BetaOutputConfig outputConfig = BetaOutputConfig.builder()
      .effort(BetaOutputConfig.Effort.HIGH)
      .taskBudget(BetaTokenTaskBudget.builder()
          .total(128000L)
          .remaining(128000L - tokensSpentSoFar)
          .build())
      .build();
  ```

  ```php PHP
  // Token yang dihabiskan sebelum pemadatan, dilacak di sisi klien
  $tokensSpentSoFar = 45000;

  $outputConfig = [
      'effort' => 'high',
      'taskBudget' => [
          'type' => 'tokens',
          'total' => 128000,
          'remaining' => 128000 - $tokensSpentSoFar,
      ],
  ];
  ```

  ```ruby Ruby
  # Token yang digunakan sebelum pemadatan, dilacak di sisi klien
  tokens_spent_so_far = 45_000

  output_config = {
    effort: :high,
    task_budget: {
      type: :tokens,
      total: 128_000,
      remaining: 128_000 - tokens_spent_so_far
    }
  }
  ```
</CodeGroup>

Untuk loop yang mengirim ulang seluruh riwayat tanpa compaction pada setiap giliran, hilangkan `remaining` dan biarkan server melacak hitung mundur.

## Mengubah anggaran di tengah percakapan

`task_budget` adalah pengaturan tingkat permintaan. Untuk mengubah anggaran di tengah tugas, misalnya untuk memperpanjangnya ketika pengguna memperluas permintaan, tetapkan `task_budget` baru di `output_config` pada permintaan berikutnya. Perhatikan konsekuensi caching-nya: nilai anggaran ikut serta dalam prompt yang dirender, sehingga nilai yang berubah tidak cocok dengan entri cache yang dibuat dengan nilai lama (lihat [Dukungan fitur](https://platform.claude.com/docs/id/build-with-claude/task-budgets#feature-support) di bawah).

## Anggaran tugas bersifat saran, bukan ditegakkan

Anggaran tugas adalah **petunjuk lunak, bukan batas keras**. Claude terkadang dapat melampaui anggaran jika sedang berada di tengah tindakan yang akan lebih mengganggu jika dihentikan daripada diselesaikan. Batas yang ditegakkan untuk total token output tetaplah `max_tokens`, yang memotong respons dengan `stop_reason: "max_tokens"` ketika tercapai.

Untuk batas keras pada biaya atau latensi, gabungkan anggaran tugas dengan nilai `max_tokens` yang wajar:

* Gunakan `task_budget` untuk memberi Claude target sebagai acuan kecepatan.
* Gunakan `max_tokens` sebagai batas atas absolut yang mencegah pembuatan yang tak terkendali.

Karena `task_budget` mencakup seluruh loop agentik (berpotensi banyak permintaan) sedangkan `max_tokens` membatasi setiap permintaan individual, kedua nilai ini independen; yang satu tidak harus sama dengan atau di bawah yang lain.

<Warning>
  **Anggaran yang terlalu kecil untuk tugas dapat menyebabkan perilaku seperti penolakan.** Ketika Claude melihat anggaran yang jelas tidak mencukupi untuk pekerjaan yang diminta (misalnya, anggaran 20.000 token untuk tugas pengodean agentik berdurasi beberapa jam), Claude mungkin menolak untuk mencoba tugas tersebut sama sekali, mempersempit cakupannya secara agresif, atau berhenti lebih awal dengan hasil parsial alih-alih memulai pekerjaan yang tidak dapat diselesaikannya. Jika Anda mengamati penolakan yang tidak terduga atau penghentian dini setelah menetapkan anggaran, naikkan anggaran sebelum men-debug parameter lain. Tentukan ukuran anggaran berdasarkan distribusi panjang tugas Anda yang sebenarnya, bukan default tetap; lihat [Memilih anggaran](https://platform.claude.com/docs/id/build-with-claude/task-budgets#choosing-a-budget).
</Warning>

## Memilih anggaran

Anggaran yang tepat bergantung pada seberapa banyak pekerjaan yang saat ini dilakukan loop agentik Anda. Daripada menebak, ukur penggunaan token Anda yang ada terlebih dahulu, lalu sesuaikan dari sana.

### Ukur penggunaan Anda saat ini

Jalankan sampel tugas yang representatif **tanpa** menetapkan `task_budget` dan catat total token yang dihabiskan Claude per tugas. Untuk loop agentik, jumlahkan `usage.output_tokens` di setiap permintaan dalam loop, ditambah token dari hasil alat yang Anda tambahkan di antara permintaan:

<CodeGroup>
  ```bash CLI
  ant messages create --transform 'usage.output_tokens' <<'YAML'
  model: claude-opus-5
  max_tokens: 4096
  messages:
    - role: user
      content: Review the codebase and propose a refactor plan.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      messages=[
          {"role": "user", "content": "Review the codebase and propose a refactor plan."}
      ],
  )

  # Jumlahkan output_tokens (teks + pemikiran + pemanggilan alat) di setiap permintaan dalam loop Anda.
  print(response.usage.output_tokens)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    messages: [{ role: "user", content: "Review the codebase and propose a refactor plan." }]
  });

  // Jumlahkan output_tokens (teks + pemikiran + pemanggilan alat) di setiap permintaan dalam loop Anda.
  console.log(response.usage.output_tokens);
  ```

  ```csharp C#

  var client = new AnthropicClient();

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Review the codebase and propose a refactor plan." }],
  });

  // Jumlahkan OutputTokens (teks + pemikiran + pemanggilan alat) di setiap permintaan dalam loop Anda.
  Console.WriteLine(response.Usage.OutputTokens);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Review the codebase and propose a refactor plan.")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Jumlahkan OutputTokens (teks + pemikiran + pemanggilan alat) di setiap permintaan dalam loop Anda.
  fmt.Println(response.Usage.OutputTokens)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(4096L)
      .addUserMessage("Review the codebase and propose a refactor plan.")
      .build();

  Message response = client.messages().create(params);
  // Jumlahkan outputTokens (teks + thinking + pemanggilan alat) di setiap permintaan dalam loop Anda.
  IO.println(response.usage().outputTokens());
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      model: 'claude-opus-5',
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Review the codebase and propose a refactor plan.'],
      ],
  );

  // Jumlahkan outputTokens (teks + pemikiran + pemanggilan alat) di setiap permintaan dalam loop Anda.
  echo $response->usage->outputTokens . "\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Review the codebase and propose a refactor plan." }
    ]
  )

  # Jumlahkan output_tokens (teks + pemikiran + pemanggilan alat) di setiap permintaan dalam loop Anda.
  puts response.usage.output_tokens
  ```
</CodeGroup>

Jalankan ini pada sekumpulan tugas yang representatif dan catat distribusinya. Mulailah dengan p99 dari pengeluaran token per tugas Anda untuk memahami bagaimana pemberian anggaran tugas kepada model dapat mengubah perilaku model, lalu uji naik atau turun sesuai kebutuhan.

Nilai minimum `task_budget.total` yang diterima bersifat spesifik per model. Pada setiap model yang mendukung anggaran tugas (lihat [Dukungan fitur](https://platform.claude.com/docs/id/build-with-claude/task-budgets#feature-support)), nilainya adalah **20.000 token**, dan nilai yang lebih kecil akan mengembalikan error 400.

## Interaksi dengan parameter lain

* **`max_tokens`:** Ortogonal terhadap anggaran tugas. `max_tokens` adalah batas keras per permintaan untuk token yang dihasilkan, sedangkan `task_budget` adalah batas bersifat saran di seluruh loop agentik (berpotensi mencakup banyak permintaan). Pada effort `xhigh` atau `max`, tetapkan `max_tokens` setidaknya 64k untuk memberi Claude ruang untuk berpikir dan bertindak pada setiap permintaan.
* **[Effort](https://platform.claude.com/docs/id/build-with-claude/effort):** Effort mengontrol seberapa dalam Claude bernalar per langkah. Anggaran tugas mengontrol seberapa banyak total pekerjaan yang dilakukan Claude di seluruh loop agentik. Keduanya saling melengkapi: effort mengatur kedalaman, anggaran tugas mengatur keluasan.
* **[Adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking):** Anggaran tugas menyertakan token pemikiran dalam hitungan, sehingga adaptive thinking (pemikiran adaptif) berkurang seiring anggaran menipis.
* **[Prompt caching](https://platform.claude.com/docs/id/build-with-claude/prompt-caching):** Penanda hitung mundur anggaran disisipkan di sisi server per giliran, sehingga tidak cocok antar permintaan. Jika klien Anda mengurangi `task_budget.remaining` pada setiap permintaan lanjutan, nilai yang berubah akan membatalkan prefiks cache apa pun yang memuatnya. Untuk mempertahankan caching prompt, tetapkan anggaran sekali pada permintaan awal dan biarkan model mengatur dirinya sendiri terhadap hitung mundur di sisi server, alih-alih mengubah anggaran di sisi klien.

## Dukungan fitur

| Model             | Dukungan                                         |
| ----------------- | ------------------------------------------------ |
| Claude Fable 5.1  | Beta (tetapkan header `task-budgets-2026-03-13`) |
| Claude Mythos 5.1 | Beta (tetapkan header `task-budgets-2026-03-13`) |
| Claude Opus 5     | Beta (tetapkan header `task-budgets-2026-03-13`) |
| Claude Fable 5    | Beta (tetapkan header `task-budgets-2026-03-13`) |
| Claude Mythos 5   | Beta (tetapkan header `task-budgets-2026-03-13`) |
| Claude Sonnet 5   | Tidak didukung                                   |
| Claude Opus 4.8   | Beta (tetapkan header `task-budgets-2026-03-13`) |
| Claude Opus 4.7   | Beta (tetapkan header `task-budgets-2026-03-13`) |
| Claude Opus 4.6   | Tidak didukung                                   |
| Claude Sonnet 4.6 | Tidak didukung                                   |
| Claude Haiku 4.5  | Tidak didukung                                   |

Anggaran tugas tidak didukung pada [Claude Code](https://code.claude.com/docs/en/overview) atau permukaan Cowork. Gunakan anggaran tugas secara langsung melalui Messages API pada [model yang didukung](https://platform.claude.com/docs/id/build-with-claude/task-budgets#feature-support).

## Langkah selanjutnya

<CardGroup>
  <Card title="Effort" icon="gauge" href="https://platform.claude.com/docs/id/build-with-claude/effort">
    Kontrol seberapa teliti Claude bernalar tentang setiap langkah dalam loop agentik.
  </Card>

  <Card title="Adaptive thinking" icon="brain" href="https://platform.claude.com/docs/id/build-with-claude/thinking">
    Biarkan Claude memutuskan kapan dan seberapa banyak menggunakan pemikiran diperpanjang.
  </Card>

  <Card title="Compaction" icon="arrows-clockwise" href="https://platform.claude.com/docs/id/build-with-claude/compaction">
    Kelola konteks dalam percakapan yang berjalan lama dengan compaction di sisi server.
  </Card>

  <Card title="Caching prompt" icon="database" href="https://platform.claude.com/docs/id/build-with-claude/prompt-caching">
    Kurangi biaya dan latensi pada prompt berulang dengan melakukan caching prefiks prompt.
  </Card>
</CardGroup>
