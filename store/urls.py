from . import views as views
from store.core.routers import AppRouter
from store.core.views import view_router

router = AppRouter()
router.include_app('store')

urlpatterns = []

urlpatterns += router.urls
urlpatterns += view_router.urls

# for url in sorted(urlpatterns, key=lambda a: str(a.pattern)):
#     view_name = (url.callback.__doc__ or url.callback.__name__).replace('-', '_')
#     print(f"path('{url.pattern}', views.{view_name}, name='{url.name}'),")
