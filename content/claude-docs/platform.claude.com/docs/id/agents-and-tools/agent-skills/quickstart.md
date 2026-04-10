---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/agent-skills/quickstart
fetched_at: 2026-04-10T03:11:42.436400Z
sha256: 7e8ebd722594c0c5f6c0d6ce24f9ff02c70ddc423f08fd44d103134b261020ae
---

# Mulai menggunakan Agent Skills di API

Pelajari cara menggunakan Agent Skills untuk membuat dokumen dengan Claude API dalam waktu kurang dari 10 menit.

---

Tutorial ini menunjukkan cara menggunakan Agent Skills untuk membuat presentasi PowerPoint. Anda akan mempelajari cara mengaktifkan Skills, membuat permintaan sederhana, dan mengakses file yang dihasilkan.

## Prasyarat

- [Kunci API Claude](/settings/keys)
- Python 3.7+ atau curl yang terinstal
- Pemahaman dasar tentang cara membuat permintaan API

## Ikhtisar Agent Skills

Agent Skills bawaan memperluas kemampuan Claude dengan keahlian khusus untuk tugas-tugas seperti membuat dokumen, menganalisis data, dan memproses file. Anthropic menyediakan Agent Skills bawaan berikut di API:

- **PowerPoint (pptx):** Membuat dan mengedit presentasi
- **Excel (xlsx):** Membuat dan menganalisis spreadsheet
- **Word (docx):** Membuat dan mengedit dokumen
- **PDF (pdf):** Menghasilkan dokumen PDF

<Note>
**Ingin membuat Skills kustom?** Lihat [Agent Skills Cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction) untuk contoh membangun Skills Anda sendiri dengan keahlian domain-spesifik.
</Note>

## Langkah 1: Daftar Skills yang tersedia

Pertama, periksa Skills apa yang tersedia. Gunakan Skills API untuk mendaftar semua Skills yang dikelola Anthropic:

<CodeGroup defaultLanguage="CLI">
```bash Shell
curl "https://api.anthropic.com/v1/skills?source=anthropic" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: skills-2025-10-02"
```

```bash CLI
ant beta:skills list --source anthropic
```

```python Python
import anthropic

client = anthropic.Anthropic()

# Daftar Skills yang dikelola Anthropic
skills = client.beta.skills.list(source="anthropic", betas=["skills-2025-10-02"])

for skill in skills.data:
    print(f"{skill.id}: {skill.display_title}")
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

// Daftar Skills yang dikelola Anthropic
const skills = await client.beta.skills.list({
  source: "anthropic",
  betas: ["skills-2025-10-02"]
});

for (const skill of skills.data) {
  console.log(`${skill.id}: ${skill.display_title}`);
}
```
</CodeGroup>

Anda akan melihat Skills berikut: `pptx`, `xlsx`, `docx`, dan `pdf`.

API ini mengembalikan metadata setiap Skill: nama dan deskripsinya. Claude memuat metadata ini saat startup untuk mengetahui Skills apa yang tersedia. Ini adalah tingkat pertama dari **progressive disclosure**, di mana Claude menemukan Skills tanpa memuat instruksi lengkapnya terlebih dahulu.

## Langkah 2: Buat presentasi

Sekarang gunakan PowerPoint Skill untuk membuat presentasi tentang energi terbarukan. Tentukan Skills menggunakan parameter `container` di Messages API:

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 4096,
    "container": {
      "skills": [
        {
          "type": "anthropic",
          "skill_id": "pptx",
          "version": "latest"
        }
      ]
    },
    "messages": [{
      "role": "user",
      "content": "Create a presentation about renewable energy with 5 slides"
    }],
    "tools": [{
      "type": "code_execution_20250825",
      "name": "code_execution"
    }]
  }'
```

```bash CLI
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 \
  --transform content <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
container:
  skills:
    - type: anthropic
      skill_id: pptx
      version: latest
messages:
  - role: user
    content: Create a presentation about renewable energy with 5 slides
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
```

```python Python
import anthropic

client = anthropic.Anthropic()

# Buat pesan dengan PowerPoint Skill
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]
    },
    messages=[
        {
            "role": "user",
            "content": "Create a presentation about renewable energy with 5 slides",
        }
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)

print(response.content)
```

```typescript TypeScript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

// Buat pesan dengan PowerPoint Skill
const response = await client.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      {
        type: "anthropic",
        skill_id: "pptx",
        version: "latest"
      }
    ]
  },
  messages: [
    {
      role: "user",
      content: "Create a presentation about renewable energy with 5 slides"
    }
  ],
  tools: [
    {
      type: "code_execution_20250825",
      name: "code_execution"
    }
  ]
});

