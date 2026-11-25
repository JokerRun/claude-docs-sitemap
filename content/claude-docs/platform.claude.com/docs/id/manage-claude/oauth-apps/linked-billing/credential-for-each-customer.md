---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 5ba08a81f11410f8e3318a2b9df918bcb77c89a34f4958c7baa35adfcd126ff5
---

---
title: Gunakan kredensial terpisah untuk setiap pelanggan
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer
description: Panggil Claude dengan token akses OAuth milik setiap pelanggan, sehingga kode yang tidak sepenuhnya Anda kendalikan hanya dapat menagih pelanggan tersebut.
---

<Warning>
  Claude Platform OAuth adalah Beta Service: perangkat lunak prarilis yang disediakan berdasarkan perjanjian Anda dengan Anthropic, seperti [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms), dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Endpoint, parameter, dan perilaku dapat berubah selama beta. Ini mungkin tidak cocok untuk penggunaan produksi.
</Warning>

Setiap pelanggan yang Anda tautkan dengan [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing) memiliki kredensialnya sendiri: sebuah “access token” (token akses) OAuth yang hanya dapat menagih pelanggan tersebut. Gunakan token ini ketika kode yang tidak sepenuhnya Anda kendalikan memanggil Claude untuk satu pelanggan, misalnya di “sandbox” (lingkungan terisolasi) milik agen atau di deployment “single-tenant” (penyewa tunggal). Bug atau kebocoran dalam kode tersebut hanya dapat menagih pelanggan tersebut.

