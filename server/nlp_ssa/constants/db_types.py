from sqlalchemy.dialects import postgresql

from db.db import Base
from constants import (
    AuthProviderEnum,
    SentimentEnum,
    SourceDiscriminatorEnum,
    TokenTypeEnum,
)

AuthProviderEnumDB = postgresql.ENUM(
    AuthProviderEnum,
    values_callable=lambda e: [x.value for x in e],
    name=AuthProviderEnum.db_type_name(),
    metadata=Base.metadata,
)

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

TokenTypeEnumDB = postgresql.ENUM(
    TokenTypeEnum,
    values_callable=lambda e: [x.value for x in e],
    name=TokenTypeEnum.db_type_name(),
    metadata=Base.metadata,
)
