---
source: platform
url: https://platform.claude.com/docs/id/models/sonnet-5/migration-guide
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 13d99f7437e6ccc03da680a274b183fc51261c68a3d0e05405d162235c920f43
---

---
title: Migrasi ke Claude Sonnet 5
url: https://platform.claude.com/docs/id/models/sonnet-5/migration-guide
description: "Migrasi ke Claude Sonnet 5 dari model Claude sebelumnya: ID model, perubahan yang merusak kompatibilitas, dan daftar periksa migrasi."
---

<Note>
  Panduan ini membahas migrasi kode [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak ada perubahan yang diperlukan selain memperbarui nama model.
</Note>

<Tip>
  **Otomatiskan migrasi Anda dengan skill Claude API.** Di Claude Code, jalankan `/claude-api migrate` untuk memanggil [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model) bawaan. Skill ini berfungsi untuk model Claude terkini mana pun sebagai target:

  ```text wrap
  /claude-api migrate this project to claude-sonnet-5
  ```

  Skill ini menerapkan penggantian ID model dan, sesuai kebutuhan, perubahan parameter yang bersifat breaking, penggantian prefill, serta kalibrasi effort untuk model target Anda di seluruh basis kode Anda, lalu menghasilkan daftar periksa berisi item yang perlu diverifikasi secara manual. Skill ini meminta Anda mengonfirmasi cakupan migrasi (seluruh direktori kerja, sebuah subdirektori, atau daftar file tertentu) sebelum mengedit file apa pun. Skill ini juga mendeteksi klien Amazon Bedrock dan Claude Platform on AWS serta menyesuaikan format ID model dan perubahan fitur untuk platform tersebut.
</Tip>

Claude Sonnet 5 menawarkan kombinasi terbaik antara kecepatan dan kecerdasan dalam keluarga model Claude. Model ini dibangun di atas Claude Sonnet 4.6.

Claude Sonnet 5 adalah peningkatan langsung (drop-in) untuk Claude Sonnet 4.6, dengan harga $2/$10 USD per juta token input/output; lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) untuk detailnya. Ada dua perubahan API yang merusak kompatibilitas untuk kode yang sudah berjalan di Claude Sonnet 4.6. Pertama, [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) aktif secara default dan "extended thinking" (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) mengembalikan error 400, sehingga permintaan yang sebelumnya berjalan tanpa thinking kini dapat mengembalikan blok `thinking` sebelum blok `text` pertama, dan kode yang membaca konten berdasarkan posisi harus memilih blok konten berdasarkan `type`. Kedua, parameter sampling (`temperature`, `top_p`, `top_k`) yang diatur ke nilai non-default mengembalikan error 400. Gunakan adaptive thinking dengan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking. Claude Sonnet 5 mendukung rangkaian fitur yang sama dengan Claude Sonnet 4.6, termasuk ["context window" (jendela konteks) 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows), [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking), ["prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching), [pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing), [Files API](https://platform.claude.com/docs/id/build-with-claude/files), [dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support), [vision](https://platform.claude.com/docs/id/build-with-claude/vision), dan rangkaian lengkap [alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien. Di Claude API dan Google Cloud, Claude Sonnet 5 juga mendukung [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) sebagai toolset stabil `computer_toolset_20260801` dan [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) untuk tugas di dalam halaman web, yang keduanya tidak didukung oleh Claude Sonnet 4.6; integrasi yang sudah ada pada versi `computer_20251124` sebelumnya tetap berfungsi tanpa perubahan di kedua model. Untuk meningkatkan integrasi yang sudah ada, lihat [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124). [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) tidak tersedia di Claude Sonnet 5. Claude Sonnet 5 juga menggunakan tokenizer baru.

## Migrasi ke Claude Sonnet 5 dari Claude Sonnet 4.6

<Note>
  Jika kode Anda menggunakan Claude Sonnet 4.5 atau yang lebih lama, terapkan juga [Migrasi ke Claude Sonnet 5 dari Claude Sonnet 4.5 dan model Sonnet sebelumnya](https://platform.claude.com/docs/id/models/sonnet-5/migration-guide#migrating-from-sonnet-45). Langkah-langkah tersebut mencakup perubahan yang merusak kompatibilitas (prefill pesan asisten ditolak, perbedaan escaping JSON parameter alat) yang tidak dicakup oleh bagian ini saja.
</Note>

### Perbarui nama model Anda

```python
# Migrasi Sonnet
model = "claude-sonnet-4-6"  # Before
model = "claude-sonnet-5"  # After
```

### Apa yang berubah

Butir 4 dan 5 dalam daftar berikut adalah perubahan yang merusak kompatibilitas. `max_tokens` tetap menjadi batas keras untuk total output (thinking ditambah teks respons), jadi tinjau kembali nilainya untuk beban kerja yang sebelumnya berjalan tanpa thinking di Claude Sonnet 4.6.

1. **Tokenizer baru:** Claude Sonnet 5 menggunakan tokenizer baru. Teks input yang sama menghasilkan sekitar 30% lebih banyak token dibandingkan di Claude Sonnet 4.6. Peningkatan pastinya bergantung pada kontennya. Permintaan, respons, dan event streaming tetap memiliki bentuk yang sama, dan tidak diperlukan perubahan kode, tetapi apa pun yang Anda ukur atau anggarkan dalam token akan bergeser: field `usage` dan hasil [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) untuk teks yang sama menjadi lebih tinggi, jendela konteks 1M token menampung lebih sedikit teks, dan batas `max_tokens` yang disesuaikan untuk Claude Sonnet 4.6 mungkin memotong output yang setara. Harga per token lebih rendah ($2/$10 USD dibandingkan $3/$15 USD per juta token input/output pada Claude Sonnet 4.6), tetapi biaya permintaan yang setara tidak turun secara proporsional langsung. Jalankan ulang penghitungan token terhadap Claude Sonnet 5 alih-alih menggunakan kembali hitungan yang diukur terhadap model sebelumnya.

2. **128k token output maksimum (tidak berubah):** Claude Sonnet 5 mendukung hingga 128k token output, sama seperti Claude Sonnet 4.6. Nilai `max_tokens` yang sudah ada tetap valid. Perhitungkan tokenizer baru saat menentukan ukurannya.

3. **Prefill pesan asisten (tidak berubah):** Melakukan prefill pada pesan asisten mengembalikan error `400` di Claude Sonnet 5, sama seperti di Claude Sonnet 4.6. Jika Anda telah menghapus prefill saat bermigrasi ke Claude Sonnet 4.6, tidak diperlukan perubahan lebih lanjut. Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

4. **Adaptive thinking aktif secara default:** Di Claude Sonnet 4.6, permintaan tanpa field `thinking` berjalan tanpa thinking; di Claude Sonnet 5, permintaan yang sama berjalan dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking). Untuk menonaktifkan thinking, kirimkan `thinking: {type: "disabled"}`. Extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung dan mengembalikan error 400. Gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) (default `high`) untuk mengontrol kedalaman thinking.

   Dengan thinking aktif, respons dapat dimulai dengan satu atau lebih blok `thinking` sebelum blok `text` pertama, yang dikembalikan dengan field `thinking` kosong pada default `display: "omitted"`. Kode yang membaca balasan berdasarkan posisi, seperti `content[0].text` atau handler stream yang memperlakukan blok konten pertama sebagai teks, harus memilih blok konten berdasarkan field `type`-nya, dan loop penggunaan alat harus mengirimkan kembali blok `thinking` secara lengkap dan tanpa modifikasi bersama hasil alatnya (lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks)). Token thinking ditagih sebagai token output meskipun teks thinking tidak dikembalikan. Jika Anda menggunakan thinking di Claude Sonnet 4.6 dan menampilkan teks thinking yang dikembalikan, perhatikan bahwa `thinking.display` memiliki default `"summarized"` di sana dan memiliki default `"omitted"` di Claude Sonnet 5; atur `display: "summarized"`, seperti pada contoh berikut, untuk tetap menerima ringkasan yang dapat dibaca (lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display)).

   <Tabs>
     <Tab title="Claude Sonnet 5">
       <Note>
         Adaptive thinking aktif secara default untuk Claude Sonnet 5. Field `thinking` ditampilkan secara eksplisit di sini untuk mengatur `display: "summarized"`; jika Anda menghilangkan `thinking`, Claude Sonnet 5 menghilangkan konten thinking dari respons secara default. Untuk default per model, lihat [Konfigurasi yang ditolak setiap model](https://platform.claude.com/docs/id/build-with-claude/thinking-troubleshooting#rejected-configurations).
       </Note>

       <CodeGroup>
         ```bash cURL
         curl https://api.anthropic.com/v1/messages \
           -H "x-api-key: $ANTHROPIC_API_KEY" \
           -H "anthropic-version: 2023-06-01" \
           -H "content-type: application/json" \
           -d '{
             "model": "claude-sonnet-5",
             "max_tokens": 16000,
             "thinking": {
               "type": "adaptive",
               "display": "summarized"
             },
             "output_config": {
               "effort": "high"
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
         ant messages create --transform content --format yaml <<'YAML'
         model: claude-sonnet-5
         max_tokens: 16000
         thinking:
           type: adaptive
           display: summarized
         output_config:
           effort: high
         messages:
           - role: user
             content: Are there an infinite number of prime numbers such that n mod 4 == 3?
         YAML
         ```

         ```python Python
         client = anthropic.Anthropic()

         response = client.messages.create(
             model="claude-sonnet-5",
             max_tokens=16000,
             thinking={"type": "adaptive", "display": "summarized"},
             output_config={"effort": "high"},
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
           model: "claude-sonnet-5",
           max_tokens: 16000,
           thinking: {
             type: "adaptive",
             display: "summarized"
           },
           output_config: {
             effort: "high"
           },
           messages: [
             {
               role: "user",
               content: "Are there an infinite number of prime numbers such that n mod 4 == 3?"
             }
           ]
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
             Model = Model.ClaudeSonnet5,
             MaxTokens = 16000,
             Thinking = new ThinkingConfigAdaptive { Display = Display.Summarized },
             OutputConfig = new OutputConfig { Effort = Effort.High },
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
         	Model:     anthropic.ModelClaudeSonnet5,
         	MaxTokens: 16000,
         	Thinking: anthropic.ThinkingConfigParamUnion{
         		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{
         			Display: anthropic.ThinkingConfigAdaptiveDisplaySummarized,
         		},
         	},
         	OutputConfig: anthropic.OutputConfigParam{
         		Effort: anthropic.OutputConfigEffortHigh,
         	},
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
         import com.anthropic.models.messages.OutputConfig;
         import com.anthropic.models.messages.ThinkingConfigAdaptive;

         void main() {
             var client = AnthropicOkHttpClient.fromEnv();

             var params = MessageCreateParams.builder()
                 .model(Model.CLAUDE_SONNET_5)
                 .maxTokens(16_000)
                 .thinking(ThinkingConfigAdaptive.builder()
                     .display(ThinkingConfigAdaptive.Display.SUMMARIZED)
                     .build())
                 .outputConfig(OutputConfig.builder()
                     .effort(OutputConfig.Effort.HIGH)
                     .build())
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
             model: 'claude-sonnet-5',
             maxTokens: 16000,
             thinking: ['type' => 'adaptive', 'display' => 'summarized'],
             outputConfig: ['effort' => 'high'],
             messages: [
                 [
                     'role' => 'user',
                     'content' => 'Are there an infinite number of prime numbers such that n mod 4 == 3?',
                 ],
             ],
         );

         // Respons berisi blok thinking yang diringkas dan blok teks
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
           model: "claude-sonnet-5",
           max_tokens: 16_000,
           thinking: {type: :adaptive, display: :summarized},
           output_config: {effort: :high},
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
     </Tab>

     <Tab title="Claude Sonnet 4.6">
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
     </Tab>
   </Tabs>

5. **Parameter sampling dihapus:** Parameter sampling (`temperature`, `top_p`, `top_k`) yang diatur ke nilai non-default tidak diterima dan mengembalikan error 400.

6. **Pengamanan keamanan siber:** Claude Sonnet 5 adalah model tingkat Sonnet pertama dengan pengamanan keamanan siber real-time. Permintaan yang melibatkan topik keamanan siber yang dilarang atau berisiko tinggi dapat ditolak. Penolakan dikembalikan sebagai respons HTTP 200 yang berhasil dengan `stop_reason: "refusal"`, bukan sebagai error. Lihat [Pengamanan siber real-time pada Claude Opus dan Sonnet](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet) untuk mengetahui apa yang diblokir oleh pengamanan tersebut dan bagaimana pekerjaan keamanan yang sah dapat mendaftar ke Cyber Verification Program.

### Daftar periksa migrasi

* Perbarui nama model dari `claude-sonnet-4-6` menjadi `claude-sonnet-5`.
* Jalankan ulang [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) terhadap Claude Sonnet 5. Tokenizer baru menghasilkan sekitar 30% lebih banyak token untuk teks yang sama, yang dapat mengubah biaya per permintaan meskipun harga per token lebih rendah. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja.
* Tinjau kembali batas `max_tokens` yang ukurannya mendekati panjang output yang Anda harapkan, dan naikkan hingga maksimum 128k (tidak berubah dari Claude Sonnet 4.6) jika berguna.
* Hapus konfigurasi `thinking: {type: "enabled", budget_tokens: N}` (mengembalikan error 400). Adaptive thinking aktif secara default; kirimkan `{type: "disabled"}` untuk menonaktifkannya, atau gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman.
* Perbarui parsing respons yang membaca konten berdasarkan posisi, seperti `content[0].text`: dengan thinking aktif, blok `thinking` tiba sebelum blok `text`. Pilih blok konten berdasarkan `type`, dan kirimkan kembali blok `thinking` tanpa modifikasi dalam loop penggunaan alat; blok yang dimodifikasi mengembalikan error 400.
* Verifikasi bahwa kode apa pun yang mem-parsing field `thinking` memperlakukannya hanya sebagai teks tampilan. `thinking.display` memiliki default `"omitted"` di Claude Sonnet 5 (sebelumnya memiliki default `"summarized"` di Claude Sonnet 4.6), sehingga blok thinking tiba dengan field `thinking` kosong; atur `display: "summarized"` untuk menerima ringkasan yang dapat dibaca. Lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).
* Hapus parameter `temperature`, `top_p`, dan `top_k` yang diatur ke nilai non-default (parameter tersebut mengembalikan error 400 di Claude Sonnet 5).
* Tambahkan penanganan untuk `stop_reason: "refusal"` jika beban kerja Anda mungkin menyentuh topik keamanan siber.
* Tetapkan ulang baseline biaya pada beban kerja tipikal Anda sebelum deployment produksi.
* Tinjau `max_tokens` untuk beban kerja yang sebelumnya berjalan tanpa thinking.

## Migrasi ke Claude Sonnet 5 dari Claude Sonnet 4.5 dan model Sonnet sebelumnya

Jika Anda bermigrasi dari Claude Sonnet 4.5 atau model Sonnet sebelumnya langsung ke Claude Sonnet 5, terapkan perubahan [Migrasi ke Claude Sonnet 5 dari Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/sonnet-5/migration-guide#migrating-from-claude-sonnet-4-6-to-claude-sonnet-5) ditambah perubahan di bagian ini.

<Warning>
  Claude Sonnet 5 memiliki default tingkat effort `high`, berbeda dengan Sonnet 4.5 yang tidak memiliki parameter effort. Pertimbangkan untuk menyesuaikan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) saat Anda bermigrasi. Jika tidak diatur secara eksplisit, Anda mungkin mengalami "latency" (latensi) yang lebih tinggi dengan tingkat effort default.
</Warning>

### Perubahan yang merusak kompatibilitas

#### Saat bermigrasi dari Sonnet 4.5

1. **Prefill pesan asisten tidak lagi didukung**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari Sonnet 4.5 atau yang lebih lama.
   </Warning>

   Prefill pesan asisten mengembalikan error `400` di Claude Sonnet 4.6 dan model yang lebih baru, termasuk Claude Sonnet 5. Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

   **Kasus penggunaan prefill yang umum dan migrasinya:**

   * **Mengontrol format output** (memaksa output JSON/YAML): Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) atau alat dengan field enum untuk tugas klasifikasi.

   * **Menghilangkan pembukaan** (menghapus frasa "Here is..."): Tambahkan instruksi langsung di prompt sistem: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc."

   * **Menghindari penolakan yang tidak tepat:** Claude kini jauh lebih baik dalam melakukan penolakan yang tepat. Prompting yang jelas dalam pesan pengguna tanpa prefill seharusnya sudah cukup.

   * **Kelanjutan** (melanjutkan respons yang terputus): Pindahkan kelanjutan ke pesan pengguna: "Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off."

   * **Hidrasi konteks / konsistensi peran** (menyegarkan konteks dalam percakapan panjang): Sisipkan pengingat yang sebelumnya berupa prefill asisten ke dalam giliran pengguna sebagai gantinya.

2. **Escaping JSON parameter alat mungkin berbeda**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari Sonnet 4.5 atau yang lebih lama.
   </Warning>

   Escaping string JSON dalam parameter alat mungkin berbeda dari model sebelumnya. Parser JSON standar menangani hal ini secara otomatis, tetapi parsing berbasis string kustom mungkin perlu diperbarui.

**Perubahan extended thinking:** Konfigurasi `budget_tokens` dari Claude Sonnet 4.5 (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung di Claude Sonnet 5 dan mengembalikan error 400. Adaptive thinking aktif secara default, sehingga sebagian besar beban kerja tidak memerlukan konfigurasi `thinking` sama sekali; gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking. Jika Anda menjalankan Claude Sonnet 4.5 tanpa extended thinking, kirimkan `thinking: {type: "disabled"}` untuk mempertahankan perilaku tersebut.

#### Saat bermigrasi dari Claude 3.x

3. **Hapus parameter sampling**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
   </Warning>

   Parameter sampling (`temperature`, `top_p`, `top_k`) yang diatur ke nilai non-default mengembalikan error 400 di Claude Sonnet 5. Hapus parameter tersebut dari permintaan, dan gunakan prompting untuk memandu perilaku model sebagai gantinya.

4. **Perbarui versi alat**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20260521`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

5. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

## Migrasi ke Claude Sonnet 5 dari Claude Haiku 4.5

Claude Haiku 4.5 dan Claude Sonnet 5 lebih berbeda di tingkat API dibandingkan model yang berdekatan dalam satu kelas: Claude Haiku 4.5 menggunakan [extended thinking](https://platform.claude.com/docs/id/build-with-claude/extended-thinking) manual (nonaktif secara default), jendela konteks 200k token, dan hingga 64k token output, sedangkan Claude Sonnet 5 berjalan dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) aktif secara default, menyediakan [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, dan mendukung hingga [128k token output](https://platform.claude.com/docs/id/models/overview).

### Perbarui nama model Anda

```python
model = "claude-haiku-4-5-20251001"  # Before
model = "claude-sonnet-5"  # After
```

### Apa yang berubah

1. **Konfigurasi thinking:** Claude Haiku 4.5 mendukung extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) dan menolak `thinking: {type: "adaptive"}`. Di Claude Sonnet 5, dukungannya terbalik: adaptive thinking aktif secara default, dan extended thinking manual mengembalikan error 400. Hapus konfigurasi `thinking: {type: "enabled", budget_tokens: N}` dan andalkan default, atau kirimkan `thinking: {type: "disabled"}` untuk menonaktifkan thinking. `budget_tokens` tidak memiliki pengganti langsung; gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking. Effort tidak tersedia di Claude Haiku 4.5 dan memiliki default `high` di Claude Sonnet 5.

   Bentuk respons berubah untuk kedua jenis permintaan Claude Haiku 4.5. Permintaan yang sebelumnya berjalan tanpa extended thinking kini dapat mengembalikan satu atau lebih blok `thinking` sebelum blok `text` pertama, sehingga kode yang membaca balasan berdasarkan posisi, seperti `content[0].text`, harus memilih blok konten berdasarkan field `type`-nya, dan loop penggunaan alat harus mengirimkan kembali blok `thinking` secara lengkap dan tanpa modifikasi bersama hasil alatnya (lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks)). Permintaan yang menggunakan extended thinking tetap menerima blok `thinking`, tetapi `thinking.display` memiliki default `"omitted"` di Claude Sonnet 5 alih-alih `"summarized"`, sehingga blok tersebut tiba dengan field `thinking` kosong; atur `display: "summarized"` untuk tetap menerima ringkasan yang dapat dibaca (lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display)). Token thinking ditagih sebagai token output meskipun teks thinking tidak dikembalikan.

