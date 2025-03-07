# คู่มือการใช้งาน

## การสร้าง route

ต้องสร้างไฟล์ `page.py` ในโฟลเดอร์ `routers` หรือ `routers/<app_name>`:

จากนั่นสร้างฟังก์ชัน `page` ในไฟล์ `page.py` ดังนี้:

```python
from django.shortcuts import render

def page(request):
    """home"""
    # document สำหรับกำหนดชื่อ path

    return render(request, 'page.html')
```

หรือ

```python
from store.core.routers import render

def page(request):
    """home"""

    context = {}
    return render(request, context)
```

ผลลัพธ์:

```python
path('', page, name='home')
```

### การสร้าง route ที่มี parameter

| Route                           | Example URL | params        |
| ------------------------------- | ----------- | ------------- |
| `routers/page.py`               | `/`         | `{}`          |
| `routers/info/page.py`          | `/info/`    | `{}`          |
| `routers/(group)/about/page.py` | `/about/`   | `{}`          |
| `routers/user/[slug]/page.py`   | `/user/1/`  | `{'slug': 1}` |

### ตัวอย่างโครงสร้างโฟลเดอร์

```
myapp
├── migrations
│   └── __init__.py
├── routers
│   ├── (auth)
│   │   ├── login
│   │   │   ├── page.html
│   │   │   └── page.py
│   │   └── register
│   │       ├── page.html
│   │       └── page.py
│   ├── info
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

ปล. ได้รับแรงบันดาลใจจาก **[Next.js App Router](https://nextjs.org/docs/app)**

## การกำหนด Metadata

จำเป็นต้องใช้ render ของ `store.core.routers` แทน `django.shortcuts.render` เพื่อใช้งาน metadata ได้

ตัวอย่างการใช้งาน metadata:

```python
from store.core.metadata import Metadata
from store.core.routers import render

def page(request):
    metadata = Metadata(title='นโยบายความเป็นส่วนตัว')
    return render(request, metadata=metadata)
```

หรือ

```python
from store.core.routers import render
from store.metadata import metadata

@metadata(title='นโยบายความเป็นส่วนตัว')
def page(request):
    return render(request)
```

ผลลัพธ์ ในไฟล์ `page.html`:

```html
<title>นโยบายความเป็นส่วนตัว</title>
```

ตัวอย่างการใช้งาน metadata แบบมี string format และ ต้องส่งค่าเข้าผ่าน context

```python
from store.core.routers import render
from store.metadata import metadata
from store.models import Product

# Product title='Suzume', description='17-year-old high school girl ...'

@metadata(
    title='{product.title}',
    og_title='{product.title}',
    og_description='{product.description}',
)
def page(request, product_id):
    """product-detail"""

    product = Product.objects.get(id=product_id)
    context = {
        'product': product,
    }
    return render(request, context)
```

ผลลัพธ์ ในไฟล์ `page.html`:

```html
<title>Suzume</title>
<meta property="og:title" content="Suzume" />
<meta property="og:description" content="17-year-old high school girl ..." />
```
