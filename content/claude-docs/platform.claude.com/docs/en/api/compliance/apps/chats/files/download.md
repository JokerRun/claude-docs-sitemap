---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/files/download
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 2bb758e06ddc7bb1e193157fe8599f5ee645848261ae3f5911224e1c7bb2ac80
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
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```
