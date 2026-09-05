---
source: platform
url: https://platform.claude.com/docs/en/api/admin/rbac_groups/delete
fetched_at: 2026-09-05T02:20:11.001334Z
sha256: c4384420cb7ab2a26c02a86f9a36784c3d5b40c8c1e427920b15646f0455ac26
---

# Delete RBAC Group

**DELETE** `/v1/organizations/rbac_groups/{group_id}`

Delete an RBAC Group. Groups provisioned by an identity provider (source type `"scim"`) cannot be deleted via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

## Path parameters

- `group_id: string`

  ID of the RBAC Group.

## Returns

- `RbacGroupDeleted object`

  - `id: string`

    ID of the RBAC Group.

  - `type: "rbac_group_deleted"`

    Deleted object type.

    For RBAC Groups, this is always `"rbac_group_deleted"`.

    default: rbac_group_deleted

## Example

```bash
curl https://api.anthropic.com/v1/organizations/rbac_groups/$GROUP_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN"
```

### Response (200)

```json
{
  "id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "type": "rbac_group_deleted"
}
```
