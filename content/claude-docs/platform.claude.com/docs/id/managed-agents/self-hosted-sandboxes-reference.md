---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: a6b19a2c7dabd1dc8ffffb9dab7c5f4b999cc2fcde16f6fcf3ca8454fa4d8eb8
---

---
title: Referensi worker self-hosted
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference
description: "Referensi untuk worker sandbox self-hosted: flag CLI ant, variabel lingkungan, persyaratan host, path sistem file, dan opsi helper SDK."
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
---

Halaman ini mendokumentasikan worker siap pakai yang melayani environment `self_hosted`. Untuk panduan berorientasi tugas, mulailah dengan [Sandbox self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes) dan [Menerapkan worker self-hosted](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers).

## Perintah dan flag CLI

| Perintah               | Deskripsi                                                                                                                                                                   |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ant beta:worker poll` | Mengklaim work item dari antrean environment dan menjalankan setiap sesi di dalam proses. Dengan `--on-work`, memanggil skrip Anda untuk setiap work item sebagai gantinya. |
| `ant beta:worker run`  | Menangani satu sesi yang diklaim lalu keluar. Gunakan sebagai entrypoint dari sandbox per sesi.                                                                             |

| Flag                | Deskripsi                                                                                                                                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--environment-id`  | Environment yang di-poll untuk mendapatkan pekerjaan. Juga dibaca dari `ANTHROPIC_ENVIRONMENT_ID`.                                                                                                                  |
| `--environment-key` | Mengautentikasi worker dengan environment ini. Juga dibaca dari `ANTHROPIC_ENVIRONMENT_KEY`.                                                                                                                        |
| `--workdir`         | Direktori tempat skill diunduh dan tempat alat membaca serta menulis file. Default-nya `.` (direktori saat ini).                                                                                                    |
| `--on-work`         | Skrip yang dipanggil untuk setiap work item yang diklaim alih-alih menjalankan alat di dalam proses. Menerima detail sesi sebagai variabel lingkungan dan work item sebagai JSON pada standard input.               |
| `--max-idle`        | Berapa lama menunggu setelah sesi menjadi idle dengan [stop reason](https://platform.claude.com/docs/id/build-with-claude/handling-stop-reasons) (alasan berhenti) `end_turn` sebelum dimatikan. Default-nya `60s`. |
| `--log-format`      | Format output log. Gunakan `json` untuk penyerapan log terstruktur. Default-nya `text`.                                                                                                                             |

## Variabel lingkungan

| Variabel                        | Deskripsi                                         | Diatur oleh                                                                                                                                                                          |
| ------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ANTHROPIC_ENVIRONMENT_ID`      | Environment yang antreannya dilayani oleh worker. | Anda, di host worker. Poller meneruskannya ke skrip `--on-work`.                                                                                                                     |
| `ANTHROPIC_ENVIRONMENT_KEY`     | Mengautentikasi worker ke antreannya.             | Anda, di host worker. Poller meneruskannya ke skrip `--on-work`.                                                                                                                     |
| `ANTHROPIC_SESSION_ID`          | Sesi yang diwakili oleh work item yang diklaim.   | Poller, untuk skrip `--on-work`.                                                                                                                                                     |
| `ANTHROPIC_WORK_ID`             | Work item yang diklaim.                           | Poller, untuk skrip `--on-work`.                                                                                                                                                     |
| `ANTHROPIC_WORK_SECRET`         | Secret per sesi milik work item.                  | Anda. Poller tidak mengaturnya. Lihat [Meneruskan secret work item](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#forward-the-work-items-secret). |
| `ANTHROPIC_BASE_URL`            | Menimpa endpoint API default. Opsional.           | Anda, di host worker.                                                                                                                                                                |
| `ANTHROPIC_WEBHOOK_SIGNING_KEY` | Memverifikasi payload webhook yang masuk.         | Anda, di host penangan webhook.                                                                                                                                                      |

## Persyaratan host

| Worker            | Persyaratan                                                                                                                      |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Semua worker      | Host Linux dengan `/bin/bash` tepat di path tersebut. Alat bash milik worker memanggilnya secara langsung, tanpa merujuk `PATH`. |
| TypeScript SDK    | `unzip` dan `tar` pada `PATH`, serta Node.js 22 atau lebih baru.                                                                 |
| Python dan Go SDK | Tidak ada binary tambahan. SDK ini menggunakan pustaka standarnya untuk ekstraksi arsip.                                         |

[Memory store](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#requirements) menambahkan persyaratannya sendiri.

## Sistem file sandbox

| Path                       | Isi                                                                                                                                                                                                                     |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/workspace`               | Direktori kerja default sistem untuk eksekusi alat dan pengunduhan skill. Jika Anda menggunakan direktori kerja yang berbeda, perbarui prompt sistem agen Anda agar Claude dapat menemukan file skill.                  |
| `<workdir>/skills/<name>/` | Skill agen yang telah diunduh.                                                                                                                                                                                          |
| `/mnt/memory/<store>/`     | Satu direktori per memory store yang terlampir, di `mount_path` milik store tersebut (misalnya, `/mnt/memory/user-preferences/`). Worker membuat direktori ini saat mengklaim sesi dan menghapusnya saat sesi berakhir. |

Pada environment self-hosted, prompt sistem sesi menghilangkan instruksi `/mnt/session/outputs` yang digunakan pada sandbox yang dikelola Anthropic. Hasil akhir berada di mana pun agen menuliskannya di sistem file sandbox Anda, biasanya di bawah direktori kerja.

Skill dapat menyertakan file executable yang dapat dijalankan langsung oleh agen. Worker CLI dan SDK mempertahankan izin eksekusi yang tercatat dalam bundel skill saat mengekstraknya. Jika Anda mengimplementasikan pengunduhan skill secara manual, Anda bertanggung jawab untuk mengatur izin eksekusi.

## Helper SDK

SDK Python, TypeScript, dan Go menyediakan tiga helper dengan tingkat kontrol yang berbeda:

| Helper                                                                                                                                                                                                                                                            | Fungsinya                                                                                 | Gunakan saat                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| [`EnvironmentWorker`](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#environment-worker)                                                                                                                                      | Menangani polling, penyiapan, dan eksekusi secara menyeluruh.                             | Sebagian besar kasus.                                                                                                        |
| [`work.poller()` (go: `environments.NewWorkPoller()`)](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#work-poller)                                                                                                            | Melakukan polling pada antrean kerja dan memberikan setiap sesi yang diklaim kepada Anda. | Anda menentukan apa yang terjadi untuk setiap sesi, misalnya meluncurkan sandbox alih-alih menjalankan alat di dalam proses. |
| [`client.beta.sessions.events.tool_runner()` (typescript: `client.beta.sessions.events.toolRunner()`; go: `client.Beta.Sessions.Events.NewToolRunner()`)](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#session-tool-runner) | Menjalankan pemanggilan alat untuk satu sesi, berdasarkan ID sesi dan daftar alat.        | Anda sudah mengklaim pekerjaan dan hanya membutuhkan lapisan eksekusi.                                                       |

### EnvironmentWorker

| Metode                                                           | Deskripsi                                                                                                                                                                                                                                                                                                                                                             |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `run()` (go: `Run()`)                                            | Berjalan tanpa batas waktu, mengambil sesi saat sesi tersebut tiba.                                                                                                                                                                                                                                                                                                   |
| `handle_item()` (typescript: `handleItem()`; go: `HandleItem()`) | Menangani satu work item yang diklaim lalu kembali. Teruskan pengidentifikasi work item, sesi, dan environment serta `work_secret` (typescript: `workSecret`; go: `WorkSecret`) secara eksplisit, atau biarkan helper ini membaca [variabel `ANTHROPIC_*`](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#environment-variables). |

| Opsi                                                                                   | Deskripsi                                                                                                                                                                                                                    |
| -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tools` (go: `ToolsFunc`)                                                              | Factory yang menerima `AgentToolContext` milik sesi dan mengembalikan daftar alat. Default-nya adalah toolset agen standar.                                                                                                  |
| `memory_sync_interval` (typescript: `memorySyncIntervalMs`; go: `MemorySyncInterval`)  | Seberapa sering memory store yang terlampir direkonsiliasi dengan server selama sesi berjalan. Lihat [Interval sinkronisasi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#sync-interval). |
| `memory_sync_deletions` (typescript: `memorySyncDeletions`; go: `MemorySyncDeletions`) | Apakah file yang dihapus agen secara lokal juga dihapus dari store. Lihat [Penghapusan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#deletions).                                          |

`EnvironmentWorker` mengelola `AgentToolContext` dan toolset secara otomatis. Teruskan factory `tools` (go: `ToolsFunc`) untuk menyesuaikan daftar alat:

<CodeGroup exclude="shell">
  ```python Python
  EnvironmentWorker(client, ..., tools=lambda env: [beta_bash_tool(env), my_custom_tool])
  ```

  ```typescript TypeScript
  new EnvironmentWorker({
    client,
    environmentId,
    environmentKey,
    tools: (ctx) => [betaBashTool(ctx), myCustomTool]
  });
  ```

  ```csharp C#
  // EnvironmentWorker saat ini belum tersedia di SDK C#.
  // Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
  ```

  ```go Go
  worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
  	EnvironmentID:  environmentID,
  	EnvironmentKey: environmentKey,
  	ToolsFunc: func(env *agenttoolset.AgentToolContext) []anthropic.BetaTool {
  		return []anthropic.BetaTool{agenttoolset.BetaBashTool(env), myCustomTool}
  	},
  })
  ```

  ```java Java
  // EnvironmentWorker saat ini belum tersedia di Java SDK.
  // Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
  ```

  ```php PHP
  // EnvironmentWorker saat ini belum tersedia di PHP SDK.
  // Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
  ```

  ```ruby Ruby
  # EnvironmentWorker saat ini belum tersedia di Ruby SDK.
  # Untuk menjawab panggilan alat kustom secara langsung, lihat aliran event sesi.
  ```
</CodeGroup>

### Work poller

| Opsi                                                                                 | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `drain` (go: `Drain`)                                                                | Apakah polling dihentikan setelah antrean kosong alih-alih menunggu pekerjaan baru.                                                                                                                                                                                                                                                                                                                          |
| `block_ms` (python; typescript: `blockMs`; go: `BlockMs`)                            | Berapa lama setiap poll menunggu pekerjaan tiba sebelum kembali, dalam milidetik. Harus antara 1 dan 999; helper melakukan poll ulang secara otomatis. Teruskan `null` (typescript; python: `None`; go: `param.Null[int64]()`) untuk pemeriksaan non-blocking. Default-nya adalah long-poll 999 ms.                                                                                                          |
| `reclaim_older_than_ms` (typescript: `reclaimOlderThanMs`; go: `ReclaimOlderThanMs`) | Mengklaim ulang work item yang telah diklaim tetapi tidak pernah di-acknowledge dalam jumlah milidetik ini.                                                                                                                                                                                                                                                                                                  |
| `auto_stop` (typescript: `autoStop`; go: `AutoStop`)                                 | Apakah sinyal berhenti dikirim untuk setiap work item setelah badan loop Anda selesai memprosesnya. Atur ke `false` (python: `False`; go: `param.NewOpt(false)`) ketika apa pun yang menjalankan work item mengirim sinyal berhenti sendiri. `handle_item()` (typescript: `handleItem()`; go: `HandleItem()`) melakukannya, begitu pula sandbox yang Anda luncurkan yang memiliki pemanggilan stop tersebut. |

Untuk contoh lengkap, lihat [Meluncurkan sandbox dari poller SDK](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#launch-sandboxes-from-the-sdk-poller).

### Session tool runner

`client.beta.sessions.events.tool_runner()` (typescript: `client.beta.sessions.events.toolRunner()`; go: `client.Beta.Sessions.Events.NewToolRunner()`) menerima daftar alat sebagai `tools` (go: `Tools`). Untuk membangun daftar tersebut, siapkan `AgentToolContext` sendiri dan panggil `beta_agent_toolset_20260401(env)` (typescript: `betaAgentToolset20260401(ctx)`; go: `agenttoolset.BetaAgentToolset20260401(env)`):

<CodeGroup exclude="shell">
  ```python Python
  from anthropic.lib.tools.agent_toolset import (
      AgentToolContext,
      beta_agent_toolset_20260401,
  )

  async with AgentToolContext(
      workdir="/workspace", client=client, session_id=work.data.id
  ) as env:
      # skills diunduh ke /workspace/skills/<name>/
      tools = beta_agent_toolset_20260401(env)
  ```

  ```typescript TypeScript
  import {
    setupSkills,
    betaAgentToolset20260401
  } from "@anthropic-ai/sdk/tools/agent-toolset/node";

  const ctx = { workdir: "/workspace", client, sessionId: work.data.id };
  await setupSkills(ctx);
  const tools = betaAgentToolset20260401(ctx);
  ```

  ```csharp C#
  // AgentToolContext saat ini belum tersedia di SDK C#.
  ```

  ```go Go
  env := &agenttoolset.AgentToolContext{Workdir: "/workspace"}
  if err := env.SetupSkills(ctx, client, work.Data.ID); err != nil {
  	panic(err)
  }
  // skills diunduh ke /workspace/skills/<name>/
  tools := agenttoolset.BetaAgentToolset20260401(env)
  ```

  ```java Java
  // AgentToolContext saat ini belum tersedia di Java SDK.
  ```

  ```php PHP
  // AgentToolContext saat ini belum tersedia di PHP SDK.
  ```

  ```ruby Ruby
  # AgentToolContext saat ini belum tersedia di Ruby SDK.
  ```
</CodeGroup>

### AgentToolContext dan toolset agen

`AgentToolContext` adalah konteks eksekusi untuk pemanggilan alat. Konteks ini mendefinisikan direktori kerja dan kebijakan path, serta dapat mengunduh skill milik sesi.

| Opsi                                                                 | Deskripsi                                                                                                         |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `allowed_roots` (typescript: `allowedRoots`; go: `AllowedRoots`)     | Direktori, selain direktori kerja, yang dapat dijangkau oleh alat file (`read`, `write`, `edit`, `glob`, `grep`). |
| `read_only_roots` (typescript: `readOnlyRoots`; go: `ReadOnlyRoots`) | Direktori yang path di bawahnya ditolak oleh `write` dan `edit`.                                                  |

`EnvironmentWorker` sendiri menambahkan direktori memory store milik sesi ke `allowed_roots` (typescript: `allowedRoots`; go: `AllowedRoots`), dan direktori store yang dilampirkan dengan `access: "read_only"` ke `read_only_roots` (typescript: `readOnlyRoots`; go: `ReadOnlyRoots`).

Pembatasan ini hanyalah pengaman untuk alat file, bukan sandbox. Pembatasan ini tidak membatasi `bash`.

`beta_agent_toolset_20260401(env)` (typescript: `betaAgentToolset20260401(ctx)`; go: `agenttoolset.BetaAgentToolset20260401(env)`) menerima `AgentToolContext` dan mengembalikan implementasi alat standar (`bash`, `read`, `write`, `edit`, `glob`, `grep`).
