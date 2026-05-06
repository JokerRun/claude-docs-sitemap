---
source: platform
url: https://platform.claude.com/docs/en/api/python/beta/webhooks/unwrap
fetched_at: 2026-05-06T03:14:02.071100Z
sha256: 4e94e3db34ec82e1a6dda9d88a26005f32055be914528135faf19280c9df8b78
---

## Unwrap

`beta.webhooks.unwrap()`

**** ``

### Example

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),  # This is the default and can be omitted
)
client.beta.webhooks.unwrap()
```
