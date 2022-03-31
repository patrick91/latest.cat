import re
from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class Version:
    major: int
    minor: Optional[int] = None
    revision: Optional[int] = None
    build: Optional[str] = None

    def __str__(self):
        out = str(self.major)
        if self.minor is not None:
            out += f".{self.minor}"
            if self.revision is not None:
                out += f".{self.revision}"
        if self.build is not None:
            out += self.build
        return out

    @classmethod
    def from_string(cls, version_string: str):
        pattern = re.compile(r"^(\d+)(?:\.(\d+)(?:\.(\d+)(?:(\w+))?)?)?$")
        if match := pattern.findall(version_string):
            match = [int(x) if x else None for x in match[0]]
            print(match)
            return cls(*match)
