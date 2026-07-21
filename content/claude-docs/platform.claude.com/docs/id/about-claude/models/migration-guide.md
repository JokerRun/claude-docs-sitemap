---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/migration-guide
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 0690dd9d64818ce86429eb3a8f08e46da300c77f8b9e28da689b0afc5837c7b1
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

  Skill ini menerapkan penggantian ID model dan, sesuai kebutuhan, perubahan parameter yang bersifat breaking, penggantian prefill, dan kalibrasi effort untuk model target Anda di seluruh basis kode Anda, lalu menghasilkan daftar periksa item yang perlu diverifikasi secara manual. Skill ini meminta Anda mengonfirmasi cakupan migrasi (seluruh direktori kerja, subdirektori, atau daftar file tertentu) sebelum mengedit file apa pun. Skill ini juga mendeteksi klien Amazon Bedrock, Google Cloud, Claude Platform on AWS, dan Microsoft Foundry serta menyesuaikan format ID model dan perubahan fitur untuk setiap platform.
</Tip>

## Bermigrasi dari Claude Mythos Preview ke Claude Mythos 5

[Claude Mythos 5](https://anthropic.com/glasswing) adalah penerus dengan akses terbatas dari [Claude Mythos Preview](https://anthropic.com/glasswing), pratinjau riset khusus undangan. Untuk model yang tersedia secara umum dengan kemampuan yang sama, lihat [Claude Fable 5](/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5).

Migrasi sebagian besar bersifat drop-in. Claude Mythos 5 menggunakan [Messages API](/docs/id/build-with-claude/working-with-messages) yang sama dan pola [tool use](/docs/id/agents-and-tools/tool-use/overview) (penggunaan alat) yang sama dengan Claude Mythos Preview, dan jumlah token kurang lebih tidak berubah karena kedua model menggunakan tokenizer yang sama. Perubahan utama yang perlu diperiksa adalah fitur-fitur yang tidak lagi tersedia (tercantum di bagian berikutnya) dan output pemikiran.

Untuk linimasa penghentian Claude Mythos Preview, lihat [Penghentian model](/docs/id/about-claude/model-deprecations).

### Perbarui nama model Anda

```python
model = "claude-mythos-preview"  # Before
model = "claude-mythos-5"  # After
```

### Fitur yang tidak tersedia di Claude Mythos 5

1. **Extended thinking dan anggaran token pemikiran:** "Extended thinking" (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung di `claude-mythos-5` dan mengembalikan error 400. [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) selalu aktif: model menentukan kapan dan seberapa banyak berpikir pada setiap permintaan, dan tidak diperlukan konfigurasi `thinking`. `thinking: {type: "disabled"}` mengembalikan error. `budget_tokens` tidak memiliki pengganti langsung: pemikiran bersifat adaptif, dan [parameter effort](/docs/id/build-with-claude/effort) adalah kontrol tingkat output yang terpisah, bukan anggaran pemikiran.

   Sebelum (Claude Mythos Preview):

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
          --header "x-api-key: $ANTHROPIC_API_KEY" \
          --header "anthropic-version: 2023-06-01" \
          --header "content-type: application/json" \
          --data \
     '{
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
          --header "x-api-key: $ANTHROPIC_API_KEY" \
          --header "anthropic-version: 2023-06-01" \
          --header "content-type: application/json" \
          --data \
     '{
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

2. **Prefill asisten:** Melakukan prefill pada pesan asisten tidak didukung di `claude-mythos-5` dan mengembalikan error 400, sama seperti di Claude Mythos Preview. Gunakan instruksi prompt sistem sebagai gantinya.

3. **Output pemikiran:** Di `claude-mythos-5`, rantai pemikiran mentah tidak pernah dikembalikan, tetapi blok thinking tetap membawa teks ringkasan yang dapat dibaca ketika `thinking.display` disetel ke `summarized`. Kirimkan kembali blok thinking tanpa perubahan saat melanjutkan percakapan pada model yang sama. Lihat [Output pemikiran di Claude Fable 5 dan Claude Mythos 5](/docs/id/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).

### Penghitungan token dan penagihan

`claude-mythos-5` menggunakan tokenizer yang sama dengan `claude-mythos-preview` (tokenizer yang diperkenalkan dengan Claude Opus 4.7). Jumlah token kurang lebih tidak berubah saat bermigrasi dari `claude-mythos-preview`. Dibandingkan dengan model sebelum Claude Opus 4.7, konten yang sama dapat ditokenisasi menjadi sekitar 30% lebih banyak token, bervariasi menurut konten dan bentuk beban kerja.

[`/v1/messages/count_tokens`](/docs/id/build-with-claude/token-counting) mengembalikan nilai yang kurang lebih tidak berubah untuk `claude-mythos-5` dibandingkan dengan `claude-mythos-preview`. Lakukan baseline ulang biaya dan latensi pada beban kerja Anda sendiri.

### Daftar periksa migrasi

* Perbarui nama model dari `claude-mythos-preview` ke `claude-mythos-5`.
* Hapus konfigurasi extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`). Adaptive thinking selalu aktif, dan tidak diperlukan field `thinking`.
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun. Menonaktifkan thinking mengembalikan error di `claude-mythos-5`.
* Hapus `budget_tokens`. Parameter ini tidak memiliki pengganti langsung: pemikiran bersifat adaptif, dan parameter `effort` adalah kontrol tingkat output yang terpisah, bukan anggaran pemikiran.
* Verifikasi bahwa kode apa pun yang mem-parsing field `thinking` memperlakukannya hanya sebagai teks tampilan dan mengirimkan kembali blok thinking tanpa perubahan saat melanjutkan pada model yang sama. `thinking.display` secara default bernilai `"omitted"` di `claude-mythos-5`, sama seperti di Claude Mythos Preview; setel `display: "summarized"` untuk menerima ringkasan yang dapat dibaca. Lihat [Output pemikiran di Claude Fable 5 dan Claude Mythos 5](/docs/id/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).
* Jika Anda memutar ulang riwayat percakapan pada model lain, hapus blok `thinking` dan `redacted_thinking` dari giliran asisten sebelumnya terlebih dahulu. Blok thinking dari `claude-mythos-5` terikat pada model yang menghasilkannya, dan model selain Claude Fable 5 dan Claude Mythos 5 mengabaikannya secara diam-diam. Penghapusan ini menjaga permintaan lintas model tetap minimal dan seragam.
* Lakukan baseline ulang jumlah token dan biaya pada beban kerja Anda sendiri. Jumlah token kurang lebih tidak berubah saat bermigrasi dari `claude-mythos-preview`.

## Bermigrasi dari Claude Opus 4.8 ke Claude Fable 5

[Claude Fable 5](/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) adalah model Anthropic yang paling mumpuni yang dirilis secara luas, tersedia secara umum di Claude API, [Claude Platform on AWS](/docs/id/build-with-claude/claude-platform-on-aws), [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock), [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry).

Migrasi sebagian besar bersifat drop-in. Claude Fable 5 menggunakan [Messages API](/docs/id/build-with-claude/working-with-messages) yang sama dan pola [penggunaan alat](/docs/id/agents-and-tools/tool-use/overview) yang sama dengan Claude Opus 4.8. Model ini mendukung [jendela konteks 1M token](/docs/id/build-with-claude/context-windows) yang sama secara default dan [maksimum 128k token output](/docs/id/about-claude/models/overview) yang sama. Jumlah token kurang lebih tidak berubah karena kedua model menggunakan tokenizer yang sama.

Perubahan utama yang perlu diperiksa adalah [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) yang selalu aktif, output pemikiran, penolakan oleh classifier keamanan, dan harga. [Sebelum Anda bermigrasi](#before-you-migrate) membahas harga dan retensi data; [Apa yang berubah](#what-changed) membahas sisanya.

### Sebelum Anda bermigrasi

Claude Fable 5 dihargai $10 per juta token input dan $50 per juta token output, dibandingkan dengan $5 dan $25 untuk Claude Opus 4.8. Lihat [Harga Claude](/docs/id/about-claude/pricing) untuk detailnya.

Claude Fable 5 memerlukan retensi data 30 hari dan tidak tersedia di bawah pengaturan zero data retention (ZDR); model ini ditetapkan sebagai Covered Model. Di Claude API, permintaan dari organisasi yang konfigurasi retensi datanya tidak memenuhi persyaratan ini mengembalikan `invalid_request_error` 400. Organisasi dengan pengaturan ZDR harus menghubungi tim akun Anthropic mereka untuk mendiskusikan konfigurasi retensi data; Claude Opus 4.8 tetap tersedia di bawah ZDR. Sebagai alternatif, Anda dapat mengonfigurasi retensi data per workspace. Persyaratan retensi data 30 hari berlaku di setiap platform tempat Claude Fable 5 ditawarkan; lihat [Persyaratan retensi data spesifik model](/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements) untuk detail per platform.

<Note>
  Jika kode Anda berada di Claude Opus 4.7 atau lebih lama, terapkan terlebih dahulu [Bermigrasi dari Claude Opus 4.7 ke Claude Opus 4.8](#migrating-from-claude-opus-47) dan, untuk model yang lebih lama dari Claude Opus 4.7, [langkah-langkah migrasi Claude Opus 4.7](#migrating-to-claude-opus-4-7). Bagian-bagian tersebut mencakup perubahan yang bersifat breaking (parameter sampling ditolak, extended thinking manual ditolak, prefill dihapus, tokenizer baru) yang tidak diulang di bagian ini.
</Note>

### Perbarui nama model Anda

```python
model = "claude-opus-4-8"  # Before
model = "claude-fable-5"  # After
```

### Apa yang berubah

Item di bagian ini menjelaskan perbedaan API dan perilaku yang perlu diperiksa setelah Anda mengganti ID model.

1. **Adaptive thinking selalu aktif:** [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) adalah satu-satunya mode thinking di `claude-fable-5`. Model menentukan kapan dan seberapa banyak berpikir pada setiap permintaan, dan tidak diperlukan konfigurasi `thinking`. `thinking: {type: "disabled"}` mengembalikan error. Gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran.

   Perubahan perilaku yang perlu diperiksa: di Claude Opus 4.8, permintaan tanpa field `thinking` berjalan tanpa thinking; di `claude-fable-5`, permintaan yang sama berjalan dengan adaptive thinking. `max_tokens` tetap menjadi batas keras pada total output, thinking ditambah teks respons, jadi tinjau kembali untuk beban kerja yang berjalan tanpa thinking di Claude Opus 4.8. Lihat [Kontrol biaya](/docs/id/build-with-claude/adaptive-thinking#cost-control).

   Sebelum (Claude Opus 4.8):

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
          --header "x-api-key: $ANTHROPIC_API_KEY" \
          --header "anthropic-version: 2023-06-01" \
          --header "content-type: application/json" \
          --data \
     '{
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
          --header "x-api-key: $ANTHROPIC_API_KEY" \
          --header "anthropic-version: 2023-06-01" \
          --header "content-type: application/json" \
          --data \
     '{
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

2. **Extended thinking dan anggaran thinking (tidak berubah):** Extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung di `claude-fable-5` dan mengembalikan error 400, sama seperti di Claude Opus 4.8. `budget_tokens` tidak memiliki pengganti langsung: pemikiran bersifat adaptif, dan [parameter effort](/docs/id/build-with-claude/effort) adalah kontrol tingkat output yang terpisah, bukan anggaran pemikiran.

3. **Prefill asisten (tidak berubah):** Melakukan prefill pada pesan asisten tidak didukung di `claude-fable-5` dan mengembalikan error 400, sama seperti di Claude Opus 4.8. Gunakan instruksi prompt sistem sebagai gantinya.

4. **Output pemikiran:** Di `claude-fable-5`, rantai pemikiran mentah tidak pernah dikembalikan, tetapi blok thinking tetap membawa teks ringkasan yang dapat dibaca ketika `thinking.display` disetel ke `summarized`. Kirimkan kembali blok thinking tanpa perubahan saat melanjutkan percakapan pada model yang sama. Lihat [Output pemikiran di Claude Fable 5 dan Claude Mythos 5](/docs/id/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).

5. **Classifier keamanan dan stop reason `refusal`:** `claude-fable-5` menjalankan classifier keamanan pada permintaan dan selama pembuatan respons. Ketika classifier menolak permintaan, Messages API mengembalikan `stop_reason: "refusal"` sebagai respons HTTP 200 yang berhasil, bukan error. Field `stop_details.category` melaporkan classifier mana yang terpicu, dengan kategori seperti `"cyber"`, `"bio"`, dan `"reasoning_extraction"`, atau `null` ketika penolakan tidak terpetakan ke kategori bernama mana pun. Lihat [tabel kategori penolakan](/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk daftar lengkapnya.

   Anda tidak ditagih untuk token input dari permintaan yang ditolak sebelum output apa pun dihasilkan. Ketika classifier terpicu di tengah stream, input dan output yang sudah di-stream akan ditagih; buang output parsial tersebut.

   Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, kirimkan parameter opt-in `fallbacks`, yang berstatus beta di Claude API dan Claude Platform on AWS. Parameter ini tidak tersedia di Message Batches API atau di Amazon Bedrock, Google Cloud, dan Microsoft Foundry; di ketiga platform tersebut, jalankan percobaan ulang di sisi klien atau gunakan middleware refusal-fallback SDK. Lihat [Menangani stop reason](/docs/id/build-with-claude/refusals-and-fallback).

6. **Mulai dari effort `high`:** Default [parameter effort](/docs/id/build-with-claude/effort) tetap `high`. Di Claude Opus 4.8, rekomendasi untuk pekerjaan coding dan otonomi tinggi adalah menyetel `xhigh` secara eksplisit. Di `claude-fable-5`, gunakan `high` sebagai default untuk sebagian besar tugas dan simpan `xhigh` untuk beban kerja yang paling sensitif terhadap kemampuan. Pengaturan effort yang lebih rendah di `claude-fable-5` tetap berkinerja baik dan sering melampaui kinerja `xhigh` pada model sebelumnya. Kurangi effort jika tugas selesai tetapi memakan waktu lebih lama dari yang diperlukan. Lihat [Prompting Claude Fable 5](/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5#consider-all-effort-levels).

7. **Minimum caching prompt yang lebih rendah:** Panjang prompt minimum yang dapat di-cache di `claude-fable-5` adalah 512 token, lebih rendah dari 1.024 token di Claude Opus 4.8. Prompt yang terlalu pendek untuk di-cache di Claude Opus 4.8 sekarang dapat membuat entri cache, tanpa perubahan kode yang diperlukan. Di Amazon Bedrock, minimum untuk `claude-fable-5` adalah 1.024 token. Lihat [Prompt caching](/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

### Daftar periksa migrasi

* Jika organisasi Anda memiliki pengaturan zero data retention (ZDR), konfirmasikan kelayakan sebelum bermigrasi. `claude-fable-5` memerlukan retensi data 30 hari dan, di Claude API, mengembalikan `invalid_request_error` 400 jika tidak. Lihat [Persyaratan retensi data spesifik model](/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Perbarui nama model dari `claude-opus-4-8` ke `claude-fable-5`.
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun. Menonaktifkan thinking mengembalikan error di `claude-fable-5`, dan permintaan tanpa field `thinking` berjalan dengan adaptive thinking.
* Jika Anda telah menghapus extended thinking manual dan prefill asisten selama migrasi sebelumnya, tidak ada tindakan yang diperlukan: keduanya tetap tidak didukung di `claude-fable-5`.
* Verifikasi bahwa kode apa pun yang mem-parsing field `thinking` memperlakukannya hanya sebagai teks tampilan dan mengirimkan kembali blok thinking tanpa perubahan saat melanjutkan pada model yang sama. `thinking.display` secara default bernilai `"omitted"` di `claude-fable-5`, sama seperti di Claude Opus 4.8; setel `display: "summarized"` untuk menerima ringkasan yang dapat dibaca. Lihat [Output pemikiran di Claude Fable 5 dan Claude Mythos 5](/docs/id/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).
* Jika Anda memutar ulang riwayat percakapan pada model lain, hapus blok `thinking` dan `redacted_thinking` dari giliran asisten sebelumnya terlebih dahulu. Blok thinking dari `claude-fable-5` terikat pada model yang menghasilkannya, dan model selain Claude Fable 5 dan Claude Mythos 5 mengabaikannya secara diam-diam. Penghapusan ini menjaga permintaan lintas model tetap minimal dan seragam. Pengecualiannya adalah menukarkan [kredit fallback](/docs/id/build-with-claude/fallback-credit), yang memerlukan body permintaan yang digaungkan kembali sesuai aturan persis fitur tersebut.
* Tangani `stop_reason: "refusal"` dan baca field `stop_details.category`. Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, pertimbangkan parameter opt-in `fallbacks` (beta). Lihat [Menangani stop reason](/docs/id/build-with-claude/refusals-and-fallback).
* Evaluasi ulang pengaturan `effort` Anda. Mulai dari `high` untuk sebagian besar tugas, termasuk beban kerja yang berjalan pada `xhigh` di Claude Opus 4.8.
* Lakukan baseline ulang biaya dan latensi pada beban kerja Anda sendiri. Jumlah token kurang lebih tidak berubah saat bermigrasi dari `claude-opus-4-8`; harga per token berbeda.

## Bermigrasi dari Claude Opus 4.7 ke Claude Opus 4.8

Claude Opus 4.8 dibangun untuk coding agentik yang kompleks dan pekerjaan enterprise. Model ini dibangun di atas Claude Opus 4.7.

Claude Opus 4.8 seharusnya memiliki kinerja out-of-the-box yang kuat pada prompt dan eval Claude Opus 4.7 yang sudah ada. Tidak ada perubahan API yang bersifat breaking untuk kode yang sudah berjalan di Claude Opus 4.7. Model ini mendukung rangkaian fitur yang sama dengan Claude Opus 4.7, termasuk [jendela konteks 1M token](/docs/id/build-with-claude/context-windows), [maksimum 128k token output](/docs/id/about-claude/models/overview), [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), [prompt caching](/docs/id/build-with-claude/prompt-caching) (caching prompt), [pemrosesan batch](/docs/id/build-with-claude/batch-processing), [Files API](/docs/id/build-with-claude/files), [dukungan PDF](/docs/id/build-with-claude/pdf-support), [vision](/docs/id/build-with-claude/vision), dan rangkaian lengkap [alat](/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien. Model ini juga menambahkan [pesan sistem di tengah percakapan](/docs/id/about-claude/models/whats-new-claude-4-8#mid-conversation-system-messages) dan mendokumentasikan secara publik [detail stop penolakan](/docs/id/about-claude/models/whats-new-claude-4-8#refusal-stop-details).

<Note>
  Jika kode Anda berada di Claude Opus 4.6 atau lebih lama, terapkan juga [langkah-langkah migrasi Claude Opus 4.7](#migrating-to-claude-opus-4-7) di bawah ini sebelum meningkatkan ke Claude Opus 4.8. Langkah-langkah tersebut mencakup perubahan yang bersifat breaking (parameter sampling ditolak, extended thinking manual ditolak, tokenizer baru) yang tidak tercakup oleh peningkatan ke 4.8 saja.
</Note>

### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-7"  # Before
model = "claude-opus-4-8"  # After
```

### Apa yang berubah

Ini bukan perubahan yang bersifat breaking. Kode yang berjalan di Claude Opus 4.7 tetap bekerja tanpa perubahan di Claude Opus 4.8. Item di bawah ini menjelaskan perbedaan perilaku yang perlu diperiksa setelah Anda mengganti ID model.

1. **Parameter sampling (tidak berubah):** Menyetel `temperature`, `top_p`, atau `top_k` ke nilai non-default mengembalikan error 400 di Claude Opus 4.8, sama seperti di Claude Opus 4.7. Tipe permintaan SDK masih mendefinisikan field-field ini untuk kompatibilitas dengan model sebelumnya, sehingga kode yang menyetelnya lolos pemeriksaan tipe, tetapi API menolak permintaan di sisi server. Jika Anda telah menghapus parameter-parameter ini saat bermigrasi ke Opus 4.7, tidak diperlukan perubahan lebih lanjut.

2. **Default effort adalah `high`:** Default [parameter effort](/docs/id/build-with-claude/effort) di Claude Opus 4.8 adalah `high` di semua permukaan, termasuk Claude Code dan Messages API. Jika Anda sudah menyetel effort secara eksplisit, pengaturan Anda tidak berubah. Untuk pekerjaan coding dan otonomi tinggi, setel `xhigh` secara eksplisit. Evaluasi ulang pengaturan effort Anda terhadap anggaran latensi dan biaya Anda.

3. **Jendela konteks 1M adalah default:** Claude Opus 4.8 menyajikan [jendela konteks](/docs/id/build-with-claude/context-windows) 1M token penuh secara default tanpa header beta dan tanpa premi konteks panjang. Jika klien Anda mengirimkan header beta jendela konteks untuk kompatibilitas dengan model yang lebih lama, Anda dapat menghapusnya di Claude Opus 4.8.

4. **Pesan sistem di tengah percakapan:** Claude Opus 4.8 menerima pesan `role: "system"` segera setelah giliran pengguna dalam array `messages` (tunduk pada [aturan penempatan](/docs/id/build-with-claude/mid-conversation-system-messages#limitations)). Gunakan field `system` tingkat atas untuk instruksi yang berlaku sejak awal. Model sebelumnya, termasuk Claude Opus 4.7, menolak `role: "system"` dalam `messages` dengan error 400. Jika Anda memelihara jalur kode yang membangun ulang seluruh riwayat pesan untuk memperbarui instruksi, Anda dapat menyederhanakannya dan mempertahankan hit [cache prompt](/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya.

5. **Detail stop penolakan:** Objek `stop_details` pada respons penolakan (tersedia sejak Claude Opus 4.7) sekarang didokumentasikan secara publik. Ketika model menolak permintaan, model mengidentifikasi kategori penolakan, selain stop reason `refusal` yang sudah ada. Tidak diperlukan header beta, dan tidak ada opsi untuk menonaktifkannya. Lihat [Menangani stop reason](/docs/id/build-with-claude/handling-stop-reasons).

6. **Minimum caching prompt yang lebih rendah:** Panjang prompt minimum yang dapat di-cache di Claude Opus 4.8 adalah 1.024 token, lebih rendah daripada di Claude Opus 4.7. Prompt yang terlalu pendek untuk di-cache di Claude Opus 4.7 sekarang dapat membuat entri cache, tanpa perubahan kode yang diperlukan. Lihat [Prompt caching](/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

7. **Level effort dikalibrasi ulang:** Alokasi token di balik setiap level effort berubah di Claude Opus 4.8 dibandingkan dengan Claude Opus 4.7: `medium` memungkinkan pemikiran yang sedikit lebih banyak, `high` sedikit lebih sedikit, dan `xhigh` jauh lebih banyak. Jika Anda menyetel level effort berdasarkan biaya atau latensi Claude Opus 4.7, lakukan baseline ulang pada level yang sama sebelum menyesuaikannya. Lihat [Effort](/docs/id/build-with-claude/effort).

### Daftar periksa migrasi

* Perbarui nama model dari `claude-opus-4-7` ke `claude-opus-4-8` (atau perbarui alias).
* Jika Anda telah menghapus parameter sampling selama migrasi Opus 4.7, tidak ada tindakan yang diperlukan. Jika Anda menambahkannya kembali dengan jalur percobaan ulang 400, hapus jalur percobaan ulang tersebut.
* Evaluasi ulang pengaturan `effort` Anda. Default-nya adalah `high` di semua permukaan; untuk pekerjaan coding dan otonomi tinggi, setel `xhigh` secara eksplisit.
* Hapus header beta jendela konteks apa pun. Jendela konteks 1M adalah default di Claude API, Amazon Bedrock, Google Cloud, dan Microsoft Foundry.
* Jika Anda membangun ulang riwayat percakapan untuk memperbarui instruksi, pertimbangkan untuk beralih ke pesan sistem di tengah percakapan untuk mempertahankan hit cache prompt.
* Verifikasi bahwa penanganan stop reason Anda membaca `stop_details` pada penolakan (tersedia sejak Claude Opus 4.7; sekarang didokumentasikan secara publik).
* Lakukan baseline ulang biaya dan latensi pada level effort yang Anda pilih.

## Bermigrasi ke Claude Opus 4.7

Claude Opus 4.7 sangat otonom dan berkinerja sangat baik pada pekerjaan agentik jangka panjang, pekerjaan pengetahuan, tugas vision, dan tugas memori.

Claude Opus 4.7 seharusnya memiliki kinerja out-of-the-box yang kuat pada prompt dan eval Claude Opus 4.6 yang sudah ada dengan harga `$5 / $25` per MTok yang sama, tetapi ada beberapa perubahan perilaku dan API yang perlu diketahui saat Anda bermigrasi. Model ini mendukung rangkaian fitur yang sama dengan Claude Opus 4.6, termasuk:

* [Jendela konteks 1M token](/docs/id/build-with-claude/context-windows) dengan harga API standar tanpa premi konteks panjang
* [Maksimum 128k token output](/docs/id/about-claude/models/overview)
* [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking)
* [Prompt caching](/docs/id/build-with-claude/prompt-caching)
* [Pemrosesan batch](/docs/id/build-with-claude/batch-processing)
* [Files API](/docs/id/build-with-claude/files)
* [Dukungan PDF](/docs/id/build-with-claude/pdf-support)
* [Vision](/docs/id/build-with-claude/vision)
* Rangkaian lengkap [alat](/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien ([bash](/docs/id/agents-and-tools/tool-use/bash-tool), [eksekusi kode](/docs/id/agents-and-tools/tool-use/code-execution-tool), [computer use](/docs/id/agents-and-tools/tool-use/computer-use-tool), [text editor](/docs/id/agents-and-tools/tool-use/text-editor-tool), [pencarian web](/docs/id/agents-and-tools/tool-use/web-search-tool), [web fetch](/docs/id/agents-and-tools/tool-use/web-fetch-tool), [konektor MCP](/docs/id/agents-and-tools/mcp-connector), [memori](/docs/id/agents-and-tools/tool-use/memory-tool))

### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-6"  # Before
model = "claude-opus-4-7"  # After
```

### Perubahan yang bersifat breaking

1. **Extended thinking dihapus:** `thinking: {type: "enabled", budget_tokens: N}` tidak lagi didukung di Claude Opus 4.7 atau model yang lebih baru dan mengembalikan error 400. Beralihlah ke [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) (`thinking: {type: "adaptive"}`) dan gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengontrol kedalaman pemikiran. Adaptive thinking **nonaktif secara default** di Claude Opus 4.7: permintaan tanpa field `thinking` berjalan tanpa thinking, sesuai dengan perilaku Opus 4.6. Setel `thinking: {type: "adaptive"}` secara eksplisit untuk mengaktifkannya.

   Sebelum (Claude Opus 4.6):

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
          --header "x-api-key: $ANTHROPIC_API_KEY" \
          --header "anthropic-version: 2023-06-01" \
          --header "content-type: application/json" \
          --data \
     '{
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

   Sesudah (Claude Opus 4.7):

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
          --header "x-api-key: $ANTHROPIC_API_KEY" \
          --header "anthropic-version: 2023-06-01" \
          --header "content-type: application/json" \
          --data \
     '{
         "model": "claude-opus-4-7",
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
     model: claude-opus-4-7
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
         model="claude-opus-4-7",
         max_tokens=16000,
         thinking={"type": "adaptive"},
         output_config={"effort": "high"},  # or "max", "xhigh", "medium", "low"
         messages=[{"role": "user", "content": "..."}],
     )
     ```

     ```typescript TypeScript
     await client.messages.create({
       model: "claude-opus-4-7",
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
         Model = "claude-opus-4-7",
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
     	Model:     "claude-opus-4-7",
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
         .model("claude-opus-4-7")
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
         model: 'claude-opus-4-7',
         thinking: ['type' => 'adaptive'],
         outputConfig: ['effort' => 'high'], // or 'max', 'xhigh', 'medium', 'low'
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: "claude-opus-4-7",
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

   Adaptive thinking dapat diarahkan melalui prompting. Untuk panduan penyetelan ketika model berpikir berlebihan atau kurang berpikir, lihat [Mengkalibrasi effort dan kedalaman pemikiran](/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-4-8#calibrating-effort-and-thinking-depth).

2. **Parameter sampling dihapus:** Menyetel `temperature`, `top_p`, atau `top_k` ke nilai non-default apa pun di Claude Opus 4.7 mengembalikan error 400. Jalur migrasi yang paling aman adalah menghilangkan parameter-parameter ini sepenuhnya dari payload permintaan. Prompting adalah cara yang direkomendasikan untuk memandu perilaku model di Claude Opus 4.7. Jika Anda menggunakan `temperature = 0` untuk determinisme, perhatikan bahwa hal itu tidak pernah menjamin output yang identik pada model sebelumnya.

3. **Konten thinking dihilangkan secara default:** Blok thinking masih muncul dalam stream respons di Claude Opus 4.7, tetapi field `thinking`-nya kosong kecuali Anda secara eksplisit memilih untuk mengaktifkannya. Ini adalah perubahan diam-diam dari Claude Opus 4.6, di mana default-nya adalah mengembalikan teks thinking yang diringkas. Untuk memulihkan konten thinking yang diringkas di Claude Opus 4.7, setel `thinking.display` ke `"summarized"`:

   <CodeGroup>
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

   Default-nya adalah `"omitted"` di Claude Opus 4.7. Jika produk Anda melakukan streaming penalaran kepada pengguna, default baru ini tampak sebagai jeda panjang sebelum output dimulai; setel `display: "summarized"` untuk memulihkan progres yang terlihat selama thinking. Lihat [Extended thinking](/docs/id/build-with-claude/extended-thinking#controlling-thinking-display) untuk detailnya.

4. **Penghitungan token yang diperbarui:** Claude Opus 4.7 menggunakan tokenizer baru, yang berkontribusi pada peningkatan kinerjanya pada berbagai tugas. Tokenizer baru ini dapat menggunakan sekitar 1x hingga 1,35x lebih banyak token saat memproses teks dibandingkan dengan model sebelumnya (hingga \~35% lebih banyak, bervariasi menurut konten).

   [`/v1/messages/count_tokens`](/docs/id/build-with-claude/token-counting) akan mengembalikan jumlah token yang berbeda untuk Claude Opus 4.7 dibandingkan dengan Claude Opus 4.6. Efisiensi token dapat bervariasi menurut bentuk beban kerja.

   Intervensi prompting, `task_budget`, dan `effort` dapat membantu mengontrol biaya dan memastikan penggunaan token yang sesuai. Kontrol-kontrol ini dapat mengorbankan kecerdasan model. Perbarui parameter `max_tokens` Anda untuk memberikan ruang tambahan, termasuk pemicu pemadatan. Claude Opus 4.7 menyediakan jendela konteks 1M dengan harga API standar tanpa premi konteks panjang.

5. **Penghapusan prefill (dibawa dari Opus 4.6):** Melakukan prefill pada pesan asisten mengembalikan error 400 di Claude Opus 4.7. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

### Memilih level effort

[Parameter effort](/docs/id/build-with-claude/effort) memungkinkan Anda menyetel keseimbangan antara kecerdasan Claude dan pengeluaran token, menukar kemampuan dengan kecepatan yang lebih tinggi dan biaya yang lebih rendah. Mulailah dengan level effort `xhigh` yang baru untuk kasus penggunaan coding dan agentik, dan gunakan minimum effort `high` untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan. Bereksperimenlah dengan level effort lain untuk lebih menyetel penggunaan token dan kecerdasan:

* **`max`:** Effort maksimum dapat memberikan peningkatan kinerja dalam beberapa kasus penggunaan, tetapi mungkin menunjukkan hasil yang semakin berkurang dari peningkatan penggunaan token. Pengaturan ini juga terkadang rentan terhadap pemikiran berlebihan. Uji effort maksimum untuk tugas yang menuntut kecerdasan.
* **`xhigh` (baru):** Effort ekstra tinggi adalah pengaturan terbaik untuk sebagian besar kasus penggunaan coding dan agentik.
* **`high`:** Pengaturan ini menyeimbangkan penggunaan token dan kecerdasan. Untuk sebagian besar kasus penggunaan yang sensitif terhadap kecerdasan, gunakan minimum effort `high`.
* **`medium`:** Baik untuk kasus penggunaan yang sensitif terhadap biaya yang perlu mengurangi penggunaan token sambil mengorbankan kecerdasan.
* **`low`:** Simpan untuk tugas pendek yang terbatas cakupannya dan beban kerja yang sensitif terhadap latensi yang tidak sensitif terhadap kecerdasan.

Effort lebih penting untuk model ini daripada untuk Opus mana pun sebelumnya. Bereksperimenlah dengannya secara aktif saat Anda melakukan upgrade.

### Perubahan perilaku

Claude Opus 4.7 memiliki beberapa perbedaan perilaku dari Claude Opus 4.6 yang bukan merupakan perubahan yang merusak API tetapi mungkin memerlukan pembaruan prompt atau penghapusan scaffolding.

1. **Panjang respons bervariasi berdasarkan kasus penggunaan:** Claude Opus 4.7 mengkalibrasi panjang respons berdasarkan seberapa kompleks tugas tersebut menurut penilaiannya, alih-alih menggunakan tingkat verbositas tetap secara default. Ini biasanya berarti jawaban yang lebih pendek untuk pencarian sederhana dan jawaban yang jauh lebih panjang untuk analisis terbuka.

   Jika produk Anda bergantung pada gaya atau verbositas output tertentu, Anda mungkin perlu menyetel prompt Anda. Misalnya, untuk mengurangi verbositas, tambahkan: "Provide concise, focused responses. Skip non-essential context, and keep examples minimal." Jika Anda melihat jenis penjelasan berlebihan tertentu, tambahkan instruksi yang ditargetkan dalam prompt Anda untuk mencegahnya.

   Contoh positif yang menunjukkan bagaimana Claude dapat berkomunikasi dengan tingkat keringkasan yang sesuai cenderung lebih efektif daripada contoh negatif atau instruksi yang memberi tahu model apa yang tidak boleh dilakukan.

2. **Mengikuti instruksi secara lebih literal:** Claude Opus 4.7 menafsirkan prompt secara lebih literal dan eksplisit daripada Claude Opus 4.6, terutama pada tingkat effort yang lebih rendah. Model ini tidak akan secara diam-diam menggeneralisasi instruksi dari satu item ke item lain, dan tidak akan menyimpulkan permintaan yang tidak Anda buat. Keuntungan dari literalisme ini adalah presisi dan lebih sedikit kekacauan. Model ini umumnya berkinerja lebih baik untuk kasus penggunaan API dengan prompt yang disetel dengan cermat, ekstraksi terstruktur, dan pipeline di mana Anda menginginkan perilaku yang dapat diprediksi. Peninjauan prompt dan harness mungkin sangat membantu untuk migrasi ke Claude Opus 4.7.

3. **Nada yang lebih langsung:** Seperti halnya model baru lainnya, gaya prosa pada penulisan bentuk panjang mungkin berubah. Claude Opus 4.7 lebih langsung dan berpendirian, dengan lebih sedikit frasa yang bersifat memvalidasi dan lebih sedikit emoji dibandingkan gaya Claude Opus 4.6 yang lebih hangat. Jika produk Anda bergantung pada suara tertentu, evaluasi ulang prompt gaya terhadap baseline baru.

4. **Pembaruan kemajuan bawaan dalam jejak agentik:** Claude Opus 4.7 memberikan pembaruan yang lebih teratur dan berkualitas lebih tinggi kepada pengguna sepanjang jejak agentik yang panjang. Jika Anda telah menambahkan scaffolding untuk memaksa pesan status sementara ("Setelah setiap 3 panggilan alat, rangkum kemajuan"), coba hapus. Jika Anda menemukan bahwa panjang atau isi pembaruan yang ditampilkan kepada pengguna dari Claude Opus 4.7 tidak terkalibrasi dengan baik untuk kasus penggunaan Anda, jelaskan secara eksplisit seperti apa pembaruan ini seharusnya dalam prompt dan berikan contoh.

5. **Lebih sedikit subagen yang dibuat secara default:** Claude Opus 4.7 cenderung membuat lebih sedikit subagen secara default. Namun, perilaku ini dapat diarahkan melalui prompting; berikan Claude Opus 4.7 panduan eksplisit tentang kapan subagen diinginkan.

6. **Kalibrasi effort yang lebih ketat:** Berubah secara signifikan dari Claude Opus 4.6, Claude Opus 4.7 mematuhi [tingkat effort](/docs/id/build-with-claude/effort) secara ketat, terutama pada tingkat rendah. Pada `low` dan `medium`, model membatasi pekerjaannya pada apa yang diminta alih-alih melakukan lebih dari yang diperlukan.

   Ini baik untuk latensi dan biaya, tetapi pada tugas yang cukup kompleks yang berjalan pada effort `low` ada risiko pemikiran yang kurang mendalam. Jika Anda mengamati penalaran yang dangkal pada masalah kompleks, naikkan effort ke `high` atau `xhigh` alih-alih mengatasinya melalui prompt.

   Jika Anda perlu mempertahankan effort pada `low` untuk latensi, tambahkan panduan yang ditargetkan: "This task involves multi-step reasoning. Think carefully through the problem before responding." Lihat [Tingkat effort yang direkomendasikan untuk Claude Opus 4.7](/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-opus-4-7).

7. **Lebih sedikit panggilan alat secara default:** Claude Opus 4.7 memiliki kecenderungan untuk menggunakan alat lebih jarang daripada Claude Opus 4.6 dan lebih banyak menggunakan penalaran. Ini menghasilkan hasil yang lebih baik dalam sebagian besar kasus.

   Untuk meningkatkan penggunaan alat, naikkan pengaturan effort. Pengaturan effort `high` atau `xhigh` menunjukkan penggunaan alat yang jauh lebih banyak dalam pencarian agentik dan pengkodean. Anda juga dapat menyesuaikan prompt Anda untuk secara eksplisit menginstruksikan model tentang kapan dan bagaimana menggunakan alatnya dengan benar.

8. **Perlindungan keamanan siber real-time:** Baru ditambahkan di Claude Opus 4.7, permintaan yang melibatkan topik terlarang atau berisiko tinggi dapat menyebabkan penolakan. Untuk pekerjaan keamanan yang sah seperti pengujian penetrasi, penelitian kerentanan, atau red-teaming, ajukan permohonan ke [Cyber Verification Program](https://claude.com/form/cyber-use-case) untuk meminta pengurangan pembatasan. Lihat [Safeguards, warnings, and appeals](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals) untuk latar belakang.

9. **Dukungan gambar resolusi tinggi:** Claude Opus 4.7 adalah model Claude pertama dengan dukungan gambar resolusi tinggi. Resolusi gambar maksimum adalah 2576 piksel pada sisi terpanjang, naik dari 1568 piksel pada model sebelumnya. Ini membuka peningkatan pada beban kerja yang berat pada visi dan sangat berharga untuk penggunaan komputer, pemahaman tangkapan layar, dan analisis dokumen.

   Dukungan resolusi tinggi bersifat otomatis dan tidak memerlukan header beta atau opt-in dari sisi klien. Dua hal yang perlu direncanakan:

   * Gambar resolusi penuh dapat menggunakan hingga sekitar 3x lebih banyak token gambar dibandingkan model sebelumnya (hingga 4.784 token per gambar, dibandingkan dengan batas sebelumnya sekitar 1.600 token per gambar). Anggarkan ulang `max_tokens` dan ekspektasi biaya untuk beban kerja yang berat pada gambar, atau lakukan downsampling sebelum mengirim jika Anda tidak memerlukan fidelitas tambahan.
   * Koordinat penunjukan dan bounding-box yang dikembalikan oleh model adalah 1:1 dengan piksel gambar aktual pada Claude Opus 4.7, sehingga tidak diperlukan konversi faktor skala.

   Lihat [Dukungan gambar resolusi tinggi pada Claude Opus 4.7](/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) untuk detailnya.

### Perubahan yang direkomendasikan

Perubahan ini tidak wajib tetapi akan meningkatkan pengalaman Anda:

1. **Evaluasi ulang `max_tokens`:** Karena teks yang sama menghasilkan jumlah token yang lebih tinggi pada Claude Opus 4.7, perbarui parameter `max_tokens` Anda untuk memberikan ruang tambahan, termasuk pemicu kompaksi. Intervensi prompting, [`task_budget`](/docs/id/build-with-claude/task-budgets), dan [`effort`](/docs/id/build-with-claude/effort) dapat membantu mengendalikan biaya dan memastikan penggunaan token yang sesuai.

2. **Audit ekspektasi jumlah token:** Setiap jalur kode yang memperkirakan token di sisi klien atau mengasumsikan rasio token-ke-karakter yang tetap harus diuji ulang terhadap Claude Opus 4.7. Gunakan [endpoint penghitungan token](/docs/id/build-with-claude/token-counting) untuk memverifikasi.

3. **Adopsi [task budgets](/docs/id/build-with-claude/task-budgets) (beta):** Claude Opus 4.7 memperkenalkan task budgets. Anggaran ini memungkinkan Anda memberi tahu Claude berapa banyak token yang dimilikinya untuk satu loop agentik penuh, termasuk pemikiran, panggilan alat, hasil alat, dan output akhir. Model melihat hitungan mundur yang berjalan dan menggunakannya untuk memprioritaskan pekerjaan dan menyelesaikan tugas dengan baik saat anggaran terpakai. Untuk menggunakannya, atur header beta `task-budgets-2026-03-13` dan tambahkan yang berikut ke konfigurasi output Anda:

   <CodeGroup>
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

   Anda mungkin perlu bereksperimen dengan task budget yang berbeda untuk kasus penggunaan Anda. Jika model diberi task budget yang terlalu ketat, model mungkin menyelesaikan tugas dengan kurang menyeluruh, dengan merujuk anggarannya sebagai kendala.

   Untuk tugas agentik terbuka di mana kualitas lebih penting daripada kecepatan, jangan atur task budget. Cadangkan task budget untuk beban kerja di mana Anda memerlukan model untuk membatasi pekerjaannya pada alokasi token. Nilai minimum untuk task budget adalah 20k token.

   Task budget bukanlah batas keras; ini adalah saran yang disadari oleh model. Ini berbeda dari `max_tokens`:

   * **`task_budget`:** batas penasihat di seluruh loop agentik penuh. Model melihatnya dan menggunakannya untuk mengatur kecepatannya sendiri.
   * **`max_tokens`:** batas keras per permintaan pada token yang dihasilkan. Ini tidak diteruskan ke model, sehingga model tidak menyadarinya.

   Gunakan `task_budget` ketika Anda ingin model mengatur dirinya sendiri, dan `max_tokens` sebagai batas keras untuk membatasi penggunaan.

4. **Atur `max_tokens` yang besar pada effort `max` atau `xhigh`:** Jika Anda menjalankan Claude Opus 4.7 pada effort `max` atau `xhigh`, atur anggaran token output maksimum yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan panggilan alatnya. Mulai dari 64k token dan sesuaikan dari sana.

5. **Lakukan downsampling gambar jika resolusi tinggi tidak diperlukan:** Claude Opus 4.7 mendukung gambar hingga 2576px / 3,75MP. Gambar resolusi tinggi menggunakan lebih banyak token. Jika fidelitas gambar tambahan tidak diperlukan, lakukan downsampling gambar sebelum mengirim ke Claude untuk menghindari peningkatan penggunaan token. Lihat [Gambar dan visi](/docs/id/build-with-claude/vision).

### Daftar periksa migrasi

* Perbarui nama model dari `claude-opus-4-6` ke `claude-opus-4-7` (atau perbarui alias).
* Hapus `temperature`, `top_p`, dan `top_k` dari payload permintaan.
* Ganti `thinking: {type: "enabled", budget_tokens: N}` dengan `thinking: {type: "adaptive"}` ditambah [parameter effort](/docs/id/build-with-claude/effort).
* Hapus semua prefill pesan asisten.
* Jika UI Anda menampilkan konten pemikiran, lakukan opt-in secara eksplisit ke ringkasan pemikiran.
* Lakukan benchmark ulang biaya dan latensi end-to-end dengan tokenisasi yang diperbarui.
* Setel ulang `max_tokens` untuk memperhitungkan tokenisasi yang diperbarui.
* Uji ulang semua estimasi jumlah token di sisi klien.
* Jika aplikasi Anda mengirim gambar, anggarkan ulang untuk [dukungan gambar resolusi tinggi](/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) (hingga sekitar 3x lebih banyak token gambar per gambar resolusi penuh). Lakukan downsampling sebelum mengirim jika Anda tidak memerlukan fidelitas tambahan.
* Jika Anda menggunakan koordinat penunjukan atau bounding-box dari model, hapus semua konversi faktor skala; koordinat adalah 1:1 dengan piksel gambar aktual pada Claude Opus 4.7.
* Tinjau prompt untuk perubahan perilaku di atas (panjang respons, literalisme, nada, pembaruan kemajuan, subagen, kalibrasi effort, pemicu alat, perlindungan siber, penanganan gambar resolusi tinggi).
* Tetapkan ulang baseline panjang respons dengan menghapus prompt pengendali panjang yang ada, lalu setel secara eksplisit.
* Jika menggunakan effort `xhigh` atau `max`, naikkan `max_tokens` ke setidaknya 64k sebagai titik awal.
* Pertimbangkan untuk mengadopsi task budgets (beta) untuk alur kerja agentik.
* Jika produk Anda melakukan pekerjaan keamanan yang sah, ajukan permohonan ke [Cyber Verification Program](https://claude.com/form/cyber-use-case) untuk mendapatkan akses ke pembatasan yang lebih rendah pada konten siber.

## Migrasi ke Claude Opus 4.7 dari Opus 4.5 atau sebelumnya

Jika Anda bermigrasi dari Claude Opus 4.5, Opus 4.1 (usang), atau model sebelumnya langsung ke Claude Opus 4.7, terapkan **semua [perubahan Opus 4.7](#migrating-to-claude-opus-4-7)** ditambah perubahan kumulatif di bagian ini yang berlaku antara Opus 4.5 dan Opus 4.7. Jika Anda bermigrasi dari Opus 4.6, Anda hanya memerlukan [bagian Opus 4.7](#migrating-to-claude-opus-4-7).

### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-5"  # Before
model = "claude-opus-4-7"  # After
```

### Perubahan yang merusak

1. **Penghapusan prefill** dibahas di [perubahan yang merusak Opus 4.7](#breaking-changes) di atas.

2. **Pengutipan parameter alat:** Claude Opus 4.6 dan model yang lebih baru mungkin menghasilkan escaping string JSON yang sedikit berbeda dalam argumen panggilan alat (misalnya, penanganan yang berbeda untuk escape Unicode atau escaping garis miring). Jika Anda mem-parsing `input` panggilan alat sebagai string mentah alih-alih menggunakan parser JSON, verifikasi logika parsing Anda. Parser JSON standar (seperti `json.loads()` atau `JSON.parse()`) menangani perbedaan ini secara otomatis.

### Perubahan yang direkomendasikan

Perubahan ini meningkatkan pengalaman Anda pada Opus 4.7. Item yang ditandai **(wajib pada Opus 4.7)** adalah rekomendasi opsional saat Opus 4.6 diluncurkan tetapi sekarang wajib; sisanya tetap direkomendasikan.

1. **Migrasi ke adaptive thinking (wajib pada Opus 4.7):** `thinking: {type: "enabled", budget_tokens: N}` mengembalikan error 400 pada Claude Opus 4.7. Beralih ke `thinking: {type: "adaptive"}` dan gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengendalikan kedalaman pemikiran. Lihat [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking).

   <CodeGroup>
     ```bash cURL
     curl -sS https://api.anthropic.com/v1/messages \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d '{
         "model": "claude-opus-4-7",
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
         model="claude-opus-4-7",
         max_tokens=16000,
         thinking={"type": "adaptive"},
         output_config={"effort": "high"},
         messages=[{"role": "user", "content": "Your prompt here"}],
     )
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-opus-4-7
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
       model: "claude-opus-4-7",
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
         Model = Model.ClaudeOpus4_7,
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
     	Model:     anthropic.ModelClaudeOpus4_7,
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
             AnthropicClient client = AnthropicOkHttpClient.fromEnv();

             MessageCreateParams params = MessageCreateParams.builder()
                 .model(Model.CLAUDE_OPUS_4_7)
                 .maxTokens(16000L)
                 .thinking(ThinkingConfigAdaptive.builder().build())
                 .outputConfig(OutputConfig.builder()
                     .effort(OutputConfig.Effort.HIGH)
                     .build())
                 .addUserMessage("Your prompt here")
                 .build();

             Message response = client.messages().create(params);
             System.out.println(response);
     ```

     ```php PHP
     $client = new Client();

     $response = $client->messages->create(
         maxTokens: 16000,
         messages: [['role' => 'user', 'content' => 'Your prompt here']],
         model: 'claude-opus-4-7',
         thinking: ['type' => 'adaptive'],
         outputConfig: ['effort' => 'high'],
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     response = client.messages.create(
       model: "claude-opus-4-7",
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

4. **Hapus header beta interleaved thinking:** Adaptive thinking secara otomatis mengaktifkan interleaved thinking pada Claude Opus 4.7, Opus 4.6, dan Sonnet 4.6. Hapus `betas=["interleaved-thinking-2025-05-14"]` dari permintaan Anda. Header ini masih berfungsi pada Sonnet 4.6 dengan extended thinking manual, tetapi mode manual sudah usang.

5. **Migrasi ke output\_config.format:** Jika menggunakan structured outputs, perbarui `output_format={...}` menjadi `output_config={"format": {...}}`. Parameter lama tetap berfungsi tetapi sudah usang dan akan dihapus dalam rilis model mendatang.

### Migrasi dari Claude 4.1 atau sebelumnya

Jika Anda bermigrasi dari Opus 4.1 (usang) atau model sebelumnya langsung ke Claude Opus 4.7, terapkan perubahan Claude Opus 4.7 di bagian atas panduan ini dan perubahan kumulatif di atas ditambah perubahan tambahan di bagian ini.

```python
# Dari Opus 4.1
model = "claude-opus-4-1-20250805"  # Before
model = "claude-opus-4-7"  # After

# Dari Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Before
model = "claude-opus-4-7"  # After
```

#### Perubahan yang merusak tambahan

1. **Hapus parameter sampling**

   <Warning>
     Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Mulai dari Claude Opus 4.7, mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default apa pun akan mengembalikan error 400. Jalur migrasi teraman adalah menghilangkan parameter ini sepenuhnya dari permintaan, dan menggunakan prompting untuk memandu perilaku model. Jika Anda menggunakan `temperature = 0` untuk determinisme, perhatikan bahwa itu tidak pernah menjamin output yang identik.

   <CodeGroup>
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
         model="claude-opus-4-7",
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
       model: "claude-opus-4-7"
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
         Model = "claude-opus-4-7",
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
     	Model: "claude-opus-4-7",
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
         .model("claude-opus-4-7")
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
         model: 'claude-opus-4-7',
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
       model: "claude-opus-4-7",
       # ...
     )
     ```
   </CodeGroup>

2. **Perbarui versi alat**

   <Warning>
     Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru. Hapus semua kode yang menggunakan perintah `undo_edit`.

   <CodeGroup>
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

   * **Text editor:** Gunakan `text_editor_20250728` dan `str_replace_based_edit_tool`. Lihat [dokumentasi alat text editor](/docs/id/agents-and-tools/tool-use/text-editor-tool) untuk detailnya.
   * **Code execution:** Tingkatkan ke `code_execution_20260521`. Lihat [dokumentasi alat code execution](/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) untuk instruksi migrasi.

3. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals):

   <CodeGroup>
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

   Model Claude 4.5+ mengembalikan stop reason `model_context_window_exceeded` ketika pembuatan berhenti karena mencapai batas jendela konteks, bukan batas `max_tokens` yang diminta. Perbarui aplikasi Anda untuk menangani stop reason baru ini:

   <CodeGroup>
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

5. **Verifikasi penanganan parameter alat (newline di akhir)**

   Model Claude 4.5+ mempertahankan newline di akhir dalam parameter string panggilan alat yang sebelumnya dihapus. Jika alat Anda bergantung pada pencocokan string yang tepat terhadap parameter panggilan alat, verifikasi bahwa logika Anda menangani newline di akhir dengan benar.

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4+ memiliki gaya komunikasi yang lebih ringkas dan langsung serta memerlukan arahan eksplisit. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

#### Perubahan tambahan yang direkomendasikan

* **Hapus header beta lama:** Hapus `token-efficient-tools-2025-02-19` dan `output-128k-2025-02-19`. Semua model Claude 4+ memiliki penggunaan alat yang hemat token secara bawaan dan header ini tidak berpengaruh.

### Daftar periksa migrasi (dari Opus 4.5 atau sebelumnya)

* Perbarui ID model ke `claude-opus-4-7`
* Terapkan semua [perubahan yang merusak Opus 4.7](#migrating-to-claude-opus-4-7) (extended thinking dihapus, parameter sampling dihapus, tampilan pemikiran dihilangkan secara default, tokenisasi yang diperbarui)
* **MERUSAK:** Hapus prefill pesan asisten (mengembalikan error 400); gunakan structured outputs atau `output_config.format` sebagai gantinya
* **MERUSAK pada Opus 4.7:** Ganti `thinking: {type: "enabled", budget_tokens: N}` dengan `thinking: {type: "adaptive"}` ditambah [parameter effort](/docs/id/build-with-claude/effort) (mengembalikan 400 pada Opus 4.7)
* Verifikasi bahwa parsing JSON panggilan alat menggunakan parser JSON standar
* Hapus header beta `effort-2025-11-24` (effort sekarang GA)
* Hapus header beta `fine-grained-tool-streaming-2025-05-14`
* Hapus header beta `interleaved-thinking-2025-05-14` (adaptive thinking mengaktifkan interleaved thinking secara otomatis)
* Migrasi `output_format` ke `output_config.format` (jika berlaku)
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: hapus `temperature`, `top_p`, dan `top_k` (nilai non-default mengembalikan 400 pada Opus 4.7)
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: perbarui versi alat (`text_editor_20250728`, `code_execution_20260521`)
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: tangani stop reason `refusal`
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: tangani stop reason `model_context_window_exceeded`
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: verifikasi penanganan parameter string alat untuk newline di akhir
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: hapus header beta lama (`token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`)
* Tinjau dan perbarui prompt dengan mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
* Uji di lingkungan pengembangan sebelum penerapan produksi

***

## Migrasi dari Claude Sonnet 4.6 ke Claude Sonnet 5

Claude Sonnet 5 menawarkan kombinasi terbaik antara kecepatan dan kecerdasan dalam keluarga model Claude. Model ini dibangun di atas Claude Sonnet 4.6.

Claude Sonnet 5 adalah peningkatan langsung untuk Claude Sonnet 4.6 dengan harga yang sama `$3 / $15` per MTok (harga perkenalan $2 / $10 per MTok hingga 31 Agustus 2026; lihat [Harga](/docs/id/about-claude/pricing#claude-sonnet-5-introductory-pricing)). Ada dua perubahan API yang merusak untuk kode yang sudah berjalan pada Claude Sonnet 4.6: extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) dan parameter sampling (`temperature`, `top_p`, `top_k`) yang diatur ke nilai non-default tidak lagi diterima dan mengembalikan error 400. Gunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [parameter effort](/docs/id/build-with-claude/effort) sebagai gantinya. Claude Sonnet 5 mendukung kumpulan fitur yang sama dengan Claude Sonnet 4.6, termasuk [jendela konteks 1M token](/docs/id/build-with-claude/context-windows), [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking), [caching prompt](/docs/id/build-with-claude/prompt-caching), [pemrosesan batch](/docs/id/build-with-claude/batch-processing), [Files API](/docs/id/build-with-claude/files), [dukungan PDF](/docs/id/build-with-claude/pdf-support), [visi](/docs/id/build-with-claude/vision), dan kumpulan lengkap [alat](/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien. [Priority Tier](/docs/id/api/service-tiers#supported-models) tidak tersedia pada Claude Sonnet 5. Claude Sonnet 5 juga menggunakan tokenizer baru.

<Note>
  Jika kode Anda menggunakan Claude Sonnet 4.5 atau sebelumnya, terapkan juga [langkah migrasi Claude Sonnet 4.6](#migrating-to-claude-sonnet-4-6) sebelum meningkatkan ke Claude Sonnet 5. Langkah-langkah tersebut mencakup perubahan yang merusak (prefill pesan asisten ditolak, perbedaan escaping JSON parameter alat) yang tidak tercakup oleh peningkatan Sonnet 5 saja.
</Note>

### Perbarui nama model Anda

```python
# Migrasi Sonnet
model = "claude-sonnet-4-6"  # Before
model = "claude-sonnet-5"  # After
```

### Apa yang berubah

Item 4 dan 5 dalam daftar berikut adalah perubahan yang merusak. `max_tokens` tetap menjadi batas keras pada total output (pemikiran ditambah teks respons), jadi tinjau kembali untuk beban kerja yang berjalan tanpa pemikiran pada Claude Sonnet 4.6.

1. **Tokenizer baru:** Claude Sonnet 5 menggunakan tokenizer baru. Teks input yang sama menghasilkan sekitar 30% lebih banyak token dibandingkan pada Claude Sonnet 4.6. Peningkatan pastinya bergantung pada konten. Permintaan, respons, dan event streaming mempertahankan bentuk yang sama, dan tidak diperlukan perubahan kode, tetapi apa pun yang Anda ukur atau anggarkan dalam token akan bergeser: field `usage` dan hasil [penghitungan token](/docs/id/build-with-claude/token-counting) untuk teks yang sama lebih tinggi, jendela konteks 1M token menampung lebih sedikit teks, dan batas `max_tokens` yang disetel untuk Claude Sonnet 4.6 dapat memotong output yang setara. Harga per token tidak berubah, sehingga biaya permintaan yang setara dapat berbeda. Jalankan ulang penghitungan token terhadap Claude Sonnet 5 alih-alih menggunakan kembali hitungan yang diukur terhadap model sebelumnya.

2. **128k token output maksimum (tidak berubah):** Claude Sonnet 5 mendukung hingga 128k token output, sama seperti Claude Sonnet 4.6. Nilai `max_tokens` yang ada tetap valid. Perhitungkan tokenizer baru saat menentukan ukurannya.

3. **Prefill pesan asisten (tidak berubah):** Melakukan prefill pada pesan asisten mengembalikan error `400` pada Claude Sonnet 5, sama seperti pada Claude Sonnet 4.6. Jika Anda menghapus prefill saat bermigrasi ke Claude Sonnet 4.6, tidak diperlukan perubahan lebih lanjut. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

4. **Adaptive thinking aktif secara default:** Pada Claude Sonnet 4.6, permintaan tanpa field `thinking` berjalan tanpa pemikiran; pada Claude Sonnet 5, permintaan yang sama berjalan dengan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking). Untuk menonaktifkan pemikiran, berikan `thinking: {type: "disabled"}`. Extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung dan mengembalikan error 400. Gunakan [parameter effort](/docs/id/build-with-claude/effort) (default `high`) untuk mengendalikan kedalaman pemikiran.

   <Tabs>
     <Tab title="Claude Sonnet 5">
       <Note>
         Adaptive thinking aktif secara default untuk Claude Sonnet 5. Field `thinking` ditampilkan secara eksplisit di sini untuk mengatur `display: "summarized"`; jika Anda menghilangkan `thinking`, Claude Sonnet 5 menghilangkan konten pemikiran dari respons secara default. Untuk default per model, lihat [Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking).
       </Note>

       <CodeGroup>
         ```bash cURL
         curl https://api.anthropic.com/v1/messages \
              --header "x-api-key: $ANTHROPIC_API_KEY" \
              --header "anthropic-version: 2023-06-01" \
              --header "content-type: application/json" \
              --data \
         '{
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

6. **Perlindungan keamanan siber:** Claude Sonnet 5 adalah model tingkat Sonnet pertama dengan perlindungan keamanan siber real-time. Permintaan yang melibatkan topik keamanan siber yang terlarang atau berisiko tinggi dapat ditolak. Penolakan dikembalikan sebagai respons HTTP 200 yang berhasil dengan `stop_reason: "refusal"`, bukan error. Lihat [Safeguards, warnings, and appeals](https://support.claude.com/en/articles/8241253-safeguards-warnings-and-appeals) untuk latar belakang.

### Daftar periksa migrasi

* Perbarui nama model dari `claude-sonnet-4-6` ke `claude-sonnet-5`.
* Jalankan ulang [penghitungan token](/docs/id/build-with-claude/token-counting) terhadap Claude Sonnet 5. Tokenizer baru menghasilkan sekitar 30% lebih banyak token untuk teks yang sama, yang dapat mengubah biaya per permintaan meskipun harga per token tidak berubah. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja.
* Tinjau kembali batas `max_tokens` yang ditetapkan mendekati panjang output yang Anda harapkan, dan naikkan hingga maksimum 128k (tidak berubah dari Claude Sonnet 4.6) jika berguna.
* Hapus konfigurasi `thinking: {type: "enabled", budget_tokens: N}` (mengembalikan error 400). Adaptive thinking aktif secara default; berikan `{type: "disabled"}` untuk menonaktifkannya, atau gunakan [parameter effort](/docs/id/build-with-claude/effort) untuk mengendalikan kedalaman.
* Hapus parameter `temperature`, `top_p`, dan `top_k` yang diatur ke nilai non-default (mengembalikan error 400 pada Claude Sonnet 5).
* Tambahkan penanganan untuk `stop_reason: "refusal"` jika beban kerja Anda mungkin menyentuh topik keamanan siber.
* Tetapkan ulang baseline biaya pada beban kerja tipikal Anda sebelum penerapan produksi.
* Tinjau `max_tokens` untuk beban kerja yang sebelumnya berjalan tanpa pemikiran.

***

## Migrasi ke Claude Sonnet 4.6

Claude Sonnet 4.6 menggabungkan kecerdasan yang kuat dengan kinerja yang cepat, menampilkan kemampuan pencarian agentik yang ditingkatkan dan eksekusi kode gratis saat digunakan dengan pencarian web atau pengambilan web. Model ini ideal untuk pengkodean sehari-hari, analisis, dan tugas konten.

Untuk ikhtisar lengkap tentang kemampuan, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

<Note>
  Harga Sonnet 4.6 adalah $3 per juta token input, $15 per juta token output. Lihat [harga Claude](/docs/id/about-claude/pricing) untuk detailnya.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Sonnet 4.5
model = "claude-sonnet-4-5"  # Before
model = "claude-sonnet-4-6"  # After
```

### Perubahan yang merusak

#### Saat bermigrasi dari Sonnet 4.5

1. **Prefill pesan asisten tidak lagi didukung**

   <Warning>
     Ini adalah perubahan yang merusak saat bermigrasi dari Sonnet 4.5 atau sebelumnya.
   </Warning>

   Melakukan prefill pada pesan asisten mengembalikan error `400` pada Sonnet 4.6. Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

   **Kasus penggunaan prefill yang umum dan migrasinya:**

   * **Mengendalikan pemformatan output** (memaksa output JSON/YAML): Gunakan [structured outputs](/docs/id/build-with-claude/structured-outputs) atau alat dengan field enum untuk tugas klasifikasi.

   * **Menghilangkan pembukaan** (menghapus frasa "Here is..."): Tambahkan instruksi langsung dalam prompt sistem: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc."

   * **Menghindari penolakan yang tidak tepat:** Claude sekarang jauh lebih baik dalam melakukan penolakan yang tepat. Prompting yang jelas dalam pesan pengguna tanpa prefill seharusnya sudah cukup.

   * **Kelanjutan** (melanjutkan respons yang terputus): Pindahkan kelanjutan ke pesan pengguna: "Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off."

   * **Hidrasi konteks / konsistensi peran** (menyegarkan konteks dalam percakapan panjang): Suntikkan apa yang sebelumnya merupakan pengingat prefill asisten ke dalam giliran pengguna sebagai gantinya.

2. **Escaping JSON parameter alat mungkin berbeda**

   <Warning>
     Ini adalah perubahan yang merusak saat bermigrasi dari Sonnet 4.5 atau sebelumnya.
   </Warning>

   Escaping string JSON dalam parameter alat mungkin berbeda dari model sebelumnya. Parser JSON standar menangani ini secara otomatis, tetapi parsing berbasis string kustom mungkin memerlukan pembaruan.

#### Saat bermigrasi dari Claude 3.x

3. **Perbarui parameter sampling**

   <Warning>
     Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

4. **Perbarui versi alat**

   <Warning>
     Ini adalah perubahan yang merusak saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20260521`). Hapus semua kode yang menggunakan perintah `undo_edit`.

5. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Perubahan yang direkomendasikan

1. **Hapus header beta `fine-grained-tool-streaming-2025-05-14`:** Fine-grained tool streaming sekarang GA pada Sonnet 4.6 dan tidak lagi memerlukan header beta.
2. **Migrasi `output_format` ke `output_config.format`:** Parameter `output_format` sudah usang. Gunakan `output_config.format` sebagai gantinya.

### Migrasi dari Sonnet 4.5

Pertimbangkan untuk bermigrasi dari Sonnet 4.5 ke Sonnet 4.6, yang memberikan kecerdasan lebih tinggi dengan harga yang sama.

<Warning>
  Sonnet 4.6 secara default menggunakan tingkat effort `high`, berbeda dengan Sonnet 4.5 yang tidak memiliki parameter effort. Pertimbangkan untuk menyesuaikan parameter effort saat Anda bermigrasi dari Sonnet 4.5 ke Sonnet 4.6. Jika tidak diatur secara eksplisit, Anda mungkin mengalami latensi yang lebih tinggi dengan tingkat effort default.
</Warning>

#### Jika Anda tidak menggunakan extended thinking

Jika Anda tidak menggunakan "extended thinking" (pemikiran diperpanjang) pada Sonnet 4.5, Anda dapat melanjutkan tanpa fitur tersebut pada Sonnet 4.6. Anda sebaiknya secara eksplisit mengatur effort ke tingkat yang sesuai untuk kasus penggunaan Anda. Pada effort `low` dengan thinking dinonaktifkan, Anda dapat mengharapkan performa yang serupa atau lebih baik dibandingkan Sonnet 4.5 tanpa pemikiran diperpanjang.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
       --header "x-api-key: $ANTHROPIC_API_KEY" \
       --header "anthropic-version: 2023-06-01" \
       --header "content-type: application/json" \
       --data \
  '{
      "model": "claude-sonnet-4-6",
      "max_tokens": 8192,
      "output_config": {
          "effort": "low"
      },
      "messages": [
          {
              "role": "user",
              "content": "Your prompt here"
          }
      ]
  }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-sonnet-4-6
  max_tokens: 8192
  output_config:
    effort: low
  messages:
    - role: user
      content: Your prompt here
  YAML
  ```

  ```python Python
  response = client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=8192,
      output_config={"effort": "low"},
      messages=[{"role": "user", "content": "Your prompt here"}],
  )
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 8192,
    output_config: { effort: "low" },
    messages: [{ role: "user", content: "Your prompt here" }]
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeSonnet4_6,
      MaxTokens = 8192,
      OutputConfig = new OutputConfig
      {
          Effort = Effort.Low
      },
      Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
  };
  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.Model("claude-sonnet-4-6"),
  	MaxTokens: 8192,
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortLow,
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Your prompt here")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.Content[0].Text)
  ```

  ```java Java
  import com.anthropic.models.messages.OutputConfig;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_4_6)
              .maxTokens(8192L)
              .outputConfig(OutputConfig.builder()
                  .effort(OutputConfig.Effort.LOW)
                  .build())
              .addUserMessage("Your prompt here")
              .build();

          Message response = client.messages().create(params);
          response.content().stream()
              .flatMap(block -> block.text().stream())
              .forEach(textBlock -> System.out.println(textBlock.text()));
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 8192,
      messages: [['role' => 'user', 'content' => 'Your prompt here']],
      model: 'claude-sonnet-4-6',
      outputConfig: ['effort' => 'low'],
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 8192,
    output_config: {
      effort: "low"
    },
    messages: [
      { role: "user", content: "Your prompt here" }
    ]
  )
  puts message.content.first.text
  ```
</CodeGroup>

#### Jika Anda menggunakan extended thinking

Jika Anda menggunakan pemikiran diperpanjang dengan `budget_tokens` pada Sonnet 4.5, fitur ini masih berfungsi pada Sonnet 4.6 tetapi sudah usang (deprecated). Bermigrasilah ke [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) dengan [parameter effort](/docs/id/build-with-claude/effort).

##### Bermigrasi ke adaptive thinking

[Adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) adalah pengganti yang direkomendasikan untuk `budget_tokens` pada Sonnet 4.6. Fitur ini sangat cocok untuk pola beban kerja berikut:

* **Agen multi-langkah otonom:** agen coding yang mengubah kebutuhan menjadi perangkat lunak yang berfungsi, pipeline analisis data, dan pencarian bug di mana model berjalan secara independen melalui banyak langkah. Adaptive thinking memungkinkan model mengkalibrasi penalarannya per langkah, tetap berada di jalur yang benar selama lintasan yang lebih panjang. Untuk beban kerja ini, mulailah dengan effort `high`. Jika latensi atau penggunaan token menjadi perhatian, turunkan ke `medium`.
* **Agen computer use:** Sonnet 4.6 mencapai akurasi terbaik di kelasnya pada evaluasi computer use menggunakan mode adaptif.
* **Beban kerja bimodal:** campuran tugas mudah dan sulit di mana mode adaptif melewati thinking pada kueri sederhana dan bernalar secara mendalam pada kueri yang kompleks.

Saat menggunakan adaptive thinking, evaluasi effort `medium` dan `high` pada tugas Anda. Tingkat yang tepat bergantung pada trade-off beban kerja Anda antara kualitas, latensi, dan penggunaan token.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
       --header "x-api-key: $ANTHROPIC_API_KEY" \
       --header "anthropic-version: 2023-06-01" \
       --header "content-type: application/json" \
       --data \
  '{
      "model": "claude-sonnet-4-6",
      "max_tokens": 64000,
      "thinking": {
          "type": "adaptive"
      },
      "output_config": {
          "effort": "medium"
      },
      "messages": [
          {
              "role": "user",
              "content": "Your prompt here"
          }
      ]
  }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-sonnet-4-6
  max_tokens: 64000
  thinking:
    type: adaptive
  output_config:
    effort: medium
  messages:
    - role: user
      content: Your prompt here
  YAML
  ```

  ```python Python
  response = client.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=64000,
      thinking={"type": "adaptive"},
      output_config={"effort": "medium"},
      messages=[{"role": "user", "content": "Your prompt here"}],
  )
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 64000,
    thinking: { type: "adaptive" },
    output_config: { effort: "medium" },
    messages: [{ role: "user", content: "Your prompt here" }]
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeSonnet4_6,
      MaxTokens = 64000,
      Thinking = new ThinkingConfigAdaptive(),
      OutputConfig = new OutputConfig { Effort = Effort.Medium },
      Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     "claude-sonnet-4-6",
  	MaxTokens: 64000,
  	Thinking: anthropic.ThinkingConfigParamUnion{
  		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
  	},
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortMedium,
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
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_4_6)
              .maxTokens(64000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
              .outputConfig(OutputConfig.builder()
                  .effort(OutputConfig.Effort.MEDIUM)
                  .build())
              .addUserMessage("Your prompt here")
              .build();

          Message response = client.messages().create(params);
          System.out.println(response);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 64000,
      messages: [['role' => 'user', 'content' => 'Your prompt here']],
      model: 'claude-sonnet-4-6',
      thinking: ['type' => 'adaptive'],
      outputConfig: ['effort' => 'medium'],
  );

  echo array_find($message->content, fn($block) => $block->type === 'text')->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 64000,
    thinking: {
      type: "adaptive"
    },
    output_config: {
      effort: "medium"
    },
    messages: [
      { role: "user", content: "Your prompt here" }
    ]
  )
  puts message.content.find { |block| block.type == :text }.text
  ```
</CodeGroup>

<Note>
  Jika Anda melihat perilaku yang tidak konsisten atau penurunan kualitas dengan adaptive thinking, coba turunkan pengaturan [effort](/docs/id/build-with-claude/effort) atau gunakan `max_tokens` sebagai batas keras terlebih dahulu. Pemikiran diperpanjang dengan `budget_tokens` masih berfungsi pada Sonnet 4.6 tetapi sudah usang dan tidak lagi direkomendasikan.
</Note>

##### Mempertahankan budget\_tokens selama migrasi

Jika Anda perlu mempertahankan `budget_tokens` sementara selama migrasi, budget sekitar 16k token memberikan ruang untuk masalah yang lebih sulit tanpa risiko penggunaan token yang tidak terkendali. Konfigurasi ini sudah usang dan akan dihapus pada rilis model mendatang.

###### Kasus penggunaan coding dan agentik

Untuk agentic coding, desain frontend, alur kerja yang banyak menggunakan alat, dan alur kerja enterprise yang kompleks, mulailah dengan effort `medium`. Jika Anda merasa latensi terlalu tinggi, pertimbangkan untuk menurunkan effort ke `low`. Jika Anda membutuhkan kecerdasan yang lebih tinggi, pertimbangkan untuk meningkatkan effort ke `high` atau bermigrasi ke Opus 4.7.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
       --header "x-api-key: $ANTHROPIC_API_KEY" \
       --header "anthropic-version: 2023-06-01" \
       --header "anthropic-beta: interleaved-thinking-2025-05-14" \
       --header "content-type: application/json" \
       --data \
  '{
      "model": "claude-sonnet-4-6",
      "max_tokens": 16384,
      "thinking": {
          "type": "enabled",
          "budget_tokens": 16384
      },
      "output_config": {
          "effort": "medium"
      },
      "messages": [
          {
              "role": "user",
              "content": "Your prompt here"
          }
      ]
  }'
  ```

  ```bash CLI
  ant beta:messages create --beta interleaved-thinking-2025-05-14 <<'YAML'
  model: claude-sonnet-4-6
  max_tokens: 16384
  thinking:
    type: enabled
    budget_tokens: 16384
  output_config:
    effort: medium
  messages:
    - role: user
      content: Your prompt here
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=16384,
      thinking={"type": "enabled", "budget_tokens": 16384},
      output_config={"effort": "medium"},
      betas=["interleaved-thinking-2025-05-14"],
      messages=[{"role": "user", "content": "Your prompt here"}],
  )
  ```

  ```typescript TypeScript
  const response = await client.beta.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 16384,
    thinking: { type: "enabled", budget_tokens: 16384 },
    output_config: { effort: "medium" },
    betas: ["interleaved-thinking-2025-05-14"],
    messages: [{ role: "user", content: "Your prompt here" }]
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = "claude-sonnet-4-6",
      MaxTokens = 16384,
      Thinking = new BetaThinkingConfigEnabled { BudgetTokens = 16384 },
      OutputConfig = new BetaOutputConfig
      {
          Effort = Effort.Medium
      },
      Betas = [AnthropicBeta.InterleavedThinking2025_05_14],
      Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
  };

  var message = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-sonnet-4-6",
  	MaxTokens: 16384,
  	Thinking:  anthropic.BetaThinkingConfigParamOfEnabled(16384),
  	OutputConfig: anthropic.BetaOutputConfigParam{
  		Effort: anthropic.BetaOutputConfigEffortMedium,
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Your prompt here")),
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaInterleavedThinking2025_05_14},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaThinkingConfigEnabled;
  import com.anthropic.models.beta.messages.BetaOutputConfig;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_4_6)
              .maxTokens(16384L)
              .thinking(BetaThinkingConfigEnabled.builder()
                  .budgetTokens(16384L)
                  .build())
              .outputConfig(BetaOutputConfig.builder()
                  .effort(BetaOutputConfig.Effort.MEDIUM)
                  .build())
              .addBeta(AnthropicBeta.INTERLEAVED_THINKING_2025_05_14)
              .addUserMessage("Your prompt here")
              .build();

          BetaMessage response = client.beta().messages().create(params);
          System.out.println(response);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 16384,
      messages: [['role' => 'user', 'content' => 'Your prompt here']],
      model: 'claude-sonnet-4-6',
      thinking: ['type' => 'enabled', 'budget_tokens' => 16384],
      outputConfig: ['effort' => 'medium'],
      betas: ['interleaved-thinking-2025-05-14'],
  );

  echo array_find($message->content, fn($block) => $block->type === 'text')->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.beta.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 16384,
    thinking: {
      type: "enabled",
      budget_tokens: 16384
    },
    output_config: {
      effort: "medium"
    },
    betas: ["interleaved-thinking-2025-05-14"],
    messages: [
      { role: "user", content: "Your prompt here" }
    ]
  )
  puts message.content.find { |block| block.type == :text }.text
  ```
</CodeGroup>

###### Kasus penggunaan chat dan non-coding

Untuk chat, pembuatan konten, pencarian, klasifikasi, dan tugas non-coding lainnya, mulailah dengan effort `low` dengan pemikiran diperpanjang. Jika Anda membutuhkan kedalaman lebih, tingkatkan effort ke `medium`.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
       --header "x-api-key: $ANTHROPIC_API_KEY" \
       --header "anthropic-version: 2023-06-01" \
       --header "anthropic-beta: interleaved-thinking-2025-05-14" \
       --header "content-type: application/json" \
       --data \
  '{
      "model": "claude-sonnet-4-6",
      "max_tokens": 8192,
      "thinking": {
          "type": "enabled",
          "budget_tokens": 16384
      },
      "output_config": {
          "effort": "low"
      },
      "messages": [
          {
              "role": "user",
              "content": "Your prompt here"
          }
      ]
  }'
  ```

  ```bash CLI
  ant beta:messages create --beta interleaved-thinking-2025-05-14 <<'YAML'
  model: claude-sonnet-4-6
  max_tokens: 8192
  thinking:
    type: enabled
    budget_tokens: 16384
  output_config:
    effort: low
  messages:
    - role: user
      content: Your prompt here
  YAML
  ```

  ```python Python
  response = client.beta.messages.create(
      model="claude-sonnet-4-6",
      max_tokens=8192,
      thinking={"type": "enabled", "budget_tokens": 16384},
      output_config={"effort": "low"},
      betas=["interleaved-thinking-2025-05-14"],
      messages=[{"role": "user", "content": "Your prompt here"}],
  )
  ```

  ```typescript TypeScript
  const response = await client.beta.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 8192,
    thinking: { type: "enabled", budget_tokens: 16384 },
    output_config: { effort: "low" },
    betas: ["interleaved-thinking-2025-05-14"],
    messages: [{ role: "user", content: "Your prompt here" }]
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Beta;
  using Anthropic.Models.Beta.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = "claude-sonnet-4-6",
      MaxTokens = 8192,
      Thinking = new BetaThinkingConfigEnabled { BudgetTokens = 16384 },
      OutputConfig = new BetaOutputConfig
      {
          Effort = Effort.Low
      },
      Betas = [AnthropicBeta.InterleavedThinking2025_05_14],
      Messages = [new() { Role = Role.User, Content = "Your prompt here" }]
  };

  var message = await client.Beta.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     "claude-sonnet-4-6",
  	MaxTokens: 8192,
  	Thinking:  anthropic.BetaThinkingConfigParamOfEnabled(16384),
  	OutputConfig: anthropic.BetaOutputConfigParam{
  		Effort: anthropic.BetaOutputConfigEffortLow,
  	},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Your prompt here")),
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaInterleavedThinking2025_05_14},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaThinkingConfigEnabled;
  import com.anthropic.models.beta.messages.BetaOutputConfig;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_4_6)
              .maxTokens(8192L)
              .thinking(BetaThinkingConfigEnabled.builder()
                  .budgetTokens(16384L)
                  .build())
              .outputConfig(BetaOutputConfig.builder()
                  .effort(BetaOutputConfig.Effort.LOW)
                  .build())
              .addBeta(AnthropicBeta.INTERLEAVED_THINKING_2025_05_14)
              .addUserMessage("Your prompt here")
              .build();

          BetaMessage response = client.beta().messages().create(params);
          System.out.println(response);
  ```

  ```php PHP
  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 8192,
      messages: [['role' => 'user', 'content' => 'Your prompt here']],
      model: 'claude-sonnet-4-6',
      thinking: ['type' => 'enabled', 'budget_tokens' => 16384],
      outputConfig: ['effort' => 'low'],
      betas: ['interleaved-thinking-2025-05-14'],
  );

  echo array_find($message->content, fn($block) => $block->type === 'text')->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.beta.messages.create(
    model: "claude-sonnet-4-6",
    max_tokens: 8192,
    thinking: {
      type: "enabled",
      budget_tokens: 16384
    },
    output_config: {
      effort: "low"
    },
    betas: ["interleaved-thinking-2025-05-14"],
    messages: [
      { role: "user", content: "Your prompt here" }
    ]
  )
  puts message.content.find { |block| block.type == :text }.text
  ```
</CodeGroup>

### Daftar periksa migrasi Sonnet 4.6

* Perbarui ID model ke `claude-sonnet-4-6`
* **BREAKING:** Hapus prefilling pesan assistant; gunakan structured outputs atau `output_config.format` sebagai gantinya
* **BREAKING:** Verifikasi bahwa parsing JSON parameter alat menangani perbedaan escaping
* **BREAKING:** Perbarui versi alat ke yang terbaru (`text_editor_20250728`, `code_execution_20260521`); versi lama tidak didukung (jika bermigrasi dari 3.x)
* **BREAKING:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
* **BREAKING:** Perbarui parameter sampling untuk hanya menggunakan `temperature` ATAU `top_p`, bukan keduanya (jika bermigrasi dari 3.x)
* Tangani stop reason `refusal` yang baru di aplikasi Anda
* Hapus header beta `fine-grained-tool-streaming-2025-05-14` (sekarang sudah GA)
* Migrasikan `output_format` ke `output_config.format`
* Tinjau dan perbarui prompt dengan mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
* **Direkomendasikan:** Bermigrasi dari `thinking: {type: "enabled", budget_tokens: N}` ke `thinking: {type: "adaptive"}` dengan [parameter effort](/docs/id/build-with-claude/effort) (`budget_tokens` sudah usang dan akan dihapus pada rilis mendatang)
* Uji di lingkungan pengembangan sebelum deployment ke produksi

***

## Bermigrasi ke Claude Sonnet 4.5

Claude Sonnet 4.5 menggabungkan kecerdasan yang kuat dengan performa yang cepat, menjadikannya ideal untuk tugas coding, analisis, dan konten sehari-hari.

Untuk gambaran lengkap tentang kemampuannya, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

<Note>
  Harga Sonnet 4.5 adalah $3 per juta token input, $15 per juta token output. Lihat [harga Claude](/docs/id/about-claude/pricing) untuk detailnya.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Before
model = "claude-sonnet-4-5-20250929"  # After
```

