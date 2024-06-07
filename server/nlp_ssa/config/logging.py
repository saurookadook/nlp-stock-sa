import logging
from enum import Enum

from config import env_vars


BaseLoggerClass = logging.getLoggerClass()


class LogLevelEnum(Enum):

    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    @classmethod
    def level_values(cls):
        return [level.value for level in cls]


class ExtendedLogger(BaseLoggerClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            import os

            raw_window_width, _ = os.get_terminal_size()
        except OSError:
            raw_window_width = 200
        self.raw_window_width = raw_window_width
        self.window_width = (
            raw_window_width - 80
        )  # to account for characters added by logging handlers

    # TODO: type annotation for "int in this Enum"?
    def log_centered(self, log_level: int, msg: str, *args, **kwargs):
        if (
            not isinstance(log_level, int)
            or log_level not in LogLevelEnum.level_values()
        ):
            log_level = LogLevelEnum.INFO.value
        self.log(logging.INFO, msg.center(self.window_width, "-"), *args, **kwargs)

    def log_section_start(self, log_level: int, entity_name: str, *args, **kwargs):
        if (
            not isinstance(log_level, int)
            or log_level not in LogLevelEnum.level_values()
        ):
            log_level = LogLevelEnum.INFO.value
        self.log(
            logging.INFO,
            f" 'Getting `{entity_name}` records...' ".center(self.window_width, "="),
            *args,
            **kwargs,
        )

    def log_section_end(
        self, log_level: int, entity_name: str, entity_count: int, *args, **kwargs
    ):
        if (
            not isinstance(log_level, int)
            or log_level not in LogLevelEnum.level_values()
        ):
            log_level = LogLevelEnum.INFO.value
        self.log(
            logging.INFO,
            f" 'Done with `{entity_name}` records! Total: {entity_count}' ".center(
                self.window_width, "="
            ),
            *args,
            **kwargs,
        )

    def log_info_centered(self, *args, **kwargs):
        self.log_centered(LogLevelEnum.INFO.value, *args, **kwargs)

    def log_info_section_start(self, *args, **kwargs):
        self.log_section_start(LogLevelEnum.INFO.value, *args, **kwargs)

    def log_info_section_end(self, *args, **kwargs):
        self.log_section_end(LogLevelEnum.INFO.value, *args, **kwargs)

    def log_warn_centered(self, *args, **kwargs):
        self.log_centered(LogLevelEnum.WARNING.value, *args, **kwargs)

    def log_warn_section_start(self, *args, **kwargs):
        self.log_section_start(LogLevelEnum.WARNING.value, *args, **kwargs)

    def log_warn_section_end(self, *args, **kwargs):
        self.log_section_end(LogLevelEnum.WARNING.value, *args, **kwargs)

    def log_error_centered(self, *args, **kwargs):
        self.log_centered(LogLevelEnum.ERROR.value, *args, **kwargs)

    def log_error_section_start(self, *args, **kwargs):
        self.log_section_start(LogLevelEnum.ERROR.value, *args, **kwargs)

    def log_error_section_end(self, *args, **kwargs):
        self.log_section_end(LogLevelEnum.ERROR.value, *args, **kwargs)


logging.setLoggerClass(ExtendedLogger)

root_logger = logging.getLogger()


def is_prod():
    return env_vars.ENV.lower() == "prod"


def configure_logging(app_name: str):
    if is_prod():
        console_handler = logging.StreamHandler()
    else:
        from rich.logging import RichHandler

        console_handler = RichHandler(
            show_time=False, rich_tracebacks=True, tracebacks_theme="emacs"
        )

    root_logger.setLevel(getattr(logging, env_vars.LOG_LEVEL.upper()))
    console_handler.setFormatter(
        logging.Formatter(
            "{asctime} [{name}: {lineno}] [{levelname}]: {message}", style="{"
        )
    )
    root_logger.addHandler(console_handler)

    # from rich import inspect

    # print(f"{'-' * 50} root_logger {'-' * 50}")
    # print(inspect(root_logger, all=True))
    # print(f"{'-' * 50} root_logger.handlers {'-' * 50}")
    # print(inspect(root_logger.handlers, all=True))

    # setattr(console_handler, "_name", "root_handler")

    # root_handler = next(
    #     iter(
    #         filter(
    #             lambda x: getattr(x, "_name") == getattr(console_handler, "_name"),
    #             root_logger.handlers,
    #         )
    #     )
    # )

    # if not root_handler:
    #     root_logger.setLevel(getattr(logging, env_config["log_level"].upper()))
    #     console_handler.setFormatter(
    #         logging.Formatter(
    #             "{asctime} [{name}: {lineno}] [{levelname}]: {message}", style="{"
    #         )
    #     )
    #     root_logger.addHandler(root_handler)
