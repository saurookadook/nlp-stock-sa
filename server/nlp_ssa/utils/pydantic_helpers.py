import arrow
import datetime
from arrow import Arrow
from pydantic import (
    BaseModel,
    ConfigDict,
    GetCoreSchemaHandler,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    alias_generators,
)
from pydantic.functional_validators import WrapValidator
from pydantic_core import core_schema
from typing import Annotated, Any


def generic_validator_with_default(class_ref, value, info):
    return (
        value
        if value is not None
        else get_default_value_from_field_config(class_ref, info)
    )


def get_default_value_from_field_config(class_ref, info):
    field = class_ref.model_fields[info.field_name]
    return field.default_factory() if callable(field.default_factory) else field.default


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

        def validate_as_or_cast_to_arrow(value) -> Arrow:
            try:
                if isinstance(value, Arrow):
                    return value
                if not isinstance(value, (str, datetime.datetime)):
                    raise TypeError(
                        "Instance of 'string' or 'datetime' required. "
                        f"Received instance of type {type(value)} instead. (value: {value})"
                    )
                return arrow.get(value)
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
            function=validate_as_or_cast_to_arrow,
            schema=core_schema.union_schema(
                [
                    core_schema.str_schema(),
                    core_schema.datetime_schema(),
                    core_schema.is_instance_schema(Arrow),
                ]
            ),
            serialization=core_schema.wrap_serializer_function_ser_schema(
                arrow_serialization, info_arg=True
            ),
        )


SerializerArrowType = Annotated[Arrow, ArrowType]


class BaseResponseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel,
        from_attributes=True,
        populate_by_name=True,
    )