console.log(response.content);
```
</CodeGroup>

Mari kita uraikan apa yang dilakukan setiap bagian:

- **`container.skills`:** Menentukan Skills mana yang dapat digunakan Claude
- **`type: "anthropic"`:** Menunjukkan bahwa ini adalah Skill yang dikelola Anthropic
- **`skill_id: "pptx"`:** Pengenal PowerPoint Skill
- **`version: "latest"`:** Versi Skill yang diatur ke yang paling baru diterbitkan
- **`tools`:** Mengaktifkan eksekusi kode (diperlukan untuk Skills)
- **Header Beta:** `code-execution-2025-08-25` dan `skills-2025-10-02`

Saat Anda membuat permintaan ini, Claude secara otomatis mencocokkan tugas Anda dengan Skill yang relevan. Karena Anda meminta presentasi, Claude menentukan bahwa PowerPoint Skill relevan dan memuat instruksi lengkapnya: tingkat kedua dari progressive disclosure. Kemudian Claude mengeksekusi kode Skill untuk membuat presentasi Anda.

## Langkah 3: Unduh file yang dibuat

Presentasi dibuat di container eksekusi kode dan disimpan sebagai file. Respons menyertakan referensi file dengan ID file. Ekstrak ID file dan unduh menggunakan Files API:

<CodeGroup>

```bash Shell nocheck
# Ekstrak file_id dari respons (menggunakan jq)
FILE_ID=$(echo "$RESPONSE" | jq -r '.content[] | select(.type=="tool_use" and .name=="code_execution") | .content[] | select(.file_id) | .file_id')

# Unduh file
curl "https://api.anthropic.com/v1/files/$FILE_ID/content" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  --output renewable_energy.pptx

echo "Presentasi disimpan ke renewable_energy.pptx"
```

```bash CLI
# Ekstrak file_id dengan --transform pada panggilan messages create
FILE_ID=$(ant beta:messages create \
  --beta code-execution-2025-08-25 --beta skills-2025-10-02 \
  --transform 'content.#.content.content.#.file_id|@flatten|0' \
  --format yaml <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
container:
  skills:
    - type: anthropic
      skill_id: pptx
      version: latest
messages:
  - role: user
    content: Create a presentation about renewable energy with 5 slides
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
)

# Unduh file
ant beta:files download \
  --file-id "$FILE_ID" \
  --output renewable_energy.pptx

printf 'Presentasi disimpan ke renewable_energy.pptx\n'
```

```python Python nocheck
from typing import Any

response: Any = None
# Ekstrak ID file dari respons
file_id = None
for block in response.content:
    if block.type == "tool_use" and block.name == "code_execution":
        # ID file ada di hasil tool
        for result_block in block.content:
            if hasattr(result_block, "file_id"):
                file_id = result_block.file_id
                break

if file_id:
    # Unduh file
    file_content = client.beta.files.download(
        file_id=file_id, betas=["files-api-2025-04-14"]
    )

    # Simpan ke disk
    with open("renewable_energy.pptx", "wb") as f:
        file_content.write_to_file(f.name)

    print(f"Presentasi disimpan ke renewable_energy.pptx")
```

```typescript TypeScript nocheck
// Ekstrak ID file dari respons
let fileId: string | null = null;
for (const block of response.content) {
  if (block.type === "tool_use" && block.name === "code_execution") {
    // ID file ada di hasil tool
    for (const resultBlock of block.content) {
      if ("file_id" in resultBlock) {
        fileId = resultBlock.file_id;
        break;
      }
    }
  }
}

if (fileId) {
  // Unduh file
  const fileContent = await client.beta.files.download(fileId, {
    betas: ["files-api-2025-04-14"]
  });

  // Simpan ke disk
  const fs = require("fs/promises");
  await fs.writeFile("renewable_energy.pptx", Buffer.from(await fileContent.arrayBuffer()));

  console.log("Presentasi disimpan ke renewable_energy.pptx");
}
```
</CodeGroup>

<Note>
Untuk detail lengkap tentang bekerja dengan file yang dihasilkan, lihat [dokumentasi code execution tool](/docs/id/agents-and-tools/tool-use/code-execution-tool#retrieve-generated-files).
</Note>

## Coba lebih banyak contoh

Sekarang setelah Anda membuat dokumen pertama dengan Skills, coba variasi berikut:

### Buat spreadsheet

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 4096,
    "container": {
      "skills": [
        {
          "type": "anthropic",
          "skill_id": "xlsx",
          "version": "latest"
        }
      ]
    },
    "messages": [{
      "role": "user",
      "content": "Create a quarterly sales tracking spreadsheet with sample data"
    }],
    "tools": [{
      "type": "code_execution_20250825",
      "name": "code_execution"
    }]
  }'
```

