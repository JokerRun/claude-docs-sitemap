---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/migration-guide
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: e94cfac52bd1793e10b1b83d681c21f621abf1b5cb4d2a55fced3b36da8de232
---

# Panduan migrasi

Panduan untuk bermigrasi ke model Claude terbaru dari versi Claude sebelumnya

---

<Note>
  Panduan ini mencakup migrasi kode [Messages API](/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](/docs/id/managed-agents/overview), tidak ada perubahan yang diperlukan selain memperbarui nama model.
</Note>

<Tip>
  **Otomatiskan migrasi Anda dengan skill Claude API.** Di Claude Code, jalankan `/claude-api migrate` untuk memanggil [skill Claude API](/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model) yang sudah disertakan. Skill ini bekerja untuk model target mana pun di halaman ini:

  ```text wrap
  /claude-api migrate this project to claude-opus-4-8
  ```

  Skill ini menerapkan penggantian ID model dan, sesuai kebutuhan, perubahan parameter yang bersifat breaking, penggantian prefill, dan kalibrasi effort untuk model target Anda di seluruh basis kode Anda, lalu menghasilkan daftar periksa item yang perlu diverifikasi secara manual. Skill ini meminta Anda mengonfirmasi cakupan migrasi (seluruh direktori kerja, subdirektori, atau daftar file tertentu) sebelum mengedit file apa pun. Skill ini juga mendeteksi klien Amazon Bedrock, Claude Platform on AWS, Google Cloud, dan Microsoft Foundry serta menyesuaikan format ID model dan perubahan fitur untuk setiap platform.
</Tip>

## Bermigrasi ke Claude Mythos 5

[Claude Mythos 5](https://anthropic.com/glasswing) adalah model dengan akses terbatas yang ditawarkan dalam ketersediaan terbatas kepada pelanggan yang disetujui dalam Project Glasswing. Model ini memiliki spesifikasi dan harga yang sama dengan [Claude Fable 5](/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5): [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) secara default, dan hingga 128k token output per permintaan.

Pengaturan dasar untuk `claude-mythos-5`:

* **Thinking:** [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) selalu aktif. Model menentukan kapan dan seberapa banyak berpikir pada setiap permintaan, dan tidak diperlukan konfigurasi `thinking`. Baik `thinking: {type: "disabled"}` maupun extended thinking (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) mengembalikan error 400.
* **Prefill:** Melakukan prefill pada pesan assistant mengembalikan error 400. Gunakan instruksi prompt sistem sebagai gantinya.
* **Retensi data:** Claude Mythos 5 memerlukan retensi data 30 hari dan tidak tersedia di bawah pengaturan zero data retention (ZDR); model ini ditetapkan sebagai Covered Model. Lihat [Persyaratan retensi data spesifik model](/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).

### Bermigrasi ke Claude Mythos 5 dari Claude Mythos Preview

[Claude Mythos 5](https://anthropic.com/glasswing) adalah penerus dengan akses terbatas dari [Claude Mythos Preview](https://anthropic.com/glasswing), pratinjau riset khusus undangan. Untuk model yang tersedia secara umum dengan kemampuan yang sama, lihat [Claude Fable 5](/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5).

Migrasi sebagian besar bersifat drop-in. Claude Mythos 5 menggunakan [Messages API](/docs/id/build-with-claude/working-with-messages) yang sama dan pola [penggunaan alat](/docs/id/agents-and-tools/tool-use/overview) yang sama dengan Claude Mythos Preview, dan jumlah token kurang lebih tidak berubah karena kedua model menggunakan tokenizer yang sama. Perubahan utama yang perlu diperiksa adalah fitur-fitur yang tidak lagi tersedia (tercantum di bagian berikutnya) dan output thinking.

Untuk linimasa penghentian Claude Mythos Preview, lihat [Penghentian model](/docs/id/about-claude/model-deprecations).

#### Perbarui nama model Anda

```python
model = "claude-mythos-preview"  # Before
model = "claude-mythos-5"  # After
```

#### Fitur yang tidak tersedia di Claude Mythos 5

1. **Extended thinking dan anggaran token thinking:** Extended thinking (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung di `claude-mythos-5` dan mengembalikan error 400. [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) selalu aktif: model menentukan kapan dan seberapa banyak berpikir pada setiap permintaan, dan tidak diperlukan konfigurasi `thinking`. `thinking: {type: "disabled"}` mengembalikan error. `budget_tokens` tidak memiliki pengganti langsung: thinking bersifat adaptif, dan [parameter effort](/docs/id/build-with-claude/effort) adalah kontrol tingkat output yang terpisah, bukan anggaran thinking.

   Sebelum (Claude Mythos Preview):

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -H "content-type: application/json" \
       -d '{
         "model": "claude-mythos-preview",
         "max_tokens": 16000,
         "thinking": {
           "type": "enabled",
           "budget_tokens": 10000
         },
         "messages": [
           {
             "role": "user",
             "content": "..."
           }
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-mythos-preview
     max_tokens: 16000
     thinking:
       type: enabled
       budget_tokens: 10000
     messages:
       - role: user
         content: "..."
     YAML
     ```

     ```python Python
     client.messages.create(
         model="claude-mythos-preview",
         max_tokens=16000,
         thinking={"type": "enabled", "budget_tokens": 10000},
         messages=[{"role": "user", "content": "..."}],
     )
     ```

     ```typescript TypeScript
     await client.messages.create({
       model: "claude-mythos-preview",
       max_tokens: 16000,
       thinking: { type: "enabled", budget_tokens: 10000 },
       messages: [{ role: "user", content: "..." }]
     });
     ```

     ```csharp C#
     using Anthropic;
     using Anthropic.Models.Messages;

     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = "claude-mythos-preview",
         MaxTokens = 16000,
         Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
         Messages = [new() { Role = Role.User, Content = "..." }]
     };

     var response = await client.Messages.Create(parameters);
     Console.WriteLine(response);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     "claude-mythos-preview",
     	MaxTokens: 16000,
     	Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
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
         .model("claude-mythos-preview")
         .maxTokens(16000L)
         .enabledThinking(10000L)
         .addUserMessage("...")
         .build();

     Message response = client.messages().create(params);
     IO.println(response);
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => '...']],
         model: 'claude-mythos-preview',
         thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: "claude-mythos-preview",
       max_tokens: 16000,
       thinking: {
         type: "enabled",
         budget_tokens: 10000
       },
       messages: [
         { role: "user", content: "..." }
       ]
     )
     ```
   </CodeGroup>

   Sesudah (Claude Mythos 5):

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -H "content-type: application/json" \
       -d '{
         "model": "claude-mythos-5",
         "max_tokens": 16000,
         "messages": [
           {
             "role": "user",
             "content": "..."
           }
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-mythos-5
     max_tokens: 16000
     messages:
       - role: user
         content: "..."
     YAML
     ```

     ```python Python
     client.messages.create(
         model="claude-mythos-5",
         max_tokens=16000,
         messages=[{"role": "user", "content": "..."}],
     )
     ```

     ```typescript TypeScript
     await client.messages.create({
       model: "claude-mythos-5",
       max_tokens: 16000,
       messages: [{ role: "user", content: "..." }]
     });
     ```

     ```csharp C#
     using Anthropic;
     using Anthropic.Models.Messages;

     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = "claude-mythos-5",
         MaxTokens = 16000,
         Messages = [new() { Role = Role.User, Content = "..." }]
     };

     var response = await client.Messages.Create(parameters);
     Console.WriteLine(response);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     "claude-mythos-5",
     	MaxTokens: 16000,
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
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
         .model("claude-mythos-5")
         .maxTokens(16000L)
         .addUserMessage("...")
         .build();

     Message response = client.messages().create(params);
     IO.println(response);
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => '...']],
         model: 'claude-mythos-5',
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: "claude-mythos-5",
       max_tokens: 16000,
       messages: [
         { role: "user", content: "..." }
       ]
     )
     ```
   </CodeGroup>

2. **Prefill assistant:** Melakukan prefill pada pesan assistant tidak didukung di `claude-mythos-5` dan mengembalikan error 400, sama seperti di Claude Mythos Preview. Gunakan instruksi prompt sistem sebagai gantinya.

3. **Output thinking:** Di `claude-mythos-5`, rantai pemikiran mentah tidak pernah dikembalikan, tetapi blok thinking tetap membawa teks ringkasan yang dapat dibaca ketika `thinking.display` diatur ke `summarized`. Kirimkan kembali blok thinking tanpa perubahan saat melanjutkan percakapan pada model yang sama. Lihat [Output thinking di Claude Fable 5 dan Claude Mythos 5](/docs/id/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).

#### Penghitungan token dan penagihan

`claude-mythos-5` menggunakan tokenizer yang sama dengan `claude-mythos-preview` (tokenizer yang diperkenalkan dengan Claude Opus 4.7). Jumlah token kurang lebih tidak berubah saat bermigrasi dari `claude-mythos-preview`. Dibandingkan dengan model sebelum Claude Opus 4.7, konten yang sama dapat ditokenisasi menjadi sekitar 30% lebih banyak token, bervariasi menurut konten dan bentuk beban kerja.

[`/v1/messages/count_tokens`](/docs/id/build-with-claude/token-counting) mengembalikan nilai yang kurang lebih tidak berubah untuk `claude-mythos-5` dibandingkan dengan `claude-mythos-preview`. Lakukan baseline ulang biaya dan latensi pada beban kerja Anda sendiri.

#### Daftar periksa migrasi

