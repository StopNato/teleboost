from .view import ViewCommand

from cleo import Application  # type: ignore

__slots__ = ("application",)

application = Application()
application.add(ViewCommand())
