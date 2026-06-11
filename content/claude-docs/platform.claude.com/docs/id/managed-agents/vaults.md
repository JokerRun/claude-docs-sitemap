---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/vaults
fetched_at: 2026-06-11T03:14:59.596724Z
sha256: 3ca826adf72db778998bbe58b45160547ef2309c6557eec366f52fdfbafcd6e6
---

# Autentikasi dengan vault

Daftarkan kredensial per pengguna saat membuat sesi.

---

Vault dan kredensial adalah primitif autentikasi yang memungkinkan Anda mendaftarkan kredensial untuk layanan pihak ketiga satu kali dan mereferensikannya berdasarkan ID saat pembuatan sesi. Ini berarti Anda tidak perlu menjalankan penyimpanan rahasia sendiri, mengirimkan token pada setiap panggilan, atau kehilangan jejak pengguna akhir mana yang diwakili oleh agen saat bertindak.

Referensi vault adalah parameter per sesi, sehingga Anda dapat mengelola produk Anda pada tingkat granularitas resource `agent` dan pengguna Anda pada tingkat granularitas resource `session`.

<Note>
Semua permintaan Managed Agents API memerlukan beta header `managed-agents-2026-04-01`. SDK menetapkan beta header tersebut secara otomatis.
</Note>

## Membuat vault \{#create-a-vault}

<Warning>
Vault dan kredensial memiliki cakupan workspace, yang berarti siapa pun dengan kunci API untuk workspace yang sama dapat mereferensikannya saat membuat sesi. Untuk mencabut akses, hapus vault atau kredensial tersebut.
</Warning>

Vault adalah kumpulan `credentials` yang terkait dengan pengguna akhir. Berikan `display_name` dan secara opsional tandai dengan `metadata` agar Anda dapat memetakannya kembali ke catatan pengguna Anda sendiri.

<CodeGroup defaultLanguage="CLI">
  
````bash
vault_id=$(curl --fail-with-body -sS https://api.anthropic.com/v1/vaults \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  --data @- <<'EOF' | jq -r '.id'
{
  "display_name": "Alice",
  "metadata": {"external_user_id": "usr_abc123"}
}
EOF
)
echo "$vault_id"  # "vlt_01ABC..."
````

  
````bash
VAULT_ID=$(ant beta:vaults create \
  --display-name "Alice" \
  --metadata '{external_user_id: usr_abc123}' \
  --transform id --raw-output)
echo "$VAULT_ID"  # "vlt_01ABC..."
````

  
````python
vault = client.beta.vaults.create(
    display_name="Alice",
    metadata={"external_user_id": "usr_abc123"},
)
print(vault.id)  # "vlt_01ABC..."
````

  
````typescript
const vault = await client.beta.vaults.create({
  display_name: "Alice",
  metadata: { external_user_id: "usr_abc123" },
});
console.log(vault.id); // "vlt_01ABC..."
````

  
````csharp
var vault = await client.Beta.Vaults.Create(new()
{
    DisplayName = "Alice",
    Metadata = new Dictionary<string, string> { ["external_user_id"] = "usr_abc123" },
});
Console.WriteLine(vault.ID); // "vlt_01ABC..."
````

  
````go
vault, err := client.Beta.Vaults.New(ctx, anthropic.BetaVaultNewParams{
	DisplayName: "Alice",
	Metadata:    map[string]string{"external_user_id": "usr_abc123"},
})
if err != nil {
	panic(err)
}
fmt.Println(vault.ID) // "vlt_01ABC..."
````

  
````java
var vault = client.beta().vaults().create(VaultCreateParams.builder()
    .displayName("Alice")
    .metadata(VaultCreateParams.Metadata.builder()
        .putAdditionalProperty("external_user_id", JsonValue.from("usr_abc123"))
        .build())
    .build());
IO.println(vault.id()); // "vlt_01ABC..."
````

  
````php
$vault = $client->beta->vaults->create(
    displayName: 'Alice',
    metadata: ['external_user_id' => 'usr_abc123'],
);
echo $vault->id . "\n"; // "vlt_01ABC..."
````

  
````ruby
vault = client.beta.vaults.create(
  display_name: "Alice",
  metadata: {external_user_id: "usr_abc123"}
)
puts vault.id # "vlt_01ABC..."
````

</CodeGroup>

Responsnya adalah catatan vault lengkap:

```json
{
  "type": "vault",
  "id": "vlt_01ABC...",
  "display_name": "Alice",
  "metadata": { "external_user_id": "usr_abc123" },
  "created_at": "2026-03-18T10:00:00Z",
  "updated_at": "2026-03-18T10:00:00Z",
  "archived_at": null
}
```

## Menambahkan kredensial \{#add-a-credential}

Dua kategori kredensial didukung:

- **Kredensial MCP** (`mcp_oauth`, `static_bearer`): setiap kredensial dikunci oleh `mcp_server_url`. Ketika agen terhubung ke server pada URL tersebut saat runtime sesi, token disuntikkan secara otomatis.
- **Variabel lingkungan** (`environment_variable`): setiap kredensial dikunci oleh `secret_name` (nama variabel lingkungan) dan disimpan di sandbox sebagai placeholder opaque. Ketika agen memulai permintaan keluar, placeholder opaque tersebut disubstitusi dengan rahasia asli saat egress. Agen tidak pernah melihat nilai rahasia. Gunakan ini untuk layanan apa pun yang mengautentikasi melalui variabel lingkungan, seperti CLI, SDK, atau panggilan API langsung.

