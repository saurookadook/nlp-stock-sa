from sqlalchemy import ForeignKey, event
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Union
from uuid import UUID


from constants.db_types import SourceDiscriminatorEnum, SourceDiscriminatorEnumDB
from db import Base
from models.mixins.db import TimestampsDB


class SourceDB(TimestampsDB, Base):
    """`Source` entities establish a polymorphic relationship between `SentimentAnalysis` entities \
        and specific data entities, such as `ArticleData`.
    """

    from models.article_data.db import ArticleDataDB

    __tablename__ = "sources"

    data_type: Mapped[SourceDiscriminatorEnum] = mapped_column(
        SourceDiscriminatorEnumDB,
        nullable=False,
    )
    data_type_id: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), nullable=False, unique=True
    )

    # data: Mapped[Union[ArticleDataDB]] = relationship(
    #     back_populates="polymorphic_source", uselist=False
    # )
    source_owner_name: Mapped[str] = mapped_column(nullable=True)

    sentiment_analysis: Mapped["SentimentAnalysisDB"] = relationship(
        "SentimentAnalysisDB", back_populates="source", uselist=False
    )
