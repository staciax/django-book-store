## Novel, Anime, and Comic Book Store

This is a Web Programming course project with the assignment to create any kind of website using the Django framework.
I developed a website for selling novels, anime, and comics.

<!-- > This project is only for the Web Programming course submission and is not intended for actual use. -->

## Preview Images

![site-preview](https://imgur.com/QqAhfNh.png)

<details>
  <summary>Show more</summary>
  <img src="https://imgur.com/3L6mhtK.png" alt="site-preview-2">
  <img src="https://imgur.com/7CNWtQl.png" alt="site-preview-3">
</details>

## Features

- [x] Membership
- [x] Product Search
- [x] Shopping Cart
- [x] Payment
- [x] Order History

## Requirements

- [Python](https://www.python.org) 3.12+
- [Node.js](https://nodejs.org/en) 20+

## Environment Variables

Create a .env file in the project and add the following Environment Variables:

```py
# django
DJANGO_SECRET_KEY='secret'
DJANGO_DEBUG='True'
DJANGO_ALLOWED_HOSTS='*'
DJANGO_CSRF_TRUSTED_ORIGINS='http://, https://'

# payment
PROMPTPAY_ID='0987654321'

# postgres
POSTGRES_DB='database'
POSTGRES_USER='username'
POSTGRES_PASSWORD='password'
POSTGRES_HOST='hostname'
POSTGRES_PORT='5432'
```

## Setup

1. Create a Virtual Environment using uv

```bash
uv venv
```

2. Install necessary packages for the project

```bash
# python package with uv
uv sync

# node package (for tailwindcss, linting, formatting, etc.)
npm install
```

3. Setup the project

```bash
make setup
```

4. Run the project

```bash
make run
```

## Setup for Development

1. Run the project

```bash
make run
```

2. Run tailwindcss in watch mode

```bash
npm run dev
```

## Router (Like Next.js App Router)

for example, define a route with the file `page.py` in the `[app]/routes` folder:

```python
from django.shortcuts import render

def page(request):
    """home"""
    # You can also name the page
    # path(..., ..., name='home')

    context = {
        'x': 1,
    }

    return render(request, context)
```

| Route                                | Example URL | params        |
| ------------------------------------ | ----------- | ------------- |
| `[app]/routes/page.py`               | `/`         | `{}`          |
| `[app]/routes/info/page.py`          | `/info/`    | `{}`          |
| `[app]/routes/(group)/about/page.py` | `/about/`   | `{}`          |
| `[app]/routes/user/[slug]/page.py`   | `/user/1/`  | `{'slug': 1}` |

### Example folder structure

```
[app]
├── migrations
│   └── __init__.py
├── routes
│   ├── (auth)
│   │   ├── login
│   │   │   ├── page.html
│   │   │   └── page.py
│   │   └── register
│   │       ├── page.html
│   │       └── page.py
│   ├── info
│   │   └── page.html
│   │   └── page.py
│   ├── user
│   │   └── [user_id]
│   │       ├── page.html
│   │       └── page.py
│   ├── layout.html
│   ├── page.html
│   └── page.py
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── urls.py
└── views.py
```

<!-- TODO: windows setup -->
<!-- TODO: docker setup -->

<!-- ## Docker and Docker Compose

Start with

```bash
make docker-setup
``` -->

## Inspiration Websites

- [Phoenix Next](https://www.phoenixnext.com) :heart:
- [Animate BKK](https://animatebkk-online.com)
- [Naiin](https://www.naiin.com)
- [MEB Market](https://www.mebmarket.com)

# License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