Nilai kredensial aktual yang Anda berikan (`token`, `access_token`, `refresh_token`, `client_secret`, `secret_value`) diperlakukan sebagai field sensitif yang hanya dapat ditulis dan tidak pernah dikembalikan dalam respons API.

<Note>
Kredensial variabel lingkungan (`environment_variable`) belum didukung dengan [sandbox yang di-host sendiri](/docs/id/managed-agents/self-hosted-sandboxes).
</Note>

<Tabs>
  <Tab title="MCP OAuth">

Gunakan `mcp_oauth` ketika server MCP menggunakan OAuth 2.0. Jika Anda menyediakan blok `refresh`, Anthropic akan me-refresh access token atas nama Anda ketika token tersebut kedaluwarsa.

Field `refresh.token_endpoint_auth.type` menunjukkan cara mengautentikasi panggilan refresh:
- `none`: public client
- `client_secret_basic`: autentikasi HTTP Basic dengan client secret
- `client_secret_post`: client secret di dalam body POST

<CodeGroup defaultLanguage="CLI">
  
````bash
credential_id=$(curl --fail-with-body -sS "https://api.anthropic.com/v1/vaults/$vault_id/credentials" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  --data @- <<'EOF' | jq -r '.id'
{
  "display_name": "Alice's Slack",
  "auth": {
    "type": "mcp_oauth",
    "mcp_server_url": "https://mcp.slack.com/mcp",
    "access_token": "xoxp-...",
    "expires_at": "2099-12-31T23:59:59Z",
    "refresh": {
      "token_endpoint": "https://slack.com/api/oauth.v2.access",
      "client_id": "1234567890.0987654321",
      "scope": "channels:read chat:write",
      "refresh_token": "xoxe-1-...",
      "token_endpoint_auth": {"type": "client_secret_post", "client_secret": "abc123..."}
    }
  }
}
EOF
)
````

  
````bash
CREDENTIAL_ID=$(ant beta:vaults:credentials create \
  --vault-id "$VAULT_ID" \
  --display-name "Alice's Slack" \
  --transform id --raw-output <<'YAML'
auth:
  type: mcp_oauth
  mcp_server_url: https://mcp.slack.com/mcp
  access_token: xoxp-...
  expires_at: "2099-12-31T23:59:59Z"
  refresh:
    token_endpoint: https://slack.com/api/oauth.v2.access
    client_id: "1234567890.0987654321"
    scope: channels:read chat:write
    refresh_token: xoxe-1-...
    token_endpoint_auth:
      type: client_secret_post
      client_secret: abc123...
YAML
)
````

  
````python
credential = client.beta.vaults.credentials.create(
    vault_id=vault.id,
    display_name="Alice's Slack",
    auth={
        "type": "mcp_oauth",
        "mcp_server_url": "https://mcp.slack.com/mcp",
        "access_token": "xoxp-...",
        "expires_at": "2099-12-31T23:59:59Z",
        "refresh": {
            "token_endpoint": "https://slack.com/api/oauth.v2.access",
            "client_id": "1234567890.0987654321",
            "scope": "channels:read chat:write",
            "refresh_token": "xoxe-1-...",
            "token_endpoint_auth": {"type": "client_secret_post", "client_secret": "abc123..."},
        },
    },
)
````

  
````typescript
const credential = await client.beta.vaults.credentials.create(vault.id, {
  display_name: "Alice's Slack",
  auth: {
    type: "mcp_oauth",
    mcp_server_url: "https://mcp.slack.com/mcp",
    access_token: "xoxp-...",
    expires_at: "2099-12-31T23:59:59Z",
    refresh: {
      token_endpoint: "https://slack.com/api/oauth.v2.access",
      client_id: "1234567890.0987654321",
      scope: "channels:read chat:write",
      refresh_token: "xoxe-1-...",
      token_endpoint_auth: {
        type: "client_secret_post",
        client_secret: "abc123...",
      },
    },
  },
});
````

  
````csharp
var credential = await client.Beta.Vaults.Credentials.Create(vault.ID, new()
{
    DisplayName = "Alice's Slack",
    Auth = new BetaManagedAgentsMcpOAuthCreateParams
    {
        Type = BetaManagedAgentsMcpOAuthCreateParamsType.McpOAuth,
        McpServerUrl = "https://mcp.slack.com/mcp",
        AccessToken = "xoxp-...",
        ExpiresAt = DateTimeOffset.Parse("2099-12-31T23:59:59Z"),
        Refresh = new()
        {
            TokenEndpoint = "https://slack.com/api/oauth.v2.access",
            ClientID = "1234567890.0987654321",
            Scope = "channels:read chat:write",
            RefreshToken = "xoxe-1-...",
            TokenEndpointAuth = new BetaManagedAgentsTokenEndpointAuthPostParam
            {
                Type = BetaManagedAgentsTokenEndpointAuthPostParamType.ClientSecretPost,
                ClientSecret = "abc123...",
            },
        },
    },
});
````

  
````go
credential, err := client.Beta.Vaults.Credentials.New(ctx, vault.ID, anthropic.BetaVaultCredentialNewParams{
	DisplayName: anthropic.String("Alice's Slack"),
	Auth: anthropic.BetaVaultCredentialNewParamsAuthUnion{
		OfMCPOAuth: &anthropic.BetaManagedAgentsMCPOAuthCreateParams{
			Type:         anthropic.BetaManagedAgentsMCPOAuthCreateParamsTypeMCPOAuth,
			MCPServerURL: "https://mcp.slack.com/mcp",
			AccessToken:  "xoxp-...",
			ExpiresAt:    anthropic.Time(time.Date(2099, time.December, 31, 23, 59, 59, 0, time.UTC)),
			Refresh: anthropic.BetaManagedAgentsMCPOAuthRefreshParams{
				TokenEndpoint: "https://slack.com/api/oauth.v2.access",
				ClientID:      "1234567890.0987654321",
				Scope:         anthropic.String("channels:read chat:write"),
				RefreshToken:  "xoxe-1-...",
				TokenEndpointAuth: anthropic.BetaManagedAgentsMCPOAuthRefreshParamsTokenEndpointAuthUnion{
					OfClientSecretPost: &anthropic.BetaManagedAgentsTokenEndpointAuthPostParam{
						Type:         anthropic.BetaManagedAgentsTokenEndpointAuthPostParamTypeClientSecretPost,
						ClientSecret: "abc123...",
					},
				},
			},
		},
	},
})
if err != nil {
	panic(err)
}
````

  
````java
var credential = client.beta().vaults().credentials().create(vault.id(),
    CredentialCreateParams.builder()
        .displayName("Alice's Slack")
        .auth(BetaManagedAgentsMcpOAuthCreateParams.builder()
            .type(BetaManagedAgentsMcpOAuthCreateParams.Type.MCP_OAUTH)
            .mcpServerUrl("https://mcp.slack.com/mcp")
            .accessToken("xoxp-...")
            .expiresAt(OffsetDateTime.parse("2099-12-31T23:59:59Z"))
            .refresh(BetaManagedAgentsMcpOAuthRefreshParams.builder()
                .tokenEndpoint("https://slack.com/api/oauth.v2.access")
                .clientId("1234567890.0987654321")
                .scope("channels:read chat:write")
                .refreshToken("xoxe-1-...")
                .clientSecretPostTokenEndpointAuth("abc123...")
                .build())
            .build())
        .build());
