---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory
fetched_at: 2026-11-19T02:13:30.221159Z
sha256: 0a6825e21a1c69cbee71b5b31ee6f679180f9395e8c66509a18214008f0b7a65
---

---
title: Memory store di sandbox self-hosted
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory
description: "Lampirkan memory store ke sesi Claude Managed Agents yang berjalan di sandbox self-hosted: siapkan host, konfigurasikan sinkronisasi, dan tangani store read-only serta konflik."
featureMetadata:
  topic:
    title: Managed Agents
    url: https://platform.claude.com/docs/en/managed-agents/overview
  status: beta
  betaHeader: managed-agents-2026-04-01
  zdr:
    eligibility: not-eligible
    note: Tidak memiliki kelayakan ZDR, kecuali untuk Managed Agents yang di-host sendiri. Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya.
  supportedModels:
    - claude-fable-5-2
    - claude-mythos-5-2
    - claude-fable-5-1
    - claude-mythos-5-1
    - claude-fable-5
    - claude-mythos-5
    - claude-mythos-preview
    - claude-opus-5-5
    - claude-opus-5
    - claude-sonnet-5-5
    - claude-sonnet-5
    - claude-haiku-5-5
    - claude-haiku-4-5-20251001
    - claude-opus-4-8
    - claude-opus-4-7
    - claude-opus-4-6
    - claude-sonnet-4-6
    - claude-opus-4-5-20251101
    - claude-sonnet-4-5-20250929
  supportedPlatforms:
    Claude API: beta
---

