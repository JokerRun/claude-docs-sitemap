---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/files/download
fetched_at: 2026-09-16T02:20:57.252456Z
sha256: 7dec65639fda10274621f4497911af5921e8fd5d00e890a5e4cb1fb9a3601604
---

---
title: Download file content
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/files/download
---

# Download file content

**GET** `/v1/compliance/apps/chats/files/{claude_file_id}/content`

Downloads the binary content of a file referenced in chat messages.

## Path parameters

- `claude_file_id: string`

  The file ID (tagged ID, e.g., claude_file_abc123)

## Headers

- `"x-api-key": optional string`

## Example

```bash
curl https://api.anthropic.com/v1/compliance/apps/chats/files/$CLAUDE_FILE_ID/content \
    -H 'anthropic-version: 2023-06-01' \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```
