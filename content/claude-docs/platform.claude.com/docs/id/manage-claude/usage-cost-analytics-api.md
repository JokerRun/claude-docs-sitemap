---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api
fetched_at: 2026-10-30T02:15:26.914079Z
sha256: 1df57bf286e20b263ed873227cdfafb604abf2d9cbfe84c359b2769ce9e46c7b
---

---
title: Usage and Cost Analytics API
url: https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api
description: Kueri penggunaan token dan biaya untuk organisasi Claude Console atau Claude Enterprise Anda berdasarkan model, workspace, kunci API, aktor, dan lainnya.
---

<Tip>
  **Admin API tidak tersedia untuk akun individu.** Untuk berkolaborasi dengan rekan tim dan menambahkan anggota, siapkan organisasi Anda di halaman [Organization](https://platform.claude.com/settings/organization) (`platform.claude.com/settings/organization`) di Claude Console.
</Tip>

Usage and Cost Analytics API melaporkan riwayat penggunaan token dan biaya untuk organisasi Anda, yang dirinci berdasarkan dimensi yang Anda pilih, seperti model, workspace, kunci API, atau pengguna atau akun layanan di balik setiap permintaan. Untuk organisasi Claude Console, data ini serupa dengan yang ditampilkan oleh halaman [Usage](https://platform.claude.com/usage) dan [Cost](https://platform.claude.com/cost) di Claude Console.

API ini memiliki dua endpoint:

* `GET /v1/organizations/analytics/usage` melaporkan jumlah token dan jumlah permintaan.
* `GET /v1/organizations/analytics/cost` melaporkan biaya dalam USD.

Usage and Cost Analytics API masih dalam tahap beta. Kirim header `anthropic-beta: analytics-usage-cost-2026-08-24` dan header [`anthropic-version`](https://platform.claude.com/docs/id/api/versioning) pada setiap permintaan. SDK dan CLI `ant` mengirimkan kedua header tersebut untuk Anda dan mengambil halaman-halaman berikutnya saat Anda membaca hasilnya, sehingga `limit` hanya menetapkan ukuran halaman.

Gunakan API ini untuk:

* **Mengatribusikan pengeluaran:** Merinci biaya dan penggunaan token berdasarkan workspace, kunci API, model, tingkat layanan, atau identitas yang membuat setiap permintaan.
* **Menemukan konsumen teratas:** Mengurutkan hasil berdasarkan token, permintaan, atau biaya untuk menjawab pertanyaan seperti “kunci API mana yang paling banyak mengeluarkan biaya bulan ini?”
* **Membangun deret waktu:** Membagi hasil ke dalam bucket harian, per jam, atau per menit untuk dasbor dan laporan keuangan.
* **Mengintegrasikan sekali saja:** Endpoint, parameter, dan field respons yang sama melayani organisasi Claude Console dan Claude Enterprise.

<Check>
  **Autentikasi**

  Organisasi Claude Console menggunakan [kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-console-organization) atau [kredensial Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api#authentication) lainnya, seperti token OAuth dengan cakupan `org:admin`. Kirim token OAuth dalam header `authorization: Bearer` alih-alih header `x-api-key`; lihat [Mendapatkan token bearer OAuth](https://platform.claude.com/docs/id/manage-claude/admin-api#oauth-bearer-token).

  Organisasi Claude Enterprise menggunakan kunci dengan cakupan `read:analytics`, yang dibuat di claude.ai oleh pemilik utama setelah Analytics API diaktifkan untuk organisasi tersebut; lihat [Mendapatkan akses ke Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api).

  Contoh-contoh di halaman ini membaca kunci dari variabel lingkungan `ANTHROPIC_API_KEY`, jadi atur variabel tersebut ke kunci Anda sebelum Anda menjalankannya.

  Jika Anda memanggil endpoint ini dengan kunci Admin API, berikan layanan yang mengumpulkan data ini kuncinya sendiri, simpan di pengelola rahasia, dan rotasi secara berkala; menetapkan [masa kedaluwarsa kunci](https://platform.claude.com/docs/id/manage-claude/authentication#key-expiration) saat Anda membuat kunci akan memberlakukan rotasi tersebut. Jika memungkinkan, gunakan aturan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) dengan [cakupan `org:admin`](https://platform.claude.com/docs/id/manage-claude/wif-reference#oauth-scopes) sebagai gantinya, sehingga layanan mendapatkan token berumur pendek dan tidak ada kunci berumur panjang yang dapat bocor.
</Check>

<Note>
  **Claude Platform on AWS:** Kedua endpoint tersedia. Permintaan menggunakan URL dasar dan autentikasi Claude Platform on AWS sebagai pengganti kunci Admin API (lihat [Membuat permintaan](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws#making-requests)), dan AWS IAM mengotorisasinya melalui [aksi `ListAccountUsage` dan `ListAccountCost`](https://platform.claude.com/docs/id/api/claude-platform-on-aws-iam-actions#usage-and-cost). Setiap permintaan hanya mencakup workspace di region AWS dari endpoint yang Anda panggil, jadi panggil endpoint setiap region untuk mencakup seluruh organisasi Anda. `user_profile_id`, `claude_tag_category`, `claude_tag_user_id`, dan dimensi Claude Managed Agents (`agent_id`, `environment_id`, `deployment_id`, dan `session_id`) bernilai `null` pada setiap baris.
</Note>

<Note>
  **Claude Models on Google Cloud (Anthropic managed):** Kedua endpoint tersedia. Panggil endpoint tersebut melalui [base URL tingkat organisasi](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#making-requests) dengan kredensial Google Cloud, bukan dengan kunci Admin API. Endpoint `/usage` memerlukan [izin IAM](https://platform.claude.com/docs/id/api/claude-models-on-google-cloud-anthropic-managed-iam-permissions) `usageAnalytics.list`, dan endpoint `/cost` memerlukan `costAnalytics.list`.
</Note>

## Mulai cepat

Dapatkan penggunaan token harian untuk minggu pertama bulan September, satu baris untuk setiap model dan hari:

<CodeGroup>
  ```bash cURL
  curl --globoff "https://api.anthropic.com/v1/organizations/analytics/usage?\
  starting_at=2026-09-01T00:00:00Z&\
  ending_at=2026-09-08T00:00:00Z&\
  time_bucket_width=1d&\
  group_by[]=model&\
  limit=10" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: analytics-usage-cost-2026-08-24" \
    -H "x-api-key: $ANTHROPIC_API_KEY"
  ```

  ```bash CLI
  ant beta:organization:analytics:usage list \
    --starting-at 2026-09-01T00:00:00Z \
    --ending-at 2026-09-08T00:00:00Z \
    --time-bucket-width 1d \
    --group-by model \
    --limit 10
  ```

  ```python Python
  client = anthropic.Anthropic()

  rows = client.beta.organization.analytics.usage.list(
      starting_at="2026-09-01T00:00:00Z",
      ending_at="2026-09-08T00:00:00Z",
      time_bucket_width="1d",
      group_by=["model"],
      limit=10,
  )

  for row in rows:
      print(f"{row.starting_at} {row.group.model}: {row.usage.total_tokens}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rows = await client.beta.organization.analytics.usage.list({
    starting_at: "2026-09-01T00:00:00Z",
    ending_at: "2026-09-08T00:00:00Z",
    time_bucket_width: "1d",
    group_by: ["model"],
    limit: 10
  });

  for await (const row of rows) {
    console.log(`${row.starting_at} ${row.group.model}: ${row.usage.total_tokens}`);
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Analytics;
  using Anthropic.Models.Beta.Organization.Analytics.Usage;

  AnthropicClient client = new();

  var page = await client.Beta.Organization.Analytics.Usage.List(
      new()
      {
          StartingAt = DateTimeOffset.Parse("2026-09-01T00:00:00Z"),
          EndingAt = DateTimeOffset.Parse("2026-09-08T00:00:00Z"),
          TimeBucketWidth = BetaAnalyticsTimeBucketWidth.Day,
          GroupBy = [BetaAnalyticsUsageGroupBy.Model],
          Limit = 10,
      }
  );

  await foreach (var row in page.Paginate())
  {
      Console.WriteLine($"{row.StartingAt} {row.Group.Model}: {row.Usage.TotalTokens}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rows := client.Beta.Organization.Analytics.Usage.ListAutoPaging(context.Background(), anthropic.BetaOrganizationAnalyticsUsageListParams{
  	StartingAt:      time.Date(2026, time.September, 1, 0, 0, 0, 0, time.UTC),
  	EndingAt:        anthropic.Time(time.Date(2026, time.September, 8, 0, 0, 0, 0, time.UTC)),
  	TimeBucketWidth: anthropic.BetaAnalyticsTimeBucketWidthDay,
  	GroupBy:         []anthropic.BetaAnalyticsUsageGroupBy{anthropic.BetaAnalyticsUsageGroupByModel},
  	Limit:           anthropic.Int(10),
  })

  for rows.Next() {
  	row := rows.Current()
  	fmt.Printf("%s %s: %d\n", row.StartingAt.Format(time.RFC3339), row.Group.Model, row.Usage.TotalTokens)
  }
  if err := rows.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.analytics.BetaAnalyticsTimeBucketWidth;
  import com.anthropic.models.beta.organization.analytics.usage.BetaAnalyticsUsageGroupBy;
  import com.anthropic.models.beta.organization.analytics.usage.UsageListParams;
  import java.time.OffsetDateTime;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UsageListParams.builder()
          .startingAt(OffsetDateTime.parse("2026-09-01T00:00:00Z"))
          .endingAt(OffsetDateTime.parse("2026-09-08T00:00:00Z"))
          .timeBucketWidth(BetaAnalyticsTimeBucketWidth.DAY)
          .addGroupBy(BetaAnalyticsUsageGroupBy.MODEL)
          .limit(10)
          .build();
      var rows = client.beta().organization().analytics().usage().list(params);

      for (var row : rows.autoPager()) {
          IO.println(row.startingAt() + " " + row.group().model().orElse(null) + ": " + row.usage().totalTokens());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rows = $client->beta->organization->analytics->usage->list(
      startingAt: new \DateTimeImmutable('2026-09-01T00:00:00Z'),
      endingAt: new \DateTimeImmutable('2026-09-08T00:00:00Z'),
      timeBucketWidth: '1d',
      groupBy: ['model'],
      limit: 10,
  );

  foreach ($rows->pagingEachItem() as $row) {
      $startingAt = $row->startingAt->format(\DateTimeInterface::ATOM);
      echo "{$startingAt} {$row->group->model}: {$row->usage->totalTokens}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.analytics.usage.list(
    starting_at: Time.utc(2026, 9, 1),
    ending_at: Time.utc(2026, 9, 8),
    time_bucket_width: :"1d",
    group_by: [:model],
    limit: 10
  )

  page.auto_paging_each do |row|
    puts "#{row.starting_at} #{row.group.model}: #{row.usage.total_tokens}"
  end
  ```
</CodeGroup>

Respons berisi satu baris untuk setiap model dan hari yang memiliki penggunaan, dengan `total_tokens` terbesar terlebih dahulu. Contoh ini menampilkan satu baris:

```json
{
  "data": [
    {
      "starting_at": "2026-09-03T00:00:00Z",
      "ending_at": "2026-09-04T00:00:00Z",
      "group": {
        "product": null,
        "model": "claude-sonnet-5",
        "context_window": null,
        "inference_geo": null,
        "speed": null,
        "slack_channel_id": null,
        "claude_tag_category": null,
        "claude_tag_user_id": null,
        "rbac_group_id": null,
        "workspace_id": null,
        "service_tier": null,
        "user_profile_id": null,
        "agent_id": null,
        "environment_id": null,
        "deployment_id": null,
        "session_id": null,
        "actor": null,
        "actor_type": null,
        "api_key_id": null
      },
      "usage": {
        "uncached_input_tokens": 1284500,
        "cache_creation": {
          "ephemeral_1h_input_tokens": 0,
          "ephemeral_5m_input_tokens": 215300
        },
        "cache_read_input_tokens": 3200000,
        "output_tokens": 891000,
        "total_tokens": 5590800,
        "server_tool_use": {
          "web_search_requests": 12
        },
        "requests": 4210
      }
    }
  ],
  "has_more": true,
  "next_page": "page_V2mQ4dkt9HcbX3pLr...",
  "data_refreshed_at": "2026-09-18T16:02:11Z"
}
```

<Tip>
  **Atur header User-Agent untuk integrasi**

  Jika Anda membangun integrasi, atur header User-Agent Anda untuk membantu Anthropic memahami pola penggunaan:

  ```text wrap
  User-Agent: YourApp/1.0.0 (https://yourapp.com)
  ```
</Tip>

## Bagaimana hasil dibentuk

* **Setiap baris memiliki tiga bagian:** `starting_at` dan `ending_at` memberikan periode yang dicakup baris tersebut, `group` menampung setiap dimensi, dan `usage` (atau `cost` pada endpoint biaya) menampung metrik.
* **Dimensi bernilai null kecuali dikelompokkan:** Sebuah dimensi di `group` bernilai `null` kecuali Anda mencantumkannya di `group_by[]`. Dimensi yang dikelompokkan juga bernilai `null` pada baris yang tidak memiliki nilai untuknya, seperti `model` pada penggunaan eksekusi kode. `group_by[]` menerima hingga lima dimensi.
* **Satu baris untuk setiap kombinasi:** Setiap baris adalah satu kombinasi dari dimensi yang dikelompokkan, dan setiap kombinasi yang memiliki penggunaan atau biaya muncul tepat satu kali di seluruh halaman sebuah kueri. Tanpa `group_by[]` dan tanpa `time_bucket_width`, respons berupa satu baris yang menjumlahkan seluruh rentang.
* **Time bucket bersifat opsional:** Atur `time_bucket_width` ke `1m`, `1h`, atau `1d` untuk membagi setiap kombinasi berdasarkan bucket UTC; `starting_at` dan `ending_at` setiap baris kemudian menjadi batas bucket-nya. Bucket tanpa penggunaan atau biaya tidak menghasilkan baris.
* **Diurutkan berdasarkan peringkat secara default:** Baris diurutkan berdasarkan metrik `order_by` di seluruh rentang, dari yang terbesar terlebih dahulu secara default (`order=asc` membalikkannya). Untuk membangun deret waktu, atur `time_bucket_width` dan `order_by=time`. Baris kemudian dikembalikan satu time bucket demi satu time bucket, dengan bucket terbaru terlebih dahulu secara default (`order=asc` menempatkan yang terlama terlebih dahulu), dan baris terbesar terlebih dahulu di dalam setiap bucket. Isi bucket yang kosong dengan nol.
* **Filter bekerja bersama pengelompokan:** Sebagian besar dimensi yang dapat Anda kelompokkan memiliki filter daftar yang sesuai dalam notasi kurung siku, seperti `models[]=claude-opus-5-5`. Ulangi parameter untuk meneruskan beberapa nilai, hingga 100. Beberapa nilai untuk filter yang sama digabungkan dengan OR, dan filter yang berbeda digabungkan dengan AND. Filter dan `group_by[]` bersifat independen; Anda dapat memfilter berdasarkan dimensi apa pun dengan atau tanpa mengelompokkannya, atau sebaliknya.

Dimensi seperti `model` dan `actor` berlaku untuk setiap organisasi. Beberapa, seperti `api_key_id`, hanya berlaku untuk organisasi Claude Console, dan yang lainnya, seperti `slack_channel_id`, hanya berlaku untuk organisasi Claude Enterprise. Dimensi yang tidak berlaku untuk organisasi Anda bernilai `null` di setiap baris dan filternya tidak cocok dengan apa pun; pengecualiannya adalah `rbac_group_id`, yang justru mengembalikan error ketika tim tidak tersedia untuk organisasi Anda. Referensi API [penggunaan](https://platform.claude.com/docs/id/api/beta/organization/analytics/usage/list) dan [biaya](https://platform.claude.com/docs/id/api/beta/organization/analytics/cost/list) mencantumkan setiap dimensi, filter, dan nilai.

### Aktor

Dimensi `actor` menunjukkan kepada siapa sebuah permintaan diatribusikan: pengguna, akun layanan, identitas cloud terfederasi (principal AWS atau Google Cloud, untuk organisasi yang mengakses Claude melalui platform cloud mereka), atau, ketika tidak ada satu pun dari itu di balik permintaan, kunci API itu sendiri. Saat Anda mengelompokkan berdasarkan `actor`, `actor` pada setiap baris adalah objek yang `type`-nya menyatakan jenisnya. Penggunaan yang tidak dapat diatribusikan ke identitas mana pun memiliki `actor: null`.

[Kunci pribadi dan kunci akun layanan](https://platform.claude.com/docs/id/manage-claude/authentication#key-types) bertindak sebagai pengguna atau akun layanan yang ditautkan dengannya, sehingga permintaannya menampilkan identitas tersebut sebagai `actor` dan kuncinya di `api_key_id`. Kunci workspace lama tidak ditautkan ke identitas, sehingga kunci tersebut muncul sebagai `actor` sekaligus `api_key_id`. Pengecualiannya adalah kunci yang dibuat Claude Code untuk seorang anggota saat masuk: kunci tersebut berada di [workspace Claude Code](https://platform.claude.com/docs/id/manage-claude/workspaces#claude-code-workspace), dan penggunaannya diatribusikan ke anggota tersebut. Permintaan yang dibuat tanpa kunci API, seperti dari Claude Console, dari Claude Code setelah [masuk tanpa kunci API](https://code.claude.com/docs/en/authentication#sign-in-without-an-api-key), atau dengan token [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation), memiliki `api_key_id: null`. Setelah masuk tanpa kunci API, `actor` adalah anggota yang masuk; `actor` dari workload terfederasi adalah akun layanannya. Untuk menyertakan penggunaan tanpa kunci API dalam filter `api_key_ids[]`, tambahkan entri kosong: `api_key_ids[]=`.

Filter `api_key_ids[]` dan `actor_ids[]` menjawab pertanyaan yang berbeda. `api_key_ids[]=apikey_...` mencocokkan setiap permintaan yang diautentikasi oleh kunci tersebut, kepada siapa pun permintaan itu diatribusikan. `actor_ids[]=apikey_...` hanya mencocokkan permintaan yang diatribusikan ke kunci itu sendiri.

## Endpoint penggunaan

`GET /v1/organizations/analytics/usage` mengembalikan jumlah token berdasarkan tipe. `order_by` menerima `total_tokens` (default), `output_tokens`, `uncached_input_tokens`, `requests`, atau `time`.

Misalnya, untuk melihat penggunaan selama seminggu untuk satu workspace dan satu kunci API, dirinci berdasarkan tingkat layanan (satu baris untuk setiap tingkat, mencakup seluruh minggu):

<CodeGroup>
  ```bash cURL
  curl --globoff "https://api.anthropic.com/v1/organizations/analytics/usage?\
  starting_at=2026-09-01T00:00:00Z&\
  ending_at=2026-09-08T00:00:00Z&\
  workspace_ids[]=wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ&\
  api_key_ids[]=apikey_01Rj2N8SVvo6BePZj99NhmiT&\
  group_by[]=service_tier" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: analytics-usage-cost-2026-08-24" \
    -H "x-api-key: $ANTHROPIC_API_KEY"
  ```

  ```bash CLI
  ant beta:organization:analytics:usage list \
    --starting-at 2026-09-01T00:00:00Z \
    --ending-at 2026-09-08T00:00:00Z \
    --workspace-id wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ \
    --api-key-id apikey_01Rj2N8SVvo6BePZj99NhmiT \
    --group-by service_tier
  ```

  ```python Python
  client = anthropic.Anthropic()

  rows = client.beta.organization.analytics.usage.list(
      starting_at="2026-09-01T00:00:00Z",
      ending_at="2026-09-08T00:00:00Z",
      workspace_ids=["wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"],
      api_key_ids=["apikey_01Rj2N8SVvo6BePZj99NhmiT"],
      group_by=["service_tier"],
  )

  for row in rows:
      print(f"{row.group.service_tier}: {row.usage.total_tokens}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rows = await client.beta.organization.analytics.usage.list({
    starting_at: "2026-09-01T00:00:00Z",
    ending_at: "2026-09-08T00:00:00Z",
    workspace_ids: ["wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"],
    api_key_ids: ["apikey_01Rj2N8SVvo6BePZj99NhmiT"],
    group_by: ["service_tier"]
  });

  for await (const row of rows) {
    console.log(`${row.group.service_tier}: ${row.usage.total_tokens}`);
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Analytics.Usage;

  AnthropicClient client = new();

  var page = await client.Beta.Organization.Analytics.Usage.List(
      new()
      {
          StartingAt = DateTimeOffset.Parse("2026-09-01T00:00:00Z"),
          EndingAt = DateTimeOffset.Parse("2026-09-08T00:00:00Z"),
          WorkspaceIds = ["wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"],
          ApiKeyIds = ["apikey_01Rj2N8SVvo6BePZj99NhmiT"],
          GroupBy = [BetaAnalyticsUsageGroupBy.ServiceTier],
      }
  );

  await foreach (var row in page.Paginate())
  {
      Console.WriteLine($"{row.Group.ServiceTier?.Raw()}: {row.Usage.TotalTokens}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rows := client.Beta.Organization.Analytics.Usage.ListAutoPaging(context.Background(), anthropic.BetaOrganizationAnalyticsUsageListParams{
  	StartingAt:   time.Date(2026, time.September, 1, 0, 0, 0, 0, time.UTC),
  	EndingAt:     anthropic.Time(time.Date(2026, time.September, 8, 0, 0, 0, 0, time.UTC)),
  	WorkspaceIDs: []string{"wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"},
  	APIKeyIDs:    []string{"apikey_01Rj2N8SVvo6BePZj99NhmiT"},
  	GroupBy:      []anthropic.BetaAnalyticsUsageGroupBy{anthropic.BetaAnalyticsUsageGroupByServiceTier},
  })

  for rows.Next() {
  	row := rows.Current()
  	fmt.Printf("%s: %d\n", row.Group.ServiceTier, row.Usage.TotalTokens)
  }
  if err := rows.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.analytics.usage.BetaAnalyticsUsageGroupBy;
  import com.anthropic.models.beta.organization.analytics.usage.UsageListParams;
  import java.time.OffsetDateTime;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UsageListParams.builder()
          .startingAt(OffsetDateTime.parse("2026-09-01T00:00:00Z"))
          .endingAt(OffsetDateTime.parse("2026-09-08T00:00:00Z"))
          .addWorkspaceId("wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ")
          .addApiKeyId("apikey_01Rj2N8SVvo6BePZj99NhmiT")
          .addGroupBy(BetaAnalyticsUsageGroupBy.SERVICE_TIER)
          .build();
      var rows = client.beta().organization().analytics().usage().list(params);

      for (var row : rows.autoPager()) {
          IO.println(row.group().serviceTier().orElse(null) + ": " + row.usage().totalTokens());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rows = $client->beta->organization->analytics->usage->list(
      startingAt: new \DateTimeImmutable('2026-09-01T00:00:00Z'),
      endingAt: new \DateTimeImmutable('2026-09-08T00:00:00Z'),
      workspaceIDs: ['wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ'],
      apiKeyIDs: ['apikey_01Rj2N8SVvo6BePZj99NhmiT'],
      groupBy: ['service_tier'],
  );

  foreach ($rows->pagingEachItem() as $row) {
      echo "{$row->group->serviceTier}: {$row->usage->totalTokens}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.analytics.usage.list(
    starting_at: Time.utc(2026, 9, 1),
    ending_at: Time.utc(2026, 9, 8),
    workspace_ids: ["wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"],
    api_key_ids: ["apikey_01Rj2N8SVvo6BePZj99NhmiT"],
    group_by: [:service_tier]
  )

  page.auto_paging_each do |row|
    puts "#{row.group.service_tier}: #{row.usage.total_tokens}"
  end
  ```
</CodeGroup>

Untuk mencari ID kunci API dan workspace, gunakan endpoint [List API Keys](https://platform.claude.com/docs/id/api/organization/api_keys/list) dan [List Workspaces](https://platform.claude.com/docs/id/api/organization/workspaces/list) atau Claude Console.

Untuk menemukan pengguna, akun layanan, dan kunci API mana yang membuat permintaan terbanyak dalam sebulan:

<CodeGroup>
  ```bash cURL
  curl --globoff "https://api.anthropic.com/v1/organizations/analytics/usage?\
  starting_at=2026-09-01T00:00:00Z&\
  ending_at=2026-10-01T00:00:00Z&\
  group_by[]=actor&\
  order_by=requests&\
  limit=25" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: analytics-usage-cost-2026-08-24" \
    -H "x-api-key: $ANTHROPIC_API_KEY"
  ```

  ```bash CLI
  ant beta:organization:analytics:usage list \
    --starting-at 2026-09-01T00:00:00Z \
    --ending-at 2026-10-01T00:00:00Z \
    --group-by actor \
    --order-by requests \
    --limit 25
  ```

  ```python Python
  client = anthropic.Anthropic()

  rows = client.beta.organization.analytics.usage.list(
      starting_at="2026-09-01T00:00:00Z",
      ending_at="2026-10-01T00:00:00Z",
      group_by=["actor"],
      order_by="requests",
      limit=25,
  )

  for row in rows:
      print(f"{row.group.actor}: {row.usage.requests}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rows = await client.beta.organization.analytics.usage.list({
    starting_at: "2026-09-01T00:00:00Z",
    ending_at: "2026-10-01T00:00:00Z",
    group_by: ["actor"],
    order_by: "requests",
    limit: 25
  });

  for await (const row of rows) {
    console.log(`${JSON.stringify(row.group.actor)}: ${row.usage.requests}`);
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Analytics.Usage;

  AnthropicClient client = new();

  var page = await client.Beta.Organization.Analytics.Usage.List(
      new()
      {
          StartingAt = DateTimeOffset.Parse("2026-09-01T00:00:00Z"),
          EndingAt = DateTimeOffset.Parse("2026-10-01T00:00:00Z"),
          GroupBy = [BetaAnalyticsUsageGroupBy.Actor],
          OrderBy = BetaAnalyticsUsageOrderBy.Requests,
          Limit = 25,
      }
  );

  await foreach (var row in page.Paginate())
  {
      Console.WriteLine($"{row.Group.Actor?.Json}: {row.Usage.Requests}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rows := client.Beta.Organization.Analytics.Usage.ListAutoPaging(context.Background(), anthropic.BetaOrganizationAnalyticsUsageListParams{
  	StartingAt: time.Date(2026, time.September, 1, 0, 0, 0, 0, time.UTC),
  	EndingAt:   anthropic.Time(time.Date(2026, time.October, 1, 0, 0, 0, 0, time.UTC)),
  	GroupBy:    []anthropic.BetaAnalyticsUsageGroupBy{anthropic.BetaAnalyticsUsageGroupByActor},
  	OrderBy:    anthropic.BetaAnalyticsUsageOrderByRequests,
  	Limit:      anthropic.Int(25),
  })

  for rows.Next() {
  	row := rows.Current()
  	fmt.Printf("%s: %d\n", row.Group.Actor.RawJSON(), row.Usage.Requests)
  }
  if err := rows.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.analytics.usage.BetaAnalyticsUsageGroupBy;
  import com.anthropic.models.beta.organization.analytics.usage.BetaAnalyticsUsageOrderBy;
  import com.anthropic.models.beta.organization.analytics.usage.UsageListParams;
  import java.time.OffsetDateTime;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UsageListParams.builder()
          .startingAt(OffsetDateTime.parse("2026-09-01T00:00:00Z"))
          .endingAt(OffsetDateTime.parse("2026-10-01T00:00:00Z"))
          .addGroupBy(BetaAnalyticsUsageGroupBy.ACTOR)
          .orderBy(BetaAnalyticsUsageOrderBy.REQUESTS)
          .limit(25)
          .build();
      var rows = client.beta().organization().analytics().usage().list(params);

      for (var row : rows.autoPager()) {
          IO.println(row.group().actor().orElse(null) + ": " + row.usage().requests().orElse(null));
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rows = $client->beta->organization->analytics->usage->list(
      startingAt: new \DateTimeImmutable('2026-09-01T00:00:00Z'),
      endingAt: new \DateTimeImmutable('2026-10-01T00:00:00Z'),
      groupBy: ['actor'],
      orderBy: 'requests',
      limit: 25,
  );

  foreach ($rows->pagingEachItem() as $row) {
      $actor = json_encode($row->group->actor);
      echo "{$actor}: {$row->usage->requests}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.analytics.usage.list(
    starting_at: Time.utc(2026, 9, 1),
    ending_at: Time.utc(2026, 10, 1),
    group_by: [:actor],
    order_by: :requests,
    limit: 25
  )

  page.auto_paging_each do |row|
    puts "#{row.group.actor}: #{row.usage.requests}"
  end
  ```
</CodeGroup>

## Endpoint biaya

`GET /v1/organizations/analytics/cost` menerima filter, dimensi, dan time bucket yang sama dengan endpoint `/usage`. Objek `cost` pada setiap baris memuat `amount` (biaya setelah diskon dan sebelum kredit apa pun diterapkan), `list_amount` (biaya berdasarkan harga daftar), `currency` (selalu `"USD"`), dan `requests`. Jumlah berupa string desimal dalam sen dengan enam angka desimal: `"41280.000000"` adalah $412,80 USD. `order_by` menerima `amount` (default), `list_amount`, atau `time`.

Dua dimensi tambahan hanya ada pada endpoint ini dan tidak dihitung dalam batas lima dimensi: `group_by[]=cost_type` membagi setiap baris menjadi satu baris untuk setiap jenis biaya, dan `group_by[]=token_type` membagi biaya token menjadi satu baris untuk setiap jenis token. `limit` juga tidak berlaku untuk kedua dimensi ini, sehingga satu halaman dapat berisi lebih dari `limit` baris. Misalnya, biaya berdasarkan model, jenis biaya, dan jenis token selama satu bulan:

<CodeGroup>
  ```bash cURL
  curl --globoff "https://api.anthropic.com/v1/organizations/analytics/cost?\
  starting_at=2026-09-01T00:00:00Z&\
  ending_at=2026-10-01T00:00:00Z&\
  group_by[]=model&\
  group_by[]=cost_type&\
  group_by[]=token_type" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: analytics-usage-cost-2026-08-24" \
    -H "x-api-key: $ANTHROPIC_API_KEY"
  ```

  ```bash CLI
  ant beta:organization:analytics:cost list \
    --starting-at 2026-09-01T00:00:00Z \
    --ending-at 2026-10-01T00:00:00Z \
    --group-by model \
    --group-by cost_type \
    --group-by token_type
  ```

  ```python Python
  client = anthropic.Anthropic()

  rows = client.beta.organization.analytics.cost.list(
      starting_at="2026-09-01T00:00:00Z",
      ending_at="2026-10-01T00:00:00Z",
      group_by=["model", "cost_type", "token_type"],
  )

  for row in rows:
      print(
          f"{row.group.model} {row.group.cost_type} {row.group.token_type}: {row.cost.amount}"
      )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rows = await client.beta.organization.analytics.cost.list({
    starting_at: "2026-09-01T00:00:00Z",
    ending_at: "2026-10-01T00:00:00Z",
    group_by: ["model", "cost_type", "token_type"]
  });

  for await (const row of rows) {
    console.log(
      `${row.group.model} ${row.group.cost_type} ${row.group.token_type}: ${row.cost.amount}`
    );
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Analytics.Cost;

  AnthropicClient client = new();

  var page = await client.Beta.Organization.Analytics.Cost.List(
      new()
      {
          StartingAt = DateTimeOffset.Parse("2026-09-01T00:00:00Z"),
          EndingAt = DateTimeOffset.Parse("2026-10-01T00:00:00Z"),
          GroupBy = [BetaAnalyticsCostGroupBy.Model, BetaAnalyticsCostGroupBy.CostType, BetaAnalyticsCostGroupBy.TokenType],
      }
  );

  await foreach (var row in page.Paginate())
  {
      Console.WriteLine(
          $"{row.Group.Model} {row.Group.CostType?.Raw()} {row.Group.TokenType?.Raw()}: {row.Cost.Amount}"
      );
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rows := client.Beta.Organization.Analytics.Cost.ListAutoPaging(context.Background(), anthropic.BetaOrganizationAnalyticsCostListParams{
  	StartingAt: time.Date(2026, time.September, 1, 0, 0, 0, 0, time.UTC),
  	EndingAt:   anthropic.Time(time.Date(2026, time.October, 1, 0, 0, 0, 0, time.UTC)),
  	GroupBy:    []anthropic.BetaAnalyticsCostGroupBy{anthropic.BetaAnalyticsCostGroupByModel, anthropic.BetaAnalyticsCostGroupByCostType, anthropic.BetaAnalyticsCostGroupByTokenType},
  })

  for rows.Next() {
  	row := rows.Current()
  	fmt.Printf("%s %s %s: %s\n", row.Group.Model, row.Group.CostType, row.Group.TokenType, row.Cost.Amount)
  }
  if err := rows.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.analytics.cost.BetaAnalyticsCostGroupBy;
  import com.anthropic.models.beta.organization.analytics.cost.CostListParams;
  import java.time.OffsetDateTime;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = CostListParams.builder()
          .startingAt(OffsetDateTime.parse("2026-09-01T00:00:00Z"))
          .endingAt(OffsetDateTime.parse("2026-10-01T00:00:00Z"))
          .addGroupBy(BetaAnalyticsCostGroupBy.MODEL)
          .addGroupBy(BetaAnalyticsCostGroupBy.COST_TYPE)
          .addGroupBy(BetaAnalyticsCostGroupBy.TOKEN_TYPE)
          .build();
      var rows = client.beta().organization().analytics().cost().list(params);

      for (var row : rows.autoPager()) {
          var group = row.group();
          IO.println(
              group.model().orElse(null) + " " + group.costType().orElse(null) + " "
                  + group.tokenType().orElse(null) + ": " + row.cost().amount()
          );
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rows = $client->beta->organization->analytics->cost->list(
      startingAt: new \DateTimeImmutable('2026-09-01T00:00:00Z'),
      endingAt: new \DateTimeImmutable('2026-10-01T00:00:00Z'),
      groupBy: ['model', 'cost_type', 'token_type'],
  );

  foreach ($rows->pagingEachItem() as $row) {
      $group = $row->group;
      echo "{$group->model} {$group->costType} {$group->tokenType}: {$row->cost->amount}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.analytics.cost.list(
    starting_at: Time.utc(2026, 9, 1),
    ending_at: Time.utc(2026, 10, 1),
    group_by: [:model, :cost_type, :token_type]
  )

  page.auto_paging_each do |row|
    group = row.group
    puts "#{group.model} #{group.cost_type} #{group.token_type}: #{row.cost.amount}"
  end
  ```
</CodeGroup>

Untuk setiap model, respons berisi lima baris `tokens` (satu untuk setiap jenis token) ditambah masing-masing satu baris untuk `web_search`, `code_execution`, dan `session_usage`. Salah satu baris tersebut:

```json
{
  "starting_at": "2026-09-01T00:00:00Z",
  "ending_at": "2026-10-01T00:00:00Z",
  "group": {
    "model": "claude-opus-5",
    ...,
    "cost_type": "tokens",
    "token_type": "cache_read_input_tokens"
  },
  "cost": {
    "currency": "USD",
    "amount": "41280.000000",
    "list_amount": "51600.000000",
    "requests": null
  }
}
```

Objek `group` memuat setiap dimensi dan disingkat di sini. Dengan `group_by[]=cost_type` atau `token_type` ditentukan, `requests` bernilai `null` di setiap baris.

<Warning>
  Permintaan yang dilayani di bawah komitmen Priority Tier muncul di endpoint penggunaan dengan `service_tier: "priority"` tetapi menyumbang biaya token nol ke `amount` dan `list_amount`, karena komitmen Anda menanggungnya; biaya komitmen ditagih secara terpisah dan tidak ada dalam data ini. Pencarian web pada permintaan tersebut ditagih dengan tarif standar. Permintaan yang melebihi kapasitas komitmen Anda dilayani dan diberi harga pada tingkat standar.
</Warning>

## Rentang tanggal dan time bucket

* Timestamp menggunakan format RFC 3339 dengan offset UTC, misalnya `2026-09-01T00:00:00Z`. `starting_at` bersifat inklusif dan `ending_at` bersifat eksklusif.
* `starting_at` harus pada atau setelah 1 Januari 2026, dan dalam 365 hari terakhir. Satu permintaan dapat mencakup paling lama 31 hari; `ending_at` secara default adalah 31 hari setelah `starting_at` atau waktu saat ini, mana yang lebih awal.
* `ending_at` wajib diisi setiap kali `time_bucket_width` diatur, dan dengan `time_bucket_width=1m` satu permintaan dapat mencakup paling lama 24 jam.
* Kedua ujung rentang dibulatkan ke bawah ke batas bucket UTC, atau ke jam ketika `time_bucket_width` tidak diatur. Misalnya, dengan `time_bucket_width=1h`, `starting_at` bernilai `2026-09-01T10:43:00Z` diperlakukan sebagai `2026-09-01T10:00:00Z` dan `ending_at` bernilai `2026-09-01T15:43:00Z` sebagai `2026-09-01T15:00:00Z`, sehingga respons mencakup pukul 10:00 hingga 15:00 UTC.

## Kesegaran data

Setiap respons menyertakan timestamp `data_refreshed_at`, dan penggunaan setelah waktu tersebut hilang atau parsial. Ketika belum ada data yang tersedia untuk bagian mana pun dari rentang yang diminta, `data_refreshed_at` bernilai `null` dan `data` kosong. Data biasanya diperbarui dalam 4 jam setelah penggunaan yang mendasarinya dan dapat memakan waktu hingga 24 jam. Nilai dapat direvisi saat peristiwa yang terlambat tiba dan rekonsiliasi berjalan, hingga sekitar 7 hari setelah akhir bulan kalender. Misalnya, nilai untuk 1 Oktober dapat berubah hingga sekitar 7 November. Untuk hasil yang stabil di seluruh panggilan berulang, atur `ending_at` pada atau sebelum `data_refreshed_at` yang sudah Anda lihat; untuk total final, kueri hanya bulan-bulan yang berakhir setidaknya 7 hari yang lalu. Setiap halaman dari kueri berpaginasi membaca snapshot data yang sama, sehingga `data_refreshed_at` identik di seluruh halaman.

## Migrasi dari Usage and Cost API

Bagian ini ditujukan untuk organisasi Claude Console yang memanggil [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api) lama (`/v1/organizations/usage_report/messages` dan `/v1/organizations/cost_report`). Kunci Admin API Anda, header `anthropic-version`, `starting_at` dan `ending_at`, nilai lebar bucket (`1m`, `1h`, `1d`), notasi kurung siku, nama field paginasi, serta nama field token dan biaya tetap berlaku. Yang berubah:

| Usage and Cost API                                                                                                                                                                  | Usage and Cost Analytics API                                                                                                                                                                                                                                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tanpa header beta                                                                                                                                                                   | `anthropic-beta: analytics-usage-cost-2026-08-24` pada setiap permintaan                                                                                                                                                                                                                                                                                                                                                      |
| Data biasanya muncul dalam 5 menit                                                                                                                                                  | Data biasanya diperbarui dalam 4 jam dan dapat memakan waktu hingga 24 jam (lihat [Kesegaran data](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api#data-freshness))                                                                                                                                                                                                                                |
| `data` adalah daftar time bucket, yang terlama terlebih dahulu, termasuk yang kosong, masing-masing dengan daftar `results` yang entrinya menampung dimensi dan metrik berdampingan | `data` adalah daftar baris yang diurutkan berdasarkan `order_by`, masing-masing dengan `starting_at` dan `ending_at` sendiri, dimensi di `group`, dan metrik di `usage` atau `cost`. Kombinasi tanpa penggunaan atau biaya tidak memiliki baris.                                                                                                                                                                              |
| `bucket_width`, default `1d`                                                                                                                                                        | `time_bucket_width`, tanpa default. Teruskan `time_bucket_width=1d` untuk mempertahankan baris harian; hilangkan untuk total seluruh rentang. Endpoint biaya juga menerima setiap filter serta bucket `1m` dan `1h`.                                                                                                                                                                                                          |
| `limit` menghitung time bucket per halaman                                                                                                                                          | `limit` menghitung baris per halaman (1 hingga 1.000, default 20), sehingga jumlah halaman bergantung pada berapa banyak kombinasi yang memiliki data                                                                                                                                                                                                                                                                         |
| Rentang tanggal apa pun, dipaginasi maju per bucket                                                                                                                                 | `starting_at` pada atau setelah 1 Januari 2026, dan dalam 365 hari terakhir, paling banyak 31 hari per permintaan, `ending_at` wajib dengan `time_bucket_width`, dan paling banyak 24 jam dengan bucket `1m` (lihat [Rentang tanggal dan time bucket](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api#date-ranges-and-time-buckets)). Bagi rentang yang lebih panjang menjadi beberapa permintaan. |
| `account_ids[]`, `service_account_ids[]`, `group_by[]=account_id`, `group_by[]=service_account_id`                                                                                  | `actor_ids[]` dengan ID bertag yang sama, dan `group_by[]=actor` atau `actor_type`; baca `actor.user_id` atau `actor.service_account_id`. Lihat [Aktor](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api#actors).                                                                                                                                                                                   |
| `context_window[]`                                                                                                                                                                  | `context_windows[]`                                                                                                                                                                                                                                                                                                                                                                                                           |
| `group_by[]=description` pada laporan biaya, dengan string `description`                                                                                                            | Tidak ada `description`. Sebagai gantinya, kelompokkan berdasarkan dimensi terstruktur: salah satu dari `model`, `cost_type`, `token_type`, `context_window`, `service_tier`, `inference_geo`, dan `speed`, yang semuanya muat dalam satu permintaan.                                                                                                                                                                         |
| Kunci API atau ID workspace yang tidak dikenal mengembalikan error                                                                                                                  | Tidak cocok dengan apa pun, termasuk nama `models[]` yang salah eja. Setiap daftar menerima hingga 100 nilai.                                                                                                                                                                                                                                                                                                                 |
| `workspace_id: null` untuk workspace default                                                                                                                                        | `workspace_id` asli dari workspace default (lihat [Bagaimana workspace default direpresentasikan?](https://platform.claude.com/docs/id/manage-claude/usage-cost-analytics-api#how-is-the-default-workspace-represented))                                                                                                                                                                                                      |
| `inference_geo: "not_available"` dan `service_tier: "standard"` pada penggunaan tanpa geo atau tingkat                                                                              | `null` untuk keduanya. `inference_geos[]=not_available` tetap mencocokkan baris tanpa inference geo.                                                                                                                                                                                                                                                                                                                          |
| `service_tier` biaya adalah `standard` atau `batch`; `amount` seperti `"123.45"`                                                                                                    | Tingkat yang sebenarnya; `amount` dengan enam angka desimal, seperti `"123.450000"`, ditambah `list_amount`.                                                                                                                                                                                                                                                                                                                  |
| Eksekusi kode tidak ada dalam laporan penggunaan; tidak ada jumlah permintaan                                                                                                       | Eksekusi kode muncul sebagai baris penggunaan dengan `model: null`; menambahkan `requests` pada kedua endpoint dan `total_tokens` pada baris penggunaan                                                                                                                                                                                                                                                                       |

Untuk mereproduksi laporan harian lama, minta `time_bucket_width=1d` dengan `group_by[]` yang sama, telusuri halaman dengan `limit=1000`, lalu kelompokkan baris berdasarkan `starting_at` dan isi hari yang hilang dengan nol. Tambahkan `order_by=time&order=asc` untuk mendapatkan hari-hari secara berurutan. Penggunaan harian berdasarkan model selama 1 minggu, sebelumnya:

```bash cURL
curl --globoff "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2026-09-01T00:00:00Z&\
ending_at=2026-09-08T00:00:00Z&\
group_by[]=model&\
bucket_width=1d" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_API_KEY"
```

dan sesudahnya:

<CodeGroup>
  ```bash cURL
  curl --globoff "https://api.anthropic.com/v1/organizations/analytics/usage?\
  starting_at=2026-09-01T00:00:00Z&\
  ending_at=2026-09-08T00:00:00Z&\
  group_by[]=model&\
  time_bucket_width=1d&\
  limit=1000" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: analytics-usage-cost-2026-08-24" \
    -H "x-api-key: $ANTHROPIC_API_KEY"
  ```

  ```bash CLI
  ant beta:organization:analytics:usage list \
    --starting-at 2026-09-01T00:00:00Z \
    --ending-at 2026-09-08T00:00:00Z \
    --time-bucket-width 1d \
    --group-by model \
    --limit 1000
  ```

  ```python Python
  client = anthropic.Anthropic()

  rows = client.beta.organization.analytics.usage.list(
      starting_at="2026-09-01T00:00:00Z",
      ending_at="2026-09-08T00:00:00Z",
      time_bucket_width="1d",
      group_by=["model"],
      limit=1000,
  )

  for row in rows:
      print(f"{row.starting_at} {row.group.model}: {row.usage.total_tokens}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rows = await client.beta.organization.analytics.usage.list({
    starting_at: "2026-09-01T00:00:00Z",
    ending_at: "2026-09-08T00:00:00Z",
    time_bucket_width: "1d",
    group_by: ["model"],
    limit: 1000
  });

  for await (const row of rows) {
    console.log(`${row.starting_at} ${row.group.model}: ${row.usage.total_tokens}`);
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Analytics;
  using Anthropic.Models.Beta.Organization.Analytics.Usage;

  AnthropicClient client = new();

  var page = await client.Beta.Organization.Analytics.Usage.List(
      new()
      {
          StartingAt = DateTimeOffset.Parse("2026-09-01T00:00:00Z"),
          EndingAt = DateTimeOffset.Parse("2026-09-08T00:00:00Z"),
          TimeBucketWidth = BetaAnalyticsTimeBucketWidth.Day,
          GroupBy = [BetaAnalyticsUsageGroupBy.Model],
          Limit = 1000,
      }
  );

  await foreach (var row in page.Paginate())
  {
      Console.WriteLine($"{row.StartingAt} {row.Group.Model}: {row.Usage.TotalTokens}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rows := client.Beta.Organization.Analytics.Usage.ListAutoPaging(context.Background(), anthropic.BetaOrganizationAnalyticsUsageListParams{
  	StartingAt:      time.Date(2026, time.September, 1, 0, 0, 0, 0, time.UTC),
  	EndingAt:        anthropic.Time(time.Date(2026, time.September, 8, 0, 0, 0, 0, time.UTC)),
  	TimeBucketWidth: anthropic.BetaAnalyticsTimeBucketWidthDay,
  	GroupBy:         []anthropic.BetaAnalyticsUsageGroupBy{anthropic.BetaAnalyticsUsageGroupByModel},
  	Limit:           anthropic.Int(1000),
  })

  for rows.Next() {
  	row := rows.Current()
  	fmt.Printf("%s %s: %d\n", row.StartingAt.Format(time.RFC3339), row.Group.Model, row.Usage.TotalTokens)
  }
  if err := rows.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.analytics.BetaAnalyticsTimeBucketWidth;
  import com.anthropic.models.beta.organization.analytics.usage.BetaAnalyticsUsageGroupBy;
  import com.anthropic.models.beta.organization.analytics.usage.UsageListParams;
  import java.time.OffsetDateTime;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UsageListParams.builder()
          .startingAt(OffsetDateTime.parse("2026-09-01T00:00:00Z"))
          .endingAt(OffsetDateTime.parse("2026-09-08T00:00:00Z"))
          .timeBucketWidth(BetaAnalyticsTimeBucketWidth.DAY)
          .addGroupBy(BetaAnalyticsUsageGroupBy.MODEL)
          .limit(1000)
          .build();
      var rows = client.beta().organization().analytics().usage().list(params);

      for (var row : rows.autoPager()) {
          IO.println(row.startingAt() + " " + row.group().model().orElse(null) + ": " + row.usage().totalTokens());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rows = $client->beta->organization->analytics->usage->list(
      startingAt: new \DateTimeImmutable('2026-09-01T00:00:00Z'),
      endingAt: new \DateTimeImmutable('2026-09-08T00:00:00Z'),
      timeBucketWidth: '1d',
      groupBy: ['model'],
      limit: 1000,
  );

  foreach ($rows->pagingEachItem() as $row) {
      $startingAt = $row->startingAt->format(\DateTimeInterface::ATOM);
      echo "{$startingAt} {$row->group->model}: {$row->usage->totalTokens}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.analytics.usage.list(
    starting_at: Time.utc(2026, 9, 1),
    ending_at: Time.utc(2026, 9, 8),
    time_bucket_width: :"1d",
    group_by: [:model],
    limit: 1000
  )

  page.auto_paging_each do |row|
    puts "#{row.starting_at} #{row.group.model}: #{row.usage.total_tokens}"
  end
  ```
</CodeGroup>

Biaya harian berdasarkan workspace, model, tingkat layanan, jendela konteks, dan inference geo, dibagi berdasarkan jenis biaya dan jenis token:

<CodeGroup>
  ```bash cURL
  curl --globoff "https://api.anthropic.com/v1/organizations/analytics/cost?\
  starting_at=2026-09-01T00:00:00Z&\
  ending_at=2026-09-08T00:00:00Z&\
  time_bucket_width=1d&\
  group_by[]=workspace_id&\
  group_by[]=model&\
  group_by[]=service_tier&\
  group_by[]=context_window&\
  group_by[]=inference_geo&\
  group_by[]=cost_type&\
  group_by[]=token_type&\
  limit=1000" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: analytics-usage-cost-2026-08-24" \
    -H "x-api-key: $ANTHROPIC_API_KEY"
  ```

  ```bash CLI
  ant beta:organization:analytics:cost list \
    --starting-at 2026-09-01T00:00:00Z \
    --ending-at 2026-09-08T00:00:00Z \
    --time-bucket-width 1d \
    --group-by workspace_id \
    --group-by model \
    --group-by service_tier \
    --group-by context_window \
    --group-by inference_geo \
    --group-by cost_type \
    --group-by token_type \
    --limit 1000
  ```

  ```python Python
  client = anthropic.Anthropic()

  rows = client.beta.organization.analytics.cost.list(
      starting_at="2026-09-01T00:00:00Z",
      ending_at="2026-09-08T00:00:00Z",
      time_bucket_width="1d",
      group_by=[
          "workspace_id",
          "model",
          "service_tier",
          "context_window",
          "inference_geo",
          "cost_type",
          "token_type",
      ],
      limit=1000,
  )

  for row in rows:
      group = row.group
      print(
          f"{row.starting_at} {group.workspace_id} {group.model} {group.service_tier} "
          f"{group.context_window} {group.inference_geo} {group.cost_type} {group.token_type}: "
          f"{row.cost.amount}"
      )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rows = await client.beta.organization.analytics.cost.list({
    starting_at: "2026-09-01T00:00:00Z",
    ending_at: "2026-09-08T00:00:00Z",
    time_bucket_width: "1d",
    group_by: [
      "workspace_id",
      "model",
      "service_tier",
      "context_window",
      "inference_geo",
      "cost_type",
      "token_type"
    ],
    limit: 1000
  });

  for await (const row of rows) {
    const { group } = row;
    console.log(
      `${row.starting_at} ${group.workspace_id} ${group.model} ${group.service_tier} ` +
        `${group.context_window} ${group.inference_geo} ${group.cost_type} ${group.token_type}: ` +
        `${row.cost.amount}`
    );
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Analytics;
  using Anthropic.Models.Beta.Organization.Analytics.Cost;

  AnthropicClient client = new();

  var page = await client.Beta.Organization.Analytics.Cost.List(
      new()
      {
          StartingAt = DateTimeOffset.Parse("2026-09-01T00:00:00Z"),
          EndingAt = DateTimeOffset.Parse("2026-09-08T00:00:00Z"),
          TimeBucketWidth = BetaAnalyticsTimeBucketWidth.Day,
          GroupBy =
          [
              BetaAnalyticsCostGroupBy.WorkspaceID,
              BetaAnalyticsCostGroupBy.Model,
              BetaAnalyticsCostGroupBy.ServiceTier,
              BetaAnalyticsCostGroupBy.ContextWindow,
              BetaAnalyticsCostGroupBy.InferenceGeo,
              BetaAnalyticsCostGroupBy.CostType,
              BetaAnalyticsCostGroupBy.TokenType,
          ],
          Limit = 1000,
      }
  );

  await foreach (var row in page.Paginate())
  {
      var group = row.Group;
      Console.WriteLine(
          $"{row.StartingAt} {group.WorkspaceID} {group.Model} {group.ServiceTier?.Raw()} "
              + $"{group.ContextWindow?.Raw()} {group.InferenceGeo?.Raw()} {group.CostType?.Raw()} "
              + $"{group.TokenType?.Raw()}: {row.Cost.Amount}"
      );
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rows := client.Beta.Organization.Analytics.Cost.ListAutoPaging(context.Background(), anthropic.BetaOrganizationAnalyticsCostListParams{
  	StartingAt:      time.Date(2026, time.September, 1, 0, 0, 0, 0, time.UTC),
  	EndingAt:        anthropic.Time(time.Date(2026, time.September, 8, 0, 0, 0, 0, time.UTC)),
  	TimeBucketWidth: anthropic.BetaAnalyticsTimeBucketWidthDay,
  	GroupBy: []anthropic.BetaAnalyticsCostGroupBy{
  		anthropic.BetaAnalyticsCostGroupByWorkspaceID,
  		anthropic.BetaAnalyticsCostGroupByModel,
  		anthropic.BetaAnalyticsCostGroupByServiceTier,
  		anthropic.BetaAnalyticsCostGroupByContextWindow,
  		anthropic.BetaAnalyticsCostGroupByInferenceGeo,
  		anthropic.BetaAnalyticsCostGroupByCostType,
  		anthropic.BetaAnalyticsCostGroupByTokenType,
  	},
  	Limit: anthropic.Int(1000),
  })

  for rows.Next() {
  	row := rows.Current()
  	group := row.Group
  	fmt.Printf("%s %s %s %s %s %s %s %s: %s\n",
  		row.StartingAt.Format(time.RFC3339), group.WorkspaceID, group.Model, group.ServiceTier,
  		group.ContextWindow, group.InferenceGeo, group.CostType, group.TokenType, row.Cost.Amount)
  }
  if err := rows.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.analytics.BetaAnalyticsTimeBucketWidth;
  import com.anthropic.models.beta.organization.analytics.cost.BetaAnalyticsCostGroupBy;
  import com.anthropic.models.beta.organization.analytics.cost.CostListParams;
  import java.time.OffsetDateTime;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = CostListParams.builder()
          .startingAt(OffsetDateTime.parse("2026-09-01T00:00:00Z"))
          .endingAt(OffsetDateTime.parse("2026-09-08T00:00:00Z"))
          .timeBucketWidth(BetaAnalyticsTimeBucketWidth.DAY)
          .addGroupBy(BetaAnalyticsCostGroupBy.WORKSPACE_ID)
          .addGroupBy(BetaAnalyticsCostGroupBy.MODEL)
          .addGroupBy(BetaAnalyticsCostGroupBy.SERVICE_TIER)
          .addGroupBy(BetaAnalyticsCostGroupBy.CONTEXT_WINDOW)
          .addGroupBy(BetaAnalyticsCostGroupBy.INFERENCE_GEO)
          .addGroupBy(BetaAnalyticsCostGroupBy.COST_TYPE)
          .addGroupBy(BetaAnalyticsCostGroupBy.TOKEN_TYPE)
          .limit(1000)
          .build();
      var rows = client.beta().organization().analytics().cost().list(params);

      for (var row : rows.autoPager()) {
          var group = row.group();
          IO.println(
              row.startingAt() + " " + group.workspaceId().orElse(null) + " " + group.model().orElse(null) + " "
                  + group.serviceTier().orElse(null) + " " + group.contextWindow().orElse(null) + " "
                  + group.inferenceGeo().orElse(null) + " " + group.costType().orElse(null) + " "
                  + group.tokenType().orElse(null) + ": " + row.cost().amount()
          );
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rows = $client->beta->organization->analytics->cost->list(
      startingAt: new \DateTimeImmutable('2026-09-01T00:00:00Z'),
      endingAt: new \DateTimeImmutable('2026-09-08T00:00:00Z'),
      timeBucketWidth: '1d',
      groupBy: [
          'workspace_id',
          'model',
          'service_tier',
          'context_window',
          'inference_geo',
          'cost_type',
          'token_type',
      ],
      limit: 1000,
  );

  foreach ($rows->pagingEachItem() as $row) {
      $startingAt = $row->startingAt->format(\DateTimeInterface::ATOM);
      $group = $row->group;
      echo "{$startingAt} {$group->workspaceID} {$group->model} {$group->serviceTier} "
          . "{$group->contextWindow} {$group->inferenceGeo} {$group->costType} {$group->tokenType}: "
          . "{$row->cost->amount}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.analytics.cost.list(
    starting_at: Time.utc(2026, 9, 1),
    ending_at: Time.utc(2026, 9, 8),
    time_bucket_width: :"1d",
    group_by: [
      :workspace_id,
      :model,
      :service_tier,
      :context_window,
      :inference_geo,
      :cost_type,
      :token_type
    ],
    limit: 1000
  )

  page.auto_paging_each do |row|
    group = row.group
    puts "#{row.starting_at} #{group.workspace_id} #{group.model} #{group.service_tier} " \
      "#{group.context_window} #{group.inference_geo} #{group.cost_type} #{group.token_type}: " \
      "#{row.cost.amount}"
  end
  ```
</CodeGroup>

## Migrasi dari laporan penggunaan dan biaya Claude Enterprise

Bagian ini ditujukan untuk organisasi Claude Enterprise yang memanggil endpoint laporan [Claude Enterprise Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api) `usage_report`, `cost_report`, `user_usage_report`, dan `user_cost_report` di bawah `/v1/organizations/analytics/`. Endpoint tersebut merupakan endpoint lama dan tetap didukung. Beralihlah ke `/analytics/usage` dan `/analytics/cost` ketika Anda menginginkan salah satu dari hal berikut:

* Setiap grup di setiap time bucket, alih-alih 100 grup teratas di setiap bucket
* Pengelompokan berdasarkan `actor` atau `actor_type` bersama dengan dimensi lain, pada penggunaan maupun biaya
* Baris yang diurutkan berdasarkan metrik pilihan Anda di seluruh rentang, atau diurutkan berdasarkan time bucket
* Satu integrasi yang juga melayani organisasi Claude Console

Kunci Anda, tanggal paling awal, jangkauan mundur 365 hari dan rentang 31 hari, nama dan nilai filter serta dimensi (kecuali `user_ids[]` dan nilai produk Claude Tag), field `actor` pengguna, field metrik dan jumlah, `data_refreshed_at`, aturan cursor, dan [batas laju tingkat organisasi](https://platform.claude.com/docs/id/manage-claude/analytics-api#working-with-the-api) tetap berlaku. Satu-satunya header baru adalah header beta `analytics-usage-cost-2026-08-24`. Yang berubah:

| Laporan Claude Enterprise                                                                                                                                                                                                               | Usage and Cost Analytics API                                                                                                                                                                                                                                                      |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `usage_report` dan `cost_report` mengembalikan time bucket, yang terlama terlebih dahulu, termasuk yang kosong, masing-masing menampung paling banyak 100 grup teratasnya; `bucket_width` default ke `1d` dan `limit` menghitung bucket | Baris yang mencakup setiap kombinasi yang memiliki data, diurutkan berdasarkan `order_by`, masing-masing dengan `starting_at` dan `ending_at` sendiri, dimensi di `group`, dan metrik di `usage` atau `cost`. `time_bucket_width` bersifat opsional dan `limit` menghitung baris. |
| Parameter time bucket adalah `bucket_width`                                                                                                                                                                                             | Parameternya adalah `time_bucket_width`, dengan nilai yang sama                                                                                                                                                                                                                   |
| Pada `usage_report` dan `cost_report`, `ending_at` bersifat opsional dengan `bucket_width` dan bucket `1m` dapat mencakup hingga 31 hari                                                                                                | `ending_at` wajib dengan `time_bucket_width`; bucket `1m` mencakup paling banyak 24 jam per permintaan                                                                                                                                                                            |
| `user_usage_report` dan `user_cost_report` mengembalikan satu baris per pengguna                                                                                                                                                        | `group_by[]=actor&actor_types[]=user_actor`. Tanpa filter tersebut, Anda juga mendapatkan baris untuk identitas non-pengguna dan baris `actor: null` untuk penggunaan yang tidak teratribusi.                                                                                     |
| Penggunaan Claude Tag memiliki `product: "claude-tag"`                                                                                                                                                                                  | `product: "claude_tag"`; `products[]` menerima kedua ejaan                                                                                                                                                                                                                        |
| Nama `models[]` yang tidak dikenali mengembalikan error 400                                                                                                                                                                             | Tidak cocok dengan apa pun                                                                                                                                                                                                                                                        |
| `user_ids[]`                                                                                                                                                                                                                            | `actor_ids[]` dengan ID bertag `user_...` yang sama                                                                                                                                                                                                                               |
| `exclude_deleted_users` pada laporan per pengguna                                                                                                                                                                                       | Memerlukan `group_by[]=actor`; tanpanya, permintaan mengembalikan error 400. Parameter ini hanya menghapus baris yang `actor`-nya adalah pengguna dengan `deleted: true`; baris untuk identitas lain dan baris dengan `actor: null` tetap ada.                                    |

Biaya per pengguna selama sebulan, sebelumnya:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/analytics/user_cost_report?\
  starting_at=2026-09-01T00:00:00Z&\
  ending_at=2026-10-01T00:00:00Z&\
  limit=100" \
    -H "anthropic-version: 2023-06-01" \
    -H "x-api-key: $ANTHROPIC_API_KEY"
  ```

  ```bash CLI
  ant beta:organization:analytics:user-cost-report list \
    --starting-at 2026-09-01T00:00:00Z \
    --ending-at 2026-10-01T00:00:00Z \
    --limit 100
  ```

  ```python Python
  client = anthropic.Anthropic()

  rows = client.beta.organization.analytics.user_cost_report.list(
      starting_at="2026-09-01T00:00:00Z",
      ending_at="2026-10-01T00:00:00Z",
      limit=100,
  )

  for row in rows:
      print(f"{row.actor.user_id}: {row.amount}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rows = await client.beta.organization.analytics.userCostReport.list({
    starting_at: "2026-09-01T00:00:00Z",
    ending_at: "2026-10-01T00:00:00Z",
    limit: 100
  });

  for await (const row of rows) {
    console.log(`${row.actor.user_id}: ${row.amount}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.Analytics.UserCostReport.List(
      new()
      {
          StartingAt = DateTimeOffset.Parse("2026-09-01T00:00:00Z"),
          EndingAt = DateTimeOffset.Parse("2026-10-01T00:00:00Z"),
          Limit = 100,
      }
  );

  await foreach (var row in page.Paginate())
  {
      Console.WriteLine($"{row.Actor.UserID}: {row.Amount}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rows := client.Beta.Organization.Analytics.UserCostReport.ListAutoPaging(context.Background(), anthropic.BetaOrganizationAnalyticsUserCostReportListParams{
  	StartingAt: time.Date(2026, time.September, 1, 0, 0, 0, 0, time.UTC),
  	EndingAt:   anthropic.Time(time.Date(2026, time.October, 1, 0, 0, 0, 0, time.UTC)),
  	Limit:      anthropic.Int(100),
  })

  for rows.Next() {
  	row := rows.Current()
  	fmt.Printf("%s: %s\n", row.Actor.UserID, row.Amount)
  }
  if err := rows.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.analytics.usercostreport.UserCostReportListParams;
  import java.time.OffsetDateTime;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UserCostReportListParams.builder()
          .startingAt(OffsetDateTime.parse("2026-09-01T00:00:00Z"))
          .endingAt(OffsetDateTime.parse("2026-10-01T00:00:00Z"))
          .limit(100)
          .build();
      var rows = client.beta().organization().analytics().userCostReport().list(params);

      for (var row : rows.autoPager()) {
          IO.println(row.actor().userId() + ": " + row.amount());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $rows = $client->beta->organization->analytics->userCostReport->list(
      startingAt: new \DateTimeImmutable('2026-09-01T00:00:00Z'),
      endingAt: new \DateTimeImmutable('2026-10-01T00:00:00Z'),
      limit: 100,
  );

  foreach ($rows->pagingEachItem() as $row) {
      echo "{$row->actor->userID}: {$row->amount}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.analytics.user_cost_report.list(
    starting_at: Time.utc(2026, 9, 1),
    ending_at: Time.utc(2026, 10, 1),
    limit: 100
  )

  page.auto_paging_each do |row|
    puts "#{row.actor.user_id}: #{row.amount}"
  end
  ```
</CodeGroup>

dan sesudahnya, dengan tambahan rincian berdasarkan produk:

<CodeGroup>
  ```bash cURL
  curl --globoff "https://api.anthropic.com/v1/organizations/analytics/cost?\
  starting_at=2026-09-01T00:00:00Z&\
  ending_at=2026-10-01T00:00:00Z&\
  group_by[]=actor&\
  group_by[]=product&\
  actor_types[]=user_actor&\
  limit=100" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: analytics-usage-cost-2026-08-24" \
    -H "x-api-key: $ANTHROPIC_API_KEY"
  ```

  ```bash CLI
  ant beta:organization:analytics:cost list \
    --starting-at 2026-09-01T00:00:00Z \
    --ending-at 2026-10-01T00:00:00Z \
    --actor-type user_actor \
    --group-by actor \
    --group-by product \
    --limit 100
  ```

  ```python Python
  client = anthropic.Anthropic()

  rows = client.beta.organization.analytics.cost.list(
      starting_at="2026-09-01T00:00:00Z",
      ending_at="2026-10-01T00:00:00Z",
      actor_types=["user_actor"],
      group_by=["actor", "product"],
      limit=100,
  )

  for row in rows:
      actor = row.group.actor
      if actor is not None and actor.type == "user_actor":
          print(f"{actor.user_id} {row.group.product}: {row.cost.amount}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const rows = await client.beta.organization.analytics.cost.list({
    starting_at: "2026-09-01T00:00:00Z",
    ending_at: "2026-10-01T00:00:00Z",
    actor_types: ["user_actor"],
    group_by: ["actor", "product"],
    limit: 100
  });

  for await (const row of rows) {
    const { actor } = row.group;
    if (actor?.type === "user_actor") {
      console.log(`${actor.user_id} ${row.group.product}: ${row.cost.amount}`);
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.Analytics;
  using Anthropic.Models.Beta.Organization.Analytics.Cost;

  AnthropicClient client = new();

  var page = await client.Beta.Organization.Analytics.Cost.List(
      new()
      {
          StartingAt = DateTimeOffset.Parse("2026-09-01T00:00:00Z"),
          EndingAt = DateTimeOffset.Parse("2026-10-01T00:00:00Z"),
          ActorTypes = [BetaAnalyticsActorType.UserActor],
          GroupBy = [BetaAnalyticsCostGroupBy.Actor, BetaAnalyticsCostGroupBy.Product],
          Limit = 100,
      }
  );

  await foreach (var row in page.Paginate())
  {
      if (row.Group.Actor is { } actor && actor.TryPickReportUser(out var user))
      {
          Console.WriteLine($"{user.UserID} {row.Group.Product}: {row.Cost.Amount}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  rows := client.Beta.Organization.Analytics.Cost.ListAutoPaging(context.Background(), anthropic.BetaOrganizationAnalyticsCostListParams{
  	StartingAt: time.Date(2026, time.September, 1, 0, 0, 0, 0, time.UTC),
  	EndingAt:   anthropic.Time(time.Date(2026, time.October, 1, 0, 0, 0, 0, time.UTC)),
  	ActorTypes: []anthropic.BetaAnalyticsActorType{anthropic.BetaAnalyticsActorTypeUserActor},
  	GroupBy:    []anthropic.BetaAnalyticsCostGroupBy{anthropic.BetaAnalyticsCostGroupByActor, anthropic.BetaAnalyticsCostGroupByProduct},
  	Limit:      anthropic.Int(100),
  })

  for rows.Next() {
  	row := rows.Current()
  	if user, ok := row.Group.Actor.AsAny().(anthropic.BetaAnalyticsReportUserActor); ok {
  		fmt.Printf("%s %s: %s\n", user.UserID, row.Group.Product, row.Cost.Amount)
  	}
  }
  if err := rows.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.analytics.BetaAnalyticsActorType;
  import com.anthropic.models.beta.organization.analytics.cost.BetaAnalyticsCostGroupBy;
  import com.anthropic.models.beta.organization.analytics.cost.CostListParams;
  import java.time.OffsetDateTime;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = CostListParams.builder()
          .startingAt(OffsetDateTime.parse("2026-09-01T00:00:00Z"))
          .endingAt(OffsetDateTime.parse("2026-10-01T00:00:00Z"))
          .addActorType(BetaAnalyticsActorType.USER_ACTOR)
          .addGroupBy(BetaAnalyticsCostGroupBy.ACTOR)
          .addGroupBy(BetaAnalyticsCostGroupBy.PRODUCT)
          .limit(100)
          .build();
      var rows = client.beta().organization().analytics().cost().list(params);

      for (var row : rows.autoPager()) {
          row.group().actor().flatMap(actor -> actor.user()).ifPresent(user ->
              IO.println(user.userId() + " " + row.group().product().orElse(null) + ": " + row.cost().amount())
          );
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\Analytics\AnalyticsReportUserActor;
  // ...

  $client = new Client();

  $rows = $client->beta->organization->analytics->cost->list(
      startingAt: new \DateTimeImmutable('2026-09-01T00:00:00Z'),
      endingAt: new \DateTimeImmutable('2026-10-01T00:00:00Z'),
      actorTypes: ['user_actor'],
      groupBy: ['actor', 'product'],
      limit: 100,
  );

  foreach ($rows->pagingEachItem() as $row) {
      $actor = $row->group->actor;
      if ($actor instanceof AnalyticsReportUserActor) {
          echo "{$actor->userID} {$row->group->product}: {$row->cost->amount}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.analytics.cost.list(
    starting_at: Time.utc(2026, 9, 1),
    ending_at: Time.utc(2026, 10, 1),
    actor_types: [:user_actor],
    group_by: [:actor, :product],
    limit: 100
  )

  page.auto_paging_each do |row|
    actor = row.group.actor
    if actor.is_a?(Anthropic::Models::Beta::Organization::BetaAnalyticsReportUserActor)
      puts "#{actor.user_id} #{row.group.product}: #{row.cost.amount}"
    end
  end
  ```
</CodeGroup>

## Pertanyaan yang sering diajukan

### Bagaimana workspace default direpresentasikan?

Workspace default dari organisasi Claude Console memiliki ID `wrkspc_` sendiri, seperti workspace lainnya. Baris untuk workspace default memiliki ID tersebut di `workspace_id`, dan Anda dapat memfilternya dengan `workspace_ids[]`. [List Workspaces](https://platform.claude.com/docs/id/api/organization/workspaces/list) tidak menyertakan workspace default kecuali Anda meneruskan `include_default=true`. Untuk memeriksa apakah `workspace_id` yang tidak dikenal adalah workspace default, teruskan ID tersebut ke [Get Workspace](https://platform.claude.com/docs/id/api/organization/workspaces/retrieve): workspace default mengembalikan `"name": "Default"`.

### Bagaimana cara mendapatkan biaya per pengguna untuk Claude Code?

Panggil endpoint biaya dengan `products[]=claude_code&group_by[]=actor`. Organisasi Claude Console juga dapat menggunakan [Claude Code Analytics API](https://platform.claude.com/docs/id/manage-claude/claude-code-analytics-api), yang melaporkan aktivitas Claude Code per pengguna dan estimasi biaya.

## Lihat juga

* [Usage and Cost API](https://platform.claude.com/docs/id/manage-claude/usage-cost-api) (lama)
* [Analytics API](https://platform.claude.com/docs/id/manage-claude/analytics-api): API analitik dan jenis kunci mana yang dibutuhkan organisasi Anda
* [Claude Code Analytics API](https://platform.claude.com/docs/id/manage-claude/claude-code-analytics-api)
* [Referensi Admin API](https://platform.claude.com/docs/id/api/beta/organization)
* [Harga](https://platform.claude.com/docs/id/about-claude/pricing)
