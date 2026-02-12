---
source: platform
url: https://platform.claude.com/docs/en/api/java/messages/batches/delete
fetched_at: 2026-02-12T04:27:12.104729Z
sha256: b405fd90399b8b8a6e020f679369d6041a518bcea29ac9c6ad7377263317e547
---

## Delete

`DeletedMessageBatch messages().batches().delete(BatchDeleteParamsparams = BatchDeleteParams.none(), RequestOptionsrequestOptions = RequestOptions.none())`

**delete** `/v1/messages/batches/{message_batch_id}`

Delete a Message Batch.

Message Batches can only be deleted once they've finished processing. If you'd like to delete an in-progress batch, you must first cancel it.

Learn more about the Message Batches API in our [user guide](https://docs.claude.com/en/docs/build-with-claude/batch-processing)

### Parameters

- `BatchDeleteParams params`

  - `Optional<String> messageBatchId`

    ID of the Message Batch.

### Returns

- `class DeletedMessageBatch:`

  - `String id`

    ID of the Message Batch.

  - `JsonValue; type "message_batch_deleted"constant`

    Deleted object type.

    For Message Batches, this is always `"message_batch_deleted"`.

    - `MESSAGE_BATCH_DELETED("message_batch_deleted")`
