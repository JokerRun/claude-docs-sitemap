---
source: platform
url: https://platform.claude.com/docs/en/api/php/beta/vaults/credentials/delete
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: d81520caca6565e8e5ed4d87461f7506c69ecd1001d5dcfae76a3843f604cbe7
---

## Delete Credential

`$client->beta->vaults->credentials->delete(string credentialID, string vaultID, ?list<AnthropicBeta> betas): ManagedAgentsDeletedCredential`

**delete** `/v1/vaults/{vault_id}/credentials/{credential_id}`

Delete Credential

### Parameters

- `vaultID: string`

- `credentialID: string`

- `betas?:optional list<AnthropicBeta>`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `ManagedAgentsDeletedCredential`

  - `string id`

    Unique identifier of the deleted credential.

  - `Type type`

### Example

```php
<?php

require_once dirname(__DIR__) . '/vendor/autoload.php';

$client = new Client(apiKey: 'my-anthropic-api-key');

$betaManagedAgentsDeletedCredential = $client
  ->beta
  ->vaults
  ->credentials
  ->delete(
  'vcrd_011CZkZEMt8gZan2iYOQfSkw',
  vaultID: 'vlt_011CZkZDLs7fYzm1hXNPeRjv',
  betas: ['message-batches-2024-09-24'],
);

var_dump($betaManagedAgentsDeletedCredential);
```

#### Response

```json
{
  "id": "vcrd_011CZkZEMt8gZan2iYOQfSkw",
  "type": "vault_credential_deleted"
}
```
