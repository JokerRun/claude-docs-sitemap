---
source: platform
url: https://platform.claude.com/docs/en/api/php/beta/vaults/delete
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: c1ead67c012bb0e9aab287dc558c42a4b8e489f53cc7acd95a4b8b88420bb5c2
---

## Delete Vault

`$client->beta->vaults->delete(string vaultID, ?list<AnthropicBeta> betas): BetaManagedAgentsDeletedVault`

**delete** `/v1/vaults/{vault_id}`

Delete Vault

### Parameters

- `vaultID: string`

- `betas?:optional list<AnthropicBeta>`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `BetaManagedAgentsDeletedVault`

  - `string id`

    Unique identifier of the deleted vault.

  - `Type type`

### Example

```php
<?php

require_once dirname(__DIR__) . '/vendor/autoload.php';

$client = new Client(apiKey: 'my-anthropic-api-key');

$betaManagedAgentsDeletedVault = $client->beta->vaults->delete(
  'vlt_011CZkZDLs7fYzm1hXNPeRjv', betas: ['message-batches-2024-09-24']
);

var_dump($betaManagedAgentsDeletedVault);
```

#### Response

```json
{
  "id": "vlt_011CZkZDLs7fYzm1hXNPeRjv",
  "type": "vault_deleted"
}
```
