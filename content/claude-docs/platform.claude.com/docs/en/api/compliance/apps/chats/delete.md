---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/delete
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 42bbdea86d1e251075312a36344dfb215b1a5e655abf6581c2e6468183882b37
---

## Delete chat

**delete** `/v1/compliance/apps/chats/{claude_chat_id}`

Permanently deletes a chat and all associated messages and
files. This is a destructive operation that cannot be undone.

### Path Parameters

- `claude_chat_id: string`

  The chat ID (tagged ID, e.g., claude_chat_abc123)

### Header Parameters

- `"x-api-key": optional string`

### Returns

- `id: string`

  The ID of the Claude chat that was deleted

- `type: optional "claude_chat_deleted"`

  Constant string confirming deletion

  - `"claude_chat_deleted"`

### Example

```http
curl https://api.anthropic.com/v1/compliance/apps/chats/$CLAUDE_CHAT_ID \
    -X DELETE \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```

#### Response

```json
{
  "id": "claude_chat_abc123",
  "type": "claude_chat_deleted"
}
```
