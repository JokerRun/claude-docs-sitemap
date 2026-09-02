---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe
fetched_at: 2026-09-02T02:36:53.462770Z
sha256: 3dff996c5b499da8177b1ae19e32197efb3b5f85dc5517a69f163dba3040d065
---

---
title: Menggunakan WIF dengan SPIFFE
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe
description: Autentikasi workload SPIFFE ke Claude API menggunakan JWT-SVID dari SPIRE atau penerbit lain yang sesuai dengan SPIFFE.
---

[SPIFFE](https://spiffe.io/) adalah standar CNCF untuk menerbitkan identitas bagi workload. [SPIRE](https://spiffe.io/docs/latest/spire-about/) adalah implementasi referensi open-source-nya, dan beberapa produk komersial juga menerbitkan identitas yang sesuai dengan SPIFFE. Anthropic melakukan federasi dengan implementasi SPIFFE apa pun yang menghasilkan JWT-SVID yang kompatibel dengan OIDC. Untuk daftar implementasi terkini, lihat [Commercial software that implements SPIFFE](https://spiffe.io/docs/latest/spiffe-about/overview/#commercial-software-that-implements-spiffe) di situs proyek SPIFFE.

Federasi bekerja baik melalui dokumen discovery OIDC di URL HTTPS publik (mode `discovery`, tunduk pada [batasan URL](https://platform.claude.com/docs/id/manage-claude/wif-reference#url-fields)) atau dengan mendaftarkan JWKS secara langsung (mode `inline`).

Spesifikasi JWT-SVID mendefinisikan `sub` sebagai SPIFFE ID milik workload, dan SPIFFE Workload API mengharuskan pemanggil menyediakan `aud` pada saat pengambilan, sehingga klaim-klaim tersebut sama di semua implementasi. Anthropic juga mewajibkan `iss` dan `iat`, yang keduanya tidak diwajibkan oleh spesifikasi JWT-SVID, jadi konfigurasikan implementasi Anda untuk mengisi keduanya (di SPIRE, `iss` adalah pengaturan server `jwt_issuer` dan `iat` diatur secara otomatis). Dengan semua itu terpenuhi, bagian [Konfigurasi Anthropic](https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe#configure-anthropic), [Memperoleh dan menggunakan token](https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe#acquire-and-use-the-token), dan [Membatasi cakupan aturan Anda](https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe#scope-your-rule) dalam panduan ini berlaku untuk implementasi SPIFFE apa pun.

SPIFFE memberikan setiap workload sebuah URI identitas yang stabil dengan bentuk `spiffe://<trust-domain>/<path>`, dan SPIRE menerbitkan identitas tersebut sebagai JWT-SVID sesuai permintaan melalui Workload API. JWT-SVID adalah JWT bertanda tangan biasa yang klaim `sub`-nya adalah SPIFFE ID milik workload dan klaim `aud`-nya disediakan oleh workload pada saat pengambilan.

Jembatan dari trust domain SPIRE ke OIDC standar adalah [SPIRE OIDC Discovery Provider](https://github.com/spiffe/spire/blob/main/support/oidc-discovery-provider/README.md), sebuah helper mandiri yang memublikasikan `/.well-known/openid-configuration` dan endpoint JWKS untuk kunci penandatanganan JWT milik trust domain. Dengan discovery provider berjalan, JWT-SVID divalidasi seperti token OIDC lainnya: daftarkan URL discovery sebagai federation issuer (penerbit federasi), tulis federation rule (aturan federasi) yang cocok dengan SPIFFE ID milik workload, dan minta workload menyajikan JWT-SVID-nya ke endpoint token-exchange Anthropic.

Contoh-contoh di halaman ini menggunakan SPIRE dan berlaku di mana pun SPIRE Agent berjalan: pod Kubernetes, mesin virtual, dan host bare-metal.

<Note>
  Jika cluster Kubernetes Anda tidak menjalankan SPIRE dan Anda ingin mengautentikasi dengan projected service-account token bawaan cluster, lihat [Menggunakan WIF dengan Kubernetes](https://platform.claude.com/docs/id/manage-claude/wif-providers/kubernetes).
</Note>

## Prasyarat

* Pemahaman tentang [konsep WIF](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#concepts): service account, federation issuer, dan federation rule.
* Deployment SPIFFE dengan identitas workload yang telah diterbitkan (contoh di halaman ini menggunakan SPIRE Server dan Agent), serta registration entry untuk workload yang perlu memanggil Claude API.
* Endpoint discovery OIDC untuk trust domain (di SPIRE, [OIDC Discovery Provider](https://github.com/spiffe/spire/blob/main/support/oidc-discovery-provider/README.md)) yang berjalan dengan endpoint HTTPS yang dapat dijangkau secara publik, atau JWKS yang diekspor untuk pendaftaran `inline`.
* Penerbit SPIFFE Anda dikonfigurasi untuk mengatur klaim `iss` pada JWT-SVID ke nilai yang akan Anda daftarkan sebagai `issuer_url` milik federation issuer. Untuk mode `discovery`, ini adalah URL publik endpoint discovery (di SPIRE, pengaturan server `jwt_issuer`).
* JWT-SVID tersedia bagi workload Anda. WIF hanya menerima JWT-SVID, bukan X.509-SVID.
* Izin untuk membuat service account, federation issuer, dan federation rule di Claude Console untuk organisasi Anthropic Anda.

Nilai audience yang diminta saat mengambil JWT-SVID selalu `https://api.anthropic.com`. Gunakan nilai ini di `jwt_audience` milik spiffe-helper, panggilan Workload API `FetchJWTSVID`, dan matcher `audience` pada federation rule.

## Konfigurasi SPIRE

Instruksi di bagian ini khusus untuk SPIRE. Jika Anda menggunakan penerbit SPIFFE yang berbeda, konfigurasikan endpoint discovery OIDC dan pengambilan JWT-SVID-nya sesuai dokumentasinya sendiri, lalu lanjutkan ke [Konfigurasi Anthropic](https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe#configure-anthropic).

Jika Anda sudah menjalankan SPIRE dengan OIDC Discovery Provider, federasi dengan Anthropic memerlukan tiga hal di sisi SPIRE: `jwt_issuer` yang cocok dengan URL discovery, registration entry untuk workload yang akan memanggil Claude API, dan cara bagi workload tersebut untuk mengambil JWT-SVID dengan audience Anthropic. Subbagian berikut membahas masing-masing. Cuplikan konfigurasi hanya menampilkan pengaturan yang relevan dengan federasi Anthropic, bukan konfigurasi deployment SPIRE yang lengkap.

<Tip>
  Baru pertama kali menyiapkan SPIRE? Deploy SPIRE Server dan Agent dengan mengikuti [SPIRE quickstart](https://spiffe.io/docs/latest/try/), lalu tambahkan [OIDC Discovery Provider](https://github.com/spiffe/spire/blob/main/support/oidc-discovery-provider/README.md) sebagai layanan terpisah di samping SPIRE Server. Federasi mode discovery bergantung pada provider yang telah di-deploy dan dapat dijangkau secara publik. Provider ini bukan bagian dari instalasi SPIRE default.
</Tip>

### Verifikasi JWT issuer

Anthropic memvalidasi JWT-SVID dengan mencocokkan klaim `iss`-nya terhadap federation issuer yang terdaftar dan mengambil JWKS dari dokumen discovery milik issuer tersebut. Dua pengaturan SPIRE harus sepakat pada URL yang sama: `jwt_issuer` milik SPIRE Server (yang menjadi klaim `iss` di setiap JWT-SVID yang dicetak) dan daftar `domains` milik OIDC Discovery Provider (yang menentukan host tempat dokumen discovery dan JWKS disajikan). URL bersama itulah yang Anda daftarkan ke Anthropic.

Trust domain dan URL issuer bersifat independen. Trust domain (`spiffe://prod.example.com`) membatasi cakupan klaim `sub`. URL issuer (`https://oidc-discovery.prod.example.com`) adalah tempat Anthropic mengambil kunci penandatanganan. Keduanya tidak perlu berbagi hostname.

Pastikan `jwt_issuer` diatur dalam konfigurasi SPIRE Server dan mengarah ke URL publik discovery provider. Contoh berikut juga menampilkan masa berlaku JWT-SVID default. Default bawaan SPIRE adalah 5 menit, yang cukup singkat sehingga rotasi berkelanjutan diperlukan (lihat [Menjalankan spiffe-helper](https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe#run-spiffe-helper)). Endpoint token-exchange Anthropic menolak token identitas apa pun yang masa berlakunya melebihi maksimum yang dikonfigurasi pada federation issuer, yaitu 1 jam secara default (lihat [Aturan validasi](https://platform.claude.com/docs/id/manage-claude/wif-reference#validation-rules)). Pemeriksaan ini berlaku untuk setiap implementasi SPIFFE, bukan hanya SPIRE, jadi pertahankan `default_jwt_svid_ttl` (atau override per-entry apa pun) pada atau di bawah maksimum tersebut.

```text server.conf
server {
    trust_domain         = "prod.example.com"
    jwt_issuer           = "https://oidc-discovery.prod.example.com"
    default_jwt_svid_ttl = "5m"
    # ...
}
```

Dalam konfigurasi OIDC Discovery Provider, hostname yang sama harus muncul di bawah `domains`, dan provider harus dapat menjangkau socket API milik SPIRE Server. Provider menyajikan dokumen discovery dan JWKS melalui HTTPS. Terminasi TLS dengan dukungan ACME bawaannya, atau tempatkan di belakang load balancer yang melakukannya.

```text oidc-discovery-provider.conf
domains = ["oidc-discovery.prod.example.com"]

server_api {
    address = "unix:///run/spire/sockets/private/api.sock"
}

acme {
    email        = "platform@example.com"
    tos_accepted = true
}
```

<Note>
  Contoh ini menggunakan `server_api`, yang menghubungkan discovery provider ke socket API berprivilese milik SPIRE Server. Provider juga menerima blok `workload_api` (dengan `socket_path` dan `trust_domain`) yang memperoleh bundle melalui Workload API milik SPIRE Agent sebagai gantinya. Gunakan ini ketika discovery provider tidak boleh memiliki akses ke Server API atau berjalan di node yang tidak dapat menjangkau Server.
</Note>

### Mendaftarkan workload

Setiap workload yang memanggil Claude API memerlukan registration entry SPIRE yang memetakan selector runtime-nya ke sebuah SPIFFE ID. Jika workload sudah terdaftar, catat SPIFFE ID-nya, yang Anda gunakan di `subject_prefix` pada federation rule. Jika belum, daftarkan. Untuk pod Kubernetes, selector-nya biasanya adalah namespace dan service account Kubernetes:

```bash CLI
# Ganti NODE_UID dengan UID node:
#   kubectl get node <node-name> -o jsonpath='{.metadata.uid}'
spire-server entry create \
    -spiffeID spiffe://prod.example.com/ns/inference/sa/worker \
    -parentID spiffe://prod.example.com/spire/agent/k8s_psat/prod-cluster/NODE_UID \
    -selector k8s:ns:inference \
    -selector k8s:sa:worker
```

<Note>
  `parentID` yang ditampilkan adalah agent ID yang dihasilkan otomatis untuk satu node. Untuk pendaftaran di seluruh cluster, jadikan entry tersebut anak dari sebuah [node alias](https://spiffe.io/docs/latest/deploying/registering/#mapping-workloads-to-multiple-nodes) agar cocok dengan workload di setiap node, seperti yang dilakukan [SPIRE Kubernetes quickstart](https://spiffe.io/docs/latest/try/getting-started-k8s/).
</Note>

Workload di luar Kubernetes menggunakan selector tingkat host seperti `unix:uid:1000` (`unix:path` juga tersedia tetapi memerlukan `discover_workload_path = true` dalam konfigurasi unix workload attestor milik agent). Cluster yang menjalankan [spire-controller-manager](https://github.com/spiffe/spire-controller-manager) dapat mendeklarasikan entry dengan custom resource `ClusterSPIFFEID` alih-alih memanggil `spire-server entry create` secara langsung.

### Menjalankan spiffe-helper

[spiffe-helper](https://github.com/spiffe/spiffe-helper) adalah utilitas sidecar yang terhubung ke socket SPIRE Agent, mengambil JWT-SVID untuk audience tertentu, menuliskannya ke file, dan mengambilnya kembali sebelum kedaluwarsa. Helper ini berjalan dalam mode daemon secara default. Contoh berikut mengatur `daemon_mode = true` secara eksplisit.

```text helper.conf
agent_address = "/run/spire/sockets/agent.sock"
# The JWT-SVID file is written under cert_dir
cert_dir      = "/var/run/secrets/anthropic.com"
daemon_mode   = true

jwt_svids = [{
    jwt_audience       = "https://api.anthropic.com"
    jwt_svid_file_name = "token"
}]
```

Di Kubernetes, jalankan spiffe-helper sebagai container sidecar yang berbagi volume `emptyDir` berbasis memori (`medium: Memory`) dengan container aplikasi Anda sehingga bearer SVID tidak pernah tersimpan di disk node. Mount socket SPIRE Agent dari host ke dalam sidecar, mount volume bersama di `/var/run/secrets/anthropic.com` pada kedua container, dan atur `ANTHROPIC_IDENTITY_TOKEN_FILE=/var/run/secrets/anthropic.com/token` pada container aplikasi. Pada VM dan bare metal, jalankan spiffe-helper sebagai layanan sistem di samping workload dan arahkan keduanya ke direktori bersama.

## Konfigurasi Anthropic

Di Claude Console, buka **Settings → Workload identity**, klik **Connect workload**, dan pilih **Custom OIDC**. Wizard akan memandu Anda mendaftarkan issuer, membuat service account, dan membuat federation rule.

Wizard membuat sumber daya ini untuk Anda. Gunakan nilai-nilai berikut, baik Anda memasukkannya di wizard maupun mengirimkannya ke [Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api):

**Federation issuer:** Daftarkan URL publik OIDC Discovery Provider dalam mode `discovery`. Anthropic mengambil `/.well-known/openid-configuration` dari URL ini dan mengikuti `jwks_uri` yang dikembalikan untuk mengambil kunci penandatanganan milik trust domain.

```json
{
  "name": "spire-prod",
  "issuer_url": "https://oidc-discovery.prod.example.com",
  "jwks": { "type": "discovery" }
}
```

Jika discovery provider tidak dapat dijangkau dari internet publik, ambil JWKS sendiri (`curl https://oidc-discovery.prod.example.com/keys`) dan daftarkan issuer dengan `"jwks": {"type": "inline", "keys": [...]}` menggunakan isi array `keys` yang dikembalikan. Dalam mode `inline`, `issuer_url` hanya dibandingkan dengan klaim `iss` pada JWT-SVID. Anthropic tidak pernah mencoba menjangkaunya.

<Warning>
  SPIRE sering merotasi kunci penandatanganan JWT, secara default dengan irama yang sama dengan CA (`ca_ttl`, 24 jam). Jika Anda mendaftarkan issuer dengan JWKS inline alih-alih URL discovery, Anda harus memperbarui JWKS setiap kali SPIRE melakukan rotasi: tambahkan kunci baru sebelum workload mulai menyajikannya, dan **hapus kunci yang sudah digantikan** setelah token yang ditandatangani dengannya kedaluwarsa. Kunci usang yang tertinggal di JWKS inline tetap dipercaya tanpa batas waktu.
</Warning>

Untuk mengotomatiskan pembaruan JWKS tanpa mengekspos endpoint discovery publik, konfigurasikan plugin [BundlePublisher](https://spiffe.io/docs/latest/deploying/spire_server/#built-in-plugins) SPIRE Server (`aws_s3`, `gcp_cloudstorage`, atau `k8s_configmap`) dengan `format = "jwks"` untuk mendorong kunci penandatanganan JWT ke penyimpanan eksternal pada setiap rotasi, lalu perbarui kunci inline milik issuer melalui [Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#federation-issuers).

**Federation rule:** Cocokkan `sub` pada JWT-SVID (SPIFFE ID) dan `aud` yang Anda konfigurasikan untuk diminta oleh spiffe-helper. SPIFFE ID adalah string URI dan `subject_prefix` mencocokkannya sebagai teks opak, sehingga nilai persis maupun pencocokan prefiks dengan `*` di akhir sama-sama berfungsi. Untuk pola yang lebih kompleks, gunakan `condition` CEL.

```json
{
  "name": "spire-inference-worker",
  "issuer_id": "fdis_...",
  "match": {
    "subject_prefix": "spiffe://prod.example.com/ns/inference/sa/worker",
    "audience": "https://api.anthropic.com"
  },
  "target": {
    "type": "service_account",
    "service_account_id": "svac_..."
  },
  "workspace_id": "wrkspc_...",
  "oauth_scope": "workspace:developer",
  "token_lifetime_seconds": 600
}
```

`token_lifetime_seconds` adalah masa berlaku access token Anthropic yang dikembalikan oleh exchange, bukan masa berlaku JWT-SVID. SDK memperbarui access token secara otomatis.

Buatlah sespesifik yang dimungkinkan oleh workload. Longgarkan `subject_prefix` menjadi `spiffe://prod.example.com/ns/inference/*` hanya jika setiap workload yang terdaftar di bawah path tersebut harus dipetakan ke service account Anthropic yang sama. Tambahkan ID `fdrl_...` milik aturan ke variabel lingkungan `ANTHROPIC_FEDERATION_RULE_ID` pada workload.

## Memperoleh dan menggunakan token

SDK Anthropic dapat membaca JWT-SVID dari file yang dikelola spiffe-helper atau memanggil SPIFFE Workload API secara langsung melalui callable penyedia token. Jalur file adalah integrasi paling sederhana dan berfungsi di setiap bahasa SDK. Jalur callable menghilangkan sidecar tetapi memerlukan klien SPIFFE Workload API dalam bahasa aplikasi Anda.

<Tabs>
  <Tab title="Berbasis file dengan spiffe-helper">
    Dengan spiffe-helper menulis JWT-SVID baru ke `/var/run/secrets/anthropic.com/token`, atur `ANTHROPIC_IDENTITY_TOKEN_FILE` ke path tersebut bersama dengan `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, dan `ANTHROPIC_WORKSPACE_ID`. SDK membaca file tersebut pada setiap token exchange, sehingga selalu mengambil SVID yang paling baru dirotasi, dan memperbarui access token Anthropic secara otomatis sebelum kedaluwarsa. Lihat [Variabel lingkungan](https://platform.claude.com/docs/id/manage-claude/wif-reference#environment-variables) untuk mengetahui asal setiap nilai.

    <CodeGroup>
      ```bash cURL
      JWT=$(cat "$ANTHROPIC_IDENTITY_TOKEN_FILE")

      ACCESS_TOKEN=$(curl -sS https://api.anthropic.com/v1/oauth/token \
        -H "content-type: application/json" \
        --data @- <<JSON | jq -r .access_token
      {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": "$JWT",
        "federation_rule_id": "$ANTHROPIC_FEDERATION_RULE_ID",
        "organization_id": "$ANTHROPIC_ORGANIZATION_ID",
        "service_account_id": "$ANTHROPIC_SERVICE_ACCOUNT_ID",
        "workspace_id": "$ANTHROPIC_WORKSPACE_ID"
      }
      JSON
      )

      curl https://api.anthropic.com/v1/messages \
        -H "authorization: Bearer $ACCESS_TOKEN" \
        -H "anthropic-version: 2023-06-01" \
        -H "content-type: application/json" \
        -d '{
          "model": "claude-opus-5",
          "max_tokens": 1024,
          "messages": [{"role": "user", "content": "Hello, Claude"}]
        }' | jq -r '.content[] | select(.type == "text") | .text'
      ```

      ```bash CLI
      # Membaca JWT-SVID yang ditulis spiffe-helper ke
      # ANTHROPIC_IDENTITY_TOKEN_FILE, ditambah ANTHROPIC_FEDERATION_RULE_ID,
      # ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID.
      ant messages create \
        --model claude-opus-5 \
        --max-tokens 1024 \
        --message '{role: user, content: "Hello, Claude"}'
      ```

      ```python Python
      import anthropic

      # Membaca JWT-SVID yang ditulis spiffe-helper ke
      # ANTHROPIC_IDENTITY_TOKEN_FILE, ditambah ANTHROPIC_FEDERATION_RULE_ID,
      # ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID.
      client = anthropic.Anthropic()

      message = client.messages.create(
          model="claude-opus-5",
          max_tokens=1024,
          messages=[{"role": "user", "content": "Hello, Claude"}],
      )
      print(next(block.text for block in message.content if block.type == "text"))
      ```

      ```typescript TypeScript
      import Anthropic from "@anthropic-ai/sdk";

      // Membaca JWT-SVID yang ditulis spiffe-helper ke
      // ANTHROPIC_IDENTITY_TOKEN_FILE, serta ANTHROPIC_FEDERATION_RULE_ID,
      // ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID.
      const client = new Anthropic();

      const message = await client.messages.create({
        model: "claude-opus-5",
        max_tokens: 1024,
        messages: [{ role: "user", content: "Hello, Claude" }]
      });
      for (const block of message.content) {
        if (block.type === "text") {
          console.log(block.text);
        }
      }
      ```

      ```csharp C#
      // Membaca JWT-SVID yang ditulis spiffe-helper ke
      // ANTHROPIC_IDENTITY_TOKEN_FILE, ditambah ANTHROPIC_FEDERATION_RULE_ID,
      // ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID.
      using var client = new AnthropicClient();

      var message = await client.Messages.Create(new()
      {
          Model = Model.ClaudeOpus5,
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],
      });
      foreach (var block in message.Content)
      {
          if (block.Value is TextBlock textBlock)
          {
              Console.WriteLine(textBlock.Text);
          }
      }
      ```

      ```go Go
      // Membaca JWT-SVID yang ditulis spiffe-helper ke
      // ANTHROPIC_IDENTITY_TOKEN_FILE, serta ANTHROPIC_FEDERATION_RULE_ID,
      // ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID.
      client := anthropic.NewClient()

      message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus5,
      	MaxTokens: 1024,
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
      	},
      })
      if err != nil {
      	panic(err)
      }
      for _, block := range message.Content {
      	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
      		fmt.Println(textBlock.Text)
      		break
      	}
      }
      ```

      ```java Java
      // Membaca JWT-SVID yang ditulis spiffe-helper ke
      // ANTHROPIC_IDENTITY_TOKEN_FILE, serta ANTHROPIC_FEDERATION_RULE_ID,
      // ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID.
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var message = client.messages().create(MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5)
              .maxTokens(1024)
              .addUserMessage("Hello, Claude")
              .build());

      IO.println(message.content());
      ```

      ```php PHP
      use Anthropic\Client;

      // Membaca JWT-SVID yang ditulis spiffe-helper ke
      // ANTHROPIC_IDENTITY_TOKEN_FILE, ditambah ANTHROPIC_FEDERATION_RULE_ID,
      // ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID.
      $client = new Client();

      $message = $client->messages->create(
          model: 'claude-opus-5',
          maxTokens: 1024,
          messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      );
      $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
      echo $textBlock->text, PHP_EOL;
      ```

      ```ruby Ruby
      require "anthropic"

      # Membaca JWT-SVID yang ditulis spiffe-helper ke
      # ANTHROPIC_IDENTITY_TOKEN_FILE, ditambah ANTHROPIC_FEDERATION_RULE_ID,
      # ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID.
      client = Anthropic::Client.new

      message = client.messages.create(
        model: "claude-opus-5",
        max_tokens: 1024,
        messages: [{role: "user", content: "Hello, Claude"}]
      )
      puts message.content.find { it.type == :text }.text
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Callable melalui SPIFFE Workload API">
    Workload yang menautkan klien SPIFFE Workload API secara langsung dapat melewati spiffe-helper dan memberikan SDK sebuah callable yang mengambil JWT-SVID baru dari socket agent. SDK memanggil callable tersebut sebelum setiap token exchange, sehingga workload selalu menyajikan SVID yang belum kedaluwarsa. Python ([py-spiffe](https://github.com/HewlettPackard/py-spiffe)) dan Go ([go-spiffe](https://github.com/spiffe/go-spiffe)) memiliki klien Workload API yang matang.

    <CodeGroup exclude="shell, typescript, java, csharp, php, ruby">
      ```python Python
      import os
      import anthropic
      from anthropic import WorkloadIdentityCredentials
      from spiffe import JwtSource

      AUDIENCE = "https://api.anthropic.com"

      # Terhubung ke socket SPIRE Agent di SPIFFE_ENDPOINT_SOCKET.
      jwt_source = JwtSource()


      def fetch_jwt_svid() -> str:
          svid = jwt_source.fetch_svid(audience={AUDIENCE})  # audience is a set of strings
          return svid.token


      client = anthropic.Anthropic(
          credentials=WorkloadIdentityCredentials(
              identity_token_provider=fetch_jwt_svid,
              federation_rule_id=os.environ["ANTHROPIC_FEDERATION_RULE_ID"],
              organization_id=os.environ["ANTHROPIC_ORGANIZATION_ID"],
              service_account_id=os.environ["ANTHROPIC_SERVICE_ACCOUNT_ID"],
              workspace_id=os.environ.get("ANTHROPIC_WORKSPACE_ID"),
          ),
      )

      message = client.messages.create(
          model="claude-opus-5",
          max_tokens=1024,
          messages=[{"role": "user", "content": "Hello, Claude"}],
      )
      print(next(block.text for block in message.content if block.type == "text"))
      ```

      ```go Go
      import (
      	"context"
      	"fmt"
      	"os"

      	"github.com/anthropics/anthropic-sdk-go"
      	"github.com/anthropics/anthropic-sdk-go/option"
      	"github.com/spiffe/go-spiffe/v2/svid/jwtsvid"
      	"github.com/spiffe/go-spiffe/v2/workloadapi"
      )
      // ...
      	const audience = "https://api.anthropic.com"

      	ctx := context.Background()
      	source, err := workloadapi.NewJWTSource(ctx)
      	if err != nil {
      		panic(err)
      	}
      	defer source.Close()

      	fetchJWTSVID := func(ctx context.Context) (string, error) {
      		svid, err := source.FetchJWTSVID(ctx, jwtsvid.Params{Audience: audience})
      		if err != nil {
      			return "", err
      		}
      		return svid.Marshal(), nil
      	}

      	client := anthropic.NewClient(
      		option.WithFederationTokenProvider(fetchJWTSVID, option.FederationOptions{
      			FederationRuleID: os.Getenv("ANTHROPIC_FEDERATION_RULE_ID"),
      			OrganizationID:   os.Getenv("ANTHROPIC_ORGANIZATION_ID"),
      			ServiceAccountID: os.Getenv("ANTHROPIC_SERVICE_ACCOUNT_ID"),
      			WorkspaceID:      os.Getenv("ANTHROPIC_WORKSPACE_ID"),
      		}),
      	)

      	message, err := client.Messages.New(ctx, anthropic.MessageNewParams{
      		Model:     anthropic.ModelClaudeOpus5,
      		MaxTokens: 1024,
      		Messages: []anthropic.MessageParam{
      			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
      		},
      	})
      	if err != nil {
      		panic(err)
      	}
      	for _, block := range message.Content {
      		if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
      			fmt.Println(textBlock.Text)
      			break
      		}
      	}
      ```
    </CodeGroup>

    <Note>
      Untuk bahasa lain, ambil JWT-SVID dengan klien SPIFFE Workload API milik runtime Anda (atau jalankan `spire-agent api fetch jwt` melalui shell), tuliskan ke file, dan atur `ANTHROPIC_IDENTITY_TOKEN_FILE` ke path tersebut seperti pada tab berbasis file.
    </Note>
  </Tab>
</Tabs>

## Verifikasi penyiapan

Sebelum menghubungkan SDK, ambil JWT-SVID langsung dari SPIRE Agent dan pastikan klaim-klaimnya cocok dengan yang diharapkan federation rule Anda. Jika Anda menggunakan implementasi SPIFFE yang berbeda, ambil JWT-SVID dengan CLI atau klien Workload API-nya dan dekode payload dengan cara yang sama.

<Note>
  Workload API melakukan atestasi terhadap proses pemanggil. Untuk registration entry Kubernetes, jalankan perintah ini di dalam pod yang memenuhi selector entry tersebut dan memiliki socket agent yang ter-mount (misalnya, dengan menggunakan `kubectl exec`). Pada VM dan bare metal, jalankan sebagai pengguna atau proses yang cocok dengan selector `unix:` milik entry. Menjalankannya dari shell host yang tidak teratestasi akan mengembalikan `no identity issued`, yang merupakan kegagalan langkah verifikasi paling umum.
</Note>

```bash CLI
spire-agent api fetch jwt \
    -audience https://api.anthropic.com \
    -socketPath /run/spire/sockets/agent.sock \
    -output json \
  | jq -r '.[0].svids[0].svid' \
  | jq -rR 'split(".")[1] | gsub("-";"+") | gsub("_";"/") | @base64d | fromjson'
```

Flag `-output json` mengembalikan respons SVID dan respons bundle sebagai array JSON dua elemen, sehingga `jq -r '.[0].svids[0].svid'` mengekstrak token mentahnya. Pada versi SPIRE lama tanpa `-output`, perintah tersebut mencetak blok berlabel sebagai gantinya. Dalam kasus itu, salurkan output default melalui `awk '/^[[:space:]]*eyJ/{print $1; exit}'` untuk mengekstrak baris token. Periksa bahwa `iss` adalah URL OIDC Discovery Provider yang Anda daftarkan, `sub` adalah SPIFFE ID milik workload, dan `aud` berisi `https://api.anthropic.com`. Kemudian jalankan contoh cURL dari [Memperoleh dan menggunakan token](https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe#acquire-and-use-the-token). Exchange yang berhasil mengembalikan `access_token` yang diawali dengan `sk-ant-oat01-`. Jika exchange gagal dengan respons opak `401` `authentication_error` (pesan `Authentication failed`), periksa [halaman riwayat autentikasi](https://platform.claude.com/settings/workload-identity-federation?tab=history) untuk alasan penolakan dan lihat [Memecahkan masalah exchange yang gagal](https://platform.claude.com/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange). Penyebab paling umum di sisi SPIRE adalah ketidakcocokan antara `jwt_issuer` milik SPIRE Server dan URL yang didaftarkan sebagai federation issuer.

## Membatasi cakupan aturan Anda

Konvensi path SPIFFE ID ditentukan oleh operator, sehingga matcher `subject_prefix` pada federation rule harus mencerminkan skema path yang digunakan registration entry Anda. Skema umum mencakup `spiffe://<trust-domain>/ns/<namespace>/sa/<service-account>` (default yang dihasilkan oleh resource `ClusterSPIFFEID` di spire-controller-manager) dan `spiffe://<trust-domain>/host/<hostname>/<service>` untuk workload VM dan bare-metal.

<Warning>
  `subject_prefix` berupa `spiffe://prod.example.com/*` cocok dengan setiap workload di trust domain. Tanpa matcher `audience`, aturan tersebut juga menerima JWT-SVID yang dicetak untuk audience apa pun, termasuk yang diminta workload untuk relying party yang tidak terkait.
</Warning>

Kunci blok `match` pada aturan ke cakupan tersempit yang sesuai dengan kasus penggunaan Anda:

* **Sematkan ke satu workload:** Atur `subject_prefix` ke SPIFFE ID lengkap tanpa `*` di akhir.
* **Selalu atur audience:** Wajibkan `audience` pada aturan dan konfigurasikan spiffe-helper (atau panggilan Workload API) dengan nilai yang sama sehingga SVID yang dicetak untuk relying party lain ditolak.
* **Batasi cakupan berdasarkan segmen path:** Gunakan `spiffe://prod.example.com/ns/inference/*` untuk memberi akses kepada setiap workload yang terdaftar di bawah sebuah namespace, dan buat aturan serta service account Anthropic terpisah per namespace alih-alih memperluas satu aturan.
* **Satu issuer per trust domain:** Setiap trust domain SPIRE memiliki kunci penandatanganan dan OIDC Discovery Provider sendiri. Daftarkan masing-masing sebagai federation issuer terpisah dan ikat aturan ke issuer yang memiliki SPIFFE ID yang dicocokkannya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Menggunakan WIF dengan Okta" icon="lock" href="https://platform.claude.com/docs/id/manage-claude/wif-providers/okta">
    Federasikan identitas aplikasi layanan Okta ke Claude API dengan Workload Identity Federation.
  </Card>

  <Card title="Workload Identity Federation" icon="cloud" href="https://platform.claude.com/docs/id/manage-claude/workload-identity-federation">
    Autentikasi workload ke Claude API dengan token identitas berumur pendek dari penyedia identitas Anda sendiri alih-alih kunci API statis berumur panjang.
  </Card>

  <Card title="Referensi WIF" icon="book" href="https://platform.claude.com/docs/id/manage-claude/wif-reference">
    Variabel lingkungan, aturan validasi, konfigurasi profil, dan referensi error untuk Workload Identity Federation.
  </Card>

  <Card title="Menggunakan WIF dengan Kubernetes" icon="cube" href="https://platform.claude.com/docs/id/manage-claude/wif-providers/kubernetes">
    Autentikasi ke Claude API dari cluster Kubernetes yang dikelola sendiri menggunakan projected service account token.
  </Card>
</CardGroup>
