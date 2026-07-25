---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost
fetched_at: 2026-07-25T03:07:29.726338Z
sha256: 32554f3cac0aa9b3ef28245e2d8d1f947cc505946d5702ebafdf72f8cf37adde
---

# Mengarahkan pemikiran

Arahkan seberapa sering dan seberapa dalam Claude berpikir dengan tingkat effort, panduan prompt sistem, dan pengarahan per pesan, serta pahami biaya dan harga pemikiran.

---

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](/docs/id/manage-claude/api-and-data-retention).
</Note>

Pemikiran Claude bersifat adaptif: model mengevaluasi setiap permintaan dan memutuskan sendiri apakah akan berpikir dan seberapa banyak. Anda menetapkan sebuah intent, secara opsional menentukan effort, dan model mengalokasikan penalaran di tempat yang menurutnya penalaran akan membantu.

Ini membuat pemikiran sangat cocok untuk beban kerja yang mencampur permintaan sepele dan kompleks, serta untuk alur kerja agentik jangka panjang di mana jumlah penalaran yang tepat bervariasi dari langkah ke langkah.

Untuk cara mengaktifkan pemikiran, cara membaca output pemikiran, dan [output pemikiran pada Claude Fable 5 dan Claude Mythos 5](/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5), lihat ikhtisar [Pemikiran](/docs/id/build-with-claude/thinking). Halaman ini membahas bagaimana Claude memutuskan kapan harus berpikir, cara mengarahkan keputusan tersebut, serta mekanisme caching, biaya, dan harga yang mengikutinya.

## Bagaimana Claude memutuskan kapan harus berpikir

Pemikiran bersifat opsional bagi model. Pada setiap permintaan, Claude menimbang kompleksitas input dan memutuskan apakah penalaran yang lebih dalam akan meningkatkan jawaban. Pertanyaan faktual sederhana mungkin mendapat respons langsung tanpa blok pemikiran sama sekali; soal matematika multilangkah atau tugas debugging yang rumit memicu penalaran yang lebih dalam.

Keputusan terjadi per permintaan. Percakapan yang sama dapat berisi giliran dengan dan tanpa pemikiran, dan giliran di mana Claude memilih untuk tidak berpikir tidak berisi blok pemikiran. Jangan membangun logika aplikasi yang mengasumsikan setiap giliran asisten dimulai dengan blok pemikiran.

