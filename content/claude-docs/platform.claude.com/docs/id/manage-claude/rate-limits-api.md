---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/rate-limits-api
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 6b24dcfd500fadf2091450390234ec95d99dcb7f26b443fadeb3b2b230634dde
---

---
title: Rate Limits API
url: https://platform.claude.com/docs/id/manage-claude/rate-limits-api
description: Kueri batas laju API organisasi Anda secara terprogram dengan Rate Limits API.
---

<Tip>
  **Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, siapkan organisasi Anda di **Console → Settings → Organization**.
</Tip>

Rate Limits API menyediakan akses terprogram ke batas laju yang dikonfigurasi untuk organisasi Anda dan workspace-nya. Ini adalah informasi yang sama yang ditampilkan pada halaman [Rate limits](https://platform.claude.com/settings/limits) di Claude Console.

Gunakan API ini untuk:

* **Menjaga gateway dan proxy tetap sinkron:** Baca batas Anda saat ini pada startup dan secara terjadwal alih-alih melakukan hardcode nilai yang bergeser ketika Anthropic menyesuaikannya.
* **Menggerakkan peringatan internal:** Bandingkan data penggunaan dari [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api) terhadap batas yang Anda konfigurasi.
* **Mengaudit konfigurasi workspace:** Verifikasi bahwa override workspace sesuai dengan yang diharapkan oleh otomatisasi provisioning Anda.

<Check>
  **Kredensial Admin API diperlukan.** Endpoint ini merupakan bagian dari Admin API. Anda dapat mengaksesnya menggunakan [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys), token OAuth dengan cakupan `org:admin`, atau kunci akun pribadi maupun akun layanan yang tidak dibatasi pada suatu workspace; kunci API workspace tidak dapat digunakan. Lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/admin-api#authentication) untuk detailnya.
</Check>

Contoh SDK dan CLI pada halaman ini membangun klien default, yang membaca kunci API Admin dari variabel lingkungan `ANTHROPIC_API_KEY`. SDK mengekspos endpoint ini sebagai `client.beta.organization.rate_limits` dan `client.beta.organization.workspaces.rate_limits`; metode list Python, TypeScript, C#, Go, dan Java mengembalikan iterator yang mengikuti `next_page` untuk Anda, sementara contoh PHP, Ruby, dan curl membaca satu halaman.

## Mulai cepat

Daftar batas laju yang dikonfigurasi untuk organisasi Anda:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rate_limits" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:rate-limits list
  ```

  ```python Python
  client = anthropic.Anthropic()

  rate_limits = client.beta.organization.rate_limits.list()

  for group in rate_limits:
      models = f" ({', '.join(group.models)})" if group.models else ""
      print(f"{group.group_type}{models}")
      for limit in group.limits:
          print(f"  {limit.type}: {limit.value}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rateLimits = await client.beta.organization.rateLimits.list();

  for await (const group of rateLimits) {
    const models = group.models ? ` (${group.models.join(", ")})` : "";
    console.log(`${group.group_type}${models}`);
    for (const limit of group.limits) {
      console.log(`  ${limit.type}: ${limit.value}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var rateLimits = await client.Beta.Organization.RateLimits.List();

  await foreach (var group in rateLimits.Paginate())
  {
      var models = group.Models is null ? "" : $" ({string.Join(", ", group.Models)})";
      Console.WriteLine($"{group.GroupType.Raw()}{models}");
      foreach (var limit in group.Limits)
      {
          Console.WriteLine($"  {limit.Type}: {limit.Value}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rateLimits := client.Beta.Organization.RateLimits.ListAutoPaging(context.Background(), anthropic.BetaOrganizationRateLimitListParams{})

  for rateLimits.Next() {
  	group := rateLimits.Current()
  	models := ""
  	if len(group.Models) > 0 {
  		models = fmt.Sprintf(" (%s)", strings.Join(group.Models, ", "))
  	}
  	fmt.Printf("%s%s\n", group.GroupType, models)
  	for _, limit := range group.Limits {
  		fmt.Printf("  %s: %d\n", limit.Type, limit.Value)
  	}
  }
  if err := rateLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var rateLimits = client.beta().organization().rateLimits().list();

  for (var group : rateLimits.autoPager()) {
      var models = group.models()
          .map(modelIds -> " (" + String.join(", ", modelIds) + ")")
          .orElse("");
      IO.println(group.groupType().asString() + models);
      for (var limit : group.limits()) {
          IO.println("  " + limit.type() + ": " + limit.value());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rateLimits = $client->beta->organization->rateLimits->list();

  foreach ($rateLimits->data as $group) {
      $models = $group->models ? ' (' . implode(', ', $group->models) . ')' : '';
      echo "{$group->groupType}{$models}\n";
      foreach ($group->limits as $limit) {
          echo "  {$limit->type}: {$limit->value}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rate_limits = client.beta.organization.rate_limits.list

  rate_limits.data.each do |group|
    models = group.models ? " (#{group.models.join(", ")})" : ""
    puts "#{group.group_type}#{models}"
    group.limits.each do |limit|
      puts "  #{limit.type}: #{limit.value}"
    end
  end
  ```
</CodeGroup>

## Batas laju organisasi

Endpoint `/v1/organizations/rate_limits` mengembalikan batas laju yang diterapkan pada tingkat organisasi untuk Messages API dan sumber daya pendukungnya. Batas untuk produk lain, seperti [Claude Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview), tidak disertakan.

### Konsep utama

* **Grup batas laju:** Setiap entri dalam respons mewakili satu grup batas laju. Batas laju model dikelompokkan sehingga beberapa versi model berbagi satu set batas, dan grup lain mencakup sumber daya seperti Message Batches API, Files API, Token Counting API, agent skills, dan alat web search.
* **`group_type`:** Mengidentifikasi kategori batas mana yang dicakup oleh entri. Lihat [Memfilter berdasarkan tipe grup](https://platform.claude.com/docs/id/manage-claude/rate-limits-api#filtering-by-group-type) untuk daftar nilai.
* **Daftar `models`:** Untuk entri `model_group`, field `models` mencantumkan setiap ID model dan alias yang dihitung terhadap batas grup tersebut. Gunakan daftar ini untuk mencari grup mana yang mencakup string model apa pun. Untuk tipe grup lain, `models` adalah `null`.
* **Daftar `limits`:** Setiap grup membawa daftar pasangan `{type, value}`. Field `type` mengidentifikasi limiter (seperti `requests_per_minute`, `input_tokens_per_minute`, atau `output_tokens_per_minute`) dan `value` adalah batas yang dikonfigurasi. Lihat [Rate limits](https://platform.claude.com/docs/id/api/rate-limits) untuk bagaimana setiap limiter diukur dan diberlakukan.

Untuk detail parameter lengkap dan skema respons, lihat [referensi Organization Rate Limits API](https://platform.claude.com/docs/id/api/admin/rate_limits/list).

### Daftar semua batas laju organisasi

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rate_limits" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:rate-limits list
  ```

  ```python Python
  client = anthropic.Anthropic()

  rate_limits = client.beta.organization.rate_limits.list()

  for group in rate_limits:
      models = f" ({', '.join(group.models)})" if group.models else ""
      print(f"{group.group_type}{models}")
      for limit in group.limits:
          print(f"  {limit.type}: {limit.value}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rateLimits = await client.beta.organization.rateLimits.list();

  for await (const group of rateLimits) {
    const models = group.models ? ` (${group.models.join(", ")})` : "";
    console.log(`${group.group_type}${models}`);
    for (const limit of group.limits) {
      console.log(`  ${limit.type}: ${limit.value}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var rateLimits = await client.Beta.Organization.RateLimits.List();

  await foreach (var group in rateLimits.Paginate())
  {
      var models = group.Models is null ? "" : $" ({string.Join(", ", group.Models)})";
      Console.WriteLine($"{group.GroupType.Raw()}{models}");
      foreach (var limit in group.Limits)
      {
          Console.WriteLine($"  {limit.Type}: {limit.Value}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rateLimits := client.Beta.Organization.RateLimits.ListAutoPaging(context.Background(), anthropic.BetaOrganizationRateLimitListParams{})

  for rateLimits.Next() {
  	group := rateLimits.Current()
  	models := ""
  	if len(group.Models) > 0 {
  		models = fmt.Sprintf(" (%s)", strings.Join(group.Models, ", "))
  	}
  	fmt.Printf("%s%s\n", group.GroupType, models)
  	for _, limit := range group.Limits {
  		fmt.Printf("  %s: %d\n", limit.Type, limit.Value)
  	}
  }
  if err := rateLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var rateLimits = client.beta().organization().rateLimits().list();

  for (var group : rateLimits.autoPager()) {
      var models = group.models()
          .map(modelIds -> " (" + String.join(", ", modelIds) + ")")
          .orElse("");
      IO.println(group.groupType().asString() + models);
      for (var limit : group.limits()) {
          IO.println("  " + limit.type() + ": " + limit.value());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rateLimits = $client->beta->organization->rateLimits->list();

  foreach ($rateLimits->data as $group) {
      $models = $group->models ? ' (' . implode(', ', $group->models) . ')' : '';
      echo "{$group->groupType}{$models}\n";
      foreach ($group->limits as $limit) {
          echo "  {$limit->type}: {$limit->value}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rate_limits = client.beta.organization.rate_limits.list

  rate_limits.data.each do |group|
    models = group.models ? " (#{group.models.join(", ")})" : ""
    puts "#{group.group_type}#{models}"
    group.limits.each do |limit|
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
      "models": ["claude-opus-5"],
      "limits": [
        { "type": "requests_per_minute", "value": 4000 },
        { "type": "input_tokens_per_minute", "value": 10000000 },
        { "type": "output_tokens_per_minute", "value": 800000 }
      ]
    },
    {
      "type": "rate_limit",
      "group_type": "model_group",
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
      "models": null,
      "limits": [{ "type": "enqueued_batch_requests", "value": 500000 }]
    }
  ],
  "next_page": null
}
```

### Cari batas untuk model tertentu

Berikan ID model atau alias apa pun sebagai parameter kueri `model` untuk mengembalikan hanya entri yang memuatnya:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/rate_limits?model=claude-opus-5" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:rate-limits list --model claude-opus-5
  ```

  ```python Python
  client = anthropic.Anthropic()

  rate_limits = client.beta.organization.rate_limits.list(model="claude-opus-5")

  for group in rate_limits:
      models = f" ({', '.join(group.models)})" if group.models else ""
      print(f"{group.group_type}{models}")
      for limit in group.limits:
          print(f"  {limit.type}: {limit.value}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rateLimits = await client.beta.organization.rateLimits.list({ model: "claude-opus-5" });

  for await (const group of rateLimits) {
    const models = group.models ? ` (${group.models.join(", ")})` : "";
    console.log(`${group.group_type}${models}`);
    for (const limit of group.limits) {
      console.log(`  ${limit.type}: ${limit.value}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var rateLimits = await client.Beta.Organization.RateLimits.List(new()
  {
      Model = "claude-opus-5"
  });

  await foreach (var group in rateLimits.Paginate())
  {
      var models = group.Models is null ? "" : $" ({string.Join(", ", group.Models)})";
      Console.WriteLine($"{group.GroupType.Raw()}{models}");
      foreach (var limit in group.Limits)
      {
          Console.WriteLine($"  {limit.Type}: {limit.Value}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rateLimits := client.Beta.Organization.RateLimits.ListAutoPaging(context.Background(), anthropic.BetaOrganizationRateLimitListParams{
  	Model: anthropic.String(anthropic.ModelClaudeOpus5),
  })

  for rateLimits.Next() {
  	group := rateLimits.Current()
  	models := ""
  	if len(group.Models) > 0 {
  		models = fmt.Sprintf(" (%s)", strings.Join(group.Models, ", "))
  	}
  	fmt.Printf("%s%s\n", group.GroupType, models)
  	for _, limit := range group.Limits {
  		fmt.Printf("  %s: %d\n", limit.Type, limit.Value)
  	}
  }
  if err := rateLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.ratelimits.RateLimitListParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = RateLimitListParams.builder()
          .model(Model.CLAUDE_OPUS_5.asString())
          .build();
      var rateLimits = client.beta().organization().rateLimits().list(params);

      for (var group : rateLimits.autoPager()) {
          var models = group.models()
              .map(modelIds -> " (" + String.join(", ", modelIds) + ")")
              .orElse("");
          IO.println(group.groupType().asString() + models);
          for (var limit : group.limits()) {
              IO.println("  " + limit.type() + ": " + limit.value());
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Messages\Model;

  $client = new Client();

  $rateLimits = $client->beta->organization->rateLimits->list(
      model: Model::CLAUDE_OPUS_5->value,
  );

  foreach ($rateLimits->data as $group) {
      $models = $group->models ? ' (' . implode(', ', $group->models) . ')' : '';
      echo "{$group->groupType}{$models}\n";
      foreach ($group->limits as $limit) {
          echo "  {$limit->type}: {$limit->value}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rate_limits = client.beta.organization.rate_limits.list(model: Anthropic::Model::CLAUDE_OPUS_5)

  rate_limits.data.each do |group|
    models = group.models ? " (#{group.models.join(", ")})" : ""
    puts "#{group.group_type}#{models}"
    group.limits.each do |limit|
      puts "  #{limit.type}: #{limit.value}"
    end
  end
  ```
</CodeGroup>

Jika string model tidak cocok dengan grup mana pun, endpoint mengembalikan error 404. Parameter `model` hanya didukung pada endpoint organisasi; endpoint workspace tidak menerimanya.

## Batas laju workspace

Endpoint `/v1/organizations/workspaces/{workspace_id}/rate_limits` mengembalikan override batas laju yang dikonfigurasi untuk satu workspace.

Respons hanya menyertakan override, jadi apa pun yang hilang darinya diwarisi dari organisasi:

* Grup yang tidak ada dalam `data` sama sekali tidak memiliki override workspace. Workspace mewarisi batas tingkat organisasi untuk grup tersebut (bukan tidak terbatas).
* Dalam grup yang ada, tipe limiter yang tidak ada dalam `limits[]` tidak memiliki override workspace untuk limiter tersebut. Workspace mewarisi nilai organisasi untuknya.
* Untuk setiap limiter yang ada, `org_limit` adalah nilai tingkat organisasi untuk limiter yang sama, atau `null` jika organisasi tidak memiliki batas yang dikonfigurasi untuk tipe limiter tersebut.

Untuk detail parameter lengkap dan skema respons, lihat [referensi Workspace Rate Limits API](https://platform.claude.com/docs/id/api/admin/workspaces/rate_limits/list).

<Tip>
  Untuk mengambil ID workspace organisasi Anda, gunakan endpoint [List Workspaces](https://platform.claude.com/docs/id/api/admin/workspaces/list), atau temukan di [Claude Console](https://platform.claude.com/settings/workspaces). Workspace default tidak dapat memiliki override batas laju, jadi tidak memiliki entri pada endpoint ini; gunakan endpoint organisasi untuk membaca batasnya.
</Tip>

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/workspaces/wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ/rate_limits" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:workspaces:rate-limits list \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ
  ```

  ```python Python
  client = anthropic.Anthropic()

  rate_limits = client.beta.organization.workspaces.rate_limits.list(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  )

  for group in rate_limits:
      models = f" ({', '.join(group.models)})" if group.models else ""
      print(f"{group.group_type}{models}")
      for limit in group.limits:
          print(f"  {limit.type}: {limit.value}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rateLimits = await client.beta.organization.workspaces.rateLimits.list(
    "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  );

  for await (const group of rateLimits) {
    const models = group.models ? ` (${group.models.join(", ")})` : "";
    console.log(`${group.group_type}${models}`);
    for (const limit of group.limits) {
      console.log(`  ${limit.type}: ${limit.value}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var rateLimits = await client.Beta.Organization.Workspaces.RateLimits.List(
      "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  );

  await foreach (var group in rateLimits.Paginate())
  {
      var models = group.Models is null ? "" : $" ({string.Join(", ", group.Models)})";
      Console.WriteLine($"{group.GroupType.Raw()}{models}");
      foreach (var limit in group.Limits)
      {
          Console.WriteLine($"  {limit.Type}: {limit.Value}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rateLimits := client.Beta.Organization.Workspaces.RateLimits.ListAutoPaging(
  	context.Background(),
  	"wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  	anthropic.BetaOrganizationWorkspaceRateLimitListParams{},
  )

  for rateLimits.Next() {
  	group := rateLimits.Current()
  	models := ""
  	if len(group.Models) > 0 {
  		models = fmt.Sprintf(" (%s)", strings.Join(group.Models, ", "))
  	}
  	fmt.Printf("%s%s\n", group.GroupType, models)
  	for _, limit := range group.Limits {
  		fmt.Printf("  %s: %d\n", limit.Type, limit.Value)
  	}
  }
  if err := rateLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var rateLimits = client.beta().organization().workspaces().rateLimits()
      .list("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ");

  for (var group : rateLimits.autoPager()) {
      var models = group.models()
          .map(modelIds -> " (" + String.join(", ", modelIds) + ")")
          .orElse("");
      IO.println(group.groupType().asString() + models);
      for (var limit : group.limits()) {
          IO.println("  " + limit.type() + ": " + limit.value());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rateLimits = $client->beta->organization->workspaces->rateLimits->list(
      workspaceID: 'wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ',
  );

  foreach ($rateLimits->data as $group) {
      $models = $group->models ? ' (' . implode(', ', $group->models) . ')' : '';
      echo "{$group->groupType}{$models}\n";
      foreach ($group->limits as $limit) {
          echo "  {$limit->type}: {$limit->value}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  workspace_id = "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  rate_limits = client.beta.organization.workspaces.rate_limits.list(workspace_id)

  rate_limits.data.each do |group|
    models = group.models ? " (#{group.models.join(", ")})" : ""
    puts "#{group.group_type}#{models}"
    group.limits.each do |limit|
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
      "models": ["claude-opus-5"],
      "limits": [
        { "type": "requests_per_minute", "value": 1000, "org_limit": 4000 },
        { "type": "input_tokens_per_minute", "value": 500000, "org_limit": 10000000 }
      ]
    },
    {
      "type": "workspace_rate_limit",
      "group_type": "model_group",
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
  ant beta:organization:rate-limits list --group-type batch
  ```

  ```python Python
  client = anthropic.Anthropic()

  rate_limits = client.beta.organization.rate_limits.list(group_type="batch")

  for group in rate_limits:
      models = f" ({', '.join(group.models)})" if group.models else ""
      print(f"{group.group_type}{models}")
      for limit in group.limits:
          print(f"  {limit.type}: {limit.value}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rateLimits = await client.beta.organization.rateLimits.list({ group_type: "batch" });

  for await (const group of rateLimits) {
    const models = group.models ? ` (${group.models.join(", ")})` : "";
    console.log(`${group.group_type}${models}`);
    for (const limit of group.limits) {
      console.log(`  ${limit.type}: ${limit.value}`);
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.RateLimits;

  AnthropicClient client = new();

  var rateLimits = await client.Beta.Organization.RateLimits.List(new()
  {
      GroupType = GroupType.Batch
  });

  await foreach (var group in rateLimits.Paginate())
  {
      var models = group.Models is null ? "" : $" ({string.Join(", ", group.Models)})";
      Console.WriteLine($"{group.GroupType.Raw()}{models}");
      foreach (var limit in group.Limits)
      {
          Console.WriteLine($"  {limit.Type}: {limit.Value}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rateLimits := client.Beta.Organization.RateLimits.ListAutoPaging(context.Background(), anthropic.BetaOrganizationRateLimitListParams{
  	GroupType: anthropic.BetaOrganizationRateLimitListParamsGroupTypeBatch,
  })

  for rateLimits.Next() {
  	group := rateLimits.Current()
  	models := ""
  	if len(group.Models) > 0 {
  		models = fmt.Sprintf(" (%s)", strings.Join(group.Models, ", "))
  	}
  	fmt.Printf("%s%s\n", group.GroupType, models)
  	for _, limit := range group.Limits {
  		fmt.Printf("  %s: %d\n", limit.Type, limit.Value)
  	}
  }
  if err := rateLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.ratelimits.RateLimitListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = RateLimitListParams.builder()
          .groupType(RateLimitListParams.GroupType.BATCH)
          .build();
      var rateLimits = client.beta().organization().rateLimits().list(params);

      for (var group : rateLimits.autoPager()) {
          var models = group.models()
              .map(modelIds -> " (" + String.join(", ", modelIds) + ")")
              .orElse("");
          IO.println(group.groupType().asString() + models);
          for (var limit : group.limits()) {
              IO.println("  " + limit.type() + ": " + limit.value());
          }
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\RateLimits\RateLimitListParams\GroupType;
  // ...

  $client = new Client();

  $rateLimits = $client->beta->organization->rateLimits->list(
      groupType: GroupType::BATCH,
  );

  foreach ($rateLimits->data as $group) {
      $models = $group->models ? ' (' . implode(', ', $group->models) . ')' : '';
      echo "{$group->groupType}{$models}\n";
      foreach ($group->limits as $limit) {
          echo "  {$limit->type}: {$limit->value}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  rate_limits = client.beta.organization.rate_limits.list(group_type: :batch)

  rate_limits.data.each do |group|
    models = group.models ? " (#{group.models.join(", ")})" : ""
    puts "#{group.group_type}#{models}"
    group.limits.each do |limit|
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

* [Rate limits](https://platform.claude.com/docs/id/api/rate-limits)
* [Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api)
* [Referensi Admin API](https://platform.claude.com/docs/id/api/admin)
* [Workspaces](https://platform.claude.com/docs/id/manage-claude/workspaces)
* [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api)
