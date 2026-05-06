---
source: platform
url: https://platform.claude.com/docs/en/api/typescript/beta/webhooks/unwrap
fetched_at: 2026-05-06T03:14:02.071100Z
sha256: d799dbb21730169caaa6f3053ca2cda1cc52c6080bbbda4c61621f5cea2b9081
---

## Unwrap

`client.beta.webhooks.unwrap(RequestOptionsoptions?): void`

**** ``

### Example

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env['ANTHROPIC_API_KEY'], // This is the default and can be omitted
});

await client.beta.webhooks.unwrap();
```
