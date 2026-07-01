---
source: platform
url: https://platform.claude.com/docs/en/api/php/beta/messages/batches/delete
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: 7cd7fdc151542dfa448e42f5a457ffdc1141a2f1c2dab3501db40372e37acff9
---

## Delete a Message Batch

`$client->beta->messages->batches->delete(string messageBatchID, ?list<AnthropicBeta> betas): DeletedMessageBatch`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://platform.claude.com/docs/en/build-with-claude/batch-processing)

### Parameters

- `messageBatchID: string`

  ID of the Message Batch.

- `betas?:optional list<AnthropicBeta>`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `DeletedMessageBatch`

  - `string id`

    ID of the Message Batch.

  - `"message_batch_deleted" type`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

### Example

```php
<?php

require_once dirname(__DIR__) . '/vendor/autoload.php';

$client = new Client(apiKey: 'my-anthropic-api-key');

$betaDeletedMessageBatch = $client->beta->messages->batches->delete(
  'message_batch_id', betas: ['message-batches-2024-09-24']
);

var_dump($betaDeletedMessageBatch);
```

#### Response

```json
{
  "id": "msgbatch_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message_batch_deleted"
}
```
