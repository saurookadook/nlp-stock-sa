#!/usr/bin/env python3

import arrow
import csv
import os
from sqlalchemy import delete, literal_column
from sqlalchemy.dialects.postgresql import insert
from uuid import UUID, uuid4
from rich import inspect

from db import db_session
from models.analysis_view import AnalysisViewDB
from models.sentiment_analysis import SentimentAnalysisDB
from models.stock import StockDB
from models.user import UserDB

window_width, _ = os.get_terminal_size()

users = [
    {
        "id": UUID("e3777f01-48f2-43a5-8448-a7f6aecb1b34"),
        "first_name": "Andrea",
        "last_name": "Ovalle",
        "username": "ovalle15",
        "email": "andrea.ovalle1990@gmail.com",
    },
    {
        "id": UUID("863cc20f-758a-4de8-ab92-04f1909a1014"),
        "first_name": "Andy",
        "last_name": "Maskiell",
        "username": "saurookadook",
        "email": "maskiella@gmail.com",
    },
]


def insert_or_update(db_session, DBModel, col_values):
    insert_stmt = insert(DBModel.__table__).values(**col_values)
    full_stmt = insert_stmt.on_conflict_do_update(
        constraint=DBModel.__table__.primary_key,
        set_={
            **col_values,
            "updated_at": arrow.utcnow(),
        },
    )
    # ).returning(literal_column("*"))
    db_session.execute(full_stmt)


def seed_db():
    local_db_session = db_session()
    # local_db_session.execute(delete(AnalysisViewDB))
    # local_db_session.execute(delete(SentimentAnalysisDB))
    # local_db_session.execute(delete(StockDB))
    # local_db_session.execute(delete(UserDB))
    # local_db_session.flush()

    print(" Seeding users... ".center(window_width, "-"))
    for user in users:
        insert_or_update(
            db_session=local_db_session,
            DBModel=UserDB,
            col_values=dict(
                **user,
                created_at=arrow.utcnow(),
                updated_at=arrow.utcnow(),
            ),
        )
        local_db_session.commit()

    print(" Seeding stocks from mixed_seed_data.csv... ".center(window_width, "-"))
    with open(
        "nlp_ssa/scripts/db/seeding/seed_data/mixed_seed_data.csv", newline=""
    ) as stocks_csv:
        dict_reader = csv.DictReader(stocks_csv)
        for row in dict_reader:
            try:
                inspect(row, sort=True)

                # TODO: need to parse 4/15/2024 as date and/or transform it to a supported date format

                print(
                    f" Creating Stock record for {row['QuoteStockSymbol']} ".center(
                        window_width, "-"
                    )
                )
                stock_dict = dict(
                    id=uuid4(),
                    quote_stock_symbol=row["QuoteStockSymbol"],
                    full_stock_symbol=row["FullStockSymbol"],
                    created_at=arrow.get(row["CreatedAt"]).to("utc"),
                )

                insert_or_update(
                    db_session=local_db_session,
                    DBModel=StockDB,
                    col_values=dict(
                        **stock_dict,
                        updated_at=arrow.utcnow(),
                    ),
                )
                local_db_session.commit()

                print(
                    f" Creating SentimentAnalysis record for {row['QuoteStockSymbol']} ".center(
                        window_width, "-"
                    )
                )
                sentiment_analysis_dict = dict(
                    id=uuid4(),
                    quote_stock_symbol=row["QuoteStockSymbol"],
                    source_group_id=UUID(row["SourceGroupID"]),
                    score=row["Score"],
                    sentiment=row["Sentiment"].lower().strip(),
                    # output=row["Output"],
                    created_at=arrow.get(row["CreatedAt"]).to("utc"),
                )

                insert_or_update(
                    db_session=local_db_session,
                    DBModel=SentimentAnalysisDB,
                    col_values=dict(
                        **sentiment_analysis_dict,
                        updated_at=arrow.utcnow(),
                    ),
                )
                local_db_session.commit()

                print(
                    f" Creating AnalysisView record for source_group_id {row['SourceGroupID']} and user {row['UserID']} ".center(
                        window_width, "-"
                    )
                )
                analysis_view_dict = dict(
                    id=uuid4(),
                    source_group_id=UUID(row["SourceGroupID"]),
                    user_id=UUID(row["UserID"]),
                    created_at=arrow.get(row["CreatedAt"]).to("utc"),
                )

                insert_or_update(
                    db_session=local_db_session,
                    DBModel=AnalysisViewDB,
                    col_values=dict(
                        **analysis_view_dict,
                        updated_at=arrow.utcnow(),
                    ),
                )
                local_db_session.commit()
            except Exception as e:
                inspect(e)
                # db_session.commit()
                breakpoint()


if __name__ == "__main__":
    seed_db()
