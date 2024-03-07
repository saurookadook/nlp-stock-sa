import arrow
import datetime


class ArrowType(arrow.Arrow):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if isinstance(value, arrow.Arrow):
            return value
        if not (isinstance(value, str) or isinstance(value, datetime.datetime)):
            raise TypeError(f"Value '{value}' must be instance of 'str' or 'datetime'.")
        return arrow.get(value)
