---
source: platform
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-amazon-bedrock
fetched_at: 2026-11-24T02:13:59.956186Z
sha256: ee527ae1c5754c602f0b4086e4608abea1c90611801d9d39017b8d7d4ed19d4e
---

---
title: Enterprise Frontier Safeguards di Amazon Bedrock
url: https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/setup-amazon-bedrock
description: Temukan panduan penyiapan dari AWS untuk Enterprise Frontier Safeguards di Amazon Bedrock.
---

Untuk menggunakan [Enterprise Frontier Safeguards](https://platform.claude.com/docs/id/manage-claude/enterprise-frontier-safeguards/overview) (EFS) di Amazon Bedrock, Anda mendapatkan akses dan menyiapkannya melalui AWS, bukan di Claude Console. EFS di Bedrock masih dalam tahap beta.

<Warning>
  EFS baru aktif setelah Anda menghubungkan bucket Amazon S3 milik Anda sendiri, meskipun Bedrock sudah menampilkan EFS sebagai `enabled`. Sampai saat itu, Bedrock menyimpan salinan prompt dan respons Anda di penyimpanan yang dikelola AWS, dan penyiapan tersebut bukan EFS.
</Warning>

Untuk menyiapkan EFS, ikuti [panduan penyiapan dari AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/anthropic-efs-enterprise-data-controls.html). Gunakan panduan tersebut juga untuk penyimpanan, kunci, dan Safety Cases, karena halaman-halaman lain dalam panduan ini menjelaskan Claude Console.

Selama masa beta, beberapa kontrol dan retensi data di Bedrock dapat berbeda dari yang dijelaskan dalam panduan ini. Tanyakan detailnya kepada AWS.