### Breaking changes

Breaking changes ini berlaku saat bermigrasi dari model Claude 3.x Sonnet.

1. **Perbarui parameter sampling**

   <Warning>
     Ini adalah breaking change saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

2. **Perbarui versi alat**

   <Warning>
     Ini adalah breaking change saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20260521`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

3. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Daftar periksa migrasi Sonnet 4.5

* Perbarui ID model ke `claude-sonnet-4-5-20250929`
* **BREAKING:** Perbarui versi alat ke yang terbaru (`text_editor_20250728`, `code_execution_20260521`); versi lama tidak didukung (jika bermigrasi dari 3.x)
* **BREAKING:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
* **BREAKING:** Perbarui parameter sampling untuk hanya menggunakan `temperature` ATAU `top_p`, bukan keduanya (jika bermigrasi dari 3.x)
* Tangani stop reason `refusal` yang baru di aplikasi Anda
* Tinjau dan perbarui prompt dengan mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
* Pertimbangkan untuk mengaktifkan pemikiran diperpanjang untuk tugas penalaran yang kompleks
* Uji di lingkungan pengembangan sebelum deployment ke produksi

***

## Bermigrasi ke Claude Haiku 4.5

Claude Haiku 4.5 adalah model Haiku tercepat dan paling cerdas dengan performa mendekati frontier, memberikan kualitas model premium untuk aplikasi interaktif dan pemrosesan volume tinggi.

Untuk gambaran lengkap tentang kemampuannya, lihat [ikhtisar model](/docs/id/about-claude/models/overview).

<Note>
  Harga Haiku 4.5 adalah $1 per juta token input, $5 per juta token output. Lihat [harga Claude](/docs/id/about-claude/pricing) untuk detailnya.
</Note>

**Perbarui nama model Anda:**

```python
# Dari Haiku 3.5
model = "claude-3-5-haiku-20241022"  # Before
model = "claude-haiku-4-5-20251001"  # After
```

**Tinjau batas laju baru:** Haiku 4.5 memiliki "rate limit" (batas laju) yang terpisah dari Haiku 3.5. Lihat [dokumentasi batas laju](/docs/id/api/rate-limits) untuk detailnya.

<Tip>
  Untuk peningkatan performa yang signifikan pada tugas coding dan penalaran, pertimbangkan untuk mengaktifkan pemikiran diperpanjang dengan `thinking: {type: "enabled", budget_tokens: N}`.
</Tip>

<Note>
  Pemikiran diperpanjang memengaruhi efisiensi [caching prompt](/docs/id/build-with-claude/prompt-caching#caching-with-thinking-blocks).

  Pemikiran diperpanjang sudah usang pada model Claude 4.6 dan dihapus pada Claude Opus 4.7. Jika menggunakan model yang lebih baru, gunakan [adaptive thinking](/docs/id/build-with-claude/adaptive-thinking) sebagai gantinya.
</Note>

**Jelajahi kemampuan baru:** Lihat [ikhtisar model](/docs/id/about-claude/models/overview) untuk detail tentang kesadaran konteks, kapasitas output yang meningkat (64k token), kecerdasan yang lebih tinggi, dan kecepatan yang lebih baik.

### Breaking changes

Breaking changes ini berlaku saat bermigrasi dari model Claude 3.x Haiku.

1. **Perbarui parameter sampling**

   <Warning>
     Ini adalah breaking change saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, bukan keduanya.

2. **Perbarui versi alat**

   <Warning>
     Ini adalah breaking change saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

3. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Daftar periksa migrasi Haiku 4.5

* Perbarui ID model ke `claude-haiku-4-5-20251001`
* **BREAKING:** Perbarui versi alat ke yang terbaru (`text_editor_20250728`, `code_execution_20250825`); versi lama tidak didukung
* **BREAKING:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
* **BREAKING:** Perbarui parameter sampling untuk hanya menggunakan `temperature` ATAU `top_p`, bukan keduanya
* Tangani stop reason `refusal` yang baru di aplikasi Anda
* Tinjau dan sesuaikan dengan batas laju baru (terpisah dari Haiku 3.5)
* Tinjau dan perbarui prompt dengan mengikuti [praktik terbaik prompting](/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
* Pertimbangkan untuk mengaktifkan pemikiran diperpanjang untuk tugas penalaran yang kompleks
* Uji di lingkungan pengembangan sebelum deployment ke produksi

***

## Dapatkan bantuan

* Periksa [dokumentasi API](/docs/id/api/overview) untuk spesifikasi terperinci
* Tinjau [kemampuan model](/docs/id/about-claude/models/overview) untuk perbandingan performa
* Tinjau [catatan rilis API](/docs/id/release-notes/api) untuk pembaruan API
* Hubungi dukungan jika Anda mengalami masalah selama migrasi
