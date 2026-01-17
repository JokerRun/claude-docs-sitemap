---
source: platform
url: https://platform.claude.com/docs/en/api/admin/workspaces/archive
fetched_at: 2026-01-17T03:25:45.160390Z
sha256: 7d76a38c315bfebec5ae9adaeed62ca549b74cc80e85bcf492bf71d30e5fde75
---

## Archive

**post** `/v1/organizations/workspaces/{workspace_id}/archive`

Archive Workspace

### Path Parameters

- `workspace_id: string`

  ID of the Workspace.

### Returns

- `Workspace = object { id, archived_at, created_at, 3 more }`

  - `id: string`

    ID of the Workspace.

  - `archived_at: string`

    RFC 3339 datetime string indicating when the Workspace was archived, or null if the Workspace is not archived.

  - `created_at: string`

    RFC 3339 datetime string indicating when the Workspace was created.

  - `display_color: string`

    Hex color code representing the Workspace in the Anthropic Console.

  - `name: string`

    Name of the Workspace.

  - `type: "workspace"`

    Object type.

    For Workspaces, this is always `"workspace"`.

    - `"workspace"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/workspaces/$WORKSPACE_ID/archive \
    -X POST \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```
