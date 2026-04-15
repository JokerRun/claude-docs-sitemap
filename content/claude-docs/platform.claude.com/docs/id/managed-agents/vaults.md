---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/vaults
fetched_at: 2026-04-15T03:11:27.437490Z
sha256: 301ef3ce98b6745ce22b976df741d97f717c1433ce7004c38821a9cdf5687251
---

# Autentikasi dengan vault

Daftarkan kredensial per-pengguna saat membuat sesi.

---

Vault dan kredensial adalah primitif autentikasi yang memungkinkan Anda mendaftarkan kredensial untuk layanan pihak ketiga sekali dan mereferensikannya berdasarkan ID saat pembuatan sesi. Ini berarti Anda tidak perlu menjalankan penyimpanan rahasia Anda sendiri, mengirimkan token pada setiap panggilan, atau kehilangan jejak pengguna akhir mana yang ditindaklanjuti oleh agen.

Referensi vault adalah parameter per-sesi, sehingga Anda dapat mengelola produk Anda di tingkat agen dan pengguna Anda di tingkat sesi.

<Note>
Semua permintaan Managed Agents API memerlukan header beta `managed-agents-2026-04-01`. SDK mengatur header beta secara otomatis.
</Note>

## Buat vault

<Warning>
Vault dan kredensial memiliki cakupan ruang kerja, artinya siapa pun dengan akses kunci API dapat menggunakannya untuk mengotorisasi agen menyelesaikan tugas. Untuk mencabut akses, hapus vault atau kredensial.
</Warning>

Vault adalah koleksi `credentials` yang terkait dengan pengguna akhir. Berikan `display_name` dan secara opsional tandai dengan `metadata` sehingga Anda dapat memetakannya kembali ke catatan pengguna Anda sendiri.

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
  --transform id --format yaml)
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

Respons adalah catatan vault lengkap:

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

## Tambahkan kredensial

Setiap kredensial mengikat ke satu `mcp_server_url`. Ketika agen terhubung ke server MCP saat runtime sesi, API mencocokkan URL server terhadap kredensial aktif di vault yang direferensikan dan menyuntikkan token.

<Tabs>
  <Tab title="Kredensial MCP OAuth">

Gunakan `mcp_oauth` ketika server MCP menggunakan OAuth 2.0. Jika Anda menyediakan blok `refresh`, Anthropic menyegarkan token akses atas nama Anda ketika kadaluarsa.

Bidang `refresh.token_endpoint_auth.type` menunjukkan cara mengautentikasi panggilan refresh:
- `none`: klien publik
- `client_secret_basic`: HTTP Basic auth dengan rahasia klien
- `client_secret_post`: rahasia klien di badan POST

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
    "expires_at": "2026-04-15T00:00:00Z",
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
  --transform id --format yaml <<'EOF'
auth:
  type: mcp_oauth
  mcp_server_url: https://mcp.slack.com/mcp
  access_token: xoxp-...
  expires_at: "2026-04-15T00:00:00Z"
  refresh:
    token_endpoint: https://slack.com/api/oauth.v2.access
    client_id: "1234567890.0987654321"
    scope: channels:read chat:write
    refresh_token: xoxe-1-...
    token_endpoint_auth:
      type: client_secret_post
      client_secret: abc123...
