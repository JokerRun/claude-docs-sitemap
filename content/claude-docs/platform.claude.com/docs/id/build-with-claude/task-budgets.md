---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/task-budgets
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: e582f64a3e73b9422756259c4681836ac7ebb4e99dca9c37f84b987c17179e49
---

# Anggaran tugas

Berikan Claude anggaran token yang bersifat saran untuk loop agentik penuh guna membantu model mengatur dirinya sendiri pada tugas agentik yang panjang.

---

"Task budgets" (anggaran tugas) memungkinkan Anda memberi tahu Claude berapa banyak token yang dimilikinya untuk satu loop agentik penuh, termasuk pemikiran, panggilan alat, hasil alat, dan output. Model melihat hitungan mundur yang berjalan dan menggunakannya untuk memprioritaskan pekerjaan dan menyelesaikan dengan baik saat anggaran terpakai.

<Note>
  Anggaran tugas berada dalam tahap beta pada Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, dan Claude Opus 4.7. Setel header beta `task-budgets-2026-03-13` untuk ikut serta.
</Note>

## Kapan menggunakan anggaran tugas

Anggaran tugas bekerja paling baik untuk alur kerja agentik di mana Claude melakukan beberapa panggilan alat dan keputusan sebelum memfinalisasi outputnya untuk menunggu respons manusia berikutnya. Gunakan anggaran tugas ketika:

* Anda ingin Claude mengatur sendiri pengeluaran token pada tugas berhorizon panjang.
* Anda memiliki batas biaya atau latensi per tugas yang dapat diprediksi untuk diterapkan.
* Anda ingin model menyelesaikan dengan baik (merangkum temuan, melaporkan kemajuan) saat mendekati anggaran alih-alih terputus di tengah tindakan.

