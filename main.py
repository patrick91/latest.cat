from starlette.applications import Starlette
from starlette.routing import Route

from data.config import database
from pages.four_oh_four import four_oh_four
from pages.home import homepage
from pages.search import search
from pages.version import fetch_latest

app = Starlette(
    debug=False,
    routes=[
        Route("/", homepage),
        Route("/search", search),
        Route("/404", four_oh_four),
        Route("/{slug}", fetch_latest),
        Route("/{slug}/{version}", fetch_latest),
    ],
    on_startup=[database.connect],
    on_shutdown=[database.disconnect],
)
