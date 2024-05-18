import gzip
import json
from rich import inspect

from db import db_session


def populate_db():
    f = gzip.open("nlp_ssa/scripts/db/states/db_state.json.gz", "rb")
    data = json.loads(f.decode("utf-8"))
    inspect(data, all=True)
    pass


if __name__ == "__main__":
    populate_db()
