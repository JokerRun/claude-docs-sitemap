---
source: platform
url: https://platform.claude.com/docs/en/api/php/messages/batches/delete
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 2dfe86e890b1794d5cf4506a772d9632907e68210a0e73c6feb99789f49600c8
---

## Delete a Message Batch

`$client->messages->batches->delete(string messageBatchID): DeletedMessageBatch`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `messageBatchID: string`

  ID of the Message Batch.

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

$deletedMessageBatch = $client->messages->batches->delete('message_batch_id');

var_dump($deletedMessageBatch);
```

#### Response

```json
{
  "id": "msgbatch_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message_batch_deleted"
}
```
