import datetime
from sqlalchemy import DateTime
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs
)
from sqlalchemy.orm import DeclarativeBase

class BaseEntity(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),
    }