---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/rate-limits-api
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: 9c1db395b6b67a0a9180a17d55e67c0837bc8e2319cd394129fed2b1039169c0
---

---
title: Rate Limits API
url: https://platform.claude.com/docs/id/manage-claude/rate-limits-api
description: Baca batas laju API organisasi Anda secara terprogram dan atur batas laju workspace dengan Rate Limits API.
---

<Tip>
  **Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, siapkan organisasi Anda di halaman [Organization](https://platform.claude.com/settings/organization) (`platform.claude.com/settings/organization`) di Claude Console.
</Tip>

Rate Limits API menyediakan akses terprogram ke “rate limit” (batas laju) yang dikonfigurasi untuk organisasi Anda dan workspace-nya. Ini adalah informasi yang sama dengan yang ditampilkan di halaman [Rate limits](https://platform.claude.com/usage/limits) di Claude Console. Anda juga dapat menggunakannya untuk mengatur dan menghapus batas laju sebuah workspace.

Gunakan API ini untuk:

* **Menjaga gateway dan proxy tetap sinkron:** Baca batas Anda saat ini ketika startup dan secara terjadwal alih-alih melakukan hardcode nilai yang akan menyimpang ketika Anthropic menyesuaikannya.
* **Mendukung peringatan internal:** Bandingkan data penggunaan dari [Usage and Cost Analytics API](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api) dengan batas yang telah Anda konfigurasi.
* **Mengaudit konfigurasi workspace:** Verifikasi bahwa override workspace sesuai dengan yang diharapkan oleh otomatisasi provisioning Anda.
* **Kelola batas workspace dari kode:** Atur dan hapus batas setiap workspace dari otomatisasi provisioning Anda alih-alih mengeditnya di Console.

<Check>
  **Kredensial Admin API diperlukan.** Endpoint ini merupakan bagian dari Admin API. Anda dapat mengaksesnya menggunakan [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys), token OAuth dengan cakupan `org:admin`, atau kunci akun pribadi maupun akun layanan yang tidak dibatasi pada suatu workspace; kunci API workspace tidak dapat digunakan. Lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/admin-api#authentication) untuk detailnya.
</Check>

Contoh SDK dan CLI di halaman ini membuat klien default, yang membaca kunci Admin API dari variabel lingkungan `ANTHROPIC_API_KEY`. SDK mengekspos endpoint ini sebagai `client.organization.rate_limits` (typescript: `client.organization.rateLimits`; csharp, go: `client.Organization.RateLimits`; java: `client.organization().rateLimits()`; php: `$client->organization->rateLimits`) dan `client.organization.workspaces.rate_limits` (typescript: `client.organization.workspaces.rateLimits`; csharp, go: `client.Organization.Workspaces.RateLimits`; java: `client.organization().workspaces().rateLimits()`; php: `$client->organization->workspaces->rateLimits`); metode list di Python, TypeScript, C#, Go, dan Java mengembalikan iterator yang mengikuti `next_page` untuk Anda, sedangkan contoh PHP, Ruby, dan curl membaca satu halaman.

## Mulai cepat

Tampilkan daftar batas laju yang dikonfigurasi untuk organisasi Anda:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rate_limits" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:rate-limits list
  ```

  ```python Python
  client = anthropic.Anthropic()

  rate_limits = client.organization.rate_limits.list()

  for entry in rate_limits:
      models = f" ({', '.join(entry.models)})" if entry.models else ""
      print(f"{entry.group.type}{models}")
      for limit in entry.limits:
          print(f"  {limit.type}: {limit.value}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rateLimits = await client.organization.rateLimits.list();

  for await (const entry of rateLimits) {
    const models = entry.models ? ` (${entry.models.join(", ")})` : "";
    console.log(`${entry.group.type}${models}`);
    for (const limit of entry.limits) {
      console.log(`  ${limit.type}: ${limit.value}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var rateLimits = await client.Organization.RateLimits.List();

  await foreach (var entry in rateLimits.Paginate())
  {
      var models = entry.Models is null ? "" : $" ({string.Join(", ", entry.Models)})";
      Console.WriteLine($"{entry.Group.Type.Raw()}{models}");
      foreach (var limit in entry.Limits)
      {
          Console.WriteLine($"  {limit.Type}: {limit.Value}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rateLimits := client.Organization.RateLimits.ListAutoPaging(context.Background(), anthropic.OrganizationRateLimitListParams{})

  for rateLimits.Next() {
  	entry := rateLimits.Current()
  	models := ""
  	if len(entry.Models) > 0 {
  		models = fmt.Sprintf(" (%s)", strings.Join(entry.Models, ", "))
  	}
  	fmt.Printf("%s%s\n", entry.Group.Type, models)
  	for _, limit := range entry.Limits {
  		fmt.Printf("  %s: %d\n", limit.Type, limit.Value)
  	}
  }
  if err := rateLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var rateLimits = client.organization().rateLimits().list();

  for (var entry : rateLimits.autoPager()) {
      var models = entry.models()
          .map(modelIds -> " (" + String.join(", ", modelIds) + ")")
          .orElse("");
      IO.println(entry.group().type().asString() + models);
      for (var limit : entry.limits()) {
          IO.println("  " + limit.type() + ": " + limit.value());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rateLimits = $client->organization->rateLimits->list();

  foreach ($rateLimits->data as $entry) {
      $models = $entry->models ? ' (' . implode(', ', $entry->models) . ')' : '';
      echo "{$entry->group->type}{$models}\n";
      foreach ($entry->limits as $limit) {
          echo "  {$limit->type}: {$limit->value}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rate_limits = client.organization.rate_limits.list

  rate_limits.data.each do |entry|
    models = entry.models ? " (#{entry.models.join(", ")})" : ""
    puts "#{entry.group.type}#{models}"
    entry.limits.each do |limit|
      puts "  #{limit.type}: #{limit.value}"
    end
  end
  ```
</CodeGroup>

## Batas laju organisasi

Endpoint `/v1/organizations/rate_limits` mengembalikan batas laju yang diterapkan pada tingkat organisasi untuk Messages API dan sumber daya pendukungnya. Batas untuk produk lain, seperti [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak disertakan.

### Konsep utama

* **Grup batas laju:** Setiap entri dalam respons mewakili satu grup batas laju. Batas laju model dikelompokkan sehingga beberapa versi model berbagi satu set batas yang sama, dan grup lainnya mencakup sumber daya seperti Message Batches API, Files API, Token Counting API, agent skills, dan alat web search.
* **Objek `group`:** Ada di setiap entri, objek ini mengidentifikasi grup batas laju tempat entri tersebut berlaku. Objek ini selalu memiliki `type`, yang merupakan salah satu nilai `group_type`, dan `id`, sebuah pengidentifikasi opak dengan awalan `rlg_`. Pada entri `model_group`, objek ini juga memiliki `display_name`, label Anthropic saat ini untuk grup tersebut, seperti `Claude Sonnet 4.x`. Label ini hanya untuk tampilan dan dapat berubah. Tipe grup lainnya tidak memiliki `display_name`.
* **`id` di dalam `group`:** Sebuah grup memiliki `id` yang sama di setiap organisasi dan di setiap override workspace, dan tidak pernah berubah. Gunakan untuk mencocokkan entri antar organisasi atau dengan katalog Anda sendiri. `id` milik entri itu sendiri berbeda per organisasi, dan `models` berubah ketika Anthropic memindahkan model antar grup. Keduanya bukan kunci yang stabil untuk grup.
* **`group_type`:** Parameter kueri yang membatasi daftar ke satu tipe grup. Lihat [Memfilter berdasarkan tipe grup](https://platform.claude.com/docs/id/manage-claude/rate-limits-api#filtering-by-group-type) untuk nilai-nilainya.
* **Daftar `models`:** Untuk entri `model_group`, field `models` mencantumkan setiap ID model dan alias yang dihitung terhadap batas grup tersebut. Gunakan daftar ini untuk mencari grup mana yang mencakup string model apa pun. Untuk tipe grup lainnya, `models` bernilai `null`.
* **Daftar `limits`:** Setiap grup membawa daftar pasangan `{type, value}`. Field `type` mengidentifikasi limiter (seperti `requests_per_minute`, `input_tokens_per_minute`, atau `output_tokens_per_minute`) dan `value` adalah batas yang dikonfigurasi. Lihat [Batas laju](https://platform.claude.com/docs/id/api/rate-limits) untuk cara setiap limiter diukur dan diberlakukan.
* **`source` pada batas workspace:** Pada endpoint workspace, setiap nilai batas juga membawa `source`, yang menyatakan asal `value`: `{"type": "workspace"}` untuk override yang disimpan pada workspace, atau `{"type": "organization"}` untuk nilai yang diwarisi dari organisasi. Secara default, endpoint workspace hanya mengembalikan override, sehingga `source.type` selalu `workspace` di sana; nilai yang diwarisi muncul ketika Anda meneruskan `include_inherited=true`. Lihat [Batas laju workspace](https://platform.claude.com/docs/id/manage-claude/rate-limits-api#workspace-rate-limits).

Untuk detail parameter lengkap dan skema respons, lihat [referensi Organization Rate Limits API](https://platform.claude.com/docs/id/api/organization/rate_limits/list).

### Menampilkan semua batas laju organisasi

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rate_limits" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:rate-limits list
  ```

  ```python Python
  client = anthropic.Anthropic()

  rate_limits = client.organization.rate_limits.list()

  for entry in rate_limits:
      models = f" ({', '.join(entry.models)})" if entry.models else ""
      print(f"{entry.group.type}{models}")
      for limit in entry.limits:
          print(f"  {limit.type}: {limit.value}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rateLimits = await client.organization.rateLimits.list();

  for await (const entry of rateLimits) {
    const models = entry.models ? ` (${entry.models.join(", ")})` : "";
    console.log(`${entry.group.type}${models}`);
    for (const limit of entry.limits) {
      console.log(`  ${limit.type}: ${limit.value}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var rateLimits = await client.Organization.RateLimits.List();

  await foreach (var entry in rateLimits.Paginate())
  {
      var models = entry.Models is null ? "" : $" ({string.Join(", ", entry.Models)})";
      Console.WriteLine($"{entry.Group.Type.Raw()}{models}");
      foreach (var limit in entry.Limits)
      {
          Console.WriteLine($"  {limit.Type}: {limit.Value}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rateLimits := client.Organization.RateLimits.ListAutoPaging(context.Background(), anthropic.OrganizationRateLimitListParams{})

  for rateLimits.Next() {
  	entry := rateLimits.Current()
  	models := ""
  	if len(entry.Models) > 0 {
  		models = fmt.Sprintf(" (%s)", strings.Join(entry.Models, ", "))
  	}
  	fmt.Printf("%s%s\n", entry.Group.Type, models)
  	for _, limit := range entry.Limits {
  		fmt.Printf("  %s: %d\n", limit.Type, limit.Value)
  	}
  }
  if err := rateLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var rateLimits = client.organization().rateLimits().list();

  for (var entry : rateLimits.autoPager()) {
      var models = entry.models()
          .map(modelIds -> " (" + String.join(", ", modelIds) + ")")
          .orElse("");
      IO.println(entry.group().type().asString() + models);
      for (var limit : entry.limits()) {
          IO.println("  " + limit.type() + ": " + limit.value());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rateLimits = $client->organization->rateLimits->list();

  foreach ($rateLimits->data as $entry) {
      $models = $entry->models ? ' (' . implode(', ', $entry->models) . ')' : '';
      echo "{$entry->group->type}{$models}\n";
      foreach ($entry->limits as $limit) {
          echo "  {$limit->type}: {$limit->value}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rate_limits = client.organization.rate_limits.list

  rate_limits.data.each do |entry|
    models = entry.models ? " (#{entry.models.join(", ")})" : ""
    puts "#{entry.group.type}#{models}"
    entry.limits.each do |limit|
      puts "  #{limit.type}: #{limit.value}"
    end
  end
  ```
</CodeGroup>

```json
{
  "data": [
    {
      "id": "rlt_01NwFawrTvAijwqn8AjKVBPS",
      "type": "rate_limit",
      "group_type": "model_group",
      "group": {
        "type": "model_group",
        "id": "rlg_01Hq7YkP3mZ9dTwRx4cVbN2s",
        "display_name": "Claude Opus 5.5"
      },
      "models": ["claude-opus-5-5"],
      "limits": [
        { "type": "requests_per_minute", "value": 4000 },
        { "type": "input_tokens_per_minute", "value": 10000000 },
        { "type": "output_tokens_per_minute", "value": 800000 }
      ]
    },
    {
      "id": "rlt_016qriyigbdebqkzhMujdHkX",
      "type": "rate_limit",
      "group_type": "model_group",
      "group": {
        "type": "model_group",
        "id": "rlg_01Kd5wMv8nSq2LcXy6tRfJ4b",
        "display_name": "Claude Opus 4.x"
      },
      "models": [
        "claude-opus-4-5",
        "claude-opus-4-5-20251101",
        "claude-opus-4-6",
        "claude-opus-4-7",
        "claude-opus-4-8"
      ],
      "limits": [
        { "type": "requests_per_minute", "value": 4000 },
        { "type": "input_tokens_per_minute", "value": 10000000 },
        { "type": "output_tokens_per_minute", "value": 800000 }
      ]
    },
    {
      "id": "rlt_01EyY8kq14eviKJPgepbgBH4",
      "type": "rate_limit",
      "group_type": "batch",
      "group": { "type": "batch", "id": "rlg_01Wn3pBz6kCg9vHtQ7mLxD5a" },
      "models": null,
      "limits": [{ "type": "enqueued_batch_requests", "value": 500000 }]
    }
  ],
  "next_page": null
}
```

### Mencari batas untuk model tertentu

Berikan ID model atau alias apa pun sebagai parameter kueri `model` untuk hanya mengembalikan entri yang memuatnya:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rate_limits?model=claude-opus-5-5" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:rate-limits list --model claude-opus-5-5
  ```

  ```python Python
  client = anthropic.Anthropic()

  rate_limits = client.organization.rate_limits.list(model="claude-opus-5-5")

  for entry in rate_limits:
      models = f" ({', '.join(entry.models)})" if entry.models else ""
      print(f"{entry.group.type}{models}")
      for limit in entry.limits:
          print(f"  {limit.type}: {limit.value}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rateLimits = await client.organization.rateLimits.list({
    model: "claude-opus-5-5"
  });

  for await (const entry of rateLimits) {
    const models = entry.models ? ` (${entry.models.join(", ")})` : "";
    console.log(`${entry.group.type}${models}`);
    for (const limit of entry.limits) {
      console.log(`  ${limit.type}: ${limit.value}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var rateLimits = await client.Organization.RateLimits.List(new()
  {
      Model = "claude-opus-5-5"
  });

  await foreach (var entry in rateLimits.Paginate())
  {
      var models = entry.Models is null ? "" : $" ({string.Join(", ", entry.Models)})";
      Console.WriteLine($"{entry.Group.Type.Raw()}{models}");
      foreach (var limit in entry.Limits)
      {
          Console.WriteLine($"  {limit.Type}: {limit.Value}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rateLimits := client.Organization.RateLimits.ListAutoPaging(context.Background(), anthropic.OrganizationRateLimitListParams{
  	Model: anthropic.String(anthropic.ModelClaudeOpus5_5),
  })

  for rateLimits.Next() {
  	entry := rateLimits.Current()
  	models := ""
  	if len(entry.Models) > 0 {
  		models = fmt.Sprintf(" (%s)", strings.Join(entry.Models, ", "))
  	}
  	fmt.Printf("%s%s\n", entry.Group.Type, models)
  	for _, limit := range entry.Limits {
  		fmt.Printf("  %s: %d\n", limit.Type, limit.Value)
  	}
  }
  if err := rateLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.organization.ratelimits.RateLimitListParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = RateLimitListParams.builder()
          .model(Model.CLAUDE_OPUS_5_5.asString())
          .build();
      var rateLimits = client.organization().rateLimits().list(params);

      for (var entry : rateLimits.autoPager()) {
          var models = entry.models()
              .map(modelIds -> " (" + String.join(", ", modelIds) + ")")
              .orElse("");
          IO.println(entry.group().type().asString() + models);
          for (var limit : entry.limits()) {
              IO.println("  " + limit.type() + ": " + limit.value());
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Messages\Model;

  $client = new Client();

  $rateLimits = $client->organization->rateLimits->list(
      model: Model::CLAUDE_OPUS_5_5->value,
  );

  foreach ($rateLimits->data as $entry) {
      $models = $entry->models ? ' (' . implode(', ', $entry->models) . ')' : '';
      echo "{$entry->group->type}{$models}\n";
      foreach ($entry->limits as $limit) {
          echo "  {$limit->type}: {$limit->value}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rate_limits = client.organization.rate_limits.list(model: Anthropic::Model::CLAUDE_OPUS_5_5)

  rate_limits.data.each do |entry|
    models = entry.models ? " (#{entry.models.join(", ")})" : ""
    puts "#{entry.group.type}#{models}"
    entry.limits.each do |limit|
      puts "  #{limit.type}: #{limit.value}"
    end
  end
  ```
</CodeGroup>

Jika string model tidak cocok dengan grup mana pun, endpoint mengembalikan error 404. Setiap model yang dapat diakses oleh organisasi Anda cocok dengan grupnya. Parameter `model` hanya didukung pada endpoint organisasi; endpoint workspace tidak menerimanya.

## Batas laju workspace

Endpoint `/v1/organizations/workspaces/{workspace_id}/rate_limits` mengembalikan override batas laju yang dikonfigurasi untuk satu workspace. Untuk juga melihat nilai yang diwarisi workspace, berikan `include_inherited=true` (lihat [Sertakan nilai yang diwarisi](https://platform.claude.com/docs/id/manage-claude/rate-limits-api#include-inherited-values)). Untuk mengubah override, lihat [Mengatur batas laju workspace](https://platform.claude.com/docs/id/manage-claude/rate-limits-api#set-workspace-rate-limits).

Secara default, respons hanya menyertakan override, sehingga apa pun yang tidak ada di dalamnya diwarisi dari organisasi:

* Grup yang tidak ada di `data` sama sekali tidak memiliki override workspace. Workspace mewarisi batas tingkat organisasi untuk grup tersebut (bukan tanpa batas).
* Di dalam grup yang ada, tipe limiter yang tidak ada di `limits[]` tidak memiliki override workspace untuk limiter tersebut. Workspace mewarisi nilai organisasi untuknya.
* Untuk setiap limiter yang ada, `org_limit` adalah nilai tingkat organisasi untuk limiter yang sama, atau `null` jika organisasi tidak memiliki batas yang dikonfigurasi untuk tipe limiter tersebut, dan `source` adalah `{"type": "workspace"}`.

Untuk detail parameter lengkap dan skema respons, lihat [referensi Workspace Rate Limits API](https://platform.claude.com/docs/id/api/organization/workspaces/rate_limits/list).

<Tip>
  Untuk mengambil ID workspace organisasi Anda, gunakan endpoint [List Workspaces](https://platform.claude.com/docs/id/api/organization/workspaces/list), atau temukan di [Claude Console](https://platform.claude.com/settings/workspaces). List Workspaces menyertakan workspace default hanya ketika Anda meneruskan `include_default=true`.
</Tip>

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/rate_limits" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:workspaces:rate-limits list \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
  ```

  ```python Python
  client = anthropic.Anthropic()

  rate_limits = client.organization.workspaces.rate_limits.list(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  )

  for entry in rate_limits:
      models = f" ({', '.join(entry.models)})" if entry.models else ""
      print(f"{entry.group.type}{models}")
      for limit in entry.limits:
          print(f"  {limit.type}: {limit.value}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rateLimits = await client.organization.workspaces.rateLimits.list(
    "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  );

  for await (const entry of rateLimits) {
    const models = entry.models ? ` (${entry.models.join(", ")})` : "";
    console.log(`${entry.group.type}${models}`);
    for (const limit of entry.limits) {
      console.log(`  ${limit.type}: ${limit.value}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var rateLimits = await client.Organization.Workspaces.RateLimits.List(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  );

  await foreach (var entry in rateLimits.Paginate())
  {
      var models = entry.Models is null ? "" : $" ({string.Join(", ", entry.Models)})";
      Console.WriteLine($"{entry.Group.Type.Raw()}{models}");
      foreach (var limit in entry.Limits)
      {
          Console.WriteLine($"  {limit.Type}: {limit.Value}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rateLimits := client.Organization.Workspaces.RateLimits.ListAutoPaging(
  	context.Background(),
  	"wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  	anthropic.OrganizationWorkspaceRateLimitListParams{},
  )

  for rateLimits.Next() {
  	entry := rateLimits.Current()
  	models := ""
  	if len(entry.Models) > 0 {
  		models = fmt.Sprintf(" (%s)", strings.Join(entry.Models, ", "))
  	}
  	fmt.Printf("%s%s\n", entry.Group.Type, models)
  	for _, limit := range entry.Limits {
  		fmt.Printf("  %s: %d\n", limit.Type, limit.Value)
  	}
  }
  if err := rateLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var rateLimits = client.organization().workspaces().rateLimits()
      .list("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ");

  for (var entry : rateLimits.autoPager()) {
      var models = entry.models()
          .map(modelIds -> " (" + String.join(", ", modelIds) + ")")
          .orElse("");
      IO.println(entry.group().type().asString() + models);
      for (var limit : entry.limits()) {
          IO.println("  " + limit.type() + ": " + limit.value());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rateLimits = $client->organization->workspaces->rateLimits->list(
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
  );

  foreach ($rateLimits->data as $entry) {
      $models = $entry->models ? ' (' . implode(', ', $entry->models) . ')' : '';
      echo "{$entry->group->type}{$models}\n";
      foreach ($entry->limits as $limit) {
          echo "  {$limit->type}: {$limit->value}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace_id = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  rate_limits = client.organization.workspaces.rate_limits.list(workspace_id)

  rate_limits.data.each do |entry|
    models = entry.models ? " (#{entry.models.join(", ")})" : ""
    puts "#{entry.group.type}#{models}"
    entry.limits.each do |limit|
      puts "  #{limit.type}: #{limit.value}"
    end
  end
  ```
</CodeGroup>

```json
{
  "data": [
    {
      "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      "rate_limit_id": "rlt_01NwFawrTvAijwqn8AjKVBPS",
      "type": "workspace_rate_limit",
      "group_type": "model_group",
      "group": {
        "type": "model_group",
        "id": "rlg_01Hq7YkP3mZ9dTwRx4cVbN2s",
        "display_name": "Claude Opus 5.5"
      },
      "models": ["claude-opus-5-5"],
      "limits": [
        {
          "type": "requests_per_minute",
          "value": 1000,
          "org_limit": 4000,
          "source": { "type": "workspace" }
        },
        {
          "type": "input_tokens_per_minute",
          "value": 500000,
          "org_limit": 10000000,
          "source": { "type": "workspace" }
        }
      ]
    },
    {
      "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      "rate_limit_id": "rlt_016qriyigbdebqkzhMujdHkX",
      "type": "workspace_rate_limit",
      "group_type": "model_group",
      "group": {
        "type": "model_group",
        "id": "rlg_01Kd5wMv8nSq2LcXy6tRfJ4b",
        "display_name": "Claude Opus 4.x"
      },
      "models": [
        "claude-opus-4-5",
        "claude-opus-4-5-20251101",
        "claude-opus-4-6",
        "claude-opus-4-7",
        "claude-opus-4-8"
      ],
      "limits": [
        {
          "type": "requests_per_minute",
          "value": 1000,
          "org_limit": 4000,
          "source": { "type": "workspace" }
        },
        {
          "type": "input_tokens_per_minute",
          "value": 500000,
          "org_limit": 10000000,
          "source": { "type": "workspace" }
        }
      ]
    }
  ],
  "next_page": null
}
```

### Menyertakan nilai yang diwarisi

Untuk membaca batas yang berlaku pada workspace dalam satu permintaan, tambahkan parameter kueri opsional `include_inherited`. Nilai defaultnya adalah `false`; nilai yang bukan Boolean mengembalikan error 400. Dengan `include_inherited=true`:

* `data` memiliki satu entri untuk setiap grup yang berlaku pada workspace dan memiliki nilai tingkat organisasi, meskipun workspace tidak meng-override satu pun darinya. Grup model berlaku ketika workspace dapat mengakses setidaknya satu modelnya.
* `limits[]` pada setiap entri mencantumkan setiap tipe limiter yang memiliki nilai dari organisasi pada grup tersebut, ditambah tipe apa pun yang di-override oleh workspace. Setiap tipe muncul sekali, dengan override workspace jika ada yang disimpan dan nilai organisasi jika tidak, sehingga satu entri dapat mencampur keduanya.
* `source` pada setiap nilai membedakan keduanya: `{"type": "workspace"}` adalah override yang disimpan, dan `{"type": "organization"}` adalah nilai yang diwarisi, di mana `value` sama dengan `org_limit`.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/rate_limits?include_inherited=true" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:workspaces:rate-limits list \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    --include-inherited
  ```

  ```python Python
  client = anthropic.Anthropic()

  rate_limits = client.organization.workspaces.rate_limits.list(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      include_inherited=True,
  )

  for entry in rate_limits:
      models = f" ({', '.join(entry.models)})" if entry.models else ""
      print(f"{entry.group.type}{models}")
      for limit in entry.limits:
          print(f"  {limit.type}: {limit.value} ({limit.source.type})")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rateLimits = await client.organization.workspaces.rateLimits.list(
    "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
    { include_inherited: true }
  );

  for await (const entry of rateLimits) {
    const models = entry.models ? ` (${entry.models.join(", ")})` : "";
    console.log(`${entry.group.type}${models}`);
    for (const limit of entry.limits) {
      console.log(`  ${limit.type}: ${limit.value} (${limit.source.type})`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var rateLimits = await client.Organization.Workspaces.RateLimits.List(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      new() { IncludeInherited = true }
  );

  await foreach (var entry in rateLimits.Paginate())
  {
      var models = entry.Models is null ? "" : $" ({string.Join(", ", entry.Models)})";
      Console.WriteLine($"{entry.Group.Type.Raw()}{models}");
      foreach (var limit in entry.Limits)
      {
          Console.WriteLine($"  {limit.Type}: {limit.Value} ({limit.Source.Type.Raw()})");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rateLimits := client.Organization.Workspaces.RateLimits.ListAutoPaging(
  	context.Background(),
  	"wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  	anthropic.OrganizationWorkspaceRateLimitListParams{
  		IncludeInherited: anthropic.Bool(true),
  	},
  )

  for rateLimits.Next() {
  	entry := rateLimits.Current()
  	models := ""
  	if len(entry.Models) > 0 {
  		models = fmt.Sprintf(" (%s)", strings.Join(entry.Models, ", "))
  	}
  	fmt.Printf("%s%s\n", entry.Group.Type, models)
  	for _, limit := range entry.Limits {
  		fmt.Printf("  %s: %d (%s)\n", limit.Type, limit.Value, limit.Source.Type)
  	}
  }
  if err := rateLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.organization.workspaces.ratelimits.RateLimitListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = RateLimitListParams.builder()
          .includeInherited(true)
          .build();
      var rateLimits = client.organization().workspaces().rateLimits()
          .list("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ", params);

      for (var entry : rateLimits.autoPager()) {
          var models = entry.models()
              .map(modelIds -> " (" + String.join(", ", modelIds) + ")")
              .orElse("");
          IO.println(entry.group().type().asString() + models);
          for (var limit : entry.limits()) {
              IO.println("  " + limit.type() + ": " + limit.value()
                  + " (" + limit.source().type().asString() + ")");
          }
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rateLimits = $client->organization->workspaces->rateLimits->list(
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
      includeInherited: true,
  );

  foreach ($rateLimits->data as $entry) {
      $models = $entry->models ? ' (' . implode(', ', $entry->models) . ')' : '';
      echo "{$entry->group->type}{$models}\n";
      foreach ($entry->limits as $limit) {
          echo "  {$limit->type}: {$limit->value} ({$limit->source->type})\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace_id = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  rate_limits = client.organization.workspaces.rate_limits.list(workspace_id, include_inherited: true)

  rate_limits.data.each do |entry|
    models = entry.models ? " (#{entry.models.join(", ")})" : ""
    puts "#{entry.group.type}#{models}"
    entry.limits.each do |limit|
      puts "  #{limit.type}: #{limit.value} (#{limit.source.type})"
    end
  end
  ```
</CodeGroup>

```json
{
  "data": [
    {
      "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      "rate_limit_id": "rlt_01NwFawrTvAijwqn8AjKVBPS",
      "type": "workspace_rate_limit",
      "group_type": "model_group",
      "group": {
        "type": "model_group",
        "id": "rlg_01Hq7YkP3mZ9dTwRx4cVbN2s",
        "display_name": "Claude Opus 5.5"
      },
      "models": ["claude-opus-5-5"],
      "limits": [
        {
          "type": "requests_per_minute",
          "value": 1000,
          "org_limit": 4000,
          "source": { "type": "workspace" }
        },
        {
          "type": "input_tokens_per_minute",
          "value": 500000,
          "org_limit": 10000000,
          "source": { "type": "workspace" }
        },
        {
          "type": "output_tokens_per_minute",
          "value": 800000,
          "org_limit": 800000,
          "source": { "type": "organization" }
        }
      ]
    },
    {
      "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      "rate_limit_id": "rlt_016qriyigbdebqkzhMujdHkX",
      "type": "workspace_rate_limit",
      "group_type": "model_group",
      "group": {
        "type": "model_group",
        "id": "rlg_01Kd5wMv8nSq2LcXy6tRfJ4b",
        "display_name": "Claude Opus 4.x"
      },
      "models": [
        "claude-opus-4-5",
        "claude-opus-4-5-20251101",
        "claude-opus-4-6",
        "claude-opus-4-7",
        "claude-opus-4-8"
      ],
      "limits": [
        {
          "type": "requests_per_minute",
          "value": 1000,
          "org_limit": 4000,
          "source": { "type": "workspace" }
        },
        {
          "type": "input_tokens_per_minute",
          "value": 500000,
          "org_limit": 10000000,
          "source": { "type": "workspace" }
        },
        {
          "type": "output_tokens_per_minute",
          "value": 800000,
          "org_limit": 800000,
          "source": { "type": "organization" }
        }
      ]
    },
    {
      "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      "rate_limit_id": "rlt_01EyY8kq14eviKJPgepbgBH4",
      "type": "workspace_rate_limit",
      "group_type": "batch",
      "group": { "type": "batch", "id": "rlg_01Wn3pBz6kCg9vHtQ7mLxD5a" },
      "models": null,
      "limits": [
        {
          "type": "enqueued_batch_requests",
          "value": 500000,
          "org_limit": 500000,
          "source": { "type": "organization" }
        }
      ]
    }
  ],
  "next_page": null
}
```

### Mengatur batas laju workspace

Untuk menetapkan atau menghapus “rate limit” (batas laju) sebuah workspace untuk satu grup batas laju, kirim permintaan `POST` ke `/v1/organizations/workspaces/{workspace_id}/rate_limits/{rate_limit_id}`. Untuk `rate_limit_id`, berikan `id` dari entri grup tersebut dari endpoint organisasi, atau `rate_limit_id` dari entri grup tersebut dari endpoint daftar workspace. Untuk menemukan ID grup yang belum di-override oleh workspace, panggil endpoint daftar workspace dengan `include_inherited=true`, yang mengembalikan grup-grup yang dapat Anda tetapkan batasnya. ID ini berbeda antar organisasi, jadi cari ID tersebut di setiap organisasi yang Anda kelola.

Badan permintaan memiliki array `limits` berisi satu atau lebih entri `{type, value}`, masing-masing untuk jenis limiter yang berbeda:

* `value` berupa bilangan bulat, nol atau lebih besar, mengatur override workspace untuk jenis limiter tersebut.
* `value` bernilai `null` menghapus override, sehingga workspace kembali mewarisi nilai organisasi. Menghapus jenis limiter yang tidak memiliki override tidak mengubah apa pun.
* Jenis limiter yang tidak disebutkan dalam permintaan mempertahankan nilainya saat ini.

Anda dapat mengatur jenis limiter berikut: `requests_per_minute`, `input_tokens_per_minute`, `output_tokens_per_minute`, `input_tokens_per_minute_cache_aware`, `tokens_per_minute`, `tokens_per_day`, `tool_uses_per_second`, dan, jika endpoint daftar menampilkannya untuk organisasi Anda, batas [fast mode](https://platform.claude.com/docs/id/build-with-claude/fast-mode) `fast_itpmca` (token input per menit, cache-aware) dan `fast_otpm` (token output per menit). Jenis mana yang diterima oleh sebuah grup bergantung pada `group.type`-nya:

* `model_group`: semua jenis kecuali `tool_uses_per_second`
* `web_search`: hanya `tool_uses_per_second`
* `batch`: hanya `requests_per_minute`

Jenis grup lainnya tidak menerima jenis limiter apa pun. Anda dapat menghapus jenis limiter mana pun yang tercantum sebelumnya pada grup mana pun. Endpoint daftar dapat mengembalikan jenis limiter yang tidak dapat Anda atur, seperti `enqueued_batch_requests`; mengirimkan salah satunya akan mengembalikan error 400.

API menyimpan nilai di atas batas organisasi untuk jenis limiter yang sama, tetapi memberlakukan nilai yang lebih rendah dari keduanya. `org_limit` pada respons menampilkan nilai organisasi.

Perubahan berlaku dalam waktu sekitar satu jam. Sampai perubahan berlaku, permintaan workspace masih dibatasi oleh nilai sebelumnya.

API memeriksa seluruh permintaan sebelum mengubah apa pun, sehingga entri yang tidak valid akan menggagalkan permintaan dengan error 400 dan tidak mengubah apa pun. Jika permintaan lolos validasi, API kemudian menerapkan entri satu per satu. Jika penerapan salah satu entri gagal, permintaan mengembalikan error dan entri-entri sebelumnya tetap diterapkan. Setiap entri menetapkan atau menghapus nilai absolut, sehingga Anda dapat dengan aman mengirim permintaan yang sama lagi. Pengiriman ulang akan menggantikan perubahan apa pun yang dibuat orang lain di antaranya pada jenis limiter yang disebutkannya.

<Note>
  Mengatur batas laju workspace belum tersedia di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws).
</Note>

Naikkan request per menit workspace untuk grup Claude Opus 5.5 menjadi 2.000 dan hapus override token input per menitnya:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/rate_limits/rlt_01NwFawrTvAijwqn8AjKVBPS" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "limits": [
        {"type": "requests_per_minute", "value": 2000},
        {"type": "input_tokens_per_minute", "value": null}
      ]
    }'
  ```

  ```bash CLI
  ant organization:workspaces:rate-limits update \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    --rate-limit-id rlt_01NwFawrTvAijwqn8AjKVBPS <<'YAML'
  limits:
    - type: requests_per_minute
      value: 2000
    - type: input_tokens_per_minute
      value: null
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  entry = client.organization.workspaces.rate_limits.update(
      "rlt_01NwFawrTvAijwqn8AjKVBPS",
      workspace_id="wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      limits=[
          {"type": "requests_per_minute", "value": 2000},
          {"type": "input_tokens_per_minute", "value": None},
      ],
  )

  for limit in entry.limits:
      print(f"{limit.type}: {limit.value}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const entry = await client.organization.workspaces.rateLimits.update(
    "rlt_01NwFawrTvAijwqn8AjKVBPS",
    {
      workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
      limits: [
        { type: "requests_per_minute", value: 2000 },
        { type: "input_tokens_per_minute", value: null }
      ]
    }
  );

  for (const limit of entry.limits) {
    console.log(`${limit.type}: ${limit.value}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var entry = await client.Organization.Workspaces.RateLimits.Update(
      "rlt_01NwFawrTvAijwqn8AjKVBPS",
      new()
      {
          WorkspaceID = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
          Limits =
          [
              new() { Type = "requests_per_minute", Value = 2000 },
              new() { Type = "input_tokens_per_minute", Value = null },
          ],
      }
  );

  foreach (var limit in entry.Limits)
  {
      Console.WriteLine($"{limit.Type}: {limit.Value}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  entry, err := client.Organization.Workspaces.RateLimits.Update(
  	context.Background(),
  	"rlt_01NwFawrTvAijwqn8AjKVBPS",
  	anthropic.OrganizationWorkspaceRateLimitUpdateParams{
  		WorkspaceID: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  		Limits: []anthropic.WorkspaceRateLimitUpdateValueParam{
  			{Type: "requests_per_minute", Value: anthropic.Int(2000)},
  			{Type: "input_tokens_per_minute", Value: param.Null[int64]()},
  		},
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  for _, limit := range entry.Limits {
  	fmt.Printf("%s: %d\n", limit.Type, limit.Value)
  }
  ```

  ```java Java
  import com.anthropic.models.organization.workspaces.ratelimits.RateLimitUpdateParams;
  import com.anthropic.models.organization.workspaces.ratelimits.WorkspaceRateLimitType;
  import com.anthropic.models.organization.workspaces.ratelimits.WorkspaceRateLimitUpdateValue;
  import java.util.Optional;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var entry = client.organization().workspaces().rateLimits().update(
          "rlt_01NwFawrTvAijwqn8AjKVBPS",
          RateLimitUpdateParams.builder()
              .workspaceId("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
              .addLimit(WorkspaceRateLimitUpdateValue.builder()
                  .type(WorkspaceRateLimitType.REQUESTS_PER_MINUTE)
                  .value(2000L)
                  .build())
              .addLimit(WorkspaceRateLimitUpdateValue.builder()
                  .type(WorkspaceRateLimitType.INPUT_TOKENS_PER_MINUTE)
                  .value(Optional.empty())
                  .build())
              .build()
      );

      for (var limit : entry.limits()) {
          IO.println(limit.type() + ": " + limit.value());
      }
  }
  ```

  ```php PHP
  use Anthropic\Organization\Workspaces\RateLimits\WorkspaceRateLimitUpdateValue;

  $client = new Client();

  $entry = $client->organization->workspaces->rateLimits->update(
      'rlt_01NwFawrTvAijwqn8AjKVBPS',
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
      limits: [
          WorkspaceRateLimitUpdateValue::with(type: 'requests_per_minute', value: 2000),
          WorkspaceRateLimitUpdateValue::with(type: 'input_tokens_per_minute', value: null),
      ],
  );

  foreach ($entry->limits as $limit) {
      echo "{$limit->type}: {$limit->value}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  entry = client.organization.workspaces.rate_limits.update(
    "rlt_01NwFawrTvAijwqn8AjKVBPS",
    workspace_id: "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
    limits: [
      { type: :requests_per_minute, value: 2000 },
      { type: :input_tokens_per_minute, value: nil }
    ]
  )

  entry.limits.each do |limit|
    puts "#{limit.type}: #{limit.value}"
  end
  ```
</CodeGroup>

Respons berupa entri grup tersebut, dalam bentuk satu entri pada daftar `data` endpoint daftar workspace. `limits`-nya mencantumkan override workspace pada grup tersebut setelah perubahan: jenis limiter yang dihapus tidak dicantumkan, dan `limits` kosong ketika tidak ada override yang tersisa. Respons menyertakan perubahan dari permintaan bahkan ketika permintaan daftar yang dibuat segera setelahnya belum menampilkannya.

```json
{
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "rate_limit_id": "rlt_01NwFawrTvAijwqn8AjKVBPS",
  "type": "workspace_rate_limit",
  "group_type": "model_group",
  "group": {
    "type": "model_group",
    "id": "rlg_01Hq7YkP3mZ9dTwRx4cVbN2s",
    "display_name": "Claude Opus 5.5"
  },
  "models": ["claude-opus-5-5"],
  "limits": [
    {
      "type": "requests_per_minute",
      "value": 2000,
      "org_limit": 4000,
      "source": { "type": "workspace" }
    }
  ]
}
```

Endpoint mengembalikan error 400 untuk permintaan yang tidak valid atau workspace yang diarsipkan. Endpoint mengembalikan error 404 ketika workspace tidak ditemukan, atau ketika `rate_limit_id` menunjuk grup yang tidak dapat digunakan oleh workspace.

## Memfilter berdasarkan tipe grup

Kedua endpoint daftar menerima parameter query opsional `group_type` yang membatasi respons ke satu kategori:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rate_limits?group_type=batch" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:rate-limits list --group-type batch
  ```

  ```python Python
  client = anthropic.Anthropic()

  rate_limits = client.organization.rate_limits.list(group_type="batch")

  for entry in rate_limits:
      models = f" ({', '.join(entry.models)})" if entry.models else ""
      print(f"{entry.group.type}{models}")
      for limit in entry.limits:
          print(f"  {limit.type}: {limit.value}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rateLimits = await client.organization.rateLimits.list({ group_type: "batch" });

  for await (const entry of rateLimits) {
    const models = entry.models ? ` (${entry.models.join(", ")})` : "";
    console.log(`${entry.group.type}${models}`);
    for (const limit of entry.limits) {
      console.log(`  ${limit.type}: ${limit.value}`);
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Organization.RateLimits;

  AnthropicClient client = new();

  var rateLimits = await client.Organization.RateLimits.List(new()
  {
      GroupType = GroupType.Batch
  });

  await foreach (var entry in rateLimits.Paginate())
  {
      var models = entry.Models is null ? "" : $" ({string.Join(", ", entry.Models)})";
      Console.WriteLine($"{entry.Group.Type.Raw()}{models}");
      foreach (var limit in entry.Limits)
      {
          Console.WriteLine($"  {limit.Type}: {limit.Value}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rateLimits := client.Organization.RateLimits.ListAutoPaging(context.Background(), anthropic.OrganizationRateLimitListParams{
  	GroupType: anthropic.OrganizationRateLimitListParamsGroupTypeBatch,
  })

  for rateLimits.Next() {
  	entry := rateLimits.Current()
  	models := ""
  	if len(entry.Models) > 0 {
  		models = fmt.Sprintf(" (%s)", strings.Join(entry.Models, ", "))
  	}
  	fmt.Printf("%s%s\n", entry.Group.Type, models)
  	for _, limit := range entry.Limits {
  		fmt.Printf("  %s: %d\n", limit.Type, limit.Value)
  	}
  }
  if err := rateLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.organization.ratelimits.RateLimitListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = RateLimitListParams.builder()
          .groupType(RateLimitListParams.GroupType.BATCH)
          .build();
      var rateLimits = client.organization().rateLimits().list(params);

      for (var entry : rateLimits.autoPager()) {
          var models = entry.models()
              .map(modelIds -> " (" + String.join(", ", modelIds) + ")")
              .orElse("");
          IO.println(entry.group().type().asString() + models);
          for (var limit : entry.limits()) {
              IO.println("  " + limit.type() + ": " + limit.value());
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Organization\RateLimits\RateLimitListParams\GroupType;
  // ...

  $client = new Client();

  $rateLimits = $client->organization->rateLimits->list(
      groupType: GroupType::BATCH,
  );

  foreach ($rateLimits->data as $entry) {
      $models = $entry->models ? ' (' . implode(', ', $entry->models) . ')' : '';
      echo "{$entry->group->type}{$models}\n";
      foreach ($entry->limits as $limit) {
          echo "  {$limit->type}: {$limit->value}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rate_limits = client.organization.rate_limits.list(group_type: :batch)

  rate_limits.data.each do |entry|
    models = entry.models ? " (#{entry.models.join(", ")})" : ""
    puts "#{entry.group.type}#{models}"
    entry.limits.each do |limit|
      puts "  #{limit.type}: #{limit.value}"
    end
  end
  ```
</CodeGroup>

Nilai yang valid adalah `model_group`, `batch`, `token_count`, `files`, `skills`, dan `web_search`.

## Paginasi

Kedua endpoint menerima parameter kueri `page` dan mengembalikan field `next_page`. Respons saat ini selalu satu halaman, jadi `next_page` adalah `null`. Lakukan loop pada `next_page` agar klien Anda melakukan paginasi dengan benar tanpa perubahan ketika respons bertambah.

## Pertanyaan yang sering diajukan

### String model mana yang muncul dalam daftar `models`?

Setiap ID model dan alias yang dihitung terhadap grup, termasuk ID bertanggal (seperti `claude-sonnet-4-5-20250929`) dan alias tidak bertanggal (seperti `claude-sonnet-4-5`). Cari string model apa pun yang Anda berikan ke Messages API dan Anda akan menemukannya dalam tepat satu entri `model_group`.

Daftar ini mencakup model yang dapat diakses oleh organisasi Anda, sehingga dapat berbeda antar organisasi.

### Apa artinya jika sebuah grup hilang dari respons workspace?

Secara default, respons workspace hanya mencantumkan override, sehingga grup yang tidak ada tidak memiliki override workspace dan mewarisi batas tingkat organisasi. Teruskan `include_inherited=true` untuk melihat nilai yang diwarisi pada endpoint workspace, atau kueri endpoint organisasi. Dengan `include_inherited=true`, sebuah grup hanya tidak ada ketika grup tersebut tidak berlaku pada workspace atau organisasi tidak menetapkan batas untuknya.

### Bisakah saya memperbarui batas laju dengan API ini?

**Untuk workspace:** Ya. Endpoint [Set Workspace Rate Limits](https://platform.claude.com/docs/id/api/organization/workspaces/rate_limits/update) mengatur atau menghapus override workspace untuk satu grup batas laju. Berikan `id` tingkat atas dari entri yang sesuai dalam [respons endpoint organisasi](https://platform.claude.com/docs/id/manage-claude/rate-limits-api#list-all-organization-rate-limits) sebagai `rate_limit_id`, bukan `id` `rlg_` di dalam `group`-nya. Nilai yang lebih rendah antara override workspace dan batas tingkat organisasi yang berlaku, dan perubahan berlaku dalam waktu sekitar satu jam. Untuk badan permintaan dan contohnya, lihat [bagian halaman ini tentang mengatur batas laju workspace](https://platform.claude.com/docs/id/manage-claude/rate-limits-api#set-workspace-rate-limits). Anda juga dapat mengatur batas laju workspace di halaman [Rate limits](https://platform.claude.com/usage/limits) di Claude Console: pilih workspace dari menu dropdown **Workspace**, lalu klik **Edit** di samping sebuah model.

**Untuk organisasi:** Tidak. Untuk meminta batas yang lebih tinggi, lihat [Meminta batas yang lebih tinggi](https://platform.claude.com/docs/id/api/rate-limits#requesting-higher-limits).

## Lihat juga

* [Batas laju](https://platform.claude.com/docs/id/api/rate-limits)
* [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api)
* [Referensi Admin API](https://platform.claude.com/docs/id/api/organization)
* [Workspace](https://platform.claude.com/docs/id/manage-claude/workspaces)
* [Usage and Cost Analytics API](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api)