````

  
````php
$credential = $client->beta->vaults->credentials->create(
    vaultID: $vault->id,
    displayName: "Alice's Slack",
    auth: ManagedAgentsMCPOAuthCreateParams::with(
        type: 'mcp_oauth',
        mcpServerURL: 'https://mcp.slack.com/mcp',
        accessToken: 'xoxp-...',
        expiresAt: new DateTimeImmutable('2099-12-31T23:59:59Z'),
        refresh: ManagedAgentsMCPOAuthRefreshParams::with(
            tokenEndpoint: 'https://slack.com/api/oauth.v2.access',
            clientID: '1234567890.0987654321',
            scope: 'channels:read chat:write',
            refreshToken: 'xoxe-1-...',
            tokenEndpointAuth: ManagedAgentsTokenEndpointAuthPostParam::with(
                type: 'client_secret_post',
                clientSecret: 'abc123...',
            ),
        ),
    ),
);
````

  
````ruby
credential = client.beta.vaults.credentials.create(
  vault.id,
  display_name: "Alice's Slack",
  auth: {
    type: "mcp_oauth",
    mcp_server_url: "https://mcp.slack.com/mcp",
    access_token: "xoxp-...",
    expires_at: "2099-12-31T23:59:59Z",
    refresh: {
      token_endpoint: "https://slack.com/api/oauth.v2.access",
      client_id: "1234567890.0987654321",
      scope: "channels:read chat:write",
      refresh_token: "xoxe-1-...",
      token_endpoint_auth: {
        type: "client_secret_post",
        client_secret: "abc123..."
      }
    }
  }
)
````

</CodeGroup>

  </Tab>
  <Tab title="MCP static bearer">

Gunakan `static_bearer` ketika server MCP menerima bearer token tetap (kunci API, personal access token, atau sejenisnya). Tidak diperlukan alur refresh.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl --fail-with-body -sS "https://api.anthropic.com/v1/vaults/$vault_id/credentials" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  --data @- <<'EOF'
{
  "display_name": "Linear API key",
  "auth": {
    "type": "static_bearer",
    "mcp_server_url": "https://mcp.linear.app/mcp",
    "token": "lin_api_your_linear_key"
  }
}
EOF
````

  
````bash
ant beta:vaults:credentials create --vault-id "$VAULT_ID" <<'YAML'
display_name: Linear API key
auth:
  type: static_bearer
  mcp_server_url: https://mcp.linear.app/mcp
  token: lin_api_your_linear_key
