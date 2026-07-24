---
source: platform
url: https://platform.claude.com/docs/id/api/service-tiers
fetched_at: 2026-07-24T03:08:28.781260Z
sha256: a2346847b3a8afd4fbcebe23bf74f99e58fae1c3f14b7b54e05367d885854989
---

# Tingkat layanan

Tingkat layanan yang berbeda memungkinkan Anda menyeimbangkan ketersediaan, kinerja, dan biaya yang dapat diprediksi berdasarkan kebutuhan aplikasi Anda.

---

<Warning>
  Komitmen kapasitas Priority Tier tidak lagi tersedia untuk dibeli. Organisasi dengan komitmen yang sudah ada dapat terus menggunakan Priority Tier hingga tanggal berakhir kontrak mereka, dan halaman ini tetap tersedia sebagai referensi bagi mereka. Jika Anda memerlukan kapasitas yang terjamin, [hubungi tim penjualan](https://claude.com/contact-sales).
</Warning>

Anthropic menawarkan tiga tingkat layanan:

* **Priority Tier:** Hanya tersedia untuk organisasi dengan komitmen kapasitas yang sudah ada
* **Standard:** Tingkat default untuk uji coba maupun penskalaan kasus penggunaan sehari-hari
* **Batch:** Terbaik untuk alur kerja asinkron yang dapat menunggu atau mendapat manfaat dari berada di luar kapasitas normal Anda

## Tingkat Standard

Tingkat standard adalah tingkat layanan default untuk semua permintaan API. API memprioritaskan permintaan ini bersama semua permintaan lainnya dengan ketersediaan upaya terbaik (best-effort).

## Priority Tier

API memprioritaskan permintaan di tingkat ini di atas semua permintaan lainnya. Prioritisasi ini membantu meminimalkan [kesalahan "server overloaded"](/docs/id/api/errors#http-errors), bahkan selama waktu puncak.

Untuk informasi lebih lanjut, lihat [Komitmen Priority Tier yang sudah ada](#existing-priority-tier-commitments).

## Bagaimana permintaan ditetapkan ke tingkat tertentu

Saat menangani permintaan, Anthropic memutuskan untuk menetapkan permintaan ke Priority Tier dalam skenario berikut:

* Organisasi Anda memiliki kapasitas Priority Tier yang cukup untuk token **input** per menit
* Organisasi Anda memiliki kapasitas Priority Tier yang cukup untuk token **output** per menit

Anthropic menghitung penggunaan terhadap kapasitas Priority Tier sebagai berikut:

**Token input**

* Pembacaan cache dihitung sebagai 0,1 token per token yang dibaca dari cache
* Penulisan cache dihitung sebagai 1,25 token per token yang ditulis ke cache dengan TTL 5 menit
* Penulisan cache dihitung sebagai 2,00 token per token yang ditulis ke cache dengan TTL 1 jam
* Untuk permintaan [inferensi khusus AS](/docs/id/manage-claude/data-residency) (`inference_geo: "us"`) pada Claude Opus 4.6, Claude Sonnet 4.6, dan model yang lebih baru, token input dihitung sebagai 1,1 token per token
* Semua token input lainnya dihitung sebagai 1 token per token

**Token output**

* Untuk permintaan [inferensi khusus AS](/docs/id/manage-claude/data-residency) (`inference_geo: "us"`) pada Claude Opus 4.6, Claude Sonnet 4.6, dan model yang lebih baru, token output dihitung sebagai 1,1 token per token
* Semua token output lainnya dihitung sebagai 1 token per token

Jika tidak, permintaan diproses pada tingkat standard.

<Note>
  Tarif pengurangan (burndown rate) ini mencerminkan harga relatif dari setiap jenis token. Misalnya, inferensi khusus AS dihargai 1,1x pada Opus 4.6, Sonnet 4.6, dan model yang lebih baru, sehingga setiap token yang dikonsumsi dengan `inference_geo: "us"` mengurangi 1,1 token dari kapasitas Priority Tier Anda.
</Note>

<Note>
  Permintaan yang ditetapkan ke Priority Tier mengambil dari kapasitas Priority Tier dan batas laju reguler. Jika melayani permintaan tersebut akan melebihi batas laju, permintaan akan ditolak.
</Note>

## Menggunakan tingkat layanan

Anda dapat mengontrol tingkat layanan mana yang dapat digunakan untuk sebuah permintaan dengan mengatur parameter `service_tier`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude!"}],
      "service_tier": "auto"
    }'
  ```

  ```bash CLI
  ant messages create \
    --transform usage.service_tier \
    --raw-output <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content: Hello, Claude!
  service_tier: auto  # Automatically use Priority Tier when available, fallback to standard
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude!"}],
      service_tier="auto",  # Automatically use Priority Tier when available, fallback to standard
  )
  print(message.usage.service_tier)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude!" }],
    service_tier: "auto" // Automatically use Priority Tier when available, fallback to standard
  });
  console.log(message.usage.service_tier);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var message = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello, Claude!" }],
      ServiceTier = ServiceTier.Auto, // Automatically use Priority Tier when available, fallback to standard
  });
  Console.WriteLine(message.Usage.ServiceTier);
  ```

  ```go Go
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude!")),
  	},
  	// Secara otomatis menggunakan Priority Tier jika tersedia, kembali ke standar jika tidak
  	ServiceTier: anthropic.MessageNewParamsServiceTierAuto,
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(message.Usage.ServiceTier)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024L)
      .addUserMessage("Hello, Claude!")
      // Secara otomatis menggunakan Priority Tier jika tersedia, kembali ke standar jika tidak
      .serviceTier(MessageCreateParams.ServiceTier.AUTO)
      .build();

  Message message = client.messages().create(params);
  IO.println(message.usage().serviceTier().orElseThrow());
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude!']],
      serviceTier: 'auto', // Automatically use Priority Tier when available, fallback to standard
  );
  echo $message->usage->serviceTier;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude!" }],
    service_tier: :auto # Automatically use Priority Tier when available, fallback to standard
  )
  puts(message.usage.service_tier)
  ```
</CodeGroup>

Parameter `service_tier` menerima nilai-nilai berikut:

* `"auto"` (default) - Menggunakan kapasitas Priority Tier jika tersedia, dan beralih ke kapasitas lain Anda jika tidak
* `"standard_only"` - Hanya menggunakan kapasitas tingkat standard, berguna jika Anda tidak ingin menggunakan kapasitas Priority Tier Anda

Objek `usage` pada respons juga menyertakan tingkat layanan yang ditetapkan untuk permintaan tersebut:

```json
{
  "usage": {
    "input_tokens": 410,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "output_tokens": 585,
    "service_tier": "priority"
  }
}
```

Ini memungkinkan Anda menentukan tingkat layanan mana yang ditetapkan untuk permintaan tersebut.

Saat meminta `service_tier="auto"` dengan model yang memiliki komitmen Priority Tier, header respons berikut memberikan wawasan:

```text wrap
anthropic-priority-input-tokens-limit: 10000
anthropic-priority-input-tokens-remaining: 9618
anthropic-priority-input-tokens-reset: 2025-01-12T23:11:59Z
anthropic-priority-output-tokens-limit: 10000
anthropic-priority-output-tokens-remaining: 6000
anthropic-priority-output-tokens-reset: 2025-01-12T23:12:21Z
```

Anda dapat menggunakan keberadaan header ini untuk mendeteksi apakah permintaan Anda memenuhi syarat untuk Priority Tier, bahkan jika melebihi batas.

## Komitmen Priority Tier yang sudah ada

Komitmen Priority Tier terdiri dari:

* Jumlah token input per menit
* Jumlah token output per menit
* Durasi komitmen (1, 3, 6, atau 12 bulan)
* Versi model tertentu

Priority Tier menargetkan waktu aktif (uptime) 99,5% dengan sumber daya komputasi yang diprioritaskan. Permintaan yang melebihi kapasitas komitmen Anda secara otomatis beralih ke tingkat standard.

### Model yang didukung

Priority Tier didukung pada semua model Claude yang tersedia (termasuk Claude Fable 5 dan Claude Opus 4.8) kecuali Claude Sonnet 5, [Claude Mythos Preview](https://anthropic.com/glasswing), dan Claude Mythos 5.

Lihat [Ikhtisar model](/docs/id/about-claude/models/overview) untuk detail lebih lanjut tentang model yang tersedia.
