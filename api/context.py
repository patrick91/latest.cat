from typing import TypedDict

from prisma import Prisma


class Context(TypedDict):
    db: Prisma
