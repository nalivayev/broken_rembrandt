from argparse import ArgumentParser
from typing import Any
from PIL import Image
from os import path, listdir, rename

import logging


class CheckerParser(ArgumentParser):

    __required_group: Any

    def __init__(self):
        ArgumentParser.__init__(self)
        self.__required_group = self.add_argument_group("required arguments")
        self.__required_group.add_argument("-p", "--path", type=str, help="path to check", required=True, default=None)
        self.add_argument('-r', '--recursively', action='store_false', help='including subdirectories')

    def parse_args(self, args=None, namespace=None):
        v_result = ArgumentParser.parse_args(self, args, namespace)
        if not path.isdir(v_result.path):
            self.error('Source path not found')
        return v_result


class CheckerLogger:

    __logger: logging.Logger

    def __init__(self):
        self.__logger = logging.getLogger()
        self.__logger.setLevel(logging.INFO)
        v_formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(message)s", datefmt="%Y.%m.%d %H:%M:%S")
        v_handler = logging.FileHandler(f"{path.splitext(__file__)[0]}.log", mode="w")
        v_handler.setFormatter(v_formatter)
        self.__logger.addHandler(v_handler)
        v_handler = logging.StreamHandler()
        v_handler.setFormatter(v_formatter)
        self.__logger.addHandler(v_handler)

    def info(self, p_message: str) -> None:
        self.__logger.info(p_message)


class FileChecker:

    def do(self, p_file_name: str):
        v_result = True
        try:
            v_image = Image.open(p_file_name)
            v_image.verify()
            v_image.close()
            v_image = Image.open(p_file_name)
            v_image.transpose(Image.FLIP_LEFT_RIGHT)
            v_image.close()
        except Exception:
            v_result = False
        return v_result


class PathChecker:

    __logger: CheckerLogger
    __checker: FileChecker

    def __add_log_message(self, p_message):
        if self.__logger is not None:
            self.__logger.info(p_message)

    def __do_recursively(self, p_path, p_recursively):
        self.__add_log_message(f"Check the path {p_path}")
        v_list = listdir(p_path)
        while len(v_list) > 0:
            v_path = path.join(p_path, v_list[0])
            if path.isfile(v_path):
                if not self.__checker.do(v_path):
                    v_name, v_extension = path.splitext(v_path)
                    try:
                        self.__add_log_message(f"File {v_list[0]} is corrupt")
                        v_name = f"{v_name}.corrupt{v_extension}"
                        rename(v_path, v_name)
                    except Exception:
                        self.__add_log_message(f"Error rename file {v_list[0]}")
                    else:
                        self.__add_log_message(f"File {v_list[0]} renamed to {v_name}")
                else:
                    self.__add_log_message(f"File {v_list[0]} is good")
            else:
                if p_recursively and path.isdir(v_path):
                    self.__do_recursively(v_path, p_recursively)
            v_list.pop(0)

    def do(self, p_logger: CheckerLogger, p_path, p_recursively):
        self.__logger = p_logger
        self.__checker = FileChecker()
        self.__do_recursively(path.abspath(p_path), p_recursively)
