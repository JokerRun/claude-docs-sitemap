---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security
fetched_at: 2026-11-19T02:13:30.221159Z
sha256: 9286f3dc54b9fde1dc60fae9f53b1cbf9703683836405b8bb1a6d146908fa161
---

---
title: Model keamanan
url: https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-security
description: Model tanggung jawab bersama untuk lingkungan sandbox yang di-hosting sendiri.
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
    Claude Platform on AWS: beta
    Claude Models on Google Cloud (Anthropic managed):
      availability: beta
      note: Anda menulis worker Anda sendiri, yang memanggil endpoint Environments Work.
---

Di setiap lingkungan, Anthropic mengamankan bagian-bagian yang dijalankannya: integritas sesi dan antrean kerja, isolasi multitenant, dan minimisasi konteks agen. Ketika Anda melakukan self-hosting sandbox, tanggung jawab berikut berada di tangan Anda.

## Apa yang menjadi tanggung jawab Anda

* **Kualitas image sandbox dan hardening runtime.** Anthropic tidak memeriksa atau memverifikasi image sandbox Anda. Ikuti praktik terbaik seperti menghapus Linux capabilities yang tidak diperlukan, menjalankan sebagai pengguna non-root, dan menggunakan sistem file root read-only.

* **Kontrol egress jaringan.** Akses jaringan sandbox Anda ditentukan oleh aturan VPC dan firewall Anda. Tanpa pembatasan egress, eksekusi alat yang telah disusupi dapat menjangkau host eksternal mana pun. Batasi lalu lintas keluar hanya ke endpoint yang dibutuhkan alat Anda.

* **Penyimpanan dan rotasi kunci layanan.** “Environment service key” (kunci layanan lingkungan), yaitu `ANTHROPIC_ENVIRONMENT_KEY`, mengotorisasi polling antrean kerja lingkungan Anda dan pengiriman hasil kembali ke sesi. Simpan kunci ini di pengelola rahasia, bukan di file environment atau image sandbox. Rotasi segera jika Anda mencurigai adanya kebocoran.

* **Isolasi beban kerja yang tidak tepercaya.** Kunci layanan lingkungan dibatasi cakupannya pada antrean kerja satu lingkungan. Jika Anda menjalankan kode yang tidak tepercaya di dalam sandbox Anda, pertimbangkan untuk menyediakan workspace dan lingkungan terpisah untuk setiap batas kepercayaan. Dengan cara ini, setiap kunci hanya menjangkau sesi dalam satu batas kepercayaan, seperti sesi satu pengguna, bukan setiap sesi dalam lingkungan bersama.

* **Kredensial per sesi.** Setiap item pekerjaan yang diklaim oleh worker Anda dapat membawa `secret` (csharp, go: `Secret`) per sesi, yang digunakan worker sebagai pengganti kunci layanan lingkungan. Akses ke [memory store](https://platform.claude.com/docs/id/managed-agents/memory) memerlukan `secret` (csharp, go: `Secret`): endpoint memory store menolak kunci layanan lingkungan (lihat [Meneruskan secret item pekerjaan](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-per-session#forward-the-work-items-secret)). Teruskan `secret` (csharp, go: `Secret`) hanya ke sandbox yang melayani sesi tersebut, jauhkan dari image dan volume bersama, dan jangan pernah mencatatnya di log.

* **Radius dampak eksekusi alat.** Alat berjalan di dalam sandbox Anda dengan izin apa pun yang dimiliki proses Anda. Terapkan prinsip hak akses minimal pada pengguna proses dan mount hanya direktori yang dibutuhkan alat Anda.

* **Retensi log dan konten sesi.** Konten percakapan dan output alat melewati worker Anda dan tetap berada di lingkungan Anda. Anda bertanggung jawab untuk menyimpan, menyunting (redact), atau menghapus data tersebut sesuai dengan kebijakan Anda sendiri. Anthropic tidak memiliki visibilitas terhadap apa yang dilakukan worker Anda dengan konten sesi setelah dikirimkan.

* **Isi memory store.** Anthropic meng-host [memory store](https://platform.claude.com/docs/id/managed-agents/memory), termasuk riwayat versinya. Ketika sebuah sesi melampirkan memory store, worker menyimpan salinan kerja di bawah `/mnt/memory/` di sandbox Anda selama worker melayani sesi tersebut dan menyinkronkan perubahan kembali. Worker menghapus salinan tersebut saat selesai menangani sesi (lihat [Cara worker menangani memori](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-memory#how-the-worker-handles-memory)). Worker yang keluar tanpa menjalankan proses teardown-nya akan meninggalkan salinan tersebut. Pembersihan salinan yang tertinggal, izin pada path tersebut, dan isolasi antarsesi yang berbagi sistem file merupakan tanggung jawab Anda.

* **Memory store read-only.** Store yang dilampirkan dengan akses `read_only` dilindungi dari pengunggahan, bukan dari modifikasi lokal.

  * **Yang diblokir:** Alat `write` dan `edit` milik worker menolak menulis di bawah direktori store tersebut. Worker tidak mengunggah apa pun dari direktori tersebut. Endpoint memory store menolak permintaan yang menggunakan `secret` (csharp, go: `Secret`) sesi untuk menulis ke store tersebut.
  * **Yang tidak diblokir:** Perintah yang dijalankan agen melalui alat `bash` dapat mengubah salinan lokal. Begitu pula [alat kustom](https://platform.claude.com/docs/id/managed-agents/self-hosted-sandboxes-custom-tools) atau server MCP yang Anda sajikan dari sandbox, yang berjalan dengan izin worker.
  * **Apa yang terjadi pada file yang diubah:** Selama worker melayani sesi tersebut, panggilan alat berikutnya membaca file yang telah diubah. Worker tidak memulihkannya dengan sendirinya. Jika file tersebut mendapatkan versi baru di store selama waktu itu, sinkronisasi berikutnya oleh worker akan menimpa file lokal dengan versi tersebut.
  * **Cara mencegah perubahan lokal juga:** Nonaktifkan alat `bash` untuk agen tersebut, dan jangan berikan alat kustom atau server MCP apa pun yang menulis ke sistem file sandbox.

## Apa yang tidak dapat dilakukan Anthropic untuk Anda

* **Mengetahui bahwa kunci Anda bocor.** Anthropic dapat mendeteksi pola penggunaan yang anomali, tetapi tidak dapat mengetahui bahwa kunci Anda telah disusupi. Jika Anda mencurigai `ANTHROPIC_ENVIRONMENT_KEY` bocor, cabut kunci tersebut dan buat penggantinya segera. Pencabutan divalidasi pada setiap permintaan, sehingga berlaku pada panggilan worker berikutnya.
* **Memverifikasi build worker Anda.** Anthropic tidak memeriksa image sandbox atau runtime Anda. Kompromi rantai pasokan (supply-chain) pada image Anda tidak dapat dideteksi dari sisi Anthropic.
* **Mengisolasi alat di dalam sandbox Anda.** Batas keamanan Anthropic berhenti di sandbox. Cara Anda mengisolasi eksekusi alat individual satu sama lain di dalam batas tersebut sepenuhnya merupakan tanggung jawab Anda.
* **Menegakkan retensi data di lingkungan Anda.** Setelah konten sesi mencapai worker Anda, konten tersebut berada di luar kontrol siklus hidup data Anthropic.
