#!/usr/bin/env python3

import arrow
import csv
import logging
from uuid import uuid4
from rich import inspect

from db import db_session
from models.stock import StockFacade

logger = logging.getLogger(__file__)


def seed_stocks():
    local_db_session = db_session()

    logger.log_info_centered(" Seeding stocks from 'stocks_seed_data.csv'... ")
    with open(
        "nlp_ssa/scripts/db/seeding/seed_data/stocks_seed_data.csv", newline=""
    ) as stocks_csv:
        stock_facade = StockFacade(db_session=db_session)

        dict_reader = csv.DictReader(stocks_csv)
        for row in dict_reader:
            try:
                inspect(row, sort=True)

                logger.log_info_centered(
                    f" Creating Stock record for {row.get('QuoteStockSymbol')} "
                )

                stock_facade.create_or_update(
                    payload=dict(
                        id=uuid4(),
                        quote_stock_symbol=row.get("QuoteStockSymbol"),
                        full_stock_symbol=row.get("FullStockSymbol"),
                        exchange_name=row.get("ExchangeName"),
                        created_at=(
                            arrow.get(row.get("CreatedAt")).to("utc")
                            if row.get("CreatedAt") is not None
                            else arrow.utcnow()
                        ),
                        updated_at=arrow.utcnow(),
                    )
                )
                local_db_session.commit()
            except Exception as e:
                inspect(e)
                # db_session.commit()
                breakpoint()


if __name__ == "__main__":
    seed_stocks()
