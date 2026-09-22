---
source: platform
url: https://platform.claude.com/docs/en/api/beta/organization/rbac_groups/delete
fetched_at: 2026-09-22T02:21:41.260167Z
sha256: 9ed63cbff0d94b8b5b5b85a3cb276bab436695a7f4da48d73c2836cdc40104b6
---

---
title: Delete RBAC Group
url: https://platform.claude.com/docs/en/api/beta/organization/rbac_groups/delete
---

# Delete RBAC Group

**DELETE** `/v1/organizations/rbac_groups/{rbac_group_id}`

Delete an RBAC Group. Groups provisioned by an identity provider (source type `"scim"`) cannot be deleted via the API while an organization in the tenant uses SCIM provisioning.

The RBAC Groups API is available to Claude Enterprise organizations only.

## Path parameters

- `rbac_group_id: string`

  ID of the RBAC Group.

## Returns

- `BetaRBACGroupDeleted object`

  - `type: "rbac_group_deleted"`

    Deleted object type.

    For RBAC Groups, this is always `"rbac_group_deleted"`.

    default: rbac_group_deleted

  - `id: string`

    ID of the RBAC Group.

## Example

```bash
curl https://api.anthropic.com/v1/organizations/rbac_groups/$RBAC_GROUP_ID \
    -X DELETE \
    -H 'anthropic-version: 2023-06-01' \
    -H "X-Api-Key: $ANTHROPIC_API_KEY"
```

### Response (200)

```json
{
  "id": "rbac_group_012rppKaSVsmTo6NqRDXQXNF",
  "type": "rbac_group_deleted"
}
```
