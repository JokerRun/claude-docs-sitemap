---
source: platform
url: https://platform.claude.com/docs/en/api/php/beta/files/retrieve_metadata
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 395be7ea5983cd9aec454281f581f10667d5777633747219566e686dff33b9e4
---

## Get File Metadata

`$client->beta->files->retrieveMetadata(string fileID, ?list<AnthropicBeta> betas): FileMetadata`

**get** `/v1/files/{file_id}`

Get File Metadata

### Parameters

- `fileID: string`

  ID of the File.

- `betas?:optional list<AnthropicBeta>`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `FileMetadata`

  - `string id`

    Unique object identifier.

    The format and length of IDs may change over time.

  - `\Datetime createdAt`

    RFC 3339 datetime string representing when the file was created.

  - `string filename`

    Original filename of the uploaded file.

  - `string mimeType`

    MIME type of the file.

  - `int sizeBytes`

    Size of the file in bytes.

  - `"file" type`

    Object type.

    For files, this is always `"file"`.

  - `?bool downloadable`

    Whether the file can be downloaded.

  - `?BetaFileScope scope`

    The scope of this file, indicating the context in which it was created (e.g., a session).

### Example

```php
<?php

require_once dirname(__DIR__) . '/vendor/autoload.php';

$client = new Client(apiKey: 'my-anthropic-api-key');

$fileMetadata = $client->beta->files->retrieveMetadata(
  'file_id', betas: ['message-batches-2024-09-24']
);

var_dump($fileMetadata);
```

#### Response

```json
{
  "id": "file_011CNha8iCJcU1wXNR6q4V8w",
  "created_at": "2025-04-15T18:37:24.100435Z",
  "filename": "document.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 102400,
  "type": "file",
  "downloadable": false,
  "scope": {
    "id": "id",
    "type": "session"
  }
}
```
