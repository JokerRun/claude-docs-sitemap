---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/generated_files/download
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 2617148d2a7a8155528042d1c274bcd69344886aedd8d09c0d8520ad9894df3a
---

# Download a Claude-generated file

**GET** `/v1/compliance/apps/chats/generated-files/{claude_gen_file_id}/content`

Downloads the binary content of a file the assistant created via tool use.

## Path parameters

- `claude_gen_file_id: string`

  The generated-file id (e.g., 'claude_gen_file_abc123') as returned in `chat_messages[].generated_files[].id` from GET /apps/chats/{claude_chat_id}/messages.

## Headers

- `"x-api-key": optional string`

## Example

```bash
curl https://api.anthropic.com/v1/compliance/apps/chats/generated-files/$CLAUDE_GEN_FILE_ID/content \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```
