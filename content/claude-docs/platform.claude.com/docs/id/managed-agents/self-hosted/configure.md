---
source: platform
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/configure
fetched_at: 2026-11-13T02:11:44.788783Z
sha256: efbf6f594ae0aac5ba20fa602adef19a2225dda38c130613fca05b7f1aa467cd
---

---
title: Single sign-on
url: https://platform.claude.com/docs/id/managed-agents/self-hosted/configure
description: Izinkan orang dan layanan memanggil server Claude Managed Agents yang di-host sendiri dengan token dari penyedia identitas Anda.
---

<Note>
  Untuk meminta akses ke Claude Managed Agents yang di-host sendiri, hubungi tim akun Anthropic Anda.
</Note>

Secara default, server Anda menerima satu kunci bersama, yaitu [kunci API server](https://platform.claude.com/docs/id/managed-agents/self-hosted#the-three-credentials). Dengan “single sign-on” (masuk tunggal), setiap orang atau layanan juga dapat memanggil server dengan token dari penyedia identitas OpenID Connect (OIDC) Anda. Server memberikan peran kepada pemanggil berdasarkan grup di dalam token. Kunci API server tetap berfungsi sebagai kredensial administrator.

Halaman ini menunjukkan cara menambahkan penyedia identitas Anda, apa yang dapat dilakukan setiap peran, dan cara mengizinkan developer login dari terminal.

## Menambahkan penyedia identitas Anda

<Steps>
  <Step title="Daftarkan server di penyedia identitas Anda">
    Daftarkan server sebagai API dengan pengidentifikasi seperti `api://cma-server`, dan minta klien untuk meminta token untuknya.
  </Step>

  <Step title="Cantumkan penyedia identitas di file pengaturan">
    Tambahkan entri di bawah `auth.issuers` di [file pengaturan](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#where-settings-go):

    ```yaml
    auth:
      issuers:
        - name: okta
          issuer_url: https://login.example.com/oauth2/default
          audiences: [api://cma-server]
          roles:
            - group: cma-admins
              role: admin
            - group: "eng-*"
              role: developer
    ```

    * `name` memberi label pada issuer di baris log, dan server mencatatnya sebagai bagian dari pembuat setiap resource. Jangan mengubahnya setelah orang-orang membuat resource.
    * `issuer_url` harus sama dengan klaim `iss` pada token Anda.
    * `audiences` mencantumkan nilai yang dapat dibawa oleh klaim `aud` sebuah token, seperti pengidentifikasi dari langkah pertama.
    * `roles` memetakan sebuah grup ke `admin`, `developer`, atau `user`. Peran tertinggi yang cocok yang berlaku.

    Untuk field lainnya, lihat [Entri issuer](https://platform.claude.com/docs/id/managed-agents/self-hosted/configuration-reference#issuer-entries). Jika penyedia Anda adalah Microsoft Entra ID, lihat juga [Microsoft Entra ID](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#microsoft-entra-id).
  </Step>

  <Step title="Mulai ulang server dan periksa sign-in">
    Mulai ulang server. Pemanggil mengirim token sebagai `Authorization: Bearer <token>`, pada rute mana pun yang menerima kunci API server.

    Untuk setiap permintaan yang diautentikasi oleh token, server mencatat `auth=oidc`, `name` issuer, dan subjek pemanggil (`sub=`).
  </Step>
</Steps>

### Jika sign-in gagal

| Respons                                        | Penyebab                                                   | Baris log server berisi |
| ---------------------------------------------- | ---------------------------------------------------------- | ----------------------- |
| `401`, sama seperti untuk kunci API yang salah | Token gagal dalam pemeriksaan. Baris log memuat alasannya. | `oidc token`            |
| `403`                                          | Grup token tidak cocok dengan entri `roles` mana pun       | `token holds no role`   |

### Microsoft Entra ID

Entra ID berbeda dari penyedia lain dalam dua hal. Kedua pengaturan dimasukkan ke dalam entri issuer:

* **Orangnya:** Entra ID memberikan `sub` yang berbeda kepada seseorang di setiap aplikasi klien, sehingga pengaturan default akan mencatat satu orang sebagai beberapa pembuat. Atur `subject_claim: oid`.
* **Grupnya:** Entra ID menghilangkan klaim `groups` dari token jika orang tersebut menjadi anggota banyak grup. Orang tersebut kemudian tidak cocok dengan entri `roles` mana pun. Untuk mencegah hal ini, minta Entra ID mengeluarkan hanya grup yang ditetapkan ke aplikasi. Atau tetapkan app role kepada orang-orang di Entra ID, dan atur `groups_claim: roles` agar server membaca app role sebagai pengganti grup.

## Apa yang dapat dilakukan setiap peran

| Peran                         | Agen, skill, sesi, vault, dan memory store                         | Environment                                                   |
| ----------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------- |
| `admin`, dan kunci API server | Melihat dan mengubah semuanya                                      | Membuat, mengubah, dan menghapusnya, serta membuat kuncinya   |
| `developer` atau `user`       | Melihat dan mengubah hanya apa yang dibuat oleh pemanggil tersebut | Mencantumkannya, membacanya, dan menjalankan sesi di dalamnya |

`developer` dan `user` memiliki akses yang sama. Pemanggil dengan salah satu peran tersebut:

* **Tidak dapat melihat resource yang dibuat oleh orang lain.** Resource tersebut tidak muncul dalam daftar, dan permintaan untuk ID-nya mendapatkan respons yang sama seperti permintaan untuk ID yang tidak dikenal. Hal ini mencakup semua yang dibuat dengan kunci API server sebelum Anda mengaktifkan single sign-on.
* **Tidak dapat membagikan resource** dengan pemanggil lain atau grup.

Petakan `admin` ke nama grup yang persis. Seorang administrator juga dapat memulai sesi yang menggunakan vault milik pengguna mana pun. Jadi berikan peran tersebut hanya kepada grup yang Anda percayai untuk memegang token MCP setiap pengguna.

## Mengizinkan developer login dari terminal

Developer dapat login melalui penyedia identitas Anda lalu menggunakan CLI `ant` dengan identitas mereka sendiri, tanpa kunci API server. Anda melakukan dua langkah pertama, dan setiap developer melakukan langkah ketiga.

<Steps>
  <Step title="Daftarkan aplikasi di penyedia identitas Anda">
    Daftarkan aplikasi native (“publik”) dengan pengaturan berikut:

    * Tanpa client secret
    * Grant kode otorisasi beserta PKCE
    * Redirect URI `http://127.0.0.1/callback`

    Beberapa penyedia memerlukan salah satu dari [redirect URI lainnya](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#other-redirect-uris).
  </Step>

  <Step title="Tambahkan aplikasi ke entri issuer">
    Tambahkan `login_client_id` dan `login_scopes` ke entri issuer, lalu mulai ulang server:

    ```yaml
    login_client_id: 0oa1b2c3d4e5f6g7h8i9
    login_scopes: [openid, cma-server.access]
    ```

    `login_scopes` mencantumkan scope yang dibutuhkan penyedia Anda untuk menerbitkan token yang klaim `aud`-nya ada di daftar `audiences` entri issuer.
  </Step>

  <Step title="Login">
    Setiap developer menjalankan login dari tingkat teratas arsip yang diekstrak:

    ```bash
    ./cma-server-admin login https://cma.example.com
    ```

    URL server harus menggunakan `https://`, atau `http://` ke `localhost`, `127.0.0.1`, atau `::1`. Dengan salah satu dari [redirect URI lainnya](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#other-redirect-uris), tambahkan flag-nya ke perintah.

    Perintah tersebut membuka halaman sign-in penyedia di browser lalu menulis profil CLI `ant` bernama `cma-server`. Berikan `--profile cma-server` ke perintah `ant` mana pun, atau jalankan `ant profile activate cma-server` untuk menjadikan profil tersebut sebagai default.
  </Step>
</Steps>

Ketika token kedaluwarsa, developer menjalankan `login` lagi. Agar CLI `ant` yang memperbarui token sebagai gantinya, tambahkan `offline_access` ke `login_scopes`.

### Redirect URI lainnya

| Penyedia                                      | Redirect URI yang didaftarkan                                   | Flag yang ditambahkan developer ke perintah `login` |
| --------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------- |
| Microsoft Entra ID                            | `http://localhost/callback`                                     | `-listen localhost:0`                               |
| Penyedia yang mewajibkan port di redirect URI | URI dengan port tetap, seperti `http://127.0.0.1:8123/callback` | `-listen 127.0.0.1:8123`                            |

Untuk mencantumkan flag lainnya, tambahkan `-h` ke perintah `login`.

## Mengizinkan orang sign in ke konsol di server Anda

Konsol di server Anda membuat orang melakukan sign-in melalui aplikasi yang Anda daftarkan untuk [login terminal](https://platform.claude.com/docs/id/managed-agents/self-hosted/configure#let-developers-log-in-from-a-terminal). Untuk menyelesaikan penyiapannya, lihat [Menyiapkan sign-in](https://platform.claude.com/docs/id/managed-agents/self-hosted/console#set-up-sign-in).
