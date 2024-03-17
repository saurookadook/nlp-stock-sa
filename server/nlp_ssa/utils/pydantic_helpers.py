import arrow
import datetime
from arrow import Arrow
from pydantic import (
    GetCoreSchemaHandler,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
)
from pydantic.functional_validators import WrapValidator
from pydantic_core import core_schema
from typing import Annotated, Any


def convert_to_arrow_instance(
    value: str | datetime.datetime | Arrow,
    handler: ValidatorFunctionWrapHandler,
    info: ValidationInfo,
) -> Arrow:
    if isinstance(value, Arrow):
        return value
    if not (isinstance(value, str) or isinstance(value, datetime.datetime)):
        raise TypeError(f"Value '{value}' must be instance of 'str' or 'datetime'.")
    return arrow.get(value)


AnnotatedArrowType = Annotated[str, WrapValidator(convert_to_arrow_instance)]


# NOTE: some other issues/posts to consider
# - https://github.com/tiangolo/fastapi/issues/1285
# - https://github.com/pydantic/pydantic/issues/8737
# - https://docs.pydantic.dev/2.0/usage/types/custom/#handling-third-party-types
class ArrowType(Arrow):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:

        def validate_with_arrow(value) -> Arrow:
            try:
                arrow_date = arrow.get(value)
                return arrow_date
            except Exception as e:
                raise ValueError(
                    f"Unable to convert value '{value}' to instance of 'Arrow'. "
                    "Value must be instance of 'str' or 'datetime'.",
                    e,
                )

        def arrow_serialization(value: Any, _, info) -> str | Arrow:
            if info.mode == "json":
                return value.format("YYYY-MM-DDTHH:mm:ss.SSSSSSZZ")
            return value

        return core_schema.no_info_after_validator_function(
            function=validate_with_arrow,
            schema=core_schema.str_schema(),
            serialization=core_schema.wrap_serializer_function_ser_schema(
                arrow_serialization, info_arg=True
            ),
        )
