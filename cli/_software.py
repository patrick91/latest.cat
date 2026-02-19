import re
from dataclasses import dataclass


@dataclass
class Link:
    url: str
    name: str


@dataclass
class Software:
    name: str
    aliases: list[str]
    slug: str
    source: str
    version_naming: str
    repository: str | None
    links: list[Link]
    package: str | None = None

    _namings = {
        # https://github.com/rust-lang/rust/tags
        "basic": re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<patch>\d+))?$"),
        # https://github.com/python/cpython/tags
        "python": re.compile(
            r"^v?(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<patch>\d+))?$"
        ),
        # https://github.com/php/php-src/tags
        "php": re.compile(
            r"^php-?(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<patch>\d+))?$"
        ),
        # https://github.com/apple/swift/tags
        "swift": re.compile(
            r"^swift-(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<patch>\d+))?-RELEASE$"
        ),
        # https://github.com/golang/go/tags
        "go": re.compile(r"^go(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<patch>\d+))?$"),
        # https://github.com/withastro/astro/tags
        "astro": re.compile(
            r"^astro@?(?P<major>\d+)\.(?P<minor>\d+)(?:\.(?P<patch>\d+))?$"
        ),
        # https://github.com/mozilla-firefox/firefox/tags
        "firefox": re.compile(
            r"^FIREFOX_(?P<major>\d+)_(?P<minor>\d+)(?:_(?P<patch>\d+))?_RELEASE$"
        ),
        # https://github.com/chromium/chromium/tags
        "chrome": re.compile(
            r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:\.(?P<build>\d+))?$"
        ),
    }
