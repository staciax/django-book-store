# User Guide

## Creating routes

You need to create a `page.py` file in the `routes` or `routes/<app_name>` folder:

Then create a `page` function in the `page.py` file as follows:

```python
from django.shortcuts import render

def page(request):
    """home"""
    # document for defining the path name
    
    return render(request, 'page.html')
```

Or

```python
from store.core.routers import render

def page(request):
    """home"""

    context = {}

    # template name is auto detected
    # it will look for page.html in the same directory as page.py
    return render(request, context)
```

Result:

```python
path('', page, name='home')
```

### Creating routes with parameters

| Route                                | Example URL | params        |
| ------------------------------------ | ----------- | ------------- |
| `[app]/routes/page.py`               | `/`         | `{}`          |
| `[app]/routes/info/page.py`          | `/info/`    | `{}`          |
| `[app]/routes/(group)/about/page.py` | `/about/`   | `{}`          |
| `[app]/routes/user/[slug]/page.py`   | `/user/1/`  | `{'slug': 1}` |

### Example folder structure

```
myapp
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

Note: Inspired by **[Next.js App Router](https://nextjs.org/docs/app)**

## Configuring Metadata

You need to use `store.core.routers` render instead of `django.shortcuts.render` to use metadata.

Example of using metadata:

```python
from store.core.metadata import Metadata
from store.core.routers import render

def page(request):
    metadata = Metadata(title='Privacy Policy')
    return render(request, metadata=metadata)
```

Or

```python
from store.core.routers import render
from store.metadata import metadata

@metadata(title='Privacy Policy')
def page(request):
    return render(request)
```

Result in `page.html`:

```html
<title>Privacy Policy</title>
```

Example of using metadata with string formatting that requires values passed through context:

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

Result in `page.html`:

```html
<title>Suzume</title>
<meta property="og:title" content="Suzume" />
<meta property="og:description" content="17-year-old high school girl ..." />
```
