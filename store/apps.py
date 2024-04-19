import logging

from django.apps import AppConfig

log = logging.getLogger(__name__)


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    verbose_name = 'store'

    def ready(self) -> None:
        from .core.metadata import set_global_metadata
        from .metadata import metadata

        set_global_metadata(metadata)
        log.info('store app ready')
