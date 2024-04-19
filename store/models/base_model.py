from django.db import models
from django.db.models.functions import Now


class BaseModel(models.Model):
    id: int

    class Meta:
        abstract = True


class TimestampModel(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True, db_default=Now())  # pyright: ignore[reportCallIssue]
    updated_at = models.DateTimeField(auto_now=True, db_default=Now())  # pyright: ignore[reportCallIssue]

    class Meta:
        abstract = True
