---
source: platform
url: https://platform.claude.com/docs/en/api/php/beta/environments/delete
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 247b6d1ef3da9b813b884a630075ac96345d96d7a8c86793b7b1f94c024c7f68
---

## Delete Environment

`$client->beta->environments->delete(string environmentID, ?list<AnthropicBeta> betas): BetaEnvironmentDeleteResponse`

**delete** `/v1/environments/{environment_id}`

Delete an environment by ID. Returns a confirmation of the deletion.

### Parameters

- `environmentID: string`

- `betas?:optional list<AnthropicBeta>`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `BetaEnvironmentDeleteResponse`

  - `string id`

    Environment identifier

  - `"environment_deleted" type`

    The type of response

### Example

```php
<?php

require_once dirname(__DIR__) . '/vendor/autoload.php';

$client = new Client(apiKey: 'my-anthropic-api-key');

$betaEnvironmentDeleteResponse = $client->beta->environments->delete(
  'env_011CZkZ9X2dpNyB7HsEFoRfW', betas: ['message-batches-2024-09-24']
);

var_dump($betaEnvironmentDeleteResponse);
```

#### Response

```json
{
  "id": "env_011CZkZ9X2dpNyB7HsEFoRfW",
  "type": "environment_deleted"
}
```
