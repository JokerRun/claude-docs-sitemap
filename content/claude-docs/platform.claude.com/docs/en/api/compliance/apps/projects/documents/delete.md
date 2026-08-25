---
source: platform
url: https://platform.claude.com/docs/en/api/compliance/apps/projects/documents/delete
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 95ec3b45fe3ccd5e442dbd6a60bc31151ccc5e3ee68f0d45393370a852469117
---

# Delete project document

**DELETE** `/v1/compliance/apps/projects/documents/{document_id}`

Delete a project document for compliance purposes.

Hard-deletes the project document permanently.

## Path parameters

- `document_id: string`

  The document ID (tagged ID, e.g., claude_proj_doc_abc123)

## Headers

- `"x-api-key": optional string`

## Returns

- `id: string`

  The ID of the project document that was deleted

- `type: "claude_project_document_deleted"`

  Constant string confirming deletion.

  default: claude_project_document_deleted

## Example

```bash
curl https://api.anthropic.com/v1/compliance/apps/projects/documents/$DOCUMENT_ID \
    -X DELETE \
    -H "Authorization: Bearer $ANTHROPIC_COMPLIANCE_API_KEY"
```

### Response (200)

```json
{
  "id": "id",
  "type": "claude_project_document_deleted"
}
```
