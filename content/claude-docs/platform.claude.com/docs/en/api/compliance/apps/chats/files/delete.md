---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/files/delete
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 4e2f6d8ef6cea6431039226ec6104ef392b8575e4237644e57b7a3fb412e7dd3
---

---
title: Delete file
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/files/delete
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
