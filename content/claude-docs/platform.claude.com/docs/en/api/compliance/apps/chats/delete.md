---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/delete
fetched_at: 2026-09-11T02:21:44.680579Z
sha256: 5d86490a838f3753ab33a7347f457a4095f372268ff63befab54c175fe84e9bc
---

---
title: Delete chat
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/delete
---

# Delete chat

**DELETE** `/v1/compliance/apps/chats/{claude_chat_id}`

Permanently deletes a chat and all associated messages and
files. This is a destructive operation that cannot be undone.

## Path parameters

- `claude_chat_id: string`

  The chat ID (tagged ID, e.g., claude_chat_abc123)

## Headers

- `"anthropic-version": optional string`

  The version of the Claude API you want to use.

  Read more about versioning and our version history [here](https://platform.claude.com/docs/en/api/versioning).

- `"x-api-key": optional string`

## Returns

- `type: optional "claude_chat_deleted"`

  Constant string confirming deletion

  default: claude_chat_deleted

- `id: string`

  The ID of the Claude chat that was deleted

## Example

```bash
curl https://api.anthropic.com/v1/compliance/apps/chats/$CLAUDE_CHAT_ID \
    -X DELETE \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```

### Response (200)

```json
{
  "id": "claude_chat_abc123",
  "type": "claude_chat_deleted"
}
```
