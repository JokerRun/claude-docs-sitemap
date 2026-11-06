---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/files/download
fetched_at: 2026-11-06T02:14:07.030986Z
sha256: 4fb0cf9e7c59a2ce34415b813de726c29efe0335c79f8570ba2833d920ed363d
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

  The file ID (tagged ID, e.g., claude_file_abc123). Also use this endpoint for any id in `chat_messages[].generated_files[].id` that starts with `claude_file_`.

## Headers

- `"anthropic-version": optional string`

  The version of the Claude API you want to use.

  Read more about versioning and our version history [here](https://platform.claude.com/docs/en/api/versioning?sdk_languages=http).

- `"x-api-key": optional string`

## Example

```bash
curl https://api.anthropic.com/v1/compliance/apps/chats/files/$CLAUDE_FILE_ID/content \
    -H 'anthropic-version: 2023-06-01' \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```
