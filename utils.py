from typing import List

from requests import Session

from misc import user_agent_rotator


def create_session_using_proxy(proxy: str) -> Session:
    session = Session()
    session.proxies = {"http": proxy, "https": proxy}
    session.headers = {"User-Agent": user_agent_rotator.get_random_user_agent()}

    return session


def get_ip(session: Session) -> str:
    return session.get("https://ident.me/").text


def read_file_lines(path: str) -> List[str]:
    lines = []

    with open(path) as file:
        for line in file.read().splitlines():
            line = line.strip()

            if line != "" and not line.startswith("#"):
                lines.append(line)

    return lines