YAML
````

  
````python
bearer_credential = client.beta.vaults.credentials.create(
    vault_id=vault.id,
    display_name="Linear API key",
    auth={
        "type": "static_bearer",
        "mcp_server_url": "https://mcp.linear.app/mcp",
        "token": "lin_api_your_linear_key",
    },
)
````

  
````typescript
const bearerCredential = await client.beta.vaults.credentials.create(vault.id, {
  display_name: "Linear API key",
  auth: {
    type: "static_bearer",
    mcp_server_url: "https://mcp.linear.app/mcp",
    token: "lin_api_your_linear_key",
  },
});
````

  
````csharp
var bearerCredential = await client.Beta.Vaults.Credentials.Create(vault.ID, new()
{
    DisplayName = "Linear API key",
    Auth = new BetaManagedAgentsStaticBearerCreateParams
    {
        Type = BetaManagedAgentsStaticBearerCreateParamsType.StaticBearer,
        McpServerUrl = "https://mcp.linear.app/mcp",
        Token = "lin_api_your_linear_key",
    },
});
````

  
````go
bearerCredential, err := client.Beta.Vaults.Credentials.New(ctx, vault.ID, anthropic.BetaVaultCredentialNewParams{
	DisplayName: anthropic.String("Linear API key"),
	Auth: anthropic.BetaVaultCredentialNewParamsAuthUnion{
		OfStaticBearer: &anthropic.BetaManagedAgentsStaticBearerCreateParams{
			Type:         anthropic.BetaManagedAgentsStaticBearerCreateParamsTypeStaticBearer,
			MCPServerURL: "https://mcp.linear.app/mcp",
			Token:        "lin_api_your_linear_key",
		},
	},
})
if err != nil {
	panic(err)
}
_ = bearerCredential
````

  
````java
var bearerCredential = client.beta().vaults().credentials().create(vault.id(),
    CredentialCreateParams.builder()
        .displayName("Linear API key")
        .auth(BetaManagedAgentsStaticBearerCreateParams.builder()
            .type(BetaManagedAgentsStaticBearerCreateParams.Type.STATIC_BEARER)
            .mcpServerUrl("https://mcp.linear.app/mcp")
            .token("lin_api_your_linear_key")
            .build())
        .build());
````

  
````php
$bearerCredential = $client->beta->vaults->credentials->create(
    vaultID: $vault->id,
    displayName: 'Linear API key',
    auth: ManagedAgentsStaticBearerCreateParams::with(
        type: 'static_bearer',
        mcpServerURL: 'https://mcp.linear.app/mcp',
        token: 'lin_api_your_linear_key',
    ),
);
````

  
````ruby
bearer_credential = client.beta.vaults.credentials.create(
  vault.id,
  display_name: "Linear API key",
  auth: {
    type: "static_bearer",
    mcp_server_url: "https://mcp.linear.app/mcp",
    token: "lin_api_your_linear_key"
  }
)
````

</CodeGroup>

  </Tab>
  <Tab title="Variabel lingkungan">

Gunakan `environment_variable` untuk mengautentikasi ke layanan eksternal melalui variabel lingkungan, seperti CLI, SDK, atau panggilan API langsung.

Array `networking.allowed_hosts` mengontrol host keluar mana yang dapat disubstitusi dengan rahasia tersebut. Gunakan `"type": "limited"` dengan daftar spesifik, atau `"type": "unrestricted"` jika pemanggil menjangkau domain yang tidak dapat Anda enumerasi sebelumnya.

Membatasi domain sangat disarankan untuk tujuan keamanan, dan mencegah kunci Anda dibagikan ke host yang tidak diotorisasi.

<Note>
`networking.allowed_hosts` pada kredensial vault mengontrol permintaan mana yang menggunakan rahasia tersebut, bukan permintaan mana yang diizinkan. Agar agen benar-benar dapat menjangkau suatu domain, domain tersebut juga harus diizinkan pada [tingkat environment](/docs/id/managed-agents/environments). Kedua tingkat harus menyertakan domain tersebut (baik melalui networking `unrestricted` atau dengan secara eksplisit mencantumkan domain di `allowed_hosts`) agar permintaan yang disubstitusi rahasia dapat berhasil.
</Note>

<CodeGroup defaultLanguage="CLI">
  
````bash
curl --fail-with-body -sS "https://api.anthropic.com/v1/vaults/$vault_id/credentials" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  --data @- <<'EOF'
{
  "auth": {
    "type": "environment_variable",
    "secret_name": "NOTION_API_KEY",
    "secret_value": "sk-your-secret-here",
    "networking": {
      "type": "limited",
      "allowed_hosts": ["api.notion.com"]
    }
  },
  "display_name": "Notion API key for sandbox"
}
EOF
````

  
````bash
ant beta:vaults:credentials create --vault-id "$VAULT_ID" <<'YAML'
display_name: Notion API key for sandbox
auth:
  type: environment_variable
  secret_name: NOTION_API_KEY
  secret_value: sk-your-secret-here
  networking:
    type: limited
    allowed_hosts: [api.notion.com]
