---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/files/download
fetched_at: 2026-08-13T02:58:08.547465Z
sha256: 303bbbcd2601c6189e3c15c81a0d8dc04689a6770a6b365b33fcdc476de0fa4a
---

---
title: Download file content
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/files/download
---

## Download file content

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