EOF
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
        "expires_at": "2026-04-15T00:00:00Z",
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
    expires_at: "2026-04-15T00:00:00Z",
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
        Type = "mcp_oauth",
        McpServerUrl = "https://mcp.slack.com/mcp",
        AccessToken = "xoxp-...",
        ExpiresAt = DateTimeOffset.Parse("2026-04-15T00:00:00Z"),
        Refresh = new()
        {
            TokenEndpoint = "https://slack.com/api/oauth.v2.access",
            ClientID = "1234567890.0987654321",
            Scope = "channels:read chat:write",
            RefreshToken = "xoxe-1-...",
            TokenEndpointAuth = new BetaManagedAgentsTokenEndpointAuthPostParam
            {
                Type = "client_secret_post",
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
			ExpiresAt:    anthropic.Time(time.Date(2026, time.April, 15, 0, 0, 0, 0, time.UTC)),
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
            .expiresAt(OffsetDateTime.parse("2026-04-15T00:00:00Z"))
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
    auth: [
        'type' => 'mcp_oauth',
        'mcp_server_url' => 'https://mcp.slack.com/mcp',
        'access_token' => 'xoxp-...',
        'expires_at' => '2026-04-15T00:00:00Z',
        'refresh' => [
            'token_endpoint' => 'https://slack.com/api/oauth.v2.access',
            'client_id' => '1234567890.0987654321',
            'scope' => 'channels:read chat:write',
            'refresh_token' => 'xoxe-1-...',
            'token_endpoint_auth' => [
                'type' => 'client_secret_post',
                'client_secret' => 'abc123...',
            ],
        ],
    ],
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
    expires_at: "2026-04-15T00:00:00Z",
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
  <Tab title="Kredensial bearer statis">

Gunakan `static_bearer` ketika server MCP menerima token bearer tetap (kunci API, token akses pribadi, atau serupa). Tidak ada alur refresh yang diperlukan.

<CodeGroup defaultLanguage="CLI">
```bash curl
curl -fsSL "https://api.anthropic.com/v1/vaults/$VAULT_ID/credentials" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d '{
    "display_name": "Linear API key",
    "auth": {
      "type": "static_bearer",
      "mcp_server_url": "https://mcp.linear.app/mcp",
      "token": "lin_api_your_linear_key"
    }
  }'
```

```bash CLI
ant beta:vaults:credentials create --vault-id "$VAULT_ID" <<'YAML'
display_name: Linear API key
auth:
  type: static_bearer
  mcp_server_url: https://mcp.linear.app/mcp
  token: lin_api_your_linear_key
YAML
```

```python Python
credential = client.beta.vaults.credentials.create(
    vault_id=vault.id,
    display_name="Linear API key",
    auth={
        "type": "static_bearer",
        "mcp_server_url": "https://mcp.linear.app/mcp",
        "token": "lin_api_your_linear_key",
    },
)
```

```typescript TypeScript
const credential = await client.beta.vaults.credentials.create(vault.id, {
  display_name: "Linear API key",
  auth: {
    type: "static_bearer",
    mcp_server_url: "https://mcp.linear.app/mcp",
    token: "lin_api_your_linear_key"
  }
});
```

```csharp C#
var credential = await client.Beta.Vaults.Credentials.Create(vault.ID, new()
{
    DisplayName = "Linear API key",
    Auth = new BetaManagedAgentsStaticBearerCreateParams
    {
        Type = "static_bearer",
        McpServerUrl = "https://mcp.linear.app/mcp",
        Token = "lin_api_your_linear_key",
    },
});
```

```go Go
credential, err := client.Beta.Vaults.Credentials.New(ctx, vault.ID, anthropic.BetaVaultCredentialNewParams{
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
```

```java Java
var credential = client.beta().vaults().credentials().create(vault.id(),
    CredentialCreateParams.builder()
        .displayName("Linear API key")
        .auth(BetaManagedAgentsStaticBearerCreateParams.builder()
            .type(BetaManagedAgentsStaticBearerCreateParams.Type.STATIC_BEARER)
            .mcpServerUrl("https://mcp.linear.app/mcp")
            .token("lin_api_your_linear_key")
            .build())
        .build());
```

```php PHP
$credential = $client->beta->vaults->credentials->create(
    vaultID: $vault->id,
    displayName: 'Notion token',
    auth: [
        'type' => 'static_bearer',
        'mcp_server_url' => 'https://mcp.linear.app/mcp',
        'token' => 'lin_api_your_linear_key',
    ],
);
```

```ruby Ruby
credential = client.beta.vaults.credentials.create(
  vault.id,
  display_name: "Linear API key",
  auth: {
    type: "static_bearer",
    mcp_server_url: "https://mcp.linear.app/mcp",
    token: "lin_api_your_linear_key"
  }
)
```
</CodeGroup>

  </Tab>
</Tabs>

<Warning>
Bidang rahasia (`token`, `access_token`, `refresh_token`, `client_secret`) hanya dapat ditulis. Mereka tidak pernah dikembalikan dalam respons API.
</Warning>

Kredensial disimpan seperti yang disediakan dan tidak divalidasi sampai runtime sesi. Token yang buruk muncul sebagai kesalahan auth MCP selama sesi, yang dipancarkan tetapi tidak memblokir sesi dari melanjutkan.

Batasan:

- **Satu kredensial aktif per `mcp_server_url` per vault.** Membuat kredensial kedua untuk URL yang sama mengembalikan 409.
- **`mcp_server_url` tidak dapat diubah.** Untuk menunjuk ke server yang berbeda, arsipkan kredensial ini dan buat yang baru.
- **Maksimal 20 kredensial per vault.** Ini sesuai dengan jumlah maksimal server MCP per agen.

## Putar kredensial

Hanya muatan rahasia dan beberapa bidang metadata yang dapat diubah. `mcp_server_url`, `token_endpoint`, dan `client_id` terkunci setelah pembuatan.

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
    "expires_at": "2026-05-15T00:00:00Z",
    "refresh": {"refresh_token": "xoxe-1-new-..."}
  }
}
EOF
````

  
````bash
ant beta:vaults:credentials update \
  --vault-id "$VAULT_ID" \
  --credential-id "$CREDENTIAL_ID" <<'EOF'