YAML
````

  
````python
env_credential = client.beta.vaults.credentials.create(
    vault_id=vault.id,
    auth={
        "type": "environment_variable",
        "secret_name": "NOTION_API_KEY",
        "secret_value": "sk-your-secret-here",
        "networking": {
            "type": "limited",
            "allowed_hosts": ["api.notion.com"],
        },
    },
    display_name="Notion API key for sandbox",
)
````

  
````typescript
const envVarCredential = await client.beta.vaults.credentials.create(vault.id, {
  auth: {
    type: "environment_variable",
    secret_name: "NOTION_API_KEY",
    secret_value: "sk-your-secret-here",
    networking: {
      type: "limited",
      allowed_hosts: ["api.notion.com"],
    },
  },
  display_name: "Notion API key for sandbox",
});
````

  
````csharp
var envVarCredential = await client.Beta.Vaults.Credentials.Create(vault.ID, new()
{
    DisplayName = "Notion API key for sandbox",
    Auth = new BetaManagedAgentsEnvironmentVariableCreateParams
    {
        Type = BetaManagedAgentsEnvironmentVariableCreateParamsType.EnvironmentVariable,
        SecretName = "NOTION_API_KEY",
        SecretValue = "sk-your-secret-here",
        Networking = new BetaManagedAgentsLimitedCredentialNetworkingParams
        {
            Type = BetaManagedAgentsLimitedCredentialNetworkingParamsType.Limited,
            AllowedHosts = ["api.notion.com"],
        },
    },
});
````

  
````go
envVarCredential, err := client.Beta.Vaults.Credentials.New(ctx, vault.ID, anthropic.BetaVaultCredentialNewParams{
	DisplayName: anthropic.String("Notion API key for sandbox"),
	Auth: anthropic.BetaVaultCredentialNewParamsAuthUnion{
		OfEnvironmentVariable: &anthropic.BetaManagedAgentsEnvironmentVariableCreateParams{
			Type:        anthropic.BetaManagedAgentsEnvironmentVariableCreateParamsTypeEnvironmentVariable,
			SecretName:  "NOTION_API_KEY",
			SecretValue: "sk-your-secret-here",
			Networking: anthropic.BetaManagedAgentsCredentialNetworkingParamsUnion{
				OfLimited: &anthropic.BetaManagedAgentsLimitedCredentialNetworkingParams{
					Type:         anthropic.BetaManagedAgentsLimitedCredentialNetworkingParamsTypeLimited,
					AllowedHosts: []string{"api.notion.com"},
				},
			},
		},
	},
})
if err != nil {
	panic(err)
}
_ = envVarCredential
````

  
````java
var envVarCredential = client.beta().vaults().credentials().create(vault.id(),
    CredentialCreateParams.builder()
        .displayName("Notion API key for sandbox")
        .auth(BetaManagedAgentsEnvironmentVariableCreateParams.builder()
            .type(BetaManagedAgentsEnvironmentVariableCreateParams.Type.ENVIRONMENT_VARIABLE)
            .secretName("NOTION_API_KEY")
            .secretValue("sk-your-secret-here")
            .limitedNetworking(List.of("api.notion.com"))
            .build())
        .build());
````

  
````php
$envVarCredential = $client->beta->vaults->credentials->create(
    vaultID: $vault->id,
    displayName: 'Notion API key for sandbox',
    auth: ManagedAgentsEnvironmentVariableCreateParams::with(
        type: 'environment_variable',
        secretName: 'NOTION_API_KEY',
        secretValue: 'sk-your-secret-here',
        networking: ManagedAgentsLimitedCredentialNetworkingParams::with(
            type: 'limited',
            allowedHosts: ['api.notion.com'],
        ),
    ),
);
````

  
````ruby
env_credential = client.beta.vaults.credentials.create(
  vault.id,
  display_name: "Notion API key for sandbox",
  auth: {
    type: "environment_variable",
    secret_name: "NOTION_API_KEY",
    secret_value: "sk-your-secret-here",
    networking: {
      type: "limited",
      allowed_hosts: ["api.notion.com"]
    }
  }
)
````

</CodeGroup>

Substitusi terjadi saat egress, bukan di dalam sandbox. Apa pun yang memproses kredensial secara lokal akan melihat placeholder opaque, bukan nilai aslinya: klien yang memvalidasi format kredensial saat startup mungkin menolaknya, dan klien yang menghitung signature permintaan dari rahasia tersebut (misalnya, AWS SigV4) akan menghasilkan signature yang tidak valid. Kredensial variabel lingkungan berfungsi untuk klien yang mengirim nilai rahasia secara verbatim dalam permintaan keluar.

Substitusi hanya berlaku untuk arah keluar. Jika klien menggunakan rahasia yang tersimpan untuk mengambil session token (misalnya, OAuth client-credentials grant), token yang dikembalikan tiba di sandbox tanpa diredaksi. Untuk alur berbasis pertukaran, lakukan pertukaran tersebut sendiri dan simpan token yang dihasilkan di vault sebagai gantinya.

<Tip>
Batasi cakupan kunci API hanya pada izin yang dibutuhkan agen. Agen dapat melakukan apa pun yang diizinkan oleh kunci tersebut, sehingga kunci dengan izin yang lebih luas dari yang diperlukan akan meningkatkan radius dampak jika agen berperilaku tidak terduga.
</Tip>

  </Tab>
