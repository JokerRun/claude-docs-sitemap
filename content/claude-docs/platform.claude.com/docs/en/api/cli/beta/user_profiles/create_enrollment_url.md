---
source: platform
url: https://platform.claude.com/docs/en/api/cli/beta/user_profiles/create_enrollment_url
fetched_at: 2026-04-17T03:11:44.711743Z
sha256: 180a01ff77fb910883cfb1f9b096bc538d12881e3c576cc654f2ba833ab86b52
---

## Create Enrollment URL

`$ ant beta:user-profiles create-enrollment-url`

**post** `/v1/user_profiles/{user_profile_id}/enrollment_url`

Create Enrollment URL

### Parameters

- `--user-profile-id: string`

  Path parameter user_profile_id

- `--beta: optional array of AnthropicBeta`

  Optional header to specify the beta version(s) you want to use.

### Returns

- `beta_user_profile_enrollment_url: object { expires_at, type, url }`

  - `expires_at: string`

    A timestamp in RFC 3339 format

  - `type: "enrollment_url"`

    Object type. Always `enrollment_url`.

    - `"enrollment_url"`

  - `url: string`

    Enrollment URL to send to the end user. Valid until `expires_at`.

### Example

```cli
ant beta:user-profiles create-enrollment-url \
  --api-key my-anthropic-api-key \
  --user-profile-id uprof_011CZkZCu8hGbp5mYRQgUmz9
```
