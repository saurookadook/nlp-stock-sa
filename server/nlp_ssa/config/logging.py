import logging

from config import env_config


root_logger = logging.getLogger()


class ExtendedLogger(logging.getLoggerClass()):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        import os

        raw_window_width, _ = os.get_terminal_size()
        self.raw_window_width = raw_window_width
        self.window_width = (
            raw_window_width - 80
        )  # to account for characters added by logging handlers

    def log_info_centered(self, msg, *args, **kwargs):
        self.info(msg.center(self.window_width, "-"), *args, **kwargs)

    def log_info_section_start(self, entity_name: str, *args, **kwargs):
        self.info(
            f" 'Getting `{entity_name}` records...' ".center(self.window_width, "="),
            *args,
            **kwargs,
        )

    def log_info_section_end(
        self, entity_name: str, entity_count: int, *args, **kwargs
    ):
        self.info(
            f" 'Done with `{entity_name}` records! Total: {entity_count}' ".center(
                self.window_width, "="
            ),
            *args,
            **kwargs,
        )


logging.setLoggerClass(ExtendedLogger)


def is_prod():
    return env_config["env"].lower() == "prod"


def configure_logging(app_name: str):
    if is_prod():
        console_handler = logging.StreamHandler()
    else:
        from rich.logging import RichHandler

        console_handler = RichHandler(
            show_time=False, rich_tracebacks=True, tracebacks_theme="emacs"
        )

    root_logger.setLevel(getattr(logging, env_config["log_level"].upper()))
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
