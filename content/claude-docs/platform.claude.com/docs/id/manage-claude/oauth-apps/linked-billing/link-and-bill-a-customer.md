---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer
fetched_at: 2026-11-25T02:14:09.890537Z
sha256: 06bc60c9b14fd619c44d37393263e31dd3c34102dbde4ac8a119f8b00095afe2
---

---
title: Tautkan dan tagih pelanggan
url: https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer
description: Arahkan pelanggan untuk menyetujui aplikasi OAuth Anda, simpan koneksinya, dan tagihkan permintaan Claude API ke organisasi Claude mereka.
featureMetadata:
  status: beta
  betaHeader: user-profiles-billing-2026-10-01
  supportedModels:
    - claude-fable-5-2
    - claude-mythos-5-2
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
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API:
      availability: beta
      note: Hanya permintaan yang mengirim `billing_policy` yang memerlukan header beta.
---

<Warning>
  Claude Platform OAuth adalah Beta Service: perangkat lunak prarilis yang disediakan berdasarkan perjanjian Anda dengan Anthropic, seperti [Ketentuan Layanan Komersial](https://www.anthropic.com/legal/commercial-terms), dan [Ketentuan Khusus Layanan](https://www.anthropic.com/legal/service-specific-terms). Endpoint, parameter, dan perilaku dapat berubah selama beta. Ini mungkin tidak cocok untuk penggunaan produksi.
</Warning>

Halaman ini menunjukkan cara membangun Linked billing ke dalam produk Anda. Pelanggan menyetujui aplikasi Anda sekali, yang membuat koneksi antara organisasi Claude mereka dan salah satu profil pengguna Anda. Setelah itu, back end Anda menagih pelanggan dengan mengirim permintaan sebagai [akun layanan operator](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#service-account) Anda sendiri, dengan menyebutkan [profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) pelanggan. Anda mencoba alur ini terlebih dahulu pada pelanggan uji, yaitu organisasi kedua milik Anda sendiri. Untuk cara kerja fitur ini dan apakah fitur ini cocok untuk produk Anda, lihat [Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing).

## Sebelum Anda memulai

Anda memerlukan hal-hal berikut:

* **Aplikasi yang disiapkan untuk Linked billing:** Aplikasi ini memerlukan autentikasi klien, akun layanan operator, dan workspace default: lihat [Siapkan aplikasi Anda untuk Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app).
* **Pelanggan uji:** Organisasi Claude kedua milik Anda, karena organisasi yang memiliki aplikasi Anda tidak dapat ditautkan ke aplikasi tersebut. Organisasi ini harus membayar Anthropic secara langsung, melalui penagihan berbasis faktur atau [kredit yang dapat membayar permintaan ini](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#which-credits-can-pay).
* **Pengguna uji:** Seseorang dengan peran Admin atau Billing di organisasi pelanggan uji, yang memberikan persetujuan untuk organisasi tersebut. Sampai aplikasi Anda aktif, hanya orang-orang dalam daftar **Test users** aplikasi yang dapat menautkannya. [Tambahkan alamat email Claude orang ini](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#add-test-users) ke daftar tersebut.

### Penyiapan contoh

Contoh-contoh membaca nilai-nilai berikut:

| Contoh | Yang dibutuhkan | Sumbernya |
| ----- | ----- | ----- |
| SDK dan CLI | Pengaturan federasi akun layanan operator Anda, dalam variabel lingkungan, termasuk file JWT federasi di `ANTHROPIC_IDENTITY_TOKEN_FILE` | [Membuat klien SDK](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#construct-the-sdk-client) |
| Permintaan cURL ke Claude API | Token akses akun layanan Anda, di `ANTHROPIC_AUTH_TOKEN` | [Autentikasi dari workload Anda](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#authenticate-from-your-workload) |
| Permintaan ke `auth.claude.com` | Client assertion: JWT untuk **Expected audience** aplikasi Anda, dalam file yang disebutkan oleh `CLIENT_ASSERTION_FILE` atau sebagai pengganti `YOUR_CLIENT_ASSERTION_JWT` | Penyedia identitas Anda |
| Semua | Client ID dan redirect URI aplikasi Anda, sebagai pengganti client ID dan redirect URI contoh | Halaman aplikasi Anda di Claude Console |

Atur `ANTHROPIC_AUTH_TOKEN` hanya di tempat contoh cURL dijalankan. Di tempat contoh SDK dan CLI dijalankan, hapus pengaturan variabel tersebut dan `ANTHROPIC_API_KEY`, karena [masing-masing lebih diprioritaskan daripada federasi](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation#credential-precedence).

Client assertion dan JWT federasi biasanya memerlukan audiens yang berbeda, jadi simpan keduanya di file terpisah: lihat [ketika kedua audiens berbeda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#if-the-audiences-differ). Contoh yang menggunakan `CLIENT_ASSERTION_FILE` membacanya untuk setiap permintaan, karena JWT di dalamnya dirotasi.

## Memilih profil pengguna

[Profil pengguna](https://platform.claude.com/docs/id/manage-claude/user-profiles) adalah catatan di organisasi Anda sendiri yang mewakili salah satu pelanggan Anda. Permintaan yang menagih pelanggan membawa ID profil, yang memberi tahu Anthropic siapa yang harus ditagih. Anda dapat menautkan profil yang sudah Anda miliki, kecuali jika profil tersebut diarsipkan, dan penautan tidak mengubah ID atau riwayat penggunaannya.

Dalam satu aplikasi, organisasi Claude pelanggan hanya dapat ditautkan ke satu profil Anda, dan satu profil hanya dapat ditautkan ke satu organisasi. Tentukan profil mana yang mewakili organisasi mana sebelum Anda menautkan pelanggan pertama Anda. Organisasi tersebut adalah organisasi yang dipilih pelanggan Anda saat memberikan persetujuan, jadi tanyakan kepada mereka bagaimana tim mereka menggunakan organisasi Claude:

* **Beberapa tim berbagi satu organisasi Claude:** Gunakan satu profil untuk semua tim.
* **Setiap tim memiliki organisasi Claude sendiri:** Gunakan satu profil untuk setiap organisasi.

Jika pelanggan memilih organisasi yang sudah ditautkan ke profil Anda yang lain, persetujuan akan ditolak: lihat [`user_profile_already_linked` di Error Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#user-profile-already-linked).

Dua kasus mengubah profil yang Anda buat: [Jika Anda memiliki profil untuk setiap orang](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#if-you-have-a-profile-for-each-person) dan [Jika Anda menjual kembali akses API](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#if-you-resell-api-access).

## Menautkan pelanggan

<Frame>
  ![Diagram urutan: pelanggan memberikan persetujuan di auth.claude.com, lalu back end Anda mendapatkan koneksi dan token OAuth](https://platform.claude.com/docs/id/images/linked-billing-link-flow.svg)
</Frame>

### Membuat profil pengguna

Buat satu profil pengguna untuk setiap organisasi Claude yang akan ditautkan, sesuai pemetaan Anda di [Memilih profil pengguna](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#choose-the-user-profile). Lewati langkah ini untuk profil yang sudah Anda miliki. Kirim nama dan ID Anda sendiri untuk pelanggan (`reference_id`). Buat profil sekali, dan simpan ID-nya bersama catatan pelanggan: setiap permintaan pembuatan membuat profil baru, bahkan dengan `reference_id` yang sama.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/user_profiles \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "content-type: application/json" \
    -d '{
      "name": "Example Customer Inc.",
      "external_user_details": {"reference_id": "cust_2abc3def"}
    }'
  ```

  ```bash CLI
  ant user-profiles create \
    --name "Example Customer Inc." \
    --external-user-details.reference-id cust_2abc3def
  ```

  ```python Python
  client = anthropic.Anthropic()

  profile = client.user_profiles.create(
      name="Example Customer Inc.",
      external_user_details={"reference_id": "cust_2abc3def"},
  )

  print(profile.id)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const profile = await client.userProfiles.create({
    name: "Example Customer Inc.",
    external_user_details: { reference_id: "cust_2abc3def" }
  });

  console.log(profile.id);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var profile = await client.UserProfiles.Create(
      new()
      {
          Name = "Example Customer Inc.",
          ExternalUserDetails = new() { ReferenceID = "cust_2abc3def" },
      }
  );

  Console.WriteLine(profile.ID);
  ```

  ```go Go
  client := anthropic.NewClient()

  profile, err := client.UserProfiles.New(context.Background(), anthropic.UserProfileNewParams{
  	Name: anthropic.String("Example Customer Inc."),
  	ExternalUserDetails: anthropic.UserProfileExternalUserDetailsParams{
  		ReferenceID: anthropic.String("cust_2abc3def"),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(profile.ID)
  ```

  ```java Java
  import com.anthropic.models.userprofiles.UserProfileCreateParams;
  import com.anthropic.models.userprofiles.UserProfileExternalUserDetailsParams;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = UserProfileCreateParams.builder()
          .name("Example Customer Inc.")
          .externalUserDetails(UserProfileExternalUserDetailsParams.builder()
              .referenceId("cust_2abc3def")
              .build())
          .build();
      var profile = client.userProfiles().create(params);

      IO.println(profile.id());
  }
  ```

  ```php PHP
  $client = new Client();

  $profile = $client->userProfiles->create(
      name: 'Example Customer Inc.',
      externalUserDetails: ['referenceID' => 'cust_2abc3def'],
  );

  echo $profile->id, PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  profile = client.user_profiles.create(
    name: "Example Customer Inc.",
    external_user_details: { reference_id: "cust_2abc3def" }
  )

  puts(profile.id)
  ```
</CodeGroup>

Respons berisi `id` profil, seperti `uprof_01HV9Z`.

### Mengarahkan pelanggan untuk memberikan persetujuan

Tambahkan [tombol Link your Claude organization](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-button) ke produk Anda, di tempat pelanggan Anda mengelola penagihan atau integrasi. HTML, warna, dan logonya siap disalin.

Halaman persetujuan hanya menawarkan organisasi dari akun Claude yang sedang masuk, dan organisasi yang dipilih pelanggan yang membayar. Untuk apa yang perlu ditampilkan di samping tombol, lihat [Apa yang perlu disampaikan kepada pelanggan Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#what-to-tell-your-customers).

Saat pelanggan mengklik tombol, lakukan tiga hal ini di back end Anda:

1. **Buat nilai `state` dan PKCE code verifier,** yaitu rahasia acak yang membuktikan bahwa back end Anda yang memulai persetujuan ini. Simpan keduanya di back end Anda, terkait dengan sesi browser dan catatan pelanggan.
2. **Kirim “pushed authorization request” (permintaan otorisasi yang didorong)** ke `auth.claude.com`, yang meneruskan detail persetujuan dari back end Anda alih-alih melalui browser.
3. **Alihkan browser** ke `https://auth.claude.com/oauth/authorize` dengan `client_id` Anda dan `request_uri` dari respons. Sebuah `request_uri` hanya berfungsi sekali dan kedaluwarsa setelah 10 menit, jadi kirim pushed authorization request baru untuk setiap klik.

Tidak ada SDK yang mencakup `auth.claude.com`, jadi contoh untuk langkah-langkah ini memanggilnya melalui HTTP:

<CodeGroup exclude="shell:CLI">
  ```bash cURL
  curl https://auth.claude.com/v1/oauth/par \
    -H "content-type: application/json" \
    -d @- <<'JSON'
  {
    "response_type": "code",
    "client_id": "clid_01ABcDeFgHiJkLmNoPqRsTuV",
    "redirect_uri": "https://app.example.com/claude/billing/callback",
    "scope": "billing:attribution",
    "connection_type": "organization_shared",
    "connection_auth_target": "platform",
    "user_profile_id": "uprof_01HV9Z",
    "state": "RANDOM_STATE",
    "code_challenge": "BASE64URL_SHA256_OF_VERIFIER",
    "code_challenge_method": "S256",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": "YOUR_CLIENT_ASSERTION_JWT"
  }
  JSON
  ```

  <CodeGroupItem language="CLI">
    CLI `ant` tidak memiliki perintah untuk `auth.claude.com`. Kirim permintaan dengan cURL atau dalam bahasa aplikasi Anda.
  </CodeGroupItem>

  ```python Python
  import base64
  import hashlib
  import os
  import secrets
  from pathlib import Path
  from urllib.parse import urlencode

  import httpx2  # comes with the Anthropic SDK

  CLIENT_ID = "clid_01ABcDeFgHiJkLmNoPqRsTuV"


  def push_authorization_request(user_profile_id: str) -> dict[str, str]:
      state = secrets.token_urlsafe(32)
      code_verifier = secrets.token_urlsafe(64)
      digest = hashlib.sha256(code_verifier.encode()).digest()
      assertion_file = Path(os.environ["CLIENT_ASSERTION_FILE"])

      response = httpx2.post(
          "https://auth.claude.com/v1/oauth/par",
          json={
              "response_type": "code",
              "client_id": CLIENT_ID,
              "redirect_uri": "https://app.example.com/claude/billing/callback",
              "scope": "billing:attribution",
              "connection_type": "organization_shared",
              "connection_auth_target": "platform",
              "user_profile_id": user_profile_id,
              "state": state,
              "code_challenge": base64.urlsafe_b64encode(digest).rstrip(b"=").decode(),
              "code_challenge_method": "S256",
              "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              "client_assertion": assertion_file.read_text().strip(),
          },
          timeout=10,
      )
      if not response.is_success:
          raise RuntimeError(f"Request failed: {response.status_code} {response.text}")

      query = {"client_id": CLIENT_ID, "request_uri": response.json()["request_uri"]}
      return {
          "approval_url": f"https://auth.claude.com/oauth/authorize?{urlencode(query)}",
          "state": state,
          "code_verifier": code_verifier,
      }
  ```

  ```typescript TypeScript
  import { createHash, randomBytes } from "node:crypto";
  import { readFile } from "node:fs/promises";

  const CLIENT_ID = "clid_01ABcDeFgHiJkLmNoPqRsTuV";

  async function pushAuthorizationRequest(userProfileId: string) {
    const state = randomBytes(32).toString("base64url");
    const codeVerifier = randomBytes(64).toString("base64url");
    const jwt = await readFile(process.env.CLIENT_ASSERTION_FILE!, "utf8");

    const response = await fetch("https://auth.claude.com/v1/oauth/par", {
      method: "POST",
      redirect: "error",
      signal: AbortSignal.timeout(10_000),
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        response_type: "code",
        client_id: CLIENT_ID,
        redirect_uri: "https://app.example.com/claude/billing/callback",
        scope: "billing:attribution",
        connection_type: "organization_shared",
        connection_auth_target: "platform",
        user_profile_id: userProfileId,
        state,
        code_challenge: createHash("sha256").update(codeVerifier).digest("base64url"),
        code_challenge_method: "S256",
        client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        client_assertion: jwt.trim()
      })
    });
    if (!response.ok) {
      throw new Error(`Request failed: ${response.status} ${await response.text()}`);
    }

    const { request_uri } = (await response.json()) as { request_uri: string };
    const query = new URLSearchParams({ client_id: CLIENT_ID, request_uri });
    return {
      approvalUrl: `https://auth.claude.com/oauth/authorize?${query}`,
      state,
      codeVerifier
    };
  }
  ```

  ```csharp C#
  using System.Buffers.Text;
  using System.Net.Http.Json;
  using System.Security.Cryptography;
  using System.Text;
  using System.Text.Json;

  const string ClientId = "clid_01ABcDeFgHiJkLmNoPqRsTuV";
  using var http = new HttpClient { Timeout = TimeSpan.FromSeconds(10) };

  async Task<(string ApprovalUrl, string State, string CodeVerifier)> PushAuthorizationRequest(
      string userProfileId
  )
  {
      var state = Base64Url.EncodeToString(RandomNumberGenerator.GetBytes(32));
      var codeVerifier = Base64Url.EncodeToString(RandomNumberGenerator.GetBytes(64));
      var digest = SHA256.HashData(Encoding.ASCII.GetBytes(codeVerifier));
      var assertionFile = Environment.GetEnvironmentVariable("CLIENT_ASSERTION_FILE")!;
      var jwt = await File.ReadAllTextAsync(assertionFile);

      using var response = await http.PostAsJsonAsync(
          "https://auth.claude.com/v1/oauth/par",
          new Dictionary<string, string>
          {
              ["response_type"] = "code",
              ["client_id"] = ClientId,
              ["redirect_uri"] = "https://app.example.com/claude/billing/callback",
              ["scope"] = "billing:attribution",
              ["connection_type"] = "organization_shared",
              ["connection_auth_target"] = "platform",
              ["user_profile_id"] = userProfileId,
              ["state"] = state,
              ["code_challenge"] = Base64Url.EncodeToString(digest),
              ["code_challenge_method"] = "S256",
              ["client_assertion_type"] = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              ["client_assertion"] = jwt.Trim(),
          }
      );
      if (!response.IsSuccessStatusCode)
      {
          var details = await response.Content.ReadAsStringAsync();
          throw new HttpRequestException($"Request failed: {(int)response.StatusCode} {details}");
      }

      var result = await response.Content.ReadFromJsonAsync<JsonElement>();
      var requestUri = Uri.EscapeDataString(result.GetProperty("request_uri").GetString()!);
      var query = $"client_id={ClientId}&request_uri={requestUri}";
      return ($"https://auth.claude.com/oauth/authorize?{query}", state, codeVerifier);
  }
  ```

  ```go Go
  import (
  	"bytes"
  	"crypto/rand"
  	"crypto/sha256"
  	"encoding/base64"
  	"encoding/json"
  	"fmt"
  	"io"
  	"net/http"
  	"net/url"
  	"os"
  	"strings"
  	"time"
  )

  const clientID = "clid_01ABcDeFgHiJkLmNoPqRsTuV"

  var httpClient = &http.Client{Timeout: 10 * time.Second}

  type approval struct{ URL, State, CodeVerifier string }

  func pushAuthorizationRequest(userProfileID string) (*approval, error) {
  	state := rand.Text()
  	codeVerifier := rand.Text() + rand.Text() // PKCE needs at least 43 characters
  	digest := sha256.Sum256([]byte(codeVerifier))
  	jwt, err := os.ReadFile(os.Getenv("CLIENT_ASSERTION_FILE"))
  	if err != nil {
  		return nil, err
  	}

  	body, err := json.Marshal(map[string]string{
  		"response_type":          "code",
  		"client_id":              clientID,
  		"redirect_uri":           "https://app.example.com/claude/billing/callback",
  		"scope":                  "billing:attribution",
  		"connection_type":        "organization_shared",
  		"connection_auth_target": "platform",
  		"user_profile_id":        userProfileID,
  		"state":                  state,
  		"code_challenge":         base64.RawURLEncoding.EncodeToString(digest[:]),
  		"code_challenge_method":  "S256",
  		"client_assertion_type":  "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
  		"client_assertion":       strings.TrimSpace(string(jwt)),
  	})
  	if err != nil {
  		return nil, err
  	}

  	endpoint := "https://auth.claude.com/v1/oauth/par"
  	response, err := httpClient.Post(endpoint, "application/json", bytes.NewReader(body))
  	if err != nil {
  		return nil, err
  	}
  	defer response.Body.Close()
  	if response.StatusCode/100 != 2 {
  		details, _ := io.ReadAll(response.Body)
  		return nil, fmt.Errorf("request failed: %d %s", response.StatusCode, details)
  	}

  	var result struct {
  		RequestURI string `json:"request_uri"`
  	}
  	if err := json.NewDecoder(response.Body).Decode(&result); err != nil {
  		return nil, err
  	}
  	query := url.Values{"client_id": {clientID}, "request_uri": {result.RequestURI}}
  	approvalURL := "https://auth.claude.com/oauth/authorize?" + query.Encode()
  	return &approval{approvalURL, state, codeVerifier}, nil
  }
  ```

  ```java Java
  import module java.base;
  import module java.net.http;
  import com.fasterxml.jackson.databind.ObjectMapper; // Jackson comes with the Anthropic SDK

  static final String CLIENT_ID = "clid_01ABcDeFgHiJkLmNoPqRsTuV";
  static final Base64.Encoder BASE64_URL = Base64.getUrlEncoder().withoutPadding();
  final HttpClient http = HttpClient.newHttpClient();
  final ObjectMapper mapper = new ObjectMapper();

  record Approval(String url, String state, String codeVerifier) {}

  String randomValue(int size) {
      var bytes = new byte[size];
      new SecureRandom().nextBytes(bytes);
      return BASE64_URL.encodeToString(bytes);
  }

  Approval pushAuthorizationRequest(String userProfileId) throws Exception {
      var state = randomValue(32);
      var codeVerifier = randomValue(64);
      var digest = MessageDigest.getInstance("SHA-256")
          .digest(codeVerifier.getBytes(StandardCharsets.US_ASCII));
      var jwt = Files.readString(Path.of(System.getenv("CLIENT_ASSERTION_FILE")));

      var body = mapper.createObjectNode()
          .put("response_type", "code")
          .put("client_id", CLIENT_ID)
          .put("redirect_uri", "https://app.example.com/claude/billing/callback")
          .put("scope", "billing:attribution")
          .put("connection_type", "organization_shared")
          .put("connection_auth_target", "platform")
          .put("user_profile_id", userProfileId)
          .put("state", state)
          .put("code_challenge", BASE64_URL.encodeToString(digest))
          .put("code_challenge_method", "S256")
          .put("client_assertion_type", "urn:ietf:params:oauth:client-assertion-type:jwt-bearer")
          .put("client_assertion", jwt.strip());

      var request = HttpRequest.newBuilder(URI.create("https://auth.claude.com/v1/oauth/par"))
          .header("content-type", "application/json")
          .timeout(Duration.ofSeconds(10))
          .POST(HttpRequest.BodyPublishers.ofString(body.toString()))
          .build();
      var response = http.send(request, HttpResponse.BodyHandlers.ofString());
      if (response.statusCode() / 100 != 2) {
          throw new IOException("Request failed: " + response.statusCode() + " " + response.body());
      }

      var requestUri = mapper.readTree(response.body()).get("request_uri").asText();
      var query = "client_id=%s&request_uri=%s"
          .formatted(CLIENT_ID, URLEncoder.encode(requestUri, StandardCharsets.UTF_8));
      return new Approval("https://auth.claude.com/oauth/authorize?" + query, state, codeVerifier);
  }
  ```

  ```php PHP
  const CLIENT_ID = 'clid_01ABcDeFgHiJkLmNoPqRsTuV';

  function base64Url(string $bytes): string
  {
      return rtrim(strtr(base64_encode($bytes), '+/', '-_'), '=');
  }

  /** @return array{approvalUrl: string, state: string, codeVerifier: string} */
  function pushAuthorizationRequest(string $userProfileId): array
  {
      $state = base64Url(random_bytes(32));
      $codeVerifier = base64Url(random_bytes(64));
      $jwt = file_get_contents((string) getenv('CLIENT_ASSERTION_FILE'))
          ?: throw new \RuntimeException('Cannot read the client assertion file');

      $body = json_encode([
          'response_type' => 'code',
          'client_id' => CLIENT_ID,
          'redirect_uri' => 'https://app.example.com/claude/billing/callback',
          'scope' => 'billing:attribution',
          'connection_type' => 'organization_shared',
          'connection_auth_target' => 'platform',
          'user_profile_id' => $userProfileId,
          'state' => $state,
          'code_challenge' => base64Url(hash('sha256', $codeVerifier, binary: true)),
          'code_challenge_method' => 'S256',
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
      $response = file_get_contents('https://auth.claude.com/v1/oauth/par', context: $context);
      $status = http_get_last_response_headers()[0] ?? '';
      if ($response === false || !preg_match('{^HTTP/\S+ 2}', $status)) {
          throw new \RuntimeException("Request failed: {$status} {$response}");
      }

      /** @var array{request_uri: string} $result */
      $result = json_decode($response, associative: true, flags: JSON_THROW_ON_ERROR);
      $query = http_build_query(['client_id' => CLIENT_ID, 'request_uri' => $result['request_uri']]);

      return [
          'approvalUrl' => "https://auth.claude.com/oauth/authorize?{$query}",
          'state' => $state,
          'codeVerifier' => $codeVerifier,
      ];
  }
  ```

  ```ruby Ruby
  require "base64"
  require "digest"
  require "json"
  require "net/http"
  require "securerandom"

  CLIENT_ID = "clid_01ABcDeFgHiJkLmNoPqRsTuV"

  def push_authorization_request(user_profile_id)
    state = SecureRandom.urlsafe_base64(32)
    code_verifier = SecureRandom.urlsafe_base64(64)
    digest = Digest::SHA256.digest(code_verifier)
    jwt = File.read(ENV.fetch("CLIENT_ASSERTION_FILE"))

    body = {
      response_type: "code",
      client_id: CLIENT_ID,
      redirect_uri: "https://app.example.com/claude/billing/callback",
      scope: "billing:attribution",
      connection_type: "organization_shared",
      connection_auth_target: "platform",
      user_profile_id:,
      state:,
      code_challenge: Base64.urlsafe_encode64(digest, padding: false),
      code_challenge_method: "S256",
      client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      client_assertion: jwt.strip
    }
    response = Net::HTTP.start("auth.claude.com", 443, use_ssl: true, read_timeout: 10) do |http|
      http.post("/v1/oauth/par", body.to_json, "content-type" => "application/json")
    end
    unless response.is_a?(Net::HTTPSuccess)
      raise "Request failed: #{response.code} #{response.body}"
    end

    request_uri = JSON.parse(response.body).fetch("request_uri")
    query = URI.encode_www_form(client_id: CLIENT_ID, request_uri:)
    { approval_url: "https://auth.claude.com/oauth/authorize?#{query}", state:, code_verifier: }
  end
  ```
</CodeGroup>

Pushed authorization request membawa client ID dan client assertion Anda, ID profil pengguna pelanggan, dan scope. Permintaan ini juga membawa redirect URI terdaftar Anda, `state`, dan code challenge yang dibuat dari verifier. `connection_type` dan `connection_auth_target` menandainya sebagai permintaan Linked billing. Untuk setiap field dan nilainya, lihat [Endpoint dan parameter OAuth](https://platform.claude.com/docs/id/manage-claude/oauth-apps/endpoints-and-parameters#authorization-requests).

Scope-nya adalah `billing:attribution`. Untuk juga mendapatkan refresh token, minta `billing:attribution offline_access`, yang memerlukan **Offline access** diaktifkan untuk aplikasi Anda. Apakah Anda memerlukannya bergantung pada [cara back end Anda menagih](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/set-up-your-app#choose-whether-to-get-refresh-tokens). Menambahkan `offline_access` untuk pelanggan yang sudah ditautkan akan membuat koneksi baru yang menggantikan koneksi sebelumnya: lihat [Jika pelanggan memberikan persetujuan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#if-a-customer-approves-again).

Di halaman persetujuan, pelanggan masuk ke Claude jika diperlukan, memilih organisasi yang akan ditautkan, dan memberikan persetujuan. Sampai aplikasi Anda aktif, orang yang memberikan persetujuan juga harus menetapkan batas atas pengeluaran untuk aplikasi Anda: lihat [Batas atas selama pengujian](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#caps-while-testing).

### Menyimpan koneksi dan token OAuth-nya

Setelah pelanggan memberikan persetujuan, `auth.claude.com` mengarahkan browser ke redirect URI Anda. Kemudian, lakukan hal-hal ini di back end Anda:

1. **Periksa callback.** Periksa bahwa `state`-nya cocok dengan yang Anda simpan, yang menunjukkan bahwa browser yang sama kembali. Periksa bahwa `iss`-nya adalah `https://identity.anthropic.com/users`, yang menunjukkan bahwa callback berasal dari Claude. Jika salah satunya tidak ada atau tidak cocok, hentikan.
2. **Periksa adanya error.** Jika callback membawa parameter `error` alih-alih kode, tidak ada koneksi yang dibuat. Untuk penyebabnya, lihat [Error Linked billing](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#while-linking).
3. **Tukarkan kode segera.** Kirim kode bersama PKCE code verifier, redirect URI dari pushed authorization request Anda, dan client assertion. Kode kedaluwarsa setelah 5 menit.
4. **Simpan apa yang dikembalikan respons.** Penukaran mengembalikan token OAuth hanya sekali.

Contoh-contoh ini mengirim penukaran kode ke `auth.claude.com` melalui HTTP:

<CodeGroup exclude="shell:CLI">
  ```bash cURL
  curl https://auth.claude.com/v1/oauth/token \
    -H "content-type: application/json" \
    -d @- <<'JSON'
  {
    "grant_type": "authorization_code",
    "code": "AUTH_CODE",
    "code_verifier": "ORIGINAL_CODE_VERIFIER",
    "redirect_uri": "https://app.example.com/claude/billing/callback",
    "client_id": "clid_01ABcDeFgHiJkLmNoPqRsTuV",
    "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
    "client_assertion": "YOUR_CLIENT_ASSERTION_JWT"
  }
  JSON
  ```

  <CodeGroupItem language="CLI">
    CLI `ant` tidak memiliki perintah untuk `auth.claude.com`. Kirim permintaan dengan cURL atau dalam bahasa aplikasi Anda.
  </CodeGroupItem>

  ```python Python
  import os
  import secrets
  from pathlib import Path

  import httpx2  # comes with the Anthropic SDK


  def handle_callback(params: dict[str, str], state: str, code_verifier: str) -> dict:
      if not secrets.compare_digest(params.get("state", "").encode(), state.encode()):
          raise ValueError("state does not match")
      if params.get("iss") != "https://identity.anthropic.com/users":
          raise ValueError("iss does not match")
      if "error" in params:
          raise PermissionError(params["error"])

      assertion_file = Path(os.environ["CLIENT_ASSERTION_FILE"])

      response = httpx2.post(
          "https://auth.claude.com/v1/oauth/token",
          json={
              "grant_type": "authorization_code",
              "code": params["code"],
              "code_verifier": code_verifier,
              "redirect_uri": "https://app.example.com/claude/billing/callback",
              "client_id": "clid_01ABcDeFgHiJkLmNoPqRsTuV",
              "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              "client_assertion": assertion_file.read_text().strip(),
          },
          timeout=10,
      )
      if not response.is_success:
          raise RuntimeError(f"Exchange failed: {response.status_code} {response.text}")
      return response.json()  # connection_id and the tokens
  ```

  ```typescript TypeScript
  import { timingSafeEqual } from "node:crypto";
  import { readFile } from "node:fs/promises";

  async function handleCallback(params: URLSearchParams, state: string, codeVerifier: string) {
    const received = new TextEncoder().encode(params.get("state") ?? "");
    const expected = new TextEncoder().encode(state);
    if (received.length !== expected.length || !timingSafeEqual(received, expected)) {
      throw new Error("state does not match");
    }
    if (params.get("iss") !== "https://identity.anthropic.com/users") {
      throw new Error("iss does not match");
    }
    if (params.has("error")) {
      throw new Error(`Linking failed: ${params.get("error")}`);
    }

    const jwt = await readFile(process.env.CLIENT_ASSERTION_FILE!, "utf8");

    const response = await fetch("https://auth.claude.com/v1/oauth/token", {
      method: "POST",
      redirect: "error",
      signal: AbortSignal.timeout(10_000),
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        grant_type: "authorization_code",
        code: params.get("code"),
        code_verifier: codeVerifier,
        redirect_uri: "https://app.example.com/claude/billing/callback",
        client_id: "clid_01ABcDeFgHiJkLmNoPqRsTuV",
        client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        client_assertion: jwt.trim()
      })
    });
    if (!response.ok) {
      throw new Error(`Exchange failed: ${response.status} ${await response.text()}`);
    }
    return response.json(); // connection_id and the tokens
  }
  ```

  ```csharp C#
  using System.Net.Http.Json;
  using System.Security.Cryptography;
  using System.Text;
  using System.Text.Json;

  using var http = new HttpClient { Timeout = TimeSpan.FromSeconds(10) };

  async Task<JsonElement> HandleCallback(
      Dictionary<string, string> parameters,
      string state,
      string codeVerifier
  )
  {
      var received = Encoding.UTF8.GetBytes(parameters.GetValueOrDefault("state", ""));
      if (!CryptographicOperations.FixedTimeEquals(received, Encoding.UTF8.GetBytes(state)))
      {
          throw new InvalidOperationException("state does not match");
      }
      if (parameters.GetValueOrDefault("iss") != "https://identity.anthropic.com/users")
      {
          throw new InvalidOperationException("iss does not match");
      }
      if (parameters.TryGetValue("error", out var error))
      {
          throw new InvalidOperationException($"Linking failed: {error}");
      }

      var assertionFile = Environment.GetEnvironmentVariable("CLIENT_ASSERTION_FILE")!;
      var jwt = await File.ReadAllTextAsync(assertionFile);

      using var response = await http.PostAsJsonAsync(
          "https://auth.claude.com/v1/oauth/token",
          new Dictionary<string, string>
          {
              ["grant_type"] = "authorization_code",
              ["code"] = parameters["code"],
              ["code_verifier"] = codeVerifier,
              ["redirect_uri"] = "https://app.example.com/claude/billing/callback",
              ["client_id"] = "clid_01ABcDeFgHiJkLmNoPqRsTuV",
              ["client_assertion_type"] = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
              ["client_assertion"] = jwt.Trim(),
          }
      );
      if (!response.IsSuccessStatusCode)
      {
          var details = await response.Content.ReadAsStringAsync();
          throw new HttpRequestException($"Exchange failed: {(int)response.StatusCode} {details}");
      }

      // connection_id dan token-tokennya
      return await response.Content.ReadFromJsonAsync<JsonElement>();
  }
  ```

  ```go Go
  import (
  	"bytes"
  	"crypto/subtle"
  	"encoding/json"
  	"errors"
  	"fmt"
  	"io"
  	"net/http"
  	"net/url"
  	"os"
  	"strings"
  	"time"
  )

  var httpClient = &http.Client{Timeout: 10 * time.Second}

  func handleCallback(params url.Values, state, codeVerifier string) (map[string]any, error) {
  	if subtle.ConstantTimeCompare([]byte(params.Get("state")), []byte(state)) != 1 {
  		return nil, errors.New("state does not match")
  	}
  	if params.Get("iss") != "https://identity.anthropic.com/users" {
  		return nil, errors.New("iss does not match")
  	}
  	if params.Has("error") {
  		return nil, fmt.Errorf("linking failed: %s", params.Get("error"))
  	}

  	jwt, err := os.ReadFile(os.Getenv("CLIENT_ASSERTION_FILE"))
  	if err != nil {
  		return nil, err
  	}

  	body, err := json.Marshal(map[string]string{
  		"grant_type":            "authorization_code",
  		"code":                  params.Get("code"),
  		"code_verifier":         codeVerifier,
  		"redirect_uri":          "https://app.example.com/claude/billing/callback",
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
  		return nil, fmt.Errorf("exchange failed: %d %s", response.StatusCode, details)
  	}

  	var connection map[string]any // connection_id and the tokens
  	err = json.NewDecoder(response.Body).Decode(&connection)
  	return connection, err
  }
  ```

  ```java Java
  import module java.base;
  import module java.net.http;
  import com.fasterxml.jackson.databind.JsonNode;
  import com.fasterxml.jackson.databind.ObjectMapper; // Jackson comes with the Anthropic SDK

  final HttpClient http = HttpClient.newHttpClient();
  final ObjectMapper mapper = new ObjectMapper();

  JsonNode handleCallback(Map<String, String> params, String state, String codeVerifier)
          throws Exception {
      var received = params.getOrDefault("state", "").getBytes(StandardCharsets.UTF_8);
      if (!MessageDigest.isEqual(received, state.getBytes(StandardCharsets.UTF_8))) {
          throw new IllegalStateException("state does not match");
      }
      if (!"https://identity.anthropic.com/users".equals(params.get("iss"))) {
          throw new IllegalStateException("iss does not match");
      }
      if (params.containsKey("error")) {
          throw new IllegalStateException("Linking failed: " + params.get("error"));
      }

      var jwt = Files.readString(Path.of(System.getenv("CLIENT_ASSERTION_FILE")));

      var body = mapper.createObjectNode()
          .put("grant_type", "authorization_code")
          .put("code", params.get("code"))
          .put("code_verifier", codeVerifier)
          .put("redirect_uri", "https://app.example.com/claude/billing/callback")
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
          throw new IOException("Exchange failed: " + response.statusCode() + " " + response.body());
      }
      return mapper.readTree(response.body()); // connection_id and the tokens
  }
  ```

  ```php PHP
  /** @param array<string, string> $params */
  function handleCallback(array $params, string $state, string $codeVerifier): mixed
  {
      if (!hash_equals($state, $params['state'] ?? '')) {
          throw new \RuntimeException('state does not match');
      }
      if (($params['iss'] ?? '') !== 'https://identity.anthropic.com/users') {
          throw new \RuntimeException('iss does not match');
      }
      if (isset($params['error'])) {
          throw new \RuntimeException("Linking failed: {$params['error']}");
      }

      $jwt = file_get_contents((string) getenv('CLIENT_ASSERTION_FILE'))
          ?: throw new \RuntimeException('Cannot read the client assertion file');

      $body = json_encode([
          'grant_type' => 'authorization_code',
          'code' => $params['code'],
          'code_verifier' => $codeVerifier,
          'redirect_uri' => 'https://app.example.com/claude/billing/callback',
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
          throw new \RuntimeException("Exchange failed: {$status} {$response}");
      }

      // connection_id dan token-tokennya
      return json_decode($response, associative: true, flags: JSON_THROW_ON_ERROR);
  }
  ```

  ```ruby Ruby
  require "json"
  require "net/http"
  require "openssl"

  def handle_callback(params, state, code_verifier)
    raise "state does not match" unless OpenSSL.secure_compare(params["state"].to_s, state)
    raise "iss does not match" unless params["iss"] == "https://identity.anthropic.com/users"
    raise "Linking failed: #{params["error"]}" if params.key?("error")

    jwt = File.read(ENV.fetch("CLIENT_ASSERTION_FILE"))

    body = {
      grant_type: "authorization_code",
      code: params.fetch("code"),
      code_verifier:,
      redirect_uri: "https://app.example.com/claude/billing/callback",
      client_id: "clid_01ABcDeFgHiJkLmNoPqRsTuV",
      client_assertion_type: "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
      client_assertion: jwt.strip
    }
    response = Net::HTTP.start("auth.claude.com", 443, use_ssl: true, read_timeout: 10) do |http|
      http.post("/v1/oauth/token", body.to_json, "content-type" => "application/json")
    end
    unless response.is_a?(Net::HTTPSuccess)
      raise "Exchange failed: #{response.code} #{response.body}"
    end

    JSON.parse(response.body) # connection_id and the tokens
  end
  ```
</CodeGroup>

Respons berisi nilai-nilai berikut:

| Nilai | Apa itu | Apa yang harus dilakukan dengannya |
| ----- | ----- | ----- |
| `connection_id` | ID koneksi | Simpan bersama catatan pelanggan, untuk mengakhiri koneksi dari back end Anda nanti |
| `access_token` | Token milik pelanggan sendiri, terpisah dari token akun layanan Anda: token ini hanya dapat menagih pelanggan ini, hingga 1 jam | Simpan sebagai rahasia |
| `refresh_token` | Token yang mendapatkan token akses baru, jika Anda meminta `offline_access` | Simpan sebagai rahasia |

Respons tidak menyebutkan organisasi mana yang ditautkan pelanggan.

Permintaan di halaman ini menagih sebagai akun layanan Anda, sehingga tidak memerlukan token OAuth. Tetap simpan token tersebut: Anda memerlukannya untuk [menggunakan kredensial terpisah untuk setiap pelanggan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/credential-for-each-customer). Jika Anda meminta refresh token, Anda tidak dapat mendapatkannya lagi kecuali Anda membatalkan tautan pelanggan dan mereka menautkan lagi.

Jika penukaran gagal, apa yang Anda lakukan bergantung pada cara kegagalannya:

* **Penukaran mengembalikan `unauthorized_client`:** Biasanya, aplikasi Anda tidak memiliki akun layanan operator atau workspace default, atau workspace-nya diarsipkan. Lihat [cara memperbaiki `unauthorized_client`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#code-exchange-unauthorized-client).
* **Penukaran mengembalikan `invalid_grant`:** Redirect URI atau verifier salah, atau kode sudah kedaluwarsa atau sudah digunakan. Redirect URI atau verifier yang salah akan menghabiskan kode, sehingga pelanggan harus memberikan persetujuan lagi. Untuk pelanggan yang sudah ditautkan, lihat [Jika pelanggan memberikan persetujuan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#if-a-customer-approves-again).
* **Penukaran mengalami timeout:** [Kirim kode yang sama sekali lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/link-and-bill-a-customer#if-the-code-exchange-times-out).

## Menagih permintaan

Kirim setiap permintaan untuk pelanggan ini sebagai akun layanan operator Anda, dan masukkan ID profil pengguna pelanggan di header `anthropic-user-profile-id`. SDK mengirim header tersebut untuk Anda dari parameter profil penggunanya. Header ini membuat permintaan dihitung dalam penggunaan profil tersebut, siapa pun yang membayar. Kemudian, pilih pada setiap permintaan apakah pelanggan atau Anda yang membayar.

### Pelanggan Anda membayar

Untuk menagihkan permintaan ke pelanggan, sebutkan profil yang memegang koneksi mereka di header tersebut, dan kirim juga:

* [`billing_policy`](https://platform.claude.com/docs/id/api/beta/messages/create) di body permintaan, diatur ke `{"type": "billing_policy", "bill_to": "user_profile"}`
* beta header `user-profiles-billing-2026-10-01`

<Warning>
  Jika permintaan menyebutkan profil pelanggan tertaut lainnya, Anthropic menagih organisasi pelanggan tersebut, dan tidak ada error yang memberi tahu Anda.
</Warning>

Periksa ID profil setiap permintaan. Pelanggan uji Anda membayar uang sungguhan untuk permintaan ini, sebagaimana pelanggan lainnya.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: user-profiles-billing-2026-10-01" \
    -H "anthropic-user-profile-id: uprof_01HV9Z" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}],
      "billing_policy": {"type": "billing_policy", "bill_to": "user_profile"}
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta user-profiles-billing-2026-10-01 \
    --user-profile-id uprof_01HV9Z \
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}' \
    --billing-policy '{type: billing_policy, bill_to: user_profile}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.beta.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      betas=["user-profiles-billing-2026-10-01"],
      user_profile_id="uprof_01HV9Z",
      billing_policy={"type": "billing_policy", "bill_to": "user_profile"},
  )

  for block in message.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.beta.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    betas: ["user-profiles-billing-2026-10-01"],
    user_profile_id: "uprof_01HV9Z",
    billing_policy: { type: "billing_policy", bill_to: "user_profile" }
  });

  for (const block of message.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Messages;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  var message = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [new BetaUserMessageParam { Content = "Hello, Claude" }],
          Betas = ["user-profiles-billing-2026-10-01"],
          UserProfileID = "uprof_01HV9Z",
          BillingPolicy = new() { BillTo = BetaBillTo.UserProfile },
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
  client := anthropic.NewClient()

  message, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Betas:         []anthropic.AnthropicBeta{"user-profiles-billing-2026-10-01"},
  	UserProfileID: anthropic.String("uprof_01HV9Z"),
  	BillingPolicy: anthropic.BetaBillingPolicyParam{BillTo: anthropic.BetaBillToUserProfile},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range message.Content {
  	if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaBillTo;
  import com.anthropic.models.beta.messages.BetaBillingPolicy;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .addBeta("user-profiles-billing-2026-10-01")
          .userProfileId("uprof_01HV9Z")
          .billingPolicy(BetaBillingPolicy.builder()
              .billTo(BetaBillTo.USER_PROFILE)
              .build())
          .build();
      var message = client.beta().messages().create(params);

      for (var block : message.content()) {
          block.text().ifPresent(textBlock -> IO.println(textBlock.text()));
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Messages\BetaBillingPolicy;
  use Anthropic\Beta\Messages\BetaBillTo;
  use Anthropic\Beta\Messages\BetaTextBlock;
  use Anthropic\Messages\Model;

  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: Model::CLAUDE_OPUS_5_5,
      betas: ['user-profiles-billing-2026-10-01'],
      userProfileID: 'uprof_01HV9Z',
      billingPolicy: BetaBillingPolicy::with(billTo: BetaBillTo::USER_PROFILE),
  );

  foreach ($message->content as $block) {
      if ($block instanceof BetaTextBlock) {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    betas: ["user-profiles-billing-2026-10-01"],
    user_profile_id: "uprof_01HV9Z",
    billing_policy: { type: :billing_policy, bill_to: :user_profile }
  )

  message.content.each do |block|
    puts(block.text) if block.is_a?(Anthropic::Beta::BetaTextBlock)
  end
  ```
</CodeGroup>

Claude API menagih pelanggan atau menolak permintaan. Claude API tidak pernah menagih Anda sebagai gantinya. Pada `/v1/messages`, permintaan yang ditolak membawa kodenya di `error.details.error_code`. Penolakan dapat memiliki penyebab berikut:

* **Koneksi baru:** Koneksi baru dapat memerlukan sekitar 10 detik untuk berfungsi setelah penukaran kode. Jika permintaan pertama Anda ditolak dengan `user_profile_billing_not_authorized` dalam 10 detik tersebut, kirim lagi setelah waktu itu berlalu. Jika masih ditolak, lihat [cara memperbaiki `user_profile_billing_not_authorized`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#user-profile-billing-not-authorized).
* **Pelanggan yang tidak dapat ditagih:** `user_profile_not_billable` dapat berarti bahwa organisasi pelanggan tidak dapat ditagih, misalnya karena belum menyiapkan penagihan. Lihat [cara memperbaiki `user_profile_not_billable`](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#user-profile-not-billable).
* **Batas pengeluaran atau tidak ada kredit:** Permintaan ditolak dengan `linked_organization_spend_limit_reached` ketika pengeluaran pelanggan melalui aplikasi Anda mencapai batas atas pengeluaran mereka atau organisasi mereka mencapai batas pengeluaran bulanannya sendiri. Hal yang sama terjadi ketika tidak ada kredit di akun mereka yang dapat membayar.
* **Hal lainnya:** Lihat [Error Linked billing saat penagihan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/errors#while-billing).

### Anda membayar

Untuk membayar sendiri sebuah permintaan, tetap kirim ID profil pengguna pelanggan di header. Kemudian, hilangkan `billing_policy` atau atur `bill_to`-nya ke `"self"`.

Tanpa `billing_policy`, beta header bersifat opsional:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-user-profile-id: uprof_01HV9Z" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```bash CLI
  ant messages create \
    --user-profile-id uprof_01HV9Z \
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      user_profile_id="uprof_01HV9Z",
  )

  for block in message.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    user_profile_id: "uprof_01HV9Z"
  });

  for (const block of message.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  var message = await client.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [new UserMessageParam { Content = "Hello, Claude" }],
          UserProfileID = "uprof_01HV9Z",
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
  client := anthropic.NewClient()

  message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  	UserProfileID: anthropic.String("uprof_01HV9Z"),
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
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .userProfileId("uprof_01HV9Z")
          .build();
      var message = client.messages().create(params);

      for (var block : message.content()) {
          block.text().ifPresent(textBlock -> IO.println(textBlock.text()));
      }
  }
  ```

  ```php PHP
  use Anthropic\Messages\Model;
  use Anthropic\Messages\TextBlock;

  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: Model::CLAUDE_OPUS_5_5,
      userProfileID: 'uprof_01HV9Z',
  );

  foreach ($message->content as $block) {
      if ($block instanceof TextBlock) {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    user_profile_id: "uprof_01HV9Z"
  )

  message.content.each do |block|
    puts(block.text) if block.is_a?(Anthropic::Models::TextBlock)
  end
  ```
</CodeGroup>

Dengan `bill_to` diatur ke `"self"`, permintaan memerlukan beta header:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    -H "anthropic-version: 2026-10-21" \
    -H "anthropic-beta: user-profiles-billing-2026-10-01" \
    -H "anthropic-user-profile-id: uprof_01HV9Z" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}],
      "billing_policy": {"type": "billing_policy", "bill_to": "self"}
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta user-profiles-billing-2026-10-01 \
    --user-profile-id uprof_01HV9Z \
    --model claude-opus-5-5 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello, Claude"}' \
    --billing-policy '{type: billing_policy, bill_to: self}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  message = client.beta.messages.create(
      model="claude-opus-5-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      betas=["user-profiles-billing-2026-10-01"],
      user_profile_id="uprof_01HV9Z",
      billing_policy={"type": "billing_policy", "bill_to": "self"},
  )

  for block in message.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const message = await client.beta.messages.create({
    model: "claude-opus-5-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    betas: ["user-profiles-billing-2026-10-01"],
    user_profile_id: "uprof_01HV9Z",
    billing_policy: { type: "billing_policy", bill_to: "self" }
  });

  for (const block of message.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Messages;
  using Model = Anthropic.Models.Messages.Model;

  AnthropicClient client = new();

  var message = await client.Beta.Messages.Create(
      new MessageCreateParams
      {
          Model = Model.ClaudeOpus5_5,
          MaxTokens = 1024,
          Messages = [new BetaUserMessageParam { Content = "Hello, Claude" }],
          Betas = ["user-profiles-billing-2026-10-01"],
          UserProfileID = "uprof_01HV9Z",
          BillingPolicy = new() { BillTo = BetaBillTo.Self },
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
  client := anthropic.NewClient()

  message, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5_5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Betas:         []anthropic.AnthropicBeta{"user-profiles-billing-2026-10-01"},
  	UserProfileID: anthropic.String("uprof_01HV9Z"),
  	BillingPolicy: anthropic.BetaBillingPolicyParam{BillTo: anthropic.BetaBillToSelf},
  })
  if err != nil {
  	log.Fatal(err)
  }

  for _, block := range message.Content {
  	if textBlock, ok := block.AsAny().(anthropic.BetaTextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaBillTo;
  import com.anthropic.models.beta.messages.BetaBillingPolicy;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      var params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5_5)
          .maxTokens(1024)
          .addUserMessage("Hello, Claude")
          .addBeta("user-profiles-billing-2026-10-01")
          .userProfileId("uprof_01HV9Z")
          .billingPolicy(BetaBillingPolicy.builder()
              .billTo(BetaBillTo.SELF)
              .build())
          .build();
      var message = client.beta().messages().create(params);

      for (var block : message.content()) {
          block.text().ifPresent(textBlock -> IO.println(textBlock.text()));
      }
  }
  ```

  ```php PHP
  use Anthropic\Beta\Messages\BetaBillingPolicy;
  use Anthropic\Beta\Messages\BetaBillTo;
  use Anthropic\Beta\Messages\BetaTextBlock;
  use Anthropic\Messages\Model;

  $client = new Client();

  $message = $client->beta->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: Model::CLAUDE_OPUS_5_5,
      betas: ['user-profiles-billing-2026-10-01'],
      userProfileID: 'uprof_01HV9Z',
      billingPolicy: BetaBillingPolicy::with(billTo: BetaBillTo::SELF),
  );

  foreach ($message->content as $block) {
      if ($block instanceof BetaTextBlock) {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.beta.messages.create(
    model: Anthropic::Model::CLAUDE_OPUS_5_5,
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    betas: ["user-profiles-billing-2026-10-01"],
    user_profile_id: "uprof_01HV9Z",
    billing_policy: { type: :billing_policy, bill_to: :self }
  )

  message.content.each do |block|
    puts(block.text) if block.is_a?(Anthropic::Beta::BetaTextBlock)
  end
  ```
</CodeGroup>

## Memeriksa hasil

Pertama, periksa di Claude Console bahwa pelanggan sudah ditautkan:

* Halaman User profiles Anda menampilkan profil pelanggan sebagai **Linked**. Hanya anggota dengan peran Admin yang melihat status ini.
* Tab **Overview** aplikasi Anda mencantumkan pelanggan di bawah **Linked customers**, dengan ID koneksi yang Anda simpan.

Kemudian, periksa tagihan di Console, karena permintaan tertagih yang berhasil mengembalikan respons normal yang tidak menyebutkan siapa yang membayar. Halaman [Linked platforms](https://platform.claude.com/linked-platforms) pelanggan uji terbuka untuk anggota organisasi tersebut dengan peran Admin atau Billing.

| Di mana | Apa yang ditampilkan | Seberapa cepat |
| ----- | ----- | ----- |
| Halaman [Linked platforms](https://platform.claude.com/linked-platforms) pelanggan uji | Pengeluaran aplikasi Anda bulan ini, dibandingkan dengan batasnya | Dalam sekitar satu menit |
| Halaman Linked platforms pelanggan uji | Biaya dan penggunaan aplikasi Anda bulan ini | Setiap beberapa jam |
| Halaman [User profiles](https://platform.claude.com/user-profiles) Anda | **Requests** dan **Tokens** menghitung permintaan. **Your spend** tidak. | Sekitar sekali per jam, meskipun permintaan dapat memerlukan beberapa jam untuk muncul |

Ketika pengujian berhasil, [publikasikan aplikasi Anda](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/test-and-publish#publish-the-app) agar pelanggan Anda dapat menautkannya.

## Apa yang perlu disampaikan kepada pelanggan Anda

Sebelum pelanggan sungguhan menautkan, sampaikan hal-hal berikut kepada mereka di produk Anda:

* **Siapa yang dapat memberikan persetujuan:** Seseorang dengan peran Admin atau Billing di organisasi Claude mereka.
* **Akun mana di produk Anda yang mereka tautkan:** Tampilkan di samping tombol.
* **Akun Claude mana yang mereka gunakan:** Minta mereka memeriksa akun yang ditampilkan halaman persetujuan.
* **Bahwa mereka sudah ditautkan:** Setelah penukaran kode, katakan bahwa pelanggan sudah ditautkan, bukan bahwa penagihan sudah aktif. Organisasi pelanggan dapat ditautkan sebelum Anthropic dapat menagihnya, misalnya sebelum organisasi tersebut menyiapkan penagihan.
* **Apa yang Anda tagihkan kepada mereka:** Hanya penggunaan Claude yang ditimbulkan oleh mereka dan pengguna mereka di produk Anda. Untuk aturan lengkapnya, lihat [Apa yang boleh Anda tagihkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing#what-you-may-bill).

## Aturan dan kasus khusus

Bagian-bagian ini memberikan aturan di balik langkah-langkah sebelumnya dan apa yang harus dilakukan dalam kasus tertentu.

### Jika aturan federasi dan autentikasi klien Anda mengharapkan audiens yang berbeda

Back end Anda mengirim JWT dari penyedia identitas Anda ke dua tempat:

* **Ke federasi, untuk Claude API:** JWT harus memiliki audiens aturan federasi Anda. Aturan yang membiarkan audiens-nya kosong mengharapkan `https://api.anthropic.com`.
* **Ke `auth.claude.com`, sebagai client assertion:** JWT harus memiliki tepat satu audiens, yaitu **Expected audience** aplikasi Anda, dari tab **Client authentication**-nya.

Dengan aturan yang membiarkan audiens-nya kosong, keduanya biasanya berbeda, jadi dapatkan JWT untuk setiap audiens dari penyedia identitas Anda. SDK dan CLI membaca JWT federasi dari file yang disebutkan oleh `ANTHROPIC_IDENTITY_TOKEN_FILE`. Client assertion ditempatkan di file yang disebutkan oleh `CLIENT_ASSERTION_FILE`.

### Jika penukaran kode mengalami timeout

Kode hanya berfungsi sekali, tetapi mencoba ulang setelah timeout aman dilakukan. Jika percobaan pertama tidak pernah mencapai `auth.claude.com`, percobaan ulang dalam 5 menit masa berlaku kode akan berhasil. Jika percobaan pertama berhasil sampai, percobaan ulang mengembalikan `invalid_grant` dan tidak mengubah apa pun. Dalam kasus tersebut, [periksa apakah pelanggan sudah ditautkan](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#check-a-links-status):

* **Belum ditautkan:** Mulai lagi dari pushed authorization request.
* **Sudah ditautkan:** Anda tidak memiliki ID koneksi atau token OAuth yang ada di respons yang hilang. Jika Anda hanya meminta `billing:attribution`, arahkan pelanggan untuk memberikan persetujuan lagi dengan scope yang sama. Itu mengembalikan ID koneksi yang sama dan token akses baru. Jika Anda juga meminta `offline_access`, ikuti [Menautkan pelanggan kembali](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again).

### Jika Anda memiliki profil untuk setiap orang

Anda mungkin sudah memiliki profil pengguna untuk setiap orang yang menggunakan produk Anda, dan beberapa di antaranya mungkin bekerja untuk satu pelanggan. Hanya satu profil yang dapat menautkan setiap organisasi, jadi Anthropic merekomendasikan agar Anda membuat satu profil lagi untuk organisasi pelanggan dan menautkan profil tersebut. Kemudian, ID profil yang Anda kirim bergantung pada siapa yang membayar:

* **Permintaan yang dibayar pelanggan:** Kirim ID profil pelanggan. Untuk juga memberi tahu Anthropic dari orang mana sebuah permintaan berasal, kirim ID opaque untuk orang tersebut di `metadata.user_id`, bukan nama, alamat email, atau nomor telepon. Lihat [Identifikasi satu orang dalam sebuah perusahaan](https://platform.claude.com/docs/id/manage-claude/user-profiles#identify-individual-users-within-a-company).
* **Permintaan yang Anda bayar:** Anda dapat tetap mengirim ID profil milik orang tersebut.

### Jika Anda menjual kembali akses API

Jika organisasi Anda menjual kembali akses API, kirim juga `"access_type": "passthrough"` saat Anda membuat profil pelanggan. Contoh-contoh tidak menyertakan `access_type`, yang membuat profil `application`. Untuk kedua jenis tersebut, lihat [Tentukan siapa yang mendapatkan profil](https://platform.claude.com/docs/id/manage-claude/user-profiles#decide-who-gets-a-profile).

### Jika pelanggan memberikan persetujuan lagi

Pelanggan memberikan persetujuan lagi ketika Anda mengarahkan mereka untuk memberikan persetujuan bagi profil yang sudah memiliki koneksi. Apa yang dilakukan penukaran kode bergantung pada scope koneksi dan scope persetujuan baru:

| Pelanggan menyetujui | Apa yang dilakukan penukaran kode | Apa yang Anda lakukan |
| ----- | ----- | ----- |
| `billing:attribution` lagi | Mengembalikan ID koneksi yang sama dan token akses baru | Simpan token akses baru |
| `billing:attribution offline_access` lagi | Mengembalikan `invalid_grant`, dan koneksi tetap seperti sebelumnya | Untuk mendapatkan token OAuth baru, [batalkan tautan pelanggan dan minta mereka menautkan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again) |
| Scope lain, seperti `offline_access` yang ditambahkan ke `billing:attribution` | Mengakhiri koneksi sebelumnya beserta token OAuth-nya dan membuat koneksi baru dengan ID baru | Simpan ID koneksi dan token OAuth baru |

Jika penukaran untuk perubahan scope gagal dengan respons 5xx, koneksi sebelumnya mungkin sudah berakhir. Permintaan yang Anda tagihkan ke pelanggan akan ditolak sampai penukaran baru berhasil. Untuk memulihkan:

1. Arahkan pelanggan untuk memberikan persetujuan lagi dengan scope baru.
2. Jika penukaran tersebut mengembalikan `invalid_grant`, [batalkan tautan pelanggan dan minta mereka menautkan lagi](https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/manage-customers#link-a-customer-again).

### Untuk agen

* Jika pushed authorization request gagal, jangan alihkan browser.
* Saat Anda mengirim permintaan dengan `bill_to: "user_profile"`, catat di log Anda sendiri: tidak ada respons yang menyebutkan siapa yang membayar.

## Langkah selanjutnya

<CardGroup cols={1}>
  <Card title="Apa yang dilihat pelanggan Anda" icon="browser" href="https://platform.claude.com/docs/id/manage-claude/oauth-apps/linked-billing/what-your-customers-see">
    Halaman persetujuan, batas atas pengeluaran, dan email yang dilihat pelanggan Anda, sehingga Anda dapat mendukung mereka
  </Card>
</CardGroup>
