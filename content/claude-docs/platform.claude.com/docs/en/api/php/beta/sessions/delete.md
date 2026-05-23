---
source: platform
url: https://platform.claude.com/docs/en/api/php/beta/sessions/delete
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 941e4091e286a292c2085cd8e3dfff031a2ca73b119fdf1e51e6b1c917e3342f
---

## Delete Session

`$client->beta->sessions->delete(string sessionID, ?list<AnthropicBeta> betas): BetaManagedAgentsDeletedSession`

**delete** `/v1/sessions/{session_id}`

Delete Session

### Parameters

- `sessionID: string`

- `betas?:optional list<AnthropicBeta>`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `BetaManagedAgentsDeletedSession`

  - `string id`

  - `Type type`

### Example

```php
<?php

require_once dirname(__DIR__) . '/vendor/autoload.php';

$client = new Client(apiKey: 'my-anthropic-api-key');

$betaManagedAgentsDeletedSession = $client->beta->sessions->delete(
  'sesn_011CZkZAtmR3yMPDzynEDxu7', betas: ['message-batches-2024-09-24']
);

var_dump($betaManagedAgentsDeletedSession);
```

#### Response

```json
{
  "id": "sesn_011CZkZAtmR3yMPDzynEDxu7",
  "type": "session_deleted"
}
```