</Tabs>

Kredensial disimpan sebagaimana diberikan dan tidak divalidasi hingga runtime sesi. Kredensial yang tidak valid akan muncul sebagai error autentikasi atau error downstream selama sesi, yang dipancarkan tetapi tidak menghalangi sesi untuk terus berjalan.

Batasan:

- **Kunci unik per vault.** `mcp_server_url` (kredensial MCP) dan `secret_name` (kredensial variabel lingkungan) harus unik di antara kredensial aktif dalam sebuah vault. Membuat duplikat akan mengembalikan 409.
- **Kunci bersifat immutable.** Untuk mengubah `mcp_server_url` atau `secret_name`, arsipkan kredensial dan buat yang baru.
- **Maksimum 20 kredensial per vault.**

## Mereferensikan vault saat pembuatan sesi \{#reference-the-vault-at-session-creation}

Berikan `vault_ids` saat membuat sesi:

<CodeGroup defaultLanguage="CLI">
  
````bash
session_id=$(curl --fail-with-body -sS https://api.anthropic.com/v1/sessions \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  --data @- <<EOF | jq -r '.id'
{
  "agent": "$agent_id",
  "environment_id": "$environment_id",
  "vault_ids": ["$vault_id"],
  "title": "Alice's Slack digest"
}
EOF
)
````

  
````bash
SESSION_ID=$(ant beta:sessions create \
  --agent "$AGENT_ID" \
  --environment-id "$ENVIRONMENT_ID" \
  --vault-id "$VAULT_ID" \
  --title "Alice's Slack digest" \
  --transform id --raw-output)
````

  
````python
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    vault_ids=[vault.id],
    title="Alice's Slack digest",
)
````

  
````typescript
const session = await client.beta.sessions.create({
  agent: agent.id,
  environment_id: environment.id,
  vault_ids: [vault.id],
  title: "Alice's Slack digest",
});
````

  
````csharp
var session = await client.Beta.Sessions.Create(new()
{
    Agent = agent.ID,
    EnvironmentID = environment.ID,
    VaultIds = [vault.ID],
    Title = "Alice's Slack digest",
});
````

  
````go
session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
	Agent: anthropic.BetaSessionNewParamsAgentUnion{
		OfString: anthropic.String(agent.ID),
	},
	EnvironmentID: environment.ID,
	VaultIDs:      []string{vault.ID},
	Title:         anthropic.String("Alice's Slack digest"),
})
if err != nil {
	panic(err)
}
````

  
````java
var session = client.beta().sessions().create(SessionCreateParams.builder()
    .agent(agent.id())
    .environmentId(environment.id())
    .vaultIds(List.of(vault.id()))
    .title("Alice's Slack digest")
    .build());
````

  
````php
$session = $client->beta->sessions->create(
    agent: $agent->id,
    environmentID: $environment->id,
    vaultIDs: [$vault->id],
    title: "Alice's Slack digest",
);
````

  
````ruby
session = client.beta.sessions.create(
  agent: agent.id,
  environment_id: environment.id,
  vault_ids: [vault.id],
  title: "Alice's Slack digest"
)
````

</CodeGroup>