```bash CLI
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
container:
  skills:
    - type: anthropic
      skill_id: xlsx
      version: latest
messages:
  - role: user
    content: Create a quarterly sales tracking spreadsheet with sample data
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
```

```python Python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
    },
    messages=[
        {
            "role": "user",
            "content": "Create a quarterly sales tracking spreadsheet with sample data",
        }
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript
const response = await client.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      {
        type: "anthropic",
        skill_id: "xlsx",
        version: "latest"
      }
    ]
  },
  messages: [
    {
      role: "user",
      content: "Create a quarterly sales tracking spreadsheet with sample data"
    }
  ],
  tools: [
    {
      type: "code_execution_20250825",
      name: "code_execution"
    }
  ]
});
```
</CodeGroup>

### Buat dokumen Word

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 4096,
    "container": {
      "skills": [
        {
          "type": "anthropic",
          "skill_id": "docx",
          "version": "latest"
        }
      ]
    },
    "messages": [{
      "role": "user",
      "content": "Write a 2-page report on the benefits of renewable energy"
    }],
    "tools": [{
      "type": "code_execution_20250825",
      "name": "code_execution"
    }]
  }'
```

```bash CLI
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
container:
  skills:
    - type: anthropic
      skill_id: docx
      version: latest
messages:
  - role: user
    content: Write a 2-page report on the benefits of renewable energy
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
```

```python Python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [{"type": "anthropic", "skill_id": "docx", "version": "latest"}]
    },
    messages=[
        {
            "role": "user",
            "content": "Write a 2-page report on the benefits of renewable energy",
        }
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript
const response = await client.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      {
        type: "anthropic",
        skill_id: "docx",
        version: "latest"
      }
    ]
  },
  messages: [
    {
      role: "user",
      content: "Write a 2-page report on the benefits of renewable energy"
    }
  ],
  tools: [
    {
      type: "code_execution_20250825",
      name: "code_execution"
    }
  ]
});
```
</CodeGroup>

### Hasilkan PDF

<CodeGroup>
```bash Shell
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: code-execution-2025-08-25,skills-2025-10-02" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 4096,
    "container": {
      "skills": [
        {
          "type": "anthropic",
          "skill_id": "pdf",
          "version": "latest"
        }
      ]
    },
    "messages": [{
      "role": "user",
      "content": "Generate a PDF invoice template"
    }],
    "tools": [{
      "type": "code_execution_20250825",
      "name": "code_execution"
    }]
  }'
```

```bash CLI
ant beta:messages create \
  --beta code-execution-2025-08-25 \
  --beta skills-2025-10-02 <<'YAML'
model: claude-opus-4-6
max_tokens: 4096
container:
  skills:
    - type: anthropic
      skill_id: pdf
      version: latest
messages:
  - role: user
    content: Generate a PDF invoice template
tools:
  - type: code_execution_20250825
    name: code_execution
YAML
```

```python Python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [{"type": "anthropic", "skill_id": "pdf", "version": "latest"}]
    },
    messages=[{"role": "user", "content": "Generate a PDF invoice template"}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

```typescript TypeScript
const response = await client.beta.messages.create({
  model: "claude-opus-4-6",
  max_tokens: 4096,
  betas: ["code-execution-2025-08-25", "skills-2025-10-02"],
  container: {
    skills: [
      {
        type: "anthropic",
        skill_id: "pdf",
        version: "latest"
      }
    ]
  },
  messages: [
    {
      role: "user",
      content: "Generate a PDF invoice template"
    }
  ],
  tools: [
    {
      type: "code_execution_20250825",
      name: "code_execution"
    }
  ]
});
```
</CodeGroup>

## Langkah selanjutnya

Sekarang setelah Anda menggunakan Agent Skills bawaan, Anda dapat:

<CardGroup cols={2}>
  <Card
    title="Panduan API"
    icon="book"
    href="/docs/id/build-with-claude/skills-guide"
  >
    Gunakan Skills dengan Claude API
  </Card>
  <Card
    title="Buat Skills Kustom"
    icon="code"
    href="/docs/id/api/skills/create-skill"
  >
    Unggah Skills Anda sendiri untuk tugas-tugas khusus
  </Card>
  <Card
    title="Panduan Penulisan"
    icon="edit"
    href="/docs/id/agents-and-tools/agent-skills/best-practices"
  >
    Pelajari praktik terbaik untuk menulis Skills yang efektif
  </Card>
  <Card
    title="Gunakan Skills di Claude Code"
    icon="terminal"
    href="https://code.claude.com/docs/en/skills"
  >
    Pelajari tentang Skills di Claude Code
  </Card>
  <Card
    title="Agent Skills Cookbook"
    icon="book"
    href="https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction"
  >
    Jelajahi contoh Skills dan pola implementasi
  </Card>
</CardGroup>