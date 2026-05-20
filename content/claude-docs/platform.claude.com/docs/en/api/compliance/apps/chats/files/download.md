---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/files/download
fetched_at: 2026-05-20T03:15:44.945478Z
sha256: 3a24df78113513f3f5d9b1ac30a377d194dba695974ebc134f2b3425c9994601
---

## Download

**get** `/v1/compliance/apps/chats/files/{claude_file_id}/content`

Downloads the binary content of a file referenced in chat messages.

### Path Parameters

- `claude_file_id: string`

  The file ID (tagged ID, e.g., claude_file_abc123)

### Header Parameters

- `"x-api-key": optional string`

### Example

```http
curl https://api.anthropic.com/v1/compliance/apps/chats/files/$CLAUDE_FILE_ID/content \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```
