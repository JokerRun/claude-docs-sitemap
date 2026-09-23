---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/apply
fetched_at: 2026-09-23T02:21:59.104890Z
sha256: aef06da86118525ddbc63d10380899541aad76680be73a71e6b6cea2b801c5dc
---

---
title: Kelola sumber daya sebagai kode dengan ant apply
url: https://platform.claude.com/docs/id/cli-sdks-libraries/cli/apply
description: Deklarasikan agen, lingkungan, skill, penyimpanan memori, dan deployment sebagai berkas di repositori Anda, lalu jaga agar sumber daya API tetap sinkron dengan berkas tersebut menggunakan ant apply.
---

`ant apply` membuat dan memperbarui sumber daya Claude API dari berkas, yaitu agen, lingkungan, skill, penyimpanan memori, dan deployment. Berkas-berkas ini disimpan di repositori Anda dan perubahannya melewati proses peninjauan yang sama dengan kode Anda. Anda mendeskripsikan setiap sumber daya dalam sebuah berkas, menjalankan `ant apply`, lalu menyetujui "plan" (rencana) yang ditampilkannya. Setelah itu, Anda melakukan commit pada `claude-lock.json` yang ditulisnya agar eksekusi berikutnya memperbarui sumber daya yang sama, bukan membuat sumber daya baru.

Untuk menginstal dan mengautentikasi CLI, lihat [panduan memulai cepat CLI](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/quickstart). `ant apply` memerlukan CLI versi 1.30.0 atau yang lebih baru.

## Terapkan agen pertama Anda

Tulis agen sebagai berkas Markdown di bawah `agents/`, lalu terapkan:

<MultiFileExample language="cli" label="CLI">
  ```bash CLI
  ant apply agents/summarizer.md
  ```

  <File filename="agents/summarizer.md">
    ```markdown
    ---
    name: Summarizer
    model: claude-opus-5-5
    tools:
      - type: agent_toolset_20260401
    ---

    You are a helpful assistant that writes concise summaries.
    ```
  </File>
</MultiFileExample>

