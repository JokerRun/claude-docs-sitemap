---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/files/content
fetched_at: 2026-05-09T03:13:52.260309Z
sha256: cab7ce065b93722f4eb619ce525c7b375ea48ae7e00d16893c281185b2aee02a
---

## Content

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
