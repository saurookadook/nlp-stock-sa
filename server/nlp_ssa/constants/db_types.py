from sqlalchemy.dialects import postgresql

from db.db import Base
from constants import SentimentEnum, SourceDiscriminatorEnum

SentimentEnumDB = postgresql.ENUM(
    SentimentEnum,
    values_callable=lambda e: [x.value for x in e],
    name=SentimentEnum.db_type_name(),
    metadata=Base.metadata,
)

SourceDiscriminatorEnumDB = postgresql.ENUM(
    SourceDiscriminatorEnum,
    values_callable=lambda e: [x.value for x in e],
    name=SourceDiscriminatorEnum.db_type_name(),
    metadata=Base.metadata,
)
