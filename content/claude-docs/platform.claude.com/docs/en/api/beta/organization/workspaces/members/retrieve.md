---
source: platform
url: https://platform.claude.com/docs/en/api/beta/organization/workspaces/members/retrieve
fetched_at: 2026-08-27T03:51:55.831897Z
sha256: abbb2bb065480fb7ffd84fc09224e6be87a6b4ccdc5e8a5ea70033daedae72d3
---

# Get Workspace Member

**GET** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Get Workspace Member

## Path parameters

- `workspace_id: string`

  ID of the Workspace.

- `user_id: string`

  ID of the User.

## Returns

- `BetaWorkspaceMember object`

  - `type: "workspace_member"`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    default: workspace_member

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

  - `workspace_role: BetaWorkspaceRole`

    Role of the Workspace Member.

    - `"workspace_admin"`

    - `"workspace_billing"`

    - `"workspace_developer"`

    - `"workspace_restricted_developer"`

    - `"workspace_user"`

## Example

```bash
curl https://api.anthropic.com/v1/organizations/workspaces/$WORKSPACE_ID/members/$USER_ID \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

### Response (200)

```json
{
  "type": "workspace_member",
  "user_id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ",
  "workspace_role": "workspace_admin"
}
```
