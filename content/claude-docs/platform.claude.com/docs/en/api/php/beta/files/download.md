---
source: platform
url: https://platform.claude.com/docs/en/api/php/beta/files/download
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: f1b31b2413549b05753d9bfad88d4c3c8a8e26a7ff62476f2c900e6a211760e0
---

## Download File

`$client->beta->files->download(string fileID, ?list<AnthropicBeta> betas): download`

**get** `/v1/files/{file_id}/content`

Download File

### Parameters

- `fileID: string`

  ID of the File.

- `betas?:optional list<AnthropicBeta>`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `mixed`

### Example

```php
<?php

require_once dirname(__DIR__) . '/vendor/autoload.php';

$client = new Client(apiKey: 'my-anthropic-api-key');

$response = $client->beta->files->download(
  'file_id', betas: ['message-batches-2024-09-24']
);

var_dump($response);
```
