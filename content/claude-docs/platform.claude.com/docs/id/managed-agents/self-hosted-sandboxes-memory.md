---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory
fetched_at: 2026-10-08T02:28:25.993144Z
sha256: bb8b2d487e44d87dee038e212b1b8b8b1938718eecc971fe3e06970631b4a0e2
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
---

Sesi pada environment self-hosted melampirkan [memory store](https://platform.claude.com/docs/id/managed-agents/memory) persis seperti sesi pada environment cloud. Cantumkan memory store tersebut di `resources` saat Anda membuat sesi, seperti yang ditunjukkan di [Melampirkan memory store ke sesi](https://platform.claude.com/docs/id/managed-agents/memory#attach-a-memory-store-to-a-session). Sebuah sesi menerima hingga 8 memory store.

Perbedaannya terletak pada siapa yang mewujudkan store tersebut. Pada environment self-hosted, worker Anda, bukan infrastruktur Anthropic, yang mengunduh setiap store ke dalam sandbox dan menyinkronkan kembali perubahan yang dibuat agen.

## Persyaratan

* **Worker yang me-mount memory store:** Gunakan CLI `ant` versi 1.33.0 atau lebih baru, atau `EnvironmentWorker` dari SDK Python, TypeScript, atau Go.
* **Sistem file POSIX:** Host Windows tidak didukung, karena worker memerlukan `O_NOFOLLOW` saat membuka file memori. Sistem file yang peka huruf besar-kecil (case-sensitive) direkomendasikan, agar path memori yang hanya berbeda dalam huruf besar-kecil tidak bertabrakan.
* **Direktori `/mnt/memory` yang dapat ditulis:** Lihat [Menyiapkan host](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#prepare-the-host).
* **Secret milik work item:** Jika kode Anda sendiri yang meluncurkan worker, [teruskan secret milik work item](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#forward-the-work-items-secret) ke worker tersebut.

<Note>
  Memory store tidak dapat dilampirkan ke sesi pada environment self-hosted di [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws).
</Note>

## Menyiapkan host

Sebelum Anda memulai worker, buat direktori induk dan jadikan direktori tersebut dapat ditulis oleh pengguna yang menjalankan worker:

```bash
sudo mkdir -p /mnt/memory && sudo chown "$USER" /mnt/memory
```

Jangan membuat direktori per-store sendiri. Worker membuat direktori `mount_path` untuk setiap store (misalnya, `/mnt/memory/user-preferences`) saat sesi dimulai dan menghapusnya saat sesi berakhir. Jika sudah ada sesuatu di path tersebut, worker menolak untuk memulai pekerjaan sesi.

Dalam [pola sandbox-per-sesi](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#run-one-sandbox-per-session), image sandbox memerlukan `/mnt/memory` yang dapat ditulis. Anda tidak perlu melakukan bind-mount direktori memori ke host, karena worker mengunggah isinya ke store sebelum sandbox keluar.

### Mengisolasi sesi yang berbagi store

Dua sesi tidak dapat me-mount store yang sama pada satu host secara bersamaan, karena keduanya memerlukan path yang sama. Jika sesi-sesi Anda melampirkan store yang sama, jalankan satu sesi per sistem file. Memberikan setiap sesi [sandbox-nya sendiri](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-workers#run-one-sandbox-per-session) memenuhi aturan ini.

## Cara worker menangani memori

Saat worker mengklaim work item yang sesinya memiliki memory store terlampir, worker akan:

1. **Mengunduh setiap store ke `mount_path`-nya.** Ini adalah direktori yang sama di bawah `/mnt/memory/` yang digunakan sesi cloud, dan prompt sistem sesi menjelaskannya kepada agen. Misalnya, store bernama "User Preferences" ditempatkan di `/mnt/memory/user-preferences/`.
2. **Membuka direktori tersebut untuk alat file.** Agen bekerja dengan memori menggunakan alat file yang sama dengan yang digunakannya di direktori kerja.
3. **Merekonsiliasi perubahan setelah pemanggilan alat,** paling banyak sekali per interval sinkronisasi (15 detik secara default). Memori yang berubah di store ditulis ke disk, dan file yang diubah agen diunggah ke store.
4. **Menjalankan sinkronisasi akhir saat sesi berakhir.** Worker menuntaskan unggahan yang masih tertunda hingga 30 detik, lalu menghapus direktori yang dibuatnya.

Memory store di sisi Anthropic tetap menjadi sumber kebenaran. [Versi memori](https://platform.claude.com/docs/id/managed-agents/memory#audit-memory-changes), redaksi, serta melihat atau mengedit memori di Console berfungsi sama seperti pada sesi cloud. Pembacaan dan penulisan memori oleh agen muncul di [aliran event](https://platform.claude.com/docs/id/managed-agents/events-and-streaming) sebagai event alat biasa.

Karena setiap worker melakukan sinkronisasi berdasarkan interval, perubahan yang ditulis dalam satu sesi baru terlihat oleh sesi lain yang sedang berjalan setelah keduanya melakukan sinkronisasi. Biasanya ini jauh di bawah satu menit pada interval default. Sesi pada sandbox cloud melihat perubahan satu sama lain hampir seketika.

Setiap direktori store berisi file penanda bernama `.anthropic-memory-store` yang mengaitkan direktori tersebut dengan store-nya. Biarkan file tersebut tetap ada: worker tidak menyinkronkan direktori yang penandanya hilang atau diubah.

<Warning>
  Worker yang dimatikan paksa (killed) alih-alih dihentikan tidak menjalankan proses teardown, sehingga editan yang belum disinkronkan akan hilang dan direktori store tetap tertinggal. Lihat [Menghentikan worker dengan baik](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#stop-workers-gracefully).
</Warning>

## Mengonfigurasi sinkronisasi

Dua opsi `EnvironmentWorker` mengontrol perilaku memori. Atur opsi tersebut di mana pun Anda membuat worker, termasuk di handler webhook. Worker CLI `ant` selalu menggunakan nilai default.

### Interval sinkronisasi

`memory_sync_interval` (typescript: `memorySyncIntervalMs`; go: `MemorySyncInterval`) mengatur seberapa sering store yang terlampir direkonsiliasi dengan server selama sesi berjalan.

| Pengaturan                    | Nilai                                                       |
| ----------------------------- | ----------------------------------------------------------- |
| Default                       | 15 detik                                                    |
| Minimum                       | 5 detik                                                     |
| Contoh (10 detik)             | `10` (python; typescript: `10_000`; go: `10 * time.Second`) |
| Menonaktifkan dukungan memori | `None` (python; typescript: `null`; go: `-1`)               |

Interval yang lebih pendek mempersempit jendela waktu di mana sesi lain melihat memori yang usang, dengan konsekuensi lebih banyak permintaan ke memory store.

Nonaktifkan dukungan memori hanya pada worker yang sesinya tidak melampirkan memory store. Worker yang dinonaktifkan tidak mengunduh maupun menyinkronkan store, sehingga sesi dengan store terlampir berjalan tanpa store tersebut meskipun prompt sistemnya masih menjelaskannya.

Selama dukungan memori diaktifkan, work item yang tiba tanpa `secret` untuk sesi dengan store terlampir akan gagal alih-alih berjalan tanpa memori. Lihat [Memory store gagal di-mount](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#memory-stores-fail-to-mount).

### Penghapusan

`memory_sync_deletions` (typescript: `memorySyncDeletions`; go: `MemorySyncDeletions`) mengatur apakah file yang dihapus agen secara lokal juga dihapus dari store. Unggahan dan unduhan tidak terpengaruh.

| Nilai                                                                 | Perilaku                                                                                                                                                                                  |
| --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"enabled"` (go: `environments.MemorySyncDeletionsEnabled`) (default) | Menghapus memori dari store setelah sinkronisasi berikutnya mengonfirmasi bahwa file tersebut masih tidak ada.                                                                            |
| `"log_only"` (go: `environments.MemorySyncDeletionsLogOnly`)          | Menjalankan pemeriksaan yang sama tetapi hanya mencatat apa yang akan dihapusnya. Gunakan mode ini untuk memantau apa yang akan dihapus worker Anda sebelum Anda memercayai mode enabled. |
| `"disabled"` (go: `environments.MemorySyncDeletionsDisabled`)         | Tidak pernah menghapus dari store.                                                                                                                                                        |

Misalnya, untuk menyinkronkan setiap 10 detik dan hanya mencatat penghapusan yang akan dilakukan worker:

<CodeGroup exclude="shell">
  ```python Python
  worker = EnvironmentWorker(
      client,
      environment_id=environment_id,
      environment_key=environment_key,
      workdir="/workspace",
      memory_sync_interval=10,  # seconds
      memory_sync_deletions="log_only",
  )
  ```

  ```typescript TypeScript
  const worker = new EnvironmentWorker({
    client,
    environmentId,
    environmentKey,
    workdir: "/workspace",
    memorySyncIntervalMs: 10_000,
    memorySyncDeletions: "log_only"
  });
  ```

  ```csharp C#
  // EnvironmentWorker saat ini belum tersedia di SDK C#.
  ```

  ```go Go
  worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
  	EnvironmentID:       environmentID,
  	EnvironmentKey:      environmentKey,
  	Workdir:             "/workspace",
  	MemorySyncInterval:  10 * time.Second,
  	MemorySyncDeletions: environments.MemorySyncDeletionsLogOnly,
  })
  ```

  ```java Java
  // EnvironmentWorker saat ini belum tersedia di Java SDK.
  ```

  ```php PHP
  // EnvironmentWorker saat ini belum tersedia di PHP SDK.
  ```

  ```ruby Ruby
  # EnvironmentWorker saat ini belum tersedia di Ruby SDK.
  ```
</CodeGroup>

## Store read-only dan konflik

Untuk store yang dilampirkan dengan `access: "read_only"`, alat `write` dan `edit` menolak mengubah file di dalam direktorinya. Worker tidak pernah mengunggah apa pun dari direktori tersebut.

Perubahan yang dibuat melalui `bash`, atau melalui alat kustom atau server MCP yang Anda layani dari sandbox, tidak diblokir secara lokal. Perubahan tersebut tidak pernah disinkronkan ke store, dan perubahan jarak jauh berikutnya pada memori tersebut akan menimpanya. Jika salinan lokal itu sendiri harus tetap tidak berubah selama sesi:

* Nonaktifkan alat `bash` untuk agen tersebut, dan jangan berikan alat kustom apa pun yang menulis ke sistem file sandbox.
* Jangan me-mount path store sebagai read-only. Worker sendiri harus membuat direktori tersebut dan menulis memori yang diunduh ke dalamnya.

Konflik diselesaikan dengan mengutamakan store. Misalkan agen mengubah file memori yang juga berubah di store sejak sesi terakhir kali menyinkronkannya. Pada sinkronisasi berikutnya, worker mempertahankan versi store, menimpa file lokal dengan versi tersebut, dan mencatat peringatan. Alat `write` dan `edit` itu sendiri berhasil dan tidak ada error yang sampai ke agen. Jika perubahan agen masih relevan, agen dapat membaca ulang file tersebut setelah sinkronisasi dan membuat perubahan itu lagi.

## Pemecahan masalah

Lihat [Memory store gagal di-mount](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-operations#memory-stores-fail-to-mount) untuk pesan log worker beserta perbaikannya.
