---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/data-residency
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 28777eb46e13cfee570416158b75b614e7cf62f2ad020c68de30facbee992a31
---

---
title: Residensi data
url: https://platform.claude.com/docs/id/manage-claude/data-residency
description: Kelola lokasi inferensi model dijalankan dan lokasi data disimpan dengan kontrol geografis.
featureMetadata:
  status: stable
  zdr:
    eligibility: eligible
    note: Excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements).
  supportedModels:
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
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
  supportedPlatforms:
    Claude API: stable
    Claude Platform on AWS:
      availability: stable
      note: Geo workspace tidak dapat dikonfigurasi; sesi Managed Agents di sana berjalan dengan geo workspace “us”.
    Claude Models on Google Cloud (Anthropic managed):
      availability: stable
      note: Geo workspace tidak dapat dikonfigurasi.
---

**Dukungan API**: Penggunaan berbeda menurut produk.

* **Messages API**: Atur `inference_geo` pada setiap permintaan, atau atur default untuk workspace.
* **Managed Agents**: Tetapkan `inference_geo` dalam konfigurasi model agen; override saat pembuatan sesi.

Kontrol “data residency” (residensi data) memungkinkan Anda mengelola lokasi data Anda diproses dan disimpan. Dua pengaturan independen mengatur hal ini:

