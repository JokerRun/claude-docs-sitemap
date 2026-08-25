---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/projects/documents/retrieve
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: f318795dcac14b96e5f7a83fbada57ebf52000c8b23c0ab964201f6c06d23304
---

# Get project document content

**GET** `/v1/compliance/apps/projects/documents/{document_id}`

Get detailed information for a specific project document.

## Path parameters

- `document_id: string`

  The document ID (tagged ID, e.g., claude_proj_doc_abc123)

## Headers

- `"x-api-key": optional string`

## Returns

- `id: string`

  Project document identifier (tagged ID)

- `content: string`

  Document text content

- `created_at: string`

  Document creation timestamp

  format: date-time

- `filename: string`

  Document filename

- `user: object or null`

  The user who created a project or project document.

  Fields that reference this type are null when the creator's account has
  been deleted or the creator is no longer a member of an organization the
  key may read.

  - `id: string`

    User identifier (tagged ID)

  - `email_address: string`

    User's email address

## Example

```bash
curl https://api.anthropic.com/v1/compliance/apps/projects/documents/$DOCUMENT_ID \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```

### Response (200)

```json
{
  "id": "claude_proj_doc_01Qr8StUvWxYzAbCdEfGhJjK",
  "content": "# Design notes\n\n- Item one\n- Item two\n",
  "created_at": "2025-03-12T18:22:41.123456Z",
  "filename": "design-notes.txt",
  "user": {
    "id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
    "email_address": "jane.doe@example.com"
  }
}
```
