---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/data-residency
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: cd3afb5cbf4719bd92aacb551d5f7b9a738e14b14b07b47b9fc9229d98c0b8e0
---

---
title: Residensi data
url: https://platform.claude.com/docs/id/manage-claude/data-residency
description: Kelola di mana inferensi model berjalan dan di mana data disimpan dengan kontrol geografis.
---

Kontrol "data residency" (residensi data) memungkinkan Anda mengelola di mana data Anda diproses dan disimpan. Dua pengaturan independen mengatur hal ini:

* **Inference geo:** Mengontrol di mana inferensi model berjalan, per permintaan. Diatur melalui parameter API `inference_geo` atau sebagai default workspace.
* **Workspace geo:** Mengontrol di mana data disimpan saat tidak digunakan (at rest) dan di mana pemrosesan endpoint (seperti transcoding gambar dan eksekusi kode) terjadi. Dikonfigurasi di tingkat workspace di [Claude Console](https://platform.claude.com).

<Note>
  [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) mendukung penyematan geografis di tingkat agen: `inference_geo` pada [konfigurasi model agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#pin-the-inference-geo) menyematkan geografi yang melayani permintaan model untuk sesi yang menjalankan agen tersebut, dengan [override per sesi](https://platform.claude.com/docs/id/managed-agents/sessions#pin-the-inference-geo-for-a-session) saat pembuatan sesi. Agen tanpa penyematan mengikuti inference geo default workspace pada setiap permintaan. Managed Agents juga mematuhi Workspace geo yang dikonfigurasi di Console, dan dengan [sandbox yang di-hosting sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes), eksekusi alat dan sistem file sandbox tetap berada di infrastruktur yang Anda kendalikan; isi [memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes#use-memory-stores) yang terlampir tetap disimpan oleh Anthropic dan disalin ke sandbox Anda untuk sesi tersebut.
</Note>

## Inference geo

<Note>
  Untuk mengetahui bagaimana zero data retention (ZDR) berlaku pada fitur ini, lihat [API dan retensi data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention).
</Note>

Parameter `inference_geo` mengontrol di mana inferensi model berjalan untuk permintaan API tertentu. Tambahkan ke panggilan `POST /v1/messages` mana pun.

| Nilai      | Deskripsi                                                                                                     |
| ---------- | ------------------------------------------------------------------------------------------------------------- |
| `"global"` | Default. Inferensi dapat berjalan di geografi mana pun yang tersedia untuk performa dan ketersediaan optimal. |
| `"us"`     | Inferensi hanya berjalan di infrastruktur yang berbasis di AS.                                                |

### Penggunaan API

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "inference_geo": "us",
      "messages": [{
        "role": "user",
        "content": "Summarize the key points of this document."
      }]
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5 \
    --max-tokens 1024 \
    --inference-geo us \
    --message '{role: user, content: "Summarize the key points of this document."}' \
    --transform '{content.#(type=="text").text,usage.inference_geo}' --format yaml
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      inference_geo="us",
      messages=[
          {"role": "user", "content": "Summarize the key points of this document."}
      ],
  )

  for block in response.content:
      if block.type == "text":
          print(block.text)
  # Periksa di mana inferensi sebenarnya dijalankan
  print(f"Inference geo: {response.usage.inference_geo}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    inference_geo: "us",
    messages: [
      {
        role: "user",
        content: "Summarize the key points of this document."
      }
    ]
  });

  const textBlock = response.content.find(
    (block): block is Anthropic.TextBlock => block.type === "text"
  );
  console.log(textBlock?.text);
  // Periksa di mana inferensi sebenarnya dijalankan
  console.log(`Inference geo: ${response.usage.inference_geo}`);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  var response = await client.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5,
          MaxTokens = 1024,
          InferenceGeo = "us",
          Messages =
          [
              new() { Role = Role.User, Content = "Summarize the key points of this document." },
          ],
      }
  );

  foreach (var block in response.Content)
  {
      if (block.TryPickText(out var textBlock))
      {
          Console.WriteLine(textBlock.Text);
      }
  }

  // Periksa di mana inferensi sebenarnya dijalankan
  Console.WriteLine($"Inference geo: {response.Usage.InferenceGeo}");
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:        anthropic.ModelClaudeOpus5,
  	MaxTokens:    1024,
  	InferenceGeo: anthropic.String("us"),
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Summarize the key points of this document.")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range message.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  // Periksa di mana inferensi sebenarnya dijalankan
  fmt.Printf("Inference geo: %s\n", message.Usage.InferenceGeo)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  Message response = client.messages().create(
          MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5)
                  .maxTokens(1024L)
                  .inferenceGeo("us")
                  .addUserMessage("Summarize the key points of this document.")
                  .build());

  response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  // Periksa di mana inferensi sebenarnya dijalankan
  IO.println("Inference geo: " + response.usage().inferenceGeo().get());
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      model: 'claude-opus-5',
      maxTokens: 1024,
      inferenceGeo: 'us',
      messages: [
          ['role' => 'user', 'content' => 'Summarize the key points of this document.'],
      ],
  );

  foreach ($response->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, PHP_EOL;
      }
  }
  // Periksa di mana inferensi sebenarnya dijalankan
  echo "Inference geo: {$response->usage->inferenceGeo}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    inference_geo: "us",
    messages: [
      {role: "user", content: "Summarize the key points of this document."}
    ]
  )

  response.content.each do |block|
    puts block.text if block.type == :text
  end
  # Periksa di mana inferensi sebenarnya dijalankan
  puts "Inference geo: #{response.usage.inference_geo}"
  ```
</CodeGroup>

### Respons

Objek `usage` pada respons menyertakan field `inference_geo` yang menunjukkan di mana inferensi berjalan:

```json Output
{
  "usage": {
    "input_tokens": 25,
    "output_tokens": 150,
    "inference_geo": "us"
  }
}
```

### Ketersediaan model

Parameter `inference_geo` didukung pada model Claude 4.6 dan yang lebih baru. Permintaan dengan `inference_geo` pada Claude Opus 4.5, Claude Sonnet 4.5, Claude Haiku 4.5, atau model yang lebih lama mengembalikan error 400.

<Note>
  Parameter `inference_geo` tersedia di Claude API (pihak pertama) dan [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws). Di Amazon Bedrock dan Google Cloud, region inferensi ditentukan oleh URL endpoint atau profil inferensi, sehingga `inference_geo` tidak berlaku. Di [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), `inference_geo` juga tidak berlaku: deployment yang di-hosting di Azure dapat menggunakan tipe deployment US Data Zone Standard, yang menjaga inferensi tetap berada di Amerika Serikat. Parameter `inference_geo` juga tidak tersedia melalui [endpoint kompatibilitas OpenAI SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk).
</Note>

### Pembatasan tingkat workspace

Pengaturan workspace juga mendukung pembatasan inference geo mana yang tersedia:

* **`allowed_inference_geos`:** Membatasi geo mana yang dapat digunakan oleh workspace. Jika permintaan menentukan `inference_geo` yang tidak ada dalam daftar ini, API mengembalikan error.
* **`default_inference_geo`:** Menetapkan geo fallback ketika `inference_geo` dihilangkan dari permintaan. Permintaan individual dapat meng-override ini dengan menetapkan `inference_geo` secara eksplisit.

Pengaturan ini dapat dikonfigurasi melalui Console atau [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) di bawah field `data_residency`.

## Workspace geo

Workspace geo ditetapkan saat Anda membuat workspace dan tidak dapat diubah setelahnya. Saat ini, `"us"` adalah satu-satunya workspace geo yang tersedia.

Untuk menetapkan workspace geo, buat workspace baru di [Console](https://platform.claude.com):

1. Buka **Settings** > **Workspaces**.
2. Buat workspace baru.
3. Pilih workspace geo.

<Note>
  **Claude Platform on AWS:** Workspace geo tidak dapat dikonfigurasi. Sesi Claude Managed Agents di platform ini berjalan dengan Workspace geo efektif `"us"`, yang saat ini merupakan satu-satunya workspace geo yang tersedia. Lihat [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) untuk pertimbangan residensi data yang spesifik untuk platform tersebut.
</Note>

## Harga

Harga residensi data bervariasi menurut generasi model:

* **Model Claude 4.6 dan yang lebih baru:** Inferensi khusus AS (`inference_geo: "us"`) dikenakan harga 1,1x tarif standar di semua kategori harga token (token input, token output, penulisan cache, dan pembacaan cache).
* **Routing global** (`inference_geo: "global"`): Harga standar berlaku.
* **Model lama:** Tidak mendukung `inference_geo` (lihat [Ketersediaan model](https://platform.claude.com/docs/id/manage-claude/data-residency#model-availability)); harga standar berlaku. Permintaan yang menyertakan parameter ini mengembalikan error 400.

Harga ini berlaku untuk Claude API (pihak pertama) dan Claude Platform on AWS. Di Claude in Microsoft Foundry, pengali 1,1x yang sama berlaku untuk deployment yang di-hosting di Azure yang menggunakan tipe deployment US Data Zone Standard. Platform yang dioperasikan mitra (Bedrock dan Google Cloud) memiliki harga regional masing-masing. Lihat [Harga residensi data](https://platform.claude.com/docs/id/about-claude/pricing#data-residency-pricing) untuk detailnya.

Pengali yang sama berlaku untuk [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview): ketika [konfigurasi model](https://platform.claude.com/docs/id/managed-agents/agent-setup) agen menyematkan `inference_geo` ke `"us"`, permintaan model dalam sesi yang menjalankan agen tersebut dikenakan harga 1,1x tarif standar.

<Note>
  Jika Anda memiliki komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers), pengali 1,1x untuk inferensi khusus AS juga memengaruhi cara token dihitung terhadap kapasitas Priority Tier Anda. Setiap token yang dikonsumsi dengan `inference_geo: "us"` mengurangi 1,1 token dari TPM yang Anda komitmenkan, konsisten dengan cara pengali harga lainnya (seperti caching prompt) memengaruhi laju burndown.
</Note>

## Dukungan Batch API

Parameter `inference_geo` didukung pada [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing). Setiap permintaan dalam batch dapat menentukan nilai `inference_geo`-nya sendiri.

## Migrasi dari opt-out lama

Jika organisasi Anda sebelumnya memilih keluar (opt-out) dari routing global untuk menjaga inferensi tetap di AS, workspace Anda telah dikonfigurasi secara otomatis dengan `allowed_inference_geos: ["us"]` dan `default_inference_geo: "us"`. Tidak diperlukan perubahan kode. Persyaratan residensi data Anda yang ada tetap diberlakukan melalui kontrol geo yang baru.

### Apa yang berubah

Opt-out lama adalah pengaturan tingkat organisasi yang membatasi semua permintaan ke infrastruktur berbasis AS. Kontrol residensi data yang baru menggantikannya dengan dua mekanisme:

* **Kontrol per permintaan:** Parameter `inference_geo` memungkinkan Anda menentukan `"us"` atau `"global"` pada setiap panggilan API, memberi Anda fleksibilitas di tingkat permintaan.
* **Kontrol workspace:** Pengaturan `default_inference_geo` dan `allowed_inference_geos` di Console memungkinkan Anda memberlakukan kebijakan geo di semua kunci dalam sebuah workspace.

### Apa yang terjadi pada workspace Anda

Workspace Anda dimigrasikan secara otomatis:

| Pengaturan lama                    | Padanan baru                                                    |
| ---------------------------------- | --------------------------------------------------------------- |
| Opt-out routing global (khusus AS) | `allowed_inference_geos: ["us"]`, `default_inference_geo: "us"` |

Semua permintaan API yang menggunakan kunci dari workspace Anda tetap berjalan di infrastruktur berbasis AS. Tidak diperlukan tindakan apa pun untuk mempertahankan perilaku Anda saat ini.

### Jika Anda ingin menggunakan routing global

Jika persyaratan residensi data Anda telah berubah dan Anda ingin memanfaatkan routing global untuk performa dan ketersediaan yang lebih baik, perbarui pengaturan inference geo workspace Anda untuk menyertakan `"global"` dalam geo yang diizinkan dan tetapkan `default_inference_geo` ke `"global"`. Lihat [Pembatasan tingkat workspace](https://platform.claude.com/docs/id/manage-claude/data-residency#workspace-level-restrictions) untuk detailnya.

### Dampak harga

Model lama tidak terpengaruh oleh migrasi ini. Untuk harga terkini pada model yang lebih baru, lihat [Harga](https://platform.claude.com/docs/id/manage-claude/data-residency#pricing).

## Keterbatasan saat ini

* **Batas laju bersama:** "Rate limit" (batas laju) dibagi bersama di semua geo.
* **Inference geo:** Hanya `"us"` dan `"global"` yang tersedia.
* **Workspace geo:** Hanya `"us"` yang tersedia saat ini. Workspace geo tidak dapat diubah setelah pembuatan workspace.

## Langkah selanjutnya

<CardGroup>
  <Card title="Harga" icon="dollar-sign" href="https://platform.claude.com/docs/id/about-claude/pricing#data-residency-pricing">
    Lihat detail harga residensi data.
  </Card>

  <Card title="Workspace" icon="building" href="https://platform.claude.com/docs/id/manage-claude/workspaces">
    Pelajari tentang konfigurasi workspace.
  </Card>

  <Card title="Usage and Cost API" icon="chart" href="https://platform.claude.com/docs/id/manage-claude/usage-cost-api">
    Lacak penggunaan dan biaya berdasarkan residensi data.
  </Card>
</CardGroup>