2. **Parameter sampling dihapus:** `temperature` dan `top_p` berfungsi di Claude Haiku 4.5 (satu per satu, tidak keduanya). Di Claude Sonnet 5, mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default mengembalikan error 400. Hapus parameter ini dan gunakan prompting untuk memandu perilaku model.

3. **Prefill asisten dihapus:** Melakukan prefill pada pesan asisten berfungsi di Claude Haiku 4.5 tetapi mengembalikan error 400 di Claude Sonnet 5. Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

4. **Jendela konteks dan output yang lebih besar:** Claude Sonnet 5 menyediakan jendela konteks 1M token secara default, naik dari 200k token di Claude Haiku 4.5, dan mendukung hingga 128k token output, naik dari 64k. Claude Sonnet 5 juga menggunakan tokenizer yang berbeda, jadi jalankan ulang [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) alih-alih menggunakan kembali hitungan yang diukur terhadap Claude Haiku 4.5.

5. **Harga:** Claude Haiku 4.5 dihargai $1/$5 USD per juta token input/output. Claude Sonnet 5 dihargai $2/$10 USD per juta token input/output. Lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).

6. **Pengamanan keamanan siber:** Claude Sonnet 5 memiliki pengamanan keamanan siber real-time. Permintaan yang melibatkan topik keamanan siber yang dilarang atau berisiko tinggi dapat ditolak, dikembalikan sebagai respons HTTP 200 yang berhasil dengan `stop_reason: "refusal"`. Lihat [Pengamanan siber real-time pada Claude Opus dan Sonnet](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet) untuk mengetahui apa yang diblokir oleh pengamanan tersebut dan bagaimana pekerjaan keamanan yang sah dapat mendaftar ke Cyber Verification Program.