Frontmatter berisi konfigurasi agen (bidang-bidang dari [Definisikan agen Anda](https://platform.claude.com/docs/id/managed-agents/agent-setup)), sedangkan isi berkas menjadi prompt sistem agen tersebut. `ant apply` [menyimpulkan](https://platform.claude.com/docs/id/cli-sdks-libraries/cli/apply#kind-inference) bahwa berkas tersebut adalah agen berdasarkan path-nya, dalam hal ini direktori `agents/`.

Di terminal interaktif, `ant apply` mencetak rencana dan menunggu persetujuan Anda:

```text Output wrap
First apply  ./claude-lock.json does not exist yet and will be created

Resources will be created with
  credentials   API key (--api-key / ANTHROPIC_API_KEY)
  host          api.anthropic.com
  organization  1b0c2a4d-6c1f-4f0e-9a57-2e8d1c3b4a5f
  workspace     wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ

Preview  ./claude-lock.json (new)

± Name                    Plan
+ ./agents/summarizer.md  create

Resources  + 1 to create

Apply these changes? (y)es / (n)o / (d)etails y

Apply  ./claude-lock.json

± Name                    Status
+ ./agents/summarizer.md  created    agent_011CYm1BLqPXpQRk5khsSXrs

Resources  + 1 created

State written to ./claude-lock.json
```

Jawab `d` untuk melihat detailnya terlebih dahulu, yaitu bidang-bidang setiap sumber daya baru atau diff per bidang untuk setiap pembaruan. `--dry-run` mencetak rencana terperinci tersebut lalu keluar tanpa mengubah apa pun.

Untuk mengubah agen, edit berkasnya dan jalankan `ant apply` lagi. Kali ini rencana akan menampilkan pembaruan, bukan pembuatan.

## Commit claude-lock.json

Eksekusi `ant apply` pertama menulis `claude-lock.json`, yaitu "lockfile" (berkas kunci), di direktori tempat Anda menjalankannya. Karena itu, jalankan perintah ini dari root repositori. Lockfile mencatat ID sumber daya yang dibuat oleh setiap berkas, serta organisasi dan workspace tempat sumber daya tersebut berada:

```json claude-lock.json
{
  "version": 1,
  "origin": {
    "base_url": "https://api.anthropic.com",
    "organization_id": "1b0c2a4d-6c1f-4f0e-9a57-2e8d1c3b4a5f",
    "workspace_id": "wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ"
  },
  "resources": {
    "./agents/summarizer.md": {
      "kind": "agent",
      "id": "agent_011CYm1BLqPXpQRk5khsSXrs",
      "version": "1",
      "hash": "d23251c8d99b3613a64f3f8d87f5fad4",
      "remote_hash": "1b771bee5bdbf600a5ad972fdac32d94"
    }
  }
}
```

Commit lockfile bersama berkas-berkas Anda. Dengan lockfile inilah eksekusi berikutnya, baik di mesin Anda maupun di CI, menemukan sumber daya tersebut alih-alih membuatnya lagi. Lockfile juga menjadi tempat Anda membaca ID agen untuk [memulai sesi](https://platform.claude.com/docs/id/managed-agents/sessions). Kedua hash di dalamnya merupakan sidik jari dari apa yang terakhir dikirim dan apa yang dikembalikan oleh API. Dari situlah eksekusi berikutnya dapat mendeteksi berkas yang telah diedit, atau sumber daya yang diubah di luar berkas-berkas ini.

## Kembangkan menjadi sebuah proyek

Anda juga dapat mendefinisikan sumber daya lainnya secara deklaratif sebagai berkas. Sebuah berkas berisi body permintaan yang akan Anda kirim ke endpoint pembuatan untuk jenis sumber daya tersebut:

* [Lingkungan](https://platform.claude.com/docs/id/managed-agents/environments) adalah berkas YAML di `environments/`.
* [Penyimpanan memori](https://platform.claude.com/docs/id/managed-agents/memory) adalah berkas YAML di `memory_stores/`.
* [Deployment](https://platform.claude.com/docs/id/managed-agents/scheduled-deployments) adalah berkas Markdown di `deployments/`. Frontmatter-nya menjadi body permintaan, sedangkan teks prosanya menjadi pesan yang memulai setiap sesi.
* [Skill](https://platform.claude.com/docs/id/managed-agents/skills) adalah direktori dengan `SKILL.md` di root-nya, yang lazimnya berada di bawah `skills/` dan diunggah sebagai satu bundel.

Semua sumber daya kecuali skill dapat ditulis sebagai YAML, JSON, atau Markdown. Dalam Markdown, frontmatter menjadi body, sedangkan teks prosa mengisi bidang teks milik jenis sumber daya tersebut: `system` untuk agen, `description` untuk lingkungan atau penyimpanan memori, dan pesan pertama untuk deployment.

Sumber daya saling merujuk melalui path. Di mana pun API mengharapkan ID sumber daya lain, tuliskan path relatif ke berkas sumber daya tersebut. Dalam proyek ini, agen reviewer mencantumkan `../skills/pr-summary` di bawah `skills`, agen lead mencantumkan `./reviewer.md` dalam daftar anggotanya, dan deployment menyebut agen, lingkungan, serta penyimpanan memorinya melalui path. `ant apply` membuat semuanya sesuai urutan dependensi dan mengisi ID yang sebenarnya. Proyek ini terdiri dari enam berkas:

<MultiFileExample variant="explorer">
  <File filename="agents/reviewer.md">
    ```markdown
    ---
    name: Code reviewer
    model: claude-opus-5-5
    tools:
      - type: agent_toolset_20260401
    skills:
      - ../skills/pr-summary
    ---

    You review pull requests for correctness, security, and readability.
    ```
  </File>

  <File filename="agents/lead.md">
    ```markdown
    ---
    name: Engineering lead
    model: claude-opus-5-5
    multiagent:
      type: coordinator
      agents:
        - ./reviewer.md
    ---

    You coordinate engineering work. Delegate code review to the reviewer.
    ```
  </File>

  <File filename="skills/pr-summary/SKILL.md">
    ```markdown
    ---
    name: pr-summary
    description: Summarize a pull request's changes and risks in the team's review format.
    ---

    # PR summary

    List what changed, why, and anything a reviewer should look at closely, in three short sections.
    ```
  </File>

  <File filename="environments/cloud.yaml">
    ```yaml
    name: review-env
    description: Cloud container with unrestricted networking for review sessions.
    config:
      type: cloud
      networking:
        type: unrestricted
    ```
  </File>

  <File filename="memory_stores/review-notes.yaml">
    ```yaml
    name: Review notes
    description: Recurring issues and house-style decisions the reviewer has recorded between runs.
    ```
  </File>

  <File filename="deployments/nightly.md">
    ```markdown
    ---
    name: Nightly review
    agent: ../agents/reviewer.md # the API's agent field: sent as {type: agent, id, version}
    environment_id: ../environments/cloud.yaml # sent as the environment's ID
    resources:
      - path: ../memory_stores/review-notes.yaml
        access: read_write
    schedule:
      type: cron
      expression: "0 3 * * *"
      timezone: America/Los_Angeles
    ---

    Review any open pull requests. Start with the oldest.
    ```
  </File>
</MultiFileExample>

Terapkan seluruh direktori:

```bash CLI
ant apply .
```

Setelah itu, `claude-lock.json` memiliki entri untuk setiap berkas dalam proyek.

Path relatif adalah cara berkas-berkas ini saling menunjuk. `ant apply` mengunci referensi agen dan skill ke versi yang baru saja diterapkannya. Dengan begitu, mengedit `reviewer.md` atau skill tersebut akan memperbarui semua yang mereferensikannya dalam eksekusi yang sama. Path juga dapat digunakan di dalam objek, seperti pada entri `resources` milik deployment, dan kunci lainnya seperti `access` tetap dipertahankan.

Untuk menunjuk sumber daya yang tidak dikelola oleh berkas-berkas ini, tuliskan ID-nya (`agent_...`, `skill_...`). Nilai lainnya, seperti `{type: anthropic, skill_id: xlsx}`, dikirim ke API apa adanya. Referensi skill juga dapat berupa URL GitHub dengan format `https://github.com/<owner>/<repo>/tree/<branch>/<dir>`, misalnya sebuah direktori di [repositori skill](https://github.com/anthropics/skills) open-source milik Anthropic. `ant apply` mengunduh lalu mengunggah direktori tersebut, dan menguncinya ke commit yang telah di-resolve hingga Anda menjalankan perintah dengan `--upgrade` (atur `GITHUB_TOKEN` untuk repositori privat).

### Cara ant apply menyimpulkan jenis berkas

Saat menelusuri sebuah direktori, `ant apply` menentukan jenis setiap berkas berdasarkan kriteria pertama yang cocok dari daftar berikut:

1. Bidang `type` di tingkat teratas dalam berkas.
2. Direktori yang langsung menampung berkas tersebut: `agents/`, `environments/`, `memory_stores/`, atau `deployments/`.
3. Nama berkas yang diawali dengan nama jenisnya, seperti `environment_staging.md`.

Berkas yang tidak cocok dengan kriteria mana pun, seperti README dan konfigurasi CI, akan dilewati kecuali Anda menyebutkannya di baris perintah. Berkas Markdown yang disebutkan secara eksplisit tetapi tidak cocok dengan kriteria mana pun diperlakukan sebagai agen. Sebaliknya, berkas YAML atau JSON yang disebutkan secara eksplisit tetapi tidak cocok akan menghasilkan error.

## Edit dan terapkan ulang

Menjalankan `ant apply` tanpa argumen akan merekonsiliasi setiap berkas yang dilacak oleh lockfile. Di terminal, perintah ini juga mencantumkan berkas sumber daya yang belum dilacak di bawah direktori lockfile dan menawarkan untuk menambahkannya. Menghapus sebuah bidang dari berkas akan mengosongkan bidang tersebut pada sumber daya, asalkan API mengizinkan bidang itu dikosongkan. Bidang yang tidak pernah Anda atur, atau yang tidak dapat dikosongkan oleh API, tetap mempertahankan nilainya saat ini.

Jika sebuah sumber daya diedit, diarsipkan, atau dihapus di luar berkas-berkas ini (misalnya di Claude Console), rencana akan diakhiri dengan `This plan cannot be applied:` beserta alasannya. Perintah kemudian keluar dengan `refusing to apply`. Gunakan `--force` untuk menimpa perubahan tersebut atau membuat sumber daya pengganti.

Menghapus sebuah berkas tidak menghapus sumber dayanya, tetapi memunculkan peringatan. Untuk menghapus sumber daya tersebut, gunakan `--prune` (sumber daya akan diarsipkan, atau dihapus jika berupa skill). Karena itu, mengganti nama berkas sama dengan mendeklarasikan sumber daya baru, sementara sumber daya lama tetap ada hingga Anda melakukan prune.

`ant apply` tidak dapat mengambil alih sumber daya yang Anda buat di Console atau dengan `ant beta:agents create`. Hanya sumber daya yang tercatat di lockfile yang dikelola, sehingga menerapkan berkas yang mendeskripsikan agen yang sudah ada akan membuat agen kedua. Jika Anda mengunduh agen dari Console dengan **Export as code**, unduhan tersebut sudah menyertakan `claude-lock.json` sendiri, sehingga menerapkannya akan memperbarui sumber daya yang Anda buat di sana.

## Jalankan ant apply di CI

Tanpa terminal, `ant apply` mencetak rencana lalu berhenti dengan pesan `cannot ask for confirmation without a terminal; re-run with --yes to apply, or --dry-run to see the plan only`. Siapkan CI sebagai berikut:

* Jalankan `ant apply --yes .` di branch default Anda setelah merge, dengan menyebutkan direktori proyek. Perintah `ant apply --yes` tanpa argumen hanya merekonsiliasi berkas yang sudah dilacak oleh lockfile dan melewati berkas yang baru ditambahkan.
* Pada pull request, jalankan `ant apply --dry-run .` untuk mencetak rencana bagi peninjau. Perintah ini hanya bersifat informatif dan tetap keluar dengan kode 0 meskipun rencananya terblokir.
* Commit `claude-lock.json` yang telah diperbarui di akhir job, bahkan jika langkah apply gagal di tengah jalan, karena apply yang hanya berjalan sebagian tetap mencatat sumber daya yang telah dibuatnya.
* Jalankan hanya satu apply dalam satu waktu, karena tidak ada mekanisme yang mengunci lockfile.
* Lakukan autentikasi dengan [Workload Identity Federation](https://platform.claude.com/docs/id/manage-claude/workload-identity-federation), bukan dengan kunci API yang disimpan, menggunakan identitas yang memiliki akses ke organisasi dan workspace yang tercatat di `claude-lock.json`. `ant apply` menolak kredensial yang mengarah ke organisasi atau workspace lain.

Untuk workflow GitHub Actions yang lengkap, lihat [contoh CI di README CLI](https://github.com/anthropics/anthropic-cli#in-ci).

## Flag

| Flag                 | Efek                                                                                                                                                                                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--dry-run`          | Mencetak rencana lalu keluar tanpa menerapkan perubahan atau menulis lockfile. Tetap keluar dengan kode 0 meskipun rencananya terblokir.                                                                                                                     |
| `--yes`              | Menerapkan perubahan tanpa meminta konfirmasi. Wajib digunakan jika tidak ada terminal.                                                                                                                                                                      |
| `--force`            | Tetap menerapkan perubahan meskipun ada sumber daya yang diubah, diarsipkan, atau dihapus di luar berkas-berkas ini.                                                                                                                                         |
| `--prune`            | Menghapus sumber daya yang ada di lockfile tetapi tidak lagi dideklarasikan dalam berkas.                                                                                                                                                                    |
| `--upgrade`          | Me-resolve ulang skill yang direferensikan melalui URL GitHub, yang jika tidak menggunakan flag ini akan tetap terkunci ke commit yang tercatat di lockfile.                                                                                                 |
| `--lock-file <path>` | Menggunakan lockfile ini alih-alih mencarinya ke atas mulai dari direktori saat ini. Simpan satu lockfile untuk setiap organisasi atau workspace, karena `ant apply` menolak lockfile yang organisasi atau workspace-nya tidak cocok dengan kredensial Anda. |
| `--verbose`, `-v`    | Menampilkan sumber daya yang tidak berubah dan nilai bidang secara lengkap dalam rencana.                                                                                                                                                                    |

## Langkah selanjutnya

<CardGroup cols={3}>
  <Card title="Mulai sesi" icon="terminal" href="https://platform.claude.com/docs/id/managed-agents/sessions">
    Jalankan agen yang telah Anda terapkan, dari CLI atau SDK
  </Card>

  <Card title="Deployment terjadwal" icon="clock" href="https://platform.claude.com/docs/id/managed-agents/scheduled-deployments">
    Bidang deployment, riwayat eksekusi, dan penjedaan
  </Card>

  <Card title="Scripting dan otomatisasi CLI" icon="code" href="https://platform.claude.com/docs/id/cli-sdks-libraries/cli/scripting">
    Pola scripting dan penggunaan dari Claude Code
  </Card>
</CardGroup>
