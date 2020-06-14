from pydantic import BaseModel
from typing import Optional

__all__ = ("ViewResult",)


class ViewResult(BaseModel):
    ok: bool
    proxy: str
    error: Optional[str] = None
