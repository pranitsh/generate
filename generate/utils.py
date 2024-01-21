import logging
import os
import pickle
import argparse
import shlex


def manage_object(
    main_dict: str,
    default_object: object,
    new_object: object = None,
    stripped_filename: str = "main",
) -> object:
    """
    Preferably provide a filepath without `.pkl`.
    Optionally, provide a new set to replace the original.
    """
    stripped_filename = stripped_filename.replace(".pkl", "")
    # prevent mixup
    main_dict = main_dict.replace(".pkl", "")
    if os.path.exists(stripped_filename + ".pkl"):
        with open(stripped_filename + ".pkl", "rb") as file:
            item_dict = pickle.load(file)
    else:
        item_dict = {main_dict: default_object}
    if new_object:
        with open(stripped_filename + ".pkl", "wb") as file:
            item_dict[main_dict] = new_object
            pickle.dump(item_dict, file)
        return new_object
    return item_dict.get(main_dict, default_object)

# TODO: Support adding objects individually for convenience.
def manage_list(name: str, new_list: list = None) -> list:
    return manage_object(name, list(), new_list)


def manage_set(name: str, new_set: set = None) -> set:
    return manage_object(name, set(), new_set)


def manage_dict(name: str, new_dict: dict = None) -> dict:
    return manage_object(name, dict(), new_dict)


def create_logger(name="generator.log", logfile=True, filter=False):
    """
    Usage:
        >>> logger = create_logger()
    """
    logged_messages = set()

    def filter_messages(record):
        nonlocal logged_messages
        msg = record.getMessage()
        if msg in logged_messages:
            return False
        logged_messages.add(msg)
        return True

    name = name.replace(".log", "")
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
        )

        if logfile:
            file_handler = logging.FileHandler(name + ".log")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.WARN)
        stream_handler.setFormatter(formatter)
        if filter:
            stream_handler.addFilter(filter_messages)
        logger.addHandler(stream_handler)

    return logger


class CustomArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if status != 0:
            raise ValueError("ArgumentParser error: " + (message or ""))

    def parse_args(self, args=None, namespace=None):
        # Uses shlex.split if args is a string
        if isinstance(args, str):
            args = shlex.split(args)
        return super().parse_args(args, namespace)
