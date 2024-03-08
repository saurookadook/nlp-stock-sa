import logging


# TODO: make a better global object lol
config = {"env": "test", "log_level": "NOTSET"}

root_logger = logging.getLogger()


def is_prod():
    return config["env"].lower() == "prod"


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
        root_logger.setLevel(getattr(logging, config["log_level"].upper()))
        console_handler.setFormatter(
            logging.Formatter(
                "{asctime} [{name}: {lineno}] [{levelname}]: {message}", style="{"
            )
        )
        root_logger.addHandler(root_handler)