* Perbarui nama model dari `claude-mythos-preview` ke `claude-mythos-5`.
* Hapus konfigurasi extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`). Adaptive thinking selalu aktif, dan tidak diperlukan field `thinking`.
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun. Menonaktifkan thinking mengembalikan error di `claude-mythos-5`.
* Hapus `budget_tokens`. Parameter ini tidak memiliki pengganti langsung: thinking bersifat adaptif, dan parameter `effort` adalah kontrol tingkat output yang terpisah, bukan anggaran thinking.
* Verifikasi bahwa kode apa pun yang mem-parsing field `thinking` memperlakukannya hanya sebagai teks tampilan dan mengirimkan kembali blok thinking tanpa perubahan saat melanjutkan pada model yang sama. `thinking.display` secara default bernilai `"omitted"` di `claude-mythos-5`, sama seperti di Claude Mythos Preview; atur `display: "summarized"` untuk menerima ringkasan yang dapat dibaca. Lihat [Output thinking di Claude Fable 5 dan Claude Mythos 5](/docs/id/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).
* Jika Anda memutar ulang riwayat percakapan pada model lain, hapus blok `thinking` dan `redacted_thinking` dari giliran assistant sebelumnya terlebih dahulu. Blok thinking dari `claude-mythos-5` terikat pada model yang menghasilkannya, dan model selain Claude Fable 5 dan Claude Mythos 5 mengabaikannya secara diam-diam. Penghapusan ini menjaga permintaan lintas model tetap minimal dan seragam.
* Lakukan baseline ulang jumlah token dan biaya pada beban kerja Anda sendiri. Jumlah token kurang lebih tidak berubah saat bermigrasi dari `claude-mythos-preview`.

## Bermigrasi ke Claude Fable 5

[Claude Fable 5](/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) adalah model paling mumpuni dari Anthropic yang dirilis secara luas, tersedia secara umum di Claude API, [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry).

Migrasi sebagian besar bersifat drop-in. Claude Fable 5 menggunakan [Messages API](/docs/id/build-with-claude/working-with-messages) yang sama dan pola [penggunaan alat](/docs/id/agents-and-tools/tool-use/overview) yang sama dengan Claude Opus 4.8. Model ini mendukung [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) yang sama secara default dan [maksimum 128k token output](/docs/id/about-claude/models/overview) yang sama. Jumlah token kurang lebih tidak berubah karena kedua model menggunakan tokenizer yang sama.

Perubahan utama yang perlu diperiksa adalah [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) yang selalu aktif, output thinking, penolakan safety classifier, dan harga. [Sebelum Anda bermigrasi](#before-you-migrate) mencakup harga dan retensi data; [Apa yang berubah](#what-changed) mencakup sisanya.

### Sebelum Anda bermigrasi

Claude Fable 5 dihargai $10 USD per juta token input dan $50 USD per juta token output, dibandingkan dengan $5 USD dan $25 USD untuk Claude Opus 4.8. Lihat [Harga Claude](/docs/id/about-claude/pricing) untuk detailnya.

Claude Fable 5 memerlukan retensi data 30 hari dan tidak tersedia di bawah pengaturan zero data retention (ZDR); model ini ditetapkan sebagai Covered Model. Di Claude API, permintaan dari organisasi yang konfigurasi retensi datanya tidak memenuhi persyaratan ini mengembalikan `invalid_request_error` 400. Organisasi dengan pengaturan ZDR harus menghubungi tim akun Anthropic mereka untuk mendiskusikan konfigurasi retensi data; Claude Opus 4.8 tetap tersedia di bawah ZDR. Sebagai alternatif, Anda dapat mengonfigurasi retensi data per workspace. Persyaratan retensi data 30 hari berlaku di setiap platform tempat Claude Fable 5 ditawarkan; lihat [Persyaratan retensi data spesifik model](/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements) untuk detail per platform.

<Note>
  Jika kode Anda berada di Claude Opus 4.7 atau lebih lama, terapkan terlebih dahulu sub-bagian [Bermigrasi ke Claude Opus 4.8](#migrating-to-claude-opus-4-8) yang relevan untuk model Anda saat ini. Bagian-bagian tersebut mencakup perubahan yang bersifat breaking (parameter sampling ditolak, extended thinking manual ditolak, prefill dihapus, tokenizer baru) yang tidak diulang di bagian ini.
</Note>

### Bermigrasi ke Claude Fable 5 dari Claude Opus 4.8

#### Perbarui nama model Anda

```python
model = "claude-opus-4-8"  # Before
model = "claude-fable-5"  # After
```

#### Apa yang berubah

Item-item di bagian ini menjelaskan perbedaan API dan perilaku yang perlu diperiksa setelah Anda mengganti ID model.

1. **Adaptive thinking selalu aktif:** [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) adalah satu-satunya mode thinking di `claude-fable-5`. Model menentukan kapan dan seberapa banyak berpikir pada setiap permintaan, dan tidak diperlukan konfigurasi `thinking`. `thinking: {type: "disabled"}` mengembalikan error. Gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking.

   Perubahan perilaku yang perlu diperiksa: di Claude Opus 4.8, permintaan tanpa field `thinking` berjalan tanpa thinking; di `claude-fable-5`, permintaan yang sama berjalan dengan adaptive thinking. `max_tokens` tetap menjadi batas keras pada total output, thinking ditambah teks respons, jadi tinjau kembali untuk beban kerja yang berjalan tanpa thinking di Claude Opus 4.8. Lihat [Kontrol biaya](/docs/id/build-with-claude/adaptive-thinking#cost-control).

   Sebelum (Claude Opus 4.8):

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
           "type": "adaptive"
         },
         "output_config": {
           "effort": "high"
         },
         "messages": [
           {
             "role": "user",
             "content": "..."
           }
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-opus-4-8
     max_tokens: 16000
     thinking:
       type: adaptive
     output_config:
       effort: high
     messages:
       - role: user
         content: "..."
     YAML
     ```

     ```python Python
     client.messages.create(
         model="claude-opus-4-8",
         max_tokens=16000,
         thinking={"type": "adaptive"},
         output_config={"effort": "high"},
         messages=[{"role": "user", "content": "..."}],
     )
     ```

     ```typescript TypeScript
     await client.messages.create({
       model: "claude-opus-4-8",
       max_tokens: 16000,
       thinking: { type: "adaptive" },
       output_config: { effort: "high" },
       messages: [{ role: "user", content: "..." }]
     });
     ```

     ```csharp C#
     using Anthropic;
     using Anthropic.Models.Messages;

     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = "claude-opus-4-8",
         MaxTokens = 16000,
         Thinking = new ThinkingConfigAdaptive(),
         OutputConfig = new OutputConfig { Effort = Effort.High },
         Messages = [new() { Role = Role.User, Content = "..." }]
     };

     var response = await client.Messages.Create(parameters);
     Console.WriteLine(response);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     "claude-opus-4-8",
     	MaxTokens: 16000,
     	Thinking: anthropic.ThinkingConfigParamUnion{
     		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
     	},
     	OutputConfig: anthropic.OutputConfigParam{
     		Effort: anthropic.OutputConfigEffortHigh,
     	},
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
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
         .model("claude-opus-4-8")
         .maxTokens(16000L)
         .thinking(ThinkingConfigAdaptive.builder().build())
         .outputConfig(OutputConfig.builder()
             .effort(OutputConfig.Effort.HIGH)
             .build())
         .addUserMessage("...")
         .build();

     Message response = client.messages().create(params);
     IO.println(response);
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => '...']],
         model: 'claude-opus-4-8',
         thinking: ['type' => 'adaptive'],
         outputConfig: ['effort' => 'high'],
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: "claude-opus-4-8",
       max_tokens: 16000,
       thinking: {
         type: "adaptive"
       },
       output_config: {
         effort: "high"
       },
       messages: [
         { role: "user", content: "..." }
       ]
     )
     ```
   </CodeGroup>

   Sesudah (Claude Fable 5):

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -H "content-type: application/json" \
       -d '{
         "model": "claude-fable-5",
         "max_tokens": 16000,
         "output_config": {
           "effort": "high"
         },
         "messages": [
           {
             "role": "user",
             "content": "..."
           }
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-fable-5
     max_tokens: 16000
     output_config:
       effort: high
     messages:
       - role: user
         content: "..."
     YAML
     ```

     ```python Python
     client.messages.create(
         model="claude-fable-5",
         max_tokens=16000,
         output_config={"effort": "high"},
         messages=[{"role": "user", "content": "..."}],
     )
     ```

     ```typescript TypeScript
     await client.messages.create({
       model: "claude-fable-5",
       max_tokens: 16000,
       output_config: { effort: "high" },
       messages: [{ role: "user", content: "..." }]
     });
     ```

     ```csharp C#
     using Anthropic;
     using Anthropic.Models.Messages;

     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = "claude-fable-5",
         MaxTokens = 16000,
         OutputConfig = new OutputConfig { Effort = Effort.High },
         Messages = [new() { Role = Role.User, Content = "..." }]
     };

     var response = await client.Messages.Create(parameters);
     Console.WriteLine(response);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     "claude-fable-5",
     	MaxTokens: 16000,
     	OutputConfig: anthropic.OutputConfigParam{
     		Effort: anthropic.OutputConfigEffortHigh,
     	},
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
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
         .model("claude-fable-5")
         .maxTokens(16000L)
         .outputConfig(OutputConfig.builder()
             .effort(OutputConfig.Effort.HIGH)
             .build())
         .addUserMessage("...")
         .build();

     Message response = client.messages().create(params);
     IO.println(response);
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => '...']],
         model: 'claude-fable-5',
         outputConfig: ['effort' => 'high'],
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: "claude-fable-5",
       max_tokens: 16000,
       output_config: {
         effort: "high"
       },
       messages: [
         { role: "user", content: "..." }
       ]
     )
     ```
   </CodeGroup>

2. **Extended thinking dan anggaran thinking (tidak berubah):** Extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung di `claude-fable-5` dan mengembalikan error 400, sama seperti di Claude Opus 4.8. `budget_tokens` tidak memiliki pengganti langsung: thinking bersifat adaptif, dan [parameter effort](/docs/id/build-with-claude/effort) adalah kontrol tingkat output yang terpisah, bukan anggaran thinking.

3. **Prefill assistant (tidak berubah):** Melakukan prefill pada pesan assistant tidak didukung di `claude-fable-5` dan mengembalikan error 400, sama seperti di Claude Opus 4.8. Gunakan instruksi prompt sistem sebagai gantinya.

4. **Output thinking:** Di `claude-fable-5`, rantai pemikiran mentah tidak pernah dikembalikan, tetapi blok thinking tetap membawa teks ringkasan yang dapat dibaca ketika `thinking.display` diatur ke `summarized`. Kirimkan kembali blok thinking tanpa perubahan saat melanjutkan percakapan pada model yang sama. Lihat [Output thinking di Claude Fable 5 dan Claude Mythos 5](/docs/id/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).

5. **Safety classifier dan stop reason `refusal`:** `claude-fable-5` menjalankan safety classifier pada permintaan dan selama pembuatan respons. Ketika sebuah classifier menolak permintaan, Messages API mengembalikan `stop_reason: "refusal"` sebagai respons HTTP 200 yang berhasil, bukan error. Field `stop_details.category` melaporkan classifier mana yang terpicu, dengan kategori seperti `"cyber"`, `"bio"`, dan `"reasoning_extraction"`, atau `null` ketika penolakan tidak terpetakan ke kategori bernama mana pun. Lihat [tabel kategori penolakan](/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk daftar lengkapnya.

   Anda tidak ditagih untuk token input dari permintaan yang ditolak sebelum output apa pun dihasilkan. Ketika classifier terpicu di tengah stream, input dan output yang sudah di-stream akan ditagih; buang output parsial tersebut.

   Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, kirimkan parameter opt-in `fallbacks`, yang berada dalam beta di Claude API dan Claude Platform on AWS. Parameter ini tidak tersedia di Message Batches API atau di Amazon Bedrock, Google Cloud, dan Microsoft Foundry; di ketiga platform tersebut, jalankan percobaan ulang di sisi klien atau gunakan middleware refusal-fallback SDK. Lihat [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback).

6. **Mulai dari effort `high`:** Default [parameter effort](/docs/id/build-with-claude/effort) tetap `high`. Di Claude Opus 4.8, rekomendasi untuk pekerjaan coding dan otonomi tinggi adalah mengatur `xhigh` secara eksplisit. Di `claude-fable-5`, gunakan `high` sebagai default untuk sebagian besar tugas dan simpan `xhigh` untuk beban kerja yang paling sensitif terhadap kemampuan. Pengaturan effort yang lebih rendah di `claude-fable-5` tetap berkinerja baik dan sering melampaui kinerja `xhigh` pada model sebelumnya. Kurangi effort jika tugas selesai tetapi memakan waktu lebih lama dari yang diperlukan. Lihat [Prompting Claude Fable 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5#consider-all-effort-levels).

7. **Minimum caching prompt yang lebih rendah:** Panjang prompt minimum yang dapat di-cache di `claude-fable-5` adalah 512 token, lebih rendah dari 1.024 token di Claude Opus 4.8. Prompt yang terlalu pendek untuk di-cache di Claude Opus 4.8 sekarang dapat membuat entri cache, tanpa perlu perubahan kode. Di Amazon Bedrock, minimum untuk `claude-fable-5` adalah 1.024 token. Lihat [Caching prompt](/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

#### Daftar periksa migrasi

* Jika organisasi Anda memiliki pengaturan zero data retention (ZDR), konfirmasikan kelayakan sebelum bermigrasi. `claude-fable-5` memerlukan retensi data 30 hari dan, di Claude API, mengembalikan `invalid_request_error` 400 jika tidak terpenuhi. Lihat [Persyaratan retensi data spesifik model](/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Perbarui nama model dari `claude-opus-4-8` ke `claude-fable-5`.
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun. Menonaktifkan thinking mengembalikan error di `claude-fable-5`, dan permintaan tanpa field `thinking` berjalan dengan adaptive thinking.
* Jika Anda telah menghapus extended thinking manual dan prefill assistant selama migrasi sebelumnya, tidak ada tindakan yang diperlukan: keduanya tetap tidak didukung di `claude-fable-5`.
* Verifikasi bahwa kode apa pun yang mem-parsing field `thinking` memperlakukannya hanya sebagai teks tampilan dan mengirimkan kembali blok thinking tanpa perubahan saat melanjutkan pada model yang sama. `thinking.display` secara default bernilai `"omitted"` di `claude-fable-5`, sama seperti di Claude Opus 4.8; atur `display: "summarized"` untuk menerima ringkasan yang dapat dibaca. Lihat [Output thinking di Claude Fable 5 dan Claude Mythos 5](/docs/id/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).
* Jika Anda memutar ulang riwayat percakapan pada model lain, hapus blok `thinking` dan `redacted_thinking` dari giliran assistant sebelumnya terlebih dahulu. Blok thinking dari `claude-fable-5` terikat pada model yang menghasilkannya, dan model selain Claude Fable 5 dan Claude Mythos 5 mengabaikannya secara diam-diam. Penghapusan ini menjaga permintaan lintas model tetap minimal dan seragam. Pengecualiannya adalah menukarkan [kredit fallback](/docs/id/build-with-claude/fallback-credit), yang memerlukan body permintaan yang digemakan kembali sesuai aturan persis fitur tersebut.
* Tangani `stop_reason: "refusal"` dan baca field `stop_details.category`. Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, pertimbangkan parameter opt-in `fallbacks` (beta). Lihat [Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback).
* Evaluasi ulang pengaturan `effort` Anda. Mulai dari `high` untuk sebagian besar tugas, termasuk beban kerja yang berjalan pada `xhigh` di Claude Opus 4.8.
* Lakukan baseline ulang biaya dan latensi pada beban kerja Anda sendiri. Jumlah token kurang lebih tidak berubah saat bermigrasi dari `claude-opus-4-8`; harga per token berbeda.

## Bermigrasi ke Claude Opus 4.8

Claude Opus 4.8 dibangun untuk coding agentik yang kompleks dan pekerjaan enterprise. Berikut adalah pengaturan dasar untuk `claude-opus-4-8`. Sub-bagian berikut mencakup perubahan spesifik yang perlu dilakukan dari setiap model Opus sebelumnya.

* **Harga:** lihat [Harga Claude](/docs/id/about-claude/pricing).
* **Thinking:** [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) adalah mode thinking yang didukung dan nonaktif secara default: permintaan tanpa field `thinking` berjalan tanpa thinking. Extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) mengembalikan error 400.
* **Effort:** [Parameter effort](/docs/id/build-with-claude/effort) secara default bernilai `high` di semua permukaan. Untuk pekerjaan coding dan otonomi tinggi, atur `xhigh` secara eksplisit.
* **Parameter sampling:** `temperature`, `top_p`, dan `top_k` yang diatur ke nilai non-default mengembalikan error 400. Hilangkan parameter tersebut dan gunakan prompting untuk memandu perilaku model.
* **Prefill:** Melakukan prefill pada pesan assistant mengembalikan error 400. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs) atau `output_config.format` sebagai gantinya.
* **Jendela konteks dan output:** [Jendela konteks 1M token](/docs/id/build-with-claude/context-windows) penuh disajikan secara default tanpa header beta dan tanpa premi konteks panjang, dengan [maksimum 128k token output](/docs/id/about-claude/models/overview).

Claude Opus 4.8 juga mendukung [caching prompt](/docs/id/build-with-claude/prompt-caching), [pemrosesan batch](/docs/id/build-with-claude/batch-processing), [Files API](/docs/id/build-with-claude/files), [dukungan PDF](/docs/id/build-with-claude/pdf-support), [vision](/docs/id/build-with-claude/vision), rangkaian lengkap [alat](/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien, [pesan sistem di tengah percakapan](/docs/id/about-claude/models/whats-new-claude-4-8#mid-conversation-system-messages), dan [detail stop penolakan](/docs/id/about-claude/models/whats-new-claude-4-8#refusal-stop-details).

### Bermigrasi ke Claude Opus 4.8 dari Claude Opus 4.7

Claude Opus 4.8 dibangun di atas Claude Opus 4.7.

Claude Opus 4.8 seharusnya memiliki kinerja out-of-the-box yang kuat pada prompt dan eval Claude Opus 4.7 yang sudah ada. Tidak ada perubahan API yang bersifat breaking untuk kode yang sudah berjalan di Claude Opus 4.7. Model ini mendukung rangkaian fitur yang sama dengan Claude Opus 4.7, termasuk [jendela konteks 1M token](/docs/id/build-with-claude/context-windows), [maksimum 128k token output](/docs/id/about-claude/models/overview), [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), [caching prompt](/docs/id/build-with-claude/prompt-caching), [pemrosesan batch](/docs/id/build-with-claude/batch-processing), [Files API](/docs/id/build-with-claude/files), [dukungan PDF](/docs/id/build-with-claude/pdf-support), [vision](/docs/id/build-with-claude/vision), dan rangkaian lengkap [alat](/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien. Model ini juga menambahkan [pesan sistem di tengah percakapan](/docs/id/about-claude/models/whats-new-claude-4-8#mid-conversation-system-messages) dan mendokumentasikan secara publik [detail stop penolakan](/docs/id/about-claude/models/whats-new-claude-4-8#refusal-stop-details).

<Note>
  Jika kode Anda berada di Claude Opus 4.6 atau lebih lama, gunakan [Bermigrasi ke Claude Opus 4.8 dari Claude Opus 4.6](#migrating-from-claude-opus-46) atau [Bermigrasi ke Claude Opus 4.8 dari Claude Opus 4.5 atau lebih lama](#migrating-from-claude-opus-45) sebagai gantinya. Bagian-bagian tersebut mencakup perubahan yang bersifat breaking (parameter sampling ditolak, extended thinking manual ditolak, tokenizer baru) yang tidak tercakup oleh peningkatan dari Claude Opus 4.7 saja.
</Note>

#### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-7"  # Before
model = "claude-opus-4-8"  # After
```

