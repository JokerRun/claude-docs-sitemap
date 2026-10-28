---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/spend-limits-api
fetched_at: 2026-10-28T02:15:32.412922Z
sha256: bca87973e56870ba3faea200fe33698f1f4e1d5736a9dd4d45feeabec7331cfa
---

---
title: Spend Limits API
url: https://platform.claude.com/docs/id/manage-claude/spend-limits-api
description: Tetapkan batas pengeluaran pada setiap anggota Claude Enterprise, lihat dari mana batas pengeluaran setiap anggota diwarisi, dan tinjau atau tindak lanjuti permintaan anggota untuk batas yang lebih tinggi.
---

Spend Limits API memungkinkan Anda menetapkan “spend limit” (batas pengeluaran) pada setiap anggota Claude Enterprise, melihat dari mana batas pengeluaran setiap anggota diwarisi, dan meninjau atau menindaklanjuti permintaan anggota untuk batas yang lebih tinggi.

Untuk *pelaporan* penggunaan dan biaya per pengguna dan per rentang waktu, lihat [Analytics APIs](https://platform.claude.com/docs/id/manage-claude/analytics-api).

<Check>
  **Diperlukan kunci Admin API dengan cakupan**

  Endpoint ini memerlukan kunci Admin API dengan “scope” (cakupan) `read:spend_limits` (untuk endpoint `GET`) atau cakupan `write:spend_limits` (untuk endpoint `POST` dan `DELETE`). Lihat [Membuat kunci Admin API](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization) untuk mengetahui di mana pemilik utama Anda membuatnya dan cakupan mana yang harus dipilih. Sertakan kunci tersebut di header `x-api-key` pada setiap permintaan, bersama dengan header [`anthropic-version`](https://platform.claude.com/docs/id/api/versioning).
</Check>

<Note>
  Spend Limits API hanya tersedia untuk organisasi Claude Enterprise. API ini tidak tersedia untuk organisasi Claude Platform (Claude Console).
</Note>

## Ikhtisar

API ini menyediakan delapan endpoint pada dua sumber daya:

| Sumber daya                               | Endpoint                                                                                                                                                                                                                                                             | Digunakan untuk                                                                                                                                                      |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Batas pengeluaran**                     | `GET /v1/organizations/spend_limits/effective`<br />`GET /v1/organizations/spend_limits/{spend_limit_id}`<br />`POST /v1/organizations/spend_limits`<br />`DELETE /v1/organizations/spend_limits/{spend_limit_id}`                                                   | Membaca batas pengeluaran efektif setiap anggota dan pengeluaran periode berjalan; menetapkan atau menghapus override per pengguna.                                  |
| **Permintaan kenaikan batas pengeluaran** | `GET /v1/organizations/spend_limit_increase_requests`<br />`GET /v1/organizations/spend_limit_increase_requests/{id}`<br />`POST /v1/organizations/spend_limit_increase_requests/{id}/approve`<br />`POST /v1/organizations/spend_limit_increase_requests/{id}/deny` | Mendaftar permintaan anggota untuk batas pengeluaran yang lebih tinggi, beserta konteks yang diperlukan untuk memutuskan; menyetujui atau menolak setiap permintaan. |

Gunakan endpoint **spend limits** untuk menjawab “batas pengeluaran apa yang berlaku untuk setiap anggota, dari mana asalnya, dan seberapa dekat mereka dengan batas tersebut?” serta untuk menetapkan override per pengguna. Gunakan endpoint **spend limit increase requests** untuk memproses antrean permintaan yang diajukan anggota.

## Prasyarat

* Organisasi Anda harus menggunakan paket Claude Enterprise.
* Kredit penggunaan harus diaktifkan untuk organisasi Anda. Primary owner Anda dapat mengaktifkannya di pengaturan penagihan claude.ai.

SDK menyediakan endpoint ini di bawah `client.beta.organization.spend_limits` (typescript: `client.beta.organization.spendLimits`; csharp, go: `client.Beta.Organization.SpendLimits`; java: `client.beta().organization().spendLimits()`; php: `$client->beta->organization->spendLimits`), dan CLI `ant` di bawah `ant beta:organization:spend-limits`. Keduanya mengirimkan header `anthropic-version` untuk Anda. Contoh-contoh membaca kunci Admin API dari variabel lingkungan `ANTHROPIC_API_KEY`. SDK dan CLI mengambil halaman berikutnya untuk Anda saat Anda menelusuri hasil, sehingga `limit` menetapkan ukuran halaman, bukan total (lihat [Paginasi](https://platform.claude.com/docs/id/manage-claude/spend-limits-api#pagination)).

## Mulai cepat

Daftarkan batas pengeluaran bulanan efektif dan pengeluaran periode berjalan setiap anggota:

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/spend_limits/effective?limit=20" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:spend-limits:effective list --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  effective_limits = client.beta.organization.spend_limits.effective.list(limit=20)

  for effective_limit in effective_limits:
      scope = effective_limit.scope
      if scope.type == "user":
          amount = effective_limit.amount or "unlimited"
          print(f"{scope.user_id}: {effective_limit.period_to_date_spend} of {amount}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const effectiveLimits = await client.beta.organization.spendLimits.effective.list({
    limit: 20
  });

  for await (const effectiveLimit of effectiveLimits) {
    const { scope } = effectiveLimit;
    if (scope.type === "user") {
      const amount = effectiveLimit.amount ?? "unlimited";
      console.log(`${scope.user_id}: ${effectiveLimit.period_to_date_spend} of ${amount}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.SpendLimits.Effective.List(
      new() { Limit = 20 }
  );

  await foreach (var effectiveLimit in page.Paginate())
  {
      if (effectiveLimit.Scope.TryPickBetaSpendLimitUser(out var userScope))
      {
          var amount = effectiveLimit.Amount ?? "unlimited";
          Console.WriteLine($"{userScope.UserID}: {effectiveLimit.PeriodToDateSpend} of {amount}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  effectiveLimits := client.Beta.Organization.SpendLimits.Effective.ListAutoPaging(context.Background(), anthropic.BetaOrganizationSpendLimitEffectiveListParams{
  	Limit: anthropic.Int(20),
  })

  for effectiveLimits.Next() {
  	effectiveLimit := effectiveLimits.Current()
  	if userScope, ok := effectiveLimit.Scope.AsAny().(anthropic.BetaSpendLimitUserScope); ok {
  		amount := effectiveLimit.Amount
  		if !effectiveLimit.JSON.Amount.Valid() {
  			amount = "unlimited"
  		}
  		fmt.Printf("%s: %s of %s\n", userScope.UserID, effectiveLimit.PeriodToDateSpend, amount)
  	}
  }
  if err := effectiveLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.spendlimits.effective.EffectiveListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = EffectiveListParams.builder()
          .limit(20)
          .build();
      var effectiveLimits = client.beta().organization().spendLimits().effective().list(params);

      for (var effectiveLimit : effectiveLimits.autoPager()) {
          var amount = effectiveLimit.amount().orElse("unlimited");
          effectiveLimit.scope().user().ifPresent(userScope ->
              IO.println(userScope.userId() + ": " + effectiveLimit.periodToDateSpend() + " of " + amount)
          );
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\SpendLimits\SpendLimitUserScope;
  // ...

  $client = new Client();

  $effectiveLimits = $client->beta->organization->spendLimits->effective->list(limit: 20);

  foreach ($effectiveLimits->pagingEachItem() as $effectiveLimit) {
      $scope = $effectiveLimit->scope;
      if ($scope instanceof SpendLimitUserScope) {
          $amount = $effectiveLimit->amount ?? 'unlimited';
          echo "{$scope->userID}: {$effectiveLimit->periodToDateSpend} of {$amount}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.spend_limits.effective.list(limit: 20)

  page.auto_paging_each do |effective_limit|
    scope = effective_limit.scope
    if scope.is_a?(Anthropic::Models::Beta::Organization::BetaSpendLimitUserScope)
      amount = effective_limit.amount || "unlimited"
      puts "#{scope.user_id}: #{effective_limit.period_to_date_spend} of #{amount}"
    end
  end
  ```
</CodeGroup>

## Konsep utama

### Hierarki batas pengeluaran

Sebuah **effective spend limit** (batas pengeluaran efektif) berlaku pada pengeluaran setiap anggota, yang ditentukan dari hierarki tingkat cakupan. Ketika seorang anggota tidak memiliki override per pengguna, mereka mewarisi batas pengeluaran yang dikonfigurasi untuk grup mereka (jika organisasi Anda menggunakan batas berbasis grup), seat tier mereka, atau default seluruh organisasi. Batas pengeluaran grup adalah default per anggota: setiap anggota yang mewarisinya dibatasi berdasarkan pengeluaran mereka sendiri, bukan anggaran grup yang digabungkan.

Membaca `GET /v1/organizations/spend_limits/effective` mengembalikan setiap anggota saat ini beserta batas pengeluaran efektif mereka yang telah ditentukan, dari mana batas tersebut ditentukan (`source`), dan pengeluaran periode berjalan mereka. Menetapkan override per pengguna dengan `POST /v1/organizations/spend_limits` mengunci seorang anggota pada batas pengeluaran tertentu terlepas dari apa yang seharusnya mereka warisi. Menghapus override mengembalikan mereka ke batas pengeluaran yang diwarisi (atau membiarkan mereka tanpa batas jika tidak ada).

Field `source` pada baris setiap anggota memberi tahu Anda dari tingkat mana batas pengeluaran mereka ditentukan: `user` (override per pengguna), `seat_tier`, `rbac_group`, atau `organization`. Perlakukan tipe cakupan sebagai himpunan terbuka; lewati nilai yang tidak dikenal alih-alih gagal.

### Periode

`period` adalah jendela berulang di mana batas pengeluaran diberlakukan dan pengeluaran direset. Sebuah batas pengeluaran diidentifikasi oleh pasangan `(scope, period)`-nya. Saat ini `monthly` adalah satu-satunya periode yang didukung; pengeluaran bulanan direset pada 00:00 UTC di tanggal satu setiap bulan kalender. Perlakukan `period` sebagai himpunan terbuka.

### Jumlah dan mata uang

Semua nilai moneter berupa string dalam **satuan minor mata uang penagihan organisasi** (sen, untuk USD). Misalnya, `"50000"` merepresentasikan 500,00 USD. Parse sebagai desimal dan bagi dengan 100 untuk menampilkan dolar; hindari floating-point biner untuk nilai besar.

`amount` bersifat **nullable**. Pada baris efektif seorang anggota, `null` berarti **tanpa batas** (tidak ada batas pengeluaran) dan `"0"` berarti anggota tidak dapat menggunakan Claude melebihi penggunaan yang termasuk dalam paket mereka. Pada baris batas pengeluaran yang dikonfigurasi (seperti yang dikembalikan oleh `GET /v1/organizations/spend_limits/{id}`), `null` hanya berarti tidak ada batas pengeluaran numerik yang ditetapkan; baca baris efektif anggota untuk membedakan tanpa batas dari hanya-penggunaan-termasuk.

`period_to_date_spend` adalah pengeluaran anggota yang terakumulasi sejak awal `period` saat ini, dalam format satuan minor yang sama; nilainya dapat mencakup bagian pecahan (misalnya, `"41280.125"`). Nilainya dapat terbaca sebagai `"0"` jika pembacaan pengeluaran sementara tidak tersedia; perlakukan sebagai informasional, bukan transaksional.

### Siklus hidup permintaan kenaikan

Sebuah **spend limit increase request** (permintaan kenaikan batas pengeluaran) dibuat ketika seorang anggota mengklik **Request more usage** di claude.ai. Permintaan tidak dibuat melalui API ini. `status` sebuah permintaan adalah salah satu dari:

| Status     | Arti                                                                                                                                                                                                                                                                    |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pending`  | Menunggu tindakan admin. Permintaan biasanya membawa `spend_summary` langsung sehingga Anda dapat melihat batas pengeluaran efektif anggota saat ini dan pengeluaran periode berjalan saat memutuskan; `spend_summary` dapat bernilai `null` jika tidak dapat dihitung. |
| `approved` | Permintaan diselesaikan dengan persetujuan: baik admin menyetujuinya secara eksplisit, tindakan admin lain menaikkan batas pengeluaran anggota, atau dukungan Anthropic menaikkan batas pengeluaran atas nama organisasi. `spend_summary` bernilai `null`.              |
| `denied`   | Admin menolak. `spend_summary` bernilai `null`. Anggota dapat langsung mengirim permintaan baru; hanya permintaan `pending` yang memblokir permintaan baru. Admin tetap dapat menaikkan batas pengeluaran anggota secara langsung kapan saja.                           |

Baik `approved` maupun `denied` bersifat terminal. Seorang anggota memiliki paling banyak satu permintaan `pending` pada satu waktu.

Menyetujui dengan `POST /v1/organizations/spend_limit_increase_requests/{id}/approve` menulis baris batas pengeluaran per pengguna yang sama dengan yang ditulis oleh `POST /v1/organizations/spend_limits`. Menetapkan batas pengeluaran secara langsung **tidak** mentransisikan permintaan yang pending; gunakan endpoint approve untuk menyelesaikan permintaan.

Secara default, Anthropic mengirim email kepada anggota ketika permintaan mereka disetujui atau ditolak. Sertakan `suppress_notification: true` pada approve atau deny untuk menekan email tersebut (misalnya, ketika sistem Anda sendiri yang memberi tahu anggota).

## Pembuatan versi

Kirim header `anthropic-version` pada setiap permintaan; lihat [Versi API](https://platform.claude.com/docs/id/api/versioning) untuk versi yang tersedia.

## Pembatasan laju

Kedelapan endpoint berbagi satu “rate limit” (batas laju) per organisasi sebesar **60 permintaan per menit**. Permintaan yang melebihi batas mengembalikan **429 Too Many Requests**.

## Paginasi

`GET /v1/organizations/spend_limits/effective` dan `GET /v1/organizations/spend_limit_increase_requests` dipaginasi dengan **cursor opaque**. Permintaan pertama mengembalikan hingga `limit` baris ditambah cursor `next_page`; teruskan cursor tersebut tanpa perubahan sebagai parameter `page` pada permintaan berikutnya, dan ulangi hingga `next_page` bernilai `null`.

**Jangan mengubah parameter query di tengah urutan.** Cursor terikat pada filter yang menerbitkannya. Jika Anda mengubah `user_ids[]`, `period[]`, `status[]`, atau `actor_ids[]` dan meneruskan cursor lama, Anda akan mendapatkan 400 dengan *“cursor does not match current query parameters”*. Mulailah urutan baru dari halaman pertama.

## Serialisasi parameter list

Parameter list menggunakan notasi kurung siku: ulangi nama parameter dengan `[]` untuk setiap nilai.

```text wrap
user_ids[]=user_01AbCdEfGh&user_ids[]=user_01JkLmNoPq
```

## Respons error

Respons error mengikuti bentuk standar yang didokumentasikan di [Errors](https://platform.claude.com/docs/id/api/errors). Kutip `request_id` dari body respons saat menghubungi dukungan.

## Batas pengeluaran

### Mendaftar batas pengeluaran efektif setiap anggota

`GET /v1/organizations/spend_limits/effective` mengembalikan satu baris per anggota saat ini, yang mencerminkan batas pengeluaran efektif setiap anggota, `source`-nya dalam hierarki cakupan, dan `period_to_date_spend` mereka. Memerlukan cakupan `read:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [List effective spend limits](https://platform.claude.com/docs/id/api/beta/organization/spend_limits/effective/list) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/spend_limits/effective?limit=20" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:spend-limits:effective list --limit 20
  ```

  ```python Python
  client = anthropic.Anthropic()

  effective_limits = client.beta.organization.spend_limits.effective.list(limit=20)

  for effective_limit in effective_limits:
      scope = effective_limit.scope
      if scope.type == "user":
          amount = effective_limit.amount or "unlimited"
          print(f"{scope.user_id}: {effective_limit.period_to_date_spend} of {amount}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const effectiveLimits = await client.beta.organization.spendLimits.effective.list({
    limit: 20
  });

  for await (const effectiveLimit of effectiveLimits) {
    const { scope } = effectiveLimit;
    if (scope.type === "user") {
      const amount = effectiveLimit.amount ?? "unlimited";
      console.log(`${scope.user_id}: ${effectiveLimit.period_to_date_spend} of ${amount}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var page = await client.Beta.Organization.SpendLimits.Effective.List(
      new() { Limit = 20 }
  );

  await foreach (var effectiveLimit in page.Paginate())
  {
      if (effectiveLimit.Scope.TryPickBetaSpendLimitUser(out var userScope))
      {
          var amount = effectiveLimit.Amount ?? "unlimited";
          Console.WriteLine($"{userScope.UserID}: {effectiveLimit.PeriodToDateSpend} of {amount}");
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  effectiveLimits := client.Beta.Organization.SpendLimits.Effective.ListAutoPaging(context.Background(), anthropic.BetaOrganizationSpendLimitEffectiveListParams{
  	Limit: anthropic.Int(20),
  })

  for effectiveLimits.Next() {
  	effectiveLimit := effectiveLimits.Current()
  	if userScope, ok := effectiveLimit.Scope.AsAny().(anthropic.BetaSpendLimitUserScope); ok {
  		amount := effectiveLimit.Amount
  		if !effectiveLimit.JSON.Amount.Valid() {
  			amount = "unlimited"
  		}
  		fmt.Printf("%s: %s of %s\n", userScope.UserID, effectiveLimit.PeriodToDateSpend, amount)
  	}
  }
  if err := effectiveLimits.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.spendlimits.effective.EffectiveListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = EffectiveListParams.builder()
          .limit(20)
          .build();
      var effectiveLimits = client.beta().organization().spendLimits().effective().list(params);

      for (var effectiveLimit : effectiveLimits.autoPager()) {
          var amount = effectiveLimit.amount().orElse("unlimited");
          effectiveLimit.scope().user().ifPresent(userScope ->
              IO.println(userScope.userId() + ": " + effectiveLimit.periodToDateSpend() + " of " + amount)
          );
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\SpendLimits\SpendLimitUserScope;
  // ...

  $client = new Client();

  $effectiveLimits = $client->beta->organization->spendLimits->effective->list(limit: 20);

  foreach ($effectiveLimits->pagingEachItem() as $effectiveLimit) {
      $scope = $effectiveLimit->scope;
      if ($scope instanceof SpendLimitUserScope) {
          $amount = $effectiveLimit->amount ?? 'unlimited';
          echo "{$scope->userID}: {$effectiveLimit->periodToDateSpend} of {$amount}\n";
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.spend_limits.effective.list(limit: 20)

  page.auto_paging_each do |effective_limit|
    scope = effective_limit.scope
    if scope.is_a?(Anthropic::Models::Beta::Organization::BetaSpendLimitUserScope)
      amount = effective_limit.amount || "unlimited"
      puts "#{scope.user_id}: #{effective_limit.period_to_date_spend} of #{amount}"
    end
  end
  ```
</CodeGroup>

```json
{
  "data": [
    {
      "scope": { "type": "user", "user_id": "user_01AbCdEfGh" },
      "actor": {
        "type": "user_actor",
        "user_id": "user_01AbCdEfGh",
        "name": "Jane Smith",
        "email_address": "jane@example.com",
        "deleted": false
      },
      "amount": "50000",
      "currency": "USD",
      "period": "monthly",
      "source": { "type": "seat_tier", "seat_tier": "enterprise_standard" },
      "spend_limit_id": "spl_01XyZaBcDeFgHiJkLmNoPq",
      "period_to_date_spend": "31402.5"
    }
  ],
  "next_page": "page_..."
}
```

### Mendapatkan satu batas pengeluaran

`GET /v1/organizations/spend_limits/{spend_limit_id}` mengembalikan satu batas pengeluaran yang dikonfigurasi berdasarkan ID. Gunakan untuk memeriksa baris yang dirujuk oleh field `spend_limit_id`. Memerlukan cakupan `read:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Retrieve a spend limit](https://platform.claude.com/docs/id/api/beta/organization/spend_limits/retrieve) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/spend_limits/spl_01AbCdEfGhIjKlMnOpQrSt" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:spend-limits retrieve \
    --spend-limit-id spl_01AbCdEfGhIjKlMnOpQrSt
  ```

  ```python Python
  client = anthropic.Anthropic()

  spend_limit = client.beta.organization.spend_limits.retrieve(
      "spl_01AbCdEfGhIjKlMnOpQrSt"
  )

  amount = spend_limit.amount or "none"
  print(f"id: {spend_limit.id}")
  print(f"amount: {amount}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const spendLimit = await client.beta.organization.spendLimits.retrieve(
    "spl_01AbCdEfGhIjKlMnOpQrSt"
  );

  const amount = spendLimit.amount ?? "none";
  console.log(`id: ${spendLimit.id}`);
  console.log(`amount: ${amount}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var spendLimit = await client.Beta.Organization.SpendLimits.Retrieve(
      "spl_01AbCdEfGhIjKlMnOpQrSt"
  );

  var amount = spendLimit.Amount ?? "none";
  Console.WriteLine($"id: {spendLimit.ID}");
  Console.WriteLine($"amount: {amount}");
  ```

  ```go Go
  client := anthropic.NewClient()

  spendLimit, err := client.Beta.Organization.SpendLimits.Get(context.Background(), "spl_01AbCdEfGhIjKlMnOpQrSt")
  if err != nil {
  	log.Fatal(err)
  }

  amount := spendLimit.Amount
  if !spendLimit.JSON.Amount.Valid() {
  	amount = "none"
  }

  fmt.Printf("id: %s\n", spendLimit.ID)
  fmt.Printf("amount: %s\n", amount)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var spendLimit = client.beta().organization().spendLimits()
      .retrieve("spl_01AbCdEfGhIjKlMnOpQrSt");

  var amount = spendLimit.amount().orElse("none");
  IO.println("id: " + spendLimit.id());
  IO.println("amount: " + amount);
  ```

  ```php PHP
  $client = new Client();

  $spendLimit = $client->beta->organization->spendLimits->retrieve('spl_01AbCdEfGhIjKlMnOpQrSt');

  $amount = $spendLimit->amount ?? 'none';
  echo "id: {$spendLimit->id}\n";
  echo "amount: {$amount}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  spend_limit = client.beta.organization.spend_limits.retrieve("spl_01AbCdEfGhIjKlMnOpQrSt")

  amount = spend_limit.amount || "none"
  puts "id: #{spend_limit.id}"
  puts "amount: #{amount}"
  ```
</CodeGroup>

### Menetapkan override per pengguna

`POST /v1/organizations/spend_limits` menetapkan override batas pengeluaran per pengguna. Ini adalah upsert dengan kunci `(scope, period)`: menetapkan batas untuk pengguna dan periode yang sudah memilikinya akan menimpanya di tempat. Endpoint ini hanya menerima `scope.type: "user"`; default tingkat seat-tier, grup, dan organisasi dikonfigurasi di pengaturan claude.ai. Memerlukan cakupan `write:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Create a spend limit](https://platform.claude.com/docs/id/api/beta/organization/spend_limits/set) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/spend_limits" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{"scope": {"type": "user", "user_id": "user_01AbCdEfGh"}, "amount": "75000"}'
  ```

  ```bash CLI
  ant beta:organization:spend-limits set \
    --scope '{type: user, user_id: user_01AbCdEfGh}' \
    --amount 75000
  ```

  ```python Python
  client = anthropic.Anthropic()

  spend_limit = client.beta.organization.spend_limits.set(
      scope={"type": "user", "user_id": "user_01AbCdEfGh"}, amount="75000"
  )

  print(f"id: {spend_limit.id}")
  print(f"amount: {spend_limit.amount}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const spendLimit = await client.beta.organization.spendLimits.set({
    scope: { type: "user", user_id: "user_01AbCdEfGh" },
    amount: "75000"
  });

  console.log(`id: ${spendLimit.id}`);
  console.log(`amount: ${spendLimit.amount}`);
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.SpendLimits;

  AnthropicClient client = new();

  var spendLimit = await client.Beta.Organization.SpendLimits.Set(
      new()
      {
          Scope = new BetaSpendLimitUserScope("user_01AbCdEfGh"),
          Amount = "75000",
      }
  );

  Console.WriteLine($"id: {spendLimit.ID}");
  Console.WriteLine($"amount: {spendLimit.Amount}");
  ```

  ```go Go
  client := anthropic.NewClient()

  spendLimit, err := client.Beta.Organization.SpendLimits.Set(context.Background(), anthropic.BetaOrganizationSpendLimitSetParams{
  	Scope: anthropic.BetaOrganizationSpendLimitSetParamsScopeUnion{
  		OfUser: &anthropic.BetaSpendLimitUserScopeParam{UserID: "user_01AbCdEfGh"},
  	},
  	Amount: anthropic.String("75000"),
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", spendLimit.ID)
  fmt.Printf("amount: %s\n", spendLimit.Amount)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.spendlimits.SpendLimitSetParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = SpendLimitSetParams.builder()
          .userScope("user_01AbCdEfGh")
          .amount("75000")
          .build();
      var spendLimit = client.beta().organization().spendLimits().set(params);

      IO.println("id: " + spendLimit.id());
      IO.println("amount: " + spendLimit.amount().orElseThrow());
  }
  ```

  ```php PHP
  use Anthropic\Beta\Organization\SpendLimits\SpendLimitUserScope;
  // ...

  $client = new Client();

  $spendLimit = $client->beta->organization->spendLimits->set(
      scope: SpendLimitUserScope::with(userID: 'user_01AbCdEfGh'),
      amount: '75000',
  );

  echo "id: {$spendLimit->id}\n";
  echo "amount: {$spendLimit->amount}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  spend_limit = client.beta.organization.spend_limits.set(
    scope: { type: :user, user_id: "user_01AbCdEfGh" },
    amount: "75000"
  )

  puts "id: #{spend_limit.id}"
  puts "amount: #{spend_limit.amount}"
  ```
</CodeGroup>

```json
{
  "type": "spend_limit",
  "id": "spl_01RsTuVwXyZaBcDeFgHiJk",
  "created_at": "2026-05-11T10:02:44Z",
  "updated_at": "2026-05-11T10:02:44Z",
  "scope": { "type": "user", "user_id": "user_01AbCdEfGh" },
  "amount": "75000",
  "currency": "USD",
  "period": "monthly"
}
```

### Menghapus override per pengguna

`DELETE /v1/organizations/spend_limits/{spend_limit_id}` menghapus override per pengguna, setelah itu anggota kembali ke default seat-tier, grup, atau organisasi yang diwarisi. Baris tingkat seat-tier, grup, dan organisasi tidak dapat dihapus melalui endpoint ini. Memerlukan cakupan `write:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Delete a spend limit](https://platform.claude.com/docs/id/api/beta/organization/spend_limits/delete) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X DELETE "https://api.anthropic.com/v1/organizations/spend_limits/spl_01RsTuVwXyZaBcDeFgHiJk" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:spend-limits delete \
    --spend-limit-id spl_01RsTuVwXyZaBcDeFgHiJk
  ```

  ```python Python
  client = anthropic.Anthropic()

  deleted_spend_limit = client.beta.organization.spend_limits.delete(
      "spl_01RsTuVwXyZaBcDeFgHiJk"
  )

  print(f"id: {deleted_spend_limit.id}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const deletedSpendLimit = await client.beta.organization.spendLimits.delete(
    "spl_01RsTuVwXyZaBcDeFgHiJk"
  );

  console.log(`id: ${deletedSpendLimit.id}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var deletedSpendLimit = await client.Beta.Organization.SpendLimits.Delete(
      "spl_01RsTuVwXyZaBcDeFgHiJk"
  );

  Console.WriteLine($"id: {deletedSpendLimit.ID}");
  ```

  ```go Go
  client := anthropic.NewClient()

  deletedSpendLimit, err := client.Beta.Organization.SpendLimits.Delete(context.Background(), "spl_01RsTuVwXyZaBcDeFgHiJk")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", deletedSpendLimit.ID)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var deletedSpendLimit = client.beta().organization().spendLimits()
      .delete("spl_01RsTuVwXyZaBcDeFgHiJk");

  IO.println("id: " + deletedSpendLimit.id());
  ```

  ```php PHP
  $client = new Client();

  $deletedSpendLimit = $client->beta->organization->spendLimits->delete('spl_01RsTuVwXyZaBcDeFgHiJk');

  echo "id: {$deletedSpendLimit->id}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  deleted_spend_limit = client.beta.organization.spend_limits.delete("spl_01RsTuVwXyZaBcDeFgHiJk")

  puts "id: #{deleted_spend_limit.id}"
  ```
</CodeGroup>

## Permintaan kenaikan batas pengeluaran

### Mendaftar permintaan kenaikan

`GET /v1/organizations/spend_limit_increase_requests` mendaftar permintaan, yang terbaru lebih dulu. Filter berdasarkan `status[]` (`pending`, `approved`, `denied`) dan `actor_ids[]`. Daftar ini mengecualikan permintaan yang pemohonnya bukan lagi anggota organisasi. Memerlukan cakupan `read:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [List spend limit increase requests](https://platform.claude.com/docs/id/api/beta/organization/spend_limits/increase_requests/list) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -g "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests?status[]=pending&limit=50" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:spend-limits:increase-requests list \
    --status pending \
    --limit 50
  ```

  ```python Python
  client = anthropic.Anthropic()

  increase_requests = client.beta.organization.spend_limits.increase_requests.list(
      status=["pending"], limit=50
  )

  for increase_request in increase_requests:
      print(f"{increase_request.id}: {increase_request.status}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const increaseRequests = await client.beta.organization.spendLimits.increaseRequests.list({
    status: ["pending"],
    limit: 50
  });

  for await (const increaseRequest of increaseRequests) {
    console.log(`${increaseRequest.id}: ${increaseRequest.status}`);
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Organization.SpendLimits.IncreaseRequests;

  AnthropicClient client = new();

  var page = await client.Beta.Organization.SpendLimits.IncreaseRequests.List(
      new() { Status = [BetaSpendLimitIncreaseRequestStatus.Pending], Limit = 50 }
  );

  await foreach (var increaseRequest in page.Paginate())
  {
      Console.WriteLine($"{increaseRequest.ID}: {increaseRequest.Status.Raw()}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  increaseRequests := client.Beta.Organization.SpendLimits.IncreaseRequests.ListAutoPaging(context.Background(), anthropic.BetaOrganizationSpendLimitIncreaseRequestListParams{
  	Status: []anthropic.BetaSpendLimitIncreaseRequestStatus{anthropic.BetaSpendLimitIncreaseRequestStatusPending},
  	Limit:  anthropic.Int(50),
  })

  for increaseRequests.Next() {
  	increaseRequest := increaseRequests.Current()
  	fmt.Printf("%s: %s\n", increaseRequest.ID, increaseRequest.Status)
  }
  if err := increaseRequests.Err(); err != nil {
  	log.Fatal(err)
  }
  ```

  ```java Java
  import com.anthropic.models.beta.organization.spendlimits.increaserequests.BetaSpendLimitIncreaseRequestStatus;
  import com.anthropic.models.beta.organization.spendlimits.increaserequests.IncreaseRequestListParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = IncreaseRequestListParams.builder()
          .addStatus(BetaSpendLimitIncreaseRequestStatus.PENDING)
          .limit(50)
          .build();
      var increaseRequests = client.beta().organization().spendLimits().increaseRequests().list(params);

      for (var increaseRequest : increaseRequests.autoPager()) {
          IO.println(increaseRequest.id() + ": " + increaseRequest.status().asString());
      }
  }
  ```

  ```php PHP
  $client = new Client();

  $increaseRequests = $client->beta->organization->spendLimits->increaseRequests->list(
      status: ['pending'],
      limit: 50,
  );

  foreach ($increaseRequests->pagingEachItem() as $increaseRequest) {
      echo "{$increaseRequest->id}: {$increaseRequest->status}\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  page = client.beta.organization.spend_limits.increase_requests.list(status: [:pending], limit: 50)

  page.auto_paging_each do |increase_request|
    puts "#{increase_request.id}: #{increase_request.status}"
  end
  ```
</CodeGroup>

Setiap permintaan pending membawa `spend_summary` langsung yang menunjukkan batas pengeluaran efektif pemohon saat ini dan pengeluaran periode berjalan, cukup untuk memutuskan tanpa pencarian terpisah.

### Mendapatkan satu permintaan kenaikan

`GET /v1/organizations/spend_limit_increase_requests/{id}` mengembalikan satu permintaan berdasarkan ID. Memerlukan cakupan `read:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Retrieve a spend limit increase request](https://platform.claude.com/docs/id/api/beta/organization/spend_limits/increase_requests/retrieve) di referensi API.

<CodeGroup>
  ```bash cURL
  curl "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01"
  ```

  ```bash CLI
  ant beta:organization:spend-limits:increase-requests retrieve \
    --spend-limit-increase-request-id slir_01AbCdEfGhIjKlMnOpQrSt
  ```

  ```python Python
  client = anthropic.Anthropic()

  increase_request = client.beta.organization.spend_limits.increase_requests.retrieve(
      "slir_01AbCdEfGhIjKlMnOpQrSt"
  )

  print(f"id: {increase_request.id}")
  print(f"status: {increase_request.status}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const increaseRequest = await client.beta.organization.spendLimits.increaseRequests.retrieve(
    "slir_01AbCdEfGhIjKlMnOpQrSt"
  );

  console.log(`id: ${increaseRequest.id}`);
  console.log(`status: ${increaseRequest.status}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var increaseRequest = await client.Beta.Organization.SpendLimits.IncreaseRequests.Retrieve(
      "slir_01AbCdEfGhIjKlMnOpQrSt"
  );

  Console.WriteLine($"id: {increaseRequest.ID}");
  Console.WriteLine($"status: {increaseRequest.Status.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  increaseRequest, err := client.Beta.Organization.SpendLimits.IncreaseRequests.Get(context.Background(), "slir_01AbCdEfGhIjKlMnOpQrSt")
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", increaseRequest.ID)
  fmt.Printf("status: %s\n", increaseRequest.Status)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  var increaseRequest = client.beta().organization().spendLimits().increaseRequests()
      .retrieve("slir_01AbCdEfGhIjKlMnOpQrSt");

  IO.println("id: " + increaseRequest.id());
  IO.println("status: " + increaseRequest.status().asString());
  ```

  ```php PHP
  $client = new Client();

  $increaseRequest = $client->beta->organization->spendLimits->increaseRequests->retrieve(
      'slir_01AbCdEfGhIjKlMnOpQrSt',
  );

  echo "id: {$increaseRequest->id}\n";
  echo "status: {$increaseRequest->status}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  increase_request = client.beta.organization.spend_limits.increase_requests.retrieve(
    "slir_01AbCdEfGhIjKlMnOpQrSt"
  )

  puts "id: #{increase_request.id}"
  puts "status: #{increase_request.status}"
  ```
</CodeGroup>

### Menyetujui permintaan kenaikan

`POST /v1/organizations/spend_limit_increase_requests/{id}/approve` menyetujui permintaan pending: endpoint ini menulis batas pengeluaran per pengguna pada `amount` yang diberikan admin untuk pemohon dan mentransisikan permintaan ke `approved`. Permintaan tidak membawa jumlah yang diminta; Anda memberikan batas pengeluaran baru saat persetujuan. Memerlukan cakupan `write:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Approve a spend limit increase request](https://platform.claude.com/docs/id/api/beta/organization/spend_limits/increase_requests/approve) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt/approve" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{"amount": "75000", "suppress_notification": true}'
  ```

  ```bash CLI
  ant beta:organization:spend-limits:increase-requests approve \
    --spend-limit-increase-request-id slir_01AbCdEfGhIjKlMnOpQrSt \
    --amount 75000 \
    --suppress-notification
  ```

  ```python Python
  client = anthropic.Anthropic()

  increase_request = client.beta.organization.spend_limits.increase_requests.approve(
      "slir_01AbCdEfGhIjKlMnOpQrSt", amount="75000", suppress_notification=True
  )

  print(f"id: {increase_request.id}")
  print(f"status: {increase_request.status}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const increaseRequest = await client.beta.organization.spendLimits.increaseRequests.approve(
    "slir_01AbCdEfGhIjKlMnOpQrSt",
    {
      amount: "75000",
      suppress_notification: true
    }
  );

  console.log(`id: ${increaseRequest.id}`);
  console.log(`status: ${increaseRequest.status}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var increaseRequest = await client.Beta.Organization.SpendLimits.IncreaseRequests.Approve(
      "slir_01AbCdEfGhIjKlMnOpQrSt",
      new() { Amount = "75000", SuppressNotification = true }
  );

  Console.WriteLine($"id: {increaseRequest.ID}");
  Console.WriteLine($"status: {increaseRequest.Status.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  increaseRequest, err := client.Beta.Organization.SpendLimits.IncreaseRequests.Approve(
  	context.Background(),
  	"slir_01AbCdEfGhIjKlMnOpQrSt",
  	anthropic.BetaOrganizationSpendLimitIncreaseRequestApproveParams{
  		Amount:               "75000",
  		SuppressNotification: anthropic.Bool(true),
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", increaseRequest.ID)
  fmt.Printf("status: %s\n", increaseRequest.Status)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.spendlimits.increaserequests.IncreaseRequestApproveParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = IncreaseRequestApproveParams.builder()
          .amount("75000")
          .suppressNotification(true)
          .build();
      var increaseRequest = client.beta().organization().spendLimits().increaseRequests()
          .approve("slir_01AbCdEfGhIjKlMnOpQrSt", params);

      IO.println("id: " + increaseRequest.id());
      IO.println("status: " + increaseRequest.status().asString());
  }
  ```

  ```php PHP
  $client = new Client();

  $increaseRequest = $client->beta->organization->spendLimits->increaseRequests->approve(
      'slir_01AbCdEfGhIjKlMnOpQrSt',
      amount: '75000',
      suppressNotification: true,
  );

  echo "id: {$increaseRequest->id}\n";
  echo "status: {$increaseRequest->status}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  increase_request = client.beta.organization.spend_limits.increase_requests.approve(
    "slir_01AbCdEfGhIjKlMnOpQrSt",
    amount: "75000",
    suppress_notification: true
  )

  puts "id: #{increase_request.id}"
  puts "status: #{increase_request.status}"
  ```
</CodeGroup>

### Menolak permintaan kenaikan

`POST /v1/organizations/spend_limit_increase_requests/{id}/deny` menolak permintaan pending. Idempoten pada `denied`: menolak permintaan yang sudah ditolak mengembalikan 200 dengan sumber daya yang ada. Endpoint ini menolak upaya untuk menolak permintaan yang sudah disetujui sehingga otomatisasi dapat membedakan percobaan ulang dari keputusan yang bertentangan. Memerlukan cakupan `write:spend_limits`.

Untuk detail parameter lengkap dan skema respons, lihat [Deny a spend limit increase request](https://platform.claude.com/docs/id/api/beta/organization/spend_limits/increase_requests/deny) di referensi API.

<CodeGroup>
  ```bash cURL
  curl -X POST "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt/deny" \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{"suppress_notification": true}'
  ```

  ```bash CLI
  ant beta:organization:spend-limits:increase-requests deny \
    --spend-limit-increase-request-id slir_01AbCdEfGhIjKlMnOpQrSt \
    --suppress-notification
  ```

  ```python Python
  client = anthropic.Anthropic()

  increase_request = client.beta.organization.spend_limits.increase_requests.deny(
      "slir_01AbCdEfGhIjKlMnOpQrSt", suppress_notification=True
  )

  print(f"id: {increase_request.id}")
  print(f"status: {increase_request.status}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const increaseRequest = await client.beta.organization.spendLimits.increaseRequests.deny(
    "slir_01AbCdEfGhIjKlMnOpQrSt",
    {
      suppress_notification: true
    }
  );

  console.log(`id: ${increaseRequest.id}`);
  console.log(`status: ${increaseRequest.status}`);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var increaseRequest = await client.Beta.Organization.SpendLimits.IncreaseRequests.Deny(
      "slir_01AbCdEfGhIjKlMnOpQrSt",
      new() { SuppressNotification = true }
  );

  Console.WriteLine($"id: {increaseRequest.ID}");
  Console.WriteLine($"status: {increaseRequest.Status.Raw()}");
  ```

  ```go Go
  client := anthropic.NewClient()

  increaseRequest, err := client.Beta.Organization.SpendLimits.IncreaseRequests.Deny(
  	context.Background(),
  	"slir_01AbCdEfGhIjKlMnOpQrSt",
  	anthropic.BetaOrganizationSpendLimitIncreaseRequestDenyParams{
  		SuppressNotification: anthropic.Bool(true),
  	},
  )
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("id: %s\n", increaseRequest.ID)
  fmt.Printf("status: %s\n", increaseRequest.Status)
  ```

  ```java Java
  import com.anthropic.models.beta.organization.spendlimits.increaserequests.IncreaseRequestDenyParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = IncreaseRequestDenyParams.builder()
          .suppressNotification(true)
          .build();
      var increaseRequest = client.beta().organization().spendLimits().increaseRequests()
          .deny("slir_01AbCdEfGhIjKlMnOpQrSt", params);

      IO.println("id: " + increaseRequest.id());
      IO.println("status: " + increaseRequest.status().asString());
  }
  ```

  ```php PHP
  $client = new Client();

  $increaseRequest = $client->beta->organization->spendLimits->increaseRequests->deny(
      'slir_01AbCdEfGhIjKlMnOpQrSt',
      suppressNotification: true,
  );

  echo "id: {$increaseRequest->id}\n";
  echo "status: {$increaseRequest->status}\n";
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  increase_request = client.beta.organization.spend_limits.increase_requests.deny(
    "slir_01AbCdEfGhIjKlMnOpQrSt",
    suppress_notification: true
  )

  puts "id: #{increase_request.id}"
  puts "status: #{increase_request.status}"
  ```
</CodeGroup>

## Contoh alur kerja

Beberapa alur kerja ini menggabungkan Spend Limits API dengan endpoint biaya [Analytics APIs](https://platform.claude.com/docs/id/manage-claude/analytics-api). Endpoint biaya Analytics dirancang untuk pelaporan pengeluaran seluruh organisasi dalam rentang tanggal. `GET /spend_limits/effective` mengembalikan batas yang saat ini berlaku untuk setiap anggota. Mulailah penyisiran dengan Analytics untuk menemukan anggota mana yang perlu dilihat, lalu baca batas mereka saat ini dengan `/effective`.

Endpoint Spend Limits memerlukan cakupan `spend_limits` dan endpoint biaya Analytics memerlukan `read:analytics`; lihat [Analytics APIs](https://platform.claude.com/docs/id/manage-claude/analytics-api) untuk cara menyediakan akses. Contoh-contoh menggunakan satu kunci Admin API yang memiliki cakupan dari setiap API yang dipanggil. Pemilik utama [memilih cakupan ini saat membuat kunci](https://platform.claude.com/docs/id/manage-claude/admin-api-keys#choose-scopes-for-a-claude-enterprise-key). Semua nilai moneter pada keduanya adalah string desimal dalam satuan minor (sen). Kedua API dipaginasi dengan cursor opaque. Tetapkan `limit` secara eksplisit dan telusuri `next_page` hingga bernilai `null` untuk mencakup seluruh organisasi.

### Mengotomatiskan alur peninjauan permintaan kenaikan

Jalankan job terjadwal yang mengambil permintaan pending, menerapkan kebijakan persetujuan organisasi Anda, dan menyelesaikan masing-masing.

1. Daftarkan permintaan pending:

   <CodeGroup>
     ```bash cURL
     curl -g "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests?status[]=pending&limit=100" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01"
     ```

     ```bash CLI
     ant beta:organization:spend-limits:increase-requests list \
       --status pending \
       --limit 100
     ```

     ```python Python
     client = anthropic.Anthropic()

     increase_requests = client.beta.organization.spend_limits.increase_requests.list(
         status=["pending"], limit=100
     )

     for increase_request in increase_requests:
         print(f"{increase_request.id}: {increase_request.status}")
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const increaseRequests = await client.beta.organization.spendLimits.increaseRequests.list({
       status: ["pending"],
       limit: 100
     });

     for await (const increaseRequest of increaseRequests) {
       console.log(`${increaseRequest.id}: ${increaseRequest.status}`);
     }
     ```

     ```csharp C#
     using Anthropic.Models.Beta.Organization.SpendLimits.IncreaseRequests;

     AnthropicClient client = new();

     var page = await client.Beta.Organization.SpendLimits.IncreaseRequests.List(
         new() { Status = [BetaSpendLimitIncreaseRequestStatus.Pending], Limit = 100 }
     );

     await foreach (var increaseRequest in page.Paginate())
     {
         Console.WriteLine($"{increaseRequest.ID}: {increaseRequest.Status.Raw()}");
     }
     ```

     ```go Go
     client := anthropic.NewClient()

     increaseRequests := client.Beta.Organization.SpendLimits.IncreaseRequests.ListAutoPaging(context.Background(), anthropic.BetaOrganizationSpendLimitIncreaseRequestListParams{
     	Status: []anthropic.BetaSpendLimitIncreaseRequestStatus{anthropic.BetaSpendLimitIncreaseRequestStatusPending},
     	Limit:  anthropic.Int(100),
     })

     for increaseRequests.Next() {
     	increaseRequest := increaseRequests.Current()
     	fmt.Printf("%s: %s\n", increaseRequest.ID, increaseRequest.Status)
     }
     if err := increaseRequests.Err(); err != nil {
     	log.Fatal(err)
     }
     ```

     ```java Java
     import com.anthropic.models.beta.organization.spendlimits.increaserequests.BetaSpendLimitIncreaseRequestStatus;
     import com.anthropic.models.beta.organization.spendlimits.increaserequests.IncreaseRequestListParams;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         var params = IncreaseRequestListParams.builder()
             .addStatus(BetaSpendLimitIncreaseRequestStatus.PENDING)
             .limit(100)
             .build();
         var increaseRequests = client.beta().organization().spendLimits().increaseRequests().list(params);

         for (var increaseRequest : increaseRequests.autoPager()) {
             IO.println(increaseRequest.id() + ": " + increaseRequest.status().asString());
         }
     }
     ```

     ```php PHP
     $client = new Client();

     $increaseRequests = $client->beta->organization->spendLimits->increaseRequests->list(
         status: ['pending'],
         limit: 100,
     );

     foreach ($increaseRequests->pagingEachItem() as $increaseRequest) {
         echo "{$increaseRequest->id}: {$increaseRequest->status}\n";
     }
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     page = client.beta.organization.spend_limits.increase_requests.list(status: [:pending], limit: 100)

     page.auto_paging_each do |increase_request|
       puts "#{increase_request.id}: #{increase_request.status}"
     end
     ```
   </CodeGroup>

   Setiap permintaan membawa `actor.user_id` pemohon dan `spend_summary` langsung dengan `amount` efektif mereka saat ini dan `period_to_date_spend`, cukup untuk memutuskan tanpa pencarian terpisah.

2. Terapkan kebijakan Anda. Misalnya, setujui otomatis ketika `amount` anggota saat ini di bawah ambang, dan arahkan batas yang lebih besar untuk peninjauan manual.

3. Selesaikan setiap permintaan. Untuk menyetujui, berikan batas baru:

   <CodeGroup>
     ```bash cURL
     curl -X POST "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt/approve" \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d '{"amount": "75000", "suppress_notification": true}'
     ```

     ```bash CLI
     ant beta:organization:spend-limits:increase-requests approve \
       --spend-limit-increase-request-id slir_01AbCdEfGhIjKlMnOpQrSt \
       --amount 75000 \
       --suppress-notification
     ```

     ```python Python
     client = anthropic.Anthropic()

     increase_request = client.beta.organization.spend_limits.increase_requests.approve(
         "slir_01AbCdEfGhIjKlMnOpQrSt", amount="75000", suppress_notification=True
     )

     print(f"id: {increase_request.id}")
     print(f"status: {increase_request.status}")
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const increaseRequest = await client.beta.organization.spendLimits.increaseRequests.approve(
       "slir_01AbCdEfGhIjKlMnOpQrSt",
       {
         amount: "75000",
         suppress_notification: true
       }
     );

     console.log(`id: ${increaseRequest.id}`);
     console.log(`status: ${increaseRequest.status}`);
     ```

     ```csharp C#
     AnthropicClient client = new();

     var increaseRequest = await client.Beta.Organization.SpendLimits.IncreaseRequests.Approve(
         "slir_01AbCdEfGhIjKlMnOpQrSt",
         new() { Amount = "75000", SuppressNotification = true }
     );

     Console.WriteLine($"id: {increaseRequest.ID}");
     Console.WriteLine($"status: {increaseRequest.Status.Raw()}");
     ```

     ```go Go
     client := anthropic.NewClient()

     increaseRequest, err := client.Beta.Organization.SpendLimits.IncreaseRequests.Approve(
     	context.Background(),
     	"slir_01AbCdEfGhIjKlMnOpQrSt",
     	anthropic.BetaOrganizationSpendLimitIncreaseRequestApproveParams{
     		Amount:               "75000",
     		SuppressNotification: anthropic.Bool(true),
     	},
     )
     if err != nil {
     	log.Fatal(err)
     }

     fmt.Printf("id: %s\n", increaseRequest.ID)
     fmt.Printf("status: %s\n", increaseRequest.Status)
     ```

     ```java Java
     import com.anthropic.models.beta.organization.spendlimits.increaserequests.IncreaseRequestApproveParams;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         var params = IncreaseRequestApproveParams.builder()
             .amount("75000")
             .suppressNotification(true)
             .build();
         var increaseRequest = client.beta().organization().spendLimits().increaseRequests()
             .approve("slir_01AbCdEfGhIjKlMnOpQrSt", params);

         IO.println("id: " + increaseRequest.id());
         IO.println("status: " + increaseRequest.status().asString());
     }
     ```

     ```php PHP
     $client = new Client();

     $increaseRequest = $client->beta->organization->spendLimits->increaseRequests->approve(
         'slir_01AbCdEfGhIjKlMnOpQrSt',
         amount: '75000',
         suppressNotification: true,
     );

     echo "id: {$increaseRequest->id}\n";
     echo "status: {$increaseRequest->status}\n";
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     increase_request = client.beta.organization.spend_limits.increase_requests.approve(
       "slir_01AbCdEfGhIjKlMnOpQrSt",
       amount: "75000",
       suppress_notification: true
     )

     puts "id: #{increase_request.id}"
     puts "status: #{increase_request.status}"
     ```
   </CodeGroup>

   Untuk menolak, panggil [endpoint deny](https://platform.claude.com/docs/id/manage-claude/spend-limits-api#deny-an-increase-request) dengan ID yang sama sebagai gantinya. Kirimkan `suppress_notification: true` ketika sistem Anda sendiri memberi tahu pemohon.

### Mengidentifikasi anggota yang mendekati batas pengeluaran mereka

Temukan anggota yang mendekati batas mereka sehingga Anda dapat menaikkannya sebelum mereka terblokir.

1. Ambil pengeluaran bulan berjalan setiap anggota dari Analytics API (satu baris per anggota, pengeluaran tertinggi lebih dulu secara default):

   <CodeGroup>
     ```bash cURL
     curl "https://api.anthropic.com/v1/organizations/analytics/user_cost_report?starting_at=2026-06-01T00:00:00Z&limit=1000" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01"
     ```

     ```bash CLI
     ant beta:organization:analytics:user-cost-report list \
       --starting-at 2026-06-01T00:00:00Z \
       --limit 1000
     ```

     ```python Python
     client = anthropic.Anthropic()

     cost_rows = client.beta.organization.analytics.user_cost_report.list(
         starting_at="2026-06-01T00:00:00Z", limit=1000
     )

     for cost_row in cost_rows:
         print(f"{cost_row.actor.user_id}: {cost_row.amount}")
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const costRows = await client.beta.organization.analytics.userCostReport.list({
       starting_at: "2026-06-01T00:00:00Z",
       limit: 1000
     });

     for await (const costRow of costRows) {
       console.log(`${costRow.actor.user_id}: ${costRow.amount}`);
     }
     ```

     ```csharp C#
     AnthropicClient client = new();

     var page = await client.Beta.Organization.Analytics.UserCostReport.List(
         new()
         {
             StartingAt = DateTimeOffset.Parse("2026-06-01T00:00:00Z"),
             Limit = 1000,
         }
     );

     await foreach (var costRow in page.Paginate())
     {
         Console.WriteLine($"{costRow.Actor.UserID}: {costRow.Amount}");
     }
     ```

     ```go Go
     client := anthropic.NewClient()

     costRows := client.Beta.Organization.Analytics.UserCostReport.ListAutoPaging(context.Background(), anthropic.BetaOrganizationAnalyticsUserCostReportListParams{
     	StartingAt: time.Date(2026, time.June, 1, 0, 0, 0, 0, time.UTC),
     	Limit:      anthropic.Int(1000),
     })

     for costRows.Next() {
     	costRow := costRows.Current()
     	fmt.Printf("%s: %s\n", costRow.Actor.UserID, costRow.Amount)
     }
     if err := costRows.Err(); err != nil {
     	log.Fatal(err)
     }
     ```

     ```java Java
     import com.anthropic.models.beta.organization.analytics.usercostreport.UserCostReportListParams;
     import java.time.OffsetDateTime;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         var params = UserCostReportListParams.builder()
             .startingAt(OffsetDateTime.parse("2026-06-01T00:00:00Z"))
             .limit(1000)
             .build();
         var costRows = client.beta().organization().analytics().userCostReport().list(params);

         for (var costRow : costRows.autoPager()) {
             IO.println(costRow.actor().userId() + ": " + costRow.amount());
         }
     }
     ```

     ```php PHP
     $client = new Client();

     $costRows = $client->beta->organization->analytics->userCostReport->list(
         startingAt: new \DateTimeImmutable('2026-06-01T00:00:00Z'),
         limit: 1000,
     );

     foreach ($costRows->pagingEachItem() as $costRow) {
         echo "{$costRow->actor->userID}: {$costRow->amount}\n";
     }
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     page = client.beta.organization.analytics.user_cost_report.list(
       starting_at: Time.utc(2026, 6, 1),
       limit: 1000
     )

     page.auto_paging_each do |cost_row|
       puts "#{cost_row.actor.user_id}: #{cost_row.amount}"
     end
     ```
   </CodeGroup>

   Setiap baris berisi `actor.user_id`, `actor.email_address`, dan `amount` (pengeluaran anggota dalam sen). Telusuri `next_page` untuk mencakup seluruh organisasi.

2. Untuk pembelanja teratas (atau semua orang di atas ambang dolar), ambil batas efektif dalam batch:

   <CodeGroup>
     ```bash cURL
     curl -g "https://api.anthropic.com/v1/organizations/spend_limits/effective?user_ids[]=user_01AbCdEfGh&user_ids[]=user_01JkLmNoPq&limit=100" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01"
     ```

     ```bash CLI
     ant beta:organization:spend-limits:effective list \
       --user-id user_01AbCdEfGh \
       --user-id user_01JkLmNoPq \
       --limit 100
     ```

     ```python Python
     client = anthropic.Anthropic()

     effective_limits = client.beta.organization.spend_limits.effective.list(
         user_ids=["user_01AbCdEfGh", "user_01JkLmNoPq"], limit=100
     )

     for effective_limit in effective_limits:
         scope = effective_limit.scope
         if scope.type == "user":
             amount = effective_limit.amount or "unlimited"
             print(f"{scope.user_id}: {effective_limit.period_to_date_spend} of {amount}")
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const effectiveLimits = await client.beta.organization.spendLimits.effective.list({
       user_ids: ["user_01AbCdEfGh", "user_01JkLmNoPq"],
       limit: 100
     });

     for await (const effectiveLimit of effectiveLimits) {
       const { scope } = effectiveLimit;
       if (scope.type === "user") {
         const amount = effectiveLimit.amount ?? "unlimited";
         console.log(`${scope.user_id}: ${effectiveLimit.period_to_date_spend} of ${amount}`);
       }
     }
     ```

     ```csharp C#
     AnthropicClient client = new();

     var page = await client.Beta.Organization.SpendLimits.Effective.List(
         new() { UserIds = ["user_01AbCdEfGh", "user_01JkLmNoPq"], Limit = 100 }
     );

     await foreach (var effectiveLimit in page.Paginate())
     {
         if (effectiveLimit.Scope.TryPickBetaSpendLimitUser(out var userScope))
         {
             var amount = effectiveLimit.Amount ?? "unlimited";
             Console.WriteLine($"{userScope.UserID}: {effectiveLimit.PeriodToDateSpend} of {amount}");
         }
     }
     ```

     ```go Go
     client := anthropic.NewClient()

     effectiveLimits := client.Beta.Organization.SpendLimits.Effective.ListAutoPaging(context.Background(), anthropic.BetaOrganizationSpendLimitEffectiveListParams{
     	UserIDs: []string{"user_01AbCdEfGh", "user_01JkLmNoPq"},
     	Limit:   anthropic.Int(100),
     })

     for effectiveLimits.Next() {
     	effectiveLimit := effectiveLimits.Current()
     	if userScope, ok := effectiveLimit.Scope.AsAny().(anthropic.BetaSpendLimitUserScope); ok {
     		amount := effectiveLimit.Amount
     		if !effectiveLimit.JSON.Amount.Valid() {
     			amount = "unlimited"
     		}
     		fmt.Printf("%s: %s of %s\n", userScope.UserID, effectiveLimit.PeriodToDateSpend, amount)
     	}
     }
     if err := effectiveLimits.Err(); err != nil {
     	log.Fatal(err)
     }
     ```

     ```java Java
     import com.anthropic.models.beta.organization.spendlimits.effective.EffectiveListParams;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         var params = EffectiveListParams.builder()
             .addUserId("user_01AbCdEfGh")
             .addUserId("user_01JkLmNoPq")
             .limit(100)
             .build();
         var effectiveLimits = client.beta().organization().spendLimits().effective().list(params);

         for (var effectiveLimit : effectiveLimits.autoPager()) {
             var amount = effectiveLimit.amount().orElse("unlimited");
             effectiveLimit.scope().user().ifPresent(userScope ->
                 IO.println(userScope.userId() + ": " + effectiveLimit.periodToDateSpend() + " of " + amount)
             );
         }
     }
     ```

     ```php PHP
     use Anthropic\Beta\Organization\SpendLimits\SpendLimitUserScope;
     // ...

     $client = new Client();

     $effectiveLimits = $client->beta->organization->spendLimits->effective->list(
         userIDs: ['user_01AbCdEfGh', 'user_01JkLmNoPq'],
         limit: 100,
     );

     foreach ($effectiveLimits->pagingEachItem() as $effectiveLimit) {
         $scope = $effectiveLimit->scope;
         if ($scope instanceof SpendLimitUserScope) {
             $amount = $effectiveLimit->amount ?? 'unlimited';
             echo "{$scope->userID}: {$effectiveLimit->periodToDateSpend} of {$amount}\n";
         }
     }
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     page = client.beta.organization.spend_limits.effective.list(
       user_ids: ["user_01AbCdEfGh", "user_01JkLmNoPq"],
       limit: 100
     )

     page.auto_paging_each do |effective_limit|
       scope = effective_limit.scope
       if scope.is_a?(Anthropic::Models::Beta::Organization::BetaSpendLimitUserScope)
         amount = effective_limit.amount || "unlimited"
         puts "#{scope.user_id}: #{effective_limit.period_to_date_spend} of #{amount}"
       end
     end
     ```
   </CodeGroup>

   Setiap baris mengembalikan batas sebagai `amount` (`null` = tanpa batas, `"0"` = hanya penggunaan termasuk) bersama `period_to_date_spend`.

3. Untuk setiap anggota dengan batas positif, hitung `period_to_date_spend / amount` dan tandai mereka yang berada pada atau di atas ambang Anda (misalnya, 80 persen). Perlakukan batas `"0"` sebagai sudah mencapai batas. Tidak ada filter sisi server untuk rasio ini.

4. Tindak lanjuti anggota yang ditandai: naikkan batas dengan `POST /v1/organizations/spend_limits`, setujui permintaan kenaikan pending jika ada, atau hubungi anggota tersebut.

### Menemukan anggota dengan penggunaan yang berubah cepat

Munculkan anggota yang pengeluarannya melonjak dari minggu ke minggu.

1. Ambil biaya harian per anggota untuk dua minggu terakhir dari Analytics API:

   <CodeGroup>
     ```bash cURL
     curl "https://api.anthropic.com/v1/organizations/analytics/user_cost_report?starting_at=2026-06-09T00:00:00Z&ending_at=2026-06-23T00:00:00Z&bucket_width=1d&limit=1000" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01"
     ```

     ```bash CLI
     ant beta:organization:analytics:user-cost-report list \
       --starting-at 2026-06-09T00:00:00Z \
       --ending-at 2026-06-23T00:00:00Z \
       --bucket-width 1d \
       --limit 1000
     ```

     ```python Python
     client = anthropic.Anthropic()

     cost_rows = client.beta.organization.analytics.user_cost_report.list(
         starting_at="2026-06-09T00:00:00Z",
         ending_at="2026-06-23T00:00:00Z",
         bucket_width="1d",
         limit=1000,
     )

     for cost_row in cost_rows:
         print(f"{cost_row.actor.user_id} {cost_row.starting_at}: {cost_row.amount}")
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const costRows = await client.beta.organization.analytics.userCostReport.list({
       starting_at: "2026-06-09T00:00:00Z",
       ending_at: "2026-06-23T00:00:00Z",
       bucket_width: "1d",
       limit: 1000
     });

     for await (const costRow of costRows) {
       console.log(`${costRow.actor.user_id} ${costRow.starting_at}: ${costRow.amount}`);
     }
     ```

     ```csharp C#
     using Anthropic.Models.Beta.Organization.Analytics.UserCostReport;

     AnthropicClient client = new();

     var page = await client.Beta.Organization.Analytics.UserCostReport.List(
         new()
         {
             StartingAt = DateTimeOffset.Parse("2026-06-09T00:00:00Z"),
             EndingAt = DateTimeOffset.Parse("2026-06-23T00:00:00Z"),
             BucketWidth = BucketWidth.Day,
             Limit = 1000,
         }
     );

     await foreach (var costRow in page.Paginate())
     {
         Console.WriteLine($"{costRow.Actor.UserID} {costRow.StartingAt}: {costRow.Amount}");
     }
     ```

     ```go Go
     client := anthropic.NewClient()

     costRows := client.Beta.Organization.Analytics.UserCostReport.ListAutoPaging(context.Background(), anthropic.BetaOrganizationAnalyticsUserCostReportListParams{
     	StartingAt:  time.Date(2026, time.June, 9, 0, 0, 0, 0, time.UTC),
     	EndingAt:    anthropic.Time(time.Date(2026, time.June, 23, 0, 0, 0, 0, time.UTC)),
     	BucketWidth: anthropic.BetaOrganizationAnalyticsUserCostReportListParamsBucketWidthDay,
     	Limit:       anthropic.Int(1000),
     })

     for costRows.Next() {
     	costRow := costRows.Current()
     	fmt.Printf("%s %s: %s\n", costRow.Actor.UserID, costRow.StartingAt, costRow.Amount)
     }
     if err := costRows.Err(); err != nil {
     	log.Fatal(err)
     }
     ```

     ```java Java
     import com.anthropic.models.beta.organization.analytics.usercostreport.UserCostReportListParams;
     import java.time.OffsetDateTime;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         var params = UserCostReportListParams.builder()
             .startingAt(OffsetDateTime.parse("2026-06-09T00:00:00Z"))
             .endingAt(OffsetDateTime.parse("2026-06-23T00:00:00Z"))
             .bucketWidth(UserCostReportListParams.BucketWidth.DAY)
             .limit(1000)
             .build();
         var costRows = client.beta().organization().analytics().userCostReport().list(params);

         for (var costRow : costRows.autoPager()) {
             IO.println(costRow.actor().userId() + " " + costRow.startingAt().orElseThrow() + ": " + costRow.amount());
         }
     }
     ```

     ```php PHP
     $client = new Client();

     $costRows = $client->beta->organization->analytics->userCostReport->list(
         startingAt: new \DateTimeImmutable('2026-06-09T00:00:00Z'),
         endingAt: new \DateTimeImmutable('2026-06-23T00:00:00Z'),
         bucketWidth: '1d',
         limit: 1000,
     );

     foreach ($costRows->pagingEachItem() as $costRow) {
         $startingAt = $costRow->startingAt?->format(\DateTimeInterface::ATOM);
         echo "{$costRow->actor->userID} {$startingAt}: {$costRow->amount}\n";
     }
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     page = client.beta.organization.analytics.user_cost_report.list(
       starting_at: Time.utc(2026, 6, 9),
       ending_at: Time.utc(2026, 6, 23),
       bucket_width: :"1d",
       limit: 1000
     )

     page.auto_paging_each do |cost_row|
       puts "#{cost_row.actor.user_id} #{cost_row.starting_at}: #{cost_row.amount}"
     end
     ```
   </CodeGroup>

   Dengan `bucket_width` ditetapkan, setiap anggota mencakup satu baris per hari yang memiliki penggunaan. Telusuri `next_page` untuk mengumpulkan seluruh rangkaian data setiap anggota.

2. Kelompokkan baris berdasarkan `actor.user_id`. Untuk setiap anggota, jumlahkan tujuh hari terakhir dan tujuh hari sebelumnya. Tandai anggota yang minggu terakhirnya melebihi minggu sebelumnya dengan kelipatan pilihan Anda (misalnya, tiga). Biaya hari-hari terakhir bersifat sementara dan dapat direvisi naik; untuk perbandingan yang dapat diulang, tetapkan `ending_at` pada atau sebelum `data_refreshed_at` yang dikembalikan sebelumnya (lihat [Ketersediaan dan kesegaran data](https://platform.claude.com/docs/id/manage-claude/analytics-api#data-availability-and-freshness)).

3. Tindak lanjuti anggota yang ditandai: sesuaikan batas dengan `POST /v1/organizations/spend_limits`, atau hubungi mereka.

### Menaikkan sementara batas pengeluaran anggota selama insiden

Beri ruang bagi penanggap insiden untuk bekerja selama insiden terbuka: naikkan batas pengeluaran mereka ketika insiden dimulai, dan kembalikan setelah insiden ditutup. Kendalikan kenaikan tersebut berdasarkan sistem manajemen insiden Anda, misalnya dengan mewajibkan ID insiden aktif dengan anggota yang ditugaskan padanya.

1. Baca batas anggota saat ini, dan catat untuk rollback:

   <CodeGroup>
     ```bash cURL
     curl -g "https://api.anthropic.com/v1/organizations/spend_limits/effective?user_ids[]=user_01AbCdEfGh&period[]=monthly" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01"
     ```

     ```bash CLI
     ant beta:organization:spend-limits:effective list \
       --user-id user_01AbCdEfGh \
       --period monthly
     ```

     ```python Python
     client = anthropic.Anthropic()

     effective_limits = client.beta.organization.spend_limits.effective.list(
         user_ids=["user_01AbCdEfGh"], period=["monthly"]
     )

     for effective_limit in effective_limits:
         scope = effective_limit.scope
         if scope.type == "user":
             amount = effective_limit.amount or "unlimited"
             print(f"{scope.user_id}: {effective_limit.period_to_date_spend} of {amount}")
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const effectiveLimits = await client.beta.organization.spendLimits.effective.list({
       user_ids: ["user_01AbCdEfGh"],
       period: ["monthly"]
     });

     for await (const effectiveLimit of effectiveLimits) {
       const { scope } = effectiveLimit;
       if (scope.type === "user") {
         const amount = effectiveLimit.amount ?? "unlimited";
         console.log(`${scope.user_id}: ${effectiveLimit.period_to_date_spend} of ${amount}`);
       }
     }
     ```

     ```csharp C#
     using Anthropic.Models.Beta.Organization.SpendLimits.Effective;

     AnthropicClient client = new();

     var page = await client.Beta.Organization.SpendLimits.Effective.List(
         new() { UserIds = ["user_01AbCdEfGh"], Period = [Period.Monthly] }
     );

     await foreach (var effectiveLimit in page.Paginate())
     {
         if (effectiveLimit.Scope.TryPickBetaSpendLimitUser(out var userScope))
         {
             var amount = effectiveLimit.Amount ?? "unlimited";
             Console.WriteLine($"{userScope.UserID}: {effectiveLimit.PeriodToDateSpend} of {amount}");
         }
     }
     ```

     ```go Go
     client := anthropic.NewClient()

     effectiveLimits := client.Beta.Organization.SpendLimits.Effective.ListAutoPaging(context.Background(), anthropic.BetaOrganizationSpendLimitEffectiveListParams{
     	UserIDs: []string{"user_01AbCdEfGh"},
     	Period:  []string{"monthly"},
     })

     for effectiveLimits.Next() {
     	effectiveLimit := effectiveLimits.Current()
     	if userScope, ok := effectiveLimit.Scope.AsAny().(anthropic.BetaSpendLimitUserScope); ok {
     		amount := effectiveLimit.Amount
     		if !effectiveLimit.JSON.Amount.Valid() {
     			amount = "unlimited"
     		}
     		fmt.Printf("%s: %s of %s\n", userScope.UserID, effectiveLimit.PeriodToDateSpend, amount)
     	}
     }
     if err := effectiveLimits.Err(); err != nil {
     	log.Fatal(err)
     }
     ```

     ```java Java
     import com.anthropic.models.beta.organization.spendlimits.effective.EffectiveListParams;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         var params = EffectiveListParams.builder()
             .addUserId("user_01AbCdEfGh")
             .addPeriod(EffectiveListParams.Period.MONTHLY)
             .build();
         var effectiveLimits = client.beta().organization().spendLimits().effective().list(params);

         for (var effectiveLimit : effectiveLimits.autoPager()) {
             var amount = effectiveLimit.amount().orElse("unlimited");
             effectiveLimit.scope().user().ifPresent(userScope ->
                 IO.println(userScope.userId() + ": " + effectiveLimit.periodToDateSpend() + " of " + amount)
             );
         }
     }
     ```

     ```php PHP
     use Anthropic\Beta\Organization\SpendLimits\SpendLimitUserScope;
     // ...

     $client = new Client();

     $effectiveLimits = $client->beta->organization->spendLimits->effective->list(
         userIDs: ['user_01AbCdEfGh'],
         period: ['monthly'],
     );

     foreach ($effectiveLimits->pagingEachItem() as $effectiveLimit) {
         $scope = $effectiveLimit->scope;
         if ($scope instanceof SpendLimitUserScope) {
             $amount = $effectiveLimit->amount ?? 'unlimited';
             echo "{$scope->userID}: {$effectiveLimit->periodToDateSpend} of {$amount}\n";
         }
     }
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     page = client.beta.organization.spend_limits.effective.list(
       user_ids: ["user_01AbCdEfGh"],
       period: [:monthly]
     )

     page.auto_paging_each do |effective_limit|
       scope = effective_limit.scope
       if scope.is_a?(Anthropic::Models::Beta::Organization::BetaSpendLimitUserScope)
         amount = effective_limit.amount || "unlimited"
         puts "#{scope.user_id}: #{effective_limit.period_to_date_spend} of #{amount}"
       end
     end
     ```
   </CodeGroup>

2. Naikkan batas:

   <CodeGroup>
     ```bash cURL
     curl -X POST "https://api.anthropic.com/v1/organizations/spend_limits" \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d '{"scope": {"type": "user", "user_id": "user_01AbCdEfGh"}, "amount": "500000", "period": "monthly"}'
     ```

     ```bash CLI
     ant beta:organization:spend-limits set \
       --scope '{type: user, user_id: user_01AbCdEfGh}' \
       --amount 500000 \
       --period monthly
     ```

     ```python Python
     client = anthropic.Anthropic()

     spend_limit = client.beta.organization.spend_limits.set(
         scope={"type": "user", "user_id": "user_01AbCdEfGh"},
         amount="500000",
         period="monthly",
     )

     print(f"id: {spend_limit.id}")
     print(f"amount: {spend_limit.amount}")
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const spendLimit = await client.beta.organization.spendLimits.set({
       scope: { type: "user", user_id: "user_01AbCdEfGh" },
       amount: "500000",
       period: "monthly"
     });

     console.log(`id: ${spendLimit.id}`);
     console.log(`amount: ${spendLimit.amount}`);
     ```

     ```csharp C#
     using Anthropic.Models.Beta.Organization.SpendLimits;

     AnthropicClient client = new();

     var spendLimit = await client.Beta.Organization.SpendLimits.Set(
         new()
         {
             Scope = new BetaSpendLimitUserScope("user_01AbCdEfGh"),
             Amount = "500000",
             Period = BetaSpendLimitPeriod.Monthly,
         }
     );

     Console.WriteLine($"id: {spendLimit.ID}");
     Console.WriteLine($"amount: {spendLimit.Amount}");
     ```

     ```go Go
     client := anthropic.NewClient()

     spendLimit, err := client.Beta.Organization.SpendLimits.Set(context.Background(), anthropic.BetaOrganizationSpendLimitSetParams{
     	Scope: anthropic.BetaOrganizationSpendLimitSetParamsScopeUnion{
     		OfUser: &anthropic.BetaSpendLimitUserScopeParam{UserID: "user_01AbCdEfGh"},
     	},
     	Amount: anthropic.String("500000"),
     	Period: anthropic.BetaSpendLimitPeriodMonthly,
     })
     if err != nil {
     	log.Fatal(err)
     }

     fmt.Printf("id: %s\n", spendLimit.ID)
     fmt.Printf("amount: %s\n", spendLimit.Amount)
     ```

     ```java Java
     import com.anthropic.models.beta.organization.spendlimits.BetaSpendLimitPeriod;
     import com.anthropic.models.beta.organization.spendlimits.SpendLimitSetParams;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         var params = SpendLimitSetParams.builder()
             .userScope("user_01AbCdEfGh")
             .amount("500000")
             .period(BetaSpendLimitPeriod.MONTHLY)
             .build();
         var spendLimit = client.beta().organization().spendLimits().set(params);

         IO.println("id: " + spendLimit.id());
         IO.println("amount: " + spendLimit.amount().orElseThrow());
     }
     ```

     ```php PHP
     use Anthropic\Beta\Organization\SpendLimits\SpendLimitUserScope;
     // ...

     $client = new Client();

     $spendLimit = $client->beta->organization->spendLimits->set(
         scope: SpendLimitUserScope::with(userID: 'user_01AbCdEfGh'),
         amount: '500000',
         period: 'monthly',
     );

     echo "id: {$spendLimit->id}\n";
     echo "amount: {$spendLimit->amount}\n";
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     spend_limit = client.beta.organization.spend_limits.set(
       scope: { type: :user, user_id: "user_01AbCdEfGh" },
       amount: "500000",
       period: :monthly
     )

     puts "id: #{spend_limit.id}"
     puts "amount: #{spend_limit.amount}"
     ```
   </CodeGroup>

3. Jika penanggap memerlukan akses yang lebih luas selama insiden, sediakan terlebih dahulu grup incident-responders yang [peran kustomnya](https://platform.claude.com/docs/id/manage-claude/user-management#custom-roles) memberikan akses tersebut, dan tambahkan anggota selama durasi insiden:

   <CodeGroup>
     ```bash cURL
     curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members" \
       -H "content-type: application/json" \
       -H "x-api-key: $ANTHROPIC_API_KEY" \
       -H "anthropic-version: 2023-06-01" \
       -d '{"user_id": "user_01AbCdEfGh"}'
     ```

     ```bash CLI
     ant beta:organization:rbac-groups:members add \
       --rbac-group-id rbac_group_01UvWxYzAbCdEfGhIjKlMn \
       --user-id user_01AbCdEfGh
     ```

     ```python Python
     client = anthropic.Anthropic()

     member = client.beta.organization.rbac_groups.members.add(
         "rbac_group_01UvWxYzAbCdEfGhIjKlMn", user_id="user_01AbCdEfGh"
     )

     print(f"user_id: {member.user_id}")
     print(f"rbac_group_id: {member.rbac_group_id}")
     ```

     ```typescript TypeScript
     const client = new Anthropic();

     const member = await client.beta.organization.rbacGroups.members.add(
       "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
       {
         user_id: "user_01AbCdEfGh"
       }
     );

     console.log(`user_id: ${member.user_id}`);
     console.log(`rbac_group_id: ${member.rbac_group_id}`);
     ```

     ```csharp C#
     AnthropicClient client = new();

     var member = await client.Beta.Organization.RbacGroups.Members.Add(
         "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
         new() { UserID = "user_01AbCdEfGh" }
     );

     Console.WriteLine($"user_id: {member.UserID}");
     Console.WriteLine($"rbac_group_id: {member.RbacGroupID}");
     ```

     ```go Go
     client := anthropic.NewClient()

     member, err := client.Beta.Organization.RBACGroups.Members.Add(
     	context.Background(),
     	"rbac_group_01UvWxYzAbCdEfGhIjKlMn",
     	anthropic.BetaOrganizationRBACGroupMemberAddParams{
     		UserID: "user_01AbCdEfGh",
     	},
     )
     if err != nil {
     	log.Fatal(err)
     }

     fmt.Printf("user_id: %s\n", member.UserID)
     fmt.Printf("rbac_group_id: %s\n", member.RBACGroupID)
     ```

     ```java Java
     import com.anthropic.models.beta.organization.rbacgroups.members.MemberAddParams;

     void main() {
         AnthropicClient client = AnthropicOkHttpClient.fromEnv();

         var params = MemberAddParams.builder()
             .userId("user_01AbCdEfGh")
             .build();
         var member = client.beta().organization().rbacGroups().members()
             .add("rbac_group_01UvWxYzAbCdEfGhIjKlMn", params);

         IO.println("user_id: " + member.userId());
         IO.println("rbac_group_id: " + member.rbacGroupId());
     }
     ```

     ```php PHP
     $client = new Client();

     $member = $client->beta->organization->rbacGroups->members->add(
         'rbac_group_01UvWxYzAbCdEfGhIjKlMn',
         userID: 'user_01AbCdEfGh',
     );

     echo "user_id: {$member->userID}\n";
     echo "rbac_group_id: {$member->rbacGroupID}\n";
     ```

     ```ruby Ruby
     client = Anthropic::Client.new

     member = client.beta.organization.rbac_groups.members.add(
       "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
       user_id: "user_01AbCdEfGh"
     )

     puts "user_id: #{member.user_id}"
     puts "rbac_group_id: #{member.rbac_group_id}"
     ```
   </CodeGroup>

   Lihat [Manajemen pengguna](https://platform.claude.com/docs/id/manage-claude/user-management#groups) untuk endpoint grup.

4. Ketika sistem insiden Anda menandai insiden sebagai ditutup, kembalikan kedua perubahan: pulihkan batas pengeluaran yang Anda catat pada langkah 1 (atau hapus override dengan `DELETE /v1/organizations/spend_limits/{spend_limit_id}` jika anggota sebelumnya tidak memilikinya), dan hapus anggota dari grup dengan `DELETE /v1/organizations/rbac_groups/{rbac_group_id}/members/{user_id}`.

## Pertanyaan yang sering diajukan

### Apakah menetapkan batas pengeluaran secara langsung menyelesaikan permintaan kenaikan pending seorang anggota?

Tidak. `POST /v1/organizations/spend_limits` menulis override tetapi membiarkan permintaan pending tidak tersentuh. Gunakan `POST /v1/organizations/spend_limit_increase_requests/{id}/approve` untuk menyelesaikan permintaan dan menulis override dalam satu panggilan.

### Apa yang terjadi ketika saya menghapus override per pengguna?

Anggota kembali ke apa pun yang akan mereka warisi dari hierarki: default grup, seat-tier, atau organisasi mereka. Jika tidak ada default di tingkat mana pun, anggota tersebut tanpa batas.

### Dapatkah saya menetapkan default seat-tier atau seluruh organisasi melalui API ini?

Tidak. Hanya override per pengguna yang dapat ditulis melalui API ini. Default tingkat seat-tier, grup, dan organisasi dikonfigurasi di pengaturan Organisasi claude.ai.

### Mengapa `period_to_date_spend` terkadang terbaca sebagai `"0"` untuk anggota aktif?

Pembacaan pengeluaran dapat sementara tidak tersedia, dalam hal ini field terbaca `"0"` alih-alih menghasilkan error. Perlakukan sebagai informasional.

## Lihat juga

<CardGroup cols={2}>
  <Card title="Referensi Spend Limits API" href="https://platform.claude.com/docs/id/api/beta/organization/spend_limits">
    Skema permintaan dan respons yang dihasilkan untuk setiap endpoint Spend Limits API.
  </Card>

  <Card title="Referensi Spend Limit Increase Requests API" href="https://platform.claude.com/docs/id/api/beta/organization/spend_limits/increase_requests">
    Skema permintaan dan respons yang dihasilkan untuk endpoint permintaan kenaikan.
  </Card>

  <Card title="Analytics APIs" href="https://platform.claude.com/docs/id/manage-claude/analytics-api">
    Pelaporan penggunaan dan biaya per pengguna dan per rentang waktu untuk Claude Enterprise.
  </Card>
</CardGroup>
