---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/files/delete
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 041cef6b29a2e34b5b7ccb80fa0f50b4cb7ae46cf95a15668f1e6b45b87f260e
---

## Delete file

**delete** `/v1/compliance/apps/chats/files/{claude_file_id}`

Permanently deletes a specific file. This is a destructive
operation that cannot be undone.

### Path Parameters

- `claude_file_id: string`

  The file ID (tagged ID, e.g., claude_file_abc123)

### Header Parameters

- `"x-api-key": optional string`

### Returns

- `id: string`

  The ID of the file that was deleted

- `type: optional "claude_file_deleted"`

  Constant string confirming deletion

  - `"claude_file_deleted"`

### Example

```http
curl https://api.anthropic.com/v1/compliance/apps/chats/files/$CLAUDE_FILE_ID \
    -X DELETE \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```

#### Response

```json
{
  "id": "claude_file_xyz789",
  "type": "claude_file_deleted"
}
```