Perilaku runtime:
- Ketika tidak ada kredensial MCP yang cocok berdasarkan `mcp_server_url`, koneksi dicoba tanpa autentikasi dan akan menghasilkan error jika server memerlukan autentikasi.
- Ketika beberapa vault berisi kredensial yang cocok, vault pertama dengan kecocokan yang menang.
- Dalam [sesi multi-agen](/docs/id/managed-agents/multi-agent), kredensial vault berlaku untuk setiap thread. Agen yang definisinya sendiri mendeklarasikan server MCP yang cocok akan mengautentikasi dengan kredensial ini. Lihat [Menghubungkan agen ke server MCP](/docs/id/managed-agents/multi-agent#connect-agents-to-mcp-servers).

## Merotasi kredensial \{#rotate-a-credential}

Nilai rahasia dan `display_name` dapat diperbarui. Field struktural (`mcp_server_url`, `secret_name`, `token_endpoint`, `client_id`) dikunci setelah pembuatan. Untuk mengubahnya, arsipkan kredensial dan buat yang baru.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/vaults/$vault_id/credentials/$credential_id" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  --data @- <<'EOF' > /dev/null
{
  "auth": {
    "type": "mcp_oauth",
    "access_token": "xoxp-new-...",
    "expires_at": "2099-12-31T23:59:59Z",
    "refresh": {"refresh_token": "xoxe-1-new-..."}
  }
}
EOF
````

  
````bash
ant beta:vaults:credentials update \
  --vault-id "$VAULT_ID" \
  --credential-id "$CREDENTIAL_ID" <<'YAML'
auth:
  type: mcp_oauth
  access_token: xoxp-new-...
  expires_at: "2099-12-31T23:59:59Z"
  refresh:
    refresh_token: xoxe-1-new-...
YAML
````

  
````python
client.beta.vaults.credentials.update(
    credential.id,
    vault_id=vault.id,
    auth={
        "type": "mcp_oauth",
        "access_token": "xoxp-new-...",
        "expires_at": "2099-12-31T23:59:59Z",
        "refresh": {"refresh_token": "xoxe-1-new-..."},
    },
)
````

  
````typescript
await client.beta.vaults.credentials.update(credential.id, {
  vault_id: vault.id,
  auth: {
    type: "mcp_oauth",
    access_token: "xoxp-new-...",
    expires_at: "2099-12-31T23:59:59Z",
    refresh: {
      refresh_token: "xoxe-1-new-...",
    },
  },
});
````

  
````csharp
await client.Beta.Vaults.Credentials.Update(credential.ID, new()
{
    VaultID = vault.ID,
    Auth = new BetaManagedAgentsMcpOAuthUpdateParams
    {
        Type = BetaManagedAgentsMcpOAuthUpdateParamsType.McpOAuth,
        AccessToken = "xoxp-new-...",
        ExpiresAt = DateTimeOffset.Parse("2099-12-31T23:59:59Z"),
        Refresh = new() { RefreshToken = "xoxe-1-new-..." },
    },
});
````

  
````go
_, err = client.Beta.Vaults.Credentials.Update(ctx, credential.ID, anthropic.BetaVaultCredentialUpdateParams{
	VaultID: vault.ID,
	Auth: anthropic.BetaVaultCredentialUpdateParamsAuthUnion{
		OfMCPOAuth: &anthropic.BetaManagedAgentsMCPOAuthUpdateParams{
			Type:        anthropic.BetaManagedAgentsMCPOAuthUpdateParamsTypeMCPOAuth,
			AccessToken: anthropic.String("xoxp-new-..."),
			ExpiresAt:   anthropic.Time(time.Date(2099, time.December, 31, 23, 59, 59, 0, time.UTC)),
			Refresh: anthropic.BetaManagedAgentsMCPOAuthRefreshUpdateParams{
				RefreshToken: anthropic.String("xoxe-1-new-..."),
			},
		},
	},
})
if err != nil {
	panic(err)
}
````

  
````java
client.beta().vaults().credentials().update(credential.id(),
    CredentialUpdateParams.builder()
        .vaultId(vault.id())
        .auth(BetaManagedAgentsMcpOAuthUpdateParams.builder()
            .type(BetaManagedAgentsMcpOAuthUpdateParams.Type.MCP_OAUTH)
            .accessToken("xoxp-new-...")
            .expiresAt(OffsetDateTime.parse("2099-12-31T23:59:59Z"))
            .refresh(BetaManagedAgentsMcpOAuthRefreshUpdateParams.builder()
                .refreshToken("xoxe-1-new-...")
                .build())
            .build())
        .build());
````

  
````php
$client->beta->vaults->credentials->update(
    $credential->id,
    vaultID: $vault->id,
    auth: ManagedAgentsMCPOAuthUpdateParams::with(
        type: 'mcp_oauth',
        accessToken: 'xoxp-new-...',
        expiresAt: new DateTimeImmutable('2099-12-31T23:59:59Z'),
        refresh: ManagedAgentsMCPOAuthRefreshUpdateParams::with(refreshToken: 'xoxe-1-new-...'),
    ),
);
````

  
````ruby
client.beta.vaults.credentials.update(
  credential.id,
  vault_id: vault.id,
  auth: {
    type: "mcp_oauth",
    access_token: "xoxp-new-...",
    expires_at: "2099-12-31T23:59:59Z",
    refresh: {refresh_token: "xoxe-1-new-..."}
  }
)
````

</CodeGroup>

## Siklus hidup kredensial \{#credential-lifecycle}

Kredensial di-resolve ulang secara berkala, baik selama sesi maupun selama siklus hidup vault. Ini memastikan bahwa rotasi, pengarsipan, atau penghapusan kredensial terpropagasi ke sesi yang sedang berjalan tanpa perlu restart.

Untuk mendapatkan notifikasi jika kredensial diarsipkan, dihapus, atau gagal di-refresh, Anda dapat berlangganan [webhook](/docs/id/managed-agents/webhooks) vault dan kredensial yang terkait dengan perubahan siklus hidup tersebut.

| Event | Pemicu |
| ----- | ------- |
| `vault.archived` | Vault diarsipkan. Event `vault_credential.archived` juga dipancarkan untuk setiap kredensial yang mendasarinya. |
| `vault.deleted` | Vault dihapus. Event `vault_credential.deleted` juga dipancarkan untuk setiap kredensial yang mendasarinya. |
| `vault_credential.archived` | Kredensial diarsipkan, baik secara langsung maupun sebagai akibat dari pengarsipan vault. |
| `vault_credential.deleted` | Kredensial dihapus, baik secara langsung maupun sebagai akibat dari penghapusan vault. |
| `vault_credential.refresh_failed` | Kredensial `mcp_oauth` tidak dapat di-refresh (refresh token tidak valid, atau error yang tidak dapat dipulihkan dari server OAuth). |

<Note>
Ini adalah daftar webhook yang tidak lengkap; lihat [Berlangganan webhook](/docs/id/managed-agents/webhooks) untuk daftar lengkapnya.
</Note>

Untuk kredensial `mcp_oauth`, resolusi ulang juga me-refresh access token jika telah kedaluwarsa. Jika refresh gagal, event `vault_credential.refresh_failed` akan dipancarkan.

### Mendiagnosis kegagalan refresh OAuth \{#diagnose-an-o-auth-refresh-failure}

Untuk mendiagnosis mengapa refresh gagal, panggil `POST /v1/vaults/{vault_id}/credentials/{credential_id}/mcp_oauth_validate` (atau `client.beta.vaults.credentials.mcp_oauth_validate(...)` di SDK). Ini memungkinkan Anda memutuskan cara menangani kegagalan tersebut; tindakan yang tepat bergantung pada jenis error.

`status` tingkat atas memberi tahu Anda apa yang harus dilakukan selanjutnya:

- `valid`: token berfungsi; tidak ada tindakan yang diperlukan.
- `invalid`: grant telah hilang atau server OAuth menolak refresh dengan 4xx. Minta pengguna akhir untuk mengotorisasi ulang.
- `unknown`: error sementara (5xx, 429, atau kegagalan jaringan). Tunggu dan coba lagi.

<CodeGroup defaultLanguage="CLI">
  
````bash
curl --fail-with-body -sS -X POST \
  "https://api.anthropic.com/v1/vaults/$vault_id/credentials/$credential_id/mcp_oauth_validate?beta=true" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01"
````

  
````bash
ant beta:vaults:credentials mcp-oauth-validate \
  --vault-id "$VAULT_ID" \
  --credential-id "$CREDENTIAL_ID" \
  --transform status --raw-output  # "valid", "invalid", or "unknown"
````

  
````python
validation = client.beta.vaults.credentials.mcp_oauth_validate(
    credential.id,
    vault_id=vault.id,
)
print(validation.status)  # "valid", "invalid", or "unknown"
````

  
````typescript
const validation = await client.beta.vaults.credentials.mcpOAuthValidate(
  credential.id,
  { vault_id: vault.id },
);
console.log(validation.status); // "valid", "invalid", or "unknown"
````

  
````csharp
var validation = await client.Beta.Vaults.Credentials.McpOAuthValidate(credential.ID, new()
{
    VaultID = vault.ID,
});
Console.WriteLine(validation.Status.Raw()); // "valid", "invalid", or "unknown"
````

  
````go
validation, err := client.Beta.Vaults.Credentials.MCPOAuthValidate(ctx, credential.ID, anthropic.BetaVaultCredentialMCPOAuthValidateParams{
	VaultID: vault.ID,
})
if err != nil {
	panic(err)
}
fmt.Println(validation.Status) // "valid", "invalid", or "unknown"
````

  
````java
var validation = client.beta().vaults().credentials().mcpOAuthValidate(credential.id(),
    CredentialMcpOAuthValidateParams.builder()
        .vaultId(vault.id())
        .build());
IO.println(validation.status()); // valid, invalid, or unknown
````

  
````php
$validation = $client->beta->vaults->credentials->mcpOAuthValidate(
    $credential->id,
    vaultID: $vault->id,
);
echo $validation->status . "\n"; // "valid", "invalid", or "unknown"
````

  
````ruby
validation = client.beta.vaults.credentials.mcp_oauth_validate(
  credential.id,
  vault_id: vault.id
)
puts validation.status # :valid, :invalid, or :unknown
````

</CodeGroup>

Responsnya adalah objek `vault_credential_validation`. `mcp_probe` menyertakan langkah handshake MCP yang gagal; `refresh` menyertakan hasil dari percobaan refresh.

```json
{
  "type": "vault_credential_validation",
  "credential_id": "vcrd_01ABC...",
  "vault_id": "vlt_01XYZ...",
  "validated_at": "2026-04-29T17:12:00Z",
  "has_refresh_token": false,
  "status": "invalid",
  "mcp_probe": {
    "method": "initialize",
    "http_response": {
      "status_code": 401,
      "content_type": "application/json",
      "body": "{\"error\":\"invalid_token\"}",
      "body_truncated": false
    }
  },
  "refresh": {
    "status": "no_refresh_token",
    "http_response": null
  }
}
```

## Operasi lainnya \{#other-operations}

- **Mendaftar vault atau kredensial:** Dipaginasi, terbaru lebih dulu. Catatan yang diarsipkan dikecualikan secara default (berikan `include_archived=true` untuk menyertakannya).
- **Mengarsipkan vault:** `POST /v1/vaults/{id}/archive`. Berlaku secara kaskade ke semua kredensial. Rahasia dihapus; catatan dipertahankan untuk audit. Sesi mendatang yang mereferensikan vault ini akan gagal; sesi yang sedang berjalan tetap berlanjut.
- **Mengarsipkan kredensial:** `POST /v1/vaults/{id}/credentials/{cred_id}/archive`. Menghapus payload rahasia; kunci kredensial (`mcp_server_url` atau `secret_name`) tetap terlihat dan dibebaskan untuk kredensial pengganti.
- **Menghapus vault atau kredensial:** Hard delete. Catatan tidak dipertahankan. Gunakan arsip jika Anda memerlukan jejak audit.