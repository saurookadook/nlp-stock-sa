import logging

from config import env_config


root_logger = logging.getLogger()


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
    setattr(console_handler, "_name", "root_handler")

    root_handler = next(
        iter(
            filter(
                lambda x: getattr(x, "_name") == getattr(console_handler, "_name"),
                root_logger.handlers,
            )
        )
    )

    if not root_handler:
        root_logger.setLevel(getattr(logging, env_config["log_level"].upper()))
        console_handler.setFormatter(
            logging.Formatter(
                "{asctime} [{name}: {lineno}] [{levelname}]: {message}", style="{"
            )
        )
        root_logger.addHandler(root_handler)
