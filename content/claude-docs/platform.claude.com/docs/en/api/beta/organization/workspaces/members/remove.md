---
source: platform
url: https://platform.claude.com/docs/en/api/beta/organization/workspaces/members/remove
fetched_at: 2026-10-31T02:12:10.366891Z
sha256: ee1c95688e962248ab950b45dae545e3a1a2465aaa3336c356aa6dd8ccb6eb39
---

---
title: Delete Workspace Member
url: https://platform.claude.com/docs/en/api/beta/organization/workspaces/members/remove
---

# Delete Workspace Member

**DELETE** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Delete Workspace Member

## Path parameters

- `workspace_id: string`

  ID of the Workspace.

- `user_id: string`

  ID of the User.

## Headers

- `"anthropic-version": optional string`

  The version of the Claude API you want to use.

  Read more about versioning and our version history [here](https://platform.claude.com/docs/en/api/versioning?sdk_languages=http).

## Returns

- `type: "workspace_member_deleted"`

  Deleted object type.

  For Workspace Members, this is always `"workspace_member_deleted"`.

  default: workspace_member_deleted

- `user_id: string`

  ID of the User.

- `workspace_id: string`

  ID of the Workspace.

## Example

```bash
curl https://api.anthropic.com/v1/organizations/workspaces/$WORKSPACE_ID/members/$USER_ID \
    -X DELETE \
    -H 'anthropic-version: 2026-10-21' \
    -H "Authorization: Bearer $ANTHROPIC_API_KEY"
```

### Response (200)

```json
{
  "type": "workspace_member_deleted",
  "user_id": "user_01WxYzAbCdEfGhJkMnPqRsTu",
  "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
}
```