#### Apa yang berubah

Ini bukan perubahan yang bersifat breaking. Kode yang berjalan di Claude Opus 4.7 tetap bekerja tanpa perubahan di Claude Opus 4.8. Item-item di bawah ini menjelaskan perbedaan perilaku yang perlu diperiksa setelah Anda mengganti ID model.

1. **Parameter sampling (tidak berubah):** Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default mengembalikan error 400 di Claude Opus 4.8, sama seperti di Claude Opus 4.7. Tipe permintaan SDK masih mendefinisikan field-field ini untuk kompatibilitas dengan model sebelumnya, sehingga kode yang mengaturnya lolos pemeriksaan tipe, tetapi API menolak permintaan tersebut di sisi server. Jika Anda menghapus parameter-parameter ini saat bermigrasi ke Opus 4.7, tidak diperlukan perubahan lebih lanjut.

2. **Default effort adalah `high`:** Default [parameter effort](/docs/id/build-with-claude/effort) di Claude Opus 4.8 adalah `high` di semua permukaan, termasuk Claude Code dan Messages API. Jika Anda sudah mengatur effort secara eksplisit, pengaturan Anda tidak berubah. Untuk pekerjaan coding dan otonomi tinggi, atur `xhigh` secara eksplisit. Evaluasi ulang pengaturan effort Anda terhadap anggaran latensi dan biaya Anda.

3. **Jendela konteks 1M adalah default:** Claude Opus 4.8 menyajikan [jendela konteks](/docs/id/build-with-claude/context-windows) 1M token penuh secara default tanpa header beta dan tanpa premi konteks panjang. Jika klien Anda mengirimkan header beta jendela konteks untuk kompatibilitas dengan model lama, Anda dapat menghapusnya di Claude Opus 4.8.