Jika setiap permintaan yang menagih pelanggan berasal dari back end Anda sendiri, Anda tidak memerlukan kredensial ini. [Tagih pelanggan sebagai akun layanan operator Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#bill-a-request), dan lewati halaman ini.

## Sebelum Anda memulai

* **Token OAuth dan ID koneksi pelanggan:** Penukaran kode mengembalikan keduanya saat Anda [menautkan pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#save-the-connection-and-its-tokens). Koneksi adalah catatan yang mengaitkan organisasi Claude milik pelanggan ke salah satu [profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) Anda.
* **Sebuah “refresh token” (token penyegaran):** [**Offline access**](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#choose-whether-to-get-refresh-tokens) diaktifkan untuk aplikasi Anda, dan pelanggan telah menyetujui `billing:attribution offline_access`. Pelanggan yang menyetujui tanpa `offline_access` mendapatkan refresh token dengan [menyetujui lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#if-a-customer-approves-again), yang menggantikan koneksi mereka tanpa pembatalan tautan.
* **Untuk contoh penyegaran:** Sebuah “client assertion” (asersi klien): JWT dari penyedia identitas Anda untuk **Expected audience** aplikasi Anda, yang disiapkan sebagai [autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#set-up-client-authentication) aplikasi Anda. Contoh-contoh membacanya dari file yang disebutkan oleh variabel lingkungan `CLIENT_ASSERTION_FILE` atau dari variabel shell `CLIENT_ASSERTION`.

## Jaga kerahasiaan token OAuth

Simpan token akses, refresh token, dan waktu kedaluwarsa setiap pelanggan di penyimpanan rahasia yang hanya dapat dibaca oleh layanan yang melakukan penyegaran. Siapa pun yang memegang token akses dapat menagih pelanggan tersebut hingga token kedaluwarsa. Jika token bocor, [batalkan tautan pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#unlink-a-customer) terlebih dahulu, lalu tautkan mereka lagi. Jika Anda kehilangan refresh token, [tautkan pelanggan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again).

## Panggil Claude dengan token akses pelanggan

Kirim token akses pelanggan sebagai pengganti kredensial akun layanan operator Anda:

* **Di Anthropic SDK:** Teruskan token akses pelanggan sebagai token autentikasi klien saat Anda membangun klien.
* **Di CLI `ant`:** Atur `ANTHROPIC_AUTH_TOKEN` ke token tersebut untuk perintah.
* **Dalam permintaan HTTP:** Kirim sebagai bearer token di header `Authorization`. Jangan kirim header `x-api-key`.

<Warning>
  Hapus `ANTHROPIC_API_KEY` di mana pun Anda menggunakan token akses pelanggan: beberapa klien mengirim kunci tersebut sebagai gantinya, dan Anthropic dapat menagih Anda.
</Warning>

Klien-klien tersebut adalah CLI `ant` dan klien SDK yang membaca token dari `ANTHROPIC_AUTH_TOKEN`. Untuk alasannya dan pengaman terhadapnya, lihat [Jika kunci API dapat menjangkau proses](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#if-an-api-key-can-reach-the-process). Jika pencarian Anda tidak menemukan token untuk pelanggan, berhentilah sebelum Anda membangun klien. Jika diberi token null, SDK mungkin beralih ke kredensial Anda sendiri dan menagih Anda.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $CUSTOMER_ACCESS_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```bash CLI
  ANTHROPIC_AUTH_TOKEN="$CUSTOMER_ACCESS_TOKEN" ant messages create \
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  client = anthropic.Anthropic(auth_token=customer_access_token)

  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )

  for block in message.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic({ authToken: customerAccessToken });

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
  AnthropicClient client = new() { AuthToken = customerAccessToken };

  var message = await client.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [new UserMessageParam { Content = "Hello, Claude" }],
      }
  );

  foreach (var block in message.Content)
  {
      if (block.TryPickText(out var textBlock))
      {
          Console.WriteLine(textBlock.Text);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient(option.WithAuthToken(customerAccessToken))

  message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
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
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.builder()
      .authToken(customerAccessToken)
      .build();
  // ...

  var params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5_5)
      .maxTokens(1024)
      .addUserMessage("Hello, Claude")
      .build();
  var message = client.messages().create(params);

  for (var block : message.content()) {
      block.text().ifPresent(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  $client = new Client(authToken: $customerAccessToken);

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: Model::CLAUDE_OPUS_5_5,
  );

  foreach ($message->content as $block) {
      if ($block instanceof \Anthropic\Messages\TextBlock) {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new(auth_token: customer_access_token)

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }]
  )

  message.content.each do |block|
    puts(block.text) if block.is_a?(Anthropic::Models::TextBlock)
  end
  ```
</CodeGroup>

Token akses pelanggan hanya berfungsi pada endpoint berikut:

* `/v1/messages` dan `/v1/chat/completions`
* `/v1/messages/count_tokens`
* endpoint Models

Pada `/v1/messages` dan `/v1/chat/completions`, token akses saja sudah cukup untuk menagih pelanggan. Anda tidak memerlukan header `anthropic-user-profile-id` atau [`billing_policy`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#bill-a-request).

Kirim setiap permintaan lainnya dan setiap permintaan yang Anda bayar sendiri sebagai akun layanan operator Anda. Ini termasuk permintaan yang menggunakan eksekusi kode yang dapat ditagih, yang [tidak dapat menagih pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#if-you-use-code-execution).

Permintaan dengan token tersebut berjalan di workspace yang Anda tetapkan sebagai default aplikasi Anda. Mengarsipkannya akan mencabut setiap token di dalamnya: lihat [Jika Anda pindah ke workspace lain](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#if-you-move-to-another-workspace). Jika permintaan dengan token tersebut ditolak, lihat [Error Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors).

## Segarkan token OAuth

Token akses pelanggan berlaku paling lama 1 jam. Sebelum kedaluwarsa, kirim refresh token pelanggan ke endpoint token untuk mendapatkan pasangan token baru. Setiap refresh token hanya berfungsi sekali, kecuali satu pengulangan dalam 30 detik untuk memulihkan jawaban yang hilang.

<Warning>
  Refresh token yang dikirim lagi lebih dari 30 detik setelah penggunaan pertamanya akan mengakhiri koneksi pelanggan, dan Anda harus menautkan mereka lagi.
</Warning>

Untuk memastikan Anda tidak pernah mengirim token yang sudah digunakan terlambat:

* Matikan percobaan ulang otomatis untuk permintaan penyegaran di klien HTTP Anda dan di proxy mana pun.
* Segarkan token OAuth setiap pelanggan dari satu layanan, satu penyegaran dalam satu waktu untuk setiap pelanggan. Jika layanan memiliki replika, berikan mereka kunci (lock) bersama. Pegang kunci tersebut sejak membaca token tersimpan pelanggan hingga token baru disimpan.
* Simpan refresh token baru sebelum Anda menggunakan token akses baru.

Permintaannya adalah grant `refresh_token` ke `auth.claude.com`. Permintaan ini membawa refresh token dan [autentikasi klien](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#set-up-client-authentication) aplikasi Anda: `client_id` dan sebuah client assertion. Tidak ada SDK yang mencakup `auth.claude.com`, sehingga contoh-contoh memanggilnya melalui HTTP. Contoh-contoh tersebut menunjukkan panggilan sederhana tanpa penanganan kegagalan:

<CodeGroup exclude="shell:CLI">
  ```bash cURL
  curl https://auth.claude.com/v1/oauth/token \
    -H "content-type: application/json" \
    -d @- <<JSON
  {
    "grant_type": "refresh_token",
    "refresh_token": "$CUSTOMER_REFRESH_TOKEN",
    "client_id": "clid_01ABcDeFgHiJkLmNoPqRsTuV",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": "$CLIENT_ASSERTION"
  }
  JSON
  ```

  <CodeGroupItem language="CLI">
    CLI `ant` tidak memiliki perintah untuk `auth.claude.com`. Kirim penyegaran dengan cURL atau dalam bahasa aplikasi Anda.
  </CodeGroupItem>

  ```python Python
  import os
  from pathlib import Path

  import httpx2  # comes with the Anthropic SDK


  def refresh_tokens(refresh_token: str) -> dict:
      assertion_file = Path(os.environ["CLIENT_ASSERTION_FILE"])

      response = httpx2.post(
          "https://auth.claude.com/v1/oauth/token",
          json={
              "grant_type": "refresh_token",
              "refresh_token": refresh_token,
              "client_id": "clid_01ABcDeFgHiJkLmNoPqRsTuV",
              "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              "client_assertion": assertion_file.read_text().strip(),
          },
          timeout=10,
      )
      if not response.is_success:
          raise RuntimeError(f"Refresh failed: {response.status_code} {response.text}")
      return response.json()  # the new access_token and refresh_token
  ```

  ```typescript TypeScript
  import { readFile } from "node:fs/promises";

  async function refreshTokens(refreshToken: string) {
    const jwt = await readFile(process.env.CLIENT_ASSERTION_FILE!, "utf8");

    const response = await fetch("https://auth.claude.com/v1/oauth/token", {
      method: "POST",
      redirect: "error",
      signal: AbortSignal.timeout(10_000),
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        grant_type: "refresh_token",
        refresh_token: refreshToken,
        client_id: "clid_01ABcDeFgHiJkLmNoPqRsTuV",
        client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        client_assertion: jwt.trim()
      })
    });
    if (!response.ok) {
      throw new Error(`Refresh failed: ${response.status} ${await response.text()}`);
    }
    return response.json(); // the new access_token and refresh_token
  }
  ```

  ```csharp C#
  using System.Net.Http.Json;
  using System.Text.Json;

  using var http = new HttpClient { Timeout = TimeSpan.FromSeconds(10) };

  async Task<JsonElement> RefreshTokens(string refreshToken)
  {
      var assertionFile = Environment.GetEnvironmentVariable("CLIENT_ASSERTION_FILE")!;
      var jwt = await File.ReadAllTextAsync(assertionFile);

      using var response = await http.PostAsJsonAsync(
          "https://auth.claude.com/v1/oauth/token",
          new Dictionary<string, string>
          {
              ["grant_type"] = "refresh_token",
              ["refresh_token"] = refreshToken,
              ["client_id"] = "clid_01ABcDeFgHiJkLmNoPqRsTuV",
              ["client_assertion_type"] = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              ["client_assertion"] = jwt.Trim(),
          }
      );
      if (!response.IsSuccessStatusCode)
      {
          var details = await response.Content.ReadAsStringAsync();
          throw new HttpRequestException($"Refresh failed: {(int)response.StatusCode} {details}");
      }

      // access_token dan refresh_token yang baru
      return await response.Content.ReadFromJsonAsync<JsonElement>();
  }
  ```

  ```go Go
  import (
  	"bytes"
  	"encoding/json"
  	"fmt"
  	"io"
  	"net/http"
  	"os"
  	"strings"
  	"time"
  )

  var httpClient = &http.Client{Timeout: 10 * time.Second}

  func refreshTokens(refreshToken string) (map[string]any, error) {
  	jwt, err := os.ReadFile(os.Getenv("CLIENT_ASSERTION_FILE"))
  	if err != nil {
  		return nil, err
  	}

  	body, err := json.Marshal(map[string]string{
  		"grant_type":            "refresh_token",
  		"refresh_token":         refreshToken,
  		"client_id":             "clid_01ABcDeFgHiJkLmNoPqRsTuV",
  		"client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
  		"client_assertion":      strings.TrimSpace(string(jwt)),
  	})
  	if err != nil {
  		return nil, err
  	}

  	endpoint := "https://auth.claude.com/v1/oauth/token"
  	response, err := httpClient.Post(endpoint, "application/json", bytes.NewReader(body))
  	if err != nil {
  		return nil, err
  	}
  	defer response.Body.Close()
  	if response.StatusCode/100 != 2 {
  		details, _ := io.ReadAll(response.Body)
  		return nil, fmt.Errorf("refresh failed: %d %s", response.StatusCode, details)
  	}

  	var tokens map[string]any // the new access_token and refresh_token
  	err = json.NewDecoder(response.Body).Decode(&tokens)
  	return tokens, err
  }
  ```

  ```java Java
  import module java.base;
  import module java.net.http;
  import com.fasterxml.jackson.databind.JsonNode;
  import com.fasterxml.jackson.databind.ObjectMapper; // Jackson comes with the Anthropic SDK

  final HttpClient http = HttpClient.newHttpClient();
  final ObjectMapper mapper = new ObjectMapper();

  JsonNode refreshTokens(String refreshToken) throws Exception {
      var jwt = Files.readString(Path.of(System.getenv("CLIENT_ASSERTION_FILE")));

      var body = mapper.createObjectNode()
          .put("grant_type", "refresh_token")
          .put("refresh_token", refreshToken)
          .put("client_id", "clid_01ABcDeFgHiJkLmNoPqRsTuV")
          .put("client_assertion_type", "urn:ietf:params:oauth:client-assertion-type:jwt-bearer")
          .put("client_assertion", jwt.strip());

      var request = HttpRequest.newBuilder(URI.create("https://auth.claude.com/v1/oauth/token"))
          .header("content-type", "application/json")
          .timeout(Duration.ofSeconds(10))
          .POST(HttpRequest.BodyPublishers.ofString(body.toString()))
          .build();
      var response = http.send(request, HttpResponse.BodyHandlers.ofString());
      if (response.statusCode() / 100 != 2) {
          throw new IOException("Refresh failed: " + response.statusCode() + " " + response.body());
      }
      return mapper.readTree(response.body()); // the new access_token and refresh_token
  }
  ```

  ```php PHP
  function refreshTokens(string $refreshToken): mixed
  {
      $jwt = file_get_contents((string) getenv('CLIENT_ASSERTION_FILE'))
          ?: throw new \RuntimeException('Cannot read the client assertion file');

      $body = json_encode([
          'grant_type' => 'refresh_token',
          'refresh_token' => $refreshToken,
          'client_id' => 'clid_01ABcDeFgHiJkLmNoPqRsTuV',
          'client_assertion_type' => 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
          'client_assertion' => trim($jwt),
      ], JSON_THROW_ON_ERROR);

      $context = stream_context_create(['http' => [
          'method' => 'POST',
          'header' => 'content-type: application/json',
          'content' => $body,
          'timeout' => 10,
          'ignore_errors' => true, // keep the body of an error response
      ]]);
      $response = file_get_contents('https://auth.claude.com/v1/oauth/token', context: $context);
      $status = http_get_last_response_headers()[0] ?? '';
      if ($response === false || !preg_match('{^HTTP/\S+ 2}', $status)) {
          throw new \RuntimeException("Refresh failed: {$status} {$response}");
      }

      // access_token dan refresh_token yang baru
      return json_decode($response, associative: true, flags: JSON_THROW_ON_ERROR);
  }
  ```

  ```ruby Ruby
  require "json"
  require "net/http"

  def refresh_tokens(refresh_token)
    jwt = File.read(ENV.fetch("CLIENT_ASSERTION_FILE"))

    body = {
      grant_type: "refresh_token",
      refresh_token:,
      client_id: "clid_01ABcDeFgHiJkLmNoPqRsTuV",
      client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      client_assertion: jwt.strip
    }
    response = Net::HTTP.start("auth.claude.com", 443, use_ssl: true, read_timeout: 10) do |http|
      http.post("/v1/oauth/token", body.to_json, "content-type" => "application/json")
    end
    unless response.is_a?(Net::HTTPSuccess)
      raise "Refresh failed: #{response.code} #{response.body}"
    end

    JSON.parse(response.body) # the new access_token and refresh_token
  end
  ```
</CodeGroup>

Respons berisi token akses baru dan refresh token baru. `expires_in` dan `refresh_token_expires_in` memberikan masa berlakunya dalam detik. Refresh token baru menggantikan yang Anda kirim, dan token akses sebelumnya berhenti berfungsi dalam beberapa menit.

Sebelum Anda mengirim token lagi setelah penyegaran gagal, baca [apa yang harus dilakukan jika penyegaran gagal](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#if-a-refresh-fails). Beberapa percobaan ulang mengakhiri koneksi, dan beberapa kegagalan berarti Anda harus menjeda penyegaran setiap pelanggan. [Contoh penyegaran lengkap](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#full-refresh-sample) menangani kegagalan-kegagalan tersebut.

Refresh token berlaku paling lama 1 tahun sejak penukaran kode, dan penyegaran tidak memperpanjangnya. Sebelum kedaluwarsa, [tautkan pelanggan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again).

## Jalankan agen di sandbox

Sebelum Anda menggunakan bagian ini, baca bagian 4.1(b) dari [Linked Billing Beta Terms](https://www.anthropic.com/legal/linked-billing-terms). Jika Anda memiliki pertanyaan tentangnya, tanyakan kepada tim akun Anthropic Anda.

Ketika agen bekerja untuk satu pelanggan di sandbox, ikuti aturan berikut:

* Berikan sandbox hanya token akses, jangan pernah refresh token. Back end Anda menyegarkan token dan mengirim setiap token akses baru ke sandbox.
* Tentukan pelanggan mana yang dilayani sandbox dari identitas sandbox itu sendiri, seperti identitas pod-nya. Jangan pernah menentukannya dari nilai yang dikirim oleh sandbox.
* Kirim ke sandbox hanya token milik pelanggan yang dilayaninya.
* Jangan berikan sandbox token identitas yang di-mount dan jangan berikan akses ke server metadata cloud.

Aturan terakhir tersebut mencegah sandbox mendapatkan JWT yang cocok dengan autentikasi klien aplikasi Anda atau salah satu [aturan federasi](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation) Anda. Dengan JWT semacam itu, kode di sandbox dapat mengautentikasi sebagai aplikasi Anda atau sebagai salah satu akun layanan Anda.

Anthropic SDK, Claude Code, dan [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) dapat membaca token akses dari file kredensial dalam profil konfigurasi. Untuk format file tersebut, lihat [File konfigurasi profil](https://platform.claude.com/docs/id/manage-claude/wif-reference#profile-configuration-file). Untuk menyiapkan sandbox:

<Steps>
  <Step title="Tambahkan profil">
    Di sandbox, buat direktori konfigurasi. Di dalamnya, tambahkan profil di `configs/customer.json` yang tipe autentikasinya adalah `user_oauth`. Jangan berikan `client_id` pada profil: jika ada, SDK mengharapkan refresh token di file tersebut dan menyegarkan token sendiri.

    <File filename="configs/customer.json">
      ```json
      {
        "version": "1.0",
        "authentication": {
          "type": "user_oauth"
        }
      }
      ```
    </File>
  </Step>

  <Step title="Tulis token akses">
    Sebelum agen dimulai, tulis token akses ke `credentials/customer.json` di direktori konfigurasi yang sama, sehingga `configs` dan `credentials` berada berdampingan. Tulis lagi segera setelah setiap penyegaran. `expires_at` adalah waktu kedaluwarsa token dalam detik Unix. Untuk kode yang menulisnya dengan aman, lihat [Saat Anda menulis setiap token akses baru ke sandbox](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#when-you-write-each-new-token-to-a-sandbox).

    ```json credentials/customer.json
    {
      "type": "oauth_token",
      "access_token": "sk-ant-oat01-...",
      "expires_at": 1793635200
    }
    ```
  </Step>

  <Step title="Arahkan klien ke profil">
    Atur `ANTHROPIC_CONFIG_DIR` ke direktori konfigurasi dan `ANTHROPIC_PROFILE` ke `customer`.
  </Step>

  <Step title="Hapus setiap kredensial lainnya">
    Hapus setiap kredensial lainnya di sandbox, karena masing-masing dapat diprioritaskan di atas profil. Ini termasuk:

    * variabel lingkungan `ANTHROPIC_API_KEY` dan `ANTHROPIC_AUTH_TOKEN`
    * variabel lingkungan `CLAUDE_CODE_OAUTH_TOKEN` dan pengaturan `apiKeyHelper` milik Claude Code
  </Step>
</Steps>

SDK mengambil setiap token baru tanpa perlu restart: lihat [Saat Anda menulis setiap token akses baru ke sandbox](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#when-you-write-each-new-token-to-a-sandbox).

## Periksa hasilnya

Untuk memastikan bahwa permintaan menagih pelanggan, lihat [di mana permintaan yang ditagih muncul](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#check-the-result). Untuk memastikan bahwa token terbatas pada pelanggannya:

* Permintaan dengan token yang menyebutkan profil pengguna Anda yang lain mendapatkan `400 invalid_request_error`.
* Beberapa menit setelah penyegaran, permintaan dengan token akses sebelumnya mendapatkan `401 authentication_error`.

## Putuskan apakah akan menonaktifkan autentikasi khusus operator

Secara default, akun layanan operator Anda dapat menagih pelanggan tertaut mana pun tanpa token akses pelanggan. Akun tersebut menyebutkan profil pengguna pelanggan dan mengatur `bill_to: "user_profile"` di [`billing_policy`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#bill-a-request). Default ini disebut “operator-only authentication” (autentikasi khusus operator), dan tetap berfungsi setelah token akses pelanggan kedaluwarsa.

Setelah permintaan setiap pelanggan menggunakan token akses mereka sendiri, Anda dapat menonaktifkan autentikasi khusus operator. Kemudian, hanya token akses milik pelanggan sendiri yang dapat menagih mereka, sehingga bug yang menyebutkan profil pengguna yang salah tidak dapat menagih pelanggan yang salah.

Permintaan setiap pelanggan kemudian bergantung pada penyegaran. Jika Anda kehilangan refresh token pelanggan, Anda tidak dapat menagih mereka hingga mereka [menautkan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again). Apa pun yang menghentikan penyegaran, seperti menonaktifkan **Offline access** atau mengosongkan [workspace default](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#default-workspace), membuat permintaan setiap pelanggan gagal seiring token akses mereka kedaluwarsa.

Claude Console hanya memeriksa bahwa aplikasi Anda memiliki `billing:attribution`, `offline_access`, dan workspace default. Sebelum Anda menonaktifkan autentikasi khusus operator, periksa sendiri hal-hal berikut:

* Penyimpanan Anda menyimpan refresh token untuk setiap pelanggan tertaut.
* Permintaan Anda dengan token akses mereka berfungsi.

Untuk menonaktifkan autentikasi khusus operator:

1. Buka tab **Client authentication** aplikasi di Console.
2. Di bawah akun layanan operator, aktifkan **Disable operator-only tokenless authentication** dan konfirmasi di kotak dialog. Namanya di API adalah `disable_operator_only_auth`.

Aturan berikut kemudian berlaku:

* Permintaan dari akun layanan saja yang mengatur `bill_to: "user_profile"` untuk pelanggan tertaut mendapatkan `403 user_profile_not_billable`. Pelanggan tetap ditampilkan sebagai **Linked**, jadi pantau log Anda untuk error ini.
* Akun layanan masih dapat mengelola profil pengguna dan mengirim permintaan yang Anda bayar sendiri.
* Untuk kembali ke default, nonaktifkan pengaturan yang sama.

## Detail implementasi, aturan, dan kasus khusus

Sisa halaman ini adalah detail di balik langkah-langkah tersebut. Bagian ini mencakup penyegaran yang gagal, contoh penyegaran lengkap, dan bagaimana kunci API atau penyegaran memengaruhi klien yang sedang berjalan. Pelanggan yang hanya menyetujui scope yang sudah usang tidak memiliki token akses sendiri: lihat [Jika Anda masih menggunakan scope usang](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#if-you-still-use-the-deprecated-scope).

### Jika penyegaran gagal

Penyegaran menggantikan refresh token yang Anda kirim. Apa yang terjadi ketika token yang sudah diganti tiba lagi bergantung pada kapan token tersebut tiba:

* **Dalam 30 detik, pertama kali:** Mengembalikan pasangan token baru dan mencabut pasangan yang tidak pernah Anda terima. Ini memungkinkan Anda mengulangi penyegaran yang jawabannya hilang.
* **Dalam 30 detik, pertama kali, jika token yang Anda kirim berusia kurang dari 30 detik saat diganti:** Mendapatkan `invalid_grant`, dan koneksi tetap ada.
* **Dalam 30 detik, kali berikutnya:** Mendapatkan `invalid_grant`, dan koneksi tetap ada.
* **Setelah 30 detik:** Mendapatkan `invalid_grant` dan mengakhiri koneksi. Setiap token dicabut, pelanggan ditampilkan sebagai **Unlinked**, dan tidak ada yang dapat menagih mereka hingga mereka menautkan lagi.

Setelah penyegaran gagal, apa yang harus dilakukan bergantung pada apakah refresh token mencapai `auth.claude.com` dan telah digunakan:

| Apa yang didapat penyegaran | Apa artinya | Apa yang harus dilakukan |
| ----- | ----- | ----- |
| Permintaan tidak dapat mencapai `auth.claude.com`, termasuk connect timeout | Token tidak terkirim | Kirim lagi nanti |
| `429` | Tidak ada yang dicabut | Tunggu, lalu kirim lagi |
| Penolakan `503`: header `retry-after` dan `"type": "error"` di tingkat atas body | Tidak ada yang dicabut | Tunggu, lalu kirim lagi |
| `4xx` lainnya, kecuali `invalid_grant` | Tidak ada yang dicabut | Perbaiki penyebabnya, lalu kirim lagi |
| `5xx` lainnya atau jaringan terputus setelah permintaan terkirim | Mungkin sudah berhasil | Kirim sekali lagi, segera |
| Tidak ada jawaban tepat waktu (read timeout) | Mungkin masih berjalan | Jangan kirim lagi |
| `invalid_grant` | Token tidak dapat digunakan sekarang | Berhenti mengirimnya |

**Tunggu, lalu kirim lagi:** Tunggu setidaknya selama yang dinyatakan `retry-after`. Jika `429` tidak memiliki header `retry-after`, lakukan back off sebelum Anda mengirimnya lagi. `503` yang tidak memiliki salah satu dari kedua tanda tersebut dihitung sebagai `5xx` lainnya.

**Perbaiki penyebabnya, lalu kirim lagi:**

* `unauthorized_client`: `error_description` biasanya menyebutkan penyebabnya, seperti workspace default yang hilang atau `offline_access` tidak lagi aktif di aplikasi Anda.
* `invalid_client`: client assertion Anda gagal. Periksa terhadap [Klaim client assertion](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#client-assertion-claims).
* `invalid_scope`: permintaan mengirim parameter `scope`, atau `billing:attribution` tidak lagi ada di aplikasi Anda.
* `4xx` lainnya, seperti `invalid_request`: perbaiki permintaan.

Jika Anda mengubah atau mengarsipkan akun layanan operator, setiap penyegaran token yang berfungsi mendapatkan `unauthorized_client`, dan mengirim lagi tidak akan membantu. Lihat [Jika Anda mengubah akun layanan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#if-you-change-the-service-account).

**Kirim sekali lagi, segera:** `auth.claude.com` harus menerima permintaan kedua dalam 30 detik sejak mengganti token. Anda tidak dapat melihat kapan itu terjadi, jadi hitung dari saat Anda mengirim permintaan pertama, dan sisakan waktu agar permintaan kedua tiba. Kemudian:

* Jika permintaan kedua mengembalikan token baru, simpan dan gunakan hanya token tersebut.
* Jika mengembalikan hal lain, tidak mendapatkan jawaban, atau tidak dapat terkirim tepat waktu, jangan kirim token lagi.

**Jangan kirim lagi:** Setelah read timeout atau jawaban hilang yang tidak dapat Anda pulihkan, berhenti menyegarkan pelanggan tersebut dan [tautkan mereka lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again).

**Berhenti mengirimnya:** Berhenti menyegarkan pelanggan tersebut. `invalid_grant` biasanya berarti salah satu dari hal berikut, dan respons tidak menyebutkan yang mana, jadi periksa dua yang pertama sebelum Anda menautkan siapa pun lagi:

* Organisasi pelanggan ditangguhkan. Jangan batalkan tautan pelanggan, dan simpan refresh token: token tersebut berfungsi lagi setelah penangguhan berakhir. Untuk mengetahuinya, tanyakan kepada [dukungan Anthropic](https://support.claude.com/en/articles/9015913-how-to-get-support) atau tim akun Anthropic Anda jika Anda memilikinya.
* Penyegaran setiap pelanggan mendapatkan `invalid_grant` pada saat yang sama. Cari penyebab di sisi Anda, seperti [workspace yang diarsipkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#if-you-move-to-another-workspace).
* Token kedaluwarsa atau sudah digunakan, koneksi berakhir, atau workspace-nya diarsipkan. [Tautkan pelanggan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again).

Koneksi jaringan yang terputus, respons `5xx`, atau timeout dapat berarti bahwa `auth.claude.com` mengalami gangguan. Jika salah satunya membuat Anda berhenti menyegarkan pelanggan, cegah gangguan tersebut agar tidak membuat Anda kehilangan lebih banyak koneksi:

1. Jeda penyegaran pelanggan Anda yang lain.
2. Segarkan satu pelanggan.
3. Lanjutkan sisanya hanya setelah penyegaran tersebut berhasil atau mendapatkan respons `4xx`.

### Contoh penyegaran lengkap

Versi penyegaran ini mengikuti [Jika penyegaran gagal](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer#if-a-refresh-fails). Versi ini menambahkan pengaman berikut ke panggilan sederhana:

* Menyegarkan ketika token akses memiliki sisa waktu kurang dari 10 menit.
* Memegang kunci untuk setiap pelanggan sejak membaca token tersimpan hingga token baru disimpan.
* Sebelum refresh token meninggalkan proses, versi ini menandai token tersimpan sebagai `on_hold` (typescript, java, php: `onHold`; csharp, go: `OnHold`), sehingga crash tidak dapat menyebabkan pengiriman kedua.
* Menunggu hingga 2 detik untuk mencapai `auth.claude.com` dan 10 detik untuk jawaban.
* Mengirim permintaan kedua hanya dalam 4 detik sejak yang pertama. Ini menyisakan waktu agar permintaan kedua tiba dalam 30 detik. Ini juga menjaga permintaan kedua tetap di dalam waktu tunggu 10 detik, sehingga permintaan yang mengalami timeout tidak pernah dikirim lagi.
* Jika hanya penulisan ke penyimpanan rahasia Anda yang gagal, versi ini mencoba penulisan lagi dan tidak menyegarkan lagi.

Contoh ini menyerahkan tiga hal kepada Anda:

* kunci yang dibagikan oleh semua replika Anda, karena kuncinya sendiri tidak menjangkau replika Anda yang lain
* menunggu dan mengirim lagi setelah penolakan `429` atau `503`, yang dilaporkannya sebagai error
* menjeda penyegaran pelanggan Anda yang lain setelah penyegaran yang hilang, di setiap replika

Panggil fungsi penyegaran untuk setiap pelanggan lebih sering dari setiap 10 menit, sehingga fungsi tersebut selalu berjalan di dalam margin tersebut.

`refresh_connection()` (typescript, go, java, php: `refreshConnection()`; csharp: `Connections.RefreshConnection()`) gagal dengan `RefreshOnHoldError` (csharp, java, php: `RefreshOnHoldException`) ketika refresh token tidak boleh dikirim lagi. Fungsi ini juga gagal pada setiap panggilan berikutnya untuk pelanggan tersebut. Catatan tersimpan mempertahankan `on_hold` (typescript, java, php: `onHold`; csharp, go: `OnHold`) dan `hold_reason` (typescript, java, php: `holdReason`; csharp, go: `HoldReason`), sehingga Anda dapat mengetahui nanti mengapa penahanan diatur. Ketika hanya penulisan yang gagal, `new_tokens` (typescript, java, php: `newTokens`; csharp, go: `NewTokens`) pada error berisi token yang harus disimpan.

Penyiapan berikut mendefinisikan nama-nama bersama. Anda menulis `load_tokens()` (typescript, go, java, php: `loadTokens()`; csharp: `LoadTokens()`) dan `save_tokens()` (typescript, go, java, php: `saveTokens()`; csharp: `SaveTokens()`) untuk penyimpanan rahasia Anda sendiri.

<CodeGroup exclude="shell:cURL, shell:CLI">
  <CodeGroupItem language="cURL">
    Penyiapan ini digunakan bersama fungsi penyegaran berikut, yang memerlukan lebih banyak logika daripada satu perintah shell. Tulis keduanya dalam bahasa aplikasi Anda.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Penyiapan ini digunakan bersama fungsi penyegaran berikut, yang memerlukan lebih banyak logika daripada satu perintah shell. Tulis keduanya dalam bahasa aplikasi Anda.
  </CodeGroupItem>

  ```python Python
  import os
  import threading
  import time
  from collections import defaultdict
  from dataclasses import dataclass, field, replace
  from pathlib import Path

  import httpx2  # comes with the Anthropic SDK

  TOKEN_URL = "https://auth.claude.com/v1/oauth/token"
  CLIENT_ID = "clid_01ABcDeFgHiJkLmNoPqRsTuV"
  JWT_BEARER = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
  REFRESH_MARGIN_SECONDS = 600
  REQUEST_TIMEOUT = httpx2.Timeout(10, connect=2)
  SECOND_REQUEST_DEADLINE_SECONDS = 4  # keep this under the 10-second read timeout


  @dataclass
  class ConnectionTokens:
      refresh_token: str = field(repr=False)
      access_token: str = field(repr=False)
      expires_at: int  # Unix seconds
      refresh_expires_at: int  # Unix seconds
      on_hold: bool = False  # True: the refresh token might have been used
      hold_reason: str | None = None  # "lost" or "invalid_grant"


  class RefreshOnHoldError(Exception):
      """The refresh token must not be sent again. Don't catch this to try again.

      If new_tokens is set, only the write failed: store those tokens.
      """

      new_tokens: ConnectionTokens | None = None


  def client_assertion() -> str:
      """Reads the JWT that authenticates your app to auth.claude.com."""
      return Path(os.environ["CLIENT_ASSERTION_FILE"]).read_text().strip()


  def load_tokens(connection_id: str) -> ConnectionTokens:
      """Reads the connection's newest tokens from your secret store."""
      raise NotImplementedError("Read the tokens from your secret store.")


  def save_tokens(connection_id: str, tokens: ConnectionTokens) -> None:
      """Writes the connection's newest tokens to your secret store."""
      raise NotImplementedError("Write the tokens to your secret store.")
  ```

  ```typescript TypeScript
  import { readFile } from "node:fs/promises";
  import type { IncomingHttpHeaders } from "node:http";
  import { request } from "node:https";

  const TOKEN_URL = "https://auth.claude.com/v1/oauth/token";
  const CLIENT_ID = "clid_01ABcDeFgHiJkLmNoPqRsTuV";
  const JWT_BEARER = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer";
  const REFRESH_MARGIN_SECONDS = 600;
  const SECOND_REQUEST_DEADLINE_MS = 4_000; // keep this under the 10-second timeout

  interface ConnectionTokens {
    refreshToken: string;
    accessToken: string;
    expiresAt: number; // Unix seconds
    refreshExpiresAt: number; // Unix seconds
    onHold?: boolean; // true: the refresh token might have been used
    holdReason?: "lost" | "invalid_grant";
  }

  /** The refresh token must not be sent again. Don't catch this to try again. */
  class RefreshOnHoldError extends Error {
    override name = "RefreshOnHoldError";
    readonly #newTokens?: ConnectionTokens; // private, so that printing the error doesn't show them

    constructor(message: string, newTokens?: ConnectionTokens) {
      super(message);
      this.#newTokens = newTokens;
    }

    /** If set, only the write failed: store these tokens. */
    get newTokens() {
      return this.#newTokens;
    }
  }

  /** Reads the JWT that authenticates your app to auth.claude.com. */
  async function clientAssertion(): Promise<string> {
    return (await readFile(process.env.CLIENT_ASSERTION_FILE!, "utf8")).trim();
  }

  /** Reads the connection's newest tokens from your secret store. */
  async function loadTokens(connectionId: string): Promise<ConnectionTokens> {
    throw new Error("Read the tokens from your secret store.");
  }

  /** Writes the connection's newest tokens to your secret store. */
  async function saveTokens(connectionId: string, tokens: ConnectionTokens): Promise<void> {
    throw new Error("Write the tokens to your secret store.");
  }
  ```

  ```csharp C#
  using System.Collections.Concurrent;
  using System.Diagnostics;
  using System.Text;
  using System.Text.Json;

  record ConnectionTokens(
      string RefreshToken,
      string AccessToken,
      long ExpiresAt, // Unix seconds
      long RefreshExpiresAt, // Unix seconds
      bool OnHold = false, // true: the refresh token might have been used
      string? HoldReason = null // "lost" or "invalid_grant"
  )
  {
      // Menjaga token agar tidak masuk ke log.
      public override string ToString() =>
          $"ConnectionTokens {{ ExpiresAt = {ExpiresAt}, OnHold = {OnHold}, HoldReason = {HoldReason} }}";
  }

  /// <summary>Refresh token tidak boleh dikirim lagi. Jangan tangkap ini untuk mencoba ulang.</summary>
  class RefreshOnHoldException(string message) : Exception(message)
  {
      /// <summary>Jika diatur, hanya penulisan yang gagal: simpan token ini.</summary>
      public ConnectionTokens? NewTokens { get; init; }
  }

  static partial class Connections
  {
      const string TokenUrl = "https://auth.claude.com/v1/oauth/token";
      const string ClientId = "clid_01ABcDeFgHiJkLmNoPqRsTuV";
      const string JwtBearer = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer";
      const int RefreshMarginSeconds = 600;
      static readonly TimeSpan SecondRequestDeadline = TimeSpan.FromSeconds(4); // keep this under the 10-second timeout

      /// <summary>Membaca JWT yang mengautentikasi aplikasi Anda ke auth.claude.com.</summary>
      static string ClientAssertion() =>
          File.ReadAllText(Environment.GetEnvironmentVariable("CLIENT_ASSERTION_FILE")!).Trim();

      /// <summary>Membaca token terbaru koneksi dari penyimpanan rahasia Anda.</summary>
      static Task<ConnectionTokens> LoadTokens(string connectionId) =>
          throw new NotImplementedException("Read the tokens from your secret store.");

      /// <summary>Menulis token terbaru koneksi ke penyimpanan rahasia Anda.</summary>
      static Task SaveTokens(string connectionId, ConnectionTokens tokens) =>
          throw new NotImplementedException("Write the tokens to your secret store.");
  }
  ```

  ```go Go
  import (
  	"bytes"
  	"encoding/json"
  	"errors"
  	"fmt"
  	"io"
  	"net"
  	"net/http"
  	"net/http/httptrace"
  	"os"
  	"strings"
  	"sync"
  	"time"
  )

  const (
  	tokenURL              = "https://auth.claude.com/v1/oauth/token"
  	clientID              = "clid_01ABcDeFgHiJkLmNoPqRsTuV"
  	jwtBearer             = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
  	refreshMargin         = 10 * time.Minute
  	secondRequestDeadline = 4 * time.Second // keep this under the 10-second timeout
  )

  var httpClient = &http.Client{
  	Timeout: 10 * time.Second,
  	Transport: &http.Transport{
  		Proxy:               http.ProxyFromEnvironment,
  		DialContext:         (&net.Dialer{Timeout: 2 * time.Second}).DialContext,
  		TLSHandshakeTimeout: 2 * time.Second,
  	},
  	CheckRedirect: func(*http.Request, []*http.Request) error { return http.ErrUseLastResponse },
  }

  type ConnectionTokens struct {
  	RefreshToken     string
  	AccessToken      string
  	ExpiresAt        int64  // Unix seconds
  	RefreshExpiresAt int64  // Unix seconds
  	OnHold           bool   // true: the refresh token might have been used
  	HoldReason       string // "lost" or "invalid_grant"
  }

  // String menjaga token agar tidak masuk ke log.
  func (t ConnectionTokens) String() string {
  	return fmt.Sprintf("ConnectionTokens{ExpiresAt: %d, OnHold: %t, HoldReason: %q}", t.ExpiresAt, t.OnHold, t.HoldReason)
  }

  // RefreshOnHoldError berarti refresh token tidak boleh dikirim lagi. Jangan coba lagi.
  type RefreshOnHoldError struct {
  	Message   string
  	NewTokens *ConnectionTokens // if set, only the write failed: store these tokens
  }

  func (e *RefreshOnHoldError) Error() string { return e.Message }

  // clientAssertion membaca JWT yang mengautentikasi aplikasi Anda ke auth.claude.com.
  func clientAssertion() (string, error) {
  	jwt, err := os.ReadFile(os.Getenv("CLIENT_ASSERTION_FILE"))
  	return strings.TrimSpace(string(jwt)), err
  }

  // loadTokens membaca token terbaru koneksi dari penyimpanan rahasia Anda.
  func loadTokens(connectionID string) (ConnectionTokens, error) {
  	return ConnectionTokens{}, errors.New("read the tokens from your secret store")
  }

  // saveTokens menulis token terbaru koneksi ke penyimpanan rahasia Anda.
  func saveTokens(connectionID string, tokens ConnectionTokens) error {
  	return errors.New("write the tokens to your secret store")
  }
  ```

  ```java Java
  import module java.base;
  import module java.net.http;
  import com.fasterxml.jackson.databind.JsonNode;
  import com.fasterxml.jackson.databind.ObjectMapper; // Jackson comes with the Anthropic SDK

  static final URI TOKEN_URL = URI.create("https://auth.claude.com/v1/oauth/token");
  static final String CLIENT_ID = "clid_01ABcDeFgHiJkLmNoPqRsTuV";
  static final String JWT_BEARER = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer";
  static final long REFRESH_MARGIN_SECONDS = 600;
  static final Duration SECOND_REQUEST_DEADLINE = Duration.ofSeconds(4); // keep this under the 10-second read timeout

  record ConnectionTokens(
      String refreshToken,
      String accessToken,
      long expiresAt, // Unix seconds
      long refreshExpiresAt, // Unix seconds
      boolean onHold, // true: the refresh token might have been used
      String holdReason // "lost" or "invalid_grant"
  ) {
      @Override // keeps the tokens out of logs
      public String toString() {
          return "ConnectionTokens[expiresAt=" + expiresAt + ", onHold=" + onHold + ", holdReason=" + holdReason + "]";
      }

      ConnectionTokens withHold(String reason) {
          return new ConnectionTokens(refreshToken, accessToken, expiresAt, refreshExpiresAt, true, reason);
      }
  }

  record AccessToken(String value, long expiresAt /* Unix seconds */) {
      @Override // keeps the token out of logs
      public String toString() {
          return "AccessToken[expiresAt=" + expiresAt + "]";
      }
  }

  /** The refresh token must not be sent again. Don't catch this to try again. */
  static class RefreshOnHoldException extends RuntimeException {
      /** If set, only the write failed: store these tokens. */
      ConnectionTokens newTokens;

      RefreshOnHoldException(String message) {
          super(message);
      }
  }

  /** Reads the JWT that authenticates your app to auth.claude.com. */
  String clientAssertion() throws IOException {
      return Files.readString(Path.of(System.getenv("CLIENT_ASSERTION_FILE"))).strip();
  }

  /** Reads the connection's newest tokens from your secret store. */
  ConnectionTokens loadTokens(String connectionId) throws IOException {
      throw new UnsupportedOperationException("Read the tokens from your secret store.");
  }

  /** Writes the connection's newest tokens to your secret store. */
  void saveTokens(String connectionId, ConnectionTokens tokens) throws IOException {
      throw new UnsupportedOperationException("Write the tokens to your secret store.");
  }
  ```

  ```php PHP
  const TOKEN_URL = 'https://auth.claude.com/v1/oauth/token';
  const CLIENT_ID = 'clid_01ABcDeFgHiJkLmNoPqRsTuV';
  const JWT_BEARER = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer';
  const REFRESH_MARGIN_SECONDS = 600;
  const SECOND_REQUEST_DEADLINE_SECONDS = 4; // keep this under the 10-second timeout

  final class ConnectionTokens
  {
      public function __construct(
          public readonly string $refreshToken,
          public readonly string $accessToken,
          public readonly int $expiresAt, // Unix seconds
          public readonly int $refreshExpiresAt, // Unix seconds
          public readonly bool $onHold = false, // true: the refresh token might have been used
          public readonly ?string $holdReason = null, // 'lost' or 'invalid_grant'
      ) {}

      /** Keeps the tokens out of var_dump and print_r. */
      public function __debugInfo(): array
      {
          return ['expiresAt' => $this->expiresAt, 'onHold' => $this->onHold, 'holdReason' => $this->holdReason];
      }

      public function withHold(string $reason): self
      {
          return new self(
              refreshToken: $this->refreshToken,
              accessToken: $this->accessToken,
              expiresAt: $this->expiresAt,
              refreshExpiresAt: $this->refreshExpiresAt,
              onHold: true,
              holdReason: $reason,
          );
      }
  }

  /** The refresh token must not be sent again. Don't catch this to try again. */
  final class RefreshOnHoldException extends \RuntimeException
  {
      /** If set, only the write failed: store these tokens. */
      public ?ConnectionTokens $newTokens = null;
  }

  /** Reads the JWT that authenticates your app to auth.claude.com. */
  function clientAssertion(): string
  {
      $jwt = file_get_contents((string) getenv('CLIENT_ASSERTION_FILE'))
          ?: throw new \RuntimeException('Cannot read the client assertion file');
      return trim($jwt);
  }

  /** Reads the connection's newest tokens from your secret store. */
  function loadTokens(string $connectionId): ConnectionTokens
  {
      throw new \LogicException('Read the tokens from your secret store.');
  }

  /** Writes the connection's newest tokens to your secret store. */
  function saveTokens(string $connectionId, ConnectionTokens $tokens): void
  {
      throw new \LogicException('Write the tokens to your secret store.');
  }
  ```

  ```ruby Ruby
  require "json"
  require "net/http"

  TOKEN_URL = URI("https://auth.claude.com/v1/oauth/token")
  CLIENT_ID = "clid_01ABcDeFgHiJkLmNoPqRsTuV"
  JWT_BEARER = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
  REFRESH_MARGIN_SECONDS = 600
  SECOND_REQUEST_DEADLINE_SECONDS = 4 # keep this under the 10-second read timeout

  ConnectionTokens = Data.define(
    :refresh_token,
    :access_token,
    :expires_at, # Unix seconds
    :refresh_expires_at, # Unix seconds
    :on_hold, # true: the refresh token might have been used
    :hold_reason # "lost" or "invalid_grant"
  ) do
    def initialize(on_hold: false, hold_reason: nil, **) = super

    # Menjaga agar token tidak masuk ke log.
    def inspect = "#<data ConnectionTokens expires_at=#{expires_at} on_hold=#{on_hold} hold_reason=#{hold_reason.inspect}>"
    alias_method :to_s, :inspect
  end

  # Refresh token tidak boleh dikirim lagi. Jangan tangkap (rescue) ini untuk mencoba lagi.
  # Jika new_tokens diatur, hanya penulisan yang gagal: simpan token tersebut.
  class RefreshOnHoldError < StandardError
    attr_accessor :new_tokens
  end

  # Membaca JWT yang mengautentikasi aplikasi Anda ke auth.claude.com.
  def client_assertion = File.read(ENV.fetch("CLIENT_ASSERTION_FILE")).strip

  # Membaca token terbaru koneksi dari penyimpanan rahasia Anda.
  def load_tokens(connection_id)
    raise NotImplementedError, "Read the tokens from your secret store."
  end

  # Menulis token terbaru koneksi ke penyimpanan rahasia Anda.
  def save_tokens(connection_id, tokens)
    raise NotImplementedError, "Write the tokens to your secret store."
  end
  ```
</CodeGroup>

Fungsi penyegaran berikut menggunakan penyiapan tersebut:

<CodeGroup exclude="shell:cURL, shell:CLI">
  <CodeGroupItem language="cURL">
    Penyegaran ini memerlukan lebih banyak logika daripada satu perintah shell. Tulis dalam bahasa aplikasi Anda.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Penyegaran ini memerlukan lebih banyak logika daripada satu perintah shell. Tulis dalam bahasa aplikasi Anda.
  </CodeGroupItem>

  ```python Python
  connection_locks: defaultdict[str, threading.Lock] = defaultdict(threading.Lock)


  def error_body(response: httpx2.Response) -> dict:
      try:
          body = response.json()
      except ValueError:
          return {}
      return body if isinstance(body, dict) else {}


  def is_lost(response: httpx2.Response) -> bool:
      """True for a 5xx response that can follow a refresh that took effect."""
      if response.status_code < 500:
          return False
      refused = (
          response.status_code == 503
          and error_body(response).get("type") == "error"
          and "retry-after" in response.headers
      )
      return not refused


  def hold_error(connection_id: str, reason: str) -> RefreshOnHoldError:
      return RefreshOnHoldError(
          f"Connection {connection_id} is on hold. {reason} Don't send its refresh token"
          " again: that can end the customer's link. See"
          ' "If a refresh fails" in the Linked billing docs.'
      )


  def refresh_connection(connection_id: str, *, force: bool = False) -> tuple[str, int]:
      """Returns a current access token and its expiry time in Unix seconds.

      Call this from your schedule. Pass force=True to refresh a token that isn't
      close to its expiry. Raises RefreshOnHoldError when the refresh token must not be
      sent again, and httpx2.HTTPStatusError for a refusal that keeps it.
      """
      # Lock ini hanya berlaku di dalam satu proses.
      with connection_locks[connection_id]:
          tokens = load_tokens(connection_id)
          if tokens.on_hold:
              raise hold_error(connection_id, f"Reason: {tokens.hold_reason}.")
          if not force and tokens.expires_at - time.time() > REFRESH_MARGIN_SECONDS:
              return tokens.access_token, tokens.expires_at
          request = {
              "grant_type": "refresh_token",
              "refresh_token": tokens.refresh_token,
              "client_id": CLIENT_ID,
              "client_assertion_type": JWT_BEARER,
              "client_assertion": client_assertion(),
          }
          # Pasang hold terlebih dahulu agar hold tetap ada jika proses berhenti di tengah refresh.
          held = replace(tokens, on_hold=True, hold_reason="lost")
          save_tokens(connection_id, held)
          issued_at = int(time.time())
          started = time.monotonic()
          # Jangan tambahkan retry: retry yang terlambat akan memutus tautan pelanggan.
          try:
              response = httpx2.post(TOKEN_URL, json=request, timeout=REQUEST_TIMEOUT)
              lost = is_lost(response)
          except (httpx2.ConnectError, httpx2.ConnectTimeout):
              # Refresh token tidak pernah keluar dari proses ini, jadi lepaskan hold-nya.
              save_tokens(connection_id, tokens)
              raise
          except httpx2.TransportError:
              lost = True
          if lost:
              if time.monotonic() - started > SECOND_REQUEST_DEADLINE_SECONDS:
                  raise hold_error(connection_id, "A refresh got no usable answer.")
              try:
                  response = httpx2.post(TOKEN_URL, json=request, timeout=REQUEST_TIMEOUT)
              except httpx2.TransportError:
                  raise hold_error(
                      connection_id, "Two refreshes got no answer."
                  ) from None
              if response.status_code != 200:
                  raise hold_error(connection_id, "The second refresh failed.")
          if error_body(response).get("error") == "invalid_grant":
              save_tokens(connection_id, replace(held, hold_reason="invalid_grant"))
              raise hold_error(connection_id, "The refresh returned invalid_grant.")
          if response.status_code != 200:
              # Penolakan yang tetap mempertahankan refresh token, jadi lepaskan hold-nya.
              save_tokens(connection_id, tokens)
              response.raise_for_status()
          body = response.json()
          tokens = ConnectionTokens(
              refresh_token=body["refresh_token"],
              access_token=body["access_token"],
              expires_at=issued_at + body["expires_in"],
              refresh_expires_at=issued_at + body["refresh_token_expires_in"],
          )
          # Ulangi hanya operasi penulisan. Jangan lakukan refresh lagi.
          for attempt in range(5):
              try:
                  save_tokens(connection_id, tokens)
                  return tokens.access_token, tokens.expires_at
              except OSError:  # your secret store's error type
                  if attempt < 4:
                      time.sleep(2**attempt)
          error = hold_error(
              connection_id,
              "The refresh succeeded, but the new tokens could not be saved.",
          )
          error.new_tokens = tokens
          raise error
  ```

  ```typescript TypeScript
  const connectionLocks = new Map<string, Promise<unknown>>();

  function withConnectionLock<T>(connectionId: string, work: () => Promise<T>): Promise<T> {
    const result = (connectionLocks.get(connectionId) ?? Promise.resolve()).then(work, work);
    connectionLocks.set(
      connectionId,
      result.catch(() => {})
    );
    return result;
  }

  class NotSent extends Error {}

  interface TokenResponse {
    status: number;
    headers: IncomingHttpHeaders;
    text: string;
  }

  function post(body: string): Promise<TokenResponse> {
    return new Promise((resolve, reject) => {
      let connected = false;
      const req = request(
        TOKEN_URL,
        {
          method: "POST",
          agent: false, // a new connection for each request
          headers: { "content-type": "application/json" },
          signal: AbortSignal.timeout(10_000)
        },
        (response) => {
          let text = "";
          response.setEncoding("utf8");
          response.on("data", (chunk: string) => (text += chunk));
          response.on("end", () =>
            resolve({ status: response.statusCode!, headers: response.headers, text })
          );
          response.on("error", reject);
        }
      );
      const connectTimer = setTimeout(
        () => req.destroy(new Error("No connection in 2 seconds")),
        2_000
      );
      req.on("socket", (socket) =>
        socket.once("secureConnect", () => {
          connected = true;
          clearTimeout(connectTimer);
        })
      );
      req.on("error", (error) => {
        clearTimeout(connectTimer);
        reject(connected ? error : new NotSent(error.message, { cause: error }));
      });
      req.end(body);
    });
  }

  function errorBody(response: TokenResponse): Record<string, unknown> {
    try {
      const body: unknown = JSON.parse(response.text);
      return typeof body === "object" && body !== null ? (body as Record<string, unknown>) : {};
    } catch {
      return {};
    }
  }

  /** True for a 5xx response that can follow a refresh that took effect. */
  function isLost(response: TokenResponse): boolean {
    if (response.status < 500) {
      return false;
    }
    const refused =
      response.status === 503 &&
      errorBody(response).type === "error" &&
      "retry-after" in response.headers;
    return !refused;
  }

  function holdError(
    connectionId: string,
    reason: string,
    newTokens?: ConnectionTokens
  ): RefreshOnHoldError {
    return new RefreshOnHoldError(
      `Connection ${connectionId} is on hold. ${reason} Don't send its refresh token again: ` +
        'that can end the customer\'s link. See "If a refresh fails" in the Linked billing docs.',
      newTokens
    );
  }

  /**
   * Returns a current access token and its expiry time in Unix seconds.
   *
   * Call this from your schedule. Pass force: true to refresh a token that isn't
   * close to its expiry. Throws RefreshOnHoldError when the refresh token must not be
   * sent again, and an Error for a refusal that keeps it.
   */
  function refreshConnection(connectionId: string, { force = false } = {}) {
    // Lock ini hanya berfungsi di dalam satu proses.
    return withConnectionLock(connectionId, async () => {
      const tokens = await loadTokens(connectionId);
      if (tokens.onHold) {
        throw holdError(connectionId, `Reason: ${tokens.holdReason}.`);
      }
      if (!force && tokens.expiresAt - Date.now() / 1000 > REFRESH_MARGIN_SECONDS) {
        return { accessToken: tokens.accessToken, expiresAt: tokens.expiresAt };
      }
      const body = JSON.stringify({
        grant_type: "refresh_token",
        refresh_token: tokens.refreshToken,
        client_id: CLIENT_ID,
        client_assertion_type: JWT_BEARER,
        client_assertion: await clientAssertion()
      });
      // Pasang hold terlebih dahulu agar hold tetap ada jika proses berhenti di tengah refresh.
      const held: ConnectionTokens = { ...tokens, onHold: true, holdReason: "lost" };
      await saveTokens(connectionId, held);
      const issuedAt = Math.floor(Date.now() / 1000);
      const started = performance.now();
      // Jangan tambahkan retry: retry yang terlambat akan memutus tautan pelanggan.
      let response: TokenResponse | undefined;
      try {
        response = await post(body);
      } catch (error) {
        if (error instanceof NotSent) {
          // Refresh token tidak pernah keluar dari proses ini, jadi lepaskan hold-nya.
          await saveTokens(connectionId, tokens);
          throw error;
        }
      }
      if (!response || isLost(response)) {
        if (performance.now() - started > SECOND_REQUEST_DEADLINE_MS) {
          throw holdError(connectionId, "A refresh got no usable answer.");
        }
        try {
          response = await post(body);
        } catch {
          throw holdError(connectionId, "Two refreshes got no answer.");
        }
        if (response.status !== 200) {
          throw holdError(connectionId, "The second refresh failed.");
        }
      }
      if (errorBody(response).error === "invalid_grant") {
        await saveTokens(connectionId, { ...held, holdReason: "invalid_grant" });
        throw holdError(connectionId, "The refresh returned invalid_grant.");
      }
      if (response.status !== 200) {
        // Penolakan yang tetap mempertahankan refresh token, jadi lepaskan hold-nya.
        await saveTokens(connectionId, tokens);
        throw new Error(`Refresh failed: ${response.status} ${response.text}`);
      }
      const answer = JSON.parse(response.text);
      const newTokens: ConnectionTokens = {
        refreshToken: answer.refresh_token,
        accessToken: answer.access_token,
        expiresAt: issuedAt + answer.expires_in,
        refreshExpiresAt: issuedAt + answer.refresh_token_expires_in
      };
      // Ulangi hanya operasi tulis. Jangan lakukan refresh lagi.
      for (let attempt = 0; attempt < 5; attempt++) {
        try {
          await saveTokens(connectionId, newTokens);
          return { accessToken: newTokens.accessToken, expiresAt: newTokens.expiresAt };
        } catch {
          // operasi tulis gagal
          if (attempt < 4) {
            await new Promise((wake) => setTimeout(wake, 2 ** attempt * 1000));
          }
        }
      }
      throw holdError(
        connectionId,
        "The refresh succeeded, but the new tokens could not be saved.",
        newTokens
      );
    });
  }
  ```

  ```csharp C#
  static partial class Connections
  {
      static readonly ConcurrentDictionary<string, SemaphoreSlim> ConnectionLocks = new();

      static readonly HttpClient Http = new(new SocketsHttpHandler
      {
          ConnectTimeout = TimeSpan.FromSeconds(2),
          AllowAutoRedirect = false,
          PooledConnectionLifetime = TimeSpan.Zero, // a new connection for each request
      })
      { Timeout = Timeout.InfiniteTimeSpan }; // Post sets the 10-second timeout

      static async Task<(HttpResponseMessage? Response, string Body, Exception? Error, bool Connected)> Post(
          string body)
      {
          using var request = new HttpRequestMessage(HttpMethod.Post, TokenUrl)
          {
              Content = new StringContent(body, Encoding.UTF8, "application/json"),
          };
          using var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(10));
          try
          {
              var response = await Http.SendAsync(request, timeout.Token);
              return (response, await response.Content.ReadAsStringAsync(timeout.Token), null, true);
          }
          catch (HttpRequestException e) when (e.HttpRequestError is HttpRequestError.ConnectionError
              or HttpRequestError.NameResolutionError or HttpRequestError.SecureConnectionError)
          {
              return (null, "", e, false);
          }
          catch (TaskCanceledException e) when (!timeout.IsCancellationRequested)
          {
              return (null, "", e, false); // the 2-second connect timeout
          }
          catch (Exception e) when (e is HttpRequestException or TaskCanceledException)
          {
              return (null, "", e, true); // a dropped connection or a timeout
          }
      }

      static JsonElement ErrorBody(string body)
      {
          try
          {
              using var document = JsonDocument.Parse(body);
              var parsed = document.RootElement;
              return parsed.ValueKind == JsonValueKind.Object ? parsed.Clone() : default;
          }
          catch (JsonException)
          {
              return default;
          }
      }

      static string? ErrorField(string body, string name) =>
          ErrorBody(body) is { ValueKind: JsonValueKind.Object } error && error.TryGetProperty(name, out var value)
              ? value.ToString()
              : null;

      /// <summary>True untuk respons 5xx yang dapat muncul setelah refresh yang berhasil diterapkan.</summary>
      static bool IsLost(HttpResponseMessage response, string body)
      {
          if ((int)response.StatusCode < 500) return false;
          var refused = (int)response.StatusCode == 503
              && ErrorField(body, "type") == "error"
              && response.Headers.Contains("retry-after");
          return !refused;
      }

      static RefreshOnHoldException HoldError(string connectionId, string reason) => new(
          $"Connection {connectionId} is on hold. {reason} Don't send its refresh token again: " +
          "that can end the customer's link. See \"If a refresh fails\" in the Linked billing docs.");

      /// <summary>
      /// Mengembalikan token akses saat ini dan waktu kedaluwarsanya dalam detik Unix.
      /// Panggil ini dari jadwal Anda. Berikan force: true untuk me-refresh token yang belum
      /// mendekati kedaluwarsa. Melempar RefreshOnHoldException saat refresh token tidak boleh
      /// dikirim lagi, dan HttpRequestException untuk penolakan yang tetap mempertahankannya.
      /// </summary>
      public static async Task<(string AccessToken, long ExpiresAt)> RefreshConnection(
          string connectionId, bool force = false)
      {
          // Lock ini hanya berfungsi di dalam satu proses.
          var connectionLock = ConnectionLocks.GetOrAdd(connectionId, _ => new SemaphoreSlim(1, 1));
          await connectionLock.WaitAsync();
          try
          {
              var tokens = await LoadTokens(connectionId);
              if (tokens.OnHold) throw HoldError(connectionId, $"Reason: {tokens.HoldReason}.");
              if (!force && tokens.ExpiresAt - DateTimeOffset.UtcNow.ToUnixTimeSeconds() > RefreshMarginSeconds)
              {
                  return (tokens.AccessToken, tokens.ExpiresAt);
              }
              var request = JsonSerializer.Serialize(new Dictionary<string, string>
              {
                  ["grant_type"] = "refresh_token",
                  ["refresh_token"] = tokens.RefreshToken,
                  ["client_id"] = ClientId,
                  ["client_assertion_type"] = JwtBearer,
                  ["client_assertion"] = ClientAssertion(),
              });
              // Pasang hold dulu, agar hold tetap ada jika proses berhenti di tengah refresh.
              var held = tokens with { OnHold = true, HoldReason = "lost" };
              await SaveTokens(connectionId, held);
              var issuedAt = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
              var started = Stopwatch.StartNew();
              // Jangan tambahkan retry: retry yang terlambat memutus tautan pelanggan.
              var (response, body, error, connected) = await Post(request);
              if (!connected)
              {
                  // Refresh token tidak pernah keluar dari proses ini, jadi lepaskan hold-nya.
                  await SaveTokens(connectionId, tokens);
                  throw new HttpRequestException("Couldn't connect to auth.claude.com.", error);
              }
              if (response is null || IsLost(response, body))
              {
                  if (started.Elapsed > SecondRequestDeadline)
                      throw HoldError(connectionId, "A refresh got no usable answer.");
                  (response, body, _, _) = await Post(request);
                  if (response is null) throw HoldError(connectionId, "Two refreshes got no answer.");
                  if ((int)response.StatusCode != 200) throw HoldError(connectionId, "The second refresh failed.");
              }
              if (ErrorField(body, "error") == "invalid_grant")
              {
                  await SaveTokens(connectionId, held with { HoldReason = "invalid_grant" });
                  throw HoldError(connectionId, "The refresh returned invalid_grant.");
              }
              if ((int)response.StatusCode != 200)
              {
                  // Penolakan yang tetap mempertahankan refresh token, jadi lepaskan hold-nya.
                  await SaveTokens(connectionId, tokens);
                  throw new HttpRequestException($"Refresh failed: {(int)response.StatusCode} {body}",
                      null, response.StatusCode);
              }
              using var document = JsonDocument.Parse(body);
              var answer = document.RootElement;
              var newTokens = new ConnectionTokens(
                  RefreshToken: answer.GetProperty("refresh_token").GetString()!,
                  AccessToken: answer.GetProperty("access_token").GetString()!,
                  ExpiresAt: issuedAt + answer.GetProperty("expires_in").GetInt64(),
                  RefreshExpiresAt: issuedAt + answer.GetProperty("refresh_token_expires_in").GetInt64());
              // Coba ulang hanya penulisannya. Jangan refresh lagi.
              for (var attempt = 0; attempt < 5; attempt++)
              {
                  try
                  {
                      await SaveTokens(connectionId, newTokens);
                      return (newTokens.AccessToken, newTokens.ExpiresAt);
                  }
                  catch (IOException) // your secret store's error type
                  {
                      if (attempt < 4) await Task.Delay(TimeSpan.FromSeconds(1 << attempt));
                  }
              }
              throw new RefreshOnHoldException(HoldError(connectionId,
                  "The refresh succeeded, but the new tokens could not be saved.").Message)
              { NewTokens = newTokens };
          }
          finally
          {
              connectionLock.Release();
          }
      }
  }
  ```

  ```go Go
  var connectionLocks sync.Map

  type tokenResponse struct {
  	status int
  	header http.Header
  	body   []byte
  }

  // post mengirim refresh. connected bernilai false jika permintaan tidak pernah terkirim.
  func post(body []byte) (response *tokenResponse, connected bool, err error) {
  	request, err := http.NewRequest(http.MethodPost, tokenURL, bytes.NewReader(body))
  	if err != nil {
  		return nil, false, err
  	}
  	request.Header.Set("content-type", "application/json")
  	trace := &httptrace.ClientTrace{GotConn: func(httptrace.GotConnInfo) { connected = true }}
  	request = request.WithContext(httptrace.WithClientTrace(request.Context(), trace))
  	answer, err := httpClient.Do(request)
  	if err != nil {
  		return nil, connected, err
  	}
  	defer answer.Body.Close()
  	data, err := io.ReadAll(answer.Body)
  	if err != nil {
  		return nil, true, err
  	}
  	return &tokenResponse{answer.StatusCode, answer.Header, data}, true, nil
  }

  func errorBody(response *tokenResponse) map[string]any {
  	var body map[string]any
  	if json.Unmarshal(response.body, &body) != nil {
  		return map[string]any{}
  	}
  	return body
  }

  // isLost bernilai true untuk respons 5xx yang bisa muncul setelah refresh yang berhasil.
  func isLost(response *tokenResponse) bool {
  	if response.status < 500 {
  		return false
  	}
  	refused := response.status == 503 &&
  		errorBody(response)["type"] == "error" &&
  		response.header.Get("retry-after") != ""
  	return !refused
  }

  func holdError(connectionID, reason string) *RefreshOnHoldError {
  	return &RefreshOnHoldError{Message: fmt.Sprintf("connection %s is on hold. %s Don't send its refresh token "+
  		"again: that can end the customer's link. See \"If a refresh fails\" in the Linked billing docs.",
  		connectionID, reason)}
  }

  // refreshConnection mengembalikan token akses saat ini dan waktu kedaluwarsanya dalam
  // detik Unix. Panggil dari jadwal Anda. Berikan force=true untuk me-refresh token yang
  // belum mendekati kedaluwarsa. Mengembalikan *RefreshOnHoldError bila refresh
  // token tidak boleh dikirim lagi, dan error lain untuk penolakan yang mempertahankannya.
  func refreshConnection(connectionID string, force bool) (string, int64, error) {
  	// Lock ini hanya berfungsi di dalam satu proses.
  	lock, _ := connectionLocks.LoadOrStore(connectionID, &sync.Mutex{})
  	lock.(*sync.Mutex).Lock()
  	defer lock.(*sync.Mutex).Unlock()

  	tokens, err := loadTokens(connectionID)
  	if err != nil {
  		return "", 0, err
  	}
  	if tokens.OnHold {
  		return "", 0, holdError(connectionID, "Reason: "+tokens.HoldReason+".")
  	}
  	if !force && time.Until(time.Unix(tokens.ExpiresAt, 0)) > refreshMargin {
  		return tokens.AccessToken, tokens.ExpiresAt, nil
  	}
  	assertion, err := clientAssertion()
  	if err != nil {
  		return "", 0, err
  	}
  	body, err := json.Marshal(map[string]string{
  		"grant_type":            "refresh_token",
  		"refresh_token":         tokens.RefreshToken,
  		"client_id":             clientID,
  		"client_assertion_type": jwtBearer,
  		"client_assertion":      assertion,
  	})
  	if err != nil {
  		return "", 0, err
  	}
  	// Pasang hold dulu, agar hold tetap ada jika proses berhenti di tengah refresh.
  	held := tokens
  	held.OnHold, held.HoldReason = true, "lost"
  	if err := saveTokens(connectionID, held); err != nil {
  		return "", 0, err
  	}
  	issuedAt := time.Now().Unix()
  	started := time.Now()
  	// Jangan tambahkan retry: retry yang terlambat memutus tautan pelanggan.
  	response, connected, err := post(body)
  	if err != nil && !connected {
  		// Refresh token tidak pernah keluar dari proses ini, jadi lepaskan hold.
  		if saveErr := saveTokens(connectionID, tokens); saveErr != nil {
  			return "", 0, saveErr
  		}
  		return "", 0, err
  	}
  	if err != nil || isLost(response) {
  		if time.Since(started) > secondRequestDeadline {
  			return "", 0, holdError(connectionID, "A refresh got no usable answer.")
  		}
  		if response, _, err = post(body); err != nil {
  			return "", 0, holdError(connectionID, "Two refreshes got no answer.")
  		}
  		if response.status != 200 {
  			return "", 0, holdError(connectionID, "The second refresh failed.")
  		}
  	}
  	if errorBody(response)["error"] == "invalid_grant" {
  		held.HoldReason = "invalid_grant"
  		if err := saveTokens(connectionID, held); err != nil {
  			return "", 0, err
  		}
  		return "", 0, holdError(connectionID, "The refresh returned invalid_grant.")
  	}
  	if response.status != 200 {
  		// Penolakan yang mempertahankan refresh token, jadi lepaskan hold.
  		if err := saveTokens(connectionID, tokens); err != nil {
  			return "", 0, err
  		}
  		return "", 0, fmt.Errorf("refresh failed: %d %s", response.status, response.body)
  	}
  	var answer struct {
  		AccessToken           string `json:"access_token"`
  		RefreshToken          string `json:"refresh_token"`
  		ExpiresIn             int64  `json:"expires_in"`
  		RefreshTokenExpiresIn int64  `json:"refresh_token_expires_in"`
  	}
  	if err := json.Unmarshal(response.body, &answer); err != nil {
  		return "", 0, holdError(connectionID, "The refresh answer could not be read.")
  	}
  	tokens = ConnectionTokens{
  		RefreshToken:     answer.RefreshToken,
  		AccessToken:      answer.AccessToken,
  		ExpiresAt:        issuedAt + answer.ExpiresIn,
  		RefreshExpiresAt: issuedAt + answer.RefreshTokenExpiresIn,
  	}
  	// Ulangi hanya penulisannya. Jangan refresh lagi.
  	for attempt := range 5 {
  		if err := saveTokens(connectionID, tokens); err == nil {
  			return tokens.AccessToken, tokens.ExpiresAt, nil
  		}
  		if attempt < 4 {
  			time.Sleep(time.Second << attempt)
  		}
  	}
  	hold := holdError(connectionID, "The refresh succeeded, but the new tokens could not be saved.")
  	hold.NewTokens = &tokens
  	return "", 0, hold
  }
  ```

  ```java Java
  final Map<String, ReentrantLock> connectionLocks = new ConcurrentHashMap<>();
  final ObjectMapper mapper = new ObjectMapper();
  final HttpClient http = HttpClient.newBuilder()
      .connectTimeout(Duration.ofSeconds(2))
      .followRedirects(HttpClient.Redirect.NEVER)
      .build();

  HttpResponse<String> post(String body) throws IOException, InterruptedException {
      var request = HttpRequest.newBuilder(TOKEN_URL)
          .header("content-type", "application/json")
          .timeout(Duration.ofSeconds(10))
          .POST(HttpRequest.BodyPublishers.ofString(body))
          .build();
      return http.send(request, HttpResponse.BodyHandlers.ofString());
  }

  JsonNode errorBody(HttpResponse<String> response) {
      try {
          return mapper.readTree(response.body());
      } catch (IOException _) {
          return mapper.createObjectNode();
      }
  }

  /** True for a 5xx response that can follow a refresh that took effect. */
  boolean isLost(HttpResponse<String> response) {
      if (response.statusCode() < 500) {
          return false;
      }
      boolean refused = response.statusCode() == 503
          && errorBody(response).path("type").asText().equals("error")
          && response.headers().firstValue("retry-after").isPresent();
      return !refused;
  }

  RefreshOnHoldException holdError(String connectionId, String reason) {
      return new RefreshOnHoldException("Connection " + connectionId + " is on hold. " + reason
          + " Don't send its refresh token again: that can end the customer's link."
          + " See \"If a refresh fails\" in the Linked billing docs.");
  }

  /**
   * Returns a current access token and its expiry time in Unix seconds.
   * Call this from your schedule. Pass force = true to refresh a token that isn't
   * close to its expiry. Throws RefreshOnHoldException when the refresh token must not be
   * sent again, and IOException for a refusal that keeps it.
   */
  AccessToken refreshConnection(String connectionId, boolean force)
          throws IOException, InterruptedException {
      // Lock ini hanya berfungsi di dalam satu proses.
      var lock = connectionLocks.computeIfAbsent(connectionId, id -> new ReentrantLock());
      lock.lock();
      try {
          var tokens = loadTokens(connectionId);
          if (tokens.onHold()) {
              throw holdError(connectionId, "Reason: " + tokens.holdReason() + ".");
          }
          if (!force && tokens.expiresAt() - Instant.now().getEpochSecond() > REFRESH_MARGIN_SECONDS) {
              return new AccessToken(tokens.accessToken(), tokens.expiresAt());
          }
          var request = mapper.createObjectNode()
              .put("grant_type", "refresh_token")
              .put("refresh_token", tokens.refreshToken())
              .put("client_id", CLIENT_ID)
              .put("client_assertion_type", JWT_BEARER)
              .put("client_assertion", clientAssertion())
              .toString();
          // Pasang hold terlebih dahulu agar hold tetap ada jika proses berhenti di tengah refresh.
          var held = tokens.withHold("lost");
          saveTokens(connectionId, held);
          long issuedAt = Instant.now().getEpochSecond();
          long started = System.nanoTime();
          // Jangan tambahkan retry: retry yang terlambat akan memutus tautan pelanggan.
          HttpResponse<String> response = null;
          try {
              response = post(request);
          } catch (ConnectException | HttpConnectTimeoutException | SSLHandshakeException e) {
              // Refresh token tidak pernah keluar dari proses ini, jadi lepaskan hold-nya.
              saveTokens(connectionId, tokens);
              throw e;
          } catch (IOException _) {
              // Koneksi terputus, atau tidak ada jawaban yang datang tepat waktu.
          }
          if (response == null || isLost(response)) {
              if (Duration.ofNanos(System.nanoTime() - started).compareTo(SECOND_REQUEST_DEADLINE) > 0) {
                  throw holdError(connectionId, "A refresh got no usable answer.");
              }
              try {
                  response = post(request);
              } catch (IOException _) {
                  throw holdError(connectionId, "Two refreshes got no answer.");
              }
              if (response.statusCode() != 200) {
                  throw holdError(connectionId, "The second refresh failed.");
              }
          }
          if (errorBody(response).path("error").asText().equals("invalid_grant")) {
              saveTokens(connectionId, held.withHold("invalid_grant"));
              throw holdError(connectionId, "The refresh returned invalid_grant.");
          }
          if (response.statusCode() != 200) {
              // Penolakan yang mempertahankan refresh token, jadi lepaskan hold-nya.
              saveTokens(connectionId, tokens);
              throw new IOException("Refresh failed: " + response.statusCode() + " " + response.body());
          }
          var answer = mapper.readTree(response.body());
          var newTokens = new ConnectionTokens(
              answer.get("refresh_token").asText(),
              answer.get("access_token").asText(),
              issuedAt + answer.get("expires_in").asLong(),
              issuedAt + answer.get("refresh_token_expires_in").asLong(),
              false,
              null);
          // Ulangi hanya operasi tulis. Jangan lakukan refresh lagi.
          for (int attempt = 0; attempt < 5; attempt++) {
              try {
                  saveTokens(connectionId, newTokens);
                  return new AccessToken(newTokens.accessToken(), newTokens.expiresAt());
              } catch (IOException _) { // your secret store's error type
                  if (attempt < 4) {
                      Thread.sleep(Duration.ofSeconds(1L << attempt));
                  }
              }
          }
          var error = holdError(connectionId, "The refresh succeeded, but the new tokens could not be saved.");
          error.newTokens = newTokens;
          throw error;
      } finally {
          lock.unlock();
      }
  }
  ```

  ```php PHP
  /**
   * Sends the refresh. Returns a string, curl's error, when the request never left this process.
   *
   * @return array{status: int, headers: list<string>, body: string}|false|string false: no answer
   */
  function post(string $body): array|false|string
  {
      $headers = [];
      $curl = curl_init(TOKEN_URL);
      curl_setopt_array($curl, [
          CURLOPT_POST => true,
          CURLOPT_POSTFIELDS => $body,
          CURLOPT_HTTPHEADER => ['content-type: application/json'],
          CURLOPT_RETURNTRANSFER => true,
          CURLOPT_CONNECTTIMEOUT => 2,
          CURLOPT_TIMEOUT => 10,
          CURLOPT_FOLLOWLOCATION => false,
          CURLOPT_FORBID_REUSE => true, // a new connection for each request
          CURLOPT_HEADERFUNCTION => function ($curl, string $line) use (&$headers): int {
              $headers[] = strtolower(trim($line));
              return strlen($line);
          },
      ]);
      $text = curl_exec($curl);
      if (!is_string($text)) {
          // Belum ada koneksi TLS berarti belum ada yang dikirim.
          return curl_getinfo($curl, CURLINFO_APPCONNECT_TIME_T) > 0 ? false : curl_error($curl);
      }
      return ['status' => curl_getinfo($curl, CURLINFO_RESPONSE_CODE), 'headers' => $headers, 'body' => $text];
  }

  /**
   * @param array{status: int, headers: list<string>, body: string} $response
   * @return array<mixed>
   */
  function errorBody(array $response): array
  {
      $body = json_decode($response['body'], associative: true);
      return is_array($body) ? $body : [];
  }

  /**
   * True for a 5xx response that can follow a refresh that took effect.
   *
   * @param array{status: int, headers: list<string>, body: string} $response
   */
  function isLost(array $response): bool
  {
      if ($response['status'] < 500) {
          return false;
      }
      $refused = $response['status'] === 503
          && (errorBody($response)['type'] ?? null) === 'error'
          && preg_grep('/^retry-after:/', $response['headers']);
      return !$refused;
  }

  function holdError(string $connectionId, string $reason): RefreshOnHoldException
  {
      return new RefreshOnHoldException(
          "Connection {$connectionId} is on hold. {$reason} Don't send its refresh token again: "
          . "that can end the customer's link. See \"If a refresh fails\" in the Linked billing docs."
      );
  }

  /**
   * Returns a current access token and its expiry time in Unix seconds.
   *
   * Call this from your schedule. Pass force: true to refresh a token that isn't
   * close to its expiry. Throws RefreshOnHoldException when the refresh token must not be
   * sent again, and \RuntimeException for a refusal that keeps it.
   *
   * @return array{string, int}
   */
  function refreshConnection(string $connectionId, bool $force = false): array
  {
      // Lock ini hanya berfungsi di satu mesin.
      $lock = fopen(sys_get_temp_dir() . '/refresh-' . hash('sha256', $connectionId) . '.lock', 'c')
          ?: throw new \RuntimeException('Cannot open the lock file');
      flock($lock, LOCK_EX);
      try {
          $tokens = loadTokens($connectionId);
          if ($tokens->onHold) {
              throw holdError($connectionId, "Reason: {$tokens->holdReason}.");
          }
          if (!$force && $tokens->expiresAt - time() > REFRESH_MARGIN_SECONDS) {
              return [$tokens->accessToken, $tokens->expiresAt];
          }
          $request = json_encode([
              'grant_type' => 'refresh_token',
              'refresh_token' => $tokens->refreshToken,
              'client_id' => CLIENT_ID,
              'client_assertion_type' => JWT_BEARER,
              'client_assertion' => clientAssertion(),
          ], JSON_THROW_ON_ERROR);
          // Tahan lebih dulu, agar penahanan tetap ada jika proses berhenti di tengah refresh.
          $held = $tokens->withHold('lost');
          saveTokens($connectionId, $held);
          $issuedAt = time();
          $started = hrtime(true);
          // Jangan tambahkan retry: retry yang terlambat akan memutus tautan pelanggan.
          $response = post($request);
          if (is_string($response)) {
              // Refresh token tidak pernah keluar dari proses ini, jadi lepaskan penahanannya.
              saveTokens($connectionId, $tokens);
              throw new \RuntimeException("Could not connect to auth.claude.com: {$response}");
          }
          if ($response === false || isLost($response)) {
              if ((hrtime(true) - $started) / 1e9 > SECOND_REQUEST_DEADLINE_SECONDS) {
                  throw holdError($connectionId, 'A refresh got no usable answer.');
              }
              $response = post($request);
              if (!is_array($response)) {
                  throw holdError($connectionId, 'Two refreshes got no answer.');
              }
              if ($response['status'] !== 200) {
                  throw holdError($connectionId, 'The second refresh failed.');
              }
          }
          if ((errorBody($response)['error'] ?? null) === 'invalid_grant') {
              saveTokens($connectionId, $held->withHold('invalid_grant'));
              throw holdError($connectionId, 'The refresh returned invalid_grant.');
          }
          if ($response['status'] !== 200) {
              // Penolakan yang tetap mempertahankan refresh token, jadi lepaskan penahanannya.
              saveTokens($connectionId, $tokens);
              throw new \RuntimeException("Refresh failed: {$response['status']} {$response['body']}");
          }
          /**
           * @var array{
           *     access_token: string,
           *     refresh_token: string,
           *     expires_in: int,
           *     refresh_token_expires_in: int,
           * } $answer
           */
          $answer = json_decode($response['body'], associative: true, flags: JSON_THROW_ON_ERROR);
          $newTokens = new ConnectionTokens(
              refreshToken: $answer['refresh_token'],
              accessToken: $answer['access_token'],
              expiresAt: $issuedAt + $answer['expires_in'],
              refreshExpiresAt: $issuedAt + $answer['refresh_token_expires_in'],
          );
          // Ulangi hanya operasi tulis. Jangan refresh lagi.
          for ($attempt = 0; $attempt < 5; $attempt++) {
              try {
                  saveTokens($connectionId, $newTokens);
                  return [$newTokens->accessToken, $newTokens->expiresAt];
              } catch (\RuntimeException) { // your secret store's error type
                  if ($attempt < 4) {
                      sleep(2 ** $attempt);
                  }
              }
          }
          $error = holdError($connectionId, 'The refresh succeeded, but the new tokens could not be saved.');
          $error->newTokens = $newTokens;
          throw $error;
      } finally {
          flock($lock, LOCK_UN);
          fclose($lock);
      }
  }
  ```

  ```ruby Ruby
  CONNECTION_LOCKS = Hash.new { |locks, connection_id| locks[connection_id] = Mutex.new }
  LOCKS_GUARD = Mutex.new

  # Memunculkan error sebelum permintaan dikirim jika tidak dapat terhubung.
  def open_connection
    Net::HTTP.start(TOKEN_URL.host, TOKEN_URL.port, use_ssl: true,
      open_timeout: 2, read_timeout: 10, write_timeout: 10, max_retries: 0)
  end

  def post(http, body)
    http.post(TOKEN_URL.path, body, "content-type" => "application/json")
  ensure
    http.finish
  end

  def error_body(response)
    body = JSON.parse(response.body.to_s)
    body.is_a?(Hash) ? body : {}
  rescue JSON::ParserError
    {}
  end

  # True untuk respons 5xx yang dapat muncul setelah refresh yang sudah berlaku.
  def lost?(response)
    return false if response.code.to_i < 500

    refused = response.code == "503" &&
      error_body(response)["type"] == "error" &&
      response.key?("retry-after")
    !refused
  end

  def hold_error(connection_id, reason)
    RefreshOnHoldError.new(
      "Connection #{connection_id} is on hold. #{reason} Don't send its refresh token again: " \
      "that can end the customer's link. See \"If a refresh fails\" in the Linked billing docs."
    )
  end

  # Mengembalikan token akses saat ini dan waktu kedaluwarsanya dalam detik Unix.
  #
  # Panggil ini dari jadwal Anda. Berikan force: true untuk me-refresh token yang belum
  # mendekati kedaluwarsa. Memunculkan RefreshOnHoldError jika refresh token tidak boleh
  # dikirim lagi, dan RuntimeError untuk penolakan yang tetap mempertahankannya.
  def refresh_connection(connection_id, force: false)
    # Lock ini hanya berfungsi di dalam satu proses.
    LOCKS_GUARD.synchronize { CONNECTION_LOCKS[connection_id] }.synchronize do
      tokens = load_tokens(connection_id)
      raise hold_error(connection_id, "Reason: #{tokens.hold_reason}.") if tokens.on_hold
      if !force && tokens.expires_at - Time.now.to_i > REFRESH_MARGIN_SECONDS
        return tokens.access_token, tokens.expires_at
      end

      request = {
        grant_type: "refresh_token",
        refresh_token: tokens.refresh_token,
        client_id: CLIENT_ID,
        client_assertion_type: JWT_BEARER,
        client_assertion:
      }.to_json
      # Tahan dulu, agar penahanan tetap ada jika proses berhenti di tengah refresh.
      held = tokens.with(on_hold: true, hold_reason: "lost")
      save_tokens(connection_id, held)
      issued_at = Time.now.to_i
      started = Process.clock_gettime(Process::CLOCK_MONOTONIC)
      # Jangan tambahkan retry: retry yang terlambat memutus tautan pelanggan.
      begin
        http = open_connection
      rescue
        # Refresh token tidak pernah keluar dari proses ini, jadi lepaskan penahanan.
        save_tokens(connection_id, tokens)
        raise
      end
      begin
        response = post(http, request)
        lost = lost?(response)
      rescue
        lost = true
      end
      if lost
        if Process.clock_gettime(Process::CLOCK_MONOTONIC) - started > SECOND_REQUEST_DEADLINE_SECONDS
          raise hold_error(connection_id, "A refresh got no usable answer.")
        end
        begin
          response = post(open_connection, request)
        rescue
          raise hold_error(connection_id, "Two refreshes got no answer.")
        end
        raise hold_error(connection_id, "The second refresh failed.") unless response.code == "200"
      end
      if error_body(response)["error"] == "invalid_grant"
        save_tokens(connection_id, held.with(hold_reason: "invalid_grant"))
        raise hold_error(connection_id, "The refresh returned invalid_grant.")
      end
      unless response.code == "200"
        # Penolakan yang tetap mempertahankan refresh token, jadi lepaskan penahanan.
        save_tokens(connection_id, tokens)
        raise "Refresh failed: #{response.code} #{response.body}"
      end
      body = JSON.parse(response.body)
      tokens = ConnectionTokens.new(
        refresh_token: body.fetch("refresh_token"),
        access_token: body.fetch("access_token"),
        expires_at: issued_at + body.fetch("expires_in"),
        refresh_expires_at: issued_at + body.fetch("refresh_token_expires_in")
      )
      # Ulangi hanya penulisan. Jangan refresh lagi.
      5.times do |attempt|
        save_tokens(connection_id, tokens)
        return tokens.access_token, tokens.expires_at
      rescue IOError, SystemCallError # your secret store's error types
        sleep(2**attempt) if attempt < 4
      end
      error = hold_error(connection_id, "The refresh succeeded, but the new tokens could not be saved.")
      error.new_tokens = tokens
      raise error
    end
  end
  ```
</CodeGroup>

### Jika kunci API dapat menjangkau proses

Bagian ini hanya untuk proses di mana `ANTHROPIC_API_KEY` mungkin diatur di samping token akses pelanggan. Klien-klien berikut mengirim kunci tersebut sebagai pengganti token:

* CLI `ant`
* klien SDK yang membaca token dari `ANTHROPIC_AUTH_TOKEN`

Klien SDK yang diberi token saat Anda membangunnya hanya mengirim token. Klien lain dapat mengirim keduanya. Kunci tetap diutamakan, kecuali pada endpoint Models, di mana permintaan dapat ditolak. Ketika kunci terkirim, Claude API mengautentikasi permintaan dengannya, sehingga permintaan tidak terbatas pada pelanggan tersebut.

Sebagai pengaman dalam proses semacam itu, kirim setiap permintaan dengan header `anthropic-user-profile-id`, `billing_policy` dengan `bill_to: "user_profile"`, dan beta header `user-profiles-billing-2026-10-01`. Kemudian, permintaan yang terkirim dengan kunci memiliki salah satu hasil berikut:

* **Dengan header dan `bill_to: "user_profile"`:** Permintaan gagal, atau menagih pelanggan yang disebutkan oleh header.
* **Dengan header saja, atau tanpa keduanya:** Anthropic menagihkannya kepada Anda.

### Saat Anda menulis setiap token akses baru ke sandbox

Back end Anda mengirim setiap token baru ke kode di sandbox, melalui saluran yang Anda bangun. Kode tersebut berjalan sebagai pengguna agen dan menulis token ke direktori `credentials` dengan mode `0700`. Kode ini menulis file baru dengan mode `0600` dan mengganti nama file tersebut menimpa yang lama, sehingga agen tidak pernah membaca setengah file. Fungsi ini melakukan hal tersebut:

<CodeGroup exclude="shell:cURL, shell:CLI">
  <CodeGroupItem language="cURL">
    Tulis file dengan kode aplikasi Anda, yang berjalan di sandbox sebagai pengguna agen.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Tulis file dengan kode aplikasi Anda, yang berjalan di sandbox sebagai pengguna agen.
  </CodeGroupItem>

  ```python Python
  import json
  import os
  import tempfile
  from pathlib import Path


  def write_credentials_file(
      config_dir: Path, profile: str, token: str, expires_at: int
  ) -> None:
      """Run this in the sandbox, as the agent's user."""
      credentials_dir = config_dir / "credentials"
      credentials_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
      body = {"type": "oauth_token", "access_token": token, "expires_at": expires_at}
      handle, temporary_path = tempfile.mkstemp(dir=credentials_dir)  # mode 0600
      with os.fdopen(handle, "w") as temporary_file:
          json.dump(body, temporary_file)
      os.replace(temporary_path, credentials_dir / f"{profile}.json")
  ```

  ```typescript TypeScript
  import { mkdir, rename, writeFile } from "node:fs/promises";
  import { join } from "node:path";

  /** Run this in the sandbox, as the agent's user. */
  async function writeCredentialsFile(
    configDir: string,
    profile: string,
    token: string,
    expiresAt: number
  ) {
    const credentialsDir = join(configDir, "credentials");
    await mkdir(credentialsDir, { mode: 0o700, recursive: true });
    const body = { type: "oauth_token", access_token: token, expires_at: expiresAt };
    const temporaryPath = join(credentialsDir, `.${crypto.randomUUID()}.tmp`);
    await writeFile(temporaryPath, JSON.stringify(body), { mode: 0o600, flag: "wx" });
    await rename(temporaryPath, join(credentialsDir, `${profile}.json`));
  }
  ```

  ```csharp C#
  using System.Text.Json;

  /// <summary>Jalankan ini di sandbox, sebagai pengguna milik agen.</summary>
  static void WriteCredentialsFile(string configDir, string profile, string token, long expiresAt)
  {
      var credentialsDir = Path.Combine(configDir, "credentials");
      Directory.CreateDirectory(credentialsDir, UnixFileMode.UserRead | UnixFileMode.UserWrite | UnixFileMode.UserExecute);
      var body = new Dictionary<string, object>
      {
          ["type"] = "oauth_token",
          ["access_token"] = token,
          ["expires_at"] = expiresAt,
      };
      var temporaryPath = Path.Combine(credentialsDir, $".{Guid.NewGuid()}.tmp");
      using (var temporaryFile = new FileStream(temporaryPath, new FileStreamOptions
      {
          Mode = FileMode.CreateNew,
          Access = FileAccess.Write,
          UnixCreateMode = UnixFileMode.UserRead | UnixFileMode.UserWrite,
      }))
      {
          JsonSerializer.Serialize(temporaryFile, body);
      }
      File.Move(temporaryPath, Path.Combine(credentialsDir, $"{profile}.json"), overwrite: true);
  }
  ```

  ```go Go
  import (
  	"encoding/json"
  	"os"
  	"path/filepath"
  )

  // writeCredentialsFile berjalan di sandbox, sebagai pengguna milik agen.
  func writeCredentialsFile(configDir, profile, token string, expiresAt int64) error {
  	credentialsDir := filepath.Join(configDir, "credentials")
  	if err := os.MkdirAll(credentialsDir, 0o700); err != nil {
  		return err
  	}
  	body, err := json.Marshal(map[string]any{"type": "oauth_token", "access_token": token, "expires_at": expiresAt})
  	if err != nil {
  		return err
  	}
  	temporaryFile, err := os.CreateTemp(credentialsDir, ".tmp-*") // mode 0600
  	if err != nil {
  		return err
  	}
  	defer os.Remove(temporaryFile.Name()) // does nothing once the rename is done
  	if _, err := temporaryFile.Write(body); err != nil {
  		temporaryFile.Close()
  		return err
  	}
  	if err := temporaryFile.Close(); err != nil {
  		return err
  	}
  	return os.Rename(temporaryFile.Name(), filepath.Join(credentialsDir, profile+".json"))
  }
  ```

  ```java Java
  import module java.base;
  import com.fasterxml.jackson.databind.ObjectMapper; // Jackson comes with the Anthropic SDK

  /** Run this in the sandbox, as the agent's user. */
  void writeCredentialsFile(Path configDir, String profile, String token, long expiresAt) throws IOException {
      var credentialsDir = Files.createDirectories(configDir.resolve("credentials"),
          PosixFilePermissions.asFileAttribute(PosixFilePermissions.fromString("rwx------")));
      var body = Map.of("type", "oauth_token", "access_token", token, "expires_at", expiresAt);
      var temporaryPath = Files.createTempFile(credentialsDir, ".", ".tmp"); // mode 0600
      Files.writeString(temporaryPath, new ObjectMapper().writeValueAsString(body));
      Files.move(temporaryPath, credentialsDir.resolve(profile + ".json"),
          StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING);
  }
  ```

  ```php PHP
  /** Run this in the sandbox, as the agent's user. */
  function writeCredentialsFile(string $configDir, string $profile, string $token, int $expiresAt): void
  {
      $credentialsDir = "{$configDir}/credentials";
      if (!is_dir($credentialsDir) && !mkdir($credentialsDir, 0700, recursive: true)) {
          throw new \RuntimeException("Cannot create {$credentialsDir}");
      }
      $credentials = ['type' => 'oauth_token', 'access_token' => $token, 'expires_at' => $expiresAt];
      $body = json_encode($credentials, JSON_THROW_ON_ERROR);
      $temporaryPath = tempnam($credentialsDir, '.tmp'); // mode 0600
      if ($temporaryPath === false || dirname($temporaryPath) !== realpath($credentialsDir)) {
          throw new \RuntimeException("Cannot create a file in {$credentialsDir}"); // tempnam can fall back to /tmp
      }
      $finalPath = "{$credentialsDir}/{$profile}.json";
      if (file_put_contents($temporaryPath, $body) === false || !rename($temporaryPath, $finalPath)) {
          throw new \RuntimeException("Cannot write the credentials for {$profile}");
      }
  }
  ```

  ```ruby Ruby
  require "fileutils"
  require "json"
  require "tempfile"

  # Jalankan ini di sandbox, sebagai pengguna agen.
  def write_credentials_file(config_dir, profile, token, expires_at)
    credentials_dir = File.join(config_dir, "credentials")
    FileUtils.mkdir_p(credentials_dir, mode: 0o700)
    body = { type: "oauth_token", access_token: token, expires_at: }
    temporary_file = Tempfile.create(".tmp", credentials_dir) # mode 0600
    temporary_file.write(body.to_json)
    temporary_file.close
    File.rename(temporary_file.path, File.join(credentials_dir, "#{profile}.json"))
  end
  ```
</CodeGroup>

Dalam beberapa menit setelah penyegaran, permintaan dengan token sebelumnya mendapatkan `401`. Klien kemudian dapat membaca file lagi dan mengirim permintaan dengan token baru. Dengan SDK TypeScript atau C# saja, satu permintaan tersebut justru gagal. Kirim sekali lagi: permintaan berikutnya menggunakan token baru. SDK juga membaca file lagi dalam 2 menit terakhir sebelum `expires_at`, atau dalam 30 detik terakhir di Java.

### Untuk agen

* Saat Anda menyegarkan, jangan kirim parameter `scope`.
* Untuk setiap penyegaran, baca client assertion lagi dari file-nya.
* Saat Anda menyimpan token baru, hitung waktu kedaluwarsanya dari saat Anda mengirim penyegaran, menggunakan `expires_in` dan `refresh_token_expires_in`.
* Saat penangguhan berakhir, hapus `on_hold` (typescript, java, php: `onHold`; csharp, go: `OnHold`) hanya jika `hold_reason` (typescript, java, php: `holdReason`; csharp, go: `HoldReason`)-nya adalah `invalid_grant`.
* Saat Anda menulis file kredensial sandbox, tulis token yang memiliki sisa waktu lebih dari 30 detik sebelum `expires_at`-nya.

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Uji dan publikasikan aplikasi Anda" icon="rocket" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish">
    Tambahkan pengguna uji, publikasikan aplikasi Anda, dan ubah atau hapus aplikasi tersebut
  </Card>

  <Card title="Apa yang dilihat pelanggan Anda" icon="browser" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see">
    Halaman persetujuan, batas atas pengeluaran, dan email yang dilihat pelanggan Anda, sehingga Anda dapat mendukung mereka
  </Card>
</CardGroup>
