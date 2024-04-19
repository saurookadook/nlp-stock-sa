#!/usr/bin/env python3

import arrow
import csv
import os
from sqlalchemy import insert

from db import db_session
from models.stock import StockDB
from models.user import UserDB

window_width, _ = os.get_terminal_size()

users = [
    {
        "first_name": "Andrea",
        "last_name": "Ovalle",
        "username": "ovalle15",
        "email": "andrea.ovalle1990@gmail.com",
    },
    {
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

    print(" Seeding stocks from stocks_seed_data.csv... ".center(window_width, "-"))
    with open("nlp_ssa/seed_data/stocks_seed_data.csv", newline="") as stocks_csv:
        dict_reader = csv.DictReader(stocks_csv)
        for row in dict_reader:
            print(row)
            local_db_session.execute(
                insert(StockDB).values(
                    **row, created_at=arrow.now(), updated_at=arrow.now()
                )
            )
        local_db_session.commit()


if __name__ == "__main__":
    seed_db()
