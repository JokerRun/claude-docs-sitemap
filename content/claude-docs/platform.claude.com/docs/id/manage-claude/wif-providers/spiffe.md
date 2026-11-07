---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe
fetched_at: 2026-11-07T02:12:06.793583Z
sha256: b0bd3ccf7f974aeff36efd1919bfcb1937c2fa0428400d120a547908a302c106
---

---
title: Menggunakan WIF dengan SPIFFE
url: https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe
description: Autentikasi workload SPIFFE ke Claude API menggunakan JWT-SVID dari SPIRE atau penerbit lain yang sesuai dengan SPIFFE.
---

[SPIFFE](https://spiffe.io/) adalah standar CNCF untuk menerbitkan identitas bagi workload. [SPIRE](https://spiffe.io/docs/latest/spire-about/) adalah implementasi referensi open-source-nya, dan beberapa produk komersial juga menerbitkan identitas yang sesuai dengan SPIFFE. Anthropic melakukan federasi dengan implementasi SPIFFE apa pun yang menghasilkan JWT-SVID yang kompatibel dengan OIDC. Untuk daftar implementasi, lihat [Commercial software that implements SPIFFE](https://spiffe.io/docs/latest/spiffe-about/overview/#commercial-software-that-implements-spiffe) di situs proyek SPIFFE.

Dalam mode `discovery`, Anthropic membaca dokumen discovery OIDC di URL HTTPS publik, tunduk pada batasan di [Field URL](https://platform.claude.com/docs/id/manage-claude/wif-reference#url-fields). Dalam mode `inline`, Anda mendaftarkan “JSON Web Key Set” (set kunci web JSON), atau JWKS, secara langsung.

Spesifikasi JWT-SVID mendefinisikan `sub` sebagai SPIFFE ID milik workload, dan SPIFFE Workload API mengharuskan pemanggil menyediakan `aud` pada saat pengambilan. Oleh karena itu, klaim-klaim tersebut sama di semua implementasi. Anthropic juga mewajibkan `iss` dan `iat`, dan keduanya tidak diwajibkan oleh spesifikasi JWT-SVID, jadi konfigurasikan implementasi Anda untuk mengisi keduanya. Di SPIRE, `iss` adalah pengaturan server `jwt_issuer`, dan SPIRE mengatur `iat` secara otomatis. Dengan semua itu terpenuhi, bagian [Konfigurasi Anthropic](https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe#configure-anthropic), [Memperoleh dan menggunakan token](https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe#acquire-and-use-the-token), dan [Membatasi cakupan aturan Anda](https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe#scope-your-rule) dalam panduan ini berlaku untuk implementasi SPIFFE apa pun.

SPIFFE memberikan setiap workload sebuah URI identitas yang stabil dengan bentuk `spiffe://<trust-domain>/<path>`, dan SPIRE menerbitkan identitas tersebut sebagai JWT-SVID sesuai permintaan melalui Workload API. JWT-SVID adalah “JSON Web Token” (token web JSON), atau JWT, bertanda tangan biasa.

[SPIRE OIDC Discovery Provider](https://github.com/spiffe/spire/blob/main/support/oidc-discovery-provider/README.md) menghubungkan trust domain SPIRE ke OIDC standar. Helper mandiri ini memublikasikan `/.well-known/openid-configuration` dan endpoint JWKS untuk kunci penandatanganan JWT milik trust domain. Dengan discovery provider berjalan, JWT-SVID divalidasi seperti token OIDC lainnya. Daftarkan URL discovery sebagai federation issuer (penerbit federasi) dan tulis federation rule (aturan federasi) yang cocok dengan SPIFFE ID milik workload. Kemudian minta workload menyajikan JWT-SVID-nya ke endpoint token-exchange Anthropic.

Contoh-contoh di halaman ini menggunakan SPIRE dan berlaku di mana pun SPIRE Agent berjalan: pod Kubernetes, mesin virtual, dan host bare-metal.

<Note>
  Jika klaster Kubernetes Anda tidak menjalankan SPIRE dan Anda ingin mengautentikasi dengan token akun layanan terproyeksi bawaan klaster, lihat [Menggunakan WIF dengan Kubernetes](https://platform.claude.com/docs/id/manage-claude/wif-providers/kubernetes).
</Note>

## Prasyarat

* Pemahaman tentang [konsep Workload Identity Federation (WIF)](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#concepts): service account, federation issuer, dan federation rule.
* Deployment SPIFFE dengan identitas workload yang telah diterbitkan, serta registration entry untuk workload yang perlu memanggil Claude API. Contoh di halaman ini menggunakan SPIRE Server dan Agent.
* Endpoint discovery OIDC untuk trust domain (di SPIRE, [OIDC Discovery Provider](https://github.com/spiffe/spire/blob/main/support/oidc-discovery-provider/README.md)) yang berjalan dengan endpoint HTTPS yang dapat dijangkau secara publik, atau JWKS yang diekspor untuk pendaftaran `inline`.
* Penerbit SPIFFE Anda dikonfigurasi untuk mengatur klaim `iss` pada JWT-SVID ke nilai yang Anda daftarkan sebagai `issuer_url` milik federation issuer. Untuk mode `discovery`, ini adalah URL publik endpoint discovery (di SPIRE, pengaturan server `jwt_issuer`).
* JWT-SVID tersedia bagi workload Anda. WIF hanya menerima JWT-SVID, bukan X.509-SVID.
* Izin untuk membuat service account, federation issuer, dan federation rule di Claude Console untuk organisasi Anthropic Anda.

Nilai audience yang diminta saat mengambil JWT-SVID selalu `https://api.anthropic.com`. Gunakan nilai ini di `jwt_audience` milik spiffe-helper, panggilan Workload API `FetchJWTSVID`, dan matcher `audience` pada federation rule.

## Konfigurasi SPIRE

Instruksi di bagian ini khusus untuk SPIRE. Jika Anda menggunakan penerbit SPIFFE yang berbeda, konfigurasikan endpoint discovery OIDC dan pengambilan JWT-SVID-nya sesuai dokumentasinya sendiri, lalu lanjutkan ke [Konfigurasi Anthropic](https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe#configure-anthropic).

Jika Anda sudah menjalankan SPIRE dengan OIDC Discovery Provider, federasi dengan Anthropic memerlukan tiga hal di sisi SPIRE:

* `jwt_issuer` yang cocok dengan URL discovery
* Entri registrasi untuk workload yang memanggil Claude API
* Cara bagi workload tersebut untuk mengambil JWT-SVID dengan audience Anthropic

Subbagian berikut membahas masing-masing. Cuplikan konfigurasi hanya menampilkan pengaturan yang relevan dengan federasi Anthropic, bukan konfigurasi deployment SPIRE yang lengkap.

<Tip>
  Baru pertama kali menyiapkan SPIRE? Deploy SPIRE Server dan Agent dengan mengikuti [panduan mulai cepat SPIRE](https://spiffe.io/docs/latest/try/), lalu tambahkan [OIDC Discovery Provider](https://github.com/spiffe/spire/blob/main/support/oidc-discovery-provider/README.md) sebagai layanan terpisah di samping SPIRE Server. Federasi mode discovery bergantung pada provider yang telah di-deploy dan dapat dijangkau secara publik. Provider ini bukan bagian dari instalasi SPIRE default.
</Tip>

### Verifikasi JWT issuer

Anthropic memvalidasi JWT-SVID dengan mencocokkan klaim `iss`-nya terhadap penerbit federasi yang terdaftar dan mengambil JWKS dari dokumen discovery milik issuer tersebut. Dua pengaturan SPIRE harus sepakat pada URL yang sama. `jwt_issuer` milik SPIRE Server menjadi klaim `iss` di setiap JWT-SVID yang diterbitkan. Daftar `domains` milik OIDC Discovery Provider menentukan host yang menyajikan dokumen discovery dan JWKS. URL bersama itulah yang Anda daftarkan ke Anthropic.

Trust domain dan URL issuer bersifat independen. Trust domain (`spiffe://prod.example.com`) membatasi cakupan klaim `sub`. URL issuer (`https://oidc-discovery.prod.example.com`) adalah tempat Anthropic mengambil kunci penandatanganan. Keduanya tidak perlu berbagi hostname.

Pastikan `jwt_issuer` diatur dalam konfigurasi SPIRE Server dan mengarah ke URL publik discovery provider. Contoh berikut juga menampilkan masa berlaku JWT-SVID default. Default bawaan SPIRE adalah 5 menit, yang cukup singkat sehingga memerlukan rotasi berkelanjutan (lihat [Menjalankan spiffe-helper](https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe#run-spiffe-helper)). Endpoint token-exchange Anthropic menolak token identitas apa pun yang masa berlakunya melebihi maksimum yang dikonfigurasi pada federation issuer, yaitu 1 jam secara default (lihat [Aturan validasi](https://platform.claude.com/docs/id/manage-claude/wif-reference#validation-rules)). Pemeriksaan ini berlaku untuk setiap implementasi SPIFFE, bukan hanya SPIRE, jadi pertahankan `default_jwt_svid_ttl` (atau override apa pun pada entri registrasi) pada atau di bawah maksimum tersebut.

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

Setiap workload yang memanggil Claude API memerlukan entri registrasi SPIRE yang memetakan selector runtime-nya ke sebuah SPIFFE ID. Jika workload sudah terdaftar, catat SPIFFE ID-nya, yang Anda gunakan di `subject_prefix` pada aturan federasi. Jika belum, daftarkan. Untuk pod Kubernetes, selector-nya biasanya adalah namespace dan akun layanan Kubernetes:

```bash
# Ganti NODE_UID dengan UID node:
#   kubectl get node <node-name> -o jsonpath='{.metadata.uid}'
spire-server entry create \
  -spiffeID spiffe://prod.example.com/ns/inference/sa/worker \
  -parentID spiffe://prod.example.com/spire/agent/k8s_psat/prod-cluster/NODE_UID \
  -selector k8s:ns:inference \
  -selector k8s:sa:worker
```

<Note>
  `parentID` yang ditampilkan adalah agent ID yang dihasilkan otomatis untuk satu node. Untuk pendaftaran di seluruh klaster, jadikan entri tersebut anak dari sebuah [alias node](https://spiffe.io/docs/latest/deploying/registering/#mapping-workloads-to-multiple-nodes) agar cocok dengan workload di setiap node, seperti yang dilakukan [panduan mulai cepat SPIRE untuk Kubernetes](https://spiffe.io/docs/latest/try/getting-started-k8s/).
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

Di Kubernetes, jalankan spiffe-helper sebagai container sidecar yang berbagi volume `emptyDir` berbasis memori (`medium: Memory`) dengan container aplikasi Anda. Dengan begitu, bearer SVID tidak pernah mencapai disk node. Mount socket SPIRE Agent dari host ke dalam sidecar, mount volume bersama di `/var/run/secrets/anthropic.com` pada kedua container, dan atur `ANTHROPIC_IDENTITY_TOKEN_FILE=/var/run/secrets/anthropic.com/token` pada container aplikasi. Pada VM dan bare metal, jalankan spiffe-helper sebagai layanan sistem di samping workload dan arahkan keduanya ke direktori bersama.

## Konfigurasi Anthropic

Di Claude Console, buka halaman [Identitas beban kerja](https://platform.claude.com/settings/workload-identity-federation) (`platform.claude.com/settings/workload-identity-federation`), klik **Hubungkan beban kerja**, dan pilih **Custom OIDC**. Wizard akan memandu Anda mendaftarkan issuer, membuat akun layanan, dan membuat aturan federasi.

Wizard membuat sumber daya ini untuk Anda. Gunakan nilai-nilai berikut, baik Anda memasukkannya di wizard maupun mengirimkannya ke [Admin API](https://platform.claude.com/docs/id/manage-claude/wif-admin-api):

**Penerbit federasi:** Daftarkan URL publik OIDC Discovery Provider dalam mode `discovery`. Anthropic mengambil `/.well-known/openid-configuration` dari URL ini dan mengikuti `jwks_uri` yang dikembalikan untuk mengambil kunci penandatanganan milik trust domain.

```json
{
  "name": "spire-prod",
  "issuer_url": "https://oidc-discovery.prod.example.com",
  "jwks": { "type": "discovery" }
}
```

Jika discovery provider tidak dapat dijangkau dari internet publik, ambil JWKS sendiri (`curl https://oidc-discovery.prod.example.com/keys`). Kemudian daftarkan issuer dengan `"jwks": {"type": "inline", "keys": [...]}`, menggunakan isi array `keys` yang dikembalikan. Dalam mode `inline`, Anthropic hanya membandingkan `issuer_url` dengan klaim `iss` pada JWT-SVID dan tidak pernah mencoba menjangkaunya.

<Warning>
  SPIRE sering merotasi kunci penandatanganan JWT, secara default dengan jadwal yang sama dengan CA (`ca_ttl`, 24 jam). Jika Anda mendaftarkan issuer dengan JWKS inline alih-alih URL discovery, Anda harus memperbarui JWKS setiap kali SPIRE melakukan rotasi. Tambahkan kunci baru sebelum workload mulai menyajikannya, dan **hapus kunci yang sudah digantikan** setelah token yang ditandatangani dengannya kedaluwarsa. Kunci usang yang tertinggal di JWKS inline tetap dipercaya tanpa batas waktu.
</Warning>

Untuk mengotomatiskan pembaruan JWKS tanpa mengekspos endpoint discovery publik, konfigurasikan plugin [BundlePublisher](https://spiffe.io/docs/latest/deploying/spire_server/#built-in-plugins) SPIRE Server (`aws_s3`, `gcp_cloudstorage`, atau `k8s_configmap`) dengan `format = "jwks"`. Plugin ini mendorong kunci penandatanganan JWT ke penyimpanan eksternal pada setiap rotasi. Kemudian perbarui kunci inline milik issuer melalui Admin API. Lihat [Penerbit federasi](https://platform.claude.com/docs/id/manage-claude/wif-admin-api#federation-issuers).

**Aturan federasi:** Cocokkan `sub` pada JWT-SVID (SPIFFE ID) dan `aud` yang Anda konfigurasikan untuk diminta oleh spiffe-helper. SPIFFE ID adalah string URI dan `subject_prefix` mencocokkannya sebagai teks opak, sehingga nilai persis maupun pencocokan prefiks dengan `*` di akhir sama-sama berfungsi. Untuk pola yang lebih kompleks, gunakan `condition` berbasis “Common Expression Language” (bahasa ekspresi umum), atau CEL.

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

`token_lifetime_seconds` adalah masa berlaku token akses Anthropic yang dikembalikan oleh pertukaran, bukan masa berlaku JWT-SVID. SDK memperbarui token akses secara otomatis.

Buatlah sespesifik yang dimungkinkan oleh workload. Longgarkan `subject_prefix` menjadi `spiffe://prod.example.com/ns/inference/*` hanya jika setiap workload yang terdaftar di bawah path tersebut harus dipetakan ke akun layanan Anthropic yang sama. Tambahkan ID `fdrl_...` milik aturan ke variabel lingkungan `ANTHROPIC_FEDERATION_RULE_ID` pada workload.

## Memperoleh dan menggunakan token

SDK dapat membaca JWT-SVID dari file yang dikelola spiffe-helper atau, kecuali di Java, memanggil SPIFFE Workload API secara langsung melalui penyedia token. Jalur file membutuhkan kode paling sedikit, dan SDK mendukungnya di setiap bahasa. Jalur penyedia token menghilangkan sidecar tetapi memerlukan klien SPIFFE Workload API dalam bahasa aplikasi Anda.

<Tabs>
  <Tab title="Berbasis file dengan spiffe-helper">
    Dengan spiffe-helper menulis JWT-SVID baru ke `/var/run/secrets/anthropic.com/token`, atur `ANTHROPIC_IDENTITY_TOKEN_FILE` ke path tersebut. Atur juga variabel lingkungan federasi lainnya yang dibaca oleh contoh berikut. SDK membaca file tersebut pada setiap pertukaran token, sehingga selalu mengambil SVID yang paling baru dirotasi. SDK juga memperbarui token akses Anthropic secara otomatis sebelum kedaluwarsa. Lihat [Variabel lingkungan](https://platform.claude.com/docs/id/manage-claude/wif-reference#environment-variables) untuk mengetahui asal setiap nilai.

    <CodeGroup>
      ```bash cURL
      JWT=$(cat "$ANTHROPIC_IDENTITY_TOKEN_FILE")

      ACCESS_TOKEN=$(curl -sS https://api.anthropic.com/v1/oauth/token \
        -H "content-type: application/json" \
        -d @- <<JSON | jq -r .access_token
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
        -H "anthropic-version: 2026-10-21" \
        -H "content-type: application/json" \
        -d '{
          "model": "claude-opus-5-5",
          "max_tokens": 1024,
          "messages": [{"role": "user", "content": "Hello, Claude"}]
        }'
      ```

      ```bash CLI
      # Membaca JWT-SVID yang ditulis spiffe-helper ke
      # ANTHROPIC_IDENTITY_TOKEN_FILE, serta ANTHROPIC_FEDERATION_RULE_ID,
      # ANTHROPIC_ORGANIZATION_ID, dan ANTHROPIC_SERVICE_ACCOUNT_ID.
      # Untuk aturan yang aktif di semua workspace atau lebih dari satu, atur ANTHROPIC_PROFILE
      # ke profil federasi yang menetapkan workspace_id.
      ant messages create \
        --model claude-opus-5-5 \
        --max-tokens 1024 \
        --message '{role: user, content: "Hello, Claude"}'
      ```

      ```python Python
      import anthropic

      # Membaca JWT-SVID yang ditulis spiffe-helper ke
      # ANTHROPIC_IDENTITY_TOKEN_FILE, serta ANTHROPIC_FEDERATION_RULE_ID,
      # ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID.
      client = anthropic.Anthropic()

      message = client.messages.create(
          model="claude-opus-5-5",
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
        model: "claude-opus-5-5",
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
      // Membaca JWT-SVID yang ditulis oleh spiffe-helper ke
      // ANTHROPIC_IDENTITY_TOKEN_FILE, serta ANTHROPIC_FEDERATION_RULE_ID,
      // ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID.
      using var client = new AnthropicClient();

      var message = await client.Messages.Create(new()
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [new UserMessageParam { Content = "Hello, Claude" }],
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
      	Model:     anthropic.ModelClaudeOpus5_5,
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
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .build());

      IO.println(message.content());
      ```

      ```php PHP
      use Anthropic\Client;

      // Membaca JWT-SVID yang ditulis spiffe-helper ke
      // ANTHROPIC_IDENTITY_TOKEN_FILE, serta ANTHROPIC_FEDERATION_RULE_ID,
      // ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID.
      $client = new Client();

      $message = $client->messages->create(
          model: 'claude-opus-5-5',
          maxTokens: 1024,
          messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      );
      $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
      echo $textBlock->text, PHP_EOL;
      ```

      ```ruby Ruby
      require "anthropic"

      # Membaca JWT-SVID yang ditulis spiffe-helper ke
      # ANTHROPIC_IDENTITY_TOKEN_FILE, serta ANTHROPIC_FEDERATION_RULE_ID,
      # ANTHROPIC_ORGANIZATION_ID, ANTHROPIC_SERVICE_ACCOUNT_ID, dan ANTHROPIC_WORKSPACE_ID.
      client = Anthropic::Client.new

      message = client.messages.create(
        model: "claude-opus-5-5",
        max_tokens: 1024,
        messages: [{role: "user", content: "Hello, Claude"}]
      )
      puts message.content.find { it.type == :text }.text
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Penyedia token melalui SPIFFE Workload API">
    Kecuali di Java, workload yang menautkan klien SPIFFE Workload API secara langsung dapat melewati spiffe-helper. Workload tersebut memberikan SDK sebuah penyedia token yang mengambil JWT-SVID baru dari socket agent. SDK memanggil provider sebelum setiap pertukaran token, sehingga workload selalu menyajikan SVID yang belum kedaluwarsa. Python ([py-spiffe](https://github.com/HewlettPackard/py-spiffe)) dan Go ([go-spiffe](https://github.com/spiffe/go-spiffe)) memiliki klien Workload API yang matang.

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
          model="claude-opus-5-5",
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

      	"github.com/anthropics/anthropic-sdk-go/v2"
      	"github.com/anthropics/anthropic-sdk-go/v2/option"
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
      		Model:     anthropic.ModelClaudeOpus5_5,
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
      Untuk bahasa lain, ambil JWT-SVID dengan klien SPIFFE Workload API milik runtime Anda (atau jalankan `spire-agent api fetch jwt`) dan tuliskan ke file. Kemudian atur `ANTHROPIC_IDENTITY_TOKEN_FILE` ke path tersebut, seperti pada tab berbasis file.
    </Note>
  </Tab>
</Tabs>

## Verifikasi penyiapan

Sebelum mengintegrasikan SDK, ambil JWT-SVID langsung dari SPIRE Agent dan pastikan klaimnya cocok dengan yang diharapkan aturan federasi Anda. Jika Anda menggunakan implementasi SPIFFE yang berbeda, ambil JWT-SVID dengan CLI atau klien Workload API-nya dan dekode payload dengan cara yang sama.

<Note>
  Workload API melakukan atestasi terhadap proses pemanggil. Untuk entri registrasi Kubernetes, jalankan perintah ini di dalam pod yang memenuhi selector entri tersebut dan memiliki socket agent yang ter-mount (misalnya, dengan menggunakan `kubectl exec`). Pada VM dan bare metal, jalankan sebagai pengguna atau proses yang cocok dengan selector `unix:` milik entri. Menjalankannya dari shell host yang tidak teratestasi akan mengembalikan `no identity issued`, yang merupakan kegagalan langkah verifikasi paling umum.
</Note>

```bash
spire-agent api fetch jwt \
  -audience https://api.anthropic.com \
  -socketPath /run/spire/sockets/agent.sock \
  -output json \
  | jq -r '.[0].svids[0].svid' \
  | jq -rR 'split(".")[1] | gsub("-";"+") | gsub("_";"/") | @base64d | fromjson'
```

Flag `-output json` mengembalikan respons SVID dan respons bundle sebagai array JSON dua elemen, sehingga `jq -r '.[0].svids[0].svid'` mengekstrak token mentah. Jika versi SPIRE Anda tidak memiliki flag `-output`, perintah tersebut mencetak blok berlabel. Dalam hal itu, salurkan output default melalui `awk '/^[[:space:]]*eyJ/{print $1; exit}'` untuk mengekstrak baris token. Periksa bahwa `iss` adalah URL OIDC Discovery Provider yang Anda daftarkan, `sub` adalah SPIFFE ID dari workload, dan `aud` berisi `https://api.anthropic.com`. Kemudian jalankan contoh di [Memperoleh dan menggunakan token](https://platform.claude.com/docs/id/manage-claude/wif-providers/spiffe#acquire-and-use-the-token). Pertukaran yang berhasil mengembalikan `access_token` yang diawali dengan `sk-ant-oat01-`. Jika pertukaran gagal dengan respons `401` `authentication_error` yang opak (pesan `Authentication failed`), periksa [halaman riwayat autentikasi](https://platform.claude.com/settings/workload-identity-federation?tab=history) di Claude Console untuk alasan penolakan. Kemudian lihat [Memecahkan masalah pertukaran yang gagal](https://platform.claude.com/docs/id/manage-claude/wif-reference#troubleshoot-a-failed-exchange). Penyebab paling umum di sisi SPIRE adalah ketidakcocokan antara `jwt_issuer` milik SPIRE Server dan URL yang Anda daftarkan sebagai penerbit federasi.

## Membatasi cakupan aturan Anda

Konvensi path SPIFFE ID ditentukan oleh operator, sehingga matcher `subject_prefix` pada federation rule harus mencerminkan skema path yang digunakan registration entry Anda. Skema umum mencakup `spiffe://<trust-domain>/ns/<namespace>/sa/<service-account>` (default yang dihasilkan oleh resource `ClusterSPIFFEID` di spire-controller-manager) dan `spiffe://<trust-domain>/host/<hostname>/<service>` untuk workload VM dan bare-metal.

<Warning>
  `subject_prefix` berupa `spiffe://prod.example.com/*` cocok dengan setiap workload di trust domain. Tanpa matcher `audience`, aturan tersebut juga menerima JWT-SVID yang diterbitkan untuk audience apa pun, termasuk yang diminta workload untuk “relying party” (pihak pengandal) yang tidak terkait.
</Warning>

Kunci blok `match` pada aturan ke cakupan tersempit yang sesuai dengan kasus penggunaan Anda:

* **Sematkan ke satu workload:** Atur `subject_prefix` ke SPIFFE ID lengkap tanpa `*` di akhir.
* **Selalu atur audience:** Wajibkan `audience` pada aturan dan konfigurasikan spiffe-helper (atau panggilan Workload API) dengan nilai yang sama sehingga Anthropic menolak SVID yang diterbitkan untuk pihak pengandal lain.
* **Batasi cakupan berdasarkan segmen path:** Gunakan `spiffe://prod.example.com/ns/inference/*` untuk mencocokkan setiap workload yang terdaftar di bawah suatu namespace. Buat aturan serta akun layanan Anthropic terpisah untuk setiap namespace alih-alih memperluas satu aturan.
* **Daftarkan satu issuer untuk setiap trust domain:** Setiap trust domain SPIRE memiliki kunci penandatanganan dan OIDC Discovery Provider sendiri. Daftarkan masing-masing sebagai penerbit federasi terpisah dan ikat aturan ke issuer yang memiliki SPIFFE ID yang dicocokkan aturan tersebut.

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
    Autentikasi ke Claude API dari klaster Kubernetes yang dikelola sendiri menggunakan token akun layanan terproyeksi.
  </Card>
</CardGroup>
