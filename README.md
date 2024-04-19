## ร้านหนังสือนิยาย อนิเมะ และ การ์ตูน

โปรเจค วิชา เว็ปโปรแกรมมิ่ง มีโจทย์ให้ทำเป็นเว็ปไซต์อะไรก็ได้ และ ใช้ต้้องเฟรมเวิร์ค Django ในการทำโปรเจค
เราได้ทำเป็นเว็ปไซต์ขายหนังสือนิยาย อนิเมะ และ การ์ตูน

> โปรเจคนี้ทำส่งวิชาเว็ปโปรแกรมมิ่งเท่านั่น ไม่ได้นำไปใช้จริงแต่อย่างใด

## ภาพตัวอย่าง

![site-preview](https://imgur.com/QqAhfNh.png)

<details>
  <summary>แสดงเพิ่มเติม</summary>
  <img src="https://imgur.com/3L6mhtK.png" alt="site-preview-2">
  <img src="https://imgur.com/7CNWtQl.png" alt="site-preview-3">
</details>

## ฟีเจอร์

- [x] สมาชิก
- [x] ค้นหาสินค้า
- [x] ตะกร้าสินค้า
- [x] ชำระเงิน
- [x] ประวัติการสั่งซื้อ

## Requirements

- [Python](https://www.python.org) 3.12+
- [Node.js](https://nodejs.org/en) 20+

## Environment Variables

สร้างไฟล์ .env ในโปรเจค และเพิ่ม Environment Variables ดังนี้

```py
DJANGO_SECRET_KEY='secret'
DJANGO_DEBUG='True'
DJANGO_ALLOWED_HOSTS='*'
DJANGO_CSRF_TRUSTED_ORIGINS='http://, https://'
PROMPTPAY_ID='0987654321'
POSTGRES_DB='database'
POSTGRES_USER='username'
POSTGRES_PASSWORD='password'
POSTGRES_HOST='hostname'
POSTGRES_PORT='5432'
```

## Setup

1. สร้าง Virtual Environment

```bash
python3 -m venv .venv
```

2. ติดตั้ง Package ที่จำเป็นสำหรับโปรเจค

```bash
# python package
make install
# node package
make node-install
```

3. เซ็ตอัพโปรเจค

```bash
make setup
```

4. รันโปรเจค

```bash
make run
```

## Setup for Development

1. ติดตั้ง Package ที่จำเป็นสำหรับโปรเจค

```bash
make dev-install
```

2. รันโปรเจค

```bash
make run
```

3. รัน tailwindcss ในโหมด watch

```bash
make tailwind-dev
```

<!-- TODO: windows setup -->
<!-- TODO: docker setup -->

<!-- ## Docker and Docker Compose

เริ่มต้นด้วย

```bash
make docker-setup
``` -->

## เว็ปไซต์ที่ใช้เป็นแรงบันดาลใจ

- [Phoenix Next](https://www.phoenixnext.com) :heart:
- [Animate BKK](https://animatebkk-online.com)
- [Naiin](https://www.naiin.com)
- [MEB Market](https://www.mebmarket.com)

# License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
