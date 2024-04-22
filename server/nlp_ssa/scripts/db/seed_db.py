#!/usr/bin/env python3

import arrow
import csv
import os
from sqlalchemy import insert
from uuid import UUID, uuid4

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


def seed_db():
    local_db_session = db_session()

    print(" Seeding stocks from stocks_seed_data.csv... ".center(window_width, "-"))
    for user in users:
        local_db_session.execute(
            insert(UserDB).values(
                **user, created_at=arrow.now(), updated_at=arrow.now()
            )
        )
        local_db_session.commit()

    print(" Seeding stocks from mixed_seed_data.csv... ".center(window_width, "-"))
    with open("nlp_ssa/seed_data/mixed_seed_data.csv", newline="") as stocks_csv:
        dict_reader = csv.DictReader(stocks_csv)
        for row in dict_reader:
            from rich import inspect

            inspect(row, sort=True)

            print(
                f" Creating Stock record for {row['QuoteStockSymbol']} ".center(
                    window_width, "-"
                )
            )
            stock_dict = dict(
                id=uuid4(),
                quote_stock_symbol=row["QuoteStockSymbol"],
                full_stock_symbol=row["FullStockSymbol"],
                source_group_id=row["SourceGroupID"],
                created_at=arrow.get(row["CreatedAt"]).to("utc"),
            )

            local_db_session.execute(
                insert(StockDB).values(**stock_dict, updated_at=arrow.utcnow())
            )
            local_db_session.commit()

            print(
                f" Creating SentimentAnalysis record for {row['QuoteStockSymbol']} ".center(
                    window_width, "-"
                )
            )
            sentiment_analysis_record = dict(
                id=uuid4(),
                quote_stock_symbol=row["QuoteStockSymbol"],
                score=row["Score"],
                sentiment=row["Sentiment"],
                # output=row["Output"],
                source_group_id=row["SourceGroupID"],
                created_at=arrow.get(row["CreatedAt"]).to("utc"),
            )

            local_db_session.execute(
                insert(SentimentAnalysisDB).values(
                    **sentiment_analysis_record, updated_at=arrow.utcnow()
                )
            )
            local_db_session.commit()

            print(
                f" Creating AnalysisView record for source_group_id {row['SourceGroupID']} and user {row['UserId']} ".center(
                    window_width, "-"
                )
            )
            analysis_view_dict = dict(
                id=uuid4(),
                source_group_id=row["SourceGroupID"],
                user_id=row["UserID"],
                created_at=arrow.get(row["CreatedAt"]).to("utc"),
            )

            local_db_session.execute(
                insert(AnalysisViewDB).values(
                    **analysis_view_dict, updated_at=arrow.utcnow()
                )
            )
            local_db_session.commit()


if __name__ == "__main__":
    seed_db()