* **Inference geo:** Mengontrol lokasi inferensi model dijalankan, per permintaan. Diatur melalui parameter API `inference_geo` atau sebagai default workspace.
* **Workspace geo:** Mengontrol lokasi data disimpan saat tidak digunakan (at rest) dan lokasi pemrosesan endpoint (seperti transcoding gambar dan eksekusi kode) terjadi. Dikonfigurasi di tingkat workspace di [Claude Console](https://platform.claude.com/).

<Note>
  [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview) mendukung penetapan geografis di tingkat agen: `inference_geo` pada [konfigurasi model agen](https://platform.claude.com/docs/id/managed-agents/agent-setup#pin-the-inference-geo) menetapkan geografi yang melayani permintaan model untuk sesi yang menjalankan agen tersebut, dengan [penggantian per sesi](https://platform.claude.com/docs/id/managed-agents/sessions#pin-the-inference-geo-for-a-session) saat pembuatan sesi. Agen tanpa penetapan mengikuti inference geo default workspace pada setiap permintaan. Managed Agents juga mematuhi Workspace geo yang dikonfigurasi di Console, dan dengan [sandbox yang di-host sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes), eksekusi alat dan sistem file sandbox tetap berada di infrastruktur yang Anda kendalikan; isi [memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory) yang terlampir tetap disimpan oleh Anthropic dan disalin ke sandbox Anda untuk sesi tersebut.
</Note>

## Inference geo

Parameter `inference_geo` mengontrol lokasi inferensi model dijalankan untuk permintaan API tertentu. Tambahkan parameter ini ke panggilan `POST /v1/messages` mana pun.

| Nilai      | Deskripsi                                                                                                    |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| `"global"` | Default. Inferensi dapat berjalan di geografi mana pun yang tersedia untuk kinerja dan ketersediaan optimal. |
| `"us"`     | Inferensi hanya berjalan di infrastruktur yang berbasis di AS.                                               |

### Penggunaan API

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
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
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --inference-geo us \
    --message '{role: user, content: "Summarize the key points of this document."}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5-5",
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
    model: "claude-opus-5-5",
    max_tokens: 1024,
    inference_geo: "us",
    messages: [
      {
        role: "user",
        content: "Summarize the key points of this document."
      }
    ]
  });

  const textBlock = response.content.find((block) => block.type === "text");
  console.log(textBlock?.text);
  // Periksa di mana inferensi benar-benar dijalankan
  console.log(`Inference geo: ${response.usage.inference_geo}`);
  ```

  ```csharp C#
  var client = new AnthropicClient();

  var response = await client.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          InferenceGeo = "us",
          Messages =
          [
              new UserMessageParam { Content = "Summarize the key points of this document." },
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
  	Model:        anthropic.ModelClaudeOpus5_5,
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
          .model(Model.CLAUDE_OPUS_5_5)
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
      model: 'claude-opus-5-5',
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
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
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

Objek `usage` pada respons menyertakan field `inference_geo` yang menunjukkan lokasi inferensi dijalankan:

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

Parameter `inference_geo` didukung pada model Claude 4.6 dan yang lebih baru. Permintaan dengan `inference_geo` pada Claude Opus 4.5, Claude Sonnet 4.5 (tidak digunakan lagi), Claude Haiku 4.5, atau model yang lebih lama akan mengembalikan error 400.

<Note>
  Parameter `inference_geo` tersedia di Claude API (first-party), [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws), dan [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed). Di Amazon Bedrock dan Claude Models on Google Cloud (Google managed), region inferensi ditentukan oleh URL endpoint atau profil inferensi, sehingga `inference_geo` tidak berlaku. Di [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry), `inference_geo` juga tidak berlaku: deployment yang di-host di Azure dapat menggunakan jenis deployment US Data Zone Standard sebagai gantinya, yang menjaga inferensi tetap berada di Amerika Serikat. Parameter `inference_geo` juga tidak tersedia melalui [endpoint kompatibilitas OpenAI SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/libraries/openai-sdk).
</Note>

### Pembatasan tingkat workspace

Pengaturan workspace juga mendukung pembatasan inference geo yang tersedia:

* **`allowed_inference_geos`:** Membatasi geo yang dapat digunakan oleh workspace. Jika permintaan menentukan `inference_geo` yang tidak ada dalam daftar ini, API akan mengembalikan error.
* **`default_inference_geo`:** Menetapkan geo cadangan ketika `inference_geo` dihilangkan dari permintaan. Permintaan individual dapat menggantinya dengan menetapkan `inference_geo` secara eksplisit.

Pengaturan ini dapat dikonfigurasi melalui Console atau [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api) di bawah field `data_residency`.

<Note>
  **Claude Models on Google Cloud (Anthropic managed):** Setiap workspace mengizinkan semua inference geo dan menggunakan `"global"` sebagai inference geo default-nya. Claude Console menampilkan kedua pengaturan tersebut sebagai hanya-baca. Untuk inferensi khusus AS, tetapkan `inference_geo: "us"` pada setiap permintaan.
</Note>

## Workspace geo

Workspace geo ditetapkan saat Anda membuat workspace dan tidak dapat diubah setelahnya. Saat ini, `"us"` adalah satu-satunya workspace geo yang tersedia.

Untuk menetapkan workspace geo, buat workspace baru di [Console](https://platform.claude.com/):

1. Buka [Workspaces di Claude Console](https://platform.claude.com/settings/workspaces) (`platform.claude.com/settings/workspaces`).
2. Klik **Create workspace** untuk membuka halaman [Create workspace](https://platform.claude.com/settings/workspaces/new) (`platform.claude.com/settings/workspaces/new`) di Console.
3. Masukkan nama, konfirmasikan nilai di field **Workspace geo**, lalu klik **Create workspace**.

<Note>
  **Claude Platform on AWS:** Workspace geo tidak dapat dikonfigurasi. Sesi Claude Managed Agents di platform ini berjalan dengan Workspace geo efektif `"us"`, yang saat ini merupakan satu-satunya workspace geo yang tersedia. Lihat [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) untuk pertimbangan residensi data yang khusus untuk platform tersebut.
</Note>

<Note>
  **Claude Models on Google Cloud (Anthropic managed):** Workspace geo tidak dapat dikonfigurasi. Setiap workspace menggunakan `"us"` sebagai workspace geo-nya, dan field **Workspace geo** tidak muncul di Claude Console.
</Note>

## Harga

Harga residensi data bervariasi menurut generasi model:

* **Model Claude 4.6 dan yang lebih baru:** Inferensi khusus AS (`inference_geo: "us"`) dikenakan harga 1,1x tarif standar di semua kategori harga token (token input, token output, penulisan cache, dan pembacaan cache). Pada Claude Haiku 5.5, pengali ini juga berlaku untuk harga yang lebih tinggi bagi prompt di atas 100.000 token (lihat [Harga konteks panjang](https://platform.claude.com/docs/id/about-claude/pricing#long-context-pricing)).
* **Perutean global (`inference_geo: "global"`):** Harga standar berlaku.
* **Model yang lebih lama:** Tidak mendukung `inference_geo` (lihat [Ketersediaan model](https://platform.claude.com/docs/id/manage-claude/data-residency#model-availability)). Harga standar berlaku. Permintaan yang menyertakan parameter ini akan mengembalikan error 400.

Harga ini berlaku untuk Claude API (first-party), Claude Platform on AWS, dan Claude Models on Google Cloud (Anthropic managed). Di Claude in Microsoft Foundry, pengali 1,1x yang sama berlaku untuk deployment yang di-host di Azure yang menggunakan jenis deployment US Data Zone Standard. Platform yang dioperasikan mitra, yaitu Bedrock dan Claude Models on Google Cloud (Google managed), memiliki harga regional masing-masing. Lihat [Harga residensi data](https://platform.claude.com/docs/id/about-claude/pricing#data-residency-pricing) untuk detailnya.

Pengali yang sama berlaku untuk [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview): ketika [konfigurasi model](https://platform.claude.com/docs/id/managed-agents/agent-setup) agen menetapkan `inference_geo` ke `"us"`, permintaan model dalam sesi yang menjalankan agen tersebut dikenakan harga 1,1x tarif standar.

<Note>
  Jika Anda memiliki komitmen [Priority Tier](https://platform.claude.com/docs/id/api/service-tiers), pengali 1,1x untuk inferensi khusus AS juga memengaruhi cara token dihitung terhadap kapasitas Priority Tier Anda. Setiap token yang dikonsumsi dengan `inference_geo: "us"` mengurangi 1,1 token dari TPM yang Anda komitmenkan, konsisten dengan cara pengali harga lainnya (seperti caching prompt) memengaruhi laju pengurangan.
</Note>

## Dukungan Batch API

Parameter `inference_geo` didukung pada [Batch API](https://platform.claude.com/docs/id/build-with-claude/batch-processing). Setiap permintaan dalam batch dapat menentukan nilai `inference_geo`-nya sendiri.

## Migrasi dari opt-out lama

Jika organisasi Anda sebelumnya memilih keluar (opt-out) dari perutean global untuk menjaga inferensi tetap di AS, workspace Anda telah dikonfigurasi secara otomatis dengan `allowed_inference_geos: ["us"]` dan `default_inference_geo: "us"`. Tidak diperlukan perubahan kode. Persyaratan residensi data Anda yang ada tetap diberlakukan melalui kontrol geo yang baru.

### Apa yang berubah

Opt-out lama adalah pengaturan tingkat organisasi yang membatasi semua permintaan ke infrastruktur berbasis AS. Kontrol residensi data yang baru menggantikannya dengan dua mekanisme:

* **Kontrol per permintaan:** Parameter `inference_geo` memungkinkan Anda menentukan `"us"` atau `"global"` pada setiap panggilan API, memberi Anda fleksibilitas di tingkat permintaan.
* **Kontrol workspace:** Pengaturan `default_inference_geo` dan `allowed_inference_geos` di Console memungkinkan Anda memberlakukan kebijakan geo di semua kunci dalam workspace.

### Apa yang terjadi pada workspace Anda

Workspace Anda dimigrasikan secara otomatis:

| Pengaturan lama                    | Padanan baru                                                    |
| ---------------------------------- | --------------------------------------------------------------- |
| Opt-out perutean global (hanya AS) | `allowed_inference_geos: ["us"]`, `default_inference_geo: "us"` |

Semua permintaan API yang menggunakan kunci dari workspace Anda tetap berjalan di infrastruktur berbasis AS. Tidak diperlukan tindakan apa pun untuk mempertahankan perilaku Anda saat ini.

### Jika Anda ingin menggunakan perutean global

Jika persyaratan residensi data Anda telah berubah dan Anda ingin memanfaatkan perutean global untuk kinerja dan ketersediaan yang lebih baik, perbarui pengaturan inference geo workspace Anda untuk menyertakan `"global"` dalam geo yang diizinkan dan tetapkan `default_inference_geo` ke `"global"`. Lihat [Pembatasan tingkat workspace](https://platform.claude.com/docs/id/manage-claude/data-residency#workspace-level-restrictions) untuk detailnya.

### Dampak harga

Model lama tidak terpengaruh oleh migrasi ini. Untuk harga terkini pada model yang lebih baru, lihat [Harga](https://platform.claude.com/docs/id/manage-claude/data-residency#pricing).

## Keterbatasan saat ini

* **Batas laju bersama:** Batas laju dibagikan di semua geo.
* **Inference geo:** Hanya `"us"` dan `"global"` yang tersedia.
* **Workspace geo:** Saat ini hanya `"us"` yang tersedia. Workspace geo tidak dapat diubah setelah workspace dibuat.

## Langkah selanjutnya

<CardGroup>
  <Card title="Harga residensi data" icon="dollar-sign" href="https://platform.claude.com/docs/id/about-claude/pricing#data-residency-pricing">
    Lihat detail harga residensi data.
  </Card>

  <Card title="Workspace" icon="building" href="https://platform.claude.com/docs/id/manage-claude/workspaces">
    Pelajari tentang konfigurasi workspace.
  </Card>

  <Card title="Usage and Cost Analytics API" icon="chart" href="https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api">
    Lacak penggunaan dan biaya berdasarkan inference geo.
  </Card>
</CardGroup>

## Ketersediaan

Residensi data tersedia di model tertentu dan layak untuk retensi data nol dan kesiapan HIPAA.

### Dukungan API

#### [Messages API](https://platform.claude.com/docs/id/build-with-claude/working-with-messages)

* Ketersediaan: Tersedia
* Penggunaan: Atur `inference_geo` pada setiap permintaan, atau atur default untuk workspace.

| Status               | Platform cloud                                                                                                                                             | Model                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tersedia             | Claude API                                                                                                                                                 | [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview), [Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/overview), [Claude Mythos 5](https://platform.claude.com/docs/id/models/mythos-5/overview), Claude Mythos Preview, [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview), [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview), [Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-4-7/overview), [Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-4-6/overview), [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/sonnet-4-6/overview) |
| Tersedia<sup>1</sup> | [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)                                                     | [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/overview), [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview), [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview), [Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-4-7/overview), [Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-4-6/overview), [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/sonnet-4-6/overview)                                                                                                                                                                                              |
| Tersedia<sup>1</sup> | [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed) | [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/overview), [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview), [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview), [Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-4-7/overview), [Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-4-6/overview), [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/sonnet-4-6/overview)                                                                                                                                                                                              |

1. Geo workspace tidak dapat dikonfigurasi.

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tersedia
* Penggunaan: Tetapkan `inference_geo` dalam konfigurasi model agen, dan override per sesi saat pembuatan sesi. Agen tanpa penetapan mengikuti default workspace.

| Status               | Platform cloud                                                                                         | Model                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tersedia             | Claude API                                                                                             | [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Mythos 5.1](https://platform.claude.com/docs/id/models/mythos-5-1/overview), [Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/overview), [Claude Mythos 5](https://platform.claude.com/docs/id/models/mythos-5/overview), Claude Mythos Preview, [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview), [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview), [Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-4-7/overview), [Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-4-6/overview), [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/sonnet-4-6/overview) |
| Tersedia<sup>1</sup> | [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws) | [Claude Fable 5.1](https://platform.claude.com/docs/id/models/fable-5-1/overview), [Claude Fable 5](https://platform.claude.com/docs/id/models/fable-5/overview), [Claude Opus 5.5](https://platform.claude.com/docs/id/models/opus-5-5/overview), [Claude Opus 5](https://platform.claude.com/docs/id/models/opus-5/overview), [Claude Sonnet 5.5](https://platform.claude.com/docs/id/models/sonnet-5-5/overview), [Claude Sonnet 5](https://platform.claude.com/docs/id/models/sonnet-5/overview), [Claude Haiku 5.5](https://platform.claude.com/docs/id/models/haiku-5-5/overview), [Claude Opus 4.8](https://platform.claude.com/docs/id/models/opus-4-8/overview), [Claude Opus 4.7](https://platform.claude.com/docs/id/models/opus-4-7/overview), [Claude Opus 4.6](https://platform.claude.com/docs/id/models/opus-4-6/overview), [Claude Sonnet 4.6](https://platform.claude.com/docs/id/models/sonnet-4-6/overview)                                                                                                                                                                                              |

1. Geo workspace tidak dapat dikonfigurasi; sesi Managed Agents di sana berjalan dengan geo workspace “us”.

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                 | HIPAA |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| Status | Layak (tidak termasuk [Model yang dicakup](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#model-specific-data-retention-requirements)) | Layak |

Endpoint yang berlaku:

* `/v1/messages` dengan `inference_geo`