Sesi pada environment self-hosted melampirkan [memory store](https://platform.claude.com/docs/id/managed-agents/memory) persis seperti sesi pada environment cloud. Cantumkan store tersebut di `resources` (csharp, go: `Resources`) saat Anda membuat sesi, seperti yang ditunjukkan di [Melampirkan memory store ke sesi](https://platform.claude.com/docs/id/managed-agents/memory#attach-a-memory-store-to-a-session). Sebuah sesi menerima hingga 8 memory store.

Perbedaannya terletak pada siapa yang mewujudkan store tersebut. Pada environment self-hosted, worker Anda, bukan infrastruktur Anthropic, yang mengunduh setiap store ke dalam sandbox dan menyinkronkan kembali perubahan yang dibuat agen.

## Persyaratan

* **Worker yang me-mount memory store:** Gunakan CLI `ant` versi 1.33.0 atau lebih baru, atau `EnvironmentWorker` dari SDK Python, TypeScript, atau Go.
* **Sistem file POSIX:** Host Windows tidak didukung, karena worker memerlukan `O_NOFOLLOW` saat membuka file memori. Anthropic menyarankan sistem file yang peka huruf besar-kecil, agar path memori yang hanya berbeda dalam huruf besar-kecil tidak bertabrakan. Volume macOS secara default tidak peka huruf besar-kecil, sehingga path semacam itu bertabrakan di sana.
* **Direktori `/mnt/memory` yang dapat ditulisi:** Lihat [Menyiapkan host](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#prepare-the-host). Di macOS, lihat [Menyiapkan host macOS](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#prepare-a-macos-host).
* **Secret milik item pekerjaan:** Jika kode Anda sendiri yang meluncurkan worker, [teruskan secret item pekerjaan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session#forward-the-work-items-secret) ke worker tersebut.

## Menyiapkan host

Di macOS, lewati perintah berikutnya dan ikuti [Menyiapkan host macOS](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#prepare-a-macos-host) sebagai gantinya.

Sebelum Anda memulai worker, buat direktori induk dan jadikan direktori tersebut dapat ditulis oleh pengguna yang menjalankan worker:

```bash
sudo mkdir -p /mnt/memory && sudo chown "$USER" /mnt/memory
```

Jangan membuat direktori store mana pun sendiri. Worker membuat direktori `mount_path` (java, php: `mountPath`; csharp, go: `MountPath`) untuk setiap store, seperti `/mnt/memory/user-preferences`, saat mengklaim sesi dan menghapusnya saat selesai menangani sesi tersebut. Jika sudah ada sesuatu di path tersebut, bahkan direktori kosong, worker menggagalkan item pekerjaan.

Dalam [pola sandbox-per-sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session), image sandbox memerlukan `/mnt/memory` yang dapat ditulis. Anda tidak perlu melakukan bind-mount direktori memori ke host, karena store menyimpan salinan permanen dari setiap memori.

### Menyiapkan host macOS

Di macOS, volume root bersifat hanya-baca, sehingga `mkdir` tidak dapat membuat `/mnt`. Sebagai gantinya, buat `/System/Volumes/Data/mnt/memory` di volume data, yang dapat ditulisi. Kemudian tambahkan satu baris ke `/etc/synthetic.conf`, sehingga macOS membuat `/mnt` sebagai tautan simbolik ke `/System/Volumes/Data/mnt`. Langkah-langkah ini memerlukan hak administrator.

Tanpa pengaturan ini, worker tidak dapat membuat direktori store, sehingga item pekerjaan gagal. Sesi kemudian tetap idle tanpa event error. Lihat [Memory store gagal di-mount atau disinkronkan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#memory-stores-fail-to-mount).

<Steps>
  <Step title="Buat direktori di volume data">
    Buat direktori `memory` dan jadikan pengguna worker sebagai pemiliknya. `$USER` adalah nama pengguna Anda sendiri. Jika worker berjalan sebagai pengguna lain, ganti `"$USER"` dengan nama pengguna tersebut.

    ```bash
    sudo mkdir -p /System/Volumes/Data/mnt/memory && sudo chown "$USER" /System/Volumes/Data/mnt/memory
    ```

    Lokasi ini hanyalah salah satu opsi. Jika Anda menggunakan lokasi lain, ubah path di baris `synthetic.conf` agar sesuai. Anthropic hanya menguji `/System/Volumes/Data/mnt`.
  </Step>

  <Step title="Tambahkan baris ke synthetic.conf">
    Jalankan `cat -et /etc/synthetic.conf`, yang menampilkan setiap tab sebagai `^I` dan setiap akhir baris sebagai `$`.

    * Jika ada baris yang berbunyi `mnt^ISystem/Volumes/Data/mnt$`, langkah ini sudah selesai. Lanjutkan ke langkah berikutnya.
    * Jika ada baris lain yang diawali dengan `mnt`, berhenti. Sesuatu yang lain di Mac ini sudah mendefinisikan `/mnt`.
    * Jika baris terakhir tidak diakhiri dengan `$`, jalankan `echo | sudo tee -a /etc/synthetic.conf` untuk mengakhirinya. Kemudian, tambahkan baris tersebut.
    * Jika tidak ada yang ditampilkan atau muncul laporan `No such file or directory`, tambahkan baris tersebut. Perintah berikut akan membuat file tersebut jika belum ada.
    * Jika tidak, tambahkan baris tersebut.

    Untuk menambahkan baris tersebut, jalankan perintah ini. Jalankan hanya sekali, karena setiap kali dijalankan akan menambahkan baris lain.

    ```bash
    printf 'mnt\tSystem/Volumes/Data/mnt\n' | sudo tee -a /etc/synthetic.conf
    ```

    Perintah tersebut menampilkan baris yang ditambahkannya. Baris tersebut memetakan nama `mnt` ke direktori yang berisi `memory`. File memerlukan tab di antara kedua kolom, yang ditulis oleh `\t`.
  </Step>

  <Step title="Buat tautan">
    Jalankan `apfs.util` dengan opsi `-t`. Perintah ini membuat tautan dari baris yang Anda tambahkan, tanpa perlu restart.

    ```bash
    sudo /System/Library/Filesystems/apfs.fs/Contents/Resources/apfs.util -t
    ```
  </Step>

  <Step title="Periksa hasilnya">
    Tampilkan daftar `/mnt` dan `/mnt/memory`.

    ```bash
    ls -ld /mnt /mnt/memory
    ```

    Baris pertama diakhiri dengan `/mnt -> System/Volumes/Data/mnt`. Baris kedua menampilkan pengguna worker sebagai pemilik `/mnt/memory`. Sekarang Anda dapat memulai worker.
  </Step>
</Steps>

Anthropic telah menguji pengaturan ini di macOS 26.7.1 dengan worker `ant` CLI.

### Mengisolasi sesi yang berbagi store

Dua sesi tidak dapat me-mount store yang sama pada satu sistem file secara bersamaan, karena keduanya memerlukan path yang sama. Untuk menjalankan sesi-sesi yang berbagi store secara berdampingan, berikan setiap sesi sistem file-nya sendiri. Jika Anda menggunakan sandbox untuk setiap sesi, setiap sesi otomatis mendapatkan sistem file-nya sendiri. Lihat [Menjalankan satu sandbox per sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session). Satu host dapat menjalankan banyak sandbox semacam itu.

## Cara worker menangani memori

Saat worker mengklaim item pekerjaan yang sesinya memiliki memory store terlampir, worker akan:

1. **Mengunduh setiap store ke `mount_path` (java, php: `mountPath`; csharp, go: `MountPath`)-nya.** Ini adalah direktori yang sama di bawah `/mnt/memory/` yang digunakan sesi cloud, dan prompt sistem sesi menjelaskannya kepada agen. Misalnya, store bernama “User Preferences” ditempatkan di `/mnt/memory/user-preferences/`.
2. **Membuka direktori tersebut untuk alat file.** Agen bekerja dengan memori menggunakan alat file yang sama dengan yang digunakannya di direktori kerja.
3. **Melakukan sinkronisasi setelah pemanggilan alat.** Worker melakukan sinkronisasi setelah pemanggilan alat jika [interval sinkronisasi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#sync-interval) (15 detik secara default) telah berlalu sejak sinkronisasi terakhirnya. Setiap sinkronisasi menulis memori yang berubah dari store ke disk dan mengunggah file yang diubah agen.
4. **Menjalankan sinkronisasi akhir saat sesi berakhir atau tetap idle selama batas idle worker.** Sinkronisasi akhir dapat memakan waktu hingga 60 detik. Perubahan yang belum diunggah hingga saat itu akan hilang. Worker kemudian menghapus direktori yang dibuatnya.

Batas idle secara default adalah 60 detik. [Saat worker selesai menangani sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-reference#when-the-worker-finishes-with-a-session) menjelaskan apa yang dicakup batas tersebut dan cara mengubahnya.

Alat `write` dan `edit` milik agen hanya mengubah salinan lokal, dan worker mengunggah perubahan tersebut pada sinkronisasi berikutnya. Path di bawah `/mnt/memory/` di luar direktori store bukanlah “scratch space” (ruang kerja sementara). Alat file worker menolak menulis ke path tersebut, dan apa pun yang ditulis perintah shell di sana tidak pernah disinkronkan ke store.

[Versi memori](https://platform.claude.com/docs/id/managed-agents/memory#audit-memory-changes), penghapusan kontennya (redact), serta melihat atau mengedit memori di Claude Console berfungsi seperti pada sesi cloud. Operasi baca dan tulis memori oleh agen muncul di [aliran event](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) sebagai event alat biasa.

Setiap direktori store berisi file penanda bernama `.anthropic-memory-store` yang mengaitkan direktori tersebut dengan store-nya. Biarkan file tersebut tetap ada. Jika penanda hilang atau diubah dan direktori masih berisi file, worker tidak menyinkronkan direktori tersebut. Worker juga tidak menghapus direktori tersebut saat selesai menangani sesi.

<Warning>
  Jika Anda menghentikan worker dengan baik selama sesi atau [menghentikan item pekerjaan sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#stop-a-session-gracefully), worker tetap mengunggah file baru dan file yang berubah. Worker juga menghapus direktori store. Worker tidak mengirimkan penghapusan, sehingga memori yang dihapus agen tetap ada di store kecuali sinkronisasi sebelumnya sudah menghapusnya dari store. Worker yang dimatikan paksa (killed) alih-alih dihentikan tidak menjalankan proses teardown, sehingga editan yang belum disinkronkan akan hilang dan direktori store tetap tertinggal. Lihat [Menghentikan worker dengan baik](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#stop-workers-gracefully).
</Warning>

## Mengonfigurasi sinkronisasi

Dua opsi `EnvironmentWorker` mengontrol perilaku memori. Atur opsi tersebut di mana pun Anda membuat worker, termasuk di handler webhook. Worker CLI `ant` selalu menggunakan nilai default.

### Interval sinkronisasi

`memory_sync_interval` (typescript: `memorySyncIntervalMs`; go: `MemorySyncInterval`) mengatur waktu terpendek antara dua sinkronisasi selama sesi berjalan.

| Pengaturan                    | Nilai                                               |
| ----------------------------- | --------------------------------------------------- |
| Default                       | 15 detik                                            |
| Minimum                       | 5 detik                                             |
| Contoh (10 detik)             | `10` (typescript: `10_000`; go: `10 * time.Second`) |
| Menonaktifkan dukungan memori | `None` (typescript: `null`; go: `-1`)               |

Worker tidak melakukan sinkronisasi berdasarkan timer. Worker memeriksa interval setelah setiap pemanggilan alat yang berjalan di sandbox Anda, seperti `bash`, `read`, atau alat kustom. Pemanggilan tersebut tidak harus menyentuh memori. Tanpa pemanggilan alat, tidak ada yang disinkronkan hingga [sinkronisasi akhir](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#how-the-worker-handles-memory). Perubahan dalam satu sesi baru sampai ke sesi lain yang sedang berjalan setelah keduanya melakukan sinkronisasi, sehingga waktu tunggunya tidak memiliki durasi yang pasti.

Interval yang lebih pendek mempersempit jendela waktu di mana sesi lain melihat memori yang usang, dengan konsekuensi lebih banyak permintaan ke memory store.

Nonaktifkan dukungan memori hanya pada worker yang sesinya tidak melampirkan memory store. Worker yang dinonaktifkan tidak mengunduh maupun menyinkronkan store, sehingga sesi dengan store terlampir berjalan tanpa store tersebut meskipun prompt sistemnya masih menjelaskannya.

Selama dukungan memori diaktifkan, item pekerjaan yang tiba tanpa `secret` (csharp, go: `Secret`) untuk sesi dengan store terlampir akan gagal alih-alih berjalan tanpa memori. Lihat [Memory store gagal di-mount atau disinkronkan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#memory-stores-fail-to-mount).

### Penghapusan

`memory_sync_deletions` (typescript: `memorySyncDeletions`; go: `MemorySyncDeletions`) mengatur apakah file yang dihapus agen secara lokal juga dihapus dari store. Unggahan dan unduhan tidak terpengaruh.

| Nilai                                                                 | Perilaku                                                                                                                                                                                          |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"enabled"` (go: `environments.MemorySyncDeletionsEnabled`) (default) | Menghapus memori dari store setelah sinkronisasi berikutnya mengonfirmasi bahwa file tersebut masih tidak ada.                                                                                    |
| `"log_only"` (go: `environments.MemorySyncDeletionsLogOnly`)          | Menjalankan pemeriksaan yang sama tetapi hanya mencatat apa yang akan dihapusnya. Gunakan mode ini untuk memantau apa yang akan dihapus worker Anda sebelum Anda memercayai mode yang diaktifkan. |
| `"disabled"` (go: `environments.MemorySyncDeletionsDisabled`)         | Tidak pernah menghapus dari store.                                                                                                                                                                |

Misalnya, untuk menyinkronkan paling banyak sekali setiap 10 detik dan hanya mencatat penghapusan yang akan dilakukan worker, gunakan contoh berikut. Contoh ini menggunakan `/workspace` sebagai direktori kerja, yang harus sudah ada sebelum worker dimulai. [Menjalankan worker always-on](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#run-an-always-on-worker) menjelaskan cara membuat direktori tersebut dan apa yang digunakan di macOS.

<CodeGroup exclude="shell, csharp, java, php, ruby">
  <CodeGroupItem language="cURL">
    Worker adalah proses yang berjalan lama, bukan satu permintaan HTTP. Untuk mengubah pengaturan sinkronisasi, gunakan `EnvironmentWorker` di SDK Python, TypeScript, atau Go.
  </CodeGroupItem>

  <CodeGroupItem language="CLI">
    Worker CLI `ant` selalu menggunakan pengaturan sinkronisasi default. Untuk mengubahnya, gunakan `EnvironmentWorker` di SDK Python, TypeScript, atau Go.
  </CodeGroupItem>

  ```python Python
  import asyncio
  import contextlib
  import os
  import signal
  from anthropic import AsyncAnthropic
  from anthropic.lib.environments import EnvironmentWorker


  async def main() -> None:
      environment_key = os.environ["ANTHROPIC_ENVIRONMENT_KEY"]
      environment_id = os.environ["ANTHROPIC_ENVIRONMENT_ID"]
      async with AsyncAnthropic(auth_token=environment_key) as client:
          worker = EnvironmentWorker(
              client,
              environment_id=environment_id,
              environment_key=environment_key,
              workdir="/workspace",
              memory_sync_interval=10,  # seconds
              memory_sync_deletions="log_only",
          )
          task = asyncio.create_task(worker.run())
          loop = asyncio.get_running_loop()
          for signum in (signal.SIGINT, signal.SIGTERM):
              loop.add_signal_handler(signum, task.cancel)
          with contextlib.suppress(asyncio.CancelledError):
              await task


  asyncio.run(main())
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import { EnvironmentWorker } from "@anthropic-ai/sdk/helpers/beta/environments";

  const environmentKey = process.env.ANTHROPIC_ENVIRONMENT_KEY!;
  const environmentId = process.env.ANTHROPIC_ENVIRONMENT_ID!;
  const client = new Anthropic({ authToken: environmentKey });
  const controller = new AbortController();
  process.once("SIGINT", () => controller.abort());
  process.once("SIGTERM", () => controller.abort());

  const worker = new EnvironmentWorker({
    client,
    environmentId,
    environmentKey,
    workdir: "/workspace",
    signal: controller.signal,
    memorySyncIntervalMs: 10_000,
    memorySyncDeletions: "log_only"
  });
  await worker.run();
  ```

  <CodeGroupItem language="C#">
    SDK C# tidak memiliki `EnvironmentWorker`.
  </CodeGroupItem>

  ```go Go
  package main

  import (
  	"context"
  	"log"
  	"os"
  	"os/signal"
  	"syscall"
  	"time"

  	"github.com/anthropics/anthropic-sdk-go/v2"
  	"github.com/anthropics/anthropic-sdk-go/v2/lib/environments"
  	"github.com/anthropics/anthropic-sdk-go/v2/option"
  )

  func main() {
  	environmentKey := os.Getenv("ANTHROPIC_ENVIRONMENT_KEY")
  	environmentID := os.Getenv("ANTHROPIC_ENVIRONMENT_ID")

  	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
  	defer stop()

  	client := anthropic.NewClient(option.WithAuthToken(environmentKey))

  	worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
  		EnvironmentID:       environmentID,
  		EnvironmentKey:      environmentKey,
  		Workdir:             "/workspace",
  		MemorySyncInterval:  10 * time.Second,
  		MemorySyncDeletions: environments.MemorySyncDeletionsLogOnly,
  	})
  	if err := worker.Run(ctx); err != nil {
  		log.Fatalf("worker: %v", err)
  	}
  }
  ```

  <CodeGroupItem language="Java">
    SDK Java tidak memiliki `EnvironmentWorker`.
  </CodeGroupItem>

  <CodeGroupItem language="PHP">
    SDK PHP tidak memiliki `EnvironmentWorker`.
  </CodeGroupItem>

  <CodeGroupItem language="Ruby">
    SDK Ruby tidak memiliki `EnvironmentWorker`.
  </CodeGroupItem>
</CodeGroup>

## Store read-only dan konflik

### Store read-only

Untuk store yang dilampirkan dengan `access: "read_only"`, alat `write` dan `edit` menolak mengubah file di dalam direktorinya. Worker tidak pernah mengunggah apa pun dari direktori tersebut.

Perubahan yang dibuat melalui `bash` atau melalui alat kustom atau server MCP yang Anda layani dari sandbox tidak diblokir secara lokal. Perubahan tersebut tidak pernah sampai ke store. File yang diubah tetap berubah hingga salah satu hal berikut terjadi:

* **Memori tersebut mendapatkan versi baru di store.** Sinkronisasi worker berikutnya menimpa file tersebut dengan versi itu.
* **Worker selesai menangani sesi.** Worker menghapus direktori tersebut.

Agar salinan lokal juga tetap tidak berubah, nonaktifkan alat `bash` untuk agen tersebut. Selain itu, jangan berikan alat kustom atau server MCP apa pun yang menulis ke sistem file sandbox. Jangan me-mount volume read-only di path store. Mount tersebut menempatkan direktori di path itu, dan worker menggagalkan item pekerjaan jika sudah ada sesuatu di sana.

### Konflik

Konflik adalah memori yang berubah baik di store maupun di sandbox sejak sinkronisasi sebelumnya. Penghapusan dihitung sebagai perubahan. Untuk store yang dilampirkan dengan `access: "read_write"`, worker menyelesaikan konflik pada sinkronisasi berikutnya:

| Di store | Di sandbox | Hasil                                           |
| -------- | ---------- | ----------------------------------------------- |
| Berubah  | Berubah    | Versi store menimpa file.                       |
| Berubah  | Dihapus    | Worker menulis kembali versi store ke sandbox.  |
| Dihapus  | Berubah    | Worker membuat ulang memori dari file tersebut. |

Pada dua baris pertama, perubahan atau penghapusan oleh agen akan hilang, meskipun pemanggilan alat berhasil. Tidak ada yang memberi tahu agen, dan satu-satunya tanda kehilangan tersebut adalah peringatan di log worker. Pada baris terakhir, penghapusan di store dibatalkan.

## Pemecahan masalah

Lihat [Memory store gagal di-mount atau disinkronkan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#memory-stores-fail-to-mount) untuk pesan log worker beserta perbaikannya.

## Ketersediaan

Memory store di sandbox self-hosted dalam versi beta di semua model.

### Dukungan API

#### [Managed Agents](https://platform.claude.com/docs/id/managed-agents/overview)

* Ketersediaan: Tersedia

| Status | Platform cloud |
| ------ | -------------- |
| Beta   | Claude API     |

### Header beta yang diperlukan

[Ikhtisar header beta](https://platform.claude.com/docs/id/api/beta-headers)

Header beta memungkinkan Anda mengakses fitur eksperimental dan kemampuan model baru sebelum menjadi bagian dari API standar.

* `managed-agents-2026-04-01`

### Penanganan data

[Ikhtisar penanganan data](https://platform.claude.com/docs/id/manage-claude/api-and-data-retention#feature-eligibility)

| Item   | Retensi data nol                                                                                                                                                                                                                                                                                     | HIPAA                                                                        |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Status | Tidak layak                                                                                                                                                                                                                                                                                          | Tidak layak                                                                  |
| Detail | Tidak memiliki kelayakan ZDR, kecuali untuk Managed Agents yang di-host sendiri. Sesi adalah sumber daya stateful; transkrip tetap tersimpan hingga Anda menghapusnya. [Pelajari lebih lanjut](https://platform.claude.com/docs/id/managed-agents/self-hosted-data-and-access#how-long-data-is-kept) | Tidak memiliki kelayakan HIPAA. Berlaku untuk semua subfitur Managed Agents. |

Endpoint yang berlaku:

* `/v1/agents`
* `/v1/sessions`
* `/v1/environments`