4. **Pesan sistem di tengah percakapan:** Claude Opus 4.8 menerima pesan `role: "system"` segera setelah giliran user dalam array `messages` (tunduk pada [aturan penempatan](/docs/id/build-with-claude/mid-conversation-system-messages#limitations)). Gunakan field `system` tingkat atas untuk instruksi yang berlaku sejak awal. Model sebelumnya, termasuk Claude Opus 4.7, menolak `role: "system"` dalam `messages` dengan error 400. Jika Anda memelihara jalur kode yang membangun ulang seluruh riwayat pesan untuk memperbarui instruksi, Anda dapat menyederhanakannya dan mempertahankan hit [cache prompt](/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya.

5. **Detail stop penolakan:** Objek `stop_details` pada respons penolakan (tersedia sejak Claude Opus 4.7) sekarang didokumentasikan secara publik. Ketika model menolak permintaan, model mengidentifikasi kategori penolakan, selain stop reason `refusal` yang sudah ada. Tidak diperlukan header beta, dan tidak ada opsi untuk menonaktifkannya. Lihat [Menangani stop reason](/docs/id/build-with-claude/handling-stop-reasons).

6. **Minimum caching prompt yang lebih rendah:** Panjang prompt minimum yang dapat di-cache di Claude Opus 4.8 adalah 1.024 token, lebih rendah daripada di Claude Opus 4.7. Prompt yang terlalu pendek untuk di-cache di Claude Opus 4.7 sekarang dapat membuat entri cache, tanpa perlu perubahan kode. Lihat [Caching prompt](/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

7. **Tingkat effort dikalibrasi ulang:** Alokasi token di balik setiap tingkat effort berubah di Claude Opus 4.8 dibandingkan dengan Claude Opus 4.7: `medium` memungkinkan thinking yang sedikit lebih banyak, `high` sedikit lebih sedikit, dan `xhigh` jauh lebih banyak. Jika Anda menyetel tingkat effort berdasarkan biaya atau latensi Claude Opus 4.7, lakukan baseline ulang pada tingkat yang sama sebelum menyesuaikannya. Lihat [Effort](/docs/id/build-with-claude/effort).

#### Daftar periksa migrasi

* Perbarui nama model dari `claude-opus-4-7` ke `claude-opus-4-8` (atau perbarui alias).
* Jika Anda menghapus parameter sampling selama migrasi Opus 4.7, tidak ada tindakan yang diperlukan. Jika Anda menambahkannya kembali dengan jalur percobaan ulang 400, hapus jalur percobaan ulang tersebut.
* Evaluasi ulang pengaturan `effort` Anda. Default-nya adalah `high` di semua permukaan; untuk pekerjaan coding dan otonomi tinggi, atur `xhigh` secara eksplisit.
* Hapus header beta jendela konteks apa pun. Jendela konteks 1M adalah default di Claude API, Amazon Bedrock, Google Cloud, dan Microsoft Foundry.
* Jika Anda membangun ulang riwayat percakapan untuk memperbarui instruksi, pertimbangkan untuk beralih ke pesan sistem di tengah percakapan untuk mempertahankan hit cache prompt.
* Verifikasi bahwa penanganan stop-reason Anda membaca `stop_details` pada penolakan (tersedia sejak Claude Opus 4.7; sekarang didokumentasikan secara publik).
* Lakukan baseline ulang biaya dan latensi pada tingkat effort yang Anda pilih.

### Migrasi ke Claude Opus 4.8 dari Claude Opus 4.6

Claude Opus 4.8 seharusnya memiliki performa out-of-the-box yang kuat pada prompt dan eval Claude Opus 4.6 yang sudah ada dengan harga yang sama, tetapi ada beberapa perubahan perilaku dan API yang perlu diketahui saat Anda bermigrasi. Perubahan ini mulai berlaku di Claude Opus 4.7, dan tidak ada perubahan API yang merusak tambahan antara Claude Opus 4.7 dan Claude Opus 4.8. Model ini mendukung rangkaian fitur yang sama dengan Claude Opus 4.6, termasuk:

* [Jendela konteks 1M token](/docs/id/build-with-claude/context-windows) dengan harga API standar tanpa premi konteks panjang
* [128k max output tokens](/docs/id/about-claude/models/overview)
* [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking)
* [Caching prompt](/docs/id/build-with-claude/prompt-caching)
* [Pemrosesan batch](/docs/id/build-with-claude/batch-processing)
* [Files API](/docs/id/build-with-claude/files)
* [Dukungan PDF](/docs/id/build-with-claude/pdf-support)
* [Vision](/docs/id/build-with-claude/vision)
* Rangkaian lengkap [alat](/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien ([bash](/docs/id/agents-and-tools/tool-use/bash-tool), [eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool), [computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool), [text editor](/docs/id/agents-and-tools/tool-use/text-editor-tool), [pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool), [web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool), [konektor MCP](/docs/id/agents-and-tools/mcp-connector), [memory](/docs/id/agents-and-tools/tool-use/memory-tool))

#### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-6"  # Before
model = "claude-opus-4-8"  # After
```

#### Perubahan yang merusak

1. **Extended thinking dihapus:** `thinking: {type: "enabled", budget_tokens: N}` tidak lagi didukung pada Claude Opus 4.7 atau model yang lebih baru dan mengembalikan error 400. Beralihlah ke [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) dan gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran. Adaptive thinking **nonaktif secara default** pada Claude Opus 4.7: permintaan tanpa field `thinking` berjalan tanpa pemikiran, sesuai dengan perilaku Opus 4.6. Atur `thinking: {type: "adaptive"}` secara eksplisit untuk mengaktifkannya.

   Sebelum (Claude Opus 4.6):

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -H "content-type: application/json" \
       -d '{
         "model": "claude-opus-4-6",
         "max_tokens": 16000,
         "thinking": {
           "type": "enabled",
           "budget_tokens": 10000
         },
         "messages": [
           {
             "role": "user",
             "content": "..."
           }
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-opus-4-6
     max_tokens: 16000
     thinking:
       type: enabled
       budget_tokens: 10000
     messages:
       - role: user
         content: "..."
     YAML
     ```

     ```python Python
     client.messages.create(
         model="claude-opus-4-6",
         max_tokens=16000,
         thinking={"type": "enabled", "budget_tokens": 10000},
         messages=[{"role": "user", "content": "..."}],
     )
     ```

     ```typescript TypeScript
     await client.messages.create({
       model: "claude-opus-4-6",
       max_tokens: 16000,
       thinking: { type: "enabled", budget_tokens: 10000 },
       messages: [{ role: "user", content: "..." }]
     });
     ```

     ```csharp C#
     using Anthropic;
     using Anthropic.Models.Messages;

     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = "claude-opus-4-6",
         MaxTokens = 16000,
         Thinking = new ThinkingConfigEnabled(budgetTokens: 10000),
         Messages = [new() { Role = Role.User, Content = "..." }]
     };

     var response = await client.Messages.Create(parameters);
     Console.WriteLine(response);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     "claude-opus-4-6",
     	MaxTokens: 16000,
     	Thinking:  anthropic.ThinkingConfigParamOfEnabled(10000),
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
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
         .model("claude-opus-4-6")
         .maxTokens(16000L)
         .enabledThinking(10000L)
         .addUserMessage("...")
         .build();

     Message response = client.messages().create(params);
     IO.println(response);
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => '...']],
         model: 'claude-opus-4-6',
         thinking: ['type' => 'enabled', 'budget_tokens' => 10000],
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: "claude-opus-4-6",
       max_tokens: 16000,
       thinking: {
         type: "enabled",
         budget_tokens: 10000
       },
       messages: [
         { role: "user", content: "..." }
       ]
     )
     ```
   </CodeGroup>

   Sesudah (Claude Opus 4.8):

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
           "type": "adaptive"
         },
         "output_config": {
           "effort": "high"
         },
         "messages": [
           {
             "role": "user",
             "content": "..."
           }
         ]
       }'
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-opus-4-8
     max_tokens: 16000
     thinking:
       type: adaptive
     output_config:
       effort: high
     messages:
       - role: user
         content: "..."
     YAML
     ```

     ```python Python
     client.messages.create(
         model="claude-opus-4-8",
         max_tokens=16000,
         thinking={"type": "adaptive"},
         output_config={"effort": "high"},  # or "max", "xhigh", "medium", "low"
         messages=[{"role": "user", "content": "..."}],
     )
     ```

     ```typescript TypeScript
     await client.messages.create({
       model: "claude-opus-4-8",
       max_tokens: 16000,
       thinking: { type: "adaptive" },
       output_config: { effort: "high" }, // or "max", "xhigh", "medium", "low"
       messages: [{ role: "user", content: "..." }]
     });
     ```

     ```csharp C#
     using Anthropic;
     using Anthropic.Models.Messages;

     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = "claude-opus-4-8",
         MaxTokens = 16000,
         Thinking = new ThinkingConfigAdaptive(),
         OutputConfig = new OutputConfig { Effort = Effort.High }, // or Max, Xhigh, Medium, Low
         Messages = [new() { Role = Role.User, Content = "..." }]
     };

     var response = await client.Messages.Create(parameters);
     Console.WriteLine(response);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     "claude-opus-4-8",
     	MaxTokens: 16000,
     	Thinking: anthropic.ThinkingConfigParamUnion{
     		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
     	},
     	OutputConfig: anthropic.OutputConfigParam{
     		Effort: anthropic.OutputConfigEffortHigh, // or Max, Xhigh, Medium, Low
     	},
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("...")),
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
         .model("claude-opus-4-8")
         .maxTokens(16000L)
         .thinking(ThinkingConfigAdaptive.builder().build())
         .outputConfig(OutputConfig.builder()
             .effort(OutputConfig.Effort.HIGH) // or MAX, XHIGH, MEDIUM, LOW
             .build())
         .addUserMessage("...")
         .build();

     Message response = client.messages().create(params);
     IO.println(response);
     ```

     ```php PHP
     $client = new Client();

     $message = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => '...']],
         model: 'claude-opus-4-8',
         thinking: ['type' => 'adaptive'],
         outputConfig: ['effort' => 'high'], // or 'max', 'xhigh', 'medium', 'low'
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: "claude-opus-4-8",
       max_tokens: 16000,
       thinking: {
         type: "adaptive"
       },
       output_config: {
         effort: "high" # or "max", "xhigh", "medium", "low"
       },
       messages: [
         { role: "user", content: "..." }
       ]
     )
     ```
   </CodeGroup>

   Adaptive thinking dapat diarahkan melalui prompting. Untuk panduan penyetelan ketika model berpikir berlebihan atau kurang, lihat [Mengkalibrasi effort dan kedalaman pemikiran](/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-4-8#calibrating-effort-and-thinking-depth).

2. **Parameter sampling dihapus:** Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default apa pun pada Claude Opus 4.7 mengembalikan error 400. Jalur migrasi teraman adalah menghilangkan parameter ini sepenuhnya dari payload permintaan. Prompting adalah cara yang direkomendasikan untuk memandu perilaku model pada Claude Opus 4.7. Jika Anda menggunakan `temperature = 0` untuk determinisme, perhatikan bahwa hal itu tidak pernah menjamin output yang identik pada model sebelumnya.

3. **Konten pemikiran dihilangkan secara default:** Blok pemikiran masih muncul dalam stream respons pada Claude Opus 4.7, tetapi field `thinking`-nya kosong kecuali Anda secara eksplisit memilih untuk mengaktifkannya. Ini adalah perubahan diam-diam dari Claude Opus 4.6, di mana default-nya adalah mengembalikan teks pemikiran yang diringkas. Untuk memulihkan konten pemikiran yang diringkas pada Claude Opus 4.7, atur `thinking.display` ke `"summarized"`:

   <CodeGroup exclude="shell">
     ```python Python
     thinking = {
         "type": "adaptive",
         "display": "summarized",
     }
     ```

     ```typescript TypeScript
     const thinking = {
       type: "adaptive",
       display: "summarized"
     };
     ```

     ```csharp C#
     var thinking = new ThinkingConfigAdaptive { Display = Display.Summarized };
     ```

     ```go Go
     thinking := anthropic.ThinkingConfigParamUnion{
     	OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{
     		Display: anthropic.ThinkingConfigAdaptiveDisplaySummarized,
     	},
     }
     ```

     ```java Java
     ThinkingConfigAdaptive thinking = ThinkingConfigAdaptive.builder()
         .display(ThinkingConfigAdaptive.Display.SUMMARIZED)
         .build();
     ```

     ```php PHP
     $thinking = ['type' => 'adaptive', 'display' => 'summarized'];
     ```

     ```ruby Ruby
     thinking = {
       type: "adaptive",
       display: "summarized"
     }
     ```
   </CodeGroup>

   Default-nya adalah `"omitted"` pada Claude Opus 4.7. Jika produk Anda melakukan streaming penalaran kepada pengguna, default baru ini muncul sebagai jeda panjang sebelum output dimulai; atur `display: "summarized"` untuk memulihkan progres yang terlihat selama pemikiran. Lihat [Pemikiran diperpanjang](/docs/id/build-with-claude/extended-thinking#controlling-thinking-display) untuk detailnya.

4. **Penghitungan token yang diperbarui:** Claude Opus 4.7 menggunakan tokenizer baru, yang berkontribusi pada peningkatan performanya pada berbagai tugas. Tokenizer baru ini dapat menggunakan sekitar 1x hingga 1,35x lebih banyak token saat memproses teks dibandingkan dengan model sebelumnya (hingga \~35% lebih banyak, bervariasi menurut konten).

   [`/v1/messages/count_tokens`](/docs/id/build-with-claude/token-counting) mengembalikan jumlah token yang berbeda untuk Claude Opus 4.7 dibandingkan dengan Claude Opus 4.6. Efisiensi token dapat bervariasi menurut bentuk beban kerja.

   Intervensi prompting, `task_budget`, dan `effort` dapat membantu mengontrol biaya dan memastikan penggunaan token yang sesuai. Kontrol ini mungkin mengorbankan kecerdasan model. Perbarui parameter `max_tokens` Anda untuk memberikan ruang tambahan, termasuk pemicu kompaksi. Claude Opus 4.7 menyediakan jendela konteks 1M dengan harga API standar tanpa premi konteks panjang.

5. **Penghapusan prefill (dibawa dari Opus 4.6):** Prefilling pesan assistant mengembalikan error 400 pada Claude Opus 4.7. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

#### Memilih tingkat effort

[Parameter effort](/docs/id/build-with-claude/effort) memungkinkan Anda menyetel kecerdasan Claude versus pengeluaran token, menukar kemampuan dengan kecepatan yang lebih tinggi dan biaya yang lebih rendah. Mulailah dengan tingkat effort `xhigh` untuk kasus penggunaan coding dan agentik, dan gunakan minimum effort `high` untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan. Bereksperimenlah dengan tingkat effort lainnya untuk lebih menyetel penggunaan token dan kecerdasan:

* **`max`:** Effort max dapat memberikan peningkatan performa dalam beberapa kasus penggunaan, tetapi mungkin menunjukkan hasil yang semakin berkurang dari peningkatan penggunaan token. Pengaturan ini juga terkadang rentan terhadap pemikiran berlebihan. Uji effort max untuk tugas yang menuntut kecerdasan.
* **`xhigh`:** Effort extra high adalah pengaturan terbaik untuk sebagian besar kasus penggunaan coding dan agentik.
* **`high`:** Pengaturan ini menyeimbangkan penggunaan token dan kecerdasan. Untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan, gunakan minimum effort `high`.
* **`medium`:** Baik untuk kasus penggunaan yang sensitif terhadap biaya yang perlu mengurangi penggunaan token sambil mengorbankan kecerdasan.
* **`low`:** Cadangkan untuk tugas pendek yang terbatas dan beban kerja yang sensitif terhadap latensi yang tidak sensitif terhadap kecerdasan.

Effort lebih penting untuk model ini dibandingkan Opus sebelumnya. Bereksperimenlah dengannya secara aktif saat Anda melakukan upgrade.

#### Perubahan perilaku

Claude Opus 4.7 memiliki beberapa perbedaan perilaku dari Claude Opus 4.6 yang bukan merupakan perubahan API yang merusak tetapi mungkin memerlukan pembaruan prompt atau penghapusan scaffolding.

1. **Panjang respons bervariasi menurut kasus penggunaan:** Claude Opus 4.7 mengkalibrasi panjang respons berdasarkan seberapa kompleks ia menilai tugas tersebut, alih-alih menggunakan verbositas tetap secara default. Ini biasanya berarti jawaban yang lebih pendek pada pencarian sederhana dan jawaban yang jauh lebih panjang pada analisis terbuka.

   Jika produk Anda bergantung pada gaya atau verbositas output tertentu, Anda mungkin perlu menyetel prompt Anda. Misalnya, untuk mengurangi verbositas, tambahkan: "Provide concise, focused responses. Skip non-essential context, and keep examples minimal." Jika Anda melihat jenis penjelasan berlebihan tertentu, tambahkan instruksi yang ditargetkan dalam prompt Anda untuk mencegahnya.

   Contoh positif yang menunjukkan bagaimana Claude dapat berkomunikasi dengan tingkat keringkasan yang sesuai cenderung lebih efektif daripada contoh negatif atau instruksi yang memberi tahu model apa yang tidak boleh dilakukan.

2. **Mengikuti instruksi secara lebih literal:** Claude Opus 4.7 menafsirkan prompt secara lebih literal dan eksplisit dibandingkan Claude Opus 4.6, terutama pada tingkat effort yang lebih rendah. Model ini tidak secara diam-diam menggeneralisasi instruksi dari satu item ke item lain, dan tidak menyimpulkan permintaan yang tidak Anda buat. Keuntungan dari literalisme ini adalah presisi dan lebih sedikit kekacauan. Model ini umumnya berkinerja lebih baik untuk kasus penggunaan API dengan prompt yang disetel dengan cermat, ekstraksi terstruktur, dan pipeline di mana Anda menginginkan perilaku yang dapat diprediksi. Peninjauan prompt dan harness mungkin sangat membantu untuk migrasi ke Claude Opus 4.8.

3. **Nada yang lebih langsung:** Seperti halnya model baru lainnya, gaya prosa pada penulisan bentuk panjang mungkin berubah. Claude Opus 4.7 lebih langsung dan berpendirian, dengan lebih sedikit frasa yang berorientasi validasi dan lebih sedikit emoji dibandingkan gaya Claude Opus 4.6 yang lebih hangat. Jika produk Anda bergantung pada suara tertentu, evaluasi ulang prompt gaya terhadap baseline baru.

4. **Pembaruan progres bawaan dalam jejak agentik:** Claude Opus 4.7 memberikan pembaruan yang lebih teratur dan berkualitas lebih tinggi kepada pengguna sepanjang jejak agentik yang panjang. Jika Anda telah menambahkan scaffolding untuk memaksa pesan status sementara ("After every 3 tool calls, summarize progress"), coba hapus. Jika Anda menemukan bahwa panjang atau isi pembaruan yang ditampilkan kepada pengguna dari Claude Opus 4.7 tidak terkalibrasi dengan baik untuk kasus penggunaan Anda, jelaskan secara eksplisit seperti apa pembaruan ini seharusnya dalam prompt dan berikan contoh.

5. **Lebih sedikit subagen yang dibuat secara default:** Claude Opus 4.7 cenderung membuat lebih sedikit subagen secara default. Namun, perilaku ini dapat diarahkan melalui prompting; berikan Claude Opus 4.7 panduan eksplisit tentang kapan subagen diinginkan.

6. **Kalibrasi effort yang lebih ketat:** Berubah secara signifikan dari Claude Opus 4.6, Claude Opus 4.7 menghormati [tingkat effort](/docs/id/build-with-claude/effort) secara ketat, terutama pada tingkat rendah. Pada `low` dan `medium`, model membatasi pekerjaannya pada apa yang diminta alih-alih melakukan lebih dari yang diminta.

   Ini baik untuk latensi dan biaya, tetapi pada tugas yang cukup kompleks yang berjalan pada effort `low` ada risiko pemikiran yang kurang. Jika Anda mengamati penalaran yang dangkal pada masalah kompleks, naikkan effort ke `high` atau `xhigh` alih-alih mengatasinya dengan prompting.

   Jika Anda perlu mempertahankan effort pada `low` untuk latensi, tambahkan panduan yang ditargetkan: "This task involves multistep reasoning. Think carefully through the problem before responding." Lihat [Tingkat effort yang direkomendasikan untuk Claude Opus 4.7](/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-opus-4-7).

7. **Lebih sedikit panggilan alat secara default:** Claude Opus 4.7 memiliki kecenderungan untuk menggunakan alat lebih jarang dibandingkan Claude Opus 4.6 dan lebih banyak menggunakan penalaran. Ini menghasilkan hasil yang lebih baik dalam sebagian besar kasus.

   Untuk meningkatkan penggunaan alat, naikkan pengaturan effort. Pengaturan effort `high` atau `xhigh` menunjukkan penggunaan alat yang jauh lebih banyak dalam pencarian agentik dan coding. Anda juga dapat menyesuaikan prompt Anda untuk secara eksplisit menginstruksikan model tentang kapan dan bagaimana menggunakan alatnya dengan benar.

8. **Perlindungan keamanan siber real-time:** Baru ditambahkan di Claude Opus 4.7, permintaan yang melibatkan topik terlarang atau berisiko tinggi dapat menyebabkan penolakan. Untuk pekerjaan keamanan yang sah seperti penetration testing, riset kerentanan, atau red-teaming, ajukan permohonan ke [Cyber Verification Program](https://claude.com/form/cyber-use-case) untuk meminta pengurangan pembatasan. Lihat [Safeguards, warnings, and appeals](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals) untuk latar belakangnya.

9. **Dukungan gambar resolusi tinggi:** Claude Opus 4.7 adalah model Claude pertama dengan dukungan gambar resolusi tinggi. Resolusi gambar maksimum adalah 2.576 piksel pada sisi terpanjang, naik dari 1.568 piksel pada model sebelumnya. Ini membuka peningkatan pada beban kerja yang berat pada vision dan sangat berharga untuk computer use, pemahaman tangkapan layar, dan analisis dokumen.

   Dukungan resolusi tinggi bersifat otomatis dan tidak memerlukan header beta atau opt-in sisi klien. Dua hal yang perlu direncanakan:

   * Gambar resolusi penuh dapat menggunakan hingga sekitar 3x lebih banyak token gambar dibandingkan model sebelumnya (hingga 4.784 token per gambar, dibandingkan dengan batas sebelumnya sekitar 1.600 token per gambar). Anggarkan ulang `max_tokens` dan ekspektasi biaya untuk beban kerja yang berat pada gambar, atau lakukan downsample sebelum mengirim jika Anda tidak memerlukan fidelitas tambahan.
   * Koordinat pointing dan bounding-box yang dikembalikan oleh model adalah 1:1 dengan piksel gambar aktual pada Claude Opus 4.7, sehingga tidak diperlukan konversi faktor skala.

   Lihat [Dukungan gambar resolusi tinggi pada Claude Opus 4.7](/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) untuk detailnya.

#### Perubahan yang direkomendasikan

Perubahan ini tidak wajib tetapi akan meningkatkan pengalaman Anda:

1. **Evaluasi ulang `max_tokens`:** Karena teks yang sama menghasilkan jumlah token yang lebih tinggi pada Claude Opus 4.7 dan model yang lebih baru, perbarui parameter `max_tokens` Anda untuk memberikan ruang tambahan, termasuk pemicu kompaksi. Intervensi prompting, [`task_budget`](/docs/id/build-with-claude/task-budgets), dan [`effort`](/docs/id/build-with-claude/effort) dapat membantu mengontrol biaya dan memastikan penggunaan token yang sesuai.

2. **Audit ekspektasi jumlah token:** Setiap jalur kode yang memperkirakan token di sisi klien atau mengasumsikan rasio token-ke-karakter yang tetap harus diuji ulang terhadap Claude Opus 4.8. Gunakan [endpoint penghitungan token](/docs/id/build-with-claude/token-counting) untuk memverifikasi.

3. **Adopsi [task budgets](/docs/id/build-with-claude/task-budgets) (beta):** Claude Opus 4.7 memperkenalkan task budgets. Anggaran ini memungkinkan Anda memberi tahu Claude berapa banyak token yang dimilikinya untuk loop agentik penuh, termasuk pemikiran, panggilan alat, hasil alat, dan output akhir. Model melihat hitungan mundur yang berjalan dan menggunakannya untuk memprioritaskan pekerjaan dan menyelesaikan tugas dengan baik saat anggaran terpakai. Untuk menggunakannya, atur header beta `task-budgets-2026-03-13` dan tambahkan yang berikut ke konfigurasi output Anda:

   <CodeGroup exclude="shell">
     ```python Python
     output_config = {
         "effort": "high",
         "task_budget": {"type": "tokens", "total": 128000},
     }
     ```

     ```typescript TypeScript
     const output_config = {
       effort: "high",
       task_budget: { type: "tokens", total: 128000 }
     };
     ```

     ```csharp C#
     var outputConfig = new BetaOutputConfig
     {
         Effort = Effort.High,
         TaskBudget = new BetaTokenTaskBudget
         {
             Total = 128000,
         },
     };
     ```

     ```go Go
     outputConfig := anthropic.BetaOutputConfigParam{
     	Effort: anthropic.BetaOutputConfigEffortHigh,
     	TaskBudget: anthropic.BetaTokenTaskBudgetParam{
     		Total: 128000,
     	},
     }
     ```

     ```java Java
     BetaOutputConfig outputConfig = BetaOutputConfig.builder()
         .effort(BetaOutputConfig.Effort.HIGH)
         .taskBudget(BetaTokenTaskBudget.builder()
             .total(128000L)
             .build())
         .build();
     ```

     ```php PHP
     $outputConfig = [
         'effort' => 'high',
         'taskBudget' => [
             'type' => 'tokens',
             'total' => 128000,
         ],
     ];
     ```

     ```ruby Ruby
     output_config = {
       effort: :high,
       task_budget: {
         type: :tokens,
         total: 128_000
       }
     }
     ```
   </CodeGroup>

   Anda mungkin perlu bereksperimen dengan task budget yang berbeda untuk kasus penggunaan Anda. Jika model diberi task budget yang terlalu ketat, model mungkin menyelesaikan tugas dengan kurang menyeluruh, merujuk pada anggarannya sebagai kendala.

   Untuk tugas agentik terbuka di mana kualitas lebih penting daripada kecepatan, jangan atur task budget. Cadangkan task budget untuk beban kerja di mana Anda memerlukan model untuk membatasi pekerjaannya pada jatah token. Nilai minimum untuk task budget adalah 20k token.

   Task budget bukanlah batas keras; ini adalah saran yang disadari oleh model. Ini berbeda dari `max_tokens`:

   * **`task_budget`:** batas penasihat di seluruh loop agentik penuh. Model melihatnya dan menggunakannya untuk mengatur kecepatannya sendiri.
   * **`max_tokens`:** batas keras per permintaan pada token yang dihasilkan. Ini tidak diteruskan ke model, sehingga model tidak menyadarinya.

   Gunakan `task_budget` ketika Anda ingin model mengatur dirinya sendiri, dan `max_tokens` sebagai batas keras untuk membatasi penggunaan.

4. **Atur `max_tokens` yang besar pada effort `max` atau `xhigh`:** Jika Anda menjalankan Claude Opus 4.7 atau model yang lebih baru pada effort `max` atau `xhigh`, atur anggaran token output maksimum yang besar sehingga model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan panggilan alatnya. Mulai dari 64k token dan setel dari sana.

5. **Lakukan downsample gambar jika resolusi tinggi tidak diperlukan:** Claude Opus 4.7 mendukung gambar hingga 2576px / 3,75MP. Gambar resolusi tinggi menggunakan lebih banyak token. Jika fidelitas gambar tambahan tidak diperlukan, lakukan downsample gambar sebelum mengirim ke Claude untuk menghindari peningkatan penggunaan token. Lihat [Gambar dan vision](/docs/id/build-with-claude/vision).

#### Daftar periksa migrasi

* Perbarui nama model dari `claude-opus-4-6` ke `claude-opus-4-8` (atau perbarui alias).
* Hapus `temperature`, `top_p`, dan `top_k` dari payload permintaan.
* Ganti `thinking: {type: "enabled", budget_tokens: N}` dengan `thinking: {type: "adaptive"}` ditambah [parameter effort](/docs/id/build-with-claude/effort).
* Hapus semua prefill pesan assistant.
* Jika UI Anda menampilkan konten pemikiran, pilih secara eksplisit untuk mengaktifkan ringkasan pemikiran.
* Lakukan benchmark ulang biaya dan latensi end-to-end dengan tokenisasi yang diperbarui.
* Setel ulang `max_tokens` untuk memperhitungkan tokenisasi yang diperbarui.
* Uji ulang semua estimasi jumlah token sisi klien.
* Jika aplikasi Anda mengirim gambar, anggarkan ulang untuk [dukungan gambar resolusi tinggi](/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) (hingga sekitar 3x lebih banyak token gambar per gambar resolusi penuh). Lakukan downsample sebelum mengirim jika Anda tidak memerlukan fidelitas tambahan.
* Jika Anda menggunakan koordinat pointing atau bounding-box dari model, hapus semua konversi faktor skala; koordinat adalah 1:1 dengan piksel gambar aktual pada Claude Opus 4.7.
* Tinjau prompt untuk perubahan perilaku di atas (panjang respons, literalisme, nada, pembaruan progres, subagen, kalibrasi effort, pemicu alat, perlindungan siber, penanganan gambar resolusi tinggi).
* Tetapkan ulang baseline panjang respons dengan prompt kontrol panjang yang ada dihapus, lalu setel secara eksplisit.
* Jika menggunakan effort `xhigh` atau `max`, naikkan `max_tokens` ke setidaknya 64k sebagai titik awal.
* Pertimbangkan untuk mengadopsi task budgets (beta) untuk alur kerja agentik.
* Jika produk Anda melakukan pekerjaan keamanan yang sah, ajukan permohonan ke [Cyber Verification Program](https://claude.com/form/cyber-use-case) untuk akses ke pembatasan yang lebih rendah pada konten siber.

### Migrasi ke Claude Opus 4.8 dari Claude Opus 4.5 atau sebelumnya

Jika Anda bermigrasi dari Claude Opus 4.5, Opus 4.1 (deprecated), atau model sebelumnya langsung ke Claude Opus 4.8, terapkan **semua perubahan di [Migrasi ke Claude Opus 4.8 dari Claude Opus 4.6](#migrating-from-claude-opus-46)** ditambah perubahan kumulatif di bagian ini yang mulai berlaku antara Opus 4.5 dan Opus 4.7. Jika Anda bermigrasi dari Opus 4.6, Anda hanya memerlukan [bagian dari Claude Opus 4.6](#migrating-from-claude-opus-46).

#### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-5"  # Before
model = "claude-opus-4-8"  # After
```

