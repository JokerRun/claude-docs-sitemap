---
source: platform
url: https://platform.claude.com/docs/id/about-claude/models/migration-guide
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 201c64b355e7487f821dded2fffa0e58e2c4453ebff20314ebd9187d3ab6f68d
---

---
title: Panduan migrasi
url: https://platform.claude.com/docs/id/about-claude/models/migration-guide
description: Panduan untuk bermigrasi ke model Claude terbaru dari versi Claude sebelumnya
---

<Note>
  Panduan ini mencakup migrasi kode [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak ada perubahan yang diperlukan selain memperbarui nama model.
</Note>

<Tip>
  **Otomatiskan migrasi Anda dengan skill Claude API.** Di Claude Code, jalankan `/claude-api migrate` untuk memanggil [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model) bawaan. Skill ini berfungsi untuk model target apa pun di halaman ini:

  ```text wrap
  /claude-api migrate this project to claude-opus-5
  ```

  Skill ini menerapkan penggantian ID model dan, sesuai kebutuhan, perubahan parameter yang bersifat breaking, penggantian prefill, serta kalibrasi effort untuk model target Anda di seluruh basis kode, lalu menghasilkan daftar periksa berisi item yang perlu diverifikasi secara manual. Skill ini meminta Anda mengonfirmasi cakupan migrasi (seluruh direktori kerja, sebuah subdirektori, atau daftar file tertentu) sebelum mengedit file apa pun. Skill ini juga mendeteksi klien Amazon Bedrock dan Claude Platform on AWS serta menyesuaikan format ID model dan perubahan fitur untuk platform tersebut.
</Tip>

## Bermigrasi ke Claude Mythos 5 dan Claude Fable 5

[Claude Fable 5](https://platform.claude.com/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) adalah model Anthropic paling mumpuni yang dirilis secara luas, tersedia di Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). [Claude Mythos 5](https://anthropic.com/glasswing) memiliki kemampuan yang sama dan hanya ditawarkan kepada pelanggan yang disetujui dalam Project Glasswing.

Pengaturan dasar yang dimiliki bersama oleh `claude-fable-5` dan `claude-mythos-5`:

* **Thinking:** ["Adaptive thinking" (pemikiran adaptif)](https://platform.claude.com/docs/id/build-with-claude/thinking) selalu aktif. Model menentukan kapan dan seberapa banyak berpikir pada setiap permintaan, dan tidak diperlukan konfigurasi `thinking`. Baik `thinking: {type: "disabled"}` maupun "extended thinking" (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) mengembalikan error 400.
* **Prefill:** Melakukan "prefill" (pengisian awal) pada pesan asisten mengembalikan error 400. Gunakan instruksi "system prompt" (prompt sistem) sebagai gantinya.
* **Jendela konteks dan output:** ["Context window" (jendela konteks) 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, dan hingga 128k token output per permintaan.
* **Harga:** $10 USD per juta token input dan $50 USD per juta token output. Lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).
* **Retensi data:** Kedua model memerlukan retensi data 30 hari dan tidak tersedia di bawah pengaturan "zero data retention" (retensi data nol), atau ZDR; keduanya ditetapkan sebagai Covered Models. Di Claude API, permintaan ke Claude Fable 5 dari organisasi yang konfigurasi retensi datanya tidak memenuhi persyaratan ini mengembalikan `invalid_request_error` 400. Organisasi dengan pengaturan ZDR sebaiknya menghubungi tim akun Anthropic mereka untuk mendiskusikan konfigurasi retensi data. Sebagai alternatif, Anda dapat mengonfigurasi retensi data per workspace. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements) untuk detail per platform.

Perbedaan antara kedua model:

* **Ketersediaan:** Claude Fable 5 tidak memerlukan persetujuan akses. Claude Mythos 5 hanya tersedia bagi pelanggan yang disetujui dalam [Project Glasswing](https://anthropic.com/glasswing).
* **Pengklasifikasi keamanan:** Claude Fable 5 menjalankan pengklasifikasi keamanan yang dapat menolak permintaan dengan `stop_reason: "refusal"`. Claude Mythos 5 tidak menyertakan pengklasifikasi ini. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).
* **Priority Tier:** [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) didukung di Claude Fable 5 tetapi tidak di Claude Mythos 5.

### Bermigrasi ke Claude Mythos 5 dan Claude Fable 5 dari Claude Mythos Preview

[Claude Mythos 5](https://anthropic.com/glasswing) adalah penerus dengan akses terbatas dari [Claude Mythos Preview](https://anthropic.com/glasswing), pratinjau riset khusus undangan. [Claude Fable 5](https://platform.claude.com/docs/id/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) menawarkan kemampuan yang sama dan tidak memerlukan persetujuan akses. Perubahan di bagian ini berlaku sama untuk kedua target.

Migrasi sebagian besar bersifat drop-in. Claude Mythos 5 dan Claude Fable 5 menggunakan [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) yang sama dan pola ["tool use" (penggunaan alat)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) yang sama dengan Claude Mythos Preview, dan jumlah token kurang lebih tidak berubah karena ketiga model menggunakan tokenizer yang sama. Perubahan utama yang perlu diperiksa adalah fitur yang tidak lagi tersedia (tercantum di bagian berikutnya) dan output thinking. Jika Anda bermigrasi ke Claude Fable 5, rencanakan juga penanganan penolakan dari pengklasifikasi keamanan, yang tidak dimiliki Claude Mythos Preview dan Claude Mythos 5; lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

Untuk jadwal penghentian Claude Mythos Preview, lihat [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

#### Perbarui nama model Anda

```python
model = "claude-mythos-preview"  # Before
model = "claude-mythos-5"  # After

# Atau, untuk model dengan kemampuan yang sama dan tanpa persyaratan persetujuan akses:
model = "claude-fable-5"  # After
```

#### Fitur yang tidak tersedia di Claude Mythos 5 dan Claude Fable 5

1. **Pemikiran diperpanjang dan anggaran token thinking:** Pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung di `claude-mythos-5` atau `claude-fable-5` dan mengembalikan error 400. [Pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking) selalu aktif: model menentukan kapan dan seberapa banyak berpikir pada setiap permintaan, dan tidak diperlukan konfigurasi `thinking`. `thinking: {type: "disabled"}` mengembalikan error. `budget_tokens` tidak memiliki pengganti langsung: thinking bersifat adaptif, dan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) adalah kontrol tingkat output yang terpisah, bukan anggaran thinking.

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

   Perubahan untuk Claude Fable 5 identik, dengan `claude-fable-5` sebagai nama model.

2. **Prefill asisten:** Melakukan prefill pada pesan asisten tidak didukung di `claude-mythos-5` atau `claude-fable-5` dan mengembalikan error 400, sama seperti di Claude Mythos Preview. Gunakan instruksi prompt sistem sebagai gantinya.

3. **Output thinking:** Di `claude-mythos-5` dan `claude-fable-5`, rantai pemikiran mentah tidak pernah dikembalikan, tetapi blok thinking tetap membawa teks ringkasan yang dapat dibaca ketika `thinking.display` diatur ke `summarized`. Kirimkan kembali blok thinking tanpa perubahan saat melanjutkan percakapan pada model yang sama. Lihat [Output thinking di Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).

#### Penghitungan token dan penagihan

`claude-mythos-5` dan `claude-fable-5` menggunakan tokenizer yang sama dengan `claude-mythos-preview` (tokenizer yang diperkenalkan bersama Claude Opus 4.7). Jumlah token kurang lebih tidak berubah saat bermigrasi dari `claude-mythos-preview`. Dibandingkan dengan model sebelum Claude Opus 4.7, konten yang sama dapat ditokenisasi menjadi kurang lebih 30% lebih banyak token, bervariasi menurut konten dan bentuk beban kerja.

[`/v1/messages/count_tokens`](https://platform.claude.com/docs/id/build-with-claude/token-counting) mengembalikan nilai yang kurang lebih tidak berubah untuk `claude-mythos-5` dan `claude-fable-5` dibandingkan dengan `claude-mythos-preview`. Tetapkan ulang baseline biaya dan latensi pada beban kerja Anda sendiri.

#### Daftar periksa migrasi

* Perbarui nama model dari `claude-mythos-preview` ke `claude-mythos-5`, atau ke `claude-fable-5`, yang menawarkan kemampuan yang sama dan tidak memerlukan persetujuan akses.
* Hapus konfigurasi pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`). Pemikiran adaptif selalu aktif, dan tidak diperlukan field `thinking`.
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun. Menonaktifkan thinking mengembalikan error di `claude-mythos-5` dan `claude-fable-5`.
* Hapus `budget_tokens`. Parameter ini tidak memiliki pengganti langsung: thinking bersifat adaptif, dan parameter `effort` adalah kontrol tingkat output yang terpisah, bukan anggaran thinking.
* Verifikasi bahwa kode apa pun yang mengurai field `thinking` memperlakukannya hanya sebagai teks tampilan dan mengirimkan kembali blok thinking tanpa perubahan saat melanjutkan pada model yang sama. `thinking.display` secara default bernilai `"omitted"` di `claude-mythos-5` dan `claude-fable-5`, sama seperti di Claude Mythos Preview; atur `display: "summarized"` untuk menerima ringkasan yang dapat dibaca. Lihat [Output thinking di Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).
* Jika Anda memutar ulang riwayat percakapan pada model lain, hapus terlebih dahulu blok `thinking` dan `redacted_thinking` dari giliran asisten sebelumnya. Blok thinking dari `claude-mythos-5` dan `claude-fable-5` terikat pada model yang menghasilkannya, dan model selain Claude Fable 5 dan Claude Mythos 5 mengabaikannya secara diam-diam. Penghapusan ini menjaga permintaan lintas model tetap minimal dan seragam.
* Jika Anda bermigrasi ke Claude Fable 5, tangani `stop_reason: "refusal"` dan baca field `stop_details.category`. Claude Fable 5 menjalankan pengklasifikasi keamanan yang tidak dimiliki Claude Mythos Preview dan Claude Mythos 5. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).
* Tetapkan ulang baseline jumlah token dan biaya pada beban kerja Anda sendiri. Jumlah token kurang lebih tidak berubah saat bermigrasi dari `claude-mythos-preview`.

### Bermigrasi ke Claude Mythos 5 dan Claude Fable 5 dari Claude Opus 5

Claude Fable 5 dan Claude Mythos 5 menggunakan [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) yang sama dan pola [penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) yang sama dengan Claude Opus 5, dengan [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) yang sama secara default dan [token output maksimum 128k](https://platform.claude.com/docs/id/about-claude/models/overview) yang sama. Pembatasan prefill dan parameter sampling, serta perilaku tampilan thinking, terbawa dari Claude Opus 5 tanpa perubahan. Perubahan yang perlu diperiksa adalah thinking yang selalu aktif, harga, Priority Tier, dan retensi data.

#### Perbarui nama model Anda

```python
model = "claude-opus-5"  # Before
model = "claude-fable-5"  # After

# Atau, untuk model Project Glasswing dengan kemampuan yang sama:
model = "claude-mythos-5"  # After
```

#### Apa yang berubah

1. **Thinking tidak dapat lagi dinonaktifkan:** Di Claude Opus 5, thinking aktif secara default dan dapat dimatikan dengan `thinking: {type: "disabled"}` pada tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah. Di `claude-fable-5` dan `claude-mythos-5`, [pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking) selalu aktif, dan `thinking: {type: "disabled"}` mengembalikan error 400 pada tingkat effort apa pun. Hapus konfigurasi `thinking: {type: "disabled"}` dan gunakan tingkat effort yang lebih rendah untuk mengendalikan pengeluaran token sebagai gantinya.

2. **Harga:** Claude Fable 5 dan Claude Mythos 5 dihargai $10 USD per juta token input dan $50 USD per juta token output, dibandingkan dengan $5 USD dan $25 USD untuk Claude Opus 5. Lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).

3. **Priority Tier:** [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) tidak didukung di Claude Opus 5, sehingga tidak ada lalu lintas yang ada yang terpengaruh. Jika organisasi Anda memiliki komitmen Priority Tier, Claude Fable 5 mendukungnya; Claude Mythos 5 tidak.

4. **Retensi data:** Claude Fable 5 dan Claude Mythos 5 memerlukan retensi data 30 hari dan tidak tersedia di bawah pengaturan zero data retention (ZDR); keduanya ditetapkan sebagai Covered Models. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).

#### Daftar periksa migrasi

* Perbarui nama model dari `claude-opus-5` ke `claude-fable-5` (atau `claude-mythos-5`).
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun; konfigurasi ini mengembalikan error 400 di `claude-fable-5` dan `claude-mythos-5`. Gunakan tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang lebih rendah untuk mengendalikan pengeluaran token sebagai gantinya, dan tinjau kembali `max_tokens` untuk beban kerja yang berjalan dengan thinking dinonaktifkan di Claude Opus 5.
* Jika organisasi Anda memiliki pengaturan zero data retention (ZDR), konfirmasikan kelayakan sebelum bermigrasi. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Tetapkan ulang baseline biaya pada beban kerja Anda sendiri. Jumlah token kurang lebih tidak berubah; harga per token berbeda.

### Bermigrasi ke Claude Mythos 5 dan Claude Fable 5 dari Claude Opus 4.8

<Note>
  Jika kode Anda menggunakan Claude Opus 4.7 atau lebih lama, terapkan terlebih dahulu bagian asal yang relevan dari [Bermigrasi ke Claude Opus 5](https://platform.claude.com/docs/id/about-claude/models/migration-guide#migrating-to-claude-opus-5) untuk perubahan tingkat API dari model Anda saat ini, lalu delta yang tersisa di bagian ini.
</Note>

Migrasi sebagian besar bersifat drop-in. Claude Fable 5 dan Claude Mythos 5 menggunakan [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) yang sama dan pola [penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) yang sama dengan Claude Opus 4.8, dengan [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) yang sama secara default dan [token output maksimum 128k](https://platform.claude.com/docs/id/about-claude/models/overview) yang sama. Jumlah token kurang lebih tidak berubah karena model-model ini menggunakan tokenizer yang sama. Perubahan utama yang perlu diperiksa adalah [pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking) yang selalu aktif, output thinking, penolakan dari pengklasifikasi keamanan (hanya Claude Fable 5), dan harga.

#### Perbarui nama model Anda

```python
model = "claude-opus-4-8"  # Before
model = "claude-fable-5"  # After

# Atau, untuk model Project Glasswing dengan kemampuan yang sama:
model = "claude-mythos-5"  # After
```

#### Apa yang berubah

Item di bagian ini menjelaskan perbedaan API dan perilaku yang perlu diperiksa setelah Anda mengganti ID model. Kecuali jika disebutkan lain, item ini berlaku sama untuk `claude-fable-5` dan `claude-mythos-5`.

1. **Pemikiran adaptif selalu aktif:** [Pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking) adalah satu-satunya mode thinking di `claude-fable-5` dan `claude-mythos-5`. Model menentukan kapan dan seberapa banyak berpikir pada setiap permintaan, dan tidak diperlukan konfigurasi `thinking`. `thinking: {type: "disabled"}` mengembalikan error. Gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengendalikan kedalaman thinking.

   Perubahan perilaku yang perlu diperiksa: di Claude Opus 4.8, permintaan tanpa field `thinking` berjalan tanpa thinking; di `claude-fable-5` dan `claude-mythos-5`, permintaan yang sama berjalan dengan pemikiran adaptif. `max_tokens` tetap menjadi batas keras pada total output, thinking ditambah teks respons, jadi tinjau kembali untuk beban kerja yang berjalan tanpa thinking di Claude Opus 4.8. Lihat [Kontrol biaya](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#cost-control).

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

   Perubahan untuk Claude Mythos 5 identik, dengan `claude-mythos-5` sebagai nama model.

2. **Pemikiran diperpanjang dan anggaran thinking (tidak berubah):** Pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung di `claude-fable-5` atau `claude-mythos-5` dan mengembalikan error 400, sama seperti di Claude Opus 4.8. `budget_tokens` tidak memiliki pengganti langsung: thinking bersifat adaptif, dan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) adalah kontrol tingkat output yang terpisah, bukan anggaran thinking.

3. **Prefill asisten (tidak berubah):** Melakukan prefill pada pesan asisten tidak didukung di `claude-fable-5` atau `claude-mythos-5` dan mengembalikan error 400, sama seperti di Claude Opus 4.8. Gunakan instruksi prompt sistem sebagai gantinya.

4. **Output thinking:** Di `claude-fable-5` dan `claude-mythos-5`, rantai pemikiran mentah tidak pernah dikembalikan, tetapi blok thinking tetap membawa teks ringkasan yang dapat dibaca ketika `thinking.display` diatur ke `summarized`. Kirimkan kembali blok thinking tanpa perubahan saat melanjutkan percakapan pada model yang sama. Lihat [Output thinking di Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).

5. **Pengklasifikasi keamanan dan stop reason `refusal` (hanya Claude Fable 5):** `claude-fable-5` menjalankan pengklasifikasi keamanan pada permintaan dan selama pembuatan respons. Claude Mythos 5 tidak menyertakan pengklasifikasi ini. Ketika pengklasifikasi menolak permintaan, Messages API mengembalikan `stop_reason: "refusal"` sebagai respons HTTP 200 yang berhasil, bukan error. Field `stop_details.category` melaporkan pengklasifikasi mana yang terpicu, dengan kategori seperti `"cyber"`, `"bio"`, dan `"reasoning_extraction"`, atau `null` ketika penolakan tidak terpetakan ke kategori bernama mana pun. Lihat [tabel kategori penolakan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk daftar lengkapnya.

   Anda tidak ditagih untuk token input dari permintaan yang ditolak sebelum output apa pun dihasilkan. Ketika pengklasifikasi terpicu di tengah streaming, input dan output yang sudah di-streaming ditagih; buang output parsial tersebut.

   Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, kirimkan parameter opt-in `fallbacks`, yang berstatus beta di Claude API. Parameter ini tidak tersedia di Message Batches API atau di Amazon Bedrock, Google Cloud, dan Microsoft Foundry; di ketiga platform tersebut, jalankan percobaan ulang di sisi klien atau gunakan middleware refusal-fallback SDK. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

6. **Mulai dari effort `high`:** Default [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) tetap `high`. Di Claude Opus 4.8, rekomendasi untuk pekerjaan coding dan otonomi tinggi adalah mengatur `xhigh` secara eksplisit. Di `claude-fable-5` dan `claude-mythos-5`, gunakan `high` sebagai default untuk sebagian besar tugas dan cadangkan `xhigh` untuk beban kerja yang paling sensitif terhadap kemampuan. Pengaturan effort yang lebih rendah tetap berkinerja baik dan sering melampaui kinerja `xhigh` pada model sebelumnya. Kurangi effort jika suatu tugas selesai tetapi memakan waktu lebih lama dari yang diperlukan. Lihat [Prompting Claude Fable 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5#consider-all-effort-levels).

7. **Minimum caching prompt yang lebih rendah:** Panjang prompt minimum yang dapat di-cache di `claude-fable-5` dan `claude-mythos-5` adalah 512 token, lebih rendah dari 1.024 token di Claude Opus 4.8. Prompt yang terlalu pendek untuk di-cache di Claude Opus 4.8 kini dapat membuat entri cache, tanpa perubahan kode yang diperlukan. Lihat ["Prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

#### Daftar periksa migrasi

* Jika organisasi Anda memiliki pengaturan zero data retention (ZDR), konfirmasikan kelayakan sebelum bermigrasi. `claude-fable-5` dan `claude-mythos-5` memerlukan retensi data 30 hari; di Claude API, permintaan ke `claude-fable-5` yang tidak memenuhi persyaratan ini mengembalikan `invalid_request_error` 400. Claude Opus 4.8 tetap tersedia di bawah ZDR. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Perbarui nama model dari `claude-opus-4-8` ke `claude-fable-5` (atau `claude-mythos-5`).
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun. Menonaktifkan thinking mengembalikan error di `claude-fable-5` dan `claude-mythos-5`, dan permintaan tanpa field `thinking` berjalan dengan pemikiran adaptif.
* Jika Anda telah menghapus pemikiran diperpanjang manual dan prefill asisten selama migrasi sebelumnya, tidak ada tindakan yang diperlukan: keduanya tetap tidak didukung di `claude-fable-5` dan `claude-mythos-5`.
* Verifikasi bahwa kode apa pun yang mengurai field `thinking` memperlakukannya hanya sebagai teks tampilan dan mengirimkan kembali blok thinking tanpa perubahan saat melanjutkan pada model yang sama. `thinking.display` secara default bernilai `"omitted"` di `claude-fable-5` dan `claude-mythos-5`, sama seperti di Claude Opus 4.8; atur `display: "summarized"` untuk menerima ringkasan yang dapat dibaca. Lihat [Output thinking di Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).
* Jika Anda memutar ulang riwayat percakapan pada model lain, hapus terlebih dahulu blok `thinking` dan `redacted_thinking` dari giliran asisten sebelumnya. Blok thinking dari `claude-fable-5` dan `claude-mythos-5` terikat pada model yang menghasilkannya, dan model selain Claude Fable 5 dan Claude Mythos 5 mengabaikannya secara diam-diam. Penghapusan ini menjaga permintaan lintas model tetap minimal dan seragam. Pengecualiannya adalah menebus [kredit fallback](https://platform.claude.com/docs/id/build-with-claude/fallback-credit), yang mengharuskan body permintaan digemakan kembali sesuai aturan persis fitur tersebut.
* Jika Anda bermigrasi ke Claude Fable 5, tangani `stop_reason: "refusal"` dan baca field `stop_details.category`. Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, pertimbangkan parameter opt-in `fallbacks` (beta). Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).
* Evaluasi ulang pengaturan `effort` Anda. Mulai dari `high` untuk sebagian besar tugas, termasuk beban kerja yang berjalan pada `xhigh` di Claude Opus 4.8.
* Tetapkan ulang baseline biaya dan latensi pada beban kerja Anda sendiri. Jumlah token kurang lebih tidak berubah saat bermigrasi dari `claude-opus-4-8`; harga per token berbeda.

## Bermigrasi ke Claude Opus 5

Claude Opus 5 adalah peningkatan besar dibandingkan Claude Opus 4.8, unggul dalam penalaran mendalam, tugas agentik dan berjangka panjang, serta penskalaan komputasi saat pengujian (test-time compute). Untuk perbedaan perilaku dan pola prompting khusus model, lihat [Prompting Claude Opus 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5).

Claude Opus 5 adalah peningkatan drop-in untuk Claude Opus 4.8 dengan harga yang sama yaitu $5 per juta token input dan $25 per juta token output; lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing). Ada dua perubahan breaking untuk kode yang sudah berjalan di Claude Opus 4.8, yang dibahas di bagian Perubahan breaking di bawah. Claude Opus 5 mendukung rangkaian fitur yang sama dengan Claude Opus 4.8, termasuk [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows) (default, tanpa header beta), [token output maksimum 128k](https://platform.claude.com/docs/id/about-claude/models/overview), [pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking), [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching), [pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing), [Files API](https://platform.claude.com/docs/id/build-with-claude/files), [dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support), [vision](https://platform.claude.com/docs/id/build-with-claude/vision), serta [alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien, dengan dua pengecualian: [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) tidak tersedia di Claude Opus 5, dan [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) tidak didukung di Claude Opus 5. Lihat setiap halaman alat untuk ketersediaan model.

### Bermigrasi ke Claude Opus 5 dari Claude Opus 4.8

<Note>
  Bagian ini hanya mencakup delta dari Claude Opus 4.8. Jika kode Anda menggunakan Claude Opus 4.7 atau lebih lama, gunakan bagian di bawah ini sebagai gantinya: [Bermigrasi ke Claude Opus 5 dari Claude Opus 4.7](https://platform.claude.com/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-47) atau [Bermigrasi ke Claude Opus 5 dari Claude Opus 4.6 dan model Opus yang lebih lama](https://platform.claude.com/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-46). Bagian tersebut mencakup delta ini ditambah perubahan breaking dari model sebelumnya (parameter sampling ditolak, pemikiran diperpanjang manual ditolak, prefill dihapus, tokenizer baru).
</Note>

#### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-8"  # Before
model = "claude-opus-5"  # After
```

`claude-opus-5` adalah ID model tetap tanpa akhiran tanggal, skema yang sama dengan `claude-opus-4-8` dan `claude-sonnet-5`.

#### Perubahan breaking

1. **Thinking aktif secara default:** Di Claude Opus 4.8, permintaan tanpa field `thinking` berjalan tanpa thinking; di Claude Opus 5, permintaan yang sama berjalan dengan [pemikiran adaptif](https://platform.claude.com/docs/id/build-with-claude/thinking). `max_tokens` tetap menjadi batas keras pada total output, thinking ditambah teks respons, jadi tinjau kembali untuk beban kerja yang berjalan tanpa thinking di Claude Opus 4.8. Untuk mempertahankan perilaku lama, kirimkan `thinking: {type: "disabled"}`, dengan tunduk pada batas effort di item berikutnya; perhatikan bahwa dengan thinking dinonaktifkan, model sesekali dapat mengeluarkan panggilan alat sebagai teks biasa atau menyertakan tag XML internal dalam output yang terlihat, jadi utamakan tingkat effort yang lebih rendah dengan thinking diaktifkan jika memungkinkan, dan lihat [Menjalankan dengan thinking dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk mitigasi jika tidak memungkinkan.

2. **Menonaktifkan thinking dibatasi pada effort `high`:** Anda masih dapat mematikan thinking dengan `thinking: {type: "disabled"}`, tetapi hanya pada tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah. Permintaan yang menggabungkan `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400. Claude Opus 4.8 menerima kombinasi ini, jadi audit permintaan yang menonaktifkan thinking sebelum Anda bermigrasi.

   Pemeriksaan ini diberlakukan pada setiap permintaan: konfigurasi effort dan thinking setiap permintaan divalidasi secara independen, sehingga permintaan yang menaikkan effort ke `xhigh` atau `max` saat thinking dinonaktifkan akan ditolak meskipun permintaan sebelumnya dalam percakapan tersebut diterima.

   Sebelum (diterima di Claude Opus 4.8, ditolak di Claude Opus 5):

   ```python
   client.messages.create(
       model="claude-opus-4-8",
       max_tokens=16000,
       thinking={"type": "disabled"},
       output_config={"effort": "xhigh"},
       messages=[{"role": "user", "content": "..."}],
   )
   ```

   Sesudah (Claude Opus 5), hapus field `thinking` untuk mengaktifkan kembali thinking:

   ```python
   client.messages.create(
       model="claude-opus-5",
       max_tokens=16000,
       output_config={"effort": "xhigh"},  # thinking is on by default
       messages=[{"role": "user", "content": "..."}],
   )
   ```

   atau biarkan thinking dinonaktifkan dan turunkan effort:

   ```python
   client.messages.create(
       model="claude-opus-5",
       max_tokens=16000,
       thinking={"type": "disabled"},
       output_config={"effort": "high"},  # or "medium", "low"
       messages=[{"role": "user", "content": "..."}],
   )
   ```

#### Perubahan yang direkomendasikan

Perubahan ini tidak wajib tetapi akan meningkatkan pengalaman Anda:

1. **Uji effort `max` untuk pekerjaan yang kritis terhadap kemampuan:** Claude Opus 5 mendukung rangkaian lengkap [tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort) (`low`, `medium`, `high`, `xhigh`, `max`). Jika kemampuan maksimum lebih penting daripada pengeluaran token, uji effort `max`. Effort ini dapat memberikan peningkatan pada tugas yang paling menuntut tetapi mungkin menunjukkan hasil yang semakin berkurang akibat peningkatan penggunaan token dan dapat cenderung berpikir berlebihan pada tugas yang lebih sederhana. Jika Anda menjalankan pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak; mulai dari 64k token dan sesuaikan dari sana.

2. **Pertimbangkan fallback otomatis:** Claude Opus 5 hadir dengan pengklasifikasi keamanan siber yang penolakan kategori cyber-nya dapat melakukan fallback ke Claude Opus 4.8. Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, pertimbangkan parameter `fallbacks` dengan mode `"default"` (`fallbacks: "default"`), yang memilih model fallback yang direkomendasikan berdasarkan kategori penolakan alih-alih daftar model yang dikelola secara manual. Fallback sisi server berstatus beta; mode `"default"` memerlukan header beta `server-side-fallback-2026-07-01`. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

3. **Cache prompt yang lebih pendek:** Panjang prompt minimum yang dapat di-cache di Claude Opus 5 adalah 512 token, turun dari 1.024 token di Claude Opus 4.8. Prompt yang terlalu pendek untuk di-cache di Claude Opus 4.8 kini dapat membuat entri cache, tanpa perubahan kode yang diperlukan. Lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

4. **Ubah alat di tengah percakapan (beta):** Anda dapat menambah atau menghapus alat di antara giliran percakapan tanpa membatalkan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya. Kirimkan header beta `mid-conversation-tool-changes-2026-07-01`. Ini berguna untuk beban kerja agentik yang mengekspos alat secara bertahap atau menghentikannya seiring kemajuan tugas; tanpanya, daftar alat yang berubah akan membatalkan prefiks yang di-cache.

5. **Sesuaikan ulang prompt panjang dan verbositas:** Respons terlihat default dan hasil tertulis berjalan lebih panjang di Claude Opus 5 daripada di Claude Opus 4.8, dan menurunkan effort mengurangi volume thinking tanpa secara andal memperpendek respons yang terlihat. Berikan prompt secara eksplisit untuk keringkasan atau panjang target sebagai gantinya. Lihat [Panjang respons dan verbositas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity) dan [Panjang hasil tertulis](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#written-deliverable-length).

6. **Hapus instruksi verifikasi yang terbawa dan batasi cakupan:** Claude Opus 5 memverifikasi pekerjaannya sendiri tanpa diperintah, jadi hapus instruksi verifikasi atau pemeriksaan mandiri eksplisit yang terbawa dari prompt yang disetel untuk model sebelumnya; membiarkannya menyebabkan verifikasi berlebihan. Untuk tugas yang sempit, batasi cakupan tugas secara eksplisit. Dalam kerangka kerja multi-agen, berikan panduan eksplisit tentang skenario mana yang memerlukan delegasi atau batasi jumlah subagen, karena Claude Opus 5 lebih mudah mendelegasikan daripada model sebelumnya. Lihat [Cakupan tugas dan verifikasi berlebihan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#task-scope-and-over-verification) dan [Mengendalikan pembuatan subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning).

#### Daftar periksa migrasi

* Perbarui nama model dari `claude-opus-4-8` ke `claude-opus-5`.
* Tinjau beban kerja yang berjalan tanpa field `thinking`: beban kerja tersebut berjalan dengan thinking di Claude Opus 5. Tinjau kembali `max_tokens`, yang tetap menjadi batas keras pada total output (thinking ditambah teks respons), atau kirimkan `thinking: {type: "disabled"}` pada effort `high` atau lebih rendah untuk mempertahankan perilaku lama. Jika Anda menonaktifkan thinking, tinjau [Menjalankan dengan thinking dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk artefak output yang dapat muncul dan mitigasi prompting-nya.
* Audit permintaan yang menonaktifkan thinking: `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400, diberlakukan pada setiap permintaan. Aktifkan kembali thinking atau turunkan effort ke `high` atau lebih rendah.
* Evaluasi ulang pengaturan `effort` Anda: jalankan sapuan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) baru pada eval Anda sendiri alih-alih membawa pengaturan yang disetel untuk model sebelumnya. Effort `low` dan `medium` layak diuji sebagai kontrol biaya dan latensi, dan uji effort `max` jika kemampuan maksimum lebih penting daripada pengeluaran token. Jika Anda menjalankan pada effort `xhigh` atau `max`, naikkan `max_tokens` ke setidaknya 64k sebagai titik awal.
* Tinjau prompt yang mendekati minimum caching: prompt dengan 512 token atau lebih kini dapat membuat entri cache, turun dari 1.024 token di Claude Opus 4.8.
* Tangani `stop_reason: "refusal"`, dan pertimbangkan `fallbacks: "default"` (beta) untuk menjalankan ulang permintaan yang ditolak pada model fallback yang direkomendasikan secara otomatis.
* Jika organisasi Anda memiliki komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models), rencanakan kapasitas secara terpisah: Priority Tier tidak didukung di Claude Opus 5, sementara Claude Opus 4.8 tetap mendukungnya.
* Untuk beban kerja agentik, pertimbangkan [anggaran tugas](https://platform.claude.com/docs/id/build-with-claude/task-budgets) (beta) dan perubahan alat di tengah percakapan (beta).
* Sesuaikan ulang prompt panjang dan verbositas: respons terlihat default dan hasil tertulis berjalan lebih panjang di Claude Opus 5, dan menurunkan effort mengurangi volume thinking tanpa secara andal memperpendek respons yang terlihat. Berikan prompt secara eksplisit untuk keringkasan atau panjang target. Lihat [Panjang respons dan verbositas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity) dan [Panjang hasil tertulis](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#written-deliverable-length).
* Hapus instruksi verifikasi dan pemeriksaan mandiri yang terbawa dari prompt yang disetel untuk model sebelumnya (instruksi tersebut menyebabkan verifikasi berlebihan di Claude Opus 5), batasi cakupan tugas secara eksplisit untuk tugas yang sempit, dan dalam kerangka kerja multi-agen arahkan atau batasi delegasi subagen. Lihat [Cakupan tugas dan verifikasi berlebihan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#task-scope-and-over-verification) dan [Mengendalikan pembuatan subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning).
* Tetapkan ulang baseline biaya dan latensi pada beban kerja Anda sendiri.

### Migrasi ke Claude Opus 5 dari Claude Opus 4.7

Claude Opus 5 seharusnya memiliki kinerja bawaan yang kuat pada prompt dan eval Claude Opus 4.7 yang sudah ada, dengan harga yang sama yaitu $5 per juta token input dan $25 per juta token output. Model ini mendukung rangkaian fitur yang sama dengan Claude Opus 4.7, termasuk ["context window" (jendela konteks) 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows), [128k token output maksimum](https://platform.claude.com/docs/id/about-claude/models/overview), ["adaptive thinking" (pemikiran adaptif)](https://platform.claude.com/docs/id/build-with-claude/thinking), ["prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching), ["batch processing" (pemrosesan batch)](https://platform.claude.com/docs/id/build-with-claude/batch-processing), [Files API](https://platform.claude.com/docs/id/build-with-claude/files), [dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support), [vision](https://platform.claude.com/docs/id/build-with-claude/vision), serta [alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien, dengan dua pengecualian: [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) tidak tersedia di Claude Opus 5, dan [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) tidak didukung di Claude Opus 5. Model ini juga menambahkan [pesan sistem di tengah percakapan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages) dan mendokumentasikan secara publik [detail penghentian penolakan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response). Di Claude API, Claude Opus 5 juga mendukung ["computer use" (penggunaan komputer)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) sebagai toolset stabil `computer_toolset_20260801` dan [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) untuk tugas di dalam halaman web, yang keduanya tidak didukung oleh Claude Opus 4.7; integrasi yang sudah ada pada versi `computer_20251124` sebelumnya tetap berfungsi tanpa perubahan di kedua model. Untuk meningkatkan integrasi yang sudah ada, lihat [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124).

<Note>
  Jika kode Anda menggunakan Claude Opus 4.6 atau yang lebih lama, gunakan [Migrasi ke Claude Opus 5 dari Claude Opus 4.6 dan model Opus yang lebih lama](https://platform.claude.com/docs/id/about-claude/models/migration-guide#migrating-from-claude-opus-46) sebagai gantinya. Bagian tersebut mencakup perubahan yang merusak kompatibilitas (parameter sampling ditolak, "extended thinking" (pemikiran diperpanjang) manual ditolak, tokenizer baru) yang tidak dicakup oleh peningkatan dari Claude Opus 4.7 saja.
</Note>

#### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-7"  # Before
model = "claude-opus-5"  # After
```

#### Perubahan yang merusak kompatibilitas

1. **Thinking aktif secara default:** Di Claude Opus 4.7, permintaan tanpa field `thinking` berjalan tanpa thinking; di Claude Opus 5, permintaan yang sama berjalan dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking). `max_tokens` tetap menjadi batas keras pada total output, yaitu thinking ditambah teks respons, jadi tinjau kembali nilainya untuk beban kerja yang berjalan tanpa thinking di Claude Opus 4.7. Untuk mempertahankan perilaku lama, kirimkan `thinking: {type: "disabled"}`, dengan tunduk pada batas effort di butir berikutnya; perhatikan bahwa dengan thinking dinonaktifkan, model sesekali dapat mengeluarkan pemanggilan alat sebagai teks biasa atau menyertakan tag XML internal dalam output yang terlihat, jadi utamakan level effort yang lebih rendah dengan thinking diaktifkan jika memungkinkan, dan lihat [Menjalankan dengan thinking dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk mitigasi jika tidak memungkinkan.

2. **Menonaktifkan thinking dibatasi pada effort `high`:** Anda dapat mematikan thinking dengan `thinking: {type: "disabled"}`, tetapi hanya pada level [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau di bawahnya. Permintaan yang menggabungkan `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400. Claude Opus 4.7 menerima kombinasi ini, jadi audit permintaan yang menonaktifkan thinking sebelum Anda bermigrasi.

   Pemeriksaan ini diberlakukan pada setiap permintaan: konfigurasi effort dan thinking setiap permintaan divalidasi secara independen, sehingga permintaan yang menaikkan effort ke `xhigh` atau `max` saat thinking dinonaktifkan akan ditolak meskipun permintaan sebelumnya dalam percakapan tersebut diterima.

   Sebelum (diterima di Claude Opus 4.7, ditolak di Claude Opus 5):

   ```python
   client.messages.create(
       model="claude-opus-4-7",
       max_tokens=16000,
       thinking={"type": "disabled"},
       output_config={"effort": "xhigh"},
       messages=[{"role": "user", "content": "..."}],
   )
   ```

   Sesudah (Claude Opus 5), hapus field `thinking` untuk berjalan dengan thinking:

   ```python
   client.messages.create(
       model="claude-opus-5",
       max_tokens=16000,
       output_config={"effort": "xhigh"},  # thinking is on by default
       messages=[{"role": "user", "content": "..."}],
   )
   ```

   atau biarkan thinking tetap dinonaktifkan dan turunkan effort:

   ```python
   client.messages.create(
       model="claude-opus-5",
       max_tokens=16000,
       thinking={"type": "disabled"},
       output_config={"effort": "high"},  # or "medium", "low"
       messages=[{"role": "user", "content": "..."}],
   )
   ```

#### Apa yang berubah

Butir-butir berikut bukan perubahan yang merusak kompatibilitas; butir-butir ini menjelaskan perbedaan perilaku yang perlu diperiksa setelah Anda mengganti ID model.

1. **Parameter sampling (tidak berubah):** Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default mengembalikan error 400 di Claude Opus 5, sama seperti di Claude Opus 4.7. Sebagian besar SDK masih mendefinisikan field ini demi kompatibilitas dengan model sebelumnya, sehingga kode yang mengaturnya lolos pemeriksaan tipe meskipun API menolak permintaan tersebut. Python SDK (v1.0 dan yang lebih baru) tidak mendefinisikannya, dan mengirimkannya akan memunculkan `TypeError`. Jika Anda telah menghapus parameter ini saat bermigrasi ke Opus 4.7, tidak diperlukan perubahan lebih lanjut.

2. **Default effort adalah `high`:** Default [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) di Claude Opus 5 adalah `high` di Claude API dan Claude Code. Jika Anda sudah mengatur effort secara eksplisit, pengaturan Anda tidak berubah.

3. **Level effort dikalibrasi ulang:** Alokasi token di balik setiap level effort berubah di Claude Opus 5 dibandingkan dengan Claude Opus 4.7, dan Claude Opus 5 mendukung rangkaian lengkap level effort (`low`, `medium`, `high`, `xhigh`, `max`). Jalankan sapuan effort baru pada eval Anda sendiri alih-alih membawa pengaturan yang disetel untuk Claude Opus 4.7. Effort `low` dan `medium` layak diuji sebagai kontrol biaya dan latensi, dan uji effort `max` jika kemampuan maksimum lebih penting daripada pengeluaran token. Jika Anda menjalankan pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak; mulai dari 64k token dan setel dari sana. Lihat [Effort](https://platform.claude.com/docs/id/build-with-claude/effort).

4. **Jendela konteks 1M adalah default:** Claude Opus 5 melayani [jendela konteks](https://platform.claude.com/docs/id/build-with-claude/context-windows) 1M token penuh secara default tanpa header beta dan tanpa premi konteks panjang. Jika klien Anda mengirimkan header beta jendela konteks demi kompatibilitas dengan model lama, Anda dapat menghapusnya di Claude Opus 5.

5. **Pesan sistem di tengah percakapan:** Claude Opus 5 menerima pesan `role: "system"` tepat setelah giliran pengguna dalam array `messages` (tunduk pada [aturan penempatan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)). Gunakan field `system` tingkat atas untuk instruksi yang berlaku sejak awal. Claude Opus 4.7 menolak `role: "system"` dalam `messages` dengan error 400. Jika Anda memelihara jalur kode yang membangun ulang seluruh riwayat pesan untuk memperbarui instruksi, Anda dapat menyederhanakannya dan mempertahankan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya.

6. **Detail penghentian penolakan:** Objek `stop_details` pada respons penolakan (tersedia sejak Claude Opus 4.7) kini didokumentasikan secara publik. Ketika model menolak suatu permintaan, objek ini mengidentifikasi kategori penolakan, selain stop reason `refusal` yang sudah ada. Tidak diperlukan header beta, dan tidak ada opsi untuk menonaktifkannya. Lihat [Menangani stop reason](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons).

7. **Minimum caching prompt lebih rendah:** Panjang prompt minimum yang dapat di-cache di Claude Opus 5 adalah 512 token, lebih rendah daripada di Claude Opus 4.7. Prompt yang terlalu pendek untuk di-cache di Claude Opus 4.7 kini dapat membuat entri cache, tanpa perlu perubahan kode. Lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

8. **Fast mode:** Claude Opus 5 mendukung [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) (pratinjau riset); fast mode tidak tersedia di Claude Opus 4.7, di mana permintaan dengan `speed: "fast"` mengembalikan error. Parameter `speed: "fast"` dan header beta `fast-mode-2026-02-01` berfungsi tanpa perubahan di Claude Opus 5.

#### Perubahan yang direkomendasikan

Perubahan ini tidak wajib tetapi akan meningkatkan pengalaman Anda:

1. **Pertimbangkan fallback otomatis:** Claude Opus 5 dirilis dengan pengklasifikasi keamanan siber yang penolakan kategori sibernya dapat melakukan fallback ke Claude Opus 4.8. Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, pertimbangkan parameter `fallbacks` dengan mode `"default"` (`fallbacks: "default"`), yang memilih model fallback yang direkomendasikan berdasarkan kategori penolakan alih-alih daftar model yang dipelihara secara manual. Fallback sisi server masih dalam beta; mode `"default"` memerlukan header beta `server-side-fallback-2026-07-01`. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

2. **Ubah alat di tengah percakapan (beta):** Anda dapat menambah atau menghapus alat di antara giliran percakapan tanpa membatalkan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya. Kirim header beta `mid-conversation-tool-changes-2026-07-01`. Ini berguna untuk beban kerja agentik yang mengekspos alat secara bertahap atau menghentikannya seiring kemajuan tugas; tanpanya, daftar alat yang berubah akan membatalkan prefiks yang di-cache.

3. **Setel ulang prompt panjang dan verbositas:** Respons terlihat default dan hasil kerja tertulis cenderung lebih panjang di Claude Opus 5 daripada di model Opus sebelumnya, dan menurunkan effort mengurangi volume thinking tanpa secara andal memperpendek respons yang terlihat. Sebagai gantinya, minta secara eksplisit agar ringkas atau tentukan panjang target. Lihat [Panjang respons dan verbositas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity) dan [Panjang hasil kerja tertulis](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#written-deliverable-length).

4. **Hapus instruksi verifikasi yang terbawa dan batasi cakupan:** Claude Opus 5 memverifikasi pekerjaannya sendiri tanpa perlu diperintah, jadi hapus instruksi verifikasi atau pemeriksaan mandiri eksplisit yang terbawa dari prompt yang disetel untuk model sebelumnya; membiarkannya akan menyebabkan verifikasi berlebihan. Untuk tugas yang sempit, batasi cakupan tugas secara eksplisit. Dalam kerangka kerja multi-agen, berikan panduan eksplisit tentang skenario mana yang memerlukan delegasi atau batasi jumlah subagen, karena Claude Opus 5 lebih mudah mendelegasikan daripada model sebelumnya. Lihat [Cakupan tugas dan verifikasi berlebihan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#task-scope-and-over-verification) dan [Mengontrol pembuatan subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning).

#### Daftar periksa migrasi

* Perbarui nama model dari `claude-opus-4-7` ke `claude-opus-5` (atau perbarui alias).
* Tinjau beban kerja yang berjalan tanpa field `thinking`: beban kerja tersebut berjalan dengan thinking di Claude Opus 5. Tinjau kembali `max_tokens`, yang tetap menjadi batas keras pada total output (thinking ditambah teks respons), atau kirimkan `thinking: {type: "disabled"}` pada effort `high` atau di bawahnya untuk mempertahankan perilaku lama. Jika Anda menonaktifkan thinking, tinjau [Menjalankan dengan thinking dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk artefak output yang dapat muncul dan mitigasi prompting-nya.
* Audit permintaan yang menonaktifkan thinking: `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400, yang diberlakukan pada setiap permintaan. Aktifkan kembali thinking atau turunkan effort ke `high` atau di bawahnya.
* Jika Anda telah menghapus parameter sampling selama migrasi Opus 4.7, tidak diperlukan tindakan apa pun. Jika Anda menambahkannya kembali dengan jalur retry 400, hapus jalur retry tersebut.
* Evaluasi ulang pengaturan `effort` Anda: jalankan sapuan [effort](https://platform.claude.com/docs/id/build-with-claude/effort) baru pada eval Anda sendiri alih-alih membawa pengaturan yang disetel untuk Claude Opus 4.7. Uji effort `low` dan `medium` sebagai kontrol biaya dan latensi, dan effort `max` jika kemampuan maksimum lebih penting daripada pengeluaran token. Jika Anda menjalankan pada effort `xhigh` atau `max`, naikkan `max_tokens` ke setidaknya 64k sebagai titik awal.
* Hapus header beta jendela konteks apa pun. Jendela konteks 1M adalah default di Claude API, Amazon Bedrock, Google Cloud, dan Microsoft Foundry.
* Jika Anda membangun ulang riwayat percakapan untuk memperbarui instruksi, pertimbangkan untuk beralih ke pesan sistem di tengah percakapan guna mempertahankan hit cache prompt.
* Verifikasi bahwa penanganan stop reason Anda membaca `stop_details` pada penolakan (tersedia sejak Claude Opus 4.7; kini didokumentasikan secara publik), dan pertimbangkan `fallbacks: "default"` (beta) untuk menjalankan ulang permintaan yang ditolak pada model fallback yang direkomendasikan secara otomatis.
* Tinjau prompt yang mendekati minimum caching: prompt dengan 512 token atau lebih kini dapat membuat entri cache.
* Jika Anda menggunakan [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool), rencanakan alternatif: fitur ini tidak tersedia di Claude Opus 5.
* Jika organisasi Anda memiliki komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models), perhatikan bahwa Priority Tier tidak didukung di Claude Opus 5.
* Jika Anda menggunakan fast mode di Claude Opus 4.7, tidak diperlukan perubahan permintaan selain ID model: `speed: "fast"` dan header beta `fast-mode-2026-02-01` berfungsi tanpa perubahan di Claude Opus 5.
* Untuk beban kerja agentik, pertimbangkan [task budget](https://platform.claude.com/docs/id/build-with-claude/task-budgets) (beta) dan perubahan alat di tengah percakapan (beta).
* Setel ulang prompt panjang dan verbositas, serta hapus instruksi verifikasi dan pemeriksaan mandiri yang terbawa dari prompt yang disetel untuk model sebelumnya.
* Tetapkan ulang baseline biaya dan latensi pada level effort yang Anda pilih.

### Bermigrasi ke Claude Opus 5 dari Claude Opus 4.6 dan model Opus sebelumnya

Claude Opus 5 seharusnya memiliki performa bawaan yang kuat pada prompt dan eval Claude Opus 4.6 yang sudah ada dengan harga yang sama, tetapi ada beberapa perubahan perilaku dan API yang perlu diketahui saat Anda bermigrasi. Sebagian besar perubahan ini mulai berlaku di Claude Opus 4.7; dua perubahan lagi, yaitu thinking aktif secara default dan batas effort untuk menonaktifkan thinking, mulai berlaku di Claude Opus 5. Semuanya dibahas di bawah ini, sehingga bagian ini lengkap untuk kode yang datang langsung dari Claude Opus 4.6. Claude Opus 5 mendukung rangkaian fitur yang sama dengan Claude Opus 4.6, termasuk:

* ["Context window" (jendela konteks) 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) dengan harga API standar tanpa premi konteks panjang
* [128k token output maksimum](https://platform.claude.com/docs/id/about-claude/models/overview)
* [Adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking)
* ["Prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching)
* [Pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing)
* [Files API](https://platform.claude.com/docs/id/build-with-claude/files)
* [Dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support)
* [Vision](https://platform.claude.com/docs/id/build-with-claude/vision)
* [Alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien ([bash](https://platform.claude.com/docs/id/agents-and-tools/tool-use/bash-tool), [eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool), [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool), [editor teks](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool), [pencarian web](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-search-tool), [konektor MCP](https://platform.claude.com/docs/id/agents-and-tools/mcp-connector), [memori](https://platform.claude.com/docs/id/agents-and-tools/tool-use/memory-tool))

Dua pengecualian: [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) tidak tersedia di Claude Opus 5, dan [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) tidak didukung di Claude Opus 5. Di Claude API, Claude Opus 5 juga mendukung [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) sebagai toolset stabil `computer_toolset_20260801` dan [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) untuk tugas di dalam halaman web, yang keduanya tidak didukung oleh Claude Opus 4.6 atau model Opus sebelumnya; integrasi yang sudah ada pada versi `computer_20251124` sebelumnya tetap berfungsi tanpa perubahan di Claude Opus 5. Untuk meningkatkan integrasi yang sudah ada, lihat [Bermigrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124).

#### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-6"  # Before
model = "claude-opus-5"  # After
```

#### Perubahan yang merusak kompatibilitas

1. **"Extended thinking" (pemikiran diperpanjang) dihapus:** `thinking: {type: "enabled", budget_tokens: N}` tidak lagi didukung di Claude Opus 4.7 atau model yang lebih baru dan mengembalikan error 400. Beralihlah ke [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (`thinking: {type: "adaptive"}`) dan gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking. Di Claude Opus 5, adaptive thinking **aktif secara default**: `thinking: {type: "adaptive"}` valid dan setara dengan menghilangkan field `thinking` sepenuhnya (lihat butir berikutnya).

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

   Sesudah (Claude Opus 5):

   <CodeGroup>
     ```bash cURL
     curl https://api.anthropic.com/v1/messages \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -H "content-type: application/json" \
       -d '{
         "model": "claude-opus-5",
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
     model: claude-opus-5
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
         model="claude-opus-5",
         max_tokens=16000,
         thinking={"type": "adaptive"},
         output_config={"effort": "high"},  # or "max", "xhigh", "medium", "low"
         messages=[{"role": "user", "content": "..."}],
     )
     ```

     ```typescript TypeScript
     await client.messages.create({
       model: "claude-opus-5",
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
         Model = "claude-opus-5",
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
     	Model:     "claude-opus-5",
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
         .model("claude-opus-5")
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
         model: 'claude-opus-5',
         thinking: ['type' => 'adaptive'],
         outputConfig: ['effort' => 'high'], // or 'max', 'xhigh', 'medium', 'low'
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     message = client.messages.create(
       model: "claude-opus-5",
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

   Adaptive thinking dapat diarahkan melalui prompting dan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort); lihat [Memilih tingkat effort](https://platform.claude.com/docs/id/about-claude/models/migration-guide#choosing-an-effort-level).

2. **Thinking aktif secara default:** Di Claude Opus 4.6 dan Claude Opus 4.7, permintaan tanpa field `thinking` berjalan tanpa thinking; di Claude Opus 5, permintaan yang sama berjalan dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking). `max_tokens` tetap menjadi batas keras pada total output, yaitu thinking ditambah teks respons, jadi tinjau kembali nilainya untuk beban kerja yang sebelumnya berjalan tanpa thinking. Untuk mempertahankan perilaku lama, kirimkan `thinking: {type: "disabled"}`, dengan tunduk pada batas effort di butir berikutnya; perhatikan bahwa dengan thinking dinonaktifkan, model terkadang dapat mengeluarkan pemanggilan alat sebagai teks biasa atau menyertakan tag XML internal dalam output yang terlihat, jadi utamakan tingkat effort yang lebih rendah dengan thinking diaktifkan jika memungkinkan, dan lihat [Menjalankan dengan thinking dinonaktifkan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) untuk mitigasi jika tidak memungkinkan.

3. **Menonaktifkan thinking dibatasi pada effort `high`:** Anda dapat mematikan thinking dengan `thinking: {type: "disabled"}`, tetapi hanya pada tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah. Permintaan yang menggabungkan `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400 di Claude Opus 5, yang diberlakukan pada setiap permintaan. Audit permintaan yang menonaktifkan thinking sebelum Anda bermigrasi: aktifkan kembali thinking atau turunkan effort ke `high` atau lebih rendah.

4. **Parameter sampling dihapus:** Mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default apa pun di Claude Opus 4.7 atau model yang lebih baru, termasuk Claude Opus 5, mengembalikan error 400. Python SDK (v1.0 dan yang lebih baru) tidak mendefinisikannya, dan mengirimkannya akan memunculkan `TypeError`. Jalur migrasi paling aman adalah menghilangkan parameter ini sepenuhnya dari payload permintaan. Prompting adalah cara yang direkomendasikan untuk memandu perilaku model di Claude Opus 5. Jika Anda sebelumnya menggunakan `temperature = 0` untuk determinisme, perhatikan bahwa hal itu tidak pernah menjamin output yang identik pada model sebelumnya.

5. **Konten thinking dihilangkan secara default:** Blok thinking masih muncul dalam stream respons di Claude Opus 4.7 dan model yang lebih baru, tetapi field `thinking`-nya kosong kecuali Anda secara eksplisit memilih untuk mengaktifkannya. Ini adalah perubahan diam-diam dari Claude Opus 4.6, yang default-nya mengembalikan teks thinking yang diringkas. Untuk memulihkan konten thinking yang diringkas, atur `thinking.display` ke `"summarized"`:

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

   Default-nya adalah `"omitted"` di Claude Opus 4.7 dan model yang lebih baru. Jika produk Anda melakukan streaming penalaran kepada pengguna, default baru ini tampak sebagai jeda panjang sebelum output dimulai; atur `display: "summarized"` untuk memulihkan progres yang terlihat selama thinking. Lihat [Mengontrol tampilan thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#controlling-thinking-display) untuk detailnya.

6. **Penghitungan token diperbarui:** Claude Opus 4.7 memperkenalkan tokenizer baru, yang juga digunakan oleh model Opus yang lebih baru, termasuk Claude Opus 5. Tokenizer ini berkontribusi pada peningkatan performa di berbagai tugas, dan mungkin menggunakan sekitar 1x hingga 1,35x lebih banyak token saat memproses teks dibandingkan model sebelum Claude Opus 4.7 (hingga \~35% lebih banyak, bervariasi menurut konten).

   [`/v1/messages/count_tokens`](https://platform.claude.com/docs/id/build-with-claude/token-counting) mengembalikan jumlah token yang berbeda untuk Claude Opus 5 dibandingkan untuk Claude Opus 4.6. Efisiensi token dapat bervariasi menurut bentuk beban kerja.

   Intervensi prompting, `task_budget`, dan `effort` dapat membantu mengontrol biaya dan memastikan penggunaan token yang sesuai. Kontrol ini mungkin mengorbankan kecerdasan model. Perbarui parameter `max_tokens` Anda untuk memberikan ruang tambahan, termasuk pemicu compaction. Claude Opus 5 menyediakan jendela konteks 1M dengan harga API standar tanpa premi konteks panjang.

7. **Penghapusan prefill (dibawa dari Opus 4.6):** Melakukan prefill pada pesan asisten mengembalikan error 400 di Claude Opus 4.7 dan model yang lebih baru, termasuk Claude Opus 5. Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

#### Memilih tingkat effort

[Parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) memungkinkan Anda menyetel kecerdasan Claude versus pengeluaran token, menukar kemampuan dengan kecepatan lebih tinggi dan biaya lebih rendah. Claude Opus 5 mendukung seluruh rangkaian tingkat effort dan default-nya adalah `high`. Jalankan sweep effort baru pada eval Anda sendiri daripada membawa pengaturan yang disetel untuk model sebelumnya:

* **`max`:** Dapat memberikan peningkatan pada tugas yang paling menuntut tetapi mungkin menunjukkan hasil yang semakin berkurang dari peningkatan penggunaan token dan dapat cenderung berpikir berlebihan pada tugas yang lebih sederhana. Uji pada kasus di mana kemampuan maksimum lebih penting daripada pengeluaran token.
* **`xhigh`:** Kemampuan yang diperluas untuk pekerjaan agentic dan coding yang berjalan lama yang membutuhkan kedalaman lebih dari default.
* **`high`:** Default. Menyeimbangkan penggunaan token dan kecerdasan untuk sebagian besar tugas.
* **`medium`:** Penurunan satu tingkat dari default untuk menghemat biaya, layak diuji sebagai kontrol biaya dan latensi.
* **`low`:** Paling efisien. Cadangkan untuk tugas singkat dengan cakupan terbatas dan beban kerja yang sensitif terhadap latensi.

Jika Anda menjalankan pada effort `xhigh` atau `max`, atur `max_tokens` yang besar agar model memiliki ruang untuk berpikir dan bertindak; mulailah dari 64k token dan setel dari sana. Effort lebih penting untuk model ini daripada untuk Opus mana pun sebelumnya. Bereksperimenlah dengannya secara aktif saat Anda melakukan upgrade.

#### Perubahan perilaku

Claude Opus 4.7 memperkenalkan beberapa perbedaan perilaku dari Claude Opus 4.6 yang bukan merupakan perubahan API yang merusak kompatibilitas tetapi mungkin memerlukan pembaruan prompt atau penghapusan scaffolding. Perubahan ini berlanjut ke Claude Opus 5, dengan penyesuaian yang dicatat di bawah.

1. **Panjang respons bervariasi menurut kasus penggunaan:** Claude Opus 4.7 mengkalibrasi panjang respons sesuai dengan seberapa kompleks tugas tersebut menurut penilaiannya, alih-alih menggunakan tingkat verbositas tetap secara default. Ini biasanya berarti jawaban yang lebih pendek pada pencarian sederhana dan jauh lebih panjang pada analisis terbuka.

   Jika produk Anda bergantung pada gaya atau verbositas output tertentu, Anda mungkin perlu menyetel prompt Anda. Misalnya, untuk mengurangi verbositas, tambahkan: "Provide concise, focused responses. Skip non-essential context, and keep examples minimal." Jika Anda melihat jenis penjelasan berlebihan tertentu, tambahkan instruksi yang ditargetkan dalam prompt Anda untuk mencegahnya.

   Contoh positif yang menunjukkan bagaimana Claude dapat berkomunikasi dengan tingkat keringkasan yang sesuai cenderung lebih efektif daripada contoh negatif atau instruksi yang memberi tahu model apa yang tidak boleh dilakukan. Di Claude Opus 5, respons terlihat default dan hasil kerja tertulis lebih panjang daripada model Opus sebelumnya, dan menurunkan effort mengurangi volume thinking tanpa secara andal memperpendek respons yang terlihat; berikan prompt secara eksplisit untuk keringkasan atau panjang target. Lihat [Panjang respons dan verbositas](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity).

2. **Mengikuti instruksi secara lebih harfiah:** Claude Opus 4.7 menafsirkan prompt secara lebih harfiah dan eksplisit daripada Claude Opus 4.6, terutama pada tingkat effort yang lebih rendah. Model ini tidak secara diam-diam menggeneralisasi instruksi dari satu item ke item lain, dan tidak menyimpulkan permintaan yang tidak Anda buat. Sisi positif dari keharfiahan ini adalah presisi dan lebih sedikit kerja sia-sia. Model ini umumnya berkinerja lebih baik untuk kasus penggunaan API dengan prompt yang disetel dengan cermat, ekstraksi terstruktur, dan pipeline di mana Anda menginginkan perilaku yang dapat diprediksi. Peninjauan prompt dan harness mungkin sangat membantu untuk migrasi ke Claude Opus 5.

3. **Nada yang lebih langsung:** Seperti halnya model baru mana pun, gaya prosa pada tulisan panjang mungkin bergeser. Claude Opus 4.7 lebih langsung dan beropini, dengan lebih sedikit frasa yang mengedepankan validasi dan lebih sedikit emoji dibandingkan gaya Claude Opus 4.6 yang lebih hangat. Jika produk Anda mengandalkan suara tertentu, evaluasi ulang prompt gaya terhadap baseline baru.

4. **Pembaruan progres bawaan dalam jejak agentic:** Claude Opus 4.7 memberikan pembaruan yang lebih teratur dan berkualitas lebih tinggi kepada pengguna sepanjang jejak agentic yang panjang. Jika Anda telah menambahkan scaffolding untuk memaksa pesan status sementara ("After every 3 tool calls, summarize progress"), cobalah menghapusnya. Jika Anda mendapati bahwa panjang atau isi pembaruan Claude Opus 4.7 yang ditujukan kepada pengguna tidak terkalibrasi dengan baik untuk kasus penggunaan Anda, jelaskan secara eksplisit seperti apa pembaruan ini seharusnya dalam prompt dan berikan contoh.

5. **Pembuatan subagen berubah:** Claude Opus 4.7 cenderung membuat lebih sedikit subagen secara default daripada Claude Opus 4.6, sementara Claude Opus 5 mendelegasikan ke subagen dengan lebih mudah daripada model sebelumnya. Perilaku ini dapat diarahkan melalui prompting ke kedua arah; berikan panduan eksplisit tentang kapan subagen diinginkan, atau batasi jumlah subagen. Lihat [Mengontrol pembuatan subagen](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning).

6. **Kalibrasi effort yang lebih ketat:** Berubah secara signifikan dari Claude Opus 4.6, Claude Opus 4.7 mematuhi [tingkat effort](https://platform.claude.com/docs/id/build-with-claude/effort) secara ketat, terutama di tingkat rendah. Pada `low` dan `medium`, model membatasi pekerjaannya pada apa yang diminta alih-alih melakukan lebih dari yang diminta.

   Ini baik untuk latensi dan biaya, tetapi pada tugas yang cukup kompleks yang berjalan pada effort `low` ada risiko kurang berpikir. Jika Anda mengamati penalaran yang dangkal pada masalah kompleks, naikkan effort ke `high` atau `xhigh` daripada mengatasinya melalui prompting.

   Jika Anda perlu mempertahankan effort pada `low` demi latensi, tambahkan panduan yang ditargetkan: "This task involves multistep reasoning. Think carefully through the problem before responding." Lihat [Tingkat effort yang direkomendasikan untuk Claude Opus 4.7](https://platform.claude.com/docs/id/build-with-claude/effort#recommended-effort-levels-for-claude-opus-4-7).

7. **Lebih sedikit pemanggilan alat secara default:** Claude Opus 4.7 memiliki kecenderungan untuk menggunakan alat lebih jarang daripada Claude Opus 4.6 dan lebih banyak menggunakan penalaran. Ini menghasilkan hasil yang lebih baik dalam sebagian besar kasus.

   Untuk meningkatkan "tool use" (penggunaan alat), naikkan pengaturan effort. Pengaturan effort `high` atau `xhigh` menunjukkan penggunaan alat yang jauh lebih banyak dalam pencarian agentic dan coding. Anda juga dapat menyesuaikan prompt Anda untuk secara eksplisit menginstruksikan model tentang kapan dan bagaimana menggunakan alatnya dengan benar.

8. **Pengaman keamanan siber real-time:** Baru ditambahkan di Claude Opus 4.7, permintaan yang melibatkan topik terlarang atau berisiko tinggi dapat menyebabkan penolakan. Untuk pekerjaan keamanan yang sah seperti penetration testing, riset kerentanan, atau red-teaming, ajukan permohonan ke [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet) untuk meminta pengurangan pembatasan. Jalur permohonan bergantung pada cara Anda mengakses Claude.

9. **Dukungan gambar resolusi tinggi:** Claude Opus 4.7 adalah model Claude pertama dengan dukungan gambar resolusi tinggi. Resolusi gambar maksimum adalah 2.576 piksel pada sisi panjang, naik dari 1.568 piksel pada model sebelumnya. Ini membuka peningkatan pada beban kerja yang sarat vision dan sangat berharga untuk computer use, pemahaman screenshot, dan analisis dokumen.

   Dukungan resolusi tinggi bersifat otomatis dan tidak memerlukan header beta atau opt-in sisi klien. Dua hal yang perlu direncanakan:

   * Gambar resolusi penuh dapat menggunakan hingga sekitar 3x lebih banyak token gambar daripada model sebelumnya (hingga 4.784 token per gambar, dibandingkan dengan batas sebelumnya sekitar 1.600 token per gambar). Anggarkan ulang `max_tokens` dan ekspektasi biaya untuk beban kerja yang sarat gambar, atau lakukan downsample sebelum mengirim jika Anda tidak memerlukan fidelitas tambahan.
   * Koordinat penunjukan dan bounding-box yang dikembalikan oleh model bersifat 1:1 dengan piksel gambar sebenarnya di Claude Opus 4.7, sehingga tidak diperlukan konversi faktor skala.

   Lihat [Dukungan gambar resolusi tinggi di Claude Opus 4.7](https://platform.claude.com/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) untuk detailnya.

#### Perubahan yang direkomendasikan

Perubahan ini tidak wajib tetapi akan meningkatkan pengalaman Anda:

1. **Evaluasi ulang `max_tokens`:** Karena teks yang sama menghasilkan jumlah token yang lebih tinggi di Claude Opus 4.7 dan model yang lebih baru, perbarui parameter `max_tokens` Anda untuk memberikan ruang tambahan, termasuk pemicu compaction. Intervensi prompting, [`task_budget`](https://platform.claude.com/docs/id/build-with-claude/task-budgets), dan [`effort`](https://platform.claude.com/docs/id/build-with-claude/effort) dapat membantu mengontrol biaya dan memastikan penggunaan token yang sesuai.

2. **Audit ekspektasi jumlah token:** Setiap jalur kode yang memperkirakan token di sisi klien atau mengasumsikan rasio token-ke-karakter yang tetap harus diuji ulang terhadap Claude Opus 5. Gunakan [endpoint penghitungan token](https://platform.claude.com/docs/id/build-with-claude/token-counting) untuk memverifikasi.

3. **Adopsi [task budget](https://platform.claude.com/docs/id/build-with-claude/task-budgets) (beta):** Claude Opus 4.7 memperkenalkan task budget. Anggaran ini memungkinkan Anda memberi tahu Claude berapa banyak token yang dimilikinya untuk satu loop agentic penuh, termasuk thinking, pemanggilan alat, hasil alat, dan output akhir. Model melihat hitungan mundur yang berjalan dan menggunakannya untuk memprioritaskan pekerjaan dan menyelesaikan tugas dengan baik saat anggaran habis. Untuk menggunakannya, atur header beta `task-budgets-2026-03-13` dan tambahkan yang berikut ke output config Anda:

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

   Anda mungkin perlu bereksperimen dengan task budget yang berbeda untuk kasus penggunaan Anda. Jika model diberi task budget yang terlalu ketat, model mungkin menyelesaikan tugas dengan kurang menyeluruh, dengan merujuk anggarannya sebagai kendala.

   Untuk tugas agentic terbuka di mana kualitas lebih penting daripada kecepatan, jangan atur task budget. Cadangkan task budget untuk beban kerja di mana Anda memerlukan model untuk membatasi pekerjaannya pada jatah token. Nilai minimum untuk task budget adalah 20k token.

   Task budget bukanlah batas keras; ini adalah saran yang disadari oleh model. Ini berbeda dari `max_tokens`:

   * **`task_budget`:** batas bersifat anjuran di seluruh loop agentic penuh. Model melihatnya dan menggunakannya untuk mengatur ritmenya sendiri.
   * **`max_tokens`:** batas atas keras per permintaan pada token yang dihasilkan. Nilai ini tidak diteruskan ke model, sehingga model tidak menyadarinya.

   Gunakan `task_budget` ketika Anda ingin model memoderasi dirinya sendiri, dan `max_tokens` sebagai batas atas keras untuk membatasi penggunaan.

4. **Atur `max_tokens` yang besar pada effort `max` atau `xhigh`:** Jika Anda menjalankan Claude Opus 4.7 atau model yang lebih baru pada effort `max` atau `xhigh`, atur anggaran token output maksimum yang besar agar model memiliki ruang untuk berpikir dan bertindak di seluruh subagen dan pemanggilan alatnya. Mulailah dari 64k token dan setel dari sana.

5. **Lakukan downsample gambar jika resolusi tinggi tidak diperlukan:** Claude Opus 4.7 dan model yang lebih baru mendukung gambar hingga 2576px / 3,75MP. Gambar resolusi tinggi menggunakan lebih banyak token. Jika fidelitas gambar tambahan tidak diperlukan, lakukan downsample gambar sebelum mengirim ke Claude untuk menghindari peningkatan penggunaan token. Lihat [Gambar dan vision](https://platform.claude.com/docs/id/build-with-claude/vision).

6. **Pertimbangkan fallback otomatis:** Claude Opus 5 dirilis dengan classifier keamanan siber yang penolakan kategori sibernya dapat melakukan fallback ke Claude Opus 4.8. Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, pertimbangkan parameter `fallbacks` dengan mode `"default"` (`fallbacks: "default"`), yang memilih model fallback yang direkomendasikan berdasarkan kategori penolakan alih-alih daftar model yang dikelola secara manual. Fallback sisi server masih dalam beta; mode `"default"` memerlukan header beta `server-side-fallback-2026-07-01`. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

7. **Cache prompt yang lebih pendek:** Panjang prompt minimum yang dapat di-cache di Claude Opus 5 adalah 512 token, lebih rendah daripada model Opus sebelumnya. Prompt yang sebelumnya terlalu pendek untuk di-cache kini dapat membuat entri cache, tanpa perlu perubahan kode. Lihat [Caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

8. **Ubah alat di tengah percakapan (beta):** Anda dapat menambah atau menghapus alat di antara giliran percakapan tanpa membatalkan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran sebelumnya. Kirim header beta `mid-conversation-tool-changes-2026-07-01`. Ini berguna untuk beban kerja agentic yang mengekspos alat secara bertahap atau menghentikannya seiring kemajuan tugas; tanpanya, daftar alat yang berubah akan membatalkan prefiks yang di-cache.

9. **Hapus instruksi verifikasi yang terbawa dan batasi cakupan:** Claude Opus 5 memverifikasi pekerjaannya sendiri tanpa perlu diberi tahu, jadi hapus instruksi verifikasi atau pemeriksaan mandiri eksplisit yang terbawa dari prompt yang disetel untuk model sebelumnya; membiarkannya akan menyebabkan verifikasi berlebihan. Untuk tugas yang sempit, batasi cakupan tugas secara eksplisit. Lihat [Cakupan tugas dan verifikasi berlebihan](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-opus-5#task-scope-and-over-verification).

#### Daftar periksa migrasi

* Perbarui nama model dari `claude-opus-4-6` ke `claude-opus-5` (atau perbarui alias).
* Hapus `temperature`, `top_p`, dan `top_k` dari payload permintaan.
* Ganti `thinking: {type: "enabled", budget_tokens: N}` dengan `thinking: {type: "adaptive"}` ditambah [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort), atau hapus field `thinking` sepenuhnya; adaptive thinking aktif secara default di Claude Opus 5.
* Tinjau beban kerja yang berjalan tanpa field `thinking`: beban kerja tersebut berjalan dengan thinking di Claude Opus 5. Tinjau kembali `max_tokens`, yang tetap menjadi batas keras pada total output (thinking ditambah teks respons), atau kirimkan `thinking: {type: "disabled"}` pada effort `high` atau lebih rendah untuk mempertahankan perilaku lama.
* Audit permintaan yang menonaktifkan thinking: `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400, yang diberlakukan pada setiap permintaan. Aktifkan kembali thinking atau turunkan effort ke `high` atau lebih rendah.
* Hapus semua prefill pesan asisten.
* Jika UI Anda menampilkan konten thinking, pilih secara eksplisit untuk mengaktifkan peringkasan thinking.
* Lakukan benchmark ulang biaya dan latensi end-to-end di bawah tokenisasi yang diperbarui.
* Setel ulang `max_tokens` untuk memperhitungkan tokenisasi yang diperbarui.
* Uji ulang semua estimasi jumlah token sisi klien.
* Jika aplikasi Anda mengirim gambar, anggarkan ulang untuk [dukungan gambar resolusi tinggi](https://platform.claude.com/docs/id/build-with-claude/vision#high-resolution-image-support-on-claude-opus-4-7) (hingga sekitar 3x lebih banyak token gambar per gambar resolusi penuh). Lakukan downsample sebelum mengirim jika Anda tidak memerlukan fidelitas tambahan.
* Jika Anda menggunakan koordinat penunjukan atau bounding-box dari model, hapus semua konversi faktor skala; koordinat bersifat 1:1 dengan piksel gambar sebenarnya di Claude Opus 4.7 dan model yang lebih baru.
* Tinjau prompt untuk perubahan perilaku (panjang respons, keharfiahan, nada, pembaruan progres, subagen, kalibrasi effort, pemicuan alat, pengaman siber, penanganan gambar resolusi tinggi).
* Tetapkan ulang baseline panjang respons dengan prompt kontrol panjang yang ada dihapus, lalu setel secara eksplisit.
* Jika menggunakan effort `xhigh` atau `max`, naikkan `max_tokens` ke setidaknya 64k sebagai titik awal.
* Pertimbangkan untuk mengadopsi task budget (beta) dan perubahan alat di tengah percakapan (beta) untuk alur kerja agentic.
* Tangani `stop_reason: "refusal"`, dan pertimbangkan `fallbacks: "default"` (beta) untuk menjalankan ulang permintaan yang ditolak pada model fallback yang direkomendasikan secara otomatis.
* Tinjau prompt yang mendekati minimum caching: prompt dengan 512 token atau lebih kini dapat membuat entri cache di Claude Opus 5.
* Jika Anda menggunakan [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool), rencanakan alternatif: fitur ini tidak tersedia di Claude Opus 5.
* Jika organisasi Anda memiliki komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models), perhatikan bahwa Priority Tier tidak didukung di Claude Opus 5.
* Hapus instruksi verifikasi dan pemeriksaan mandiri yang terbawa dari prompt yang disetel untuk model sebelumnya; instruksi tersebut menyebabkan verifikasi berlebihan di Claude Opus 5.
* Jika produk Anda melakukan pekerjaan keamanan yang sah, ajukan permohonan ke [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet) untuk akses ke pembatasan yang lebih rendah pada konten siber.

#### Bermigrasi dari Claude Opus 4.5 atau sebelumnya

Jika Anda bermigrasi dari Claude Opus 4.5, Opus 4.1, atau model sebelumnya langsung ke Claude Opus 5, terapkan **semua perubahan sebelumnya di bagian ini** ditambah perubahan kumulatif berikut, yang mulai berlaku antara Opus 4.5 dan Opus 4.7. Jika Anda bermigrasi dari Opus 4.6, perubahan sebelumnya di bagian ini adalah semua yang Anda butuhkan.

##### Perbarui nama model Anda

```python
# Migrasi Opus
model = "claude-opus-4-5"  # Before
model = "claude-opus-5"  # After
```

##### Perubahan yang merusak kompatibilitas

1. **Penghapusan prefill** dibahas dalam [perubahan yang merusak kompatibilitas untuk bermigrasi dari Claude Opus 4.6](https://platform.claude.com/docs/id/about-claude/models/migration-guide#opus-46-breaking-changes).

2. **Pengutipan parameter alat:** Claude Opus 4.6 dan model yang lebih baru mungkin menghasilkan escaping string JSON yang sedikit berbeda dalam argumen pemanggilan alat (misalnya, penanganan escape Unicode atau escaping garis miring yang berbeda). Jika Anda mem-parse `input` pemanggilan alat sebagai string mentah alih-alih menggunakan parser JSON, verifikasi logika parsing Anda. Parser JSON standar (seperti `json.loads()` atau `JSON.parse()`) menangani perbedaan ini secara otomatis.

##### Perubahan yang direkomendasikan

Perubahan ini meningkatkan pengalaman Anda di Claude Opus 4.7 dan model yang lebih baru. Butir yang ditandai **(wajib di Opus 4.7)** merupakan rekomendasi opsional saat Opus 4.6 diluncurkan tetapi kini wajib; sisanya tetap direkomendasikan.

1. **Bermigrasi ke adaptive thinking (wajib di Opus 4.7):** `thinking: {type: "enabled", budget_tokens: N}` mengembalikan error 400 di Claude Opus 4.7 dan model yang lebih baru. Beralihlah ke `thinking: {type: "adaptive"}` dan gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking; di Claude Opus 5, `thinking: {type: "adaptive"}` setara dengan menghilangkan field `thinking`, yang berjalan dengan adaptive thinking secara default. Lihat [Thinking](https://platform.claude.com/docs/id/build-with-claude/thinking).

   <CodeGroup>
     ```bash cURL
     curl -sS https://api.anthropic.com/v1/messages \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d '{
         "model": "claude-opus-5",
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
         model="claude-opus-5",
         max_tokens=16000,
         thinking={"type": "adaptive"},
         output_config={"effort": "high"},
         messages=[{"role": "user", "content": "Your prompt here"}],
     )
     ```

     ```bash CLI
     ant messages create <<'YAML'
     model: claude-opus-5
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
       model: "claude-opus-5",
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
         Model = Model.ClaudeOpus5,
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
     	Model:     anthropic.ModelClaudeOpus5,
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
                 .model(Model.CLAUDE_OPUS_5)
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
         model: 'claude-opus-5',
         thinking: ['type' => 'adaptive'],
         outputConfig: ['effort' => 'high'],
     );
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     response = client.messages.create(
       model: "claude-opus-5",
       max_tokens: 16000,
       thinking: { type: "adaptive" },
       output_config: { effort: "high" },
       messages: [{ role: "user", content: "Your prompt here" }]
     )
     ```
   </CodeGroup>

   Perhatikan bahwa migrasi ini juga berpindah dari `client.beta.messages.create` ke `client.messages.create`. Adaptive thinking dan effort tidak memerlukan namespace SDK beta atau header beta apa pun.

2. **Hapus header beta effort:** Parameter effort tidak memerlukan header beta. Hapus `betas=["effort-2025-11-24"]` dari permintaan Anda.

3. **Hapus header beta fine-grained tool streaming:** Fine-grained tool streaming tidak memerlukan header beta. Hapus `betas=["fine-grained-tool-streaming-2025-05-14"]` dari permintaan Anda.

4. **Hapus header beta interleaved thinking:** Adaptive thinking secara otomatis mengaktifkan interleaved thinking di Claude Opus 4.7, Opus 4.6, dan Sonnet 4.6. Hapus `betas=["interleaved-thinking-2025-05-14"]` dari permintaan Anda. Header ini masih berfungsi di Sonnet 4.6 dengan pemikiran diperpanjang manual, tetapi mode manual sudah deprecated.

5. **Bermigrasi ke output\_config.format:** Jika menggunakan structured outputs, perbarui `output_format={...}` menjadi `output_config={"format": {...}}`. API masih menerima parameter `output_format` yang deprecated, tetapi parameter ini akan dihapus dalam rilis model mendatang. Python SDK (v1.0 dan yang lebih baru) tidak menerima `output_format={...}` pada `client.beta.messages.create()` atau `count_tokens()`. Argumen `output_format=Model` dari helper `parse()` dan `stream()` tidak berubah.

#### Bermigrasi dari Claude 4.1 atau sebelumnya

Jika Anda bermigrasi dari Opus 4.1 atau model sebelumnya langsung ke Claude Opus 5, terapkan semua perubahan sebelumnya di bagian ini, ditambah perubahan tambahan di sub-bagian ini.

```python
# Dari Opus 4.1
model = "claude-opus-4-1-20250805"  # Before
model = "claude-opus-5"  # After

# Dari Sonnet 3.7
model = "claude-3-7-sonnet-20250219"  # Before
model = "claude-opus-5"  # After
```

##### Perubahan tambahan yang merusak kompatibilitas

1. **Hapus parameter sampling**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
   </Warning>

   Mulai dari Claude Opus 4.7, mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default apa pun mengembalikan error 400. Python SDK (v1.0 dan yang lebih baru) tidak mendefinisikannya, dan mengirimkannya akan memunculkan `TypeError`. Jalur migrasi paling aman adalah menghilangkan parameter ini sepenuhnya dari permintaan, dan menggunakan prompting untuk memandu perilaku model. Jika Anda sebelumnya menggunakan `temperature = 0` untuk determinisme, perhatikan bahwa hal itu tidak pernah menjamin output yang identik.

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
         model="claude-opus-5",
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
       model: "claude-opus-5"
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
         Model = "claude-opus-5",
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
     	Model: "claude-opus-5",
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
         .model("claude-opus-5")
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
         model: 'claude-opus-5',
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
       model: "claude-opus-5",
       # ...
     )
     ```
   </CodeGroup>

2. **Perbarui versi alat**

   <Warning>
     Ini adalah perubahan yang merusak kompatibilitas saat bermigrasi dari model Claude 3.x.
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

   * **Editor teks:** Gunakan `text_editor_20250728` dan `str_replace_based_edit_tool`. Lihat dokumentasi [Alat editor teks](https://platform.claude.com/docs/id/agents-and-tools/tool-use/text-editor-tool) untuk detailnya.
   * **Eksekusi kode:** Upgrade ke `code_execution_20260521`. Lihat dokumentasi [Alat eksekusi kode](https://platform.claude.com/docs/id/agents-and-tools/tool-use/code-execution-tool#upgrade-to-latest-tool-version) untuk instruksi migrasi.

3. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals):

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

   Model Claude 4.5+ mengembalikan stop reason `model_context_window_exceeded` ketika pembuatan berhenti karena mencapai batas jendela konteks, bukan batas `max_tokens` yang diminta. Perbarui aplikasi Anda untuk menangani stop reason baru ini:

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

5. **Verifikasi penanganan parameter alat (newline di akhir)**

   Model Claude 4.5+ mempertahankan newline di akhir dalam parameter string pemanggilan alat yang sebelumnya dihapus. Jika alat Anda mengandalkan pencocokan string yang persis terhadap parameter pemanggilan alat, verifikasi bahwa logika Anda menangani newline di akhir dengan benar.

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4+ memiliki gaya komunikasi yang lebih ringkas dan langsung serta memerlukan arahan eksplisit. Tinjau [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

##### Perubahan tambahan yang direkomendasikan

* **Hapus header beta lama:** Hapus `token-efficient-tools-2025-02-19` dan `output-128k-2025-02-19`. Semua model Claude 4+ memiliki penggunaan alat hemat token bawaan dan header ini tidak berpengaruh.

#### Daftar periksa migrasi (dari Claude Opus 4.5 atau sebelumnya)

* Perbarui ID model ke `claude-opus-5`
* Terapkan semua [perubahan yang merusak kompatibilitas untuk bermigrasi dari Claude Opus 4.6](https://platform.claude.com/docs/id/about-claude/models/migration-guide#opus-46-breaking-changes) (pemikiran diperpanjang dihapus, thinking aktif secara default, batas effort untuk menonaktifkan thinking, parameter sampling dihapus, tampilan thinking dihilangkan secara default, tokenisasi diperbarui)
* **MERUSAK KOMPATIBILITAS:** Hapus prefill pesan asisten (mengembalikan error 400); gunakan structured outputs atau `output_config.format` sebagai gantinya
* **MERUSAK KOMPATIBILITAS di Opus 4.7:** Ganti `thinking: {type: "enabled", budget_tokens: N}` dengan `thinking: {type: "adaptive"}` ditambah [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) (mengembalikan 400 di Opus 4.7)
* Verifikasi bahwa parsing JSON pemanggilan alat menggunakan parser JSON standar
* Hapus header beta `effort-2025-11-24` (parameter effort tidak memerlukannya)
* Hapus header beta `fine-grained-tool-streaming-2025-05-14`
* Hapus header beta `interleaved-thinking-2025-05-14` (adaptive thinking mengaktifkan interleaved thinking secara otomatis)
* Migrasikan `output_format` ke `output_config.format` (jika berlaku)
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: hapus `temperature`, `top_p`, dan `top_k` (nilai non-default mengembalikan 400 di Opus 4.7)
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: perbarui versi alat (`text_editor_20250728`, `code_execution_20260521`)
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: tangani stop reason `refusal`
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: tangani stop reason `model_context_window_exceeded`
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: verifikasi penanganan parameter string alat untuk newline di akhir
* Jika bermigrasi dari Claude 4.1 atau sebelumnya: hapus header beta lama (`token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`)
* Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
* Uji di lingkungan pengembangan sebelum deployment produksi

### Migrasi ke Claude Opus 5 dari Claude Sonnet 5

Claude Opus 5 dan Claude Sonnet 5 berbagi permukaan API yang sama: keduanya berjalan dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) aktif secara default, keduanya menetapkan default [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) ke `high` pada Claude API dan Claude Code, keduanya melayani ["context window" (jendela konteks) 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default dengan [128k token output maksimum](https://platform.claude.com/docs/id/about-claude/models/overview), dan keduanya tidak mendukung [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models). "Extended thinking" (pemikiran diperpanjang) manual dan parameter sampling non-default mengembalikan error 400 pada kedua model, begitu pula prefill asisten.

#### Perbarui nama model Anda

```python
model = "claude-sonnet-5"  # Before
model = "claude-opus-5"  # After
```

#### Apa yang berubah

1. **Harga:** Claude Opus 5 dihargai $5 per juta token input dan $25 per juta token output. Claude Sonnet 5 dihargai $2/$10 per juta token input/output. Lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing) untuk harga lengkap.

2. **Menonaktifkan thinking dibatasi pada effort `high`:** Pada Claude Sonnet 5, `thinking: {type: "disabled"}` diterima pada level effort apa pun. Pada Claude Opus 5, ini hanya diterima pada level [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau di bawahnya; permintaan yang menggabungkan `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400, yang diberlakukan pada setiap permintaan. Audit permintaan yang menonaktifkan thinking sebelum Anda bermigrasi.

3. **Pesan sistem di tengah percakapan:** Claude Opus 5 menerima pesan `role: "system"` tepat setelah giliran pengguna dalam array `messages` (tunduk pada [aturan penempatan](https://platform.claude.com/docs/id/build-with-claude/mid-conversation-system-messages#limitations)). Fitur ini tidak tersedia pada Claude Sonnet 5; gunakan field `system` tingkat atas sebagai gantinya. Jika Anda memelihara jalur kode yang membangun ulang seluruh riwayat pesan untuk memperbarui instruksi, Anda dapat menyederhanakannya dan mempertahankan hit [cache prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching) pada giliran-giliran sebelumnya.

4. **Web fetch tidak tersedia:** Alat [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool) tersedia pada Claude Sonnet 5 tetapi tidak pada Claude Opus 5.

#### Daftar periksa migrasi

* Perbarui nama model dari `claude-sonnet-5` ke `claude-opus-5`.
* Audit permintaan yang menonaktifkan thinking: `thinking: {type: "disabled"}` dengan effort `xhigh` atau `max` mengembalikan error 400 pada Claude Opus 5. Aktifkan kembali thinking atau turunkan effort ke `high` atau di bawahnya.
* Jika Anda menggunakan [web fetch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/web-fetch-tool), rencanakan alternatif: alat ini tidak tersedia pada Claude Opus 5.
* Jalankan ulang [token counting](https://platform.claude.com/docs/id/build-with-claude/token-counting) (penghitungan token) terhadap Claude Opus 5 alih-alih menggunakan kembali hitungan yang diukur terhadap Claude Sonnet 5, dan tetapkan ulang baseline biaya dan latensi pada beban kerja Anda sendiri; harga per token berbeda.

***

## Migrasi ke Claude Sonnet 5

Claude Sonnet 5 menawarkan kombinasi terbaik antara kecepatan dan kecerdasan dalam keluarga model Claude. Model ini dibangun di atas Claude Sonnet 4.6.

Claude Sonnet 5 adalah peningkatan drop-in untuk Claude Sonnet 4.6, dengan harga $2/$10 USD per juta token input/output; lihat [Harga](https://platform.claude.com/docs/id/about-claude/pricing) untuk detailnya. Ada dua perubahan API yang bersifat breaking untuk kode yang sudah berjalan pada Claude Sonnet 4.6: extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) dan parameter sampling (`temperature`, `top_p`, `top_k`) yang diatur ke nilai non-default tidak lagi diterima dan mengembalikan error 400. Gunakan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) dengan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) sebagai gantinya. Claude Sonnet 5 mendukung rangkaian fitur yang sama dengan Claude Sonnet 4.6, termasuk [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows), [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking), ["prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching), [pemrosesan batch](https://platform.claude.com/docs/id/build-with-claude/batch-processing), [Files API](https://platform.claude.com/docs/id/build-with-claude/files), [dukungan PDF](https://platform.claude.com/docs/id/build-with-claude/pdf-support), [vision](https://platform.claude.com/docs/id/build-with-claude/vision), dan rangkaian lengkap [alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) sisi server dan sisi klien. Pada Claude API, Claude Sonnet 5 juga mendukung [computer use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool) (penggunaan komputer) sebagai toolset stabil `computer_toolset_20260801` dan [alat browser use](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) untuk tugas di dalam halaman web, yang keduanya tidak didukung oleh Claude Sonnet 4.6; integrasi yang sudah ada pada versi `computer_20251124` sebelumnya tetap berfungsi tanpa perubahan pada kedua model. Untuk meningkatkan integrasi yang sudah ada, lihat [Migrasi dari `computer_20251124`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124). [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) tidak tersedia pada Claude Sonnet 5. Claude Sonnet 5 juga menggunakan tokenizer baru.

### Migrasi ke Claude Sonnet 5 dari Claude Sonnet 4.6

<Note>
  Jika kode Anda menggunakan Claude Sonnet 4.5 atau yang lebih lama, terapkan juga [Migrasi ke Claude Sonnet 5 dari Claude Sonnet 4.5 dan model Sonnet yang lebih lama](https://platform.claude.com/docs/id/about-claude/models/migration-guide#migrating-from-sonnet-45). Langkah-langkah tersebut mencakup perubahan breaking (prefill pesan asisten ditolak, perbedaan escaping JSON parameter alat) yang tidak dicakup oleh bagian ini saja.
</Note>

#### Perbarui nama model Anda

```python
# Migrasi Sonnet
model = "claude-sonnet-4-6"  # Before
model = "claude-sonnet-5"  # After
```

#### Apa yang berubah

Butir 4 dan 5 dalam daftar berikut adalah perubahan breaking. `max_tokens` tetap menjadi batas keras pada total output (thinking ditambah teks respons), jadi tinjau kembali nilainya untuk beban kerja yang berjalan tanpa thinking pada Claude Sonnet 4.6.

1. **Tokenizer baru:** Claude Sonnet 5 menggunakan tokenizer baru. Teks input yang sama menghasilkan sekitar 30% lebih banyak token dibandingkan pada Claude Sonnet 4.6. Peningkatan pastinya bergantung pada konten. Permintaan, respons, dan event streaming tetap memiliki bentuk yang sama, dan tidak diperlukan perubahan kode, tetapi apa pun yang Anda ukur atau anggarkan dalam token akan bergeser: field `usage` dan hasil [token counting](https://platform.claude.com/docs/id/build-with-claude/token-counting) untuk teks yang sama menjadi lebih tinggi, jendela konteks 1M token menampung lebih sedikit teks, dan batas `max_tokens` yang disetel untuk Claude Sonnet 4.6 mungkin memotong output yang setara. Harga per token lebih rendah ($2/$10 dibandingkan $3/$15 per juta token input/output pada Claude Sonnet 4.6), tetapi biaya permintaan yang setara tidak turun secara proporsional langsung. Jalankan ulang token counting terhadap Claude Sonnet 5 alih-alih menggunakan kembali hitungan yang diukur terhadap model sebelumnya.

2. **128k token output maksimum (tidak berubah):** Claude Sonnet 5 mendukung hingga 128k token output, sama seperti Claude Sonnet 4.6. Nilai `max_tokens` yang sudah ada tetap valid. Perhitungkan tokenizer baru saat menentukan ukurannya.

3. **Prefill pesan asisten (tidak berubah):** Melakukan prefill pada pesan asisten mengembalikan error `400` pada Claude Sonnet 5, sama seperti pada Claude Sonnet 4.6. Jika Anda telah menghapus prefill saat bermigrasi ke Claude Sonnet 4.6, tidak diperlukan perubahan lebih lanjut. Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) (output terstruktur), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

4. **Adaptive thinking aktif secara default:** Pada Claude Sonnet 4.6, permintaan tanpa field `thinking` berjalan tanpa thinking; pada Claude Sonnet 5, permintaan yang sama berjalan dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking). Untuk mematikan thinking, kirimkan `thinking: {type: "disabled"}`. Extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung dan mengembalikan error 400. Gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) (default `high`) untuk mengontrol kedalaman thinking.

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

6. **Pengaman keamanan siber:** Claude Sonnet 5 adalah model tingkat Sonnet pertama dengan pengaman keamanan siber real-time. Permintaan yang melibatkan topik keamanan siber yang dilarang atau berisiko tinggi mungkin ditolak. Penolakan dikembalikan sebagai respons HTTP 200 yang berhasil dengan `stop_reason: "refusal"`, bukan sebagai error. Lihat [Pengaman siber real-time pada Claude Opus dan Sonnet](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet) untuk mengetahui apa yang diblokir oleh pengaman tersebut dan bagaimana pekerjaan keamanan yang sah dapat mendaftar ke Cyber Verification Program.

#### Daftar periksa migrasi

* Perbarui nama model dari `claude-sonnet-4-6` ke `claude-sonnet-5`.
* Jalankan ulang [token counting](https://platform.claude.com/docs/id/build-with-claude/token-counting) terhadap Claude Sonnet 5. Tokenizer baru menghasilkan sekitar 30% lebih banyak token untuk teks yang sama, yang dapat mengubah biaya per permintaan meskipun harga per token lebih rendah. Peningkatan pastinya bergantung pada konten dan bentuk beban kerja.
* Tinjau kembali batas `max_tokens` yang ukurannya mendekati panjang output yang Anda harapkan, dan naikkan hingga maksimum 128k (tidak berubah dari Claude Sonnet 4.6) jika berguna.
* Hapus konfigurasi `thinking: {type: "enabled", budget_tokens: N}` (mengembalikan error 400). Adaptive thinking aktif secara default; kirimkan `{type: "disabled"}` untuk mematikannya, atau gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman.
* Hapus parameter `temperature`, `top_p`, dan `top_k` yang diatur ke nilai non-default (parameter ini mengembalikan error 400 pada Claude Sonnet 5).
* Tambahkan penanganan untuk `stop_reason: "refusal"` jika beban kerja Anda mungkin menyentuh topik keamanan siber.
* Tetapkan ulang baseline biaya pada beban kerja tipikal Anda sebelum deployment produksi.
* Tinjau `max_tokens` untuk beban kerja yang sebelumnya berjalan tanpa thinking.

### Migrasi ke Claude Sonnet 5 dari Claude Sonnet 4.5 dan model Sonnet yang lebih lama

Jika Anda bermigrasi dari Claude Sonnet 4.5 atau model Sonnet yang lebih lama langsung ke Claude Sonnet 5, terapkan perubahan [Migrasi ke Claude Sonnet 5 dari Claude Sonnet 4.6](https://platform.claude.com/docs/id/about-claude/models/migration-guide#migrating-from-claude-sonnet-4-6-to-claude-sonnet-5) ditambah perubahan dalam bagian ini.

<Warning>
  Claude Sonnet 5 menggunakan level effort default `high`, berbeda dengan Sonnet 4.5 yang tidak memiliki parameter effort. Pertimbangkan untuk menyesuaikan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) saat Anda bermigrasi. Jika tidak diatur secara eksplisit, Anda mungkin mengalami latensi yang lebih tinggi dengan level effort default.
</Warning>

#### Perubahan breaking

##### Saat bermigrasi dari Sonnet 4.5

1. **Prefill pesan asisten tidak lagi didukung**

   <Warning>
     Ini adalah perubahan breaking saat bermigrasi dari Sonnet 4.5 atau yang lebih lama.
   </Warning>

   Melakukan prefill pada pesan asisten mengembalikan error `400` pada Claude Sonnet 4.6 dan model yang lebih baru, termasuk Claude Sonnet 5. Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

   **Kasus penggunaan prefill yang umum dan migrasinya:**

   * **Mengontrol format output** (memaksa output JSON/YAML): Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs) atau alat dengan field enum untuk tugas klasifikasi.

   * **Menghilangkan pembukaan** (menghapus frasa "Here is..."): Tambahkan instruksi langsung dalam prompt sistem: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc."

   * **Menghindari penolakan yang buruk:** Claude kini jauh lebih baik dalam melakukan penolakan yang tepat. Prompting yang jelas dalam pesan pengguna tanpa prefill seharusnya sudah cukup.

   * **Kelanjutan** (melanjutkan respons yang terputus): Pindahkan kelanjutan ke pesan pengguna: "Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off."

   * **Hidrasi konteks / konsistensi peran** (menyegarkan konteks dalam percakapan panjang): Sisipkan apa yang sebelumnya merupakan pengingat asisten yang di-prefill ke dalam giliran pengguna sebagai gantinya.

2. **Escaping JSON parameter alat mungkin berbeda**

   <Warning>
     Ini adalah perubahan breaking saat bermigrasi dari Sonnet 4.5 atau yang lebih lama.
   </Warning>

   Escaping string JSON dalam parameter alat mungkin berbeda dari model sebelumnya. Parser JSON standar menangani hal ini secara otomatis, tetapi parsing berbasis string kustom mungkin perlu diperbarui.

**Perubahan extended thinking:** Konfigurasi `budget_tokens` dari Claude Sonnet 4.5 (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung pada Claude Sonnet 5 dan mengembalikan error 400. Adaptive thinking aktif secara default, sehingga sebagian besar beban kerja tidak memerlukan konfigurasi `thinking` sama sekali; gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking. Jika Anda menjalankan Claude Sonnet 4.5 tanpa extended thinking, kirimkan `thinking: {type: "disabled"}` untuk mempertahankan perilaku tersebut.

##### Saat bermigrasi dari Claude 3.x

3. **Hapus parameter sampling**

   <Warning>
     Ini adalah perubahan breaking saat bermigrasi dari model Claude 3.x.
   </Warning>

   Parameter sampling (`temperature`, `top_p`, `top_k`) yang diatur ke nilai non-default mengembalikan error 400 pada Claude Sonnet 5. Hapus parameter tersebut dari permintaan, dan gunakan prompting untuk memandu perilaku model sebagai gantinya.

4. **Perbarui versi alat**

   <Warning>
     Ini adalah perubahan breaking saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20260521`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

5. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

6. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

### Migrasi ke Claude Sonnet 5 dari Claude Haiku 4.5

Claude Haiku 4.5 dan Claude Sonnet 5 lebih berbeda di tingkat API dibandingkan model-model yang berdekatan dalam satu kelas: Claude Haiku 4.5 menggunakan [extended thinking](https://platform.claude.com/docs/id/build-with-claude/extended-thinking) manual (nonaktif secara default), jendela konteks 200k token, dan hingga 64k token output, sedangkan Claude Sonnet 5 berjalan dengan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) aktif secara default, melayani [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, dan mendukung hingga [128k token output](https://platform.claude.com/docs/id/about-claude/models/overview).

#### Perbarui nama model Anda

```python
model = "claude-haiku-4-5-20251001"  # Before
model = "claude-sonnet-5"  # After
```

#### Apa yang berubah

1. **Konfigurasi thinking:** Claude Haiku 4.5 mendukung extended thinking manual (`thinking: {type: "enabled", budget_tokens: N}`) dan menolak `thinking: {type: "adaptive"}`. Pada Claude Sonnet 5, dukungannya terbalik: adaptive thinking aktif secara default, dan extended thinking manual mengembalikan error 400. Hapus konfigurasi `thinking: {type: "enabled", budget_tokens: N}` dan andalkan default, atau kirimkan `thinking: {type: "disabled"}` untuk mematikan thinking. `budget_tokens` tidak memiliki pengganti langsung; gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking. Effort tidak tersedia pada Claude Haiku 4.5 dan default-nya `high` pada Claude Sonnet 5.

2. **Parameter sampling dihapus:** `temperature` dan `top_p` berfungsi pada Claude Haiku 4.5 (satu per satu, tidak keduanya). Pada Claude Sonnet 5, mengatur `temperature`, `top_p`, atau `top_k` ke nilai non-default mengembalikan error 400. Hapus parameter ini dan gunakan prompting untuk memandu perilaku model.

3. **Prefill asisten dihapus:** Melakukan prefill pada pesan asisten berfungsi pada Claude Haiku 4.5 tetapi mengembalikan error 400 pada Claude Sonnet 5. Gunakan [structured outputs](https://platform.claude.com/docs/id/build-with-claude/structured-outputs), instruksi prompt sistem, atau `output_config.format` sebagai gantinya.

4. **Jendela konteks dan output yang lebih besar:** Claude Sonnet 5 melayani jendela konteks 1M token secara default, naik dari 200k token pada Claude Haiku 4.5, dan mendukung hingga 128k token output, naik dari 64k. Claude Sonnet 5 juga menggunakan tokenizer yang berbeda, jadi jalankan ulang [token counting](https://platform.claude.com/docs/id/build-with-claude/token-counting) alih-alih menggunakan kembali hitungan yang diukur terhadap Claude Haiku 4.5.

5. **Harga:** Claude Haiku 4.5 dihargai $1/$5 per juta token input/output. Claude Sonnet 5 dihargai $2/$10 per juta token input/output. Lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).

6. **Pengaman keamanan siber:** Claude Sonnet 5 memiliki pengaman keamanan siber real-time. Permintaan yang melibatkan topik keamanan siber yang dilarang atau berisiko tinggi mungkin ditolak, dikembalikan sebagai respons HTTP 200 yang berhasil dengan `stop_reason: "refusal"`. Lihat [Pengaman siber real-time pada Claude Opus dan Sonnet](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet) untuk mengetahui apa yang diblokir oleh pengaman tersebut dan bagaimana pekerjaan keamanan yang sah dapat mendaftar ke Cyber Verification Program.

#### Daftar periksa migrasi

* Perbarui nama model dari `claude-haiku-4-5-20251001` (atau alias `claude-haiku-4-5`) ke `claude-sonnet-5`.
* Hapus konfigurasi `thinking: {type: "enabled", budget_tokens: N}` (mengembalikan error 400). Adaptive thinking aktif secara default; kirimkan `thinking: {type: "disabled"}` untuk mempertahankan perilaku tanpa thinking, dan tinjau kembali `max_tokens` untuk beban kerja yang berjalan tanpa thinking.
* Gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) (default `high`) untuk mengontrol kedalaman thinking dan pengeluaran token; parameter ini tidak tersedia pada Claude Haiku 4.5, sehingga tidak ada pengaturan yang sudah ada yang terbawa.
* Hapus pengaturan `temperature` dan `top_p` (nilai non-default mengembalikan error 400 pada Claude Sonnet 5).
* Hapus semua prefill pesan asisten (prefill mengembalikan error 400 pada Claude Sonnet 5).
* Jalankan ulang [token counting](https://platform.claude.com/docs/id/build-with-claude/token-counting) terhadap Claude Sonnet 5, dan tinjau kembali batas `max_tokens`, yang dapat Anda naikkan hingga maksimum 128k.
* Tambahkan penanganan untuk `stop_reason: "refusal"` jika beban kerja Anda mungkin menyentuh topik keamanan siber.
* Tetapkan ulang baseline biaya pada beban kerja tipikal Anda sebelum deployment produksi; harga per token berbeda.

***

## Migrasi ke Claude Haiku 4.5

Claude Haiku 4.5 adalah model Haiku tercepat dan paling cerdas dengan performa mendekati frontier, menghadirkan kualitas model premium untuk aplikasi interaktif dan pemrosesan bervolume tinggi.

Untuk gambaran lengkap kemampuannya, lihat [ikhtisar model](https://platform.claude.com/docs/id/about-claude/models/overview).

<Note>
  Untuk harga Claude Haiku 4.5, lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).
</Note>

<Tip>
  Untuk peningkatan performa yang signifikan pada tugas coding dan penalaran, pertimbangkan untuk mengaktifkan extended thinking dengan `thinking: {type: "enabled", budget_tokens: N}`.
</Tip>

<Note>
  Extended thinking memengaruhi efisiensi [caching prompt](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#caching-with-thinking-blocks).

  Extended thinking sudah deprecated pada model Claude 4.6 dan dihapus pada Claude Opus 4.7. Jika menggunakan model yang lebih baru, gunakan [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) sebagai gantinya.
</Note>

### Migrasi ke Claude Haiku 4.5 dari Claude Haiku 3.5 dan model Haiku yang lebih lama

**Perbarui nama model Anda:**

```python
# Dari Haiku 3.5
model = "claude-3-5-haiku-20241022"  # Before
model = "claude-haiku-4-5-20251001"  # After
```

**Tinjau batas laju baru:** Haiku 4.5 memiliki "rate limit" (batas laju) yang terpisah dari Haiku 3.5. Lihat dokumentasi [Batas laju](https://platform.claude.com/docs/id/api/rate-limits) untuk detailnya.

**Jelajahi kemampuan baru:** Lihat [ikhtisar model](https://platform.claude.com/docs/id/about-claude/models/overview) untuk detail tentang kesadaran konteks, kapasitas output yang lebih besar (64k token), kecerdasan yang lebih tinggi, dan kecepatan yang lebih baik.

#### Perubahan breaking

Perubahan breaking ini berlaku saat bermigrasi dari model Claude 3.x Haiku.

1. **Perbarui parameter sampling**

   <Warning>
     Ini adalah perubahan breaking saat bermigrasi dari model Claude 3.x.
   </Warning>

   Gunakan hanya `temperature` ATAU `top_p`, tidak keduanya. Mengatur keduanya mengembalikan error 400 pada Claude Haiku 4.5.

2. **Perbarui versi alat**

   <Warning>
     Ini adalah perubahan breaking saat bermigrasi dari model Claude 3.x.
   </Warning>

   Perbarui ke versi alat terbaru (`text_editor_20250728`, `code_execution_20250825`). Hapus kode apa pun yang menggunakan perintah `undo_edit`.

3. **Tangani stop reason `refusal`**

   Perbarui aplikasi Anda untuk [menangani stop reason `refusal`](https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals).

4. **Perbarui prompt Anda untuk perubahan perilaku**

   Model Claude 4 memiliki gaya komunikasi yang lebih ringkas dan langsung. Tinjau [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices) untuk panduan optimasi.

#### Daftar periksa migrasi Haiku 4.5

* Perbarui ID model ke `claude-haiku-4-5-20251001`
* **BREAKING:** Perbarui versi alat ke yang terbaru (`text_editor_20250728`, `code_execution_20250825`); versi lama tidak didukung
* **BREAKING:** Hapus kode apa pun yang menggunakan perintah `undo_edit` (jika berlaku)
* **BREAKING:** Perbarui parameter sampling agar hanya menggunakan `temperature` ATAU `top_p`, tidak keduanya (mengatur keduanya mengembalikan error 400)
* Tangani stop reason `refusal` baru dalam aplikasi Anda
* Tinjau dan sesuaikan dengan batas laju baru (terpisah dari Haiku 3.5)
* Tinjau dan perbarui prompt mengikuti [praktik terbaik prompting](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/claude-prompting-best-practices)
* Pertimbangkan untuk mengaktifkan extended thinking untuk tugas penalaran yang kompleks
* Uji di lingkungan pengembangan sebelum deployment produksi

***

## Dapatkan bantuan

* Periksa [dokumentasi API](https://platform.claude.com/docs/id/api/overview) untuk spesifikasi terperinci
* Tinjau [kemampuan model](https://platform.claude.com/docs/id/about-claude/models/overview) untuk perbandingan performa
* Tinjau [catatan rilis API](https://platform.claude.com/docs/id/release-notes/api) untuk pembaruan API
* Hubungi dukungan jika Anda mengalami masalah apa pun selama migrasi
