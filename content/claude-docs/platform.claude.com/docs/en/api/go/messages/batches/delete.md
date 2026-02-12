---
source: platform
url: https://platform.claude.com/docs/en/api/go/messages/batches/delete
fetched_at: 2026-02-12T04:27:12.104729Z
sha256: 32ca757c24b0a0d70a9fc4fb1c3b1e94e1195ea499e5cb3f1dd5dcaaf63fc4cd
---

## Delete

`client.Messages.Batches.Delete(ctx, messageBatchID) (*DeletedMessageBatch, error)`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `messageBatchID string`

  ID of the Message Batch.

### Returns

- `type DeletedMessageBatch struct{…}`

  - `ID string`

    ID of the Message Batch.

  - `Type MessageBatchDeleted`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `const MessageBatchDeletedMessageBatchDeleted MessageBatchDeleted = "message_batch_deleted"`
