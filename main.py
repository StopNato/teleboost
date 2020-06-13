import distutils.util
import re

import click
from colorama import Fore, Style
from loguru import logger
from requests import Session
from yaspin import yaspin

from misc import key_re, post_url_re, Post
from utils import create_session_using_proxy, read_file_lines


@logger.catch
@click.command()
@click.option("-u", "--url", help="Post URL", required=True)
@click.option(
    "-v", "--view-count", default=-1, help="How many views to add to the post"
)
@click.option(
    "-p",
    "--proxies",
    help="Path to a file with SOCKS5 proxies",
    type=click.Path(exists=True),
    required=True,
)
def main(url: str, proxies: str, view_count: int):
    channel, post_id = re.search(post_url_re, url).groups()
    post = Post(channel, post_id)

    proxies = read_file_lines(proxies)

    if view_count == -1 or len(proxies) < view_count:
        view_count = len(proxies)

    with yaspin() as spinner:
        for proxy in proxies[:view_count]:
            session = create_session_using_proxy(f"socks5h://{proxy}")
            key = get_key(session, post)

            if add_view(session, post, key):
                spinner.text = f"{Fore.GREEN}{proxy}{Style.RESET_ALL}"
            else:
                spinner.text = f"{Fore.RED}{proxy}{Style.RESET_ALL}"


@logger.catch
def get_key(session: Session, post: Post) -> str:
    embed_post = session.get(
        f"https://t.me/{post.channel}/{post.id}", params={"embed": 1}
    ).text
    key = re.search(key_re, embed_post).group(1)

    return key


@logger.catch
def add_view(session: Session, post: Post, key: str) -> bool:
    response = session.get(
        "https://t.me/v/",
        params={"views": key},
        headers={
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"https://t.me/{post.channel}/{post.id}?embed=1",
        },
    ).text

    return distutils.util.strtobool(response)


if __name__ == "__main__":
    main()
