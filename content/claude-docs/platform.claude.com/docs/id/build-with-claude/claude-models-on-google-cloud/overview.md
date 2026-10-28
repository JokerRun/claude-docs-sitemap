---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/overview
fetched_at: 2026-10-28T02:15:32.412922Z
sha256: a5a6a0364af3368702711905ed47110d226e5af3fcd22778aba1d14d10f0e7e6
---

---
title: Claude Models on Google Cloud
url: https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/overview
description: Bandingkan Claude Models on Google Cloud (Anthropic managed) dan Claude Models on Google Cloud (Google managed), serta cari tahu mana yang Anda gunakan.
---

Anda dapat menggunakan Claude melalui proyek Google Cloud Anda dengan dua cara:

* **[Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed):** Anthropic mengoperasikan [Claude API](https://platform.claude.com/docs/id/api/overview).
* **[Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed):** Google mengoperasikan model Claude sebagai bagian dari Google Cloud’s Agent Platform.

## Perbedaan kedua penawaran Google Cloud

Tabel berikut membandingkan Claude Models on Google Cloud (Anthropic managed) dengan Claude Models on Google Cloud (Google managed).

| Aspek                                            | [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed)                                                     | [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed)                                                                                                  |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Permukaan API**                                | Endpoint Claude API<br />`/v1/{endpoint}`                                                                                                                                                                      | Endpoint prediksi Agent Platform                                                                                                                                                                                                                      |
| **Format permintaan**                            | Sama seperti Claude API<br />`model` di badan permintaan<br />Header `anthropic-version`                                                                                                                       | `model` di URL<br />`anthropic_version` di badan permintaan                                                                                                                                                                                           |
| **Streaming**                                    | `"stream": true` di badan permintaan                                                                                                                                                                           | Endpoint `:streamRawPredict` terpisah                                                                                                                                                                                                                 |
| **Lokasi**                                       | `global`<br />Lihat [Resolusi proyek, lokasi, dan workspace](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#project-location-and-workspace-resolution). | Endpoint global, multi-region, atau regional<br />Lihat [Endpoint global, multi-region, dan regional](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#global-multi-region-and-regional-endpoints). |
| **ID model untuk model sebelum Claude 4.6**      | ID Claude API<br />Contoh: `claude-haiku-4-5-20251001`                                                                                                                                                         | ID Claude API, dengan `@` menggantikan tanda hubung sebelum tanggal snapshot<br />Contoh: `claude-haiku-4-5@20251001`<br />Lihat [ID model dan pembuatan versi](https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions).      |
| **Layanan yang perlu diaktifkan di proyek Anda** | Lihat [Siapkan akun Anda](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account).                                                          | Agent Platform API<br />`aiplatform.googleapis.com`                                                                                                                                                                                                   |
| **Organisasi Anthropic**                         | Organisasi Anthropic baru untuk proyek Anda                                                                                                                                                                    | Tidak ada                                                                                                                                                                                                                                             |
| **Penagihan**                                    | Google Cloud Marketplace                                                                                                                                                                                       | Google Cloud, sebagai penggunaan Agent Platform                                                                                                                                                                                                       |
| **Batas laju**                                   | Dikelola oleh Anthropic                                                                                                                                                                                        | Dikelola oleh Google Cloud                                                                                                                                                                                                                            |

## Kesamaan kedua penawaran

* **Kredensial:** Kedua penawaran menggunakan kredensial Google Cloud, termasuk Application Default Credentials. Anda memberikan akses ke setiap penawaran secara terpisah, melalui peran IAM masing-masing.

  * [Kredensial untuk Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#authentication)
  * [Kredensial untuk Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#before-making-api-calls)

* **Penagihan:** Biaya untuk kedua penawaran muncul di tagihan Google Cloud Anda.

  * [Penagihan untuk Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#billing)
  * [Penagihan untuk Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#billing)

* **ID model:** Model Claude 4.6 dan yang lebih baru menggunakan ID Claude API mereka di kedua penawaran. Lihat [ID model dan pembuatan versi](https://platform.claude.com/docs/id/about-claude/models/model-ids-and-versions).

* **SDK:** [SDK klien](https://platform.claude.com/docs/id/cli-sdks-libraries/overview) Anthropic mendukung kedua penawaran.

## Berpindah di antara kedua penawaran

Ikuti langkah-langkah untuk penawaran mana pun yang menjadi tujuan perpindahan Anda:

* [Langkah-langkah untuk berpindah ke Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#migrating-from-google-managed)
* [Langkah-langkah untuk berpindah ke Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed#migrating-from-anthropic-managed)

## Penawaran mana yang Anda gunakan?

Tabel berikut mencantumkan nilai-nilai yang mengidentifikasi Claude Models on Google Cloud (Anthropic managed) dan Claude Models on Google Cloud (Google managed). Temukan nilai yang sudah Anda miliki. Misalnya, cari host di URL permintaan Anda atau klien SDK di kode Anda. Judul kolom dari nilai tersebut adalah penawaran Anda.

| Yang perlu diperiksa                               | [Claude Models on Google Cloud (Anthropic managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed)                                                                                                                                | [Claude Models on Google Cloud (Google managed)](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed)                                                                                                                                                                                |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tujuan permintaan Anda**                         | `claude.googleapis.com`<br />URL menyertakan ID workspace Anda.<br />URL diakhiri dengan path Claude API, seperti `.../invoke/v1/messages`.                                                                                                                                               | Salah satu host Agent Platform berikut:<br />`aiplatform.googleapis.com`<br />`aiplatform.us.rep.googleapis.com`<br />`aiplatform.eu.rep.googleapis.com`<br />`{region}-aiplatform.googleapis.com`<br />Path URL berisi `.../publishers/anthropic/models/{model}`.<br />URL diakhiri dengan `:rawPredict` atau `:streamRawPredict`. |
| **Klien SDK di kode Anda**                         | `AnthropicGoogleCloud` (csharp: `AnthropicGoogleCloudClient`; go: `googlecloud.NewClient()`; java: `GoogleCloudBackend`; php: `Anthropic\GoogleCloud\Client`; ruby: `Anthropic::GoogleCloudClient`)<br />Di setiap SDK, nama klien mengandung `GoogleCloud` (semuanya huruf kecil di Go). | `AnthropicVertex` (csharp: `AnthropicVertexClient`; go: `vertex.WithGoogleAuth()`; java: `VertexBackend`; php: `Anthropic\Vertex\Client`; ruby: `Anthropic::VertexClient`)<br />Di setiap SDK, nama klien mengandung `Vertex` (semuanya huruf kecil di Go).                                                                         |
| **Peran IAM yang memberikan akses**                | `roles/claude.admin`<br />`roles/claude.user`<br />`roles/claude.viewer`                                                                                                                                                                                                                  | Peran IAM Agent Platform                                                                                                                                                                                                                                                                                                            |
| **Konsol manajemen**                               | Claude Console, di `platform.claude.com`<br />Anda membukanya dari konsol Google Cloud.                                                                                                                                                                                                   | Konsol Google Cloud                                                                                                                                                                                                                                                                                                                 |
| **Lokasi setiap penawaran di konsol Google Cloud** | Opsi berlabel **Anthropic managed**<br />Lihat [Siapkan akun Anda](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#set-up-your-account).                                                                                            | Model Claude di [Model Garden](https://cloud.google.com/model-garden)                                                                                                                                                                                                                                                               |

Jika Anda memanggil `api.anthropic.com` dengan kunci API, Anda tidak menggunakan satu pun dari kedua penawaran tersebut. Untuk memindahkan panggilan tersebut ke Claude Models on Google Cloud (Anthropic managed), lihat [Berpindah dari organisasi Anthropic yang sudah ada](https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed#moving-from-an-existing-anthropic-organization).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Claude Models on Google Cloud (Anthropic managed)" icon="cloud" href="https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/anthropic-managed">
    Siapkan akun Anda dan buat permintaan pertama Anda.
  </Card>

  <Card title="Claude Models on Google Cloud (Google managed)" icon="cloud" href="https://platform.claude.com/docs/id/build-with-claude/claude-models-on-google-cloud/google-managed">
    Instal SDK dan buat permintaan pertama Anda.
  </Card>

  <Card title="Izin IAM untuk Claude Models on Google Cloud (Anthropic managed)" icon="lock" href="https://platform.claude.com/docs/id/api/claude-models-on-google-cloud-anthropic-managed-iam-permissions">
    Cari izin, peran, dan jenis log audit.
  </Card>
</CardGroup>
