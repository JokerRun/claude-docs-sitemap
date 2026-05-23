---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/generated_files/download
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 3cf8ca82af8b1d3e5bef67ea0311a8cc535c423475970f172e2ebba224f14432
---

## Download a Claude-generated file

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
