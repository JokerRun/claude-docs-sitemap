---
source: platform
url: https://platform.claude.com/docs/id/models/fable-5/migration-guide
fetched_at: 2026-09-01T02:22:36.834082Z
sha256: 48aadeab8bf67754903244936e4df5d1732497dd85ff03d986afbee23d16e685
---

---
title: Migrasi ke Claude Mythos 5 dan Claude Fable 5
url: https://platform.claude.com/docs/id/models/fable-5/migration-guide
description: "Migrasi ke Claude Mythos 5 dan Claude Fable 5 dari Claude Mythos Preview, Claude Opus 5, atau Claude Opus 4.8: ID model, perubahan API, dan daftar periksa migrasi."
---

<Note>
  Panduan ini membahas migrasi kode [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages). Jika Anda menggunakan [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak ada perubahan yang diperlukan selain memperbarui nama model.
</Note>

<Tip>
  **Otomatiskan migrasi Anda dengan skill Claude API.** Di Claude Code, jalankan `/claude-api migrate` untuk memanggil [skill Claude API](https://platform.claude.com/docs/id/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model) bawaan. Skill ini berfungsi untuk model Claude terkini mana pun sebagai target:

  ```text wrap
  /claude-api migrate this project to claude-fable-5
  ```

  Skill ini menerapkan penggantian ID model dan, sesuai kebutuhan, perubahan parameter yang bersifat breaking, penggantian prefill, serta kalibrasi effort untuk model target Anda di seluruh basis kode Anda, lalu menghasilkan daftar periksa berisi item yang perlu diverifikasi secara manual. Skill ini meminta Anda mengonfirmasi cakupan migrasi (seluruh direktori kerja, sebuah subdirektori, atau daftar file tertentu) sebelum mengedit file apa pun. Skill ini juga mendeteksi klien Amazon Bedrock dan Claude Platform on AWS serta menyesuaikan format ID model dan perubahan fitur untuk platform tersebut.
</Tip>

[Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5) adalah model Anthropic paling mumpuni yang dirilis secara luas, tersedia di Claude API, [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai), dan [Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry). [Claude Mythos 5](https://anthropic.com/glasswing) memiliki kemampuan yang sama dan hanya ditawarkan kepada pelanggan yang disetujui dalam Project Glasswing.

Pengaturan dasar yang dimiliki bersama oleh `claude-fable-5` dan `claude-mythos-5`:

* **Thinking:** [Adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) (pemikiran adaptif) selalu aktif. Model menentukan kapan dan seberapa banyak berpikir pada setiap permintaan, dan tidak diperlukan konfigurasi `thinking`. Baik `thinking: {type: "disabled"}` maupun "extended thinking" (pemikiran diperpanjang) manual (`thinking: {type: "enabled", budget_tokens: N}`) mengembalikan error 400.
* **Prefill:** Melakukan prefill pada pesan asisten mengembalikan error 400. Gunakan instruksi "system prompt" (prompt sistem) sebagai gantinya.
* **Jendela konteks dan output:** ["Context window" (jendela konteks) 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) secara default, dan hingga 128k token output per permintaan.
* **Harga:** $10 USD per juta token input dan $50 USD per juta token output. Lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).
* **Retensi data:** Kedua model memerlukan retensi data 30 hari dan tidak tersedia di bawah pengaturan "zero data retention" (retensi data nol), atau ZDR; keduanya ditetapkan sebagai Covered Models. Di Claude API, permintaan ke Claude Fable 5 dari organisasi yang konfigurasi retensi datanya tidak memenuhi persyaratan ini mengembalikan `invalid_request_error` 400. Organisasi dengan pengaturan ZDR sebaiknya menghubungi tim akun Anthropic mereka untuk mendiskusikan konfigurasi retensi data. Sebagai alternatif, Anda dapat mengonfigurasi retensi data per workspace. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements) untuk detail per platform.

Perbedaan antara kedua model:

* **Ketersediaan:** Claude Fable 5 tidak memerlukan persetujuan akses. Claude Mythos 5 hanya tersedia bagi pelanggan yang disetujui dalam [Project Glasswing](https://anthropic.com/glasswing).
* **Pengklasifikasi keamanan:** Claude Fable 5 menjalankan "safety classifiers" (pengklasifikasi keamanan) yang dapat menolak permintaan dengan `stop_reason: "refusal"`. Claude Mythos 5 tidak menyertakan pengklasifikasi ini. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).
* **Priority Tier:** [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) didukung di Claude Fable 5 tetapi tidak di Claude Mythos 5.

## Migrasi ke Claude Mythos 5 dan Claude Fable 5 dari Claude Mythos Preview

[Claude Mythos 5](https://anthropic.com/glasswing) adalah penerus dengan akses terbatas dari [Claude Mythos Preview](https://anthropic.com/glasswing), pratinjau riset khusus undangan. [Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/introducing-claude-fable-5-and-claude-mythos-5) menawarkan kemampuan yang sama dan tidak memerlukan persetujuan akses. Perubahan dalam bagian ini berlaku sama untuk kedua target.

Migrasi sebagian besar bersifat drop-in. Claude Mythos 5 dan Claude Fable 5 menggunakan [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) yang sama dan pola ["tool use" (penggunaan alat)](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) yang sama seperti Claude Mythos Preview, dan jumlah token kurang lebih tidak berubah karena ketiga model menggunakan tokenizer yang sama. Perubahan utama yang perlu diperiksa adalah fitur yang tidak lagi tersedia (tercantum di bagian berikutnya) dan output thinking. Jika Anda bermigrasi ke Claude Fable 5, rencanakan juga penanganan penolakan oleh pengklasifikasi keamanan, yang tidak dimiliki Claude Mythos Preview dan Claude Mythos 5; lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

Untuk jadwal penghentian Claude Mythos Preview, lihat [Penghentian model](https://platform.claude.com/docs/id/about-claude/model-deprecations).

### Perbarui nama model Anda

```python
model = "claude-mythos-preview"  # Before
model = "claude-mythos-5"  # After

# Atau, untuk model dengan kemampuan yang sama dan tanpa persyaratan persetujuan akses:
model = "claude-fable-5"  # After
```

### Fitur yang tidak tersedia di Claude Mythos 5 dan Claude Fable 5

1. **Pemikiran diperpanjang dan anggaran token thinking:** Pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`) tidak didukung di `claude-mythos-5` atau `claude-fable-5` dan mengembalikan error 400. [Adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) selalu aktif: model menentukan kapan dan seberapa banyak berpikir pada setiap permintaan, dan tidak diperlukan konfigurasi `thinking`. `thinking: {type: "disabled"}` mengembalikan error. `budget_tokens` tidak memiliki pengganti langsung: thinking bersifat adaptif, dan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) adalah kontrol tingkat output yang terpisah, bukan anggaran thinking.

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

3. **Output thinking:** Di `claude-mythos-5` dan `claude-fable-5`, rantai pemikiran mentah tidak pernah dikembalikan, tetapi blok thinking tetap membawa teks ringkasan yang dapat dibaca ketika `thinking.display` diatur ke `summarized`. Kirimkan kembali blok thinking tanpa perubahan saat melanjutkan percakapan pada model yang sama. Lihat [Output thinking pada Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).

### Penghitungan token dan penagihan

`claude-mythos-5` dan `claude-fable-5` menggunakan tokenizer yang sama dengan `claude-mythos-preview` (tokenizer yang diperkenalkan bersama Claude Opus 4.7). Jumlah token kurang lebih tidak berubah saat bermigrasi dari `claude-mythos-preview`. Dibandingkan dengan model sebelum Claude Opus 4.7, konten yang sama dapat ditokenisasi menjadi sekitar 30% lebih banyak token, bervariasi menurut konten dan bentuk beban kerja.

[`/v1/messages/count_tokens`](https://platform.claude.com/docs/id/build-with-claude/token-counting) mengembalikan nilai yang kurang lebih tidak berubah untuk `claude-mythos-5` dan `claude-fable-5` dibandingkan dengan `claude-mythos-preview`. Tetapkan ulang baseline biaya dan latensi pada beban kerja Anda sendiri.

### Daftar periksa migrasi

* Perbarui nama model dari `claude-mythos-preview` ke `claude-mythos-5`, atau ke `claude-fable-5`, yang menawarkan kemampuan yang sama dan tidak memerlukan persetujuan akses.
* Hapus konfigurasi pemikiran diperpanjang manual (`thinking: {type: "enabled", budget_tokens: N}`). Adaptive thinking selalu aktif, dan tidak diperlukan field `thinking`.
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun. Menonaktifkan thinking mengembalikan error di `claude-mythos-5` dan `claude-fable-5`.
* Hapus `budget_tokens`. Tidak ada pengganti langsungnya: thinking bersifat adaptif, dan parameter `effort` adalah kontrol tingkat output yang terpisah, bukan anggaran thinking.
* Verifikasi bahwa kode apa pun yang mem-parsing field `thinking` memperlakukannya hanya sebagai teks tampilan dan mengirimkan kembali blok thinking tanpa perubahan saat melanjutkan pada model yang sama. `thinking.display` secara default bernilai `"omitted"` di `claude-mythos-5` dan `claude-fable-5`, sama seperti di Claude Mythos Preview; atur `display: "summarized"` untuk menerima ringkasan yang dapat dibaca. Lihat [Output thinking pada Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).
* Jika Anda memutar ulang riwayat percakapan pada model lain, hapus terlebih dahulu blok `thinking` dan `redacted_thinking` dari giliran asisten sebelumnya. Blok thinking dari `claude-mythos-5` dan `claude-fable-5` terikat pada model yang menghasilkannya, dan model selain Claude Fable 5 dan Claude Mythos 5 mengabaikannya secara diam-diam. Penghapusan menjaga permintaan lintas model tetap minimal dan seragam.
* Jika Anda bermigrasi ke Claude Fable 5, tangani `stop_reason: "refusal"` dan baca field `stop_details.category`. Claude Fable 5 menjalankan pengklasifikasi keamanan yang tidak dimiliki Claude Mythos Preview dan Claude Mythos 5. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).
* Tetapkan ulang baseline jumlah token dan biaya pada beban kerja Anda sendiri. Jumlah token kurang lebih tidak berubah saat bermigrasi dari `claude-mythos-preview`.

## Migrasi ke Claude Mythos 5 dan Claude Fable 5 dari Claude Opus 5

Claude Fable 5 dan Claude Mythos 5 menggunakan [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) yang sama dan pola [penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) yang sama seperti Claude Opus 5, dengan [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) yang sama secara default dan [128k token output maksimum](https://platform.claude.com/docs/id/models/overview) yang sama. Pembatasan prefill dan parameter sampling, serta perilaku tampilan thinking, terbawa dari Claude Opus 5 tanpa perubahan. Perubahan yang perlu diperiksa adalah thinking yang selalu aktif, harga, Priority Tier, dan retensi data.

### Perbarui nama model Anda

```python
model = "claude-opus-5"  # Before
model = "claude-fable-5"  # After

# Atau, untuk model Project Glasswing dengan kemampuan yang sama:
model = "claude-mythos-5"  # After
```

### Apa yang berubah

1. **Thinking tidak dapat lagi dinonaktifkan:** Di Claude Opus 5, thinking aktif secara default dan dapat dimatikan dengan `thinking: {type: "disabled"}` pada tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) `high` atau lebih rendah. Di `claude-fable-5` dan `claude-mythos-5`, [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) selalu aktif, dan `thinking: {type: "disabled"}` mengembalikan error 400 pada tingkat effort apa pun. Hapus konfigurasi `thinking: {type: "disabled"}` dan gunakan tingkat effort yang lebih rendah untuk mengontrol pengeluaran token sebagai gantinya.

   Jika permintaan Claude Opus 5 Anda menonaktifkan thinking, bentuk respons berubah: respons dapat dimulai dengan satu atau lebih blok `thinking` sebelum blok `text` pertama, dikembalikan dengan field `thinking` kosong pada default `display: "omitted"` (default yang sama dengan Claude Opus 5). Kode yang membaca balasan berdasarkan posisi, seperti `content[0].text` atau handler stream yang memperlakukan blok konten pertama sebagai teks, harus memilih blok konten berdasarkan field `type`-nya, dan loop penggunaan alat harus mengirimkan kembali blok `thinking` secara lengkap dan tanpa modifikasi bersama hasil alatnya. API menolak blok thinking yang diedit, diurutkan ulang, atau dihapus sebagian dengan error 400 (lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks)). Token thinking ditagih sebagai token output bahkan ketika teks thinking tidak dikembalikan.

2. **Harga:** Claude Fable 5 dan Claude Mythos 5 dihargai $10 USD per juta token input dan $50 USD per juta token output, dibandingkan dengan $5 USD dan $25 USD untuk Claude Opus 5. Lihat [harga Claude](https://platform.claude.com/docs/id/about-claude/pricing).

3. **Priority Tier:** [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers#supported-models) tidak didukung di Claude Opus 5, sehingga tidak ada lalu lintas yang ada yang terpengaruh. Jika organisasi Anda memiliki komitmen Priority Tier, Claude Fable 5 mendukungnya; Claude Mythos 5 tidak.

4. **Retensi data:** Claude Fable 5 dan Claude Mythos 5 memerlukan retensi data 30 hari dan tidak tersedia di bawah pengaturan zero data retention (ZDR); keduanya ditetapkan sebagai Covered Models. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).

### Daftar periksa migrasi

* Perbarui nama model dari `claude-opus-5` ke `claude-fable-5` (atau `claude-mythos-5`).
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun; konfigurasi ini mengembalikan error 400 di `claude-fable-5` dan `claude-mythos-5`. Gunakan tingkat [effort](https://platform.claude.com/docs/id/build-with-claude/effort) yang lebih rendah untuk mengontrol pengeluaran token sebagai gantinya, dan tinjau kembali `max_tokens` untuk beban kerja yang berjalan dengan thinking dinonaktifkan di Claude Opus 5.
* Jika beban kerja tersebut membaca konten berdasarkan posisi, seperti `content[0].text`, perbarui agar memilih blok konten berdasarkan `type`: blok `thinking` kini tiba sebelum blok `text`. Kirimkan kembali blok `thinking` secara lengkap dan tanpa modifikasi dalam loop penggunaan alat; blok yang dimodifikasi mengembalikan error 400.
* Jika organisasi Anda memiliki pengaturan zero data retention (ZDR), konfirmasikan kelayakan sebelum bermigrasi. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Tetapkan ulang baseline biaya pada beban kerja Anda sendiri. Jumlah token kurang lebih tidak berubah; harga per token berbeda, dan beban kerja yang berjalan dengan thinking dinonaktifkan kini menghasilkan token thinking, yang ditagih sebagai token output.

## Migrasi ke Claude Mythos 5 dan Claude Fable 5 dari Claude Opus 4.8

<Note>
  Jika kode Anda menggunakan Claude Opus 4.7 atau lebih lama, terapkan terlebih dahulu bagian "dari" yang relevan pada [Migrasi ke Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/migration-guide) untuk perubahan tingkat API dari model Anda saat ini, lalu delta yang tersisa di bagian ini.
</Note>

Migrasi sebagian besar bersifat drop-in. Claude Fable 5 dan Claude Mythos 5 menggunakan [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages) yang sama dan pola [penggunaan alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/overview) yang sama seperti Claude Opus 4.8, dengan [jendela konteks 1M token](https://platform.claude.com/docs/id/build-with-claude/context-windows) yang sama secara default dan [128k token output maksimum](https://platform.claude.com/docs/id/models/overview) yang sama. Jumlah token kurang lebih tidak berubah karena model-model ini menggunakan tokenizer yang sama. Perubahan utama yang perlu diperiksa adalah [adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) yang selalu aktif, output thinking, penolakan oleh pengklasifikasi keamanan (hanya Claude Fable 5), dan harga.

### Perbarui nama model Anda

```python
model = "claude-opus-4-8"  # Before
model = "claude-fable-5"  # After

# Atau, untuk model Project Glasswing dengan kemampuan yang sama:
model = "claude-mythos-5"  # After
```

### Apa yang berubah

Butir-butir dalam bagian ini menjelaskan perbedaan API dan perilaku yang perlu diperiksa setelah Anda mengganti ID model. Kecuali disebutkan lain, semuanya berlaku sama untuk `claude-fable-5` dan `claude-mythos-5`.

1. **Adaptive thinking selalu aktif:** [Adaptive thinking](https://platform.claude.com/docs/id/build-with-claude/thinking) adalah satu-satunya mode thinking di `claude-fable-5` dan `claude-mythos-5`. Model menentukan kapan dan seberapa banyak berpikir pada setiap permintaan, dan tidak diperlukan konfigurasi `thinking`. `thinking: {type: "disabled"}` mengembalikan error. Gunakan [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) untuk mengontrol kedalaman thinking.

   Perubahan perilaku yang perlu diperiksa: di Claude Opus 4.8, permintaan tanpa field `thinking` berjalan tanpa thinking; di `claude-fable-5` dan `claude-mythos-5`, permintaan yang sama berjalan dengan adaptive thinking. `max_tokens` tetap menjadi batas keras pada total output, thinking ditambah teks respons, jadi tinjau kembali untuk beban kerja yang berjalan tanpa thinking di Claude Opus 4.8. Lihat [Kontrol biaya](https://platform.claude.com/docs/id/build-with-claude/thinking-steering-and-cost#cost-control). Respons juga dapat dimulai dengan satu atau lebih blok `thinking` sebelum blok `text` pertama, sehingga kode yang membaca balasan berdasarkan posisi (misalnya, `content[0].text`, atau handler stream yang memperlakukan blok konten pertama sebagai teks) harus memilih blok konten berdasarkan field `type`-nya. Token thinking ditagih sebagai token output bahkan ketika teks thinking tidak dikembalikan kepada Anda, sehingga beban kerja yang berjalan tanpa thinking di Claude Opus 4.8 menghasilkan lebih banyak token output per permintaan, di samping perbedaan harga per token.

   Jika Anda menjalankan loop penggunaan alat, kirimkan kembali blok `thinking` dari setiap respons asisten ke API secara lengkap dan tanpa modifikasi saat Anda mengembalikan hasil alat, termasuk blok yang field `thinking`-nya kosong. Kembalikan pesan asisten sebagaimana diterima alih-alih memfilter blok kontennya berdasarkan tipe atau membangunnya ulang: API menolak blok thinking yang diedit, diurutkan ulang, atau dihapus sebagian dengan error 400. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).

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

4. **Output thinking:** Di `claude-fable-5` dan `claude-mythos-5`, rantai pemikiran mentah tidak pernah dikembalikan, tetapi blok thinking tetap membawa teks ringkasan yang dapat dibaca ketika `thinking.display` diatur ke `summarized`. Kirimkan kembali blok thinking tanpa perubahan saat melanjutkan percakapan pada model yang sama. Lihat [Output thinking pada Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).

5. **Pengklasifikasi keamanan dan stop reason `refusal` (hanya Claude Fable 5):** `claude-fable-5` menjalankan pengklasifikasi keamanan pada permintaan dan selama pembuatan respons. Claude Mythos 5 tidak menyertakan pengklasifikasi ini. Ketika pengklasifikasi menolak permintaan, Messages API mengembalikan `stop_reason: "refusal"` sebagai respons HTTP 200 yang berhasil, bukan error. Field `stop_details.category` melaporkan pengklasifikasi mana yang terpicu, dengan kategori seperti `"cyber"`, `"bio"`, dan `"reasoning_extraction"`, atau `null` ketika penolakan tidak terpetakan ke kategori bernama mana pun. Lihat [tabel kategori penolakan](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback#refusal-response) untuk daftar lengkapnya.

   Anda tidak ditagih untuk token input dari permintaan yang ditolak sebelum output apa pun dihasilkan. Ketika pengklasifikasi terpicu di tengah stream, input dan output yang sudah di-stream ditagih; buang output parsial tersebut.

   Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, kirimkan parameter opt-in `fallbacks`, yang berstatus beta di Claude API. Parameter ini tidak tersedia di Message Batches API atau di Amazon Bedrock, Google Cloud, dan Microsoft Foundry; di ketiga platform tersebut, jalankan percobaan ulang di sisi klien atau gunakan middleware refusal-fallback SDK. Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).

6. **Mulai dari effort `high`:** Default [parameter effort](https://platform.claude.com/docs/id/build-with-claude/effort) tetap `high`. Di Claude Opus 4.8, rekomendasi untuk pekerjaan coding dan otonomi tinggi adalah mengatur `xhigh` secara eksplisit. Di `claude-fable-5` dan `claude-mythos-5`, gunakan `high` sebagai default untuk sebagian besar tugas dan simpan `xhigh` untuk beban kerja yang paling sensitif terhadap kemampuan. Pengaturan effort yang lebih rendah tetap berkinerja baik dan sering melampaui kinerja `xhigh` pada model sebelumnya. Kurangi effort jika suatu tugas selesai tetapi memakan waktu lebih lama dari yang diperlukan. Lihat [Prompting Claude Fable 5](https://platform.claude.com/docs/id/build-with-claude/prompt-engineering/prompting-claude-fable-5#consider-all-effort-levels).

7. **Minimum caching prompt yang lebih rendah:** Panjang prompt minimum yang dapat di-cache di `claude-fable-5` dan `claude-mythos-5` adalah 512 token, lebih rendah dari 1.024 token di Claude Opus 4.8. Prompt yang terlalu pendek untuk di-cache di Claude Opus 4.8 kini dapat membuat entri cache, tanpa perlu perubahan kode. Lihat ["Prompt caching" (caching prompt)](https://platform.claude.com/docs/id/build-with-claude/prompt-caching#cache-limitations) untuk minimum per model.

### Daftar periksa migrasi

* Jika organisasi Anda memiliki pengaturan zero data retention (ZDR), konfirmasikan kelayakan sebelum bermigrasi. `claude-fable-5` dan `claude-mythos-5` memerlukan retensi data 30 hari; di Claude API, permintaan ke `claude-fable-5` yang tidak memenuhi persyaratan ini mengembalikan `invalid_request_error` 400. Claude Opus 4.8 tetap tersedia di bawah ZDR. Lihat [Persyaratan retensi data khusus model](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
* Perbarui nama model dari `claude-opus-4-8` ke `claude-fable-5` (atau `claude-mythos-5`).
* Hapus konfigurasi `thinking: {type: "disabled"}` apa pun. Menonaktifkan thinking mengembalikan error di `claude-fable-5` dan `claude-mythos-5`, dan permintaan tanpa field `thinking` berjalan dengan adaptive thinking.
* Perbarui parsing respons yang membaca konten berdasarkan posisi, seperti `content[0].text`: dengan adaptive thinking yang selalu aktif, blok `thinking` tiba sebelum blok `text`. Pilih blok konten berdasarkan `type` sebagai gantinya, dan kirimkan kembali blok `thinking` secara lengkap dan tanpa modifikasi dalam loop penggunaan alat; blok yang dimodifikasi mengembalikan error 400. Lihat [Mempertahankan blok thinking](https://platform.claude.com/docs/id/build-with-claude/thinking#preserving-thinking-blocks).
* Jika Anda telah menghapus pemikiran diperpanjang manual dan prefill asisten selama migrasi sebelumnya, tidak diperlukan tindakan apa pun: keduanya tetap tidak didukung di `claude-fable-5` dan `claude-mythos-5`.
* Verifikasi bahwa kode apa pun yang mem-parsing field `thinking` memperlakukannya hanya sebagai teks tampilan dan mengirimkan kembali blok thinking tanpa perubahan saat melanjutkan pada model yang sama. `thinking.display` secara default bernilai `"omitted"` di `claude-fable-5` dan `claude-mythos-5`, sama seperti di Claude Opus 4.8; atur `display: "summarized"` untuk menerima ringkasan yang dapat dibaca. Lihat [Output thinking pada Claude Fable 5 dan Claude Mythos 5](https://platform.claude.com/docs/id/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5).
* Jika Anda memutar ulang riwayat percakapan pada model lain, hapus terlebih dahulu blok `thinking` dan `redacted_thinking` dari giliran asisten sebelumnya. Blok thinking dari `claude-fable-5` dan `claude-mythos-5` terikat pada model yang menghasilkannya, dan model selain Claude Fable 5 dan Claude Mythos 5 mengabaikannya secara diam-diam. Penghapusan menjaga permintaan lintas model tetap minimal dan seragam. Pengecualiannya adalah menukarkan [kredit fallback](https://platform.claude.com/docs/id/build-with-claude/fallback-credit), yang mengharuskan body permintaan dikembalikan sesuai aturan persis fitur tersebut.
* Jika Anda bermigrasi ke Claude Fable 5, tangani `stop_reason: "refusal"` dan baca field `stop_details.category`. Untuk menjalankan ulang permintaan yang ditolak pada model lain secara otomatis, pertimbangkan parameter opt-in `fallbacks` (beta). Lihat [Penolakan dan fallback](https://platform.claude.com/docs/id/build-with-claude/refusals-and-fallback).
* Evaluasi ulang pengaturan `effort` Anda. Mulai dari `high` untuk sebagian besar tugas, termasuk beban kerja yang berjalan pada `xhigh` di Claude Opus 4.8.
* Tetapkan ulang baseline biaya dan latensi pada beban kerja Anda sendiri. Jumlah token kurang lebih tidak berubah saat bermigrasi dari `claude-opus-4-8`; harga per token berbeda, dan token thinking ditagih sebagai token output, sehingga beban kerja yang berjalan tanpa thinking menghasilkan lebih banyak token output per permintaan.
