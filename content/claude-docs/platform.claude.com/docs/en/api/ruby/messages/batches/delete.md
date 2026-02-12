---
source: platform
url: https://platform.claude.com/docs/en/api/ruby/messages/batches/delete
fetched_at: 2026-02-12T04:27:12.104729Z
sha256: f25f8aaec86b9012984f80b540fcce7414ee5d133b2a0577b5a8d446da6a1808
---

## Delete

`messages.batches.delete(message_batch_id) -> DeletedMessageBatch`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `message_batch_id: String`

  ID of the Message Batch.

### Returns

- `class DeletedMessageBatch`

  - `id: String`

    ID of the Message Batch.

  - `type: :message_batch_deleted`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `:message_batch_deleted`