#### Perubahan yang merusak

1. **Penghapusan prefill** dibahas di [perubahan yang merusak untuk migrasi dari Claude Opus 4.6](#breaking-changes).

2. **Quoting parameter alat:** Claude Opus 4.6 dan model yang lebih baru mungkin menghasilkan escaping string JSON yang sedikit berbeda dalam argumen panggilan alat (misalnya, penanganan yang berbeda untuk escape Unicode atau escaping garis miring). Jika Anda mem-parsing `input` panggilan alat sebagai string mentah alih-alih menggunakan parser JSON, verifikasi logika parsing Anda. Parser JSON standar (seperti `json.loads()` atau `JSON.parse()`) menangani perbedaan ini secara otomatis.

#### Perubahan yang direkomendasikan

Perubahan ini meningkatkan pengalaman Anda pada Claude Opus 4.7 dan model yang lebih baru. Item yang ditandai **(wajib pada Opus 4.7)** adalah rekomendasi opsional ketika Opus 4.6 diluncurkan tetapi sekarang wajib; sisanya tetap direkomendasikan.

1. **Migrasi ke adaptive thinking (wajib pada Opus 4.7):** `thinking: {type: "enabled", budget_tokens: N}` mengembalikan error 400 pada Claude Opus 4.7. Beralihlah ke `thinking: {type: "adaptive"}` dan gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran. Lihat [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking).

   <CodeGroup>
     ```bash cURL
     curl -sS https://api.anthropic.com/v1/messages \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d '{
         "model": "claude-opus-4-8",
         "max_tokens": 16000,
         "thinking": {"type": "adaptive"},
         "output_config": {"effort": "high"},
         "messages": [{"role": "user", "content": "Your prompt here"}]
       }'
     ```

     ```python Before
     response = client.beta.messages.create(
         model="claude-opus-4-5",
         max_tokens=16000,
         thinking={"type": "enabled", "budget_tokens": 32000},
         betas=["interleaved-thinking-2025-05-14"],
         messages=[{"role": "user", "content": "Your prompt here"}],
     )
     ```

     ```python After
     response = client.messages.create(
         model="claude-opus-4-8",
         max_tokens=16000,
         thinking={"type": "adaptive"},
         output_config={"effort": "high"},
         messages=[{"role": "user", "content": "Your prompt here"}],
     )
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-opus-4-8
     max_tokens: 16000
     thinking:
       type: adaptive
     output_config:
       effort: high
     messages:
       - role: user
         content: Your prompt here
     YAML
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const response = await client.messages.create({
       model: "claude-opus-4-8",
       max_tokens: 16000,
       thinking: { type: "adaptive" },
       output_config: { effort: "high" },
       messages: [{ role: "user", content: "Your prompt here" }]
     });
     ```

     ```csharp C#
     using Anthropic;
     using Anthropic.Models.Messages;

     AnthropicClient client = new();

     var parameters = new MessageCreateParams
     {
         Model = Model.ClaudeOpus4_8,
         MaxTokens = 16000,
         Thinking = new ThinkingConfigAdaptive(),
         OutputConfig = new OutputConfig { Effort = Effort.High },
         Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
     };

     var response = await client.Messages.Create(parameters);
     Console.WriteLine(response);
     ```

     ```go Go
     client := anthropic.NewClient()

     response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
     	Model:     anthropic.ModelClaudeOpus4_8,
     	MaxTokens: 16000,
     	Thinking: anthropic.ThinkingConfigParamUnion{
     		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
     	},
     	OutputConfig: anthropic.OutputConfigParam{
     		Effort: anthropic.OutputConfigEffortHigh,
     	},
     	Messages: []anthropic.MessageParam{
     		anthropic.NewUserMessage(anthropic.NewTextBlock("Your prompt here")),
     	},
     })
     if err != nil {
     	log.Fatal(err)
     }
     fmt.Println(response)
     ```

     ```java Java
     import com.anthropic.models.messages.OutputConfig;
     import com.anthropic.models.messages.ThinkingConfigAdaptive;
     // ...
     public class AdaptiveThinkingExample {
         public static void main(String[] args) {
             AnthropicClient client = AnthropicOkHttpClient.fromEnv();

             MessageCreateParams params = MessageCreateParams.builder()
                 .model(Model.CLAUDE_OPUS_4_8)
                 .maxTokens(16000L)
                 .thinking(ThinkingConfigAdaptive.builder().build())
                 .outputConfig(OutputConfig.builder()
                     .effort(OutputConfig.Effort.HIGH)
                     .build())
                 .addUserMessage("Your prompt here")
                 .build();

             Message response = client.messages().create(params);
             System.out.println(response);
         }
     }
     ```

     ```php PHP
     $client = new Client();

     $response = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => 'Your prompt here']],
         model: 'claude-opus-4-8',
         thinking: ['type' => 'adaptive'],
         outputConfig: ['effort' => 'high'],
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     response = client.messages.create(
       model: "claude-opus-4-8",
       max_tokens: 16000,
       thinking: { type: "adaptive" },
       output_config: { effort: "high" },
       messages: [{ role: "user", content: "Your prompt here" }]
     )
     ```
   </CodeGroup>

   Perhatikan bahwa migrasi ini juga berpindah dari `client.beta.messages.create` ke `client.messages.create`. Adaptive thinking dan effort adalah fitur GA dan tidak memerlukan namespace SDK beta atau header beta apa pun.

2. **Hapus header beta effort:** Parameter effort sekarang GA. Hapus `betas=["effort-2025-11-24"]` dari permintaan Anda.

3. **Hapus header beta fine-grained tool streaming:** Fine-grained tool streaming sekarang GA. Hapus `betas=["fine-grained-tool-streaming-2025-05-14"]` dari permintaan Anda.

4. **Hapus header beta interleaved thinking:** Adaptive thinking secara otomatis mengaktifkan interleaved thinking pada Claude Opus 4.7, Opus 4.6, dan Sonnet 4.6. Hapus `betas=["interleaved-thinking-2025-05-14"]` dari permintaan Anda. Header ini masih berfungsi pada Sonnet 4.6 dengan extended thinking manual, tetapi mode manual sudah deprecated.

5. **Migrasi ke output\_config.format:** Jika menggunakan structured outputs, perbarui `output_format={...}` menjadi `output_config={"format": {...}}`. Parameter lama tetap berfungsi tetapi sudah deprecated dan akan dihapus dalam rilis model mendatang.

#### Migrasi dari Claude 4.1 atau sebelumnya

Jika Anda bermigrasi dari Opus 4.1 (deprecated) atau model sebelumnya langsung ke Claude Opus 4.8, terapkan perubahan [Migrasi ke Claude Opus 4.8 dari Claude Opus 4.6](#migrating-from-claude-opus-46) dan perubahan kumulatif sebelumnya di bagian ini, ditambah perubahan tambahan di sub-bagian ini.

```python
# Dari Opus 4.1
model = "claude-opus-4-1-20250805"  # Before
model = "claude-opus-4-8"  # After

# Dari Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Before
model = "claude-opus-4-8"  # After
```

##### Perubahan yang merusak tambahan

1. **Hapus parameter sampling**

   <Warning>
     Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Mulai dari Claude Opus 4.7, mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default apa pun mengembalikan error 400. Jalur migrasi teraman adalah menghilangkan parameter ini sepenuhnya dari permintaan, dan menggunakan prompting untuk memandu perilaku model. Jika Anda menggunakan `temperature = 0` untuk determinisme, perhatikan bahwa hal itu tidak pernah menjamin output yang identik.

   <CodeGroup exclude="shell">
     ```python Python
     # Sebelum - Ini akan menghasilkan error pada model Claude 4+
     response = client.messages.create(
         model="claude-3-7-sonnet-20250219",
         temperature=0.7,
         top_p=0.9,  # Non-default sampling params return 400 on Opus 4.7
         # ...
     )

     # Sesudah
     response = client.messages.create(
         model="claude-opus-4-8",
         # ...
     )
     ```

     ```typescript TypeScript
     // Sebelum - Ini akan menghasilkan error pada model Claude 4+
     await client.messages.create({
       model: "claude-3-7-sonnet-20250219",
       temperature: 0.7,
       top_p: 0.9 // Non-default sampling params return 400 on Opus 4.7
       // ...
     });

     // Sesudah
     await client.messages.create({
       model: "claude-opus-4-8"
       // ...
     });
     ```

     ```csharp C#
     // Sebelum - Ini akan menghasilkan error pada model Claude 4+
     await client.Messages.Create(new MessageCreateParams
     {
         Model = "claude-3-7-sonnet-20250219",
         Temperature = 0.7,
         TopP = 0.9, // Non-default sampling params return 400 on Opus 4.7
         // ...
     });

     // Sesudah
     await client.Messages.Create(new MessageCreateParams
     {
         Model = "claude-opus-4-8",
         // ...
     });
     ```

     ```go Go
     // Sebelum - Ini akan menghasilkan error pada model Claude 4+
     client.Messages.New(ctx, anthropic.MessageNewParams{
     	Model:       "claude-3-7-sonnet-20250219",
     	Temperature: anthropic.Float(0.7),
     	TopP:        anthropic.Float(0.9), // Non-default sampling params return 400 on Opus 4.7
     	// ...
     })

     // Sesudah
     client.Messages.New(ctx, anthropic.MessageNewParams{
     	Model: "claude-opus-4-8",
     	// ...
     })
     ```

     ```java Java
     // Sebelum - Ini akan menghasilkan error pada model Claude 4+
     client.messages().create(MessageCreateParams.builder()
         .model("claude-3-7-sonnet-20250219")
         .temperature(0.7)
         .topP(0.9) // Non-default sampling params return 400 on Opus 4.7
         // ...
         .build());

     // Sesudah
     client.messages().create(MessageCreateParams.builder()
         .model("claude-opus-4-8")
         // ...
         .build());
     ```

     ```php PHP
     // Sebelum - Ini akan menghasilkan error pada model Claude 4+
     $client->messages->create(
         model: 'claude-3-7-sonnet-20250219',
         temperature: 0.7,
         topP: 0.9, // Non-default sampling params return 400 on Opus 4.7
         // ...
     );

     // Sesudah
     $client->messages->create(
         model: 'claude-opus-4-8',
         // ...
     );
     ```

     ```ruby Ruby
     # Sebelum - Ini akan menghasilkan error pada model Claude 4+
     client.messages.create(
       model: "claude-3-7-sonnet-20250219",
       temperature: 0.7,
       top_p: 0.9, # Non-default sampling params return 400 on Opus 4.7
       # ...
     )

     # Sesudah
     client.messages.create(
       model: "claude-opus-4-8",
       # ...
     )
     ```
   </CodeGroup>

2. **Perbarui versi alat**

   <Warning>
     Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru. Hapus semua kode yang menggunakan perintah `undo_edit`.

   <CodeGroup exclude="shell">
     ```python Python
     # Sebelum
     tools = [{"type": "text_editor_20250124", "name": "str_replace_editor"}]

     # Sesudah
     tools = [{"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"}]
     ```

     ```typescript TypeScript
     // Sebelum
     const legacyTools = [{ type: "text_editor_20250124", name: "str_replace_editor" }];

     // Sesudah
     const tools = [{ type: "text_editor_20250728", name: "str_replace_based_edit_tool" }];
     ```

     ```csharp C#
     var parameters = new MessageCreateParams
     {
         // Sebelum: {"type": "text_editor_20250124", "name": "str_replace_editor"}
         // Sesudah:
         Tools = [new ToolTextEditor20250728()],
         // ...
     };
     ```

     ```go Go
     params := anthropic.MessageNewParams{
     	// Sebelum: {"type": "text_editor_20250124", "name": "str_replace_editor"}
     	// Sesudah:
     	Tools: []anthropic.ToolUnionParam{
     		{OfTextEditor20250728: &anthropic.ToolTextEditor20250728Param{}},
     	},
     	// ...
     }
     ```

     ```java Java
     MessageCreateParams params = MessageCreateParams.builder()
         // Sebelum: {"type": "text_editor_20250124", "name": "str_replace_editor"}
         // Sesudah:
         .addTool(ToolTextEditor20250728.builder().build())
         // ...
         .build();
     ```

     ```php PHP
     $message = $client->messages->create(
         // Sebelum: ['type' => 'text_editor_20250124', 'name' => 'str_replace_editor']
         // Sesudah:
         tools: [new ToolTextEditor20250728()],
         // ...
     );
     ```

     ```ruby Ruby
     # Sebelum
     legacy_tools = [{type: "text_editor_20250124", name: "str_replace_editor"}]

     # Sesudah
     tools = [{type: "text_editor_20250728", name: "str_replace_based_edit_tool"}]
     ```
   </CodeGroup>

   * **Text editor:** Gunakan `text_editor_20250728` dan `str_replace_based_edit_tool`. Lihat dokumentasi [alat text editor](/docs/id/agents-and-tools/tool-use/text-editor-tool) untuk detailnya.
   * **Eksekusi kode:** Upgrade ke `code_execution_20260521`. Lihat dokumentasi [alat eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) untuk instruksi migrasi.

3. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals):

   <CodeGroup exclude="shell">
     ```python Python
     response = client.messages.create(...)

     if response.stop_reason == "refusal":
         # Tangani penolakan dengan tepat
         pass
     ```

     ```typescript TypeScript
     const response = await client.messages.create(/* ... */);

     if (response.stop_reason === "refusal") {
       // Tangani penolakan dengan tepat
     }
     ```

     ```csharp C#
     var response = await client.Messages.Create(...);

     if (response.StopReason?.Value() == StopReason.Refusal)
     {
         // Tangani penolakan dengan tepat
     }
     ```

     ```go Go
     response, _ := client.Messages.New(ctx, params) // your existing request

     if response.StopReason == anthropic.StopReasonRefusal {
     	// Tangani penolakan dengan tepat
     }
     ```

     ```java Java
     Message response = client.messages().create(...);

     StopReason reason = response.stopReason().orElse(StopReason.END_TURN);
     if (reason.equals(StopReason.REFUSAL)) {
         // Tangani penolakan dengan tepat
     }
     ```

     ```php PHP
     $response = $client->messages->create(...);

     if ($response->stopReason === 'refusal') {
         // Tangani penolakan dengan tepat
     }
     ```

     ```ruby Ruby
     response = client.messages.create(...)

     if response.stop_reason == :refusal
       # Tangani penolakan dengan tepat
     end
     ```
   </CodeGroup>

4. **Tangani stop reason `model_context_window_exceeded`**

   Model Claude 4.5+ mengembalikan stop reason `model_context_window_exceeded` ketika generasi berhenti karena mencapai batas jendela konteks, bukan batas `max_tokens` yang diminta. Perbarui aplikasi Anda untuk menangani stop reason baru ini:

   <CodeGroup exclude="shell">
     ```python Python
     response = client.messages.create(...)

     if response.stop_reason == "model_context_window_exceeded":
         # Tangani batas jendela konteks dengan tepat
         pass
     ```

     ```typescript TypeScript
     const response = await client.messages.create(/* ... */);

     if (response.stop_reason === "model_context_window_exceeded") {
       // Tangani batas jendela konteks dengan tepat
     }
     ```

     ```csharp C#
     var response = await client.Messages.Create(...);

     if (response.StopReason?.Raw() == "model_context_window_exceeded")
     {
         // Tangani batas jendela konteks dengan tepat
     }
     ```

     ```go Go
     response, _ := client.Messages.New(ctx, params) // your existing request

     if response.StopReason == "model_context_window_exceeded" {
     	// Tangani batas jendela konteks dengan tepat
     }
     ```

     ```java Java
     Message response = client.messages().create(...);

     StopReason reason = response.stopReason().orElse(StopReason.END_TURN);
     if (reason.equals(StopReason.of("model_context_window_exceeded"))) {
         // Tangani batas jendela konteks dengan tepat
     }
     ```

     ```php PHP
     $response = $client->messages->create(...);

     if ($response->stopReason === 'model_context_window_exceeded') {
         // Tangani batas jendela konteks dengan tepat
     }
     ```

     ```ruby Ruby
     response = client.messages.create(...)

     if response.stop_reason == :model_context_window_exceeded
       # Tangani batas jendela konteks dengan tepat
     end
     ```
   </CodeGroup>

5. **Verifikasi penanganan parameter alat (trailing newlines)**

   Model Claude 4.5+ mempertahankan trailing newlines dalam parameter string panggilan alat yang sebelumnya dihapus. Jika alat Anda bergantung pada pencocokan string yang tepat terhadap parameter panggilan alat, verifikasi bahwa logika Anda menangani trailing newlines dengan benar.

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4+ memiliki gaya komunikasi yang lebih ringkas dan langsung serta memerlukan arahan eksplisit. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

##### Perubahan yang direkomendasikan tambahan

* **Hapus header beta lama:** Hapus `token-efficient-tools-2025-02-19` dan `output-128k-2025-02-19`. Semua model Claude 4+ memiliki penggunaan alat yang hemat token bawaan dan header ini tidak berpengaruh.

#### Daftar periksa migrasi (dari Opus 4.5 atau sebelumnya)

* Perbarui ID model ke `claude-opus-4-8`
* Terapkan semua perubahan yang merusak di [Migrasi ke Claude Opus 4.8 dari Claude Opus 4.6](#migrating-from-claude-opus-46) (extended thinking dihapus, parameter sampling dihapus, tampilan pemikiran dihilangkan secara default, tokenisasi yang diperbarui)
* **MERUSAK:** Hapus prefill pesan assistant (mengembalikan error 400); gunakan structured outputs atau `output_config.format` sebagai gantinya
* **MERUSAK pada Opus 4.7:** Ganti `thinking: {type: "enabled", budget_tokens: N}` dengan `thinking: {type: "adaptive"}` ditambah [parameter effort](/docs/id/build-with-claude/effort) (mengembalikan 400 pada Opus 4.7)
* Verifikasi bahwa parsing JSON panggilan alat menggunakan parser JSON standar
* Hapus header beta `effort-2025-11-24` (effort sekarang GA)
* Hapus header beta `fine-grained-tool-streaming-2025-05-14`
* Hapus header beta `interleaved-thinking-2025-05-14` (adaptive thinking mengaktifkan interleaved thinking secara otomatis)
* Migrasikan `output_format` ke `output_config.format` (jika berlaku)
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: hapus `temperature`, `top_p`, dan `top_k` (nilai non-default mengembalikan 400 pada Opus 4.7)
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: perbarui versi alat (`text_editor_20250728`, `code_execution_20260521`)
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: tangani stop reason `refusal`
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: tangani stop reason `model_context_window_exceeded`
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: verifikasi penanganan parameter string alat untuk trailing newlines
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: hapus header beta lama (`token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`)
* Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
* Uji di lingkungan pengembangan sebelum deployment produksi

***

## Migrasi ke Claude Sonnet 5

Claude Sonnet 5 menawarkan kombinasi terbaik antara kecepatan dan kecerdasan dalam keluarga model Claude. Model ini dibangun di atas Claude Sonnet 4.6.

Claude Sonnet 5 adalah upgrade drop-in untuk Claude Sonnet 4.6. Harga perkenalan $2/$10 USD per juta token input/output berlaku hingga 31 Agustus 2026, setelah itu harga standar $3/$15 USD per juta token input/output akan berlaku; lihat [Harga](/docs/id/about-claude/pricing#claude-sonnet-5-introductory-pricing) untuk detailnya. Ada dua perubahan API yang merusak untuk kode yang sudah berjalan pada Claude Sonnet 4.6: extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) dan parameter sampling (`temperature`, `top_p`, `top_k`) yang diatur ke nilai non-default tidak lagi diterima dan mengembalikan error 400. Gunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [parameter effort](/docs/id/build-with-claude/effort) sebagai gantinya. Claude Sonnet 5 mendukung rangkaian fitur yang sama dengan Claude Sonnet 4.6, termasuk [jendela konteks 1M token](/docs/id/build-with-claude/context-windows), [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), [caching prompt](/docs/id/build-with-claude/prompt-caching), [pemrosesan batch](/docs/id/build-with-claude/batch-processing), [Files API](/docs/id/build-with-claude/files), [dukungan PDF](/docs/id/build-with-claude/pdf-support), [vision](/docs/id/build-with-claude/vision), dan rangkaian lengkap [alat](/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien. [Priority Tier](/docs/id/api/service-tiers#supported-models) tidak tersedia pada Claude Sonnet 5. Claude Sonnet 5 juga menggunakan tokenizer baru.

### Migrasi ke Claude Sonnet 5 dari Claude Sonnet 4.6

<Note>
  Jika kode Anda menggunakan Claude Sonnet 4.5 atau versi sebelumnya, terapkan juga [Migrasi ke Claude Sonnet 5 dari Claude Sonnet 4.5 atau versi sebelumnya](#migrating-from-sonnet-45). Langkah-langkah tersebut mencakup perubahan yang merusak kompatibilitas (prefilling pesan assistant ditolak, perbedaan escaping JSON pada parameter alat) yang tidak dicakup oleh bagian ini saja.
</Note>

#### Perbarui nama model Anda

```python
# Migrasi Sonnet
model = "claude-sonnet-4-6"  # Before
model = "claude-sonnet-5"  # After
```

#### Apa yang berubah

Item 4 dan 5 dalam daftar berikut adalah perubahan yang merusak kompatibilitas. `max_tokens` tetap menjadi batas keras untuk total output (pemikiran ditambah teks respons), jadi tinjau kembali untuk beban kerja yang berjalan tanpa pemikiran pada Claude Sonnet 4.6.

1. **Tokenizer baru:** Claude Sonnet 5 menggunakan tokenizer baru. Teks input yang sama menghasilkan sekitar 30% lebih banyak token dibandingkan pada Claude Sonnet 4.6. Peningkatan pastinya bergantung pada konten. Permintaan, respons, dan event streaming mempertahankan bentuk yang sama, dan tidak diperlukan perubahan kode, tetapi apa pun yang Anda ukur atau anggarkan dalam token akan bergeser: field `usage` dan hasil [penghitungan token](/docs/id/build-with-claude/token-counting) untuk teks yang sama menjadi lebih tinggi, jendela konteks 1M token menampung lebih sedikit teks, dan batas `max_tokens` yang disetel untuk Claude Sonnet 4.6 dapat memotong output yang setara. Harga per token tidak berubah, sehingga biaya permintaan yang setara dapat berbeda. Jalankan kembali penghitungan token terhadap Claude Sonnet 5 alih-alih menggunakan kembali hitungan yang diukur terhadap model sebelumnya.

2. **128k token output maksimum (tidak berubah):** Claude Sonnet 5 mendukung hingga 128k token output, sama seperti Claude Sonnet 4.6. Nilai `max_tokens` yang ada tetap valid. Perhitungkan tokenizer baru saat menentukan ukurannya.

3. **Prefilling pesan assistant (tidak berubah):** Prefilling pesan assistant mengembalikan error `400` pada Claude Sonnet 5, sama seperti pada Claude Sonnet 4.6. Jika Anda menghapus prefill saat bermigrasi ke Claude Sonnet 4.6, tidak diperlukan perubahan lebih lanjut. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

4. **Adaptive thinking aktif secara default:** Pada Claude Sonnet 4.6, permintaan tanpa field `thinking` berjalan tanpa pemikiran; pada Claude Sonnet 5, permintaan yang sama berjalan dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking). Untuk menonaktifkan pemikiran, kirimkan `thinking: {type: "disabled"}`. Extended thinking (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung dan mengembalikan error 400. Gunakan [parameter effort](/docs/id/build-with-claude/effort) (default `high`) untuk mengontrol kedalaman pemikiran.

   <Tabs>
     <Tab title="Claude Sonnet 5">
       <Note>
         Adaptive thinking aktif secara default untuk Claude Sonnet 5. Field `thinking` ditampilkan secara eksplisit di sini untuk mengatur `display: "summarized"`; jika Anda menghilangkan `thinking`, Claude Sonnet 5 menghilangkan konten pemikiran dari respons secara default. Untuk default per model, lihat [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking).
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
         ant messages create \
           --transform content --format yaml <<'YAML'
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

6. **Pengamanan keamanan siber:** Claude Sonnet 5 adalah model tingkat Sonnet pertama dengan pengamanan keamanan siber real-time. Permintaan yang melibatkan topik keamanan siber yang dilarang atau berisiko tinggi dapat ditolak. Penolakan dikembalikan sebagai respons HTTP 200 yang berhasil dengan `stop_reason: "refusal"`, bukan error. Lihat [Safeguards, warnings, and appeals](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals) untuk latar belakang.

#### Daftar periksa migrasi

* Perbarui nama model dari `claude-sonnet-4-6` menjadi `claude-sonnet-5`.
* Jalankan kembali [penghitungan token](/docs/id/build-with-claude/token-counting) terhadap Claude Sonnet 5. Tokenizer baru menghasilkan sekitar 30% lebih banyak token untuk teks yang sama, yang dapat mengubah biaya per permintaan meskipun harga per token tidak berubah. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja.
* Tinjau kembali batas `max_tokens` yang ditentukan mendekati panjang output yang Anda harapkan, dan naikkan hingga maksimum 128k (tidak berubah dari Claude Sonnet 4.6) jika berguna.
* Hapus konfigurasi `thinking: {type: "enabled", budget_tokens: N}` (mengembalikan error 400). Adaptive thinking aktif secara default; kirimkan `{type: "disabled"}` untuk menonaktifkannya, atau gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman.
* Hapus parameter `temperature`, `top_p`, dan `top_k` yang diatur ke nilai non-default (parameter tersebut mengembalikan error 400 pada Claude Sonnet 5).
* Tambahkan penanganan untuk `stop_reason: "refusal"` jika beban kerja Anda mungkin menyentuh topik keamanan siber.
* Tetapkan ulang baseline biaya pada beban kerja tipikal Anda sebelum deployment produksi.
* Tinjau `max_tokens` untuk beban kerja yang sebelumnya berjalan tanpa pemikiran.

### Migrasi ke Claude Sonnet 5 dari Claude Sonnet 4.5 atau versi sebelumnya

Jika Anda bermigrasi dari Claude Sonnet 4.5 atau model Sonnet yang lebih lama langsung ke Claude Sonnet 5, terapkan perubahan [Migrasi ke Claude Sonnet 5 dari Claude Sonnet 4.6](#migrating-from-claude-sonnet-4-6-to-claude-sonnet-5) ditambah perubahan di bagian ini.

<Warning>
  Claude Sonnet 5 secara default menggunakan tingkat effort `high`, berbeda dengan Sonnet 4.5 yang tidak memiliki parameter effort. Pertimbangkan untuk menyesuaikan [parameter effort](/docs/id/build-with-claude/effort) saat Anda bermigrasi. Jika tidak diatur secara eksplisit, Anda mungkin mengalami latensi yang lebih tinggi dengan tingkat effort default.
</Warning>

#### Perubahan yang merusak kompatibilitas

##### Saat bermigrasi dari Sonnet 4.5

1. **Prefilling pesan assistant tidak lagi didukung**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari Sonnet 4.5 atau versi sebelumnya.
   </Warning>

   Prefilling pesan assistant mengembalikan error `400` pada Claude Sonnet 4.6 dan model yang lebih baru, termasuk Claude Sonnet 5. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

   **Kasus penggunaan prefill yang umum dan migrasinya:**

   * **Mengontrol format output** (memaksa output JSON/YAML): Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs) atau alat dengan field enum untuk tugas klasifikasi.

   * **Menghilangkan pembukaan** (menghapus frasa "Here is..."): Tambahkan instruksi langsung di prompt sistem: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc."

   * **Menghindari penolakan yang tidak tepat:** Claude sekarang jauh lebih baik dalam melakukan penolakan yang tepat. Prompting yang jelas dalam pesan pengguna tanpa prefill seharusnya sudah cukup.

   * **Kelanjutan** (melanjutkan respons yang terputus): Pindahkan kelanjutan ke pesan pengguna: "Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off."

   * **Hidrasi konteks / konsistensi peran** (menyegarkan konteks dalam percakapan panjang): Suntikkan apa yang sebelumnya merupakan pengingat prefilled-assistant ke dalam giliran pengguna sebagai gantinya.

2. **Escaping JSON pada parameter alat mungkin berbeda**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari Sonnet 4.5 atau versi sebelumnya.
   </Warning>

   Escaping string JSON dalam parameter alat mungkin berbeda dari model sebelumnya. Parser JSON standar menangani ini secara otomatis, tetapi parsing berbasis string kustom mungkin perlu diperbarui.

**Perubahan extended thinking (pemikiran diperpanjang):** Konfigurasi `budget_tokens` dari Claude Sonnet 4.5 (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung pada Claude Sonnet 5 dan mengembalikan error 400. Adaptive thinking aktif secara default, sehingga sebagian besar beban kerja tidak memerlukan konfigurasi `thinking` sama sekali; gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran. Jika Anda menjalankan Claude Sonnet 4.5 tanpa pemikiran diperpanjang, kirimkan `thinking: {type: "disabled"}` untuk mempertahankan perilaku tersebut.

##### Saat bermigrasi dari Claude 3.x

3. **Hapus parameter sampling**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
   </Warning>

   Parameter sampling (`temperature`, `top_p`, `top_k`) yang diatur ke nilai non-default mengembalikan error 400 pada Claude Sonnet 5. Hapus parameter tersebut dari permintaan, dan gunakan prompting untuk memandu perilaku model sebagai gantinya.

4. **Perbarui versi alat**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20260521`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

5. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

***

## Migrasi ke Claude Haiku 4.5

Claude Haiku 4.5 adalah model Haiku tercepat dan paling cerdas dengan performa mendekati frontier, memberikan kualitas model premium untuk aplikasi interaktif dan pemrosesan volume tinggi.

Untuk gambaran lengkap tentang kemampuannya, lihat [gambaran umum model](/docs/id/about-claude/models/overview).

<Note>
  Untuk harga Claude Haiku 4.5, lihat [harga Claude](/docs/id/about-claude/pricing).
</Note>

<Tip>
  Untuk peningkatan performa yang signifikan pada tugas coding dan penalaran, pertimbangkan untuk mengaktifkan pemikiran diperpanjang dengan `thinking: {type: "enabled", budget_tokens: N}`.
</Tip>

<Note>
  Pemikiran diperpanjang memengaruhi efisiensi [caching prompt](/docs/id/build-with-claude/prompt-caching#caching-with-thinking-blocks).

  Pemikiran diperpanjang sudah usang (deprecated) pada model Claude 4.6 dan dihapus pada Claude Opus 4.7. Jika menggunakan model yang lebih baru, gunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) sebagai gantinya.
</Note>

### Migrasi ke Claude Haiku 4.5 dari Claude Haiku 3.5 atau versi sebelumnya

**Perbarui nama model Anda:**

```python
# Dari Haiku 3.5
model = "claude-3-5-haiku-20241022"  # Before
model = "claude-haiku-4-5-20251001"  # After
```

**Tinjau batas laju baru:** Haiku 4.5 memiliki batas laju yang terpisah dari Haiku 3.5. Lihat dokumentasi [Batas laju](/docs/id/api/rate-limits) untuk detailnya.

**Jelajahi kemampuan baru:** Lihat [gambaran umum model](/docs/id/about-claude/models/overview) untuk detail tentang kesadaran konteks, peningkatan kapasitas output (64k token), kecerdasan yang lebih tinggi, dan kecepatan yang lebih baik.

#### Perubahan yang merusak kompatibilitas

Perubahan yang merusak kompatibilitas ini berlaku saat bermigrasi dari model Claude 3.x Haiku.

1. **Perbarui parameter sampling**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya. Mengatur keduanya mengembalikan error 400 pada Claude Haiku 4.5.

2. **Perbarui versi alat**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

3. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

#### Daftar periksa migrasi Haiku 4.5

* Perbarui ID model menjadi `claude-haiku-4-5-20251001`
* **MERUSAK KOMPATIBILITAS:** Perbarui versi alat ke yang terbaru (`text_editor_20250728`, `code_execution_20250825`); versi lama tidak didukung
* **MERUSAK KOMPATIBILITAS:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
* **MERUSAK KOMPATIBILITAS:** Perbarui parameter sampling untuk menggunakan hanya `temperature` ATAU `top_p`, bukan keduanya (mengatur keduanya mengembalikan error 400)
* Tangani stop reason `refusal` baru di aplikasi Anda
* Tinjau dan sesuaikan untuk batas laju baru (terpisah dari Haiku 3.5)
* Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
* Pertimbangkan untuk mengaktifkan pemikiran diperpanjang untuk tugas penalaran yang kompleks
* Uji di lingkungan pengembangan sebelum deployment produksi

***

## Dapatkan bantuan

* Periksa [dokumentasi API](/docs/id/api/overview) untuk spesifikasi terperinci
* Tinjau [kemampuan model](/docs/id/about-claude/models/overview) untuk perbandingan performa
* Tinjau [catatan rilis API](/docs/id/release-notes/api) untuk pembaruan API
* Hubungi dukungan jika Anda mengalami masalah selama migrasi
