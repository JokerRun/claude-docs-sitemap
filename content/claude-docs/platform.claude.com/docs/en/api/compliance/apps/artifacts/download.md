---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/artifacts/download
fetched_at: 2026-10-13T02:33:54.812386Z
sha256: afd9b79cdeffbfefbc0ab8fce60f1385d7f07805ea09f70107bfb190f46fa4d5
---

---
title: Download artifact content
url: https://platform.claude.com/docs/en/api/compliance/apps/artifacts/download
---

# Download artifact content

**GET** `/v1/compliance/apps/artifacts/{artifact_version_id}/content`

Download the content of an artifact version for compliance purposes.

Returns the full text content of the artifact version.

## Path parameters

- `artifact_version_id: string`

  The artifact version ID (tagged ID, e.g., claude_artifact_version_abc123)

## Headers

- `"anthropic-version": optional string`

  The version of the Claude API you want to use.

  Read more about versioning and our version history [here](https://platform.claude.com/docs/en/api/versioning?sdk_languages=http).

- `"x-api-key": optional string`

## Example

```bash
curl https://api.anthropic.com/v1/compliance/apps/artifacts/$ARTIFACT_VERSION_ID/content \
    -H 'anthropic-version: 2023-06-01' \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```
