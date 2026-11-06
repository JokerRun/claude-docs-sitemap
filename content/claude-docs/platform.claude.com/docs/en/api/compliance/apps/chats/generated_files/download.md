---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/generated_files/download
fetched_at: 2026-11-06T02:14:07.030986Z
sha256: 61ba94991022a29df054a78d440f094766185ee287aaa993a40c3517e98d04be
---

---
title: Download a Claude-generated file
url: https://platform.claude.com/docs/en/api/compliance/apps/chats/generated_files/download
---

# Download a Claude-generated file

**GET** `/v1/compliance/apps/chats/generated-files/{claude_gen_file_id}/content`

Downloads the binary content of a file the assistant created via tool use.

## Path parameters

- `claude_gen_file_id: string`

  The generated-file id (e.g., 'claude_gen_file_abc123') as returned in `chat_messages[].generated_files[].id` from `GET /v1/compliance/apps/chats/{claude_chat_id}/messages`. An id that does not start with `claude_gen_file_` returns a 400 error. `generated_files` can also list ids that start with `claude_file_`; request those from `GET /v1/compliance/apps/chats/files/{claude_file_id}/content` instead.

## Headers

- `"anthropic-version": optional string`

  The version of the Claude API you want to use.

  Read more about versioning and our version history [here](https://platform.claude.com/docs/en/api/versioning?sdk_languages=http).

- `"x-api-key": optional string`

## Example

```bash
curl https://api.anthropic.com/v1/compliance/apps/chats/generated-files/$CLAUDE_GEN_FILE_ID/content \
    -H 'anthropic-version: 2023-06-01' \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```
