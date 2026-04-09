---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/skills/versions/create
fetched_at: 2026-04-09T03:10:22.306859Z
sha256: 3e91a54c1fa92b907c699bef6be89e61ac19c5fbdee5a24654f03f979fc827e0
---

## Create

`$ ant beta:skills:versions create`

**post** `/v1/skills/{skill_id}/versions`

Create Skill Version

### Parameters

- `--skill-id: string`

  Path param: Unique identifier for the skill.

  The format and length of IDs may change over time.

- `--file: optional array of string`

  Body param: Files to upload for the skill.

  All files must be in the same top-level directory and must include a SKILL.md file at the root of that directory.

- `--beta: optional array of AnthropicBeta`

  Header param: Optional header to specify the beta version(s) you want to use.

### Returns

- `BetaSkillVersionNewResponse: object { id, created_at, description, 5 more }`

  - `id: string`

    Unique identifier for the skill version.

    The format and length of IDs may change over time.

  - `created_at: string`

    ISO 8601 timestamp of when the skill version was created.

  - `description: string`

    Description of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `directory: string`

    Directory name of the skill version.

    This is the top-level directory name that was extracted from the uploaded files.

  - `name: string`

    Human-readable name of the skill version.

    This is extracted from the SKILL.md file in the skill upload.

  - `skill_id: string`

    Identifier for the skill that this version belongs to.

  - `type: string`

    Object type.

    For Skill Versions, this is always `"skill_version"`.

  - `version: string`

    Version identifier for the skill.

    Each version is identified by a Unix epoch timestamp (e.g., "1759178010641129").

### Example

```cli
ant beta:skills:versions create \
  --api-key my-anthropic-api-key \
  --skill-id skill_id
```
