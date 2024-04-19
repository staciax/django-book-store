import re
from datetime import datetime

from django.utils import timezone


# inspired by https://gist.github.com/silkyland/004e9c74ed9ed8b76d613bc2e4e48f52
def to_thai_slug(text: str) -> str:
    slug = re.sub(r'\s+', '-', text)
    slug = re.sub(r'\(|\)', '', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    slug = slug.lower()

    return slug


def build_media_filename(
    upload_filename: str,
    *,
    prefix: str | None = None,
    with_timestamp: bool = True,
) -> str:
    filename = upload_filename

    if prefix:
        filename = f'{prefix}_{filename}'

    if with_timestamp:
        tz_now = datetime.now(timezone.get_default_timezone())
        timestamp = tz_now.strftime('%Y%m%d%H%M%S')
        filename = f'{timestamp}_{filename}'

    filename = filename.lower().replace(' ', '_').replace('-', '_').replace('__', '_')

    return filename