Kontrol utama atas keputusan ini adalah parameter [effort](/docs/id/build-with-claude/effort), yang bertindak sebagai panduan lunak untuk seberapa bersedia Claude berpikir dan seberapa dalam; lihat [Tingkat effort](#effort-levels) di halaman ini untuk apa yang dilakukan setiap tingkat.

Jika Anda ingin Claude lebih jarang berpikir, turunkan tingkat effort sebelum beralih ke pengarahan berbasis prompt.

Pemikiran juga menyisip dengan penggunaan alat secara otomatis: Claude dapat berpikir di antara panggilan alat, merefleksikan setiap hasil alat sebelum memutuskan apa yang harus dilakukan selanjutnya ([interleaved thinking](/docs/id/build-with-claude/thinking#interleaved-thinking)). Anda tidak memerlukan header beta atau konfigurasi tambahan apa pun untuk ini.

Untuk gambaran lengkap tentang bagaimana konfigurasi pemikiran dan parameter effort berinteraksi, lihat [Pemikiran dan effort](/docs/id/build-with-claude/thinking#thinking-and-effort).

## Mengarahkan seberapa sering Claude berpikir

Apakah Claude berpikir pada giliran tertentu dapat diarahkan melalui prompt. Effort menetapkan postur keseluruhan, tetapi Anda juga dapat membentuk keputusan secara langsung dengan panduan bahasa alami, baik secara global di prompt sistem maupun per pesan dari giliran pengguna.

Gunakan kedua tuas tersebut bersama-sama dalam urutan ini:

1. Tetapkan tingkat effort yang sesuai dengan keseimbangan default kualitas dan latensi beban kerja Anda.
2. Tambahkan panduan prompt hanya jika pemicuan Claude masih tidak sesuai dengan kebutuhan Anda pada tingkat tersebut.

Untuk panduan prompting yang lebih luas dengan pemikiran, lihat [memanfaatkan kemampuan thinking dan interleaved thinking](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities).

### Tingkat effort

Effort adalah tuas pengarahan utama untuk pemikiran. Setiap tingkat menetapkan default yang berbeda untuk seberapa sering Claude berpikir dan seberapa dalam:

| Tingkat effort   | Perilaku pemikiran                                                                                          |
| ---------------- | ----------------------------------------------------------------------------------------------------------- |
| `max`            | Claude selalu berpikir tanpa batasan pada kedalaman pemikiran.                                              |
| `xhigh`          | Claude selalu berpikir secara mendalam dengan eksplorasi yang diperluas.                                    |
| `high` (default) | Claude hampir selalu berpikir. Memberikan penalaran mendalam pada tugas-tugas kompleks.                     |
| `medium`         | Claude menggunakan pemikiran moderat. Mungkin melewatkan pemikiran untuk kueri sederhana.                   |
| `low`            | Claude meminimalkan pemikiran. Melewatkan pemikiran untuk tugas sederhana di mana kecepatan paling penting. |

Tabel ini menjelaskan bagaimana setiap tingkat mengubah perilaku pemikiran. Untuk panduan tentang tingkat mana yang harus dipilih untuk beban kerja tertentu, termasuk rekomendasi per model, lihat [Kapan menyesuaikan parameter effort](/docs/id/build-with-claude/effort#when-to-adjust-the-effort-parameter) di halaman effort.

Effort ditetapkan di `output_config.effort`, bukan di dalam objek `thinking`; untuk contoh lengkap per bahasa, lihat [Effort](/docs/id/build-with-claude/effort#basic-usage).

```json
{
  "model": "claude-opus-4-8",
  "max_tokens": 4096,
  "output_config": { "effort": "medium" },
  "messages": [{ "role": "user", "content": "..." }]
}
```

Ketersediaan tingkat bervariasi menurut model; [tabel ketersediaan effort](/docs/id/build-with-claude/effort#effort-levels) di halaman effort adalah otoritas untuk tingkat mana yang didukung setiap model.

### Panduan prompt sistem

Panduan prompt sistem menggeser ambang pemikiran Claude untuk setiap permintaan dalam percakapan. Jika Claude berpikir lebih sering daripada yang dibutuhkan beban kerja Anda, tambahkan panduan seperti ini ke prompt sistem Anda:

```text wrap
Extended thinking adds latency and should only be used when it
will meaningfully improve answer quality, typically for problems
that require multistep reasoning. When in doubt, respond directly.
```

Untuk mendorong pemikiran sebagai gantinya, gunakan frasa seperti:

```text wrap
This task involves multistep reasoning. Think carefully before responding.
```

Efektivitas pengarahan dapat sensitif terhadap pilihan kata yang tepat. Jika satu frasa tidak menghasilkan perilaku yang Anda inginkan, coba varian yang lebih langsung.

### Pengarahan per pesan

Anda juga dapat mengarahkan pemikiran berdasarkan per pesan dari giliran pengguna, secara independen dari prompt sistem. Menambahkan `"Please think hard before responding."` ke pesan pengguna mendorong Claude untuk berpikir pada giliran tersebut; `"Answer directly without deliberating."` menekannya.

Pengarahan per pesan berguna ketika hanya beberapa permintaan dalam percakapan yang memerlukan penalaran diperpanjang. Sebuah agent harness, misalnya, dapat menambahkan frasa pendorong pada langkah perencanaan dan frasa penekan pada konfirmasi rutin, tanpa menyentuh prompt sistem atau mengubah parameter permintaan apa pun di antara giliran.

### Verifikasi pengarahan pada beban kerja Anda

Pengarahan berbasis prompt mengubah perilaku model, jadi perlakukan seperti perubahan prompt lainnya: ukur sebelum Anda merilis. Jalankan sampel representatif dari lalu lintas Anda dengan dan tanpa panduan, dan bandingkan seberapa sering pemikiran terpicu (keberadaan blok pemikiran dalam respons), penggunaan token output, latensi, dan kualitas jawaban pada kasus-kasus yang penting bagi Anda.

<Warning>
  Mengarahkan Claude untuk lebih jarang berpikir dapat mengurangi kualitas pada tugas yang mendapat manfaat dari penalaran. Menurunkan tingkat [effort](/docs/id/build-with-claude/effort) biasanya merupakan tuas pertama yang lebih baik, karena ini adalah kontrol yang terkalibrasi alih-alih instruksi yang sensitif terhadap pilihan kata. Ukur dampaknya pada beban kerja spesifik Anda sebelum menerapkan penyetelan berbasis prompt ke produksi.
</Warning>

## Mekanisme

Tiga mekanisme mengikuti dari Claude yang mengelola pemikirannya sendiri: validasi giliran, caching prompt, dan cara Anda membatasi biaya.

### Validasi giliran

Giliran asisten tidak perlu dimulai dengan blok pemikiran. (Model yang menggunakan budget pemikiran manual lama mewajibkan giliran asisten terakhir dari permintaan dengan pemikiran aktif dimulai dengan blok pemikiran; lihat [Struktur giliran dalam mode manual](/docs/id/build-with-claude/extended-thinking#turn-structure-in-manual-mode).)

Untuk aplikasi multi-giliran, ini berarti Anda dapat mengirimkan kembali riwayat percakapan dalam bentuk apa pun yang Anda miliki:

* Giliran asisten di mana Claude memilih untuk tidak berpikir adalah riwayat yang valid apa adanya.
* Anda dapat melanjutkan percakapan yang dimulai tanpa pemikiran, atau yang menggunakan konfigurasi pemikiran yang berbeda, tanpa menulis ulang riwayatnya.
* Riwayat yang dirakit dari sumber campuran tidak perlu blok pemikiran disisipkan kembali di awal setiap giliran asisten untuk lolos validasi.

Pelonggaran ini tentang validasi, bukan tentang apa yang harus Anda kirim. Ketika Anda memiliki blok pemikiran, kirimkan kembali tanpa modifikasi, terutama selama penggunaan alat, di mana blok tersebut membawa penalaran di balik panggilan alat Claude. Lihat ikhtisar [Pemikiran](/docs/id/build-with-claude/thinking) untuk aturan lengkapnya.

### Caching prompt

Permintaan berurutan yang mempertahankan konfigurasi pemikiran dan tingkat effort yang sama mempertahankan caching prompt; lihat [Pemikiran dan caching prompt](/docs/id/build-with-claude/thinking#thinking-and-prompt-caching) untuk aturan lengkapnya. Nilai effort yang diselesaikan dirender ke dalam prompt, jadi mengubahnya di antara permintaan membatalkan breakpoint cache, sama seperti mengubah parameter lama [`budget_tokens`](/docs/id/build-with-claude/extended-thinking#extended-thinking-with-prompt-caching) pada model yang menggunakannya. Menetapkan `effort` secara eksplisit ke default model setara dengan menghilangkannya dan tidak merusak cache.

Konsekuensi praktisnya: pilih konfigurasi pemikiran dan tingkat effort per percakapan dan pertahankan. Jika beberapa giliran membutuhkan lebih banyak atau lebih sedikit pemikiran, arahkan dengan [prompting per pesan](#tuning-thinking-behavior): panduan yang ditambahkan ke pesan pengguna terbaru membiarkan breakpoint cache sebelumnya tetap utuh, sedangkan perubahan konfigurasi atau effort tidak.

Contoh berikut mendemonstrasikan pembatalan dengan skrip multi-giliran yang dapat Anda jalankan sendiri:

<Accordion title="Perubahan effort membatalkan cache prompt">
  <Tabs>
    <Tab title="cURL">
      <Note>
        Alur kerja ini tidak cocok diterjemahkan ke perintah shell sekali jalan. Lihat tab SDK untuk pola multi-giliran; permintaan HTTP per giliran mengikuti contoh di halaman [Caching prompt](/docs/id/build-with-claude/prompt-caching).
      </Note>
    </Tab>

    <Tab title="CLI">
      <Note>
        Alur kerja ini tidak cocok diterjemahkan ke perintah shell sekali jalan. Lihat tab SDK untuk pola multi-giliran; pemanggilan CLI per giliran mengikuti contoh di halaman [Caching prompt](/docs/id/build-with-claude/prompt-caching).
      </Note>
    </Tab>

    <Tab title="Python">
      ```python
      import requests

      client = Anthropic()


      def fetch_article_content(url):
          text = requests.get(url).text
          lines = (line.strip() for line in text.splitlines())
          return "\n".join(line for line in lines if line)


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
          model="claude-opus-4-8",
          max_tokens=16000,
          thinking={"type": "adaptive"},
          messages=MESSAGES,
      )

      print(f"First response usage: {response1.usage}")

      MESSAGES.append({"role": "assistant", "content": response1.content})
      MESSAGES.append({"role": "user", "content": "Analyze the characters in this passage."})

      # Permintaan kedua - konfigurasi sama (cache hit diharapkan)
      print("\nSecond request - same configuration (cache hit expected)")
      response2 = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=16000,
          thinking={"type": "adaptive"},
          messages=MESSAGES,
      )

      print(f"Second response usage: {response2.usage}")

      MESSAGES.append({"role": "assistant", "content": response2.content})
      MESSAGES.append({"role": "user", "content": "Analyze the setting in this passage."})

      # Permintaan ketiga - tingkat effort berbeda (cache miss diharapkan)
      print("\nThird request - different effort level (cache miss expected)")
      response3 = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=16000,
          thinking={"type": "adaptive"},
          output_config={"effort": "medium"},
          messages=MESSAGES,
      )

      print(f"Third response usage: {response3.usage}")
      ```
    </Tab>

    <Tab title="TypeScript">
      ```typescript

      const client = new Anthropic();

      async function fetchArticleContent(url: string): Promise<string> {
        const response = await fetch(url);
        const text = await response.text();
        const lines = text.split("\n").map((line) => line.trim());
        return lines.filter((line) => line).join("\n");
      }

      const bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
      const bookContent = await fetchArticleContent(bookUrl);
      const LARGE_TEXT = bookContent.substring(0, 10000);

      // Tanpa prompt sistem - caching dilakukan di messages sebagai gantinya
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
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: { type: "adaptive" },
        messages
      });

      console.log("First response usage: ", response1.usage);

      messages.push(
        { role: "assistant", content: response1.content },
        { role: "user", content: "Analyze the characters in this passage." }
      );

      // Permintaan kedua - konfigurasi sama (diharapkan cache hit)
      console.log("\nSecond request - same configuration (cache hit expected)");
      const response2 = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: { type: "adaptive" },
        messages
      });

      console.log("Second response usage: ", response2.usage);

      messages.push(
        { role: "assistant", content: response2.content },
        { role: "user", content: "Analyze the setting in this passage." }
      );

      // Permintaan ketiga - tingkat effort berbeda (diharapkan cache miss)
      console.log("\nThird request - different effort level (cache miss expected)");
      const response3 = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: { type: "adaptive" },
        output_config: { effort: "medium" },
        messages
      });

      console.log("Third response usage: ", response3.usage);
      ```
    </Tab>

    <Tab title="C#">
      ```csharp
      AnthropicClient client = new();

      string bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
      string bookContent = await FetchArticleContent(bookUrl);
      string largeText = bookContent.Substring(0, Math.Min(10000, bookContent.Length));

      Console.WriteLine("First request - establishing cache");
      var parameters1 = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigAdaptive(),
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

      Console.WriteLine("\nSecond request - same configuration (cache hit expected)");
      var parameters2 = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigAdaptive(),
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

      Console.WriteLine("\nThird request - different effort level (cache miss expected)");
      var parameters3 = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigAdaptive(),
          OutputConfig = new OutputConfig
          {
              Effort = Effort.Medium
          },
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
    </Tab>

    <Tab title="Go">
      ```go
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
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 16000,
      	Thinking: anthropic.ThinkingConfigParamUnion{
      		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
      	},
      	Messages: messages,
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Printf("First response usage: %s\n", response1.Usage.RawJSON())

      messages = append(messages, response1.ToParam())
      messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the characters in this passage.")))

      // Permintaan kedua - konfigurasi sama (diharapkan cache hit)
      fmt.Println("\nSecond request - same configuration (cache hit expected)")
      response2, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 16000,
      	Thinking: anthropic.ThinkingConfigParamUnion{
      		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
      	},
      	Messages: messages,
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Printf("Second response usage: %s\n", response2.Usage.RawJSON())

      messages = append(messages, response2.ToParam())
      messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the setting in this passage.")))

      // Permintaan ketiga - tingkat effort berbeda (diharapkan cache miss)
      fmt.Println("\nThird request - different effort level (cache miss expected)")
      response3, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 16000,
      	Thinking: anthropic.ThinkingConfigParamUnion{
      		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
      	},
      	OutputConfig: anthropic.OutputConfigParam{
      		Effort: anthropic.OutputConfigEffortMedium,
      	},
      	Messages: messages,
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Printf("Third response usage: %s\n", response3.Usage.RawJSON())
      ```
    </Tab>

    <Tab title="Java">
      ```java
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
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(16000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
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

          // Permintaan kedua - konfigurasi yang sama (cache hit diharapkan)
          IO.println("\nSecond request - same configuration (cache hit expected)");
          MessageCreateParams params2 = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(16000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
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

          // Permintaan ketiga - tingkat upaya berbeda (cache miss diharapkan)
          IO.println("\nThird request - different effort level (cache miss expected)");
          MessageCreateParams params3 = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(16000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
              .outputConfig(OutputConfig.builder()
                  .effort(OutputConfig.Effort.MEDIUM)
                  .build())
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
    </Tab>

    <Tab title="PHP">
      ```php
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
          maxTokens: 16000,
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
          model: 'claude-opus-4-8',
          thinking: ['type' => 'adaptive'],
      );

      echo "First response usage: " . json_encode($response1->usage) . "\n";

      echo "\nSecond request - same configuration (cache hit expected)\n";
      $response2 = $client->messages->create(
          maxTokens: 16000,
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
          model: 'claude-opus-4-8',
          thinking: ['type' => 'adaptive'],
      );

      echo "Second response usage: " . json_encode($response2->usage) . "\n";

      echo "\nThird request - different effort level (cache miss expected)\n";
      $response3 = $client->messages->create(
          maxTokens: 16000,
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
          model: 'claude-opus-4-8',
          thinking: ['type' => 'adaptive'],
          outputConfig: ['effort' => 'medium'],
      );

      echo "Third response usage: " . json_encode($response3->usage) . "\n";
      ```
    </Tab>

    <Tab title="Ruby">
      ```ruby
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
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
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

      puts "\nSecond request - same configuration (cache hit expected)"
      response2 = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
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

      puts "\nThird request - different effort level (cache miss expected)"
      response3 = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        output_config: {
          effort: "medium"
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
    </Tab>
  </Tabs>

  Berikut adalah output dari skrip tersebut (Anda mungkin melihat angka yang sedikit berbeda):

  ```text Output wrap
  First request - establishing cache
  First response usage: { cache_creation_input_tokens: 3546, cache_read_input_tokens: 0, input_tokens: 15, output_tokens: 1033 }

  Second request - same configuration (cache hit expected)
  Second response usage: { cache_creation_input_tokens: 0, cache_read_input_tokens: 3546, input_tokens: 1062, output_tokens: 1630 }

  Third request - different effort level (cache miss expected)
  Third response usage: { cache_creation_input_tokens: 3546, cache_read_input_tokens: 0, input_tokens: 2706, output_tokens: 1468 }
  ```

  Dengan breakpoint cache di array messages, mengubah effort dari default `high` ke `medium` membatalkannya: permintaan ketiga menunjukkan `cache_creation_input_tokens=3546` dan `cache_read_input_tokens=0` sedangkan permintaan kedua menunjukkan pembacaan cache penuh.
</Accordion>

### Kontrol biaya

Anda tidak menetapkan budget token pemikiran. Dua kontrol membatasi biaya:

* `max_tokens` adalah batas keras pada total output untuk permintaan, gabungan pemikiran dan teks respons. Claude tidak pernah menghasilkan melewatinya. Dalam loop penggunaan alat, setiap permintaan dalam giliran memiliki `max_tokens` sendiri, jadi ini tidak membatasi pengeluaran seluruh giliran.
* `effort` adalah panduan lunak tentang seberapa banyak dari output tersebut yang dialokasikan Claude untuk pemikiran. Ini membentuk perilaku tetapi tidak menjamin jumlah token.

Karena pemikiran dihitung terhadap `max_tokens`, tetapkan cukup tinggi untuk menyisakan ruang bagi penalaran dan jawaban. `max_tokens` yang diukur untuk respons tanpa pemikiran sering kali terlalu kecil begitu Claude mulai berpikir pada permintaan yang sulit.

Pada effort `high` dan di atasnya, Claude mungkin berpikir secara ekstensif dan lebih mungkin menghabiskan budget. Jika Anda melihat [`stop_reason: "max_tokens"`](/docs/id/build-with-claude/thinking-troubleshooting#stopped-at-max-tokens) dalam respons, Anda memiliki dua solusi:

* Naikkan `max_tokens` untuk memberi model lebih banyak ruang untuk pemikiran plus jawaban.
* Turunkan tingkat effort sehingga Claude berpikir lebih sedikit dan menyisakan lebih banyak budget untuk teks respons.

Mana yang tepat tergantung pada apakah respons yang terpotong membutuhkan penalaran tersebut. Jika kualitas pada permintaan tersebut penting, naikkan batasnya; jika terlalu banyak dipikirkan, turunkan effort-nya.

## Harga

Pemikiran dikenakan biaya untuk:

* Token yang digunakan Claude saat berpikir (ditagih sebagai token output)
* Blok pemikiran dari giliran asisten sebelumnya yang tetap berada dalam konteks, sesuai [default preservasi](/docs/id/build-with-claude/thinking#thinking-block-preservation-by-model): semua giliran secara default pada model keep-all, hanya giliran terakhir di tempat lain (ditagih sebagai token input)
* Token output teks standar

<Note>
  Ketika pemikiran aktif, prompt sistem khusus secara otomatis disertakan untuk mendukung fitur ini.
</Note>

Apa yang ditagihkan kepada Anda sama terlepas dari pengaturan `display`; hanya apa yang Anda lihat yang berubah:

|                             | `display: "summarized"`                                      | `display: "omitted"`                          |
| --------------------------- | ------------------------------------------------------------ | --------------------------------------------- |
| **Token input**             | Token dalam permintaan asli Anda                             | Sama seperti summarized                       |
| **Token output (ditagih)**  | Token pemikiran penuh yang dihasilkan Claude secara internal | Sama seperti summarized                       |
| **Token output (terlihat)** | Teks pemikiran yang diringkas                                | Nol token pemikiran (field `thinking` kosong) |
| **Pembuatan ringkasan**     | Tanpa biaya                                                  | Tidak berlaku                                 |

<Warning>
  Jumlah token output yang ditagih **tidak** cocok dengan jumlah token yang terlihat dalam respons. Anda ditagih untuk proses pemikiran penuh, bukan konten pemikiran yang terlihat dalam respons.
</Warning>

Untuk melihat berapa banyak token output yang ditagih yang dihabiskan untuk penalaran internal, baca `usage.output_tokens_details.thinking_tokens` dalam respons. Nilai ini mencerminkan penalaran mentah yang dihasilkan model (bukan teks ringkasan yang dikembalikan dalam body) dan selalu kurang dari atau sama dengan `output_tokens`. Kurangkan dari `output_tokens` untuk memperkirakan bagian output yang bukan penalaran. Saat streaming, rincian ini hanya muncul pada event `message_delta` terakhir.

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

`output_tokens` tetap menjadi total inklusif dan otoritatif yang digunakan untuk penagihan. `output_tokens_details` adalah rincian hanya-baca untuk observabilitas. Untuk informasi harga lengkap termasuk tarif dasar, penulisan cache, cache hit, dan token output, lihat [Harga](/docs/id/about-claude/pricing).

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Pemikiran" icon="brain" href="/docs/id/build-with-claude/thinking">
    Aktifkan pemikiran, baca output pemikiran, dan periksa dukungan per model.
  </Card>

  <Card title="Pemikiran dalam alur kerja alat dan multi-giliran" icon="wrench" href="/docs/id/build-with-claude/thinking-tool-workflows">
    Pertahankan blok pemikiran di seluruh panggilan alat dan kelola pemikiran dalam percakapan multi-giliran.
  </Card>

  <Card title="Effort" icon="sliders" href="/docs/id/build-with-claude/effort">
    Kontrol seberapa banyak pemikiran dan output yang dialokasikan Claude per permintaan.
  </Card>
</CardGroup>