### Daftar periksa migrasi

* Perbarui nama model dari `claude-haiku-4-5-20251001` (atau alias `claude-haiku-4-5`) menjadi `claude-sonnet-5`.
* Hapus konfigurasi `thinking: {type: "enabled", budget_tokens: N}` (mengembalikan error 400). Adaptive thinking aktif secara default; kirimkan `thinking: {type: "disabled"}` untuk mempertahankan perilaku tanpa thinking, dan tinjau kembali `max_tokens` untuk beban kerja yang sebelumnya berjalan tanpa thinking.
* Perbarui parsing respons yang membaca konten berdasarkan posisi, seperti `content[0].text`: dengan thinking aktif, blok `thinking` tiba sebelum blok `text`. Pilih blok konten berdasarkan `type`, dan kirimkan kembali blok `thinking` tanpa modifikasi dalam loop penggunaan alat; blok yang dimodifikasi mengembalikan error 400.
* Jika UI Anda menampilkan konten thinking, atur `display: "summarized"`. `thinking.display` memiliki default `"omitted"` di Claude Sonnet 5, sehingga jika tidak diatur, blok thinking tiba dengan field `thinking` kosong. Lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display).
* Gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) (default `high`) untuk mengontrol kedalaman thinking dan pengeluaran token; parameter ini tidak tersedia di Claude Haiku 4.5, sehingga tidak ada pengaturan yang sudah ada yang terbawa.
* Hapus pengaturan `temperature` dan `top_p` (nilai non-default mengembalikan error 400 di Claude Sonnet 5).
* Hapus prefill pesan asisten apa pun (prefill tersebut mengembalikan error 400 di Claude Sonnet 5).
* Jalankan ulang [penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) terhadap Claude Sonnet 5, dan tinjau kembali batas `max_tokens`, yang dapat Anda naikkan hingga maksimum 128k.
* Tambahkan penanganan untuk `stop_reason: "refusal"` jika beban kerja Anda mungkin menyentuh topik keamanan siber.
* Tetapkan ulang baseline biaya pada beban kerja tipikal Anda sebelum deployment produksi; harga per token berbeda.
