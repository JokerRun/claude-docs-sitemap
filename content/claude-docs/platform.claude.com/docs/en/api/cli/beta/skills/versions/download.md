---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/skills/versions/download
fetched_at: 2026-05-23T03:13:35.851650Z
sha256: 783c1aad12c5757c7b07d77a3bb3271b04ac08bae4f9eec37817924ec67711dd
---

## Download Skill Version Content

`$ ant beta:skills:versions download`

**get** `/v1/skills/{skill_id}/versions/{version}/content`

Download a skill version's content as a zip archive.

### Parameters

- `--skill-id: string`

  Path param: Unique identifier for the skill.

  The format and length of IDs may change over time.

- `--version: string`

  Path param: Version identifier for the skill.

  Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

- `--beta: optional array of AnthropicBeta`

  Header param: Optional header to specify the beta version(s) you want to use.

### Returns

- `unnamed_schema_1: file path`

### Example

```cli
ant beta:skills:versions download \
  --api-key my-anthropic-api-key \
  --skill-id skill_id \
  --version version
```
