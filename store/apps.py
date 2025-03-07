import logging

from django.apps import AppConfig

log = logging.getLogger(__name__)


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    verbose_name = 'store'

    def ready(self) -> None:
        # NOTE: avoid circular import
        from .core.metadata import set_global_metadata  # noqa: PLC0415
        from .metadata import metadata  # noqa: PLC0415

        set_global_metadata(metadata)
        log.info('store app ready')
