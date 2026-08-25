---
source: platform
url: https://platform.claude.com/docs/en/api/admin/rbac_groups/delete
fetched_at: 2026-08-25T02:28:41.066498Z
sha256: 086e0c7e2bd62c6ab93f6f2a26a54644e8a6346b8360389752598d325d930531
---

# Delete RBAC Group

**DELETE** `/v1/organizations/rbac_groups/{group_id}`

Delete an RBAC Group. Groups provisioned by an identity provider (source type `"scim"`) cannot be deleted via the API.

The RBAC Groups API is in beta and available to Claude Enterprise organizations only. Requests must send the `ce-user-management-2026-07-13` value in the `anthropic-beta` header.

## Path parameters

- `group_id: string`

  ID of the RBAC Group.

## Headers

- `"anthropic-beta": optional array of string`

  Optional header to specify the beta version(s) you want to use.

  To use multiple betas, use a comma separated list like `beta1,beta2` or specify the header multiple times for each beta.

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
    -H "Authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

### Response (200)

```json
{
  "id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "type": "rbac_group_deleted"
}
```
