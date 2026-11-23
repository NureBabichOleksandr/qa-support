import re

from sqlalchemy.exc import DBAPIError

USER_ERROR_MIN_NUMBER = 50000

_SQL_SERVER_MESSAGE = re.compile(r"\[SQL Server\](?P<message>.+?)\s\((?P<number>\d+)\)", re.S)


class SqlServerError:

    def __init__(self, exc: DBAPIError) -> None:
        raw = " ".join(str(arg) for arg in getattr(exc.orig, "args", ()) or (exc.orig,))
        match = _SQL_SERVER_MESSAGE.search(raw)
        self.number: int | None = int(match["number"]) if match else None
        self.message: str = match["message"].strip() if match else raw

    @property
    def is_user_error(self) -> bool:
        return self.number is not None and self.number >= USER_ERROR_MIN_NUMBER
