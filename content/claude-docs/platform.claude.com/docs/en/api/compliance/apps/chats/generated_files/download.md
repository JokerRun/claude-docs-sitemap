---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/generated_files/download
fetched_at: 2026-05-20T03:15:44.945478Z
sha256: 9d6cae2b5fcc15e2925e0217c041f235c5bfdc275a79e285b2216d603aaa7887
---

## Download

**get** `/v1/compliance/apps/chats/generated-files/{claude_gen_file_id}/content`

Downloads the binary content of a file the assistant created via tool use.

### Path Parameters

- `claude_gen_file_id: string`

  The generated-file id (e.g., 'claude_gen_file_abc123') as returned in `chat_messages[].generated_files[].id` from GET /apps/chats/{claude_chat_id}/messages.

### Header Parameters

- `"x-api-key": optional string`

### Example

```http
curl https://api.anthropic.com/v1/compliance/apps/chats/generated-files/$CLAUDE_GEN_FILE_ID/content \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```