auth:
  type: mcp_oauth
  access_token: xoxp-new-...
  expires_at: "2026-05-15T00:00:00Z"
  refresh:
    refresh_token: xoxe-1-new-...
EOF
````

  
````python
client.beta.vaults.credentials.update(
    credential.id,
    vault_id=vault.id,
    auth={
        "type": "mcp_oauth",
        "access_token": "xoxp-new-...",
        "expires_at": "2026-05-15T00:00:00Z",
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
    expires_at: "2026-05-15T00:00:00Z",
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
        Type = "mcp_oauth",
        AccessToken = "xoxp-new-...",
        ExpiresAt = DateTimeOffset.Parse("2026-05-15T00:00:00Z"),
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
			ExpiresAt:   anthropic.Time(time.Date(2026, time.May, 15, 0, 0, 0, 0, time.UTC)),
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
            .expiresAt(OffsetDateTime.parse("2026-05-15T00:00:00Z"))
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
    auth: [
        'type' => 'mcp_oauth',
        'access_token' => 'xoxp-new-...',
        'expires_at' => '2026-05-15T00:00:00Z',
        'refresh' => ['refresh_token' => 'xoxe-1-new-...'],
    ],
);
````

  
````ruby
client.beta.vaults.credentials.update(
  credential.id,
  vault_id: vault.id,
  auth: {
    type: "mcp_oauth",
    access_token: "xoxp-new-...",
    expires_at: "2026-05-15T00:00:00Z",
    refresh: {refresh_token: "xoxe-1-new-..."}
  }
)
````

</CodeGroup>

## Referensikan vault saat pembuatan sesi

Lewatkan `vault_ids` saat membuat sesi:

<CodeGroup>
  
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
  --transform id --format yaml)
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

- Kredensial diselesaikan kembali secara berkala selama sesi, sehingga rotasi atau arsip menyebar ke sesi yang berjalan tanpa restart.
- Ketika vault tidak memiliki kredensial untuk server MCP, koneksi dicoba tanpa autentikasi dan menghasilkan kesalahan.
- Ketika beberapa vault mencakup server MCP, vault pertama dengan kecocokan menang.

## Operasi lainnya

- **Daftar vault atau kredensial:** Dipaginasi, terbaru terlebih dahulu. Catatan yang diarsipkan dikecualikan secara default (lewatkan `include_archived=true` untuk memasukkannya).
- **Arsipkan vault:** `POST /v1/vaults/{id}/archive`. Kaskade ke semua kredensial. Rahasia dihapus; catatan dipertahankan untuk audit. Sesi masa depan yang mereferensikan vault ini gagal; sesi yang berjalan berlanjut.
- **Arsipkan kredensial:** `POST /v1/vaults/{id}/credentials/{cred_id}/archive`. Menghapus muatan rahasia; `mcp_server_url` tetap terlihat. Membebaskan `mcp_server_url` untuk kredensial pengganti.
- **Hapus vault atau kredensial:** Penghapusan keras. Catatan tidak dipertahankan. Gunakan arsip jika Anda memerlukan jejak audit.