Anggaran tugas melengkapi [parameter effort](/docs/id/build-with-claude/effort): effort mengontrol seberapa menyeluruh Claude bernalar tentang setiap langkah, sementara anggaran tugas membatasi total pekerjaan yang dapat dilakukan Claude di sepanjang loop agentik.

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
      "model": "claude-opus-4-8",
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
  model: claude-opus-4-8
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
      model="claude-opus-4-8",
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
    model: "claude-opus-4-8",
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
      Model = Messages::Model.ClaudeOpus4_8,
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
  	Model:     anthropic.ModelClaudeOpus4_8,
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
      .model(Model.CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
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
* `total`: jumlah token yang dapat dihabiskan Claude di sepanjang loop agentik, termasuk pemikiran, panggilan alat, hasil alat, dan output.
* `remaining` (opsional): sisa anggaran yang dibawa dari permintaan sebelumnya. Secara default bernilai `total` jika dihilangkan.

## Cara kerja hitungan mundur anggaran

Claude melihat penanda hitungan mundur anggaran yang disisipkan di sisi server di sepanjang percakapan. Penanda ini menunjukkan berapa banyak token yang tersisa dalam loop agentik saat ini dan diperbarui saat model menghasilkan pemikiran, panggilan alat, dan output, serta saat memproses hasil alat. Claude menggunakan sinyal ini untuk mengatur kecepatannya dan menyelesaikan dengan baik saat anggaran terpakai.

<Note>
  **Hitungan mundur hanya terlihat oleh model.** Respons API tidak menyertakan field sisa anggaran: tidak ada informasi `task_budget` dalam objek `usage` respons, dan SDK tidak memiliki accessor untuk itu. Untuk melacak pengeluaran di sisi klien, jumlahkan penggunaan token di seluruh permintaan dalam loop Anda seperti yang ditunjukkan di [Ukur penggunaan Anda saat ini](#measure-your-current-usage), atau teruskan angka Anda sendiri dengan `remaining` saat [membawa anggaran melintasi kompaksi](#carrying-a-budget-across-compaction-with-remaining).
</Note>

<Warning>
  **Hitungan mundur mencerminkan token yang telah diproses Claude dalam loop agentik saat ini, bukan token yang Anda kirim ulang di antara giliran.** Jika klien Anda mengirim seluruh riwayat percakapan pada setiap permintaan lanjutan, jumlah token di sisi klien Anda mungkin berbeda dari anggaran yang dilacak Claude. Jika Anda juga mengurangi `remaining` sambil mengirim ulang riwayat penuh, model melihat anggaran yang dilaporkan terlalu rendah dan hitungan mundur turun lebih cepat dari seharusnya, menyebabkan Claude menyelesaikan lebih awal daripada yang sebenarnya diizinkan anggaran. Tetapkan anggaran yang longgar dan biarkan model mengatur dirinya sendiri terhadap hitungan mundur alih-alih mencoba mencerminkannya di sisi klien.
</Warning>

### Contoh terperinci: penghitungan anggaran di sepanjang giliran

Anggaran tugas menghitung apa yang **dilihat** Claude (pemikiran, panggilan alat dan hasilnya, serta teks), bukan apa yang ada dalam payload permintaan Anda. Dalam loop agentik, klien Anda mengirim ulang seluruh percakapan pada setiap permintaan, sehingga payload bertambah dari giliran ke giliran, tetapi anggaran hanya berkurang sebesar token yang dilihat Claude pada giliran ini.

Pertimbangkan sebuah loop dengan `task_budget: {type: "tokens", total: 100000}` dan satu alat `bash`.

**Giliran 1.** Anda mengirim permintaan awal:

```json
{
  "messages": [
    { "role": "user", "content": "Audit this repo for security issues and report findings." }
  ]
}
```

Claude berpikir, lalu mengeluarkan panggilan alat dan berhenti dengan `stop_reason: "tool_use"`:

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

Misalkan giliran asisten ini (pemikiran ditambah panggilan alat) berjumlah 5.000 token yang dihasilkan. Hitungan mundur yang dilihat Claude selama pembuatan berakhir di sekitar `remaining` ≈ 95.000.

**Giliran 2.** Klien Anda menjalankan alat, lalu mengirim ulang riwayat penuh dengan hasil alat ditambahkan:

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

Pesan user dan asisten giliran-1 yang dikirim ulang tidak dihitung lagi, tetapi hasil alat sebesar 2.800 token adalah konten baru yang dilihat Claude pada giliran ini dan dihitung terhadap anggaran. Claude menghabiskan 4.000 token lagi untuk pemikiran dan panggilan alat kedua (`grep -rn "eval(" src/`). Hitungan mundur berakhir di sekitar `remaining` ≈ 88.200.

**Giliran 3.** Riwayat penuh dikirim ulang lagi dengan hasil alat kedua (1.200 token output grep) ditambahkan. Claude menulis laporan temuan akhir sebesar 6.000 token dan berhenti dengan `stop_reason: "end_turn"`. `remaining` ≈ 81.000.

Menempatkan ketiga giliran berdampingan membuat perbedaan antara ukuran payload dan pengeluaran anggaran menjadi eksplisit:

| Giliran   | Payload permintaan (perkiraan token input yang Anda kirim) | Token yang dihitung terhadap anggaran pada giliran ini    | `remaining` anggaran setelahnya |
| --------- | ---------------------------------------------------------- | --------------------------------------------------------- | ------------------------------- |
| 1         | \~20                                                       | 5.000 (pemikiran + `tool_use`)                            | \~95.000                        |
| 2         | \~7.800 (riwayat giliran 1 + hasil alat)                   | 6.800 (2.800 hasil alat + 4.000 pemikiran dan `tool_use`) | \~88.200                        |
| 3         | \~13.000 (riwayat penuh + hasil alat kedua)                | 7.200 (1.200 hasil alat + 6.000 `text`)                   | \~81.000                        |
| **Total** | **\~20.820 dikirim di seluruh permintaan**                 | **19.000 dihitung terhadap anggaran**                     | N/A                             |

Klien Anda mengirim pesan user giliran-1 tiga kali dan pesan asisten giliran-1 dua kali, tetapi masing-masing hanya dihitung sekali. Anggaran menghabiskan 19.000 dari 100.000 token, meskipun payload kumulatif yang ditransmisikan klien Anda lebih besar dan input yang di-cache prompt pada giliran 2 dan 3 bahkan lebih besar lagi.

### Membawa anggaran melintasi kompaksi dengan `remaining`

Jika loop agentik Anda melakukan kompaksi atau menulis ulang konteks di antara permintaan (misalnya, dengan merangkum giliran sebelumnya), server tidak memiliki memori tentang berapa banyak anggaran yang dihabiskan sebelum kompaksi. Teruskan `remaining` pada permintaan berikutnya agar hitungan mundur berlanjut dari tempat Anda berhenti alih-alih disetel ulang ke `total`:

<CodeGroup exclude="shell">
  ```python Python
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
  outputConfig := anthropic.BetaOutputConfigParam{
  	Effort: anthropic.BetaOutputConfigEffortHigh,
  	TaskBudget: anthropic.BetaTokenTaskBudgetParam{
  		Total:     128000,
  		Remaining: anthropic.Int(128000 - tokensSpentSoFar),
  	},
  }
  ```

  ```java Java
  BetaOutputConfig outputConfig = BetaOutputConfig.builder()
      .effort(BetaOutputConfig.Effort.HIGH)
      .taskBudget(BetaTokenTaskBudget.builder()
          .total(128000L)
          .remaining(128000L - tokensSpentSoFar)
          .build())
      .build();
  ```

  ```php PHP
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

Untuk loop yang mengirim ulang riwayat penuh tanpa kompaksi pada setiap giliran, hilangkan `remaining` dan biarkan server melacak hitungan mundur.

## Anggaran tugas bersifat saran, bukan paksaan

Anggaran tugas adalah **petunjuk lunak, bukan batas keras**. Claude terkadang dapat melebihi anggaran jika sedang berada di tengah tindakan yang akan lebih mengganggu jika diinterupsi daripada diselesaikan. Batas yang diberlakukan pada total token output tetaplah `max_tokens`, yang memotong respons dengan `stop_reason: "max_tokens"` saat tercapai.

Untuk batas keras pada biaya atau latensi, kombinasikan anggaran tugas dengan nilai `max_tokens` yang wajar:

* Gunakan `task_budget` untuk memberi Claude target untuk mengatur kecepatannya.
* Gunakan `max_tokens` sebagai batas absolut yang mencegah pembuatan yang tidak terkendali.

Karena `task_budget` mencakup seluruh loop agentik (berpotensi banyak permintaan) sementara `max_tokens` membatasi setiap permintaan individual, kedua nilai tersebut independen; yang satu tidak harus berada pada atau di bawah yang lain.

<Warning>
  **Anggaran yang terlalu kecil untuk tugas dapat menyebabkan perilaku seperti penolakan.** Ketika Claude melihat anggaran yang jelas tidak cukup untuk pekerjaan yang diminta (misalnya, anggaran 20.000 token untuk tugas pengkodean agentik berjam-jam), Claude mungkin menolak untuk mencoba tugas tersebut sama sekali, mempersempit cakupannya secara agresif, atau berhenti lebih awal dengan hasil parsial alih-alih memulai pekerjaan yang tidak dapat diselesaikannya. Jika Anda mengamati penolakan yang tidak terduga atau penghentian prematur setelah menetapkan anggaran, naikkan anggaran sebelum men-debug parameter lain. Ukur anggaran berdasarkan distribusi panjang tugas Anda yang sebenarnya alih-alih default tetap; lihat [Memilih anggaran](#choosing-a-budget).
</Warning>

## Memilih anggaran

Anggaran yang tepat bergantung pada seberapa banyak pekerjaan yang saat ini dilakukan loop agentik Anda. Alih-alih menebak, ukur penggunaan token Anda yang ada terlebih dahulu lalu sesuaikan dari sana.

### Ukur penggunaan Anda saat ini

Jalankan sampel tugas yang representatif **tanpa** menyetel `task_budget` dan catat total token yang dihabiskan Claude per tugas. Untuk loop agentik, jumlahkan `usage.output_tokens` di setiap permintaan dalam loop, ditambah token dari hasil alat yang Anda tambahkan di antara permintaan:

<CodeGroup>
  ```bash CLI
  ant messages create --transform 'usage.output_tokens' <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  messages:
    - role: user
      content: Review the codebase and propose a refactor plan.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=4096,
      messages=[
          {"role": "user", "content": "Review the codebase and propose a refactor plan."}
      ],
  )

  # Jumlahkan output_tokens (teks + pemikiran + panggilan alat) di setiap permintaan dalam loop Anda.
  print(response.usage.output_tokens)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [{ role: "user", content: "Review the codebase and propose a refactor plan." }]
  });

  // Jumlahkan output_tokens (teks + pemikiran + panggilan alat) di setiap permintaan dalam loop Anda.
  console.log(response.usage.output_tokens);
  ```

  ```csharp C#

  var client = new AnthropicClient();

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Messages = [new() { Role = Role.User, Content = "Review the codebase and propose a refactor plan." }],
  });

  // Jumlahkan OutputTokens (teks + pemikiran + panggilan alat) di seluruh permintaan dalam loop Anda.
  Console.WriteLine(response.Usage.OutputTokens);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Review the codebase and propose a refactor plan.")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  // Jumlahkan OutputTokens (teks + pemikiran + panggilan alat) di seluruh permintaan dalam loop Anda.
  fmt.Println(response.Usage.OutputTokens)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(4096L)
      .addUserMessage("Review the codebase and propose a refactor plan.")
      .build();

  Message response = client.messages().create(params);
  // Jumlahkan outputTokens (teks + pemikiran + panggilan alat) di seluruh permintaan dalam loop Anda.
  IO.println(response.usage().outputTokens());
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      model: 'claude-opus-4-8',
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
    model: "claude-opus-4-8",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Review the codebase and propose a refactor plan." }
    ]
  )

  # Jumlahkan output_tokens (teks + pemikiran + pemanggilan alat) di setiap permintaan dalam loop Anda.
  puts response.usage.output_tokens
  ```
</CodeGroup>

Jalankan ini pada serangkaian tugas yang representatif dan catat distribusinya. Mulailah dengan p99 dari pengeluaran token per tugas Anda untuk memahami bagaimana memberikan anggaran tugas kepada model dapat mengubah perilaku model, lalu uji naik atau turun sesuai kebutuhan.

Nilai minimum `task_budget.total` yang diterima adalah **20.000 token**; nilai di bawah minimum mengembalikan error 400.

## Interaksi dengan parameter lain

* **`max_tokens`:** Ortogonal terhadap anggaran tugas. `max_tokens` adalah batas keras per permintaan pada token yang dihasilkan, sementara `task_budget` adalah batas yang bersifat saran di sepanjang loop agentik penuh (berpotensi mencakup banyak permintaan). Pada effort `xhigh` atau `max`, setel `max_tokens` ke setidaknya 64k untuk memberi Claude ruang untuk berpikir dan bertindak pada setiap permintaan.
* **[Effort](/docs/id/build-with-claude/effort):** Effort mengontrol seberapa dalam Claude bernalar per langkah. Anggaran tugas mengontrol berapa banyak total pekerjaan yang dilakukan Claude di sepanjang loop agentik. Keduanya saling melengkapi: effort menyetel kedalaman, anggaran tugas menyetel keluasan.
* **[Pemikiran adaptif](/docs/id/build-with-claude/adaptive-thinking):** Anggaran tugas menyertakan token pemikiran dalam hitungan, sehingga pemikiran adaptif secara alami berkurang saat anggaran menipis.
* **[Caching prompt](/docs/id/build-with-claude/prompt-caching):** Penanda hitungan mundur anggaran disisipkan di sisi server per giliran, sehingga tidak cocok di antara permintaan. Jika klien Anda mengurangi `task_budget.remaining` pada setiap permintaan lanjutan, nilai yang berubah membatalkan prefiks cache apa pun yang memuatnya. Untuk mempertahankan caching, tetapkan anggaran sekali pada permintaan awal dan biarkan model mengatur dirinya sendiri terhadap hitungan mundur di sisi server alih-alih mengubah anggaran di sisi klien.

## Dukungan fitur

| Model             | Dukungan                                      |
| ----------------- | --------------------------------------------- |
| Claude Fable 5    | Beta (setel header `task-budgets-2026-03-13`) |
| Claude Mythos 5   | Beta (setel header `task-budgets-2026-03-13`) |
| Claude Sonnet 5   | Tidak didukung                                |
| Claude Opus 4.8   | Beta (setel header `task-budgets-2026-03-13`) |
| Claude Opus 4.7   | Beta (setel header `task-budgets-2026-03-13`) |
| Claude Opus 4.6   | Tidak didukung                                |
| Claude Sonnet 4.6 | Tidak didukung                                |
| Claude Haiku 4.5  | Tidak didukung                                |

Anggaran tugas tidak didukung pada [Claude Code](https://code.claude.com/docs/en/overview) atau permukaan Cowork. Gunakan anggaran tugas langsung melalui Messages API pada [model yang didukung](#feature-support).

## Langkah selanjutnya

<CardGroup>
  <Card title="Effort" icon="gauge" href="/docs/id/build-with-claude/effort">
    Kontrol seberapa menyeluruh Claude bernalar tentang setiap langkah dari loop agentik.
  </Card>

  <Card title="Pemikiran adaptif" icon="brain" href="/docs/id/build-with-claude/adaptive-thinking">
    Biarkan Claude memutuskan kapan dan seberapa banyak menggunakan pemikiran diperpanjang.
  </Card>

  <Card title="Kompaksi" icon="arrows-clockwise" href="/docs/id/build-with-claude/compaction">
    Kelola konteks dalam percakapan yang berjalan lama dengan kompaksi di sisi server.
  </Card>

  <Card title="Caching prompt" icon="database" href="/docs/id/build-with-claude/prompt-caching">
    Kurangi biaya dan latensi pada prompt yang berulang dengan melakukan caching pada prefiks prompt.
  </Card>
</CardGroup>
