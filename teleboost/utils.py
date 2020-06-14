import re
from pathlib import Path
from typing import List, Tuple, Union

from .misc import post_url_re


def parse_telegram_post_url(url: str) -> Tuple[str, int]:
    res = re.search(post_url_re, url)
    if res is None:
        raise Exception("Invalid url")
    channel, post_id = res.groups()
    return channel, int(post_id)


def read_file_lines(path: Union[str, Path]) -> List[str]:
    lines = []

    with open(path) as file:
        for line in file.read().splitlines():
            line = line.strip()

            if line != "" and not line.startswith("#"):
                lines.append(line)

    return lines
