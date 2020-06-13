import re
from collections import namedtuple

from random_user_agent.user_agent import UserAgent

user_agent_rotator = UserAgent()

key_re = re.compile(r"data-view=\"(\S*)\"")
post_url_re = re.compile(r"http(?:s|)://\S*/(.*)/(\d*)")

Post = namedtuple("Post", ["channel", "id"])
