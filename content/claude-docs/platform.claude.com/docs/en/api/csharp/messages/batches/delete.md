---
source: platform
url: https://platform.claude.com/docs/en/api/csharp/messages/batches/delete
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: 025f7fbd9fe00adc32e814119d8945d6bbae74db9229b80da333e9ac43b2cc08
---

## Delete a Message Batch

`DeletedMessageBatch Messages.Batches.Delete(BatchDeleteParamsparameters, CancellationTokencancellationToken = default)`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://platform.claude.com/docs/en/build-with-claude/batch-processing)

### Parameters

- `BatchDeleteParams parameters`

  - `required string messageBatchID`

    ID of the Message Batch.

### Returns

- `class DeletedMessageBatch:`

  - `required string ID`

    ID of the Message Batch.

  - `JsonElement Type "message_batch_deleted"constant`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

### Example

```csharp
BatchDeleteParams parameters = new() { MessageBatchID = "message_batch_id" };

var deletedMessageBatch = await client.Messages.Batches.Delete(parameters);

Console.WriteLine(deletedMessageBatch);
```

#### Response

```json
{
  "id": "msgbatch_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message_batch_deleted"
}
```
