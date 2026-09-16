---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/artifacts/download
fetched_at: 2026-09-16T02:20:57.252456Z
sha256: a3898666319770c2f6285afd410f6e300ca68c2a98f943a299fd49d6860bb4b6
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

- `"x-api-key": optional string`

## Example

```bash
curl https://api.anthropic.com/v1/compliance/apps/artifacts/$ARTIFACT_VERSION_ID/content \
    -H 'anthropic-version: 2023-06-01' \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```
