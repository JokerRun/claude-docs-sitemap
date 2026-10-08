---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/rate-limits-api
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: 07862ed6910be81ce537ed9bf92072300ad21bd7bbb74af08fa1600c43064d5e
---

---
title: Rate Limits API
url: https://platform.claude.com/docs/id/manage-claude/rate-limits-api
description: Kueri batas laju API organisasi Anda secara terprogram dengan Rate Limits API.
---

<Tip>
  **Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, siapkan organisasi Anda di **Console → Settings → Organization**.
</Tip>

Rate Limits API menyediakan akses terprogram ke "rate limit" (batas laju) yang dikonfigurasi untuk organisasi Anda dan workspace-nya. Ini adalah informasi yang sama dengan yang ditampilkan di halaman [Batas laju](https://platform.claude.com/settings/limits) di Claude Console.

Gunakan API ini untuk:

* **Menjaga gateway dan proxy tetap sinkron:** Baca batas Anda saat ini ketika startup dan secara terjadwal alih-alih melakukan hardcode nilai yang akan menyimpang ketika Anthropic menyesuaikannya.
* **Mendukung peringatan internal:** Bandingkan data penggunaan dari [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api) dengan batas yang telah Anda konfigurasi.
* **Mengaudit konfigurasi workspace:** Verifikasi bahwa override workspace sesuai dengan yang diharapkan oleh otomatisasi provisioning Anda.

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
      Console.WriteLine($"{entry.Group.Type.GetString()}{models}");
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
* **`group_type`:** Sudah deprecated dan digantikan oleh `type` di dalam `group`. Field ini masih dikembalikan, selalu sama dengan nilai tersebut, dan tidak memiliki tanggal penghapusan. Parameter kueri `group_type` tidak deprecated. Lihat [Memfilter berdasarkan tipe grup](https://platform.claude.com/docs/id/manage-claude/rate-limits-api#filtering-by-group-type) untuk daftar nilainya.
* **Daftar `models`:** Untuk entri `model_group`, field `models` mencantumkan setiap ID model dan alias yang dihitung terhadap batas grup tersebut. Gunakan daftar ini untuk mencari grup mana yang mencakup string model apa pun. Untuk tipe grup lainnya, `models` bernilai `null`.
* **Daftar `limits`:** Setiap grup membawa daftar pasangan `{type, value}`. Field `type` mengidentifikasi limiter (seperti `requests_per_minute`, `input_tokens_per_minute`, atau `output_tokens_per_minute`) dan `value` adalah batas yang dikonfigurasi. Lihat [Batas laju](https://platform.claude.com/docs/id/api/rate-limits) untuk cara setiap limiter diukur dan diberlakukan.

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
      Console.WriteLine($"{entry.Group.Type.GetString()}{models}");
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
  curl "https://api.anthropic.com/v1/organizations/rate_limits?model=claude-opus-5" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant organization:rate-limits list --model claude-opus-5
  ```

  ```python Python
  client = anthropic.Anthropic()

  rate_limits = client.organization.rate_limits.list(model="claude-opus-5")

  for entry in rate_limits:
      models = f" ({', '.join(entry.models)})" if entry.models else ""
      print(f"{entry.group.type}{models}")
      for limit in entry.limits:
          print(f"  {limit.type}: {limit.value}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rateLimits = await client.organization.rateLimits.list({ model: "claude-opus-5" });

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
      Model = "claude-opus-5"
  });

  await foreach (var entry in rateLimits.Paginate())
  {
      var models = entry.Models is null ? "" : $" ({string.Join(", ", entry.Models)})";
      Console.WriteLine($"{entry.Group.Type.GetString()}{models}");
      foreach (var limit in entry.Limits)
      {
          Console.WriteLine($"  {limit.Type}: {limit.Value}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rateLimits := client.Organization.RateLimits.ListAutoPaging(context.Background(), anthropic.OrganizationRateLimitListParams{
  	Model: anthropic.String(anthropic.ModelClaudeOpus5),
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
          .model(Model.CLAUDE_OPUS_5.asString())
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
      model: Model::CLAUDE_OPUS_5->value,
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

  rate_limits = client.organization.rate_limits.list(model: Anthropic::Model::CLAUDE_OPUS_5)

  rate_limits.data.each do |entry|
    models = entry.models ? " (#{entry.models.join(", ")})" : ""
    puts "#{entry.group.type}#{models}"
    entry.limits.each do |limit|
      puts "  #{limit.type}: #{limit.value}"
    end
  end
  ```
</CodeGroup>

Jika string model tidak cocok dengan grup mana pun, endpoint mengembalikan error 404. Parameter `model` hanya didukung pada endpoint organisasi; endpoint workspace tidak menerimanya.

## Batas laju workspace

Endpoint `/v1/organizations/workspaces/{workspace_id}/rate_limits` mengembalikan override batas laju yang dikonfigurasi untuk satu workspace.

Respons hanya menyertakan override, sehingga apa pun yang tidak ada di dalamnya diwarisi dari organisasi:

* Grup yang tidak ada di `data` sama sekali tidak memiliki override workspace. Workspace mewarisi batas tingkat organisasi untuk grup tersebut (bukan tanpa batas).
* Di dalam grup yang ada, tipe limiter yang tidak ada di `limits[]` tidak memiliki override workspace untuk limiter tersebut. Workspace mewarisi nilai organisasi untuknya.
* Untuk setiap limiter yang ada, `org_limit` adalah nilai tingkat organisasi untuk limiter yang sama, atau `null` jika organisasi tidak memiliki batas yang dikonfigurasi untuk tipe limiter tersebut.

Untuk detail parameter lengkap dan skema respons, lihat [referensi Workspace Rate Limits API](https://platform.claude.com/docs/id/api/organization/workspaces/rate_limits/list).

<Tip>
  Untuk mengambil ID workspace organisasi Anda, gunakan endpoint [List Workspaces](https://platform.claude.com/docs/id/api/organization/workspaces/list), atau temukan di [Claude Console](https://platform.claude.com/settings/workspaces). Workspace default tidak dapat memiliki override batas laju, sehingga tidak memiliki entri di endpoint ini; gunakan endpoint organisasi untuk membaca batasnya.
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
      Console.WriteLine($"{entry.Group.Type.GetString()}{models}");
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
      "type": "workspace_rate_limit",
      "group_type": "model_group",
      "group": {
        "type": "model_group",
        "id": "rlg_01Hq7YkP3mZ9dTwRx4cVbN2s",
        "display_name": "Claude Opus 5.5"
      },
      "models": ["claude-opus-5-5"],
      "limits": [
        { "type": "requests_per_minute", "value": 1000, "org_limit": 4000 },
        { "type": "input_tokens_per_minute", "value": 500000, "org_limit": 10000000 }
      ]
    },
    {
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
        { "type": "requests_per_minute", "value": 1000, "org_limit": 4000 },
        { "type": "input_tokens_per_minute", "value": 500000, "org_limit": 10000000 }
      ]
    }
  ],
  "next_page": null
}
```

## Memfilter berdasarkan tipe grup

Kedua endpoint menerima parameter kueri opsional `group_type` yang membatasi respons ke satu kategori:

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
      Console.WriteLine($"{entry.Group.Type.GetString()}{models}");
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

### Apa artinya jika sebuah grup hilang dari respons workspace?

Workspace tidak memiliki override untuk grup tersebut dan mewarisi batas tingkat organisasi. Kueri endpoint organisasi untuk melihat nilai yang diwarisi.

### Bisakah saya memperbarui batas laju dengan API ini?

Tidak. Untuk mengatur batas laju workspace, buka workspace di [Claude Console](https://platform.claude.com/settings/workspaces) dan gunakan tab **Rate limits**.

## Lihat juga

* [Batas laju](https://platform.claude.com/docs/id/api/rate-limits)
* [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api)
* [Referensi Admin API](https://platform.claude.com/docs/id/api/organization)
* [Workspace](https://platform.claude.com/docs/id/manage-claude/workspaces)
* [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api)
